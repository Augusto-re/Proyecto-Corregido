from utils import manejo_archivos
from utils.config_archivo import get_core_info
from pathlib import Path



#ejercicio 2G
def valuesInColumn(dataset:Path, columns_name: str):
    """retorna la cantidad de valores en la columna dada

    Args:
        dataset (Path): ruta al dataset
        columns_name (str): nombre de la columna

    Returns:
        int: cantidad de valores únicos en la columna
    """    
    config, core = get_core_info(dataset)
    archivo_path = dataset / core
    values = set()
    archivo = manejo_archivos.get_archive(archivo_path, **config)

    if columns_name not in archivo[0].keys():
        return 0

    for row in archivo:
        values.update([row[columns_name]])


    return len(values)





#ejercicio 2H
def valueFrecuenseInColumn(dataset: Path, columns_name: str):
    """retorna la frecuencia de cada valor en la columna dada

    Args:
        dataset (Path): ruta al dataset
        columns_name (str): nombre de la columna

    Returns:
        dict: diccionario con la frecuencia de cada valor en la columna
    """    
    config, core = get_core_info(dataset)
    archivo_path = dataset / core
    values = set()
    archivo = manejo_archivos.get_archive(archivo_path, **config)
    values_in_column = {}

    for row in archivo:
        value = row.get(columns_name)
        values_in_column[value] = values_in_column.get(value, 0) + 1


    return values_in_column
