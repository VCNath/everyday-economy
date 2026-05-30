from app.schemas.common import MetricValue, SourceNote
from app.schemas.dashboard import (
    BasketCalculationRequest,
    BasketCalculationResponse,
    BasketLineItem,
    CompareMetricRow,
    CompareMetricValue,
    CompareResponse,
    LeaderboardResponse,
    LeaderboardRow,
    MapFeature,
    MapResponse,
    RegionSeriesPoint,
    RegionSeriesResponse,
    RegionSummary,
    SourceStatusResponse,
)
from app.services.seed_data import BASKET_ITEMS, INDICATORS, LAST_CHECKED, LOCATIONS, METRICS, PERIOD
from app.services.repository import EconomicRepository


def period_label(period) -> str:
    return period.strftime("%Y-%m") if hasattr(period, "strftime") else str(period)


class DashboardService:
    def __init__(self, session=None):
        self.session = session
        self.repo = EconomicRepository(session) if session is not None else None

    def list_locations(self, geography_level: str | None = None):
        if self.repo:
            locations = self.repo.locations(geography_level)
            if locations:
                return [
                    {
                        "id": loc.id,
                        "name": loc.name,
                        "country_code": loc.country_code,
                        "region_code": loc.region_code,
                        "geography_level": loc.geography_level,
                        "parent_location_id": loc.parent_location_id,
                        "latitude": float(loc.latitude or 0),
                        "longitude": float(loc.longitude or 0),
                    }
                    for loc in locations
                ]
        if geography_level:
            return [loc for loc in LOCATIONS if loc.geography_level == geography_level]
        return LOCATIONS

    def get_location(self, location_id: str):
        if self.repo:
            from app.models.economic import LocationModel

            loc = self.session.get(LocationModel, location_id)
            if loc:
                return {
                    "id": loc.id,
                    "name": loc.name,
                    "country_code": loc.country_code,
                    "region_code": loc.region_code,
                    "geography_level": loc.geography_level,
                    "parent_location_id": loc.parent_location_id,
                    "latitude": float(loc.latitude or 0),
                    "longitude": float(loc.longitude or 0),
                }
        return next((loc for loc in LOCATIONS if loc.id == location_id), None)

    def search_locations(self, query: str):
        q = query.lower()
        if self.repo:
            locations = self.repo.search_locations(q)
            if locations:
                return [
                    {
                        "id": loc.id,
                        "name": loc.name,
                        "country_code": loc.country_code,
                        "region_code": loc.region_code,
                        "geography_level": loc.geography_level,
                        "parent_location_id": loc.parent_location_id,
                        "latitude": float(loc.latitude or 0),
                        "longitude": float(loc.longitude or 0),
                    }
                    for loc in locations
                ]
        return [loc for loc in LOCATIONS if q in loc.name.lower() or q in loc.id.lower()]

    def list_indicators(self):
        if self.repo:
            indicators = self.repo.indicators()
            if indicators:
                return [
                    {
                        "id": indicator.id,
                        "name": indicator.name,
                        "category": indicator.category,
                        "description": indicator.description or "",
                        "unit": indicator.unit,
                        "frequency": indicator.frequency,
                        "source_id": indicator.source_id or "internal",
                        "higher_is_good": bool(indicator.higher_is_good),
                        "display_precision": indicator.display_precision,
                        "human_translation": indicator.description or indicator.name,
                    }
                    for indicator in indicators
                ]
        return INDICATORS

    def get_indicator(self, indicator_id: str):
        if self.repo:
            from app.models.economic import IndicatorModel

            indicator = self.session.get(IndicatorModel, indicator_id)
            if indicator:
                return {
                    "id": indicator.id,
                    "name": indicator.name,
                    "category": indicator.category,
                    "description": indicator.description or "",
                    "unit": indicator.unit,
                    "frequency": indicator.frequency,
                    "source_id": indicator.source_id or "internal",
                    "higher_is_good": bool(indicator.higher_is_good),
                    "display_precision": indicator.display_precision,
                    "human_translation": indicator.description or indicator.name,
                }
        return next((indicator for indicator in INDICATORS if indicator.id == indicator_id), None)

    def get_map(self, indicator: str, geography_level: str, calculation: str = "value"):
        if self.repo:
            observations = self.repo.latest_observations(indicator, geography_level)
            if observations:
                locations_by_id = {loc.id: loc for loc in self.repo.locations()}
                indicator_meta = self.get_indicator(indicator)
                higher_is_good = bool(indicator_meta.get("higher_is_good")) if isinstance(indicator_meta, dict) else False
                reverse = higher_is_good
                ranked = sorted(observations, key=lambda obs: float(obs.value or 0), reverse=reverse)
                features = [
                    MapFeature(
                        location_id=obs.location_id,
                        name=locations_by_id[obs.location_id].name,
                        value=float(obs.value or 0),
                        rank=index + 1,
                        geometry_ref=obs.location_id,
                        yoy_change=float(obs.calculations[0].yoy_change) if obs.calculations and obs.calculations[0].yoy_change is not None else None,
                        updated=period_label(obs.period),
                    )
                    for index, obs in enumerate(ranked)
                    if obs.location_id in locations_by_id
                ]
                return MapResponse(
                    indicator=indicator,
                    period=period_label(observations[0].period),
                    geography_level=geography_level,
                    source="Statistics Canada",
                    features=features,
                )
        locations = [loc for loc in LOCATIONS if loc.geography_level in {geography_level, "territory"} and loc.id != "CA"]
        ranked = self._rank_locations(locations, indicator)
        features = [
            MapFeature(
                location_id=loc.id,
                name=loc.name,
                value=METRICS[loc.id][indicator],
                rank=rank,
                geometry_ref=loc.id,
                yoy_change=METRICS[loc.id].get("cpi_food_yoy"),
                updated=PERIOD,
            )
            for rank, loc in ranked
        ]
        return MapResponse(
            indicator=indicator,
            period=PERIOD,
            geography_level=geography_level,
            source="Statistics Canada",
            features=features,
        )

    def get_region_summary(self, location_id: str):
        if self.repo:
            summary = self._get_database_region_summary(location_id)
            if summary:
                return summary
        loc = self.get_location(location_id)
        if loc is None or location_id not in METRICS:
            return None
        metrics = METRICS[location_id]
        national = METRICS["CA"]
        if metrics["cpi_all_items_yoy"] < national["cpi_all_items_yoy"]:
            pace = "slower than"
        else:
            pace = "faster than"
        insight = (
            f"Prices are rising {pace} the national average. Food, shelter, and fuel are "
            "the main household pressure points this month."
        )
        cards = {
            "cpi_yoy": MetricValue(value=metrics["cpi_all_items_yoy"], unit="%", label="Overall consumer prices", yoy_change=metrics["cpi_all_items_yoy"], latest_period=PERIOD),
            "food_cpi_yoy": MetricValue(value=metrics["cpi_food_yoy"], unit="%", label="Grocery and restaurant pressure", yoy_change=metrics["cpi_food_yoy"], latest_period=PERIOD),
            "gas_price_cents_litre": MetricValue(value=metrics["gas_regular_cents_litre"], unit="c/L", label="Cost to commute or drive", latest_period=PERIOD),
            "unemployment_rate": MetricValue(value=metrics["unemployment_rate"], unit="%", label="Job market softness", latest_period=PERIOD),
            "basic_basket_monthly_cost": MetricValue(value=metrics["basic_basket_monthly_cost"], unit="CAD/month", label="Estimated monthly essentials", yoy_change=metrics["cpi_food_yoy"], latest_period=PERIOD),
            "affordability_score": MetricValue(value=metrics["affordability_score"], unit="/100", label="Household pressure score", latest_period=PERIOD),
        }
        return RegionSummary(
            location_id=loc.id,
            name=loc.name,
            period=PERIOD,
            metrics=metrics,
            insight=insight,
            sources=["Statistics Canada", "Internal composite"],
            cards=cards,
        )

    def get_leaderboard(self, leaderboard_type: str, geography_level: str = "province", limit: int = 10):
        if self.repo:
            rows = self.repo.leaderboard_rows(leaderboard_type, limit)
            definition = self.repo.leaderboard_definition(leaderboard_type)
            if rows and definition:
                locations_by_id = {loc.id: loc for loc in self.repo.locations()}
                return LeaderboardResponse(
                    leaderboard_type=leaderboard_type,
                    period=period_label(rows[0].period),
                    geography_level=definition.geography_level,
                    rows=[
                        LeaderboardRow(
                            rank=row.rank,
                            location_id=row.location_id,
                            name=locations_by_id[row.location_id].name if row.location_id in locations_by_id else row.location_id,
                            value=float(row.value or 0),
                            unit=row.unit or definition.unit or "",
                            yoy_change=float(row.yoy_change) if row.yoy_change is not None else None,
                            mom_change=float(row.mom_change) if row.mom_change is not None else None,
                            previous_rank=row.previous_rank,
                            rank_change=row.rank_change,
                            updated=period_label(row.period),
                        )
                        for row in rows
                    ],
                )
        indicator, sort_reverse, unit = self._leaderboard_config(leaderboard_type)
        locations = [loc for loc in LOCATIONS if loc.id != "CA" and loc.id in METRICS]
        ranked_locations = sorted(
            locations,
            key=lambda loc: METRICS[loc.id][indicator],
            reverse=sort_reverse,
        )[:limit]
        rows = [
            LeaderboardRow(
                rank=index + 1,
                location_id=loc.id,
                name=loc.name,
                value=METRICS[loc.id][indicator],
                unit=unit,
                yoy_change=METRICS[loc.id].get("cpi_food_yoy"),
                mom_change=round(((index % 4) - 1.5) * 0.2, 1),
                previous_rank=max(1, index + (2 if index % 3 == 0 else 1)),
                rank_change=(1 if index % 3 == 0 else 0),
                updated=PERIOD,
            )
            for index, loc in enumerate(ranked_locations)
        ]
        return LeaderboardResponse(
            leaderboard_type=leaderboard_type,
            period=PERIOD,
            geography_level=geography_level,
            rows=rows,
        )

    def calculate_basket(self, request: BasketCalculationRequest):
        if self.repo:
            latest = self.repo.latest_period("basic_basket_monthly_cost")
            stored = self.repo.observation("basic_basket_monthly_cost", request.location_id, latest) if latest else None
            if stored and stored.value is not None:
                fallback = self._fallback_basket_lines(request)
                calculation = stored.calculations[0] if stored.calculations else None
                return BasketCalculationResponse(
                    location_id=request.location_id,
                    basket_type=request.basket_type,
                    period=period_label(stored.period),
                    total_cost=float(stored.value),
                    yoy_change=float(calculation.yoy_change) if calculation and calculation.yoy_change is not None else METRICS.get(request.location_id, METRICS["CA"])["cpi_food_yoy"],
                    coverage_score=0.65 if stored.is_estimated else 1.0,
                    items=fallback,
                )
        return self._seeded_basket_response(request)

    def _seeded_basket_response(self, request: BasketCalculationRequest):
        lines = self._fallback_basket_lines(request)
        return BasketCalculationResponse(
            location_id=request.location_id,
            basket_type=request.basket_type,
            period=PERIOD,
            total_cost=round(sum(line.monthly_cost for line in lines), 2),
            yoy_change=METRICS.get(request.location_id, METRICS["CA"])["cpi_food_yoy"],
            coverage_score=0.82,
            items=lines,
        )

    def _fallback_basket_lines(self, request: BasketCalculationRequest):
        location_factor = METRICS.get(request.location_id, METRICS["CA"])["basic_basket_monthly_cost"] / METRICS["CA"]["basic_basket_monthly_cost"]
        requested = {item.item_id: item.quantity for item in request.items}
        lines = []
        basket_type_factor = {"basic": 1.0, "student": 0.72, "family": 2.25, "commuter": 1.15}.get(request.basket_type, 1.0)
        household_factor = max(1, request.household_size) if request.basket_type == "family" else 1
        extended_items = [
            *BASKET_ITEMS,
            {"item_id": "ground_beef", "name": "Ground beef", "quantity": 3, "unit": "kg", "unit_price": 12.5},
            {"item_id": "rice", "name": "Rice", "quantity": 2, "unit": "bag", "unit_price": 7.5},
            {"item_id": "coffee", "name": "Coffee", "quantity": 2, "unit": "tin", "unit_price": 8.75},
            {"item_id": "gasoline", "name": "Gasoline", "quantity": 120, "unit": "L", "unit_price": METRICS.get(request.location_id, METRICS["CA"])["gas_regular_cents_litre"] / 100},
            {"item_id": "rent_placeholder", "name": "Rent placeholder", "quantity": 1, "unit": "month", "unit_price": 1200 * location_factor},
        ]
        for item in extended_items:
            quantity = requested.get(item["item_id"], item["quantity"])
            quantity = quantity * basket_type_factor * household_factor
            unit_price = round(item["unit_price"] * location_factor, 2)
            lines.append(
                BasketLineItem(
                    item_id=item["item_id"],
                    name=item["name"],
                    quantity=quantity,
                    unit=item["unit"],
                    unit_price=unit_price,
                    monthly_cost=round(unit_price * quantity, 2),
                )
            )
        return lines

    def default_basket(self):
        request = BasketCalculationRequest(location_id="CA-SK", items=[])
        return self.calculate_basket(request)

    def source_status(self):
        if self.repo:
            freshness = self.repo.freshness()
            sources = {source.id: source for source in self.repo.data_sources()}
            if freshness or sources:
                source_names = {
                    "statcan": "Statistics Canada",
                    "bank_of_canada": "Bank of Canada",
                    "internal": "Everyday Economy",
                    "world_bank": "World Bank",
                    "oecd": "OECD",
                    "cmhc": "CMHC",
                }
                freshness_keys = {(row.source_id, row.dataset_id) for row in freshness}
                notes = [
                    SourceNote(
                        source=source_names.get(row.source_id, row.source_id),
                        dataset=row.dataset_id,
                        latest_period=period_label(row.latest_period) if row.latest_period else "unknown",
                        last_checked=period_label(row.last_checked_at.date()) if row.last_checked_at else "unknown",
                        status=row.status or "unknown",
                        notes=row.notes,
                    )
                    for row in freshness
                ]
                for source_id, source in sources.items():
                    if source.enabled or any(key[0] == source_id for key in freshness_keys):
                        continue
                    notes.append(
                        SourceNote(
                            source=source_names.get(source_id, source.name),
                            dataset="stub",
                            latest_period="not enabled",
                            last_checked="not checked",
                            status="disabled",
                            notes=source.notes,
                        )
                    )
                return SourceStatusResponse(
                    sources=notes
                )
        return SourceStatusResponse(
            sources=[
                SourceNote(source="Statistics Canada", dataset="CPI", latest_period="2026-04", last_checked=LAST_CHECKED),
                SourceNote(source="Statistics Canada", dataset="Food Prices", latest_period="2026-03", last_checked=LAST_CHECKED),
                SourceNote(source="Statistics Canada", dataset="Gasoline", latest_period="2026-04", last_checked=LAST_CHECKED),
                SourceNote(source="Statistics Canada", dataset="Labour Force", latest_period="2026-04", last_checked=LAST_CHECKED),
                SourceNote(source="Bank of Canada", dataset="Rates and FX", latest_period="2026-05-27", last_checked=LAST_CHECKED),
            ]
        )

    def _rank_locations(self, locations, indicator: str):
        indicator_meta = self.get_indicator(indicator)
        if isinstance(indicator_meta, dict):
            reverse = bool(indicator_meta.get("higher_is_good"))
        else:
            reverse = bool(getattr(indicator_meta, "higher_is_good", False))
        ranked = sorted(locations, key=lambda loc: METRICS[loc.id][indicator], reverse=reverse)
        return [(index + 1, loc) for index, loc in enumerate(ranked)]

    def _leaderboard_config(self, leaderboard_type: str):
        config = {
            "grocery_basket": ("basic_basket_monthly_cost", True, "CAD/month"),
            "cheapest_groceries": ("basic_basket_monthly_cost", False, "CAD/month"),
            "highest_inflation": ("cpi_all_items_yoy", True, "%"),
            "lowest_inflation": ("cpi_all_items_yoy", False, "%"),
            "gas_prices": ("gas_regular_cents_litre", True, "cents/litre"),
            "best_affordability": ("affordability_score", True, "score"),
            "worst_affordability": ("affordability_score", False, "score"),
            "unemployment": ("unemployment_rate", True, "%"),
            "highest_unemployment": ("unemployment_rate", True, "%"),
            "highest_food_inflation": ("cpi_food_yoy", True, "%"),
            "most_expensive_groceries": ("basic_basket_monthly_cost", True, "CAD/month"),
            "highest_gas_prices": ("gas_regular_cents_litre", True, "cents/litre"),
            "lowest_gas_prices": ("gas_regular_cents_litre", False, "cents/litre"),
            "biggest_monthly_movers": ("cpi_all_items_yoy", True, "%"),
        }
        return config.get(leaderboard_type, config["grocery_basket"])

    def source_run_status(self):
        if not self.repo:
            return {"runs": []}
        return {
            "runs": [
                {
                    "source_id": run.source_id,
                    "job_name": run.job_name,
                    "status": run.status,
                    "started_at": period_label(run.started_at) if run.started_at else None,
                    "finished_at": period_label(run.finished_at) if run.finished_at else None,
                    "rows_fetched": run.rows_fetched,
                    "rows_inserted": run.rows_inserted,
                    "rows_updated": run.rows_updated,
                    "error_message": run.error_message,
                }
                for run in self.repo.latest_refresh_runs()
            ]
        }

    def data_quality_summary(self):
        return {"flags": self.repo.quality_summary() if self.repo else []}

    def get_region_series(self, location_id: str, indicator_id: str):
        if self.repo:
            from app.models.economic import ObservationModel

            observations = (
                self.session.query(ObservationModel)
                .filter(
                    ObservationModel.location_id == location_id,
                    ObservationModel.indicator_id == indicator_id,
                )
                .order_by(ObservationModel.period)
                .all()
            )
            if observations:
                points = [
                    RegionSeriesPoint(
                        period=period_label(obs.period),
                        value=float(obs.value or 0),
                        yoy_change=float(obs.calculations[0].yoy_change) if obs.calculations and obs.calculations[0].yoy_change is not None else None,
                        mom_change=float(obs.calculations[0].mom_change) if obs.calculations and obs.calculations[0].mom_change is not None else None,
                        source=obs.source_id or "internal",
                        is_estimated=bool(obs.is_estimated),
                    )
                    for obs in observations
                    if obs.value is not None
                ]
                return RegionSeriesResponse(
                    location_id=location_id,
                    indicator_id=indicator_id,
                    latest_period=period_label(observations[-1].period),
                    points=points,
                )
        fallback_value = METRICS.get(location_id, METRICS.get("CA", {})).get(indicator_id)
        if fallback_value is None:
            return None
        return RegionSeriesResponse(
            location_id=location_id,
            indicator_id=indicator_id,
            latest_period=PERIOD,
            points=[RegionSeriesPoint(period=PERIOD, value=float(fallback_value), source="seeded", is_estimated=True)],
            notes="Fallback seeded series data is being used.",
        )

    def compare_regions(self, location_ids: list[str], indicator_ids: list[str] | None = None):
        indicator_ids = indicator_ids or [
            "cpi_all_items_yoy",
            "cpi_food_yoy",
            "cpi_shelter_yoy",
            "gas_regular_cents_litre",
            "unemployment_rate",
            "basic_basket_monthly_cost",
            "affordability_score",
        ]
        metrics = []
        period = PERIOD
        for indicator_id in indicator_ids:
            indicator = self.get_indicator(indicator_id)
            if indicator is None:
                continue
            values = []
            for location_id in location_ids:
                location = self.get_location(location_id)
                name = location["name"] if isinstance(location, dict) else location.name if location else location_id
                value = None
                latest_period = period
                source = "Statistics Canada"
                is_estimated = False
                if self.repo:
                    latest = self.repo.latest_period(indicator_id)
                    if latest:
                        obs = self.repo.observation(indicator_id, location_id, latest)
                        if obs and obs.value is not None:
                            value = float(obs.value)
                            latest_period = period_label(latest)
                            source = obs.source_id or source
                            is_estimated = bool(obs.is_estimated)
                if value is None:
                    fallback = METRICS.get(location_id, {}).get(indicator_id)
                    if fallback is not None:
                        value = float(fallback)
                        source = "seeded"
                        is_estimated = True
                values.append(
                    CompareMetricValue(
                        location_id=location_id,
                        name=name,
                        value=value,
                        unit=indicator["unit"] if isinstance(indicator, dict) else indicator.unit,
                        latest_period=latest_period,
                        source=source,
                        is_estimated=is_estimated,
                    )
                )
            metrics.append(
                CompareMetricRow(
                    indicator_id=indicator_id,
                    label=indicator["name"] if isinstance(indicator, dict) else indicator.name,
                    unit=indicator["unit"] if isinstance(indicator, dict) else indicator.unit,
                    values=values,
                )
            )
        insight = "Comparison combines latest persisted source data where available and seeded fallback values where needed."
        if metrics:
            affordability = next((row for row in metrics if row.indicator_id == "affordability_score"), None)
            if affordability:
                sortable = [v for v in affordability.values if v.value is not None]
                if sortable:
                    best = max(sortable, key=lambda value: value.value or 0)
                    worst = min(sortable, key=lambda value: value.value or 0)
                    insight = f"{best.name} currently has the strongest affordability score among selected regions, while {worst.name} is under greater household pressure."
        return CompareResponse(
            location_ids=location_ids,
            period=period,
            metrics=metrics,
            insight=insight,
            source="mixed",
            is_cached=False,
        )

    def _get_database_region_summary(self, location_id: str):
        loc = self.get_location(location_id)
        if loc is None:
            return None
        metric_ids = [
            "cpi_all_items_yoy",
            "cpi_food_yoy",
            "cpi_shelter_yoy",
            "gas_regular_cents_litre",
            "unemployment_rate",
            "basic_basket_monthly_cost",
            "affordability_score",
        ]
        metrics = {}
        period = None
        for indicator_id in metric_ids:
            latest = self.repo.latest_period(indicator_id)
            if latest is None:
                if location_id in METRICS and indicator_id in METRICS[location_id]:
                    metrics[indicator_id] = METRICS[location_id][indicator_id]
                continue
            obs = self.repo.observation(indicator_id, location_id, latest)
            if obs is None and location_id != "CA":
                obs = self.repo.observation(indicator_id, "CA", latest)
            if obs and obs.value is not None:
                metrics[indicator_id] = float(obs.value)
                period = latest if period is None or latest > period else period
            elif location_id in METRICS and indicator_id in METRICS[location_id]:
                metrics[indicator_id] = METRICS[location_id][indicator_id]
        if len(metrics) < 3:
            return None
        period = period or PERIOD
        national_cpi = metrics.get("cpi_all_items_yoy", 0)
        insight = (
            "Prices are being estimated from stored source observations. Food, shelter, fuel, "
            "and labour indicators are combined when available."
        )
        cards = {
            key: MetricValue(
                value=value,
                unit="%" if key.endswith("_yoy") or key == "unemployment_rate" else "CAD/month" if key == "basic_basket_monthly_cost" else "c/L" if key == "gas_regular_cents_litre" else "/100",
                label=key.replace("_", " "),
                latest_period=period_label(period),
            )
            for key, value in metrics.items()
        }
        return RegionSummary(
            location_id=location_id,
            name=loc["name"] if isinstance(loc, dict) else loc.name,
            period=period_label(period),
            metrics=metrics,
            insight=insight,
            sources=["Statistics Canada", "Bank of Canada", "Internal composite"],
            cards=cards,
        )


dashboard_service = DashboardService()
