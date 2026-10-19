"""What one guild member explores, the whole guild knows: zones, resources, the map and founding (D-282).

[ES] Pruebas de lo que pidió el dueño el 18-oct-2026 ("organiza la información de las locaciones cuando están en el gremio,
que te permita conocer la información de los recursos que hay en la zona, para no tener que investigar doble la zona para
los del gremio únicamente"), con sus respuestas: vale para todo menos la experiencia; lo comparten el gremio y, después,
el campamento; y hay una pantalla 🗺️ Zonas del gremio:
- lo que explora un compañero se ve en 📍 Zona (recursos, %) y en el 🗺️ Mapa (color), sin explorar uno mismo;
- vale para fundar (la zona al 100 % y las vecinas conocidas);
- quien explora igual gana su experiencia (su % propio sigue siendo el suyo);
- los del campamento también lo comparten; alguien de afuera no ve nada;
- 🗺️ Zonas del gremio ordena las zonas (la más cercana primero), busca por recurso y el código /z1 arma el camino.
Archivo: tests/test_conocimiento_del_gremio.py · Módulo: M15 Social, M8 Mundo · Prueba: engine/service/gremio.py (_mates,
_mates_knowledge, _known_pct, _knows_zone, _gremio_zones_view, _zone_code), engine/service/game.py (_known_resources,
_resources_lines, _fog_cell, _known_terrains, _camp_requirements).
"""

from conftest import make_hero
from test_camps import old_camp_at, place
from test_gremio_desde_el_inicio import join, new_gremio


def text(view):
    return "\n".join([view.notice or ""] + view.body)


def guild_of_two(service):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    gid, _ = new_gremio(service)
    join(service, gid, "test:2")
    return gid


def test_a_mate_s_exploration_shows_in_zone_and_map_without_exploring(service):
    guild_of_two(service)
    place(service, "test:2", 3, 0, known=["0:0", "3:0"], exploration={"3:0": 100})
    place(service, "test:1", 3, 0, known=["0:0", "3:0"])
    hero = service._load("test:1")
    assert hero.exploration.get("3:0", 0) == 0                                   # its own % did not move
    assert service._known_pct(hero, 3, 0) == 100
    zone = text(service.act("test:1", "home"))
    assert "Explorada al 100 %" in zone
    assert service._fog_cell(service._load("test:1"), 3, 0) == service.content.biomes[service._zone(3, 0).biome].get(
        "color", service.content.biomes[service._zone(3, 0).biome]["emoji"])       # the map shows its colour


def test_it_counts_for_founding_but_experience_stays_with_who_explores(service, clock):
    guild_of_two(service)
    around = {"3:0": 100}
    place(service, "test:2", 3, 0, known=["0:0", "3:0", "2:0", "4:0", "3:1", "3:-1"], exploration=around)
    place(service, "test:1", 3, 0, known=["0:0", "3:0"])
    reqs = dict((text, ok) for text, ok in service._camp_requirements(service._load("test:1")))
    explored = next(ok for text, ok in reqs.items() if "100 %" in text or "explorado" in text)
    neighbours = next(ok for text, ok in reqs.items() if "vecinas" in text)
    assert explored and neighbours
    service.content.balance["explore"]["encounter"] = 0.0                       # no fight in the way of the check
    before = service._load("test:1").xp
    service.act("test:1", "do:explore:1")                                         # it can still explore it itself
    for _ in range(30):
        clock.advance(60)
        service.act("test:1", "home")
    hero = service._load("test:1")
    assert 0 < hero.exploration.get("3:0", 0) < 100 and hero.xp > before          # its own %, its own experience
    assert service._load("test:2").exploration["3:0"] == 100


def test_camp_members_share_and_outsiders_see_nothing(service):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    make_hero(service, "test:3", "Cira")
    old_camp_at(service, "test:1", 6, 0, name="Roca Alta")
    camp = service.store.get("camp", "6:0")
    camp["members"].append("test:2")
    service.store.put("camp", "6:0", camp)
    place(service, "test:2", 6, 0, camp="6:0", exploration={"8:0": 60})
    assert service._known_pct(service._load("test:1"), 8, 0) == 60                # a camp mate
    assert service._known_pct(service._load("test:3"), 8, 0) == 0                 # not in it: nothing
    assert "gzones" in [a.id for a in service.act("test:1", "guild").actions]
    assert "gremio" in service.act("test:3", "gzones").notice.lower()


def test_guild_zones_lists_nearest_first_searches_and_codes(service):
    guild_of_two(service)
    place(service, "test:2", 5, 0, known=["0:0", "5:0", "2:0"], exploration={"5:0": 100, "2:0": 40})
    view = service.act("test:1", "gzones")
    assert view.kind == "gremio_zones" and view.expects_text
    lines = [line for line in view.body if "/z" in line and line[:2] in ("1.", "2.")]
    assert "(2, 0)" in lines[0] and "(5, 0)" in lines[1] and "Bram" in lines[0]
    item = service.content.items[service._known_resources(service._load("test:1"), 5, 0)[-1]]
    word = service.texts.t(item["name_key"]).split()[0]
    found = service.text("test:1", word.lower())
    assert found.kind == "gremio_zones" and any("(5, 0)" in line for line in found.body)
    service.act("test:1", "gzones")
    walk = service.text("test:1", "/z1")
    assert walk.kind == "walk" and service.store.get("walk", "test:1")["steps"] == ["e", "e"]
    assert "gzones" in [a.id for a in service.act("test:1", "guild").actions]


def test_guild_zones_read_well_in_english(service):
    from test_idiomas import english_hero
    english_hero(service)
    make_hero(service, "test:2", "Bram")
    gid, _ = new_gremio(service)
    join(service, gid, "test:2")
    place(service, "test:2", 2, 0, exploration={"2:0": 40})
    view = service.act("test:1", "gzones")
    assert view.title == "🗺️ Guild zones" and "(2, 0)" in text(view)
    assert not service.texts.fallbacks.get("en")


def test_who_leaves_keeps_only_what_it_explored(service):
    # [ES] D-283 (pedido del dueño): si la persona sale del gremio, solo se mantiene con la información que conoce
    guild_of_two(service)
    place(service, "test:2", 3, 0, exploration={"3:0": 100, "4:0": 60})
    place(service, "test:1", 0, 0, exploration={"5:0": 40})
    assert service._known_pct(service._load("test:1"), 3, 0) == 100
    service.act("test:2", "gleave!")                                              # Bram leaves the guild
    leaver = service._load("test:2")
    assert service._mates(leaver) == [] and service._known_pct(leaver, 3, 0) == 100   # its own exploration stays
    assert service._known_pct(leaver, 5, 0) == 0                                  # what the others knew is gone for it
    assert service._known_pct(service._load("test:1"), 3, 0) == 0                 # and the one left loses what it gave


def test_guild_mates_are_drawn_on_the_map(service):
    guild_of_two(service)
    make_hero(service, "test:3", "Cira")
    place(service, "test:2", 2, 1)
    place(service, "test:3", -1, 0)                                               # not in the guild: not drawn
    view = service.act("test:1", "map")
    mark = "🏰"                                                                   # D-286: Bram's class (🏰 Guerrero)
    assert "🏰 Bram · Guerrero · (2, 1)" in text(view) and "Cira" not in text(view)
    grid = [line for line in view.body if " " not in line]                       # the map's rows (the legend has spaces)
    assert sum(line.count("🧍") for line in grid) == 1                            # you
    assert sum(line.count(mark) for line in grid) == 1                            # Bram; Cira is not in the guild
