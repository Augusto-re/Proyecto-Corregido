from utils import manejo_archivos
from ejercicios import ejercicio3
import random
import string

def generar_registro_vacio(header):
    """
    Genera un diccionario vacío con las claves del encabezado.

    Args:
        header (list): Lista de nombres de columnas.

    Returns:
        dict: Registro vacío con claves del encabezado y valores vacíos.
    """
    return {columna : ' ' for columna in header}

def validar_registro(registro, **config):
    """
    Valida un registro utilizando las funciones de validación correspondientes.

    Args:
        registro (dict): Registro a validar.
        **config: Configuración específica del dataset.

    Returns:
        bool: True si el registro es válido, False en caso contrario.
    """
    for clave, valor in registro.items():
        match clave:
            case "longitudeDecimal" | "decimalLongitude" :
                if not ejercicio3.coordenadas_validas_longitud(valor):
                    return False  # coordenadas inválidas
            case "latitudeDecimal" | "decimalLatitude":
                if not ejercicio3.coordenadas_validas_latitud(valor):
                    return False  # coordenadas inválidas
            case "countryCode":
                if not ejercicio3.country_codes_validos(valor):
                    return False  # código de país inválido
    return True   

def completar_registro_manual(registro):
    """
    Completa un registro vacío con información ingresada por el usuario.

    Args:
        registro (dict): Registro vacío a completar.

    Returns:
        dict: Registro completo listo para ser añadido al CSV.
    """
    for clave in registro.keys():
        valor = input(f"Ingrese el valor para '{clave}': ")
        registro[clave] = valor

def completar_registro_random(registro):
    """
    Completa un registro vacío con información deducida de acuerdo a cada dataset.

    Returns:
        dict: Registro completo listo para ser añadido al CSV.
    """
    for clave in registro.keys():
        match clave:
            case "longitudeDecimal" | "decimalLongitude":
                registro[clave] = random.uniform(-180, 180)  # Genera una longitud aleatoria válida
            case "latitudeDecimal" | "decimalLatitude":
                registro[clave] = random.uniform(-90, 90)  # Genera una latitud aleatoria válida
            case "countryCode":
                registro[clave] = "".join(random.choices(string.ascii_uppercase, k=2))  # Genera un código de país aleatorio de dos letras
            case _ :
                registro[clave] = "n/n" # Asignamos un valor genérico para otras claves

def traer_ultimo_id_existente(dataset):
    """
    Trae el último ID existente en el dataset para generar un nuevo ID.

    Returns:
        str: Último ID existente en el dataset.
    """
    elemento = dataset[-1]  # Obtener el último elemento del dataset
    id_ultimo_elemento = elemento.get('id') or elemento.get('gbifID') or elemento.get('ID')
    return id_ultimo_elemento

def generar_id(dataset, datasets_names ):
    """
        Genera un ID para un registro basado en la configuración del dataset.
    Args:
        
    Returns:
        str: ID generado para el registro.
    """
    id_generado = None
    if (datasets_names == 'A'):
        ultimo_id = int(traer_ultimo_id_existente(dataset))  
        id_generado = str(ultimo_id + 1)
        
    elif (datasets_names  == 'B'):
        ultimo_id = int(traer_ultimo_id_existente(dataset))
        id_generado = str(ultimo_id + 1)
    elif (datasets_names  == 'C'):
        ultimo_id = traer_ultimo_id_existente(dataset)
        parte_numerica , parte_alfabetica = ultimo_id.split('@')
        id_generado =  str(int(parte_numerica) + 1) + '@' + parte_alfabetica
    else:
        print("Nombre de dataset no válido.")
        
    return id_generado


def insertar_registro(DATASETS_PATH_PROCESSED , registros , archivo , **configs):
    ruta = (DATASETS_PATH_PROCESSED / configs.get('core'))
    #si archivo procesado se encuentra en la carpeta processed_datasets + agregar el nuevo registro al final del archivo
    if (ruta.exists()):
        manejo_archivos.appened_archive([registros], ruta, **configs)
    else:
        # Creamos una lista que contenga todos los elementos y escribimos una sola vez
        archivo.append(registros)
        manejo_archivos.write_archive(archivo, ruta, **configs) 