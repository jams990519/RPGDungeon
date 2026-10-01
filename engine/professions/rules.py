"""Chained professions, phase 1 (D-109): ranks from profession xp, who produces each material, recipe checks,
perks (D-111) and masterworks (D-116).

Pure helpers over content/professions.yaml and balance.yaml "professions" / "masterwork". They never touch the store:
the service keeps every hero's profession xp in Hero.professions (profession id -> xp) and calls these functions.

[ES]
Para qué sirve: las cuentas de los oficios encadenados (recolectar → refinar → fabricar): el rango de 1 a 100 que
sale de la experiencia de cada oficio, su título (Aprendiz, Oficial...), qué oficio produce cada material (para
comprobar que casi toda receta pide materiales de dos oficios o más), qué falta para una receta y cuántas veces
alcanza con lo que llevas y tu energía. También el beneficio de cada oficio (D-111) y la ✒️ obra maestra (D-116):
las piezas gemelas "obra maestra" que se arman al cargar el contenido (masterwork_items) y la probabilidad de que
una pieza fabricada salga así (masterwork_chance). D-115 (fase 2, lado del equipo): las cuentas del ✨ Encantamiento:
cuántas esencias da desencantar una pieza (disenchant_yield, disenchant_amount con el beneficio del oficio), qué
encantamiento lleva cada ranura (enchant_for_slot), cuánto suma con tu rango (enchant_value) y qué pide (enchant_cost).
No guarda nada: el servicio lee Hero.professions y llama a estas funciones.
Documento de diseño: diseno/07-economia/profesiones.md §0 (fase 1, D-109), §0.2 (beneficios), §0.4 (obra maestra),
    §0.5 (✨ Encantamiento, D-115 fase 2) y §4
Módulo: M14 Oficios
Depende de: ninguno (los datos llegan de content/professions.yaml y de content/balance.yaml, bloques professions,
    masterwork y enchanting)
Lo usan: engine/service/game.py (secciones "professions" y "enchanting"), engine/core/content.py (masterwork_items, al
    cargar los objetos), tests/test_professions.py, tests/test_masterwork.py y tests/test_oficios_equipo.py
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno (la experiencia de oficio se guarda en Hero.professions)
Reglas que nunca se rompen:
    1. El rango nunca baja: sale solo de la experiencia acumulada, que nunca se resta.
    2. Sin tope de oficios (D-57): cualquiera puede subir todos; el freno es el tiempo, los materiales y la estación.
    3. Una receta se hace entera o no se hace: nunca se gasta la mitad de los materiales.
    4. Los ids de obra maestra son el id de la pieza + MASTERWORK_SUFFIX ("_obra") y quedan guardados en las mochilas:
       el sufijo nunca cambia (IDs estables). Una obra maestra nunca sale en el botín al azar (source: masterwork).
Si cambias esto, revisa:
    - La curva (balance.yaml professions.rank_formula): cuánto tarda el rango 100 (~1 año dedicado, profesiones.md §4)
    - Servicio: engine/service/game.py (_prof_rank, _trade_gather, _trade_loot, _station_view, _recipe_view, _make)
    - Obra maestra (D-116): balance.yaml masterwork (bono, bono de más por ranura, precio y probabilidad base) y el
      perk {masterwork} de la 🪑 Carpintería en content/professions.yaml; el servicio la sortea en _make
    - Beneficios (perks): una clave nueva va en PERK_KEYS, en el texto prof.perk.<clave> y donde el servicio la use. D-112:
      "explore" (🧭 Explorador) son puntos de exploración por vuelta (game.py _explore_step usa la parte entera)
    - ✨ Encantamiento (D-115, fase 2): balance.yaml enchanting (esencias por rareza y nivel, costo por nivel de la pieza,
      un encantamiento por ranura con su valor de min a max); los precios de las esencias en items.yaml tienen que dejar
      que desencantar y vender las esencias pague siempre menos que vender la pieza (tests/test_oficios_equipo.py)
    - Pruebas: tests/test_professions.py, tests/test_masterwork.py, tests/test_enemy_camps.py, tests/test_oficios_equipo.py
"""

from __future__ import annotations

import math
from typing import Any


def xp_for_rank(formula: dict[str, float], rank: int) -> int:
    """Total profession xp needed to reach a rank: base × (rank − 1) ^ exponent.

    [ES]
    Qué hace: dice cuánta experiencia de oficio total pide un rango (rango 1 = 0).
    La llaman: rank_of, la pantalla ⚒️ Oficios (barra de avance) y las pruebas.
    Si cambia, afecta: el ritmo de todos los oficios (balance.yaml professions.rank_formula).
    """
    if rank <= 1:
        return 0
    return int(round(formula["base"] * (rank - 1) ** formula["exponent"]))


