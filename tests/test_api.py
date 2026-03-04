from fastapi.testclient import TestClient
from app.api import app
from app.db.session import get_engine, Base

client = TestClient(app)


def setup_module(module):
    # ensure fresh database (PostgreSQL)
    engine = get_engine()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_register_and_login():
    # register first user
    resp = client.post(
        "/auth/register",
        json={"username": "alice", "password": "secret123"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["username"] == "alice"

    # login with correct credentials
    resp = client.post(
        "/auth/login",
        data={"username": "alice", "password": "secret123"},
    )
    assert resp.status_code == 200
    token = resp.json()["access_token"]

    # access protected endpoint
    resp = client.get("/health", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_login_failures():
    resp = client.post(
        "/auth/login",
        data={"username": "nonexist", "password": "x"},
    )
    assert resp.status_code == 401


def test_logout():
    # register and login again
    client.post(
        "/auth/register",
        json={"username": "bob", "password": "password1"},
    )
    resp = client.post(
        "/auth/login",
        data={"username": "bob", "password": "password1"},
    )
    token = resp.json()["access_token"]
    # logout
    resp = client.post("/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    # token should be revoked
    resp = client.get("/health", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 401
