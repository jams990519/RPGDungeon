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
