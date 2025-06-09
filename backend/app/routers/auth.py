import os
from fastapi import APIRouter

SECRET_KEY: str = os.getenv("SECRET_KEY", "changeme")

router = APIRouter()

@router.get("/health")
async def health_check() -> dict[str, str]:
    """Simple endpoint to verify router is loaded."""
    return {"status": "ok"}
