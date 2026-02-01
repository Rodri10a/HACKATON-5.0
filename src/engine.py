"""
ENGINE.PY - MOTOR PRINCIPAL DEL JUEGO
======================================
Clase principal que orquesta todos los sistemas del juego
"""
'''
import pygame
import sys
from constants import GameState
from settings import *
from player import Player
from map import Map
from camera import Camera
from spawn_manager import SpawnManager
from combat_manager import CombatManager
from ui_manager import UIManager
from asset_.asset_loader import AssetLoader

class GameEngine:
    """
    PSEUDOCÓDIGO:
    
    __init__(self):
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
    
    
    def inicializar_juego_nuevo(self):
        """
        Inicializar una nueva partida
        
        PSEUDOCÓDIGO:
        # Crear mapa
        self.mapa = Map()
        
        # Crear jugador en el centro del mapa
        pos_inicial_x = MAPA_ANCHO_PIXELES // 2
        pos_inicial_y = MAPA_ALTO_PIXELES // 2
        self.jugador = Player(pos_inicial_x, pos_inicial_y)
        
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
        
        print("Nueva partida iniciada")
        """
        pass
    
    
    def reiniciar_juego(self):
        """
        Reiniciar el juego (después de Game Over)
        
        PSEUDOCÓDIGO:
        # Limpiar sistemas existentes
        SI self.spawn_manager:
            self.spawn_manager.enemigos.clear()
        SI self.combat_manager:
            self.combat_manager.orbes_xp.clear()
            self.combat_manager.efectos.clear()
        
        # Inicializar nueva partida
        self.inicializar_juego_nuevo()
        
        # Cambiar estado
        self.estado = GameState.JUGANDO
        """
        pass
    
    
    def run(self):
        """
        Loop principal del juego
        
        PSEUDOCÓDIGO:
        MIENTRAS self.corriendo:
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
        """
        pass
    
    
    def manejar_eventos(self):
        """
        Procesar eventos de Pygame
        
        PSEUDOCÓDIGO:
        PARA evento EN pygame.event.get():
            SI evento.type == pygame.QUIT:
                self.corriendo = False
            
            # Eventos de teclado
            SI evento.type == pygame.KEYDOWN:
                self.manejar_tecla_presionada(evento.key)
            
            # Eventos de mouse
            SI evento.type == pygame.MOUSEBUTTONDOWN:
                self.manejar_click_mouse(evento.pos, evento.button)
            
            # Eventos de ventana
            SI evento.type == pygame.VIDEORESIZE:
                self.manejar_resize(evento.w, evento.h)
        """
        pass
    
    
    def manejar_tecla_presionada(self, tecla):
        """
        Manejar teclas presionadas según estado del juego
        
        PSEUDOCÓDIGO:
        # MENÚ
        SI self.estado == GameState.MENU:
            SI tecla == pygame.K_SPACE O tecla == pygame.K_RETURN:
                self.inicializar_juego_nuevo()
                self.estado = GameState.JUGANDO
            SI tecla == pygame.K_ESCAPE:
                self.corriendo = False
        
        # JUGANDO
        SI self.estado == GameState.JUGANDO:
            SI tecla == pygame.K_ESCAPE:
                self.pausar_juego()
            
            # Debug: teclas especiales
            SI DEBUG_MODE:
                SI tecla == pygame.K_F1:
                    self.jugador.ganar_xp(100)  # XP instantánea
                SI tecla == pygame.K_F2:
                    self.spawn_manager.spawnear_oleada_boss()
                SI tecla == pygame.K_F3:
                    self.jugador.vida_actual = self.jugador.vida_maxima
        
        # PAUSA
        SI self.estado == GameState.PAUSA:
            SI tecla == pygame.K_ESCAPE:
                self.reanudar_juego()
            SI tecla == pygame.K_q:
                self.volver_al_menu()
        
        # MEJORA
        SI self.estado == GameState.MEJORA:
            # Las mejoras se manejan con clicks de mouse
            pass
        
        # GAME OVER
        SI self.estado == GameState.GAME_OVER:
            SI tecla == pygame.K_SPACE:
                self.reiniciar_juego()
            SI tecla == pygame.K_ESCAPE:
                self.volver_al_menu()
        """
        pass
    
    
    def manejar_click_mouse(self, pos, boton):
        """
        Manejar clicks del mouse
        
        PSEUDOCÓDIGO:
        # Solo procesar click izquierdo
        SI boton != 1:
            RETORNAR
        
        # MEJORA - Seleccionar mejora
        SI self.estado == GameState.MEJORA:
            SI self.ui_manager.mostrar_pantalla_mejora:
                indice = self.ui_manager.manejar_click_mejora(
                    pos, 
                    self.ui_manager.opciones_mejora
                )
                
                SI indice NO es None:
                    # Aplicar mejora seleccionada
                    opcion = self.ui_manager.opciones_mejora[indice]
                    self.jugador.aplicar_mejora(opcion["tipo"], opcion["valor"])
                    
                    # Reproducir sonido
                    self.assets.reproducir_sonido("subir_nivel")
                    
                    # Cerrar pantalla de mejora y reanudar juego
                    self.ui_manager.mostrar_pantalla_mejora = False
                    self.estado = GameState.JUGANDO
        """
        pass
    
    
    def manejar_resize(self, ancho, alto):
        """
        Manejar cambio de tamaño de ventana
        
        PSEUDOCÓDIGO:
        # Actualizar tamaño de pantalla
        self.pantalla = pygame.display.set_mode((ancho, alto), pygame.RESIZABLE)
        
        # Actualizar cámara si existe
        SI self.camara:
            self.camara.ancho = ancho
            self.camara.alto = alto
        
        print(f"Ventana redimensionada a {ancho}x{alto}")
        """
        pass
    
    
    def actualizar(self):
        """
        Actualizar lógica según estado del juego
        
        PSEUDOCÓDIGO:
        SI self.estado == GameState.MENU:
            self.actualizar_menu()
        
        SINO SI self.estado == GameState.JUGANDO:
            self.actualizar_juego()
        
        SINO SI self.estado == GameState.PAUSA:
            # No actualizar nada en pausa
            pass
        
        SINO SI self.estado == GameState.MEJORA:
            # No actualizar juego, solo esperar selección
            pass
        
        SINO SI self.estado == GameState.GAME_OVER:
            # No actualizar juego
            pass
        """
        pass
    
    
    def actualizar_menu(self):
        """
        Actualizar lógica del menú
        
        PSEUDOCÓDIGO:
        # Animaciones del menú (opcional)
        # Por ahora, solo espera input
        pass
        """
        pass
    
    
    def actualizar_juego(self):
        """
        Actualizar toda la lógica del juego
        
        PSEUDOCÓDIGO:
        # Actualizar jugador
        self.jugador.actualizar(self.dt)
        
        # Actualizar armas del jugador
        self.jugador.actualizar_armas(self.dt, self.spawn_manager.enemigos)
        
        # Actualizar cámara
        self.camara.actualizar(self.dt)
        
        # Actualizar spawn de enemigos
        self.spawn_manager.actualizar(self.dt)
        
        # Actualizar sistema de combate
        self.combat_manager.actualizar(self.dt)
        
        # Actualizar UI
        self.ui_manager.actualizar(self.dt)
        
        # Verificar si el jugador murió
        SI NO self.jugador.esta_vivo:
            self.game_over()
        
        # Verificar si debe mostrar pantalla de mejora
        SI self.jugador.nivel > self.nivel_anterior:
            self.mostrar_pantalla_mejora()
            self.nivel_anterior = self.jugador.nivel
        """
        pass
    
    
    def dibujar(self):
        """
        Dibujar según estado del juego
        
        PSEUDOCÓDIGO:
        SI self.estado == GameState.MENU:
            self.dibujar_menu()
        
        SINO SI self.estado == GameState.JUGANDO:
            self.dibujar_juego()
        
        SINO SI self.estado == GameState.PAUSA:
            self.dibujar_juego()  # Dibujar juego congelado
            self.ui_manager.dibujar_menu_pausa()
        
        SINO SI self.estado == GameState.MEJORA:
            self.dibujar_juego()  # Dibujar juego de fondo
            self.ui_manager.dibujar_pantalla_mejora(self.ui_manager.opciones_mejora)
        
        SINO SI self.estado == GameState.GAME_OVER:
            self.dibujar_juego()  # Mostrar último frame
            self.ui_manager.dibujar_game_over()
        """
        pass
    
    
    def dibujar_menu(self):
        """
        Dibujar pantalla de menú
        
        PSEUDOCÓDIGO:
        self.ui_manager.dibujar_pantalla_inicio()
        """
        pass
    
    
    def dibujar_juego(self):
        """
        Dibujar todo el juego
        
        PSEUDOCÓDIGO:
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
        SI MOSTRAR_FPS:
            self.dibujar_fps()
        """
        pass
    
    
    def dibujar_fps(self):
        """
        Dibujar contador de FPS
        
        PSEUDOCÓDIGO:
        fuente = pygame.font.Font(None, 24)
        fps_texto = f"FPS: {int(self.fps_actual)}"
        superficie = fuente.render(fps_texto, True, (0, 255, 0))
        self.pantalla.blit(superficie, (10, ALTO_VENTANA - 30))
        """
        pass
    
    
    def pausar_juego(self):
        """
        Pausar el juego
        
        PSEUDOCÓDIGO:
        self.estado = GameState.PAUSA
        self.juego_pausado = True
        self.assets.pausar_musica()
        print("Juego pausado")
        """
        pass
    
    
    def reanudar_juego(self):
        """
        Reanudar el juego
        
        PSEUDOCÓDIGO:
        self.estado = GameState.JUGANDO
        self.juego_pausado = False
        self.assets.reanudar_musica()
        print("Juego reanudado")
        """
        pass
    
    
    def mostrar_pantalla_mejora(self):
        """
        Mostrar pantalla de selección de mejoras
        
        PSEUDOCÓDIGO:
        # Cambiar estado
        self.estado = GameState.MEJORA
        
        # Generar opciones de mejora
        opciones = self.jugador.mostrar_pantalla_mejoras()
        self.ui_manager.opciones_mejora = opciones
        self.ui_manager.mostrar_pantalla_mejora = True
        
        # Pausar música o reducir volumen
        pygame.mixer.music.set_volume(0.1)
        
        print(f"¡Nivel {self.jugador.nivel} alcanzado!")
        """
        pass
    
    
    def game_over(self):
        """
        Manejar Game Over
        
        PSEUDOCÓDIGO:
        # Cambiar estado
        self.estado = GameState.GAME_OVER
        
        # Detener música de gameplay
        self.assets.detener_musica()
        
        # Reproducir música/sonido de game over
        self.assets.reproducir_sonido("game_over")
        self.assets.reproducir_musica("game_over", loop=0, volumen=0.3)
        
        # Guardar estadísticas
        self.guardar_estadisticas()
        
        print(f"GAME OVER - Nivel: {self.jugador.nivel}, Tiempo: {int(self.jugador.tiempo_supervivencia)}s")
        """
        pass
    
    
    def volver_al_menu(self):
        """
        Volver al menú principal
        
        PSEUDOCÓDIGO:
        # Cambiar estado
        self.estado = GameState.MENU
        
        # Detener música actual
        self.assets.detener_musica()
        
        # Reproducir música de menú
        self.assets.reproducir_musica("menu", volumen=0.3)
        
        # Limpiar sistemas de juego
        self.limpiar_partida()
        
        print("Volviendo al menú principal")
        """
        pass
    
    
    def limpiar_partida(self):
        """
        Limpiar datos de la partida actual
        
        PSEUDOCÓDIGO:
        SI self.spawn_manager:
            self.spawn_manager.enemigos.clear()
        
        SI self.combat_manager:
            self.combat_manager.orbes_xp.clear()
            self.combat_manager.efectos.clear()
        
        # Resetear referencias
        self.mapa = None
        self.jugador = None
        self.camara = None
        self.spawn_manager = None
        self.combat_manager = None
        """
        pass
    
    
    def guardar_estadisticas(self):
        """
        Guardar estadísticas de la partida
        
        PSEUDOCÓDIGO:
        stats = {
            "nivel": self.jugador.nivel,
            "tiempo_supervivencia": self.jugador.tiempo_supervivencia,
            "enemigos_matados": self.jugador.enemigos_matados,
            "xp_total": self.combat_manager.stats["xp_total_recolectada"],
            "daño_infligido": self.combat_manager.stats["daño_total_infligido"]
        }
        
        # TODO: Guardar en archivo JSON
        # import json
        # with open("data/stats.json", "w") as f:
        #     json.dump(stats, f)
        
        print(f"Estadísticas guardadas: {stats}")
        """
        pass
    
    
    def cargar_configuracion(self):
        """
        Cargar configuración del juego
        
        PSEUDOCÓDIGO:
        # TODO: Cargar desde archivo JSON
        # import json
        # try:
        #     with open("data/config.json", "r") as f:
        #         config = json.load(f)
        #         # Aplicar configuración
        # except:
        #     print("No se encontró archivo de configuración")
        """
        pass
    
    
    def guardar_configuracion(self):
        """
        Guardar configuración del juego
        
        PSEUDOCÓDIGO:
        config = {
            "volumen_musica": pygame.mixer.music.get_volume(),
            "volumen_sfx": 0.7,  # TODO: Obtener de settings
            "pantalla_completa": False,
            "mostrar_fps": MOSTRAR_FPS
        }
        
        # TODO: Guardar en archivo JSON
        """
        pass
    
    
    def limpiar(self):
        """
        Limpiar recursos antes de salir
        
        PSEUDOCÓDIGO:
        # Guardar configuración
        self.guardar_configuracion()
        
        # Detener todos los sonidos
        self.assets.detener_musica()
        pygame.mixer.stop()
        
        # Limpiar assets
        self.assets.limpiar()
        
        print("Recursos limpiados. Saliendo...")
        """
        pass
    
    
    def obtener_estadisticas_sesion(self):
        """
        Obtener estadísticas de la sesión actual
        
        PSEUDOCÓDIGO:
        RETORNAR {
            "tiempo_total_juego": self.tiempo_total_juego,
            "partidas_jugadas": self.partidas_jugadas,
            "fps_promedio": int(self.fps_actual)
        }
        """
        pass
    '''