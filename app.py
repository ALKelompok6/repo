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
    options=df["NAMA BULAN"].unique(),
    default=df["NAMA BULAN"].unique()
)

nama = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["NAMA"].unique(),
    default=df["NAMA"].unique()
)

angkatan = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["ANGKATAN"].unique(),
    default=df["ANGKATAN"].unique()
)

df_selection = df.query(
    "TAHUN == @tahun & `NAMA BULAN` ==@bulan & NAMA == @nama & ANGKATAN ==@angkatan"
)

st.dataframe(df_selection[['NAMA PELATIHAN', 'TAHUN', 'KESESUAIAN MATERI',	'HARI',	'JP',	'RENCANA PESERTA',	'RENCANA JAMLATOR', 'TELAH MENGIKUTI/LULUS',	'TIDAK MEMENUHI SYARAT',	'MENGUNDURKAN DIRI',	'TIDAK MENGIKUTI',	'TOTAL REALISASI PESERTA',	'PERSENTASE KEIKUTSERTAAN',	'TOTAL JAMLATOR']])

# ---- MAINPAGE ----
st.title("Data Pelatihan 2021 Pusat Pendidikan dan Pelatihan Kepemimpinan dan Manajerial")
total_rencana = int(df_selection['RENCANA PESERTA'].sum())
total_peserta = int(df_selection['TOTAL REALISASI PESERTA'].sum())
total_jamlator = int(df_selection['TOTAL JAMLATOR'].sum())
rerata_seseusaian_materi = round(df_selection['KESESUAIAN MATERI'].mean(), 2)
indeks_bintang =':star:' * int(round(rerata_seseusaian_materi, 0))

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.subheader('RENCANA PESERTA')
    st.subheader(f"{total_rencana:,}")
with col2:
    st.subheader('TOTAL REALISASI PESERTA')
    st.subheader(f"{total_jamlator:,}")
with col3:
    st.subheader('TOTAL JAMLATOR')
    st.subheader(f"{total_peserta:,}")
with col4:
    st.subheader('KESESUAIAN MATERI')
    st.subheader(f"{rerata_seseusaian_materi:,} {indeks_bintang}")

st.markdown("""---""")

#RENCANA VS REALISASI PESERTA PER PELATIHAN
st.subheader('RENCANA VS REALISASI PESERTA PER PELATIHAN')
realisasi_peserta_by_nama = (
df_selection.groupby(by=['NAMA']).sum()[['RENCANA PESERTA', 'TOTAL REALISASI PESERTA']].sort_values(by='NAMA')
)
st.dataframe(realisasi_peserta_by_nama)
st.line_chart(data=realisasi_peserta_by_nama, x=['NAMA'], y=['RENCANA PESERTA', 'TOTAL REALISASI PESERTA'], width=0, height=0, use_container_width=True)