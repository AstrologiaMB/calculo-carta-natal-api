"""
Módulo para el cálculo de cartas natales usando nuestra implementación local de Immanuel.
"""
from datetime import datetime
from typing import Dict, Any
from zoneinfo import ZoneInfo
from ..immanuel import Subject, Natal
from ..immanuel.const import chart
from ..immanuel.setup import settings

# Configurar objetos a incluir en el cálculo
settings.objects = [
    # Planetas
    chart.SUN, chart.MOON, chart.MERCURY, chart.VENUS, chart.MARS,
    chart.JUPITER, chart.SATURN, chart.URANUS, chart.NEPTUNE, chart.PLUTO,
    # Ángulos
    chart.ASC, chart.MC,
    # Puntos especiales
    chart.TRUE_NORTH_NODE, chart.LILITH, chart.CHIRON,
    chart.PART_OF_FORTUNE, chart.VERTEX
]

def _convertir_formato_carta(natal_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convierte el formato de la carta natal de Immanuel al formato esperado por main.py
    """
    result = {
        'points': {},
        'houses': {},
        'location': natal_data.get('location', {})
    }
    
    # Convertir objetos
    for index, obj in natal_data.get('objects', {}).items():
        # Extraer datos básicos
        point_data = {
            'sign': obj.sign.name,
            'position': str(obj.sign_longitude.formatted),
            'retrograde': obj.movement.retrograde if hasattr(obj, 'movement') else False
        }
        
        # Usar el nombre del objeto como clave
        result['points'][obj.name] = point_data
    
    # Convertir casas
    for index, house in natal_data.get('houses', {}).items():
        result['houses'][str(house.number)] = {
            'sign': house.sign.name,
            'position': str(house.sign_longitude.formatted)
        }
    
    return result

def calcular_carta_natal(datos_usuario: Dict[str, Any]) -> Dict[str, Any]:
    """
    Función principal para calcular una carta natal usando Immanuel.
    
    Args:
        datos_usuario: Diccionario con los datos del usuario:
            - hora_local: str (formato ISO)
            - lat: float
            - lon: float
            - zona_horaria: str
            
    Returns:
        Dict con la carta natal calculada
    """
    try:
        # Usar coordenadas directamente
        latitude = datos_usuario['lat']
        longitude = datos_usuario['lon']
        
        # Usar tiempo local directamente como hace cartaimmanuel
        local_time = datetime.fromisoformat(datos_usuario['hora_local'])
        
        # Crear sujeto para la carta natal
        native = Subject(
            date_time=local_time,
            latitude=latitude,
            longitude=longitude
        )
        
        # Calcular carta natal usando Immanuel
        natal_chart = Natal(native)
        raw_data = natal_chart.to_dict()
        
        # Agregar información de ubicación
        raw_data['location'] = {
            'latitude': datos_usuario['lat'],
            'longitude': datos_usuario['lon'],
            'name': datos_usuario.get('lugar', 'Unknown'),
            'timezone': datos_usuario['zona_horaria']
        }
        
        # Convertir al formato esperado
        result = _convertir_formato_carta(raw_data)
        return result
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error detallado:\n{error_details}")
        raise ValueError(f"Error calculando carta natal: {str(e)}")
