"""
PLAYER.PY - LÓGICA DEL CAMPESINO
=================================
Control del jugador, stats, nivel y armas
"""

import pygame
from base_entity import BaseEntity
from src.settings import *

class Player(BaseEntity):
    '''
    """
    PSEUDOCÓDIGO:
    
    __init__(self, x, y):
        # Llamar constructor padre
        super().__init__(x, y, 50, 50, (255, 200, 0))  # Amarillo campesino
        
        # Stats del campesino
        self.vida_maxima = CAMPESINO_VIDA_MAX
        self.vida_actual = CAMPESINO_VIDA_MAX
        self.velocidad = CAMPESINO_VELOCIDAD
        
        # Sistema de experiencia y nivel
        self.nivel = 1
        self.xp_actual = 0
        self.xp_necesaria = XP_POR_NIVEL[0]
        
        # Inventario de armas
        self.armas_equipadas = []  # Lista de instancias de Weapon
        self.armas_disponibles = ["MACHETE"]  # Empieza con machete
        
        # Radio de recolección de XP
        self.radio_recoleccion = CAMPESINO_RADIO_RECOLECCION
        
        # Cooldown de invulnerabilidad al recibir daño
        self.invulnerable = False
        self.tiempo_invulnerabilidad = 0
        self.duracion_invulnerabilidad = 0.5  # segundos
        
        # Stats de juego
        self.enemigos_matados = 0
        self.tiempo_supervivencia = 0
    
    
    def manejar_input(self):
        """
        Procesar input del teclado para movimiento
        
        PSEUDOCÓDIGO:
        teclas = pygame.key.get_pressed()
        
        # Resetear dirección
        self.direccion.x = 0
        self.direccion.y = 0
        
        # Movimiento WASD o flechas
        SI teclas[K_w] O teclas[K_UP]:
            self.direccion.y = -1
        SI teclas[K_s] O teclas[K_DOWN]:
            self.direccion.y = 1
        SI teclas[K_a] O teclas[K_LEFT]:
            self.direccion.x = -1
        SI teclas[K_d] O teclas[K_RIGHT]:
            self.direccion.x = 1
        """
        pass
    
    
    def ganar_xp(self, cantidad):
        """
        Sumar XP y verificar subida de nivel
        
        PSEUDOCÓDIGO:
        self.xp_actual += cantidad
        
        # Verificar subida de nivel
        MIENTRAS self.xp_actual >= self.xp_necesaria:
            self.subir_nivel()
        """
        pass
    
    
    def subir_nivel(self):
        """
        Aumentar nivel y ofrecer mejora
        
        PSEUDOCÓDIGO:
        # Restar XP usada
        self.xp_actual -= self.xp_necesaria
        self.nivel += 1
        
        # Calcular nueva XP necesaria
        SI self.nivel <= len(XP_POR_NIVEL):
            self.xp_necesaria = XP_POR_NIVEL[self.nivel - 1]
        SINO:
            # Fórmula exponencial para niveles altos
            self.xp_necesaria = int(XP_POR_NIVEL[-1] * (1.5 ** (self.nivel - 10)))
        
        # Curación completa al subir nivel
        self.vida_actual = self.vida_maxima
        
        # PAUSAR JUEGO y mostrar pantalla de mejoras
        self.mostrar_pantalla_mejoras()
        """
        pass
    
    
    def mostrar_pantalla_mejoras(self):
        """
        Mostrar 3 opciones aleatorias de mejora
        
        PSEUDOCÓDIGO:
        opciones_disponibles = []
        
        # Opción 1: Nueva arma (si hay disponibles)
        PARA CADA arma EN ARMAS_CONFIG:
            SI arma NO está en self.armas_equipadas:
                opciones_disponibles.agregar(("nueva_arma", arma))
        
        # Opción 2: Mejorar arma existente
        PARA CADA arma EN self.armas_equipadas:
            SI arma.nivel < arma.nivel_maximo:
                opciones_disponibles.agregar(("mejorar_arma", arma))
        
        # Opción 3: Mejoras pasivas (vida, velocidad, etc)
        opciones_disponibles.agregar(("aumentar_vida_max", 20))
        opciones_disponibles.agregar(("aumentar_velocidad", 20))
        opciones_disponibles.agregar(("aumentar_radio_recoleccion", 20))
        
        # Elegir 3 opciones aleatorias
        opciones_mostrar = random.sample(opciones_disponibles, 3)
        
        # Esperar elección del jugador (UI_Manager se encarga)
        # Cuando elige, aplicar mejora correspondiente
        """
        pass
    
    
    def aplicar_mejora(self, tipo_mejora, valor):
        """
        Aplicar la mejora elegida
        
        PSEUDOCÓDIGO:
        SI tipo_mejora == "nueva_arma":
            nueva_arma = Weapon(valor, self)  # valor es el nombre del arma
            self.armas_equipadas.agregar(nueva_arma)
        
        SI tipo_mejora == "mejorar_arma":
            valor.subir_nivel()  # valor es la instancia del arma
        
        SI tipo_mejora == "aumentar_vida_max":
            self.vida_maxima += valor
            self.vida_actual += valor  # También cura
        
        SI tipo_mejora == "aumentar_velocidad":
            self.velocidad += valor
        
        SI tipo_mejora == "aumentar_radio_recoleccion":
            self.radio_recoleccion += valor
        """
        pass
    
    
    def recibir_daño(self, cantidad):
        """
        Sobrescribir para incluir invulnerabilidad
        
        PSEUDOCÓDIGO:
        SI NO self.invulnerable:
            super().recibir_daño(cantidad)
            
            # Activar invulnerabilidad temporal
            self.invulnerable = True
            self.tiempo_invulnerabilidad = 0
            
            # Efecto visual (parpadeo)
            # Se maneja en el método dibujar
        """
        pass
    
    
    def actualizar_invulnerabilidad(self, dt):
        """
        Actualizar timer de invulnerabilidad
        
        PSEUDOCÓDIGO:
        SI self.invulnerable:
            self.tiempo_invulnerabilidad += dt
            
            SI self.tiempo_invulnerabilidad >= self.duracion_invulnerabilidad:
                self.invulnerable = False
                self.tiempo_invulnerabilidad = 0
        """
        pass
    
    
    def actualizar_armas(self, dt, enemigos):
        """
        Actualizar todas las armas equipadas
        
        PSEUDOCÓDIGO:
        PARA CADA arma EN self.armas_equipadas:
            arma.actualizar(dt, enemigos)
        """
        pass
    
    
    def recolectar_xp_cercana(self, orbes_xp):
        """
        Atraer y recolectar orbes de XP cercanas
        
        PSEUDOCÓDIGO:
        PARA CADA orbe EN orbes_xp:
            distancia = self.distancia_a(orbe)
            
            SI distancia <= self.radio_recoleccion:
                # Atraer orbe hacia jugador
                direccion = orbe.direccion_hacia(self)
                orbe.x += direccion.x * 300 * dt  # Velocidad de atracción
                orbe.y += direccion.y * 300 * dt
                
                # SI toca al jugador, recolectar
                SI self.colisiona_con(orbe):
                    self.ganar_xp(orbe.cantidad)
                    orbes_xp.remove(orbe)
        """
        pass
    
    
    def limitar_al_mapa(self):
        """
        No permitir que salga del mapa
        
        PSEUDOCÓDIGO:
        SI self.x < 0:
            self.x = 0
        SI self.x > MAPA_ANCHO_PIXELES:
            self.x = MAPA_ANCHO_PIXELES
        SI self.y < 0:
            self.y = 0
        SI self.y > MAPA_ALTO_PIXELES:
            self.y = MAPA_ALTO_PIXELES
        
        # Actualizar rect
        self.rect.center = (int(self.x), int(self.y))
        """
        pass
    
    
    def al_morir(self):
        """
        Callback cuando muere el jugador
        
        PSEUDOCÓDIGO:
        # Cambiar estado del juego a GAME_OVER
        # Mostrar pantalla de estadísticas finales
        # - Tiempo supervivido
        # - Nivel alcanzado
        # - Enemigos matados
        """
        pass
    
    
    def dibujar(self, pantalla, camara):
        """
        Dibujar con efecto de parpadeo si es invulnerable
        
        PSEUDOCÓDIGO:
        SI self.invulnerable:
            # Parpadear cada 0.1 segundos
            SI int(self.tiempo_invulnerabilidad * 10) % 2 == 0:
                super().dibujar(pantalla, camara)
        SINO:
            super().dibujar(pantalla, camara)
        """
        pass
    
    
    def actualizar(self, dt):
        """
        Actualización principal del jugador
        
        PSEUDOCÓDIGO:
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
        """
        pass
        '''