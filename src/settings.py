"""
SETTINGS.PY - CONFIGURACIÓN GLOBAL DEL JUEGO
============================================
Todas las constantes y configuraciones del juego
"""

# ========== CONFIGURACIÓN DE PANTALLA ==========
ANCHO_VENTANA = 1280
ALTO_VENTANA = 720
FPS = 60
TITULO_JUEGO = "Campesino Paraguayo: Survival"

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
            {"daño": 25, "cantidad": 1},
            {"daño": 35, "cantidad": 2},
            {"daño": 50, "cantidad": 3},
            {"daño": 75, "cantidad": 4}
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
ZONA_MUERTA_CAMARA = 100  # Píxeles de "zona muerta" para movimiento suave

# ========== COLISIONES ==========
DISTANCIA_COLISION_JUGADOR = 40
DISTANCIA_COLISION_ENEMIGO = 30

# ========== UI ==========
TAMAÑO_BARRA_VIDA = (300, 30)
POSICION_BARRA_VIDA = (20, 20)
TAMAÑO_BARRA_XP = (300, 20)
POSICION_BARRA_XP = (20, 60)
TAMAÑO_FUENTE_STATS = 24
TAMAÑO_FUENTE_NIVEL = 18

# ========== DROPS Y RECOMPENSAS ==========
CHANCE_DROP_VIDA = 0.05  # 5% de chance de drop de vida al matar
VIDA_RECUPERADA_DROP = 20
XP_MULTIPLICADOR_NIVEL = 1.0  # Se puede ajustar según nivel

# ========== DEBUG ==========
DEBUG_MODE = False  # Cambiar a True para ver hitboxes y info
MOSTRAR_FPS = True

# ========== CONFIGURACIÓN DE AUDIO ==========
VOLUMEN_MUSICA = 0.3
VOLUMEN_SFX = 0.7

# ========== CONFIGURACIÓN DE PROYECTILES ==========
PROYECTIL_HACHA_VELOCIDAD = 400  # píxeles por segundo
PROYECTIL_HACHA_ALCANCE = 500  # distancia máxima
PROYECTIL_HACHA_ROTACION = 720  # grados por segundo

# ========== CONFIGURACIÓN DE EFECTOS ==========
EFECTO_IMPACTO_DURACION = 0.3  # segundos
EFECTO_PARTICULA_VIDA = 1.0  # segundos
EFECTO_PARTICULA_CANTIDAD = 5  # partículas por efecto

# ========== CONFIGURACIÓN DE KNOCKBACK ==========
KNOCKBACK_FUERZA_BASE = 100  # píxeles de retroceso
KNOCKBACK_FUERZA_MACHETE = 100
KNOCKBACK_FUERZA_HACHA = 50
KNOCKBACK_FUERZA_AZADA = 200

# ========== CONFIGURACIÓN DE INVULNERABILIDAD ==========
INVULNERABILIDAD_DURACION = 0.5  # segundos después de recibir daño

# ========== CONFIGURACIÓN DE OLEADAS ESPECIALES ==========
OLEADA_BOSS_INTERVALO = 600  # segundos (10 minutos)
OLEADA_ELITE_INTERVALO = 180  # segundos (3 minutos)

# ========== CONFIGURACIÓN DE BALANCEO ==========
VIDA_BONUS_POR_NIVEL = 20  # Vida extra al subir nivel
VELOCIDAD_BONUS_POR_NIVEL = 10  # Velocidad extra al mejorar
RADIO_RECOLECCION_BONUS = 20  # Radio extra al mejorar

# ========== LÍMITES DEL JUEGO ==========
MAX_ENEMIGOS_PANTALLA = 300
MAX_PROYECTILES = 200
MAX_ORBES_XP = 500
MAX_NIVEL = 100
MAX_ARMAS_EQUIPADAS = 6

# ========== CONFIGURACIÓN DE TILES DEL MAPA ==========
TILE_COLORES = {
    "PASTO_OSCURO": (34, 139, 34),   # Verde oscuro
    "PASTO_CLARO": (50, 205, 50),    # Verde claro
    "PASTO_MEDIO": (60, 179, 113),   # Verde medio
    "TIERRA": (139, 90, 43),         # Marrón
    "AGUA": (65, 105, 225)           # Azul
}

