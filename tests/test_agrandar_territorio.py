"""🗺️ Agrandar territorio (D-304, 0.41): where the camp grows, by direction, up to the zones of its stage; and its 🤝 assistants.

[ES] Pruebas del pedido del dueño del 20-oct-2026 ("en territorio es donde vas a escoger para dónde te vas a expandir, en qué
dirección"; "dame la opción como dueño de gremio para agregar un asistente… que va a permitir definir hacia dónde va a avanzar
el territorio junto contigo"; y la tabla de zonas de E-218, que confirmó):
- la pantalla tiene el minimapa de 5 × 5 centrado en el campamento, una línea por zona libre con su dirección (8, el norte suma
  a la y) y un botón por zona con su número y dirección; de a 2 con ➡️ Más zonas (4 botones como máximo);
- cuesta camps.grow_cost_per_level × las zonas que ya tiene, sin cofres, y el nivel NO cambia; los ids viejos siguen andando;
- cada etapa tiene su tope de zonas (3, 5, 9, 15, 25): al tope, el aviso y ⏫ Siguiente nivel; quien ya tenía más, las conserva;
- solo el fundador y los 🤝 asistentes eligen la zona; los demás ven todo y la línea de quién elige; a los demás les llega
  hacia dónde creció; en 👥 Miembros el fundador ve cómo nombrar un asistente; los textos dicen "asistente";
- 🔨 Mejoras nombra a todos las obras sin activar; la hambruna no deja agrandar; y se lee en inglés.
Archivo: tests/test_agrandar_territorio.py · Módulo: M14 Construcción · Prueba: engine/service/game.py (_grow_view,
_grow_camp, _grow_candidates, _territory_map, _direction_key, _zones_cap, _upgrades_view) y engine/service/gremio.py
(_helpers_founder_line)
"""

from conftest import make_hero
from test_camps import old_camp_at, place
from test_guilds import join, set_level
from engine.service.game import button_cap

KEY = "6:0"


def ids(view):
    return [a.id for a in view.actions]


def text(view):
    return "\n".join([view.notice or ""] + view.body)


def camp(service):
    return service.store.get("camp", KEY)


def camp_with(service, *names, level=1):
    make_hero(service, "test:1", "Lyra")
    old_camp_at(service, "test:1", 6, 0, name="Roca Alta")
    set_level(service, level)
    for n, name in enumerate(names, 2):
        make_hero(service, f"test:{n}", name)
        join(service, f"test:{n}")
        place(service, f"test:{n}", 6, 0)
    service.tick()


def grid(view):
    return [line for line in view.body if line and set(line) <= set("▫️🟩🔸⬛🏕️1️⃣2️⃣3️⃣️⃣")]


def test_the_mini_map_and_one_line_per_direction(service):
    camp_with(service)
    view = service.act("test:1", "improve")
    view = service.act("test:1", "grow")
    assert view.kind == "camp_grow" and view.title == "🗺️ Agrandar territorio"
    assert view.body[0] == "🗺️ Tu campamento ocupa 1 de las 3 zonas que permite la etapa campamento."
    assert "Cada zona nueva cuesta 🪵 Madera ×15 · 🪨 Piedra ×10 · 🧵 Fibra ×5, de tu mochila." in view.body
    rows = grid(view)
    assert rows == ["▫️▫️▫️▫️▫️", "▫️▫️1️⃣▫️▫️", "▫️🔸🏕️2️⃣▫️", "▫️▫️🔸▫️▫️", "▫️▫️▫️▫️▫️"]
    assert "🏕️ centro · 1️⃣ para elegir · 🔸 libre (➡️ Más zonas)" in view.body
    assert "1️⃣ ⬆️ Norte · (6, 1) · ❔" in view.body and "2️⃣ ➡️ Este · (7, 0) · ❔" in view.body
    assert ids(view) == ["claim:6:1", "claim:7:0", "grow:1", "improve"]
    assert [a.label for a in view.actions[:3]] == ["1️⃣ ⬆️ Norte", "2️⃣ ➡️ Este", "➡️ Más zonas"]
    assert len(view.actions) <= button_cap(view.kind) == 4
    more = service.act("test:1", "grow:1")
    assert ids(more) == ["claim:6:-1", "claim:5:0", "grow:0", "improve"]
    assert [a.label for a in more.actions[:2]] == ["1️⃣ ⬇️ Sur", "2️⃣ ⬅️ Oeste"]


