"""Gear: who can wear what, the bonus it gives, loot rolls and equip rules (D-77).

[ES]
Para qué sirve: el equipo del héroe. Dice si una pieza te sirve (tipo de tu clase) y si ya tienes
el nivel, suma los bonos de lo que llevas puesto, sortea el botín de equipo al ganar y pone o quita
piezas. Desde D-83 juegas como quieras: el nivel es lo único que impide ponerse algo; una pieza que no
es de tu clase se puede llevar, pero rinde la mitad (gear.off_type_factor). La primera pieza de una
ranura vacía se pone sola.
Documento de diseño: diseno/03-personaje/equipamiento.md §11 (lo que ya está en el juego)
Módulo: M2 Héroe (equipo)
Depende de: content/items.yaml (kind: gear), content/balance.yaml (gear), content/classes.yaml (group)
Lo usan: engine/service/game.py (vistas de equipo, botín, equipo inicial), engine/hero/hero.py (bonos vía el kit)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: Hero.gear (ranura -> id de objeto)
Reglas que nunca se rompen:
    1. Una pieza puesta sale de la mochila; al quitarla vuelve a la mochila. Nunca se duplica ni se pierde.
    2. Solo el nivel impide ponerse una pieza (D-83). El tipo es una referencia: fuera de tu clase rinde menos.
Si cambias esto, revisa:
    - Servicio: engine/service/game.py (_gear_view, _item_view, _end_combat)
    - Números: balance.yaml gear.*, items.yaml stats (mueven el balance de todas las clases)
    - Pruebas: tests/test_gear.py
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


def suits(item: dict[str, Any], hero: Hero, classes: dict[str, Any], balance: dict[str, Any]) -> bool:
    """True if the piece is of a type the hero's class uses (full bonus). [ES] Qué hace: dice si la pieza es de tu clase (la referencia "te sirve"). La llaman: el servicio y gear_bonus. Si cambia, afecta: los consejos y cuánto rinde cada pieza."""
    return item.get("type") in allowed_types(classes, balance, hero)


def can_use(item: dict[str, Any], hero: Hero, classes: dict[str, Any], balance: dict[str, Any]) -> str | None:
    """None if the hero can wear it now; "level" if its level is still too low (the only hard rule, D-83).

    [ES]
    Qué hace: dice si ya puedes ponerte la pieza. Solo el nivel lo impide; el tipo es un consejo (suits).
    La llaman: el servicio (vistas y botín), equip() y auto_equip().
    Si cambia, afecta: quién puede ponerse cada pieza.
    """
    if hero.level < item.get("req_level", 1):
        return "level"
    return None


def piece_stats(item: dict[str, Any], hero: Hero, classes: dict[str, Any], balance: dict[str, Any]) -> dict[str, float]:
    """What a piece really gives this hero: full stats if it suits the class, else × gear.off_type_factor. [ES] Qué hace: los bonos reales de una pieza para ti. La llaman: gear_bonus y las vistas. Si cambia, afecta: cuánto rinde el equipo."""
    factor = 1.0 if suits(item, hero, classes, balance) else balance["gear"]["off_type_factor"]
    return {stat: float(value) * factor for stat, value in item.get("stats", {}).items()}


def gear_bonus(items: dict[str, Any], hero: Hero, classes: dict[str, Any], balance: dict[str, Any]) -> dict[str, float]:
    """Sum of what everything worn gives: {"attack": +frac, "hp": +frac, "armor": +flat}.

    [ES]
    Qué hace: suma los bonos de lo que llevas puesto (las piezas que no son de tu clase rinden la mitad).
    La llaman: el servicio al armar el kit; hero_stats los aplica.
    Si cambia, afecta: vida, ataque y defensa en combate.
    """
    total: dict[str, float] = {}
    for item_id in hero.gear.values():
        if item_id in items:
            for stat, value in piece_stats(items[item_id], hero, classes, balance).items():
                total[stat] = total.get(stat, 0.0) + value
    return total


def roll_gear(items: dict[str, Any], classes: dict[str, Any], balance: dict[str, Any], hero: Hero,
              enemy_level: int, rng: Rng) -> str | None:
    """Maybe drop a gear piece after a victory: level window, rarity weights, mostly "for you".

    [ES]
    Qué hace: sortea si cae una pieza y cuál. Casi siempre es de tu tipo (botín "para ti"),
    a veces de otra clase (para vender). Lo raro sale menos.
    La llama: el servicio al ganar un combate.
    Si cambia, afecta: cuánto equipo entra al juego (balance.yaml gear.drop_chance).
    """
    cfg = balance["gear"]
    if not rng.chance(cfg["drop_chance"]):
        return None
    below, above = cfg["level_window"]
    pool = [(iid, it) for iid, it in items.items() if it.get("kind") == "gear" and not it.get("retired")
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


def auto_equip(hero: Hero, item_id: str, items: dict[str, Any], classes: dict[str, Any], balance: dict[str, Any]) -> bool:
    """Wear a new piece by itself only if its slot is empty and the level allows it (D-83). [ES] Qué hace: si no llevas nada en esa ranura, te pone sola la pieza nueva, aunque no sea la mejor para ti. La llama: el servicio al soltar botín. Si cambia, afecta: qué llevas puesto sin tocar nada."""
    item = items.get(item_id, {})
    if item.get("kind") != "gear" or hero.gear.get(item.get("slot", "")):
        return False
    return equip(hero, item_id, items, classes, balance) is None


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
