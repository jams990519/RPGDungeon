"""Chained professions, phase 1 (D-109): ranks from profession xp, who produces each material, recipe checks.

Pure helpers over content/professions.yaml and balance.yaml "professions". They never touch the store: the
service keeps every hero's profession xp in Hero.professions (profession id -> xp) and calls these functions.

[ES]
Para qué sirve: las cuentas de los oficios encadenados (recolectar → refinar → fabricar): el rango de 1 a 100 que
sale de la experiencia de cada oficio, su título (Aprendiz, Oficial...), qué oficio produce cada material (para
comprobar que casi toda receta pide materiales de dos oficios o más), qué falta para una receta y cuántas veces
alcanza con lo que llevas y tu energía. No guarda nada: el servicio lee Hero.professions y llama a estas funciones.
Documento de diseño: diseno/07-economia/profesiones.md §0 (fase 1, D-109) y §4 (rangos)
Módulo: M14 Oficios
Depende de: ninguno (los datos llegan de content/professions.yaml y de content/balance.yaml, bloque professions)
Lo usan: engine/service/game.py (sección "professions"), tests/test_professions.py
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno (la experiencia de oficio se guarda en Hero.professions)
Reglas que nunca se rompen:
    1. El rango nunca baja: sale solo de la experiencia acumulada, que nunca se resta.
    2. Sin tope de oficios (D-57): cualquiera puede subir todos; el freno es el tiempo, los materiales y la estación.
    3. Una receta se hace entera o no se hace: nunca se gasta la mitad de los materiales.
Si cambias esto, revisa:
    - La curva (balance.yaml professions.rank_formula): cuánto tarda el rango 100 (~1 año dedicado, profesiones.md §4)
    - Servicio: engine/service/game.py (_prof_rank, _trade_gather, _trade_loot, _station_view, _recipe_view, _make)
    - Pruebas: tests/test_professions.py
"""

from __future__ import annotations

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


PERK_KEYS = ("attack", "hp", "armor", "regen", "potion", "bandage", "heal", "bag", "sell")


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
    de más), bag (espacio de mochila de más) y sell (monedas de más al vender, 💱 Comercio, D-116).
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


def _as_list(value: Any) -> list[Any]:
    return list(value) if isinstance(value, (list, tuple)) else [value]

