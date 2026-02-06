from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Union
from datetime import datetime
from enum import Enum

class RetrogradeStatus(str, Enum):
    DIRECT = "direct"
    RETROGRADE = "retrograde"
    STATIONARY = "stationary"

class PlanetName(str, Enum):
    SUN = "Sun"
    MOON = "Moon"
    MERCURY = "Mercury"
    VENUS = "Venus"
    MARS = "Mars"
    JUPITER = "Jupiter"
    SATURN = "Saturn"
    URANUS = "Uranus"
    NEPTUNE = "Neptune"
    PLUTO = "Pluto"
    NORTH_NODE = "North Node"
    SOUTH_NODE = "South Node"
    CHIRON = "Chiron"
    LILITH = "Lilith"
    ASCENDANT = "Ascendant"
    MIDHEAVEN = "Midheaven"
    VERTEX = "Vertex"
    PART_OF_FORTUNE = "Part of Fortune"

class SignName(str, Enum):
    ARIES = "Aries"
    TAURUS = "Taurus"
    GEMINI = "Gemini"
    CANCER = "Cancer"
    LEO = "Leo"
    VIRGO = "Virgo"
    LIBRA = "Libra"
    SCORPIO = "Scorpio"
    SAGITTARIUS = "Sagittarius"
    CAPRICORN = "Capricorn"
    AQUARIUS = "Aquarius"
    PISCES = "Pisces"

class PointData(BaseModel):
    """Data strict for a celestial point"""
    name: str = Field(..., description="Name of the celestial body")
    sign: str = Field(..., description="Zodiac sign name")
    sign_id: int = Field(..., ge=0, le=11, description="Zodiac sign index (0=Aries)")
    degree: float = Field(..., ge=0, lt=30, description="Degree within the sign")
    abs_degree: float = Field(..., ge=0, lt=360, description="Absolute degree in the zodiac")
    minutes: int = Field(..., ge=0, lt=60, description="Minutes portion of the position")
    retrograde: bool = Field(..., description="True if retrograde")
    house: int = Field(..., ge=1, le=12, description="House placement (1-12)")
    
    model_config = ConfigDict(extra='forbid')

class HouseData(BaseModel):
    """Data strict for a house cusp"""
    house: int = Field(..., ge=1, le=12, description="House number")
    sign: str = Field(..., description="Zodiac sign on the cusp")
    degree: float = Field(..., ge=0, lt=30, description="Degree within the sign")
    minutes: int = Field(..., ge=0, lt=60, description="Minutes portion")
    abs_degree: float = Field(..., ge=0, lt=360, description="Absolute degree in the zodiac")
    
    model_config = ConfigDict(extra='forbid')

class AspectData(BaseModel):
    """Data strict for an aspect"""
    p1: str = Field(..., description="First planet name")
    p2: str = Field(..., description="Second planet name")
    aspect: str = Field(..., description="Aspect name (e.g., Conjunction)")
    orb: float = Field(..., description="Orb of the aspect in degrees")
    applying: bool = Field(..., description="True if applying, False if separating")
    
    model_config = ConfigDict(extra='forbid')

class ElementCount(BaseModel):
    fire: int
    earth: int
    air: int
    water: int

class ModalityCount(BaseModel):
    cardinal: int
    fixed: int
    mutable: int

class BalanceData(BaseModel):
    elements: ElementCount
    modalities: ModalityCount
    polarities: dict[str, int] # positive/negative

class NatalChart(BaseModel):
    """Strict Schema for Natal Chart Response"""
    points: dict[str, PointData]
    houses: dict[str, HouseData]
    aspects: List[AspectData]
    balance: Optional[BalanceData] = None
    
    model_config = ConfigDict(extra='ignore') 

class CartaNatalResponseStrict(BaseModel):
    """Strict Response Wrapper replacing CartaNatalResponse"""
    success: bool
    data: NatalChart
    data_reducido: Optional[dict] = None
    error: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    
    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()}) 
