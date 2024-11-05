import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('Streamlit Project')
st.write('Project: Displaying the charts of the selected region')
st.write('Displaying the dataframe of highway lengths by districts')

@st.cache_data
def load_data():

    data_url = 'https://github.com/spatialthoughts/python-dataviz-web/releases/' \
        'download/osm/'
        
    csv_file = 'highway_lengths_by_district.csv'
    url = data_url + csv_file
    df = pd.read_csv(url)
    
    return df

df = load_data()
st.dataframe(df)

#Selecting districts column from df
districts = df['DISTRICT'].values
district=st.selectbox('Select a district:',districts)

st.text(f'Currently selected:{district}')

#Selecting the data of the user selected district
filtered= df[df['DISTRICT']==district]
st.dataframe(filtered)

##Selecting colors for NH, SH
#It will display in 2 rows.
# NH_color = st.color_picker('Select NH color','#3d34eb')
# SH_color = st.color_picker('Select NH color','#eb34eb')
##To dispaly the colors in the same color, we will use st.layouts or containers
col1,col2 = st.columns(2)
NH_color = col1.color_picker('Select NH color','#3d34eb')
SH_color = col2.color_picker('Select SH color','#eb34eb')
# Using Matplotlib to create a bar-chart with the filtered dataframe and display it using st.pyplot() widget.
fig,ax=plt.subplots(1,1)

#filtered.plot(kind='bar',ax=ax,color=['#3d34eb','#eb34eb'], xlabel='Category', ylabel='Highway length in kilometers')
filtered.plot(kind='bar',ax=ax,color=[NH_color,SH_color], xlabel='Category', ylabel='Highway length in kilometers')
ax.set_xticklabels([])

#To display the figure in streamlit
st.pyplot(fig)