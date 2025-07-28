# Tech Context: Carta Natal App

## Technologies used

### Lenguajes de programación
- **Python**: Lenguaje principal para la lógica de la aplicación
- **HTML/CSS/JavaScript**: Utilizados en las visualizaciones generadas

### Bibliotecas y frameworks principales
1. **Astrología y cálculos astronómicos**:
   - `immanuel`: Biblioteca para cálculos astrológicos precisos
   - `zoneinfo`: Manejo de zonas horarias

2. **Geolocalización**:
   - `geopy`: Conversión de nombres de lugares a coordenadas geográficas
   - `timezonefinder`: Determinación de zonas horarias basadas en coordenadas

3. **Visualización**:
   - Módulos personalizados en `src/visualizers/`
   - Posiblemente basados en bibliotecas como D3.js o similar para las visualizaciones web

4. **Utilidades estándar**:
   - `datetime`: Manejo de fechas y horas
   - `json`: Serialización y deserialización de datos
   - `webbrowser`: Apertura automática del navegador para visualizaciones

### Dependencias externas
- **AstroChart**: Biblioteca JavaScript para visualización de cartas astrológicas
  - Requiere un formato JSON específico con planetas como arrays y casas como "cusps"
  - Soporta indicadores de retrógrado y nomenclatura específica (ej. "NNode")
- **Kerykeion**: Posiblemente otra biblioteca de visualización astrológica

## Development setup

### Requisitos del sistema
- Python 3.9+ (debido al uso de zoneinfo)
- Navegador web moderno para visualizaciones

### Estructura del proyecto
```
carta_natal_astrowellness/
├── main.py                  # Punto de entrada principal
├── src/                     # Código fuente
│   ├── calculators/         # Calculadoras astrológicas
│   ├── immanuel/            # Biblioteca immanuel (posiblemente adaptada)
│   └── visualizers/         # Módulos de visualización
├── AstroChart/              # Biblioteca de visualización
├── README_JSON_REDUCIDO.md  # Documentación del formato JSON para AstroChart
└── cline_docs/              # Documentación del proyecto
```

### Instalación de dependencias
Las dependencias principales que probablemente necesiten ser instaladas:
```bash
pip install geopy timezonefinder
```

## Technical constraints

1. **Precisión de cálculos astrológicos**:
   - Los cálculos astrológicos requieren alta precisión en posiciones planetarias
   - Dependencia de efemérides astronómicas precisas

2. **Limitaciones de geolocalización**:
   - Dependencia de servicios externos para geocodificación
   - Posibles problemas con lugares poco conocidos o con nombres ambiguos
   - Limitaciones de tasa de consulta en servicios de geocodificación gratuitos

3. **Compatibilidad de visualizaciones**:
   - Las visualizaciones generadas deben ser compatibles con navegadores modernos
   - Posibles diferencias de renderizado entre navegadores

4. **Rendimiento**:
   - Los cálculos astrológicos pueden ser computacionalmente intensivos
   - Generación de visualizaciones complejas puede consumir recursos

5. **Internacionalización**:
   - Manejo de diferentes formatos de fecha/hora según la localización
   - Traducción de términos astrológicos a diferentes idiomas
   - Soporte para nombres de lugares en diferentes idiomas

6. **Almacenamiento de datos**:
   - Actualmente limitado a archivos JSON locales
   - Dos formatos de JSON: completo (detallado) y reducido (para AstroChart)
   - No hay persistencia de datos centralizada o base de datos

7. **Compatibilidad con AstroChart**:
   - Requiere un formato JSON específico para la visualización
   - Necesita transformación de datos (planetas como arrays, casas como "cusps")
   - Manejo especial para planetas retrógrados y nomenclatura específica
