import pandas as pd

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
    dataframe['DATA_LECTURA'] = pd.to_datetime(dataframe['DATA_LECTURA'], errors='coerce')
    
    print(f"Datos cargados: {len(dataframe)} filas")
    return dataframe