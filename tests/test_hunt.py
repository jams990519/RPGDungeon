"""Hunting in the zone and the hunting party of a camp (D-106, provisional).

[ES] Pruebas de la cacería: 🧭 Explorar → 🏹 Cazar abre la pantalla de cacería y 🏹 Buscar presa empieza enseguida una pelea
contra un enemigo común de la zona por 2 de energía (D-108), sin exploración ni recursos; al ganar sale 🏹 Otra presa. No se caza
malherido, ocupado, sin energía, en el Claro ni en la guarida. 📒 Lugares se mudó a 🗺️ Mapa (🧭 Explorar sigue en 4 botones).
La 🏹 Partida de caza de un campamento avisa solo a los miembros presentes en la misma zona, da bono de grupo y cuenta las
presas; al terminar la ventana (reloj perezoso) llega un informe y, si juntaron la meta, un premio chico. También: ningún
texto falta y ninguna pantalla pasa de 4 botones (6 en combate).
"""

from collections import deque

from conftest import make_hero
from engine.core import FixedClock, MemoryStore
from engine.hero import hero_stats
from engine.service import GameService
from engine.social import hunting as hunt_rules
from test_camps import found_at, place

KEY = "6:0"
MINUTE = 60


def ids(view):
    return [a.id for a in view.actions]


def win(service, account):
    """Finish the current fight with a victory (the enemy is left at 1 health before each attack)."""
    view = None
    for _ in range(10):
        state = service.store.get("combat", account)
        if state is None:
            break
        state["enemy"]["hp"] = 1
        service.store.put("combat", account, state)
        hero = service._load(account)
        hero.hp = hero_stats(service._kit(hero), hero.level)["max_hp"]     # never fall while finishing it
        service._save(hero)
        view = service.act(account, "atk")
    assert view is not None and view.kind == "combat_end" and service.store.get("combat", account) is None
    return view


def wild(service):
    """A zone next to the Claro where hunting works (a biome with danger, not the lair)."""
    for x, y in ((1, 0), (0, 1), (-1, 0), (0, -1), (2, 0)):
        zone = service._zone(x, y)
        if service.content.biomes[zone.biome]["danger"] > 0 and not service._is_lair(x, y):
            return x, y
    raise AssertionError("no wild zone near the Claro")


def hunter(service, account="test:1", name="Lyra"):
    make_hero(service, account, name)
    x, y = wild(service)
    place(service, account, x, y)
    return x, y


def camp_with_members(service, clock):
    """test:1 founds a camp at 6:0; test:2 (same zone), test:3 (other zone) and test:5 (same zone, idle) are members;
    test:4 is in the same zone but is not a member. Everyone plays now except test:5, who played 20 minutes ago."""
    make_hero(service, "test:1", "Lyra")
    found_at(service, "test:1", 6, 0)
    for account, name in (("test:2", "Bram"), ("test:3", "Cora"), ("test:4", "Dax"), ("test:5", "Eris")):
        make_hero(service, account, name)
    camp = service.store.get("camp", KEY)
    camp["members"] += ["test:2", "test:3", "test:5"]
    service.store.put("camp", KEY, camp)
    place(service, "test:2", 6, 0, camp=KEY)
    place(service, "test:3", 7, 1, camp=KEY)
    place(service, "test:4", 6, 0)
    place(service, "test:5", 6, 0, camp=KEY)
    service.act("test:5", "hero")
    clock.advance(20 * MINUTE)
    for account in ("test:1", "test:2", "test:3", "test:4"):
        service.act(account, "hero")
    service.tick()                             # drop older pushes (founding, raids)


