import os
import sys

src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.append(src_path)

def main():
   
    # Ejercicio 2
    print("Ejecutando ejercicio 2 - Predicción Temperaturas")
    print("="*50)
    import ej2_predic_temp
    
    # Ejercicio 3  
    print("\nEjecutando ejercicio 3 - Predicción Lluvias")
    print("="*50)
    import ej3_predic_lluvia
    
    print("\n✅ Todos los ejercicios completados")
    print("📊 Gráficos guardados en: src/graficos_generados/")

if __name__ == "__main__":
    main()