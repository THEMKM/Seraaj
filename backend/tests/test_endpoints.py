from fastapi.testclient import TestClient
from app.main import app
from app.db import init_db

client = TestClient(app)


def setup_module():
    init_db()


def test_auth_register_login_and_me():
    resp = client.post(
        "/auth/register",
        json={"email": "a@example.com", "password": "pw", "role": "VOLUNTEER"},
    )
    assert resp.status_code == 200
    token = resp.json()["access_token"]

    login = client.post(
        "/auth/login",
        json={"email": "a@example.com", "password": "pw"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    me = client.get("/auth/users/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["email"] == "a@example.com"


def test_full_flow():
    # register org admin
    resp = client.post(
        "/auth/register",
        json={"email": "org@example.com", "password": "pw", "role": "ORG_ADMIN"},
    )
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    # create org
    org = client.post(
        "/org",
        json={"name": "Org", "description": "desc"},
        headers=headers,
    )
    assert org.status_code == 200
    org_id = org.json()["id"]
    # create opportunity
    opp = client.post(
        f"/opportunity/org/{org_id}",
        json={
            "title": "Opp",
            "description": "desc",
            "skills_required": ["python"],
            "min_hours": 1,
            "start_date": "2025-01-01",
            "end_date": "2025-01-02",
            "is_remote": True,
            "status": "OPEN",
        },
        headers=headers,
    )
    assert opp.status_code == 200
    opp_id = opp.json()["id"]

    # volunteer signup
    vol = client.post(
        "/auth/register",
        json={"email": "vol@example.com", "password": "pw", "role": "VOLUNTEER"},
    )
    vol_token = vol.json()["access_token"]
    vheaders = {"Authorization": f"Bearer {vol_token}"}
    # create profile
    profile = client.put(
        "/volunteer/profile",
        json={
            "user_id": client.get("/auth/users/me", headers=vheaders).json()["id"],
            "full_name": "Vol Name",
            "skills": ["python"],
            "interests": ["design"],
            "languages": ["en"],
            "location_country": "US",
            "location_city": "NYC",
            "availability_hours": 5,
        },
        headers=vheaders,
    )
    assert profile.status_code == 200

    # apply
    application = client.post(
        f"/application/{opp_id}/apply",
        json={},
        headers=vheaders,
    )
    assert application.status_code == 200
    app_id = application.json()["id"]

    # recognition stub
    rec = client.post(f"/recognition/{app_id}", headers=headers)
    assert rec.status_code == 200
    assert "png_url" in rec.json()
