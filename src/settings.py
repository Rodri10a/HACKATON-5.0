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
COLOR_FONDO = (34, 139, 34)
COLOR_VIDA = (220, 20, 60)
COLOR_XP = (255, 215, 0)
COLOR_TEXTO = (255, 255, 255)
COLOR_UI_FONDO = (0, 0, 0)

# ========== STATS BASE DEL CAMPESINO ==========
CAMPESINO_VIDA_MAX = 100
CAMPESINO_VELOCIDAD = 200
CAMPESINO_DAÑO_BASE = 10
CAMPESINO_RADIO_RECOLECCION = 80  # Más grande para recoger XP más fácil

# ========== SISTEMA DE EXPERIENCIA (MÁS FÁCIL) ==========
# Cada nivel se completa en aprox 30-45 segundos
XP_POR_NIVEL = [25, 40, 60, 90, 130, 180, 250, 350, 480, 650] 

# ========== CONFIGURACIÓN DE ENEMIGOS ==========
ENEMIGO_CONFIGS = {
    "MOSQUITO": {
        "vida": 10,
        "velocidad": 110,
        "daño": 2,
        "xp": 12,
        "spawn_peso": 12,
        "ancho": 35,          # Pequeño, ligeramente horizontal
        "alto": 28,
    },
    "AOAO": {
        "vida": 50,
        "velocidad": 50,
        "daño": 8,
        "xp": 25,
        "spawn_peso": 10,
        "ancho": 50,          # Criatura vertical grande
        "alto": 65,
    },
    "PORA": {
        "vida": 25,
        "velocidad": 40,
        "daño": 4,
        "xp": 15,
        "spawn_peso": 8,
        "ancho": 55,          # Fantasma vertical con brazos
        "alto": 75,
    },
    "YACARE": {
        "vida": 35,
        "velocidad": 55,
        "daño": 6,
        "xp": 22,
        "spawn_peso": 7,
        "ancho": 95,          # Cocodrilo muy horizontal
        "alto": 45,
    },
    "LUISON": {
        "vida": 130,
        "velocidad": 80,
        "daño": 18,
        "xp": 75,
        "spawn_peso": 1,      # Raro - Boss
        "ancho": 70,          # Boss grande, casi cuadrado
        "alto": 70,
    },
    "POMBERO": {
        "vida": 70,
        "velocidad": 60,
        "daño": 10,
        "xp": 40,
        "spawn_peso": 5,
        "ancho": 55,          # Usa sprite de PORA
        "alto": 75,
    },
    "SERPIENTE": {
        "vida": 28,
        "velocidad": 75,
        "daño": 7,
        "xp": 18,
        "spawn_peso": 8,
        "ancho": 100,         # Serpiente muy horizontal
        "alto": 38,
    }
}

# ========== SISTEMA DE OLEADAS (ESCALAMIENTO RÁPIDO) ==========
# --- En la sección SISTEMA DE OLEADAS ---
TIEMPO_ENTRE_SPAWNS = 1.2        # Antes 0.8 (Tardan más en aparecer)
ENEMIGOS_POR_SPAWN = 1           # Antes 2 (Sale solo 1 a la vez al inicio)
AUMENTO_ENEMIGOS_CADA = 120      # Antes 60 (La dificultad sube cada 2 minutos, no cada 1)

