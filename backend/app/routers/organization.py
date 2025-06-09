from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..db import get_session
from ..models import Organization
from .dependencies import require_role

router = APIRouter(prefix="/org", tags=["organization"])


@router.post("", response_model=Organization)
def create_org(
    org: Organization,
    session: Session = Depends(get_session),
    user=Depends(require_role("ORG_ADMIN")),
) -> Organization:
    """Create an organization owned by the authenticated admin."""
    org.owner_id = user.id
    session.add(org)
    session.commit()
    session.refresh(org)
    return org
