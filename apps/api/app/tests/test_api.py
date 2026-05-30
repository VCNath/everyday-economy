from fastapi.testclient import TestClient
from pathlib import Path
from uuid import uuid4
from datetime import UTC, date, datetime, timedelta
import jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.deps import get_db
from app.config import get_settings
from app.database import Base
from app.models.economic import DataQualityFlagModel, DataSourceModel, IndicatorModel, LocationModel, ObservationModel
from app.main import app

client = TestClient(app)


def _auth_headers(email: str = "tester@example.com"):
    return {"Authorization": f"Bearer demo:{email}:Tester"}


def _admin_headers(email: str = "admin@example.com"):
    return {"Authorization": f"Bearer demo:{email}:Admin:admin"}


def _override_db():
    db_file = Path(f"/tmp/everyday-economy-test-{uuid4().hex}.db")
    engine = create_engine(f"sqlite:///{db_file}", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    db.add(LocationModel(id="CA-SK", name="Saskatchewan", country_code="CA", region_code="SK", geography_level="province"))
    db.add(DataSourceModel(id="statcan", name="Statistics Canada", provider="Statistics Canada"))
    db.add(IndicatorModel(id="cpi_food_yoy", name="Food inflation", category="prices", unit="%", frequency="monthly", source_id="statcan"))
    db.add(ObservationModel(indicator_id="cpi_food_yoy", location_id="CA-SK", period=date(2026, 4, 1), value=5.3, unit="%", source_id="statcan"))
    db.add(DataQualityFlagModel(flag_type="missing_value", severity="warning", message="test flag"))
    db.commit()

    def _get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = _get_db
    return db


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_locations_endpoint():
    response = client.get("/locations")
    assert response.status_code == 200
    assert any(row["id"] == "CA-SK" for row in response.json())


def test_indicators_endpoint_and_categories():
    response = client.get("/indicators")
    assert response.status_code == 200
    assert any(row["id"] == "cpi_food_yoy" for row in response.json())

    categories = client.get("/indicators/categories")
    assert categories.status_code == 200
    assert "prices" in categories.json()


def test_source_status_endpoint():
    response = client.get("/source-status")
    assert response.status_code == 200
    payload = response.json()
    assert "sources" in payload
    assert payload["sources"]


def test_map_endpoint_contract():
    db = _override_db()
    response = client.get("/map?indicator=cpi_food_yoy")
    assert response.status_code == 200
    payload = response.json()
    assert payload["indicator"] == "cpi_food_yoy"
    assert payload["features"]
    app.dependency_overrides.clear()
    db.close()


def test_region_series_contract():
    response = client.get("/regions/CA-SK/series?indicators=cpi_food_yoy&window=12m")
    assert response.status_code == 200
    payload = response.json()
    assert payload["location_id"] == "CA-SK"
    assert payload["series"]
    assert payload["series"][0]["points"]


def test_compare_endpoint_contract():
    response = client.get("/compare?location_ids=CA-SK,CA-AB,CA-MB&window=12m&include_series=true")
    assert response.status_code == 200
    payload = response.json()
    assert [location["location_id"] for location in payload["locations"]] == ["CA-SK", "CA-AB", "CA-MB"]
    assert payload["rows"]
    assert "window" in payload


def test_compare_unknown_indicator_returns_warning():
    response = client.get("/compare?location_ids=CA-SK&indicators=not_a_metric")
    assert response.status_code == 200
    payload = response.json()
    assert payload["warnings"]


def test_region_series_invalid_window_returns_400():
    response = client.get("/regions/CA-SK/series?indicators=cpi_food_yoy&window=99m")
    assert response.status_code == 400


def test_region_series_unknown_location_warning():
    response = client.get("/regions/CA-XX/series?indicators=cpi_food_yoy")
    assert response.status_code == 200
    payload = response.json()
    assert payload["warnings"]


def test_region_summary_contract():
    response = client.get("/regions/CA-SK/summary")
    assert response.status_code == 200
    payload = response.json()
    assert payload["name"] == "Saskatchewan"
    assert "cpi_food_yoy" in payload["metrics"]
    assert payload["insight"]


def test_leaderboard_rows_are_ranked():
    response = client.get("/leaderboards/grocery_basket?limit=5")
    assert response.status_code == 200
    rows = response.json()["rows"]
    assert len(rows) == 5
    assert rows[0]["rank"] == 1


def test_basket_endpoint():
    response = client.get("/basket/default")
    assert response.status_code == 200
    payload = response.json()
    assert payload["total_cost"] > 0
    assert payload["items"]


def test_yoy_missing_values():
    from app.transformations.calculate_yoy import calculate_yoy

    assert calculate_yoy(None, 100) is None
    assert calculate_yoy(100, 0) is None
    assert round(calculate_yoy(110, 100), 1) == 10.0


def test_mom_missing_values():
    from app.transformations.calculate_mom import calculate_mom

    assert calculate_mom(None, 100) is None
    assert calculate_mom(100, 0) is None
    assert round(calculate_mom(102, 100), 1) == 2.0


def test_me_requires_auth():
    response = client.get("/me")
    assert response.status_code == 401


def test_demo_auth_rejected_in_production():
    settings = get_settings()
    original_environment = settings.environment
    original_allow_demo = settings.allow_demo_auth
    settings.environment = "production"
    settings.allow_demo_auth = True
    try:
        response = client.get("/me", headers=_auth_headers())
        assert response.status_code == 401
    finally:
        settings.environment = original_environment
        settings.allow_demo_auth = original_allow_demo


def test_supabase_jwt_auth_syncs_user():
    db = _override_db()
    settings = get_settings()
    original_secret = settings.supabase_jwt_secret
    original_audience = settings.supabase_audience
    original_issuer = settings.supabase_issuer
    secret = "test-supabase-secret-at-least-32-bytes"
    settings.supabase_jwt_secret = secret
    settings.supabase_audience = "authenticated"
    settings.supabase_issuer = "https://example.supabase.co/auth/v1"
    token = jwt.encode(
        {
            "sub": str(uuid4()),
            "email": "supabase@example.com",
            "aud": "authenticated",
            "iss": settings.supabase_issuer,
            "exp": datetime.now(UTC) + timedelta(minutes=5),
            "user_metadata": {"display_name": "Supabase User"},
        },
        secret,
        algorithm="HS256",
    )
    try:
        response = client.get("/me", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        assert response.json()["email"] == "supabase@example.com"
        assert response.json()["role"] == "user"
    finally:
        settings.supabase_jwt_secret = original_secret
        settings.supabase_audience = original_audience
        settings.supabase_issuer = original_issuer
        app.dependency_overrides.clear()
        db.close()


def test_me_profile_and_preferences_flow():
    db = _override_db()
    response = client.get("/me", headers=_auth_headers())
    assert response.status_code == 200
    assert response.json()["email"] == "tester@example.com"

    pref = client.get("/me/preferences", headers=_auth_headers())
    assert pref.status_code == 200
    assert pref.json()["household_size"] == 1

    updated = client.put(
        "/me/preferences",
        headers=_auth_headers(),
        json={"default_location_id": "CA-SK", "default_metric": "cpi_food_yoy"},
    )
    assert updated.status_code == 200
    assert updated.json()["default_location_id"] == "CA-SK"
    app.dependency_overrides.clear()
    db.close()


def test_saved_regions_and_watchlist_flow():
    db = _override_db()
    saved = client.post("/me/saved-regions", headers=_auth_headers(), json={"location_id": "CA-SK", "label": "Home"})
    assert saved.status_code == 200
    assert saved.json()["location_id"] == "CA-SK"

    duplicate = client.post("/me/saved-regions", headers=_auth_headers(), json={"location_id": "CA-SK", "label": "Home"})
    assert duplicate.status_code == 200

    listing = client.get("/me/saved-regions", headers=_auth_headers())
    assert listing.status_code == 200
    assert len(listing.json()) == 1

    watchlist = client.get("/me/watchlist", headers=_auth_headers())
    assert watchlist.status_code == 200
    assert watchlist.json()[0]["freshness"]["freshness_status"]

    removed = client.delete("/me/saved-regions/CA-SK", headers=_auth_headers())
    assert removed.status_code == 200
    app.dependency_overrides.clear()
    db.close()


def test_alert_rules_crud_and_toggle():
    db = _override_db()
    created = client.post(
        "/me/alerts",
        headers=_auth_headers(),
        json={
            "location_id": "CA-SK",
            "indicator_id": "cpi_food_yoy",
            "alert_type": "threshold",
            "comparison_operator": "gte",
            "threshold_value": 5,
        },
    )
    assert created.status_code == 200
    alert_id = created.json()["id"]
    listing = client.get("/me/alerts", headers=_auth_headers())
    assert listing.status_code == 200
    assert listing.json()
    disabled = client.post(f"/me/alerts/{alert_id}/disable", headers=_auth_headers())
    assert disabled.status_code == 200
    enabled = client.post(f"/me/alerts/{alert_id}/enable", headers=_auth_headers())
    assert enabled.status_code == 200
    deleted = client.delete(f"/me/alerts/{alert_id}", headers=_auth_headers())
    assert deleted.status_code == 200
    app.dependency_overrides.clear()
    db.close()


def test_notifications_and_reports_flow():
    db = _override_db()
    client.post("/me/saved-regions", headers=_auth_headers(), json={"location_id": "CA-SK"})
    generated = client.post("/me/reports/generate?location_id=CA-SK", headers=_auth_headers())
    assert generated.status_code == 200
    reports = client.get("/me/reports", headers=_auth_headers())
    assert reports.status_code == 200
    assert reports.json()["items"]
    notifications = client.get("/me/notifications", headers=_auth_headers())
    assert notifications.status_code == 200
    report_note = notifications.json()["items"][0]["id"]
    marked = client.post(f"/me/notifications/{report_note}/read", headers=_auth_headers())
    assert marked.status_code == 200
    unread = client.get("/me/notifications/unread-count", headers=_auth_headers())
    assert unread.status_code == 200
    assert "count" in unread.json()
    app.dependency_overrides.clear()
    db.close()


def test_alert_evaluation_generates_notification_once():
    db = _override_db()
    client.post(
        "/me/alerts",
        headers=_auth_headers(),
        json={
            "location_id": "CA-SK",
            "indicator_id": "cpi_food_yoy",
            "alert_type": "threshold",
            "comparison_operator": "gte",
            "threshold_value": 5,
        },
    )
    first = client.post("/admin/evaluate-alerts", headers=_auth_headers("tester@admin.local"))
    assert first.status_code == 200
    second = client.post("/admin/evaluate-alerts", headers=_auth_headers("tester@admin.local"))
    assert second.status_code == 200
    notifications = client.get("/me/notifications", headers=_auth_headers())
    assert notifications.status_code == 200
    # One alert notification max per day for same rule
    alert_notifications = [n for n in notifications.json()["items"] if n["type"] == "alert"]
    assert len(alert_notifications) <= 1
    app.dependency_overrides.clear()
    db.close()


def test_admin_routes_require_auth_and_admin_role():
    db = _override_db()
    no_auth = client.get("/admin/summary")
    assert no_auth.status_code == 401
    non_admin = client.get("/admin/summary", headers=_auth_headers())
    assert non_admin.status_code == 403
    admin = client.get("/admin/summary", headers=_admin_headers())
    assert admin.status_code == 200
    app.dependency_overrides.clear()
    db.close()


def test_admin_job_trigger_and_reject_unknown_job():
    db = _override_db()
    rejected = client.post("/admin/jobs/refresh-source", headers=_admin_headers(), json={"job_name": "rm -rf"})
    assert rejected.status_code == 400
    triggered = client.post("/admin/jobs/evaluate-alerts", headers=_admin_headers())
    assert triggered.status_code == 200
    runs = client.get("/admin/job-runs", headers=_admin_headers())
    assert runs.status_code == 200
    assert runs.json()["items"]
    app.dependency_overrides.clear()
    db.close()


def test_admin_feature_flag_update_creates_audit_log():
    db = _override_db()
    flags = client.get("/admin/feature-flags", headers=_admin_headers())
    assert flags.status_code == 200
    updated = client.put("/admin/feature-flags/adminPanel", headers=_admin_headers(), json={"enabled": True})
    assert updated.status_code == 200
    logs = client.get("/admin/audit-logs", headers=_admin_headers())
    assert logs.status_code == 200
    assert any(row["action"] == "admin.feature_flag.update" for row in logs.json())
    app.dependency_overrides.clear()
    db.close()


def test_admin_data_quality_list_and_review():
    db = _override_db()
    flags = client.get("/admin/data-quality", headers=_admin_headers())
    assert flags.status_code == 200
    assert flags.json()["items"]
    flag_id = flags.json()["items"][0]["id"]
    reviewed = client.post(f"/admin/data-quality/{flag_id}/review", headers=_admin_headers())
    assert reviewed.status_code == 200
    assert reviewed.json()["reviewed_at"] is not None
    app.dependency_overrides.clear()
    db.close()


def test_email_service_disabled_and_console_modes():
    from app.services.email_service import EmailService

    settings = get_settings()
    original_provider = settings.email_provider
    settings.email_provider = "disabled"
    try:
        assert EmailService().send("test@example.com", "Subject", "Body") is False
        settings.email_provider = "console"
        assert EmailService().send("test@example.com", "Subject", "Body") is True
    finally:
        settings.email_provider = original_provider


def test_feedback_submit_anonymous_and_validation():
    db = _override_db()
    invalid = client.post("/feedback", json={"feedback_type": "bug", "message": "short"})
    assert invalid.status_code == 422
    response = client.post(
        "/feedback",
        json={
            "feedback_type": "data_issue",
            "page_path": "/regions/CA-SK",
            "rating": 4,
            "message": "The food inflation number looks different from the source panel.",
            "email": "beta@example.com",
            "metadata": {"region": "CA-SK", "indicator": "cpi_food_yoy", "secret": "should_not_store"},
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "new"
    assert payload["metadata"]["region"] == "CA-SK"
    assert "secret" not in payload["metadata"]
    app.dependency_overrides.clear()
    db.close()


def test_feedback_submit_logged_in_and_admin_review():
    db = _override_db()
    response = client.post(
        "/feedback",
        headers=_auth_headers(),
        json={"feedback_type": "bug", "page_path": "/dashboard", "message": "Dashboard card spacing looked broken on my phone."},
    )
    assert response.status_code == 200
    feedback_id = response.json()["id"]
    listed_no_auth = client.get("/admin/feedback")
    assert listed_no_auth.status_code == 401
    listed_user = client.get("/admin/feedback", headers=_auth_headers())
    assert listed_user.status_code == 403
    listed = client.get("/admin/feedback", headers=_admin_headers())
    assert listed.status_code == 200
    assert any(row["id"] == feedback_id for row in listed.json()["items"])
    updated = client.put(f"/admin/feedback/{feedback_id}", headers=_admin_headers(), json={"status": "reviewed"})
    assert updated.status_code == 200
    assert updated.json()["status"] == "reviewed"
    logs = client.get("/admin/audit-logs", headers=_admin_headers())
    assert any(row["action"] == "admin.feedback.update" for row in logs.json())
    app.dependency_overrides.clear()
    db.close()


def test_npem_normalization_and_confidence_logic():
    from app.services.npem_confidence_service import NpemConfidenceService
    from app.services.npem_normalization_service import NpemNormalizationService

    normalizer = NpemNormalizationService()
    assert normalizer.normalize(10, 0, 20, "benefit") == 50
    assert normalizer.normalize(10, 0, 20, "burden") == 50
    assert normalizer.normalize(10, 10, 10, "benefit") == 50

    confidence = NpemConfidenceService()
    assert confidence.grade(90) == "A"
    assert confidence.grade(72) == "B"
    assert confidence.grade(60) == "C"
    assert confidence.grade(45) == "D"
    assert confidence.grade(25) == "E"


def test_npem_endpoints_and_job():
    db = _override_db()
    groups = client.get("/npem/groups")
    assert groups.status_code == 200
    assert any(row["group_code"] == "YA_UC" for row in groups.json())

    scenarios = client.get("/npem/scenarios")
    assert scenarios.status_code == 200
    assert all(round(sum(row["weights"].values()), 2) == 1.0 for row in scenarios.json())

    scores = client.get("/npem?province=AB&year=2025&scenario=baseline")
    assert scores.status_code == 200
    payload = scores.json()
    assert payload["scores"]
    assert 0 <= payload["scores"][0]["final_score"] <= 100
    assert all(0.95 <= row["paf_value"] <= 1.05 for row in payload["scores"])
    assert payload["scores"][0]["confidence"]["confidence_grade"] in {"A", "B", "C", "D", "E"}

    provenance = client.get("/npem/provenance?province=AB&group=YA_UC&year=2025")
    assert provenance.status_code == 200
    assert provenance.json()

    citations = client.get("/npem/citations?province=AB&group=YA_UC&year=2025")
    assert citations.status_code == 200
    assert citations.json()

    job = client.post("/admin/jobs/calculate-npem", headers=_admin_headers())
    assert job.status_code == 200
    assert job.json()["job_run"]["rows_updated"] > 0
    app.dependency_overrides.clear()
    db.close()
