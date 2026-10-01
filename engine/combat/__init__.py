"""M5 Combat: the round engine with the 6-button bar (D-46).

[ES]
Para qué sirve: resolver las peleas por rondas: una sola elección por ronda entre
⚔️ Atacar, 3 habilidades, 🏃 Huir (o 🌀 Esquivar) y 🎒 Mochila.
Documento de diseño: diseno/04-combate/ronda-y-acciones.md
Módulo: M5 Combate (incluye por ahora la parte mínima de M6 Enemigos: elegir y avisar el ataque, y las fases de jefe, D-82)
Depende de: engine.core (Rng, Texts), content/classes.yaml, enemies.yaml, items.yaml, balance.yaml
Lo usan: engine/service/game.py
Eventos que publica: ninguno directo; el servicio publica HitReceived, HeroDowned y CombatEnded
Eventos que escucha: ninguno
Datos de los que es dueño: espacio "combat" del almacén (clave = id del héroe)
Reglas que nunca se rompen:
    1. Una sola elección por ronda; respuestas y objetos van primero; huir va al final (D-46, ronda §6).
    2. Todo el azar sale de la semilla guardada del combate.
Si cambias esto, revisa:
    - Servicio: engine/service/game.py — arma las vistas de combate
    - Números: balance.yaml combat.*, classes.yaml, enemies.yaml
    - Pruebas: tests/test_combat.py, tests/test_boss.py
"""

from engine.combat.engine import (
    CombatContext,
    choose_next_move,
    find_move,
    make_combat,
    phase_for,
    phase_moves,
    resolve_round,
    validate_choice,
)

__all__ = ["CombatContext", "choose_next_move", "find_move", "make_combat", "phase_for", "phase_moves",
           "resolve_round", "validate_choice"]
