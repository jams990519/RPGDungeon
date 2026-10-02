"""Camp improvements and camp knowledge (D-101, provisional): catalog, works, effects, defense, castle, screens.

[ES] Pruebas de las 🔨 Mejoras de los campamentos: el catálogo (18 o más, repartidas en los niveles 1 a 8), las obras
que se abren por nivel y se completan con aportes de cualquier miembro, los efectos (Fogón y Enfermería solo para
miembros en el territorio, Refugio, Puesto de trueque que nunca compra comida, Taller, Herrería, Granero, Ahumadero,
Huerto, Pozo, Cabañas), la 🛡️ Defensa que leerán las incursiones, el castillo que pide 15 mejoras, el 📚 Conocimiento
(con la Biblioteca, uno a la vez, solo miembros en el territorio), el Claro sin mejoras (D-98) y el tope de 4 botones.
"""

from collections import deque

import pytest

from conftest import make_hero
from engine.core import FixedClock, MemoryStore, Rng
from engine.hero import Hero, hero_stats
from engine.service import GameService
from engine.service.game import HUB_BUTTONS, HUB_KINDS
from test_camps import found_at, place
from test_guilds import join, new_guild, set_level

DAY = 24 * 3600
KEY = "6:0"


def ids(view):
    return [a.id for a in view.actions]


def camp_at(service, level, account="test:1"):
    """Found a camp at 6:0 for `account` and set its level straight in the store."""
    found_at(service, account, 6, 0)
    set_level(service, level)
    return service.store.get("camp", KEY)


def build(service, *uids, key=KEY):
    """Mark improvements as built straight in the store (the works themselves are tested below)."""
    record = service._upgrades(key)
    for uid in uids:
        record["built"][uid] = service.clock.now()
    service.store.put("upgrades", key, record)


def learn(service, *tids, key=KEY):
    record = service._upgrades(key)
    record["tech"].setdefault("done", []).extend(tids)
    service.store.put("upgrades", key, record)


def set_hero(service, account, **values):
    hero = service._load(account)
    for k, v in values.items():
        setattr(hero, k, v)
    service._save(hero)


def test_catalog_is_wide_spread_and_complete(content):
    catalog = content.camp_upgrades["upgrades"]
    techs = content.camp_upgrades["knowledge"]
    t = GameService(content, MemoryStore(), FixedClock(), world_seed=7).texts
    assert len(catalog) >= 18
    assert content.balance["upgrades"]["castle_min_built"] == 15 <= len(catalog)
    assert {udef["level"] for udef in catalog.values()} == set(range(1, 9))     # every stage opens something
    for uid, udef in catalog.items():
        assert t.has(udef["name_key"]) and t.has(udef["desc_key"]) and udef["emoji"], uid
        assert udef["cost"] and all(item in content.items for item in udef["cost"]), uid
    defenses = [uid for uid, udef in catalog.items() if udef.get("defense")]
    assert len(defenses) >= 8
    assert len(techs) == 3 and all(t.has(tdef["name_key"]) and t.has(tdef["desc_key"]) for tdef in techs.values())
    first = [udef for udef in catalog.values() if udef["level"] == 1]
    assert all(sum(udef["cost"].values()) <= 60 and not udef.get("coins") for udef in first)   # 2 players, a day or two
    cheapest = sorted(sum(udef["cost"].values()) for udef in catalog.values())[:15]
    assert sum(cheapest) >= 2000                                   # 15 built: weeks for a group, like the castle


def test_works_open_by_camp_level(service):
    make_hero(service, "test:1", "Lyra")
    camp_at(service, 1)
    view = service.act("test:1", "upgrades")
    assert view.kind == "camp_upgrades" and "upw" in ids(view) and len(view.actions) <= 4
    assert any("0 de 20" in line and "15" in line for line in view.body)
    assert any("🔒 En nivel 2" in line for line in view.body)
    works = service.act("test:1", "upw")
    assert [a.id for a in works.actions] == ["upg:fogon", "upg:empalizada", "upgrades"]
    service.act("test:1", "upg:refugio")                           # level 3: still locked
    assert "refugio" not in service._upgrades(KEY)["works"]
    set_level(service, 3)
    open_now = service._open_works(service.store.get("camp", KEY), service._upgrades(KEY))
    assert {"fogon", "empalizada", "torre_vigia", "pozo", "refugio", "trueque", "granero", "trampas"} == set(open_now)
    works = service.act("test:1", "upw")
    assert len(works.actions) == 4 and works.actions[2].id == "upw:1"   # 2 per page + ➡️ Ver más + ↩️ Volver


