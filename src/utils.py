"""
Módulo con funciones auxiliares para el ejercicio 1
"""

import pandas as pd
# Para poder crear la carpeta para los gráficos 
import os

def crear_carpeta_outputs():
    # Crea la carpeta outputs si no existe
    os.makedirs('outputs', exist_ok=True)

def cargar_datos():
    df_fabra = pd.read_csv('data/Dades_meteorològiques_de_la_XEMA_20251020-D5.csv', dtype={'VALOR_LECTURA': str})
    df_raval = pd.read_csv('data/Dades_meteorològiques_de_la_XEMA_20251020-X4.csv', dtype={'VALOR_LECTURA': str})
    return df_fabra, df_raval

def convertir_fechas(df_fabra, df_raval):
    # Convierte las columnas de fecha a datetime
    df_fabra['DATA_LECTURA'] = pd.to_datetime(df_fabra['DATA_LECTURA'], format='mixed')
    df_raval['DATA_LECTURA'] = pd.to_datetime(df_raval['DATA_LECTURA'], format='mixed')

def filtrar_temperaturas_2025(df_fabra, df_raval):
    temp_fabra = df_fabra[
        (df_fabra['CODI_VARIABLE'] == 32) & 
        (df_fabra['DATA_LECTURA'].dt.year == 2025)
    ].copy()
    
    temp_raval = df_raval[
        (df_raval['CODI_VARIABLE'] == 32) & 
        (df_raval['DATA_LECTURA'].dt.year == 2025)
    ].copy()
    
    # Convertir a num
    temp_fabra['VALOR_LECTURA'] = pd.to_numeric(temp_fabra['VALOR_LECTURA'], errors='coerce')
    temp_raval['VALOR_LECTURA'] = pd.to_numeric(temp_raval['VALOR_LECTURA'], errors='coerce')
    
    # Devuelve una tupla de los DataFrames filtrados de Fabra y Raval
    return temp_fabra, temp_raval

def calcular_temperatura_mensual(temp_fabra, temp_raval):
    temp_fabra['MES'] = temp_fabra['DATA_LECTURA'].dt.month
    temp_raval['MES'] = temp_raval['DATA_LECTURA'].dt.month
    
    media_fabra = temp_fabra.groupby('MES')['VALOR_LECTURA'].mean()
    media_raval = temp_raval.groupby('MES')['VALOR_LECTURA'].mean()
    
    # Devuelve una tupla de las series con medias mensuales de Fabra y Raval
    return media_fabra, media_raval

def obtener_datos_diarios(dataframe, codigo_variable, agregacion='media'):
    # Filtrar por variable
    dataframe_variable = dataframe[dataframe['CODI_VARIABLE'] == codigo_variable].copy()
    
    if len(dataframe_variable) == 0:
        print(f"Advertencia: No se encontraron datos para la variable {codigo_variable}")
        return pd.Series(dtype=float)
    
    # Pasar a num
    dataframe_variable['VALOR_LECTURA'] = (
        dataframe_variable['VALOR_LECTURA']
        .astype(str)
        # Reemplazar comas por puntos
        .str.replace(',', '.') 
        # Convertir a número
        .apply(pd.to_numeric, errors='coerce')
    )

    # Configurar índice de tiempo
    dataframe_variable.dropna(subset=['DATA_LECTURA'], inplace=True)
    dataframe_variable.set_index('DATA_LECTURA', inplace=True)
   
    if agregacion == 'media':
        diario = dataframe_variable['VALOR_LECTURA'].resample('D').mean()
    elif agregacion == 'suma':
        diario = dataframe_variable['VALOR_LECTURA'].resample('D').sum()
    else:
        diario = dataframe_variable['VALOR_LECTURA'].resample('D').mean()
    
    print(f"Datos diarios para variable {codigo_variable}: {len(diario)} días")
    return diario