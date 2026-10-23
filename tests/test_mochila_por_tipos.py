"""The backpack counts item types, not units, and the 🎒 profession backpacks (D-338, confirmed; how: D-339, provisional; 0.62).

[ES]
Pruebas de la mochila por tipos que pidió el dueño (D-338, 23-oct-2026: "quiero poder farmear mucho más, aunque tarde, y que el
límite sea el inventario"): 50 tipos distintos y 30 de cada uno; el equipo suelto aparte con su tope (20); el cinturón y lo puesto
no cuentan; las 🎒 mochilas de oficio (40 y 50 por tipo, sus recursos no ocupan tipos, hasta 3 de oficios distintos, se hacen
desde el rango 5 y el 40 en las 🔥 Fogatas y el 🔥 Fogón, se ponen y se quitan desde 🎒 Mochila); quien ya pasa un tope lo
conserva todo y solo no suma más; recolectar y sus lotes se cortan en el tope; el botín (D-90) entra igual; 📦 Entregas respeta
los topes; el mercader, las recetas, el 🏛️ Mercado y los 📜 pedidos; y los textos en los dos idiomas.
Archivo: tests/test_mochila_por_tipos.py · Módulo: M4 Equipo e inventario (con M14 Oficios) · Prueba: engine/service/backpack.py
"""

import re

import pytest
from conftest import make_hero
from engine.core import Rng
from engine.hero import Hero
from engine.professions import xp_for_rank
from engine.service.backpack import PBAG_CODE_RE
from engine.service.craft_orders import CRAFT_ORDER_CODE_RE
from engine.service.game import (COORD_RE, FAQ_CODE_RE, GEAR_CODE_RE, PLACE_CODE_RE, RECIPE_CODE_RE, RECON_CODE_RE,
                                 RESOURCE_CODE_RE, SELL_CODE_RE)
from engine.service.gremio import (ARMORY_IN_RE, ARMORY_OUT_RE, FUND_CODE_RE, GUILD_CODE_RE, MEMBER_CODE_RE, PLAYER_CODE_RE,
                                   ZONE_CODE_RE)
from engine.service.map_scroll import SCROLL_CODE_RE
from engine.service.market import market_code
from engine.service.repair import REPAIR_CODE_RE
from test_camps import found_at, place

ACC = "test:1"
HERBS = "herbolario"


def materials(service, n, skip=()):
    """`n` materials with a resource code, not in `skip` (one type each)."""
    out = [i for i, it in service.content.items.items() if it.get("kind") == "material" and it.get("code") and i not in skip]
    assert len(out) >= n
    return out[:n]


def herb_items(service):
    return set(service._pbag_resources(HERBS))


def rank_xp(service, rank):
    return xp_for_rank(service.content.balance["professions"]["rank_formula"], rank)


def hero_with(service, account=ACC, **values):
    hero = service._load(account)
    for key, value in values.items():
        setattr(hero, key, value)
    service._save(hero)
    return service._load(account)


def full_types(service, hero, skip=(), extra=0):
    """A backpack with every general type used (plus `extra` over), one unit each, never the items in `skip`."""
    return {i: 1 for i in materials(service, service._bag_types_cap(hero) + extra, skip=set(skip))}


class StubRng:
    """An exploration in the Claro that finds the first item of its list (🌿 hierba curativa)."""

    def random(self):
        return 0.5

    def uniform(self, low, high):
        return low

    def pick_weighted(self, options, weights):
        return options[0]

    def chance(self, probability):
        return False


# ---------------------------------------------------------------- the numbers (D-338)


