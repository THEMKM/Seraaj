"""Simple matching algorithm using skill weights, availability, and location."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4
from typing import Dict, Iterable, List, Optional, Tuple

from .models import (
    Badge,
    LearningResource,
    Location,
    Opportunity,
    OrganizationProfile,
    Conversation,
    Message,
    Workspace,
    WorkspaceFile,
    WorkspaceTask,
    SkillEndorsement,
    VolunteerBadge,
    VolunteerProfile,
    ForumCategory,
    ForumPost,
    ForumReply,
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


class MessagingService:
    """Simple in-memory messaging between users."""

    def __init__(self) -> None:
        self.conversations: Dict[str, Conversation] = {}
        self.messages: List[Message] = []

    def create_conversation(self, participant_ids: List[str]) -> str:
        conv_id = str(uuid4())
        self.conversations[conv_id] = Conversation(conv_id, participant_ids)
        return conv_id

    def send_message(self, conversation_id: str, sender_id: str, content: str) -> Message:
        if conversation_id not in self.conversations:
            raise ValueError("conversation does not exist")
        msg = Message(
            conversation_id=conversation_id,
            sender_id=sender_id,
            content=content,
            timestamp=datetime.utcnow(),
        )
        self.messages.append(msg)
        return msg

    def history(self, conversation_id: str) -> List[Message]:
        return [m for m in self.messages if m.conversation_id == conversation_id]


MESSAGING_SERVICE = MessagingService()


class WorkspaceStore:
    """In-memory store for opportunity workspaces."""

    def __init__(self) -> None:
        self._workspaces: Dict[str, Workspace] = {}

    def create_workspace(self, application_id: str) -> Workspace:
        ws = Workspace(application_id=application_id)
        self._workspaces[application_id] = ws
        return ws

    def get(self, application_id: str) -> Optional[Workspace]:
        return self._workspaces.get(application_id)

    def add_note(self, application_id: str, note: str) -> None:
        ws = self._workspaces.setdefault(application_id, Workspace(application_id))
        ws.notes += f"{note}\n"

    def add_task(self, application_id: str, description: str) -> None:
        ws = self._workspaces.setdefault(application_id, Workspace(application_id))
        ws.tasks.append(WorkspaceTask(description))

    def complete_task(self, application_id: str, index: int) -> None:
        ws = self._workspaces.get(application_id)
        if not ws or index >= len(ws.tasks):
            return
        ws.tasks[index].completed = True

    def add_file(self, application_id: str, name: str, url: str) -> None:
        ws = self._workspaces.setdefault(application_id, Workspace(application_id))
        ws.files.append(WorkspaceFile(name, url))


WORKSPACE_STORE = WorkspaceStore()


class AnalyticsService:
    """Compute impact reports and volunteer statements."""

    def __init__(self) -> None:
        self._completions: List[CompletionRecord] = []

    def record_completion(self, record: CompletionRecord) -> None:
        self._completions.append(record)

    def organization_report(self, organization_id: str) -> OrganizationImpact:
        relevant = [c for c in self._completions if c.organization_id == organization_id]
        total_hours = sum(c.hours for c in relevant)
        opps = {c.opportunity_id for c in relevant}
        volunteers = {c.volunteer_id for c in relevant}
        metrics: Dict[str, int] = {}
        for c in relevant:
            for k, v in c.metrics.items():
                metrics[k] = metrics.get(k, 0) + v
        return OrganizationImpact(
            organization_id=organization_id,
            total_hours=total_hours,
            opportunities_completed=len(opps),
            volunteer_count=len(volunteers),
            metrics=metrics,
        )

    def volunteer_statement(self, volunteer_id: str) -> VolunteerImpact:
        relevant = [c for c in self._completions if c.volunteer_id == volunteer_id]
        total_hours = sum(c.hours for c in relevant)
        opps = {c.opportunity_id for c in relevant}
        return VolunteerImpact(
            volunteer_id=volunteer_id,
            total_hours=total_hours,
            opportunities_completed=len(opps),
        )

    def platform_insights(self) -> PlatformInsights:
        total_hours = sum(c.hours for c in self._completions)
        volunteers = {c.volunteer_id for c in self._completions}
        organizations = {c.organization_id for c in self._completions}
        opportunities = {c.opportunity_id for c in self._completions}
        skills: Dict[str, int] = {}
        locations: Dict[str, int] = {}
        for c in self._completions:
            for s in c.skills:
                skills[s] = skills.get(s, 0) + 1
            if c.location:
                key = f"{c.location.latitude:.2f},{c.location.longitude:.2f}"
                locations[key] = locations.get(key, 0) + 1
        top_skills = dict(sorted(skills.items(), key=lambda p: p[1], reverse=True)[:5])
        return PlatformInsights(
            volunteer_count=len(volunteers),
            organization_count=len(organizations),
            opportunity_count=len(opportunities),
            total_hours=total_hours,
            top_skills=top_skills,
            geographic_distribution=locations,
        )

    def export_csv_for_org(self, organization_id: str, path: str) -> None:
        import csv

        report = self.organization_report(organization_id)
        with open(path, "w", newline="") as fh:
            writer = csv.writer(fh)
            writer.writerow([
                "organization_id",
                "total_hours",
                "opportunities_completed",
                "volunteer_count",
            ])
            writer.writerow(
                [
                    report.organization_id,
                    report.total_hours,
                    report.opportunities_completed,
                    report.volunteer_count,
                ]
            )
            for metric, value in report.metrics.items():
                writer.writerow([metric, value])

    def generate_certificate(self, volunteer_id: str, opportunity_id: str) -> str:
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        return f"Certificate: {volunteer_id} completed {opportunity_id} on {date_str}"


ANALYTICS_SERVICE = AnalyticsService()


class ForumService:
    """Simple discussion board management."""

    def __init__(self) -> None:
        self.categories: Dict[str, ForumCategory] = {}
        self.posts: Dict[str, ForumPost] = {}
        self.replies: List[ForumReply] = []

    def create_category(self, name: str) -> str:
        cid = str(uuid4())
        self.categories[cid] = ForumCategory(cid, name)
        return cid

    def create_post(
        self, category_id: str, author_id: str, title: str, content: str
    ) -> str:
        pid = str(uuid4())
        self.posts[pid] = ForumPost(
            pid,
            category_id,
            author_id,
            title,
            content,
            datetime.utcnow(),
        )
        return pid

    def add_reply(self, post_id: str, author_id: str, content: str) -> str:
        rid = str(uuid4())
        self.replies.append(
            ForumReply(rid, post_id, author_id, content, datetime.utcnow())
        )
        return rid

    def vote_post(self, post_id: str, up: bool = True) -> None:
        post = self.posts.get(post_id)
        if not post:
            return
        if up:
            post.upvotes += 1
        else:
            post.downvotes += 1

    def vote_reply(self, reply_id: str, up: bool = True) -> None:
        for reply in self.replies:
            if reply.reply_id == reply_id:
                if up:
                    reply.upvotes += 1
                else:
                    reply.downvotes += 1
                break

    def posts_by_author(self, author_id: str) -> List[ForumPost]:
        return [p for p in self.posts.values() if p.author_id == author_id]

    def posts_in_category(self, category_id: str) -> List[ForumPost]:
        return [p for p in self.posts.values() if p.category_id == category_id]

    def replies_for_post(self, post_id: str) -> List[ForumReply]:
        return [r for r in self.replies if r.post_id == post_id]


FORUM_SERVICE = ForumService()
