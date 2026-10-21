"""🗺️ Pergamino de mapa: the 🧭 Explorador's map scroll (D-311 part 5, E-180; how it was applied: D-326, 0.50).

[ES] Pruebas de la parte 5 de D-311 (confirmada por el dueño): "el 🧭 Explorador hace un 🗺️ pergamino con las zonas que exploró
al 50 % o más de una región de 6 × 6 y lo vende al precio que quiera; quien lo usa ve esos colores para siempre". Revisa que:
- sin el rango de map_scroll.rank no se hace (y el botón 🗺️ Pergaminos ni aparece, D-287), y sin map_scroll.min_zones
  zonas al 50 % en la región tampoco; nada se gasta si falta algo;
- el pergamino guarda las zonas correctas: solo las de la región, solo las que el autor investigó él mismo al 50 % o más,
  nunca una 🔥 fogata; gasta la energía y la piel y da experiencia de 🧭 Explorador;
- otro jugador que lo usa ve esas zonas a color (y sus terrenos en la leyenda), pero no sus recursos, ni sus nodos, ni el
  viaje directo; el pergamino se gasta al usarlo;
- se publica en 🏛️ Mercado → 🗺️ Mapas a un precio libre (fuera de la banda de 0,25 a 10 veces), se compra, llega a 📦 Entregas
  y conserva sus zonas; cancelar lo devuelve con sus zonas;
- las pantallas no pasan el tope de botones, se leen en inglés sin textos prestados y /pm1 no choca con otros códigos.
Archivo: tests/test_pergamino_mapa.py · Módulo: M8 Mundo y mapa, M13 Economía · Prueba: engine/service/map_scroll.py
(MapScrollMixin), engine/service/market.py (categoría "maps", la banda, los datos de cada copia) y engine/service/game.py
(_fog_cell, _known_terrains, _zone_view, _map_view, _bag_view, _explorer_unlocks, _explorer_prof_lines, text()).
"""

import re

from conftest import make_hero
from engine.professions import xp_for_rank
from engine.service.game import (COORD_RE, FAQ_CODE_RE, GEAR_CODE_RE, PLACE_CODE_RE, RECIPE_CODE_RE, RECON_CODE_RE,
                                 RESOURCE_CODE_RE, SELL_CODE_RE, button_cap)
from engine.service.gremio import (ARMORY_IN_RE, ARMORY_OUT_RE, FUND_CODE_RE, GUILD_CODE_RE, MEMBER_CODE_RE,
                                   PLAYER_CODE_RE, ZONE_CODE_RE)
from engine.service.map_scroll import SCROLL_CODE_RE
from engine.service.market import market_code

SPOT = (6, 0)          # region (1, 0): from (3, -3) to (8, 2), no bonfire in it


def ids(view):
    return [a.id for a in view.actions]


def text(view):
    return "\n".join([view.notice or ""] + list(view.body) + [a.label for a in view.actions])


def cfg(service):
    return service.content.balance["map_scroll"]


def region(service, x, y):
    """Every zone "x:y" of the region of (x, y), north row first (the same grid the engine uses)."""
    size = cfg(service)["region"]
    half = size // 2
    rx, ry = (x + half) // size, (y + half) // size
    x0, y0 = rx * size - half, ry * size - half
    return [f"{zx}:{zy}" for zy in range(y0 + size - 1, y0 - 1, -1) for zx in range(x0, x0 + size)]


def setup(service, account="test:1", rank=None, at=SPOT, exploration=None, **extra):
    """An explorer of `rank` standing at `at`, with the scroll's materials (×3), full energy and this exploration."""
    hero = service._load(account)
    rank = cfg(service)["rank"] if rank is None else rank
    hero.professions["explorador"] = xp_for_rank(service.content.balance["professions"]["rank_formula"], rank)
    hero.x, hero.y = at
    hero.exploration = dict(exploration or {})
    hero.energy = service.content.balance["energy"]["max"]
    for item_id, n in cfg(service)["materials"].items():
        hero.backpack[item_id] = 3 * int(n)
    for key, value in extra.items():
        setattr(hero, key, value)
    service._save(hero)
    return hero