SPAWN_MINIMO = 0.3               # Tiempo mínimo entre spawns (no puede bajar de esto)
SPAWN_REDUCCION_POR_MINUTO = 0.1 # Cuánto se reduce el tiempo entre spawns cada minuto
# ========== CONFIGURACIÓN DE ARMAS ==========
ARMAS_CONFIG = {
    "MACHETE": {
        "daño_base": 20,
        "alcance": 180,          # Más alcance
        "cooldown": 0.4,        # Más rápido
        "tipo": "melee",
        # Modifica la lista de "niveles" dentro de "MACHETE":
        "niveles": [
        {"daño": 20, "alcance": 120}, # Antes 80
        {"daño": 30, "alcance": 150}, # Antes 90
        {"daño": 45, "alcance": 200}, # Antes 100
        {"daño": 65, "alcance": 250}  # Antes 120 (Casi media pantalla)  
]
    },
    "HACHA": {
        "daño_base": 30,
        "alcance": 80,
        "cooldown": 1.0,        # Más rápido
        "tipo": "proyectil",
        "niveles": [
            {"daño": 30, "cantidad": 2, "velocidad": 450},
            {"daño": 42, "cantidad": 3, "velocidad": 450},
            {"daño": 60, "cantidad": 4, "velocidad": 450},
            {"daño": 85, "cantidad": 5, "velocidad": 450}
        ]
    },
    "AZADA": {
        "daño_base": 25,
        "alcance": 100,
        "cooldown": 0.7,        # Más rápido
        "tipo": "aoe",
        "niveles": [ 
            {"daño": 25, "radio": 70},
            {"daño": 38, "radio": 90},
            {"daño": 55, "radio": 120},
            {"daño": 80, "radio": 160}
        ]
    },
    "TERERE": {
        "daño_base": 0,
        "cooldown": 4.0,
        "tipo": "buff",
        "niveles": [
            {"vida_por_seg": 3, "duracion": 6},
            {"vida_por_seg": 6, "duracion": 8},
            {"vida_por_seg": 10, "duracion": 12},
            {"vida_por_seg": 16, "duracion": 18}
        ]
    }
}

# ========== CONFIGURACIÓN DE MAPA ==========
TILE_SIZE = 64
MAPA_ANCHO_TILES = 20
MAPA_ALTO_TILES = 20
MAPA_ANCHO_PIXELES = MAPA_ANCHO_TILES * TILE_SIZE
MAPA_ALTO_PIXELES = MAPA_ALTO_TILES * TILE_SIZE

# ========== CONFIGURACIÓN DE CÁMARA ==========
CAMARA_VELOCIDAD_SEGUIMIENTO = 5

# ========== UI ==========
TAMAÑO_BARRA_VIDA = (250, 28)
POSICION_BARRA_VIDA = (20, 20)
TAMAÑO_BARRA_XP = (250, 16)
POSICION_BARRA_XP = (20, 55)

# ========== DROPS Y RECOMPENSAS ==========
CHANCE_DROP_VIDA = 0.05
VIDA_RECUPERADA_DROP = 20

# ========== DEBUG ==========
DEBUG_MODE = False
MOSTRAR_FPS = True

# ========== PROYECTILES ==========
PROYECTIL_HACHA_VELOCIDAD = 450
PROYECTIL_HACHA_ALCANCE = 500
PROYECTIL_HACHA_ROTACION = 720

# ========== KNOCKBACK ==========
KNOCKBACK_FUERZA_MACHETE = 120
KNOCKBACK_FUERZA_HACHA = 60
KNOCKBACK_FUERZA_AZADA = 220

# ========== INVULNERABILIDAD ==========
INVULNERABILIDAD_DURACION = 0.5

# ========== MEJORAS (más grandes) ==========
VIDA_BONUS_POR_NIVEL = 25
VELOCIDAD_BONUS_POR_NIVEL = 15
RADIO_RECOLECCION_BONUS = 25

# ========== LÍMITES ==========
MAX_ENEMIGOS_PANTALLA = 100
MAX_PROYECTILES = 200
MAX_ORBES_XP = 500
MAX_ARMAS_EQUIPADAS = 6

# ========== TILES ==========
TILE_COLORES = {
    "PASTO_OSCURO": (34, 139, 34),
    "PASTO_CLARO": (50, 205, 50),
    "PASTO_MEDIO": (60, 179, 113)
}

# ========== SPAWN ==========
SPAWN_MARGEN_PANTALLA = 100

# ========== MEJORAS VALORES (más grandes) ==========
MEJORAS_POR_NIVEL = 3
MEJORAS_VALORES = {
    "vida_max": 30,                 # Más vida por mejora
    "velocidad": 25,                # Más velocidad
    "radio_recoleccion": 25,        # Más radio
    "daño": 8,
    "cooldown_reduccion": 0.1
}

# ========== TIEMPO DE ENEMIGOS ESPECIALES ==========
TIEMPO_AGUARA_GUAZU = 180          # Aparece a los 3 minutos
TIEMPO_LUISON = 240                # Aparece a los 4 minutos

# ========== VERSIÓN ==========
VERSION_MAJOR = 1
VERSION_MINOR = 0
VERSION_PATCH = 0
VERSION_BUILD = "MVP"
VERSION_STRING = f"v{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}-{VERSION_BUILD}"

# ========== METADATA ==========
GAME_NAME = "Karai Survival"