"""
FastAPI Wrapper para Carta Natal - Proyecto Astrowellness
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging
import traceback
import sys
from datetime import datetime
from typing import Dict, Any

# Importar funciones existentes de main.py
try:
    from main import calcular_carta_natal, generar_json_reducido, get_coordinates
except ImportError as e:
    print(f"Error importando main.py: {e}")
    print("Asegúrate de que main.py esté en el mismo directorio")
    sys.exit(1)

# Importar modelos y configuración
from models import UserDataRequest, CartaNatalResponse, HealthResponse, ErrorResponse
from config import settings

# Importar calculadora de análisis cruzados
from src.calculators.cross_chart_calculator import calcular_cuspides_cruzadas, calcular_aspectos_cruzados

# Configurar logging
logging.basicConfig(
    level=settings.log_level,
    format=settings.log_format,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('carta_natal_api.log')
    ]
)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description=settings.description,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# Middleware para logging de requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url}")
    
    # Procesar request
    response = await call_next(request)
    
    # Log response
    process_time = (datetime.now() - start_time).total_seconds()
    logger.info(f"Response: {response.status_code} - {process_time:.3f}s")
    
    return response

# Manejador de errores de validación
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            error="Datos de entrada inválidos",
            detail=str(exc)
        ).model_dump()
    )

# Manejador de errores generales
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {exc}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Error interno del servidor",
            detail=str(exc) if settings.log_level == "DEBUG" else None
        ).model_dump()
    )

@app.get("/", response_model=Dict[str, Any])
async def root():
    """Información básica del servicio"""
    return {
        "service": settings.app_name,
        "version": settings.version,
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "carta_tropical": "/carta-natal/tropical",
            "carta_draconica": "/carta-natal/draconica",
            "carta_cruzada": "/carta-natal/cruzada"
        },
        "description": settings.description
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check del servicio"""
    try:
        # Verificar que las dependencias principales estén disponibles
        dependencies_ok = True
        try:
            import geopy
            import timezonefinder
            from main import calcular_carta_natal
        except ImportError:
            dependencies_ok = False
        
        return HealthResponse(
            status="healthy" if dependencies_ok else "degraded",
            service=settings.app_name,
            version=settings.version,
            timestamp=datetime.now(),
            python_version=settings.python_version,
            dependencies_ok=dependencies_ok
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy")

@app.post("/carta-natal/tropical", response_model=CartaNatalResponse)
async def calcular_carta_tropical(request: UserDataRequest):
    """Calcular carta natal trópica"""
    logger.info(f"Calculando carta tropical para: {request.nombre}")
    
    try:
        # Preparar datos para main.py
        datos_usuario = await preparar_datos_usuario(request)
        logger.debug(f"Datos preparados: {datos_usuario}")
        
        # Calcular carta natal
        resultado = calcular_carta_natal(datos_usuario, draconica=False)
        logger.info("Carta tropical calculada exitosamente")
        
        # Generar formato reducido para AstroChart
        resultado_reducido = generar_json_reducido(resultado)
        logger.debug("Formato reducido generado")
        
        return CartaNatalResponse(
            success=True,
            data=resultado,
            data_reducido=resultado_reducido
        )
        
    except Exception as e:
        logger.error(f"Error calculando carta tropical: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500, 
            detail=f"Error calculando carta natal: {str(e)}"
        )

@app.post("/carta-natal/draconica", response_model=CartaNatalResponse)
async def calcular_carta_draconica(request: UserDataRequest):
    """Calcular carta natal dracónica"""
    logger.info(f"Calculando carta dracónica para: {request.nombre}")
    
    try:
        # Preparar datos para main.py
        datos_usuario = await preparar_datos_usuario(request)
        
        # Calcular carta dracónica
        resultado = calcular_carta_natal(datos_usuario, draconica=True)
        logger.info("Carta dracónica calculada exitosamente")
        
        # Generar formato reducido
        resultado_reducido = generar_json_reducido(resultado)
        
        return CartaNatalResponse(
            success=True,
            data=resultado,
            data_reducido=resultado_reducido
        )
        
    except Exception as e:
        logger.error(f"Error calculando carta dracónica: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500, 
            detail=f"Error calculando carta dracónica: {str(e)}"
        )

@app.post("/carta-natal/cruzada", response_model=CartaNatalResponse)
async def calcular_carta_cruzada(request: UserDataRequest):
    """Calcular análisis cruzado dracónico-tropical"""
    logger.info(f"Calculando análisis cruzado para: {request.nombre}")
    
    try:
        # Preparar datos para main.py
        datos_usuario = await preparar_datos_usuario(request)
        logger.debug(f"Datos preparados: {datos_usuario}")
        
        # Calcular ambas cartas
        logger.info("Calculando carta tropical...")
        carta_tropical = calcular_carta_natal(datos_usuario, draconica=False)
        
        logger.info("Calculando carta dracónica...")
        carta_draconica = calcular_carta_natal(datos_usuario, draconica=True)
        
        # Calcular análisis cruzados
        logger.info("Calculando cúspides cruzadas...")
        cuspides_cruzadas = calcular_cuspides_cruzadas(carta_tropical, carta_draconica)
        
        logger.info("Calculando aspectos cruzados...")
        aspectos_cruzados = calcular_aspectos_cruzados(carta_tropical, carta_draconica)
        
        logger.info(f"Análisis completado: {len(cuspides_cruzadas)} cúspides, {len(aspectos_cruzados)} aspectos")
        
        # Estructurar respuesta usando CartaNatalResponse existente
        return CartaNatalResponse(
            success=True,
            data={
                "tipo_analisis": "cruzado_draconico_tropical",
                "carta_tropical": carta_tropical,
                "carta_draconica": carta_draconica,
                "cuspides_cruzadas": cuspides_cruzadas,
                "aspectos_cruzados": aspectos_cruzados,
                "metadata": {
                    "total_cuspides": len(cuspides_cruzadas),
                    "total_aspectos": len(aspectos_cruzados),
                    "orbe_conjuncion": 8.0,
                    "orbe_oposicion": 8.0,
                    "puntos_analizados": [
                        'Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 
                        'Uranus', 'Neptune', 'Pluto', 'True North Node', 'Chiron'
                    ]
                }
            },
            data_reducido=None  # No aplica para análisis cruzado
        )
        
    except Exception as e:
        logger.error(f"Error en análisis cruzado: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500, 
            detail=f"Error calculando análisis cruzado: {str(e)}"
        )

async def preparar_datos_usuario(request: UserDataRequest) -> Dict[str, Any]:
    """
    Convierte UserDataRequest al formato esperado por main.py
    """
    try:
        # Obtener coordenadas usando la función existente
        logger.info(f"Obteniendo coordenadas para: {request.ciudad_nacimiento}, {request.pais_nacimiento}")
        lat, lon, timezone = get_coordinates(request.ciudad_nacimiento, request.pais_nacimiento)
        logger.info(f"Coordenadas obtenidas: {lat}, {lon}, {timezone}")
        
        # Preparar fecha/hora en formato ISO
        fecha_hora_iso = f"{request.fecha_nacimiento}T{request.hora_nacimiento}:00"
        fecha_hora_natal = f"{request.fecha_nacimiento} {request.hora_nacimiento}"
        
        datos = {
            "nombre": request.nombre,
            "hora_local": fecha_hora_iso,
            "fecha_hora_natal": fecha_hora_natal,
            "lat": lat,
            "lon": lon,
            "zona_horaria": timezone,
            "lugar": f"{request.ciudad_nacimiento}, {request.pais_nacimiento}"
        }
        
        return datos
        
    except Exception as e:
        logger.error(f"Error preparando datos de usuario: {e}")
        raise ValueError(f"Error procesando ubicación: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Iniciando {settings.app_name} v{settings.version}")
    logger.info(f"Servidor: http://{settings.host}:{settings.port}")
    logger.info(f"Documentación: http://{settings.host}:{settings.port}/docs")
    
    uvicorn.run(
        "app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower()
    )
