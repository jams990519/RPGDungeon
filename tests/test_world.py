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
    origin, dest = zone_at(5, 0, 0), zone_at(5, 0, 1)
    known = travel_minutes(origin, dest, content.biomes, content.balance, True)
    unknown = travel_minutes(origin, dest, content.biomes, content.balance, False)
    assert known >= 1 and unknown > known


def test_biome_variety(content):
    biomes = {zone_at(7, x, y).biome for x in range(-30, 31, 3) for y in range(-30, 31, 3)}
    assert len(biomes) >= 5
    assert biomes <= set(content.biomes)
