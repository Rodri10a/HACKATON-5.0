"""
CAMERA.PY - SISTEMA DE CÁMARA
==============================
Cámara que sigue al jugador suavemente
"""

import pygame
from settings import *


class Camera:
    """Cámara que sigue al jugador con interpolación suave"""
    
    def __init__(self, ancho, alto):
        """
        Inicializar cámara
        
        Args:
            ancho: Ancho de la ventana
            alto: Alto de la ventana
        """
        self.ancho = ancho
        self.alto = alto
        
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
        
        Args:
            entidad: Entidad a seguir (generalmente el jugador)
        """
        self.target = entidad
    
    def actualizar(self, dt):
        """
        Actualizar posición de cámara para seguir al target
        
        Args:
            dt: Delta time en segundos
        """
        if self.target is None:
            return
        
        # Calcular posición deseada (centrar target en pantalla)
        target_offset_x = self.target.x - self.ancho // 2
        target_offset_y = self.target.y - self.alto // 2
        
        # Interpolación suave (lerp)
        # Esto hace que la cámara "alcance" suavemente al jugador
        self.offset_x += (target_offset_x - self.offset_x) * self.velocidad_seguimiento * dt
        self.offset_y += (target_offset_y - self.offset_y) * self.velocidad_seguimiento * dt
        
        # Limitar cámara a los bordes del mapa
        self.limitar_al_mapa()
    
    def limitar_al_mapa(self):
        """No permitir que la cámara muestre fuera del mapa"""
        # Limitar X
        if self.offset_x < 0:
            self.offset_x = 0
        if self.offset_x > MAPA_ANCHO_PIXELES - self.ancho:
            self.offset_x = MAPA_ANCHO_PIXELES - self.ancho
        
        # Limitar Y
        if self.offset_y < 0:
            self.offset_y = 0
        if self.offset_y > MAPA_ALTO_PIXELES - self.alto:
            self.offset_y = MAPA_ALTO_PIXELES - self.alto
    
    def aplicar_a_entidad(self, entidad):
        """
        Convertir posición del mundo a posición en pantalla
        
        Args:
            entidad: Entidad con atributos x, y
            
        Returns:
            tuple: (pantalla_x, pantalla_y)
        """
        pantalla_x = entidad.x - self.offset_x
        pantalla_y = entidad.y - self.offset_y
        return (pantalla_x, pantalla_y)
    
    def mundo_a_pantalla(self, x, y):
        """
        Convertir coordenadas del mundo a pantalla
        
        Args:
            x: Coordenada X en el mundo
            y: Coordenada Y en el mundo
            
        Returns:
            tuple: (pantalla_x, pantalla_y)
        """
        pantalla_x = x - self.offset_x
        pantalla_y = y - self.offset_y
        return (pantalla_x, pantalla_y)
    
    def pantalla_a_mundo(self, x, y):
        """
        Convertir coordenadas de pantalla a mundo
        (Útil para eventos de mouse)
        
        Args:
            x: Coordenada X en pantalla
            y: Coordenada Y en pantalla
            
        Returns:
            tuple: (mundo_x, mundo_y)
        """
        mundo_x = x + self.offset_x
        mundo_y = y + self.offset_y
        return (mundo_x, mundo_y)
    
    def esta_visible(self, entidad, margen=100):
        """
        Verificar si una entidad está visible en pantalla
        (con margen extra para optimización)
        
        Args:
            entidad: Entidad con atributos x, y
            margen: Margen extra en píxeles
            
        Returns:
            bool: True si está visible
        """
        # Calcular posición en pantalla
        pantalla_x = entidad.x - self.offset_x
        pantalla_y = entidad.y - self.offset_y
        
        # Verificar si está dentro de los límites (con margen)
        visible_x = -margen < pantalla_x < self.ancho + margen
        visible_y = -margen < pantalla_y < self.alto + margen
        
        return visible_x and visible_y
    
    def centrar_en(self, x, y):
        """
        Centrar cámara inmediatamente en una posición
        (Sin interpolación, útil al iniciar el juego)
        
        Args:
            x: Coordenada X en el mundo
            y: Coordenada Y en el mundo
        """
        self.offset_x = x - self.ancho // 2
        self.offset_y = y - self.alto // 2
        self.limitar_al_mapa()