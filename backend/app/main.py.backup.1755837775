from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Budgetax API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
def healthz():
    return "ok"

from .routers import transactions, assets, auth, income, expenses, invoices

app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(assets.router)
app.include_router(income.router)
app.include_router(expenses.router)
app.include_router(invoices.router)
