from __future__ import annotations
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..db import get_session
from ..models import Application, Organization, Opportunity, Workspace
from .dependencies import get_current_user

router = APIRouter(prefix="/workspace", tags=["workspace"])


@router.get("/{app_id}", response_model=Workspace)
def get_workspace(
    app_id: str,
    session: Session = Depends(get_session),
    user=Depends(get_current_user),
) -> Workspace:
    application = session.get(Application, UUID(app_id))
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    opportunity = session.get(Opportunity, application.opportunity_id)
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    org = session.get(Organization, opportunity.org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    if user.id not in {application.volunteer_id, org.owner_id}:
        raise HTTPException(status_code=403, detail="Not authorized")

    ws = session.exec(
        select(Workspace).where(Workspace.application_id == application.id)
    ).first()
    if not ws:
        ws = Workspace(application_id=application.id)
        session.add(ws)
        session.commit()
        session.refresh(ws)
    return ws


@router.put("/{app_id}", response_model=Workspace)
def update_workspace(
    app_id: str,
    ws_in: Workspace,
    session: Session = Depends(get_session),
    user=Depends(get_current_user),
) -> Workspace:
    application = session.get(Application, UUID(app_id))
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    opportunity = session.get(Opportunity, application.opportunity_id)
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    org = session.get(Organization, opportunity.org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    if user.id not in {application.volunteer_id, org.owner_id}:
        raise HTTPException(status_code=403, detail="Not authorized")

    ws = session.exec(
        select(Workspace).where(Workspace.application_id == application.id)
    ).first()
    if not ws:
        ws = Workspace(application_id=application.id)
        session.add(ws)
    for field, val in ws_in.model_dump(exclude={"id", "application_id"}).items():
        setattr(ws, field, val)
    session.add(ws)
    session.commit()
    session.refresh(ws)
    return ws
