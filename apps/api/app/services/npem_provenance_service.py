from app.services.npem_scoring_service import NpemScoringService


class NpemProvenanceService:
    def __init__(self, session):
        self.session = session

    def provenance(self, province: str, group: str, year: int) -> list[dict]:
        scoring = NpemScoringService(self.session)
        rows = [row for row in scoring.rows(province, year, "baseline") if row.group_code == group]
        if not rows:
            return []
        return [
            {
                "provenance_id": row.provenance_id,
                "source_system": row.source_system,
                "source_series_id": row.source_series_id,
                "citation_text": row.citation_text,
                "release_date": row.release_date.isoformat() if row.release_date else None,
                "access_date": row.access_date.isoformat() if row.access_date else None,
                "transform_step": row.transform_step,
                "licence_note": row.licence_note,
                "source_url": row.source_url,
                "source_hash": row.source_hash,
            }
            for row in scoring.provenance_for(rows[0].score_id)
        ]
