import sys
import os
import csv 
from pathlib import Path 
from collections import Counter
from datetime import datetime 


sys.path.append(os.path.abspath(".."))
archivo = Path.cwd()/'archivo'/'logs_catedra.csv'

def usuarios_act1_turno_mañana(reader, formato=None):
    """Función que retorna todos los usuarios que realizaron la actividad 1 (act1)
    correspondiente al turno mañana, desde una IP de la facultad.
    
    Parámetros:
    - reader: Un objeto csv.DictReader con los datos ya cargados.
    - formato (opcional): Indica cómo mostrar los nombres de usuario:
      - "M" para mayúsculas,
      - "m" para minúsculas,
      - None para tal como aparece en el dataset.
      
    Retorna:
    - Una lista de usuarios que cumplan las condiciones."""
    
    usuarios = []  # Lista donde almacenaremos los nombres de los usuarios
    
    # Recorremos cada fila del archivo
    for fila in reader:
        evento = fila["Nombre evento"].lower()
        contexto = fila["Contexto del evento"].lower()
        ip = fila["Dirección IP"]

        # Verificamos si el "nombre evento" contiene "curso visto"
        # y si la "dirección IP" empieza con "163.10" (dirección de la facultad)
        if "curso visto" in evento and ip.startswith("163.10"):
            
            # Obtenemos el nombre de usuario
            usuario = fila["Nombre completo del usuario"]
            
            # Si el parámetro formato es "M", convertimos el nombre de usuario a mayúsculas
            if formato == "M":
                usuario = usuario.upper()
            # Si el parámetro formato es "m", convertimos el nombre de usuario a minúsculas
            elif formato == "m":
                usuario = usuario.lower()
            
            # Agregamos el nombre de usuario a la lista de usuarios
            usuarios.append(usuario)
    
    # Retornamos la lista de usuarios
    return usuarios

with open(archivo, encoding="utf-8") as file:
    reader = csv.DictReader(file, delimiter=",")

     # Llamamos a la función con el reader (el contenido del archivo) y el formato
    usuarios = usuarios_act1_turno_mañana(reader, formato="m")  # Puedes cambiar "M" a "m" o None
    
# Imprimimos los resultados
print("Usuarios que realizaron la act1 turno mañana desde una IP de la facultad:")
for usuario in usuarios:
    print(usuario)



def mas_popular(csv_reader, modo=None):
    users = filter(lambda x:  es_nocturno(x["Hora"]), csv_reader)
    return Counter( map(lambda x: x['Nombre completo del usuario'], users)).most_common(1)


def usuarios_act1_turno_mañana(reader, formato=None):
    """Función que retorna todos los usuarios que realizaron la actividad 1 (act1)
    correspondiente al turno mañana, desde una IP de la facultad.
    
    Parámetros:
    - reader: Un objeto csv.DictReader con los datos ya cargados.
    - formato (opcional): Indica cómo mostrar los nombres de usuario:
      - "M" para mayúsculas,
      - "m" para minúsculas,
      - None para tal como aparece en el dataset.
      
    Retorna:
    - Una lista de usuarios que cumplan las condiciones."""
    
    usuarios = []  # Lista donde almacenaremos los nombres de los usuarios
    
    
    # Recorremos cada fila del archivo
    for fila in reader:
        evento = fila["Nombre evento"].lower()
        contexto = fila["Contexto del evento"].lower()
        ip = fila["Dirección IP"]

        # Verificamos si el "nombre evento" contiene "curso visto"
        # y si la "dirección IP" empieza con "163.10" (dirección de la facultad)
        if "curso visto" in evento and ip.startswith("163.10"):
            
            # Obtenemos el nombre de usuario
            usuario = fila["Nombre completo del usuario"]
            
            # Si el parámetro formato es "M", convertimos el nombre de usuario a mayúsculas
            if formato == "M":
                usuario = usuario.upper()
            # Si el parámetro formato es "m", convertimos el nombre de usuario a minúsculas
            elif formato == "m":
                usuario = usuario.lower()
            
            # Agregamos el nombre de usuario a la lista de usuarios
            usuarios.append(usuario)
    
    
    return usuarios


# Función para mostrar el menú de opciones y obtener la elección del usuario
def menu():
    sys.path.append(os.path.abspath(".."))
    archivo = Path.cwd()/'archivo'/'logs_catedra.csv'
    
    with open(archivo, encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=",")

        print("\nMenú de opciones:")
        print("1. Mostrar nombres en MAYÚSCULAS")
        print("2. Mostrar nombres en minúsculas")
        print("3. Mostrar nombres tal como aparecen en el dataset")
        print("4. Salir")
            
        opcion = input("Seleccione una opción (1-4): ")
            
        if opcion == "1":
            usuarios = usuarios_act1_turno_mañana(reader, formato="M")
            print("\nUsuarios con nombres en MAYÚSCULAS:")
        elif opcion == "2":
            usuarios = usuarios_act1_turno_mañana(reader, formato="m")
            print("\nUsuarios con nombres en minúsculas:")
        elif opcion == "3":
            usuarios = usuarios_act1_turno_mañana(reader, formato=None)
            print("\nUsuarios con nombres tal como aparecen en el dataset:")
        elif opcion == "4":
            print("¡Hasta luego!")
            return  
        else:
            print("Opción inválida.seleccione una opción entre 1 y 4.")
            return 

        # Imprimimos los usuarios que cumplieron las condiciones
        if usuarios:
            for usuario in usuarios:
                print(usuario)
        else:
            print("No se encontraron usuarios que cumplan las condiciones.")

# Bloque principal (main) del programa
if __name__ == "__main__":
    menu()  

