# Seraaj Matching Prototype

This repository contains a minimal prototype illustrating how weighted skills
and volunteer proficiency can be used to compute a match score between
volunteers and opportunities.

## Usage

```python
from matching import Opportunity, VolunteerProfile, score_opportunity

opportunity = Opportunity(skills_weighted={"python": 5, "sql": 3},
                          categories_weighted={"data": 2})

volunteer = VolunteerProfile(
    skill_proficiency={"python": "expert", "sql": "intermediate"},
    interest_level={"data": "high"},
)

score = score_opportunity(opportunity, volunteer)
print(f"Match score: {score:.2f}")
```

The algorithm assigns points based on the organization's weight for each skill
and category and the volunteer's proficiency or interest level. The result is a
normalized score between 0 and 1.

## Messaging Prototype

The `chat` package contains a small FastAPI application demonstrating in-platform messaging between volunteers and organizations.

Run the server with:

```bash
uvicorn chat.server:app
```

Create a conversation and send messages via the HTTP API or connect to
`/ws/chat/{conversation_id}` using WebSocket for realtime updates.
