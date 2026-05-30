from dataclasses import dataclass
from datetime import date
import hashlib
import json
import logging

from app.connectors.bank_of_canada import BankOfCanadaConnector
from app.connectors.bank_of_canada_series import BANK_OF_CANADA_SERIES
from app.connectors.statcan import StatCanConnector
from app.config import get_settings
from app.models.economic import SourceRefreshRunModel, utc_now
from app.services.repository import EconomicRepository
from app.services.seed_registry import STATCAN_GEO_NAMES, seed_reference_data
from app.services.seed_data import BASKET_ITEMS, METRICS
from app.transformations.affordability_score import calculate_affordability_score_v1
from app.transformations.calculate_mom import calculate_mom
from app.transformations.calculate_yoy import calculate_yoy
from app.transformations.normalize_observations import map_labour_characteristic

logger = logging.getLogger(__name__)


def month_date(value: str) -> date:
    if len(value) == 7:
        return date.fromisoformat(f"{value}-01")
    return date.fromisoformat(value)


def add_months(period: date, months: int) -> date:
    month = period.month - 1 + months
    year = period.year + month // 12
    month = month % 12 + 1
    return date(year, month, 1)


@dataclass
class IngestResult:
    job_name: str
    status: str
    rows_fetched: int
    rows_inserted: int
    rows_updated: int
    latest_period: date | None = None
    error_message: str | None = None


