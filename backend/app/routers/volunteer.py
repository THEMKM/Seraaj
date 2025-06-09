from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..db import get_session
from ..models import VolunteerProfile
from uuid import UUID
from .dependencies import get_current_user, require_role

router = APIRouter(prefix="/volunteer", tags=["volunteer"])


@router.put("/profile", response_model=VolunteerProfile)
def upsert_profile(
    profile: VolunteerProfile,
    session: Session = Depends(get_session),
    user=Depends(require_role("VOLUNTEER")),
) -> VolunteerProfile:
    profile.user_id = UUID(str(profile.user_id))
    existing = session.get(VolunteerProfile, profile.user_id)
    if existing:
        for field, value in profile.dict(exclude_unset=True).items():
            setattr(existing, field, value)
        session.add(existing)
    else:
        session.add(profile)
    session.commit()
    session.refresh(profile if not existing else existing)
    return profile if not existing else existing
