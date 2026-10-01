"""Masterworks and camp furniture (D-116, confirmed): profession benefits that are not only for combat.

[ES] Pruebas de la ✒️ obra maestra y los 🪑 muebles del campamento: cada pieza de artesano tiene su gemela obra maestra
(mejor en todo, con un bono más, más cara y nunca en el botín al azar); la probabilidad crece con el rango y es mayor
en la 🪑 Carpintería (hasta 15 %) que en los demás oficios que hacen equipo (hasta 5 %); la pieza sale firmada con el
nombre de quien la hizo y la firma se ve en 🔁 Equipar y en la pieza; la Carpintería ya no da ataque; los héroes viejos
cargan; venderla paga más; los muebles solo los hace la Carpintería, se colocan una vez por campamento y dan su bono;
todas las pantallas con 4 botones como mucho y sin textos que falten.
"""

import pytest

from conftest import make_hero
from engine.core import Rng
from engine.hero import Hero, hero_stats
from engine.hero.gear import roll_gear, starter_gear
from engine.professions import masterwork_chance, masterwork_id, xp_for_rank
from engine.professions import rules as profession_rules
from test_camp_upgrades import KEY, camp_at, set_hero


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


def crafted(content):
    return {iid: it for iid, it in content.items.items() if it.get("kind") == "gear" and it.get("source") == "crafted"}


# ---------------------------------------------------------------- the masterwork pieces


def test_every_crafted_piece_has_a_better_masterwork_twin_that_never_drops(content):
    cfg = content.balance["masterwork"]
    made = crafted(content)
    assert len(made) >= 100
    for iid, it in made.items():
        twin = content.items[masterwork_id(iid)]
        assert twin["masterwork"] is True and twin["base"] == iid and twin["source"] == "masterwork", iid
        for key in ("name_key", "emoji", "kind", "slot", "type", "tier", "rarity", "req_level"):
            assert twin[key] == it[key], (iid, key)
        assert all(twin["stats"].get(k, 0) >= v for k, v in it["stats"].items()), iid      # better in every stat...
        assert sum(twin["stats"].values()) > sum(it["stats"].values()) * (1 + cfg["stat_bonus"]) - 1e-9, iid   # ...+10 % and one bonus more
        extra = cfg["extra"][it["slot"]]
        assert all(twin["stats"][k] > it["stats"].get(k, 0) * (1 + cfg["stat_bonus"]) for k in extra), iid
        assert twin["price"] > it["price"], iid
    outputs = {out for r in content.professions["recipes"].values() for out in r["output"]}
    assert set(made) <= outputs                                         # twins are not "crafted": no recipe of their own
    assert not any(masterwork_id(iid) in outputs for iid in made)
    twins = {iid for iid, it in content.items.items() if it.get("masterwork")}
    assert len(twins) == len(made)
    for level in (5, 8, 30, 60, 100):                                   # never in random loot
        hero = Hero(id="x", name="X", class_id="guerrero", level=level)
        for seed in range(150):
            assert roll_gear(content.items, content.classes, content.balance, hero, level, Rng(seed), chance=1.0) not in twins
    for class_id in ("guerrero", "cazador_punteria", "mago_escarcha"):
        fresh = Hero(id="y", name="Y", class_id=class_id)
        assert not set(starter_gear(content.items, content.classes, content.balance, fresh)) & twins


def test_masterwork_chance_grows_with_rank_and_carpentry_is_the_specialist(service):
    catalog = service.content.professions["professions"]
    base = service.content.balance["masterwork"]["base_chance"]
    assert catalog["carpinteria"]["perk"] == {"masterwork": 0.15}
    assert masterwork_chance(catalog["carpinteria"], 100, 100, base) == pytest.approx(0.15)
    assert masterwork_chance(catalog["carpinteria"], 50, 100, base) == pytest.approx(0.075)
    assert masterwork_chance(catalog["herreria"], 100, 100, base) == pytest.approx(0.05)
    assert masterwork_chance(catalog["herreria"], 50, 100, base) == pytest.approx(0.025)
    hero = ready(service)
    chances = []
    for rank in (1, 25, 50, 75, 100):
        hero.professions = {"carpinteria": rank_xp(service, rank), "herreria": rank_xp(service, rank)}
        carp, smith = service._masterwork_chance(hero, "carpinteria"), service._masterwork_chance(hero, "herreria")
        assert carp == pytest.approx(3 * smith) and carp > 0
        chances.append(carp)
    assert chances == sorted(chances) and chances[-1] == pytest.approx(0.15)     # evenly with the rank, 15 % at 100
    for pid in ("carpinteria", "herreria", "sastreria", "peleteria", "joyeria"):
        assert service._makes_masterworks(pid), pid
    for pid in ("alquimia", "medicina", "aserradero", "lenador"):
        assert not service._makes_masterworks(pid), pid                 # potions, remedies and materials: never


