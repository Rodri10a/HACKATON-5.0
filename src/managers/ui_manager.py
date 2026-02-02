
# from src.settings import *


import pygame
from settings import *


class UIManager:
    """Gestor de interfaz de usuario"""
    
    def __init__(self, pantalla, jugador):
        """
        Inicializar UI manager
        
        Args:
            pantalla: Surface de pygame
            jugador: Objeto Player
        """
        self.pantalla = pantalla
        self.jugador = jugador
        
        # Fuentes
        self.fuente_grande = pygame.font.Font(None, 48)
        self.fuente_media = pygame.font.Font(None, 32)
        self.fuente_pequeña = pygame.font.Font(None, 24)
        
        # Estados de UI
        self.mostrar_menu_pausa = False
        self.mostrar_pantalla_mejora = False
        self.mostrar_game_over = False
        
        # Opciones de mejora disponibles
        self.opciones_mejora = []
        self.mejora_seleccionada = None
    
    def dibujar_hud(self):
        """Dibujar HUD principal (vida, XP, nivel, tiempo)"""
        # Barra de vida
        self.dibujar_barra_vida()
        
        # Barra de XP
        self.dibujar_barra_xp()
        
        # Nivel actual
        self.dibujar_nivel()
        
        # Tiempo de supervivencia
        self.dibujar_tiempo()
        
        # Contador de enemigos matados
        self.dibujar_estadisticas()
    
    def dibujar_barra_vida(self):
        """Dibujar barra de vida del jugador"""
        x, y = POSICION_BARRA_VIDA
        ancho, alto = TAMAÑO_BARRA_VIDA
        
        # Fondo de la barra (negro)
        pygame.draw.rect(
            self.pantalla,
            (0, 0, 0),
            (x, y, ancho, alto)
        )
        
        # Calcular ancho de vida actual
        porcentaje_vida = self.jugador.vida_actual / self.jugador.vida_maxima
        ancho_vida = int(ancho * porcentaje_vida)
        
        # Dibujar vida (rojo)
        pygame.draw.rect(
            self.pantalla,
            COLOR_VIDA,
            (x, y, ancho_vida, alto)
        )
        
        # Borde de la barra
        pygame.draw.rect(
            self.pantalla,
            COLOR_TEXTO,
            (x, y, ancho, alto),
            2  # grosor del borde
        )
        
        # Texto de vida
        texto = f"{int(self.jugador.vida_actual)} / {self.jugador.vida_maxima}"
        superficie_texto = self.fuente_pequeña.render(texto, True, COLOR_TEXTO)
        texto_rect = superficie_texto.get_rect()
        texto_rect.center = (x + ancho // 2, y + alto // 2)
        self.pantalla.blit(superficie_texto, texto_rect)
    
    def dibujar_barra_xp(self):
        """Dibujar barra de experiencia"""
        x, y = POSICION_BARRA_XP
        ancho, alto = TAMAÑO_BARRA_XP
        
        # Fondo
        pygame.draw.rect(self.pantalla, (0, 0, 0), (x, y, ancho, alto))
        
        # Calcular progreso de XP
        porcentaje_xp = self.jugador.xp_actual / self.jugador.xp_necesaria
        ancho_xp = int(ancho * porcentaje_xp)
        
        # Dibujar XP (dorado)
        pygame.draw.rect(
            self.pantalla,
            COLOR_XP,
            (x, y, ancho_xp, alto)
        )
        
        # Borde
        pygame.draw.rect(self.pantalla, COLOR_TEXTO, (x, y, ancho, alto), 2)
        
        # Texto
        texto = f"XP: {int(self.jugador.xp_actual)} / {self.jugador.xp_necesaria}"
        superficie_texto = self.fuente_pequeña.render(texto, True, COLOR_TEXTO)
        self.pantalla.blit(superficie_texto, (x + 5, y + alto + 5))
    
    def dibujar_nivel(self):
        """Dibujar nivel actual del jugador"""
        texto = f"NIVEL {self.jugador.nivel}"
        superficie = self.fuente_grande.render(texto, True, COLOR_XP)
        rect = superficie.get_rect()
        rect.topright = (ANCHO_VENTANA - 20, 20)
        self.pantalla.blit(superficie, rect)
    
    def dibujar_tiempo(self):
        """Dibujar tiempo de supervivencia"""
        minutos = int(self.jugador.tiempo_supervivencia // 60)
        segundos = int(self.jugador.tiempo_supervivencia % 60)
        
        texto = f"Tiempo: {minutos:02d}:{segundos:02d}"
        superficie = self.fuente_media.render(texto, True, COLOR_TEXTO)
        rect = superficie.get_rect()
        rect.topright = (ANCHO_VENTANA - 20, 80)
        self.pantalla.blit(superficie, rect)
    
    def dibujar_estadisticas(self):
        """Dibujar estadísticas de juego"""
        # Enemigos matados
        texto = f"Enemigos: {self.jugador.enemigos_matados}"
        superficie = self.fuente_pequeña.render(texto, True, COLOR_TEXTO)
        rect = superficie.get_rect()
        rect.topright = (ANCHO_VENTANA - 20, 120)
        self.pantalla.blit(superficie, rect)
        
        # Armas equipadas
        y_offset = 150
        for arma in self.jugador.armas_equipadas:
            texto = f"{arma.tipo} Nv.{arma.nivel}"
            superficie = self.fuente_pequeña.render(texto, True, COLOR_TEXTO)
            rect = superficie.get_rect()
            rect.topright = (ANCHO_VENTANA - 20, y_offset)
            self.pantalla.blit(superficie, rect)
            y_offset += 25
    
    def dibujar_pantalla_mejora(self, opciones):
        """
        Pantalla de selección de mejora al subir nivel
        
        Args:
            opciones: Lista de diccionarios con opciones de mejora
        """
        # Overlay oscuro semi-transparente
        overlay = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.pantalla.blit(overlay, (0, 0))
        
        # Título
        titulo = "¡SUBISTE DE NIVEL!"
        superficie_titulo = self.fuente_grande.render(titulo, True, COLOR_XP)
        rect_titulo = superficie_titulo.get_rect()
        rect_titulo.center = (ANCHO_VENTANA // 2, 100)
        self.pantalla.blit(superficie_titulo, rect_titulo)
        
        # Dibujar 3 opciones de mejora
        ancho_carta = 300
        alto_carta = 400
        espacio = 50
        x_inicial = (ANCHO_VENTANA - (ancho_carta * 3 + espacio * 2)) // 2
        y_carta = 200
        
        for i, opcion in enumerate(opciones):
            x_carta = x_inicial + (ancho_carta + espacio) * i
            
            # Detectar hover del mouse
            mouse_x, mouse_y = pygame.mouse.get_pos()
            hover = (x_carta < mouse_x < x_carta + ancho_carta and
                    y_carta < mouse_y < y_carta + alto_carta)
            
            # Dibujar carta
            self.dibujar_carta_mejora(
                x_carta, y_carta, 
                ancho_carta, alto_carta, 
                opcion, hover, i
            )
        
        # Instrucciones
        texto = "Haz clic en una carta para elegir"
        superficie = self.fuente_media.render(texto, True, COLOR_TEXTO)
        rect = superficie.get_rect()
        rect.center = (ANCHO_VENTANA // 2, ALTO_VENTANA - 50)
        self.pantalla.blit(superficie, rect)
    
    def dibujar_carta_mejora(self, x, y, ancho, alto, opcion, hover, indice):
        """
        Dibujar carta individual de mejora
        
        Args:
            x: Posición X de la carta
            y: Posición Y de la carta
            ancho: Ancho de la carta
            alto: Alto de la carta
            opcion: Diccionario con la opción
            hover: Si el mouse está sobre la carta
            indice: Índice de la carta (0, 1, 2)
        """
        # Color de fondo (más claro si hover)
        color_fondo = (60, 60, 60) if hover else (40, 40, 40)
        
        # Rectángulo de la carta
        pygame.draw.rect(
            self.pantalla,
            color_fondo,
            (x, y, ancho, alto)
        )
        
        # Borde (dorado si hover)
        color_borde = COLOR_XP if hover else COLOR_TEXTO
        pygame.draw.rect(
            self.pantalla,
            color_borde,
            (x, y, ancho, alto),
            3
        )
        
        # Título según tipo de mejora
        tipo = opcion["tipo"]
        
        if tipo == "nueva_arma":
            titulo = "NUEVA ARMA"
            descripcion = opcion["valor"]
        elif tipo == "mejorar_arma":
            titulo = "MEJORAR ARMA"
            descripcion = f"{opcion['valor']} Nv.{opcion['nivel']}"
        else:
            titulo = "MEJORA PASIVA"
            descripcion = opcion["descripcion"]
        
        # Dibujar título
        texto_titulo = self.fuente_media.render(titulo, True, COLOR_XP)
        rect_titulo = texto_titulo.get_rect()
        rect_titulo.centerx = x + ancho // 2
        rect_titulo.top = y + 30
        self.pantalla.blit(texto_titulo, rect_titulo)
        
        # Dibujar descripción
        texto_desc = self.fuente_grande.render(descripcion, True, COLOR_TEXTO)
        rect_desc = texto_desc.get_rect()
        rect_desc.center = (x + ancho // 2, y + alto // 2)
        self.pantalla.blit(texto_desc, rect_desc)
        
        # Número de la carta
        texto_num = self.fuente_pequeña.render(f"[{indice + 1}]", True, COLOR_TEXTO)
        rect_num = texto_num.get_rect()
        rect_num.centerx = x + ancho // 2
        rect_num.bottom = y + alto - 20
        self.pantalla.blit(texto_num, rect_num)
    
    def manejar_click_mejora(self, pos_mouse, opciones):
        """
        Detectar click en carta de mejora
        
        Args:
            pos_mouse: Tupla (x, y) con posición del mouse
            opciones: Lista de opciones de mejora
            
        Returns:
            int: Índice de opción elegida, o None
        """
        mouse_x, mouse_y = pos_mouse
        
        ancho_carta = 300
        alto_carta = 400
        espacio = 50
        x_inicial = (ANCHO_VENTANA - (ancho_carta * 3 + espacio * 2)) // 2
        y_carta = 200
        
        for i, opcion in enumerate(opciones):
            x_carta = x_inicial + (ancho_carta + espacio) * i
            
            # Verificar si click está dentro de la carta
            if (x_carta < mouse_x < x_carta + ancho_carta and
                y_carta < mouse_y < y_carta + alto_carta):
                
                return i  # Índice de opción elegida
        
        return None
    
    def dibujar_menu_pausa(self):
        """Menú de pausa"""
        # Overlay
        overlay = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.pantalla.blit(overlay, (0, 0))
        
        # Título
        titulo = self.fuente_grande.render("PAUSA", True, COLOR_TEXTO)
        rect = titulo.get_rect()
        rect.center = (ANCHO_VENTANA // 2, 200)
        self.pantalla.blit(titulo, rect)
        
        # Opciones
        opciones = ["Reanudar (ESC)", "Salir al Menú (Q)"]
        y_offset = 300
        
        for opcion in opciones:
            texto = self.fuente_media.render(opcion, True, COLOR_TEXTO)
            rect = texto.get_rect()
            rect.center = (ANCHO_VENTANA // 2, y_offset)
            self.pantalla.blit(texto, rect)
            y_offset += 60
    
    def dibujar_game_over(self):
        """Pantalla de Game Over con estadísticas"""
        # Overlay rojo oscuro
        overlay = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA))
        overlay.set_alpha(200)
        overlay.fill((80, 0, 0))
        self.pantalla.blit(overlay, (0, 0))
        
        # Título GAME OVER
        titulo = self.fuente_grande.render("GAME OVER", True, COLOR_VIDA)
        rect = titulo.get_rect()
        rect.center = (ANCHO_VENTANA // 2, 100)
        self.pantalla.blit(titulo, rect)
        
        # Estadísticas finales
        minutos = int(self.jugador.tiempo_supervivencia // 60)
        segundos = int(self.jugador.tiempo_supervivencia % 60)
        
        stats = [
            f"Nivel Alcanzado: {self.jugador.nivel}",
            f"Tiempo Supervivido: {minutos}:{segundos:02d}",
            f"Enemigos Eliminados: {self.jugador.enemigos_matados}",
        ]
        
        y_offset = 200
        for stat in stats:
            texto = self.fuente_media.render(stat, True, COLOR_TEXTO)
            rect = texto.get_rect()
            rect.center = (ANCHO_VENTANA // 2, y_offset)
            self.pantalla.blit(texto, rect)
            y_offset += 50
        
        # Instrucciones
        instruccion = "Presiona ESPACIO para reiniciar o ESC para salir"
        texto = self.fuente_pequeña.render(instruccion, True, COLOR_TEXTO)
        rect = texto.get_rect()
        rect.center = (ANCHO_VENTANA // 2, ALTO_VENTANA - 50)
        self.pantalla.blit(texto, rect)
    
    def dibujar_pantalla_inicio(self):
        """Pantalla de inicio del juego"""
        # Fondo
        self.pantalla.fill((0, 0, 0))
        
        # Título del juego
        titulo = self.fuente_grande.render("CAMPESINO PARAGUAYO", True, COLOR_XP)
        rect = titulo.get_rect()
        rect.center = (ANCHO_VENTANA // 2, 150)
        self.pantalla.blit(titulo, rect)
        
        subtitulo = self.fuente_media.render("Survival", True, COLOR_TEXTO)
        rect = subtitulo.get_rect()
        rect.center = (ANCHO_VENTANA // 2, 200)
        self.pantalla.blit(subtitulo, rect)
        
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
            texto = self.fuente_pequeña.render(linea, True, COLOR_TEXTO)
            rect = texto.get_rect()
            rect.center = (ANCHO_VENTANA // 2, y_offset)
            self.pantalla.blit(texto, rect)
            y_offset += 35
    
    def actualizar(self, dt):
        """
        Actualizar animaciones de UI si las hay
        
        Args:
            dt: Delta time en segundos
        """
        # Por ahora, la UI es estática
        pass