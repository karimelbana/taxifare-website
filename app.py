import streamlit as st

import datetime
import requests

import pandas as pd
import numpy as np

import leafmap.foliumap as leafmap

'''
# TaxiFareModel front

This front queries the Le Wagon [taxi fare model API](https://taxifare.lewagon.ai/predict?pickup_datetime=2012-10-06%2012:10:20&pickup_longitude=40.7614327&pickup_latitude=-73.9798156&dropoff_longitude=40.6513111&dropoff_latitude=-73.8803331&passenger_count=2)
'''

with st.form(key='params_for_api'):

    pickup_date = st.date_input('pickup datetime', value=datetime.datetime(2012, 10, 6, 12, 10, 20))
    pickup_time = st.time_input('pickup datetime', value=datetime.datetime(2012, 10, 6, 12, 10, 20))
    pickup_datetime = f'{pickup_date} {pickup_time}'
    pickup_longitude = st.number_input('pickup longitude', value=40.7614327)
    pickup_latitude = st.number_input('pickup latitude', value=-73.9798156)
    dropoff_longitude = st.number_input('dropoff longitude', value=40.6413111)
    dropoff_latitude = st.number_input('dropoff latitude', value=-73.7803331)
    passenger_count = st.number_input('passenger_count', min_value=1, max_value=8, step=1, value=1)

    st.form_submit_button('Make prediction')

params = dict(
    pickup_datetime=pickup_datetime,
    pickup_longitude=pickup_longitude,
    pickup_latitude=pickup_latitude,
    dropoff_longitude=dropoff_longitude,
    dropoff_latitude=dropoff_latitude,
    passenger_count=passenger_count)

st.write(params)


wagon_cab_api_url = 'https://taxifare.lewagon.ai/predict'
response = requests.get(wagon_cab_api_url, params=params)
st.write(response.url)

prediction = response.json()

pred = prediction['fare']

st.header(f'Fare amount: ${round(pred, 2)}')

#@st.cache
def get_map_data():

    #return pd.DataFrame({'lat': pickup_latitude, 'lon': pickup_longitude}, index=[0])
    return pd.DataFrame({'latitude': [float(pickup_latitude), float(dropoff_latitude)] ,
                         'longitude': [float(pickup_longitude), float(dropoff_longitude)]}, index=[0,1])

df = get_map_data()

st.write(df)

#st.map(df, zoom=10)
#st.map(latitude=-73, longitude=40)
#data = pd.read_csv("https://raw.githubusercontent.com/opengeos/leafmap/master/examples/data/us_cities.csv")

m = leafmap.Map(center=(pickup_longitude, pickup_latitude), zoom=10)
#m.to_streamlit(height=600)
#m.add_points_from_xy(df, x="lon", y="lat", min_width=10, icon_colors=['red'])
#m.add_points_from_xy(data, x="longitude", y="latitude")
#m

#m = leafmap.Map()
#data = "https://raw.githubusercontent.com/opengeos/leafmap/master/examples/data/us_cities.csv"
#m.add_points_from_xy(data, x="longitude", y="latitude")
m.add_points_from_xy(df, x="latitude", y="longitude", marker_colors=['red'])
#m.add_points_from_xy(df, x="latitude", y="longitude", marker_colors=['red'])

m.to_streamlit(height=600)
