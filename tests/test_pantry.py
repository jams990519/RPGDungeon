"""Settlement pantry, phase 1 of "building is not enough" (D-93, provisional; D-95: only player camps).

[ES] Pruebas de la despensa: la comida que comen cada día los miembros activos de un campamento de jugadores
(desde nivel 3). El Claro no se mantiene: no tiene dueño (D-95), así que nunca tiene despensa, su posada cura y
su obra sube apenas se paga. Cubre el consumo con el tiempo, el campamento que no crece con la despensa vacía,
la carne de las bestias, las provisiones del mercader, la migración (nadie empieza castigado) y el tope de 4 botones.
"""

import pytest

from conftest import make_hero
from engine.combat import make_combat
from engine.hero import Hero
from engine.world import pantry as pantry_rules
from test_camps import found_at, place

DAY = 24 * 3600
ALDEA = 2


def set_stage(service, stage, progress=None):
    data = service._settlement()
    data["stage"] = stage
    data["progress"] = progress or {}
    service.store.put("settlement", "claro", data)


def set_rations(service, key, rations):
    service.store.put("pantry", key, {"rations": float(rations), "at": service.clock.now()})


def give(service, account, **items):
    hero = service._load(account)
    for item_id, n in items.items():
        hero.backpack[item_id] = hero.backpack.get(item_id, 0) + n
    service._save(hero)


def rations(service, key):
    return service.store.get("pantry", key)["rations"]


def camp_at_level(service, level, members=("test:1",)):
    """Found a camp at 6:0 for test:1, then set its level and members straight in the store."""
    found_at(service, "test:1", 6, 0)
    camp = service.store.get("camp", "6:0")
    camp["level"], camp["members"] = level, list(members)
    service.store.put("camp", "6:0", camp)
    for member in members:
        hero = service._load(member)
        hero.camp, hero.x, hero.y = "6:0", 6, 0
        service._save(hero)
    return camp


def test_pure_rules():
    assert pantry_rules.consume(10, 3, 2, 1) == 4
    assert pantry_rules.consume(3, 5, 2, 1) == 0                      # never below 0
    assert pantry_rules.consume(3, 0, 9, 1) == 3                      # nobody active: nobody eats
    assert pantry_rules.days_left(9, 0, 1) == 9                       # 0 eaters count as 1 (no division by 0)
    states = {"abundancia": 14, "holgada": 7, "justa": 3, "escasez": 1, "hambruna": 0}
    assert [pantry_rules.state(d, states) for d in (0, 1, 2, 3, 6, 7, 13, 14)] == \
        ["hambruna", "escasez", "escasez", "justa", "justa", "holgada", "holgada", "abundancia"]


def test_the_claro_never_has_a_pantry(service):
    make_hero(service)
    for stage in range(len(service.content.balance["settlement"]["stages"])):
        set_stage(service, stage)
        view = service.act("test:1", "claro")
        # D-109: the Claro has the basic profession stations, so ⚒️ Oficios ("oficios") is its 3rd button (4 in all)
        assert [a.id for a in view.actions] == ["shop", "inn", "oficios", "home"], stage
        assert not any("Despensa" in line for line in view.body)
        assert service.act("test:1", "feed").kind == "claro"         # an old 0.10 button lands on the Claro
    assert service.store.get("pantry", "claro") is None
    assert "claro_from_stage" not in service.content.balance["pantry"]


def test_consumption_over_time_counts_only_active_members(service, clock):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    camp = camp_at_level(service, 3, members=("test:1", "test:2"))
    view = service.act("test:1", "claro")                    # at the camp: its screen, with the pantry
    assert any("Despensa" in line for line in view.body)
    assert rations(service, "6:0") == 7 * 2                  # migration: 7 days for every member
    clock.advance(DAY)
    service.act("test:1", "claro")                           # only Lyra played in the last 24 h
    assert service._camp_active(camp) == 1
    assert rations(service, "6:0") == pytest.approx(13)
    service.act("test:2", "claro")
    clock.advance(DAY)
    service.act("test:1", "claro")
    service.act("test:2", "claro")
    assert service._camp_active(camp) == 2
    assert rations(service, "6:0") == pytest.approx(11)      # 2 active members × 1 day
    clock.advance(30 * DAY)
    service.act("test:1", "claro")
    assert rations(service, "6:0") == 0                      # floor at 0, never negative