def test_eight_directions_north_is_plus_y(service):
    cases = {(0, 1): "n", (1, 1): "ne", (1, 0): "e", (1, -1): "se", (0, -1): "s", (-1, -1): "sw", (-1, 0): "w",
             (-1, 1): "nw", (2, 1): "ne", (3, 1): "e", (1, 3): "n", (-3, -1): "w"}
    for (dx, dy), key in cases.items():
        assert service._direction_key(dx, dy) == key, (dx, dy)
    assert service.texts.t("territory.dir.ne") == "↗️ Noreste"


def test_the_cost_follows_the_zones_and_the_level_stays(service):
    camp_with(service)
    view = service.act("test:1", "claim:6:1")
    assert camp(service)["level"] == 1 and camp(service)["zones"] == [[6, 0], [6, 1]]
    assert view.kind == "camp_grow" and view.notice.startswith("🗺️ ¡El territorio creció hacia el ⬆️ Norte!")
    assert "2 de 3 zonas" in view.notice and service.store.get("territory", "6:1") == {"camp": KEY}
    hero = service._load("test:1")
    assert (hero.backpack["madera"], hero.backpack["piedra"], hero.backpack["fibra"]) == (165, 180, 95)
    assert "Cada zona nueva cuesta 🪵 Madera ×30 · 🪨 Piedra ×20 · 🧵 Fibra ×10, de tu mochila." in view.body
    assert "🟩" in "".join(grid(view))
    service.act("test:1", "claim:7:0")
    hero = service._load("test:1")
    assert hero.backpack["madera"] == 135 and hero.chests == 0 and camp(service)["level"] == 1


def test_each_stage_has_its_zone_cap(service):
    assert service.content.balance["camps"]["zones_by_stage"] == {"campamento": 3, "aldea": 5, "pueblo": 9, "ciudad": 15,
                                                                  "castillo": 25}
    assert [service._zones_cap_at(level) for level in range(1, 10)] == [3, 3, 5, 5, 9, 9, 15, 15, 25]
    camp_with(service)
    service.act("test:1", "claim:6:1")
    service.act("test:1", "claim:7:0")
    view = service.act("test:1", "grow")
    assert "Llegaste al tope de zonas de tu nivel: sube de nivel para agrandar más." in view.body
    assert ids(view) == ["lvlup", "improve"] and view.actions[0].label == "⏫ Siguiente nivel"
    backpack = dict(service._load("test:1").backpack)
    view = service.act("test:1", "claim:5:0")
    assert len(camp(service)["zones"]) == 3 and service._load("test:1").backpack == backpack
    set_level(service, 3)                                               # aldea: up to 5
    assert ids(service.act("test:1", "grow"))[-1] == "improve" and "claim:" in ids(service.act("test:1", "grow"))[0]


def test_a_camp_over_its_cap_keeps_its_zones(service):
    camp_with(service)
    data = camp(service)
    data["zones"] = [[6, 0], [7, 0], [8, 0], [6, 1], [6, -1]]           # 5 zones at level 1 (cap 3): nothing is taken away
    service.store.put("camp", KEY, data)
    view = service.act("test:1", "grow")
    assert view.body[0] == "🗺️ Tu campamento ocupa 5 de las 3 zonas que permite la etapa campamento." and "lvlup" in ids(view)
    assert len(camp(service)["zones"]) == 5


def test_only_the_founder_and_the_assistants_choose_where(service):
    camp_with(service, "Bram", "Cora")
    place(service, "test:2", 6, 0, backpack={"madera": 99, "piedra": 99, "fibra": 99})
    view = service.act("test:2", "grow")
    assert "🤝 La dirección la eligen el fundador o un asistente." in view.body
    assert grid(view) and "1️⃣ ⬆️ Norte · (6, 1) · ❔" in view.body
    assert not any(i.startswith("claim:") for i in ids(view)) and ids(view) == ["grow:1", "improve"]
    view = service.act("test:2", "claim:6:1")                           # an old or typed button: nothing paid
    assert view.notice == "🤝 La dirección la eligen el fundador o un asistente."
    assert len(camp(service)["zones"]) == 1 and service._load("test:2").backpack["madera"] == 99
    service.act("test:1", "ghelp:test:2")                               # Lyra makes Bram an assistant
    assert camp(service)["helpers"] == ["test:2"]
    service.tick()
    view = service.act("test:2", "grow")
    assert ids(view)[:2] == ["claim:6:1", "claim:7:0"]
    service.act("test:2", "claim:7:0")
    assert camp(service)["zones"] == [[6, 0], [7, 0]] and service._load("test:2").backpack["madera"] == 84
    told = [v for acc, v in service.tick() if acc in ("test:1", "test:3") and v.kind == "camp_news"]
    assert len(told) == 2 and all("Bram agrandó Roca Alta hacia el ➡️ Este" in v.body[0] for v in told)


