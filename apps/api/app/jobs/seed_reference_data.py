from app.database import SessionLocal, init_db
from app.services.feature_flag_service import FeatureFlagService
from app.services.npem_scoring_service import NpemScoringService
from app.services.seed_registry import seed_reference_data


def run() -> None:
    init_db()
    with SessionLocal() as session:
        seed_reference_data(session)
        NpemScoringService(session).seed_methodology()
        flags = FeatureFlagService(session).list()
        print(f"Seeded reference data, N.P.E.M. methodology registries, and {len(flags)} feature flags.")


if __name__ == "__main__":
    run()
