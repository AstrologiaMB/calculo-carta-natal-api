# System Patterns: Carta Natal App

## How the system is built
La aplicación Carta Natal App está construida como una aplicación de línea de comandos en Python, con una arquitectura modular que separa claramente las diferentes responsabilidades:

1. **Módulo principal (main.py)**:
   - Punto de entrada de la aplicación
   - Maneja la interacción con el usuario
   - Coordina el flujo de trabajo entre los diferentes componentes

2. **Módulos de cálculo astrológico**:
   - Utiliza la biblioteca `immanuel` para realizar cálculos astrológicos precisos
   - Implementa funciones específicas para calcular cartas natales tropicales y dracónicas

3. **Módulos de visualización**:
   - Diferentes visualizadores para representar gráficamente las cartas natales
   - Genera archivos HTML interactivos que se pueden abrir en un navegador

4. **Servicios de geolocalización**:
   - Utiliza `geopy` para convertir nombres de ciudades en coordenadas geográficas
   - Emplea `timezonefinder` para determinar zonas horarias basadas en coordenadas

## Key technical decisions

1. **Uso de bibliotecas especializadas**:
   - `immanuel` para cálculos astrológicos precisos
   - `geopy` para servicios de geolocalización
   - Visualizadores personalizados para representaciones gráficas

2. **Separación de responsabilidades**:
   - Clara separación entre cálculo astrológico y visualización
   - Módulos independientes que pueden evolucionar por separado

3. **Persistencia de datos**:
   - Almacenamiento de resultados en formato JSON para facilitar su uso posterior
   - Generación de archivos JSON optimizados para AstroChart
   - Nombres de archivo que incluyen información relevante (nombre, lugar, fecha)

4. **Validación de entrada**:
   - Validación robusta de los datos ingresados por el usuario
   - Manejo de errores con mensajes claros y descriptivos

5. **Visualización web**:
   - Generación de visualizaciones como archivos HTML
   - Uso del navegador web para mostrar representaciones interactivas

## Architecture patterns

1. **Patrón de arquitectura modular**:
   - Componentes independientes con responsabilidades bien definidas
   - Facilita el mantenimiento y la extensión del sistema

2. **Patrón de fachada**:
   - La función `calcular_carta_natal()` actúa como una fachada que simplifica la interacción con la compleja biblioteca de cálculo astrológico

3. **Patrón de estrategia**:
   - Diferentes estrategias de visualización (kerykeion, astrochart) que pueden ser seleccionadas según las necesidades

4. **Patrón de adaptador**:
   - Adaptación de los datos calculados por `immanuel` al formato requerido por los visualizadores
   - Transformación de datos completos a formato JSON optimizado para AstroChart

5. **Flujo de trabajo secuencial**:
   - Proceso claramente definido: entrada de datos → cálculo → almacenamiento (completo y reducido) → visualización
   - Cada etapa depende de la finalización exitosa de la anterior

6. **Patrón de transformación de datos**:
   - Transformación de datos completos a formato reducido para diferentes propósitos
   - Conversión de formatos de datos para compatibilidad con bibliotecas externas (AstroChart)
