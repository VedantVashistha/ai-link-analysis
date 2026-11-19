from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_ssrf_blocked():
    res = client.post("/link-analysis", json={"url": "http://127.0.0.1:8000"})
    assert res.status_code == 400
    assert "forbidden" in res.json()["detail"].lower() or "blocked" in res.json()["detail"].lower()


def test_invalid_scheme():
    res = client.post("/link-analysis", json={"url": "ftp://example.com"})
    assert res.status_code == 400