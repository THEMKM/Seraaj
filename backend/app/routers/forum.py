from __future__ import annotations
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, SQLModel

from ..db import get_session
from ..models import ForumPost, ForumReply
from .dependencies import get_current_user

router = APIRouter(prefix="/forum", tags=["forum"])


class PostCreate(SQLModel):
    title: str
    content: str


@router.post("/post", response_model=ForumPost)
def create_post(
    post_in: PostCreate,
    session: Session = Depends(get_session),
    user=Depends(get_current_user),
) -> ForumPost:
    post = ForumPost(
        author_id=user.id,
        title=post_in.title,
        content=post_in.content,
    )
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


@router.get("/post", response_model=List[ForumPost])
def list_posts(session: Session = Depends(get_session)) -> List[ForumPost]:
    return session.exec(select(ForumPost)).all()


@router.get("/post/{post_id}", response_model=ForumPost)
def get_post(post_id: str, session: Session = Depends(get_session)) -> ForumPost:
    post = session.get(ForumPost, UUID(post_id))
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


class ReplyCreate(SQLModel):
    content: str


@router.post("/post/{post_id}/reply", response_model=ForumReply)
def add_reply(
    post_id: str,
    rep_in: ReplyCreate,
    session: Session = Depends(get_session),
    user=Depends(get_current_user),
) -> ForumReply:
    post = session.get(ForumPost, UUID(post_id))
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    reply = ForumReply(
        post_id=post.id,
        author_id=user.id,
        content=rep_in.content,
    )
    session.add(reply)
    session.commit()
    session.refresh(reply)
    return reply


@router.get("/post/{post_id}/replies", response_model=List[ForumReply])
def list_replies(post_id: str, session: Session = Depends(get_session)) -> List[ForumReply]:
    return session.exec(
        select(ForumReply).where(ForumReply.post_id == UUID(post_id))
    ).all()
