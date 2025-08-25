from fastapi import APIRouter
from sqlalchemy.orm import Session
from ..database import SessionLocal, engine
from ..models import Base, Account

router = APIRouter()

@router.post("/admin/init")
def admin_init():  Base.metadata.create_all(bind=engine)
from fastapi import APIRouter
from sqlalchemy.orm import Session
from ..database import SessionLocal, engine
from ..models import Base, Account

router = APIRouter()

@router.post("/admin/init")
def admin_init():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    # Seed a default account once
    db: Session = SessionLocal()
    try:
        exists = db.query(Account).first()
        if not exists:
            acc = Account(name="Main Account", institution="Cloud", owner_key="user1")
            db.add(acc)
            db.commit()
        return {"ok": True}
    finally:
        db.close()
