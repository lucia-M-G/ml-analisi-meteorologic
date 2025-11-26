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