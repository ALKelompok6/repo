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

st.sidebar.header('Tahun')
menu = ["2021","2022"]
choice = st.sidebar.selectbox("Pilih Tahun", menu)

if choice == "2021":
    st.title("Data Pelatihan 2021 Pusat Pendidikan dan Pelatihan Kepemimpinan dan Manajerial")
    total_rencana = int(df.query(" `TAHUN` == '2,021' ")['RENCANA PESERTA'].sum())
    total_peserta = int(df.query(" `TAHUN` == '2,021' ")['TOTAL REALISASI PESERTA'].sum())
    total_jamlator = int(df.query(" `TAHUN` == '2,021' ")['TOTAL JAMLATOR'].sum())
    rerata_seseusaian_materi = round(df.query(" `TAHUN` == '2,021' ")['KESESUAIAN MATERI'].mean(), 2)
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

    st.dataframe(df[['NAMA PELATIHAN', 'TAHUN', 'KESESUAIAN MATERI',	'HARI',	'JP',	'RENCANA PESERTA',	'RENCANA JAMLATOR', 'TELAH MENGIKUTI/LULUS',	'TIDAK MEMENUHI SYARAT',	'MENGUNDURKAN DIRI',	'TIDAK MENGIKUTI',	'TOTAL REALISASI PESERTA',	'PERSENTASE KEIKUTSERTAAN',	'TOTAL JAMLATOR']].query(" `TAHUN` == '2,021' "))

    st.subheader('TOTAL RENCANA VS REALISASI PESERTA PER NAMA PELATIHAN')
    realisasi_peserta_by_nama = (
	df.query(" `TAHUN` == '2,021' ").groupby(by=['NAMA']).sum()[['RENCANA PESERTA', 'TOTAL REALISASI PESERTA']].sort_values(by='NAMA')
    )
    st.dataframe(realisasi_peserta_by_nama)
    st.line_chart(data=realisasi_peserta_by_nama, x=['NAMA'], y=['RENCANA PESERTA', 'TOTAL REALISASI PESERTA'], width=0, height=0, use_container_width=True)

    st.subheader('TOTAL RENCANA VS REALISASI JAMLATOR PER NAMA PELATIHAN')
    realisasi_jamlator_by_nama = (
	df.query(" `TAHUN` == '2,021' ").groupby(by=['NAMA']).sum()[['RENCANA JAMLATOR', 'TOTAL JAMLATOR']].sort_values(by='NAMA')
    )
    st.dataframe(realisasi_jamlator_by_nama)
    st.line_chart(data=realisasi_jamlator_by_nama, x=['NAMA'], y=['RENCANA JAMLATOR', 'TOTAL JAMLATOR'], width=0, height=0, use_container_width=True)

    st.subheader('INDEKS KESESUAIAN MATERI')
    kesesuaian_materi = (
	df.query(" `TAHUN` == '2,021' ").groupby(by=['BULAN']).mean()[['KESESUAIAN MATERI']].sort_values(by='BULAN')
    )
    st.dataframe(kesesuaian_materi)
    st.line_chart(data=kesesuaian_materi, x=['BULAN'], y=['KESESUAIAN MATERI'], width=0, height=0, use_container_width=True)

    st.subheader('PESERTA PER STATUS')
    peserta_per_unit = (
	df.query(" `TAHUN` == '2,021' ").groupby(by=['NAMA']).sum()[['TELAH MENGIKUTI/LULUS', 'TIDAK MEMENUHI SYARAT', 'MENGUNDURKAN DIRI',	'TIDAK MENGIKUTI']].sort_values(by='NAMA')
    )
    st.dataframe(peserta_per_unit)
    st.line_chart(data=peserta_per_unit, x=['NAMA'], y=['TELAH MENGIKUTI/LULUS', 'TIDAK MEMENUHI SYARAT', 'MENGUNDURKAN DIRI',	'TIDAK MENGIKUTI'], width=0, height=0, use_container_width=True)    

    st.subheader('PESERTA PER UNIT')
    peserta_per_unit = (
	df.query(" `TAHUN` == '2,021' ").groupby(by=['NAMA']).sum()[['PESERTA SETJEN',	'PESERTA ITJEN',	'PESERTA DJA',	'PESERTA DJP',	'PESERTA DJBC',	'PESERTA DJPb',	'PESERTA DJPK',	'PESERTA DJKN',	'PESERTA DJPPR',	'PESERTA BKF',	'PESERTA BPPK',	'PESERTA LNSW',	'PESERTA KSSK']].sort_values(by='NAMA')
    )
    st.dataframe(peserta_per_unit)
    st.line_chart(data=peserta_per_unit, x=['NAMA'], y=['PESERTA SETJEN',	'PESERTA ITJEN',	'PESERTA DJA',	'PESERTA DJP',	'PESERTA DJBC',	'PESERTA DJPb',	'PESERTA DJPK',	'PESERTA DJKN',	'PESERTA DJPPR',	'PESERTA BKF',	'PESERTA BPPK',	'PESERTA LNSW',	'PESERTA KSSK'], width=0, height=0, use_container_width=True)   

