# Deployment

## Local Development Flow

1. Start Postgres and Redis:

```bash
docker compose -f infra/docker-compose.yml up postgres redis
```

2. Start FastAPI:

```bash
source .venv/bin/activate
python -m uvicorn app.main:app --reload --app-dir apps/api --port 8000
```

3. Run ingestion or a seed/calculation command:

```bash
PYTHONPATH=apps/api python -m app.jobs.ingest_statcan --dataset cpi
PYTHONPATH=apps/api python -m app.jobs.refresh_indicators
```

4. Start Next.js:

```bash
pnpm dev
```

5. Open http://localhost:3000 and verify dashboard, leaderboards, source status, and region summary.

## Migrations

Alembic baseline is configured in `apps/api/alembic`.

From `apps/api`:

```bash
alembic upgrade head
alembic revision --autogenerate -m "describe change"
```

`infra/postgres/init.sql` can still bootstrap a fresh local Postgres, but ongoing schema evolution should use Alembic revisions.

## Docker

```bash
docker compose -f infra/docker-compose.yml up --build
```

The compose stack includes:

- `api`: FastAPI backend.
- `worker`: refresh calculations/leaderboards.
- `scheduler`: runs `python -m app.jobs.refresh_all`.
- `postgres`: PostgreSQL (`postgres:16-alpine`) for cross-platform local development.
- `redis`: cache service.

Local database note:

- The local compose default favors startup reliability on arm64 and Apple Silicon.
- Staging/production should still use a PostGIS-enabled managed Postgres if geography features require PostGIS.

## Environment

Required local variables are shown in `.env.example`. No current Statistics Canada, Bank of Canada, World Bank, OECD, or CMHC variable requires a secret API key.

Auth variables:

- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `SUPABASE_URL`
- `SUPABASE_JWT_SECRET`
- `SUPABASE_JWKS_URL`
- `SUPABASE_AUDIENCE`
- `SUPABASE_ISSUER`
- `SUPABASE_SERVICE_ROLE_KEY` (backend only, optional for current scaffold)
- `ALLOW_DEMO_AUTH`
- `ENVIRONMENT`

Production rules:

- Set `ENVIRONMENT=production`.
- Set `ALLOW_DEMO_AUTH=false`.
- Never expose `SUPABASE_SERVICE_ROLE_KEY` to the frontend.
- Promote admins through the database: `UPDATE users SET role = 'admin' WHERE email = '...';`.

Email variables:

- `EMAIL_PROVIDER=disabled|console|resend|sendgrid|postmark`
- `EMAIL_FROM`
- `RESEND_API_KEY`
- `SENDGRID_API_KEY`
- `POSTMARK_API_KEY`

Security variables:

- `ALLOWED_ORIGINS=https://your-frontend.example`
- `RATE_LIMIT_ENABLED=true`
- `RATE_LIMIT_REQUESTS_PER_MINUTE=120`

Admin operations tables are now part of schema evolution:

- `job_runs`
- `admin_audit_logs`
- `feature_flags`
- data quality review fields on `data_quality_flags`

## Suggested MVP Hosting

- Frontend: Vercel.
- Backend API: Render, Fly.io, Railway, or containerized VPS.
- Database: Supabase Postgres with PostGIS, Neon with PostGIS, or managed PostgreSQL.
- Cache: Upstash Redis or managed Redis.
- Scheduler: backend cron, GitHub Actions, or managed cron.
- Monitoring: Sentry and structured logs.

## Phase 9 Staging Deployment Runbook

Phase 9 moves the app from local development toward a controlled staging environment. The repository is provider-neutral, but the recommended first staging stack is:

- Frontend: Vercel.
- Backend: Render, Fly.io, Railway, or another Docker-capable host.
- Database: Supabase Postgres with PostGIS enabled, or another managed Postgres/PostGIS provider.
- Redis: Upstash Redis or managed Redis.
- Auth: Supabase Auth.
- Monitoring: hosting provider logs first; Sentry optional via `SENTRY_DSN` and `NEXT_PUBLIC_SENTRY_DSN`.

Actual staging URLs are created in the hosting providers, not in the repository.

### Frontend Deployment

Recommended Vercel settings:

- Framework: Next.js.
- Monorepo root: repository root.
- App directory/project root: `apps/web`.
- Install command: `corepack enable && pnpm install --frozen-lockfile`.
- Build command from monorepo root: `pnpm --filter @everyday-economy/web build`.
- Build command if Vercel executes inside `apps/web`: `pnpm build`.
- Output: `.next`.

Required staging frontend variables:

```bash
NEXT_PUBLIC_ENVIRONMENT=staging
NEXT_PUBLIC_API_BASE_URL=https://your-staging-api.example.com
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=...
NEXT_PUBLIC_ALLOW_DEMO_AUTH=false
NEXT_PUBLIC_SENTRY_DSN=
```

Confirm no production frontend build points to `localhost`.

### Backend Deployment

The API Dockerfile is in `apps/api` and starts Uvicorn with the platform-provided port:

```bash
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

Recommended backend settings:

- Docker build context: `apps/api`.
- Health check path: `/health`.
- Runtime command: use the Dockerfile default unless your provider requires an explicit command.
- Run migrations before exposing staging traffic.

Required staging backend variables:

```bash
ENVIRONMENT=staging
ALLOW_DEMO_AUTH=false
DATABASE_URL=postgresql+psycopg://...
REDIS_URL=rediss://...
ALLOWED_ORIGINS=https://your-staging-web.example.com
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_JWT_SECRET=...
SUPABASE_JWKS_URL=
SUPABASE_AUDIENCE=authenticated
SUPABASE_ISSUER=
EMAIL_PROVIDER=console
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS_PER_MINUTE=120
```

Use `.env.staging.example` as the safe template. Do not place real secrets in git.

### Database Setup

1. Create a staging database.
2. Enable PostGIS:

```sql
CREATE EXTENSION IF NOT EXISTS postgis;
```

3. Set `DATABASE_URL` on the backend host.
4. Run migrations from `apps/api`:

```bash
alembic upgrade head
```

5. Seed canonical reference data:

```bash
python -m app.jobs.seed_reference_data
```

For providers with pooled database URLs, prefer the direct connection URL for migrations when the provider recommends it.

### First Staging Data Load

Run these commands from the deployed backend shell/job runner or an equivalent release job:

```bash
alembic upgrade head
python -m app.jobs.seed_reference_data
python -m app.jobs.ingest_statcan --dataset cpi
python -m app.jobs.ingest_statcan --dataset gas
python -m app.jobs.ingest_statcan --dataset bank_of_canada
python -m app.jobs.refresh_indicators
python -m app.jobs.build_leaderboards
python -m app.jobs.calculate_baskets
python -m app.jobs.evaluate_alerts
python -m app.jobs.generate_monthly_reports
```

If a source is unavailable, public endpoints should continue to return persisted or seeded fallback data with warning/trust metadata.

### Supabase Auth Setup

1. Create a staging Supabase project.
2. Enable email/password auth.
3. Add redirect URLs:
   - `http://localhost:3000`
   - staging frontend URL
   - future production frontend URL
4. Set frontend Supabase public variables.
5. Set backend Supabase verification variables.
6. Create a staging user through the app.
7. Promote that user to admin:

```sql
UPDATE users
SET role = 'admin'
WHERE email = 'your-email@example.com';
```

Admin role comes from the local database, not from frontend-provided claims.

### Redis Setup

Set `REDIS_URL` to the managed Redis connection string. Redis supports cache/rate-limit/job-adjacent behavior, but the public app should still render with backend fallback data if Redis is temporarily unavailable.

### Monitoring and Logging

Minimum staging monitoring:

- Backend provider logs.
- Frontend provider build/runtime logs.
- `/health`, `/health/db`, `/health/cache`, and `/health/sources`.
- Admin `/admin/source-health` and `/admin/data-ingestion`.

Optional Sentry variables:

```bash
SENTRY_DSN=
NEXT_PUBLIC_SENTRY_DSN=
```

If Sentry is not configured before public beta, add uptime checks for the frontend and API `/health`.

## Staging Setup

1. Create a staging Supabase project or managed Postgres/PostGIS database.
2. Configure Redis or Upstash Redis.
3. Deploy the FastAPI backend with staging environment variables.
4. Run `alembic upgrade head` from `apps/api`.
5. Deploy the Next.js frontend with staging `NEXT_PUBLIC_*` variables.
6. Set backend `ALLOWED_ORIGINS` to the staging frontend URL.
7. Create a user through Supabase Auth, then promote admin role in the database.
8. Run ingestion and verify `/data/api-status`, `/admin/source-health`, and `/dashboard`.
9. Verify `/feedback` submission and `/admin/feedback` review.
10. Review `/help`, `/help/faq`, `/help/known-limitations`, `/changelog`, and `/releases`.
11. Complete `docs/staging-qa-checklist.md` and `docs/public-beta-checklist.md`.

## Production Setup

1. Create production database with PostGIS enabled.
2. Configure production Redis.
3. Configure Supabase Auth and capture JWT settings.
4. Set `ENVIRONMENT=production` and `ALLOW_DEMO_AUTH=false`.
5. Set explicit `ALLOWED_ORIGINS`; do not use wildcard origins.
6. Run `alembic upgrade head`.
7. Run source ingestion jobs.
8. Promote the initial admin user via SQL.
9. Configure email provider or leave `EMAIL_PROVIDER=disabled`.
10. Configure monitoring, logs, and backups before public access.

## Backup and Restore

See `docs/backup-restore.md` for the full backup and restore runbook.

Postgres backup:

```bash
pg_dump "$DATABASE_URL" > everyday-economy-backup.sql
```

Restore:

```bash
psql "$DATABASE_URL" < everyday-economy-backup.sql
alembic upgrade head
```

Managed providers such as Supabase should also have scheduled backups enabled.

Critical tables:

- `users`
- `user_preferences`
- `saved_regions`
- `saved_baskets`
- `alert_rules`
- `notifications`
- `notification_preferences`
- `monthly_reports`
- `observations`
- `source_freshness`
- `job_runs`
- `admin_audit_logs`
- `feature_flags`
- `beta_feedback`

## Security Checklist

See `docs/security-checklist.md` for the full staging and public beta checklist.

- Demo auth disabled in production.
- Admin routes backend-protected.
- Admin mutations audited.
- Supabase service role key backend-only.
- CORS locked to known frontend origins.
- Rate limiting enabled or replaced with a managed/Redis-backed limiter.
- Secrets are not committed.
- Public routes do not expose user-specific data.
- Account routes require auth.
- Email provider secrets backend-only.
- Database backups configured.
- Migrations tested before deploy.

## Known Limitations

- Province geometries are nullable until map geometry loading lands.
- World Bank, OECD, CMHC, FRED, BLS, and BEA ingestion are intentionally out of scope for Phase 2.
- Supabase auth is wired, but Google OAuth still requires provider configuration.
- Admin role checks are enforced by backend `/admin/*` routes even in demo auth mode.
- Email provider delivery supports disabled/console and Resend-ready configuration; SendGrid/Postmark remain documented stubs.
- Admin actions remain hidden/disabled unless explicitly enabled later.
- Public beta limitations are tracked in `docs/known-limitations.md`.
- Feedback review and release note process are documented in `docs/feedback-system.md` and `docs/beta-release-notes.md`.
