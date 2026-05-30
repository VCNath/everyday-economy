from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Everyday Economy API"
    environment: str = "development"
    allow_demo_auth: bool = True
    database_url: str = "postgresql+psycopg://economy:economy@localhost:5432/economy"
    create_tables_on_startup: bool = False
    redis_url: str = "redis://localhost:6379/0"
    statcan_base_url: str = "https://www150.statcan.gc.ca"
    bank_of_canada_base_url: str = "https://www.bankofcanada.ca/valet"
    world_bank_base_url: str = "https://api.worldbank.org/v2"
    oecd_base_url: str = "https://sdmx.oecd.org/public/rest"
    cmhc_base_url: str = "https://www.cmhc-schl.gc.ca"
    api_base_url: str = "http://localhost:8000"
    frontend_url: str = "http://localhost:3000"
    supabase_url: str | None = None
    supabase_jwt_secret: str | None = None
    supabase_jwks_url: str | None = None
    supabase_audience: str | None = "authenticated"
    supabase_issuer: str | None = None
    supabase_service_role_key: str | None = None
    email_provider: str = "disabled"
    email_from: str | None = None
    resend_api_key: str | None = None
    sendgrid_api_key: str | None = None
    postmark_api_key: str | None = None
    store_raw_payloads: bool = False
    log_level: str = "info"
    cache_ttl_map_seconds: int = 21600
    cache_ttl_leaderboard_seconds: int = 21600
    cache_ttl_region_summary_seconds: int = 3600
    cache_ttl_source_status_seconds: int = 900
    allowed_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    rate_limit_enabled: bool = True
    rate_limit_requests_per_minute: int = 120

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def is_production(self) -> bool:
        return self.environment.lower() in {"production", "prod"}

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
