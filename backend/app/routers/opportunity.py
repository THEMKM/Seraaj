from __future__ import annotations
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from uuid import UUID

from ..db import get_session
from ..models import Opportunity, OpportunityStatus, Organization
from sqlmodel import SQLModel
from datetime import date
from .dependencies import require_role

router = APIRouter(prefix="/opportunity", tags=["opportunity"])


@router.get("/{opp_id}", response_model=Opportunity)
def get_opportunity(
    opp_id: str,
    session: Session = Depends(get_session),
) -> Opportunity:
    """Return a single opportunity."""
    opp = session.get(Opportunity, UUID(opp_id))
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return opp


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
    org = session.get(Organization, UUID(org_id))
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    if org.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    opp = Opportunity(**opp_in.model_dump(), org_id=org.id)
    session.add(opp)
    session.commit()
    session.refresh(opp)
    return opp


@router.get("/search", response_model=List[Opportunity])
def search_opportunity(session: Session = Depends(get_session)):
    return session.exec(select(Opportunity).where(Opportunity.status == OpportunityStatus.OPEN)).all()
