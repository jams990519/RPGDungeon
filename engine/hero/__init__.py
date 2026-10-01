"""M2 Hero: the player character, its stats and progression.

[ES]
Para qué sirve: el personaje del jugador: nombre, clase, nivel, vida, oro, posición,
cinturón y mochila, y la actividad en curso (viaje o exploración).
Documento de diseño: diseno/03-personaje/creacion-de-personaje.md, progresion.md
Módulo: M2 Héroe
Depende de: engine.core (contenido)
Lo usan: engine/service/game.py, engine/combat
Eventos que publica: ninguno (los publica el servicio)
Eventos que escucha: ninguno
Datos de los que es dueño: espacio "hero" del almacén
Reglas que nunca se rompen:
    1. Las estadísticas salen de la clase y el nivel; no se guardan a mano.
Si cambias esto, revisa:
    - Servicio: engine/service/game.py — crea y guarda héroes
    - Combate: engine/combat/engine.py — lee vida, ataque, armadura e iniciativa
    - Pruebas: tests/test_service.py
"""

from engine.hero.hero import Hero, hero_stats, xp_for_level

__all__ = ["Hero", "hero_stats", "xp_for_level"]
