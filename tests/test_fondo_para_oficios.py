"""The guild's fund for the professions (D-322, 0.47): works first, then the left-over at your camp's stations.

[ES] Pruebas de lo que pidió el dueño el 21-oct-2026 ("que los jugadores del gremio puedan primero construir las estructuras y
después poder utilizar los recursos para las profesiones de cada uno. Puedan utilizar los recursos del gremio"):
- primero las obras: lo que les falta a las obras activas y a ⏫ Siguiente nivel queda guardado (la reserva) y nunca se usa
  para oficios; solo lo que sobra;
- en las estaciones de TU campamento la receta toma primero de la mochila y después de lo que sobra del fondo; la lista con
  código (/r1) lo cuenta (✅💰) y la receta dice cuánto pondría el fondo;
- el tope por día real de cada miembro, el registro 📜 Quién usó qué y el interruptor 🔓/🔒 que solo mueven el fundador o un
  🤝 asistente;
- no vale en las fogatas, ni para quien no es miembro del campamento (visitante o quien espera lugar en el gremio, D-294);
- las pantallas en inglés.
Archivo: tests/test_fondo_para_oficios.py · Módulo: M14 Oficios y M15 Social · Prueba: engine/service/gremio.py (_fund_reserve,
_fund_surplus, _fund_pool, _fund_take, _fund_craft_lines, _fund_craft_toggle, _fund_log_view, _guild_funds_view),
engine/service/game.py (_recipe_status, _station_view, _recipe_view, _make) y engine/professions/rules.py (fund_draw, max_times).
"""

import pytest

from conftest import make_hero
from engine.professions import fund_draw, max_times
from test_camp_upgrades import build, camp_at, set_hero
from test_camps import place
from test_guilds import join

# D-257 (0.33): these tests are about crafting with the fund; learning a profession has its own tests.
pytestmark = pytest.mark.usefixtures("every_profession_known")

KEY = "6:0"


def ids(view):
    return [a.id for a in view.actions]


def text(view):
    return "\n".join([view.notice or ""] + view.body)


def put_fund(service, fund, **extra):
    """Write the camp's fund (and other fields of its record) straight in the store."""
    record = service._upgrades(KEY)
    record["fund"] = dict(fund)
    record.update(extra)
    service.store.put("upgrades", KEY, record)


def camp_with_sawmill(service, english=False):
    """Lyra founds the camp at 6:0 (level 1) with a 🪚 Aserradero; Bram joins and stands at its center with nothing."""
    make_hero(service, "test:1", "Lyra")
    if english:
        from test_idiomas import english_hero
        english_hero(service, "test:2", "Bram")
    else:
        make_hero(service, "test:2", "Bram")
    camp_at(service, 1)
    join(service, "test:2")
    build(service, "aserradero")
    place(service, "test:2", 6, 0, backpack={}, energy=50)
    set_hero(service, "test:1", backpack={})
    return service.store.get("camp", KEY)


def wood_reserve(service, camp):
    """What the next level asks of 🪵 madera at level 1 (and nothing active yet): the reserve of a fresh camp."""
    return service._lvlup_need(int(camp.get("level", 1))).get("madera", 0)


def test_pure_helpers_take_the_backpack_first_and_never_pass_the_cap():
    recipe = {"inputs": {"madera": 3, "fibra": 1}, "energy": 1}
    assert fund_draw(recipe, {"madera": 1}, {"madera": 10, "fibra": 5}) == {"madera": 2, "fibra": 1}
    assert fund_draw(recipe, {"madera": 9, "fibra": 3}, {"madera": 10}, times=3) == {}          # the backpack is enough
    assert fund_draw(recipe, {}, {"madera": 4}, times=2) == {"madera": 4}                       # never more than the fund has
    assert max_times(recipe, {"madera": 3, "fibra": 1}, 50) == 1                                 # as before without a fund
    assert max_times(recipe, {"madera": 3, "fibra": 1}, 50, {"madera": 30, "fibra": 10}) == 11
    # the daily cap counts every unit the fund puts in, all materials together: 2 times take 3 + 1 = 4, 3 times 6 + 2 = 8 > 6
    assert sum(fund_draw(recipe, {"madera": 3, "fibra": 1}, {"madera": 30, "fibra": 10}, 2).values()) == 4
    assert sum(fund_draw(recipe, {"madera": 3, "fibra": 1}, {"madera": 30, "fibra": 10}, 3).values()) == 8
    assert max_times(recipe, {"madera": 3, "fibra": 1}, 50, {"madera": 30, "fibra": 10}, fund_cap=6) == 2
    assert max_times(recipe, {}, 50, {"madera": 30, "fibra": 10}, fund_cap=7) == 1
    assert max_times(recipe, {}, 2, {"madera": 30, "fibra": 10}) == 2                            # energy still rules