def explored(service, n, pct=60, at=SPOT):
    """The first `n` zones of the region of `at` at `pct` %."""
    return {key: pct for key in region(service, *at)[:n]}


def make_scroll(service, account="test:1", n=8, at=SPOT):
    setup(service, account, exploration=explored(service, n, at=at), at=at)
    view = service.act(account, "scr:do")
    hero = service._load(account)
    assert hero.map_scrolls, text(view)
    return hero.map_scrolls[-1]


def sell_code(view):
    """The /sN of the first 🗺️ scroll in the 🏷️ Vender list (the starter potions come first)."""
    return next(re.search(r"(/s\d+) 🗺️", line).group(1) for line in view.body if "/s" in line and "🗺️" in line)


def check_caps(view):
    if view.layout:
        assert sum(view.layout) == len(view.actions), (view.kind, view.layout)
    else:
        assert len(view.actions) <= button_cap(view.kind), (view.kind, len(view.actions))
    for action in view.actions:
        assert len(action.id.encode("utf-8")) <= 64


def test_without_the_rank_or_the_minimum_zones_no_scroll_is_made(service):
    make_hero(service)
    setup(service, rank=cfg(service)["rank"] - 1, exploration=explored(service, 12))
    assert "scrolls" not in ids(service.act("test:1", "map"))            # D-287: locked things are not shown
    view = service.act("test:1", "scr:make")
    assert view.kind == "map_scrolls" and "🔒" in view.notice and "scr:make" not in ids(view)
    service.act("test:1", "scr:do")
    hero = service._load("test:1")
    assert not hero.map_scrolls and hero.energy == service.content.balance["energy"]["max"]
    need = cfg(service)["min_zones"]
    few = explored(service, need - 1)
    few[region(service, *SPOT)[need]] = 49                                   # 49 % does not count
    setup(service, exploration=few)
    assert "scrolls" in ids(service.act("test:1", "map"))                    # the rank shows the button
    view = service.act("test:1", "scr:make")
    assert view.kind == "map_scroll_make" and "scr:do" not in ids(view) and "❌" in text(view)
    assert f"{need - 1} (" in text(view)
    service.act("test:1", "scr:do")
    hero = service._load("test:1")
    assert not hero.map_scrolls and "pergamino_mapa" not in hero.backpack
    assert hero.energy == service.content.balance["energy"]["max"] and hero.backpack["piel"] == 3   # nothing spent
    setup(service, exploration=explored(service, need), energy=cfg(service)["energy"] - 1)
    service.act("test:1", "scr:do")
    assert not service._load("test:1").map_scrolls                           # no energy, no scroll
    assert not service.texts.missing, service.texts.missing


def test_making_it_records_the_right_zones_and_pays_the_explorer(service):
    make_hero(service)
    zones = region(service, *SPOT)
    exploration = {zones[0]: 50, zones[1]: 100, zones[2]: 75, zones[3]: 60, zones[4]: 55, zones[5]: 90, zones[6]: 51,
                   zones[7]: 40,                                             # under 50 %: left out
                   "20:20": 100, "0:1": 100}                                 # outside the region: left out
    hero = setup(service, exploration=exploration)
    xp = hero.professions["explorador"]
    view = service.act("test:1", "scrolls")
    assert view.kind == "map_scrolls" and "scr:make" in ids(view)
    make = service.act("test:1", "scr:make")
    assert make.kind == "map_scroll_make" and "scr:do" in ids(make) and "7 (" in text(make)
    start = next(n for n, line in enumerate(make.body) if line.startswith("📍"))
    grid = make.body[start + 1:start + 1 + cfg(service)["region"]]          # the region as the scroll would draw it
    assert all(len(re.findall(r".\ufe0f?", row)) == cfg(service)["region"] for row in grid), grid
    assert make.body[start + 1 + cfg(service)["region"]].startswith("🧍")   # then its legend
    done = service.act("test:1", "scr:do")
    hero = service._load("test:1")
    assert len(hero.map_scrolls) == 1 and hero.backpack["pergamino_mapa"] == 1
    data = hero.map_scrolls[0]
    assert set(data["zones"]) == set(zones[:7]) and data["by"] == "Lyra" and data["id"] == "p1"
    assert data["center"] == [6, 0] and data["size"] == cfg(service)["region"]
    assert hero.energy == service.content.balance["energy"]["max"] - cfg(service)["energy"]
    assert hero.backpack["piel"] == 2
    assert hero.professions["explorador"] == xp + cfg(service)["explorer_xp"]
    assert "🗺️" in done.notice and "/pm1" in text(done)
    assert service._load("test:1").exploration == exploration              # making it never touches what you explored
    second = service.act("test:1", "scr:do")                               # another copy: its own record and number
    assert [s["id"] for s in service._load("test:1").map_scrolls] == ["p1", "p2"] and "/pm2" in text(second)
    assert service._load("test:1").backpack["pergamino_mapa"] == 2


