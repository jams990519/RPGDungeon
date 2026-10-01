"""Play the engine in a terminal. Proves the engine does not need Telegram.

Usage: python -m adapters.cli.play [--fast]
  --fast  travel and exploration take 1/600 of real time.

[ES]
Para qué sirve: jugar desde la consola, para probar el motor sin Telegram. Demuestra
que el motor no depende de ningún cliente (D-40).
Documento de diseño: diseno/01-plataforma/web-y-multiplataforma.md §1
Módulo: adaptadores (cliente de consola)
Depende de: engine.service, engine.core, adapters.storage
Lo usan: desarrolladores, para probar a mano
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno (guarda en data/consola.sqlite3)
Reglas que nunca se rompen:
    1. No agrega reglas: solo dibuja vistas y manda acciones.
Si cambias esto, revisa:
    - Nada del juego depende de este archivo
"""

from __future__ import annotations

import sys

from adapters.storage import SqliteStore
from engine.core import SystemClock, load_content
from engine.messaging import View
from engine.service import GameService


def draw(view: View) -> None:
    """Print a view. [ES] Qué hace: dibuja una vista en la consola. La llaman: main. Si cambia, afecta: solo la consola."""
    print("\n" + "=" * 50)
    if view.notice:
        print(view.notice + "\n")
    print(view.title)
    for line in view.body:
        print(line)
    for number, action in enumerate(view.actions, start=1):
        mark = "" if action.enabled else " (no disponible)"
        print(f"  {number}. {action.label}{mark}")


def main() -> None:
    """Run the console loop. [ES] Qué hace: el bucle de juego en consola. La llaman: python -m adapters.cli.play. Si cambia, afecta: solo la consola."""
    fast = "--fast" in sys.argv
    service = GameService(load_content(), SqliteStore("data/consola.sqlite3"), SystemClock(), time_scale=1 / 600 if fast else 1.0)
    account = "console:local"
    view = service.view(account)
    while True:
        draw(view)
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            return
        if raw.lower() in ("q", "salir"):
            return
        if raw.isdigit() and 1 <= int(raw) <= len(view.actions):
            view = service.act(account, view.actions[int(raw) - 1].id)
        elif view.expects_text:
            view = service.text(account, raw)
        else:
            view = service.view(account)


if __name__ == "__main__":
    main()
