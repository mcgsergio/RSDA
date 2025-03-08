import streamlit as st
import mysql.connector
import pandas as pd

# Configuración de la conexión a MySQL
st.set_page_config(page_title="RSDA Club", layout="wide")

DB_CONFIG = {
    "host": "trolley.proxy.rlwy.net",  # HOST de Railway
    "user": "root",  # Usuario de Railway
    "password": "lCjDZmmLyhoERAeXbBxSdAeVTXLwEJXP",  # Copia la contraseña de Railway
    "database": "railway",  # Nombre de la base de datos en Railway
    "port": 24865  # Puerto de Railway
}

import mysql.connector

def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        st.error(f"Error de conexión a MySQL: {e}")
        return None


def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        st.error(f"Error de conexión a MySQL: {e}")
        return None

def fetch_data(query):
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return pd.DataFrame(data)

# Configurar la interfaz de Streamlit
st.sidebar.image("escudo_rsda.jpeg", width=150)
st.sidebar.title("Menú de Navegación")
menu = st.sidebar.radio("Selecciona una opción", ["Equipos"])

if menu == "Equipos":
    st.title("🏆 Equipos del RSDA")
    equipos_df = fetch_data("SELECT id_equipo, nombre FROM Equipos")
    if equipos_df.empty:
        st.warning("No hay equipos disponibles.")
    else:
        equipo_seleccionado = st.sidebar.selectbox("Selecciona un equipo", equipos_df["nombre"], index=0)
        equipo_id = equipos_df.loc[equipos_df["nombre"] == equipo_seleccionado, "id_equipo"].values[0]
        
        if equipo_seleccionado:
            st.markdown(f"<div class='equipo-container'><h2>{equipo_seleccionado}</h2></div>", unsafe_allow_html=True)
            
            st.subheader("Cuerpo Técnico")
            cuerpo_tecnico_df = fetch_data(f"SELECT nombre, apellido1, apellido2, rol, correo, telefono FROM CuerpoTecnico WHERE id_equipo = '{equipo_id}'")
            if not cuerpo_tecnico_df.empty:
                st.markdown(
                    cuerpo_tecnico_df.to_html(index=False, escape=False, classes='table-style'),
                    unsafe_allow_html=True
                )
            else:
                st.warning("No hay datos del cuerpo técnico.")
            
            st.subheader("Jugadores")
            jugadores_df = fetch_data(f"SELECT * FROM Jugadores WHERE id_equipo = '{equipo_id}'")
            if not jugadores_df.empty:
                st.dataframe(jugadores_df, use_container_width=True)
            else:
                st.warning("No hay jugadores en este equipo.")
            
            st.subheader("📅 Entrenamientos")
            entrenamientos_df = fetch_data(f"SELECT fecha, dia_semana, microciclo, numero_sesion, id_equipo, url_video FROM Entrenamientos WHERE id_equipo = '{equipo_id}' ORDER BY numero_sesion ASC")
            if 'id' in entrenamientos_df.columns:
                entrenamientos_df = entrenamientos_df.drop(columns=['id'])
            if 'url_video' in entrenamientos_df.columns:
                entrenamientos_df["Ver"] = entrenamientos_df["url_video"].apply(lambda x: f'<a href="{x}" target="_blank">🔗 Ver</a>' if pd.notna(x) and x != '' else 'Sin URL')
                entrenamientos_df = entrenamientos_df.drop(columns=['url_video'])
            if entrenamientos_df.empty:
                st.warning("No hay entrenamientos registrados.")
            else:
                st.write(entrenamientos_df.drop(columns=['id'], errors='ignore').to_html(escape=False, index=False, classes='table-style'), unsafe_allow_html=True)
            
            st.subheader("⚽ Partidos")
            partidos_df = fetch_data(f"SELECT fecha, jornada, rival, resultado, campo, id_equipo, url_video FROM Partidos WHERE id_equipo = '{equipo_id}' ORDER BY jornada ASC")
            if 'id' in partidos_df.columns:
                partidos_df = partidos_df.drop(columns=['id'])
            if 'url_video' in partidos_df.columns:
                partidos_df["Ver"] = partidos_df["url_video"].apply(lambda x: f'<a href="{x}" target="_blank">🎥 Ver</a>' if pd.notna(x) and x != '' else 'Sin URL')
                partidos_df = partidos_df.drop(columns=['url_video'])
            if partidos_df.empty:
                st.warning("No hay partidos registrados.")
            else:
                st.write(partidos_df.drop(columns=['id'], errors='ignore').to_html(escape=False, index=False, classes='table-style'), unsafe_allow_html=True)

# Estilos CSS personalizados para centrar datos en las tablas
st.markdown(
    """
    <style>
        .table-style {
            text-align: center;
            margin-left: auto;
            margin-right: auto;
            border-collapse: collapse;
            width: 100%;
        }
        .table-style th, .table-style td {
            text-align: center;
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }
        .table-style tr:hover {
            background-color: #f5f5f5;
        }
        .table-style th {
            background-color: #990000;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)





























