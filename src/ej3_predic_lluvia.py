import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from utils import cargar_datos, convertir_fechas, obtener_datos_diarios
from analisis import mostrar_info_datos

# Configuración de rutas absolutas
DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
DIRECTORIO_DATOS = os.path.join(DIRECTORIO_ACTUAL, "../data")
DIRECTORIO_SALIDA = os.path.join(DIRECTORIO_ACTUAL, "../outputs")

# Crear directorio de salida si no existe
os.makedirs(DIRECTORIO_SALIDA, exist_ok=True)

def main():
    print("EJERCICIO 3: PREDICCIÓN DE LLUVIA 2025")
    print("=" * 60)
    
    print("Cargando datos...")
    df_fabra, df_raval = cargar_datos()

    print("\nExplorando datos...")
    mostrar_info_datos(df_fabra, df_raval)
    
    print("\nConvirtiendo fechas...")
    convertir_fechas(df_fabra, df_raval)
    
    print("Procesando precipitación diaria...")
    precipitacion_diaria_d5 = obtener_datos_diarios(df_fabra, 35, 'suma')
    precipitacion_diaria_x4 = obtener_datos_diarios(df_raval, 35, 'suma')
    
    historico_d5 = precipitacion_diaria_d5[precipitacion_diaria_d5.index.year < 2025]
    real_2025_d5 = precipitacion_diaria_d5[precipitacion_diaria_d5.index.year == 2025]
    
    historico_x4 = precipitacion_diaria_x4[precipitacion_diaria_x4.index.year < 2025]
    real_2025_x4 = precipitacion_diaria_x4[precipitacion_diaria_x4.index.year == 2025]
    
    # Analizar
    print("\nAnalizando correlaciones...")
    correlaciones_d5 = analizar_correlaciones(df_fabra, precipitacion_diaria_d5)
    correlaciones_x4 = analizar_correlaciones(df_raval, precipitacion_diaria_x4)
    
    # Prediciones
    print("\nGenerando predicciones 2025...")
    fechas_2025 = pd.date_range(start='2025-01-01', end='2025-12-31', freq='D')
    
    prediccion_2025_d5 = pd.Series(predecir_precipitacion(historico_d5)[:len(fechas_2025)], index=fechas_2025)
    prediccion_2025_x4 = pd.Series(predecir_precipitacion(historico_x4)[:len(fechas_2025)], index=fechas_2025)
    
    # Gráficos
    crear_diagramas_sectores(prediccion_2025_d5, prediccion_2025_x4)
    crear_barras_verticales(prediccion_2025_d5, prediccion_2025_x4)
    crear_barras_horizontales(prediccion_2025_d5, prediccion_2025_x4)
    
    # Precisión
    print("\nCalculando precisión...")
    precision_d5, pred_lluvia_d5, real_lluvia_d5, total_d5 = calcular_precision(prediccion_2025_d5, real_2025_d5)
    precision_x4, pred_lluvia_x4, real_lluvia_x4, total_x4 = calcular_precision(prediccion_2025_x4, real_2025_x4)
    
    mostrar_resultados_precision(precision_d5, pred_lluvia_d5, real_lluvia_d5, total_d5,
                               precision_x4, pred_lluvia_x4, real_lluvia_x4, total_x4)

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

def crear_diagramas_sectores(pred_d5, pred_x4):
    print("Creando diagramas de sectores...")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Fabra (D5)
    lluvia_d5 = (pred_d5 > 0).sum()
    no_lluvia_d5 = (pred_d5 == 0).sum()
    ax1.pie([lluvia_d5, no_lluvia_d5], labels=['Llueve', 'No Llueve'], 
            autopct='%1.1f%%', colors=['lightblue', 'gold'])
    ax1.set_title('Fabra (D5): Días de Lluvia 2025')
    
    # Raval (X4)
    lluvia_x4 = (pred_x4 > 0).sum()
    no_lluvia_x4 = (pred_x4 == 0).sum()
    ax2.pie([lluvia_x4, no_lluvia_x4], labels=['Llueve', 'No Llueve'], 
            autopct='%1.1f%%', colors=['lightgreen', 'gold'])
    ax2.set_title('Raval (X4): Días de Lluvia 2025')
    
    plt.tight_layout()
    plt.savefig(os.path.join(DIRECTORIO_SALIDA, 'ej3_diagrama_sectores_lluvia.png'))
    plt.show()

