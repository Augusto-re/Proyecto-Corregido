from utils import manejo_archivos
from utils.config_archivo import get_core_info
from utils.constantes import DATASETS_PATH_PROCESSED
from ejercicios.ejercicio4 import validar_registro
from pathlib import Path


def _guardar_dataset(archivo: list, path_raw: Path, **config):
    """
    Guarda el dataset modificado en processed_datasets manteniendo
    la misma estructura que el original.

    Args:
        archivo (list): Lista de registros a guardar.
        path_raw (Path): Ruta original del dataset en raw_datasets.
        **config: Configuración del archivo (encoding, separador, etc.)
    """
    core = config.get("core")
    dir_path = DATASETS_PATH_PROCESSED / path_raw.name
    dir_path.mkdir(parents=True, exist_ok=True)
    ruta_csv = dir_path / core
    manejo_archivos.write_archive(archivo, ruta_csv, **config)


# ---------------------Inciso A----------------------
def buscar_registros(datasets_paths: list[Path], filtros: dict):
    """
    Busca registros que coincidan con todos los filtros indicados.

    Args:
        datasets_paths (list[Path]): Rutas a las carpetas de cada dataset.
        filtros (dict): Columnas y valores a filtrar.
                        Ejemplo: {"scientificName": "Elaenia chilensis", "country": "Argentina"}

    Returns:
        list: Registros que cumplen todas las condiciones.
    """
    resultados = []

    for path in datasets_paths:
        config, core = get_core_info(path)
        archivo = manejo_archivos.get_archive(path / core, **config)

        for fila in archivo:
            if all(fila.get(col) == val for col, val in filtros.items()):
                resultados.append(fila)

    return resultados


# ---------------------Inciso B----------------------
def actualizar_campo(path_raw: Path, id_registro: str, columna: str, nuevo_valor: str):
    """
    Actualiza un campo de un registro identificado por su ID.

    Args:
        path_raw (Path): Ruta a la carpeta del dataset.
        id_registro (str): ID del registro a modificar.
        columna (str): Nombre de la columna a actualizar.
        nuevo_valor (str): Nuevo valor para la columna.

    Returns:
        bool: True si se encontró y modificó el registro, False si no se encontró.
    """
    config, core = get_core_info(path_raw)
    # archivo = manejo_archivos.get_archive(path_raw / core, **config) ---> aca antes recibia la lista, ahora recibo un generador
    archivo = list(
        manejo_archivos.get_archive(path_raw / core, **config)
    )  # aca me trae el generador completo antesw de empezar

    encontrado = False
    for fila in archivo:
        id_fila = fila.get("id") or fila.get("gbifID") or fila.get("ID")
        if id_fila == id_registro:
            fila[columna] = nuevo_valor
            encontrado = True
            break

    if not encontrado:
        print(f"ERROR: No se encontró el registro con ID '{id_registro}'.")
        return False

    config["core"] = core
    _guardar_dataset(archivo, path_raw, **config)
    return True


# ---------------------Inciso C----------------------
def actualizar_campos(path_raw: Path, id_registro: str, nuevos_valores: dict):
    """
    Actualiza múltiples campos de un registro en una sola operación.

    Args:
        path_raw (Path): Ruta a la carpeta del dataset.
        id_registro (str): ID del registro a modificar.
        nuevos_valores (dict): Columnas y nuevos valores.
                               Ejemplo: {"country": "Argentina", "stateProvince": "Buenos Aires"}

    Returns:
        bool: True si se encontró y modificó el registro, False si no se encontró.
    """
    config, core = get_core_info(path_raw)
    archivo = list(
        manejo_archivos.get_archive(path_raw / core, **config)
    )  # me traigo el generador completo

    encontrado = False
    for fila in archivo:
        id_fila = fila.get("id") or fila.get("gbifID") or fila.get("ID")
        if id_fila == id_registro:
            for columna, valor in nuevos_valores.items():
                fila[columna] = valor
            encontrado = True
            break

    if not encontrado:
        print(f"ERROR: No se encontró el registro con ID '{id_registro}'.")
        return False

    config["core"] = core
    _guardar_dataset(archivo, path_raw, **config)
    return True


# ---------------------Inciso D----------------------
def actualizar_campos_validado(path_raw: Path, id_registro: str, nuevos_valores: dict):
    """
    Actualiza múltiples campos de un registro validando los nuevos valores
    antes de aplicar los cambios.

    Args:
        path_raw (Path): Ruta a la carpeta del dataset.
        id_registro (str): ID del registro a modificar.
        nuevos_valores (dict): Columnas y nuevos valores a aplicar.

    Returns:
        bool: True si la validación pasó y se guardaron los cambios, False si falló.
    """
    config, core = get_core_info(path_raw)
    archivo = list(
        manejo_archivos.get_archive(path_raw / core, **config)
    )  # me traigo el generador completo

    encontrado = False
    for fila in archivo:
        id_fila = fila.get("id") or fila.get("gbifID") or fila.get("ID")
        if id_fila == id_registro:
            copia = dict(fila)
            for columna, valor in nuevos_valores.items():
                copia[columna] = valor

            # Validación propia para no depender de tipos en validar_registro
            errores = []
            for campo in ("decimalLatitude", "latitudeDecimal"):
                val = copia.get(campo)
                if val not in (None, "", " "):
                    try:
                        if not (-90 <= float(val) <= 90):
                            errores.append(f"{campo} fuera de rango: {val}")
                    except (ValueError, TypeError):
                        errores.append(f"{campo} no es numérico: {val}")

            for campo in ("decimalLongitude", "longitudeDecimal"):
                val = copia.get(campo)
                if val not in (None, "", " "):
                    try:
                        if not (-180 <= float(val) <= 180):
                            errores.append(f"{campo} fuera de rango: {val}")
                    except (ValueError, TypeError):
                        errores.append(f"{campo} no es numérico: {val}")

            if errores:
                print(
                    f"ERROR: Los nuevos valores no pasaron la validación. Registro no modificado."
                )
                for e in errores:
                    print(f"  - {e}")
                return False

            for columna, valor in nuevos_valores.items():
                fila[columna] = valor

            encontrado = True
            break

    if not encontrado:
        print(f"ERROR: No se encontró el registro con ID '{id_registro}'.")
        return False

    config["core"] = core
    _guardar_dataset(archivo, path_raw, **config)
    print(f"Registro '{id_registro}' actualizado correctamente.")
    return True
