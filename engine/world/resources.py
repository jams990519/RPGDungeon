"""Resource regions of the infinite map: which resources each zone has and how rich (D-87, D-180).

[ES]
Para qué sirve: decir qué recursos hay en cada zona. Hay 6 recursos "de base" (madera, piedra, fibra, hierba,
metal y arcilla). Cada uno forma manchas de distinto tamaño sobre el mapa (unas chicas de 2-3 zonas,
otras de 5×5 o más), mezcladas entre sí: una zona tiene de 1 a 3 de base. El bioma ayuda (más madera
en el bosque, más piedra en la montaña), pero no manda. Todo sale de la semilla del mundo.
D-180 y D-183 (0.27): cada terreno tiene su catálogo de 10 a 15 recursos posibles (catalog: los de base de su "gather" en
content/biomes.yaml más los suyos, "own"). Encima de los de base, cada zona suma 2 o 3 de los propios de su terreno
(terrain_resources, con su propio canal de la semilla, riqueza de 0,3 a 1,0), hasta quedar con 4 a 6 recursos de tierra
(balance.yaml resources.terrain). Los de base NO cambian: zone_resources da lo mismo que antes en cada zona. El color del
terreno nunca promete un recurso (D-179): solo se sabe cuál hay explorando. El Claro (zonas "fixed") no suma ninguno.
D-115 (fase 2 de los oficios): además, algunas zonas tienen agua (un río, un lago, el pantano): ahí se pesca 🐟 pescado
(water_resources). Es un recurso aparte, que se suma a los de la zona sin quitar ninguno: los biomas con "water" en
content/biomes.yaml dicen qué parte de sus zonas tiene agua, y balance.yaml camp_professions.fish cuánto pesa.
Documento de diseño: diseno/02-mundo/mapa-infinito-y-viaje.md §1.12 (exploración y recursos; §1.12.2 el catálogo de cada terreno)
Módulo: M8 Mundo (recursos)
Depende de: engine.core (hash_unit), content/balance.yaml (resources, resources.terrain y camp_professions.fish),
    content/biomes.yaml (gather, own y water)
Lo usan: engine/service/game.py (_zone_resources junta los tres: explorar, recolectar, mapa, campamentos, nodos de
    recursos, cofres de los campamentos enemigos)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno (el agotamiento se guarda en el espacio "stock" del almacén, por recurso)
Reglas que nunca se rompen:
    1. La misma semilla da siempre los mismos recursos en la misma zona.
    2. Toda zona tiene al menos 1 recurso de base y como mucho resources.max_per_zone (3). Con los del terreno, una zona
       que no es fija tiene de resources.terrain.total[0] a total[1] recursos de tierra (4 a 6); el agua suma 1 aparte.
    3. El agua (D-115) y los recursos del terreno (D-180) nunca cambian los de base de una zona: cada uno usa su propio
       sorteo ("water", "terrain_count", "terrain_pick", "terrain_rich").
Si cambias esto, revisa:
    - Números: balance.yaml resources.* (cambiar escalas o umbrales mueve los recursos de un mundo ya creado; terrain.*
      mueve solo los del terreno)
    - Contenido: content/biomes.yaml "own" (agregar uno al final de la lista puede cambiar qué propios trae una zona: el
      sorteo ordena por recurso); cada recurso nuevo pide su objeto en content/items.yaml, su oficio de recolección
      ("gathers" de content/professions.yaml), un uso (una receta) y sus textos (content/locales/es_terrenos.yaml)
    - Servicio: engine/service/game.py (_zone_resources junta los tres; _gather_step, _stock, _known_resources, _map_view,
      _ecamp_chest, _node_main)
    - Pruebas: tests/test_resources.py, tests/test_oficios_campamento.py (el pescado), tests/test_nodos_y_terrenos.py
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


def catalog(biome: str, biomes: dict[str, Any]) -> list[str]:
    """Every resource a terrain can bring (D-180): its base affinities ("gather") and then its own ones ("own").

    [ES]
    Qué hace: el catálogo del terreno: los recursos de base que ese terreno favorece y los suyos propios (10 a 15 en total).
    Una zona trae solo una parte. Los de base pueden salir en cualquier terreno (sus manchas no miran el bioma); el catálogo
    dice lo que es típico de ese terreno. La llaman: las pruebas y la documentación (red de sistemas).
    Si cambia, afecta: solo lo que se cuenta como "del terreno"; los recursos de cada zona salen de terrain_resources.
    """
    bdef = biomes.get(biome) or {}
    base = list((bdef.get("gather") or {}).keys())
    return base + [r for r in (bdef.get("own") or []) if r not in base]


def terrain_resources(seed: int, x: int, y: int, biome: str, base: dict[str, float], balance: dict[str, Any],
                      biomes: dict[str, Any]) -> dict[str, float]:
    """The terrain's own resources a zone adds on top of its base ones (D-180, D-183), strongest first, or {}.

    Args:
        base: the zone's base resources (zone_resources), so the total stays inside resources.terrain.total.

    [ES]
    Qué hace: elige cuáles de los recursos propios de su terreno ("own" en content/biomes.yaml) trae la zona: 2 o 3
    (resources.terrain.add), sin pasar de 6 recursos de tierra en total ni quedar con menos de 4 (resources.terrain.total:
    con 1 de base suma 3; con 3 de base, 2 o 3). Cada uno con su riqueza de 0,3 a 1,0 (terrain.richness). Usa canales nuevos
    de la semilla ("terrain_count", "terrain_pick", "terrain_rich"): nunca mueve los de base ni el agua. Las zonas fijas
    (el Claro) no suman nada. D-185 (el dueño pidió un reparto "bastante aleatorio"): cada propio elegido tiene
    resources.terrain.foreign_chance de cambiarse por uno del catálogo de OTRO terreno (canales "terrain_foreign" y
    "terrain_foreign_pick"): por eso puede haber árboles donde se supone que no deberían.
    La llama: GameService._zone_resources. Si cambia, afecta: qué recursos del terreno hay en cada zona de todos.
    """
    cfg = balance["resources"]
    tcfg = cfg.get("terrain") or {}
    own = [r for r in ((biomes.get(biome) or {}).get("own") or []) if r not in base]
    if not tcfg or not own or f"{x}:{y}" in cfg.get("fixed", {}):
        return {}
    low, high = (int(v) for v in tcfg.get("add", [2, 3]))
    want = low + int(hash_unit(seed, "terrain_count", x, y) * (high - low + 1))
    total_min, total_max = (int(v) for v in tcfg.get("total", [4, 6]))
    want = max(want, total_min - len(base))           # 1 base resource: it adds 3 (4 in all)
    want = min(want, total_max - len(base), len(own))  # never more than 6 land resources in all
    if want <= 0:
        return {}
    picked = sorted(own, key=lambda r: (hash_unit(seed, "terrain_pick", x, y, r), r))[:want]
    foreign_chance = float(tcfg.get("foreign_chance", 0.0))
    if foreign_chance > 0:                            # D-185: now and then one comes from another terrain's catalog
        others = sorted({r for b, d in biomes.items() if b != biome for r in ((d or {}).get("own") or [])}
                        - set((biomes.get(biome) or {}).get("own") or []) - set(base))
        mixed: list[str] = []
        for slot, res in enumerate(picked):
            choices = [o for o in others if o not in mixed]
            if choices and hash_unit(seed, "terrain_foreign", x, y, slot) < foreign_chance:
                res = min(choices, key=lambda o: (hash_unit(seed, "terrain_foreign_pick", x, y, slot, o), o))
            mixed.append(res)
        picked = mixed
    rich_low, rich_high = (float(v) for v in tcfg.get("richness", [0.3, 1.0]))
    rich = {r: round(rich_low + (rich_high - rich_low) * hash_unit(seed, "terrain_rich", x, y, r), 2) for r in picked}
    return dict(sorted(rich.items(), key=lambda kv: (-kv[1], kv[0])))


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
    """The richest resource of a zone. [ES] Qué hace: el recurso principal (antes, el color del mapa al 100 %; desde D-179 el
    mapa pinta el terreno). La llaman: tests/test_resources.py (las manchas de recursos). Si cambia, afecta: solo esa prueba."""
    return max(resources.items(), key=lambda kv: kv[1])[0]
