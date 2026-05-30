from app.models.economic import (
    DataSourceModel,
    IndicatorModel,
    LeaderboardDefinitionModel,
    LocationModel,
    ScoreWeightModel,
)
from app.services.seed_data import INDICATORS, LOCATIONS


STATCAN_GEO_NAMES = {
    "CA": "Canada",
    "CA-BC": "British Columbia",
    "CA-AB": "Alberta",
    "CA-SK": "Saskatchewan",
    "CA-MB": "Manitoba",
    "CA-ON": "Ontario",
    "CA-QC": "Quebec",
    "CA-NB": "New Brunswick",
    "CA-NS": "Nova Scotia",
    "CA-PE": "Prince Edward Island",
    "CA-NL": "Newfoundland and Labrador",
    "CA-YT": "Yukon",
    "CA-NT": "Northwest Territories",
    "CA-NU": "Nunavut",
}


DATA_SOURCES = [
    DataSourceModel(
        id="statcan",
        name="Statistics Canada",
        provider="Statistics Canada",
        base_url="https://www150.statcan.gc.ca",
        documentation_url="https://www.statcan.gc.ca/en/developers/wds",
        requires_api_key=False,
        refresh_frequency="monthly",
        enabled=True,
        notes="Bulk CSV tables are downloaded from /n1/tbl/csv.",
    ),
    DataSourceModel(
        id="bank_of_canada",
        name="Bank of Canada Valet API",
        provider="Bank of Canada",
        base_url="https://www.bankofcanada.ca/valet",
        documentation_url="https://www.bankofcanada.ca/valet/docs",
        requires_api_key=False,
        refresh_frequency="daily",
        enabled=True,
        notes="Rates and exchange-rate series are fetched from Valet JSON endpoints.",
    ),
    DataSourceModel(
        id="internal",
        name="Everyday Economy calculations",
        provider="Everyday Economy",
        requires_api_key=False,
        refresh_frequency="after ingestion",
        enabled=True,
        notes="Derived indicators, baskets, scores, and leaderboards.",
    ),
    DataSourceModel(
        id="world_bank",
        name="World Bank Indicators API",
        provider="World Bank",
        base_url="https://api.worldbank.org/v2",
        documentation_url="https://datahelpdesk.worldbank.org/knowledgebase/topics/125589",
        requires_api_key=False,
        refresh_frequency="monthly/annual",
        enabled=False,
        notes="Stubbed for a later global-comparison phase.",
    ),
    DataSourceModel(
        id="oecd",
        name="OECD Data Explorer API",
        provider="OECD",
        base_url="https://sdmx.oecd.org/public/rest",
        documentation_url="https://data-explorer.oecd.org/",
        requires_api_key=False,
        refresh_frequency="monthly/annual",
        enabled=False,
        notes="Stubbed for a later OECD comparison phase.",
    ),
    DataSourceModel(
        id="cmhc",
        name="Canada Mortgage and Housing Corporation",
        provider="CMHC",
        base_url="https://www.cmhc-schl.gc.ca",
        documentation_url="https://www.cmhc-schl.gc.ca/professionals/housing-markets-data-and-research",
        requires_api_key=False,
        refresh_frequency="monthly/annual",
        enabled=False,
        notes="Stubbed for future housing/rent data. Not ingested in Phase 2.",
    ),
    DataSourceModel(
        id="fred",
        name="Federal Reserve Economic Data",
        provider="Federal Reserve Bank of St. Louis",
        base_url="https://api.stlouisfed.org",
        documentation_url="https://fred.stlouisfed.org/docs/api/fred/",
        requires_api_key=True,
        refresh_frequency="daily/monthly",
        enabled=False,
        notes="Disabled stub for future U.S. expansion work.",
    ),
    DataSourceModel(
        id="bls",
        name="U.S. Bureau of Labor Statistics",
        provider="BLS",
        base_url="https://api.bls.gov/publicAPI/v2",
        documentation_url="https://www.bls.gov/developers/home.htm",
        requires_api_key=False,
        refresh_frequency="monthly",
        enabled=False,
        notes="Disabled stub for future U.S. labour/inflation integration.",
    ),
    DataSourceModel(
        id="bea",
        name="U.S. Bureau of Economic Analysis",
        provider="BEA",
        base_url="https://apps.bea.gov/api/data",
        documentation_url="https://apps.bea.gov/API/docs/index.htm",
        requires_api_key=True,
        refresh_frequency="monthly/quarterly",
        enabled=False,
        notes="Disabled stub for future U.S. GDP and macro integration.",
    ),
]


