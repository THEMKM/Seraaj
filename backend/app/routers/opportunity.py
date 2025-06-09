from __future__ import annotations
from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from uuid import UUID

from ..db import get_session
from ..models import Opportunity, OpportunityStatus
from sqlmodel import SQLModel
from datetime import date
from .dependencies import require_role

router = APIRouter(prefix="/opportunity", tags=["opportunity"])


class OpportunityCreate(SQLModel):
    title: str
    description: str
    skills_required: List[str]
    min_hours: int
    start_date: date
    end_date: date
    is_remote: bool = True
    status: OpportunityStatus


@router.post("/org/{org_id}", response_model=Opportunity)
def create_opportunity(
    org_id: str,
    opp_in: OpportunityCreate,
    session: Session = Depends(get_session),
    user=Depends(require_role("ORG_ADMIN")),
) -> Opportunity:
    """Create an opportunity for the given organization."""
    opp = Opportunity(**opp_in.model_dump(), org_id=UUID(org_id))
    session.add(opp)
    session.commit()
    session.refresh(opp)
    return opp


@router.get("/search", response_model=List[Opportunity])
def search_opportunity(session: Session = Depends(get_session)):
    return session.exec(select(Opportunity).where(Opportunity.status == OpportunityStatus.OPEN)).all()
