"""Story and roleplay, simple layer (D-117, provisional): the pure rules.

Missions are lists of steps; each step has one goal. A goal either counts game events (explore, gather, win,
craft, sell, visit, talk, feed, build) or checks the hero's state (a zone explored to a %, having a camp, a level).
Named characters pick a greeting line by conditions (missions done, decisions taken, reputation rank). Daily
tasks rotate by real day (one per faction, from the world seed) and camp tasks by week. Reputation turns into
ranks. These helpers are pure: the service (engine/service/story.py) reads the store and the hero and calls them.

[ES]
Para qué sirve: las cuentas de la historia y el rol: cuánto avanza un objetivo con cada cosa que haces en el juego,
cuándo un objetivo de estado ya se cumple, qué saludo dice cada personaje según lo que hiciste y elegiste, qué
encargos tocan hoy (uno por facción) y esta semana en cada campamento, el rango de reputación y la biografía limpia.
Documento de diseño: diseno/06-contenido/historia-y-rol.md §1 (capa simple) y "En el juego"
Módulo: M10 Misiones (personajes, facciones y diario: M2 Héroe y M15 Social; el código vive en engine/service/story.py)
Depende de: engine.core.rng.hash_unit (sorteo fijo de los encargos); los datos llegan de content/story.yaml y los
    números de content/balance.yaml (bloque story)
Lo usan: engine/service/story.py (StoryMixin)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno
Reglas que nunca se rompen:
    1. Un objetivo solo cuenta lo que pasa desde que es el paso actual (salvo los de estado, que miran cómo está el héroe).
    2. Los encargos del día son los mismos para todos y salen de la semilla del mundo y del día: nadie los elige ni los cambia.
    3. Un objetivo que no se entiende (tipo nuevo, datos viejos) nunca avanza ni rompe nada.
Si cambias esto, revisa:
    - Servicio: engine/service/story.py (_quest_progress, _daily_event, _camp_event, _npc_line)
    - Datos: content/story.yaml (tipos de objetivo y condiciones de los saludos)
    - Pruebas: tests/test_story.py
"""

from __future__ import annotations

import re
import unicodedata
from typing import Any

from engine.core.rng import hash_unit

# Goals that look at the hero's state instead of counting events. [ES] Objetivos de estado: se cumplen solos si ya está.
STATE_GOALS = ("explored", "camp", "level")
# Goals that count game events. [ES] Objetivos que cuentan cosas que pasan en el juego.
EVENT_GOALS = ("talk", "deliver", "explore", "gather", "win", "guardian", "craft", "sell", "visit", "feed", "build", "choice")


def target(goal: dict[str, Any]) -> int:
    """How much a goal needs (n, default 1). [ES] Qué hace: cuánto pide un objetivo (n; 1 si no dice). La llama: el servicio. Si cambia, afecta: cuándo se cumple cada paso."""
    if goal.get("kind") in STATE_GOALS or goal.get("kind") in ("talk", "deliver", "choice", "visit", "guardian"):
        return 1
    return max(1, int(goal.get("n", 1)))


def amount(goal: dict[str, Any], kind: str, data: dict[str, Any]) -> int:
    """How much one game event advances a goal (0 if it does not count).

    Args:
        goal: the step goal from content/story.yaml (with a resolved "npc").
        kind: the event ("explore", "gather", "win", "craft", "sell", "visit", "talk", "feed", "build", "choice").
        data: the event's facts (see engine/service/story.py _story_event).

    [ES]
    Qué hace: dice cuánto suma una cosa que pasó en el juego a un objetivo. Explorar suma 1 por vuelta (con
    "claro: true", solo explorando desde el Claro; con "outside: true", solo fuera de él). Recolectar suma las
    unidades del material pedido (o todas). Ganar suma 1 si la pelea cumple el bioma o es una presa de 🏹 Cazar,
    si así lo pide. Fabricar suma las veces hechas; vender, las cosas vendidas; llegar a un lugar, 1 si es el pedido
    (la guarida, una Lejanía o unas coordenadas); hablar, 1 con el personaje justo; aportar a la despensa, las
    raciones; aportar a una obra, los materiales.
    La llaman: el servicio, para las misiones, los encargos del día y los del campamento.
    Si cambia, afecta: el avance de todas las misiones y encargos.
    """
    want = goal.get("kind")
    if want == "explore" and kind == "explore":
        if goal.get("claro") and (data.get("x"), data.get("y")) != (0, 0):
            return 0
        if goal.get("outside") and int(data.get("lejania", 0)) < 1:
            return 0
        return 1
    if want == "gather" and kind == "gather":
        items = data.get("items") or {}
        item = goal.get("item")
        return int(items.get(item, 0)) if item else int(sum(items.values()))
    if want == "win" and kind == "win":
        if goal.get("hunt") and not data.get("hunt"):
            return 0
        if goal.get("biomes") and data.get("biome") not in goal["biomes"]:
            return 0
        return 1
    if want == "guardian" and kind == "win":
        if not data.get("boss"):
            return 0
        return 1 if not goal.get("enemy") or goal["enemy"] == data.get("enemy") else 0
    if want == "craft" and kind == "craft":
        if goal.get("profession") and goal["profession"] != data.get("profession"):
            return 0
        if goal.get("recipe") and goal["recipe"] != data.get("recipe"):
            return 0
        return max(1, int(data.get("n", 1)))
    if want == "sell" and kind == "sell":
        return int(data.get("n", 0))
    if want == "visit" and kind == "visit":
        if goal.get("lair"):
            return 1 if data.get("lair") else 0
        if "zone" in goal:
            return 1 if [data.get("x"), data.get("y")] == list(goal["zone"]) else 0
        return 1 if int(data.get("lejania", 0)) >= int(goal.get("lejania", 1)) else 0
    if want in ("talk", "deliver") and kind == "talk":
        return 1 if goal.get("npc") == data.get("npc") else 0
    if want == "feed" and kind == "feed":
        return int(data.get("rations", 0))
    if want == "build" and kind == "build":
        return int(data.get("n", 0))
    if want == "choice" and kind == "choice":
        return 1 if data.get("opt") in (goal.get("options") or []) else 0
    return 0


