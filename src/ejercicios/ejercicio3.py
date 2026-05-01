from utils import manejo_archivos
from utils.config_archivo import  get_core_info
from utils.constantes import CAMPOS_FECHA_DWC
from pathlib import Path
import string
from datetime import datetime



def coordenadas_invalidas (datasets_paths: Path):
    """
    Args:
        datasets_paths (Path): rutas de los archivos a buscar

    Returns:
        _type_: _description_
    """

    # decimalLatitude
    # decimalLongitude
    def revisar_coordenadas(dato):
        # GET porque hay datos que no tienen ese campo
        lat = dato.get('decimalLatitude')
        lon = dato.get('decimalLongitude')
        try:
            latitud = float(lat)
            longitud = float(lon)
        except (ValueError, TypeError):
            return True  # inválido

        if not (-90 <= latitud <= 90 and -180 <= longitud <= 180):
            return True  # inválido

        return False  # válido
    
    coordenadas_invalidas = []
    for path in datasets_paths:
        config, core = get_core_info(path)
        path = path / core

        archivo = manejo_archivos.get_archive(path, **config)
        
        coordenadas_invalidas.extend(list(filter(revisar_coordenadas, archivo)))

    return len(coordenadas_invalidas), coordenadas_invalidas

def coordenadas_validas_longitud (VALOR):
    """
    Args:
        valor (str): valor a verificar

    Returns:
        _type_: true si el valor es valido , false si es invalido
    """
    if not (-180 <= VALOR <= 180):
        return False  # inválido

    return True  # válido

def coordenadas_validas_latitud (VALOR):
    """
    Args:
        valor (str): valor a verificar

    Returns:
        _type_: true si el valor es valido , false si es invalido
    """

    if not (-90 <= VALOR <= 90):
        return False  # inválido

    return True  # válido



def validar_fecha_dwc(valor):
    anio_actual = datetime.now().year

    valor = str(valor).strip()
    if valor in ("", "nan", "none"):
        return False

    # Sacar solo la parte fecha (ignorar TIME si existe)
    parte = valor.split("T")[0]

    # Intentar convertir — si falla, no es fecha válida
    fecha_obj = None
    for fmt in ["%Y-%m-%d", "%Y-%m", "%Y"]:
        try:
            fecha_obj = datetime.strptime(parte, fmt)
            break
        except ValueError:
            continue

    if fecha_obj is None:
        return False

    if fecha_obj.year > anio_actual:
        return False

    return True


def fechas_invalidas(datasets_paths: Path):
    """
    Args:
        datasets_paths (Path): rutas de los archivos a buscar
    Returns:
        tuple: cantidad de errores y lista de registros con fecha inválida
    """
    def revisar_fechas(dato):
        for campo in CAMPOS_FECHA_DWC:
            valor = dato.get(campo)
            if valor is not None and not validar_fecha_dwc(valor):
                return True  # inválido
        return False  # válido

    fechas_invalidas = []
    for path in datasets_paths:
        config, core = get_core_info(path)
        path = path / core
        archivo = manejo_archivos.get_archive(path, **config)
        fechas_invalidas.extend(list(filter(revisar_fechas, archivo)))

    return len(fechas_invalidas), fechas_invalidas

# ---------------------Inciso D----------------------
def registros_duplicados(datasets_paths: Path):
    """
    Args:
        datasets_paths (Path): rutas de los archivos a buscar

    Returns:
        _type_: _description_
    """

    ids_vistos = set()
    ids_duplicados = set()

    for path in datasets_paths:
        config, core = get_core_info(path)
        path = path / core

        archivo = manejo_archivos.get_archive(path, **config)

        for dato in archivo:
            id_dato = dato.get('id') or dato.get('gbifID') or dato.get('ID')
            if id_dato in ids_vistos:
                ids_duplicados.add(id_dato)
            else:
                ids_vistos.add(id_dato)

    return len(ids_duplicados), list(ids_duplicados)

#---------------------Inciso E----------------------
# countryCode / countryCode
def country_codes_validos(VALOR):
    """
    Args:
       valor (str): valor a verificar

    Returns:
        _type_: true si el valor es valido , false si es invalido
    """

    # Lista de códigos de país válidos
    codigos_paises_validos = set(string.ascii_uppercase[i] 
                                 + string.ascii_uppercase[j] 
                                 for i in range(26) for j in range(26))


    return VALOR in codigos_paises_validos