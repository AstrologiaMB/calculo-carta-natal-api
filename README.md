# 🌟 Carta Natal API - Microservicio de Cálculo Astrológico

Microservicio FastAPI especializado en el cálculo de cartas natales astrológicas de alta precisión. Genera cartas tropicales y dracónicas utilizando Swiss Ephemeris y la biblioteca Immanuel, proporcionando datos astronómicos exactos para el ecosistema [Astrowellness](https://github.com/AstrologiaMB/homepageastrowellness).

## 🎯 Características Principales

### ✨ **Cálculos Astrológicos Avanzados**
- **Cartas Tropicales**: Sistema zodiacal estándar occidental
- **Cartas Dracónicas**: Sistema basado en los nodos lunares
- **Swiss Ephemeris**: Máxima precisión astronómica disponible
- **Biblioteca Immanuel**: Motor de cálculo astrológico profesional
- **Geocodificación Automática**: Conversión de ciudades a coordenadas precisas

### 🚀 **Tecnología Moderna**
- **FastAPI**: API REST de alta performance con documentación automática
- **Pydantic**: Validación robusta de datos y modelos tipados
- **CORS Configurado**: Integración seamless con frontend React
- **Logging Avanzado**: Sistema de logs configurable para debugging
- **Health Checks**: Monitoreo automático del estado del servicio

### 🔮 **Funcionalidades Únicas**
- **Formato Dual**: Datos completos y formato reducido para AstroChart
- **Manejo de Zonas Horarias**: Cálculo automático según ubicación
- **Validación Inteligente**: Verificación de datos de entrada
- **API RESTful**: Endpoints claros y bien documentados

## 🏗️ Arquitectura del Sistema

```
calculo-carta-natal-api/
├── app.py                          # FastAPI application principal
├── main.py                         # Motor de cálculo astrológico
├── models.py                       # Modelos Pydantic para requests/responses
├── config.py                       # Configuración del microservicio
├── requirements.txt                # Dependencias Python
├── cline_docs/                     # Documentación del proyecto
├── src/                            # Código fuente modular
│   ├── calculators/                # Calculadores especializados
│   └── immanuel/                   # Biblioteca Immanuel personalizada
└── README.md                       # Documentación completa
```

## 🌟 Tipos de Cartas Soportadas

### **Carta Tropical** 🌞
- **Sistema**: Zodíaco tropical estándar
- **Punto 0°**: Equinoccio de primavera
- **Uso**: Astrología occidental tradicional
- **Características**: Signos fijos respecto a las estaciones

### **Carta Dracónica** 🐉
- **Sistema**: Basado en los nodos lunares
- **Punto 0°**: Nodo Norte lunar como 0° Aries
- **Uso**: Astrología kármica y evolutiva
- **Características**: Revela patrones del alma y propósito espiritual

## 🚀 Inicio Rápido

### 1. **Instalación**
```bash
# Clonar el repositorio
git clone https://github.com/AstrologiaMB/calculo-carta-natal-api.git
cd calculo-carta-natal-api

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. **Iniciar el Microservicio**
```bash
# Opción 1: Usando Python directamente
python app.py

# Opción 2: Usando Uvicorn
uvicorn app:app --host 0.0.0.0 --port 8001 --reload
```

### 3. **Verificar Funcionamiento**
```bash
# Health check
curl http://localhost:8001/health

# Información del servicio
curl http://localhost:8001/
```

El servicio estará disponible en:
- **API**: http://localhost:8001
- **Documentación**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

## 📚 API Endpoints

### **Cálculo de Carta Tropical**
```http
POST /carta-natal/tropical
Content-Type: application/json

{
  "nombre": "Luis Minvielle",
  "fecha_nacimiento": "1964-12-26",
  "hora_nacimiento": "21:12",
  "ciudad_nacimiento": "Buenos Aires",
  "pais_nacimiento": "Argentina"
}
```

### **Cálculo de Carta Dracónica**
```http
POST /carta-natal/draconica
Content-Type: application/json

{
  "nombre": "Luis Minvielle",
  "fecha_nacimiento": "1964-12-26",
  "hora_nacimiento": "21:12",
  "ciudad_nacimiento": "Buenos Aires",
  "pais_nacimiento": "Argentina"
}
```

### **✨ NUEVO: Análisis Cruzado Dracónico-Tropical**
```http
POST /carta-natal/cruzada
Content-Type: application/json

{
  "nombre": "Luis Minvielle",
  "fecha_nacimiento": "1964-12-26",
  "hora_nacimiento": "21:12",
  "ciudad_nacimiento": "Buenos Aires",
  "pais_nacimiento": "Argentina"
}
```

**Respuesta del Análisis Cruzado:**
```json
{
  "success": true,
  "data": {
    "tipo_analisis": "cruzado_draconico_tropical",
    "carta_tropical": { /* carta tropical completa */ },
    "carta_draconica": { /* carta dracónica completa */ },
    "cuspides_cruzadas": [
      {
        "casa_draconica": 1,
        "signo_draconica": "Aries",
        "grados_draconica": "29°28'",
        "casa_tropical_ubicacion": 9,
        "distancia_desde_cuspide": {
          "grados": 17,
          "minutos": 19,
          "direccion": "después"
        },
        "descripcion": "Casa 1 Dracónica (Aries 29°28') cae en Casa 9 Tropical"
      }
      // ... 11 cúspides más
    ],
    "aspectos_cruzados": [
      {
        "punto_draconico": "Venus",
        "punto_tropical": "Pluto",
        "tipo_aspecto": "Conjunción",
        "orbe_decimal": 0.34,
        "exacto": true,
        "descripcion": "Venus Dracónico conjunción Pluto Tropical - Orbe: 0°20'"
      }
      // ... más aspectos
    ],
    "metadata": {
      "total_cuspides": 12,
      "total_aspectos": 18,
      "orbe_conjuncion": 8.0,
      "orbe_oposicion": 8.0
    }
  }
}
```

### **Respuesta Típica**
```json
{
  "success": true,
  "data": {
    "nombre": "Luis Minvielle",
    "fecha_hora_natal": "1964-12-26 21:12",
    "lugar": "Buenos Aires, Argentina",
    "coordenadas": {
      "latitud": -34.6118,
      "longitud": -58.3960,
      "zona_horaria": "America/Argentina/Buenos_Aires"
    },
    "planetas": {
      "Sol": {
        "signo": "Capricornio",
        "grados": 4.5,
        "casa": 6,
        "retrogrado": false
      },
      "Luna": {
        "signo": "Cáncer",
        "grados": 12.3,
        "casa": 12,
        "retrogrado": false
      }
      // ... más planetas
    },
    "casas": {
      "1": {
        "signo": "Cáncer",
        "grados": 28.7
      }
      // ... más casas
    },
    "aspectos": [
      {
        "planeta1": "Sol",
        "planeta2": "Luna",
        "aspecto": "Oposición",
        "orbe": 2.1,
        "exacto": false
      }
      // ... más aspectos
    ]
  },
  "data_reducido": {
    // Formato optimizado para AstroChart
    "planets": [...],
    "houses": [...],
    "aspects": [...]
  }
}
```

### **Endpoints de Monitoreo**
- `GET /` - Información básica del servicio
- `GET /health` - Health check completo con validación de dependencias
- `GET /docs` - Documentación interactiva Swagger
- `GET /redoc` - Documentación alternativa ReDoc

## 🧮 Proceso de Cálculo

### **1. Validación de Entrada**
```python
# Validación automática con Pydantic
request = UserDataRequest(
    nombre="Luis Minvielle",
    fecha_nacimiento="1964-12-26",
    hora_nacimiento="21:12",
    ciudad_nacimiento="Buenos Aires",
    pais_nacimiento="Argentina"
)
```

### **2. Geocodificación**
```python
# Conversión automática de ciudad a coordenadas
lat, lon, timezone = get_coordinates("Buenos Aires", "Argentina")
# Resultado: -34.6118, -58.3960, "America/Argentina/Buenos_Aires"
```

### **3. Cálculo Astronómico**
```python
# Usando Swiss Ephemeris a través de Immanuel
carta = calcular_carta_natal(datos_usuario, draconica=False)
# Precisión: décimas de segundo de arco
```

### **4. Formato de Salida**
```python
# Dos formatos: completo y reducido
resultado_completo = carta  # Todos los datos
resultado_reducido = generar_json_reducido(carta)  # Para AstroChart
```

## 🔧 Configuración Técnica

### **Dependencias Principales**
- **Python**: 3.8+
- **FastAPI**: Framework web moderno
- **Immanuel**: Biblioteca de cálculos astrológicos
- **Swiss Ephemeris**: Motor astronómico de precisión
- **Geopy**: Geocodificación de ubicaciones
- **TimezoneFinder**: Determinación automática de zonas horarias

### **Variables de Entorno**
```env
# Puerto del servidor
PORT=8001

# Host de binding
HOST=0.0.0.0

# Orígenes CORS permitidos
CORS_ORIGINS=["http://localhost:3000"]

# Nivel de logging
LOG_LEVEL=INFO
```

### **Configuración por Defecto**
- **Puerto**: 8001
- **Host**: 0.0.0.0 (todas las interfaces)
- **CORS**: Configurado para localhost:3000
- **Logging**: Nivel INFO con archivo de log

## 🔗 Integración con Ecosistema Astrowellness

### **Frontend React (sidebar-fastapi)**
```typescript
// Llamada desde el frontend
const response = await fetch('http://localhost:8001/carta-natal/tropical', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    nombre: 'Luis Minvielle',
    fecha_nacimiento: '1964-12-26',
    hora_nacimiento: '21:12',
    ciudad_nacimiento: 'Buenos Aires',
    pais_nacimiento: 'Argentina'
  })
});

