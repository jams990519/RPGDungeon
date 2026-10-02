"""Solo dungeons (D-164, D-165, D-170, D-171): the 🕳️ small dungeon, the 🌀 deep dungeon and the 🕳️ cave marks of the map.

[ES] Pruebas de las mazmorras para uno: las entradas salen siempre en el mismo lugar (semilla del mundo), desde Lejanía 2,
nunca en el Claro, la guarida ni el territorio de un campamento de jugadores, y un campamento enemigo en pie tapa la entrada
ese día. Lo de adentro cambia cada día y es igual para todos: la familia (nunca la misma dos días seguidos), el jefe, el
camino y el cofre. La chica tiene siempre 4 salas y el jefe, el cofre sale una vez por día, es modesto y puede traer equipo de
otra clase (D-165); huir o caer no borra lo despejado. La profunda se endurece piso a piso, se elige ⬇️ Bajar o 🚪 Salir con
lo ganado, caer deja la mitad de la bolsa, el récord queda y entre pisos la vida no vuelve sola. El mapa marca 🕳️ (la cueva, D-181) lo que está
cerca y 🕳️ / 🌀 lo que ya conoces. Las peleas automáticas nunca pelean una mazmorra (D-114). Ninguna pantalla pasa de 4 botones
(6 en combate), ningún texto falta y los héroes de antes cargan.
"""

from collections import deque

import pytest

from conftest import make_hero
from engine.core import FixedClock, MemoryStore, Rng
from engine.hero import Hero, hero_stats
from engine.service import GameService
from engine.world import dungeons as dungeon_rules
from engine.world.mapgen import lejania
from test_camps import place
from test_hunt import win

DAY = 86400
MINUTE = 60
SEED = 12345


def ids(view):
    return [a.id for a in view.actions]


def all_dungeons(service, radius=12):
    return [(x, y, service._dng_kind(x, y)) for x in range(-radius, radius + 1) for y in range(-radius, radius + 1)
            if service._dng_kind(x, y)]


def dungeon_zone(service, kind):
    """The nearest dungeon of that kind whose entrance no enemy camp covers today (the test seed has some near the Claro)."""
    found = sorted(((x, y) for x, y, k in all_dungeons(service) if k == kind and not service._dng_blocked(x, y)),
                   key=lambda p: (abs(p[0]) + abs(p[1]), p))
    assert found, f"no {kind} dungeon near the Claro"
    return found[0]


def at_dungeon(service, kind, account="test:1", name="Lyra", **extra):
    """A hero standing at the nearest dungeon of that kind, tutorial done, full energy, level 20 (it wins most fights)."""
    make_hero(service, account, name)
    x, y = dungeon_zone(service, kind)
    hero = service._load(account)
    data = {"energy": 50, "tutorial": len(service.content.balance["tutorial"]["steps"]), "known": ["0:0", f"{x}:{y}"]}
    data.update(extra)
    place(service, account, x, y, **data)
    return x, y


def lose(service, account, outcome="defeat"):
    """End the open fight as a defeat (or a flight), through the normal end of every fight."""
    state = service.store.get("combat", account)
    state["outcome"] = outcome
    hero = service._load(account)
    view = service._end_combat(hero, state)
    service._save(hero)
    return view


def record(service, account="test:1"):
    return service.store.get("dungeon", account) or {}


# ---------------------------------------------------------------- pure rules

