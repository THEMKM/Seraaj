# Seraaj Volunteer Matching Platform

Seraaj is a demonstration project showing how to match volunteers to opportunities and manage collaboration around them.  It provides a full FastAPI backend, a React frontend, and a small matching library that can be used standalone.

Key features include:

- Weighted skill and interest matching with location and availability filters.
- Learning paths, endorsements, and badge awards for gamification.
- Messaging and lightweight workspaces for accepted applications.
- Impact analytics and certificate generation.
- Rich profiles with testimonials and a simple forum service.

The repository is organised as follows:

- `backend/` – FastAPI app and Alembic migrations.
- `frontend/` – Vite + React interface styled with Tailwind.
- `matching/` – Pure‑Python scoring algorithms and utilities.
- `docs/adr/` – Architecture decision records.

## Quickstart

Prerequisites: Docker and Node.js 18+.

```bash
make dev            # build and start backend, Postgres and Redis
make seed           # populate demo data (optional)
(cd frontend && npm install && npm run dev)
```

Everything can also be started with a single line:

```bash
docker compose up --build -d && docker compose exec backend python seed.py && (cd frontend && npm install && npm run dev)
```

Seeding happens automatically on startup when `SEED_DEMO_DATA=true` (set in `.env.example`), so running the script manually is optional.

Backend API runs on `http://localhost:8000` and the frontend on `http://localhost:5173`.

### Environment Setup

Copy `.env.example` to `.env` and adjust the values for your deployment:

```bash
cp .env.example .env
```

The default Postgres user and password are both `seraaj` as configured in
`docker-compose.yml`.

For local development you can instead start from `.env.sample`.
Both environment files include a `SECRET_KEY` entry. Ensure the same value is
used across them (the default is `dev-secret`) so that JWTs issued by the
backend can be verified.

## Usage Examples

```python
from matching import (
    Location,
    Opportunity,
    VolunteerProfile,
    score_opportunity,
    recommend_opportunities,
)

opportunity = Opportunity(
    skills_weighted={"python": 5, "sql": 3},
    categories_weighted={"data": 2},
    availability_required={"mon": ["am"]},
    location=Location(40.0, -75.0),
)

volunteer = VolunteerProfile(
    skill_proficiency={"python": "expert", "sql": "intermediate"},
    interest_level={"data": "high"},
    availability={"mon": ["am", "pm"]},
    preferred_location=Location(40.1, -75.1),
)

score = score_opportunity(opportunity, volunteer)
print(f"Match score: {score:.2f}")

# Recommend the best opportunities for the volunteer
recommended = recommend_opportunities(volunteer, [opportunity])
print(recommended)
```

The algorithm considers weighted skills, interest categories, availability and proximity to produce a final score between 0 and 1.

### Learning Paths and Gamification

```python
from matching import (
    LearningResource,
    suggest_learning_path,
    ENDORSEMENT_STORE,
    SkillEndorsement,
    check_and_award_badges,
    BADGE_STORE,
)
from datetime import datetime

# Recommend learning options
resources = [LearningResource("python", "https://example.com/python-course")]
opps, res = suggest_learning_path(volunteer, [opportunity], resources)

# Record an endorsement after opportunity completion
ENDORSEMENT_STORE.add(
    SkillEndorsement(
        volunteer_id="vol1",
        organization_id="org1",
        opportunity_id="opp1",
        skill_name="python",
        endorsement_date=datetime.utcnow(),
    )
)

# Award badges based on hours and endorsements
check_and_award_badges("vol1", hours=12, endorsement_count=1)
print(BADGE_STORE.for_volunteer("vol1"))
```

### Messaging and Workspaces

```python
from matching import MESSAGING_SERVICE, WORKSPACE_STORE

# Start a conversation
cid = MESSAGING_SERVICE.create_conversation(["vol1", "org1"])
MESSAGING_SERVICE.send_message(cid, "vol1", "Hello!")
print(MESSAGING_SERVICE.history(cid))

# Manage a workspace
ws = WORKSPACE_STORE.create_workspace("app1")
WORKSPACE_STORE.add_task("app1", "Submit ID check")
WORKSPACE_STORE.complete_task("app1", 0)
print(WORKSPACE_STORE.get("app1"))
```

### Impact Reporting and Analytics

```python
from matching import (
    CompletionRecord,
    ANALYTICS_SERVICE,
    OrganizationImpact,
)

# Record that a volunteer completed work
ANALYTICS_SERVICE.record_completion(
    CompletionRecord(
        volunteer_id="vol1",
        organization_id="org1",
        opportunity_id="opp1",
        hours=5,
        skills=["python"],
    )
)

# Fetch an organization impact report and export it
report = ANALYTICS_SERVICE.organization_report("org1")
print(report)
ANALYTICS_SERVICE.export_csv_for_org("org1", "org1_report.csv")

# Generate a volunteer certificate
certificate = ANALYTICS_SERVICE.generate_certificate("vol1", "opp1")
print(certificate)

# Get platform-wide insights
insights = ANALYTICS_SERVICE.platform_insights()
print(insights)
```

### Rich Profiles and Community Forums

```python
from matching import (
    VolunteerProfile,
    OrganizationProfile,
    FORUM_SERVICE,
)

# Add portfolio items and testimonials
volunteer.portfolio_urls.append("https://example.com/work1")
volunteer.testimonials.append("Great collaborator!")

org_profile = OrganizationProfile(
    organization_id="org1",
    mission="Save the world",
)
org_profile.testimonials.append("Amazing nonprofit")

# Create a forum thread
cat_id = FORUM_SERVICE.create_category("General")
post_id = FORUM_SERVICE.create_post(cat_id, "vol1", "Hello", "Nice to meet you")
FORUM_SERVICE.add_reply(post_id, "org1", "Welcome!")
FORUM_SERVICE.vote_post(post_id, up=True)
print(FORUM_SERVICE.replies_for_post(post_id))

reply_id = FORUM_SERVICE.add_reply(post_id, "vol1", "Thanks!")
FORUM_SERVICE.vote_reply(reply_id, up=True)
```

## Contributing

Pull requests are welcome. Please see `AGENTS.md` for the collaboration workflow and coding conventions.

## Testing

Ensure Docker is installed before running the test suite. The tests execute inside containers and will fail without Docker.

The backend uses a `SECRET_KEY` environment variable when issuing and decoding
JWTs. Tests require this to match the value in your `.env` or `.env.sample`
(default `dev-secret`).

```bash
make test
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