def test_bonfires_never_go_in_the_scroll(service):
    make_hero(service)
    setup(service, at=(12, 0), exploration={key: 100 for key in region(service, 12, 0)})
    service.act("test:1", "scr:do")
    data = service._load("test:1").map_scrolls[0]
    assert "12:0" not in data["zones"] and len(data["zones"]) == cfg(service)["region"] ** 2 - 1


def test_another_player_who_uses_it_sees_those_zones_in_colour_and_nothing_more(service):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    data = make_scroll(service)
    lyra = service._load("test:1")
    service._scroll_take(lyra, data["id"])
    service._save(lyra)
    bram = setup(service, "test:2", rank=1, at=(0, 0))
    service._scroll_add(bram, data)
    service._save(bram)
    blank = service._fog_stage(0)["mark"]
    bram = service._load("test:2")
    assert all(service._fog_cell(bram, *map(int, key.split(":"))) == blank for key in data["zones"])
    view = service.act("test:2", "map")
    assert "scrolls" in ids(view) and any("(1)" in a.label for a in view.actions)      # he carries one: the button shows
    assert "/pergaminos" in text(service.act("test:2", "bag"))
    scrolls = service.text("test:2", "/pergaminos")
    assert scrolls.kind == "map_scrolls" and "/pm1" in text(scrolls) and "🆕 8" in text(scrolls)
    assert "scr:make" not in ids(scrolls)                                     # rank 1: he cannot make one
    detail = service.text("test:2", "/pm1")
    assert detail.kind == "map_scroll" and f"scr:use:{data['id']}" in ids(detail) and "Lyra" in text(detail)
    used = service.act("test:2", f"scr:use:{data['id']}")
    assert used.kind == "map_scrolls" and "8" in used.notice
    bram = service._load("test:2")
    for key in data["zones"]:
        x, y = map(int, key.split(":"))
        assert service._fog_cell(bram, x, y) == service.content.biomes[service._zone(x, y).biome]["color"], key
        assert service._known_resources(bram, x, y) == []                    # only the colour: no resources
        assert not bram.remembers(x, y) and service._known_pct(bram, x, y) == 0   # no travel rights, no %
    other = next(key for key in region(service, *SPOT) if key not in data["zones"])
    assert service._fog_cell(bram, *map(int, other.split(":"))) == blank      # the rest of the region stays blank
    terrains = {service._zone(*map(int, key.split(":"))).biome for key in data["zones"]}
    assert terrains <= set(service._known_terrains(bram))                     # their terrains join the legend
    assert not service.store.get("nodes", "test:2")                           # no resource nodes either
    x, y = map(int, data["zones"][0].split(":"))
    bram.x, bram.y = x, y
    service._save(bram)
    assert "🗺️" in text(service.act("test:2", "home"))                       # 📍 Zona says why it is in colour
    assert not service.texts.missing, service.texts.missing