def test_members_contribute_until_it_is_built(service):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    camp_at(service, 1)
    join(service, "test:2")
    place(service, "test:2", 6, 0, backpack={"madera": 5})
    set_hero(service, "test:1", backpack={"madera": 12, "piedra": 3, "fibra": 4})
    xp_before = service._load("test:1").xp
    view = service.act("test:1", "upg:fogon")                     # 20 madera + 15 piedra
    assert "🤲" in view.notice and "Fogón" in view.notice
    progress = service._upgrades(KEY)["works"]["fogon"]
    assert progress == {"madera": 12, "piedra": 3}
    hero = service._load("test:1")
    assert hero.backpack == {"fibra": 4} and hero.xp > xp_before and hero.merit == 15   # fibra is not asked
    assert "No llevas nada" in service.act("test:1", "upg:fogon").notice
    service.act("test:2", "upg:fogon")                            # any member, no approval
    assert service._upgrades(KEY)["works"]["fogon"]["madera"] == 17
    set_hero(service, "test:2", backpack={"madera": 50, "piedra": 50})
    view = service.act("test:2", "upg:fogon")
    record = service._upgrades(KEY)
    assert "fogon" in record["built"] and "fogon" not in record["works"]
    assert service._load("test:2").backpack == {"madera": 47, "piedra": 38}   # never more than it asks
    assert "Terminaron" in view.notice
    news = [v for acc, v in service.tick() if acc == "test:1"]
    assert news and news[0].kind == "camp_news" and "Fogón" in news[0].body[0]
    assert "upg:fogon" not in ids(service.act("test:2", "upw"))   # built for ever: no longer a work
    set_hero(service, "test:2", activity={"kind": "explore", "until": service.clock.now() + 600, "left": 0, "total": 1},
             backpack={"madera": 50, "fibra": 50})
    view = service.act("test:2", "upg:empalizada")              # busy (exploring): nothing is taken
    assert view.notice == service.texts.t("activity.busy") and "empalizada" not in service._upgrades(KEY)["works"]
    assert service._load("test:2").backpack == {"madera": 50, "fibra": 50}


def test_only_members_at_the_camp_build(service):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    camp_at(service, 1)
    place(service, "test:2", 6, 0, backpack={"madera": 50, "piedra": 50})
    view = service.act("test:2", "upgrades")                      # a visitor: the camp screen, nothing built
    assert view.kind == "player_camp" and service.act("test:2", "upg:fogon").kind == "player_camp"
    assert service._upgrades(KEY)["works"] == {}
    place(service, "test:1", 7, 0)                                # the founder away from the camp center
    assert service.act("test:1", "upg:fogon").kind != "camp_works"
    assert service._upgrades(KEY)["works"] == {}


def regen_gain(service, clock, account, downed=False, minutes=60):
    set_hero(service, account, hp=1, downed=downed, last_regen_at=clock.now())
    clock.advance(minutes * 60)
    service.view(account)
    return service._load(account).hp - 1


def test_fogon_and_enfermeria_only_for_members_in_the_territory(service, clock):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    camp_at(service, 7)
    place(service, "test:2", 6, 0)                                # a visitor in the territory
    base = regen_gain(service, clock, "test:1")
    assert base > 10 and regen_gain(service, clock, "test:2") == base
    build(service, "fogon")
    assert abs(regen_gain(service, clock, "test:1") - 1.5 * base) <= 2       # ×1,5 for the member
    assert regen_gain(service, clock, "test:2") == base                       # nothing for the visitor
    place(service, "test:1", 9, 9)
    assert regen_gain(service, clock, "test:1") == base                       # nothing outside the territory
    place(service, "test:1", 6, 0)
    downed = regen_gain(service, clock, "test:1", downed=True, minutes=120)
    build(service, "enfermeria")
    assert abs(regen_gain(service, clock, "test:1", downed=True, minutes=120) - 1.5 * downed) <= 2
    assert service._camp_regen_mult(service._load("test:2")) == 1.0


