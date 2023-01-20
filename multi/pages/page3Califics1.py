# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 21:30:47 2023
page3Califics1.py
Control de Cursos. Manejo de profesores
@author: conza
"""
import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 
 
st.title("Calificaciones de estudiantes") 

st.markdown('Esta Streamlit app explora algunas variables de los estudiantes y\
            posibles relaciones entre variables') 

#define seleccion de archivo
grades_file = st.radio("Selecciona el origen de archivo",
                       ("Archivo por defecto","Subir archivo local"))
if grades_file == "Archivo por defecto":
    grades_df = pd.read_csv('C:\\Users\\conza\\ControlCursos\\multi\\pages\\gradedata3.csv')  
if grades_file == "Subir archivo local":    
    grades_file = st.file_uploader('Selecciona archivo CSV') 
    if grades_file is not None: 
    	grades_df = pd.read_csv(grades_file) 
    else: 
    	st.stop()

grafico = st.sidebar.selectbox('Select grafico',
                               ['Histogramas','Dispersion','Barras'])

if grafico == 'Histogramas':
    sns.set_style('darkgrid')
    fig, ax = plt.subplots()
    ax = sns.histplot(grades_df)
    st.pyplot(fig)

if grafico == 'Dispersion':
    selected_x_var = st.selectbox("Selecciona variable 'X' eje abscisas", 
      ['hrs_estudio', 'edad', 'hrs_ejercicio', 'calf1']) 
    selected_y_var = st.selectbox("Selecciona variable 'Y'eje ordenadas", 
      ['calf1', 'hrs_ejercicio', 'hrs_estudio', 'edad'])      
    sns.set_style('darkgrid')
    markers = {"male": "X", "female": "o"}
    fig, ax = plt.subplots() 
    ax = sns.scatterplot(data = grades_df, x = selected_x_var, 
      y = selected_y_var, hue = 'genero',
      markers = markers, style = 'genero'
                         )
      
    plt.xlabel(selected_x_var) 
    plt.ylabel(selected_y_var) 
    plt.title("Grafico de dispersion de variables") 
    st.pyplot(fig)
elif grafico == 'Barras':
    selected_x_var = st.selectbox("Selecciona variable 'X' eje abscisas", 
      ['hrs_estudio', 'edad', 'hrs_ejercicio', 'calf1']) 
    selected_y_var = st.selectbox("Selecciona variable 'Y'eje ordenadas", 
      ['calf1', 'hrs_ejercicio', 'hrs_estudio', 'edad'])      
    sns.set_style('darkgrid')

    fig, ax = plt.subplots() 
    ax = sns.barplot(data = grades_df, x = selected_x_var, 
      y = selected_y_var, hue = 'genero')
    plt.xlabel(selected_x_var) 
    plt.ylabel(selected_y_var) 
    plt.title("Grafico de barras de variables") 
    st.pyplot(fig)

    