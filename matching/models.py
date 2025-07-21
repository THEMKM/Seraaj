from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Opportunity:
    """Represents an opportunity with weighted required skills."""
    # mapping from skill name to weight (1-5)
    skills_weighted: Dict[str, int] = field(default_factory=dict)
    # mapping from category name to required interest weight (optional)
    categories_weighted: Dict[str, int] = field(default_factory=dict)

@dataclass
class VolunteerProfile:
    """Represents a volunteer with proficiency and interests."""
    # mapping from skill name to proficiency (beginner/intermediate/expert)
    skill_proficiency: Dict[str, str] = field(default_factory=dict)
    # mapping from category name to interest level (low/medium/high)
    interest_level: Dict[str, str] = field(default_factory=dict)
