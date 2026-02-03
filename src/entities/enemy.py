"""
ENEMY.PY - TODOS LOS TIPOS DE ENEMIGOS
=======================================
IA básica de persecución y diferentes tipos de fauna paraguaya
"""

import pygame
import random
import math
from entities.base_entity import BaseEntity
from settings import *

class Enemy(BaseEntity):
    """Clase de enemigo con IA básica de persecución"""
    
    def __init__(self, x, y, tipo):
        """
        Inicializar enemigo
        
        Args:
            x: Posición X inicial
            y: Posición Y inicial
            tipo: Tipo de enemigo (string)
        """
        # Obtener configuración del tipo de enemigo
        config = ENEMIGO_CONFIGS[tipo]
        
        # Definir color según tipo
        colores = {
            "AOAO": (0, 0, 255),          # Azul      
            "PORA": (255, 255, 0),        # Amarillo
            "YACARE": (0, 100, 0),          # Verde oscuro
            "LUISON": (80, 0, 0),           # Rojo oscuro
            "MOSQUITO": (100, 100, 100),    # Gris
            "POMBERO": (139, 90, 43),       # Marrón
            "SERPIENTE": (0, 128, 0)        # Verde
        }
        
        # Mapeo de sprites
        sprites = {
            "AOAO": "assets/sprites/aoao.png",
            "PORA": "assets/sprites/pora.png",
            "YACARE": "assets/sprites/yacare.png",
            "LUISON": "assets/sprites/luison.png",
            "MOSQUITO": "assets/sprites/mosquito.png",
            "POMBERO": "assets/sprites/pora.png",
            "SERPIENTE": "assets/sprites/serpiente.png"
        }
        
        # Llamar constructor padre con sprite
        super().__init__(x, y, config["ancho"], config["alto"], colores[tipo], sprite_path=sprites.get(tipo))

        # Configurar stats desde config
        self.tipo = tipo
        self.vida_maxima = config["vida"]
        self.vida_actual = config["vida"]
        self.velocidad = config["velocidad"]
        self.daño = config["daño"]
        self.xp_drop = config["xp"]

        # Flip del sprite según dirección
        self.imagen_original = self.image.copy() if self.image else None
        self.voltear_horizontalmente = False

        # Referencias
        self.jugador = None  # Se asigna desde spawn_manager

        # Timers de ataque
        self.cooldown_ataque = 1.0  # segundos
        self.timer_ataque = 0
        self.puede_atacar = True

        # Estado
        self.esta_atacando = False
    
    def perseguir_jugador(self, dt):
        """
        IA básica: moverse hacia el jugador

        Args:
            dt: Delta time en segundos
        """
        if self.jugador and self.jugador.esta_vivo:
            # Obtener dirección hacia jugador
            self.direccion = self.direccion_hacia(self.jugador)

            # Actualizar flip según dirección horizontal
            if self.direccion.x < 0:
                self.voltear_horizontalmente = True  # Mirando a la izquierda
            elif self.direccion.x > 0:
                self.voltear_horizontalmente = False  # Mirando a la derecha

            # Mover hacia el jugador
            self.mover(dt)
    
    def atacar_jugador(self):
        """Realizar ataque si está en rango"""
        if not self.puede_atacar:
            return
        
        if self.jugador and self.colisiona_con(self.jugador):
            self.jugador.recibir_daño(self.daño)
            self.puede_atacar = False
            self.timer_ataque = 0
            self.esta_atacando = True
    
    def actualizar_cooldown_ataque(self, dt):
        """
        Actualizar timer de ataque
        
        Args:
            dt: Delta time en segundos
        """
        if not self.puede_atacar:
            self.timer_ataque += dt
            
            if self.timer_ataque >= self.cooldown_ataque:
                self.puede_atacar = True
                self.timer_ataque = 0
                self.esta_atacando = False
    
    def al_morir(self):
        """Dropear XP cuando muere"""
        # El combat_manager creará el orbe de XP
        if self.jugador:
            self.jugador.enemigos_matados += 1
    
    def recibir_knockback(self, direccion, fuerza):
        """
        Retroceso al recibir daño

        Args:
            direccion: Vector de dirección del knockback
            fuerza: Fuerza del knockback en píxeles
        """
        self.x += direccion.x * fuerza
        self.y += direccion.y * fuerza
        self.rect.center = (int(self.x), int(self.y))

    def dibujar(self, pantalla, camara):
        """
        Dibujar enemigo con flip según dirección

        Args:
            pantalla: Surface de pygame
            camara: Objeto Camera
        """
        if self.imagen_original:
            # Aplicar flip horizontal si es necesario
            imagen_actual = pygame.transform.flip(self.imagen_original, self.voltear_horizontalmente, False)
            # Actualizar la imagen del enemigo
            self.image = imagen_actual

        # Llamar al método dibujar del padre
        super().dibujar(pantalla, camara)

    def actualizar(self, dt):
        """
        Actualización principal del enemigo
        
        Args:
            dt: Delta time en segundos
        """
        if not self.esta_vivo:
            return
        
        # Perseguir al jugador
        self.perseguir_jugador(dt)
        
        # Intentar atacar
        self.atacar_jugador()
        
        # Actualizar cooldowns
        self.actualizar_cooldown_ataque(dt)


