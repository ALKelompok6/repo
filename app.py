# Core Pkgs
import streamlit as st
import plotly.express as px
# sklearn version = 0.24.2

# EDA Pkgs
import pandas as pd
import numpy as np
import seaborn as sns
st.set_option('deprecation.showPyplotGlobalUse', False)

#coba
# Utils
import joblib

# Image
from PIL import Image

# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

df = load_data(st.secrets["public_gsheets_url"])

st.title("Data Pelatihan 2021 dan 2022 Pusat Pendidikan dan Pelatihan Kepemimpinan dan Manajerial")
st.dataframe(df.head())
    all_columns = df.columns.to_list()
    columns_to_plot = st.selectbox("Select Column for Histogram", all_columns)
    hist_plot = df[columns_to_plot].plot.hist()
    st.write(hist_plot)
    st.pyplot()