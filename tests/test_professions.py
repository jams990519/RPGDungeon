"""Chained professions, phase 1 (D-109): gather -> refine -> craft.

[ES] Pruebas de los ⚒️ Oficios: el catálogo (15 oficios, recetas que piden materiales de 2 oficios o más, equipo de
artesano que vale como el botín de su nivel y nunca sale al azar), el rango que sale de la experiencia de oficio, la
experiencia de oficio al recolectar y al vencer bestias (carne y piel, solo de bestias), el material raro solo desde su
rango, refinar y fabricar en una estación (gasta materiales y energía, da experiencia de héroe y de oficio, todo o
nada), el equipo y la poción fabricados que se usan, las estaciones del Claro y del campamento (🧵 Taller, 🔨 Herrería),
/oficios, los héroes viejos sin oficios, el ritmo de experiencia por ⚡ de D-108 y el tope de 4 botones.
"""

from collections import deque

from conftest import make_hero
from engine.combat import make_combat
from engine.core import FixedClock, ItemCrafted, MemoryStore, ProfessionRankUp, Rng
from engine.hero import Hero, hero_stats
from engine.hero.gear import roll_gear, starter_gear
from engine.professions import branches_of, max_times, missing_for, rank_of, rank_title, xp_for_rank
from engine.service import GameService
from test_camp_upgrades import build, camp_at, set_hero

FORMULA = {"base": 9, "exponent": 2.0}


def ids(view):
    return [a.id for a in view.actions]


def ready(service, account="test:1", **values):
    """A hero in the Claro, tutorial done (no rewards in the way), with the given fields set."""
    make_hero(service, account, "Lyra" if account == "test:1" else "Bram")
    hero = service._load(account)
    hero.tutorial = len(service.content.balance["tutorial"]["steps"])
    for key, value in values.items():
        setattr(hero, key, value)
    service._save(hero)
    return hero


def rank_xp(service, rank):
    return xp_for_rank(service.content.balance["professions"]["rank_formula"], rank)


# ---------------------------------------------------------------- catalog


def test_catalog_has_the_three_branches_and_every_recipe_is_complete(content):
    data = content.professions
    profs, recipes = data["professions"], data["recipes"]
    t = GameService(content, MemoryStore(), FixedClock(), world_seed=7).texts
    by_branch = {b: [p for p, d in profs.items() if d["branch"] == b] for b in ("gather", "refine", "craft")}
    assert set(by_branch["gather"]) == {"lenador", "minero", "herbolario", "desollador"}
    assert set(by_branch["refine"]) == {"aserradero", "fundicion", "destilacion", "tejeduria", "curtiduria"}
    assert set(by_branch["craft"]) == {"carpinteria", "herreria", "alquimia", "sastreria", "peleteria", "joyeria"}
    for pid, pdef in profs.items():
        assert pdef["emoji"] and t.has(pdef["name_key"]) and t.has(pdef["how_key"]), pid
    for rid, rdef in recipes.items():
        assert rdef["profession"] in profs and profs[rdef["profession"]]["branch"] in ("refine", "craft"), rid
        assert all(item in content.items for item in list(rdef["inputs"]) + list(rdef["output"])), rid
        assert rdef["energy"] >= 1 and rdef["xp"] >= 1 and 1 <= rdef["min_rank"] <= 100, rid
    for pid in by_branch["refine"] + by_branch["craft"]:
        ranks = sorted({r["min_rank"] for r in recipes.values() if r["profession"] == pid})
        assert ranks[0] == 1, pid                                       # everyone can start every profession
        if pid in by_branch["craft"]:
            assert ranks == [1, 25, 50], pid                            # recipes at increasing ranks
    stations = data["stations"]
    assert set(stations["claro"]) == set(by_branch["refine"] + by_branch["craft"])
    assert set(stations["camp"]) <= set(content.camp_upgrades["upgrades"])
    assert {s for group in stations["camp"].values() for s in group} == set(stations["claro"])
    assert [r["id"] for r in data["ranks"]] == ["aprendiz", "oficial", "experto", "artesano", "maestro", "gran_maestro"]
    assert not t.missing


