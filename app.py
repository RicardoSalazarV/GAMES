# app.py
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Configuración general
st.set_page_config(page_title="Análisis de Videojuegos", layout="wide")

# Título
st.title("📊 Análisis de Videojuegos")
st.markdown("Explora estadísticas y tendencias de videojuegos a partir de un dataset procesado.")

# Función para cargar y procesar los datos
@st.cache_data
def load_data(uploaded_file=None):
    try:
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.success("✅ Datos cargados desde el archivo subido por el usuario.")
        else:
            # Rutas por defecto
            possible_paths = [
                "datasets/games.csv",
                "games.csv",
                "./games.csv",
                os.path.join("datasets", "games.csv")
            ]

            # Ruta local (desarrollo)
            local_path = "C:\\Users\\ricar\\Desktop\\videojuegos\\datasets\\games.csv"
            if os.path.exists(local_path):
                possible_paths.insert(0, local_path)

            df = None
            for path in possible_paths:
                try:
                    df = pd.read_csv(path)
                    st.success(f"✅ Datos cargados correctamente desde: `{path}`")
                    break
                except FileNotFoundError:
                    continue

            if df is None:
                st.warning("⚠️ No se encontró el archivo de datos. Por favor, carga un archivo CSV.")
                return pd.DataFrame()
        
        # Limpieza y procesamiento
        df.columns = df.columns.str.lower().str.replace(" ", "_").str.strip()
        df = df.dropna(subset=['name', 'genre'])

        df['year_of_release'] = df['year_of_release'].fillna(df['year_of_release'].median())

        df['critic_score_null'] = df['critic_score'].isnull().astype(int)
        df['critic_score'] = df['critic_score'].fillna(df['critic_score'].median())

        df['user_score'] = pd.to_numeric(df['user_score'], errors='coerce')
        df['user_score'] = df['user_score'].fillna(df['user_score'].median())

        df['rating'] = df['rating'].fillna(df['rating'].mode()[0])

        df['total_sales'] = (
            df['na_sales'] + df['eu_sales'] + df['jp_sales'] + df['other_sales']
        )

        return df

    except Exception as e:
        st.error(f"❌ Error al cargar los datos: {e}")
        return pd.DataFrame()

# Subida de archivo
uploaded_file = st.file_uploader("📁 Carga tu propio archivo CSV de videojuegos", type=["csv"])
games = load_data(uploaded_file)

if not games.empty:
    # Análisis por plataforma
    st.subheader("📦 Estadísticas por Plataforma")

    platform_stats = games.groupby('platform').agg({
        'total_sales': 'sum',
        'name': 'count',
        'critic_score': 'mean',
        'user_score': 'mean'
    }).rename(columns={'name': 'count_of_games'}).reset_index()

    # Mostrar tabla
    st.dataframe(platform_stats.sort_values(by="total_sales", ascending=False))

    # Visualizaciones
    st.subheader("📈 Visualización de Ventas por Plataforma")

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=platform_stats.sort_values(by="total_sales", ascending=False),
                x="platform", y="total_sales", ax=ax, palette="viridis")
    ax.set_title("Total de Ventas por Plataforma")
    ax.set_ylabel("Millones de unidades")
    st.pyplot(fig)

    # Filtro interactivo por plataforma
    st.subheader("🎮 Explora Juegos por Plataforma")

    platforms = sorted(games['platform'].unique())
    selected_platform = st.selectbox("Selecciona una plataforma", platforms)

    filtered_games = games[games['platform'] == selected_platform]
    st.write(f"Juegos disponibles: {len(filtered_games)}")

    st.dataframe(filtered_games[['name', 'genre', 'year_of_release', 'total_sales', 'critic_score', 'user_score']].sort_values(by="total_sales", ascending=False))

    st.markdown("---")
    st.markdown("App creada por [RICARDO SALAZAR] • • Desplegada en Render")
else:
    st.info("Por favor, carga un archivo CSV para continuar.")
