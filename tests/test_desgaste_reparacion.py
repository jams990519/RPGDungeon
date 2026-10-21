"""🔧 Gear wears, gets repaired and one day breaks (D-139, confirmed; how it was applied: D-333, provisional; 0.57).

[ES] Pruebas de lo que dijo el dueño en la entrevista de voz (E-23): "el equipo se gasta, se repara y un día se rompe, con una
duración generosa que dé trabajo a los artesanos". La forma (capa simple, D-44) es de Claude (D-333, provisional) con la
recomendación de E-70 (unas 3 semanas de juego diario por reparación, se rompe tras 5 reparaciones). Revisa que:
- cada pelea gasta cada pieza puesta un poco, más al huir y más al caer; las piezas de la mochila no se gastan;
- en 0 la pieza queda dañada: sigue puesta y no se borra, pero no da bonos (ni su ✨) hasta repararla;
- el aviso "⚠️ desgaste alto" sale una sola vez al bajar del 20 %, y la pieza se marca ⚠️ en 🛡️ Equipo y en la ficha;
- reparar uno mismo pide el oficio que hace esa pieza, rango desde su nivel − 10, su estación, el refinado de base y ⚡, y da
  experiencia de oficio; con poco rango o sin el oficio no gasta nada;
- el herrero de la 🔥 fogata cobra 3 × lo que valen los materiales, solo en una fogata, y esas monedas se queman;
- cada reparación baja el máximo 4; antes de la última se pregunta otra vez; en su última vida, al llegar a 0, se rompe y sale
  (con su ✨ y su ✒️); la ✒️ obra maestra aguanta 8;
- los 📜 encargos de reparación: el dueño aparta las monedas, un artesano con el oficio los hace desde una estación, cobra
  menos el impuesto y el dueño recibe su pieza reparada y un aviso; cancelar, vencer o quedar sin sentido devuelve todo;
- la durabilidad viaja con cada pieza en el 🏛️ Mercado (quien compra ve "🔧 80/96") y en la ⚔️ Armería; lo que sale de la
  mochila se lleva la copia más gastada; lo que se pone, la mejor;
- los héroes de antes cargan con todo su equipo lleno y rinden igual (el simulador y el balance no cambian);
- todo se lee en los dos idiomas, sin pasar el tope de botones, y los códigos /rp y /ro no chocan con los de antes.
Archivo: tests/test_desgaste_reparacion.py · Módulo: M4 Equipo (con M14 Oficios y M13 Economía) · Prueba:
engine/hero/durability.py, engine/hero/gear.py (gear_bonus, is_better, equip, unequip), engine/service/repair.py (RepairMixin),
engine/service/game.py (_end_combat, _auto_combat, _worn_view, _item_view, _hero_view, _forget_piece, text(), tick()),
engine/service/market.py y engine/service/gremio.py (la durabilidad que viaja).
"""

import re

import pytest

from conftest import make_hero
from engine.combat import make_combat
from engine.hero import durability
from engine.hero.gear import gear_bonus, real_stats
from engine.professions import xp_for_rank
from engine.service.game import (COORD_RE, FAQ_CODE_RE, GEAR_CODE_RE, PLACE_CODE_RE, RECIPE_CODE_RE, RECON_CODE_RE,
                                 RESOURCE_CODE_RE, SELL_CODE_RE, button_cap)
from engine.service.gremio import (ARMORY_IN_RE, ARMORY_OUT_RE, FUND_CODE_RE, GUILD_CODE_RE, MEMBER_CODE_RE, PLAYER_CODE_RE,
                                   ZONE_CODE_RE)
from engine.service.map_scroll import SCROLL_CODE_RE
from engine.service.market import market_code
from engine.service.repair import REPAIR_CODE_RE
from test_armeria import guild_of_two

ENEMY = "lobo_ceniciento"
SWORD = "espada_1"                      # the guerrero's starter weapon: level 1, a sword (🔨 Herrería, 🔩 lingote)
MASTER = "artesano_espada_1_obra"       # a ✒️ masterwork sword of level 3


def ids(view):
    return [a.id for a in view.actions]


