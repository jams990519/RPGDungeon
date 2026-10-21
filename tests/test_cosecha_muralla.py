"""The wall's harvest (D-309, confirmed by the owner on 20-oct-2026; how: D-325, provisional; 0.49).

[ES] Pruebas de lo que decidió el dueño (E-216 y E-217):
- con la 🧱 Muralla construida, cada zona del territorio da sola el 20 % de lo que vuelve a crecer, al 💰 fondo del campamento
  (nunca a la mochila de nadie);
- sin muralla no hay cosecha; sin miembros activos esa semana, tampoco; se junta como mucho 7 días;
- llega una vez por semana, sola (tick), con un aviso a cada miembro en su idioma; la fracción no se pierde;
- la cosecha reemplaza el +50 % de recolectar en tu territorio (gather.own_land_bonus vale 1,0);
- la línea "🌾 Cosecha de la muralla: +N/día · guardado X (tope 7 días)" en ⬆️ Mejorar, 💰 Fondos e ℹ️ Información, y la pista
  sin muralla solo desde su nivel (D-287); ❓ /d61 y los textos que prometían el +50 %.
Archivo: tests/test_cosecha_muralla.py · Módulo: M9 Frontera y Fundación (con M24 Construcción y M15, el fondo) · Prueba:
engine/world/harvest.py (regrow_per_day, daily_rate, accrue, split_units) y engine/service/game.py (_harvest_goods,
_harvest_rate, _harvest_state, _harvest_deliver, _harvest_tick, _harvest_line, _gather_step, _harvest_faq_values), y
engine/service/gremio.py (_guild_funds_view).
"""

import pytest

from conftest import make_hero
from engine.core import Rng
from engine.world import harvest as harvest_rules
from test_camp_upgrades import build, camp_at, set_hero
from test_camps import place
from test_guilds import join, set_level

KEY = "6:0"
DAY = 86400
TITLE_ES = "🌾 Cosecha de la muralla"
TITLE_EN = "🌾 Wall harvest"


def text(view):
    return "\n".join([view.notice or "", view.title or ""] + list(view.body))


def walled_camp(service, english_member=False, level=5):
    """Lyra founds the camp at 6:0 (level 5) and Bram joins; nothing is built yet. Returns the camp record."""
    make_hero(service, "test:1", "Lyra")
    if english_member:
        from test_idiomas import english_hero
        english_hero(service, "test:2", "Bram")
    else:
        make_hero(service, "test:2", "Bram")
    camp_at(service, level)
    join(service, "test:2")
    return service.store.get("camp", KEY)


def add_zones(service, *zones):
    """Give the camp more territory straight in the store (🗺️ Agrandar territorio has its own tests)."""
    camp = service.store.get("camp", KEY)
    for x, y in zones:
        camp["zones"].append([x, y])
        service.store.put("territory", f"{x}:{y}", {"camp": KEY})
    service.store.put("camp", KEY, camp)
    return camp


def seen_now(service, *accounts):
    for account in accounts:
        set_hero(service, account, seen_at=service.clock.now())


def harvest_pushes(service, ticked, title):
    return [(acc, view) for acc, view in ticked if view.title == title]


def fund(service):
    return dict(service._upgrades(KEY)["fund"])


def expected_week(service, camp, days=7):
    """What `days` days of harvest give per resource (whole units), from the zones' resources and today's numbers."""
    per = 0.20 * 24                                       # harvest.share × what a resource regrows per day (24)
    rate = {}
    for x, y in service._camp_zone_list(camp):
        for res in service._harvest_goods(x, y):
            rate[res] = rate.get(res, 0.0) + per
    return {res: int(n * days) for res, n in rate.items()}


# ---------------------------------------------------------------- the pure helpers


def test_pure_helpers_regrow_rate_cap_and_whole_units(content):
    stock = content.balance["stock"]
    assert harvest_rules.regrow_per_day(stock, "madera") == pytest.approx(24)            # 2 % an hour, 2 % a unit
    assert harvest_rules.regrow_per_day(stock, "madera", real=True) == pytest.approx(72)  # D-305: ×3 the 6 base ones
    assert harvest_rules.regrow_per_day(stock, "sal", real=True) == pytest.approx(24)     # the terrain's own: ×1
    assert harvest_rules.regrow_per_day(stock, "madera", real=True, well=0.5) == pytest.approx(108)   # ⛲ Pozo
    rate = harvest_rules.daily_rate([["madera", "piedra"], ["madera"]], stock, 0.20)
    assert rate == {"madera": pytest.approx(9.6), "piedra": pytest.approx(4.8)}
    pile = harvest_rules.accrue({}, rate, 3, 7)
    assert pile["madera"] == pytest.approx(28.8)
    pile = harvest_rules.accrue(pile, rate, 30, 7)                                       # never more than 7 days
    assert pile == {"madera": pytest.approx(67.2), "piedra": pytest.approx(33.6)}
    assert harvest_rules.accrue({"sal": 5.0}, rate, 1, 7)["sal"] == 5.0                    # not harvested any more: it waits
    units, rest = harvest_rules.split_units(pile)
    assert units == {"madera": 67, "piedra": 33}
    assert rest == {"madera": pytest.approx(0.2), "piedra": pytest.approx(0.6)}


