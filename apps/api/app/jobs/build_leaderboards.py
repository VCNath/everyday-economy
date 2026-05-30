from app.database import SessionLocal, init_db
from app.services.leaderboards import LeaderboardBuilder
from app.services.seed_registry import seed_reference_data


def run() -> None:
    init_db()
    with SessionLocal() as session:
        seed_reference_data(session)
        rows = LeaderboardBuilder(session).build_all()
        print(f"Built {rows} leaderboard rows.")


if __name__ == "__main__":
    run()