const { data } = await response.json();
console.log(`Carta calculada para: ${data.nombre}`);
```

### **Integración con Otros Microservicios**
- **Puerto 8001**: **Carta Natal** (este servicio)
- **Puerto 8002**: Interpretaciones RAG
- **Puerto 8003**: Astrogematría
- **Puerto 8004**: Calendario Personal

### **Flujo de Datos**
```
Frontend → Datos Natales → Carta Natal API → Cálculo → Carta Completa → Frontend
```

## 🧪 Ejemplos de Uso

### **Ejemplo 1: Carta Tropical Básica**
```bash
curl -X POST http://localhost:8001/carta-natal/tropical \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Luis Minvielle",
    "fecha_nacimiento": "1964-12-26",
    "hora_nacimiento": "21:12",
    "ciudad_nacimiento": "Buenos Aires",
    "pais_nacimiento": "Argentina"
  }'
```

### **Ejemplo 2: Carta Dracónica**
```bash
curl -X POST http://localhost:8001/carta-natal/draconica \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "María García",
    "fecha_nacimiento": "1985-03-15",
    "hora_nacimiento": "14:30",
    "ciudad_nacimiento": "Madrid",
    "pais_nacimiento": "España"
  }'
```

### **Ejemplo 3: Con Ubicación Internacional**
```bash
curl -X POST http://localhost:8001/carta-natal/tropical \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "John Smith",
    "fecha_nacimiento": "1990-07-04",
    "hora_nacimiento": "09:45",
    "ciudad_nacimiento": "New York",
    "pais_nacimiento": "United States"
  }'
