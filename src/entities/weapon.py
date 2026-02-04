"""
ARMA.PY - SISTEMA DE ARMAS
===========================
Diferentes tipos de armas con sus mecánicas únicas
"""

import pygame
import math
import random
from settings import *


class Weapon:
    """Clase base de armas"""
    
    def __init__(self, tipo, dueño, assets=None):
        """
        Inicializar arma

        Args:
            tipo: Tipo de arma (string)
            dueño: Referencia al jugador
            assets: Referencia al AssetLoader para sonidos
        """
        self.tipo = tipo
        self.dueño = dueño
        self.assets = assets
        self.nivel = 1
        
        # Obtener configuración del arma
        self.config = ARMAS_CONFIG[tipo]
        self.cooldown = self.config["cooldown"]
        self.tipo_ataque = self.config["tipo"]
        
        # Timer de cooldown
        self.timer_cooldown = 0
        self.puede_usar = True
        
        # Lista de proyectiles (para armas tipo proyectil)
        self.proyectiles = []
        
        # Lista de efectos visuales (para armas tipo AoE)
        self.efectos = []
        
        # Buff activo (para armas tipo buff)
        self.buff_activo = False
        self.timer_buff = 0
        self.duracion_buff = 0

    def subir_nivel(self):
        """
        Subir el nivel del arma (máximo 4)

        Returns:
            bool: True si subió de nivel, False si ya está al máximo
        """
        max_nivel = len(self.config["niveles"])
        if self.nivel < max_nivel:
            self.nivel += 1

            # Actualizar cooldown si el nivel tiene uno específico
            config_nivel = self.config["niveles"][self.nivel - 1]
            if "cooldown" in config_nivel:
                self.cooldown = config_nivel["cooldown"]

            return True
        return False

    def puede_mejorar(self):
        """
        Verificar si el arma puede subir de nivel

        Returns:
            bool: True si puede mejorar, False si está al máximo
        """
        max_nivel = len(self.config["niveles"])
        return self.nivel < max_nivel

    def actualizar(self, dt, enemigos):
        """
        Actualizar arma y sus proyectiles/efectos
        
        Args:
            dt: Delta time en segundos
            enemigos: Lista de enemigos
        """
        # Actualizar cooldown
        if not self.puede_usar:
            self.timer_cooldown += dt
            if self.timer_cooldown >= self.cooldown:
                self.puede_usar = True
                self.timer_cooldown = 0
        
        # Solo atacar automáticamente si NO es machete
        if self.puede_usar and len(enemigos) > 0 and self.tipo != "MACHETE":
            self.usar(enemigos)
        
        # Actualizar proyectiles
        proyectiles_activos = []
        for proyectil in self.proyectiles:
            proyectil.actualizar(dt)
            if not proyectil.debe_eliminarse:
                proyectiles_activos.append(proyectil)
        self.proyectiles = proyectiles_activos
        
        # Actualizar efectos
        efectos_activos = []
        for efecto in self.efectos:
            efecto.actualizar(dt)
            if not efecto.completado:
                efectos_activos.append(efecto)
        self.efectos = efectos_activos
        
        # Actualizar buff
        if self.buff_activo:
            self.timer_buff += dt
            if self.timer_buff >= self.duracion_buff:
                self.buff_activo = False
                self.timer_buff = 0
    
    def usar(self, enemigos):
        """
        Usar el arma según su tipo
        
        Args:
            enemigos: Lista de enemigos
        """
        if self.tipo_ataque == "melee":
            self.ataque_machete(enemigos)
        elif self.tipo_ataque == "proyectil":
            self.ataque_hacha(enemigos)
        elif self.tipo_ataque == "aoe":
            self.ataque_azada(enemigos)
        elif self.tipo_ataque == "buff":
            self.buff_terere()
        
        # Activar cooldown
        self.puede_usar = False
        self.timer_cooldown = 0
    
    def ataque_machete(self, enemigos):
        """
        Ataque melee circular alrededor del jugador con efecto visual
        Usa colisión de hitbox para detectar enemigos

        Args:
            enemigos: Lista de enemigos
        """
        config_nivel = self.config["niveles"][self.nivel - 1]
        daño = config_nivel["daño"]
        alcance = config_nivel["alcance"]

        # Determinar dirección del slash basado en el último movimiento
        direccion = self.dueño.direccion
        if direccion.length() == 0:
            # Si está quieto, slash hacia la derecha por defecto
            direccion = pygame.math.Vector2(1, 0)

        # Crear efecto visual del slash
        efecto_slash = EfectoSlashMachete(
            self.dueño.x,
            self.dueño.y,
            direccion,
            alcance
        )
        self.efectos.append(efecto_slash)

        # Reproducir sonido del machete
        if self.assets:
            self.assets.reproducir_sonido("ataque_machete", volumen=0.4)

        # Crear área de ataque (rectángulo centrado en el jugador)
        area_ataque = pygame.Rect(
            self.dueño.x - alcance,
            self.dueño.y - alcance,
            alcance * 2,
            alcance * 2
        )

        # Aplicar daño a enemigos cuyo hitbox colisiona con el área de ataque
        for enemigo in enemigos:
            if not enemigo.esta_vivo:
                continue

            # Verificar colisión de hitbox
            if area_ataque.colliderect(enemigo.rect):
                # Aplicar daño
                enemigo.recibir_daño(daño)

                # Calcular dirección para knockback (desde centro del jugador al enemigo)
                dx = enemigo.x - self.dueño.x
                dy = enemigo.y - self.dueño.y
                distancia = math.sqrt(dx * dx + dy * dy)

                # Aplicar knockback
                if distancia > 0:
                    direccion_kb = pygame.math.Vector2(dx / distancia, dy / distancia)
                    enemigo.recibir_knockback(direccion_kb, KNOCKBACK_FUERZA_MACHETE)
    
    def ataque_hacha(self, enemigos):
        """
        Disparar un solo proyectil de rifle hacia el enemigo más cercano

        Args:
            enemigos: Lista de enemigos
        """
        config_nivel = self.config["niveles"][self.nivel - 1]
        daño = config_nivel["daño"]
        velocidad = config_nivel["velocidad"]

        # Encontrar enemigo más cercano
        enemigos_vivos = [e for e in enemigos if e.esta_vivo]
        if not enemigos_vivos:
            return

        # Encontrar el más cercano
        enemigo_objetivo = min(
            enemigos_vivos,
            key=lambda e: math.sqrt((e.x - self.dueño.x)**2 + (e.y - self.dueño.y)**2)
        )

        # Calcular dirección hacia el enemigo más cercano
        dx = enemigo_objetivo.x - self.dueño.x
        dy = enemigo_objetivo.y - self.dueño.y
        distancia = math.sqrt(dx * dx + dy * dy)

        if distancia > 0:
            direccion = pygame.math.Vector2(dx / distancia, dy / distancia)

            # Crear un solo proyectil de rifle
            proyectil = ProyectilRifle(
                self.dueño.x,
                self.dueño.y,
                direccion,
                velocidad,
                daño
            )
            self.proyectiles.append(proyectil)

            # Reproducir sonido del rifle
            if self.assets:
                self.assets.reproducir_sonido("ataque_rifle", volumen=0.3)
    
    def ataque_azada(self, enemigos):
        """
        Ataque AoE que daña a todos los enemigos en un radio
        
        Args:
            enemigos: Lista de enemigos
        """
        config_nivel = self.config["niveles"][self.nivel - 1]
        daño = config_nivel["daño"]
        radio = config_nivel["radio"]
        
        for enemigo in enemigos:
            if not enemigo.esta_vivo:
                continue
            
            # Calcular distancia
            dx = enemigo.x - self.dueño.x
            dy = enemigo.y - self.dueño.y
            distancia = math.sqrt(dx * dx + dy * dy)
            
            if distancia <= radio:
                # Aplicar daño
                enemigo.recibir_daño(daño)
                
                # Aplicar knockback fuerte
                if distancia > 0:
                    direccion = pygame.math.Vector2(dx / distancia, dy / distancia)
                    enemigo.recibir_knockback(direccion, KNOCKBACK_FUERZA_AZADA)
        
        # Crear efecto visual
        efecto = EfectoAzada(self.dueño.x, self.dueño.y, radio)
        self.efectos.append(efecto)
    
    def buff_terere(self):
        """Aplicar buff de regeneración al jugador"""
        config_nivel = self.config["niveles"][self.nivel - 1]
        self.vida_por_seg = config_nivel["vida_por_seg"]
        self.duracion_buff = config_nivel["duracion"]
        
        self.buff_activo = True
        self.timer_buff = 0
    
    def aplicar_buff(self, dt):
        """
        Aplicar efectos del buff si está activo
        
        Args:
            dt: Delta time en segundos
        """
        if self.buff_activo and self.tipo == "TERERE":
            self.dueño.curar(self.vida_por_seg * dt)
    
    def subir_nivel(self):
        """Subir nivel del arma"""
        if self.nivel < len(self.config["niveles"]):
            self.nivel += 1
    
    def dibujar(self, pantalla, camara):
        """
        Dibujar proyectiles y efectos del arma
        
        Args:
            pantalla: Surface de pygame
            camara: Objeto Camera
        """
        # Dibujar proyectiles
        for proyectil in self.proyectiles:
            proyectil.dibujar(pantalla, camara)
        
        # Dibujar efectos
        for efecto in self.efectos:
            efecto.dibujar(pantalla, camara)


