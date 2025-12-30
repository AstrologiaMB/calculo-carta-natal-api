"""
Configuración para FastAPI - Carta Natal API
"""
import os
import sys
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # Información de la aplicación
    app_name: str = "Carta Natal API - Astrowellness"
    version: str = "1.0.0"
    description: str = "Microservicio para cálculo de cartas natales astrológicas"
    
    # Configuración del servidor
    host: str = "0.0.0.0"
    port: int = 8001
    reload: bool = True  # Solo para desarrollo
    
    # CORS - Permitir orígenes específicos (Producción y Desarrollo)
    cors_origins: List[str] = [
        "http://localhost:3000",
        "https://homepageastrowellness.fly.dev",
        "https://astrochat.online",
        "https://www.astrochat.online"
    ]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configuración específica
    max_request_size: int = 1024 * 1024  # 1MB
    timeout_seconds: int = 30
    
    # Información del sistema
    python_version: str = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Instancia global de configuración
settings = Settings()
