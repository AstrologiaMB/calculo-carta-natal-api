# Active Context: Microservicio Carta Natal - Proyecto Astrowellness

## What you're working on now

Estamos trabajando en la conversión del programa Python de cálculo de cartas natales en un microservicio FastAPI para el proyecto Astrowellness. Este microservicio será consumido por la aplicación frontend Next.js (sidebar-fastapi) a través de endpoints HTTP.

**Rol en la Arquitectura:**
```
Astrowellness (Proyecto Principal)
├── sidebar-fastapi/ (Frontend Next.js + API Gateway)
└── calculo-carta-natal-api/ (Microservicio Python - ESTE PROYECTO)
    └── [futuros microservicios Python...]
```

**Estado Actual:**
- ✅ Programa Python completamente funcional (main.py)
- ✅ Entorno virtual configurado con dependencias
- ✅ Función generar_json_reducido() compatible con AstroChart
- ❌ FastAPI wrapper pendiente de implementación
- ❌ Endpoints HTTP no implementados

## Recent changes

### **Programa Python Base Completado**
1. **main.py Funcional:** Implementación completa con:
   - Cálculo de cartas natales tropicales y dracónicas usando biblioteca `immanuel`
   - Geocodificación automática con `geopy` y `timezonefinder`
   - Función `calcular_carta_natal()` que acepta datos de usuario y retorna carta completa
   - Función `generar_json_reducido()` que convierte al formato AstroChart
   - Manejo de aspectos, casas, planetas y ángulos
   - Validación de datos de entrada y manejo de errores

2. **Formato de Datos Optimizado:** 
   - JSON reducido compatible con @astrodraw/astrochart
   - Conversión de planetas a arrays con longitud absoluta (0-360°)
   - Indicadores de retrogradación (-0.1)
   - Transformación de casas a array "cusps"
   - Renombramiento de "True North Node" a "NNode"

3. **Entorno Técnico:**
   - Virtual environment (venv/) configurado
   - Dependencias instaladas: immanuel, geopy, timezonefinder, zoneinfo
   - Archivos de ejemplo generados y probados

### **Archivos de Ejemplo Generados**
- `carta_astrochart_tropical_Lmapi_Buenos_Aires_26-12-1964.json`
- `carta_astrochart_draconica_Lmapi_Buenos_Aires_26-12-1964.json`
- Datos completos y reducidos disponibles para testing

## Next steps

### **Fase 1: Implementar FastAPI Wrapper (INMEDIATO)**
1. **Crear app.py con FastAPI:**
   - Importar y reutilizar funciones de main.py
   - Configurar CORS para sidebar-fastapi
   - Implementar logging y manejo de errores

2. **Implementar Endpoints HTTP:**
   - `POST /carta-natal/tropical` - Calcular carta natal trópica
   - `POST /carta-natal/draconica` - Calcular carta dracónica  
   - `GET /health` - Health check del servicio
   - `GET /` - Información del servicio

3. **Modelos de Datos con Pydantic:**
   - `UserDataRequest` - Datos de entrada del usuario
   - `CartaNatalResponse` - Respuesta con carta natal
   - `ErrorResponse` - Manejo de errores

4. **Configuración del Servidor:**
   - Puerto configurable (default: 8001)
   - Configuración de CORS para desarrollo
   - Logging estructurado

### **Fase 2: Testing y Validación**
1. **Testing Local:**
   - Probar endpoints con curl/Postman
   - Validar formato de respuesta
   - Verificar manejo de errores

2. **Integración con Frontend:**
   - Coordinar con sidebar-fastapi
   - Probar comunicación entre servicios
   - Validar datos en componentes React

### **Fase 3: Optimización**
1. **Performance:**
   - Optimizar cálculos astrológicos
   - Implementar caché local si es necesario
   - Monitoreo de tiempos de respuesta

2. **Documentación:**
   - OpenAPI/Swagger automático
   - Documentación de endpoints
   - Ejemplos de uso

## Decisiones Técnicas

- **Reutilización de Código:** Mantener main.py intacto y crear wrapper FastAPI
- **Separación de Responsabilidades:** FastAPI solo como capa HTTP, lógica en main.py
- **Formato de Datos:** Usar función generar_json_reducido() existente
- **Puerto del Servicio:** 8001 (para evitar conflicto con Next.js en 3000)
- **CORS:** Permitir requests desde localhost:3000 (sidebar-fastapi)
- **Manejo de Errores:** Respuestas HTTP estándar con detalles de error

## Integración con Proyecto Principal

Este microservicio será consumido por sidebar-fastapi a través de:
1. **API Gateway:** sidebar-fastapi actuará como proxy
2. **Autenticación:** sidebar-fastapi manejará auth, este servicio recibe datos validados
3. **Caché:** sidebar-fastapi implementará caché usando Prisma
4. **Fallback:** sidebar-fastapi tendrá datos locales como respaldo

## Archivos Clave

- `main.py` - Programa Python base (NO MODIFICAR)
- `app.py` - FastAPI wrapper (A CREAR)
- `requirements.txt` - Dependencias (A CREAR)
- `models.py` - Modelos Pydantic (A CREAR)
- `config.py` - Configuración (A CREAR)
