#!/usr/bin/env python3
"""
Script para debuggear los datos reales que usa la API
"""
import requests
import json

# Hacer request a la API para obtener datos reales
print("=== DEBUGGING API DATA ===")

# 1. Obtener carta tropical
print("1. Obteniendo carta tropical...")
tropical_response = requests.post("http://localhost:8001/carta-natal/tropical", json={
    "nombre": "Luis Minvielle",
    "fecha_nacimiento": "1970-10-03",
    "hora_nacimiento": "14:30",
    "lugar_nacimiento": "Buenos Aires, Argentina",
    "latitud": -34.6118,
    "longitud": -58.3960,
    "genero": "masculino"
})

if tropical_response.status_code == 200:
    tropical_data = tropical_response.json()
    print("✅ Carta tropical obtenida")
    
    # Mostrar cúspides tropicales
    print("\nCúspides Tropicales (API):")
    for casa in range(1, 13):
        if str(casa) in tropical_data['houses']:
            house_data = tropical_data['houses'][str(casa)]
            print(f"Casa {casa:2d}: {house_data['longitude']:7.2f}° ({house_data['sign']} {house_data['degrees']:.2f}°)")
else:
    print(f"❌ Error obteniendo carta tropical: {tropical_response.status_code}")
    exit(1)

# 2. Obtener carta dracónica
print("\n2. Obteniendo carta dracónica...")
draconic_response = requests.post("http://localhost:8001/carta-natal/draconica", json={
    "nombre": "Luis Minvielle",
    "fecha_nacimiento": "1970-10-03",
    "hora_nacimiento": "14:30",
    "lugar_nacimiento": "Buenos Aires, Argentina",
    "latitud": -34.6118,
    "longitud": -58.3960,
    "genero": "masculino"
})

if draconic_response.status_code == 200:
    draconic_data = draconic_response.json()
    print("✅ Carta dracónica obtenida")
    
    # Mostrar cúspides dracónicas
    print("\nCúspides Dracónicas (API):")
    for casa in range(1, 13):
        if str(casa) in draconic_data['houses']:
            house_data = draconic_data['houses'][str(casa)]
            print(f"Casa {casa:2d}: {house_data['longitude']:7.2f}° ({house_data['sign']} {house_data['degrees']:.2f}°)")
else:
    print(f"❌ Error obteniendo carta dracónica: {draconic_response.status_code}")
    exit(1)

# 3. Obtener carta cruzada
print("\n3. Obteniendo carta cruzada...")
cruzada_response = requests.post("http://localhost:8001/carta-natal/cruzada", json={
    "nombre": "Luis Minvielle",
    "fecha_nacimiento": "1970-10-03",
    "hora_nacimiento": "14:30",
    "lugar_nacimiento": "Buenos Aires, Argentina",
    "latitud": -34.6118,
    "longitud": -58.3960,
    "genero": "masculino"
})

if cruzada_response.status_code == 200:
    cruzada_data = cruzada_response.json()
    print("✅ Carta cruzada obtenida")
    
    # Mostrar cúspides cruzadas
    print("\nCúspides Cruzadas (API):")
    for cuspide in cruzada_data['cuspides_cruzadas']:
        print(f"Casa {cuspide['casa_draconica']} Dracónica → Casa {cuspide['casa_tropical_ubicacion']} Tropical")
        print(f"  {cuspide['descripcion']}")
else:
    print(f"❌ Error obteniendo carta cruzada: {cruzada_response.status_code}")
    exit(1)

# 4. Comparar con mi test
print("\n=== COMPARACIÓN CON TEST ===")
print("Casa 1 Dracónica según API:", cruzada_data['cuspides_cruzadas'][0]['casa_tropical_ubicacion'])
print("Casa 1 Dracónica según mi test: 12")
print("¡DISCREPANCIA ENCONTRADA!")

# 5. Analizar datos de entrada
print("\n=== ANÁLISIS DE DATOS DE ENTRADA ===")
print("Datos tropicales que usa la API:")
cuspides_api = []
for casa in range(1, 13):
    if str(casa) in tropical_data['houses']:
        lon = tropical_data['houses'][str(casa)]['longitude']
        cuspides_api.append((casa, lon))
        
print("Cúspides API vs Test:")
cuspides_test = [
    (1, 336.87), (2, 6.52), (3, 36.87), (4, 66.87), (5, 96.87), (6, 126.87),
    (7, 156.87), (8, 186.52), (9, 216.87), (10, 246.87), (11, 276.87), (12, 306.87)
]

for i, ((casa_api, lon_api), (casa_test, lon_test)) in enumerate(zip(cuspides_api, cuspides_test)):
    diff = abs(lon_api - lon_test)
    status = "✅" if diff < 1.0 else "❌"
    print(f"{status} Casa {casa_api}: API={lon_api:7.2f}° vs Test={lon_test:7.2f}° (diff={diff:.2f}°)")
