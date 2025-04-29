import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración básica de la página
st.set_page_config(
    page_title="Portal Cliengo-Táctica",
    page_icon="📊",
    layout="wide"
)

# Título de la app
st.title("📊 Portal de Leads: Cliengo - Táctica")

# Cargar datos
@st.cache_data
def cargar_datos():
    return pd.read_csv("leads.csv", parse_dates=["FechaIngreso"])

df = cargar_datos()

# Convertir columnas de fechas
if "FechaIngreso" in df.columns:
    df["FechaIngreso"] = pd.to_datetime(df["FechaIngreso"], errors="coerce")
else:
    st.error("El archivo no contiene una columna llamada 'FechaIngreso'.")
    st.stop()

# Mapeo de días a español
dias_es = {
    "Monday": "Lunes",
    "Tuesday": "Martes",
    "Wednesday": "Miércoles",
    "Thursday": "Jueves",
    "Friday": "Viernes",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
}

# ---- Sidebar para filtros ----
st.sidebar.header("Filtrar Datos")

# Selección de fecha de inicio y fin
fecha_inicio = st.sidebar.date_input("Seleccionar fecha de inicio", df["FechaIngreso"].min())
fecha_fin = st.sidebar.date_input("Seleccionar fecha de fin", df["FechaIngreso"].max())

# Filtrar datos por las fechas seleccionadas
df_filtrado = df[(df["FechaIngreso"] >= pd.to_datetime(fecha_inicio)) & (df["FechaIngreso"] <= pd.to_datetime(fecha_fin))]

# Extraer hora de la columna 'FechaIngreso'
df_filtrado["HoraIngreso"] = df_filtrado["FechaIngreso"].dt.hour

# ---- Opción de visualización (Pantallazo Semanal, Semana Detallada, Detalle Diario) ----
opcion = st.sidebar.radio("Seleccionar vista:", ("Pantallazo Semanal", "Semana Detallada", "Detalle Diario"))

# ---- Pantallazo Semanal ----
if opcion == "Pantallazo Semanal":
    st.header("📅 Pantallazo Semanal")
    
    # Agregar columna con el día de la semana en español
    df_filtrado["DiaSemana"] = df_filtrado["FechaIngreso"].dt.day_name().map(dias_es)

    # Agrupar datos por día de la semana y hora
    df_semanal = df_filtrado.groupby(["DiaSemana", "HoraIngreso"]).size().reset_index(name="CantidadLeads")

    # Ordenar por día de la semana
    dias_orden = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    df_semanal["DiaSemana"] = pd.Categorical(df_semanal["DiaSemana"], categories=dias_orden, ordered=True)
    df_semanal = df_semanal.sort_values("DiaSemana")

    # Crear gráfico semanal
    fig_semanal = px.bar(df_semanal, x="DiaSemana", y="CantidadLeads", color="HoraIngreso",
                        labels={"DiaSemana": "Día de la Semana", "CantidadLeads": "Cantidad de Leads", "HoraIngreso": "Hora"},
                        title="Cantidad de Leads por Día y Hora",
                        color_continuous_scale="Viridis")

    # Mostrar gráfico
    st.plotly_chart(fig_semanal, use_container_width=True)

# ---- Semana Detallada ----
elif opcion == "Semana Detallada":
    st.header("📊 Semana Detallada (por Día y Horario)")

    # Agrupar por día de la semana y hora
    df_semana_detallada = df_filtrado.groupby([df_filtrado["FechaIngreso"].dt.date, "HoraIngreso"]).size().reset_index(name="CantidadLeads")

    # Crear gráfico detallado por día y hora
    fig_semana_detallada = px.bar(df_semana_detallada, x="FechaIngreso", y="CantidadLeads", color="HoraIngreso",
                                labels={"FechaIngreso": "Fecha", "CantidadLeads": "Cantidad de Leads", "HoraIngreso": "Hora"},
                                title="Leads Detallados por Día y Hora",
                                color_continuous_scale="Cividis")

    # Mostrar gráfico
    st.plotly_chart(fig_semana_detallada, use_container_width=True)

# ---- Detalle Diario ----
else:
    st.header("📅 Detalle Diario")

    # Crear gráfico para detalle diario
    df_diario = df_filtrado.groupby([df_filtrado["FechaIngreso"].dt.date, "HoraIngreso"]).size().reset_index(name="CantidadLeads")
    fig_diario = px.bar(df_diario, x="FechaIngreso", y="CantidadLeads", color="HoraIngreso",
                        labels={"FechaIngreso": "Fecha", "CantidadLeads": "Cantidad de Leads", "HoraIngreso": "Hora"},
                        title="Leads por Día y Hora",
                        color_continuous_scale="Blues")

    # Mostrar gráfico
    st.plotly_chart(fig_diario, use_container_width=True)

# ---- Footer ----
st.markdown("---")