def text(view):
    return "\n".join([view.notice or ""] + list(view.body) + [a.label for a in view.actions])


def set_hero(service, account, **values):
    hero = service._load(account)
    for key, value in values.items():
        setattr(hero, key, value)
    service._save(hero)


def rec(item, cur, top=100.0, rep=0):
    return {"id": item, "cur": float(cur), "max": float(top), "rep": rep}


def fight(service, outcome, account="test:1"):
    """Close one fight with this outcome, as any fight (_end_combat); returns its end screen."""
    hero = service._load(account)
    edef = service.content.enemies[ENEMY]
    state = make_combat(ENEMY, edef, 1, service._kit(hero), 3)
    state["outcome"] = outcome
    view = service._end_combat(hero, state)
    service._save(hero)
    return view


def wear_of(service, slot="arma", account="test:1"):
    return durability.worn_record(service._load(account), slot, service.content.balance)


def cfg(service):
    return service.content.balance["durability"]


def check_caps(view):
    assert len(view.actions) <= button_cap(view.kind), (view.kind, len(view.actions))
    for action in view.actions:
        assert len(action.id.encode("utf-8")) <= 64


def learn_smithing(service, account, rank):
    hero = service._load(account)
    if "herreria" not in hero.learned:
        hero.learned.append("herreria")
    hero.professions["herreria"] = xp_for_rank(service.content.balance["professions"]["rank_formula"], rank)
    service._save(hero)


# ---------------------------------------------------------------------------------------------------- wear and damage

def test_every_fight_wears_the_worn_pieces_more_when_fleeing_and_most_when_falling(service):
    make_hero(service, "test:1", "Lyra")
    set_hero(service, "test:1", backpack={"espada_2": 1})
    loss = cfg(service)["wear"]
    assert loss["win"] < loss["flee"] < loss["defeat"]
    fight(service, "victory")
    assert wear_of(service)["cur"] == pytest.approx(100 - loss["win"])
    assert wear_of(service, "armadura")["cur"] == pytest.approx(100 - loss["win"])        # every worn piece
    fight(service, "fled")
    assert wear_of(service)["cur"] == pytest.approx(100 - loss["win"] - loss["flee"])
    fight(service, "defeat")
    assert wear_of(service)["cur"] == pytest.approx(100 - loss["win"] - loss["flee"] - loss["defeat"])
    hero = service._load("test:1")
    assert "espada_2" not in hero.bag_wear                                                # the backpack does not wear
    # generous: a day of play (20 fights: 18 won, 1 fled, 1 lost) leaves a new piece far from a repair
    day = 18 * loss["win"] + loss["flee"] + loss["defeat"]
    assert 14 <= 100 / day <= 35, 100 / day


def test_at_zero_the_piece_stays_worn_and_kept_but_gives_nothing(service):
    make_hero(service, "test:1", "Lyra")
    hero = service._load("test:1")
    full = gear_bonus(service.content.items, hero, service.content.classes, service.content.balance)
    set_hero(service, "test:1", gear_wear={"arma": rec(SWORD, 0.1)}, gear_enchants={SWORD: {"id": "filo", "value": 0.02}})
    view = fight(service, "defeat")
    assert any("Se dañó" in line and "0/100" in line for line in view.body)
    hero = service._load("test:1")
    assert hero.gear["arma"] == SWORD and durability.damaged(hero.gear_wear["arma"])     # still worn, never deleted
    bonus = gear_bonus(service.content.items, hero, service.content.classes, service.content.balance)
    assert bonus.get("attack", 0.0) == pytest.approx(full.get("attack", 0.0) - 0.04)      # the sword (and its ✨) give nothing
    assert SWORD in hero.gear_enchants
    view = fight(service, "victory")                                                       # it loses nothing more
    assert not any("Se dañó" in line for line in view.body) and durability.damaged(wear_of(service))
    worn = service.act("test:1", "gear")
    assert "sin bonos" in text(worn) and "⚠️ 🔧 0/100 dañada" in text(worn) and "rpr" in ids(worn)
    assert "⚠️" in text(service.act("test:1", "hero"))
    item = service.act("test:1", f"item:{SWORD}")
    assert "Dañada" in text(item) and "rpr:arma" in ids(item)
    check_caps(worn)
    check_caps(item)


