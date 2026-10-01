"""Game clock. Real time drives travel and other timers (D-58).

Timers are lazy: the engine stores "arrives at" timestamps and settles them
when someone looks, so nothing is lost if the server restarts.

[ES]
Para qué sirve: dar la hora al motor. Los viajes y las exploraciones guardan "a
qué hora terminan" y se cumplen cuando alguien mira (temporizadores perezosos).
Documento de diseño: diseno/02-mundo/mapa-infinito-y-viaje.md; arquitectura §7
Módulo: M1 Núcleo
Depende de: ninguno
Lo usan: engine/service/game.py, adapters (crean el reloj real), tests (reloj fijo)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno
Reglas que nunca se rompen:
    1. El motor nunca llama a time.time() directo: siempre a un Clock (para poder probar).
Si cambias esto, revisa:
    - Servicio: engine/service/game.py — todos los temporizadores
    - Pruebas: tests/test_service.py usan FixedClock
"""

from __future__ import annotations

import time


class Clock:
    """Source of the current time in seconds. [ES] Qué es: el reloj del juego. Quién la usa: el servicio. Si cambia, afecta: todos los temporizadores."""

    def now(self) -> float:
        raise NotImplementedError


class SystemClock(Clock):
    """Wall-clock time. [ES] Qué es: la hora real del servidor. Quién la usa: los adaptadores. Si cambia, afecta: viajes y descansos."""

    def now(self) -> float:
        return time.time()


class FixedClock(Clock):
    """Manually advanced clock for tests and simulations.

    [ES]
    Qué es: un reloj que solo avanza cuando se le pide; sirve para probar viajes sin esperar.
    Quién la usa: tests/ y el cliente de consola.
    Si cambia, afecta: las pruebas.
    """

    def __init__(self, start: float = 1_000_000.0) -> None:
        self._now = start

    def now(self) -> float:
        return self._now

    def advance(self, seconds: float) -> None:
        """Move time forward. [ES] Qué hace: adelanta el reloj. La llaman: pruebas. Si cambia, afecta: pruebas."""
        self._now += seconds
