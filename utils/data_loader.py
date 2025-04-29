import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

# Función para cargar y procesar los datos iniciales
@st.cache_data
def cargar_datos():
    """
    Carga los datos desde el archivo CSV y realiza transformaciones básicas.
    
    Returns:
        DataFrame: Datos de leads procesados con columnas adicionales
    """
    # Cargar datos desde CSV
    df = pd.read_csv("leads.csv", parse_dates=["FechaIngreso"])
    
    # Crear columnas derivadas útiles para análisis
    df["HoraIngreso"] = df["FechaIngreso"].dt.hour
    df["MinutoIngreso"] = df["FechaIngreso"].dt.minute
    df["Bloque30min"] = df["HoraIngreso"].astype(str) + ":" + ((df["MinutoIngreso"] // 30) * 30).astype(str).str.zfill(2)
    
    # Extraer información de día de la semana (0=Lunes, 6=Domingo)
    df["DiaSemana"] = df["FechaIngreso"].dt.dayofweek
    df["NombreDiaSemana"] = df["FechaIngreso"].dt.day_name(locale='es_ES')
    
    # Crear una versión corta del nombre del día (L, M, X, J, V, S, D)
    dias_mapping = {0: 'L', 1: 'M', 2: 'X', 3: 'J', 4: 'V', 5: 'S', 6: 'D'}
    df["DiaCodigo"] = df["DiaSemana"].map(dias_mapping)
    
    # Calcular semana del año
    df["Semana"] = df["FechaIngreso"].dt.isocalendar().week
    
    # Filtrar los domingos si es necesario (según requisito)
    # df = df[df["DiaSemana"] != 6]  # Descomentar para eliminar los domingos
    
    # Limpiar y normalizar datos
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