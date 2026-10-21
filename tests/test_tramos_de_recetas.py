"""The recipe reform of 0.44 (D-306: E-221, E-222, E-223): tiers every 5 ranks, WoW recipe colors, recipe books.

[ES] Pruebas de la reforma de recetas (decidida por el dueño el 20-oct-2026). En los oficios de equipo (🪑 🔨 🪡 🦺 💍) hay un
tramo de recetas cada 5 rangos, con la pieza del nivel del tramo; la energía y la experiencia de las piezas crecen con el tramo.
Los colores como en WoW: 🟧 naranja da la experiencia de oficio entera, 🟨 amarilla la mitad, 🟩 verde un cuarto y ⬜ gris nada,
según cuánto te queda chica la receta; se ven en 🛠️ Fabricar con su leyenda y la experiencia que da cada receta. Los 📚 libros
de recetas del 🧑‍🏫 Entrenador (🥈2 al 25, 🥈10 al 50, 🥈25 al 75) abren las recetas de esos rangos; quien ya practicaba recibe
gratis los de los rangos que tenía (D-64). La primera receta de 💍 Joyería no pide gema y las 67 recetas de malla quedan
retiradas sin quitarle a nadie sus piezas. Todo también en inglés. El contenido lo arma tools/recipe_tiers.py: la prueba avisa
si quedó viejo.
Archivo: tests/test_tramos_de_recetas.py · Módulo: M14 Oficios · Prueba: engine/professions/rules.py (tier_rank, tier_energy,
tier_xp, recipe_color, color_factor, books_for, book_price, book_id), engine/service/game.py (sección "recipe tiers, colors and
books", _station_view, _recipe_view, _make, _prof_gain, _trainer_view, _load), tools/recipe_tiers.py, content/professions.yaml,
content/items.yaml, balance.yaml recipe_tiers.
"""

import sys
from pathlib import Path

from conftest import make_hero
from engine.service.game import button_cap
from engine.professions import rules
from engine.professions import xp_for_rank

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import recipe_tiers  # noqa: E402

GEAR = ("carpinteria", "herreria", "sastreria", "peleteria", "joyeria")


def body(view):
    return "\n".join(view.body)


def ids(view):
    return [a.id for a in view.actions]


def crafter(service, pid="herreria", rank=1, gold=0, books=(), bag=None, account="test:1"):
    """A new hero (it buys its own books) that knows `pid` at `rank`, in the Claro, with these coins, books and materials."""
    if service._load(account) is None:
        make_hero(service, account)
    hero = service._load(account)
    if pid not in hero.learned:
        hero.learned.append(pid)
    hero.professions[pid] = xp_for_rank(service.content.balance["professions"]["rank_formula"], rank)
    hero.gold = gold
    hero.recipe_books = list(books)
    hero.backpack.update(bag or {})
    hero.energy = 50
    service._save(hero)
    return hero


def gear_line(content, pid):
    """(slot, type) -> {recipe rank: piece level} of the non-exclusive gear recipes of a profession."""
    lines = {}
    for rdef in content.professions["recipes"].values():
        item = content.items.get(next(iter(rdef["output"])), {})
        if rdef["profession"] != pid or rdef.get("retired") or rdef.get("spec") or item.get("kind") != "gear":
            continue
        lines.setdefault((item["slot"], item["type"]), {}).setdefault(rdef["min_rank"], []).append(item["req_level"])
    return lines


# ---------------------------------------------------------------- content


def test_the_generated_content_is_up_to_date():
    assert recipe_tiers.main(["--check"]) == 0          # run python tools/recipe_tiers.py after changing balance or gear