def test_the_reserve_keeps_what_the_works_and_the_next_level_lack(service):
    camp = camp_with_sawmill(service)
    need_level = service._lvlup_need(1)
    put_fund(service, {"madera": 100, "piedra": 10}, active=["fogon"])
    record = service._upgrades(KEY)
    need_work = service._upgrade_need(service._upgrade_catalog()["fogon"], service._camp_perks(camp), record, "fogon")
    reserve = service._fund_reserve(camp, record)
    assert reserve["madera"] == need_work["madera"] + need_level["madera"]
    assert reserve["piedra"] == need_work["piedra"] + need_level["piedra"]
    surplus = service._fund_surplus(camp, record)
    assert surplus == {"madera": 100 - reserve["madera"]} and "piedra" not in surplus      # stone is all kept
    # what a work already got is no longer kept: give the 🔥 Fogón its wood and the reserve drops
    record["works"]["fogon"] = {"madera": need_work["madera"]}
    service.store.put("upgrades", KEY, record)
    assert service._fund_reserve(camp, service._upgrades(KEY))["madera"] == need_level["madera"]
    view = service.act("test:2", "gfunds")
    body = text(view)
    assert "🔓 abierto" in body and "Guardado para las obras y el nivel" in body and "Sobra para oficios" in body
    assert ids(view) == ["gfund", "gflog", "guild"]                     # a common member: no switch
    assert ids(service.act("test:1", "gfunds")) == ["gfund", "gflog", "gfcraft", "guild"]      # the founder: 🔒 Cerrar
    assert not service.texts.missing


def test_the_recipe_takes_the_backpack_first_then_the_left_over_never_the_reserve(service):
    camp = camp_with_sawmill(service)
    keep = wood_reserve(service, camp)
    put_fund(service, {"madera": keep + 30})
    set_hero(service, "test:2", backpack={"madera": 2})
    view = service.act("test:2", "rec:tablon:0")
    body = text(view)
    assert "✅ 🪵 Madera: 2/3 +💰1" in body and "💰 Del fondo del gremio, por vez: 🪵 Madera ×1" in body
    assert "Hoy puedes tomar 40 más" in body
    assert "mk:tablon:10:0" in ids(view) and "mk:tablon:10:0" == f"mk:tablon:{(2 + 30) // 3}:0"   # 32 wood → 10 times
    view = service.act("test:2", "mk:tablon:4:0")                     # 12 wood: 2 from the backpack, 10 from the fund
    hero = service._load("test:2")
    assert "madera" not in hero.backpack and hero.backpack["tablon"] >= 4
    assert service._upgrades(KEY)["fund"] == {"madera": keep + 20}
    assert "💰 Del fondo del gremio: 🪵 Madera ×10 · hoy llevas 10 de 40" in view.notice
    service.act("test:2", f"mk:tablon:{20 // 3}:0")                   # the rest of the left-over: 18 of the 20
    assert service._upgrades(KEY)["fund"] == {"madera": keep + 2}
    view = service.act("test:2", "rec:tablon:0")                      # 2 left over: not enough for one, the reserve stays
    assert not any(a.id.startswith("mk:") for a in view.actions) and "Te falta" in text(view)
    view = service.act("test:2", "mk:tablon:1:0")
    assert "Te falta" in view.notice and service._upgrades(KEY)["fund"] == {"madera": keep + 2}
    assert not service.texts.missing


