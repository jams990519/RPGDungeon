"""Professions phase 2, camp side (D-115, D-116): 🎣 Pescador, 🍲 Cocina, 🗿 Cantería, 🏗️ Construcción.

[ES] Pruebas de la fase 2 de los oficios, lado del campamento: el 🐟 pescado solo en las zonas con agua (sin mover los
recursos de tierra) y el 🎣 Pescador que sube al juntarlo; la 🍲 Cocina que gasta carne, pescado y hierbas y llena la
despensa con más raciones (su beneficio y el del Pescador, con el MEJOR rango entre los miembros del campamento); la 🗿
Cantería que vuelve la piedra sillar; las mejoras desde el nivel 7 que piden sillar y tablón sin romper lo ya construido ni
perder lo crudo ya aportado; la 🏗️ Construcción que abarata las obras y la reparación y sube aportando; las 🛠️ defensas
que dañan las oleadas y se reparan desde 🔨 Obras; los héroes y campamentos guardados antes; el tope de 4 botones y que
no falte ningún texto.
"""

from collections import deque

import pytest

from conftest import make_hero
from engine.core import FixedClock, MemoryStore, Rng
from engine.professions import branches_of, xp_for_rank
from engine.professions import rules as profession_rules
from engine.service import GameService
from engine.world import zone_at
from engine.world.resources import water_resources, zone_resources
from test_camp_upgrades import build, camp_at, set_hero
from test_camps import place
from test_guilds import join

KEY = "6:0"
NEW = ("pescador", "cocina", "canteria", "construccion")


def ids(view):
    return [a.id for a in view.actions]


def rank_xp(service, rank):
    return xp_for_rank(service.content.balance["professions"]["rank_formula"], rank)


def set_rank(service, account, pid, rank):
    hero = service._load(account)
    hero.professions[pid] = rank_xp(service, rank)
    service._save(hero)


def ready(service, account="test:1", **values):
    """A hero in the Claro, tutorial done (no rewards in the way), with the given fields set."""
    make_hero(service, account, {"test:1": "Lyra", "test:2": "Bram", "test:3": "Cora"}[account])
    hero = service._load(account)
    hero.tutorial = len(service.content.balance["tutorial"]["steps"])
    for key, value in values.items():
        setattr(hero, key, value)
    service._save(hero)
    return hero


def two_members(service, level):
    """Lyra founds the camp at 6:0 (level `level`) and Bram joins; both stand at its center."""
    ready(service, "test:1")
    ready(service, "test:2")
    camp_at(service, level)
    join(service, "test:2")
    place(service, "test:2", 6, 0)
    return service.store.get("camp", KEY)


def pantry_now(service):
    return service.store.get("pantry", KEY)["rations"]


# ---------------------------------------------------------------- catalog


def test_catalog_of_the_camp_side(content):
    profs, recipes = content.professions["professions"], content.professions["recipes"]
    t = GameService(content, MemoryStore(), FixedClock(), world_seed=7).texts
    assert {pid: profs[pid]["branch"] for pid in NEW} == {"pescador": "gather", "cocina": "craft", "canteria": "refine",
                                                          "construccion": "service"}
    assert profession_rules.camp_perk_professions(profs) == list(NEW)          # D-116: their perks are for the camp
    assert profs["pescador"]["perk"] == {"fish_food": 0.30} and profs["cocina"]["perk"] == {"cook_food": 0.30}
    assert profs["canteria"]["perk"] == {"stone_cost": 0.15}
    assert profs["construccion"]["perk"] == {"build_cost": 0.20, "repair_cost": 0.50}
    assert set(profession_rules.CAMP_PERK_KEYS) <= set(profession_rules.PERK_KEYS)
    for pid in NEW:
        assert t.has(profs[pid]["name_key"]) and t.has(profs[pid]["how_key"]), pid
    for key in profession_rules.CAMP_PERK_KEYS:
        assert t.has(f"prof.perk.{key}"), key
    stations = content.professions["stations"]
    assert {"cocina", "canteria"} <= set(stations["claro"])
    assert stations["camp"]["fogon"] == ["cocina"] and "canteria" in stations["camp"]["taller"]
    # 🍲 Cocina: rank 1 to 100, every recipe needs 2 professions or more and makes more rations than its raw food
    cooking = {rid: r for rid, r in recipes.items() if r["profession"] == "cocina"}
    assert sorted({r["min_rank"] for r in cooking.values()}) == [1, 25, 50, 75, 100]
    items = content.items
    for rid, rdef in cooking.items():
        assert len(branches_of(rdef, profs, recipes)) >= 2, rid
        out_id, n = next(iter(rdef["output"].items()))
        raw = sum(int(items[i].get("food", 0)) * k for i, k in rdef["inputs"].items())
        assert items[out_id]["cooked"] and items[out_id]["kind"] == "food", rid
        assert items[out_id]["food"] * n > raw > 0, rid
        assert rdef["xp"] == 6 * rdef["energy"], rid                            # 6 per ⚡, like every recipe
    # 🗿 Cantería: 3 stones → 1 sillar, priced like the plank (refining never makes coins)
    assert recipes["sillar"] == {"profession": "canteria", "inputs": {"piedra": 3}, "output": {"sillar": 1}, "min_rank": 1,
                                 "energy": 1, "xp": 6}
    assert items["sillar"]["price"] * 0.5 <= 3 * items["piedra"]["price"] * 0.5 + 1 and items["sillar"].get("keep")
    assert profession_rules.refined_from(profs, recipes)["sillar"] == ("piedra", 3)
    assert not t.missing


