from dataclasses import dataclass
from datetime import date

from dateutil.relativedelta import relativedelta
from fastapi import HTTPException


WINDOW_MONTHS = {
    "3m": 3,
    "6m": 6,
    "12m": 12,
    "24m": 24,
    "5y": 60,
}


@dataclass(frozen=True)
class TimeWindow:
    window: str
    start_period: date | None
    end_period: date | None


def parse_period(value: str) -> date:
    try:
        if len(value) == 7:
            return date.fromisoformat(f"{value}-01")
        return date.fromisoformat(value)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"Invalid period '{value}'. Expected YYYY-MM or YYYY-MM-DD.") from exc


def resolve_time_window(
    *,
    latest_period: date | None,
    start_period: str | None,
    end_period: str | None,
    window: str | None,
    default_window: str = "12m",
) -> TimeWindow:
    if start_period and end_period:
        start = parse_period(start_period)
        end = parse_period(end_period)
        if start > end:
            raise HTTPException(status_code=400, detail="start_period must be less than or equal to end_period.")
        return TimeWindow(window=window or "custom", start_period=start, end_period=end)

    resolved_window = window or default_window
    if resolved_window == "all":
        return TimeWindow(window="all", start_period=None, end_period=latest_period)
    if resolved_window not in WINDOW_MONTHS:
        raise HTTPException(status_code=400, detail=f"Invalid window '{resolved_window}'. Use 3m, 6m, 12m, 24m, 5y, or all.")
    if latest_period is None:
        return TimeWindow(window=resolved_window, start_period=None, end_period=None)

    months = WINDOW_MONTHS[resolved_window]
    return TimeWindow(
        window=resolved_window,
        start_period=latest_period - relativedelta(months=months - 1),
        end_period=latest_period,
    )
