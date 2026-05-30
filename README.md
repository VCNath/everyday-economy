# Everyday Economy

Everyday Economy is a map-first economic dashboard that translates official Canadian economic data into plain-English cost-of-living signals.

The project is a runnable full-stack scaffold:

- `apps/web`: Next.js, React, TypeScript dashboard UI with backend fallbacks.
- `apps/api`: FastAPI backend, SQLAlchemy models, source connectors, ingestion jobs, calculations, and tests.
- `packages/shared`: shared TypeScript indicator and location types.
- `infra`: Docker Compose for API, worker, scheduler, PostgreSQL, and Redis.
- `docs`: product, data, API, deployment, and methodology notes.

Economic data shown by the app is **latest available**, not live second-by-second market data.

## Quick Start

```bash
pnpm install
python3 -m venv .venv
source .venv/bin/activate
pip install -e "apps/api[dev]"
```

Start infrastructure:

```bash
docker compose -f infra/docker-compose.yml up postgres redis
```

Start the backend:

```bash
source .venv/bin/activate
python -m uvicorn app.main:app --reload --app-dir apps/api --port 8000
```

Run a first CPI ingest:

```bash
PYTHONPATH=apps/api python -m app.jobs.ingest_statcan --dataset cpi
```

Start the frontend:

```bash
pnpm dev
```

Frontend: http://localhost:3000  
Backend docs: http://localhost:8000/docs

Local Docker note:

- The default local `postgres` service uses `postgres:16-alpine` for cross-platform startup reliability, including Apple Silicon.
- Production/staging should still use PostGIS-enabled managed Postgres where geography workloads require PostGIS features.

## Data Engine Commands

```bash
PYTHONPATH=apps/api python -m app.jobs.refresh_all
PYTHONPATH=apps/api python -m app.jobs.ingest_statcan --dataset cpi
PYTHONPATH=apps/api python -m app.jobs.ingest_statcan --dataset gas
PYTHONPATH=apps/api python -m app.jobs.ingest_statcan --dataset labour
PYTHONPATH=apps/api python -m app.jobs.ingest_statcan --dataset food_prices
PYTHONPATH=apps/api python -m app.jobs.ingest_statcan --dataset bank_of_canada
PYTHONPATH=apps/api python -m app.jobs.refresh_indicators
PYTHONPATH=apps/api python -m app.jobs.calculate_baskets
PYTHONPATH=apps/api python -m app.jobs.build_leaderboards
```

## Phase 3.5 Query Endpoints

- `GET /compare`
  - Supports `location_ids`, `indicators`, `window`, `start_period`, `end_period`, `include_series`, `include_freshness`
- `GET /regions/{location_id}/series`
  - Supports `indicators`, `window`, `start_period`, `end_period`, `include_freshness`

Supported windows: `3m`, `6m`, `12m`, `24m`, `5y`, `all`.

## Trust Metadata

Metric responses may include trust metadata with:

- `freshness_status` (`healthy`, `stale`, `partial`, `cached`, `estimated`, `unavailable`, `error`, `disabled`)
- `is_estimated`
- `is_cached`
- `coverage_score`
- `source_id` and `source_name`

Frontend pages use these to render trust badges rather than hiding uncertainty.

## Alembic Baseline

Alembic is now configured in `apps/api/alembic` with baseline revision `20260528_0001`.

From `apps/api`:

```bash
alembic upgrade head
alembic revision --autogenerate -m "your message"
```

`infra/postgres/init.sql` remains available for local bootstrap. New schema changes should use Alembic revisions.

SQLite smoke test:

```bash
PYTHONPATH=apps/api DATABASE_URL=sqlite:////tmp/everyday-economy.db \
  python -m app.jobs.ingest_statcan --dataset cpi
```

## Implemented Sources

- Statistics Canada bulk CSV: CPI, food prices, gasoline, labour force scaffolds; CPI is verified end-to-end.
- Bank of Canada Valet API: policy rate and CAD/USD series wiring.
- World Bank, OECD, and CMHC are disabled registry stubs for later phases.

The API uses persisted observations when available and seeded data when real data is missing or unavailable. Frontend mock data remains as the final fallback.

## Phase 4 Account Layer

Phase 4 adds a first user-state layer without breaking public routes:

- Login/signup/forgot/reset pages are now functional with a local auth scaffold.
- New backend account routes under `/me` persist profile, preferences, and saved regions.
- `/account/saved-regions` is the watchlist page, enriched with latest region summary metrics.
- Sidebar/topbar/menu are auth-aware.

Current auth implementation is a provider-ready scaffold using demo bearer tokens (`Bearer demo:<email>[:name]`) for local development.
Supabase environment variables are now included in `.env.example` for provider swap-in:

- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `SUPABASE_URL`
- `SUPABASE_JWT_SECRET`
- `SUPABASE_SERVICE_ROLE_KEY`

### Production Auth

Phase 7 wires Supabase Auth as the production path:

- Frontend sessions use `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY`.
- Backend `/me/*` and `/admin/*` calls verify Supabase JWTs with `SUPABASE_JWT_SECRET` or `SUPABASE_JWKS_URL`.
- Demo bearer tokens are local-only and must be disabled in production with `ALLOW_DEMO_AUTH=false`.
- Admin access comes from the local `users.role` column, not from frontend claims.
- Promote an admin manually after first login:

```sql
UPDATE users SET role = 'admin' WHERE email = 'admin@example.com';
```

Google OAuth remains a disabled UI affordance until the Supabase provider is configured.

## Phase 5 Alerts + Reports

