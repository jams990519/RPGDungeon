"""Player camps (D-71): founding requirements and contact with visitors. [ES] Pruebas de campamentos."""

from conftest import make_hero
from engine.hero import Hero


def place(service, account, x, y, **extra):
    hero = Hero.from_dict(service.store.get("hero", account))
    hero.x, hero.y = x, y
    for k, v in extra.items():
        setattr(hero, k, v)
    service.store.put("hero", account, hero.to_dict())


def test_found_camp_needs_exploring_around(service):
    make_hero(service, "test:1", "Lyra")
    place(service, "test:1", 3, 0, backpack={"madera": 30, "piedra": 10})
    view = service.act("test:1", "claro")
    assert view.kind == "found_camp" and not any(a.id == "found" for a in view.actions)
    known = ["0:0", "3:0", "2:0", "4:0", "3:1", "3:-1"]
    place(service, "test:1", 3, 0, backpack={"madera": 30, "piedra": 10}, known=known, exploration={"3:0": 100})
    view = service.act("test:1", "claro")
    assert any(a.id == "found" for a in view.actions)
    ask = service.act("test:1", "found")
    assert ask.kind == "name_camp" and ask.expects_text
    assert service.text("test:1", "x").kind == "name_camp"           # too short: asked again
    view = service.text("test:1", "Roca Alta")
    camp = service.store.get("camp", "3:0")
    assert camp["name"] == "Roca Alta" and camp["founder"] == "Lyra" and camp["members"] == ["test:1"]
    assert service.store.get("hero", "test:1")["backpack"] == {"madera": 10}
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
    known = ["0:0", f"{x}:{y}", f"{x-1}:{y}", f"{x+1}:{y}", f"{x}:{y+1}", f"{x}:{y-1}"]
    place(service, account, x, y, backpack={"madera": 200, "piedra": 200, "fibra": 100}, known=known, exploration={f"{x}:{y}": 100})
    service.act(account, "found")
    return service.text(account, f"Campo {account[-1]} {x}")


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
    found_at(service, "test:1", 6, 0)
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
    place(service, "test:2", -6, 0, backpack={"madera": 50, "piedra": 50}, known=known, exploration={"-6:0": 100})
    service.act("test:2", "found")
    view = service.text("test:2", "bastión norte")
    assert view.kind == "name_camp" and service.store.get("camp", "-6:0") is None