def test_the_owner_numbers_are_in_balance_and_the_old_space_is_kept_retired(content):
    pack = content.balance["hero"]["backpack"]
    assert (pack["types"], pack["per_type"], pack["gear_pieces"], pack["prof_slots"]) == (50, 30, 20, 3)
    assert content.balance["hero"]["backpack_capacity"] == 60                     # retired, never deleted (history)
    defs = content.balance["prof_backpacks"]["items"]
    assert len(defs) == 10 and all(iid in content.items and content.items[iid]["kind"] == "prof_bag" for iid in defs)
    assert sorted({d["per_type"] for d in defs.values()}) == [40, 50]
    assert {d["profession"] for d in defs.values()} == {"lenador", "minero", "herbolario", "pescador", "desollador"}
    recipes = content.professions["recipes"]
    for iid, d in defs.items():                                                    # each profession makes its own
        rdef = recipes[iid]
        assert rdef["profession"] == d["profession"] and rdef["output"] == {iid: 1}
        assert rdef["min_rank"] == (5 if d["per_type"] == 40 else 40)
        assert any(i not in content.professions["professions"][d["profession"]].get("gathers", [])
                   + content.professions["professions"][d["profession"]].get("skins", []) for i in rdef["inputs"])


def test_fifty_types_and_thirty_of_each(service):
    make_hero(service)
    hero = hero_with(service, backpack={"madera": 29})
    assert service._bag_room(hero, "madera") == 1 and service._bag_room(hero, "piedra") == 30
    hero = hero_with(service, backpack={"madera": 30})
    assert service._bag_room(hero, "madera") == 0                                  # its type is full
    bag = full_types(service, hero, skip={"piedra"})
    hero = hero_with(service, backpack=bag)
    assert service._bag_types_used(hero) == 50 and service._bag_full(hero)
    assert service._bag_room(hero, "piedra") == 0                                  # a new type: none free
    some = next(iter(bag))
    assert service._bag_room(hero, some) == 29                                     # more of what you carry still fits
    assert 50 * 30 == service._pack_types() * service._pack_per_type()             # 1,500 at most


def test_gear_is_counted_apart_with_its_own_cap(service):
    make_hero(service)
    gear = [i for i, it in service.content.items.items() if it.get("kind") == "gear" and not it.get("source")][:3]
    hero = hero_with(service, backpack={gear[0]: 19, gear[1]: 1})
    assert service._bag_gear_used(hero) == 20 and service._bag_types_used(hero) == 0     # pieces never take a type
    assert service._bag_room(hero, gear[2]) == 0 and service._bag_room(hero, "madera") == 30
    assert "Equipo suelto lleno (20/20)" in service._bag_why(hero, [gear[2]])
    assert service._bag_no_room(hero, gear[2]).startswith("🛡️ Ya llevas 20/20 piezas de equipo sueltas")
    hero = hero_with(service, backpack={gear[0]: 5})
    assert service._bag_room(hero, gear[2]) == 15


def test_the_belt_and_worn_gear_never_count(service):
    make_hero(service)
    hero = service._load(ACC)
    assert hero.gear and hero.belt                                                  # starter gear on, belt filled
    hero = hero_with(service, backpack={})
    assert service._bag_types_used(hero) == 0 and service._bag_gear_used(hero) == 0
    view = service.act(ACC, "bag")
    assert "🎒 Mochila: 0/50 tipos (hasta 30 de cada uno) · 🛡️ Equipo suelto: 0/20" in view.body
    assert any("lo puesto y el cinturón no cuentan" in line for line in view.body)


# ---------------------------------------------------------------- 🎒 profession backpacks (D-338.2, D-338.3, D-339)