def crear_barras_verticales(pred_d5, pred_x4):
    print("Creando gráficos de barras verticales...")
    
    meses_nombres = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    
    # Fabra (D5)
    fig, axes = plt.subplots(4, 3, figsize=(15, 12))
    fig.suptitle('Fabra (D5): Precipitación Diaria 2025')
    for i, ax in enumerate(axes.flat):
        mes = i + 1
        datos_mes = pred_d5[pred_d5.index.month == mes]
        ax.bar(datos_mes.index.day, datos_mes.values, color='blue', alpha=0.7)
        ax.set_title(meses_nombres[mes-1])
        ax.set_ylabel('mm')
        ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(DIRECTORIO_SALIDA, 'ej3_barras_verticales_d5.png'))
    plt.show()
    
    # Raval (X4)
    fig, axes = plt.subplots(4, 3, figsize=(15, 12))
    fig.suptitle('Raval (X4): Precipitación Diaria 2025')
    for i, ax in enumerate(axes.flat):
        mes = i + 1
        datos_mes = pred_x4[pred_x4.index.month == mes]
        ax.bar(datos_mes.index.day, datos_mes.values, color='green', alpha=0.7)
        ax.set_title(meses_nombres[mes-1])
        ax.set_ylabel('mm')
        ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(DIRECTORIO_SALIDA, 'ej3_barras_verticales_x4.png'))
    plt.show()

def crear_barras_horizontales(pred_d5, pred_x4):
    print("Creando gráficos de barras horizontales...")
    
    meses_nombres = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    
    # Fabra (D5)
    fig, axes = plt.subplots(4, 3, figsize=(15, 12))
    fig.suptitle('Fabra (D5): Precipitación Diaria 2025')
    for i, ax in enumerate(axes.flat):
        mes = i + 1
        datos_mes = pred_d5[pred_d5.index.month == mes]
        ax.barh(datos_mes.index.day, datos_mes.values, color='blue', alpha=0.7)
        ax.set_title(meses_nombres[mes-1])
        ax.set_xlabel('mm')
        ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(DIRECTORIO_SALIDA, 'ej3_barras_horizontales_d5.png'))
    plt.show()
    
    # Raval (X4)
    fig, axes = plt.subplots(4, 3, figsize=(15, 12))
    fig.suptitle('Raval (X4): Precipitación Diaria 2025')
    for i, ax in enumerate(axes.flat):
        mes = i + 1
        datos_mes = pred_x4[pred_x4.index.month == mes]
        ax.barh(datos_mes.index.day, datos_mes.values, color='green', alpha=0.7)
        ax.set_title(meses_nombres[mes-1])
        ax.set_xlabel('mm')
        ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(DIRECTORIO_SALIDA, 'ej3_barras_horizontales_x4.png'))
    plt.show()

def calcular_precision(prediccion, real):
    fechas_comunes = real.index.intersection(prediccion.index)
    if len(fechas_comunes) == 0:
        return 0, 0, 0, 0
    
    pred_comun = prediccion.loc[fechas_comunes]
    real_comun = real.loc[fechas_comunes]
    
    pred_bin = (pred_comun > 0)
    real_bin = (real_comun > 0)
    
    aciertos = (pred_bin == real_bin).sum()
    precision = (aciertos / len(fechas_comunes)) * 100

    # Calcular días con lluvia
    dias_predicho_lluvia = pred_bin.sum()
    dias_real_lluvia = real_bin.sum()
    
    return precision, dias_predicho_lluvia, dias_real_lluvia, len(fechas_comunes)

def mostrar_resultados_precision(precision_d5, pred_lluvia_d5, real_lluvia_d5, total_d5,
                               precision_x4, pred_lluvia_x4, real_lluvia_x4, total_x4):
    print(f"\nPrecisión de la predicción:")
    print(f"Fabra (D5): {precision_d5:.1f}%")
    print(f"  - Días predichos con lluvia: {pred_lluvia_d5}")
    print(f"  - Días reales con lluvia: {real_lluvia_d5}")
    print(f"  - Días analizados: {total_d5}")
    
    print(f"Raval (X4): {precision_x4:.1f}%")
    print(f"  - Días predichos con lluvia: {pred_lluvia_x4}")
    print(f"  - Días reales con lluvia: {real_lluvia_x4}")
    print(f"  - Días analizados: {total_x4}")
    
    # Guardar en archivo de texto
    with open(os.path.join(DIRECTORIO_SALIDA, 'ej3_resultados_precision.txt'), 'w', encoding='utf-8') as f:
        f.write(f"Fabra (D5): {precision_d5:.1f}%\n")
        f.write(f"Días predichos con lluvia: {pred_lluvia_d5}\n")
        f.write(f"Días reales con lluvia: {real_lluvia_d5}\n")
        f.write(f"Días analizados: {total_d5}\n\n")
        
        f.write(f"Raval (X4): {precision_x4:.1f}%\n")
        f.write(f"Días predichos con lluvia: {pred_lluvia_x4}\n")
        f.write(f"Días reales con lluvia: {real_lluvia_x4}\n")
        f.write(f"Días analizados: {total_x4}\n")

if __name__ == "__main__":
    main()