from utils.manejo_archivos import get_archive, write_archive
from utils.constantes import CAMPOS_FECHA_DWC
import operator
from .ejercicio3 import country_codes_validos, coordenadas_validas_latitud, coordenadas_validas_longitud, validar_fecha_dwc
from .ejercicio7 import registrar_operacion

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

    registrar_operacion(operacion='DELETE', num_registros=eliminados, nombre_dataset=datos['raw_path'].name)
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

    registrar_operacion(operacion='DELETE', num_registros=eliminados, nombre_dataset=datos['raw_path'].name)
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

    registrar_operacion(operacion='DELETE', num_registros=eliminados, nombre_dataset=datos['raw_path'].name)
    if eliminados == 0:
        print("No se eliminaron registros")
        return

    write_archive(nuevo, path, **config)

    print(f"Registros eliminados: {eliminados}")
    print("Archivo modificado correctamente")



def es_fila_valida(fila: dict, name: str, ids_vistos: set):
    errores = []

    # -------- countryCode --------
    if "countryCode" in fila:
        code = (fila.get("countryCode") or "").strip().upper()

        if not code:
            errores.append("countryCode vacío")
        elif not country_codes_validos(code):
            errores.append("countryCode inválido")

    if name != "iadiza":
        # -------- coordenadas --------
        lat_key = None
        lon_key = None

        if "latitudeDecimal" in fila:
            lat_key = "latitudeDecimal"
        elif "decimalLatitude" in fila:
            lat_key = "decimalLatitude"

        if "longitudeDecimal" in fila:
            lon_key = "longitudeDecimal"
        elif "decimalLongitude" in fila:
            lon_key = "decimalLongitude"

        if lat_key and lon_key:
            lat = fila.get(lat_key)
            lon = fila.get(lon_key)

            if lat is not None and lon is not None:
                try:
                    lat = float(lat)
                    lon = float(lon)

                    if not coordenadas_validas_latitud(lat):
                        errores.append("latitud inválida")

                    if not coordenadas_validas_longitud(lon):
                        errores.append("longitud inválida")

                except (ValueError, TypeError):
                    errores.append("coordenadas inválidas")

    # -------- fechas --------
    campos_presentes = [campo for campo in CAMPOS_FECHA_DWC if campo in fila]

    if campos_presentes:
        alguna_valida = False

        for campo in campos_presentes:
            valor = fila.get(campo)

            if valor is None:
                continue

            if validar_fecha_dwc(valor):
                alguna_valida = True
                break

        if not alguna_valida:
            errores.append("fecha inválida")

    # -------- duplicados --------
    id_dato = fila.get('id') or fila.get('gbifID') or fila.get('ID')

    if id_dato:
        if id_dato in ids_vistos:
            errores.append("registro duplicado")
        else:
            ids_vistos.add(id_dato)

    return (len(errores) == 0, errores)


def validar_y_crear(datos: dict):
    name = datos["raw_path"].name
    raw_path = datos['raw_path'] / datos['core']
    processed_path = datos['archivo']

    config = datos['config']

    archivo = get_archive(raw_path, **config)

    registros_validos = []
    eliminados = 0
    motivos = {}

    ids_vistos = set()
    
    for fila in archivo:
        es_valida, errores = es_fila_valida(fila, name, ids_vistos)

        if es_valida:
            registros_validos.append(fila)
        else:
            eliminados += 1
            for error in errores:
                motivos[error] = motivos.get(error, 0) + 1

    total = len(archivo)
    porcentaje = (eliminados / total * 100) if total > 0 else 0

    # guardar nuevo archivo (processed)
    write_archive(registros_validos, processed_path, **config)

    registrar_operacion(operacion='DELETE', num_registros=eliminados, nombre_dataset=datos['raw_path'].name)
    print(f'eliminados: {eliminados} \n porcentaje: {porcentaje} \n motivos: {motivos} \n')

    return