# ---------------------------------------------------------------- 🎣 fish and the Pescador


def test_fish_only_where_there_is_water_and_land_resources_do_not_move(content):
    seen = {}
    for x in range(-15, 16):
        for y in range(-15, 16):
            biome = zone_at(7, x, y).biome
            land = zone_resources(7, x, y, biome, content.balance, content.biomes)
            water = water_resources(7, x, y, biome, content.balance, content.biomes)
            assert "pescado" not in land                                    # the 6 land resources never change
            assert water in ({}, {"pescado": 0.5})
            seen.setdefault(biome, []).append(bool(water))
    assert all(seen["pantano"])                                             # the whole swamp has water
    for biome in ("bosque", "pradera"):
        share = sum(seen[biome]) / len(seen[biome])
        assert 0.15 <= share <= 0.45, (biome, share)                        # ~3 zones of 10
    for biome, flags in seen.items():                                       # 0.28: the new terrains bring their own "water"
        share = float(content.biomes[biome].get("water", 0.0))
        if share <= 0:
            assert not any(flags), biome                                    # no "water": never fish (montaña, volcán...)
        elif share >= 1:
            assert all(flags), biome                                        # the swamp and the lake: every zone
    assert water_resources(7, 0, 0, "pantano", content.balance, content.biomes) == {}   # fixed zones (the Claro): never


def water_zone(service):
    for r in range(1, 12):
        for x in range(-r, r + 1):
            for y in range(-r, r + 1):
                if max(abs(x), abs(y)) == r and service._zone(x, y).biome == "pantano":
                    return service._zone(x, y)
    raise AssertionError("no swamp near the Claro")


def test_gathering_fish_raises_the_pescador(service):
    hero = ready(service)
    service.content.balance["gather"]["encounter_scale"] = 0                # no ambush (test only)
    zone = water_zone(service)
    assert "pescado" in service._zone_resources(zone.x, zone.y)
    hero = service._load("test:1")
    hero.x, hero.y = zone.x, zone.y
    activity = {"log": [], "got": {}, "until": 1, "done": 0}
    for step in range(12):
        activity["done"] = step
        service._gather_step(hero, zone, Rng(step), activity)
    fish = hero.backpack.get("pescado", 0)
    assert fish > 0 and activity["got"]["pescado"] == fish
    assert hero.professions["pescador"] == fish                             # 1 profession xp per fish
    assert activity["trade"]["pescador"] == fish and "⚒️ Oficios" in service._trade_summary(activity["trade"])
    stock = service._stock(zone.x, zone.y)
    assert stock["pescado"] < 1.0                                           # it runs out and comes back like the rest
    service._save(hero)
    view = service.act("test:1", "oficios")
    assert any("Pescador" in line and "rango" in line for line in view.body)
    assert any("🏰 Es de campamento" in line for line in view.body)
    assert not service.texts.missing


