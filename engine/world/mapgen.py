"""Deterministic generation of the borderless map.

Each zone is a cell (x, y). Nothing is stored until players change it: the
terrain (biome), name and level come from hashing the world seed with the
coordinates. Since D-186 the terrain is a patchwork: patches of a few zones
each (a jittered grid, every zone joins its nearest patch centre), each patch
a terrain drawn by weight, the cold ones likelier to the north and the hot ones
to the south. The old climate biome (temperature, humidity, elevation) stays as
classic_biome: the land resource regions still use it (D-185: the
terrain never decides the resources). Lejanía is the ring distance from the
Claro at (0, 0).

[ES]
Para qué sirve: inventar cualquier zona del mapa infinito siempre igual, sin
guardarla, a partir de la semilla del mundo y sus coordenadas.
D-186 (confirmada): el terreno se dibuja como un tablero salteado: manchas de
pocas zonas (3 a 12, de tamaño y forma variados) de distintos colores, unas al
lado de otras. Cada mancha sortea su terreno con el peso de content/biomes.yaml
("terrain": weight y climate; los fríos salen más al norte y los calientes más
al sur, balance.yaml terrain). Las 🏚️ ruinas siguen sueltas (scatter) y el Claro
fijo. El bioma "clásico" de antes (classic_biome) queda solo para los recursos
de tierra, así lo que los jugadores ya conocen de cada zona no se movió (D-185);
el agua (la pesca) sí sigue al terreno que se ve: un pantano siempre tiene agua.
Documento de diseño: diseno/02-mundo/mapa-infinito-y-viaje.md (vocabulario: zona, Lejanía, anillo)
Módulo: M8 Mundo
Depende de: engine.core.hash_unit, content/biomes.yaml, content/locales (partes de nombres)
Lo usan: engine/world/travel.py, engine/service/game.py (zone_at para todo; classic_biome para _zone_resources)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno
Reglas que nunca se rompen:
    1. zone_at(seed, x, y) es determinista: mismo resultado siempre.
    2. (0, 0) es siempre el Claro, Lejanía 0, sin peligro.
Si cambias esto, revisa:
    - Mundo ya creado: cambiar balance.yaml terrain, los pesos de content/biomes.yaml o los sorteos CAMBIA el terreno de
      zonas ya visitadas (sus enemigos y su peligro); cambiar classic_biome MUEVE los recursos de tierra de un mundo ya creado
    - Servicio: engine/service/game.py — encuentros por bioma y nivel, el color del 🗺️ Mapa (D-179)
    - Pruebas: tests/test_world.py
"""

from __future__ import annotations

from dataclasses import dataclass

from engine.core.rng import hash_unit

DIRECTIONS: dict[str, tuple[int, int]] = {"n": (0, 1), "s": (0, -1), "e": (1, 0), "w": (-1, 0)}


@dataclass(frozen=True)
class Zone:
    """One cell of the infinite map.

    [ES]
    Qué es: una zona del mapa (en el diseño, "zona", con su bioma y su Lejanía).
    Quién la usa: el servicio para mostrar lugares, calcular viajes y elegir enemigos.
    Si cambia, afecta: vistas, viaje y encuentros.
    """

    x: int
    y: int
    biome: str
    lejania: int
    ring: int
    level: int
    name_index: tuple[int, int]


def lejania(x: int, y: int) -> int:
    """Ring distance from the Claro. [ES] Qué hace: cuántas zonas hay hasta el Claro. La llaman: generación, viaje. Si cambia, afecta: peligro y nivel de todo el mapa."""
    return max(abs(x), abs(y))


