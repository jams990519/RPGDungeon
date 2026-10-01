"""Resource regions of the infinite map: which resources each zone has and how rich (D-87).

[ES]
Para qué sirve: decir qué recursos hay en cada zona. Hay 6 tipos (madera, piedra, fibra, hierba,
metal y arcilla). Cada uno forma manchas de distinto tamaño sobre el mapa (unas chicas de 2-3 zonas,
otras de 5×5 o más), mezcladas entre sí: una zona tiene de 1 a 3 tipos. El bioma ayuda (más madera
en el bosque, más piedra en la montaña), pero no manda. Todo sale de la semilla del mundo.
D-115 (fase 2 de los oficios): además, algunas zonas tienen agua (un río, un lago, el pantano): ahí se pesca 🐟 pescado
(water_resources). Es un recurso aparte, que se suma a los de la zona sin quitar ninguno: los biomas con "water" en
content/biomes.yaml dicen qué parte de sus zonas tiene agua, y balance.yaml camp_professions.fish cuánto pesa.
Documento de diseño: diseno/02-mundo/mapa-infinito-y-viaje.md §1.12 (exploración y recursos)
Módulo: M8 Mundo (recursos)
Depende de: engine.core (hash_unit), content/balance.yaml (resources y camp_professions.fish), content/biomes.yaml
    (gather y water)
Lo usan: engine/service/game.py (explorar, recolectar, mapa, campamentos)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno (el agotamiento se guarda en el espacio "stock" del almacén)
Reglas que nunca se rompen:
    1. La misma semilla da siempre los mismos recursos en la misma zona.
    2. Toda zona tiene al menos 1 recurso y como mucho resources.max_per_zone (de tierra; el agua suma 1 aparte).
    3. El agua (D-115) nunca cambia los recursos de tierra de una zona: solo agrega el pescado (sorteo propio, "water").
Si cambias esto, revisa:
    - Números: balance.yaml resources.* (cambiar escalas o umbrales mueve los recursos de un mundo ya creado)
    - Servicio: engine/service/game.py (_zone_resources junta los dos; _gather_step, _stock, _known_resources, _map_view,
      _ecamp_chest)
    - Pruebas: tests/test_resources.py, tests/test_oficios_campamento.py (el pescado)
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


def water_resources(seed: int, x: int, y: int, biome: str, balance: dict[str, Any], biomes: dict[str, Any]) -> dict[str, float]:
    """The fishing resource of a zone with water (D-115 phase 2), or {}: {fish id: richness}.

    A share of the zones of each biome has water (content/biomes.yaml "water": 1.0 = all of them); which ones comes from
    the world seed with its own channel, so it never moves the land resources. Zones with fixed resources (the Claro)
    have none.

    [ES]
    Qué hace: dice si la zona tiene agua y, si la tiene, devuelve el 🐟 pescado con su peso (balance.yaml
    camp_professions.fish.richness). En el pantano todas las zonas tienen agua; en el bosque y la pradera, algunas (sus
    ríos y lagos). Sale de la semilla: siempre las mismas zonas.
    La llama: el servicio (GameService._zone_resources), que lo suma a los recursos de tierra.
    Si cambia, afecta: dónde se pesca (y el 🎣 Pescador y la 🍲 Cocina que dependen del pescado).
    """
    fish = (balance.get("camp_professions") or {}).get("fish") or {}
    share = float((biomes.get(biome) or {}).get("water", 0.0))
    if not fish or share <= 0 or f"{x}:{y}" in balance["resources"].get("fixed", {}):
        return {}
    if hash_unit(seed, "water", x, y) >= share:
        return {}
    return {fish["resource"]: float(fish["richness"])}


def main_resource(resources: dict[str, float]) -> str:
    """The richest resource of a zone (the colour on the map). [ES] Qué hace: el recurso principal. La llama: el mapa. Si cambia, afecta: el color de cada zona."""
    return max(resources.items(), key=lambda kv: kv[1])[0]