def test_a_tier_every_5_ranks_in_the_gear_professions_with_piece_level_equal_to_rank(content):
    cfg = content.balance["recipe_tiers"]
    assert cfg["professions"] == list(GEAR) and cfg["step"] == 5
    tiers = [1] + list(range(5, 101, 5))
    for pid in GEAR:
        for line, by_rank in gear_line(content, pid).items():
            assert sorted(by_rank) == tiers, (pid, line)
            for rank, levels in by_rank.items():
                assert all(rules.tier_rank(level, 5) == rank and level <= max(rank, 3) for level in levels), (pid, line, rank)
    assert rules.tier_rank(3, 5) == 1 and rules.tier_rank(5, 5) == 5 and rules.tier_rank(8, 5) == 10
    assert rules.tier_rank(15, 5) == 15 and rules.tier_rank(100, 5) == 100


def test_energy_and_experience_grow_with_the_tier(content):
    cfg = content.balance["recipe_tiers"]
    recipes = content.professions["recipes"]
    for rid, rdef in recipes.items():
        if rdef["profession"] not in GEAR or rdef.get("retired"):
            continue
        rank = rdef["min_rank"]
        if content.items[next(iter(rdef["output"]))].get("kind") == "gear":
            assert rdef["energy"] == rules.tier_energy(rank, cfg["energy_by_rank"]), rid
            assert rdef["xp"] == rules.tier_xp(12, rank, cfg["xp_per_rank"]), rid
        else:                                                # bandages and 🪑 furniture keep their energy
            assert rdef["xp"] == rules.tier_xp(6 * rdef["energy"], rank, cfg["xp_per_rank"]), rid
    assert [recipes[r]["energy"] for r in ("espada_forjada", "espada_nivel_50", "espada_nivel_55", "espada_nivel_100")] == [2, 2, 3, 4]
    assert [recipes[r]["xp"] for r in ("espada_forjada", "espada_nivel_50", "espada_nivel_100")] == [12, 18, 24]
    assert recipes["pocion_vida"]["xp"] == 6 and recipes["tablon"]["xp"] == 6          # untiered professions: as before


def test_new_pieces_beat_nothing_less_and_never_make_coins(content):
    ratio = content.balance["shop"]["sell_ratio"]
    recipes = content.professions["recipes"]
    profs = content.professions["professions"]
    generated = {rid: r for rid, r in recipes.items() if next(iter(r["output"])).rsplit("_", 2)[-2:-1] == ["nivel"]}
    assert len(generated) == 180                           # 20 gear lines × the 9 new levels (15, 25 … 95)
    for rid, rdef in generated.items():
        out = next(iter(rdef["output"]))
        item = content.items[out]
        assert item["source"] == "crafted" and item["rarity"] == "epico" and item["req_level"] == rdef["min_rank"], rid
        assert item["price"] * ratio < sum(content.items[m]["price"] * n for m, n in rdef["inputs"].items()), rid
        assert len(rules.branches_of(rdef, profs, recipes)) >= 2, rid
        assert content.items[rules.masterwork_id(out)]["masterwork"], rid               # D-116: its ✒️ twin
    assert "artesano_espada_nivel_15" in content.items and recipes["espada_nivel_15"]["min_rank"] == 15


# ---------------------------------------------------------------- colors


def test_recipe_colors_like_wow(content):
    colors = content.balance["recipe_tiers"]["colors"]
    seen = {gap: rules.recipe_color(20 + gap, 20, colors) for gap in (-3, 0, 4, 5, 9, 10, 14, 15, 60)}
    assert seen == {-3: "orange", 0: "orange", 4: "orange", 5: "yellow", 9: "yellow", 10: "green", 14: "green",
                    15: "grey", 60: "grey"}
    assert [rules.color_factor(c, colors) for c in ("orange", "yellow", "green", "grey")] == [1.0, 0.5, 0.25, 0.0]


