"""
SPAWN_MANAGER.PY - GESTIÓN DE APARICIÓN DE ENEMIGOS
====================================================
Controla cuándo y dónde aparecen enemigos, escalando dificultad
"""

import pygame
import random
import math
from entities.enemy import Enemy
from settings import *


class SpawnManager:
    """Gestor de spawning de enemigos con escalado de dificultad"""
    
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
        
        # Tiempo de juego (para escalar dificultad)
        self.tiempo_juego = 0
        self.ultimo_escalado = 0
        
        # Límite de enemigos en pantalla
        self.max_enemigos = MAX_ENEMIGOS_PANTALLA
        
        # Referencia al combat_manager (se asigna desde engine)
        self.combat_manager = None
    
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
        
        # Escalar dificultad cada minuto
        if int(self.tiempo_juego) > self.ultimo_escalado and int(self.tiempo_juego) % 60 == 0:
            self.escalar_dificultad()
            self.ultimo_escalado = int(self.tiempo_juego)
        
        # Verificar si es momento de spawnear
        if self.timer_spawn >= self.tiempo_entre_spawns:
            if len(self.enemigos) < self.max_enemigos:
                self.spawnear_enemigos()
            self.timer_spawn = 0
        
        # Actualizar todos los enemigos
        self.actualizar_enemigos(dt)
        
        # Eliminar enemigos muertos
        self.limpiar_enemigos_muertos()
    
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
            
            # Agregar tipo 'peso' veces a la lista
            for _ in range(int(peso)):
                opciones.append(tipo)
        
        # Elegir aleatoriamente
        if opciones:
            return random.choice(opciones)
        else:
            return "CARPINCHO"  # Fallback
    
    def escalar_dificultad(self):
        """Aumentar dificultad progresivamente"""
        # Reducir tiempo entre spawns (hasta un mínimo)
        if self.tiempo_entre_spawns > SPAWN_MINIMO:
            self.tiempo_entre_spawns -= SPAWN_REDUCCION_POR_MINUTO
            self.tiempo_entre_spawns = max(SPAWN_MINIMO, self.tiempo_entre_spawns)
        
        # Aumentar cantidad de enemigos por spawn cada 2 minutos
        if int(self.tiempo_juego) % AUMENTO_ENEMIGOS_CADA == 0:
            self.enemigos_por_spawn += 1
    
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
        """Eliminar enemigos muertos de la lista y crear orbes de XP"""
        # Primero crear orbes de XP para los enemigos muertos
        if self.combat_manager:
            for enemigo in self.enemigos:
                if not enemigo.esta_vivo:
                    # Crear orbe de XP en la posición del enemigo
                    self.combat_manager.crear_orbe_xp(enemigo.x, enemigo.y, enemigo.xp_drop)

        # Luego eliminar los enemigos muertos
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
            distancia = math.sqrt(dx * dx + dy * dy)
            
            if distancia <= rango:
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
        if len(self.enemigos) == 0:
            return None
        
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
        return {
            "enemigos_activos": len(self.enemigos),
            "enemigos_por_spawn": self.enemigos_por_spawn,
            "tiempo_entre_spawns": self.tiempo_entre_spawns,
            "tiempo_juego": int(self.tiempo_juego)
        }