def test_entrances_are_fixed_spread_out_and_never_near_the_claro(content):
    cfg = content.balance["dungeons"]
    size = cfg["stretch"]
    found = {}
    for bx in range(-4, 4):
        for by in range(-4, 4):
            here = dungeon_rules.entrances(SEED, bx, by, cfg)
            assert here == dungeon_rules.entrances(SEED, bx, by, cfg)                  # always the same
            if any(lejania(x, y) >= cfg["min_lejania"] for x in range(bx * size, bx * size + size)
                   for y in range(by * size, by * size + size)):
                assert 2 <= len(here) <= 3, (bx, by)                                    # D-181: 2 or 3 per stretch
            for i, (x, y, kind) in enumerate(here):
                assert lejania(x, y) >= cfg["min_lejania"] and kind in ("small", "deep")
                assert dungeon_rules.stretch_of(x, y, size) == (bx, by)
                assert dungeon_rules.entrance_at(SEED, x, y, cfg) == kind
                for x2, y2, _ in here[i + 1:]:
                    assert max(abs(x - x2), abs(y - y2)) > cfg["spacing"]               # never side by side
                found[(x, y)] = kind
    old = dict(cfg, second_chance=0.5, third_chance=0.0)                             # the counts before D-181
    for bx in range(-4, 4):
        for by in range(-4, 4):
            before = dungeon_rules.entrances(SEED, bx, by, old)
            assert dungeon_rules.entrances(SEED, bx, by, cfg)[:len(before)] == before    # nothing moved: only added
    kinds = list(found.values())
    assert kinds.count("deep") and kinds.count("small") > kinds.count("deep")         # deep ones are rarer
    # an excluded zone (the Guardian's lair) never holds one: another zone of its stretch is used
    x, y = next(iter(found))
    assert dungeon_rules.entrance_at(SEED, x, y, cfg, excluded=((x, y),)) is None
    assert dungeon_rules.entrances(SEED, *dungeon_rules.stretch_of(x, y, size), cfg, excluded=((x, y),))


def test_the_family_changes_every_day_and_every_family_comes_back(content):
    families = list(content.dungeons["families"])
    for x, y in ((3, 3), (-7, 5), (12, -4)):
        days = [dungeon_rules.family_of_day(SEED, day, x, y, families) for day in range(0, 6 * len(families))]
        assert all(a != b for a, b in zip(days, days[1:]))                              # never the same two days in a row
        for start in range(0, len(days), len(families)):
            assert sorted(days[start:start + len(families)]) == sorted(families)       # each one once per cycle
    assert dungeon_rules.family_of_day(SEED, 40, 3, 3, ["a", "b"]) != dungeon_rules.family_of_day(SEED, 41, 3, 3, ["a", "b"])
    assert dungeon_rules.family_of_day(SEED, 40, 3, 3, ["a"]) == "a"


def test_rooms_have_a_fixed_structure_and_the_boss_is_the_strongest(content):
    from engine.world.raids import power
    fams = content.dungeons["families"]
    for day in range(30):
        for fid, fdef in fams.items():
            rooms = dungeon_rules.delve_rooms(SEED, day, 4, 3, content.enemies, fdef["members"], 9, 4)
            assert len(rooms) == 5 and rooms[-1]["boss"] and not any(r["boss"] for r in rooms[:-1])
            assert all(r["id"] in fdef["members"] and r["level"] == 9 for r in rooms)
            pool = dungeon_rules.level_pool(content.enemies, fdef["members"], 9)
            assert power(content.enemies[rooms[-1]["id"]], 9) == max(power(e, 9) for _, e in pool)
    assert all(not content.enemies[m].get("boss") for f in fams.values() for m in f["members"])


def test_deep_floors_get_harder_and_every_fifth_has_the_boss(content):
    cfg = content.balance["dungeons"]["deep"]
    members = content.dungeons["families"]["manada"]["members"]
    previous = None
    for floor in range(1, 16):
        plan = dungeon_rules.floor_plan(SEED, 20, 3, 3, content.enemies, members, 5, floor, cfg)
        assert 1 <= len(plan) <= 2 and (floor > 1 or len(plan) == 1)
        assert all(f["level"] == 5 + floor - 1 for f in plan)
        assert any(f["boss"] for f in plan) == (floor % cfg["boss_every"] == 0)
        common = [f for f in plan if not f["boss"]] or plan
        if previous:
            assert common[0]["hp_mult"] > previous["hp_mult"] and common[0]["attack_mult"] > previous["attack_mult"]
        previous = common[0]
        assert plan == dungeon_rules.floor_plan(SEED, 20, 3, 3, content.enemies, members, 5, floor, cfg)
    boss = [f for f in dungeon_rules.floor_plan(SEED, 20, 3, 3, content.enemies, members, 5, 5, cfg) if f["boss"]][0]
    hp, attack = dungeon_rules.floor_mults(5, cfg, False)
    assert boss["hp_mult"] == pytest.approx(hp * cfg["boss_hp_mult"]) and boss["attack_mult"] == pytest.approx(attack * cfg["boss_attack_mult"])
    pot = {"coins": 9, "items": {"piel": 3, "carne": 1}, "gear": ["a", "b", "c"]}
    assert dungeon_rules.defeat_share(pot, 0.5) == {"coins": 4, "items": {"piel": 1}, "gear": ["a"]}


