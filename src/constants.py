"""
CONSTANTS.PY - CONSTANTES DEL JUEGO
====================================
Constantes inmutables y enumeraciones del juego
"""

from enum import Enum

# ========== ESTADOS DEL JUEGO ==========
class GameState(Enum):
    """
    Estados posibles del juego
    """
    MENU = "menu"
    JUGANDO = "jugando"
    PAUSA = "pausa"
    MEJORA = "mejora"  # Pantalla de selección de mejora
    GAME_OVER = "game_over"


# ========== TIPOS DE ENEMIGOS ==========
class EnemyType(Enum):
    """
    Tipos de enemigos disponibles
    """
    CARPINCHO = "CARPINCHO"
    YACARE = "YACARE"
    TATU = "TATU"
    AGUARA_GUAZU = "AGUARA_GUAZU"


# ========== TIPOS DE ARMAS ==========
class WeaponType(Enum):
    """
    Tipos de armas disponibles
    """
    MACHETE = "MACHETE"
    HACHA = "HACHA"
    AZADA = "AZADA"
    TERERE = "TERERE"


# ========== TIPOS DE TILES ==========
class TileType(Enum):
    """
    Tipos de tiles del mapa
    """
    PASTO_OSCURO = "PASTO_OSCURO"
    PASTO_CLARO = "PASTO_CLARO"
    PASTO_MEDIO = "PASTO_MEDIO"
    TIERRA = "TIERRA"
    AGUA = "AGUA"


# ========== TIPOS DE MEJORAS ==========
class UpgradeType(Enum):
    """
    Tipos de mejoras disponibles al subir nivel
    """
    NUEVA_ARMA = "nueva_arma"
    MEJORAR_ARMA = "mejorar_arma"
    AUMENTAR_VIDA_MAX = "aumentar_vida_max"
    AUMENTAR_VELOCIDAD = "aumentar_velocidad"
    AUMENTAR_RADIO_RECOLECCION = "aumentar_radio_recoleccion"
    AUMENTAR_DAÑO = "aumentar_daño"
    REDUCIR_COOLDOWN = "reducir_cooldown"


# ========== DIRECCIONES ==========
class Direction(Enum):
    """
    Direcciones de movimiento
    """
    ARRIBA = "arriba"
    ABAJO = "abajo"
    IZQUIERDA = "izquierda"
    DERECHA = "derecha"


# ========== TECLAS DE CONTROL ==========
class Controls:
    """
    Mapeo de teclas de control
    """
    # Movimiento
    ARRIBA = ['w', 'up']
    ABAJO = ['s', 'down']
    IZQUIERDA = ['a', 'left']
    DERECHA = ['d', 'right']
    
    # Sistema
    PAUSA = ['escape', 'p']
    CONFIRMAR = ['space', 'return']
    SALIR = ['q']


# ========== CONSTANTES DE FÍSICA ==========
class Physics:
    """
    Constantes físicas del juego
    """
    GRAVEDAD = 0  # No hay gravedad (juego top-down)
    FRICCION = 0.9  # Para deslizamiento (opcional)
    VELOCIDAD_MAXIMA = 500  # píxeles por segundo
    KNOCKBACK_DURACION = 0.2  # segundos
    KNOCKBACK_DECELERACION = 0.95  # Factor de reducción


# ========== CONSTANTES DE BALANCE ==========
class Balance:
    """
    Constantes de balance del juego
    """
    # Experiencia
    XP_MULTIPLICADOR_BASE = 1.0
    XP_BONUS_POR_COMBO = 0.1  # +10% por cada enemigo en combo
    
    # Dificultad
    DIFICULTAD_INCREMENTO_POR_MINUTO = 0.05  # 5% cada minuto
    DIFICULTAD_MAXIMA = 3.0  # 300% de dificultad máxima
    
    # Spawn
    ENEMIGOS_MAXIMO_PANTALLA = 300
    ENEMIGOS_MAXIMO_GLOBAL = 500
    
    # Vida
    VIDA_REGENERACION_FUERA_COMBATE = 1.0  # vida/segundo
    TIEMPO_FUERA_COMBATE = 5.0  # segundos sin daño


