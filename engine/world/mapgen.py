"""Deterministic generation of the borderless map.

Each zone is a cell (x, y). Nothing is stored until players change it: the
biome, name and level come from hashing the world seed with the coordinates.
North (positive y) is colder, south is warmer; noise adds humidity and
elevation. Lejanía is the ring distance from the Claro at (0, 0).

[ES]
Para qué sirve: inventar cualquier zona del mapa infinito siempre igual, sin
guardarla, a partir de la semilla del mundo y sus coordenadas.
Documento de diseño: diseno/02-mundo/mapa-infinito-y-viaje.md (vocabulario: zona, Lejanía, anillo)
Módulo: M8 Mundo
Depende de: engine.core.hash_unit, content/biomes.yaml, content/locales (partes de nombres)
Lo usan: engine/world/travel.py, engine/service/game.py
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno
Reglas que nunca se rompen:
    1. zone_at(seed, x, y) es determinista: mismo resultado siempre.
    2. (0, 0) es siempre el Claro, Lejanía 0, sin peligro.
Si cambias esto, revisa:
    - Mundo ya creado: cambiar umbrales o el ruido CAMBIA los biomas de zonas ya visitadas
    - Servicio: engine/service/game.py — encuentros por bioma y nivel
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


def _biome(seed: int, x: int, y: int) -> str:
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


def zone_at(seed: int, x: int, y: int, level_per_lejania: float = 0.9, name_parts: tuple[int, int] = (10, 10)) -> Zone:
    """Generate the zone at (x, y) for a world seed.

    Args:
        seed: world seed (stored once in the "meta" namespace).
        x, y: coordinates; any integers (the map has no border).
        level_per_lejania: balance number from balance.yaml travel.level_per_lejania.
        name_parts: sizes of the two name-part lists in the locale file.

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
        biome=_biome(seed, x, y),
        lejania=dist,
        ring=ring(dist),
        level=max(1, round(1 + dist * level_per_lejania)),
        name_index=(first, second),
    )