def test_every_craft_recipe_needs_two_professions_or_more(content):
    profs, recipes = content.professions["professions"], content.professions["recipes"]
    for rid, rdef in recipes.items():
        if profs[rdef["profession"]]["branch"] == "craft":
            assert len(branches_of(rdef, profs, recipes)) >= 2, rid     # nobody is self-sufficient by design (D-109)
    assert branches_of(recipes["espada_forjada"], profs, recipes) == {"fundicion", "curtiduria"}
    assert branches_of(recipes["pocion_vida"], profs, recipes) == {"destilacion", "minero"}
    assert branches_of(recipes["anillo_engarzado"], profs, recipes) == {"fundicion", "minero"}


def test_crafted_gear_is_like_loot_of_its_level_and_better_at_high_ranks(content):
    items = content.items
    crafted = {iid: it for iid, it in items.items() if it.get("source") == "crafted"}
    outputs = {out for r in content.professions["recipes"].values() for out in r["output"]}
    assert set(crafted) <= outputs                                      # every crafted piece has a recipe
    for typ in ("espada", "daga", "arco", "baston", "tela", "cuero", "malla", "placas", "joya"):
        loot2, loot4 = items[f"{typ}_2"], items[f"{typ}_4"]
        first, best = items[f"artesano_{typ}_1"], items[f"artesano_{typ}_3"]
        assert first["stats"] == loot2["stats"] and first["req_level"] == loot2["req_level"], typ      # rank 1: like loot
        assert all(best["stats"].get(k, 0) >= v for k, v in loot4["stats"].items()), typ
        assert sum(best["stats"].values()) > sum(loot4["stats"].values()), typ                       # rank 50: a bit more
        assert best["req_level"] == loot4["req_level"], typ
    hero = Hero(id="x", name="X", class_id="guerrero", level=8)
    for seed in range(300):                                             # never in random loot
        dropped = roll_gear(items, content.classes, content.balance, hero, 8, Rng(seed), chance=1.0)
        assert dropped not in crafted
    fresh = Hero(id="y", name="Y", class_id="guerrero")
    assert not set(starter_gear(items, content.classes, content.balance, fresh)) & set(crafted)


# ---------------------------------------------------------------- ranks


def test_rank_comes_from_profession_xp_with_a_long_curve(service):
    assert xp_for_rank(FORMULA, 1) == 0 and xp_for_rank(FORMULA, 2) == 9
    assert [xp_for_rank(FORMULA, r) for r in (10, 25, 50, 100)] == [729, 5184, 21609, 88209]
    assert rank_of(0, FORMULA, 100) == 1 and rank_of(8, FORMULA, 100) == 1 and rank_of(9, FORMULA, 100) == 2
    assert rank_of(5183, FORMULA, 100) == 24 and rank_of(5184, FORMULA, 100) == 25
    assert rank_of(10**9, FORMULA, 100) == 100                          # never past the top rank
    titles = service.content.professions["ranks"]
    assert [rank_title(r, titles) for r in (1, 20, 21, 41, 61, 81, 96, 100)] == \
        ["aprendiz", "aprendiz", "oficial", "experto", "artesano", "maestro", "gran_maestro", "gran_maestro"]
    cfg = service.content.balance["professions"]
    per_day = 40 * 6                                                    # a dedicated refiner or crafter: 6 per ⚡
    assert 300 <= xp_for_rank(cfg["rank_formula"], 100) / per_day <= 420    # rank 100 in about a year (§4)


