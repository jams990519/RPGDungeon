"""World generation and travel time (D-58). [ES] Pruebas del mapa infinito y del tiempo de viaje."""

from engine.world import lejania, ring, travel_minutes, zone_at


def test_claro_is_origin():
    zone = zone_at(1, 0, 0)
    assert zone.biome == "claro" and zone.lejania == 0 and zone.ring == 0


def test_generation_is_deterministic_and_borderless():
    a = zone_at(99, 1234, -5678)
    b = zone_at(99, 1234, -5678)
    assert a == b
    assert a.lejania == 5678 and a.ring == 10


def test_lejania_and_ring():
    assert lejania(3, -7) == 7
    assert ring(1) == 1 and ring(3) == 1 and ring(4) == 2 and ring(100) == 10


def test_level_grows_with_distance():
    assert zone_at(5, 30, 0).level > zone_at(5, 2, 0).level


def test_travel_takes_time(content):
    claro = [(0, 0, 0)]
    minutes = [travel_minutes(0, d, claro, content.balance) for d in range(0, 9)]
    assert minutes == [2, 2, 2, 3, 3, 4, 4, 5, 5]          # D-78: 2, 2, 3, 3, 4, 4...
    assert travel_minutes(0, 500, claro, content.balance) == content.balance["travel"]["max_minutes"]
    camp = claro + [(20, 0, 0)]
    assert travel_minutes(21, 0, camp, content.balance) == 2   # the count restarts at your camp


def test_biome_variety(content):
    biomes = {zone_at(7, x, y).biome for x in range(-30, 31, 3) for y in range(-30, 31, 3)}
    assert len(biomes) >= 5
    assert biomes <= set(content.biomes)


def test_block_tilings_are_tetris_pieces():
    """D-186 ("como jugando Tetris"): every 4x4 block is cut into 4 tetrominoes; all 117 tilings, all different."""
    from collections import Counter
    from engine.world.mapgen import block_tilings
    tilings = block_tilings()
    assert len(tilings) == 117 and len(set(tilings)) == 117
    for tiling in tilings:
        assert sorted(Counter(tiling).values()) == [4, 4, 4, 4]


def test_terrain_is_a_patchwork_of_varied_patches(content):
    """D-186: Tetris-like pieces of 4 zones of one terrain each, side by side (two neighbours of the same terrain look like a
    bigger patch); cold north, hot south."""
    from engine.world import terrain_at
    seed = 12345
    grid = {(x, y): terrain_at(seed, x, y) for x in range(-30, 31) for y in range(-30, 31)}
    seen, sizes = set(), []
    for start, kind in grid.items():                       # flood-fill the patches (ruins are loose zones: skipped)
        if start in seen or kind in ("ruinas", "claro"):
            continue
        stack, size = [start], 0
        seen.add(start)
        while stack:
            x, y = stack.pop()
            size += 1
            for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if n in grid and n not in seen and grid[n] == kind:
                    seen.add(n)
                    stack.append(n)
        sizes.append(size)
    from collections import Counter
    count = Counter(sizes)
    assert count.most_common(1)[0][0] == 4                             # most patches are a single Tetris piece
    assert len(count) >= 5 and max(sizes) <= 60                        # some merge into bigger shapes, never a huge blob
    north = [grid[(x, y)] for x in range(-30, 31) for y in range(15, 31)]
    south = [grid[(x, y)] for x in range(-30, 31) for y in range(-30, -14)]
    assert north.count("tundra") > south.count("tundra") and south.count("desierto") > north.count("desierto")
    assert terrain_at(seed, 0, 0) == "claro"


def test_the_service_builds_the_terrain_from_content(service):
    """D-186: content/biomes.yaml "terrain" and balance.yaml terrain feed zone_at; every weighted biome shows up."""
    table = service._terrain_cfg()
    assert table[0] == service.content.balance["terrain"]["climate_slope"]
    kinds = {kind[0] for kind in table[2]}                 # (biome, weight, climate, tier): 0.28 added the tier
    assert kinds == {b for b, d in service.content.biomes.items() if d.get("terrain", {}).get("weight")}
    found = {service._zone(x, y).biome for x in range(-20, 21) for y in range(-20, 21)}
    assert kinds | {"claro"} <= found