def rank_of(xp: int, formula: dict[str, float], max_rank: int) -> int:
    """The rank (1..max_rank) that a profession xp total gives.

    [ES]
    Qué hace: convierte la experiencia de un oficio en su rango, de 1 a max_rank (100).
    La llaman: el servicio cada vez que muestra o usa un rango.
    Si cambia, afecta: qué recetas y materiales raros tiene abiertos cada héroe.
    """
    rank = 1
    while rank < max_rank and xp >= xp_for_rank(formula, rank + 1):
        rank += 1
    return rank


def rank_title(rank: int, titles: list[dict[str, Any]]) -> str:
    """Id of the rank title (aprendiz, oficial... gran_maestro) for a rank; titles are sorted by "from".

    [ES]
    Qué hace: da el id del título del rango (Aprendiz 1-20, Oficial 21-40, Experto 41-60, Artesano 61-80,
    Maestro 81-95, Gran Maestro 96-100; content/professions.yaml "ranks").
    La llaman: la pantalla ⚒️ Oficios y los avisos de subida de rango.
    Si cambia, afecta: solo el nombre que se muestra.
    """
    current = titles[0]["id"] if titles else ""
    for row in titles:
        if rank >= int(row["from"]):
            current = row["id"]
    return current


def gatherer_of(item_id: str, professions: dict[str, Any]) -> str | None:
    """The gathering profession that collects (or skins) an item, or None.

    [ES]
    Qué hace: dice qué oficio de recolección junta un material (madera → leñador, carne y piel → desollador...).
    La llaman: el servicio al recolectar (_trade_gather) y al soltar botín (_trade_loot).
    Si cambia, afecta: qué oficio sube con cada material.
    """
    for pid, pdef in professions.items():
        if pdef.get("branch") == "gather" and (item_id in (pdef.get("gathers") or []) or item_id in (pdef.get("skins") or [])):
            return pid
    return None


def source_of(item_id: str, professions: dict[str, Any], recipes: dict[str, Any]) -> str | None:
    """The profession that produces an item: its gathering profession, its rare-find profession or the refining
    profession whose recipe outputs it.

    [ES]
    Qué hace: dice de qué oficio sale un material: de recolección (madera, gema en bruto...) o de refinado (tablón...).
    La llaman: branches_of y las pruebas (casi toda receta de fabricación pide materiales de 2 oficios o más).
    Si cambia, afecta: solo la comprobación de "quién necesita a quién".
    """
    pid = gatherer_of(item_id, professions)
    if pid:
        return pid
    for pid, pdef in professions.items():
        if (pdef.get("rare") or {}).get("item") == item_id:
            return pid
    for rdef in recipes.values():
        if item_id in (rdef.get("output") or {}) and professions.get(rdef.get("profession"), {}).get("branch") == "refine":
            return rdef["profession"]
    return None


def branches_of(recipe: dict[str, Any], professions: dict[str, Any], recipes: dict[str, Any]) -> set[str]:
    """The distinct professions that produce a recipe's inputs. [ES] Qué hace: junta los oficios de donde salen los
    materiales de una receta. La llaman: las pruebas. Si cambia, afecta: la regla de "dos oficios o más" (D-109)."""
    return {src for item in (recipe.get("inputs") or {}) if (src := source_of(item, professions, recipes))}


def missing_for(recipe: dict[str, Any], carried: dict[str, int], times: int = 1) -> dict[str, int]:
    """What the hero still lacks to make a recipe `times` times: item id -> missing units (empty = it has it all).

    [ES]
    Qué hace: dice qué falta (y cuánto) para hacer una receta tantas veces con lo que llevas en la mochila.
    La llaman: las pantallas de estación y receta, y _make antes de gastar nada.
    Si cambia, afecta: qué recetas se marcan ✅ y cuándo se rechaza hacer algo.
    """
    need = {item: int(n) * times for item, n in (recipe.get("inputs") or {}).items()}
    return {item: n - carried.get(item, 0) for item, n in need.items() if carried.get(item, 0) < n}


