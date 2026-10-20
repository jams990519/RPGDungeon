"""⚔️ Armería: the guild's shared gear chest (D-290, 0.39): leave and take pieces with codes, from anywhere, with a record.

[ES] Pruebas de lo que pidió y respondió el dueño el 19-oct-2026 ("tienes que poner un botón de armamento"; respuesta: una
armería del gremio, un cofre de equipo compartido: los miembros dejan armas y armaduras que no usan y otros las toman, con
registro de quién dejó o tomó qué):
- ⚔️ Armería está en 🛡️ Gremio desde que existe el gremio; se deja con /a1 (equipo de la mochila, nunca lo puesto) y se toma
  con /t1, desde cualquier lugar; cualquiera del gremio toma;
- cada pieza conserva su ✨ encantamiento y su ✒️ firma; si quien la toma ya lleva una igual distinta, no se la lleva;
- caben armory.slots piezas; la pantalla muestra cuántas hay ("🗃️ 1/30": desde D-302 solo ahí, no en 🛡️ Gremio) y los
  últimos movimientos (quién dejó o tomó qué);
- al fundar, la armería se muda al campamento con todo; si el último miembro disuelve el gremio, las piezas vuelven a él;
- sin gremio, explica; y se lee en inglés.
Archivo: tests/test_armeria.py · Módulo: M15 Social · Prueba: engine/service/gremio.py (_armory_view, _armory_in_code,
_armory_out_code, _armory_empty_to, _finish_founding), engine/service/game.py (text(): ARMORY_IN_RE y ARMORY_OUT_RE).
"""

from conftest import make_hero
from test_camps import place
from test_gremio_desde_el_inicio import fund_cost, join, keep_present, new_gremio, site

MASTER = "artesano_espada_2_obra"


def ids(view):
    return [a.id for a in view.actions]


def text(view):
    return "\n".join([view.notice or ""] + view.body)


def set_hero(service, account, **values):
    hero = service._load(account)
    for key, value in values.items():
        setattr(hero, key, value)
    service._save(hero)


def guild_of_two(service):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    gid, _ = new_gremio(service)
    join(service, gid, "test:2")
    service.tick()
    return gid


def test_leave_and_take_with_codes_from_anywhere_with_a_record(service):
    gid = guild_of_two(service)
    worn = dict(service._load("test:1").gear)
    set_hero(service, "test:1", backpack={"espada_2": 2, "madera": 3}, x=9, y=-4,
             gear_enchants={"espada_2": {"id": "filo", "value": 0.02}})
    assert "garm" in ids(service.act("test:1", "guild"))
    view = service.act("test:1", "garm")
    assert view.kind == "armory" and ids(view) == ["guild"] and "0/30" in text(view)
    mine = [line for line in view.body if line.startswith("/a")]
    assert len(mine) == 1 and "Espada" in mine[0] and "×2" in mine[0]          # only the backpack: never what is worn
    assert worn and service._load("test:1").gear == worn                        # the worn pieces stay worn
    view = service.text("test:1", "/a1")
    assert "Dejaste" in view.notice and service._load("test:1").backpack["espada_2"] == 1
    assert service._load("test:1").gear_enchants["espada_2"]["id"] == "filo"   # one copy left: it keeps its ✨
    service.text("test:1", "/a01")                                               # /a01 works too
    hero = service._load("test:1")
    assert "espada_2" not in hero.backpack and "espada_2" not in hero.gear_enchants   # the ✨ travelled with the piece
    record = service.store.get("armory", gid)
    assert [e["item"] for e in record["items"]] == ["espada_2", "espada_2"] and record["items"][0]["enchant"]["id"] == "filo"
    view = service.act("test:2", "garm")                                         # anyone in the guild takes
    assert any(line.startswith("/t1 ") and "dejó Lyra" in line for line in view.body)
    view = service.text("test:2", "/t1")
    bram = service._load("test:2")
    assert "Tomaste" in view.notice and bram.backpack["espada_2"] == 1 and bram.gear_enchants["espada_2"]["id"] == "filo"
    assert "espada_2" in bram.gear_new
    view = service.text("test:2", "/t1")                                         # same piece, same ✨: it goes with it
    assert service._load("test:2").backpack["espada_2"] == 2 and not service.store.get("armory", gid)["items"]
    log = [line for line in view.body if line.startswith(("📥", "📤"))]
    assert log[0].startswith("📤 Bram tomó") and log[-1].startswith("📥 Lyra dejó") and len(log) == 4
    assert "ya no está" in service.text("test:2", "/t1").notice
    assert "no está en tu lista" in service.text("test:2", "/a9").notice