def test_pure_rules():
    assert hunt_rules.party_bonus(0, 0.1, 0.3) == 0.0
    assert abs(hunt_rules.party_bonus(2, 0.1, 0.3) - 0.2) < 1e-9
    assert hunt_rules.party_bonus(7, 0.1, 0.3) == 0.3                     # capped
    assert hunt_rules.party_target(1, 3, 2) == 6 and hunt_rules.party_target(4, 3, 2) == 12
    party = {"members": {"a": 0, "b": 0}, "prey": 0}
    for _ in range(5):
        hunt_rules.add_prey(party, "a")
    assert party["prey"] == 5 and not hunt_rules.reward_earned(party, 3, 2)
    hunt_rules.add_prey(party, "b")
    assert hunt_rules.reward_earned(party, 3, 2) and hunt_rules.rewarded(party) == ["a", "b"]
    party["members"]["c"] = 0                                             # joined and hunted nothing: no reward
    assert hunt_rules.rewarded(party) == ["a", "b"] and not hunt_rules.reward_earned(party, 3, 2)   # target is 9 now
    assert not hunt_rules.reward_earned({"members": {"a": 9}, "prey": 9}, 3, 2)                      # a party of one


def test_explore_menu_keeps_four_buttons_and_places_moved_to_the_map(service):
    hunter(service)
    menu = service.act("test:1", "explore_menu")
    assert ids(menu) == ["explore", "gather", "hunt", "map"]
    assert "🏹 Cazar" in [a.label for a in menu.actions]
    mapv = service.act("test:1", "map")
    # 📒 Lugares first and ↩️ Volver last; in between, at most a "goto:" to the nearest 🕳️ cave or 👹 camp you see (D-181:
    # with 2 or 3 entrances per stretch there can be one 2 zones from the Claro)
    assert ids(mapv)[0] == "places" and ids(mapv)[-1] == "explore_menu" and len(mapv.actions) <= 4
    assert all(i.startswith(("goto:", "recon")) for i in ids(mapv)[1:-1])
    places = service.act("test:1", "places")
    assert places.kind == "places" and ids(places)[-1] == "map"            # ↩️ Volver goes back to the map
    assert any(a.id == "goto:0:0" for a in places.actions)
    # The console numbers these same buttons: from the explore menu it still reaches the map, and from there Lugares.
    from adapters.cli import play
    assert "map" in [a.id for a in play.options(menu, service)] and "places" in [a.id for a in play.options(mapv, service)]
    assert not service.texts.missing


def test_hunt_starts_a_fight_with_a_zone_mob_and_costs_energy(service):
    x, y = hunter(service)
    before = service._load("test:1")
    screen = service.act("test:1", "hunt")
    assert screen.kind == "hunt" and ids(screen) == ["prey", "explore_menu"]     # no camp: no party button
    text = "\n".join(screen.body)
    cost = service.content.balance["hunt"]["energy"]
    assert cost == 2                                                       # D-108 (confirmed): 2 ⚡ per prey
    assert f"⚡{cost}" in text and "Por aquí rondan" in text and "Partida de caza" in text   # the hint to have a camp
    view = service.act("test:1", "prey")
    assert view.kind == "combat" and "🏹" in view.notice
    state = service.store.get("combat", "test:1")
    assert state["hunt"] == {"x": x, "y": y}
    zone = service._zone(x, y)
    assert state["enemy"]["id"] in [eid for eid, _ in service._zone_enemies(zone)]
    assert not service.content.enemies[state["enemy"]["id"]].get("boss")
    after = service._load("test:1")
    assert after.energy == before.energy - service.content.balance["hunt"]["energy"]
    assert after.exploration == before.exploration and after.backpack == before.backpack and after.activity is None
    assert not service.texts.missing


def test_a_won_hunt_gives_only_combat_rewards_and_offers_another_prey(service):
    x, y = hunter(service)
    service.act("test:1", "prey")
    before = service._load("test:1")
    enemy = service.content.enemies[service.store.get("combat", "test:1")["enemy"]["id"]]
    end = win(service, "test:1")
    after = service._load("test:1")
    assert ids(end) == ["prey", "home"] and "🏹 Otra presa" in [a.label for a in end.actions]
    assert after.kills == before.kills + 1 and after.xp > before.xp
    assert after.exploration == before.exploration                     # no exploration %
    allowed = set(enemy.get("loot", {})) | set(before.backpack)
    gathered = {"madera", "piedra", "fibra", "arcilla"} - set(enemy.get("loot", {}))
    for item_id, count in after.backpack.items():
        item = service.content.items[item_id]
        assert item_id in allowed or item.get("kind") == "gear", item_id    # only loot and gear, never resources
        assert item_id not in gathered or count == before.backpack.get(item_id, 0)
    again = service.act("test:1", "prey")
    assert again.kind == "combat" and service._load("test:1").energy == before.energy - service.content.balance["hunt"]["energy"]
    assert not service.texts.missing