class EconomicIngestionService:
    cpi_products = {
        "All-items": ("cpi_all_items_index", "index"),
        "Food": ("cpi_food_index", "index"),
        "Shelter": ("cpi_shelter_index", "index"),
    }

    derived_cpi = {
        "cpi_all_items_index": "cpi_all_items_yoy",
        "cpi_food_index": "cpi_food_yoy",
        "cpi_shelter_index": "cpi_shelter_yoy",
    }

    province_gas_city = {
        "CA-NL": "St. John's, Newfoundland and Labrador",
        "CA-PE": "Charlottetown and Summerside, Prince Edward Island",
        "CA-NS": "Halifax, Nova Scotia",
        "CA-NB": "Saint John, New Brunswick",
        "CA-QC": "Montréal, Quebec",
        "CA-ON": "Toronto, Ontario",
        "CA-MB": "Winnipeg, Manitoba",
        "CA-SK": "Regina, Saskatchewan",
        "CA-AB": "Calgary, Alberta",
        "CA-BC": "Vancouver, British Columbia",
    }

    basket_products = {
        "milk": ("Milk, 2 litres", 4),
        "eggs": ("Eggs, 1 dozen", 2),
        "bread": ("White bread, 675 grams", 6),
        "chicken": ("Whole chicken, per kilogram", 4),
        "ground_beef": ("Ground beef, per kilogram", 3),
        "rice": ("Rice, 2 kilograms", 2),
        "apples": ("Apples, per kilogram", 5),
        "coffee": ("Coffee, 300 grams", 2),
        # Legacy item ids preserved for older fallback/UI data.
        "whole_chicken_kg": ("Whole chicken, per kilogram", 4),
        "eggs_dozen": ("Eggs, 1 dozen", 2),
        "apples_kg": ("Apples, per kilogram", 5),
        "bread_loaf": ("White bread, 675 grams", 6),
        "milk_2l": ("Milk, 2 litres", 4),
    }

    def __init__(
        self,
        session,
        statcan: StatCanConnector | None = None,
        bank_of_canada: BankOfCanadaConnector | None = None,
    ):
        self.session = session
        self.repo = EconomicRepository(session)
        self.settings = get_settings()
        self.statcan = statcan or StatCanConnector(base_url=self.settings.statcan_base_url)
        self.bank_of_canada = bank_of_canada or BankOfCanadaConnector(base_url=self.settings.bank_of_canada_base_url)
        self.geo_to_location = {name: location_id for location_id, name in STATCAN_GEO_NAMES.items()}
        self.gas_geo_to_location = {name: location_id for location_id, name in self.province_gas_city.items()}

    def initialize_reference_data(self) -> None:
        seed_reference_data(self.session)

    def ingest_cpi(self, recent_months: int = 30) -> IngestResult:
        return self._run_job("ingest_statcan_cpi", lambda: self._ingest_cpi(recent_months))

    def ingest_gas(self, recent_months: int = 30) -> IngestResult:
        return self._run_job("ingest_statcan_gas", lambda: self._ingest_gas(recent_months))

    def ingest_labour(self, recent_months: int = 30) -> IngestResult:
        return self._run_job("ingest_statcan_labour", lambda: self._ingest_labour(recent_months))

    def ingest_food_prices(self, recent_months: int = 15) -> IngestResult:
        return self._run_job("ingest_statcan_food_prices", lambda: self._ingest_food_prices(recent_months))

    def ingest_bank_of_canada(self) -> IngestResult:
        return self._run_job("ingest_bank_of_canada", self._ingest_bank_of_canada)

    def calculate_changes(self) -> None:
        for indicator_id in [
            "cpi_all_items_index",
            "cpi_food_index",
            "cpi_shelter_index",
            "gas_regular_cents_litre",
            "unemployment_rate",
            "employment_rate",
            "participation_rate",
            "basic_basket_monthly_cost",
        ]:
            self._calculate_indicator_changes(indicator_id)

        for source_indicator, derived_indicator in self.derived_cpi.items():
            self._derive_yoy_indicator(source_indicator, derived_indicator)
        self._derive_yoy_indicator("basic_basket_monthly_cost", "basic_basket_yoy")
        self.calculate_affordability_scores()
        self.session.commit()

    def build_baskets(self) -> int:
        # Build a basic monthly basket when enough retail product rows exist.
        latest = self.repo.latest_period("price_chicken") or self.repo.latest_period("price_whole_chicken_kg")
        if latest is None:
            return self._seed_fallback_baskets()

        location_ids = [loc.id for loc in self.repo.locations() if loc.id != "CA"]
        built = 0
        for location_id in ["CA", *location_ids]:
            total = 0.0
            coverage = 0
            for item_id, (_source_name, quantity) in self.basket_products.items():
                obs = self.repo.observation(f"price_{item_id}", location_id, latest)
                if obs and obs.value is not None:
                    total += float(obs.value) * quantity
                    coverage += 1
            if coverage:
                self.repo.upsert_observation(
                    indicator_id="basic_basket_monthly_cost",
                    location_id=location_id,
                    period=latest,
                    value=round(total, 2),
                    unit="CAD/month",
                    source_id="internal",
                    source_table_id="18-10-0245-01",
                    is_estimated=coverage < len(self.basket_products),
                )
                built += 1
        self.session.commit()
        self._calculate_indicator_changes("basic_basket_monthly_cost")
        self._derive_yoy_indicator("basic_basket_monthly_cost", "basic_basket_yoy")
        self.session.commit()
        return built

    def _run_job(self, job_name: str, fn) -> IngestResult:
        run = SourceRefreshRunModel(source_id="statcan", job_name=job_name, status="running")
        if "bank_of_canada" in job_name:
            run.source_id = "bank_of_canada"
        self.session.add(run)
        self.session.commit()
        try:
            result = fn()
            run.status = result.status
            run.rows_fetched = result.rows_fetched
            run.rows_inserted = result.rows_inserted
            run.rows_updated = result.rows_updated
            run.error_message = result.error_message
            run.finished_at = utc_now()
            self.session.commit()
            return result
        except Exception as exc:
            self.session.rollback()
            run.status = "error"
            run.error_message = str(exc)
            run.finished_at = utc_now()
            self.session.add(run)
            self.session.commit()
            return IngestResult(job_name, "error", 0, 0, 0, error_message=str(exc))

    def _period_cutoff(self, latest_period: date, recent_months: int) -> date:
        return add_months(latest_period, -recent_months)

    def _latest_period_in_rows(self, rows, table_key: str) -> date | None:
        latest = None
        for row in rows:
            try:
                period = month_date(row["REF_DATE"])
            except ValueError:
                continue
            latest = period if latest is None or period > latest else latest
        return latest

    def _ingest_cpi(self, recent_months: int) -> IngestResult:
        content = self.statcan.fetch_table_zip("cpi")
        rows = list(self.statcan.iter_rows_from_zip_bytes(content, "cpi"))
        latest = self._latest_period_in_rows(rows, "cpi")
        self._store_raw_payload("statcan", "cpi", content, latest, {"row_count": len(rows), "table_id": "18-10-0004-01"})
        cutoff = self._period_cutoff(latest, recent_months) if latest else None
        fetched = inserted = updated = 0
        unmapped_locations = set()

        for row in rows:
            product = row.get("Products and product groups")
            location_id = self.geo_to_location.get(row.get("GEO", ""))
            if location_id is None:
                if row.get("GEO"):
                    unmapped_locations.add(row.get("GEO"))
                continue
            if product not in self.cpi_products:
                continue
            if not row.get("VALUE"):
                self.repo.add_quality_flag(flag_type="missing_value", severity="warning", message=f"Missing CPI value for {location_id} {product} {row.get('REF_DATE')}")
                continue
            period = month_date(row["REF_DATE"])
            if cutoff and period < cutoff:
                continue
            indicator_id, unit = self.cpi_products[product]
            _obs, was_inserted = self.repo.upsert_observation(
                indicator_id=indicator_id,
                location_id=location_id,
                period=period,
                value=float(row["VALUE"]),
                unit=unit,
                source_id="statcan",
                source_table_id="18-10-0004-01",
                source_series_id=row.get("VECTOR"),
            )
            fetched += 1
            inserted += 1 if was_inserted else 0
            updated += 0 if was_inserted else 1
        self.repo.upsert_freshness(source_id="statcan", dataset_id="cpi", latest_period=latest, status="healthy")
        for geo in sorted(unmapped_locations):
            self.repo.add_quality_flag(flag_type="unmapped_location", severity="warning", message=f"Unmapped StatCan CPI GEO: {geo}")
        self.session.commit()
        return IngestResult("ingest_statcan_cpi", "success", fetched, inserted, updated, latest)

    def _ingest_gas(self, recent_months: int) -> IngestResult:
        content = self.statcan.fetch_table_zip("gas")
        rows = list(self.statcan.iter_rows_from_zip_bytes(content, "gas"))
        latest = self._latest_period_in_rows(rows, "gas")
        self._store_raw_payload("statcan", "gasoline", content, latest, {"row_count": len(rows), "table_id": "18-10-0001-01"})
        cutoff = self._period_cutoff(latest, recent_months) if latest else None
        fetched = inserted = updated = 0
        gas_name = "Regular unleaded gasoline at self service filling stations"
        fallback_gas_name = "Regular unleaded gasoline at full service filling stations"

        for row in rows:
            fuel = row.get("Type of fuel")
            location_id = self.gas_geo_to_location.get(row.get("GEO", ""))
            if fuel not in {gas_name, fallback_gas_name} or location_id is None or not row.get("VALUE"):
                continue
            period = month_date(row["REF_DATE"])
            if cutoff and period < cutoff:
                continue
            _obs, was_inserted = self.repo.upsert_observation(
                indicator_id="gas_regular_cents_litre",
                location_id=location_id,
                period=period,
                value=float(row["VALUE"]),
                unit="cents/litre",
                source_id="statcan",
                source_table_id="18-10-0001-01",
                source_series_id=row.get("VECTOR"),
            )
            fetched += 1
            inserted += 1 if was_inserted else 0
            updated += 0 if was_inserted else 1
        self.repo.upsert_freshness(source_id="statcan", dataset_id="gasoline", latest_period=latest, status="healthy")
        self.session.commit()
        return IngestResult("ingest_statcan_gas", "success", fetched, inserted, updated, latest)

    def _ingest_labour(self, recent_months: int) -> IngestResult:
        content = self.statcan.fetch_table_zip("labour")
        rows = list(self.statcan.iter_rows_from_zip_bytes(content, "labour"))
        latest = self._latest_period_in_rows(rows, "labour")
        self._store_raw_payload("statcan", "labour_force", content, latest, {"row_count": len(rows), "table_id": "14-10-0287-01"})
        cutoff = self._period_cutoff(latest, recent_months) if latest else None
        fetched = inserted = updated = 0

        for row in rows:
            location_id = self.geo_to_location.get(row.get("GEO", ""))
            indicator_id = map_labour_characteristic(row.get("Labour force characteristics"))
            if (
                indicator_id is None
                or row.get("Gender") != "Total - Gender"
                or row.get("Age group") != "15 years and over"
                or row.get("Statistics") != "Estimate"
                or row.get("Data type") != "Seasonally adjusted"
                or location_id is None
                or not row.get("VALUE")
            ):
                continue
            period = month_date(row["REF_DATE"])
            if cutoff and period < cutoff:
                continue
            _obs, was_inserted = self.repo.upsert_observation(
                indicator_id=indicator_id,
                location_id=location_id,
                period=period,
                value=float(row["VALUE"]),
                unit="%",
                source_id="statcan",
                source_table_id="14-10-0287-01",
                source_series_id=row.get("VECTOR"),
            )
            fetched += 1
            inserted += 1 if was_inserted else 0
            updated += 0 if was_inserted else 1
        self.repo.upsert_freshness(source_id="statcan", dataset_id="labour_force", latest_period=latest, status="healthy")
        self.session.commit()
        return IngestResult("ingest_statcan_labour", "success", fetched, inserted, updated, latest)

    def _ingest_food_prices(self, recent_months: int) -> IngestResult:
        from app.models.economic import IndicatorModel

        for item_id, (product_name, _quantity) in self.basket_products.items():
            self.session.merge(
                IndicatorModel(
                    id=f"price_{item_id}",
                    name=product_name,
                    category="food_prices",
                    description=f"Monthly average retail price for {product_name}.",
                    unit="CAD",
                    frequency="monthly",
                    source_id="statcan",
                    external_table_id="18-10-0245-01",
                    calculation_type="source",
                    higher_is_good=False,
                    display_precision=2,
                )
            )
        self.session.commit()

        content = self.statcan.fetch_table_zip("food_prices")
        rows = list(self.statcan.iter_rows_from_zip_bytes(content, "food_prices"))
        latest = self._latest_period_in_rows(rows, "food_prices")
        self._store_raw_payload("statcan", "food_prices", content, latest, {"row_count": len(rows), "table_id": "18-10-0245-01"})
        cutoff = self._period_cutoff(latest, recent_months) if latest else None
        product_to_item = {product: item_id for item_id, (product, _quantity) in self.basket_products.items()}
        fetched = inserted = updated = 0

        for row in rows:
            product = row.get("Products")
            item_id = product_to_item.get(product or "")
            location_id = self.geo_to_location.get(row.get("GEO", ""))
            if item_id is None or location_id is None or not row.get("VALUE"):
                continue
            period = month_date(row["REF_DATE"])
            if cutoff and period < cutoff:
                continue
            _obs, was_inserted = self.repo.upsert_observation(
                indicator_id=f"price_{item_id}",
                location_id=location_id,
                period=period,
                value=float(row["VALUE"]),
                unit="CAD",
                source_id="statcan",
                source_table_id="18-10-0245-01",
                source_series_id=row.get("VECTOR"),
            )
            fetched += 1
            inserted += 1 if was_inserted else 0
            updated += 0 if was_inserted else 1
        self.repo.upsert_freshness(source_id="statcan", dataset_id="food_prices", latest_period=latest, status="healthy")
        self.session.commit()
        return IngestResult("ingest_statcan_food_prices", "success", fetched, inserted, updated, latest)

    def _ingest_bank_of_canada(self) -> IngestResult:
        fetched = inserted = updated = 0
        latest = None
        dataset_latest = {}
        for indicator_id, config in BANK_OF_CANADA_SERIES.items():
            series_id = config["series_id"]
            observations = self.bank_of_canada.recent_observations(series_id, recent=30)
            for observation in observations:
                _obs, was_inserted = self.repo.upsert_observation(
                    indicator_id=indicator_id,
                    location_id="CA",
                    period=observation.period,
                    value=observation.value,
                    unit=config["unit"],
                    source_id="bank_of_canada",
                    source_series_id=observation.series_id,
                )
                latest = observation.period if latest is None or observation.period > latest else latest
                dataset_latest[config["dataset_id"]] = observation.period if config["dataset_id"] not in dataset_latest or observation.period > dataset_latest[config["dataset_id"]] else dataset_latest[config["dataset_id"]]
                fetched += 1
                inserted += 1 if was_inserted else 0
                updated += 0 if was_inserted else 1
        for dataset_id, period in dataset_latest.items():
            self.repo.upsert_freshness(source_id="bank_of_canada", dataset_id=dataset_id, latest_period=period, status="healthy")
        self.session.commit()
        return IngestResult("ingest_bank_of_canada", "success", fetched, inserted, updated, latest)

    def calculate_affordability_scores(self) -> int:
        metric_ids = [
            "cpi_all_items_yoy",
            "cpi_food_yoy",
            "cpi_shelter_yoy",
            "gas_regular_cents_litre",
            "unemployment_rate",
            "basic_basket_monthly_cost",
        ]
        latest_periods = [self.repo.latest_period(metric_id) for metric_id in metric_ids]
        periods = [period for period in latest_periods if period is not None]
        if not periods:
            return 0
        period = max(periods)
        locations = [loc for loc in self.repo.locations("province") if loc.id != "CA"]
        values_by_location = {}
        peer_values = {metric_id: [] for metric_id in metric_ids}
        for loc in locations:
            values_by_location[loc.id] = {}
            for metric_id in metric_ids:
                metric_period = self.repo.latest_period(metric_id)
                if metric_period is None:
                    continue
                obs = self.repo.observation(metric_id, loc.id, metric_period)
                if obs and obs.value is not None:
                    value = float(obs.value)
                    values_by_location[loc.id][metric_id] = value
                    peer_values[metric_id].append(value)
        count = 0
        for location_id, region_values in values_by_location.items():
            if len(region_values) < 3:
                continue
            score = calculate_affordability_score_v1(region_values, peer_values)
            self.repo.upsert_observation(
                indicator_id="affordability_score",
                location_id=location_id,
                period=period,
                value=score,
                unit="score",
                source_id="internal",
                is_estimated=True,
            )
            count += 1
        self.session.commit()
        return count

    def _seed_fallback_baskets(self) -> int:
        latest = date.fromisoformat("2026-04-01")
        count = 0
        for location_id, metrics in METRICS.items():
            self.repo.upsert_observation(
                indicator_id="basic_basket_monthly_cost",
                location_id=location_id,
                period=latest,
                value=metrics["basic_basket_monthly_cost"],
                unit="CAD/month",
                source_id="internal",
                is_estimated=True,
            )
            count += 1
        self.session.commit()
        self._calculate_indicator_changes("basic_basket_monthly_cost")
        self.repo.upsert_freshness(source_id="internal", dataset_id="basic_basket", latest_period=latest, status="partial", notes="Seeded fallback basket used where StatCan retail product coverage is unavailable.")
        self.session.commit()
        return count

    def _store_raw_payload(self, source_id: str, dataset_id: str, content: bytes, period: date | None, metadata: dict) -> None:
        if not self.settings.store_raw_payloads:
            return
        try:
            request_hash = hashlib.sha256(content).hexdigest()
            payload = {"metadata": metadata, "content_sha256": request_hash}
            self.repo.store_raw_payload(
                source_id=source_id,
                dataset_id=dataset_id,
                request_hash=request_hash,
                period=period,
                payload=json.loads(json.dumps(payload)),
            )
        except Exception:
            logger.exception("Raw payload storage failed for %s/%s", source_id, dataset_id)

    def _calculate_indicator_changes(self, indicator_id: str) -> None:
        from app.models.economic import ObservationModel

        observations = (
            self.session.query(ObservationModel)
            .filter(ObservationModel.indicator_id == indicator_id)
            .order_by(ObservationModel.location_id, ObservationModel.period)
            .all()
        )
        by_key = {(obs.location_id, obs.period): obs for obs in observations}
        for obs in observations:
            prior_year = by_key.get((obs.location_id, add_months(obs.period, -12)))
            prior_month = by_key.get((obs.location_id, add_months(obs.period, -1)))
            national = by_key.get(("CA", obs.period))
            yoy_change = calculate_yoy(float(obs.value), float(prior_year.value)) if prior_year and prior_year.value is not None else None
            mom_change = calculate_mom(float(obs.value), float(prior_month.value)) if prior_month and prior_month.value is not None else None
            if (yoy_change is not None and abs(yoy_change) > 50) or (mom_change is not None and abs(mom_change) > 25):
                self.repo.add_quality_flag(
                    flag_type="outlier_change",
                    severity="warning",
                    message=f"Large change for {indicator_id}/{obs.location_id}/{obs.period}: yoy={yoy_change}, mom={mom_change}",
                    observation_id=obs.id,
                )
            self.repo.upsert_calculation(
                obs,
                yoy_change=yoy_change,
                mom_change=mom_change,
                national_difference=(float(obs.value) - float(national.value)) if national and national.value is not None and obs.location_id != "CA" else None,
            )

    def _derive_yoy_indicator(self, source_indicator: str, derived_indicator: str) -> None:
        from app.models.economic import ObservationModel

        observations = (
            self.session.query(ObservationModel)
            .filter(ObservationModel.indicator_id == source_indicator)
            .order_by(ObservationModel.location_id, ObservationModel.period)
            .all()
        )
        by_key = {(obs.location_id, obs.period): obs for obs in observations}
        for obs in observations:
            prior = by_key.get((obs.location_id, add_months(obs.period, -12)))
            if not prior or prior.value in (None, 0) or obs.value is None:
                continue
            value = calculate_yoy(float(obs.value), float(prior.value))
            if value is None:
                continue
            self.repo.upsert_observation(
                indicator_id=derived_indicator,
                location_id=obs.location_id,
                period=obs.period,
                value=round(value, 3),
                unit="%",
                source_id="internal",
                source_table_id=obs.source_table_id,
                source_series_id=obs.source_series_id,
            )
