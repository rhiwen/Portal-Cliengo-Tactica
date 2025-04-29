import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.data_loader import cargar_datos, aplicar_filtros

# Configuración de la página
st.set_page_config(
    page_title="Caudal de Leads por Horario",
    page_icon="📈",
    layout="wide"
)

# Título principal
st.title("📈 Caudal de Leads por Horario")
st.markdown("Análisis del volumen de leads recibidos por franja horaria, con enfoque en la franja de 17:00 a 21:00 horas")

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
servicios_disponibles = df["Servicio"].unique().tolist()
servicios_seleccionados = st.sidebar.multiselect(
    "Servicios",
    options=servicios_disponibles,
    default=servicios_disponibles
)

canales_disponibles = df["CanalOrigen"].unique().tolist()
canales_seleccionados = st.sidebar.multiselect(
    "Canales de Origen",
    options=canales_disponibles,
    default=canales_disponibles
)

# Opción para excluir domingos
excluir_domingos = st.sidebar.checkbox("Excluir domingos", value=True)

# Tipo de visualización temporal
vista_temporal = st.sidebar.radio(
    "Vista temporal",
    options=["Horas", "Bloques de 30 minutos"],
    index=0
)

# Aplicar filtros
df_filtrado = aplicar_filtros(
    df,
    fecha_inicio=fecha_inicio_dt,
    fecha_fin=fecha_fin_dt,
    servicios=servicios_seleccionados,
    canales=canales_seleccionados
)

# Excluir domingos si está marcada la opción
if excluir_domingos:
    df_filtrado = df_filtrado[df_filtrado["DiaSemana"] != 6]

# Preparar datos según la vista temporal seleccionada
if vista_temporal == "Horas":
    # Agrupación por hora
    leads_por_hora = df_filtrado.groupby("HoraIngreso").size().reset_index(name="CantidadLeads")
    eje_x = "HoraIngreso"
    etiqueta_x = "Hora del día"
    titulo_grafico = "Cantidad de Leads por Hora (Todo el día)"
else:
    # Agrupación por bloques de 30 minutos
    leads_por_hora = df_filtrado.groupby("Bloque30min").size().reset_index(name="CantidadLeads")
    eje_x = "Bloque30min"
    etiqueta_x = "Bloque de 30 minutos"
    titulo_grafico = "Cantidad de Leads por Bloques de 30 minutos"

# Gráfico general de leads por hora/bloque
fig_general = px.bar(
    leads_por_hora,
    x=eje_x,
    y="CantidadLeads",
    labels={eje_x: etiqueta_x, "CantidadLeads": "Cantidad de Leads"},
    title=titulo_grafico,
    color_discrete_sequence=["#636EFA"]
)

# Filtrar para franja horaria especial (17:00 - 21:00)
if vista_temporal == "Horas":
    df_franja = df_filtrado[(df_filtrado["HoraIngreso"] >= 17) & (df_filtrado["HoraIngreso"] <= 21)]
    leads_franja = df_franja.groupby("HoraIngreso").size().reset_index(name="CantidadLeads")
    titulo_franja = "Cantidad de Leads entre 17:00 y 21:00"
else:
    # Para bloques de 30 min, filtramos los que están entre 17:00 y 21:30
    df_franja = df_filtrado[
        (df_filtrado["HoraIngreso"] >= 17) & 
        ((df_filtrado["HoraIngreso"] < 21) | 
        ((df_filtrado["HoraIngreso"] == 21) & (df_filtrado["MinutoIngreso"] < 30)))
    ]
    leads_franja = df_franja.groupby("Bloque30min").size().reset_index(name="CantidadLeads")
    titulo_franja = "Cantidad de Leads entre 17:00 y 21:30 (bloques de 30 min)"

