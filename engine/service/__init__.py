"""Game service: the single entry point clients use (commands in, views out).

[ES]
Para qué sirve: la puerta del motor para todos los clientes (Telegram, consola, la
web en el futuro). Recibe órdenes y devuelve vistas neutras.
Documento de diseño: diseno/01-plataforma/web-y-multiplataforma.md §2 (servicios de juego)
Módulo: capa de servicios (une M1, M2, M3, M5, M6, M8, M19)
Depende de: engine.core, engine.hero, engine.world, engine.combat, engine.messaging
Lo usan: adapters/telegram, adapters/cli, tests
Eventos que publica: los de engine.core.events
Eventos que escucha: ninguno
Datos de los que es dueño: coordina "hero", "combat", "zone", "pending" y "meta"
Reglas que nunca se rompen:
    1. Los clientes solo hablan con GameService, nunca con los módulos internos.
Si cambias esto, revisa:
    - Adaptadores: adapters/telegram/bot.py, adapters/cli/play.py
    - Pruebas: tests/test_service.py
"""

from engine.service.game import GameService

__all__ = ["GameService"]
