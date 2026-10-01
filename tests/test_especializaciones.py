"""🎓 Profession specializations (D-115, D-141): one at rank 25, another at 75, never the three.

[ES] Pruebas de las especializaciones de oficio (red-de-oficios.md §3): cada oficio tiene 3 con textos y efectos que el motor
entiende; antes del rango 25 no se elige, al 25 se elige una gratis, al 75 una segunda distinta, nunca una tercera; el efecto
crece con el dominio y vale solo en su línea (recolectar, refinar, fabricar, obra maestra, curar, vender, encantar, infiltrarse);
las recetas exclusivas solo las ve y las hace su especialización (con 25 % de dominio); cambiar cuesta las monedas de
balance.yaml specs.switch_cost, saca la vieja (y su receta) y guarda su dominio; los héroes viejos cargan; las pantallas tienen
4 botones como mucho y no falta ningún texto.
"""

from collections import deque

import pytest

from conftest import make_hero
from engine.core import FixedClock, MemoryStore
from engine.hero import Hero
from engine.professions import branches_of, masterwork_id, xp_for_rank
from engine.professions import rules as profession_rules
from engine.professions.rules import PERK_KEYS, SPEC_FILTERS, SPEC_KINDS
from engine.service import GameService


def ids(view):
    return [a.id for a in view.actions]


def ready(service, account="test:1", **values):
    """A hero in the Claro, tutorial done, with the given fields set."""
    make_hero(service, account, "Lyra" if account == "test:1" else "Bram")
    hero = service._load(account)
    hero.tutorial = len(service.content.balance["tutorial"]["steps"])
    for key, value in values.items():
        setattr(hero, key, value)
    service._save(hero)
    return hero


def rank_xp(service, rank):
    return xp_for_rank(service.content.balance["professions"]["rank_formula"], rank)


def full(service):
    return service.content.balance["specs"]["mastery_xp"]


def with_ranks(service, ranks, account="test:1", **values):
    hero = service._load(account)
    hero.professions = {pid: rank_xp(service, rank) for pid, rank in ranks.items()}
    for key, value in values.items():
        setattr(hero, key, value)
    service._save(hero)
    return hero


# ---------------------------------------------------------------- the catalog


def test_every_profession_has_three_specializations_with_texts_and_known_effects(content):
    specs = content.professions["specs"]
    profs = content.professions["professions"]
    recipes = content.professions["recipes"]
    t = GameService(content, MemoryStore(), FixedClock(), world_seed=7).texts
    assert set(specs) == set(profs)                                         # every profession in the game has its three
    seen = set()
    for pid, rows in specs.items():
        assert len(rows) == 3, pid
        for sdef in rows:
            sid = sdef["id"]
            assert sid not in seen and sid.startswith(pid + "_"), sid       # stable, unique in the whole game
            seen.add(sid)
            assert sdef["emoji"] and t.has(f"spec.{sid}.name") and t.has(f"spec.{sid}.desc"), sid
            assert sdef["effects"], sid
            for effect in sdef["effects"]:
                assert effect["kind"] in SPEC_KINDS and effect["value"] > 0, sid
                assert set(effect) <= {"kind", "key", "value"} | set(SPEC_FILTERS), sid
                if effect["kind"] == "perk":
                    assert effect["key"] in PERK_KEYS, sid
                for item in effect.get("items", []):
                    assert item in content.items, (sid, item)
                for typ in effect.get("types", []):
                    assert t.has(f"gear.type.{typ}"), (sid, typ)
                for sale in effect.get("sales", []):
                    assert t.has(f"spec.sale.{sale}"), (sid, sale)
                for eid in effect.get("enchants", []):
                    assert eid in content.balance["enchanting"]["enchants"], (sid, eid)
    for rows in specs.values():                                             # Telegram: a button id fits in 64 bytes
        for a in rows:
            for b in rows:
                assert len(f"pspx!:{a['id']}:{b['id']}".encode()) <= 64, (a["id"], b["id"])
    exclusive = {rid: r for rid, r in recipes.items() if r.get("spec")}
    assert len(exclusive) == 18                                             # 16 gear pieces and 2 camp furniture pieces
    for rid, rdef in exclusive.items():
        owner = profession_rules.spec_owner(specs, rdef["spec"])[0]
        assert owner == rdef["profession"], rid                             # a specialization of the profession that makes it
        assert len(branches_of(rdef, profs, recipes)) >= 2, rid             # nobody is self-sufficient (D-109)
    assert not t.missing


