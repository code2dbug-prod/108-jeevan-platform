from __future__ import annotations

from .derived import whole_sign_house
from .models import GrahaPosition


MANGLIK_HOUSES = {1, 2, 4, 7, 8, 12}


def sade_sati(natal: list[GrahaPosition], transit: list[GrahaPosition]) -> dict:
    moon = next(g for g in natal if g.key == "moon")
    saturn = next(g for g in transit if g.key == "saturn")
    relative = ((saturn.rashi - moon.rashi) % 12) + 1
    phase = {12: "rising", 1: "peak", 2: "setting"}.get(relative)
    return {
        "active": phase is not None,
        "phase": phase,
        "natal_moon_rashi": moon.rashi,
        "transit_saturn_rashi": saturn.rashi,
        "rule_id": "PARASHARI_SADE_SATI_MOON_12_1_2",
    }


def manglik(ascendant_rashi: int | None, natal: list[GrahaPosition]) -> dict:
    if ascendant_rashi is None:
        return {
            "assessable": False,
            "active": None,
            "mars_house": None,
            "rule_id": "JEEVAN_MANGLIK_BASELINE_ASC_1_2_4_7_8_12",
            "note": "Birth time required for Lagna-based Manglik assessment.",
        }
    mars = next(g for g in natal if g.key == "mars")
    house = whole_sign_house(ascendant_rashi, mars.rashi)
    return {
        "assessable": True,
        "active": house in MANGLIK_HOUSES,
        "mars_house": house,
        "rule_id": "JEEVAN_MANGLIK_BASELINE_ASC_1_2_4_7_8_12",
        "note": "Project baseline only; cancellation rules and alternate Moon/Venus traditions are not implied.",
    }
