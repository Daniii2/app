# streamlit_app.py

import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
from PIL import Image

image = Image.open('pictures/logo.png')
st.image(image)

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

# Perform query.
sql = """
    SELECT * 
    FROM `digitales-373718.covmaritex.Calidad`
    """

df = client.query(sql).to_dataframe()

st.dataframe(df)