def test_exclusive_pieces_beat_the_crafted_piece_of_their_level_and_never_make_coins(content):
    recipes = content.professions["recipes"]
    ratio = content.balance["shop"]["sell_ratio"]
    for rid, rdef in recipes.items():
        out = next(iter(rdef["output"]))
        item = content.items[out]
        if not rdef.get("spec") or item.get("kind") != "gear":
            continue
        tier = 2 if item["req_level"] == 5 else 13
        base = content.items[f"artesano_{item['type']}_{tier}"]
        assert item["slot"] == base["slot"] and item["req_level"] == base["req_level"] and item["source"] == "crafted", out
        assert all(item["stats"].get(k, 0) >= v for k, v in base["stats"].items()), out
        assert sum(item["stats"].values()) > sum(base["stats"].values()), out        # better in its line
        assert rdef["min_rank"] == (25 if tier == 2 else 100) and rdef["energy"] == 2 and rdef["xp"] == 12, out
        materials = sum(content.items[m]["price"] * n for m, n in rdef["inputs"].items())
        assert item["price"] * ratio < materials, out                               # crafting never makes coins (D-113)
        assert masterwork_id(out) in content.items, out                             # its ✒️ twin, made at load


def test_rules_slots_choice_mastery_and_cost(content):
    specs = content.professions["specs"]
    cfg = content.balance["specs"]
    slots_at = cfg["slots_at"]
    assert [profession_rules.spec_slots(r, slots_at) for r in (1, 24, 25, 74, 75, 100)] == [0, 0, 1, 1, 2, 2]
    held = {}
    assert profession_rules.spec_choice(specs, held, "minero", "minero_gemas", 24, slots_at) == "locked"
    assert profession_rules.spec_choice(specs, held, "minero", "minero_gemas", 25, slots_at) == "pick"
    held = {"minero": ["minero_gemas"]}
    assert profession_rules.spec_choice(specs, held, "minero", "minero_gemas", 30, slots_at) == "held"
    assert profession_rules.spec_choice(specs, held, "minero", "minero_metales", 30, slots_at) == "switch"
    assert profession_rules.spec_choice(specs, held, "minero", "minero_metales", 75, slots_at) == "pick"
    held = {"minero": ["minero_gemas", "minero_metales"]}
    assert profession_rules.spec_choice(specs, held, "minero", "minero_cantera", 100, slots_at) == "switch"   # never three
    assert profession_rules.spec_choice(specs, held, "minero", "herreria_armero", 100, slots_at) == "locked"  # not this profession
    assert profession_rules.spec_share(0, cfg["mastery_xp"]) == 0
    assert profession_rules.spec_share(cfg["mastery_xp"] // 2, cfg["mastery_xp"]) == pytest.approx(0.5)
    assert profession_rules.spec_share(cfg["mastery_xp"] * 3, cfg["mastery_xp"]) == 1.0
    cost = cfg["switch_cost"]
    assert profession_rules.switch_cost(25, cost) == cost["base"] + 25 * cost["per_rank"]
    assert profession_rules.switch_cost(100, cost) > profession_rules.switch_cost(25, cost)          # P-105: grows with the rank


# ---------------------------------------------------------------- choosing


def test_cannot_pick_before_rank_25_and_the_first_is_free_at_25(service):
    ready(service, gold=0)
    with_ranks(service, {"minero": 24})
    view = service.act("test:1", "pspv:minero_gemas")
    assert view.kind == "spec" and "pspp:minero_gemas" not in ids(view) and any("🔒" in line for line in view.body)
    view = service.act("test:1", "pspp:minero_gemas")
    assert "🔒" in view.notice and service._load("test:1").prof_specs == {}
    with_ranks(service, {"minero": 25}, gold=0)
    view = service.act("test:1", "pspv:minero_gemas")
    assert "pspp:minero_gemas" in ids(view)
    view = service.act("test:1", "pspp:minero_gemas")
    hero = service._load("test:1")
    assert view.kind == "prof_specs" and "Elegiste" in view.notice
    assert hero.prof_specs == {"minero": ["minero_gemas"]} and hero.gold == 0                        # free
    view = service.act("test:1", "pspv:minero_metales")                     # one slot until rank 75: only switching
    assert "pspp:minero_metales" not in ids(view) and any(i.startswith("pspx:minero_metales:") for i in ids(view))
    assert "lleno" in service.act("test:1", "pspp:minero_metales").notice
    assert service._load("test:1").prof_specs == {"minero": ["minero_gemas"]}


def test_second_at_75_must_differ_and_never_a_third(service):
    ready(service)
    with_ranks(service, {"herreria": 75})
    service.act("test:1", "pspp:herreria_armero")
    assert "Ya tienes" in service.act("test:1", "pspp:herreria_armero").notice                       # the same one twice: no
    service.act("test:1", "pspp:herreria_armas")
    assert service._load("test:1").prof_specs == {"herreria": ["herreria_armero", "herreria_armas"]}
    view = service.act("test:1", "pspv:herreria_herramientas")
    assert "pspp:herreria_herramientas" not in ids(view)                    # never the three
    assert service.act("test:1", "pspp:herreria_herramientas").notice
    assert service._load("test:1").prof_specs["herreria"] == ["herreria_armero", "herreria_armas"]
    assert len(view.actions) <= 4 and [i for i in ids(view) if i.startswith("pspx:")] == [
        "pspx:herreria_herramientas:herreria_armero", "pspx:herreria_herramientas:herreria_armas"]


def test_switching_costs_coins_removes_the_old_one_and_keeps_its_mastery(service):
    ready(service, gold=0)
    with_ranks(service, {"herreria": 40})
    service.act("test:1", "pspp:herreria_armero")
    hero = service._load("test:1")
    hero.spec_xp["herreria_armero"] = 3000
    hero.backpack = {"lingote": 20, "cuero_curtido": 10}
    service._save(hero)
    cost = profession_rules.switch_cost(40, service.content.balance["specs"]["switch_cost"])
    view = service.act("test:1", "pspx:herreria_armas:herreria_armero")    # asks first
    assert view.kind == "spec_switch" and ids(view)[0] == "pspx!:herreria_armas:herreria_armero" and len(view.actions) <= 4
    view = service.act("test:1", "pspx!:herreria_armas:herreria_armero")   # no coins: nothing changes
    hero = service._load("test:1")
    assert "Te faltan monedas" in view.notice and hero.prof_specs == {"herreria": ["herreria_armero"]} and hero.gold == 0
    hero.gold = cost + 7
    service._save(hero)
    view = service.act("test:1", "pspx!:herreria_armas:herreria_armero")
    hero = service._load("test:1")
    assert view.kind == "prof_specs" and "Dejaste" in view.notice
    assert hero.prof_specs == {"herreria": ["herreria_armas"]} and hero.gold == 7
    assert hero.spec_xp["herreria_armero"] == 3000 and hero.spec_xp.get("herreria_armas", 0) == 0     # memory kept, new from zero
    assert any("💾" in line and "Armero" in line for line in view.body)
    view = service.act("test:1", "mk:espec_placas_1:1:0")                   # the old one's exclusive recipe is closed again
    assert "🔒" in view.notice and service._load("test:1").backpack == {"lingote": 20, "cuero_curtido": 10}
    hero = service._load("test:1")
    hero.gold = cost
    service._save(hero)
    service.act("test:1", "pspx!:herreria_armero:herreria_armas")          # coming back resumes the saved mastery
    hero = service._load("test:1")
    assert hero.prof_specs == {"herreria": ["herreria_armero"]} and service._pspec_share(hero, "herreria_armero") == pytest.approx(3000 / full(service))


def test_mastery_grows_with_profession_xp_and_tells_what_opens(service):
    ready(service, backpack={"lingote": 200, "cuero_curtido": 100}, energy=500, level=5)
    hero = with_ranks(service, {"herreria": 24})
    hero.professions["herreria"] = rank_xp(service, 25) - 6
    service._save(hero)
    view = service.act("test:1", "mk:espada_forjada:1:0")                  # crossing rank 25 tells you can choose
    assert "Ya puedes elegir especialización" in view.notice and "🔨 Herrería" in view.notice
    service.act("test:1", "pspp:herreria_armas")
    need = int(full(service) * service.content.balance["specs"]["recipe_mastery"])
    hero = service._load("test:1")
    hero.spec_xp["herreria_armas"] = need - 12
    service._save(hero)
    assert "rec:espec_espada_1:0" not in str(ids(service.act("test:1", "est:craft:0")))
    view = service.act("test:1", "mk:espada_forjada:1:0")                  # +12 profession xp → 25 % mastery
    hero = service._load("test:1")
    assert hero.spec_xp["herreria_armas"] == need
    assert "Nueva receta exclusiva" in view.notice and "Hoja de forjador" in view.notice
    hero.professions["herreria"] = rank_xp(service, 75) - 6
    service._save(hero)
    view = service.act("test:1", "mk:espada_forjada:1:0")
    assert "segunda especialización" in view.notice
    hero = service._load("test:1")
    hero.spec_xp["herreria_armas"] = full(service) - 12
    service._save(hero)
    assert "Dominas" in service.act("test:1", "mk:espada_forjada:1:0").notice


# ---------------------------------------------------------------- effects, only in their line


def test_gathering_yield_applies_only_to_its_items_and_grows_with_mastery(service):
    hero = ready(service)
    hero = with_ranks(service, {"minero": 25}, prof_specs={"minero": ["minero_metales"]}, spec_xp={"minero_metales": 0})
    assert service._pspec_bonus(hero, "yield", item="pieza_metal") == 0                           # 0 % mastery: nothing yet
    hero.spec_xp["minero_metales"] = full(service) // 2
    assert service._pspec_bonus(hero, "yield", item="pieza_metal") == pytest.approx(0.10)
    hero.spec_xp["minero_metales"] = full(service)
    assert service._pspec_bonus(hero, "yield", item="pieza_metal") == pytest.approx(0.20)
    assert service._pspec_bonus(hero, "yield", item="piedra") == 0                                # only its own line
    service._save(hero)
    hero = service._load("test:1")
    got = {"pieza_metal": 100, "piedra": 100}
    service._trade_gather(hero, got, {"until": 1, "done": 1})
    metal_extra, stone_extra = got["pieza_metal"] - 100, got["piedra"] - 100
    assert metal_extra > stone_extra + 8                                    # 27.5 % against 7.5 %


def test_find_effect_brings_gems_while_mining(service):
    ready(service)
    hero = with_ranks(service, {"minero": 25}, prof_specs={"minero": ["minero_gemas"]}, spec_xp={"minero_gemas": 10 ** 6})
    plain = Hero(id="x", name="X", class_id="guerrero", professions=dict(hero.professions))
    with_spec = without = 0
    for done in range(200):
        got = {"piedra": 1}
        service._trade_gather(hero, got, {"until": 5, "done": done})
        with_spec += got.get("gema_bruta", 0)
        hero.backpack = {}
        got = {"piedra": 1}
        service._trade_gather(plain, got, {"until": 5, "done": done})
        without += got.get("gema_bruta", 0)
        plain.backpack = {}
    assert with_spec >= without + 6                                         # +8 % per round, on top of the usual rare


def test_refining_yield_applies_only_to_its_output(service):
    ready(service, energy=1000, backpack={"pieza_metal": 400, "madera": 600})
    hero = with_ranks(service, {"fundicion": 25, "aserradero": 25}, prof_specs={"fundicion": ["fundicion_hierro"]},
                      spec_xp={"fundicion_hierro": full(service)})
    lingote = service.act("test:1", "rec:lingote:0")
    tablon = service.act("test:1", "rec:tablon:0")
    assert any("22 %" in line or "23 %" in line for line in lingote.body)  # 7.5 % of the rank + 15 % of 🔩 Hierro
    assert any("8 %" in line or "7 %" in line for line in tablon.body)     # the sawmill: only its rank
    service.act("test:1", "mk:lingote:200:0")
    service.act("test:1", "mk:tablon:200:0")
    hero = service._load("test:1")
    assert hero.backpack["lingote"] - 200 > hero.backpack["tablon"] - 200 + 15


def test_crafting_masterwork_effect_only_in_its_line(service):
    ready(service)
    hero = with_ranks(service, {"herreria": 50}, prof_specs={"herreria": ["herreria_armero"]},
                      spec_xp={"herreria_armero": full(service)})
    items = service.content.items
    assert service._pspec_masterwork(hero, items["artesano_placas_3"]) == pytest.approx(0.05)
    assert service._pspec_masterwork(hero, items["artesano_cabeza_placas_3"]) == pytest.approx(0.05)
    assert service._pspec_masterwork(hero, items["artesano_espada_3"]) == 0                       # not swords
    view = service.act("test:1", "rec:coraza_artesano:0")
    assert any("7.5 %" in line and "obra maestra" in line for line in view.body)                   # 2.5 % rank + 5 % spec
    view = service.act("test:1", "rec:espada_artesano:0")
    assert any("2.5 %" in line and "obra maestra" in line for line in view.body)


def test_remedy_specializations_heal_more_or_make_more(service):
    ready(service, energy=500, backpack={"extracto": 120, "arcilla": 120})
    hero = with_ranks(service, {"medicina": 25, "alquimia": 25},
                      prof_specs={"medicina": ["medicina_auxilios"], "alquimia": ["alquimia_pociones"]},
                      spec_xp={"medicina_auxilios": full(service), "alquimia_pociones": full(service)})
    base = profession_rules.perks(service.content.professions["professions"], {"medicina": 25, "alquimia": 25}, 100,
                                  "placas", "espada", "defensa")
    perks = service._perks(hero)
    assert perks["bandage"] == pytest.approx(base["bandage"] + 0.15)       # 🩹 Primeros auxilios
    assert perks["potion"] == pytest.approx(base["potion"])                # no 🍷 Elixires: potions stay
    assert perks["heal"] == 0                                              # 🩺 not a healer, no surgery
    service.act("test:1", "mk:pocion_vida:100:0")
    hero = service._load("test:1")
    made = hero.backpack.get("pocion_vida", 0) + hero.belt.get("pocion_vida", 0) - 2   # 2 from the starting backpack
    assert made > 200 + 10                                                 # 🧪 Pociones: +20 % of making one more
    healer = Hero(id="h", name="H", class_id="sacerdote_sagrado", professions={"medicina": rank_xp(service, 25)},
                  prof_specs={"medicina": ["medicina_cirugia"]}, spec_xp={"medicina_cirugia": full(service)})
    tank = Hero(id="t", name="T", class_id="guerrero", professions={"medicina": rank_xp(service, 25)},
                prof_specs={"medicina": ["medicina_cirugia"]}, spec_xp={"medicina_cirugia": full(service)})
    assert service._perks(healer)["heal"] > service._perks(tank)["heal"] == 0                       # 🩺 Cirugía: healers only


def test_trade_enchant_and_explorer_specializations(service):
    ready(service, backpack={"madera": 10}, gold=0)
    hero = with_ranks(service, {"comercio": 25}, prof_specs={"comercio": ["comercio_tratante"]},
                      spec_xp={"comercio_tratante": full(service)})
    service.act("test:1", "sell:all")
    plain = service._load("test:1").gold
    hero = service._load("test:1")
    hero.prof_specs = {"comercio": ["comercio_abastecedor"]}
    hero.spec_xp["comercio_abastecedor"] = full(service)
    hero.backpack, hero.gold = {"madera": 10}, 0
    service._save(hero)
    service.act("test:1", "sell:all")
    assert service._load("test:1").gold > plain                            # 📦 Abastecedor: goods; 🛡️ Tratante: only gear
    edef = service.content.balance["enchanting"]["enchants"]["filo"]
    hero = Hero(id="e", name="E", class_id="guerrero", professions={"encantamiento": rank_xp(service, 25)},
                prof_specs={"encantamiento": ["encantamiento_armas"]}, spec_xp={"encantamiento_armas": full(service)})
    assert profession_rules.enchant_value(edef, 25, 100, service._pspec_bonus(hero, "enchant", enchant="filo")) == 0.02
    assert profession_rules.enchant_value(edef, 25, 100) == 0.01
    assert service._pspec_bonus(hero, "enchant", enchant="vigor") == 0      # ⚔️ Armas: only ⚔️ Filo
    scout = Hero(id="s", name="S", class_id="guerrero", professions={"explorador": rank_xp(service, 30)},
                 prof_specs={"explorador": ["explorador_infiltrado", "explorador_cartografo"]},
                 spec_xp={"explorador_infiltrado": full(service), "explorador_cartografo": full(service)})
    assert service._pspec_bonus(scout, "detect") == pytest.approx(0.10)
    assert int(service._perks(scout)["explore"]) == int(service._perks(Hero(id="z", name="Z", class_id="guerrero",
                                                                             professions=dict(scout.professions)))["explore"]) + 3


# ---------------------------------------------------------------- exclusive recipes


def test_exclusive_recipe_only_for_its_specialization(service):
    ready(service, backpack={"lingote": 40, "cuero_curtido": 20}, energy=100, level=5)
    with_ranks(service, {"herreria": 30})
    stations = [service.act("test:1", f"est:craft:{page}") for page in range(30)]
    assert not any("espec_placas_1" in i for v in stations for i in ids(v))  # hidden for the others
    view = service.act("test:1", "rec:espec_placas_1:0")
    assert any("Solo la hace" in line for line in view.body) and not any(i.startswith("mk:") for i in ids(view))
    view = service.act("test:1", "mk:espec_placas_1:1:0")
    assert "🔒" in view.notice and service._load("test:1").backpack == {"lingote": 40, "cuero_curtido": 20}   # nothing spent
    service.act("test:1", "pspp:herreria_armero")
    view = service.act("test:1", "rec:espec_placas_1:0")                    # held, but 0 % mastery: still closed
    assert any("dominio" in line and "🔒" in line for line in view.body)
    hero = service._load("test:1")
    hero.spec_xp["herreria_armero"] = int(full(service) * service.content.balance["specs"]["recipe_mastery"])
    service._save(hero)
    view = service.act("test:1", "rec:espec_placas_1:0")
    assert "mk:espec_placas_1:1:0" in ids(view) and any("Receta exclusiva" in line for line in view.body)
    service.act("test:1", "mk:espec_placas_1:1:0")
    hero = service._load("test:1")
    assert hero.gear.get("armadura") in ("espec_placas_1", masterwork_id("espec_placas_1")) or \
        hero.backpack.get("espec_placas_1", 0) + hero.backpack.get(masterwork_id("espec_placas_1"), 0) == 1
    assert "🔒" in service.act("test:1", "mk:espec_espada_1:1:0").notice  # the sword is the 🗡️ Forjador's


# ---------------------------------------------------------------- old saves and screens


def test_old_heroes_without_specializations_load(service):
    make_hero(service)
    data = service.store.get("hero", "test:1")
    data.pop("prof_specs", None)
    data.pop("spec_xp", None)
    data["professions"] = {"minero": rank_xp(service, 30)}
    service.store.put("hero", "test:1", data)
    hero = service._load("test:1")
    assert hero.prof_specs == {} and hero.spec_xp == {}
    view = service.act("test:1", "oficios")
    assert "pspecs" in ids(view) and any("Puedes elegir especialización" in line for line in view.body)
    assert service.act("test:1", "pspecs").kind == "specs"
    assert service.commands()["/especialidad"] == "pspecs"
    assert not service.texts.missing


def test_the_hub_pages_many_professions_within_four_buttons(service):
    ready(service)
    with_ranks(service, {pid: 60 for pid in service.content.professions["professions"]})
    view = service.act("test:1", "pspecs")
    pages = 0
    seen = set()
    while view.kind == "specs" and pages < 20:
        assert len(view.actions) == 4 and ids(view)[-2].startswith("pspecs:") and ids(view)[-1] == "oficios"
        seen |= {i for i in ids(view) if i.startswith("pspec:")}
        view = service.act("test:1", ids(view)[-2])
        pages += 1
        if ids(view)[-2] == "pspecs:0":
            seen |= {i for i in ids(view) if i.startswith("pspec:")}
            break
    assert seen == {f"pspec:{pid}" for pid in service.content.professions["specs"]}        # every profession is reachable


def test_every_specialization_screen_keeps_four_buttons_and_its_texts(content):
    def make(path):
        service = GameService(content, MemoryStore(), FixedClock(), world_seed=7)
        make_hero(service, "test:1", "Lyra", "paladin_reprension")
        hero = service._load("test:1")
        hero.level, hero.energy, hero.gold = 9, 50, 100000
        hero.professions = {pid: rank_xp(service, 80 if pid in ("herreria", "carpinteria", "minero") else 20)
                            for pid in content.professions["professions"]}
        hero.prof_specs = {"herreria": ["herreria_armero"], "carpinteria": ["carpinteria_escudos", "carpinteria_arqueria"]}
        hero.spec_xp = {"herreria_armero": 5000, "minero_gemas": 900}
        service._save(hero)
        view = service.act("test:1", "oficios")
        for action in path:
            view = service.act("test:1", action)
        return service, view

    seen, queue, kinds = set(), deque([[]]), set()
    while queue and len(seen) < 120:
        path = queue.popleft()
        service, view = make(path)
        assert len(view.actions) <= 4, (path, view.kind, ids(view))
        assert not service.texts.missing, (path, service.texts.missing)
        kinds.add(view.kind)
        key = (view.kind, tuple(ids(view)))
        if key in seen or len(path) >= 4:
            continue
        seen.add(key)
        for action_id in ids(view):
            if action_id.startswith(("pspecs", "pspec:", "pspv:", "pspp:", "pspx")):
                queue.append(path + [action_id])
    assert {"professions", "specs", "prof_specs", "spec", "spec_switch"} <= kinds
