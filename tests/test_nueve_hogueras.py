"""The 9 bonfires: where they are, what each one has, who is born where and where arrivals go when one is full (D-265, D-277).

[ES] Pruebas de lo que pidió el dueño (D-265: "en cada fogata… cuando exceda 20 jugadores vas a sacar a los jugadores a una
hoguera cercana"; D-277: el peligro desde la hoguera más cercana, las 9 a la vista desde el primer día, nombres por su lado
y una sola despensa):
- son 9: el Claro y 8 a 12 zonas; cada una es tierra protegida, terreno "claro" y Lejanía 0, y la Lejanía de toda zona se
  cuenta desde la más cercana (el nivel baja alrededor de cada hoguera);
- cada hoguera tiene todo lo de la fogata: el menú del campamento, 👥 Jugadores con su "N/20" y los personajes;
- los jugadores nuevos nacen en el Claro hasta que se llena, después en la siguiente con lugar;
- quien viaja a una hoguera llena sigue solo hasta la más cercana con lugar; a nadie que ya está se lo mueve;
- 📒 Lugares lista las 9 desde el primer día (sin contar para el tope del 🧭 Explorador) y se puede viajar a cualquiera;
- la meta "explora el Claro" de la historia es la hoguera donde naciste; y todo se lee en inglés.
Archivo: tests/test_nueve_hogueras.py · Módulo: M8 Mundo, M2 Viaje · Prueba: engine/world/mapgen.py (bonfire_layout,
configure_bonfires, nearest_bonfire, lejania), engine/service/game.py (_bonfire_with_room, _bonfire_count, la creación,
_arrive, _places_view, _zone_name), engine/service/gremio.py (_players_view), engine/service/story.py (_in_claro, _goal_zone).
"""

from conftest import make_hero
from engine.world import mapgen
from test_camps import place

NINE = [(0, 0), (0, 12), (12, 0), (0, -12), (-12, 0), (12, 12), (12, -12), (-12, -12), (-12, 12)]


def text(view):
    return "\n".join([view.notice or ""] + view.body)


def small_cap(service, cap=2):
    service.content.balance["bonfire"]["cap"] = cap


def new_hero(service, n):
    account = f"test:{n}"
    make_hero(service, account, f"Heroe{chr(64 + n)}")
    service.act(account, "home")                                   # pressing a button: present at its bonfire
    return service._load(account)


def test_nine_bonfires_protected_and_lejania_from_the_nearest(service):
    assert list(mapgen.BONFIRES) == NINE
    for x, y in NINE:
        zone = service._zone(x, y)
        assert zone.biome == "claro" and zone.lejania == 0 and service._territory(x, y) == {"claro": True}
    assert service._zone(11, 0).lejania == 1 and service._zone(6, 6).lejania == 6 and service._zone(30, 0).lejania == 18
    assert service._zone(11, 0).level < service._zone(6, 0).level            # near the East campfire it is easier again
    assert service._zone_name(service._zone(0, 12)) == "Fogata del Norte"
    assert service._zone_name(service._zone(-12, -12)) == "Fogata del Suroeste"


def test_every_bonfire_has_the_camp_menu_players_and_characters(service):
    make_hero(service)
    place(service, "test:1", 12, -12, known=["0:0", "12:-12"])
    hub = service.act("test:1", "claro")
    assert hub.kind == "claro" and {"players", "trainer", "shop", "inn", "board"} <= {a.id for a in hub.actions}
    players = service.act("test:1", "players")
    assert players.kind == "players" and "1/20" in text(players)
    assert service._in_claro(service._load("test:1"))                       # the characters are here too
    assert "Fogata del Sureste" in text(service.act("test:1", "home"))


def test_new_players_fill_the_claro_first_then_the_next_with_room(service):
    small_cap(service)
    homes = [tuple(new_hero(service, n).home) for n in range(1, 6)]
    assert homes == [(0, 0), (0, 0), (0, 12), (0, 12), (12, 0)]
    hero = service._load("test:3")
    assert (hero.x, hero.y) == (0, 12) and "0:12" in hero.known


def test_a_full_bonfire_sends_arrivals_on_and_moves_nobody(service, clock):
    small_cap(service)
    for n in range(1, 5):
        new_hero(service, n)                                          # 1, 2 at the Claro; 3, 4 at the North campfire
    service.act("test:1", "goto:0:12")
    rerouted = None
    for _ in range(40):
        clock.advance(60)
        for other in ("test:2", "test:3", "test:4"):
            service.act(other, "home")
        view = service.act("test:1", "home")
        if view.notice and "llena" in view.notice:
            rerouted = view.notice
        if not service._load("test:1").activity:
            break
    assert rerouted and "Fogata del Norte (0, 12)" in rerouted and "El Claro (0, 0)" in rerouted
    assert (service._load("test:1").x, service._load("test:1").y) == (0, 0)
    assert all((service._load(a).x, service._load(a).y) == (0, 12) for a in ("test:3", "test:4"))   # nobody moved


def test_places_lists_every_bonfire_from_the_first_day(service):
    make_hero(service)
    places = text(service.act("test:1", "plc:fire"))                      # D-301: 📒 Lugares → 🔥 Fogatas
    for name in ("Fogata del Norte", "Fogata del Este", "Fogata del Sur", "Fogata del Oeste", "Fogata del Noreste",
                 "Fogata del Sureste", "Fogata del Suroeste", "Fogata del Noroeste"):
        assert name in places, name
    assert "Rango 10" not in places and "rango 10" not in places          # the bonfires do not use up the 3 places
    assert service.act("test:1", "goto:12:12").kind == "activity"          # never visited, still a trip
    assert service._load("test:1").activity["goal"] == [12, 12]


def test_the_story_claro_goal_is_your_own_bonfire(service):
    small_cap(service, 1)
    new_hero(service, 1)
    hero = new_hero(service, 2)
    assert hero.home == [0, 12]
    assert service._goal_zone(hero, {"kind": "explored", "zone": [0, 0], "pct": 100}) == (0, 12)
    assert service._goal_zone(service._load("test:1"), {"kind": "explored", "zone": [0, 0]}) == (0, 0)
    assert service._goal_zone(hero, {"kind": "explored", "zone": [3, 4]}) == (3, 4)


def test_bonfires_read_well_in_english(service):
    from test_idiomas import english_hero
    english_hero(service)
    places = text(service.act("test:1", "plc:fire"))
    assert "North Campfire (0, 12)" in places and "Southwest Campfire" in places
    assert not service.texts.fallbacks.get("en")
