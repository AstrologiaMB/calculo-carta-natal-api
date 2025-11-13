from datetime import datetime
import json
import os
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from zoneinfo import ZoneInfo
from timezonefinder import TimezoneFinder

from src.immanuel import charts
from src.immanuel.const import chart
from src.immanuel.setup import settings

# Configurar objetos y aspectos
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

# Configurar aspectos con orbes ajustados
settings.aspects = {
    0: 8,     # Conjunción con orbe de 8°
    60: 6,    # Sextil con orbe de 6°
    90: 8,    # Cuadratura con orbe de 8°
    120: 8,   # Trígono con orbe de 8°
    180: 8    # Oposición con orbe de 8°
}

def get_timezone(lat: float, lon: float) -> str:
    """Obtiene la zona horaria para unas coordenadas."""
    tf = TimezoneFinder()
    return tf.timezone_at(lat=lat, lng=lon)

def format_position(position):
    """Formatea una posición planetaria para mostrarla de forma legible."""
    retro = " (R)" if position.get('retrograde') else ""
    return f"{position['sign']} {position['degrees']}°{retro}"

def generar_json_reducido(datos_carta):
    """
    Convierte los datos completos de la carta natal a un formato reducido
    optimizado para AstroChart.
    
    Args:
        datos_carta: Diccionario con los datos completos de la carta natal
        
    Returns:
        Diccionario con los datos en formato reducido para AstroChart
    """
    # Planetas válidos para AstroChart
    planetas_validos = [
        "Sun", "Moon", "Mercury", "Venus", "Mars", 
        "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto",
        "True North Node", "Lilith", "Chiron"
    ]
    
    # Mapeo de nombres de planetas
    mapeo_nombres = {
        "True North Node": "NNode"
    }
    
    # Transformación de planetas
    planets = {}
    for key, value in datos_carta['points'].items():
        if key in planetas_validos:
            # Convertir nombre si es necesario
            nombre_planeta = mapeo_nombres.get(key, key)
            
            # Calcular longitud absoluta (0-360)
            # Convertir de "grados en signo" a "grados absolutos"
            signos = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                     "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
            signo_index = signos.index(value['sign'])
            longitud_absoluta = (signo_index * 30) + value['degrees']
            
            # Redondear a 2 decimales
            longitud_absoluta = round(longitud_absoluta, 2)
            
            # Guardar como array
            planets[nombre_planeta] = [longitud_absoluta]
            
            # Añadir indicador de retrógrado si es necesario
            if value.get('retrograde', False):
                planets[nombre_planeta].append(-0.1)  # Valor negativo indica retrógrado

    # Transformación de casas a formato de array
    cusps = []
    for i in range(1, 13):  # Casas del 1 al 12
        if str(i) in datos_carta['houses']:
            cusps.append(round(datos_carta['houses'][str(i)]['longitude'], 2))
    
    # Construcción del JSON final
    return {
        "planets": planets,
        "cusps": cusps
    }

def get_coordinates(city: str, country: str) -> tuple:
    """Obtiene las coordenadas y zona horaria de una ubicación."""
    try:
        geolocator = Nominatim(user_agent="carta_natal_app")
        location = geolocator.geocode(f"{city}, {country}", exactly_one=True, timeout=10)
        
        if location:
            timezone = get_timezone(location.latitude, location.longitude)
            if timezone:
                return location.latitude, location.longitude, timezone
            else:
                raise ValueError("No se pudo determinar la zona horaria")
        else:
            raise ValueError("No se pudo encontrar la ubicación")
            
    except GeocoderTimedOut:
        raise ValueError("Tiempo de espera agotado al buscar la ubicación")
    except Exception as e:
        raise ValueError(f"Error al buscar la ubicación: {str(e)}")

