"""0.42: 🪓 Talar (chop wood, D-305) and 🩹 rest first (D-308).

🪓 Talar is a gathering batch that takes only 🪵 wood: the same energy, minutes and amounts as 🧺 Recolectar, the own-land
bonus, the 🪓 Lumberjack and a wood node's ×2; only the wood is depleted and the batch stops when it runs out. Its button sits
next to 🧺 Recolectar in 🧭 Explorar wherever the zone has wood (D-314: 5 buttons, layout [1, 2, 2]). With the hero's life
under its 🩹 Retirarse % (⚙️ Opciones) no batch of exploring, gathering or chopping starts (fights are not touched).

[ES] Pruebas de la 0.42. 🪓 Talar (D-305, confirmada por el dueño el 20-oct-2026): solo da 🪵 madera, solo agota la madera,
sube al 🪓 Leñador, rinde ×2 en un nodo de madera (no trabaja un nodo de otro recurso), no se ofrece donde no hay madera ni
en la guarida, va en lotes como recolectar y se corta cuando la madera se agota o se llena la mochila; también en inglés.
🩹 Retirarse (D-308, confirmada el 20-oct-2026): con la vida bajo el % no empieza un lote de explorar, recolectar ni talar
(pantalla 🩹 Descansa primero con 🛏️ Posada, 🩺 Salud, ⚙️ Opciones y ↩️ Volver, sin cobrar nada); por encima, sí; las
peleas siguen igual. Los recursos que vuelven ×3 (D-305.2) se prueban en tests/test_resources.py.
"""

import re

import pytest

from conftest import make_hero
from engine.core import Rng
from engine.hero import hero_stats
from test_camps import place
from test_hunt import wild

MIN = 60


def ids(view):
    return [a.id for a in view.actions]


def run(service, clock, account="test:1", hours=6):
    """Let a batch run to its end; returns the pushed notices of `account`."""
    pushes = []
    for _ in range(hours):
        clock.advance(3600)
        pushes += [view.notice or "" for acc, view in service.tick() if acc == account]
    return "\n".join(pushes)


def set_life(service, clock, pct, account="test:1"):
    """Leave the hero at `pct` % of its life, with no regeneration pending."""
    hero = service._load(account)
    max_hp = hero_stats(service._kit(hero), hero.level)["max_hp"]
    hero.hp = max(1, int(max_hp * pct / 100))
    hero.last_regen_at = clock.now()
    service._save(hero)
    return hero.hp, max_hp


# ---------------------------------------------------------------- 🪓 Talar (D-305)

def test_talar_sits_next_to_gather_where_the_zone_has_wood(service):
    make_hero(service)
    menu = service.act("test:1", "explore_menu")
    assert ids(menu) == ["explore", "gather", "chop", "hunt", "map"] and menu.layout == [1, 2, 2]   # D-314: 3 rows
    labels = [a.label for a in menu.actions]
    assert labels[1].startswith("🧺 Recolectar") and labels[2].startswith("🪓 Talar")
    screen = service.act("test:1", "chop")
    assert screen.kind == "batch" and screen.title == "🪓 Talar" and screen.layout == [len(screen.actions) - 1, 1]
    assert ids(screen)[0] == "do:chop:5" and ids(screen)[-1] == "explore_menu"
    assert ids(service.act("test:1", "amt:chop:0")) == ids(screen)
    assert not service.texts.missing


def test_talar_is_not_offered_without_wood_nor_in_the_lair(content, service, monkeypatch):
    make_hero(service)
    monkeypatch.setitem(content.balance["resources"]["fixed"], "0:0", {"fibra": 0.8})   # a bonfire without wood
    menu = service.act("test:1", "explore_menu")
    assert ids(menu) == ["explore", "gather", "hunt", "map"] and not menu.layout
    view = service.act("test:1", "chop")                       # an old button: a notice, nothing spent
    assert view.kind == "explore_menu" and "no hay madera" in view.notice
    assert service._load("test:1").energy == 50
    monkeypatch.setattr(service, "_is_lair", lambda x, y: True)
    lair = service.act("test:1", "explore_menu")
    assert "chop" not in ids(lair) and "gather" not in ids(lair)
    assert service.act("test:1", "do:chop:5").kind == "explore_menu" and service._load("test:1").activity is None


