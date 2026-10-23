"""Exploration by percent, resource regions, depletion, backpack space and energy batches (D-87).

[ES] Prueba la exploración por porcentaje, las regiones de recursos, el agotamiento, el espacio de la
mochila, el gasto de energía en lote (con cancelar) y los colores del mapa. D-300 (pedido del dueño, 20-oct-2026: más
madera): la madera solo se suma (ninguna zona pierde un recurso, comparado con el reparto de antes; los nodos no se
mueven) y vuelve el doble de rápido. D-303 (0.41.1, orden del dueño: "en todos lugares, en menor medida, pero deberían
tener"): toda zona que no es fija tiene 🪵 madera; en el bosque es la más rica (1,0), va primera y se conoce al 1 %; en
los demás terrenos es pobre (hasta 0,5) y va después de los de base; con cualquier %, nadie conoce menos que antes.
D-305 (0.42, el dueño el 20-oct-2026): los 6 recursos de base vuelven 3 por hora en cada zona (la madera también, antes ×2);
los propios del terreno y el pescado siguen ×1. 🪓 Talar se prueba en tests/test_talar.py.
"""

import copy

import pytest

from conftest import make_hero
from engine.core import FixedClock, MemoryStore
from engine.service import GameService
from engine.world import mapgen, zone_at
from engine.world.resources import main_resource, wood_first, zone_resources


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
    assert "🔥 Fogata" in body[1]                                            # D-220: only the terrains you know; D-311: the 🔥 is a Fogata
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
    # [ES] D-338 (0.62): el lote se corta cuando lo de la zona llega al tope de su tipo (30), ya no al espacio de 60
    make_hero(service)
    hero = service._load("test:1")
    per = service._pack_per_type()
    hero.backpack.update({res: per - 1 for res in service._zone_resources(0, 0)})
    service._save(hero)
    service.act("test:1", "do:gather:10")
    pushes = []
    for _ in range(4):
        clock.advance(3600)
        pushes += [v for acc, v in service.tick() if acc == "test:1"]
    hero = service._load("test:1")
    assert all(hero.backpack[res] == per for res in service._zone_resources(0, 0)) and hero.activity is None
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
            if _is_forest(service, x, y):                                   # D-303: a forest's wood leads (1.0)
                assert list(found)[0] == "madera" and found["madera"] == 1.0
                found = {r: v for r, v in found.items() if r != "madera"}
                classic = {r: v for r, v in classic.items() if r != "madera"}
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


# ---------------------------------------------------------------- D-300 and D-303: wood in every zone (owner, 20-oct-2026)

def _without_wood(content):
    """The content as before D-300: no resources.wood block and no stock.regen_mult (the old wood distribution)."""
    old = copy.deepcopy(content)
    old.balance["resources"].pop("wood", None)
    old.balance["stock"].pop("regen_mult", None)
    return old


def _is_forest(service, x, y):
    return wood_first(x, y, service._zone(x, y).biome, service.content.balance)


def _fixed(service, x, y):
    return mapgen.is_bonfire(x, y) or f"{x}:{y}" in service.content.balance["resources"].get("fixed", {})


def test_every_zone_has_wood(content):
    """D-303 (owner: "los bosques deberían tener, las montañas deberían tener, o sea, en todos lugares"): in a 61 × 61
    sample every zone that is not fixed (the Claro, the bonfires, which keep their fixed wood) has 🪵 wood."""
    for seed in (12345, 777):
        service = GameService(content, MemoryStore(), FixedClock(), world_seed=seed)
        zones = forests = 0
        for x in range(-30, 31):
            for y in range(-30, 31):
                found = service._zone_resources(x, y)
                assert "madera" in found and 0.3 <= found["madera"] <= 1.0, (seed, x, y, found)
                if not _fixed(service, x, y):
                    zones += 1
                    forests += _is_forest(service, x, y)
        assert zones > 3600 and forests > 400, (zones, forests)


def test_forest_zones_list_wood_first_and_a_new_explorer_knows_it(content):
    """D-303: in a forest terrain (bosque, bosque oscuro, selva) wood is the richest (1.0) and goes first, so a hero who
    explored the zone to 1 % already knows it, along with the zone's first resource of before (nobody knows less)."""
    wcfg = content.balance["resources"]["wood"]
    assert set(wcfg["forest"]) == {"bosque", "bosque_oscuro", "selva"} and set(wcfg["forest"]) <= set(content.biomes)
    assert wcfg["forest_min"] == 1.0
    service = GameService(content, MemoryStore(), FixedClock(), world_seed=12345)
    make_hero(service)
    hero = service._load("test:1")
    checked = 0
    for x in range(-30, 31):
        for y in range(-30, 31):
            if _fixed(service, x, y) or not _is_forest(service, x, y):
                continue
            found = service._zone_resources(x, y)
            assert list(found)[0] == "madera" and found["madera"] == 1.0, (x, y, found)
            if checked < 40:
                hero.exploration[f"{x}:{y}"] = 1
                known = service._known_resources(hero, x, y)
                base = list(service._zone_land(x, y)[0])
                assert known[0] == "madera" and base[0] in known, (x, y, known)
            checked += 1
    assert checked > 400


