
# ANÁLISIS DE VEHÍCULOS USADOS
# app.py - Aplicación Streamlit


# Importar librerías
import pandas as pd
import plotly.express as px
import streamlit as st

# Leer los datos
car_data = pd.read_csv('vehicles_us.csv')


# CONFIGURACIÓN DE LA APLICACIÓN


# Título principal
st.title('Analisis de Vehiculos Usados')
st.header('Exploracion Interactiva de Datos')

# Información sobre el dataset
st.write(
    f"Dataset: {len(car_data):,} vehiculos - {len(car_data.columns)} columnas")
st.write("Usa los botones abajo para crear visualizaciones.")


# SECCIÓN 1: MOSTRAR TODO EL CATÁLOGO DEL DATASET


st.header('1. Catalogo Completo del Dataset')

# Mostrar todo el dataset
if st.checkbox('Mostrar todo el catalogo del dataset'):
    st.write("Catalogo completo del dataset (usa scroll para navegar):")

    # Mostrar todas las filas con scroll
    st.dataframe(car_data, height=500)

    # Información adicional sobre el dataset
    st.write("**Resumen del dataset:**")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de vehiculos", f"{len(car_data):,}")
    with col2:
        st.metric("Total de columnas", len(car_data.columns))
    with col3:
        # Verificar si model_year existe y tiene datos
        if 'model_year' in car_data.columns and not car_data['model_year'].isna().all():
            min_year = int(car_data['model_year'].min())
            max_year = int(car_data['model_year'].max())
            st.metric("Rango de años", f"{min_year}-{max_year}")
        else:
            st.metric("Columnas", "Sin año")

    # Lista de columnas con tipos de datos
    st.write("**Columnas y tipos de datos:**")
    type_info = pd.DataFrame({
        'Columna': car_data.columns,
        'Tipo de dato': car_data.dtypes.values,
        'Valores unicos': [car_data[col].nunique() for col in car_data.columns],
        'Valores nulos': [car_data[col].isna().sum() for col in car_data.columns]
    })
    st.dataframe(type_info)


# SECCIÓN 2: HISTOGRAMA


st.header('2. Histograma')

# Opción A: Con BOTON (como pide el proyecto)
hist_button = st.button('Construir histograma')

if hist_button:
    st.write(
        'Creacion de un histograma para el conjunto de datos de anuncios de venta de coches')

    # Crear histograma
    fig = px.histogram(
        car_data,
        x="odometer",
        title="Distribucion del Odometro (Kilometraje)",
        labels={"odometer": "Odometro (millas)",
                "count": "Numero de vehiculos"},
        nbins=50
    )

    # Personalizar
    fig.update_layout(
        bargap=0.1,
        showlegend=False
    )

    # Mostrar grafico
    st.plotly_chart(fig, use_container_width=True)

    # Estadisticas adicionales
    st.write(
        f"Promedio de kilometraje: {car_data['odometer'].mean():,.0f} millas")
    st.write(f"Maximo kilometraje: {car_data['odometer'].max():,.0f} millas")

# Opcion B: Con CHECKBOX (extra - opcional)
st.subheader('Otra opcion: Usar checkbox')

build_histogram_checkbox = st.checkbox(
    'Construir un histograma (con checkbox)')

if build_histogram_checkbox:
    st.write('Construyendo un histograma para la columna odometro usando checkbox')

    # Seleccionar columna para histograma
    column_option = st.selectbox(
        'Selecciona la columna para el histograma:',
        ['odometer', 'price', 'model_year', 'days_listed']
    )

    # Crear histograma
    fig = px.histogram(
        car_data,
        x=column_option,
        title=f"Distribucion de {column_option}",
        nbins=30
    )

    # Mostrar grafico
    st.plotly_chart(fig, use_container_width=True)


# SECCIÓN 3: GRAFICO DE DISPERSION


st.header('3. Grafico de Dispersion')

# Boton para grafico de dispersion
scatter_button = st.button('Construir grafico de dispersion')

