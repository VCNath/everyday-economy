from app.database import SessionLocal, init_db
from app.services.ingestion import EconomicIngestionService
from app.services.leaderboards import LeaderboardBuilder


def run(include_large_tables: bool = True) -> None:
    init_db()
    with SessionLocal() as session:
        service = EconomicIngestionService(session)
        service.initialize_reference_data()
        results = [
            service.ingest_cpi(),
            service.ingest_gas(),
            service.ingest_bank_of_canada(),
        ]
        if include_large_tables:
            results.extend([service.ingest_labour(), service.ingest_food_prices()])
        basket_count = service.build_baskets()
        service.calculate_changes()
        leaderboard_count = LeaderboardBuilder(session).build_all()
        for result in results:
            print(
                f"{result.job_name}: {result.status} fetched={result.rows_fetched} "
                f"inserted={result.rows_inserted} updated={result.rows_updated}"
            )
        print(f"Basket rows refreshed: {basket_count}")
        print(f"Leaderboard rows refreshed: {leaderboard_count}")


if __name__ == "__main__":
    run()
