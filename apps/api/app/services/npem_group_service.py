from app.models.economic import NpemGroupMetadataModel, utc_now
from app.npem.variable_dictionary import GROUPS


class NpemGroupService:
    def __init__(self, session):
        self.session = session

    def seed_defaults(self) -> None:
        for payload in GROUPS:
            group = self.session.get(NpemGroupMetadataModel, payload["group_code"]) or NpemGroupMetadataModel(group_code=payload["group_code"])
            for key, value in payload.items():
                setattr(group, key, value)
            group.updated_at = utc_now()
            self.session.merge(group)
        self.session.commit()

    def list(self, include_disabled: bool = False) -> list[NpemGroupMetadataModel]:
        self.seed_defaults()
        query = self.session.query(NpemGroupMetadataModel)
        if not include_disabled:
            query = query.filter(NpemGroupMetadataModel.enabled.is_(True))
        return list(query.order_by(NpemGroupMetadataModel.selection_priority).all())

    def select_groups(self, province: str, year: int) -> dict:
        groups = self.list()
        is_territory = province in {"YT", "NT", "NU", "CA-YT", "CA-NT", "CA-NU"}
        threshold = 0.03 if is_territory else 0.05
        selected = [g for g in groups if g.group_layer == "core"][:4]
        overlays = [g for g in groups if g.group_layer == "overlay"][:2]
        return {
            "province": province,
            "year": year,
            "threshold": threshold,
            "selected_groups": [
                {
                    "group_code": g.group_code,
                    "group_label": g.group_label,
                    "group_layer": g.group_layer,
                    "overlap_warning": "overlapping cohort" if g.group_layer == "overlay" else None,
                    "selection_reason": "core headline group" if g.group_layer == "core" else "eligible overlay cohort",
                }
                for g in [*selected, *overlays]
            ],
            "warnings": ["Overlay cohorts may overlap and are not mutually exclusive."],
        }
