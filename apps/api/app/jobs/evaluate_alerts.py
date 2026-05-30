from app.database import SessionLocal
from app.services.alert_evaluation_service import AlertEvaluationService
from app.services.job_run_service import JobRunService


def main() -> None:
    session = SessionLocal()
    job = None
    try:
        job = JobRunService(session).start(job_type="scheduled", job_name="evaluate_alerts", trigger_source="cli")
        result = AlertEvaluationService(session).evaluate()
        JobRunService(session).finish(job, status="succeeded", rows_updated=result["triggered"])
        print(f"Evaluated {result['evaluated']} rules, triggered {result['triggered']} alerts.")
    except Exception as exc:
        if job is not None:
            JobRunService(session).finish(job, status="failed", error_message=str(exc))
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
