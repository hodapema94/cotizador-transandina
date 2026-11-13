
from modules.rutas import (
    listar_rutas,
    obtener_ruta,
    calcular_costo_ruta
)


print("COTIZADOR TRANSANDINA")
print("=" * 45)

# 1. Consultar rutas disponibles

print("\nRUTAS DISPONIBLES")
print("-" * 45)

rutas = listar_rutas()

print(rutas.to_string(index=False))


# 2. Consultar los puntos de la ruta

print("\nPUNTOS DE LA RUTA")
print("-" * 45)

detalle = obtener_ruta(1)

print(detalle.to_string(index=False))


# 3. Calcular el costo de la ruta

print("\nCOTIZACIÓN DE LA RUTA")
print("-" * 45)

resultado = calcular_costo_ruta(1)

print(
    f"Origen: {resultado['origen']}"
)

print(
    f"Destino: {resultado['destino']}"
)

print(
    f"Distancia: {resultado['distancia_km']:.2f} km"
)

print(
    f"Costo Simpson: ${resultado['costo_simpson']:,.2f}"
)

print(
    f"Costo Trapecio: ${resultado['costo_trapecio']:,.2f}"
)

print(
    f"Diferencia: ${resultado['diferencia']:,.2f}"
)
