"""The world clock (D-126, confirmed; D-239.9, confirmed: a world day lasts 4 real days; how it was applied: D-334,
provisional; 0.58): day, evening and night, the same for everyone, and the small tilt each band gives to what you gather.

A world day lasts world_clock.day_hours real hours (96) from a fixed instant (world_clock.anchor, UTC seconds); it is split
in equal bands (world_clock.bands: dia, tarde, noche), so each band lasts 32 hours and whoever always plays at the same
hour still sees the three. The clock is pure arithmetic on the time: nothing is stored and a restart loses nothing.
Each band multiplies the weight of some resources in the draw of a gathering round (world_clock.weights: band → resource →
multiplier; missing = 1.0). It only changes the mix of a round, never the amount, and no weight goes below min_weight:
no resource ever disappears.

[ES]
Para qué sirve: el reloj del mundo de D-126 (confirmada: "día, tarde y noche en el mundo; cada franja del día da recursos
    distintos, y un día del mundo dura hasta 4 días reales") con la duración de D-239.9 (confirmada: 4 días reales; cada
    franja, unas 32 horas). Dice en qué franja está el mundo en un momento (igual para todos: no depende de la zona horaria de
    nadie, D-124), cuándo empezó y cuándo termina, cuál sigue, y cuánto pesa cada recurso en esa franja al recolectar (de
    día, más madera y piedra; de noche, más hierbas, setas y pescado; la tarde, lo de siempre). Cuentas puras, sin guardar
    nada: el servicio las llama con la hora.
Documento de diseño: diseno/02-mundo/mundo-vivo-y-viaje.md §2 (D-126, D-239.9, D-334)
Módulo: M8 Mundo (día, tarde y noche; el reloj de M1 da la hora)
Depende de: nada (los números llegan de content/balance.yaml, bloque world_clock: day_hours, anchor, bands, weights,
    min_weight, max_weight)
Lo usan: engine/service/world_time.py (_world_band, la línea de 📍 Zona, el peso de cada recurso) y, por medio de ella,
    engine/service/game.py (_gather_step, _explore_step y _is_night: la 🌙 noche de los 🔥 Braseros, raids.night.source)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno
Reglas que nunca se rompen:
    1. La franja es la misma para todos en el mismo instante (D-124): sale solo de la hora y de anchor, nunca de la zona
       horaria ni del cliente de nadie.
    2. Una franja nunca hace desaparecer un recurso: el peso nunca baja de min_weight (ni sube de max_weight) y solo cambia
       la mezcla de una vuelta, no cuántas unidades da.
    3. No guarda nada: cambiar day_hours o anchor mueve la franja de todos al instante (nadie pierde nada, pero lo que se
       anunció como "la noche llega en …" cambia). anchor no se toca.
Si cambias esto, revisa:
    - Servicio: engine/service/world_time.py y engine/service/game.py (_gather_step, _explore_step, _is_night)
    - Números: balance.yaml world_clock (y raids.night.source / band: la noche de los Braseros); el registro de balance
      (diseno/03-personaje/balance.md §7, 0.58)
    - Mapa de impacto: diseno/01-plataforma/mapa-de-impacto.md (M8, C-19 y §4.3 "Día de juego")
    - Pruebas: tests/test_zona_horaria_y_dia.py; tests/test_raids.py (los Braseros de noche)
"""

from __future__ import annotations

import math
from typing import Any, Mapping, Sequence

DEFAULT_BANDS = ("dia", "tarde", "noche")
MIN_WEIGHT, MAX_WEIGHT = 0.5, 2.0


def bands(cfg: Mapping[str, Any]) -> list[str]:
    """The band ids in order (world_clock.bands; default día, tarde, noche). [ES] Las franjas, en orden."""
    found = [str(b) for b in cfg.get("bands") or DEFAULT_BANDS if b]
    return found or list(DEFAULT_BANDS)


def day_seconds(cfg: Mapping[str, Any], scale: float = 1.0) -> float:
    """Real seconds of one world day: day_hours × 3600 × the service's time_scale. [ES] Cuánto dura un día del mundo."""
    return max(1.0, float(cfg.get("day_hours", 96))) * 3600.0 * max(1e-9, float(scale))


def band_at(cfg: Mapping[str, Any], when: float, scale: float = 1.0) -> dict[str, Any]:
    """The world's band at the instant `when`: its id, index, start and end (UTC seconds), the next band and the day number.

    [ES]
    Qué hace: en qué franja está el mundo en ese momento. Cuenta desde anchor (el instante en que empezó un ☀️ día) y parte
    cada día del mundo en partes iguales. Devuelve {"id", "index", "start", "end", "next", "day"}: "end" es cuándo llega la
    franja siguiente ("next"). Igual para todos (no mira la zona horaria de nadie).
    La llaman: engine/service/world_time.py (_world_band). Si cambia, afecta: la línea de 📍 Zona, qué rinde cada vuelta de
    recolectar y cuándo cuentan los 🔥 Braseros.
    """
    ids = bands(cfg)
    day = day_seconds(cfg, scale)
    length = day / len(ids)
    elapsed = float(when) - float(cfg.get("anchor", 0))
    number = math.floor(elapsed / day)
    into = elapsed - number * day
    index = min(len(ids) - 1, max(0, int(into // length)))
    start = float(cfg.get("anchor", 0)) + number * day + index * length
    return {"id": ids[index], "index": index, "start": start, "end": start + length,
            "next": ids[(index + 1) % len(ids)], "day": int(number)}


def weight(cfg: Mapping[str, Any], band: str, resource: str) -> float:
    """How much a resource weighs in a gathering round during that band (missing = 1.0), between min_weight and max_weight.

    [ES]
    Qué hace: cuánto pesa un recurso en el sorteo de una vuelta de recolectar en esa franja (world_clock.weights; lo que no
    está vale 1,0). Nunca baja de min_weight (0,5) ni pasa de max_weight (2,0): ningún recurso desaparece.
    La llaman: weighted y favoured, y engine/service/world_time.py (_band_weight). Si cambia, afecta: qué sale al recolectar.
    """
    low = float(cfg.get("min_weight", MIN_WEIGHT))
    high = float(cfg.get("max_weight", MAX_WEIGHT))
    table = (cfg.get("weights") or {}).get(band) or {}
    try:
        value = float(table.get(resource, 1.0))
    except (TypeError, ValueError):
        value = 1.0
    return max(low, min(high, value))


def weighted(cfg: Mapping[str, Any], band: str, resources: Sequence[str], base: Sequence[float]) -> list[float]:
    """The base weights of a draw, each multiplied by its resource's weight in that band. [ES] Los pesos de un sorteo con la franja."""
    return [float(b) * weight(cfg, band, r) for r, b in zip(resources, base)]


def favoured(cfg: Mapping[str, Any], band: str, resources: Sequence[str]) -> list[str]:
    """The resources (of those given) that weigh more than usual in that band, the most favoured first.

    [ES]
    Qué hace: de los recursos dados (los de la zona), los que salen más que lo normal en esa franja, primero los que más.
    La llama: engine/service/world_time.py (la línea de 🧭 Explorar "☀️ De día, aquí sale más: …").
    Si cambia, afecta: solo lo que se lee.
    """
    order = {r: i for i, r in enumerate(resources)}
    picked = [r for r in resources if weight(cfg, band, r) > 1.0]
    return sorted(picked, key=lambda r: (-weight(cfg, band, r), order[r]))
