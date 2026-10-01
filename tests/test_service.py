"""End-to-end flow through GameService. [ES] Pruebas del recorrido completo: crear héroe, viajar, explorar, pelear."""

from conftest import make_hero


def finish_combat(service, account):
    view = service.view(account)
    for _ in range(80):
        if view.kind != "combat":
            break
        view = service.act(account, "atk")
    return view


def test_creation_flow(service):
    view = service.view("test:1")
    assert view.kind == "create_name" and view.expects_text
    view = service.text("test:1", "x")
    assert view.notice  # bad name
    view = service.text("test:1", "Lyra")
    assert view.kind == "create_class"
    view = service.act("test:1", "cls:guerrero")
    assert view.kind == "zone"


def test_names_are_unique(service):
    make_hero(service, "test:1", "Lyra")
    service.view("test:2")
    view = service.text("test:2", "lyra")
    assert view.kind == "create_name" and view.notice


def test_travel_takes_real_time(service, clock):
    make_hero(service)
    view = service.act("test:1", "go:n")
    assert view.kind == "activity"
    assert service.view("test:1").kind == "activity"
    blocked = service.act("test:1", "go:s")
    assert blocked.notice  # busy
    clock.advance(3 * 3600)
    view = service.view("test:1")
    hero = service.store.get("hero", "test:1")
    assert (hero["x"], hero["y"]) == (0, 1)
    assert view.kind in ("zone", "combat")


def test_tick_notifies_arrivals(service, clock):
    make_hero(service)
    service.act("test:1", "go:e")
    assert service.tick() == []
    clock.advance(3 * 3600)
    notices = service.tick()
    assert len(notices) == 1 and notices[0][0] == "test:1"


def test_explore_and_fight_until_end(service, clock):
    make_hero(service)
    service.act("test:1", "go:e")
    clock.advance(3 * 3600)
    finish_combat(service, "test:1")
    for _ in range(15):
        service.act("test:1", "explore")
        clock.advance(3600)
        view = service.view("test:1")
        if view.kind == "combat":
            end = finish_combat(service, "test:1")
            assert end.kind == "combat_end"
            break
    hero = service.store.get("hero", "test:1")
    assert hero["kills"] + hero["gold"] > 0


def test_action_ids_fit_telegram(service, clock):
    make_hero(service)
    views = [service.view("test:1"), service.act("test:1", "map"), service.act("test:1", "hero"), service.act("test:1", "bag")]
    for view in views:
        for action in view.actions:
            assert len(action.id.encode()) <= 64


def test_no_missing_texts(service, clock):
    make_hero(service)
    service.act("test:1", "map")
    service.act("test:1", "hero")
    service.act("test:1", "bag")
    service.act("test:1", "go:w")
    clock.advance(3 * 3600)
    finish_combat(service, "test:1")
    for _ in range(6):
        service.act("test:1", "explore")
        clock.advance(3600)
        finish_combat(service, "test:1")
    assert service.texts.missing == set()
