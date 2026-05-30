# Feedback System

Phase 11 adds an in-app feedback loop for public beta users.

## User Flow

Users can open the feedback dialog from the floating feedback button. The form captures:

- feedback type
- optional rating
- message
- optional email for logged-out users
- current page path
- safe browser/page metadata

Feedback types:

- `bug`
- `data_issue`
- `confusing`
- `feature_request`
- `design_feedback`
- `general`

## Data Issue Flow

Use `data_issue` when a user is questioning a number, source, period, confidence grade, or methodology note. Metadata may include:

- `region`
- `indicator`
- `source`
- `period`

The feedback system should not collect sensitive personal information.

## Backend

Public endpoint:

- `POST /feedback`

Admin endpoints:

- `GET /admin/feedback`
- `PUT /admin/feedback/{feedback_id}`

Admin statuses:

- `new`
- `reviewed`
- `planned`
- `fixed`
- `closed`

Status changes create admin audit log entries.

## Admin Review

Admins review submissions at `/admin/feedback`. Data issues should be checked against:

- source freshness
- raw observations
- transformation and calculation logic
- trust metadata
- N.P.E.M. provenance where applicable

Closing feedback should mean the item was reviewed and either fixed, documented, or intentionally rejected.
