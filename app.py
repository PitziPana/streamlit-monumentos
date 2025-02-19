import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Cargar los datos
file_path = "/Volumes/JAVITXU/streamlit_monumentos/monumentos_actualizados.csv"
df = pd.read_csv(file_path)

# Eliminar filas con coordenadas vacías
df = df.dropna(subset=["Latitud", "Longitud"])

# Configuración de la app
st.title("Mapa de Monumentos Altomedievales")
st.markdown("### Consulta los monumentos altomedievales de la península ibérica")

# Crear el mapa
mapa = folium.Map(location=[df["Latitud"].mean(), df["Longitud"].mean()], zoom_start=6)

# Agregar los monumentos con puntos bien visibles
for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row["Latitud"], row["Longitud"]],
        radius=6,  # Ajuste para que sean visibles, pero no gigantes
        color="darkred",  # Un rojo más oscuro para mejor contraste
        fill=True,
        fill_color="red",  # Rojo intenso para que resalte
        fill_opacity=0.9,
        popup=f"<b>{row['Nombre']}</b><br><a href='{row['URL']}' target='_blank'>Ver más</a>",
        tooltip=row["Nombre"],
    ).add_to(mapa)

# Mostrar el mapa en Streamlit
st_folium(mapa, width=800, height=600)

# Mostrar la tabla de monumentos en 3 columnas
st.markdown("### Lista de Monumentos")

monumentos = df[["Nombre", "URL"]].copy()
monumentos["Nombre"] = monumentos.apply(lambda x: f"[{x['Nombre']}]({x['URL']})", axis=1)

# Dividir en 3 columnas
col1, col2, col3 = st.columns(3)

# Llenar cada columna con una parte de la lista
for index, row in enumerate(monumentos["Nombre"]):
    if index % 3 == 0:
        col1.markdown(row, unsafe_allow_html=True)
    elif index % 3 == 1:
        col2.markdown(row, unsafe_allow_html=True)
    else:
        col3.markdown(row, unsafe_allow_html=True)
st.sidebar.image("/Volumes/JAVITXU/streamlit_monumentos/avatar.jpg", width=150)
st.sidebar.write("Manufactured by PitziPana")
