from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from typing import Optional
from datetime import datetime
from ..core.security import api_key_guard
from ..db import SessionLocal
from .. import models, schemas
from ..services.categorizer import apply_rules

router = APIRouter(prefix="/transactions", tags=["transactions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/import", response_model=schemas.Message)
def import_transactions(payload: schemas.TransactionImport, _: bool = Depends(api_key_guard), db: Session = Depends(get_db)):
    for item in payload.items:
        t = models.Transaction(
            account_id=item.account_id,
            posted_at=item.posted_at or datetime.utcnow(),
            description=item.description,
            amount=item.amount,
            currency=item.currency,
            category_id=item.category_id,
            deductible=bool(item.deductible) if item.deductible is not None else False,
            owner_key="tenant",  # replace with your tenant lookup
        )
        # Auto-categorise (simple rules)
        if t.category_id is None:
            name, deductible, ato_label = apply_rules(t.description)
            if name:
                # ensure category exists
                cat = db.scalar(select(models.Category).where(models.Category.name==name))
                if not cat:
                    cat = models.Category(name=name, ato_label=ato_label, deductible_default=bool(deductible))
                    db.add(cat); db.flush()
                t.category_id = cat.id
                if deductible is not None:
                    t.deductible = deductible
        db.add(t)
    db.commit()
    return {"message": "Imported"}

@router.get("/", response_model=list[schemas.TransactionOut])
def list_transactions(month: Optional[str] = Query(default=None, description="YYYY-MM"), _: bool = Depends(api_key_guard), db: Session = Depends(get_db)):
    q = select(models.Transaction)
    if month:
        y, m = month.split("-")
        start = datetime(int(y), int(m), 1)
        if m == "12":
            end = datetime(int(y)+1, 1, 1)
        else:
            end = datetime(int(y), int(m)+1, 1)
        q = q.where(models.Transaction.posted_at >= start, models.Transaction.posted_at < end)
    q = q.order_by(models.Transaction.posted_at.desc())
    return db.scalars(q).all()

@router.get("/tax-summary", response_model=schemas.TaxSummaryOut)
def tax_summary(fy: str = Query(..., description="e.g., 2024-25"), _: bool = Depends(api_key_guard), db: Session = Depends(get_db)):
    # naive FY window: 1 July to 30 June
    start_year = int(fy.split("-")[0])
    start = datetime(start_year, 7, 1)
    end = datetime(start_year+1, 7, 1)
    # Sum by ATO label for deductible expenses (amounts negative -> expenses)
    stmt = (
        select(models.Category.ato_label, func.sum(models.Transaction.amount))
        .join(models.Transaction, models.Transaction.category_id == models.Category.id)
        .where(models.Transaction.posted_at >= start, models.Transaction.posted_at < end, models.Transaction.deductible == True)
        .group_by(models.Category.ato_label)
    )
    rows = db.execute(stmt).all()
    totals = []
    for label, total in rows:
        if label is None: 
            label = "Unlabelled"
        # expenses are usually negative amounts
        value = float(total) * -1.0
        totals.append({"ato_label": label, "total": round(value, 2)})
    return {"fy_label": fy, "currency": "AUD", "totals": totals}
