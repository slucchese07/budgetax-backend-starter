from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import date
from ..core.security import api_key_guard
from ..db import SessionLocal
from .. import models, schemas
from ..services.depreciation import build_schedule

router = APIRouter(prefix="/assets", tags=["assets"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.AssetOut)
def create_asset(payload: schemas.AssetIn, _: bool = Depends(api_key_guard), db: Session = Depends(get_db)):
    asset = models.Asset(
        name=payload.name,
        purchase_date=payload.purchase_date,
        cost=payload.cost,
        method=payload.method,
        effective_life_years=payload.effective_life_years,
        salvage_value=payload.salvage_value,
        owner_key="tenant",
    )
    db.add(asset); db.commit(); db.refresh(asset)
    return asset

@router.get("/", response_model=list[schemas.AssetOut])
def list_assets(_: bool = Depends(api_key_guard), db: Session = Depends(get_db)):
    return db.scalars(select(models.Asset)).all()

@router.post("/{asset_id}/schedule", response_model=list[schemas.DepreciationEntryOut])
def generate_schedule(asset_id: int, fy_start: int = Query(..., description="Start FY year, e.g., 2024 for 2024-25"), years: int = 5, _: bool = Depends(api_key_guard), db: Session = Depends(get_db)):
    asset = db.get(models.Asset, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    # Build in-memory schedule
    schedule = build_schedule(float(asset.cost), asset.method, asset.effective_life_years, float(asset.salvage_value), fy_start, years)
    # Persist rows (idempotency kept simple; production: upsert logic by fy_label)
    created = []
    for row in schedule:
        entry = models.DepreciationEntry(
            asset_id=asset.id,
            fy_label=row["fy_label"],
            opening_value=row["opening_value"],
            depreciation=row["depreciation"],
            closing_value=row["closing_value"],
        )
        db.add(entry); db.flush(); created.append(entry)
    db.commit()
    # Sort by FY
    return created
