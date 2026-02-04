"""
ENGINE.PY - MOTOR PRINCIPAL DEL JUEGO
======================================
Clase principal que orquesta todos los sistemas del juego
"""

import pygame
import sys
from constants import GameState
from settings import *
from entities.player import Player
from entities.weapon import Weapon
from entities.enemy import TerrereItem
from World.map import Map
from World.camera import Camera
from managers.spawn_manager import SpawnManager
from managers.combat_manager import CombatManager
from managers.ui_manager import UIManager
from asset_.asset_loader import AssetLoader


class GameEngine:
    """Motor principal del juego - Orquesta todos los sistemas"""
    
    def __init__(self):
        """Inicializar motor del juego"""
        # Inicializar Pygame
        pygame.init()
        pygame.mixer.init()
        
        # Crear ventana
        self.pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        pygame.display.set_caption(TITULO_JUEGO)
        
        # Reloj para controlar FPS
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.fps_actual = 60
        
        # Estado del juego
        self.estado = GameState.MENU
        self.corriendo = True
        self.juego_pausado = False
        
        # Cargar assets
        print("Cargando assets...")
        self.assets = AssetLoader()

        # Reproducir música del menú al iniciar
        self.assets.reproducir_musica("menu", volumen=0.2)

        # Sistemas del juego (se inicializan después)
        self.mapa = None
        self.jugador = None
        self.camara = None
        self.spawn_manager = None
        self.combat_manager = None
        self.ui_manager = None
        
        # Sistema de items (tereres)
        self.tereres = []
        self.timer_spawn_terere = 0
        self.intervalo_spawn_terere = 25.0  # cada 15 segundos
        
        # Estadísticas de sesión
        self.tiempo_total_juego = 0
        self.partidas_jugadas = 0
        
        # Nivel anterior para detectar subida
        self.nivel_anterior = 1
    
    def inicializar_juego_nuevo(self):
        """Inicializar una nueva partida"""
        print("Iniciando nueva partida...")
        
        # Crear mapa
        self.mapa = Map()
        
        # Crear jugador en el centro del mapa
        pos_inicial_x = MAPA_ANCHO_PIXELES // 2
        pos_inicial_y = MAPA_ALTO_PIXELES // 2
        self.jugador = Player(pos_inicial_x, pos_inicial_y, self.assets)
        
        # Equipar machete inicial
        machete = Weapon("MACHETE", self.jugador, self.assets)
        self.jugador.armas_equipadas.append(machete)
        
        # Crear cámara
        self.camara = Camera(ANCHO_VENTANA, ALTO_VENTANA)
        self.camara.establecer_target(self.jugador)
        self.camara.centrar_en(pos_inicial_x, pos_inicial_y)
        
        # Crear spawn manager
        self.spawn_manager = SpawnManager(self.mapa, self.camara, self.jugador)

        # Crear combat manager
        self.combat_manager = CombatManager(self.jugador, self.spawn_manager)

        # Asignar combat_manager al spawn_manager para que pueda crear orbes
        self.spawn_manager.combat_manager = self.combat_manager
        
        # Crear UI manager
        self.ui_manager = UIManager(self.pantalla, self.jugador)
        
        # Reproducir música de gameplay
        self.assets.reproducir_musica("gameplay", volumen=0.3)
        
        # Incrementar contador de partidas
        self.partidas_jugadas += 1
        
        # Resetear nivel anterior
        self.nivel_anterior = 1
        
        print("Partida iniciada correctamente")
    
    def reiniciar_juego(self):
        """Reiniciar el juego (después de Game Over)"""
        # Limpiar sistemas existentes
        if self.spawn_manager:
            self.spawn_manager.enemigos.clear()
        if self.combat_manager:
            self.combat_manager.orbes_xp.clear()
            self.combat_manager.efectos.clear()
        
        # Inicializar nueva partida
        self.inicializar_juego_nuevo()
        
        # Cambiar estado
        self.estado = GameState.JUGANDO
    
    def run(self):
        """Loop principal del juego"""
        while self.corriendo:
            # Calcular delta time
            self.dt = self.clock.tick(FPS) / 1000.0
            self.fps_actual = self.clock.get_fps()
            
            # Actualizar tiempo total
            self.tiempo_total_juego += self.dt
            
            # Manejar eventos
            self.manejar_eventos()
            
            # Actualizar según estado
            self.actualizar()
            
            # Dibujar según estado
            self.dibujar()
            
            # Actualizar pantalla
            pygame.display.flip()
        
        # Limpiar y salir
        self.limpiar()
        pygame.quit()
        sys.exit()
    
    def manejar_eventos(self):
        """Procesar eventos de Pygame"""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.corriendo = False
            
            if evento.type == pygame.KEYDOWN:
                self.manejar_tecla_presionada(evento.key)
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                self.manejar_click_mouse(evento.pos, evento.button)
    
    def manejar_tecla_presionada(self, tecla):
        """
        Manejar teclas presionadas según estado del juego
        
        Args:
            tecla: Código de la tecla presionada
        """
        # MENÚ
        if self.estado == GameState.MENU:
            if tecla == pygame.K_SPACE or tecla == pygame.K_RETURN:
                self.inicializar_juego_nuevo()
                self.estado = GameState.JUGANDO
            if tecla == pygame.K_ESCAPE:
                self.corriendo = False
        
        # JUGANDO
        elif self.estado == GameState.JUGANDO:
            if tecla == pygame.K_ESCAPE:
                self.pausar_juego()
            
            # Atacar con machete al presionar ESPACIO
            if tecla == pygame.K_SPACE:
                for arma in self.jugador.armas_equipadas:
                    if arma.tipo == "MACHETE" and arma.puede_usar:
                        arma.usar(self.spawn_manager.enemigos)
                        break
            
            # Debug: teclas especiales
            if DEBUG_MODE:
                if tecla == pygame.K_F1:
                    self.jugador.ganar_xp(100)
                if tecla == pygame.K_F3:
                    self.jugador.vida_actual = self.jugador.vida_maxima
        
        # PAUSA
        elif self.estado == GameState.PAUSA:
            if tecla == pygame.K_ESCAPE:
                self.reanudar_juego()
            if tecla == pygame.K_q:
                self.volver_al_menu()
        
        # MEJORA
        elif self.estado == GameState.MEJORA:
            pass
        
        # GAME OVER
        elif self.estado == GameState.GAME_OVER:
            if tecla == pygame.K_SPACE:
                self.reiniciar_juego()
            if tecla == pygame.K_ESCAPE:
                self.volver_al_menu()
    
    def manejar_click_mouse(self, pos, boton):
        """
        Manejar clicks del mouse
        
        Args:
            pos: Tupla (x, y) con posición del click
            boton: Botón del mouse
        """
        if boton != 1: 
            return
        
        # MEJORA - Seleccionar mejora
        if self.estado == GameState.MEJORA:
            if self.ui_manager.mostrar_pantalla_mejora:
                indice = self.ui_manager.manejar_click_mejora(
                    pos, 
                    self.ui_manager.opciones_mejora
                )
                
                if indice is not None:
                    opcion = self.ui_manager.opciones_mejora[indice]
                    self.aplicar_mejora_seleccionada(opcion)
                    
                    self.ui_manager.mostrar_pantalla_mejora = False
                    self.jugador.subio_nivel = False
                    self.estado = GameState.JUGANDO
        
        
        # MENÚ - Click en el botón INICIAR JUEGO 
        if self.estado == GameState.MENU:
            boton_ancho = 300
            boton_alto = 65
            boton_x = ANCHO_VENTANA // 2 - boton_ancho // 2
            boton_y = ALTO_VENTANA - 220 
            
            if boton_x <= pos[0] <= boton_x + boton_ancho and boton_y <= pos[1] <= boton_y + boton_alto:
                self.inicializar_juego_nuevo()
                self.estado = GameState.JUGANDO
    
    def aplicar_mejora_seleccionada(self, opcion):
        """
        Aplicar la mejora que el jugador seleccionó
        
        Args:
            opcion: Diccionario con la opción de mejora
        """
        tipo = opcion["tipo"]
        valor = opcion["valor"]
        
        self.jugador.aplicar_mejora(tipo, valor)
        
        if tipo == "nueva_arma":
            nueva_arma = Weapon(valor, self.jugador, self.assets)
            self.jugador.armas_equipadas.append(nueva_arma)
    
    def actualizar(self):
        """Actualizar lógica según estado del juego"""
        if self.estado == GameState.MENU:
            self.actualizar_menu()
        
        elif self.estado == GameState.JUGANDO:
            self.actualizar_juego()
        
        elif self.estado == GameState.PAUSA:
            pass
        
        elif self.estado == GameState.MEJORA:
            pass
        
        elif self.estado == GameState.GAME_OVER:
            pass
    
    def actualizar_menu(self):
        """Actualizar lógica del menú"""
        pass
    
    def actualizar_juego(self):
        """Actualizar toda la lógica del juego"""
        self.jugador.actualizar(self.dt)
        self.jugador.actualizar_armas(self.dt, self.spawn_manager.enemigos)
        self.camara.actualizar(self.dt)
        self.spawn_manager.actualizar(self.dt)

        self.combat_manager.actualizar(self.dt)
        self.ui_manager.actualizar(self.dt)
        
        # Actualizar sistema de tereres
        self.actualizar_tereres(self.dt)
        
        # Verificar si el jugador murió
        if not self.jugador.esta_vivo:
            self.game_over()
        
        # Verificar si debe mostrar pantalla de mejora
        if self.jugador.subio_nivel:
            self.mostrar_pantalla_mejora()
    
    def dibujar(self):
        """Dibujar según estado del juego"""
        if self.estado == GameState.MENU:
            self.dibujar_menu()
        
        elif self.estado == GameState.JUGANDO:
            self.dibujar_juego()
        
        elif self.estado == GameState.PAUSA:
            self.dibujar_juego()
            self.ui_manager.dibujar_menu_pausa()
        
        elif self.estado == GameState.MEJORA:
            self.dibujar_juego()
            self.ui_manager.dibujar_pantalla_mejora(self.ui_manager.opciones_mejora)
        
        elif self.estado == GameState.GAME_OVER:
            self.dibujar_juego()
            self.ui_manager.dibujar_game_over()
    
    def dibujar_menu(self):
        """Dibujar pantalla de menú - solo imagen de fondo y boton"""
        # Cargar fondo
        try:
            fondo = pygame.image.load("assets/sprites/fondo_karai.jpeg")
            fondo = pygame.transform.scale(fondo, (ANCHO_VENTANA, ALTO_VENTANA))
            self.pantalla.blit(fondo, (0, 0))
        except:
            self.pantalla.fill((0, 0, 0))
        
        # ========== BOTÓN ESTILO ORIGINAL ==========
        boton_ancho = 300
        boton_alto = 65
        boton_x = ANCHO_VENTANA // 2 - boton_ancho // 2
        boton_y = ALTO_VENTANA - 220  # Más abajo
        
        # Detectar hover
        pos_mouse = pygame.mouse.get_pos()
        hover = (boton_x <= pos_mouse[0] <= boton_x + boton_ancho and 
                boton_y <= pos_mouse[1] <= boton_y + boton_alto)
        
        # Sombra del botón
        pygame.draw.rect(self.pantalla, (0, 0, 0), 
                        (boton_x + 4, boton_y + 4, boton_ancho, boton_alto), 
                        border_radius=8)
        
        # Fondo principal del botón (madera oscura)
        color_fondo = (90, 55, 20) if hover else (70, 40, 15)
        pygame.draw.rect(self.pantalla, color_fondo, 
                        (boton_x, boton_y, boton_ancho, boton_alto), 
                        border_radius=8)
        
        # Borde exterior grueso (madera)
        pygame.draw.rect(self.pantalla, (50, 30, 10), 
                        (boton_x, boton_y, boton_ancho, boton_alto), 
                        4, border_radius=8)
        
        # Borde interior dorado
        pygame.draw.rect(self.pantalla, (200, 160, 50), 
                        (boton_x + 6, boton_y + 6, boton_ancho - 12, boton_alto - 12), 
                        2, border_radius=5)
        
        # Línea horizontal decorativa arriba
        pygame.draw.line(self.pantalla, (200, 160, 50), 
                        (boton_x + 15, boton_y + 12), 
                        (boton_x + boton_ancho - 15, boton_y + 12), 2)
        
        # Línea horizontal decorativa abajo
        pygame.draw.line(self.pantalla, (200, 160, 50), 
                        (boton_x + 15, boton_y + boton_alto - 12), 
                        (boton_x + boton_ancho - 15, boton_y + boton_alto - 12), 2)
        
        # ===== FLECHA IZQUIERDA (roja) =====
        flecha_izq_x = boton_x + 18
        flecha_izq_y = boton_y + boton_alto // 2
        flecha_color = (220, 50, 30) if hover else (180, 40, 20)
        
        # Triángulo izquierdo
        puntos_izq = [
            (flecha_izq_x, flecha_izq_y),                    # Punta izquierda
            (flecha_izq_x + 18, flecha_izq_y - 12),          # Arriba derecha
            (flecha_izq_x + 18, flecha_izq_y + 12)           # Abajo derecha
        ]
        pygame.draw.polygon(self.pantalla, flecha_color, puntos_izq)
        pygame.draw.polygon(self.pantalla, (255, 100, 60), puntos_izq, 2)
        
        # ===== FLECHA DERECHA (roja) =====
        flecha_der_x = boton_x + boton_ancho - 18
        flecha_der_y = boton_y + boton_alto // 2
        
        # Triángulo derecho
        puntos_der = [
            (flecha_der_x, flecha_der_y),                    # Punta derecha
            (flecha_der_x - 18, flecha_der_y - 12),          # Arriba izquierda
            (flecha_der_x - 18, flecha_der_y + 12)           # Abajo izquierda
        ]
        pygame.draw.polygon(self.pantalla, flecha_color, puntos_der)
        pygame.draw.polygon(self.pantalla, (255, 100, 60), puntos_der, 2)
        
        # ===== TEXTO "► INICIAR JUEGO" =====
        fuente_boton = pygame.font.Font(None, 40)
        
        # Sombra del texto
        texto_sombra = fuente_boton.render("INICIAR JUEGO", True, (0, 0, 0))
        rect_sombra = texto_sombra.get_rect()
        rect_sombra.center = (ANCHO_VENTANA // 2 + 2, boton_y + boton_alto // 2 + 2)
        self.pantalla.blit(texto_sombra, rect_sombra)
        
        # Texto principal (brillo si hover)
        color_texto = (255, 240, 180) if hover else (240, 220, 160)
        texto_boton = fuente_boton.render("INICIAR JUEGO", True, color_texto)
        rect_boton = texto_boton.get_rect()
        rect_boton.center = (ANCHO_VENTANA // 2, boton_y + boton_alto // 2)
        self.pantalla.blit(texto_boton, rect_boton)
        
        # ===== PEQUEÑO TEXTO "Presiona ESPACIO" debajo =====
        fuente_pequeña = pygame.font.Font(None, 22)
        
        # Sombra
        esp_sombra = fuente_pequeña.render("o presiona ESPACIO para comenzar", True, (0, 0, 0))
        rect_esp_sombra = esp_sombra.get_rect()
        rect_esp_sombra.center = (ANCHO_VENTANA // 2 + 1, boton_y + boton_alto + 22)
        self.pantalla.blit(esp_sombra, rect_esp_sombra)
        
        # Texto
        esp_texto = fuente_pequeña.render("o presiona ESPACIO para comenzar", True, (200, 200, 200))
        rect_esp = esp_texto.get_rect()
        rect_esp.center = (ANCHO_VENTANA // 2, boton_y + boton_alto + 21)
        self.pantalla.blit(esp_texto, rect_esp)
    
    def dibujar_juego(self):
        """Dibujar todo el juego"""
        self.pantalla.fill(COLOR_FONDO)
        self.mapa.dibujar(self.pantalla, self.camara)
        self.combat_manager.dibujar(self.pantalla, self.camara)
        self.spawn_manager.dibujar(self.pantalla, self.camara)
        
        # Dibujar tereres
        for terere in self.tereres:
            terere.dibujar(self.pantalla, self.camara)
        
        self.jugador.dibujar(self.pantalla, self.camara)
        self.ui_manager.dibujar_hud()
        
        if MOSTRAR_FPS:
            self.dibujar_fps()
    
    def dibujar_fps(self):
        """Dibujar contador de FPS"""
        fuente = pygame.font.Font(None, 24)
        fps_texto = f"FPS: {int(self.fps_actual)}"
        superficie = fuente.render(fps_texto, True, (0, 255, 0))
        self.pantalla.blit(superficie, (10, ALTO_VENTANA - 30))
    
    def pausar_juego(self):
        """Pausar el juego"""
        self.estado = GameState.PAUSA
        self.juego_pausado = True
        self.assets.pausar_musica()
    
    def reanudar_juego(self):
        """Reanudar el juego"""
        self.estado = GameState.JUGANDO
        self.juego_pausado = False
        self.assets.reanudar_musica()
    
    def mostrar_pantalla_mejora(self):
        """Mostrar pantalla de selección de mejoras"""
        self.estado = GameState.MEJORA
        opciones = self.jugador.generar_opciones_mejora()
        self.ui_manager.opciones_mejora = opciones
        self.ui_manager.mostrar_pantalla_mejora = True
        pygame.mixer.music.set_volume(0.1)
    
    def actualizar_tereres(self, dt):
        """
        Actualizar sistema de tereres
        
        Args:
            dt: Delta time en segundos
        """
        # Incrementar timer de spawn
        self.timer_spawn_terere += dt
        
        # Spawnear nuevo terere si es tiempo
        if self.timer_spawn_terere >= self.intervalo_spawn_terere:
            self.spawnear_terere()
            self.timer_spawn_terere = 0
        
        # Actualizar tereres
        for terere in self.tereres[:]:
            terere.actualizar(dt)
            
            # Verificar colisión con jugador
            if self.jugador.rect.colliderect(terere.rect):
                self.jugador.aplicar_buff_terere()
                self.tereres.remove(terere)
    
    def spawnear_terere(self):
        """Spawnear un terere en posición aleatoria"""
        import random
        
        # Posición aleatoria en el mapa
        x = random.uniform(100, MAPA_ANCHO_PIXELES - 100)
        y = random.uniform(100, MAPA_ALTO_PIXELES - 100)
        
        terere = TerrereItem(x, y)
        self.tereres.append(terere)
    
    def game_over(self):
        """Manejar Game Over"""
        self.estado = GameState.GAME_OVER
        self.assets.detener_musica()
        self.assets.reproducir_sonido("game_over")
        print(f"GAME OVER - Nivel: {self.jugador.nivel}, Tiempo: {int(self.jugador.tiempo_supervivencia)}s")
    
    def volver_al_menu(self):
        """Volver al menú principal"""
        self.estado = GameState.MENU
        self.assets.detener_musica()
        self.assets.reproducir_musica("menu", volumen=0.3)
        self.limpiar_partida()
    
    def limpiar_partida(self):
        """Limpiar datos de la partida actual"""
        if self.spawn_manager:
            self.spawn_manager.enemigos.clear()
        if self.combat_manager:
            self.combat_manager.orbes_xp.clear()
            self.combat_manager.efectos.clear()
        
        self.tereres.clear()
        
        self.mapa = None
        self.jugador = None
        self.camara = None
        self.spawn_manager = None
        self.combat_manager = None
    
    def limpiar(self):
        """Limpiar recursos antes de salir"""
        self.assets.detener_musica()
        pygame.mixer.stop()
        self.assets.limpiar()
        print("Recursos limpiados. Saliendo...")