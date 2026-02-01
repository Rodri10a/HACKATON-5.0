"""
WEAPON.PY - SISTEMA DE ARMAS Y HERRAMIENTAS
============================================
Diferentes armas con comportamientos únicos
"""

import pygame
import math
import random
from src.settings import *

class Weapon:
    '''
    """
    PSEUDOCÓDIGO:
    
    __init__(self, tipo, dueño):
        self.tipo = tipo  # "MACHETE", "HACHA", "AZADA", "TERERE"
        self.dueño = dueño  # Referencia al jugador
        
        # Cargar configuración del arma
        self.config = ARMAS_CONFIG[tipo]
        
        # Nivel del arma
        self.nivel = 1
        self.nivel_maximo = len(self.config["niveles"])
        
        # Stats actuales (del nivel 1)
        self.stats = self.config["niveles"][0].copy()
        
        # Cooldown
        self.cooldown = self.config["cooldown"]
        self.timer_cooldown = 0
        self.puede_usar = True
        
        # Proyectiles activos (para armas de proyectiles)
        self.proyectiles = []
    
    
    def subir_nivel(self):
        """
        Aumentar nivel del arma y mejorar stats
        
        PSEUDOCÓDIGO:
        SI self.nivel < self.nivel_maximo:
            self.nivel += 1
            # Actualizar stats al nuevo nivel
            self.stats = self.config["niveles"][self.nivel - 1].copy()
        """
        pass
    
    
    def actualizar(self, dt, enemigos):
        """
        Actualizar cooldown y lógica del arma
        
        PSEUDOCÓDIGO:
        # Actualizar cooldown
        SI NO self.puede_usar:
            self.timer_cooldown += dt
            SI self.timer_cooldown >= self.cooldown:
                self.puede_usar = True
                self.timer_cooldown = 0
        
        # SI puede usar, usar automáticamente
        SI self.puede_usar Y hay enemigos cercanos:
            self.usar(enemigos)
        
        # Actualizar proyectiles si los hay
        PARA CADA proyectil EN self.proyectiles:
            proyectil.actualizar(dt)
            SI proyectil.debe_eliminarse:
                self.proyectiles.remove(proyectil)
        """
        pass
    
    
    def usar(self, enemigos):
        """
        Usar el arma según su tipo
        
        PSEUDOCÓDIGO:
        SI self.tipo == "MACHETE":
            self.ataque_machete(enemigos)
        
        SINO SI self.tipo == "HACHA":
            self.ataque_hacha(enemigos)
        
        SINO SI self.tipo == "AZADA":
            self.ataque_azada(enemigos)
        
        SINO SI self.tipo == "TERERE":
            self.buff_terere()
        
        # Marcar en cooldown
        self.puede_usar = False
        self.timer_cooldown = 0
        """
        pass
    
    
    def ataque_machete(self, enemigos):
        """
        Ataque melee en área circular alrededor del jugador
        
        PSEUDOCÓDIGO:
        alcance = self.stats["alcance"]
        daño = self.stats["daño"]
        
        PARA CADA enemigo EN enemigos:
            distancia = self.dueño.distancia_a(enemigo)
            
            SI distancia <= alcance:
                # Aplicar daño
                enemigo.recibir_daño(daño)
                
                # Aplicar knockback
                direccion = self.dueño.direccion_hacia(enemigo)
                enemigo.recibir_knockback(direccion, fuerza=100)
        """
        pass
    
    
    def ataque_hacha(self, enemigos):
        """
        Lanzar hacha(s) giratoria(s) hacia enemigos
        
        PSEUDOCÓDIGO:
        cantidad = self.stats["cantidad"]  # Número de hachas
        daño = self.stats["daño"]
        
        # Encontrar enemigos más cercanos
        enemigos_ordenados = sorted(enemigos, 
                                    key=lambda e: self.dueño.distancia_a(e))
        
        # Lanzar un hacha hacia cada enemigo cercano
        PARA i EN range(min(cantidad, len(enemigos_ordenados))):
            enemigo_objetivo = enemigos_ordenados[i]
            
            # Crear proyectil
            direccion = self.dueño.direccion_hacia(enemigo_objetivo)
            proyectil = ProyectilHacha(
                self.dueño.x, 
                self.dueño.y, 
                direccion, 
                daño
            )
            self.proyectiles.append(proyectil)
        """
        pass
    
    
    def ataque_azada(self, enemigos):
        """
        Ataque AoE (Área de Efecto) que daña a todos en un radio
        
        PSEUDOCÓDIGO:
        radio = self.stats["radio"]
        daño = self.stats["daño"]
        
        # Crear efecto visual (círculo expandiéndose)
        efecto = EfectoAzada(self.dueño.x, self.dueño.y, radio)
        
        PARA CADA enemigo EN enemigos:
            distancia = self.dueño.distancia_a(enemigo)
            
            SI distancia <= radio:
                enemigo.recibir_daño(daño)
                
                # Knockback fuerte desde el centro
                direccion = self.dueño.direccion_hacia(enemigo)
                enemigo.recibir_knockback(direccion, fuerza=200)
        """
        pass
    
    
    def buff_terere(self):
        """
        Buff de regeneración de vida
        
        PSEUDOCÓDIGO:
        vida_por_seg = self.stats["vida_por_seg"]
        duracion = self.stats["duracion"]
        
        # Aplicar buff al jugador
        self.dueño.aplicar_buff_regeneracion(vida_por_seg, duracion)
        
        # Efecto visual (aura verde alrededor del jugador)
        """
        pass
    
    
    def dibujar(self, pantalla, camara):
        """
        Dibujar proyectiles y efectos del arma
        
        PSEUDOCÓDIGO:
        # Dibujar proyectiles activos
        PARA CADA proyectil EN self.proyectiles:
            proyectil.dibujar(pantalla, camara)
        """
        pass


class ProyectilHacha:
    """
    Proyectil de hacha giratoria
    
    PSEUDOCÓDIGO:
    
    __init__(self, x, y, direccion, daño):
        self.x = x
        self.y = y
        self.direccion = direccion
        self.daño = daño
        
        # Stats del proyectil
        self.velocidad = 400  # píxeles por segundo
        self.alcance_maximo = 500  # distancia máxima
        self.distancia_recorrida = 0
        
        # Sprite y rotación
        self.image = pygame.Surface((30, 30))
        self.image.fill((192, 192, 192))  # Gris metálico
        self.rect = self.image.get_rect()
        self.rotacion = 0
        self.velocidad_rotacion = 720  # grados por segundo
        
        # Enemigos ya golpeados (para no golpear múltiples veces)
        self.enemigos_golpeados = []
        
        # Control
        self.debe_eliminarse = False
    
    
    def actualizar(self, dt):
        """
        Mover y rotar el proyectil
        
        PSEUDOCÓDIGO:
        # Mover en dirección
        desplazamiento = self.velocidad * dt
        self.x += self.direccion.x * desplazamiento
        self.y += self.direccion.y * desplazamiento
        self.distancia_recorrida += desplazamiento
        
        # Actualizar rect
        self.rect.center = (int(self.x), int(self.y))
        
        # Rotar
        self.rotacion += self.velocidad_rotacion * dt
        self.rotacion %= 360
        
        # Verificar si debe eliminarse
        SI self.distancia_recorrida >= self.alcance_maximo:
            self.debe_eliminarse = True
        """
        pass
    
    
    def verificar_colision_enemigos(self, enemigos):
        """
        Verificar colisión con enemigos
        
        PSEUDOCÓDIGO:
        PARA CADA enemigo EN enemigos:
            SI enemigo NO está en self.enemigos_golpeados:
                SI self.rect.colliderect(enemigo.rect):
                    # Aplicar daño
                    enemigo.recibir_daño(self.daño)
                    
                    # Knockback
                    enemigo.recibir_knockback(self.direccion, fuerza=50)
                    
                    # Marcar como golpeado
                    self.enemigos_golpeados.append(enemigo)
        """
        pass
    
    
    def dibujar(self, pantalla, camara):
        """
        Dibujar hacha rotada
        
        PSEUDOCÓDIGO:
        pantalla_x = int(self.x - camara.offset_x)
        pantalla_y = int(self.y - camara.offset_y)
        
        # Rotar imagen
        imagen_rotada = pygame.transform.rotate(self.image, self.rotacion)
        rect_rotado = imagen_rotada.get_rect(center=(pantalla_x, pantalla_y))
        
        pantalla.blit(imagen_rotada, rect_rotado)
        """
        pass


class EfectoAzada:
    """
    Efecto visual para ataque de azada
    
    PSEUDOCÓDIGO:
    
    __init__(self, x, y, radio_final):
        self.x = x
        self.y = y
        self.radio_actual = 0
        self.radio_final = radio_final
        self.velocidad_expansion = 500  # píxeles por segundo
        self.completado = False
        self.alpha = 255  # Transparencia
    
    
    def actualizar(self, dt):
        """
        Expandir el círculo
        
        PSEUDOCÓDIGO:
        self.radio_actual += self.velocidad_expansion * dt
        
        # Desvanecer
        self.alpha -= 500 * dt
        
        SI self.radio_actual >= self.radio_final O self.alpha <= 0:
            self.completado = True
        """
        pass
    
    
    def dibujar(self, pantalla, camara):
        """
        Dibujar círculo expandiéndose
        
        PSEUDOCÓDIGO:
        pantalla_x = int(self.x - camara.offset_x)
        pantalla_y = int(self.y - camara.offset_y)
        
        # Dibujar círculo con transparencia
        superficie = pygame.Surface((radio_actual*2, radio_actual*2))
        superficie.set_alpha(self.alpha)
        pygame.draw.circle(superficie, (139, 69, 19), 
                          (radio_actual, radio_actual), 
                          radio_actual, 3)
        
        pantalla.blit(superficie, (pantalla_x, pantalla_y))
        """
        pass
        
        '''