def max_times(recipe: dict[str, Any], carried: dict[str, int], energy: int) -> int:
    """How many times the recipe can be made now with the materials carried and the energy left.

    [ES]
    Qué hace: cuenta cuántas veces alcanza la receta con lo que llevas y tu energía (cada vez cuesta su energía).
    La llaman: la pantalla de receta (botones 🔨 Hacer) y las pruebas.
    Si cambia, afecta: qué botones de hacer se ofrecen.
    """
    inputs = recipe.get("inputs") or {}
    by_items = min((carried.get(item, 0) // int(n) for item, n in inputs.items() if int(n) > 0), default=0)
    cost = int(recipe.get("energy", 1))
    by_energy = energy // cost if cost > 0 else by_items
    return max(0, min(by_items, by_energy))


PERK_KEYS = ("attack", "hp", "armor", "regen", "potion", "bandage", "heal", "bag", "sell", "masterwork", "explore",
             "disenchant")      # [ES] D-115 (fase 2): ✨ Encantamiento, esencias de más al desencantar


def perks(professions: dict[str, Any], ranks: dict[str, int], max_rank: int, armor_type: str | None,
          weapon_type: str | None, role: str | None) -> dict[str, float]:
    """The bonuses a hero gets from its professions (D-111): each perk grows evenly with the rank, up to its value at max_rank.

    Args:
        professions: content/professions.yaml "professions" (each may have a "perk" block).
        ranks: profession id -> the hero's rank, ONLY for professions the hero has started.
        armor_type, weapon_type, role: what the hero wears and plays, for perks limited by "armor", "weapon" or "role".

    [ES]
    Qué hace: suma los beneficios de los oficios del héroe (D-111). Cada beneficio crece parejo con el rango: al
    rango 50 la mitad del valor de la tabla, al 100 el valor entero. Los que dicen "armor", "weapon" o "role" solo
    valen si el héroe lleva esa armadura, pelea con esa arma o juega ese rol (la Herrería, solo con placas; la
    Medicina, solo a los sanadores). Devuelve attack, hp, armor (fracciones), regen, potion, bandage, heal (fracciones
    de más), bag (espacio de mochila de más), sell (monedas de más al vender, 💱 Comercio, D-116), masterwork (solo
    informativo: la probabilidad de obra maestra de la 🪑 Carpintería; la que vale para cada receta la da
    masterwork_chance, porque es del oficio que fabrica, D-116), explore (puntos de exploración de más por
    vuelta, 🧭 Explorador, D-112: el servicio usa la parte entera) y disenchant (fracción de esencias de más al
    desencantar, ✨ Encantamiento, D-115 fase 2: disenchant_amount).
    La llaman: GameService._perks (kit, vida que vuelve, pociones y vendas, mochila) y las pruebas.
    Si cambia, afecta: cuánto ayuda cada oficio en el combate y fuera de él (diseno/07-economia/profesiones.md §0.2).
    """
    out = {k: 0.0 for k in PERK_KEYS}
    for pid, rank in ranks.items():
        perk = (professions.get(pid) or {}).get("perk")
        if not perk or rank <= 0:
            continue
        if "armor_type" in perk and armor_type not in _as_list(perk["armor_type"]):
            continue
        if "weapon_type" in perk and weapon_type not in _as_list(perk["weapon_type"]):
            continue
        share = min(rank, max_rank) / max_rank
        for key in PERK_KEYS:
            if key not in perk:
                continue
            if key == "heal" and "heal_role" in perk and role not in _as_list(perk["heal_role"]):
                continue
            out[key] += float(perk[key]) * share
    return out


MASTERWORK_SUFFIX = "_obra"     # [ES] D-116: id de la obra maestra = id de la pieza + "_obra". Nunca cambia (IDs guardados)


def masterwork_id(item_id: str) -> str:
    """The id of the masterwork twin of a crafted piece. [ES] Qué hace: da el id de la obra maestra de una pieza
    ("artesano_arco_1" → "artesano_arco_1_obra"). La llaman: masterwork_items y el servicio (_make). Si cambia, afecta:
    los ids guardados en las mochilas (nunca se cambia)."""
    return item_id + MASTERWORK_SUFFIX


def masterwork_items(items: dict[str, Any], cfg: dict[str, Any] | None) -> dict[str, Any]:
    """The masterwork twins of every crafted gear piece (D-116), derived when the content loads.

    Each twin keeps the piece's name, emoji, slot, type, tier, rarity and level; every stat is × (1 + stat_bonus), it
    gets the slot's extra bonus (cfg "extra") and costs price_mult times more. It is marked masterwork: true, base: <id>
    and source: masterwork, so it never drops in random loot nor counts as a recipe's output. A twin already written in
    items.yaml wins (it is never overwritten).

    Args:
        items: content/items.yaml (already without retired entries).
        cfg: balance.yaml "masterwork" (stat_bonus, extra, price_mult); None or empty = no masterworks.

    [ES]
    Qué hace: arma, al cargar el contenido, la ✒️ obra maestra de cada pieza de artesano (source: crafted): la misma
    pieza con todos sus bonos × 1,10, un bono más según la ranura (balance.yaml masterwork.extra: defensa en las armas,
    ataque en las armaduras, vida en las joyas) y un precio más alto. Usa el nombre de la pieza (el juego le agrega la
    marca ✒️ y la firma), así no hacen falta textos nuevos. Nunca sale en el botín (source: masterwork).
    La llama: engine/core/content.py (load_content), una vez.
    Si cambia, afecta: cuánto mejor es una obra maestra y cuánto paga el mercader por ella (registro de balance,
    diseno/03-personaje/balance.md); los ids nunca cambian (MASTERWORK_SUFFIX).
    """
    if not cfg:
        return {}
    mult = 1.0 + float(cfg.get("stat_bonus", 0.0))
    extra = cfg.get("extra") or {}
    price_mult = float(cfg.get("price_mult", 1.0))
    out: dict[str, Any] = {}
    for iid, item in items.items():
        if item.get("kind") != "gear" or item.get("source") != "crafted" or item.get("masterwork"):
            continue
        twin_id = masterwork_id(iid)
        if twin_id in items:
            continue
        stats = {stat: round(float(value) * mult, 4) for stat, value in (item.get("stats") or {}).items()}
        for stat, value in (extra.get(item.get("slot")) or {}).items():
            stats[stat] = round(stats.get(stat, 0.0) + float(value), 4)
        twin = dict(item)
        twin.update(source="masterwork", masterwork=True, base=iid, stats=stats,
                    price=max(1, int(round(float(item.get("price", 1)) * price_mult))))
        out[twin_id] = twin
    return out


def masterwork_chance(profession: dict[str, Any], rank: int, max_rank: int, base_chance: float) -> float:
    """Chance that one gear piece made by this profession comes out a masterwork (D-116), growing evenly with the rank.

    The profession's own perk "masterwork" (🪑 Carpintería: 0.15) replaces the base chance of every other gear-crafting
    profession (balance.yaml masterwork.base_chance). The caller only asks for gear that has a masterwork twin.

    [ES]
    Qué hace: da la probabilidad de que una pieza de equipo salga ✒️ obra maestra al fabricarla con este oficio: crece
    pareja con el rango (rango 50 = la mitad). La 🪑 Carpintería usa su beneficio (hasta 15 % al rango 100, en sus
    arcos y bastones); los demás oficios que hacen equipo (Herrería, Sastrería, Peletería, Joyería), la base de
    balance.yaml (hasta 5 %). Las pociones y los muebles nunca salen obra maestra (el servicio no pregunta).
    La llaman: GameService._masterwork_chance (en _make, la receta y ⚒️ Oficios) y las pruebas.
    Si cambia, afecta: cuántas obras maestras entran al juego (registro de balance).
    """
    perk = profession.get("perk") or {}
    top = float(perk["masterwork"]) if "masterwork" in perk else float(base_chance)
    return top * min(max(rank, 0), max_rank) / max_rank


def disenchant_yield(item: dict[str, Any], cfg: dict[str, Any], essence: str = "esencia",
                     major: str = "esencia_mayor") -> dict[str, int]:
    """Essences a gear piece gives when disenchanted, before the Enchanting perk (D-115, phase 2).

    Args:
        item: the gear piece (content/items.yaml; a masterwork twin counts as its rarity).
        cfg: balance.yaml "enchanting" → "disenchant" (by_rarity, per_levels, major_rarities).

    [ES]
    Qué hace: dice cuántas ✨ esencias da una pieza al desencantarla: las de su rareza (común 1 … épica 4) más 1 por cada
    per_levels niveles de la pieza; las 🟣 épicas dan además 1 🔮 esencia mayor. Sin el beneficio del oficio (eso lo
    suma disenchant_amount).
    La llaman: GameService (_disenchant_preview, _disenchant) y las pruebas (la trampa de monedas: lo que dan las esencias
    en el mercader nunca pasa lo que paga por la pieza).
    Si cambia, afecta: cuántas esencias entran al juego (balance.yaml enchanting.disenchant).
    """
    level = int(item.get("req_level", 1))
    count = int((cfg.get("by_rarity") or {}).get(item.get("rarity", "comun"), 1)) + level // max(1, int(cfg.get("per_levels", 20)))
    out = {essence: max(0, count)}
    if item.get("rarity") in (cfg.get("major_rarities") or []):
        out[major] = 1
    return {k: v for k, v in out.items() if v > 0}


def disenchant_amount(base: int, perk: float, roll: float) -> int:
    """Base essences × (1 + perk): the whole part always, one more with the chance of the fraction (roll in [0, 1)).

    [ES]
    Qué hace: aplica el beneficio del ✨ Encantamiento (hasta +30 % al rango 100) a una cantidad de esencias: la parte
    entera siempre y una más con la probabilidad de la fracción (con 3 esencias y +15 %: 3, y 45 % de que sean 4). Así
    el beneficio crece parejo aunque se desencante de a una pieza.
    La llama: GameService._disenchant (un sorteo propio por pieza).
    Si cambia, afecta: cuántas esencias da desencantar con rango.
    """
    total = max(0, base) * (1.0 + max(0.0, perk))
    whole = int(total + 1e-9)
    return whole + (1 if roll < total - whole - 1e-9 else 0)


def enchant_for_slot(slot: str, enchants: dict[str, Any]) -> str | None:
    """Id of the enchantment a gear slot takes (one per slot in the simple layer), or None.

    [ES]
    Qué hace: dice qué encantamiento lleva cada ranura (⚔️ Filo en arma y manos, ❤️ Vigor en pecho, cabeza y piernas,
    🛡️ Guarda en pies y joya; balance.yaml enchanting.enchants "slots"). En la capa simple el jugador no elige.
    La llaman: GameService (_enchant_view, _enchant) y las pruebas.
    Si cambia, afecta: qué bono puede tener cada pieza.
    """
    for eid, edef in enchants.items():
        if slot in (edef.get("slots") or []):
            return eid
    return None


def enchant_value(edef: dict[str, Any], rank: int, max_rank: int) -> float:
    """The enchantment's value at an Enchanting rank: evenly from "min" (rank 1) to "max" (max_rank), in whole points.

    The value is rounded half up to a whole point (0.01 = 1 % or 1 of armor), so what the player sees is what it gives and a
    new enchantment is only "better" when it shows a higher number.

    [ES]
    Qué hace: da cuánto suma un encantamiento hecho con tu rango: parejo desde "min" en el rango 1 hasta "max" en el 100,
    redondeado a puntos enteros (⚔️ Filo y ❤️ Vigor: +1 % hasta el rango 25, +2 % del 26 al 75 y +3 % del 76 al 100;
    🛡️ Guarda: +1 de defensa hasta el 50 y +2 desde el 51). El valor queda guardado en la pieza al encantar: subir de rango
    después no lo cambia (se puede volver a encantar para mejorarlo, cuando el número sube).
    La llaman: GameService (_enchant_view, _enchant) y las pruebas.
    Si cambia, afecta: cuánto ayuda cada encantamiento (balance.yaml enchanting.enchants).
    """
    low, high = float(edef.get("min", 0.0)), float(edef.get("max", 0.0))
    share = (min(max(rank, 1), max_rank) - 1) / max(1, max_rank - 1)
    return math.floor((low + (high - low) * share) * 100 + 0.5 + 1e-9) / 100


def enchant_cost(item: dict[str, Any], edef: dict[str, Any], cfg: dict[str, Any], essence: str = "esencia",
                 major: str = "esencia_mayor") -> dict[str, int]:
    """What enchanting this piece takes: essences by the piece's level, a major essence from a level and the material.

    Args:
        item: the gear piece to enchant.
        edef: the enchantment (balance.yaml enchanting.enchants.<id>: its "material").
        cfg: balance.yaml "enchanting" → "enchant" (essences, essences_per_levels, major_from_level, material_per_levels).

    [ES]
    Qué hace: dice qué pide encantar una pieza: ✨ esencias (3 y 1 más cada 10 niveles de la pieza), 🔮 1 esencia mayor si la
    pieza es de nivel 50 o más, y el material del encantamiento (🔩 lingote, 🧴 extracto o 💠 gema: 1 y 1 más cada 50
    niveles). Así encantar lo mejor del juego gasta mucho equipo viejo (el sumidero) y pide a otros oficios.
    La llaman: GameService (_enchant_view, _enchant) y las pruebas.
    Si cambia, afecta: cuánto equipo y material se gasta al encantar (balance.yaml enchanting.enchant).
    """
    level = int(item.get("req_level", 1))
    cost = {essence: int(cfg.get("essences", 3)) + level // max(1, int(cfg.get("essences_per_levels", 10)))}
    if level >= int(cfg.get("major_from_level", 10 ** 9)):
        cost[major] = 1
    material = edef.get("material")
    if material:
        cost[material] = cost.get(material, 0) + 1 + level // max(1, int(cfg.get("material_per_levels", 50)))
    return cost


def _as_list(value: Any) -> list[Any]:
    return list(value) if isinstance(value, (list, tuple)) else [value]

