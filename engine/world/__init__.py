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
Aquí también viven, mientras no exista engine/front, pantry.py: las cuentas de la despensa de M9 (D-93, provisional),
y raids.py: las cuentas de las incursiones y de la Noche de prueba de los campamentos (D-99, provisional).
encounters.py dice qué enemigos pueden salir en cada zona: los del bioma cuya franja de nivel tiene el nivel de la
zona (D-108); lo usan los encuentros del servicio y las incursiones.
enemy_camps.py dice dónde hay 👹 campamentos enemigos cada día (semilla + día), su guarnición y su cofre, y hasta dónde
los ve cada 🧭 Explorador (D-112).
dungeons.py dice dónde están las 🕳️ 🌀 mazmorras para uno (semilla del mundo: nunca se mueven), qué familia de enemigos
las llena cada día, sus salas, sus pisos, su cofre y su bolsa (D-164, D-165, D-170, D-171).
resources.py dice qué recursos tiene cada zona: los 6 de base (D-87), los propios de su terreno (D-180, D-183: catálogo de 10
por terreno, de 4 a 6 por zona) y el pescado de las zonas con agua (D-115).
nodes.py dice dónde hay ✨ nodos de recursos (semilla del mundo: 2 o 3 por tramo de 6 × 6, nunca se mueven) y de qué
recurso es cada uno (D-171, D-181, D-184).
Si cambias esto, revisa:
    - Servicio: engine/service/game.py — viaje, exploración, encuentros y territorio (territory.py, D-81)
    - Encuentros: encounters.py (bioma y franja de nivel de content/enemies.yaml); tests/test_bestiary.py
    - Campamentos enemigos: enemy_camps.py (usa encounters.py y raids.power); tests/test_enemy_camps.py
    - Mazmorras: dungeons.py (usa mapgen.lejania y raids.power; las familias en content/dungeons.yaml); tests/test_mazmorras.py
    - Recursos y nodos: resources.py y nodes.py (nodes.py usa dungeons.entrance_at: un nodo nunca cae en una entrada);
      tests/test_resources.py, tests/test_nodos_y_terrenos.py
    - Pruebas: tests/test_world.py
"""

from engine.world.mapgen import DIRECTIONS, Zone, lejania, ring, zone_at
from engine.world.travel import travel_minutes

__all__ = ["DIRECTIONS", "Zone", "lejania", "ring", "zone_at", "travel_minutes"]
