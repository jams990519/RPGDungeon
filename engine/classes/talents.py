"""Talent points, unlocks, the 3-slot bar and the effective combat kit of a hero.

[ES]
Para qué sirve: calcular qué habilidades tiene cada héroe según sus puntos (8 por especialización,
repartidas en los 100 niveles), armar su barra de 3 (elegida por el jugador o automática) y devolver
el "kit" (clase + habilidades + mejoras pasivas) que usa el combate.
Documento de diseño: diseno/03-personaje/talentos.md (D-68, D-79)
Módulo: M3 Clases y talentos
Depende de: content/classes.yaml (group, role, abilities), content/balance.yaml (talents)
Lo usan: engine/service/game.py
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno (lee y cambia hero.talents, hero.points, hero.unlocked y hero.bar)
Reglas que nunca se rompen:
    1. bar() siempre pone una respuesta en la casilla 1 si el héroe tiene alguna desbloqueada.
    2. Un héroe nunca pierde una habilidad desbloqueada (salvo al reiniciar talentos o si su especialización se retira).
    3. Una barra guardada que ya no vale (hero.bar) no rompe nada: se usa la barra automática.
Si cambias esto, revisa:
    - Combate: engine/combat/engine.py recibe el kit como class_def (el orden de la barra es el de los botones)
    - Servicio: engine/service/game.py (pantallas 🌟 Talentos y 🎛️ Barra de combate)
    - D-110: la barra automática de Defensa guarda su curación más nueva en la casilla 3 (HEAL_FIRST_ROLES); la mejora
      pasiva puede traer armor (talents.passive.defensa), que hero_stats suma a la armadura (tools/balance_report.py)
    - Pruebas: tests/test_talents.py, tests/test_spec_abilities.py, tests/test_balance_d110.py
"""

from __future__ import annotations

import copy
from typing import Any

from engine.hero.hero import Hero


def specs_of(classes: dict[str, Any], group: str) -> list[str]:
    """Spec ids of a class, in content order. [ES] Qué hace: lista las especializaciones de una clase. La llaman: el servicio. Si cambia, afecta: el orden en pantalla."""
    return [cid for cid, c in classes.items() if c.get("group", cid) == group and not c.get("retired")]


def default_spec(classes: dict[str, Any], group: str) -> str:
    """First spec of a class: the hero's starting point. [ES] Qué hace: da la especialización inicial de una clase. La llaman: la creación de héroe. Si cambia, afecta: los héroes nuevos."""
    return specs_of(classes, group)[0]


def base_response(classes: dict[str, Any], group: str) -> str:
    """The free starting response of a class (first response of its first spec). [ES] Qué hace: da la respuesta defensiva con la que empieza la clase. La llaman: la creación de héroe. Si cambia, afecta: el kit inicial."""
    for ability in classes[default_spec(classes, group)]["abilities"]:
        if ability["kind"] == "response":
            return ability["id"]
    return classes[default_spec(classes, group)]["abilities"][0]["id"]


def _abilities(classes: dict[str, Any], group: str) -> dict[str, tuple[str, int, dict[str, Any]]]:
    out = {}
    for spec in specs_of(classes, group):
        for index, ability in enumerate(classes[spec]["abilities"]):
            out[ability["id"]] = (spec, index, ability)
    return out


def unlock_points(balance: dict[str, Any]) -> list[int]:
    """Points in a spec needed to unlock each of its abilities, in order (8 values). [ES] Qué hace: dice cuántos puntos pide cada habilidad. La llaman: el servicio y spend_point. Si cambia, afecta: el ritmo de desbloqueo."""
    return list(balance["talents"]["unlock"])


def _unlock_spec(classes: dict[str, Any], balance: dict[str, Any], hero: Hero, spec: str) -> list[str]:
    """Unlock every ability of a spec the hero's points there already pay for; returns the new ids."""
    new = []
    abilities = classes[spec]["abilities"]
    for index, need in enumerate(unlock_points(balance)):
        if index < len(abilities) and hero.talents.get(spec, 0) >= need and abilities[index]["id"] not in hero.unlocked:
            hero.unlocked.append(abilities[index]["id"])
            new.append(abilities[index]["id"])
    return new


def _group(classes: dict[str, Any], hero: Hero) -> str:
    return classes[hero.class_id].get("group", hero.class_id)


