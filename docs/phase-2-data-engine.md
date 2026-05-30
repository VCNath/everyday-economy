# Phase 2 Data Engine

Phase 2 turns the backend from seeded data into a real ingestion and persistence layer while preserving frontend contracts.

## Current capabilities

- Statistics Canada bulk CSV downloads:
  - CPI: `18-10-0004-01`
  - Retail food prices: `18-10-0245-01`
  - Gasoline prices: `18-10-0001-01`
  - Labour force: `14-10-0287-01`
- Bank of Canada Valet observations:
  - `V39079`: target for the overnight rate
- Normalized persistence through SQLAlchemy models.
- Source freshness updates.
- YoY and MoM calculations.
- Derived CPI YoY indicators from CPI index observations.
- Leaderboard snapshots from stored observations.
- Seeded fallback when the database is empty or unavailable.

## Data flow

1. Seed reference sources, locations, indicators, and leaderboard definitions.
2. Download source data.
3. Filter to supported Canadian geographies and MVP indicators.
4. Upsert normalized observations.
5. Update source freshness.
6. Calculate YoY, MoM, and national differences.
7. Derive CPI YoY observations.
8. Rebuild basket estimates where food-price coverage exists.
9. Rebuild leaderboard snapshots.

## Local commands

```bash
DATABASE_URL=sqlite:///./economy.db CREATE_TABLES_ON_STARTUP=true \
  python -m app.jobs.ingest_statcan
```

The default job ingests CPI, gasoline, and Bank of Canada policy-rate data. Add `--include-large-tables` to include labour and food-price tables.

## Fallback behavior

If PostgreSQL is not running, API route dependencies fall back to seeded data instead of failing the frontend. This keeps the app shell stable during source or database outages.
