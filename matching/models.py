from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class Location:
    """Simple geographic coordinate."""
    latitude: float
    longitude: float


@dataclass
class Opportunity:
    """Represents an opportunity with additional context."""

    # mapping from skill name to weight (1-5)
    skills_weighted: Dict[str, int] = field(default_factory=dict)
    # mapping from category name to weight (1-5)
    categories_weighted: Dict[str, int] = field(default_factory=dict)
    # availability requirement expressed as mapping day -> list of blocks
    availability_required: Dict[str, List[str]] = field(default_factory=dict)
    # location coordinates for in-person work; None for remote
    location: Optional[Location] = None


@dataclass
class VolunteerProfile:
    """Represents a volunteer with preferences and proficiency."""

    skill_proficiency: Dict[str, str] = field(default_factory=dict)
    interest_level: Dict[str, str] = field(default_factory=dict)
    availability: Dict[str, List[str]] = field(default_factory=dict)
    preferred_location: Optional[Location] = None
    willing_to_remote: bool = True
    # skills a volunteer wants to learn/develop
    desired_skills: List[str] = field(default_factory=list)
    # testimonials from organizations
    testimonials: List[str] = field(default_factory=list)
    # links to portfolio items
    portfolio_urls: List[str] = field(default_factory=list)


@dataclass
class OrganizationProfile:
    """Public-facing information about an organization."""

    organization_id: str
    mission: str = ""
    testimonials: List[str] = field(default_factory=list)
    gallery_urls: List[str] = field(default_factory=list)
    opportunities: List[str] = field(default_factory=list)


@dataclass
class LearningResource:
    """External resource for learning a specific skill."""

    skill_name: str
    url: str


@dataclass
class SkillEndorsement:
    """Endorsement of a volunteer's skill by an organization."""

    volunteer_id: str
    organization_id: str
    opportunity_id: str
    skill_name: str
    endorsement_date: datetime
    endorsement_strength: int = 1


@dataclass
class Badge:
    """Represents a badge that can be awarded to a volunteer."""

    name: str
    description: str
    image_url: str


@dataclass
class VolunteerBadge:
    """A badge awarded to a volunteer."""

    volunteer_id: str
    badge_name: str
    award_date: datetime


@dataclass
class Conversation:
    """Represents a private conversation between participants."""

    conversation_id: str
    participant_ids: List[str]


@dataclass
class Message:
    """Individual message within a conversation."""

    conversation_id: str
    sender_id: str
    content: str
    timestamp: datetime


@dataclass
class WorkspaceTask:
    """Task item within an opportunity workspace."""

    description: str
    completed: bool = False


@dataclass
class WorkspaceFile:
    """File uploaded to a workspace."""

    name: str
    url: str


@dataclass
class Workspace:
    """Collaboration space for an accepted application."""

    application_id: str
    notes: str = ""
    tasks: List[WorkspaceTask] = field(default_factory=list)
    files: List[WorkspaceFile] = field(default_factory=list)


@dataclass
class CompletionRecord:
    """Record of a volunteer completing an opportunity."""

    volunteer_id: str
    organization_id: str
    opportunity_id: str
    hours: int
    metrics: Dict[str, int] = field(default_factory=dict)
    skills: List[str] = field(default_factory=list)
    location: Optional[Location] = None
    completion_date: datetime = field(default_factory=datetime.utcnow)


@dataclass
class OrganizationImpact:
    """Aggregated impact metrics for an organization."""

    organization_id: str
    total_hours: int
    opportunities_completed: int
    volunteer_count: int
    metrics: Dict[str, int]


@dataclass
class VolunteerImpact:
    """Summary of a volunteer's contributions."""

    volunteer_id: str
    total_hours: int
    opportunities_completed: int


@dataclass
class PlatformInsights:
    """High level metrics for the entire platform."""

    volunteer_count: int
    organization_count: int
    opportunity_count: int
    total_hours: int
    top_skills: Dict[str, int]
    geographic_distribution: Dict[str, int]


@dataclass
class ForumCategory:
    """A discussion category on the platform."""

    category_id: str
    name: str


@dataclass
class ForumPost:
    """A forum post created by a user."""

    post_id: str
    category_id: str
    author_id: str
    title: str
    content: str
    timestamp: datetime
    upvotes: int = 0
    downvotes: int = 0


@dataclass
class ForumReply:
    """A reply to a forum post."""

    reply_id: str
    post_id: str
    author_id: str
    content: str
    timestamp: datetime
    upvotes: int = 0
    downvotes: int = 0
