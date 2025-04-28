import streamlit as st
import pandas as pd

def filtrar_datos(data, canales, servicios, categorias, estados, fecha_inicio, fecha_fin):
    # Convierte las fechas seleccionadas a formato Timestamp para comparar bien
    fecha_inicio = pd.to_datetime(fecha_inicio)
    fecha_fin = pd.to_datetime(fecha_fin)
    
    df = data.copy()
    if canales:
        df = df[df['canal'].isin(canales)]
    if servicios:
        df = df[df['servicio'].isin(servicios)]
    if categorias:
        df = df[df['categoria'].isin(categorias)]
    if estados:
        df = df[df['estado_lead'].isin(estados)]
    if fecha_inicio and fecha_fin:
        df = df[(df['fecha_ingreso'] >= fecha_inicio) & (df['fecha_ingreso'] <= fecha_fin)]
    return df

def mostrar_filtros(data):
    st.sidebar.title("Filtros")
    canales = st.sidebar.multiselect("Filtrar por Canal", options=data['canal'].unique())
    servicios = st.sidebar.multiselect("Filtrar por Servicio", options=data['servicio'].unique())
    categorias = st.sidebar.multiselect("Filtrar por Categoría", options=data['categoria'].unique())
    estados = st.sidebar.multiselect("Filtrar por Estado del Lead", options=data['estado_lead'].unique())
    fecha_inicio, fecha_fin = st.sidebar.date_input(
        "Rango de Fecha de Ingreso",
        value=[data['fecha_ingreso'].min(), data['fecha_ingreso'].max()],
        min_value=data['fecha_ingreso'].min(),
        max_value=data['fecha_ingreso'].max()
    )
    return canales, servicios, categorias, estados, fecha_inicio, fecha_fin
