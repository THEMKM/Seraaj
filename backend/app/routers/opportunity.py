from __future__ import annotations
from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from ..db import get_session
from ..models import Opportunity, OpportunityStatus
from .dependencies import require_role

router = APIRouter(prefix="/opportunity", tags=["opportunity"])


@router.post("/org/{org_id}", response_model=Opportunity)
def create_opportunity(org_id: str, opp: Opportunity, session: Session = Depends(get_session), user=Depends(require_role("ORG_ADMIN"))):
    opp.org_id = org_id
    session.add(opp)
    session.commit()
    session.refresh(opp)
    return opp


@router.get("/search", response_model=List[Opportunity])
def search_opportunity(session: Session = Depends(get_session)):
    return session.exec(select(Opportunity).where(Opportunity.status == OpportunityStatus.OPEN)).all()
