from fastapi import Depends, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from .config import settings

# This defines an API-key security scheme for Swagger
api_key_scheme = APIKeyHeader(name="X-API-Key", auto_error=False, description="Enter your API key")

async def api_key_guard(x_api_key: str | None = Depends(api_key_scheme)):
    if not x_api_key or x_api_key != settings.api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
    return True
