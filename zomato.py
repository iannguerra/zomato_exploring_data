import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
# Load data
path = "zomato.csv"
df = pd.read_csv(path)

# Dicionário de países
COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
}

# Mapear os códigos de país para os nomes de país
df['Country Name'] = df['Country Code'].map(COUNTRIES)

st.sidebar.title("Zomato Dashboard")

categories = ['Geral', 'País', 'Cidades', 'Restaurantes', 'Tipo de Culinária']

selected_category = st.sidebar.radio("Selecione a categoria", categories)

def create_google_maps_style_map(data, lat_column, lon_column, color_column, size_column, title, column):
    fig = px.scatter_mapbox(
        data,
        lat=lat_column,
        lon=lon_column,
        color=color_column,
        size=size_column,
        hover_name='Restaurant Name',
        title=title,
        mapbox_style="carto-positron",  
        zoom=1, 
        opacity=0.7,  
        color_continuous_scale="Viridis",
    )

    column.plotly_chart(fig)


if selected_category == "Geral":
    st.title('**Informações Gerais**')
    col1, col2, col3, col4 = st.columns(4)
    # Display key metrics
    col1.metric("Restaurantes Cadastrados", f"{df['Restaurant ID'].nunique():,}")
    col1.metric("Países Cadastrados", f"{df['Country Code'].nunique():,}")
    col2.metric("Cidades Cadastradas", f"{df['City'].nunique():,}")
    
    total_votes = df['Votes'].sum()
    formatted_total_votes = "{:,}".format(total_votes)
    col2.metric("Total de Avaliações", f"{formatted_total_votes}")
    
    col3.metric("Culinárias Registradas", f"{df['Cuisines'].nunique():,}")

    # Geographic Map
    create_google_maps_style_map(df, 'Latitude', 'Longitude', 'Rating color','Votes', 'Distribuição de restaurantes por países',col1)


elif selected_category == 'País':
    st.title('**Informações dos Países**')

    # Criar um gráfico de barras
    bar_fig = px.bar(
        df.groupby('Country Name')['City'].nunique().reset_index(),
        x='Country Name',
        y='City',
        title='Número de Cidades Registradas por País',
        labels={'City': 'Número de Cidades', 'Country Name': 'País'},
    )
    bar_fig.update_layout(xaxis_title='Países', yaxis_title='Número de Cidades')

    # Exibir gráfico no Streamlit
    st.plotly_chart(bar_fig) 
    
    bar_fig2 = px.bar(
        df.groupby('Country Name')['Restaurant ID'].nunique().reset_index(),
        x='Country Name',
        y='Restaurant ID',
        title='Países com mais restaurantes registrados',
        labels={'Restaurant ID': 'Número de restaurantes', 'Country Name': 'País'},
    )
    bar_fig2.update_layout(xaxis_title='Países', yaxis_title='Número de Restaurantes')
    st.plotly_chart(bar_fig2)

    
    bar_fig3 = px.bar(
        df[df['Price range'] == 4].groupby('Country Name')['Restaurant ID'].nunique().reset_index(),
        x='Country Name',
        y='Restaurant ID',
        title='Países com mais restaurantes com nível de preço igual a 4',
        labels={'Restaurant ID': 'Número de restaurantes', 'Country Name': 'País'},
    )
    bar_fig3.update_layout(xaxis_title='Países', yaxis_title='Número de Restaurantes')
    st.plotly_chart(bar_fig3)

    bar_fig4 = px.bar(
        df.groupby('Country Name')['Cuisines'].nunique().reset_index(),
        x='Country Name',
        y='Cuisines',
        title='Número de Tipos de Culinária Distintos por País',
        labels={'Cuisines': 'Número de Tipos de Culinária', 'Country Name': 'País'},
    )

    bar_fig4.update_layout(xaxis_title='Países', yaxis_title='Número de Tipos de Culinária')
    st.plotly_chart(bar_fig4)
    
    bar_fig5 = px.bar(
    df.groupby('Country Name')['Votes'].sum().reset_index(),
    x='Country Name',
    y='Votes',
    title='Número Total de Avaliações por País',
    labels={'Votes': 'Número Total de Avaliações', 'Country Name': 'País'},
)
    bar_fig5.update_layout(xaxis_title='Países', yaxis_title='Número Total de Avaliações')
    st.plotly_chart(bar_fig5)

    bar_fig6 = px.bar(
        df.groupby('Country Name')['Restaurant ID'].nunique().reset_index(),
        x='Country Name',
        y='Restaurant ID',
        title='Número de Restaurantes que Fazem Entrega por País',
        labels={'Restaurant ID': 'Número de Restaurantes', 'Country Name': 'País'},
    )
    bar_fig6.update_layout(xaxis_title='Países', yaxis_title='Número de Restaurantes')
    st.plotly_chart(bar_fig6)

    bar_fig_reservations = px.bar(
        df.groupby('Country Name')['Has Table booking'].sum().reset_index(),
        x='Country Name',
        y='Has Table booking',
        title='Número de Restaurantes que Aceitam Reservas por País',
        labels={'Has Table booking': 'Número de Restaurantes', 'Country Name': 'País'},
    )
    bar_fig_reservations.update_layout(xaxis_title='Países', yaxis_title='Número de Restaurantes')
    st.plotly_chart(bar_fig_reservations)


    bar_fig_avg_rating = px.bar(
        df.groupby('Country Name')['Aggregate rating'].mean().reset_index(),
        x='Country Name',
        y='Aggregate rating',
        title='Média das Notas Médias por País',
        labels={'Aggregate rating': 'Média das Notas Médias', 'Country Name': 'País'},
    )
    bar_fig_avg_rating.update_layout(xaxis_title='Países', yaxis_title='Média das Notas Médias')
    st.plotly_chart(bar_fig_avg_rating)

    bar_fig_avg_price_for_two = px.bar(
        df.groupby('Country Name')['Average Cost for two'].mean().reset_index(),
        x='Country Name',
        y='Average Cost for two',
        title='Média de Preço de um Prato para Dois por País',
        labels={'Average Cost for two': 'Média de Preço para Dois', 'Country Name': 'País'},log_y=True
    )
    bar_fig_avg_price_for_two.update_layout(xaxis_title='Países', yaxis_title='Média de Preço para Dois')
    st.plotly_chart(bar_fig_avg_price_for_two)

