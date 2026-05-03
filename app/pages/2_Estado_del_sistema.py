import streamlit as st
from pathlib import Path

def mostrar_logs_nativos():
    st.subheader("Logs de Operaciones")
    
    root_path = Path(__file__).resolve().parent.parent.parent
    
    log_path = root_path / "logs" / "operations.log"

    if log_path.exists():
        try:
            with open(log_path, "r", encoding="utf-8") as file:
                # Leemos y limpiamos líneas
                lines = [line.strip() for line in file if line.strip()]

            if not lines:
                st.info("El archivo de logs está vacío.")
                return

            datos_tabla = []
            for line in lines:
                columnas = [col.strip() for col in line.split("|")]
                datos_tabla.append(columnas)

            st.dataframe(
                datos_tabla,
                column_config={
                    "0": "Fecha y Hora",
                    "1": "Dataset",
                    "2": "Operación",
                    "3": "Cantidad"
                },
                use_container_width=True,
                hide_index=True
            )

        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")
    else:
        # Debug: esto te confirmará si la ruta calculada es correcta
        st.error(f"Archivo no encontrado en: {log_path}")
        st.info("Verifica que el nombre sea 'operations.log' (plural) o 'operation.log' (singular).")


mostrar_logs_nativos()