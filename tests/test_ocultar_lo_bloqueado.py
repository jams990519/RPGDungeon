"""What is not for your level yet is not shown, in the whole game, with no "next unlock" line (D-287, 0.39).

[ES] Pruebas del pedido del dueño (19-oct-2026): "si hay algo que no está para tu nivel, no lo vas a mostrar", en todo el
juego y sin una línea de "lo próximo que se abre". Fuera del campamento y del gremio (que tienen su propio cambio): las
estaciones no anuncian recetas de rango más alto ni la pantalla de un oficio dice qué abre el próximo rango; el 🧑‍🏫 Entrenador
no tiene "🔒 Más adelante" ni el botón 🎓 antes del rango 25; 🎓 Especialización no lista los oficios que no llegan; los talentos
no muestran habilidades cerradas ni el segundo rol antes del nivel 5, ni el 🔀 modo híbrido (su línea en 🌟 Talentos y su botón
en 🎛️ Barra de combate) antes del nivel 10 (0.54, D-330); el campamento enemigo no tiene el botón 🔒 de
🕵️ Infiltrarse; las misiones de nivel más alto no salen y se avisan al llegar a su nivel. Lo que se pide a mano (un botón
viejo o un código) recibe un aviso corto. Todo en los dos idiomas.
Archivo: tests/test_ocultar_lo_bloqueado.py · Módulo: capa de servicios (M14 Oficios, M2 Héroe, M10 Misiones, mapa) · Prueba:
engine/service/game.py (_trainer_view, _prof_detail_view, _explorer_prof_lines, _station_view, _recipe_view, _ench_view,
_pspecs_view, _pspec_prof_view, _pspec_view, _chain_talents_view, _chain_spec_view, _bar_view, _spec_view, _ecamp_menu,
_places_view, _recon_view, _level_point_lines) y engine/service/story.py (_story_summary_lines, _quests_view, _quest_block,
_quest_complete, _story_level_lines).
"""

import pytest

from conftest import legacy_content, make_hero
from engine.classes import specs_of
from engine.hero import xp_for_level
from engine.service import GameService
from engine.core import FixedClock, MemoryStore
from test_enemy_camps import at_camp
from test_professions import rank_xp


def ids(view):
    return [a.id for a in view.actions]


def body(view):
    return "\n".join(view.body)


def set_profs(service, account="test:1", learned=(), **ranks):
    """Give the hero these profession ranks (and mark them learned)."""
    hero = service._load(account)
    hero.professions.update({pid: rank_xp(service, rank) for pid, rank in ranks.items()})
    hero.learned = list(dict.fromkeys(list(hero.learned) + list(learned or ranks)))
    hero.tutorial = len(service.content.balance["tutorial"]["steps"])
    service._save(hero)
    return hero


# ---------------------------------------------------------------- professions


def test_a_station_and_a_profession_hide_higher_ranks_and_the_next_unlock(service, every_profession_known):
    make_hero(service)
    hero = set_profs(service, learned=["herreria"], herreria=1)
    recipes = service._recipes()
    for branch in ("craft", "refine"):
        for page in range(3):
            view = service.act("test:1", f"est:{branch}:{page}")
            assert view.kind == "station", branch
            assert "🔒" not in body(view) and "Más recetas" not in body(view)
            for code in (service.store.get("gremio_codes", "test:1") or {}).get("recipes", []):     # D-321: the /rN list
                rid = code.split("|")[0]
                assert service._prof_rank(hero, recipes[rid]["profession"]) >= int(recipes[rid].get("min_rank", 1)), rid
    detail = service.text("test:1", "/herreria")
    assert detail.kind == "profession" and "🔓" not in body(detail) and "En rango" not in body(detail)
    old = service.act("test:1", "rec:espada_templada:0")              # rank 5 (25 until 0.44), from an old button: back to the station
    assert old.kind == "station" and old.notice.startswith("🔒") and "Espada templada" not in body(old)
    assert service._load("test:1").backpack == hero.backpack            # nothing made, nothing spent


