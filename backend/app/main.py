# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Budgetax API", version="0.1.0")

# CORS (relax now; lock down later to your app’s origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Startup (optional) -------------------------------------------------------
# If init_db exists, run it on boot to ensure tables exist.
try:
    from .db import init_db  # type: ignore

    @app.on_event("startup")
    def _startup() -> None:
        try:
            init_db()
        except Exception:
            # OK if tables already exist or DB isn’t reachable during build
            pass
except Exception:
    # If .db or init_db is missing, just continue.
    pass


# --- Health -------------------------------------------------------------------
@app.get("/ping")
def ping():
    return {"ok": True}

@app.get("/healthz")
def healthz():
    return {"ok": True}


# --- Routers ------------------------------------------------------------------
# Import each router defensively so a missing file doesn’t crash the app.
try:
    from .routers import admin  # /admin/*
    app.include_router(admin.router)
except Exception:
    pass

try:
    from .routers import assets
    app.include_router(assets.router)
except Exception:
    pass

try:
    from .routers import auth
    app.include_router(auth.router)
except Exception:
    pass

try:
    from .routers import expenses
    app.include_router(expenses.router)
except Exception:
    pass

try:
    from .routers import income
    app.include_router(income.router)
except Exception:
    pass

try:
    from .routers import invoices
    app.include_router(invoices.router)
except Exception:
    pass

try:
    from .routers import liabilities
    app.include_router(liabilities.router)
except Exception:
    pass

try:
    from .routers import transactions
    app.include_router(transactions.router)
except Exception:
    pass