def test_the_chest_is_modest_and_its_gear_can_be_of_any_class(content):
    cfg = content.balance["dungeons"]
    chest = dungeon_rules.delve_chest(SEED, 5, 4, 3, 10, {"piel": 1.0, "carne": 1.0}, cfg["small"]["chest"], cfg["coin_unit"],
                                      cfg["coin_level_scale"])
    low, high = cfg["small"]["chest"]["materials"]
    assert low <= sum(chest["items"].values()) <= high and set(chest["items"]) <= {"piel", "carne"}
    camp = content.balance["enemy_camps"]["chest"]
    assert chest["coins"] < 10 * camp["coins_per_level"] / 3 and chest["gear_chance"] < camp["gear_chance"]   # modest (D-170)
    types = set()
    for seed in range(400):
        piece = dungeon_rules.chest_gear(content.items, content.balance["gear"], 10, Rng(seed), 1.0)
        item = content.items[piece]
        assert item["kind"] == "gear" and not item.get("source")                       # never crafted or Guardian gear
        assert 10 - content.balance["gear"]["level_window"][0] <= item.get("req_level", 1) <= 11
        types.add(item["type"])
    weapons = {w for ws in content.balance["gear"]["weapons_by_group"].values() for w in ws}
    armors = set(content.balance["gear"]["armor_by_group"].values())
    assert weapons | armors <= types                                                    # D-165: every type drops
    assert dungeon_rules.chest_gear(content.items, content.balance["gear"], 10, Rng(1), 0.0) is None


def test_families_point_to_real_enemies_items_and_texts(service):
    fams = service.content.dungeons["families"]
    for fid, fdef in fams.items():
        assert service.texts.has(fdef["name_key"]), fid
        assert all(m in service.content.enemies for m in fdef["members"]), fid
        assert all(m in service.content.items for m in fdef["materials"]), fid
    assert len(service.texts.list("dungeon.rooms")) >= service.content.balance["dungeons"]["small"]["rooms"]
    assert service.texts.list("dungeon.boss_rooms")


# ---------------------------------------------------------------- placement in the world

def test_placement_is_the_same_for_everyone_and_respects_the_exclusions(content, clock):
    one = GameService(content, MemoryStore(), clock, world_seed=SEED)
    two = GameService(content, MemoryStore(), clock, world_seed=SEED)
    found = all_dungeons(one)
    assert found and found == all_dungeons(two)
    clock.advance(DAY)
    assert all_dungeons(one) == found                                                   # the places never move
    cfg = one._guardian_cfg()
    for x, y, _ in found:
        assert lejania(x, y) >= 2 and (x, y) != (cfg["x"], cfg["y"]) and not one._territory(x, y)
    for x, y in one._claro_zones():
        assert one._dng_kind(x, y) is None
    make_hero(one)
    x, y, _ = found[0]
    one.store.put("camp", f"{x}:{y}", {"name": "Roca", "founder": "Lyra", "founder_id": "test:1", "members": ["test:1"],
                                        "relations": {}, "asked": [], "x": x, "y": y, "zones": [[x, y]]})
    one.store.put("territory", f"{x}:{y}", {"camp": f"{x}:{y}"})
    assert one._dng_kind(x, y) is None                                                  # a player camp's land hides it


def test_a_standing_enemy_camp_covers_the_entrance_for_the_day(content, clock):
    service = GameService(content, MemoryStore(), clock, world_seed=SEED)
    make_hero(service)
    zones = [(x, y) for x, y, _ in all_dungeons(service)]
    today = service._today()
    day = next(d for d in range(today, today + 400) if any(service._ecamp_exists(x, y, d) for x, y in zones))
    clock.advance((day - today) * DAY)
    x, y = next((x, y) for x, y in zones if service._ecamp_exists(x, y))
    place(service, "test:1", x, y, energy=50, tutorial=len(content.balance["tutorial"]["steps"]))
    assert service._dng_blocked(x, y)
    assert "dungeon" not in ids(service.act("test:1", "explore_menu"))                  # the camp's menu
    view = service.act("test:1", "dgo")
    assert "campamento enemigo" in view.notice and service._load("test:1").energy == 50
    assert any("tapa la entrada" in line for line in service.act("test:1", "home").body)