def test_talar_gives_only_wood_and_depletes_only_wood(service, clock):
    make_hero(service)                                          # the Claro: 🪵 madera and 🧵 fibra
    service.content.balance["hero"]["backpack"]["per_type"] = 100      # test only: 20 rounds never reach a type's cap (D-338)
    view = service.act("test:1", "do:chop:20")
    assert view.kind == "activity" and view.title == "🪓 Talando" and "talar 20 veces" in view.notice
    hero = service._load("test:1")
    assert hero.activity["kind"] == "gather" and hero.activity["only"] == "madera" and hero.energy == 49
    summary = run(service, clock)
    hero = service._load("test:1")
    materials = {i for i in hero.backpack if service.content.items[i]["kind"] == "material"}
    assert materials == {"madera"} and hero.backpack["madera"] >= 20      # every unit of every round is wood
    assert "🪓 Talaste 20 veces" in summary and "✨ Talar te enseñó" in summary
    stock = service._stock(0, 0)
    assert stock["fibra"] == 1.0 and stock["madera"] < 1.0                 # only the wood went down


def test_talar_raises_the_lumberjack(service, clock, every_profession_known):
    make_hero(service)
    service.act("test:1", "do:chop:10")
    summary = run(service, clock, hours=3)
    hero = service._load("test:1")
    assert hero.professions.get("lenador", 0) >= hero.backpack["madera"] > 0      # 1 profession xp per unit (or more)
    assert "🪓 Leñador +" in summary and "Minero" not in summary and "Herbolario" not in summary


def _one_round(service, node):
    """One round of 🪓 Talar at the Claro with a fixed draw, with `node` as the zone's resource node."""
    service.store.put("stock", "0:0", {"levels": {"madera": 1.0, "fibra": 1.0}, "at": service.clock.now()})
    hero = service._load("test:1")
    hero.backpack = {}
    original = type(service)._node_main
    service._node_main = (lambda x, y: node) if node else (lambda x, y: original(service, x, y))
    activity = {"kind": "gather", "only": "madera", "got": {}, "log": [], "until": 1.0, "done": 1}
    service._gather_step(hero, service._zone(0, 0), Rng(7), activity)
    del service._node_main
    return activity, service._stock(0, 0)


def test_talar_on_a_wood_node_doubles_and_never_works_another_node(service):
    make_hero(service)
    plain, plain_stock = _one_round(service, None)
    wood, wood_stock = _one_round(service, "madera")
    other, other_stock = _one_round(service, "fibra")
    units = plain["got"]["madera"]
    assert units >= 1 and wood["got"]["madera"] == 2 * units                   # nodes.yield_mult 2: each unit counts twice
    assert 1.0 - wood_stock["madera"] == pytest.approx((1.0 - plain_stock["madera"]) / 2)   # ...and depletes half
    assert wood["node"]["extra"] == units
    assert other["got"] == plain["got"] and "node" not in other                 # a fibra node is not worked by chopping
    assert other_stock["fibra"] == 1.0


def test_talar_stops_when_the_wood_runs_out_and_waits_while_it_is_out(service, clock):
    make_hero(service)
    cfg = service.content.balance["stock"]
    service.store.put("stock", "0:0", {"levels": {"madera": cfg["min_yield"] + 0.05, "fibra": 1.0}, "at": clock.now()})
    service.act("test:1", "do:chop:20")
    summary = run(service, clock, hours=2)
    hero = service._load("test:1")
    done = int(re.search(r"Talaste (\d+) ve", summary).group(1))
    assert hero.activity is None and 1 <= done < 20 and "se agotó" in summary     # it stopped before paying a round for nothing
    assert hero.backpack["madera"] >= done and "fibra" not in hero.backpack       # no round came back empty
    service.store.put("stock", "0:0", {"levels": {"madera": 0.1, "fibra": 1.0}, "at": clock.now()})
    service.view("test:1")
    energy = service._load("test:1").energy
    view = service.act("test:1", "chop")
    assert view.kind == "explore_menu" and "madera" in view.notice and service._load("test:1").energy == energy
    assert service.act("test:1", "gather").kind == "batch"      # the fibre is still there: 🧺 Recolectar works


