
def validar_datos(x, y):
    """
    Valida los puntos de distancia y sus respectivos costos.
    """

    if len(x) != len(y):
        raise ValueError("La cantidad de distancias y costos debe coincidir.")

    if len(x) < 3:
        raise ValueError("Se necesitan mínimo 3 puntos.")

    if any(valor < 0 for valor in y):
        raise ValueError("Los costos no pueden ser negativos.")

    if any(x[i] <= x[i - 1] for i in range(1, len(x))):
        raise ValueError("Las distancias deben ser crecientes.")

    # Calcular la separación entre los puntos
    h = x[1] - x[0]

    # Comprobar que todos los puntos estén igualmente espaciados
    for i in range(1, len(x) - 1):
        diferencia = x[i + 1] - x[i]

        if abs(diferencia - h) > 1e-8:
            raise ValueError(
                "Los puntos deben estar igualmente espaciados."
            )

    return h


def simpson_tercio(x, y):
    """
    Calcula la integral aproximada utilizando
    la regla compuesta de Simpson 1/3.
    """

    h = validar_datos(x, y)
    n = len(x) - 1

    if n % 2 != 0:
        raise ValueError(
            "Simpson 1/3 necesita un número par de subintervalos."
        )

    suma = y[0] + y[-1]

    for i in range(1, n):

        if i % 2 == 0:
            suma += 2 * y[i]
        else:
            suma += 4 * y[i]

    resultado = (h / 3) * suma

    return resultado


def regla_trapecio(x, y):
    """
    Calcula la integral aproximada utilizando
    la regla compuesta del trapecio.
    """

    h = validar_datos(x, y)

    suma = y[0] + y[-1]

    for i in range(1, len(y) - 1):
        suma += 2 * y[i]

    resultado = (h / 2) * suma

    return resultado