def test_colors_decide_the_profession_experience(service):
    hero = crafter(service, "herreria", rank=27, books=["herreria:25"],
                   bag={"lingote": 200, "cuero_curtido": 100, "gema_bruta": 20})
    recipes = service._recipes()
    assert service._recipe_xp(recipes["espada_nivel_25"], 27) == 15                  # 🟧 full
    assert service._recipe_xp(recipes["espada_nivel_20"], 27) == 14 // 2             # 🟨 half
    assert service._recipe_xp(recipes["espada_nivel_15"], 27) == 14 // 4             # 🟩 a quarter
    assert service._recipe_xp(recipes["espada_forjada"], 27) == 0                    # ⬜ none
    before = hero.professions["herreria"]
    view = service.act("test:1", "mk:espada_forjada:1:0")                            # a grey recipe still makes the piece
    after = service._load("test:1")
    assert after.backpack.get("artesano_espada_1", 0) + after.backpack.get("artesano_espada_1_obra", 0) >= 1
    assert after.professions["herreria"] == before and "Herrería +0" in view.notice
    service.act("test:1", "mk:espada_nivel_25:1:0")
    assert service._load("test:1").professions["herreria"] == before + 15


def test_a_batch_changes_color_when_the_rank_rises(service):
    hero = crafter(service, "herreria", rank=1, bag={"lingote": 200, "cuero_curtido": 100})
    rdef = service._recipes()["daga_forjada"]
    total = service._batch_prof_xp(hero, rdef, 40)
    assert total < 40 * rdef["xp"]                         # the last makes are 🟨 or worse: rank 6 and up
    service.act("test:1", "mk:daga_forjada:20:0")
    assert service._load("test:1").professions["herreria"] == service._batch_prof_xp(hero, rdef, 20)


def test_untiered_professions_still_give_their_whole_experience(service):
    hero = crafter(service, "alquimia", rank=80, books=["alquimia:25", "alquimia:50"], bag={"extracto": 5, "arcilla": 5})
    rdef = service._recipes()["pocion_vida"]
    assert service._recipe_color(rdef, 80) is None and service._recipe_xp(rdef, 80) == rdef["xp"] == 6
    view = service.act("test:1", "est:craft:0")
    assert "🟧" not in body(view) and "⚗️+6" in body(view)          # no color, but the experience it gives


def test_the_station_shows_colors_their_legend_and_the_experience(service):
    crafter(service, "herreria", rank=12, bag={"lingote": 30, "cuero_curtido": 10, "gema_bruta": 2})
    view = service.act("test:1", "est:craft:0")
    text = body(view)
    assert "🟧 experiencia entera · 🟨 la mitad · 🟩 un cuarto · ⬜ nada" in text
    assert "🟧 🟣🗡️ Hoja de la frontera" in text and "🔨+13" in text
    assert any(a.label.startswith("✅ 🟧") for a in view.actions)
    recipe = service.act("test:1", "rec:espada_forjada:0")
    assert "🟩 Receta verde" in body(recipe) and "Herrería +3" in body(recipe)


# ---------------------------------------------------------------- books


def test_book_prices_and_ranks(content):
    books = content.balance["recipe_tiers"]["books"]
    assert [(b["rank"], b["price"]) for b in books] == [(25, 200), (50, 1000), (75, 2500)]   # 🥈2, 🥈10, 🥈25
    assert rules.books_for(24, books) == [] and rules.books_for(25, books) == [25]
    assert rules.books_for(100, books) == [25, 50, 75] and rules.book_id("herreria", 25) == "herreria:25"


