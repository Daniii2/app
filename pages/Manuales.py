
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
r_path = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTngRA1plSspUHCVtVh5eNJ-yI0kBGL7O204tsCF9D7Wzlkcqv3aW-I1Am7tzW4UsLFKHJ8H7wYD_jj/pub?gid=0&single=true&output=csv'
a_path = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTU-HZRHw6vg2wYcIYZFlNyF7sjYfZTfdJ5RGBdV1y-ix8bCy8HI38zxnMT_e7dpzUMNklHHLBhEXPw/pub?gid=0&single=true&output=csv'
#Manuales
manuales = pd.read_csv(m_path, sep=',', header=0)
manuales['Nombre_Completo'] = manuales['Nombres']+' '+manuales['Apellidos']
#Llegadas
llegadas = pd.read_csv(l_path, sep=',', header=0)
llegadas['Mos'] = llegadas['Mos'].astype('int')
llegadas['Mos'] = llegadas['Mos'].astype('string')
#Recibidos
recibidos = pd.read_csv(r_path, sep=',', header=0)
recibidos['Mos'] = recibidos['Mos'].astype('int')
recibidos['Mos'] = recibidos['Mos'].astype('string')
#Asignaciomes
asignaciones = pd.read_csv(a_path, sep=',', header=0)
asignaciones['Mos'] = asignaciones['Mos'].astype('int')
asignaciones['Mos'] = asignaciones['Mos'].astype('string')
#Merge

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
data = df.loc[:, ['Proceso_x', 'Referencia', 'Aprobadas', 'Costo', 'Valor_Total']].rename(columns={'Proceso_x':'Proceso', 'Costo':'Valor_Unidad'})

col1, col2 = st.columns(2)
with col1:
    st.metric(label='Aprobadas', value=data['Aprobadas'].sum().astype('int'))
with col2:
    st.metric(label='Valor_Total', value=data['Valor_Total'].sum().astype('int'))

st.dataframe(data)

