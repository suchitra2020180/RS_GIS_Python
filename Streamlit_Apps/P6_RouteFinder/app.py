import streamlit as st
import requests
import folium
from streamlit_folium import folium_static
from streamlit_folium import st_folium

st.set_page_config(page_title='Route Finder')
st.title('Route Finder')
st.markdown('This app uses the [OpenRouteService API](https://openrouteservice.org/) '
  'to geocode and get directions between the specified origin and destination.')
st.info('Enter the cities to find the route')


@st.cache_data
def geocode(location):
    ORS_API_Key=st.secrets['ORS_API_Key']
    url='https://api.openrouteservice.org/geocode/search'
    parameters={
        'api_key': ORS_API_Key,
        'text':location
    }

    response = requests.get(url,parameters)
    if response.status_code == 200:
        print('Request successful')
        data = response.json()
        coordinates = data['features'][0]['geometry']['coordinates']
        #print('coordinates:',coordinates)
        #st.text(f'{coordinates}')
    else:
        print('Request Failed')
        
    return coordinates

@st.cache_data
def distance_api(start_loc, end_loc,travel_mode):
    ORS_API_Key=st.secrets['ORS_API_Key']
    mode_dict = {
        'Car': 'driving-car',
        'Walk': 'foot-walking',
        'Bike': 'cycling-regular'
    }
    #url = 'https://api.openrouteservice.org/v2/directions/driving-car'
    url = 'https://api.openrouteservice.org/v2/directions/'+mode_dict[travel_mode]
    #st.write(url)
    parameters={
        'api_key':ORS_API_Key,
        'start':'{},{}'.format(start_loc[0],start_loc[1]),
        'end':'{},{}'.format(end_loc[0],end_loc[1])
    }
    
    response = requests.get(url,parameters)
    if response.status_code == 200:
        print('Request Successful')
        result = response.json()
        #st.write(result)
        distance_m = result['features'][0]['properties']['summary']['distance']
        coords=result['features'][0]['geometry']['coordinates']
        polyline_coords= [(y,x) for x,y in coords]
        # st.write(polyline_coords)
        # st.info('changed')
        # st.write(polyline_coords)
    else:
        print('Request failed')
    return distance_m,polyline_coords

origin = st.text_input('Start Location (Ex:San Fransisco, CA)')
destination = st.text_input('Destination (Ex:San Francisco, CA)')
modes= ['Car', 'Walk', 'Bike']
travel_mode = st.selectbox('Travel Mode',modes)
button = st.button('Get Directions')

if origin and destination:
    origin_coor= geocode(origin)
    st.text(f'{origin}:{origin_coor}')
    dest_coor = geocode(destination)
    st.text(f'{destination}:{dest_coor}')
        
    [distance ,polyline_coords]= distance_api(origin_coor,dest_coor,travel_mode)
    #st.write('Distance')
    st.text(f'Distance: {distance/1000} km')
    
    ##Mapping
if button:
    map = folium.Map(origin_coor,zoom_start=10)
    folium.Marker(location=(origin_coor[1],origin_coor[0]), popup=origin,tooltip=origin,icon=folium.Icon(color='green',icon='crosshairs',prefix='fa')).add_to(map)
    folium.Marker(location=(dest_coor[1],dest_coor[0]), popup=destination,tooltip=destination,icon=folium.Icon(color='red',icon='crosshairs',prefix='fa')).add_to(map)
    folium.PolyLine(locations=polyline_coords,tooltip=f' Distance from {origin} to {destination} by {travel_mode}: {distance/1000:.2f}  km', color='blue',weight=5).add_to(map)
    # Automatically adjust zoom to include both origin and destination
    map.fit_bounds([(origin_coor[1], origin_coor[0]), (dest_coor[1], dest_coor[0])])
    
    ##Saving the map
    map.save('directions.html')
    with open('directions.html') as file:
        # Define a placeholder to display the distance and download button once computed.    
        placeholder = st.empty()
        placeholder.download_button('Download Directions', data=file, file_name='directions.html')
    folium_static(map)