# Gráfico para la franja especial
fig_franja = px.bar(
    leads_franja,
    x=eje_x,
    y="CantidadLeads",
    labels={eje_x: f"{etiqueta_x} (17:00 - 21:00)", "CantidadLeads": "Cantidad de Leads"},
    title=titulo_franja,
    color_discrete_sequence=["#EF553B"]
)

# Mostrar gráficos en dos columnas
col1, col2 = st.columns(2)
col1.plotly_chart(fig_general, use_container_width=True)
col2.plotly_chart(fig_franja, use_container_width=True)

# Análisis por día de la semana
st.header("📅 Análisis por Día de la Semana")

# Agrupar por día de la semana
leads_por_dia = df_filtrado.groupby("DiaCodigo").size().reset_index(name="CantidadLeads")

# Ordenar los días de la semana correctamente (L, M, X, J, V, S, D)
orden_dias = ['L', 'M', 'X', 'J', 'V', 'S', 'D']
leads_por_dia["DiaCodigo"] = pd.Categorical(leads_por_dia["DiaCodigo"], categories=orden_dias, ordered=True)
leads_por_dia = leads_por_dia.sort_values("DiaCodigo")

# Gráfico de leads por día de la semana
fig_dias = px.bar(
    leads_por_dia,
    x="DiaCodigo",
    y="CantidadLeads",
    labels={"DiaCodigo": "Día de la semana", "CantidadLeads": "Cantidad de Leads"},
    title="Cantidad de Leads por Día de la Semana",
    color_discrete_sequence=["#00CC96"]
)

# Heatmap de leads por día y hora
# Crear tabla pivote para el heatmap
if vista_temporal == "Horas":
    heatmap_data = pd.pivot_table(
        df_filtrado,
        values="FechaIngreso",
        index="DiaCodigo",
        columns="HoraIngreso",
        aggfunc="count",
        fill_value=0
    )
    
    # Ordenar los días de la semana correctamente
    heatmap_data = heatmap_data.reindex(orden_dias)
    
    # Crear heatmap
    fig_heatmap = px.imshow(
        heatmap_data,
        labels=dict(x="Hora del día", y="Día de la semana", color="Cantidad de Leads"),
        x=heatmap_data.columns,
        y=heatmap_data.index,
        title="Distribución de Leads por Día y Hora",
        color_continuous_scale="YlOrRd"
    )
    
    # Añadir números a las celdas
    for i in range(len(heatmap_data.index)):
        for j in range(len(heatmap_data.columns)):
            if heatmap_data.iloc[i, j] > 0:
                fig_heatmap.add_annotation(
                    x=j,
                    y=i,
                    text=str(int(heatmap_data.iloc[i, j])),
                    showarrow=False,
                    font=dict(color="black")
                )

# Mostrar gráficos en dos columnas
col1, col2 = st.columns(2)
col1.plotly_chart(fig_dias, use_container_width=True)

if vista_temporal == "Horas":
    col2.plotly_chart(fig_heatmap, use_container_width=True)

# Sección de información adicional
with st.expander("ℹ️ Información sobre este reporte"):
    st.markdown("""
    ### Acerca del reporte de caudal de leads
    
    Este reporte está diseñado para visualizar el volumen de leads recibidos en diferentes franjas horarias, 
    con un enfoque especial en la franja de 17:00 a 21:00 horas, que es el período de mayor actividad.
    
    #### Métricas clave:
    - **Cantidad total de leads:** Número total de leads recibidos en el período seleccionado.
    - **Distribución por hora/bloque:** Visualización del volumen de leads en cada hora o bloque de 30 minutos.
    - **Análisis por día de la semana:** Distribución de leads según el día de la semana (L-D).
    
    #### Notas:
    - Los domingos pueden ser excluidos del análisis según se requiera.
    - La franja horaria de 17:00 a 21:00 es analizada en detalle según los requerimientos específicos.
    """)

# Pie de página
st.markdown("---")
st.markdown("© 2025 - Portal de Leads SPS | Versión 1.0")