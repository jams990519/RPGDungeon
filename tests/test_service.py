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
    view = service.act("test:1", "grp:guerrero")
    assert view.kind == "create_class" and any(a.id == "grp:" for a in view.actions)
    view = service.act("test:1", "grp:")                # back to the class list
    assert any(a.id.startswith("page:") for a in view.actions)
    service.act("test:1", "grp:guerrero")
    view = service.act("test:1", [a.id for a in service.act("test:1", "grp:guerrero").actions if a.id.startswith("cls:")][0])
    assert view.kind == "origin" and len(view.actions) <= 4      # D-117: the origin comes right after the class...
    assert service.act("test:1", "home").kind == "zone"          # ...but never blocks: the menu goes on playing


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
        service.act("test:1", "do:explore:5")
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
        service.act("test:1", "do:explore:5")
        clock.advance(3600)
        finish_combat(service, "test:1")
    assert service.texts.missing == set()


def test_hero_remembers_places_and_routes_back(service, clock):
    make_hero(service)
    service.act("test:1", "go:e")
    clock.advance(3 * 3600)
    view = service.view("test:1")
    while view.kind == "combat":
        view = service.act("test:1", "atk")
    hero = service.store.get("hero", "test:1")
    assert "1:0" in hero["known"] and "0:0" in hero["known"]
    places = service.act("test:1", "places")
    assert any(a.id == "goto:0:0" for a in places.actions)
    view = service.act("test:1", "goto:0:0")
    if view.kind == "activity":
        clock.advance(3 * 3600)
        service.view("test:1")
        hero = service.store.get("hero", "test:1")
        assert (hero["x"], hero["y"]) == (0, 0) or service.store.get("combat", "test:1")


def test_multi_leg_route_chains(service, clock):
    make_hero(service)
    from engine.hero import Hero
    hero = Hero.from_dict(service.store.get("hero", "test:1"))
    hero.known += ["3:0"]
    service.store.put("hero", "test:1", hero.to_dict())
    view = service.act("test:1", "goto:3:0")
    assert view.kind == "activity"
    for _ in range(10):
        clock.advance(3 * 3600)
        v = service.view("test:1")
        while v.kind == "combat":
            v = service.act("test:1", "atk")
        hero = service.store.get("hero", "test:1")
        if (hero["x"], hero["y"]) == (3, 0) or hero["activity"] is None:
            break
    assert hero["x"] >= 1


def test_shop_and_inn_in_claro(service, clock):
    make_hero(service)
    assert "claro" in [a.id for a in service.menu()]
    ids = [a.id for a in service.act("test:1", "claro").actions]
    assert "shop" in ids and "inn" in ids and "camp" not in ids        # D-98: no common work in the Claro
    hero = service.store.get("hero", "test:1")
    hero["gold"] = 50
    hero["backpack"]["hierba_curativa"] = 2
    hero["hp"] = 10
    service.store.put("hero", "test:1", hero)
    view = service.act("test:1", "buy:pocion_vida")
    assert service.store.get("hero", "test:1")["gold"] == 44 and view.notice
    service.act("test:1", "sell:all")
    assert service.store.get("hero", "test:1")["gold"] == 44 + 2   # 2 herbs x 1
    view = service.act("test:1", "inn")
    assert view.kind == "activity"
    clock.advance(600)
    service.view("test:1")
    hero = service.store.get("hero", "test:1")
    from engine.hero import hero_stats
    assert hero["hp"] == hero_stats(service._kit(service._load("test:1")), 1)["max_hp"] and hero["gold"] == 42


def test_shop_only_in_claro(service, clock):
    make_hero(service)
    service.act("test:1", "go:n")
    clock.advance(3 * 3600)
    service.view("test:1")
    while service.store.get("combat", "test:1"):
        service.act("test:1", "atk")
    view = service.act("test:1", "buy:pocion_vida")
    assert view.notice and "Claro" in view.notice


def test_new_epoch_restarts_the_game(content, clock):
    from engine.core import MemoryStore
    from engine.service import GameService
    store = MemoryStore()
    store.put("meta", "world", {"seed": 1, "epoch": 1})
    store.put("hero", "tg:1", {"name": "Viejo"})
    store.put("zone", "1:0", {"discovered_by": "Viejo"})
    service = GameService(content, store, clock)
    assert store.get("hero", "tg:1") is None and store.get("zone", "1:0") is None
    assert store.get("meta", "world")["epoch"] == content.balance["world"]["epoch"]
    store.put("hero", "tg:2", {"name": "Nuevo"})
    GameService(content, store, clock)  # same epoch: nothing is wiped
    assert store.get("hero", "tg:2") is not None


