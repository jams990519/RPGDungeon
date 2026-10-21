"""0.43 (D-306, the owner on 20-oct-2026; how it was done: D-316): profession titles bought at the Trainer, learning prices by
branch, more hide and Skinner xp per beast, 🎣 Pescar, 🧱 Mantenimiento (a camp work that repeats) and the trader buying
potions and remedies for a little.

[ES] Pruebas de la 0.43. **Títulos (D-306.1, E-228):** al tope de tu título (20, 40, 60, 80, 95) el oficio no guarda experiencia
hasta comprar el siguiente en el 🧑‍🏫 Entrenador (Oficial 🥉50 y nivel 10 ... Gran Maestro 🥈50 y nivel 50); se compra solo en el
tope, con el nivel y las monedas; quien ya pasaba un tope conserva su rango y tiene gratis los títulos hasta él (D-64); el
🧭 Explorador no tiene títulos (D-316); 📋 Mis oficios, el Entrenador y la pantalla del oficio dicen qué comprar.
**Precios (D-306.4, E-222):** 🥈1 fabricación (y ✨), 🥉50 recolección, refinado (y 🏗️); gratis para quien ya practicaba.
**Lo que no avanzaba (D-306.5, E-223):** la 🦌 piel ×2,5 por bestia y +3 de 🔪 Desollador por bestia desollada; 🎣 Pescar solo
da 🐟 pescado y solo donde hay agua (y lo sabes, o el terreno es todo agua); 🧱 Mantenimiento sube la 🏗️ Construcción más allá
del 24 una y otra vez; el mercader compra pociones y remedios a un cuarto de su precio (no lo del cinturón). Todo también en
inglés.
Archivo: tests/test_titulos_de_oficio.py · Módulo: M14 Oficios · Prueba: engine/service/game.py (_prof_gain, _prof_room,
_title_*, _titles_view, _buy_title, _learn_price, _skin_loot_count, _end_combat, _can_fish, _explore_menu, _maintain,
_sellable, _sell_price), engine/professions/rules.py (title_cap, held_title_index, xp_room), content/balance.yaml
(professions.titles, learn_price, skinning; shop.remedy_sell_ratio; camp_professions.maintenance).
"""

import pytest

from conftest import make_hero
from engine.combat import make_combat
from engine.professions import rules as profession_rules
from engine.professions import xp_for_rank
from test_camp_upgrades import build, camp_at, set_hero
from test_camps import place
from test_guilds import join

KEY = "6:0"


def body(view):
    return "\n".join(view.body)


def ids(view):
    return [a.id for a in view.actions]


def rank_xp(service, rank):
    return xp_for_rank(service.content.balance["professions"]["rank_formula"], rank)


def hero_with(service, account="test:1", learned=("minero",), **values):
    """A hero in the Claro who learned `learned`, with the given fields set."""
    hero = service._load(account) or (make_hero(service, account) and service._load(account))
    hero.learned = list(dict.fromkeys(list(hero.learned) + list(learned)))
    hero.tutorial = len(service.content.balance["tutorial"]["steps"])
    for key, value in values.items():
        setattr(hero, key, value)
    service._save(hero)
    return hero


def run(service, clock, account="test:1", hours=6):
    pushes = []
    for _ in range(hours):
        clock.advance(3600)
        pushes += [view.notice or "" for acc, view in service.tick() if acc == account]
    return "\n".join(pushes)


# ---------------------------------------------------------------- 🎖️ titles (D-306.1)

def test_the_rules_give_each_title_its_cap(content):
    rows = content.professions["ranks"]
    assert [profession_rules.title_cap(rows, i, 100) for i in range(len(rows))] == [20, 40, 60, 80, 95, 100]
    assert profession_rules.held_title_index(rows, 45, None) == 2                  # D-64: rank 45 already is Experto
    assert profession_rules.held_title_index(rows, 20, "oficial") == 1
    formula = content.balance["professions"]["rank_formula"]
    assert profession_rules.xp_room(xp_for_rank(formula, 21) - 1, formula, 20, 100) == 0
    assert profession_rules.xp_room(0, formula, 100, 100) is None
    titles = content.balance["professions"]["titles"]
    assert [(t["price"], t["level"]) for t in titles.values()] == [(50, 10), (200, 20), (1000, 30), (3000, 40), (5000, 50)]


