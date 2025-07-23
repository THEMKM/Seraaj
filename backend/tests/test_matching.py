from app.db import init_db, engine
from app.matching import compute_match_scores
from app.models import (
    VolunteerProfile,
    Opportunity,
    Application,
    User,
    UserRole,
    OpportunityStatus,
    ApplicationStatus,
)
from sqlmodel import Session, select
from datetime import date


def test_matching_empty_db():
    init_db()
    assert compute_match_scores() == 0


def test_matching_with_data():
    """Ensure a volunteer is matched to an opportunity when both exist."""
    init_db()
    with Session(engine) as session:
        user = User(email="v@example.com", hashed_password="x", role=UserRole.VOLUNTEER)
        session.add(user)
        session.commit()
        session.refresh(user)

        # create volunteer profile
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

        # organization admin user
        org = User(email="o@example.com", hashed_password="x", role=UserRole.ORG_ADMIN)
        session.add(org)
        session.commit()
        session.refresh(org)

        # create an opportunity for the organization
        opportunity = Opportunity(
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
        session.add(opportunity)
        session.commit()

        application = Application(
            volunteer_id=user.id,
            opportunity_id=opportunity.id,
            status=ApplicationStatus.PENDING,
        )
        session.add(application)
        session.commit()

    assert compute_match_scores() == 1


def test_matching_embeddings(monkeypatch):
    """When alg_v2 flag is on, embeddings drive the score."""
    from app.routers.settings import FLAGS

    init_db()
    monkeypatch.setitem(FLAGS, "alg_v2", True)

    with Session(engine) as session:
        user = User(
            email="ve@example.com", hashed_password="x", role=UserRole.VOLUNTEER
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        profile = VolunteerProfile(
            user_id=user.id,
            full_name="V2",
            skills=["python"],
            interests=[],
            languages=["en"],
            location_country="US",
            location_city="Z",
            availability_hours=5,
            embedding=[1.0] + [0.0] * 767,
        )

        org = User(email="oe@example.com", hashed_password="x", role=UserRole.ORG_ADMIN)
        session.add(org)
        session.commit()
        session.refresh(org)

        opportunity = Opportunity(
            org_id=org.id,
            title="OppE",
            description="desc",
            skills_required=["python"],
            min_hours=1,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 1, 2),
            is_remote=True,
            status=OpportunityStatus.OPEN,
            embedding=[1.0] + [0.0] * 767,
        )
        session.add(profile)
        session.add(opportunity)
        session.commit()

        application = Application(
            volunteer_id=user.id,
            opportunity_id=opportunity.id,
            status=ApplicationStatus.PENDING,
        )
        session.add(application)
        session.commit()

    assert compute_match_scores() == 1
    with Session(engine) as session:
        app_db = session.exec(select(Application)).first()
        assert app_db.match_score == 1.0
