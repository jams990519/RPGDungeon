"""📒 Lugares: only the important places you know, each with a code, and a confirmation before travelling (D-223, 0.30.2).

[ES] Pruebas de 📒 Lugares. La lista trae solo los lugares importantes que ya visitaste: el 🔥 Claro (siempre), los
🏕️ campamentos de jugadores, las 🕳️ 🌀 mazmorras y la 👑 guarida; las zonas comunes no. Cada lugar tiene su código (/ir1,
/ir2...) y los 3 más cercanos un botón; elegir uno (botón o código) pregunta antes de viajar, y al confirmar el héroe va
solo, zona por zona. Un código que no está en la lista no hace nada raro. Ningún texto falta. 0.33 (pedido del dueño:
"debería dejarme ir hacia la fogata"): estando ocupado también se puede ir: un lote se corta, un viaje cambia el rumbo y
solo descansando en la posada hay que esperar. D-301 (pedido del dueño, 20-oct-2026): 📒 Lugares es un menú con un botón
por tipo: primero 🏕️ tu campamento (va directo a "¿Viajar?"), después 🕳️ Mazmorras, 🔥 Fogatas y los demás tipos que
tengan algo; cada tipo lista sus lugares con su código /irN (desde 1 en cada lista) y su tiempo; un /irN de una lista
guardada antes de D-301 sigue sirviendo; en inglés, sin textos de repuesto.
Archivo: tests/test_lugares.py · Módulo: M8 Mundo y mapa · Prueba: engine/service/game.py (_important_places,
_place_groups, _places_view, _places_kind_view, _place_confirm_view, _place_code, "plc:", "goask:", "goto:" y el texto /irN).
"""

from conftest import make_hero
from test_camps import found_at


def kind_lines(service, kind, account="test:1"):
    """A 📒 Lugares kind's screen ("plc:<kind>", D-301) and its lines with a code."""
    view = service.act(account, f"plc:{kind}")
    return view, [line for line in view.body if "/ir" in line or "/go" in line]


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
    menu = service.act("test:1", "places")
    assert menu.kind == "places" and [a.id for a in menu.actions] == ["plc:dng", "plc:fire", "map"]   # D-301: no camp yet
    _, fires = kind_lines(service, "fire")
    _, dungeons = kind_lines(service, "dng")
    assert any(line.startswith("1. 🔥") and "El Claro" in line for line in fires)       # the Claro, always (the nearest)
    assert len(fires) == 9                                                            # D-277: the 9 bonfires, all of them
    assert len(dungeons) == 1 and "mazmorra" in dungeons[0] and dungeons[0].startswith("1. ")   # the dungeon you visited
    name = service._zone_name(service._zone(*plain[1]))
    assert not any(name in line for line in fires + dungeons)                         # ordinary zones: not listed
    view = service.act("test:1", "plc:dng")
    assert view.kind == "places_kind" and view.actions[-1].id == "places"             # ↩️ Volver: back to 📒 Lugares
    assert all(a.id.startswith("goask:") for a in view.actions[:-1]) and len(view.actions) <= 4
    assert not service.texts.missing


def test_a_button_asks_first_and_then_you_travel(service):
    make_hero(service)
    place(service, 0, 3, known=["0:1", "0:2"])
    view = service.act("test:1", "goask:0:0")
    assert view.kind == "place_confirm" and [a.id for a in view.actions] == ["goto:0:0", "plc:fire"]   # D-301
    assert not service._load("test:1").activity                                      # nothing happens before confirming
    assert service.act("test:1", "plc:fire").kind == "places_kind"                    # "No, volver": the 🔥 Fogatas list
    service.act("test:1", "goto:0:0")
    hero = service._load("test:1")
    assert hero.activity["kind"] == "travel" and hero.activity["goal"] == [0, 0]
    assert not service.texts.missing


def test_a_code_asks_first_too(service):
    make_hero(service)
    place(service, 0, 3, known=["0:1", "0:2"])
    service.act("test:1", "plc:fire")
    first = service._place_groups(service._load("test:1"))["fire"][0]
    view = service.text("test:1", "/ir1")
    assert view.kind == "place_confirm" and view.actions[0].id == f"goto:{first[1]}:{first[2]}"
    assert service.text("test:1", "/ir_1").kind == "place_confirm"
    view = service.text("test:1", "/ir99")                                            # not on the list: back to it
    assert view.kind == "places_kind" and view.notice
    assert not service._load("test:1").activity
    assert not service.texts.missing