def test_balance_harvest_block_and_the_bonus_key_stays(content):
    cfg = content.balance["harvest"]
    assert cfg["wall"] == "muralla" and cfg["wall"] in content.camp_upgrades["upgrades"]
    assert cfg["share"] == pytest.approx(0.20) and cfg["cap_days"] == 7 and cfg["week_days"] == 7
    assert cfg["active_days"] == 7 and cfg["real_regen"] is False
    assert content.balance["gather"]["own_land_bonus"] == pytest.approx(1.0)             # D-309: replaced, the key stays


# ---------------------------------------------------------------- no wall, no harvest


def test_no_harvest_without_a_wall(service, clock):
    camp = walled_camp(service)
    service.tick()
    clock.advance(8 * DAY)
    seen_now(service, "test:1", "test:2")
    ticked = service.tick()
    assert fund(service) == {} and "harvest" not in service._upgrades(KEY)
    assert service._harvest_state(camp, service._upgrades(KEY)) is None
    assert not harvest_pushes(service, ticked, TITLE_ES)
    view = service.act("test:1", "improve")                                               # level 5: the hint, not the line
    body = text(view)
    assert "Con la 🧱 Muralla construida" in body and "guardado" not in body
    set_level(service, 4)                                                                # D-287: below its level, nothing
    assert "Muralla" not in text(service.act("test:1", "improve"))
    assert not service.texts.missing


# ---------------------------------------------------------------- a week with a wall and active members


def test_harvest_with_a_wall_and_active_members_goes_to_the_fund(service, clock):
    camp = walled_camp(service, english_member=True)
    camp = add_zones(service, (7, 0), (5, 0))
    build(service, "muralla")
    bags = {acc: dict(service._load(acc).backpack) for acc in ("test:1", "test:2")}
    service.tick()                                                                      # the week starts with the wall
    data = service._upgrades(KEY)["harvest"]
    assert data["since"] == pytest.approx(clock.now()) and data["pile"] == {}
    clock.advance(3 * DAY)
    service.act("test:2", "home")                                                       # Bram plays this week
    ticked = service.tick()
    assert not harvest_pushes(service, ticked, TITLE_ES) and fund(service) == {}        # not before the week ends
    clock.advance(4 * DAY)
    ticked = service.tick()
    want = expected_week(service, camp)
    assert want and fund(service) == want                                               # 20 % of 24 a day × 7 days
    assert all(service.content.items[i]["kind"] == "material" and not service.content.items[i].get("food") for i in want)
    for acc, before in bags.items():                                                    # never into anyone's backpack
        assert service._load(acc).backpack == before
    record = service._upgrades(KEY)
    assert record["harvest"]["total"] == want and record["harvest"]["last"]["items"] == want
    assert record["harvest"]["pile"] == {} and record["harvest"]["since"] == pytest.approx(clock.now())
    es = harvest_pushes(service, ticked, TITLE_ES)
    en = harvest_pushes(service, ticked, TITLE_EN)
    assert [acc for acc, _ in es] == ["test:1"] and [acc for acc, _ in en] == ["test:2"]   # each in their language
    assert "3 zonas" in text(es[0][1]) and "3 zones" in text(en[0][1])
    assert [a.id for a in es[0][1].actions] == ["gfunds"]
    assert not harvest_pushes(service, service.tick(), TITLE_ES)                         # one notice a week, not more
    assert not service.texts.missing


def test_the_fraction_is_kept_for_the_next_week(service, clock):
    camp = walled_camp(service)
    build(service, "muralla")
    service.tick()
    for _ in range(2):
        clock.advance(7 * DAY)
        seen_now(service, "test:1")
        service.tick()
    want = {res: int(0.2 * 24 * 14) for res in service._harvest_goods(6, 0)}            # 67.2 → 67, not 2 × 33
    assert fund(service) == want
    assert camp["zones"] == [[6, 0]]


# ---------------------------------------------------------------- nobody played that week


def test_no_harvest_without_activity_that_week(service, clock):
    walled_camp(service)
    build(service, "muralla")
    service.tick()
    clock.advance(7 * DAY + 60)                                                         # nobody pressed a button
    ticked = service.tick()
    assert fund(service) == {} and not harvest_pushes(service, ticked, TITLE_ES)
    data = service._upgrades(KEY)["harvest"]
    assert data["pile"] == {} and data.get("carry") == {} and data["since"] == pytest.approx(clock.now())
    clock.advance(7 * DAY)                                                              # the next week someone plays
    seen_now(service, "test:2")
    service.tick()
    assert fund(service) == {res: int(0.2 * 24 * 7) for res in service._harvest_goods(6, 0)}   # only that week


