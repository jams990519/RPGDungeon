"""🏛️ Mercado: the player market (D-320, 0.46; D-137): sell orders, buy orders, 📋 Mis órdenes and 📦 Entregas.

[ES] Pruebas del pedido del dueño del 21-oct-2026 ("los jugadores venden a otros jugadores el equipo que encuentran o
fabrican: órdenes de venta para el equipo y lo fabricado, órdenes de compra para los recursos"), con la subasta global y los
transportistas de D-137 y las reglas chicas de D-320 (provisional). Revisa que:
- 🏛️ Mercado se abre desde el 🛒 Mercader de cualquier fogata, desde ⚒️ Oficios del campamento con el 🏪 Puesto de trueque y con
  /mercado o /market, sin pasar el tope de botones;
- una orden de venta saca las cosas de la mochila; quien compra paga, el vendedor cobra al momento menos el impuesto (con un
  aviso en su idioma) y lo comprado llega a 📦 Entregas a los market.delivery_minutes, donde se recoge;
- un pedido de compra aparta las monedas; quien lleva el recurso le vende en parte o todo, cobra menos el impuesto y las
  unidades viajan a 📦 Entregas de quien pidió;
- cancelar o vencer devuelve todo lo que queda (cosas a 📦 Entregas, monedas a la bolsa) y avisa al dueño de una vencida;
- el tope de órdenes, las monedas o cosas que no alcanzan, la banda de precio (D-26), nadie se compra a sí mismo y fuera de
  una fogata o del campamento solo se mira;
- la mochila llena deja el resto en la caja; nada se pierde;
- una ✒️ obra maestra viaja con su firma y su ✨ encantamiento; si choca con la copia que ya llevas, espera en la caja;
- dos compradores no se llevan la misma unidad; 💰 bolsas y 🪎 cofres también se venden;
- todas las pantallas se leen en inglés sin textos prestados del español; los códigos no chocan con los de antes;
- el informe diario cuenta el mercado.
Archivo: tests/test_mercado.py · Módulo: M13 Economía · Prueba: engine/service/market.py (MarketMixin), engine/service/game.py
(text(), act(), tick(), _shop_view, _service_uses), adapters/reports.py (market_lines).
"""

import re

from conftest import make_hero
from engine.service.game import (COORD_RE, FAQ_CODE_RE, GEAR_CODE_RE, PLACE_CODE_RE, RESOURCE_CODE_RE, SELL_CODE_RE,
                                 button_cap)
from engine.service.gremio import (ARMORY_IN_RE, ARMORY_OUT_RE, FUND_CODE_RE, GUILD_CODE_RE, MEMBER_CODE_RE,
                                   PLAYER_CODE_RE, ZONE_CODE_RE)
from engine.service.market import market_code
from test_camp_upgrades import build, camp_at
from test_camps import place


def ids(view):
    return [a.id for a in view.actions]


def text(view):
    return "\n".join([view.notice or ""] + list(view.body) + [a.label for a in view.actions])


def set_hero(service, account, **values):
    hero = service._load(account)
    for key, value in values.items():
        setattr(hero, key, value)
    service._save(hero)


def two_players(service):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    set_hero(service, "test:1", backpack={"pocion_vida": 3}, gold=0)
    set_hero(service, "test:2", backpack={}, gold=1000)


def tax(service, total):
    return int(total * service.content.balance["market"]["tax"] + 0.5)


def delivery(service):
    return service.content.balance["market"]["delivery_minutes"] * 60


def list_potions(service, price=20, n=2, account="test:1"):
    view = service.act(account, "mkt:sell:0")
    code = next(re.search(r"(/s\d+) 🧪", line).group(1) for line in view.body if "🧪" in line and "/s" in line)
    service.text(account, code)
    service.text(account, f"{price} x{n}")
    return service.act(account, "mkt:ok")


def check_caps(view):
    if view.layout:
        assert sum(view.layout) == len(view.actions) and view.layout[-1] == 1, (view.kind, view.layout)
    else:
        assert len(view.actions) <= button_cap(view.kind), (view.kind, len(view.actions))
    for action in view.actions:
        assert len(action.id.encode("utf-8")) <= 64


