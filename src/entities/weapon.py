"""
ARMA.PY - SISTEMA DE ARMAS
===========================
Diferentes tipos de armas con sus mecánicas únicas
"""

import pygame
import math
import random
from settings import *


class Weapon:
    """Clase base de armas"""
    
    def __init__(self, tipo, dueño):
        """
        Inicializar arma
        
        Args:
            tipo: Tipo de arma (string)
            dueño: Referencia al jugador
        """
        self.tipo = tipo
        self.dueño = dueño
        self.nivel = 1
        
        # Obtener configuración del arma
        self.config = ARMAS_CONFIG[tipo]
        self.cooldown = self.config["cooldown"]
        self.tipo_ataque = self.config["tipo"]
        
        # Timer de cooldown
        self.timer_cooldown = 0
        self.puede_usar = True
        
        # Lista de proyectiles (para armas tipo proyectil)
        self.proyectiles = []
        
        # Lista de efectos visuales (para armas tipo AoE)
        self.efectos = []
        
        # Buff activo (para armas tipo buff)
        self.buff_activo = False
        self.timer_buff = 0
        self.duracion_buff = 0
    
    def actualizar(self, dt, enemigos):
        """
        Actualizar arma y sus proyectiles/efectos
        
        Args:
            dt: Delta time en segundos
            enemigos: Lista de enemigos
        """
        # Actualizar cooldown
        if not self.puede_usar:
            self.timer_cooldown += dt
            if self.timer_cooldown >= self.cooldown:
                self.puede_usar = True
                self.timer_cooldown = 0
        
        # Si puede usar, atacar
        if self.puede_usar and len(enemigos) > 0:
            self.usar(enemigos)
        
        # Actualizar proyectiles
        proyectiles_activos = []
        for proyectil in self.proyectiles:
            proyectil.actualizar(dt)
            if not proyectil.debe_eliminarse:
                proyectiles_activos.append(proyectil)
        self.proyectiles = proyectiles_activos
        
        # Actualizar efectos
        efectos_activos = []
        for efecto in self.efectos:
            efecto.actualizar(dt)
            if not efecto.completado:
                efectos_activos.append(efecto)
        self.efectos = efectos_activos
        
        # Actualizar buff
        if self.buff_activo:
            self.timer_buff += dt
            if self.timer_buff >= self.duracion_buff:
                self.buff_activo = False
                self.timer_buff = 0
    
    def usar(self, enemigos):
        """
        Usar el arma según su tipo
        
        Args:
            enemigos: Lista de enemigos
        """
        if self.tipo_ataque == "melee":
            self.ataque_machete(enemigos)
        elif self.tipo_ataque == "proyectil":
            self.ataque_hacha(enemigos)
        elif self.tipo_ataque == "aoe":
            self.ataque_azada(enemigos)
        elif self.tipo_ataque == "buff":
            self.buff_terere()
        
        # Activar cooldown
        self.puede_usar = False
        self.timer_cooldown = 0
    
    def ataque_machete(self, enemigos):
        """
        Ataque melee circular alrededor del jugador
        
        Args:
            enemigos: Lista de enemigos
        """
        config_nivel = self.config["niveles"][self.nivel - 1]
        daño = config_nivel["daño"]
        alcance = config_nivel["alcance"]
        
        for enemigo in enemigos:
            if not enemigo.esta_vivo:
                continue
            
            # Calcular distancia
            dx = enemigo.x - self.dueño.x
            dy = enemigo.y - self.dueño.y
            distancia = math.sqrt(dx * dx + dy * dy)
            
            if distancia <= alcance:
                # Aplicar daño
                enemigo.recibir_daño(daño)
                
                # Aplicar knockback
                if distancia > 0:
                    direccion = pygame.math.Vector2(dx / distancia, dy / distancia)
                    enemigo.recibir_knockback(direccion, KNOCKBACK_FUERZA_MACHETE)
    
    def ataque_hacha(self, enemigos):
        """
        Lanzar proyectiles de hacha hacia enemigos cercanos
        
        Args:
            enemigos: Lista de enemigos
        """
        config_nivel = self.config["niveles"][self.nivel - 1]
        daño = config_nivel["daño"]
        cantidad = config_nivel["cantidad"]
        velocidad = config_nivel["velocidad"]
        
        # Encontrar enemigos más cercanos
        enemigos_vivos = [e for e in enemigos if e.esta_vivo]
        if not enemigos_vivos:
            return
        
        # Ordenar por distancia
        enemigos_ordenados = sorted(
            enemigos_vivos,
            key=lambda e: math.sqrt((e.x - self.dueño.x)**2 + (e.y - self.dueño.y)**2)
        )
        
        # Lanzar hachas hacia los más cercanos
        for i in range(min(cantidad, len(enemigos_ordenados))):
            enemigo_objetivo = enemigos_ordenados[i]
            
            # Calcular dirección
            dx = enemigo_objetivo.x - self.dueño.x
            dy = enemigo_objetivo.y - self.dueño.y
            distancia = math.sqrt(dx * dx + dy * dy)
            
            if distancia > 0:
                direccion = pygame.math.Vector2(dx / distancia, dy / distancia)
                
                # Crear proyectil
                proyectil = ProyectilHacha(
                    self.dueño.x,
                    self.dueño.y,
                    direccion,
                    velocidad,
                    daño
                )
                self.proyectiles.append(proyectil)
    
    def ataque_azada(self, enemigos):
        """
        Ataque AoE que daña a todos los enemigos en un radio
        
        Args:
            enemigos: Lista de enemigos
        """
        config_nivel = self.config["niveles"][self.nivel - 1]
        daño = config_nivel["daño"]
        radio = config_nivel["radio"]
        
        for enemigo in enemigos:
            if not enemigo.esta_vivo:
                continue
            
            # Calcular distancia
            dx = enemigo.x - self.dueño.x
            dy = enemigo.y - self.dueño.y
            distancia = math.sqrt(dx * dx + dy * dy)
            
            if distancia <= radio:
                # Aplicar daño
                enemigo.recibir_daño(daño)
                
                # Aplicar knockback fuerte
                if distancia > 0:
                    direccion = pygame.math.Vector2(dx / distancia, dy / distancia)
                    enemigo.recibir_knockback(direccion, KNOCKBACK_FUERZA_AZADA)
        
        # Crear efecto visual
        efecto = EfectoAzada(self.dueño.x, self.dueño.y, radio)
        self.efectos.append(efecto)
    
    def buff_terere(self):
        """Aplicar buff de regeneración al jugador"""
        config_nivel = self.config["niveles"][self.nivel - 1]
        self.vida_por_seg = config_nivel["vida_por_seg"]
        self.duracion_buff = config_nivel["duracion"]
        
        self.buff_activo = True
        self.timer_buff = 0
    
    def aplicar_buff(self, dt):
        """
        Aplicar efectos del buff si está activo
        
        Args:
            dt: Delta time en segundos
        """
        if self.buff_activo and self.tipo == "TERERE":
            self.dueño.curar(self.vida_por_seg * dt)
    
    def subir_nivel(self):
        """Subir nivel del arma"""
        if self.nivel < len(self.config["niveles"]):
            self.nivel += 1
    
    def dibujar(self, pantalla, camara):
        """
        Dibujar proyectiles y efectos del arma
        
        Args:
            pantalla: Surface de pygame
            camara: Objeto Camera
        """
        # Dibujar proyectiles
        for proyectil in self.proyectiles:
            proyectil.dibujar(pantalla, camara)
        
        # Dibujar efectos
        for efecto in self.efectos:
            efecto.dibujar(pantalla, camara)