def test_a_profession_backpack_raises_its_resources_and_frees_their_types(service):
    make_hero(service)
    hero = service._load(ACC)
    bag = dict(list(full_types(service, hero, skip=herb_items(service)).items())[:-2])
    bag["hierba_curativa"] = 30
    hero = hero_with(service, backpack=dict(bag, mochila_herbolario=1))
    assert service._bag_types_used(hero) == 50                                      # 48 + the herbs + the backpack itself
    assert service._bag_room(hero, "hierba_curativa") == 0 and service._bag_room(hero, "setas") == 0
    view = service.text(ACC, "/mp1")                                                # put it on from 🎒 Mochilas de oficio
    hero = service._load(ACC)
    assert hero.prof_bags == ["mochila_herbolario"] and "mochila_herbolario" not in hero.backpack
    assert "Te pusiste la 🎒 Mochila de herbolario" in view.notice and "hasta 40 de cada uno" in view.notice
    assert service._bag_room(hero, "hierba_curativa") == 10                        # 30 → 40
    assert service._bag_room(hero, "setas") == 40                                   # a new herb type: its compartment
    assert service._bag_types_used(hero) == 48                                      # the herbs and the backpack left the types
    fresh = materials(service, 1, skip=set(bag) | herb_items(service))[0]
    assert service._bag_room(hero, fresh) == 30                                     # and freed room for anything new
    hero = hero_with(service, prof_bags=["mochila_herbolario_grande"])
    assert service._bag_room(hero, "hierba_curativa") == 20 and service._bag_type_cap(hero, "musgo") == 50   # the large: 50
    body = "\n".join(service.act(ACC, "resources").body)
    assert "🌿 Hierba curativa 30/50 🎒" in body and "🎒 = va en tu mochila de oficio: no ocupa tipo." in body


def test_up_to_three_backpacks_of_different_professions(service):
    make_hero(service)
    hero_with(service, backpack={"mochila_lenador": 1, "mochila_minero": 1, "mochila_herbolario": 1, "mochila_pescador": 1})
    for _ in range(3):
        service.text(ACC, "/mp1")
    hero = service._load(ACC)
    assert hero.prof_bags == ["mochila_lenador", "mochila_minero", "mochila_herbolario"]
    view = service.text(ACC, "/mp1")
    assert "Ya llevas 3 mochilas de oficio" in view.notice and service._load(ACC).backpack["mochila_pescador"] == 1
    pockets = service._pbag_pockets(service._load(ACC))
    assert pockets["madera"] == pockets["piedra"] == pockets["setas"] == 40 and "pescado" not in pockets


def test_put_on_take_off_and_swap_from_the_backpack_screen(service):
    make_hero(service)
    hero_with(service, backpack={"mochila_herbolario": 1, "mochila_herbolario_grande": 1, "hierba_curativa": 35})
    view = service.act(ACC, "bag")
    assert [a.id for a in view.actions][-1] == "pbags"
    view = service.act(ACC, "pbags")
    assert view.kind == "prof_bags" and [a.id for a in view.actions] == ["bag"]
    assert "/mp1 🎒 Mochila de herbolario ×1 · 🌿 Herbolario · 40 por tipo" in view.body
    assert "/mp2 🎒 Mochila grande de herbolario ×1 · 🌿 Herbolario · 50 por tipo" in view.body
    service.text(ACC, "/mp1")
    view = service.text(ACC, "/mp1")                                                # the large one: same profession, a swap
    hero = service._load(ACC)
    assert hero.prof_bags == ["mochila_herbolario_grande"] and hero.backpack["mochila_herbolario"] == 1
    assert "La 🎒 Mochila de herbolario volvió a la mochila." in view.notice
    assert "/mq1 🎒 Mochila grande de herbolario · 🌿 Herbolario · 50 por tipo · 1 tipo de su oficio contigo" in view.body
    view = service.text(ACC, "/mq1")                                                # take it off: back in the backpack
    hero = service._load(ACC)
    assert hero.prof_bags == [] and hero.backpack["mochila_herbolario_grande"] == 1 and hero.backpack["hierba_curativa"] == 35
    assert "Te quitaste la 🎒 Mochila grande de herbolario" in view.notice
    assert "Pasas un tope: no pierdes nada" in view.notice                         # 35 > 30 now: kept, only blocked
    assert service._bag_room(hero, "hierba_curativa") == 0
    assert service.text(ACC, "/mq5").notice == "⚠️ /mq5 no está en la lista: mírala otra vez."
    assert service.text(ACC, "/mochilas").kind == "prof_bags" and service.text(ACC, "/backpacks").kind == "prof_bags"


