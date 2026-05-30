from datetime import UTC, datetime

from sqlalchemy import func

from app.models.economic import (
    AlertRuleModel,
    DataQualityFlagModel,
    JobRunModel,
    MonthlyReportModel,
    NotificationModel,
    SourceFreshnessModel,
)
from app.services.dashboard_service import DashboardService
from app.services.job_run_service import JobRunService


class AdminService:
    def __init__(self, session):
        self.session = session
        self.dashboard = DashboardService(session)
        self.job_runs = JobRunService(session)

    def summary(self) -> dict:
        freshness = self.session.query(SourceFreshnessModel).all()
        healthy_sources = len([row for row in freshness if row.status == "healthy"])
        stale_sources = len([row for row in freshness if row.status in {"stale", "error", "partial"}])
        failed_jobs = self.session.query(func.count(JobRunModel.id)).filter(JobRunModel.status == "failed").scalar() or 0
        open_dq = self.session.query(func.count(DataQualityFlagModel.id)).filter(DataQualityFlagModel.reviewed_at.is_(None)).scalar() or 0
        active_alerts = self.session.query(func.count(AlertRuleModel.id)).filter(AlertRuleModel.enabled.is_(True)).scalar() or 0
        today = datetime.now(UTC).date()
        notes_today = self.session.query(func.count(NotificationModel.id)).filter(func.date(NotificationModel.created_at) == today).scalar() or 0
        month_start = datetime.now(UTC).replace(day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
        reports_month = self.session.query(func.count(MonthlyReportModel.id)).filter(MonthlyReportModel.generated_at >= month_start).scalar() or 0
        return {
            "healthy_sources": int(healthy_sources),
            "stale_sources": int(stale_sources),
            "failed_jobs": int(failed_jobs),
            "open_data_quality_flags": int(open_dq),
            "alert_rules_active": int(active_alerts),
            "notifications_generated_today": int(notes_today),
            "reports_generated_this_month": int(reports_month),
        }

    def source_health(self) -> list[dict]:
        sources = self.dashboard.source_status().sources
        runs = self.dashboard.source_runs().runs
        result = []
        for source in sources:
            run = next((candidate for candidate in runs if source.source.lower().startswith((candidate.source_id or "").replace("_", " ").lower()[:5])), None)
            result.append(
                {
                    "source": source.source,
                    "dataset": source.dataset,
                    "status": source.status,
                    "latest_period": source.latest_period,
                    "last_checked": source.last_checked,
                    "last_successful_run": run.finished_at if run and run.status == "succeeded" else None,
                    "error_message": run.error_message if run else None,
                    "rows_fetched": run.rows_fetched if run else 0,
                    "rows_inserted": run.rows_inserted if run else 0,
                    "rows_updated": run.rows_updated if run else 0,
                }
            )
        return result
