"""
BASE_ENTITY.PY - CLASE PADRE PARA TODAS LAS ENTIDADES
====================================================
Clase base que heredarán jugador, enemigos y proyectiles
"""

import pygame
import math

class BaseEntity:
    """Clase base para todas las entidades del juego"""
    
    def __init__(self, x, y, ancho, alto, color, sprite_path=None):
        """
        Inicializar entidad base
        
        Args:
            x: Posición X inicial
            y: Posición Y inicial
            ancho: Ancho de la entidad
            alto: Alto de la entidad
            color: Color RGB de la entidad
            sprite_path: Ruta opcional del sprite
        """
        # Posición
        self.x = float(x)
        self.y = float(y)
        
        # Crear superficie y rect para colisiones
        if sprite_path:
            try:
                self.image = pygame.image.load(sprite_path).convert_alpha()
                self.image = pygame.transform.scale(self.image, (ancho, alto))
            except:
                # Si falla, usar color sólido
                self.image = pygame.Surface((ancho, alto))
                self.image.fill(color)
        else:
            self.image = pygame.Surface((ancho, alto))
            self.image.fill(color)
        
        self.rect = self.image.get_rect()
        self.rect.center = (int(self.x), int(self.y))
        
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
        
        Args:
            dt: Delta time en segundos
        """
        if self.direccion.length() > 0:
            # Normalizar para movimiento diagonal consistente
            self.direccion = self.direccion.normalize()
            
            # Calcular desplazamiento
            desplazamiento_x = self.direccion.x * self.velocidad * dt
            desplazamiento_y = self.direccion.y * self.velocidad * dt
            
            # Actualizar posición
            self.x += desplazamiento_x
            self.y += desplazamiento_y
            
            # Actualizar rect
            self.rect.center = (int(self.x), int(self.y))
    
    def recibir_daño(self, cantidad):
        """
        Reducir vida y verificar muerte
        
        Args:
            cantidad: Cantidad de daño a recibir
        """
        self.vida_actual -= cantidad
        
        if self.vida_actual <= 0:
            self.vida_actual = 0
            self.esta_vivo = False
            self.al_morir()
    
    def curar(self, cantidad):
        """
        Recuperar vida sin exceder máximo
        
        Args:
            cantidad: Cantidad de vida a recuperar
        """
        self.vida_actual += cantidad
        
        if self.vida_actual > self.vida_maxima:
            self.vida_actual = self.vida_maxima
    
    def al_morir(self):
        """
        Callback cuando la entidad muere
        Las subclases pueden sobreescribir esto
        """
        pass
    
    def dibujar(self, pantalla, camara):
        """
        Dibujar en pantalla con offset de cámara
        
        Args:
            pantalla: Surface de pygame donde dibujar
            camara: Objeto Camera para calcular offset
        """
        # Calcular posición en pantalla
        pantalla_x = self.rect.x - camara.offset_x
        pantalla_y = self.rect.y - camara.offset_y
        
        # Dibujar solo si está visible en pantalla
        if -100 < pantalla_x < pantalla.get_width() + 100 and -100 < pantalla_y < pantalla.get_height() + 100:
            pantalla.blit(self.image, (pantalla_x, pantalla_y))
    
    def distancia_a(self, otra_entidad):
        """
        Calcular distancia a otra entidad
        
        Args:
            otra_entidad: Otra instancia de BaseEntity
            
        Returns:
            float: Distancia en píxeles
        """
        dx = self.x - otra_entidad.x
        dy = self.y - otra_entidad.y
        return math.sqrt(dx * dx + dy * dy)
    
    def direccion_hacia(self, otra_entidad):
        """
        Obtener vector de dirección hacia otra entidad
        
        Args:
            otra_entidad: Otra instancia de BaseEntity
            
        Returns:
            Vector2: Vector normalizado hacia la entidad
        """
        vector = pygame.math.Vector2(
            otra_entidad.x - self.x,
            otra_entidad.y - self.y
        )
        
        if vector.length() > 0:
            return vector.normalize()
        
        return vector
    
    def colisiona_con(self, otra_entidad):
        """
        Verificar colisión con otra entidad
        
        Args:
            otra_entidad: Otra instancia de BaseEntity
            
        Returns:
            bool: True si hay colisión
        """
        return self.rect.colliderect(otra_entidad.rect)
    
    def actualizar(self, dt):
        """
        Actualización general (a sobreescribir en subclases)
        
        Args:
            dt: Delta time en segundos
        """
        pass