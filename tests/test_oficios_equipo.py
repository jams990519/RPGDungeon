"""Phase 2 of the profession network, gear side (D-115): ✨ Enchanting, the "⬆️ better piece" notice and crafted head,
hands, legs and feet.

[ES] Pruebas de la fase 2 de la red de oficios, lado del equipo: desencantar da esencias según el nivel y la rareza de la
pieza (y hasta 30 % más con el rango 100 del ✨ Encantamiento), encantar pone UN encantamiento por pieza (se reemplaza, no se
suma) que entra en las estadísticas y se ve en el equipo; nada se gasta si falta algo; los héroes viejos cargan; desencantar y
vender las esencias nunca paga más que vender la pieza; el aviso "⬆️ Tienes una pieza mejor" sale solo si la pieza es mejor y
la puedes usar, y su botón 🔁 Equipar la pone; cada pieza de artesano de cabeza, manos, piernas y pies tiene su receta y
supera al botín de su nivel; todas las pantallas con 4 botones como mucho y sin textos que falten.
"""

import pytest

from conftest import make_hero
from engine.combat import make_combat
from engine.hero import Hero, hero_stats
from engine.hero.gear import gear_bonus, gear_score, is_better, piece_score
from engine.professions import (branches_of, disenchant_amount, disenchant_yield, enchant_cost, enchant_for_slot,
                                enchant_value, masterwork_id, xp_for_rank)
from engine.professions.rules import PERK_KEYS
import engine.service.game as game_module

NEW_SLOTS = ("cabeza", "manos", "piernas", "pies")
TYPES = ("tela", "cuero", "malla", "placas")
PROFESSION_OF = {"tela": "sastreria", "cuero": "peleteria", "malla": "peleteria", "placas": "herreria"}


def ids(view):
    return [a.id for a in view.actions]


def ready(service, account="test:1", class_id="guerrero", **values):
    """A hero in the Claro, tutorial done, with the given fields set."""
    make_hero(service, account, "Lyra" if account == "test:1" else "Bram", class_id)
    hero = service._load(account)
    hero.tutorial = len(service.content.balance["tutorial"]["steps"])
    for key, value in values.items():
        setattr(hero, key, value)
    service._save(hero)
    return hero


def rank_xp(service, rank):
    return xp_for_rank(service.content.balance["professions"]["rank_formula"], rank)


def set_rank(service, account, pid, rank):
    hero = service._load(account)
    hero.professions[pid] = rank_xp(service, rank)
    service._save(hero)


def gear_items(content, **match):
    return {iid: it for iid, it in content.items.items() if it.get("kind") == "gear" and all(it.get(k) == v for k, v in match.items())}


# ---------------------------------------------------------------- ✨ disenchanting


