"""
SPAWN_MANAGER.PY - GESTIÓN DE APARICIÓN DE ENEMIGOS
====================================================
Controla cuándo y dónde aparecen enemigos, escalando dificultad
"""
import logging
import pygame
import random
import math
from entities.enemy import Enemy
from settings import *

logging.basicConfig(level=logging.INFO,
format='%(asctime)s - %(levelname)s - %(message)s', datefmt="%H:%M:%S",
handlers=[
    logging.FileHandler("game.log") ,
    logging.StreamHandler()
])


class SpawnManager:
    """Gestor de spawning de enemigos con oleadas con escalado de dificultad"""
    
    def __init__(self, mapa, camara, jugador):
        """
        Inicializar spawn manager
        
        Args:
            mapa: Objeto Map
            camara: Objeto Camera
            jugador: Objeto Player
        """
        self.mapa = mapa
        self.camara = camara
        self.jugador = jugador
        
        # Lista de enemigos activos
        self.enemigos = []
        
        # Control de spawn
        self.tiempo_entre_spawns = TIEMPO_ENTRE_SPAWNS
        self.timer_spawn = 0
        self.enemigos_por_spawn = ENEMIGOS_POR_SPAWN
        self.enemigos_por_spawn_base = ENEMIGOS_POR_SPAWN
        
        # Tiempo de juego (para escalar dificultad)
        self.tiempo_juego = 0
        self.ultimo_escalado = 0
        
        # Límite de enemigos en pantalla
        self.max_enemigos = MAX_ENEMIGOS_PANTALLA

        # sistema de spawn basado en oleadas
        self.estado_oleada = "NORMAL"
        self.tiempo_estado = 0

        # Duracion de los estados
        self.duracion_normal = 25
        self.duracion_horda = 12
        self.duracion_descanso = 8

        # spawns por estado
        self.factores_spawn = {
            "NORMAL": 1.0 ,
            "HORDA": 0.4,
            "DESCANSO": 1.6
        }

        logging.info("SpawnManager inicializado .Estado inicial: NORMAL")

    def actualizar(self, dt):
        """
        Actualizar spawns y enemigos
        
        Args:
            dt: Delta time en segundos
        """
        # Actualizar tiempo de juego
        self.tiempo_juego += dt
        
        # Actualizar timers de spawn
        self.timer_spawn += dt

        # Actualizar estado de oleada
        self.actualizar_oleada(dt)
        
        # Escalar dificultad cada minuto
        if int(self.tiempo_juego) > self.ultimo_escalado and int(self.tiempo_juego) % 60 == 0:
            self.escalar_dificultad()
            self.ultimo_escalado = int(self.tiempo_juego)
            logging.info(f"Dificultad escalada: tiempo entre spawns {self.tiempo_entre_spawns}, enemigos por spawn {self.enemigos_por_spawn}")
        
        # Verificar si es momento de spawnear
        if self.timer_spawn >= self.tiempo_entre_spawns:
            if len(self.enemigos) < self.max_enemigos:
                self.spawnear_enemigos()
            self.timer_spawn = 0
        
        # Actualizar todos los enemigos
        self.actualizar_enemigos(dt)
        
        # Eliminar enemigos muertos
        self.limpiar_enemigos_muertos()


    # Methodo para actualizar el estado de la oleada
    def actualizar_oleada(self, dt):
        self.tiempo_estado += dt
        estado_anterior = self.estado_oleada

        if self.estado_oleada == "NORMAL" and self.tiempo_estado >= self.duracion_normal:
            self.estado_oleada = "HORDA"
            self.tiempo_estado = 0
        elif self.estado_oleada == "HORDA" and self.tiempo_estado >= self.duracion_horda:
            self.estado_oleada = "DESCANSO"
            self.tiempo_estado = 0
        elif self.estado_oleada == "DESCANSO" and self.tiempo_estado >= self.duracion_descanso:
            self.estado_oleada = "NORMAL"
            self.tiempo_estado = 0

        factor = self.factores_spawn[self.estado_oleada]
        self.tiempo_entre_spawns = max(SPAWN_MINIMO, TIEMPO_ENTRE_SPAWNS * factor)
        self.enemigos_por_spawn = max(1, int(self.enemigos_por_spawn_base * factor))
        if estado_anterior != self.estado_oleada:
            logging.info(f"Cambio de estado de oleada: {self.estado_oleada}")


    def escalar_dificultad(self):
        """Aumentar dificultad progresivamente"""
        # Reducir tiempo entre spawns (hasta un mínimo)
        if self.tiempo_entre_spawns > SPAWN_MINIMO:
            self.tiempo_entre_spawns -= SPAWN_REDUCCION_POR_MINUTO
            self.tiempo_entre_spawns = max(SPAWN_MINIMO, self.tiempo_entre_spawns)
        
        # Aumentar cantidad de enemigos por spawn cada 2 minutos
        if int(self.tiempo_juego) % AUMENTO_ENEMIGOS_CADA == 0:
            self.enemigos_por_spawn += 1
    
    
    def spawnear_enemigos(self):
        """Crear nuevos enemigos"""
        for i in range(self.enemigos_por_spawn):
            # Elegir tipo de enemigo según probabilidades
            tipo_enemigo = self.elegir_tipo_enemigo()
            
            # Obtener posición de spawn (fuera de pantalla)
            x, y = self.mapa.posicion_spawn_fuera_pantalla(
                self.camara, 
                margen=SPAWN_MARGEN_PANTALLA
            )
            
            # Crear enemigo
            enemigo = Enemy(x, y, tipo_enemigo)
            enemigo.jugador = self.jugador  # Asignar referencia al jugador
            
            self.enemigos.append(enemigo)
            logging.info(f"Spawn enemigo: {tipo_enemigo} en ({x:.2f}, {y:.2f})")
    
    def elegir_tipo_enemigo(self):
        """
        Elegir tipo de enemigo según pesos de spawn
        
        Returns:
            string: Tipo de enemigo
        """
        # Crear lista ponderada de tipos
        opciones = []
        
        for tipo, config in ENEMIGO_CONFIGS.items():
            peso = config["spawn_peso"]
            
            # Ajustar peso según tiempo de juego
            # Enemigos más fuertes aparecen más seguido con el tiempo
            if tipo == "AGUARA_GUAZU":  # Boss
                # Solo aparece después de 5 minutos
                if self.tiempo_juego < 300:
                    peso = 0
                else:
                    peso = int(peso * (self.tiempo_juego / 300))

            # En hordas aparecen más enemigos fuertes
            if self.estado_oleada == "HORDA":
                peso = max(1 ,int(peso *1.5))

            
            # Agregar tipo 'peso' veces a la lista
            for _ in range(int(peso)):
                opciones.append(tipo)
        
        # Elegir aleatoriamente
        return random.choice(opciones) if opciones else "CARPINCHO"
    
    
    def actualizar_enemigos(self, dt):
        """
        Actualizar todos los enemigos vivos
        
        Args:
            dt: Delta time en segundos
        """
        for enemigo in self.enemigos:
            if enemigo.esta_vivo:
                enemigo.actualizar(dt)
    
    def limpiar_enemigos_muertos(self):
        """Eliminar enemigos muertos de la lista"""
        muertos = [e for e in self.enemigos if not e.esta_vivo]
        for m in muertos:
            logging.info(f"Enemigo muerto: {m.tipo} en ({m.x:.2f}, {m.y:.2f})")
        self.enemigos = [e for e in self.enemigos if e.esta_vivo]
    
    def obtener_enemigos_en_rango(self, x, y, rango):
        """
        Obtener enemigos dentro de un rango
        (Útil para detectar objetivos de armas)
        
        Args:
            x: Posición X en el mundo
            y: Posición Y en el mundo
            rango: Radio de búsqueda
            
        Returns:
            list: Lista de enemigos en rango
        """
        enemigos_cercanos = []
        
        for enemigo in self.enemigos:
            if not enemigo.esta_vivo:
                continue
            
            # Calcular distancia
            dx = enemigo.x - x
            dy = enemigo.y - y
            if math.sqrt(dx * dx + dy * dy) <= rango:
                enemigos_cercanos.append(enemigo)
        
        return enemigos_cercanos
    
    def obtener_enemigo_mas_cercano(self, x, y):
        """
        Obtener el enemigo más cercano a una posición
        
        Args:
            x: Posición X en el mundo
            y: Posición Y en el mundo
            
        Returns:
            Enemy: Enemigo más cercano, o None
        """
        
        enemigo_cercano = None
        distancia_minima = float('inf')
        
        for enemigo in self.enemigos:
            if not enemigo.esta_vivo:
                continue
            
            dx = enemigo.x - x
            dy = enemigo.y - y
            distancia = math.sqrt(dx * dx + dy * dy)
            
            if distancia < distancia_minima:
                distancia_minima = distancia
                enemigo_cercano = enemigo
        
        return enemigo_cercano
    
    def dibujar(self, pantalla, camara):
        """
        Dibujar todos los enemigos visibles
        
        Args:
            pantalla: Surface de pygame
            camara: Objeto Camera
        """
        for enemigo in self.enemigos:
            if enemigo.esta_vivo:
                # Solo dibujar si está visible
                if camara.esta_visible(enemigo):
                    enemigo.dibujar(pantalla, camara)
    
    def obtener_estadisticas(self):
        """
        Obtener estadísticas de spawn
        
        Returns:
            dict: Diccionario con estadísticas
        """
        stats = {
            "enemigos_activos": len(self.enemigos),
            "enemigos_por_spawn": self.enemigos_por_spawn,
            "tiempo_entre_spawns": self.tiempo_entre_spawns,
            "tiempo_juego": int(self.tiempo_juego)
        }
        logging.info(f"Estadísticas de Spawn: {stats}")
        return stats