def test_a_profession_stops_at_its_title_cap_and_keeps_nothing_more(service):
    make_hero(service)
    hero = hero_with(service, professions={"minero": rank_xp(service, 20) - 5})
    lines = service._prof_gain(hero, "minero", 5000)
    top = rank_xp(service, 21) - 1
    assert hero.professions["minero"] == top and service._prof_rank(hero, "minero") == 20
    assert lines[-1].startswith("🔒 ⛏️ Minero llegó al tope de Aprendiz (rango 20)") and "Oficial" in lines[-1]
    assert "🥉50" in lines[-1] and "nivel 10" in lines[-1] and "no se guarda" in lines[-1]
    again = service._prof_gain(hero, "minero", 30)                                 # D-316: not kept
    assert hero.professions["minero"] == top and len(again) == 1 and again[0].startswith("🔒")
    assert service._title_waiting(hero, "minero") and service._title_next(hero, "minero") == "oficial"


def test_buying_the_next_title_needs_the_cap_the_level_and_the_coins(service):
    make_hero(service)
    hero_with(service, professions={"minero": rank_xp(service, 12)}, gold=500)
    early = service.act("test:1", "ptitle:minero")                               # not at the cap yet: nothing charged
    assert "todavía no llegó al tope" in early.notice and service._load("test:1").gold == 500
    hero_with(service, professions={"minero": rank_xp(service, 21) - 1}, gold=500)
    low = service.act("test:1", "ptitle:minero")
    assert "nivel 10" in low.notice and service._load("test:1").gold == 500
    hero_with(service, level=10, gold=20)
    poor = service.act("test:1", "ptitle:minero")
    assert "cuesta 🥉50" in poor.notice and service._load("test:1").gold == 20
    hero_with(service, gold=120)
    done = service.act("test:1", "ptitle:minero")
    hero = service._load("test:1")
    assert "Ya eres Oficial de ⛏️ Minero" in done.notice and hero.gold == 70 and hero.prof_titles == {"minero": "oficial"}
    assert done.kind == "titles" and "ptitle:minero" not in ids(done)
    service._prof_gain(hero, "minero", 1000)
    assert service._prof_rank(hero, "minero") > 20 and service._prof_cap(hero, "minero") == 40
    assert service.act("test:1", "ptitle:minero").notice.startswith("🎖️")    # rank 21+: Experto waits for rank 40


def test_heroes_past_a_cap_keep_their_rank_and_their_titles_for_free(service):
    make_hero(service)
    hero = hero_with(service, professions={"minero": rank_xp(service, 45) + 10}, gold=0)   # from before 0.43
    assert service._prof_rank(hero, "minero") == 45 and service._prof_cap(hero, "minero") == 60
    assert not service._title_waiting(hero, "minero")
    before = hero.professions["minero"]
    service._prof_gain(hero, "minero", 100)
    assert hero.professions["minero"] == before + 100 and hero.gold == 0 and hero.prof_titles == {}
    service._prof_gain(hero, "minero", 10 ** 6)                                    # up to 60: then Artesano is bought
    assert service._prof_rank(hero, "minero") == 60
    assert service._title_lock_line(hero, "minero", "ptitle.lock_short") == \
        "🔒 Tope de Experto: compra Artesano en el Entrenador (🥈10, nivel 30)"