EXTRA_INDICATORS = [
    IndicatorModel(id="cpi_all_items_index", name="All-items CPI index", category="prices", description="Monthly CPI all-items index.", unit="index", frequency="monthly", source_id="statcan", external_table_id="18-10-0004-01", calculation_type="source", higher_is_good=False, display_precision=1),
    IndicatorModel(id="cpi_food_index", name="Food CPI index", category="prices", description="Monthly CPI food index.", unit="index", frequency="monthly", source_id="statcan", external_table_id="18-10-0004-01", calculation_type="source", higher_is_good=False, display_precision=1),
    IndicatorModel(id="cpi_shelter_index", name="Shelter CPI index", category="housing", description="Monthly CPI shelter index.", unit="index", frequency="monthly", source_id="statcan", external_table_id="18-10-0004-01", calculation_type="source", higher_is_good=False, display_precision=1),
    IndicatorModel(id="employment_rate", name="Employment rate", category="labour", description="Employment rate for population aged 15 years and over.", unit="percent", frequency="monthly", source_id="statcan", external_table_id="14-10-0287-01", calculation_type="source", higher_is_good=True, display_precision=1),
    IndicatorModel(id="participation_rate", name="Participation rate", category="labour", description="Labour force participation rate for population aged 15 years and over.", unit="percent", frequency="monthly", source_id="statcan", external_table_id="14-10-0287-01", calculation_type="source", higher_is_good=True, display_precision=1),
    IndicatorModel(id="basic_basket_yoy", name="Basic basket YoY", category="basket", description="Year-over-year change in the estimated monthly basic basket.", unit="percent", frequency="monthly", source_id="internal", calculation_type="calculated", higher_is_good=False, display_precision=1),
    IndicatorModel(id="boc_policy_rate", name="Bank of Canada policy rate", category="financial", description="Target for the overnight rate from the Bank of Canada Valet API.", unit="percent", frequency="daily", source_id="bank_of_canada", external_series_id="V39079", calculation_type="source", higher_is_good=False, display_precision=2),
    IndicatorModel(id="cad_usd_exchange_rate", name="CAD/USD exchange rate", category="financial", description="Canadian dollar to U.S. dollar exchange-rate context from the Bank of Canada Valet API.", unit="CAD per USD", frequency="daily", source_id="bank_of_canada", external_series_id="FXUSDCAD", calculation_type="source", higher_is_good=None, display_precision=4),
]


