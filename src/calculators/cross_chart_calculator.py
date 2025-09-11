"""
Calculadora de análisis cruzados entre cartas dracónicas y tropicales

Este módulo implementa algoritmos para:
1. Cúspides Cruzadas: Determinar en qué casa tropical cae cada cúspide dracónica
2. Aspectos Cruzados: Encontrar conjunciones y oposiciones entre planetas dracónicos y tropicales

Algoritmos desarrollados y verificados con datos reales del usuario.
"""
from typing import List, Dict, Any, Tuple
import math

# Lista de puntos a analizar (sin Lilith por solicitud del usuario)
PUNTOS_PRINCIPALES = [
    'Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 
    'Uranus', 'Neptune', 'Pluto', 'True North Node', 'Chiron'
]

def normalizar_longitud(longitud: float) -> float:
    """
    Normaliza longitud a rango 0-360°
    
    Args:
        longitud: Longitud en grados (puede ser negativa o > 360)
        
    Returns:
        Longitud normalizada entre 0-360°
    """
    return longitud % 360

def formatear_grados_minutos(grados: float) -> str:
    """
    Convierte grados decimales a formato legible °'
    
    Args:
        grados: Grados en formato decimal
        
    Returns:
        String en formato "15°45'"
    """
    grados_int = int(grados)
    minutos = int((grados % 1) * 60)
    return f"{grados_int}°{minutos}'"

def calcular_distancia_angular(lon1: float, lon2: float) -> float:
    """
    Calcula la distancia angular más corta entre dos longitudes
    
    Args:
        lon1: Primera longitud
        lon2: Segunda longitud
        
    Returns:
        Distancia angular en grados (0-180°)
    """
    diff = abs(normalizar_longitud(lon1) - normalizar_longitud(lon2))
    return min(diff, 360 - diff)

def encontrar_casa_tropical(cuspide_drac_lon: float, cuspides_tropicales: List[Tuple[int, float]]) -> int:
    """
    Encuentra en qué casa tropical cae una cúspide dracónica
    
    Args:
        cuspide_drac_lon: Longitud de la cúspide dracónica
        cuspides_tropicales: Lista de tuplas (numero_casa, longitud) en orden natural 1-12
        
    Returns:
        Número de casa tropical (1-12)
    """
    cuspide_drac_lon = normalizar_longitud(cuspide_drac_lon)
    
    # Recorrer las casas en orden natural (1-12)
    for i in range(len(cuspides_tropicales)):
        casa_actual = cuspides_tropicales[i][0]
        lon_actual = normalizar_longitud(cuspides_tropicales[i][1])
        
        # Obtener siguiente cúspide (circular: después de casa 12 viene casa 1)
        siguiente_idx = (i + 1) % len(cuspides_tropicales)
        lon_siguiente = normalizar_longitud(cuspides_tropicales[siguiente_idx][1])
        
        # Determinar si la cúspide dracónica cae en esta casa tropical
        if lon_actual > lon_siguiente:
            # Cruce de 0°/360° (ej: casa 12 a casa 1)
            if cuspide_drac_lon >= lon_actual or cuspide_drac_lon < lon_siguiente:
                return casa_actual
        else:
            # Caso normal (sin cruce de 0°/360°)
            if lon_actual <= cuspide_drac_lon < lon_siguiente:
                return casa_actual
    
    # Fallback: devolver casa 1
    return 1

def calcular_distancia_cuspide(cuspide_drac_lon: float, cuspides_tropicales: List[Tuple[int, float]], casa_tropical: int) -> Dict[str, Any]:
    """
    Calcula la distancia desde la cúspide dracónica hasta la cúspide tropical más cercana
    
    Args:
        cuspide_drac_lon: Longitud de la cúspide dracónica
        cuspides_tropicales: Lista de cúspides tropicales
        casa_tropical: Casa tropical donde cae la cúspide dracónica
        
    Returns:
        Diccionario con información de distancia
    """
    # Encontrar la cúspide tropical de la casa
    cuspide_tropical_lon = None
    for casa, lon in cuspides_tropicales:
        if casa == casa_tropical:
            cuspide_tropical_lon = lon
            break
    
    if cuspide_tropical_lon is None:
        return {"grados": 0, "minutos": 0, "direccion": "exacto"}
    
    # Calcular distancia considerando dirección
    cuspide_drac_lon = normalizar_longitud(cuspide_drac_lon)
    cuspide_tropical_lon = normalizar_longitud(cuspide_tropical_lon)
    
    # Calcular diferencia con signo
    diff = cuspide_drac_lon - cuspide_tropical_lon
    
    # Normalizar diferencia para obtener la distancia más corta
    if diff > 180:
        diff -= 360
    elif diff < -180:
        diff += 360
    
    # Determinar dirección
    if abs(diff) < 0.01:  # Prácticamente exacto
        direccion = "exacto"
        grados_abs = 0
    elif diff > 0:
        direccion = "después"
        grados_abs = diff
    else:
        direccion = "antes"
        grados_abs = abs(diff)
    
    grados = int(grados_abs)
    minutos = int((grados_abs % 1) * 60)
    
    return {
        "grados": grados,
        "minutos": minutos,
        "direccion": direccion
    }

