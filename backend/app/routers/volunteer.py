from fastapi import APIRouter, Depends
from sqlmodel import Session

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
    profile.user_id = user.id
    existing = session.get(VolunteerProfile, profile.user_id)
    if existing:
        for field, value in profile.dict(exclude_unset=True, exclude={"user_id"}).items():
            setattr(existing, field, value)
        session.add(existing)
        session.commit()
        session.refresh(existing)
        return existing
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile
