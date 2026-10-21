"""The recipe reform reaches every profession (0.52, D-306 confirmed; how it was applied: D-328, provisional).

[ES] Pruebas de la 0.52: el refinado (🪚 🔥 💧 🧶 🪣 🗿), la ⚗️ Alquimia, la 🩺 Medicina y la 🍲 Cocina tienen, como los oficios de
equipo desde la 0.44, una receta cada 5 rangos hasta el 100 con su color (🟧 🟨 🟩 ⬜). El refinado gana un refinado mejor por
tramo (vale más que el del tramo anterior); las pociones y los remedios curan más con el tramo (con la toxicidad de su receta
ancla, en el mismo lugar del cinturón) y los platos dan más raciones. Los ids de antes siguen (las obras del campamento y las
recetas los usan), la lista con código (/r1) los muestra agrupados por oficio con su tramo, el 💰 fondo del gremio puede poner
lo que falta y quien ya tenía rango recibe gratis los libros nuevos (D-64). Todo también en inglés.
Archivo: tests/test_tramos_refinado_alquimia_medicina_cocina.py · Módulo: M14 Oficios · Prueba: tools/recipe_tiers.py (el
contenido generado), content/balance.yaml recipe_tiers (professions, refine, consumables, book_gifts), content/professions.yaml,
content/items.yaml, engine/service/game.py (_tiered, _recipe_color, _recipe_xp, _station_view, _make, _refill_belt,
_belt_members, _grant_book_gifts, _sell_code), engine/hero/hero.py (book_gifts), engine/professions/rules.py (refined_from).
"""

import sys
from pathlib import Path

import pytest

from conftest import listed_recipes, make_hero
from engine.professions import rules, xp_for_rank

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import recipe_tiers  # noqa: E402

REFINE = ("aserradero", "fundicion", "destilacion", "tejeduria", "curtiduria", "canteria")
CONSUMABLE = ("alquimia", "medicina", "cocina")
NEW = REFINE + CONSUMABLE
TIERS = [1] + list(range(5, 101, 5))
OLD_REFINED = ("tablon", "lingote", "extracto", "tela_tejida", "cuero_curtido", "sillar")


def body(view):
    return "\n".join(view.body)


def ids(view):
    return [a.id for a in view.actions]


def crafter(service, pid, rank, books=(), bag=None, account="test:1", energy=60):
    """A hero (in the Claro, with every station) that knows `pid` at `rank`, with these books and materials."""
    if service._load(account) is None:
        make_hero(service, account)
    hero = service._load(account)
    if pid not in hero.learned:
        hero.learned.append(pid)
    hero.professions[pid] = xp_for_rank(service.content.balance["professions"]["rank_formula"], rank)
    hero.recipe_books = list(hero.recipe_books or []) + [b for b in books if b not in (hero.recipe_books or [])]
    hero.backpack = dict(bag or {})
    hero.energy = energy
    service._save(hero)
    return hero


def own_recipes(content, pid):
    return {rid: r for rid, r in content.professions["recipes"].items()
            if r["profession"] == pid and not r.get("retired") and not r.get("spec")}


# ---------------------------------------------------------------- content


def test_the_generated_content_is_up_to_date():
    assert recipe_tiers.main(["--check"]) == 0          # run python tools/recipe_tiers.py after changing balance.yaml recipe_tiers


def test_every_one_of_these_professions_has_a_recipe_every_5_ranks_up_to_100_with_a_color(service):
    cfg = service.content.balance["recipe_tiers"]
    assert set(NEW) <= set(cfg["professions"]) and cfg["step"] == 5
    for pid in NEW:
        recipes = own_recipes(service.content, pid)
        assert sorted({r["min_rank"] for r in recipes.values()}) == TIERS, pid
        for rid, rdef in recipes.items():
            assert service._tiered(pid) and service._recipe_color(rdef, rdef["min_rank"]) == "orange", rid
            assert service._recipe_color(rdef, rdef["min_rank"] + 15) == "grey", rid
            if rid.endswith(f"_tramo_{rdef['min_rank']}"):       # generated: energy and xp like a gear piece of its tier
                assert rdef["energy"] == rules.tier_energy(rdef["min_rank"], cfg["energy_by_rank"]), rid
                assert rdef["xp"] == rules.tier_xp(12, rdef["min_rank"], cfg["xp_per_rank"]), rid
    # 120 refined goods (6 × 20 tiers), 19 potions, 18 remedies and 16 dishes
    generated = [rid for rid in service.content.professions["recipes"] if "_tramo_" in rid]
    assert len(generated) == 173
    assert sum(1 for rid in generated if service.content.professions["recipes"][rid]["profession"] in REFINE) == 120


