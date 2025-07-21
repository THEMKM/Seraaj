from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional


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
