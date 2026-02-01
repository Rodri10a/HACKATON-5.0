"""
BASE_ENTITY.PY - CLASE PADRE PARA TODAS LAS ENTIDADES
====================================================
Clase base que heredarán jugador, enemigos y proyectiles
"""

import pygame
from settings import *

class BaseEntity:
    '''
    """
    PSEUDOCÓDIGO:
    
    __init__(self, x, y, ancho, alto, color):
        # Inicializar posición
        self.x = x
        self.y = y
        
        # Crear superficie y rect para colisiones
        self.image = pygame.Surface((ancho, alto))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Stats básicos
        self.velocidad = 0
        self.vida_actual = 0
        self.vida_maxima = 0
        self.esta_vivo = True
        
        # Vector de dirección
        self.direccion = pygame.math.Vector2(0, 0)
    
    
    def mover(self, dt):
        """
        Mover la entidad según su dirección y velocidad
        
        PSEUDOCÓDIGO:
        SI direccion.length() > 0:
            # Normalizar para movimiento diagonal consistente
            direccion.normalize_ip()
            
            # Calcular desplazamiento
            desplazamiento_x = direccion.x * velocidad * dt
            desplazamiento_y = direccion.y * velocidad * dt
            
            # Actualizar posición
            self.x += desplazamiento_x
            self.y += desplazamiento_y
            
            # Actualizar rect
            self.rect.center = (int(self.x), int(self.y))
        """
        pass
    
    
    def recibir_daño(self, cantidad):
        """
        Reducir vida y verificar muerte
        
        PSEUDOCÓDIGO:
        self.vida_actual -= cantidad
        
        SI self.vida_actual <= 0:
            self.vida_actual = 0
            self.esta_vivo = False
            self.al_morir()  # Callback
        """
        pass
    
    
    def curar(self, cantidad):
        """
        Recuperar vida sin exceder máximo
        
        PSEUDOCÓDIGO:
        self.vida_actual += cantidad
        
        SI self.vida_actual > self.vida_maxima:
            self.vida_actual = self.vida_maxima
        """
        pass
    
    
    def al_morir(self):
        """
        Callback cuando la entidad muere
        Las subclases pueden sobreescribir esto
        
        PSEUDOCÓDIGO:
        # Para enemigos: dropear XP
        # Para jugador: game over
        # Por defecto: solo marcar como muerto
        """
        pass
    
    
    def dibujar(self, pantalla, camara):
        """
        Dibujar en pantalla con offset de cámara
        
        PSEUDOCÓDIGO:
        # Calcular posición en pantalla
        pantalla_x = self.rect.x - camara.offset_x
        pantalla_y = self.rect.y - camara.offset_y
        
        # Dibujar solo si está visible en pantalla
        SI esta_en_pantalla(pantalla_x, pantalla_y):
            pantalla.blit(self.image, (pantalla_x, pantalla_y))
            
            SI DEBUG_MODE:
                # Dibujar hitbox
                pygame.draw.rect(pantalla, (255, 0, 0), 
                               (pantalla_x, pantalla_y, rect.width, rect.height), 2)
        """
        pass
    
    
    def distancia_a(self, otra_entidad):
        """
        Calcular distancia a otra entidad
        
        PSEUDOCÓDIGO:
        dx = self.x - otra_entidad.x
        dy = self.y - otra_entidad.y
        distancia = sqrt(dx*dx + dy*dy)
        RETORNAR distancia
        """
        pass
    
    
    def direccion_hacia(self, otra_entidad):
        """
        Obtener vector de dirección hacia otra entidad
        
        PSEUDOCÓDIGO:
        vector = pygame.math.Vector2(
            otra_entidad.x - self.x,
            otra_entidad.y - self.y
        )
        
        SI vector.length() > 0:
            vector.normalize_ip()
        
        RETORNAR vector
        """
        pass
    
    
    def colisiona_con(self, otra_entidad):
        """
        Verificar colisión con otra entidad
        
        PSEUDOCÓDIGO:
        RETORNAR self.rect.colliderect(otra_entidad.rect)
        """
        pass
    
    
    def actualizar(self, dt):
        """
        Actualización general (a sobreescribir en subclases)
        
        PSEUDOCÓDIGO:
        # Las subclases implementarán su lógica específica
        pass
        """
        pass
        ''' 