def test_hunting_is_blocked_downed_busy_without_energy_in_the_claro_and_in_the_lair(service):
    x, y = hunter(service)
    energy = service._load("test:1").energy
    # Downed: heal first (no energy spent, no fight).
    place(service, "test:1", x, y, downed=True, hp=1)
    view = service.act("test:1", "hunt")
    assert view.kind == "hunt" and "malherido" in view.notice
    view = service.act("test:1", "prey")
    assert view.kind == "hunt" and "malherido" in view.notice
    assert service.store.get("combat", "test:1") is None and service._load("test:1").energy == energy
    # Busy exploring: the usual "busy" answer.
    place(service, "test:1", x, y, downed=False)
    service.act("test:1", "do:explore:5")
    view = service.act("test:1", "prey")
    assert view.kind == "activity" and view.notice == service.texts.t("activity.busy")
    assert service.store.get("combat", "test:1") is None
    service.act("test:1", "stop")
    # Not enough energy for a prey (1 is enough to explore, not to hunt).
    place(service, "test:1", x, y, energy=1)
    view = service.act("test:1", "prey")
    assert view.kind == "hunt" and "⚡" in view.notice and "cazar, 2" in view.notice
    assert service.store.get("combat", "test:1") is None and service._load("test:1").energy == 1
    # The Claro has no prey.
    place(service, "test:1", 0, 0, energy=10)
    view = service.act("test:1", "hunt")
    assert view.kind == "explore_menu" and view.notice == service.texts.t("hunt.no_prey")
    assert service.act("test:1", "prey").kind == "explore_menu" and service.store.get("combat", "test:1") is None
    # The lair: only the Guardian (its button stays; no 🏹 Cazar).
    cfg = service.content.balance["guardian"]
    place(service, "test:1", cfg["x"], cfg["y"])
    menu = service.act("test:1", "explore_menu")
    assert ids(menu) == ["explore", "boss", "map"]
    view = service.act("test:1", "prey")
    assert view.kind == "explore_menu" and view.notice == service.texts.t("hunt.lair")
    assert service.store.get("combat", "test:1") is None and service._load("test:1").energy == 10
    assert not service.texts.missing


def test_no_other_prey_button_without_energy(service):
    x, y = hunter(service)
    cost = service.content.balance["hunt"]["energy"]
    place(service, "test:1", x, y, energy=cost + 1)                       # one prey, then less than a prey left
    service.act("test:1", "prey")
    end = win(service, "test:1")
    assert ids(end) == ["home"]


def test_party_tells_only_active_members_in_the_same_zone(service, clock):
    camp_with_members(service, clock)
    screen = service.act("test:1", "hunt")
    assert screen.kind == "hunt" and ids(screen) == ["prey", "huntparty", "explore_menu"]
    view = service.act("test:1", "huntparty")
    assert view.notice == service.texts.t("hunt.party_called", n=1)
    party = service.store.get("hunt_party", KEY)
    assert party["members"] == {"test:1": 0} and (party["x"], party["y"]) == (6, 0)
    assert party["until"] - party["at"] == 30 * MINUTE
    pushes = [(account, v) for account, v in service.tick() if v.kind == "hunt_party"]
    assert [account for account, _ in pushes] == ["test:2"]             # not test:3 (elsewhere), test:4 (no member), test:5 (idle)
    notice = pushes[0][1]
    assert ids(notice) == ["huntjoin"] and "Lyra" in "\n".join(notice.body)
    # Joining: only members, only from the party's zone.
    assert service.act("test:4", "huntjoin").notice == service.texts.t("hunt.party_no_camp")
    assert "ve allá" in service.act("test:3", "huntjoin").notice
    service.act("test:2", "do:explore:5")                                 # joining works while exploring there
    view = service.act("test:2", "huntjoin")
    assert view.kind == "activity" and "Te uniste" in view.notice
    assert service.store.get("hunt_party", KEY)["members"] == {"test:1": 0, "test:2": 0}
    service.act("test:2", "stop")
    view = service.act("test:2", "hunt")
    assert view.kind == "hunt" and "huntjoin" not in ids(view) and "huntparty" not in ids(view)
    # A second call while it lasts does not open another one.
    assert service.act("test:2", "huntparty").notice == service.texts.t("hunt.party_member")
    assert not service.texts.missing


