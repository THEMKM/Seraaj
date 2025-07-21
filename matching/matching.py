"""Simple matching algorithm using skill weights, availability, and location."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Iterable, List, Optional, Tuple

from .models import (
    Badge,
    LearningResource,
    Location,
    Opportunity,
    SkillEndorsement,
    VolunteerBadge,
    VolunteerProfile,
)

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


class EndorsementStore:
    """Simple in-memory storage for skill endorsements."""

    def __init__(self) -> None:
        self._data: List[SkillEndorsement] = []

    def add(self, endorsement: SkillEndorsement) -> None:
        self._data.append(endorsement)

    def for_volunteer(self, volunteer_id: str) -> List[SkillEndorsement]:
        return [e for e in self._data if e.volunteer_id == volunteer_id]


ENDORSEMENT_STORE = EndorsementStore()


class BadgeStore:
    """In-memory store for awarded badges."""

    def __init__(self) -> None:
        self._data: List[VolunteerBadge] = []

    def award(self, badge: VolunteerBadge) -> None:
        self._data.append(badge)

    def for_volunteer(self, volunteer_id: str) -> List[VolunteerBadge]:
        return [b for b in self._data if b.volunteer_id == volunteer_id]


BADGE_STORE = BadgeStore()


HOUR_BADGES: Dict[int, Badge] = {
    10: Badge(
        name="10 Hours",
        description="Completed 10 volunteer hours",
        image_url="",
    ),
    50: Badge(
        name="50 Hours",
        description="Completed 50 volunteer hours",
        image_url="",
    ),
}

ENDORSEMENT_BADGE = Badge(
    name="Endorsed",
    description="Received first skill endorsement",
    image_url="",
)


def check_and_award_badges(volunteer_id: str, hours: int, endorsement_count: int) -> None:
    """Award badges based on hours and endorsements."""
    for threshold, badge in HOUR_BADGES.items():
        if hours >= threshold and badge.name not in [b.badge_name for b in BADGE_STORE.for_volunteer(volunteer_id)]:
            BADGE_STORE.award(
                VolunteerBadge(
                    volunteer_id=volunteer_id,
                    badge_name=badge.name,
                    award_date=datetime.utcnow(),
                )
            )

    if endorsement_count > 0 and ENDORSEMENT_BADGE.name not in [b.badge_name for b in BADGE_STORE.for_volunteer(volunteer_id)]:
        BADGE_STORE.award(
            VolunteerBadge(
                volunteer_id=volunteer_id,
                badge_name=ENDORSEMENT_BADGE.name,
                award_date=datetime.utcnow(),
            )
        )


def leaderboard_by_hours(volunteer_hours: Dict[str, int]) -> List[Tuple[str, int]]:
    """Return a simple leaderboard sorted by hours volunteered."""
    return sorted(volunteer_hours.items(), key=lambda p: p[1], reverse=True)


def suggest_learning_path(
    volunteer: VolunteerProfile,
    opportunities: Iterable[Opportunity],
    resources: Iterable[LearningResource],
    limit: int = 5,
) -> Tuple[List[Opportunity], List[LearningResource]]:
    """Suggest opportunities and resources to develop desired skills."""
    relevant_opps = [
        (opp, score_opportunity(opp, volunteer))
        for opp in opportunities
        if any(skill in volunteer.desired_skills for skill in opp.skills_weighted)
    ]
    relevant_opps.sort(key=lambda p: p[1], reverse=True)
    opps = [o for o, _ in relevant_opps[:limit]]
    res = [r for r in resources if r.skill_name in volunteer.desired_skills]
    return opps, res
