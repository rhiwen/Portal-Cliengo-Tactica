# 🔔 Portal SPS: Cliengo-Táctica

Este proyecto es una aplicación desarrollada con Streamlit y Plotly para visualizar y analizar el flujo de leads de SPS (empresa de alarmas) que ingresan a través de Cliengo (Chatbot y WhatsApp) y su integración con Táctica CRM.

## 🚀 Objetivos

El portal permite:

- 📈 Visualizar el caudal de leads por franjas horarias, con enfoque en 17:00-21:00 hs.
- 📊 Analizar leads por día de la semana (L-S, excluyendo domingos)
- 📋 Explorar la distribución por tipo de servicio de alarma y canal de origen
- 🔍 Realizar análisis detallados con filtros avanzados

## 🛠️ Tecnologías Utilizadas

- **Python 3.10+**
- **Streamlit 1.44+**: Framework para crear aplicaciones web interactivas
- **Plotly 6.0+**: Biblioteca para visualizaciones interactivas
- **Pandas 2.2+**: Procesamiento y análisis de datos

## 📂 Estructura del Proyecto

```
/Portal-Cliengo-Tactica/
│
├── app.py                  # Aplicación principal (punto de entrada)
├── pages/                  # Carpeta para páginas adicionales
│   ├── 1_Leads_Horario.py  # Página de análisis por horario
│   ├── 2_Leads_Servicio.py # Página de análisis por servicio/categoría
│   └── 3_Detalles.py       # Página para ver datos detallados
├── utils/                  # Utilidades compartidas
│   └── data_loader.py      # Funciones para cargar y procesar datos
├── leads.csv               # Datos de prueba
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Documentación del proyecto
```

## 🧪 Instalación

1. **Clonar el repositorio:**

```bash
git clone https://github.com/rhiwen/Portal-Cliengo-Tactica.git
cd Portal-Cliengo-Tactica
```

2. **Crear y activar el entorno virtual:**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/Scripts/activate
```

3. **Instalar dependencias:**

```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación:**

```bash
streamlit run app.py
```

## 📈 Funcionalidades

### Página Principal
- Resumen general y métricas clave
- Dashboard con KPIs principales

### Leads por Horario
- Visualización de leads por hora, con enfoque en 17:00-21:00
- Análisis por día de la semana (L-S)
- Heatmap de distribución día-hora

### Leads por Servicio
- Distribución por tipo de servicio de alarma
- Análisis por canal de origen (Chatbot/WhatsApp)
- Evolución temporal por servicio

### Exploración Detallada
- Filtros avanzados por múltiples criterios
- Búsqueda por texto en campos relevantes
- Exportación de datos filtrados
- Análisis de efectividad por servicio y canal

## 🔮 Próximas Mejoras

- Conexión directa a la API de Táctica para datos en tiempo real
- Nuevas visualizaciones para análisis de efectividad comercial
- Filtros más avanzados para segmentación de leads
- Paneles personalizados para diferentes roles de usuario
- Alertas automatizadas para caudales de leads fuera de rango

## 📝 Notas

- Este proyecto está en desarrollo activo.
- Actualmente los datos se cargan desde un CSV de prueba.
- En futuras versiones se implementará la conexión a la API de Táctica.
- El portal está optimizado para las necesidades específicas de SPS como empresa de alarmas.