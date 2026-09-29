from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

VIMSHOTTARI = [
    ("ketu", 7), ("venus", 20), ("sun", 6), ("moon", 10), ("mars", 7),
    ("rahu", 18), ("jupiter", 16), ("saturn", 19), ("mercury", 17),
]
TOTAL_YEARS = 120.0
NAKSHATRA_SPAN = 360.0 / 27.0
YEAR_DAYS = 365.2425


@dataclass(frozen=True)
class DashaPeriod:
    lord: str
    start: datetime
    end: datetime


def _add_years_fraction(dt: datetime, years: float) -> datetime:
    return dt + timedelta(days=years * YEAR_DAYS)


def mahadasha_timeline(birth_dt: datetime, moon_longitude: float, cycles: int = 2) -> list[DashaPeriod]:
    lon = moon_longitude % 360.0
    nak_index = int(lon // NAKSHATRA_SPAN)
    start_idx = nak_index % 9
    fraction_elapsed = (lon % NAKSHATRA_SPAN) / NAKSHATRA_SPAN
    first_lord, first_years = VIMSHOTTARI[start_idx]
    first_start = _add_years_fraction(birth_dt, -(first_years * fraction_elapsed))

    periods: list[DashaPeriod] = []
    cursor = first_start
    for offset in range(9 * max(1, cycles)):
        lord, years = VIMSHOTTARI[(start_idx + offset) % 9]
        end = _add_years_fraction(cursor, years)
        periods.append(DashaPeriod(lord=lord, start=cursor, end=end))
        cursor = end
    return periods


def active_mahadasha(birth_dt: datetime, moon_longitude: float, as_of: datetime) -> DashaPeriod:
    for period in mahadasha_timeline(birth_dt, moon_longitude):
        if period.start <= as_of < period.end:
            return period
    raise ValueError("as_of lies outside generated Vimshottari range")


def subperiod_timeline(parent: DashaPeriod) -> list[DashaPeriod]:
    parent_years = (parent.end - parent.start).total_seconds() / 86400.0 / YEAR_DAYS
    start_idx = next(i for i, (lord, _) in enumerate(VIMSHOTTARI) if lord == parent.lord)
    cursor = parent.start
    result: list[DashaPeriod] = []
    for offset in range(9):
        lord, years = VIMSHOTTARI[(start_idx + offset) % 9]
        end = _add_years_fraction(cursor, parent_years * years / TOTAL_YEARS)
        result.append(DashaPeriod(lord=lord, start=cursor, end=end))
        cursor = end
    return result


def antardasha_timeline(maha: DashaPeriod) -> list[DashaPeriod]:
    return subperiod_timeline(maha)


def pratyantardasha_timeline(antara: DashaPeriod) -> list[DashaPeriod]:
    return subperiod_timeline(antara)


def active_subperiod(parent: DashaPeriod, as_of: datetime) -> DashaPeriod:
    for period in subperiod_timeline(parent):
        if period.start <= as_of < period.end:
            return period
    raise ValueError("as_of lies outside parent Dasha period")


def active_antardasha(maha: DashaPeriod, as_of: datetime) -> DashaPeriod:
    return active_subperiod(maha, as_of)


def active_pratyantardasha(antara: DashaPeriod, as_of: datetime) -> DashaPeriod:
    return active_subperiod(antara, as_of)
