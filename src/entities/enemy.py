"""
ENEMY.PY - TODOS LOS TIPOS DE ENEMIGOS
=======================================
IA básica de persecución y diferentes tipos de fauna paraguaya
"""

import pygame
import random
from base_entity import BaseEntity
from src.settings import *

class Enemy(BaseEntity):
    '''
    """
    PSEUDOCÓDIGO:
    
    __init__(self, x, y, tipo):
        # Obtener configuración del tipo de enemigo
        config = ENEMIGO_CONFIGS[tipo]
        
        # Definir color según tipo
        colores = {
            "CARPINCHO": (139, 69, 19),     # Marrón
            "YACARE": (0, 100, 0),          # Verde oscuro
            "TATU": (169, 169, 169),        # Gris
            "AGUARA_GUAZU": (255, 69, 0)    # Naranja-rojo
        }
        
        # Llamar constructor padre
        super().__init__(x, y, 40, 40, colores[tipo])
        
        # Configurar stats desde config
        self.tipo = tipo
        self.vida_maxima = config["vida"]
        self.vida_actual = config["vida"]
        self.velocidad = config["velocidad"]
        self.daño = config["daño"]
        self.xp_drop = config["xp"]
        
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
        
        PSEUDOCÓDIGO:
        SI self.jugador Y self.jugador.esta_vivo:
            # Obtener dirección hacia jugador
            self.direccion = self.direccion_hacia(self.jugador)
            
            # Mover hacia el jugador
            self.mover(dt)
        """
        pass
    
    
    def atacar_jugador(self):
        """
        Realizar ataque si está en rango
        
        PSEUDOCÓDIGO:
        SI NO self.puede_atacar:
            RETORNAR
        
        SI self.colisiona_con(self.jugador):
            self.jugador.recibir_daño(self.daño)
            self.puede_atacar = False
            self.timer_ataque = 0
            self.esta_atacando = True
        """
        pass
    
    
    def actualizar_cooldown_ataque(self, dt):
        """
        Actualizar timer de ataque
        
        PSEUDOCÓDIGO:
        SI NO self.puede_atacar:
            self.timer_ataque += dt
            
            SI self.timer_ataque >= self.cooldown_ataque:
                self.puede_atacar = True
                self.timer_ataque = 0
                self.esta_atacando = False
        """
        pass
    
    
    def al_morir(self):
        """
        Dropear XP cuando muere
        
        PSEUDOCÓDIGO:
        # Crear orbe de XP en esta posición
        orbe = OrbXP(self.x, self.y, self.xp_drop)
        
        # Agregar a lista global de orbes (se maneja en combat_manager)
        # combat_manager.orbes_xp.append(orbe)
        
        # Aumentar contador de enemigos matados del jugador
        SI self.jugador:
            self.jugador.enemigos_matados += 1
        """
        pass
    
    
    def recibir_knockback(self, direccion, fuerza):
        """
        Retroceso al recibir daño
        
        PSEUDOCÓDIGO:
        # Aplicar fuerza en dirección opuesta
        self.x += direccion.x * fuerza
        self.y += direccion.y * fuerza
        self.rect.center = (int(self.x), int(self.y))
        """
        pass
    
    
    def actualizar(self, dt):
        """
        Actualización principal del enemigo
        
        PSEUDOCÓDIGO:
        SI NO self.esta_vivo:
            RETORNAR
        
        # Perseguir al jugador
        self.perseguir_jugador(dt)
        
        # Intentar atacar
        self.atacar_jugador()
        
        # Actualizar cooldowns
        self.actualizar_cooldown_ataque(dt)
        """
        pass


class OrbXP:
    """
    Orbe de experiencia que se dropea al matar enemigos
    
    PSEUDOCÓDIGO:
    
    __init__(self, x, y, cantidad):
        self.x = x
        self.y = y
        self.cantidad = cantidad  # Valor de XP
        
        # Crear sprite pequeño dorado
        self.image = pygame.Surface((10, 10))
        self.image.fill(COLOR_XP)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Animación (opcional para MVP)
        self.tiempo_vida = 0
        self.flotando = True
    
    
    def actualizar(self, dt):
        """
        Animación de flotación
        
        PSEUDOCÓDIGO:
        self.tiempo_vida += dt
        
        # Efecto de flotación sutil
        offset_y = math.sin(self.tiempo_vida * 3) * 2
        self.rect.centery = int(self.y + offset_y)
        """
        pass
    
    
    def dibujar(self, pantalla, camara):
        """
        Dibujar orbe en pantalla
        
        PSEUDOCÓDIGO:
        pantalla_x = self.rect.x - camara.offset_x
        pantalla_y = self.rect.y - camara.offset_y
        
        SI esta_en_pantalla(pantalla_x, pantalla_y):
            pantalla.blit(self.image, (pantalla_x, pantalla_y))
        """
        pass


# ========== VARIACIONES ESPECIALES (para expansión futura) ==========
"""
Estas clases pueden heredar de Enemy y sobrescribir comportamientos

class CarpionchoElite(Enemy):
    # Carpincho más grande y rápido que aparece cada 5 minutos
    
class YacareAcorazado(Enemy):
    # Yacaré con más vida que solo recibe daño por detrás
    
class TatuExcavador(Enemy):
    # Tatú que puede atravesar el jugador y aparecer detrás
    
class AguaraGuazuAlfa(Enemy):
    # Boss que aparece cada 10 minutos
    # Tiene ataques especiales y dropea mucho XP
"""
'''