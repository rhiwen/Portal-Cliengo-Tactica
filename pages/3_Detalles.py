import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from utils.data_loader import cargar_datos, aplicar_filtros

# Configuración de la página
st.set_page_config(
    page_title="Información detallada de Leads",
    page_icon="🔍",
    layout="wide"
)

# Título principal
st.title("🔍 Información detallada de Leads")
st.markdown("Visualización con opciones avanzadas de filtrado y análisis")

# Cargar datos
df = cargar_datos()

# Panel de filtros en la barra lateral
st.sidebar.header("Filtros Avanzados")

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

# Filtros específicos por columna
col1_sidebar, col2_sidebar = st.sidebar.columns(2)

with col1_sidebar:
    servicios_disponibles = df["Servicio"].unique().tolist()
    servicios_seleccionados = st.multiselect(
        "Servicios",
        options=servicios_disponibles,
        default=servicios_disponibles
    )

    estados_disponibles = df["Estado"].unique().tolist()
    estados_seleccionados = st.multiselect(
        "Estados",
        options=estados_disponibles,
        default=estados_disponibles
    )

with col2_sidebar:
    canales_disponibles = df["CanalOrigen"].unique().tolist()
    canales_seleccionados = st.multiselect(
        "Canales",
        options=canales_disponibles,
        default=canales_disponibles
    )
    
    tipos_cliente_disponibles = df["TipoDeCliente"].unique().tolist()
    tipos_cliente_seleccionados = st.multiselect(
        "Tipo de Cliente",
        options=tipos_cliente_disponibles,
        default=tipos_cliente_disponibles
    )

# Filtro de texto para búsqueda
texto_busqueda = st.sidebar.text_input("Búsqueda por texto (nombre, email, notas)", "")

# Aplicar filtros
df_filtrado = aplicar_filtros(
    df,
    fecha_inicio=fecha_inicio_dt,
    fecha_fin=fecha_fin_dt,
    servicios=servicios_seleccionados,
    canales=canales_seleccionados,
    estados=estados_seleccionados
)

# Filtrar por tipo de cliente
if tipos_cliente_seleccionados and len(tipos_cliente_seleccionados) > 0:
    df_filtrado = df_filtrado[df_filtrado["TipoDeCliente"].isin(tipos_cliente_seleccionados)]

# Filtrar por texto de búsqueda
if texto_busqueda:
    texto_busqueda = texto_busqueda.lower()
    df_filtrado = df_filtrado[
        df_filtrado["Nombre"].str.lower().str.contains(texto_busqueda) |
        df_filtrado["Email"].str.lower().str.contains(texto_busqueda) |
        df_filtrado["Notas"].str.lower().str.contains(texto_busqueda)
    ]

# Opciones de visualización
st.sidebar.header("Opciones de Visualización")
mostrar_raw_data = st.sidebar.checkbox("Mostrar datos crudos", value=True)
ordenar_por = st.sidebar.selectbox(
    "Ordenar por",
    options=["FechaIngreso", "Servicio", "CanalOrigen", "Estado"],
    index=0
)
orden_ascendente = st.sidebar.checkbox("Orden ascendente", value=False)

# Ordenar datos
df_filtrado = df_filtrado.sort_values(by=ordenar_por, ascending=orden_ascendente)

# Opciones de análisis
st.header("Opciones de Análisis")
tipo_analisis = st.radio(
    "Seleccione tipo de análisis:",
    options=["Métricas Generales", "Análisis por Tipo de Cliente", "Análisis de Efectividad"],
    horizontal=True
)

# Mostrar diferentes análisis según la selección
if tipo_analisis == "Métricas Generales":
    # Crear columnas para métricas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Leads", len(df_filtrado))
    
    with col2:
        leads_chatbot = len(df_filtrado[df_filtrado["CanalOrigen"] == "Chatbot"])
        porcentaje_chatbot = leads_chatbot / len(df_filtrado) if len(df_filtrado) > 0 else 0
        st.metric("Leads por Chatbot", leads_chatbot, f"{porcentaje_chatbot:.1%}")
        
    with col3:
        leads_whatsapp = len(df_filtrado[df_filtrado["CanalOrigen"] == "WhatsApp"])
        porcentaje_whatsapp = leads_whatsapp / len(df_filtrado) if len(df_filtrado) > 0 else 0
        st.metric("Leads por WhatsApp", leads_whatsapp, f"{porcentaje_whatsapp:.1%}")
    
    with col4:
        leads_asesorados = len(df_filtrado[df_filtrado["Estado"] == "Asesorado"])
        tasa_efectividad = leads_asesorados / len(df_filtrado) if len(df_filtrado) > 0 else 0
        st.metric("Tasa de Efectividad", f"{tasa_efectividad:.1%}")
    
    # Gráfico de tendencia diaria
    st.subheader("Tendencia Diaria de Leads")
    
    # Crear columna de fecha sin hora
    df_filtrado["FechaSinHora"] = df_filtrado["FechaIngreso"].dt.date
    
    # Agrupar por fecha
    leads_por_dia = df_filtrado.groupby("FechaSinHora").size().reset_index(name="CantidadLeads")
    
    # Crear gráfico de líneas
    fig = px.line(
        leads_por_dia,
        x="FechaSinHora",
        y="CantidadLeads",
        title="Evolución de Leads por Día",
        markers=True
    )
    
    # Mostrar gráfico
    st.plotly_chart(fig, use_container_width=True)

