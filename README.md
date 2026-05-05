# Integrantes :

- Santiago Ariel Alvares
- Marcos Paulo Pissani
- Augusto Retamozo
- Nicolás Guzzo
- Laureano Savia

# Instalacion de las dependencias <!-- Título grande con h1 -->

## Entorno Virtual

> ⚠ Este proyecto requiere Python 3.13.12

```bash
Creacion : python -m venv venv

# Activar entorno
# En Linux/macOS:
source venv/bin/activate
# En Windows:
source venv/scripts/activate

#Desactivar entorno:
deactivate
```

### Instalar todas las dependencias con el siguiente comando :

- `pip install -r requirements.txt` : installa todos los entornos que son requeridos, los que estan escritos en requirements.tx

# Guia para instalacion individual

### Se recomienda generar un entorno virtual -> (venv) Activado

## Jupyter Notebook

```bash
#instalar Jupyter
$ pip install notebook

#Iniciar servidor de Jupyter
$ jupyter notebook

# Finalizar servidor (en consola
$ ctrl + c

# Ver versión instalada
$ pip show jupyter
```

## Streamlit

```bash
# Instalar Streamlit
$ pip install streamlit

# Ejecutar aplicación
$ streamlit run nombre_archivo.py

# Finalizar servidor (en consola
$ ctrl + c
```