def test_refined_goods_get_better_tier_by_tier_and_never_make_coins(content):
    cfg = content.balance["recipe_tiers"]["refine"]
    ratio = content.balance["shop"]["sell_ratio"]
    recipes = content.professions["recipes"]
    for pid, line in cfg["lines"].items():
        prices, raws = [content.items[line["base"]]["price"]], [0]
        for rank in range(5, 101, 5):
            iid = f"{line['base']}_tramo_{rank}"
            item, rdef = content.items[iid], recipes[iid]
            assert rdef["profession"] == pid and rdef["min_rank"] == rank and rdef["output"] == {iid: 1}
            assert set(rdef["inputs"]) == {line["base"], line["raw"], line["catalyst"]}, iid
            assert item["kind"] == "material" and item["keep"] and item["code"] == line["code"] + rank // 5, iid
            cost = sum(content.items[k]["price"] * n for k, n in rdef["inputs"].items())
            assert item["price"] == cost + rdef["energy"] and item["price"] * ratio < cost, iid     # D-113
            prices.append(item["price"])
            raws.append(rdef["inputs"][line["raw"]])
        assert prices == sorted(set(prices)) and raws == sorted(set(raws)), pid       # strictly better, tier by tier
    assert recipes["tablon_tramo_100"]["inputs"] == {"tablon": 3, "madera": 20, "resina": 5}


def test_potions_remedies_and_dishes_do_more_tier_by_tier(content):
    recipes, items = content.professions["recipes"], content.items
    remedy_ratio = content.balance["shop"]["remedy_sell_ratio"]
    slots = content.balance["hero"]["belt_slots"]
    for pid, key in (("alquimia", "heal"), ("medicina", "heal"), ("cocina", "food")):
        best = {}
        for rid, rdef in own_recipes(content, pid).items():
            out = next(iter(rdef["output"]))
            best[rdef["min_rank"]] = max(best.get(rdef["min_rank"], 0), items[out][key])
            if "_tramo_" not in rid:
                continue
            item = items[out]
            assert len(rules.branches_of(rdef, content.professions["professions"], recipes)) >= 2, rid    # D-109
            if key == "heal":
                anchor = items[item["belt_slot"]]
                assert item["belt"] and item["belt_slot"] in slots, rid               # the belt does not grow
                assert item["toxicity"] == anchor["toxicity"] and item["heal"] > anchor["heal"], rid
                assert item["price"] * remedy_ratio < sum(items[k]["price"] * n for k, n in rdef["inputs"].items()), rid
            else:
                raw = sum(items[k].get("food", 0) * n for k, n in rdef["inputs"].items())
                assert item["cooked"] and item["food"] * rdef["output"][out] > raw > 0 and item["price"] == item["food"], rid
        effects = [best[rank] for rank in TIERS]
        assert effects == sorted(set(effects)), (pid, effects)                         # higher tier, bigger effect
    assert items["pocion_mayor_tramo_100"]["heal"] == 0.75 and items["vendaje_maestro_tramo_100"]["heal"] == 0.6
    assert items["pocion_vida_tramo_20"]["toxicity"] == 40 and items["pocion_mayor_tramo_30"]["toxicity"] == 60
    assert items["festin_tramo_95"]["food"] < items["banquete"]["food"]


def test_old_ids_still_exist_and_keep_working(service):
    content = service.content
    recipes = content.professions["recipes"]
    for iid in OLD_REFINED + ("pocion_vida", "pocion_mayor", "unguento", "botiquin", "vendaje_maestro", "racion_campamento",
                              "pescado_asado", "guiso_cazador", "conserva", "festin", "banquete"):
        assert iid in content.items and not content.items[iid].get("retired"), iid
    assert recipes["tablon"]["inputs"] == {"madera": 3} and recipes["lingote"]["inputs"] == {"pieza_metal": 2}
    assert recipes["sillar"]["inputs"] == {"piedra": 3} and recipes["pocion_vida"]["output"] == {"pocion_vida": 2}
    for rid in ("lingote_carbon", "cuero_corteza", "extracto_raiz", "tela_lino", "sillar_arena", "pociones_mayores",
                "botiquin_miel", "festin_miel"):
        assert rid in service._recipes(), rid
    # the camp's buildings (D-317, D-319) still ask for the old refined goods, and refined_from only knows those
    asked = {k for u in content.camp_upgrades["upgrades"].values() for k in (u.get("cost") or {})}
    assert set(OLD_REFINED) <= asked and not any("_tramo_" in k for k in asked)
    assert all(k in content.items or k == "coins" for k in asked)
    refined = rules.refined_from(content.professions["professions"], recipes)
    assert refined["tablon"] == ("madera", 3) and refined["sillar"] == ("piedra", 3)
    assert not any("_tramo_" in iid for iid in refined)
    codes = [it["code"] for it in content.items.values() if "code" in it]
    assert len(codes) == len(set(codes)) and 99 not in codes                           # stable, unique codes


