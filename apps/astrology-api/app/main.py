from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .engine import calculate_chart
from .models import BirthData, ChartResponse, UnknownTimeResponse
from .uncertainty import analyze_unknown_birth_time

app = FastAPI(title="108-Jeevan Jyotisha Engine", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=[x.strip() for x in settings.cors_origins.split(",")], allow_credentials=True, allow_methods=["GET","POST"], allow_headers=["*"])

@app.get("/health")
def health():
    return {"ok": True, "service": "astrology-api", "calculation_engine": "swiss-ephemeris", "ayanamsa": "lahiri"}

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
