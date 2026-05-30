from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_dashboard_service
from app.schemas.freshness import DataWarning, MetricTrustMetadata
from app.schemas.series import RegionSeriesResponse
from app.schemas.dashboard import RegionSeriesPoint as LegacyRegionSeriesPoint, RegionSummary
from app.schemas.series import IndicatorSeries, SeriesPoint
from app.services.dashboard_service import DashboardService
from app.services.region_series_service import RegionSeriesService
from app.services.time_window_service import WINDOW_MONTHS, parse_period

router = APIRouter(prefix="/regions", tags=["regions"])


@router.get("/{location_id}/summary", response_model=RegionSummary)
def get_region_summary(location_id: str, service: DashboardService = Depends(get_dashboard_service)):
    summary = service.get_region_summary(location_id)
    if summary is None:
        raise HTTPException(status_code=404, detail="Region summary not found")
    return summary


@router.get("/{location_id}/series", response_model=RegionSeriesResponse)
def get_region_series(
    location_id: str,
    indicators: str = "cpi_all_items_yoy",
    start_period: str | None = None,
    end_period: str | None = None,
    window: str | None = "12m",
    frequency: str | None = "monthly",
    include_freshness: bool = True,
    service: DashboardService = Depends(get_dashboard_service),
):
    _ = frequency
    if start_period and end_period:
        start = parse_period(start_period)
        end = parse_period(end_period)
        if start > end:
            raise HTTPException(status_code=400, detail="start_period must be less than or equal to end_period.")
    if window and window not in set(WINDOW_MONTHS) | {"all"}:
        raise HTTPException(status_code=400, detail=f"Invalid window '{window}'. Use 3m, 6m, 12m, 24m, 5y, or all.")
    parsed_indicators = [indicator.strip() for indicator in indicators.split(",") if indicator.strip()]
    region_series_service = RegionSeriesService(service.session) if service.session is not None else None
    series = (
        region_series_service.get_series(
            location_id=location_id,
            indicators=parsed_indicators,
            start_period=start_period,
            end_period=end_period,
            window=window,
            include_freshness=include_freshness,
        )
        if region_series_service is not None
        else None
    )
    if series is None:
        legacy = service.get_region_series(location_id, parsed_indicators[0])
        if legacy is not None:
            point = legacy.points[0] if legacy.points else LegacyRegionSeriesPoint(period=legacy.latest_period, value=0)  # type: ignore[arg-type]
            series = RegionSeriesResponse(
                location_id=legacy.location_id,
                location_name=legacy.location_id,
                window=window or "12m",
                start_period=None,
                end_period=legacy.latest_period,
                series=[
                    IndicatorSeries(
                        indicator_id=legacy.indicator_id,
                        indicator_name=legacy.indicator_id,
                        unit="",
                        points=[
                            SeriesPoint(
                                period=point.period,
                                value=point.value,
                                yoy_change=point.yoy_change,
                                mom_change=point.mom_change,
                                trust=MetricTrustMetadata(
                                    source_id=point.source,
                                    source_name=point.source,
                                    latest_period=legacy.latest_period,
                                    freshness_status="estimated" if point.is_estimated else "healthy",
                                    is_estimated=point.is_estimated,
                                    is_cached=False,
                                ),
                            )
                        ],
                    )
                ],
                freshness=[],
                warnings=[DataWarning(code="fallback", message=legacy.notes or "Fallback series response.", severity="warning")],
            )
    if series is None:
        raise HTTPException(status_code=404, detail="Region series not found")
    return series
