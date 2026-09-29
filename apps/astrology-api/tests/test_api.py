from fastapi.testclient import TestClient

from app.main import app
from app.models import GrahaPosition
from app.transits import parashari_drishti_events, sign_distance

client = TestClient(app)


def position(key: str, rashi: int) -> GrahaPosition:
    longitude = (rashi - 1) * 30.0 + 1.0
    return GrahaPosition(
        key=key,
        longitude=longitude,
        rashi=rashi,
        degree_in_rashi=1.0,
        nakshatra="Test",
        pada=1,
        retrograde=False,
    )


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["ayanamsa"] == "lahiri"
    assert response.json()["drishti_system"] == "parashari-full-sign"


def test_exact_chart_returns_nine_grahas():
    response = client.post(
        "/v1/charts/calculate",
        json={
            "full_name": "Test Person",
            "date_of_birth": "1990-01-01",
            "birth_time": "12:00:00",
            "birth_time_precision": "exact",
            "birthplace_label": "Delhi, India",
            "latitude": 28.6139,
            "longitude": 77.2090,
            "timezone": "Asia/Kolkata",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert len(payload["grahas"]) == 9
    assert payload["ascendant"] is not None


def test_unknown_time_rejects_fake_time():
    response = client.post(
        "/v1/charts/unknown-time",
        json={
            "full_name": "Test Person",
            "date_of_birth": "1990-01-01",
            "birth_time": "12:00:00",
            "birth_time_precision": "unknown",
            "birthplace_label": "Delhi, India",
            "latitude": 28.6139,
            "longitude": 77.2090,
            "timezone": "Asia/Kolkata",
        },
    )
    assert response.status_code == 422


def test_sign_distance_is_inclusive_and_wraps():
    assert sign_distance(1, 1) == 1
    assert sign_distance(1, 7) == 7
    assert sign_distance(12, 6) == 7


def test_mars_has_full_fourth_seventh_and_eighth_drishti():
    natal = [
        position("sun", 4),
        position("moon", 7),
        position("jupiter", 8),
        position("venus", 5),
    ]
    events = parashari_drishti_events(natal, [position("mars", 1)])
    assert {event["drishti_house"] for event in events} == {4, 7, 8}


def test_jupiter_and_saturn_special_full_drishti():
    natal = [
        position("sun", 5),
        position("moon", 9),
        position("mercury", 3),
        position("venus", 10),
    ]
    jupiter = parashari_drishti_events(natal, [position("jupiter", 1)])
    saturn = parashari_drishti_events(natal, [position("saturn", 1)])
    assert {event["drishti_house"] for event in jupiter} == {5, 9}
    assert {event["drishti_house"] for event in saturn} == {3, 10}


def test_nodes_do_not_receive_unsourced_special_drishti_rules():
    natal = [position("sun", 5), position("moon", 7), position("mars", 9)]
    events = parashari_drishti_events(
        natal,
        [position("rahu", 1), position("ketu", 1)],
    )
    assert events == []


def test_western_aspect_vocabulary_is_not_emitted():
    natal = [position("sun", 5), position("moon", 7), position("mars", 9)]
    events = parashari_drishti_events(natal, [position("jupiter", 1)])
    serialized = str(events).lower()
    for forbidden in ("square", "trine", "sextile", "opposition", "conjunction"):
        assert forbidden not in serialized
