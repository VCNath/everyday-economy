from app.database import SessionLocal, init_db
from app.services.npem_scoring_service import NpemScoringService


def run() -> None:
    init_db()
    with SessionLocal() as session:
        result = NpemScoringService(session).run_with_job()
        print(f"Calculated N.P.E.M. demo scores: {result['score_rows']} score rows, {result['normalized_rows']} normalized rows.")


if __name__ == "__main__":
    run()
