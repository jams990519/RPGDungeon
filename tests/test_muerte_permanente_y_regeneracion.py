"""0.60: the 💀 optional permadeath with its 🪦 hall (D-147) and the professions that speed up a zone's regrowth (D-145).

[ES] Pruebas de la 0.60 (cómo se aplicó: D-336, provisional). 💀 Muerte permanente: el botón en ⚙️ Opciones, la doble
confirmación (en orden, con tiempo, y otro botón la cancela), hasta el nivel 10, que no se apaga, que no la jura un fundador
ni un líder de gremio y que quien la juró no crea un gremio ni recibe el liderazgo. Una caída SIN 💀 sigue igual (malherido,
pierde el 10 % de las monedas y sigue en el juego). Una caída CON 💀 (a mano o en un lote automático) anota el 🪦 Salón, guarda
el héroe entero en su archivo, cancela sus órdenes del 🏛️ Mercado y sus encargos de reparación hacia él, lo saca de su
campamento y su gremio, publica HeroFellForever, avisa a los compañeros y deja crear un héroe nuevo con las mismas ⚙️ Opciones
y los 💎 diamantes; ninguna otra cuenta cambia. Los títulos de prestigio, la marca 💀, ❓ /d65 y el aviso del parche. 🌱 Los
oficios: quien recolecta con su oficio aprendido hace que ese recurso vuelva más rápido en la zona por 24 h, se ve en
📍 Zona y vence. Todo en español y en inglés, sin textos faltantes.
"""

import pytest

from conftest import make_hero
from engine.combat import make_combat
from engine.core import HeroFellForever, Rng
from engine.hero import hero_stats
from engine.professions import xp_for_rank
from engine.service.game import button_cap
from test_camps import old_camp_at, place
from test_gremio_desde_el_inicio import join, new_gremio
from test_hunt import wild

MINUTE = 60
HOUR = 3600
DAY = 86400


def ids(view):
    return [a.id for a in view.actions]


def text(view):
    return "\n".join([view.title or "", *(view.body or []), view.notice or ""])


def swear(service, account="test:1"):
    """Go through the two confirmations; returns the last screen."""
    assert "oath:ask" in ids(service.act(account, "oath"))
    assert ids(service.act(account, "oath:ask")) == ["oath:ask2", "oath"]
    assert ids(service.act(account, "oath:ask2")) == ["oath:swear", "oath"]
    return service.act(account, "oath:swear")


def enemy_id(service):
    return next(eid for eid, e in service.content.enemies.items() if not e.get("boss"))


def open_fight(service, account="test:1"):
    hero = service._load(account)
    eid = enemy_id(service)
    state = make_combat(eid, service.content.enemies[eid], 1, service._kit(hero), 7)
    service.store.put("combat", account, state)
    return state


@pytest.fixture
def losing(monkeypatch):
    """Every round of a fight by hand ends in a defeat (the rest of the fight's end is the real one)."""
    def lose(state, hero, cdef, choice, ctx):
        state["outcome"] = "defeat"
        state["log"] = ["⚔️ round"]
        hero.hp = 0
    monkeypatch.setattr("engine.service.game.resolve_round", lose)


def lose_by_hand(service, account="test:1"):
    open_fight(service, account)
    return service.act(account, "atk")


# ---------------------------------------------------------------- ⚙️ Opciones and the double confirmation

def test_options_show_the_permadeath_button_in_both_languages(service):
    make_hero(service)
    view = service.act("test:1", "options")
    assert ids(view) == ["opt:retreat", "lang", "fb", "dudas@options", "oath", "home"]
    assert len(view.actions) <= button_cap("options") == 6 and view.layout == [2, 2, 1, 1]
    assert "💀 Muerte permanente: apagada." in view.body and view.actions[4].label == "💀 Muerte permanente"
    screen = service.act("test:1", "oath")
    assert screen.kind == "oath" and ids(screen) == ["oath:ask", "fallen", "options"]
    assert "hasta el nivel 10" in text(screen) and "«Superviviente de hierro»" in text(screen) and "Estado: apagada." in screen.body
    service.act("test:1", "lang:en")
    view = service.act("test:1", "options")
    assert "💀 Permadeath: off." in view.body and view.actions[4].label == "💀 Permadeath"
    screen = service.act("test:1", "oath")
    assert "up to level 10" in text(screen) and "«Iron Survivor»" in text(screen) and "☠️ Swear" == screen.actions[0].label
    assert not service.texts.missing


