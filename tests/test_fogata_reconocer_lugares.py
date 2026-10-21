"""🔥 Fogatas, 🔭 Reconocer with what the 🧭 Explorador sees, your territory grey and ✨ nodes in 📒 Lugares (0.48, D-311, D-324).

[ES] Pruebas de lo que decidió el dueño el 20-oct-2026 (D-311, partes 1, 2, 3 y 6; cómo se aplicó: D-324, provisional):
- (1) E-205: las hogueras se llaman 🔥 Fogata en todo el juego y "campamento" queda solo para el de los jugadores: ningún texto
  en español dice "hoguera" ni llama "campamento" a una fogata; en inglés, "campfire" (nunca "bonfire"); la cabecera de 📍 Zona,
  la leyenda del 🗺️ Mapa y el título del menú de la fogata dicen 🔥 Fogata y el nombre de cada una;
- (2) E-207: lo que el Explorador veía en el mapa (los 👹 campamentos enemigos lejanos, su tiempo y su fuerza) sale en
  🔭 Reconocer como lista de lo que su rango deja ver (1 zona, 3 desde el 25, todo el mapa desde el 50; la fuerza desde el 75),
  con nombre, distancia y ⏱️ tiempo, y el código /rcN en lo que se puede reconocer ahora; el 🗺️ Mapa sigue sin dibujarlos;
- (3) E-177: las zonas de tu propio campamento se ven grises hasta investigarlas al 50 %, como cualquier otra (el 🏕️ del
  centro sigue su regla);
- (6) E-203 y E-206: 📒 Lugares suma ✨ Nodos con los nodos de recursos que encontraste (zona, recurso y código /irN) y se viaja
  solo a lo que ya visitaste.
Archivo: tests/test_fogata_reconocer_lugares.py · Módulo: M8 Mundo y mapa · Prueba: engine/service/game.py (_biome_label,
_claro_view, _fog_cell, _map_view, _recon_view, _recon_entries, _recon_line, _recon_code, _recon_hint_lines, RECON_CODE_RE,
_important_places, _places_view, _places_kind_view, _place_confirm_view) y los textos de content/locales (es y en).
"""

import re

from conftest import make_hero
from engine.service import GameService
from test_camps import old_camp_at, place
from test_enemy_camps import camp_zone, rank_xp
from test_idiomas import english_hero
from test_nodos_y_terrenos import node_near
from test_reconocimiento import free_zone_next_to


def flatten(node, prefix=""):
    """Dotted key -> what the player reads (placeholders such as {bonfires} taken out: they are not words of the text)."""
    if isinstance(node, dict):
        out = {}
        for key, value in node.items():
            out.update(flatten(value, f"{prefix}.{key}" if prefix else str(key)))
        return out
    if isinstance(node, list):
        return {f"{prefix}[{i}]": re.sub(r"\{[^{}]*\}", "", str(v)) for i, v in enumerate(node)}
    return {prefix: re.sub(r"\{[^{}]*\}", "", str(node))}


def grid(service, view):
    """The map's rows: always its last 2 × radius + 1 lines (the legends above can grow)."""
    radius = service.content.balance["map_view"]["radius"]
    return view.body[-(2 * radius + 1):]


def cell(service, hero_xy, view, x, y):
    radius = service.content.balance["map_view"]["radius"]
    hx, hy = hero_xy
    return re.findall(r".️?", grid(service, view)[hy + radius - y])[x - hx + radius]


def explorer(service, x, y, rank, account="test:1", **extra):
    """A hero (made if needed) standing at (x, y) with that 🧭 Explorador rank, full energy, tutorial done."""
    if service._load(account) is None:
        make_hero(service, account)
    profs = {"explorador": rank_xp(service, rank)} if rank > 1 else {}
    data = {"energy": 50, "tutorial": len(service.content.balance["tutorial"]["steps"]), "professions": profs,
            "known": ["0:0", f"{x}:{y}"]}
    data.update(extra)
    place(service, account, x, y, **data)
    return service._load(account)