def test_old_heroes_load_without_profession_backpacks(service):
    make_hero(service)
    data = service.store.get("hero", ACC)
    data.pop("prof_bags", None)
    service.store.put("hero", ACC, data)
    assert Hero.from_dict(data).prof_bags == [] and service._load(ACC).prof_bags == []


# ---------------------------------------------------------------- crafting them (D-339)


def crafter(service, rank, account=ACC, **values):
    make_hero(service, account)
    return hero_with(service, account, learned=[HERBS, "lenador"], professions={HERBS: rank_xp(service, rank),
                                                                                "lenador": rank_xp(service, rank)},
                     energy=50, **values)


def test_each_level_is_made_from_its_rank_at_any_fire(service):
    crafter(service, 4, backpack={"hierba_curativa": 30, "fibra": 30, "cuero_curtido": 10, "tela_tejida": 10})
    view = service.act(ACC, "mk:mochila_herbolario:1:0")
    assert "rango 5" in (view.notice or "") and service._load(ACC).backpack.get("mochila_herbolario") is None
    hero_with(service, professions={HERBS: rank_xp(service, 5)})
    listed = "\n".join(service.act(ACC, "est:craft:0").body)
    assert "Mochila de herbolario" in listed and "Mochila grande de herbolario" not in listed   # 🛠️ Fabricar lists it
    view = service.act(ACC, "mk:mochila_herbolario:1:0")
    hero = service._load(ACC)
    assert hero.prof_bags == ["mochila_herbolario"]                                 # the first one goes on by itself
    assert hero.backpack["hierba_curativa"] == 22 and hero.backpack["fibra"] == 22 and hero.backpack["cuero_curtido"] == 8
    assert "Te la pusiste" in view.notice
    view = service.act(ACC, "mk:mochila_herbolario_grande:1:0")
    assert "rango 40" in (view.notice or "")
    hero_with(service, professions={HERBS: rank_xp(service, 40)}, backpack={"hierba_curativa": 30, "fibra": 30,
                                                                             "cuero_curtido": 10, "tela_tejida": 10})
    assert service._load(ACC).recipe_books == []
    view = service.act(ACC, "mk:mochila_herbolario_grande:1:0")                     # rank 40, no 📚 book asked
    hero = service._load(ACC)
    assert hero.prof_bags == ["mochila_herbolario_grande"] and hero.backpack["mochila_herbolario"] == 1   # better: a swap
    assert not service._book_missing(hero, service.content.professions["recipes"]["mochila_herbolario_grande"])


def test_backpacks_are_made_at_the_fire_only(service):
    crafter(service, 10, backpack={"madera": 30, "cuero_curtido": 10})
    place(service, ACC, 3, 0)
    view = service.act(ACC, "mk:mochila_lenador:1:0")
    assert "🔥 Las mochilas de oficio se hacen al fuego" in view.notice and "mochila_lenador" not in service._load(ACC).backpack
    assert "lenador" not in service._stations_here(service._load(ACC))[0]
    place(service, ACC, 0, 0)
    assert "lenador" in service._stations_here(service._load(ACC))[0]               # any 🔥 Fogata


def test_the_camp_hearth_is_a_fire_too(service):
    make_hero(service)
    found_at(service, ACC, 6, 0)
    hero = service._load(ACC)
    stations, where = service._stations_here(hero)
    assert where is None or "lenador" not in stations
    record = service._upgrades("6:0")
    record["built"].update({"fogon": 0.0})
    service.store.put("upgrades", "6:0", record)
    stations, where = service._stations_here(service._load(ACC))
    assert where == "camp" and {"cocina", "lenador", "herbolario"} <= set(stations)
    line = service._stations_line(where, stations)
    assert "Cocina" in line and "Leñador" not in line                               # not a building's station


