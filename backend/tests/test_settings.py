from fastapi.testclient import TestClient
from app.main import app
from app.db import init_db

client = TestClient(app)


def setup_module():
    init_db()


def _superadmin_header():
    resp = client.post(
        "/auth/register",
        json={"email": "root@example.com", "password": "pw", "role": "SUPERADMIN"},
    )
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_toggle_flag_and_health():
    headers = _superadmin_header()
    flags = client.get("/settings/flags", headers=headers)
    assert flags.status_code == 200
    first = flags.json()["alg_v2"]
    toggle = client.post("/settings/flags/alg_v2", headers=headers)
    assert toggle.status_code == 200
    assert toggle.json()["alg_v2"] != first
    health = client.get("/settings/health", headers=headers)
    assert health.status_code == 200
    assert "db" in health.json()