```

## 📊 Rendimiento y Optimización

### **Métricas Típicas**
- **Tiempo de respuesta**: 500ms - 2s por carta (dependiendo de complejidad)
- **Memoria**: ~50MB en funcionamiento
- **CPU**: Uso moderado durante cálculos
- **Concurrencia**: Soporta múltiples requests simultáneos

### **Optimizaciones Implementadas**
- Cache de coordenadas geográficas
- Reutilización de conexiones de base de datos efemeris
- Validación rápida de entrada
- Logging configurable para performance

## 🔍 Datos Calculados

### **Planetas Incluidos**
- **Luminarias**: Sol, Luna
- **Planetas Personales**: Mercurio, Venus, Marte
- **Planetas Sociales**: Júpiter, Saturno
- **Planetas Transpersonales**: Urano, Neptuno, Plutón
- **Puntos Especiales**: Nodo Norte, Nodo Sur, Lilith

### **Sistema de Casas**
- **Método**: Placidus (por defecto)
- **Casas**: 12 casas completas con cúspides exactas
- **Ángulos**: Ascendente, Medio Cielo, Descendente, Fondo del Cielo

### **Aspectos Calculados**
- **Mayores**: Conjunción (0°), Oposición (180°), Cuadratura (90°), Trígono (120°), Sextil (60°)
- **Menores**: Semicuadratura (45°), Sesquicuadratura (135°), Quintil (72°)
- **Orbes**: Configurables según tipo de aspecto y planetas involucrados

## 🔍 Solución de Problemas

### **Error: Puerto 8001 en uso**
```bash
# Liberar puerto
kill $(lsof -ti:8001)
python app.py
```

### **Error: Dependencias faltantes**
```bash
# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

