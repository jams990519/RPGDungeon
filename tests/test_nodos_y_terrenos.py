"""Terrain catalogs (D-180, D-183) and resource nodes (D-181, D-184).

[ES] Pruebas del catálogo de cada terreno (10 a 15 recursos posibles; cada zona que no es fija trae de 4 a 6 de tierra, y los 6
de base siguen exactamente donde estaban), de los recursos nuevos (cada uno con su oficio de recolección, una receta, precio en
el mercader, nombre y "para qué sirve", sin dejar ganar monedas), del descubrimiento por exploración (umbrales para hasta 6) y de
los nodos de recursos: lugar fijo para todos (2 o 3 por tramo de 6 × 6, nunca pegados, nunca en el Claro, la guarida ni una
entrada de mazmorra), el símbolo genérico ✨ en el 🗺️ Mapa hasta LLEGAR a su zona (explorar alrededor no lo descubre) y el
emoji de su recurso después, y su efecto al recolectar (×2, se agota la mitad, a veces un raro del terreno). Ningún texto falta.
"""

import pytest

from conftest import make_hero
from engine.core import FixedClock, MemoryStore, Rng
from engine.professions import branches_of, gatherer_of
from engine.service import GameService
from engine.world import dungeons as dungeon_rules
from engine.world import nodes as node_rules
from engine.world import classic_biome, zone_at
from engine.world.mapgen import lejania
from engine.world.resources import catalog, terrain_resources, zone_resources
from test_camps import place

MINUTE = 60
BASE = {"madera", "piedra", "fibra", "hierba_curativa", "pieza_metal", "arcilla"}

# [ES] Los recursos de base de estas zonas con la semilla 7, calculados con el código de la 0.26.1 (antes de D-180): no se mueven.
BEFORE = {
    (0, 0): {"madera": 1.0, "fibra": 0.8},
    (1, 0): {"fibra": 1.0, "hierba_curativa": 0.78},
    (3, -2): {"piedra": 1.0},
    (-5, 4): {"fibra": 1.0, "pieza_metal": 0.91, "piedra": 0.9},
    (7, 7): {"madera": 1.0, "hierba_curativa": 0.92},
    (-9, -3): {"piedra": 1.0, "hierba_curativa": 0.78, "madera": 0.77},
    (12, 1): {"madera": 1.0, "hierba_curativa": 0.89, "piedra": 0.85},
    (2, 11): {"madera": 1.0},
    (-14, -14): {"pieza_metal": 1.0, "madera": 0.94, "arcilla": 0.89},
    (20, -6): {"pieza_metal": 1.0, "hierba_curativa": 0.99},
}


def new_resources(content):
    return sorted({r for bdef in content.biomes.values() for r in (bdef.get("own") or [])})


def ready(service, account="test:1", **values):
    """A hero in the Claro, tutorial done (no rewards in the way), with the given fields set."""
    make_hero(service, account)
    hero = service._load(account)
    hero.tutorial = len(service.content.balance["tutorial"]["steps"])
    for key, value in values.items():
        setattr(hero, key, value)
    service._save(hero)
    return hero


def node_near(service, radius=12):
    """The nearest node to the Claro whose two zones to the south are plain land (no node, no dungeon, not the lair)."""
    found = []
    for x in range(-radius, radius + 1):
        for y in range(-radius, radius + 1):
            if not service._node_main(x, y) or lejania(x, y) < 3:
                continue
            south = [(x, y - 1), (x, y - 2)]
            if any(service._node_main(*c) or service._dng_kind(*c) or service._is_lair(*c) or service._ecamp_standing(*c)
                   for c in south):
                continue
            found.append((abs(x) + abs(y), x, y))
    assert found, "no node near the Claro"
    _, x, y = min(found)
    return x, y


def map_row(service, hero, y):
    radius = service.content.balance["map_view"]["radius"]
    return service.act(hero.id, "map").body[2 + (hero.y + radius - y)]


# ---------------------------------------------------------------- terrain catalogs (D-180, D-183)


def test_every_terrain_has_a_catalog_of_10_to_15_resources(content):
    for biome, bdef in content.biomes.items():
        if biome == "claro":
            assert not bdef.get("own") and not bdef.get("node_rare")       # the Claro keeps its fixed resources only
            continue
        cat = catalog(biome, content.biomes)
        assert 10 <= len(cat) <= 15, (biome, len(cat))
        assert len(cat) == len(set(cat)), biome
        assert not set(bdef["own"]) & BASE, biome                            # the own ones are new, never the base ones
        assert bdef["node_rare"] in content.items, biome
    assert len(new_resources(content)) >= 15                                 # overlap is fine (setas in forest and swamp)