def ring(dist: int) -> int:
    """Ring number (I-X) for a Lejanía; 0 is the Claro. [ES] Qué hace: el anillo de una Lejanía (de 3 en 3, tope X). La llaman: generación. Si cambia, afecta: tiers y vistas."""
    if dist == 0:
        return 0
    return min(10, 1 + (dist - 1) // 3)


def _smooth_noise(seed: int, channel: str, x: int, y: int, scale: int = 4) -> float:
    """Value noise: interpolate hashed values on a coarse grid so biomes form patches."""
    gx, gy = x // scale, y // scale
    fx, fy = (x % scale) / scale, (y % scale) / scale

    def corner(cx: int, cy: int) -> float:
        return hash_unit(seed, channel, cx, cy)

    top = corner(gx, gy) * (1 - fx) + corner(gx + 1, gy) * fx
    bottom = corner(gx, gy + 1) * (1 - fx) + corner(gx + 1, gy + 1) * fx
    return top * (1 - fy) + bottom * fy


def classic_biome(seed: int, x: int, y: int) -> str:
    """The climate biome of before D-186 (temperature, humidity, elevation): only the resource regions and the water use it.

    [ES]
    Qué hace: el bioma "clásico" de una zona, el que se usaba antes del tablero de terrenos (D-186). Ya no se ve en el mapa:
    solo lo usan los recursos de tierra (_zone_resources), para que no se moviera nada de lo que se conoce (D-185).
    La llama: GameService._zone_resources. Si cambia, afecta: los recursos de tierra de todo el mapa ya creado.
    """
    if x == 0 and y == 0:
        return "claro"
    temperature = 0.5 - y * 0.03 + (_smooth_noise(seed, "temp", x, y, 6) - 0.5) * 0.4
    humidity = _smooth_noise(seed, "hum", x, y)
    elevation = _smooth_noise(seed, "elev", x, y, 5)
    if hash_unit(seed, "ruins", x, y) < 0.06:
        return "ruinas"
    if elevation > 0.72:
        return "tundra" if temperature < 0.35 else "montana"
    if temperature < 0.2:
        return "tundra"
    if temperature > 0.75 and humidity < 0.5:
        return "desierto"
    if humidity > 0.7:
        return "pantano"
    if humidity > 0.45:
        return "bosque"
    if elevation > 0.55:
        return "colinas"
    return "pradera"


# D-186: default terrain table for direct calls (tests, tools); the service passes the one built from content/biomes.yaml
# and balance.yaml terrain (GameService._terrain_cfg). [ES] La tabla por defecto, igual a la de content/biomes.yaml.
DEFAULT_TERRAIN: tuple = (
    3, 0.02, 3.0,                                   # patch size, climate slope per zone of y, climate strength
    (("pradera", 3.0, "any"), ("bosque", 3.0, "any"), ("colinas", 2.0, "any"), ("pantano", 2.0, "any"),
     ("montana", 2.0, "any"), ("desierto", 2.0, "hot"), ("tundra", 2.0, "cold")),
    (("ruinas", 0.06),),                            # scattered single zones: (biome, share)
)


def _patch_terrain(seed: int, cx: int, cy: int, py: float, terrain: tuple) -> str:
    """The terrain of one patch centre: a weighted draw, cold kinds likelier to the north and hot ones to the south."""
    _, slope, strength, kinds, _ = terrain
    temperature = 0.5 - py * slope                  # north (positive y) is colder
    weights = []
    for biome, weight, climate in kinds:
        mult = 1.0
        if climate == "cold":
            mult = max(0.15, min(3.0, 1 + (0.5 - temperature) * strength))
        elif climate == "hot":
            mult = max(0.15, min(3.0, 1 + (temperature - 0.5) * strength))
        weights.append((biome, weight * mult))
    roll = hash_unit(seed, "terrain_kind", cx, cy) * sum(w for _, w in weights)
    for biome, weight in weights:
        roll -= weight
        if roll <= 0:
            return biome
    return weights[-1][0]


def terrain_at(seed: int, x: int, y: int, terrain: tuple = DEFAULT_TERRAIN) -> str:
    """The terrain (biome id) of a zone on the D-186 patchwork.

    Args:
        terrain: (patch size, climate slope, climate strength, ((biome, weight, climate), ...), ((biome, share), ...)).

    [ES]
    Qué hace: el terreno de una zona. El mapa se parte en una rejilla de patch × patch con un centro movido al azar en cada
    casilla; cada zona se une al centro más cercano, así salen manchas de tamaño y forma variados (de unas 3 a 12 zonas), y
    cada mancha sortea su terreno por peso (frío al norte, calor al sur). Encima, algunas zonas sueltas son 🏚️ ruinas.
    La llama: zone_at. Si cambia, afecta: el color del mapa, los enemigos y el peligro de cada zona.
    """
    if x == 0 and y == 0:
        return "claro"
    patch, _, _, _, scattered = terrain
    for biome, share in scattered:
        if hash_unit(seed, f"scatter:{biome}" if biome != "ruinas" else "ruins", x, y) < share:
            return biome
    gx, gy = x // patch, y // patch
    best = None
    for cx in (gx - 1, gx, gx + 1):
        for cy in (gy - 1, gy, gy + 1):
            px = cx * patch + hash_unit(seed, "terrain_px", cx, cy) * patch
            py = cy * patch + hash_unit(seed, "terrain_py", cx, cy) * patch
            dist = (px - x - 0.5) ** 2 + (py - y - 0.5) ** 2
            if best is None or dist < best[0]:
                best = (dist, cx, cy, py)
    return _patch_terrain(seed, best[1], best[2], best[3], terrain)


def zone_at(seed: int, x: int, y: int, level_per_lejania: float = 0.9, name_parts: tuple[int, int] = (10, 10),
            terrain: tuple = DEFAULT_TERRAIN) -> Zone:
    """Generate the zone at (x, y) for a world seed.

    Args:
        seed: world seed (stored once in the "meta" namespace).
        x, y: coordinates; any integers (the map has no border).
        level_per_lejania: balance number from balance.yaml travel.level_per_lejania.
        name_parts: sizes of the two name-part lists in the locale file.
        terrain: the D-186 terrain table (terrain_at); the service builds it from content/biomes.yaml and balance.yaml.

    [ES]
    Qué hace: devuelve la zona de esas coordenadas, siempre igual para la misma semilla.
    La llaman: el servicio y el cálculo de viaje.
    Si cambia, afecta: todo el mapa.
    """
    dist = lejania(x, y)
    first = int(hash_unit(seed, "name1", x, y) * name_parts[0])
    second = int(hash_unit(seed, "name2", x, y) * name_parts[1])
    return Zone(
        x=x,
        y=y,
        biome=terrain_at(seed, x, y, terrain),
        lejania=dist,
        ring=ring(dist),
        level=max(1, round(1 + dist * level_per_lejania)),
        name_index=(first, second),
    )