# ---------------------------------------------------------------- the 7-day cap


def test_it_piles_up_seven_days_at_most(service, clock):
    camp = walled_camp(service)
    build(service, "muralla")
    service.tick()
    service.store.put("meta", "harvest", {"next": clock.now() + 40 * DAY})              # the delivery comes late (bot off)
    clock.advance(20 * DAY)
    record = service._upgrades(KEY)
    state = service._harvest_state(camp, record)
    per_day = sum(service._harvest_rate(camp).values())
    assert sum(state["pile"].values()) == pytest.approx(7 * per_day)                    # 20 days waited, 7 kept
    place(service, "test:1", 6, 0)
    assert "(tope 7 días)" in text(service.act("test:1", "improve"))
    service.store.put("meta", "harvest", {"next": 0})
    seen_now(service, "test:1")
    service.tick()
    assert fund(service) == expected_week(service, camp)


# ---------------------------------------------------------------- what the members see


def test_the_harvest_line_in_improve_funds_and_information(service, clock):
    camp = walled_camp(service)
    add_zones(service, (7, 0))
    build(service, "muralla")
    service.tick()
    clock.advance(2 * DAY)
    camp = service.store.get("camp", KEY)
    rate = sum(service._harvest_rate(camp).values())
    per_day = round(rate)
    stored = int(sum(service._harvest_state(camp, service._upgrades(KEY))["pile"].values()))
    assert stored == int(2 * rate) and per_day == round(0.2 * 24 * sum(len(service._harvest_goods(x, y)) for x, y in camp["zones"]))
    line = f"🌾 Cosecha de la muralla: +{per_day}/día · guardado {stored} (tope 7 días) · al 💰 fondo en"
    place(service, "test:1", 6, 0)
    assert line in text(service.act("test:1", "improve"))                               # ⬆️ Mejorar
    assert line in text(service.act("test:2", "gfunds"))                                # 💰 Fondos, from anywhere
    info = text(service.act("test:1", "campinfo"))                                      # ℹ️ Información
    assert line in info and "50 %" not in info
    assert not service.texts.missing


def test_english_line_and_no_more_promise_of_fifty_percent(service, clock):
    walled_camp(service, english_member=True)
    build(service, "muralla")
    service.tick()
    place(service, "test:2", 6, 0)
    body = text(service.act("test:2", "gfunds"))
    assert "🌾 Wall harvest: +" in body and "(cap 7 days)" in body
    for lang in ("es", "en"):                                                           # ❓ and 📚 never promise the +50 %
        with service.texts.use(lang):
            values = service._faq_values()
            for code in ("d09", "d57", "d61"):
                answer = service.texts.t(f"faq.{code}.a", **values)
                assert "{" not in answer and "% más" not in answer and "% more" not in answer
            assert service.texts.t("territory.info_line", items="x", cap=3).count("50") == 0
    assert values["harvest_pct"] == 20 and values["harvest_days"] == 7 and values["wall_level"] == 5
    assert "own_bonus" not in values
    assert not service.texts.missing


# ---------------------------------------------------------------- the +50 % is gone in your own land


def test_gathering_in_your_own_land_gives_no_bonus(service):
    walled_camp(service)
    service.content.balance["gather"]["amount"] = [2, 2]                                # a fixed draw (test only)
    service.content.balance["gather"]["encounter_scale"] = 0                            # no ambush (test only)
    service._trade_gather = lambda hero, got, activity: []                              # no profession extras (test only)
    service._node_main = lambda x, y: None                                              # no node ×2 (test only)
    zone = service._zone(6, 0)
    service.store.put("stock", KEY, {"levels": {r: 1.0 for r in service._zone_resources(6, 0)}, "at": service.clock.now()})
    hero = service._load("test:2")                                                      # a member, in the camp's land
    hero.x, hero.y, hero.backpack = 6, 0, {}
    activity = {"kind": "gather", "got": {}, "log": [], "until": 1.0, "done": 1}
    service._gather_step(hero, zone, Rng(3), activity)
    plain = 2 + zone.level // 3
    assert sum(activity["got"].values()) == plain                                       # before 0.49: int(plain × 1.5 + 0.5)
    assert plain != int(plain * 1.5 + 0.5)


def test_pescado_is_food_and_never_harvested(service):
    make_hero(service, "test:1", "Lyra")
    for x in range(-12, 13):
        for y in range(-12, 13):
            if "pescado" in service._zone_resources(x, y):
                goods = service._harvest_goods(x, y)
                assert "pescado" not in goods and goods                                # the fund takes no food
                return
    raise AssertionError("no water zone near the Claro")
