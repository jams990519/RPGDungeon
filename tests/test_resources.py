"""Exploration by percent, resource regions, depletion, backpack space and energy batches (D-87).

[ES] Prueba la exploración por porcentaje, las regiones de recursos, el agotamiento, el espacio de la
mochila, el gasto de energía en lote (con cancelar) y los colores del mapa. D-300 (pedido del dueño, 20-oct-2026: más
madera): toda zona de bosque tiene 🪵 madera, la madera solo se suma (ninguna zona pierde un recurso, comparado con el
reparto de antes; los nodos no se mueven) y vuelve el doble de rápido.
"""

import copy

import pytest

from conftest import make_hero
from engine.core import FixedClock, MemoryStore
from engine.service import GameService
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
    assert view.kind == "batch" and view.layout == [len(view.actions) - 1, 1]   # D-189: the amounts in one row, then cancel
    assert view.actions[-1].id == "explore_menu"                            # cancel before starting: nothing spent
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
    assert "🔥 Campamento" in body[1]                                        # D-220: only the terrains you know; D-223: the 🔥 is a camp
    north = service.content.biomes[service._zone(0, 1).biome]
    radius = service.content.balance["map_view"]["radius"]
    north_cell = north["color"] if hero.exploration.get("0:1", 0) >= 50 else service._fog_stage(hero.exploration.get("0:1", 0))["mark"]
    assert north_cell in body[2 + radius - 1]                                # D-212: grey until 50 %, then its colour
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
    # Owner's requests: every amount shows its estimated total time (D-114) and, since D-189, all the amounts come at once as
    # small buttons with just the number, side by side, with one wide ❌ Cancelar; the times go in one line of the text.
    make_hero(service)
    view = service.act("test:1", "explore")
    minutes = service.content.balance["explore"]["minutes"]
    five = next(a for a in view.actions if a.id == "do:explore:5")
    assert five.label == "5" and view.actions[-1].label == "❌ Cancelar" and view.layout == [len(view.actions) - 1, 1]
    assert any(f"5 → {service._fmt_duration(service._seconds(minutes * 5))}" in line for line in view.body)
    energy = service._load("test:1").energy
    assert any("⏱️" in line and service._fmt_duration(service._seconds(minutes * energy)) in line for line in view.body)
    assert [a.id for a in service.act("test:1", "amt:explore:1").actions] == [a.id for a in view.actions]
    assert not service.texts.missing


def test_the_terrain_patchwork_never_moved_the_land_resources(service):
    """D-185, D-186: the land resources still follow the classic biome (what players knew of their zones did not move);
    since D-212 / D-220 the map is grey until you investigate (tests/test_mapa_gris.py), and paints the terrain at 50 %."""
    from engine.world import classic_biome
    for x in range(-8, 9, 2):
        for y in range(-8, 9, 2):
            if service._is_lair(x, y):
                continue
            classic = zone_resources(service.world_seed, x, y, classic_biome(service.world_seed, x, y),
                                     service.content.balance, service.content.biomes)
            found = service._zone_resources(x, y)
            assert service._zone_land(x, y)[0] == classic                   # the 6 base ones, as before
            assert {r: found[r] for r in classic} == classic and list(found)[:len(classic)] == list(classic)
    make_hero(service)
    hero = service._load("test:1")
    radius = service.content.balance["map_view"]["radius"]
    hero.exploration.update({f"{x}:{y}": 50 for x in range(-radius, radius + 1) for y in range(-radius, radius + 1)})
    service._save(hero)
    body = service.act("test:1", "map").body
    rows = body[2:2 + 2 * radius + 1]
    assert not any("▫️" in row or "◽" in row or "◻️" in row for row in rows)   # all at 50 %: no grey squares left
    colours = {b["color"] for b in service.content.biomes.values()}
    assert sum(row.count(c) for row in rows for c in colours) >= (2 * radius + 1) ** 2 - 10