def rank_index(points: int, ranks: list[dict[str, Any]]) -> int:
    """Index of the reputation rank for some points (ranks sorted by "from"). [ES] Qué hace: el rango de reputación (su lugar en la lista) para unos puntos. La llama: el servicio. Si cambia, afecta: los rangos de todas las facciones."""
    index = 0
    for i, rank in enumerate(ranks):
        if int(points) >= int(rank["from"]):
            index = i
    return index


def rank_position(rank_id: str, ranks: list[dict[str, Any]]) -> int:
    """Index of a rank id in the list (0 if unknown). [ES] Qué hace: el lugar de un rango por su id. La llama: el servicio y matches. Si cambia, afecta: las condiciones de los saludos."""
    for i, rank in enumerate(ranks):
        if rank["id"] == rank_id:
            return i
    return 0


def matches(when: dict[str, Any] | None, facts: dict[str, Any], ranks: list[dict[str, Any]]) -> bool:
    """True if every condition of a greeting line holds.

    Conditions: done (mission id done), active (mission id is the current one), choice ({decision: option}),
    rank_min / rank_max (rank id with the character's faction), origin (origin id), met (talked before).

    [ES]
    Qué hace: dice si un saludo de un personaje vale ahora: todas sus condiciones tienen que cumplirse (misión
    hecha, misión en curso, decisión tomada, rango mínimo o máximo con su facción, origen, si ya hablaron).
    Una condición desconocida no se cumple (el saludo no sale).
    La llama: el servicio (_npc_line). Si cambia, afecta: lo que dice cada personaje.
    """
    for key, value in (when or {}).items():
        if key == "done" and value not in facts.get("done", ()):
            return False
        if key == "active" and value not in facts.get("active", ()):
            return False
        if key == "choice" and any(facts.get("choices", {}).get(c) != o for c, o in dict(value).items()):
            return False
        if key == "rank_min" and facts.get("rank", 0) < rank_position(value, ranks):
            return False
        if key == "rank_max" and facts.get("rank", 0) > rank_position(value, ranks):
            return False
        if key == "origin" and facts.get("origin") != value:
            return False
        if key == "met" and bool(facts.get("met")) != bool(value):
            return False
        if key not in ("done", "active", "choice", "rank_min", "rank_max", "origin", "met"):
            return False
    return True


def daily_pick(pool: dict[str, dict[str, Any]], factions: list[str], giver_faction: dict[str, str], seed: int, day: int) -> list[str]:
    """Today's tasks: one per faction (in faction order), drawn from the world seed and the day.

    [ES]
    Qué hace: elige los encargos de hoy, uno de cada facción, con un sorteo fijo (semilla del mundo y número de día):
    son los mismos para todos y cambian solos cada día real. Los retirados no salen.
    La llama: el servicio (_daily_ids). Si cambia, afecta: qué encargos ve todo el mundo hoy.
    """
    picked: list[str] = []
    for fid in factions:
        options = [tid for tid, tdef in pool.items() if not tdef.get("retired") and giver_faction.get(tdef.get("giver")) == fid]
        if options:
            picked.append(options[int(hash_unit(seed, "daily", day, fid) * len(options)) % len(options)])
    return picked


def weekly_pick(pool: dict[str, dict[str, Any]], seed: int, week: int, camp_key: str, level: int, count: int) -> list[str]:
    """This week's camp tasks: `count` of the pool for the camp's level, drawn from seed, week and camp.

    [ES]
    Qué hace: elige los encargos de campamento de la semana (los que el nivel del campamento permite), con un sorteo
    fijo por semilla, semana y campamento: cada campamento tiene los suyos y cambian cada semana.
    La llama: el servicio (_camp_task_ids). Si cambia, afecta: qué encargos ven los miembros de cada campamento.
    """
    options = [tid for tid, tdef in pool.items() if not tdef.get("retired") and int(level) >= int(tdef.get("min_level", 1))]
    options.sort(key=lambda tid: hash_unit(seed, "camp_task", week, camp_key, tid))
    return options[:max(0, int(count))]


def clean_text(text: str, limit: int) -> str:
    """Player-written text made safe to show: one line, no control characters, at most `limit` characters.

    [ES]
    Qué hace: limpia un texto que escribe el jugador (biografía, brindis): una sola línea, sin caracteres raros ni
    espacios de más, cortado al largo máximo.
    La llama: el servicio (/bio, /brindar). Si cambia, afecta: lo que otros jugadores leen de ti.
    """
    plain = "".join(ch if unicodedata.category(ch)[0] != "C" else " " for ch in str(text))
    plain = re.sub(r"\s+", " ", plain).strip()
    return plain[:max(0, int(limit))].strip()
