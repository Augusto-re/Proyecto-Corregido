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




def eliminar_registro_de_columna(contexto: dict):
    path = contexto['archivo']
    config = contexto['config']

    archivo = get_archive(path, **config)

    columnas =  list(archivo[0].keys())

    print("selecione columna de interes")
    for i, columna in enumerate(columnas):
        print(f"{i} - {columna}")
    
    columna = int(input("selecionar: "))

    columna = columnas[columna]

    valores = []
    print('Ingrese los valores a eliminar \n exit para salir')
    valor = input('').lower()
    while valor != 'exit':
        valores.append(valor)
        valor = input('').lower()

    # eliminar registros:
    try:
        archivo = list(filter(lambda x: x.get(columna).lower() not in valores , archivo))
        write_archive(archivo, path, **config)
    except Exception as e:
        print("ocurrio un error al modificar el archivo")
        print(f"Error: {e}")
        print(f"Tipo de error: {type(e)}")
    else:
        print("archivo modificador")
    
    return None