class ProyectilRifle:
    """Proyectil de rifle (bala)"""
    
    def __init__(self, x, y, direccion, velocidad, daño):
        """
        Inicializar proyectil
        
        Args:
            x: Posición X inicial
            y: Posición Y inicial
            direccion: Vector2 de dirección
            velocidad: Velocidad en píxeles/segundo
            daño: Daño que inflige
        """
        self.x = float(x)
        self.y = float(y)
        self.direccion = direccion
        self.velocidad = velocidad
        self.daño = daño
        
        # Crear sprite - Intentar cargar imagen, si falla usar superficie de color
        try:
            self.image = pygame.image.load("assets/sprites/proyectil_rifle.png").convert_alpha()
            # Escalar la imagen a un tamaño de bala más pequeño
            self.image = pygame.transform.scale(self.image, (16, 16))
        except:
            # Fallback: superficie de color si no existe la imagen
            self.image = pygame.Surface((16, 16))
            self.image.fill((192, 192, 192))  # Gris plateado

        self.rect = self.image.get_rect()
        self.rect.center = (int(self.x), int(self.y))
        
        # Distancia recorrida
        self.distancia_recorrida = 0
        self.alcance_maximo = PROYECTIL_RIFLE_ALCANCE
        
        # Rotación
        self.angulo = 0
        
        # Enemigos ya golpeados
        self.enemigos_golpeados = []
        
        # Flag de eliminación
        self.debe_eliminarse = False
    
    def actualizar(self, dt):
        """
        Actualizar posición y rotación
        
        Args:
            dt: Delta time en segundos
        """
        # Mover
        desplazamiento = self.velocidad * dt
        self.x += self.direccion.x * desplazamiento
        self.y += self.direccion.y * desplazamiento
        self.rect.center = (int(self.x), int(self.y))
        
        # Actualizar distancia
        self.distancia_recorrida += desplazamiento
        
        # Rotar
        self.angulo += PROYECTIL_RIFLE_ROTACION * dt
        
        # Verificar si debe eliminarse
        if self.distancia_recorrida >= self.alcance_maximo:
            self.debe_eliminarse = True
    
    def verificar_colision_enemigos(self, enemigos):
        """
        Verificar colisión con enemigos
        
        Args:
            enemigos: Lista de enemigos
        """
        for enemigo in enemigos:
            if not enemigo.esta_vivo:
                continue
            
            if enemigo in self.enemigos_golpeados:
                continue
            
            # Verificar colisión
            if self.rect.colliderect(enemigo.rect):
                enemigo.recibir_daño(self.daño)
                self.enemigos_golpeados.append(enemigo)
                
                # Aplicar knockback
                dx = enemigo.x - self.x
                dy = enemigo.y - self.y
                distancia = math.sqrt(dx * dx + dy * dy)
                if distancia > 0:
                    direccion = pygame.math.Vector2(dx / distancia, dy / distancia)
                    enemigo.recibir_knockback(direccion, KNOCKBACK_FUERZA_RIFLE)
    
    def dibujar(self, pantalla, camara):
        """
        Dibujar proyectil
        
        Args:
            pantalla: Surface de pygame
            camara: Objeto Camera
        """
        pantalla_x = self.rect.x - camara.offset_x
        pantalla_y = self.rect.y - camara.offset_y
        
        # Solo dibujar si está en pantalla
        if -50 < pantalla_x < pantalla.get_width() + 50 and -50 < pantalla_y < pantalla.get_height() + 50:
            # Rotar imagen
            imagen_rotada = pygame.transform.rotate(self.image, self.angulo)
            rect_rotado = imagen_rotada.get_rect(center=(pantalla_x + 10, pantalla_y + 10))
            pantalla.blit(imagen_rotada, rect_rotado)