def test_zones_bring_4_to_6_land_resources_and_the_base_ones_never_move(content):
    service = GameService(content, MemoryStore(), FixedClock(), world_seed=7)
    for (x, y), before in BEFORE.items():
        biome = classic_biome(7, x, y)                  # D-185, D-187: the base ones follow the classic biome, not the terrain
        assert zone_resources(7, x, y, biome, content.balance, content.biomes) == before, (x, y)
        found = service._zone_resources(x, y)
        assert {r: found[r] for r in before} == before and list(found)[:len(before)] == list(before)   # base first, same
    sizes, picks, foreign = set(), 0, 0
    every_own = {r for d in content.biomes.values() for r in d.get("own", [])}
    for x in range(-15, 16):
        for y in range(-15, 16):
            zone = service._zone(x, y)
            found = service._zone_resources(x, y)
            land = {r: v for r, v in found.items() if r != "pescado"}
            rbiome = zone.biome if service._is_lair(x, y) else classic_biome(7, x, y)    # the lair keeps its biome (D-82)
            base = zone_resources(7, x, y, rbiome, content.balance, content.biomes)
            own = terrain_resources(7, x, y, zone.biome, base, content.balance, content.biomes)
            assert land == {**base, **own}
            assert found == service._zone_resources(x, y)                   # always the same for the same seed
            if (x, y) == (0, 0):
                assert land == {"madera": 1.0, "fibra": 0.8}                 # the Claro: only its fixed ones
                continue
            assert 4 <= len(land) <= 6, (x, y, land)
            assert 1 <= len(own) <= 3 and set(own) <= every_own, (x, y)
            assert all(0.3 <= v <= 1.0 for v in own.values())
            sizes.add(len(land))
            picks += len(own)
            foreign += sum(1 for r in own if r not in content.biomes[zone.biome]["own"])
    assert sizes == {4, 5, 6}
    share = content.balance["resources"]["terrain"]["foreign_chance"]
    assert share - 0.08 <= foreign / picks <= share + 0.08         # D-185: about 3 in 10 come from another terrain


def test_every_new_resource_has_a_family_a_use_a_price_and_its_texts(service):
    content = service.content
    profs, recipes = content.professions["professions"], content.professions["recipes"]
    t = service.texts
    ratio = content.balance["shop"]["sell_ratio"]
    for res in new_resources(content):
        item = content.items[res]
        assert item["kind"] == "material" and not item.get("food") and not item.get("keep"), res   # 💱 Vender todo sells it
        assert 2 <= item["price"] <= 6, res                                  # close to the base ones: gathering pays the same
        assert t.has(item["name_key"]) and t.has(f"resources.use.{res}"), res
        assert gatherer_of(res, profs) in ("lenador", "minero", "herbolario"), res   # its perks and extra units apply
        uses = [rid for rid, r in recipes.items() if res in r["inputs"] and not r.get("retired")]
        assert uses, res                                                      # at least one real use today
    for rid, rdef in recipes.items():
        if not rdef.get("variant"):
            continue
        assert rdef["variant"] in rdef["inputs"] and rdef["variant"] in content.items, rid
        out_id, n = next(iter(rdef["output"].items()))
        out = content.items[out_id]
        if out.get("kind") == "food":                                          # 🍲 more rations than its raw food
            raw = sum(int(content.items[i].get("food", 0)) * k for i, k in rdef["inputs"].items())
            assert out["food"] * n > raw > 0, rid
            assert rdef["xp"] == 6 * rdef["energy"], rid
        else:                                                                  # refining and crafting never make coins
            materials = sum(content.items[m]["price"] * k for m, k in rdef["inputs"].items())
            assert out["price"] * n * ratio < materials, rid
        if profs[rdef["profession"]]["branch"] == "craft":
            assert len(branches_of(rdef, profs, recipes)) >= 2, rid         # D-109: nobody is self-sufficient
    assert t.t("prof.variant", name="A", item="B") == "A · con B"
    assert "con ⏳ Arena fina" in service._recipe_name("pocion_vida_arena")
    assert not t.missing


