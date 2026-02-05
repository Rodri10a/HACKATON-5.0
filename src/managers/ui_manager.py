"""
UI_MANAGER.PY - GESTOR DE INTERFAZ DE USUARIO 
==============================================
Todas las pantallas y elementos HUD del juego 
"""

import pygame
from settings import *


class UIManager:
    """Gestor de toda la interfaz del juego"""
    
    def __init__(self, pantalla, jugador):
        """
        Inicializar UI manager
        
        Args:
            pantalla: Surface principal de pygame
            jugador: Referencia al jugador
        """
        self.pantalla = pantalla
        self.jugador = jugador
        
        # Fuentes
        self.fuente_grande = pygame.font.Font(None, 48)
        self.fuente_media = pygame.font.Font(None, 32)
        self.fuente_pequeña = pygame.font.Font(None, 24)
        self.fuente_tiny = pygame.font.Font(None, 20)
        
        # Flags
        self.mostrar_menu_pausa = False
        self.mostrar_pantalla_mejora = False
        self.mostrar_game_over = False
        
        # Opciones de mejora (se setean desde engine)
        self.opciones_mejora = []
    
    def dibujar_hud(self):
        """Dibujar todo el HUD"""
        self.dibujar_barra_vida()
        self.dibujar_barra_xp()
        self.dibujar_info_derecha()
        self.dibujar_armas_equipadas()
    
    def dibujar_barra_vida(self):
        """Dibujar barra de vida con fondo, borde y texto"""
        x, y = 20, 20
        ancho, alto = 250, 28
        
        # Fondo oscuro de la barra
        pygame.draw.rect(self.pantalla, (30, 30, 30), (x - 2, y - 2, ancho + 4, alto + 4), border_radius=6)
        
        # Fondo rojo oscuro (vida perdida)
        pygame.draw.rect(self.pantalla, (80, 10, 10), (x, y, ancho, alto), border_radius=4)
        
        # Calcular porcentaje de vida
        porcentaje = self.jugador.vida_actual / self.jugador.vida_maxima
        ancho_vida = int(ancho * porcentaje)
        
        # Color de la barra según vida restante
        if porcentaje > 0.5:
            color_vida = (50, 200, 50)      # Verde
        elif porcentaje > 0.25:
            color_vida = (230, 180, 0)      # Amarillo
        else:
            color_vida = (220, 30, 30)      # Rojo
        
        # Barra de vida
        if ancho_vida > 0:
            pygame.draw.rect(self.pantalla, color_vida, (x, y, ancho_vida, alto), border_radius=4)
        
        # Borde dorado
        pygame.draw.rect(self.pantalla, (200, 170, 60), (x - 2, y - 2, ancho + 4, alto + 4), 2, border_radius=6)
        
        # Texto de vida centrado
        texto_vida = f"{int(self.jugador.vida_actual)} / {int(self.jugador.vida_maxima)}"
        superficie_texto = self.fuente_pequeña.render(texto_vida, True, (255, 255, 255))
        rect_texto = superficie_texto.get_rect()
        rect_texto.center = (x + ancho // 2, y + alto // 2)
        
        # Sombra del texto
        sombra = self.fuente_pequeña.render(texto_vida, True, (0, 0, 0))
        rect_sombra = sombra.get_rect()
        rect_sombra.center = (x + ancho // 2 + 1, y + alto // 2 + 1)
        self.pantalla.blit(sombra, rect_sombra)
        self.pantalla.blit(superficie_texto, rect_texto)
    
    def dibujar_barra_xp(self):
        """Dibujar barra de XP bajo la barra de vida"""
        x, y = 20, 55
        ancho, alto = 250, 16
        
        # Fondo oscuro
        pygame.draw.rect(self.pantalla, (30, 30, 30), (x - 2, y - 2, ancho + 4, alto + 4), border_radius=4)
        
        # Fondo oscuro de la barra
        pygame.draw.rect(self.pantalla, (40, 30, 10), (x, y, ancho, alto), border_radius=3)
        
        # Calcular porcentaje de XP
        porcentaje_xp = self.jugador.xp_actual / self.jugador.xp_necesaria if self.jugador.xp_necesaria > 0 else 0
        ancho_xp = int(ancho * porcentaje_xp)
        
        # Barra de XP dorada
        if ancho_xp > 0:
            pygame.draw.rect(self.pantalla, COLOR_XP, (x, y, ancho_xp, alto), border_radius=3)
        
        # Borde
        pygame.draw.rect(self.pantalla, (180, 150, 40), (x - 2, y - 2, ancho + 4, alto + 4), 2, border_radius=4)
        
        # Texto de XP
        texto_xp = f"XP: {int(self.jugador.xp_actual)} / {int(self.jugador.xp_necesaria)}"
        superficie_xp = self.fuente_tiny.render(texto_xp, True, (255, 255, 255))
        rect_xp = superficie_xp.get_rect()
        rect_xp.center = (x + ancho // 2, y + alto // 2)
        
        # Sombra
        sombra_xp = self.fuente_tiny.render(texto_xp, True, (0, 0, 0))
        rect_sombra = sombra_xp.get_rect()
        rect_sombra.center = (x + ancho // 2 + 1, y + alto // 2 + 1)
        self.pantalla.blit(sombra_xp, rect_sombra)
        self.pantalla.blit(superficie_xp, rect_xp)
    
    def dibujar_info_derecha(self):
        """Dibujar nivel, tiempo y enemigos en la parte derecha con fondo"""
        x_derecha = ANCHO_VENTANA - 20
        
        # --- NIVEL ---
        # Fondo del nivel
        texto_nivel = f"NIVEL {self.jugador.nivel}"
        sup_nivel = self.fuente_media.render(texto_nivel, True, COLOR_XP)
        rect_nivel = sup_nivel.get_rect()
        rect_nivel.topright = (x_derecha, 15)
        
        # Fondo semi-transparente
        fondo_nivel = pygame.Surface((rect_nivel.width + 20, rect_nivel.height + 10), pygame.SRCALPHA)
        fondo_nivel.fill((0, 0, 0, 160))
        self.pantalla.blit(fondo_nivel, (rect_nivel.x - 10, rect_nivel.y - 5))
        pygame.draw.rect(self.pantalla, (200, 170, 60), (rect_nivel.x - 10, rect_nivel.y - 5, rect_nivel.width + 20, rect_nivel.height + 10), 2, border_radius=6)
        
        # Sombra texto
        sombra = self.fuente_media.render(texto_nivel, True, (0, 0, 0))
        rect_sombra = sombra.get_rect()
        rect_sombra.topright = (x_derecha + 1, 16)
        self.pantalla.blit(sombra, rect_sombra)
        self.pantalla.blit(sup_nivel, rect_nivel)
        
        # --- TIEMPO ---
        minutos = int(self.jugador.tiempo_supervivencia) // 60
        segundos = int(self.jugador.tiempo_supervivencia) % 60
        texto_tiempo = f"Tiempo: {minutos:02d}:{segundos:02d}"
        sup_tiempo = self.fuente_pequeña.render(texto_tiempo, True, (255, 255, 255))
        rect_tiempo = sup_tiempo.get_rect()
        rect_tiempo.topright = (x_derecha, 60)
        
        # Fondo
        fondo_tiempo = pygame.Surface((rect_tiempo.width + 20, rect_tiempo.height + 8), pygame.SRCALPHA)
        fondo_tiempo.fill((0, 0, 0, 160))
        self.pantalla.blit(fondo_tiempo, (rect_tiempo.x - 10, rect_tiempo.y - 4))
        pygame.draw.rect(self.pantalla, (100, 100, 100), (rect_tiempo.x - 10, rect_tiempo.y - 4, rect_tiempo.width + 20, rect_tiempo.height + 8), 1, border_radius=5)
        
        # Sombra texto
        sombra_t = self.fuente_pequeña.render(texto_tiempo, True, (0, 0, 0))
        rect_sombra_t = sombra_t.get_rect()
        rect_sombra_t.topright = (x_derecha + 1, 61)
        self.pantalla.blit(sombra_t, rect_sombra_t)
        self.pantalla.blit(sup_tiempo, rect_tiempo)
        
        # --- ENEMIGOS ---
        texto_enemigos = f"Enemigos: {self.jugador.enemigos_matados}"
        sup_enemigos = self.fuente_pequeña.render(texto_enemigos, True, (255, 255, 255))
        rect_enemigos = sup_enemigos.get_rect()
        rect_enemigos.topright = (x_derecha, 95)
        
        # Fondo
        fondo_enemigos = pygame.Surface((rect_enemigos.width + 20, rect_enemigos.height + 8), pygame.SRCALPHA)
        fondo_enemigos.fill((0, 0, 0, 160))
        self.pantalla.blit(fondo_enemigos, (rect_enemigos.x - 10, rect_enemigos.y - 4))
        pygame.draw.rect(self.pantalla, (100, 100, 100), (rect_enemigos.x - 10, rect_enemigos.y - 4, rect_enemigos.width + 20, rect_enemigos.height + 8), 1, border_radius=5)
        
        # Sombra texto
        sombra_e = self.fuente_pequeña.render(texto_enemigos, True, (0, 0, 0))
        rect_sombra_e = sombra_e.get_rect()
        rect_sombra_e.topright = (x_derecha + 1, 96)
        self.pantalla.blit(sombra_e, rect_sombra_e)
        self.pantalla.blit(sup_enemigos, rect_enemigos)
    
    def dibujar_armas_equipadas(self):
        """Dibujar las armas equipadas abajo a la derecha"""
        x_derecha = ANCHO_VENTANA - 20
        y_inicio = 130
        
        for i, arma in enumerate(self.jugador.armas_equipadas):
            texto_arma = f"{arma.tipo} Nv.{arma.nivel}"
            sup_arma = self.fuente_tiny.render(texto_arma, True, (255, 255, 255))
            rect_arma = sup_arma.get_rect()
            rect_arma.topright = (x_derecha, y_inicio + i * 25)
            
            # Fondo
            fondo_arma = pygame.Surface((rect_arma.width + 16, rect_arma.height + 6), pygame.SRCALPHA)
            fondo_arma.fill((0, 0, 0, 160))
            self.pantalla.blit(fondo_arma, (rect_arma.x - 8, rect_arma.y - 3))
            pygame.draw.rect(self.pantalla, (100, 100, 100), (rect_arma.x - 8, rect_arma.y - 3, rect_arma.width + 16, rect_arma.height + 6), 1, border_radius=4)
            
            # Sombra
            sombra_a = self.fuente_tiny.render(texto_arma, True, (0, 0, 0))
            rect_sombra_a = sombra_a.get_rect()
            rect_sombra_a.topright = (x_derecha + 1, y_inicio + i * 25 + 1)
            self.pantalla.blit(sombra_a, rect_sombra_a)
            self.pantalla.blit(sup_arma, rect_arma)
    
    def dibujar_pantalla_mejora(self, opciones):
        """
        Dibujar pantalla de mejoras al subir de nivel
        
        Args:
            opciones: Lista de diccionarios con las opciones
        """
        if not opciones:
            return
        
        # Overlay oscuro semi-transparente
        overlay = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.pantalla.blit(overlay, (0, 0))
        
        # Título
        titulo = self.fuente_grande.render("¡SUBISTE DE NIVEL!", True, COLOR_XP)
        rect_titulo = titulo.get_rect()
        rect_titulo.center = (ANCHO_VENTANA // 2, 60)
        self.pantalla.blit(titulo, rect_titulo)
        
        # Subtitulo
        subtitulo = self.fuente_pequeña.render("Elige una mejora", True, (200, 200, 200))
        rect_sub = subtitulo.get_rect()
        rect_sub.center = (ANCHO_VENTANA // 2, 100)
        self.pantalla.blit(subtitulo, rect_sub)
        
        # Dibujar 3 cartas de mejora
        carta_ancho = 280
        carta_alto = 350
        espaciado = 40
        total_ancho = carta_ancho * 3 + espaciado * 2
        inicio_x = (ANCHO_VENTANA - total_ancho) // 2
        inicio_y = (ALTO_VENTANA - carta_alto) // 2 + 30
        
        pos_mouse = pygame.mouse.get_pos()
        
        for i, opcion in enumerate(opciones[:3]):
            carta_x = inicio_x + i * (carta_ancho + espaciado)
            carta_y = inicio_y
            
            # Detectar hover
            hover = carta_x <= pos_mouse[0] <= carta_x + carta_ancho and carta_y <= pos_mouse[1] <= carta_y + carta_alto
            
            self.dibujar_carta_mejora(carta_x, carta_y, carta_ancho, carta_alto, opcion, hover, i)
    
    def dibujar_carta_mejora(self, x, y, ancho, alto, opcion, hover, indice):
        """
        Dibujar una carta de mejora mejorada
        
        Args:
            x: Posición X
            y: Posición Y
            ancho: Ancho de la carta
            alto: Alto de la carta
            opcion: Diccionario con la opción
            hover: Si el mouse está encima
            indice: Índice de la carta
        """
        # Fondo de la carta
        color_fondo = (70, 70, 90) if hover else (45, 45, 60)
        pygame.draw.rect(self.pantalla, color_fondo, (x, y, ancho, alto), border_radius=12)
        
        # Borde (dorado si hover)
        color_borde = (255, 215, 0) if hover else (120, 120, 150)
        grosor_borde = 4 if hover else 2
        pygame.draw.rect(self.pantalla, color_borde, (x, y, ancho, alto), grosor_borde, border_radius=12)
        
        # Área para imagen
        imagen_x = x + 10
        imagen_y = y + 10
        imagen_ancho = ancho - 20
        # Aumentar el área de imagen para permitir imágenes más grandes (cuadradas)
        imagen_alto = 140
        
        # Intentar cargar y mostrar imagen (forzar cuadrado)
        imagen_ruta = opcion.get("imagen", "")
        if imagen_ruta:
            try:
                img = pygame.image.load(imagen_ruta).convert_alpha()
                # Forzar tamaño cuadrado: usar el menor lado disponible
                max_w = imagen_ancho - 10
                max_h = imagen_alto - 10
                # Tamaño objetivo máximo (px) para la imagen cuadrada
                objetivo_max = 140
                size = min(objetivo_max, max_w, max_h)
                # Escalar manteniendo calidad
                img = pygame.transform.smoothscale(img, (size, size))
                img_rect = img.get_rect()
                img_rect.center = (imagen_x + imagen_ancho // 2, imagen_y + imagen_alto // 2)
                self.pantalla.blit(img, img_rect)
            except:
                # Placeholder si la imagen no existe
                pygame.draw.rect(self.pantalla, (100, 100, 120), (imagen_x, imagen_y, imagen_ancho, imagen_alto), 2)
                placeholder = self.fuente_pequeña.render("?", True, (150, 150, 170))
                placeholder_rect = placeholder.get_rect()
                placeholder_rect.center = (imagen_x + imagen_ancho // 2, imagen_y + imagen_alto // 2)
                self.pantalla.blit(placeholder, placeholder_rect)
        
        # Línea divisoria
        linea_y = imagen_y + imagen_alto + 10
        pygame.draw.line(self.pantalla, (100, 100, 120), (x + 10, linea_y), (x + ancho - 10, linea_y), 1)
        
        # Título
        titulo = opcion.get("titulo", opcion.get("descripcion", "Mejora"))
        sup_titulo = self.fuente_media.render(titulo, True, (255, 255, 255))
        rect_titulo = sup_titulo.get_rect()
        rect_titulo.center = (x + ancho // 2, linea_y + 35)
        self.pantalla.blit(sup_titulo, rect_titulo)
        
        # Descripción
        descripcion = opcion.get("descripcion", "")
        sup_desc = self.fuente_pequeña.render(descripcion, True, (220, 220, 0))
        rect_desc = sup_desc.get_rect()
        rect_desc.center = (x + ancho // 2, linea_y + 70)
        self.pantalla.blit(sup_desc, rect_desc)
        
        # Detalles adicionales
        detalles = opcion.get("detalles", "")
        if detalles:
            sup_detalles = self.fuente_tiny.render(detalles, True, (180, 180, 180))
            rect_detalles = sup_detalles.get_rect()
            rect_detalles.center = (x + ancho // 2, linea_y + 100)
            self.pantalla.blit(sup_detalles, rect_detalles)
        
        # Información de nivel si aplica
        if opcion.get("nivel_actual"):
            nivel_texto = f"Nv. {opcion.get('nivel_actual')} → {opcion.get('nivel_siguiente')}"
            sup_nivel = self.fuente_tiny.render(nivel_texto, True, (100, 200, 255))
            rect_nivel = sup_nivel.get_rect()
            rect_nivel.center = (x + ancho // 2, linea_y + 125)
            self.pantalla.blit(sup_nivel, rect_nivel)
        
        # Número/índice en la esquina superior izquierda
        numero = self.fuente_media.render(str(indice + 1), True, COLOR_XP if hover else (150, 150, 150))
        rect_numero = numero.get_rect()
        rect_numero.topleft = (x + 15, y + 15)
        self.pantalla.blit(numero, rect_numero)
        
        # Texto "Seleccionar" abajo si hover
        if hover:
            sup_seleccionar = self.fuente_pequeña.render("▶ SELECCIONAR", True, COLOR_XP)
            rect_sel = sup_seleccionar.get_rect()
            rect_sel.center = (x + ancho // 2, y + alto - 30)
            self.pantalla.blit(sup_seleccionar, rect_sel)
    
    def manejar_click_mejora(self, pos_mouse, opciones):
        """
        Verificar si el click fue en una carta de mejora
        
        Args:
            pos_mouse: Posición del mouse (x, y)
            opciones: Lista de opciones
            
        Returns:
            int o None: Índice de la carta clickeada
        """
        carta_ancho = 280
        carta_alto = 350
        espaciado = 40
        total_ancho = carta_ancho * 3 + espaciado * 2
        inicio_x = (ANCHO_VENTANA - total_ancho) // 2
        inicio_y = (ALTO_VENTANA - carta_alto) // 2 + 30
        
        for i in range(min(3, len(opciones))):
            carta_x = inicio_x + i * (carta_ancho + espaciado)
            carta_y = inicio_y
            
            if (carta_x <= pos_mouse[0] <= carta_x + carta_ancho and
                carta_y <= pos_mouse[1] <= carta_y + carta_alto):
                return i
        
        return None
    
    def dibujar_menu_pausa(self):
        """Dibujar pantalla de pausa"""
        # Overlay oscuro
        overlay = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.pantalla.blit(overlay, (0, 0))
        
        # Título PAUSA
        titulo = self.fuente_grande.render("PAUSA", True, (255, 255, 255))
        rect = titulo.get_rect()
        rect.center = (ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 60)
        self.pantalla.blit(titulo, rect)
        
        # Opciones
        opciones = [
            "Reanudar (ESC)",
            "Salir al Menú (Q)"
        ]
        
        y_offset = ALTO_VENTANA // 2 + 10
        for opcion in opciones:
            texto = self.fuente_media.render(opcion, True, (200, 200, 200))
            rect = texto.get_rect()
            rect.center = (ANCHO_VENTANA // 2, y_offset)
            self.pantalla.blit(texto, rect)
            y_offset += 50
    
    def dibujar_game_over(self):
        """Dibujar pantalla de Game Over"""
        # Overlay rojo oscuro
        overlay = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA), pygame.SRCALPHA)
        overlay.fill((80, 0, 0, 200))
        self.pantalla.blit(overlay, (0, 0))
        
        # Título GAME OVER
        titulo = self.fuente_grande.render("GAME OVER", True, (255, 50, 50))
        rect = titulo.get_rect()
        rect.center = (ANCHO_VENTANA // 2, 150)
        self.pantalla.blit(titulo, rect)
        
        # Estadísticas
        minutos = int(self.jugador.tiempo_supervivencia) // 60
        segundos = int(self.jugador.tiempo_supervivencia) % 60
        
        stats = [
            f"Nivel alcanzado: {self.jugador.nivel}",
            f"Tiempo sobrevivido: {minutos:02d}:{segundos:02d}",
            f"Enemigos derrotados: {self.jugador.enemigos_matados}"
        ]
        
        y_offset = ALTO_VENTANA // 2 - 60
        for stat in stats:
            texto = self.fuente_media.render(stat, True, (220, 220, 220))
            rect = texto.get_rect()
            rect.center = (ANCHO_VENTANA // 2, y_offset)
            self.pantalla.blit(texto, rect)
            y_offset += 45
        
        # Instrucciones
        instrucciones = [
            "ESPACIO - Reiniciar",
            "ESC - Salir al Menú"
        ]
        
        y_offset = ALTO_VENTANA - 120
        for instruccion in instrucciones:
            texto = self.fuente_pequeña.render(instruccion, True, (180, 180, 180))
            rect = texto.get_rect()
            rect.center = (ANCHO_VENTANA // 2, y_offset)
            self.pantalla.blit(texto, rect)
            y_offset += 30
    
    def actualizar(self, dt):
        """
        Actualizar UI
        
        Args:
            dt: Delta time en segundos
        """
        pass