def test_the_trainer_my_professions_and_the_profession_say_what_to_buy(service):
    make_hero(service)
    hero_with(service, professions={"minero": rank_xp(service, 21) - 1}, level=10, gold=200)
    mine = service.act("test:1", "myprof")
    assert "🔒 Tope de Aprendiz: compra Oficial en el Entrenador (🥉50, nivel 10)" in mine.body
    assert "no se guarda" in body(mine)
    trainer = service.act("test:1", "trainer")
    assert "ptitles" in ids(trainer) and "🥈1 los de fabricación y 🥉50 los de recolección y refinado" in body(trainer)
    assert any(line.startswith("🔒 ⛏️ Minero en el tope de Aprendiz") for line in trainer.body)
    titles = service.text("test:1", "/titulos")
    assert titles.kind == "titles" and ids(titles) == ["ptitle:minero", "trainer"]
    assert "Oficial 🥉50 (nivel 10)" in body(titles) and "Explorador sube solo" in body(titles)
    detail = service.text("test:1", "/minero")
    assert ids(detail)[0] == "ptitle:minero:d" and detail.actions[0].label == "🎖️ Comprar Oficial · 🥉50"
    bought = service.act("test:1", "ptitle:minero:d")
    assert bought.kind == "profession" and "Oficial" in bought.notice and "ptitle:minero:d" not in ids(bought)
    assert "ptitles" not in ids(service.act("test:1", "trainer"))                 # nothing waits any more
    assert "🎖️ Oficial: sube hasta el rango 40." in body(bought) or "rango 40" in body(bought)
    assert not service.texts.missing


def test_the_trainer_fits_titles_and_specializations_in_five_buttons(service):
    from engine.service.game import button_cap
    make_hero(service)
    hero_with(service, learned=("minero", "herreria"), professions={"minero": rank_xp(service, 21) - 1,
                                                                    "herreria": rank_xp(service, 30)})
    trainer = service.act("test:1", "trainer")
    assert ids(trainer) == ["myprof", "learnlist", "ptitles", "pspecs", "claro"] and trainer.layout == [2, 2, 1]
    assert len(trainer.actions) <= button_cap("trainer") == 5


def test_the_explorer_has_no_titles(service):
    make_hero(service)
    hero = hero_with(service, learned=(), professions={"explorador": rank_xp(service, 20)})
    service._prof_gain(hero, "explorador", 10 ** 5)
    assert service._prof_rank(hero, "explorador") > 20 and service._prof_room(hero, "explorador") is None
    assert not service._title_waiting(hero, "explorador")


def test_a_capped_gathering_batch_says_nothing_was_kept(service):
    make_hero(service)
    hero = hero_with(service, learned=("lenador",), professions={"lenador": rank_xp(service, 21) - 1})
    activity = {"kind": "gather", "got": {}, "log": [], "until": 1.0, "done": 1}
    first = service._trade_gather(hero, {"madera": 3}, activity)
    activity["log"] += first
    second = service._trade_gather(hero, {"madera": 3}, activity)
    assert activity["trade"] == {"lenador": 0} and len(first) == 1 and first[0].startswith("🔒") and second == []
    assert hero.professions["lenador"] == rank_xp(service, 21) - 1


# ---------------------------------------------------------------- 📚 learning prices by branch (D-306.4)

def test_learning_prices_by_branch_and_free_for_who_practised(service):
    make_hero(service)
    hero = service._load("test:1")
    prices = {pid: service._learn_price(hero, pid) for pid in ("cocina", "herreria", "encantamiento", "minero", "desollador",
                                                             "pescador", "aserradero", "canteria", "construccion")}
    assert prices == {"cocina": 100, "herreria": 100, "encantamiento": 100, "minero": 50, "desollador": 50, "pescador": 50,
                      "aserradero": 50, "canteria": 50, "construccion": 50}
    hero.professions["herreria"] = 40
    assert service._learn_price(hero, "herreria") == 0
    learn = service.act("test:1", "learnlist")
    assert "🔨 Herrería · 🥈1  /herreria" in body(learn) and "🪚 Aserradero · 🥉50  /aserradero" in body(learn)


# ---------------------------------------------------------------- 🦌 hide and 🔪 Desollador (D-306.5)

