"""M19 Messaging: neutral views that every client draws its own way.

[ES]
Para qué sirve: lo que el motor devuelve a cualquier cliente: un título, unas
líneas de texto y unas acciones con ID. Telegram las dibuja como mensaje con
botones; la web y la app, a su manera. Nadie recibe más información que otro.
Documento de diseño: diseno/01-plataforma/web-y-multiplataforma.md §3
Módulo: M19 Mensajería
Depende de: ninguno
Lo usan: engine/service/game.py (crea vistas), adapters/* (las dibujan)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno
Reglas que nunca se rompen:
    1. Lo que no se muestra no se envía (web-y-multiplataforma §3.3 regla 1).
    2. Un ID de acción cabe en 64 bytes (límite de callback_data de Telegram).
    3. La vista es un contrato: se agregan campos, no se quitan.
Si cambias esto, revisa:
    - Adaptadores: adapters/telegram/render.py, adapters/cli/play.py
    - Pruebas: tests/test_service.py (largo de los IDs)
"""

from engine.messaging.views import Action, View

__all__ = ["Action", "View"]
