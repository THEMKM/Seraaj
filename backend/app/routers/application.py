from __future__ import annotations
from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from ..db import get_session
from ..models import Application
from .dependencies import require_role

router = APIRouter(prefix="/application", tags=["application"])


@router.post("/{opp_id}/apply", response_model=Application)
def apply(opp_id: str, application: Application, session: Session = Depends(get_session), user=Depends(require_role("VOLUNTEER"))):
    application.opportunity_id = opp_id
    session.add(application)
    session.commit()
    session.refresh(application)
    return application


@router.get("/org/{org_id}", response_model=List[Application])
def list_applications(org_id: str, session: Session = Depends(get_session), user=Depends(require_role("ORG_ADMIN"))):
    from ..models import Opportunity
    return session.exec(
        select(Application).join(Opportunity).where(Opportunity.org_id == org_id)
    ).all()
