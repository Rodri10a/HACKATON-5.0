<div align="center">

# KARAI SURVIVAL

### Sobrevivi a las Leyendas del Paraguay

<img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/Pygame-2.6-green?style=for-the-badge&logo=python&logoColor=white" alt="Pygame">
<img src="https://img.shields.io/badge/Genre-Roguelike-red?style=for-the-badge" alt="Genre">
<img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" alt="Status">

**Un roguelike de accion y supervivencia en 2D inspirado en el folklore paraguayo**

[Jugar Ahora](#instalacion) | [Documentacion](#caracteristicas) | [Equipo](#equipo-de-desarrollo) | [Roadmap](#roadmap)

---

</div>

## Sobre el Juego

**KARAI SURVIVAL** te sumerge en las tierras paraguayas donde deberas encarnar a un valiente **Campesino** enfrentando oleadas interminables de criaturas del folklore local. A medida que el tiempo avanza, la fauna hostil se vuelve cada vez mas implacable y despiadada.

### Objetivo Principal
Sobrevivi el mayor tiempo posible mientras recolectas **experiencia** para transformar tus humildes herramientas de trabajo en **armas de destruccion masiva**. Cada segundo cuenta, cada decision importa.

### Lo que hace unico a KARAI SURVIVAL
- **Ambientacion 100% Paraguaya**: Enemigos basados en leyendas y mitos locales
- **Sistema de Progresion Dinamico**: Las armas evolucionan con vos
- **Soundtrack Paraguayo Autentico**: Musica que te conecta con la tierra
- **Arte Pixel Art 2D**: Estetica retro con identidad regional
- **Dificultad Creciente**: Cada minuto que sobrevivis, el desafio aumenta

---

## Equipo de Desarrollo

<table align="center">
<tr>
<td align="center" width="200px">
<img src="https://github.com/identicons/rodrigo.png" width="100px" style="border-radius:50%"/><br>
<b>Rodrigo Arguello</b><br>
<i>Team Lead</i><br>
<sub>Logica del Juego</sub><br>
<sub>Arquitectura</sub><br>
<sub>Git/GitHub</sub><br>
<sub>Gestion de Tareas</sub>
</td>
<td align="center" width="200px">
<img src="https://github.com/identicons/eduardo.png" width="100px" style="border-radius:50%"/><br>
<b>Eduardo Lugo</b><br>
<i>Visual & Audio Designer</i><br>
<sub>Diseno de Armas</sub><br>
<sub>Efectos de Sonido</sub><br>
<sub>Musica</sub>
</td>
<td align="center" width="200px">
<img src="https://github.com/identicons/edgar.png" width="100px" style="border-radius:50%"/><br>
<b>Edgar Ojeda</b><br>
<i>Character Artist</i><br>
<sub>Diseno de Personajes</sub><br>
<sub>Diseno de Enemigos</sub><br>
<sub>Sprites & Animaciones</sub>
</td>
</tr>
<tr>
<td align="center" width="200px">
<img src="https://github.com/identicons/marcos.png" width="100px" style="border-radius:50%"/><br>
<b>Marcos Caceres</b><br>
<i>Game Systems Developer</i><br>
<sub>Configuracion del Juego</sub><br>
<sub>Sistema de Personajes</sub><br>
<sub>Player Controller</sub>
</td>
<td align="center" width="200px">
<img src="https://github.com/identicons/oscar.png" width="100px" style="border-radius:50%"/><br>
<b>Oscar Lopez</b><br>
<i>Level Designer</i><br>
<sub>Sistema de Mapas</sub><br>
<sub>Diseno de Niveles</sub><br>
<sub>Ambientacion</sub>
</td>
<td align="center" width="200px">
<img src="https://github.com/identicons/alexis.png" width="100px" style="border-radius:50%"/><br>
<b>Alexis Samudio</b><br>
<i>UI/UX Designer</i><br>
<sub>Interfaz Grafica</sub><br>
<sub>HUD & Menus</sub><br>
<sub>Experiencia de Usuario</sub>
</td>
</tr>
</table>

---

## Stack Tecnologico

<div align="center">

| Categoria | Tecnologia | Version | Proposito |
|-----------|-----------|---------|-----------|
| **Lenguaje** | Python | 3.12 | Desarrollo principal |
| **Game Engine** | Pygame | 2.6 | Motor de juego 2D |
| **Version Control** | Git | Latest | Control de versiones |
| **Hosting** | GitHub | - | Repositorio del proyecto |
| **Arte** | Pixel Art 2D | - | Estilo visual retro |
| **Audio** | WAV/MP3 | - | Efectos y musica |

</div>

---

## Caracteristicas del Juego

### Enemigos del Folklore Paraguayo

<table>
<tr>
<td width="50%">

**Criaturas Terrestres**
- **Lobo** - Rapido y agresivo
- **Yacare** - Lento pero resistente
- **Serpiente** - Movimientos impredecibles
- **Luison** - El septimo hijo, criatura de la noche
- **Aoao** - Espiritu protector convertido en amenaza

</td>
<td width="50%">

**Criaturas Voladoras**
- **Mosquito** - Pequeno pero molesto
- **[Proximamente]** - Mas enemigos en desarrollo

**Escalada de Dificultad**
- Enemigos mas rapidos con el tiempo
- Mayor cantidad de spawns
- Combinaciones letales de enemigos

</td>
</tr>
</table>

### Arsenal del Campesino

| Arma | Tipo | Evolucion |
|------|------|-----------|
| **Machete** | Cuerpo a cuerpo | Nv1 -> Nv2 -> Nv3 -> Nv4 |
| **Rifle** | Distancia | Nv1 -> Nv2 -> Nv3 -> Nv4 |
| **Carrulin** | Area | Nv1 -> Nv2 -> Nv3 -> Nv4 |
| **Terere** | Buff | Nv1 -> Nv2 -> Nv3 -> Nv4 |

> **Sistema de Mejora**: Las armas suben de nivel automaticamente al ganar experiencia

### Power-Ups

- **Jengibre** - Restaura vida instantaneamente
- **Boost de Velocidad** - Aumenta la velocidad de movimiento temporalmente
- **Terere** - Regeneracion de vida

---

## Gameplay y Controles

<div align="center">

### Controles
```
W         -> Mover Arriba
S         -> Mover Abajo
A         -> Mover Izquierda
D         -> Mover Derecha
SPACE BAR -> Atacar
MOUSE     -> Apuntar
```

### Mecanicas Principales

| Mecanica | Descripcion |
|----------|-------------|
| **Sobrevivir** | Resiste oleadas infinitas de enemigos |
| **Recolectar XP** | Derrota enemigos y recoge orbs de experiencia |
| **Subir de Nivel** | Desbloquea mejoras para tus armas |
| **Estrategia** | Los enemigos dropean buffs ocasionales |
| **Contra Reloj** | Cada minuto que pasa, aumenta la dificultad |

</div>

---

## Instalacion y Ejecucion

### Requisitos Previos
```bash
# Python 3.12 o superior
python --version

# Pip actualizado
pip --version
```

### Instalacion

1. **Clonar el repositorio**
```bash
git clone https://github.com/Rodri10a/HACKATON-5.0.git
cd HACKATON-5.0
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Ejecutar el juego**
```bash
python main.py
```

### Estructura del Proyecto
```
KARAI-SURVIVAL/
├── assets/
│   ├── sprites/      # Personajes, enemigos, armas
│   ├── audio/        # Musica y efectos de sonido
│   └── ui/           # Elementos de interfaz
├── src/
│   ├── game/         # Logica principal del juego
│   ├── entities/     # Clases de personajes y enemigos
│   ├── systems/      # Sistemas de juego (colisiones, spawn, etc.)
│   └── ui/           # Interfaces y menus
├── config/           # Archivos de configuracion
├── main.py           # Punto de entrada
└── requirements.txt  # Dependencias
```

---

## Logros y Desafios

### Desafios Superados
- Implementacion completa de **Pygame** desde cero
- Sistema de **logica de juego** roguelike funcional
- **Sistema de colisiones** optimizado y preciso
- Integracion de **arte, sonido y codigo** en tiempo record
- Trabajo colaborativo mediante **Git flow** profesional

### Aprendizajes Clave
- Gestion de proyectos con Git y GitHub
- Desarrollo de juegos con Pygame
- Diseno de sistemas roguelike
- Trabajo en equipo bajo presion
- Optimizacion de rendimiento en Python

---

## Roadmap

### Proximas Actualizaciones

#### Version 1.1 - Expansion de Contenido
- [ ] 5+ Nuevos enemigos del folklore paraguayo
- [ ] 3+ Nuevas armas tradicionales
- [ ] Sistema de personajes jugables
- [ ] Jefes finales epicos

#### Version 1.2 - Nuevos Mundos
- [ ] Mapas adicionales (Selva, Pueblo, Rio)
- [ ] Biomas con mecanicas unicas
- [ ] Sistema de clima dinamico

#### Version 2.0 - Multiplataforma
- [ ] Version movil (Android/iOS)
- [ ] Sistema de guardado en la nube
- [ ] Tablas de clasificacion globales
- [ ] Soporte para gamepad

#### Futuro
- [ ] Modo multijugador cooperativo
- [ ] Editor de niveles
- [ ] Mod support
- [ ] Steam release

---

## Licencia

Este proyecto fue desarrollado durante la **Hackathon 5.0** como proyecto educativo.

---

## Agradecimientos

- A los organizadores de la Hackathon 5.0
- A la rica cultura y folklore paraguayo que inspiro este juego
- A cada miembro del equipo por su dedicacion y talento
- A la comunidad de Pygame por sus recursos

---

## Contacto y Contribuciones

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github)](https://github.com/Rodri10a/HACKATON-5.0)

**Encontraste un bug? Tenes una idea?**

[Reportar Bug](https://github.com/Rodri10a/HACKATON-5.0/issues) | [Sugerir Feature](https://github.com/Rodri10a/HACKATON-5.0/issues) | [Contribuir](https://github.com/Rodri10a/HACKATON-5.0/pulls)

---

<sub>Desarrollado con amor y terere en Paraguay</sub>

**2025 KARAI SURVIVAL Team - Hackathon 5.0**

</div>
