"""📒 Lugares: only the important places you know, each with a code, and a confirmation before travelling (D-223, 0.30.2).

[ES] Pruebas de 📒 Lugares. La lista trae solo los lugares importantes que ya visitaste: el 🔥 Claro (siempre), los
🏕️ campamentos de jugadores, las 🕳️ 🌀 mazmorras y la 👑 guarida; las zonas comunes no. Cada lugar tiene su código (/ir1,
/ir2...) y los 3 más cercanos un botón; elegir uno (botón o código) pregunta antes de viajar, y al confirmar el héroe va
solo, zona por zona. Un código que no está en la lista no hace nada raro. Ningún texto falta. 0.33 (pedido del dueño:
"debería dejarme ir hacia la fogata"): estando ocupado también se puede ir: un lote se corta, un viaje cambia el rumbo y
solo descansando en la posada hay que esperar.
Archivo: tests/test_lugares.py · Módulo: M8 Mundo y mapa · Prueba: engine/service/game.py (_important_places,
_places_view, _place_confirm_view, _place_code, "goask:", "goto:" y el texto /irN).
"""

from conftest import make_hero


def place(service, x, y, known=()):
    hero = service._load("test:1")
    hero.x, hero.y = x, y
    hero.known = sorted(set(hero.known) | set(known) | {f"{x}:{y}"})
    service._save(hero)
    return hero


def dungeon_near(service):
    for r in range(2, 30):
        for x in range(-r, r + 1):
            for y in (-r, r):
                if service._dng_kind(x, y):
                    return x, y
    raise AssertionError("no dungeon found")


def ordinary(service, count=2):
    """Zones near the Claro with nothing important in them (no dungeon, camp or lair)."""
    out = []
    for x in range(-3, 4):
        for y in range(-3, 4):
            if (x, y) != (0, 0) and not service._dng_kind(x, y) and not service._is_lair(x, y) \
                    and not service.store.get("camp", f"{x}:{y}"):
                out.append((x, y))
    return out[:count]


def test_only_important_places_are_listed(service):
    make_hero(service)
    dx, dy = dungeon_near(service)
    plain = ordinary(service)
    place(service, 0, 0, known=[f"{x}:{y}" for x, y in plain] + [f"{dx}:{dy}"])
    place(service, plain[0][0], plain[0][1])
    view = service.act("test:1", "places")
    lines = [line for line in view.body if "/ir" in line]
    assert any(line.startswith(("1. 🔥", "2. 🔥")) for line in lines)                 # the Claro, always
    assert any("mazmorra" in line for line in lines)                                  # the dungeon you visited
    name = service._zone_name(service._zone(*plain[1]))
    assert not any(name in line for line in lines)                                    # ordinary zones: not listed
    assert all(a.id.startswith("goask:") for a in view.actions[:-1]) and view.actions[-1].id == "map"
    assert len(view.actions) <= 4
    assert not service.texts.missing


def test_a_button_asks_first_and_then_you_travel(service):
    make_hero(service)
    place(service, 0, 3, known=["0:1", "0:2"])
    view = service.act("test:1", "goask:0:0")
    assert view.kind == "place_confirm" and [a.id for a in view.actions] == ["goto:0:0", "places"]
    assert not service._load("test:1").activity                                      # nothing happens before confirming
    assert service.act("test:1", "places").kind == "places"                           # "No, volver"
    service.act("test:1", "goto:0:0")
    hero = service._load("test:1")
    assert hero.activity["kind"] == "travel" and hero.activity["goal"] == [0, 0]
    assert not service.texts.missing


def test_a_code_asks_first_too(service):
    make_hero(service)
    place(service, 0, 3, known=["0:1", "0:2"])
    service.act("test:1", "places")
    first = service._important_places(service._load("test:1"))[0]
    view = service.text("test:1", "/ir1")
    assert view.kind == "place_confirm" and view.actions[0].id == f"goto:{first[1]}:{first[2]}"
    assert service.text("test:1", "/ir_1").kind == "place_confirm"
    view = service.text("test:1", "/ir9")                                             # not on the list: back to it
    assert view.kind == "places" and view.notice
    assert not service._load("test:1").activity
    assert not service.texts.missing


def test_you_cannot_ask_for_a_place_you_never_visited(service):
    make_hero(service)
    dx, dy = dungeon_near(service)
    place(service, 0, 3)
    view = service.act("test:1", f"goask:{dx}:{dy}")
    assert view.kind == "places" and view.notice                                      # not one of your places
    service.act("test:1", f"goto:{dx}:{dy}")
    assert not service._load("test:1").activity
    assert not service.texts.missing


def test_exploring_you_can_still_go_to_the_bonfire(service):
    """0.33 (the owner: "debería dejarme ir hacia la fogata"): busy exploring, /ir2 no longer says "not on your list"."""
    make_hero(service)
    place(service, 0, 3, known=["0:1", "0:2"])
    service.act("test:1", "explore")
    service.act("test:1", "do:explore:5")
    hero = service._load("test:1")
    assert hero.activity["kind"] == "explore"
    energy = hero.energy
    service.act("test:1", "places")
    view = service.act("test:1", "goask:0:0")
    assert view.kind == "place_confirm" and "⏹️" in "\n".join(view.body)          # it says the batch will be cut
    view = service.act("test:1", "goto:0:0")
    hero = service._load("test:1")
    assert hero.activity["kind"] == "travel" and hero.activity["goal"] == [0, 0]
    assert hero.energy >= energy                                                   # the step in progress gave its energy back
    assert view.notice and not service.texts.missing


def test_travelling_you_can_change_course(service):
    make_hero(service)
    place(service, 0, 3, known=["0:1", "0:2", "1:3"])
    service.act("test:1", "go:e")
    hero = service._load("test:1")
    assert hero.activity["kind"] == "travel" and hero.activity["to"] == [1, 3]
    view = service.act("test:1", "goask:0:0")
    assert view.kind == "place_confirm" and "🧭" in view.body[-1]
    service.act("test:1", "goto:0:0")
    hero = service._load("test:1")
    assert hero.activity["to"] == [1, 3] and hero.activity["goal"] == [0, 0]       # the leg in progress ends first
    assert hero.activity["path"][-1] == [0, 0]
    assert not service.texts.missing


def test_resting_at_the_inn_you_wait(service):
    make_hero(service)
    hero = place(service, 0, 3, known=["0:1", "0:2"])
    hero.activity = {"kind": "rest", "until": service.clock.now() + 3600}
    service._save(hero)
    view = service.act("test:1", "goask:0:0")
    assert view.kind == "places" and "🛏️" in view.notice
    service.act("test:1", "goto:0:0")
    assert service._load("test:1").activity["kind"] == "rest"
