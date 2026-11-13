
from modules.cotizador import calcular_cotizacion


print("COTIZADOR TRANSANDINA")
print("=" * 45)

# Seleccionar la ruta Medellín - Bogotá
id_ruta = 1

# Definir el margen comercial
margen = 20

# Generar la cotización
resultado = calcular_cotizacion(id_ruta, margen)


print("\nDETALLE DEL RECORRIDO")
print("-" * 45)

print(f"Origen: {resultado['origen']}")
print(f"Destino: {resultado['destino']}")
print(f"Distancia: {resultado['distancia_km']:.2f} km")


print("\nDETALLE ECONÓMICO")
print("-" * 45)

print(
    f"Costo operativo: "
    f"${resultado['costo_operativo']:,.2f}"
)

print(
    f"Costo por trapecio: "
    f"${resultado['metodo_referencia']:,.2f}"
)

print(
    f"Margen aplicado: "
    f"{resultado['margen_porcentaje']}%"
)

print(
    f"Valor del margen: "
    f"${resultado['valor_margen']:,.2f}"
)


print("\nRESULTADO DE LA COTIZACIÓN")
print("-" * 45)

print(
    f"Tarifa sugerida: "
    f"${resultado['tarifa_sugerida']:,.2f}"
)

print(
    f"Utilidad estimada: "
    f"${resultado['utilidad']:,.2f}"
)