def get_coordinates_with_options(city: str, country: str, limit: int = 5) -> dict:
    """
    Obtiene coordenadas con soporte para múltiples resultados.
    Retorna estructura diferente si hay 1 vs múltiples opciones.
    
    Args:
        city: Ciudad a buscar
        country: País a buscar
        limit: Número máximo de resultados (default: 5)
        
    Returns:
        dict: Si hay 1 resultado: {"single": True, "lat": float, "lon": float, "timezone": str, "address": str}
              Si hay múltiples: {"multiple": True, "options": [{"address": str, "lat": float, "lon": float, "timezone": str}, ...]}
    """
    try:
        geolocator = Nominatim(user_agent="carta_natal_app")
        locations = geolocator.geocode(
            f"{city}, {country}", 
            exactly_one=False, 
            limit=limit,
            timeout=10
        )
        
        if not locations:
            raise ValueError("No se pudo encontrar la ubicación")
        
        if len(locations) == 1:
            # Solo una opción - retorno directo
            loc = locations[0]
            timezone = get_timezone(loc.latitude, loc.longitude)
            return {
                "single": True,
                "lat": loc.latitude,
                "lon": loc.longitude,
                "timezone": timezone,
                "address": loc.address
            }
        else:
            # Múltiples opciones - retornar para selección
            options = []
            for loc in locations:
                try:
                    tz = get_timezone(loc.latitude, loc.longitude)
                    options.append({
                        "address": loc.address,
                        "lat": loc.latitude,
                        "lon": loc.longitude,
                        "timezone": tz
                    })
                except:
                    # Si falla timezone, omitir esta opción
                    continue
            
            if not options:
                raise ValueError("No se pudieron procesar las ubicaciones encontradas")
                
            return {
                "multiple": True,
                "options": options
            }
            
    except GeocoderTimedOut:
        raise ValueError("Tiempo de espera agotado al buscar la ubicación")
    except Exception as e:
        raise ValueError(f"Error al buscar la ubicación: {str(e)}")

