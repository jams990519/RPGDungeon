"""📍 Zona in short blocks, one idea per line, and a 🗺️ Mapa with nothing under the grid (D-221, D-222, 0.30.1).

[ES] Pruebas de la pantalla ordenada. 📍 Zona va en bloques separados por renglones vacíos: el lugar (nombre, coordenadas,
peligro), lo explorado con un recurso por renglón, lo que hay aquí, las 🧭 Rutas (con el emoji del terreno, sin su nombre),
tu estado y una sola línea final de ❓ Dudas. 🧭 Explorar también lista los recursos uno por renglón. El 🗺️ Mapa trae la
leyenda, los terrenos y la cuadrícula, nada más: las listas de abajo se mudaron a 📒 Lugares. Viajar directo ("goto:")
solo va a lugares que el héroe ya visitó. Ningún texto falta.
Archivo: tests/test_zona_ordenada.py · Módulo: M8 Mundo y mapa · Prueba: engine/service/game.py (_zone_view,
_resources_lines, _explore_menu, _map_view, _map_marks_lines, _places_view y "goto:").
"""

from conftest import make_hero


def place(service, x, y, known=(), exploration=None):
    hero = service._load("test:1")
    hero.x, hero.y = x, y
    hero.known = sorted(set(hero.known) | set(known) | {f"{x}:{y}"})
    hero.exploration.update(exploration or {})
    service._save(hero)
    return hero


def blocks(body):
    """The screen split at its blank lines."""
    out, cur = [], []
    for line in body:
        if line == "":
            if cur:
                out.append(cur)
            cur = []
        else:
            cur.append(line)
    if cur:
        out.append(cur)
    return out


def test_the_zone_screen_goes_in_short_blocks(service):
    make_hero(service)
    place(service, 0, 2, known=["0:1", "0:3", "1:2"], exploration={"0:2": 100})
    view = service.act("test:1", "home")
    parts = blocks(view.body)
    place_block = parts[0]
    assert place_block[1].startswith("📌 (0, 2) · Lejanía") and place_block[2].startswith("⚔️ Peligro de nivel")
    resources = next(part for part in parts if part[0].startswith("🔎 Explorada al 100 %"))
    assert len(resources) > 1 and all(line.startswith("• ") for line in resources[1:])      # one resource per line
    assert all("▰" in line or "▱" in line for line in resources[1:])
    routes = next(part for part in parts if part[0] == "🧭 Rutas")
    assert len(routes) == 5 and [line[:2] for line in routes[1:]] == ["⬆️", "⬇️", "➡️", "⬅️"]
    names = [service.texts.t(b["name_key"]) for b in service.content.biomes.values()]
    assert not any(f"{name} " in line.split(":", 1)[1] for line in routes[1:] for name in names)   # emoji, not the name
    assert parts[-1] == [service.texts.t("menu.hint")]                                        # one short help line at the end
    assert any(part[0].startswith("❤️") for part in parts)
    assert not service.texts.missing


def test_a_zone_still_being_explored_says_what_is_left(service):
    make_hero(service)
    place(service, 0, 2, exploration={"0:2": 30})
    body = service.act("test:1", "home").body
    resources = next(part for part in blocks(body) if part[0].startswith("🔎 Explorada al 30 %"))
    assert service.texts.t("explore.resources_more") in resources                         # less than 100 %: more to find
    assert any(line.startswith("◻️ Aquí") for line in body)                                 # the grey stage of your square
    assert not service.texts.missing


def test_the_explore_menu_lists_resources_one_per_line(service):
    make_hero(service)
    place(service, 0, 2, exploration={"0:2": 100})
    body = service.act("test:1", "explore_menu").body
    resources = next(part for part in blocks(body) if part[0].startswith("🔎 Explorada al"))
    assert all(line.startswith("• ") for line in resources[1:])
    assert not service.texts.missing


def test_the_map_has_nothing_under_the_grid_and_places_keeps_the_lists(service):
    make_hero(service)
    place(service, 0, 5, known=[f"0:{i}" for i in range(1, 6)])
    radius = service.content.balance["map_view"]["radius"]
    view = service.act("test:1", "map")
    assert len(view.body) == 2 + 2 * radius + 1                                   # legend, terrains and the grid only
    assert not any(line.startswith(("Coordenadas", "🕳️ (", "✨ (", "👹 (", "🔭")) for line in view.body)
    marks = service._map_marks_lines(service._load("test:1"))
    places = service.act("test:1", "places").body
    if marks:                                                                     # what the map marks, under its title
        assert service.texts.t("places.marks_title") in places and all(line in places for line in marks)
    assert not service.texts.missing


def test_travelling_directly_only_goes_where_you_have_been(service):
    make_hero(service)
    place(service, 0, 0)
    service.act("test:1", "goto:4:4")                                             # never been there: no shortcut
    assert not service._load("test:1").activity
    place(service, 0, 0, known=["0:1", "0:2"])
    service.act("test:1", "goto:0:2")                                             # remembered: off you go, zone by zone
    hero = service._load("test:1")
    assert hero.activity and hero.activity["kind"] == "travel" and hero.activity["goal"] == [0, 2]
    assert not service.texts.missing
