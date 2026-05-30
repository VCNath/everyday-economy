from sqlalchemy import select

from app.models.economic import NotificationModel


class NotificationService:
    def __init__(self, session):
        self.session = session

    def list(self, user_id: str, unread_only: bool = False) -> list[NotificationModel]:
        stmt = select(NotificationModel).where(NotificationModel.user_id == user_id).order_by(NotificationModel.created_at.desc())
        if unread_only:
            stmt = stmt.where(NotificationModel.is_read.is_(False))
        return list(self.session.scalars(stmt))

    def create(self, **kwargs) -> NotificationModel:
        row = NotificationModel(**kwargs)
        self.session.add(row)
        self.session.commit()
        self.session.refresh(row)
        return row

    def unread_count(self, user_id: str) -> int:
        return len(self.list(user_id, unread_only=True))

    def mark_read(self, user_id: str, notification_id: str) -> bool:
        row = self.session.get(NotificationModel, notification_id)
        if row is None or row.user_id != user_id:
            return False
        row.is_read = True
        self.session.commit()
        return True

    def mark_all_read(self, user_id: str) -> int:
        rows = self.list(user_id, unread_only=True)
        for row in rows:
            row.is_read = True
        self.session.commit()
        return len(rows)

