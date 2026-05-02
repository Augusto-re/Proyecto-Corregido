from pathlib import Path

PROJECT_PATH = Path(__file__).parent.parent.parent # Path a la raiz del archivo #
DATASETS_PATH_RAW = PROJECT_PATH / "raw_datasets" 
DATASETS_PATH_PROCESSED = PROJECT_PATH / "processed_datasets" 
LOGS_PATH = PROJECT_PATH / "logs" 

# Fechas estandar en Darwin Core
CAMPOS_FECHA_DWC = [
    "eventDate",
    "modified",
    "dateIdentified",
    "verbatimEventDate",
    "georeferencedDate",
]