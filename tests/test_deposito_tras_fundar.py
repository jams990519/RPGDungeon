"""After founding the guild keeps its tools: 💰 Depositar from anywhere into the camp's fund, 📢, the members and the chat (D-291).

[ES] Pruebas de lo que pidió el dueño el 19-oct-2026 ("una vez se crea el gremio no se puede perder el botón de depositar porque
ahí es donde se va a depositar… el chat, qué pasó cuando creé el campamento: esas cositas deben mantenerse"):
- después de fundar, 🛡️ Gremio sigue con 📢 Mensaje, 💰 Depositar, ⚔️ Armería y 🗺️ Zonas, los miembros con su código y los
  📢 mensajes de antes de fundar (pasan al campamento); desde D-302 (0.39.4) detrás de sus botones: 👥 Miembros, 💰 Fondos del
  campamento (con 💰 Depositar) y 📢 Chat (con 📢 Mensaje);
- 💰 Depositar (en 🛡️ Gremio y en 🏘️ Servicios) y /f02 funcionan desde cualquier lugar: lo depositado va al fondo del campamento,
  que alimenta las obras activas (la que se activó primero, antes); lo que sobra queda y se ve; al activar una obra, el fondo le
  da lo que tiene; se anota quién dio qué y no da experiencia (como el fondo de antes de fundar);
- vale también para los campamentos de antes del gremio; y se lee en inglés.
Archivo: tests/test_deposito_tras_fundar.py · Módulo: M14 Construcción y M15 Social · Prueba: engine/service/gremio.py
(_fund_view, _camp_fund_view, _camp_deposit, _fund_code, _finish_founding, _gremio_post) y engine/service/game.py
(_feed_works, _activate_work, _guild_view).
"""

from conftest import make_hero
from test_camps import found_at, old_camp_at, place
from test_gremio_desde_el_inicio import fund_cost, join as gremio_join, keep_present, new_gremio, pushes, site
from test_guilds import join

KEY = "6:0"


def ids(view):
    return [a.id for a in view.actions]


def text(view):
    return "\n".join([view.notice or ""] + view.body)


def set_hero(service, account, **values):
    hero = service._load(account)
    for key, value in values.items():
        setattr(hero, key, value)
    service._save(hero)


def test_the_guild_screen_keeps_its_tools_and_the_messages_of_before(service, clock):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    gid, _ = new_gremio(service)
    gremio_join(service, gid, "test:2")
    service.tick()
    service.text("test:1", "Nos juntamos en el bosque")                     # D-285: loose text, before founding
    fund_cost(service, gid)
    site(service, "test:1", 6, 0)
    place(service, "test:2", 6, 0)
    service.act("test:2", "home")
    service.act("test:1", "found")
    keep_present(service, clock, ["test:1", "test:2"], 60)
    camp = service.store.get("camp", KEY)
    assert camp and camp["messages"][-1]["text"] == "Nos juntamos en el bosque"   # D-291: carried into the camp
    view = service.act("test:1", "guild")
    assert view.kind == "guild" and ids(view)[:5] == ["gmembers", "gfunds", "gchat", "garm", "gzones"]   # D-302: submenus
    assert "gfund" in ids(service.act("test:1", "gfunds"))                  # 💰 Depositar inside 💰 Fondos
    chat = service.act("test:1", "gchat")
    body = text(chat)
    assert "💬 Lyra: Nos juntamos en el bosque" in body and "le llega a todo tu gremio" in body and "gmsg" in ids(chat)
    assert any(line.startswith("/m1 👑 Lyra") for line in service.act("test:1", "gmembers").body)
    service.act("test:2", f"gcamp:{gid}:y")
    service.tick()
    assert service.act("test:1", "gmsg").expects_text                       # 📢 Mensaje after founding
    view = service.text("test:1", "Traigan piedra")
    assert view.kind == "guild_chat" and "enviado" in view.notice and "💬 Lyra: Traigan piedra" in view.body
    got = pushes(service, "test:2", "gremio_message")
    assert got and "💬 Lyra: Traigan piedra" in got[0].body
    lines = [line for line in service.act("test:1", "gmembers").body if line.startswith("/m")]
    assert len(lines) == 2 and "Bram" in lines[1]
    card = service.text("test:1", "/m2")                                     # /m codes after founding
    assert card.kind == "gremio_member" and "Bram" in text(card)


