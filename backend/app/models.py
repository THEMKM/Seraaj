from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str

    volunteer_profile: Optional["VolunteerProfile"] = Relationship(back_populates="user")

class VolunteerProfile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    bio: Optional[str] = Field(default="")

    user: Optional[User] = Relationship(back_populates="volunteer_profile")
    applications: List["Application"] = Relationship(back_populates="volunteer")

class Organization(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None

    opportunities: List["Opportunity"] = Relationship(back_populates="organization")

class Opportunity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    organization_id: int = Field(foreign_key="organization.id")
    title: str
    description: str

    organization: Optional[Organization] = Relationship(back_populates="opportunities")
    applications: List["Application"] = Relationship(back_populates="opportunity")

class Application(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    opportunity_id: int = Field(foreign_key="opportunity.id")
    volunteer_id: int = Field(foreign_key="volunteerprofile.id")
    status: str = Field(default="pending")

    opportunity: Optional[Opportunity] = Relationship(back_populates="applications")
    volunteer: Optional[VolunteerProfile] = Relationship(back_populates="applications")
