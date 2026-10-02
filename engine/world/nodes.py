"""Resource nodes of the infinite map (D-171, D-181, D-184): where they are and what each one gives.

A node is a property of a zone. The map is cut in stretches of `stretch` × `stretch` zones and each stretch holds 2 or 3
nodes (Lejanía `min_lejania` or more, never side by side, never on the Claro, the Guardian's lair or a dungeon entrance).
Where they are and their main resource come only from the world seed and the coordinates: they never move and they are the
same for everyone. The main resource is one of the zone's land resources (the service passes them): most of the time one of
the terrain's own resources, otherwise the zone's strongest. These helpers are pure: the service (engine/service/game.py,
section "resource nodes") keeps which nodes each hero discovered (store "nodes") and applies the effect when gathering.

[ES]
Para qué sirve: las cuentas de los nodos de recursos: dónde hay uno (tramos de 6 × 6 zonas con 2 o 3 cada uno, desde
Lejanía 1, nunca pegados, nunca en el Claro, la guarida ni la entrada de una mazmorra; sí dentro del territorio de un
campamento de jugadores, D-87) y cuál es su recurso principal (uno de los de la zona: casi siempre uno propio del terreno,
si no el más fuerte). No guarda nada. El efecto (rinde el doble, se agota más despacio, a veces un raro del terreno) lo
aplica el servicio al recolectar, con los números de balance.yaml nodes.
Documento de diseño: diseno/02-mundo/mapa-infinito-y-viaje.md §1.16 (nodos de recursos, D-181 y D-184)
Módulo: M8 Mundo (nodos)
Depende de: engine.core.rng (hash_unit), engine/world/mapgen.py (lejania), engine/world/dungeons.py (entrance_at: un nodo
    nunca cae en la entrada de una mazmorra); los números llegan de content/balance.yaml, bloques nodes y dungeons
Lo usan: engine/service/game.py (sección "resource nodes": _node_main, _node_seen, el 🗺️ Mapa, 📍 Zona, la llegada y
    _gather_step), tests/test_nodos_y_terrenos.py
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno (el servicio guarda qué nodos descubrió cada héroe en el espacio "nodes" del almacén)
Reglas que nunca se rompen:
    1. node_at es determinista: la misma semilla y zona dan siempre lo mismo, para todos. Nunca hay nodo con Lejanía menor
       que min_lejania, en una zona excluida (el Claro con todo su territorio posible, la guarida) ni en una entrada de
       mazmorra.
    2. Dos nodos nunca quedan pegados (a spacing zonas o menos), tampoco entre tramos vecinos: cada tramo deja libres sus
       últimas `spacing` filas y columnas.
    3. El recurso principal es siempre uno de los recursos de tierra de la zona (nunca el 🐟 pescado).
Si cambias esto, revisa:
    - Números: balance.yaml nodes (stretch, count, spacing, min_lejania, own_share). Cambiarlos o cambiar los hash MUEVE los
      nodos de un mundo ya creado (no borra nada: lo descubierto queda guardado por zona; un nodo que se mueve deja de estar)
    - Mazmorras: cambiar balance.yaml dungeons mueve sus entradas y puede sacar o poner un nodo en esas zonas
    - Servicio: engine/service/game.py (🗺️ Mapa, 📍 Zona, la llegada, recolectar)
    - Pruebas: tests/test_nodos_y_terrenos.py
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any

from engine.core.rng import hash_unit
from engine.world import dungeons as dungeon_rules
from engine.world.mapgen import lejania


def stretch_of(x: int, y: int, size: int) -> tuple[int, int]:
    """The stretch (block of size × size zones) a zone belongs to. [ES] Qué hace: dice en qué tramo cae una zona. La llaman:
    node_at. Si cambia, afecta: dónde están todos los nodos."""
    return x // size, y // size


def _dungeon_key(cfg: dict[str, Any] | None) -> tuple:
    if not cfg:
        return ()
    return (int(cfg["stretch"]), int(cfg["min_lejania"]), float(cfg["second_chance"]), float(cfg["deep_share"]),
            int(cfg["spacing"]), float(cfg.get("third_chance", 0.0)))


@lru_cache(maxsize=8192)
def _stretch_nodes(seed: int, bx: int, by: int, size: int, low: int, high: int, spacing: int, min_lejania: int,
                   excluded: tuple[tuple[int, int], ...], dungeon: tuple, dungeon_excluded: tuple[tuple[int, int], ...]
                   ) -> tuple[tuple[int, int], ...]:
    dcfg = dict(zip(("stretch", "min_lejania", "second_chance", "deep_share", "spacing", "third_chance"), dungeon))
    inner = max(1, size - spacing)       # the last `spacing` rows and columns stay free: no node touches the next stretch
    cells = [(x, y) for x in range(bx * size, bx * size + inner) for y in range(by * size, by * size + inner)
             if lejania(x, y) >= min_lejania and (x, y) not in excluded
             and not (dcfg and dungeon_rules.entrance_at(seed, x, y, dcfg, dungeon_excluded))]
    count = low + int(hash_unit(seed, "node_count", bx, by) * (high - low + 1))
    cells.sort(key=lambda c: (hash_unit(seed, "node_spot", c[0], c[1]), c))
    chosen: list[tuple[int, int]] = []
    for x, y in cells:
        if len(chosen) >= count:
            break
        if any(max(abs(x - cx), abs(y - cy)) <= spacing for cx, cy in chosen):
            continue
        chosen.append((x, y))
    return tuple(chosen)


def nodes_in(seed: int, bx: int, by: int, cfg: dict[str, Any], excluded: tuple[tuple[int, int], ...] = (),
             dungeon_cfg: dict[str, Any] | None = None,
             dungeon_excluded: tuple[tuple[int, int], ...] = ()) -> list[tuple[int, int]]:
    """The resource nodes of one stretch: [(x, y)], `count` of them (2 or 3), never side by side.

    Args:
        cfg: balance.yaml nodes (stretch, count [low, high], spacing, min_lejania).
        excluded: zones that never hold a node (the Claro and all its possible land, the Guardian's lair, fixed zones).
        dungeon_cfg / dungeon_excluded: balance.yaml dungeons and its excluded zones, so a node never sits on an entrance.

    [ES]
    Qué hace: da los nodos de un tramo: de count[0] a count[1] (2 o 3), en zonas de Lejanía min_lejania o más, elegidas
    por la semilla, nunca a spacing zonas o menos uno de otro (ni del tramo de al lado), nunca en una zona excluida ni en
    la entrada de una mazmorra. Si un tramo no tiene lugar para todos (cerca del Claro), da los que caben.
    La llama: node_at. Si cambia, afecta: dónde están los nodos de todos.
    """
    low, high = (int(v) for v in cfg.get("count", [2, 3]))
    return list(_stretch_nodes(int(seed), int(bx), int(by), int(cfg["stretch"]), low, high, int(cfg.get("spacing", 1)),
                               int(cfg.get("min_lejania", 1)), tuple(sorted(tuple(e) for e in excluded)),
                               _dungeon_key(dungeon_cfg), tuple(sorted(tuple(e) for e in dungeon_excluded))))


def node_at(seed: int, x: int, y: int, cfg: dict[str, Any], excluded: tuple[tuple[int, int], ...] = (),
            dungeon_cfg: dict[str, Any] | None = None, dungeon_excluded: tuple[tuple[int, int], ...] = ()) -> bool:
    """True if the zone holds a resource node. [ES] Qué hace: dice si en una zona hay un nodo de recursos; siempre igual para la
    misma semilla y zona. La llama: GameService._node_main. Si cambia, afecta: dónde están los nodos de todos."""
    bx, by = stretch_of(x, y, int(cfg["stretch"]))
    return (x, y) in nodes_in(seed, bx, by, cfg, excluded, dungeon_cfg, dungeon_excluded)


def node_main(seed: int, x: int, y: int, base: dict[str, float], own: dict[str, float], own_share: float) -> str | None:
    """The node's main resource: one of the terrain's own resources of the zone (with own_share) or its strongest one.

    Args:
        base: the zone's base resources, strongest first (engine/world/resources.py zone_resources).
        own: the terrain's own resources the zone brings, strongest first (terrain_resources).

    [ES]
    Qué hace: elige el recurso principal del nodo, siempre uno de los de tierra de la zona: con own_share (0,6) uno de los
    propios del terreno que trae la zona (sorteado por la semilla), si no el más fuerte de la zona. Nunca el pescado.
    La llama: GameService._node_main. Si cambia, afecta: de qué es cada nodo (lo que ya descubrió cada uno se muestra con el
    recurso nuevo).
    """
    land = {**base, **own}
    if not land:
        return None
    if own and hash_unit(seed, "node_type", x, y) < own_share:
        names = sorted(own)
        return names[int(hash_unit(seed, "node_pick", x, y) * len(names)) % len(names)]
    return max(land.items(), key=lambda kv: (kv[1], kv[0]))[0]
