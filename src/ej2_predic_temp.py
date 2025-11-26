import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from utils import cargar_datos, obtener_datos_diarios

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

print("Procesando temperaturas diarias (D5 - Fabra)...")
temperatura_diaria_d5 = obtener_datos_diarios(dataframe_d5, 32, 'media')

print("Procesando temperaturas diarias (X4 - Raval)...")
temperatura_diaria_x4 = obtener_datos_diarios(dataframe_x4, 32, 'media')

historico_d5 = temperatura_diaria_d5[temperatura_diaria_d5.index.year < 2025]
real_2025_d5 = temperatura_diaria_d5[temperatura_diaria_d5.index.year == 2025]

historico_x4 = temperatura_diaria_x4[temperatura_diaria_x4.index.year < 2025]
real_2025_x4 = temperatura_diaria_x4[temperatura_diaria_x4.index.year == 2025]

# Calcular medias mensuales
medias_mensuales_d5 = historico_d5.groupby(historico_d5.index.month).mean()
medias_mensuales_x4 = historico_x4.groupby(historico_x4.index.month).mean()

meses = range(1, 13)
prediccion_d5 = medias_mensuales_d5.values
prediccion_x4 = medias_mensuales_x4.values

# GRÁFICO 1: Predicción vs Realidad para ambas estaciones

figura, (eje1, eje2) = plt.subplots(1, 2, figsize=(14, 5))

# D5 Fabra
eje1.plot(meses, prediccion_d5, 'b--o', label='Predicción')
if not real_2025_d5.empty:
    mensual_real_d5 = real_2025_d5.resample('ME').mean()
    eje1.plot(mensual_real_d5.index.month, mensual_real_d5.values, 'g-s', label='Real 2025')
eje1.set_title('Fabra (D5): Predicción vs Realidad 2025')
eje1.set_xlabel('Mes')
eje1.set_ylabel('Temperatura (°C)')
eje1.set_xticks(meses)
eje1.set_xticklabels(['E', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])
eje1.legend()
eje1.grid(True, alpha=0.3)

# X4 Raval
eje2.plot(meses, prediccion_x4, 'r--o', label='Predicción')
if not real_2025_x4.empty:
    mensual_real_x4 = real_2025_x4.resample('ME').mean()
    eje2.plot(mensual_real_x4.index.month, mensual_real_x4.values, 'orange', marker='s', linestyle='-', label='Real 2025')
eje2.set_title('Raval (X4): Predicción vs Realidad 2025')
eje2.set_xlabel('Mes')
eje2.set_ylabel('Temperatura (°C)')
eje2.set_xticks(meses)
eje2.set_xticklabels(['E', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])
eje2.legend()
eje2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(DIRECTORIO_SALIDA, 'ej2_prediccion_vs_real.png'))
plt.close()

# GRÁFICO 2: Histogramas para ambas estaciones

figura, (eje1, eje2) = plt.subplots(1, 2, figsize=(14, 5))

# Histograma D5 Fabra
eje1.hist(historico_d5.values, bins=30, color='skyblue', edgecolor='black', alpha=0.7, label='Histórico')
if not real_2025_d5.empty:
    eje1.hist(real_2025_d5.values, bins=30, color='orange', edgecolor='black', alpha=0.5, label='Real 2025')
eje1.set_title('Fabra (D5): Distribución Temperaturas')
eje1.set_xlabel('Temperatura (°C)')
eje1.set_ylabel('Días')
eje1.legend()

# Histograma X4 Raval
eje2.hist(historico_x4.values, bins=30, color='lightgreen', edgecolor='black', alpha=0.7, label='Histórico')
if not real_2025_x4.empty:
    eje2.hist(real_2025_x4.values, bins=30, color='coral', edgecolor='black', alpha=0.5, label='Real 2025')
eje2.set_title('Raval (X4): Distribución Temperaturas')
eje2.set_xlabel('Temperatura (°C)')
eje2.set_ylabel('Días')
eje2.legend()

plt.tight_layout()
plt.savefig(os.path.join(DIRECTORIO_SALIDA, 'ej2_histograma_2025.png'))
plt.close()

# GRÁFICO 3: Simulación Noviembre para ambas estaciones

noviembre_historico_d5 = historico_d5[historico_d5.index.month == 11].dropna()
noviembre_historico_x4 = historico_x4[historico_x4.index.month == 11].dropna()

noviembre_simulado_d5 = np.random.choice(noviembre_historico_d5.values, size=30)
noviembre_simulado_x4 = np.random.choice(noviembre_historico_x4.values, size=30)

figura, (eje1, eje2) = plt.subplots(1, 2, figsize=(14, 5))

# Simulación D5 Fabra
eje1.plot(range(1, 31), noviembre_simulado_d5, 'b-x', label='Simulación Nov 2025', linewidth=2, markersize=6)
eje1.set_title('Fabra (D5): Simulación Temperaturas Noviembre 2025')
eje1.set_xlabel('Día')
eje1.set_ylabel('Temperatura (°C)')
eje1.grid(True, alpha=0.3)
eje1.legend()

# Simulación X4 Raval
eje2.plot(range(1, 31), noviembre_simulado_x4, 'r-x', label='Simulación Nov 2025', linewidth=2, markersize=6)
eje2.set_title('Raval (X4): Simulación Temperaturas Noviembre 2025')
eje2.set_xlabel('Día')
eje2.set_ylabel('Temperatura (°C)')
eje2.grid(True, alpha=0.3)
eje2.legend()

plt.tight_layout()
plt.savefig(os.path.join(DIRECTORIO_SALIDA, 'ej2_simulacion_noviembre.png'))
plt.close()