# ---------------------------------------------------------------- the recipe list, making, the belt


def test_the_recipe_list_shows_the_new_tiers_grouped_with_codes(service):
    crafter(service, "aserradero", 31, books=["aserradero:25"], bag={"tablon": 2, "madera": 7, "resina": 3})
    crafter(service, "canteria", 12, books=[], bag={"tablon": 2, "madera": 7, "resina": 3})
    view = service.act("test:1", "est:refine:0")
    lines = [line for line in view.body if line.startswith("/r")]
    assert view.kind == "station" and "🟧 experiencia entera · 🟨 la mitad · 🟩 un cuarto · ⬜ nada" in view.body
    assert "🪚 Aserradero · rango 31" in view.body
    assert lines[0].startswith("/r1 🟧 ✅ 🟫 Tablón de la vigía · tramo 30 · 🪚+16")     # ✅ first, the highest tier first
    assert lines[1] == "/r2 🟨 ✅ 🟫 Tablón de las cenizas · tramo 25 · 🪚+7"                 # the color falls tier by tier
    assert lines[2] == "/r3 🟩 ✅ 🟫 Tablón del páramo · tramo 20 · 🪚+3"
    assert "/r7 ⬜ ✅ 🟫 Tablón · tramo 1 · 🪚+0" in lines and "🗿 Cantería · rango 12" in view.body
    shown = listed_recipes(service, branch="refine")
    tiers = [service._recipes()[rid]["min_rank"] for rid in shown if service._recipes()[rid]["profession"] == "aserradero"]
    assert shown[0] == "tablon_tramo_30" and set(tiers) == {1, 5, 10, 15, 20, 25, 30} and "tablon_tramo_35" not in shown
    stone = [rid for rid in shown if service._recipes()[rid]["profession"] == "canteria"]
    assert shown.index(stone[0]) > max(shown.index(rid) for rid in shown if rid.startswith("tablon"))   # grouped by profession
    view = service.act("test:1", "est:refine:0")                     # 12 recipes, 8 per page (D-321)
    assert "12 recetas · página 1 de 2" in view.body and "est:refine:1" in ids(view)
    first = service.text("test:1", "/r1")                            # the code opens what the last list showed
    assert first.kind == "recipe" and "Tablón de la vigía" in body(first) and "mk:tablon_tramo_30:1:0" in ids(first)


def test_the_list_hides_tiers_behind_a_missing_book_and_counts_them(service):
    crafter(service, "alquimia", 40, books=[], bag={"extracto": 4, "arcilla": 2, "flor_luna": 1})
    view = service.act("test:1", "est:craft:0")
    assert "📚 Con el libro ⚗️ Alquimia 25 se abren" in body(view)
    shown = listed_recipes(service)
    assert "pocion_vida_tramo_20" in shown and "pocion_mayor_tramo_40" not in shown


def test_making_a_tier_recipe_gives_the_better_good_and_its_experience(service):
    crafter(service, "aserradero", 30, books=["aserradero:25"], bag={"tablon": 4, "madera": 14, "resina": 6})
    view = service.act("test:1", "mk:tablon_tramo_30:2:0")
    hero = service._load("test:1")
    assert "Hiciste" in view.notice and hero.backpack.get("tablon_tramo_30", 0) >= 2
    assert hero.backpack.get("madera", 0) == 2 and hero.backpack.get("resina", 0) == 2
    assert hero.professions["aserradero"] == xp_for_rank(service.content.balance["professions"]["rank_formula"], 30) + 32
    detail = service.text("test:1", f"/{service.content.items['tablon_tramo_30']['code']}")
    assert detail.kind == "resource" and "/106" in detail.title and "refinado del tramo 30" in body(detail)
    sold = service.text("test:1", "/v106")                                           # the merchant buys it, half its price
    assert "tablon_tramo_30" not in service._load("test:1").backpack and sold.kind == "shop_sell"


