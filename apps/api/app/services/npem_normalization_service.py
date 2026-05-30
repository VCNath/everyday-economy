from app.npem.variable_dictionary import COMPONENTS


class NpemNormalizationService:
    def percentile(self, values: list[float], percentile: float) -> float:
        if not values:
            return 0
        ordered = sorted(values)
        if len(ordered) == 1:
            return ordered[0]
        position = (len(ordered) - 1) * percentile
        lower = int(position)
        upper = min(lower + 1, len(ordered) - 1)
        fraction = position - lower
        return ordered[lower] + ((ordered[upper] - ordered[lower]) * fraction)

    def normalize(self, value: float, p5: float, p95: float, direction: str) -> float:
        if p95 == p5:
            return 50.0
        x_w = min(max(value, p5), p95)
        if direction == "benefit":
            score = 100 * (x_w - p5) / (p95 - p5)
        else:
            score = 100 * (p95 - x_w) / (p95 - p5)
        return round(max(0, min(100, score)), 2)

    def normalize_component_values(self, component_code: str, values: dict[tuple[str, str], float]) -> dict[tuple[str, str], dict[str, float | bool]]:
        direction = COMPONENTS[component_code]["direction"]
        p5 = self.percentile(list(values.values()), 0.05)
        p95 = self.percentile(list(values.values()), 0.95)
        return {
            key: {
                "raw_value": value,
                "winsor_p5": p5,
                "winsor_p95": p95,
                "normalized_score": self.normalize(value, p5, p95, direction),
                "inversion_applied": direction == "burden",
            }
            for key, value in values.items()
        }
