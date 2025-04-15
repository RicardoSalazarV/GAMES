🎮 Análisis Interactivo de Videojuegos
Aplicación web interactiva construida con Streamlit que permite explorar estadísticas de un conjunto de datos de videojuegos. La app permite cargar datos personalizados, visualizar estadísticas agregadas por plataforma y explorar juegos específicos.

📦 Contenido del Proyecto
bash
Copiar
Editar
├── datasets/
│   └── games.csv               # Dataset por defecto de videojuegos
├── app.py                      # Código principal de la aplicación Streamlit
├── requirements.txt            # Dependencias del proyecto
└── README.md                   # Este archivo
🚀 Demo en Línea
Desplegado en Render:

🔗 Abrir la aplicación
https://games-xtfr.onrender.com

📊 Funcionalidades Principales
Carga de datos dinámica desde archivo CSV o ruta predefinida

Limpieza y procesamiento automático del dataset

Estadísticas por plataforma:

Total de ventas

Número de juegos

Puntaje promedio de críticos y usuarios

Visualización gráfica con Seaborn

Explorador interactivo de juegos por plataforma

📁 Dataset
El dataset games.csv debe estar ubicado en una de estas rutas:

datasets/games.csv (estructura recomendada)

También se puede subir manualmente desde la interfaz de la app

El archivo debe contener al menos las siguientes columnas:

name, platform, genre, year_of_release, critic_score, user_score, rating, na_sales, eu_sales, jp_sales, other_sales

