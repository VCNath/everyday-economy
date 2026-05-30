from pydantic import BaseModel

from app.schemas.freshness import DataWarning, MetricTrustMetadata
from app.schemas.series import IndicatorSeries


class CompareLocation(BaseModel):
    location_id: str
    location_name: str


class CompareIndicator(BaseModel):
    indicator_id: str
    indicator_name: str
    unit: str


class CompareMetricRow(BaseModel):
    location_id: str
    location_name: str
    indicator_id: str
    indicator_name: str
    value: float | None = None
    unit: str
    period: str | None = None
    yoy_change: float | None = None
    mom_change: float | None = None
    trust: MetricTrustMetadata


class CompareResponse(BaseModel):
    locations: list[CompareLocation]
    indicators: list[CompareIndicator]
    period: str
    window: str
    rows: list[CompareMetricRow]
    series: list[IndicatorSeries]
    freshness: list[MetricTrustMetadata]
    warnings: list[DataWarning]
