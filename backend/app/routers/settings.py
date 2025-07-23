from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..db import engine
from .dependencies import require_role
import os

router = APIRouter(prefix="/settings", tags=["settings"])

# simple in-memory feature flags
default_flags = {
    "alg_v2": False,
    "referrals": False,
    "i18n": False,
    "oauth_un": False,
}
FLAGS = {key: os.getenv(key.upper(), str(val)).lower() == "true" for key, val in default_flags.items()}

@router.get("/flags")
def get_flags(user=Depends(require_role("SUPERADMIN"))):
    return FLAGS

@router.post("/flags/{flag}")
def toggle_flag(flag: str, user=Depends(require_role("SUPERADMIN"))):
    if flag not in FLAGS:
        raise HTTPException(status_code=404, detail="flag not found")
    FLAGS[flag] = not FLAGS[flag]
    return {flag: FLAGS[flag]}

@router.get("/health")
def system_health(user=Depends(require_role("SUPERADMIN"))):
    db = True
    redis = True
    worker = True
    try:
        with Session(engine):
            pass
    except Exception:
        db = False
    # redis/workers would normally be checked via ping; stub True
    return {"db": db, "redis": redis, "worker": worker}
