# Known Limitations

Everyday Economy is in public beta. The app is useful for exploring latest available economic signals, but several areas remain under active refinement.

## Data Coverage

- Some datasets may use seeded or demo fallback data when real source ingestion is incomplete.
- Data is latest available, not live second-by-second.
- Province and territory coverage is stronger than city-level coverage.
- Source freshness may differ by metric.

## N.P.E.M.

- N.P.E.M. scores are deterministic demo/estimated scaffold data until production source adapters and governance review are complete.
- Overlay cohorts can overlap and should not be interpreted as mutually exclusive population groups.
- Indigenous identity overlays require additional governance review before public analytical use.
- Small-cell, suppression, or proxy-heavy cases should be treated with lower confidence.

## Alerts and Reports

- Alerts evaluate against available backend data and may not fire until relevant data has been ingested or calculated.
- Email delivery may be disabled or console-only in staging.
- Monthly reports use deterministic templates, not AI-generated commentary.

## Accounts and Admin

- Production auth requires configured Supabase credentials.
- Admin promotion is manual through the database.
- Admin job triggers are intentionally limited to a safe whitelist.

## Feedback

Feedback and data issue reports are reviewed by admins. Submitting a report does not automatically change data or methodology.