def test_the_explorer_shows_only_the_thresholds_it_reached(service):
    make_hero(service)
    novice = service.text("test:1", "/explorador")
    assert "🗺️" not in body(novice) and "🔓" not in body(novice)
    set_profs(service, explorador=30)
    view = body(service.text("test:1", "/explorador"))
    assert "✅10" in view and "✅30" in view and "todo el mapa" not in view and "🔓" not in view


def test_enchantments_above_your_rank_are_not_listed(service, every_profession_known):
    make_hero(service)
    set_profs(service, encantamiento=1)
    view = service.act("test:1", "ench")
    assert view.kind == "enchanting" and "🔒" not in body(view)
    assert "Filo" in body(view) and "Guarda" not in body(view)          # 🛡️ Guarda opens at rank 25
    set_profs(service, encantamiento=25)
    assert "Guarda" in body(service.act("test:1", "ench"))


# ---------------------------------------------------------------- 🧑‍🏫 trainer and 🎓 specializations


def test_the_trainer_hides_what_comes_later(service):
    make_hero(service)
    view = service.act("test:1", "trainer")
    assert ids(view) == ["myprof", "learnlist", "claro"]               # no 🎓 before rank 25
    text = body(view)
    assert "🔒" not in text and "Más adelante" not in text and "25" not in text and "75" not in text
    set_profs(service, herreria=25)                                     # D-306 (0.44): rank 25 also opens 📚 its recipe book
    assert ids(service.act("test:1", "trainer")) == ["myprof", "learnlist", "pspecs", "pbooks", "claro"]


def test_specializations_show_only_what_your_ranks_open(service):
    make_hero(service)
    empty = service.act("test:1", "pspecs")                             # typed /especialidad before any rank 25
    assert empty.kind == "specs" and empty.body == [service.texts.t("spec.none_yet")] and ids(empty) == ["oficios"]
    set_profs(service, herreria=25, minero=3)
    view = service.act("test:1", "pspecs")
    assert "Herrería" in body(view) and "🔒" not in body(view) and "Minero" not in body(view)
    prof = service.act("test:1", "pspec:herreria")
    assert prof.kind == "prof_specs" and "🔓" not in body(prof) and "En rango" not in body(prof)
    one, top = service._recipe_name("espec_espada_1"), service._recipe_name("espec_espada_2")    # ranks 25 and 100
    assert one in body(prof) and top not in body(prof)
    spec = service.act("test:1", "pspv:herreria_armas")
    assert spec.kind == "spec" and one in body(spec) and top not in body(spec)
    old = service.act("test:1", "pspec:minero")                         # an old button: a short reply, nothing chosen
    assert old.kind == "specs" and "🔒" in old.notice and not service._load("test:1").prof_specs.get("minero")


# ---------------------------------------------------------------- 🌟 talents


def test_the_second_role_and_the_hybrid_mode_wait_for_their_level(service):
    make_hero(service)
    hero = service._load("test:1")
    other = next(spec for spec in specs_of(service.content.classes, service.content.classes[hero.class_id]["group"])
                 if spec != hero.class_id)
    view = service.act("test:1", "talents")
    # 0.54 (D-330): the hybrid mode's line is 🔀 (it was 🧪 "coming soon"); its button lives in 🎛️ Barra de combate
    assert "🔒" not in body(view) and f"tal:{other}" not in ids(view) and "🔀" not in body(view)
    bar = service.act("test:1", "bar")
    assert "🔀" not in body(bar) and "nivel 10" not in body(bar) and "hyb" not in ids(bar)
    old = service.act("test:1", f"tal:{other}")                          # an old button: back with a short reply
    assert old.kind == "talents" and "nivel 5" in old.notice
    hero = service._load("test:1")
    hero.level = 10
    service._save(hero)
    view = service.act("test:1", "talents")
    assert f"tal:{other}" in ids(view) and "🔀" in body(view)
    assert "hyb" in ids(service.act("test:1", "bar"))


