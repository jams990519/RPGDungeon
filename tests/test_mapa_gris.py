"""The grey map: zones show grey marks until investigated to 50 %, then their terrain's colour (D-212, D-220, 0.30).

[ES] Pruebas del mapa gris. Un héroe nuevo ve todo en puntos grises ▫️ (salvo el 🔥 Claro y los íconos, que siguen sus
reglas); el punto crece al investigar (◽ con rastros desde el 1 %, ◻️ reconocida desde el 25 %) y al 50 % aparece el
color del terreno. La leyenda solo nombra los terrenos que ya conoces (cuántos de cuántos). Explorar avisa cada etapa a su
manera: ◻️ al reconocer, 🎨 al llegar al color y 🆕 la primera vez que ves un terreno; también vale lo que exploras
alrededor sin moverte (D-107). Ningún texto falta.
Archivo: tests/test_mapa_gris.py · Módulo: M8 Mundo y mapa · Prueba: engine/service/game.py (_fog_stage, _fog_cell,
_known_terrains, _fog_notices, _map_view, _explore_step) y content/balance.yaml (map_view.fog).
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


def place(service, x, y, exploration=None):
    hero = service._load("test:1")
    hero.x, hero.y = x, y
    hero.exploration.update(exploration or {})
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


def test_a_new_hero_sees_the_whole_map_grey(service):
    make_hero(service)
    hero = service._load("test:1")
    body = service.act("test:1", "map").body
    grey = mark(service, "unknown")
    colours = {b["color"] for b in service.content.biomes.values()}
    grid = rows(service, body)
    assert sum(row.count(grey) for row in grid) >= len(grid) ** 2 - 10      # all grey, but for 🧍 and a few icons
    assert not any(c in row for row in grid for c in colours if c != "🔥")
    assert "(1 de 15)" in body[1] and "🔥 Claro" in body[1] and "🟩" not in body[1]
    assert all(s["mark"] in body[0] for s in fog(service)["stages"]) and "50 %" in body[0]
    assert cell(service, hero, body, 0, 0) == "🧍"
    assert not service.texts.missing


def test_the_mark_grows_by_stages_and_the_colour_comes_at_50(service):
    make_hero(service)
    hero = place(service, 0, 0, {"1:0": 0, "-1:0": 10, "0:1": 30, "0:-1": 50, "1:1": 100})
    body = service.act("test:1", "map").body
    assert cell(service, hero, body, 1, 0) in (mark(service, "unknown"), "✨", "🕳️")   # 0 %: never studied
    assert cell(service, hero, body, -1, 0) == mark(service, "traces")                  # 1-24 %
    assert cell(service, hero, body, 0, 1) == mark(service, "scouted")                  # 25-49 %
    assert cell(service, hero, body, 0, -1) == colour(service, 0, -1)                   # 50 %: its colour
    assert cell(service, hero, body, 1, 1) == colour(service, 1, 1)
    known = {service._zone(0, -1).biome, service._zone(1, 1).biome, service._zone(0, 0).biome}
    assert f"({len(known)} de 15)" in body[1]
    for biome_id in known:                                                              # the legend names what you know
        assert service._terrain_label(biome_id) in body[1]
    assert not service.texts.missing


def test_the_claro_always_shows_and_your_grey_zone_says_how_far(service):
    make_hero(service)
    hero = place(service, 1, 0, {"1:0": 30})
    body = service.act("test:1", "map").body
    assert cell(service, hero, body, 0, 0) == "🔥"
    here = next(line for line in body if line.startswith(mark(service, "scouted") + " Aquí"))
    assert "30 %" in here and "50 %" in here
    hero = place(service, 1, 0, {"1:0": 60})                                           # once coloured, no line
    assert not any("Aquí:" in line for line in service.act("test:1", "map").body)


def explore_once(service, hero, seed=7):
    zone = service._zone(hero.x, hero.y)
    activity = {"log": [], "got": {}}
    service._explore_step(hero, zone, Rng(seed), activity)
    return activity["log"]


def test_exploring_says_each_stage_its_own_way(service):
    make_hero(service)
    x, y = other_biome_zone(service)
    hero = place(service, x, y, {f"{x}:{y}": 10})                    # 10 % + 15-30 %: always crosses 25 %, never 50 %
    log = explore_once(service, hero)
    assert any(line.startswith(mark(service, "scouted")) and "reconocida" in line for line in log)
    assert not any(line.startswith("🎨") for line in log)
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
    assert cell(service, hero, body, tx, ty) in (colour(service, tx, ty), "✨", "🕳️", "👹")


def test_old_heroes_keep_their_percent_and_only_the_colour_follows_it(service):
    """E-179: nobody loses what they explored; zones at 50 % or more keep their colour, the rest go back to grey."""
    make_hero(service)
    hero = place(service, 0, 0, {"2:0": 100, "-2:0": 49})
    body = service.act("test:1", "map").body
    hero = service._load("test:1")
    assert hero.exploration["2:0"] == 100 and hero.exploration["-2:0"] == 49
    assert cell(service, hero, body, 2, 0) in (colour(service, 2, 0), "✨", "🕳️")
    assert cell(service, hero, body, -2, 0) in (mark(service, "scouted"), "✨", "🕳️")
