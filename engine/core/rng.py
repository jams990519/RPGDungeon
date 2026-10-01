"""Reproducible randomness: every random draw comes from a saved seed.

Combat stores its seed and a draw counter, so any fight can be replayed
exactly (architecture rule 6). World generation hashes coordinates with the
world seed, so the map is the same on every server restart.

[ES]
Para qué sirve: que todo el azar se pueda repetir. Con la misma semilla sale la
misma pelea y el mismo mapa; así se investigan errores y se mide el balance.
Documento de diseño: diseno/01-plataforma/arquitectura-modular.md §1 regla 6
Módulo: M1 Núcleo
Depende de: ninguno
Lo usan: engine/combat/engine.py, engine/world/mapgen.py, engine/service/game.py
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno
Reglas que nunca se rompen:
    1. Nada del motor usa random global: siempre una Rng con semilla.
    2. hash_unit(seed, *parts) da siempre el mismo valor para los mismos datos.
Si cambias esto, revisa:
    - Mundo: engine/world/mapgen.py — cambiar el hash CAMBIA EL MAPA ENTERO de un mundo ya creado
    - Combate: engine/combat/engine.py — las peleas guardadas dejan de repetirse igual
    - Pruebas: tests/test_world.py, tests/test_combat.py
"""

from __future__ import annotations

import hashlib
import random


class Rng:
    """Seeded random generator that remembers how many draws it made.

    Attributes:
        seed: the starting seed.
        draws: number of values drawn so far (saved with the fight).

    [ES]
    Qué es: un dado con memoria; se puede guardar y retomar en el mismo punto.
    Quién la usa: Combate y el servicio del juego.
    Si cambia, afecta: la repetición exacta de peleas guardadas.
    """

    def __init__(self, seed: int, draws: int = 0) -> None:
        self.seed = seed
        self.draws = 0
        self._random = random.Random(seed)
        for _ in range(draws):
            self.random()

    def random(self) -> float:
        """Return a float in [0, 1). [ES] Qué hace: tira el dado. La llaman: todos los que usan azar. Si cambia, afecta: toda tirada."""
        self.draws += 1
        return self._random.random()

    def chance(self, probability: float) -> bool:
        """Return True with the given probability (0-1). [ES] Qué hace: "¿sale o no sale?". La llaman: Combate, Mundo. Si cambia, afecta: críticos, huidas, encuentros."""
        return self.random() < probability

    def uniform(self, low: float, high: float) -> float:
        """Return a float between low and high. [ES] Qué hace: un número al azar en un rango. La llaman: Combate. Si cambia, afecta: el daño."""
        return low + (high - low) * self.random()

    def pick_weighted(self, items: list, weights: list[float]):
        """Pick one item using weights. [ES] Qué hace: elige uno según su peso. La llaman: Enemigos, Mundo. Si cambia, afecta: qué ataque o qué encuentro sale."""
        total = sum(weights)
        roll = self.random() * total
        upto = 0.0
        for item, weight in zip(items, weights):
            upto += weight
            if roll < upto:
                return item
        return items[-1]


def hash_unit(seed: int | str, *parts: object) -> float:
    """Deterministic value in [0, 1) from a seed and any parts (coordinates, ids).

    [ES]
    Qué hace: convierte "semilla + coordenadas" en un número fijo entre 0 y 1.
    La llaman: engine/world/mapgen.py para generar el mapa infinito.
    Si cambia, afecta: TODO el mapa ya generado (biomas, nombres, peligros).
    """
    text = "|".join(str(p) for p in (seed, *parts))
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") / 2**64
