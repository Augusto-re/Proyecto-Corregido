from utils import manejo_archivos
from utils.config_archivo import get_core_info
from pathlib import Path
from ejercicios.ejercicio3 import (
    coordenadas_invalidas,
    fechas_invalidas,
    registros_duplicados,
)

# ---------------------Inciso H----------------------
# Cotas aproximadas de Sudamérica
LAT_MIN_SUDAMERICA = -56.0
LAT_MAX_SUDAMERICA = 13.0
LON_MIN_SUDAMERICA = -82.0
LON_MAX_SUDAMERICA = -34.0


# ---------------------Inciso G----------------------
def resumen_calidad(datasets_paths: list[Path]):
    """
    Genera un resumen de calidad del dataset en una sola pasada
    para evitar leer los archivos múltiples veces.

    Args:
        datasets_paths (list[Path]): rutas a las carpetas de cada dataset.

    Returns:
        tuple: (dict con el resumen, str con el reporte en texto)
    """
    from datetime import datetime
    from utils.constantes import CAMPOS_FECHA_DWC
    from ejercicios.ejercicio3 import validar_fecha_dwc

    CAMPOS_TAXONOMICOS = ["scientificName", "kingdom"]

    total = 0
    coord_invalidas = 0
    fechas_inv = 0
    duplicados = 0
    taxonomia_incompleta = 0
    ids_vistos = set()
    ids_duplicados = set()

    for path in datasets_paths:
        config, core = get_core_info(path)
        archivo = manejo_archivos.get_archive(path / core, **config)

        for fila in archivo:
            total += 1

            # Coordenadas
            lat = fila.get("decimalLatitude") or fila.get("latitudeDecimal")
            lon = fila.get("decimalLongitude") or fila.get("longitudeDecimal")
            try:
                latitud = float(lat)
                longitud = float(lon)
                if not (-90 <= latitud <= 90 and -180 <= longitud <= 180):
                    coord_invalidas += 1
            except (ValueError, TypeError):
                coord_invalidas += 1

            # Fechas
            for campo in CAMPOS_FECHA_DWC:
                valor = fila.get(campo)
                if valor is not None and not validar_fecha_dwc(valor):
                    fechas_inv += 1
                    break

            # Duplicados
            id_dato = fila.get("id") or fila.get("gbifID") or fila.get("ID")
            if id_dato in ids_vistos:
                ids_duplicados.add(id_dato)
            else:
                ids_vistos.add(id_dato)

            # Taxonomía
            if any(not fila.get(campo, "").strip() for campo in CAMPOS_TAXONOMICOS):
                taxonomia_incompleta += 1

    duplicados = len(ids_duplicados)

    resumen = {
        "total_registros": total,
        "coordenadas_invalidas": coord_invalidas,
        "fechas_invalidas": fechas_inv,
        "duplicados": duplicados,
        "taxonomia_incompleta": taxonomia_incompleta,
    }

    reporte = (
        f"=== Resumen de calidad ===\n"
        f"Total de registros:              {resumen['total_registros']}\n"
        f"Coordenadas inválidas:           {resumen['coordenadas_invalidas']}\n"
        f"Fechas inválidas:                {resumen['fechas_invalidas']}\n"
        f"Registros duplicados:            {resumen['duplicados']}\n"
        f"Taxonomía incompleta:            {resumen['taxonomia_incompleta']}\n"
    )

    return resumen, reporte


# ---------------------Inciso H----------------------
def coordenada_en_sudamerica(latitud: float, longitud: float):
    """
    Valida si una coordenada se encuentra dentro de los límites
    aproximados de Sudamérica.

    Args:
        latitud (float): valor de latitud a validar.
        longitud (float): valor de longitud a validar.

    Returns:
        bool: True si está dentro de Sudamérica, False si no.
    """
    return (
        LAT_MIN_SUDAMERICA <= latitud <= LAT_MAX_SUDAMERICA
        and LON_MIN_SUDAMERICA <= longitud <= LON_MAX_SUDAMERICA
    )


def coordenadas_fuera_sudamerica(datasets_paths: list[Path]):
    """
    Detecta registros cuyas coordenadas están fuera de los límites
    aproximados de Sudamérica.

    Args:
        datasets_paths (list[Path]): rutas a las carpetas de cada dataset.

    Returns:
        tuple: cantidad de registros fuera de Sudamérica y lista de registros.
    """
    fuera = []

    for path in datasets_paths:
        config, core = get_core_info(path)
        archivo = manejo_archivos.get_archive(path / core, **config)

        for fila in archivo:
            lat = fila.get("decimalLatitude") or fila.get("latitudeDecimal") or None
            lon = fila.get("decimalLongitude") or fila.get("longitudeDecimal") or None

            if lat is None or lon is None:
                continue

            try:
                latitud = float(lat)
                longitud = float(lon)
            except (ValueError, TypeError):
                continue  # si no se puede convertir, lo maneja coordenadas_invalidas

            if not coordenada_en_sudamerica(latitud, longitud):
                fuera.append(fila)

    return len(fuera), fuera
