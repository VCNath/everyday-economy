from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_admin_user, get_db
from app.models.economic import UserModel
from app.schemas.admin import (
    AdminAuditLogResponse,
    AdminDashboardSummary,
    AdminJobRunListResponse,
    AdminJobRunResponse,
    AdminJobTriggerRequest,
    AdminJobTriggerResponse,
    AdminSourceHealthResponse,
    DataQualityFlagListResponse,
    DataQualityFlagResponse,
    FeatureFlagResponse,
    FeatureFlagUpdate,
)
from app.services.admin_audit_service import AdminAuditService
from app.services.admin_service import AdminService
from app.services.alert_evaluation_service import AlertEvaluationService
from app.services.data_quality_service import DataQualityService
from app.services.feature_flag_service import FeatureFlagService
from app.services.ingestion import EconomicIngestionService
from app.services.job_run_service import JobRunService
from app.services.leaderboards import LeaderboardBuilder
from app.services.monthly_report_service import MonthlyReportService
from app.services.npem_scoring_service import NpemScoringService
from app.models.economic import AlertRuleModel, NotificationModel, SavedRegionModel

router = APIRouter(prefix="/admin", tags=["admin"])


def _job_to_response(row) -> AdminJobRunResponse:
    duration = None
    if row.finished_at:
        duration = int((row.finished_at - row.started_at).total_seconds())
    return AdminJobRunResponse(
        id=row.id,
        job_type=row.job_type,
        job_name=row.job_name,
        status=row.status,
        trigger_source=row.trigger_source,
        triggered_by_user_id=row.triggered_by_user_id,
        started_at=row.started_at.isoformat(),
        finished_at=row.finished_at.isoformat() if row.finished_at else None,
        duration_seconds=duration,
        rows_fetched=row.rows_fetched,
        rows_inserted=row.rows_inserted,
        rows_updated=row.rows_updated,
        rows_failed=row.rows_failed,
        error_message=row.error_message,
        metadata=row.metadata_json,
    )


@router.get("/summary", response_model=AdminDashboardSummary)
def summary(_admin=Depends(get_admin_user), db=Depends(get_db)):
    return AdminService(db).summary()


@router.get("/source-health", response_model=list[AdminSourceHealthResponse])
def source_health(_admin=Depends(get_admin_user), db=Depends(get_db)):
    return [AdminSourceHealthResponse(**row) for row in AdminService(db).source_health()]


@router.get("/job-runs", response_model=AdminJobRunListResponse)
def list_job_runs(
    job_type: str | None = None,
    status: str | None = None,
    limit: int = 100,
    _admin=Depends(get_admin_user),
    db=Depends(get_db),
):
    rows = JobRunService(db).list(limit=limit, job_type=job_type, status=status)
    return AdminJobRunListResponse(items=[_job_to_response(row) for row in rows])


