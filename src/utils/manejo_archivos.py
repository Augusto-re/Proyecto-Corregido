import csv
from pathlib import Path

"""
encoding
fieldsTerminatedBy -> Como se separan las columnas.
linesTerminatedBy -> Cómo se separan las filas.
fieldsEnclosedBy -> Indica como estan encerrados los campos.
"""
"""
    import csv
file_route = Path('ejemplos') / "clase05" / "songs_normalize.csv"

file = open(file_route, "r")
csv_reader = csv.reader(file, delimiter=',')
#encabezado = csvreader.__next__()
header = next(csv_reader)
print(header)
file.close()

"""


def get_header(path: Path, **config):
    """
    Args:
        path (Path): Ruta del archivo a leer
        **config: Configuracion para abrir el archivo
    Returns:
        list(str): Nombre de los encabezados de cada columna
    """
    encoding = config.get("encoding", "utf-8")
    delimiter = config.get("fieldsTerminatedBy", "\t")
    enclosure = config.get("fieldsEnclosedBy", "")

    # Uso nombre del parametro csv
    quotechar = enclosure if enclosure else None

    with path.open(encoding=encoding, newline="") as f:
        reader = csv.reader(f, delimiter=delimiter, quotechar=quotechar)

        # Tomar la siguiente como header
        return next(reader, None)


# Esto es lo actual en el proyecto

# def get_archive(path: Path, **config):
#    """
#   Args:
#        path (Path): Ruta del archivo a leer
#      **config: Configuracion para abrir el archivo
#
#    Returns:
#        list(dict): lista de dict, que cada elemento es una fila del documento
#    """
#    #encoding = config.get("encoding", "utf-8")
#    delimiter = config.get("fieldsTerminatedBy", "\t")
#    #enclosure = config.get("fieldsEnclosedBy", "")
#
#    with path.open(encoding=encoding, newline="") as f:
#        if enclosure:
#            reader = csv.DictReader(
#                f,
#                delimiter=delimiter,
#                quotechar=enclosure
#            )
#        else:
#            reader = csv.DictReader(
#                f,
#                delimiter=delimiter
#            )
#
#        return list(reader)


# Esto es con el yield


def get_archive(path: Path, **config):
    """
    Genera las filas del dataset de a una, sin cargar todo en memoria.
    Usar directamente en un bucle for:
        for fila in get_archive(path, **config):
            ...
    Si necesitás la lista completa (para modificar y reescribir),
    materializarla explícitamente:
        filas = list(get_archive(path, **config))

    Args:
        path (Path): Ruta del archivo a leer
        **config: Configuracion para abrir el archivo

    Yields:
        dict: Una fila del dataset como diccionario {columna: valor}
    """
    encoding = config.get("encoding", "utf-8")
    delimiter = config.get("fieldsTerminatedBy", "\t")
    enclosure = config.get("fieldsEnclosedBy", "")

    f = path.open(encoding=encoding, newline="")
    try:
        if enclosure:
            reader = csv.DictReader(f, delimiter=delimiter, quotechar=enclosure)
        else:
            reader = csv.DictReader(f, delimiter=delimiter)

        for fila in reader:
            yield fila
    finally:
        f.close()


def write_archive(data: list, path: Path, **config):
    """
    Args:
        data (list): Lista de diccionarios a escribir en el archivo
        path (Path): Ruta del archivo a escribir
        **config: Configuracion para abrir el archivo

    Returns:
        None
    """
    encoding = config.get("encoding", "utf-8")
    delimiter = config.get("fieldsTerminatedBy", "\t")
    enclosure = config.get("fieldsEnclosedBy", "")

    columnas = []
    for r in data:
        for k in r.keys():
            if k not in columnas:
                columnas.append(k)

    with path.open(encoding=encoding, mode="w", newline="") as f:
        if enclosure:
            writer = csv.DictWriter(
                f, fieldnames=columnas, delimiter=delimiter, quotechar=enclosure
            )
        else:
            writer = csv.DictWriter(f, fieldnames=columnas, delimiter=delimiter)

        writer.writeheader()
        writer.writerows(data)


def appened_archive(data: list, path: Path, **config):
    """
    Args:
        data (list): Lista de diccionarios a escribir en el archivo
        path (Path): Ruta del archivo a escribir
        **config: Configuracion para abrir el archivo

    Returns:
        None
    """
    encoding = config.get("encoding", "utf-8")
    delimiter = config.get("fieldsTerminatedBy", "\t")
    enclosure = config.get("fieldsEnclosedBy", "")

    columnas = []
    for r in data:
        for k in r.keys():
            if k not in columnas:
                columnas.append(k)

    with path.open(encoding=encoding, mode="a", newline="") as f:
        if enclosure:
            writer = csv.DictWriter(
                f, fieldnames=columnas, delimiter=delimiter, quotechar=enclosure
            )
        else:
            writer = csv.DictWriter(f, fieldnames=columnas, delimiter=delimiter)

        # No escribimos el header porque ya existe, solo las filas nuevas
        writer.writerows(data)
