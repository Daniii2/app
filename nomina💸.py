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
l_path = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vS38H6Hh28X9Xto3k1_TDV4h8GYp5xpYjvCk6Esl4ksp8PdjSFJdBoiP34j30g5-5tJr2upfXFnAGQb/pub?gid=0&single=true&output=csv'

#Calidad dataframe
calidad = pd.read_csv(c_path, sep=',', header=0)
calidad = calidad.dropna()
calidad['Mos'] = calidad['Mos'].astype('int')
calidad['Mos'] = calidad['Mos'].astype('string')
calidad['IDProceso'] = calidad.Mos+calidad.Proceso
#Procesos
procesos = pd.read_csv(p_path, sep=',', header=0)
procesos = procesos.dropna()
procesos['IDProceso'] = procesos['IDProceso'].astype('string')
#Manuales
manuales = pd.read_csv(m_path, sep=',', header=0)
manuales['Nombre_Completo'] = manuales['Nombres']+' '+manuales['Apellidos']
#Llegadas
llegadas = pd.read_csv(l_path, sep=',', header=0)
llegadas['Mos'] = llegadas['Mos'].astype('int')
llegadas['Mos'] = llegadas['Mos'].astype('string')
llegadas = llegadas.loc[:, ['Mos', 'Referencia']]
llegadas = llegadas.drop_duplicates()
#Merge
df = calidad.merge(manuales, how='inner', left_on=['Manual'], right_on=['Nombre_Completo'])
df2 = df.merge(procesos, how='left', on=['IDProceso'])
df3 = df2.merge(llegadas, how='left', left_on=['Mos_x'], right_on=['Mos'])
#Transformations

df3['Num_Documento'] = df3['Num_Documento'].astype('string')
df3['Valor_Total'] = df3['Aprobadas'] * df3['Costo']

#Mes filter
mes = st.selectbox(
    'Seleccione un mes',
    list(set(df3.Mes)))
st.write('Seleccionaste:', mes)

#Quincena filter
quincena = st.selectbox(
    'Seleccione una quincena',
    list(set(df3.Quincena)))
st.write('Seleccionaste:', quincena)

#Cedula text filter
num_documento = st.text_input("Ingrese el número de documento a consultar", '')
st.write('Ingresaste:', num_documento)

#Applying filters to dataframes
df3 = df3[(df['Mes'] == mes) & (df3['Quincena'] == quincena) & (df3['Num_Documento'] == num_documento)]
data = df3.loc[:, ['Proceso_x', 'Referencia', 'Aprobadas', 'Costo', 'Valor_Total']].rename(columns={'Proceso_x':'Proceso', 'Costo':'Valor_Unidad'})

col1, col2 = st.columns(2)
with col1:
    st.metric(label='Aprobadas', value=data['Aprobadas'].sum().astype('int'))
with col2:
    st.metric(label='Valor_Total', value=data['Valor_Total'].sum().astype('int'))

st.dataframe(data)
