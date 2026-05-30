from app.models.economic import NotificationPreferenceModel, utc_now


class NotificationPreferencesService:
    def __init__(self, session):
        self.session = session

    def get_or_create(self, user_id: str) -> NotificationPreferenceModel:
        pref = self.session.get(NotificationPreferenceModel, user_id)
        if pref is None:
            pref = NotificationPreferenceModel(user_id=user_id)
            self.session.add(pref)
            self.session.commit()
            self.session.refresh(pref)
        return pref

    def update(self, user_id: str, payload: dict) -> NotificationPreferenceModel:
        pref = self.get_or_create(user_id)
        for key in (
            "in_app_enabled",
            "email_enabled",
            "monthly_report_enabled",
            "data_release_alerts_enabled",
            "source_health_alerts_enabled",
        ):
            if key in payload and payload[key] is not None:
                setattr(pref, key, payload[key])
        pref.updated_at = utc_now()
        self.session.commit()
        self.session.refresh(pref)
        return pref

