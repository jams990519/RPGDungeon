"""Player camps (D-71): founding requirements and contact with visitors. [ES] Pruebas de campamentos.

D-269 (0.35): a camp is founded by a guild (its leader, 2 members present, the fund pays, it takes time). found_at does
all of that; old_camp_at writes a camp as it was founded before D-269 (no guild), for the tests of the old camps' rules
(they keep working: D-64).
"""

from conftest import make_hero
from engine.hero import Hero


def place(service, account, x, y, **extra):
    hero = Hero.from_dict(service.store.get("hero", account))
    hero.x, hero.y = x, y
    for k, v in extra.items():
        setattr(hero, k, v)
    service.store.put("hero", account, hero.to_dict())


def test_found_camp_needs_exploring_around_and_a_guild(service, clock):
    # [ES] D-269 (0.35): lo de siempre (explorar alrededor) y además un gremio: su líder, 2 miembros aquí y el fondo paga
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    place(service, "test:1", 3, 0, backpack={"madera": 30, "piedra": 10})
    view = service.act("test:1", "claro")
    assert view.kind == "found_camp" and not any(a.id == "found" for a in view.actions)
    known = ["0:0", "3:0", "2:0", "4:0", "3:1", "3:-1"]
    place(service, "test:1", 3, 0, backpack={"madera": 30, "piedra": 10}, known=known, exploration={"3:0": 100}, gold=100)
    view = service.act("test:1", "claro")
    assert not any(a.id == "found" for a in view.actions)           # alone, with no guild: nobody founds alone any more
    assert any("gremio" in line for line in view.body)
    assert service.act("test:1", "gnew").kind == "name_gremio"
    assert service.text("test:1", "x").kind == "name_gremio"         # too short: asked again
    service.text("test:1", "Roca Alta")
    gid = service.store.get("gremio_of", "test:1")["gremio"]
    service.act("test:2", f"greq:{gid}")
    service.act("test:1", f"gans:{gid}:test:2:y")
    service.text("test:1", "/f01")                                     # the wood and the stone go to the fund, from here
    service.text("test:1", "/f02")
    place(service, "test:2", 3, 0)
    service.act("test:2", "home")
    view = service.act("test:1", "claro")
    assert any(a.id == "found" for a in view.actions), view.body
    view = service.act("test:1", "found")
    assert view.kind == "found_camp" and service.store.get("camp", "3:0") is None    # it takes time now
    for _ in range(4):                                                  # 1 h with 2 members present
        clock.advance(15 * 60)
        view = service.act("test:1", "claro")
        service.act("test:2", "home")
    camp = service.store.get("camp", "3:0")
    assert camp["name"] == "Roca Alta" and camp["founder"] == "Lyra" and camp["members"] == ["test:1"]
    assert service.store.get("hero", "test:1")["backpack"] == {}       # all of it went to the fund...
    assert service.store.get("upgrades", "3:0")["fund"] == {"madera": 10}   # ...and what was left, to the camp's works
    assert "(3, 0)" in view.notice and "Roca Alta" in view.notice


def test_visitor_contacts_members_and_gets_answer(service, clock):
    make_hero(service, "test:1", "Lyra")
    service.store.put("camp", "0:1", {"name": "Campamento de Lyra", "founder": "Lyra", "founder_id": "test:1",
                                       "members": ["test:1"], "relations": {}, "asked": [], "x": 0, "y": 1})
    make_hero(service, "test:2", "Bram")
    service.act("test:2", "go:n")
    clock.advance(3600)
    service.view("test:2")
    pushes = [v for acc, v in service.tick() if acc == "test:1"]
    assert pushes and pushes[0].kind == "camp_visit"
    answer = pushes[0].actions[0].id                   # friendly
    service.act("test:1", answer)
    assert service.store.get("camp", "0:1")["relations"]["test:2"] == "friendly"
    replies = [v for acc, v in service.tick() if acc == "test:2"]
    assert replies and replies[0].kind == "camp_answer"
    assert all(len(a.id.encode()) <= 64 for a in pushes[0].actions)


