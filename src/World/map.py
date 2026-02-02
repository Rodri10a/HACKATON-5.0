"""
MAP.PY - GENERACIÓN Y RENDERIZADO DEL MAPA
===========================================
Mapa procedural simple con tiles de terreno
"""

import pygame
import random
from settings import *


class Map:
    """Mapa procedural con tiles de pasto"""
    
    def __init__(self):
        """Inicializar mapa"""
        # Dimensiones del mapa en tiles
        self.ancho_tiles = MAPA_ANCHO_TILES
        self.alto_tiles = MAPA_ALTO_TILES
        
        # Generar tiles del mapa
        self.tiles = self.generar_mapa()
        
        # Superficie pre-renderizada del mapa (optimización)
        # Para MVP, renderizar todo el mapa una vez
        self.superficie_mapa = self.pre_renderizar_mapa()
    
    def generar_mapa(self):
        """
        Generar matriz de tiles
        
        Returns:
            list: Matriz 2D de tipos de tiles
        """
        tiles = []
        
        for fila in range(self.alto_tiles):
            fila_tiles = []
            
            for columna in range(self.ancho_tiles):
                # Seleccionar tipo de tile aleatoriamente
                # Para MVP: solo diferentes tonos de verde (pasto)
                tipo = random.choice([
                    "PASTO_OSCURO",
                    "PASTO_CLARO",
                    "PASTO_MEDIO"
                ])
                
                fila_tiles.append(tipo)
            
            tiles.append(fila_tiles)
        
        return tiles
    
    def obtener_color_tile(self, tipo):
        """
        Obtener color según tipo de tile
        
        Args:
            tipo: Tipo de tile (string)
            
        Returns:
            tuple: Color RGB
        """
        return TILE_COLORES.get(tipo, (34, 139, 34))
    
    def pre_renderizar_mapa(self):
        """
        Renderizar todo el mapa en una superficie grande
        (Optimización: se hace una sola vez)
        
        Returns:
            Surface: Superficie con el mapa completo renderizado
        """
        # Crear superficie del tamaño total del mapa
        superficie = pygame.Surface((
            self.ancho_tiles * TILE_SIZE,
            self.alto_tiles * TILE_SIZE
        ))
        
        # Intentar cargar imagen de fondo
        try:
            fondo = pygame.image.load("assets/sprites/mapa.jpeg")
            # Escalar al tamaño del mapa completo
            fondo = pygame.transform.scale(
                fondo, 
                (self.ancho_tiles * TILE_SIZE, self.alto_tiles * TILE_SIZE)
            )
            superficie.blit(fondo, (0, 0))
            print("✓ Fondo del mapa cargado exitosamente")
        except Exception as e:
            print(f"✗ No se pudo cargar pasto_juego.png: {e}")
            print("  Usando tiles de colores por defecto")
            
            # Si no encuentra la imagen, usar tiles como antes
            for fila in range(self.alto_tiles):
                for columna in range(self.ancho_tiles):
                    tipo_tile = self.tiles[fila][columna]
                    color = self.obtener_color_tile(tipo_tile)
                    
                    # Calcular posición del tile
                    x = columna * TILE_SIZE
                    y = fila * TILE_SIZE
                    
                    # Dibujar rectángulo del tile
                    pygame.draw.rect(
                        superficie,
                        color,
                        (x, y, TILE_SIZE, TILE_SIZE)
                    )
                    
                    # Agregar variación visual (líneas de pasto)
                    if tipo_tile == "PASTO_CLARO":
                        for _ in range(3):
                            brizna_x = x + random.randint(5, TILE_SIZE - 5)
                            brizna_y = y + random.randint(5, TILE_SIZE - 5)
                            pygame.draw.line(
                                superficie,
                                (40, 195, 40),
                                (brizna_x, brizna_y),
                                (brizna_x, brizna_y + 3),
                                1
                            )
        
        return superficie
    
    def dibujar(self, pantalla, camara):
        """
        Dibujar porción visible del mapa
        
        Args:
            pantalla: Surface de pygame donde dibujar
            camara: Objeto Camera para calcular qué mostrar
        """
        # Calcular qué porción del mapa es visible
        offset_x = int(camara.offset_x)
        offset_y = int(camara.offset_y)
        
        # Crear rect de la porción visible
        area_visible = pygame.Rect(
            offset_x,
            offset_y,
            camara.ancho,
            camara.alto
        )
        
        # Dibujar solo la porción visible del mapa pre-renderizado
        pantalla.blit(
            self.superficie_mapa,
            (0, 0),  # Posición en pantalla (esquina superior izquierda)
            area_visible  # Área del mapa fuente a copiar
        )
    
    def obtener_tile_en_posicion(self, x, y):
        """
        Obtener tipo de tile en una posición del mundo
        (Útil para colisiones futuras con obstáculos)
        
        Args:
            x: Posición X en el mundo
            y: Posición Y en el mundo
            
        Returns:
            string: Tipo de tile, o None si está fuera del mapa
        """
        tile_x = int(x // TILE_SIZE)
        tile_y = int(y // TILE_SIZE)
        
        # Verificar límites
        if tile_x < 0 or tile_x >= self.ancho_tiles:
            return None
        if tile_y < 0 or tile_y >= self.alto_tiles:
            return None
        
        return self.tiles[tile_y][tile_x]
    
    def posicion_spawn_aleatoria(self):
        """
        Obtener posición aleatoria válida en el mapa
        (Para spawn de enemigos)
        
        Returns:
            tuple: (x, y) posición en el mundo
        """
        x = random.randint(0, MAPA_ANCHO_PIXELES)
        y = random.randint(0, MAPA_ALTO_PIXELES) 
        
        return (x, y)
    
    def posicion_spawn_fuera_pantalla(self, camara, margen=100):
        """
        Obtener posición justo fuera de la pantalla visible
        (Para spawn de enemigos cerca del jugador)
        
        Args:
            camara: Objeto Camera
            margen: Distancia fuera de pantalla en píxeles
            
        Returns:
            tuple: (x, y) posición en el mundo
        """
        # Elegir lado aleatorio (arriba, abajo, izquierda, derecha)
        lado = random.choice(["arriba", "abajo", "izquierda", "derecha"])
        
        if lado == "arriba":
            x = random.randint(int(camara.offset_x), int(camara.offset_x + camara.ancho))
            y = camara.offset_y - margen
        
        elif lado == "abajo":
            x = random.randint(int(camara.offset_x), int(camara.offset_x + camara.ancho))
            y = camara.offset_y + camara.alto + margen
        
        elif lado == "izquierda":
            x = camara.offset_x - margen
            y = random.randint(int(camara.offset_y), int(camara.offset_y + camara.alto))
        
        else:  # derecha
            x = camara.offset_x + camara.ancho + margen
            y = random.randint(int(camara.offset_y), int(camara.offset_y + camara.alto))
        
        # Asegurar que esté dentro del mapa
        x = max(0, min(x, MAPA_ANCHO_PIXELES))
        y = max(0, min(y, MAPA_ALTO_PIXELES))
        
        return (x, y)