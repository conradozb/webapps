# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 00:54:27 2023
gestcur.py
@author: conza
Control de Cursos. Manejo de profesores.
"""
#ST_WSUAMI3.py
# This program use the screped csv file created by WSUAMI3.py

import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.shared import GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import matplotlib.pyplot as plt 
import seaborn as sns 

st.title('Muestra datos de profesores de la UAM Iztapalapa previamente\
         obtenidos por web scraping')
#st.subtitle('Estos datos pueden ser modificados')
st.subheader("Utiliza archivos 'csv' para tratamiento de datos")
st.subheader("No se incluye opcion para recopilar nuevamente los datos de:\
             https://covia.izt.uam.mx/investigadores/investigador/")



def crud(path):
    '''
    funcion crud: Create, Read, Update, Delete on csv file
    path=ruta absoluta del archivo csv
    '''
    df = pd.read_csv(path)
    df = df.fillna('None') #llena los campos vacios con 'none'
    index = len(df) #obtiene el numero de renglones como referencia de indice
    ### Initiate the streamlit-aggrid widget
    st.write("Numero total de renglones",index)
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_side_bar()
    gb.configure_pagination(enabled=True,
                            paginationAutoPageSize=False,
                            paginationPageSize=15)
    gb.configure_default_column(groupable=True, value=True,
                                enableRowGroup=True, aggFunc="sum",
                                editable=True)
    gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    gridOptions = gb.build()
    ### Insert the dataframe into the widget
    df_new = AgGrid(df,gridOptions=gridOptions,
                    enable_enterprise_modules=True,
                    update_mode=GridUpdateMode.MODEL_CHANGED)
    
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


eleccion = st.radio("Selecciona tu eleccion",
                    ("CRUD Profesores", "Graficos exploratorios"))

path='UAMI_profs_copy.csv'

if (eleccion == 'CRUD Profesores'):
    st.title('Profesores: Altas, Bajas, Cambios, Consultas')
    # llama a procedimiento para control de datos de profesores
    # funcion CRUD: Create, Remove, UpDate de un archivo csv como parametro
    crud(path)

elif (eleccion == 'Graficos exploratorios'):        
    st.title("Graficos de exploratorios sobre profesores de la UAMI") 
    st.markdown('Esta Streamlit app explora algunos datos de profesores') 
    grpr_df = pd.read_csv(path) 
    
    selected_x_var = st.selectbox("Selecciona variable 'X' eje abscisas", 
      ['Grado', 'División', 'Departamento']) 
    sns.set_style('darkgrid')

    fig, ax = plt.subplots() 
    ax = sns.countplot(data = grpr_df, x = selected_x_var)
    plt.xlabel(selected_x_var)
    plt.xticks(rotation=90)
    ax.bar_label(ax.containers[0]) # to display count
    plt.title("Numero de ocurrencias (profesores) en variable seleccionada") 
    st.pyplot(fig)
                
        