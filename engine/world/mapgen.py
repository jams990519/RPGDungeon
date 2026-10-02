"""Deterministic generation of the borderless map.

Each zone is a cell (x, y). Nothing is stored until players change it: the
terrain (biome), name and level come from hashing the world seed with the
coordinates. Since D-186 the terrain looks like a game of Tetris: the map is
cut into 4x4 blocks (odd block rows shifted by 2, like bricks), each block is
tiled by tetrominoes (I, O, T, S, Z, J, L; one of the 117 tilings of a 4x4
square, picked by the seed) and each piece draws its terrain by weight, the
cold ones likelier to the north and the hot ones to the south. Terrains
added later go in a newer "tier" (0.28: tier 1): a piece first checks, with
its own roll, whether it takes a terrain of the newest tier and otherwise
draws exactly as before, so adding terrains only changes the pieces that turn
into a new one. The old climate biome (temperature, humidity, elevation) stays as
classic_biome: the land resource regions still use it (D-185: the
terrain never decides the resources). Lejanía is the ring distance from the
Claro at (0, 0).

[ES]
Para qué sirve: inventar cualquier zona del mapa infinito siempre igual, sin
guardarla, a partir de la semilla del mundo y sus coordenadas.
D-186 (confirmada): el terreno se dibuja como un tablero salteado, "como jugando
Tetris": piezas de 4 zonas (la I, la O, la T, la S, la Z, la J y la L), cada una
de un terreno, encajadas unas con otras; colores, orden y posición cambian. El
mapa se parte en bloques de 4 × 4 (las filas impares corridas 2, como ladrillos)
y cada bloque se llena con una de las 117 formas de cubrir un cuadrado de 4 × 4
con piezas de Tetris. Cada pieza sortea su terreno con el peso de
content/biomes.yaml ("terrain": weight y climate; los fríos salen más al norte y
los calientes más al sur, balance.yaml terrain). Dos piezas vecinas del mismo
terreno se ven como una mancha más grande. El Claro queda fijo.
0.28 (D-188, terrenos nuevos): cada terreno dice en qué tanda se agregó ("tier" en content/biomes.yaml; sin tier, la 0, la de
siempre). Cada pieza mira primero, con un sorteo propio de esa tanda, si le toca un terreno de la tanda más nueva (con la parte
que les toca por peso y clima); si no, sortea entre los de antes EXACTAMENTE como antes. Así agregar terrenos solo cambia las
piezas que pasan a ser de un terreno nuevo (unas 3 de cada 10 en la 0.28): las demás conservan su terreno, sus enemigos,
sus recursos propios y sus nodos. La parte de cada terreno en todo el mapa es la misma que con un sorteo único por peso.
El bioma "clásico" de antes (classic_biome) queda solo para los recursos
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
    - Mundo ya creado: cambiar balance.yaml terrain, los pesos de content/biomes.yaml, las piezas o los sorteos CAMBIA el
      terreno de zonas ya visitadas (sus enemigos, su peligro, sus recursos propios y sus nodos); cambiar classic_biome MUEVE
      los recursos de tierra de un mundo ya creado. Un terreno nuevo va con un "tier" más alto que los que ya estaban: si
      entra en una tanda vieja, cambia el sorteo de casi todo el mapa (la 0.28 lo midió: sin tanda nueva habría cambiado el
      terreno del 77 % de las zonas)
    - Contenido: content/biomes.yaml (terrain), content/enemies.yaml ("biomes": cada terreno con enemigos en cada franja)
    - Servicio: engine/service/game.py — encuentros por bioma y nivel, el color del 🗺️ Mapa (D-179)
    - Pruebas: tests/test_world.py, tests/test_terrenos_nuevos.py
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

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
# and balance.yaml terrain (GameService._terrain_cfg). Each kind: (biome, weight, climate, tier).
# [ES] La tabla por defecto, igual a la de content/biomes.yaml (0.28: los 6 terrenos nuevos, en la tanda 1).
DEFAULT_TERRAIN: tuple = (
    0.02, 3.0,                                      # climate slope per zone of y, climate strength
    (("pradera", 3.0, "any", 0), ("bosque", 3.0, "any", 0), ("colinas", 2.0, "any", 0), ("pantano", 2.0, "any", 0),
     ("montana", 2.0, "any", 0), ("desierto", 2.0, "hot", 0), ("tundra", 2.0, "cold", 0), ("ruinas", 1.0, "any", 0),
     ("selva", 1.5, "hot", 1), ("sabana", 1.5, "hot", 1), ("volcan", 0.5, "any", 1), ("canon", 1.0, "any", 1),   # 0.28 (D-188)
     ("bosque_oscuro", 1.0, "cold", 1), ("lago", 1.0, "any", 1)),
    (),                                             # scattered single zones: (biome, share); none since the Tetris look
)

BLOCK = 4                                           # the 4x4 blocks tiled by tetrominoes
_TETROMINOES = {"I": ((0, 0), (1, 0), (2, 0), (3, 0)), "O": ((0, 0), (1, 0), (0, 1), (1, 1)),
                "T": ((0, 0), (1, 0), (2, 0), (1, 1)), "S": ((1, 0), (2, 0), (0, 1), (1, 1)),
                "L": ((0, 0), (0, 1), (0, 2), (1, 2))}   # Z and J are the mirrors of S and L


@lru_cache(maxsize=1)
def block_tilings() -> tuple[tuple[int, ...], ...]:
    """Every way to tile a 4x4 block with tetrominoes (117): per tiling, the piece number of each cell, row by row.

    [ES]
    Qué hace: calcula una vez todas las formas de cubrir un cuadrado de 4 × 4 con piezas de Tetris (las 19 posiciones de las
    5 piezas, con giros y espejos): 117 formas. Cada una dice, celda por celda, a qué pieza pertenece.
    La llama: terrain_at. Si cambia, afecta: la forma de todas las manchas del mapa.
    """
    fixed = set()
    for cells in _TETROMINOES.values():
        for mirror in (False, True):
            shape = [(-x, y) for x, y in cells] if mirror else list(cells)
            for _ in range(4):
                shape = [(-y, x) for x, y in shape]
                mx, my = min(x for x, _ in shape), min(y for _, y in shape)
                fixed.add(tuple(sorted((x - mx, y - my) for x, y in shape)))
    shapes = sorted(fixed)
    grid, found = [-1] * (BLOCK * BLOCK), []

    def place(piece: int) -> None:
        if -1 not in grid:
            found.append(tuple(grid))
            return
        cell = grid.index(-1)
        ex, ey = cell % BLOCK, cell // BLOCK
        for shape in shapes:
            ax, ay = min(shape, key=lambda c: (c[1], c[0]))      # the shape's first cell lands on the first empty one
            cells = [(ex + x - ax, ey + y - ay) for x, y in shape]
            if all(0 <= x < BLOCK and 0 <= y < BLOCK and grid[y * BLOCK + x] == -1 for x, y in cells):
                for x, y in cells:
                    grid[y * BLOCK + x] = piece
                place(piece + 1)
                for x, y in cells:
                    grid[y * BLOCK + x] = -1

    place(0)
    return tuple(found)


def _weighted_pick(roll: float, weights: list[tuple[str, float]]) -> str:
    """The biome a roll (0..1) lands on, by weight. [ES] Qué hace: el sorteo por peso de siempre. La llama: _piece_terrain."""
    roll *= sum(w for _, w in weights)
    for biome, weight in weights:
        roll -= weight
        if roll <= 0:
            return biome
    return weights[-1][0]


def _piece_terrain(seed: int, key: tuple[int, int, int], py: float, terrain: tuple) -> str:
    """The terrain of one piece: a weighted draw, cold kinds likelier to the north and hot ones to the south.

    Kinds of a newer tier (0.28) are checked first, newest first, each tier with its own roll and its share of the weight
    left; a piece that takes none of them draws among the oldest tier exactly as before (channel "terrain_kind"), so adding
    a tier only changes the pieces that turn into one of its terrains. Each kind still gets weight / total of the pieces.

    [ES]
    Qué hace: sortea el terreno de una pieza por peso y clima. Primero mira la tanda más nueva (0.28: tier 1) con su propio
    sorteo ("terrain_tier:<n>") y la parte del peso que le toca; si no le toca, la que sigue; al final, la tanda 0 con el
    sorteo de siempre. Las piezas que no pasan a un terreno nuevo quedan igual que antes de agregarlo.
    La llama: terrain_at. Si cambia, afecta: el terreno (color, enemigos, peligro, recursos propios y nodos) de todo el mapa.
    """
    slope, strength, kinds, _ = terrain
    temperature = 0.5 - py * slope                  # north (positive y) is colder
    weights = []
    for kind in kinds:
        biome, weight, climate = kind[:3]
        tier = int(kind[3]) if len(kind) > 3 else 0
        mult = 1.0
        if climate == "cold":
            mult = max(0.15, min(3.0, 1 + (0.5 - temperature) * strength))
        elif climate == "hot":
            mult = max(0.15, min(3.0, 1 + (temperature - 0.5) * strength))
        weights.append((biome, weight * mult, tier))
    tiers = sorted({tier for _, _, tier in weights}, reverse=True)
    for tier in tiers[:-1]:                         # newest first; the oldest tier draws as it always did
        left = sum(w for _, w, t in weights if t <= tier)
        mine = [(b, w) for b, w, t in weights if t == tier]
        if hash_unit(seed, f"terrain_tier:{tier}", *key) * left < sum(w for _, w in mine):
            return _weighted_pick(hash_unit(seed, f"terrain_kind:{tier}", *key), mine)
    return _weighted_pick(hash_unit(seed, "terrain_kind", *key), [(b, w) for b, w, t in weights if t == tiers[-1]])


def terrain_at(seed: int, x: int, y: int, terrain: tuple = DEFAULT_TERRAIN) -> str:
    """The terrain (biome id) of a zone on the D-186 Tetris-like map.

    Args:
        terrain: (climate slope, climate strength, ((biome, weight, climate, tier), ...), ((biome, share), ...)); the tier
            (0.28) is optional and 0 when missing.

    [ES]
    Qué hace: el terreno de una zona. Busca su bloque de 4 × 4 (las filas impares de bloques corridas 2 zonas, como
    ladrillos, para que no se vea una cuadrícula), la forma de piezas de Tetris de ese bloque (una de las 117, por la
    semilla) y la pieza donde cae la zona; la pieza sortea su terreno por peso (frío al norte, calor al sur). Los "scatter"
    (si algún terreno los tiene) salen en zonas sueltas encima. El Claro es fijo.
    La llama: zone_at. Si cambia, afecta: el color del mapa, los enemigos y el peligro de cada zona.
    """
    if x == 0 and y == 0:
        return "claro"
    for biome, share in terrain[3]:
        if hash_unit(seed, f"scatter:{biome}", x, y) < share:
            return biome
    by = y // BLOCK
    shifted = x + (BLOCK // 2 if by % 2 else 0)
    bx = shifted // BLOCK
    tilings = block_tilings()
    tiling = tilings[int(hash_unit(seed, "terrain_tiling", bx, by) * len(tilings))]
    piece = tiling[(y - by * BLOCK) * BLOCK + (shifted - bx * BLOCK)]
    return _piece_terrain(seed, (bx, by, piece), by * BLOCK + BLOCK / 2, terrain)


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