def test_market_opens_from_the_merchant_the_command_and_the_camp_trading_post(service):
    make_hero(service, "test:1", "Lyra")
    shop = service.act("test:1", "shop")
    assert "mkt" in ids(shop) and ids(shop)[-1] == "claro" and len(shop.actions) <= 4
    hub = service.act("test:1", "mkt")
    assert hub.kind == "market" and ids(hub)[:6] == ["mkt:cats", "mkt:sell:0", "mkt:fill:0", "mkt:ask:0", "mkt:mine", "mkt:box"]
    assert ids(hub)[-1] == "shop"                                   # ↩️ Volver goes back to the 🛒 Mercader
    check_caps(hub)
    assert service.text("test:1", "/mercado").kind == "market" and service.text("test:1", "/market").kind == "market"
    cats = service.act("test:1", "mkt:cats")
    assert cats.kind == "market_cats" and len(cats.actions) == 10         # D-326 (0.50): + 🗺️ Mapas; D-339 (0.62): + 🎒 Mochilas
    check_caps(cats)
    camp_at(service, 3)                                              # the founder stands at its camp (6, 0)
    assert "mkt" not in ids(service.act("test:1", "svc:oficio"))    # no 🏪 Puesto de trueque yet
    build(service, "trueque")
    view = service.act("test:1", "svc:oficio")
    assert "mkt" in ids(view) and "csell" in ids(view)
    check_caps(view)
    hub = service.act("test:1", "mkt")
    assert ids(hub)[-1] == "svc:oficio" and "🚶" not in text(hub)    # trading works at the camp with the Trading Post


def test_sell_order_lifecycle_pays_the_seller_and_delivers_after_the_trip(service, clock):
    two_players(service)
    view = list_potions(service, price=20, n=2)
    assert view.kind == "market_mine" and "🧪" in text(view)
    assert service._load("test:1").backpack.get("pocion_vida") == 1        # escrow: 2 left the backpack
    offers = service.act("test:2", "mkt:cat:remedies:0")
    assert "/c1" in text(offers) and "Lyra" in text(offers)
    offer = service.text("test:2", "/c1")
    assert offer.kind == "market_offer" and any(a.id.endswith(":a") for a in offer.actions)
    service.act("test:2", [a.id for a in offer.actions if a.id.endswith(":a")][0])
    seller, buyer = service._load("test:1"), service._load("test:2")
    assert buyer.gold == 1000 - 40 and seller.gold == 40 - tax(service, 40)       # paid at once, minus the tax
    assert "pocion_vida" not in buyer.backpack or buyer.backpack["pocion_vida"] == 0
    assert service.store.get("market_order", "m1") is None and not service._mkt_mine("test:1")   # filled: closed
    box = service.act("test:2", "mkt:box")
    assert "mkt:get" not in ids(box) and "🐴" in text(box)                  # still on its way
    pushes = dict(service.tick())
    assert "test:1" in pushes and "Bram" in text(pushes["test:1"])          # the seller hears about it
    clock.advance(delivery(service) + 1)
    pushes = dict(service.tick())
    assert "test:2" in pushes and "📦" in pushes["test:2"].title            # the buyer: it arrived
    before = sum(service._load("test:2").belt.values()) + service._load("test:2").backpack.get("pocion_vida", 0)
    view = service.act("test:2", "mkt:get")
    after_hero = service._load("test:2")
    assert sum(after_hero.belt.values()) + after_hero.backpack.get("pocion_vida", 0) == before + 2
    assert not service._mkt_box("test:2") and "📦" in view.notice


