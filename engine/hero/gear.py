"""Gear: who can wear what, the bonus it gives, loot rolls and equip rules (D-77).

[ES]
Para qué sirve: el equipo del héroe. Dice si una pieza es "para ti" (tipo de tu clase y nivel),
suma los bonos de lo que llevas puesto, sortea el botín de equipo al ganar y pone o quita piezas.
Documento de diseño: diseno/03-personaje/equipamiento.md §6 (Recuerdos del Guardián) y §11 (lo que ya está en el juego)
Módulo: M2 Héroe (equipo)
Depende de: content/items.yaml (kind: gear), content/balance.yaml (gear), content/classes.yaml (group)
Lo usan: engine/service/game.py (vistas de equipo, botín, equipo inicial, Recuerdo del Guardián), engine/hero/hero.py (bonos vía el kit)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: Hero.gear (ranura -> id de objeto)
Reglas que nunca se rompen:
    1. Una pieza puesta sale de la mochila; al quitarla vuelve a la mochila. Nunca se duplica ni se pierde.
    2. Solo se pone lo que es de tu tipo y de tu nivel o menos.
    3. Las piezas con "source" (por ejemplo las del Guardián, D-82) nunca salen en el botín al azar:
       solo se consiguen por su fuente (el Recuerdo).
Si cambias esto, revisa:
    - Servicio: engine/service/game.py (_gear_view, _item_view, _end_combat)
    - Números: balance.yaml gear.*, items.yaml stats (mueven el balance de todas las clases)
    - Pruebas: tests/test_gear.py, tests/test_boss.py
"""

from __future__ import annotations

from typing import Any

from engine.core.rng import Rng
from engine.hero.hero import Hero


def group_of(classes: dict[str, Any], hero: Hero) -> str:
    """The hero's class group (guerrero, mago...). [ES] Qué hace: da la clase base del héroe. La llaman: este módulo. Si cambia, afecta: qué equipo es para cada uno."""
    return classes[hero.class_id].get("group", hero.class_id)


def allowed_types(classes: dict[str, Any], balance: dict[str, Any], hero: Hero) -> set[str]:
    """Armor and weapon types the hero's class uses, plus jewels (anyone). [ES] Qué hace: lista los tipos de equipo de tu clase. La llaman: can_use y roll_gear. Si cambia, afecta: el botín "para ti"."""
    cfg = balance["gear"]
    group = group_of(classes, hero)
    return {cfg["armor_by_group"].get(group, ""), *cfg["weapons_by_group"].get(group, []), "joya"}


def can_use(item: dict[str, Any], hero: Hero, classes: dict[str, Any], balance: dict[str, Any]) -> str | None:
    """None if the hero can wear it now; else "type" (not for your class) or "level" (later).

    [ES]
    Qué hace: dice si la pieza es para ti ahora, más adelante ("level") o nunca ("type").
    La llaman: el servicio (vistas y botín) y equip().
    Si cambia, afecta: quién puede ponerse cada pieza.
    """
    if item.get("type") not in allowed_types(classes, balance, hero):
        return "type"
    if hero.level < item.get("req_level", 1):
        return "level"
    return None


def gear_bonus(items: dict[str, Any], hero: Hero) -> dict[str, float]:
    """Sum of the stats of everything worn: {"attack": +frac, "hp": +frac, "armor": +flat}.

    [ES]
    Qué hace: suma los bonos de lo que llevas puesto.
    La llaman: el servicio al armar el kit; hero_stats los aplica.
    Si cambia, afecta: vida, ataque y defensa en combate.
    """
    total: dict[str, float] = {}
    for item_id in hero.gear.values():
        for stat, value in items.get(item_id, {}).get("stats", {}).items():
            total[stat] = total.get(stat, 0.0) + float(value)
    return total


