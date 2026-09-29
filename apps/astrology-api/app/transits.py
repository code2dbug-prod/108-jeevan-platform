from __future__ import annotations

from datetime import datetime

from .engine import calculate_at
from .models import GrahaPosition

# Full Parashari Graha Drishti expressed as house/sign distances counted
# inclusively from the sign occupied by the aspecting graha.
# Classical visible-graha baseline:
# - all seven visible grahas: 7th
# - Mars: additional 4th and 8th
# - Jupiter: additional 5th and 9th
# - Saturn: additional 3rd and 10th
#
# Rahu/Ketu special drishti traditions vary, so nodes are intentionally
# excluded until the project explicitly selects and sources a node tradition.
FULL_DRISHTI: dict[str, tuple[int, ...]] = {
    "sun": (7,),
    "moon": (7,),
    "mars": (4, 7, 8),
    "mercury": (7,),
    "jupiter": (5, 7, 9),
    "venus": (7,),
    "saturn": (3, 7, 10),
}

RULE_IDS = {
    ("sun", 7): "PARASHARI_DRISHTI_ALL_7",
    ("moon", 7): "PARASHARI_DRISHTI_ALL_7",
    ("mercury", 7): "PARASHARI_DRISHTI_ALL_7",
    ("venus", 7): "PARASHARI_DRISHTI_ALL_7",
    ("mars", 4): "PARASHARI_DRISHTI_MARS_4",
    ("mars", 7): "PARASHARI_DRISHTI_ALL_7",
    ("mars", 8): "PARASHARI_DRISHTI_MARS_8",
    ("jupiter", 5): "PARASHARI_DRISHTI_JUPITER_5",
    ("jupiter", 7): "PARASHARI_DRISHTI_ALL_7",
    ("jupiter", 9): "PARASHARI_DRISHTI_JUPITER_9",
    ("saturn", 3): "PARASHARI_DRISHTI_SATURN_3",
    ("saturn", 7): "PARASHARI_DRISHTI_ALL_7",
    ("saturn", 10): "PARASHARI_DRISHTI_SATURN_10",
}


def sign_distance(source_rashi: int, target_rashi: int) -> int:
    """Return inclusive 1..12 sign distance from source to target."""
    if not 1 <= source_rashi <= 12 or not 1 <= target_rashi <= 12:
        raise ValueError("rashi must be between 1 and 12")
    return ((target_rashi - source_rashi) % 12) + 1


def parashari_drishti_events(
    natal: list[GrahaPosition],
    transit: list[GrahaPosition],
) -> list[dict]:
    """Return full sign-based Parashari drishti from transit grahas to natal grahas."""
    events: list[dict] = []
    for transit_graha in transit:
        distances = FULL_DRISHTI.get(transit_graha.key)
        if not distances:
            continue

        for natal_graha in natal:
            distance = sign_distance(transit_graha.rashi, natal_graha.rashi)
            if distance not in distances:
                continue

            events.append(
                {
                    "transit_graha": transit_graha.key,
                    "natal_graha": natal_graha.key,
                    "drishti_house": distance,
                    "strength": "full",
                    "rule_id": RULE_IDS[(transit_graha.key, distance)],
                    "source_rashi": transit_graha.rashi,
                    "target_rashi": natal_graha.rashi,
                }
            )

    return sorted(
        events,
        key=lambda event: (
            event["transit_graha"],
            event["drishti_house"],
            event["natal_graha"],
        ),
    )


# Backward-compatible internal alias. The semantics are now explicitly
# Parashari Graha Drishti, not Western geometric aspects.
def aspect_events(
    natal: list[GrahaPosition],
    transit: list[GrahaPosition],
) -> list[dict]:
    return parashari_drishti_events(natal, transit)


def current_gochara(at: datetime, latitude: float, longitude: float):
    return calculate_at(at, latitude, longitude, "exact")
