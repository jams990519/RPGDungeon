"""The 0.29 menus (D-190, D-191; D-192 provisional): bottom menu, 🏕️ Campamento and 👤 Héroe hubs, 🧑‍🏫 Entrenador, ❓ Dudas.

[ES] Pruebas de los menús nuevos: el menú de abajo tiene 5 botones sin 📖 Historia; los centros del Claro, de tu campamento y
del héroe van en orden y con 8 botones como mucho; el entrenador presenta los oficios; ❓ Dudas encuentra respuestas por
palabra y por código, y toda pregunta tiene sus textos; crear un héroe lleva directo al juego, sin origen; el botón viejo
📖 Historia sigue respondiendo.
"""

import re

from conftest import make_hero
from engine.service.game import HUB_BUTTONS, HUB_KINDS
from test_camps import found_at


def ids(view):
    return [a.id for a in view.actions]


def test_bottom_menu_has_five_buttons_without_story(service):
    make_hero(service)
    menu = service.menu()
    assert [m.id for m in menu] == ["home", "explore_menu", "claro", "hero", "options"]
    assert "story" not in [m.id for m in menu] and menu[-1].label == "⚙️ Opciones"
    assert service.commands()["/dudas"] == "dudas" and service.commands()["/historia"] == "story"


def test_creation_goes_straight_to_the_game_without_origin(service):
    view = make_hero(service)
    hero = service._load("test:1")
    assert view.kind == "zone" and "Bienvenido" in view.notice                  # D-190: name and class, then the game
    assert hero.origin is None and not hero.story.get("offered")                # the origin stays for later (E-131)
    assert service.act("test:1", "hero").kind == "hero"                         # the hub, never the origin screen by itself
    assert service.act("test:1", "hero").kind == "hero"


def test_old_story_button_and_command_still_answer(service):
    make_hero(service)
    view = service.act("test:1", "story")
    assert view.kind == "journal" and "📖 Historia" in view.notice and "📔 Diario" in view.notice
    assert ids(view) == ["squests", "factions", "jshow", "hero"]
    assert service.text("test:1", "/historia").kind == "journal"
    old_key = service.text("test:1", "📖 Historia")                             # the key of an old Telegram keyboard
    assert old_key.kind == "journal" and old_key.notice
    assert service.act("test:1", "factions").actions[-1].id == "journal"       # the story's screens go back to the diary
    assert service.act("test:1", "squests").actions[-1].id == "journal"
    assert not service.texts.missing


def test_claro_hub_order_and_button_cap(service):
    make_hero(service)
    view = service.act("test:1", "claro")
    assert view.kind == "claro" and view.kind in HUB_KINDS
    assert ids(view) == ["cook", "research", "oficios", "trainer", "shop", "inn", "board", "dudas"]
    assert len(view.actions) <= HUB_BUTTONS
    text = "\n".join(view.body)
    for mark in ("🍲 Cocinar", "🔬 Investigar", "🛠️ Fabricar", "🧑‍🏫 Entrenador", "🛒 Mercader", "🛏️ Posada", "📜 Tablón", "❓ Dudas"):
        assert mark in text                                                     # one detailed line per option
    assert all("·" not in a.label for a in view.actions)                        # costs go in the text, not on the button


def test_claro_options_lead_somewhere_or_explain(service):
    make_hero(service)
    cook = service.act("test:1", "cook")
    assert cook.kind == "station" and cook.title == "🍲 Cocinar" and ids(cook)[-1] == "claro"
    assert all(a.id.startswith(("rec:", "est:cook:", "claro")) for a in cook.actions)
    recipe = service.act("test:1", cook.actions[0].id)
    assert recipe.kind == "recipe" and recipe.actions[-1].id.startswith("est:cook:")   # a kitchen recipe goes back to 🍲
    research = service.act("test:1", "research")                               # the Claro does not research: it explains
    assert research.kind == "claro" and "Biblioteca" in research.notice
    assert service.act("test:1", "oficios").kind == "professions"
    assert service.act("test:1", "board").actions[-1].id == "claro"


def test_own_camp_hub_and_manage_screen(service):
    make_hero(service)
    found_at(service, "test:1", 6, 0)
    view = service.act("test:1", "claro")
    assert view.kind == "player_camp" and len(view.actions) <= HUB_BUTTONS
    assert ids(view) == ["cook", "research", "oficios", "trainer", "upsvc", "board", "campmgmt", "dudas"]
    assert "Fogón" in service.act("test:1", "cook").notice                      # no 🔥 Fogón yet: it says where
    assert "Biblioteca" in service.act("test:1", "research").notice             # no 📚 Biblioteca yet
    manage = service.act("test:1", "campmgmt")
    assert manage.kind == "camp_manage" and manage.kind in HUB_KINDS
    assert ids(manage) == ["grow", "upgrades", "guild", "claro"]
    for screen in ("grow", "upgrades", "guild"):
        assert service.act("test:1", screen).actions[-1].id == "campmgmt"      # back to 🏰 Gestionar
    assert service.act("test:1", "upsvc").actions[-1].id == "claro"