def test_the_scroll_is_spent_when_used(service):
    make_hero(service)
    data = make_scroll(service)
    assert service._load("test:1").backpack["pergamino_mapa"] == 1
    view = service.act("test:1", f"scr:use:{data['id']}")
    hero = service._load("test:1")
    assert not hero.map_scrolls and "pergamino_mapa" not in hero.backpack
    assert "0" in view.notice                                                 # the author already saw them in colour
    again = service.act("test:1", f"scr:use:{data['id']}")
    assert again.kind == "map_scrolls" and "⌛" in again.notice               # gone: nothing happens twice
    assert set(data["zones"]) <= set(service._load("test:1").charted)        # for ever, even if exploration changed
    assert service.text("test:1", "/pm1").kind == "map_scrolls"              # the old code points nowhere now


def test_it_is_sold_and_bought_on_the_market_and_keeps_its_zones(service, clock):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    data = make_scroll(service)
    setup(service, "test:2", rank=1, at=(0, 0), gold=20000)
    lyra = service._load("test:1")
    lyra.x, lyra.y, lyra.gold = 0, 0, 0                                       # trading happens at a 🔥 bonfire
    service._save(lyra)
    sell = service.act("test:1", "mkt:sell:0")
    assert "🗺️" in text(sell) and "Lyra" in text(sell)
    draft = service.text("test:1", sell_code(sell))
    assert draft.kind == "market_draft" and not any(a.id.startswith("mkt:q:") for a in draft.actions)   # one copy
    low, high = cfg(service)["price_min"], cfg(service)["price_max"]
    assert f"{service._money(low)}" in text(draft) and f"{service._money(high)}" in text(draft)
    typed = service.text("test:1", "5000 x3")                                # free price, far above 10 × its reference
    assert not typed.notice and service.store.get("market_open", "test:1")["price"] == 5000
    service.act("test:1", "mkt:ok")
    lyra = service._load("test:1")
    assert not lyra.map_scrolls and "pergamino_mapa" not in lyra.backpack
    order = service.store.get("market_order", "m1")
    assert order["n"] == 1 and order["price"] == 5000 and order["scroll"]["zones"] == data["zones"]
    cats = service.act("test:2", "mkt:cats")
    assert "mkt:cat:maps:0" in ids(cats)
    check_caps(cats)
    offers = service.act("test:2", "mkt:cat:maps:0")
    assert "/c1" in text(offers) and "Lyra" in text(offers)
    offer = service.text("test:2", "/c1")
    assert offer.kind == "market_offer" and "🆕 8" in text(offer)
    service.act("test:2", "mkt:buy:m1:1")
    tax = int(5000 * service.content.balance["market"]["tax"] + 0.5)
    assert service._load("test:2").gold == 15000 and service._load("test:1").gold == 5000 - tax
    clock.advance(service.content.balance["market"]["delivery_minutes"] * 60 + 1)
    service.act("test:2", "mkt:get")
    bram = service._load("test:2")
    assert len(bram.map_scrolls) == 1 and bram.backpack["pergamino_mapa"] == 1
    assert bram.map_scrolls[0]["zones"] == data["zones"] and bram.map_scrolls[0]["by"] == "Lyra"
    service.act("test:2", f"scr:use:{data['id']}")
    bram = service._load("test:2")
    x, y = map(int, data["zones"][0].split(":"))
    assert service._fog_cell(bram, x, y) == service.content.biomes[service._zone(x, y).biome]["color"]


def test_the_price_band_of_a_scroll_and_a_cancel_brings_it_back(service):
    make_hero(service)
    data = make_scroll(service)
    hero = service._load("test:1")
    hero.x, hero.y = 0, 0
    service._save(hero)
    service.text("test:1", sell_code(service.act("test:1", "mkt:sell:0")))
    view = service.text("test:1", "999999")
    assert service.store.get("market_open", "test:1")["price"] == cfg(service)["price_max"] and view.notice
    service.text("test:1", "0")
    assert service.store.get("market_open", "test:1")["price"] == cfg(service)["price_min"]
    service.act("test:1", "mkt:ok")
    assert not service._load("test:1").map_scrolls
    service.act("test:1", "mkt:x:m1")                                        # ❌ cancel: it waits in 📦 Entregas
    box = service._mkt_box("test:1")
    assert box and box[0]["scroll"]["zones"] == data["zones"]
    service.act("test:1", "mkt:get")
    hero = service._load("test:1")
    assert [s["id"] for s in hero.map_scrolls] == [data["id"]] and hero.backpack["pergamino_mapa"] == 1


