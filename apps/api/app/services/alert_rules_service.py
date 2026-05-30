from fastapi import HTTPException
from sqlalchemy import select

from app.models.economic import AlertRuleModel, IndicatorModel, LocationModel, utc_now

VALID_OPERATORS = {"gt", "gte", "lt", "lte", "eq", "change_gt", "change_gte", "rank_below", "rank_above"}


class AlertRulesService:
    def __init__(self, session):
        self.session = session

    def _validate(self, payload: dict) -> None:
        if payload.get("comparison_operator") and payload["comparison_operator"] not in VALID_OPERATORS:
            raise HTTPException(status_code=400, detail="Invalid comparison_operator.")
        if payload.get("location_id"):
            if self.session.get(LocationModel, payload["location_id"]) is None:
                raise HTTPException(status_code=400, detail="Invalid location_id.")
        if payload.get("indicator_id"):
            if self.session.get(IndicatorModel, payload["indicator_id"]) is None:
                raise HTTPException(status_code=400, detail="Invalid indicator_id.")

    def list(self, user_id: str) -> list[AlertRuleModel]:
        return list(self.session.scalars(select(AlertRuleModel).where(AlertRuleModel.user_id == user_id).order_by(AlertRuleModel.created_at.desc())))

    def get(self, user_id: str, alert_id: str) -> AlertRuleModel | None:
        row = self.session.get(AlertRuleModel, alert_id)
        if row is None or row.user_id != user_id:
            return None
        return row

    def create(self, user_id: str, payload: dict) -> AlertRuleModel:
        self._validate(payload)
        if payload.get("comparison_operator") in {"gt", "gte", "lt", "lte", "eq"} and payload.get("threshold_value") is None:
            raise HTTPException(status_code=400, detail="threshold_value is required.")
        row = AlertRuleModel(user_id=user_id, **payload)
        self.session.add(row)
        self.session.commit()
        self.session.refresh(row)
        return row

    def update(self, user_id: str, alert_id: str, payload: dict) -> AlertRuleModel | None:
        row = self.get(user_id, alert_id)
        if row is None:
            return None
        self._validate(payload)
        for key, value in payload.items():
            setattr(row, key, value)
        row.updated_at = utc_now()
        self.session.commit()
        self.session.refresh(row)
        return row

    def delete(self, user_id: str, alert_id: str) -> bool:
        row = self.get(user_id, alert_id)
        if row is None:
            return False
        self.session.delete(row)
        self.session.commit()
        return True

    def set_enabled(self, user_id: str, alert_id: str, enabled: bool) -> bool:
        row = self.get(user_id, alert_id)
        if row is None:
            return False
        row.enabled = enabled
        row.updated_at = utc_now()
        self.session.commit()
        return True

