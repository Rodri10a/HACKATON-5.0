"""
SETTINGS.PY - CONFIGURACIÓN GLOBAL DEL JUEGO
============================================
Todas las constantes y configuraciones del juego
"""

# ========== CONFIGURACIÓN DE PANTALLA ==========
ANCHO_VENTANA = 1280
ALTO_VENTANA = 720
FPS = 60
TITULO_JUEGO = "Karai Survival"
# ========== COLORES (RGB) ==========
COLOR_FONDO = (34, 139, 34)  # Verde tierra paraguaya
COLOR_VIDA = (220, 20, 60)    # Rojo para barra de vida
COLOR_XP = (255, 215, 0)      # Dorado para XP
COLOR_TEXTO = (255, 255, 255) # Blanco
COLOR_UI_FONDO = (0, 0, 0)    # Negro semi-transparente

# ========== STATS BASE DEL CAMPESINO ==========
CAMPESINO_VIDA_MAX = 100
CAMPESINO_VELOCIDAD = 200  # píxeles por segundo
CAMPESINO_DAÑO_BASE = 10
CAMPESINO_RADIO_RECOLECCION = 50  # Radio para recoger XP

# ========== SISTEMA DE EXPERIENCIA ==========
XP_POR_NIVEL = [100, 150, 225, 340, 510, 765, 1150, 1725, 2590, 3885]
# Después del nivel 10, usar fórmula: XP_POR_NIVEL[-1] * 1.5^(nivel-10)

# ========== CONFIGURACIÓN DE ENEMIGOS ==========
ENEMIGO_CONFIGS = {
    "CARPINCHO": {
        "vida": 30,
        "velocidad": 80,
        "daño": 5,
        "xp": 10,
        "spawn_peso": 10  # Mayor peso = más común
    },
    "YACARE": {
        "vida": 50,
        "velocidad": 60,
        "daño": 8,
        "xp": 15,
        "spawn_peso": 7
    },
    "TATU": {
        "vida": 80,
        "velocidad": 40,
        "daño": 12,
        "xp": 25,
        "spawn_peso": 4
    },
    "AGUARA_GUAZU": {
        "vida": 150,
        "velocidad": 100,
        "daño": 20,
        "xp": 50,
        "spawn_peso": 2  # Boss menor
    }
}

# ========== SISTEMA DE OLEADAS ==========
TIEMPO_ENTRE_SPAWNS = 1.0  # segundos iniciales
SPAWN_REDUCCION_POR_MINUTO = 0.05  # Cada minuto spawnean más rápido
SPAWN_MINIMO = 0.2  # Tiempo mínimo entre spawns
ENEMIGOS_POR_SPAWN = 1  # Inicial
AUMENTO_ENEMIGOS_CADA = 120  # segundos (cada 2 min +1 enemigo)

# ========== CONFIGURACIÓN DE ARMAS/HERRAMIENTAS ==========
ARMAS_CONFIG = {
    "MACHETE": {
        "daño_base": 15,
        "alcance": 60,
        "cooldown": 0.5,
        "tipo": "melee",
        "niveles": [
            {"daño": 15, "alcance": 60},
            {"daño": 22, "alcance": 70},
            {"daño": 33, "alcance": 80},
            {"daño": 50, "alcance": 100}
        ]
    },
    "HACHA": {
        "daño_base": 25,
        "alcance": 80,
        "cooldown": 1.2,
        "tipo": "proyectil",
        "niveles": [
            {"daño": 25, "cantidad": 1, "velocidad": 400},
            {"daño": 35, "cantidad": 2, "velocidad": 400},
            {"daño": 50, "cantidad": 3, "velocidad": 400},
            {"daño": 75, "cantidad": 4, "velocidad": 400}
        ]
    },
    "AZADA": {
        "daño_base": 20,
        "alcance": 100,
        "cooldown": 0.8,
        "tipo": "aoe",  # Área de efecto
        "niveles": [
            {"daño": 20, "radio": 50},
            {"daño": 30, "radio": 70},
            {"daño": 45, "radio": 100},
            {"daño": 70, "radio": 150}
        ]
    },
    "TERERE": {
        "daño_base": 0,
        "cooldown": 5.0,
        "tipo": "buff",  # Regeneración
        "niveles": [
            {"vida_por_seg": 2, "duracion": 5},
            {"vida_por_seg": 4, "duracion": 7},
            {"vida_por_seg": 7, "duracion": 10},
            {"vida_por_seg": 12, "duracion": 15}
        ]
    }
}