def test_double_confirmation_in_order_with_time_and_cancelled_by_other_buttons(service, clock):
    make_hero(service)
    # skipping a step never swears it
    assert "⏳" in service.act("test:1", "oath:swear").notice and not service._load("test:1").oath
    assert "⏳" in service.act("test:1", "oath:ask2").notice and not service._load("test:1").oath
    first = service.act("test:1", "oath:ask")
    assert first.kind == "oath_confirm" and "UNA pelea" in text(first) and "nivel 1" in text(first)
    assert "⏳" in service.act("test:1", "oath:swear").notice and not service._load("test:1").oath   # step 1 is not step 2
    # another button cancels the confirmation
    service.act("test:1", "oath:ask")
    service.act("test:1", "home")
    assert service.store.get("oath_confirm", "test:1") is None
    assert "⏳" in service.act("test:1", "oath:ask2").notice
    # an old confirmation runs out
    service.act("test:1", "oath:ask")
    service.act("test:1", "oath:ask2")
    clock.advance(11 * MINUTE)
    assert "⏳" in service.act("test:1", "oath:swear").notice and not service._load("test:1").oath
    # ❌ No goes back and cancels
    service.act("test:1", "oath:ask")
    assert service.act("test:1", "oath").kind == "oath" and service.store.get("oath_confirm", "test:1") is None
    # the whole way swears it, for ever
    done = swear(service)
    hero = service._load("test:1")
    assert hero.oath == {"at": clock.now()} and "juró la muerte permanente" in done.notice
    assert ids(done) == ["fallen", "options"]                           # no way to switch it off
    assert "💀 Ya la juraste." in service.act("test:1", "oath:ask").notice
    assert service._load("test:1").oath == {"at": clock.now()}
    assert any(e["k"] == "oath" for e in service._load("test:1").journal)
    assert not service.texts.missing


def test_only_up_to_level_ten(service):
    make_hero(service)
    place(service, "test:1", 0, 0, level=11)
    screen = service.act("test:1", "oath")
    assert "oath:ask" not in ids(screen) and "🔒 Solo se jura hasta el nivel 10" in text(screen)
    assert "🔒" in service.act("test:1", "oath:ask").notice and service.store.get("oath_confirm", "test:1") is None
    service.content.balance["permadeath"]["max_level"] = 0                       # 0 = at any level
    assert "oath:ask" in ids(service.act("test:1", "oath"))


def test_founders_and_guild_leaders_cannot_swear_and_a_sworn_hero_leads_nothing(service):
    make_hero(service, "test:1", "Lyra")
    x, y = wild(service)
    old_camp_at(service, "test:1", x + 4, y)
    screen = service.act("test:1", "oath")
    assert "oath:ask" not in ids(screen) and "fundador" in text(screen)
    # a guild leader cannot swear it; a member can, and then cannot receive the leadership or create a guild
    make_hero(service, "test:2", "Bram")
    make_hero(service, "test:3", "Cora")
    gid, _ = new_gremio(service, "test:2", "Lobos Grises")
    assert "oath:ask" not in ids(service.act("test:2", "oath")) and "líder" in text(service.act("test:2", "oath"))
    join(service, gid, "test:3", leader="test:2")
    swear(service, "test:3")
    assert service._load("test:3").oath.get("at")
    refused = service.act("test:2", "glead!:test:3")
    assert "💀 Cora juró la muerte permanente" in refused.notice
    assert service.store.get("gremio", gid)["leader"] == "test:2"
    make_hero(service, "test:4", "Dax")
    swear(service, "test:4")
    hero = service._load("test:4")
    hero.gold = 100
    service._save(hero)
    assert "no lidera gremios" in service.act("test:4", "gnew").notice and service.store.get("gremio_of", "test:4") is None


# ---------------------------------------------------------------- the fall

def test_a_normal_defeat_is_unchanged(service, losing):
    make_hero(service)
    make_hero(service, "test:2", "Bram")
    hero = service._load("test:1")
    hero.gold = 1000
    service._save(hero)
    view = lose_by_hand(service)
    hero = service._load("test:1")
    assert view.kind == "combat_end" and hero is not None
    assert hero.downed and hero.hp == 1 and hero.gold == 900
    assert not list(service.store.items("fallen")) and not list(service.store.items("fallen_hero"))
    assert service.store.get("reborn", "test:1") is None


