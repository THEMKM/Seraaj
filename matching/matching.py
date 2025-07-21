"""Simple matching algorithm using skill weights and proficiency levels."""
from typing import Dict

from .models import Opportunity, VolunteerProfile

PROFICIENCY_POINTS: Dict[str, int] = {
    "beginner": 1,
    "intermediate": 2,
    "expert": 3,
}

INTEREST_POINTS: Dict[str, int] = {
    "low": 1,
    "medium": 2,
    "high": 3,
}


def score_opportunity(opportunity: Opportunity, volunteer: VolunteerProfile) -> float:
    """Return a normalized score between 0 and 1."""
    total = 0
    max_total = 0

    for skill, weight in opportunity.skills_weighted.items():
        max_total += weight * PROFICIENCY_POINTS["expert"]
        proficiency = volunteer.skill_proficiency.get(skill)
        if proficiency:
            points = PROFICIENCY_POINTS.get(proficiency.lower(), 0)
            total += weight * points

    for category, weight in opportunity.categories_weighted.items():
        max_total += weight * INTEREST_POINTS["high"]
        interest = volunteer.interest_level.get(category)
        if interest:
            points = INTEREST_POINTS.get(interest.lower(), 0)
            total += weight * points

    if max_total == 0:
        return 0.0
    return total / max_total
