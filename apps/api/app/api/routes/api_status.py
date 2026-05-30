from fastapi import APIRouter, Depends

from app.api.deps import get_dashboard_service
from app.schemas.dashboard import SourceStatusResponse
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/source-status", tags=["source status"])


@router.get("", response_model=SourceStatusResponse)
def source_status(service: DashboardService = Depends(get_dashboard_service)):
    return service.source_status()


@router.get("/runs")
def source_runs(service: DashboardService = Depends(get_dashboard_service)):
    return service.source_run_status()


@router.get("/quality")
def data_quality(service: DashboardService = Depends(get_dashboard_service)):
    return service.data_quality_summary()