def ensure_talents(classes: dict[str, Any], balance: dict[str, Any], hero: Hero) -> None:
    """Initialise or migrate a hero to the talent system (heroes made before it keep their progress).

    [ES]
    Qué hace: prepara los talentos de un héroe; a los héroes viejos les da los puntos que les
    corresponden por nivel, puestos en su especialización actual.
    La llaman: el servicio al cargar un héroe.
    Si cambia, afecta: los héroes guardados.
    """
    group = _group(classes, hero)
    if classes.get(hero.class_id, {}).get("retired"):
        # The spec was retired (D-69): move to the class's first spec and refund its points.
        hero.points += hero.talents.pop(hero.class_id, 0)
        hero.class_id = default_spec(classes, group)
        retired_ids = {a["id"] for cid, c in classes.items() if c.get("retired") for a in c["abilities"]}
        hero.unlocked = [a for a in hero.unlocked if a not in retired_ids]
    if hero.unlocked:
        # Heroes saved before abilities 4-8 existed (D-79): unlock what their points already pay for.
        for spec in specs_of(classes, group):
            if hero.talents.get(spec):
                _unlock_spec(classes, balance, hero, spec)
        return
    hero.unlocked = [base_response(classes, group)]
    if hero.level > 1 and not hero.talents:
        for _ in range(hero.level - 1):
            hero.points += 1
            spend_point(classes, balance, hero, hero.class_id)


def spend_point(classes: dict[str, Any], balance: dict[str, Any], hero: Hero, spec: str) -> list[str]:
    """Put one point in a spec of the hero's class; returns newly unlocked ability ids.

    [ES]
    Qué hace: gasta un punto en una especialización, desbloquea habilidades y actualiza la
    especialización principal.
    La llaman: el servicio (botón ➕) y la migración de héroes viejos.
    Si cambia, afecta: el poder de cada héroe.
    """
    group = _group(classes, hero)
    if hero.points <= 0 or spec not in specs_of(classes, group):
        return []
    hero.points -= 1
    hero.talents[spec] = hero.talents.get(spec, 0) + 1
    new = _unlock_spec(classes, balance, hero, spec)
    best = max(hero.talents.items(), key=lambda kv: kv[1])
    if best[1] > hero.talents.get(hero.class_id, 0):
        hero.class_id = best[0]
    return new


def _is_response(ability: dict[str, Any]) -> bool:
    return ability["kind"] == "response"


def _known_unlocked(classes: dict[str, Any], hero: Hero) -> tuple[dict[str, tuple[str, int, dict[str, Any]]], list[str]]:
    known = _abilities(classes, _group(classes, hero))
    return known, [a for a in dict.fromkeys(hero.unlocked) if a in known]


DAMAGE_KINDS = ("strike", "finisher", "dot")


HEAL_FIRST_ROLES = ("defensa",)    # D-110: a tank's automatic bar keeps a heal in slot 3


def _auto_slots(known: dict[str, Any], unlocked: list[str], role: str | None = None) -> list[str]:
    """Automatic bar: newest response, newest damage ability (strike, finisher or dot), newest other one.

    D-110: for Defensa the third slot is the newest heal when one is unlocked (a tank whose
    automatic bar dropped its heal for a newer utility could not hold out, which is its role).
    """
    responses = [a for a in unlocked if _is_response(known[a][2])]
    if not responses:
        return unlocked[-3:]
    chosen = [responses[-1]]
    damage = [a for a in unlocked if known[a][2]["kind"] in DAMAGE_KINDS]
    if damage:
        chosen.append(damage[-1])
    heals = [a for a in unlocked if known[a][2]["kind"] == "heal" and a not in chosen]
    if role in HEAL_FIRST_ROLES and heals:
        chosen.append(heals[-1])
    for pool in ([a for a in unlocked if not _is_response(known[a][2])], unlocked):
        for ability_id in reversed(pool):
            if len(chosen) < 3 and ability_id not in chosen:
                chosen.append(ability_id)
    return chosen


