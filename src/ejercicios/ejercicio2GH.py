from utils import manejo_archivos
from utils.config_archivo import get_core_info
from pathlib import Path
#ejercicio 2G
def valuesInColumn(dataset:Path, columns_name: str):

    values = set()
    headers = manejo_archivos.get_header(dataset)
    if columns_name not in headers:
        return f"la columna '{columns_name}' no existe en el archivo {archivo_path}"
    for path in dataset:
        config, core = get_core_info(path)
        archivo_path = path / core
        archivo = manejo_archivos.get_archive(archivo_path, **config)
        values.update(archivo[columns_name])


    return len(values)

print(valuesInColumn("C:\Users\cacog\code\raw_datasets\Colección Ornitológica del IADIZA-CCT CONICET Mendoza IADIZA-COI\Colecci├│n Ornitol├│gica del IADIZA-CCT CONICET Mendoza IADIZA-COI\occurrence.txt","publisher"))

#ejercicio 2H
def valueFrecuenseInClolumn(dataset: Path, columns_name: str):

    values_in_column = {}

    for path in dataset:
        config, core = get_core_info(path)
        archivo_path = path / core
        archivo = dict(manejo_archivos.get_archive(archivo_path, **config))
        values_in_column = {}
        for value in archivo[columns_name]:
            values_in_column[value] = values_in_column.get(value, 0) + 1


    return values_in_column