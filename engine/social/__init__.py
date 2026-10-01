"""M15 Social: people playing together. Today only the guild of a player camp (D-97, provisional).

[ES]
Para qué sirve: lo social del juego. Hoy solo tiene las cuentas del gremio de un campamento
(guilds.py): cupo por nivel, requisitos para subir y contadores de lo que hacen sus miembros.
Grupos, amigos, alianzas, rangos y banco de gremio son propuesta (diseno/08-social/gremios-y-social.md).
Documento de diseño: diseno/08-social/gremios-y-social.md §0 (en el juego, capa simple)
Módulo: M15 Social
Depende de: ninguno (los números llegan de content/balance.yaml, bloque guild)
Lo usan: engine/service/game.py
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno (el servicio guarda los gremios en los espacios "guild" y "guild_name" del almacén)
Reglas que nunca se rompen:
    1. El nivel de gremio da comodidad (más cupo, poder llegar a castillo), nunca poder de combate.
Si cambias esto, revisa:
    - Servicio: engine/service/game.py (sección "guilds")
    - Pruebas: tests/test_guilds.py
"""

from engine.social.guilds import COUNTERS, can_rise, capacity, count, needs, rise

__all__ = ["COUNTERS", "can_rise", "capacity", "count", "needs", "rise"]
