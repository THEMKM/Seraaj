from faker import Faker
from sqlmodel import Session, select

from app.routers.auth import get_password_hash

from app.db import engine, init_db
from app.models import (
    User,
    UserRole,
    VolunteerProfile,
    Organization,
    Opportunity,
    Application,
    OpportunityStatus,
    ApplicationStatus,
)
from app.services.embedding import embed
from random import sample, randint, choice

fake = Faker()

SKILLS = ["python", "javascript", "excel", "design", "marketing", "writing"]


def create_demo_accounts(session: Session) -> None:
    """Create predefined accounts for each user role."""
    demo_users = [
        ("volunteer@example.com", UserRole.VOLUNTEER),
        ("orgadmin@example.com", UserRole.ORG_ADMIN),
        ("superadmin@example.com", UserRole.SUPERADMIN),
    ]
    for email, role in demo_users:
        user = User(
            email=email,
            hashed_password=get_password_hash("pass123"),
            role=role,
        )
        session.add(user)
    session.commit()


def create_users(session: Session, count: int = 500) -> list[User]:
    users = []
    for _ in range(count):
        user = User(
            email=fake.unique.email(),
            hashed_password=get_password_hash("seed"),
            role=UserRole.VOLUNTEER,
        )
        session.add(user)
        users.append(user)
    session.commit()
    for user in users:
        session.refresh(user)
    return users


def create_profiles(session: Session, users: list[User]):
    for user in users:
        profile = VolunteerProfile(
            user_id=user.id,
            full_name=fake.name(),
            skills=sample(SKILLS, k=3),
            interests=sample(SKILLS, k=2),
            languages=["en"],
            location_city=fake.city(),
            location_country=fake.country(),
            availability_hours=randint(1, 10),
        )
        profile.embedding = embed(" ".join(profile.skills or []))
        session.add(profile)
    session.commit()


def create_orgs(
    session: Session, admins: list[User] | None = None, count: int = 20
) -> list[Organization]:
    """Create organizations owned by actual ORG_ADMIN users."""

    admins = admins or session.exec(
        select(User).where(User.role == UserRole.ORG_ADMIN)
    ).all()
    if not admins:
        raise ValueError("No ORG_ADMIN users available for organization owners")

    orgs = []
    for _ in range(count):
        owner = choice(admins)
        org = Organization(
            name=fake.company(),
            description=fake.bs(),
            website=fake.url(),
            owner_id=owner.id,
        )
        session.add(org)
        orgs.append(org)

    session.commit()
    for org in orgs:
        session.refresh(org)
    return orgs


def create_opportunities(session: Session, orgs: list[Organization], count: int = 200) -> list[Opportunity]:
    opps = []
    for _ in range(count):
        org = choice(orgs)
        opp = Opportunity(
            org_id=org.id,
            title=fake.job(),
            description=fake.text(),
            skills_required=sample(SKILLS, k=3),
            min_hours=randint(1, 10),
            start_date=fake.date_this_year(),
            end_date=fake.date_between(start_date="today", end_date="+30d"),
            is_remote=True,
            status=OpportunityStatus.OPEN,
        )
        opp.embedding = embed(opp.description)
        session.add(opp)
        opps.append(opp)
    session.commit()
    for opp in opps:
        session.refresh(opp)
    return opps


def create_applications(session: Session, users: list[User], opps: list[Opportunity], count: int = 1000):
    for _ in range(count):
        user = choice(users)
        opp = choice(opps)
        application = Application(
            volunteer_id=user.id,
            opportunity_id=opp.id,
            status=ApplicationStatus.PENDING,
        )
        session.add(application)
    session.commit()


def seed_demo_data():
    init_db()
    with Session(engine) as session:
        create_demo_accounts(session)
        users = create_users(session)
        create_profiles(session, users)
        admins = session.exec(select(User).where(User.role == UserRole.ORG_ADMIN)).all()
        orgs = create_orgs(session, admins=admins)
        opps = create_opportunities(session, orgs)
        create_applications(session, users, opps)
    print("Seed complete")


seed = seed_demo_data  # backwards compatibility


if __name__ == "__main__":
    seed_demo_data()
