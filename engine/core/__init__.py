"""M1 Core: events, seeded randomness, clock, content, texts and storage port.

[ES]
Para qué sirve: lo que todos los módulos necesitan (eventos, azar con semilla,
reloj, contenido, textos y la interfaz de guardado). Los demás importan desde aquí.
Documento de diseño: diseno/01-plataforma/arquitectura-modular.md §2 (M1)
Módulo: M1 Núcleo
Depende de: ninguno
Lo usan: todos los módulos del motor
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: espacio "meta" del almacén (semilla del mundo)
Reglas que nunca se rompen:
    1. Los demás módulos importan solo desde engine.core, no desde sus archivos internos.
Si cambias esto, revisa:
    - Todo el motor
"""

from engine.core.clock import Clock, FixedClock, SystemClock
from engine.core.content import Content, load_content
from engine.core.events import (
    CombatEnded,
    CombatStarted,
    Event,
    EventBus,
    HeroCreated,
    HeroDowned,
    HitReceived,
    TravelArrived,
    TravelStarted,
    ZoneDiscovered,
)
from engine.core.i18n import Texts
from engine.core.rng import Rng, hash_unit
from engine.core.store import MemoryStore, Store

__all__ = [
    "Clock", "FixedClock", "SystemClock", "Content", "load_content", "Event", "EventBus",
    "HeroCreated", "HeroDowned", "HitReceived", "TravelArrived", "TravelStarted",
    "ZoneDiscovered", "CombatStarted", "CombatEnded", "Texts", "Rng", "hash_unit",
    "MemoryStore", "Store",
]