# ========== CONFIGURACIÓN DE SPAWN DE ENEMIGOS ==========
SPAWN_MARGEN_PANTALLA = 100  # Píxeles fuera de pantalla para spawn
SPAWN_DISTANCIA_MINIMA_JUGADOR = 150  # No spawnear muy cerca del jugador

# ========== CONFIGURACIÓN DE MEJORAS ==========
MEJORAS_POR_NIVEL = 3  # Cantidad de opciones al subir nivel
MEJORAS_VALORES = {
    "vida_max": 20,
    "velocidad": 20,
    "radio_recoleccion": 20,
    "daño": 5,
    "cooldown_reduccion": 0.1
}

# ========== CONFIGURACIÓN DE ANIMACIONES ==========
ANIMACION_PARPADEO_VELOCIDAD = 10  # Velocidad de parpadeo al recibir daño
ANIMACION_ORBE_XP_VELOCIDAD = 3  # Velocidad de flotación de orbes
ANIMACION_ORBE_XP_AMPLITUD = 2  # Amplitud de flotación

# ========== CONFIGURACIÓN DE SONIDOS ==========
SONIDOS_DISPONIBLES = [
    "golpe",
    "muerte_enemigo",
    "recolectar_xp",
    "subir_nivel",
    "game_over",
    "ataque_machete",
    "ataque_hacha",
    "ataque_azada",
    "recibir_daño",
    "click_ui"
]

# ========== CONFIGURACIÓN DE MÚSICA ==========
MUSICAS_DISPONIBLES = {
    "menu": "menu_theme",
    "gameplay": "gameplay_theme",
    "game_over": "game_over_theme"
}

# ========== CONFIGURACIÓN DE DIFICULTAD ==========
DIFICULTAD_ESCALADO = {
    "vida_enemigos": 1.1,  # +10% cada minuto
    "daño_enemigos": 1.05,  # +5% cada minuto
    "velocidad_enemigos": 1.03,  # +3% cada minuto
    "spawn_rate": 0.95  # -5% tiempo entre spawns cada minuto
}

# ========== CONFIGURACIÓN DE PARTÍCULAS ==========
PARTICULA_VELOCIDAD_MIN = 50
PARTICULA_VELOCIDAD_MAX = 200
PARTICULA_TAMAÑO_MIN = 2
PARTICULA_TAMAÑO_MAX = 8
PARTICULA_VIDA_MIN = 0.1
PARTICULA_VIDA_MAX = 1.0

# ========== CONFIGURACIÓN DE CÁMARA SHAKE ==========
SHAKE_INTENSIDAD_GOLPE = 3
SHAKE_INTENSIDAD_MUERTE = 7
SHAKE_INTENSIDAD_BOSS = 15
SHAKE_DURACION_DEFAULT = 0.3

# ========== CONFIGURACIÓN DE UI AVANZADA ==========
UI_OVERLAY_ALPHA = 200
UI_MENU_ALPHA = 180
UI_CARD_ANCHO = 300
UI_CARD_ALTO = 400
UI_CARD_ESPACIO = 50
UI_CARD_HOVER_SCALE = 1.05

# ========== CONFIGURACIÓN DE COLORES EXTENDIDOS ==========
COLOR_RAREZA = {
    "COMUN": (200, 200, 200),
    "POCO_COMUN": (30, 255, 0),
    "RARO": (0, 112, 221),
    "EPICO": (163, 53, 238),
    "LEGENDARIO": (255, 128, 0)
}

COLOR_ESTADO = {
    "POSITIVO": (0, 255, 0),
    "NEGATIVO": (255, 0, 0),
    "NEUTRAL": (200, 200, 200),
    "ADVERTENCIA": (255, 255, 0)
}

COLOR_BOTONES = {
    "NORMAL": (60, 60, 60),
    "HOVER": (80, 80, 80),
    "PRESIONADO": (40, 40, 40),
    "DESHABILITADO": (30, 30, 30)
}

