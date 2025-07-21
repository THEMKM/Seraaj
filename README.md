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
