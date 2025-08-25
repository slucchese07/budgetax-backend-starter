from fastapi import FastAPI
from .db import init_db
from .routers import transactions, assets, auth, income, expenses, invoices

init_db()
app = FastAPI(title="Budgetax API", version="0.1.0")

app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(assets.router)
app.include_router(income.router)
app.include_router(expenses.router)
app.include_router(invoices.router)

@app.get("/healthz")
def healthz():
    return {"ok": True}

# Liabilities router
from .routers import liabilities
app.include_router(liabilities.router)

from .routers import liabilities
app.include_router(liabilities.router)
