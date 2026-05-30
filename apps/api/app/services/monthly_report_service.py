from datetime import date, datetime

from sqlalchemy import select

from app.models.economic import MonthlyReportModel, UserModel
from app.services.dashboard_service import DashboardService
from app.services.notification_service import NotificationService
from app.services.notification_preferences_service import NotificationPreferencesService
from app.services.saved_regions_service import SavedRegionsService


class MonthlyReportService:
    def __init__(self, session):
        self.session = session
        self.dashboard = DashboardService(session)
        self.saved_regions = SavedRegionsService(session)
        self.notifications = NotificationService(session)
        self.notification_prefs = NotificationPreferencesService(session)

    def list_reports(self, user_id: str) -> list[MonthlyReportModel]:
        return list(
            self.session.scalars(
                select(MonthlyReportModel).where(MonthlyReportModel.user_id == user_id).order_by(MonthlyReportModel.generated_at.desc())
            )
        )

    def get_report(self, user_id: str, report_id: str) -> MonthlyReportModel | None:
        report = self.session.get(MonthlyReportModel, report_id)
        if report is None or report.user_id != user_id:
            return None
        return report

    def generate_for_region(self, user_id: str, location_id: str) -> MonthlyReportModel:
        summary = self.dashboard.get_region_summary(location_id)
        period_raw = summary.period if summary else datetime.now().strftime("%Y-%m")
        report_period = date.fromisoformat(f"{period_raw}-01")
        name = summary.name if summary else location_id
        metrics = summary.metrics if summary else {}
        text = (
            f"In {period_raw}, {name} recorded CPI {metrics.get('cpi_all_items_yoy', 0):.1f}%, "
            f"food {metrics.get('cpi_food_yoy', 0):.1f}%, gas {metrics.get('gas_regular_cents_litre', 0):.1f}¢/L, "
            f"unemployment {metrics.get('unemployment_rate', 0):.1f}%, basket ${metrics.get('basic_basket_monthly_cost', 0):.2f}, "
            f"affordability {metrics.get('affordability_score', 0):.1f}."
        )
        report = MonthlyReportModel(
            user_id=user_id,
            location_id=location_id,
            report_period=report_period,
            title=f"{name} Monthly Affordability Report",
            summary=text,
            report_json={"location": name, "period": period_raw, "metrics": metrics, "source_notes": summary.sources if summary else []},
        )
        self.session.add(report)
        self.session.commit()
        self.session.refresh(report)
        prefs = self.notification_prefs.get_or_create(user_id)
        if prefs.in_app_enabled:
            self.notifications.create(
                user_id=user_id,
                location_id=location_id,
                type="report",
                severity="info",
                title=f"{name} monthly report ready",
                message=f"Your {name} monthly affordability report is ready.",
                period=report_period,
                freshness_status="healthy",
            )
        return report

    def generate_monthly_for_all_users(self) -> int:
        users = list(self.session.scalars(select(UserModel)))
        created = 0
        for user in users:
            prefs = self.notification_prefs.get_or_create(user.id)
            if not prefs.monthly_report_enabled:
                continue
            for row in self.saved_regions.list(user.id):
                self.generate_for_region(user.id, row.location_id)
                created += 1
        return created

