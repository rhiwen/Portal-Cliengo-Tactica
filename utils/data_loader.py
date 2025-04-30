import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

# Función para cargar y procesar los datos iniciales (ahora sin usar locale)
@st.cache_data
def cargar_datos():
    df = pd.read_csv("leads.csv", parse_dates=["FechaIngreso"])
    
    df["HoraIngreso"] = df["FechaIngreso"].dt.hour
    df["MinutoIngreso"] = df["FechaIngreso"].dt.minute
    df["Bloque30min"] = df["HoraIngreso"].astype(str) + ":" + ((df["MinutoIngreso"] // 30) * 30).astype(str).str.zfill(2)
    
    df["DiaSemana"] = df["FechaIngreso"].dt.dayofweek
    
    # Mapeo manual de los días de la semana
    dias_semana_mapping = {
        0: 'Lunes',
        1: 'Martes',
        2: 'Miércoles',
        3: 'Jueves',
        4: 'Viernes',
        5: 'Sábado',
        6: 'Domingo'
    }
    df["NombreDiaSemana"] = df["DiaSemana"].map(dias_semana_mapping)
    
    dias_mapping = {0: 'L', 1: 'M', 2: 'X', 3: 'J', 4: 'V', 5: 'S', 6: 'D'}
    df["DiaCodigo"] = df["DiaSemana"].map(dias_mapping)
    
    df["Semana"] = df["FechaIngreso"].dt.isocalendar().week
    
    for columna in ['Servicio', 'CanalOrigen', 'Estado', 'TipoDeCliente', 'Clasificacion']:
        if columna in df.columns:
            df[columna] = df[columna].fillna('No especificado')
    
    return df

# Función para generar rangos de fechas
def generar_rango_fechas(dias=30):
    """
    Genera un rango de fechas para filtrar datos.
    
    Args:
        dias (int): Número de días hacia atrás desde hoy
        
    Returns:
        tuple: Fecha inicial y fecha final para filtros
    """
    fecha_final = datetime.now()
    fecha_inicial = fecha_final - timedelta(days=dias)
    return fecha_inicial, fecha_final

# Función para aplicar filtros comunes a los dataframes
def aplicar_filtros(df, fecha_inicio=None, fecha_fin=None, servicios=None, canales=None, estados=None):
    """
    Aplica filtros comunes al DataFrame de leads.
    
    Args:
        df (DataFrame): DataFrame de leads
        fecha_inicio (datetime): Fecha de inicio para filtrar
        fecha_fin (datetime): Fecha final para filtrar
        servicios (list): Lista de servicios para filtrar
        canales (list): Lista de canales para filtrar
        estados (list): Lista de estados para filtrar
        
    Returns:
        DataFrame: DataFrame filtrado
    """
    # Copia para no modificar el original
    df_filtrado = df.copy()
    
    # Aplicar filtros de fecha
    if fecha_inicio and fecha_fin:
        df_filtrado = df_filtrado[(df_filtrado["FechaIngreso"] >= fecha_inicio) & 
                                (df_filtrado["FechaIngreso"] <= fecha_fin)]
    
    # Aplicar filtros de servicio
    if servicios and len(servicios) > 0:
        df_filtrado = df_filtrado[df_filtrado["Servicio"].isin(servicios)]
    
    # Aplicar filtros de canal
    if canales and len(canales) > 0:
        df_filtrado = df_filtrado[df_filtrado["CanalOrigen"].isin(canales)]
    
    # Aplicar filtros de estado
    if estados and len(estados) > 0:
        df_filtrado = df_filtrado[df_filtrado["Estado"].isin(estados)]
    
    return df_filtrado