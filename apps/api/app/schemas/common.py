from pydantic import BaseModel


class SourceNote(BaseModel):
    source: str
    dataset: str
    latest_period: str
    last_checked: str
    status: str = "healthy"
    notes: str | None = None


class MetricValue(BaseModel):
    value: float
    unit: str
    label: str
    yoy_change: float | None = None
    mom_change: float | None = None
    source: str = "Statistics Canada"
    latest_period: str