class ProyectilHacha:
    """Proyectil de hacha que rota"""
    
    def __init__(self, x, y, direccion, velocidad, daño):
        """
        Inicializar proyectil
        
        Args:
            x: Posición X inicial
            y: Posición Y inicial
            direccion: Vector2 de dirección
            velocidad: Velocidad en píxeles/segundo
            daño: Daño que inflige
        """
        self.x = float(x)
        self.y = float(y)
        self.direccion = direccion
        self.velocidad = velocidad
        self.daño = daño
        
        # Crear sprite
        self.image = pygame.Surface((20, 20))
        self.image.fill((192, 192, 192))  # Gris plateado
        self.rect = self.image.get_rect()
        self.rect.center = (int(self.x), int(self.y))
        
        # Distancia recorrida
        self.distancia_recorrida = 0
        self.alcance_maximo = PROYECTIL_HACHA_ALCANCE
        
        # Rotación
        self.angulo = 0
        
        # Enemigos ya golpeados
        self.enemigos_golpeados = []
        
        # Flag de eliminación
        self.debe_eliminarse = False
    
    def actualizar(self, dt):
        """
        Actualizar posición y rotación
        
        Args:
            dt: Delta time en segundos
        """
        # Mover
        desplazamiento = self.velocidad * dt
        self.x += self.direccion.x * desplazamiento
        self.y += self.direccion.y * desplazamiento
        self.rect.center = (int(self.x), int(self.y))
        
        # Actualizar distancia
        self.distancia_recorrida += desplazamiento
        
        # Rotar
        self.angulo += PROYECTIL_HACHA_ROTACION * dt
        
        # Verificar si debe eliminarse
        if self.distancia_recorrida >= self.alcance_maximo:
            self.debe_eliminarse = True
    
    def verificar_colision_enemigos(self, enemigos):
        """
        Verificar colisión con enemigos
        
        Args:
            enemigos: Lista de enemigos
        """
        for enemigo in enemigos:
            if not enemigo.esta_vivo:
                continue
            
            if enemigo in self.enemigos_golpeados:
                continue
            
            # Verificar colisión
            if self.rect.colliderect(enemigo.rect):
                enemigo.recibir_daño(self.daño)
                self.enemigos_golpeados.append(enemigo)
                
                # Aplicar knockback
                dx = enemigo.x - self.x
                dy = enemigo.y - self.y
                distancia = math.sqrt(dx * dx + dy * dy)
                if distancia > 0:
                    direccion = pygame.math.Vector2(dx / distancia, dy / distancia)
                    enemigo.recibir_knockback(direccion, KNOCKBACK_FUERZA_HACHA)
    
    def dibujar(self, pantalla, camara):
        """
        Dibujar proyectil
        
        Args:
            pantalla: Surface de pygame
            camara: Objeto Camera
        """
        pantalla_x = self.rect.x - camara.offset_x
        pantalla_y = self.rect.y - camara.offset_y
        
        # Solo dibujar si está en pantalla
        if -50 < pantalla_x < pantalla.get_width() + 50 and -50 < pantalla_y < pantalla.get_height() + 50:
            # Rotar imagen
            imagen_rotada = pygame.transform.rotate(self.image, self.angulo)
            rect_rotado = imagen_rotada.get_rect(center=(pantalla_x + 10, pantalla_y + 10))
            pantalla.blit(imagen_rotada, rect_rotado)


