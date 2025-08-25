from fastapi import APIRouter
from sqlalchemy.orm import Session
from ..database import SessionLocal, engine
from ..models import Base, Account

router = APIRouter()

@router.post("/admin/init")
def admin_init():
    # create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    # seed a default account once
    with SessionLocal() as db:
        if not db.query(Account).first():
            acc = Account(name="Main Account", institution="Cloud", owner_key="user1")
            db.add(acc)
            db.commit()

    return {"ok": True}
