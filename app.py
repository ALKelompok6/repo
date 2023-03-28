# Core Pkgs
import streamlit as st
import plotly.express as px
# sklearn version = 0.24.2

import plotly.graph_objects as go
from plotly.subplots import make_subplots

# EDA Pkgs
import pandas as pd
import numpy as np
import seaborn as sns
st.set_option('deprecation.showPyplotGlobalUse', False)

# Utils
import joblib

# Image
from PIL import Image

st.set_page_config(page_title='DATA PELATIHAN JARAH JAUH 2021 DAN 2022',
	page_icon=':bar_chart:',
	layout='wide')

# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

df = load_data(st.secrets["public_gsheets_url"])

st.title("Data Pelatihan 2021 dan 2022 Pusat Pendidikan dan Pelatihan Kepemimpinan dan Manajerial")
st.dataframe(df, width=1360)

st.subheader('TOTAL RENCANA PESERTA PER TAHUN')
rencana_peserta_by_tahun = (
	df.groupby(by=['TAHUN']).sum()[['RENCANA PESERTA']].sort_values(by='TAHUN')
)
st.dataframe(rencana_peserta_by_tahun, width=1360)
st.bar_chart(data=rencana_peserta_by_tahun, x=['TAHUN'], y=['RENCANA PESERTA'], width=0, height=0, use_container_width=True)

st.subheader('TOTAL REALISASI PESERTA PER TAHUN')
realisasi_peserta_by_tahun = (
	df.groupby(by=['TAHUN']).sum()[['TOTAL REALISASI PESERTA']].sort_values(by='TAHUN')
)
st.dataframe(realisasi_peserta_by_tahun, width=1360)
st.bar_chart(data=realisasi_peserta_by_tahun, x=['TAHUN'], y=['TOTAL REALISASI PESERTA'], width=0, height=0, use_container_width=True)

st.subheader('TOTAL RENCANA PESERTA PER NAMA PELATIHAN')
rencana_peserta_by_nama = (
	df.groupby(by=['NAMA']).sum()[['RENCANA PESERTA']].sort_values(by='NAMA')
)
st.dataframe(rencana_peserta_by_nama, width=1760)
st.bar_chart(data=rencana_peserta_by_nama, x=['NAMA'], y=['RENCANA PESERTA'], width=0, height=0, use_container_width=True)

st.subheader('TOTAL REALISASI PESERTA PER NAMA PELATIHAN')
realisasi_peserta_by_nama = (
	df.groupby(by=['NAMA']).sum()[['RENCANA PESERTA', 'TOTAL REALISASI PESERTA']].sort_values(by='NAMA')
)
st.dataframe(realisasi_peserta_by_nama)
st.bar_chart(data=realisasi_peserta_by_nama, x=['NAMA'], y=['RENCANA PESERTA', 'TOTAL REALISASI PESERTA'], width=0, height=0, use_container_width=True)

#df = px.data.gapminder().query("country == 'Italy' ")
#df.loc[:,df.TAHUN == '2021']
#ambil filter data yang memiliki alamat kebayoran lama 
# df['Address']=='Kebayoran Lama, Jakarta'
filter_1 = (df['TAHUN']=='2021')
df.loc[~filter_1,:]