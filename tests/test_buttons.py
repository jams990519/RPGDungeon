"""Press every button reachable from the main screens: no crash, no missing text, at most 4 inline buttons (6 in combat,
8 in the hubs).

[ES] Prueba que todos los botones funcionen: recorre las pantallas pulsando cada botón (D-66). Tope de botones: 4 (D-75),
6 en combate (D-46), hasta 8 de 2 en 2 en los centros de 🏕️ Campamento y 👤 Héroe y en ❓ Dudas (D-192, E-132: HUB_KINDS) y
las filas de cantidades de D-189. D-244 (0.33): 📍 Zona trae 5 botones ([2, 2, 1]) y 🔗 Moverte sus flechas en una fila y
❌ Cancelar y ✅ Terminar juntos al final ([4, 2] o [4, 1, 2]).
"""

from collections import deque

from conftest import make_hero
from engine.core import FixedClock, MemoryStore
from engine.service import GameService
from engine.service.game import HUB_BUTTONS, HUB_KINDS

SKIP = ("go:", "goto:", "explore", "gather", "inn", "found", "respec", "donate")


def build(content, path):
    service = GameService(content, MemoryStore(), FixedClock(), world_seed=7)
    make_hero(service, "test:1", "Lyra", "paladin_reprension")
    view = service.view("test:1")
    for action in path:
        view = service.act("test:1", action)
    return service, view


def test_every_button_works(content):
    seen, queue, pressed = set(), deque([[]]), 0
    while queue and pressed < 300:
        path = queue.popleft()
        service, view = build(content, path)
        pressed += 1
        # D-46 combat bar; D-192 (E-132): the hubs show up to 8, 2 per row; 4 elsewhere (D-75)
        limit = 6 if view.kind == "combat" else HUB_BUTTONS if view.kind in HUB_KINDS else 4
        if view.layout:                                 # D-189: amount pickers: a row of small amounts and one wide back
            assert sum(view.layout) == len(view.actions) and max(view.layout) <= 8, (path, view.layout)
            # D-244: 🔗 Moverte closes with two buttons side by side (❌ Cancelar, ✅ Terminar)
            assert view.layout[-1] == 1 or view.kind == "walk", (path, view.layout)
        else:
            assert len(view.actions) <= limit, (path, view.kind, len(view.actions))
        assert len(service.menu()) <= 6
        assert not service.texts.missing, (path, service.texts.missing)
        key = (view.kind, tuple(a.id for a in view.actions))
        if key in seen:
            continue
        seen.add(key)
        for action_id in [a.id for a in view.actions] + [m.id for m in service.menu()]:
            if len(path) < 4 and not action_id.startswith(SKIP):
                queue.append(path + [action_id])
    assert len(seen) >= 8


def test_creation_buttons_go_back(content):
    service = GameService(content, MemoryStore(), FixedClock(), world_seed=7)
    service.view("test:2")
    first = service.text("test:2", "Nadie")
    assert len(first.actions) <= 4
    page2 = service.act("test:2", "page:1")
    detail = service.act("test:2", page2.actions[0].id)
    assert any(a.id == "grp:" for a in detail.actions)
    back = service.act("test:2", "grp:")
    assert back.kind == "create_class" and back.actions == page2.actions
