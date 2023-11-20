import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import plotly.express as px

# Load data
path = "zomato.csv"
df = pd.read_csv(path)

# Sidebar
st.sidebar.title("Zomato Dashboard")

categories = ['Geral', 'País', 'Cidades', 'Restaurantes', 'Tipo de Culinária']

# Main content
st.title("General Information")
selected_category = st.sidebar.radio("Select Category", categories)

# Use st.columns() to define columns
col1, col2, col3, col4 = st.columns(4)

def create_google_maps_style_map(data, lat_column, lon_column, color_column, title, column):
    fig = px.scatter_mapbox(
        data,
        lat=lat_column,
        lon=lon_column,
        color=color_column,
        hover_name='Restaurant Name',
        title=title,
        mapbox_style="carto-positron",  # You can choose different map styles
        zoom=1,  # Adjust the initial zoom level
        opacity=0.7,  # Adjust marker opacity
    )
    column.plotly_chart(fig)
if selected_category == "Geral":
    # Display key metrics
    col1.metric("Restaurantes Cadastrados", f"{df['Restaurant ID'].nunique():,}")
    col1.metric("Países Cadastrados", f"{df['Country Code'].nunique():,}")
    col2.metric("Cidades Cadastradas", f"{df['City'].nunique():,}")
    
    total_votes = df['Votes'].sum()
    formatted_total_votes = "{:,}".format(total_votes)
    col2.metric("Total de Avaliações", f"{formatted_total_votes}")
    
    col3.metric("Culinárias Registradas", f"{df['Cuisines'].nunique():,}")

    # Geographic Map
    create_google_maps_style_map(df, 'Latitude', 'Longitude', 'Rating color', 'Restaurant Distribution and Rating by Country', col1)



