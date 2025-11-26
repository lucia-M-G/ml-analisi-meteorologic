import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from utils import cargar_datos, obtener_datos_diarios

# Configuración de rutas absolutas
DIRECTORIO_SCRIPT = os.path.dirname(os.path.abspath(__file__))
RAIZ_PROYECTO = os.path.abspath(os.path.join(DIRECTORIO_SCRIPT, "../../.."))
DIRECTORIO_DATOS = os.path.join(RAIZ_PROYECTO, "analysis/ac06-pandes-al-meteocat-alexandrasofronie_luciamartinez/data")
DIRECTORIO_SALIDA = os.path.join(RAIZ_PROYECTO, "client/public/generated_plots")

# Cargar datos 
print("Cargando datos...")
dataframe_d5 = cargar_datos(os.path.join(DIRECTORIO_DATOS, "Dades_meteorològiques_de_la_XEMA_20251020-D5.csv"))
dataframe_x4 = cargar_datos(os.path.join(DIRECTORIO_DATOS, "Dades_meteorològiques_de_la_XEMA_20251020-X4.csv"))

print("Procesando temperaturas diarias (D5 - Fabra)...")
temperatura_diaria_d5 = obtener_datos_diarios(dataframe_d5, 32, 'media')

print("Procesando temperaturas diarias (X4 - Raval)...")
temperatura_diaria_x4 = obtener_datos_diarios(dataframe_x4, 32, 'media')