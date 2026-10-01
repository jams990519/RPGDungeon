"""Settlement pantry (D-93, provisional): food that active residents eat every real day.

Phase 1 of "building is not enough" (capa simple): the Claro from the aldea stage and player
camps from level 3 keep a pantry. Consumption is lazy, like the zone stock: the store keeps
{"rations": float, "at": ts} and every read subtracts active × elapsed_days × ration_per_day.
These helpers are pure: the service reads the store, counts active residents and calls them.

[ES]
Para qué sirve: las cuentas de la despensa de un asentamiento (el Claro desde aldea y los
campamentos desde el nivel 3): cuánta comida queda después de que comieron los residentes
activos, cuántos días alcanza y en qué estado está (abundancia, holgada, justa, escasez, hambruna).
Documento de diseño: diseno/02-mundo/supervivencia-del-asentamiento.md §0.4, §3.1-3.2, §4.2, §7 (D-93, provisional)
Módulo: M9 Frontera y Fundación (vive en engine/world hasta que exista engine/front)
Depende de: ninguno (los números llegan de content/balance.yaml, bloque pantry)
Lo usan: engine/service/game.py (_pantry, _pantry_status, _take_food)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno (el servicio guarda la despensa en el espacio "pantry" del almacén)
Reglas que nunca se rompen:
    1. La despensa nunca baja de 0 y nunca toca la mochila de nadie: solo entra lo que un jugador aporta.
    2. Quien no juega no come: el consumo cuenta solo a los residentes activos (§15.3).
    3. Con 0 residentes activos no se consume nada; los días se cuentan como si hubiera 1 (no se divide por 0).
Si cambias esto, revisa:
    - Servicio: engine/service/game.py (obra común del Claro, posada, campamentos que crecen)
    - Números: balance.yaml pantry (states, ration_per_day, min_days_to_rise)
    - Pruebas: tests/test_pantry.py
"""

from __future__ import annotations

from typing import Any


def consume(rations: float, active: int, elapsed_days: float, ration_per_day: float) -> float:
    """Rations left after `active` residents ate for `elapsed_days` (never below 0).

    [ES]
    Qué hace: resta lo que comieron los residentes activos en el tiempo que pasó (consumo perezoso).
    La llaman: el servicio cada vez que lee una despensa.
    Si cambia, afecta: cuánto dura la comida del Claro y de los campamentos.
    """
    eaten = max(0, active) * max(0.0, elapsed_days) * ration_per_day
    return max(0.0, float(rations) - eaten)


def days_left(rations: float, active: int, ration_per_day: float) -> int:
    """Whole days the food lasts at the current consumption (at least 1 eater is assumed).

    [ES]
    Qué hace: dice cuántos días enteros alcanza la comida con los residentes activos de hoy.
    La llaman: el servicio (pantallas, posada, subida de etapa, crecer un campamento).
    Si cambia, afecta: el estado de la despensa y cuándo sube el Claro.
    """
    daily = max(1, active) * ration_per_day
    return int(max(0.0, rations) // daily) if daily > 0 else 0


def state(days: int, thresholds: dict[str, int]) -> str:
    """The pantry state for a number of days: the highest threshold reached (hambruna below 1 day).

    [ES]
    Qué hace: traduce los días de comida a un estado (abundancia ≥14, holgada ≥7, justa ≥3, escasez ≥1, hambruna).
    La llaman: el servicio.
    Si cambia, afecta: la posada (no cura en hambruna), la obra común y el crecimiento de los campamentos.
    """
    for name, need in sorted(thresholds.items(), key=lambda kv: -kv[1]):
        if days >= need:
            return name
    return min(thresholds, key=thresholds.get)


def food_in(items: dict[str, Any], backpack: dict[str, int]) -> tuple[dict[str, int], int]:
    """Every food item in a backpack and the rations it is worth (items.yaml `food`).

    [ES]
    Qué hace: encuentra la comida de la mochila (carne, provisiones...) y cuántas raciones vale.
    La llaman: el servicio al aportar comida.
    Si cambia, afecta: qué objetos cuentan como comida.
    """
    found = {i: n for i, n in backpack.items() if n > 0 and items.get(i, {}).get("food")}
    return found, sum(int(items[i]["food"]) * n for i, n in found.items())
