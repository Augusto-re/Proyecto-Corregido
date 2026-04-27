


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
    return True

def completar_registro():
    """
    Completa un registro vacío con información deducida de acuerdo a cada dataset.

    Returns:
        dict: Registro completo listo para ser añadido al CSV.
    """
    return {}

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
    if (datasets_names == 'iadiza'):
        ultimo_id = traer_ultimo_id_existente(dataset)  
        id_generado = ultimo_id + 1
        
    elif (datasets_names  == 'inaturalist'):
        ultimo_id = traer_ultimo_id_existente(dataset)
        id_generado = ultimo_id + 1  
    else:
        ultimo_id = traer_ultimo_id_existente(dataset)
        parte_numerica , parte_alfabetica = ultimo_id.split('@')
        id_generado =  parte_numerica + 1 + '@' + parte_alfabetica
        
    return id_generado