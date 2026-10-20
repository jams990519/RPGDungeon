"""📚 Guías of ❓ Dudas (D-297): the extra button, its categories and every guide, in Spanish and English; ❓ Dudas in ⚙️.

[ES] Pruebas del pedido del dueño (20-oct-2026): "un botón extra como si fuese un submenú con subguías de acuerdo a sus
clases, cómo conseguir recursos, cómo funciona cada cosa… tanto en español y en inglés" y "agrega el botón de dudas también
en el botón de opción". Revisa que:
- ❓ Dudas muestra 📚 Guías primero (y a lo ancho), todos sus temas y ↩️ Volver: 9 botones, uno más que los centros;
- 📚 Guías abre sus 3 categorías y cada categoría sus guías, sin pasar el tope de botones (de a 6 con ➡️ Más si son más de 7);
- TODAS las guías se abren en español y en inglés, de 5 a 9 líneas, sin un marcador {…} sin llenar, sin textos que falten
  ni prestados del español, y con ↩️ Volver a su categoría y ❓ Dudas;
- hay una guía por cada clase que se juega (las 6), con su nombre, sus 2 roles y la cadena de cada rol como en el juego;
- con una guía abierta, lo que escribes se busca en ❓ Dudas;
- ⚙️ Opciones trae ❓ Dudas y su ↩️ Volver vuelve a ⚙️ Opciones; desde 🏕️ Campamento vuelve al centro, como antes;
- 👤 Héroe sigue con sus 8 botones (ya estaba lleno: ahí no entra ❓ Dudas).
Archivo: tests/test_guias.py · Módulo: capa de servicios (❓ Dudas) · Prueba: engine/service/game.py (sección "📚 Guías",
_dudas_view, _dudas_action, _dudas_back, _options_view, button_cap), content/guides.yaml, content/locales/es_guias.yaml y
en_guias.yaml.
"""

import re

import pytest

from conftest import make_hero
from engine.service.game import HUB_BUTTONS, button_cap

PLACEHOLDER = re.compile(r"\{[a-z_]+[^{}]*\}")
SPANISH = re.compile(r"[áéíóúñ¿¡]")


def ids(view):
    return [a.id for a in view.actions]


def all_text(view):
    return "\n".join([view.title or "", view.notice or ""] + list(view.body) + [a.label for a in view.actions])


def walk(service, account="test:1"):
    """Every 📚 Guías screen: the menu, each category (every page) and each guide, as (action, view)."""
    seen = [("guides", service.act(account, "guides"))]
    for category in service._guidebook_categories():
        page = service.act(account, f"guides:{category}")
        seen.append((f"guides:{category}", page))
        for _ in range(5):                               # ➡️ Más goes round the pages
            more = [a.id for a in page.actions if a.id.startswith(f"guides:{category}:")]
            if not more or more[0] == f"guides:{category}:0":
                break
            page = service.act(account, more[0])
            seen.append((more[0], page))
    for gid in service._guidebook_entries():
        seen.append((f"guide:{gid}", service.act(account, f"guide:{gid}")))
    return seen


def test_dudas_shows_guides_first_and_still_every_topic_and_back(service):
    make_hero(service)
    view = service.act("test:1", "dudas")
    topics = service._faq_topics()
    assert view.kind == "dudas" and ids(view)[0] == "guides" and view.actions[0].label == "📚 Guías"
    assert ids(view)[1:-1] == [f"dudas:{topic}" for topic in topics] and len(topics) == 7
    assert ids(view)[-1] == "claro"                              # opened from 🏕️ Campamento: back to the hub, as before
    assert len(view.actions) == HUB_BUTTONS + 1 == button_cap("dudas")      # D-297: the owner asked for one extra button
    assert view.layout[0] == 1 and view.layout[-1] == 1 and sum(view.layout) == len(view.actions)   # 📚 and ↩️ wide
    assert any("📚 Guías" in line for line in view.body)


