import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from utils.data_loader import cargar_datos, aplicar_filtros

# Configuración de la página
st.set_page_config(
    page_title="Leads por Categoría y Servicio",
    page_icon="📋",
    layout="wide"
)

# Título principal
st.title("📋 Leads por Categoría y Servicio")
st.markdown("Análisis de la distribución de leads por tipo de servicio, categoría y canal de origen")

# Cargar datos
df = cargar_datos()

# Panel de filtros en la barra lateral
st.sidebar.header("Filtros")

# Filtro de fechas
fecha_min = df["FechaIngreso"].min().date()
fecha_max = df["FechaIngreso"].max().date()

fecha_inicio = st.sidebar.date_input(
    "Fecha inicial",
    value=fecha_min,
    min_value=fecha_min,
    max_value=fecha_max
)

fecha_fin = st.sidebar.date_input(
    "Fecha final",
    value=fecha_max,
    min_value=fecha_min,
    max_value=fecha_max
)

# Convertir a datetime para poder filtrar
fecha_inicio_dt = datetime.combine(fecha_inicio, datetime.min.time())
fecha_fin_dt = datetime.combine(fecha_fin, datetime.max.time())

# Filtros adicionales
canales_disponibles = df["CanalOrigen"].unique().tolist()
canales_seleccionados = st.sidebar.multiselect(
    "Canales de Origen",
    options=canales_disponibles,
    default=canales_disponibles
)

estados_disponibles = df["Estado"].unique().tolist()
estados_seleccionados = st.sidebar.multiselect(
    "Estados",
    options=estados_disponibles,
    default=estados_disponibles
)

# Opción para excluir domingos
excluir_domingos = st.sidebar.checkbox("Excluir domingos", value=True)

# Tipo de visualización
tipo_grafico = st.sidebar.radio(
    "Tipo de visualización",
    options=["Gráfico de Sunburst", "Gráfico de Barras", "Gráfico de Líneas Temporales"],
    index=0
)

# Aplicar filtros
df_filtrado = aplicar_filtros(
    df,
    fecha_inicio=fecha_inicio_dt,
    fecha_fin=fecha_fin_dt,
    canales=canales_seleccionados,
    estados=estados_seleccionados
)

# Excluir domingos si está marcada la opción
if excluir_domingos:
    df_filtrado = df_filtrado[df_filtrado["DiaSemana"] != 6]

