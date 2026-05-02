'''
Ejercicio 6.A
Escribir una función que elimine un registro dado su identificador (occurrenceID, por
ejemplo). En caso de no encontrarlo informe del error.

Ejercicio 6.B
Escribir una función que elimine registros cuyo valor en una columna pertenezca a una lista
de valores suministrada por el usuario.
Ejemplo:
"Argentina", "Chile"
'''

from utils.manejo_archivos import get_archive, write_archive

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


def eliminar_registro(contexto: dict):
    path = contexto['archivo']
    config = contexto['config']

    id_input = input("Ingrese un occurrenceID a eliminar: ")
    id_objetivo = normalizar_id(id_input)

    archivo = get_archive(path, **config)

    encontrado = False

    for i, registro in enumerate(archivo):
        if registro.get("occurrenceID") == id_objetivo:
            del archivo[i]
            encontrado = True
            break

    if not encontrado:
        print(f"No se encontró un registro con occurrenceID = {id_objetivo}")
        return

    write_archive(archivo, path, **config)
    print(f"Se eliminó correctamente el registro {id_objetivo}")