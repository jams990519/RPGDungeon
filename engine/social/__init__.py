"""M15 Social: people playing together. Today the guild of a player camp (D-97) and its hunting party (D-106), both provisional.

[ES]
Para qué sirve: lo social del juego. Hoy tiene las cuentas del gremio de un campamento
(guilds.py): cupo por nivel, requisitos para subir y contadores de lo que hacen sus miembros;
y las de la 🏹 Partida de caza de un campamento (hunting.py, D-106): bono de grupo, meta y premio.
Grupos, amigos, alianzas, rangos y banco de gremio son propuesta (diseno/08-social/gremios-y-social.md).
Documento de diseño: diseno/08-social/gremios-y-social.md §0 (en el juego, capa simple); diseno/06-contenido/cacerias.md §0
Módulo: M15 Social
Depende de: ninguno (los números llegan de content/balance.yaml, bloques guild y hunt.party)
Lo usan: engine/service/game.py
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno (el servicio guarda los gremios en los espacios "guild" y "guild_name" del almacén,
    y la partida de caza abierta de cada campamento en "hunt_party")
Reglas que nunca se rompen:
    1. El nivel de gremio da comodidad (más cupo, poder llegar a castillo), nunca poder de combate.
    2. La partida de caza no junta a nadie en una misma pelea: el combate sigue de 1 contra 1 (D-106).
Si cambias esto, revisa:
    - Servicio: engine/service/game.py (secciones "guilds" y "hunting")
    - Pruebas: tests/test_guilds.py, tests/test_hunt.py
"""

from engine.social.guilds import COUNTERS, can_rise, capacity, count, needs, rise

__all__ = ["COUNTERS", "can_rise", "capacity", "count", "needs", "rise"]
