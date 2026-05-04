import datetime
from pathlib import Path
from utils.constantes import LOGS_PATH
#------------------Inciso A------------------

def fecha_hora_actual():
    ahora = datetime.datetime.now()
    return ahora.strftime("%Y-%m-%d %H:%M:%S")

#------------------Inciso B , C Y D------------------

def registrar_operacion(operacion, num_registros, nombre_dataset):

    fecha = fecha_hora_actual()
    path = LOGS_PATH / 'operatios.log'
    if path.exists():
        append_operations(fecha, operacion, num_registros, nombre_dataset)
    else:
        write_operations(fecha, operacion, num_registros, nombre_dataset, path)

def write_operations(fecha , operacion ,num_registros ,nombre_dataset , path : Path):
    
    with open(path, mode="w" , encoding="utf-8") as f:
        if num_registros == 0:
            f.write(f"{fecha} | {nombre_dataset} | {operacion} | ERROR\n")
        else:
            f.write(f"{fecha} | {nombre_dataset} | {operacion} | {num_registros} registros\n")

def append_operations(fecha , operacion ,num_registros ,nombre_dataset):
    path = LOGS_PATH / 'operatios.log'
    with open(path, mode="a" , encoding="utf-8") as f:
        if num_registros == 0:
            f.write(f"{fecha} | {nombre_dataset} | {operacion} | ERROR\n")
        else:
            f.write(f"{fecha} | {nombre_dataset} | {operacion} | {num_registros} registros\n")