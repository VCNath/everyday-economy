from fastapi import APIRouter, Depends

from app.api.deps import get_dashboard_service
from app.schemas.dashboard import BasketCalculationRequest, BasketCalculationResponse
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/basket", tags=["basket"])


@router.get("/default", response_model=BasketCalculationResponse)
def default_basket(service: DashboardService = Depends(get_dashboard_service)):
    return service.default_basket()


@router.post("/calculate", response_model=BasketCalculationResponse)
def calculate_basket(
    request: BasketCalculationRequest,
    service: DashboardService = Depends(get_dashboard_service),
):
    return service.calculate_basket(request)


@router.get("/{basket_type}/by-region")
def basket_by_region(basket_type: str, service: DashboardService = Depends(get_dashboard_service)):
    leaderboard = service.get_leaderboard("grocery_basket")
    return {"basket_type": basket_type, "period": leaderboard.period, "regions": leaderboard.rows}