# ========== CONSTANTES DE UI ==========
class UIConstants:
    """
    Constantes de interfaz de usuario
    """
    # Tamaños de fuente
    FUENTE_TITULO = 64
    FUENTE_GRANDE = 48
    FUENTE_MEDIA = 32
    FUENTE_PEQUEÑA = 24
    FUENTE_MINI = 18
    
    # Tamaños de barras
    BARRA_VIDA_ANCHO = 300
    BARRA_VIDA_ALTO = 30
    BARRA_XP_ANCHO = 300
    BARRA_XP_ALTO = 20
    
    # Transparencias
    OVERLAY_ALPHA = 200
    MENU_ALPHA = 180
    
    # Animaciones
    FADE_IN_DURACION = 0.5
    FADE_OUT_DURACION = 0.5
    CARD_HOVER_SCALE = 1.05


# ========== CONSTANTES DE AUDIO ==========
class AudioConstants:
    """
    Constantes de audio
    """
    VOLUMEN_MUSICA_DEFAULT = 0.3
    VOLUMEN_SFX_DEFAULT = 0.7
    VOLUMEN_MINIMO = 0.0
    VOLUMEN_MAXIMO = 1.0
    
    # Canales de audio
    CANAL_SFX_GOLPE = 0
    CANAL_SFX_XP = 1
    CANAL_SFX_UI = 2
    CANAL_SFX_AMBIENTE = 3


# ========== CONSTANTES DE TIEMPO ==========
class TimeConstants:
    """
    Constantes relacionadas con tiempo
    """
    DIA_DURACION = 300  # 5 minutos = 1 día de juego
    NOCHE_DURACION = 300  # 5 minutos = 1 noche de juego
    
    # Oleadas especiales
    OLEADA_BOSS_INTERVALO = 600  # Cada 10 minutos
    OLEADA_ELITE_INTERVALO = 180  # Cada 3 minutos
    
    # Eventos
    EVENTO_RANDOM_MIN = 120  # Mínimo 2 minutos entre eventos
    EVENTO_RANDOM_MAX = 300  # Máximo 5 minutos entre eventos


# ========== CONSTANTES DE EFECTOS VISUALES ==========
class VFXConstants:
    """
    Constantes de efectos visuales
    """
    PARTICULA_VIDA_MINIMA = 0.1
    PARTICULA_VIDA_MAXIMA = 1.0
    PARTICULA_VELOCIDAD_MIN = 50
    PARTICULA_VELOCIDAD_MAX = 200
    PARTICULA_TAMAÑO_MIN = 2
    PARTICULA_TAMAÑO_MAX = 8
    
    # Shake de cámara
    SHAKE_INTENSIDAD_LEVE = 3
    SHAKE_INTENSIDAD_MEDIA = 7
    SHAKE_INTENSIDAD_FUERTE = 15
    SHAKE_DURACION_DEFAULT = 0.3


# ========== CONSTANTES MATEMÁTICAS ==========
class MathConstants:
    """
    Constantes matemáticas útiles
    """
    PI = 3.14159265359
    TAU = 6.28318530718  # 2 * PI
    GRADOS_A_RADIANES = 0.01745329251
    RADIANES_A_GRADOS = 57.2957795131


# ========== CONSTANTES DE DEBUG ==========
class DebugConstants:
    """
    Constantes para modo debug
    """
    MOSTRAR_HITBOXES = False
    MOSTRAR_FPS = True
    MOSTRAR_POSICIONES = False
    MOSTRAR_STATS_ENEMIGOS = False
    MODO_INVENCIBLE = False
    MODO_XP_INFINITO = False
    SPAWN_INSTANTANEO = False


# ========== MENSAJES DEL SISTEMA ==========
class SystemMessages:
    """
    Mensajes del sistema
    """
    # Errores
    ERROR_CARGA_SPRITE = "Error al cargar sprite: {}"
    ERROR_CARGA_SONIDO = "Error al cargar sonido: {}"
    ERROR_CARGA_MAPA = "Error al cargar mapa: {}"
    
    # Advertencias
    WARN_SPRITE_NO_ENCONTRADO = "ADVERTENCIA: Sprite '{}' no encontrado"
    WARN_SONIDO_NO_ENCONTRADO = "ADVERTENCIA: Sonido '{}' no encontrado"
    WARN_MUCHOS_ENEMIGOS = "ADVERTENCIA: Demasiados enemigos en pantalla ({})"
    
    # Info
    INFO_JUEGO_INICIADO = "Juego iniciado correctamente"
    INFO_ASSETS_CARGADOS = "Assets cargados: {} sprites, {} sonidos"
    INFO_NIVEL_ALCANZADO = "¡Nivel {} alcanzado!"


