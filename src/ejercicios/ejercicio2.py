from utils import manejo_archivos
from pathlib import Path


def columnas_con_nulos(datasets_paths, configs):
    """
    Retorna las columnas que poseen al menos un valor nulo o vacío
    en cada dataset.

    Args:
        datasets_paths (list[Path]): Rutas a las carpetas de cada dataset.

    Returns:
        dict: {nombre_dataset: list[str]} columnas con al menos un nulo.
    """
    resultado = {}

    for path, config in zip(datasets_paths, configs):
        archivo = manejo_archivos.get_archive(path, **config)

        columnas_nulas = set()
        for fila in archivo:
            for col, val in fila.items():
                if val is None or val.strip() == "":
                    columnas_nulas.add(col)

        resultado[path.name] = sorted(columnas_nulas)

    return resultado


def porcentaje_nulos_por_columna(datasets_paths, configs):
    """
    Retorna el porcentaje de valores nulos por columna para cada dataset.

    Args:
        datasets_paths (list[Path]): Rutas a las carpetas de cada dataset.

    Returns:
        dict: {nombre_dataset: {columna: porcentaje}} con 2 decimales.
              Ejemplo: {"iadiza": {"country": 0.0, "stateProvince": 34.57}}
    """
    resultado = {}

    for path, config in zip(datasets_paths, configs):
        archivo = manejo_archivos.get_archive(path, **config)

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

#ejercicio 2G
def valuesInColumn(archivo_path:Path, config:dict, columns_name: str):
    """retorna la cantidad de valores en la columna dada

    Args:
        dataset (Path): ruta al dataset
        columns_name (str): nombre de la columna

    Returns:
        int: cantidad de valores únicos en la columna
    """    
    values = set()
    archivo = manejo_archivos.get_archive(archivo_path, **config)

    if columns_name not in archivo[0].keys():
        return 0 #si no existe el nombre de columna

    for row in archivo:
        values.update([row[columns_name]])


    return len(values)





#ejercicio 2H
def valueFrecuenseInColumn(archivo_path:Path, config:dict, columns_name: str):
    """retorna la frecuencia de cada valor en la columna dada

    Args:
        dataset (Path): ruta al dataset
        columns_name (str): nombre de la columna

    Returns:
        dict: diccionario con la frecuencia de cada valor en la columna
    """    
    archivo = manejo_archivos.get_archive(archivo_path, **config)
    values_in_column = {}

    for row in archivo:
        value = row.get(columns_name) #accedo a la columna
        values_in_column[value] = values_in_column.get(value, 0) + 1 #sumo 1 en frecuencia


    return values_in_column


#ejercicio 2I
def validar_columna_tipo(columna, tipo):
    iterable = columna.values() if isinstance(columna, dict) else columna

    valores = []
    for v in iterable:
        if v is None:
            continue
        if isinstance(v, str):
            v = v.strip()
            if v == "":
                continue
        valores.append(v)

    if not valores:
        return None

    # -------- NUMERIC --------
    if tipo == "numeric":
        numeros = []

        for v in valores:
            try:
                numeros.append(float(v))
            except (ValueError, TypeError):
                continue  # ignora valores inválidos

        if not numeros:
            return None

        return {
            "min": min(numeros),
            "max": max(numeros),
            "promedio": sum(numeros) / len(numeros)
        }

    # -------- COORDINATE --------
    elif tipo == "coordinate":
        coords = []

        for v in valores:
            try:
                coords.append(float(v))
            except (ValueError, TypeError):
                continue

        if not coords:
            return None

        return {
            "min": min(coords),
            "max": max(coords)
        }

    # -------- TEXT --------
    elif tipo == "text":
        longitudes = []

        for v in valores:
            if isinstance(v, str):
                longitudes.append(len(v))
            else:
                longitudes.append(len(str(v)))

        if not longitudes:
            return None

        return {
            "min": min(longitudes),
            "max": max(longitudes)
        }

    else:
        raise ValueError(f"Tipo inválido: {tipo}")


#ejercicio 2J
def columnas_nulas(archivo_path: Path, config: dict):
    """
    Retorna las columnas cuyo contenido es completamente nulo.

    Args:
        archivo_path (Path): Ruta del dataset.
        config (dict): Configuración para lectura.

    Returns:
        list[str]: Columnas con contenido completamente nulo.
    """

    archivo = manejo_archivos.get_archive(archivo_path, **config)

    total = {}
    total_nulos = {}

    for fila in archivo:
        for col, val in fila.items():
            # Inicializar si no existe
            if col not in total:
                total[col] = 0
                total_nulos[col] = 0

            total[col] += 1

            # Validación de nulo robusta
            if val is None or (isinstance(val, str) and val.strip() == ""):
                total_nulos[col] += 1

    columnas_nulas = [
        col for col in total
        if total[col] > 0 and total[col] == total_nulos[col]
    ]

    return columnas_nulas