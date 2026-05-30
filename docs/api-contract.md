# API Contract

The frontend calls only the FastAPI backend. Statistics Canada, Bank of Canada, and future source APIs are accessed through backend connectors and ingestion jobs.

## Preserved Endpoints

- `GET /health`
- `GET /health/db`
- `GET /health/cache`
- `GET /health/sources`
- `GET /locations`
- `GET /locations/search?q=sask`
- `GET /indicators`
- `GET /indicators/categories`
- `GET /map?indicator=cpi_food_yoy&geography_level=province&date=latest`
- `GET /regions/{location_id}/summary`
- `GET /leaderboards`
- `GET /leaderboards/{leaderboard_type}`
- `GET /basket/default`
- `POST /basket/calculate`
- `GET /source-status`
- `GET /source-status/runs`
- `GET /source-status/quality`
- `GET /compare`
- `GET /regions/{location_id}/series`
- `GET /me`
- `GET /me/profile`
- `PUT /me/profile`
- `GET /me/preferences`
- `PUT /me/preferences`
- `GET /me/saved-regions`
- `POST /me/saved-regions`
- `DELETE /me/saved-regions/{location_id}`
- `GET /me/watchlist`
- `GET /me/alerts`
- `POST /me/alerts`
- `GET /me/alerts/{alert_id}`
- `PUT /me/alerts/{alert_id}`
- `DELETE /me/alerts/{alert_id}`
- `POST /me/alerts/{alert_id}/enable`
- `POST /me/alerts/{alert_id}/disable`
- `GET /me/notifications`
- `GET /me/notifications/unread-count`
- `POST /me/notifications/{notification_id}/read`
- `POST /me/notifications/read-all`
- `GET /me/notification-preferences`
- `PUT /me/notification-preferences`
- `GET /me/reports`
- `GET /me/reports/{report_id}`
- `POST /me/reports/generate`
- `POST /me/reports/generate-monthly`
- `POST /admin/evaluate-alerts`
- `POST /admin/generate-monthly-reports`
- `GET /admin/summary`
- `GET /admin/source-health`
- `GET /admin/job-runs`
- `GET /admin/job-runs/{job_run_id}`
- `POST /admin/jobs/refresh-source`
- `POST /admin/jobs/refresh-all`
- `POST /admin/jobs/refresh-cpi`
- `POST /admin/jobs/refresh-gas`
- `POST /admin/jobs/refresh-labour`
- `POST /admin/jobs/evaluate-alerts`
- `POST /admin/jobs/generate-monthly-reports`
- `POST /admin/jobs/build-leaderboards`
- `POST /admin/jobs/calculate-baskets`
- `GET /admin/data-quality`
- `POST /admin/data-quality/{flag_id}/review`
- `GET /admin/audit-logs`
- `GET /admin/feature-flags`
- `PUT /admin/feature-flags/{key}`
- `GET /admin/users`
- `GET /npem/groups`
- `GET /npem/groups/select?province=AB&year=2025`
- `GET /npem/variables`
- `GET /npem/scenarios`
- `GET /npem?province=AB&year=2025&scenario=baseline`
- `GET /npem/trend?province=AB&group=YA_UC&from_year=2021&to_year=2025&scenario=baseline`
- `GET /npem/compare?province=AB&scenario_a=baseline&scenario_b=housing_stress`
- `GET /npem/provenance?province=AB&group=YA_UC&year=2025`
- `GET /npem/citations?province=AB&group=YA_UC&year=2025`
- `POST /feedback`
- `GET /admin/feedback`
- `PUT /admin/feedback/{feedback_id}`

## Behavior

Responses keep the existing frontend shape. If persisted source data exists, services use it. If real data is missing, source ingestion fails, or the database is unavailable, the backend falls back to seeded Canadian data and the frontend falls back to mock data.

`/source-status` returns source, dataset, latest available period, last checked date, status, and optional notes. `/source-status/runs` exposes latest ingestion run counts for admin status screens. `/source-status/quality` summarizes non-blocking data quality flags.

## Authentication and Security

Public data endpoints remain public. Account endpoints under `/me/*` require `Authorization: Bearer <access_token>`.

Production auth uses Supabase JWTs verified by the backend. Local demo tokens are accepted only when `ALLOW_DEMO_AUTH=true` and `ENVIRONMENT` is not production.

