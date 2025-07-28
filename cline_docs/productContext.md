# Product Context: Carta Natal App

## Why this project exists
La aplicación "Carta Natal App" existe para proporcionar a los usuarios una herramienta completa para calcular, visualizar y analizar cartas natales astrológicas. La astrología es un sistema de creencias que sugiere que las posiciones de los cuerpos celestes en el momento del nacimiento de una persona pueden influir en su personalidad, relaciones y eventos de vida. Esta aplicación permite a los usuarios generar estas cartas natales con precisión y visualizarlas de manera intuitiva.

## What problems it solves
1. **Accesibilidad a la astrología**: Hace que los cálculos astrológicos complejos sean accesibles para usuarios sin conocimientos técnicos profundos.
2. **Precisión en cálculos**: Elimina errores humanos en los cálculos astrológicos que requieren datos astronómicos precisos.
3. **Visualización clara**: Proporciona representaciones visuales claras de información astrológica compleja.
4. **Versatilidad**: Ofrece tanto cartas natales tropicales (estándar) como dracónicas (alternativas).
5. **Personalización**: Permite diferentes opciones de visualización y temas.
6. **Almacenamiento de datos**: Guarda los resultados en formato JSON para referencia futura o análisis adicional.

## How it should work
1. **Entrada de datos**:
   - El usuario proporciona su nombre completo, fecha de nacimiento, hora de nacimiento, y lugar de nacimiento (ciudad y país).
   - La aplicación valida estos datos para asegurar que sean correctos y utilizables.

2. **Procesamiento de datos**:
   - La aplicación convierte la ubicación en coordenadas geográficas (latitud/longitud).
   - Determina la zona horaria correspondiente a esas coordenadas.
   - Calcula las posiciones planetarias, ángulos, casas y aspectos astrológicos para el momento y lugar especificados.
   - Genera dos tipos de cartas: tropical (estándar) y dracónica (alternativa).

3. **Presentación de resultados**:
   - Muestra un resumen textual de la carta natal en la consola.
   - Guarda los resultados completos en archivos JSON.
   - Genera archivos JSON optimizados para AstroChart con formato específico.
   - Ofrece visualizaciones gráficas interactivas con diferentes opciones:
     - Visualización individual o combinada de cartas
     - Diferentes temas visuales (claro, oscuro, monocromático)
     - Opción para mostrar u ocultar líneas de aspectos

4. **Interacción del usuario**:
   - Interfaz de línea de comandos intuitiva con validación de entrada.
   - Opciones claras para personalizar la experiencia.
   - Apertura automática de visualizaciones en el navegador web.