# Preparar datos según tipo de visualización
if tipo_grafico == "Gráfico de Sunburst":
    # Agrupar datos para el gráfico de sunburst
    leads_categoria = df_filtrado.groupby(["Servicio", "CanalOrigen"]).size().reset_index(name="CantidadLeads")
    
    # Crear gráfico sunburst
    fig = px.sunburst(
        leads_categoria,
        path=["Servicio", "CanalOrigen"],
        values="CantidadLeads",
        title="Distribución de Leads por Servicio y Canal de Origen",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    # Mostrar el gráfico
    st.plotly_chart(fig, use_container_width=True)

elif tipo_grafico == "Gráfico de Barras":
    # Agrupar datos para el gráfico de barras
    leads_categoria = df_filtrado.groupby(["Servicio", "CanalOrigen"]).size().reset_index(name="CantidadLeads")
    
    # Crear gráfico de barras
    fig = px.bar(
        leads_categoria,
        x="Servicio",
        y="CantidadLeads",
        color="CanalOrigen",
        title="Cantidad de Leads por Servicio y Canal de Origen",
        barmode="group"
    )
    
    # Mostrar el gráfico
    st.plotly_chart(fig, use_container_width=True)

else:  # Gráfico de Líneas Temporales
    # Crear columna de fecha sin hora para agrupar por día
    df_filtrado["FechaSinHora"] = df_filtrado["FechaIngreso"].dt.date
    
    # Agrupar por fecha y servicio
    leads_por_dia = df_filtrado.groupby(["FechaSinHora", "Servicio"]).size().reset_index(name="CantidadLeads")
    
    # Crear gráfico de líneas
    fig = px.line(
        leads_por_dia,
        x="FechaSinHora",
        y="CantidadLeads",
        color="Servicio",
        title="Evolución Temporal de Leads por Servicio",
        markers=True
    )
    
    # Personalizar el gráfico
    fig.update_layout(
        xaxis_title="Fecha",
        yaxis_title="Cantidad de Leads",
        legend_title="Servicio"
    )
    
    # Mostrar el gráfico
    st.plotly_chart(fig, use_container_width=True)

# Análisis adicional: Distribución por estado
st.header("Estado de los Leads por Servicio")

# Agrupar por servicio y estado
estado_por_servicio = df_filtrado.groupby(["Servicio", "Estado"]).size().reset_index(name="CantidadLeads")

# Crear gráfico de barras apiladas
fig_estado = px.bar(
    estado_por_servicio,
    x="Servicio",
    y="CantidadLeads",
    color="Estado",
    title="Distribución de Estados por Servicio",
    color_discrete_map={
        "Asesorado": "#00CC96",
        "Pendiente": "#FFA15A",
        "Descartado": "#EF553B"
    }
)

# Mostrar el gráfico
st.plotly_chart(fig_estado, use_container_width=True)

# Tabla resumen
st.header("Tabla Resumen por Servicio")

# Crear tabla resumen
resumen_servicio = df_filtrado.groupby(["Servicio"]).agg(
    Total_Leads=("FechaIngreso", "count"),
    Chatbot=pd.NamedAgg(column="CanalOrigen", aggfunc=lambda x: sum(x == "Chatbot")),
    WhatsApp=pd.NamedAgg(column="CanalOrigen", aggfunc=lambda x: sum(x == "WhatsApp")),
    Asesorados=pd.NamedAgg(column="Estado", aggfunc=lambda x: sum(x == "Asesorado")),
    Pendientes=pd.NamedAgg(column="Estado", aggfunc=lambda x: sum(x == "Pendiente")),
    Descartados=pd.NamedAgg(column="Estado", aggfunc=lambda x: sum(x == "Descartado")),
    Tasa_Efectividad=pd.NamedAgg(column="Estado", aggfunc=lambda x: sum(x == "Asesorado") / len(x) if len(x) > 0 else 0)
).reset_index()

# Formatear columna de tasa de efectividad
resumen_servicio["Tasa_Efectividad"] = resumen_servicio["Tasa_Efectividad"].apply(lambda x: f"{x:.1%}")

# Mostrar tabla
st.dataframe(
    resumen_servicio,
    column_config={
        "Servicio": "Tipo de Servicio",
        "Total_Leads": st.column_config.NumberColumn("Total Leads", format="%d"),
        "Chatbot": st.column_config.NumberColumn("Chatbot", format="%d"),
        "WhatsApp": st.column_config.NumberColumn("WhatsApp", format="%d"),
        "Asesorados": st.column_config.NumberColumn("Asesorados", format="%d"),
        "Pendientes": st.column_config.NumberColumn("Pendientes", format="%d"),
        "Descartados": st.column_config.NumberColumn("Descartados", format="%d"),
        "Tasa_Efectividad": "Tasa de Efectividad"
    },
    use_container_width=True,
    hide_index=True
)

# Sección de información adicional
with st.expander("ℹ️ Información sobre este reporte"):
    st.markdown("""
    ### Acerca del reporte de leads por categoría y servicio
    
    Este reporte está diseñado para visualizar la distribución de leads según el tipo de servicio solicitado 
    y el canal de origen, permitiendo entender mejor el perfil de los leads que ingresan al sistema.
    
    #### Métricas clave:
    - **Distribución por servicio:** Cantidad de leads por cada tipo de servicio ofrecido.
    - **Distribución por canal:** Diferenciación entre leads que ingresan por Chatbot y WhatsApp.
    - **Estado de los leads:** Clasificación según su estado actual (Asesorado, Pendiente, Descartado).
    - **Tasa de efectividad:** Porcentaje de leads asesorados sobre el total por cada servicio.
    
    #### Notas:
    - Es posible filtrar por fechas, canales y estados para un análisis más detallado.
    - Se puede visualizar la evolución temporal de los leads para identificar tendencias.
    """)

# Pie de página
st.markdown("---")