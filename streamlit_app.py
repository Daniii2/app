# streamlit_app.py

import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
from PIL import Image
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode

image = Image.open('pictures/logo.png')

col1, col2, col3 = st.columns(3)
with col1:
    st.write(' ')
with col2:
    st.image(image)
with col3:
    st.write(' ')

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

# Perform query.
sql = """
    SELECT E.Num_Documento, C.*, P.Costo AS Valor_Unidad, (C.Aprobadas * P.Costo) AS Valor_Total, EXTRACT(MONTH FROM C.Fecha) AS Mes,
    CASE WHEN EXTRACT(DAY FROM C.Fecha) <=15 THEN 'Q1' ELSE 'Q2' END AS Quincena,
    FROM `digitales-373718.covmaritex.Calidad` AS C
    JOIN covmaritex.Procesos AS P
    ON C.Mos = P.Mos AND C.Proceso = P.Proceso
    JOIN covmaritex.Empleados AS E
    ON C.Manual = E.Nombre_Completo
    """

#Transform query to pandas dataframe
df = client.query(sql).to_dataframe()
df['Num_Documento'] = df['Num_Documento'].astype('string')
df['Valor_Unidad'] = df['Valor_Unidad'].astype('int64')
df['Valor_Total'] = df['Valor_Total'].astype('int64')

#Mes filter
mes = st.selectbox(
    'Seleccione un mes',
    list(set(df.Mes)))
st.write('Seleccionaste:', mes)

#Quincena filter
quincena = st.selectbox(
    'Seleccione una quincena',
    list(set(df.Quincena)))
st.write('Seleccionaste:', quincena)

#Cedula text filter
num_documento = st.text_input("Ingrese el número de documento a consultar", '')
st.write('Ingresaste:', num_documento)

#Applying filters to dataframes
df = df[(df['Mes'] == mes) & (df['Quincena'] == quincena) & (df['Num_Documento'] == num_documento)]
data = df.loc[:, ['Proceso', 'Aprobadas', 'Valor_Unidad', 'Valor_Total']]

st.dataframe(data)