def test_the_explorer_rank_announces_and_lists_the_scroll(service):
    make_hero(service)
    rank = cfg(service)["rank"]
    setup(service, rank=rank - 1)
    assert "🗺️ pergaminos" not in text(service.text("test:1", "/explorador"))
    hero = service._load("test:1")
    need = xp_for_rank(service.content.balance["professions"]["rank_formula"], rank) - hero.professions["explorador"]
    lines = service._prof_gain(hero, "explorador", need)
    assert any("pergaminos de mapa" in line for line in lines)               # the rank-up says it opens
    service._save(hero)
    assert f"✅{rank} 🗺️ pergaminos" in text(service.text("test:1", "/explorador"))


def test_screens_keep_their_buttons_and_read_in_english(service, clock):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    service.act("test:1", "lang:en")
    service.act("test:2", "lang:en")
    data = make_scroll(service)
    make_scroll(service)
    make_scroll(service)
    screens = [service.act("test:1", a) for a in ("map", "scrolls", "scr:make", f"scr:v:{data['id']}", "bag")]
    screens.append(service.text("test:1", "/scrolls"))
    screens.append(service.text("test:1", "/pm2"))
    screens.append(service.text("test:1", "/pm9"))
    hero = service._load("test:1")
    hero.x, hero.y = 0, 0
    service._save(hero)
    sell = service.act("test:1", "mkt:sell:0")
    screens += [sell, service.text("test:1", sell_code(sell)), service.act("test:1", "mkt:ok")]
    setup(service, "test:2", rank=1, at=(0, 0), gold=1000)
    screens += [service.act("test:2", "mkt:cats"), service.act("test:2", "mkt:cat:maps:0"), service.text("test:2", "/c1"),
                service.act("test:2", "mkt:buy:m1:1")]
    clock.advance(service.content.balance["market"]["delivery_minutes"] * 60 + 1)
    screens += [view for _, view in service.tick()]
    screens.append(service.act("test:2", "mkt:get"))
    sid = service._load("test:2").map_scrolls[0]["id"]
    screens.append(service.act("test:2", f"scr:use:{sid}"))
    screens.append(service.act("test:1", f"scr:use:{data['id']}"))
    assert "scroll" in text(screens[1]).lower()
    for view in screens:
        check_caps(view)
    assert not service.texts.fallbacks.get("en"), service.texts.fallbacks
    assert not service.texts.missing, service.texts.missing


def test_the_scroll_code_never_clashes_with_the_others():
    for code in ("/pm1", "/pm_2", "/pm12", "/pm3@LostRealmsbot"):
        assert SCROLL_CODE_RE.match(code)
        assert market_code(code) is None
        for other in (FAQ_CODE_RE, PLACE_CODE_RE, COORD_RE, SELL_CODE_RE, GEAR_CODE_RE, RESOURCE_CODE_RE, RECIPE_CODE_RE,
                      RECON_CODE_RE, PLAYER_CODE_RE, GUILD_CODE_RE, MEMBER_CODE_RE, FUND_CODE_RE, ZONE_CODE_RE,
                      ARMORY_IN_RE, ARMORY_OUT_RE):
            assert not other.match(code), (code, other.pattern)
    for code in ("/p1", "/m1", "/pergaminos", "/r1", "/rc1", "/c1"):
        assert not SCROLL_CODE_RE.match(code), code


def test_heroes_saved_before_load_with_no_scrolls(service):
    make_hero(service)
    data = service.store.get("hero", "test:1")
    data.pop("map_scrolls", None)
    data.pop("charted", None)
    service.store.put("hero", "test:1", data)
    hero = service._load("test:1")
    assert hero.map_scrolls == [] and hero.charted == [] and "pergamino_mapa" not in hero.backpack
    for screen in ("map", "bag", "home", "scrolls"):
        assert service.act("test:1", screen).kind
    assert not service.texts.missing
