import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
from PIL import Image

# Configuración de la página
st.set_page_config(page_title="Gestión R.S.D. Alcalá", page_icon="⚽", layout="wide")

# Cargar escudo del club
logo_path = "escudo_rsda.jpeg"  # Asegúrate de tener esta imagen en tu directorio de trabajo
escudo = Image.open(logo_path)

# Función para conectar a la base de datos

def conectar_db():
    return mysql.connector.connect(
        host="localhost",   # Cambiar si la BD está en un servidor remoto
        user="root",  # Reemplaza con tu usuario de MySQL
        password="",  # Reemplaza con tu contraseña
        database="RSDA"
    )

# Funciones para obtener datos de la base de datos
def obtener_equipos():
    conexion = conectar_db()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Equipo;")
    equipos = cursor.fetchall()
    conexion.close()
    return equipos

def obtener_jugadores_por_equipo(id_equipo):
    conexion = conectar_db()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Jugador WHERE id_Equipo = %s;", (id_equipo,))
    jugadores = cursor.fetchall()
    conexion.close()
    return jugadores

def obtener_cuerpo_tecnico_por_equipo(id_equipo):
    conexion = conectar_db()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Cuerpo_Tecnico WHERE id_Equipo = %s;", (id_equipo,))
    cuerpo_tecnico = cursor.fetchall()
    conexion.close()
    return cuerpo_tecnico

def obtener_entrenamientos_por_equipo(id_equipo):
    conexion = conectar_db()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Entrenamiento WHERE id_Equipo = %s;", (id_equipo,))
    entrenamientos = cursor.fetchall()
    conexion.close()
    return entrenamientos

def obtener_partidos_por_equipo(id_equipo):
    conexion = conectar_db()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Partidos WHERE id_Equipo = %s;", (id_equipo,))
    partidos = cursor.fetchall()
    conexion.close()
    return partidos

# Encabezado con el escudo y el nombre del club
col1, col2 = st.columns([1, 4])
with col1:
    st.image(escudo, width=100)
with col2:
    st.markdown("# ⚽ R.S.D. ALCALÁ")
    st.markdown("### Plataforma de Gestión de Equipos y Partidos")

# Menú lateral
st.sidebar.title("Menú")
opcion = st.sidebar.radio("Selecciona una sección:", ["Dashboard", "Equipos"])

# Dashboard con datos generales
if opcion == "Dashboard":
    st.markdown("## 📊 Dashboard General")
    equipos = obtener_equipos()
    if equipos:
        for equipo in equipos:
            st.metric(label=f"{equipo['nombre']}", value=f"{equipo['categoria']} - {equipo['grupo']}")
    else:
        st.warning("No hay equipos registrados.")

# Página de Equipos con pestañas individuales
elif opcion == "Equipos":
    equipos = obtener_equipos()
    if equipos:
        tabs = st.tabs([equipo["nombre"] for equipo in equipos])
        for tab, equipo in zip(tabs, equipos):
            with tab:
                st.markdown(f"## ⚽ {equipo['nombre']}")
                
                # Cuerpo Técnico
                st.markdown("### 🎽 Cuerpo Técnico")
                cuerpo_tecnico = obtener_cuerpo_tecnico_por_equipo(equipo['id_Equipo'])
                if cuerpo_tecnico:
                    df_cuerpo_tecnico = pd.DataFrame(cuerpo_tecnico)
                    st.dataframe(df_cuerpo_tecnico, use_container_width=True)
                else:
                    st.warning("No hay miembros del cuerpo técnico registrados.")
                
                # Jugadores
                st.markdown("### 👥 Jugadores")
                jugadores = obtener_jugadores_por_equipo(equipo['id_Equipo'])
                if jugadores:
                    df_jugadores = pd.DataFrame(jugadores)
                    st.dataframe(df_jugadores, use_container_width=True)
                else:
                    st.warning("No hay jugadores registrados.")
                
                # Entrenamientos
                st.markdown("### 📅 Entrenamientos")
                entrenamientos = obtener_entrenamientos_por_equipo(equipo['id_Equipo'])
                if entrenamientos:
                    df_entrenamientos = pd.DataFrame(entrenamientos)
                    df_entrenamientos["fecha"] = pd.to_datetime(df_entrenamientos["fecha"]).dt.strftime("%d/%m/%Y")
                    df_entrenamientos["Video"] = df_entrenamientos["url_video_completo"].apply(lambda x: f'<a href="{x}" target="_blank">📺 Ver Video</a>')
                    st.write(df_entrenamientos.to_html(escape=False), unsafe_allow_html=True)
                else:
                    st.warning("No hay entrenamientos registrados.")
                
                # Partidos
                st.markdown("### ⚽ Partidos")
                partidos = obtener_partidos_por_equipo(equipo['id_Equipo'])
                if partidos:
                    df_partidos = pd.DataFrame(partidos)
                    df_partidos["fecha"] = pd.to_datetime(df_partidos["fecha"]).dt.strftime("%d/%m/%Y")
                    df_partidos["Video"] = df_partidos["url_video"].apply(lambda x: f'<a href="{x}" target="_blank">📺 Ver Video</a>')
                    st.write(df_partidos.to_html(escape=False), unsafe_allow_html=True)
                else:
                    st.warning("No hay partidos registrados.")
    else:
        st.warning("No hay equipos registrados.")


