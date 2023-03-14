# streamlit_app.py

import streamlit as st
import pandas as pd
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

#Paths
c_path = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSv0ShIcmXQ9-mN_Vr6sZGZExejKYTqs2C22iMGbCwqbI2L_g9G2I4oyAphLmGQG3DM4I75nsc0o3OK/pub?gid=0&single=true&output=csv'
p_path = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vR1b55YBjl3Nx619-ZxcA1HFI4I-HKNEkj1e5mF4Ou_44Zttfjn0huUCPluDRdxoeMEZAZVJgU-AqFF/pub?gid=0&single=true&output=csv'
m_path = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vScaT6bvHkLPpetxUalJpZiM-1CF4fH3iKEw0oM4LiE7bhOuOQZ0fvTr20yD7qHYH3mLtgtghoDGyrj/pub?gid=0&single=true&output=csv'

#Calidad dataframe
calidad = pd.read_csv(c_path, sep=',', header=0)
calidad = calidad.dropna()
calidad['Mos'] = calidad['Mos'].astype('int')
calidad['Mos'] = calidad['Mos'].astype('string')
calidad['IDProceso'] = calidad.Mos+calidad.Proceso
#Procesos
procesos = pd.read_csv(p_path, sep=',', header=0)
procesos['IDProceso'] = procesos['IDProceso'].astype('string')
#Manuakes
manuales = pd.read_csv(m_path, sep=',', header=0)
manuales['Nombre_Completo'] = manuales['Nombres']+' '+manuales['Apellidos']
#Merge
calidad_p = calidad.merge(procesos, how='left', left_on=['IDProceso'], right_on=['IDProceso'])
df = calidad_p.merge(manuales, how='left', left_on=['Manual'], right_on=['Nombre_Completo'])
#Transformations

df['Num_Documento'] = df['Num_Documento'].astype('string')
df['Valor_Total'] = df['Aprobadas'] * df['Costo']

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
data = df.loc[:, ['Proceso_x', 'Aprobadas', 'Costo', 'Valor_Total']].rename(columns={'Proceso_x':'Proceso', 'Costo':'Valor_Unidad'})

st.metric(data['Aprobadas'].sum())
st.dataframe(data)

