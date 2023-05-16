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

urlbase = 'https://docs.google.com/spreadsheets/d/e/'

#Paths
c_path = urlbase+'2PACX-1vQo8wOJniN1sffDtpuQO8hT3EdrYB9YzJEoBPVNjnbfYi2Vq4aDgw8SEo51zDD0HLH5NmIKbvsWKYzB/pub?gid=0&single=true&output=csv'
m_path = urlbase+'2PACX-1vScaT6bvHkLPpetxUalJpZiM-1CF4fH3iKEw0oM4LiE7bhOuOQZ0fvTr20yD7qHYH3mLtgtghoDGyrj/pub?gid=0&single=true&output=csv'
l_path = urlbase+'2PACX-1vS38H6Hh28X9Xto3k1_TDV4h8GYp5xpYjvCk6Esl4ksp8PdjSFJdBoiP34j30g5-5tJr2upfXFnAGQb/pub?gid=0&single=true&output=csv'

#Calidad
calidad = pd.read_csv(c_path, sep=',', header=0)
calidad = calidad.dropna()
calidad['Mos'] = calidad['Mos'].astype('int')
calidad['Mos'] = calidad['Mos'].astype('string')

#Manuales
manuales = pd.read_csv(m_path, sep=',', header=0)
manuales['Nombre_Completo'] = manuales['Nombres']+' '+manuales['Apellidos']
manuales = manuales.dropna()
manuales = manuales.drop_duplicates(keep='last')
manuales = manuales.loc[:, ['Nombre_Completo', 'Num_Documento']]

#Llegadas
llegadas = pd.read_csv(l_path, sep=',', header=0)
llegadas['Mos'] = llegadas['Mos'].astype('int')
llegadas['Mos'] = llegadas['Mos'].astype('string')
llegadas = llegadas.dropna()
llegadas = llegadas.loc[:, ['Mos', 'Referencia', 'Costo_Unidad']]
llegadas = llegadas.drop_duplicates(keep='last')

#Merge
df = calidad.merge(manuales, how='inner', left_on=['Manual'], right_on=['Nombre_Completo'])
df2 = df.merge(llegadas, how='inner', left_on=['Mos'], right_on=['Mos'])

#Transformations

df2['Num_Documento'] = df2['Num_Documento'].astype('string')
df2['Valor_Total'] = df2['Aprobadas'] * df2['Costo_Unidad']
df2['Mes'] = df2['Mes'].astype('int')
df2['Quincena'] = df2['Quincena'].astype('int')

#Mes filter
mes = st.selectbox(
    'Seleccione un mes',
    list(set(df2.Mes)))
st.write('Seleccionaste:', mes)

#Quincena filter
quincena = st.selectbox(
    'Seleccione una quincena',
    list(set(df2.Quincena)))
st.write('Seleccionaste:', quincena)


#Applying filters to dataframes
data = df2.loc[(df2['Mes'] == mes) & (df2['Quincena'] == quincena), 
              ['Manual', 'Referencia', 'Aprobadas', 'Costo_Unidad', 'Valor_Total']].rename(columns={'Costo_Unidad':'Valor_Unidad', 'Aprobadas':'Unidades'})

data = data.groupby(['Referencia','Valor_Unidad']).sum().reset_index()

col1, col2 = st.columns(2)
with col1:
    st.metric(label='Unidades', value=data['Unidades'].sum().astype('int'))
with col2:
    st.metric(label='Valor_Total', value='$'+data['Valor_Total'].sum().astype('int').astype('str'))

data['Valor_Unidad'] = data['Valor_Unidad'].astype('int')
data['Valor_Total'] = data['Valor_Total'].astype('int')

st.table(data)

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(data)

st.download_button(
    label="Descargar nómina",
    data=csv,
    file_name=f'nomina.csv',
    mime='text/csv',
)