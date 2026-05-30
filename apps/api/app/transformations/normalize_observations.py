from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True)
class NormalizedObservation:
    indicator_id: str
    location_id: str
    period: date
    value: float
    unit: str
    source_id: str
    source_table_id: str | None = None
    source_series_id: str | None = None
    source_released_at: datetime | None = None
    is_preliminary: bool = False
    is_estimated: bool = False


def normalize_indicator_id(raw_name: str) -> str:
    return raw_name.strip().lower().replace(" ", "_").replace("-", "_")


def parse_month_period(value: str) -> date:
    if len(value) == 7:
        return date.fromisoformat(f"{value}-01")
    return date.fromisoformat(value)


def normalize_statcan_unit(value: str | None, fallback: str) -> str:
    if not value:
        return fallback
    cleaned = value.strip()
    if cleaned in {"2002=100", "2017=100"}:
        return "index"
    if cleaned in {"Percent", "%"}:
        return "%"
    if "cents per litre" in cleaned.lower():
        return "cents/litre"
    if cleaned in {"Dollars", "dollars"}:
        return "CAD"
    return fallback


def map_statcan_location(geo_name: str | None, geo_to_location: dict[str, str]) -> str | None:
    if not geo_name:
        return None
    return geo_to_location.get(geo_name.strip())


def map_cpi_product(product: str | None) -> tuple[str, str] | None:
    products = {
        "All-items": ("cpi_all_items_index", "index"),
        "Food": ("cpi_food_index", "index"),
        "Shelter": ("cpi_shelter_index", "index"),
    }
    return products.get(product or "")


def map_labour_characteristic(characteristic: str | None) -> str | None:
    characteristics = {
        "Unemployment rate": "unemployment_rate",
        "Employment rate": "employment_rate",
        "Participation rate": "participation_rate",
    }
    return characteristics.get(characteristic or "")
