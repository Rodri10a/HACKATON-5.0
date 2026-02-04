"""
ASSET_LOADER.PY - CARGADOR DE RECURSOS
=======================================
Gestión centralizada de sprites, sonidos y fuentes
"""

import pygame
import os
from settings import *


class AssetLoader:
    """Cargador centralizado de recursos del juego"""
    
    def __init__(self):
        """Inicializar asset loader"""
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
        
        print(f"Assets cargados: {len(self.sprites)} sprites, {len([s for s in self.sonidos.values() if s])} sonidos")
    
    def verificar_directorios(self):
        """Verificar que existan los directorios de assets"""
        directorios = [self.dir_sprites, self.dir_sonidos, self.dir_musica]
        
        for directorio in directorios:
            if not os.path.exists(directorio):
                # Crear directorio si no existe
                os.makedirs(directorio)
                print(f"Creado directorio: {directorio}")
    
    def cargar_sprites(self):
        """Cargar todos los sprites desde el directorio"""
        # Sprites del jugador
        self.cargar_sprite_jugador()
        
        # Sprites de enemigos
        self.cargar_sprites_enemigos()
        
        # Sprites de armas/proyectiles
        self.cargar_sprites_armas()
        
        # Sprites de efectos
        self.cargar_sprites_efectos()
    
    def cargar_sprite_jugador(self):
        """Cargar sprites de animación del jugador"""
        # Cargar frames de animación del jugador
        frames_jugador = []
        for i in range(1, 3):  # Cargar player.png y player_2.png
            ruta = os.path.join(self.dir_sprites, f"player{'' if i == 1 else '_' + str(i)}.png")
            
            if os.path.exists(ruta):
                imagen = pygame.image.load(ruta).convert_alpha()
                # Escalar al tamaño deseado (50x120 para coincidir con hitbox)
                imagen = pygame.transform.scale(imagen, (75, 180))
                frames_jugador.append(imagen)
            else:
                # Usar placeholder (rectángulo amarillo)
                placeholder = pygame.Surface((75, 180))
                placeholder.fill((255, 200, 0))
                frames_jugador.append(placeholder)
        
        # Guardar frames de animación
        self.sprites["player_frames"] = frames_jugador
        # También guardar el primer frame como "player" para compatibilidad
        self.sprites["player"] = frames_jugador[0]
    
    def cargar_sprites_enemigos(self):
        """Cargar sprites de todos los enemigos"""
        enemigos = ["carpincho", "yacare", "tatu", "aguara_guazu"]
        colores_placeholder = {
            "carpincho": (139, 69, 19),
            "yacare": (0, 100, 0),
            "tatu": (169, 169, 169),
            "aguara_guazu": (255, 69, 0)
        }
        
        for enemigo in enemigos:
            ruta = os.path.join(self.dir_sprites, f"{enemigo}.png")
            
            if os.path.exists(ruta):
                imagen = pygame.image.load(ruta).convert_alpha()
                imagen = pygame.transform.scale(imagen, (40, 40))
                self.sprites[enemigo] = imagen
            else:
                # Placeholder
                placeholder = pygame.Surface((40, 40))
                placeholder.fill(colores_placeholder[enemigo])
                self.sprites[enemigo] = placeholder
    
    def cargar_sprites_armas(self):
        """Cargar sprites de armas y proyectiles"""
        armas = ["machete", "rifle", "carrulim", "terere"]
        
        for arma in armas:
            ruta = os.path.join(self.dir_sprites, f"{arma}.png")
            
            if os.path.exists(ruta):
                imagen = pygame.image.load(ruta).convert_alpha()
                imagen = pygame.transform.scale(imagen, (30, 30))
                self.sprites[arma] = imagen
            else:
                # Placeholder gris
                placeholder = pygame.Surface((30, 30))
                placeholder.fill((192, 192, 192))
                self.sprites[arma] = placeholder
        
        # Sprite de orbe XP
        ruta_orbe = os.path.join(self.dir_sprites, "orbe_xp.png")
        if os.path.exists(ruta_orbe):
            imagen = pygame.image.load(ruta_orbe).convert_alpha()
            imagen = pygame.transform.scale(imagen, (10, 10))
            self.sprites["orbe_xp"] = imagen
        else:
            placeholder = pygame.Surface((10, 10))
            placeholder.fill(COLOR_XP)
            self.sprites["orbe_xp"] = placeholder
    
    def cargar_sprites_efectos(self):
        """Cargar sprites de efectos visuales"""
        efectos = ["impacto", "explosion", "particula"]
        
        for efecto in efectos:
            ruta = os.path.join(self.dir_sprites, "efectos", f"{efecto}.png")
            
            if os.path.exists(ruta):
                imagen = pygame.image.load(ruta).convert_alpha()
                self.sprites[efecto] = imagen
    
    def cargar_sonidos(self):
        """Cargar todos los efectos de sonido"""
        sonidos_lista = [
            "golpe",
            "muerte_enemigo",
            "recolectar_xp",
            "subir_nivel",
            "game_over",
            "ataque_machete",
            "ataque_rifle",
            "ataque_fuego"
        ]
        
        for nombre in sonidos_lista:
            # Intentar cargar .wav primero, luego .ogg, luego .mp3
            extensiones = [".wav", ".ogg", ".mp3"]
            cargado = False
            
            for ext in extensiones:
                ruta = os.path.join(self.dir_sonidos, nombre + ext)
                
                if os.path.exists(ruta):
                    try:
                        sonido = pygame.mixer.Sound(ruta)
                        self.sonidos[nombre] = sonido
                        cargado = True
                        break
                    except:
                        pass
            
            if not cargado:
                # Crear sonido placeholder (silencioso)
                self.sonidos[nombre] = None
    
    def cargar_musica(self):
        """Cargar archivos de música de fondo"""
        musicas = {
            "menu": "menu_theme.mp3",
            "gameplay": "gameplay_theme.mp3",
            "game_over": "game_over_theme.mp3"
        }
        
        for clave, archivo in musicas.items():
            ruta = os.path.join(self.dir_musica, archivo)
            
            if os.path.exists(ruta):
                self.musica[clave] = ruta
            else:
                self.musica[clave] = None
    
    def obtener_sprite(self, nombre):
        """
        Obtener un sprite por nombre
        
        Args:
            nombre: Nombre del sprite
            
        Returns:
            Surface: Sprite solicitado
        """
        if nombre in self.sprites:
            return self.sprites[nombre]
        else:
            # Retornar sprite placeholder
            placeholder = pygame.Surface((32, 32))
            placeholder.fill((255, 0, 255))  # Magenta para indicar error
            return placeholder
    
    def reproducir_sonido(self, nombre, volumen=1.0):
        """
        Reproducir un efecto de sonido
        
        Args:
            nombre: Nombre del sonido
            volumen: Volumen (0.0 a 1.0)
        """
        if nombre in self.sonidos and self.sonidos[nombre]:
            try:
                self.sonidos[nombre].set_volume(volumen)
                self.sonidos[nombre].play()
            except:
                pass
    
    def reproducir_musica(self, nombre, loop=-1, volumen=0.5):
        """
        Reproducir música de fondo
        
        Args:
            nombre: Nombre de la música
            loop: Número de loops (-1 = infinito)
            volumen: Volumen (0.0 a 1.0)
        """
        if nombre in self.musica and self.musica[nombre]:
            try:
                pygame.mixer.music.load(self.musica[nombre])
                pygame.mixer.music.set_volume(volumen)
                pygame.mixer.music.play(loop)
            except:
                pass
    
    def detener_musica(self):
        """Detener la música actual"""
        try:
            pygame.mixer.music.stop()
        except:
            pass
    
    def pausar_musica(self):
        """Pausar la música actual"""
        try:
            pygame.mixer.music.pause()
        except:
            pass
    
    def reanudar_musica(self):
        """Reanudar la música pausada"""
        try:
            pygame.mixer.music.unpause()
        except:
            pass
    
    def establecer_volumen_general(self, volumen):
        """
        Establecer volumen general de efectos de sonido
        
        Args:
            volumen: Volumen (0.0 a 1.0)
        """
        for sonido in self.sonidos.values():
            if sonido:
                try:
                    sonido.set_volume(volumen)
                except:
                    pass
    
    def limpiar(self):
        """Liberar recursos de memoria"""
        # Limpiar sprites
        self.sprites.clear()
        
        # Detener y limpiar sonidos
        try:
            pygame.mixer.music.stop()
        except:
            pass
        
        for sonido in self.sonidos.values():
            if sonido:
                try:
                    sonido.stop()
                except:
                    pass
        
        self.sonidos.clear()
        
        print("Assets liberados de memoria")