def test_a_full_backpack_still_makes_the_backpack_that_goes_on(service):
    crafter(service, 5)
    hero = service._load(ACC)
    bag = full_types(service, hero, skip={"hierba_curativa", "fibra", "cuero_curtido"} | herb_items(service))
    bag = dict(list(bag.items())[:-3], hierba_curativa=30, fibra=30, cuero_curtido=10)
    hero = hero_with(service, backpack=bag)
    assert service._bag_full(hero)
    used = service._bag_types_used(hero)
    view = service.act(ACC, "mk:mochila_herbolario:1:0")
    hero = service._load(ACC)
    assert hero.prof_bags == ["mochila_herbolario"], view.notice                   # it went on: no room needed
    assert service._bag_types_used(hero) == used - 2                                # 🌿 and 🧵 moved to its compartment
    view = service.act(ACC, "mk:mochila_herbolario:1:0")                            # a second one: into the backpack
    assert service._load(ACC).backpack.get("mochila_herbolario") == 1 and "Póntela" in view.notice


def test_a_recipe_whose_result_does_not_fit_spends_nothing(service, every_profession_known):
    make_hero(service)
    hero = hero_with(service, backpack={"madera": 30, "tablon": 30}, energy=50,
                     professions={"aserradero": rank_xp(service, 1)})
    view = service.act(ACC, "mk:tablon:1:0")
    hero = service._load(ACC)
    assert hero.backpack == {"madera": 30, "tablon": 30} and hero.energy == 50
    assert "Llenos: 🟫 Tablón 30/30." in view.notice
    hero = hero_with(service, backpack={"madera": 30, "tablon": 28})
    view = service.act(ACC, "rec:tablon:0")
    assert "🎒 Por el lugar en la mochila puedes hacer 2 ahora." in view.body
    assert {a.id for a in view.actions} >= {"mk:tablon:2:0"} and "mk:tablon:5:0" not in {a.id for a in view.actions}


def test_backpacks_sell_on_the_market_and_can_be_ordered(service):
    make_hero(service)
    assert service._mkt_category("mochila_lenador") == "packs"
    cats = service.act(ACC, "mkt:cats")
    assert len(cats.actions) == 10 and any("🎒 Mochilas de oficio" in a.label for a in cats.actions)
    assert {"lenador", "minero", "herbolario", "pescador", "desollador"} <= set(service._corder_profs())
    assert service._corder_recipe("mochila_minero_grande") is not None
    assert service._corder_books(service.content.professions["recipes"]["mochila_minero_grande"]) == []


# ---------------------------------------------------------------- over the cap, nothing is lost (D-338.4, D-90)


def test_a_hero_over_the_caps_keeps_everything_and_cannot_add_more(service):
    make_hero(service)
    hero = service._load(ACC)
    bag = full_types(service, hero, skip={"madera", "piedra"}, extra=4)
    bag["madera"] = 45
    hero = hero_with(service, backpack=dict(bag), gold=100)
    hero = service._load(ACC)
    assert hero.backpack == bag                                                     # loading takes nothing away
    assert service._bag_room(hero, "madera") == 0 and service._bag_room(hero, "piedra") == 0
    view = service.act(ACC, "bag")
    assert "🎒 Pasas un tope: no pierdes nada, pero hasta bajar de él no entra más de eso." in view.body
    view = service.act(ACC, "buy:pocion_vida")
    assert "No cabe en la mochila" in view.notice and service._load(ACC).gold == 100     # never charged
    hero = hero_with(service, backpack={i: n for i, n in bag.items() if i != "madera"} | {"madera": 29})
    hero = hero_with(service, backpack=dict(list(hero.backpack.items())[6:]))       # sold some: below the cap again
    assert service._bag_room(hero, "madera") == 1 and service._bag_room(hero, "piedra") == 30


def test_found_things_still_go_in_past_every_cap(service):
    make_hero(service)
    hero = service._load(ACC)
    bag = full_types(service, hero, skip={"hierba_curativa", "pieza_metal", "venda", "pocion_vida"})
    hero = hero_with(service, backpack=dict(bag))
    activity = {"log": [], "got": {}}
    assert service._explore_step(hero, service._zone(0, 0), StubRng(), activity) is None
    assert hero.backpack["hierba_curativa"] == 1                                     # a find: a new type past the cap
    assert service._bag_add(hero, "hierba_curativa", 40) == 40 and hero.backpack["hierba_curativa"] == 41   # D-90