# ---------------------------------------------------------------- D-300: more wood (owner, 20-oct-2026)

def _without_wood(content):
    """The content as before D-300: no resources.wood block and no stock.regen_mult (the old wood distribution)."""
    old = copy.deepcopy(content)
    old.balance["resources"].pop("wood", None)
    old.balance["stock"].pop("regen_mult", None)
    return old


def test_forest_zones_always_have_wood(content):
    """D-300: every zone whose terrain the map shows as a forest has 🪵 wood, rich enough to gather (forest_min)."""
    wcfg = content.balance["resources"]["wood"]
    forests = set(wcfg["forest"])
    assert forests == {"bosque", "bosque_oscuro", "selva"} and forests <= set(content.biomes)
    for seed in (7, 12345):
        service = GameService(content, MemoryStore(), FixedClock(), world_seed=seed)
        seen = 0
        for x in range(-18, 19):
            for y in range(-18, 19):
                if service._zone(x, y).biome in forests:
                    found = service._zone_resources(x, y)
                    assert found.get("madera", 0) >= wcfg["forest_min"], (seed, x, y, found)
                    seen += 1
        assert seen > 100


def test_wood_is_only_added_and_no_zone_loses_a_resource(content):
    """D-300: compared with the distribution of before, every zone keeps each resource it had (same richness, same order),
    wood goes right after the base ones, the nodes did not move and more zones have wood."""
    old_content = _without_wood(content)
    for seed in (7, 2026):
        new = GameService(content, MemoryStore(), FixedClock(), world_seed=seed)
        old = GameService(old_content, MemoryStore(), FixedClock(), world_seed=seed)
        before = after = total = 0
        for x in range(-16, 17, 2):
            for y in range(-16, 17):
                was, now = old._zone_resources(x, y), new._zone_resources(x, y)
                assert all(r in now for r in was), (seed, x, y)                       # nothing lost...
                assert {r: now[r] for r in was if r != "madera"} == {r: v for r, v in was.items() if r != "madera"}
                assert now.get("madera", 0) >= was.get("madera", 0)                   # ...and wood never poorer
                assert [r for r in now if r in was] == list(was), (seed, x, y)        # the old ones keep their order
                added = [r for r in now if r not in was]
                assert added in ([], ["madera"]), (seed, x, y, added)                  # only wood is ever added...
                if added:
                    base = old._zone_land(x, y)[0]
                    assert list(now).index("madera") == len(base), (seed, x, y)        # ...right after the base ones
                    assert 0.3 <= now["madera"] <= 1.0
                assert new._node_main(x, y) == old._node_main(x, y), (seed, x, y)      # the nodes did not move
                total += 1
                before += "madera" in was
                after += "madera" in now
        assert after - before >= total * 0.08, (seed, before, after, total)          # clearly more zones with wood
        assert new._zone_resources(3, 5) == new._zone_resources(3, 5)                  # the same seed, the same world


def test_wood_regrows_twice_as_fast(service, clock):
    """D-300 (owner: "lento para las construcciones, pero tampoco tan lento"): wood comes back ×2 (stock.regen_mult)."""
    mult = service.content.balance["stock"]["regen_mult"]["madera"]
    assert mult == 2.0
    x, y = next((x, y) for x in range(1, 30) for y in range(0, 30)
                if "madera" in service._zone_resources(x, y) and len(service._zone_resources(x, y)) > 1)
    service.store.put("stock", f"{x}:{y}", {"levels": {r: 0.0 for r in service._zone_resources(x, y)}, "at": clock.now()})
    clock.advance(5 * 3600)
    stock = service._stock(x, y)
    regen = service.content.balance["stock"]["regen_per_hour"]
    other = next(r for r in stock if r != "madera")
    assert stock[other] == pytest.approx(5 * regen)
    assert stock["madera"] == pytest.approx(5 * regen * mult)                          # 2 units an hour instead of 1
    assert service._stock(0, 0)["madera"] == 1.0                                          # untouched zones stay full