def test_raw_fish_yields_more_with_the_best_pescador_of_the_camp(service):
    two_members(service, 3)
    camp = service.store.get("camp", KEY)
    service._camp_pantry(camp)                                              # the pantry starts (and settles) now
    set_rank(service, "test:2", "pescador", 100)                            # Bram, the camp's fisher
    set_hero(service, "test:1", backpack={"pescado": 10, "carne": 2})
    before = pantry_now(service)
    view = service.act("test:1", "campfeed")
    assert pantry_now(service) - before == pytest.approx(10 + 4 + 3)        # fish 10 + carne 2×2 + 🎣 30 % of 10
    assert "🎣" in view.notice and "Bram" in view.notice
    assert not service.texts.missing


# ---------------------------------------------------------------- 🍲 cooking


def test_cooking_spends_ingredients_and_feeds_the_pantry_with_the_cook_perk(service):
    ready(service, backpack={"carne": 3, "hierba_curativa": 2, "pescado": 4, "madera": 2}, energy=30)
    hero = service._load("test:1")
    xp, energy = hero.xp, hero.energy
    view = service.act("test:1", "mk:racion_campamento:2:0")
    hero = service._load("test:1")
    assert "Hiciste" in view.notice and hero.backpack["racion_campamento"] == 2
    assert hero.backpack["carne"] == 1 and "hierba_curativa" not in hero.backpack and hero.energy == energy - 2
    assert hero.professions["cocina"] == 12
    assert hero.xp == xp + 2 * service.content.balance["professions"]["hero_xp_per_energy"]   # D-108, like refining
    recipe = service.act("test:1", "rec:pescado_asado:0")
    assert any("3 raciones" in line for line in recipe.body)                # what it is worth in the pantry
    service.act("test:1", "mk:pescado_asado:2:0")
    assert service._load("test:1").backpack["pescado_asado"] == 2
    assert service.act("test:1", "mk:guiso_cazador:1:0").notice.startswith("🔒")   # rank 25
    # at the camp: Lyra cooks at the 🔥 Fogón; the best 🍲 Cocina among the members decides the bonus
    ready(service, "test:2")
    camp_at(service, 3)
    join(service, "test:2")
    camp = service.store.get("camp", KEY)
    assert service._stations_here(service._load("test:1")) == ([], None)
    build(service, "fogon")
    assert service._stations_here(service._load("test:1")) == (["cocina"], "camp")
    assert "upsvc" in ids(service.act("test:1", "upgrades"))               # the Fogón's station opens 🏘️ Servicios
    services = service.act("test:1", "upsvc")
    assert "oficios" in ids(services) and len(services.actions) <= 4
    assert ids(service.act("test:1", "oficios"))[:2] == ["est:refine:0", "est:craft:0"]
    service._camp_pantry(camp)
    set_rank(service, "test:2", "cocina", 100)                              # Bram is the camp's cook (rank 100)
    set_hero(service, "test:1", backpack={"racion_campamento": 2, "pescado_asado": 2, "carne": 1})   # founding took the backpack
    before = pantry_now(service)
    view = service.act("test:1", "campfeed")                                # 2 rations (3) + 2 grilled fish (3)
    assert pantry_now(service) - before == pytest.approx(12 + 2 + 3)        # carne 1×2 + 🍲 30 % of 12 → 3
    assert "🍲" in view.notice and "Bram" in view.notice
    assert not service.texts.missing


