# Core Pkgs
import streamlit as st
import plotly.express as px
# sklearn version = 0.24.2
px.defaults.template='plotly_dark'
px.defaults.color_continuous_scale='reds'

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

#rencana (nama + tanggal + hari + JP + rencana peserta + rencana JP)
#realisasi peserta (per UE1 + total)
#realisasi jamlator (per UE1 + total)
#evaluasi penyelenggaraan pembelajaran (kesesuaian materi)
#evaluasi hasil pembelajaran (status keikutsertaan)
#realisasi jamlator (per UE1 + total) RENCANA VS REALISASI

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
    "Pilih Nama Pelatihan:",
    options=df["NAMA"].unique(),
    default=df["NAMA"].unique()
)

angkatan = st.sidebar.multiselect(
    "Pilih Angkatan:",
    options=df["ANGKATAN"].unique(),
    default=df["ANGKATAN"].unique()
)

df_selection = df.query(
    "TAHUN ==@tahun & `NAMA BULAN` == @bulan & NAMA == @nama & ANGKATAN ==@angkatan"
)

# ---- MAINPAGE ----
tahun_picked = (df_selection['TAHUN'].sum())
st.title("Data Pelatihan Pusat Pendidikan dan Pelatihan Kepemimpinan dan Manajerial")
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
    st.subheader(f"{total_peserta:,}")
with col3:
    st.subheader('TOTAL JAMLATOR')
    st.subheader(f"{total_jamlator:,}")
with col4:
    st.subheader('KESESUAIAN MATERI')
    st.subheader(f"{rerata_seseusaian_materi:,} {indeks_bintang}")

st.markdown("""---""")

st.dataframe(df_selection[['NAMA PELATIHAN', 'TAHUN', 'KESESUAIAN MATERI',	'HARI',	'JP',	'RENCANA PESERTA',	'RENCANA JAMLATOR', 'TELAH MENGIKUTI/LULUS',	'TIDAK MEMENUHI SYARAT',	'MENGUNDURKAN DIRI',	'TIDAK MENGIKUTI',	'TOTAL REALISASI PESERTA',	'PERSENTASE KEIKUTSERTAAN',	'TOTAL JAMLATOR']])

#RENCANA VS REALISASI PESERTA PER PELATIHAN
st.subheader('RENCANA VS REALISASI PESERTA PER PELATIHAN')
realisasi_peserta_by_nama = (
df_selection.groupby(by=['BULAN']).sum()[['RENCANA PESERTA', 'TOTAL REALISASI PESERTA']].sort_values(by='BULAN')
)
st.dataframe(realisasi_peserta_by_nama)
st.line_chart(data=realisasi_peserta_by_nama, x=['BULAN'], y=['RENCANA PESERTA', 'TOTAL REALISASI PESERTA'], width=0, height=0, use_container_width=True)

st.subheader('RENCANA VS REALISASI JAMLATOR PER PELATIHAN')
realisasi_jamlator_by_nama = (
df_selection.groupby(by=['NAMA']).sum()[['RENCANA JAMLATOR', 'TOTAL JAMLATOR']].sort_values(by='NAMA')
)
st.dataframe(realisasi_jamlator_by_nama)
st.line_chart(data=realisasi_jamlator_by_nama, x=['BULAN'], y=['RENCANA JAMLATOR', 'TOTAL JAMLATOR'], width=0, height=0, use_container_width=True)

#st.subheader('PERSENTASE KEIKUTSERTAAN DAN REALISASI JAMLATOR')
#persentase_keikutsertaan_by_bulan = (
#round(df_selection.groupby(by=['BULAN']).mean()[['PERSENTASE KEIKUTSERTAAN']].sort_values(by='BULAN'), 2)
#)
#st.dataframe(persentase_keikutsertaan_by_bulan)
#st.bar_chart(data=persentase_keikutsertaan_by_bulan, x=['BULAN'], y=['PERSENTASE KEIKUTSERTAAN'], width=0, height=0, use_container_width=True)