def test_beasts_drop_two_and_a_half_times_the_hide_and_the_same_meat(service):
    make_hero(service)
    hero = hero_with(service, learned=())                                         # no 🔪 Desollador: no extra units
    edef = service.content.enemies["lobo_ceniciento"]
    hides, meats = [], []
    for seed in range(240):
        hero.backpack = {}
        state = make_combat("lobo_ceniciento", edef, 2, service._kit(hero), seed)
        state["outcome"] = "victory"
        service._end_combat(hero, state)
        if hero.backpack.get("piel"):
            hides.append(hero.backpack["piel"])
        if hero.backpack.get("carne"):
            meats.append(hero.backpack["carne"])
    assert set(hides) <= {2, 3, 5} and 3.3 <= sum(hides) / len(hides) <= 4.2      # 1-2 (1,5) × 2,5 = 3,75
    assert set(meats) <= {1, 2}                                                   # the meat does not change
    assert service._skin_loot_count(hero, "carne", 2, 1) == 2


def test_the_skinner_gets_experience_per_beast_skinned(service):
    make_hero(service)
    hero = hero_with(service, learned=("desollador",))
    edef = service.content.enemies["lobo_ceniciento"]
    for seed in range(60):
        hero.backpack = {}
        before = hero.professions.get("desollador", 0)
        state = make_combat("lobo_ceniciento", edef, 2, service._kit(hero), seed)
        state["outcome"] = "victory"
        service._end_combat(hero, state)
        units = hero.backpack.get("piel", 0) + hero.backpack.get("carne", 0)
        if units:
            assert hero.professions["desollador"] - before == units + 3            # 1 per unit + 3 per beast
            return
    raise AssertionError("the wolf never dropped meat or hide")


# ---------------------------------------------------------------- 🎣 Pescar (D-306.5, D-316)

def _water_zone(service, swamp=False):
    """A zone near the Claro with fish: in a swamp (all water) or in another terrain (a river or a pond)."""
    fish = service._fish_resource()
    for r in range(1, 25):
        for x in range(-r, r + 1):
            for y in (-r, r):
                for zx, zy in ((x, y), (y, x)):
                    if service._is_lair(zx, zy) or fish not in service._zone_resources(zx, zy):
                        continue
                    whole = float(service.content.biomes[service._zone(zx, zy).biome].get("water", 0)) >= 1.0
                    if whole == swamp:
                        return zx, zy
    return None


def test_fishing_is_offered_only_where_there_is_water_and_you_know_it(service, content):
    make_hero(service)
    menu = service.act("test:1", "explore_menu")
    assert "fish" not in ids(menu)                                                 # the Claro has no water
    assert service.act("test:1", "fish").notice == "🐟 En esta zona no hay agua para pescar."
    river = _water_zone(service)
    assert river, "no zone with water near the Claro"
    place(service, "test:1", *river)
    assert "fish" not in ids(service.act("test:1", "explore_menu"))               # a river you have not found yet
    place(service, "test:1", *river, exploration={f"{river[0]}:{river[1]}": 100})
    menu = service.act("test:1", "explore_menu")
    assert ids(menu)[:4] == ["explore", "gather", "chop", "fish"] and menu.layout == [1, 2, 2, 1]
    assert menu.actions[3].label.startswith("🎣 Pescar") and len(menu.actions) == 6
    swamp = _water_zone(service, swamp=True)
    if swamp:                                                                      # all water: always offered
        place(service, "test:1", *swamp, exploration={})
        assert "fish" in ids(service.act("test:1", "explore_menu"))


def test_fishing_gives_only_fish_and_raises_the_fisher(service, clock, content):
    content.balance["gather"]["encounter_scale"] = 0                              # no ambush in the way
    make_hero(service)
    river = _water_zone(service)
    place(service, "test:1", *river, exploration={f"{river[0]}:{river[1]}": 100}, learned=["pescador"])
    screen = service.act("test:1", "fish")
    assert screen.kind == "batch" and screen.title == "🎣 Pescar" and ids(screen)[0] == "do:fish:5"
    view = service.act("test:1", "do:fish:10")
    hero = service._load("test:1")
    assert view.title == "🎣 Pescando" and hero.activity["only"] == "pescado" and hero.activity["mode"] == "fish"
    assert service._status_text(hero) == "🎣 Pescando"
    summary = run(service, clock, hours=3)
    hero = service._load("test:1")
    fishes = hero.backpack.get("pescado", 0)
    gathered = {i for i in hero.backpack if service.content.items[i]["kind"] in ("material", "food")}
    assert gathered == {"pescado"} and fishes >= 10
    assert "🎣 Pescaste" in summary and "🎣 Pescador +" in summary
    assert hero.professions["pescador"] >= fishes


