from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from timezonefinder import TimezoneFinder

from .config import settings
from .dasha import active_antardasha, active_mahadasha, active_pratyantardasha
from .derived import enrich_chart
from .engine import calculate_chart
from .models import (
    BirthData, ChartResponse, DashaPeriodModel, DashaResponse, FullChartResponse,
    TimezoneRequest, TimezoneResponse, TransitRequest, TransitResponse, UnknownTimeResponse,
)
from .transits import current_gochara, parashari_drishti_events
from .uncertainty import analyze_unknown_birth_time

app = FastAPI(title="108-Jeevan Jyotisha Engine", version="0.2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[x.strip() for x in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
timezone_finder = TimezoneFinder(in_memory=True)


@app.get("/health")
def health():
    return {
        "ok": True,
        "service": "astrology-api",
        "calculation_engine": "swiss-ephemeris",
        "ayanamsa": "lahiri",
        "house_system": "whole-sign",
        "drishti_system": "parashari-full-sign",
        "version": "0.2.0",
    }


@app.post("/v1/places/timezone", response_model=TimezoneResponse)
def timezone_for_coordinates(data: TimezoneRequest):
    zone = timezone_finder.timezone_at(lat=data.latitude, lng=data.longitude)
    if not zone:
        raise HTTPException(status_code=422, detail="Timezone could not be resolved")
    return TimezoneResponse(timezone=zone)


@app.post("/v1/charts/calculate", response_model=ChartResponse)
def chart(data: BirthData):
    try:
        return calculate_chart(data)
    except (ValueError, KeyError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/v1/charts/full", response_model=FullChartResponse)
def full_chart(data: BirthData):
    try:
        base = calculate_chart(data)
        derived = enrich_chart(
            base.ascendant.rashi if base.ascendant else None,
            base.ascendant.longitude if base.ascendant else None,
            base.grahas,
        )
        return FullChartResponse(**base.model_dump(), **derived)
    except (ValueError, KeyError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/v1/charts/unknown-time", response_model=UnknownTimeResponse)
def unknown_time(data: BirthData, interval_minutes: int = Query(60, ge=15, le=180)):
    try:
        return analyze_unknown_birth_time(data, interval_minutes)
    except (ValueError, KeyError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/v1/dasha/current", response_model=DashaResponse)
def current_dasha(data: BirthData, as_of: datetime | None = None):
    try:
        chart_data = calculate_chart(data)
        moon = next(g for g in chart_data.grahas if g.key == "moon")
        birth_dt = datetime.combine(data.date_of_birth, data.birth_time, tzinfo=ZoneInfo(data.timezone))
        reference = as_of or datetime.now(ZoneInfo(data.timezone))
        maha = active_mahadasha(birth_dt, moon.longitude, reference)
        antara = active_antardasha(maha, reference)
        pratyantara = active_pratyantardasha(antara, reference)
        return DashaResponse(
            mahadasha=DashaPeriodModel(lord=maha.lord, start=maha.start, end=maha.end),
            antardasha=DashaPeriodModel(lord=antara.lord, start=antara.start, end=antara.end),
            pratyantardasha=DashaPeriodModel(
                lord=pratyantara.lord, start=pratyantara.start, end=pratyantara.end
            ),
            moon_longitude=moon.longitude,
            as_of=reference,
        )
    except (ValueError, KeyError, StopIteration, TypeError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/v1/transits/compare", response_model=TransitResponse)
def compare_transits(request: TransitRequest):
    transit = current_gochara(request.at, request.latitude, request.longitude)
    return TransitResponse(
        at=request.at,
        grahas=transit.grahas,
        events=parashari_drishti_events(request.natal.grahas, transit.grahas),
    )