def test_camp_perks_use_the_best_rank_among_current_members(service):
    two_members(service, 3)
    set_rank(service, "test:1", "cocina", 40)
    set_rank(service, "test:2", "cocina", 100)
    set_rank(service, "test:1", "construccion", 50)
    camp = service.store.get("camp", KEY)
    perks = service._camp_perks(camp)
    assert perks["cook_food"] == (pytest.approx(0.30), "Bram")              # the best, never the sum
    assert perks["build_cost"] == (pytest.approx(0.10), "Lyra") and perks["repair_cost"] == (pytest.approx(0.25), "Lyra")
    assert perks["fish_food"] == (0.0, None) and perks["stone_cost"] == (0.0, None)
    view = service.act("test:1", "claro")
    line = next(line for line in view.body if "Oficios del campamento" in line)
    assert line.startswith("🏰") and "Bram" in line and "Lyra" in line and "+30 %" in line
    assert any("Oficios del campamento" in line for line in service.act("test:1", "oficios").body)
    camp["members"].remove("test:2")                                        # Bram leaves: his perk goes with him
    service.store.put("camp", KEY, camp)
    assert service._camp_perks(camp)["cook_food"] == (pytest.approx(0.12), "Lyra")
    hero = service._load("test:1")                                          # the hero playing counts with what it has now
    hero.professions["cocina"] = rank_xp(service, 100)
    assert service._camp_perks(camp, hero)["cook_food"][0] == pytest.approx(0.30)
    assert service._camp_perks({"claro": True})["cook_food"] == (0.0, None)
    assert profession_rules.camp_best_ranks(service.content.professions["professions"],
                                            {"A": {"cocina": 7}, "B": {"cocina": 7}})["cocina"] == (7, "A")   # ties: the first
    assert not service.texts.missing


# ---------------------------------------------------------------- 🗿 Cantería and the refined upgrades


def test_canteria_refines_stone_into_sillar(service):
    ready(service, backpack={"piedra": 7}, energy=30)
    view = service.act("test:1", "rec:sillar:0")
    assert ids(view)[:2] == ["mk:sillar:1:0", "mk:sillar:2:0"]
    service.act("test:1", "mk:sillar:2:0")
    hero = service._load("test:1")
    assert hero.backpack["sillar"] >= 2 and hero.backpack["piedra"] == 1 and hero.professions["canteria"] == 12
    set_rank(service, "test:1", "canteria", 50)
    assert any("⭐ 15 %" in line for line in service.act("test:1", "rec:sillar:0").body)   # the refiner's extra unit
    set_hero(service, "test:1", backpack={"sillar": 3, "piedra": 3})
    service.act("test:1", "sell:all")                                      # 💱 Vender todo keeps a profession's work
    assert service._load("test:1").backpack == {"sillar": 3}


def test_higher_tier_upgrades_ask_refined_stone_without_breaking_what_was_built(service):
    ready(service)
    camp_at(service, 8)
    catalog = service._upgrade_catalog()
    for uid, udef in catalog.items():                                       # only from level 7 on (D-115)
        refined = {"sillar", "tablon"} & set(udef["cost"])
        assert bool(refined) == (udef["level"] >= 7), uid
    build(service, *[uid for uid in catalog if uid != "torres_arqueros"])   # the foso among them: built for ever
    record = service._upgrades(KEY)
    record["works"]["torres_arqueros"] = {"madera": 280, "piedra": 150}     # what the old cost had asked, already given
    service.store.put("upgrades", KEY, record)
    works = service._open_works(service.store.get("camp", KEY), service._upgrades(KEY))
    assert works == ["torres_arqueros"]
    view = service.act("test:1", "upgrades")
    assert any("Torres de arqueros" in line and "59 %" in line for line in view.body)    # 190 of 320
    # the old raw beyond the new cost counts as refined: 240 madera = 80 tablón, 120 piedra = 40 sillar
    works = service.act("test:1", "upw")
    assert any("Tablón: 80/80" in line for line in works.body) and any("Sillar: 40/40" in line for line in works.body)
    assert service._upgrades(KEY)["works"]["torres_arqueros"] == {"madera": 280, "piedra": 150}   # views never write
    set_hero(service, "test:1", backpack={"pieza_metal": 70, "fibra": 60, "madera": 5}, x=6, y=0)
    view = service.act("test:1", "upg:torres_arqueros")
    record = service._upgrades(KEY)
    assert "torres_arqueros" in record["built"] and "Terminaron" in view.notice
    assert "foso" in record["built"] and service._load("test:1").backpack == {"madera": 5}   # nothing more than it asks
    assert not service.texts.missing


# ---------------------------------------------------------------- 🏗️ Construcción


