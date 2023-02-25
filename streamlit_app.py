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
    SELECT E.Num_Documento, C.*, ROUND(P.Costo, 0) AS Valor_Unidad, ROUND((C.Aprobadas * P.Costo), 0) AS Valor_Total, EXTRACT(MONTH FROM C.Fecha) AS Mes,
    CASE WHEN EXTRACT(DAY FROM C.Fecha) <=15 THEN 'Q1' ELSE 'Q2' END AS Quincena,
    FROM `digitales-373718.covmaritex.Calidad` AS C
    JOIN covmaritex.Procesos AS P
    ON C.Mos = P.Mos AND C.Proceso = P.Proceso
    JOIN covmaritex.Empleados AS E
    ON C.Manual = E.Nombre_Completo
    """

df = client.query(sql).to_dataframe()
df2 = df.loc[:, ['Proceso', 'Aprobadas', 'Valor_Unidad', 'Valor_Total']]

st.dataframe(df2)
