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

    def __init__(self, x, y, assets=None):
        """
        Inicializar jugador

        Args:
            x: Posición X inicial
            y: Posición Y inicial
            assets: Referencia al AssetLoader para sonidos
        """
        # Llamar constructor padre con sprite - Tamaño más grande
        super().__init__(x, y, 70, 160, (255, 200, 0), sprite_path="assets/sprites/player_frame1.png")

        # Referencia a assets para sonidos
        self.assets = assets

        # Sistema de animación con 2 frames
        self.frames_animacion = []
        self.cargar_frames_animacion()
        self.frame_actual = 0
        self.tiempo_animacion = 0
        self.velocidad_animacion = 0.15  # Segundos por frame (ajusta para más rápido/lento)

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
        self.direccion = pygame.math.Vector2(0, 0)

        #Rotacion y flip del sprite segun direccion
        self.imagen_original = self.image.copy()
        self.voltear_horizontalmente = False
        self.ultima_direccion_x = 1  # 1: derecha, -1: izquierda


        # Cooldown de invulnerabilidad al recibir daño
        self.invulnerable = False
        self.tiempo_invulnerabilidad = 0
        self.duracion_invulnerabilidad = INVULNERABILIDAD_DURACION

        # Stats de juego
        self.enemigos_matados = 0
        self.tiempo_supervivencia = 0

        # Flag para subida de nivel
        self.subio_nivel = False

        # Sistema de regeneración (por terere)
        self.regenerando = False
        self.tiempo_regeneracion = 0
        self.duracion_regeneracion = 7.0  # segundos
        self.vida_regenerada_por_segundo = 10

        # Tereré automático cada 25 segundos
        self.tiempo_para_terere = 0
        self.intervalo_terere = 25.0  # segundos

    def cargar_frames_animacion(self):
        """Cargar los 2 frames de animación del jugador"""
        try:
            # Frame 1 - Tamaño más grande (70x160)
            frame1 = pygame.image.load("assets/sprites/karai1.png").convert_alpha()
            frame1 = pygame.transform.scale(frame1, (70, 160))
            self.frames_animacion.append(frame1)

            # Frame 2 - Tamaño más grande (70x160)
            frame2 = pygame.image.load("assets/sprites/karai2.png").convert_alpha()
            frame2 = pygame.transform.scale(frame2, (70, 160))
            self.frames_animacion.append(frame2)

        except:
            # Si falla cargar los frames, usar placeholder
            placeholder = pygame.Surface((70, 160))
            placeholder.fill((255, 200, 0))
            self.frames_animacion.append(placeholder)
            self.frames_animacion.append(placeholder.copy())

    def actualizar_animacion(self, dt):
        """
        Actualizar frame de animación

        Args:
            dt: Delta time en segundos
        """
        # Solo animar si el jugador se está moviendo
        if self.direccion.length() > 0:
            self.tiempo_animacion += dt

            # Cambiar de frame cuando pase el tiempo
            if self.tiempo_animacion >= self.velocidad_animacion:
                self.tiempo_animacion = 0
                self.frame_actual = (self.frame_actual + 1) % len(self.frames_animacion)

                # Actualizar imagen original con el nuevo frame
                self.imagen_original = self.frames_animacion[self.frame_actual]
        else:
            # Si no se mueve, usar frame 0 (idle)
            self.frame_actual = 0
            self.imagen_original = self.frames_animacion[0]

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

    #actualizar direccion visual segun movimiento horizontal
        if self.direccion.x != 0:
            self.ultima_direccion_x = self.direccion.x
            self.voltear_horizontalmente = (self.direccion.x < 0)
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

        # Reproducir sonido de subida de nivel
        if self.assets:
            self.assets.reproducir_sonido("subir_nivel", volumen=0.5)

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
                "titulo": f"Desbloquear {arma}",
                "descripcion": f"Obtén un nuevo arma: {arma}",
                "detalles": f"Tipo: {ARMAS_CONFIG[arma]['tipo'].upper()}",
                "imagen": f"assets/sprites/{arma.lower()}.png"
            })

                # Opción 2: Mejorar arma existente (si puede mejorar)
        for arma in self.armas_equipadas:
            if arma.puede_mejorar():
                nivel_actual = arma.nivel
                nivel_siguiente = nivel_actual + 1

                # Obtener descripción según tipo de arma
                # Usar nivel_siguiente - 1 como índice (0-based indexing)
                if arma.tipo_ataque == "melee":
                    config_siguiente = arma.config["niveles"][nivel_siguiente - 1]
                    daño = config_siguiente.get("daño", 0)
                    alcance = config_siguiente.get("alcance", 0)
                    detalles = f"Daño: {daño} | Alcance: {alcance}"
                elif arma.tipo_ataque == "proyectil":
                    config_siguiente = arma.config["niveles"][nivel_siguiente - 1]
                    daño = config_siguiente.get("daño", 0)
                    cooldown = config_siguiente.get("cooldown", 0)
                    detalles = f"Daño: {daño} | Velocidad: {cooldown:.1f}s"
                elif arma.tipo_ataque == "aoe":
                    config_siguiente = arma.config["niveles"][nivel_siguiente - 1]
                    daño = config_siguiente.get("daño", 0)
                    radio = config_siguiente.get("radio", 0)
                    detalles = f"Daño: {daño} | Radio: {radio}px"
                elif arma.tipo_ataque == "buff":
                    config_siguiente = arma.config["niveles"][nivel_siguiente - 1]
                    vida_seg = config_siguiente.get("vida_por_seg", 0)
                    duracion = config_siguiente.get("duracion", 0)
                    detalles = f"Vida/s: {vida_seg} | Duración: {duracion}s"
                else:
                    detalles = f"Mejora nivel {nivel_siguiente}"

                opciones_disponibles.append({
                    "tipo": "mejorar_arma",
                    "valor": arma,
                    "titulo": f"Mejorar {arma.tipo}",
                    "descripcion": f"Sube a nivel {nivel_siguiente}",
                    "detalles": detalles,
                    "imagen": f"assets/sprites/{arma.tipo.lower()}.png",
                    "nivel_actual": nivel_actual,
                    "nivel_siguiente": nivel_siguiente
                })
        # Opción 3: Mejoras pasivas
        opciones_disponibles.append({
            "tipo": "aumentar_vida_max",
            "valor": MEJORAS_VALORES["vida_max"],
            "titulo": "Aumentar Vida",
            "descripcion": f"+{MEJORAS_VALORES['vida_max']} de Vida Máxima",
            "detalles": "Mejora tu resistencia",
            "imagen": "assets/sprites/health.png"
        })

        opciones_disponibles.append({
            "tipo": "aumentar_velocidad",
            "valor": MEJORAS_VALORES["velocidad"],
            "titulo": "Aumentar Velocidad",
            "descripcion": f"+{MEJORAS_VALORES['velocidad']} de Velocidad",
            "detalles": "Muévete más rápido",
            "imagen": "assets/sprites/speed.png"
        })

        opciones_disponibles.append({
            "tipo": "aumentar_radio_recoleccion",
            "valor": MEJORAS_VALORES["radio_recoleccion"],
            "titulo": "Expandir Radio",
            "descripcion": f"+{MEJORAS_VALORES['radio_recoleccion']}px Radio",
            "detalles": "Recolecta XP desde más lejos",
            "imagen": "assets/sprites/radius.png"
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
        elif tipo_mejora == "mejorar_arma":
            # Mejorar el arma referenciado en 'valor'
            arma = valor
            arma.subir_nivel()
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

                    # Reproducir sonido de recolección
                    if self.assets:
                        self.assets.reproducir_sonido("recolectar_xp", volumen=0.2)

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
        #Aplicar flip horizontal si se voltea
        imagen_actual = pygame.transform.flip(self.imagen_original, self.voltear_horizontalmente, False)
        #Actualizar la imagen del jugador para dibujar
        self.image = imagen_actual
        if self.invulnerable:
            # Parpadear cada 0.1 segundos
            if int(self.tiempo_invulnerabilidad * 10) % 2 == 0:
                super().dibujar(pantalla, camara)
        else:
            super().dibujar(pantalla, camara)

    def aplicar_buff_terere(self):
        """Aplicar buff de regeneración del terere"""
        self.regenerando = True
        self.tiempo_regeneracion = 0

    def actualizar_regeneracion(self, dt):
        """
        Actualizar sistema de regeneración

        Args:
            dt: Delta time en segundos
        """
        if self.regenerando:
            self.tiempo_regeneracion += dt

            # Regenerar vida cada segundo
            vida_a_regenerar = self.vida_regenerada_por_segundo * dt
            self.vida_actual = min(self.vida_actual + vida_a_regenerar, self.vida_maxima)

            # Detener regeneración después de la duración
            if self.tiempo_regeneracion >= self.duracion_regeneracion:
                self.regenerando = False
                self.tiempo_regeneracion = 0

    def actualizar_terere_automatico(self, dt):
        """
        Activar tereré automáticamente cada 25 segundos

        Args:
            dt: Delta time en segundos
        """
        self.tiempo_para_terere += dt

        if self.tiempo_para_terere >= self.intervalo_terere:
            self.tiempo_para_terere = 0
            self.aplicar_buff_terere()

            # Reproducir sonido si está disponible
            if self.assets:
                self.assets.reproducir_sonido("terere", volumen=0.4)

    def actualizar(self, dt):
        """
        Actualización principal del jugador

        Args:
            dt: Delta time en segundos
        """
        # Manejar input
        self.manejar_input()

        # Actualizar animación
        self.actualizar_animacion(dt)

        # Mover
        self.mover(dt)

        # Limitar al mapa
        self.limitar_al_mapa()

        # Actualizar invulnerabilidad
        self.actualizar_invulnerabilidad(dt)

        # Actualizar regeneración
        self.actualizar_regeneracion(dt)

        # Actualizar tereré automático
        self.actualizar_terere_automatico(dt)

        # Actualizar tiempo de supervivencia
        self.tiempo_supervivencia += dt