def test_each_category_opens_and_stays_within_the_buttons(service):
    make_hero(service)
    menu = service.act("test:1", "guides")
    categories = service._guidebook_categories()
    assert categories == ["classes", "resources", "howto"]
    assert menu.kind == "guides" and ids(menu) == [f"guides:{c}" for c in categories] + ["dudas"]
    assert [a.label for a in menu.actions][:3] == ["🎭 Clases", "🪵 Recursos", "⚙️ Cómo funciona"]
    assert len(menu.actions) <= button_cap(menu.kind)
    for category in categories:
        view = service.act("test:1", f"guides:{category}")
        assert view.kind == "guides_category" and ids(view)[-1] == "guides", category
        assert len(view.actions) <= button_cap(view.kind) == HUB_BUTTONS, category
        guides = [i for i in ids(view) if i.startswith("guide:")]
        assert guides and all(i[6:] in service._guidebook_entries(category) for i in guides), category
    assert service.act("test:1", "guides:nada").kind == "guides"          # an unknown category goes back to 📚 Guías
    assert service.act("test:1", "guide:nada").kind == "guides"           # and so does an unknown guide
    assert service.act("test:1", "guides").actions[-1].id == "dudas"


def test_a_long_category_goes_in_pages_with_more(service):
    make_hero(service)
    guides = service.content.guides["guides"]
    for n in range(4):                                   # 11 guides in ⚙️ Cómo funciona: 6 a page and ➡️ Más
        guides[f"extra{n}"] = {"category": "howto"}
        service.content.texts.setdefault("guides_page", {})[f"extra{n}"] = {"title": f"Extra {n}", "text": "Línea"}
    first = service.act("test:1", "guides:howto")
    assert len(first.actions) == HUB_BUTTONS and ids(first)[-2:] == ["guides:howto:1", "guides"]
    second = service.act("test:1", "guides:howto:1")
    assert second.kind == "guides_category" and ids(second)[-2:] == ["guides:howto:0", "guides"]
    shown = [i for i in ids(first) + ids(second) if i.startswith("guide:")]
    assert len(shown) == len(set(shown)) == len(service._guidebook_entries("howto")) == 11


@pytest.mark.parametrize("lang", ["es", "en"])
def test_every_guide_opens_in_both_languages_without_gaps(service, lang):
    make_hero(service)
    if lang == "en":
        service.act("test:1", "lang:en")
    screens = walk(service)
    pages = [(action, view) for action, view in screens if action.startswith("guide:")]
    assert len(pages) == len(service._guidebook_entries()) >= 17
    for action, view in screens:
        text = all_text(view)
        assert not PLACEHOLDER.search(text), (lang, action, PLACEHOLDER.findall(text))
        assert "[" not in view.title and not any(line.startswith("[guides") for line in view.body), (lang, action)
        assert len(view.actions) <= button_cap(view.kind), (lang, action, view.kind)
        assert view.expects_text, action                             # typing still searches ❓ Dudas
        if lang == "en":
            assert not SPANISH.search(text), (action, [line for line in text.splitlines() if SPANISH.search(line)])
    for action, view in pages:
        category = service._guidebook_entries()[action[6:]]["category"]
        assert view.kind == "guides_page" and ids(view) == [f"guides:{category}", "dudas"], action
        lines = [line for line in view.body if line.strip()]
        assert 5 <= len(lines) <= 9, (lang, action, len(lines))      # the owner wants short guides
    assert not service.texts.missing
    assert not service.texts.fallbacks.get("en"), sorted(service.texts.fallbacks.get("en", []))


