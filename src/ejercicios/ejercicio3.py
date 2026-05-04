from utils import manejo_archivos
from utils.config_archivo import  get_core_info
from utils.constantes import CAMPOS_FECHA_DWC
from pathlib import Path
import string
from datetime import datetime
from utils import manejo_archivos
from ejercicios.ejercicio3 import (
    coordenadas_invalidas,
    fechas_invalidas,
    registros_duplicados,
)



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
