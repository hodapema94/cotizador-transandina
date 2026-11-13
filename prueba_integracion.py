
from modules.integracion import simpson_tercio, regla_trapecio

# Datos de la ruta Medellín - Bogotá

distancias = [
    0,
    103.75,
    207.5,
    311.25,
    415
]

costos = [
    4800,
    6100,
    4500,
    6400,
    5000
]

# Calcular el costo mediante ambos métodos

resultado_simpson = simpson_tercio(distancias, costos)

resultado_trapecio = regla_trapecio(distancias, costos)

# Mostrar resultados

print("COTIZADOR TRANSANDINA")
print("-------------------------------")

print(f"Simpson 1/3: ${resultado_simpson:,.2f}")
print(f"Trapecio: ${resultado_trapecio:,.2f}")

diferencia = resultado_simpson - resultado_trapecio

print(f"Diferencia: ${diferencia:,.2f}")