# ---------------------------------------------------------------- gathering and its batches


def test_gathering_skips_a_full_type_and_stops_when_nothing_fits(service):
    make_hero(service)
    service.content.balance["gather"]["amount"] = [5, 5]                            # a fixed draw (test only)
    service.content.balance["gather"]["encounter_scale"] = 0                        # no ambush (test only)
    zone = service._zone(0, 0)
    claro = sorted(service._zone_resources(0, 0))
    full, other = claro[0], claro[1]
    hero = hero_with(service, backpack={full: 30, other: 27})
    activity = {"kind": "gather", "got": {}, "log": [], "until": 1.0, "done": 1, "left": 5}
    service._gather_step(hero, zone, Rng(3), activity)
    assert hero.backpack[full] == 30 and hero.backpack[other] == 30 and activity["got"] == {other: 3}
    assert full in activity["full"] and other in activity["full"]
    assert service._continue_batch(hero, activity, 2.0) == "bag_full"              # stops before charging the next round
    notice = service._gather_blocked(hero, zone)
    assert notice.startswith("🎒 No cabe más de lo que hay aquí. Llenos: ")
    assert "💡 Una 🎒 mochila de oficio" in notice                                  # a profession backpack would help


def test_a_batch_stops_cleanly_at_the_cap_and_says_why(service, clock):
    make_hero(service)
    claro = sorted(service._zone_resources(0, 0))
    hero = hero_with(service, backpack={claro[0]: 30, claro[1]: 26}, energy=50)
    service.act(ACC, "do:gather:20")
    pushes = []
    for _ in range(6):
        clock.advance(3600)
        pushes += [v for acc, v in service.tick() if acc == ACC]
    hero = service._load(ACC)
    assert hero.activity is None and hero.backpack[claro[1]] == 30 and hero.backpack[claro[0]] == 30
    assert len(pushes) == 1
    notice = pushes[0].notice
    done = int(re.search(r"Recolectaste (\d+)", notice).group(1))
    assert done <= 3                                                                 # it stopped at the cap, not after 20
    assert "🎒 El lote terminó: en la mochila ya no cabe nada más de lo que hay en esta zona." in notice
    assert "Ya no caben más:" in notice and "Lo demás siguió entrando" not in notice


def test_talar_and_pescar_say_how_much_of_their_resource_fits(service):
    make_hero(service)
    hero_with(service, backpack={"madera": 12})
    view = service.act(ACC, "chop")
    assert view.kind == "batch" and "🪵 Madera: 12/30 en la mochila" in view.body
    hero_with(service, backpack={"madera": 30})
    view = service.act(ACC, "chop")
    assert view.kind == "explore_menu" and "Llenos: 🪵 Madera 30/30." in view.notice


# ---------------------------------------------------------------- 📦 Entregas and the trader


def test_deliveries_respect_the_types_and_the_gear_cap(service, clock):
    make_hero(service)
    hero = service._load(ACC)
    gear = [i for i, it in service.content.items.items() if it.get("kind") == "gear" and not it.get("source")][:2]
    bag = full_types(service, hero, skip={"pocion_vida"})
    bag[gear[0]] = 20
    hero_with(service, backpack=dict(bag))
    now = clock.now()
    service._mkt_box_put(ACC, [{"good": "pocion_vida", "n": 5, "at": now, "from": "Bram", "why": "bought"},
                               {"good": gear[1], "n": 1, "at": now, "from": "Bram", "why": "bought"},
                               {"good": next(iter(bag)), "n": 40, "at": now, "from": "Bram", "why": "bought"}])
    view = service.act(ACC, "mkt:get")
    hero = service._load(ACC)
    assert "pocion_vida" not in hero.backpack and gear[1] not in hero.backpack
    assert hero.backpack[next(iter(bag))] == 30                                       # up to its type's cap
    left = {e["good"]: e["n"] for e in service._mkt_box(ACC)}
    assert left == {"pocion_vida": 5, gear[1]: 1, next(iter(bag)): 11}                 # never lost: it waits
    assert "Sin tipos libres" in view.notice and "Equipo suelto lleno (20/20)" in view.notice


