from __future__ import annotations
from datetime import datetime, date
from typing import List
from uuid import UUID, uuid4

import enum
import sqlalchemy
from pydantic import EmailStr
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


class VolunteerProfile(SQLModel, table=True):
    user_id: UUID = Field(foreign_key="user.id", primary_key=True)
    full_name: str
    skills: List[str] = Field(sa_column=sqlalchemy.Column(sqlalchemy.ARRAY(sqlalchemy.String)))
    interests: List[str] = Field(sa_column=sqlalchemy.Column(sqlalchemy.ARRAY(sqlalchemy.String)))
    languages: List[str] = Field(sa_column=sqlalchemy.Column(sqlalchemy.ARRAY(sqlalchemy.String)))
    location_city: str | None
    location_country: str
    availability_hours: int


class Organization(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    owner_id: UUID = Field(foreign_key="user.id")
    name: str
    description: str
    website: str | None


class Opportunity(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    org_id: UUID = Field(foreign_key="organization.id")
    title: str
    description: str
    skills_required: List[str] = Field(sa_column=sqlalchemy.Column(sqlalchemy.ARRAY(sqlalchemy.String)))
    min_hours: int
    start_date: date
    end_date: date
    is_remote: bool = True
    status: OpportunityStatus


class Application(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    volunteer_id: UUID = Field(foreign_key="user.id")
    opportunity_id: UUID = Field(foreign_key="opportunity.id")
    status: ApplicationStatus
    match_score: float | None = None
    applied_at: datetime = Field(default_factory=datetime.utcnow)