def found_at(service, account, x, y):
    """Found a camp at (x, y) the D-269 way, with `account` as leader; return the founder's screen when it is done.

    [ES] Crea el gremio (el 🥉20 se le devuelve antes, así las monedas de la prueba quedan igual), suma un segundo miembro
    de ayuda presente en la zona, deposita en el fondo justo lo que cuesta fundar, empieza la fundación y adelanta el reloj
    de a 15 min (los dos tocan un botón: siguen presentes) hasta que termina (1 h con 2). El ayudante rechaza la invitación
    al campamento y se borra, así el campamento queda como antes: solo el fundador, con 🪵 180, 🪨 190 y 🌿 100 en la
    mochila. Lo único nuevo: el campamento tiene gremio (su cupo es el del gremio, guild.levels) y el reloj avanzó 1 hora.
    """
    outbox = service.store.get("outbox", account)
    known =["0:0", f"{x}:{y}", f"{x-1}:{y}", f"{x+1}:{y}", f"{x}:{y+1}", f"{x}:{y-1}"]
    cost = dict(service.content.balance["camps"]["found_cost"])
    place(service, account, x, y, backpack=dict(cost), known=known, exploration={f"{x}:{y}": 100})
    hero = service._load(account)
    hero.gold += int(service.content.balance["gremio"]["found_coins"])
    service._save(hero)
    service.act(account, "gnew")
    service.text(account, f"Campo {account[-1]} {x}")
    gid = service.store.get("gremio_of", account)["gremio"]
    helper = f"aid:{account}:{x}:{y}"
    make_hero(service, helper, f"Aide{account[-1]}x{x + 500}y{y + 500}")
    service.act(helper, f"greq:{gid}")
    service.act(account, f"gans:{gid}:{helper}:y")
    for item_id in cost:
        service.text(account, f"/f{int(service.content.items[item_id]['code']):02d}")
    place(service, account, x, y, backpack={"madera": 180, "piedra": 190, "fibra": 100})
    place(service, helper, x, y)
    service.act(helper, "home")
    service.act(account, "found")
    view = None
    for _ in range(12):
        service.clock.advance(service._seconds(15))
        view = service.act(account, "claro")
        if service.store.get("camp", f"{x}:{y}"):
            break
        service.act(helper, "home")
    assert service.store.get("camp", f"{x}:{y}"), "the founding did not end"
    service.act(helper, f"gcamp:{gid}:n")
    for space in ("hero", "player", "outbox", "gremio_codes", "walk"):
        service.store.delete(space, helper)
    for key in (f"{x}:{y}", "0:0"):
        record = service.store.get("presence", key)
        if record and record.get("seen", {}).pop(helper, None) is not None:
            service.store.put("presence", key, record)
    camp = service.store.get("camp", f"{x}:{y}")
    if outbox:                          # the helper's request and answer to the founder are not part of the test
        service.store.put("outbox", account, outbox)
    else:
        service.store.delete("outbox", account)
    assert camp["members"] == [account]
    return view


def old_camp_at(service, account, x, y, name=None):
    """A camp founded before D-269 (no guild), written as the old solo founding left it (D-64: those camps keep working).

    [ES] Para las pruebas de las reglas de los campamentos sin gremio (D-84, D-97): el campamento, su nombre, su territorio y
    la mochila con 🪵 180, 🪨 190 y 🌿 100, como dejaba el viejo found_at. Sin gremio y sin mover el reloj.
    """
    known = ["0:0", f"{x}:{y}", f"{x-1}:{y}", f"{x+1}:{y}", f"{x}:{y+1}", f"{x}:{y-1}"]
    place(service, account, x, y, backpack={"madera": 180, "piedra": 190, "fibra": 100}, known=known, exploration={f"{x}:{y}": 100})
    hero = service._load(account)
    name = name or f"Campo {account[-1]} {x}"
    key = f"{x}:{y}"
    now = service.clock.now()
    service.store.put("camp_name", service._name_key(name), {"camp": key})
    service.store.put("camp", key, {"name": name, "founder": hero.name, "founder_id": hero.id, "members": [hero.id],
                                    "relations": {}, "asked": [], "x": x, "y": y, "created": now, "level": 1, "zones": [[x, y]],
                                    "next_raid_at": now + service._raid_interval()})
    service.store.put("territory", key, {"camp": key})
    hero.camp = key
    service._save(hero)
    return service.act(account, "claro")


def test_camp_grows_one_zone_per_level(service):
    make_hero(service, "test:1", "Lyra")
    found_at(service, "test:1", 6, 0)
    for expected, pick in ((2, "claim:7:0"), (3, "claim:8:0"), (4, "claim:6:1")):
        choose = service.act("test:1", "grow")                    # you choose where it grows (D-87)
        assert choose.kind == "camp_grow" and len(choose.actions) <= 4
        view = service.act("test:1", pick)
        assert view.kind == "player_camp" and len(view.actions) <= 8      # D-192: the camp hub shows up to 8, 2 per row
        camp = service.store.get("camp", "6:0")
        assert camp["level"] == expected and len(camp["zones"]) == expected
    assert camp["zones"] == [[6, 0], [7, 0], [8, 0], [6, 1]]
    assert service.act("test:1", "claim:20:20").kind == "camp_grow"   # not next to the land: refused
    hero = service.store.get("hero", "test:1")
    assert hero["backpack"]["madera"] == 200 - 20 - 15 * (1 + 2 + 3)