# ========== CONFIGURACIÓN DE MAPA ==========
TILE_SIZE = 64  # Tamaño de cada tile del mapa
MAPA_ANCHO_TILES = 100  # Mapa grande para explorar
MAPA_ALTO_TILES = 100
MAPA_ANCHO_PIXELES = MAPA_ANCHO_TILES * TILE_SIZE
MAPA_ALTO_PIXELES = MAPA_ALTO_TILES * TILE_SIZE

# ========== CONFIGURACIÓN DE CÁMARA ==========
CAMARA_VELOCIDAD_SEGUIMIENTO = 5  # Suavidad del seguimiento

# ========== UI ==========
TAMAÑO_BARRA_VIDA = (300, 30)
POSICION_BARRA_VIDA = (20, 20)
TAMAÑO_BARRA_XP = (300, 20)
POSICION_BARRA_XP = (20, 60)

# ========== DROPS Y RECOMPENSAS ==========
CHANCE_DROP_VIDA = 0.05  # 5% de chance de drop de vida al matar
VIDA_RECUPERADA_DROP = 20

# ========== DEBUG ==========
DEBUG_MODE = False  # Cambiar a True para ver hitboxes y info
MOSTRAR_FPS = True

# ========== CONFIGURACIÓN DE PROYECTILES ==========
PROYECTIL_HACHA_VELOCIDAD = 400  # píxeles por segundo
PROYECTIL_HACHA_ALCANCE = 500  # distancia máxima
PROYECTIL_HACHA_ROTACION = 720  # grados por segundo

# ========== CONFIGURACIÓN DE KNOCKBACK ==========
KNOCKBACK_FUERZA_MACHETE = 100
KNOCKBACK_FUERZA_HACHA = 50
KNOCKBACK_FUERZA_AZADA = 200

# ========== CONFIGURACIÓN DE INVULNERABILIDAD ==========
INVULNERABILIDAD_DURACION = 0.5  # segundos después de recibir daño

# ========== CONFIGURACIÓN DE BALANCEO ==========
VIDA_BONUS_POR_NIVEL = 20  # Vida extra al subir nivel
VELOCIDAD_BONUS_POR_NIVEL = 10  # Velocidad extra al mejorar
RADIO_RECOLECCION_BONUS = 20  # Radio extra al mejorar

# ========== LÍMITES DEL JUEGO ==========
MAX_ENEMIGOS_PANTALLA = 300
MAX_PROYECTILES = 200
MAX_ORBES_XP = 500
MAX_ARMAS_EQUIPADAS = 6

# ========== CONFIGURACIÓN DE TILES DEL MAPA ==========
TILE_COLORES = {
    "PASTO_OSCURO": (34, 139, 34),   # Verde oscuro
    "PASTO_CLARO": (50, 205, 50),    # Verde claro
    "PASTO_MEDIO": (60, 179, 113)    # Verde medio
}

# ========== CONFIGURACIÓN DE SPAWN DE ENEMIGOS ==========
SPAWN_MARGEN_PANTALLA = 100  # Píxeles fuera de pantalla para spawn

# ========== CONFIGURACIÓN DE MEJORAS ==========
MEJORAS_POR_NIVEL = 3  # Cantidad de opciones al subir nivel
MEJORAS_VALORES = {
    "vida_max": 20,
    "velocidad": 20,
    "radio_recoleccion": 20,
    "daño": 5,
    "cooldown_reduccion": 0.1
}

# ========== INFORMACIÓN DE VERSIÓN ==========
VERSION_MAJOR = 1
VERSION_MINOR = 0
VERSION_PATCH = 0
VERSION_BUILD = "MVP"
VERSION_STRING = f"v{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}-{VERSION_BUILD}"

# ========== METADATA DEL JUEGO ==========
GAME_NAME = "Karai Survival"