def test_carpentry_perk_no_longer_gives_attack(service):
    catalog = service.content.professions["professions"]
    p = profession_rules.perks(catalog, {"carpinteria": 100}, 100, "malla", "arco", "ataque")
    assert p["attack"] == 0 and p["masterwork"] == pytest.approx(0.15)
    hero = ready(service)
    base = service._kit(hero)["perk_bonus"]
    hero.professions = {"carpinteria": rank_xp(service, 100), "herreria": rank_xp(service, 100)}
    hero.gear["arma"] = "artesano_baston_1"
    service._save(hero)
    hero = service._load("test:1")
    assert service._kit(hero)["perk_bonus"]["attack"] == base["attack"] == 0
    view = service.act("test:1", "oficios")
    lines = [line for line in view.body if "Beneficio ahora" in line]
    assert any("+15 % de obra maestra" in line for line in lines)        # 🪑 Carpintería
    assert any("+3 de armadura" in line and "+5 % de obra maestra" in line for line in lines)   # 🔨 its base chance too
    assert not service.texts.missing


# ---------------------------------------------------------------- crafting one


def test_a_masterwork_comes_out_signed_and_better(service, monkeypatch):
    ready(service, backpack={"lingote": 6, "cuero_curtido": 2}, energy=30, level=3)
    monkeypatch.setattr(service, "_masterwork_chance", lambda hero, pid: 1.0)
    recipe = service.act("test:1", "rec:espada_forjada:0")
    assert any("obra maestra" in line for line in recipe.body)
    view = service.act("test:1", "mk:espada_forjada:1:0")
    twin = masterwork_id("artesano_espada_1")
    hero = service._load("test:1")
    assert "¡Obra maestra!" in view.notice and "Lyra" in view.notice
    assert hero.backpack == {"lingote": 3, "cuero_curtido": 1, twin: 1} and hero.gear_signatures == {twin: "Lyra"}
    assert twin in hero.gear_new
    gear = service.act("test:1", "gear:0")
    assert any("✒️ Obra maestra de Lyra" in line for line in gear.body)
    item = service.act("test:1", f"item:{twin}")
    assert item.body[1] == "✒️ Obra maestra de Lyra" and any("Exclusiva" in line for line in item.body)
    assert "✒️" in item.body[0]
    monkeypatch.setattr(service, "_masterwork_chance", lambda hero, pid: 0.0)
    service.act("test:1", "mk:espada_forjada:1:0")
    hero = service._load("test:1")
    assert hero.backpack["artesano_espada_1"] == 1 and hero.backpack[twin] == 1   # the normal one, unsigned
    worn = []
    for piece in ("artesano_espada_1", twin):
        service.act("test:1", f"equip:{piece}")
        hero = service._load("test:1")
        assert hero.gear["arma"] == piece
        worn.append(hero_stats(service._kit(hero), hero.level))
    assert worn[1]["attack"] > worn[0]["attack"] and worn[1]["armor"] > worn[0]["armor"]   # +10 % and +1 defense
    assert any("✒️" in line for line in service.act("test:1", "gear").body)
    assert not service.texts.missing


def test_masterworks_go_on_by_themselves_in_an_empty_slot(service, monkeypatch):
    ready(service, backpack={"lingote": 1, "gema_bruta": 1}, energy=30, level=3)
    monkeypatch.setattr(service, "_masterwork_chance", lambda hero, pid: 1.0)
    service.act("test:1", "mk:anillo_engarzado:1:0")
    assert service._load("test:1").gear.get("joya") == masterwork_id("artesano_joya_1")


def test_how_many_masterworks_come_out_by_profession(service):
    # Real draws, fixed seed: at rank 100 a carpenter gets ~15 % and a blacksmith ~5 %.
    ready(service, backpack={"tablon": 600, "cuero_curtido": 400, "lingote": 600}, energy=2000, level=3)
    hero = service._load("test:1")
    hero.professions = {"carpinteria": rank_xp(service, 100), "herreria": rank_xp(service, 100)}
    service._save(hero)
    service.act("test:1", "mk:arco_olmo:200:0")
    service.act("test:1", "mk:espada_forjada:200:0")
    hero = service._load("test:1")
    bows = hero.backpack.get(masterwork_id("artesano_arco_1"), 0) + (hero.gear.get("arma") == masterwork_id("artesano_arco_1"))
    swords = hero.backpack.get(masterwork_id("artesano_espada_1"), 0)
    assert 12 <= bows <= 50 and 1 <= swords <= 25 and bows > swords
    assert hero.backpack.get("artesano_arco_1", 0) + bows == 200        # nothing lost: normal + masterwork = made
    assert hero.backpack.get("artesano_espada_1", 0) + swords == 200