def test_land_blocks_other_camps_and_counts_for_travel(service):
    from engine.world import travel_minutes
    make_hero(service, "test:1", "Lyra")
    found_at(service, "test:1", 6, 0)
    service.act("test:1", "claim:6:1")
    service.act("test:1", "claim:7:0")                   # zones (6,0), (6,1), (7,0)
    make_hero(service, "test:2", "Bram")
    place(service, "test:2", 7, 0, backpack={"madera": 50, "piedra": 50}, known=["7:0", "6:0", "8:0", "7:1", "7:-1"], exploration={"7:0": 100})
    assert not any(a.id == "found" for a in service.act("test:2", "claro").actions)
    hero = service._load("test:1")
    anchors = service._anchors(hero)
    assert travel_minutes(8, 0, anchors, service.content.balance) == 1   # D-197: 1 minute per zone everywhere
    old = {**service.content.balance, "travel": {**service.content.balance["travel"], "first_minutes": 2, "steps_per_minute": 2}}
    assert travel_minutes(8, 0, anchors, old) == 2          # with D-78's rule, the camp still restarts the count


def test_claro_grows_with_its_stage(service):
    assert service._claro_zones() == [[0, 0]]
    data = service._settlement()
    data["stage"] = 2
    service.store.put("settlement", "claro", data)
    assert service._claro_zones() == [[0, 0], [0, 1], [1, 0]]
    assert service._territory(1, 0) == {"claro": True}


def test_founder_lets_players_join_and_cap_grows(service, clock):
    make_hero(service, "test:1", "Lyra")
    old_camp_at(service, "test:1", 6, 0)                 # D-84: a camp without a guild (one founded before D-269)
    camp = service.store.get("camp", "6:0")
    assert service._members_cap(camp) == 2
    for n, name in ((2, "Bram"), (3, "Cora")):
        make_hero(service, f"test:{n}", name)
        place(service, f"test:{n}", 6, 0)
    view = service.act("test:2", "claro")
    assert any(a.id == "askjoin" for a in view.actions)
    service.act("test:2", "askjoin")
    asks = [v for acc, v in service.tick() if acc == "test:1" and v.kind == "camp_join"]
    assert asks and all(len(a.id.encode()) <= 64 for a in asks[0].actions)
    service.act("test:1", asks[0].actions[0].id)                       # accept
    assert service.store.get("camp", "6:0")["members"] == ["test:1", "test:2"]
    assert service.store.get("hero", "test:2")["camp"] == "6:0"
    assert any(v.kind == "camp_answer" for acc, v in service.tick() if acc == "test:2")
    view = service.act("test:3", "askjoin")                             # full at level 1
    assert "lleno" in (view.notice or "")
    service.act("test:1", "claim:7:0")
    assert service._members_cap(service.store.get("camp", "6:0")) == 4
    service.act("test:2", "leave")
    assert service.store.get("hero", "test:2")["camp"] is None
    assert service.store.get("camp", "6:0")["members"] == ["test:1"]


def test_camp_names_are_unique_and_founder_can_rename(service):
    make_hero(service, "test:1", "Lyra")
    found_at(service, "test:1", 6, 0)
    service.act("test:1", "rename")
    service.text("test:1", "Bastion Norte")
    assert service.store.get("camp", "6:0")["name"] == "Bastion Norte"
    make_hero(service, "test:2", "Bram")
    known = ["0:0", "-6:0", "-7:0", "-5:0", "-6:1", "-6:-1"]
    place(service, "test:2", -6, 0, backpack={"madera": 50, "piedra": 50}, known=known, exploration={"-6:0": 100}, gold=100)
    assert service.act("test:2", "found").kind == "found_camp"         # D-269: nobody founds alone (no name prompt)
    service.act("test:2", "gnew")                                       # the guild's name is its camp's: unique among both
    view = service.text("test:2", "bastión norte")
    assert view.kind == "name_gremio" and "Ya hay" in view.body[0] and service.store.get("gremio_of", "test:2") is None
