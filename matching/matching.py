"""Simple matching algorithm using skill weights, availability, and location."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple

from .models import Location, Opportunity, VolunteerProfile

# scoring constants for proficiency and interest

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

# Weights used when combining different scoring components
SKILL_WEIGHT = 0.6
CATEGORY_WEIGHT = 0.1
AVAILABILITY_WEIGHT = 0.2
LOCATION_WEIGHT = 0.1


def _availability_score(required: Dict[str, List[str]], available: Dict[str, List[str]]) -> float:
    """Return fraction of required time blocks the volunteer can satisfy."""
    required_blocks = sum(len(v) for v in required.values())
    if required_blocks == 0:
        return 1.0
    satisfied = 0
    for day, blocks in required.items():
        avail_blocks = set(available.get(day, []))
        satisfied += len([b for b in blocks if b in avail_blocks])
    return satisfied / required_blocks


def _haversine_distance(loc1: Location, loc2: Location) -> float:
    """Compute the distance in kilometers between two points."""
    from math import radians, sin, cos, sqrt, atan2

    R = 6371.0
    lat1, lon1 = radians(loc1.latitude), radians(loc1.longitude)
    lat2, lon2 = radians(loc2.latitude), radians(loc2.longitude)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def _location_score(opportunity: Opportunity, volunteer: VolunteerProfile, radius_km: float = 50.0) -> float:
    """Return 1 if distance within radius or remote is allowed."""
    if opportunity.location is None or volunteer.willing_to_remote:
        return 1.0
    if volunteer.preferred_location is None:
        return 0.0
    distance = _haversine_distance(opportunity.location, volunteer.preferred_location)
    return 1.0 if distance <= radius_km else 0.0


def score_opportunity(opportunity: Opportunity, volunteer: VolunteerProfile) -> float:
    """Return a normalized score between 0 and 1 including context."""
    skill_total = 0.0
    skill_max = 0.0

    for skill, weight in opportunity.skills_weighted.items():
        skill_max += weight * PROFICIENCY_POINTS["expert"]
        proficiency = volunteer.skill_proficiency.get(skill)
        if proficiency:
            points = PROFICIENCY_POINTS.get(proficiency.lower(), 0)
            skill_total += weight * points

    category_total = 0.0
    category_max = 0.0
    for category, weight in opportunity.categories_weighted.items():
        category_max += weight * INTEREST_POINTS["high"]
        interest = volunteer.interest_level.get(category)
        if interest:
            points = INTEREST_POINTS.get(interest.lower(), 0)
            category_total += weight * points

    skill_score = skill_total / skill_max if skill_max else 0.0
    category_score = category_total / category_max if category_max else 0.0

    availability_score = _availability_score(
        opportunity.availability_required, volunteer.availability
    )
    location_score = _location_score(opportunity, volunteer)

    # weighted combination
    final_score = (
        SKILL_WEIGHT * skill_score
        + CATEGORY_WEIGHT * category_score
        + AVAILABILITY_WEIGHT * availability_score
        + LOCATION_WEIGHT * location_score
    )
    return max(0.0, min(1.0, final_score))


def recommend_opportunities(
    volunteer: VolunteerProfile, opportunities: Iterable[Opportunity], limit: int = 5
) -> List[Tuple[Opportunity, float]]:
    """Return top matching opportunities for a volunteer."""
    scored = [
        (opp, score_opportunity(opp, volunteer)) for opp in opportunities
    ]
    scored.sort(key=lambda pair: pair[1], reverse=True)
    return scored[:limit]


def recommend_volunteers(
    opportunity: Opportunity, volunteers: Iterable[VolunteerProfile], limit: int = 5
) -> List[Tuple[VolunteerProfile, float]]:
    """Return top matching volunteers for an opportunity."""
    scored = [
        (vol, score_opportunity(opportunity, vol)) for vol in volunteers
    ]
    scored.sort(key=lambda pair: pair[1], reverse=True)
    return scored[:limit]


@dataclass
class MatchFeedback:
    """Feedback for a completed match."""

    match_id: str
    rating: int  # 1-5
    comment: str = ""


class FeedbackStore:
    """In-memory store of feedback for demonstration purposes."""

    def __init__(self) -> None:
        self._data: List[MatchFeedback] = []

    def record(self, feedback: MatchFeedback) -> None:
        self._data.append(feedback)

    def average_rating(self) -> float:
        if not self._data:
            return 0.0
        return sum(f.rating for f in self._data) / len(self._data)


FEEDBACK_STORE = FeedbackStore()