Phase 5 adds personal notification and reporting foundations:

- Alert rule CRUD (`/me/alerts`)
- Notification inbox (`/me/notifications`)
- Notification preferences (`/me/notification-preferences`)
- Monthly reports (`/me/reports`)
- Alert evaluation job: `python -m app.jobs.evaluate_alerts`
- Monthly report job: `python -m app.jobs.generate_monthly_reports`

Email is scaffolded via `EMAIL_PROVIDER` with `disabled` and `console` modes ready. Provider integrations are intentionally stubbed.

## Phase 6 Admin Operations

Phase 6 adds an internal operations console and admin APIs:

- Admin overview and operations pages: `/admin`, `/admin/source-health`, `/admin/data-ingestion`, `/admin/data-quality`, `/admin/feature-flags`, `/admin/users`, `/admin/audit-logs`
- Backend-admin protected endpoints under `/admin/*` with role enforcement
- Safe job trigger whitelist and `job_runs` tracking
- Admin audit logging for mutable operations
- Runtime feature flag storage and toggling

Local demo admin token format:

- `Authorization: Bearer demo:admin@example.com:Admin:admin`

Or any `@admin.local` email in demo mode (for legacy convenience).

## Phase 7 Deployment Readiness

Phase 7 adds production-readiness controls:

- Supabase JWT verification in the backend.
- Supabase browser auth on the frontend.
- Environment-based CORS via `ALLOWED_ORIGINS`.
- Basic in-memory rate limiting via `RATE_LIMIT_ENABLED` and `RATE_LIMIT_REQUESTS_PER_MINUTE`.
- Email modes: `disabled`, `console`, and provider-ready `resend`.
- Production deployment, backup/restore, and security checklist documentation.

Production must set:

- `ENVIRONMENT=production`
- `ALLOW_DEMO_AUTH=false`
- explicit `ALLOWED_ORIGINS`
- backend-only email and Supabase service secrets

## Phase 8 UI Polish

Phase 8 introduces the modern visual system:

- MUI theme infrastructure with custom Everyday Economy tokens.
- Clear/glass light-first surfaces with polished dark mode support.
- Blue, cyan, and green brand palette.
- Generated landing hero asset at `apps/web/public/brand/economic-radar-glass.png`.
- Reusable polish primitives such as `GlassCard`, `SectionHeader`, `PageHero`, `StatusPill`, `TrendPill`, `DataTable`, `FilterBar`, and `LoadingSkeleton`.
- Updated design documentation in `docs/design-system.md`.

Phase 8 does not deploy the app. Staging deployment and public beta preparation move to Phase 9.

## Phase 9 Staging Readiness

Phase 9 prepares the app for a controlled staging deployment without adding new product features.

Recommended staging stack:

- Frontend: Vercel.
- Backend: Render, Fly.io, Railway, or another Docker-capable host.
- Database: managed PostgreSQL/PostGIS such as Supabase Postgres.
- Redis: Upstash Redis or managed Redis.
- Auth: Supabase Auth.
- Monitoring: hosting logs first; Sentry optional.

Staging safety requirements:

- `ENVIRONMENT=staging`
- `ALLOW_DEMO_AUTH=false`
- explicit `ALLOWED_ORIGINS`
- no frontend exposure of backend-only secrets
- admin role promoted through the database

Staging setup docs:

- `docs/deployment.md`
- `docs/staging-qa-checklist.md`
- `docs/backup-restore.md`
- `docs/security-checklist.md`

Useful verification commands:

```bash
pnpm test:web
pnpm build:web
pnpm test:api
pnpm docker:api
```

First staging data-load sequence from the backend runtime:

```bash
alembic upgrade head
python -m app.jobs.seed_reference_data
python -m app.jobs.ingest_statcan --dataset cpi
python -m app.jobs.ingest_statcan --dataset gas
python -m app.jobs.ingest_statcan --dataset bank_of_canada
python -m app.jobs.refresh_indicators
python -m app.jobs.build_leaderboards
python -m app.jobs.calculate_baskets
```

## Phase 10 N.P.E.M.

Phase 10 adds the National Personal Economic Model:

- N.P.E.M. database tables and Alembic migration.
- Group/archetype registry with core groups and overlapping overlays.
- Variable dictionary.
- Scenario weights for `baseline`, `housing_stress`, and `income_strength`.
- Winsorized 0-100 normalization.
- Confidence score and grade.
- Provincial adjustment factor.
- Provenance and citation records.
- API routes under `/npem`.
- Frontend routes under `/npem`.

Development calculation command:

```bash
PYTHONPATH=apps/api .venv/bin/python -m app.jobs.calculate_npem
```

Current N.P.E.M. values are deterministic demo/estimated scaffold data, not production facts. See `docs/npem-methodology.md`.

## Phase 11 Public Beta

Phase 11 adds the first public beta feedback and stabilization layer:

- A subtle public beta banner across the app.
- Public feedback submission at `POST /feedback`.
- Admin feedback review at `/admin/feedback` and `GET/PUT /admin/feedback`.
- Public help, FAQ, known limitations, changelog, and release note pages.
- Data issue reporting through the same feedback flow.
- Public beta checklist and release notes documentation.

The feedback system accepts anonymous feedback and logged-in feedback. It stores only practical support metadata such as page path, browser/device hints, optional region/indicator/source fields, and the user id when safely available. Admin feedback status changes are audited.

Useful beta documentation:

- `docs/public-beta-checklist.md`
- `docs/feedback-system.md`
- `docs/beta-release-notes.md`
- `docs/known-limitations.md`