class OrbXP:
    """Orbe de experiencia que se dropea al matar enemigos"""
    
    def __init__(self, x, y, cantidad):
        """
        Inicializar orbe de XP
        
        Args:
            x: Posición X
            y: Posición Y
            cantidad: Valor de XP del orbe
        """
        self.x = float(x)
        self.y = float(y)
        self.cantidad = cantidad  # Valor de XP
        
        # Crear sprite
        try:
            self.image = pygame.image.load("assets/sprites/orbe_xp.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (30, 30))
        except:
            self.image = pygame.Surface((20, 20))
            self.image.fill(COLOR_XP)
        
        self.rect = self.image.get_rect()
        self.rect.center = (int(x), int(y))
        
        # Animación
        self.tiempo_vida = 3
        self.flotando = True
    
    def actualizar(self, dt):
        """
        Animación de flotación
        
        Args:
            dt: Delta time en segundos
        """
        self.tiempo_vida += dt
        
        # Efecto de flotación sutil
        offset_y = math.sin(self.tiempo_vida * 3) * 2
        self.rect.centery = int(self.y + offset_y)
    
    def dibujar(self, pantalla, camara):
        """
        Dibujar orbe en pantalla
        
        Args:
            pantalla: Surface de pygame
            camara: Objeto Camera
        """
        pantalla_x = self.rect.x - camara.offset_x
        pantalla_y = self.rect.y - camara.offset_y
        
        # Solo dibujar si está en pantalla
        if -50 < pantalla_x < pantalla.get_width() + 50 and -50 < pantalla_y < pantalla.get_height() + 50:
            pantalla.blit(self.image, (pantalla_x, pantalla_y))
    
    def distancia_a(self, entidad):
        """
        Calcular distancia a una entidad
        
        Args:
            entidad: Objeto con atributos x, y
            
        Returns:
            float: Distancia en píxeles
        """
        dx = self.x - entidad.x
        dy = self.y - entidad.y
        return math.sqrt(dx * dx + dy * dy)
    
    def direccion_hacia(self, entidad):
        """
        Obtener dirección hacia una entidad
        
        Args:
            entidad: Objeto con atributos x, y
            
        Returns:
            Vector2: Vector normalizado hacia la entidad
        """
        vector = pygame.math.Vector2(
            entidad.x - self.x,
            entidad.y - self.y
        )
        
        if vector.length() > 0:
            return vector.normalize()
        
        return vector
    
    def colisiona_con(self, entidad):
        """
        Verificar colisión con una entidad
        
        Args:
            entidad: Objeto con atributo rect
            
        Returns:
            bool: True si hay colisión
        """
        return self.rect.colliderect(entidad.rect)