# streamlit_app.py

import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.

def run_query(query):
    df = client.query(query).to_dataframe()
    return df

rows = run_query("SELECT * FROM `digitales-373718.covmaritex.Calidad`")

print(rows)