elif tipo_analisis == "Análisis por Tipo de Cliente":
    # Análisis por tipo de cliente
    tipo_cliente_counts = df_filtrado["TipoDeCliente"].value_counts().reset_index()
    tipo_cliente_counts.columns = ["TipoDeCliente", "Cantidad"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribución por Tipo de Cliente")
        fig_pie = px.pie(
            tipo_cliente_counts,
            values="Cantidad",
            names="TipoDeCliente",
            title="Distribución por Tipo de Cliente",
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.subheader("Estado por Tipo de Cliente")
        estado_tipo_cliente = df_filtrado.groupby(["TipoDeCliente", "Estado"]).size().reset_index(name="Cantidad")
        
        fig_bar = px.bar(
            estado_tipo_cliente,
            x="TipoDeCliente",
            y="Cantidad",
            color="Estado",
            title="Estado de Leads por Tipo de Cliente",
            barmode="group",
            color_discrete_map={
                "Asesorado": "#00CC96",
                "Pendiente": "#FFA15A",
                "Descartado": "#EF553B"
            }
        )
        st.plotly_chart(fig_bar, use_container_width=True)

else:  # Análisis de Efectividad
    st.subheader("Análisis de Efectividad por Servicio y Canal")
    
    # Calcular métricas de efectividad
    efectividad = df_filtrado.groupby(["Servicio", "CanalOrigen"]).agg(
        Total=("FechaIngreso", "count"),
        Asesorados=pd.NamedAgg(column="Estado", aggfunc=lambda x: sum(x == "Asesorado")),
        Pendientes=pd.NamedAgg(column="Estado", aggfunc=lambda x: sum(x == "Pendiente")),
        Descartados=pd.NamedAgg(column="Estado", aggfunc=lambda x: sum(x == "Descartado"))
    ).reset_index()
    
    # Calcular tasa de efectividad
    efectividad["TasaEfectividad"] = efectividad["Asesorados"] / efectividad["Total"]
    
    # Crear gráfico de barras para tasa de efectividad
    fig_efectividad = px.bar(
        efectividad,
        x="Servicio",
        y="TasaEfectividad",
        color="CanalOrigen",
        title="Tasa de Efectividad por Servicio y Canal",
        barmode="group",
        text_auto=".1%"
    )
    
    # Configurar formato de porcentaje
    fig_efectividad.update_layout(yaxis_tickformat=".1%")
    
    # Mostrar gráfico
    st.plotly_chart(fig_efectividad, use_container_width=True)
    
    # Mostrar tabla de efectividad
    st.subheader("Tabla de Efectividad")
    
    # Formatear columna de tasa de efectividad para la tabla
    efectividad["TasaEfectividad"] = efectividad["TasaEfectividad"].apply(lambda x: f"{x:.1%}")
    
    # Mostrar tabla
    st.dataframe(
        efectividad,
        column_config={
            "Servicio": "Tipo de Servicio",
            "CanalOrigen": "Canal de Origen",
            "Total": st.column_config.NumberColumn("Total Leads", format="%d"),
            "Asesorados": st.column_config.NumberColumn("Asesorados", format="%d"),
            "Pendientes": st.column_config.NumberColumn("Pendientes", format="%d"),
            "Descartados": st.column_config.NumberColumn("Descartados", format="%d"),
            "TasaEfectividad": "Tasa de Efectividad"
        },
        use_container_width=True,
        hide_index=True
    )

# Mostrar datos crudos si está habilitado
if mostrar_raw_data:
    st.header("Datos Detallados")
    
    # Configuración de columnas para visualización
    columnas_a_mostrar = [
        "FechaIngreso", "Nombre", "Telefono", "Email", 
        "Servicio", "CanalOrigen", "Estado", "TipoDeCliente", "Clasificacion", "Notas"
    ]
    
    # Mostrar datos en formato de tabla con configuración personalizada
    st.dataframe(
        df_filtrado[columnas_a_mostrar],
        column_config={
            "FechaIngreso": st.column_config.DatetimeColumn("Fecha y Hora", format="DD/MM/YYYY HH:mm"),
            "Nombre": "Nombre",
            "Telefono": "Teléfono",
            "Email": "Correo Electrónico",
            "Servicio": "Tipo de Servicio",
            "CanalOrigen": "Canal de Origen",
            "Estado": "Estado",
            "TipoDeCliente": "Tipo de Cliente",
            "Clasificacion": "Clasificación",
            "Notas": st.column_config.TextColumn("Notas", width="large")
        },
        hide_index=True,
        use_container_width=True
    )

    # Exportar datos
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Descargar datos como CSV",
        data=csv,
        file_name=f"leads_sps_{fecha_inicio}_al_{fecha_fin}.csv",
        mime="text/csv",
    )

# Sección de información adicional
with st.expander("ℹ️ Información sobre esta página"):
    st.markdown("""
    ### Acerca de la exploración detallada de leads
    
    Esta página permite realizar un análisis más profundo con opciones avanzadas 
    de filtrado y diferentes tipos de visualizaciones para obtener insights específicos.
    
    #### Funcionalidades principales:
    - **Filtros avanzados:** Permite filtrar por fechas, servicios, canales, estados y tipos de cliente.
    - **Búsqueda por texto:** Facilita la localización de leads específicos por nombre, email o contenido de notas.
    - **Tipos de análisis:** Ofrece diferentes vistas analíticas (métricas generales, análisis por tipo de cliente, análisis de efectividad).
    - **Exportación de datos:** Permite descargar los datos filtrados en formato CSV para análisis externos.
    
    #### Notas:
    - Esta página está diseñada para usuarios avanzados que necesitan un análisis más detallado de los datos.
    - En futuras versiones, se implementará la conexión directa a la API de Tactica para obtener datos en tiempo real.
    """)

# Pie de página
st.markdown("---")