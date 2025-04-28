import pandas as pd
import streamlit as st

@st.cache_data
def cargar_datos():
    """
    Carga los datos desde leads.csv y parsea la columna de fecha.
    """
    return pd.read_csv('leads.csv', parse_dates=['fecha_ingreso'])
