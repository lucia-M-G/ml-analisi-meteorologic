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

if __name__ == "__main__":
    main()