def test_xp_is_slow_and_infinite(content):
    from engine.hero import xp_for_level
    f = content.balance["hero"]["xp_formula"]
    needs = [xp_for_level(f, lv + 1) - xp_for_level(f, lv) for lv in range(1, 200)]
    assert all(b > a for a, b in zip(needs, needs[1:]))  # every level costs more than the last
    assert xp_for_level(f, 1000) > xp_for_level(f, 999) > 0


def test_names_ignore_accents_spaces_and_reservations(service):
    make_hero(service, "test:1", "José Luis")
    service.view("test:2")
    assert service.text("test:2", "jose luis").notice
    assert service.text("test:2", "JoseLuis").notice
    service.view("test:3")
    service.text("test:3", "Aria")          # reserved while test:3 chooses a class
    service.view("test:4")
    assert service.text("test:4", "aria").notice


def test_gather_in_claro_and_sell_to_the_trader(service, clock):
    make_hero(service)
    view = service.act("test:1", "explore")          # tutorial 1: explore the Claro (choose how much energy, D-87)
    assert view.kind == "batch" and any(a.id == "explore_menu" for a in view.actions)
    service.act("test:1", "do:explore:5")
    clock.advance(3600)
    service.view("test:1")
    assert service.store.get("hero", "test:1")["tutorial"] == 1
    service.act("test:1", "do:gather:5")
    clock.advance(3600)
    service.view("test:1")
    hero = service.store.get("hero", "test:1")
    assert hero["tutorial"] == 2
    assert any(hero["backpack"].get(i, 0) for i in ("madera", "fibra"))
    gold = hero["gold"]
    service.act("test:1", "shop")
    view = service.act("test:1", "sell:all")         # tutorial 3: sell what you do not need (D-98 replaced donating)
    hero = service.store.get("hero", "test:1")
    assert hero["tutorial"] == 3 and hero["gold"] > gold and "📜" in view.notice
    assert view.kind == "shop"


def test_the_claro_never_grows(service, clock):
    make_hero(service)
    hero = service.store.get("hero", "test:1")
    hero["backpack"].update({"madera": 50, "fibra": 40})
    service.store.put("hero", "test:1", hero)
    for old_button in ("camp", "donate", "feed"):                 # buttons of the old common work (D-98)
        view = service.act("test:1", old_button)
        assert view.kind == "claro" and "no crece" in view.notice
    assert service._settlement()["stage"] == 0
    assert service.store.get("hero", "test:1")["backpack"]["madera"] == 50   # nothing taken
    view = service.act("test:1", "claro")
    # D-109: the Claro has the basic profession stations, so ⚒️ Oficios ("oficios") is its 3rd button;
    # D-117: 📜 Tablón ("board") took the ↩️ Volver slot (📍 Zona in the bottom menu goes back)
    assert [a.id for a in view.actions] == ["shop", "inn", "oficios", "board"]
    assert any("funda tu propio campamento" in line for line in view.body)


def test_tutorial_hint_shows_in_zone(service):
    make_hero(service)
    view = service.view("test:1")
    assert any("📜" in line for line in view.body)


def test_invite_link_gives_energy_on_join(service):
    make_hero(service, "test:1", "Lyra")
    before = service.store.get("hero", "test:1")["energy"]
    code = service.invite_code("test:1")
    service.register_referral("test:2", code)
    make_hero(service, "test:2", "Bram")
    inviter = service.store.get("hero", "test:1")
    assert inviter["energy"] == before + 1 and inviter["invites"] == 1
    service.register_referral("test:1", code)       # cannot invite yourself again
    assert service.store.get("referral", "test:1") is None


def test_travel_costs_energy(service, clock):
    make_hero(service)
    hero = service.store.get("hero", "test:1")
    hero["energy"] = 0
    service.store.put("hero", "test:1", hero)
    view = service.act("test:1", "go:n")
    assert view.kind == "zone" and "⚡" in (view.notice or "")
    view = service.act("test:1", "explore_menu")
    assert service.act("test:1", "do:explore:5").kind == "explore_menu"   # exploring costs energy too (D-78)
    clock.advance(86400 / 40 + 5)
    view = service.act("test:1", "go:n")
    assert view.kind == "activity"


