from app.db import init_db, engine
from app.matching import compute_match_scores
from app.models import VolunteerProfile, Opportunity, Application, User, UserRole, OpportunityStatus, ApplicationStatus
from sqlmodel import Session
from datetime import date


def test_matching_empty_db():
    init_db()
    assert compute_match_scores() == 0


def test_matching_with_data():
    init_db()
    with Session(engine) as session:
        user = User(email="v@example.com", hashed_password="x", role=UserRole.VOLUNTEER)
        session.add(user)
        session.commit()
        session.refresh(user)
        profile = VolunteerProfile(
            user_id=user.id,
            full_name="V",
            skills=["python"],
            interests=["data"],
            languages=["en"],
            location_country="US",
            location_city="A",
            availability_hours=5,
        )
        org = User(email="o@example.com", hashed_password="x", role=UserRole.ORG_ADMIN)
        session.add(org)
        session.commit()
        session.refresh(org)
        organization = Opportunity(
            org_id=org.id,
            title="Opp",
            description="desc",
            skills_required=["python"],
            min_hours=1,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 1, 2),
            is_remote=True,
            status=OpportunityStatus.OPEN,
        )
        session.add(profile)
        session.add(organization)
        session.commit()
        application = Application(
            volunteer_id=user.id,
            opportunity_id=organization.id,
            status=ApplicationStatus.PENDING,
        )
        session.add(application)
        session.commit()
    assert compute_match_scores() == 1
