# Everyday Economy API

FastAPI service responsible for source ingestion, normalization, calculations, caching, and frontend-ready economic dashboard responses.

## Run locally

```bash
python -m uvicorn app.main:app --reload --app-dir apps/api --port 8000
```

OpenAPI docs are available at `/docs`.

## Ingestion commands

Run from the repository root:

```bash
PYTHONPATH=apps/api python -m app.jobs.refresh_all
PYTHONPATH=apps/api python -m app.jobs.ingest_statcan --dataset cpi
PYTHONPATH=apps/api python -m app.jobs.ingest_statcan --dataset gas
PYTHONPATH=apps/api python -m app.jobs.ingest_statcan --dataset labour
PYTHONPATH=apps/api python -m app.jobs.ingest_statcan --dataset food_prices
PYTHONPATH=apps/api python -m app.jobs.ingest_statcan --dataset bank_of_canada
PYTHONPATH=apps/api python -m app.jobs.calculate_baskets
PYTHONPATH=apps/api python -m app.jobs.build_leaderboards
```
