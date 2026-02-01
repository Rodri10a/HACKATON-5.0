"""
MAP.PY - GENERACIÓN Y RENDERIZADO DEL MAPA
===========================================
Mapa procedural simple con tiles de terreno
"""

import pygame
import random
from src.settings import *

class Map:
    '''
    """
    PSEUDOCÓDIGO:
    
    __init__(self):
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
        
        PSEUDOCÓDIGO:
        tiles = []
        
        PARA fila EN range(self.alto_tiles):
            fila_tiles = []
            
            PARA columna EN range(self.ancho_tiles):
                # Seleccionar tipo de tile aleatoriamente
                # Para MVP: solo diferentes tonos de verde (pasto)
                tipo = random.choice([
                    "PASTO_OSCURO",
                    "PASTO_CLARO",
                    "PASTO_MEDIO"
                ])
                
                fila_tiles.append(tipo)
            
            tiles.append(fila_tiles)
        
        RETORNAR tiles
        """
        pass
    
    
    def obtener_color_tile(self, tipo):
        """
        Obtener color según tipo de tile
        
        PSEUDOCÓDIGO:
        colores = {
            "PASTO_OSCURO": (34, 139, 34),   # Verde oscuro
            "PASTO_CLARO": (50, 205, 50),    # Verde claro
            "PASTO_MEDIO": (60, 179, 113),   # Verde medio
            "TIERRA": (139, 90, 43),         # Marrón (para expansión)
            "AGUA": (65, 105, 225)           # Azul (para expansión)
        }
        
        RETORNAR colores.get(tipo, (34, 139, 34))
        """
        pass
    
    
    def pre_renderizar_mapa(self):
        """
        Renderizar todo el mapa en una superficie grande
        (Optimización: se hace una sola vez)
        
        PSEUDOCÓDIGO:
        # Crear superficie del tamaño total del mapa
        superficie = pygame.Surface((
            self.ancho_tiles * TILE_SIZE,
            self.alto_tiles * TILE_SIZE
        ))
        
        # Dibujar cada tile
        PARA fila EN range(self.alto_tiles):
            PARA columna EN range(self.ancho_tiles):
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
                
                # Agregar variación visual (líneas, puntos)
                SI tipo_tile == "PASTO_CLARO":
                    # Dibujar algunas "briznas" de pasto
                    PARA _ EN range(3):
                        brizna_x = x + random.randint(5, TILE_SIZE-5)
                        brizna_y = y + random.randint(5, TILE_SIZE-5)
                        pygame.draw.line(
                            superficie,
                            (40, 195, 40),
                            (brizna_x, brizna_y),
                            (brizna_x, brizna_y + 3),
                            1
                        )
        
        RETORNAR superficie
        """
        pass
    
    
    def dibujar(self, pantalla, camara):
        """
        Dibujar porción visible del mapa
        
        PSEUDOCÓDIGO:
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
        
        # SI DEBUG_MODE:
        #     self.dibujar_grid(pantalla, camara)
        """
        pass
    
    
    def dibujar_grid(self, pantalla, camara):
        """
        Dibujar grid de tiles (para debug)
        
        PSEUDOCÓDIGO:
        # Calcular tiles visibles
        inicio_tile_x = int(camara.offset_x // TILE_SIZE)
        inicio_tile_y = int(camara.offset_y // TILE_SIZE)
        fin_tile_x = inicio_tile_x + (camara.ancho // TILE_SIZE) + 2
        fin_tile_y = inicio_tile_y + (camara.alto // TILE_SIZE) + 2
        
        # Dibujar líneas del grid
        PARA x EN range(inicio_tile_x, fin_tile_x):
            pantalla_x = (x * TILE_SIZE) - camara.offset_x
            pygame.draw.line(
                pantalla,
                (100, 100, 100),
                (pantalla_x, 0),
                (pantalla_x, camara.alto)
            )
        
        PARA y EN range(inicio_tile_y, fin_tile_y):
            pantalla_y = (y * TILE_SIZE) - camara.offset_y
            pygame.draw.line(
                pantalla,
                (100, 100, 100),
                (0, pantalla_y),
                (camara.ancho, pantalla_y)
            )
        """
        pass
    
    
    def obtener_tile_en_posicion(self, x, y):
        """
        Obtener tipo de tile en una posición del mundo
        (Útil para colisiones futuras con obstáculos)
        
        PSEUDOCÓDIGO:
        tile_x = int(x // TILE_SIZE)
        tile_y = int(y // TILE_SIZE)
        
        # Verificar límites
        SI tile_x < 0 O tile_x >= self.ancho_tiles:
            RETORNAR None
        SI tile_y < 0 O tile_y >= self.alto_tiles:
            RETORNAR None
        
        RETORNAR self.tiles[tile_y][tile_x]
        """
        pass
    
    
    def posicion_spawn_aleatoria(self):
        """
        Obtener posición aleatoria válida en el mapa
        (Para spawn de enemigos)
        
        PSEUDOCÓDIGO:
        x = random.randint(0, MAPA_ANCHO_PIXELES)
        y = random.randint(0, MAPA_ALTO_PIXELES)
        
        RETORNAR (x, y)
        """
        pass
    
    
    def posicion_spawn_fuera_pantalla(self, camara, margen=100):
        """
        Obtener posición justo fuera de la pantalla visible
        (Para spawn de enemigos cerca del jugador)
        
        PSEUDOCÓDIGO:
        # Elegir lado aleatorio (arriba, abajo, izquierda, derecha)
        lado = random.choice(["arriba", "abajo", "izquierda", "derecha"])
        
        SI lado == "arriba":
            x = random.randint(camara.offset_x, camara.offset_x + camara.ancho)
            y = camara.offset_y - margen
        
        SI lado == "abajo":
            x = random.randint(camara.offset_x, camara.offset_x + camara.ancho)
            y = camara.offset_y + camara.alto + margen
        
        SI lado == "izquierda":
            x = camara.offset_x - margen
            y = random.randint(camara.offset_y, camara.offset_y + camara.alto)
        
        SI lado == "derecha":
            x = camara.offset_x + camara.ancho + margen
            y = random.randint(camara.offset_y, camara.offset_y + camara.alto)
        
        # Asegurar que esté dentro del mapa
        x = max(0, min(x, MAPA_ANCHO_PIXELES))
        y = max(0, min(y, MAPA_ALTO_PIXELES))
        
        RETORNAR (x, y)
        """
        pass
        '''