def test_buy_order_escrows_coins_and_is_filled_in_parts(service, clock):
    two_players(service)
    service.text("test:2", "/b01")                                          # 🪵 madera, code /01
    service.text("test:2", "3 x20")
    view = service.act("test:2", "mkt:ok")
    assert view.kind == "market_mine" and service._load("test:2").gold == 1000 - 60
    set_hero(service, "test:1", backpack={"madera": 12})
    fill = service.act("test:1", "mkt:fill:0")
    assert "/k1" in text(fill) and "Bram" in text(fill)
    service.text("test:1", "/k1")
    service.act("test:1", "mkt:give:m1:a")
    seller = service._load("test:1")
    assert "madera" not in seller.backpack and seller.gold == 36 - tax(service, 36)
    order = service.store.get("market_order", "m1")
    assert order["n"] == 8                                                   # partly filled: it stays up
    set_hero(service, "test:1", backpack={"madera": 30})
    service.act("test:1", "mkt:give:m1:a")
    assert service._load("test:1").backpack["madera"] == 22 and service.store.get("market_order", "m1") is None
    clock.advance(delivery(service) + 1)
    service.tick()
    set_hero(service, "test:2", backpack={})
    service.act("test:2", "mkt:get")
    assert service._load("test:2").backpack["madera"] == 20 and service._load("test:2").gold == 940


def test_cancel_returns_items_to_the_box_and_coins_to_the_wallet(service):
    two_players(service)
    list_potions(service, price=10, n=3)
    view = service.text("test:1", "/o1")
    assert view.kind == "market_order" and "mkt:x:m1" in ids(view)
    service.act("test:1", "mkt:x:m1")
    assert service.store.get("market_order", "m1") is None and service._mkt_index("sell:remedies") == []
    box = service._mkt_box("test:1")
    assert box and box[0]["good"] == "pocion_vida" and box[0]["n"] == 3 and box[0]["at"] <= service.clock.now()   # ready at once
    service.act("test:1", "mkt:get")
    assert service._load("test:1").backpack.get("pocion_vida", 0) + sum(service._load("test:1").belt.values()) >= 3
    service.text("test:2", "/b02")
    service.text("test:2", "4 x25")
    service.act("test:2", "mkt:ok")
    assert service._load("test:2").gold == 900
    service.act("test:2", "mkt:x:m2")
    assert service._load("test:2").gold == 1000


def test_orders_expire_and_everything_left_goes_back_with_a_notice(service, clock):
    two_players(service)
    list_potions(service, price=10, n=2)
    service.text("test:2", "/b02")
    service.text("test:2", "4 x25")
    service.act("test:2", "mkt:ok")
    clock.advance(service.content.balance["market"]["order_days"] * 86400 + 60)
    pushes = dict(service.tick())
    assert "test:1" in pushes and "test:2" in pushes and "⌛" in pushes["test:1"].title
    assert not list(service.store.items("market_order"))
    assert service._load("test:2").gold == 1000
    assert service._mkt_box("test:1")[0]["n"] == 2
    log = service.store.get("market_log", str(service._today()))
    assert log["expired"] == 2


def test_limits_coins_items_band_self_trade_and_place(service):
    two_players(service)
    cap = service.content.balance["market"]["max_orders"]
    set_hero(service, "test:1", backpack={"pocion_vida": cap + 2}, gold=0)
    for _ in range(cap):
        list_potions(service, price=10, n=1)
    view = list_potions(service, price=10, n=1)
    assert view.kind == "market_draft" and str(cap) in view.notice          # the cap of active orders
    offer = service.act("test:1", "mkt:o:m1")
    assert not any(a.id.startswith("mkt:buy:") for a in offer.actions)        # never buy your own order
    assert "📋" in service.act("test:1", "mkt:buy:m1:1").notice
    set_hero(service, "test:2", gold=5)
    assert "💰" in service.act("test:2", "mkt:buy:m1:1").notice and service.store.get("market_order", "m1")["n"] == 1
    service.text("test:2", "/b01")
    service.text("test:2", "3 x20")
    assert service.act("test:2", "mkt:ok").kind == "market_draft"            # 60 > 5 coins: refused
    low, high = service._mkt_band("pocion_vida")
    service.act("test:1", "mkt:x:m1")
    set_hero(service, "test:1", backpack={"pocion_vida": 1})
    service.act("test:1", "mkt:sell:0")
    service.text("test:1", "/s1")
    view = service.text("test:1", str(high * 100))
    assert "⚖️" in view.notice and service.store.get("market_open", "test:1")["price"] == high
    view = service.text("test:1", "5 x9")
    assert service.store.get("market_open", "test:1")["n"] == 9
    assert "🎒" in service.act("test:1", "mkt:ok").notice                  # only 1 in the backpack
    assert "⌨️" in service.text("test:1", "hola").notice                   # not a number: says how to type it
    place(service, "test:2", 3, 0, gold=1000)                               # away from any bonfire: browse only
    hub = service.act("test:2", "mkt")
    assert "🚶" in text(hub) and ids(hub)[-1] == "home"
    assert "🚶" in service.act("test:2", "mkt:buy:m2:1").notice and service._load("test:2").gold == 1000


