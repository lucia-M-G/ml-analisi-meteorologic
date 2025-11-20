"""
EJERCICIO 1: COMPARATIVA TEMPERATURAS 2025
Comparar la temperatura media mensual del 2025 entre las estaciones
Fabra (411m del nivel del mar) y Raval (33m del nivel del mar)
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

def cargar_datos():
    # Cargar los archivos CSV desde la carpeta data/
    df_fabra = pd.read_csv('data/D5_Observatori_Fabra.csv')
    df_raval = pd.read_csv('data/X4_Estacio_Raval.csv')
    
    # Cambiar a formato datetime la columna de 'fechas'
    # para poder desglosar en año, mes, etc.
    df_fabra['DATA_LECTURA'] = pd.to_datetime(df_fabra['DATA_LECTURA'])
    df_raval['DATA_LECTURA'] = pd.to_datetime(df_raval['DATA_LECTURA'])
    
    # Devuelver los datos de las estaciones
    return df_fabra, df_raval

if __name__ == "__main__":
    main()