def recon_line(view, x, y):
    return next((line for line in view.body if f"({x}, {y})" in line), None)


# ---------------------------------------------------------------- (1) 🔥 Fogata, not "hoguera" nor "campamento"

def test_no_spanish_text_says_hoguera_and_no_english_text_says_bonfire(content):
    spanish = flatten(content.locales["es"])
    assert not [key for key, value in spanish.items() if "hoguera" in value.lower()]
    for old in ("campamento base", "campamento de inicio", "campamento del claro", "campamento (la"):
        assert not [key for key, value in spanish.items() if old in value.lower()], old
    english = flatten(content.locales["en"])
    assert not [key for key, value in english.items() if "bonfire" in value.lower()]
    assert not [key for key, value in english.items() if re.search(r"\b(base|starting) camp\b", value.lower())]


def test_the_bonfires_are_called_fogata_on_every_screen(service):
    make_hero(service)
    hub = service.act("test:1", "claro")
    assert hub.kind == "claro" and hub.title == "🔥 El Claro"
    assert "campamento" not in hub.body[0].lower()
    assert service.act("test:1", "home").body[0] == "El Claro — 🔥 Fogata"
    legend = service.act("test:1", "map").body[1]
    assert "🔥 Fogata" in legend and "Campamento" not in legend
    place(service, "test:1", 0, 12)                                     # the Fogata del Norte (D-277)
    hub = service.act("test:1", "claro")
    assert hub.kind == "claro" and hub.title == "🔥 Fogata del Norte"
    assert service.act("test:1", "home").body[0] == "Fogata del Norte — 🔥 Fogata"
    assert not service.texts.missing


def test_the_bonfires_read_campfire_in_english(service):
    english_hero(service)
    hub = service.act("test:1", "claro")
    assert hub.title == "🔥 The Clearing"
    assert "🔥 Campfire" in service.act("test:1", "home").body[0]
    assert "🔥 Campfire" in service.act("test:1", "map").body[1]
    assert not service.texts.fallbacks.get("en")


# ---------------------------------------------------------------- (2) 🔭 Reconocer lists what your 🧭 rank lets you see

def test_recon_lists_the_enemy_camps_your_rank_lets_you_see(service):
    service.content.balance["recon"]["listed"] = 50                       # every line, whatever else is near (test only)
    make_hero(service)
    cx, cy = camp_zone(service)
    name = service._zone_name(service._zone(cx, cy))
    explorer(service, cx + 5, cy, 25)                                      # 5 zones away: past rank 25's 3 zones
    assert recon_line(service.act("test:1", "recon"), cx, cy) is None
    explorer(service, cx + 3, cy, 25)                                      # 3 zones away: seen, out of 🔭 reach (1)
    view = service.act("test:1", "recon")
    line = recon_line(view, cx, cy)
    assert line and line.startswith("👹") and name in line and "a 3 zonas" in line and "⏱️" in line
    assert "/rc" not in line and "💪" not in line                          # no code out of reach; strength from rank 75
    assert f"rcn:{cx}:{cy}" not in [a.id for a in view.actions]
    assert any("Ves campamentos enemigos hasta 3 zonas" in body for body in view.body)
    explorer(service, cx + 5, cy, 50)                                      # rank 50: the whole map
    line = recon_line(service.act("test:1", "recon"), cx, cy)
    assert line and name in line and "/rc" not in line and "💪" not in line
    assert any("todo tu mapa" in body for body in service.act("test:1", "recon").body)
    explorer(service, cx + 5, cy, 75)                                      # rank 75: and its strength
    camp = service._ecamp(cx, cy)
    line = recon_line(service.act("test:1", "recon"), cx, cy)
    assert line and "💪" in line and f"quedan {service._ecamp_left(camp)}" in line
    assert not service.texts.missing


