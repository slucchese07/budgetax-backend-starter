from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import List

from ..core.security import api_key_guard
from ..db import SessionLocal
from .. import models, schemas

router = APIRouter(prefix="/invoices", tags=["invoices"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.InvoiceOut)
def create_invoice(payload: schemas.InvoiceIn, _: bool = Depends(api_key_guard), db: Session = Depends(get_db)):
    invoice = models.Invoice(
        client_name=payload.client_name,
        description=payload.description,
        amount=payload.amount,
        issued_date=payload.issued_date,
        due_date=payload.due_date,
        status=payload.status,
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice

@router.get("/", response_model=List[schemas.InvoiceOut])
def list_invoices(_: bool = Depends(api_key_guard), db: Session = Depends(get_db)):
    return db.query(models.Invoice).all()

@router.get("/{invoice_id}", response_model=schemas.InvoiceOut)
def get_invoice(invoice_id: int, _: bool = Depends(api_key_guard), db: Session = Depends(get_db)):
    invoice = db.query(models.Invoice).get(invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

@router.put("/{invoice_id}", response_model=schemas.InvoiceOut)
def update_invoice(invoice_id: int, payload: schemas.InvoiceIn, _: bool = Depends(api_key_guard), db: Session = Depends(get_db)):
    invoice = db.query(models.Invoice).get(invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    for key, value in payload.dict().items():
        setattr(invoice, key, value)
    db.commit()
    db.refresh(invoice)
    return invoice

@router.delete("/{invoice_id}", response_model=schemas.Message)
def delete_invoice(invoice_id: int, _: bool = Depends(api_key_guard), db: Session = Depends(get_db)):
    invoice = db.query(models.Invoice).get(invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    db.delete(invoice)
    db.commit()
    return {"message": "Invoice deleted"}
