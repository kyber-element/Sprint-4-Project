import pandas as pd
import plotly.express as px

df = pd.read_csv('./datasets/vehicles_us.csv')

df.info()

df_miss = df.isna().sum()

df_dup = df.duplicated().sum()

df_check = df[df.isna().any(axis=1)]

df['engine_capacity'] = df['engine_capacity'].fillna(0.0)

df = df.drop(df.columns[0], axis=1)

manufacturer_choice = df['manufacturer_name'].unique()

list_for_hist = ['transmission', 'engine_type', 'body_type', 'state']

price_hist = px.histogram(df, x='price_usd', title='Distribution of Prices')

body_hist = px.histogram(df, x='body_type', title='Distribution of Vehicle Types')

df['age'] = 2024 - df['year_produced']

def age_category(x):
    if x < 5:
        return '0-5'
    elif x <= 10:
        return '5-10'
    elif x <= 20:
        return '10-20'
    else:
        return '20+'

df['age_category'] = (df['age']).apply(age_category)

odo_pic_scatter = px.scatter(df, x='odometer_value', y='price_usd', color='number_of_photos', title='Price vs Mileage with Photos Overlay')

year_manu_scatter = px.scatter(df, x='year_produced', y='price_usd', color='manufacturer_name', title='Price vs Year Produced by Manufacturer')

list_for_scatter = ['odometer_value', 'engine_capacity', 'number_of_photos']


import streamlit as st

# Check if the checkbox is checked
agree = st.checkbox('By checking this box, you acknowledge this is a work in progress and not current sales figures.')
if agree:
    st.header('Market prices of car ads.')

    st.write('This study analyzes the market prices of car advertisements, focusing on understanding how various factors influence the pricing of used vehicles. By collecting a comprehensive dataset that includes variables such as manufacturer name, model, transmission type, color, odometer reading, year of production, engine type and capacity, body type, warranty status, and the condition of the vehicle, the study aims to identify trends and correlations within the used car market. The analysis explores how attributes like mileage, age, engine size, and brand reputation impact the listed prices of cars. Additionally, the study examines the distribution of prices across different categories and investigates price patterns based on geographic location, vehicle condition (new vs. used), and other key characteristics. The findings of this study are intended to provide valuable insights for both buyers and sellers in the used car market, helping them make informed decisions based on data-driven price trends and factors that most significantly affect vehicle value.')
    st.write('Filter the data below to see the models by manufacturer.')

# Manufacturer selection
    selected_menu = st.selectbox('Select a manufacturer', manufacturer_choice, key='selectbox1')

# Year slider selector
    df['year_produced'].min(), df['year_produced'].max()

    min_year, max_year = int(df['year_produced'].min()), int(df['year_produced'].max())

    year_range = st.slider('Select years', value=(min_year, max_year), min_value=min_year, max_value=max_year)

    df_filtered = df[(df['manufacturer_name'] == selected_menu) & (df['year_produced'].between(year_range[0], year_range[1]))]

    st.dataframe(df_filtered)

    st.header('Price analysis')
    st.write('''
             Let's analyze what influences price the most. We will check how distribution of price varies depending on transmission, engine, body type, and the vehicle's state.
    ''')

# Histogram based on selected type
    selected_type = st.selectbox('Split for price distribution', list_for_hist, key='selectbox2')

    fig1 = px.histogram(df, x='price_usd', color = selected_type)
    fig1.update_layout(title='<b> Split of price by {}</b>'.format(selected_type))

    st.plotly_chart(fig1)

# Scatter plot based on selected attribute

    choice_for_scatter = st.selectbox('Price dependency on', list_for_scatter, key='selectbox3')

    fig2 = px.scatter(df, x=choice_for_scatter, y='price_usd', color='age_category', hover_data=['year_produced'])
    fig2.update_layout(title='<b> Price vs {}</b>'.format(choice_for_scatter))

    st.plotly_chart(fig2)
    
    st.header('Conclusion')
    
    st.write('This analysis delves into the market prices of used cars by examining a dataset containing detailed information about various vehicle attributes, including manufacturer, model, transmission type, color, odometer reading, year of production, engine type and capacity, and body type')


else:
    st.write('### Please check to confirm and proceed.')