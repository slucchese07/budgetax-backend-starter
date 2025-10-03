from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import admin
app.include_router(admin.router)

from .db import init_db
from .routers import (
    admin,          # if you want admin endpoints; otherwise remove this line
    assets,
    auth,
    expenses,
    income,
    invoices,
    liabilities,
    transactions,
)

app = FastAPI(title="Budgetax API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten later to your mobile/web origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def _startup():
    init_db()

@app.get("/ping")
def ping():
    return {"ok": True}

@app.get("/healthz")
def healthz():
    return {"ok": True}

# Routers (remove any you don't actually have)
try:
    app.include_router(admin.router)
except Exception:
    pass

app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(assets.router)
app.include_router(income.router)
app.include_router(expenses.router)
app.include_router(invoices.router)
app.include_router(liabilities.router)
