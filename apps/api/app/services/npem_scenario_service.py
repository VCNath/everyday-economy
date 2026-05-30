from app.models.economic import NpemScenarioModel, NpemScenarioWeightModel, utc_now
from app.npem.variable_dictionary import MODEL_VERSION, SCENARIOS


class NpemScenarioService:
    def __init__(self, session):
        self.session = session

    def validate_weights(self, weights: dict[str, float]) -> bool:
        return abs(sum(weights.values()) - 1.0) <= 0.0001

    def seed_defaults(self) -> None:
        for code, payload in SCENARIOS.items():
            if not self.validate_weights(payload["weights"]):
                raise ValueError(f"N.P.E.M. scenario weights must sum to 1.00: {code}")
            scenario = self.session.get(NpemScenarioModel, code) or NpemScenarioModel(scenario_code=code)
            scenario.label = payload["label"]
            scenario.description = payload["description"]
            scenario.enabled = True
            scenario.model_version = MODEL_VERSION
            scenario.updated_at = utc_now()
            self.session.merge(scenario)
            for component_code, weight in payload["weights"].items():
                row = (
                    self.session.query(NpemScenarioWeightModel)
                    .filter_by(scenario_code=code, component_code=component_code)
                    .one_or_none()
                ) or NpemScenarioWeightModel(scenario_code=code, component_code=component_code)
                row.weight = weight
                self.session.merge(row)
        self.session.commit()

    def list(self) -> list[NpemScenarioModel]:
        self.seed_defaults()
        return list(self.session.query(NpemScenarioModel).order_by(NpemScenarioModel.scenario_code).all())

    def weights(self, scenario_code: str) -> dict[str, float]:
        self.seed_defaults()
        return {
            row.component_code: float(row.weight)
            for row in self.session.query(NpemScenarioWeightModel).filter_by(scenario_code=scenario_code).all()
        }
