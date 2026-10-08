"""The blank map: zones show ▫️ until investigated to 50 %, then their terrain's colour; nothing else is drawn (D-212,
D-220, D-223).

[ES] Pruebas del mapa en blanco. Un héroe nuevo ve todo en blanco ▫️; solo se ven él (🧍) y el 🔥 campamento del inicio
(D-223: ya no se dibujan mazmorras, nodos, campamentos ni la guarida, y las etapas ◽ ◻️ se retiraron). Al 50 % aparece el
color del terreno. La leyenda solo nombra los terrenos que ya conoces (cuántos de cuántos) y el 🔥 se llama campamento.
Explorar avisa al llegar el color (🎨) y la primera vez que ves un terreno (🆕); también vale lo que exploras alrededor sin
moverte (D-107). 📍 Zona dice cuánto le falta a tu zona para su color. Ningún texto falta.
Archivo: tests/test_mapa_gris.py · Módulo: M8 Mundo y mapa · Prueba: engine/service/game.py (_fog_stage, _fog_stages,
_fog_cell, _known_terrains, _fog_notices, _map_view, _zone_view, _explore_step) y content/balance.yaml (map_view.fog).
Si cambian los umbrales o las marcas de map_view.fog, estas pruebas se ajustan solas porque los leen de ahí.
"""

import re

from conftest import make_hero
from engine.core.rng import Rng


def rows(service, body):
    radius = service.content.balance["map_view"]["radius"]
    return body[2:2 + 2 * radius + 1]


def cell(service, hero, body, x, y):
    radius = service.content.balance["map_view"]["radius"]
    cells = re.findall(r".️?", rows(service, body)[hero.y + radius - y])
    return cells[x - hero.x + radius]


def fog(service):
    return service.content.balance["map_view"]["fog"]


def mark(service, stage_id):
    return next(stage["mark"] for stage in fog(service)["stages"] if stage["id"] == stage_id)


def colour(service, x, y):
    return service.content.biomes[service._zone(x, y).biome]["color"]


def place(service, x, y, exploration=None, known=None):
    hero = service._load("test:1")
    hero.x, hero.y = x, y
    hero.exploration.update(exploration or {})
    if known is not None:
        hero.known = sorted(set(hero.known) | set(known))
    service._save(hero)
    return hero


def other_biome_zone(service, near=(0, 0), skip=()):
    """A zone near `near` whose terrain is not the Claro's and that is not in `skip`."""
    claro = service._zone(0, 0).biome
    for r in range(2, 8):
        for x in range(near[0] - r, near[0] + r + 1):
            for y in range(near[1] - r, near[1] + r + 1):
                if (x, y) not in skip and service._zone(x, y).biome != claro and not service._is_lair(x, y):
                    return x, y
    raise AssertionError("no zone found")


def test_a_new_hero_sees_the_whole_map_blank(service):
    make_hero(service)
    hero = service._load("test:1")
    body = service.act("test:1", "map").body
    blank = mark(service, "unknown")
    grid = rows(service, body)
    assert sum(row.count(blank) for row in grid) == len(grid) ** 2 - 1                   # everything blank but you
    assert "(1 de 15)" in body[1] and "🔥 Campamento" in body[1] and "🟩" not in body[1]
    assert blank in body[0] and "50 %" in body[0] and "Guardián" not in body[0]
    assert "◽" not in body[0] and "◻️" not in body[0]                                    # D-223: no grey stages any more
    assert cell(service, hero, body, 0, 0) == "🧍"
    assert not service.texts.missing


def test_the_colour_comes_at_50_and_nothing_in_between(service):
    make_hero(service)
    hero = place(service, 0, 0, {"1:0": 0, "-1:0": 10, "0:1": 30, "0:-1": 50, "1:1": 100})
    body = service.act("test:1", "map").body
    for x, y in ((1, 0), (-1, 0), (0, 1)):                                             # under 50 %: blank
        assert cell(service, hero, body, x, y) == mark(service, "unknown")
    assert cell(service, hero, body, 0, -1) == colour(service, 0, -1)                   # 50 %: its colour
    assert cell(service, hero, body, 1, 1) == colour(service, 1, 1)
    known = {service._zone(0, -1).biome, service._zone(1, 1).biome, service._zone(0, 0).biome}
    assert f"({len(known)} de 15)" in body[1]
    for biome_id in known:                                                              # the legend names what you know
        assert service._terrain_label(biome_id) in body[1]
    assert not service.texts.missing


