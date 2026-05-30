import argparse

from app.database import init_db, SessionLocal
from app.services.ingestion import EconomicIngestionService
from app.services.leaderboards import LeaderboardBuilder


def run(dataset: str = "all", include_large_tables: bool = False) -> None:
    init_db()
    with SessionLocal() as session:
        service = EconomicIngestionService(session)
        service.initialize_reference_data()
        runners = {
            "cpi": service.ingest_cpi,
            "gas": service.ingest_gas,
            "labour": service.ingest_labour,
            "food_prices": service.ingest_food_prices,
            "bank_of_canada": service.ingest_bank_of_canada,
        }
        if dataset == "all":
            selected = ["cpi", "gas", "bank_of_canada"]
            if include_large_tables:
                selected.extend(["labour", "food_prices"])
        else:
            selected = [dataset]
        results = [runners[name]() for name in selected]
        if include_large_tables or dataset == "food_prices":
            service.build_baskets()
        service.calculate_changes()
        LeaderboardBuilder(session).build_all()
        for result in results:
            print(
                f"{result.job_name}: {result.status} fetched={result.rows_fetched} "
                f"inserted={result.rows_inserted} updated={result.rows_updated}"
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset",
        choices=["all", "cpi", "gas", "labour", "food_prices", "bank_of_canada"],
        default="all",
    )
    parser.add_argument("--include-large-tables", action="store_true")
    args = parser.parse_args()
    run(dataset=args.dataset, include_large_tables=args.include_large_tables)
