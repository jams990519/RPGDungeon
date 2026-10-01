"""Gear: who can wear what, the bonus it gives, loot rolls and equip rules (D-77).

[ES]
Para qué sirve: el equipo del héroe. Dice si una pieza te sirve (tipo de tu clase) y si ya tienes
el nivel, suma los bonos de lo que llevas puesto, sortea el botín de equipo al ganar y pone o quita
piezas. Desde D-83 juegas como quieras: el nivel es lo único que impide ponerse algo; una pieza que no
es de tu clase se puede llevar, pero rinde la mitad (gear.off_type_factor). La primera pieza de una
ranura vacía se pone sola. D-115 (fase 2): suma el ✨ encantamiento de cada pieza (real_stats) y dice con un solo
puntaje (gear_score: ataque + vida + 2 × defensa, balance.yaml gear.score) si una pieza que no llevas es "⬆️ mejor"
(is_better): tu nivel la permite, es de tu tipo y su puntaje pasa al de lo que llevas en esa ranura.
Documento de diseño: diseno/03-personaje/equipamiento.md §6 (Recuerdos del Guardián) y §11 (lo que ya está en el juego)
Módulo: M2 Héroe (equipo)
Depende de: content/items.yaml (kind: gear), content/balance.yaml (gear; enchanting.enchants para el encantamiento),
    content/classes.yaml (group)
Lo usan: engine/service/game.py (vistas de equipo, botín, equipo inicial, Recuerdo del Guardián), engine/hero/hero.py (bonos vía el kit)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: Hero.gear (ranura -> id de objeto); lee Hero.gear_enchants (lo escribe el servicio)
Reglas que nunca se rompen:
    1. Una pieza puesta sale de la mochila; al quitarla vuelve a la mochila. Nunca se duplica ni se pierde.
    2. Solo el nivel impide ponerse una pieza (D-83). El tipo es una referencia: fuera de tu clase rinde menos.
    3. Las piezas con "source" (por ejemplo las del Guardián, D-82, el equipo de artesano, source: crafted, D-109, o
       sus ✒️ obras maestras, source: masterwork, D-116) nunca salen en el botín al azar: solo se consiguen por su
       fuente (el Recuerdo, una receta de oficio, la suerte del artesano al fabricar).
Si cambias esto, revisa:
    - Servicio: engine/service/game.py (_gear_view, _item_view, _end_combat; drop_chance_for en el bono de la partida de caza)
    - Números: balance.yaml gear.* (drop_chance, high_level_drop, level_window), items.yaml stats (mueven el balance de
      todas las clases; medir con tools/balance_report.py)
    - D-110/D-113: el equipo va cada 10 niveles desde el 10 hasta el 100; si la ventana de nivel cae entre dos niveles de
      pieza, roll_gear usa el nivel de pieza más cercano por debajo. Desde el nivel 10 el botín sale menos y como mucho
      raro; lo mejor de cada nivel es el equipo de artesano (tests/test_balance_d110.py)
    - El equipo inicial toma la primera pieza de tier gear.start_tier (1) de su tipo: el de artesano empieza en tier 2
      y va al final de items.yaml, así nunca se elige (tests/test_professions.py)
    - D-115 (fase 2): gear_bonus suma los encantamientos (Hero.gear_enchants) con real_stats; gear_score/is_better deciden el
      aviso "⬆️ Tienes una pieza mejor" y la marca ⬆️ del servicio (engine/service/game.py _better_piece, _gear_view). Cambiar
      gear.score cambia qué pieza se ofrece; is_better nunca pone nada solo (no hay opción de equipar solo)
    - Pruebas: tests/test_gear.py, tests/test_boss.py, tests/test_professions.py (equipo de artesano), tests/test_balance_d110.py,
      tests/test_oficios_equipo.py (encantamientos y pieza mejor)
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


def enchant_stats(hero: Hero, item_id: str, balance: dict[str, Any]) -> dict[str, float]:
    """The ✨ enchantment the hero put on a piece (D-115, phase 2), as stats; {} if none (or its id is unknown).

    [ES]
    Qué hace: da el bono del ✨ encantamiento guardado en Hero.gear_enchants para esa pieza (⚔️ Filo = ataque, ❤️ Vigor =
    vida, 🛡️ Guarda = defensa; balance.yaml enchanting.enchants). Un encantamiento rinde entero aunque la pieza no sea
    de tu tipo.
    La llaman: real_stats (y por ahí gear_bonus) y el servicio (vistas de equipo).
    Si cambia, afecta: cuánto suma cada encantamiento en combate.
    """
    record = (getattr(hero, "gear_enchants", None) or {}).get(item_id)
    if not record:
        return {}
    edef = ((balance.get("enchanting") or {}).get("enchants") or {}).get(record.get("id"))
    if not edef:
        return {}
    return {edef["stat"]: float(record.get("value", 0.0))}


def real_stats(items: dict[str, Any], item_id: str, hero: Hero, classes: dict[str, Any], balance: dict[str, Any]) -> dict[str, float]:
    """What a piece gives this hero for real: piece_stats (half if off type) plus its enchantment (D-115).

    [ES]
    Qué hace: lo que una pieza te da de verdad: sus bonos (la mitad si no es de tu tipo) más su ✨ encantamiento.
    La llaman: gear_bonus, piece_score, is_better y el servicio (vistas y comparaciones).
    Si cambia, afecta: las estadísticas en combate y qué pieza se marca ⬆️ mejor.
    """
    item = items.get(item_id)
    if not item:
        return {}
    stats = piece_stats(item, hero, classes, balance)
    for stat, value in enchant_stats(hero, item_id, balance).items():
        stats[stat] = stats.get(stat, 0.0) + value
    return stats


def gear_bonus(items: dict[str, Any], hero: Hero, classes: dict[str, Any], balance: dict[str, Any]) -> dict[str, float]:
    """Sum of what everything worn gives: {"attack": +frac, "hp": +frac, "armor": +flat}, enchantments included.

    [ES]
    Qué hace: suma los bonos de lo que llevas puesto (las piezas que no son de tu clase rinden la mitad) y sus ✨
    encantamientos (D-115, fase 2).
    La llaman: el servicio al armar el kit; hero_stats los aplica (la defensa nunca pasa gear.armor_cap).
    Si cambia, afecta: vida, ataque y defensa en combate.
    """
    total: dict[str, float] = {}
    for item_id in hero.gear.values():
        if item_id in items:
            for stat, value in real_stats(items, item_id, hero, classes, balance).items():
                total[stat] = total.get(stat, 0.0) + value
    return total


def gear_score(stats: dict[str, float], balance: dict[str, Any]) -> float:
    """One number for "how good" some stats are: attack + hp + 2 × armor (balance.yaml gear.score).

    [ES]
    Qué hace: resume en un número lo que da una pieza: ataque % + vida % + 2 × defensa (balance.yaml gear.score; la
    defensa pesa doble porque quita daño en cada golpe). Es el puntaje que dice si una pieza es "⬆️ mejor".
    La llaman: piece_score, is_better y el servicio (_gear_diff).
    Si cambia, afecta: qué pieza se marca ⬆️ mejor y el aviso "⬆️ Tienes una pieza mejor".
    """
    weights = (balance.get("gear") or {}).get("score") or {"attack": 1.0, "hp": 1.0, "armor": 2.0}
    return sum(float(weights.get(stat, 0.0)) * value for stat, value in stats.items())


def piece_score(items: dict[str, Any], item_id: str, hero: Hero, classes: dict[str, Any], balance: dict[str, Any]) -> float:
    """gear_score of what a piece really gives this hero (0 for no piece). [ES] Qué hace: el puntaje de una pieza para ti
    (con la mitad si no es de tu tipo y su encantamiento). La llaman: is_better y el servicio. Si cambia, afecta: el aviso ⬆️."""
    return gear_score(real_stats(items, item_id, hero, classes, balance), balance) if item_id in items else 0.0


def is_better(items: dict[str, Any], item_id: str, hero: Hero, classes: dict[str, Any], balance: dict[str, Any]) -> bool:
    """True if a piece the hero is NOT wearing is usable now, of its class's type, and scores more than the worn one.

    "Better" (D-115, phase 2): the hero's level allows it (can_use), it suits the class (suits: its own armor or weapon
    type, or a jewel) and piece_score(new) > piece_score(worn in that slot); an empty slot scores 0.

    [ES]
    Qué hace: dice si una pieza que NO llevas puesta es "⬆️ mejor" para ti: ya tienes el nivel, es de tu tipo (tu armadura,
    tu arma o una joya) y su puntaje (gear_score de lo que te da de verdad, con su encantamiento) pasa al de la pieza que
    llevas en esa ranura (sin nada puesto, cuenta 0). No la pone sola: el servicio avisa y ofrece 🔁 Equipar.
    La llaman: el servicio (aviso al recibir una pieza, marca ⬆️ en 🔁 Equipar).
    Si cambia, afecta: cuándo sale el aviso "⬆️ Tienes una pieza mejor" y la marca ⬆️.
    """
    item = items.get(item_id)
    if not item or item.get("kind") != "gear" or item_id in hero.gear.values():
        return False
    if can_use(item, hero, classes, balance) is not None or not suits(item, hero, classes, balance):
        return False
    worn = hero.gear.get(item.get("slot", ""), "")
    return piece_score(items, item_id, hero, classes, balance) > piece_score(items, worn, hero, classes, balance) + 1e-9


def drop_chance_for(balance: dict[str, Any], enemy_level: int) -> float:
    """Chance that a common victory drops a gear piece: gear.drop_chance, lower from gear.high_level_drop.from_level (D-113).

    [ES]
    Qué hace: dice la probabilidad de que una victoria común suelte una pieza: gear.drop_chance (15 %) y, contra
    enemigos desde gear.high_level_drop.from_level (nivel 10), la más baja de high_level_drop.chance (D-113: el botín
    suelta menos y peor; lo mejor de cada nivel lo fabrican los jugadores).
    La llaman: roll_gear (sin probabilidad propia) y el servicio (bono de la partida de caza, D-106).
    Si cambia, afecta: cuánto equipo entra al juego en cada nivel.
    """
    cfg = balance["gear"]
    high = cfg.get("high_level_drop") or {}
    if high and enemy_level >= int(high.get("from_level", 10 ** 9)):
        return float(high["chance"])
    return float(cfg["drop_chance"])


def roll_gear(items: dict[str, Any], classes: dict[str, Any], balance: dict[str, Any], hero: Hero,
              enemy_level: int, rng: Rng, chance: float | None = None) -> str | None:
    """Maybe drop a gear piece after a victory: level window, rarity weights, mostly "for you".

    Args:
        chance: drop chance for this roll; None uses drop_chance_for (bosses pass their own).

    The pieces come from the level window (gear.level_window: enemy level − 4 .. + 1). Since the gear goes every 10
    levels above level 8 (D-110), a window can fall between two tiers: then the pieces of the nearest tier below are used,
    so a level 15 enemy drops level 10 gear instead of nothing.

    [ES]
    Qué hace: sortea si cae una pieza y cuál. Casi siempre es de tu tipo (botín "para ti"),
    a veces de otra clase (para vender). Lo raro sale menos. Si no hay piezas en la ventana de nivel (el equipo va
    cada 10 niveles desde el 10, D-110), salen las del nivel de pieza más cercano por debajo.
    La llama: el servicio al ganar un combate.
    Si cambia, afecta: cuánto equipo entra al juego (balance.yaml gear.drop_chance y gear.high_level_drop).
    """
    cfg = balance["gear"]
    if not rng.chance(drop_chance_for(balance, enemy_level) if chance is None else chance):
        return None
    below, above = cfg["level_window"]
    lootable = [(iid, it) for iid, it in items.items() if it.get("kind") == "gear" and not it.get("retired") and not it.get("source")]
    pool = [(iid, it) for iid, it in lootable if enemy_level - below <= it.get("req_level", 1) <= enemy_level + above]
    if not pool:
        lower = [it.get("req_level", 1) for _, it in lootable if it.get("req_level", 1) <= enemy_level + above]
        pool = [(iid, it) for iid, it in lootable if lower and it.get("req_level", 1) == max(lower)]
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
