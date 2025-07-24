import datetime

from app.matching import compute_match_scores, celery_app
from app.db import init_db, engine
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


def test_compute_match_scores_async(monkeypatch):
    """Task executed via Celery updates Application.match_score."""
    init_db()
    celery_app.conf.task_always_eager = True

    with Session(engine) as session:
        user = User(email="async@example.com", hashed_password="x", role=UserRole.VOLUNTEER)
        session.add(user)
        session.commit()
        session.refresh(user)

        profile = VolunteerProfile(
            user_id=user.id,
            full_name="Async",
            skills=["python"],
            interests=["data"],
            languages=["en"],
            location_country="US",
            location_city="X",
            availability_hours=5,
        )

        org = User(email="orgasync@example.com", hashed_password="x", role=UserRole.ORG_ADMIN)
        session.add(org)
        session.commit()
        session.refresh(org)

        opportunity = Opportunity(
            org_id=org.id,
            title="OppAsync",
            description="desc",
            skills_required=["python"],
            min_hours=1,
            start_date=datetime.date(2025, 1, 1),
            end_date=datetime.date(2025, 1, 2),
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

    result = compute_match_scores.delay()
    assert result.get() == 1

    with Session(engine) as session:
        app_db = session.exec(select(Application)).first()
        assert app_db.match_score is not None

