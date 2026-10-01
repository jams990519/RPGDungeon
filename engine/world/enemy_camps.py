"""Enemy camps that move every day (D-112): the pure rules.

Simple layer of diseno/02-mundo/mapa-infinito-y-viaje.md §1.14. Every real day some zones (Lejanía 2 or more) hold an
enemy camp. Where they are comes only from the world seed, the day index and the coordinates, so every player sees the
same camps and nothing is stored to place them; the next day they show up somewhere else (never in the same zone two
days in a row). Each camp has a garrison of 4-8 enemies of its zone's biome at the zone level + 1, the last one its
chief (an elite: more life and attack, like the Noche de prueba). The service keeps what players did to a camp (beaten
guards, who fought, who scouted it, destroyed) in the store, per day and zone, and asks these helpers the rest. The
service also checks what these helpers cannot know: the Claro, the Guardian's lair and player camp territory never
hold a camp.

[ES]
Para qué sirve: las cuentas de los ⛺ campamentos enemigos: si una zona tiene campamento hoy (semilla del mundo + día
+ coordenadas: todos ven los mismos, y al otro día salen en otro lado), su guarnición (enemigos del bioma del nivel de
la zona + 1, y el último es el jefe, el más fuerte), el cofre que suelta al caer (monedas, materiales de la zona y una
probabilidad de equipo), qué tan lejos ve campamentos cada Explorador y la probabilidad de que lo descubran al
🕵️ infiltrarse. No guarda nada.
Documento de diseño: diseno/02-mundo/mapa-infinito-y-viaje.md §1.14 (D-112); diseno/07-economia/profesiones.md §0.2
    (el 🧭 Explorador)
Módulo: M8 Mundo (dónde están los campamentos) con datos de M6 (content/enemies.yaml)
Depende de: engine.core.rng (hash_unit), engine/world/encounters.py (qué enemigos caben en el bioma y el nivel, D-108),
    engine/world/raids.py (power: quién es el más fuerte); los números llegan de content/balance.yaml, bloques
    enemy_camps y explorer
Lo usan: engine/service/game.py (sección "enemy camps and the explorer": _ecamp, _assault, _infiltrate, mapa, Lugares;
    D-172: el 🔭 Reconocer de lejos muestra la misma guarnición y el mismo jefe, sin el cofre), tests/test_enemy_camps.py,
    tests/test_reconocimiento.py
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno (el servicio guarda lo que pasó con cada campamento en el espacio "enemy_camp" del
    almacén, clave "<día>:<x>:<y>")
Reglas que nunca se rompen:
    1. has_camp es determinista: el mismo mundo, día y zona dan siempre lo mismo, para todos los jugadores.
    2. Una zona nunca tiene campamento dos días seguidos, ni con Lejanía menor que min_lejania.
    3. La guarnición tiene entre garrison[0] y garrison[1] enemigos y el último es siempre el jefe; nunca jefes de
       mundo (boss: true) ni enemigos retirados (encounter_pool los deja afuera).
    4. El cofre sale solo de la semilla, el día y la zona: lo que muestra 🕵️ Infiltrarse es lo que se gana.
Si cambias esto, revisa:
    - Servicio: engine/service/game.py (explorar y recolectar bloqueados, 🧭 Explorar, 📍 Zona, 🗺️ Mapa, _end_combat)
    - Números: balance.yaml enemy_camps (density, min_lejania, garrison, level_bonus, chief_*, chest, share, infiltrate)
      y explorer (ranks, base_sight, near_radius)
    - Cambiar density o el hash MUEVE los campamentos del día (no borra nada: lo guardado es por día)
    - Pruebas: tests/test_enemy_camps.py
"""

from __future__ import annotations

from typing import Any

from engine.core.rng import hash_unit
from engine.world.encounters import clamp_level, encounter_pool
from engine.world.mapgen import lejania
from engine.world.raids import power


def rolls_camp(seed: int, day: int, x: int, y: int, density: float) -> bool:
    """True if the day's draw puts a camp in this zone (before the "not two days in a row" rule).

    [ES] Qué hace: el sorteo del día para una zona (semilla + día + coordenadas < densidad). La llama: has_camp.
    Si cambia, afecta: dónde salen todos los campamentos.
    """
    return hash_unit(seed, "enemy_camp", day, x, y) < density


def has_camp(seed: int, day: int, x: int, y: int, density: float, min_lejania: int) -> bool:
    """True if the zone holds an enemy camp on that day: far enough, its draw, and no camp there the day before.

    [ES]
    Qué hace: dice si una zona tiene campamento enemigo ese día: Lejanía de min_lejania o más, el sorteo del día y que
    ayer no lo tuviera (así reaparece en otro lado). El servicio además saca el Claro, la guarida y el territorio de
    los campamentos de jugadores.
    La llama: GameService._ecamp_exists.
    Si cambia, afecta: dónde están los campamentos de todos los jugadores.
    """
    if lejania(x, y) < min_lejania:
        return False
    return rolls_camp(seed, day, x, y, density) and not rolls_camp(seed, day - 1, x, y, density)