# ---------------------------------------------------------------- the content changes every day

def test_the_content_changes_with_the_day_and_is_the_same_for_everyone(content, clock):
    one = GameService(content, MemoryStore(), clock, world_seed=SEED)
    two = GameService(content, MemoryStore(), clock, world_seed=SEED)
    x, y = dungeon_zone(one, "small")
    today = one._dng_today(x, y)
    assert today == two._dng_today(x, y)
    assert len(today["rooms"]) == content.balance["dungeons"]["small"]["rooms"] + 1 and len(today["path"]) == 4
    seen = []
    for _ in range(4):
        clock.advance(DAY)
        tomorrow = one._dng_today(x, y)
        assert tomorrow["family"] != today["family"] and len(tomorrow["rooms"]) == len(today["rooms"])
        seen.append(tomorrow["family"])
        today = tomorrow
    assert len(set(seen)) >= 3


# ---------------------------------------------------------------- 🕳️ the small dungeon

def test_the_small_dungeon_has_four_rooms_and_its_chest_once_a_day(service, clock):
    x, y = at_dungeon(service, "small", level=20)
    menu = service.act("test:1", "explore_menu")
    assert ids(menu) == ["explore", "gather", "dungeon", "map"]                         # 🕳️ Entrar takes 🏹 Cazar's place
    screen = service.act("test:1", "dungeon")
    assert screen.kind == "dungeon" and ids(screen) == ["dgo", "hunt", "explore_menu"]
    info = service._dng_today(x, y)
    cost = service.content.balance["dungeons"]["small"]["fight_energy"]
    for room in range(4):
        view = service.act("test:1", "dgo")
        state = service.store.get("combat", "test:1")
        assert view.kind == "combat" and state["dungeon"]["room"] == room and not state["dungeon"]["boss"]
        assert state["enemy"]["id"] == info["rooms"][room]["id"]
        end = win(service, "test:1")
        assert record(service)["delves"][f"{x}:{y}"]["cleared"] == room + 1 and "dgo" in ids(end)
        assert len(end.actions) <= 4
    assert service._load("test:1").energy == 50 - 4 * cost
    before = service._load("test:1")
    service.act("test:1", "dgo")
    state = service.store.get("combat", "test:1")
    assert state["dungeon"]["boss"] and state["enemy"]["id"] == info["boss"]
    from engine.combat import make_combat
    plain = make_combat(info["boss"], service.content.enemies[info["boss"]], info["level"], service._kit(before), 1)
    assert state["enemy"]["max_hp"] == round(plain["enemy"]["max_hp"] * 1.8)
    assert any("Jefe de la mazmorra" in line for line in service._combat_view(before, state).body)
    hero = service._load("test:1")
    end = win(service, "test:1")
    after = service._load("test:1")
    chest = service._dng_chest_of(info)
    edef = service.content.enemies[info["boss"]]
    assert after.xp - hero.xp == service._zone_xp(edef["xp"], info["level"])          # no extra experience in the chest
    assert after.gold >= hero.gold + chest["coins"] and any("cofre" in line for line in end.body)
    for item, n in chest["items"].items():
        assert after.backpack.get(item, 0) >= hero.backpack.get(item, 0) + n
    assert record(service)["delves"][f"{x}:{y}"]["done"] and "dgo" not in ids(end)
    again = service.act("test:1", "dgo")                                                 # once a day: nothing charged
    assert "Ya la terminaste" in again.notice and service._load("test:1").energy == after.energy
    assert "dgo" not in ids(service.act("test:1", "dungeon"))
    clock.advance(DAY)                                                                   # a new day: a new dungeon
    assert "dgo" in ids(service.act("test:1", "dungeon")) and service._dng_record(service._load("test:1"))["delves"] == {}
    assert not service.texts.missing


