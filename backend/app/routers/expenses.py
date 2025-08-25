from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
from typing import Optional

from ..core.security import api_key_guard
from ..db import SessionLocal
from .. import models, schemas

router = APIRouter(prefix="/transactions", tags=["transactions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def ensure_category(db: Session, name: str, ato_label: Optional[str] = None, deductible_default: bool = False) -> models.Category:
    cat = db.scalar(select(models.Category).where(models.Category.name == name))
    if not cat:
        cat = models.Category(name=name, ato_label=ato_label, deductible_default=deductible_default)
        db.add(cat); db.flush()
    return cat

def ensure_primary_account(db: Session) -> models.Account:
    acc = db.scalar(select(models.Account).where(models.Account.id == 1))
    if not acc:
        acc = models.Account(id=1, name="Primary", institution=None, owner_key="tenant")
        db.add(acc); db.flush()
    return acc

@router.post("/expense", response_model=schemas.TransactionOut, summary="Record Expense")
def add_expense(payload: schemas.ExpenseIn, _: bool = Depends(api_key_guard), db: Session = Depends(get_db)):
    """
    Create a single **expense** transaction.
    - Send a POSITIVE amount; we store it as negative.
    - Optional category_name (defaults to 'General').
    - deductible defaults to True.
    - account_id optional; defaults to primary account (id=1).
    """
    account_id = payload.account_id or ensure_primary_account(db).id
    cat = ensure_category(db, name=payload.category_name or "General", ato_label=payload.category_name or "General", deductible_default=True)

    t = models.Transaction(
        account_id=account_id,
        posted_at=payload.posted_at or datetime.utcnow(),
        description=payload.description,
        amount= -abs(payload.amount),  # store expenses negative
        currency=payload.currency,
        category_id=cat.id,
        deductible=bool(payload.deductible),
        owner_key="tenant",
    )
    db.add(t); db.commit(); db.refresh(t)
    return t