def test_hero_hub_card_and_buttons(service):
    make_hero(service)
    view = service.act("test:1", "hero")
    assert view.kind == "hero" and view.kind in HUB_KINDS and len(view.actions) <= HUB_BUTTONS
    assert ids(view) == ["bag", "talents", "health", "stats", "bar", "oficios", "journal", "origin"]
    text = "\n".join(view.body)
    assert "❤️ Vida:" in text and "⚡ Energía: 50/50 (llena)" in text and "/oficios" in text
    hero = service._load("test:1")
    hero.energy, hero.hp, hero.points = 30, hero.hp // 2, 2
    service._save(hero)
    text = "\n".join(service.act("test:1", "hero").body)
    assert "(+1 en" in text and "(llena en" in text                            # timers, like TowerWars' card
    assert service.act("test:1", "hero").body[0].startswith("✨")               # pending points first
    origin = service.act("test:1", "origin")
    assert origin.kind == "origin" and len(origin.actions) <= 4                # chosen whenever you want (E-131)
    service.act("test:1", "origpick:noble")
    card = service.act("test:1", "origin")
    assert card.kind == "origin_card" and ids(card) == ["squests", "hero"]     # kept for ever once chosen


def test_trainer_presents_the_professions(service):
    make_hero(service)
    view = service.act("test:1", "trainer")
    assert view.kind == "trainer" and len(view.actions) <= 4
    assert ids(view) == ["oficios", "pspecs", "ench", "claro"]
    text = "\n".join(view.body)
    for word in ("Recolección", "Refinado", "Fabricación", "Explorador", "25", "75", "Construcción"):
        assert word in text
    assert service.text("test:1", "/entrenador").kind == "trainer"
    assert not service.texts.missing


def test_dudas_screen_topics_and_search_by_word(service):
    make_hero(service)
    view = service.act("test:1", "dudas")
    assert view.kind == "dudas" and view.expects_text and len(view.actions) <= HUB_BUTTONS
    assert ids(view)[-1] == "claro" and all(i.startswith("dudas:") for i in ids(view)[:-1])
    topic = service.act("test:1", ids(view)[1])
    assert topic.kind == "dudas_topic" and any(re.match(r"^/d\d\d · ", line) for line in topic.body)
    found = service.text("test:1", "energía")                                  # the screen is open: any text searches
    assert found.kind in ("duda", "dudas_results")
    assert "d07" in service._faq_search("energía") and service._faq_search("ENERGIA")[0] == "d07"
    assert "d35" in service._faq_search("¿cómo fundo un campamento?")
    assert "d46" in service._faq_search("cocinar")
    assert "d15" in service._faq_search("mazmorras")                          # plurals and accents do not matter
    many = service.text("test:1", "/dudas mapa")
    assert many.kind == "dudas_results" and len(many.actions) <= 4 and many.actions[-1].id == "dudas"
    none = service.text("test:1", "/dudas xyzzy")
    assert none.kind == "dudas" and "xyzzy" in none.notice


def test_dudas_answers_by_code(service):
    make_hero(service)
    for typed in ("/d07", "/D7", "d07"):
        service.act("test:1", "dudas")
        view = service.text("test:1", typed)
        assert view.kind == "duda" and "energía" in view.title.lower(), typed
    answer = service.act("test:1", "duda:d35")
    assert answer.kind == "duda" and "/d36" in "\n".join(answer.body) and len(answer.actions) <= 4
    assert "{" not in "\n".join(answer.body)
    unknown = service.text("test:1", "/d99")
    assert unknown.kind == "dudas" and "/d99" in unknown.notice
    service.act("test:1", "home")                                              # leaving ❓ Dudas: text is not a search any more
    assert service.text("test:1", "energía").kind == "zone"


def test_every_faq_entry_has_texts_topic_and_valid_related(service):
    make_hero(service)
    faq = service.content.faq
    entries = service._faq_entries()
    assert 40 <= len(entries) <= 60
    topics = faq["topics"]
    assert set(topics) == {q["topic"] for q in entries.values()} and len(topics) + 1 <= HUB_BUTTONS
    values = service._faq_values()
    for code, entry in entries.items():
        assert re.match(r"^d\d{2,3}$", code)
        assert entry["keywords"] and entry["topic"] in topics
        assert all(c in entries and c != code for c in entry.get("related", [])), code
        question = service.texts.t(f"faq.{code}.q")
        answer = service.texts.t(f"faq.{code}.a", **values)
        assert len(question) <= 40, code                                        # short: it is also a button
        assert "{" not in answer and "[" not in answer, code                   # every number filled from balance.yaml
        view = service.act("test:1", f"duda:{code}")
        assert view.kind == "duda" and len(view.actions) <= 4
    assert all(code in entries for code in faq["popular"])
    for topic in topics:
        assert service.texts.has(f"dudas.topic.{topic}")
    assert not service.texts.missing


def test_dudas_does_not_steal_the_camp_name(service):
    make_hero(service)
    found_at(service, "test:1", 6, 0)
    assert service.store.get("camp", "6:0")["name"] == "Campo 1 6"            # naming still wins over any search
    service.act("test:1", "dudas")
    service.act("test:1", "claro")
    assert service.text("test:1", "hola").notice and service.store.get("dudas_open", "test:1") is None
