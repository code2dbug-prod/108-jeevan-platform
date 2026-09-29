from datetime import date, datetime, time
from typing import Literal
from pydantic import BaseModel, Field, model_validator

BirthPrecision = Literal["exact", "approximate", "unknown"]

class BirthData(BaseModel):
    full_name: str = Field(min_length=1)
    date_of_birth: date
    birth_time: time | None = None
    birth_time_precision: BirthPrecision = "exact"
    birthplace_label: str = Field(min_length=1)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    timezone: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_time_precision(self):
        if self.birth_time_precision == "exact" and self.birth_time is None:
            raise ValueError("exact birth time requires birth_time")
        if self.birth_time_precision == "unknown" and self.birth_time is not None:
            raise ValueError("unknown birth time must not provide birth_time")
        return self

class GrahaPosition(BaseModel):
    key: str
    longitude: float
    rashi: int
    degree_in_rashi: float
    nakshatra: str
    pada: int
    retrograde: bool

class Ascendant(BaseModel):
    longitude: float
    rashi: int

class ChartResponse(BaseModel):
    calculation_version: str
    ayanamsa: Literal["lahiri"] = "lahiri"
    house_system: Literal["whole-sign"] = "whole-sign"
    birth_time_reliability: BirthPrecision
    ascendant: Ascendant | None
    grahas: list[GrahaPosition]
    warnings: list[str] = []

class UncertaintyField(BaseModel):
    field: str
    stable: bool
    values: list[str]

class UnknownTimeResponse(BaseModel):
    calculation_version: str
    sample_interval_minutes: int
    samples: int
    stable_grahas: list[GrahaPosition]
    unstable: list[UncertaintyField]
    warnings: list[str]

class DashaPeriodModel(BaseModel):
    lord: str
    start: datetime
    end: datetime

class DashaResponse(BaseModel):
    mahadasha: DashaPeriodModel
    antardasha: DashaPeriodModel
    moon_longitude: float
    as_of: datetime

class TransitRequest(BaseModel):
    natal: ChartResponse
    at: datetime
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    orb: float = Field(default=3.0, ge=0.1, le=10.0)

class TransitResponse(BaseModel):
    at: datetime
    grahas: list[GrahaPosition]
    events: list[dict]
