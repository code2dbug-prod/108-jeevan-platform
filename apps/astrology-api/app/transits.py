from __future__ import annotations

from datetime import datetime

from .engine import calculate_at
from .models import GrahaPosition

ASPECT_ANGLES = {
    "conjunction": 0.0,
    "opposition": 180.0,
    "trine": 120.0,
    "square": 90.0,
    "sextile": 60.0,
}


def angular_distance(a: float, b: float) -> float:
    delta = abs((a - b) % 360.0)
    return min(delta, 360.0 - delta)


def aspect_events(natal: list[GrahaPosition], transit: list[GrahaPosition], orb: float = 3.0) -> list[dict]:
    events: list[dict] = []
    for t in transit:
        for n in natal:
            distance = angular_distance(t.longitude, n.longitude)
            for name, angle in ASPECT_ANGLES.items():
                error = abs(distance - angle)
                if error <= orb:
                    events.append({
                        "transit_graha": t.key,
                        "natal_graha": n.key,
                        "aspect": name,
                        "orb": round(error, 3),
                    })
    return sorted(events, key=lambda x: x["orb"])


def current_gochara(at: datetime, latitude: float, longitude: float):
    return calculate_at(at, latitude, longitude, "exact")