# ---------------------------------------------------------------- selling and old saves


def test_a_masterwork_sells_for_more_and_its_signature_goes_with_the_last_copy(service, monkeypatch):
    twin = masterwork_id("artesano_espada_1")
    ready(service, backpack={"artesano_espada_1": 1, twin: 1}, gear_signatures={twin: "Lyra"}, level=3, gold=0)
    service.act("test:1", "sellg:artesano_espada_1")
    normal = service._load("test:1").gold
    service.act("test:1", f"sellg:{twin}")
    hero = service._load("test:1")
    master = hero.gold - normal
    ratio = service.content.balance["masterwork"]["price_mult"]
    assert master > normal and master == pytest.approx(normal * ratio, abs=1)
    assert twin not in hero.backpack and hero.gear_signatures == {}


def test_crafting_to_sell_stays_close_to_the_materials_value(content):
    """D-116 trade-off: a normal piece sells for less than its materials (D-113); a masterwork for 25 % more than the
    piece. Even at the best chance (15 %), selling everything made earns at most ~4 % over the materials' price."""
    cfg = content.balance["masterwork"]
    ratio = content.balance["shop"]["sell_ratio"]
    top = max(float((p.get("perk") or {}).get("masterwork", cfg["base_chance"])) for p in content.professions["professions"].values())
    for rdef in content.professions["recipes"].values():
        out = next(iter(rdef["output"]))
        if content.items[out].get("source") != "crafted":
            continue
        materials = sum(content.items[m]["price"] * n for m, n in rdef["inputs"].items())
        expected = content.items[out]["price"] * ratio * (1 + top * (cfg["price_mult"] - 1))
        assert expected < materials * 1.05, out


def test_old_heroes_without_signatures_load(service):
    make_hero(service)
    twin = masterwork_id("artesano_joya_1")
    data = service.store.get("hero", "test:1")
    data.pop("gear_signatures", None)
    data["backpack"] = {twin: 1}
    service.store.put("hero", "test:1", data)
    hero = service._load("test:1")
    assert hero.gear_signatures == {}
    assert Hero.from_dict({"id": "a", "name": "A", "class_id": "guerrero"}).gear_signatures == {}
    view = service.act("test:1", f"item:{twin}")
    assert view.body[1] == "✒️ Obra maestra"                           # no signature saved: still a masterwork
    assert service.act("test:1", "gear:0").kind == "gear"
    assert not service.texts.missing


# ---------------------------------------------------------------- 🪑 camp furniture


def test_furniture_is_made_only_by_carpentry_from_its_rank(service):
    recipes = service.content.professions["recipes"]
    furniture = {rid: r for rid, r in recipes.items() if service.content.items[next(iter(r["output"]))].get("kind") == "furniture"}
    # D-141: 🛡️ Escudos and 🛒 Mobiliario y carros add one exclusive piece each (recipes with "spec": tests/test_especializaciones.py)
    assert {rid for rid, r in furniture.items() if not r.get("spec")} == {"literas_roble", "armero_roble"}
    assert {r["profession"] for r in furniture.values()} == {"carpinteria"}
    assert [furniture[r]["min_rank"] for r in ("literas_roble", "armero_roble")] == [40, 70]
    ready(service, backpack={"tablon": 12, "tela_tejida": 4, "cuero_curtido": 2}, energy=30)
    hero = service._load("test:1")
    hero.professions = {"carpinteria": rank_xp(service, 39)}
    service._save(hero)
    assert "🔒" in service.act("test:1", "mk:literas_roble:1:0").notice
    hero = service._load("test:1")
    hero.professions = {"carpinteria": rank_xp(service, 40)}
    service._save(hero)
    recipe = service.act("test:1", "rec:literas_roble:0")
    assert any("mueble para tu campamento" in line for line in recipe.body) and len(recipe.actions) <= 4
    assert not any("obra maestra" in line for line in recipe.body)       # furniture never comes out a masterwork
    view = service.act("test:1", "mk:literas_roble:1:0")
    hero = service._load("test:1")
    assert "🔨 Obras" in view.notice and hero.backpack == {"literas_roble": 1}
    resources = service.act("test:1", "resources")
    assert any("Literas de roble" in line for line in resources.body)
    assert not service.texts.missing