def test_the_trader_sells_up_to_the_type_cap(service):
    make_hero(service)
    hero_with(service, backpack={"pocion_vida": 30}, belt={"pocion_vida": 3, "venda": 2}, gold=500)
    view = service.act(ACC, "buy:pocion_vida")
    hero = service._load(ACC)
    assert "Llenos: 🧪 Poción de vida 30/30." in view.notice and hero.gold == 500
    view = service.act(ACC, "buy:venda")                                             # another type still fits
    assert service._load(ACC).backpack.get("venda") == 1


# ---------------------------------------------------------------- both languages and ❓ /d67


@pytest.mark.parametrize("lang", ["es", "en"])
def test_texts_in_both_languages(content, lang):
    texts = content.locales[lang]
    for key in ("space", "space_full", "gather_block", "no_room", "gear_full", "hint", "pbags_title", "pbag_on", "pbag_off"):
        assert texts["pack"].get(key), (lang, key)
    for iid in content.balance["prof_backpacks"]["items"]:
        assert texts["item"].get(iid), (lang, iid)
    assert texts["faq"]["d67"]["q"] and texts["market"]["cat"]["packs"]


def test_an_english_player_reads_the_backpack_in_english(service):
    service.view(ACC)
    service.act(ACC, "lang:en")
    service.text(ACC, "Lyra")
    service.act(ACC, "grp:guerrero")
    service.act(ACC, "cls:guerrero_dps")
    hero_with(service, backpack={"mochila_minero": 1, "piedra": 3})
    view = service.act(ACC, "bag")
    assert any(line.startswith("🎒 Backpack: 2/50 types (up to 30 of each)") for line in view.body)
    assert view.actions[-1].label == "🎒 Profession backpacks"
    view = service.text(ACC, "/mp1")
    assert "You put on the 🎒 Miner's backpack" in view.notice and view.title == "🎒 Profession backpacks"
    assert "🪨 Stone 3/40 🎒" in "\n".join(service.act(ACC, "resources").body)
    answer = service.text(ACC, "/d67")
    assert "profession backpack" in "\n".join(answer.body).lower() and not service.texts.missing


def test_the_faq_explains_the_types_and_the_profession_backpacks(service):
    make_hero(service)
    d30 = "\n".join(service.text(ACC, "/d30").body)
    assert "hasta 50 tipos distintos" in d30 and "hasta 30 de cada uno" in d30 and "hasta 20 piezas" in d30
    d67 = "\n".join(service.text(ACC, "/d67").body)
    assert "desde el rango 5" in d67 and "desde el 40" in d67 and "hasta 40 de cada uno (la grande, 50)" in d67
    assert not service.texts.missing


def test_the_backpack_codes_never_clash_with_the_old_ones():
    for code in ("/mp1", "/mq2", "/mp_1", "/mq12", "/mp3@LostRealmsbot"):
        assert PBAG_CODE_RE.match(code)
        for other in (FAQ_CODE_RE, PLACE_CODE_RE, COORD_RE, SELL_CODE_RE, GEAR_CODE_RE, RESOURCE_CODE_RE, RECIPE_CODE_RE,
                      RECON_CODE_RE, SCROLL_CODE_RE, PLAYER_CODE_RE, GUILD_CODE_RE, MEMBER_CODE_RE, FUND_CODE_RE, ZONE_CODE_RE,
                      ARMORY_IN_RE, ARMORY_OUT_RE, REPAIR_CODE_RE, CRAFT_ORDER_CODE_RE):
            assert not other.match(code), (code, other.pattern)
        assert market_code(code) is None
    for code in ("/m1", "/mochilas", "/minero", "/pm1", "/q1", "/e1"):
        assert not PBAG_CODE_RE.match(code), code
