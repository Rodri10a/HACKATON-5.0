"""
CAMERA.PY - SISTEMA DE CÁMARA
==============================
Cámara que sigue al jugador suavemente
"""

import pygame
from src.settings import *

class Camera:
    '''
    """
    PSEUDOCÓDIGO:
    
    __init__(self, ancho, alto):
        self.ancho = ancho  # Ancho de la ventana
        self.alto = alto    # Alto de la ventana
        
        # Offset de la cámara (posición en el mundo)
        self.offset_x = 0
        self.offset_y = 0
        
        # Target (objetivo a seguir, generalmente el jugador)
        self.target = None
        
        # Velocidad de seguimiento (interpolación)
        self.velocidad_seguimiento = CAMARA_VELOCIDAD_SEGUIMIENTO
    
    
    def establecer_target(self, entidad):
        """
        Establecer la entidad a seguir
        
        PSEUDOCÓDIGO:
        self.target = entidad
        """
        pass
    
    
    def actualizar(self, dt):
        """
        Actualizar posición de cámara para seguir al target
        
        PSEUDOCÓDIGO:
        SI self.target ES None:
            RETORNAR
        
        # Calcular posición deseada (centrar target en pantalla)
        target_offset_x = self.target.x - self.ancho // 2
        target_offset_y = self.target.y - self.alto // 2
        
        # Interpolación suave (lerp)
        # Esto hace que la cámara "alcance" suavemente al jugador
        self.offset_x += (target_offset_x - self.offset_x) * self.velocidad_seguimiento * dt
        self.offset_y += (target_offset_y - self.offset_y) * self.velocidad_seguimiento * dt
        
        # Limitar cámara a los bordes del mapa
        self.limitar_al_mapa()
        """
        pass
    
    
    def limitar_al_mapa(self):
        """
        No permitir que la cámara muestre fuera del mapa
        
        PSEUDOCÓDIGO:
        # Limitar X
        SI self.offset_x < 0:
            self.offset_x = 0
        SI self.offset_x > MAPA_ANCHO_PIXELES - self.ancho:
            self.offset_x = MAPA_ANCHO_PIXELES - self.ancho
        
        # Limitar Y
        SI self.offset_y < 0:
            self.offset_y = 0
        SI self.offset_y > MAPA_ALTO_PIXELES - self.alto:
            self.offset_y = MAPA_ALTO_PIXELES - self.alto
        """
        pass
    
    
    def aplicar_a_entidad(self, entidad):
        """
        Convertir posición del mundo a posición en pantalla
        
        PSEUDOCÓDIGO:
        pantalla_x = entidad.x - self.offset_x
        pantalla_y = entidad.y - self.offset_y
        RETORNAR (pantalla_x, pantalla_y)
        """
        pass
    
    
    def mundo_a_pantalla(self, x, y):
        """
        Convertir coordenadas del mundo a pantalla
        
        PSEUDOCÓDIGO:
        pantalla_x = x - self.offset_x
        pantalla_y = y - self.offset_y
        RETORNAR (pantalla_x, pantalla_y)
        """
        pass
    
    
    def pantalla_a_mundo(self, x, y):
        """
        Convertir coordenadas de pantalla a mundo
        (Útil para eventos de mouse)
        
        PSEUDOCÓDIGO:
        mundo_x = x + self.offset_x
        mundo_y = y + self.offset_y
        RETORNAR (mundo_x, mundo_y)
        """
        pass
    
    
    def esta_visible(self, entidad, margen=100):
        """
        Verificar si una entidad está visible en pantalla
        (con margen extra para optimización)
        
        PSEUDOCÓDIGO:
        # Calcular posición en pantalla
        pantalla_x = entidad.x - self.offset_x
        pantalla_y = entidad.y - self.offset_y
        
        # Verificar si está dentro de los límites (con margen)
        visible_x = -margen < pantalla_x < self.ancho + margen
        visible_y = -margen < pantalla_y < self.alto + margen
        
        RETORNAR visible_x Y visible_y
        """
        pass
    
    
    def centrar_en(self, x, y):
        """
        Centrar cámara inmediatamente en una posición
        (Sin interpolación, útil al iniciar el juego)
        
        PSEUDOCÓDIGO:
        self.offset_x = x - self.ancho // 2
        self.offset_y = y - self.alto // 2
        self.limitar_al_mapa()
        """
        pass
    
    
    def shake(self, intensidad, duracion):
        """
        Efecto de temblor de cámara (para impactos)
        (OPCIONAL para MVP, pero agrega mucho juice)
        
        PSEUDOCÓDIGO:
        self.shake_intensidad = intensidad
        self.shake_duracion = duracion
        self.shake_timer = 0
        """
        pass
    
    
    def actualizar_shake(self, dt):
        """
        Actualizar efecto de shake
        
        PSEUDOCÓDIGO:
        SI self.shake_timer < self.shake_duracion:
            self.shake_timer += dt
            
            # Aplicar offset aleatorio
            shake_x = random.randint(-intensidad, intensidad)
            shake_y = random.randint(-intensidad, intensidad)
            
            self.offset_x += shake_x
            self.offset_y += shake_y
        """
        pass
        '''