def test_construccion_lowers_the_works_and_rises_by_giving(service):
    two_members(service, 1)
    camp = service.store.get("camp", KEY)
    fogon = service._upgrade_catalog()["fogon"]
    assert service._upgrade_need(fogon, service._camp_perks(camp)) == {"madera": 20, "piedra": 15}
    set_rank(service, "test:2", "construccion", 100)                        # Bram: −20 % of every material
    assert service._upgrade_need(fogon, service._camp_perks(camp)) == {"madera": 16, "piedra": 12}
    set_rank(service, "test:2", "canteria", 100)                            # and −15 % of the stone
    assert service._upgrade_need(fogon, service._camp_perks(camp)) == {"madera": 16, "piedra": 11}
    trueque = service._upgrade_catalog()["trueque"]
    assert service._upgrade_need(trueque, service._camp_perks(camp))["coins"] == trueque["coins"]   # coins never
    works = service.act("test:1", "upw")
    assert any("Madera: 0/16" in line for line in works.body) and any(line.startswith("🏰") for line in works.body)
    set_hero(service, "test:1", backpack={"madera": 30, "piedra": 30}, professions={})
    view = service.act("test:1", "upg:fogon")
    hero = service._load("test:1")
    assert "fogon" in service._upgrades(KEY)["built"] and hero.backpack == {"madera": 14, "piedra": 19}
    assert hero.professions["construccion"] == 27 and "Construcción +27" in view.notice   # 1 per material given
    # a refined material counts what it carries (3)
    assert service._build_gain(hero, {"sillar": 2, "coins": 50}) and hero.professions["construccion"] == 33
    # if the perks already cover a work, the next 🤲 finishes it even empty-handed
    record = service._upgrades(KEY)
    record["works"]["empalizada"] = {"madera": 24, "fibra": 8}              # 30 madera + 10 fibra, −20 %
    service.store.put("upgrades", KEY, record)
    set_hero(service, "test:1", backpack={})
    view = service.act("test:1", "upg:empalizada")
    assert "empalizada" in service._upgrades(KEY)["built"] and "Terminaron" in view.notice
    assert not service.texts.missing


# ---------------------------------------------------------------- 🛠️ raid damage and repair


def test_raids_damage_the_defenses_and_the_members_repair_them(service, clock):
    two_members(service, 3)
    build(service, "empalizada", "torre_vigia", "trampas")                 # 3 points of 🛡️ Defensa
    camp = service.store.get("camp", KEY)
    assert service._camp_defense(camp) == 3 and service._camp_damage(camp) == 0
    raid = {"kind": "raid", "at": clock.now(), "until": clock.now(), "required": 1, "wins": 0, "fights": {}}
    service._resolve_raid(camp, dict(raid), service._load("test:1"))       # lost: −2
    assert service._camp_damage(camp) == 2 and service._camp_defense(camp) == 1
    end = [v for acc, v in service.tick() if acc == "test:2" and v.kind == "camp_raid_end"]
    assert end and any("dañó las defensas" in line for line in end[0].body)
    service._resolve_raid(camp, dict(raid, wins=1), service._load("test:1"))   # defended: −1, never past what was built
    assert service._camp_damage(camp) == 3 and service._camp_defense(camp) == 0
    service._resolve_raid(camp, dict(raid), service._load("test:1"))
    assert service._camp_damage(camp) == 3
    service._resolve_raid(camp, dict(raid, kind="trial"), service._load("test:1"))   # the Noche de prueba never damages
    assert service._camp_damage(camp) == 3
    service.tick()
    view = service.act("test:1", "claro")
    assert any(line.startswith("🛠️") and "−3" in line for line in view.body) and len(view.actions) <= 4
    up = service.act("test:1", "upgrades")
    assert any(line.startswith("🛠️") for line in up.body) and "upw" in ids(up)
    works = service.act("test:1", "upw")
    assert works.actions[0].id == "uprep" and len(works.actions) <= 4
    assert any("Tablón: 0/6" in line for line in works.body) and any("Sillar: 0/6" in line for line in works.body)
    set_hero(service, "test:1", backpack={"tablon": 4, "sillar": 1})
    view = service.act("test:1", "uprep")
    assert "🤲" in view.notice and service._camp_damage(camp) == 3
    assert service._upgrades(KEY)["repair"] == {"tablon": 4, "sillar": 1}
    assert service._load("test:1").professions["construccion"] == 15     # 5 refined × 3
    assert "No llevas nada" in service.act("test:1", "uprep").notice
    set_rank(service, "test:2", "construccion", 100)                        # Bram, the builder: repairing costs half
    camp = service.store.get("camp", KEY)
    assert service._repair_need(3, service._camp_perks(camp)) == {"tablon": 3, "sillar": 3}
    set_hero(service, "test:1", backpack={"sillar": 5})
    view = service.act("test:1", "uprep")
    record = service._upgrades(KEY)
    assert record["damage"] == 0 and record["repair"] == {} and "Repararon" in view.notice
    assert service._load("test:1").backpack == {"sillar": 3}               # never more than it asks
    assert service._camp_defense(camp) == 3
    news = [v for acc, v in service.tick() if acc == "test:2" and v.kind == "camp_news"]
    assert news and "reparó" in news[0].body[0]
    assert "uprep" not in ids(service.act("test:1", "upw"))
    assert service.act("test:1", "uprep").notice.startswith("🛠️")
    assert not service.texts.missing


