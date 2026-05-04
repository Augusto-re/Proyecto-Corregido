from utils import manejo_archivos
from utils.config_archivo import get_core_info
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
def validar_columna_tipo(columna, tipo ):
    iterable = columna.values() if isinstance(columna, dict) else columna
    valores = [v for v in iterable if v is not None and v != ""]
    
    if not valores :
        return None
    
    if tipo == "numeric":
        numeros = [float(v) for v in valores]
        minimo = min(numeros)
        maximo = max(numeros)
        promedio = sum(numeros) / len(numeros)
        return{
            "min":minimo,
            "max": maximo,
            "promedio": promedio
        }
    elif tipo == "coordinate":
        coords = [float(v) for v in valores]
        minimo2 = min(coords)
        maximo2 = max(coords)
        return {
            "min":minimo2,
            "max": maximo2
        }
        
    elif tipo == "text" :
        longitudes = [len(v) for v in valores]
        minimo3 =min(longitudes)
        maximo3 = max(longitudes)
        return {
            "min":minimo3,
            "max": maximo3
        }
    else :
        print('no se paso un tipo de dato valido ')
#ejercicio 2J
def columnas_nulas(datasets_paths : list[Path]):
    """"
        esta funcion retorna las keys de las columnas cuyo contenido
        es completamente nulo
    
    Args:
        datasets_paths (list[Path]): Rutas a las carpetas de cada dataset.

    Returns:
        dict: {nombre_dataset: list[str]} columnas con contenido nulo.
    
    """
    resultado = {}

    for path in datasets_paths:
        config, core = get_core_info(path)
        archivo_path = path / core
        archivo = manejo_archivos.get_archive(archivo_path, **config)
        total = {}
        total[col]=0
        total_nulos ={}
        total_nulos[col] =0
        columnas_nulas = []

        for fila in archivo:
            for col, val in fila.items():   
                total[col] +=1
                if val is None or val.strip() == "":
                    total_nulos[col] +=1
                    

        for col in total:
            if total[col] > 0 and total_nulos[col] == total[col]:
                columnas_nulas.append(col)

    resultado[path.name] = columnas_nulas

    return resultado