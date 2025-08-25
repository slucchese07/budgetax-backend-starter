# Budgetax Backend Starter (FastAPI + Postgres)

A minimal backend to kickstart your **budgeting + tax deductions** app. It supports:
- Transactions import + categorisation (with deductible flags and ATO-like labels).
- Asset register with simple depreciation calculators (Diminishing Value / Prime Cost).
- Tax-year summary endpoint to total deductible categories.
- Simple API-key auth via `X-API-Key` header (so you can test fast without full auth).

> ⚠️ This is a *starter* and not tax advice. Validate all tax logic for your jurisdiction (ATO for AU).

## Quick Start (Docker)
1. Create a `.env` file at project root (same folder as `docker-compose.yml`):
```
API_KEY=dev-secret-key
POSTGRES_USER=budgetax
POSTGRES_PASSWORD=budgetax
POSTGRES_DB=budgetax
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL=postgresql+psycopg2://budgetax:budgetax@db:5432/budgetax
TZ=Australia/Sydney
```

2. Run:
```
docker compose up --build
```

3. Open docs: http://localhost:8000/docs  
   Use header: `X-API-Key: dev-secret-key`
