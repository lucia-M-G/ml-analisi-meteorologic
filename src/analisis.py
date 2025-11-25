"""
Módulo con funciones de análisis de datos
"""

def mostrar_info_datos(df_fabra, df_raval):
    # df_fabra --> DataFrame de Fabra
    # df_raval --> DataFrame de Raval
    print("Primeras filas Fabra:")
    print(df_fabra.head())
    print("\nPrimeras filas Raval:")
    print(df_raval.head())

def mostrar_info_temperaturas(temp_fabra, temp_raval):
    # temp_fabra --> Temperaturas de Fabra
    # temp_raval --> Temperaturas de Raval
    print(f"Temperaturas Fabra 2025: {len(temp_fabra)} registros")
    print(f"Temperaturas Raval 2025: {len(temp_raval)} registros")

def mostrar_temperaturas_mensuales(media_fabra, media_raval):
    print("Temperatura media Fabra por mes:")
    print(media_fabra)
    print("\nTemperatura media Raval por mes:")
    print(media_raval)

def analizar_diferencias(media_fabra, media_raval):
    print("\n" + "=" * 60)
    print("ANÁLISIS: Fabra (411m) vs Raval (33m)")
    print("Diferencia de altitud: 378 metros")
    print("=" * 60)

    for mes in range(1, 13):
        temp_f = media_fabra[mes]
        temp_r = media_raval[mes]
        diferencia = temp_r - temp_f
        
        print(f"Mes {mes}: Fabra {temp_f:.1f}°C - Raval {temp_r:.1f}°C = {diferencia:+.1f}°C")