def test_deposits_from_far_away_feed_the_active_works_oldest_first(service):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    found_at(service, "test:1", 6, 0)
    join(service, "test:2")
    service.act("test:1", "upact:fogon")                                     # 20 madera + 15 piedra
    service.act("test:1", "upact:empalizada")                                # 30 madera + 10 fibra
    place(service, "test:2", 9, -4, backpack={"madera": 60, "piedra": 5, "carne": 2}, energy=50)
    service.act("test:2", "do:explore:3")                                    # far away and busy: it still goes in
    service.tick()
    xp, merit = service._load("test:2").xp, service._load("test:2").merit
    view = service.act("test:2", "gfund")
    assert view.kind == "camp_fund" and ids(view) == ["gfunds"] and any(line.startswith("/f01 ") for line in view.body)
    assert not any("Carne" in line and line.startswith("/f") for line in view.body)     # food is for the pantry
    assert any(line.startswith("1.") and "Fogón" in line for line in view.body)       # the order the fund fills them
    view = service.text("test:2", "/f01")
    assert "Depositaste" in view.notice and "El fondo puso" in view.notice
    record = service._upgrades(KEY)
    assert record["works"]["fogon"] == {"madera": 20} and record["works"]["empalizada"] == {"madera": 30}
    assert record["fund"] == {} and record["levelup"]["given"] == {"madera": 10}    # D-313: the rest fills ⏫ Siguiente nivel
    service.text("test:2", "/f02")
    assert service._upgrades(KEY)["works"]["fogon"] == {"madera": 20, "piedra": 5}
    assert service._upgrades(KEY)["gave"]["test:2"] == {"madera": 60, "piedra": 5}       # who gave what
    assert (service._load("test:2").xp, service._load("test:2").merit) == (xp, merit)    # the fund gives no experience
    set_hero(service, "test:2", backpack={"piedra": 12})
    view = service.text("test:2", "/f02")
    record = service._upgrades(KEY)
    assert "fogon" in record["building"] and "fogon" not in record["active"] and "Materiales completos" in view.notice
    assert record["fund"] == {} and record["levelup"]["given"] == {"madera": 10, "piedra": 2}   # D-313: the rest, to the level
    news = pushes(service, "test:1", "camp_news")
    assert news and "Fogón" in news[-1].body[0]
    assert any("Bram" in line and "×60" in line for line in service.act("test:1", "gfund").body)


def test_deposit_in_servicios_waits_for_a_work_and_an_activation_takes_it(service):
    make_hero(service, "test:1", "Lyra")
    found_at(service, "test:1", 6, 0)
    assert ids(service.act("test:1", "upsvc"))[-2:] == ["gfund:svc", "claro"]
    set_hero(service, "test:1", backpack={"madera": 25, "fibra": 4})
    data = service._upgrades(KEY)                                           # D-313: the level's materials are in already,
    data["levelup"] = {"to": 2, "given": {"madera": 30, "piedra": 20, "fibra": 10}, "chests": 0}   # so the deposit waits
    service.store.put("upgrades", KEY, data)
    view = service.act("test:1", "gfund:svc")
    assert view.kind == "camp_fund" and ids(view) == ["upsvc"]               # ↩️ back to 🏘️ Servicios
    view = service.text("test:1", "/f01")
    assert "No hay obras activas" in text(view) and service._upgrades(KEY)["fund"] == {"madera": 25}
    # [ES] D-317 (0.45): el 🪚 Aserradero ya casi no pide madera (pide tablones); la 🪵 Empalizada sigue pidiendo 30
    view = service.act("test:1", "upact:empalizada")                        # ▶️ the fund gives it what it has
    assert "El fondo puso" in view.notice and service._upgrades(KEY)["works"]["empalizada"] == {"madera": 25}
    assert service._upgrades(KEY)["fund"] == {}


def test_old_camps_without_a_guild_deposit_too_and_it_reads_well_in_english(service):
    from test_idiomas import english_hero
    english_hero(service, "test:1", "Lyra")
    old_camp_at(service, "test:1", 6, 0, name="Grey Rock")                  # before D-269: no guild record
    service.act("test:1", "upact:fogon")
    set_hero(service, "test:1", backpack={"madera": 5}, x=0, y=0)
    view = service.text("test:1", "/f01")
    assert view.kind == "camp_fund" and "You deposited" in view.notice
    assert service._upgrades(KEY)["works"]["fogon"] == {"madera": 5}
    for action in ("gfund", "guild", "garm", "gmembers", "gfunds", "gchat", "campinfo"):
        assert "[" not in text(service.act("test:1", action)), action
    assert not service.texts.fallbacks.get("en"), sorted(service.texts.fallbacks.get("en", []))[:20]
    assert not service.texts.missing
