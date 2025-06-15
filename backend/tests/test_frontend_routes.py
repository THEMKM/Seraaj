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


def test_opportunity_detail_and_org_list():
    org_h = _auth_header("org3@example.com", role="ORG_ADMIN")
    org = client.post("/org", json={"name": "O3", "description": "d"}, headers=org_h)
    org_id = org.json()["id"]
    opp = client.post(
        f"/opportunity/org/{org_id}",
        json={
            "title": "T",
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

    detail = client.get(f"/opportunity/{opp_id}")
    assert detail.status_code == 200
    assert detail.json()["id"] == opp_id

    opps = client.get("/org/opportunities", headers=org_h)
    assert opps.status_code == 200
    assert any(o["id"] == opp_id for o in opps.json())


def test_my_apps_and_applicants():
    org_h = _auth_header("org4@example.com", role="ORG_ADMIN")
    org = client.post("/org", json={"name": "O4", "description": "d"}, headers=org_h)
    org_id = org.json()["id"]
    opp = client.post(
        f"/opportunity/org/{org_id}",
        json={
            "title": "T2",
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

    vol_h = _auth_header("vol3@example.com")
    uid = client.get("/auth/me", headers=vol_h).json()["id"]
    client.put(
        "/volunteer/profile",
        json={
            "user_id": uid,
            "full_name": "Name",
            "skills": ["x"],
            "interests": [],
            "languages": ["en"],
            "location_country": "US",
            "location_city": "B",
            "availability_hours": 5,
        },
        headers=vol_h,
    )
    client.post(
        f"/application/{opp_id}/apply",
        json={},
        headers=vol_h,
    )

    apps = client.get("/applications/me", headers=vol_h)
    assert apps.status_code == 200
    assert len(apps.json()) == 1

    applicants = client.get("/applicants", headers=org_h)
    assert applicants.status_code == 200
    assert len(applicants.json()) == 1
