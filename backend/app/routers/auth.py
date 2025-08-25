from fastapi import APIRouter, Depends
from ..core.security import api_key_guard

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/whoami")
def whoami(_: bool = Depends(api_key_guard)):
    return {"ok": True}
