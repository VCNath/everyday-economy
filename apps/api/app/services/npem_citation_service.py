from app.services.npem_provenance_service import NpemProvenanceService


class NpemCitationService:
    def __init__(self, session):
        self.session = session

    def citations(self, province: str, group: str, year: int) -> list[dict]:
        return [
            {
                "citation_text": row["citation_text"],
                "source_url": row["source_url"],
                "source_system": row["source_system"],
                "licence_note": row["licence_note"],
            }
            for row in NpemProvenanceService(self.session).provenance(province, group, year)
        ]
