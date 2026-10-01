"""Resource regions of the infinite map: which resources each zone has and how rich (D-87).

[ES]
Para qué sirve: decir qué recursos hay en cada zona. Hay 6 tipos (madera, piedra, fibra, hierba,
metal y arcilla). Cada uno forma manchas de distinto tamaño sobre el mapa (unas chicas de 2-3 zonas,
otras de 5×5 o más), mezcladas entre sí: una zona tiene de 1 a 3 tipos. El bioma ayuda (más madera
en el bosque, más piedra en la montaña), pero no manda. Todo sale de la semilla del mundo.
Documento de diseño: diseno/02-mundo/mapa-infinito-y-viaje.md §1.12 (exploración y recursos)
Módulo: M8 Mundo (recursos)
Depende de: engine.core (hash_unit), content/balance.yaml (resources), content/biomes.yaml (gather)
Lo usan: engine/service/game.py (explorar, recolectar, mapa, campamentos)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno (el agotamiento se guarda en el espacio "stock" del almacén)
Reglas que nunca se rompen:
    1. La misma semilla da siempre los mismos recursos en la misma zona.
    2. Toda zona tiene al menos 1 recurso y como mucho resources.max_per_zone.
Si cambias esto, revisa:
    - Números: balance.yaml resources.* (cambiar escalas o umbrales mueve los recursos de un mundo ya creado)
    - Servicio: engine/service/game.py (_zone_resources, _gather_outcome, _map_view)
    - Pruebas: tests/test_resources.py
"""

from __future__ import annotations

from typing import Any

from engine.core import hash_unit


def _noise(seed: int, channel: str, x: int, y: int, scale: int) -> float:
    gx, gy = x // scale, y // scale
    fx, fy = (x % scale) / scale, (y % scale) / scale
    c = lambda cx, cy: hash_unit(seed, channel, cx, cy)
    top = c(gx, gy) * (1 - fx) + c(gx + 1, gy) * fx
    bottom = c(gx, gy + 1) * (1 - fx) + c(gx + 1, gy + 1) * fx
    return top * (1 - fy) + bottom * fy


def zone_resources(seed: int, x: int, y: int, biome: str, balance: dict[str, Any], biomes: dict[str, Any]) -> dict[str, float]:
    """Resources of a zone with their richness (0.3 to 1.0), strongest first.

    [ES]
    Qué hace: devuelve los recursos de la zona y qué tan rica es en cada uno.
    La llama: el servicio (explorar, recolectar, mapa).
    Si cambia, afecta: qué se consigue en cada lugar del mundo.
    """
    cfg = balance["resources"]
    fixed = cfg.get("fixed", {}).get(f"{x}:{y}")
    if fixed:
        return dict(fixed)
    affinity = biomes.get(biome, {}).get("gather", {})
    top_weight = max(affinity.values()) if affinity else 1
    scores = {}
    for res, scale in cfg["region_scale"].items():
        # Each resource has its own patch size; a second, wider noise makes some regions much bigger.
        value = 0.65 * _noise(seed, f"res:{res}", x, y, scale) + 0.35 * _noise(seed, f"res2:{res}", x, y, scale * 2)
        value += cfg["biome_bonus"] * affinity.get(res, 0) / top_weight
        scores[res] = value
    ranked = sorted(scores.items(), key=lambda kv: -kv[1])
    present = [(r, v) for r, v in ranked if v >= cfg["threshold"]][: cfg["max_per_zone"]] or ranked[:1]
    best = present[0][1]
    return {r: round(max(0.3, min(1.0, v / best)), 2) for r, v in present}


def main_resource(resources: dict[str, float]) -> str:
    """The richest resource of a zone (the colour on the map). [ES] Qué hace: el recurso principal. La llama: el mapa. Si cambia, afecta: el color de cada zona."""
    return max(resources.items(), key=lambda kv: kv[1])[0]