def test_rank_up_tells_what_it_opens(service):
    hero = ready(service)
    lines = service._prof_gain(hero, "minero", rank_xp(service, 10))
    assert any("rango 10" in line for line in lines) and any("Gema en bruto" in line for line in lines)
    lines = service._prof_gain(hero, "herreria", rank_xp(service, 25))
    assert any("Espada templada" in line for line in lines)
    assert service._prof_gain(hero, "herreria", 1) == []                # no new rank: no line
    events = [e for e in service.bus.history if isinstance(e, ProfessionRankUp)]
    assert {(e.profession_id, e.rank) for e in events} >= {("minero", 10), ("herreria", 25)}
    assert service._prof_gain(hero, "nada", 50) == [] and "nada" not in hero.professions


# ---------------------------------------------------------------- gathering professions


def test_gathering_gives_profession_xp_per_unit(service, clock):
    ready(service)
    service.act("test:1", "do:gather:5")                               # the Claro gives madera and fibra
    pushes = []
    for _ in range(4):
        clock.advance(3600)
        pushes += [v for acc, v in service.tick() if acc == "test:1"]
    hero = service._load("test:1")
    assert hero.professions.get("lenador", 0) == hero.backpack.get("madera", 0) > 0
    assert hero.professions.get("herbolario", 0) == hero.backpack.get("fibra", 0)
    assert "minero" not in hero.professions and "desollador" not in hero.professions
    assert any("⚒️ Oficios" in (v.notice or "") and "Leñador" in (v.notice or "") for v in pushes)
    assert not service.texts.missing


def test_rank_gives_extra_units_up_to_the_backpack_space(service):
    hero = ready(service)
    service.content.balance["professions"]["rank_yield"] = 1.0          # every rank: always one more (test only)
    got = {"madera": 3}
    hero.backpack = {"madera": 3}
    service._trade_gather(hero, got, {"until": 1, "done": 1, "log": []})
    assert got["madera"] == 6 and hero.backpack["madera"] == 6 and hero.professions["lenador"] == 6
    hero.backpack = {"piedra": service._bag_cap() - 1}
    got = {"piedra": 1}
    service._trade_gather(hero, got, {"until": 2, "done": 1, "log": []})
    assert got["piedra"] == 2 and service._bag_used(hero) == service._bag_cap()   # gathering stops at the space (D-90)


def test_rare_material_only_from_its_rank(service):
    hero = ready(service)
    cfg = service.content.balance["professions"]
    cfg["rare_chance"] = 1.0                                            # always, once the rank allows it (test only)
    hero.professions["minero"] = rank_xp(service, 10) - 30              # rank 9
    for step in range(20):
        got = {"piedra": 1}
        service._trade_gather(hero, got, {"until": step, "done": 1, "log": []})
        assert "gema_bruta" not in got and "gema_bruta" not in hero.backpack
    hero.professions["minero"] = rank_xp(service, 10)
    got = {"pieza_metal": 1, "madera": 2}
    activity = {"until": 99, "done": 1, "log": []}
    service._trade_gather(hero, got, activity)
    assert got["gema_bruta"] == 1 and hero.backpack["gema_bruta"] == 1
    assert "flor_luna" not in got                                       # the herbalist's rare needs herbs and its rank
    assert set(activity["trade"]) == {"minero", "lenador"}


# ---------------------------------------------------------------- skinning: carne and piel from beasts


