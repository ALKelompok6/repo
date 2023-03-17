# Core Pkgs
import streamlit as st
import plotly.express as px
# sklearn version = 0.24.2

# EDA Pkgs
import pandas as pd
import numpy as np
import seaborn as sns
st.set_option('deprecation.showPyplotGlobalUse', False)

# Utils
import joblib

# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

df = load_data(st.secrets["https://docs.google.com/spreadsheets/d/1ZbSoBVO9Z5hC88Gs06DJCSzo7fufr317ZbqmM6lCUMw/edit?usp=sharing"])

# Print results.
for row in df.itertuples():
    st.write(f"{row.name} has a :{row.pet}:")
st.title("Data Pelatihan Jarak Jauh 2021 dan 2022")
