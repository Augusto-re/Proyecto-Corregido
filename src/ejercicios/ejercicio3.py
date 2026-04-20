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