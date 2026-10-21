"""The guild from the first moment (D-269), 👥 Jugadores at the bonfire (D-265, D-274) and works that take time (D-269.4).

[ES] Pruebas del gremio desde el inicio: 👥 Jugadores en el menú de la fogata (en lugar de 🔬 Investigar) con los que jugaron en
el último minuto y el contador "N/20"; crear un gremio (🥉20, nombre libre y único), pedir entrar y aceptar (líder u oficial),
invitar desde la tarjeta de un jugador, oficiales, ceder el liderazgo, salir y disolver; ver a los miembros (dónde están, qué
hacen, si están en línea); 📢 mensajes a cada miembro en su idioma; 💰 depositar en el fondo desde lejos; 📍 punto de reunión y
🏗️ Moverte a la construcción (viaje de verdad, sin diagonales, aunque nunca hayas pisado esa zona); fundar con 2 presentes
(1 h con 2, 30 min con 4, nunca menos del piso); el campamento nace con el nombre del gremio, su gremio y las invitaciones; las
obras del campamento tardan según los miembros en su territorio; y todo se lee en inglés sin textos de reserva.
Archivo: tests/test_gremio_desde_el_inicio.py · Módulo: M15 Social y M14 Construcción · Prueba: engine/service/gremio.py
(GremioMixin) y los ganchos de engine/service/game.py; content/balance.yaml (gremio, works, bonfire, presence.bonfire_seconds).
"""

from conftest import make_hero
from engine.hero import Hero
from engine.service.game import HUB_BUTTONS, HUB_KINDS
from test_camps import found_at, place

MIN = 60


def ids(view):
    return [a.id for a in view.actions]


def text(view):
    return "\n".join([view.notice or ""] + view.body)


def gold(service, account, amount):
    hero = service._load(account)
    hero.gold = amount
    service._save(hero)


def new_gremio(service, account="test:1", name="Lobos Grises"):
    gold(service, account, 100)
    assert service.act(account, "gnew").kind == "name_gremio"
    view = service.text(account, name)
    return service.store.get("gremio_of", account)["gremio"], view


def join(service, gid, account, leader="test:1"):
    service.act(account, f"greq:{gid}")
    service.act(leader, f"gans:{gid}:{account}:y")


def pushes(service, account, kind=None):
    return [v for acc, v in service.tick() if acc == account and (kind is None or v.kind == kind)]


def site(service, account, x, y, explored=True):
    """A good spot to found at (x, y) for this hero: far, explored, neighbours known."""
    known = ["0:0", f"{x}:{y}", f"{x-1}:{y}", f"{x+1}:{y}", f"{x}:{y+1}", f"{x}:{y-1}"]
    place(service, account, x, y, known=known, exploration={f"{x}:{y}": 100} if explored else {})


def fund_cost(service, gid):
    record = service.store.get("gremio", gid)
    record["fund"] = dict(service.content.balance["camps"]["found_cost"])
    service.store.put("gremio", gid, record)


