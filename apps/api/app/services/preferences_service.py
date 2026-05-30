from fastapi import HTTPException
from sqlalchemy import select

from app.models.economic import LocationModel, UserPreferenceModel, utc_now


class PreferencesService:
    def __init__(self, session):
        self.session = session

    def get_or_create(self, user_id: str) -> UserPreferenceModel:
        preference = self.session.get(UserPreferenceModel, user_id)
        if preference is None:
            preference = UserPreferenceModel(user_id=user_id)
            self.session.add(preference)
            self.session.commit()
            self.session.refresh(preference)
        return preference

    def update(self, user_id: str, payload: dict) -> UserPreferenceModel:
        preference = self.get_or_create(user_id)
        default_location_id = payload.get("default_location_id")
        if default_location_id is not None:
            location_exists = self.session.scalar(
                select(LocationModel.id).where(LocationModel.id == default_location_id)
            )
            if not location_exists:
                raise HTTPException(status_code=400, detail="Invalid default_location_id.")
            preference.default_location_id = default_location_id

        for key in ("default_metric", "default_period", "default_basket_id", "theme", "data_density"):
            if key in payload and payload[key] is not None:
                setattr(preference, key, payload[key])
        if payload.get("household_size") is not None:
            preference.household_size = int(payload["household_size"])
        preference.updated_at = utc_now()
        self.session.commit()
        self.session.refresh(preference)
        return preference
