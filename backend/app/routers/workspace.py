from __future__ import annotations
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from ..db import get_session
from ..models import Workspace
from .dependencies import get_current_user

router = APIRouter(prefix="/workspace", tags=["workspace"])


@router.get("/{app_id}", response_model=Workspace)
def get_workspace(
    app_id: str,
    session: Session = Depends(get_session),
    user=Depends(get_current_user),
) -> Workspace:
    ws = session.exec(
        select(Workspace).where(Workspace.application_id == UUID(app_id))
    ).first()
    if not ws:
        ws = Workspace(application_id=UUID(app_id))
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
    ws = session.exec(
        select(Workspace).where(Workspace.application_id == UUID(app_id))
    ).first()
    if not ws:
        ws = Workspace(application_id=UUID(app_id))
        session.add(ws)
    for field, val in ws_in.model_dump(exclude={"id", "application_id"}).items():
        setattr(ws, field, val)
    session.add(ws)
    session.commit()
    session.refresh(ws)
    return ws
