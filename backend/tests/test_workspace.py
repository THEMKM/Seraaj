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


def _create_opp(org_h):
    org = client.post("/org", json={"name": "OrgW", "description": "d"}, headers=org_h)
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
        headers=org_h,
    )
    return org_id, opp.json()["id"]


def _apply(vol_h, opp_id):
    uid = client.get("/auth/me", headers=vol_h).json()["id"]
    client.put(
        "/volunteer/profile",
        json={
            "user_id": uid,
            "full_name": "V",
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
    app_resp = client.post(f"/application/{opp_id}/apply", json={}, headers=vol_h)
    return app_resp.json()["id"]


def test_workspace_permissions():
    org_h = _auth_header("orgw@example.com", role="ORG_ADMIN")
    org_id, opp_id = _create_opp(org_h)

    vol_h = _auth_header("volw@example.com")
    app_id = _apply(vol_h, opp_id)

    other_vol_h = _auth_header("volunauth@example.com")

    # applicant can get and update
    get_resp = client.get(f"/workspace/{app_id}", headers=vol_h)
    assert get_resp.status_code == 200

    upd_resp = client.put(
        f"/workspace/{app_id}",
        json={"notes": "n", "tasks": [], "files": []},
        headers=vol_h,
    )
    assert upd_resp.status_code == 200
    assert upd_resp.json()["notes"] == "n"

    # org admin can access
    org_get = client.get(f"/workspace/{app_id}", headers=org_h)
    assert org_get.status_code == 200

    # other volunteer cannot
    bad_get = client.get(f"/workspace/{app_id}", headers=other_vol_h)
    assert bad_get.status_code == 403
    bad_upd = client.put(
        f"/workspace/{app_id}",
        json={"notes": "h"},
        headers=other_vol_h,
    )
    assert bad_upd.status_code == 403

