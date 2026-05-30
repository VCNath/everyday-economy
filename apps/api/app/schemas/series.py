from pydantic import BaseModel

from app.schemas.freshness import DataWarning, MetricTrustMetadata


class SeriesPoint(BaseModel):
    period: str
    value: float | None = None
    yoy_change: float | None = None
    mom_change: float | None = None
    trust: MetricTrustMetadata


class IndicatorSeries(BaseModel):
    indicator_id: str
    indicator_name: str
    unit: str
    points: list[SeriesPoint]


class RegionSeriesResponse(BaseModel):
    location_id: str
    location_name: str
    window: str
    start_period: str | None = None
    end_period: str | None = None
    series: list[IndicatorSeries]
    freshness: list[MetricTrustMetadata]
    warnings: list[DataWarning]
