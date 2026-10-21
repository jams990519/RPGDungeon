"""Camp raids and the Noche de prueba (D-99, provisional): the pure rules.

Phase 2 of "building is not enough" (capa simple, player camps only): from level 5 a raid reaches
a camp once a week; to grow to castillo the camp must win a Noche de prueba (a bigger raid with an
elite enemy). The clock is lazy like the pantry: the camp stores next_raid_at and the service opens,
counts and resolves raids when a member plays. These helpers are pure: the service reads the store,
counts active members and calls them.

[ES]
Para qué sirve: las cuentas de las incursiones de los campamentos de jugadores (desde pueblo, nivel 5) y
de la Noche de prueba antes de castillo: cuántas victorias hacen falta, cuándo llega la próxima, qué
enemigo ataca (y su versión élite) y cuánta comida se pierde si no alcanzan.
Documento de diseño: diseno/02-mundo/supervivencia-del-asentamiento.md §0.5, §6.1-6.2, §7.2 y §15 (D-99, provisional)
Módulo: M9 Frontera y Fundación (vive en engine/world hasta que exista engine/front)
Depende de: engine/world/encounters.py (qué enemigos caben en el bioma y el nivel, D-108); los números llegan de
    content/balance.yaml, bloque raids; los enemigos de content/enemies.yaml
Lo usan: engine/service/game.py (_raid_settle, _open_raid, _defend, _resolve_raid, _trial_view) y, desde la 0.53 (D-122,
    D-329), engine/service/ladder.py (wave_mult y series_outcome: las 🌊 oleadas crecientes antes del castillo)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno (el servicio guarda la incursión abierta y la próxima hora en el campamento: "camp/<x:y>")
Reglas que nunca se rompen:
    1. Nunca hace falta menos de min_wins victorias, y nunca se divide por 0 miembros.
    2. La comida perdida nunca pasa de lo que hay en la despensa: perder una incursión no quita nada más (§15).
    3. Los jefes (boss: true) y lo retirado (retired: true) nunca atacan un campamento.
    4. La versión élite solo cambia vida y ataque del enemigo en esa pelea: nunca toca enemies.yaml.
    5. Las oleadas crecientes (D-122, D-329): cada oleada de la serie es más fuerte que la anterior (nunca más débil), y la
       serie se aprueba al llegar a las victorias pedidas o se pierde cuando ya no se pueden alcanzar (nunca antes).
Si cambias esto, revisa:
    - Servicio: engine/service/game.py (pantalla del campamento, botón 🛡️ Defender, crecer a castillo)
    - Combate: engine/combat/engine.py make_combat (scale_enemy depende de las claves hp, max_hp, attack, base_attack)
    - Números: balance.yaml raids (required_share, min_wins, per_week, loss_share, trial.*) y ladder.castle_waves (count,
      pass_wins, growth, retry_days)
    - Pruebas: tests/test_raids.py y tests/test_oleadas_crecientes_castillo.py
"""

from __future__ import annotations

import math
from typing import Any

from engine.world.encounters import clamp_level, encounter_pool


def required_wins(active: int, share: float, minimum: int) -> int:
    """Wins a raid needs: ceil(active members × share), never below `minimum`.

    [ES]
    Qué hace: cuántas victorias de miembros distintos hacen falta (la mitad de los activos, redondeado
    hacia arriba, y nunca menos del mínimo: 1 en la incursión, 2 en la Noche de prueba).
    La llama: el servicio al abrir una incursión y en la pantalla de la Noche de prueba.
    Si cambia, afecta: qué tan fácil es defender un campamento grande o chico.
    """
    return max(int(minimum), math.ceil(max(0, active) * share - 1e-9))


def next_raid_at(until: float, now: float, interval: float) -> float:
    """When the next weekly raid comes: one interval after the last window closed; if that already
    passed (nobody played for a long time), one interval from now, so nobody comes back to a raid.

    [ES]
    Qué hace: agenda la próxima incursión una semana después de la anterior; si el campamento estuvo
    quieto más de una semana, cuenta la semana desde ahora (nadie vuelve y se encuentra otra encima).
    La llama: el servicio al cerrar una incursión.
    Si cambia, afecta: cada cuánto llegan las incursiones.
    """
    nxt = until + interval
    return nxt if nxt > now else now + interval


