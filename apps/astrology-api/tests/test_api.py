from datetime import date, time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["ayanamsa"] == "lahiri"

def test_exact_chart_returns_nine_grahas():
    response = client.post("/v1/charts/calculate", json={
        "full_name":"Test Person","date_of_birth":"1990-01-01","birth_time":"12:00:00","birth_time_precision":"exact",
        "birthplace_label":"Delhi, India","latitude":28.6139,"longitude":77.2090,"timezone":"Asia/Kolkata"
    })
    assert response.status_code == 200
    payload=response.json()
    assert len(payload["grahas"]) == 9
    assert payload["ascendant"] is not None

def test_unknown_time_rejects_fake_time():
    response = client.post("/v1/charts/unknown-time", json={
        "full_name":"Test Person","date_of_birth":"1990-01-01","birth_time":"12:00:00","birth_time_precision":"unknown",
        "birthplace_label":"Delhi, India","latitude":28.6139,"longitude":77.2090,"timezone":"Asia/Kolkata"
    })
    assert response.status_code == 422