def test_a_sworn_hero_falls_for_ever_and_the_account_starts_again(service, clock, losing):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    other_before = service.store.get("hero", "test:2")
    swear(service)
    hero = service._load("test:1")
    hero.gold, hero.gems = 500, 7
    hero.options["retreat"] = 70
    service._save(hero)
    events = []
    service.bus.subscribe(HeroFellForever, events.append)
    clock.advance(3 * DAY)
    view = lose_by_hand(service)
    assert view.kind == "fallen" and view.title == "🪦 Lyra cayó para siempre" and ids(view) == ["newhero", "fallen"]
    assert "⚔️ round" in view.notice and "malherido" not in (view.notice or "")
    memorial = service.store.get("fallen", "f1")
    assert memorial["name"] == "Lyra" and memorial["account"] == "test:1" and memorial["days"] == 3
    assert memorial["enemy"] == enemy_id(service) and memorial["archive"] == "test:1#1"
    assert "🪦 Lyra" in view.body[0] and "3 días con 💀" in view.body[0]
    assert events == [HeroFellForever("test:1", "f1")]
    # the hero is kept whole (D-64), nothing of it stays in "hero"
    assert service.store.get("hero", "test:1") is None
    archived = service.store.get("fallen_hero", "test:1#1")["hero"]
    assert archived["name"] == "Lyra" and archived["gold"] == 500 and archived["oath"]["fell"] == clock.now()
    assert archived["journal"][-1]["k"] == "fell"
    # nobody else changed
    assert service.store.get("hero", "test:2") == other_before
    # the hall, also without a hero, in both languages
    hall = service.act("test:1", "fallen")
    assert hall.kind == "fallen_hall" and "🪦 Lyra" in text(hall) and ids(hall) == ["newhero"]
    assert "🪦 Lyra" in text(service.act("test:2", "fallen"))
    assert service.text("test:1", "/caidos").kind == "fallen_hall"
    # a new hero: the creation, with the same options and the 💎; the name stays in the hall for others only
    assert service.act("test:1", "newhero").kind == "create_name"
    make_hero(service, "test:3", "Cora")
    assert service._name_taken("Lyra", "test:3") and not service._name_taken("Lyra", "test:1")
    make_hero(service, "test:1", "Lyra")
    reborn = service._load("test:1")
    assert reborn.level == 1 and reborn.gold == service.content.balance["hero"]["start_gold"] and reborn.gems == 7
    assert reborn.options.get("retreat") == 70 and reborn.oath == {} and reborn.camp is None
    assert service.store.get("reborn", "test:1") is None
    assert service.store.get("fallen_hero", "test:1#1")["hero"]["gems"] == 0      # the 💎 went to the account
    assert service.act("test:1", "home").kind == "zone"
    assert not service.texts.missing


def test_the_fall_cancels_market_and_repair_orders_into_the_fallen_hero(service, losing):
    make_hero(service)
    swear(service)
    hero = service._load("test:1")
    hero.gold = 1000
    hero.backpack["pocion_vida"] = 2
    hero.backpack["pocion_vida"] -= 2                     # the units go into the order (escrow)
    sell = service._mkt_new_order(hero, "sell", "pocion_vida", 10, 2)
    hero.gold -= 4 * 5                                    # a buy order escrows its coins
    buy = service._mkt_new_order(hero, "buy", "madera", 5, 4)
    hero.gold -= 26
    service.store.put("repair_order", "test:1|arma", {"id": "test:1|arma", "by": "test:1", "name": "Lyra", "slot": "arma",
                                                      "item": hero.gear.get("arma", "espada_1"), "price": 26, "at": 0,
                                                      "until": 10**12})
    service._save(hero)
    lose_by_hand(service)
    assert service.store.get("market_order", sell["id"]) is None and service.store.get("market_order", buy["id"]) is None
    assert service.store.get("repair_order", "test:1|arma") is None
    assert service.store.get("market_box", "test:1") is None and service.store.get("market_mine", "test:1") is None
    record = service.store.get("fallen_hero", "test:1#1")
    assert record["hero"]["gold"] == 1000                 # 954 + 20 back from the buy order + 26 from the repair order
    assert any(e["good"] == "pocion_vida" and e["n"] == 2 for e in record["box"])


