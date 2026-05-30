def calculate_mom(current_value: float | None, previous_month_value: float | None) -> float | None:
    if current_value is None or previous_month_value in (None, 0):
        return None
    return ((current_value - previous_month_value) / previous_month_value) * 100
