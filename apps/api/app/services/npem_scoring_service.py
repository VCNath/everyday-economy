from datetime import date
import hashlib

from app.models.economic import (
    JobRunModel,
    NpemNormalizedScoreModel,
    NpemProvenanceModel,
    NpemProvincialAdjustmentModel,
    NpemQualityComponentModel,
    NpemScoreModel,
    utc_now,
)
from app.npem.variable_dictionary import COMPONENTS, GROUPS, MODEL_VERSION
from app.services.npem_confidence_service import NpemConfidenceService
from app.services.npem_group_service import NpemGroupService
from app.services.npem_normalization_service import NpemNormalizationService
from app.services.npem_scenario_service import NpemScenarioService
from app.services.npem_variable_service import NpemVariableService
from app.services.seed_data import LOCATIONS


PROVINCE_CODES = [loc.id for loc in LOCATIONS if loc.id != "CA"]
GROUP_CODES = [group["group_code"] for group in GROUPS]


class NpemScoringService:
    def __init__(self, session):
        self.session = session
        self.normalizer = NpemNormalizationService()
        self.confidence = NpemConfidenceService()

    def seed_methodology(self) -> None:
        NpemVariableService(self.session).seed_defaults()
        NpemGroupService(self.session).seed_defaults()
        NpemScenarioService(self.session).seed_defaults()

    def _demo_raw_value(self, geography_code: str, group_code: str, component_code: str) -> float:
        geo_index = PROVINCE_CODES.index(geography_code) if geography_code in PROVINCE_CODES else 0
        group_index = GROUP_CODES.index(group_code) if group_code in GROUP_CODES else 0
        component_index = list(COMPONENTS).index(component_code)
        base = 40 + (geo_index * 2.6) + (group_index * 1.9) + (component_index * 1.3)
        if component_code in {"GCI", "DSI"}:
            return base + (8 if group_code in {"CP_FAM", "SWA_SINGLE"} else 0)
        if component_code == "HRI":
            return base + (12 if group_code in {"RENTER", "YA_UC", "LP_FAM"} else 0)
        if component_code == "ECI":
            return base + (14 if group_code == "STUDENT" else 0)
        if component_code == "DLI":
            return base + (10 if group_code in {"YA_UC", "STUDENT"} else 0)
        return base

    def calculate_demo_scores(self, reference_year: int = 2025) -> dict[str, int]:
        self.seed_methodology()
        component_values: dict[str, dict[tuple[str, str], float]] = {
            component: {
                (geo, group): self._demo_raw_value(geo, group, component)
                for geo in PROVINCE_CODES
                for group in GROUP_CODES
            }
            for component in COMPONENTS
        }
        normalized_by_key: dict[tuple[str, str, str], float] = {}
        norm_rows = 0
        for component_code, values in component_values.items():
            normalized = self.normalizer.normalize_component_values(component_code, values)
            for (geo, group), payload in normalized.items():
                row = (
                    self.session.query(NpemNormalizedScoreModel)
                    .filter_by(geography_code=geo, reference_year=reference_year, group_code=group, component_code=component_code, model_version=MODEL_VERSION)
                    .one_or_none()
                ) or NpemNormalizedScoreModel(geography_code=geo, reference_year=reference_year, group_code=group, component_code=component_code, model_version=MODEL_VERSION)
                row.raw_value = payload["raw_value"]
                row.winsor_p5 = payload["winsor_p5"]
                row.winsor_p95 = payload["winsor_p95"]
                row.normalized_score = payload["normalized_score"]
                row.inversion_applied = payload["inversion_applied"]
                row.imputation_level = 2
                row.confidence_component = 68
                self.session.merge(row)
                normalized_by_key[(geo, group, component_code)] = float(payload["normalized_score"])
                norm_rows += 1
        self.session.commit()

        paf_values = self._store_paf(reference_year)
        scenario_service = NpemScenarioService(self.session)
        scenarios = scenario_service.list()
        score_rows = 0
        for scenario in scenarios:
            weights = scenario_service.weights(scenario.scenario_code)
            by_geo: dict[str, list[NpemScoreModel]] = {}
            for geo in PROVINCE_CODES:
                by_geo[geo] = []
                for group in GROUP_CODES:
                    base = sum(normalized_by_key[(geo, group, component)] * weights[component] for component in weights)
                    paf = paf_values.get(geo, 1.0)
                    final = round(max(0, min(100, base * paf)), 2)
                    quality = self._store_quality(geo, group, reference_year)
                    row = (
                        self.session.query(NpemScoreModel)
                        .filter_by(geography_code=geo, reference_year=reference_year, group_code=group, scenario_code=scenario.scenario_code, model_version=MODEL_VERSION)
                        .one_or_none()
                    ) or NpemScoreModel(geography_code=geo, reference_year=reference_year, group_code=group, scenario_code=scenario.scenario_code, model_version=MODEL_VERSION)
                    row.base_composite = round(base, 2)
                    row.paf_value = paf
                    row.final_score = final
                    row.confidence_score = quality.confidence_score
                    row.confidence_grade = quality.confidence_grade
                    persisted = self.session.merge(row)
                    self.session.flush()
                    self._store_provenance(persisted)
                    by_geo[geo].append(persisted)
                    score_rows += 1
                for rank, row in enumerate(sorted(by_geo[geo], key=lambda score: float(score.final_score or 0), reverse=True), start=1):
                    row.score_rank_within_geo = rank
                    self.session.merge(row)
        self.session.commit()
        return {"normalized_rows": norm_rows, "score_rows": score_rows}

    def _store_paf(self, reference_year: int) -> dict[str, float]:
        ratios = {}
        for geo in PROVINCE_CODES:
            idx = PROVINCE_CODES.index(geo)
            mbm = 42000 + idx * 1300
            modeled = 40000 + idx * 1150
            ratios[geo] = mbm / modeled
        median_u = sorted(ratios.values())[len(ratios) // 2]
        paf_values = {}
        for geo, ratio in ratios.items():
            adjustment = max(-0.05, min(0.05, 0.25 * ((ratio - median_u) / median_u)))
            paf = round(1 + adjustment, 4)
            row = (
                self.session.query(NpemProvincialAdjustmentModel)
                .filter_by(geography_code=geo, reference_year=reference_year)
                .one_or_none()
            ) or NpemProvincialAdjustmentModel(geography_code=geo, reference_year=reference_year)
            row.mbm_total = round(42000 + PROVINCE_CODES.index(geo) * 1300, 2)
            row.modeled_essentials_prov = round(40000 + PROVINCE_CODES.index(geo) * 1150, 2)
            row.undercoverage_ratio = ratio
            row.paf_value = paf
            self.session.merge(row)
            paf_values[geo] = paf
        self.session.commit()
        return paf_values

    def _store_quality(self, geo: str, group: str, reference_year: int) -> NpemQualityComponentModel:
        overlay = group in {"INDIG", "IMM", "RIMM", "STUDENT", "RENTER"}
        territory = geo in {"CA-YT", "CA-NT", "CA-NU"}
        suppression = 0.15 if group == "INDIG" and territory else 0.08 if overlay else 0.02
        proxy_share = 0.45 if group in {"INDIG", "RIMM", "STUDENT"} else 0.32 if overlay else 0.24
        coverage = max(0.45, 0.82 - suppression)
        recency = 0.78
        directness = max(0.40, 1 - proxy_share)
        reliability = 0.78 if not territory else 0.68
        score = self.confidence.score(coverage=coverage, recency=recency, directness=directness, reliability=reliability, suppression_penalty=suppression)
        grade = self.confidence.grade(score)
        row = (
            self.session.query(NpemQualityComponentModel)
            .filter_by(geography_code=geo, reference_year=reference_year, group_code=group)
            .one_or_none()
        ) or NpemQualityComponentModel(geography_code=geo, reference_year=reference_year, group_code=group)
        row.coverage_ratio = coverage
        row.recency_score = recency
        row.directness_score = directness
        row.reliability_score = reliability
        row.suppression_penalty = suppression
        row.proxy_share = proxy_share
        row.confidence_score = score
        row.confidence_grade = grade
        self.session.merge(row)
        self.session.flush()
        return row

    def _store_provenance(self, score: NpemScoreModel) -> None:
        existing = self.session.query(NpemProvenanceModel).filter_by(score_id=score.score_id, transform_step="npem_demo_scoring").one_or_none()
        if existing:
            return
        source_text = f"{score.geography_code}:{score.group_code}:{score.scenario_code}:{score.reference_year}:{MODEL_VERSION}"
        self.session.add(
            NpemProvenanceModel(
                score_id=score.score_id,
                source_system="Everyday Economy deterministic demo scaffold",
                source_series_id="npem_demo_v1",
                citation_text="Everyday Economy. National Personal Economic Model demo scaffold, model version npem_v1_demo_2026. Uses seeded/proxy data for development display only.",
                release_date=date(score.reference_year, 12, 31),
                access_date=date.today(),
                transform_step="npem_demo_scoring",
                licence_note="Demo methodology scaffold. Replace with source-specific licence notes as production adapters land.",
                source_url="https://everyday-economy.local/docs/npem-methodology",
                source_hash=hashlib.sha256(source_text.encode()).hexdigest(),
            )
        )

    def rows(self, province: str = "AB", year: int = 2025, scenario: str = "baseline") -> list[NpemScoreModel]:
        geo = self._geo_code(province)
        rows = (
            self.session.query(NpemScoreModel)
            .filter_by(geography_code=geo, reference_year=year, scenario_code=scenario)
            .order_by(NpemScoreModel.score_rank_within_geo)
            .all()
        )
        if not rows:
            self.calculate_demo_scores(year)
            rows = (
                self.session.query(NpemScoreModel)
                .filter_by(geography_code=geo, reference_year=year, scenario_code=scenario)
                .order_by(NpemScoreModel.score_rank_within_geo)
                .all()
            )
        return rows

    def components_for(self, geography_code: str, group_code: str, year: int) -> list[NpemNormalizedScoreModel]:
        return (
            self.session.query(NpemNormalizedScoreModel)
            .filter_by(geography_code=geography_code, group_code=group_code, reference_year=year, model_version=MODEL_VERSION)
            .order_by(NpemNormalizedScoreModel.component_code)
            .all()
        )

    def quality_for(self, geography_code: str, group_code: str, year: int) -> NpemQualityComponentModel | None:
        return self.session.query(NpemQualityComponentModel).filter_by(geography_code=geography_code, group_code=group_code, reference_year=year).one_or_none()

    def provenance_for(self, score_id: str) -> list[NpemProvenanceModel]:
        return list(self.session.query(NpemProvenanceModel).filter_by(score_id=score_id).all())

    def _geo_code(self, province: str) -> str:
        return province if province.startswith("CA-") else f"CA-{province}"

    def run_with_job(self) -> dict[str, int]:
        run = JobRunModel(job_type="calculation", job_name="calculate_npem", status="running", trigger_source="cli")
        self.session.add(run)
        self.session.commit()
        try:
            result = self.calculate_demo_scores()
            run.status = "succeeded"
            run.finished_at = utc_now()
            run.rows_updated = result["score_rows"]
            self.session.commit()
            return result
        except Exception as exc:
            run.status = "failed"
            run.finished_at = utc_now()
            run.error_message = str(exc)
            self.session.commit()
            raise
