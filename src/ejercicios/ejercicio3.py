from utils import manejo_archivos
from utils.config_archivo import  get_core_info
from pathlib import Path
import string




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
def country_codes_invalidos(datasets_paths: Path):
    """
    Args:
        datasets_paths (Path): rutas de los archivos a buscar

    Returns:
        _type_: _description_
    """

    # caracteres alfabéticos en mayúscula, con una longitud de dos caracteres para identificar paises.
    codigos_paises_validos = set(string.ascii_uppercase[i] 
                                 + string.ascii_uppercase[j] 
                                 for i in range(26) for j in range(26))

    codigos_invalidos = set()

    for path in datasets_paths:

        config, core = get_core_info(path)
        path = path / core

        archivo = manejo_archivos.get_archive(path, **config)

        for dato in archivo:
            country_code = dato.get('countryCode')

            # Eliminar espacios en blanco y convertir a mayúsculas para comparar con los códigos válidos
            if country_code:
                country_code = country_code.strip().upper()
                
                # Verificar si el countryCode es válido y agregarlo a la lista de códigos inválidos si no lo es
                if country_code not in codigos_paises_validos:
                    codigos_invalidos.add(country_code)
                    
    return list(codigos_invalidos)