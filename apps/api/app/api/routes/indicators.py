from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_dashboard_service
from app.schemas.indicators import Indicator
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/indicators", tags=["indicators"])


@router.get("", response_model=list[Indicator])
def list_indicators(service: DashboardService = Depends(get_dashboard_service)):
    return service.list_indicators()


@router.get("/categories")
def indicator_categories(service: DashboardService = Depends(get_dashboard_service)):
    categories = set()
    for indicator in service.list_indicators():
        categories.add(indicator["category"] if isinstance(indicator, dict) else indicator.category)
    return sorted(categories)


@router.get("/{indicator_id}", response_model=Indicator)
def get_indicator(indicator_id: str, service: DashboardService = Depends(get_dashboard_service)):
    indicator = service.get_indicator(indicator_id)
    if indicator is None:
        raise HTTPException(status_code=404, detail="Indicator not found")
    return indicator