def test_piel_comes_only_from_beasts(service):
    for enemy_id, edef in service.content.enemies.items():
        loot = edef.get("loot", {})
        assert ("piel" in loot) == ("carne" in loot), enemy_id         # beasts drop both; nobody else drops piel
        if "piel" in loot:
            assert 0.2 <= loot["piel"] < loot["carne"], enemy_id
    hero = ready(service)
    edef = service.content.enemies["lobo_ceniciento"]
    for seed in range(40):
        hero.backpack = {}
        state = make_combat("lobo_ceniciento", edef, 2, service._kit(hero), seed)
        state["outcome"] = "victory"
        service._end_combat(hero, state)
        if hero.backpack.get("piel"):
            break
    assert hero.backpack.get("piel", 0) >= 1
    skins = hero.backpack.get("piel", 0) + hero.backpack.get("carne", 0)
    assert hero.professions["desollador"] >= skins >= 1                 # 1 profession xp per unit skinned
    before = hero.professions["desollador"]
    bandit = service.content.enemies["bandido_errante"]
    for seed in range(30):
        hero.backpack = {}
        state = make_combat("bandido_errante", bandit, 2, service._kit(hero), seed)
        state["outcome"] = "victory"
        service._end_combat(hero, state)
        assert "piel" not in hero.backpack and "carne" not in hero.backpack
    assert hero.professions["desollador"] == before


# ---------------------------------------------------------------- refining and crafting


def test_refining_spends_inputs_and_energy_and_gives_both_xps(service):
    ready(service, backpack={"madera": 7}, energy=30)
    hero = service._load("test:1")
    xp, energy = hero.xp, hero.energy
    view = service.act("test:1", "mk:tablon:2:0")
    hero = service._load("test:1")
    assert view.kind == "recipe" and "Hiciste" in view.notice
    assert hero.backpack["madera"] == 1 and hero.backpack["tablon"] >= 2     # rank 1: 0.3 % of one more
    assert hero.energy == energy - 2
    assert hero.professions["aserradero"] == 12
    step = service.content.balance["professions"]["hero_xp_per_energy"]
    assert hero.xp == xp + 2 * step                                      # level 1 and rank 1: × 1
    assert any(isinstance(e, ItemCrafted) and e.recipe_id == "tablon" for e in service.bus.history)


def test_missing_materials_energy_station_or_rank_spend_nothing(service, clock):
    ready(service, backpack={"madera": 7, "lingote": 5, "cuero_curtido": 2}, energy=30)
    before = service._load("test:1").to_dict()

    def unchanged():
        now = service._load("test:1").to_dict()
        return all(now[k] == before[k] for k in ("backpack", "energy", "xp", "professions"))

    view = service.act("test:1", "mk:tablon:3:0")                       # 9 madera asked, 7 carried
    assert "No gastaste nada" in view.notice and unchanged()
    view = service.act("test:1", "mk:espada_templada:1:0")              # rank 25 recipe at rank 1
    assert "🔒" in view.notice and unchanged()
    set_hero(service, "test:1", energy=1)
    before["energy"] = 1
    view = service.act("test:1", "mk:espada_forjada:1:0")               # 2 ⚡ asked, 1 left
    assert "energía" in view.notice.lower() and unchanged()
    set_hero(service, "test:1", energy=30, x=3, y=0)                    # away from any station
    before["energy"] = 30
    view = service.act("test:1", "mk:tablon:1:0")
    assert "estación" in view.notice and unchanged()
    set_hero(service, "test:1", x=0, y=0, activity={"kind": "explore", "until": clock.now() + 600, "left": 0, "total": 1, "got": {}, "log": []})
    view = service.act("test:1", "mk:tablon:1:0")                       # busy exploring: one activity at a time
    assert view.notice and unchanged()
    assert service.act("test:1", "mk:nada:1:0").kind == "professions"


def test_crafted_gear_can_be_worn(service):
    ready(service, backpack={"lingote": 3, "cuero_curtido": 1}, energy=30, level=3)
    view = service.act("test:1", "mk:espada_forjada:1:0")
    hero = service._load("test:1")
    assert "Hiciste" in view.notice and hero.backpack == {"artesano_espada_1": 1}   # the starter sword is still worn
    assert "artesano_espada_1" in hero.gear_new
    attack = hero_stats(service._kit(hero), hero.level)["attack"]
    service.act("test:1", "equip:artesano_espada_1")
    hero = service._load("test:1")
    assert hero.gear["arma"] == "artesano_espada_1"
    assert hero_stats(service._kit(hero), hero.level)["attack"] > attack
    assert hero.professions["herreria"] == 12


