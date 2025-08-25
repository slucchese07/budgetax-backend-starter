from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import engine, SessionLocal, get_db
from ..models import Base
from ..models import Account  # if you want to seed a default account

router = APIRouter()

@router.post("/init")
def init(db: Session = Depends(get_db)):
    # Create tables (no-op if they already exist)
    Base.metadata.create_all(bind=engine)

    # Optional: seed a default account if none exist
    existing = db.query(Account).first()
    if not existing:
        acc = Account(name="Main Account", institution="Cloud", owner_key="user1")
        db.add(acc)
        db.commit()
        db.refresh(acc)
        return {"status": "created", "account_id": acc.id}

    return {"status": "ok", "account_id": existing.id}