def test_backpack_full_leaves_the_rest_in_the_box(service, clock):
    two_players(service)
    set_hero(service, "test:1", backpack={"provisiones": 10})
    view = service.act("test:1", "mkt:sell:0")
    code = next(re.search(r"(/s\d+) 🥖", line).group(1) for line in view.body if "🥖" in line)
    service.text("test:1", code)
    service.text("test:1", "15 x10")
    service.act("test:1", "mkt:ok")
    service.act("test:2", "mkt:buy:m1:a")
    clock.advance(delivery(service) + 1)
    cap = service._pack_per_type()                                           # D-338 (0.62): up to its type's cap
    set_hero(service, "test:2", backpack={"provisiones": cap - 4})
    view = service.act("test:2", "mkt:get")
    hero = service._load("test:2")
    assert hero.backpack["provisiones"] == cap and "🎒" in view.notice and f"🥖 Provisiones {cap}/{cap}" in view.notice
    assert service._mkt_box("test:2")[0]["n"] == 6                          # never lost: it waits
    set_hero(service, "test:2", backpack={})
    service.act("test:2", "mkt:get")
    assert service._load("test:2").backpack["provisiones"] == 6 and not service._mkt_box("test:2")


def test_a_masterwork_travels_with_its_signature_and_enchantment(service, clock):
    two_players(service)
    piece = next(i for i, item in service.content.items.items() if item.get("masterwork") and item.get("slot") == "arma")
    set_hero(service, "test:1", backpack={piece: 1}, gear_signatures={piece: "Lyra"},
             gear_enchants={piece: {"id": "filo", "value": 0.02}})
    service.act("test:1", "mkt:sell:0")
    service.text("test:1", "/s1")
    service.act("test:1", "mkt:ok")
    seller = service._load("test:1")
    assert piece not in seller.backpack and piece not in seller.gear_signatures and piece not in seller.gear_enchants
    offers = service.act("test:2", "mkt:cat:weapons:0")
    assert "Lyra" in text(offers) and ("✅" in text(offers) or "🔒" in text(offers) or "⚠️" in text(offers))
    offer = service.text("test:2", "/c1")
    assert "✒️" in text(offer) and "Lyra" in text(offer)
    service.act("test:2", "mkt:buy:m1:1")
    clock.advance(delivery(service) + 1)
    service.act("test:2", "mkt:get")
    buyer = service._load("test:2")
    assert buyer.backpack[piece] == 1 and buyer.gear_signatures[piece] == "Lyra" and buyer.gear_enchants[piece]["id"] == "filo"
    # a second copy signed by someone else waits in the box (the copies of a piece share one signature)
    order = service._mkt_new_order(service._load("test:1"), "sell", piece, service._mkt_ref_price(piece), 1, None, "Otro")
    assert order["sig"] == "Otro"
    service.act("test:2", f"mkt:buy:{order['id']}:1")
    clock.advance(delivery(service) + 1)
    view = service.act("test:2", "mkt:get")
    assert "✨" in view.notice and service._load("test:2").backpack[piece] == 1 and service._mkt_box("test:2")


