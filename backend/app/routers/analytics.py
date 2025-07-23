from __future__ import annotations
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlmodel import Session, select, SQLModel

from ..db import get_session
from ..models import AnalyticsRecord
from .dependencies import get_current_user

router = APIRouter(prefix="/analytics", tags=["analytics"])


class RecordCreate(SQLModel):
    volunteer_id: UUID
    organization_id: UUID
    opportunity_id: UUID
    hours: int
    metrics: dict = {}


@router.post("/record", response_model=AnalyticsRecord)
def create_record(
    rec_in: RecordCreate,
    session: Session = Depends(get_session),
    user=Depends(get_current_user),
) -> AnalyticsRecord:
    rec = AnalyticsRecord(**rec_in.model_dump())
    session.add(rec)
    session.commit()
    session.refresh(rec)
    return rec


@router.get("/volunteer/{vol_id}", response_model=List[AnalyticsRecord])
def records_for_volunteer(
    vol_id: str,
    session: Session = Depends(get_session),
) -> List[AnalyticsRecord]:
    return session.exec(
        select(AnalyticsRecord).where(AnalyticsRecord.volunteer_id == UUID(vol_id))
    ).all()


@router.get("/organization/{org_id}", response_model=List[AnalyticsRecord])
def records_for_org(
    org_id: str,
    session: Session = Depends(get_session),
) -> List[AnalyticsRecord]:
    return session.exec(
        select(AnalyticsRecord).where(AnalyticsRecord.organization_id == UUID(org_id))
    ).all()