def test_crafted_gear_goes_on_by_itself_in_an_empty_slot(service):
    ready(service, backpack={"lingote": 1, "gema_bruta": 1}, energy=30, level=3)
    view = service.act("test:1", "mk:anillo_engarzado:1:0")
    hero = service._load("test:1")
    assert hero.gear.get("joya") == "artesano_joya_1" and "te la pusiste" in view.notice.lower()


def test_crafted_potions_fill_the_belt_and_can_be_drunk(service):
    ready(service, backpack={"extracto": 2, "arcilla": 1, "flor_luna": 1}, energy=30)
    hero = service._load("test:1")
    hero.professions["alquimia"] = rank_xp(service, 25)
    service._save(hero)
    view = service.act("test:1", "mk:pocion_mayor:1:0")
    hero = service._load("test:1")
    assert "Hiciste" in view.notice and hero.belt.get("pocion_mayor") == 1     # belt slot (balance.yaml hero.belt_slots)
    max_hp = hero_stats(service._kit(hero), hero.level)["max_hp"]
    set_hero(service, "test:1", hp=1)
    service.act("test:1", "use:pocion_mayor")
    hero = service._load("test:1")
    assert hero.hp == 1 + round(max_hp * 0.6) and "pocion_mayor" not in hero.belt
    set_hero(service, "test:1", backpack={"extracto": 1, "arcilla": 1})
    service.act("test:1", "mk:pocion_vida:1:0")                         # rank 1: 2 potions of life
    hero = service._load("test:1")
    assert hero.belt.get("pocion_vida", 0) + hero.backpack.get("pocion_vida", 0) >= 4


def test_make_buttons_follow_what_you_carry(service):
    ready(service, backpack={"madera": 30}, energy=8)
    view = service.act("test:1", "rec:tablon:0")
    assert view.kind == "recipe" and ids(view) == ["mk:tablon:1:0", "mk:tablon:5:0", "mk:tablon:8:0", "est:refine:0"]
    assert any("✅" in line and "Madera" in line for line in view.body)
    rdef = service.content.professions["recipes"]["tablon"]
    assert max_times(rdef, {"madera": 30}, 8) == 8 and max_times(rdef, {"madera": 2}, 8) == 0
    assert missing_for(rdef, {"madera": 2}) == {"madera": 1} and missing_for(rdef, {"madera": 6}, 2) == {}
    set_hero(service, "test:1", backpack={"madera": 2})
    view = service.act("test:1", "rec:tablon:0")
    assert ids(view) == ["est:refine:0"] and any("❌" in line for line in view.body)


# ---------------------------------------------------------------- stations, screens and the command


def test_oficios_command_and_screen(service):
    ready(service)
    assert service.commands()["/oficios"] == "oficios"
    view = service.act("test:1", "claro")
    assert ids(view) == ["shop", "inn", "oficios", "home"]
    view = service.act("test:1", "oficios")
    assert view.kind == "professions" and ids(view) == ["est:refine:0", "est:craft:0", "claro"]
    assert any("Todavía no empezaste" in line for line in view.body)
    assert any("Sin empezar" in line and "Joyería" in line for line in view.body)
    hero = service._load("test:1")
    hero.professions = {"minero": 40, "herreria": rank_xp(service, 25) + 5}
    service._save(hero)
    view = service.act("test:1", "oficios")
    body = "\n".join(view.body)
    assert "Minero · rango 3 (Aprendiz)" in body and "Herrería · rango 25 (Oficial)" in body
    assert "En rango 10: 💠 Gema en bruto" in body and "En rango 50" in body
    set_hero(service, "test:1", x=4, y=0)
    view = service.act("test:1", "oficios")                            # anywhere: ranks yes, stations no
    assert ids(view) == ["hero"] and any("🧵 Taller" in line for line in view.body)
    assert any("/oficios" in line for line in service.act("test:1", "hero").body)
    assert not service.texts.missing


