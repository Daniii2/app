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
a_path = urlbase+'2PACX-1vTU-HZRHw6vg2wYcIYZFlNyF7sjYfZTfdJ5RGBdV1y-ix8bCy8HI38zxnMT_e7dpzUMNklHHLBhEXPw/pub?gid=0&single=true&output=csv'

#Calidad
calidad = pd.read_csv(c_path, sep=',', header=0)
calidad = calidad.dropna()
calidad['Mos'] = calidad['Mos'].astype('int')
calidad['Mos'] = calidad['Mos'].astype('string')

#Asignaciones
asignaciones = pd.read_csv(a_path, sep=',', header=0)
asignaciones = asignaciones.dropna()
asignaciones['Mos'] = asignaciones['Mos'].astype('int')
asignaciones['Mos'] = asignaciones['Mos'].astype('string')

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
df = asignaciones.merge(calidad, how='left', left_on=['Manual', 'Mos', 'Talla'], right_on=['Manual', 'Mos', 'Talla'])
df2 = df.merge(manuales, how='inner', left_on=['Manual'], right_on=['Nombre_Completo'])
df3 = df.merge(llegadas, how='inner', left_on=['Mos'], right_on=['Mos'])
df3 = df3.loc[:, ['Mes_x', 'Quincena_x', 'Manual', 'Referencia', 'Mos', 'Talla', 'Cantidad', 'Entregadas', 'Aprobadas', 'Devueltas']].rename(
    columns={'Mes_x':'Mes', 'Quincena_x':'Quincena', 'Cantidad':'Asignadas'})
df3 = df3.fillna(0)

#Transformations
df3['Pendientes'] = df3['Asignadas'] - df3['Entregadas']
df3['Mes'] = df3['Mes'].astype('int')
df3['Quincena'] = df3['Quincena'].astype('int')
df3['Asignadas'] = df3['Asignadas'].astype('int')
df3['Entregadas'] = df3['Entregadas'].astype('int')
df3['Aprobadas'] = df3['Aprobadas'].astype('int')
df3['Devueltas'] = df3['Devueltas'].astype('int')
df3['Pendientes'] = df3['Pendientes'].astype('int')

col1, col2 = st.columns(2)
with col1:
    #Mes filter
    manual = st.multiselect(
        'Seleccione una manual/manuales',
        df3['Manual'].sort_values().unique(),
        default = df3['Manual'].sort_values().unique()[0])
    st.write('Seleccionaste:', manual)
with col2:
    #Mos filter
    mos = st.selectbox(
        'Seleccione una Mos',
        list(set(df3.Mos)))
    st.write('Seleccionaste:', mos)

#Applying filters to dataframes
data = df3.loc[(df3['Manual'].isin(manual)) & (df3['Mos'] == mos),
               ['Manual', 'Referencia', 'Mos', 'Talla', 'Asignadas', 'Entregadas', 'Aprobadas', 'Devueltas', 'Pendientes']]

data = data.groupby(['Manual', 'Referencia', 'Mos', 'Talla']).sum().reset_index()

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