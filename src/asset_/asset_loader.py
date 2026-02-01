"""
ASSET_LOADER.PY - CARGADOR DE RECURSOS
=======================================
Gestión centralizada de sprites, sonidos y fuentes
"""

import pygame
import os
from src.settings import *

class AssetLoader:
    '''
    """
    PSEUDOCÓDIGO:
    
    __init__(self):
        # Directorios de assets
        self.dir_sprites = "assets/sprites"
        self.dir_sonidos = "assets/sounds"
        self.dir_musica = "assets/music"
        
        # Diccionarios de assets cargados
        self.sprites = {}
        self.sonidos = {}
        self.musica = {}
        
        # Verificar si existen los directorios
        self.verificar_directorios()
        
        # Cargar todos los assets
        self.cargar_sprites()
        self.cargar_sonidos()
        self.cargar_musica()
    
    
    def verificar_directorios(self):
        """
        Verificar que existan los directorios de assets
        
        PSEUDOCÓDIGO:
        directorios = [self.dir_sprites, self.dir_sonidos, self.dir_musica]
        
        PARA directorio EN directorios:
            SI NO os.path.exists(directorio):
                # Crear directorio si no existe
                os.makedirs(directorio)
                print(f"Creado directorio: {directorio}")
        """
        pass
    
    
    def cargar_sprites(self):
        """
        Cargar todos los sprites desde el directorio
        
        PSEUDOCÓDIGO:
        # Sprites del jugador
        self.cargar_sprite_jugador()
        
        # Sprites de enemigos
        self.cargar_sprites_enemigos()
        
        # Sprites de armas/proyectiles
        self.cargar_sprites_armas()
        
        # Sprites de UI
        self.cargar_sprites_ui()
        
        # Sprites de efectos
        self.cargar_sprites_efectos()
        
        print(f"Cargados {len(self.sprites)} sprites")
        """
        pass
    
    
    def cargar_sprite_jugador(self):
        """
        Cargar sprite del jugador
        
        PSEUDOCÓDIGO:
        ruta = os.path.join(self.dir_sprites, "player.png")
        
        SI os.path.exists(ruta):
            imagen = pygame.image.load(ruta).convert_alpha()
            # Escalar al tamaño deseado si es necesario
            imagen = pygame.transform.scale(imagen, (50, 50))
            self.sprites["player"] = imagen
        SINO:
            # Usar placeholder (cuadrado amarillo)
            placeholder = pygame.Surface((50, 50))
            placeholder.fill((255, 200, 0))
            self.sprites["player"] = placeholder
            print("ADVERTENCIA: player.png no encontrado, usando placeholder")
        """
        pass
    
    
    def cargar_sprites_enemigos(self):
        """
        Cargar sprites de todos los enemigos
        
        PSEUDOCÓDIGO:
        enemigos = ["carpincho", "yacare", "tatu", "aguara_guazu"]
        colores_placeholder = {
            "carpincho": (139, 69, 19),
            "yacare": (0, 100, 0),
            "tatu": (169, 169, 169),
            "aguara_guazu": (255, 69, 0)
        }
        
        PARA enemigo EN enemigos:
            ruta = os.path.join(self.dir_sprites, f"{enemigo}.png")
            
            SI os.path.exists(ruta):
                imagen = pygame.image.load(ruta).convert_alpha()
                imagen = pygame.transform.scale(imagen, (40, 40))
                self.sprites[enemigo] = imagen
            SINO:
                # Placeholder
                placeholder = pygame.Surface((40, 40))
                placeholder.fill(colores_placeholder[enemigo])
                self.sprites[enemigo] = placeholder
                print(f"ADVERTENCIA: {enemigo}.png no encontrado")
        """
        pass
    
    
    def cargar_sprites_armas(self):
        """
        Cargar sprites de armas y proyectiles
        
        PSEUDOCÓDIGO:
        armas = ["machete", "hacha", "azada", "terere"]
        
        PARA arma EN armas:
            ruta = os.path.join(self.dir_sprites, f"{arma}.png")
            
            SI os.path.exists(ruta):
                imagen = pygame.image.load(ruta).convert_alpha()
                imagen = pygame.transform.scale(imagen, (30, 30))
                self.sprites[arma] = imagen
            SINO:
                # Placeholder gris
                placeholder = pygame.Surface((30, 30))
                placeholder.fill((192, 192, 192))
                self.sprites[arma] = placeholder
        
        # Sprite de orbe XP
        ruta_orbe = os.path.join(self.dir_sprites, "orbe_xp.png")
        SI os.path.exists(ruta_orbe):
            imagen = pygame.image.load(ruta_orbe).convert_alpha()
            imagen = pygame.transform.scale(imagen, (10, 10))
            self.sprites["orbe_xp"] = imagen
        SINO:
            placeholder = pygame.Surface((10, 10))
            placeholder.fill(COLOR_XP)
            self.sprites["orbe_xp"] = placeholder
        """
        pass
    
    
    def cargar_sprites_ui(self):
        """
        Cargar sprites de UI (iconos, etc)
        
        PSEUDOCÓDIGO:
        ui_elementos = ["icono_vida", "icono_xp", "icono_nivel"]
        
        PARA elemento EN ui_elementos:
            ruta = os.path.join(self.dir_sprites, "ui", f"{elemento}.png")
            
            SI os.path.exists(ruta):
                imagen = pygame.image.load(ruta).convert_alpha()
                imagen = pygame.transform.scale(imagen, (20, 20))
                self.sprites[elemento] = imagen
        """
        pass
    
    
    def cargar_sprites_efectos(self):
        """
        Cargar sprites de efectos visuales
        
        PSEUDOCÓDIGO:
        efectos = ["impacto", "explosion", "particula"]
        
        PARA efecto EN efectos:
            ruta = os.path.join(self.dir_sprites, "efectos", f"{efecto}.png")
            
            SI os.path.exists(ruta):
                imagen = pygame.image.load(ruta).convert_alpha()
                self.sprites[efecto] = imagen
        """
        pass
    
    
    def cargar_sonidos(self):
        """
        Cargar todos los efectos de sonido
        
        PSEUDOCÓDIGO:
        sonidos_lista = [
            "golpe",
            "muerte_enemigo",
            "recolectar_xp",
            "subir_nivel",
            "game_over",
            "ataque_machete",
            "ataque_hacha",
            "ataque_azada"
        ]
        
        PARA nombre EN sonidos_lista:
            # Intentar cargar .wav primero, luego .ogg, luego .mp3
            extensiones = [".wav", ".ogg", ".mp3"]
            cargado = False
            
            PARA ext EN extensiones:
                ruta = os.path.join(self.dir_sonidos, nombre + ext)
                
                SI os.path.exists(ruta):
                    try:
                        sonido = pygame.mixer.Sound(ruta)
                        self.sonidos[nombre] = sonido
                        cargado = True
                        break
                    except:
                        print(f"Error al cargar {ruta}")
            
            SI NO cargado:
                # Crear sonido silencioso placeholder
                self.sonidos[nombre] = None
                print(f"ADVERTENCIA: Sonido '{nombre}' no encontrado")
        
        print(f"Cargados {len([s for s in self.sonidos.values() if s])} sonidos")
        """
        pass
    
    
    def cargar_musica(self):
        """
        Cargar archivos de música de fondo
        
        PSEUDOCÓDIGO:
        musicas = {
            "menu": "menu_theme.ogg",
            "gameplay": "gameplay_theme.ogg",
            "game_over": "game_over_theme.ogg"
        }
        
        PARA clave, archivo EN musicas.items():
            ruta = os.path.join(self.dir_musica, archivo)
            
            SI os.path.exists(ruta):
                self.musica[clave] = ruta
            SINO:
                self.musica[clave] = None
                print(f"ADVERTENCIA: Música '{archivo}' no encontrada")
        """
        pass
    
    
    def obtener_sprite(self, nombre):
        """
        Obtener un sprite por nombre
        
        PSEUDOCÓDIGO:
        SI nombre EN self.sprites:
            RETORNAR self.sprites[nombre]
        SINO:
            print(f"ERROR: Sprite '{nombre}' no existe")
            # Retornar sprite placeholder
            placeholder = pygame.Surface((32, 32))
            placeholder.fill((255, 0, 255))  # Magenta para indicar error
            RETORNAR placeholder
        """
        pass
    
    
    def reproducir_sonido(self, nombre, volumen=1.0):
        """
        Reproducir un efecto de sonido
        
        PSEUDOCÓDIGO:
        SI nombre EN self.sonidos Y self.sonidos[nombre]:
            try:
                self.sonidos[nombre].set_volume(volumen)
                self.sonidos[nombre].play()
            except:
                print(f"Error al reproducir sonido '{nombre}'")
        """
        pass
    
    
    def reproducir_musica(self, nombre, loop=-1, volumen=0.5):
        """
        Reproducir música de fondo
        
        PSEUDOCÓDIGO:
        SI nombre EN self.musica Y self.musica[nombre]:
            try:
                pygame.mixer.music.load(self.musica[nombre])
                pygame.mixer.music.set_volume(volumen)
                pygame.mixer.music.play(loop)  # -1 = loop infinito
            except:
                print(f"Error al reproducir música '{nombre}'")
        """
        pass
    
    
    def detener_musica(self):
        """
        Detener la música actual
        
        PSEUDOCÓDIGO:
        pygame.mixer.music.stop()
        """
        pass
    
    
    def pausar_musica(self):
        """
        Pausar la música actual
        
        PSEUDOCÓDIGO:
        pygame.mixer.music.pause()
        """
        pass
    
    
    def reanudar_musica(self):
        """
        Reanudar la música pausada
        
        PSEUDOCÓDIGO:
        pygame.mixer.music.unpause()
        """
        pass
    
    
    def establecer_volumen_general(self, volumen):
        """
        Establecer volumen general de efectos de sonido
        
        PSEUDOCÓDIGO:
        PARA sonido EN self.sonidos.values():
            SI sonido:
                sonido.set_volume(volumen)
        """
        pass
    
    
    def limpiar(self):
        """
        Liberar recursos de memoria
        
        PSEUDOCÓDIGO:
        # Limpiar sprites
        self.sprites.clear()
        
        # Detener y limpiar sonidos
        pygame.mixer.music.stop()
        PARA sonido EN self.sonidos.values():
            SI sonido:
                sonido.stop()
        self.sonidos.clear()
        
        print("Assets liberados de memoria")
        """
        pass


# ========== INSTANCIA GLOBAL ==========
"""
Para usar en todo el proyecto:

# En main.py al inicio:
assets = AssetLoader()

# Para obtener sprites:
sprite_player = assets.obtener_sprite("player")
sprite_carpincho = assets.obtener_sprite("carpincho")

# Para reproducir sonidos:
assets.reproducir_sonido("golpe", volumen=0.7)
assets.reproducir_sonido("recolectar_xp")

# Para música:
assets.reproducir_musica("gameplay", volumen=0.3)
assets.pausar_musica()
assets.reanudar_musica()
assets.detener_musica()
"""
```

Este archivo incluye:

✅ **Carga automática de sprites**:
- Jugador, enemigos, armas, UI, efectos
- Sistema de placeholders si no existen las imágenes
- Escalado automático a tamaños correctos

✅ **Carga de sonidos**:
- Soporta .wav, .ogg, .mp3
- Efectos de sonido (golpes, XP, nivel)
- Sistema de volumen por sonido

✅ **Carga de música**:
- Música de fondo por estado (menú, gameplay, game over)
- Control completo (play, pause, stop)
- Sistema de loop

✅ **Funciones de utilidad**:
- `obtener_sprite()` - Obtener sprite por nombre
- `reproducir_sonido()` - Reproducir efecto
- `reproducir_musica()` - Reproducir música
- `establecer_volumen_general()` - Control de volumen
- `limpiar()` - Liberar memoria

**Estructura de carpetas necesaria:**
```
assets/
├── sprites/
│   ├── player.png
│   ├── carpincho.png
│   ├── yacare.png
│   ├── tatu.png
│   ├── aguara_guazu.png
│   ├── machete.png
│   ├── hacha.png
│   ├── azada.png
│   ├── terere.png
│   ├── orbe_xp.png
│   └── ui/
│       └── (iconos opcionales)
├── sounds/
│   ├── golpe.wav
│   ├── muerte_enemigo.wav
│   ├── recolectar_xp.wav
│   └── subir_nivel.wav
└── music/
    ├── menu_theme.ogg
    ├── gameplay_theme.ogg
    └── game_over_theme.ogg
    
    '''