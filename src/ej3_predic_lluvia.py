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