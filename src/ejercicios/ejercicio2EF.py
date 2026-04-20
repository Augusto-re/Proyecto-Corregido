from utils import manejo_archivos
from utils.config_archivo import get_core_info
from pathlib import Path


def columnas_con_nulos(datasets_paths: list[Path]):
    """
    Retorna las columnas que poseen al menos un valor nulo o vacío
    en cada dataset.

    Args:
        datasets_paths (list[Path]): Rutas a las carpetas de cada dataset.

    Returns:
        dict: {nombre_dataset: list[str]} columnas con al menos un nulo.
    """
    resultado = {}

    for path in datasets_paths:
        config, core = get_core_info(path)
        archivo_path = path / core
        archivo = manejo_archivos.get_archive(archivo_path, **config)

        columnas_nulas = set()
        for fila in archivo:
            for col, val in fila.items():
                if val is None or val.strip() == "":
                    columnas_nulas.add(col)

        resultado[path.name] = sorted(columnas_nulas)

    return resultado


def porcentaje_nulos_por_columna(datasets_paths: list[Path]):
    """
    Retorna el porcentaje de valores nulos por columna para cada dataset.

    Args:
        datasets_paths (list[Path]): Rutas a las carpetas de cada dataset.

    Returns:
        dict: {nombre_dataset: {columna: porcentaje}} con 2 decimales.
              Ejemplo: {"iadiza": {"country": 0.0, "stateProvince": 34.57}}
    """
    resultado = {}

    for path in datasets_paths:
        config, core = get_core_info(path)
        archivo_path = path / core
        archivo = manejo_archivos.get_archive(archivo_path, **config)

        conteo_nulos = {}
        total = 0

        for fila in archivo:
            total += 1
            for col, val in fila.items():
                if col not in conteo_nulos:
                    conteo_nulos[col] = 0
                if val is None or val.strip() == "":
                    conteo_nulos[col] += 1

        if total == 0:
            resultado[path.name] = {}
            continue

        resultado[path.name] = {
            col: round((nulos / total) * 100, 2) for col, nulos in conteo_nulos.items()
        }

    return resultado
