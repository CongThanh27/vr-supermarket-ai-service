from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)


def test_analyze_ping():
    # register/login to obtain token
    client.post("/auth/register", json={"username": "carl", "password": "pwd12345"})
    resp = client.post("/auth/login", data={"username": "carl", "password": "pwd12345"})
    token = resp.json()["access_token"]
    resp = client.get("/analyze/ping", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "analyze pong"


def test_dialogue_hello():
    resp = client.get("/dialogue/hello")
    assert resp.status_code == 200
    assert resp.json()["message"] == "hello anonymous"