def test_fleeing_or_falling_keeps_the_rooms_cleared_today(service):
    x, y = at_dungeon(service, "small", level=20)
    for _ in range(2):
        service.act("test:1", "dgo")
        win(service, "test:1")
    service.act("test:1", "dgo")
    end = lose(service, "test:1", "fled")
    assert record(service)["delves"][f"{x}:{y}"]["cleared"] == 2 and any("queda" in line for line in end.body)
    place(service, "test:1", x, y, energy=50, downed=False, hp=10**6)
    service.act("test:1", "dgo")
    end = lose(service, "test:1", "defeat")
    hero = service._load("test:1")
    assert hero.downed and record(service)["delves"][f"{x}:{y}"]["cleared"] == 2
    refused = service.act("test:1", "dgo")                                               # malherido: nothing charged
    assert "malherido" in refused.notice and service._load("test:1").energy == hero.energy
    place(service, "test:1", x, y, downed=False)
    service.act("test:1", "dgo")
    assert service.store.get("combat", "test:1")["dungeon"]["room"] == 2               # it goes on from room 3


def test_a_fight_from_yesterday_does_not_count_for_today(service, clock):
    x, y = at_dungeon(service, "small", level=20)
    service.act("test:1", "dgo")
    clock.advance(DAY)
    end = win(service, "test:1")
    assert record(service).get("delves", {}).get(f"{x}:{y}", {}).get("cleared", 0) == 0
    assert any("cambió con el día" in line for line in end.body)


def test_rewards_per_energy_stay_close_to_hunting(content):
    """D-118 / D-108: a small dungeon gives about the experience per ⚡ of hunting (no extra experience in its chest)."""
    from engine.world.encounters import clamp_level, encounter_pool
    scale = content.balance["hero"]["xp_level_scale"]

    def zxp(base, level):
        return int(base * (1 + scale * (level - 1)))

    cost = content.balance["dungeons"]["small"]["fight_energy"]
    hunt_cost = content.balance["hunt"]["energy"]
    for zone_level in (3, 10, 30, 60, 90):
        hunts = []
        for biome in content.biomes:
            if biome != "claro":
                pool = encounter_pool(content.enemies, biome, zone_level)
                hunts.append(sum(zxp(e["xp"], clamp_level(e, zone_level)) for _, e in pool) / len(pool) / hunt_cost)
        delves = []
        level = zone_level + content.balance["dungeons"]["level_bonus"]
        for fdef in content.dungeons["families"].values():
            pool = dungeon_rules.level_pool(content.enemies, fdef["members"], level)
            rooms = sum(zxp(e["xp"], level) for _, e in pool) / len(pool)
            boss = zxp(content.enemies[dungeon_rules.boss_of(pool, level)]["xp"], level)
            delves.append((4 * rooms + boss) / (5 * cost))
        ratio = (sum(delves) / len(delves)) / (sum(hunts) / len(hunts))
        assert 0.9 <= ratio <= 1.2, (zone_level, ratio)


# ---------------------------------------------------------------- 🌀 the deep dungeon

