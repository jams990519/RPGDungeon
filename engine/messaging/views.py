"""View and Action data classes.

[ES]
Para qué sirve: definir la forma de una vista neutra y de cada acción (botón).
Documento de diseño: diseno/01-plataforma/web-y-multiplataforma.md §3
Módulo: M19 Mensajería
Depende de: ninguno
Lo usan: engine/service/game.py, adapters/telegram/render.py, adapters/cli/play.py
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno
Reglas que nunca se rompen:
    1. Los campos solo se agregan (la vista es un contrato con los clientes).
Si cambias esto, revisa:
    - Adaptadores: adapters/telegram/render.py, adapters/cli/play.py
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Action:
    """One thing the player can do now.

    Attributes:
        id: short command id sent back to the engine (<= 64 bytes).
        label: text already translated.
        enabled: False when it cannot be used now (the engine explains why if pressed).

    [ES]
    Qué es: un botón de la vista.
    Quién la usa: el servicio la crea; los clientes la dibujan y devuelven su id.
    Si cambia, afecta: todos los clientes.
    """

    id: str
    label: str
    enabled: bool = True


@dataclass
class View:
    """A screen: title, body lines and actions.

    Attributes:
        kind: screen type ("create", "zone", "combat", "travel", "hero", "bag", "map", ...).
        title: first line.
        body: text lines, already translated.
        actions: buttons, in order; clients lay them out 2 per row.
        notice: optional short line shown first (result of the last command).
        layout: optional buttons per row for the first rows (D-189: an amount picker is [5, 1], a row of small amount
            buttons and one wide back button); the rest go 2 per row. Empty: 2 per row.

    [ES]
    Qué es: una pantalla neutra del juego. D-189: "layout" dice cuántos botones van en cada fila (por ejemplo [5, 1]: una
    fila de botoncitos con la cantidad y un botón ancho de volver); sin layout, 2 por fila.
    Quién la usa: el servicio la devuelve; los clientes la dibujan.
    Si cambia, afecta: todos los clientes.
    """

    kind: str
    title: str
    body: list[str] = field(default_factory=list)
    actions: list[Action] = field(default_factory=list)
    notice: str | None = None
    expects_text: bool = False
    meta: dict = field(default_factory=dict)
    layout: list[int] = field(default_factory=list)
