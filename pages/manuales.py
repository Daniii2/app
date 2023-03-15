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
p_path = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vR1b55YBjl3Nx619-ZxcA1HFI4I-HKNEkj1e5mF4Ou_44Zttfjn0huUCPluDRdxoeMEZAZVJgU-AqFF/pub?gid=0&single=true&output=csv'
l_path = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vS38H6Hh28X9Xto3k1_TDV4h8GYp5xpYjvCk6Esl4ksp8PdjSFJdBoiP34j30g5-5tJr2upfXFnAGQb/pub?gid=0&single=true&output=csv'
r_path = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTngRA1plSspUHCVtVh5eNJ-yI0kBGL7O204tsCF9D7Wzlkcqv3aW-I1Am7tzW4UsLFKHJ8H7wYD_jj/pub?gid=0&single=true&output=csv'
a_path = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTU-HZRHw6vg2wYcIYZFlNyF7sjYfZTfdJ5RGBdV1y-ix8bCy8HI38zxnMT_e7dpzUMNklHHLBhEXPw/pub?gid=0&single=true&output=csv'
c_path = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSv0ShIcmXQ9-mN_Vr6sZGZExejKYTqs2C22iMGbCwqbI2L_g9G2I4oyAphLmGQG3DM4I75nsc0o3OK/pub?gid=0&single=true&output=csv'
m_path = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vScaT6bvHkLPpetxUalJpZiM-1CF4fH3iKEw0oM4LiE7bhOuOQZ0fvTr20yD7qHYH3mLtgtghoDGyrj/pub?gid=0&single=true&output=csv'

#Manuales
manuales = pd.read_csv(m_path, sep=',', header=0)
manuales['Nombre_Completo'] = manuales['Nombres']+" "+manuales['Apellidos']
manuales = manuales.loc[:, ['Nombre_Completo', 'Num_Documento']]
#Llegadas
llegadas = pd.read_csv(l_path, sep=',', header=0)
llegadas['Mos'] = llegadas['Mos'].astype('int')
llegadas['Mos'] = llegadas['Mos'].astype('string')
llegadas = llegadas.loc[:, ['Mos', 'Referencia']]
llegadas = llegadas.drop_duplicates()
#Recibidos
recibidos = pd.read_csv(r_path, sep=',', header=0)
recibidos = recibidos.dropna()
recibidos['Mos'] = recibidos['Mos'].astype('int')
recibidos['Mos'] = recibidos['Mos'].astype('string')
recibidos = recibidos.merge(manuales, how='left', left_on='Manual', right_on='Nombre_Completo')
recibidos = recibidos.pivot_table(index=['Mes', 'Quincena', 'Mos', 'Num_Documento'], values=['Cantidad'], aggfunc=['count', 'sum']).rename(columns={'count': 'cant_procesos', 'sum': 'cantidad'}).reset_index()
recibidos['recibidos'] = recibidos['cantidad'] / recibidos['cant_procesos'] 
recibidos['recibidos'] = recibidos['recibidos'].astype('int')
recibidos = recibidos.loc[:, ['Mes', 'Quincena', 'Num_Documento', 'Mos', 'recibidos']]
#Asignaciones
asignaciones = pd.read_csv(a_path, sep=',', header=0)
asignaciones = asignaciones.dropna()
asignaciones['Mos'] = asignaciones['Mos'].astype('int')
asignaciones['Mos'] = asignaciones['Mos'].astype('string')
asignaciones = asignaciones.merge(manuales, how='left', left_on='Manual', right_on='Nombre_Completo')
asignaciones = asignaciones.pivot_table(index=['Mes', 'Quincena', 'Mos', 'Num_Documento'], values=['Cantidad'], aggfunc=['sum']).rename(columns={'sum': 'cantidad'}).reset_index()
asignaciones['asignados'] = asignaciones['cantidad']
asignaciones['asignados'] = asignaciones['asignados'].astype('int')
asignaciones = asignaciones.loc[:, ['Mes', 'Quincena', 'Num_Documento', 'Mos', 'asignados']]
#Calidad
calidad = pd.read_csv(c_path, sep=',', header=0)
calidad = calidad.dropna()
calidad['Mos'] = calidad['Mos'].astype('int')
calidad['Mos'] = calidad['Mos'].astype('string')
calidad = calidad.merge(manuales, how='left', left_on='Manual', right_on='Nombre_Completo')
calidad = calidad.pivot_table(index=['Mes', 'Quincena', 'Mos', 'Num_Documento'], values='Aprobadas', aggfunc=['count', 'sum']).rename(columns={'count': 'cant_procesos', 'sum': 'cantidad'}).reset_index()
calidad['aprobadas'] = calidad['cantidad'] / calidad['cant_procesos'] 
calidad['aprobadas'] = calidad['aprobadas'].astype('int')
calidad = calidad.loc[:, ['Mes', 'Quincena', 'Num_Documento', 'Mos', 'aprobadas']]

#Dataframe final
df0 = asignaciones.merge(recibidos, how='left', left_on=['Mes', 'Quincena', 'Num_Documento', 'Mos'], right_on=['Mes', 'Quincena', 'Num_Documento', 'Mos'])
df = df0.merge(calidad, how='left', left_on=['Mes', 'Quincena', 'Num_Documento', 'Mos'], right_on=['Mes', 'Quincena', 'Num_Documento', 'Mos'])
df = df.fillna(0)
df['pendientes'] = df['asignados'] - df['recibidos']
df['devueltas'] = df['recibidos'] - df['aprobadas']
df['Num_Documento'] = df['Num_Documento'].astype('string')
df = df.dropna()

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
data = df[(df['Mes'] == mes) & (df['Quincena'] == quincena) & (df['Num_Documento'] == num_documento)]
data = data.loc[:, ['Num_Documento', 'asignados', 'recibidos', 'pendientes', 'aprobadas', 'devueltas']]

st.dataframe(data)
