# entities/arma.py
# HERRAMIENTAS/ARMAS DEL CAMPESINO

'''
CLASE: Arma (hereda de BaseEntity o sprite básico)
=====================================

ATRIBUTOS:
----------
- nombre: str (ej: "Machete", "Azada", "Hoz")
- nivel: int (nivel actual del arma, empieza en 1)
- damage: float (daño base)
- velocidad_ataque: float (ataques por segundo)
- rango: float (alcance del ataque en píxeles)
- tipo_ataque: str ("melee", "proyectil", "area")
- sprite/imagen: Surface
- posicion: Vector2 o (x, y)
- angulo_rotacion: float
- propietario: Player (referencia al campesino)
- cooldown_actual: float (tiempo restante hasta próximo ataque)
- activa: bool (si el arma está equipada/activa)

# Para armas de proyectil:
- velocidad_proyectil: float
- cantidad_proyectiles: int (cuántos proyectiles dispara)
- patron_disparo: str ("circular", "lineal", "hacia_enemigo_cercano")

# Para mejoras por nivel:
- multiplicador_damage_por_nivel: float (ej: 1.2)
- bonus_stats: dict (estadísticas adicionales por nivel)


MÉTODOS:
--------
__init__(nombre, stats_base):
    - Inicializar todos los atributos base
    - Cargar sprite correspondiente
    - Establecer propietario como None inicialmente

equipar(jugador):
    - Asignar jugador como propietario
    - Marcar como activa
    - Posicionar relativa al jugador

actualizar(delta_time):
    - Reducir cooldown_actual
    - Actualizar posición relativa al jugador
    - Calcular rotación hacia mouse o enemigo más cercano
    - Si cooldown_actual <= 0 y hay enemigos:
        - Ejecutar ataque()
        - Reiniciar cooldown

ataque():
    - Según tipo_ataque:
        SI es "melee":
            - Crear hitbox temporal en el rango
            - Detectar colisiones con enemigos
            - Aplicar daño a enemigos en rango
            - Efecto visual de swing
        
        SI es "proyectil":
            - Crear proyectil(es) según cantidad_proyectiles
            - Aplicar patrón de disparo
            - Añadir proyectiles al grupo de proyectiles
        
        SI es "area":
            - Crear área de efecto
            - Dañar todos los enemigos en radio

subir_nivel():
    - nivel += 1
    - damage *= multiplicador_damage_por_nivel
    - Aplicar mejoras adicionales según nivel:
        * Aumentar rango
        * Aumentar velocidad_ataque
        * Añadir efectos especiales (cada 3 niveles por ej)
    - Actualizar sprite si corresponde

dibujar(pantalla, camara):
    - Dibujar sprite del arma
    - Aplicar rotación
    - Ajustar posición según offset de cámara

obtener_stats():
    - Retornar diccionario con todas las estadísticas actuales


CLASE: Proyectil (si usas proyectiles)
=====================================

ATRIBUTOS:
- posicion: Vector2
- velocidad: Vector2
- damage: float
- rango_maximo: float
- distancia_recorrida: float
- sprite: Surface
- activo: bool

MÉTODOS:
actualizar(delta_time, lista_enemigos):
    - Mover según velocidad
    - Incrementar distancia_recorrida
    - Verificar colisión con enemigos
    - Si colisiona: aplicar daño y desactivar
    - Si distancia_recorrida > rango_maximo: desactivar

dibujar(pantalla, camara):
    - Renderizar sprite


DICCIONARIO DE ARMAS DISPONIBLES:
=================================
ARMAS_BASE = {
    "machete": {
        "damage": 10,
        "velocidad_ataque": 2.0,
        "rango": 50,
        "tipo": "melee"
    },
    "azada": {
        "damage": 8,
        "velocidad_ataque": 1.5,
        "rango": 60,
        "tipo": "melee"
    },
    "honda": {
        "damage": 5,
        "velocidad_ataque": 3.0,
        "rango": 200,
        "tipo": "proyectil",
        "cantidad_proyectiles": 1
    }
    # ... más armas
}

NOTAS DE IMPLEMENTACIÓN:
- Las armas pueden evolucionar (machete → machete mejorado → machete llameante)
- Sistema de sinergia entre armas (combos)
- Auto-targeting para facilitar gameplay
- Efectos de partículas al atacar
'''
