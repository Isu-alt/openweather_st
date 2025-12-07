import streamlit as st
import plotly.express as px
import requests
import pandas as pd

#https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}

API_KEY=st.secrets["openweathermap"]["api_key"]
BASE_URL="https://api.openweathermap.org/data/2.5/weather"

@st.cache_data(ttl=84600)
def fetch_stock_data(city_name):
    print(f"Fetch data {city_name}")
    
    url = f"{BASE_URL}?q={city_name}&appid={API_KEY}&units=metric"
    print(url)
    response =requests.get(url)

    if response.status_code == 200:
        print(response.text)
        return response.json()
    else:
        st.error(f"Faild to fetch data: {response.status_code} - {response.text}")

#fetch_stock_data("New York")

def process_data(data):

    if  "coord" in data and "main" in data and "wind" in data:
        df = pd.DataFrame([ {**data['coord'],**data['main'], **data['wind']} ])
        df = df.drop(columns=["feels_like", "temp_min", "temp_max", "sea_level", "grnd_level"])
        numeric_float_columns = ["lon", "lat","temp", "speed"]
        numerik_int_columns = ["pressure", "humidity","deg"]
        df[numeric_float_columns] = df[numeric_float_columns].astype(float)
        df[numerik_int_columns] = df[numerik_int_columns].astype(int)
        print(df)
        return df
    
    else:
        st.error("Not data available")
        return None
    

def main():
    st.title("Robot Dreams Python - Weather Map & Data Visualization App")
    
    stock_city_name = st.text_input(
        "Enter City Name: ", "Budapest"
    )
    
    data = fetch_stock_data(stock_city_name)

    if data:
        df = process_data(data)
        st.header(f"Current Weather in {stock_city_name}")

        if df is not None:
            temp_kpi, humid_kpi, wind_kpi = st.columns(3)

            # TEMP KPI
            with temp_kpi:
                st.metric(label="Tempature (°C)", value=f"{df['temp'].values[0]} °C")
            # HUMINIDY KPI
            with humid_kpi:
                st.metric(label="Humidity (%)", value=f"{df['humidity'].values[0]} %")
            # WIND KPI
            with wind_kpi:
                st.metric(label="Wind Speed (m/s)", value=f"{df['speed'].values[0]} m/s")

            #MAPS
            st.subheader("Weather Map")
            st.map(df['lat', 'lon'])

    else:
        st.error("No data!")


if __name__=="__main__":
    main()

