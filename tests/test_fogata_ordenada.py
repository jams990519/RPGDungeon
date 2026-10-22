"""The bonfire tidied up (0.33): one mission a day per character, a trader that buys and sells, an inn that takes its
time, ⚙️ Opciones without automatic fights and with 💬 Feedback, the journal that goes back where it was opened, and
the daily player report for the team (D-258, D-259, D-260).

[ES] Pruebas del orden de la fogata (pedido del dueño, 17-oct-2026):
- 📜 Tablón: cada personaje da un encargo por día; lo que se junta se entrega; lo que se cuenta se cobra hablando; se
  cobra en el Claro o en tu propio campamento (la fogata no se controla); el de cocina de Marta solo con 🍲 Cocina.
- 🛒 Mercader con 🛒 Comprar y 💱 Vender; vender todo de una cosa con su código (/v02).
- 🛏️ Posada que tarda según la vida que falta (de 0 a llena en 1 hora).
- ⚙️ Opciones: sin ⚔️ Peleas automáticas ni 🧪 Pociones; 🩹 Retirarse, 🌐 Idioma, 💬 Feedback, ❓ Dudas (D-297) y ↩️ Volver; el mensaje de
  feedback se guarda y sale una sola vez para el chat de informes.
- 📔 Diario: ↩️ Volver va al campamento si lo abriste desde 📜 Tablón, y al héroe si lo abriste desde 👤 Héroe.
- El informe de jugadores (adapters/reports.py): genérico, sin nombres, uno por día, con la foto del día.
Archivo: tests/test_fogata_ordenada.py · Módulo: M7 Historia, M10 Economía, M20 Telemetría · Prueba:
engine/service/story.py (_daily_ids, _claim_daily, _can_meet, _npc_view, _board_view, _journal_view),
engine/service/game.py (_shop_view, _shop_sell_view, _sell_code, _inn_seconds, _options_view, _feedback_view,
_save_feedback, take_feedback), adapters/reports.py.
"""

from conftest import make_hero
from test_camps import found_at

from adapters import reports
from engine.hero import hero_stats


def body(view):
    return "\n".join(view.body)


def ids(view):
    return [a.id for a in view.actions]


def carry(service, account="test:1", **items):
    hero = service._load(account)
    hero.backpack.update(items)
    service._save(hero)


def test_every_character_gives_one_mission_a_day(service):
    make_hero(service)
    hero = service._load("test:1")
    picked = service._daily_ids(hero)
    givers = [service._story_data()["daily"][tid]["giver"] for tid in picked]
    assert sorted(givers) == sorted(service._npc_defs())
    assert "d_cocina" not in picked and "d_forja" not in picked               # they need 🍲 Cocina or a crafting profession
    board = service.act("test:1", "board")
    assert sum(1 for line in board.body if line.startswith(("▫️ ", "🎁 "))) == len(picked)


def test_a_delivery_is_handed_over_and_paid_when_you_talk(service):
    make_hero(service)
    hero = service._load("test:1")
    tid = next(t for t in service._daily_ids(hero) if service._story_data()["daily"][t]["goal"]["kind"] == "deliver")
    tdef = service._story_data()["daily"][tid]
    nid, need = tdef["giver"], tdef["goal"]["items"]
    view = service.act("test:1", f"npc:{nid}")
    assert f"dly:{nid}" in ids(view) and "Su encargo de hoy" in body(view)
    assert "Te falta" in service.act("test:1", f"dly:{nid}").notice                 # nothing taken without all of it
    carry(service, **{i: n + 2 for i, n in need.items()})
    gold = service._load("test:1").gold
    view = service.act("test:1", f"dly:{nid}")
    hero = service._load("test:1")
    assert "Encargo cumplido" in view.notice and hero.gold > gold
    assert all(hero.backpack.get(i) == 2 for i in need)                           # it took exactly what it asked
    assert "Ya cumpliste" in body(view)
    assert service.act("test:1", f"dly:{nid}").notice is None                     # paid once


def test_a_counted_mission_is_ready_then_cashed_in(service):
    make_hero(service)
    hero = service._load("test:1")
    odo = next(t for t in service._daily_ids(hero) if service._story_data()["daily"][t]["giver"] == "odo")
    goal = service._story_data()["daily"][odo]["goal"]
    if goal["kind"] == "deliver":                                                 # today Odo wants clay: count another one
        record = service._daily(hero)
        record["ids"] = [t for t in record["ids"] if t != odo] + ["d_venta"]
        service._save(hero)
        odo, goal = "d_venta", service._story_data()["daily"]["d_venta"]["goal"]
    hero = service._load("test:1")
    lines = service._daily_event(hero, goal["kind"], {"n": goal.get("n", 1), "lejania": 3, "x": 3, "y": 0})
    assert any("está listo" in line for line in lines)
    service._save(hero)
    view = service.act("test:1", "dly:odo")
    assert "Encargo cumplido" in view.notice


