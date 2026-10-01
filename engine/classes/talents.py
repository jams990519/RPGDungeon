"""Talent points, unlocks, the 3-slot bar and the effective combat kit of a hero.

[ES]
Para qué sirve: calcular qué habilidades tiene cada héroe según sus puntos, armar su barra de 3
y devolver el "kit" (clase + habilidades + mejoras pasivas) que usa el combate.
Documento de diseño: diseno/03-personaje/talentos.md (D-68)
Módulo: M3 Clases y talentos
Depende de: content/classes.yaml (group, role, abilities), content/balance.yaml (talents)
Lo usan: engine/service/game.py
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno (lee y cambia campos del héroe que le pasa el servicio)
Reglas que nunca se rompen:
    1. bar() siempre incluye una respuesta si el héroe tiene alguna desbloqueada.
Si cambias esto, revisa:
    - Combate: engine/combat/engine.py recibe el kit como class_def
    - Pruebas: tests/test_talents.py
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
    """Points in a spec needed to unlock its 1st, 2nd and 3rd ability. [ES] Qué hace: dice cuántos puntos pide cada habilidad. La llaman: el servicio. Si cambia, afecta: el ritmo de desbloqueo."""
    return list(balance["talents"]["unlock"])


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
    new = []
    for index, need in enumerate(unlock_points(balance)):
        abilities = classes[spec]["abilities"]
        if index < len(abilities) and hero.talents[spec] >= need and abilities[index]["id"] not in hero.unlocked:
            hero.unlocked.append(abilities[index]["id"])
            new.append(abilities[index]["id"])
    best = max(hero.talents.items(), key=lambda kv: kv[1])
    if best[1] > hero.talents.get(hero.class_id, 0):
        hero.class_id = best[0]
    return new


def bar(classes: dict[str, Any], hero: Hero) -> list[dict[str, Any]]:
    """The 3 abilities in use: the latest unlocked, always keeping one response.

    [ES]
    Qué hace: arma la barra de 3 habilidades con las últimas desbloqueadas, sin quedarse nunca sin respuesta.
    La llaman: kit() y la vista del héroe.
    Si cambia, afecta: qué botones salen en combate.
    """
    known = _abilities(classes, _group(classes, hero))
    unlocked = [a for a in hero.unlocked if a in known]
    chosen = unlocked[-3:]
    if not any(known[a][2]["kind"] == "response" for a in chosen):
        responses = [a for a in unlocked if known[a][2]["kind"] == "response"]
        if responses:
            chosen = ([responses[-1]] + chosen)[:3] if len(chosen) < 3 else [responses[-1]] + chosen[1:]
    return [known[a][2] for a in chosen]


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
