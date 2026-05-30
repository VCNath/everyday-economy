import csv
import io
import zipfile
from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.connectors.statcan import StatCanConnector
from app.database import Base
from app.models.economic import ObservationModel
from app.services.ingestion import EconomicIngestionService
from app.services.leaderboards import LeaderboardBuilder
from app.services.seed_registry import seed_reference_data
from app.transformations.normalize_observations import (
    map_cpi_product,
    map_labour_characteristic,
    map_statcan_location,
    normalize_statcan_unit,
)


def make_zip(filename: str, rows: list[dict[str, str]]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        csv_buffer = io.StringIO()
        writer = csv.DictWriter(csv_buffer, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
        archive.writestr(filename, csv_buffer.getvalue())
    return buffer.getvalue()


def make_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    return Session()


class FakeStatCanConnector(StatCanConnector):
    def __init__(self, zip_bytes: bytes):
        super().__init__()
        self.zip_bytes = zip_bytes

    def fetch_table_zip(self, table_key: str) -> bytes:
        return self.zip_bytes


def test_statcan_connector_reads_bulk_zip_rows():
    rows = [
        {
            "REF_DATE": "2026-04",
            "GEO": "Saskatchewan",
            "Products and product groups": "Food",
            "VALUE": "104.0",
        }
    ]
    connector = StatCanConnector()
    parsed = list(connector.iter_rows_from_zip_bytes(make_zip("18100004.csv", rows), "cpi"))
    assert parsed[0]["GEO"] == "Saskatchewan"
    assert parsed[0]["VALUE"] == "104.0"


def test_mapping_helpers():
    assert map_statcan_location("Saskatchewan", {"Saskatchewan": "CA-SK"}) == "CA-SK"
    assert map_statcan_location("Unknown", {"Saskatchewan": "CA-SK"}) is None
    assert map_cpi_product("Food") == ("cpi_food_index", "index")
    assert map_labour_characteristic("Employment rate") == "employment_rate"
    assert normalize_statcan_unit("2002=100", "raw") == "index"


def test_connector_failure_behavior_is_captured():
    class FailingStatCanConnector(StatCanConnector):
        def fetch_table_zip(self, table_key: str) -> bytes:
            raise RuntimeError("source unavailable")

    session = make_session()
    service = EconomicIngestionService(session, statcan=FailingStatCanConnector())
    service.initialize_reference_data()
    result = service.ingest_cpi()

    assert result.status == "error"
    assert "source unavailable" in result.error_message


def test_cpi_ingestion_persists_and_derives_yoy():
    rows = []
    for period, value in [("2025-04", "100.0"), ("2026-04", "104.0")]:
        rows.append(
            {
                "REF_DATE": period,
                "GEO": "Saskatchewan",
                "DGUID": "",
                "Products and product groups": "Food",
                "UOM": "2002=100",
                "UOM_ID": "17",
                "SCALAR_FACTOR": "units",
                "SCALAR_ID": "0",
                "VECTOR": "v-test",
                "COORDINATE": "1.1",
                "VALUE": value,
                "STATUS": "",
                "SYMBOL": "",
                "TERMINATED": "",
                "DECIMALS": "1",
            }
        )
    session = make_session()
    service = EconomicIngestionService(session, statcan=FakeStatCanConnector(make_zip("18100004.csv", rows)))
    service.initialize_reference_data()
    result = service.ingest_cpi(recent_months=18)
    service.calculate_changes()

    derived = (
        session.query(ObservationModel)
        .filter(
            ObservationModel.indicator_id == "cpi_food_yoy",
            ObservationModel.location_id == "CA-SK",
            ObservationModel.period == date(2026, 4, 1),
        )
        .one()
    )
    assert result.rows_fetched == 2
    assert round(float(derived.value), 1) == 4.0


def test_leaderboard_builder_uses_stored_observations():
    session = make_session()
    seed_reference_data(session)
    service = EconomicIngestionService(session)
    repo = service.repo
    repo.upsert_observation(indicator_id="basic_basket_monthly_cost", location_id="CA-SK", period=date(2026, 4, 1), value=420, unit="CAD/month", source_id="internal")
    repo.upsert_observation(indicator_id="basic_basket_monthly_cost", location_id="CA-BC", period=date(2026, 4, 1), value=480, unit="CAD/month", source_id="internal")
    session.commit()

    count = LeaderboardBuilder(session).build("grocery_basket")
    rows = repo.leaderboard_rows("grocery_basket", limit=2)

    assert count == 2
    assert rows[0].location_id == "CA-BC"
    assert rows[0].rank == 1
