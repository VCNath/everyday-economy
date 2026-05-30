from app.models.economic import FeatureFlagModel, utc_now

DEFAULT_FLAGS: dict[str, str] = {
    "auth": "Authentication features",
    "savedRegions": "Saved region watchlist",
    "savedBaskets": "Saved baskets",
    "watchlist": "Watchlist views",
    "alerts": "Alerting features",
    "monthlyReports": "Monthly reports",
    "emailNotifications": "Email notifications",
    "adminPanel": "Admin operations pages",
    "cityLevelData": "City level metrics",
    "globalComparison": "Global comparison views",
    "paidPlans": "Paid plan features",
    "publicApi": "Public API surface",
    "aiAssistant": "AI assistant features",
}


class FeatureFlagService:
    def __init__(self, session):
        self.session = session

    def ensure_defaults(self) -> None:
        changed = False
        for key, desc in DEFAULT_FLAGS.items():
            existing = self.session.get(FeatureFlagModel, key)
            if existing is None:
                self.session.add(FeatureFlagModel(key=key, enabled=False, description=desc))
                changed = True
        if changed:
            self.session.commit()

    def list(self) -> list[FeatureFlagModel]:
        self.ensure_defaults()
        return list(self.session.query(FeatureFlagModel).order_by(FeatureFlagModel.key).all())

    def update(self, key: str, *, enabled: bool, description: str | None, updated_by_user_id: str | None) -> FeatureFlagModel:
        self.ensure_defaults()
        row = self.session.get(FeatureFlagModel, key)
        if row is None:
            row = FeatureFlagModel(key=key)
            self.session.add(row)
        row.enabled = enabled
        if description is not None:
            row.description = description
        row.updated_by_user_id = updated_by_user_id
        row.updated_at = utc_now()
        self.session.commit()
        self.session.refresh(row)
        return row

