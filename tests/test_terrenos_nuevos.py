"""New terrains of 0.28 (D-185, D-186, D-188): more colours on the Tetris map, the same base resources.

[ES] Pruebas de los terrenos nuevos de la 0.28 ("puedes agregar cuantos colores quieras en cuanto a tipo de zona", D-185;
el mapa "como jugando Tetris", D-186; cuáles y sus números, D-188 provisional). Todo terreno que sale en el mapa (con
"terrain.weight" en content/biomes.yaml) tiene un color único que no confunde el mapa, nombre, emoji, catálogo de 10 a 15
recursos y enemigos en cada franja de nivel (encuentros, campamentos enemigos e incursiones), y aparece en el mapa de una zona
grande. Los nuevos salen menos que los clásicos, se ven en el 🗺️ Mapa de Tetris con su leyenda (investigadas al 50 %, D-220), y los 6 recursos de base no se
movieron (siguen al bioma clásico, que nunca devuelve un terreno nuevo). El material nuevo (🖤 obsidiana) tiene oficio, receta,
precio y textos. Ningún texto falta.
"""

import copy

from conftest import make_hero
from engine.core import FixedClock, MemoryStore
from engine.professions import gatherer_of
from engine.service import GameService
from engine.world import classic_biome, enemy_camps, raids
from engine.world.encounters import encounter_pool
from engine.world.resources import catalog
from test_camps import place

NEW = ("selva", "sabana", "volcan", "canon", "bosque_oscuro", "lago")
CLASSIC = {"claro", "pradera", "bosque", "colinas", "pantano", "montana", "desierto", "tundra", "ruinas"}
BASE = {"madera", "piedra", "fibra", "hierba_curativa", "pieza_metal", "arcilla"}
MAP_MARKS = {"🧍", "👑", "👹", "🏕️", "🕳️", "🌀", "✨", "▪️", "▫️", "◽", "◻️"}   # [ES] lo que el 🗺️ Mapa dibuja encima del terreno (▫️ ◽ ◻️: las zonas grises, D-220)
BANDS = (1, 10, 25, 50, 75, 100)


def terrains(content):
    """The terrains drawn on the map (D-186): the biomes with a terrain weight."""
    return [b for b, d in content.biomes.items() if (d.get("terrain") or {}).get("weight")]


def land_resources(content):
    return BASE | {r for d in content.biomes.values() for r in (d.get("own") or [])}


def test_every_terrain_has_a_unique_colour_a_name_an_emoji_and_a_catalog(service):
    content, t = service.content, service.texts
    kinds = terrains(content)
    assert set(NEW) <= set(kinds)
    colours = [d["color"] for d in content.biomes.values()]
    assert len(colours) == len(set(colours))                                  # one colour per terrain, never repeated
    node_icons = {content.items[r]["emoji"] for r in land_resources(content)}
    for biome in kinds:
        bdef = content.biomes[biome]
        assert bdef["color"] not in MAP_MARKS | node_icons, biome            # the map never mixes it up with a mark or a node
        assert t.has(bdef["name_key"]) and bdef["name_key"] == f"biome.{biome}", biome
        assert bdef["emoji"] and bdef["emoji"] != bdef["color"], biome
        assert 0 < bdef["danger"] < 1 and 0 <= float(bdef.get("water", 0)) <= 1, biome
        assert bdef["terrain"].get("climate", "any") in ("any", "cold", "hot"), biome
        cat = catalog(biome, content.biomes)
        assert 10 <= len(cat) <= 15 and len(cat) == len(set(cat)), (biome, len(cat))
        assert not set(bdef["own"]) & BASE and set(bdef["gather"]) <= BASE, biome
        assert all(r in content.items for r in cat) and bdef["node_rare"] in content.items, biome
    emojis = [content.biomes[b]["emoji"] for b in kinds]
    assert len(emojis) == len(set(emojis))                                    # zone headers never repeat either
    assert not t.missing


def test_new_terrains_are_less_common_than_the_classic_ones(content):
    weight = {b: float(content.biomes[b]["terrain"]["weight"]) for b in terrains(content)}
    classic = [w for b, w in weight.items() if b in CLASSIC and b != "ruinas"]
    assert all(weight[b] < min(classic) for b in NEW)                        # 1 to 1.5, the classic ones 2 or 3
    assert weight["volcan"] == min(weight.values())                           # the rarest one
    assert content.biomes["volcan"]["danger"] == max(d["danger"] for d in content.biomes.values())
    assert content.biomes["lago"]["water"] == 1.0                             # the lake: fish in every zone, like the swamp


def test_every_terrain_has_enemies_at_every_band(content):
    enemies = content.enemies
    for biome in terrains(content):
        for level in BANDS:
            pool = encounter_pool(enemies, biome, level)
            assert pool and all(biome in e["biomes"] and not e.get("boss") for _, e in pool), (biome, level)
            fitting = [eid for eid, e in pool if e["level_min"] <= level <= e["level_max"] and eid != "bandido_errante"]
            assert len(fitting) >= (1 if level == 1 else 2), (biome, level, fitting)   # its own, never another biome's fallback
            members = enemy_camps.garrison(7, 3, 5, 5, enemies, biome, level, (4, 8))   # 👹 enemy camps of that terrain
            assert 4 <= len(members) <= 8 and all(biome in enemies[m["id"]]["biomes"] for m in members), (biome, level)
            raider, raid_level = raids.pick_enemy(enemies, biome, level, roll=0.4)      # 🌊 raids on a camp there
            assert biome in enemies[raider]["biomes"] and enemies[raider]["level_min"] <= raid_level <= enemies[raider]["level_max"]
        far = encounter_pool(enemies, biome, 150)                             # past the last band: the strongest ones
        assert far and all(e["level_max"] == 100 for _, e in far), biome
    assert all(b in enemies["bandido_errante"]["biomes"] for b in NEW)       # the bandit is everywhere
    stripped = copy.deepcopy(enemies)                                         # the old terrains keep the same enemies, in order
    for edef in stripped.values():
        edef["biomes"] = [b for b in edef.get("biomes", []) if b not in NEW]
    for biome in CLASSIC - {"claro"}:
        for level in range(1, 101, 3):
            assert [i for i, _ in encounter_pool(enemies, biome, level)] == [i for i, _ in encounter_pool(stripped, biome, level)]