def test_refugio_heals_at_the_camp_cheaper_than_the_inn(service, clock):
    make_hero(service, "test:1", "Lyra")
    camp_at(service, 3)
    assert "upsvc" not in ids(service.act("test:1", "upgrades"))  # no service built yet
    build(service, "refugio")
    set_hero(service, "test:1", hp=5, gold=10, last_regen_at=clock.now())
    view = service.act("test:1", "upsvc")
    assert view.kind == "camp_services" and ids(view) == ["crest", "claro"]      # D-192: 🏘️ Servicios is a hub button
    view = service.act("test:1", "crest")
    price = service.content.camp_upgrades["upgrades"]["refugio"]["service"]["rest_price"]
    assert price < service.content.balance["inn"]["price"]
    hero = service._load("test:1")
    assert view.kind == "activity" and hero.activity["kind"] == "rest" and hero.gold == 10 - price
    clock.advance(6 * 60)
    service.view("test:1")
    hero = service._load("test:1")
    assert hero.activity is None and hero.hp == hero_stats(service._kit(hero), hero.level)["max_hp"]
    assert "vida llena" in service.act("test:1", "crest").notice and service._load("test:1").gold == 10 - price


def test_trueque_sells_materials_but_never_food(service):
    make_hero(service, "test:1", "Lyra")
    camp_at(service, 3)
    set_hero(service, "test:1", backpack={"madera": 10, "carne": 3, "provisiones": 2}, gold=0)
    service.act("test:1", "csell")
    assert service._load("test:1").backpack["madera"] == 10      # no Puesto de trueque yet: nothing sold
    build(service, "trueque")
    view = service.act("test:1", "upsvc")
    assert "csell" in ids(view)
    view = service.act("test:1", "csell")
    hero = service._load("test:1")
    assert hero.backpack == {"carne": 3, "provisiones": 2}       # food stays: it feeds the pantry
    assert hero.gold == 10 * max(1, int(service.content.items["madera"]["price"] * 0.5))
    assert "No llevas materiales" in service.act("test:1", "csell").notice


def test_taller_sews_bags_and_builds_chests_at_the_camp(service):
    make_hero(service, "test:1", "Lyra")
    camp_at(service, 5)
    recipe = service.content.balance["currency"]["bag_recipe"]
    set_hero(service, "test:1", backpack=dict(recipe), gold=500, bags=0)
    service.act("test:1", "sew")                                  # no Taller: bags only in the Claro
    assert service._load("test:1").bags == 0
    assert "sew" not in ids(service.act("test:1", "wallet"))
    build(service, "taller")
    view = service.act("test:1", "ctaller")
    # D-109: the Taller also opens the camp's profession stations, so ⚒️ Oficios ("oficios") is its 4th button
    assert view.kind == "camp_workshop" and ids(view) == ["tsew", "tchest", "oficios", "upsvc"]
    view = service.act("test:1", "tsew")
    assert view.kind == "camp_workshop" and service._load("test:1").bags == 1
    bags, materials = service._chest_recipe()
    set_hero(service, "test:1", bags=bags, backpack=dict(materials), chests=0)
    service.act("test:1", "tchest")
    hero = service._load("test:1")
    assert hero.chests == 1 and hero.bags == 0
    assert "sew" in ids(service.act("test:1", "wallet"))         # 💰 Monedas also offers it at the camp


def test_herreria_buys_gear_at_the_camp(service):
    make_hero(service, "test:1", "Lyra")
    camp_at(service, 6)
    worn = set(service._load("test:1").gear.values())
    piece = next(i for i, item in service.content.items.items() if item.get("kind") == "gear" and item.get("price") and i not in worn)
    set_hero(service, "test:1", backpack={piece: 1}, gold=0)
    assert f"sellg:{piece}" not in ids(service.act("test:1", f"item:{piece}"))
    service.act("test:1", f"sellg:{piece}")
    assert service._load("test:1").backpack == {piece: 1}
    build(service, "herreria")
    assert f"sellg:{piece}" in ids(service.act("test:1", f"item:{piece}"))
    service.act("test:1", f"sellg:{piece}")
    hero = service._load("test:1")
    assert hero.backpack == {} and hero.gold > 0


