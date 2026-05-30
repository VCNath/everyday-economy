# Security Checklist

Use this checklist for staging readiness and again before public beta.

## Authentication

- [ ] `ALLOW_DEMO_AUTH=false` in staging and production.
- [ ] Demo admin tokens are rejected outside local development/test.
- [ ] Frontend uses Supabase session access tokens.
- [ ] Backend verifies Supabase JWTs.
- [ ] Missing or invalid auth returns `401`.
- [ ] Authenticated non-admin access to admin APIs returns `403`.
- [ ] Admin role is read from local `users.role`, not from frontend-supplied values.
- [ ] Initial admin is promoted manually with SQL.

## Secrets

- [ ] No real secrets are committed.
- [ ] `SUPABASE_SERVICE_ROLE_KEY` is backend-only.
- [ ] Email provider keys are backend-only.
- [ ] Database URLs and Redis URLs are stored in hosting provider secret settings.
- [ ] Staging and production have separate credentials.

## CORS and Network

- [ ] `ALLOWED_ORIGINS` contains only known frontend origins.
- [ ] No wildcard CORS in staging or production.
- [ ] `NEXT_PUBLIC_API_BASE_URL` points to the deployed API.
- [ ] Backend health endpoint is reachable.
- [ ] Admin and account APIs are not accessible without auth.

## Rate Limiting

- [ ] `RATE_LIMIT_ENABLED=true`, or provider/WAF rate limits are configured.
- [ ] `RATE_LIMIT_REQUESTS_PER_MINUTE` is set intentionally.
- [ ] Expensive admin mutations remain protected by auth and role checks.
- [ ] Public endpoints degrade gracefully under partial backend/source failures.

## Admin Operations

- [ ] Admin routes are backend-protected.
- [ ] Admin navigation is hidden for non-admins, but backend remains source of truth.
- [ ] Manual job triggers use a whitelist, not arbitrary commands.
- [ ] Admin mutations create audit logs.
- [ ] Feature flag updates are audited.

## Data and Privacy

- [ ] Public routes do not expose user-specific data.
- [ ] `/me/*` routes require authenticated user.
- [ ] Saved regions, alerts, notifications, and reports are scoped to the current user.
- [ ] Source freshness and data quality endpoints expose operational data only as intended.
- [ ] Raw payload storage is disabled unless explicitly needed.
- [ ] Feedback submissions do not collect unnecessary sensitive personal information.
- [ ] Feedback metadata is limited to safe page/browser/data issue context.
- [ ] Admin feedback review remains admin-only.

## Backups and Recovery

- [ ] Managed database backups are enabled.
- [ ] Restore procedure has been tested.
- [ ] Critical tables are documented in `docs/backup-restore.md`.
- [ ] Alembic migrations are tested before deploy.

## Email

- [ ] Staging email mode is intentionally `disabled`, `console`, or configured provider.
- [ ] Email failures do not break alert/report flows.
- [ ] Sender domain is verified before production sending.

## Pre-Beta Blockers

- [ ] Demo auth disabled.
- [ ] CORS locked.
- [ ] Admin role verified.
- [ ] Migrations tested.
- [ ] Backups configured.
- [ ] Staging QA checklist completed.
- [ ] Feedback form tested.
- [ ] Help, FAQ, known limitations, changelog, and release notes pages reviewed.
- [ ] Public beta checklist completed.