def test_the_fall_leaves_the_camp_and_the_guild_and_tells_the_mates(service, losing):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    x, y = wild(service)
    old_camp_at(service, "test:2", x + 4, y)
    key = f"{x + 4}:{y}"
    camp = service.store.get("camp", key)
    camp["members"].append("test:1")
    camp["helpers"] = ["test:1"]
    service.store.put("camp", key, camp)
    place(service, "test:1", x + 4, y, camp=key)
    swear(service)
    service.tick()
    founder_before = service.store.get("hero", "test:2")
    lose_by_hand(service)
    camp = service.store.get("camp", key)
    assert camp["members"] == ["test:2"] and camp["helpers"] == [] and camp["founder_id"] == "test:2"
    assert service.store.get("fallen_hero", "test:1#1")["hero"]["camp"] is None
    news = [v for acc, v in service.tick() if acc == "test:2" and v.kind == "fallen_news"]
    assert news and "💀 Lyra cayó para siempre" in news[0].body[0]
    after = service.store.get("hero", "test:2")
    assert after == founder_before
    # a guild member before the camp leaves the guild; the leader keeps it
    make_hero(service, "test:3", "Cora")
    make_hero(service, "test:4", "Dax")
    gid, _ = new_gremio(service, "test:3", "Lobos Grises")
    join(service, gid, "test:4", leader="test:3")
    swear(service, "test:4")
    lose_by_hand(service, "test:4")
    record = service.store.get("gremio", gid)
    assert record["members"] == ["test:3"] and record["leader"] == "test:3"
    assert service.store.get("gremio_of", "test:4") is None and service.store.get("gremio_of", "test:3")


def test_an_automatic_fight_in_a_batch_is_a_fall_too(service, clock, monkeypatch, auto_fights_on):
    def defeat(state, hero, class_def, ctx, *, attentive=True, use_items=True, max_rounds=None, on_hit=None):
        state["outcome"] = "defeat"
        state["log"] = []
        hero.hp = 0
        return 1
    monkeypatch.setattr("engine.service.game.play_out", defeat)
    make_hero(service)
    swear(service)
    x, y = wild(service)
    place(service, "test:1", x, y)
    hero = service._load("test:1")
    hero.options["fights"] = "auto"
    service._save(hero)
    service.act("test:1", "do:hunt:10")
    pushes = []
    for _ in range(6):
        clock.advance(16 * MINUTE)
        pushes += [v for acc, v in service.tick() if acc == "test:1"]
    assert len(pushes) == 1 and pushes[0].kind == "fallen"
    assert "te venció en una pelea automática." in pushes[0].notice and "malherido" not in pushes[0].notice
    assert service.store.get("hero", "test:1") is None and service.store.get("fallen", "f1")
    assert service.act("test:1", "home").kind == "create_name"


def test_prestige_titles_and_the_mark_change_no_stats(service, clock):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    before = hero_stats(service._kit(service._load("test:1")), 1)
    gold = service._load("test:1").gold
    swear(service)
    assert hero_stats(service._kit(service._load("test:1")), 1) == before and service._load("test:1").gold == gold
    sheet = service.act("test:1", "hero")
    assert "💀 Lyra" in text(sheet) and "💀 Muerte permanente: día 1 de su única vida" in sheet.body
    clock.advance(7 * DAY + MINUTE)
    view = service.act("test:1", "home")
    assert "hierro_7" in service._load("test:1").titles and "«Superviviente de hierro»" in view.notice
    assert "hierro_30" not in service._load("test:1").titles
    assert "💀 Lyra" in "\n".join(p["name"] for p in service._zone_players(*service._load("test:1").home))
    service.act("test:1", "lang:en")
    assert "💀 Permadeath: day 8 of their only life" in service.act("test:1", "hero").body
    assert not service.texts.missing


# ---------------------------------------------------------------- 🌱 the professions speed up regrowth (D-145)

def learn(service, account, pid, rank):
    hero = service._load(account)
    if pid not in hero.learned:
        hero.learned.append(pid)
    hero.professions[pid] = xp_for_rank(service._prof_cfg()["rank_formula"], rank)
    service._save(hero)
    return hero