LEADERBOARD_DEFINITIONS = [
    LeaderboardDefinitionModel(id="grocery_basket", name="Most Expensive Grocery Basket", description="Estimated basic monthly basket, highest first.", indicator_id="basic_basket_monthly_cost", sort_direction="desc", geography_level="province", unit="CAD/month"),
    LeaderboardDefinitionModel(id="most_expensive_groceries", name="Most Expensive Groceries", description="Estimated basic monthly basket, highest first.", indicator_id="basic_basket_monthly_cost", sort_direction="desc", geography_level="province", unit="CAD/month"),
    LeaderboardDefinitionModel(id="cheapest_groceries", name="Cheapest Grocery Basket", description="Estimated basic monthly basket, lowest first.", indicator_id="basic_basket_monthly_cost", sort_direction="asc", geography_level="province", unit="CAD/month"),
    LeaderboardDefinitionModel(id="highest_inflation", name="Highest Inflation", description="All-items CPI YoY, highest first.", indicator_id="cpi_all_items_yoy", sort_direction="desc", geography_level="province", unit="%"),
    LeaderboardDefinitionModel(id="lowest_inflation", name="Lowest Inflation", description="All-items CPI YoY, lowest first.", indicator_id="cpi_all_items_yoy", sort_direction="asc", geography_level="province", unit="%"),
    LeaderboardDefinitionModel(id="highest_food_inflation", name="Highest Food Inflation", description="Food CPI YoY, highest first.", indicator_id="cpi_food_yoy", sort_direction="desc", geography_level="province", unit="%"),
    LeaderboardDefinitionModel(id="gas_prices", name="Highest Gas Prices", description="Regular gasoline price, highest first.", indicator_id="gas_regular_cents_litre", sort_direction="desc", geography_level="province", unit="cents/litre"),
    LeaderboardDefinitionModel(id="highest_gas_prices", name="Highest Gas Prices", description="Regular gasoline price, highest first.", indicator_id="gas_regular_cents_litre", sort_direction="desc", geography_level="province", unit="cents/litre"),
    LeaderboardDefinitionModel(id="lowest_gas_prices", name="Lowest Gas Prices", description="Regular gasoline price, lowest first.", indicator_id="gas_regular_cents_litre", sort_direction="asc", geography_level="province", unit="cents/litre"),
    LeaderboardDefinitionModel(id="best_affordability", name="Best Affordability", description="Composite affordability score, highest first.", indicator_id="affordability_score", sort_direction="desc", geography_level="province", unit="score"),
    LeaderboardDefinitionModel(id="worst_affordability", name="Worst Affordability", description="Composite affordability score, lowest first.", indicator_id="affordability_score", sort_direction="asc", geography_level="province", unit="score"),
    LeaderboardDefinitionModel(id="unemployment", name="Highest Unemployment", description="Unemployment rate, highest first.", indicator_id="unemployment_rate", sort_direction="desc", geography_level="province", unit="%"),
    LeaderboardDefinitionModel(id="highest_unemployment", name="Highest Unemployment", description="Unemployment rate, highest first.", indicator_id="unemployment_rate", sort_direction="desc", geography_level="province", unit="%"),
    LeaderboardDefinitionModel(id="biggest_monthly_movers", name="Biggest Monthly Movers", description="Largest month-over-month CPI moves.", indicator_id="cpi_all_items_yoy", sort_direction="desc", geography_level="province", unit="%"),
]


SCORE_WEIGHTS = [
    ScoreWeightModel(score_id="affordability_score_v1", component_indicator_id="cpi_all_items_yoy", weight=20, direction="lower_is_better"),
    ScoreWeightModel(score_id="affordability_score_v1", component_indicator_id="cpi_food_yoy", weight=20, direction="lower_is_better"),
    ScoreWeightModel(score_id="affordability_score_v1", component_indicator_id="cpi_shelter_yoy", weight=20, direction="lower_is_better"),
    ScoreWeightModel(score_id="affordability_score_v1", component_indicator_id="gas_regular_cents_litre", weight=15, direction="lower_is_better"),
    ScoreWeightModel(score_id="affordability_score_v1", component_indicator_id="unemployment_rate", weight=15, direction="lower_is_better"),
    ScoreWeightModel(score_id="affordability_score_v1", component_indicator_id="basic_basket_monthly_cost", weight=10, direction="lower_is_better"),
]


def seed_reference_data(session) -> None:
    for source in DATA_SOURCES:
        session.merge(source)

    for loc in LOCATIONS:
        session.merge(
            LocationModel(
                id=loc.id,
                name=loc.name,
                country_code=loc.country_code,
                region_code=loc.region_code,
                geography_level=loc.geography_level,
                parent_location_id=loc.parent_location_id,
                statcan_geo_name=STATCAN_GEO_NAMES.get(loc.id, loc.name),
                latitude=loc.latitude,
                longitude=loc.longitude,
            )
        )

    for indicator in INDICATORS:
        session.merge(
            IndicatorModel(
                id=indicator.id,
                name=indicator.name,
                category=indicator.category,
                description=indicator.description,
                unit=indicator.unit,
                frequency=indicator.frequency,
                source_id=indicator.source_id,
                calculation_type="calculated" if indicator.id.endswith("_yoy") else "source",
                higher_is_good=indicator.higher_is_good,
                display_precision=indicator.display_precision,
            )
        )

    for indicator in EXTRA_INDICATORS:
        session.merge(indicator)

    for definition in LEADERBOARD_DEFINITIONS:
        session.merge(definition)

    for weight in SCORE_WEIGHTS:
        session.merge(weight)

    session.commit()