class EfectoAzada:
    """Efecto visual del ataque de azada (círculo expandiéndose)"""
    
    def __init__(self, x, y, radio_final):
        """
        Inicializar efecto
        
        Args:
            x: Posición X del centro
            y: Posición Y del centro
            radio_final: Radio final del círculo
        """
        self.x = x
        self.y = y
        self.radio_actual = 0
        self.radio_final = radio_final
        self.velocidad_expansion = 500  # píxeles por segundo
        
        self.alpha = 255
        self.completado = False
    
    def actualizar(self, dt):
        """
        Actualizar expansión y fade
        
        Args:
            dt: Delta time en segundos
        """
        # Expandir
        self.radio_actual += self.velocidad_expansion * dt
        
        # Fade out
        self.alpha -= 850 * dt
        
        # Marcar como completado
        if self.radio_actual >= self.radio_final or self.alpha <= 0:
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
        radio_int = int(self.radio_actual)
        if radio_int > 0:
            superficie = pygame.Surface((radio_int * 2, radio_int * 2), pygame.SRCALPHA)
            color = (255, 200, 100, max(0, int(self.alpha)))
            pygame.draw.circle(superficie, color, (radio_int, radio_int), radio_int, 3)
            pantalla.blit(superficie, (pantalla_x - radio_int, pantalla_y - radio_int))