def test_the_low_notice_comes_once_under_twenty_percent(service):
    make_hero(service, "test:1", "Lyra")
    line = cfg(service)["low_pct"] * 100
    set_hero(service, "test:1", gear_wear={"arma": rec(SWORD, line + 0.1)})
    view = fight(service, "victory")
    assert sum("Desgaste alto" in l and "Espada oxidada" in l for l in view.body) == 1
    view = fight(service, "victory")
    assert not any("Desgaste alto" in l for l in view.body)                                # once, not at every fight
    assert "⚠️ 🔧 20/100" in text(service.act("test:1", "gear"))
    assert "⚠️" in text(service.act("test:1", "hero"))
    # pieces wear together: two that cross at once share one line, never one notice per piece
    set_hero(service, "test:1", gear_wear={"arma": rec(SWORD, line + 0.1), "armadura": rec("placas_1", line + 0.1)})
    view = fight(service, "victory")
    low = [l for l in view.body if "Desgaste alto" in l]
    assert len(low) == 1 and "Espada oxidada" in low[0] and "Peto abollado" in low[0] and "las piezas" in low[0]


def test_automatic_fights_put_the_wear_notices_in_the_batch_summary(service):
    make_hero(service, "test:1", "Lyra")
    set_hero(service, "test:1", gear_wear={"arma": rec(SWORD, 0.1)})
    hero = service._load("test:1")
    edef = service.content.enemies[ENEMY]
    state = make_combat(ENEMY, edef, 1, service._kit(hero), 3)
    activity = {"log": []}
    service.store.put("combat", hero.id, state)
    service._auto_combat(hero, state, activity)                     # any end wears at least 0.15: the sword reaches 0
    assert sum("Se dañó" in line for line in activity["log"]) == 1 and state["wear"]


# ---------------------------------------------------------------------------------------------------- repairing

def test_self_repair_needs_the_profession_its_station_the_material_and_gives_xp(service):
    make_hero(service, "test:1", "Lyra")
    set_hero(service, "test:1", gear_wear={"arma": rec(SWORD, 0.0)}, backpack={"lingote": 2})
    view = service.text("test:1", "/reparar")
    assert view.kind == "repair" and "/rp1" in text(view)
    view = service.text("test:1", "/rp1")
    assert view.kind == "repair_piece" and "rpr!:arma:self" not in ids(view)              # no 🔨 without the profession
    assert "no sabes" in text(view) and "🥉39" in text(view)
    learn_smithing(service, "test:1", 1)
    view = service.text("test:1", "/rp1")
    assert "rpr!:arma:self" in ids(view)
    check_caps(view)
    hero = service._load("test:1")
    energy, xp = hero.energy, hero.professions["herreria"]
    set_hero(service, "test:1", x=3, y=3)                                                  # away from a station: nothing spent
    view = service.act("test:1", "rpr!:arma:self")
    assert "estación" in view.notice and durability.damaged(wear_of(service))
    set_hero(service, "test:1", x=0, y=0)
    view = service.act("test:1", "rpr!:arma:self")
    assert "Reparaste" in view.notice and "96/96" in view.notice
    hero = service._load("test:1")
    fixed = hero.gear_wear["arma"]
    assert fixed["cur"] == fixed["max"] == 100 - cfg(service)["repair_loss"] and fixed["rep"] == 1
    assert hero.backpack.get("lingote") == 1 and hero.energy == energy - cfg(service)["energy"]
    assert hero.professions["herreria"] - xp == durability.repair_xp(service.content.items[SWORD], service.content.balance)
    assert durability.repair_xp(service.content.items[SWORD], service.content.balance) >= cfg(service)["xp"]