def test_disenchant_gives_essences_scaled_by_level_and_rarity(content):
    cfg = content.balance["enchanting"]["disenchant"]
    items = content.items
    assert disenchant_yield(items["cabeza_tela_1"], cfg) == {"esencia": 1}                       # ⚪ common, level 1
    assert disenchant_yield(items["espada_2"], cfg) == {"esencia": 2}                            # 🟢 level 3
    assert disenchant_yield(items["espada_14"], cfg) == {"esencia": 3 + 100 // 20}                # 🔵 level 100: 8
    assert disenchant_yield(items["artesano_espada_13"], cfg) == {"esencia": 9, "esencia_mayor": 1}   # 🟣: also a major one
    assert disenchant_yield(items[masterwork_id("artesano_espada_13")], cfg) == {"esencia": 9, "esencia_mayor": 1}
    for typ in ("espada", "placas", "cabeza_tela"):
        counts = [disenchant_yield(items[f"{typ}_{tier}"], cfg)["esencia"] for tier in range(5, 15)]
        assert counts == sorted(counts) and counts[-1] > counts[0], typ                          # more with the level
    assert disenchant_amount(10, 0.3, 0.99) == 13 and disenchant_amount(10, 0.0, 0.0) == 10
    assert disenchant_amount(3, 0.15, 0.44) == 4 and disenchant_amount(3, 0.15, 0.46) == 3       # 3 × 1.15 = 3.45


def test_disenchanting_a_piece_destroys_it_and_raises_the_profession(service):
    ready(service, level=12, backpack={"espada_5": 2, "placas_3": 1}, energy=30)
    view = service.act("test:1", "ench:espada_5")
    assert view.kind == "enchant" and "dis:espada_5" in ids(view) and len(view.actions) <= 4
    assert any("Esencia arcana ×3" in line for line in view.body)
    view = service.act("test:1", "dis:espada_5")
    hero = service._load("test:1")
    assert hero.backpack["espada_5"] == 1 and hero.backpack["esencia"] == 3 and hero.energy == 29
    assert hero.professions["encantamiento"] == 6 and "Desencantaste" in view.notice
    assert view.kind == "enchant"                                       # a copy is left: its screen again
    view = service.act("test:1", "dis:espada_5")
    assert view.kind == "gear" and "espada_5" not in service._load("test:1").backpack
    worn = service.act("test:1", "dis:espada_1")                        # what you wear is never disenchanted
    assert "quítatelo" in worn.notice and service._load("test:1").gear["arma"] == "espada_1"
    hero = service._load("test:1")
    hero.energy = 0
    service._save(hero)
    assert "dis:placas_3" not in ids(service.act("test:1", "ench:placas_3"))
    service.act("test:1", "dis:placas_3")
    assert service._load("test:1").backpack.get("placas_3") == 1        # no energy: nothing happens
    assert not service.texts.missing


def test_disenchant_perk_gives_30_percent_more_at_rank_100(service):
    catalog = service.content.professions["professions"]
    assert "disenchant" in PERK_KEYS and catalog["encantamiento"]["perk"] == {"disenchant": 0.30}
    assert catalog["encantamiento"]["branch"] == "enchant"
    ready(service, level=12, backpack={"espada_7": 40}, energy=200)    # 🔵 level 30: 3 + 1 = 4 essences each
    set_rank(service, "test:1", "encantamiento", 100)
    for _ in range(40):
        service.act("test:1", "dis:espada_7")
    got = service._load("test:1").backpack["esencia"]
    assert 4 * 40 * 1.2 <= got <= 4 * 40 * 1.4                          # ~+30 % (208 on average)
    view = service.act("test:1", "oficios")
    assert any("+30 % de esencias al desencantar" in line for line in view.body)
    assert not service.texts.missing


# ---------------------------------------------------------------- ✨ enchanting


def test_enchant_applies_once_per_piece_and_shows_in_stats(service):
    ready(service, level=3, backpack={"esencia": 30, "lingote": 4}, energy=30)
    hero = service._load("test:1")
    base = hero_stats(service._kit(hero), hero.level)
    bonus = gear_bonus(service.content.items, hero, service.content.classes, service.content.balance)["attack"]
    view = service.act("test:1", "ench:espada_1")
    assert "enc:espada_1" in ids(view) and any("⚔️ Filo" in line for line in view.body)
    view = service.act("test:1", "enc:espada_1")
    hero = service._load("test:1")
    assert hero.gear_enchants == {"espada_1": {"id": "filo", "value": 0.01}}
    assert hero.backpack == {"esencia": 27, "lingote": 3} and hero.energy == 28 and hero.professions["encantamiento"] == 12
    assert gear_bonus(service.content.items, hero, service.content.classes, service.content.balance)["attack"] == pytest.approx(bonus + 0.01)
    assert hero_stats(service._kit(hero), hero.level)["attack"] > base["attack"]
    again = service.act("test:1", "enc:espada_1")                        # the same value again: not better, nothing spent
    assert "No gastaste nada" in again.notice and service._load("test:1").backpack["esencia"] == 27
    set_rank(service, "test:1", "encantamiento", 26)
    service.act("test:1", "enc:espada_1")
    hero = service._load("test:1")
    assert hero.gear_enchants["espada_1"] == {"id": "filo", "value": 0.02}          # replaced, never stacked
    assert gear_bonus(service.content.items, hero, service.content.classes, service.content.balance)["attack"] == pytest.approx(bonus + 0.02)
    assert any("✨" in line for line in service.act("test:1", "gear").body)
    item = service.act("test:1", "item:espada_1")
    assert any("✨ Encantamiento: ⚔️ Filo +2% ataque" in line for line in item.body) and "ench:espada_1" in ids(item)
    hub = service.act("test:1", "ench")
    assert any("Lo que llevas encantado" in line and "Filo" in line for line in hub.body)
    assert service.commands()["/encantar"] == "ench"
    assert not service.texts.missing


def test_one_enchant_per_slot_value_and_cost_rules(content):
    cfg = content.balance["enchanting"]
    enchants = cfg["enchants"]
    for slot in content.balance["gear"]["slots"]:
        assert enchant_for_slot(slot, enchants), slot                    # every slot takes exactly one enchantment
        assert sum(slot in e["slots"] for e in enchants.values()) == 1, slot
    filo = enchants["filo"]
    assert [enchant_value(filo, r, 100) for r in (1, 25, 26, 75, 76, 100)] == [0.01, 0.01, 0.02, 0.02, 0.03, 0.03]
    assert enchant_value(enchants["guarda"], 50, 100) == 0.01 and enchant_value(enchants["guarda"], 51, 100) == 0.02
    assert enchant_cost(content.items["espada_1"], filo, cfg["enchant"]) == {"esencia": 3, "lingote": 1}
    assert enchant_cost(content.items["espada_9"], filo, cfg["enchant"]) == {"esencia": 8, "esencia_mayor": 1, "lingote": 2}
    assert enchant_cost(content.items["artesano_espada_13"], filo, cfg["enchant"]) == {"esencia": 13, "esencia_mayor": 1, "lingote": 3}
    materials = {e["material"] for e in enchants.values()}
    assert materials == {"lingote", "extracto", "gema_bruta"}            # three other professions feed the enchanter


def test_enchanting_spends_nothing_when_something_is_missing(service):
    ready(service, level=50, backpack={"esencia": 30, "gema_bruta": 3, "pies_placas_9": 1, "espada_9": 1}, energy=30)
    view = service.act("test:1", "enc:pies_placas_9")                    # 🛡️ Guarda needs rank 25
    assert "rango 25" in view.notice and service._load("test:1").backpack["esencia"] == 30
    set_rank(service, "test:1", "encantamiento", 25)
    view = service.act("test:1", "enc:pies_placas_9")                    # level 50: a major essence too
    assert "Esencia mayor" in view.notice and "No gastaste nada" in view.notice
    assert service._load("test:1").backpack == {"esencia": 30, "gema_bruta": 3, "pies_placas_9": 1, "espada_9": 1}
    hero = service._load("test:1")
    hero.backpack["esencia_mayor"] = 1
    hero.energy = 1
    service._save(hero)
    view = service.act("test:1", "enc:pies_placas_9")                    # no energy
    assert service._load("test:1").backpack["esencia_mayor"] == 1 and not service._load("test:1").gear_enchants
    hero = service._load("test:1")
    hero.energy = 30
    service._save(hero)
    service.act("test:1", "enc:pies_placas_9")                           # a piece in the backpack can be enchanted too
    hero = service._load("test:1")
    assert hero.gear_enchants == {"pies_placas_9": {"id": "guarda", "value": 0.01}} and "esencia_mayor" not in hero.backpack
    assert hero.backpack["esencia"] == 30 - 8 and hero.backpack["gema_bruta"] == 1
    service.act("test:1", "dis:pies_placas_9")                           # the last copy takes its enchantment
    assert "pies_placas_9" not in service._load("test:1").gear_enchants
    assert not service.texts.missing


def test_a_signed_masterwork_asks_before_disenchanting(service):
    twin = masterwork_id("artesano_espada_1")
    ready(service, level=3, backpack={twin: 1}, gear_signatures={twin: "Lyra"}, energy=30)
    view = service.act("test:1", f"dis:{twin}")
    assert view.kind == "disenchant_confirm" and ids(view) == [f"dis!:{twin}", f"ench:{twin}"]
    assert any("obra maestra de Lyra" in line for line in view.body)
    assert service._load("test:1").backpack == {twin: 1}                 # nothing yet
    view = service.act("test:1", f"dis!:{twin}")
    hero = service._load("test:1")
    assert twin not in hero.backpack and hero.gear_signatures == {} and hero.backpack["esencia"] >= 2
    assert not service.texts.missing


def test_old_heroes_without_enchantments_load(service):
    make_hero(service)
    data = service.store.get("hero", "test:1")
    data.pop("gear_enchants", None)
    service.store.put("hero", "test:1", data)
    hero = service._load("test:1")
    assert hero.gear_enchants == {}
    assert Hero.from_dict({"id": "a", "name": "A", "class_id": "guerrero"}).gear_enchants == {}
    data["gear_enchants"] = {"espada_1": {"id": "retirado", "value": 0.5}}   # an unknown enchantment id is ignored, never a crash
    service.store.put("hero", "test:1", data)
    hero = service._load("test:1")
    assert gear_bonus(service.content.items, hero, service.content.classes, service.content.balance)["attack"] == pytest.approx(0.04)
    for action in ("gear", "gear:0", "item:espada_1", "ench:espada_1", "ench", "oficios"):
        assert service.act("test:1", action).actions
    assert not service.texts.missing


# ---------------------------------------------------------------- no coins from nothing


def test_disenchanting_never_pays_more_than_selling_the_piece(content):
    """Worst case: the perk at rank 100 rounded up and 💱 Comercio on both sides; the essences at the merchant (half price,
    1 🥉 at least each) are always worth less than the piece."""
    cfg = content.balance["enchanting"]
    ratio = content.balance["shop"]["sell_ratio"]
    perk = content.professions["professions"]["encantamiento"]["perk"]["disenchant"]
    for iid, item in gear_items(content).items():
        piece = max(1, int(item["price"] * ratio))
        gives = disenchant_yield(item, cfg["disenchant"], cfg["essence"], cfg["major_essence"])
        best = sum(disenchant_amount(n, perk, 0.0) * max(1, int(content.items[e]["price"] * ratio)) for e, n in gives.items())
        assert best < piece, iid
    for essence in (cfg["essence"], cfg["major_essence"]):
        assert content.items[essence]["keep"] and essence not in content.balance["shop"]["sells"]


def test_disenchant_and_sell_earns_less_than_selling(service):
    ready(service, level=12, backpack={"espada_5": 2}, gold=0, energy=30)
    set_rank(service, "test:1", "encantamiento", 100)
    service.act("test:1", "sellg:espada_5")
    by_selling = service._load("test:1").gold
    service.act("test:1", "dis:espada_5")
    hero = service._load("test:1")
    essences = hero.backpack["esencia"]
    for _ in range(essences):
        service.act("test:1", "sell:esencia")
    assert service._load("test:1").gold - by_selling < by_selling


# ---------------------------------------------------------------- ⬆️ the better piece


def test_better_means_usable_of_your_type_and_a_higher_score(content):
    items, classes, balance = content.items, content.classes, content.balance
    hero = Hero(id="h", name="H", class_id="guerrero", level=10, gear={"arma": "espada_1", "armadura": "placas_1"})
    assert is_better(items, "espada_5", hero, classes, balance)          # level 10, sword, far more attack
    assert not is_better(items, "espada_6", hero, classes, balance)      # level 20: not yet
    assert not is_better(items, "daga_5", hero, classes, balance)        # not your weapon type
    assert not is_better(items, "tela_5", hero, classes, balance)        # not your armor type
    assert is_better(items, "cabeza_placas_5", hero, classes, balance)   # an empty slot: anything of yours is better
    hero.gear["arma"] = "espada_5"
    assert not is_better(items, "espada_4", hero, classes, balance) and not is_better(items, "espada_5", hero, classes, balance)
    score = piece_score(items, "espada_5", hero, classes, balance)
    assert score == pytest.approx(gear_score(items["espada_5"]["stats"], balance))
    hero.gear_enchants = {"espada_4": {"id": "filo", "value": 0.03}}     # an enchantment counts in the score
    assert piece_score(items, "espada_4", hero, classes, balance) == pytest.approx(gear_score(items["espada_4"]["stats"], balance) + 0.03)


def test_loot_says_when_a_piece_is_better_and_equip_works(service, monkeypatch):
    ready(service, level=10, energy=30)
    hero = service._load("test:1")
    edef = service.content.enemies["lobo_ceniciento"]
    monkeypatch.setattr(game_module, "roll_gear", lambda *a, **k: "espada_5")
    state = make_combat("lobo_ceniciento", edef, 10, service._kit(hero), 1)
    state["outcome"] = "victory"
    view = service._end_combat(hero, state)
    service._save(hero)
    assert any("Tienes una pieza mejor" in line and "Espada de la frontera" in line for line in view.body)
    assert ids(view)[0] == "equip:espada_5" and len(view.actions) <= 4 and state["better"] == "espada_5"
    worn = service.act("test:1", ids(view)[0])
    hero = service._load("test:1")
    assert hero.gear["arma"] == "espada_5" and hero.backpack.get("espada_1") == 1 and worn.kind == "gear_worn"
    for piece in ("espada_4", "daga_5", "espada_6"):                     # worse, not your type, too high: no notice
        monkeypatch.setattr(game_module, "roll_gear", lambda *a, piece=piece, **k: piece)
        hero = service._load("test:1")
        state = make_combat("lobo_ceniciento", edef, 10, service._kit(hero), 2)
        state["outcome"] = "victory"
        view = service._end_combat(hero, state)
        service._save(hero)
        assert not any("pieza mejor" in line for line in view.body), piece
        assert not any(a.id.startswith("equip:") for a in view.actions), piece
    gear = service.act("test:1", "gear:0")
    assert not any("⬆️" in line for line in gear.body if "•" in line)  # none of those is better
    hero = service._load("test:1")
    hero.backpack["placas_5"] = 1
    service._save(hero)
    gear = service.act("test:1", "gear:0")
    assert any("Peto de la frontera ⬆️" in line for line in gear.body)
    labels = [a.label for page in range(4) for a in service.act("test:1", f"gear:{page}").actions]
    assert any("Peto de la frontera ⬆️" in label for label in labels)          # its button carries the mark too
    assert not service.texts.missing


def test_crafting_a_better_piece_offers_equip_within_four_buttons(service):
    ready(service, level=3, backpack={"lingote": 30, "cuero_curtido": 30}, energy=30)
    view = service.act("test:1", "mk:espada_forjada:1:0")
    assert any("Tienes una pieza mejor" in line for line in view.notice.split("\n"))
    assert ids(view)[0] == "equip:artesano_espada_1" and len(view.actions) <= 4
    assert ids(view)[-1].startswith("est:")                              # ↩️ Volver stays
    service.act("test:1", "equip:artesano_espada_1")
    assert service._load("test:1").gear["arma"] == "artesano_espada_1"
    view = service.act("test:1", "mk:espada_forjada:1:0")               # the same piece again: not better, no button
    assert not any(a.id.startswith("equip:") for a in view.actions)
    assert not service.texts.missing


def test_automatic_fights_put_the_better_piece_in_the_batch_summary(service, monkeypatch):
    ready(service, level=10, energy=30)
    hero = service._load("test:1")
    edef = service.content.enemies["lobo_ceniciento"]

    def play(state, hero, class_def, ctx, **kwargs):
        state["outcome"] = "victory"
        state["log"] = []
        state["enemy"]["hp"] = 0
        return 1

    monkeypatch.setattr(game_module, "play_out", play)
    monkeypatch.setattr(game_module, "roll_gear", lambda *a, **k: "espada_5")
    state = make_combat("lobo_ceniciento", edef, 10, service._kit(hero), 3)
    activity = {"kind": "explore", "log": []}
    assert service._auto_combat(hero, state, activity) == "victory"
    assert any("Tienes una pieza mejor" in line and "Espada de la frontera" in line for line in activity["log"])
    assert "espada_5" in hero.backpack and hero.gear["arma"] == "espada_1"   # never put on by itself


# ---------------------------------------------------------------- crafted head, hands, legs and feet


def test_every_new_crafted_piece_has_its_recipe_and_beats_loot_of_its_level(content):
    recipes = content.professions["recipes"]
    profs = content.professions["professions"]
    by_output = {out: rdef for rdef in recipes.values() for out in rdef["output"]}
    ratio = content.balance["shop"]["sell_ratio"]
    count = 0
    for slot in NEW_SLOTS:
        for typ in TYPES:
            made = sorted((it["req_level"], iid) for iid, it in gear_items(content, slot=slot, type=typ, source="crafted").items())
            assert [lv for lv, _ in made] == [3, 5, 8] + list(range(10, 101, 10)), (slot, typ)
            for level, iid in made:
                item = content.items[iid]
                rdef = by_output[iid]
                assert rdef["profession"] == PROFESSION_OF[typ], iid
                assert rdef["min_rank"] == ({3: 1, 5: 25, 8: 50}.get(level) or 50 + level // 2), iid
                assert rdef["energy"] == 2 and rdef["xp"] == 12, iid
                assert len(branches_of(rdef, profs, recipes)) >= 2, iid
                loot = [it for it in gear_items(content, slot=slot, type=typ).values() if not it.get("source") and it["req_level"] == level]
                assert len(loot) == 1, iid
                assert all(item["stats"].get(k, 0) >= v for k, v in loot[0]["stats"].items()), iid
                assert sum(item["stats"].values()) > sum(loot[0]["stats"].values()), iid
                materials = sum(content.items[m]["price"] * n for m, n in rdef["inputs"].items())
                assert item["price"] * ratio < materials, iid                # crafting never makes coins (D-113)
                assert masterwork_id(iid) in content.items, iid              # its ✒️ twin, made at load
                count += 1
    assert count == 208


def test_best_crafted_beats_best_loot_in_the_new_slots_at_every_level(content):
    def best(pool, level):
        fits = [it for it in pool.values() if it["req_level"] <= level]
        return max(fits, key=lambda it: (it["req_level"], sum(it["stats"].values()))) if fits else None

    for slot in NEW_SLOTS:
        for typ in TYPES:
            loot = {i: it for i, it in gear_items(content, slot=slot, type=typ).items() if not it.get("source")}
            made = gear_items(content, slot=slot, type=typ, source="crafted")
            for level in range(3, 101):
                b_loot, b_made = best(loot, level), best(made, level)
                assert b_made["req_level"] >= b_loot["req_level"], (slot, typ, level)
                assert sum(b_made["stats"].values()) > sum(b_loot["stats"].values()), (slot, typ, level)
            assert all(it["rarity"] == "epico" for it in made.values() if it["req_level"] >= 10)


def test_a_crafted_helmet_is_made_and_worn(service):
    ready(service, level=3, backpack={"lingote": 3, "cuero_curtido": 2}, energy=30)
    view = service.act("test:1", "rec:artesano_cabeza_placas_1:0")
    assert view.kind == "recipe" and any("Celada de aprendiz" in line for line in view.body)
    service.act("test:1", "mk:artesano_cabeza_placas_1:1:0")
    hero = service._load("test:1")
    assert hero.gear.get("cabeza") in ("artesano_cabeza_placas_1", masterwork_id("artesano_cabeza_placas_1"))
    assert hero.professions["herreria"] == 12
    assert not service.texts.missing


# ---------------------------------------------------------------- screens


def test_enchanting_screens_keep_four_buttons_and_no_missing_texts(service):
    twin = masterwork_id("artesano_joya_1")
    ready(service, level=12, backpack={"esencia": 40, "esencia_mayor": 2, "lingote": 5, "extracto": 5, "gema_bruta": 5,
                                       "espada_5": 1, "placas_5": 1, twin: 1, "joya_5": 1}, gear_signatures={twin: "Lyra"}, energy=40)
    set_rank(service, "test:1", "encantamiento", 30)
    for action in ("ench", "gear", "gear:0", "gear:1", "item:espada_5", "ench:espada_5", "enc:espada_5", "item:espada_1",
                   "ench:espada_1", "ench:joya_5", "enc:joya_5", f"dis:{twin}", f"ench:{twin}", f"dis!:{twin}", "dis:placas_5",
                   "ench:nada", "enc:nada", "dis:nada", "oficios", "hero", "bag"):
        view = service.act("test:1", action)
        assert len(view.actions) <= (8 if view.kind == "hero" else 4), (action, ids(view))   # D-192: the hero hub, up to 8
    assert not service.texts.missing
