"""In-process event bus and the engine's domain events.

Modules talk through events instead of importing each other (architecture
rule 3). Handlers run synchronously, in subscription order.

[ES]
Para qué sirve: es el "correo interno" del motor. Un módulo avisa que pasó algo
(un golpe, una llegada) y los que se interesan reaccionan, sin conocerse.
Documento de diseño: diseno/01-plataforma/arquitectura-modular.md §1 regla 3 y §4
Módulo: M1 Núcleo
Depende de: ninguno
Lo usan: engine/service/game.py (publica), telemetría futura (escucha)
Eventos que publica: los define aquí; los publican Combate, Mundo, Héroe y Oficios (ItemCrafted, ProfessionRankUp: D-109)
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno
Reglas que nunca se rompen:
    1. El nombre de un evento es estable como un ID: no se renombra (convenciones §7.2).
    2. Un evento solo agrega campos; nunca se quitan ni cambian de significado.
Si cambias esto, revisa:
    - Servicio: engine/service/game.py — publica todos estos eventos
    - Pruebas: tests/test_service.py
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Callable


@dataclass(frozen=True)
class Event:
    """Base class for every domain event.

    [ES]
    Qué es: la forma común de todos los eventos del motor.
    Quién la usa: cada evento hereda de aquí.
    Si cambia, afecta: a todos los eventos y a quien los escuche.
    """


@dataclass(frozen=True)
class HeroCreated(Event):
    """A new hero entered the world. [ES] HeroeCreado."""
    hero_id: str
    class_id: str


@dataclass(frozen=True)
class TravelStarted(Event):
    """A hero began moving to another zone. [ES] ViajeEmpezado."""
    hero_id: str
    to_x: int
    to_y: int
    arrives_at: float


@dataclass(frozen=True)
class TravelArrived(Event):
    """A hero reached a zone. [ES] ViajeTerminado."""
    hero_id: str
    x: int
    y: int


@dataclass(frozen=True)
class ZoneDiscovered(Event):
    """First visit by anyone to a zone. [ES] ZonaDescubierta (mapa del servidor)."""
    hero_id: str
    x: int
    y: int


@dataclass(frozen=True)
class CombatStarted(Event):
    """A fight began. [ES] CombateEmpezado."""
    hero_id: str
    enemy_id: str
    seed: int


@dataclass(frozen=True)
class HitReceived(Event):
    """Someone took damage. [ES] GolpeRecibido (diseño §4 de la arquitectura)."""
    target_id: str
    amount: int
    critical: bool


@dataclass(frozen=True)
class HeroDowned(Event):
    """A hero reached 0 health. [ES] HeroeDerribado."""
    hero_id: str


@dataclass(frozen=True)
class CombatEnded(Event):
    """A fight ended. outcome: 'victory' | 'defeat' | 'fled'. [ES] CombateTerminado."""
    hero_id: str
    outcome: str


@dataclass(frozen=True)
class BossDefeated(Event):
    """A hero beat a region Guardian (D-82). first_in_server: nobody had beaten it before. [ES] JefeDerrotado."""
    hero_id: str
    enemy_id: str
    first_win: bool
    first_in_server: bool


@dataclass(frozen=True)
class ItemCrafted(Event):
    """A hero refined or crafted at a station (D-109). count: units made this time. [ES] ObjetoFabricado."""
    hero_id: str
    recipe_id: str
    item_id: str
    count: int


@dataclass(frozen=True)
class ProfessionRankUp(Event):
    """A hero's profession reached a new rank (D-109). [ES] RangoDeOficioSubido."""
    hero_id: str
    profession_id: str
    rank: int


Handler = Callable[[Event], None]


@dataclass
class EventBus:
    """Synchronous publish/subscribe bus.

    [ES]
    Qué es: el bus de eventos del núcleo.
    Quién la usa: el servicio del juego lo crea y publica; otros módulos se suscriben.
    Si cambia, afecta: a todo el que publique o escuche eventos.
    """

    _handlers: dict[type, list[Handler]] = field(default_factory=lambda: defaultdict(list))
    history: list[Event] = field(default_factory=list)
    keep_history: int = 200

    def subscribe(self, event_type: type, handler: Handler) -> None:
        """Register a handler for an event type and its subclasses.

        [ES]
        Qué hace: anota a alguien que quiere enterarse de un tipo de evento.
        La llaman: módulos que reaccionan (telemetría, pruebas).
        Si cambia, afecta: el orden en que reaccionan los módulos.
        """
        self._handlers[event_type].append(handler)

    def publish(self, event: Event) -> None:
        """Deliver an event to every matching handler.

        [ES]
        Qué hace: avisa a todos los suscritos a ese evento (o a uno más general).
        La llaman: engine/service/game.py.
        Si cambia, afecta: a todos los que escuchan eventos.
        """
        self.history.append(event)
        if len(self.history) > self.keep_history:
            del self.history[: len(self.history) - self.keep_history]
        for event_type, handlers in list(self._handlers.items()):
            if isinstance(event, event_type):
                for handler in list(handlers):
                    handler(event)
