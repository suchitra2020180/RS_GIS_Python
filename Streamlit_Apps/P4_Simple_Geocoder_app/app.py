import streamlit as st
import requests
import folium
from streamlit_folium import folium_static

st.title('Simple Geocoder App')
st.markdown('This app will use [OpenRouteSrvice API] (https://openrouteservice.org/)'
            ' to geocode the user given input address to coordinates and display its location on the map')

#Get the address from the user
location = 'Vijayawada'
ORS_API_Key = '5b3ce3597851110001cf624881bd046c52854751bb431394a4c8af38'

url='https://api.openrouteservice.org/geocode/search'
parameters={
    'api_key' :ORS_API_Key,
    'text' : location
}

response = requests.get(url,parameters)
if response.status_code == 200:
    st.text('Request Successful')
    data = response.json()
else:
    st.text('Request Failed')
    
result= data  #Its a dictionary

coordinates = result['features'][0]['geometry']['coordinates']


st.write(f'Result: {result}')
st.write(f'Location: {location}, coordinates: {coordinates}')

#Lets add a marker at these coordinates in folium

map=folium.Map(coordinates,zoom_start=5)
folium.Marker((coordinates[1],coordinates[0]),popup=location,icon=folium.Icon(color='green', icon='crosshairs', prefix='fa')). add_to(map)
folium_static(map,width=800)