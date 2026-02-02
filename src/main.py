"""
MAIN.PY - PUNTO DE ENTRADA PRINCIPAL DEL JUEGO
===============================================
Inicializa el motor del juego y ejecuta el game loop
"""

import sys
import os

# Agregar el directorio src al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Imports principales
from engine import GameEngine
from settings import VERSION_STRING, GAME_NAME


def main():
    """Función principal - Punto de entrada del juego"""
    try:
        # Imprimir información de inicio
        print("=" * 60)
        print(f"{GAME_NAME}")
        print(f"Versión: {VERSION_STRING}")
        print("=" * 60)
        print()
        
        # Crear instancia del motor del juego
        print("Inicializando motor del juego...")
        motor = GameEngine()
        
        print("Motor inicializado correctamente")
        print("Iniciando game loop...")
        print()
        
        # Ejecutar el juego
        motor.run()
        
    except KeyboardInterrupt:
        # Manejo de Ctrl+C
        print("\n\nJuego interrumpido por el usuario")
        print("Cerrando...")
        
    except Exception as e:
        # Manejo de errores generales
        print("\n" + "="*60)
        print("ERROR CRÍTICO")
        print("="*60)
        print(f"Tipo: {type(e).__name__}")
        print(f"Mensaje: {str(e)}")
        print()
        print("Stack trace:")
        import traceback
        traceback.print_exc()
        print("="*60)
        print()
        print("El juego se cerrará.")
        
        # Esperar input antes de cerrar (para ver el error)
        input("Presiona ENTER para salir...")
        
    finally:
        # Limpieza final
        print("\nJuego cerrado")
        sys.exit(0)


def verificar_dependencias():
    """Verificar que todas las dependencias estén instaladas"""
    print("Verificando dependencias...")
    dependencias = ['pygame']
    faltantes = []
    
    for dependencia in dependencias:
        try:
            __import__(dependencia)
            print(f"✓ {dependencia} instalado")
        except ImportError:
            print(f"✗ {dependencia} NO instalado")
            faltantes.append(dependencia)
    
    if len(faltantes) > 0:
        print("\nDependencias faltantes:")
        for dep in faltantes:
            print(f"  - {dep}")
        print("\nInstala con: pip install " + " ".join(faltantes))
        return False
    
    print("Todas las dependencias instaladas correctamente")
    print()
    return True


def verificar_estructura():
    """Verificar que exista la estructura de carpetas necesaria"""
    carpetas_necesarias = [
        "assets",
        "assets/sprites",
        "assets/sounds",
        "assets/music",
        "data"
    ]
    
    print("Verificando estructura de carpetas...")
    
    for carpeta in carpetas_necesarias:
        if not os.path.exists(carpeta):
            print(f"  Creando carpeta: {carpeta}")
            os.makedirs(carpeta)
        else:
            print(f"✓ {carpeta}")
    
    print("Estructura de carpetas lista")
    print()


def mostrar_controles():
    """Mostrar información de controles al inicio"""
    print("CONTROLES DEL JUEGO")
    print("-" * 60)
    print("  Movimiento:   WASD o Flechas")
    print("  Pausa:        ESC")
    print("  Confirmar:    ESPACIO o ENTER")
    print()
    if True:  # Siempre mostrar para que sepan
        print("  DEBUG:")
        print("    F1: Ganar 100 XP")
        print("    F3: Curación completa")
    print("-" * 60)
    print()


def inicializar_ambiente():
    """Inicializar ambiente de juego"""
    # Verificar dependencias
    if not verificar_dependencias():
        print("\nNo se puede iniciar el juego sin las dependencias.")
        input("Presiona ENTER para salir...")
        sys.exit(1)
    
    # Verificar estructura de carpetas
    verificar_estructura()
    
    # Mostrar controles
    mostrar_controles()


# ========== PUNTO DE ENTRADA ==========
if __name__ == "__main__":
    # Inicializar ambiente
    inicializar_ambiente()
    
    # Ejecutar juego
    main()