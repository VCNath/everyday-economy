from app.models.economic import LeaderboardSnapshotModel, LocationModel, ObservationModel
from app.services.repository import EconomicRepository


class LeaderboardBuilder:
    def __init__(self, session):
        self.session = session
        self.repo = EconomicRepository(session)

    def build_all(self) -> int:
        count = 0
        for leaderboard_id in [
            "grocery_basket",
            "most_expensive_groceries",
            "cheapest_groceries",
            "highest_inflation",
            "lowest_inflation",
            "highest_food_inflation",
            "gas_prices",
            "highest_gas_prices",
            "lowest_gas_prices",
            "best_affordability",
            "worst_affordability",
            "unemployment",
            "highest_unemployment",
            "biggest_monthly_movers",
        ]:
            count += self.build(leaderboard_id)
        self.session.commit()
        return count

    def build(self, leaderboard_id: str) -> int:
        definition = self.repo.leaderboard_definition(leaderboard_id)
        if definition is None or not definition.indicator_id:
            return 0
        latest = self.repo.latest_period(definition.indicator_id)
        if latest is None:
            return 0

        rows = (
            self.session.query(ObservationModel)
            .join(LocationModel, LocationModel.id == ObservationModel.location_id)
            .filter(
                ObservationModel.indicator_id == definition.indicator_id,
                ObservationModel.period == latest,
                LocationModel.geography_level.in_(["province", "territory"]),
            )
            .all()
        )
        reverse = definition.sort_direction == "desc"
        if leaderboard_id == "biggest_monthly_movers":
            ranked = sorted(
                rows,
                key=lambda obs: abs(float(obs.calculations[0].mom_change or 0)) if obs.calculations else 0,
                reverse=True,
            )
        else:
            ranked = sorted(rows, key=lambda obs: float(obs.value or 0), reverse=reverse)
        for index, obs in enumerate(ranked):
            previous = (
                self.session.query(LeaderboardSnapshotModel)
                .filter(
                    LeaderboardSnapshotModel.leaderboard_id == leaderboard_id,
                    LeaderboardSnapshotModel.location_id == obs.location_id,
                    LeaderboardSnapshotModel.period < latest,
                )
                .order_by(LeaderboardSnapshotModel.period.desc())
                .first()
            )
            existing = (
                self.session.query(LeaderboardSnapshotModel)
                .filter(
                    LeaderboardSnapshotModel.leaderboard_id == leaderboard_id,
                    LeaderboardSnapshotModel.location_id == obs.location_id,
                    LeaderboardSnapshotModel.period == latest,
                )
                .first()
            )
            snapshot = existing or LeaderboardSnapshotModel(
                leaderboard_id=leaderboard_id,
                location_id=obs.location_id,
                period=latest,
            )
            snapshot.rank = index + 1
            snapshot.previous_rank = previous.rank if previous else None
            snapshot.rank_change = (previous.rank - snapshot.rank) if previous else None
            snapshot.value = float(obs.value or 0)
            snapshot.unit = definition.unit or obs.unit
            snapshot.yoy_change = (
                float(obs.calculations[0].yoy_change)
                if obs.calculations and obs.calculations[0].yoy_change is not None
                else None
            )
            snapshot.mom_change = (
                float(obs.calculations[0].mom_change)
                if obs.calculations and obs.calculations[0].mom_change is not None
                else None
            )
            self.session.add(snapshot)
        return len(ranked)