def test_a_camp_without_defenses_is_never_damaged(service, clock):
    ready(service)
    camp_at(service, 1)
    camp = service.store.get("camp", KEY)
    raid = {"kind": "raid", "at": clock.now(), "until": clock.now(), "required": 1, "wins": 0, "fights": {}}
    service._resolve_raid(camp, raid, service._load("test:1"))
    assert service._camp_damage(camp) == 0 and service.store.get("upgrades", KEY) is None   # nothing written
    end = [v for _, v in service.tick() if v.kind == "camp_raid_end"]
    assert end and not any("dañó" in line for line in end[0].body)


# ---------------------------------------------------------------- old saves, buttons and texts


def test_old_heroes_and_camps_load(service):
    two_members(service, 4)
    service.store.put("upgrades", KEY, {"built": {"empalizada": 0.0}, "works": {}, "tech": {}})   # saved before D-115
    data = service.store.get("hero", "test:2")
    data.pop("professions", None)
    service.store.put("hero", "test:2", data)
    camp = service.store.get("camp", KEY)
    assert service._camp_damage(camp) == 0 and service._camp_defense(camp) == 1
    assert all(value == (0.0, None) for value in service._camp_perks(camp).values())
    assert service.act("test:1", "claro").kind == "player_camp"
    assert service.act("test:1", "upgrades").kind == "camp_upgrades"
    assert service.act("test:2", "oficios").kind == "professions"
    record = service._upgrades(KEY)
    assert record["damage"] == 0 and record["repair"] == {}


def test_every_camp_screen_keeps_four_buttons_with_damage_and_perks(content):
    def make(path):
        service = GameService(content, MemoryStore(), FixedClock(), world_seed=7)
        two_members(service, 8)
        build(service, "empalizada", "fogon", "refugio", "trueque", "herreria", "biblioteca", "torre_vigia")   # no Taller
        record = service._upgrades(KEY)
        record["damage"] = 2
        service.store.put("upgrades", KEY, record)
        for pid in NEW:
            set_rank(service, "test:2", pid, 60)
        place(service, "test:1", 6, 0, backpack={"madera": 300, "piedra": 300, "fibra": 100, "tablon": 9, "sillar": 9,
                                                 "carne": 6, "pescado": 6, "hierba_curativa": 4},
              gold=5000, energy=50, hp=5)
        view = service.act("test:1", "claro")
        for action in path:
            view = service.act("test:1", action)
        return service, view

    seen, queue, kinds = set(), deque([[]]), set()
    while queue and len(seen) < 150:
        path = queue.popleft()
        service, view = make(path)
        assert len(view.actions) <= 4, (path, view.kind, ids(view))
        assert not service.texts.missing, (path, service.texts.missing)
        kinds.add(view.kind)
        key = (view.kind, tuple(ids(view)))
        if key in seen or len(path) >= 5:
            continue
        seen.add(key)
        for action_id in ids(view):
            if not action_id.startswith(("claim:", "go:", "goto:", "guild", "rename", "leave", "grow")):
                queue.append(path + [action_id])
    assert {"player_camp", "camp_upgrades", "camp_works", "camp_services", "professions", "station", "recipe"} <= kinds
