from app.database import SessionLocal
from app.services.job_run_service import JobRunService
from app.services.monthly_report_service import MonthlyReportService


def main() -> None:
    session = SessionLocal()
    job = None
    try:
        job = JobRunService(session).start(job_type="scheduled", job_name="generate_monthly_reports", trigger_source="cli")
        created = MonthlyReportService(session).generate_monthly_for_all_users()
        JobRunService(session).finish(job, status="succeeded", rows_updated=created)
        print(f"Generated {created} monthly reports.")
    except Exception as exc:
        if job is not None:
            JobRunService(session).finish(job, status="failed", error_message=str(exc))
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
