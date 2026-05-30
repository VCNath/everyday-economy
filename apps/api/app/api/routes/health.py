from fastapi import APIRouter, Depends

from app.config import get_settings
from app.api.deps import get_dashboard_service
from app.services.dashboard_service import DashboardService
from app.database import SessionLocal
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import redis

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    return {"status": "ok", "service": get_settings().app_name}


@router.get("/health/db")
def health_db():
    try:
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))
        return {"status": "healthy"}
    except SQLAlchemyError as exc:
        return {"status": "error", "message": str(exc)}


@router.get("/health/cache")
def health_cache():
    try:
        client = redis.Redis.from_url(get_settings().redis_url, socket_connect_timeout=1)
        client.ping()
        return {"status": "healthy"}
    except redis.RedisError as exc:
        return {"status": "error", "message": str(exc)}


@router.get("/health/sources")
def health_sources(service: DashboardService = Depends(get_dashboard_service)):
    return service.source_status()