if selected_category == 'Cidades':
    st.title('**Informações sobre as cidades**')

    # Pergunta 1: Cidade com mais restaurantes registrados
    city_most_restaurants = df['City'].value_counts().idxmax()
    st.write(f"A cidade que possui mais restaurantes registrados é: {city_most_restaurants}")

    # Gráfico 1: Número de restaurantes por cidade
    city_counts = df['City'].value_counts().reset_index()
    city_counts.columns = ['Cidade', 'Número de Restaurantes']
    fig1 = px.bar(city_counts, x='Cidade', y='Número de Restaurantes', labels={'Cidade': 'Cidade', 'Número de Restaurantes': 'Número de Restaurantes'})
    fig1.update_layout(title_text='Número de Restaurantes por Cidade')
    st.plotly_chart(fig1)

    # Pergunta 2: Cidade com mais restaurantes com nota média acima de 4
    city_high_rating = df[df['Aggregate rating'] > 4]['City'].value_counts().idxmax()
    st.write(f"A cidade que possui mais restaurantes com nota média acima de 4 é: {city_high_rating}")

    # Gráfico 2: Número de restaurantes com nota média acima de 4 por cidade
    city_high_rating_counts = df[df['Aggregate rating'] > 4]['City'].value_counts().reset_index()
    city_high_rating_counts.columns = ['Cidade', 'Número de Restaurantes']
    fig2 = px.bar(city_high_rating_counts, x='Cidade', y='Número de Restaurantes', labels={'Cidade': 'Cidade', 'Número de Restaurantes': 'Número de Restaurantes'})
    fig2.update_layout(title_text='Número de Restaurantes com Nota Média Acima de 4 por Cidade')
    st.plotly_chart(fig2)

    # Pergunta 3: Cidade com mais restaurantes com nota média abaixo de 2.5
    city_low_rating = df[df['Aggregate rating'] < 2.5]['City'].value_counts().idxmax()
    st.write(f"A cidade que possui mais restaurantes com nota média abaixo de 2.5 é: {city_low_rating}")

    # Gráfico 3: Número de restaurantes com nota média abaixo de 2.5 por cidade
    city_low_rating_counts = df[df['Aggregate rating'] < 2.5]['City'].value_counts().reset_index()
    city_low_rating_counts.columns = ['Cidade', 'Número de Restaurantes']
    fig3 = px.bar(city_low_rating_counts, x='Cidade', y='Número de Restaurantes', labels={'Cidade': 'Cidade', 'Número de Restaurantes': 'Número de Restaurantes'})
    fig3.update_layout(title_text='Número de Restaurantes com Nota Média Abaixo de 2.5 por Cidade')
    st.plotly_chart(fig3)

    # Pergunta 4: Cidade com o maior valor médio de um prato para dois
    city_highest_avg_price_for_two = df.groupby('City')['Average Cost for two'].mean().idxmax()
    st.write(f"A cidade que possui o maior valor médio de um prato para dois é: {city_highest_avg_price_for_two}")

    avg_price_for_two_by_city = df.groupby('City')['Average Cost for two'].mean().reset_index()
    avg_price_for_two_by_city.columns = ['Cidade', 'Valor Médio de um Prato para Dois']
    fig4 = px.bar(avg_price_for_two_by_city, x='Cidade', y='Valor Médio de um Prato para Dois', 
                  labels={'Cidade': 'Cidade', 'Valor Médio de um Prato para Dois': 'Valor Médio de um Prato para Dois'},
                  log_y=True)
    fig4.update_layout(title_text='Valor Médio de um Prato para Dois por Cidade')
    st.plotly_chart(fig4)

    city_most_cuisines = df.groupby('City')['Cuisines'].nunique().idxmax()
    st.write(f"A cidade que possui a maior quantidade de tipos de culinária distintas é: {city_most_cuisines}")

    # Gráfico 2: Número de tipos de culinária distintas por cidade
    cuisines_counts = df.groupby('City')['Cuisines'].nunique().reset_index()
    cuisines_counts.columns = ['Cidade', 'Número de Tipos de Culinária Distintos']
    fig2 = px.bar(cuisines_counts, x='Cidade', y='Número de Tipos de Culinária Distintos', labels={'Cidade': 'Cidade', 'Número de Tipos de Culinária Distintos': 'Número de Tipos de Culinária Distintos'})
    fig2.update_layout(title_text='Número de Tipos de Culinária Distintos por Cidade')
    st.plotly_chart(fig2)

    # Pergunta 3: Cidade com mais restaurantes que fazem reservas
    city_most_table_booking = df[df['Has Table booking'] == 1]['City'].value_counts().idxmax()
    st.write(f"A cidade que possui a maior quantidade de restaurantes que fazem reservas é: {city_most_table_booking}")

    # Gráfico 3: Número de restaurantes que fazem reservas por cidade
    table_booking_counts = df[df['Has Table booking'] == 1]['City'].value_counts().reset_index()
    table_booking_counts.columns = ['Cidade', 'Número de Restaurantes com Reservas']
    fig3 = px.bar(table_booking_counts, x='Cidade', y='Número de Restaurantes com Reservas', labels={'Cidade': 'Cidade', 'Número de Restaurantes com Reservas': 'Número de Restaurantes com Reservas'})
    fig3.update_layout(title_text='Número de Restaurantes com Reservas por Cidade')
    st.plotly_chart(fig3)

    city_most_delivery = df[df['Has Online delivery'] == 1]['City'].value_counts().idxmax()
    st.write(f"A cidade que possui a maior quantidade de restaurantes que fazem entregas é: {city_most_delivery}")

    # Gráfico 4: Número de restaurantes que fazem entregas por cidade
    delivery_counts = df[df['Has Online delivery'] == 1]['City'].value_counts().reset_index()
    delivery_counts.columns = ['Cidade', 'Número de Restaurantes com Entregas']
    fig4 = px.bar(delivery_counts, x='Cidade', y='Número de Restaurantes com Entregas', labels={'Cidade': 'Cidade', 'Número de Restaurantes com Entregas': 'Número de Restaurantes com Entregas'})
    fig4.update_layout(title_text='Número de Restaurantes com Entregas por Cidade')
    st.plotly_chart(fig4)

    # Pergunta 5: Cidade com mais restaurantes que aceitam pedidos online
    city_most_online_ordering = df[df['Has Online delivery'] == 1]['City'].value_counts().idxmax()
    st.write(f"A cidade que possui a maior quantidade de restaurantes que aceitam pedidos online é: {city_most_online_ordering}")

    # Gráfico 5: Número de restaurantes que aceitam pedidos online por cidade
    online_ordering_counts = df[df['Has Online delivery'] == 1]['City'].value_counts().reset_index()
    online_ordering_counts.columns = ['Cidade', 'Número de Restaurantes com Pedidos Online']
    fig5 = px.bar(online_ordering_counts, x='Cidade', y='Número de Restaurantes com Pedidos Online', labels={'Cidade': 'Cidade', 'Número de Restaurantes com Pedidos Online': 'Número de Restaurantes com Pedidos Online'})
    fig5.update_layout(title_text='Número de Restaurantes com Pedidos Online por Cidade')
    st.plotly_chart(fig5)


