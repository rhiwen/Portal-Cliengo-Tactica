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

# Mostrar datos
with st.expander("🔍 Ver datos crudos"):
    st.dataframe(df)

# ---- Reporte 1: Caudal de leads entre 17:00 y 21:00 hs ----
st.header("📈 Caudal de Leads por Horario")

# Crear nueva columna de hora
df["HoraIngreso"] = df["FechaIngreso"].dt.hour

# Filtrar leads entre 17 y 21 hs
df_franja = df[(df["HoraIngreso"] >= 17) & (df["HoraIngreso"] <= 21)]

# Agrupar por hora
leads_por_hora = df.groupby("HoraIngreso").size().reset_index(name="CantidadLeads")
leads_franja = df_franja.groupby("HoraIngreso").size().reset_index(name="CantidadLeads")

# Gráfico general de leads por hora
fig_general = px.bar(leads_por_hora, x="HoraIngreso", y="CantidadLeads",
                    labels={"HoraIngreso": "Hora del día", "CantidadLeads": "Cantidad de Leads"},
                    title="Cantidad de Leads por Hora (Todo el día)",
                    color_discrete_sequence=["#636EFA"])

# Gráfico filtrado para 17-21 hs
fig_franja = px.bar(leads_franja, x="HoraIngreso", y="CantidadLeads",
                    labels={"HoraIngreso": "Hora (17 a 21)", "CantidadLeads": "Cantidad de Leads"},
                    title="Cantidad de Leads entre 17:00 y 21:00",
                    color_discrete_sequence=["#EF553B"])

# Mostrar gráficos
col1, col2 = st.columns(2)
col1.plotly_chart(fig_general, use_container_width=True)
col2.plotly_chart(fig_franja, use_container_width=True)

# ---- Reporte 2: Leads por Categoría y Servicio ----
st.header("📋 Leads por Categoría y Servicio")

# Agrupar
leads_categoria = df.groupby(["FechaIngreso", "Servicio", "CanalOrigen"]).size().reset_index(name="CantidadLeads")

# Gráfico
fig_categoria = px.sunburst(
    leads_categoria,
    path=["Servicio", "CanalOrigen"],
    values="CantidadLeads",
    title="Distribución de Leads por Servicio y Canal de Origen",
    color_discrete_sequence=px.colors.qualitative.Pastel
)

st.plotly_chart(fig_categoria, use_container_width=True)

# ---- Footer ----
st.markdown("---")

