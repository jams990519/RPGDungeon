"""Exploration by percent, resource regions, depletion, backpack space and energy batches (D-87).

[ES] Prueba la exploración por porcentaje, las regiones de recursos, el agotamiento, el espacio de la
mochila, el gasto de energía en lote (con cancelar) y los colores del mapa.
"""

from conftest import make_hero
from engine.world import zone_at
from engine.world.resources import main_resource, zone_resources


def test_regions_have_one_to_three_of_six_resources(content):
    seen, mains, sizes = set(), {}, set()
    for x in range(-20, 21):
        for y in range(-20, 21):
            res = zone_resources(7, x, y, zone_at(7, x, y).biome, content.balance, content.biomes)
            assert 1 <= len(res) <= 3 and all(0.3 <= v <= 1.0 for v in res.values())
            assert res == zone_resources(7, x, y, zone_at(7, x, y).biome, content.balance, content.biomes)
            seen |= set(res)
            sizes.add(len(res))
            mains[(x, y)] = main_resource(res)
    assert seen == {"madera", "piedra", "fibra", "hierba_curativa", "pieza_metal", "arcilla"}
    assert sizes == {1, 2, 3}
    # patches of different sizes: find the biggest connected patch of one main resource
    best, done = 0, set()
    for start in mains:
        if start in done:
            continue
        stack, size = [start], 0
        done.add(start)
        while stack:
            cx, cy = stack.pop()
            size += 1
            for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                if (nx, ny) in mains and (nx, ny) not in done and mains[(nx, ny)] == mains[start]:
                    done.add((nx, ny))
                    stack.append((nx, ny))
        best = max(best, size)
    assert best >= 25                                  # some regions are 5×5 or bigger


def test_batch_asks_amount_and_can_be_cancelled(service, clock):
    make_hero(service)
    view = service.act("test:1", "explore")
    assert view.kind == "batch" and len(view.actions) <= 4
    assert any(a.id == "explore_menu" for a in view.actions)              # cancel before starting: nothing spent
    assert service._load("test:1").energy == 50
    service.act("test:1", "do:explore:10")
    assert service._load("test:1").energy == 49                            # 1 per step, paid when it starts
    view = service.act("test:1", "home")
    assert any(a.id == "stop" for a in view.actions)
    service.act("test:1", "stop")
    hero = service._load("test:1")
    assert hero.energy == 50 and hero.activity is None                      # the step in progress gives it back


def test_exploring_reaches_100_then_goes_on_around_you_without_moving(service, clock):
    make_hero(service)
    service.act("test:1", "do:explore:10")
    for _ in range(12):
        clock.advance(3600)
        service.view("test:1")
    hero = service._load("test:1")
    assert hero.exploration["0:0"] == 100
    assert service._known_resources(hero, 0, 0) == ["madera", "fibra"]
    body = service.act("test:1", "map").body                                 # D-179: colours by terrain, legend built alone
    assert "🟩 Pradera" in body[1] and "🟢 Bosque" in body[1] and "🔥 Claro" in body[1]
    north = service.content.biomes[service._zone(0, 1).biome]
    radius = service.content.balance["map_view"]["radius"]
    assert north["color"] in body[2 + radius - 1]                            # the remembered zone to the north, painted
    # D-107: the batch did not stop at 100 %: it went on with the zone to the north, and the hero never moved.
    assert (hero.x, hero.y) == (0, 0) and hero.activity is None
    assert hero.exploration.get("0:1", 0) > 0 and hero.remembers(0, 1)
    view = service.act("test:1", "explore")
    assert view.kind == "batch" and any("Alrededor: " in line for line in view.body)
    tx, ty = service._explore_target(hero)                                  # the zone to the north, or the next one
    assert (tx, ty) != (0, 0) and any(f"({tx}, {ty})" in line and "sin moverte" in line for line in view.body)