if selected_category == 'Restaurantes':
    st.title('**Informações sobre os restaurantes**')
    # Gráficos de barras para as perguntas de 1 a 5
    fig1 = px.bar(df.nlargest(10, 'Votes'), x='Restaurant Name', y='Votes',
                  labels={'Restaurant Name': 'Restaurante', 'Votes': 'Número de Avaliações'},
                  title='Top 10 Restaurantes com Mais Avaliações')
    st.plotly_chart(fig1)

    fig2 = px.bar(df.nlargest(10, 'Aggregate rating'), x='Restaurant Name', y='Aggregate rating',
                  labels={'Restaurant Name': 'Restaurante', 'Aggregate rating': 'Nota Média'},
                  title='Top 10 Restaurantes com Maior Nota Média')
    st.plotly_chart(fig2)

    fig3 = px.bar(df.nlargest(10, 'Average Cost for two'), x='Restaurant Name', y='Average Cost for two',
                  labels={'Restaurant Name': 'Restaurante', 'Average Cost for two': 'Valor Médio para Dois'},
                  title='Top 10 Restaurantes com Maior Valor Médio para Dois')
    st.plotly_chart(fig3)


    fig5 = px.bar(df[(df['Cuisines'].str.contains('Brazilian')) & (df['Country Code'] == 30)].nlargest(10, 'Aggregate rating'), x='Restaurant Name', y='Aggregate rating',
                  labels={'Restaurant Name': 'Restaurante', 'Aggregate rating': 'Nota Média'},
                  title='Top 10 Restaurantes de Culinária Brasileira com Maior Nota Média')
    st.plotly_chart(fig5)
    online_ordering_vs_reviews = df.groupby('Has Online delivery')['Votes'].mean().reset_index()
    online_ordering_vs_reviews.columns = ['Aceita Pedido Online', 'Média de Avaliações']
    fig6 = px.bar(online_ordering_vs_reviews, x='Aceita Pedido Online', y='Média de Avaliações', 
                  labels={'Aceita Pedido Online': 'Aceita Pedido Online', 'Média de Avaliações': 'Média de Avaliações'})
    fig6.update_layout(title_text='Relação entre Aceitação de Pedido Online e Média de Avaliações')
    st.plotly_chart(fig6)

    # Pergunta 7: Restaurantes que fazem reservas são, na média, os que possuem o maior valor médio de um prato para duas pessoas?
    table_booking_vs_avg_price = df.groupby('Has Table booking')['Average Cost for two'].mean().reset_index()
    table_booking_vs_avg_price.columns = ['Faz Reservas', 'Média de Valor para Dois']
    fig7 = px.bar(table_booking_vs_avg_price, x='Faz Reservas', y='Média de Valor para Dois', 
                  labels={'Faz Reservas': 'Faz Reservas', 'Média de Valor para Dois': 'Média de Valor para Dois'})
    fig7.update_layout(title_text='Relação entre Reservas e Média de Valor para Dois')
    st.plotly_chart(fig7)


