from pydantic import BaseModel


class AlertRuleCreate(BaseModel):
    location_id: str
    indicator_id: str
    alert_type: str
    comparison_operator: str
    threshold_value: float | None = None
    change_value: float | None = None
    rank_value: int | None = None
    frequency: str = "on_change"
    enabled: bool = True
    channel_in_app: bool = True
    channel_email: bool = False


class AlertRuleUpdate(BaseModel):
    alert_type: str | None = None
    comparison_operator: str | None = None
    threshold_value: float | None = None
    change_value: float | None = None
    rank_value: int | None = None
    frequency: str | None = None
    enabled: bool | None = None
    channel_in_app: bool | None = None
    channel_email: bool | None = None


class AlertRuleResponse(BaseModel):
    id: str
    user_id: str
    location_id: str
    location_name: str
    indicator_id: str
    indicator_name: str
    alert_type: str
    comparison_operator: str
    threshold_value: float | None = None
    change_value: float | None = None
    rank_value: int | None = None
    frequency: str
    enabled: bool
    channels: dict[str, bool]
    last_triggered_at: str | None = None
    created_at: str
    updated_at: str


class NotificationResponse(BaseModel):
    id: str
    type: str
    severity: str
    title: str
    message: str
    location_id: str | None = None
    indicator_id: str | None = None
    value: float | None = None
    threshold_value: float | None = None
    period: str | None = None
    source_id: str | None = None
    freshness_status: str | None = None
    is_read: bool
    created_at: str


class NotificationListResponse(BaseModel):
    items: list[NotificationResponse]


class NotificationPreferencesResponse(BaseModel):
    in_app_enabled: bool
    email_enabled: bool
    monthly_report_enabled: bool
    data_release_alerts_enabled: bool
    source_health_alerts_enabled: bool


class NotificationPreferencesUpdate(BaseModel):
    in_app_enabled: bool | None = None
    email_enabled: bool | None = None
    monthly_report_enabled: bool | None = None
    data_release_alerts_enabled: bool | None = None
    source_health_alerts_enabled: bool | None = None


class MonthlyReportResponse(BaseModel):
    id: str
    location_id: str
    report_period: str
    title: str
    summary: str
    report_json: dict
    generated_at: str


class MonthlyReportListResponse(BaseModel):
    items: list[MonthlyReportResponse]


class AlertEvaluationResult(BaseModel):
    evaluated: int
    triggered: int