def calcular_carta_natal(datos_usuario: dict, draconica=False) -> dict:
    """
    Función principal para calcular una carta natal usando Immanuel.
    
    Args:
        datos_usuario: Diccionario con los datos del usuario:
            - hora_local: str (formato ISO)
            - lat: float
            - lon: float
            - zona_horaria: str
        draconica: Si es True, calcula una carta dracónica
            
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
        native = charts.Subject(
            date_time=local_time,
            latitude=latitude,
            longitude=longitude
        )
        
        # Calcular carta natal o dracónica según corresponda
        if draconica:
            print("🚨 MAIN.PY: Creando DraconicChart...")
            chart_obj = charts.DraconicChart(native)
            print("🚨 MAIN.PY: DraconicChart creado exitosamente")
        else:
            chart_obj = charts.Natal(native)
            
        raw_data = chart_obj.to_dict()
        
        # Convertir al formato esperado
        result = {
            'points': {},
            'houses': {},
            'angles': {},
            'aspects': [],
            'location': {
                'latitude': datos_usuario['lat'],
                'longitude': datos_usuario['lon'],
                'name': datos_usuario.get('lugar', 'Unknown'),
                'timezone': datos_usuario['zona_horaria']
            },
            'fecha_hora_natal': datos_usuario.get('fecha_hora_natal', '')
        }
        
        # Convertir objetos
        for index, obj in raw_data.get('objects', {}).items():
            # Extraer datos básicos
            point_data = {
                'longitude': obj.longitude.raw if hasattr(obj.longitude, 'raw') else obj.longitude,
                'latitude': (obj.latitude.raw if hasattr(obj.latitude, 'raw') else obj.latitude) if hasattr(obj, 'latitude') else 0.0,
                'distance': (obj.distance.raw if hasattr(obj.distance, 'raw') else obj.distance) if hasattr(obj, 'distance') else 0.0,
                'sign': obj.sign.name,
                'degrees': obj.sign_longitude.raw if hasattr(obj.sign_longitude, 'raw') else obj.sign_longitude,
                'retrograde': obj.movement.retrograde if hasattr(obj, 'movement') and hasattr(obj.movement, 'retrograde') else False
            }
            
            # Usar el nombre del objeto como clave
            result['points'][obj.name] = point_data
            
            # Agregar ángulos
            if obj.name in ['Asc', 'MC']:
                result['angles'][obj.name] = {
                    'longitude': obj.longitude.raw if hasattr(obj.longitude, 'raw') else obj.longitude,
                    'sign': obj.sign.name,
                    'degrees': obj.sign_longitude.raw if hasattr(obj.sign_longitude, 'raw') else obj.sign_longitude
                }
                
                # Agregar puntos opuestos (DSC y IC)
                opposite_name = 'Dsc' if obj.name == 'Asc' else 'Ic'
                opposite_longitude = ((obj.longitude.raw if hasattr(obj.longitude, 'raw') else obj.longitude) + 180) % 360
                opposite_sign_longitude = opposite_longitude % 30
                opposite_sign_index = int(opposite_longitude / 30)
                opposite_sign = ['Aries', 'Tauro', 'Géminis', 'Cáncer', 'Leo', 'Virgo', 
                               'Libra', 'Escorpio', 'Sagitario', 'Capricornio', 'Acuario', 'Piscis'][opposite_sign_index]
                
                result['angles'][opposite_name] = {
                    'longitude': opposite_longitude,
                    'sign': opposite_sign,
                    'degrees': opposite_sign_longitude
                }
        
        # Convertir casas
        for index, house in raw_data.get('houses', {}).items():
            result['houses'][str(house.number)] = {
                'longitude': house.longitude.raw if hasattr(house.longitude, 'raw') else house.longitude,
                'sign': house.sign.name,
                'degrees': house.sign_longitude.raw if hasattr(house.sign_longitude, 'raw') else house.sign_longitude
            }
        
        # Obtener aspectos usando la función de immanuel
        aspect_types = {
            0: 'Conjunción',
            60: 'Sextil',
            90: 'Cuadratura',
            120: 'Trígono',
            180: 'Oposición'
        }
        
        # Calcular aspectos
        aspects_set = set()  # Para evitar duplicados
        for p1_idx, aspects_dict in raw_data.get('aspects', {}).items():
            for p2_idx, aspect in aspects_dict.items():
                # Procesar aspectos entre todos los objetos (no solo planetas principales)
                # Comentado para incluir todos los aspectos
                # planets = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']
                # if aspect._active_name not in planets or aspect._passive_name not in planets:
                #     continue
                    
                # Crear una clave única para el aspecto
                aspect_key = tuple(sorted([aspect._active_name, aspect._passive_name]) + [aspect.type])
                if aspect_key in aspects_set:
                    continue
                aspects_set.add(aspect_key)
                
                # Convertir el tipo de aspecto a español
                if aspect.type == 'Conjunction':
                    asp_type = 'Conjunción'
                elif aspect.type == 'Sextile':
                    asp_type = 'Sextil'
                elif aspect.type == 'Square':
                    asp_type = 'Cuadratura'
                elif aspect.type == 'Trine':
                    asp_type = 'Trígono'
                elif aspect.type == 'Opposition':
                    asp_type = 'Oposición'
                else:
                    continue
                
                # Imprimir información detallada del aspecto
                print(f"\nAspecto entre {aspect._active_name} y {aspect._passive_name}:")
                print(f"Tipo: {aspect.type}")
                print(f"Orbe: {aspect.orb}")
                print(f"Distancia: {aspect.distance.raw if hasattr(aspect.distance, 'raw') else aspect.distance}")
                print(f"Diferencia: {aspect.difference.raw if hasattr(aspect.difference, 'raw') else aspect.difference}")
                print(f"Movimiento: {aspect.movement.__dict__ if hasattr(aspect.movement, '__dict__') else aspect.movement}")
                print(f"Condición: {aspect.condition.__dict__ if hasattr(aspect.condition, '__dict__') else aspect.condition}")
                
                # Agregar el aspecto con información completa
                result['aspects'].append({
                    'point1': aspect._active_name,
                    'point2': aspect._passive_name,
                    'aspect': asp_type,
                    'difference': {
                        'raw': aspect.difference.raw if hasattr(aspect.difference, 'raw') else aspect.difference,
                        'formatted': aspect.difference.formatted if hasattr(aspect.difference, 'formatted') else None,
                        'direction': aspect.difference.direction if hasattr(aspect.difference, 'direction') else None,
                        'degrees': aspect.difference.degrees if hasattr(aspect.difference, 'degrees') else None,
                        'minutes': aspect.difference.minutes if hasattr(aspect.difference, 'minutes') else None,
                        'seconds': aspect.difference.seconds if hasattr(aspect.difference, 'seconds') else None
                    },
                    'movement': {
                        'applicative': aspect.movement.applicative if hasattr(aspect.movement, 'applicative') else False,
                        'exact': aspect.movement.exact if hasattr(aspect.movement, 'exact') else False,
                        'separative': aspect.movement.separative if hasattr(aspect.movement, 'separative') else False,
                        'formatted': aspect.movement.formatted if hasattr(aspect.movement, 'formatted') else None
                    },
                    'condition': {
                        'associate': aspect.condition.associate if hasattr(aspect.condition, 'associate') else False,
                        'dissociate': aspect.condition.dissociate if hasattr(aspect.condition, 'dissociate') else False,
                        'formatted': aspect.condition.formatted if hasattr(aspect.condition, 'formatted') else None
                    }
                })
        
        # Ordenar aspectos por importancia
        aspect_order = {
            'Conjunción': 1,
            'Oposición': 2,
            'Cuadratura': 3,
            'Trígono': 4,
            'Sextil': 5
        }
        result['aspects'].sort(key=lambda x: (aspect_order[x['aspect']], x['point1'], x['point2']))
        
        return result
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error detallado:\n{error_details}")
        raise ValueError(f"Error calculando carta natal: {str(e)}")

def main():
    print("\n=== Calculadora de Carta Natal AstroWellness ===\n")
    print("(Presione Ctrl+C en cualquier momento para salir)\n")
    
    try:
        # Obtener datos del usuario
        print("Ingrese los datos de la persona:")
        while True:
            try:
                nombre = input("Nombre completo: ").strip()
                if not nombre:
                    raise ValueError("El nombre no puede estar vacío")
                if len(nombre) < 2:
                    raise ValueError("El nombre debe tener al menos 2 caracteres")
                if any(c.isdigit() for c in nombre):
                    raise ValueError("El nombre no debe contener números")
                # Capitalizar cada palabra del nombre
                nombre = ' '.join(word.capitalize() for word in nombre.split())
                break
            except ValueError as e:
                print(f"Error: {str(e)}")
                print("Por favor intente nuevamente.")

        print("\nIngrese los datos de nacimiento:")
        print("Formato de fecha: DD/MM/YYYY (ejemplo: 26/12/1964)")
        print("Formato de hora: HH:MM en 24h (ejemplo: 21:12)")
        while True:
            try:
                fecha = input("Fecha (DD/MM/YYYY): ").strip()
                # Eliminar todos los espacios y caracteres no numéricos excepto / y -
                fecha = ''.join(c for c in fecha if c.isdigit() or c in '/-')
                if '/' in fecha:
                    dia, mes, anio = map(int, fecha.split('/'))
                elif '-' in fecha:
                    dia, mes, anio = map(int, fecha.split('-'))
                else:
                    raise ValueError("Use formato DD/MM/YYYY o DD-MM-YYYY")
                
                # Validar fecha
                datetime(anio, mes, dia)
                break
            except ValueError as e:
                print(f"Error en la fecha: {str(e)}")
                print("Por favor intente nuevamente.")

        while True:
            try:
                hora = input("Hora (HH:MM): ").strip()
                # Eliminar todos los espacios
                hora = ''.join(hora.split())
                # Verificar formato HH:MM
                if not hora.count(':') == 1:
                    raise ValueError("Debe tener exactamente un ':'")
                # Separar horas y minutos
                try:
                    horas, minutos = hora.split(':')
                    # Verificar que solo hay dígitos
                    if not (horas.isdigit() and minutos.isdigit()):
                        raise ValueError("Debe contener solo números")
                    # Convertir a enteros y validar rango
                    horas, minutos = int(horas), int(minutos)
                    if not (0 <= horas <= 23 and 0 <= minutos <= 59):
                        raise ValueError("Hora fuera de rango (00:00-23:59)")
                except ValueError as e:
                    if str(e) == "not enough values to unpack (expected 2, got 1)":
                        raise ValueError("Formato inválido, use HH:MM")
                    raise
                break
            except ValueError as e:
                print("Error: Use formato HH:MM (24 horas)")
                print("Por favor intente nuevamente.")

        while True:
            try:
                ciudad = input("\nCiudad de nacimiento: ").strip()
                if ciudad.lower() in ['q', 'quit', 'exit', 'salir']:
                    print("\nPrograma terminado.")
                    return
                    
                pais = input("País de nacimiento: ").strip()
                if pais.lower() in ['q', 'quit', 'exit', 'salir']:
                    print("\nPrograma terminado.")
                    return
                
                # Limpiar y validar ciudad
                ciudad = ' '.join(''.join(c for c in ciudad if c.isalpha() or c.isspace()).split())
                if not ciudad:
                    raise ValueError("La ciudad no puede estar vacía")
                if len(ciudad) < 2:
                    raise ValueError("La ciudad debe tener al menos 2 letras")
                if not any(c.isalpha() for c in ciudad):
                    raise ValueError("La ciudad debe contener letras")
                    
                # Limpiar y validar país
                pais = ' '.join(''.join(c for c in pais if c.isalpha() or c.isspace()).split())
                if not pais:
                    raise ValueError("El país no puede estar vacío")
                if len(pais) < 2:
                    raise ValueError("El país debe tener al menos 2 letras")
                if not any(c.isalpha() for c in pais):
                    raise ValueError("El país debe contener letras")
                
                # Capitalizar primera letra de cada palabra
                ciudad = ' '.join(word.capitalize() for word in ciudad.split())
                pais = ' '.join(word.capitalize() for word in pais.split())
                break
            except ValueError as e:
                print(f"Error: {str(e)}")
                print("Por favor intente nuevamente.")
        
        # Obtener coordenadas
        print("\nBuscando coordenadas...")
        latitud, longitud, zona_horaria = get_coordinates(ciudad, pais)
        print(f"Coordenadas encontradas: {latitud}, {longitud}")
        
        # Preparar datos para el cálculo
        fecha_hora_iso = f"{anio:04d}-{mes:02d}-{dia:02d}T{horas:02d}:{minutos:02d}:00"
        fecha_hora_natal = f"{anio:04d}-{mes:02d}-{dia:02d} {horas:02d}:{minutos:02d}"
        datos_usuario = {
            "nombre": nombre,
            "hora_local": fecha_hora_iso,
            "fecha_hora_natal": fecha_hora_natal,  # Formato para Natal
            "lat": latitud,
            "lon": longitud,
            "zona_horaria": zona_horaria,
            "lugar": f"{ciudad}, {pais}"
        }
        
        # Calcular ambas cartas (tropical y dracónica)
        print("\nCalculando carta natal tropical...")
        result_tropical = calcular_carta_natal(datos_usuario, draconica=False)
        result_tropical['nombre'] = nombre  # Agregar el nombre al resultado
        result_tropical['tipo'] = 'Tropical'  # Indicar que es una carta tropical
        
        print("\nCalculando carta dracónica...")
        result_draconic = calcular_carta_natal(datos_usuario, draconica=True)
        result_draconic['nombre'] = nombre  # Agregar el nombre al resultado
        result_draconic['tipo'] = 'Dracónica'  # Indicar que es una carta dracónica
        
        # Preguntar qué carta mostrar primero
        tipo_carta = input("\n¿Qué carta desea visualizar primero? (t=tropical/d=dracónica, por defecto: t): ").lower()
        if tipo_carta == 'd':
            result = result_draconic
            result_alt = result_tropical
            print("\nMostrando carta dracónica...")
        else:
            result = result_tropical
            result_alt = result_draconic
            print("\nMostrando carta tropical...")
        
        # Guardar resultados de ambas cartas (formato completo)
        output_file_tropical = f"carta_natal_tropical_{nombre.replace(' ', '_')}_{ciudad.replace(' ', '_')}_{fecha.replace('/', '-')}.json"
        with open(output_file_tropical, 'w', encoding='utf-8') as f:
            json.dump(result_tropical, f, indent=2, ensure_ascii=False)
            
        output_file_draconic = f"carta_natal_draconica_{nombre.replace(' ', '_')}_{ciudad.replace(' ', '_')}_{fecha.replace('/', '-')}.json"
        with open(output_file_draconic, 'w', encoding='utf-8') as f:
            json.dump(result_draconic, f, indent=2, ensure_ascii=False)
        
        # Generar y guardar JSON reducido para AstroChart
        resultado_reducido_tropical = generar_json_reducido(result_tropical)
        output_file_tropical_reducido = f"carta_astrochart_tropical_{nombre.replace(' ', '_')}_{ciudad.replace(' ', '_')}_{fecha.replace('/', '-')}.json"
        with open(output_file_tropical_reducido, 'w', encoding='utf-8') as f:
            json.dump(resultado_reducido_tropical, f, indent=2, ensure_ascii=False)

        resultado_reducido_draconic = generar_json_reducido(result_draconic)
        output_file_draconic_reducido = f"carta_astrochart_draconica_{nombre.replace(' ', '_')}_{ciudad.replace(' ', '_')}_{fecha.replace('/', '-')}.json"
        with open(output_file_draconic_reducido, 'w', encoding='utf-8') as f:
            json.dump(resultado_reducido_draconic, f, indent=2, ensure_ascii=False)
            
        # Usar el archivo de la carta seleccionada para mostrar
        output_file = output_file_tropical if result['tipo'] == 'Tropical' else output_file_draconic
            
        # Mostrar resumen
        print("\nCarta Natal:")
        print("-" * 50)
        print(f"Nombre: {nombre}")
        print(f"Lugar: {result['location']['name']}")
        print(f"Coordenadas: {result['location']['latitude']:.2f}°, {result['location']['longitude']:.2f}°")
        print(f"Zona Horaria: {result['location']['timezone']}")
        
        # Posiciones planetarias
        print("\nPosiciones Planetarias:")
        print("-" * 30)
        for planeta, datos in result['points'].items():
            print(f"{planeta:8}: {format_position(datos)}")
        
        # Ángulos principales
        print("\nÁngulos Principales:")
        print("-" * 30)
        for angulo in ['Asc', 'MC', 'Dsc', 'Ic']:  # Cambiar 'Mc' a 'MC'
            if angulo in result['angles']:
                datos = result['angles'][angulo]
                print(f"{angulo:8}: {datos['sign']} {datos['degrees']}°")
            elif angulo in result['points']:  # Verificar también en points si no está en angles
                datos = result['points'][angulo]
                print(f"{angulo:8}: {datos['sign']} {datos['degrees']}°")
        
        # Casas
        print("\nCasas Astrológicas:")
        print("-" * 30)
        for num, datos in result['houses'].items():
            print(f"Casa {num:2}: {datos['sign']} {datos['degrees']}°")
            
        # Aspectos
        if result.get('aspects'):
            print("\nAspectos:")
            print("-" * 30)
            for aspecto in result['aspects']:
                # Usar el formato que proporciona Immanuel directamente
                orbe_formateado = aspecto['difference']['formatted'] if aspecto['difference']['formatted'] else f"{aspecto['difference']['raw']}°"
                movimiento = aspecto['movement']['formatted'] if aspecto['movement']['formatted'] else ("Aplicativo" if aspecto['movement']['applicative'] else "Separativo")
                condicion = aspecto['condition']['formatted'] if aspecto['condition']['formatted'] else ("Associate" if aspecto['condition']['associate'] else "Dissociate")
                
                print(f"{aspecto['point1']:8} {aspecto['aspect']:10} {aspecto['point2']:8} {orbe_formateado} ({movimiento}, {condicion})")
            
        print(f"\nCarta natal completa guardada en: {output_file}")
        print("\nArchivos JSON reducidos para AstroChart guardados en:")
        print(f"- {output_file_tropical_reducido}")
        print(f"- {output_file_draconic_reducido}")
        
    except KeyboardInterrupt:
        print("\n\nPrograma terminado.")
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("Por favor intente nuevamente.")

if __name__ == "__main__":
    main()
