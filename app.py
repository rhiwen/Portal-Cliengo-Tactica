import streamlit as st
from utils.data_loader import cargar_datos
import pandas as pd
import hmac
import json
from datetime import datetime
import pytz  # tener pytz instalado
import time

# Configuración básica de la página
st.set_page_config(
    page_title="Portal SPS: Cliengo-Tactica",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inicializar el estado de la sesión
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""

# Inicializar la hora de la última actualización
if "last_update" not in st.session_state:
    st.session_state.last_update = datetime.now()

def check_password(username, password):
    # Verificar si el usuario existe en secrets.toml
    if username in st.secrets["users"]:
        # Comparar la contraseña de forma segura
        stored_password = st.secrets["users"][username]["password"]
        if hmac.compare_digest(stored_password, password):
            return True
    return False

def login():
    st.title("SPS Alarmas - Sistema de Gestión de Leads")
    
    with st.form("login_form"):
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Iniciar Sesión")
        
        if submit:
            if check_password(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.role = st.secrets["users"][username]["role"]
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")

def logout():
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.rerun()

# Mostrar login o contenido principal
if not st.session_state.authenticated:
    login()
else:
    # Mostrar el mensaje de bienvenida en la barra lateral
    st.sidebar.write(f"Bienvenido, {st.session_state.username}. (rol: {st.session_state.role})")
    if st.sidebar.button("Cerrar Sesión"):
        logout()

    # Estilos CSS personalizados
    st.markdown("""
        <style>
        .main-header {
            font-size: 3rem;  /* Aumentar tamaño de fuente */
            color: #003366;
            text-align: center;
            margin-bottom: 1rem;
        }
        .sub-header {
            font-size: 2rem;  /* Aumentar tamaño de fuente */
            color: #0066cc;
            margin-bottom: 0.5rem;
            font-weight: bold;  /* Títulos en negrita */
        }
        .card {
            border-radius: 0.5rem;
            padding: 2rem;  /* Aumentar padding */
            box-shadow: 0 0.25rem 0.5rem rgba(0,0,0,0.1);
            margin-bottom: 1rem;
            width: 100%;  /* Hacer que el cuadro ocupe toda la pantalla */
        }
        </style>
        """, unsafe_allow_html=True)

    # Cargar datos una sola vez
    df = cargar_datos()

    # Cargar el JSON desde el archivo resumen.json
    with open('resumen.json', 'r') as json_file:
        resumen_data = json.load(json_file)

    # Verificar si hay un error en la carga de datos del resumen
    if resumen_data['error']:
        st.error(resumen_data['mensaje'])
    else:
        # Convertir la lista de datos a un DataFrame
        resumen_df = pd.DataFrame(resumen_data['data'])

        # Mostrar la hora actual y la última actualización
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<h3 class="main-header">🔔 Leads hasta el momento</h3>', unsafe_allow_html=True)
    with col2:
    # Obtener la hora local de Buenos Aires
        buenos_aires_tz = pytz.timezone('America/Argentina/Buenos_Aires')
        current_time = datetime.now(buenos_aires_tz).strftime('%H:%M')
        last_update_time = st.session_state.last_update.astimezone(buenos_aires_tz).strftime('%H:%M')  # Corregido
        st.markdown(f"<h3>{current_time}</h3> <i>Última act.:</i> {last_update_time}", unsafe_allow_html=True)


    # Mostrar el Resumen de Leads por Agente
    st.dataframe(resumen_df, use_container_width=True, hide_index=True)

    # Información principal
    st.markdown("""
    <div class="card">
    <h2 class="sub-header">Bienvenido al Portal de Leads de SPS</h2>
    <p>Esta aplicación permite visualizar y analizar el flujo de leads que ingresan a través de Cliengo 
    (Chatbot y WhatsApp) mediante su integración con el CRM Tactica.</p>

    <p>👈 Usá la barra lateral para navegar entre las diferentes secciones:</p>
    <ul>
        <li><b>Página Principal</b>: Resumen general acotado por Agente y Estado</li>
        <li><b>Leads por Horario</b>: Análisis del caudal de leads por franjas horarias</li>
        <li><b>Leads por Servicio</b>: Distribución de leads por categoría y servicio</li>
        <li><b>Detalles</b>: Exploración detallada de todos los datos y descarga en CSV</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    # Información adicional
    st.markdown("""
    <div class="card">
    <h3 class="sub-header">Sobre los datos</h3>
    <p>- Actualmente los datos se cargan desde archivos JSON (en el caso del cuadro superior)
    y CSV (en las demás páginas) de prueba. Próximamente
    se implementará la conexión directa a la API de Tactica para obtener datos en tiempo real.</p>

    <p><b>- Nota:</b> Los reportes están diseñados según los requerimientos específicos 
    de SPS para analizar el alto caudal de actividad entre las 17:00 y 21:00 horas
    y su clasificación por servicios.</p>
    </div>
    """, unsafe_allow_html=True)

# Pie de página
st.markdown("---")
st.markdown("© 2025 - Portal de Leads SPS | Versión 1.0")