def test_party_bonus_tally_and_lazy_end_with_report(service, clock):
    camp_with_members(service, clock)
    service.act("test:1", "huntparty")
    service.act("test:2", "huntjoin")
    service.tick()
    # test:1 hunts with test:2 present: +10 % experience.
    service.act("test:1", "prey")
    state = service.store.get("combat", "test:1")
    edef = service.content.enemies[state["enemy"]["id"]]
    expected = int(service._zone_xp(edef["xp"], state["enemy"]["level"]) * 1.0 * 1.1)    # D-108 scaling, +10 % (D-106)
    xp_before = service._load("test:1").xp
    end = win(service, "test:1")
    assert service._load("test:1").xp - xp_before == expected
    text = "\n".join(end.body)
    assert "1/6" in text and "+10 %" in text
    assert ids(end) == ["prey", "home"]                                  # already in the party: no party button
    # test:4 (not a member) hunts in the same zone: no bonus, no tally.
    service.act("test:4", "prey")
    state = service.store.get("combat", "test:4")
    edef = service.content.enemies[state["enemy"]["id"]]
    plain = int(service._zone_xp(edef["xp"], state["enemy"]["level"]) * 1.0)
    xp_before = service._load("test:4").xp
    end = win(service, "test:4")
    assert service._load("test:4").xp - xp_before == plain and "Partida" not in "\n".join(end.body)
    service.act("test:2", "prey")
    win(service, "test:2")
    party = service.store.get("hunt_party", KEY)
    assert party["prey"] == 2 and party["members"] == {"test:1": 1, "test:2": 1}
    # The screen shows the party and the bonus now.
    screen = service.act("test:1", "hunt")
    assert any("2/6" in line for line in screen.body) and any("+10 %" in line for line in screen.body)
    # The window ends: nothing happens until a camp member plays (lazy clock); a stranger does not close it.
    clock.advance(31 * MINUTE)
    service.act("test:4", "hero")
    assert service.store.get("hunt_party", KEY) is not None
    service.act("test:2", "hero")
    assert service.store.get("hunt_party", KEY) is None
    reports = [(account, v) for account, v in service.tick() if v.kind == "hunt_party_end"]
    assert sorted(account for account, _ in reports) == ["test:1", "test:2"]
    body = "\n".join(reports[0][1].body)
    assert "2 presas" in body and "Lyra 1" in body and "Bram 1" in body and "No llegaron a la meta" in body
    # After it ended, a hunt does not count for any party.
    service.act("test:1", "prey")
    end = win(service, "test:1")
    assert "Partida" not in "\n".join(end.body) and "huntparty" in ids(end)
    assert not service.texts.missing