def bar_slots(classes: dict[str, Any], hero: Hero) -> list[str]:
    """Ability ids of the bar, slot 1 first (slot 1 = a response).

    [ES]
    Qué hace: devuelve la barra en uso: la que eligió el jugador (hero.bar) si sigue valiendo; si no,
    la automática (casilla 1 = la respuesta más nueva, casilla 2 = el golpe más nuevo, casilla 3 = la otra
    habilidad más nueva; D-110: en Defensa, la curación más nueva, si ya abrió alguna).
    Si la barra elegida tiene casillas vacías y hay habilidades libres, las llena con las últimas.
    La llaman: bar(), el servicio (pantalla 🎛️ Barra de combate) y set_bar_slot().
    Si cambia, afecta: qué botones salen en combate y en qué orden.
    """
    known, unlocked = _known_unlocked(classes, hero)
    auto = _auto_slots(known, unlocked, classes.get(hero.class_id, {}).get("role"))
    saved = list(hero.bar or [])
    has_response = any(_is_response(known[a][2]) for a in unlocked)
    valid = (
        bool(saved)
        and len(saved) <= 3
        and len(set(saved)) == len(saved)
        and all(a in unlocked for a in saved)
        and (not has_response or _is_response(known[saved[0]][2]))
    )
    if not valid:
        return auto
    latest = list(reversed(unlocked))
    for ability_id in [a for a in latest if not _is_response(known[a][2])] + latest:
        if len(saved) >= min(3, len(unlocked)):
            break
        if ability_id not in saved:
            saved.append(ability_id)
    return saved


def bar(classes: dict[str, Any], hero: Hero) -> list[dict[str, Any]]:
    """The (up to) 3 abilities in use, slot 1 first.

    [ES]
    Qué hace: arma la barra de 3 habilidades (ver bar_slots); la casilla 1 es siempre una respuesta.
    La llaman: kit() y la vista del héroe.
    Si cambia, afecta: qué botones salen en combate.
    """
    known = _abilities(classes, _group(classes, hero))
    return [known[a][2] for a in bar_slots(classes, hero)]


def bar_choices(classes: dict[str, Any], hero: Hero, slot: int) -> list[str]:
    """Unlocked ability ids that can go in a bar slot (1-3), excluding what is already there.

    [ES]
    Qué hace: lista lo que se puede poner en una casilla: en la 1, solo respuestas; en la 2 y la 3,
    cualquier otra habilidad desbloqueada que no esté en la casilla 1.
    La llaman: el servicio (pantalla para elegir casilla).
    Si cambia, afecta: qué opciones ve el jugador.
    """
    known, unlocked = _known_unlocked(classes, hero)
    slots = bar_slots(classes, hero)
    current = slots[slot - 1] if 0 < slot <= len(slots) else None
    if slot == 1:
        return [a for a in unlocked if _is_response(known[a][2]) and a != current]
    first = slots[0] if slots else None
    return [a for a in unlocked if a not in (current, first)]


def set_bar_slot(classes: dict[str, Any], hero: Hero, slot: int, ability_id: str) -> bool:
    """Put an unlocked ability in a slot (1-3); swaps if it already sits in another slot. Returns True if done.

    [ES]
    Qué hace: guarda la elección del jugador en hero.bar. Si la habilidad ya estaba en otra casilla,
    las cambia de lugar. Nunca deja la casilla 1 sin respuesta.
    La llaman: el servicio (botones de la pantalla 🎛️ Barra de combate).
    Si cambia, afecta: la barra guardada de cada héroe.
    """
    if not 1 <= slot <= 3 or ability_id not in bar_choices(classes, hero, slot):
        return False
    slots = bar_slots(classes, hero)
    if slot > len(slots):
        slots.append(ability_id)
    else:
        old = slots[slot - 1]
        if ability_id in slots:
            slots[slots.index(ability_id)] = old
        slots[slot - 1] = ability_id
    hero.bar = slots
    return True


def kit(classes: dict[str, Any], balance: dict[str, Any], hero: Hero) -> dict[str, Any]:
    """Effective class definition for combat and stats: main spec + bar + passive bonuses.

    [ES]
    Qué hace: devuelve la "clase efectiva" del héroe: recurso y estadísticas de su especialización
    principal, su barra de habilidades y las mejoras pasivas de sus puntos.
    La llaman: el servicio (combate, vida máxima, vistas).
    Si cambia, afecta: todo el combate del héroe.
    """
    base = copy.deepcopy(classes[hero.class_id])
    base["abilities"] = bar(classes, hero)
    cfg = balance["talents"]
    bonus = {"attack": 0.0, "hp": 0.0}
    for spec, points in hero.talents.items():
        role = classes.get(spec, {}).get("role", "ataque")
        for stat, per_point in cfg["passive"].get(role, {}).items():
            bonus[stat] = bonus.get(stat, 0.0) + per_point * min(points, cfg["passive_cap"])
    base["talent_bonus"] = bonus
    return base
