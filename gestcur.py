# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 00:54:27 2023
gestcur.py
@author: conza
Control de Cursos. Manejo de profesores.
"""
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.shared import GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import matplotlib.pyplot as plt 
import seaborn as sns 

st.title('Pagina prototipo de gestion de cursos')
st.header("Aplicacion web creada con Python 3.9.15, Streamlit 1.11 y \
          ag-grid 18.0.1, bajo entorno de Windows 10 e\
              IDE Spyder 5.3.3 de Anaconda Navigator 2.3.2")             
st.subheader("Codigo adaptado del libro:\
             Khorasani, M., Abdou, M., & Hernández Fernández, J. (2022).\
                 Web Application Development with Streamlit:\
                     Develop and Deploy Secure and Scalable Web Applications\
                         to the Cloud Using a Pure Python Framework. Apress.")
st.subheader("Utiliza archivos 'csv' para almacenamiento de datos")



def crud(path):
    '''
    funcion CRUD: Create, Read, Update, Delete archivo csv
    path=ruta absoluta del archivo csv
    '''
    df = pd.read_csv(path)
    df = df.fillna('None') #llena los campos vacios con 'none'
    index = len(df) #obtiene el numero de renglones como referencia de indice
    ### Initiate the streamlit-aggrid widget
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_side_bar()
    gb.configure_default_column(groupable=True, value=True,
                                enableRowGroup=True, aggFunc="sum",
                                editable=True)
    gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    gridOptions = gb.build()
    ### Insert the dataframe into the widget
    df_new = AgGrid(df,gridOptions=gridOptions,
                    enable_enterprise_modules=True,
                    update_mode=GridUpdateMode.MODEL_CHANGED)
    st.write("Numero total de renglones",index)
    st.info('Para cambios, editar directamente en el renglon y columna deseados')
    ### Add a new row to the widget
    if st.button('---Adiciona nuevo renglon al final de la tabla\
                  para crear nuevo registro---'):
        df_new['data'].loc[index,:] = 'None'
        df_new['data'].to_csv(path,index=False)
        st.experimental_rerun()
    ### Save the dataframe to disk if the widget has been modified
    if df.equals(df_new['data']) is False:
        df_new['data'].to_csv(path,index=False)
        st.experimental_rerun()
    ### Remove selected rows from the widget
    if st.button('----Elimina renglones seleccionados---'):
        if len(df_new['selected_rows']) > 0:
            #
            exclude = pd.DataFrame(df_new['selected_rows'])
            pd.merge(df_new['data'],
                     exclude,
                     how='outer',
                     indicator=True).query('_merge == "left_only"').drop('_merge', 1).to_csv(path, index=False)
            st.experimental_rerun()
        else:
            st.warning('Please select at least one row')
    ### Check for duplicate rows
    if (df_new['data'].duplicated().sum()) > 0:
        st.warning("Se detectaron renglones o registros duplicados.\
                     Numero de renglones duplicados: %s" % \
                         (df_new['data'].duplicated().sum()))
        if st.button('---Elimina renglones duplicados---'):
            #df_new['data'] = df_new['data'].drop_duplicates()
            df_new['data'].drop_duplicates(inplace=True)
            df_new['data'].to_csv(path,index=False)
            st.experimental_rerun()


#Defining Columns
col1, col2 = st.columns(2)

with col1:
    CRUD1 = st.selectbox("Selecciona datos de trabajo:",
                         ['Profesores','Alumnos'])
    if (CRUD1 == 'Profesores'):
        st.title('Datos de profesores. Altas, Bajas, Cambios, Consultas')
        # llama a procedimiento para control de datos de profesores
        # funcion CRUD: Create, Remove, UpDate de un archivo csv como parametro
        crud('/app/webapps/Profes3.csv')
        
with col2:
    st.title("Calificaciones de estudiantes") 

    st.markdown('Esta Streamlit app explora algunas variables de los estudiantes y\
                posibles relaciones entre variables') 
                
    grafalumns = st.selectbox("Selecciona grafico sobre alumnos:",
                               ['Histograma','Dispersion',
                                'Barras'])
    if (grafalumns == 'Histograma'):
        grades_df = pd.read_csv('/app/webapps/gradedata3.csv')  
        sns.set_style('darkgrid')
        fig, ax = plt.subplots()
        ax = sns.histplot(grades_df)
        st.pyplot(fig)
    
    elif (grafalumns == 'Dispersion'):
        grades_df = pd.read_csv('/app/webapps/gradedata3.csv')  
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
    
    elif (grafalumns == 'Barras'):
        grades_df = pd.read_csv('/app/webapps/gradedata3.csv')  
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
        
