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

private_gsheets_url = "https://docs.google.com/spreadsheets/d/1lGqAx7sDL0B-nAl1Tlh3aPLWAYfcFdVSS_Y9_aU4VJc/edit?usp=sharing"

[gcp_service_account]
type = "service_account"
project_id = "xxx"
private_key_id = "xxx"
private_key = "xxx"
client_email = "xxx"
client_id = "xxx"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "xxx"

st.title("Data Pelatihan Jarak Jauh 2021 dan 2022")
