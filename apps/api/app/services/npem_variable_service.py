from app.models.economic import NpemVariableModel, utc_now
from app.npem.variable_dictionary import VARIABLES


class NpemVariableService:
    def __init__(self, session):
        self.session = session

    def seed_defaults(self) -> None:
        for row in VARIABLES:
            variable = self.session.get(NpemVariableModel, row[0]) or NpemVariableModel(variable_code=row[0])
            (
                variable.variable_code,
                variable.label,
                variable.definition,
                variable.unit_code,
                variable.preferred_source,
                variable.fallback_source,
                variable.expected_year,
                variable.metric_family,
                variable.requires_nowcast,
                variable.proxy_allowed,
                variable.notes,
            ) = row
            variable.updated_at = utc_now()
            self.session.merge(variable)
        self.session.commit()

    def list(self) -> list[NpemVariableModel]:
        self.seed_defaults()
        return list(self.session.query(NpemVariableModel).order_by(NpemVariableModel.variable_code).all())
