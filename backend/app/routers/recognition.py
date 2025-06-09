import os
import time
import cloudinary
from cloudinary.utils import cloudinary_url, api_sign_request
from fastapi import APIRouter, Depends

from .dependencies import require_role

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME", "demo"),
    api_key=os.getenv("CLOUDINARY_API_KEY", "key"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET", "secret"),
)

router = APIRouter(prefix="/recognition", tags=["recognition"])

@router.post("/{app_id}")
def generate_card(app_id: str, user=Depends(require_role("ORG_ADMIN"))):
    """Return a signed Cloudinary upload URL and resulting PNG path."""
    if cloudinary.config().cloud_name == "demo":
        return {
            "upload_url": "https://example.com/upload",
            "png_url": f"https://example.com/{app_id}.png",
        }
    timestamp = int(time.time())
    params = {"public_id": f"seraaj/{app_id}", "timestamp": timestamp}
    signature = api_sign_request(params, cloudinary.config().api_secret)
    upload_url = (
        f"https://api.cloudinary.com/v1_1/{cloudinary.config().cloud_name}/image/upload"
        f"?public_id={params['public_id']}&timestamp={timestamp}&api_key={cloudinary.config().api_key}&signature={signature}"
    )
    png_url, _ = cloudinary_url(params["public_id"], format="png", secure=True)
    return {"upload_url": upload_url, "png_url": png_url}
