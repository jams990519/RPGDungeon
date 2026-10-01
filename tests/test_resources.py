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


def test_exploring_reaches_100_and_stops(service, clock):
    make_hero(service)
    service.act("test:1", "do:explore:10")
    for _ in range(12):
        clock.advance(3600)
        service.view("test:1")
    hero = service._load("test:1")
    assert hero.exploration["0:0"] == 100
    assert 50 - hero.energy < 10                                          # it stopped early, at 100 %
    assert service.act("test:1", "explore").kind == "explore_menu"         # nothing left to explore
    assert service._known_resources(hero, 0, 0) == ["madera", "fibra"]
    assert "🟫" in "\n".join(service.act("test:1", "map").body)             # the Claro shows its colour


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
