"""
COMBAT_MANAGER.PY - GESTIÓN DE COMBATE Y COLISIONES
====================================================
Maneja interacciones entre jugador, enemigos, armas y orbes XP
"""
import random
import pygame
import math
from entities.enemy import OrbXP
from settings import *


class CombatManager:
    """Gestor de combate y colisiones del juego"""
    
    def __init__(self, jugador, spawn_manager):
        """
        Inicializar combat manager
        
        Args:
            jugador: Objeto Player
            spawn_manager: Objeto SpawnManager
        """
        self.jugador = jugador
        self.spawn_manager = spawn_manager
        
        # Orbes de XP en el mapa
        self.orbes_xp = []
        
        # Efectos visuales activos
        self.efectos = []
        
        # Estadísticas
        self.stats = {
            "daño_total_infligido": 0,
            "daño_total_recibido": 0,
            "xp_total_recolectada": 0
        }
    
    def actualizar(self, dt):
        """
        Actualizar sistema de combate
        
        Args:
            dt: Delta time en segundos
        """
        # Verificar colisiones enemigos-jugador
        self.verificar_colisiones_enemigos_jugador()
        
        # Actualizar armas del jugador y verificar hits
        self.actualizar_armas_jugador(dt)
        
        # Actualizar orbes de XP
        self.actualizar_orbes_xp(dt)
        
        # Recolectar XP cercana
        self.jugador.recolectar_xp_cercana(self.orbes_xp)
        
        # Actualizar efectos visuales
        self.actualizar_efectos(dt)
    
    def verificar_colisiones_enemigos_jugador(self):
        """Verificar si enemigos tocan al jugador"""
        for enemigo in self.spawn_manager.enemigos:
            if not enemigo.esta_vivo:
                continue
            
            # El enemigo ya maneja su propio ataque
            # Solo necesitamos que esté cerca
            pass
    
    def actualizar_armas_jugador(self, dt):
        """
        Actualizar todas las armas y verificar impactos
        
        Args:
            dt: Delta time en segundos
        """
        for arma in self.jugador.armas_equipadas:
            # Actualizar arma
            arma.actualizar(dt, self.spawn_manager.enemigos)
            
            # Aplicar buff si está activo
            arma.aplicar_buff(dt)
            
            # Si es arma de proyectiles, verificar colisiones
            if len(arma.proyectiles) > 0:
                self.verificar_proyectiles(arma)
    
    def verificar_proyectiles(self, arma):
        """
        Verificar colisiones de proyectiles con enemigos
        
        Args:
            arma: Objeto Weapon
        """
        for proyectil in arma.proyectiles:
            if proyectil.debe_eliminarse:
                continue
            
            proyectil.verificar_colision_enemigos(self.spawn_manager.enemigos)
    
    def crear_orbe_xp(self, x, y, cantidad):
        """
        Crear orbe de XP en una posición
        
        Args:
            x: Posición X en el mundo
            y: Posición Y en el mundo
            cantidad: Valor de XP del orbe
        """
        orbe = OrbXP(x, y, cantidad)
        self.orbes_xp.append(orbe)
        
        # Limitar cantidad de orbes para no saturar
        if len(self.orbes_xp) > MAX_ORBES_XP:
            self.orbes_xp.pop(0)  # Eliminar el más viejo
    
    def actualizar_orbes_xp(self, dt):
        """
        Actualizar animación de orbes
        
        Args:
            dt: Delta time en segundos
        """
        for orbe in self.orbes_xp:
            orbe.actualizar(dt)
    
    def crear_efecto_impacto(self, x, y):
        """
        Crear efecto visual de impacto
        
        Args:
            x: Posición X en el mundo
            y: Posición Y en el mundo
        """
        efecto = EfectoImpacto(x, y)
        self.efectos.append(efecto)
    
    def actualizar_efectos(self, dt):
        """
        Actualizar y limpiar efectos visuales
        
        Args:
            dt: Delta time en segundos
        """
        efectos_activos = []
        
        for efecto in self.efectos:
            efecto.actualizar(dt)
            
            if not efecto.completado:
                efectos_activos.append(efecto)
        
        self.efectos = efectos_activos
    
    def verificar_muerte_enemigo(self, enemigo):
        """
        Callback cuando un enemigo muere
        
        Args:
            enemigo: Objeto Enemy que murió
        """
        if not enemigo.esta_vivo:
            # Crear orbe de XP
            self.crear_orbe_xp(enemigo.x, enemigo.y, enemigo.xp_drop)
    
    def dibujar(self, pantalla, camara):
        """
        Dibujar elementos de combate
        
        Args:
            pantalla: Surface de pygame
            camara: Objeto Camera
        """
        # Dibujar orbes de XP
        for orbe in self.orbes_xp:
            if camara.esta_visible(orbe):
                orbe.dibujar(pantalla, camara)
        
        # Dibujar armas del jugador (proyectiles, efectos)
        for arma in self.jugador.armas_equipadas:
            arma.dibujar(pantalla, camara)
        
        # Dibujar efectos visuales
        for efecto in self.efectos:
            efecto.dibujar(pantalla, camara)
    
    def obtener_estadisticas(self):
        """
        Obtener estadísticas de combate
        
        Returns:
            dict: Diccionario con estadísticas
        """
        return {
            "daño_infligido": self.stats["daño_total_infligido"],
            "daño_recibido": self.stats["daño_total_recibido"],
            "xp_recolectada": self.stats["xp_total_recolectada"],
            "orbes_activas": len(self.orbes_xp)
        }