def test_everyone_gets_fifty_energy_once(service):
    make_hero(service)
    hero = service.store.get("hero", "test:1")
    assert hero["energy"] == 50
    hero["energy"], hero["energy_version"] = 7, 1
    service.store.put("hero", "test:1", hero)
    service.act("test:1", "hero")
    assert service.store.get("hero", "test:1")["energy"] == 50
    hero = service.store.get("hero", "test:1")
    hero["energy"] = 7
    service.store.put("hero", "test:1", hero)
    service.act("test:1", "hero")
    assert service.store.get("hero", "test:1")["energy"] == 7      # only once


def test_level_cap_is_100(content):
    from engine.hero import xp_for_level
    hb = content.balance["hero"]
    assert hb["max_level"] == 100
    assert xp_for_level(hb["xp_formula"], 100) > 5_000_000


def test_class_pages_have_at_most_six_buttons(service):
    service.view("test:9")
    view = service.text("test:9", "Pager")
    seen = set()
    for _ in range(10):
        assert len(view.actions) <= 4
        seen |= {a.id for a in view.actions if a.id.startswith("grp:")}
        nxt = [a.id for a in view.actions if a.id.startswith("page:")]
        view = service.act("test:9", nxt[0])
    assert len(seen & {f"grp:{g}" for g in service._class_groups()}) == len(service._class_groups())


def test_patch_announced_once_and_players_survive_reset(content, clock):
    from engine.core import MemoryStore
    from engine.service import GameService
    store = MemoryStore()
    store.put("meta", "world", {"seed": 1, "epoch": 1})
    store.put("hero", "tg:5", {"name": "Viejo"})
    service = GameService(content, store, clock)
    assert "tg:5" in service.players()            # kept for the announcement even after the reset
    view = service.pending_announcement()
    assert view is not None and view.body
    assert service.pending_announcement() is None  # only once per version


def test_falling_means_a_slow_recovery(service, clock):
    from engine.hero import hero_stats
    make_hero(service)
    hero = service._load("test:1")
    max_hp = hero_stats(service._kit(hero), hero.level)["max_hp"]
    hero.hp, hero.downed, hero.last_regen_at = 1, True, clock.now()
    service._save(hero)
    for _ in range(10):                                   # acting every minute must not lose the slow regen
        clock.advance(60)
        service.act("test:1", "hero")
    slow = service._load("test:1").hp
    assert 1 < slow < 1 + max_hp * 0.03
    assert "Malherido" in "\n".join(service.act("test:1", "hero").body)
    clock.advance(9 * 3600)
    service.act("test:1", "hero")
    hero = service._load("test:1")
    assert hero.hp == max_hp and not hero.downed


def test_the_map_is_a_square_as_wide_as_the_message(service):
    make_hero(service)
    body = service.act("test:1", "map").body
    side = 2 * service.content.balance["map_view"]["radius"] + 1
    rows = [line for line in body if line and " " not in line]              # the grid rows: cells only, no spaces
    assert side == 13 and len(rows) == side
    assert all(line.replace("\ufe0f", "").__len__() == side for line in rows)   # every row has 13 cells


def test_health_screen_shows_the_body_and_how_it_heals(service):
    make_hero(service)
    hero = service._load("test:1")
    max_hp = hero.hp
    hero.hp, hero.last_regen_at = max_hp // 3, service.clock.now()
    service._save(hero)
    assert service.commands()["/salud"] == "health"
    view = service.act("test:1", "health")
    body = "\n".join(view.body)
    assert view.kind == "health" and [a.id for a in view.actions] == ["potions", "hero"]
    assert "herido" in body and "4 h" in body and "Enfermedades: ninguna" in body
    assert not service.texts.missing


def test_full_health_comes_back_in_four_hours(service, clock):
    make_hero(service)
    hero = service._load("test:1")
    max_hp = hero.hp
    hero.hp, hero.last_regen_at = 1, clock.now()
    service._save(hero)
    clock.advance(2 * 3600)
    service.view("test:1")
    assert abs(service._load("test:1").hp - max_hp / 2) <= 2            # half in 2 hours
    clock.advance(2 * 3600)
    service.view("test:1")
    assert service._load("test:1").hp == max_hp


def test_exploring_gives_experience(service, clock):
    make_hero(service)
    service.act("test:1", "do:explore:5")
    clock.advance(3600)
    view = service.view("test:1")
    hero = service._load("test:1")
    assert hero.xp > 0
