from html import escape

from app.models.economic import BetaFeedbackModel, utc_now


ALLOWED_STATUSES = {"new", "reviewed", "planned", "fixed", "closed"}


class FeedbackService:
    def __init__(self, session):
        self.session = session

    def create(
        self,
        *,
        feedback_type: str,
        message: str,
        user_id: str | None = None,
        page_path: str | None = None,
        rating: int | None = None,
        email: str | None = None,
        metadata: dict | None = None,
    ) -> BetaFeedbackModel:
        clean_message = escape(message.strip(), quote=False)
        row = BetaFeedbackModel(
            user_id=user_id,
            page_path=(page_path or "")[:500] or None,
            feedback_type=feedback_type,
            rating=rating,
            message=clean_message,
            email=email,
            metadata_json=self._safe_metadata(metadata),
            status="new",
        )
        self.session.add(row)
        self.session.commit()
        self.session.refresh(row)
        return row

    def list(self, *, status: str | None = None, feedback_type: str | None = None, limit: int = 100) -> list[BetaFeedbackModel]:
        query = self.session.query(BetaFeedbackModel)
        if status:
            query = query.filter(BetaFeedbackModel.status == status)
        if feedback_type:
            query = query.filter(BetaFeedbackModel.feedback_type == feedback_type)
        return list(query.order_by(BetaFeedbackModel.created_at.desc()).limit(min(limit, 250)).all())

    def update_status(self, feedback_id: str, status: str) -> BetaFeedbackModel | None:
        if status not in ALLOWED_STATUSES:
            raise ValueError("Unsupported feedback status.")
        row = self.session.get(BetaFeedbackModel, feedback_id)
        if row is None:
            return None
        row.status = status
        row.updated_at = utc_now()
        self.session.commit()
        self.session.refresh(row)
        return row

    def _safe_metadata(self, metadata: dict | None) -> dict | None:
        if not metadata:
            return None
        allowed = {"viewport", "userAgent", "region", "indicator", "source", "period"}
        return {key: str(value)[:500] for key, value in metadata.items() if key in allowed and value is not None}