def test_one_guide_per_class_with_its_roles_and_chains(service):
    make_hero(service)
    entries = service._guidebook_entries("classes")
    groups = service._class_groups()
    assert len(groups) == 6 and sorted(e["class"] for e in entries.values()) == sorted(groups)
    for gid, entry in entries.items():
        view = service.act("test:1", f"guide:{gid}")
        group = entry["class"]
        assert view.title == service.texts.t(f"class_group.{group}.name"), gid       # "🤺 Guerrero": the game's own name
        text = "\n".join(view.body)
        specs = [cid for cid, cdef in service.content.classes.items() if cdef.get("group") == group and not cdef.get("retired")]
        assert len(specs) == 2, group
        for cid in specs:
            sdef = service.content.classes[cid]
            assert service.texts.t(sdef["name_key"]) in text, (gid, cid)          # "🐢 Guerrero · Tanque"
            assert service._chain_order_text(sdef) in text, (gid, cid)            # its chain, with the buttons' names
        assert service.texts.t(f"guides_page.{group}.tip") in text


def test_class_guides_never_borrow_a_class_icon(service):
    """D-293: the hand-written lines of the guides (intro, tip, the rest) use no class or role icon at all."""
    icons = set()
    for texts in service.content.locales.values():
        for cid, cdef in service.content.classes.items():
            if cdef.get("retired"):
                continue
            icons.add(texts["class_group"][cdef["group"]]["name"].split(" ")[0].replace("️", ""))
            icons.add(cdef["icon"].replace("️", ""))
    def strings(node):
        if isinstance(node, dict):
            for value in node.values():
                yield from strings(value)
        elif isinstance(node, str):
            yield node

    for lang, texts in service.content.locales.items():
        for key in ("guides", "guides_page"):
            blob = "\n".join(strings(texts[key])).replace("️", "")
            assert not [icon for icon in icons if icon in blob], (lang, key)


def test_typing_on_a_guide_searches_dudas(service):
    make_hero(service)
    service.act("test:1", "guide:energy")
    found = service.text("test:1", "energía")
    assert found.kind in ("duda", "dudas_results")
    service.act("test:1", "home")                                    # leaving: text is not a search any more
    assert service.store.get("dudas_open", "test:1") is None


def test_dudas_from_options_goes_back_to_options(service):
    make_hero(service)
    options = service.act("test:1", "options")
    assert "dudas@options" in ids(options) and ids(options)[-1] == "home"
    assert len(options.actions) == button_cap("options") == 5           # D-297: one more than D-75's 4, the owner asked
    view = service.act("test:1", "dudas@options")
    assert view.kind == "dudas" and ids(view)[-1] == "options"
    service.act("test:1", "dudas:world")                                  # a topic, an answer, a guide: the way back stays
    service.act("test:1", "duda:d07")
    service.act("test:1", "guide:map")
    assert ids(service.act("test:1", "dudas"))[-1] == "options"
    assert service.act("test:1", "options").kind == "options"
    hub = service.act("test:1", "claro")                                  # from 🏕️ Campamento: back to the hub, as always
    assert ids(service.act("test:1", "dudas"))[-1] == "claro"
    assert ids(hub)[-1] == "dudas"
    service.store.put("dudas_open", "test:1", {"at": 0, "from": "zzz"})   # an unknown origin is never a button
    assert ids(service.act("test:1", "dudas"))[-1] == "claro"
    assert ids(service.act("test:1", "dudas@nada"))[-1] == "claro"


def test_dudas_from_options_in_english(service):
    make_hero(service)
    service.act("test:1", "lang:en")
    options = service.act("test:1", "options")
    assert [a.label for a in options.actions if a.id == "dudas@options"] == ["❓ Help"]
    view = service.act("test:1", "dudas@options")
    assert view.actions[0].label == "📚 Guides" and view.actions[-1].label == "↩️ Back"
    assert not service.texts.fallbacks.get("en")


def test_hero_hub_is_still_full(service):
    make_hero(service)
    view = service.act("test:1", "hero")
    assert view.kind == "hero" and len(view.actions) == HUB_BUTTONS and "dudas" not in ids(view)   # E-132: no room