def test_the_recipe_list_counts_the_left_over(service):
    camp = camp_with_sawmill(service)
    keep = wood_reserve(service, camp)
    view = service.act("test:2", "est:refine:0")
    assert any(line.startswith("/r1 ▫️ 🟫 Tablón") for line in view.body)        # nothing carried, nothing in the fund
    assert not any("fondo del gremio" in line for line in view.body)
    put_fund(service, {"madera": keep + 2})                                      # 2 left over: something, not enough
    assert any(line.startswith("/r1 🔸 🟫 Tablón") for line in service.act("test:2", "est:refine:0").body)
    put_fund(service, {"madera": keep + 3})
    view = service.act("test:2", "est:refine:0")
    assert any(line.startswith("/r1 ✅💰 🟫 Tablón") for line in view.body)
    assert any("Cuenta lo que sobra en el fondo del gremio" in line for line in view.body)
    only = service.act("test:2", "esto:refine:0")                               # ✅ Solo las que puedo hacer: with the fund
    assert any(line.startswith("/r1 ✅💰 🟫 Tablón") for line in only.body)
    assert service.text("test:2", "/r1").kind == "recipe"
    set_hero(service, "test:2", backpack={"madera": 3})                         # the backpack alone: a plain ✅
    assert any(line.startswith("/r1 ✅ 🟫 Tablón") for line in service.act("test:2", "est:refine:0").body)
    assert not service.texts.missing


def test_the_daily_cap_and_a_new_day(service, clock):
    camp = camp_with_sawmill(service)
    service.content.balance["fund_crafts"]["daily_cap"] = 7
    keep = wood_reserve(service, camp)
    put_fund(service, {"madera": keep + 30})
    view = service.act("test:2", "rec:tablon:0")
    assert "mk:tablon:2:0" in ids(view) and "mk:tablon:5:0" not in ids(view)      # 7 a day: 2 tablones (6 wood)
    view = service.act("test:2", "mk:tablon:3:0")                                # 9 > 7: nothing spent
    assert "solo puedes tomar 7 más hoy" in view.notice and service._upgrades(KEY)["fund"] == {"madera": keep + 30}
    service.act("test:2", "mk:tablon:2:0")
    assert service._fund_used(service._upgrades(KEY), "test:2") == 6
    view = service.act("test:2", "est:refine:0")
    assert any(line.startswith("/r1 🔸 🟫 Tablón") for line in view.body)       # 1 left today: not enough for one
    set_hero(service, "test:2", backpack={"madera": 2})                         # 2 of mine + 1 of the fund = 1 make
    assert "🪵 Madera ×1 · hoy llevas 7 de 7" in service.act("test:2", "mk:tablon:1:0").notice
    assert service._fund_used(service._upgrades(KEY), "test:2") == 7
    view = service.act("test:2", "est:refine:0")
    assert any("Ya tomaste hoy los 7" in line for line in view.body)
    view = service.act("test:2", "rec:tablon:0")                                 # the fund covers it, the cap does not
    assert "+💰3" in text(view) and "solo puedes tomar 0 más hoy" in text(view)
    assert not any(a.id.startswith("mk:") for a in view.actions)
    assert service._fund_used(service._upgrades(KEY), "test:1") == 0            # the cap is per member
    clock.advance(service._day_seconds())                                       # a new real day: from zero
    assert service._fund_used(service._upgrades(KEY), "test:2") == 0
    assert "mk:tablon:2:0" in ids(service.act("test:2", "rec:tablon:0"))
    assert not service.texts.missing


def test_only_the_founder_or_an_assistant_opens_or_closes_it_and_the_log_says_who(service):
    camp = camp_with_sawmill(service)
    keep = wood_reserve(service, camp)
    put_fund(service, {"madera": keep + 30})
    service.act("test:2", "mk:tablon:2:0")
    view = service.act("test:2", "gfcraft")                                      # a common member: no
    assert "Solo el fundador o un 🤝 asistente" in view.notice and service._fund_open(service._upgrades(KEY))
    view = service.act("test:1", "gfcraft")                                      # the founder closes it
    assert "Cerraste" in view.notice and not service._fund_open(service._upgrades(KEY))
    assert "gfcraft" in ids(view) and "🔒 cerrado" in text(view)
    view = service.act("test:2", "est:refine:0")
    assert any("está cerrado" in line for line in view.body) and any(line.startswith("/r1 ▫️") for line in view.body)
    view = service.act("test:2", "mk:tablon:1:0")
    assert "Te falta" in view.notice and service._upgrades(KEY)["fund"] == {"madera": keep + 24}   # closed: nothing taken
    camp = service.store.get("camp", KEY)
    camp["helpers"] = ["test:2"]                                                # Bram becomes a 🤝 assistant
    service.store.put("camp", KEY, camp)
    view = service.act("test:2", "gfcraft")
    assert "Abriste" in view.notice and service._fund_open(service._upgrades(KEY))
    log = service.act("test:1", "gflog")
    assert log.kind == "fund_log" and ids(log) == ["gfunds"]
    lines = [line for line in log.body if line.startswith(("🛠️", "🔓", "🔒"))]
    assert lines[0].startswith("🔓 Bram abrió") and lines[1].startswith("🔒 Lyra cerró")
    assert lines[2].startswith("🛠️ Bram: 🪵 Madera ×6 → 🟫 Tablón ×2")
    service.content.balance["fund_crafts"]["log_kept"] = 2                      # only the last log_kept lines are kept
    service.act("test:1", "gfcraft")
    assert [e["k"] for e in service._upgrades(KEY)["fund_log"]] == ["open", "close"]
    assert not service.texts.missing


