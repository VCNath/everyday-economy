from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.deps import get_dashboard_service
from app.schemas.locations import Location
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/locations", tags=["locations"])


@router.get("", response_model=list[Location])
def list_locations(
    geography_level: str | None = Query(default=None),
    service: DashboardService = Depends(get_dashboard_service),
):
    return service.list_locations(geography_level)


@router.get("/search", response_model=list[Location])
def search_locations(q: str, service: DashboardService = Depends(get_dashboard_service)):
    return service.search_locations(q)


@router.get("/{location_id}", response_model=Location)
def get_location(location_id: str, service: DashboardService = Depends(get_dashboard_service)):
    location = service.get_location(location_id)
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


@router.get("/{location_id}/geometry")
def get_location_geometry(location_id: str, service: DashboardService = Depends(get_dashboard_service)):
    location = service.get_location(location_id)
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return {"location_id": location_id, "geometry_ref": location_id}