def test_the_founder_sees_how_to_name_an_assistant(service):
    make_hero(service, "test:1", "Lyra")
    old_camp_at(service, "test:1", 6, 0, name="Roca Alta")
    alone = service.act("test:1", "gmembers")
    assert "🤝 Asistentes: 0 de 1. Cuando entre otro miembro, podrás nombrarlo asistente." in alone.body
    make_hero(service, "test:2", "Bram")
    join(service, "test:2")
    view = service.act("test:1", "gmembers")
    assert "🤝 Asistentes: 0 de 1 — toca el código de un miembro (/m2) y elige 🤝 Hacer asistente." in view.body
    code = next(line for line in view.body if line.startswith("/m") and "Bram" in line).split()[0]
    card = service.text("test:1", code)
    assert card.actions[0].label == "🤝 Hacer asistente"
    view = service.act("test:1", "ghelp:test:2")
    assert "Bram ahora es asistente: activa obras, elige hacia dónde crece el territorio" in view.notice
    founder = service.act("test:1", "gmembers")
    assert "🤝 Asistentes: 1 de 1: Bram — toca el código de un miembro (/m2) y elige 🤝 Hacer asistente." in founder.body
    member = service.act("test:2", "gmembers")
    assert "🤝 Asistentes (1/1): Bram" in member.body
    assert not any("ayudante" in line.lower() for line in text(founder).splitlines() + text(member).splitlines())


def test_every_member_sees_the_works_that_are_not_active_yet(service):
    camp_with(service, "Bram")
    member = service.act("test:2", "upgrades")
    assert ("⏸️ Sin activar: 🔥 Fogón · 🪵 Empalizada · 🪚 Aserradero · 🧶 Tejeduría · 🗿 Cantería (las activa el fundador o "
            "un 🤝 asistente).") in member.body
    founder = service.act("test:1", "upgrades")
    assert "▶️ Para activar en 🏘️ Servicios: 🔥 Fogón · 🪵 Empalizada · 🪚 Aserradero · 🧶 Tejeduría · 🗿 Cantería." in founder.body
    service.act("test:1", "upact:fogon:w")                               # active: everyone sees its bar
    member = service.act("test:2", "upgrades")
    assert any(line.startswith("🔥 Fogón") and "%" in line for line in member.body)
    assert any(line.startswith("⏸️ Sin activar: 🪵 Empalizada") for line in member.body)
    works = service.act("test:2", "upw")
    assert not any(i.startswith("upact:") for i in ids(works)) and "upg:fogon" in ids(works)


def test_an_empty_pantry_blocks_the_territory(service):
    camp_with(service, level=3)
    service.store.put("pantry", KEY, {"rations": 0.0, "at": service.clock.now()})
    view = service.act("test:1", "grow")
    assert view.kind == "camp_improve" and view.notice == service.texts.t("pantry.grow_famine")
    view = service.act("test:1", "claim:6:1")
    assert view.kind == "camp_improve" and len(camp(service)["zones"]) == 1


def test_the_territory_reads_well_in_english(service):
    from test_idiomas import english_hero
    english_hero(service, "test:1", "Lyra")
    old_camp_at(service, "test:1", 6, 0, name="Grey Rock")
    view = service.act("test:1", "grow")
    assert view.title == "🗺️ Expand territory" and view.body[0] == "🗺️ Your camp takes 1 of the 3 zones its stage (camp) allows."
    assert [a.label for a in view.actions[:2]] == ["1️⃣ ⬆️ North", "2️⃣ ➡️ East"]
    view = service.act("test:1", "claim:6:1")
    assert view.notice.startswith("🗺️ The territory grew to the ⬆️ North!")
    for screen in (view, service.act("test:1", "gmembers"), service.act("test:1", "campinfo")):
        assert "[" not in text(screen), text(screen)
    assert "🤝 Assistants: 0 of 1. When another member joins, you can name them assistant." in service.act("test:1", "gmembers").body
    assert not service.texts.fallbacks.get("en"), sorted(service.texts.fallbacks.get("en", []))[:20]
    assert not service.texts.missing
