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
D-300 (0.39, pedido del dueño, 20-oct-2026: "distribuye un poquitico el recurso de madera en diferentes puntos del mapa,
porque prácticamente se está volviendo imposible encontrarlo"; números de Claude, provisionales): la 🪵 madera se SUMA en
más zonas (wood_resource): toda zona de terreno de bosque (el que se ve) la tiene, y en las demás aparece con un umbral
propio más bajo (balance.yaml resources.wood). Va justo después de los de base. Solo suma: ninguna zona pierde un recurso
que tenía, los propios del terreno salen igual que antes y no hay sorteos nuevos. Además vuelve más rápido que los demás
recursos (balance.yaml stock.regen_mult, lo aplica GameService._stock).
D-303 (0.41.1, orden del dueño, 20-oct-2026: "los bosques deberían tener, las montañas deberían tener, o sea, en todos
lugares, en menor medida, pero deberían tener"; números de Claude, provisionales): la 🪵 madera está en TODA zona que no es
fija ni hoguera. En los terrenos de bosque (el que se ve: bosque, bosque oscuro y selva) es la más rica (1,0) y va PRIMERA
(wood_first: se conoce desde la primera exploración); en los demás terrenos, si no era de base, se suma pobre (de 0,3 a
resources.wood.elsewhere_max, 0,5) justo después de los de base. El umbral de D-300 (resources.wood.threshold) quedó sin uso.
Documento de diseño: diseno/02-mundo/mapa-infinito-y-viaje.md §1.12 (exploración y recursos; §1.12.2 el catálogo de cada terreno)
Módulo: M8 Mundo (recursos)
Depende de: engine.core (hash_unit), content/balance.yaml (resources, resources.terrain, resources.wood y
    camp_professions.fish), content/biomes.yaml (gather, own y water)
Lo usan: engine/service/game.py (_zone_land y _zone_resources juntan los cuatro: explorar, recolectar, mapa, campamentos,
    nodos de recursos, cofres de los campamentos enemigos; wood_first lo usa _zone_resources para poner la madera primera)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno (el agotamiento se guarda en el espacio "stock" del almacén, por recurso)
Reglas que nunca se rompen:
    1. La misma semilla da siempre los mismos recursos en la misma zona.
    2. Toda zona tiene al menos 1 recurso de base y como mucho resources.max_per_zone (3). Con los del terreno, una zona
       que no es fija tiene de resources.terrain.total[0] a total[1] recursos de tierra (4 a 6); la 🪵 madera de D-300 y
       D-303 puede sumar 1 más (hasta 7) y el agua suma 1 aparte.
    3. El agua (D-115), los recursos del terreno (D-180) y la madera de D-300/D-303 nunca cambian los de base de una zona:
       cada uno usa su propio sorteo ("water", "terrain_count", "terrain_pick", "terrain_rich") o, la madera, la fuerza de
       siempre; los del terreno se sortean con los de base SIN la madera sumada.
    4. D-300 y D-303: la madera solo se suma. Ninguna zona pierde un recurso que tenía antes.
    5. D-303: toda zona que no es fija ni hoguera tiene 🪵 madera (con el bloque resources.wood de content/balance.yaml).
Si cambias esto, revisa:
    - Números: balance.yaml resources.* (cambiar escalas o umbrales mueve los recursos de un mundo ya creado; terrain.*
      mueve solo los del terreno; wood.* solo cuánta madera se suma: forest_min en los bosques, elsewhere_max en el resto)
    - Contenido: content/biomes.yaml "own" (agregar uno al final de la lista puede cambiar qué propios trae una zona: el
      sorteo ordena por recurso); cada recurso nuevo pide su objeto en content/items.yaml, su oficio de recolección
      ("gathers" de content/professions.yaml), un uso (una receta) y sus textos (content/locales/es_terrenos.yaml)
    - Servicio: engine/service/game.py (_zone_land y _zone_resources juntan los cuatro; _gather_step, _stock (D-300: la
      madera vuelve más rápido), _known_resources (D-303: la madera sumada o movida no ocupa un lugar de los que revela
      explorar), _map_view, _ecamp_chest, _node_main); engine/service/gremio.py (_resource_search_view: D-303, las zonas
      ricas primero entre las cercanas)
    - Pruebas: tests/test_resources.py, tests/test_oficios_campamento.py (el pescado), tests/test_nodos_y_terrenos.py
"""

from __future__ import annotations

from typing import Any

from engine.core import hash_unit
from engine.world.mapgen import is_bonfire               # D-265: every bonfire has the Claro's fixed resources


def _noise(seed: int, channel: str, x: int, y: int, scale: int) -> float:
    gx, gy = x // scale, y // scale
    fx, fy = (x % scale) / scale, (y % scale) / scale
    c = lambda cx, cy: hash_unit(seed, channel, cx, cy)
    top = c(gx, gy) * (1 - fx) + c(gx + 1, gy) * fx
    bottom = c(gx, gy + 1) * (1 - fx) + c(gx + 1, gy + 1) * fx
    return top * (1 - fy) + bottom * fy


def _base_scores(seed: int, x: int, y: int, biome: str, cfg: dict[str, Any], biomes: dict[str, Any]) -> dict[str, float]:
    """How strong each of the 6 base resources is in a zone (its patches plus the biome's help), before any threshold.

    [ES]
    Qué hace: la "fuerza" de cada recurso de base en la zona: dos ruidos de la semilla (manchas de distinto tamaño,
    resources.region_scale) más la ayuda del bioma (resources.biome_bonus). zone_resources se queda con los que pasan
    resources.threshold; wood_resource (D-300, D-303) usa la de la 🪵 madera para su riqueza fuera del bosque. Es el mismo
    cálculo que había dentro de zone_resources antes de D-300: separarlo no movió ningún recurso. La llaman: zone_resources
    y wood_resource.
    Si cambia, afecta: los recursos de base (y la riqueza de la madera de D-303 fuera del bosque) de todo el mapa ya creado.
    """
    affinity = biomes.get(biome, {}).get("gather", {})
    top_weight = max(affinity.values()) if affinity else 1
    scores = {}
    for res, scale in cfg["region_scale"].items():
        # Each resource has its own patch size; a second, wider noise makes some regions much bigger.
        value = 0.65 * _noise(seed, f"res:{res}", x, y, scale) + 0.35 * _noise(seed, f"res2:{res}", x, y, scale * 2)
        value += cfg["biome_bonus"] * affinity.get(res, 0) / top_weight
        scores[res] = value
    return scores


def zone_resources(seed: int, x: int, y: int, biome: str, balance: dict[str, Any], biomes: dict[str, Any]) -> dict[str, float]:
    """Resources of a zone with their richness (0.3 to 1.0), strongest first.

    [ES]
    Qué hace: devuelve los recursos de la zona y qué tan rica es en cada uno.
    La llama: el servicio (explorar, recolectar, mapa).
    Si cambia, afecta: qué se consigue en cada lugar del mundo.
    """
    cfg = balance["resources"]
    fixed = cfg.get("fixed", {}).get("0:0" if is_bonfire(x, y) else f"{x}:{y}")   # D-265: the 9 bonfires, like the Claro
    if fixed:
        return dict(fixed)
    scores = _base_scores(seed, x, y, biome, cfg, biomes)
    ranked = sorted(scores.items(), key=lambda kv: -kv[1])
    present = [(r, v) for r, v in ranked if v >= cfg["threshold"]][: cfg["max_per_zone"]] or ranked[:1]
    best = present[0][1]
    return {r: round(max(0.3, min(1.0, v / best)), 2) for r, v in present}


def wood_first(x: int, y: int, terrain: str, balance: dict[str, Any]) -> bool:
    """True if this zone's 🪵 wood leads its land resources (D-303): a visible forest terrain, not fixed and not a bonfire.

    [ES]
    Qué hace: dice si la zona es de un terreno de bosque (el que se ve: resources.wood.forest, hoy bosque, bosque oscuro y
    selva) y no es fija ni hoguera. Ahí la 🪵 madera es la más rica (wood_resource) y va PRIMERA en la lista de recursos de
    la zona: se conoce desde la primera exploración (1 %). Sin el bloque resources.wood de content/balance.yaml, nunca.
    La llaman: wood_resource y GameService._zone_resources (pone la madera primera).
    Si cambia, afecta: el orden de los recursos de las zonas de bosque (qué se conoce primero al explorar).
    """
    cfg = balance["resources"]
    wcfg = cfg.get("wood") or {}
    return (bool(wcfg) and terrain in (wcfg.get("forest") or []) and not is_bonfire(x, y)
            and f"{x}:{y}" not in cfg.get("fixed", {}))


def wood_resource(seed: int, x: int, y: int, biome: str, terrain: str, base: dict[str, float], balance: dict[str, Any],
                  biomes: dict[str, Any]) -> dict[str, float]:
    """The 🪵 wood a zone adds on top of its base resources (D-300, D-303), or {}: {"madera": richness}.

    Args:
        biome: the biome its base resources were drawn with (the classic one, mapgen.classic_biome; the lair's own).
        terrain: the terrain the map shows (zone_at().biome): in a forest terrain (resources.wood.forest, wood_first) wood
            is the richest one (resources.wood.forest_min, 1.0), also when it was already a base one.
        base: the zone's base resources (zone_resources); outside a forest, if wood is already one of them, nothing is
            added.

    Every zone that is not fixed nor a bonfire ends up with wood. Wood is only ever added: it never pushes another
    resource out (it may go beyond resources.max_per_zone, and the terrain's own resources are still drawn from the base
    without it), and it uses no new draw: the same seed gives the same wood.

    [ES]
    Qué hace: D-303 (0.41.1, orden del dueño, 20-oct-2026: "los bosques deberían tener, las montañas deberían tener, o sea,
    en todos lugares, en menor medida, pero deberían tener"; los números son de Claude, provisionales; reemplaza los de
    D-300). Toda zona que no es fija ni hoguera tiene 🪵 madera: (1) si su terreno VISIBLE es un bosque (wood_first) la
    madera vale resources.wood.forest_min (1,0, la más rica), aunque ya fuera de base con menos, y GameService la pone
    primera; (2) en los demás terrenos, si ya era de base queda como estaba; si no, se suma pobre: su fuerza (la misma de
    siempre, _base_scores) contra la del más fuerte de la zona, llevada de 0,3 a resources.wood.elsewhere_max (0,5).
    Solo SUMA: nunca saca otro recurso (puede pasar del tope de 3 de base, y una zona puede quedar con 7 recursos de
    tierra) y no usa sorteos nuevos. Las hogueras y el Claro ya tienen madera fija. Sin el bloque resources.wood de
    content/balance.yaml no suma nada (el reparto de antes de D-300). resources.wood.threshold (D-300) ya no se usa.
    La llama: GameService._zone_land. GameService._zone_resources la pone primera en el bosque y, en el resto, justo
    después de los de base (explorar los revela en ese orden; la madera no ocupa un lugar: _known_resources).
    Si cambia, afecta: dónde hay madera para todos y cuánta (recolectar, 🔎 Buscar recursos, el cofre de los campamentos
    enemigos, ⬆️ Agrandar campamento) y tests/test_resources.py.
    """
    cfg = balance["resources"]
    wcfg = cfg.get("wood") or {}
    res = wcfg.get("resource", "madera")
    if not wcfg or not base or is_bonfire(x, y) or f"{x}:{y}" in cfg.get("fixed", {}):
        return {}
    if wood_first(x, y, terrain, balance):            # a forest: the richest wood, also when it was a base one
        return {res: round(min(1.0, max(float(base.get(res, 0.0)), float(wcfg.get("forest_min", 1.0)))), 2)}
    if res in base:                                   # elsewhere a base one stays as it was
        return {}
    scores = _base_scores(seed, x, y, biome, cfg, biomes)
    if res not in scores:
        return {}
    best = max([scores[r] for r in base if r in scores] or [scores[res]])
    share = max(0.0, min(1.0, scores[res] / best)) if best > 0 else 0.0
    low, high = 0.3, max(0.3, float(wcfg.get("elsewhere_max", 0.5)))
    return {res: round(low + (high - low) * share, 2)}


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
