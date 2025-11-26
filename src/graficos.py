"""
Módulo con funciones para crear gráficos
"""

import matplotlib.pyplot as plt

def crear_grafico_comparativo(media_fabra, media_raval):
    plt.figure(figsize=(10, 6))
    meses = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    plt.plot(meses, media_fabra.values, marker='o', color='blue', label='Fabra (411m)')
    plt.plot(meses, media_raval.values, marker='s', color='red', label='Raval (33m)')

    plt.title('Temperatura Media Mensual 2025')
    plt.xlabel('Mes')
    plt.ylabel('Temperatura (°C)')
    plt.legend()
    plt.grid(True)
    plt.savefig('outputs/comparativa_temperaturas.png')
    plt.show()

def crear_graficos_separados(media_fabra, media_raval):
    # media_fabra --> Series con medias de Fabra
    # media_raval --> Series con medias de Raval
    meses = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    
    # Gráfico Fabra
    plt.figure(figsize=(8, 5))
    plt.plot(meses, media_fabra.values, marker='o', color='blue')
    plt.title('Fabra (411m) - Temperatura Media 2025')
    plt.xlabel('Mes')
    plt.ylabel('Temperatura (°C)')
    plt.grid(True)
    plt.savefig('outputs/temperatura_fabra.png')
    plt.show()

    # Gráfico Raval
    plt.figure(figsize=(8, 5))
    plt.plot(meses, media_raval.values, marker='s', color='red')
    plt.title('Raval (33m) - Temperatura Media 2025')
    plt.xlabel('Mes')
    plt.ylabel('Temperatura (°C)')
    plt.grid(True)
    plt.savefig('outputs/temperatura_raval.png')
    plt.show()