## 📊 Portal Cliengo-Táctica

Este proyecto es un prototipo rápido desarrollado con Streamlit y Plotly, cuyo objetivo es visualizar y analizar el flujo de leads que ingresan a través de Cliengo y su integración con Táctica CRM.

# 🚀 Objetivo

    Relevar y presentar información clave del proceso comercial:

        📈 Volumen de leads por horario.

        📋 Leads por categoría y tipo de servicio.

# 🛠️ Tecnologías Utilizadas

    Python 3.10+

    Streamlit

    Plotly

    Pandas

# 📂 Estructura del Proyecto

/Portal-Cliengo-Tactica/
│
├── app.py               # Aplicación principal de Streamlit
├── leads.csv            # Archivo de datos de prueba
├── requirements.txt     # Dependencias del proyecto
├── .gitignore           # Exclusiones para Git
├── README.md            # Documentación del proyecto
└── /venv/               # Entorno virtual (excluido de Git)

# 🧪 Instalación

    Clonar el repositorio:

git clone https://github.com/rhiwen/Portal-Cliengo-Tactica.git
cd Portal-Cliengo-Tactica

    Crear y activar el entorno virtual:

python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

    Instalar dependencias:

pip install -r requirements.txt

    Ejecutar la aplicación:

streamlit run app.py

# 📈 Funcionalidades

    Reporte de caudal de leads: visualización de cantidad de leads ingresados por hora, con filtro especial entre las 17:00 y las 21:00 hs.

    Reporte de leads por categoría/servicio: visualización del volumen diario clasificado por tipo de servicio y canal de origen.

# 🔮 Mejoras Futuras

    Conexión directa a base de datos o APIs.

    Filtros dinámicos para fechas, canales y categorías.

    Segmentaciones personalizadas por estado del lead.

    Paneles multiusuario.

# 🧹 Notas

    Este es un prototipo inicial. Los datos actuales provienen de un CSV de prueba.

    A medida que se formalice el proceso en Táctica, se actualizarán campos y reportes.