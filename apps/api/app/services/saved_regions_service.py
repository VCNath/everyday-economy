from fastapi import HTTPException
from sqlalchemy import select

from app.models.economic import LocationModel, SavedRegionModel


class SavedRegionsService:
    def __init__(self, session):
        self.session = session

    def list(self, user_id: str) -> list[SavedRegionModel]:
        return list(
            self.session.scalars(
                select(SavedRegionModel).where(SavedRegionModel.user_id == user_id).order_by(SavedRegionModel.created_at.desc())
            )
        )

    def save(self, user_id: str, location_id: str, label: str | None = None) -> SavedRegionModel:
        location = self.session.get(LocationModel, location_id)
        if location is None:
            raise HTTPException(status_code=400, detail="Invalid location_id.")
        existing = self.session.get(SavedRegionModel, {"user_id": user_id, "location_id": location_id})
        if existing is not None:
            if label is not None:
                existing.label = label
                self.session.commit()
                self.session.refresh(existing)
            return existing
        row = SavedRegionModel(user_id=user_id, location_id=location_id, label=label)
        self.session.add(row)
        self.session.commit()
        self.session.refresh(row)
        return row

    def remove(self, user_id: str, location_id: str) -> bool:
        existing = self.session.get(SavedRegionModel, {"user_id": user_id, "location_id": location_id})
        if existing is None:
            return False
        self.session.delete(existing)
        self.session.commit()
        return True

