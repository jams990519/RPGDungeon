"""🔎 The resource finder: where a resource is, in zones investigated to 50 % or more (D-296).

[ES] Pruebas de lo que pidió el dueño el 19-oct-2026: "en el apartado del campamento y del gremio vas a poner un buscador de
recursos… si busco madera, únicamente para zonas investigadas a más del 50 %, te va a decir en qué zona está para que puedas
ir a farmearlo más fácil":
- escribir el recurso (con o sin tildes, mayúsculas, en español o en inglés) lista las zonas investigadas al 50 % o más donde
  ya se sabe que está, la más cercana primero, con cuánto queda; una zona al 40 % no sale;
- vale lo que exploró tu gremio (D-282) y, sin gremio, lo que exploraste tú;
- /buscar madera funciona desde cualquier lugar y el código /z1 arma el camino en 🔗 Moverte;
- un recurso agotado se marca ⏳; una palabra que no es un recurso dice cómo escribirlo;
- el botón 🔎 Buscar recursos está en 🛡️ Gremio (con y sin gremio) y en 🏰 Gestionar del campamento; se lee bien en inglés;
- D-303 (0.40.1: la 🪵 madera en todas las zonas): entre las cercanas van primero las ricas (gremio.search_rich_penalty):
  un bosque a una zona más sale antes que una zona con madera pobre.
Archivo: tests/test_buscador_de_recursos.py · Módulo: M15 Social, M8 Mundo · Prueba: engine/service/gremio.py
(_resource_search_view, _resource_matches, _gremio_zones_view), engine/service/game.py (text: /buscar, _camp_member_actions).
"""

from conftest import make_hero
from engine.world import mapgen
from engine.world.resources import wood_first
from test_camps import old_camp_at, place
from test_gremio_desde_el_inicio import join, new_gremio


def text(view):
    return "\n".join([view.notice or ""] + view.body)


def wood_zones(service, n=2):
    """Zones near the Claro where wood is among the first 3 resources (known from 40 %), nearest first."""
    found = []
    for d in range(1, 12):
        for x in range(-d, d + 1):
            for y in range(-d, d + 1):
                if max(abs(x), abs(y)) != d or (x, y) == (0, 0):
                    continue
                if "madera" in list(service._zone_resources(x, y))[:3] and not service._zone(x, y).biome == "claro":
                    found.append((x, y))
        if len(found) >= n:
            return found[:n]
    return found


def test_alone_it_lists_zones_known_to_fifty_percent_with_the_resource(service):
    make_hero(service)
    (ax, ay), (bx, by) = wood_zones(service)
    place(service, "test:1", 0, 0, exploration={f"{ax}:{ay}": 60, f"{bx}:{by}": 40})
    view = service.text("test:1", "/buscar MADERA")
    body = text(view)
    assert view.kind == "gremio_zones" and view.title == "🔎 Buscar recursos" and "50 %" in body
    assert f"({ax}, {ay})" in body and f"({bx}, {by})" not in body              # 40 % does not count
    assert "/z1" in body and "queda" in body
    walk = service.text("test:1", "/z1")
    assert walk.kind == "walk" and service.store.get("walk", "test:1")["steps"]


def test_accents_english_names_and_unknown_words(service):
    make_hero(service)
    (ax, ay), _ = wood_zones(service)
    place(service, "test:1", 0, 0, exploration={f"{ax}:{ay}": 100})
    service.act("test:1", "gzones")
    assert f"({ax}, {ay})" in text(service.text("test:1", "wood"))              # the English name works too
    assert f"({ax}, {ay})" in text(service.text("test:1", "  Madéra "))
    assert "No conozco un recurso llamado «dragones»" in text(service.text("test:1", "dragones"))


def test_the_guild_s_exploration_counts_and_a_depleted_zone_is_marked(service):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    gid, _ = new_gremio(service)
    join(service, gid, "test:2")
    (ax, ay), _ = wood_zones(service)
    place(service, "test:2", ax, ay, exploration={f"{ax}:{ay}": 80})
    stock = {r: 1.0 for r in service._zone_resources(ax, ay)}
    stock["madera"] = 0.0
    service.store.put("stock", f"{ax}:{ay}", {"levels": stock, "at": service.clock.now()})
    body = text(service.text("test:1", "/buscar madera"))
    assert f"({ax}, {ay})" in body and "⏳ agotado" in body
    assert "gremio" not in (service.text("test:1", "/buscar madera").notice or "")    # with a guild, no "join one" hint


def test_the_button_is_in_the_guild_with_or_without_one_and_in_the_camp(service):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    assert "gzones" in [a.id for a in service.act("test:1", "guild").actions]   # no guild yet
    alone = service.act("test:1", "gzones")
    assert alone.title == "🔎 Buscar recursos" and "gremio" in alone.notice.lower()
    new_gremio(service)
    assert "gzones" in [a.id for a in service.act("test:1", "guild").actions]
    old_camp_at(service, "test:2", 6, 0)
    assert "gzones" in [a.id for a in service.act("test:2", "campmgmt").actions]
    assert "gzones" in [a.id for a in service.act("test:2", "guild").actions]


def test_the_finder_reads_well_in_english(service):
    from test_idiomas import english_hero
    english_hero(service)
    (ax, ay), _ = wood_zones(service)
    place(service, "test:1", 0, 0, exploration={f"{ax}:{ay}": 100})
    view = service.text("test:1", "/search wood")
    assert view.title == "🔎 Find resources" and f"({ax}, {ay})" in text(view) and "left" in text(view)
    assert not service.texts.fallbacks.get("en")


def test_near_and_rich_zones_come_first(service):
    """D-303 (0.40.1): wood is in every zone now, so the finder weighs richness too (gremio.search_rich_penalty): a forest
    (wood 1.0) one zone farther comes before a poor wood zone (0.5 or less). With the penalty at 0, only distance counts."""
    make_hero(service)
    zones = [(x, y) for x in range(-8, 9) for y in range(-8, 9) if not mapgen.is_bonfire(x, y)]
    forest = [z for z in zones if wood_first(*z, service._zone(*z).biome, service.content.balance)]
    poor = [z for z in zones if z not in forest and service._zone_resources(*z).get("madera", 1.0) <= 0.5]
    dist = lambda z: abs(z[0]) + abs(z[1])
    (fx, fy), (px, py) = next((f, p) for f in forest for p in poor if dist(f) == dist(p) + 1)
    place(service, "test:1", 0, 0, exploration={f"{fx}:{fy}": 100, f"{px}:{py}": 100})
    body = text(service.text("test:1", "/buscar madera"))
    assert body.index(f"({fx}, {fy})") < body.index(f"({px}, {py})")            # the rich forest first...
    assert f"a {dist((fx, fy))} zonas" in body                                  # ...showing its real distance
    service.content.balance["gremio"]["search_rich_penalty"] = 0
    body = text(service.text("test:1", "/buscar madera"))
    assert body.index(f"({px}, {py})") < body.index(f"({fx}, {fy})")            # distance alone: the nearer one first
