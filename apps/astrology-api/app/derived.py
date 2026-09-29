from __future__ import annotations

from dataclasses import dataclass
from math import floor

from .models import GrahaPosition

RASHI_LORDS = {
    1: "mars", 2: "venus", 3: "mercury", 4: "moon", 5: "sun", 6: "mercury",
    7: "venus", 8: "mars", 9: "jupiter", 10: "saturn", 11: "saturn", 12: "jupiter",
}
EXALTATION = {
    "sun": (1, 10.0), "moon": (2, 3.0), "mars": (10, 28.0), "mercury": (6, 15.0),
    "jupiter": (4, 5.0), "venus": (12, 27.0), "saturn": (7, 20.0),
}
DEBILITATION = {k: (((r + 5) % 12) + 1, d) for k, (r, d) in EXALTATION.items()}


def whole_sign_house(asc_rashi: int, rashi: int) -> int:
    return ((rashi - asc_rashi) % 12) + 1


def house_map(asc_rashi: int, grahas: list[GrahaPosition]) -> list[dict]:
    houses = []
    for house in range(1, 13):
        rashi = ((asc_rashi + house - 2) % 12) + 1
        houses.append({
            "house": house,
            "rashi": rashi,
            "lord": RASHI_LORDS[rashi],
            "occupants": [g.key for g in grahas if g.rashi == rashi],
        })
    return houses


def dignity(graha: GrahaPosition) -> str:
    if graha.key in EXALTATION and graha.rashi == EXALTATION[graha.key][0]:
        return "exalted"
    if graha.key in DEBILITATION and graha.rashi == DEBILITATION[graha.key][0]:
        return "debilitated"
    own = {
        "sun": {5}, "moon": {4}, "mars": {1, 8}, "mercury": {3, 6},
        "jupiter": {9, 12}, "venus": {2, 7}, "saturn": {10, 11},
    }
    return "own-sign" if graha.rashi in own.get(graha.key, set()) else "neutral"


def navamsa_rashi(longitude: float) -> int:
    rashi_index = int((longitude % 360) // 30)
    part = int(((longitude % 30) // (30 / 9)))
    modality = rashi_index % 3
    start = rashi_index if modality == 0 else (rashi_index + 8 if modality == 1 else rashi_index + 4)
    return ((start + part) % 12) + 1


def navamsa(grahas: list[GrahaPosition], asc_longitude: float | None) -> dict:
    return {
        "ascendant_rashi": navamsa_rashi(asc_longitude) if asc_longitude is not None else None,
        "grahas": [{"key": g.key, "rashi": navamsa_rashi(g.longitude)} for g in grahas],
    }


def panchanga_from_longitudes(sun_lon: float, moon_lon: float) -> dict:
    elongation = (moon_lon - sun_lon) % 360
    tithi_index = int(elongation // 12) + 1
    paksha = "shukla" if tithi_index <= 15 else "krishna"
    tithi_in_paksha = tithi_index if tithi_index <= 15 else tithi_index - 15
    yoga_index = int(((sun_lon + moon_lon) % 360) // (360 / 27)) + 1
    karana_index = int(elongation // 6) + 1
    return {
        "tithi": tithi_index,
        "paksha": paksha,
        "tithi_in_paksha": tithi_in_paksha,
        "yoga_index": yoga_index,
        "karana_index": karana_index,
    }


def enrich_chart(asc_rashi: int | None, asc_longitude: float | None, grahas: list[GrahaPosition]) -> dict:
    sun = next(g for g in grahas if g.key == "sun")
    moon = next(g for g in grahas if g.key == "moon")
    return {
        "houses": house_map(asc_rashi, grahas) if asc_rashi else [],
        "dignities": {g.key: dignity(g) for g in grahas if g.key not in {"rahu", "ketu"}},
        "navamsa": navamsa(grahas, asc_longitude),
        "panchanga": panchanga_from_longitudes(sun.longitude, moon.longitude),
    }