def test_the_rank_asked_is_the_level_of_the_piece_minus_the_margin(service):
    make_hero(service, "test:1", "Lyra")
    piece = next(i for i, it in service.content.items.items()
                 if it.get("kind") == "gear" and it.get("type") == "placas" and it.get("req_level") == 50 and not it.get("source"))
    item = service.content.items[piece]
    need = durability.repair_rank(item, service.content.balance)
    assert need == 50 - cfg(service)["rank_margin"]
    mats = durability.repair_materials(item, service.content.balance)
    assert mats == {"lingote": 1 + 50 // cfg(service)["material_step"]}
    hero = service._load("test:1")
    hero.gear["armadura"] = piece
    hero.gear_wear["armadura"] = rec(piece, 10)
    hero.backpack["lingote"] = 10
    service._save(hero)
    learn_smithing(service, "test:1", need - 1)
    view = service.act("test:1", "rpr!:armadura:self")
    assert "necesitas" in view.notice and wear_of(service, "armadura")["cur"] == 10
    assert service._load("test:1").backpack["lingote"] == 10                                # nothing spent
    learn_smithing(service, "test:1", need)
    view = service.act("test:1", "rpr!:armadura:self")
    assert "Reparaste" in view.notice and service._load("test:1").backpack["lingote"] == 10 - mats["lingote"]
    # who repairs each type: the profession that makes it
    by = cfg(service)["repair_by"]
    assert by["espada"] == by["placas"] == "herreria" and by["arco"] == by["baston"] == "carpinteria"
    assert by["cuero"] == "peleteria" and by["tela"] == "sastreria" and by["joya"] == "joyeria"
    types = {it.get("type") for it in service.content.items.values() if it.get("kind") == "gear"}
    assert types <= set(by)                                                                 # every piece can be repaired
    crafted = {}
    for rdef in service.content.professions["recipes"].values():
        for out in rdef["output"]:
            out_item = service.content.items.get(out) or {}
            if out_item.get("kind") == "gear" and not rdef.get("retired") and not rdef.get("spec"):
                crafted.setdefault(out_item["type"], set()).add(rdef["profession"])
    for typ, makers in crafted.items():
        assert by[typ] in makers, (typ, makers)


def test_the_campfire_smith_charges_clearly_more_and_only_at_a_campfire(service):
    make_hero(service, "test:1", "Lyra")
    item = service.content.items[SWORD]
    price = durability.npc_price(item, service.content.items, service.content.balance)
    mats_value = durability.materials_value(durability.repair_materials(item, service.content.balance), service.content.items)
    assert price == cfg(service)["npc_mult"] * mats_value == 39
    assert price > durability.order_price(item, service.content.items, service.content.balance) > mats_value
    set_hero(service, "test:1", gear_wear={"arma": rec(SWORD, 30)}, gold=price, x=3, y=3)
    view = service.act("test:1", "rpr!:arma:npc")
    assert "fogata" in view.notice and service._load("test:1").gold == price
    set_hero(service, "test:1", x=0, y=0)
    assert "🔧 El herrero" in "\n".join(service.act("test:1", "shop").body)              # the merchant says where
    view = service.act("test:1", "rpr!:arma:npc")
    assert "herrero" in view.notice and service._load("test:1").gold == 0
    assert wear_of(service)["max"] == 96 and wear_of(service)["cur"] == 96
    view = service.act("test:1", "rpr!:arma:npc")
    assert "llena" in view.notice                                                            # full: nothing to repair


def test_each_repair_lowers_the_maximum_the_last_one_asks_and_then_it_breaks(service):
    make_hero(service, "test:1", "Lyra")
    repairs, loss = cfg(service)["repairs"], cfg(service)["repair_loss"]
    top = 100 - loss * (repairs - 1)
    set_hero(service, "test:1", gold=10000, gear_enchants={SWORD: {"id": "filo", "value": 0.02}},
             gear_wear={"arma": rec(SWORD, 0, top, repairs - 1)})
    view = service.act("test:1", "rpr:arma")
    assert "última" in text(view) and "1 reparación más" in text(view)
    view = service.act("test:1", "rpr!:arma:npc")
    assert view.kind == "repair_confirm" and "rpr!:arma:npc:ok" in ids(view) and "se rompe" in text(view)
    assert wear_of(service)["rep"] == repairs - 1                                            # nothing done yet
    view = service.act("test:1", "rpr!:arma:npc:ok")
    final = wear_of(service)
    assert final["rep"] == repairs and final["max"] == top - loss and "última vida" in view.notice
    view = service.act("test:1", "rpr:arma")
    assert "Última vida" in text(view) and not any(a.id.startswith("rpr!") for a in view.actions)
    set_hero(service, "test:1", gear_wear={"arma": rec(SWORD, 0.1, top - loss, repairs)})
    view = fight(service, "victory")
    assert any("se rompió para siempre" in line for line in view.body)
    hero = service._load("test:1")
    assert "arma" not in hero.gear and "arma" not in hero.gear_wear and SWORD not in hero.gear_enchants
    # with no repairs left the worn piece shows it everywhere: never deleted at 0 while it still takes repairs
    assert durability.repairs_left(rec(SWORD, 50, 80, repairs), service.content.items[SWORD], service.content.balance) == 0


def test_a_masterwork_takes_more_repairs(service):
    make_hero(service, "test:1", "Lyra")
    item = service.content.items[MASTER]
    assert durability.max_repairs(item, service.content.balance) == cfg(service)["masterwork_repairs"] > cfg(service)["repairs"]
    hero = service._load("test:1")
    hero.gear["arma"] = MASTER
    hero.gear_wear["arma"] = rec(MASTER, 0, 80, cfg(service)["repairs"])
    hero.gear_signatures[MASTER] = "Lyra"
    hero.gold = 1000
    service._save(hero)
    view = service.act("test:1", "rpr:arma")
    assert "obras maestras aguantan" in text(view)
    view = service.act("test:1", "rpr!:arma:npc")
    assert view.kind == "repair_piece" and wear_of(service)["rep"] == cfg(service)["repairs"] + 1   # no last-repair question yet


# ---------------------------------------------------------------------------------------------------- 📜 repair orders

def test_a_repair_order_pays_the_artisan_and_repairs_the_owners_piece(service, clock):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    item = service.content.items[SWORD]
    price = durability.order_price(item, service.content.items, service.content.balance)
    set_hero(service, "test:1", gold=100, gear_wear={"arma": rec(SWORD, 0)})
    set_hero(service, "test:2", gold=0, backpack={"lingote": 3})
    view = service.act("test:1", "rpo:arma")
    assert "Encargaste" in view.notice and "rpx:arma" in ids(view) and service._load("test:1").gold == 100 - price
    assert "📜 encargada" in text(service.act("test:1", "rpr"))
    assert "🔒" in text(service.act("test:2", "rpl"))                                        # Bram cannot do it yet
    learn_smithing(service, "test:2", 1)
    assert "rpr" in ids(service.act("test:2", "gear"))                                       # there is work for him
    view = service.act("test:2", "rpl")
    assert view.kind == "repair_orders" and "/ro1" in text(view) and "✅" in text(view) and "Lyra" in text(view)
    check_caps(view)
    view = service.text("test:2", "/ro1")
    tax = service._mkt_tax(price)
    assert "Reparaste" in view.notice and service._load("test:2").gold == price - tax
    bram = service._load("test:2")
    assert bram.backpack["lingote"] == 2 and bram.professions["herreria"] > xp_for_rank(
        service.content.balance["professions"]["rank_formula"], 1)
    assert wear_of(service)["max"] == 96 and wear_of(service)["rep"] == 1                   # the owner's piece is repaired
    assert not service.store.get("repair_order", "test:1|arma")
    notes = [view for account, view in service.tick() if account == "test:1"]
    assert notes and "Bram" in text(notes[0])
    assert "no está en la lista" in service.text("test:2", "/ro1").notice                    # the list moved on


def test_orders_go_back_when_cancelled_expired_or_no_longer_needed(service, clock):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    learn_smithing(service, "test:2", 1)
    set_hero(service, "test:2", backpack={"lingote": 3})
    set_hero(service, "test:1", gold=100, gear_wear={"arma": rec(SWORD, 0)})
    service.act("test:1", "rpo:arma")
    service.act("test:2", "rpl")                                                           # Bram saw it...
    view = service.act("test:1", "rpx:arma")                                               # ...and Lyra cancels it
    assert "Cancelaste" in view.notice and service._load("test:1").gold == 100
    assert "ya no está" in service.text("test:2", "/ro1").notice
    service.act("test:1", "rpo:arma")                                                      # expired: coins back, a notice
    clock.advance(cfg(service)["order_days"] * 86400 + 1)
    notes = [view for account, view in service.tick() if account == "test:1"]
    assert service._load("test:1").gold == 100 and notes and "Nadie" in text(notes[0])
    service.act("test:1", "rpo:arma")                                                      # void: the piece was taken off
    service.act("test:1", "unequip:arma")
    service.act("test:2", "rpl")
    view = service.text("test:2", "/ro1")
    assert "ya no hace falta" in view.notice and service._load("test:1").gold == 100
    assert service._load("test:2").backpack["lingote"] == 3                                  # nothing spent
    service.act("test:1", f"equip:{SWORD}")
    set_hero(service, "test:1", gear_wear={"arma": rec(SWORD, 0)})
    service.act("test:1", "rpo:arma")                                                      # repaired by yourself: order closed
    set_hero(service, "test:1", gold=service._load("test:1").gold + 39)
    view = service.act("test:1", "rpr!:arma:npc")
    assert "Cancelaste" in view.notice and service._load("test:1").gold == 100
    assert not service.store.get("repair_order", "test:1|arma")


# ---------------------------------------------------------------------------------------------------- the piece travels

def test_the_market_carries_durability_and_the_worst_copy_goes_first(service, clock):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    used = rec(SWORD, 80, 96, 1)
    set_hero(service, "test:1", backpack={SWORD: 1}, bag_wear={SWORD: [used]}, gold=0)
    set_hero(service, "test:2", gold=1000)
    view = service.act("test:1", "mkt:sell:0")
    line = next(l for l in view.body if "Espada oxidada" in l and "/s" in l)
    assert "🔧 80/96" in line
    service.text("test:1", re.search(r"(/s\d+)", line).group(1))
    service.act("test:1", "mkt:ok")
    seller = service._load("test:1")
    assert SWORD not in seller.backpack and SWORD not in seller.bag_wear
    order = service.store.get("market_order", "m1")
    assert order["wear"][0]["cur"] == 80
    offers = service.act("test:2", "mkt:cat:weapons:0")
    assert "🔧 80/96" in text(offers)                                                       # the buyer sees it before paying
    offer = service.text("test:2", "/c1")
    assert "Durabilidad: 80/96" in text(offer) and "4 reparaciones más" in text(offer)
    service.act("test:2", "mkt:buy:m1:1")
    clock.advance(service.content.balance["market"]["delivery_minutes"] * 60 + 1)
    service.act("test:2", "mkt:get")
    buyer = service._load("test:2")
    assert buyer.backpack[SWORD] == 1 and buyer.bag_wear[SWORD][0]["cur"] == 80
    assert "🔧 80/96" in text(service.act("test:2", "gear:0"))
    service.act("test:2", "unequip:arma")                                                  # now 2 copies: one new, one used
    service.act("test:2", f"equip:{SWORD}")                                                # the best (new) goes on
    buyer = service._load("test:2")
    assert "arma" not in buyer.gear_wear and buyer.bag_wear[SWORD][0]["cur"] == 80
    service.act("test:2", f"sellg:{SWORD}")                                                # the worst leaves first
    buyer = service._load("test:2")
    assert SWORD not in buyer.bag_wear and SWORD not in buyer.backpack and buyer.gear["arma"] == SWORD


def test_the_armory_carries_durability(service):
    gid = guild_of_two(service)
    set_hero(service, "test:1", backpack={"espada_2": 1}, bag_wear={"espada_2": [rec("espada_2", 50, 92, 2)]})
    service.act("test:1", "garm")
    service.text("test:1", "/a1")
    entry = service.store.get("armory", gid)["items"][0]
    assert entry["wear"]["cur"] == 50 and "espada_2" not in service._load("test:1").bag_wear
    view = service.act("test:2", "garm")
    assert "🔧 50/92" in text(view)
    service.text("test:2", "/t1")
    assert service._load("test:2").bag_wear["espada_2"][0]["max"] == 92


# ---------------------------------------------------------------------------------------------------- old heroes, balance

def test_old_heroes_load_with_full_gear_and_the_same_stats(service):
    make_hero(service, "test:1", "Lyra")
    data = service.store.get("hero", "test:1")
    data.pop("gear_wear", None)
    data.pop("bag_wear", None)                                                               # a hero saved before 0.57
    service.store.put("hero", "test:1", data)
    hero = service._load("test:1")
    assert hero.gear_wear == {} and hero.bag_wear == {}
    for slot, item_id in hero.gear.items():
        record = durability.worn_record(hero, slot, service.content.balance)
        assert record["cur"] == record["max"] == cfg(service)["max"] and record["rep"] == 0
    bonus = gear_bonus(service.content.items, hero, service.content.classes, service.content.balance)
    total = {}
    for item_id in hero.gear.values():
        for stat, value in real_stats(service.content.items, item_id, hero, service.content.classes, service.content.balance).items():
            total[stat] = total.get(stat, 0.0) + value
    assert bonus == total                                                                     # the simulator's numbers stay
    assert not any("⚠️" in line for line in service.act("test:1", "hero").body)
    assert "rpr" not in ids(service.act("test:1", "gear"))                                   # nothing to repair: no button
    # a record of another piece (Hero.gear changed by hand) never passes its wear on
    hero.gear_wear["arma"] = rec("daga_1", 0)
    assert not durability.slot_damaged(hero, "arma", service.content.balance)


# ---------------------------------------------------------------------------------------------------- both languages

def test_every_screen_reads_in_both_languages(service, clock):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    learn_smithing(service, "test:2", 1)
    for account in ("test:1", "test:2"):
        service.act(account, "lang:en")
    repairs = cfg(service)["repairs"]
    set_hero(service, "test:1", gold=500, gear_wear={"arma": rec(SWORD, 0, 84, repairs - 1), "armadura": rec("placas_1", 15)})
    screens = [service.act("test:1", a) for a in ("gear", "hero", "rpr", "rpr:arma", "rpr!:arma:npc", "rpo:arma", "rpl", "shop")]
    screens += [service.text("test:1", "/repair"), service.text("test:1", "/rp2"), service.act("test:1", "item:placas_1")]
    screens += [service.act("test:2", "rpl"), service.act("test:2", "pview:herreria"), fight(service, "victory")]
    screens += [view for _, view in service.tick()]
    joined = "\n".join(text(v) for v in screens)
    assert "Repair" in joined and "Durability" in joined and "damaged" in joined
    for view in screens:
        check_caps(view)
    assert not service.texts.fallbacks.get("en"), service.texts.fallbacks
    assert not service.texts.missing, service.texts.missing
    service.act("test:1", "lang:es")
    view = service.act("test:1", "rpr")
    assert "Reparar" in view.title and "/rp1" in text(view)
    view = service.text("test:1", "/d63")
    assert "durabilidad" in text(view) and "{" not in text(view)


def test_repair_codes_never_clash_with_the_old_ones():
    for code in ("/rp1", "/ro2", "/rp_1", "/ro12"):
        assert REPAIR_CODE_RE.match(code)
        for other in (FAQ_CODE_RE, PLACE_CODE_RE, COORD_RE, SELL_CODE_RE, GEAR_CODE_RE, RESOURCE_CODE_RE, RECIPE_CODE_RE,
                      RECON_CODE_RE, SCROLL_CODE_RE, PLAYER_CODE_RE, GUILD_CODE_RE, MEMBER_CODE_RE, FUND_CODE_RE, ZONE_CODE_RE,
                      ARMORY_IN_RE, ARMORY_OUT_RE):
            assert not other.match(code), (code, other.pattern)
        assert market_code(code) is None
    for code in ("/r1", "/rc1", "/e1", "/q1", "/reparar", "/repair", "/pm1"):
        assert not REPAIR_CODE_RE.match(code), code
