from app.models.economic import JobRunModel, utc_now


class JobRunService:
    def __init__(self, session):
        self.session = session

    def start(
        self,
        *,
        job_type: str,
        job_name: str,
        trigger_source: str,
        triggered_by_user_id: str | None = None,
        metadata: dict | None = None,
    ) -> JobRunModel:
        row = JobRunModel(
            job_type=job_type,
            job_name=job_name,
            status="running",
            trigger_source=trigger_source,
            triggered_by_user_id=triggered_by_user_id,
            metadata_json=metadata,
        )
        self.session.add(row)
        self.session.commit()
        self.session.refresh(row)
        return row

    def finish(
        self,
        row: JobRunModel,
        *,
        status: str,
        rows_fetched: int = 0,
        rows_inserted: int = 0,
        rows_updated: int = 0,
        rows_failed: int = 0,
        error_message: str | None = None,
    ) -> JobRunModel:
        row.status = status
        row.rows_fetched = rows_fetched
        row.rows_inserted = rows_inserted
        row.rows_updated = rows_updated
        row.rows_failed = rows_failed
        row.error_message = error_message
        row.finished_at = utc_now()
        self.session.commit()
        self.session.refresh(row)
        return row

    def list(self, limit: int = 100, job_type: str | None = None, status: str | None = None) -> list[JobRunModel]:
        query = self.session.query(JobRunModel)
        if job_type:
            query = query.filter(JobRunModel.job_type == job_type)
        if status:
            query = query.filter(JobRunModel.status == status)
        return list(query.order_by(JobRunModel.started_at.desc()).limit(limit).all())

    def get(self, job_run_id: str) -> JobRunModel | None:
        return self.session.get(JobRunModel, job_run_id)

