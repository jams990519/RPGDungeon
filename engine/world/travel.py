"""Travel time between neighbouring zones (D-58: moving takes time).

[ES]
Para qué sirve: calcular cuántos minutos reales tarda ir a una zona vecina. D-197 (confirmada):
1 minuto por cuadro, cerca o lejos (10 cuadros = 10 minutos). La fórmula vieja de D-78 (las 2
primeras zonas desde el Claro o tu campamento 2 minutos, las 2 siguientes 3, luego 4...) sigue
disponible si balance.yaml travel.steps_per_minute vuelve a ser mayor que 0.
Documento de diseño: diseno/02-mundo/mapa-infinito-y-viaje.md (el viaje)
Módulo: M8 Mundo
Depende de: content/balance.yaml (travel.first_minutes, steps_per_minute, max_minutes)
Lo usan: engine/service/game.py
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno
Reglas que nunca se rompen:
    1. Ningún viaje tarda 0: el mínimo es travel.first_minutes (D-58, D-197).
    2. Moverse no gasta energía, solo tiempo (D-190, D-197).
    3. Con steps_per_minute > 0, al fundar o agrandar tu campamento la cuenta vuelve a empezar desde su borde.
Si cambias esto, revisa:
    - Números: balance.yaml travel.* (ritmo de todo el juego)
    - Servicio: engine/service/game.py (_anchors: el Claro y el campamento del héroe)
    - Pruebas: tests/test_world.py
"""

from __future__ import annotations

from typing import Any


def anchor_distance(x: int, y: int, anchors: list[tuple[int, int, int]]) -> int:
    """Rings from (x, y) to the nearest anchor (x, y, radius); 0 inside an anchor's area.

    [ES]
    Qué hace: cuántas zonas hay hasta el punto de partida más cercano (el Claro o tu campamento,
    contando las zonas que ocupa el campamento).
    La llama: travel_minutes y el servicio.
    Si cambia, afecta: el tiempo de todos los viajes.
    """
    return min(max(0, max(abs(x - ax), abs(y - ay)) - radius) for ax, ay, radius in anchors)


def travel_minutes(x: int, y: int, anchors: list[tuple[int, int, int]], balance: dict[str, Any]) -> float:
    """Minutes of real time to walk into zone (x, y): flat travel.first_minutes per zone (D-197), or growing with distance.

    With travel.steps_per_minute > 0 the old D-78 rule applies: 2, 2, 3, 3, 4, 4... by distance to the nearest anchor.

    Args:
        x, y: destination zone.
        anchors: (x, y, radius) of the Claro and of the hero's camp.
        balance: content/balance.yaml.

    Returns:
        minutes (before the server time scale).

    [ES]
    Qué hace: tiempo a pie hacia la zona (x, y). D-197: 1 minuto por cuadro, siempre igual
    (travel.steps_per_minute 0). Si steps_per_minute vuelve a ser N > 0, cada N zonas más lejos del
    Claro o de tu campamento suma 1 minuto, hasta el tope (la regla vieja de D-78).
    La llaman: el servicio al mostrar rutas y al empezar un viaje.
    Si cambia, afecta: el ritmo del juego y el valor de fundar campamentos lejos.
    """
    cfg = balance["travel"]
    per = int(cfg.get("steps_per_minute", 0))
    if per <= 0:                                       # D-197: the same time for every zone, near or far
        return float(cfg["first_minutes"])
    steps = max(1, anchor_distance(x, y, anchors))
    minutes = cfg["first_minutes"] + (steps - 1) // per
    return float(min(cfg["max_minutes"], minutes))
