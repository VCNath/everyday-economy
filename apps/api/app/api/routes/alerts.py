from datetime import date

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_current_user, get_db
from app.models.economic import IndicatorModel, LocationModel, UserModel
from app.schemas.alerts import (
    AlertRuleCreate,
    AlertRuleResponse,
    AlertRuleUpdate,
    MonthlyReportListResponse,
    MonthlyReportResponse,
    NotificationListResponse,
    NotificationPreferencesResponse,
    NotificationPreferencesUpdate,
)
from app.services.alert_evaluation_service import AlertEvaluationService
from app.services.alert_rules_service import AlertRulesService
from app.services.monthly_report_service import MonthlyReportService
from app.services.notification_preferences_service import NotificationPreferencesService
from app.services.notification_service import NotificationService

router = APIRouter(prefix="/me", tags=["alerts"])
admin_router = APIRouter(prefix="/admin", tags=["alerts-admin"])


def _rule_to_response(db, row) -> AlertRuleResponse:
    location = db.get(LocationModel, row.location_id)
    indicator = db.get(IndicatorModel, row.indicator_id)
    return AlertRuleResponse(
        id=row.id,
        user_id=row.user_id,
        location_id=row.location_id,
        location_name=location.name if location else row.location_id,
        indicator_id=row.indicator_id,
        indicator_name=indicator.name if indicator else row.indicator_id,
        alert_type=row.alert_type,
        comparison_operator=row.comparison_operator,
        threshold_value=float(row.threshold_value) if row.threshold_value is not None else None,
        change_value=float(row.change_value) if row.change_value is not None else None,
        rank_value=row.rank_value,
        frequency=row.frequency,
        enabled=row.enabled,
        channels={"in_app": row.channel_in_app, "email": row.channel_email},
        last_triggered_at=row.last_triggered_at.isoformat() if row.last_triggered_at else None,
        created_at=row.created_at.isoformat(),
        updated_at=row.updated_at.isoformat(),
    )


@router.get("/alerts", response_model=list[AlertRuleResponse])
def list_alerts(current_user: UserModel = Depends(get_current_user), db=Depends(get_db)):
    rows = AlertRulesService(db).list(current_user.id)
    return [_rule_to_response(db, row) for row in rows]


@router.post("/alerts", response_model=AlertRuleResponse)
def create_alert(payload: AlertRuleCreate, current_user: UserModel = Depends(get_current_user), db=Depends(get_db)):
    row = AlertRulesService(db).create(current_user.id, payload.model_dump())
    return _rule_to_response(db, row)


