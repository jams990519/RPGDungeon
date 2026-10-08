"""M3 Classes and talents: a hero picks a class, then earns its specialization point by point.

[ES]
Para qué sirve: la clase se elige al crear el héroe; la especialización se gana con el tiempo.
Cada nivel da 1 punto de talento que se pone en una especialización de la clase: cada especialización
tiene 8 habilidades que se desbloquean con 1, 3, 6, 10, 16, 24, 34 y 46 puntos (balance.yaml talents.unlock),
y cada punto suma una mejora pasiva pequeña según el rol (D-68, D-79). El jugador elige su barra de 3.
Documento de diseño: diseno/03-personaje/talentos.md, clases-y-especializaciones.md
Módulo: M3 Clases y talentos
Depende de: engine.core (contenido), engine.hero
Lo usan: engine/service/game.py
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: los campos talents, points, unlocked y bar del héroe
Reglas que nunca se rompen:
    1. La barra tiene como máximo 3 habilidades y la casilla 1 es siempre una respuesta (D-46, D-79).
    2. La especialización principal es la que tiene más puntos (en empate, se queda la actual).
Si cambias esto, revisa:
    - Servicio: engine/service/game.py (_kit, vistas de talentos, subida de nivel)
    - Números: balance.yaml talents.*
    - Pruebas: tests/test_talents.py, tests/test_spec_abilities.py
"""

from engine.classes.talents import (
    base_response,
    bar,
    bar_choices,
    bar_slots,
    default_spec,
    ensure_talents,
    is_chain_spec,
    kit,
    second_role_open,
    set_bar_slot,
    spend_point,
    specs_of,
    switch_role,
    sync_chain,
    unlock_points,
)

__all__ = ["base_response", "bar", "bar_choices", "bar_slots", "default_spec", "ensure_talents", "is_chain_spec", "kit",
           "second_role_open", "set_bar_slot", "spend_point", "specs_of", "switch_role", "sync_chain", "unlock_points"]
