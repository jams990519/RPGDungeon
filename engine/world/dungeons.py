"""Solo dungeons (D-164, D-170, D-171): the pure rules.

Simple layer of diseno/06-contenido/mazmorras-y-bandas.md §0. The map is cut in stretches of `stretch` × `stretch` zones and
each stretch holds 1 or 2 dungeon entrances (Lejanía 2 or more, never side by side). Where they are and their kind (🕳️ a
small dungeon for one, 🌀 a deep dungeon by floors, rarer) come only from the world seed and the coordinates: they never
move. What is inside changes every real day (D-164): the enemy family that fills it (any family of content/dungeons.yaml,
never tied to the biome; never the same two days in a row), its boss (the family's strongest enemy of the dungeon's level),
the path (room names) and the loot. The structure is fixed: a small dungeon is always `rooms` rooms and its boss; a deep
dungeon goes down floor by floor, each one harder. These helpers are pure: the service (engine/service/game.py, section
"solo dungeons") keeps each hero's progress in the store and asks them the rest. The service also checks what these helpers
cannot know: player camp territory hides an entrance and a standing enemy camp blocks it for the day.

[ES]
Para qué sirve: las cuentas de las mazmorras para uno: dónde hay entradas (tramos de 6 × 6 zonas con 1 o 2 cada uno, desde
Lejanía 2, nunca pegadas, 1 de cada 4 profunda), qué familia de enemigos la llena cada día (una por día, nunca la misma dos
días seguidos; cada familia sale una vez cada tantos días como familias haya), qué enemigo hay en cada sala y quién es el
jefe (el más fuerte de la familia en ese nivel), el camino del día (nombres de sala), cómo se endurece cada piso de la
profunda, qué guarda el cofre de la chica y la bolsa de cada piso, y la pieza de equipo de cualquier clase que puede caer
(D-165). No guarda nada.
Documento de diseño: diseno/06-contenido/mazmorras-y-bandas.md §0 (D-164, D-165, D-170); diseno/02-mundo/mapa-infinito-y-viaje.md
    §1.15 (los ❓ del mapa, D-171)
Módulo: M8 Mundo (dónde están las entradas) con datos de M6 (content/dungeons.yaml, content/enemies.yaml) y M3 (botín)
Depende de: engine.core.rng (hash_unit, Rng), engine/world/mapgen.py (lejania), engine/world/raids.py (power: quién es el
    más fuerte); los números llegan de content/balance.yaml, bloque dungeons; las familias, de content/dungeons.yaml
Lo usan: engine/service/game.py (sección "solo dungeons": _dng_kind, _dng_today, _dng_go, _dng_fight_done, el mapa; D-172:
    el 🔭 Reconocer de lejos muestra la familia, el jefe y el cofre de hoy, y el ❓ pasa a 🕳️ / 🌀), tests/test_mazmorras.py,
    tests/test_reconocimiento.py
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno (el servicio guarda el avance de cada héroe en el espacio "dungeon" del almacén y la lista
    🏆 del día en "dungeon_top")
Reglas que nunca se rompen:
    1. entrance_at es determinista: la misma semilla y zona dan siempre lo mismo, para todos. Nunca hay entrada con Lejanía
       menor que min_lejania ni en una zona excluida (la guarida del Guardián).
    2. family_of_day es determinista y nunca repite familia dos días seguidos en la misma mazmorra.
    3. La estructura es fija (D-164): una mazmorra chica tiene siempre rooms salas y el jefe al final; un piso de la
       profunda tiene 1 o 2 peleas y cada boss_every pisos la última es el jefe.
    4. Nunca salen jefes de mundo (boss: true) ni enemigos retirados; el nivel del enemigo es el de la mazmorra o el piso.
    5. El equipo del cofre y de la bolsa puede ser de cualquier clase y tipo (D-165) y nunca es de artesano ni del Guardián
       (piezas con "source").
Si cambias esto, revisa:
    - Servicio: engine/service/game.py (🧭 Explorar, 📍 Zona, 🗺️ Mapa, la pantalla de la mazmorra, _end_combat, _settle)
    - Números: balance.yaml dungeons (stretch, second_chance, min_lejania, spacing, deep_share, level_bonus, small.*, deep.*)
    - Cambiar stretch, second_chance, deep_share, spacing o los hash MUEVE las entradas de un mundo ya creado (no borra nada)
    - Agregar o retirar una familia de content/dungeons.yaml cambia el orden de las familias desde ese día
    - Pruebas: tests/test_mazmorras.py
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any

from engine.core.rng import Rng, hash_unit
from engine.world.mapgen import lejania
from engine.world.raids import power

SMALL = "small"
DEEP = "deep"


def stretch_of(x: int, y: int, size: int) -> tuple[int, int]:
    """The stretch (block of size × size zones) a zone belongs to. [ES] Qué hace: dice en qué tramo del mapa cae una zona. La llaman: entrance_at y el servicio. Si cambia, afecta: dónde están todas las entradas."""
    return x // size, y // size


@lru_cache(maxsize=8192)
def _stretch_entrances(seed: int, bx: int, by: int, size: int, min_lejania: int, second_chance: float, deep_share: float,
                       spacing: int, excluded: tuple[tuple[int, int], ...]) -> tuple[tuple[int, int, str], ...]:
    cells = [(x, y) for x in range(bx * size, bx * size + size) for y in range(by * size, by * size + size)
             if lejania(x, y) >= min_lejania and (x, y) not in excluded]
    count = 2 if hash_unit(seed, "dungeon_count", bx, by) < second_chance else 1
    cells.sort(key=lambda c: (hash_unit(seed, "dungeon_spot", c[0], c[1]), c))
    chosen: list[tuple[int, int, str]] = []
    for x, y in cells:
        if len(chosen) >= count:
            break
        if any(max(abs(x - cx), abs(y - cy)) <= spacing for cx, cy, _ in chosen):
            continue
        chosen.append((x, y, DEEP if hash_unit(seed, "dungeon_kind", x, y) < deep_share else SMALL))
    return tuple(chosen)


def entrances(seed: int, bx: int, by: int, cfg: dict[str, Any],
              excluded: tuple[tuple[int, int], ...] = ()) -> list[tuple[int, int, str]]:
    """The dungeon entrances of one stretch: [(x, y, "small" | "deep")], 1 or 2, never side by side.

    Args:
        cfg: balance.yaml dungeons (stretch, min_lejania, second_chance, deep_share, spacing).
        excluded: zones that never hold an entrance (the Guardian's lair); another zone of the stretch is used instead.

    [ES]
    Qué hace: da las entradas de un tramo: 1, o 2 con second_chance; en zonas de Lejanía min_lejania o más, elegidas por
    la semilla, nunca a spacing zonas o menos una de otra; cada una 🌀 profunda con deep_share, si no 🕳️ chica.
    La llama: entrance_at. Si cambia, afecta: dónde están las mazmorras de todos.
    """
    return list(_stretch_entrances(int(seed), int(bx), int(by), int(cfg["stretch"]), int(cfg["min_lejania"]),
                                   float(cfg["second_chance"]), float(cfg["deep_share"]), int(cfg["spacing"]),
                                   tuple(sorted(tuple(e) for e in excluded))))


def entrance_at(seed: int, x: int, y: int, cfg: dict[str, Any], excluded: tuple[tuple[int, int], ...] = ()) -> str | None:
    """"small" or "deep" if the zone holds a dungeon entrance, else None (before the service's territory check).

    [ES]
    Qué hace: dice si en una zona hay entrada de mazmorra y de qué tipo. Siempre igual para la misma semilla y zona.
    La llama: GameService._dng_kind (que además saca el territorio de los campamentos de jugadores).
    Si cambia, afecta: dónde están las mazmorras de todos.
    """
    bx, by = stretch_of(x, y, int(cfg["stretch"]))
    for ex, ey, kind in entrances(seed, bx, by, cfg, excluded):
        if (ex, ey) == (x, y):
            return kind
    return None


@lru_cache(maxsize=4096)
def _cycle_order(seed: int, x: int, y: int, cycle: int, families: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(families, key=lambda f: (hash_unit(seed, "dungeon_cycle", x, y, cycle, f), f)))


def family_of_day(seed: int, day: int, x: int, y: int, families: list[str]) -> str | None:
    """The enemy family that fills the dungeon at (x, y) on a day; never the same as the day before.

    With n families, every run of n days uses each family once, in an order drawn from the seed for that dungeon (a
    "cycle"); if a cycle would start with the family that ended the previous one, its first two days swap.

    [ES]
    Qué hace: dice qué familia de enemigos llena la mazmorra ese día (hoy duendes, mañana limos, pasado dragones). Cada
    mazmorra tiene su propio orden: en cada vuelta de n días (n = cuántas familias hay) sale cada familia una vez, y nunca
    la misma dos días seguidos. Es igual para todos los jugadores.
    La llama: GameService._dng_today. Si cambia, afecta: contra qué se pelea en cada mazmorra cada día.
    """
    names = tuple(families)
    count = len(names)
    if count == 0:
        return None
    if count == 1:
        return names[0]
    if count == 2:
        return names[(day + int(hash_unit(seed, "dungeon_pair", x, y) * 2)) % 2]
    cycle, pos = divmod(int(day), count)
    order = list(_cycle_order(int(seed), x, y, cycle, names))
    if order[0] == _cycle_order(int(seed), x, y, cycle - 1, names)[-1]:     # the last of a cycle never moves (n >= 3)
        order[0], order[1] = order[1], order[0]
    return order[pos]


def level_pool(enemies: dict[str, Any], members: list[str], level: int) -> list[tuple[str, dict[str, Any]]]:
    """The family members that fit a level: those whose range holds it, else those with the closest range (like D-108).

    [ES]
    Qué hace: de los enemigos de la familia, los que tienen ese nivel en su franja; si ninguno, los de la franja más
    cercana. Nunca jefes de mundo ni retirados. La llaman: delve_rooms y floor_plan.
    Si cambia, afecta: qué enemigos salen en cada sala y piso.
    """
    found = [(eid, enemies[eid]) for eid in members
             if eid in enemies and not enemies[eid].get("boss") and not enemies[eid].get("retired")]
    if not found:
        return []

    def gap(e: dict[str, Any]) -> int:
        return max(int(e["level_min"]) - level, level - int(e["level_max"]), 0)

    best = min(gap(e) for _, e in found)
    return [(eid, e) for eid, e in found if gap(e) == best]


def boss_of(pool: list[tuple[str, dict[str, Any]]], level: int) -> str:
    """The boss among the fitting members: the strongest at that level (life × attack). [ES] Qué hace: elige al jefe: el más fuerte de los que caben en el nivel. La llaman: delve_rooms y floor_plan. Si cambia, afecta: contra quién es la última pelea."""
    return max(pool, key=lambda pair: (power(pair[1], level), pair[0]))[0]


def delve_rooms(seed: int, day: int, x: int, y: int, enemies: dict[str, Any], members: list[str], level: int,
                rooms: int) -> list[dict[str, Any]]:
    """The fights of a small dungeon on a day: `rooms` rooms, then the boss. Always the same count (D-164).

    Returns:
        list of {"id", "level", "boss"}; rooms + 1 entries (empty if the family has no enemy).

    [ES]
    Qué hace: arma las peleas de la mazmorra chica del día: un enemigo de la familia en cada sala (sorteado por la semilla
    y el día) y el jefe al final. Todas del nivel de la mazmorra. Igual para todos.
    La llama: GameService._dng_today. Si cambia, afecta: contra quién pelea cada uno en cada sala.
    """
    pool = level_pool(enemies, members, level)
    if not pool:
        return []
    out = [{"id": pool[int(hash_unit(seed, "dungeon_room", day, x, y, i) * len(pool)) % len(pool)][0],
            "level": level, "boss": False} for i in range(int(rooms))]
    out.append({"id": boss_of(pool, level), "level": level, "boss": True})
    return out


def daily_path(seed: int, day: int, x: int, y: int, names: int, rooms: int) -> list[int]:
    """Indexes of the room names of the day's path (distinct), in order. [ES] Qué hace: elige el camino del día (qué nombre de sala va en cada paso). La llama: el servicio. Si cambia, afecta: solo el texto del camino."""
    order = sorted(range(max(0, names)), key=lambda i: (hash_unit(seed, "dungeon_path", day, x, y, i), i))
    return order[:rooms]


def boss_room(seed: int, day: int, x: int, y: int, names: int) -> int:
    """Index of the day's boss room name. [ES] Qué hace: elige el nombre de la sala del jefe del día. La llama: el servicio. Si cambia, afecta: solo el texto."""
    return int(hash_unit(seed, "dungeon_throne", day, x, y) * max(1, names)) % max(1, names)


def floor_level(base_level: int, floor: int, cfg: dict[str, Any]) -> int:
    """Enemy level on a floor: the dungeon's level + level_per_floor for each floor below the first. [ES] Qué hace: el nivel de los enemigos de un piso. La llaman: floor_plan y el servicio. Si cambia, afecta: qué tan duro es bajar."""
    return int(base_level) + (int(floor) - 1) * int(cfg["level_per_floor"])


def floor_mults(floor: int, cfg: dict[str, Any], boss: bool) -> tuple[float, float]:
    """(life ×, attack ×) of a floor's enemy: +hp_per_floor and +attack_per_floor per floor; the boss on top.

    [ES]
    Qué hace: cuánto más vida y ataque tiene un enemigo de ese piso (5 % y 3 % por piso; el jefe de piso, además, +80 % y
    +20 %). Solo esa pelea: nunca toca enemies.yaml. La llama: floor_plan. Si cambia, afecta: hasta dónde se baja.
    """
    hp = 1.0 + float(cfg["hp_per_floor"]) * (int(floor) - 1)
    attack = 1.0 + float(cfg["attack_per_floor"]) * (int(floor) - 1)
    if boss:
        hp *= float(cfg["boss_hp_mult"])
        attack *= float(cfg["boss_attack_mult"])
    return hp, attack


def floor_plan(seed: int, day: int, x: int, y: int, enemies: dict[str, Any], members: list[str], base_level: int,
               floor: int, cfg: dict[str, Any]) -> list[dict[str, Any]]:
    """The fights of one floor of a deep dungeon on a day: 1, or 2 from floor 2 on; every boss_every floors the last is the boss.

    Returns:
        list of {"id", "level", "boss", "hp_mult", "attack_mult"} (empty if the family has no enemy).

    [ES]
    Qué hace: arma las peleas de un piso de la profunda: el piso 1 tiene 1; desde el 2, 1 o 2 (two_fights_chance, sale del
    día: igual para todos); cada boss_every pisos la última es el jefe de la familia. Nivel y fuerza suben con el piso.
    La llama: el servicio (_dng_go, _dng_fight_done y la pantalla). Si cambia, afecta: qué tan duro es cada piso.
    """
    level = floor_level(base_level, floor, cfg)
    pool = level_pool(enemies, members, level)
    if not pool:
        return []
    count = 1 if floor <= 1 else (2 if hash_unit(seed, "dungeon_fights", day, x, y, floor) < float(cfg["two_fights_chance"]) else 1)
    boss_floor = int(floor) % int(cfg["boss_every"]) == 0
    out = []
    for index in range(count):
        boss = boss_floor and index == count - 1
        enemy_id = boss_of(pool, level) if boss else \
            pool[int(hash_unit(seed, "dungeon_floor", day, x, y, floor, index) * len(pool)) % len(pool)][0]
        hp, attack = floor_mults(floor, cfg, boss)
        out.append({"id": enemy_id, "level": level, "boss": boss, "hp_mult": hp, "attack_mult": attack})
    return out


def coins_for(fights: float, level: int, unit: float, scale: float) -> int:
    """Coins worth `fights` common fights of a level: fights × unit × (1 + scale × (level − 1)). [ES] Qué hace: cuántas monedas valen tantas peleas comunes de ese nivel. La llaman: delve_chest y floor_pot. Si cambia, afecta: cuántas monedas da cada mazmorra."""
    return int(round(float(fights) * float(unit) * (1 + float(scale) * (max(1, int(level)) - 1))))


def pick_materials(seed: int, parts: tuple[Any, ...], materials: dict[str, float], units: int) -> dict[str, int]:
    """`units` materials drawn by weight from a family's list, from the seed and `parts` (no state). [ES] Qué hace: sortea qué materiales de la familia salen (según su peso). La llaman: delve_chest y floor_pot. Si cambia, afecta: qué materiales entran al juego."""
    names = [m for m, w in materials.items() if float(w) > 0]
    total = sum(float(materials[m]) for m in names)
    out: dict[str, int] = {}
    for index in range(units if names else 0):
        pick = hash_unit(seed, "dungeon_mat", *parts, index) * total
        chosen = names[-1]
        for name in names:
            pick -= float(materials[name])
            if pick <= 0:
                chosen = name
                break
        out[chosen] = out.get(chosen, 0) + 1
    return out


def delve_chest(seed: int, day: int, x: int, y: int, level: int, materials: dict[str, float], cfg: dict[str, Any],
                unit: float, scale: float) -> dict[str, Any]:
    """What the small dungeon's chest holds today: coins, materials of the day's family and the chance of a gear piece.

    Args:
        cfg: balance.yaml dungeons.small.chest ({coin_fights, materials: [low, high], gear_chance}).

    [ES]
    Qué hace: dice qué guarda hoy el cofre de la mazmorra chica: monedas de coin_fights peleas comunes de su nivel, de
    materials[0] a materials[1] materiales de la familia del día y la probabilidad de una pieza de equipo (de cualquier
    clase, D-165). Sale de la semilla, el día y la zona: la pantalla muestra justo esto.
    La llama: GameService._dng_chest_of. Si cambia, afecta: cuánto da terminar una mazmorra chica (modesto, D-170).
    """
    low, high = (int(v) for v in cfg["materials"])
    units = low + int(hash_unit(seed, "dungeon_chest", day, x, y) * (high - low + 1))
    return {"coins": coins_for(cfg["coin_fights"], level, unit, scale),
            "items": pick_materials(seed, ("chest", day, x, y), materials, units),
            "gear_chance": float(cfg["gear_chance"]), "gear_level": int(level)}


def floor_pot(seed: int, day: int, x: int, y: int, floor: int, level: int, materials: dict[str, float], cfg: dict[str, Any],
              unit: float, scale: float, boss: bool) -> dict[str, Any]:
    """What a cleared floor adds to the run's pot: coins, materials and, on a boss floor, the chance of a gear piece.

    Args:
        cfg: balance.yaml dungeons.deep.pot ({coin_fights, materials, gear_chance}).

    [ES]
    Qué hace: lo que suma a la bolsa de la bajada cada piso despejado: monedas de media pelea común de su nivel, 1
    material de la familia y, en los pisos de jefe, la probabilidad de una pieza de cualquier clase (D-165).
    La llama: GameService._dng_fight_done. Si cambia, afecta: cuánto vale bajar un piso más.
    """
    return {"coins": coins_for(cfg["coin_fights"], level, unit, scale),
            "items": pick_materials(seed, ("pot", day, x, y, floor), materials, int(cfg["materials"])),
            "gear_chance": float(cfg["gear_chance"]) if boss else 0.0, "gear_level": int(level)}


def chest_gear(items: dict[str, Any], gear_cfg: dict[str, Any], level: int, rng: Rng, chance: float) -> str | None:
    """Maybe a gear piece of ANY class and type (D-165): the usual level window and rarity weights, no "for you" pick.

    Args:
        gear_cfg: balance.yaml gear (level_window, rarity_weight).

    [ES]
    Qué hace: sortea si cae una pieza y cuál, de cualquier clase y tipo por igual (D-165: el botín no está cortado a tu
    medida; lo que no te sirve se vende). Usa la misma ventana de nivel y el mismo peso de rareza que el botín de siempre,
    y nunca da equipo de artesano ni del Guardián (piezas con "source"). El botín de las peleas sigue igual (P-111).
    La llama: el servicio al abrir el cofre de la chica y al despejar un piso de jefe de la profunda.
    Si cambia, afecta: cuánto equipo de otras clases entra al juego para vender.
    """
    if not rng.chance(chance):
        return None
    below, above = gear_cfg["level_window"]
    lootable = [(iid, it) for iid, it in items.items()
                if it.get("kind") == "gear" and not it.get("retired") and not it.get("source")]
    pool = [(iid, it) for iid, it in lootable if level - below <= it.get("req_level", 1) <= level + above]
    if not pool:
        lower = [it.get("req_level", 1) for _, it in lootable if it.get("req_level", 1) <= level + above]
        pool = [(iid, it) for iid, it in lootable if lower and it.get("req_level", 1) == max(lower)]
    if not pool:
        return None
    weights = [float(gear_cfg["rarity_weight"].get(it.get("rarity", "comun"), 1.0)) for _, it in pool]
    pick = rng.random() * sum(weights)
    for (iid, _), weight in zip(pool, weights):
        pick -= weight
        if pick <= 0:
            return iid
    return pool[-1][0]


def add_to_pot(pot: dict[str, Any], coins: int, items: dict[str, int], gear: str | None) -> None:
    """Put a floor's loot in the run's pot. [ES] Qué hace: suma a la bolsa de la bajada lo de un piso. La llama: el servicio. Si cambia, afecta: lo que se cobra al salir."""
    pot["coins"] = int(pot.get("coins", 0)) + int(coins)
    bag = pot.setdefault("items", {})
    for item_id, count in items.items():
        bag[item_id] = bag.get(item_id, 0) + int(count)
    if gear:
        pot.setdefault("gear", []).append(gear)


def defeat_share(pot: dict[str, Any], keep: float) -> dict[str, Any]:
    """The part of the pot kept after losing: `keep` of the coins and of each material (rounded down), and of the pieces.

    [ES]
    Qué hace: lo que te queda de la bolsa si caes o huyes: la mitad de las monedas, de cada material y de las piezas
    (redondeado hacia abajo: con 1 pieza, la pierdes). La llama: el servicio. Si cambia, afecta: cuánto duele perder abajo.
    """
    gear = list(pot.get("gear") or [])
    items = {k: int(v * keep) for k, v in (pot.get("items") or {}).items() if int(v * keep) > 0}
    return {"coins": int(int(pot.get("coins", 0)) * keep), "items": items, "gear": gear[:int(len(gear) * keep)]}
