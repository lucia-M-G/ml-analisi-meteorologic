import pandas as pd
import numpy as np

def cargar_datos(ruta_archivo):
    """
    Carga los datos desde un archivo CSV
    """
    try:

        columnas_usar = ['CODI_ESTACIO', 'CODI_VARIABLE', 'DATA_LECTURA', 'VALOR_LECTURA']
        dataframe = pd.read_csv(ruta_archivo, usecols=columnas_usar, low_memory=False)
    except ValueError:
        # Si hay error con las columnas, leer todo el archivo
        dataframe = pd.read_csv(ruta_archivo, low_memory=False)
    
    # Convertir VALOR_LECTURA a numérico
    dataframe['VALOR_LECTURA'] = (
        dataframe['VALOR_LECTURA']
        .astype(str)
        .str.replace(',', '.')
        .apply(pd.to_numeric, errors='coerce')
    )
    
    # Parsear DATA_LECTURA a datetime
    try:
        dataframe['DATA_LECTURA'] = pd.to_datetime(
            dataframe['DATA_LECTURA'], 
            format='%d/%m/%Y %I:%M:%S %p',  # Formato: "20/10/2025 03:30:00 PM"
            errors='coerce'
        )
    except:
        # Si falla el formato específico, usar inferencia automática
        dataframe['DATA_LECTURA'] = pd.to_datetime(dataframe['DATA_LECTURA'], errors='coerce')
    
    print(f"Datos cargados: {len(dataframe)} filas")
    return dataframe

def obtener_datos_diarios(dataframe, codigo_variable, agregacion='media'):
    """
    Obtiene datos diarios agregados para una variable específica
    """
    # Filtrar por variable
    dataframe_variable = dataframe[dataframe['CODI_VARIABLE'] == codigo_variable].copy()
    
    if len(dataframe_variable) == 0:
        print(f"Advertencia: No se encontraron datos para la variable {codigo_variable}")
        return pd.Series(dtype=float)
    
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