from fastapi import APIRouter, Depends, Query

from app.api.deps import get_dashboard_service
from app.schemas.dashboard import MapResponse
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/map", tags=["map"])


@router.get("", response_model=MapResponse)
def get_map(
    indicator: str = Query(default="cpi_food_yoy"),
    geography_level: str = Query(default="province"),
    date: str = Query(default="latest"),
    calculation: str = Query(default="value"),
    service: DashboardService = Depends(get_dashboard_service),
):
    return service.get_map(indicator=indicator, geography_level=geography_level, calculation=calculation)
