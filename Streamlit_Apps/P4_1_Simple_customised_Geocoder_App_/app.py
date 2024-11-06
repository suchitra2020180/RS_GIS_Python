import streamlit as st
import requests
import folium
from streamlit_folium import folium_static   

st.title('Geocoder App')
st.markdown('This app uses the [OpenRouteService API](https://openrouteservice.org/) '
    'to geocode the input address and siplay the results on a map.')

#Allow user to give the location
location = st.text_input('Enter any location to get its coordinates:')
st.text(f'User input: {location}')

#Geocoding code
@st.cache_data
def geocode(address):
    ORS_API_Key='5b3ce3597851110001cf624881bd046c52854751bb431394a4c8af38'
    url = 'https://api.openrouteservice.org/geocode/search'
    parameters = {
        'api_key':ORS_API_Key,
        'text' : address
    }

    response = requests.get(url,parameters)

    if response.status_code == 200:
        st.write('Request Successful')
        result = response.json()
        if result['features']:
            x,y = result['features'][0]['geometry']['coordinates']
            return (y,x)
        
coordinates = geocode(location)
st.text(f'Geocoded coordinates for {location}: {coordinates}')


#Displaying its location on map
basemaps=['OpenStreetMap', 'CartoDB Positron', 'CartoDB DarkMatter','OpenTopoMap','Stadia_StamenWatercolor']
sel_basemap = st.selectbox('Select a basemap:',basemaps)
map=folium.Map(coordinates,zoom_start = 10, tiles=sel_basemap)
folium.Marker(coordinates,popup=[location,coordinates],tooltip= 'click me !',icon=folium.Icon(color='green', icon='cloud', prefix='fa')). add_to(map)
folium_static(map,width=800)


    
    
