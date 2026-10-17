"""Professions are learned once by paying their first recipe; gathering and exploration rise on their own (D-257, 0.33).

[ES] Pruebas de aprender oficios (pedido del dueño, 17-oct-2026). La 🪓 recolección (menos el 🔪 Desollador) y la 🧭
exploración no se aprenden: suben solas. Los demás se aprenden una vez pagando su primera receta (balance.yaml
professions.learn_price) en 🔬 Investigar del Claro o en 🧑‍🏫 Entrenador → 📚 Aprender oficios; sin aprenderlos su rango es 0:
no se cocina, no se refina ni se fabrica con ellos, no se encanta y no suben. Lo que ya practicabas antes de la 0.33 se
aprende gratis y conserva su rango. 📋 Mis oficios trae una línea corta por oficio con su código (/minero); lo largo sale
tocando el código. 🛠️ Fabricar ya no lista los oficios "sin empezar". Todo en los dos idiomas.
Archivo: tests/test_aprender_oficios.py · Módulo: M14 Oficios · Prueba: engine/service/game.py (_knows, _prof_rank,
_prof_gain, _learn, _learn_view, _my_profs_view, _prof_detail_view, _professions_view, _trainer_view, _research,
_station_view, _recipe_view), content/professions.yaml (learn: auto), balance.yaml professions.learn_price.
"""

from conftest import make_hero


def body(view):
    return "\n".join(view.body)


def ids(view):
    return [a.id for a in view.actions]


def rich(service, account="test:1", gold=500):
    hero = service._load(account)
    hero.gold = gold
    service._save(hero)
    return hero


def test_gathering_and_exploring_are_never_learned(service):
    make_hero(service)
    hero = service._load("test:1")
    for pid in ("minero", "herbolario", "lenador", "pescador", "explorador"):
        assert service._knows(hero, pid), pid
    for pid in ("desollador", "cocina", "herreria", "comercio", "encantamiento", "construccion"):
        assert not service._knows(hero, pid), pid
        assert service._prof_rank(hero, pid) == 0
    assert service._prof_rank(hero, "minero") == 1


def test_a_profession_not_learned_never_rises(service):
    make_hero(service)
    hero = service._load("test:1")
    assert service._prof_gain(hero, "desollador", 50) == [] and not hero.professions.get("desollador")
    service._prof_gain(hero, "minero", 50)
    assert hero.professions["minero"] == 50


def test_research_in_the_claro_lists_what_you_can_learn_with_its_price(service):
    make_hero(service)
    view = service.act("test:1", "research")
    assert view.kind == "learn"
    price = service._money(service.content.balance["professions"]["learn_price"])
    assert f"🍲 Cocina · {price}  /cocina" in body(view)
    assert "Minero" not in body(view) and "Explorador" not in body(view)        # they rise on their own
    assert "Cocinar: primero aprende" in body(service.act("test:1", "claro"))


def test_learning_costs_its_first_recipe_and_opens_rank_one(service):
    make_hero(service)
    view = service.text("test:1", "/cocina")
    assert view.kind == "profession" and "Primera receta" in body(view) and ids(view)[0] == "learn:cocina"
    poor = service.act("test:1", "learn:cocina")                                  # a new hero has 10 🥉
    assert "No te alcanza" in poor.notice and "cocina" not in service._load("test:1").learned
    rich(service, gold=100)
    view = service.act("test:1", "learn:cocina")
    hero = service._load("test:1")
    assert "cocina" in hero.learned and hero.gold == 100 - service.content.balance["professions"]["learn_price"]
    assert "Aprendiste" in view.notice and service._prof_rank(hero, "cocina") == 1
    assert "cook" in ids(view)
    station = service.act("test:1", "cook")
    assert station.kind == "station" and any(a.id.startswith("rec:") for a in station.actions)
    assert service.act("test:1", "learn:cocina").notice                        # already known: nothing charged
    assert service._load("test:1").gold == hero.gold


def test_without_the_profession_you_cannot_cook_refine_craft_or_enchant(service):
    make_hero(service)
    rich(service)
    view = service.act("test:1", "cook")
    assert view.kind == "profession" and "primero aprende" in view.notice
    refine = service.act("test:1", "est:refine:0")
    assert "Todavía no sabes ningún oficio de refinar" in body(refine) and "learnlist" in ids(refine)
    rid = next(r for r, rdef in service._recipes().items() if rdef["profession"] == "aserradero")
    hero = service._load("test:1")
    hero.backpack.update({i: 20 for i in service._recipes()[rid]["inputs"]})
    service._save(hero)
    assert "primero aprende" in body(service.act("test:1", f"rec:{rid}:0"))
    service.act("test:1", f"mk:{rid}:1:0")
    assert not service._load("test:1").professions.get("aserradero")           # nothing made
    assert service.act("test:1", "ench").kind == "profession"
    service.act("test:1", "learn:aserradero")
    made = service.act("test:1", f"mk:{rid}:1:0")
    assert service._load("test:1").professions.get("aserradero", 0) > 0, made.notice


def test_old_practice_is_learned_free_and_keeps_its_rank(service):
    make_hero(service)
    hero = service._load("test:1")
    hero.professions["desollador"] = 300                                         # practised before 0.33
    service._save(hero)
    assert service._prof_rank(service._load("test:1"), "desollador") == 0
    assert "gratis" in body(service.act("test:1", "learnlist"))
    service.act("test:1", "learn:desollador")
    hero = service._load("test:1")
    assert hero.gold == 10 and "desollador" in hero.learned and service._prof_rank(hero, "desollador") > 1


def test_my_professions_is_short_with_codes_and_the_detail_is_behind_them(service):
    make_hero(service)
    hero = service._load("test:1")
    hero.professions.update({"minero": 120, "explorador": 200, "desollador": 30})
    service._save(hero)
    view = service.act("test:1", "myprof")
    text = body(view)
    assert "⛏️ Minero · rango" in text and text.count("/minero") == 1 and "/explorador" in text
    assert "Desollador" not in text                                               # not learned: not yours
    assert "Beneficio" not in text and "Sin empezar" not in text
    detail = service.text("test:1", "/minero")
    assert detail.kind == "profession" and "Beneficio ahora" in body(detail)
    make = service.act("test:1", "oficios")
    assert "Sin empezar" not in body(make) and "/minero" in body(make)


def test_the_trainer_lists_yours_and_those_left_with_learn_buttons(service):
    make_hero(service)
    view = service.act("test:1", "trainer")
    assert ids(view) == ["myprof", "learnlist", "pspecs", "claro"]
    text = body(view)
    assert "Te faltan por aprender" in text and "pagando su primera receta" in text
    assert "ench" not in ids(view)


def test_construction_is_learned_only_in_a_camp(service):
    make_hero(service)
    rich(service)
    view = service.act("test:1", "learn:construccion")
    assert "campamento" in view.notice and "construccion" not in service._load("test:1").learned


def test_learning_reads_well_in_english(service):
    from test_idiomas import english_hero
    english_hero(service)
    rich(service)
    view = service.act("test:1", "research")
    assert view.title == "📚 Learn professions"
    view = service.act("test:1", "learn:cocina")
    assert "You learned" in view.notice
    assert not service.texts.fallbacks.get("en")