def test_the_same_unit_is_never_sold_twice_and_bags_and_chests_sell_too(service):
    two_players(service)
    make_hero(service, "test:3", "Cora")
    set_hero(service, "test:3", gold=1000)
    set_hero(service, "test:1", bags=3, chests=1)
    view = service.act("test:1", "mkt:sell:0")
    assert "💰" in text(view) and "🪎" in text(view)
    code = next(re.search(r"(/s\d+) 💰", line).group(1) for line in view.body if "💰 " in line and "/s" in line)
    service.text("test:1", code)
    service.act("test:1", "mkt:p:1")
    service.act("test:1", "mkt:ok")
    hero = service._load("test:1")
    assert hero.bags == 2
    price = service.store.get("market_order", "m1")["price"]
    service.act("test:2", "mkt:buy:m1:1")
    view = service.act("test:3", "mkt:buy:m1:1")
    assert "⌛" in view.notice and service._load("test:3").gold == 1000        # already sold: nothing charged
    assert service._load("test:2").gold == 1000 - price
    service.clock.advance(delivery(service) + 1)
    service.act("test:2", "mkt:get")
    assert service._load("test:2").bags == 1


def test_english_screens_have_no_spanish_fallbacks(service, clock):
    two_players(service)
    service.act("test:1", "lang:en")
    service.act("test:2", "lang:en")
    list_potions(service, price=12, n=2)
    service.text("test:1", "/b03")
    service.text("test:1", "x5")
    screens = [service.act("test:1", a) for a in ("mkt", "mkt:cats", "mkt:cat:remedies:0", "mkt:sell:0", "mkt:fill:0",
                                                   "mkt:ask:0", "mkt:mine", "mkt:box", "shop")]
    screens += [service.text("test:1", "/o1"), service.text("test:1", "/b05"), service.act("test:1", "mkt:p:2")]
    service.act("test:2", "mkt:cat:remedies:0")
    screens += [service.text("test:2", "/c1"), service.act("test:2", "mkt:buy:m1:1")]
    clock.advance(delivery(service) + 1)
    screens += [view for _, view in service.tick()]
    screens.append(service.act("test:2", "mkt:get"))
    assert "Market" in screens[0].title and "Deliveries" in text(screens[0])
    for view in screens:
        check_caps(view)
    assert not service.texts.fallbacks.get("en"), service.texts.fallbacks
    assert not service.texts.missing, service.texts.missing


def test_market_codes_never_clash_with_the_old_ones():
    for code in ("/c1", "/s2", "/b07", "/k3", "/o1", "/c_1"):
        assert market_code(code)
        for other in (FAQ_CODE_RE, PLACE_CODE_RE, COORD_RE, SELL_CODE_RE, GEAR_CODE_RE, RESOURCE_CODE_RE, PLAYER_CODE_RE,
                      GUILD_CODE_RE, MEMBER_CODE_RE, FUND_CODE_RE, ZONE_CODE_RE, ARMORY_IN_RE, ARMORY_OUT_RE):
            assert not other.match(code), (code, other.pattern)
    for code in ("/e1", "/q1", "/v02", "/d07", "/ir1", "/go2", "/07", "/j1", "/p1", "/g1", "/m1", "/f02", "/z1", "/a1",
                 "/t1", "/r1", "/stats", "/bio", "/opciones", "/mercado"):
        assert market_code(code) is None, code


def test_typed_price_goes_to_the_draft_and_any_other_button_closes_it(service):
    two_players(service)
    service.act("test:1", "mkt:sell:0")
    service.text("test:1", "/s1")
    service.text("test:1", "17")
    assert service.store.get("market_open", "test:1")["price"] == 17
    service.act("test:1", "hero")
    assert service.store.get("market_open", "test:1") is None
    view = service.text("test:1", "17")
    assert view.kind != "market_draft"


def test_the_daily_report_counts_the_market(service):
    from adapters import reports
    two_players(service)
    list_potions(service, price=20, n=2)
    service.act("test:2", "mkt:buy:m1:1")
    lines = "\n".join(reports.market_lines(service))
    assert "9. MERCADO" in lines and "compras 1" in lines and "unidades 1" in lines and "1 de venta" in lines
    _, report = reports.build(service)
    assert "9. MERCADO" in report