class EfectoImpacto:
    """Efecto visual de impacto (círculo expandiéndose)"""
    
    def __init__(self, x, y):
        """
        Inicializar efecto
        
        Args:
            x: Posición X en el mundo
            y: Posición Y en el mundo
        """
        self.x = x
        self.y = y
        self.tiempo_vida = 0
        self.duracion = 0.3  # segundos
        self.completado = False
        self.tamaño = 20
        self.alpha = 255
    
    def actualizar(self, dt):
        """
        Actualizar expansión y fade
        
        Args:
            dt: Delta time en segundos
        """
        self.tiempo_vida += dt
        
        # Expandir y desvanecer
        self.tamaño += 50 * dt
        self.alpha -= 850 * dt
        
        if self.tiempo_vida >= self.duracion:
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
        tamaño_int = int(self.tamaño)
        if tamaño_int > 0:
            superficie = pygame.Surface((tamaño_int * 2, tamaño_int * 2), pygame.SRCALPHA)
            color = (255, 200, 0, max(0, int(self.alpha)))
            pygame.draw.circle(
                superficie,
                color,
                (tamaño_int, tamaño_int),
                tamaño_int,
                2
            )
            pantalla.blit(superficie, (pantalla_x - tamaño_int, pantalla_y - tamaño_int))


class EfectoParticulas:
    """Sistema simple de partículas"""
    
    def __init__(self, x, y, color, cantidad, velocidad):
        """
        Inicializar sistema de partículas
        
        Args:
            x: Posición X en el mundo
            y: Posición Y en el mundo
            color: Color de las partículas (RGB)
            cantidad: Número de partículas
            velocidad: Velocidad de las partículas
        """
        self.particulas = []
        
        for _ in range(cantidad):
            angulo = random.uniform(0, 360)
            angulo_rad = math.radians(angulo)
            vel = random.uniform(velocidad * 0.5, velocidad)
            
            particula = {
                "x": x,
                "y": y,
                "vx": math.cos(angulo_rad) * vel,
                "vy": math.sin(angulo_rad) * vel,
                "vida": 1.0  # 0.0 a 1.0
            }
            self.particulas.append(particula)
        
        self.color = color
        self.completado = False
    
    def actualizar(self, dt):
        """
        Actualizar partículas
        
        Args:
            dt: Delta time en segundos
        """
        for particula in self.particulas:
            # Mover
            particula["x"] += particula["vx"] * dt
            particula["y"] += particula["vy"] * dt
            
            # Reducir vida
            particula["vida"] -= dt * 2
        
        # Eliminar partículas muertas
        self.particulas = [p for p in self.particulas if p["vida"] > 0]
        
        if len(self.particulas) == 0:
            self.completado = True
    
    def dibujar(self, pantalla, camara):
        """
        Dibujar partículas
        
        Args:
            pantalla: Surface de pygame
            camara: Objeto Camera
        """
        for particula in self.particulas:
            pantalla_x = int(particula["x"] - camara.offset_x)
            pantalla_y = int(particula["y"] - camara.offset_y)
            
            tamaño = max(1, int(particula["vida"] * 5))
            
            pygame.draw.circle(
                pantalla,
                self.color,
                (pantalla_x, pantalla_y),
                tamaño
            )