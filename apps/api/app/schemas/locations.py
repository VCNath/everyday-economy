from pydantic import BaseModel


class Location(BaseModel):
    id: str
    name: str
    country_code: str = "CA"
    region_code: str | None = None
    geography_level: str
    parent_location_id: str | None = None
    latitude: float
    longitude: float
