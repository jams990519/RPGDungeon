"""Travel time between neighbouring zones (D-58: moving takes time).

[ES]
Para qué sirve: calcular cuántos minutos reales tarda ir a una zona vecina.
Documento de diseño: diseno/02-mundo/mapa-infinito-y-viaje.md (el viaje)
Módulo: M8 Mundo
Depende de: content/biomes.yaml (travel_minutes), content/balance.yaml (travel.*)
Lo usan: engine/service/game.py
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno
Reglas que nunca se rompen:
    1. Ningún viaje tarda 0: el mínimo es 1 minuto antes de la escala de tiempo (D-58).
Si cambias esto, revisa:
    - Números: biomes.yaml travel_minutes, balance.yaml travel.* (ritmo de todo el juego)
    - Pruebas: tests/test_world.py
"""

from __future__ import annotations

from typing import Any

from engine.world.mapgen import Zone


def travel_minutes(origin: Zone, destination: Zone, biomes: dict[str, Any], balance: dict[str, Any], discovered: bool) -> float:
    """Minutes of real time to walk from origin into a neighbouring destination.

    Args:
        origin, destination: neighbouring zones.
        biomes: content/biomes.yaml.
        balance: content/balance.yaml.
        discovered: whether anyone already discovered the destination.

    Returns:
        minutes (before the server time scale).

    [ES]
    Qué hace: tiempo a pie hacia la zona vecina: depende del bioma de destino, de si
    hay senderos cerca del Claro y de si la zona ya está descubierta.
    La llaman: el servicio al mostrar rutas y al empezar un viaje.
    Si cambia, afecta: el ritmo del juego y el valor de los caminos futuros.
    """
    travel = balance.get("travel", {})
    minutes = float(biomes[destination.biome]["travel_minutes"])
    if origin.lejania <= 1 and destination.lejania <= 1:
        minutes *= travel.get("near_claro_factor", 1.0)
    if not discovered:
        minutes *= travel.get("unknown_zone_factor", 1.0)
    return max(1.0, minutes)