def test_missions_are_cashed_in_at_your_own_camp_not_elsewhere(service):
    make_hero(service)
    hero = service._load("test:1")
    tid = next(t for t in service._daily_ids(hero) if service._story_data()["daily"][t]["goal"]["kind"] == "deliver")
    tdef = service._story_data()["daily"][tid]
    found_at(service, "test:1", 6, 0)
    carry(service, **{i: n for i, n in tdef["goal"]["items"].items()})
    assert service._can_meet(service._load("test:1"))
    assert "Encargo cumplido" in service.act("test:1", f"dly:{tdef['giver']}").notice
    hero = service._load("test:1")
    hero.x, hero.y = 2, 2                                                          # out in the wild
    service._save(hero)
    assert not service._can_meet(service._load("test:1"))


def test_martas_cooking_mission_needs_cooking(service):
    make_hero(service)
    hero = service._load("test:1")
    assert not service._task_eligible(hero, service._story_data()["daily"]["d_cocina"])
    hero.learned = ["cocina"]
    assert service._task_eligible(hero, service._story_data()["daily"]["d_cocina"])


def test_the_trader_has_buy_and_sell_and_codes_sell_everything_of_a_thing(service):
    make_hero(service)
    view = service.act("test:1", "shop")
    assert ids(view) == ["shop:buy", "shop:sell", "mkt", "claro"]          # D-320 (0.46): 🏛️ Mercado entre jugadores
    assert service.act("test:1", "shop:buy").kind == "shop_buy"
    carry(service, piedra=10, carne=3, tablon=2)
    sell = service.act("test:1", "shop:sell")
    text = body(sell)
    assert "/v02" in text and "🍖" in text and "/v11" in text                    # stone, food and refined goods can be sold
    gold = service._load("test:1").gold
    view = service.text("test:1", "/v02")
    hero = service._load("test:1")
    assert "piedra" not in hero.backpack and hero.gold > gold and view.kind == "shop_sell"
    assert "/v99" in service.text("test:1", "/v99").notice


def test_the_inn_takes_time_by_the_life_you_lack(service):
    make_hero(service)
    hero = service._load("test:1")
    max_hp = hero_stats(service._kit(hero), hero.level)["max_hp"]
    hero.hp = 1
    service._save(hero)
    assert 7 * 60 <= service._inn_seconds(service._load("test:1")) <= 7.5 * 60      # D-284: almost empty, about 7,5 min (30 / 4)
    hero = service._load("test:1")
    hero.hp = max_hp // 2
    service._save(hero)
    assert service._inn_seconds(service._load("test:1")) == 5 * 60                  # half (3,75 min): never under inn.min_minutes
    hero = service._load("test:1")
    hero.hp, hero.gold = 1, 50
    service._save(hero)
    view = service.act("test:1", "inn")
    assert service._load("test:1").activity["kind"] == "rest" and view.notice


def test_options_without_automatic_fights_and_with_feedback(service):
    make_hero(service)
    view = service.act("test:1", "options")
    assert ids(view) == ["opt:retreat", "lang", "fb", "dudas@options", "oath", "home"]   # D-297: ❓ Dudas; D-336: 💀 Muerte permanente
    assert "Peleas automáticas" not in body(view) and "Pociones" not in body(view)
    hero = service._load("test:1")
    hero.options["fights"] = "auto"                                                # an old choice no longer turns them on
    service._save(hero)
    assert not service._auto_on(service._load("test:1"))
    ask = service.act("test:1", "fb")
    assert ask.kind == "feedback" and ask.expects_text
    thanks = service.text("test:1", "No encuentro dónde vender")
    assert thanks.kind == "options" and "Gracias" in thanks.notice
    notes = service.take_feedback()
    assert len(notes) == 1 and notes[0]["text"] == "No encuentro dónde vender" and notes[0]["hero"] == "Lyra"
    assert service.take_feedback() == []                                           # sent once
    service.act("test:1", "fb")
    service.act("test:1", "home")                                                  # leaving cancels it
    assert service.text("test:1", "hola").kind != "options" and service.take_feedback() == []


def test_the_journal_goes_back_where_it_was_opened(service):
    make_hero(service)
    from_board = service.act("test:1", "cjournal")
    assert from_board.actions[-1].id == "claro"
    service.act("test:1", "factions")
    assert service.act("test:1", "journal").actions[-1].id == "claro"            # its own screens keep the way back
    from_hero = service.act("test:1", "hjournal")
    assert from_hero.actions[-1].id == "hero"


def test_the_daily_player_report_is_generic_and_once_a_day(service, clock):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    service.act("test:1", "home")
    service.act("test:2", "home")
    assert reports.due(service)
    name, text = reports.build(service)
    assert name.startswith("informe-jugadores-") and name.endswith(".txt")
    assert "Lyra" not in text and "Bram" not in text and "test:" not in text      # generic: no names, no accounts
    assert "Héroes creados: 2" in text and "primer informe" in text
    reports.mark_sent(service)
    assert not reports.due(service)
    clock.advance(86400)
    hero = service._load("test:1")
    hero.professions["minero"] = 40
    service._save(hero)
    service.act("test:1", "home")
    assert reports.due(service)
    _, text = reports.build(service)
    assert "Unidades recolectadas: hoy 40" in text
