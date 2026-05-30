from pydantic import BaseModel


class AdminSourceHealthResponse(BaseModel):
    source: str
    dataset: str
    status: str
    latest_period: str | None = None
    last_checked: str | None = None
    last_successful_run: str | None = None
    error_message: str | None = None
    rows_fetched: int = 0
    rows_inserted: int = 0
    rows_updated: int = 0


class AdminJobRunResponse(BaseModel):
    id: str
    job_type: str
    job_name: str
    status: str
    trigger_source: str
    triggered_by_user_id: str | None = None
    started_at: str
    finished_at: str | None = None
    duration_seconds: int | None = None
    rows_fetched: int = 0
    rows_inserted: int = 0
    rows_updated: int = 0
    rows_failed: int = 0
    error_message: str | None = None
    metadata: dict | None = None


class AdminJobRunListResponse(BaseModel):
    items: list[AdminJobRunResponse]


class AdminJobTriggerRequest(BaseModel):
    job_name: str


class AdminJobTriggerResponse(BaseModel):
    job_run: AdminJobRunResponse


class DataQualityFlagResponse(BaseModel):
    id: int
    flag_type: str
    severity: str
    message: str | None = None
    created_at: str
    reviewed_at: str | None = None
    reviewed_by_user_id: str | None = None
    review_note: str | None = None


class DataQualityFlagListResponse(BaseModel):
    items: list[DataQualityFlagResponse]


class AdminAuditLogResponse(BaseModel):
    id: str
    user_id: str | None = None
    action: str
    entity_type: str | None = None
    entity_id: str | None = None
    details: dict | None = None
    ip_address: str | None = None
    user_agent: str | None = None
    created_at: str


class FeatureFlagResponse(BaseModel):
    key: str
    enabled: bool
    description: str | None = None
    updated_by_user_id: str | None = None
    updated_at: str
    created_at: str


class FeatureFlagUpdate(BaseModel):
    enabled: bool
    description: str | None = None


class AdminDashboardSummary(BaseModel):
    healthy_sources: int
    stale_sources: int
    failed_jobs: int
    open_data_quality_flags: int
    alert_rules_active: int
    notifications_generated_today: int
    reports_generated_this_month: int

