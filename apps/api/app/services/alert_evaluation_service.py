from datetime import datetime

from sqlalchemy import select

from app.models.economic import AlertRuleModel, ObservationCalculationModel, ObservationModel, utc_now
from app.services.notification_preferences_service import NotificationPreferencesService
from app.services.notification_service import NotificationService


class AlertEvaluationService:
    def __init__(self, session):
        self.session = session
        self.notifications = NotificationService(session)
        self.pref_service = NotificationPreferencesService(session)

    def _latest_observation(self, indicator_id: str, location_id: str) -> ObservationModel | None:
        return self.session.scalar(
            select(ObservationModel)
            .where(ObservationModel.indicator_id == indicator_id, ObservationModel.location_id == location_id)
            .order_by(ObservationModel.period.desc())
            .limit(1)
        )

    def _operator_match(self, op: str, value: float, threshold: float | None, change: float | None, rank: int | None, mom: float | None) -> bool:
        if op == "gt":
            return threshold is not None and value > threshold
        if op == "gte":
            return threshold is not None and value >= threshold
        if op == "lt":
            return threshold is not None and value < threshold
        if op == "lte":
            return threshold is not None and value <= threshold
        if op == "eq":
            return threshold is not None and value == threshold
        if op == "change_gt":
            return change is not None and mom is not None and mom > change
        if op == "change_gte":
            return change is not None and mom is not None and mom >= change
        if op in {"rank_below", "rank_above"}:
            # Rank evaluation can be added against snapshots; keep no-op for now.
            return False
        return False

    def evaluate(self) -> dict[str, int]:
        rows = list(self.session.scalars(select(AlertRuleModel).where(AlertRuleModel.enabled.is_(True))))
        evaluated = 0
        triggered = 0
        for rule in rows:
            evaluated += 1
            obs = self._latest_observation(rule.indicator_id, rule.location_id)
            if obs is None or obs.value is None:
                continue
            calc = self.session.scalar(select(ObservationCalculationModel).where(ObservationCalculationModel.observation_id == obs.id))
            mom = float(calc.mom_change) if calc and calc.mom_change is not None else None
            value = float(obs.value)
            match = self._operator_match(rule.comparison_operator, value, float(rule.threshold_value) if rule.threshold_value is not None else None, float(rule.change_value) if rule.change_value is not None else None, rule.rank_value, mom)
            if not match:
                continue
            if rule.last_triggered_at and rule.last_triggered_at.date() == utc_now().date():
                continue
            prefs = self.pref_service.get_or_create(rule.user_id)
            if prefs.in_app_enabled and rule.channel_in_app:
                self.notifications.create(
                    user_id=rule.user_id,
                    alert_rule_id=rule.id,
                    location_id=rule.location_id,
                    indicator_id=rule.indicator_id,
                    type="alert",
                    severity="warning",
                    title="Alert triggered",
                    message=f"{rule.indicator_id} in {rule.location_id} is {value:.2f}, crossing your configured threshold.",
                    value=value,
                    threshold_value=float(rule.threshold_value) if rule.threshold_value is not None else None,
                    period=obs.period,
                    source_id=obs.source_id,
                    freshness_status="healthy",
                )
                triggered += 1
            rule.last_triggered_at = utc_now()
            rule.updated_at = utc_now()
        self.session.commit()
        return {"evaluated": evaluated, "triggered": triggered}