def test_recipes_of_rank_25_need_their_book_and_buying_it_opens_them(service):
    crafter(service, "herreria", rank=27, gold=150, bag={"lingote": 40, "cuero_curtido": 20, "gema_bruta": 5})
    station = service.act("test:1", "est:craft:0")
    assert "rec:espada_nivel_25:0" not in ids(station)
    assert "📚 Con el libro 🔨 Herrería 25 se abren 7 recetas más aquí" in body(station)
    recipe = service.act("test:1", "rec:espada_nivel_25:0")
    assert "📕 Pide el libro de recetas 🔨 Herrería 25" in body(recipe) and "pbooks" in ids(recipe)
    assert not any(a.id.startswith("mk:") for a in recipe.actions)
    before = service.store.get("hero", "test:1")
    refused = service.act("test:1", "mk:espada_nivel_25:1:0")
    after = service.store.get("hero", "test:1")
    assert "📕" in refused.notice and after["backpack"] == before["backpack"] and after["energy"] == before["energy"]
    books = service.act("test:1", "pbooks")
    assert books.kind == "recipe_books" and "📕 🔨 Herrería 25 · 🥈2 · abre 7 recetas" in body(books)
    poor = service.act("test:1", "pbook:herreria:25")
    assert "No te alcanza" in poor.notice and service._load("test:1").recipe_books == []
    hero = service._load("test:1")
    hero.gold = 250
    service._save(hero)
    bought = service.act("test:1", "pbook:herreria:25")
    assert "Compraste el libro 🔨 Herrería 25: ya puedes hacer 7 recetas nuevas" in bought.notice
    hero = service._load("test:1")
    assert hero.recipe_books == ["herreria:25"] and hero.gold == 50
    assert "Ya tienes" in service.act("test:1", "pbook:herreria:25").notice and service._load("test:1").gold == 50
    assert "rec:espada_nivel_25:0" in ids(service.act("test:1", "est:craft:0"))
    made = service.act("test:1", "mk:espada_nivel_25:1:0")
    assert "Hiciste" in made.notice


def test_books_above_your_rank_are_not_sold(service):
    crafter(service, "herreria", rank=60, gold=10000, books=["herreria:25"])
    view = service.act("test:1", "pbooks")
    assert "pbook:herreria:50" in ids(view) and "pbook:herreria:75" not in ids(view)
    refused = service.act("test:1", "pbook:herreria:75")
    assert "🔒" in refused.notice and service._load("test:1").gold == 10000
    hero = service._load("test:1")
    rdef = service._recipes()["espada_nivel_100"]
    assert service._book_missing(hero, rdef) == [50, 75]           # a rank-100 recipe needs the three books


def test_rank_up_says_the_trainer_sells_the_book(service):
    crafter(service, "herreria", rank=24, bag={"lingote": 60, "cuero_curtido": 30, "gema_bruta": 10})
    hero = service._load("test:1")
    hero.professions["herreria"] = xp_for_rank(service.content.balance["professions"]["rank_formula"], 25) - 1
    service._save(hero)
    view = service.act("test:1", "mk:espada_nivel_20:1:0")
    assert "rango 25" in view.notice and "📚 Rango 25: el 🧑‍🏫 Entrenador ya te vende el libro 🔨 Herrería 25 (🥈2)" in view.notice
    assert "Hoja de las cenizas" not in view.notice                # the new recipes wait for the book


def test_the_trainer_shows_books_only_when_there_is_something(service):
    make_hero(service)
    assert "pbooks" not in ids(service.act("test:1", "trainer"))
    crafter(service, "herreria", rank=26)
    view = service.act("test:1", "trainer")
    assert "pbooks" in ids(view) and len(view.actions) <= button_cap("trainer")    # D-315: 📚 in the 🧑‍🏫 Entrenador (up to 6)
    assert service.act("test:1", "pbooks").actions[-1].id == "trainer"


def test_old_heroes_keep_what_they_could_make(service):
    make_hero(service)
    formula = service.content.balance["professions"]["rank_formula"]
    data = service.store.get("hero", "test:1")
    data.pop("recipe_books", None)
    data.pop("books_checked", None)                                 # saved before 0.44
    data["learned"] = list(data.get("learned", [])) + ["herreria", "alquimia", "cocina"]
    data["professions"] = {"herreria": xp_for_rank(formula, 60), "alquimia": xp_for_rank(formula, 30),
                           "cocina": xp_for_rank(formula, 10), "sastreria": xp_for_rank(formula, 51)}  # sastrería: practised, not learned
    service.store.put("hero", "test:1", data)
    service.act("test:1", "trainer")
    hero = service._load("test:1")
    assert sorted(hero.recipe_books) == ["alquimia:25", "herreria:25", "herreria:50", "sastreria:25", "sastreria:50"]
    assert hero.books_checked
    hero.professions["herreria"] = xp_for_rank(formula, 80)          # later ranks are bought, never given again
    service._save(hero)
    service.act("test:1", "trainer")
    assert "herreria:75" not in service._load("test:1").recipe_books


