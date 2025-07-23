# Seraaj Matching Prototype

This repository contains a minimal prototype illustrating how weighted skills,
volunteer proficiency, availability, and location can be used to compute a
match score between volunteers and opportunities. It also exposes simple
recommendation helpers and a feedback store.

## Usage

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

The algorithm considers weighted skills, interest categories, availability,
and proximity to produce a final score between 0 and 1.

### Learning Paths and Gamification

Additional helpers can suggest opportunities and external resources for a
volunteer's desired skills, store skill endorsements, and award badges.

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

You can create conversations between users and lightweight workspaces for
accepted applications.

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

Record completed opportunities and generate simple impact statements or platform insights.

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

Profiles can now store testimonials and portfolios. A lightweight forum service
allows community discussion.

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

