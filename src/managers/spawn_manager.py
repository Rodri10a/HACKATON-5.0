"""
SPAWN_MANAGER.PY - GESTIÓN DE APARICIÓN DE ENEMIGOS
====================================================
Controla cuándo y dónde aparecen enemigos, escalando dificultad
"""

import pygame
import random
from entities.enemy import Enemy
from src.settings import *

class SpawnManager:
    '''
    """
    PSEUDOCÓDIGO:
    
    __init__(self, mapa, camara, jugador):
        self.mapa = mapa
        self.camara = camara
        self.jugador = jugador
        
        # Lista de enemigos activos
        self.enemigos = []
        
        # Control de spawn
        self.tiempo_entre_spawns = TIEMPO_ENTRE_SPAWNS
        self.timer_spawn = 0
        self.enemigos_por_spawn = ENEMIGOS_POR_SPAWN
        
        # Tiempo de juego (para escalar dificultad)
        self.tiempo_juego = 0
        
        # Límite de enemigos en pantalla
        self.max_enemigos = 300  # Para evitar lag
    
    
    def actualizar(self, dt):
        """
        Actualizar spawns y enemigos
        
        PSEUDOCÓDIGO:
        # Actualizar tiempo de juego
        self.tiempo_juego += dt
        
        # Actualizar timers de spawn
        self.timer_spawn += dt
        
        # Escalar dificultad cada minuto
        SI int(self.tiempo_juego) % 60 == 0 Y int(self.tiempo_juego) > 0:
            self.escalar_dificultad()
        
        # Verificar si es momento de spawnear
        SI self.timer_spawn >= self.tiempo_entre_spawns:
            SI len(self.enemigos) < self.max_enemigos:
                self.spawnear_enemigos()
            self.timer_spawn = 0
        
        # Actualizar todos los enemigos
        self.actualizar_enemigos(dt)
        
        # Eliminar enemigos muertos
        self.limpiar_enemigos_muertos()
        """
        pass
    
    
    def spawnear_enemigos(self):
        """
        Crear nuevos enemigos
        
        PSEUDOCÓDIGO:
        PARA i EN range(self.enemigos_por_spawn):
            # Elegir tipo de enemigo según probabilidades
            tipo_enemigo = self.elegir_tipo_enemigo()
            
            # Obtener posición de spawn (fuera de pantalla)
            x, y = self.mapa.posicion_spawn_fuera_pantalla(
                self.camara, 
                margen=100
            )
            
            # Crear enemigo
            enemigo = Enemy(x, y, tipo_enemigo)
            enemigo.jugador = self.jugador  # Asignar referencia al jugador
            
            self.enemigos.append(enemigo)
        """
        pass
    
    
    def elegir_tipo_enemigo(self):
        """
        Elegir tipo de enemigo según pesos de spawn
        
        PSEUDOCÓDIGO:
        # Crear lista ponderada de tipos
        opciones = []
        
        PARA tipo, config EN ENEMIGO_CONFIGS.items():
            peso = config["spawn_peso"]
            
            # Ajustar peso según tiempo de juego
            # Enemigos más fuertes aparecen más seguido con el tiempo
            SI tipo == "AGUARA_GUAZU":  # Boss
                # Solo aparece después de 5 minutos
                SI self.tiempo_juego < 300:
                    peso = 0
                SINO:
                    peso = peso * (self.tiempo_juego / 300)
            
            # Agregar tipo 'peso' veces a la lista
            PARA _ EN range(int(peso)):
                opciones.append(tipo)
        
        # Elegir aleatoriamente
        RETORNAR random.choice(opciones)
        """
        pass
    
    
    def escalar_dificultad(self):
        """
        Aumentar dificultad progresivamente
        
        PSEUDOCÓDIGO:
        # Reducir tiempo entre spawns (hasta un mínimo)
        SI self.tiempo_entre_spawns > SPAWN_MINIMO:
            self.tiempo_entre_spawns -= SPAWN_REDUCCION_POR_MINUTO
            self.tiempo_entre_spawns = max(SPAWN_MINIMO, self.tiempo_entre_spawns)
        
        # Aumentar cantidad de enemigos por spawn cada 2 minutos
        SI int(self.tiempo_juego) % 120 == 0:
            self.enemigos_por_spawn += 1
        """
        pass
    
    
    def actualizar_enemigos(self, dt):
        """
        Actualizar todos los enemigos vivos
        
        PSEUDOCÓDIGO:
        PARA enemigo EN self.enemigos:
            SI enemigo.esta_vivo:
                enemigo.actualizar(dt)
        """
        pass
    
    
    def limpiar_enemigos_muertos(self):
        """
        Eliminar enemigos muertos de la lista
        
        PSEUDOCÓDIGO:
        # Filtrar solo enemigos vivos
        self.enemigos = [e for e in self.enemigos if e.esta_vivo]
        """
        pass
    
    
    def obtener_enemigos_en_rango(self, x, y, rango):
        """
        Obtener enemigos dentro de un rango
        (Útil para detectar objetivos de armas)
        
        PSEUDOCÓDIGO:
        enemigos_cercanos = []
        
        PARA enemigo EN self.enemigos:
            SI NO enemigo.esta_vivo:
                CONTINUAR
            
            # Calcular distancia
            dx = enemigo.x - x
            dy = enemigo.y - y
            distancia = sqrt(dx*dx + dy*dy)
            
            SI distancia <= rango:
                enemigos_cercanos.append(enemigo)
        
        RETORNAR enemigos_cercanos
        """
        pass
    
    
    def obtener_enemigo_mas_cercano(self, x, y):
        """
        Obtener el enemigo más cercano a una posición
        
        PSEUDOCÓDIGO:
        SI len(self.enemigos) == 0:
            RETORNAR None
        
        enemigo_cercano = None
        distancia_minima = float('inf')
        
        PARA enemigo EN self.enemigos:
            SI NO enemigo.esta_vivo:
                CONTINUAR
            
            dx = enemigo.x - x
            dy = enemigo.y - y
            distancia = sqrt(dx*dx + dy*dy)
            
            SI distancia < distancia_minima:
                distancia_minima = distancia
                enemigo_cercano = enemigo
        
        RETORNAR enemigo_cercano
        """
        pass
    
    
    def dibujar(self, pantalla, camara):
        """
        Dibujar todos los enemigos visibles
        
        PSEUDOCÓDIGO:
        PARA enemigo EN self.enemigos:
            SI enemigo.esta_vivo:
                # Solo dibujar si está visible
                SI camara.esta_visible(enemigo):
                    enemigo.dibujar(pantalla, camara)
        """
        pass
    
    
    def spawnear_oleada_boss(self):
        """
        Spawnear oleada especial de boss
        (Llamar cada X minutos)
        
        PSEUDOCÓDIGO:
        # Spawnear boss en posición aleatoria
        x, y = self.mapa.posicion_spawn_fuera_pantalla(self.camara, 200)
        
        boss = Enemy(x, y, "AGUARA_GUAZU")
        boss.jugador = self.jugador
        
        # Escalar stats del boss según tiempo
        multiplicador = 1 + (self.tiempo_juego / 600)  # +100% cada 10 min
        boss.vida_maxima *= multiplicador
        boss.vida_actual *= multiplicador
        boss.daño *= multiplicador
        
        self.enemigos.append(boss)
        
        # Spawnear enemigos menores alrededor del boss
        PARA _ EN range(10):
            offset_x = random.randint(-200, 200)
            offset_y = random.randint(-200, 200)
            
            enemigo = Enemy(x + offset_x, y + offset_y, "CARPINCHO")
            enemigo.jugador = self.jugador
            self.enemigos.append(enemigo)
        """
        pass
    
    
    def obtener_estadisticas(self):
        """
        Obtener estadísticas de spawn
        
        PSEUDOCÓDIGO:
        RETORNAR {
            "enemigos_activos": len(self.enemigos),
            "enemigos_por_spawn": self.enemigos_por_spawn,
            "tiempo_entre_spawns": self.tiempo_entre_spawns,
            "tiempo_juego": int(self.tiempo_juego)
        }
        """
        pass
        '''