class EfectoAzada:
    """Efecto visual del ataque de azada (círculo expandiéndose)"""
    
    def __init__(self, x, y, radio_final):
        """
        Inicializar efecto
        
        Args:
            x: Posición X del centro
            y: Posición Y del centro
            radio_final: Radio final del círculo
        """
        self.x = x
        self.y = y
        self.radio_actual = 0
        self.radio_final = radio_final
        self.velocidad_expansion = 500  # píxeles por segundo
        
        self.alpha = 255
        self.completado = False
    
    def actualizar(self, dt):
        """
        Actualizar expansión y fade
        
        Args:
            dt: Delta time en segundos
        """
        # Expandir
        self.radio_actual += self.velocidad_expansion * dt
        
        # Fade out
        self.alpha -= 850 * dt
        
        # Marcar como completado
        if self.radio_actual >= self.radio_final or self.alpha <= 0:
            self.completado = True
    
    def dibujar(self, pantalla, camara):
        """
        Dibujar círculo expandiéndose
        
        Args:
            pantalla: Surface de pygame
            camara: Objeto Camera
        """
        if self.completado:
            return
        
        pantalla_x = int(self.x - camara.offset_x)
        pantalla_y = int(self.y - camara.offset_y)
        
        # Crear superficie con transparencia
        radio_int = int(self.radio_actual)
        if radio_int > 0:
            superficie = pygame.Surface((radio_int * 2, radio_int * 2), pygame.SRCALPHA)
            color = (255, 200, 100, max(0, int(self.alpha)))
            pygame.draw.circle(superficie, color, (radio_int, radio_int), radio_int, 3)
            pantalla.blit(superficie, (pantalla_x - radio_int, pantalla_y - radio_int))