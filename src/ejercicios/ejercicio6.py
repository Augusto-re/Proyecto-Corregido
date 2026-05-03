from utils.manejo_archivos import get_archive, write_archive
import operator


def filtro(archivo: list[dict], filtros: dict, condicion='=='):
    """filtro para eliminar registro en datasets

    Args:
        archivo (list[dict]): datasets
        filtros (dict): diccionario con key nombre de columnas y values list[str]
        condicion (str, optional): condicional a utilizar. por defecto '=='.

    Returns:
        nuevo_registro (list[dict]): lista de registros con el filtro aplicado
        eliminados (int): cantidad de registro eliminados 
    """    
    # operaciones de comparacion
    ops = {
        '==': operator.eq,
        '!=': operator.ne,
        '>=': operator.ge,
        '>': operator.gt,
        '<=': operator.le,
        '<': operator.lt
    }

    try:
        op = ops[condicion]
    except:
        return [], 0
    
    nuevo_archivo = []
    eliminados = 0

    # Para cada fila
    for row in archivo:
        eliminar = False

        # aplico el filtro
        for col, valores in filtros.items():

            dato = str(row.get(col)).strip().lower()

            if dato is None:
                continue

            for valor in valores:
                valor = str(valor).strip().lower()

                try:
                    if op(dato, valor):
                        eliminar = True
                        break
                except Exception:
                    continue

            if eliminar:
                break

        if eliminar:
            eliminados += 1
        else:
            nuevo_archivo.append(row)

    return nuevo_archivo, eliminados

def normalizar_id(id_input):
    """_summary_

    Args:
        id_input (str): ocurrenceID incompleto

    Returns:
        str: devuelve el ocurrence id completo como esta en los archivos
    """    
    prefijo = "IADIZA:COI:"
    
    # si comineza con el prefijo se deduse que esta bien escrito
    if id_input.startswith(prefijo):
        return id_input
    
    return f"{prefijo}{id_input.zfill(6)}"


def eliminar_registro(datos: dict):
    path = datos['archivo']
    config = datos['config']

    id_objetivo = normalizar_id(input("Ingrese occurrenceID: "))

    archivo = get_archive(path, **config)

    filtros = {
        "occurrenceID": [id_objetivo]
    }

    nuevo, eliminados = filtro(archivo, filtros)

    if eliminados == 0:
        print(f"No se encontró el registro {id_objetivo}")
        return

    write_archive(nuevo, path, **config)
    print(f"Se eliminó correctamente el registro {id_objetivo}")


def eliminar_registro_de_columna(datos: dict):
    path = datos['archivo']
    config = datos['config']

    archivo = get_archive(path, **config)
    columnas = list(archivo[0].keys())

    print("Seleccione columna de interés")
    for i, col in enumerate(columnas):
        print(f"{i} - {col}")

    col_idx = int(input("Seleccionar: "))
    columna = columnas[col_idx]

    valores = []
    print("Ingrese valores a eliminar (exit para terminar):")

    while True:
        v = input().strip().lower()
        if v == "exit":
            break
        valores.append(v)

    filtros = {
        columna: valores
    }

    nuevo, eliminados = filtro(archivo, filtros)

    if eliminados == 0:
        print("No se eliminaron registros")
        return

    write_archive(nuevo, path, **config)

    print(f"Registros eliminados: {eliminados}")
    print("Archivo modificado correctamente")


def eliminar_multiples_columnas_valores(datos: dict):
    path = datos['archivo']
    config = datos['config']

    archivo = get_archive(path, **config)
    columnas = list(archivo[0].keys())

    print("Seleccione columnas de interés")
    for i, col in enumerate(columnas):
        print(f"{i} - {col}")

    columnas_interes = []

    print("Ingrese índices (-1 para terminar):")
    while True:
        col_idx = int(input("Seleccionar: "))
        if col_idx == -1:
            break
        columnas_interes.append(columnas[col_idx])

    filtros = {}

    for col in columnas_interes:
        print(f"Ingrese valores para la columna '{col}' (exit para terminar):")
        valores = []

        while True:
            v = input().strip().lower()
            if v == "exit":
                break
            valores.append(v)

        filtros[col] = valores

    condicion = input("ingrese el condicional a poner ej: '=='")
    nuevo, eliminados = filtro(archivo, filtros, condicion)

    if eliminados == 0:
        print("No se eliminaron registros")
        return

    write_archive(nuevo, path, **config)

    print(f"Registros eliminados: {eliminados}")
    print("Archivo modificado correctamente")

def validar_y_crear ():
    
    return None