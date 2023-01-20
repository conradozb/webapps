# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 17:41:02 2023
pagina1Profesores.py
Control de Cursos. Manejo de profesores.
@author: conza
"""
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.shared import GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
def crud(path):
    '''
    funcion CRUD: Create, Read, Update, Delete archivo csv
    path=ruta absoluta del archivo csv
    '''
    df = pd.read_csv(path)
    #df=pd.read_csv('C:\\Users\\conza\\ControlCursos\\multi\\pages\\Profes.csv')
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
### cuerpo principal del programa donde se pasa el archivo csv como argumento
if __name__ == '__main__':
    # Titulo de la pagina
    st.title('Datos de profesores. Altas, Bajas, Cambios, Consultas')
    # llama a procedimiento para control de datos de profesores
    # funcion CRUD: Create, Remove, UpDate de un archivo csv como parametro
    crud('C:\\Users\\conza\\ControlCursos\\multi\\pages\\Profes3.csv')