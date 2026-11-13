
from modules.funciones_matematicas import (
    costo_total,
    ingreso_total,
    utilidad_total,
    costo_marginal,
    ingreso_marginal,
    utilidad_marginal,
    puntos_equilibrio,
    maximizar_utilidad
)


print("COTIZADOR TRANSANDINA")
print("=" * 45)

# Evaluar diferentes cantidades de viajes

for q in [50, 65, 100]:

    print(f"\nANÁLISIS PARA {q} VIAJES")

    print(f"Costo total: ${costo_total(q):,.4f} millones")

    print(f"Ingreso total: ${ingreso_total(q):,.4f} millones")

    print(f"Utilidad: ${utilidad_total(q):,.4f} millones")


# Analizar las derivadas para 65 viajes

print("\nANÁLISIS MARGINAL PARA 65 VIAJES")
print("-" * 45)

print(f"Costo marginal: ${costo_marginal(65):,.4f} millones")

print(f"Ingreso marginal: ${ingreso_marginal(65):,.4f} millones")

print(f"Utilidad marginal: ${utilidad_marginal(65):,.4f} millones")


# Encontrar puntos de equilibrio

print("\nPUNTOS DE EQUILIBRIO")
print("-" * 45)

for punto in puntos_equilibrio():

    print(f"{punto:.4f} viajes")


# Encontrar la máxima utilidad

print("\nOPTIMIZACIÓN DE UTILIDAD")
print("-" * 45)

resultado = maximizar_utilidad()

print(f"Viajes óptimos: {resultado['viajes_optimos']:.4f}")

print(
    f"Utilidad máxima: "
    f"${resultado['utilidad_maxima']:,.4f} millones"
)

print(
    f"Segunda derivada: "
    f"{resultado['segunda_derivada']:.4f}"
)

print(f"¿Es un máximo?: {resultado['es_maximo']}")

print(f"Viajes enteros recomendados: {resultado['viajes_enteros']}")

print(
    f"Utilidad con viajes enteros: "
    f"${resultado['utilidad_viajes_enteros']:,.4f} millones"
)
