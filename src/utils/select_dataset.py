from .constantes import DATASETS_PATH_PROCESSED, DATASETS_PATH_RAW
from .config_archivo import get_core_info
from pathlib import Path

def ejecutar_sobre_dataset(datasets_paths:list[Path], funcion):
    # Obtener nombres de datasets desde los paths
    nombres = [path.name for path in datasets_paths]

    # Generar opciones A, B, C...
    opciones = [chr(ord('A') + i) for i in range(len(nombres))]

    # Construir texto dinámico
    partes = [f"{op}) {nombre}" for op, nombre in zip(opciones, nombres)]
    texto = "Seleccione un dataset: " + ", ".join(partes)

    ingresar = input("¿Desea operar sobre un dataset? (s/n): ").lower()
    while ingresar not in ['s', 'n']:
        ingresar = input("Ingrese 's' o 'n': ").lower()

    while ingresar == 's':
        dataset_name = input(f'{texto}').upper()

        if dataset_name not in opciones:
            print("Opción inválida.")
            continue

        index = ord(dataset_name) - ord('A')

        # Construyo un "contexto" del dataset
        raw_path = datasets_paths[index]  # raw
        config, core = get_core_info(raw_path)

        processed_path = DATASETS_PATH_PROCESSED / raw_path.name
        archivo = processed_path / core

        datos = {
            "processed_path": processed_path,
            "raw_path": raw_path,
            "config": config,
            "core": core,
            "archivo": archivo,
        }

        funcion(datos)

        ingresar = input("\n¿Desea operar sobre otro dataset? (s/n): ").lower()
        while ingresar not in ['s', 'n']:
            ingresar = input("Ingrese 's' o 'n': ").lower()