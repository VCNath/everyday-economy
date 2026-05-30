from pydantic import BaseModel

from app.schemas.common import MetricValue, SourceNote


class MapFeature(BaseModel):
    location_id: str
    name: str
    value: float
    rank: int
    geometry_ref: str
    yoy_change: float | None = None
    updated: str


class MapResponse(BaseModel):
    indicator: str
    period: str
    geography_level: str
    source: str
    features: list[MapFeature]


class RegionSummary(BaseModel):
    location_id: str
    name: str
    period: str
    metrics: dict[str, float]
    insight: str
    sources: list[str]
    cards: dict[str, MetricValue]


class LeaderboardRow(BaseModel):
    rank: int
    location_id: str
    name: str
    value: float
    unit: str
    yoy_change: float | None = None
    mom_change: float | None = None
    previous_rank: int | None = None
    rank_change: int | None = None
    source: str = "Statistics Canada"
    updated: str


class LeaderboardResponse(BaseModel):
    leaderboard_type: str
    period: str
    geography_level: str
    rows: list[LeaderboardRow]


class BasketItemRequest(BaseModel):
    item_id: str
    quantity: float


class BasketCalculationRequest(BaseModel):
    location_id: str
    basket_type: str = "basic"
    household_size: int = 1
    items: list[BasketItemRequest]


class BasketLineItem(BaseModel):
    item_id: str
    name: str
    quantity: float
    unit: str
    unit_price: float
    monthly_cost: float


class BasketCalculationResponse(BaseModel):
    location_id: str
    basket_type: str
    period: str
    total_cost: float
    yoy_change: float
    coverage_score: float
    items: list[BasketLineItem]


class SourceStatusResponse(BaseModel):
    sources: list[SourceNote]


class RegionSeriesPoint(BaseModel):
    period: str
    value: float
    yoy_change: float | None = None
    mom_change: float | None = None
    source: str | None = None
    is_estimated: bool = False


class RegionSeriesResponse(BaseModel):
    location_id: str
    indicator_id: str
    latest_period: str
    points: list[RegionSeriesPoint]
    notes: str | None = None


class CompareMetricValue(BaseModel):
    location_id: str
    name: str
    value: float | None = None
    unit: str
    latest_period: str
    source: str
    is_estimated: bool = False


class CompareMetricRow(BaseModel):
    indicator_id: str
    label: str
    unit: str
    values: list[CompareMetricValue]


class CompareResponse(BaseModel):
    location_ids: list[str]
    period: str
    metrics: list[CompareMetricRow]
    insight: str
    source: str
    is_cached: bool = False