def test_station_lists_what_you_can_make_first_two_per_page(service):
    ready(service, backpack={"lingote": 2, "cuero_curtido": 1, "tablon": 1}, energy=30)
    view = service.act("test:1", "est:craft:0")
    assert view.kind == "station" and len(view.actions) == 4
    assert view.actions[0].id == "rec:daga_forjada:0" and view.actions[0].label.startswith("✅")
    # then those you carry part of, in file order (Carpintería comes first): the staff, with what is missing
    assert view.actions[1].id == "rec:baston_roble:0" and not view.actions[1].label.startswith("✅")
    assert view.actions[2].id == "est:craft:1" and view.actions[3].id == "oficios"
    assert any("Falta" in line and "Tablón ×2" in line and "Tela ×1" in line for line in view.body)
    assert any("Página 1 de 6" in line for line in view.body)          # 11 rank-1 crafting recipes in the Claro
    refine = service.act("test:1", "est:refine:0")
    assert refine.kind == "station" and len(refine.actions) == 4      # 5 refining recipes: 2 per page
    assert any("Página 1 de 3" in line for line in refine.body)
    seen = set()
    for page in range(3):
        seen |= {a.id for a in service.act("test:1", f"est:refine:{page}").actions if a.id.startswith("rec:")}
    assert seen == {"rec:tablon:0", "rec:lingote:0", "rec:extracto:1", "rec:tela:1", "rec:cuero:2"}
    set_hero(service, "test:1", x=3, y=0)
    assert service.act("test:1", "est:craft:0").kind == "professions"   # no station here


def test_camp_stations_come_with_the_taller_and_the_herreria(service):
    make_hero(service, "test:1", "Lyra")
    camp_at(service, 6)
    set_hero(service, "test:1", backpack={"madera": 3, "pieza_metal": 2}, energy=30)
    assert service._stations_here(service._load("test:1")) == ([], None)
    assert service.act("test:1", "mk:tablon:1:0").notice and service._load("test:1").backpack["madera"] == 3
    build(service, "taller")
    view = service.act("test:1", "ctaller")
    assert "oficios" in ids(view)
    view = service.act("test:1", "oficios")
    assert ids(view) == ["est:refine:0", "est:craft:0", "ctaller"]
    assert any("Estaciones de tu campamento" in line for line in view.body)
    refine = service.act("test:1", "est:refine:0")
    listed = {a.id.split(":")[1] for p in range(2) for a in service.act("test:1", f"est:refine:{p}").actions if a.id.startswith("rec:")}
    assert "lingote" not in listed and "tablon" in listed               # no Herrería yet: no foundry here
    assert any("Claro" in line for line in refine.body)
    recipe = service.act("test:1", "rec:tablon:0")
    assert any("⭐ 10 %" in line for line in recipe.body)               # camp bonus (balance.yaml professions.camp_bonus)
    service.act("test:1", "mk:tablon:1:0")
    hero = service._load("test:1")
    assert hero.backpack.get("tablon", 0) >= 1 and "madera" not in hero.backpack
    assert "estación" in service.act("test:1", "mk:lingote:1:0").notice
    assert service._load("test:1").backpack["pieza_metal"] == 2          # the foundry is not here: nothing spent
    build(service, "herreria")
    service.act("test:1", "mk:lingote:1:0")
    assert service._load("test:1").backpack.get("lingote", 0) >= 1


def test_herreria_without_taller_opens_its_stations_from_the_services(service):
    make_hero(service, "test:1", "Lyra")
    camp_at(service, 6)
    build(service, "herreria")
    view = service.act("test:1", "upsvc")
    assert view.kind == "camp_services" and "oficios" in ids(view) and len(view.actions) <= 4
    stations, where = service._stations_here(service._load("test:1"))
    assert set(stations) == {"fundicion", "herreria", "joyeria"} and where == "camp"
    assert ids(service.act("test:1", "oficios"))[-1] == "upsvc"