def find_restaurant_by_rating(df, cuisine_type, find_max=True):
    cuisine_restaurants = df[df['Cuisines'] == cuisine_type].copy()
    cuisine_restaurants['Average Rating'] = cuisine_restaurants.groupby('Restaurant Name')['Aggregate rating'].transform('mean')
    
    if find_max:
        restaurant_info = cuisine_restaurants.loc[cuisine_restaurants['Average Rating'].idxmax()]
    else:
        restaurant_info = cuisine_restaurants.loc[cuisine_restaurants['Average Rating'].idxmin()]
    
    return restaurant_info

if selected_category == 'Tipo de Culinária':
   
    st.title('**Informações sobre Tipos de Culinária**')

    cuisines_list = df['Cuisines'].str.split(', ', expand=True).stack().unique()

    # Escolher a opção para análise
    cuisine_option = st.selectbox('Escolha o tipo de culinária:', cuisines_list)

    # Pergunta 1: Restaurante com a maior média de avaliação para o tipo de culinária escolhido
    top_cuisine_restaurant = find_restaurant_by_rating(df, cuisine_option, find_max=True)
    st.write(f"**Restaurante com a Maior Média de Avaliação de tipo de Culinária ({cuisine_option.capitalize()}):**")
    st.write(top_cuisine_restaurant[['Restaurant Name', 'Average Rating']])

    # Pergunta 2: Restaurante com a menor média de avaliação para o tipo de culinária escolhido
    bottom_cuisine_restaurant = find_restaurant_by_rating(df, cuisine_option, find_max=False)
    st.write(f"**Restaurante com a Menor Média de Avaliação do tipo de Culinária({cuisine_option.capitalize()}):**")
    st.write(bottom_cuisine_restaurant[['Restaurant Name', 'Average Rating']])

    # Gráfico: Média de avaliação para o tipo de culinária escolhido
    cuisine_avg_rating = df[df['Cuisines'].fillna('').str.contains(cuisine_option)].groupby('City')['Aggregate rating'].mean().reset_index()
    cuisine_avg_rating.columns = ['Cidade', 'Média de Avaliação']
    fig_cuisine = px.bar(cuisine_avg_rating, x='Cidade', y='Média de Avaliação', 
                         labels={'Cidade': 'Cidade', 'Média de Avaliação': 'Média de Avaliação'},
                         title=f'Média de Avaliação para Culinária {cuisine_option.capitalize()} por Cidade')
    st.plotly_chart(fig_cuisine)

