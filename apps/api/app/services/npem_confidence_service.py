class NpemConfidenceService:
    def score(
        self,
        *,
        coverage: float,
        recency: float,
        directness: float,
        reliability: float,
        suppression_penalty: float = 0.0,
    ) -> float:
        raw = 100 * (0.40 * coverage + 0.25 * recency + 0.20 * directness + 0.15 * reliability)
        return round(max(0, min(100, raw - (suppression_penalty * 100))), 2)

    def grade(self, score: float) -> str:
        if score >= 85:
            return "A"
        if score >= 70:
            return "B"
        if score >= 55:
            return "C"
        if score >= 40:
            return "D"
        return "E"

    def label(self, grade: str) -> str:
        return {
            "A": "High confidence",
            "B": "Good confidence",
            "C": "Moderate confidence",
            "D": "Low confidence",
            "E": "Experimental",
        }.get(grade, "Unknown confidence")
