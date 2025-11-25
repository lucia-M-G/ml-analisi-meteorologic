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
    df_fabra = pd.read_csv('data/D5_Observatori_Fabra.csv', dtype={'VALOR_LECTURA': str})
    df_raval = pd.read_csv('data/X4_Estacio_Raval.csv', dtype={'VALOR_LECTURA': str})
    return df_fabra, df_raval

def convertir_fechas(df_fabra, df_raval):
    # Convierte las columnas de fecha a datetime
    df_fabra['DATA_LECTURA'] = pd.to_datetime(df_fabra['DATA_LECTURA'], format='mixed')
    df_raval['DATA_LECTURA'] = pd.to_datetime(df_raval['DATA_LECTURA'], format='mixed')