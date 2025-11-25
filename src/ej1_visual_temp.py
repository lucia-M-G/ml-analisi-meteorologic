"""
EJERCICIO 1: COMPARATIVA TEMPERATURAS 2025
Comparar la temperatura media mensual del 2025 entre las estaciones
Fabra (411m del nivel del mar) y Raval (33m del nivel del mar)
"""

from utils import *
from graficos import *
from analisis import *

def main():
    print("EJERCICIO 1: COMPARATIVA TEMPERATURAS 2025")
    print("=" * 60)
    
    # Configuración inicial
    crear_carpeta_outputs()
    
    # Cargar datos
    print("Cargando datos...")
    df_fabra, df_raval = cargar_datos()
    
    # Explorar datos
    print("\nExplorando datos...")
    mostrar_info_datos(df_fabra, df_raval)
    
    # Procesar datos
    print("\nConvirtiendo fechas...")
    convertir_fechas(df_fabra, df_raval)
    
    print("Filtrando temperaturas 2025...")
    temp_fabra, temp_raval = filtrar_temperaturas_2025(df_fabra, df_raval)
    mostrar_info_temperaturas(temp_fabra, temp_raval)
    
    # Calcular estadísticas
    print("\nCalculando temperatura media mensual...")
    media_fabra, media_raval = calcular_temperatura_mensual(temp_fabra, temp_raval)
    mostrar_temperaturas_mensuales(media_fabra, media_raval)
    
    # Visualizar datos
    print("\nCreando gráficos...")
    crear_grafico_comparativo(media_fabra, media_raval)
    crear_graficos_separados(media_fabra, media_raval)
    
    # Analizar resultados
    print("\nAnalizando diferencias...")
    analizar_diferencias(media_fabra, media_raval)

if __name__ == "__main__":
    main()