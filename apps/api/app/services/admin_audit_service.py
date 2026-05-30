from app.models.economic import AdminAuditLogModel


class AdminAuditService:
    def __init__(self, session):
        self.session = session

    def log(
        self,
        *,
        user_id: str | None,
        action: str,
        entity_type: str | None = None,
        entity_id: str | None = None,
        details: dict | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> AdminAuditLogModel:
        row = AdminAuditLogModel(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.session.add(row)
        self.session.commit()
        self.session.refresh(row)
        return row

    def list(self, limit: int = 100) -> list[AdminAuditLogModel]:
        return list(
            self.session.query(AdminAuditLogModel)
            .order_by(AdminAuditLogModel.created_at.desc())
            .limit(limit)
            .all()
        )