def test_old_heroes_without_professions_load(service):
    make_hero(service)
    data = service.store.get("hero", "test:1")
    data.pop("professions", None)
    service.store.put("hero", "test:1", data)
    hero = service._load("test:1")
    assert hero.professions == {} and service._prof_rank(hero, "herreria") == 1
    assert service.act("test:1", "oficios").kind == "professions"
    assert Hero.from_dict({"id": "a", "name": "A", "class_id": "guerrero"}).professions == {}


# ---------------------------------------------------------------- D-108: experience per energy


def test_crafting_xp_per_energy_keeps_pace_with_gathering(service):
    hero = ready(service)
    recipes = service.content.professions["recipes"]
    gather = service.content.balance["gather"]["xp_per_step"]
    for level in (1, 10, 30, 60, 100):
        hero.level = level
        for rid in ("tablon", "espada_forjada", "pocion_vida"):
            rdef = recipes[rid]
            per_energy = service._make_xp(hero, rdef, 100) / rdef["energy"]
            zone = service._zone_xp(gather, level)                     # gathering in a zone of your level, per ⚡
            assert zone <= per_energy <= 1.5 * zone, (level, rid)       # like gathering with its fights (~1.45×)
    hero.level = 60
    novice = service._make_xp(hero, recipes["tablon"], 1)               # a novice crafter learns little
    assert novice == service.content.balance["professions"]["hero_xp_per_energy"]


# ---------------------------------------------------------------- 4 buttons and texts


def test_every_profession_screen_keeps_four_buttons_and_its_texts(content):
    def make(path):
        service = GameService(content, MemoryStore(), FixedClock(), world_seed=7)
        make_hero(service, "test:1", "Lyra", "paladin_reprension")
        hero = service._load("test:1")
        hero.level, hero.energy = 9, 50
        hero.professions = {pid: rank_xp(service, 50) for pid in content.professions["professions"]}
        hero.backpack = {item: 12 for item in ("madera", "pieza_metal", "hierba_curativa", "fibra", "piel", "arcilla", "tablon",
                                               "lingote", "extracto", "tela_tejida", "cuero_curtido", "gema_bruta", "flor_luna")}
        service._save(hero)
        view = service.act("test:1", "oficios")
        for action in path:
            view = service.act("test:1", action)
        return service, view

    seen, queue, kinds = set(), deque([[]]), set()
    while queue and len(seen) < 160:
        path = queue.popleft()
        service, view = make(path)
        assert len(view.actions) <= 4, (path, view.kind, ids(view))
        assert not service.texts.missing, (path, service.texts.missing)
        kinds.add(view.kind)
        key = (view.kind, tuple(ids(view)))
        if key in seen or len(path) >= 3:
            continue
        seen.add(key)
        for action_id in ids(view):
            if action_id.startswith(("oficios", "est:", "rec:", "mk:")):
                queue.append(path + [action_id])
    assert {"professions", "station", "recipe"} <= kinds


def test_sell_all_keeps_refined_goods_and_rares(service):
    # D-109: 💱 Vender todo only sells raw materials; refined goods and rares are a profession's work (sold one by one).
    from conftest import make_hero as _make
    _make(service)
    hero = service._load("test:1")
    hero.backpack.update({"madera": 3, "tablon": 2, "gema_bruta": 1, "carne": 1})
    hero.gold = 0
    service._save(hero)
    service.act("test:1", "shop")
    service.act("test:1", "sell:all")
    hero = service._load("test:1")
    assert "madera" not in hero.backpack and hero.backpack["tablon"] == 2 and hero.backpack["gema_bruta"] == 1
    assert hero.backpack["carne"] == 1 and hero.gold > 0
