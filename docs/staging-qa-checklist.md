# Staging QA Checklist

Use this checklist after each staging deploy and before inviting public beta users.

## Environment

- [ ] Frontend URL is set in backend `ALLOWED_ORIGINS`.
- [ ] Frontend `NEXT_PUBLIC_API_BASE_URL` points to the staging API.
- [ ] Backend `ENVIRONMENT=staging`.
- [ ] Backend `ALLOW_DEMO_AUTH=false`.
- [ ] Database URL points to managed staging Postgres/PostGIS.
- [ ] Redis URL points to managed staging Redis, or Redis degradation is documented.
- [ ] Supabase redirect URLs include local and staging frontend URLs.
- [ ] Email mode is intentionally set to `disabled`, `console`, or a configured provider.

## Public Routes

- [ ] `/`
- [ ] `/dashboard`
- [ ] `/map`
- [ ] `/leaderboards`
- [ ] `/compare`
- [ ] `/basket`
- [ ] `/regions/CA-SK`
- [ ] `/insights`
- [ ] `/data/sources`
- [ ] `/data/api-status`
- [ ] `/data/methodology`
- [ ] `/npem`
- [ ] `/npem/methodology`
- [ ] `/help`
- [ ] `/help/faq`
- [ ] `/help/known-limitations`
- [ ] `/changelog`
- [ ] `/releases`

Verify:

- [ ] Pages render without console crashes.
- [ ] Backend unavailable fallback still renders public pages.
- [ ] Trust badges show source/freshness/estimated states.
- [ ] "Latest available data" language appears where appropriate.

## Auth

- [ ] Signup works.
- [ ] Login works.
- [ ] Logout works.
- [ ] Forgot password flow sends or logs the expected message.
- [ ] Reset password redirect is configured if enabled.
- [ ] Backend creates/syncs local user row after authenticated API call.

## Account Routes

- [ ] `/account/profile`
- [ ] `/account/saved-regions`
- [ ] `/account/preferences`
- [ ] `/account/alerts`
- [ ] `/account/notifications`
- [ ] `/account/reports`
- [ ] `/account/billing`

Verify:

- [ ] Logged-out users see a login prompt or redirect.
- [ ] Logged-in users can load account data.
- [ ] Billing remains a safe placeholder.

## User Flows

- [ ] Save a region.
- [ ] Remove a saved region.
- [ ] Update preferences.
- [ ] Create an alert.
- [ ] Disable and re-enable an alert.
- [ ] Run alert evaluation for test data.
- [ ] View generated notification.
- [ ] Mark notification read.
- [ ] Generate a monthly report for a saved region.
- [ ] Submit general feedback.
- [ ] Submit a data issue report from a source or methodology context.

## Admin

- [ ] Promote one staging user with `UPDATE users SET role = 'admin' WHERE email = '...'`.
- [ ] Logged-out users cannot access admin pages.
- [ ] Non-admin users see a forbidden state.
- [ ] Admin user can open `/admin`.
- [ ] `/admin/source-health`
- [ ] `/admin/data-ingestion`
- [ ] `/admin/data-quality`
- [ ] `/admin/feature-flags`
- [ ] `/admin/users`
- [ ] `/admin/audit-logs`
- [ ] `/admin/feedback`

Verify:

- [ ] Manual job trigger confirmation appears.
- [ ] Allowed job triggers create `job_runs` rows.
- [ ] Unknown job triggers are rejected.
- [ ] Feature flag toggles create audit logs.
- [ ] Feedback status updates create audit logs.
- [ ] Admin mutation actions remain audited.

## Data

- [ ] `alembic upgrade head` completed.
- [ ] `python -m app.jobs.seed_reference_data` completed.
- [ ] At least CPI ingestion has run, or seeded fallback is intentionally in use.
- [ ] `python -m app.jobs.build_leaderboards` completed.
- [ ] `python -m app.jobs.calculate_baskets` completed.
- [ ] `/source-status` returns source rows.
- [ ] `/health/sources` returns source health.
- [ ] Leaderboards render from backend response.
- [ ] Region summary renders for `CA-SK`.
- [ ] Compare page renders default regions.
- [ ] Basket page renders item-level estimates and coverage.

## Mobile

- [ ] `/dashboard`
- [ ] `/map`
- [ ] `/leaderboards`
- [ ] `/regions/CA-SK`
- [ ] `/account/saved-regions`
- [ ] `/account/alerts`
- [ ] `/admin`

Verify:

- [ ] No unintended horizontal overflow.
- [ ] Tables scroll only where intentional.
- [ ] Buttons are touch-friendly.
- [ ] Bottom navigation and drawers work.

## Performance

- [ ] Frontend build has no unexpected bundle warnings.
- [ ] Dashboard does not issue duplicate API requests on first load.
- [ ] Large tables remain responsive.
- [ ] Map interaction remains smooth enough on mobile.

## Accessibility

- [ ] Keyboard focus is visible.
- [ ] Forms have labels.
- [ ] Icon buttons have accessible labels.
- [ ] Tables have headers.
- [ ] Status is not communicated by colour alone.
- [ ] Reduced-motion preference is respected where animation exists.

## Security

- [ ] Demo auth is disabled in staging.
- [ ] Supabase service role key is not exposed to frontend.
- [ ] Public pages do not expose user-specific data.
- [ ] `/me/*` routes require auth.
- [ ] `/admin/*` routes require admin role.
- [ ] CORS does not use wildcard origins.
- [ ] Rate limiting is enabled or provider-level limits are configured.
- [ ] Secrets are stored only in provider environment settings.
- [ ] Database backups are configured or scheduled.
