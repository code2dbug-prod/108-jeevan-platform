from fastapi.testclient import TestClient

from app.conditions import manglik, sade_sati
from app.derived import navamsa_rashi, whole_sign_house
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


def birth_payload():
    return {
        "full_name": "Test Person",
        "date_of_birth": "1990-01-01",
        "birth_time": "12:00:00",
        "birth_time_precision": "exact",
        "birthplace_label": "Delhi, India",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "timezone": "Asia/Kolkata",
    }


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["ayanamsa"] == "lahiri"
    assert response.json()["drishti_system"] == "parashari-full-sign"


def test_exact_chart_returns_nine_grahas():
    response = client.post("/v1/charts/calculate", json=birth_payload())
    assert response.status_code == 200
    payload = response.json()
    assert len(payload["grahas"]) == 9
    assert payload["ascendant"] is not None


def test_full_chart_returns_derived_sections():
    response = client.post("/v1/charts/full", json=birth_payload())
    assert response.status_code == 200
    payload = response.json()
    assert len(payload["houses"]) == 12
    assert "sun" in payload["dignities"]
    assert payload["navamsa"]["ascendant_rashi"] in range(1, 13)
    assert payload["panchanga"]["tithi"] in range(1, 31)


def test_current_dasha_includes_pratyantardasha():
    response = client.post("/v1/dasha/current", json=birth_payload())
    assert response.status_code == 200
    assert response.json()["pratyantardasha"] is not None


def test_unknown_time_rejects_fake_time():
    payload=birth_payload()
    payload["birth_time_precision"]="unknown"
    payload["birth_time"]="12:00:00"
    response = client.post("/v1/charts/unknown-time", json=payload)
    assert response.status_code == 422


def test_whole_sign_house_wraps():
    assert whole_sign_house(1, 1) == 1
    assert whole_sign_house(12, 1) == 2


def test_navamsa_stays_in_rashi_range():
    for longitude in (0.0, 29.9, 30.0, 119.2, 359.9):
        assert 1 <= navamsa_rashi(longitude) <= 12


def test_sign_distance_is_inclusive_and_wraps():
    assert sign_distance(1, 1) == 1
    assert sign_distance(1, 7) == 7
    assert sign_distance(12, 6) == 7


def test_mars_has_full_fourth_seventh_and_eighth_drishti():
    natal = [position("sun", 4), position("moon", 7), position("jupiter", 8), position("venus", 5)]
    events = parashari_drishti_events(natal, [position("mars", 1)])
    assert {event["drishti_house"] for event in events} == {4, 7, 8}


def test_jupiter_and_saturn_special_full_drishti():
    natal = [position("sun", 5), position("moon", 9), position("mercury", 3), position("venus", 10)]
    jupiter = parashari_drishti_events(natal, [position("jupiter", 1)])
    saturn = parashari_drishti_events(natal, [position("saturn", 1)])
    assert {event["drishti_house"] for event in jupiter} == {5, 9}
    assert {event["drishti_house"] for event in saturn} == {3, 10}


def test_nodes_do_not_receive_unsourced_special_drishti_rules():
    natal = [position("sun", 5), position("moon", 7), position("mars", 9)]
    assert parashari_drishti_events(natal, [position("rahu", 1), position("ketu", 1)]) == []


def test_western_aspect_vocabulary_is_not_emitted():
    natal = [position("sun", 5), position("moon", 7), position("mars", 9)]
    serialized = str(parashari_drishti_events(natal, [position("jupiter", 1)])).lower()
    for forbidden in ("square", "trine", "sextile", "opposition", "conjunction"):
        assert forbidden not in serialized


def test_sade_sati_three_sign_window():
    natal = [position("moon", 5)]
    assert sade_sati(natal, [position("saturn", 4)])["phase"] == "rising"
    assert sade_sati(natal, [position("saturn", 5)])["phase"] == "peak"
    assert sade_sati(natal, [position("saturn", 6)])["phase"] == "setting"
    assert sade_sati(natal, [position("saturn", 7)])["active"] is False


def test_manglik_baseline_is_explicit_and_lagna_based():
    result = manglik(1, [position("mars", 8)])
    assert result["active"] is True
    assert result["mars_house"] == 8
    assert result["rule_id"] == "JEEVAN_MANGLIK_BASELINE_ASC_1_2_4_7_8_12"