def test_granero_huerto_and_ahumadero_change_the_pantry(service, clock):
    make_hero(service, "test:1", "Lyra")
    camp = camp_at(service, 4)
    service.act("test:1", "claro")
    service.store.put("pantry", KEY, {"rations": 10.0, "at": clock.now()})
    clock.advance(DAY)
    service.act("test:1", "claro")
    assert service.store.get("pantry", KEY)["rations"] == pytest.approx(9)       # 1 active member, 1 day
    build(service, "granero")
    clock.advance(DAY)
    view = service.act("test:1", "claro")
    assert service.store.get("pantry", KEY)["rations"] == pytest.approx(8.1)     # 10 % less
    assert any("Granero" in line for line in view.body)
    build(service, "huerto")
    clock.advance(DAY)
    service.act("test:1", "claro")
    assert service.store.get("pantry", KEY)["rations"] == pytest.approx(8.2)     # −0,9 + 1 from the garden
    set_hero(service, "test:1", backpack={"carne": 2})
    service.act("test:1", "campfeed")
    assert service.store.get("pantry", KEY)["rations"] == pytest.approx(12.2)    # 2 × 2 rations
    build(service, "ahumadero")
    set_hero(service, "test:1", backpack={"carne": 2})
    view = service.act("test:1", "campfeed")
    assert service.store.get("pantry", KEY)["rations"] == pytest.approx(18.2)    # 2 × (2 + 1)
    assert "Ahumadero" in view.notice
    assert camp["x"] == 6


def test_cabanas_and_pozo(service, clock):
    make_hero(service, "test:1", "Lyra")
    camp = camp_at(service, 4)
    cap = service._members_cap(camp)
    build(service, "cabanas")
    assert service._members_cap(camp) == cap + 2
    resources = list(service._zone_resources(6, 0))
    service.store.put("stock", KEY, {"levels": {r: 0.0 for r in resources}, "at": clock.now()})
    service.store.put("stock", "9:9", {"levels": {r: 0.0 for r in service._zone_resources(9, 9)}, "at": clock.now()})
    clock.advance(10 * 3600)
    before = service._stock(6, 0)[resources[0]]
    build(service, "pozo")
    after = service._stock(6, 0)[resources[0]]
    assert after == pytest.approx(before * 1.5)                   # 50 % faster in the territory
    outside = list(service._stock(9, 9).values())[0]
    assert outside == pytest.approx(before)                       # not outside it


def test_camp_defense_sums_the_built_defenses(service):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    camp = camp_at(service, 8)
    assert service._camp_defense(camp) == 0
    build(service, "empalizada", "fogon")
    assert service._camp_defense(camp) == 1
    catalog = service._upgrade_catalog()
    build(service, *[uid for uid, udef in catalog.items() if udef.get("defense")])
    total = sum(udef.get("defense", 0) for udef in catalog.values())
    assert service._camp_defense(camp) == total == 11
    assert service._camp_defense(camp, night=True) == 12          # 🔥 Braseros count once more at night
    assert service._camp_defense({"claro": True}) == 0 and service._camp_defense(None) == 0
    assert service._camp_effect(camp, "warning_hours") == 2       # 🗼 Torre de vigía: for the raids
    assert any("Defensa: 11" in line for line in service.act("test:1", "claro").body)
    place(service, "test:2", 6, 0)
    assert any("Defensa: 11" in line for line in service.act("test:2", "claro").body)   # visitors see it too


def test_castle_needs_fifteen_improvements(service):
    make_hero(service, "test:1", "Lyra")
    cfg = service.content.balance["guild"]
    castle = next(s["from_level"] for s in service.content.balance["camps"]["stages"] if s["id"] == "castillo")
    camp_at(service, castle - 1)
    place(service, "test:1", 6, 0, backpack={"madera": 999, "piedra": 999, "fibra": 999}, chests=99)
    new_guild(service)
    guild = service.store.get("guild", KEY)
    guild["level"] = cfg["castle_min_level"]
    service.store.put("guild", KEY, guild)
    for n in range(2, cfg["castle_min_members"] + 1):
        make_hero(service, f"test:{n}", f"Miembro{chr(64 + n)}")
        join(service, f"test:{n}")
    need = service.content.balance["upgrades"]["castle_min_built"]
    build(service, *list(service._upgrade_catalog())[:need - 1])
    view = service.act("test:1", "grow")                          # the guild is ready, 14 built: blocked
    assert view.kind == "camp_grow" and ids(view) == ["upgrades", "campmgmt"]   # D-192: back to 🏰 Gestionar
    assert any("▫️" in line and f"{need} mejoras" in line and f"tienen {need - 1}" in line for line in view.body)
    service.act("test:1", "claim:7:0")
    assert service.store.get("camp", KEY)["level"] == castle - 1
    build(service, list(service._upgrade_catalog())[need - 1])
    view = service.act("test:1", "grow")
    assert view.kind == "camp_trial"                              # D-99: then only the Noche de prueba is left
    data = service.store.get("camp", KEY)
    data["trial_won"] = True
    service.store.put("camp", KEY, data)
    view = service.act("test:1", "grow")
    assert any("✅" in line and f"{need} mejoras" in line for line in view.body)
    claims = [a.id for a in view.actions if a.id.startswith("claim:")]
    service.act("test:1", claims[0])
    assert service.store.get("camp", KEY)["level"] == castle
    assert service._castle_upgrades(service.store.get("camp", KEY)) == []     # a castle keeps growing freely


