import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('Simple Streamlit dashboard')
st.write('Displaying the dataframe with highways')

@st.cache_data()
def load_data():
    data_url =  'https://github.com/spatialthoughts/python-dataviz-web/releases/' \
        'download/osm/'
    csv_file = 'highway_lengths_by_district.csv'
    url=data_url + csv_file
    
    df=pd.read_csv(url)
    return df

df =load_data()

st.dataframe(df)

districts = df['DISTRICT'].values
district = st.selectbox('Select any district:',districts)
st.text(f'Selected {district}')

filtered = df[df['DISTRICT']==district]


col1, col2, col3 =st.columns(3)
nh_color=col1.color_picker('Select NH color:','#ab34eb',key='nh')
sh_color=col2.color_picker('select SH color:','#eb34a2',key='sh')
filter_dist=col3.radio('Units:', options=['Kilometers','Miles'],index=0, horizontal=False, captions=None, label_visibility="visible")
if filter_dist == 'Kilometers':
    filtered['NH']=filtered['NH']
    filtered['SH']=filtered['SH']
else:
    #filtered['NH']=filtered['NH'].apply(lambda x: x*0.621371) #Convert to miles
    #filtered['SH']=filtered['SH'].apply(lambda x: x*0.621371)
    filtered=filtered[['NH','SH']]*0.621371
    
NH_max=df['NH'].max()
SH_max=df['SH'].max()
#st.text(f'NH max: {NH_max}')
#st.text(f'SH max: {SH_max}')
fig,ax=plt.subplots(1,1)
filtered.plot(kind='bar', ax=ax,color=[nh_color,sh_color], ylabel=f'Highway length {filter_dist}', xlabel='Category')
ax.set_title(f'Length of highways in {district} district ')
ax.set_ylim(0,2500)
ax.set_xticklabels([])
st.pyplot(fig)

