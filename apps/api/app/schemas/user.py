from pydantic import BaseModel

from app.schemas.freshness import MetricTrustMetadata


class UserProfile(BaseModel):
    id: str
    email: str
    display_name: str | None = None
    avatar_url: str | None = None
    role: str = "user"
    created_at: str | None = None


class UpdateUserProfileRequest(BaseModel):
    display_name: str | None = None
    avatar_url: str | None = None


class UserPreferences(BaseModel):
    default_location_id: str | None = None
    default_metric: str | None = None
    default_period: str | None = None
    default_basket_id: str | None = None
    household_size: int = 1
    theme: str = "system"
    data_density: str = "simple"


class UpdateUserPreferencesRequest(BaseModel):
    default_location_id: str | None = None
    default_metric: str | None = None
    default_period: str | None = None
    default_basket_id: str | None = None
    household_size: int | None = None
    theme: str | None = None
    data_density: str | None = None


class SavedRegionRequest(BaseModel):
    location_id: str
    label: str | None = None


class SavedRegion(BaseModel):
    location_id: str
    name: str
    label: str | None = None
    saved_at: str


class WatchlistRegion(BaseModel):
    location_id: str
    name: str
    label: str | None = None
    saved_at: str
    summary: dict[str, float]
    freshness: MetricTrustMetadata