def test_old_castles_and_lower_levels_ask_nothing(service):
    make_hero(service, "test:1", "Lyra")
    camp = camp_at(service, 3)
    assert service._castle_upgrades(camp) == []
    set_level(service, 9)                                         # a castle from before D-101, no improvements
    place(service, "test:1", 6, 0, backpack={"madera": 999, "piedra": 999, "fibra": 999}, chests=99)
    service.act("test:1", "claim:7:0")
    assert service.store.get("camp", KEY)["level"] == 10


def test_knowledge_needs_the_library_one_at_a_time(service):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    camp_at(service, 7)
    join(service, "test:2")
    place(service, "test:2", 6, 0)
    view = service.act("test:1", "know")                           # no Biblioteca yet
    assert view.kind == "camp_upgrades" and "know" not in ids(view) and "Biblioteca" in (view.notice or "")
    build(service, "biblioteca")
    view = service.act("test:1", "know")
    assert view.kind == "camp_knowledge" and ids(view) == ["kstart:herramientas", "kstart:cartografia", "kstart:rastreo", "upgrades"]
    view = service.act("test:1", "kstart:herramientas")
    assert ids(view) == ["kgive", "upgrades"]
    assert "otra cosa" in service.act("test:2", "kstart:cartografia").notice   # one at a time
    tdef = service._tech_catalog()["herramientas"]
    set_hero(service, "test:1", backpack={"madera": 150}, gold=0)
    service.act("test:1", "kgive")
    set_hero(service, "test:2", backpack={"pieza_metal": 60}, gold=1000)
    view = service.act("test:2", "kgive")
    tech = service._upgrades(KEY)["tech"]
    assert tech["done"] == ["herramientas"] and tech["current"] is None
    assert service._load("test:2").gold == 1000 - tdef["coins"] and service._load("test:2").backpack == {"pieza_metal": 10}
    assert "Aprendieron" in view.notice
    assert [v for acc, v in service.tick() if acc == "test:1" and v.kind == "camp_news"]
    assert ids(service.act("test:1", "know")) == ["kstart:cartografia", "kstart:rastreo", "upgrades"]


def test_knowledge_effects_only_for_members_in_the_territory(service):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    camp_at(service, 7)
    build(service, "biblioteca")
    learn(service, "herramientas", "cartografia", "rastreo")
    member, visitor = service._load("test:1"), service._load("test:2")
    assert service._camp_tech_bonus(member, 6, 0, "gather_bonus") == pytest.approx(0.10)
    assert service._camp_tech_bonus(member, 6, 0, "explore_points") == 5
    assert service._camp_tech_bonus(member, 6, 0, "loot_bonus", "carne") == pytest.approx(0.10)
    assert service._camp_tech_bonus(member, 7, 0, "loot_bonus", "carne") == pytest.approx(0.10)   # Rastreo: next to the land
    assert service._camp_tech_bonus(member, 7, 0, "gather_bonus") == 0                            # the others: only inside
    assert service._camp_tech_bonus(member, 9, 9, "loot_bonus", "carne") == 0
    assert service._camp_tech_bonus(visitor, 6, 0, "gather_bonus") == 0                           # members only
    zone = service._zone(6, 0)
    explored = []
    for account in ("test:1", "test:2"):
        hero = service._load(account)
        hero.camp = "6:0" if account == "test:1" else None
        hero.x, hero.y = 6, 0                                     # D-107: exploring studies the zone where you stand first
        hero.exploration = {}
        service._explore_step(hero, zone, Rng(99), {"log": [], "got": {}})
        explored.append(hero.exploration["6:0"])
    assert explored[0] == explored[1] + 5                         # Cartografía: same draw, +5 points