Admin endpoints under `/admin/*` require an authenticated local user with `users.role = 'admin'`. The backend does not trust frontend-provided role values. Non-admin users receive `403`; missing or invalid auth receives `401`.

The API uses environment-based CORS from `ALLOWED_ORIGINS` and a configurable rate-limit middleware. Rate limit responses use HTTP `429`.

## Staging Deployment Contract

Staging and production deployments must keep these deployment-facing contracts stable:

- `GET /health` is the backend platform health check.
- `GET /health/db` verifies database connectivity.
- `GET /health/cache` verifies Redis/cache connectivity and may report an error state without crashing the API.
- `GET /health/sources` summarizes data-source freshness for operations.
- Frontend requests must use `NEXT_PUBLIC_API_BASE_URL`; no deployed frontend should call `localhost`.
- Backend CORS must allow the deployed frontend origin through `ALLOWED_ORIGINS`.
- Staging and production must set `ALLOW_DEMO_AUTH=false`.
- Admin APIs remain backend-role protected even if the admin navigation is hidden in the frontend.

Canonical staging setup command order:

```bash
alembic upgrade head
python -m app.jobs.seed_reference_data
python -m app.jobs.ingest_statcan --dataset cpi
python -m app.jobs.refresh_indicators
python -m app.jobs.build_leaderboards
python -m app.jobs.calculate_baskets
```

## Leaderboards

Implemented leaderboard IDs:

- `highest_inflation`
- `lowest_inflation`
- `highest_food_inflation`
- `most_expensive_groceries`
- `cheapest_groceries`
- `highest_gas_prices`
- `lowest_gas_prices`
- `highest_unemployment`
- `best_affordability`
- `worst_affordability`
- `biggest_monthly_movers`

Legacy aliases such as `grocery_basket`, `gas_prices`, and `unemployment` remain supported.

## Compare Query Params

`GET /compare` supports:

- `location_ids=CA-SK,CA-AB,CA-MB`
- `indicators=cpi_all_items_yoy,cpi_food_yoy,gas_regular_cents_litre`
- `start_period=YYYY-MM` and `end_period=YYYY-MM`
- `window=3m|6m|12m|24m|5y|all`
- `include_series=true|false`
- `include_freshness=true|false`

## Region Series Query Params

`GET /regions/{location_id}/series` supports:

- `indicators=...` (comma-separated)
- `start_period=YYYY-MM` and `end_period=YYYY-MM`
- `window=3m|6m|12m|24m|5y|all`
- `include_freshness=true|false`

## Account/Auth Notes

`/me/*` endpoints require an auth bearer token.

Current local scaffold token format:

- `Authorization: Bearer demo:<email>[:display_name]`

Invalid or missing auth returns `401`.
Saved regions validate `location_id` and return `400` for unknown locations.

Admin endpoints require authenticated admin role:

- missing auth -> `401`
- authenticated non-admin -> `403`

## N.P.E.M. Notes

N.P.E.M. responses include:

- scenario metadata and weights
- model version
- final score and rank
- component scores
- confidence score/grade/label
- proxy and overlap warnings
- provenance summaries and citations

Current N.P.E.M. values are deterministic demo/estimated scaffold data. They are labelled as such and should not be presented as production facts until real source adapters and validation review are complete.

## Public Beta Feedback

`POST /feedback` is public and accepts anonymous or authenticated feedback:

```json
{
  "page_path": "/regions/CA-SK",
  "feedback_type": "data_issue",
  "rating": 3,
  "message": "The gas price source note was confusing.",
  "email": "optional@example.com",
  "metadata": {
    "region": "CA-SK",
    "indicator": "gas_regular_cents_litre",
    "source": "statcan",
    "period": "2026-04"
  }
}
```

Allowed feedback types are `bug`, `data_issue`, `confusing`, `feature_request`, `design_feedback`, and `general`.

Admin feedback routes require admin role:

- `GET /admin/feedback?status=new&feedback_type=data_issue`
- `PUT /admin/feedback/{feedback_id}` with `{ "status": "reviewed" }`

Allowed statuses are `new`, `reviewed`, `planned`, `fixed`, and `closed`. Feedback status updates create admin audit log entries.