def test_the_deep_dungeon_goes_down_floor_by_floor(service, clock):
    x, y = at_dungeon(service, "deep", level=20)
    menu = service.act("test:1", "explore_menu")
    assert "dungeon" in ids(menu)
    screen = service.act("test:1", "dungeon")
    assert ids(screen) == ["dgo", "hunt", "explore_menu"]
    cfg = service.content.balance["dungeons"]["deep"]
    view = service.act("test:1", "dgo")
    state = service.store.get("combat", "test:1")
    assert view.kind == "combat" and state["dungeon"]["floor"] == 1 and record(service)["deep"]["floor"] == 1
    assert service._load("test:1").energy == 50 - cfg["enter_energy"] - cfg["fight_energy"]
    end = win(service, "test:1")
    run = record(service)["deep"]
    assert run["cleared"] == 1 and run["floor"] == 2 and run["pot"]["coins"] > 0
    assert ids(end)[:2] == ["dgo", "dout"] and record(service)["best"] == 1 and len(end.actions) <= 4
    assert service._dng_top(x, y, service._today()) == [(1, "Lyra")]
    screen = service.act("test:1", "dungeon")
    assert ids(screen) == ["dgo", "dout", "potions", "explore_menu"]
    assert any("piso 1" in line for line in screen.body) and any("Lyra (piso 1)" in line for line in screen.body)
    # no free healing between floors: an hour later the life is the same
    hero = service._load("test:1")
    hero.hp = 50
    service._save(hero)
    clock.advance(60 * MINUTE)
    assert service._load("test:1").hp == 50 and service.act("test:1", "dungeon").kind == "dungeon"
    assert service._load("test:1").hp == 50
    # ⬇️ Bajar: floor 2 is harder (level + 1 and more life)
    place(service, "test:1", x, y, hp=10**6, energy=50)
    service.act("test:1", "dgo")
    state = service.store.get("combat", "test:1")
    assert state["dungeon"]["floor"] == 2 and state["enemy"]["level"] == service._dng_today(x, y)["level"] + 1
    assert service._load("test:1").energy == 50 - cfg["fight_energy"]
    while record(service)["deep"]["cleared"] < 2:
        win(service, "test:1")
        if record(service)["deep"]["cleared"] < 2:
            service.act("test:1", "dgo")
    pot = record(service)["deep"]["pot"]
    gold = service._load("test:1").gold
    out = service.act("test:1", "dout")                                                  # 🚪 Salir con lo ganado: all of it
    assert record(service)["deep"] is None and service._load("test:1").gold == gold + pot["coins"]
    assert "bolsa entera" in out.notice and record(service)["best"] == 2
    # the life comes back again once out
    hero = service._load("test:1")
    hero.hp = 50
    service._save(hero)
    clock.advance(60 * MINUTE)
    service.act("test:1", "home")
    assert service._load("test:1").hp > 50
    assert not service.texts.missing


def test_falling_in_the_deep_dungeon_keeps_half_of_the_pot_and_the_record(service):
    x, y = at_dungeon(service, "deep", level=20)
    service.act("test:1", "dgo")
    win(service, "test:1")
    service.act("test:1", "dgo")
    while record(service)["deep"]["cleared"] < 2:
        win(service, "test:1")
        if record(service)["deep"]["cleared"] < 2:
            service.act("test:1", "dgo")
    service.act("test:1", "dgo")
    pot = record(service)["deep"]["pot"]
    gold = service._load("test:1").gold
    end = lose(service, "test:1", "defeat")
    hero = service._load("test:1")
    lost = int(gold * service.content.balance["hero"]["defeat_gold_loss"])
    assert record(service)["deep"] is None and record(service)["best"] == 2 and hero.downed
    assert hero.gold == gold - lost + pot["coins"] // 2 and any("mitad" in line for line in end.body)
    refused = service.act("test:1", "dgo")
    assert "malherido" in refused.notice


def test_leaving_the_zone_closes_the_run_with_the_whole_pot(service, clock):
    x, y = at_dungeon(service, "deep", level=20)
    service.content.balance["explore"]["arrival_encounter_scale"] = 0      # no ambush on arrival (test only: the run would
    service.act("test:1", "dgo")                                            # close after that fight, never in the middle)
    win(service, "test:1")
    pot = record(service)["deep"]["pot"]
    gold = service._load("test:1").gold
    service.act("test:1", "go:n")
    clock.advance(30 * MINUTE)
    view = service.act("test:1", "home")
    assert record(service)["deep"] is None and service._load("test:1").gold >= gold + pot["coins"] - 1
    assert "bolsa entera" in (view.notice or "")


def test_automatic_fights_never_fight_in_a_dungeon(service):
    at_dungeon(service, "small", level=20)
    service.act("test:1", "opt:fights")
    service.act("test:1", "dgo")
    hero = service._load("test:1")
    activity = {"kind": "explore", "done": 1, "left": 3, "got": {}, "log": [], "until": 0}
    lines = service._batch_fight(hero, activity, "aviso")
    assert lines is not None and service.store.get("combat", "test:1") is not None
    assert not activity.get("fights")


# ---------------------------------------------------------------- the 🗺️ Mapa (D-171)

