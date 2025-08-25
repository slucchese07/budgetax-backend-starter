# backend/app/routers/admin.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal, engine, get_db
from ..models import Base, Account  # adjust import names if your model is named differently
from ..schemas import Message
from ..auth import require_api_key  # this is the dependency you already use for X-API-Key

router = APIRouter()

@router.post("/init", response_model=Message, dependencies=[Depends(require_api_key)])
def init_database(db: Session = Depends(get_db)):
    """
    One-time initializer: creates tables and inserts a default account if none exists.
    Safe to re-run (it won't duplicate the default account).
    """
    # Create all tables (no-op if they already exist)
    Base.metadata.create_all(bind=engine)

    # Ensure at least one account exists (needed by transactions endpoints)
    existing = db.query(Account).first()
    if not existing:
        default = Account(name="Main Account", institution="Cloud", owner_key="user1")
        db.add(default)
        db.commit()

    return Message(message="DB initialized (tables ensured; default account present).")