def test_only_you_and_the_bonfire_are_drawn(service):
    """D-223: no dungeon, node, enemy camp, player camp or lair on the map, even right next to you."""
    make_hero(service)
    hero = place(service, 0, 3, {f"{x}:{y}": 0 for x in range(-6, 7) for y in range(-3, 10)},
                 known=[f"{x}:{y}" for x in range(-6, 7) for y in range(-3, 10)])
    body = service.act("test:1", "map").body
    allowed = {"🧍", "🔥", mark(service, "unknown")} | {b["color"] for b in service.content.biomes.values()}
    cells = {c for row in rows(service, body) for c in re.findall(r".️?", row)}
    assert cells <= allowed and not cells & {"🕳️", "🌀", "✨", "👹", "👑", "🏕️"}
    assert cell(service, hero, body, 0, 0) == "🔥"
    assert [a.id for a in service.act("test:1", "map").actions] == ["places", "explore_menu"]
    assert not service.texts.missing


def test_the_claro_always_shows_and_your_blank_zone_says_how_far(service):
    """D-222, D-223: the map has nothing under the grid, so the "how far is my square" line lives in 📍 Zona."""
    make_hero(service)
    hero = place(service, 1, 0, {"1:0": 30})
    body = service.act("test:1", "map").body
    assert cell(service, hero, body, 0, 0) == "🔥"
    zone = service.act("test:1", "home").body
    here = next(line for line in zone if line.startswith(mark(service, "unknown") + " Esta zona sigue en blanco"))
    assert "30 %" in here and "50 %" in here
    hero = place(service, 1, 0, {"1:0": 60})                                           # once coloured, no line
    assert not any("sigue en blanco" in line for line in service.act("test:1", "home").body)


def explore_once(service, hero, seed=7):
    zone = service._zone(hero.x, hero.y)
    activity = {"log": [], "got": {}}
    service._explore_step(hero, zone, Rng(seed), activity)
    return activity["log"]


def test_exploring_says_when_the_colour_and_a_new_terrain_come(service):
    make_hero(service)
    x, y = other_biome_zone(service)
    hero = place(service, x, y, {f"{x}:{y}": 10})                    # 10 % + 15-30 %: never 50 %
    log = explore_once(service, hero)
    assert not any(line.startswith(("🎨", "◻️", "◽")) for line in log)                  # D-223: no stage notices
    hero.exploration[f"{x}:{y}"] = 45                                 # 45 % + 15-30 %: always reaches 50 %
    log = explore_once(service, hero, seed=8)
    label = service._terrain_label(service._zone(x, y).biome)
    assert any(line.startswith("🎨") and label in line for line in log)
    assert any(line.startswith("🆕") and label in line and "de 15" in line for line in log)   # the first zone of its terrain
    assert not service.texts.missing


def test_a_terrain_you_already_know_is_not_new_again(service):
    make_hero(service)
    x, y = other_biome_zone(service)
    biome = service._zone(x, y).biome
    twin = next((a, b) for a in range(-12, 13) for b in range(-12, 13)
                if (a, b) != (x, y) and service._zone(a, b).biome == biome and not service._is_lair(a, b))
    hero = place(service, x, y, {f"{x}:{y}": 45, f"{twin[0]}:{twin[1]}": 60})
    log = explore_once(service, hero)
    assert any(line.startswith("🎨") for line in log)
    assert not any(line.startswith("🆕") for line in log)


def test_studying_a_zone_around_you_paints_it_too(service):
    """D-107 and E-181: the % belongs to the zone, so the one you study from next door also gets its colour."""
    make_hero(service)
    hero = place(service, 0, 0, {"0:0": 100})
    tx, ty = service._explore_target(hero)
    hero.exploration[f"{tx}:{ty}"] = 45
    log = explore_once(service, hero)
    assert any(line.startswith("🎨") and service._zone_name(service._zone(tx, ty)) in line for line in log)
    service._save(hero)
    body = service.act("test:1", "map").body
    assert cell(service, hero, body, tx, ty) == colour(service, tx, ty)


def test_old_heroes_keep_their_percent_and_only_the_colour_follows_it(service):
    """E-179: nobody loses what they explored; zones at 50 % or more keep their colour, the rest go back to grey."""
    make_hero(service)
    hero = place(service, 0, 0, {"2:0": 100, "-2:0": 49})
    body = service.act("test:1", "map").body
    hero = service._load("test:1")
    assert hero.exploration["2:0"] == 100 and hero.exploration["-2:0"] == 49
    assert cell(service, hero, body, 2, 0) == colour(service, 2, 0)
    assert cell(service, hero, body, -2, 0) == mark(service, "unknown")              # 49 %: blank (D-223)