# ---------------------------------------------------------------- 🧱 Mantenimiento (D-306.5, D-316)

def test_upkeep_repeats_and_raises_construction_past_rank_24(service):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    camp_at(service, 3)
    join(service, "test:2")
    place(service, "test:2", 6, 0)
    assert ("keep", "upkeep") not in service._works_entries(service._load("test:2"), service.store.get("camp", KEY),
                                                            service._upgrades(KEY))      # nothing built yet
    build(service, "empalizada")
    cost = service.content.balance["camp_professions"]["maintenance"]["cost"]
    set_hero(service, "test:2", learned=["construccion"], professions={"construccion": rank_xp(service, 25) - 10},
             backpack={k: n * 3 for k, n in cost.items()})
    works = service.act("test:2", "upw")
    assert "upkeep" in ids(works) and any(line.startswith("🧱 Mantenimiento") for line in works.body)
    for n in (1, 2, 3):
        view = service.act("test:2", "upkeep")
        record = service._upgrades(KEY)
        assert record["upkeep_done"] == n and record["upkeep"] == {} and "Mantenimiento completo" in view.notice
    hero = service._load("test:2")
    assert service._prof_rank(hero, "construccion") >= 25 and hero.backpack == {}
    assert hero.professions["construccion"] == rank_xp(service, 25) - 10 + 3 * sum(cost.values())
    assert "No llevas nada" in service.act("test:2", "upkeep").notice
    news = [v for acc, v in service.tick() if acc == "test:1" and v.kind == "camp_news"]
    assert news and "Bram completó un mantenimiento" in news[0].body[0]
    assert not service.texts.missing


# ---------------------------------------------------------------- 🧪 the trader buys potions (D-306.5)

def test_the_trader_buys_potions_and_remedies_for_a_little_but_not_the_belt(service):
    make_hero(service)
    hero = hero_with(service, learned=())
    belt = dict(hero.belt)
    hero.backpack = {"pocion_vida": 4, "pocion_mayor": 1}
    hero.gold = 0
    service._save(hero)
    view = service.act("test:1", "shop:sell")
    assert "/v61" in body(view) and "/v63" in body(view) and "lo del cinturón no se vende" in body(view)
    sold = service.text("test:1", "/v61")
    hero = service._load("test:1")
    assert "pocion_vida" not in hero.backpack and hero.gold == 4 and hero.belt == belt   # 🥉6 × 25 % = 1 each
    service.text("test:1", "/v63")
    assert service._load("test:1").gold == 4 + 4                                       # 🥉18 × 25 % = 4
    assert "Vendiste" in sold.notice or "🧪" in sold.notice
    for item_id in service.content.balance["shop"]["sells"]:                           # never a profit buying and selling
        assert service._sell_price(item_id) < service._shop_price(service._load("test:1"), item_id)


# ---------------------------------------------------------------- English

def test_the_new_screens_read_well_in_english(service):
    from test_idiomas import english_hero
    english_hero(service)
    hero_with(service, professions={"minero": rank_xp(service, 21) - 1}, level=10, gold=200)
    titles = service.act("test:1", "ptitles")
    assert titles.title == "🎖️ Profession titles" and "Journeyman 🥉50 (level 10)" in body(titles)
    mine = service.act("test:1", "myprof")
    assert "🔒 Apprentice cap: buy Journeyman at the Trainer (🥉50, level 10)" in mine.body
    assert "Journeyman" in service.act("test:1", "ptitle:minero").notice
    assert "for crafting" in body(service.act("test:1", "trainer"))
    hero = service._load("test:1")
    hero.backpack = {"venda": 3}
    service._save(hero)
    assert "Potions and remedies" in body(service.act("test:1", "shop:sell"))
    assert not service.texts.fallbacks.get("en")