def test_exploring_reveals_up_to_six_resources(service):
    hero = ready(service)
    zone = next((x, y) for x in range(1, 20) for y in range(1, 20)
                if len([r for r in service._zone_resources(x, y) if r != "pescado"]) == 6)
    ranked = list(service._zone_resources(*zone))
    key = f"{zone[0]}:{zone[1]}"
    counts = []
    for pct in (0, 1, 20, 40, 60, 80, 99, 100):
        hero.exploration[key] = pct
        counts.append(len(service._known_resources(hero, *zone)))
    assert counts == [0, 1, 2, 3, 4, 5, 5, len(ranked)]                      # at 100 % everything is known
    assert service._known_resources(hero, *zone) == ranked


# ---------------------------------------------------------------- resource nodes (D-181, D-184)


def test_nodes_are_fixed_spread_out_and_two_or_three_per_stretch(content):
    one = GameService(content, MemoryStore(), FixedClock(), world_seed=12345)
    two = GameService(content, MemoryStore(), FixedClock(), world_seed=12345)
    cfg = content.balance["nodes"]
    size = cfg["stretch"]
    excluded = set(one._node_excluded())
    assert (0, 0) in excluded and (5, 2) in excluded                          # the Claro and the Guardian's lair
    nodes = []
    for bx in range(-3, 3):
        for by in range(-3, 3):
            found = [(x, y) for x in range(bx * size, bx * size + size) for y in range(by * size, by * size + size)
                     if one._node_main(x, y)]
            assert 2 <= len(found) <= 3, (bx, by, found)
            nodes += found
    for x, y in nodes:
        assert one._node_main(x, y) == two._node_main(x, y)                    # the same for everyone, never moves
        assert lejania(x, y) >= cfg["min_lejania"] and (x, y) not in excluded
        assert not dungeon_rules.entrance_at(12345, x, y, content.balance["dungeons"], ((5, 2),))   # never a dungeon entrance
        land = [r for r in one._zone_resources(x, y) if r != "pescado"]
        assert one._node_main(x, y) in land                                    # one of the zone's land resources
    for i, a in enumerate(nodes):                                              # never side by side, not even across stretches
        for b in nodes[i + 1:]:
            assert max(abs(a[0] - b[0]), abs(a[1] - b[1])) > cfg["spacing"], (a, b)
    own = sum(1 for x, y in nodes if one._node_main(x, y) not in BASE)
    assert 0.35 <= own / len(nodes) <= 0.85                                   # mostly the terrain's own (own_share 0.6)
    assert node_rules.node_main(1, 0, 0, {}, {}, 0.6) is None


def test_the_map_shows_a_generic_symbol_until_you_arrive(service, clock):
    service.content.balance["explore"]["arrival_encounter_scale"] = 0         # no ambush on arrival (test only)
    ready(service, energy=50)
    x, y = node_near(service)
    main = service._node_main(x, y)
    icon = service.content.items[main]["emoji"]
    place(service, "test:1", x, y - 2, known=["0:0", f"{x}:{y - 2}"])        # 2 zones away: within hint_radius
    hero = service._load("test:1")
    assert (x, y, None) in service._node_seen(hero)
    view = service.act("test:1", "map")
    assert "✨" in map_row(service, hero, y) and icon not in map_row(service, hero, y)
    assert len(view.actions) <= 4
    view = service.act("test:1", "places")                                     # D-222 (0.30.1): the list moved to 📒 Lugares
    assert any(line.startswith(f"✨ ({x}, {y})") and "llega para saber" in line for line in view.body)
    assert sum(1 for line in view.body if line.startswith("✨ (")) <= service.content.balance["nodes"]["map_lines"]
    far = service._load("test:1")                                              # far from anything you remember: nothing
    place(service, "test:1", x + 13, y + 13, known=["0:0", f"{x + 13}:{y + 13}"])
    assert not any(n[:2] == (x, y) for n in service._node_seen(service._load("test:1")))
    # D-107: exploring around from the zone next to it does NOT discover it ("solo al llegar")
    place(service, "test:1", x, y - 1, known=far.known + [f"{x}:{y - 1}"], exploration={f"{x}:{y - 1}": 100})
    hero = service._load("test:1")
    assert service._explore_target(hero) == (x, y)
    service._explore_step(hero, service._zone(x, y - 1), Rng(3), {"log": [], "got": {}, "until": 0, "done": 0})
    assert f"{x}:{y}" not in service._node_found(hero)
    # arriving: the node is discovered for ever, with its notice; the map shows its resource
    place(service, "test:1", x, y - 1, activity=None)
    service.store.delete("combat", "test:1")                                  # the exploring round may have started a fight
    service.act("test:1", "go:n")
    assert service._load("test:1").activity["kind"] == "travel"
    clock.advance(25 * MINUTE)
    view = service.act("test:1", "home")
    assert f"{x}:{y}" in service._node_found(service._load("test:1"))
    assert "Encontraste un nodo de recursos" in (view.notice or "") and service._item_label(main) in view.notice
    assert any(line.startswith("✨ Nodo de") and service._item_label(main) in line for line in view.body)
    assert any("Estás en un nodo" in line for line in service.act("test:1", "places").body)
    place(service, "test:1", x, y - 2, activity=None)
    hero = service._load("test:1")
    assert (x, y, main) in service._node_seen(hero)
    assert icon in map_row(service, hero, y)
    assert any(line.startswith(f"✨ ({x}, {y})") and f"nodo de {service._item_label(main)}" in line
               for line in service.act("test:1", "places").body)
    assert "Encontraste" not in (service.act("test:1", "home").notice or "")   # discovered once, for ever
    assert not service.texts.missing


