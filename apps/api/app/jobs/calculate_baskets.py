from app.database import SessionLocal, init_db
from app.services.ingestion import EconomicIngestionService


def run() -> None:
    init_db()
    with SessionLocal() as session:
        service = EconomicIngestionService(session)
        service.initialize_reference_data()
        count = service.build_baskets()
        print(f"Basket calculations refreshed for {count} locations.")


if __name__ == "__main__":
    run()
