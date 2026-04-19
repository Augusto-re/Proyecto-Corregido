import csv
from pathlib import Path

'''
encoding
fieldsTerminatedBy -> Como se separan las columnas.
linesTerminatedBy -> Cómo se separan las filas.
fieldsEnclosedBy -> Indica como estan encerrados los campos.
'''
'''
    import csv
file_route = Path('ejemplos') / "clase05" / "songs_normalize.csv"

file = open(file_route, "r")
csv_reader = csv.reader(file, delimiter=',')
#encabezado = csvreader.__next__()
header = next(csv_reader)
print(header)
file.close()

'''

def get_header(path : Path, **config):
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
        reader = csv.reader(
            f,
            delimiter=delimiter,
            quotechar=quotechar
        )

        # Tomar la siguiente como header
        return next(reader, None)
    

def get_archive(path: Path, **config):
    """
    Args:
        path (Path): Ruta del archivo a leer
        **config: Configuracion para abrir el archivo

    Returns:
        list(dict): lista de dict, que cada elemento es una fila del documento
    """    
    encoding = config.get("encoding", "utf-8")
    delimiter = config.get("fieldsTerminatedBy", "\t")
    enclosure = config.get("fieldsEnclosedBy", "")

    with path.open(encoding=encoding, newline="") as f:
        if enclosure:
            reader = csv.DictReader(
                f,
                delimiter=delimiter,
                quotechar=enclosure
            )
        else:
            reader = csv.DictReader(
                f,
                delimiter=delimiter
            )

        return list(reader)