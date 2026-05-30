from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import admin, alerts, api_status, basket, compare, feedback, health, indicators, leaderboard, locations, map, me, npem, regions
from app.config import get_settings
from app.database import init_db
from app.middleware import InMemoryRateLimitMiddleware

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.create_tables_on_startup:
        init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Backend data refinery for map-first cost-of-living signals.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if settings.rate_limit_enabled:
    app.add_middleware(
        InMemoryRateLimitMiddleware,
        requests_per_minute=settings.rate_limit_requests_per_minute,
    )

app.include_router(health.router)
app.include_router(locations.router)
app.include_router(indicators.router)
app.include_router(map.router)
app.include_router(regions.router)
app.include_router(leaderboard.router)
app.include_router(basket.router)
app.include_router(compare.router)
app.include_router(api_status.router)
app.include_router(me.router)
app.include_router(alerts.router)
app.include_router(alerts.admin_router)
app.include_router(admin.router)
app.include_router(npem.router)
app.include_router(feedback.router)
app.include_router(feedback.admin_router)
