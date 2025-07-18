import uuid
from fastapi.testclient import TestClient
from app.main import app
from app.db import init_db

client = TestClient(app)


def setup_module():
    init_db()


def _auth_header(email: str, role: str = "VOLUNTEER"):
    resp = client.post("/auth/register", json={"email": email, "password": "pw", "role": role})
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_update_status_and_list_apps():
    org_headers = _auth_header("org2@example.com", role="ORG_ADMIN")
    org = client.post("/org", json={"name": "O2", "description": "d"}, headers=org_headers)
    org_id = org.json()["id"]
    opp = client.post(
        f"/opportunity/org/{org_id}",
        json={"title": "T", "description": "d", "skills_required": ["x"], "min_hours": 1, "start_date": "2025-01-01", "end_date": "2025-01-02", "is_remote": True, "status": "OPEN"},
        headers=org_headers,
    )
    opp_id = opp.json()["id"]
    vol_headers = _auth_header("v2@example.com")
    profile = client.put(
        "/volunteer/profile",
        json={
            "user_id": client.get("/auth/me", headers=vol_headers).json()["id"],
            "full_name": "Name",
            "skills": ["x"],
            "interests": [],
            "languages": ["en"],
            "location_country": "US",
            "location_city": "B", 
            "availability_hours": 5,
        },
        headers=vol_headers,
    )
    app_resp = client.post(
        f"/application/{opp_id}/apply",
        json={},
        headers=vol_headers,
    )
    app_id = app_resp.json()["id"]
    upd = client.post(f"/application/{app_id}/status", params={"status": "ACCEPTED"}, headers=org_headers)
    assert upd.status_code == 200
    assert upd.json()["status"] == "ACCEPTED"
    apps = client.get(f"/application/org/{org_id}", headers=org_headers)
    assert len(apps.json()) == 1


def test_apply_closed_opportunity():
    """Applying to a CLOSED opportunity should fail."""
    org_h = _auth_header("orgclosed@example.com", role="ORG_ADMIN")
    org = client.post("/org", json={"name": "OC", "description": "d"}, headers=org_h)
    org_id = org.json()["id"]
    closed_opp = client.post(
        f"/opportunity/org/{org_id}",
        json={
            "title": "T3",
            "description": "d",
            "skills_required": ["x"],
            "min_hours": 1,
            "start_date": "2025-01-01",
            "end_date": "2025-01-02",
            "is_remote": True,
            "status": "CLOSED",
        },
        headers=org_h,
    )
    opp_id = closed_opp.json()["id"]

    vol_h = _auth_header("volclosed@example.com")
    uid = client.get("/auth/me", headers=vol_h).json()["id"]
def test_duplicate_application_rejected():
    org_headers = _auth_header("org3@example.com", role="ORG_ADMIN")
    org = client.post("/org", json={"name": "O3", "description": "d"}, headers=org_headers)
    org_id = org.json()["id"]
    opp = client.post(
        f"/opportunity/org/{org_id}",
        json={"title": "T2", "description": "d", "skills_required": ["x"], "min_hours": 1,
             "start_date": "2025-01-01", "end_date": "2025-01-02", "is_remote": True, "status": "OPEN"},
        headers=org_headers,
    )
    opp_id = opp.json()["id"]
    vol_headers = _auth_header("v3@example.com")
    uid = client.get("/auth/me", headers=vol_headers).json()["id"]
    client.put(
        "/volunteer/profile",
        json={
            "user_id": uid,
            "full_name": "Name",
            "skills": ["x"],
            "interests": [],
            "languages": ["en"],
            "location_country": "US",
            "location_city": "C",
            "availability_hours": 5,
        },
        headers=vol_headers,
    )
    first = client.post(
        f"/application/{opp_id}/apply",
        json={"volunteer_id": uid, "opportunity_id": opp_id, "status": "PENDING"},
        headers=vol_headers,
    )
    assert first.status_code == 200
    dup = client.post(
        f"/application/{opp_id}/apply",
        json={"volunteer_id": uid, "opportunity_id": opp_id, "status": "PENDING"},
        headers=vol_headers,
    )
    assert dup.status_code == 400
    assert dup.json()["detail"] == "Already applied"

