"""📜 Crafting orders between players (D-140, confirmed; how it was applied: D-335, provisional; 0.59).

[ES] Pruebas de lo que dijo el dueño en la entrevista de voz (E-24): "pedidos de fabricación, y todo servicio se paga aparte. Le
das al artesano los materiales, o le pagas para que los consiga, más su mano de obra". La forma (capa simple, D-44) es de
Claude (D-335, provisional), con la maquinaria de los 📜 encargos de reparación (D-333) y del 🏛️ Mercado (D-320). Revisa que:
- se encarga poniendo los materiales (salen de la mochila y quedan apartados) o pagando para que el artesano los consiga (a su
  precio de referencia o al que escribes con "m120"), más la mano de obra, que va siempre aparte: las monedas quedan apartadas;
- la mano de obra sugerida sale del tramo y la energía de la receta y solo se cambia dentro de la banda del mercado (D-26);
- un artesano sin el oficio o sin el rango no puede hacerlo; con ellos, en su estación, lo hace al momento: lo hecho viaja a
  📦 Entregas de quien encargó, el artesano cobra lo apartado menos el impuesto del mercado y gana experiencia del oficio;
- una ✒️ obra maestra llega con la firma del artesano;
- cancelar o vencer devuelve todo (las monedas a la bolsa, los materiales a 📦 Entregas), con aviso en su idioma;
- nadie hace su propio pedido; el tope de pedidos abiertos es el del mercado;
- se llega desde el 🏛️ Mercado, /pedidos, un oficio que no sabes, una receta que no puedes hacer y la estación del artesano;
- todo se lee en los dos idiomas, sin pasar el tope de botones, y los códigos /cf, /co y /cm no chocan con los de antes.
Archivo: tests/test_pedidos_de_fabricacion.py · Módulo: M13 Economía (con M14 Oficios) · Prueba: engine/service/craft_orders.py
(CraftOrderMixin), engine/service/game.py (text(), act(), tick(), _recipe_code, _recipe_view, _station_view, _prof_detail_view)
y engine/service/market.py (el botón del 🏛️ Mercado y 📦 Entregas).
"""

import re

import pytest

from conftest import make_hero
from engine.professions import xp_for_rank
from engine.service import GameService
from engine.service.craft_orders import CRAFT_ORDER_CODE_RE
from engine.service.game import (COORD_RE, FAQ_CODE_RE, GEAR_CODE_RE, PLACE_CODE_RE, RECIPE_CODE_RE, RECON_CODE_RE,
                                 RESOURCE_CODE_RE, SELL_CODE_RE, button_cap)
from engine.service.gremio import (ARMORY_IN_RE, ARMORY_OUT_RE, FUND_CODE_RE, GUILD_CODE_RE, MEMBER_CODE_RE, PLAYER_CODE_RE,
                                   ZONE_CODE_RE)
from engine.service.map_scroll import SCROLL_CODE_RE
from engine.service.market import market_code
from engine.service.repair import REPAIR_CODE_RE

RECIPE = "espada_forjada"               # 🔨 Herrería rank 1, ⚡2: 🔩 Lingote ×3 + 🟤 Cuero ×1 → 🟢🗡️ Espada forjada
SWORD = "artesano_espada_1"
MASTER = "artesano_espada_1_obra"
MATS = {"lingote": 3, "cuero_curtido": 1}


def ids(view):
    return [a.id for a in view.actions]


def text(view):
    return "\n".join([view.notice or ""] + list(view.body) + [a.label for a in view.actions])


def set_hero(service, account, **values):
    hero = service._load(account)
    for key, value in values.items():
        setattr(hero, key, value)
    service._save(hero)


def learn(service, account, pid="herreria", rank=1):
    hero = service._load(account)
    if pid not in hero.learned:
        hero.learned.append(pid)
    hero.professions[pid] = xp_for_rank(service.content.balance["professions"]["rank_formula"], rank)
    service._save(hero)


def check_caps(view):
    if view.layout:
        assert sum(view.layout) == len(view.actions) and view.layout[-1] == 1 and max(view.layout) <= 8, (view.kind, view.layout)
    else:
        assert len(view.actions) <= button_cap(view.kind), (view.kind, len(view.actions))
    for action in view.actions:
        assert len(action.id.encode("utf-8")) <= 64, action.id


def recipe(service):
    return service.content.professions["recipes"][RECIPE]