st.subheader('INDEKS KESESUAIAN MATERI')
kesesuaian_materi = (
round(df_selection.groupby(by=['BULAN']).mean()[['KESESUAIAN MATERI']].sort_values(by='BULAN'), 2)
)
st.dataframe(kesesuaian_materi)
st.bar_chart(data=kesesuaian_materi, x=['BULAN'], y=['KESESUAIAN MATERI'], width=0, height=0, use_container_width=True)

st.subheader('PESERTA PER STATUS')
peserta_per_unit = (
df_selection.groupby(by=['NAMA']).sum()[['TELAH MENGIKUTI/LULUS', 'TIDAK MEMENUHI SYARAT', 'MENGUNDURKAN DIRI',	'TIDAK MENGIKUTI']].sort_values(by='NAMA')
)
st.dataframe(peserta_per_unit)
st.line_chart(data=peserta_per_unit, x=['NAMA'], y=['TELAH MENGIKUTI/LULUS', 'TIDAK MEMENUHI SYARAT', 'MENGUNDURKAN DIRI',	'TIDAK MENGIKUTI'], width=0, height=0, use_container_width=True)    

st.subheader('PESERTA PER UNIT')
peserta_per_unit = (
df_selection.groupby(by=['NAMA']).sum()[['PESERTA SETJEN',	'PESERTA ITJEN',	'PESERTA DJA',	'PESERTA DJP',	'PESERTA DJBC',	'PESERTA DJPb',	'PESERTA DJPK',	'PESERTA DJKN',	'PESERTA DJPPR',	'PESERTA BKF',	'PESERTA BPPK',	'PESERTA LNSW',	'PESERTA KSSK']].sort_values(by='NAMA')
)
st.dataframe(peserta_per_unit)
st.area_chart(data=peserta_per_unit, x=['NAMA'], y=['PESERTA SETJEN',	'PESERTA ITJEN',	'PESERTA DJA',	'PESERTA DJP',	'PESERTA DJBC',	'PESERTA DJPb',	'PESERTA DJPK',	'PESERTA DJKN',	'PESERTA DJPPR',	'PESERTA BKF',	'PESERTA BPPK',	'PESERTA LNSW',	'PESERTA KSSK'], width=0, height=0, use_container_width=True)

st.subheader('PESERTA PER JAMLATOR')
peserta_per_unit = (
df_selection.groupby(by=['NAMA']).sum()[['JAMLATOR SETJEN',	'JAMLATOR ITJEN',	'JAMLATOR DJA',	'JAMLATOR DJP',	'JAMLATOR DJBC',	'JAMLATOR DJPb',	'JAMLATOR DJPK',	'JAMLATOR DJKN',	'JAMLATOR DJPPR',	'JAMLATOR BKF',	'JAMLATOR BPPK',	'JAMLATOR LNSW',	'JAMLATOR KSSK']].sort_values(by='NAMA')
)
st.dataframe(peserta_per_unit)
st.line_chart(data=peserta_per_unit, x=['NAMA'], y=['JAMLATOR SETJEN',	'JAMLATOR ITJEN',	'JAMLATOR DJA',	'JAMLATOR DJP',	'JAMLATOR DJBC',	'JAMLATOR DJPb',	'JAMLATOR DJPK',	'JAMLATOR DJKN',	'JAMLATOR DJPPR',	'JAMLATOR BKF',	'JAMLATOR BPPK',	'JAMLATOR LNSW',	'JAMLATOR KSSK'], width=0, height=0, use_container_width=True)

st.subheader('RENCANA VS REALISASI PESERTA PER TAHUN')
realisasi_peserta_by_tahun = (
	df.groupby(by=['TAHUN']).sum()[['RENCANA PESERTA', 'TOTAL REALISASI PESERTA']].sort_values(by='TAHUN')
)
st.dataframe(realisasi_peserta_by_tahun, width=1360)
st.bar_chart(data=realisasi_peserta_by_tahun, x=['TAHUN'], y=['RENCANA PESERTA', 'TOTAL REALISASI PESERTA'], width=0, height=0, use_container_width=True)