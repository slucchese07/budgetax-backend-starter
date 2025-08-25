from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/liabilities", tags=["liabilities"])

@router.post("/", response_model=schemas.LiabilityOut)
def create_liability(liability: schemas.LiabilityIn, db: Session = Depends(get_db)):
    db_liability = models.Liability(**liability.dict())
    db.add(db_liability)
    db.commit()
    db.refresh(db_liability)
    return db_liability

@router.get("/", response_model=list[schemas.LiabilityOut])
def list_liabilities(db: Session = Depends(get_db)):
    return db.query(models.Liability).all()
