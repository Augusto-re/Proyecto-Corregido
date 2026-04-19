import xml.etree.ElementTree as ET
from pathlib import Path


def parser(value: str) -> str:
    """Convierte secuencias de escape literales a sus caracteres reales."""
    escape_map = {"\\t": "\t", "\\n": "\n", "\\r": "\r"}
    return escape_map.get(value, value)

def get_core_info(meta_path: Path):
    """
    Args:
        meta_path (Path): Path/ruta del la carpeta a leer

    Returns:
        tuple:
            dict : configuracion necesaria para leer el archivo
            str : Nombre del archivo junto con la extension
    """

    # ruta para obtener config 
    meta_path = meta_path / 'meta.xml'
    # Parseo y convierto el archivo en un arbol
    tree = ET.parse(meta_path)
    # Obtengo la raiz
    root = tree.getroot()

    # busca hasta encontrar la 1ra coincidencia | {*} ignora el namespace
    core = root.find(".//{*}core")
    location = root.find(".//{*}location")

    config = {
        "encoding": core.get("encoding", "utf-8").lower(),  # Codificacion
        "fieldsTerminatedBy": parser(core.get("fieldsTerminatedBy", "\t")), # Indica el caracter con el que termina cada fila
        "fieldsEnclosedBy": parser(core.get("fieldsEnclosedBy", "")),   # Columnas encerrada por "x"
        "linesTerminatedBy": parser(core.get("linesTerminatedBy", "\n")),   # Caracter que Inidica el final de la fila
        "ignoreHeaderLines": int(core.get("ignoreHeaderLines", 0))  # Indica cantidad de filas que hay que ignorar para empezar a leer los datos
    }

    file_name = location.text.strip()

    return config, file_name