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
    place(service, "test:1", 3, 0, backpack={"madera": 30, "piedra": 10}, known=known, explored=["3:0"])
    view = service.act("test:1", "claro")
    assert any(a.id == "found" for a in view.actions)
    view = service.act("test:1", "found")
    camp = service.store.get("camp", "3:0")
    assert camp["founder"] == "Lyra" and camp["members"] == ["test:1"]
    assert service.store.get("hero", "test:1")["backpack"] == {"madera": 10}
    assert "(3, 0)" in view.notice


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
    place(service, account, x, y, backpack={"madera": 200, "piedra": 200, "fibra": 100}, known=known, explored=[f"{x}:{y}"])
    return service.act(account, "found")


def test_camp_grows_one_zone_per_level(service):
    make_hero(service, "test:1", "Lyra")
    found_at(service, "test:1", 6, 0)
    for expected in (2, 3, 4):
        view = service.act("test:1", "grow")
        assert view.kind == "player_camp" and len(view.actions) <= 4
        camp = service.store.get("camp", "6:0")
        assert camp["level"] == expected and len(camp["zones"]) == expected
    assert camp["zones"] == [[6, 0], [6, 1], [7, 0], [6, -1]]
    hero = service.store.get("hero", "test:1")
    assert hero["backpack"]["madera"] == 200 - 20 - 15 * (1 + 2 + 3)


def test_land_blocks_other_camps_and_counts_for_travel(service):
    from engine.world import travel_minutes
    make_hero(service, "test:1", "Lyra")
    found_at(service, "test:1", 6, 0)
    service.act("test:1", "grow")
    service.act("test:1", "grow")                       # zones (6,0), (6,1), (7,0)
    make_hero(service, "test:2", "Bram")
    place(service, "test:2", 7, 0, backpack={"madera": 50, "piedra": 50}, known=["7:0", "6:0", "8:0", "7:1", "7:-1"], explored=["7:0"])
    assert not any(a.id == "found" for a in service.act("test:2", "claro").actions)
    hero = service._load("test:1")
    anchors = service._anchors(hero)
    assert travel_minutes(8, 0, anchors, service.content.balance) == 2   # one step past the camp's edge


def test_claro_grows_with_its_stage(service):
    assert service._claro_zones() == [[0, 0]]
    data = service._settlement()
    data["stage"] = 2
    service.store.put("settlement", "claro", data)
    assert service._claro_zones() == [[0, 0], [0, 1], [1, 0]]
    assert service._territory(1, 0) == {"claro": True}