def test_furniture_is_placed_once_per_camp_and_gives_its_bonus(service, clock):
    make_hero(service, "test:1", "Lyra")
    camp = camp_at(service, 3)
    set_hero(service, "test:1", backpack={"literas_roble": 2, "armero_roble": 1})
    cap, defense = service._members_cap(camp), service._camp_defense(camp)
    view = service.act("test:1", "upgrades")
    assert "upw" in ids(view) and any("Llevas para colocar" in line for line in view.body) and len(view.actions) <= 4
    pages, found = 0, set()
    page = service.act("test:1", "upw")
    while pages < 10:
        assert page.kind == "camp_works" and len(page.actions) <= 4
        found |= {a.id for a in page.actions if a.id.startswith("upf:")}
        more = [a.id for a in page.actions if a.id.startswith("upw:")]
        if not more or more[0] == "upw:0":
            break
        page = service.act("test:1", more[0])
        pages += 1
    assert found == {"upf:literas_roble", "upf:armero_roble"}
    view = service.act("test:1", "upf:literas_roble")
    assert "Colocaste" in view.notice
    camp = service.store.get("camp", KEY)
    assert service._members_cap(camp) == cap + 1 and service._load("test:1").backpack["literas_roble"] == 1
    assert service.store.get("upgrades", KEY)["furniture"]["literas_roble"]["by"] == "Lyra"
    again = service.act("test:1", "upf:literas_roble")                   # one of each piece: the second never stacks
    assert "ya tiene" in again.notice
    assert service._members_cap(camp) == cap + 1 and service._load("test:1").backpack["literas_roble"] == 1
    works = [a.id for p in range(4) for a in service.act("test:1", f"upw:{p}").actions]
    assert "upf:literas_roble" not in works                              # nothing to place twice
    service.act("test:1", "upf:armero_roble")
    assert service._camp_defense(camp) == defense + 1 and "armero_roble" not in service._load("test:1").backpack
    view = service.act("test:1", "upgrades")
    assert any("🪑 Muebles:" in line and "(de Lyra)" in line for line in view.body)
    assert any("Defensa: " + str(defense + 1) in line for line in view.body)
    set_hero(service, "test:1", x=0, y=0)                               # the Claro: furniture goes in your own camp
    assert service.act("test:1", "upf:literas_roble").kind == "claro"
    assert not service.texts.missing


def test_giving_to_a_work_keeps_its_page_with_furniture_listed(service):
    make_hero(service, "test:1", "Lyra")
    camp_at(service, 8)
    set_hero(service, "test:1", backpack={"literas_roble": 1, "armero_roble": 1, "madera": 5})
    record = service._upgrades(KEY)
    works = service._open_works(service.store.get("camp", KEY), record)
    entries = service._works_entries(service._load("test:1"), service.store.get("camp", KEY), record)
    assert entries[-2:] == [("furn", "literas_roble"), ("furn", "armero_roble")] and len(entries) == len(works) + 2
    view = service.act("test:1", f"upg:{works[-1]}")
    assert view.kind == "camp_works" and len(view.actions) <= 4 and "Aportaste" in view.notice
    assert f"upg:{works[-1]}" in ids(view)                               # it stays on the page of that work


def test_masterwork_and_furniture_screens_have_four_buttons_at_most(service, monkeypatch):
    make_hero(service, "test:1", "Lyra")
    camp_at(service, 5)
    hero = service._load("test:1")
    hero.professions = {"carpinteria": rank_xp(service, 100)}
    hero.backpack = {"tablon": 60, "tela_tejida": 20, "cuero_curtido": 20, "lingote": 20, "literas_roble": 1}
    hero.energy = 50
    service._save(hero)
    from test_camp_upgrades import build
    build(service, "taller")
    monkeypatch.setattr(service, "_masterwork_chance", lambda hero, pid: 1.0)
    for action in ("upgrades", "upw", "ctaller", "oficios", "est:craft:0", "est:craft:1", "rec:arco_olmo:0", "mk:arco_olmo:1:0",
                   "rec:literas_roble:0", "mk:literas_roble:1:0", "gear", "gear:0", f"item:{masterwork_id('artesano_arco_1')}",
                   "resources", "upf:literas_roble", "upgrades"):
        view = service.act("test:1", action)
        assert len(view.actions) <= 4, (action, ids(view))
    assert not service.texts.missing
