"""M3 Classes and talents: a hero picks a class, then earns its specialization point by point.

[ES]
Para qué sirve: la clase se elige al crear el héroe; la especialización se gana con el tiempo.
Cada nivel da 1 punto de talento que se pone en una especialización de la clase: con 1, 3 y 6
puntos se desbloquean sus 3 habilidades, y cada punto suma una mejora pasiva según el rol (D-68).
Documento de diseño: diseno/03-personaje/talentos.md, clases-y-especializaciones.md
Módulo: M3 Clases y talentos
Depende de: engine.core (contenido), engine.hero
Lo usan: engine/service/game.py
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: los campos talents, points y unlocked del héroe
Reglas que nunca se rompen:
    1. La barra tiene como máximo 3 habilidades y siempre al menos una respuesta (D-46).
    2. La especialización principal es la que tiene más puntos (en empate, se queda la actual).
Si cambias esto, revisa:
    - Servicio: engine/service/game.py (_kit, vistas de talentos, subida de nivel)
    - Números: balance.yaml talents.*
    - Pruebas: tests/test_talents.py
"""

from engine.classes.talents import (
    base_response,
    bar,
    default_spec,
    ensure_talents,
    kit,
    spend_point,
    specs_of,
    unlock_points,
)

__all__ = ["base_response", "bar", "default_spec", "ensure_talents", "kit", "spend_point", "specs_of", "unlock_points"]
