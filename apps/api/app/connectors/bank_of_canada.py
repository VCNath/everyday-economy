from dataclasses import dataclass
from datetime import date
import logging

import httpx

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ValetObservation:
    series_id: str
    period: date
    value: float


class BankOfCanadaConnector:
    """Bank of Canada Valet API connector."""

    def __init__(self, base_url: str = "https://www.bankofcanada.ca/valet", timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def recent_observations(self, series_id: str, recent: int = 30) -> list[ValetObservation]:
        url = f"{self.base_url}/observations/{series_id}/json"
        try:
            response = httpx.get(url, params={"recent": recent}, timeout=self.timeout)
            response.raise_for_status()
            payload = response.json()
        except httpx.HTTPStatusError as exc:
            logger.error("Bank of Canada series %s returned HTTP %s", series_id, exc.response.status_code)
            raise
        except (httpx.RequestError, ValueError):
            logger.exception("Bank of Canada series %s request failed", series_id)
            raise
        observations = []
        for row in payload.get("observations", []):
            value = row.get(series_id, {}).get("v")
            if value is None:
                continue
            observations.append(
                ValetObservation(
                    series_id=series_id,
                    period=date.fromisoformat(row["d"]),
                    value=float(value),
                )
            )
        return observations
