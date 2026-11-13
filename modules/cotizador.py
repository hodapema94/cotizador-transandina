
from modules.rutas import calcular_costo_ruta


def calcular_cotizacion(id_ruta, margen_porcentaje):
    """
    Genera una cotización a partir del costo integrado de una ruta.

    El margen se aplica sobre el costo operativo estimado.
    """

    # Validar el margen
    if not isinstance(margen_porcentaje, (int, float)):
        raise TypeError("El margen debe ser un valor numérico.")

    if margen_porcentaje < 0:
        raise ValueError("El margen no puede ser negativo.")

    # Obtener los costos de la ruta
    datos_ruta = calcular_costo_ruta(id_ruta)

    costo_operativo = datos_ruta["costo_simpson"]

    # Calcular el valor adicional correspondiente al margen
    valor_margen = costo_operativo * (margen_porcentaje / 100)

    # Calcular la tarifa comercial
    tarifa_sugerida = costo_operativo + valor_margen

    # Calcular la utilidad estimada del viaje
    utilidad = tarifa_sugerida - costo_operativo

    return {
        "id_ruta": id_ruta,
        "origen": datos_ruta["origen"],
        "destino": datos_ruta["destino"],
        "distancia_km": datos_ruta["distancia_km"],
        "costo_operativo": costo_operativo,
        "metodo_referencia": datos_ruta["costo_trapecio"],
        "margen_porcentaje": margen_porcentaje,
        "valor_margen": valor_margen,
        "tarifa_sugerida": tarifa_sugerida,
        "utilidad": utilidad
    }