def test_not_at_the_campfires_nor_for_who_is_not_a_member(service):
    camp = camp_with_sawmill(service)
    keep = wood_reserve(service, camp)
    put_fund(service, {"madera": keep + 30})
    place(service, "test:2", 0, 0, backpack={"madera": 1})                      # the Claro has every station, not the fund
    view = service.act("test:2", "rec:tablon:0")
    assert "+💰" not in text(view) and not any(a.id.startswith("mk:") for a in view.actions)
    assert any(line.startswith("/r1 🔸 🟫 Tablón") for line in service.act("test:2", "est:refine:0").body)
    assert "Te falta" in service.act("test:2", "mk:tablon:1:0").notice
    assert service._upgrades(KEY)["fund"] == {"madera": keep + 30}
    make_hero(service, "test:3", "Cora")                                        # a visitor at the camp: no stations at all
    place(service, "test:3", 6, 0, backpack={"madera": 1})
    hero = service._load("test:3")
    assert service._stations_here(hero) == ([], None) and service._fund_pool(hero, "camp") is None
    camp = service.store.get("camp", KEY)                                       # D-294: waiting for room in the guild
    camp["waiting"] = ["test:3"]
    service.store.put("camp", KEY, camp)
    service.store.put("camp_wait", "test:3", {"camp": KEY})
    assert service._fund_pool(service._load("test:3"), "camp") is None
    view = service.act("test:3", "gfunds")
    assert view.kind == "guild_funds" and "gfcraft" not in ids(view)
    assert service._upgrades(KEY)["fund"] == {"madera": keep + 30}
    assert not service.texts.missing


def test_it_reads_well_in_english(service):
    camp = camp_with_sawmill(service, english=True)
    keep = wood_reserve(service, camp)
    put_fund(service, {"madera": keep + 30})
    set_hero(service, "test:2", backpack={"madera": 1})
    camp = service.store.get("camp", KEY)
    camp["helpers"] = ["test:2"]
    service.store.put("camp", KEY, camp)
    lst = service.act("test:2", "est:refine:0")
    assert any("✅💰" in line for line in lst.body) and any("guild's fund counts" in line for line in lst.body)
    recipe = service.act("test:2", "rec:tablon:0")
    assert "From the guild's fund, each time: 🪵 Wood ×2" in text(recipe)
    made = service.act("test:2", "mk:tablon:2:0")
    assert "From the guild's fund: 🪵 Wood ×5 · 5 of 40 today" in made.notice
    funds = service.act("test:2", "gfunds")
    assert "Fund for professions: 🔓 open" in text(funds) and "Kept for the works and the level" in text(funds)
    assert service.act("test:2", "gfcraft").notice.startswith("🔒 You closed")
    log = service.act("test:2", "gflog")
    assert any(line.startswith("🛠️ Bram: 🪵 Wood ×5 → 🟫 Plank ×2") for line in log.body)
    assert any("Bram closed the fund" in line for line in log.body)
    for view in (lst, recipe, made, funds, log):
        assert "[" not in text(view).replace("[ES]", ""), text(view)
    assert not service.texts.fallbacks.get("en"), sorted(service.texts.fallbacks.get("en", []))[:20]
    assert not service.texts.missing
