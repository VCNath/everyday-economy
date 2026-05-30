from app.models.economic import DataQualityFlagModel, utc_now


class DataQualityService:
    def __init__(self, session):
        self.session = session

    def list(self, severity: str | None = None, flag_type: str | None = None, reviewed: bool | None = None) -> list[DataQualityFlagModel]:
        query = self.session.query(DataQualityFlagModel)
        if severity:
            query = query.filter(DataQualityFlagModel.severity == severity)
        if flag_type:
            query = query.filter(DataQualityFlagModel.flag_type == flag_type)
        if reviewed is True:
            query = query.filter(DataQualityFlagModel.reviewed_at.isnot(None))
        if reviewed is False:
            query = query.filter(DataQualityFlagModel.reviewed_at.is_(None))
        return list(query.order_by(DataQualityFlagModel.created_at.desc()).all())

    def review(self, flag_id: int, *, user_id: str, note: str | None = None) -> DataQualityFlagModel | None:
        row = self.session.get(DataQualityFlagModel, flag_id)
        if row is None:
            return None
        row.reviewed_at = utc_now()
        row.reviewed_by_user_id = user_id
        row.review_note = note
        self.session.commit()
        self.session.refresh(row)
        return row

