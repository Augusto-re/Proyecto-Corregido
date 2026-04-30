
from utils import manejo_archivos
from utils.config_archivo import get_core_info
from pathlib import Path

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
        total_nulos ={}
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