if scatter_button:
    st.write('Creacion de un grafico de dispersion para el conjunto de datos de anuncios de venta de coches')

    # Limpiar datos
    scatter_data = car_data.dropna(subset=['odometer', 'price'])

    # Crear grafico de dispersion
    fig = px.scatter(
        scatter_data,
        x="odometer",
        y="price",
        title="Relacion entre Odometro y Precio",
        labels={
            "odometer": "Odometro (millas)",
            "price": "Precio (USD)"
        },
        opacity=0.6,
        trendline="ols"
    )

    # Personalizar
    fig.update_layout(
        height=500,
        yaxis=dict(
            tickprefix="$",
            tickformat=","
        )
    )

    # Mostrar grafico
    st.plotly_chart(fig, use_container_width=True)

    # Calcular correlacion
    correlation = scatter_data['odometer'].corr(scatter_data['price'])
    st.write(f"Correlacion: {correlation:.2f}")
    st.write(
        "Nota: 1 = perfecta positiva, -1 = perfecta negativa, 0 = sin correlacion")


# SECCIÓN 4: EXPLORACION ADICIONAL


st.header('4. Exploracion Adicional')

# Mostrar primeros registros
if st.checkbox('Mostrar primeros registros del dataset'):
    num_rows = st.slider('Numero de filas a mostrar:', 5, 100, 10)
    st.write(f"Primeras {num_rows} filas del dataset:")
    st.dataframe(car_data.head(num_rows))

# Estadisticas basicas
if st.checkbox('Mostrar estadisticas descriptivas'):
    st.write("Estadisticas descriptivas del dataset:")
    st.write(car_data.describe())

# Informacion del dataset (sin emojis, como pediste)
if st.checkbox('Mostrar informacion del dataset'):
    st.write("Informacion del dataset:")

    # Mostrar informacion detallada
    st.write("**Informacion general:**")
    st.write(f"- Total de filas: {car_data.shape[0]}")
    st.write(f"- Total de columnas: {car_data.shape[1]}")

    st.write("**Columnas disponibles:**")
    for i, col in enumerate(car_data.columns, 1):
        st.write(f"{i}. {col} ({car_data[col].dtype})")

    st.write("**Resumen de tipos de datos:**")
    type_counts = car_data.dtypes.value_counts()
    for dtype, count in type_counts.items():
        st.write(f"- {dtype}: {count} columnas")

    # Valores nulos
    null_counts = car_data.isnull().sum()
    if null_counts.sum() > 0:
        st.write("**Valores nulos por columna:**")
        for col in car_data.columns:
            null_count = car_data[col].isnull().sum()
            if null_count > 0:
                percentage = (null_count / len(car_data)) * 100
                st.write(f"- {col}: {null_count} nulos ({percentage:.1f}%)")


# SECCIÓN 5: MAS GRAFICOS


st.header('5. Mas Visualizaciones')

# Grafico de barras por condicion
if st.checkbox('Mostrar grafico de barras por condicion'):
    st.write('Grafico de barras: Distribucion por condicion del vehiculo')

    # Contar vehiculos por condicion
    condition_counts = car_data['condition'].value_counts().reset_index()
    condition_counts.columns = ['condition', 'count']

    # Crear grafico de barras
    fig = px.bar(
        condition_counts,
        x='condition',
        y='count',
        title='Numero de Vehiculos por Condicion',
        labels={'condition': 'Condicion', 'count': 'Numero de vehiculos'},
        color='condition'
    )

    # Mostrar grafico
    st.plotly_chart(fig, use_container_width=True)


# PIE DE PAGINA


st.markdown("---")
st.write("Acerca de esta aplicacion")
st.write("""
Esta aplicacion web permite explorar datos de vehiculos usados en venta.
Caracteristicas incluidas:
- Histogramas interactivos
- Graficos de dispersion con linea de tendencia
- Estadisticas descriptivas
- Visualizacion de datos en tablas
- Catalogo completo del dataset

Tecnologias: Streamlit, Plotly Express, Pandas
""")

st.write("Desarrollado como proyecto de analisis de datos de TripleTen Sprint 7")
