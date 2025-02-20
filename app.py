import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Cargar los datos
file_path = "monumentos_actualizados.csv"
df = pd.read_csv(file_path)

# Eliminar filas con coordenadas vacías
df = df.dropna(subset=["Latitud", "Longitud"])

# Intentar obtener la ubicación del usuario
geolocator = Nominatim(user_agent="streamlit-monumentos")
try:
    location = geolocator.geocode("Madrid, España")  # Simulación de ubicación del usuario
    user_lat, user_lon = location.latitude, location.longitude
except GeocoderTimedOut:
    user_lat, user_lon = df["Latitud"].mean(), df["Longitud"].mean()  # Ubicación por defecto si falla

# Configuración de la app
st.title("Mapa de Monumentos Altomedievales")
st.markdown("### Consulta los monumentos altomedievales de la península ibérica")

# Crear el mapa
mapa = folium.Map(location=[user_lat, user_lon], zoom_start=6)

# Agregar la ubicación del usuario
folium.Marker(
    [user_lat, user_lon],
    popup="📍 Mi ubicación",
    tooltip="📍 Mi ubicación",
    icon=folium.Icon(color="blue", icon="user"),
).add_to(mapa)

# Agregar los monumentos con puntos bien visibles
for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row["Latitud"], row["Longitud"]],
        radius=6,
        color="darkred",
        fill=True,
        fill_color="red",
        fill_opacity=0.9,
        popup=f"<b>{row['Nombre']}</b><br><a href='{row['URL']}' target='_blank'>Ver más</a>",
        tooltip=row["Nombre"],
    ).add_to(mapa)

# Mostrar el mapa en Streamlit
st_folium(mapa, width=800, height=600)

