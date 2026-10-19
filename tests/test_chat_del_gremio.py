"""Guild chat and who is who on the map: any loose text of a member reaches the whole guild (D-285); each mate on the map
with its class's emoji and a line saying who it is (D-286).

[ES] Pruebas de lo que pidió el dueño el 19-oct-2026 ("cuando ya se crea un gremio, todos los mensajes que se envíen dentro
del juego van a ser recibidos por el resto de jugadores"; y del mapa: "para saber diferenciar dónde está cada quien y qué
tipo es"):
- en un gremio sin campamento, el texto suelto le llega a cada compañero (en su idioma) y queda en 🛡️ Gremio;
- con campamento, igual: le llega a los del campamento y queda en su 🛡️ Gremio;
- sin gremio, el texto suelto sigue avisando que se usen los botones; los comandos con "/" y las pantallas que piden texto
  (❓ Dudas, 💬 Feedback, los nombres) no se mandan al gremio;
- en el 🗺️ Mapa cada compañero sale con el emoji de su clase, 👥 si hay varios en la misma zona, y arriba una línea por
  compañero: nombre, clase y coordenadas; también cuántos quedan fuera del mapa. Y todo se lee en inglés.
Archivo: tests/test_chat_del_gremio.py · Módulo: M15 Social, M8 Mundo · Prueba: engine/service/gremio.py (_guild_chat,
_gremio_view), engine/service/game.py (text, _guild_view, _map_view, _map_mate_lines).
"""

from conftest import make_hero
from test_camps import old_camp_at, place
from test_gremio_desde_el_inicio import join, new_gremio, pushes


def text(view):
    return "\n".join([view.notice or ""] + view.body)


def label(service, account):
    """("🌳", "Druida"): the mark the map draws and the class its line names, as 👤 Héroe says it."""
    mark, _, cls = service._class_label(service.store.get("hero", account)).partition(" ")
    return mark, cls


def guild_of_three(service):
    make_hero(service, "test:1", "Lyra", "guerrero")
    make_hero(service, "test:2", "Bram", "picaro")                               # 0.31: the old Pícaro is a 🌳 Druida now
    make_hero(service, "test:3", "Cira", "sacerdote")
    gid, _ = new_gremio(service)
    join(service, gid, "test:2")
    join(service, gid, "test:3")
    service.tick()                                                                # the join notices are not this test's
    return gid


def test_loose_text_reaches_the_whole_guild_before_a_camp(service):
    from test_idiomas import english_hero
    make_hero(service, "test:1", "Lyra")
    english_hero(service, "test:2", "Bram")
    gid, _ = new_gremio(service)
    join(service, gid, "test:2")
    service.tick()
    view = service.text("test:1", "  Nos vemos en el  bosque ")
    assert "Enviado a tu gremio (1 compañero)" in view.notice
    got = pushes(service, "test:2", "gremio_message")
    assert got and got[0].title == "📢 Guild Lobos Grises" and "💬 Lyra: Nos vemos en el bosque" in got[0].body
    assert not pushes(service, "test:1", "gremio_message")                        # not to who wrote it
    assert service.store.get("gremio", gid)["messages"][-1]["text"] == "Nos vemos en el bosque"
    hub = text(service.act("test:2", "guild"))
    assert "💬 Lyra: Nos vemos en el bosque" in hub and "whole guild gets it" in hub
    assert not service.texts.fallbacks.get("en")


def test_loose_text_reaches_the_camp_once_it_is_founded(service):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    old_camp_at(service, "test:1", 6, 0, name="Roca Alta")
    camp = service.store.get("camp", "6:0")
    camp["members"].append("test:2")
    service.store.put("camp", "6:0", camp)
    place(service, "test:2", 6, 0, camp="6:0")
    service.tick()
    view = service.text("test:2", "¿Quién trae piedra?")
    assert "Enviado a tu gremio (1 compañero)" in view.notice
    got = pushes(service, "test:1", "gremio_message")
    assert got and "Roca Alta" in got[0].title and "💬 Bram: ¿Quién trae piedra?" in got[0].body
    guild = text(service.act("test:1", "guild"))
    assert "💬 Bram: ¿Quién trae piedra?" in guild and "le llega a todo tu gremio" in guild


def test_without_a_guild_and_other_text_screens_nothing_is_sent(service):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    view = service.text("test:1", "hola")
    assert "botones" in view.notice                                              # no guild: the old hint
    gid, _ = new_gremio(service)
    join(service, gid, "test:2")
    service.tick()
    service.text("test:1", "/nada")                                              # a command is never a message
    service.act("test:1", "dudas")
    service.text("test:1", "energía")                                            # ❓ Dudas open: a search
    service.act("test:1", "home")
    assert not pushes(service, "test:2", "gremio_message")
    assert not service.store.get("gremio", gid).get("messages")


def test_each_mate_on_the_map_shows_its_class_and_who_it_is(service):
    guild_of_three(service)
    make_hero(service, "test:4", "Dario")
    place(service, "test:2", 2, 1)
    place(service, "test:3", -3, 0)
    place(service, "test:4", 1, 0)                                                # not in the guild: not drawn
    view = service.act("test:1", "map")
    grid = [line for line in view.body if " " not in line]                       # the map's rows (the legend has spaces)
    (bram, bram_cls), (cira, cira_cls) = label(service, "test:2"), label(service, "test:3")
    assert bram != cira
    assert sum(line.count("🧍") for line in grid) == 1
    assert sum(line.count(bram) for line in grid) == 1 and sum(line.count(cira) for line in grid) == 1
    body = text(view)
    assert "🛡️ Tu gremio en el mapa (2):" in body
    assert f"{bram} Bram · {bram_cls} · (2, 1)" in body and f"{cira} Cira · Sacerdote · (-3, 0)" in body
    assert body.index("Bram") < body.index("Cira")                                # the nearest first
    assert "Dario" not in body
    assert view.body.index(grid[0]) > max(i for i, line in enumerate(view.body) if "Cira" in line)   # all above the grid


def test_several_in_one_zone_and_mates_off_the_map(service):
    guild_of_three(service)
    place(service, "test:2", 1, 1)
    place(service, "test:3", 1, 1)
    view = service.act("test:1", "map")
    grid = [line for line in view.body if " " not in line]
    assert sum(line.count("👥") for line in grid) == 1
    body = text(view)
    assert f"Bram · {label(service, 'test:2')[1]} · (1, 1)" in body and "Cira · Sacerdote · (1, 1)" in body and "👥 varios" in body
    place(service, "test:3", 40, 0)                                               # far away: off this map
    body = text(service.act("test:1", "map"))
    assert "1 compañero fuera de este mapa" in body and "Cira" not in body


def test_the_map_s_guild_lines_read_well_in_english(service):
    from test_idiomas import english_hero
    english_hero(service)
    make_hero(service, "test:2", "Bram", "sacerdote")
    gid, _ = new_gremio(service)
    join(service, gid, "test:2")
    place(service, "test:2", 2, 1)
    body = text(service.act("test:1", "map"))
    assert "🛡️ Your guild on the map (1):" in body and "📿 Bram · Priest · (2, 1)" in body
    assert not service.texts.fallbacks.get("en")
