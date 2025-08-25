from fastapi import APIRouter
from ..database import SessionLocal, engine
from ..models import Base, Account

router = APIRouter(tags=["admin"])

@router.post("/admin/init")
def admin_init():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    # Seed one default account if none exists
    with SessionLocal() as db:
        if not db.query(Account).first():
            db.add(Account(name="Main Account", institution="Cloud", owner_key="user1"))
            db.commit()
    return {"ok": True}
