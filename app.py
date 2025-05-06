import streamlit as st
from utils.data_loader import cargar_datos
import pandas as pd
import json

# Configuración básica de la página
st.set_page_config(
    page_title="Portal SPS: Cliengo-Tactica",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #003366;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #0066cc;
        margin-bottom: 0.5rem;
    }
    .card {
        /*background-color: #f8f9fa;*/
        border-radius: 0.5rem;
        padding: 1.5rem;
        box-shadow: 0 0.25rem 0.5rem rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Título y descripción
st.markdown('<h1 class="main-header">🔔 Portal de Leads SPS: Cliengo - Tactica</h1>', unsafe_allow_html=True)

# Información principal
st.markdown("""
<div class="card">
<h2 class="sub-header">Bienvenido al Portal de Leads de SPS</h2>
<p>Esta aplicación permite visualizar y analizar el flujo de leads que ingresan a través de Cliengo 
(Chatbot y WhatsApp) mediante su integración con el CRM Tactica.</p>

<p>👈 Usá la barra lateral para navegar entre las diferentes secciones:</p>
<ul>
    <li><b>Página Principal</b>: Resumen general acotado por Vendedor y Estado</li>
    <li><b>Leads por Horario</b>: Análisis del caudal de leads por franjas horarias</li>
    <li><b>Leads por Servicio</b>: Distribución de leads por categoría y servicio</li>
    <li><b>Detalles</b>: Exploración detallada de todos los datos y descarga en CSV</li>
</ul>
</div>
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
    
    # Mostrar el DataFrame de leads en Streamlit
    #st.markdown('<h2 class="sub-header">Leads</h2>', unsafe_allow_html=True)
    #st.dataframe(leads_df)  # Mostrar el DataFrame de leads

    # Mostrar el DataFrame de resumen en Streamlit
    st.markdown('<h2 class="sub-header">Resumen de Ventas por Vendedor</h2>', unsafe_allow_html=True)
    st.dataframe(resumen_df)


# Información adicional
st.markdown("""
<div class="card">
<h2 class="sub-header">Sobre los datos</h2>
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