### **Error: Ubicación no encontrada**
```bash
# Verificar formato de ciudad y país
# Usar nombres en inglés para mejor compatibilidad
# Ejemplo: "Buenos Aires", "Argentina" (no "Buenos Aires, Argentina")
```

### **Logs y Debugging**
```bash
# Ver logs en tiempo real
tail -f carta_natal_api.log

# Verificar health check
curl http://localhost:8001/health
```

## 🧪 Testing y Validación

### **Test Básico**
```python
# Test de la función core
from main import calcular_carta_natal

datos = {
    "nombre": "Test User",
    "fecha_hora_natal": "1990-01-01 12:00",
    "lat": 0.0,
    "lon": 0.0,
    "zona_horaria": "UTC"
}

resultado = calcular_carta_natal(datos, draconica=False)
print(resultado)  # Debería mostrar carta completa
```

### **Validación de Precisión**
- Comparación con software astrológico profesional
- Tests unitarios para casos edge
- Validación de coordenadas geográficas

## 📚 Documentación Adicional

- **[API Documentation](http://localhost:8001/docs)** - Documentación interactiva Swagger
- **[ReDoc](http://localhost:8001/redoc)** - Documentación alternativa
- **[Health Check](http://localhost:8001/health)** - Estado del servicio
- **[Ecosistema Astrowellness](https://github.com/AstrologiaMB/homepageastrowellness)** - Proyecto principal

## 🤝 Contribución

Este microservicio es parte del ecosistema Astrowellness. Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### **Áreas de Contribución**
- Nuevos sistemas de casas (Koch, Campanus, etc.)
- Soporte para más puntos astrológicos (asteroides, etc.)
- Optimizaciones de performance
- Documentación y ejemplos
- Tests y validaciones

## 📄 Licencia

Este proyecto es parte del ecosistema Astrowellness desarrollado por AstrologiaMB.

## 🔮 Roadmap

- [ ] **Sistemas de Casas Adicionales**: Koch, Campanus, Regiomontanus
- [ ] **Asteroides**: Ceres, Pallas, Juno, Vesta
- [ ] **Puntos Arábigos**: Parte de la Fortuna, etc.
- [ ] **Cache Inteligente**: Redis para cálculos frecuentes
- [ ] **Batch Processing**: Cálculo de múltiples cartas simultáneamente
- [ ] **API Versioning**: Versionado de endpoints
- [ ] **Métricas Avanzadas**: Monitoring y analytics
- [ ] **Rectificación**: Herramientas de corrección horaria

## 📞 Soporte

Para soporte técnico o preguntas sobre integración:
- **Issues**: GitHub Issues del repositorio
- **Health Check**: Verificar `/health` endpoint
- **Documentación**: Consultar `/docs` para API reference
- **Logs**: Revisar `carta_natal_api.log` para errores específicos

---

**🌟 Desarrollado con precisión astronómica por el equipo de AstrologiaMB**

*Microservicio de carta natal - Versión 1.0.0*
