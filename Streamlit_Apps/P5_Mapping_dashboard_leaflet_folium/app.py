import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import leafmap.foliumap as leafmap

st.set_page_config(page_title='dashboard',layout='wide')
st.title('Mapping Highway dashboard')
st.info('Maps')

#Creating side bar
st.sidebar.title('About')
st.sidebar.info('Explore the highway statistics')

##Get data
data_url = 'https://storage.googleapis.com/spatialthoughts-public-data/python-dataviz/osm/'
gpkg_file = 'karnataka.gpkg'
csv_file = 'highway_lengths_by_district.csv'

##Functions to read data

#For gpkg file
@st.cache_data
def read_gpkg(url, layer):
    gdf = gpd.read_file(url, layer=layer)
    return gdf
    

#For csv file
@st.cache_data
def read_csv(url):
    df = pd.read_csv(url)
    return df
    


#Filepath given to function
data_loading = st.text('Loading data . . . ')
gpkg_url = data_url + gpkg_file
csv_url = data_url + csv_file
districts_gdf = read_gpkg(gpkg_url, layer = 'karnataka_districts')

roads_gdf = read_gpkg(gpkg_url, layer = 'karnataka_highways')

length_df = read_csv(csv_url)

data_loading.text('Loading data done!! ')



#Create charts on the side bar
districts = districts_gdf['DISTRICT'].values
sel_district = st.sidebar.selectbox('Select any district',districts)
st.text(f'Selected {sel_district}')

#Get the length of highways in that district from csv file
length_district =length_df[length_df['DISTRICT']==sel_district]
#Adding checkbox for Roads in that district
overlay = st.sidebar.checkbox('Overlay roads')

#st.dataframe(length_district)

fig,ax =plt.subplots(1,1)
length_district.plot(ax=ax, kind='bar',color=['green','red'], xlabel='Category', ylabel='Highway length')
ax.set_xticklabels([])
ax.set_ylim(0, 2500)
st.sidebar.pyplot(fig)


#Create folium map using leafmap
map=leafmap.Map(layers_control=True,zoom=5,draw_control=False,
    measure_control=False,
    fullscreen_control=False,)
map.add_basemap('CartoDB.DarkMatter')
map.add_gdf(gdf=districts_gdf, zoom_to_layer=False, layer_name ='districts',info_mode='on click', style={'color':'#7fcdbb', 'fillOpacity': 0.3, 'weight': 3}) #Does not display info
#map.add_gdf(gdf=districts_gdf, zoom_to_layer=False, layer_name ='districts', style={'color':'#7fcdbb', 'fillOpacity': 0.3, 'weight': 0.5}) #Display info when overlay curser on district

if overlay:
    map.add_gdf(
        gdf=roads_gdf,
        zoom_to_layer=False,
        layer_name='highways',
        info_mode=None,
        style={'color': 'red', 'weight': 1.5},
    )
selected_dist_gdf=districts_gdf[districts_gdf['DISTRICT']==sel_district]
map.add_gdf(gdf=selected_dist_gdf, zoom_to_layer=True,layer_name='Selected_distrct',info_mode=None, style={'color':'orange', 'fill':None, 'weight':5})
m_streamlit = map.to_streamlit(800, 600)