import csv
import io
import logging
import re
import zipfile
from collections.abc import Iterable
from dataclasses import dataclass

import httpx

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class StatCanTable:
    table_id: str
    product_id: str
    filename: str


class StatCanConnector:
    """Statistics Canada bulk CSV connector.

    The public WDS helper can be used to discover download URLs, but the stable
    bulk CSV route is simple and cacheable:
    https://www150.statcan.gc.ca/n1/tbl/csv/{product_id}-eng.zip
    """

    tables = {
        "cpi": StatCanTable("18-10-0004-01", "18100004", "18100004.csv"),
        "food_prices": StatCanTable("18-10-0245-01", "18100245", "18100245.csv"),
        "gas": StatCanTable("18-10-0001-01", "18100001", "18100001.csv"),
        "labour": StatCanTable("14-10-0287-01", "14100287", "14100287.csv"),
    }

    def __init__(self, base_url: str = "https://www150.statcan.gc.ca", timeout: float = 60.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def download_url(self, table: StatCanTable) -> str:
        return f"{self.base_url}/n1/tbl/csv/{table.product_id}-eng.zip"

    def fetch_table_zip(self, table_key: str) -> bytes:
        table = self.tables[table_key]
        try:
            response = httpx.get(self.download_url(table), timeout=self.timeout, follow_redirects=True)
            response.raise_for_status()
            return response.content
        except httpx.HTTPStatusError as exc:
            logger.error("Statistics Canada table %s returned HTTP %s", table.table_id, exc.response.status_code)
            raise
        except httpx.RequestError:
            logger.exception("Statistics Canada table %s request failed", table.table_id)
            raise

    def fetch_table_metadata(self, table_key: str) -> dict[str, str]:
        table = self.tables[table_key]
        return {
            "source": "statcan",
            "table_id": table.table_id,
            "product_id": table.product_id,
            "download_url": self.download_url(table),
        }

    def iter_rows_from_zip_bytes(self, content: bytes, table_key: str) -> Iterable[dict[str, str]]:
        table = self.tables[table_key]
        try:
            with zipfile.ZipFile(io.BytesIO(content)) as archive:
                with archive.open(table.filename) as raw:
                    text = io.TextIOWrapper(raw, encoding="utf-8-sig", newline="")
                    yield from csv.DictReader(text)
        except (KeyError, zipfile.BadZipFile):
            logger.exception("Statistics Canada table %s bulk ZIP could not be parsed", table.table_id)
            raise

    def iter_table_rows(self, table_key: str) -> Iterable[dict[str, str]]:
        yield from self.iter_rows_from_zip_bytes(self.fetch_table_zip(table_key), table_key)


def statcan_product_id(table_id: str) -> str:
    return re.sub(r"[^0-9]", "", table_id)[:8]
