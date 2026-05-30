from app.database import SessionLocal, init_db
from app.services.ingestion import EconomicIngestionService
from app.services.leaderboards import LeaderboardBuilder


def run() -> None:
    init_db()
    with SessionLocal() as session:
        service = EconomicIngestionService(session)
        service.initialize_reference_data()
        service.calculate_changes()
        service.build_baskets()
        rows = LeaderboardBuilder(session).build_all()
        print(f"Refreshed calculations and {rows} leaderboard rows.")


if __name__ == "__main__":
    run()
