import uuid
from fastapi.testclient import TestClient
import os
from app.main import app
from app.db import init_db

client = TestClient(app)


def setup_module():
    os.environ.setdefault("SECRET_KEY", "dev-secret")
    init_db()


from jose import jwt

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
ALGORITHM = "HS256"


def _auth_header(email: str, role: str = "VOLUNTEER") -> tuple[dict, str]:
    resp = client.post(
        "/auth/register", json={"email": email, "password": "pw", "role": role}
    )
    token = resp.json()["access_token"]
    user_id = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])["sub"]
    return {"Authorization": f"Bearer {token}"}, user_id


def test_application_created_successfully():
    """Volunteer can apply to an open opportunity."""
    org_h, _ = _auth_header("org-new@example.com", role="ORG_ADMIN")
    org = client.post("/org", json={"name": "ONew", "description": "d"}, headers=org_h)
    org_id = org.json()["id"]
    opp = client.post(
        f"/opportunity/org/{org_id}",
        json={
            "title": "TT",
            "description": "d",
            "skills_required": ["x"],
            "skills_weighted": {"x": 5},
            "categories_weighted": {"general": 1},
            "availability_required": {"mon": ["am"]},
            "min_hours": 1,
            "start_date": "2025-01-01",
            "end_date": "2025-01-02",
            "is_remote": True,
            "status": "OPEN",
        },
        headers=org_h,
    )
    opp_id = opp.json()["id"]
    vol_h, v_id = _auth_header("vol-new@example.com")
    client.put(
        "/volunteer/profile",
        json={
            "user_id": v_id,
            "full_name": "Name",
            "skills": ["x"],
            "interests": [],
            "languages": ["en"],
            "skill_proficiency": {"x": "expert"},
            "desired_skills": ["python"],
            "location_country": "US",
            "location_city": "A",
            "location_lat": 0.0,
            "location_lng": 0.0,
            "availability_hours": 5,
        },
        headers=vol_h,
    )
    resp = client.post(f"/application/{opp_id}/apply", json={}, headers=vol_h)
    assert resp.status_code == 200
    data = resp.json()
    assert data["volunteer_id"] == v_id
    assert data["opportunity_id"] == opp_id


def test_update_status_and_list_apps():
    org_headers, _ = _auth_header("org2@example.com", role="ORG_ADMIN")
    org = client.post("/org", json={"name": "O2", "description": "d"}, headers=org_headers)
    org_id = org.json()["id"]
    opp = client.post(
        f"/opportunity/org/{org_id}",
        json={
            "title": "T",
            "description": "d",
            "skills_required": ["x"],
            "skills_weighted": {"x": 5},
            "categories_weighted": {"general": 1},
            "availability_required": {"mon": ["am"]},
            "min_hours": 1,
            "start_date": "2025-01-01",
            "end_date": "2025-01-02",
            "is_remote": True,
            "status": "OPEN",
        },
        headers=org_headers,
    )
    opp_id = opp.json()["id"]
    vol_headers, vol_id = _auth_header("v2@example.com")
    profile = client.put(
        "/volunteer/profile",
        json={
            "user_id": vol_id,
            "full_name": "Name",
            "skills": ["x"],
            "interests": [],
            "languages": ["en"],
            "skill_proficiency": {"x": "expert"},
            "desired_skills": ["python"],
            "location_country": "US",
            "location_city": "B",
            "location_lat": 0.0,
            "location_lng": 0.0,
            "availability_hours": 5,
        },
        headers=vol_headers,
    )
    app_resp = client.post(
        f"/application/{opp_id}/apply",
        json={},
        headers=vol_headers,
    )
    assert app_resp.status_code == 200
    assert app_resp.json()["volunteer_id"] == vol_id
    assert app_resp.json()["opportunity_id"] == opp_id
    app_id = app_resp.json()["id"]
    upd = client.post(
        f"/application/{app_id}/status",
        json={"status": "ACCEPTED"},
        headers=org_headers,
    )
    assert upd.status_code == 200
    assert upd.json()["status"] == "ACCEPTED"
    apps = client.get(f"/application/org/{org_id}", headers=org_headers)
    assert len(apps.json()) == 1


def test_apply_closed_opportunity():
    """Applying to a CLOSED opportunity should fail."""
    org_h, _ = _auth_header("orgclosed@example.com", role="ORG_ADMIN")
    org = client.post("/org", json={"name": "OC", "description": "d"}, headers=org_h)
    org_id = org.json()["id"]
    closed_opp = client.post(
        f"/opportunity/org/{org_id}",
        json={
            "title": "T3",
            "description": "d",
            "skills_required": ["x"],
            "skills_weighted": {"x": 5},
            "categories_weighted": {"general": 1},
            "availability_required": {"mon": ["am"]},
            "min_hours": 1,
            "start_date": "2025-01-01",
            "end_date": "2025-01-02",
            "is_remote": True,
            "status": "CLOSED",
        },
        headers=org_h,
    )
    opp_id = closed_opp.json()["id"]

    vol_h, uid = _auth_header("volclosed@example.com")
    resp = client.post(
        f"/application/{opp_id}/apply",
        json={},
        headers=vol_h,
    )
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Opportunity closed"


def test_duplicate_application_rejected():
    org_headers, _ = _auth_header("org3@example.com", role="ORG_ADMIN")
    org = client.post("/org", json={"name": "O3", "description": "d"}, headers=org_headers)
    org_id = org.json()["id"]
    opp = client.post(
        f"/opportunity/org/{org_id}",
        json={
            "title": "T2",
            "description": "d",
            "skills_required": ["x"],
            "skills_weighted": {"x": 5},
            "categories_weighted": {"general": 1},
            "availability_required": {"mon": ["am"]},
            "min_hours": 1,
            "start_date": "2025-01-01",
            "end_date": "2025-01-02",
            "is_remote": True,
            "status": "OPEN",
        },
        headers=org_headers,
    )
    opp_id = opp.json()["id"]
    vol_headers, uid = _auth_header("v3@example.com")
    client.put(
        "/volunteer/profile",
        json={
            "user_id": uid,
            "full_name": "Name",
            "skills": ["x"],
            "interests": [],
            "languages": ["en"],
            "skill_proficiency": {"x": "expert"},
            "desired_skills": ["python"],
            "location_country": "US",
            "location_city": "C",
            "location_lat": 0.0,
            "location_lng": 0.0,
            "availability_hours": 5,
        },
        headers=vol_headers,
    )
    first = client.post(
        f"/application/{opp_id}/apply",
        json={"status": "PENDING"},
        headers=vol_headers,
    )
    assert first.status_code == 200
    dup = client.post(
        f"/application/{opp_id}/apply",
        json={"status": "PENDING"},
        headers=vol_headers,
    )
    assert dup.status_code == 400
    assert dup.json()["detail"] == "Already applied"

