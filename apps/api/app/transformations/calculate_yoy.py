def calculate_yoy(current_value: float | None, prior_year_value: float | None) -> float | None:
    if current_value is None or prior_year_value in (None, 0):
        return None
    return ((current_value - prior_year_value) / prior_year_value) * 100