def test_what_you_can_scout_now_has_a_code_that_scouts_it(service):
    make_hero(service)
    cx, cy = camp_zone(service)
    explorer(service, cx + 1, cy, 10)                                      # next door: within 🔭 reach at rank 10
    view = service.act("test:1", "recon")
    line = recon_line(view, cx, cy)
    code = re.search(r"/rc(\d+)$", line)
    assert code and line.startswith("👹") and service._zone_name(service._zone(cx, cy)) in line
    assert f"rcn:{cx}:{cy}" in [a.id for a in view.actions] and len(view.actions) <= 4
    shown = service.store.get("recon_shown", "test:1")["list"]
    assert shown[int(code.group(1)) - 1] == [cx, cy]
    energy = service._load("test:1").energy
    report = service.text("test:1", f"/rc{code.group(1)}")
    assert report.kind == "recon_report"
    assert service._load("test:1").energy == energy - service.content.balance["recon"]["energy"]
    again = service.text("test:1", f"/rc{code.group(1)}")                 # the same code: already scouted today
    assert again.kind == "recon" and "Ya reconociste" in again.notice
    done = recon_line(service.act("test:1", "recon"), cx, cy)
    assert done.startswith("✅ 👹") and "quedan" in done and "/rc" not in done
    wrong = service.text("test:1", "/rc99")
    assert wrong.kind == "recon" and "código" in wrong.notice
    assert service._load("test:1").energy == energy - service.content.balance["recon"]["energy"]
    assert not service.texts.missing


def test_the_recon_code_waits_for_the_rank_and_never_works_in_combat(service):
    make_hero(service)
    cx, cy = camp_zone(service)
    explorer(service, cx + 1, cy, 9)
    assert service.text("test:1", "/rc1").kind == "recon"                  # before rank 10: the short 🔒 reply
    assert service.store.get("recon", "test:1") is None
    hx, hy = free_zone_next_to(service, cx, cy)
    explorer(service, hx, hy, 10)
    assert recon_line(service.act("test:1", "recon"), cx, cy).endswith("/rc1")
    service.act("test:1", "hunt")
    assert service.act("test:1", "prey").kind == "combat"
    assert service.text("test:1", "/rc1").kind == "combat"
    assert service.store.get("recon", "test:1") is None                    # nothing scouted in combat


def test_the_explore_menu_says_when_camps_are_in_sight(service, monkeypatch):
    make_hero(service)
    cx, cy = camp_zone(service)
    explorer(service, cx + 5, cy, 50)
    monkeypatch.setattr(GameService, "_recon_pending", lambda self, hero: [])   # nothing left to scout within reach
    menu = service.act("test:1", "explore_menu")
    assert any("a la vista" in line and "/reconocer" in line for line in menu.body)
    explorer(service, cx + 5, cy, 1)                                       # no 🔭 yet: no line
    assert not any("/reconocer" in line for line in service.act("test:1", "explore_menu").body)


def test_the_map_still_draws_no_enemy_camp(service):
    make_hero(service)
    cx, cy = camp_zone(service)
    explorer(service, cx + 2, cy, 100)
    view = service.act("test:1", "map")
    assert not any("👹" in row for row in grid(service, view))           # E-207: it went to 🔭, not back to the map
    assert [a.id for a in view.actions] == ["places", "explore_menu"]


# ---------------------------------------------------------------- (3) your own territory is grey too

def test_your_own_territory_is_grey_until_50(service):
    make_hero(service)
    old_camp_at(service, "test:1", 6, 0, name="Roca Alta")
    camp = service.store.get("camp", "6:0")
    camp["zones"].append([7, 0])
    service.store.put("camp", "6:0", camp)
    service.store.put("territory", "7:0", {"camp": "6:0"})
    assert service._territory(7, 0)
    blank = next(s["mark"] for s in service.content.balance["map_view"]["fog"]["stages"] if s["id"] == "unknown")
    colour = service.content.biomes[service._zone(7, 0).biome]["color"]
    place(service, "test:1", 8, 0, exploration={"6:0": 100, "7:0": 0})
    view = service.act("test:1", "map")
    assert cell(service, (8, 0), view, 7, 0) == blank                      # your land, never investigated: grey
    assert cell(service, (8, 0), view, 6, 0) == "🏕️"                       # the camp's own icon keeps its rule
    place(service, "test:1", 8, 0, exploration={"6:0": 100, "7:0": 49})
    assert cell(service, (8, 0), service.act("test:1", "map"), 7, 0) == blank
    place(service, "test:1", 8, 0, exploration={"6:0": 100, "7:0": 50})
    assert cell(service, (8, 0), service.act("test:1", "map"), 7, 0) == colour   # at 50 %, its colour


