def clamp_score(score: float) -> float:
    return max(0, min(100, score))


def calculate_affordability_score(components: dict[str, float], weights: dict[str, float]) -> float:
    score = 100
    for key, value in components.items():
        score -= value * weights.get(key, 0)
    return clamp_score(score)


def minmax_normalize(value: float, values: list[float]) -> float:
    if not values:
        return 0
    minimum = min(values)
    maximum = max(values)
    if maximum == minimum:
        return 0
    return (value - minimum) / (maximum - minimum)


def calculate_affordability_score_v1(region_values: dict[str, float], peer_values: dict[str, list[float]]) -> float:
    """Estimate a 0-100 household pressure score.

    This v1 composite is deliberately simple: lower CPI, food, shelter, fuel,
    unemployment, and basket values improve the score. It is a directional
    dashboard signal, not a formal affordability index.
    """

    weights = {
        "cpi_all_items_yoy": 20,
        "cpi_food_yoy": 20,
        "cpi_shelter_yoy": 20,
        "gas_regular_cents_litre": 15,
        "unemployment_rate": 15,
        "basic_basket_monthly_cost": 10,
    }
    penalty = 0.0
    for indicator_id, weight in weights.items():
        value = region_values.get(indicator_id)
        if value is None:
            continue
        penalty += minmax_normalize(value, peer_values.get(indicator_id, [])) * weight
    return round(clamp_score(100 - penalty), 1)