def chop_once(service, account="test:1"):
    hero = service._load(account)
    hero.x, hero.y = 0, 0
    hero.exploration["0:0"] = 100
    activity = {"kind": "gather", "only": "madera", "got": {}, "log": [], "until": 1, "done": 1}
    service._gather_step(hero, service._zone(0, 0), Rng(3), activity)
    service._save(hero)
    return activity


def test_a_trade_tends_the_zone_and_it_grows_back_faster(service, clock):
    make_hero(service)
    activity = chop_once(service)                          # without the 🪓 Leñador: no care
    assert activity["got"].get("madera") and "tend" not in service.store.get("stock", "0:0")
    learn(service, "test:1", "lenador", 10)
    chop_once(service)
    tend = service.store.get("stock", "0:0")["tend"]["madera"]
    assert tend["bonus"] == pytest.approx(0.2) and tend["by"] == "lenador"
    assert tend["until"] == pytest.approx(clock.now() + 24 * HOUR)
    view = service.act("test:1", "home")
    assert "🌱 🪵 Madera vuelve más rápido por 🪓 Leñador: +20 %" in text(view)
    service.act("test:1", "lang:en")
    assert "grows back faster thanks to 🪓 Lumberjack: +20 %" in text(service.act("test:1", "home"))
    # a weaker gatherer does not shorten it; a stronger one replaces it
    make_hero(service, "test:2", "Bram")
    learn(service, "test:2", "lenador", 5)
    clock.advance(HOUR)
    chop_once(service, "test:2")
    assert service.store.get("stock", "0:0")["tend"]["madera"]["bonus"] == pytest.approx(0.2)
    learn(service, "test:2", "lenador", 80)
    chop_once(service, "test:2")
    assert service.store.get("stock", "0:0")["tend"]["madera"]["bonus"] == pytest.approx(1.0)   # capped at max_bonus
    # it runs out after 24 hours: no line and no record left after the next gathering
    clock.advance(25 * HOUR)
    assert "🌱" not in text(service.act("test:1", "home"))
    hero = learn(service, "test:1", "lenador", 0)
    hero.learned.remove("lenador")
    service._save(hero)
    chop_once(service)
    assert "tend" not in service.store.get("stock", "0:0")
    assert not service.texts.missing


def test_the_regrowth_math_counts_only_the_tended_hours(service, clock):
    x, y = wild(service)
    key = f"{x}:{y}"
    per_hour = service.content.balance["stock"]["regen_per_hour"] * service.content.balance["stock"]["regen_mult"]["madera"]
    now = clock.now()
    service.store.put("stock", key, {"levels": {"madera": 0.2}, "at": now})
    clock.advance(2 * HOUR)
    plain = service._stock(x, y)["madera"]
    assert plain == pytest.approx(0.2 + 2 * per_hour)
    service.store.put("stock", key, {"levels": {"madera": 0.2}, "at": now,
                                     "tend": {"madera": {"bonus": 0.5, "until": now + HOUR, "by": "lenador"}}})
    tended = service._stock(x, y)["madera"]
    assert tended == pytest.approx(0.2 + (2 + 0.5) * per_hour) and tended > plain
    others = {r: v for r, v in service._stock(x, y).items() if r != "madera"}
    assert all(v == 1.0 for v in others.values())          # only the tended resource moves


# ---------------------------------------------------------------- ❓ Dudas and the patch

def test_faq_and_patch_in_both_languages(service):
    make_hero(service)
    answer = service.act("test:1", "duda:d65")
    assert "💀" in answer.title and "nivel 10" in text(answer) and "7, 30 y 100" in text(answer) and "{" not in text(answer)
    assert "+2 % por cada rango" in text(service.act("test:1", "duda:d09"))
    service.act("test:1", "lang:en")
    answer = service.act("test:1", "duda:d65")
    assert "Permadeath" in answer.title or "permadeath" in text(answer)
    assert "level 10" in text(answer) and "{" not in text(answer)
    patch = list(service.content.patches.values())[-1]
    assert patch["version"] == "0.60" and patch["title_en"] and len(patch["notes"]) == len(patch["notes_en"])
    assert not service.texts.missing