def test_wood_elsewhere_is_poor_only_added_and_nobody_knows_less(content):
    """D-303: compared with the distribution of before D-300, every zone keeps each resource it had (same richness, except
    wood lifted to 1.0 in a forest), only wood is added, outside a forest the added wood is poor (0.3 to elsewhere_max, 0.5)
    and right after the base ones, a base wood outside a forest is untouched, and at every % a hero knows at least what
    it knew before."""
    wcfg = content.balance["resources"]["wood"]
    assert wcfg["elsewhere_max"] == 0.5
    old_content = _without_wood(content)
    reveal = content.balance["exploration"]["reveal_at"]
    for seed in (12345, 2026):
        new = GameService(content, MemoryStore(), FixedClock(), world_seed=seed)
        old = GameService(old_content, MemoryStore(), FixedClock(), world_seed=seed)
        make_hero(new)
        make_hero(old)
        hero_new, hero_old = new._load("test:1"), old._load("test:1")
        added = 0
        for x in range(-30, 31, 3):
            for y in range(-30, 31, 2):
                was, now = old._zone_resources(x, y), new._zone_resources(x, y)
                assert all(r in now for r in was), (seed, x, y)                       # nothing lost...
                assert {r: now[r] for r in was if r != "madera"} == {r: v for r, v in was.items() if r != "madera"}
                assert now.get("madera", 0) >= was.get("madera", 0)                   # ...and wood never poorer
                assert [r for r in now if r in was and r != "madera"] == [r for r in was if r != "madera"]
                assert [r for r in now if r not in was] in ([], ["madera"]), (seed, x, y)   # only wood is ever added
                if not _fixed(new, x, y) and not _is_forest(new, x, y):
                    base = old._zone_land(x, y)[0]
                    if "madera" in base:
                        assert now == was, (seed, x, y)                               # a base wood stays as it was
                    else:
                        assert list(now).index("madera") == len(base), (seed, x, y)    # right after the base ones...
                        assert 0.3 <= now["madera"] <= wcfg["elsewhere_max"], (seed, x, y, now)   # ...and poor
                        added += 1
                for pct in reveal[:-1]:                                               # nobody knows less than before
                    key = f"{x}:{y}"
                    hero_new.exploration[key] = hero_old.exploration[key] = pct
                    knew, knows = old._known_resources(hero_old, x, y), new._known_resources(hero_new, x, y)
                    assert set(knew) <= set(knows), (seed, x, y, pct, knew, knows)
        assert added > 150, added
        assert new._zone_resources(3, 5) == new._zone_resources(3, 5)                  # the same seed, the same world


def test_the_nodes_never_moved(content):
    """D-300 and D-303: a node's resource is drawn from the base and own resources as they were, never from the added
    wood (nor from the forest's lifted wood): every node is where it was, with the same resource."""
    old_content = _without_wood(content)
    new = GameService(content, MemoryStore(), FixedClock(), world_seed=4242)
    old = GameService(old_content, MemoryStore(), FixedClock(), world_seed=4242)
    nodes = 0
    for x in range(-30, 31):
        for y in range(-30, 31):
            main = new._node_main(x, y)
            assert main == old._node_main(x, y), (x, y)
            nodes += main is not None
    assert nodes > 100


BASE = ("madera", "piedra", "fibra", "hierba_curativa", "pieza_metal", "arcilla")


def test_the_six_base_resources_regrow_three_times_as_fast(service, clock):
    """D-305 (0.42, owner, 20-oct-2026): the 6 base resources come back 3 per hour in each zone instead of 1 (wood ×3 too,
    it was ×2 by D-300); the terrain's own resources and fish stay at ×1 (stock.regen_mult)."""
    cfg = service.content.balance["stock"]
    assert {r: cfg["regen_mult"][r] for r in BASE} == {r: 3.0 for r in BASE}
    assert set(cfg["regen_mult"]) == set(BASE)                                            # nothing else goes faster
    x, y = next((x, y) for x in range(1, 30) for y in range(0, 30)
                if any(r != "madera" for r in service._zone_land(x, y)[0]) and service._zone_land(x, y)[2])
    resources = service._zone_resources(x, y)
    service.store.put("stock", f"{x}:{y}", {"levels": {r: 0.0 for r in resources}, "at": clock.now()})
    clock.advance(5 * 3600)
    stock = service._stock(x, y)
    regen = cfg["regen_per_hour"]
    base = next(r for r in service._zone_land(x, y)[0] if r != "madera")
    own = next(iter(service._zone_land(x, y)[2]))
    assert stock["madera"] == pytest.approx(5 * regen * 3)                             # 3 units an hour instead of 1
    assert stock[base] == pytest.approx(5 * regen * 3)
    assert stock[own] == pytest.approx(5 * regen)                                       # the terrain's own: as before
    assert round(regen * 3 / cfg["per_unit"]) == 3                                      # 3 units of 2 % an hour
    assert service._stock(0, 0)["madera"] == 1.0                                          # untouched zones stay full
    values = service._faq_values()
    assert values["base_units"] == "3" and values["base_regen"] == 6                    # what ❓ Dudas and 📚 Guías say
