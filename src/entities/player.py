"""
PLAYER.PY - LÓGICA DEL CAMPESINO
=================================
Control del jugador, stats, nivel y armas
"""

import pygame
import random
from entities.base_entity import BaseEntity
from settings import *

class Player(BaseEntity):
    """Clase del jugador - Campesino Paraguayo"""
    
    def __init__(self, x, y):
        """
        Inicializar jugador
        
        Args:
            x: Posición X inicial
            y: Posición Y inicial
        """
        # Llamar constructor padre (cuadrado amarillo)
        super().__init__(x, y, 50, 50, (255, 200, 0))
        
        # Stats del campesino
        self.vida_maxima = CAMPESINO_VIDA_MAX
        self.vida_actual = CAMPESINO_VIDA_MAX
        self.velocidad = CAMPESINO_VELOCIDAD
        
        # Sistema de experiencia y nivel
        self.nivel = 1
        self.xp_actual = 0
        self.xp_necesaria = XP_POR_NIVEL[0]
        
        # Inventario de armas
        self.armas_equipadas = []
        self.armas_disponibles = ["MACHETE"]  # Empieza con machete
        
        # Radio de recolección de XP
        self.radio_recoleccion = CAMPESINO_RADIO_RECOLECCION
        
        # Cooldown de invulnerabilidad al recibir daño
        self.invulnerable = False
        self.tiempo_invulnerabilidad = 0
        self.duracion_invulnerabilidad = INVULNERABILIDAD_DURACION
        
        # Stats de juego
        self.enemigos_matados = 0
        self.tiempo_supervivencia = 0
        
        # Flag para subida de nivel
        self.subio_nivel = False
    
    def manejar_input(self):
        """Procesar input del teclado para movimiento"""
        teclas = pygame.key.get_pressed()
        
        # Resetear dirección
        self.direccion.x = 0
        self.direccion.y = 0
        
        # Movimiento WASD o flechas
        if teclas[pygame.K_w] or teclas[pygame.K_UP]:
            self.direccion.y = -1
        if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            self.direccion.y = 1
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            self.direccion.x = -1
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            self.direccion.x = 1
    
    def ganar_xp(self, cantidad):
        """
        Sumar XP y verificar subida de nivel
        
        Args:
            cantidad: Cantidad de XP a ganar
        """
        self.xp_actual += cantidad
        
        # Verificar subida de nivel
        while self.xp_actual >= self.xp_necesaria:
            self.subir_nivel()
    
    def subir_nivel(self):
        """Aumentar nivel y ofrecer mejora"""
        # Restar XP usada
        self.xp_actual -= self.xp_necesaria
        self.nivel += 1
        
        # Calcular nueva XP necesaria
        if self.nivel <= len(XP_POR_NIVEL):
            self.xp_necesaria = XP_POR_NIVEL[self.nivel - 1]
        else:
            # Fórmula exponencial para niveles altos
            self.xp_necesaria = int(XP_POR_NIVEL[-1] * (1.5 ** (self.nivel - 10)))
        
        # Curación completa al subir nivel
        self.vida_actual = self.vida_maxima
        
        # Marcar que subió nivel (para que el engine pause)
        self.subio_nivel = True
    
    def generar_opciones_mejora(self):
        """
        Generar 3 opciones aleatorias de mejora
        
        Returns:
            list: Lista de diccionarios con opciones de mejora
        """
        opciones_disponibles = []
        
        # Opción 1: Nueva arma (si hay disponibles)
        armas_disponibles_para_obtener = []
        for arma in ARMAS_CONFIG.keys():
            if arma not in self.armas_disponibles:
                armas_disponibles_para_obtener.append(arma)
        
        for arma in armas_disponibles_para_obtener:
            opciones_disponibles.append({
                "tipo": "nueva_arma",
                "valor": arma,
                "descripcion": f"Desbloquear {arma}"
            })
        
        # Opción 2: Mejorar arma existente (placeholder - implementar con sistema de armas)
        # Por ahora agregamos mejoras pasivas
        
        # Opción 3: Mejoras pasivas
        opciones_disponibles.append({
            "tipo": "aumentar_vida_max",
            "valor": MEJORAS_VALORES["vida_max"],
            "descripcion": f"+{MEJORAS_VALORES['vida_max']} Vida Máxima"
        })
        
        opciones_disponibles.append({
            "tipo": "aumentar_velocidad",
            "valor": MEJORAS_VALORES["velocidad"],
            "descripcion": f"+{MEJORAS_VALORES['velocidad']} Velocidad"
        })
        
        opciones_disponibles.append({
            "tipo": "aumentar_radio_recoleccion",
            "valor": MEJORAS_VALORES["radio_recoleccion"],
            "descripcion": f"+{MEJORAS_VALORES['radio_recoleccion']} Radio Recolección"
        })
        
        # Si hay menos de 3 opciones, duplicar algunas
        while len(opciones_disponibles) < 3:
            opciones_disponibles.append({
                "tipo": "aumentar_vida_max",
                "valor": MEJORAS_VALORES["vida_max"],
                "descripcion": f"+{MEJORAS_VALORES['vida_max']} Vida Máxima"
            })
        
        # Elegir 3 opciones aleatorias
        if len(opciones_disponibles) > 3:
            opciones_mostrar = random.sample(opciones_disponibles, 3)
        else:
            opciones_mostrar = opciones_disponibles[:3]
        
        return opciones_mostrar
    
    def aplicar_mejora(self, tipo_mejora, valor):
        """
        Aplicar la mejora elegida
        
        Args:
            tipo_mejora: Tipo de mejora (string)
            valor: Valor de la mejora
        """
        if tipo_mejora == "nueva_arma":
            # Agregar arma a disponibles
            if valor not in self.armas_disponibles:
                self.armas_disponibles.append(valor)
        
        elif tipo_mejora == "aumentar_vida_max":
            self.vida_maxima += valor
            self.vida_actual += valor  # También cura
        
        elif tipo_mejora == "aumentar_velocidad":
            self.velocidad += valor
        
        elif tipo_mejora == "aumentar_radio_recoleccion":
            self.radio_recoleccion += valor
    
    def recibir_daño(self, cantidad):
        """
        Sobrescribir para incluir invulnerabilidad
        
        Args:
            cantidad: Cantidad de daño a recibir
        """
        if not self.invulnerable:
            super().recibir_daño(cantidad)
            
            # Activar invulnerabilidad temporal
            self.invulnerable = True
            self.tiempo_invulnerabilidad = 0
    
    def actualizar_invulnerabilidad(self, dt):
        """
        Actualizar timer de invulnerabilidad
        
        Args:
            dt: Delta time en segundos
        """
        if self.invulnerable:
            self.tiempo_invulnerabilidad += dt
            
            if self.tiempo_invulnerabilidad >= self.duracion_invulnerabilidad:
                self.invulnerable = False
                self.tiempo_invulnerabilidad = 0
    
    def actualizar_armas(self, dt, enemigos):
        """
        Actualizar todas las armas equipadas
        
        Args:
            dt: Delta time en segundos
            enemigos: Lista de enemigos
        """
        for arma in self.armas_equipadas: 
            arma.actualizar(dt, enemigos) 
            
            
    def usar_machete_manual(self, enemigos):
        """
        Usar machete manualmente cuando se presiona ESPACIO
        
        Args:
            enemigos: Lista de enemigos
        """
        for arma in self.armas_equipadas:
            if arma.tipo == "MACHETE":
                if arma.puede_usar:
                    arma.usar(enemigos)
                break
            
    def recolectar_xp_cercana(self, orbes_xp):
        """
        Atraer y recolectar orbes de XP cercanas
        
        Args:
            orbes_xp: Lista de orbes de XP
        """
        orbes_a_eliminar = []
        
        for orbe in orbes_xp:
            distancia = self.distancia_a(orbe)
            
            if distancia <= self.radio_recoleccion:
                # Atraer orbe hacia jugador
                direccion = orbe.direccion_hacia(self)
                orbe.x += direccion.x * 300 * 0.016  # Aproximación de dt
                orbe.y += direccion.y * 300 * 0.016
                orbe.rect.center = (int(orbe.x), int(orbe.y))
                
                # Si toca al jugador, recolectar
                if self.colisiona_con(orbe):
                    self.ganar_xp(orbe.cantidad)
                    orbes_a_eliminar.append(orbe)
        
        # Eliminar orbes recolectadas
        for orbe in orbes_a_eliminar:
            if orbe in orbes_xp:
                orbes_xp.remove(orbe)
    
    def limitar_al_mapa(self):
        """No permitir que salga del mapa"""
        if self.x < 0:
            self.x = 0
        if self.x > MAPA_ANCHO_PIXELES:
            self.x = MAPA_ANCHO_PIXELES
        if self.y < 0:
            self.y = 0
        if self.y > MAPA_ALTO_PIXELES:
            self.y = MAPA_ALTO_PIXELES
        
        # Actualizar rect
        self.rect.center = (int(self.x), int(self.y))
    
    def al_morir(self):
        """Callback cuando muere el jugador"""
        # El engine manejará el game over
        pass
    
    def dibujar(self, pantalla, camara):
        """
        Dibujar con efecto de parpadeo si es invulnerable
        
        Args:
            pantalla: Surface de pygame
            camara: Objeto Camera
        """
        if self.invulnerable:
            # Parpadear cada 0.1 segundos
            if int(self.tiempo_invulnerabilidad * 10) % 2 == 0:
                super().dibujar(pantalla, camara)
        else:
            super().dibujar(pantalla, camara)
    
    def actualizar(self, dt):
        """
        Actualización principal del jugador
        
        Args:
            dt: Delta time en segundos
        """
        # Manejar input
        self.manejar_input()
        
        # Mover
        self.mover(dt)
        
        # Limitar al mapa
        self.limitar_al_mapa()
        
        # Actualizar invulnerabilidad
        self.actualizar_invulnerabilidad(dt)
        
        # Actualizar tiempo de supervivencia
        self.tiempo_supervivencia += dt