# Product Spec

Everyday Economy is a map-first economic dashboard that translates official economic data into everyday cost-of-living signals.

The MVP is Canada-first and organized around:

- Map-first exploration by province, territory, and later CMA/city.
- Plain-English translation of economic indicators.
- Sticky leaderboards for groceries, inflation, housing, gas, jobs, affordability, and movers.
- Source transparency on every card, chart, and endpoint.

The first product screen should answer: where is life getting more expensive fastest, what is driving it, and how does my region compare?

## Phase 4 Additions

The product now includes a first personal layer:

- account auth scaffolding
- saved regions watchlist
- user preferences persistence
- auth-aware sidebar/topbar behavior

Public dashboard pages remain usable without login.

## Phase 5 Additions

Everyday Economy now supports:

- personal alert rules on saved regions
- in-app notifications and read state
- monthly region report generation and history
- notification preferences for in-app/email/report toggles

This phase is deterministic and source-aware (no forecast or AI report writing).

## Phase 6 Additions

The platform now includes an operations control layer:

- admin status overview
- source health operations
- ingestion and job run history
- safe manual job triggers
- data quality review workflow
- feature flag management
- admin audit logs

## Phase 7 Additions

The platform is now prepared for staging and production hardening:

- Supabase Auth is the production identity path.
- Demo auth remains local-only and is disabled in production.
- Backend JWT verification protects account and admin APIs.
- Admin roles come from the local database.
- Email delivery supports disabled, console, and Resend-ready modes.
- CORS and rate limiting are environment-configured.
- Deployment, backup/restore, and security checklist documentation is in place.

## Phase 8 Additions

Everyday Economy now has a dedicated modern UI polish phase:

- clear/glass visual system
- blue primary brand colour with cyan and green accents
- MUI theme infrastructure
- improved light and dark mode styling
- generated landing hero visual
- polished dashboard, map, leaderboard, account, and admin surfaces
- restrained motion and improved focus states
- design system documentation

Deployment/public beta work is now Phase 9.

## Phase 9 Additions

Phase 9 prepares Everyday Economy for a controlled staging environment and public beta readiness:

- provider-neutral staging deployment runbook
- Vercel-style frontend deployment settings
- Docker-backed FastAPI deployment settings
- managed Postgres/PostGIS and Redis setup notes
- Supabase Auth staging setup and admin promotion flow
- first staging data-load command sequence
- staging QA checklist
- backup/restore checklist
- security checklist

Phase 9 is not a new feature phase. It exists to prove the product works outside localhost before public beta users are invited.

## Phase 10 Additions

Everyday Economy now includes the National Personal Economic Model, abbreviated N.P.E.M.:

- archetype and overlay group metadata
- N.P.E.M. variable dictionary
- baseline, housing stress, and income strength scenarios
- winsorized normalization service
- confidence grading
- provincial adjustment factor
- score provenance and citations
- N.P.E.M. API endpoints
- N.P.E.M. dashboard, methodology, compare, group, and provenance pages

Current N.P.E.M. values are deterministic demo/estimated scaffold data. The model architecture is in place, but production source adapters and governance review are still required before public ranking claims.

## Phase 11 Additions

Everyday Economy now includes a public beta readiness layer:

- beta status messaging across core pages
- in-app feedback and data issue reporting
- admin feedback triage
- public help, FAQ, methodology, data source, and known limitation pages
- changelog and release notes pages
- public beta checklist documentation
- clearer onboarding and empty-state language for outside users

Phase 11 does not add major scoring or product features. It exists to make the platform understandable, supportable, and ready for feedback from people who were not part of the build process.
