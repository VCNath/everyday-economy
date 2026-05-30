from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.deps import get_dashboard_service
from app.schemas.compare import CompareIndicator, CompareLocation, CompareMetricRow, CompareResponse
from app.schemas.freshness import MetricTrustMetadata
from app.services.compare_service import CompareService
from app.services.dashboard_service import DashboardService
from app.services.time_window_service import WINDOW_MONTHS, parse_period

router = APIRouter(prefix="/compare", tags=["compare"])


@router.get("", response_model=CompareResponse)
def compare_regions(
    location_ids: str = Query(default="CA-SK,CA-AB,CA-MB"),
    indicators: str | None = Query(default=None),
    start_period: str | None = Query(default=None),
    end_period: str | None = Query(default=None),
    window: str | None = Query(default="12m"),
    frequency: str | None = Query(default="monthly"),
    include_series: bool = Query(default=True),
    include_freshness: bool = Query(default=True),
    service: DashboardService = Depends(get_dashboard_service),
):
    _ = frequency  # frequency aggregation is a future enhancement.
    if start_period and end_period:
        start = parse_period(start_period)
        end = parse_period(end_period)
        if start > end:
            raise HTTPException(status_code=400, detail="start_period must be less than or equal to end_period.")
    if window and window not in set(WINDOW_MONTHS) | {"all"}:
        raise HTTPException(status_code=400, detail=f"Invalid window '{window}'. Use 3m, 6m, 12m, 24m, 5y, or all.")

    parsed_locations = [location_id.strip() for location_id in location_ids.split(",") if location_id.strip()]
    parsed_indicators = [indicator_id.strip() for indicator_id in indicators.split(",") if indicator_id.strip()] if indicators else [
        "cpi_all_items_yoy",
        "cpi_food_yoy",
        "cpi_shelter_yoy",
        "gas_regular_cents_litre",
        "unemployment_rate",
        "basic_basket_monthly_cost",
        "affordability_score",
    ]
    compare_service = CompareService(service.session) if service.session is not None else None
    if compare_service is None:
        fallback = service.compare_regions(parsed_locations, parsed_indicators)
        locations = [CompareLocation(location_id=location_id, location_name=location_id) for location_id in fallback.location_ids]
        indicators_out: list[CompareIndicator] = []
        rows: list[CompareMetricRow] = []
        for metric in fallback.metrics:
            indicators_out.append(
                CompareIndicator(
                    indicator_id=metric.indicator_id,
                    indicator_name=metric.label,
                    unit=metric.unit,
                )
            )
            for value in metric.values:
                rows.append(
                    CompareMetricRow(
                        location_id=value.location_id,
                        location_name=value.name,
                        indicator_id=metric.indicator_id,
                        indicator_name=metric.label,
                        value=value.value,
                        unit=metric.unit,
                        period=value.latest_period,
                        trust=MetricTrustMetadata(
                            source_id=value.source,
                            source_name=value.source,
                            latest_period=value.latest_period,
                            freshness_status="estimated" if value.is_estimated else "healthy",
                            is_estimated=value.is_estimated,
                            is_cached=False,
                        ),
                    )
                )
        warnings = []
        for indicator_id in parsed_indicators:
            if service.get_indicator(indicator_id) is None:
                warnings.append({"code": "unknown_indicator", "message": f"Indicator {indicator_id} was not found.", "severity": "warning"})
        return CompareResponse(
            locations=locations,
            indicators=indicators_out,
            period=fallback.period,
            window=window or "12m",
            rows=rows,
            series=[],
            freshness=[],
            warnings=warnings,
        )
    return compare_service.get_compare(
        location_ids=parsed_locations,
        indicators=parsed_indicators,
        start_period=start_period,
        end_period=end_period,
        window=window,
        include_series=include_series,
        include_freshness=include_freshness,
    )
