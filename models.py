"""
Modelos Pydantic para FastAPI - Carta Natal API
"""
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, Dict, List, Any
from datetime import datetime
import re

class UserDataRequest(BaseModel):
    """Datos de entrada para calcular carta natal"""
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre completo del usuario")
    fecha_nacimiento: str = Field(..., description="Fecha de nacimiento en formato YYYY-MM-DD")
    hora_nacimiento: str = Field(..., description="Hora de nacimiento en formato HH:MM")
    ciudad_nacimiento: str = Field(..., min_length=2, description="Ciudad de nacimiento")
    pais_nacimiento: str = Field(..., min_length=2, description="País de nacimiento")
    
    @field_validator('fecha_nacimiento')
    @classmethod
    def validate_fecha(cls, v):
        """Validar formato de fecha YYYY-MM-DD"""
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', v):
            raise ValueError('Fecha debe estar en formato YYYY-MM-DD')
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Fecha inválida')
        return v
    
    @field_validator('hora_nacimiento')
    @classmethod
    def validate_hora(cls, v):
        """Validar formato de hora HH:MM"""
        if not re.match(r'^\d{2}:\d{2}$', v):
            raise ValueError('Hora debe estar en formato HH:MM')
        try:
            datetime.strptime(v, '%H:%M')
        except ValueError:
            raise ValueError('Hora inválida')
        return v

class CartaNatalResponse(BaseModel):
    """Respuesta con datos de carta natal"""
    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})
    
    success: bool
    data: Optional[Dict[str, Any]] = None
    data_reducido: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class HealthResponse(BaseModel):
    """Respuesta del health check"""
    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})
    
    status: str
    service: str
    version: str
    timestamp: datetime
    python_version: str
    dependencies_ok: bool

class ErrorResponse(BaseModel):
    """Respuesta de error estándar"""
    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})
    
    success: bool = False
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
