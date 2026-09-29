from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from .engine import CALCULATION_VERSION, calculate_at
from .models import BirthData, GrahaPosition, UncertaintyField, UnknownTimeResponse


def analyze_unknown_birth_time(data: BirthData, interval_minutes: int = 60) -> UnknownTimeResponse:
    if data.birth_time_precision != "unknown":
        raise ValueError("unknown-time analysis requires birth_time_precision=unknown")
    if interval_minutes < 15 or interval_minutes > 180:
        raise ValueError("sample interval must be between 15 and 180 minutes")

    zone = ZoneInfo(data.timezone)
    start = datetime.combine(data.date_of_birth, time(0, 0), tzinfo=zone)
    samples = []
    cursor = start
    while cursor.date() == data.date_of_birth:
        samples.append(calculate_at(cursor, data.latitude, data.longitude, "unknown"))
        cursor += timedelta(minutes=interval_minutes)

    stable_grahas: list[GrahaPosition] = []
    unstable: list[UncertaintyField] = []
    keys = [g.key for g in samples[0].grahas]
    for key in keys:
        positions = [next(g for g in sample.grahas if g.key == key) for sample in samples]
        rashis = sorted({str(p.rashi) for p in positions})
        nakshatras = sorted({p.nakshatra for p in positions})
        if len(rashis) == 1 and len(nakshatras) == 1:
            stable_grahas.append(positions[len(positions)//2])
        else:
            unstable.append(UncertaintyField(field=f"{key}.rashi", stable=len(rashis)==1, values=rashis))
            unstable.append(UncertaintyField(field=f"{key}.nakshatra", stable=len(nakshatras)==1, values=nakshatras))

    asc_values = sorted({str(s.ascendant.rashi) for s in samples if s.ascendant})
    unstable.append(UncertaintyField(field="ascendant.rashi", stable=len(asc_values)==1, values=asc_values))

    return UnknownTimeResponse(
        calculation_version=CALCULATION_VERSION,
        sample_interval_minutes=interval_minutes,
        samples=len(samples),
        stable_grahas=stable_grahas,
        unstable=unstable,
        warnings=[
            "Birth time is unknown. Lagna, houses, bhava lordship and divisional-chart claims are suppressed unless stable across the sampled day.",
            "This is an uncertainty analysis, not birth-time rectification.",
        ],
    )
