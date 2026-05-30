# Source Methodology

Everyday Economy displays the **latest available** official data. It is not a real-time market terminal; most economic releases are monthly or daily with publication lag.

## Statistics Canada

Implemented/scaffolded tables:

- `18-10-0004-01`: monthly CPI by geography and product group. CPI is ingested end-to-end in Phase 2.
- `18-10-0245-01`: monthly average retail prices for selected products.
- `18-10-0001-01`: monthly gasoline and fuel oil prices.
- `14-10-0287-01`: monthly labour force characteristics.

The connector uses bulk CSV ZIP downloads from:

```text
https://www150.statcan.gc.ca/n1/tbl/csv/{product_id}-eng.zip
```

Retail product prices support a practical basket estimate, but they are not the full CPI basket.

## Bank of Canada

The Valet API connector is wired for:

- `V39079`: policy/overnight target rate context.
- `FXUSDCAD`: CAD per USD exchange-rate context.

These series require no API key.

## Calculations

YoY:

```text
((current_value - value_12_months_ago) / value_12_months_ago) * 100
```

MoM:

```text
((current_value - previous_month_value) / previous_month_value) * 100
```

National difference:

```text
region_value - Canada_value
```

Basket cost:

```text
SUM(item_price_in_region * monthly_quantity)
```

## Affordability Score v1

The affordability score is a directional 0-100 composite estimate, not an official index. It currently normalizes and weights:

- all-items CPI YoY
- food CPI YoY
- shelter CPI YoY
- gasoline price
- unemployment rate
- basic basket cost where available

Lower pressure improves the score. Missing components are skipped, and estimated values are marked as estimated.

## Quality and Freshness

Ingestion records source freshness by source and dataset. Non-critical data quality flags include missing values, unmapped locations, unmapped indicators, duplicate upserts, outlier changes, stale sources, and unit mismatches. Non-critical warnings do not block ingestion.

Frontend trust badges map to these statuses:

- `healthy`
- `stale`
- `partial`
- `cached`
- `estimated`
- `unavailable`
- `error`
- `disabled`

## Alerts and Reports (Phase 5)

Alert evaluation is deterministic and tied to stored observations. Supported operator families:

- threshold (`gt`, `gte`, `lt`, `lte`, `eq`)
- change (`change_gt`, `change_gte`)
- rank placeholders (`rank_below`, `rank_above`) for later leaderboard-coupled expansion

Monthly reports are deterministic summaries generated from stored region metrics and source metadata; they are not AI-generated narratives.

## Phase 6 Operations Method

Admin-triggered jobs use a strict whitelist and are never arbitrary shell execution from client input.

Operational records:

- `job_runs` capture status, timing, rows affected, and errors.
- `admin_audit_logs` capture admin mutations (feature flag changes, quality reviews, job triggers).
- Data quality flags can be marked reviewed with reviewer metadata.

## Phase 7 Production Safety Method

Production authentication uses Supabase JWT verification in the backend. Demo tokens are development-only and rejected when `ENVIRONMENT=production`.

Admin authorization is based on the local `users.role` value after token verification. Frontend state can hide or show admin UI, but the backend remains the source of truth for admin access.

Email delivery is non-blocking for alert and report flows. If a provider is disabled or fails, the notification/report operation should still complete and log the email outcome.

## Phase 10 N.P.E.M. Method

N.P.E.M. is a separate scoring layer from the legacy `affordability_score`. It keeps the legacy/simple score intact while adding archetype-based, scenario-weighted scores.

N.P.E.M. uses:

- core archetypes for headline rankings
- labelled overlay cohorts for analytical views
- winsorized 0-100 normalization
- burden inversion for cost/pressure metrics
- scenario weights that must sum to 1.00
- provincial adjustment factor capped to +/- 5%
- confidence grades from coverage, recency, directness, and reliability
- provenance and citation records for every published score

Current N.P.E.M. outputs are deterministic demo estimates. GCI and DLI are transparent proxies until direct group-level source adapters land. Indigenous identity overlays require governance review and small-cell/suppression caution before public use.

## Public Beta Data Issue Reporting

During public beta, users can report suspected data issues from any page through the feedback form. Data issue submissions should include the page path and, when available, region, indicator, source, and period metadata.

Data issue reports do not automatically change published values. Admin review should check source freshness, raw observations, transformations, trust metadata, and any relevant N.P.E.M. provenance before marking a report fixed or closed.
