from __future__ import annotations
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from uuid import UUID

from ..db import get_session
from ..models import Application, ApplicationStatus, Opportunity, Organization
from .dependencies import require_role

router = APIRouter(prefix="/application", tags=["application"])
# Additional router for paths not under /application prefix
extra_router = APIRouter(tags=["application"])


@router.post("/{opp_id}/apply", response_model=Application)
def apply(
    opp_id: str,
    application: Application,
    session: Session = Depends(get_session),
    user=Depends(require_role("VOLUNTEER")),
) -> Application:
    application.opportunity_id = UUID(opp_id)
    application.volunteer_id = UUID(str(application.volunteer_id))
    session.add(application)
    session.commit()
    session.refresh(application)
    return application


@router.get("/org/{org_id}", response_model=List[Application])
def list_applications(
    org_id: str,
    session: Session = Depends(get_session),
    user=Depends(require_role("ORG_ADMIN")),
) -> List[Application]:
    from ..models import Opportunity
    return session.exec(
        select(Application).join(Opportunity).where(Opportunity.org_id == UUID(org_id))
    ).all()


@router.post("/{app_id}/status", response_model=Application)
def update_status(
    app_id: str,
    status: ApplicationStatus,
    session: Session = Depends(get_session),
    user=Depends(require_role("ORG_ADMIN")),
) -> Application:
    application = session.get(Application, UUID(app_id))
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    application.status = status
    session.add(application)
    session.commit()
    session.refresh(application)
    return application


# --- Extra frontend convenience endpoints ---

@extra_router.get("/applications/me", response_model=List[Application])
def my_applications(
    session: Session = Depends(get_session),
    user=Depends(require_role("VOLUNTEER")),
) -> List[Application]:
    """Return applications submitted by the authenticated volunteer."""
    return session.exec(
        select(Application).where(Application.volunteer_id == user.id)
    ).all()


@extra_router.get("/applicants", response_model=List[Application])
def list_applicants(
    session: Session = Depends(get_session),
    user=Depends(require_role("ORG_ADMIN")),
) -> List[Application]:
    """List applications for opportunities owned by the authenticated org admin."""
    org_ids = session.exec(
        select(Organization.id).where(Organization.owner_id == user.id)
    ).all()
    if not org_ids:
        return []
    return session.exec(
        select(Application)
        .join(Opportunity)
        .where(Opportunity.org_id.in_(org_ids))
    ).all()
