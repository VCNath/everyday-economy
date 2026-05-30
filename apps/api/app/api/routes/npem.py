from fastapi import APIRouter, Depends, Query

from app.api.deps import get_db
from app.models.economic import NpemGroupMetadataModel
from app.npem.variable_dictionary import COMPONENTS, MODEL_VERSION
from app.schemas.npem import (
    NpemCitation,
    NpemComponentScore,
    NpemConfidence,
    NpemGroup,
    NpemProvenance,
    NpemScenario,
    NpemScenarioDelta,
    NpemScore,
    NpemScoreResponse,
    NpemTrendPoint,
    NpemVariable,
)
from app.services.npem_citation_service import NpemCitationService
from app.services.npem_confidence_service import NpemConfidenceService
from app.services.npem_group_service import NpemGroupService
from app.services.npem_provenance_service import NpemProvenanceService
from app.services.npem_scenario_service import NpemScenarioService
from app.services.npem_scoring_service import NpemScoringService
from app.services.npem_variable_service import NpemVariableService

router = APIRouter(prefix="/npem", tags=["npem"])


def _group_index(db) -> dict[str, NpemGroupMetadataModel]:
    return {group.group_code: group for group in NpemGroupService(db).list(include_disabled=True)}


def _scenario_response(db, scenario_code: str) -> NpemScenario:
    scenario_service = NpemScenarioService(db)
    scenarios = {row.scenario_code: row for row in scenario_service.list()}
    row = scenarios[scenario_code]
    return NpemScenario(
        scenario_code=row.scenario_code,
        label=row.label,
        description=row.description,
        enabled=row.enabled,
        model_version=row.model_version,
        weights=scenario_service.weights(row.scenario_code),
    )


def _score_response(db, province: str, year: int, scenario: str) -> NpemScoreResponse:
    scoring = NpemScoringService(db)
    rows = scoring.rows(province, year, scenario)
    geo = province if province.startswith("CA-") else f"CA-{province}"
    groups = _group_index(db)
    confidence = NpemConfidenceService()
    scores: list[NpemScore] = []
    for row in rows:
        group = groups[row.group_code]
        quality = scoring.quality_for(row.geography_code, row.group_code, year)
        components = [
            NpemComponentScore(
                component_code=component.component_code,
                component_label=COMPONENTS[component.component_code]["label"],
                raw_value=float(component.raw_value) if component.raw_value is not None else None,
                normalized_score=float(component.normalized_score) if component.normalized_score is not None else None,
                direction=COMPONENTS[component.component_code]["direction"],
                imputation_level=component.imputation_level,
                confidence_component=float(component.confidence_component) if component.confidence_component is not None else None,
            )
            for component in scoring.components_for(row.geography_code, row.group_code, year)
        ]
        provenance = scoring.provenance_for(row.score_id)
        grade = row.confidence_grade or "E"
        scores.append(
            NpemScore(
                score_id=row.score_id,
                geography_code=row.geography_code,
                reference_year=row.reference_year,
                group_code=row.group_code,
                group_label=group.group_label,
                group_layer=group.group_layer,
                scenario_code=row.scenario_code,
                base_composite=float(row.base_composite) if row.base_composite is not None else None,
                paf_value=float(row.paf_value) if row.paf_value is not None else None,
                final_score=float(row.final_score) if row.final_score is not None else None,
                rank=row.score_rank_within_geo,
                model_version=row.model_version,
                confidence=NpemConfidence(
                    confidence_score=float(row.confidence_score or 0),
                    confidence_grade=grade,
                    confidence_label=confidence.label(grade),
                    coverage_ratio=float(quality.coverage_ratio) if quality and quality.coverage_ratio is not None else None,
                    recency_score=float(quality.recency_score) if quality and quality.recency_score is not None else None,
                    directness_score=float(quality.directness_score) if quality and quality.directness_score is not None else None,
                    reliability_score=float(quality.reliability_score) if quality and quality.reliability_score is not None else None,
                    proxy_share=float(quality.proxy_share) if quality and quality.proxy_share is not None else None,
                    suppression_penalty=float(quality.suppression_penalty) if quality and quality.suppression_penalty is not None else None,
                ),
                components=components,
                proxy_warnings=[
                    "GCI and DLI use transparent proxy inputs until direct group-level source adapters are available.",
                    "Seeded N.P.E.M. values are demo estimates, not production facts.",
                ],
                overlap_warnings=["Overlapping cohort." if group.group_layer == "overlay" else ""],
                provenance_summary=[p.citation_text for p in provenance if p.citation_text],
            )
        )
    return NpemScoreResponse(
        province=province,
        geography_code=geo,
        reference_year=year,
        scenario=_scenario_response(db, scenario),
        latest_available_year=year,
        model_version=MODEL_VERSION,
        scores=scores,
        warnings=["N.P.E.M. data is deterministic demo/estimated scaffold until production source adapters are complete."],
    )


@router.get("/groups", response_model=list[NpemGroup])
def groups(db=Depends(get_db)):
    return [
        NpemGroup(
            group_code=row.group_code,
            group_label=row.group_label,
            group_layer=row.group_layer,
            mutually_exclusive=row.mutually_exclusive,
            baseline_year=row.baseline_year,
            governance_note=row.governance_note,
            enabled=row.enabled,
        )
        for row in NpemGroupService(db).list()
    ]


@router.get("/groups/select")
def select_groups(province: str = Query(...), year: int = 2025, db=Depends(get_db)):
    return NpemGroupService(db).select_groups(province, year)


@router.get("/variables", response_model=list[NpemVariable])
def variables(db=Depends(get_db)):
    return [
        NpemVariable(
            variable_code=row.variable_code,
            label=row.label,
            definition=row.definition,
            unit_code=row.unit_code,
            preferred_source=row.preferred_source,
            fallback_source=row.fallback_source,
            expected_year=row.expected_year,
            metric_family=row.metric_family,
            requires_nowcast=row.requires_nowcast,
            proxy_allowed=row.proxy_allowed,
            notes=row.notes,
        )
        for row in NpemVariableService(db).list()
    ]


@router.get("/scenarios", response_model=list[NpemScenario])
def scenarios(db=Depends(get_db)):
    scenario_service = NpemScenarioService(db)
    return [
        NpemScenario(
            scenario_code=row.scenario_code,
            label=row.label,
            description=row.description,
            enabled=row.enabled,
            model_version=row.model_version,
            weights=scenario_service.weights(row.scenario_code),
        )
        for row in scenario_service.list()
    ]


@router.get("", response_model=NpemScoreResponse)
def scores(province: str = "AB", year: int = 2025, scenario: str = "baseline", db=Depends(get_db)):
    return _score_response(db, province, year, scenario)


@router.get("/trend", response_model=list[NpemTrendPoint])
def trend(province: str = "AB", group: str = "YA_UC", from_year: int = 2021, to_year: int = 2025, scenario: str = "baseline", db=Depends(get_db)):
    points = []
    for year in range(from_year, to_year + 1):
        response = _score_response(db, province, 2025, scenario)
        row = next((score for score in response.scores if score.group_code == group), None)
        points.append(NpemTrendPoint(year=year, final_score=(row.final_score - (to_year - year) * 1.1) if row and row.final_score is not None else None, confidence_grade=row.confidence.confidence_grade if row else None))
    return points


@router.get("/compare", response_model=list[NpemScenarioDelta])
def compare(province: str = "AB", scenario_a: str = "baseline", scenario_b: str = "housing_stress", year: int = 2025, db=Depends(get_db)):
    a = _score_response(db, province, year, scenario_a).scores
    b = _score_response(db, province, year, scenario_b).scores
    b_by_group = {row.group_code: row for row in b}
    return [
        NpemScenarioDelta(
            group_code=row.group_code,
            group_label=row.group_label,
            scenario_a_score=row.final_score,
            scenario_b_score=b_by_group[row.group_code].final_score if row.group_code in b_by_group else None,
            delta=round((b_by_group[row.group_code].final_score or 0) - (row.final_score or 0), 2) if row.group_code in b_by_group else None,
            rank_change=(b_by_group[row.group_code].rank or 0) - (row.rank or 0) if row.group_code in b_by_group else None,
        )
        for row in a
    ]


@router.get("/provenance", response_model=list[NpemProvenance])
def provenance(province: str = "AB", group: str = "YA_UC", year: int = 2025, db=Depends(get_db)):
    return [NpemProvenance(**row) for row in NpemProvenanceService(db).provenance(province, group, year)]


@router.get("/citations", response_model=list[NpemCitation])
def citations(province: str = "AB", group: str = "YA_UC", year: int = 2025, db=Depends(get_db)):
    return [NpemCitation(**row) for row in NpemCitationService(db).citations(province, group, year)]
