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
from src.settings import VERSION_STRING, GAME_NAME

def main():
    """
    Función principal - Punto de entrada del juego
    
    PSEUDOCÓDIGO:
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
    """
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
    """
    Verificar que todas las dependencias estén instaladas
    
    PSEUDOCÓDIGO:
    dependencias = ['pygame']
    faltantes = []
    
    PARA dependencia EN dependencias:
        try:
            __import__(dependencia)
            print(f"✓ {dependencia} instalado")
        except ImportError:
            print(f"✗ {dependencia} NO instalado")
            faltantes.append(dependencia)
    
    SI len(faltantes) > 0:
        print("\nDependencias faltantes:")
        PARA dep EN faltantes:
            print(f"  - {dep}")
        print("\nInstala con: pip install " + " ".join(faltantes))
        RETORNAR False
    
    RETORNAR True
    """
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
    """
    Verificar que exista la estructura de carpetas necesaria
    
    PSEUDOCÓDIGO:
    carpetas_necesarias = [
        "assets",
        "assets/sprites",
        "assets/sounds",
        "assets/music",
        "data"
    ]
    
    print("Verificando estructura de carpetas...")
    
    PARA carpeta EN carpetas_necesarias:
        SI NO os.path.exists(carpeta):
            print(f"  Creando carpeta: {carpeta}")
            os.makedirs(carpeta)
        SINO:
            print(f"✓ {carpeta}")
    
    print("Estructura de carpetas lista")
    print()
    """
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
    """
    Mostrar información de controles al inicio
    
    PSEUDOCÓDIGO:
    print("CONTROLES DEL JUEGO")
    print("-" * 60)
    print("  Movimiento:   WASD o Flechas")
    print("  Pausa:        ESC o P")
    print("  Confirmar:    ESPACIO o ENTER")
    print()
    print("  DEBUG (si está activado):")
    print("    F1: Ganar 100 XP")
    print("    F2: Spawnear oleada boss")
    print("    F3: Curación completa")
    print("-" * 60)
    print()
    """
    print("CONTROLES DEL JUEGO")
    print("-" * 60)
    print("  Movimiento:   WASD o Flechas")
    print("  Pausa:        ESC o P")
    print("  Confirmar:    ESPACIO o ENTER")
    print()
    print("  DEBUG (si está activado):")
    print("    F1: Ganar 100 XP")
    print("    F2: Spawnear oleada boss")
    print("    F3: Curación completa")
    print("-" * 60)
    print()


def inicializar_ambiente():
    """
    Inicializar ambiente de juego
    
    PSEUDOCÓDIGO:
    # Verificar dependencias
    SI NO verificar_dependencias():
        print("\nNo se puede iniciar el juego sin las dependencias.")
        input("Presiona ENTER para salir...")
        sys.exit(1)
    
    # Verificar estructura de carpetas
    verificar_estructura()
    
    # Mostrar controles
    mostrar_controles()
    """
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
    """
    PSEUDOCÓDIGO:
    
    # Inicializar ambiente
    inicializar_ambiente()
    
    # Ejecutar juego
    main()
    """
    # Inicializar ambiente
    inicializar_ambiente()
    
    # Ejecutar juego
    main()


# ========== NOTAS DE DESARROLLO ==========
"""
INSTRUCCIONES DE EJECUCIÓN:

1. PRIMERA VEZ:
   cd HACKATON-5.0
   pip install pygame
   python src/main.py

2. EJECUCIÓN NORMAL:
   python src/main.py

3. MODO DEBUG:
   Editar settings.py:
   DEBUG_MODE = True
   
   Luego ejecutar normalmente.

4. SI HAY ERRORES:
   - Verificar que pygame esté instalado: pip list | grep pygame
   - Verificar que todos los archivos estén en src/
   - Verificar que existan las carpetas assets/
   - Revisar el stack trace en consola

5. ESTRUCTURA ESPERADA:
   HACKATON-5.0/
   ├── src/
   │   ├── main.py (este archivo)
   │   ├── engine.py
   │   ├── settings.py
   │   ├── constants.py
   │   ├── entities/
   │   │   ├── __init__.py
   │   │   ├── base_entity.py
   │   │   ├── player.py
   │   │   ├── enemy.py
   │   │   └── arma.py
   │   ├── manage/
   │   │   ├── __init__.py
   │   │   ├── combat_manager.py
   │   │   ├── spawn_manager.py
   │   │   └── ui_manager.py
   │   ├── World/
   │   │   ├── __init__.py
   │   │   ├── camera.py
   │   │   └── map.py
   │   └── asset_/
   │       ├── __init__.py
   │       └── asset_loader.py
   ├── assets/
   │   ├── sprites/
   │   ├── sounds/
   │   └── music/
   └── data/

6. TROUBLESHOOTING COMÚN:

   Error: ModuleNotFoundError: No module named 'pygame'
   Solución: pip install pygame

   Error: ModuleNotFoundError: No module named 'X'
   Solución: Verificar que el archivo X.py exista en src/ o subcarpetas
             Verificar que haya __init__.py en cada subcarpeta

   Error: FileNotFoundError: [Errno 2] No such file or directory: 'assets/...'
   Solución: Crear carpetas assets/ manualmente o dejar que el juego las cree

   Error: pygame.error: No available video device
   Solución: En Linux, instalar: sudo apt-get install python3-pygame

7. RENDIMIENTO:
   - Si el juego va lento, reducir MAX_ENEMIGOS_PANTALLA en settings.py
   - Si hay lag, reducir RENDER_DISTANCE en settings.py
   - Desactivar MOSTRAR_FPS si causa problemas

8. PARA EL HACKATON:
   - Mantener DEBUG_MODE = False para la demo
   - Ajustar dificultad en settings.py si es necesario
   - Probar que el juego corra al menos 10 minutos sin crashes
   - Verificar que FPS sea > 30 con 100+ enemigos

¡ÉXITOS EN EL HACKATON! 🚀
"""
