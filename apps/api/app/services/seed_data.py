from app.schemas.indicators import Indicator
from app.schemas.locations import Location

PERIOD = "2026-04"
LAST_CHECKED = "2026-05-27"

LOCATIONS = [
    Location(id="CA", name="Canada", geography_level="country", latitude=56.1304, longitude=-106.3468),
    Location(id="CA-BC", name="British Columbia", region_code="BC", geography_level="province", latitude=53.7267, longitude=-127.6476, parent_location_id="CA"),
    Location(id="CA-AB", name="Alberta", region_code="AB", geography_level="province", latitude=53.9333, longitude=-116.5765, parent_location_id="CA"),
    Location(id="CA-SK", name="Saskatchewan", region_code="SK", geography_level="province", latitude=52.9399, longitude=-106.4509, parent_location_id="CA"),
    Location(id="CA-MB", name="Manitoba", region_code="MB", geography_level="province", latitude=53.7609, longitude=-98.8139, parent_location_id="CA"),
    Location(id="CA-ON", name="Ontario", region_code="ON", geography_level="province", latitude=51.2538, longitude=-85.3232, parent_location_id="CA"),
    Location(id="CA-QC", name="Quebec", region_code="QC", geography_level="province", latitude=52.9399, longitude=-73.5491, parent_location_id="CA"),
    Location(id="CA-NB", name="New Brunswick", region_code="NB", geography_level="province", latitude=46.5653, longitude=-66.4619, parent_location_id="CA"),
    Location(id="CA-NS", name="Nova Scotia", region_code="NS", geography_level="province", latitude=44.682, longitude=-63.7443, parent_location_id="CA"),
    Location(id="CA-PE", name="Prince Edward Island", region_code="PE", geography_level="province", latitude=46.5107, longitude=-63.4168, parent_location_id="CA"),
    Location(id="CA-NL", name="Newfoundland and Labrador", region_code="NL", geography_level="province", latitude=53.1355, longitude=-57.6604, parent_location_id="CA"),
    Location(id="CA-YT", name="Yukon", region_code="YT", geography_level="territory", latitude=64.2823, longitude=-135.0, parent_location_id="CA"),
    Location(id="CA-NT", name="Northwest Territories", region_code="NT", geography_level="territory", latitude=64.8255, longitude=-124.8457, parent_location_id="CA"),
    Location(id="CA-NU", name="Nunavut", region_code="NU", geography_level="territory", latitude=70.2998, longitude=-83.1076, parent_location_id="CA"),
]

INDICATORS = [
    Indicator(id="cpi_all_items_yoy", name="Overall inflation", category="prices", description="Year-over-year change in all-items CPI.", unit="percent", frequency="monthly", source_id="statcan", higher_is_good=False, human_translation="Overall consumer prices"),
    Indicator(id="cpi_food_yoy", name="Food pressure", category="prices", description="Year-over-year change in food CPI.", unit="percent", frequency="monthly", source_id="statcan", higher_is_good=False, human_translation="Grocery and restaurant price pressure"),
    Indicator(id="cpi_shelter_yoy", name="Shelter pressure", category="housing", description="Year-over-year change in shelter CPI.", unit="percent", frequency="monthly", source_id="statcan", higher_is_good=False, human_translation="Rent, mortgage interest, utilities, and housing pressure"),
    Indicator(id="gas_regular_cents_litre", name="Gasoline", category="transportation", description="Average regular gasoline price.", unit="cents/litre", frequency="monthly", source_id="statcan", higher_is_good=False, human_translation="Cost to commute or drive"),
    Indicator(id="unemployment_rate", name="Unemployment", category="labour", description="Unemployment rate.", unit="percent", frequency="monthly", source_id="statcan", higher_is_good=False, human_translation="Job market softness"),
    Indicator(id="basic_basket_monthly_cost", name="Basic basket", category="basket", description="Estimated monthly essential basket cost.", unit="CAD/month", frequency="monthly", source_id="statcan", higher_is_good=False, human_translation="Estimated monthly cost of selected essentials"),
    Indicator(id="affordability_score", name="Affordability score", category="composite", description="Composite score from 0 to 100.", unit="score", frequency="monthly", source_id="internal", higher_is_good=True, human_translation="Household pressure score"),
]

