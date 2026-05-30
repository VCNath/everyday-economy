from datetime import date

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError

from app.models.economic import (
    DataQualityFlagModel,
    DataSourceModel,
    IndicatorModel,
    LeaderboardDefinitionModel,
    LeaderboardSnapshotModel,
    LocationModel,
    ObservationCalculationModel,
    ObservationModel,
    RawSourcePayloadModel,
    SourceFreshnessModel,
    SourceRefreshRunModel,
    utc_now,
)


class EconomicRepository:
    def __init__(self, session):
        self.session = session

    def locations(self, geography_level: str | None = None) -> list[LocationModel]:
        stmt = select(LocationModel)
        if geography_level:
            if geography_level == "province":
                stmt = stmt.where(LocationModel.geography_level.in_(["province", "territory"]))
            else:
                stmt = stmt.where(LocationModel.geography_level == geography_level)
        return list(self.session.scalars(stmt.order_by(LocationModel.name)))

    def search_locations(self, query: str) -> list[LocationModel]:
        q = f"%{query.lower()}%"
        return list(
            self.session.scalars(
                select(LocationModel)
                .where(
                    func.lower(LocationModel.name).like(q)
                    | func.lower(LocationModel.id).like(q)
                    | func.lower(LocationModel.region_code).like(q)
                )
                .order_by(LocationModel.name)
            )
        )

    def indicators(self) -> list[IndicatorModel]:
        return list(self.session.scalars(select(IndicatorModel).order_by(IndicatorModel.name)))

    def indicator_by_id(self, indicator_id: str) -> IndicatorModel | None:
        return self.session.get(IndicatorModel, indicator_id)

    def location_by_id(self, location_id: str) -> LocationModel | None:
        return self.session.get(LocationModel, location_id)

    def data_sources(self) -> list[DataSourceModel]:
        return list(self.session.scalars(select(DataSourceModel).order_by(DataSourceModel.name)))

    def latest_period(self, indicator_id: str) -> date | None:
        return self.session.scalar(
            select(func.max(ObservationModel.period)).where(ObservationModel.indicator_id == indicator_id)
        )

    def latest_observations(self, indicator_id: str, geography_level: str | None = None) -> list[ObservationModel]:
        latest = self.latest_period(indicator_id)
        if latest is None:
            return []
        stmt = (
            select(ObservationModel)
            .join(LocationModel, LocationModel.id == ObservationModel.location_id)
            .where(ObservationModel.indicator_id == indicator_id, ObservationModel.period == latest)
        )
        if geography_level:
            if geography_level == "province":
                stmt = stmt.where(LocationModel.geography_level.in_(["province", "territory"]))
            else:
                stmt = stmt.where(LocationModel.geography_level == geography_level)
        return list(self.session.scalars(stmt))

    def observation(self, indicator_id: str, location_id: str, period: date) -> ObservationModel | None:
        return self.session.scalar(
            select(ObservationModel).where(
                ObservationModel.indicator_id == indicator_id,
                ObservationModel.location_id == location_id,
                ObservationModel.period == period,
            )
        )

    def upsert_observation(
        self,
        *,
        indicator_id: str,
        location_id: str,
        period: date,
        value: float,
        unit: str,
        source_id: str,
        source_table_id: str | None = None,
        source_series_id: str | None = None,
        is_estimated: bool = False,
        is_preliminary: bool = False,
    ) -> tuple[ObservationModel, bool]:
        existing = self.session.scalar(
            select(ObservationModel).where(
                ObservationModel.indicator_id == indicator_id,
                ObservationModel.location_id == location_id,
                ObservationModel.period == period,
                ObservationModel.source_id == source_id,
            )
        )
        if existing:
            if existing.unit and unit and existing.unit != unit:
                self.add_quality_flag(
                    flag_type="unit_mismatch",
                    severity="warning",
                    message=f"{indicator_id}/{location_id}/{period} changed unit from {existing.unit} to {unit}.",
                    observation_id=existing.id,
                )
            self.add_quality_flag(
                flag_type="duplicate_observation",
                severity="info",
                message=f"Upsert replaced existing {indicator_id}/{location_id}/{period}/{source_id}.",
                observation_id=existing.id,
            )
            existing.value = value
            existing.unit = unit
            existing.source_table_id = source_table_id
            existing.source_series_id = source_series_id
            existing.ingested_at = utc_now()
            existing.is_estimated = is_estimated
            existing.is_preliminary = is_preliminary
            return existing, False

        observation = ObservationModel(
            indicator_id=indicator_id,
            location_id=location_id,
            period=period,
            value=value,
            unit=unit,
            source_id=source_id,
            source_table_id=source_table_id,
            source_series_id=source_series_id,
            is_estimated=is_estimated,
            is_preliminary=is_preliminary,
        )
        self.session.add(observation)
        return observation, True

    def upsert_calculation(
        self,
        observation: ObservationModel,
        *,
        yoy_change: float | None,
        mom_change: float | None,
        national_difference: float | None = None,
    ) -> ObservationCalculationModel:
        self.session.flush()
        existing = self.session.scalar(
            select(ObservationCalculationModel).where(
                ObservationCalculationModel.observation_id == observation.id
            )
        )
        if existing:
            existing.yoy_change = yoy_change
            existing.mom_change = mom_change
            existing.national_difference = national_difference
            existing.calculated_at = utc_now()
            return existing

        calculation = ObservationCalculationModel(
            observation_id=observation.id,
            yoy_change=yoy_change,
            mom_change=mom_change,
            national_difference=national_difference,
        )
        self.session.add(calculation)
        return calculation

    def freshness(self) -> list[SourceFreshnessModel]:
        return list(self.session.scalars(select(SourceFreshnessModel).order_by(SourceFreshnessModel.source_id)))

    def latest_refresh_runs(self) -> list[SourceRefreshRunModel]:
        runs = list(
            self.session.scalars(
                select(SourceRefreshRunModel).order_by(SourceRefreshRunModel.id.desc())
            )
        )
        latest = {}
        for run in runs:
            latest.setdefault((run.source_id, run.job_name), run)
        return sorted(latest.values(), key=lambda run: (run.source_id or "", run.job_name))

    def upsert_freshness(
        self,
        *,
        source_id: str,
        dataset_id: str,
        latest_period: date | None,
        status: str,
        notes: str | None = None,
    ) -> None:
        freshness = self.session.get(SourceFreshnessModel, {"source_id": source_id, "dataset_id": dataset_id})
        if freshness is None:
            freshness = SourceFreshnessModel(source_id=source_id, dataset_id=dataset_id)
            self.session.add(freshness)
        freshness.latest_period = latest_period
        freshness.last_checked_at = utc_now()
        freshness.status = status
        freshness.notes = notes

    def store_raw_payload(
        self,
        *,
        source_id: str,
        dataset_id: str,
        request_hash: str,
        payload: dict,
        period: date | None = None,
    ) -> None:
        self.session.add(
            RawSourcePayloadModel(
                source_id=source_id,
                dataset_id=dataset_id,
                request_hash=request_hash,
                period=period,
                payload=payload,
            )
        )

    def add_quality_flag(
        self,
        *,
        flag_type: str,
        severity: str,
        message: str,
        observation_id: int | None = None,
    ) -> None:
        self.session.add(
            DataQualityFlagModel(
                observation_id=observation_id,
                flag_type=flag_type,
                severity=severity,
                message=message,
            )
        )

    def quality_summary(self) -> list[dict[str, int | str]]:
        rows = (
            self.session.query(
                DataQualityFlagModel.flag_type,
                DataQualityFlagModel.severity,
                func.count(DataQualityFlagModel.id),
            )
            .group_by(DataQualityFlagModel.flag_type, DataQualityFlagModel.severity)
            .all()
        )
        return [
            {"flag_type": flag_type, "severity": severity, "count": count}
            for flag_type, severity, count in rows
        ]

    def leaderboard_definition(self, leaderboard_id: str) -> LeaderboardDefinitionModel | None:
        return self.session.get(LeaderboardDefinitionModel, leaderboard_id)

    def leaderboard_rows(self, leaderboard_id: str, limit: int = 10) -> list[LeaderboardSnapshotModel]:
        latest = self.session.scalar(
            select(func.max(LeaderboardSnapshotModel.period)).where(
                LeaderboardSnapshotModel.leaderboard_id == leaderboard_id
            )
        )
        if latest is None:
            return []
        return list(
            self.session.scalars(
                select(LeaderboardSnapshotModel)
                .where(
                    LeaderboardSnapshotModel.leaderboard_id == leaderboard_id,
                    LeaderboardSnapshotModel.period == latest,
                )
                .order_by(LeaderboardSnapshotModel.rank)
                .limit(limit)
            )
        )

    def safe_commit(self) -> bool:
        try:
            self.session.commit()
            return True
        except SQLAlchemyError:
            self.session.rollback()
            return False