# ========== VALORES POR DEFECTO ==========
class Defaults:
    """
    Valores por defecto del juego
    """
    NOMBRE_JUGADOR = "Campesino"
    DIFICULTAD = "Normal"
    IDIOMA = "ES"
    PANTALLA_COMPLETA = False
    VSYNC = True
    MOSTRAR_TUTORIAL = True


# ========== LÍMITES DEL JUEGO ==========
class Limits:
    """
    Límites y restricciones del juego
    """
    NIVEL_MAXIMO = 100
    ARMAS_MAXIMO = 6
    MEJORAS_POR_NIVEL = 3
    ENEMIGOS_POR_TIPO_MAX = 100
    XP_ORBES_MAXIMO = 500
    PROYECTILES_MAXIMO = 200


# ========== PATHS DE ARCHIVOS ==========
class Paths:
    """
    Rutas de archivos y directorios
    """
    # Directorios principales
    DIR_ASSETS = "assets/"
    DIR_SPRITES = "assets/sprites/"
    DIR_SONIDOS = "assets/sounds/"
    DIR_MUSICA = "assets/music/"
    DIR_FUENTES = "assets/fonts/"
    DIR_DATOS = "data/"
    
    # Archivos de configuración
    CONFIG_JUEGO = "data/config.json"
    CONFIG_CONTROLES = "data/controls.json"
    HIGHSCORES = "data/highscores.json"
    
    # Archivos de guardado
    SAVE_SLOT_1 = "data/save1.json"
    SAVE_SLOT_2 = "data/save2.json"
    SAVE_SLOT_3 = "data/save3.json"


# ========== CÓDIGOS DE COLOR ==========
class Colors:
    """
    Paleta de colores del juego (además de los en settings.py)
    """
    # Rareza de items
    COMUN = (200, 200, 200)      # Gris claro
    POCO_COMUN = (30, 255, 0)    # Verde
    RARO = (0, 112, 221)         # Azul
    EPICO = (163, 53, 238)       # Púrpura
    LEGENDARIO = (255, 128, 0)   # Naranja
    
    # Estados
    POSITIVO = (0, 255, 0)       # Verde
    NEGATIVO = (255, 0, 0)       # Rojo
    NEUTRAL = (200, 200, 200)    # Gris
    ADVERTENCIA = (255, 255, 0)  # Amarillo
    
    # UI
    BOTON_NORMAL = (60, 60, 60)
    BOTON_HOVER = (80, 80, 80)
    BOTON_PRESIONADO = (40, 40, 40)
    BOTON_DESHABILITADO = (30, 30, 30)


# ========== VERSIÓN DEL JUEGO ==========
class Version:
    """
    Información de versión
    """
    MAJOR = 1
    MINOR = 0
    PATCH = 0
    BUILD = "MVP"
    
    @staticmethod
    def get_version_string():
        """Obtener string de versión completo"""
        return f"v{Version.MAJOR}.{Version.MINOR}.{Version.PATCH}-{Version.BUILD}"


# ========== METADATOS DEL JUEGO ==========
class GameMetadata:
    """
    Metadatos del juego
    """
    NOMBRE = "Campesino Paraguayo: Survival"
    NOMBRE_CORTO = "Campesino Survival"
    DESARROLLADOR = "Equipo Hackaton"
    ANIO = 2025
    GENERO = "Roguelike, Acción, Supervivencia"
    PLATAFORMA = "PC (Windows/Linux/Mac)"


# ========== ESTADÍSTICAS ==========
class StatsTracking:
    """
    Nombres de estadísticas rastreadas
    """
    TIEMPO_TOTAL_JUGADO = "tiempo_total"
    ENEMIGOS_TOTALES_MATADOS = "enemigos_matados_total"
    NIVEL_MAXIMO_ALCANZADO = "nivel_max"
    TIEMPO_SUPERVIVENCIA_RECORD = "tiempo_supervivencia_max"
    PARTIDAS_JUGADAS = "partidas_jugadas"
    PARTIDAS_GANADAS = "partidas_ganadas"
    DAÑO_TOTAL_INFLIGIDO = "daño_total"
    DAÑO_TOTAL_RECIBIDO = "daño_recibido_total"
    XP_TOTAL_RECOLECTADA = "xp_total"