class EfectoSlashMachete:
    """Efecto visual de slash del machete (arco que se expande)"""
    
    def __init__(self, x, y, direccion, alcance):
        """
        Inicializar efecto de slash
        
        Args:
            x: Posición X del jugador
            y: Posición Y del jugador
            direccion: Dirección hacia donde mira el jugador
            alcance: Alcance del machete
        """
        self.x = x
        self.y = y
        self.direccion = direccion
        self.alcance = alcance
        
        # Animación
        self.progreso = 0  # 0.0 a 1.0
        self.velocidad_animacion = 5.0  # Muy rápido
        self.completado = False
        
        # Ángulo del slash (más amplio)
        self.angulo_inicio = -120  # Comienza más arriba
        self.angulo_fin = 120      # Termina más abajo
        
        # Calcular ángulo base según dirección
        if abs(direccion.x) > abs(direccion.y):
            # Horizontal
            if direccion.x > 0:
                self.angulo_base = 0  # Derecha
            else:
                self.angulo_base = 180  # Izquierda
        else:
            # Vertical
            if direccion.y > 0:
                self.angulo_base = 90  # Abajo
            else:
                self.angulo_base = -90  # Arriba
    
    def actualizar(self, dt):
        """
        Actualizar animación del slash
        
        Args:
            dt: Delta time en segundos
        """
        self.progreso += self.velocidad_animacion * dt
        
        if self.progreso >= 1.0:
            self.completado = True
    
    def dibujar(self, pantalla, camara):
        """
        Dibujar el slash animado
        
        Args:
            pantalla: Surface de pygame
            camara: Objeto Camera
        """
        if self.completado:
            return 
        
        # Posición en pantalla
        pantalla_x = int(self.x - camara.offset_x)
        pantalla_y = int(self.y - camara.offset_y)
        
        # Calcular ángulo actual del slash según progreso
        angulo_actual = self.angulo_inicio + (self.angulo_fin - self.angulo_inicio) * self.progreso
        angulo_total = self.angulo_base + angulo_actual
        
        # Convertir a radianes
        angulo_rad = math.radians(angulo_total)
        
        # Calcular punto final del slash
        end_x = pantalla_x + math.cos(angulo_rad) * self.alcance
        end_y = pantalla_y + math.sin(angulo_rad) * self.alcance
        
        # Calcular alpha (más transparente al final)
        alpha = int(255 * (1.0 - self.progreso))
        
        # Dibujar arco
        color = (220, 220, 255, alpha)  # Blanco-azulado
        
        # Crear superficie temporal con transparencia
        temp_surface = pygame.Surface((self.alcance * 2, self.alcance * 2), pygame.SRCALPHA)
        
        # Dibujar línea del slash (más gruesa)
        grosor = int(18 * (1.0 - self.progreso * 0.5))  # Más grueso
        
        # Calcular posiciones relativas a la superficie temporal
        centro = (self.alcance, self.alcance)
        punto_final = (
            int(centro[0] + math.cos(angulo_rad) * self.alcance),
            int(centro[1] + math.sin(angulo_rad) * self.alcance)
        )
        
        pygame.draw.line(temp_surface, color, centro, punto_final, grosor)
        
        # Dibujar en pantalla
        pos_blit = (pantalla_x - self.alcance, pantalla_y - self.alcance)
        pantalla.blit(temp_surface, pos_blit)   