import streamlit as st
from utils.data_loader import cargar_datos

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
st.markdown('<h1 class="main-header">🔔 Portal de Leads SPS: Cliengo - Táctica</h1>', unsafe_allow_html=True)

# Información principal
st.markdown("""
<div class="card">
<h2 class="sub-header">Bienvenido al Portal de Leads de SPS</h2>
<p>Esta aplicación permite visualizar y analizar el flujo de leads que ingresan a través de Cliengo 
(Chatbot y WhatsApp) y su integración con el CRM Táctica.</p>

<p>Utilice la barra lateral para navegar entre las diferentes secciones:</p>
<ul>
    <li><b>Página Principal</b>: Resumen general y estadísticas clave</li>
    <li><b>Leads por Horario</b>: Análisis del caudal de leads por franjas horarias</li>
    <li><b>Leads por Servicio</b>: Distribución de leads por categoría y servicio</li>
    <li><b>Detalles</b>: Exploración detallada de los datos</li>
</ul>
</div>
""", unsafe_allow_html=True)

# Cargar datos una sola vez
df = cargar_datos()

# Calcular métricas clave
total_leads = len(df)
leads_asesorados = len(df[df['Estado'] == 'Asesorado'])
leads_pendientes = len(df[df['Estado'] == 'Pendiente'])
leads_descartados = len(df[df['Estado'] == 'Descartado'])

# Mostrar KPIs
st.markdown('<h2 class="sub-header">Resumen de Leads</h2>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Leads", total_leads)

with col2:
    st.metric("Asesorados", leads_asesorados, f"{leads_asesorados/total_leads:.1%}")

with col3:
    st.metric("Pendientes", leads_pendientes, f"{leads_pendientes/total_leads:.1%}")

with col4:
    st.metric("Descartados", leads_descartados, f"{leads_descartados/total_leads:.1%}")

# Información adicional
st.markdown("""
<div class="card">
<h2 class="sub-header">Sobre los datos</h2>
<p>Actualmente los datos se cargan desde un archivo CSV de prueba. En futuras versiones, 
se implementará la conexión directa a la API de Táctica para obtener datos en tiempo real.</p>

<p><b>Nota importante:</b> Los reportes están diseñados según los requerimientos específicos 
de SPS para analizar los leads entre las 17:00 y 21:00 horas y su clasificación por servicios.</p>
</div>
""", unsafe_allow_html=True)

# Pie de página
st.markdown("---")
st.markdown("© 2025 - Portal de Leads SPS | Versión 1.0")