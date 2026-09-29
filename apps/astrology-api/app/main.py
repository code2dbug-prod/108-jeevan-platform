from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .dasha import active_antardasha, active_mahadasha
from .engine import calculate_chart
from .models import (
    BirthData,
    ChartResponse,
    DashaPeriodModel,
    DashaResponse,
    TransitRequest,
    TransitResponse,
    UnknownTimeResponse,
)
from .transits import aspect_events, current_gochara
from .uncertainty import analyze_unknown_birth_time

app = FastAPI(title="108-Jeevan Jyotisha Engine", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[x.strip() for x in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {
        "ok": True,
        "service": "astrology-api",
        "calculation_engine": "swiss-ephemeris",
        "ayanamsa": "lahiri",
        "house_system": "whole-sign",
    }

@app.post("/v1/charts/calculate", response_model=ChartResponse)
def chart(data: BirthData):
    try:
        return calculate_chart(data)
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
        return DashaResponse(
            mahadasha=DashaPeriodModel(lord=maha.lord, start=maha.start, end=maha.end),
            antardasha=DashaPeriodModel(lord=antara.lord, start=antara.start, end=antara.end),
            moon_longitude=moon.longitude,
            as_of=reference,
        )
    except (ValueError, KeyError, StopIteration) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

@app.post("/v1/transits/compare", response_model=TransitResponse)
def compare_transits(request: TransitRequest):
    transit = current_gochara(request.at, request.latitude, request.longitude)
    return TransitResponse(
        at=request.at,
        grahas=transit.grahas,
        events=aspect_events(request.natal.grahas, transit.grahas, request.orb),
    )
