import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from utilidades import cargar_datos, obtener_datos_diarios

# Configuración de rutas absolutas
DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
DIRECTORIO_DATOS = os.path.join(DIRECTORIO_ACTUAL, "../data")
DIRECTORIO_SALIDA = os.path.join(DIRECTORIO_ACTUAL, "graficos_generados")

# Crear directorio de salida si no existe
os.makedirs(DIRECTORIO_SALIDA, exist_ok=True)

# Cargar datos
print("Cargando datos...")
dataframe_d5 = cargar_datos(os.path.join(DIRECTORIO_DATOS, "Dades_meteorològiques_de_la_XEMA_20251020-D5.csv"))
dataframe_x4 = cargar_datos(os.path.join(DIRECTORIO_DATOS, "Dades_meteorològiques_de_la_XEMA_20251020-X4.csv"))

# Obtener precipitación diaria
print("Procesando Precipitación Diaria...")
precipitacion_diaria_d5 = obtener_datos_diarios(dataframe_d5, 35, 'suma')
precipitacion_diaria_x4 = obtener_datos_diarios(dataframe_x4, 35, 'suma')

historico_d5 = precipitacion_diaria_d5[precipitacion_diaria_d5.index.year < 2025]
real_2025_d5 = precipitacion_diaria_d5[precipitacion_diaria_d5.index.year == 2025]

historico_x4 = precipitacion_diaria_x4[precipitacion_diaria_x4.index.year < 2025]
real_2025_x4 = precipitacion_diaria_x4[precipitacion_diaria_x4.index.year == 2025]

# Analizar correlaciones

def analizar_correlaciones(dataframe, precipitacion_diaria):
    variables_interes = [(32, 'Temperatura'), (33, 'Humedad'), (36, 'Presión')]
    correlaciones = {}
    
    for codigo_variable, nombre_variable in variables_interes:
        try:
            variable_diaria = obtener_datos_diarios(dataframe, codigo_variable, 'media')
            ppt_alineado, var_alineado = precipitacion_diaria.align(variable_diaria, join='inner')
            
            if len(ppt_alineado) > 10:
                correlacion = ppt_alineado.corr(var_alineado)
                correlaciones[codigo_variable] = correlacion
                print(f"  {nombre_variable}: {correlacion:.3f}")
        except:
            pass
    
    return correlaciones  

print("\nCorrelaciones D5 (Fabra):")
correlaciones_d5 = analizar_correlaciones(dataframe_d5, precipitacion_diaria_d5)

print("Correlaciones X4 (Raval):")
correlaciones_x4 = analizar_correlaciones(dataframe_x4, precipitacion_diaria_x4)  

# Algoritomo predicción

def predecir_precipitacion(historico):
    historico_df = pd.DataFrame({
        'fecha': historico.index,
        'dia_año': historico.index.dayofyear,
        'precipitacion': historico.values
    })
    
    predicciones = []
    for dia in range(1, 366):
        datos_dia = historico_df[historico_df['dia_año'] == dia]
        
        if len(datos_dia) > 0:
            prob_lluvia = (datos_dia['precipitacion'] > 0).mean()
            media_lluvia = datos_dia[datos_dia['precipitacion'] > 0]['precipitacion'].mean()
            
            if np.random.random() < prob_lluvia:
                variacion = np.random.normal(0, media_lluvia * 0.3)
                prediccion = max(0.1, media_lluvia + variacion)
            else:
                prediccion = 0.0
        else:
            prediccion = 0.0
            
        predicciones.append(prediccion)
    
    return predicciones