def test_talar_stops_with_a_full_backpack(service, clock):
    # [ES] D-338 (0.62): 🪓 Talar se corta cuando la 🪵 madera llega al tope de su tipo (30)
    make_hero(service)
    hero = service._load("test:1")
    hero.backpack["madera"] = service._pack_per_type() - 1
    service._save(hero)
    service.act("test:1", "do:chop:10")
    summary = run(service, clock, hours=3)
    hero = service._load("test:1")
    assert hero.backpack["madera"] == service._pack_per_type() and hero.activity is None and "mochila" in summary.lower()
    assert service.act("test:1", "chop").kind == "explore_menu"                # full: it does not start


def test_talar_shows_who_is_chopping(service):
    make_hero(service)
    service.act("test:1", "do:chop:5")
    hero = service._load("test:1")
    assert service._status_text(hero) == "🪓 Talando"
    make_hero(service, "test:2", "Bram")
    assert any("🪓 talando" in line for line in service.act("test:2", "home").body)


def test_talar_in_english(service, clock):
    service.view("test:1")
    service.act("test:1", "lang:en")
    service.text("test:1", "Lyra")
    service.act("test:1", "grp:guerrero")
    service.act("test:1", "cls:guerrero_dps")
    menu = service.act("test:1", "explore_menu")
    labels = [a.label for a in menu.actions]
    assert labels[1].startswith("🧺 Gather") and labels[2].startswith("🪓 Chop wood")
    assert service.act("test:1", "chop").title == "🪓 Chop wood"
    assert "You'll chop wood 5 times" in service.act("test:1", "do:chop:5").notice
    summary = run(service, clock, hours=1)
    assert "🪓 You chopped wood 5 times" in summary
    assert not service.texts.missing


# ---------------------------------------------------------------- 🩹 rest first (D-308)

def test_low_life_does_not_start_exploring_gathering_or_chopping(service, clock):
    make_hero(service)
    hp, max_hp = set_life(service, clock, 20)                  # under the default 🩹 Retirarse (30 %)
    for kind in ("explore", "gather", "chop"):
        for action in (kind, f"do:{kind}:5"):
            view = service.act("test:1", action)
            assert view.kind == "retreat" and view.title == "🩹 Descansa primero", action
            text = "\n".join(view.body)
            assert f"{hp}/{max_hp}" in text and "Retirarse con menos de 30 %" in text
            assert ids(view) == ["inn", "health", "options", "explore_menu"]          # at a 🔥 Fogata: the inn first
    hero = service._load("test:1")
    assert hero.energy == 50 and hero.activity is None          # nothing is spent
    assert service.act("test:1", "health").kind == "health"
    assert service.act("test:1", "inn").kind == "activity"      # the existing rest works from there
    assert not service.texts.missing


def test_above_the_limit_batches_start_and_the_limit_follows_options(service, clock):
    make_hero(service)
    set_life(service, clock, 40)
    assert service.act("test:1", "explore").kind == "batch"     # 40 % is above 30 %
    service.act("test:1", "opt:retreat")                         # 30 → 50 %
    view = service.act("test:1", "gather")
    assert view.kind == "retreat" and "50 %" in "\n".join(view.body)
    set_life(service, clock, 60)
    assert service.act("test:1", "do:chop:5").kind == "activity"


def test_rest_first_away_from_a_bonfire_and_fights_untouched(service, clock):
    make_hero(service)
    x, y = wild(service)
    place(service, "test:1", x, y)
    set_life(service, clock, 10)
    view = service.act("test:1", "explore")
    assert view.kind == "retreat" and ids(view) == ["health", "options", "explore_menu"]   # no inn out here
    fight = service.act("test:1", "prey")                       # 🏹 Cazar a mano: fights are not touched (D-308)
    assert fight.kind == "combat" and service.store.get("combat", "test:1") is not None
