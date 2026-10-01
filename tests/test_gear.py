"""Gear and loot with requirements (D-77).

[ES] Prueba el equipo: cada clase tiene su arma y armadura, el equipo inicial, los requisitos
(tipo y nivel), el botín "para ti" y que poner o quitar piezas nunca duplique ni pierda nada.
"""

from conftest import make_hero
from engine.core import Rng
from engine.hero import Hero, hero_stats
from engine.hero.gear import allowed_types, can_use, equip, roll_gear, starter_gear


def test_every_class_has_gear(content):
    cfg = content.balance["gear"]
    groups = {c.get("group") for c in content.classes.values() if not c.get("retired")}
    gear = [it for it in content.items.values() if it.get("kind") == "gear"]
    for group in groups:
        armor = cfg["armor_by_group"][group]
        weapons = cfg["weapons_by_group"][group]
        assert weapons, group
        for typ in [armor, *weapons, "joya"]:
            tiers = sorted(it["tier"] for it in gear if it["type"] == typ)
            assert tiers == [1, 2, 3, 4], (group, typ)
    for it in gear:
        assert it["slot"] in cfg["slots"] and it["rarity"] in cfg["rarity_icon"]


def test_new_hero_starts_with_weapon_and_armor(service):
    make_hero(service, class_id="mago_fuego")
    hero = service._load("test:1")
    assert hero.gear == {"arma": "baston_1", "armadura": "tela_1"}
    stats = hero_stats(service._kit(hero), hero.level)
    bare = hero_stats(service.content.classes[hero.class_id], hero.level)
    assert hero.hp == stats["max_hp"] > bare["max_hp"]
    assert stats["attack"] > bare["attack"]


def test_old_heroes_get_starter_gear_once(service):
    make_hero(service, class_id="guerrero")
    data = service.store.get("hero", "test:1")
    data.pop("gear"), data.pop("gear_started")
    service.store.put("hero", "test:1", data)
    service.act("test:1", "hero")
    hero = service._load("test:1")
    assert hero.gear == {"arma": "espada_1", "armadura": "placas_1"} and hero.gear_started
    service.act("test:1", "unequip:arma")
    assert "arma" not in service._load("test:1").gear      # not given again


def test_requirements_type_and_level(content):
    classes, balance, items = content.classes, content.balance, content.items
    hero = Hero(id="h", name="H", class_id="picaro", level=1)
    assert can_use(items["daga_1"], hero, classes, balance) is None
    assert can_use(items["placas_1"], hero, classes, balance) == "type"
    assert can_use(items["daga_3"], hero, classes, balance) == "level"
    hero.backpack = {"daga_3": 1, "placas_1": 1}
    assert equip(hero, "daga_3", items, classes, balance) == "level"
    assert equip(hero, "placas_1", items, classes, balance) == "type"
    hero.level = 5
    assert equip(hero, "daga_3", items, classes, balance) is None
    assert hero.gear["arma"] == "daga_3" and "daga_3" not in hero.backpack


def test_equip_swaps_without_losing_pieces(service):
    make_hero(service, class_id="guerrero")
    hero = service._load("test:1")
    hero.level, hero.backpack["espada_2"] = 3, 1
    service._save(hero)
    view = service.act("test:1", "item:espada_2")
    assert any(a.id == "equip:espada_2" for a in view.actions)
    service.act("test:1", "equip:espada_2")
    hero = service._load("test:1")
    assert hero.gear["arma"] == "espada_2" and hero.backpack.get("espada_1") == 1 and "espada_2" not in hero.backpack


def test_loot_is_mostly_for_you_and_near_your_level(content):
    classes, balance, items = content.classes, content.balance, content.items
    hero = Hero(id="h", name="H", class_id="sacerdote", level=2)
    mine = allowed_types(classes, balance, hero)
    drops = [roll_gear(items, classes, balance, hero, 2, Rng(seed, 0)) for seed in range(3000)]
    drops = [d for d in drops if d]
    assert 0.10 < len(drops) / 3000 < 0.20
    share = sum(items[d]["type"] in mine for d in drops) / len(drops)
    assert 0.6 < share < 0.8
    assert all(items[d]["req_level"] <= 3 for d in drops)


def test_gear_screens_keep_four_buttons_and_sell_in_claro(service):
    make_hero(service, class_id="guerrero")
    hero = service._load("test:1")
    for item_id in ("espada_2", "daga_1", "tela_1", "joya_1", "placas_2"):
        hero.backpack[item_id] = 1
    service._save(hero)
    view = service.act("test:1", "gear")
    assert view.kind == "gear" and len(view.actions) <= 4
    assert any(a.id.startswith("gear:") for a in view.actions)
    seen = set()
    for _ in range(5):
        seen |= {a.id for a in view.actions if a.id.startswith("item:")}
        view = service.act("test:1", next(a.id for a in view.actions if a.id.startswith("gear:")))
    assert len(seen) == 7                                    # 2 worn + 5 in the backpack
    item = service.act("test:1", "item:tela_1")
    assert not any(a.id.startswith("equip:") for a in item.actions)
    gold = service._load("test:1").gold
    service.act("test:1", "sellg:tela_1")
    hero = service._load("test:1")
    assert "tela_1" not in hero.backpack and hero.gold > gold


def test_starter_gear_exists_for_every_spec(content):
    for class_id, cdef in content.classes.items():
        if cdef.get("retired"):
            continue
        hero = Hero(id="h", name="H", class_id=class_id)
        assert len(starter_gear(content.items, content.classes, content.balance, hero)) == 2, class_id
