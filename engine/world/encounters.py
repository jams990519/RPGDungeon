"""Which enemies can appear in a zone: the pure rule behind every random encounter (D-108).

An enemy can appear in a zone when the zone's biome is one of its biomes and the zone level is inside its
level range (level_min..level_max). Bosses and retired enemies never appear. When no enemy of the biome
holds that level (a zone past the highest band, like level 101+), the biome enemies whose range is closest
are used, so a far zone never sends a level 6 wolf.

[ES]
Para qué sirve: decidir qué enemigos pueden salir en una zona (del bioma de la zona y con su nivel dentro de
su franja) y con qué nivel salen. Lo usan los encuentros de explorar, recolectar y llegar, y las incursiones.
Documento de diseño: diseno/06-contenido/bestiario.md ("En el juego": franjas por bioma, D-108);
    diseno/02-mundo/mapa-infinito-y-viaje.md (nivel de la zona según la Lejanía)
Módulo: M8 Mundo (dónde aparece cada criatura) con datos de M6 (content/enemies.yaml)
Depende de: ninguno (recibe el diccionario de enemigos ya cargado)
Lo usan: engine/service/game.py (_start_combat) y engine/world/raids.py (pick_enemy)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno
Reglas que nunca se rompen:
    1. Un jefe (boss: true) o un enemigo retirado (retired: true) nunca sale al azar.
    2. Si hay enemigos del bioma cuya franja tiene el nivel de la zona, solo salen esos, en el orden del archivo
       (el mismo orden de siempre: las semillas guardadas dan el mismo enemigo).
    3. Si no hay ninguno, salen los del bioma con la franja más cercana; nunca uno de nivel muy lejano.
    4. El nivel del enemigo siempre queda dentro de su franja (clamp_level).
Si cambias esto, revisa:
    - Servicio: engine/service/game.py (_start_combat: encuentros al explorar, recolectar y llegar)
    - Incursiones: engine/world/raids.py (pick_enemy, la Noche de prueba elige al más fuerte de esta lista)
    - Datos: content/enemies.yaml (biomes, level_min, level_max)
    - Pruebas: tests/test_bestiary.py, tests/test_raids.py
"""

from __future__ import annotations

from typing import Any


def encounter_pool(enemies: dict[str, Any], biome: str, level: int) -> list[tuple[str, dict[str, Any]]]:
    """The (id, definition) pairs that can appear in a zone of this biome and level, in file order.

    [ES]
    Qué hace: da la lista de enemigos que pueden salir en una zona: los del bioma cuya franja tiene ese nivel;
    si no hay, los del bioma con la franja más cercana (y si el bioma no tiene ninguno, los más cercanos de todos).
    La llaman: el servicio (_start_combat) y las incursiones (pick_enemy).
    Si cambia, afecta: contra qué se pelea en cada zona y quién ataca los campamentos.
    """
    common = [(eid, e) for eid, e in enemies.items() if not e.get("boss") and not e.get("retired")]
    candidates = [(eid, e) for eid, e in common if biome in e.get("biomes", [])] or common

    def gap(e: dict[str, Any]) -> int:
        return max(e["level_min"] - level, level - e["level_max"], 0)

    if not candidates:
        return []
    best = min(gap(e) for _, e in candidates)
    return [(eid, e) for eid, e in candidates if gap(e) == best]


def clamp_level(enemy_def: dict[str, Any], level: int) -> int:
    """The enemy's level for a wanted level, kept inside its range. [ES] Qué hace: deja el nivel del enemigo dentro de su franja. La llaman: el servicio y las incursiones. Si cambia, afecta: el nivel de todos los encuentros."""
    return max(enemy_def["level_min"], min(enemy_def["level_max"], level))
