"""M8 World: the infinite map (D-58) and travel that takes real time.

[ES]
Para qué sirve: el mapa sin borde, generado con semilla cuando alguien lo explora,
y el viaje entre zonas que toma tiempo real.
Documento de diseño: diseno/02-mundo/mapa-infinito-y-viaje.md (D-58)
Módulo: M8 Mundo
Depende de: engine.core (semilla y hash), content/biomes.yaml, content/balance.yaml
Lo usan: engine/service/game.py
Eventos que publica: ninguno (el servicio publica TravelArrived y ZoneDiscovered)
Eventos que escucha: ninguno
Datos de los que es dueño: espacio "zone" del almacén (solo zonas que cambiaron los jugadores)
Reglas que nunca se rompen:
    1. La misma semilla da siempre el mismo mapa (D-58, arquitectura regla 6).
    2. Moverse entre zonas toma tiempo; no hay teletransporte (D-58).
Si cambias esto, revisa:
    - Servicio: engine/service/game.py — viaje, exploración, encuentros y territorio (territory.py, D-81)
    - Pruebas: tests/test_world.py
"""

from engine.world.mapgen import DIRECTIONS, Zone, lejania, ring, zone_at
from engine.world.travel import travel_minutes

__all__ = ["DIRECTIONS", "Zone", "lejania", "ring", "zone_at", "travel_minutes"]
