from fastapi.testclient import TestClient
from app.main import app
from app.db import init_db

client = TestClient(app)


def setup_module():
    init_db()


def _auth_header(email: str, role: str = "VOLUNTEER"):
    resp = client.post(
        "/auth/register", json={"email": email, "password": "pw", "role": role}
    )
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_conversation_and_forum_workflow():
    h1 = _auth_header("v1@example.com")
    h2 = _auth_header("v2@example.com")

    uid2 = client.get("/auth/me", headers=h2).json()["id"]
    conv = client.post(
        "/conversation",
        json={"participant_ids": [uid2]},
        headers=h1,
    )
    assert conv.status_code == 200
    cid = conv.json()["id"]

    msg = client.post(
        f"/conversation/{cid}/message",
        json={"content": "hello"},
        headers=h1,
    )
    assert msg.status_code == 200

    msgs = client.get(f"/conversation/{cid}/messages", headers=h2)
    assert len(msgs.json()) == 1

    # forum
    post = client.post(
        "/forum/post",
        json={"title": "Hi", "content": "all"},
        headers=h1,
    )
    pid = post.json()["id"]
    reply = client.post(
        f"/forum/post/{pid}/reply",
        json={"content": "welcome"},
        headers=h2,
    )
    assert reply.status_code == 200

    # analytics record
    org_h = _auth_header("org@example.com", role="ORG_ADMIN")
    org = client.post("/org", json={"name": "Org", "description": "d"}, headers=org_h)
    org_id = org.json()["id"]
    opp = client.post(
        f"/opportunity/org/{org_id}",
        json={
            "title": "O",
            "description": "d",
            "skills_required": ["x"],
            "min_hours": 1,
            "start_date": "2025-01-01",
            "end_date": "2025-01-02",
            "is_remote": True,
            "status": "OPEN",
        },
        headers=org_h,
    )
    opp_id = opp.json()["id"]
    rec = client.post(
        "/analytics/record",
        json={
            "volunteer_id": client.get("/auth/me", headers=h1).json()["id"],
            "organization_id": org_id,
            "opportunity_id": opp_id,
            "hours": 1,
        },
        headers=h1,
    )
    assert rec.status_code == 200