def test_standing_in_a_node_zone_discovers_it_once(service):
    ready(service)
    x, y = node_near(service)
    place(service, "test:1", x, y, known=["0:0", f"{x}:{y}"])               # e.g. it was there when the patch came
    view = service.act("test:1", "home")
    assert "Encontraste un nodo de recursos" in (view.notice or "")
    again = service.act("test:1", "home")
    assert "Encontraste" not in (again.notice or "")                          # only the first time
    assert service.store.get("nodes", "test:1")["found"] == [f"{x}:{y}"]


def test_a_node_doubles_its_resource_depletes_slower_and_gives_a_rare(service):
    service.content.balance["nodes"]["rare_chance"] = 1.0                     # always, to see it (test only)
    ready(service)
    x, y = node_near(service)
    main = service._node_main(x, y)
    rare = service._node_rare(x, y)
    place(service, "test:1", x, y, known=["0:0", f"{x}:{y}"])
    hero = service._load("test:1")
    levels = {r: (1.0 if r == main else 0.0) for r in service._zone_resources(x, y)}   # only the node's resource is left
    service.store.put("stock", f"{x}:{y}", {"levels": levels, "at": service.clock.now()})
    danger = service.content.biomes[service._zone(x, y).biome]["danger"] * service.content.balance["gather"]["encounter_scale"]
    seed = next(s for s in range(100) if Rng(s).random() >= danger)             # no ambush this round
    activity = {"log": [], "got": {}, "until": 7, "done": 0}
    assert service._gather_step(hero, service._zone(x, y), Rng(seed), activity) is None
    cfg = service.content.balance
    left = service._stock(x, y)[main]
    picks = round((1.0 - left) / (cfg["stock"]["per_unit"] * cfg["nodes"]["stock_mult"]))
    assert picks >= 1 and activity["node"]["extra"] == picks                   # ×2: one unit more per pick...
    assert activity["got"][main] >= 2 * picks                                  # (the profession may add its own extra unit)
    assert left == pytest.approx(1.0 - picks * cfg["stock"]["per_unit"] * 0.5)  # ...and half the depletion
    assert activity["got"][rare] == 1 and activity["node"]["rare"] == 1
    lines = service._batch_summary(hero, {**activity, "kind": "gather", "done": 1}, "done")
    assert any(f"+{picks} de más" in line for line in lines) and any("En el nodo encontraste" in line for line in lines)
    assert not service.texts.missing


def test_the_grow_screen_marks_the_nodes_you_discovered(service):
    ready(service)
    x, y = node_near(service)
    hero = service._load("test:1")
    assert service._node_grow_mark(hero, x, y) == ""
    service._node_discover(hero, x, y)
    emoji = service.content.items[service._node_main(x, y)]["emoji"]
    assert service._node_grow_mark(hero, x, y) == f" ✨{emoji}"


def test_old_heroes_without_a_node_record_load(service):
    ready(service)
    assert service.store.get("nodes", "test:1") is None
    assert service._node_found(service._load("test:1")) == set()
    assert service.act("test:1", "map").kind == "map"
    assert not service.texts.missing