def test_the_claro_has_no_improvements(service):
    make_hero(service, "test:1", "Lyra")
    set_hero(service, "test:1", hp=5)
    set_hero(service, "test:1", backpack={"madera": 50, "piedra": 50, "fibra": 4, "pieza_metal": 1}, gold=500, bags=0)
    for action in ("upgrades", "upw", "upg:fogon", "upsvc", "crest", "csell", "ctaller", "tsew", "tchest", "know",
                   "kstart:rastreo", "kgive"):
        view = service.act("test:1", action)
        assert view.kind in ("claro", "activity", "zone"), (action, view.kind)
        assert len(view.actions) <= (8 if view.kind == "claro" else 4)           # D-192: the Claro hub, up to 8
    assert list(service.store.items("upgrades")) == []
    hero = service._load("test:1")
    assert hero.backpack == {"madera": 50, "piedra": 50, "fibra": 4, "pieza_metal": 1} and hero.bags == 0 and hero.gold == 500
    assert service._built({"claro": True}) == [] and service._camp_effect({"claro": True}, "regen_mult") == 0
    assert "Mejoras" not in " ".join(service.act("test:1", "claro").body)


def test_camps_saved_before_the_patch_still_work(service):
    make_hero(service, "test:1", "Lyra")
    service.store.put("camp", "0:3", {"name": "Viejo", "founder": "Lyra", "founder_id": "test:1",
                                       "members": ["test:1"], "relations": {}, "asked": [], "x": 0, "y": 3})
    hero = Hero.from_dict(service.store.get("hero", "test:1"))
    hero.camp, hero.x, hero.y = "0:3", 0, 3
    service.store.put("hero", "test:1", hero.to_dict())
    view = service.act("test:1", "claro")
    assert view.kind == "player_camp" and ids(view) == ["cook", "research", "oficios", "trainer", "upsvc", "board", "campmgmt", "dudas"]   # D-192: the camp hub
    assert ids(service.act("test:1", "campmgmt")) == ["grow", "upgrades", "guild", "claro"]
    assert any("Mejoras construidas: 0" in line and "Defensa: 0" in line for line in view.body)
    assert service.act("test:1", "upgrades").kind == "camp_upgrades"


def test_every_upgrade_screen_keeps_four_buttons(content):
    """Crawl every button from the camp screen with all services built, as member, at levels 2 and 8."""

    def make(level, path):
        service = GameService(content, MemoryStore(), FixedClock(), world_seed=7)
        make_hero(service, "test:1", "Lyra")
        camp_at(service, level)
        if level >= 8:
            build(service, "refugio", "trueque", "taller", "herreria", "biblioteca", "fogon")
        place(service, "test:1", 6, 0, backpack={"madera": 300, "piedra": 300, "fibra": 100, "pieza_metal": 20}, gold=5000, hp=5)
        view = service.act("test:1", "claro")
        for action in path:
            view = service.act("test:1", action)
        return service, view

    for level in (2, 8):
        seen, queue, kinds = set(), deque([[]]), set()
        while queue:
            path = queue.popleft()
            service, view = make(level, path)
            if view.layout:                     # D-189: an amount picker (reached from 🛠️ Fabricar since D-192)
                assert view.layout[-1] == 1 and sum(view.layout) == len(view.actions), (level, path, view.layout)
            else:
                assert len(view.actions) <= (8 if view.kind in HUB_KINDS else 4), (level, path, view.kind, ids(view))   # D-192
            assert not service.texts.missing, (path, service.texts.missing)
            kinds.add(view.kind)
            key = (view.kind, tuple(ids(view)))
            if key in seen or len(path) >= 4:
                continue
            seen.add(key)
            for action_id in ids(view):
                if not action_id.startswith(("claim:", "go:", "goto:", "guild", "rename", "leave")):
                    queue.append(path + [action_id])
        assert {"player_camp", "camp_upgrades", "camp_works"} <= kinds, level
        if level >= 8:
            assert {"camp_services", "camp_workshop", "camp_knowledge"} <= kinds