def test_the_menu_shows_your_camp_first_then_dungeons_then_bonfires(service, clock):
    """D-301 (the owner: "el primer botón va a ser el del campamento... luego Mazmorras... luego Fogatas, y así
    sucesivamente"): your camp's button straight to "Travel?", then one button per kind that has places."""
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    found_at(service, "test:1", 6, 0)
    found_at(service, "test:2", -6, 0)
    dx, dy = dungeon_near(service)
    place(service, 0, 3, known=["0:0", f"{dx}:{dy}"])
    menu = service.act("test:1", "places")
    ids = [a.id for a in menu.actions]
    assert ids == ["goask:6:0", "plc:dng", "plc:fire", "plc:camps", "map"], ids
    assert menu.actions[0].label == "🏕️ Campo 1 6"                                  # the camp's name
    assert [a.label.split(" (")[0] for a in menu.actions[1:4]] == ["🕳️ Mazmorras", "🔥 Fogatas", "🏕️ Campamentos"]
    assert menu.actions[2].label == "🔥 Fogatas (9)"                                  # how many each kind has
    assert menu.layout == [1, 2, 1, 1] and sum(menu.layout) == len(menu.actions)      # the camp wide, then 2 per row
    assert any("Campo 1 6 (6, 0)" in line for line in menu.body)
    confirm = service.act("test:1", "goask:6:0")
    assert confirm.kind == "place_confirm" and [a.id for a in confirm.actions] == ["goto:6:0", "places"]
    _, camps = kind_lines(service, "camps")
    assert len(camps) == 1 and "Campo 2 -6" in camps[0] and "/ir1" in camps[0]        # other players' camps: their own list
    assert not any("Campo 1 6" in line for line in camps)                             # yours is not repeated there
    assert service.act("test:1", "plc:camp").kind == "place_confirm"                  # "plc:camp" is your camp's trip too
    assert service.act("test:1", "plc:lair").kind == "places"                         # a kind with nothing: the menu
    hero = service._load("test:1")
    hero.x, hero.y = 6, 0
    service._save(hero)
    assert service.act("test:1", "places").actions[0].id == "plc:dng"                 # standing in your camp: no button
    assert not service.texts.missing


def test_each_kind_lists_its_places_with_codes_and_typed_codes_keep_working(service):
    """D-301: every kind starts at /ir1; a typed code is the place of the last list you saw, and a list saved before D-301
    (one list, no kind) still takes /irN to the place it showed."""
    make_hero(service)
    entrances = [(x, y) for x in range(-20, 21) for y in range(-20, 21) if service._dng_kind(x, y)][:4]
    place(service, 0, 3, known=["0:0"] + [f"{x}:{y}" for x, y in entrances])
    dng, dungeons = kind_lines(service, "dng")
    assert [line.split(".")[0] for line in dungeons] == ["1", "2", "3"]               # D-112: the 3 nearest without rank 10
    assert "1 más" in "\n".join(dng.body)
    first = service._place_groups(service._load("test:1"))["dng"][0]
    assert service.text("test:1", "/ir1").actions[0].id == f"goto:{first[1]}:{first[2]}"
    _, fires = kind_lines(service, "fire")
    fire1 = service._place_groups(service._load("test:1"))["fire"][0]
    assert fires[0].endswith("/ir1") and service.text("test:1", "/ir1").actions[0].id == f"goto:{fire1[1]}:{fire1[2]}"
    service.store.put("places_shown", "test:1", {"list": [[0, 0], [12, 12]]})          # saved by the 0.39.4 single list
    assert service.text("test:1", "/ir2").actions[0].id == "goto:12:12"
    view = service.text("test:1", "/ir3")
    assert view.kind == "places" and view.notice                                       # not on it: the menu, with a notice
    assert not service.texts.missing


def test_places_read_well_in_english(service):
    from test_idiomas import english_hero
    english_hero(service)
    dx, dy = dungeon_near(service)
    place(service, 0, 3, known=["0:0", f"{dx}:{dy}"])
    menu = service.act("test:1", "places")
    assert [a.label.split(" (")[0] for a in menu.actions[:-1]] == ["🕳️ Dungeons", "🔥 Campfires"]
    view, fires = kind_lines(service, "fire")
    assert view.title == "📒 Places · 🔥 Campfires" and fires[0].endswith("/go1")
    assert service.text("test:1", "/go1").kind == "place_confirm"
    assert not service.texts.fallbacks.get("en") and not service.texts.missing


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
