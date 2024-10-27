import streamlit as st
import pandas as pd
import plotly.express as px


df = pd.read_csv('dailyForecastResultFinal3.csv', index_col=0, parse_dates=True)


df['month'] = df.index.month_name()
df['year'] = df.index.year
df['quarter'] = df.index.to_period('Q').strftime('Q%q %Y')


st.title('Bread Daily Production Quantity Forecast')


if 'prev_forecast_type' not in st.session_state:
    st.session_state['prev_forecast_type'] = None

if 'prev_period' not in st.session_state:
    st.session_state['prev_period'] = None


forecastType = st.selectbox('Select Forecast Type', ['Yearly', 'Monthly', 'Quarterly'])


options = []


if forecastType == 'Yearly':
    options = ['2022', '2023', '2024']

elif forecastType == 'Monthly':
    months_years = df[['month', 'year']].drop_duplicates()
    options = [f"{row['month']} {row['year']}" for _, row in months_years.iterrows()]

elif forecastType == 'Quarterly':
    options = df['quarter'].unique()


period = st.selectbox('Select Period', options)


if forecastType != st.session_state['prev_forecast_type'] or period != st.session_state['prev_period']:
    st.session_state['show_forecast'] = False
    st.session_state['prev_forecast_type'] = forecastType
    st.session_state['prev_period'] = period


if 'show_forecast' not in st.session_state:
    st.session_state['show_forecast'] = False

if st.button('Show Forecast'):
    st.session_state['show_forecast'] = True


if st.session_state['show_forecast']:
    filteredForecast = pd.DataFrame()
    if forecastType == 'Yearly' and period:
        if period == '2022':
            filteredForecast = df['2022-10-01':'2022-12-31']

        elif period == '2023':
            filteredForecast = df['2023-01-01':'2023-12-31']

        elif period == '2024':
            filteredForecast = df['2024-01-01':'2024-12-31']

        dayAmt = len(filteredForecast)
        days = st.slider('Select Number of Days', 1, dayAmt, 4)
        filteredForecast = filteredForecast.head(days)

    elif forecastType == 'Monthly' and period:
        month, year = period.split()
        year = int(year)
        filteredForecast = df[(df['month'] == month) & (df['year'] == year)]
        dayAmt = len(filteredForecast)
        days = st.slider('Select Number of Days', 1, dayAmt, 4)
        filteredForecast = filteredForecast.head(days)
        
    elif forecastType == 'Quarterly' and period:
        filteredForecast = df[df['quarter'] == period]
        dayAmt = len(filteredForecast)
        days = st.slider('Select Number of Days', 1, dayAmt, 4)
        filteredForecast = filteredForecast.head(days)


    if not filteredForecast.empty:
        fig = px.line(filteredForecast, x=filteredForecast.index, y='Amount of Bread', title='Bread Daily Quantity Forecast')
        fig.update_layout(width=1200, height=600)  
        st.plotly_chart(fig)
        st.write(filteredForecast)


st.title('FURTHER SALES ANALYSIS')


powerbi_dashboard_url = "https://app.powerbi.com/view?r=eyJrIjoiZTIzOGRjOTctOThmMi00MjQyLWFkNDYtNDdhMzFkZGE4NDE2IiwidCI6IjBmZWQwM2EzLTQwMmQtNDYzMy1hOGNkLThiMzA4ODIyMjUzZSIsImMiOjEwfQ%3D%3D"
st.markdown(f"""
    <div style="display: flex; justify-content: center;">
        <iframe title="bakerySalesFYPDashboard" width="1280" height="400" src="{powerbi_dashboard_url}" frameborder="0" allowFullScreen="true"></iframe>
    </div>
    """, unsafe_allow_html=True)
