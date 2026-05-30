# Backup and Restore

Everyday Economy stores both product state and economic observations in PostgreSQL/PostGIS. Backups must protect user data, saved regions, alerts, notifications, reports, observations, source freshness, and admin operations history.

## Recommended Staging and Production Policy

- Use managed PostgreSQL automated backups where available.
- Keep at least daily backups for staging and production.
- Test restore into a disposable database before public beta.
- Run Alembic migrations after restoring an older backup.
- Never store database dumps with real user data in the repository.

## Manual Backup

Use the direct database URL when possible:

```bash
pg_dump "$DATABASE_URL" > everyday-economy-backup.sql
```

Compressed backup:

```bash
pg_dump "$DATABASE_URL" | gzip > everyday-economy-backup.sql.gz
```

## Manual Restore

Restore into an empty database:

```bash
psql "$DATABASE_URL" < everyday-economy-backup.sql
cd apps/api
alembic upgrade head
```

Restore from a compressed backup:

```bash
gunzip -c everyday-economy-backup.sql.gz | psql "$DATABASE_URL"
cd apps/api
alembic upgrade head
```

## PostGIS Requirement

Before applying migrations or restoring geometry-capable tables, enable PostGIS:

```sql
CREATE EXTENSION IF NOT EXISTS postgis;
```

Most current geometries are nullable, but staging and production databases should still enable PostGIS to match the expected schema.

## Critical Tables

- `users`
- `user_preferences`
- `saved_regions`
- `saved_baskets`
- `alert_rules`
- `notifications`
- `notification_preferences`
- `monthly_reports`
- `locations`
- `indicators`
- `data_sources`
- `observations`
- `calculations`
- `leaderboards`
- `baskets`
- `source_freshness`
- `source_refresh_runs`
- `raw_source_payloads`
- `data_quality_flags`
- `job_runs`
- `admin_audit_logs`
- `feature_flags`

## Restore Drill

Before public beta:

1. Create a temporary database.
2. Enable PostGIS.
3. Restore the latest backup.
4. Run `alembic upgrade head`.
5. Start the API against the restored database.
6. Check `/health/db`, `/locations`, `/source-status`, `/leaderboards`, and `/admin`.
7. Confirm account, saved regions, alerts, and reports load for a test user.

## Known Limitations

- Redis cache contents are not treated as durable data.
- Email provider delivery logs live with the provider unless exported separately.
- Production point-in-time recovery depends on the managed database provider selected in Phase 9.
