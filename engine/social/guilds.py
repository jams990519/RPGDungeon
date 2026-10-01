"""Guild of a player camp (D-97, provisional): capacity per level and collective requirements.

Capa simple of the guild design: one guild per player camp, founded by the camp's founder.
Its members ARE the camp's members. The guild has a level (1..N, balance.yaml guild.levels):
each level gives a member capacity and lists what the members must do together, after joining,
to rise to the next one (explorations, victories, gathered resources). The service keeps the
guild in the store and calls these pure helpers.

[ES]
Para qué sirve: las cuentas del gremio de un campamento: cuántos miembros caben en cada nivel,
qué tienen que hacer entre todos para subir (exploraciones, peleas ganadas, recursos recolectados)
y la subida misma. No toca el almacén: el servicio lee el gremio, llama a estas funciones y lo guarda.
Documento de diseño: diseno/08-social/gremios-y-social.md §0 (en el juego, capa simple, D-97 provisional)
Módulo: M15 Social
Depende de: ninguno (los números llegan de content/balance.yaml, bloque guild)
Lo usan: engine/service/game.py (_members_cap, _guild_count, _guild_view, _rise_guild)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno (el gremio se guarda en el espacio "guild" del almacén, clave "x:y" de su campamento)
Reglas que nunca se rompen:
    1. Un gremio nunca baja de nivel y los contadores nunca bajan, salvo al pagar una subida.
    2. Lo que sobra al subir pasa al nivel siguiente: nada de lo que hicieron los miembros se pierde.
    3. Los nombres de los contadores son IDs estables: solo se agregan (las misiones contarán cuando existan).
Si cambias esto, revisa:
    - Servicio: engine/service/game.py (cupo del campamento, ganchos de exploración, victoria y recolección)
    - Números: balance.yaml guild.levels (capacity, needs)
    - Pruebas: tests/test_guilds.py
"""

from __future__ import annotations

from typing import Any

# Counter ids, in the order the guild screen shows them. Only add new ones (e.g. "missions" once missions exist).
COUNTERS = ("explorations", "victories", "gathered")


def _row(levels: list[dict[str, Any]], level: int) -> dict[str, Any]:
    return levels[max(0, min(len(levels), int(level)) - 1)] if levels else {}


def capacity(levels: list[dict[str, Any]], level: int) -> int:
    """Members that fit in a guild of this level (the last row holds for higher levels).

    [ES]
    Qué hace: dice cuántos miembros caben en un gremio de ese nivel.
    La llama: el servicio (_members_cap): es el cupo del campamento que tiene gremio.
    Si cambia, afecta: quién puede entrar a cada campamento con gremio y llegar al mínimo del castillo.
    """
    return int(_row(levels, level).get("capacity", 0))


def needs(levels: list[dict[str, Any]], level: int) -> dict[str, int]:
    """What the members must do together to rise from this level; empty at the top level.

    [ES]
    Qué hace: da lo que falta hacer entre todos para pasar al nivel siguiente (vacío en el último).
    La llama: el servicio (pantalla del gremio y subida).
    Si cambia, afecta: el ritmo de los gremios y cuándo un campamento puede ser castillo.
    """
    if not levels or level >= len(levels):
        return {}
    return {k: int(v) for k, v in _row(levels, level).get("needs", {}).items()}


def can_rise(guild: dict[str, Any], levels: list[dict[str, Any]]) -> bool:
    """True when the guild's counters cover every requirement of its level.

    [ES]
    Qué hace: dice si el gremio ya cumple lo que pide su nivel.
    La llama: el servicio (muestra el botón ⬆️ Subir el gremio).
    Si cambia, afecta: cuándo sube cada gremio.
    """
    need = needs(levels, guild.get("level", 1))
    progress = guild.get("progress", {})
    return bool(need) and all(progress.get(k, 0) >= n for k, n in need.items())


def rise(guild: dict[str, Any], levels: list[dict[str, Any]]) -> bool:
    """Rise one level if the requirements are met; the excess carries over. Returns True if it rose.

    [ES]
    Qué hace: sube el gremio un nivel y descuenta lo pedido; lo que sobra queda para el nivel siguiente.
    La llama: el servicio (_rise_guild).
    Si cambia, afecta: el nivel y el cupo de los gremios.
    """
    if not can_rise(guild, levels):
        return False
    progress = guild.setdefault("progress", {})
    for k, n in needs(levels, guild.get("level", 1)).items():
        progress[k] = progress.get(k, 0) - n
    guild["level"] = guild.get("level", 1) + 1
    return True


def count(guild: dict[str, Any], amounts: dict[str, int]) -> bool:
    """Add what a member just did to the guild's counters (only positive amounts). Returns True if it changed.

    [ES]
    Qué hace: suma a los contadores del gremio lo que acaba de hacer un miembro.
    La llama: el servicio al explorar, recolectar y ganar una pelea.
    Si cambia, afecta: el avance de todos los gremios.
    """
    progress = guild.setdefault("progress", {})
    changed = False
    for k, n in amounts.items():
        if n > 0:
            progress[k] = progress.get(k, 0) + int(n)
            changed = True
    return changed
