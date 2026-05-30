from app.schemas.freshness import MetricTrustMetadata
from app.services.dashboard_service import DashboardService
from app.services.saved_regions_service import SavedRegionsService


class WatchlistService:
    def __init__(self, session):
        self.session = session
        self.saved_regions = SavedRegionsService(session)
        self.dashboard = DashboardService(session)

    def list_watchlist(self, user_id: str) -> list[dict]:
        rows = self.saved_regions.list(user_id)
        statuses = self.dashboard.source_status().sources
        freshness_status = statuses[0].status if statuses else "partial"
        latest_period = statuses[0].latest_period if statuses else None
        last_checked = statuses[0].last_checked if statuses else None
        items: list[dict] = []
        for row in rows:
            location = self.dashboard.get_location(row.location_id)
            if not location:
                continue
            summary = self.dashboard.get_region_summary(row.location_id)
            metrics = summary.metrics if summary else {}
            items.append(
                {
                    "location_id": row.location_id,
                    "name": location["name"],
                    "label": row.label,
                    "saved_at": row.created_at.isoformat(),
                    "summary": {
                        "cpi_yoy": float(metrics.get("cpi_all_items_yoy", 0)),
                        "food_cpi_yoy": float(metrics.get("cpi_food_yoy", 0)),
                        "gas_price_cents_litre": float(metrics.get("gas_regular_cents_litre", 0)),
                        "unemployment_rate": float(metrics.get("unemployment_rate", 0)),
                        "basic_basket_monthly_cost": float(metrics.get("basic_basket_monthly_cost", 0)),
                        "affordability_score": float(metrics.get("affordability_score", 0)),
                    },
                    "freshness": MetricTrustMetadata(
                        source_id="statcan",
                        source_name="Statistics Canada",
                        latest_period=latest_period,
                        last_checked=last_checked,
                        freshness_status=freshness_status,
                        is_estimated=False,
                        is_cached=False,
                    ),
                }
            )
        return items