def test_the_claro_inn_heals_even_with_old_pantry_data(service):
    set_stage(service, ALDEA)
    make_hero(service)
    set_rations(service, "claro", 0)                                # left by 0.10: ignored now (D-95)
    hero = service._load("test:1")
    hero.hp, hero.gold, hero.last_regen_at = 5, 50, service.clock.now()
    service._save(hero)
    view = service.act("test:1", "inn")
    assert view.kind == "activity" and service._load("test:1").activity["kind"] == "rest"


def test_the_claro_keeps_its_stage_and_never_grows(service):
    needs = dict(service.content.balance["settlement"]["stages"][ALDEA]["needs"])
    set_stage(service, ALDEA, dict(needs, madera=needs["madera"] - 1))
    make_hero(service)
    give(service, "test:1", madera=1)
    view = service.act("test:1", "donate")
    assert service._settlement()["stage"] == ALDEA and "no crece" in view.notice   # what it had stays (D-98)
    assert service._load("test:1").backpack["madera"] == 1


def test_camp_cannot_grow_with_an_empty_pantry(service):
    make_hero(service)
    found_at(service, "test:1", 6, 0)
    service.act("test:1", "claim:7:0")
    view = service.act("test:1", "claim:8:0")                       # level 3: aldea, the pantry opens
    camp = service.store.get("camp", "6:0")
    assert camp["level"] == 3
    assert any("Despensa" in line for line in view.body)
    assert [a.id for a in view.actions] == ["grow", "campfeed", "guild", "upgrades"]    # 4 buttons at most (rename: in 🛡️ Gremio, D-97; D-101: 🔨 Mejoras)
    assert rations(service, "6:0") == 7                             # a new pantry starts with 7 days
    set_rations(service, "6:0", 0)
    view = service.act("test:1", "grow")
    assert view.kind == "player_camp" and "despensa" in view.notice.lower()
    assert any("vacía" in line for line in view.body)
    service.act("test:1", "claim:6:1")
    assert service.store.get("camp", "6:0")["level"] == 3           # nothing paid, nothing lost
    give(service, "test:1", carne=1)
    view = service.act("test:1", "campfeed")
    assert "2 raciones" in view.notice and rations(service, "6:0") == 2
    assert service.act("test:1", "grow").kind == "camp_grow"
    service.act("test:1", "claim:6:1")
    camp = service.store.get("camp", "6:0")
    assert camp["level"] == 4 and len(camp["zones"]) == 4 and camp["members"] == ["test:1"]


def test_camp_pantry_needs_level_three_and_being_there(service):
    make_hero(service)
    found_at(service, "test:1", 6, 0)
    give(service, "test:1", carne=2)
    view = service.act("test:1", "campfeed")
    assert "nivel 3" in view.notice and service._load("test:1").backpack["carne"] == 2
    assert not any(a.id == "campfeed" for a in view.actions)


def _victories(service, enemy_id, seeds):
    edef = service.content.enemies[enemy_id]
    drops = []
    for seed in seeds:
        hero = service._load("test:1")
        hero.backpack = {}
        state = make_combat(enemy_id, edef, edef["level_min"], service._kit(hero), seed)
        state["outcome"] = "victory"
        service._end_combat(hero, state)
        drops.append(hero.backpack.get("carne", 0))
    return drops


def test_beasts_drop_meat_and_people_do_not(service):
    make_hero(service)
    wolf = _victories(service, "lobo_ceniciento", range(60))
    assert 15 < sum(1 for n in wolf if n) < 45                       # about half the wins
    assert set(wolf) == {0, 1, 2}                                    # 1 or 2 pieces
    assert not any(_victories(service, "bandido_errante", range(30)))
    assert not any(_victories(service, "esqueleto_soldado", range(30)))
    for enemy_id, edef in service.content.enemies.items():
        if "carne" in edef.get("loot", {}):
            assert 0.4 <= edef["loot"]["carne"] <= 0.6, enemy_id


