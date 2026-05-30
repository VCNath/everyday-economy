# Data Dictionary

## Sources

| Source ID | Name | Enabled | API key | Refresh | Notes |
| --- | --- | --- | --- | --- | --- |
| `statcan` | Statistics Canada | yes | no | monthly/daily check | Bulk CSV source for CPI, food/product prices, gasoline, and labour force data. |
| `bank_of_canada` | Bank of Canada Valet API | yes | no | daily | Policy-rate and CAD/USD context series. |
| `internal` | Everyday Economy calculations | yes | no | after ingest | YoY/MoM, baskets, affordability score, leaderboards. |
| `world_bank` | World Bank Indicators API | no | no | later | Stub for global comparison. |
| `oecd` | OECD Data Explorer API | no | no | later | Stub for OECD comparison. |
| `cmhc` | CMHC | no | no | later | Stub for housing/rent data. |
| `fred` | Federal Reserve Economic Data | no | yes | later | Stub for future U.S. expansion. |
| `bls` | U.S. Bureau of Labor Statistics | no | no | later | Stub for future U.S. labour/inflation coverage. |
| `bea` | U.S. Bureau of Economic Analysis | no | yes | later | Stub for future U.S. GDP/macro coverage. |

## Indicators

| Internal ID | Label | Category | Unit | Source | External ID |
| --- | --- | --- | --- | --- | --- |
| `cpi_all_items_index` | All-items CPI index | prices | index | Statistics Canada | `18-10-0004-01` |
| `cpi_all_items_yoy` | Overall inflation | prices | percent | Internal calculation | CPI index YoY |
| `cpi_food_index` | Food CPI index | prices | index | Statistics Canada | `18-10-0004-01` |
| `cpi_food_yoy` | Food inflation | prices | percent | Internal calculation | Food CPI YoY |
| `cpi_shelter_index` | Shelter CPI index | housing | index | Statistics Canada | `18-10-0004-01` |
| `cpi_shelter_yoy` | Shelter inflation | housing | percent | Internal calculation | Shelter CPI YoY |
| `gas_regular_cents_litre` | Regular gasoline | transportation | cents/litre | Statistics Canada | `18-10-0001-01` |
| `unemployment_rate` | Unemployment rate | labour | percent | Statistics Canada | `14-10-0287-01` |
| `employment_rate` | Employment rate | labour | percent | Statistics Canada | `14-10-0287-01` |
| `participation_rate` | Participation rate | labour | percent | Statistics Canada | `14-10-0287-01` |
| `basic_basket_monthly_cost` | Basic basket monthly cost | basket | CAD/month | Internal/StatCan | Retail product prices |
| `basic_basket_yoy` | Basic basket YoY | basket | percent | Internal calculation | Basket YoY |
| `affordability_score` | Affordability score v1 | composite | score | Internal calculation | v1 estimate |
| `boc_policy_rate` | Bank of Canada policy rate | financial | percent | Bank of Canada | `V39079` |
| `cad_usd_exchange_rate` | CAD/USD exchange rate | financial | CAD per USD | Bank of Canada | `FXUSDCAD` |

## Locations

Canonical Canada locations are `CA`, `CA-BC`, `CA-AB`, `CA-SK`, `CA-MB`, `CA-ON`, `CA-QC`, `CA-NB`, `CA-NS`, `CA-PE`, `CA-NL`, `CA-YT`, `CA-NT`, and `CA-NU`. Geometry is nullable until province geometries are loaded.

## User State Tables (Phase 4)

- `users`: account identity (`id`, `email`, display fields, role, timestamps)
- `user_preferences`: per-user defaults (region, metric, period, basket, theme, density)
- `saved_regions`: user watchlist entries keyed by `(user_id, location_id)`
- `saved_baskets`: reserved for later phase basket persistence

## Alerts and Reporting Tables (Phase 5)

- `alert_rules`: user-configured threshold/change/rank rule definitions
- `notifications`: in-app alert and report events with read state
- `notification_preferences`: per-user delivery and category toggles
- `monthly_reports`: generated per-region monthly affordability summaries

## Admin Operations Tables (Phase 6)

- `job_runs`: operational run history for manual/scheduled jobs
- `admin_audit_logs`: mutation audit trail for admin actions
- `feature_flags`: runtime feature toggles with update metadata
- `data_quality_flags` now includes review fields (`reviewed_at`, `reviewed_by_user_id`, `review_note`)

## Phase 7 Security Notes

Phase 7 does not add new database tables. It hardens how existing account and admin tables are used:

- `users.role` is the source of truth for admin access.
- Supabase user IDs are synced into `users.id` after JWT verification.
- Demo-auth-created users are local-development records only.
- Admin promotion should be performed directly in the database, for example:

```sql
UPDATE users SET role = 'admin' WHERE email = 'admin@example.com';
```

## Phase 9 Deployment Notes

Phase 9 does not add new tables. Staging deployment relies on the existing Alembic schema and these bootstrap steps:

- enable PostGIS in the managed database
- run `alembic upgrade head`
- run `python -m app.jobs.seed_reference_data`
- run available ingestion/calculation jobs
- verify source freshness, leaderboards, baskets, account data, and admin operation tables

Redis is treated as cache/operational support, not durable product state.

## N.P.E.M. Tables (Phase 10)

- `npem_group_metadata`: core archetypes and overlay cohort metadata.
- `npem_variables`: N.P.E.M. variable dictionary.
- `npem_raw_data`: raw variable records by source/geography/year/group.
- `npem_normalized_scores`: 0-100 component scores after winsorized normalization.
- `npem_scenarios`: scenario definitions.
- `npem_scenario_weights`: scenario component weights.
- `npem_scores`: final scenario scores by geography, group, and year.
- `npem_provenance`: source/provenance/citation records for scores.
- `npem_quality_components`: coverage, recency, directness, reliability, proxy, and suppression scores.
- `npem_provincial_adjustments`: provincial adjustment factor inputs and outputs.

Current N.P.E.M. data is seeded/demo estimated data for development rendering and tests.

## Public Beta Tables (Phase 11)

- `beta_feedback`: public beta feedback and data issue submissions.

`beta_feedback` stores:

- optional `user_id` for authenticated feedback
- `page_path`
- `feedback_type`
- optional `rating`
- sanitized `message`
- optional contact `email`
- safe metadata JSON for browser/page context or data issue hints
- review `status`
- `created_at` and `updated_at`

Feedback metadata should avoid sensitive personal data. Intended keys include `viewport`, `userAgent`, `region`, `indicator`, `source`, and `period`.