def roll_gear(items: dict[str, Any], classes: dict[str, Any], balance: dict[str, Any], hero: Hero,
              enemy_level: int, rng: Rng, chance: float | None = None) -> str | None:
    """Maybe drop a gear piece after a victory: level window, rarity weights, mostly "for you".

    Args:
        chance: drop chance for this roll; None uses balance gear.drop_chance (bosses pass their own).

    [ES]
    Qué hace: sortea si cae una pieza y cuál. Casi siempre es de tu tipo (botín "para ti"),
    a veces de otra clase (para vender). Lo raro sale menos.
    La llama: el servicio al ganar un combate.
    Si cambia, afecta: cuánto equipo entra al juego (balance.yaml gear.drop_chance).
    """
    cfg = balance["gear"]
    if not rng.chance(cfg["drop_chance"] if chance is None else chance):
        return None
    below, above = cfg["level_window"]
    pool = [(iid, it) for iid, it in items.items() if it.get("kind") == "gear" and not it.get("retired") and not it.get("source")
            and enemy_level - below <= it.get("req_level", 1) <= enemy_level + above]
    if not pool:
        return None
    mine = allowed_types(classes, balance, hero)
    for_you = rng.chance(cfg["for_you_chance"])
    narrowed = [(iid, it) for iid, it in pool if (it.get("type") in mine) == for_you]
    pool = narrowed or pool
    weights = [cfg["rarity_weight"].get(it.get("rarity", "comun"), 1.0) for _, it in pool]
    pick = rng.random() * sum(weights)
    for (iid, _), weight in zip(pool, weights):
        pick -= weight
        if pick <= 0:
            return iid
    return pool[-1][0]


def source_choices(items: dict[str, Any], classes: dict[str, Any], balance: dict[str, Any], hero: Hero, source: str) -> list[str]:
    """The pieces of a source (e.g. "guardian") made for this hero: its main weapon type, then its armor type.

    [ES]
    Qué hace: da las dos piezas que el Recuerdo del Guardián ofrece a este héroe: el arma de su
    tipo principal y la armadura de su tipo (siempre "para ti").
    La llama: el servicio (pantalla del Recuerdo).
    Si cambia, afecta: qué puede elegir cada clase con su Recuerdo.
    """
    cfg = balance["gear"]
    group = group_of(classes, hero)
    wanted = [(cfg["weapons_by_group"].get(group) or [None])[0], cfg["armor_by_group"].get(group)]
    out = []
    for typ in wanted:
        for iid, it in items.items():
            if it.get("kind") == "gear" and it.get("source") == source and it.get("type") == typ and not it.get("retired"):
                out.append(iid)
                break
    return out


def equip(hero: Hero, item_id: str, items: dict[str, Any], classes: dict[str, Any], balance: dict[str, Any]) -> str | None:
    """Wear a piece from the backpack; the old piece of that slot goes back. Returns an error code or None.

    [ES]
    Qué hace: te pone una pieza de la mochila y guarda en la mochila la que tenías en esa ranura.
    La llama: el servicio (botón ✅ Equipar).
    Si cambia, afecta: el inventario y las estadísticas.
    """
    item = items.get(item_id)
    if not item or item.get("kind") != "gear" or hero.backpack.get(item_id, 0) <= 0:
        return "missing"
    reason = can_use(item, hero, classes, balance)
    if reason:
        return reason
    slot = item["slot"]
    old = hero.gear.get(slot)
    hero.backpack[item_id] -= 1
    if hero.backpack[item_id] <= 0:
        del hero.backpack[item_id]
    if old:
        hero.backpack[old] = hero.backpack.get(old, 0) + 1
    hero.gear[slot] = item_id
    return None


def unequip(hero: Hero, slot: str) -> str | None:
    """Take off the piece of a slot and put it in the backpack. Returns the item id or None. [ES] Qué hace: quita la pieza y la guarda en la mochila. La llama: el servicio (botón Quitar). Si cambia, afecta: inventario y estadísticas."""
    item_id = hero.gear.pop(slot, None)
    if item_id:
        hero.backpack[item_id] = hero.backpack.get(item_id, 0) + 1
    return item_id


def starter_gear(items: dict[str, Any], classes: dict[str, Any], balance: dict[str, Any], hero: Hero) -> list[str]:
    """Equip the tier-1 weapon (first type of the class) and armor of the hero's type in empty slots. [ES] Qué hace: da el equipo inicial (arma y armadura básicas de tu clase), ya puesto. La llama: el servicio al crear el héroe y una vez a los héroes viejos (parche 0.6). Si cambia, afecta: el poder inicial."""
    cfg = balance["gear"]
    group = group_of(classes, hero)
    wanted = {"arma": (cfg["weapons_by_group"].get(group) or [None])[0], "armadura": cfg["armor_by_group"].get(group)}
    given = []
    for slot, typ in wanted.items():
        if not typ or hero.gear.get(slot):
            continue
        for iid, it in items.items():
            if it.get("kind") == "gear" and it.get("slot") == slot and it.get("type") == typ and it.get("tier") == cfg["start_tier"]:
                hero.gear[slot] = iid
                given.append(iid)
                break
    return given