def garrison(seed: int, day: int, x: int, y: int, enemies: dict[str, Any], biome: str, level: int,
             size: list[int] | tuple[int, int]) -> list[dict[str, Any]]:
    """The camp's garrison, in fighting order: guards first, the chief last.

    Returns:
        list of {"id", "level", "chief"}; between size[0] and size[1] members. Guards are drawn from the biome's
        encounter pool at `level`; the chief is the strongest of that pool (life × attack).

    [ES]
    Qué hace: arma la guarnición de un campamento: cuántos son (de size[0] a size[1], contando al jefe), qué enemigo es
    cada guardia (de los que salen en ese bioma y nivel) y el jefe al final (el más fuerte de esa lista). Siempre igual
    para el mismo día y zona.
    La llama: GameService._ecamp. Si cambia, afecta: contra qué pelean todos los que asaltan ese campamento.
    """
    low, high = int(size[0]), int(size[1])
    count = low + int(hash_unit(seed, "enemy_camp_size", day, x, y) * (high - low + 1))
    pool = encounter_pool(enemies, biome, level)
    if not pool:
        return []
    members = []
    for index in range(max(1, count) - 1):
        enemy_id, enemy_def = pool[int(hash_unit(seed, "enemy_camp_guard", day, x, y, index) * len(pool)) % len(pool)]
        members.append({"id": enemy_id, "level": clamp_level(enemy_def, level), "chief": False})
    chief_id, chief_def = max(pool, key=lambda pair: (power(pair[1], clamp_level(pair[1], level)), pair[0]))
    members.append({"id": chief_id, "level": clamp_level(chief_def, level), "chief": True})
    return members


def chest(seed: int, day: int, x: int, y: int, level: int, resources: dict[str, float], cfg: dict[str, Any]) -> dict[str, Any]:
    """What the camp's chest holds: coins, materials of the zone and the chance of a gear piece of the camp's level.

    Args:
        resources: the zone's resources, material id -> weight (engine/world/resources.py).
        cfg: balance.yaml enemy_camps.chest ({coins_per_level, materials: [low, high], gear_chance, xp}).

    [ES]
    Qué hace: dice qué guarda el cofre del campamento: monedas (nivel × coins_per_level), de materials[0] a
    materials[1] unidades de los materiales de la zona (según su peso) y la probabilidad de una pieza de equipo del
    nivel del campamento. Sale de la semilla, el día y la zona: 🕵️ Infiltrarse muestra justo esto.
    La llama: GameService._ecamp_chest. Si cambia, afecta: cuánto da destruir un campamento (economía).
    """
    coins = int(level * float(cfg["coins_per_level"]))
    low, high = (int(v) for v in cfg["materials"])
    units = low + int(hash_unit(seed, "enemy_camp_chest", day, x, y) * (high - low + 1))
    items: dict[str, int] = {}
    names = [r for r, w in resources.items() if w > 0]
    total = sum(resources[r] for r in names)
    for index in range(units if names else 0):
        pick = hash_unit(seed, "enemy_camp_item", day, x, y, index) * total
        for res in names:
            pick -= resources[res]
            if pick <= 0:
                break
        items[res] = items.get(res, 0) + 1
    return {"coins": coins, "items": items, "gear_chance": float(cfg["gear_chance"]), "gear_level": level}


def sight(rank: int, cfg: dict[str, Any], map_radius: int) -> int:
    """How far (in zones, the square around you) a hero sees enemy camps, by its 🧭 Explorador rank.

    [ES]
    Qué hace: cuántas zonas a la redonda ve campamentos enemigos un héroe: cualquiera, base_sight (su zona y las 8
    vecinas); desde el rango camps_near, near_radius (3); desde camps_all, todo su mapa (map_radius, 6 → 13 × 13).
    La llama: GameService._ecamp_sight. Si cambia, afecta: qué campamentos ve cada uno en el 🗺️ Mapa.
    """
    ranks = cfg["ranks"]
    if rank >= int(ranks["camps_all"]):
        return int(map_radius)
    if rank >= int(ranks["camps_near"]):
        return int(cfg["near_radius"])
    return int(cfg["base_sight"])


def detect_chance(rank: int, cfg: dict[str, Any], from_rank: int) -> float:
    """Chance that the camp finds an infiltrating explorer: detect_base at the first rank that can try, lower each rank.

    Args:
        cfg: balance.yaml enemy_camps.infiltrate ({detect_base, detect_per_rank, detect_min}).
        from_rank: the 🧭 Explorador rank that opens 🕵️ Infiltrarse (balance.yaml explorer.ranks.infiltrate).

    [ES]
    Qué hace: la probabilidad de que te descubran al infiltrarte: detect_base en el rango que abre la infiltración
    (30) y detect_per_rank menos por cada rango más, sin bajar de detect_min (45 % al 30, 10 % al 100).
    La llama: GameService._infiltrate. Si cambia, afecta: cuántas infiltraciones terminan en pelea.
    """
    chance = float(cfg["detect_base"]) - float(cfg["detect_per_rank"]) * max(0, rank - int(from_rank))
    return max(float(cfg["detect_min"]), min(1.0, chance))
