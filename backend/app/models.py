from __future__ import annotations
from datetime import datetime, date
from typing import List, Dict
from uuid import UUID, uuid4

import enum
import sqlalchemy
from pgvector.sqlalchemy import Vector
from pydantic import EmailStr, ConfigDict
from sqlmodel import Field, SQLModel


class UserRole(str, enum.Enum):
    VOLUNTEER = "VOLUNTEER"
    ORG_ADMIN = "ORG_ADMIN"
    SUPERADMIN = "SUPERADMIN"


class OpportunityStatus(str, enum.Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class ApplicationStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: EmailStr = Field(index=True, unique=True)
    hashed_password: str
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class VolunteerProfile(SQLModel, table=True):
    user_id: UUID = Field(foreign_key="user.id", primary_key=True)
    full_name: str
    skills: List[str] = Field(sa_column=sqlalchemy.Column(sqlalchemy.JSON))
    interests: List[str] = Field(sa_column=sqlalchemy.Column(sqlalchemy.JSON))
    languages: List[str] = Field(sa_column=sqlalchemy.Column(sqlalchemy.JSON))
    skill_proficiency: Dict[str, str] = Field(
        sa_column=sqlalchemy.Column(sqlalchemy.JSON), default_factory=dict
    )
    desired_skills: List[str] = Field(
        sa_column=sqlalchemy.Column(sqlalchemy.JSON), default_factory=list
    )
    location_city: str | None
    location_country: str
    location_lat: float | None = None
    location_lng: float | None = None
    availability_hours: int
    embedding: list[float] | None = Field(
        sa_column=sqlalchemy.Column(Vector(768), index=True, nullable=True),
        default=None,
    )

    model_config = ConfigDict(from_attributes=True)


class Organization(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    owner_id: UUID = Field(foreign_key="user.id")
    name: str
    description: str
    website: str | None

    model_config = ConfigDict(from_attributes=True)


class Opportunity(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    org_id: UUID = Field(foreign_key="organization.id")
    title: str
    description: str
    embedding: list[float] | None = Field(
        sa_column=sqlalchemy.Column(Vector(768), index=True, nullable=True),
        default=None,
    )
    skills_weighted: Dict[str, int] = Field(
        sa_column=sqlalchemy.Column(sqlalchemy.JSON), default_factory=dict
    )
    categories_weighted: Dict[str, int] = Field(
        sa_column=sqlalchemy.Column(sqlalchemy.JSON), default_factory=dict
    )
    availability_required: Dict[str, List[str]] = Field(
        sa_column=sqlalchemy.Column(sqlalchemy.JSON), default_factory=dict
    )
    skills_required: List[str] = Field(sa_column=sqlalchemy.Column(sqlalchemy.JSON))
    min_hours: int
    start_date: date
    end_date: date
    is_remote: bool = True
    status: OpportunityStatus

    model_config = ConfigDict(from_attributes=True)


class Application(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    volunteer_id: UUID = Field(foreign_key="user.id")
    opportunity_id: UUID = Field(foreign_key="opportunity.id")
    status: ApplicationStatus
    match_score: float | None = None
    applied_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(from_attributes=True)


class Conversation(SQLModel, table=True):
    """Conversation between participants."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    participant_ids: list[UUID] = Field(
        sa_column=sqlalchemy.Column(sqlalchemy.JSON)
    )

    model_config = ConfigDict(from_attributes=True)


class Message(SQLModel, table=True):
    """Single message in a conversation."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversation.id")
    sender_id: UUID = Field(foreign_key="user.id")
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(from_attributes=True)


class Workspace(SQLModel, table=True):
    """Collaboration workspace for an application."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    application_id: UUID = Field(foreign_key="application.id", unique=True)
    notes: str | None = ""
    tasks: list[dict] = Field(
        default_factory=list,
        sa_column=sqlalchemy.Column(sqlalchemy.JSON, default="[]"),
    )
    files: list[dict] = Field(
        default_factory=list,
        sa_column=sqlalchemy.Column(sqlalchemy.JSON, default="[]"),
    )

    model_config = ConfigDict(from_attributes=True)


class ForumPost(SQLModel, table=True):
    """Discussion post."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    author_id: UUID = Field(foreign_key="user.id")
    title: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    upvotes: int = 0
    downvotes: int = 0

    model_config = ConfigDict(from_attributes=True)


class ForumReply(SQLModel, table=True):
    """Reply to a post."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    post_id: UUID = Field(foreign_key="forumpost.id")
    author_id: UUID = Field(foreign_key="user.id")
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    upvotes: int = 0
    downvotes: int = 0

    model_config = ConfigDict(from_attributes=True)


class AnalyticsRecord(SQLModel, table=True):
    """Impact analytics record."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    volunteer_id: UUID = Field(foreign_key="user.id")
    organization_id: UUID = Field(foreign_key="organization.id")
    opportunity_id: UUID = Field(foreign_key="opportunity.id")
    hours: int
    metrics: dict = Field(
        default_factory=dict,
        sa_column=sqlalchemy.Column(sqlalchemy.JSON, default="{}"),
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(from_attributes=True)