def keep_present(service, clock, accounts, minutes, step=10):
    """Advance the clock `minutes`, every member pressing a button every `step` minutes (they stay present)."""
    for _ in range(int(minutes // step)):
        clock.advance(step * MIN)
        for account in accounts:
            service.act(account, "home")


# ---------------------------------------------------------------------------------------------------- 👥 Jugadores

def test_players_replace_research_in_the_bonfire_hub_and_list_the_last_minute(service, clock):
    make_hero(service, "test:1", "Lyra")
    view = service.act("test:1", "claro")
    assert ids(view)[1] == "players" and "research" not in ids(view) and len(view.actions) <= HUB_BUTTONS
    assert any("👥 Jugadores: 1/20" in line for line in view.body)
    for n, name in ((2, "Bram"), (3, "Cora")):
        make_hero(service, f"test:{n}", name)
        service.act(f"test:{n}", "home")
    clock.advance(2 * MIN)
    service.act("test:2", "home")                                  # Bram played now; Cora 2 minutes ago
    view = service.act("test:1", "players")
    assert view.kind == "players" and ids(view) == ["guild", "players", "claro"]
    body = text(view)
    assert "👥 3/20 en la fogata" in body                          # the counter: the 15-minute rule, you included
    assert "/j1 · Bram" in body and "Cora" not in body              # the list: the last minute only
    assert service.commands()["/jugadores"] == "players" and service.commands()["/players"] == "players"
    card = service.text("test:1", "/j1")
    assert card.kind == "player_card" and "Bram" in text(card) and ids(card) == ["players"]     # no guild: nothing to offer
    assert service.text("test:1", "/j9").kind == "players"           # a code that is not on the list
    service.act("test:2", "go:n")
    clock.advance(5 * MIN)
    service.view("test:2")
    away = service.act("test:2", "players")                         # away from the bonfire: it says where it is seen
    assert away.kind != "players" and "fogata" in away.notice
    assert service.act("test:1", "research").kind == "learn"        # the old button still opens 📚 Aprender oficios


def test_invite_from_a_players_card_and_ask_to_join_from_it(service):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    make_hero(service, "test:3", "Cora")
    gid, _ = new_gremio(service)
    service.act("test:2", "home")
    service.act("test:3", "home")
    service.act("test:1", "players")
    lines = [line for line in service.act("test:1", "players").body if line.startswith("/j")]
    n = next(i for i, line in enumerate(lines, 1) if "Bram" in line)
    card = service.text("test:1", f"/j{n}")
    assert f"ginvite:test:2" in ids(card)
    service.act("test:1", "ginvite:test:2")
    invite = pushes(service, "test:2", "gremio_invite")
    assert invite and all(len(a.id.encode()) <= 64 for a in invite[0].actions)
    service.act("test:2", invite[0].actions[0].id)                  # ✅
    assert "test:2" in service.store.get("gremio", gid)["members"]
    assert "🛡️ Lobos Grises" in text(service.act("test:3", "players"))     # the guild's name next to each member
    lines = [line for line in service.act("test:3", "players").body if line.startswith("/j")]
    n = next(i for i, line in enumerate(lines, 1) if "Lyra" in line)
    card = service.text("test:3", f"/j{n}")
    assert f"greq:{gid}" in ids(card)                                 # Cora can ask to join Lyra's guild from her card


# ---------------------------------------------------------------------------------------------------- creating and joining

def test_creating_a_guild_costs_twenty_bronze_and_its_name_is_unique(service):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    view = service.act("test:1", "guild")                            # no camp, no guild: what a guild is
    assert view.kind == "gremio_none" and ids(view)[:2] == ["gnew", "glist"]
    gold(service, "test:1", 19)
    assert "Te faltan monedas" in service.act("test:1", "gnew").notice
    gold(service, "test:1", 100)
    service.act("test:1", "gnew")
    assert service.text("test:1", "x").kind == "name_gremio"
    view = service.text("test:1", "Lobos Grises")
    assert view.kind == "gremio" and view.kind in HUB_KINDS and "Lobos Grises" in view.notice
    assert service._load("test:1").gold == 100 - service.content.balance["gremio"]["found_coins"] == 80
    assert "Ya tienes gremio" in service.act("test:1", "gnew").notice     # one guild per hero
    gold(service, "test:2", 100)
    service.act("test:2", "gnew")
    assert service.text("test:2", "lobos grises").kind == "name_gremio"   # taken (no case, no accents)
    assert service.store.get("gremio_of", "test:2") is None


def test_request_accept_refuse_officers_and_the_cap_of_five(service):
    make_hero(service, "test:1", "Lyra")
    gid, _ = new_gremio(service)
    for n in range(2, 8):
        make_hero(service, f"test:{n}", f"Miembro{chr(64 + n)}")
    listing = service.act("test:2", "glist")
    assert listing.kind == "gremio_list" and listing.expects_text and any("/g1 · 🛡️ Lobos Grises" in l for l in listing.body)
    found = service.text("test:2", "lobos")                          # any text searches
    assert any("Lobos Grises" in line for line in found.body)
    card = service.text("test:2", "/g1")
    assert card.kind == "gremio_card" and f"greq:{gid}" in ids(card)
    service.act("test:2", f"greq:{gid}")
    ask = pushes(service, "test:1", "gremio_request")
    assert ask and all(len(a.id.encode()) <= 64 for a in ask[0].actions)
    service.act("test:1", ask[0].actions[0].id)
    assert service.store.get("gremio", gid)["members"] == ["test:1", "test:2"]
    assert pushes(service, "test:2", "gremio_answer")
    service.act("test:3", f"greq:{gid}")
    service.act("test:1", f"gans:{gid}:test:3:n")                     # refused
    assert "test:3" not in service.store.get("gremio", gid)["members"] and service.store.get("gremio_of", "test:3") is None
    assert "ya se respondió" in service.act("test:1", f"gans:{gid}:test:3:y").notice
    service.text("test:1", "/m2")                                      # Bram's card → ⭐ officer
    view = service.act("test:1", "goff:test:2")
    assert "test:2" in service.store.get("gremio", gid)["officers"] and "oficial" in view.notice
    service.act("test:4", f"greq:{gid}")
    assert "1 solicitud espera" in text(service.act("test:2", "guild"))   # D-302: one short line on the guild screen
    view = service.act("test:2", "gmembers")
    assert "greqs" in ids(view)                                        # 🙋 Solicitudes (1) for the officer, in 👥 Miembros
    assert ids(service.act("test:2", "greqs"))[-1] == "gmembers"       # its ↩️ goes back there
    service.act("test:2", f"gans:{gid}:test:4:y")                      # an officer accepts too
    join(service, gid, "test:5")
    join(service, gid, "test:6")
    assert len(service.store.get("gremio", gid)["members"]) == 5      # 5 before the camp
    view = service.act("test:7", f"greq:{gid}")
    assert "lleno" in view.notice and "test:7" not in service.store.get("gremio", gid)["requests"]


def test_one_guild_per_hero_also_against_old_camps(service):
    from test_camps import old_camp_at
    make_hero(service, "test:1", "Lyra")
    old_camp_at(service, "test:1", 6, 0)                              # a camp of before (no guild)
    gold(service, "test:1", 100)
    assert "Ya tienes gremio (o campamento)" in service.act("test:1", "gnew").notice     # its guild is its camp's
    make_hero(service, "test:2", "Bram")
    new_gremio(service, "test:2", "Osos Pardos")
    place(service, "test:2", 6, 0)
    view = service.act("test:2", "askjoin")                           # in a guild: no other camp
    assert "gremio" in view.notice and "test:2" not in service.store.get("camp", "6:0").get("requests", [])


def test_leaving_handing_over_and_dissolving(service):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    gid, _ = new_gremio(service)
    join(service, gid, "test:2")
    assert "cede el liderazgo" in service.act("test:1", "gleave").notice   # the leader hands over first
    service.text("test:1", "/m2")
    assert service.act("test:1", "glead:test:2").kind == "gremio_confirm"
    service.act("test:1", "glead!:test:2")
    record = service.store.get("gremio", gid)
    assert record["leader"] == "test:2" and "test:1" in record["officers"]
    assert service.act("test:1", "gleave").kind == "gremio_confirm"
    service.act("test:1", "gleave!")
    assert service.store.get("gremio", gid)["members"] == ["test:2"] and service.store.get("gremio_of", "test:1") is None
    hero = service._load("test:2")
    hero.backpack = {"madera": 7}
    service._save(hero)
    service.text("test:2", "/f01")
    service.act("test:2", "gleave")
    view = service.act("test:2", "gleave!")                          # the last one: dissolved, the fund back
    assert service.store.get("gremio", gid)["closed"] and service._load("test:2").backpack == {"madera": 7}
    assert view.kind == "gremio_none" and "disolvió" in view.notice
    gold(service, "test:2", 100)
    service.act("test:2", "gnew")
    assert service.text("test:2", "Lobos Grises").kind == "gremio"   # its name is free again


# ---------------------------------------------------------------------------------------------------- members, messages, fund

def test_members_show_where_they_are_what_they_do_and_if_they_are_online(service, clock):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    gid, _ = new_gremio(service)
    join(service, gid, "test:2")
    place(service, "test:2", 3, 0, energy=50)
    service.act("test:2", "do:explore:3")
    view = service.act("test:1", "gmembers")                         # D-302: the members live in 👥 Miembros
    lines = [line for line in view.body if line.startswith("/m")]
    assert lines[0].startswith("/m1 👑 Lyra") and "🟢 en línea" in lines[0]
    assert "Bram" in lines[1] and "(3, 0)" in lines[1] and "explorando" in lines[1] and "🟢" in lines[1]
    clock.advance(3 * 60 * MIN)
    service.act("test:2", "stop")
    clock.advance(20 * MIN)
    lines = [line for line in service.act("test:1", "gmembers").body if line.startswith("/m")]
    assert "⚪" in lines[1] and "hace 20 min" in lines[1]


def test_messages_go_to_every_member_in_their_language_and_the_last_ones_stay(service):
    from test_idiomas import english_hero
    make_hero(service, "test:1", "Lyra")
    english_hero(service, "test:2", "Bram")
    gid, _ = new_gremio(service)
    join(service, gid, "test:2")
    service.tick()
    ask = service.act("test:1", "gmsg")
    assert ask.expects_text
    view = service.text("test:1", "¡Nos vemos en el bosque!  " + "x" * 300)
    assert view.kind == "guild_chat" and "enviado" in view.notice     # D-302: back to 📢 Chat
    got = pushes(service, "test:2", "gremio_message")
    assert got and got[0].title == "📢 Guild Lobos Grises" and "Lyra: ¡Nos vemos en el bosque!" in got[0].body[0]
    cap = service.content.balance["gremio"]["message_max_chars"]
    stored = service.store.get("gremio", gid)["messages"][-1]["text"]
    assert len(stored) == cap and stored.endswith("…")
    keep = service.content.balance["gremio"]["messages_kept"]
    for n in range(keep + 1):
        service.act("test:2", "gmsg")
        service.text("test:2", f"mensaje {n}")
    messages = service.store.get("gremio", gid)["messages"]
    assert len(messages) == keep and messages[-1]["text"] == f"mensaje {keep}"
    assert f"💬 Bram: mensaje {keep}" in text(service.act("test:1", "gchat"))   # D-302: the chat is its own screen


def test_the_fund_takes_deposits_from_far_away_and_shows_who_gave_what(service):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    gid, _ = new_gremio(service)
    join(service, gid, "test:2")
    place(service, "test:2", 9, -4, backpack={"madera": 12, "piedra": 3, "carne": 2}, energy=50)
    service.act("test:2", "do:explore:3")                             # far away and busy: it still goes in
    view = service.act("test:2", "gfund")
    assert view.kind == "gremio_fund" and any(line.startswith("/f01 ") for line in view.body)
    assert not any("Carne" in line and line.startswith("/f") for line in view.body)      # food is for the pantry
    view = service.text("test:2", "/f01")
    assert "Depositaste" in view.notice and "madera" not in service._load("test:2").backpack
    service.text("test:2", "/f02")
    record = service.store.get("gremio", gid)
    assert record["fund"] == {"madera": 12, "piedra": 3} and record["gave"]["test:2"] == {"madera": 12, "piedra": 3}
    assert any("Bram:" in line and "×12" in line for line in service.act("test:1", "gfund").body)
    assert "No llevas nada" in service.text("test:2", "/f01").notice


# ---------------------------------------------------------------------------------------------------- meeting point, 🏗️ button

def test_meeting_point_and_the_construction_button_travel_the_real_path(service, clock):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    gid, _ = new_gremio(service)
    join(service, gid, "test:2")
    service.tick()
    zone = service.act("test:2", "home")
    assert ids(zone)[-1] == "zmap" and zone.layout == [2, 2, 1, 1]  # no place defined: no button
    place(service, "test:1", 3, -2)
    service.act("test:1", "gmeet")
    view = service.act("test:1", "gmeetset")
    assert service.store.get("gremio", gid)["meet"] == [3, -2] and view.kind == "gremio_meet"
    told = pushes(service, "test:2", "gremio_news")
    assert told and told[0].actions[0].id == "goask:3:-2"
    assert not service._load("test:2").remembers(3, -2)               # Bram never stood there
    zone = service.act("test:2", "home")
    assert ids(zone)[-1] == "goask:3:-2" and zone.layout == [2, 2, 1, 1, 1]
    assert zone.actions[-1].label == "🏗️ Moverte a la construcción"
    ask = service.act("test:2", "goask:3:-2")
    assert ask.kind == "place_confirm" and ids(ask)[0] == "goto:3:-2"
    trip = service.act("test:2", "goto:3:-2")
    activity = service._load("test:2").activity
    assert activity["goal"] == [3, -2] and activity["to"] == [1, 0]
    assert activity["path"] == [[2, 0], [3, 0], [3, -1], [3, -2]]     # east-west first, then north-south: no diagonals
    assert "goask:3:-2" not in ids(trip)                              # already on the way there
    for _ in range(6):
        clock.advance(5 * MIN)
        service.view("test:2")
    hero = service._load("test:2")
    if (hero.x, hero.y) == (3, -2):                                   # (an ambush could stop the trip: not this test's point)
        zone = service.act("test:2", "home")
        assert "goask:3:-2" not in ids(zone) and zone.layout == [2, 2, 1, 1]   # standing there: no button


def test_the_travel_screen_offers_the_construction_too(service):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    gid, _ = new_gremio(service)
    join(service, gid, "test:2")
    place(service, "test:1", -2, 1)
    service.act("test:1", "gmeetset")
    view = service.act("test:2", "go:e")
    assert view.kind == "activity" and "goask:-2:1" in ids(view) and len(view.actions) <= 4


# ---------------------------------------------------------------------------------------------------- founding

def test_founding_needs_two_members_present_and_takes_an_hour(service, clock):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    gid, _ = new_gremio(service)
    join(service, gid, "test:2")
    fund_cost(service, gid)
    site(service, "test:1", 6, 0)
    view = service.act("test:1", "gfound")
    assert view.kind == "gremio_found" and "found" not in ids(view)
    assert any("Miembros del gremio aquí: 1 de 2" in line for line in view.body)
    place(service, "test:2", 6, 0)
    service.act("test:2", "home")
    view = service.act("test:1", "gfound")
    assert "found" in ids(view)
    service.act("test:1", "found")
    record = service.store.get("gremio", gid)
    assert record["founding"] and record["fund"] == {}                # the fund paid when it started
    keep_present(service, clock, ["test:1", "test:2"], 50)
    assert service.store.get("camp", "6:0") is None                   # 50 min with 2: not yet
    assert "🏗️ Fundando" in text(service.act("test:1", "guild"))
    keep_present(service, clock, ["test:1", "test:2"], 10)
    camp = service.store.get("camp", "6:0")
    assert camp and camp["name"] == "Lobos Grises" and camp["founder_id"] == "test:1" and camp["members"] == ["test:1"]


def test_founding_with_four_takes_half_an_hour_and_never_less_than_the_floor(service, clock):
    make_hero(service, "test:1", "Lyra")
    gid, _ = new_gremio(service)
    members = ["test:1"]
    for n in (2, 3, 4):
        make_hero(service, f"test:{n}", f"Miembro{chr(64 + n)}")
        join(service, gid, f"test:{n}")
        members.append(f"test:{n}")
    fund_cost(service, gid)
    site(service, "test:1", 6, 0)
    for account in members[1:]:
        place(service, account, 6, 0)
        service.act(account, "home")
    service.act("test:1", "found")
    keep_present(service, clock, members, 20)
    assert service.store.get("camp", "6:0") is None
    keep_present(service, clock, members, 10)
    assert service.store.get("camp", "6:0") is not None               # 30 min with 4
    # the floor: never under found_floor_minutes, however many are there (here raised to 40 to see it with 4 members)
    service.content.balance["gremio"]["found_floor_minutes"] = 40
    make_hero(service, "test:9", "Zora")
    gid2, _ = new_gremio(service, "test:9", "Osos Pardos")
    others = []
    for n in (5, 6, 7):
        make_hero(service, f"test:{n}", f"Otro{chr(64 + n)}")
        join(service, gid2, f"test:{n}", leader="test:9")
        others.append(f"test:{n}")
    fund_cost(service, gid2)
    site(service, "test:9", -6, 0)
    for account in others:
        place(service, account, -6, 0)
        service.act(account, "home")
    service.act("test:9", "found")
    keep_present(service, clock, ["test:9"] + others, 30)
    assert service.store.get("camp", "-6:0") is None
    keep_present(service, clock, ["test:9"] + others, 10)
    assert service.store.get("camp", "-6:0") is not None


def test_nobody_present_pauses_the_founding_and_tick_finishes_it(service, clock):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    gid, _ = new_gremio(service)
    join(service, gid, "test:2")
    fund_cost(service, gid)
    site(service, "test:1", 6, 0)
    place(service, "test:2", 6, 0)
    service.act("test:2", "home")
    service.act("test:1", "found")
    clock.advance(5 * 60 * MIN)                                       # both gone quiet: only their first 15 min counted
    service.tick()
    assert service.store.get("camp", "6:0") is None
    done = service.store.get("gremio", gid)["founding"]["done"]
    assert done == 2 * 15 * MIN
    assert service.store.get("works_open", f"found:{gid}")["eta"] is None      # paused: tick() no longer looks at it
    for account in ("test:1", "test:2"):                              # both exploring there: present with the chat closed
        place(service, account, 6, 0, energy=50)
        service.act(account, "do:explore:6")
    entry = service.store.get("works_open", f"found:{gid}")
    assert entry and entry["eta"] is not None
    clock.advance(entry["eta"] - clock.now() + 1)
    out = service.tick()                                              # nobody pressed anything: tick() ends it
    assert service.store.get("camp", "6:0") is not None and service._load("test:1").camp == "6:0"
    assert any(acc == "test:1" and v.kind == "gremio_founded" for acc, v in out)       # the leader is told...
    assert any(acc == "test:2" and v.kind == "gremio_camp_invite" for acc, v in out)   # ...and the other one invited


def test_the_camp_is_born_with_the_guild_and_invites_the_other_members(service, clock):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    make_hero(service, "test:3", "Cora")
    gid, _ = new_gremio(service)
    join(service, gid, "test:2")
    join(service, gid, "test:3")
    record = service.store.get("gremio", gid)
    record["fund"] = {"madera": 25, "piedra": 10}                     # 5 wood more than founding asks
    service.store.put("gremio", gid, record)
    site(service, "test:1", 6, 0)
    place(service, "test:2", 6, 0)
    service.act("test:2", "home")
    service.act("test:1", "found")
    keep_present(service, clock, ["test:1", "test:2"], 60)
    camp = service.store.get("camp", "6:0")
    guild = service.store.get("guild", "6:0")
    assert camp["gremio"] == gid and guild["name"] == "Lobos Grises" and guild["gremio"] == gid and guild["level"] == 1
    assert service._members_cap(camp) == 10 and camp["cap_floor"] == 0     # D-327: the campamento stage; a new camp has no old cap
    assert service.store.get("upgrades", "6:0")["fund"] == {"madera": 5}       # what was left goes to the works
    assert service.store.get("gremio", gid)["invited"] == ["test:2", "test:3"]
    invites = [v for acc, v in service.tick() if acc == "test:3" and v.kind == "gremio_camp_invite"]
    assert invites and ids(invites[0]) == [f"gcamp:{gid}:y", f"gcamp:{gid}:n"]
    zone = service.act("test:3", "home")                              # Cora has not answered: 🏗️ takes her to the camp
    assert ids(zone)[-1] == "goask:6:0"
    service.act("test:3", f"gcamp:{gid}:y")
    assert service.store.get("camp", "6:0")["members"] == ["test:1", "test:3"] and service._load("test:3").camp == "6:0"
    assert "goask:6:0" not in ids(service.act("test:3", "home"))     # a member of the founded camp: no button
    service.act("test:2", f"gcamp:{gid}:n")
    assert service._load("test:2").camp is None and service.store.get("gremio_of", "test:2") is None
    assert service.act("test:2", "guild").kind == "gremio_none"      # free for another guild
    assert service.act("test:1", "guild").kind == "guild"            # the leader sees the camp's guild (D-97)
    assert "ya se respondió" in service.act("test:3", f"gcamp:{gid}:y").notice


# ---------------------------------------------------------------------------------------------------- works with time

def give_all(service, account, uid):
    camp = service.store.get("camp", "6:0")
    udef = service._upgrade_catalog()[uid]
    need = service._upgrade_need(udef, service._camp_perks(camp, service._load(account)))
    hero = service._load(account)
    for item, n in need.items():
        if item == "coins":
            hero.gold += n
        else:
            hero.backpack[item] = hero.backpack.get(item, 0) + n
    service._save(hero)
    return service.act(account, f"upg:{uid}")


def test_camp_works_take_time_by_the_members_in_the_territory(service, clock):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    found_at(service, "test:1", 6, 0)
    service.act("test:1", "claim:7:0")                                # the territory: (6, 0) and (7, 0)
    uid = service._open_works(service.store.get("camp", "6:0"), service._upgrades("6:0"))[0]
    level = int(service._upgrade_catalog()[uid].get("level", 1))
    view = give_all(service, "test:1", uid)
    record = service.store.get("upgrades", "6:0")
    assert uid in record["building"] and uid not in record["built"] and "Materiales completos" in view.notice
    assert uid not in service._open_works(service.store.get("camp", "6:0"), service._upgrades("6:0"))
    assert "🏗️ Obras en curso" in text(service.act("test:1", "upgrades"))
    keep_present(service, clock, ["test:1"], 60 * level)              # alone: twice as long (2 h × level)
    assert uid not in service.store.get("upgrades", "6:0")["built"]
    hero = service._load("test:2")
    hero.camp = "6:0"
    service._save(hero)
    camp = service.store.get("camp", "6:0")
    camp["members"].append("test:2")
    service.store.put("camp", "6:0", camp)
    place(service, "test:2", 7, 0)                                    # anywhere inside the territory counts
    service.act("test:2", "home")
    keep_present(service, clock, ["test:1", "test:2"], 30 * level)    # 1 h × level of work left: 30 min with 2
    assert uid in service.store.get("upgrades", "6:0")["built"]
    assert any(v.kind == "camp_news" for acc, v in service.tick() if acc == "test:2")


def test_a_work_pauses_with_nobody_and_old_built_upgrades_stay(service, clock):
    make_hero(service, "test:1", "Lyra")
    found_at(service, "test:1", 6, 0)
    upgrades = service._upgrades("6:0")
    first = list(service._upgrade_catalog())[0]
    upgrades["built"][first] = clock.now()                            # built before D-269: it stays built
    service.store.put("upgrades", "6:0", upgrades)
    uid = service._open_works(service.store.get("camp", "6:0"), service._upgrades("6:0"))[0]
    give_all(service, "test:1", uid)
    place(service, "test:1", 0, 0)                                    # away from the territory
    clock.advance(10 * 60 * MIN)
    service.act("test:1", "home")
    record = service.store.get("upgrades", "6:0")
    assert first in record["built"] and uid in record["building"]
    assert record["building"][uid]["done"] <= 15 * MIN + 1            # only the minutes before leaving counted


# ---------------------------------------------------------------------------------------------------- English

def test_the_guild_reads_well_in_english(service, clock):
    from test_idiomas import english_hero
    english_hero(service, "test:1", "Lyra")
    english_hero(service, "test:2", "Bram", "mago_dps") if "mago_dps" in service.content.classes else english_hero(service, "test:2", "Bram")
    view = service.act("test:1", "claro")
    assert view.actions[1].label == "👥 Players"
    assert service.act("test:1", "players").title == "👥 Players at the campfire"
    gold(service, "test:1", 100)
    service.act("test:1", "gnew")
    view = service.text("test:1", "Grey Wolves")
    gid = service.store.get("gremio_of", "test:1")["gremio"]
    join(service, gid, "test:2")
    for screen in ("guild", "gmembers", "gfunds", "gchat", "gfund", "gmeet", "gmeetset", "gfound", "glist", "gmsg"):   # D-302
        view = service.act("test:1", screen)
        assert view.title and "[" not in text(view), (screen, text(view))
    site(service, "test:1", 6, 0)
    fund_cost(service, gid)
    place(service, "test:2", 6, 0)
    zone = service.act("test:2", "home")                              # the meeting point is the Clearing (set above)
    assert zone.actions[-1].label == "🏗️ Go to the construction site" and zone.actions[-1].id == "goask:0:0"
    service.act("test:1", "found")
    keep_present(service, clock, ["test:1", "test:2"], 60)
    assert service.store.get("camp", "6:0")["name"] == "Grey Wolves"
    service.tick()
    assert not service.texts.fallbacks.get("en"), sorted(service.texts.fallbacks.get("en", []))[:20]
    assert not service.texts.missing, service.texts.missing


def test_old_heroes_load_with_no_guild_record(service):
    """Heroes and camps saved before D-269 keep working: no new field is required (D-64)."""
    make_hero(service, "test:1", "Lyra")
    data = service.store.get("hero", "test:1")
    assert Hero.from_dict(data).camp is None
    assert service.act("test:1", "guild").kind == "gremio_none"
    assert service.act("test:1", "home").layout == [2, 2, 1, 1]
