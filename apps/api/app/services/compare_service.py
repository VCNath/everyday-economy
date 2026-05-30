from app.schemas.compare import CompareIndicator, CompareLocation, CompareMetricRow, CompareResponse
from app.schemas.freshness import MetricTrustMetadata
from app.schemas.freshness import DataWarning
from app.services.region_series_service import RegionSeriesService


class CompareService:
    def __init__(self, session):
        self.session = session
        self.region_series_service = RegionSeriesService(session)

    def get_compare(
        self,
        *,
        location_ids: list[str],
        indicators: list[str],
        start_period: str | None = None,
        end_period: str | None = None,
        window: str | None = None,
        include_series: bool = True,
        include_freshness: bool = True,
    ) -> CompareResponse:
        rows: list[CompareMetricRow] = []
        warnings: list[DataWarning] = []
        locations: list[CompareLocation] = []
        indicator_map: dict[str, CompareIndicator] = {}
        combined_series = []
        combined_freshness = []
        resolved_window = window or "12m"
        latest_period = "latest"

        for location_id in location_ids:
            series_response = self.region_series_service.get_series(
                location_id=location_id,
                indicators=indicators,
                start_period=start_period,
                end_period=end_period,
                window=window,
                include_freshness=include_freshness,
            )
            locations.append(CompareLocation(location_id=location_id, location_name=series_response.location_name))
            combined_freshness.extend(series_response.freshness)
            warnings.extend(series_response.warnings)
            resolved_window = series_response.window
            latest_period = series_response.end_period or latest_period

            for indicator_series in series_response.series:
                indicator_map[indicator_series.indicator_id] = CompareIndicator(
                    indicator_id=indicator_series.indicator_id,
                    indicator_name=indicator_series.indicator_name,
                    unit=indicator_series.unit,
                )
                latest_point = indicator_series.points[-1] if indicator_series.points else None
                trust = (
                    latest_point.trust
                    if latest_point
                    else MetricTrustMetadata(
                        source_id="unavailable",
                        source_name="Unavailable",
                        latest_period=series_response.end_period,
                        freshness_status="unavailable",
                        is_estimated=True,
                        notes=f"No value available for {indicator_series.indicator_id} in {location_id}.",
                    )
                )
                rows.append(
                    CompareMetricRow(
                        location_id=location_id,
                        location_name=series_response.location_name,
                        indicator_id=indicator_series.indicator_id,
                        indicator_name=indicator_series.indicator_name,
                        value=latest_point.value if latest_point else None,
                        unit=indicator_series.unit,
                        period=latest_point.period if latest_point else None,
                        yoy_change=latest_point.yoy_change if latest_point else None,
                        mom_change=latest_point.mom_change if latest_point else None,
                        trust=trust,
                    )
                )
                if include_series:
                    combined_series.append(indicator_series.model_copy(update={"indicator_id": f"{location_id}:{indicator_series.indicator_id}"}))

        return CompareResponse(
            locations=locations,
            indicators=list(indicator_map.values()),
            period=latest_period,
            window=resolved_window,
            rows=rows,
            series=combined_series if include_series else [],
            freshness=combined_freshness if include_freshness else [],
            warnings=warnings,
        )
