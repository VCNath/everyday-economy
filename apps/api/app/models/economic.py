from datetime import UTC, date, datetime
import uuid

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    JSON,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class LocationModel(Base):
    __tablename__ = "locations"

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    country_code: Mapped[str] = mapped_column(Text, nullable=False, default="CA")
    region_code: Mapped[str | None] = mapped_column(Text)
    geography_level: Mapped[str] = mapped_column(Text, nullable=False)
    parent_location_id: Mapped[str | None] = mapped_column(Text, ForeignKey("locations.id"))
    statcan_geo_name: Mapped[str | None] = mapped_column(Text)
    statcan_geo_code: Mapped[str | None] = mapped_column(Text)
    latitude: Mapped[float | None] = mapped_column(Numeric)
    longitude: Mapped[float | None] = mapped_column(Numeric)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class DataSourceModel(Base):
    __tablename__ = "data_sources"

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    provider: Mapped[str] = mapped_column(Text, nullable=False)
    base_url: Mapped[str | None] = mapped_column(Text)
    documentation_url: Mapped[str | None] = mapped_column(Text)
    requires_api_key: Mapped[bool] = mapped_column(Boolean, default=False)
    refresh_frequency: Mapped[str | None] = mapped_column(Text)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class IndicatorModel(Base):
    __tablename__ = "indicators"

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    unit: Mapped[str] = mapped_column(Text, nullable=False)
    frequency: Mapped[str] = mapped_column(Text, nullable=False)
    source_id: Mapped[str | None] = mapped_column(Text, ForeignKey("data_sources.id"))
    external_table_id: Mapped[str | None] = mapped_column(Text)
    external_series_id: Mapped[str | None] = mapped_column(Text)
    calculation_type: Mapped[str | None] = mapped_column(Text)
    higher_is_good: Mapped[bool | None] = mapped_column(Boolean)
    display_precision: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class ObservationModel(Base):
    __tablename__ = "observations"
    __table_args__ = (
        UniqueConstraint("indicator_id", "location_id", "period", "source_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    indicator_id: Mapped[str] = mapped_column(Text, ForeignKey("indicators.id"))
    location_id: Mapped[str] = mapped_column(Text, ForeignKey("locations.id"))
    period: Mapped[date] = mapped_column(Date, nullable=False)
    value: Mapped[float | None] = mapped_column(Numeric)
    unit: Mapped[str | None] = mapped_column(Text)
    source_id: Mapped[str | None] = mapped_column(Text, ForeignKey("data_sources.id"))
    source_table_id: Mapped[str | None] = mapped_column(Text)
    source_series_id: Mapped[str | None] = mapped_column(Text)
    source_released_at: Mapped[datetime | None] = mapped_column(DateTime)
    ingested_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    is_preliminary: Mapped[bool] = mapped_column(Boolean, default=False)
    is_estimated: Mapped[bool] = mapped_column(Boolean, default=False)

    calculations: Mapped[list["ObservationCalculationModel"]] = relationship(back_populates="observation")


class ObservationCalculationModel(Base):
    __tablename__ = "observation_calculations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    observation_id: Mapped[int] = mapped_column(ForeignKey("observations.id"), unique=True)
    yoy_change: Mapped[float | None] = mapped_column(Numeric)
    mom_change: Mapped[float | None] = mapped_column(Numeric)
    three_month_change: Mapped[float | None] = mapped_column(Numeric)
    twelve_month_change: Mapped[float | None] = mapped_column(Numeric)
    z_score: Mapped[float | None] = mapped_column(Numeric)
    national_difference: Mapped[float | None] = mapped_column(Numeric)
    calculated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    observation: Mapped[ObservationModel] = relationship(back_populates="calculations")


class RawSourcePayloadModel(Base):
    __tablename__ = "raw_source_payloads"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    source_id: Mapped[str] = mapped_column(Text, ForeignKey("data_sources.id"))
    dataset_id: Mapped[str] = mapped_column(Text, nullable=False)
    request_hash: Mapped[str] = mapped_column(Text, nullable=False)
    period: Mapped[date | None] = mapped_column(Date)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    fetched_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class LeaderboardDefinitionModel(Base):
    __tablename__ = "leaderboard_definitions"

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    indicator_id: Mapped[str | None] = mapped_column(Text, ForeignKey("indicators.id"))
    sort_direction: Mapped[str] = mapped_column(Text, nullable=False)
    geography_level: Mapped[str] = mapped_column(Text, nullable=False)
    unit: Mapped[str | None] = mapped_column(Text)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class LeaderboardSnapshotModel(Base):
    __tablename__ = "leaderboard_snapshots"
    __table_args__ = (
        UniqueConstraint("leaderboard_id", "location_id", "period"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    leaderboard_id: Mapped[str] = mapped_column(Text, ForeignKey("leaderboard_definitions.id"))
    location_id: Mapped[str] = mapped_column(Text, ForeignKey("locations.id"))
    period: Mapped[date] = mapped_column(Date, nullable=False)
    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    previous_rank: Mapped[int | None] = mapped_column(Integer)
    rank_change: Mapped[int | None] = mapped_column(Integer)
    value: Mapped[float | None] = mapped_column(Numeric)
    unit: Mapped[str | None] = mapped_column(Text)
    yoy_change: Mapped[float | None] = mapped_column(Numeric)
    mom_change: Mapped[float | None] = mapped_column(Numeric)
    national_average: Mapped[float | None] = mapped_column(Numeric)
    difference_from_average: Mapped[float | None] = mapped_column(Numeric)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class SourceRefreshRunModel(Base):
    __tablename__ = "source_refresh_runs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    source_id: Mapped[str | None] = mapped_column(Text, ForeignKey("data_sources.id"))
    job_name: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime)
    rows_fetched: Mapped[int] = mapped_column(Integer, default=0)
    rows_inserted: Mapped[int] = mapped_column(Integer, default=0)
    rows_updated: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[str | None] = mapped_column(Text)


class SourceFreshnessModel(Base):
    __tablename__ = "source_freshness"

    source_id: Mapped[str] = mapped_column(Text, ForeignKey("data_sources.id"), primary_key=True)
    dataset_id: Mapped[str] = mapped_column(Text, primary_key=True)
    latest_period: Mapped[date | None] = mapped_column(Date)
    latest_source_release: Mapped[datetime | None] = mapped_column(DateTime)
    last_checked_at: Mapped[datetime | None] = mapped_column(DateTime)
    status: Mapped[str | None] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text)


class DataQualityFlagModel(Base):
    __tablename__ = "data_quality_flags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    observation_id: Mapped[int | None] = mapped_column(ForeignKey("observations.id"))
    flag_type: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(Text, nullable=False)
    message: Mapped[str | None] = mapped_column(Text)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime)
    reviewed_by_user_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.id"))
    review_note: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class ScoreWeightModel(Base):
    __tablename__ = "score_weights"

    score_id: Mapped[str] = mapped_column(Text, primary_key=True)
    component_indicator_id: Mapped[str] = mapped_column(Text, ForeignKey("indicators.id"), primary_key=True)
    weight: Mapped[float] = mapped_column(Numeric, nullable=False)
    direction: Mapped[str] = mapped_column(Text, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    email: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    display_name: Mapped[str | None] = mapped_column(Text)
    avatar_url: Mapped[str | None] = mapped_column(Text)
    role: Mapped[str] = mapped_column(Text, default="user")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class UserPreferenceModel(Base):
    __tablename__ = "user_preferences"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), primary_key=True)
    default_location_id: Mapped[str | None] = mapped_column(Text)
    default_metric: Mapped[str | None] = mapped_column(Text)
    default_period: Mapped[str | None] = mapped_column(Text)
    default_basket_id: Mapped[str | None] = mapped_column(Text)
    household_size: Mapped[int] = mapped_column(Integer, default=1)
    theme: Mapped[str] = mapped_column(Text, default="system")
    data_density: Mapped[str] = mapped_column(Text, default="simple")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class SavedRegionModel(Base):
    __tablename__ = "saved_regions"
    __table_args__ = (
        UniqueConstraint("user_id", "location_id"),
    )

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), primary_key=True)
    location_id: Mapped[str] = mapped_column(Text, ForeignKey("locations.id"), primary_key=True)
    label: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class SavedBasketModel(Base):
    __tablename__ = "saved_baskets"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(Text, nullable=False)
    basket_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class AlertRuleModel(Base):
    __tablename__ = "alert_rules"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    location_id: Mapped[str] = mapped_column(Text, ForeignKey("locations.id"))
    indicator_id: Mapped[str] = mapped_column(Text, ForeignKey("indicators.id"))
    alert_type: Mapped[str] = mapped_column(Text, nullable=False)
    comparison_operator: Mapped[str] = mapped_column(Text, nullable=False)
    threshold_value: Mapped[float | None] = mapped_column(Numeric)
    change_value: Mapped[float | None] = mapped_column(Numeric)
    rank_value: Mapped[int | None] = mapped_column(Integer)
    frequency: Mapped[str] = mapped_column(Text, default="on_change")
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    channel_in_app: Mapped[bool] = mapped_column(Boolean, default=True)
    channel_email: Mapped[bool] = mapped_column(Boolean, default=False)
    last_triggered_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class NotificationModel(Base):
    __tablename__ = "notifications"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    alert_rule_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("alert_rules.id"))
    location_id: Mapped[str | None] = mapped_column(Text, ForeignKey("locations.id"))
    indicator_id: Mapped[str | None] = mapped_column(Text, ForeignKey("indicators.id"))
    type: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    value: Mapped[float | None] = mapped_column(Numeric)
    threshold_value: Mapped[float | None] = mapped_column(Numeric)
    period: Mapped[date | None] = mapped_column(Date)
    source_id: Mapped[str | None] = mapped_column(Text)
    freshness_status: Mapped[str | None] = mapped_column(Text)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class MonthlyReportModel(Base):
    __tablename__ = "monthly_reports"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    location_id: Mapped[str] = mapped_column(Text, ForeignKey("locations.id"))
    report_period: Mapped[date] = mapped_column(Date, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    report_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class NotificationPreferenceModel(Base):
    __tablename__ = "notification_preferences"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), primary_key=True)
    in_app_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    email_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    monthly_report_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    data_release_alerts_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    source_health_alerts_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class JobRunModel(Base):
    __tablename__ = "job_runs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    job_type: Mapped[str] = mapped_column(Text, nullable=False)
    job_name: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False)
    triggered_by_user_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.id"))
    trigger_source: Mapped[str] = mapped_column(Text, nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime)
    rows_fetched: Mapped[int] = mapped_column(Integer, default=0)
    rows_inserted: Mapped[int] = mapped_column(Integer, default=0)
    rows_updated: Mapped[int] = mapped_column(Integer, default=0)
    rows_failed: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[str | None] = mapped_column(Text)
    metadata_json: Mapped[dict | None] = mapped_column("metadata", JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class AdminAuditLogModel(Base):
    __tablename__ = "admin_audit_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.id"))
    action: Mapped[str] = mapped_column(Text, nullable=False)
    entity_type: Mapped[str | None] = mapped_column(Text)
    entity_id: Mapped[str | None] = mapped_column(Text)
    details: Mapped[dict | None] = mapped_column(JSON)
    ip_address: Mapped[str | None] = mapped_column(Text)
    user_agent: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class FeatureFlagModel(Base):
    __tablename__ = "feature_flags"

    key: Mapped[str] = mapped_column(Text, primary_key=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    description: Mapped[str | None] = mapped_column(Text)
    updated_by_user_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.id"))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class NpemGroupMetadataModel(Base):
    __tablename__ = "npem_group_metadata"

    group_code: Mapped[str] = mapped_column(Text, primary_key=True)
    group_label: Mapped[str] = mapped_column(Text, nullable=False)
    group_layer: Mapped[str] = mapped_column(Text, nullable=False)
    mutually_exclusive: Mapped[bool] = mapped_column(Boolean, nullable=False)
    baseline_year: Mapped[int | None] = mapped_column(Integer)
    hh_size_default: Mapped[float | None] = mapped_column(Numeric(4, 2))
    adults_default: Mapped[float | None] = mapped_column(Numeric(4, 2))
    children_default: Mapped[float | None] = mapped_column(Numeric(4, 2))
    selection_priority: Mapped[int | None] = mapped_column(Integer)
    rule_json: Mapped[dict | None] = mapped_column(JSON)
    governance_note: Mapped[str | None] = mapped_column(Text)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class NpemVariableModel(Base):
    __tablename__ = "npem_variables"

    variable_code: Mapped[str] = mapped_column(Text, primary_key=True)
    label: Mapped[str] = mapped_column(Text, nullable=False)
    definition: Mapped[str] = mapped_column(Text, nullable=False)
    unit_code: Mapped[str] = mapped_column(Text, nullable=False)
    preferred_source: Mapped[str | None] = mapped_column(Text)
    fallback_source: Mapped[str | None] = mapped_column(Text)
    expected_year: Mapped[int | None] = mapped_column(Integer)
    metric_family: Mapped[str | None] = mapped_column(Text)
    requires_nowcast: Mapped[bool] = mapped_column(Boolean, default=False)
    proxy_allowed: Mapped[bool] = mapped_column(Boolean, default=True)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class NpemRawDataModel(Base):
    __tablename__ = "npem_raw_data"
    __table_args__ = (
        Index("idx_npem_raw_geo_year_group_variable", "geography_code", "reference_year", "group_code", "variable_code"),
        UniqueConstraint("source_system", "source_series_id", "geography_code", "reference_year", "group_code", "variable_code"),
    )

    raw_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source_system: Mapped[str] = mapped_column(Text, nullable=False)
    source_series_id: Mapped[str | None] = mapped_column(Text)
    geography_code: Mapped[str] = mapped_column(Text, nullable=False)
    geography_name: Mapped[str | None] = mapped_column(Text)
    reference_year: Mapped[int] = mapped_column(Integer, nullable=False)
    reference_period: Mapped[str | None] = mapped_column(Text)
    variable_code: Mapped[str | None] = mapped_column(Text, ForeignKey("npem_variables.variable_code"))
    group_code: Mapped[str | None] = mapped_column(Text, ForeignKey("npem_group_metadata.group_code"))
    value_num: Mapped[float | None] = mapped_column(Numeric(18, 4))
    unit_code: Mapped[str | None] = mapped_column(Text)
    release_date: Mapped[date | None] = mapped_column(Date)
    access_date: Mapped[date | None] = mapped_column(Date)
    source_url_hash: Mapped[str | None] = mapped_column(Text)
    quality_flag: Mapped[str | None] = mapped_column(Text)
    provenance_id: Mapped[str | None] = mapped_column(String(36))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class NpemNormalizedScoreModel(Base):
    __tablename__ = "npem_normalized_scores"
    __table_args__ = (
        Index("idx_npem_norm_geo_year_group", "geography_code", "reference_year", "group_code"),
        UniqueConstraint("geography_code", "reference_year", "group_code", "component_code", "model_version"),
    )

    norm_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    geography_code: Mapped[str] = mapped_column(Text, nullable=False)
    reference_year: Mapped[int] = mapped_column(Integer, nullable=False)
    group_code: Mapped[str | None] = mapped_column(Text, ForeignKey("npem_group_metadata.group_code"))
    component_code: Mapped[str] = mapped_column(Text, nullable=False)
    raw_value: Mapped[float | None] = mapped_column(Numeric(18, 6))
    winsor_p5: Mapped[float | None] = mapped_column(Numeric(18, 6))
    winsor_p95: Mapped[float | None] = mapped_column(Numeric(18, 6))
    normalized_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    inversion_applied: Mapped[bool] = mapped_column(Boolean, default=False)
    imputation_level: Mapped[int] = mapped_column(Integer, default=0)
    confidence_component: Mapped[float | None] = mapped_column(Numeric(5, 2))
    model_version: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class NpemScenarioModel(Base):
    __tablename__ = "npem_scenarios"

    scenario_code: Mapped[str] = mapped_column(Text, primary_key=True)
    label: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    model_version: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class NpemScenarioWeightModel(Base):
    __tablename__ = "npem_scenario_weights"

    scenario_code: Mapped[str] = mapped_column(Text, ForeignKey("npem_scenarios.scenario_code"), primary_key=True)
    component_code: Mapped[str] = mapped_column(Text, primary_key=True)
    weight: Mapped[float] = mapped_column(Numeric(8, 6), nullable=False)


class NpemScoreModel(Base):
    __tablename__ = "npem_scores"
    __table_args__ = (
        Index("idx_npem_scores_geo_year_scenario", "geography_code", "reference_year", "scenario_code"),
        Index("idx_npem_scores_group", "group_code"),
        UniqueConstraint("geography_code", "reference_year", "group_code", "scenario_code", "model_version"),
    )

    score_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    geography_code: Mapped[str] = mapped_column(Text, nullable=False)
    reference_year: Mapped[int] = mapped_column(Integer, nullable=False)
    group_code: Mapped[str | None] = mapped_column(Text, ForeignKey("npem_group_metadata.group_code"))
    scenario_code: Mapped[str | None] = mapped_column(Text, ForeignKey("npem_scenarios.scenario_code"))
    base_composite: Mapped[float | None] = mapped_column(Numeric(5, 2))
    paf_value: Mapped[float | None] = mapped_column(Numeric(6, 4))
    final_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    score_rank_within_geo: Mapped[int | None] = mapped_column(Integer)
    confidence_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    confidence_grade: Mapped[str | None] = mapped_column(Text)
    model_version: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class NpemProvenanceModel(Base):
    __tablename__ = "npem_provenance"
    __table_args__ = (Index("idx_npem_provenance_score", "score_id"),)

    provenance_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    score_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("npem_scores.score_id"))
    source_system: Mapped[str] = mapped_column(Text, nullable=False)
    source_series_id: Mapped[str | None] = mapped_column(Text)
    citation_text: Mapped[str | None] = mapped_column(Text)
    release_date: Mapped[date | None] = mapped_column(Date)
    access_date: Mapped[date | None] = mapped_column(Date)
    transform_step: Mapped[str | None] = mapped_column(Text)
    licence_note: Mapped[str | None] = mapped_column(Text)
    source_url: Mapped[str | None] = mapped_column(Text)
    source_hash: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class NpemQualityComponentModel(Base):
    __tablename__ = "npem_quality_components"
    __table_args__ = (
        UniqueConstraint("geography_code", "reference_year", "group_code"),
    )

    quality_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    geography_code: Mapped[str] = mapped_column(Text, nullable=False)
    reference_year: Mapped[int] = mapped_column(Integer, nullable=False)
    group_code: Mapped[str | None] = mapped_column(Text, ForeignKey("npem_group_metadata.group_code"))
    coverage_ratio: Mapped[float | None] = mapped_column(Numeric(5, 4))
    recency_score: Mapped[float | None] = mapped_column(Numeric(5, 4))
    directness_score: Mapped[float | None] = mapped_column(Numeric(5, 4))
    reliability_score: Mapped[float | None] = mapped_column(Numeric(5, 4))
    suppression_penalty: Mapped[float | None] = mapped_column(Numeric(5, 4))
    proxy_share: Mapped[float | None] = mapped_column(Numeric(5, 4))
    confidence_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    confidence_grade: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class NpemProvincialAdjustmentModel(Base):
    __tablename__ = "npem_provincial_adjustments"

    adjustment_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    geography_code: Mapped[str] = mapped_column(Text, nullable=False)
    reference_year: Mapped[int] = mapped_column(Integer, nullable=False)
    mbm_total: Mapped[float | None] = mapped_column(Numeric(18, 4))
    modeled_essentials_prov: Mapped[float | None] = mapped_column(Numeric(18, 4))
    undercoverage_ratio: Mapped[float | None] = mapped_column(Numeric(18, 6))
    paf_value: Mapped[float | None] = mapped_column(Numeric(6, 4))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class BetaFeedbackModel(Base):
    __tablename__ = "beta_feedback"
    __table_args__ = (
        Index("idx_beta_feedback_status", "status"),
        Index("idx_beta_feedback_type", "feedback_type"),
        Index("idx_beta_feedback_created_at", "created_at"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.id"))
    page_path: Mapped[str | None] = mapped_column(Text)
    feedback_type: Mapped[str] = mapped_column(Text, nullable=False)
    rating: Mapped[int | None] = mapped_column(Integer)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str | None] = mapped_column(Text)
    metadata_json: Mapped[dict | None] = mapped_column("metadata", JSON)
    status: Mapped[str] = mapped_column(Text, default="new")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