def calcular_cuspides_cruzadas(carta_tropical: dict, carta_draconica: dict) -> List[dict]:
    """
    Calcula en qué casa tropical cae cada cúspide dracónica
    
    Args:
        carta_tropical: Diccionario con datos de carta tropical
        carta_draconica: Diccionario con datos de carta dracónica
        
    Returns:
        Lista de diccionarios con información de cúspides cruzadas
    """
    cuspides_cruzadas = []
    
    # Crear lista de cúspides tropicales en orden natural (1-12)
    # NO ordenar por longitud para mantener secuencia correcta de casas
    cuspides_tropicales = []
    for casa in range(1, 13):
        if str(casa) in carta_tropical['houses']:
            lon = carta_tropical['houses'][str(casa)]['longitude']
            cuspides_tropicales.append((casa, lon))
    
    # Mantener orden natural de casas 1-12 (NO ordenar por longitud)
    
    # Para cada cúspide dracónica
    for casa_drac in range(1, 13):
        if str(casa_drac) not in carta_draconica['houses']:
            continue
            
        casa_drac_data = carta_draconica['houses'][str(casa_drac)]
        cuspide_drac_lon = casa_drac_data['longitude']
        
        # Encontrar casa tropical
        casa_tropical = encontrar_casa_tropical(cuspide_drac_lon, cuspides_tropicales)
        
        # Calcular distancia
        distancia_info = calcular_distancia_cuspide(cuspide_drac_lon, cuspides_tropicales, casa_tropical)
        
        cuspides_cruzadas.append({
            'casa_draconica': casa_drac,
            'signo_draconica': casa_drac_data['sign'],
            'grados_draconica': casa_drac_data['degrees'],  # Devolver grados decimales
            'casa_tropical_ubicacion': casa_tropical,
            'distancia_desde_cuspide': distancia_info,
            'descripcion': f"Casa {casa_drac} Dracónica ({casa_drac_data['sign']} {casa_drac_data['degrees']}°) cae en Casa {casa_tropical} Tropical"
        })
    
    return cuspides_cruzadas

def calcular_aspectos_entre_puntos(lon_drac: float, lon_trop: float, orbe_conjuncion: float, orbe_oposicion: float) -> List[Dict[str, Any]]:
    """
    Calcula aspectos (conjunción/oposición) entre dos puntos
    
    Args:
        lon_drac: Longitud del punto dracónico
        lon_trop: Longitud del punto tropical
        orbe_conjuncion: Orbe para conjunciones
        orbe_oposicion: Orbe para oposiciones
        
    Returns:
        Lista de aspectos encontrados
    """
    aspectos = []
    distancia = calcular_distancia_angular(lon_drac, lon_trop)
    
    # Verificar conjunción (0°)
    if distancia <= orbe_conjuncion:
        aspectos.append({
            'tipo': 'Conjunción',
            'orbe': distancia
        })
    
    # Verificar oposición (180°)
    orbe_oposicion_real = abs(distancia - 180)
    if orbe_oposicion_real <= orbe_oposicion:
        aspectos.append({
            'tipo': 'Oposición',
            'orbe': orbe_oposicion_real
        })
    
    return aspectos

def calcular_aspectos_cruzados(carta_tropical: dict, carta_draconica: dict, 
                              orbe_conjuncion: float = 8.0, orbe_oposicion: float = 8.0) -> List[dict]:
    """
    Calcula conjunciones y oposiciones entre planetas dracónicos y tropicales
    
    Args:
        carta_tropical: Diccionario con datos de carta tropical
        carta_draconica: Diccionario con datos de carta dracónica
        orbe_conjuncion: Orbe para conjunciones (default: 8°)
        orbe_oposicion: Orbe para oposiciones (default: 8°)
        
    Returns:
        Lista de aspectos cruzados ordenados por exactitud
    """
    aspectos_cruzados = []
    
    for punto_drac in PUNTOS_PRINCIPALES:
        if punto_drac not in carta_draconica['points']:
            continue
            
        punto_drac_data = carta_draconica['points'][punto_drac]
        lon_drac = punto_drac_data['longitude']
        
        for punto_trop in PUNTOS_PRINCIPALES:
            if punto_trop not in carta_tropical['points']:
                continue
            
            # Evitar comparar mismo punto consigo mismo
            if punto_drac == punto_trop:
                continue
                
            punto_trop_data = carta_tropical['points'][punto_trop]
            lon_trop = punto_trop_data['longitude']
            
            # Calcular aspectos
            aspectos = calcular_aspectos_entre_puntos(lon_drac, lon_trop, orbe_conjuncion, orbe_oposicion)
            
            for aspecto in aspectos:
                aspectos_cruzados.append({
                    'punto_draconico': punto_drac,
                    'signo_draconico': punto_drac_data['sign'],
                    'grados_draconico': punto_drac_data['degrees'],  # Grados decimales
                    'punto_tropical': punto_trop,
                    'signo_tropical': punto_trop_data['sign'],
                    'grados_tropical': punto_trop_data['degrees'],  # Grados decimales
                    'tipo_aspecto': aspecto['tipo'],
                    'orbe_grados': int(aspecto['orbe']),
                    'orbe_minutos': int((aspecto['orbe'] % 1) * 60),
                    'orbe_decimal': round(aspecto['orbe'], 2),
                    'exacto': aspecto['orbe'] < 1.0,
                    'descripcion': f"{punto_drac} Dracónico ({punto_drac_data['sign']} {punto_drac_data['degrees']}°) {aspecto['tipo'].lower()} {punto_trop} Tropical ({punto_trop_data['sign']} {punto_trop_data['degrees']}°) - Orbe: {int(aspecto['orbe'])}°{int((aspecto['orbe'] % 1) * 60)}'"
                })
    
    # Ordenar por exactitud (orbe más pequeño primero)
    aspectos_cruzados.sort(key=lambda x: x['orbe_decimal'])
    
    return aspectos_cruzados
