from fastapi import APIRouter, Depends, Query

from app.api.deps import get_dashboard_service
from app.schemas.dashboard import LeaderboardResponse
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/leaderboards", tags=["leaderboards"])


@router.get("", response_model=LeaderboardResponse)
def default_leaderboard(
    type: str = Query(default="grocery_basket"),
    geography_level: str = Query(default="province"),
    period: str = Query(default="latest"),
    sort: str = Query(default="desc"),
    limit: int = Query(default=10, ge=1, le=50),
    service: DashboardService = Depends(get_dashboard_service),
):
    return service.get_leaderboard(type, geography_level, limit)


@router.get("/{leaderboard_type}", response_model=LeaderboardResponse)
def get_leaderboard(
    leaderboard_type: str,
    geography_level: str = Query(default="province"),
    limit: int = Query(default=10, ge=1, le=50),
    service: DashboardService = Depends(get_dashboard_service),
):
    return service.get_leaderboard(leaderboard_type, geography_level, limit)