@pytest.fixture
def legacy_service():
    return GameService(legacy_content(), MemoryStore(), FixedClock(), world_seed=12345, time_scale=1.0)


def test_class_abilities_you_do_not_have_are_not_listed(legacy_service):
    service = legacy_service
    make_hero(service, class_id="guerrero")
    data = service.store.get("hero", "test:1")
    data.update({"level": 6, "points": 5})
    service.store.put("hero", "test:1", data)
    for _ in range(5):
        view = service.act("test:1", "pt:guerrero_furia")
    hero = service._load("test:1")
    lines = [line for line in view.body if line.startswith(("🔓", "🔒"))]
    names = [service.texts.t(f"ability.{a['id']}.name") for a in service.content.classes["guerrero_furia"]["abilities"]]
    assert lines and all(line.startswith("🔓") for line in lines)
    assert len(lines) == sum(1 for a in service.content.classes["guerrero_furia"]["abilities"] if a["id"] in hero.unlocked)
    assert not any(line.startswith("Siguiente") for line in view.body) and len(lines) < len(names)


# ---------------------------------------------------------------- 🧭 exploring


def test_the_enemy_camp_menu_hides_the_locked_infiltrate_button(service):
    at_camp(service)
    menu = service.act("test:1", "explore_menu")
    assert ids(menu) == ["assault", "hunt", "map"] and "rango 30" not in body(menu)
    typed = service.act("test:1", "infiltrate")                          # an old button: a short reply, nothing spent
    assert "rango 30" in typed.notice and service._load("test:1").energy == 50


def test_places_and_recon_say_nothing_about_ranks_to_come(service):
    make_hero(service)
    assert "rango" not in body(service.act("test:1", "places")).lower()
    set_profs(service, explorador=10)
    recon = service.act("test:1", "recon")
    assert recon.kind == "recon" and "🔓" not in body(recon) and "rango 30" not in body(recon)


# ---------------------------------------------------------------- 📔 story


def test_missions_above_your_level_are_hidden_and_announced_when_reached(service):
    make_hero(service)
    hero = service._load("test:1")
    service._st(hero)["done"] += ["c1_m1", "c1_m2"]                     # c1_m3 starts at level 2
    service._save(hero)
    journal = body(service.act("test:1", "story"))
    quests = body(service.act("test:1", "squests"))
    for text in (journal, quests):
        assert "🔒" not in text and "nivel 2" not in text
    title = service._quest_title("c1_m3")
    assert title not in journal and title not in quests
    hero = service._load("test:1")
    hero.xp = xp_for_level(service.content.balance["hero"]["xp_formula"], 2) - 1
    lines = service._give_xp(hero, 1)
    assert hero.level == 2 and service.texts.t("story.next_quest", title=title) in lines
    service._save(hero)
    assert title in body(service.act("test:1", "squests"))


# ---------------------------------------------------------------- 🇬🇧 English


def test_the_hidden_screens_read_well_in_english(service):
    from test_idiomas import english_hero
    english_hero(service)
    set_profs(service, herreria=25, explorador=10)
    for action in ("trainer", "pspecs", "pspec:herreria", "pspv:herreria_armas", "talents", "bar", "places", "recon",
                   "story", "squests", "est:craft:0", "rec:espec_espada_2:0", "explore_menu"):
        view = service.act("test:1", action)
        assert view.body, action
    assert service.text("test:1", "/explorador").body and service.text("test:1", "/herreria").body
    hero = service._load("test:1")
    hero.professions = {}
    service._save(hero)
    assert service.act("test:1", "pspecs").body == ["🎓 You have no specializations yet."]
    assert not service.texts.fallbacks.get("en") and not service.texts.missing