def test_signatures_travel_conflicts_wait_and_the_armory_has_a_cap(service):
    gid = guild_of_two(service)
    set_hero(service, "test:1", backpack={MASTER: 1, "espada_2": 1}, gear_signatures={MASTER: "Lyra"},
             gear_enchants={"espada_2": {"id": "filo", "value": 0.03}})
    service.act("test:1", "garm")
    lines = [line for line in service.act("test:1", "garm").body if line.startswith("/a")]
    n_master = next(i for i, line in enumerate(lines, 1) if "✒️" in line)
    service.text("test:1", f"/a{n_master}")
    assert MASTER not in service._load("test:1").gear_signatures
    view = service.act("test:2", "garm")
    assert any("(✒️ Lyra)" in line for line in view.body)
    service.text("test:2", "/t1")
    assert service._load("test:2").gear_signatures[MASTER] == "Lyra"            # the signature is never lost
    service.content.balance["armory"]["slots"] = 1
    service.act("test:1", "garm")
    service.text("test:1", "/a1")                                                # the enchanted sword goes in
    assert len(service.store.get("armory", gid)["items"]) == 1
    set_hero(service, "test:2", backpack={"espada_2": 1})                        # Bram's own sword, not enchanted
    service.act("test:2", "garm")
    assert "llena" in service.text("test:2", "/a1").notice                       # 1 of 1: full
    view = service.text("test:2", "/t1")
    assert "otro encantamiento o firma" in view.notice and len(service.store.get("armory", gid)["items"]) == 1
    assert service._load("test:2").backpack == {"espada_2": 1}


def test_the_armory_moves_with_the_founding_and_comes_back_if_the_guild_dissolves(service, clock):
    gid = guild_of_two(service)
    set_hero(service, "test:1", backpack={"espada_2": 1})
    service.act("test:1", "garm")
    service.text("test:1", "/a1")
    fund_cost(service, gid)
    site(service, "test:1", 6, 0)
    place(service, "test:2", 6, 0)
    service.act("test:2", "home")
    service.act("test:1", "found")
    keep_present(service, clock, ["test:1", "test:2"], 60)
    assert service.store.get("camp", "6:0") and service.store.get("armory", gid) is None
    assert [e["item"] for e in service.store.get("armory", "6:0")["items"]] == ["espada_2"]   # moved, nothing lost
    service.act("test:2", f"gcamp:{gid}:y")
    view = service.act("test:2", "guild")
    assert "garm" in ids(view) and not any("Armería" in line for line in view.body)   # D-302: the count is on its screen
    assert "🗃️ 1/30 piezas" in service.act("test:2", "garm").body
    assert "Tomaste" in service.text("test:2", "/t1").notice and service._load("test:2").backpack["espada_2"] == 1
    make_hero(service, "test:3", "Cora")                                         # a lone guild that dissolves
    new_gremio(service, "test:3", "Osos Pardos")
    set_hero(service, "test:3", backpack={"espada_2": 1})
    service.act("test:3", "garm")
    service.text("test:3", "/a1")
    assert "espada_2" not in service._load("test:3").backpack
    service.act("test:3", "gleave")
    view = service.act("test:3", "gleave!")
    assert service._load("test:3").backpack == {"espada_2": 1} and "armería" in view.notice


def test_without_a_guild_it_explains_and_it_reads_well_in_english(service):
    from test_idiomas import english_hero
    make_hero(service, "test:1", "Lyra")
    view = service.act("test:1", "garm")
    assert view.kind == "gremio_none" and "armería es de un gremio" in view.notice
    assert "armería es de un gremio" in service.text("test:1", "/t1").notice
    english_hero(service, "test:2", "Bram")
    new_gremio(service, "test:2", "Grey Wolves")
    set_hero(service, "test:2", backpack={"espada_2": 1})
    view = service.act("test:2", "garm")
    assert view.title == "⚔️ Guild armory" and "[" not in text(view)
    assert "You left" in service.text("test:2", "/a1").notice
    assert "[" not in text(service.act("test:2", "guild"))
    assert not service.texts.fallbacks.get("en"), sorted(service.texts.fallbacks.get("en", []))[:20]
