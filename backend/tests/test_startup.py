import os
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.main import app
from app.db import init_db, engine
from app.models import User, UserRole


def test_startup_does_not_drop_tables(monkeypatch):
    # prepare db with existing row
    init_db()
    with Session(engine) as session:
        user = User(email="keep@example.com", hashed_password="pw", role=UserRole.VOLUNTEER)
        session.add(user)
        session.commit()
        uid = user.id

    # simulate production startup
    monkeypatch.setenv("APP_ENV", "prod")
    monkeypatch.setenv("RESET_ON_START", "false")
    with TestClient(app):
        pass

    # ensure row still exists
    with Session(engine) as session:
        assert session.get(User, uid) is not None
