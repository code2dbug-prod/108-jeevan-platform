from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo
import swisseph as swe

from .config import settings
from .models import Ascendant, BirthData, ChartResponse, GrahaPosition

CALCULATION_VERSION = "jeevan-jyotisha-0.1.0"
NAKSHATRAS = [
    "Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra","Punarvasu","Pushya","Ashlesha",
    "Magha","Purva Phalguni","Uttara Phalguni","Hasta","Chitra","Swati","Vishakha","Anuradha","Jyeshtha",
    "Mula","Purva Ashadha","Uttara Ashadha","Shravana","Dhanishtha","Shatabhisha","Purva Bhadrapada","Uttara Bhadrapada","Revati",
]
GRAHAS = {
    "sun": swe.SUN, "moon": swe.MOON, "mars": swe.MARS, "mercury": swe.MERCURY,
    "jupiter": swe.JUPITER, "venus": swe.VENUS, "saturn": swe.SATURN, "rahu": swe.MEAN_NODE,
}

if settings.ephemeris_path:
    swe.set_ephe_path(settings.ephemeris_path)
swe.set_sid_mode(swe.SIDM_LAHIRI)


def _jd_utc(local_dt: datetime) -> float:
    utc = local_dt.astimezone(ZoneInfo("UTC"))
    hour = utc.hour + utc.minute / 60 + utc.second / 3600
    return swe.julday(utc.year, utc.month, utc.day, hour, swe.GREG_CAL)


def _norm(lon: float) -> float:
    return lon % 360.0


def _nakshatra(lon: float) -> tuple[str, int]:
    span = 360.0 / 27.0
    index = int(lon // span) % 27
    within = lon - index * span
    pada = min(4, int(within // (span / 4.0)) + 1)
    return NAKSHATRAS[index], pada


def _graha_position(key: str, lon: float, speed: float) -> GrahaPosition:
    lon = _norm(lon)
    nakshatra, pada = _nakshatra(lon)
    return GrahaPosition(
        key=key,
        longitude=round(lon, 6),
        rashi=int(lon // 30) + 1,
        degree_in_rashi=round(lon % 30, 6),
        nakshatra=nakshatra,
        pada=pada,
        retrograde=speed < 0,
    )


def calculate_at(local_dt: datetime, latitude: float, longitude: float, reliability: str) -> ChartResponse:
    jd = _jd_utc(local_dt)
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
    grahas: list[GrahaPosition] = []
    for key, body in GRAHAS.items():
        values, _ = swe.calc_ut(jd, body, flags)
        grahas.append(_graha_position(key, values[0], values[3]))
    rahu = next(g for g in grahas if g.key == "rahu")
    ketu = _graha_position("ketu", rahu.longitude + 180.0, -1.0 if rahu.retrograde else 1.0)
    grahas.append(ketu)

    cusps, ascmc = swe.houses_ex(jd, latitude, longitude, b"W", swe.FLG_SIDEREAL)
    asc_lon = _norm(ascmc[0])
    return ChartResponse(
        calculation_version=CALCULATION_VERSION,
        birth_time_reliability=reliability,
        ascendant=Ascendant(longitude=round(asc_lon, 6), rashi=int(asc_lon // 30) + 1),
        grahas=grahas,
        warnings=[],
    )


def calculate_chart(data: BirthData) -> ChartResponse:
    if data.birth_time is None:
        raise ValueError("Use the unknown-time endpoint when birth time is unknown")
    local_dt = datetime.combine(data.date_of_birth, data.birth_time, tzinfo=ZoneInfo(data.timezone))
    response = calculate_at(local_dt, data.latitude, data.longitude, data.birth_time_precision)
    if data.birth_time_precision == "approximate":
        response.warnings.append("Birth time is approximate; Lagna, houses, Vargas and timing-sensitive claims require uncertainty review.")
    return response