# ---------------------------------------------------------------- (6) 📒 Lugares → ✨ Nodos

def found_node(service):
    """A hero who stood on a node's zone (and found it), now back at the Claro."""
    make_hero(service)
    x, y = node_near(service)
    place(service, "test:1", x, y, known=["0:0", f"{x}:{y}"])
    service.act("test:1", "home")                                          # standing there discovers it (D-184)
    assert f"{x}:{y}" in service._node_found(service._load("test:1"))
    place(service, "test:1", 0, 0)
    return x, y


def test_places_lists_the_nodes_you_found_with_zone_resource_and_code(service):
    make_hero(service)
    assert "plc:node" not in [a.id for a in service.act("test:1", "places").actions]   # nothing found yet
    x, y = found_node(service)
    main = service._node_main(x, y)
    menu = service.act("test:1", "places")
    button = next(a for a in menu.actions if a.id == "plc:node")
    assert button.label == "✨ Nodos (1)" and [a.id for a in menu.actions][-1] == "map"
    view = service.act("test:1", "plc:node")
    assert view.kind == "places_kind" and view.title == "📒 Lugares · ✨ Nodos"
    line = next(line for line in view.body if line.startswith("1. "))
    assert service._item_label(main) in line and service._zone_name(service._zone(x, y)) in line
    assert f"({x}, {y})" in line and line.endswith("/ir1")
    assert f"goask:{x}:{y}" in [a.id for a in view.actions] and len(view.actions) <= 4
    confirm = service.text("test:1", "/ir1")
    assert confirm.kind == "place_confirm" and [a.id for a in confirm.actions] == [f"goto:{x}:{y}", "plc:node"]
    service.act("test:1", f"goto:{x}:{y}")
    assert service._load("test:1").activity["kind"] == "travel"
    assert not service.texts.missing


def test_a_node_you_never_stood_on_is_not_listed(service):
    make_hero(service)
    x, y = node_near(service)
    service.store.put("nodes", "test:1", {"found": [f"{x}:{y}"]})         # found, but not a zone the hero remembers
    place(service, "test:1", 0, 0, known=["0:0"])
    assert "plc:node" not in [a.id for a in service.act("test:1", "places").actions]
    service.act("test:1", f"goto:{x}:{y}")                                 # D-222: "Moverte allá" only where you have been
    assert not service._load("test:1").activity


def test_a_zone_in_two_lists_goes_back_to_the_one_you_saw(service, monkeypatch):
    make_hero(service)
    two = [(60.0, 4, 2, "🏕️", "Roca", "camps"), (60.0, 4, 2, "✨", "🪵 Madera en Roca", "node")]
    monkeypatch.setattr(GameService, "_important_places", lambda self, hero: list(two))
    service.store.put("places_shown", "test:1", {"list": [[4, 2]], "kind": "node"})
    assert service.act("test:1", "goask:4:2").actions[-1].id == "plc:node"
    service.store.put("places_shown", "test:1", {"list": [[4, 2]], "kind": "camps"})
    assert service.act("test:1", "goask:4:2").actions[-1].id == "plc:camps"


def test_nodes_read_well_in_english(service):
    english_hero(service)
    x, y = node_near(service)
    place(service, "test:1", x, y, known=["0:0", f"{x}:{y}"])
    service.act("test:1", "home")
    place(service, "test:1", 0, 0)
    view = service.act("test:1", "plc:node")
    assert view.title == "📒 Places · ✨ Nodes" and any(" at " in line and "/go1" in line for line in view.body)
    assert not service.texts.fallbacks.get("en")
