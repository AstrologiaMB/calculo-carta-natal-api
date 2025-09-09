# Active Context: Microservicio Carta Natal - Proyecto Astrowellness

## What you're working on now

✅ **RAG SEPARATION COMPLETADO** - Implementación exitosa de RAGs separados para resolver contaminación cruzada entre interpretaciones tropicales y dracónicas.

**Estado Actual:**
- ✅ Feature flag `USE_SEPARATE_ENGINES = True` activado
- ✅ Tres índices RAG funcionando: TROPICAL (22 docs), DRACÓNICO (7 docs), MIXTO (29 docs backup)
- ✅ Contaminación cruzada eliminada: consultas tropicales → contenido tropical puro, consultas dracónicas → contenido dracónico puro
- ✅ Zero downtime durante implementación
- ✅ Sistema con fallback automático a índice mixto en caso de error

**Microservicio FastAPI para cálculo de cartas natales con análisis cruzado dracónico-tropical también completado exitosamente.**

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
- ✅ FastAPI wrapper completamente implementado
- ✅ Endpoints HTTP funcionando perfectamente
- ✅ **NUEVO:** Análisis cruzado dracónico-tropical implementado

## Recent changes

### **✅ IMPLEMENTACIÓN COMPLETADA - Análisis Cruzado Dracónico-Tropical**

**Último cambio (Agosto 2025):** Implementación exitosa del análisis cruzado entre cartas dracónicas y tropicales.

### **FastAPI Microservicio Completado**
1. **app.py Funcional:** Microservicio FastAPI completo con:
   - Endpoints HTTP: `/carta-natal/tropical`, `/carta-natal/draconica`, `/carta-natal/cruzada`
   - Middleware de CORS configurado para sidebar-fastapi
   - Logging estructurado y manejo de errores
   - Documentación automática con Swagger UI
   - Health check endpoint

2. **Modelos Pydantic Implementados:**
   - `UserDataRequest` - Validación de datos de entrada
   - `CartaNatalResponse` - Respuesta estándar para todos los endpoints
   - `HealthResponse` - Health check
   - `ErrorResponse` - Manejo de errores
   - Modelos internos para tipado de análisis cruzados

3. **Nuevo Módulo de Análisis Cruzado:**
   - `src/calculators/cross_chart_calculator.py` - Algoritmos verificados
   - Cálculo de cúspides cruzadas (12 cúspides dracónicas → casas tropicales)
   - Cálculo de aspectos cruzados (conjunciones y oposiciones)
   - Quirón incluido, Lilith excluido según especificaciones
   - Orbes configurables (8° por defecto)

### **Testing Exitoso Completado**
- **18 aspectos cruzados** encontrados con datos reales
- **12 cúspides cruzadas** correctamente mapeadas
- **Aspectos exactos** verificados: Venus Dracónico ♂ Plutón Tropical (orbe 0°20')
- **Formato RAG** compatible con microservicio interpretador
- **Swagger UI** funcionando correctamente

### **Archivos Clave Implementados**
- `app.py` - FastAPI wrapper completo
- `models.py` - Modelos Pydantic
- `config.py` - Configuración del servicio
- `src/calculators/cross_chart_calculator.py` - Algoritmos de análisis cruzado
- `requirements.txt` - Dependencias actualizadas

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
