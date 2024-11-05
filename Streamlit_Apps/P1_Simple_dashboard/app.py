import streamlit as st
import pandas as pd
st.title('Welcome')
st.write('This is my first streamlit app')
st.write('This dashboard will display a chart for the selected region')

##Data collection
data_url = 'https://github.com/spatialthoughts/python-dataviz-web/releases/' \
      'download/osm/'
csv_file = 'highway_lengths_by_district.csv'
url = data_url + csv_file

#Reading the csv file
df=pd.read_csv(url)

st.dataframe(df)
st.write('The app will now display the dataframe. The dataframe consists of 3 columns. The DISTRICT column contains a unique name for the admin region. The NH and SH columns contain the length of National Highways and State Highways in Kilometers for each admin region. We will now create a dashboard that displays a chart with the lengths of highways for the user-selected admin region.')

st.write('Whenever we run app.py, it will run thewhole data and fetch data through url. For big data sets, it is advisable to put data fetching in a function and use @st.cache_data decorator which will cache the results')
st.write('Anytime the function is called with the same arguments, it will return the cached version of the data instead of fetching it.')
