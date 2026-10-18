"""Every place names its coordinates, and /ir x y lays out the 🔗 Moverte road to any of them (D-278, D-279).

[ES] Pruebas de lo que pidió el dueño el 18-oct-2026 ("asegúrate que todas las posiciones tengan una coordenada para cuando
los jugadores quieran moverse en una coordenada ya sepan cómo hacerlo"):
- las rutas de 📍 Zona, el 🗺️ Mapa, 📒 Lugares, la confirmación del viaje y los avisos del viaje dicen las coordenadas;
- /ir x y (también /ir x,y y /go (x, y)) arma 🔗 Moverte hasta ahí, primero este-oeste y después norte-sur, sin salir solo;
  más de 50 pasos dice hasta dónde llegar primero; ya ahí u ocupado, avisa;
- ❓ Dudas explica cómo ir a una coordenada;
- y el gremio se arma desde cualquier lugar (D-279): 🛡️ Gremio está en 🏕️ Campamento aunque no haya campamento ahí.
Archivo: tests/test_coordenadas.py · Módulo: M2 Mundo y viaje, M15 Social · Prueba: engine/service/game.py (_place_label,
_coord_walk, COORD_RE, _zone_view, _places_view, _map_view, _camp_here_view), content/faq.yaml (d54).
"""

from conftest import make_hero
from test_camps import place


def ids(view):
    return [a.id for a in view.actions]


def text(view):
    return "\n".join([view.notice or ""] + view.body)


def test_routes_the_map_and_places_say_their_coordinates(service):
    make_hero(service)
    place(service, "test:1", 2, -1, known=["0:0", "2:-1"])
    zone = text(service.act("test:1", "home"))
    assert "Norte (2, 0)" in zone and "Sur (2, -2)" in zone and "Este (3, -1)" in zone and "Oeste (1, -1)" in zone
    assert "tú, en (2, -1)" in text(service.act("test:1", "zmap"))
    places = text(service.act("test:1", "places"))
    assert "El Claro (0, 0)" in places and "/ir x y" in places
    confirm = text(service.act("test:1", "goask:0:0"))
    assert "(0, 0)" in confirm
    started = service.act("test:1", "goto:0:0")
    assert "El Claro (0, 0)" in text(started)                          # the trip screen and its notice


def test_ir_x_y_lays_out_the_walk_east_west_then_north_south(service):
    make_hero(service)
    view = service.text("test:1", "/ir 2 -3")
    assert view.kind == "walk" and "(2, -3)" in view.notice and "5 pasos" in text(view)
    assert service.store.get("walk", "test:1")["steps"] == ["e", "e", "s", "s", "s"]
    assert not service._load("test:1").activity                        # it does not leave by itself
    service.act("test:1", "wlk:go")
    trip = service._load("test:1").activity
    assert trip["kind"] == "travel" and trip["goal"] == [2, -3] and trip["walk"]
    for typed in ("/ir -1,4", "/go (-1, 4)", "/ir_-1 4"):
        make_hero(service, "test:9", "Otra")
        assert service.store.get("walk", "test:9") is None
        service.text("test:9", typed)
        assert service.store.get("walk", "test:9")["steps"] == ["w", "n", "n", "n", "n"], typed
        service.store.delete("hero", "test:9")
        service.store.delete("walk", "test:9")


def test_too_far_here_or_busy_only_explains(service):
    make_hero(service)
    far = service.text("test:1", "/ir 40 30")
    assert "70 pasos" in far.notice and "/ir 40 10" in far.notice                 # 50 steps along the road first
    assert not (service.store.get("walk", "test:1") or {}).get("steps")           # nothing laid out
    assert "Ya estás en (0, 0)" in service.text("test:1", "/ir 0 0").notice
    service.act("test:1", "go:e")
    assert service._load("test:1").activity
    busy = service.text("test:1", "/ir 5 5")
    assert "primero termina" in busy.notice and service._load("test:1").activity["kind"] == "travel"


def test_dudas_explain_how_to_go_to_a_coordinate(service):
    make_hero(service)
    view = service.text("test:1", "/dudas coordenada")
    assert "/ir x y" in text(view) or any("d54" in a.id for a in view.actions)
    answer = text(service.text("test:1", "/d54"))
    assert "/ir x y" in answer and "(0, 0)" in answer


def test_the_guild_button_is_there_where_there_is_no_camp(service):
    make_hero(service)
    place(service, "test:1", 3, 0, known=["0:0", "3:0"])
    view = service.act("test:1", "claro")
    assert view.kind == "found_camp" and "guild" in ids(view) and len(view.actions) <= 4
    assert service.act("test:1", "guild").kind == "gremio_none"           # create or search a guild from here


def test_coordinates_read_well_in_english(service):
    from test_idiomas import english_hero
    english_hero(service)
    zone = text(service.act("test:1", "home"))
    assert "North (0, 1)" in zone
    view = service.text("test:1", "/go 1 1")
    assert "(1, 1)" in view.notice and "/go x y" in text(view)
    assert not service.texts.fallbacks.get("en")