def test_party_reward_when_the_goal_is_reached(service, clock):
    camp_with_members(service, clock)
    service.act("test:1", "huntparty")
    party = service.store.get("hunt_party", KEY)
    party["members"] = {"test:1": 6, "test:2": 3, "test:5": 0}            # target = 3 × 3 = 9
    party["prey"] = 9
    service.store.put("hunt_party", KEY, party)
    reward = service.content.balance["hunt"]["party"]["reward"]
    gold = {a: service._load(a).gold for a in ("test:1", "test:2", "test:5")}
    xp = {a: service._load(a).xp for a in ("test:1", "test:2", "test:5")}
    clock.advance(31 * MINUTE)
    service.act("test:1", "hero")                                          # the actor is paid in memory and saved
    assert service.store.get("hunt_party", KEY) is None
    for account in ("test:1", "test:2"):
        assert service._load(account).gold == gold[account] + reward["gold"]
        assert service._load(account).xp == xp[account] + reward["xp"]
    assert service._load("test:5").gold == gold["test:5"] and service._load("test:5").xp == xp["test:5"]   # joined, hunted nothing
    reports = {account: v for account, v in service.tick() if v.kind == "hunt_party_end"}
    assert set(reports) == {"test:1", "test:2", "test:5"}
    assert "Meta cumplida" in "\n".join(reports["test:5"].body)
    # A party of one never gets the reward, even with many prey.
    service.act("test:1", "huntparty")
    party = service.store.get("hunt_party", KEY)
    party["members"], party["prey"] = {"test:1": 12}, 12
    service.store.put("hunt_party", KEY, party)
    gold_now = service._load("test:1").gold
    clock.advance(31 * MINUTE)
    service.act("test:1", "hero")
    assert service._load("test:1").gold == gold_now
    reports = [v for account, v in service.tick() if v.kind == "hunt_party_end"]
    assert reports and "al menos 2 cazadores" in "\n".join(reports[0].body)
    assert not service.texts.missing


def test_party_needs_a_camp_a_huntable_zone_and_a_healthy_hero(service, clock):
    camp_with_members(service, clock)
    view = service.act("test:4", "huntparty")                             # test:4 has no camp
    assert view.notice == service.texts.t("hunt.party_no_camp") and "huntparty" not in ids(view)
    place(service, "test:1", 0, 0)                                         # a member in the Claro: no prey there
    view = service.act("test:1", "huntparty")
    assert view.kind == "explore_menu" and view.notice == service.texts.t("hunt.no_prey")
    place(service, "test:1", 6, 0, downed=True, hp=1)                     # downed: heal first
    view = service.act("test:1", "huntparty")
    assert view.kind == "hunt" and "malherido" in view.notice
    assert service.store.get("hunt_party", KEY) is None
    assert not [v for _, v in service.tick() if v.kind == "hunt_party"]
    assert not service.texts.missing


def test_old_saves_without_hunting_data_load_fine(service):
    make_hero(service)
    for screen in ("home", "explore_menu", "hero", "map", "places"):
        assert service.act("test:1", screen).kind
    assert service.store.get("hunt_party", "0:0") is None


def _build(content, path):
    clock = FixedClock()
    service = GameService(content, MemoryStore(), clock, world_seed=12345)
    camp_with_members(service, clock)
    view = service.view("test:1")
    for action in path:
        view = service.act("test:1", action)
    return service, view


def test_hunt_screens_have_at_most_four_buttons_and_no_missing_texts(content):
    seen, queue = set(), deque([["hunt"], ["huntparty"], ["explore_menu"]])
    while queue:
        path = queue.popleft()
        service, view = _build(content, path)
        assert len(view.actions) <= (6 if view.kind == "combat" else 4), (path, view.kind)
        assert not service.texts.missing, (path, service.texts.missing)
        for _, pushed in service.tick():
            assert len(pushed.actions) <= 4 and all(len(a.id.encode()) <= 64 for a in pushed.actions)
        key = (view.kind, tuple(a.id for a in view.actions))
        if key in seen:
            continue
        seen.add(key)
        for action in view.actions:
            if len(path) < 4 and not action.id.startswith(("go:", "goto:", "explore", "gather", "sellg:", "ab:", "flee", "dodge", "use:")):
                queue.append(path + [action.id])
    kinds = {k for k, _ in seen}
    assert {"hunt", "combat", "explore_menu", "map"} <= kinds
    # A won hunt with a camp and no party: [🏹 Otra presa] [🏹 Partida de caza] [▶️ Continuar].
    service, _ = _build(content, ["prey"])
    end = win(service, "test:1")
    assert ids(end) == ["prey", "huntparty", "home"]
