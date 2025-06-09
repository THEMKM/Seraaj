from fastapi import APIRouter, Depends

from .dependencies import require_role

router = APIRouter(prefix="/recognition", tags=["recognition"])

@router.post("/{app_id}")
def generate_card(app_id: str, user=Depends(require_role("ORG_ADMIN"))):
    # Stub implementation returning a fake PNG URL
    return {"png_url": f"https://example.com/recognition/{app_id}.png"}