def test_the_map_shows_something_is_there_before_you_know_what(service):
    make_hero(service)
    x, y = dungeon_zone(service, "deep")
    place(service, "test:1", x, y + 2, known=["0:0", f"{x}:{y + 2}"])                    # 2 zones away: within hint_radius
    view = service.act("test:1", "map")
    assert any(line.startswith(f"🕳️ ({x}, {y})") and "cueva" in line for line in view.body)   # D-181: a cave, not which
    assert not any(line.startswith(f"🌀 ({x}, {y})") for line in view.body)
    assert any(a.id == f"goto:{x}:{y}" for a in view.actions) and len(view.actions) <= 4
    service.act("test:1", f"goto:{x}:{y}")
    assert service._load("test:1").activity["kind"] == "travel"
    place(service, "test:1", x, y + 1, activity=None, known=["0:0", f"{x}:{y}", f"{x}:{y + 1}"])
    view = service.act("test:1", "map")
    assert any(line.startswith(f"🌀 ({x}, {y})") for line in view.body)                # now you know what it is
    far = [x + 12, y + 12]
    place(service, "test:1", far[0], far[1], known=["0:0", f"{far[0]}:{far[1]}"])
    assert not any(f"({x}, {y})" in line for line in service.act("test:1", "map").body)
    assert not service.texts.missing


def test_arriving_reveals_the_dungeon(service, clock):
    make_hero(service)
    x, y = dungeon_zone(service, "small")
    place(service, "test:1", x - 1, y, energy=50, tutorial=len(service.content.balance["tutorial"]["steps"]))
    service.act("test:1", "go:e")
    clock.advance(30 * MINUTE)
    view = service.act("test:1", "home")
    assert "mazmorra chica" in (view.notice or "") and any("🕳️ Mazmorra chica" in line for line in view.body)


# ---------------------------------------------------------------- screens, texts and old saves

@pytest.mark.parametrize("kind", ["small", "deep"])
def test_every_dungeon_screen_keeps_four_buttons_and_its_texts(content, kind):
    def build(path):
        service = GameService(content, MemoryStore(), FixedClock(), world_seed=SEED)
        at_dungeon(service, kind, level=20, hp=10**6)
        view = service.act("test:1", "explore_menu")
        for action in path:
            view = service.act("test:1", action)
        return service, view

    seen, queue, kinds = set(), deque([[]]), set()
    while queue and len(seen) < 40:
        path = queue.popleft()
        service, view = build(path)
        limit = 6 if view.kind == "combat" else 4
        if view.layout:                                 # D-189: amount pickers: a row of small amounts, then one wide back
            assert view.layout[-1] == 1 and sum(view.layout) == len(view.actions), (path, view.kind, ids(view))
        else:
            assert len(view.actions) <= limit, (path, view.kind, ids(view))
        assert not service.texts.missing, (path, service.texts.missing)
        kinds.add(view.kind)
        key = (view.kind, tuple(ids(view)))
        if key in seen or len(path) >= 4:
            continue
        seen.add(key)
        for action_id in ids(view):
            if not action_id.startswith(("go:", "goto:", "do:", "ab:", "use:", "prey", "flee")):
                queue.append(path + [action_id])
    assert {"explore_menu", "dungeon", "combat", "map"} <= kinds


def test_old_heroes_load_and_play_a_dungeon(service):
    make_hero(service)
    x, y = dungeon_zone(service, "small")
    data = service.store.get("hero", "test:1")
    for key in ("options", "story", "factions", "journal", "bio", "gear_signatures", "gear_enchants", "professions"):
        data.pop(key, None)
    data.update({"x": x, "y": y, "energy": 50, "level": 20})
    service.store.put("hero", "test:1", data)
    assert service.store.get("dungeon", "test:1") is None
    view = service.act("test:1", "dungeon")
    assert view.kind == "dungeon" and "dgo" in ids(view)
    assert service.act("test:1", "dgo").kind == "combat"
    assert isinstance(Hero.from_dict(service.store.get("hero", "test:1")), Hero)
    assert not service.texts.missing


def test_no_dungeon_here_is_refused_without_spending(service):
    make_hero(service)
    place(service, "test:1", 1, 0, energy=50)
    assert service._dng_kind(1, 0) is None
    for action in ("dungeon", "dgo", "dout"):
        view = service.act("test:1", action)
        assert view.notice and service._load("test:1").energy == 50, action
    assert hero_stats(service._kit(service._load("test:1")), 1)["max_hp"] > 0
