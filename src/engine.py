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
        
        # Sistemas del juego (se inicializan después)
        self.mapa = None
        self.jugador = None
        self.camara = None
        self.spawn_manager = None
        self.combat_manager = None
        self.ui_manager = None
        
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
        self.jugador = Player(pos_inicial_x, pos_inicial_y)
        
        # Equipar machete inicial
        machete = Weapon("MACHETE", self.jugador)
        self.jugador.armas_equipadas.append(machete)
        
        # Crear cámara
        self.camara = Camera(ANCHO_VENTANA, ALTO_VENTANA)
        self.camara.establecer_target(self.jugador)
        self.camara.centrar_en(pos_inicial_x, pos_inicial_y)
        
        # Crear spawn manager
        self.spawn_manager = SpawnManager(self.mapa, self.camara, self.jugador)
        
        # Crear combat manager
        self.combat_manager = CombatManager(self.jugador, self.spawn_manager)
        
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
            self.dt = self.clock.tick(FPS) / 1000.0  # Convertir ms a segundos
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
            
            # Eventos de teclado
            if evento.type == pygame.KEYDOWN:
                self.manejar_tecla_presionada(evento.key)
            
            # Eventos de mouse
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
            
            # Debug: teclas especiales
            if DEBUG_MODE:
                if tecla == pygame.K_F1:
                    self.jugador.ganar_xp(100)  # XP instantánea
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
            # Las mejoras se manejan con clicks de mouse
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
            boton: Botón del mouse (1=izquierdo, 2=medio, 3=derecho)
        """
        # Solo procesar click izquierdo
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
                    # Aplicar mejora seleccionada
                    opcion = self.ui_manager.opciones_mejora[indice]
                    self.aplicar_mejora_seleccionada(opcion)
                    
                    # Cerrar pantalla de mejora y reanudar juego
                    self.ui_manager.mostrar_pantalla_mejora = False
                    self.jugador.subio_nivel = False
                    self.estado = GameState.JUGANDO
    
    def aplicar_mejora_seleccionada(self, opcion):
        """
        Aplicar la mejora que el jugador seleccionó
        
        Args:
            opcion: Diccionario con la opción de mejora
        """
        tipo = opcion["tipo"]
        valor = opcion["valor"]
        
        # Aplicar mejora al jugador
        self.jugador.aplicar_mejora(tipo, valor)
        
        # Si es nueva arma, equiparla
        if tipo == "nueva_arma":
            nueva_arma = Weapon(valor, self.jugador)
            self.jugador.armas_equipadas.append(nueva_arma)
    
    def actualizar(self):
        """Actualizar lógica según estado del juego"""
        if self.estado == GameState.MENU:
            self.actualizar_menu()
        
        elif self.estado == GameState.JUGANDO:
            self.actualizar_juego()
        
        elif self.estado == GameState.PAUSA:
            # No actualizar nada en pausa
            pass
        
        elif self.estado == GameState.MEJORA:
            # No actualizar juego, solo esperar selección
            pass
        
        elif self.estado == GameState.GAME_OVER:
            # No actualizar juego
            pass
    
    def actualizar_menu(self):
        """Actualizar lógica del menú"""
        # Animaciones del menú (opcional)
        pass
    
    def actualizar_juego(self):
        """Actualizar toda la lógica del juego"""
        # Actualizar jugador
        self.jugador.actualizar(self.dt)
        
        # Actualizar armas del jugador
        self.jugador.actualizar_armas(self.dt, self.spawn_manager.enemigos)
        
        # Actualizar cámara
        self.camara.actualizar(self.dt)
        
        # Actualizar spawn de enemigos
        self.spawn_manager.actualizar(self.dt)
        
        # Verificar enemigos muertos y crear orbes XP
        for enemigo in self.spawn_manager.enemigos:
            if not enemigo.esta_vivo and enemigo not in self.combat_manager.orbes_xp:
                self.combat_manager.verificar_muerte_enemigo(enemigo)
        
        # Actualizar sistema de combate
        self.combat_manager.actualizar(self.dt)
        
        # Actualizar UI
        self.ui_manager.actualizar(self.dt)
        
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
            self.dibujar_juego()  # Dibujar juego congelado
            self.ui_manager.dibujar_menu_pausa()
        
        elif self.estado == GameState.MEJORA:
            self.dibujar_juego()  # Dibujar juego de fondo
            self.ui_manager.dibujar_pantalla_mejora(self.ui_manager.opciones_mejora)
        
        elif self.estado == GameState.GAME_OVER:
            self.dibujar_juego()  # Mostrar último frame
            self.ui_manager.dibujar_game_over()
    
    def dibujar_menu(self):
        """Dibujar pantalla de menú"""
        # Fondo negro
        self.pantalla.fill((0, 0, 0))
        
        # Crear fuentes temporales para el menú
        fuente_grande = pygame.font.Font(None, 48)
        fuente_media = pygame.font.Font(None, 32)
        fuente_pequeña = pygame.font.Font(None, 24)
        self.assets.reproducir_musica("menu_theme")
        # Título del juego
        titulo = fuente_grande.render("KARAI SURVIVAL", True, COLOR_XP)
        rect = titulo.get_rect()
        rect.center = (ANCHO_VENTANA // 2, 150)
        self.pantalla.blit(titulo, rect)
        
        # Instrucciones
        instrucciones = [
            "Usa WASD o Flechas para moverte",
            "Las armas atacan automáticamente",
            "Recolecta XP para subir de nivel",
            "¡Sobrevive el mayor tiempo posible!",
            "",
            "Presiona ESPACIO para comenzar"
        ]
        
        y_offset = 300
        for linea in instrucciones:
            texto = fuente_pequeña.render(linea, True, COLOR_TEXTO)
            rect = texto.get_rect()
            rect.center = (ANCHO_VENTANA // 2, y_offset)
            self.pantalla.blit(texto, rect)
            y_offset += 35
       
        self.assets.reproducir_musica("menu_theme")
    def dibujar_juego(self):
        """Dibujar todo el juego"""
        # Limpiar pantalla
        self.pantalla.fill(COLOR_FONDO)
        
        # Dibujar mapa
        self.mapa.dibujar(self.pantalla, self.camara)
        
        # Dibujar orbes de XP y efectos
        self.combat_manager.dibujar(self.pantalla, self.camara)
        
        # Dibujar enemigos
        self.spawn_manager.dibujar(self.pantalla, self.camara)
        
        # Dibujar jugador
        self.jugador.dibujar(self.pantalla, self.camara)
        
        # Dibujar HUD
        self.ui_manager.dibujar_hud()
        
        # Dibujar FPS si está activado
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
        # Cambiar estado
        self.estado = GameState.MEJORA
        
        # Generar opciones de mejora
        opciones = self.jugador.generar_opciones_mejora()
        self.ui_manager.opciones_mejora = opciones
        self.ui_manager.mostrar_pantalla_mejora = True
        
        # Reducir volumen de música
        pygame.mixer.music.set_volume(0.1)
    
    def game_over(self):
        """Manejar Game Over"""
        # Cambiar estado
        self.estado = GameState.GAME_OVER
        
        # Detener música de gameplay
        self.assets.detener_musica()
        
        # Reproducir música/sonido de game over
        self.assets.reproducir_sonido("game_over")
        
        print(f"GAME OVER - Nivel: {self.jugador.nivel}, Tiempo: {int(self.jugador.tiempo_supervivencia)}s")
    
    def volver_al_menu(self):
        """Volver al menú principal"""
        # Cambiar estado
        self.estado = GameState.MENU
        
        # Detener música actual
        self.assets.detener_musica()
        
        # Limpiar sistemas de juego
        self.limpiar_partida()
    
    def limpiar_partida(self):
        """Limpiar datos de la partida actual"""
        if self.spawn_manager:
            self.spawn_manager.enemigos.clear()
        
        if self.combat_manager:
            self.combat_manager.orbes_xp.clear()
            self.combat_manager.efectos.clear()
        
        # Resetear referencias
        self.mapa = None
        self.jugador = None
        self.camara = None
        self.spawn_manager = None
        self.combat_manager = None
    
    def limpiar(self):
        """Limpiar recursos antes de salir"""
        # Detener todos los sonidos
        self.assets.detener_musica()
        pygame.mixer.stop()
        
        # Limpiar assets
        self.assets.limpiar()
        
        print("Recursos limpiados. Saliendo...")