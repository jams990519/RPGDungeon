"""Safer trips, monsters at your level, players' camps in sight, the map from 📍 Zona and the trainer's tip (0.34).

[ES] Pruebas de lo que pidió el dueño el 18-oct-2026:
- al moverte sale una pelea de 6 a 14 % por zona (D-266): 📍 Zona lo dice, y en el campamento o la fogata, que está protegida;
- los monstruos de afuera salen de tu nivel, de 1 menos a 2 más (D-266); 🏹 Cazar muestra los de tu nivel;
- los campamentos de jugadores se ven en el 🗺️ Mapa y en 📒 Lugares, aunque nunca los hayas pisado, y se puede viajar a
  ellos (D-267);
- 🗺️ Mapa ancho debajo de 🔗 Moverte y en la pantalla del viaje; ↩️ Volver regresa ahí (D-268);
- el 🧑‍🏫 Entrenador recomienda el oficio de la armadura de tu clase (D-271).
Archivo: tests/test_viajes_y_campamentos.py · Módulo: M2 Mundo, M5 Combate, M14 Oficios · Prueba: engine/service/game.py
(_danger_line, _wild_level, _start_combat, _zone_view, _activity_view, _map_view, _important_places, _can_goto,
_trainer_recommend_lines), content/balance.yaml (explore.arrival_encounter_scale, wild_level, places, professions).
"""

from conftest import make_hero
from test_camps import found_at

from engine.core import Rng


def ids(view):
    return [a.id for a in view.actions]


def move(service, account, x, y, **fields):
    hero = service._load(account)
    hero.x, hero.y = x, y
    for key, value in fields.items():
        setattr(hero, key, value)
    service._save(hero)
    return hero


def test_fights_on_the_way_are_rarer_and_the_zone_says_how_much(service):
    make_hero(service)
    assert service.content.balance["explore"]["arrival_encounter_scale"] == 0.25
    home = service.act("test:1", "home")
    assert any("Zona protegida" in line for line in home.body)                 # the bonfire protects its land
    move(service, "test:1", 3, 0)
    zone = service._zone(3, 0)
    pct = round(service.content.biomes[zone.biome]["danger"] * 25)
    line = next(line for line in service.act("test:1", "home").body if line.startswith("⚔️"))
    assert f"{pct} % de pelea" in line and "de tu nivel" in line and 6 <= pct <= 14


def test_monsters_outside_match_your_level(service):
    make_hero(service)
    hero = move(service, "test:1", 2, 0, level=20)
    levels = {service._wild_level(hero, Rng(seed)) for seed in range(200)}
    assert levels == {19, 20, 21, 22}                                           # one under to two over
    zone = service._zone(2, 0)
    service._start_combat(hero, zone, Rng(7), "encounter.found")
    fight = service.store.get("combat", hero.id)
    enemy = service.content.enemies[fight["enemy"]["id"]]
    level = fight["enemy"]["level"]
    assert enemy["level_min"] <= level <= enemy["level_max"]
    assert level >= min(19, enemy["level_max"]) and level > zone.level + 1   # not the zone's level any more
    low = move(service, "test:1", 2, 0, level=1)
    assert {service._wild_level(low, Rng(seed)) for seed in range(100)} == {1, 2, 3}   # never under level 1


def test_the_map_button_sits_under_move_and_goes_back_there(service):
    make_hero(service)
    zone = service.act("test:1", "home")
    assert ids(zone)[-2:] == ["walk", "zmap"] and zone.layout == [2, 2, 1, 1]
    assert service.act("test:1", "zmap").actions[-1].id == "home"
    assert service.act("test:1", "map").actions[-1].id == "explore_menu"      # from 🧭 Explorar it still goes back there
    service.act("test:1", "go:e")
    trip = service.act("test:1", "home")
    assert trip.kind == "activity" and "zmap" in ids(trip)                     # while travelling too
    assert service.act("test:1", "zmap").kind == "map"


def test_players_camps_are_seen_on_the_map_and_in_places_and_you_can_go(service):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    found_at(service, "test:1", 6, 0)
    assert service.store.get("camp", "6:0")
    map_view = service.act("test:2", "map")                                    # Bram never went there
    assert any("🏕️" in row for row in map_view.body) and any("campamento de jugadores" in line for line in map_view.body)
    places = service.act("test:2", "places")
    assert any("Campo 1 6" in line for line in places.body)
    hero = service._load("test:2")
    assert not hero.remembers(6, 0) and service._can_goto(hero, 6, 0)
    trip = service.act("test:2", "goto:6:0")
    assert service._load("test:2").activity and service._load("test:2").activity["kind"] == "travel", trip.notice


def test_the_trainer_recommends_your_armours_profession(service):
    make_hero(service)                                                         # a warrior: plate
    view = service.act("test:1", "trainer")
    assert any(line.startswith("⭐") and "Herrería" in line and "/herreria" in line for line in view.body)
    hero = service._load("test:1")
    hero.learned = ["herreria"]
    service._save(hero)
    view = service.act("test:1", "trainer")
    assert any(line.startswith("⭐") and "rango 1" in line for line in view.body)
    assert len(view.actions) <= 4
