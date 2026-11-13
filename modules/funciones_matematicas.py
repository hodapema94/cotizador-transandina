#Calcular el costo total de los viajes.
#Calcular los ingresos.
#Calcular la utilidad.
#Obtener los costos e ingresos marginales mediante derivadas.
#Encontrar los puntos de equilibrio.
#Determinar cuántos viajes permiten alcanzar la máxima utilidad.


import numpy as np


def validar_viajes(q):
    """
    Comprueba que la cantidad de viajes sea válida.
    """

    if not isinstance(q, (int, float)):
        raise TypeError("La cantidad de viajes debe ser numérica.")

    if q < 0:
        raise ValueError("La cantidad de viajes no puede ser negativa.")


def costo_total(q):
    """
    Calcula el costo total mensual.
    Resultado expresado en millones de pesos.
    """

    validar_viajes(q)

    return (
        0.00005 * q**3
        - 0.006 * q**2
        + 2.4 * q
        + 45
    )


def ingreso_total(q):
    """
    Calcula los ingresos totales mensuales.
    Resultado expresado en millones de pesos.
    """

    validar_viajes(q)

    return 4.2 * q - 0.015 * q**2


def utilidad_total(q):
    """
    Calcula la utilidad mensual.
    Utilidad = Ingresos - Costos.
    Resultado expresado en millones de pesos.
    """

    validar_viajes(q)

    return ingreso_total(q) - costo_total(q)


def costo_marginal(q):
    """
    Primera derivada del costo total.
    """

    validar_viajes(q)

    return 0.00015 * q**2 - 0.012 * q + 2.4


def ingreso_marginal(q):
    """
    Primera derivada del ingreso total.
    """

    validar_viajes(q)

    return 4.2 - 0.03 * q


def utilidad_marginal(q):
    """
    Primera derivada de la utilidad.
    """

    validar_viajes(q)

    return -0.00015 * q**2 - 0.018 * q + 1.8


def segunda_derivada_utilidad(q):
    """
    Segunda derivada de la utilidad.
    Permite analizar si un punto crítico es máximo o mínimo.
    """

    validar_viajes(q)

    return -0.0003 * q - 0.018


def puntos_equilibrio():
    """
    Encuentra las cantidades de viajes donde
    los ingresos son iguales a los costos.
    """

    # Coeficientes de la función de utilidad:
    # -0.00005q³ - 0.009q² + 1.8q - 45

    coeficientes = [
        -0.00005,
        -0.009,
        1.8,
        -45
    ]

    raices = np.roots(coeficientes)

    # Conservar únicamente las raíces reales y positivas
    resultados = [
        float(raiz.real)
        for raiz in raices
        if abs(raiz.imag) < 1e-8 and raiz.real > 0
    ]

    return sorted(resultados)


def maximizar_utilidad():
    """
    Encuentra el punto crítico de la utilidad
    y comprueba si corresponde a un máximo.
    """

    # Resolver U'(q) = 0
    coeficientes = [
        -0.00015,
        -0.018,
        1.8
    ]

    raices = np.roots(coeficientes)

    # Seleccionar la raíz real y positiva
    candidatos = [
        float(raiz.real)
        for raiz in raices
        if abs(raiz.imag) < 1e-8 and raiz.real >= 0
    ]

    if not candidatos:
        raise ValueError("No se encontró un punto crítico válido.")

    q_optimo = candidatos[0]

    utilidad_maxima = utilidad_total(q_optimo)

    # Comprobar la segunda derivada
    segunda_derivada = segunda_derivada_utilidad(q_optimo)

    es_maximo = segunda_derivada < 0

    # Como los viajes son unidades enteras,
    # comparar los dos enteros más cercanos.
    viajes_candidatos = [
        int(np.floor(q_optimo)),
        int(np.ceil(q_optimo))
    ]

    mejor_cantidad = max(
        viajes_candidatos,
        key=utilidad_total
    )

    return {
        "viajes_optimos": q_optimo,
        "utilidad_maxima": utilidad_maxima,
        "segunda_derivada": segunda_derivada,
        "es_maximo": es_maximo,
        "viajes_enteros": mejor_cantidad,
        "utilidad_viajes_enteros": utilidad_total(mejor_cantidad)
    }