def test_merchant_sells_provisions_without_losing_buttons(service):
    make_hero(service)
    give(service, "test:1", madera=3, carne=1)
    hero = service._load("test:1")
    hero.gold = 100
    service._save(hero)
    view = service.act("test:1", "shop")
    ids = [a.id for a in view.actions]
    assert "buy:provisiones" in ids and "sell:all" in ids and len(ids) <= 4
    price = service.content.items["provisiones"]["price"]
    assert price >= 10                                               # an expensive emergency (coin sink)
    service.act("test:1", "buy:provisiones")
    hero = service._load("test:1")
    assert hero.backpack["provisiones"] == 1 and hero.gold == 100 - price
    service.act("test:1", "sell:all")
    hero = service._load("test:1")
    assert "madera" not in hero.backpack and hero.backpack["carne"] == 1    # food is kept: it feeds the pantry
    assert hero.backpack["provisiones"] == 1                         # bought food is never sold back by mistake
    hero.backpack = {}
    service._save(hero)
    assert [a.id for a in service.act("test:1", "shop").actions][-1] == "claro"


def test_claro_screens_keep_four_buttons(service):
    set_stage(service, ALDEA)
    make_hero(service)
    # D-109: ⚒️ Oficios ("oficios") joined the Claro; still 4 buttons at most (D-75)
    assert [a.id for a in service.act("test:1", "claro").actions] == ["shop", "inn", "oficios", "home"]


def test_every_claro_button_works_from_aldea(content):
    from collections import deque

    from engine.core import FixedClock, MemoryStore
    from engine.service import GameService

    def build(path):
        service = GameService(content, MemoryStore(), FixedClock(), world_seed=7)
        set_stage(service, ALDEA)
        make_hero(service, "test:1", "Lyra")
        give(service, "test:1", carne=2, provisiones=1, madera=5)
        view = service.act("test:1", "claro")
        for action in path:
            view = service.act("test:1", action)
        return service, view

    follow = ("camp", "shop", "feed", "donate", "inn", "claro", "buy:provisiones", "sell:all")
    seen, queue = set(), deque([[]])
    while queue:
        path = queue.popleft()
        service, view = build(path)
        assert len(view.actions) <= 4, (path, view.kind)
        assert not service.texts.missing, (path, service.texts.missing)
        key = (view.kind, tuple(a.id for a in view.actions))
        if key in seen:
            continue
        seen.add(key)
        queue.extend(path + [a.id] for a in view.actions if len(path) < 3 and a.id in follow)
    assert {"claro", "shop"} <= {kind for kind, _ in seen}           # D-98: no common work screen any more


def test_old_heroes_load_and_get_seen_lazily(service, clock):
    make_hero(service)
    data = service.store.get("hero", "test:1")
    data.pop("seen_at", None)                                       # a hero saved before the patch
    service.store.put("hero", "test:1", data)
    assert Hero.from_dict(data).seen_at == 0
    service.act("test:1", "hero")
    assert service.store.get("hero", "test:1")["seen_at"] == clock.now()
    assert "test:1" in service._active()
    clock.advance(25 * 3600)
    assert "test:1" not in service._active()                         # gone quiet: does not eat


def test_existing_camp_starts_with_a_week_for_its_members(service):
    for n, name in ((1, "Lyra"), (2, "Bram"), (3, "Cora")):
        make_hero(service, f"test:{n}", name)
    camp_at_level(service, 5, members=("test:1", "test:2", "test:3"))   # a camp that was already a pueblo
    view = service.act("test:1", "claro")
    assert rations(service, "6:0") == 7 * 3
    assert any("Abundancia" in line for line in view.body)          # 21 rations for the 1 who plays today
