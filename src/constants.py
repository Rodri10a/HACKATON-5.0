"""
CONSTANTS.PY - CONSTANTES DEL JUEGO
====================================
Constantes inmutables y enumeraciones del juego
"""

from enum import Enum

# ========== ESTADOS DEL JUEGO ==========
class GameState(Enum):
    """Estados posibles del juego"""
    MENU = "menu"
    JUGANDO = "jugando"
    PAUSA = "pausa"
    MEJORA = "mejora"
    GAME_OVER = "game_over"


# ========== TIPOS DE ENEMIGOS ==========
class EnemyType(Enum):
    """Tipos de enemigos disponibles"""
    CARPINCHO = "CARPINCHO"
    YACARE = "YACARE"
    TATU = "TATU"
    AGUARA_GUAZU = "AGUARA_GUAZU"


# ========== TIPOS DE ARMAS ==========
class WeaponType(Enum):
    """Tipos de armas disponibles"""
    MACHETE = "MACHETE"
    HACHA = "HACHA"
    AZADA = "AZADA"
    TERERE = "TERERE"


# ========== TIPOS DE TILES ==========
class TileType(Enum):
    """Tipos de tiles del mapa"""
    PASTO_OSCURO = "PASTO_OSCURO"
    PASTO_CLARO = "PASTO_CLARO"
    PASTO_MEDIO = "PASTO_MEDIO"


# ========== TIPOS DE MEJORAS ==========
class UpgradeType(Enum):
    """Tipos de mejoras disponibles al subir nivel"""
    NUEVA_ARMA = "nueva_arma"
    MEJORAR_ARMA = "mejorar_arma"
    AUMENTAR_VIDA_MAX = "aumentar_vida_max"
    AUMENTAR_VELOCIDAD = "aumentar_velocidad"
    AUMENTAR_RADIO_RECOLECCION = "aumentar_radio_recoleccion"


# ========== DIRECCIONES ==========
class Direction(Enum):
    """Direcciones de movimiento"""
    ARRIBA = "arriba"
    ABAJO = "abajo"
    IZQUIERDA = "izquierda"
    DERECHA = "derecha"