@router.get("/job-runs/{job_run_id}", response_model=AdminJobRunResponse)
def get_job_run(job_run_id: str, _admin=Depends(get_admin_user), db=Depends(get_db)):
    row = JobRunService(db).get(job_run_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Job run not found.")
    return _job_to_response(row)


def _run_whitelisted_job(db, admin_user: UserModel, job_name: str):
    whitelist = {
        "refresh_statcan_cpi",
        "refresh_statcan_gas",
        "refresh_statcan_labour",
        "refresh_bank_of_canada",
        "refresh_all_sources",
        "build_leaderboards",
        "calculate_baskets",
        "evaluate_alerts",
        "generate_monthly_reports",
        "calculate_npem",
    }
    if job_name not in whitelist:
        raise HTTPException(status_code=400, detail="Unknown or unsupported job.")
    runs = JobRunService(db)
    audits = AdminAuditService(db)
    run = runs.start(job_type="manual", job_name=job_name, trigger_source="admin_api", triggered_by_user_id=admin_user.id)
    try:
        rows_fetched = rows_inserted = rows_updated = rows_failed = 0
        if job_name == "refresh_statcan_cpi":
            result = EconomicIngestionService(db).ingest_cpi()
            rows_fetched, rows_inserted, rows_updated = result.rows_fetched, result.rows_inserted, result.rows_updated
        elif job_name == "refresh_statcan_gas":
            result = EconomicIngestionService(db).ingest_gas()
            rows_fetched, rows_inserted, rows_updated = result.rows_fetched, result.rows_inserted, result.rows_updated
        elif job_name == "refresh_statcan_labour":
            result = EconomicIngestionService(db).ingest_labour()
            rows_fetched, rows_inserted, rows_updated = result.rows_fetched, result.rows_inserted, result.rows_updated
        elif job_name == "refresh_bank_of_canada":
            result = EconomicIngestionService(db).ingest_bank_of_canada()
            rows_fetched, rows_inserted, rows_updated = result.rows_fetched, result.rows_inserted, result.rows_updated
        elif job_name == "refresh_all_sources":
            service = EconomicIngestionService(db)
            service.ingest_cpi()
            service.ingest_gas()
            service.ingest_labour()
            service.ingest_bank_of_canada()
            service.calculate_changes()
            rows_updated = 1
        elif job_name == "build_leaderboards":
            rows_updated = LeaderboardBuilder(db).build_all()
        elif job_name == "calculate_baskets":
            rows_updated = EconomicIngestionService(db).build_baskets()
        elif job_name == "evaluate_alerts":
            result = AlertEvaluationService(db).evaluate()
            rows_updated = result["triggered"]
        elif job_name == "generate_monthly_reports":
            rows_updated = MonthlyReportService(db).generate_monthly_for_all_users()
        elif job_name == "calculate_npem":
            result = NpemScoringService(db).calculate_demo_scores()
            rows_updated = result["score_rows"]
        run = runs.finish(run, status="succeeded", rows_fetched=rows_fetched, rows_inserted=rows_inserted, rows_updated=rows_updated, rows_failed=rows_failed)
        audits.log(user_id=admin_user.id, action="admin.job_trigger", entity_type="job_run", entity_id=run.id, details={"job_name": job_name, "status": "succeeded"})
        return run
    except Exception as exc:
        run = runs.finish(run, status="failed", error_message=str(exc))
        audits.log(user_id=admin_user.id, action="admin.job_trigger", entity_type="job_run", entity_id=run.id, details={"job_name": job_name, "status": "failed", "error": str(exc)})
        raise HTTPException(status_code=500, detail=f"Job failed: {exc}") from exc


@router.post("/jobs/refresh-source", response_model=AdminJobTriggerResponse)
def trigger_refresh_source(payload: AdminJobTriggerRequest, admin_user: UserModel = Depends(get_admin_user), db=Depends(get_db)):
    row = _run_whitelisted_job(db, admin_user, payload.job_name)
    return AdminJobTriggerResponse(job_run=_job_to_response(row))


@router.post("/jobs/refresh-cpi", response_model=AdminJobTriggerResponse)
def trigger_refresh_cpi(admin_user: UserModel = Depends(get_admin_user), db=Depends(get_db)):
    row = _run_whitelisted_job(db, admin_user, "refresh_statcan_cpi")
    return AdminJobTriggerResponse(job_run=_job_to_response(row))


@router.post("/jobs/refresh-gas", response_model=AdminJobTriggerResponse)
def trigger_refresh_gas(admin_user: UserModel = Depends(get_admin_user), db=Depends(get_db)):
    row = _run_whitelisted_job(db, admin_user, "refresh_statcan_gas")
    return AdminJobTriggerResponse(job_run=_job_to_response(row))


@router.post("/jobs/refresh-labour", response_model=AdminJobTriggerResponse)
def trigger_refresh_labour(admin_user: UserModel = Depends(get_admin_user), db=Depends(get_db)):
    row = _run_whitelisted_job(db, admin_user, "refresh_statcan_labour")
    return AdminJobTriggerResponse(job_run=_job_to_response(row))


@router.post("/jobs/refresh-all", response_model=AdminJobTriggerResponse)
def trigger_refresh_all(admin_user: UserModel = Depends(get_admin_user), db=Depends(get_db)):
    row = _run_whitelisted_job(db, admin_user, "refresh_all_sources")
    return AdminJobTriggerResponse(job_run=_job_to_response(row))


@router.post("/jobs/evaluate-alerts", response_model=AdminJobTriggerResponse)
def trigger_evaluate_alerts(admin_user: UserModel = Depends(get_admin_user), db=Depends(get_db)):
    row = _run_whitelisted_job(db, admin_user, "evaluate_alerts")
    return AdminJobTriggerResponse(job_run=_job_to_response(row))


@router.post("/jobs/generate-monthly-reports", response_model=AdminJobTriggerResponse)
def trigger_monthly_reports(admin_user: UserModel = Depends(get_admin_user), db=Depends(get_db)):
    row = _run_whitelisted_job(db, admin_user, "generate_monthly_reports")
    return AdminJobTriggerResponse(job_run=_job_to_response(row))


@router.post("/jobs/build-leaderboards", response_model=AdminJobTriggerResponse)
def trigger_leaderboards(admin_user: UserModel = Depends(get_admin_user), db=Depends(get_db)):
    row = _run_whitelisted_job(db, admin_user, "build_leaderboards")
    return AdminJobTriggerResponse(job_run=_job_to_response(row))


@router.post("/jobs/calculate-baskets", response_model=AdminJobTriggerResponse)
def trigger_baskets(admin_user: UserModel = Depends(get_admin_user), db=Depends(get_db)):
    row = _run_whitelisted_job(db, admin_user, "calculate_baskets")
    return AdminJobTriggerResponse(job_run=_job_to_response(row))


@router.post("/jobs/calculate-npem", response_model=AdminJobTriggerResponse)
def trigger_npem(admin_user: UserModel = Depends(get_admin_user), db=Depends(get_db)):
    row = _run_whitelisted_job(db, admin_user, "calculate_npem")
    return AdminJobTriggerResponse(job_run=_job_to_response(row))


@router.get("/data-quality", response_model=DataQualityFlagListResponse)
def list_data_quality(
    severity: str | None = None,
    flag_type: str | None = None,
    reviewed: bool | None = None,
    _admin=Depends(get_admin_user),
    db=Depends(get_db),
):
    rows = DataQualityService(db).list(severity=severity, flag_type=flag_type, reviewed=reviewed)
    return DataQualityFlagListResponse(
        items=[
            DataQualityFlagResponse(
                id=row.id,
                flag_type=row.flag_type,
                severity=row.severity,
                message=row.message,
                created_at=row.created_at.isoformat(),
                reviewed_at=row.reviewed_at.isoformat() if row.reviewed_at else None,
                reviewed_by_user_id=row.reviewed_by_user_id,
                review_note=row.review_note,
            )
            for row in rows
        ]
    )


@router.post("/data-quality/{flag_id}/review", response_model=DataQualityFlagResponse)
def review_data_quality(flag_id: int, review_note: str | None = None, admin_user: UserModel = Depends(get_admin_user), db=Depends(get_db)):
    row = DataQualityService(db).review(flag_id, user_id=admin_user.id, note=review_note)
    if row is None:
        raise HTTPException(status_code=404, detail="Data quality flag not found.")
    AdminAuditService(db).log(user_id=admin_user.id, action="admin.data_quality.review", entity_type="data_quality_flag", entity_id=str(flag_id))
    return DataQualityFlagResponse(
        id=row.id,
        flag_type=row.flag_type,
        severity=row.severity,
        message=row.message,
        created_at=row.created_at.isoformat(),
        reviewed_at=row.reviewed_at.isoformat() if row.reviewed_at else None,
        reviewed_by_user_id=row.reviewed_by_user_id,
        review_note=row.review_note,
    )


@router.get("/audit-logs", response_model=list[AdminAuditLogResponse])
def list_audit_logs(limit: int = 100, _admin=Depends(get_admin_user), db=Depends(get_db)):
    return [
        AdminAuditLogResponse(
            id=row.id,
            user_id=row.user_id,
            action=row.action,
            entity_type=row.entity_type,
            entity_id=row.entity_id,
            details=row.details,
            ip_address=row.ip_address,
            user_agent=row.user_agent,
            created_at=row.created_at.isoformat(),
        )
        for row in AdminAuditService(db).list(limit=limit)
    ]


@router.get("/feature-flags", response_model=list[FeatureFlagResponse])
def list_feature_flags(_admin=Depends(get_admin_user), db=Depends(get_db)):
    rows = FeatureFlagService(db).list()
    return [
        FeatureFlagResponse(
            key=row.key,
            enabled=row.enabled,
            description=row.description,
            updated_by_user_id=row.updated_by_user_id,
            updated_at=row.updated_at.isoformat(),
            created_at=row.created_at.isoformat(),
        )
        for row in rows
    ]


@router.put("/feature-flags/{key}", response_model=FeatureFlagResponse)
def update_feature_flag(key: str, payload: FeatureFlagUpdate, admin_user: UserModel = Depends(get_admin_user), db=Depends(get_db)):
    row = FeatureFlagService(db).update(key, enabled=payload.enabled, description=payload.description, updated_by_user_id=admin_user.id)
    AdminAuditService(db).log(user_id=admin_user.id, action="admin.feature_flag.update", entity_type="feature_flag", entity_id=key, details={"enabled": payload.enabled})
    return FeatureFlagResponse(
        key=row.key,
        enabled=row.enabled,
        description=row.description,
        updated_by_user_id=row.updated_by_user_id,
        updated_at=row.updated_at.isoformat(),
        created_at=row.created_at.isoformat(),
    )


@router.get("/users")
def list_users(_admin=Depends(get_admin_user), db=Depends(get_db)):
    users = db.query(UserModel).order_by(UserModel.created_at.desc()).all()
    result = []
    for user in users:
        result.append(
            {
                "id": user.id,
                "email": user.email,
                "display_name": user.display_name,
                "role": user.role,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "saved_region_count": db.query(SavedRegionModel).filter(SavedRegionModel.user_id == user.id).count(),
                "alert_rule_count": db.query(AlertRuleModel).filter(AlertRuleModel.user_id == user.id).count(),
                "notification_count": db.query(NotificationModel).filter(NotificationModel.user_id == user.id).count(),
            }
        )
    return {"items": result}
