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

#st.sidebar.header('Tahun')
#choice = st.sidebar.multiselect(
#    'Pilih Tahun:',
#   options=df['TAHUN'].unique(),
#    default=df['TAHUN'].unique()
#)

#df_selection = df.query(
#    "Choice == @choice"
#)

#st.dataframe(df_selection)

#rencana (nama + tanggal + hari + JP + rencana peserta + rencana JP)
#realisasi peserta (per UE1 + total)
#realisasi jamlator (per UE1 + total)
#evaluasi penyelenggaraan pembelajaran (kesesuaian materi)
#evaluasi hasil pembelajaran (status keikutsertaan)
#realisasi jamlator (per UE1 + total) RENCANA VS REALISASI

# ---- SIDEBAR ----
st.sidebar.header("Tahun")
tahun = st.sidebar.multiselect(
    "Pilih Tahun:",
    options=df["TAHUN"].unique(),
    default=df["TAHUN"].unique()
)

bulan = st.sidebar.multiselect(
    "Pilih Bulan:",
    options=df["BULAN"].unique(),
    default=df["BULAN"].unique(),
)

nama = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["NAMA"].unique(),
    default=df["NAMA"].unique(),
)

angkatan = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["ANGKATAN"].unique(),
    default=df["ANGKATAN"].unique(),
)


df_selection = df.query(
    "TAHUN == @tahun & NAMA BULAN ==@bulan & NAMA == @nama & ANGKATAN ==@angkatan"
)

st.dataframe(df_selection)