@router.get("/alerts/{alert_id}", response_model=AlertRuleResponse)
def get_alert(alert_id: str, current_user: UserModel = Depends(get_current_user), db=Depends(get_db)):
    row = AlertRulesService(db).get(current_user.id, alert_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Alert rule not found.")
    return _rule_to_response(db, row)


@router.put("/alerts/{alert_id}", response_model=AlertRuleResponse)
def update_alert(alert_id: str, payload: AlertRuleUpdate, current_user: UserModel = Depends(get_current_user), db=Depends(get_db)):
    row = AlertRulesService(db).update(current_user.id, alert_id, payload.model_dump(exclude_unset=True))
    if row is None:
        raise HTTPException(status_code=404, detail="Alert rule not found.")
    return _rule_to_response(db, row)


@router.delete("/alerts/{alert_id}")
def delete_alert(alert_id: str, current_user: UserModel = Depends(get_current_user), db=Depends(get_db)):
    deleted = AlertRulesService(db).delete(current_user.id, alert_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Alert rule not found.")
    return {"status": "ok"}


@router.post("/alerts/{alert_id}/enable")
def enable_alert(alert_id: str, current_user: UserModel = Depends(get_current_user), db=Depends(get_db)):
    if not AlertRulesService(db).set_enabled(current_user.id, alert_id, True):
        raise HTTPException(status_code=404, detail="Alert rule not found.")
    return {"status": "ok"}


@router.post("/alerts/{alert_id}/disable")
def disable_alert(alert_id: str, current_user: UserModel = Depends(get_current_user), db=Depends(get_db)):
    if not AlertRulesService(db).set_enabled(current_user.id, alert_id, False):
        raise HTTPException(status_code=404, detail="Alert rule not found.")
    return {"status": "ok"}


@router.get("/notifications", response_model=NotificationListResponse)
def list_notifications(unread_only: bool = False, current_user: UserModel = Depends(get_current_user), db=Depends(get_db)):
    rows = NotificationService(db).list(current_user.id, unread_only=unread_only)
    return NotificationListResponse(
        items=[
            {
                "id": row.id,
                "type": row.type,
                "severity": row.severity,
                "title": row.title,
                "message": row.message,
                "location_id": row.location_id,
                "indicator_id": row.indicator_id,
                "value": float(row.value) if row.value is not None else None,
                "threshold_value": float(row.threshold_value) if row.threshold_value is not None else None,
                "period": row.period.isoformat() if row.period else None,
                "source_id": row.source_id,
                "freshness_status": row.freshness_status,
                "is_read": row.is_read,
                "created_at": row.created_at.isoformat(),
            }
            for row in rows
        ]
    )


@router.get("/notifications/unread-count")
def unread_count(current_user: UserModel = Depends(get_current_user), db=Depends(get_db)):
    return {"count": NotificationService(db).unread_count(current_user.id)}


@router.post("/notifications/{notification_id}/read")
def mark_read(notification_id: str, current_user: UserModel = Depends(get_current_user), db=Depends(get_db)):
    if not NotificationService(db).mark_read(current_user.id, notification_id):
        raise HTTPException(status_code=404, detail="Notification not found.")
    return {"status": "ok"}


@router.post("/notifications/read-all")
def mark_all_read(current_user: UserModel = Depends(get_current_user), db=Depends(get_db)):
    return {"updated": NotificationService(db).mark_all_read(current_user.id)}


@router.get("/notification-preferences", response_model=NotificationPreferencesResponse)
def get_notification_preferences(current_user: UserModel = Depends(get_current_user), db=Depends(get_db)):
    pref = NotificationPreferencesService(db).get_or_create(current_user.id)
    return NotificationPreferencesResponse(
        in_app_enabled=pref.in_app_enabled,
        email_enabled=pref.email_enabled,
        monthly_report_enabled=pref.monthly_report_enabled,
        data_release_alerts_enabled=pref.data_release_alerts_enabled,
        source_health_alerts_enabled=pref.source_health_alerts_enabled,
    )


@router.put("/notification-preferences", response_model=NotificationPreferencesResponse)
def update_notification_preferences(payload: NotificationPreferencesUpdate, current_user: UserModel = Depends(get_current_user), db=Depends(get_db)):
    pref = NotificationPreferencesService(db).update(current_user.id, payload.model_dump(exclude_unset=True))
    return NotificationPreferencesResponse(
        in_app_enabled=pref.in_app_enabled,
        email_enabled=pref.email_enabled,
        monthly_report_enabled=pref.monthly_report_enabled,
        data_release_alerts_enabled=pref.data_release_alerts_enabled,
        source_health_alerts_enabled=pref.source_health_alerts_enabled,
    )


@router.get("/reports", response_model=MonthlyReportListResponse)
def list_reports(current_user: UserModel = Depends(get_current_user), db=Depends(get_db)):
    rows = MonthlyReportService(db).list_reports(current_user.id)
    return MonthlyReportListResponse(
        items=[
            MonthlyReportResponse(
                id=row.id,
                location_id=row.location_id,
                report_period=row.report_period.isoformat(),
                title=row.title,
                summary=row.summary,
                report_json=row.report_json,
                generated_at=row.generated_at.isoformat(),
            )
            for row in rows
        ]
    )


@router.get("/reports/{report_id}", response_model=MonthlyReportResponse)
def get_report(report_id: str, current_user: UserModel = Depends(get_current_user), db=Depends(get_db)):
    row = MonthlyReportService(db).get_report(current_user.id, report_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Report not found.")
    return MonthlyReportResponse(
        id=row.id,
        location_id=row.location_id,
        report_period=row.report_period.isoformat(),
        title=row.title,
        summary=row.summary,
        report_json=row.report_json,
        generated_at=row.generated_at.isoformat(),
    )


@router.post("/reports/generate", response_model=MonthlyReportResponse)
def generate_report(location_id: str, current_user: UserModel = Depends(get_current_user), db=Depends(get_db)):
    row = MonthlyReportService(db).generate_for_region(current_user.id, location_id)
    return MonthlyReportResponse(
        id=row.id,
        location_id=row.location_id,
        report_period=row.report_period.isoformat(),
        title=row.title,
        summary=row.summary,
        report_json=row.report_json,
        generated_at=row.generated_at.isoformat(),
    )


@router.post("/reports/generate-monthly")
def generate_monthly(current_user: UserModel = Depends(get_current_user), db=Depends(get_db)):
    # user-scoped generation
    service = MonthlyReportService(db)
    count = 0
    for saved in service.saved_regions.list(current_user.id):
        service.generate_for_region(current_user.id, saved.location_id)
        count += 1
    return {"generated": count}


@admin_router.post("/evaluate-alerts")
def evaluate_alerts_admin(current_user: UserModel = Depends(get_current_user), db=Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only.")
    return AlertEvaluationService(db).evaluate()


@admin_router.post("/generate-monthly-reports")
def generate_monthly_reports_admin(current_user: UserModel = Depends(get_current_user), db=Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only.")
    created = MonthlyReportService(db).generate_monthly_for_all_users()
    return {"generated": created}
