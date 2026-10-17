"""English and Spanish (D-250): the language is chosen on the first screen and in ⚙️ Options, every text exists in both.

[ES] Pruebas del idioma: el español y el inglés tienen las mismas claves, huecos, plurales y etiquetas (tools/
check_locales.py); la primera pantalla de la creación ofrece 🇪🇸 Español y 🇬🇧 English con la pregunta en los dos idiomas;
elegir inglés deja todo en inglés (creación, menú de abajo, pantallas, combate) sin una sola frase prestada del español;
los que ya jugaban siguen en español y cambian en ⚙️ Opciones → 🌐 Idioma (o /idioma, /language), y el teclado de abajo
cambia con ellos; los atajos en inglés (/coins, /help, /greet, /go1) hacen lo mismo que los españoles; un aviso para otro
jugador le llega en SU idioma; el aviso del parche sale en el idioma de cada uno; el nombre de una zona es el mismo
lugar en los dos idiomas ("Vado Gris" = "Grey Ford").
Archivo: tests/test_idiomas.py · Módulo: M1 Núcleo (textos) · Prueba: engine/core/i18n.py (Texts.use), engine/core/
content.py (Content.locales), engine/service/game.py (_speaking, _language_action, _push_each, menu, announcement_view),
content/locales/es*.yaml y en*.yaml, tools/check_locales.py.
"""

import re

import pytest

from conftest import make_hero
from engine.core import FixedClock, MemoryStore, Rng, load_content
from engine.service import GameService
from tools.check_locales import compare

SPANISH = re.compile(r"[áéíóúñ¿¡]")


@pytest.fixture(scope="module")
def shared_content():
    return load_content()


def all_text(view):
    return "\n".join([view.title or "", view.notice or ""] + list(view.body) + [a.label for a in view.actions])


def english_hero(service, account="test:1", name="Lyra", class_id="guerrero_dps"):
    service.view(account)
    service.act(account, "lang:en")
    service.text(account, name)
    group = service.content.classes[class_id]["group"]
    service.act(account, f"grp:{group}")
    return service.act(account, f"cls:{class_id}")


def test_both_languages_have_the_same_keys_placeholders_and_tags(shared_content):
    assert set(shared_content.locales) >= {"es", "en"}
    errors, _warnings = compare(shared_content.locales["es"], shared_content.locales["en"])
    assert errors == []


def test_the_first_screen_offers_both_languages(service):
    view = service.view("test:9")
    assert view.kind == "create_name" and view.expects_text
    assert [a.id for a in view.actions] == ["lang:es", "lang:en"]
    assert any("Elige tu idioma" in line for line in view.body) and any("Choose your language" in line for line in view.body)
    view = service.act("test:9", "lang:en")
    assert view.kind == "create_name" and "Choose your language" not in "\n".join(view.body)
    assert "Lost Realms" in view.title and "awakening" in view.title.lower() or "Awakening" in view.title
    assert "✅" in view.actions[1].label and view.meta.get("menu_changed")
    view = service.text("test:9", "Ayla")
    assert view.kind == "create_class" and "Warrior" in all_text(view)
    assert not SPANISH.search(all_text(view))


def test_typing_a_name_right_away_keeps_spanish(service):
    make_hero(service)
    view = service.view("test:1")
    assert [a.label for a in service.menu("test:1")][0] == "📍 Zona"
    assert view.kind == "zone"


def test_an_english_hero_plays_everything_in_english(service):
    english_hero(service)
    labels = [a.label for a in service.menu("test:1")]
    assert labels == ["📍 Zone", "🧭 Explore", "🏕️ Camp", "👤 Hero", "⚙️ Options"]
    seen = []
    for action in ("home", "explore_menu", "claro", "hero", "options", "stats", "health", "bag", "wallet", "gear",
                   "talents", "map", "places", "oficios", "dudas", "trainer", "journal", "board", "guide"):
        seen.append(service.act("test:1", action))
    hero = service._load("test:1")
    service._start_combat(hero, service._zone(1, 0), Rng(5), "encounter.ambush")
    service._save(hero)
    for _ in range(25):
        state = service.store.get("combat", "test:1")
        if not state:
            break
        hero = service._load("test:1")
        hero.hp = 999
        service._save(hero)
        seen.append(service.act("test:1", ("atk", "ab:1", "ab:0", "ab:2")[state["round"] % 4]))
    assert not service.texts.missing
    assert not service.texts.fallbacks.get("en"), sorted(service.texts.fallbacks.get("en", []))[:20]
    leftovers = [line for view in seen for line in all_text(view).splitlines() if SPANISH.search(line)]
    assert leftovers == []


def test_old_players_switch_in_options_and_the_keyboard_follows(service):
    make_hero(service)
    options = service.act("test:1", "options")
    assert [a.id for a in options.actions][-1] == "lang" and len(options.actions) <= 4
    screen = service.act("test:1", "lang")
    assert screen.kind == "language" and [a.id for a in screen.actions] == ["lang:es", "lang:en", "options"]
    assert screen.actions[0].label.startswith("✅")
    view = service.act("test:1", "lang:en")
    assert view.kind == "options" and view.meta.get("menu_changed") and "English" in view.notice
    assert service.menu("test:1")[0].label == "📍 Zone"
    assert service.menu_labels()["📍 Zona"] == service.menu_labels()["📍 Zone"] == "home"
    assert service.act("test:1", "home").kind == "zone"
    back = service.act("test:1", "lang:es")
    assert "español" in back.notice and service.menu("test:1")[0].label == "📍 Zona"
    assert service.text("test:1", "/language").kind == "language"


def test_english_commands_do_what_the_spanish_ones_do(service):
    english_hero(service)
    assert service.text("test:1", "/coins").kind == service.text("test:1", "/monedas").kind
    assert service.text("test:1", "/professions").kind == service.text("test:1", "/oficios").kind
    found = service.text("test:1", "/help energy")
    assert found.kind.startswith("duda") and "energy" in all_text(found).lower()     # one hit opens the answer
    assert service.commands()["/help"] == service.commands()["/dudas"]
    assert service._canonical_command("/greet Bram") == "/saludar Bram"


def test_a_message_for_another_player_comes_in_their_language(content):
    service = GameService(content, MemoryStore(), FixedClock(), world_seed=7)
    make_hero(service, "test:1", "Lyra")
    english_hero(service, "test:2", "Bram")
    service.act("test:1", "home")
    service.act("test:2", "home")
    service.tick()
    service.text("test:1", "/saludar")
    delivered = dict(service.tick())
    assert "test:2" in delivered
    text = all_text(delivered["test:2"])
    assert not SPANISH.search(text) and "Lyra" in text


def test_the_patch_notes_come_in_each_players_language(service):
    make_hero(service, "test:1", "Lyra")
    english_hero(service, "test:2", "Bram")
    latest = list(service.content.patches.values())[-1]
    assert latest.get("title_en") and latest.get("notes_en")
    assert service.announcement_view("test:1").title == latest["title"]
    assert service.announcement_view("test:2").title == latest["title_en"]


def test_a_zone_is_the_same_place_in_both_languages(service):
    zone = service._zone(3, -2)
    with service.texts.use("es"):
        spanish = service._zone_name(zone)
    with service.texts.use("en"):
        english = service._zone_name(zone)
    first_es, first_en = service.texts.list("world.name_first", "es"), service.texts.list("world.name_first", "en")
    assert first_es[zone.name_index[0] % len(first_es)] in spanish
    assert first_en[zone.name_index[0] % len(first_en)] in english
    assert spanish != english