def test_new_heroes_get_no_free_books(service):
    make_hero(service)
    hero = service._load("test:1")
    assert hero.books_checked and hero.recipe_books == []


# ---------------------------------------------------------------- jewelcrafting and mail


def test_the_first_jewelcrafting_recipe_needs_no_gem(service):
    assert service._first_recipe("joyeria") == "colgante_cobre"
    rdef = service._recipes()["colgante_cobre"]
    assert "gema_bruta" not in rdef["inputs"] and rdef["min_rank"] == 1
    make_hero(service)
    hero = service._load("test:1")
    hero.gold = 1000
    service._save(hero)
    detail = service.act("test:1", "pview:joyeria")
    assert "📿 Colgante de cobre" in body(detail)
    service.act("test:1", "learn:joyeria")
    hero = service._load("test:1")
    hero.backpack.update({"lingote": 2, "cuero_curtido": 2})
    hero.energy = 50
    service._save(hero)
    made = service.act("test:1", "mk:colgante_cobre:1:0")
    hero = service._load("test:1")
    assert "Hiciste" in made.notice
    assert hero.backpack.get("colgante_cobre", 0) + hero.backpack.get("colgante_cobre_obra", 0) + \
        int(hero.gear.get("joya", "").startswith("colgante_cobre")) == 1


def test_mail_recipes_are_retired_and_the_pieces_stay(service):
    raw = service.content.professions["recipes"]
    mail = [rid for rid, r in raw.items() if service.content.items[next(iter(r["output"]))].get("type") == "malla"]
    assert len(mail) == 67 and all(raw[rid].get("retired") for rid in mail)
    assert not any(rid in service._recipes() for rid in mail)
    assert "artesano_malla_3" in service.content.items and "artesano_malla_3_obra" in service.content.items
    hero = crafter(service, "peleteria", rank=60, books=["peleteria:25", "peleteria:50"],
                   bag={"artesano_malla_3": 1, "cuero_curtido": 20, "lingote": 20})
    assert "artesano_malla_3" in hero.backpack
    station = service.act("test:1", "est:craft:0")                   # the stations list only service._recipes()
    assert "malla" not in " ".join(ids(station)) and "cota_" not in " ".join(ids(station))
    before = service.store.get("hero", "test:1")
    view = service.act("test:1", "mk:cota_ligera:1:0")               # an old button: nothing happens, nothing is spent
    after = service.store.get("hero", "test:1")
    assert view.kind == "professions" and after["backpack"] == before["backpack"]
    assert service._load("test:1").backpack["artesano_malla_3"] == 1


# ---------------------------------------------------------------- English


def test_recipe_screens_read_well_in_english(service):
    crafter(service, "herreria", rank=27, gold=300, bag={"lingote": 40, "cuero_curtido": 20, "gema_bruta": 5})
    service.store.put("prefs", "test:1", {"lang": "en"})
    station = service.act("test:1", "est:craft:0")
    assert "🟧 full experience · 🟨 half · 🟩 a quarter · ⬜ none" in body(station)
    assert "📚 With the book 🔨 Blacksmithing 25, 7 more recipes open here" in body(station)
    books = service.act("test:1", "pbooks")
    assert books.title == "📚 Recipe books" and "📕 🔨 Blacksmithing 25 · 🥈2 · opens 7 recipes" in body(books)
    bought = service.act("test:1", "pbook:herreria:25")
    assert "You bought the book 🔨 Blacksmithing 25: you can now make 7 new recipes" in bought.notice
    recipe = service.act("test:1", "rec:espada_nivel_25:0")
    assert "🟧 Orange recipe" in body(recipe) and "Ashen Blade" in body(recipe)
    trainer = service.act("test:1", "trainer")
    assert any(a.label == "📚 Recipe books" for a in trainer.actions)
    assert not service.texts.fallbacks and not service.texts.missing