def power(enemy_def: dict[str, Any], level: int) -> float:
    """Rough strength of an enemy at a level: life × attack (for picking the strongest).

    [ES]
    Qué hace: una cuenta simple de qué tan fuerte es un enemigo a cierto nivel (vida × ataque).
    La llama: pick_enemy, para elegir el más fuerte del bioma en la Noche de prueba.
    Si cambia, afecta: qué enemigo trae la Noche de prueba.
    """
    base, per = enemy_def["base"], enemy_def.get("per_level", {})
    lv = max(1, level) - 1
    return (base["hp"] + per.get("hp", 0) * lv) * (base["attack"] + per.get("attack", 0) * lv)


def pick_enemy(enemies: dict[str, Any], biome: str, level: int, strongest: bool = False, roll: float = 0.0) -> tuple[str, int]:
    """The raid enemy of a camp: from its biome and fitting its level (like the normal encounters).

    `strongest` picks the hardest one (Noche de prueba); otherwise `roll` (0..1) picks one at random.
    The level is clamped to the enemy's own range.

    [ES]
    Qué hace: elige el enemigo que ataca el campamento, del bioma de su zona y de su nivel (como los
    encuentros normales). En la Noche de prueba, el más fuerte de los que caben. Devuelve (id, nivel).
    La llama: el servicio al abrir una incursión o al mostrar la Noche de prueba.
    Si cambia, afecta: contra qué pelean los defensores.
    """
    pool = encounter_pool(enemies, biome, level)        # D-108: same rule as the normal encounters

    def clamp(e: dict[str, Any]) -> int:
        return clamp_level(e, level)

    if strongest:
        enemy_id, enemy_def = max(pool, key=lambda pair: (power(pair[1], clamp(pair[1])), pair[0]))
    else:
        enemy_id, enemy_def = pool[int(roll * len(pool)) % len(pool)]
    return enemy_id, clamp(enemy_def)


def scale_enemy(state: dict[str, Any], hp_mult: float, attack_mult: float) -> None:
    """Make the enemy of a new fight an elite: more life and attack (only this fight).

    [ES]
    Qué hace: vuelve élite al enemigo de una pelea recién creada (más vida y más ataque). Solo esa pelea.
    La llama: el servicio cuando un defensor sale a la Noche de prueba.
    Si cambia, afecta: qué tan difícil es la Noche de prueba.
    """
    enemy = state["enemy"]
    enemy["max_hp"] = enemy["hp"] = max(1, int(round(enemy["max_hp"] * hp_mult)))
    enemy["attack"] = float(enemy["attack"]) * attack_mult
    enemy["base_attack"] = float(enemy.get("base_attack", enemy["attack"] / attack_mult)) * attack_mult


def food_lost(rations: float, share: float) -> float:
    """Rations a lost raid takes from the pantry (never more than there is).

    [ES]
    Qué hace: cuánta comida se lleva una incursión perdida (una parte de la despensa; nunca más de lo que hay).
    La llama: el servicio al cerrar una incursión perdida.
    Si cambia, afecta: cuánto duele perder una incursión.
    """
    return max(0.0, min(float(rations), float(rations) * share))


def wave_mult(n: int, growth: float) -> float:
    """How much stronger the n-th growing wave of the castle's series is than a normal raid: 1 + growth × n (D-122, D-329).

    [ES]
    Qué hace: la fuerza de la oleada creciente número n (1, 2, 3…) contra una oleada normal: con growth 0,2, la 1.ª ×1,2,
    la 2.ª ×1,4… la 5.ª ×2,0 (vida y ataque de los atacantes, antes de la 🛡️ Defensa). Nunca baja de ×1.
    La llama: engine/service/ladder.py (_castle_wave_mark, al abrir la oleada; y los textos que dicen cuánto más fuerte es).
    Si cambia, afecta: qué tan difícil es aprobar las oleadas crecientes del castillo.
    """
    return 1.0 + max(0.0, float(growth)) * max(0, int(n))


def series_outcome(won: int, lost: int, count: int, pass_wins: int) -> str | None:
    """"passed" once the wins reach pass_wins, "failed" once they no longer can, None while the series is open (D-329).

    [ES]
    Qué hace: dice si la serie de oleadas crecientes ya se decidió: "passed" al llegar a las victorias pedidas (3 de 5),
    "failed" cuando ni ganando todas las que quedan se llega ("si pierde más de las que gana, no aprueba", D-122: con 5
    oleadas, a las 3 perdidas), o None si sigue abierta.
    La llama: engine/service/ladder.py (_castle_wave_done, al cerrar cada oleada de la serie).
    Si cambia, afecta: cuándo se aprueba o se pierde la serie (tests/test_oleadas_crecientes_castillo.py).
    """
    need = min(max(1, int(pass_wins)), max(1, int(count)))
    if won >= need:
        return "passed"
    if won + max(0, int(count) - won - lost) < need:
        return "failed"
    return None
