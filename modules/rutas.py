
from pathlib import Path
import pandas as pd

from modules.integracion import (
    simpson_tercio,
    regla_trapecio
)


# Ubicación del archivo CSV
RUTA_ARCHIVO = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "costos_rutas.csv"
)


def cargar_rutas():
    """
    Carga las rutas registradas en el archivo CSV.
    """

    if not RUTA_ARCHIVO.exists():
        raise FileNotFoundError(
            "No se encontró el archivo costos_rutas.csv."
        )

    datos = pd.read_csv(RUTA_ARCHIVO)

    columnas = [
        "id_ruta",
        "origen",
        "destino",
        "distancia_km",
        "costo_km"
    ]

    if not all(columna in datos.columns for columna in columnas):
        raise ValueError(
            "El archivo CSV no contiene todas las columnas necesarias."
        )

    if datos.empty:
        raise ValueError("El archivo de rutas está vacío.")

    if datos[columnas].isnull().any().any():
        raise ValueError("Existen datos vacíos en el archivo de rutas.")

    return datos


def listar_rutas():
    """
    Devuelve el listado de rutas disponibles.
    """

    datos = cargar_rutas()

    rutas = datos[
        ["id_ruta", "origen", "destino"]
    ].drop_duplicates()

    return rutas.reset_index(drop=True)


def obtener_ruta(id_ruta):
    """
    Consulta los puntos de una ruta específica.
    """

    datos = cargar_rutas()

    ruta = datos[
        datos["id_ruta"] == id_ruta
    ].copy()

    if ruta.empty:
        raise ValueError(
            f"No existe una ruta con el identificador {id_ruta}."
        )

    ruta = ruta.sort_values("distancia_km")

    return ruta


def calcular_costo_ruta(id_ruta):
    """
    Calcula el costo de una ruta mediante Simpson
    y lo compara con la regla del trapecio.
    """

    ruta = obtener_ruta(id_ruta)

    distancias = ruta["distancia_km"].tolist()
    costos = ruta["costo_km"].tolist()

    costo_simpson = simpson_tercio(distancias, costos)

    costo_trapecio = regla_trapecio(distancias, costos)

    primera_fila = ruta.iloc[0]

    return {
        "id_ruta": id_ruta,
        "origen": primera_fila["origen"],
        "destino": primera_fila["destino"],
        "distancia_km": float(ruta["distancia_km"].max()),
        "costo_simpson": costo_simpson,
        "costo_trapecio": costo_trapecio,
        "diferencia": costo_simpson - costo_trapecio
    }
