"""Play the engine in a terminal. Proves the engine does not need Telegram.

Usage: python -m adapters.cli.play [--fast]
  --fast  travel and exploration take 1/600 of real time.
Type a number to press a button (the global menu comes after the screen's buttons),
a shortcut such as /stats or /doble, or free text when the screen asks for it.

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
    2. Muestra también el menú fijo del motor (service.menu()) y acepta sus atajos
       (service.commands()), como Telegram: sin ellos, de la zona solo se podía viajar. Los atajos con texto
       (/bio <texto>, /saludar <nombre>, D-117) van a service.text(), igual que en Telegram.
Si cambias esto, revisa:
    - Nada del juego depende de este archivo
    - Prueba: tests/test_playtest_fixes.py (la consola llega a Explorar)
"""

from __future__ import annotations

import sys

from adapters.storage import SqliteStore
from engine.core import SystemClock, load_content
from engine.messaging import Action, View
from engine.service import GameService


def options(view: View, service: GameService) -> list[Action]:
    """The screen's buttons, then the global menu (except while creating the hero).

    [ES] Qué hace: junta los botones de la pantalla y el menú fijo, numerados seguidos. La llaman: draw y main.
    Si cambia, afecta: solo la consola.
    """
    if view.kind.startswith("create"):
        return list(view.actions)
    return list(view.actions) + service.menu()


def draw(view: View, service: GameService | None = None) -> None:
    """Print a view. [ES] Qué hace: dibuja una vista en la consola, con el menú fijo al final. La llaman: main. Si cambia, afecta: solo la consola."""
    print("\n" + "=" * 50)
    if view.notice:
        print(view.notice + "\n")
    print(view.title)
    for line in view.body:
        print(line)
    buttons = options(view, service) if service else list(view.actions)
    for number, action in enumerate(buttons, start=1):
        if number == len(view.actions) + 1:
            print("  ---")
        mark = "" if action.enabled else " (no disponible)"
        print(f"  {number}. {action.label}{mark}")


def main() -> None:
    """Run the console loop. [ES] Qué hace: el bucle de juego en consola. La llaman: python -m adapters.cli.play. Si cambia, afecta: solo la consola."""
    fast = "--fast" in sys.argv
    service = GameService(load_content(), SqliteStore("data/consola.sqlite3"), SystemClock(), time_scale=1 / 600 if fast else 1.0)
    account = "console:local"
    view = service.view(account)
    while True:
        draw(view, service)
        buttons = options(view, service)
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            return
        if raw.lower() in ("q", "salir"):
            return
        if raw.isdigit() and 1 <= int(raw) <= len(buttons):
            view = service.act(account, buttons[int(raw) - 1].id)
        elif raw.lower() in service.commands():
            view = service.act(account, service.commands()[raw.lower()])
        elif raw.startswith("/"):
            view = service.text(account, raw)       # D-117: /bio <texto>, /saludar <nombre>, /diario <nombre>...
        elif view.expects_text:
            view = service.text(account, raw)
        else:
            view = service.view(account)


if __name__ == "__main__":
    main()