# ========== CONFIGURACIÓN DE PATHS ==========
PATH_ASSETS = "assets/"
PATH_SPRITES = "assets/sprites/"
PATH_SONIDOS = "assets/sounds/"
PATH_MUSICA = "assets/music/"
PATH_FUENTES = "assets/fonts/"
PATH_DATOS = "data/"

# ========== CONFIGURACIÓN DE GUARDADO ==========
ARCHIVO_CONFIG = "data/config.json"
ARCHIVO_HIGHSCORES = "data/highscores.json"
ARCHIVO_ESTADISTICAS = "data/stats.json"

# ========== CONFIGURACIÓN DE DESARROLLO ==========
MODO_DESARROLLO = False  # Activa características de desarrollo
GODMODE = False  # Invencibilidad
XP_INFINITO = False  # XP instantánea
SPAWN_INSTANTANEO = False  # Spawn sin cooldown

# ========== INFORMACIÓN DE VERSIÓN ==========
VERSION_MAJOR = 1
VERSION_MINOR = 0
VERSION_PATCH = 0
VERSION_BUILD = "MVP"
VERSION_STRING = f"v{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}-{VERSION_BUILD}"

# ========== METADATA DEL JUEGO ==========
GAME_NAME = "Karai Survival"
GAME_NAME_SHORT = "Karai Survival"
DEVELOPER = "Equipo Hackaton"
YEAR = 2025
GENRE = "Roguelike, Acción, Supervivencia"
PLATFORM = "PC (Windows/Linux/Mac)"

# ========== CONFIGURACIÓN DE LOGS ==========
LOG_NIVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_ARCHIVO = "game.log"
LOG_CONSOLA = True

# ========== CONFIGURACIÓN DE PERFORMANCE ==========
VSYNC = True  # Sincronización vertical
RENDER_DISTANCE = 1000  # Distancia máxima de renderizado
CULLING_ENABLED = True  # Activar culling de objetos fuera de pantalla

# ========== CONFIGURACIÓN DE CONTROLES ==========
CONTROLES = {
    "ARRIBA": ['w', 'up'],
    "ABAJO": ['s', 'down'],
    "IZQUIERDA": ['a', 'left'],
    "DERECHA": ['d', 'right'],
    "PAUSA": ['escape', 'p'],
    "CONFIRMAR": ['space', 'return'],
    "CANCELAR": ['escape'],
    "DEBUG_XP": ['f1'],
    "DEBUG_BOSS": ['f2'],
    "DEBUG_HEAL": ['f3']
}

# ========== CONFIGURACIÓN DE ESTADÍSTICAS ==========
STATS_RASTREADAS = [
    "tiempo_total_jugado",
    "enemigos_totales_matados",
    "nivel_maximo_alcanzado",
    "tiempo_supervivencia_record",
    "partidas_jugadas",
    "partidas_ganadas",
    "daño_total_infligido",
    "daño_total_recibido",
    "xp_total_recolectada"
]

# ========== NOTAS DE DESARROLLO ==========
"""
NOTAS PARA EL EQUIPO:

1. Para cambiar la dificultad del juego, ajustar:
   - TIEMPO_ENTRE_SPAWNS (más bajo = más difícil)
   - ENEMIGO_CONFIGS (stats de enemigos)
   - CAMPESINO_VIDA_MAX (vida del jugador)

2. Para balancear armas:
   - Ajustar ARMAS_CONFIG
   - Modificar cooldowns y daño

3. Para debugging:
   - Activar DEBUG_MODE = True
   - Usar teclas F1, F2, F3 en el juego

4. Para optimización:
   - Reducir MAX_ENEMIGOS_PANTALLA si hay lag
   - Ajustar RENDER_DISTANCE

5. El mapa es de 6400x6400 píxeles (100x100 tiles de 64x64)
   - Puedes cambiar MAPA_ANCHO_TILES y MAPA_ALTO_TILES
   - O cambiar TILE_SIZE para tiles más grandes/pequeños
"""