def test_every_terrain_shows_up_in_a_large_area(content):
    service = GameService(content, MemoryStore(), FixedClock(), world_seed=7)
    found = {}
    for x in range(-40, 41):
        for y in range(-40, 41):
            biome = service._zone(x, y).biome
            found[biome] = found.get(biome, 0) + 1
    assert set(terrains(content)) | {"claro"} == set(found)
    assert all(found[b] < found[c] for b in NEW for c in ("pradera", "bosque")), found
    zone = next(service._zone(x, y) for x in range(-40, 41) for y in range(-40, 41) if service._zone(x, y).biome == "volcan")
    assert service._biome_label(zone) == "🌋 Volcán"                          # the zone header: emoji and name


def test_the_new_terrains_appear_on_the_tetris_map_with_their_legend(service):
    make_hero(service)
    radius = service.content.balance["map_view"]["radius"]
    seen = set()
    for x, y in ((0, 0), (0, 30), (0, -30), (30, 0), (-30, 0)):
        place(service, "test:1", x, y)
        hero = service._load("test:1")                                         # D-220: colours show from 50 %
        hero.exploration.update({f"{a}:{b}": 50 for a in range(x - radius, x + radius + 1)
                                 for b in range(y - radius, y + radius + 1)})
        service._save(hero)
        view = service.act("test:1", "map")
        assert view.kind == "map" and len(view.actions) <= 4
        legend, rows = view.body[1], view.body[2:2 + 2 * radius + 1]
        in_view = {service._zone(a, b).biome for a in range(x - radius, x + radius + 1)
                   for b in range(y - radius, y + radius + 1)}
        for biome in in_view:                                                  # the legend names what you know
            bdef = service.content.biomes[biome]
            assert f"{bdef['color']} {service.texts.t(bdef['name_key'])}" in legend, biome   # the legend builds itself
        for row in rows:
            seen |= {service.content.biomes[b]["color"] for b in NEW if service.content.biomes[b]["color"] in row}
    assert seen == {service.content.biomes[b]["color"] for b in NEW}
    assert not service.texts.missing


def test_adding_terrains_never_moves_the_base_resources(content):
    """D-185: the base resources follow the classic biome, which never returns a new terrain; without the new terrains the
    base resources of every zone are exactly the same."""
    old = copy.deepcopy(content)
    for biome in NEW:
        old.biomes.pop(biome)
    before = GameService(old, MemoryStore(), FixedClock(), world_seed=7)
    after = GameService(content, MemoryStore(), FixedClock(), world_seed=7)
    zones, changed, kept, same_own = 0, 0, 0, 0
    for x in range(-20, 21):
        for y in range(-20, 21):
            zones += 1
            assert classic_biome(7, x, y) in CLASSIC
            assert after._zone_land(x, y)[0] == before._zone_land(x, y)[0], (x, y)
            new, old_biome = after._zone(x, y).biome, before._zone(x, y).biome
            if new != old_biome:
                changed += 1
                assert new in NEW, (x, y, old_biome, new)                    # tier 1: only pieces that turn into a new terrain
            else:
                kept += 1
                same_own += after._zone_land(x, y)[1] == before._zone_land(x, y)[1]
    assert 0.15 <= changed / zones <= 0.40, changed / zones                   # about 3 pieces in 10 got a new colour
    assert same_own / kept >= 0.95                                            # the rest keep their own resources (and nodes)


def test_the_default_terrain_table_matches_the_content(service):
    """mapgen.DEFAULT_TERRAIN (direct calls, tools) is the same table the service builds from content/biomes.yaml."""
    from engine.world.mapgen import DEFAULT_TERRAIN
    table = service._terrain_cfg()
    assert DEFAULT_TERRAIN[:2] == table[:2] and DEFAULT_TERRAIN[3] == table[3]
    assert [tuple(k) for k in DEFAULT_TERRAIN[2]] == [tuple(k) for k in table[2]]
    assert {k[0] for k in table[2] if k[3] == 1} == set(NEW)                  # the new terrains, in their own tier


def test_obsidian_has_a_family_a_use_a_price_and_its_texts(service):
    content, t = service.content, service.texts
    item = content.items["obsidiana"]
    assert item["kind"] == "material" and 2 <= item["price"] <= 6 and not item.get("keep")
    assert gatherer_of("obsidiana", content.professions["professions"]) == "minero"
    recipe = content.professions["recipes"]["sillar_obsidiana"]
    assert recipe["variant"] == "obsidiana" and "obsidiana" in recipe["inputs"]
    assert t.has("item.obsidiana") and t.has("resources.use.obsidiana")
    assert [b for b, d in content.biomes.items() if "obsidiana" in (d.get("own") or [])] == ["volcan"]
    assert "🖤 Obsidiana" in service._recipe_name("sillar_obsidiana")
    assert not t.missing