def labor_ref(service):
    rdef = recipe(service)
    cfg = service.content.balance["craft_order"]
    return round(cfg["labor_per_energy"] * rdef["energy"] * (1 + rdef["min_rank"] / cfg["labor_rank_step"]))


def mats_value(service):
    return sum(service.content.items[i]["price"] * n for i, n in MATS.items())


def two_players(service, gold=1000):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    set_hero(service, "test:1", gold=gold, backpack={"lingote": 6, "cuero_curtido": 2})
    set_hero(service, "test:2", gold=0, backpack={})


def post(service, account="test:1", mode="mats", n=1, typed=None):
    view = service.act(account, f"cord:r:{RECIPE}")
    assert view.kind == "corder_draft", text(view)
    service.act(account, f"cord:m:{mode}")
    service.act(account, f"cord:q:{n}")
    for line in typed or []:
        service.text(account, line)
    return service.act(account, "cord:ok")


def the_order(service):
    orders = [o for _, o in service.store.items("craft_order")]
    assert len(orders) == 1, orders
    return orders[0]


def delivery(service):
    return service.content.balance["market"]["delivery_minutes"] * 60


# ---------------------------------------------------------------------------------------------------- posting

def test_posting_with_your_materials_escrows_them_and_the_labor(service):
    two_players(service)
    view = post(service, n=2)
    assert view.kind == "corders" and "Encargaste" in view.notice and "/cm1" in text(view)
    lyra = service._load("test:1")
    assert "lingote" not in lyra.backpack and "cuero_curtido" not in lyra.backpack       # 6 + 2: all of it went in
    order = the_order(service)
    assert order["mode"] == "mats" and order["mats"] == {"lingote": 6, "cuero_curtido": 2}
    assert order["coins"] == 2 * labor_ref(service) and lyra.gold == 1000 - order["coins"]  # only the labor, set aside
    assert order["item"] == SWORD and order["units"] == 2 and order["n"] == 2
    # without the materials it is refused and nothing is spent
    set_hero(service, "test:2", gold=500, backpack={"lingote": 1})
    view = post(service, "test:2", mode="mats")
    assert view.kind == "corder_draft" and "Te falta" in view.notice
    assert service._load("test:2").gold == 500 and service._load("test:2").backpack == {"lingote": 1}


def test_posting_with_coins_pays_the_materials_at_their_reference_value_or_the_typed_price(service):
    two_players(service)
    service.act("test:1", f"cord:r:{RECIPE}")
    draft = service.act("test:1", "cord:m:coins")
    assert "Gasta: 🔩 Lingote ×3" in text(draft) and service._money(mats_value(service)) in text(draft)
    view = post(service, mode="coins")
    order = the_order(service)
    assert order["mode"] == "coins" and order["mats"] == {} and order["mats_price"] == mats_value(service)
    assert order["coins"] == mats_value(service) + labor_ref(service)
    lyra = service._load("test:1")
    assert lyra.gold == 1000 - order["coins"] and lyra.backpack == {"lingote": 6, "cuero_curtido": 2}   # her bag untouched
    assert "pagaste los materiales" in text(view)
    service.act("test:1", f"cord:x:{order['id']}")
    # "m60" sets what you pay for the materials of each make (inside the band); it needs the coins mode
    service.act("test:1", f"cord:r:{RECIPE}")
    service.act("test:1", "cord:m:mats")
    assert "Que los consiga" in service.text("test:1", "m60").notice
    service.act("test:1", "cord:m:coins")
    service.text("test:1", "m60")
    service.act("test:1", "cord:ok")
    assert the_order(service)["mats_price"] == 60


