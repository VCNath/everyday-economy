from pydantic import BaseModel


class MetricTrustMetadata(BaseModel):
    source_id: str | None = None
    source_name: str | None = None
    source_table_id: str | None = None
    source_series_id: str | None = None
    latest_period: str | None = None
    last_checked: str | None = None
    freshness_status: str = "unavailable"
    is_estimated: bool = False
    is_cached: bool = False
    coverage_score: float | None = None
    notes: str | None = None


class DataWarning(BaseModel):
    code: str
    message: str
    severity: str = "warning"
