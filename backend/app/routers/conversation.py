from __future__ import annotations
from typing import List
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, SQLModel

from ..db import get_session
from ..models import Conversation, Message, User
from .dependencies import get_current_user

router = APIRouter(prefix="/conversation", tags=["conversation"])


class ConversationCreate(SQLModel):
    participant_ids: List[UUID]


@router.post("", response_model=Conversation)
def create_conversation(
    conv_in: ConversationCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> Conversation:
    if user.id not in conv_in.participant_ids:
        conv_in.participant_ids.append(user.id)
    conv = Conversation(participant_ids=conv_in.participant_ids)
    session.add(conv)
    session.commit()
    session.refresh(conv)
    return conv


@router.get("", response_model=List[Conversation])
def list_conversations(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> List[Conversation]:
    return session.exec(
        select(Conversation).where(
            Conversation.participant_ids.contains([str(user.id)])
        )
    ).all()


@router.get("/{conv_id}", response_model=Conversation)
def get_conversation(
    conv_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> Conversation:
    conv = session.get(Conversation, UUID(conv_id))
    if not conv or str(user.id) not in [str(pid) for pid in conv.participant_ids]:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conv


class MessageCreate(SQLModel):
    content: str


@router.post("/{conv_id}/message", response_model=Message)
def send_message(
    conv_id: str,
    msg_in: MessageCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> Message:
    conv = session.get(Conversation, UUID(conv_id))
    if not conv or str(user.id) not in [str(pid) for pid in conv.participant_ids]:
        raise HTTPException(status_code=404, detail="Conversation not found")
    msg = Message(
        conversation_id=conv.id,
        sender_id=user.id,
        content=msg_in.content,
    )
    session.add(msg)
    session.commit()
    session.refresh(msg)
    return msg


@router.get("/{conv_id}/messages", response_model=List[Message])
def list_messages(
    conv_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> List[Message]:
    conv = session.get(Conversation, UUID(conv_id))
    if not conv or str(user.id) not in [str(pid) for pid in conv.participant_ids]:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return session.exec(
        select(Message).where(Message.conversation_id == conv.id)
    ).all()
