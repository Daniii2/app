# streamlit_app.py

import streamlit as st
import pandas as pd
from PIL import Image
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode

image = Image.open('../pictures/logo.png')

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
a_path = urlbase+'2PACX-1vTU-HZRHw6vg2wYcIYZFlNyF7sjYfZTfdJ5RGBdV1y-ix8bCy8HI38zxnMT_e7dpzUMNklHHLBhEXPw/pub?gid=0&single=true&output=csv'

#Calidad
calidad = pd.read_csv(c_path, sep=',', header=0)
calidad = calidad.dropna()
calidad['Mos'] = calidad['Mos'].astype('int')
calidad['Mos'] = calidad['Mos'].astype('string')
calidad = calidad.loc[:, ['Manual', 'Mos', 'Talla', 'Entregadas', 'Aprobadas', 'Devueltas']].groupby(['Manual', 'Mos', 'Talla']).sum().reset_index()

#Asignaciones
asignaciones = pd.read_csv(a_path, sep=',', header=0)
asignaciones = asignaciones.dropna()
asignaciones['Mos'] = asignaciones['Mos'].astype('int')
asignaciones['Mos'] = asignaciones['Mos'].astype('string')
asignaciones = asignaciones.loc[:, ['Manual', 'Mos', 'Talla', 'Cantidad']].groupby(['Manual', 'Mos', 'Talla']).sum().reset_index()

#Llegadas
llegadas = pd.read_csv(l_path, sep=',', header=0)
llegadas['Mos'] = llegadas['Mos'].astype('int')
llegadas['Mos'] = llegadas['Mos'].astype('string')
llegadas = llegadas.dropna()
llegadas = llegadas.loc[:, ['Mos', 'Referencia', 'Costo_Unidad']]
llegadas = llegadas.drop_duplicates(keep='last')

#Merge
df = asignaciones.merge(calidad, how='left', left_on=['Manual', 'Mos', 'Talla'], right_on=['Manual', 'Mos', 'Talla'])
df2 = df.loc[:, ['Manual', 'Mos', 'Talla', 'Cantidad', 'Entregadas', 'Aprobadas', 'Devueltas']].rename(
    columns={'Cantidad':'Asignadas'})
df3 = df2.fillna(0)

#Transformations
df3['Pendientes'] = df3['Asignadas'] - df3['Entregadas']
df3['Asignadas'] = df3['Asignadas'].astype('int')
df3['Entregadas'] = df3['Entregadas'].astype('int')
df3['Aprobadas'] = df3['Aprobadas'].astype('int')
df3['Devueltas'] = df3['Devueltas'].astype('int')
df3['Pendientes'] = df3['Pendientes'].astype('int')

mos = st.selectbox(
        'Seleccione una Mos',
        df3['Mos'].sort_values().unique())
st.write('Seleccionaste:', mos)

#Applying filters to dataframes
data = df3.loc[df3['Mos']==mos,
               ['Manual', 'Talla', 'Asignadas', 'Entregadas', 'Aprobadas', 'Devueltas', 'Pendientes']]

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label='Asignadas', value=data['Asignadas'].sum().astype('int'))
with col2:
    st.metric(label='Entregadas', value=data['Entregadas'].sum().astype('int'))
with col3:
    st.metric(label='Pendientes', value=data['Pendientes'].sum().astype('int'))
with col4:
    st.metric(label='Devueltas', value=data['Devueltas'].sum().astype('int'))

st.table(data)