def test_explore_around_order_and_the_end_of_it(service, clock):
    make_hero(service)
    hero = service._load("test:1")
    assert service._explore_around(hero)[:4] == [(0, 1), (1, 0), (0, -1), (-1, 0)]   # N, E, S, W, then diagonals
    assert len(service._explore_around(hero)) == 8                                  # explore.around_radius: 1
    hero.exploration = {"0:0": 100, "0:1": 100}
    service._save(hero)
    assert service._explore_target(service._load("test:1")) == (1, 0)
    hero.exploration = {f"{x}:{y}": 100 for x in (-1, 0, 1) for y in (-1, 0, 1)}
    service._save(hero)
    energy = hero.energy
    view = service.act("test:1", "explore")                                        # nothing left from here
    assert view.kind == "explore_menu" and "alrededor" in view.notice
    service.act("test:1", "do:explore:5")
    assert service._load("test:1").energy == energy and service._load("test:1").activity is None
    hero = service._load("test:1")
    hero.exploration["1:1"] = 40
    service._save(hero)
    service.act("test:1", "do:explore:20")                                         # one zone left: it stops when done
    for _ in range(30):
        clock.advance(3600)
        service.view("test:1")
    hero = service._load("test:1")
    assert hero.exploration["1:1"] == 100 and hero.activity is None and (hero.x, hero.y) == (0, 0)
    assert all(hero.exploration.get(f"{x}:{y}", 0) == 100 for x in (-1, 0, 1) for y in (-1, 0, 1))
    assert not any(k for k in hero.exploration if k not in {f"{x}:{y}" for x in (-1, 0, 1) for y in (-1, 0, 1)})   # never further
    assert not service.texts.missing


def test_gathering_only_gives_the_zone_resources_and_depletes(service, clock):
    make_hero(service)
    service.act("test:1", "do:gather:20")
    for _ in range(8):
        clock.advance(3600)
        service.view("test:1")
    hero = service._load("test:1")
    got = {i for i in hero.backpack if service.content.items[i]["kind"] == "material"}
    assert got and got <= {"madera", "fibra"}
    stock = service._stock(0, 0)
    assert min(stock.values()) < 1.0
    clock.advance(200 * 3600)
    assert service._stock(0, 0) == {"madera": 1.0, "fibra": 1.0}           # it comes back with time


def test_backpack_space_stops_gathering(service, clock):
    make_hero(service)
    hero = service._load("test:1")
    hero.backpack["piedra"] = service._bag_cap() - service._bag_used(hero) - 1
    service._save(hero)
    service.act("test:1", "do:gather:10")
    pushes = []
    for _ in range(4):
        clock.advance(3600)
        pushes += [v for acc, v in service.tick() if acc == "test:1"]
    hero = service._load("test:1")
    assert service._bag_used(hero) == service._bag_cap() and hero.activity is None
    assert len(pushes) == 1 and "mochila" in (pushes[0].notice or "").lower()   # one message at the end, not one per step


def test_gathering_gives_experience_scaled_by_the_zone_level(service, clock):
    # D-108: every path reaches level 100 on its own; gathering pays xp_per_step × zone level, like a kill.
    make_hero(service)
    hero = service._load("test:1")
    hero.tutorial = len(service.content.balance["tutorial"]["steps"])      # no tutorial reward in the way
    service._save(hero)
    service.act("test:1", "do:gather:3")
    pushes = []
    for _ in range(3):
        clock.advance(3600)
        pushes += [v for acc, v in service.tick() if acc == "test:1"]
    hero = service._load("test:1")
    step = service.content.balance["gather"]["xp_per_step"]
    assert hero.xp == 3 * step                                             # the Claro is level 1: × 1
    assert any(f"+{3 * step} experiencia" in line for v in pushes for line in (v.notice or "").split("\n"))
    assert service._zone_xp(step, 11) == int(step * 2.5)                   # 15 % more per level
    edef = service.content.enemies["lobo_ceniciento"]
    assert service._zone_xp(edef["xp"], 5) == int(edef["xp"] * 1.6)        # kills: the same scale as before


def test_amount_choices_show_the_estimated_total_time(service):
    # Owner's request: every amount shows its estimated total time, and the screen the time with all the energy.
    make_hero(service)
    view = service.act("test:1", "explore")
    minutes = service.content.balance["explore"]["minutes"]
    five = next(a for a in view.actions if a.id == "do:explore:5")
    assert "⏱️" in five.label and service._fmt_duration(service._seconds(minutes * 5)) in five.label
    energy = service._load("test:1").energy
    assert any("⏱️" in line and service._fmt_duration(service._seconds(minutes * energy)) in line for line in view.body)
    view = service.act("test:1", "amt:explore:1")
    assert all("⏱️" in a.label for a in view.actions if a.id.startswith("do:"))
    assert not service.texts.missing
