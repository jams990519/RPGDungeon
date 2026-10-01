"""Camp territory: a camp covers 1 zone, then 2, 3, 4... as it grows (D-81).

[ES]
Para qué sirve: decir qué zonas ocupa un campamento. Al fundarlo ocupa 1 zona; cada vez que se
agranda suma la siguiente zona de una espiral alrededor del centro (norte, este, sur, oeste, las
diagonales y luego el anillo siguiente), saltando las zonas que ya son de otro.
Documento de diseño: diseno/02-mundo/mapa-infinito-y-viaje.md §1.9 (campamentos que crecen)
Módulo: M8 Mundo (territorio)
Depende de: ninguno
Lo usan: engine/service/game.py (agrandar campamentos, Claro, viaje, encuentros)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno (el servicio guarda las zonas en el espacio "camp" y "territory")
Reglas que nunca se rompen:
    1. El orden de la espiral nunca cambia: cambiarlo movería el territorio del Claro ya crecido.
    2. Una zona es de un solo campamento.
Si cambias esto, revisa:
    - Servicio: engine/service/game.py (_claro_zones, _grow_camp, _anchors)
    - Viaje: engine/world/travel.py (la distancia se cuenta desde cualquier zona del territorio)
    - Pruebas: tests/test_camps.py
"""

from __future__ import annotations

from collections.abc import Callable, Iterator

FIRST_RING = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]


def spiral() -> Iterator[tuple[int, int]]:
    """Offsets around a center: (0, 0), then N, E, S, W, the diagonals, then ring 2 and so on.

    [ES]
    Qué hace: da, en orden fijo, las zonas alrededor de un centro hacia donde crece un campamento.
    La llaman: next_zone y claro_zones.
    Si cambia, afecta: qué zonas ocupan todos los campamentos (romper el orden mueve territorios).
    """
    yield (0, 0)
    yield from FIRST_RING
    radius = 2
    while True:
        ring = [(dx, dy) for dx in range(-radius, radius + 1) for dy in range(-radius, radius + 1) if max(abs(dx), abs(dy)) == radius]
        ring.sort(key=lambda p: (abs(p[0]) + abs(p[1]), p[1] < 0, p[0] < 0, p))
        yield from ring
        radius += 1


def first_zones(cx: int, cy: int, count: int) -> list[list[int]]:
    """The first `count` zones of the spiral around (cx, cy), with nothing blocked. [ES] Qué hace: zonas del Claro según su etapa. La llama: el servicio. Si cambia, afecta: el territorio del Claro."""
    out = []
    for dx, dy in spiral():
        if len(out) >= count:
            break
        out.append([cx + dx, cy + dy])
    return out


def next_zone(cx: int, cy: int, owned: list[list[int]], is_free: Callable[[int, int], bool], limit: int = 200) -> list[int] | None:
    """Next spiral zone around (cx, cy) that the camp does not own yet and nobody else holds.

    [ES]
    Qué hace: elige la zona que suma un campamento al agrandarse, saltando las de otros.
    La llama: el servicio al agrandar un campamento.
    Si cambia, afecta: hacia dónde crecen los campamentos.
    """
    mine = {(x, y) for x, y in owned}
    for i, (dx, dy) in enumerate(spiral()):
        if i >= limit:
            return None
        x, y = cx + dx, cy + dy
        if (x, y) not in mine and is_free(x, y):
            return [x, y]
    return None