METRICS = {
    "CA": {"cpi_all_items_yoy": 2.7, "cpi_food_yoy": 3.9, "cpi_shelter_yoy": 4.6, "gas_regular_cents_litre": 158.6, "unemployment_rate": 6.1, "basic_basket_monthly_cost": 446.25, "affordability_score": 64},
    "CA-BC": {"cpi_all_items_yoy": 3.1, "cpi_food_yoy": 5.8, "cpi_shelter_yoy": 5.7, "gas_regular_cents_litre": 178.4, "unemployment_rate": 5.9, "basic_basket_monthly_cost": 487.22, "affordability_score": 51},
    "CA-AB": {"cpi_all_items_yoy": 2.8, "cpi_food_yoy": 4.2, "cpi_shelter_yoy": 4.9, "gas_regular_cents_litre": 149.8, "unemployment_rate": 6.7, "basic_basket_monthly_cost": 451.08, "affordability_score": 65},
    "CA-SK": {"cpi_all_items_yoy": 2.4, "cpi_food_yoy": 3.7, "cpi_shelter_yoy": 3.8, "gas_regular_cents_litre": 154.2, "unemployment_rate": 5.6, "basic_basket_monthly_cost": 428.35, "affordability_score": 72},
    "CA-MB": {"cpi_all_items_yoy": 2.2, "cpi_food_yoy": 3.5, "cpi_shelter_yoy": 3.4, "gas_regular_cents_litre": 151.1, "unemployment_rate": 5.4, "basic_basket_monthly_cost": 419.48, "affordability_score": 76},
    "CA-ON": {"cpi_all_items_yoy": 2.9, "cpi_food_yoy": 4.9, "cpi_shelter_yoy": 5.2, "gas_regular_cents_litre": 161.6, "unemployment_rate": 6.8, "basic_basket_monthly_cost": 462.18, "affordability_score": 56},
    "CA-QC": {"cpi_all_items_yoy": 2.1, "cpi_food_yoy": 3.2, "cpi_shelter_yoy": 3.6, "gas_regular_cents_litre": 164.9, "unemployment_rate": 5.1, "basic_basket_monthly_cost": 433.6, "affordability_score": 74},
    "CA-NB": {"cpi_all_items_yoy": 2.5, "cpi_food_yoy": 3.6, "cpi_shelter_yoy": 4.0, "gas_regular_cents_litre": 159.7, "unemployment_rate": 7.0, "basic_basket_monthly_cost": 421.35, "affordability_score": 68},
    "CA-NS": {"cpi_all_items_yoy": 2.6, "cpi_food_yoy": 4.1, "cpi_shelter_yoy": 4.4, "gas_regular_cents_litre": 162.5, "unemployment_rate": 6.4, "basic_basket_monthly_cost": 438.84, "affordability_score": 63},
    "CA-PE": {"cpi_all_items_yoy": 2.3, "cpi_food_yoy": 3.8, "cpi_shelter_yoy": 3.9, "gas_regular_cents_litre": 160.2, "unemployment_rate": 7.4, "basic_basket_monthly_cost": 426.11, "affordability_score": 66},
    "CA-NL": {"cpi_all_items_yoy": 2.7, "cpi_food_yoy": 4.4, "cpi_shelter_yoy": 4.1, "gas_regular_cents_litre": 171.5, "unemployment_rate": 9.2, "basic_basket_monthly_cost": 444.03, "affordability_score": 55},
    "CA-YT": {"cpi_all_items_yoy": 3.0, "cpi_food_yoy": 5.1, "cpi_shelter_yoy": 4.8, "gas_regular_cents_litre": 181.0, "unemployment_rate": 4.5, "basic_basket_monthly_cost": 501.2, "affordability_score": 50},
    "CA-NT": {"cpi_all_items_yoy": 3.4, "cpi_food_yoy": 6.2, "cpi_shelter_yoy": 5.4, "gas_regular_cents_litre": 186.4, "unemployment_rate": 5.0, "basic_basket_monthly_cost": 528.9, "affordability_score": 44},
    "CA-NU": {"cpi_all_items_yoy": 3.8, "cpi_food_yoy": 7.4, "cpi_shelter_yoy": 5.9, "gas_regular_cents_litre": 190.3, "unemployment_rate": 12.6, "basic_basket_monthly_cost": 612.4, "affordability_score": 31},
}

BASKET_ITEMS = [
    {"item_id": "milk_2l", "name": "Milk, 2L", "quantity": 4, "unit": "each", "unit_price": 5.29},
    {"item_id": "eggs_dozen", "name": "Eggs, dozen", "quantity": 2, "unit": "dozen", "unit_price": 4.79},
    {"item_id": "bread_loaf", "name": "Bread", "quantity": 6, "unit": "loaf", "unit_price": 3.49},
    {"item_id": "chicken_kg", "name": "Chicken", "quantity": 4, "unit": "kg", "unit_price": 13.25},
    {"item_id": "apples_kg", "name": "Apples", "quantity": 5, "unit": "kg", "unit_price": 4.18},
]