def test_a_tier_remedy_takes_the_place_of_its_anchor_on_the_belt(service):
    crafter(service, "alquimia", 20, bag={"extracto": 8, "arcilla": 8})
    hero = service._load("test:1")
    hero.belt = {"venda": 1}
    hero.backpack.update({"pocion_vida": 4, "pocion_vida_tramo_10": 2, "pocion_mayor_tramo_60": 3, "pocion_mayor": 1})
    service._refill_belt(hero)
    assert hero.belt["pocion_vida_tramo_10"] == 2 and hero.belt["pocion_vida"] == 1            # the best first, 3 places
    assert hero.belt["pocion_mayor_tramo_60"] == 1 and "pocion_mayor" not in hero.belt        # 1 place for both
    assert hero.backpack["pocion_vida"] == 3 and hero.backpack["pocion_mayor_tramo_60"] == 2
    assert not service._refill_belt(hero)                                                       # full: nothing moves
    service._save(hero)
    service.act("test:1", "mk:pocion_vida_tramo_20:1:0")                                       # a new one waits for a free place
    hero = service._load("test:1")
    assert hero.backpack.get("pocion_vida_tramo_20", 0) >= 2 and "pocion_vida_tramo_20" not in hero.belt
    potions = service.act("test:1", "potions")                                                  # 🧪 Pociones lists them all
    assert potions.kind == "potions" and "Poción de vida del páramo" in body(potions) and "45" in body(potions)


def test_the_guild_fund_can_put_in_what_a_tier_recipe_lacks(service):
    from test_fondo_para_oficios import KEY, camp_with_sawmill, put_fund, wood_reserve
    from test_camp_upgrades import set_hero
    camp = camp_with_sawmill(service)
    hero = service._load("test:2")
    hero.learned.append("aserradero")
    hero.professions["aserradero"] = xp_for_rank(service.content.balance["professions"]["rank_formula"], 5)
    service._save(hero)
    put_fund(service, {"madera": wood_reserve(service, camp) + 10, "resina": 5})
    set_hero(service, "test:2", backpack={"tablon": 1})
    view = service.act("test:2", "rec:tablon_tramo_5:0")
    assert "+💰1" in body(view) and "mk:tablon_tramo_5:1:0" in ids(view)
    service.act("test:2", "mk:tablon_tramo_5:1:0")
    assert service._load("test:2").backpack.get("tablon_tramo_5", 0) >= 1
    assert service._upgrades(KEY)["fund"]["resina"] == 4


# ---------------------------------------------------------------- the books of who already practised (D-64)


def test_old_refiners_get_the_new_books_once_and_new_heroes_none(service):
    make_hero(service)
    formula = service.content.balance["professions"]["rank_formula"]
    data = service.store.get("hero", "test:1")
    data.pop("book_gifts", None)                                            # saved before 0.52 (after the 0.44 gift)
    data["books_checked"] = True
    data["recipe_books"] = ["alquimia:25", "alquimia:50", "herreria:25"]
    data["professions"] = {"aserradero": xp_for_rank(formula, 60), "alquimia": xp_for_rank(formula, 80),
                           "herreria": xp_for_rank(formula, 60), "cocina": xp_for_rank(formula, 30)}
    service.store.put("hero", "test:1", data)
    service.act("test:1", "trainer")
    hero = service._load("test:1")
    assert sorted(hero.recipe_books) == ["alquimia:25", "alquimia:50", "alquimia:75", "aserradero:25", "aserradero:50",
                                         "herreria:25"]               # never the gear books: those are bought since 0.44
    assert hero.book_gifts == ["0.52"]
    hero.professions["aserradero"] = xp_for_rank(formula, 80)
    service._save(hero)
    service.act("test:1", "trainer")
    assert "aserradero:75" not in service._load("test:1").recipe_books    # later ranks are bought, never given again
    make_hero(service, "test:2", "Bram")
    fresh = service._load("test:2")
    assert fresh.book_gifts == ["0.52"] and fresh.recipe_books == []


# ---------------------------------------------------------------- English


def test_the_new_tiers_read_well_in_english(service):
    crafter(service, "medicina", 6, bag={"extracto": 2, "tela_tejida": 2})
    service.store.put("prefs", "test:1", {"lang": "en"})
    view = service.act("test:1", "est:craft:0")
    assert any("Trail Salve ×2 · tier 5 · 🩺+13" in line for line in view.body)
    recipe = service.act("test:1", "rec:unguento_tramo_5:0")
    assert "Orange recipe" in body(recipe) and "24" in body(recipe)
    assert not service.texts.missing


@pytest.mark.parametrize("lang", ["es", "en"])
def test_every_new_item_has_a_name_and_a_use_in_both_languages(content, lang):
    texts = content.locales[lang]
    for iid in content.items:
        if "_tramo_" not in iid:
            continue
        assert texts["item"].get(iid), (lang, iid)
        assert texts["resources"]["use"].get(iid), (lang, iid)
