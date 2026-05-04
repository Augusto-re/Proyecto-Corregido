import csv
from utils import manejo_archivos
from utils.config_archivo import get_core_info
from pathlib import Path


#inciso B
def notCordRegister(dataset: Path):

    """retorna los registro sin coordenadas

    Args:
        dataset (Path): Ruta al dataset

    Returns:
        list: Lista de registros sin coordenadas
    """

    def cord_check(dato):
        
        latitud = dato.get('decimalLatitude|latitudeDecimal')
        longitud = dato.get('decimalLongitude|longitudeDecimal')
        try:
            latitud = float(latitud)
            longitud = float(longitud)
        except :
            return True  # inválido
        return False
    




    notCordRegister = []
    config,core = get_core_info(dataset)
    path = dataset / core
    archivo = manejo_archivos.get_archive(path,**config)
    for row in archivo:
        if cord_check(row):
            notCordRegister.append(row)
    return notCordRegister




  #inciso F  
def notNumericOrNegative(dataset: Path):
    """devuelve los registros con valores no numericos o negativos

    Args:
        dataset (Path): ruta al dataset

    Returns:
        _type_: lista con los registros con valores no numericos o negativos
    """

    config, core = get_core_info(dataset)
    archivo_path = dataset / core
    archivo = manejo_archivos.get_archive(archivo_path, **config)
    
    def notNumeric(value):
        try:
            float(value)
            return False
        except (ValueError, TypeError):
            return True
    notValidsReg = []
    for row in archivo:
        dato = row.get('coordinateUncertaintyInMeters')
        if notNumeric(dato):
            notValidsReg.append(row)
    return notValidsReg



    