"""Chained professions, phase 1 (D-109): ranks from profession xp, who produces each material, recipe checks,
perks (D-111), masterworks (D-116) and the camp perks of phase 2 (D-115, D-116).

Pure helpers over content/professions.yaml and balance.yaml "professions" / "masterwork". They never touch the store:
the service keeps every hero's profession xp in Hero.professions (profession id -> xp) and calls these functions.

[ES]
Para qué sirve: las cuentas de los oficios encadenados (recolectar → refinar → fabricar): el rango de 1 a 100 que
sale de la experiencia de cada oficio, su título (Aprendiz, Oficial...), qué oficio produce cada material (para
comprobar que casi toda receta pide materiales de dos oficios o más), qué falta para una receta y cuántas veces
alcanza con lo que llevas y tu energía. También el beneficio de cada oficio (D-111) y la ✒️ obra maestra (D-116):
las piezas gemelas "obra maestra" que se arman al cargar el contenido (masterwork_items) y la probabilidad de que
una pieza fabricada salga así (masterwork_chance). Fase 2, lado del campamento (D-115, D-116): los beneficios de
campamento y castillo (🎣 Pescador, 🍲 Cocina, Cantería, 🏗️ Construcción) no son de cada héroe: valen para el campamento
donde es miembro, con el MEJOR rango entre sus miembros (camp_best_ranks, camp_perks), y bajan lo que piden las obras
(scaled_cost). No guarda nada: el servicio lee Hero.professions y llama a estas funciones.
Documento de diseño: diseno/07-economia/profesiones.md §0 (fase 1, D-109), §0.2 (beneficios), §0.4 (obra maestra y
    beneficios de campamento) y §4; diseno/07-economia/red-de-oficios.md §5 (fase 2)
Módulo: M14 Oficios
Depende de: ninguno (los datos llegan de content/professions.yaml y de content/balance.yaml, bloques professions y
    masterwork)
Lo usan: engine/service/game.py (secciones "professions" y "camp professions, phase 2"), engine/core/content.py
    (masterwork_items, al cargar los objetos), tests/test_professions.py, tests/test_masterwork.py y
    tests/test_oficios_campamento.py
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno (la experiencia de oficio se guarda en Hero.professions)
Reglas que nunca se rompen:
    1. El rango nunca baja: sale solo de la experiencia acumulada, que nunca se resta.
    2. Sin tope de oficios (D-57): cualquiera puede subir todos; el freno es el tiempo, los materiales y la estación.
    3. Una receta se hace entera o no se hace: nunca se gasta la mitad de los materiales.
    4. Los ids de obra maestra son el id de la pieza + MASTERWORK_SUFFIX ("_obra") y quedan guardados en las mochilas:
       el sufijo nunca cambia (IDs estables). Una obra maestra nunca sale en el botín al azar (source: masterwork).
    5. Un beneficio de campamento (CAMP_PERK_KEYS) nunca se suma entre miembros: rige el mejor rango de cada oficio, así
       un campamento grande no rinde más por tener muchos cocineros. Una obra nunca pide menos de 1 de cada cosa.
Si cambias esto, revisa:
    - La curva (balance.yaml professions.rank_formula): cuánto tarda el rango 100 (~1 año dedicado, profesiones.md §4)
    - Servicio: engine/service/game.py (_prof_rank, _trade_gather, _trade_loot, _station_view, _recipe_view, _make)
    - Obra maestra (D-116): balance.yaml masterwork (bono, bono de más por ranura, precio y probabilidad base) y el
      perk {masterwork} de la 🪑 Carpintería en content/professions.yaml; el servicio la sortea en _make
    - Beneficios (perks): una clave nueva va en PERK_KEYS, en el texto prof.perk.<clave> y donde el servicio la use. D-112:
      "explore" (🧭 Explorador) son puntos de exploración por vuelta (game.py _explore_step usa la parte entera)
    - D-115 fase 2: las claves de campamento (CAMP_PERK_KEYS: fish_food, cook_food, stone_cost, build_cost, repair_cost)
      las usa el servicio en _camp_feed (despensa), _upgrade_need (obras) y _repair_need (reparar las defensas)
    - Pruebas: tests/test_professions.py, tests/test_masterwork.py, tests/test_enemy_camps.py,
      tests/test_oficios_campamento.py
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
             "fish_food", "cook_food", "stone_cost", "build_cost", "repair_cost")      # D-115 phase 2: the camp perks (last 5)
# [ES] D-115/D-116: los beneficios de campamento y castillo. No son del héroe: rige el mejor rango entre los miembros del
# campamento (camp_perks). fish_food y cook_food = raciones de más en la despensa (fracción); stone_cost, build_cost y
# repair_cost = cuánto menos piden las obras de piedra, todas las obras y la reparación de las defensas (fracción).
CAMP_PERK_KEYS = ("fish_food", "cook_food", "stone_cost", "build_cost", "repair_cost")


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
    masterwork_chance, porque es del oficio que fabrica, D-116) y explore (puntos de exploración de más por
    vuelta, 🧭 Explorador, D-112: el servicio usa la parte entera). D-115: también las claves de campamento
    (CAMP_PERK_KEYS) con el rango propio, solo para mostrarlas: las que valen son las del mejor miembro (camp_perks).
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


def camp_perk_professions(professions: dict[str, Any]) -> list[str]:
    """Ids of the professions whose perk is a camp perk (D-115 phase 2), in catalog order. [ES] Qué hace: dice qué oficios
    dan un beneficio de campamento o castillo (🎣 Pescador, 🍲 Cocina, Cantería, 🏗️ Construcción). La llaman: el servicio
    (_camp_perks, ⚒️ Oficios) y camp_best_ranks. Si cambia, afecta: qué oficios cuentan para el campamento."""
    return [pid for pid, pdef in professions.items() if any(key in (pdef.get("perk") or {}) for key in CAMP_PERK_KEYS)]


def camp_best_ranks(professions: dict[str, Any], members: dict[str, dict[str, int]]) -> dict[str, tuple[int, str]]:
    """For every camp-perk profession, the best rank among the camp's members and who holds it (D-115 phase 2).

    Args:
        professions: content/professions.yaml "professions".
        members: member name -> {profession id: rank}, ONLY for professions the member has started.

    Returns:
        profession id -> (best rank, member name); professions nobody started are left out. On a tie, the first member
        in the given order keeps it (the service passes the members in camp order: the founder first).

    [ES]
    Qué hace: para cada oficio con beneficio de campamento, busca el mejor rango entre los miembros y quién lo tiene. Los
    beneficios de campamento no se suman entre miembros: rige el mejor (simple y justo: un campamento grande no rinde más
    por tener diez cocineros, y el que se dedica es el que hace la diferencia).
    La llaman: GameService._camp_perks y las pruebas.
    Si cambia, afecta: cuánto rinden la despensa y las obras de cada campamento.
    """
    best: dict[str, tuple[int, str]] = {}
    for pid in camp_perk_professions(professions):
        for name, ranks in members.items():
            rank = int(ranks.get(pid, 0))
            if rank > 0 and (pid not in best or rank > best[pid][0]):
                best[pid] = (rank, name)
    return best


def camp_perks(professions: dict[str, Any], best: dict[str, tuple[int, str]], max_rank: int) -> dict[str, tuple[float, str | None]]:
    """The camp perks from the best ranks (camp_best_ranks): key -> (value, member who gives it), growing evenly with rank.

    [ES]
    Qué hace: convierte los mejores rangos en los beneficios de campamento (CAMP_PERK_KEYS): cada uno crece parejo con el
    rango, como los demás beneficios (rango 50 = la mitad del valor de content/professions.yaml). Devuelve también quién lo
    da, para mostrarlo en el campamento. Una clave sin nadie que la dé vale (0.0, None).
    La llaman: GameService._camp_perks (despensa, obras, reparación, pantallas) y las pruebas.
    Si cambia, afecta: cuánto rinden la despensa y las obras de cada campamento.
    """
    out: dict[str, tuple[float, str | None]] = {key: (0.0, None) for key in CAMP_PERK_KEYS}
    for pid, (rank, name) in best.items():
        perk = (professions.get(pid) or {}).get("perk") or {}
        share = min(rank, max_rank) / max_rank
        for key in CAMP_PERK_KEYS:
            if key in perk and float(perk[key]) * share > out[key][0]:
                out[key] = (float(perk[key]) * share, name)
    return out


def scaled_cost(cost: dict[str, int], cut: float, stone_cut: float = 0.0,
                stone_items: tuple[str, ...] | list[str] = ()) -> dict[str, int]:
    """A materials cost after the camp perks: every material × (1 − cut), stone ones also × (1 − stone_cut), rounded up,
    never below 1. "coins" are never cut (they are not a material).

    [ES]
    Qué hace: baja lo que pide una obra (o una reparación) con los beneficios del campamento: todo × (1 − cut) (🏗️
    Construcción) y lo de piedra (stone_items: piedra y sillar) además × (1 − stone_cut) (Cantería). Redondea hacia arriba
    y nunca deja menos de 1 de cada cosa; las monedas no se tocan.
    La llaman: GameService._upgrade_need y _repair_need, y las pruebas.
    Si cambia, afecta: cuánto cuestan las mejoras y las reparaciones de los campamentos con esos oficios.
    """
    out: dict[str, int] = {}
    for key, n in cost.items():
        n = int(n)
        if key == "coins" or n <= 0:
            out[key] = n
            continue
        mult = max(0.0, 1.0 - cut) * (max(0.0, 1.0 - stone_cut) if key in stone_items else 1.0)
        out[key] = max(1, math.ceil(n * mult - 1e-9))
    return out


def refined_from(professions: dict[str, Any], recipes: dict[str, Any]) -> dict[str, tuple[str, int]]:
    """Refined material -> (raw material, units per refined unit), from the refining recipes with one input and one
    output (🧱 sillar ← 🪨 piedra ×3, 🟫 tablón ← 🪵 madera ×3).

    [ES]
    Qué hace: dice de qué material crudo sale cada refinado simple y cuántas unidades lleva (sillar = 3 piedras). El
    servicio lo usa para que lo crudo que ya se aportó de más a una obra (porque la obra ahora pide refinados, D-115)
    cuente como refinado, y para la experiencia de 🏗️ Construcción (un refinado vale lo que lleva).
    La llaman: GameService._credit_raw y _build_xp.
    Si cambia, afecta: solo esas dos cuentas.
    """
    out: dict[str, tuple[str, int]] = {}
    for rdef in recipes.values():
        if rdef.get("retired") or (professions.get(rdef.get("profession")) or {}).get("branch") != "refine":
            continue
        inputs, output = rdef.get("inputs") or {}, rdef.get("output") or {}
        if len(inputs) == 1 and len(output) == 1 and int(next(iter(output.values()))) == 1:
            raw, n = next(iter(inputs.items()))
            out.setdefault(next(iter(output)), (raw, int(n)))
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


def _as_list(value: Any) -> list[Any]:
    return list(value) if isinstance(value, (list, tuple)) else [value]

