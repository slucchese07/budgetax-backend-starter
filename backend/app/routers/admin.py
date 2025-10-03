# backend/app/routers/admin.py
from fastapi import APIRouter
from ..db import SessionLocal, engine, Base
from ..models import Account

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/init")
def admin_init():
    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Seed one default account if none exists
    with SessionLocal() as db:
        if not db.query(Account).first():
            db.add(Account(name="Main Account", institution="Cloud", owner_key="user1"))
            db.commit()
    return {"ok": True}

@router.get("/ping")
def admin_ping():
    return {"ok": True}