elif choice == "2022":
    st.subheader("Data Pelatihan 2022 Pusat Pendidikan dan Pelatihan Kepemimpinan dan Manajerial")
    total_rencana = int(df.query(" `TAHUN` == '2,022' ")['RENCANA PESERTA'].sum())
    total_peserta = int(df.query(" `TAHUN` == '2,022' ")['TOTAL REALISASI PESERTA'].sum())
    total_jamlator = int(df.query(" `TAHUN` == '2,022' ")['TOTAL JAMLATOR'].sum())
    rerata_seseusaian_materi = round(df.query(" `TAHUN` == '2,022' ")['KESESUAIAN MATERI'].mean(), 2)
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

    st.dataframe(df[['NAMA PELATIHAN', 'TAHUN', 'KESESUAIAN MATERI',	'HARI',	'JP',	'RENCANA PESERTA',	'RENCANA JAMLATOR', 'TELAH MENGIKUTI/LULUS',	'TIDAK MEMENUHI SYARAT',	'MENGUNDURKAN DIRI',	'TIDAK MENGIKUTI',	'TOTAL REALISASI PESERTA',	'PERSENTASE KEIKUTSERTAAN',	'TOTAL JAMLATOR']].query(" `TAHUN` == '2,022' "))

    st.subheader('TOTAL RENCANA VS REALISASI PESERTA PER NAMA PELATIHAN')
    realisasi_peserta_by_nama = (
	df.query(" `TAHUN` == '2,022' ").groupby(by=['NAMA']).sum()[['RENCANA PESERTA', 'TOTAL REALISASI PESERTA']].sort_values(by='NAMA')
    )
    st.dataframe(realisasi_peserta_by_nama)
    st.line_chart(data=realisasi_peserta_by_nama, x=['NAMA'], y=['RENCANA PESERTA', 'TOTAL REALISASI PESERTA'], width=0, height=0, use_container_width=True)

    st.subheader('TOTAL RENCANA VS REALISASI JAMLATOR PER NAMA PELATIHAN')
    realisasi_jamlator_by_nama = (
	df.query(" `TAHUN` == '2,021' ").groupby(by=['NAMA']).sum()[['RENCANA JAMLATOR', 'TOTAL JAMLATOR']].sort_values(by='NAMA')
    )
    st.dataframe(realisasi_jamlator_by_nama)
    st.line_chart(data=realisasi_jamlator_by_nama, x=['NAMA'], y=['RENCANA JAMLATOR', 'TOTAL JAMLATOR'], width=0, height=0, use_container_width=True)

    st.subheader('INDEKS KESESUAIAN MATERI')
    kesesuaian_materi = (
	df.query(" `TAHUN` == '2,022' ").groupby(by=['BULAN']).mean()[['KESESUAIAN MATERI']].sort_values(by='BULAN')
    )
    st.dataframe(kesesuaian_materi)
    st.line_chart(data=kesesuaian_materi, x=['BULAN'], y=['KESESUAIAN MATERI'], width=0, height=0, use_container_width=True)

    st.subheader('PESERTA PER STATUS')
    peserta_per_unit = (
	df.query(" `TAHUN` == '2,022' ").groupby(by=['NAMA']).sum()[['TELAH MENGIKUTI/LULUS', 'TIDAK MEMENUHI SYARAT', 'MENGUNDURKAN DIRI',	'TIDAK MENGIKUTI']].sort_values(by='NAMA')
    )
    st.dataframe(peserta_per_unit)
    st.line_chart(data=peserta_per_unit, x=['NAMA'], y=['TELAH MENGIKUTI/LULUS', 'TIDAK MEMENUHI SYARAT', 'MENGUNDURKAN DIRI',	'TIDAK MENGIKUTI'], width=0, height=0, use_container_width=True) 

    st.subheader('PESERTA PER UNIT')
    peserta_per_unit = (
	df.query(" `TAHUN` == '2,022' ").groupby(by=['NAMA']).sum()[['PESERTA SETJEN',	'PESERTA ITJEN',	'PESERTA DJA',	'PESERTA DJP',	'PESERTA DJBC',	'PESERTA DJPb',	'PESERTA DJPK',	'PESERTA DJKN',	'PESERTA DJPPR',	'PESERTA BKF',	'PESERTA BPPK',	'PESERTA LNSW',	'PESERTA KSSK']].sort_values(by='NAMA')
    )
    st.dataframe(peserta_per_unit)
    st.line_chart(data=peserta_per_unit, x=['NAMA'], y=['PESERTA SETJEN',	'PESERTA ITJEN',	'PESERTA DJA',	'PESERTA DJP',	'PESERTA DJBC',	'PESERTA DJPb',	'PESERTA DJPK',	'PESERTA DJKN',	'PESERTA DJPPR',	'PESERTA BKF',	'PESERTA BPPK',	'PESERTA LNSW',	'PESERTA KSSK'], width=0, height=0, use_container_width=True)  

st.subheader('TOTAL RENCANA VS REALISASI PESERTA PER TAHUN')
realisasi_peserta_by_tahun = (
	df.groupby(by=['TAHUN']).sum()[['RENCANA PESERTA', 'TOTAL REALISASI PESERTA']].sort_values(by='TAHUN')
)
st.dataframe(realisasi_peserta_by_tahun, width=1360)
st.bar_chart(data=realisasi_peserta_by_tahun, x=['TAHUN'], y=['RENCANA PESERTA', 'TOTAL REALISASI PESERTA'], width=0, height=0, use_container_width=True)