def test_the_labor_fee_is_suggested_and_stays_inside_the_market_band(service):
    two_players(service)
    ref = labor_ref(service)
    market = service.content.balance["market"]
    low, high = max(1, int(ref * market["price_min"])), int(-(-ref * market["price_max"] // 1))
    draft = service.act("test:1", f"cord:r:{RECIPE}")
    assert service._money(ref) in text(draft) and "cord:l:2" in ids(draft)
    check_caps(draft)
    view = service.act("test:1", "cord:l:3")
    assert service.store.get("corder_open", "test:1")["labor"] == 3 * ref
    view = service.text("test:1", "999999")                                  # too much: back to the top of the band
    assert "banda" in view.notice and service.store.get("corder_open", "test:1")["labor"] == high
    view = service.text("test:1", "0 x2")                                    # too little: the bottom; and 2 makes
    draft = service.store.get("corder_open", "test:1")
    assert draft["labor"] == low and draft["n"] == 2
    assert "Escribe un número" in service.text("test:1", "mucho").notice
    service.text("test:1", "x99")                                            # at most craft_order.max_units
    assert service.store.get("corder_open", "test:1")["n"] == service.content.balance["craft_order"]["max_units"]
    service.act("test:1", "cord:q:1")
    service.text("test:1", "25")
    service.act("test:1", "cord:ok")
    assert the_order(service)["labor"] == 25
    assert not service.store.get("corder_open", "test:1")                    # the draft is gone
    # leaving the draft with another button stops reading numbers as a fee
    service.act("test:1", f"cord:r:{RECIPE}")
    service.act("test:1", "hero")
    assert not service.store.get("corder_open", "test:1")


# ---------------------------------------------------------------------------------------------------- taking

def test_an_artisan_without_the_profession_or_the_rank_cannot_take_it(service, monkeypatch):
    two_players(service)
    post(service)
    view = service.act("test:2", "cord:t:0")
    assert "/co1" in text(view) and "🔒" in text(view) and "Lyra" in text(view)
    view = service.text("test:2", "/co1")
    assert "Herrería" in view.notice and "Entrenador" in view.notice and the_order(service)
    # a recipe of rank 5: Bram has Herrería 1 only
    service.act("test:1", "cord")
    set_hero(service, "test:1", backpack={})
    service.act("test:1", "cord:r:espada_templada")
    service.act("test:1", "cord:m:coins")
    service.act("test:1", "cord:ok")
    learn(service, "test:2")
    view = service.act("test:2", "cord:t:0")
    lines = [line for line in view.body if "/co" in line]
    code = next(re.search(r"(/co\d+)", line).group(1) for line in lines if "templada" in line)
    view = service.text("test:2", code)
    assert "necesitas" in view.notice and "5" in view.notice
    assert service._load("test:2").gold == 0 and len(list(service.store.items("craft_order"))) == 2


def test_taking_it_crafts_at_once_and_the_item_travels_to_the_posters_deliveries(service, clock):
    two_players(service)
    post(service, n=2)
    learn(service, "test:2")
    energy = service._load("test:2").energy
    assert "cord" in ids(service.act("test:2", "mkt"))
    hub = service.act("test:2", "cord")
    assert "🔨 Para hacer (1)" in [a.label for a in hub.actions]
    view = service.text("test:2", "/pedidos")
    assert view.kind == "corders"
    service.act("test:2", "cord:t:0")
    view = service.text("test:2", "/co1")
    assert "Hiciste el pedido de Lyra" in view.notice and "Herrería" in view.notice
    bram = service._load("test:2")
    assert bram.energy == energy - 2 * recipe(service)["energy"]
    assert bram.professions["herreria"] > xp_for_rank(service.content.balance["professions"]["rank_formula"], 1)
    assert SWORD not in bram.backpack                                          # it is not the artisan's
    assert not list(service.store.items("craft_order"))
    notes = [view for account, view in service.tick() if account == "test:1"]
    assert notes and "Bram" in text(notes[0]) and "Entregas" in text(notes[0])
    box = service.store.get("market_box", "test:1")["items"]
    assert box[0]["good"] in (SWORD, MASTER) and sum(e["n"] for e in box) == 2 and box[0]["why"] == "crafted"
    assert "lo hizo Bram" in text(service.act("test:1", "mkt:box"))
    clock.advance(delivery(service) + 1)
    service.tick()
    service.act("test:1", "mkt:get")
    lyra = service._load("test:1")
    assert lyra.backpack.get(SWORD, 0) + lyra.backpack.get(MASTER, 0) == 2
    assert "no está en la lista" in service.text("test:2", "/co1").notice        # the list moved on


def test_the_artisan_gets_the_escrow_minus_the_market_tax_and_supplies_paid_materials(service):
    two_players(service)
    post(service, mode="coins")
    order = the_order(service)
    learn(service, "test:2")
    service.act("test:2", "cord:t:0")
    assert "Para este pedido te falta" in service.text("test:2", "/co1").notice   # he has to bring the materials
    set_hero(service, "test:2", backpack={"lingote": 4, "cuero_curtido": 1})
    service.act("test:2", "cord:t:0")
    view = service.text("test:2", "/co1")
    tax = service._mkt_tax(order["coins"])
    assert tax > 0 and service._money(tax) in view.notice
    bram = service._load("test:2")
    assert bram.gold == order["coins"] - tax                                   # labor + materials, minus 5 % of all of it
    assert bram.backpack == {"lingote": 1}                                     # he put the materials in
    log = service.store.get("market_log", str(service._today()))
    assert log["craft_done"] == 1 and log["craft_tax"] == tax and log["craft_coins"] == order["coins"]


def test_a_masterwork_arrives_with_the_artisans_signature(service, clock, monkeypatch):
    two_players(service)
    monkeypatch.setattr(GameService, "_masterwork_chance", lambda self, hero, pid: 1.0)
    post(service)
    learn(service, "test:2")
    service.act("test:2", "cord:t:0")
    view = service.text("test:2", "/co1")
    assert "obra maestra" in view.notice and "Bram" in view.notice
    entry = service.store.get("market_box", "test:1")["items"][0]
    assert entry["good"] == MASTER and entry["sig"] == "Bram"
    notes = [view for account, view in service.tick() if account == "test:1"]
    assert any("firma de Bram" in text(v) for v in notes)
    clock.advance(delivery(service) + 1)
    service.tick()
    service.act("test:1", "mkt:get")
    lyra = service._load("test:1")
    assert lyra.backpack[MASTER] == 1 and lyra.gear_signatures[MASTER] == "Bram"
    assert "Bram" in text(service.act("test:1", f"item:{MASTER}"))


# ---------------------------------------------------------------------------------------------------- cancel, expiry, safety

def test_cancel_and_expiry_give_everything_back(service, clock):
    two_players(service)
    post(service)
    order = the_order(service)
    learn(service, "test:2")
    service.act("test:2", "cord:t:0")                                         # Bram saw it...
    view = service.text("test:1", "/cm1")                                      # ...and Lyra cancels it
    assert view.kind == "corder_mine" and f"cord:x:{order['id']}" in ids(view)
    view = service.act("test:1", f"cord:x:{order['id']}")
    assert "Cancelaste" in view.notice and service._load("test:1").gold == 1000
    box = service.store.get("market_box", "test:1")["items"]
    assert {e["good"]: e["n"] for e in box} == MATS and all(e["at"] <= clock.now() for e in box)   # ready at once
    assert "ya no está" in service.text("test:2", "/co1").notice
    service.act("test:1", "mkt:get")
    assert service._load("test:1").backpack == {"lingote": 6, "cuero_curtido": 2}
    post(service, mode="coins")                                               # expired: coins back and a notice
    clock.advance(service.content.balance["craft_order"]["order_days"] * 86400 + 1)
    notes = [view for account, view in service.tick() if account == "test:1"]
    assert service._load("test:1").gold == 1000 and notes and "Nadie" in text(notes[0])
    assert not list(service.store.items("craft_order"))
    total = {}                                                                 # the daily report's counts, over the days
    for _, day in service.store.items("market_log"):
        for key, value in day.items():
            total[key] = total.get(key, 0) + value
    assert total["craft_expired"] == 1 and total["craft_cancelled"] == 1 and total["craft_posted"] == 2


def test_nobody_makes_their_own_order_and_the_cap_is_the_markets(service):
    two_players(service, gold=100000)
    learn(service, "test:1")
    post(service)
    view = service.act("test:1", "cord:t:0")
    assert "/co1" not in text(view)                                           # yours are not in the list...
    order = the_order(service)
    assert "tuyo" in service._corder_take(service._load("test:1"), order["id"]).notice   # ...nor can you make them
    assert not service._corder_takeable(service._load("test:1"))
    cap = service.content.balance["market"]["max_orders"]
    for _ in range(cap - 1):
        post(service, mode="coins")
    assert len(list(service.store.items("craft_order"))) == cap
    view = post(service, mode="coins")
    assert view.kind == "corder_draft" and str(cap) in view.notice
    assert len(list(service.store.items("craft_order"))) == cap


# ---------------------------------------------------------------------------------------------------- where it is reached

def test_it_is_reached_from_the_market_and_the_order_list_uses_recipe_codes(service):
    two_players(service)
    hub = service.act("test:1", "mkt")
    assert ids(hub)[-2:] == ["cord", "shop"] and len(hub.actions) <= button_cap("market")
    profs = service.act("test:1", "cord:new")
    line = next(l for l in profs.body if "Herrería" in l)
    recipes = service.text("test:1", re.search(r"(/cf\d+)", line).group(1))
    assert recipes.kind == "corder_recipes" and "/r1" in text(recipes)
    check_caps(recipes)
    code = next(re.search(r"(/r\d+)", l).group(1) for l in recipes.body if "Espada forjada" in l)
    draft = service.text("test:1", code)                                       # /r of the order list opens the draft
    assert draft.kind == "corder_draft" and "Espada forjada" in text(draft) and draft.layout
    check_caps(draft)
    assert ids(draft)[-1] == "cord:p:herreria:0"                               # ↩️ back to that profession's list


def test_unknown_professions_and_locked_recipes_offer_the_order_button(service):
    two_players(service)
    view = service.act("test:1", "pview:herreria")
    assert "cord:p:herreria:0" in ids(view) and ids(view)[0].startswith("learn:") and len(view.actions) <= 4
    view = service.act("test:1", f"rec:{RECIPE}:0")
    assert f"cord:r:{RECIPE}" in ids(view)
    assert service.act("test:1", f"cord:r:{RECIPE}").kind == "corder_draft"
    # the artisan's station lists the orders they can make, with /co codes, and their profession says how many
    post(service)
    learn(service, "test:2")
    station = service.act("test:2", "est:craft:0")
    assert any("/co1" in line and "Lyra" in line for line in station.body)
    assert any("Pedidos de fabricación" in line for line in service.act("test:2", "pview:herreria").body)
    view = service.text("test:2", "/co1")
    assert "Hiciste el pedido" in view.notice


# ---------------------------------------------------------------------------------------------------- languages and codes

def test_every_screen_reads_in_both_languages(service, clock):
    two_players(service)
    learn(service, "test:2")
    for account in ("test:1", "test:2"):
        service.act(account, "lang:en")
    screens = [service.act("test:1", a) for a in ("mkt", "cord", "cord:new", "cord:p:herreria:0", f"cord:r:{RECIPE}",
                                                    "cord:m:coins", "cord:l:2")]
    screens += [service.text("test:1", "40 x2"), service.text("test:1", "m50"), service.text("test:1", "nope")]
    screens += [service.act("test:1", "cord:ok"), service.text("test:1", "/orders"), service.text("test:1", "/cm1")]
    screens += [service.act("test:2", "cord:t:0"), service.act("test:2", "est:craft:0"), service.act("test:2", "pview:herreria")]
    set_hero(service, "test:2", backpack={"lingote": 6, "cuero_curtido": 2})
    screens += [service.text("test:2", "/co1"), service.act("test:1", "mkt:box"), service.act("test:1", "pview:sastreria")]
    screens += [view for _, view in service.tick()]
    post(service, mode="mats")
    clock.advance(service.content.balance["craft_order"]["order_days"] * 86400 + 1)
    screens += [view for _, view in service.tick()]
    joined = "\n".join(text(v) for v in screens)
    assert "Crafting orders" in joined and "Labor" in joined and "made your order" in joined and "Nobody took" in joined
    for view in screens:
        check_caps(view)
    assert not service.texts.fallbacks.get("en"), service.texts.fallbacks
    assert not service.texts.missing, service.texts.missing
    service.act("test:1", "lang:es")
    view = service.act("test:1", "cord")
    assert "Pedidos de fabricación" in view.title
    view = service.text("test:1", "/d64")
    assert "artesano" in text(view) and "{" not in text(view)


def test_order_codes_never_clash_with_the_old_ones():
    for code in ("/cf1", "/co2", "/cm_1", "/co12"):
        assert CRAFT_ORDER_CODE_RE.match(code)
        for other in (FAQ_CODE_RE, PLACE_CODE_RE, COORD_RE, SELL_CODE_RE, GEAR_CODE_RE, RESOURCE_CODE_RE, RECIPE_CODE_RE,
                      RECON_CODE_RE, SCROLL_CODE_RE, PLAYER_CODE_RE, GUILD_CODE_RE, MEMBER_CODE_RE, FUND_CODE_RE, ZONE_CODE_RE,
                      ARMORY_IN_RE, ARMORY_OUT_RE, REPAIR_CODE_RE):
            assert not other.match(code), (code, other.pattern)
        assert market_code(code) is None
    for code in ("/c1", "/o1", "/r1", "/ro1", "/rp1", "/cocina", "/pedidos", "/orders", "/f01"):
        assert not CRAFT_ORDER_CODE_RE.match(code), code
