"""The first region Guardian (D-82): lair, button, phases, no flee, Memento, wait to repeat, Pioneer.

[ES] Pruebas del Guardián del Claro (Raigambre): aparece en su guarida, el botón se ve, las fases
cambian, no se puede huir, la primera victoria da el Recuerdo, hay espera para repetir y el aviso
al servidor del primer vencedor sale una sola vez.
"""

from conftest import make_hero
from engine.combat import find_move, make_combat, phase_for, phase_moves, resolve_round, validate_choice
from engine.core import BossDefeated, Rng
from engine.world import zone_at


def _cfg(service):
    return service.content.balance["guardian"]


def _to_lair(service, account="test:1"):
    """Put the hero in the lair, as if it had walked there."""
    cfg = _cfg(service)
    hero = service._load(account)
    hero.x, hero.y = cfg["x"], cfg["y"]
    hero.remember(cfg["x"], cfg["y"])
    service._save(hero)
    service.store.put("zone", f"{cfg['x']}:{cfg['y']}", {"discovered_by": hero.name, "at": 0})
    return hero


def _win_guardian(service, account="test:1"):
    """Challenge the Guardian and land the last blow."""
    view = service.act(account, "boss")
    assert view.kind == "combat"
    state = service.store.get("combat", account)
    state["enemy"]["hp"] = 1
    service.store.put("combat", account, state)
    return service.act(account, "atk")


def test_lair_is_fixed_near_but_not_next_to_the_claro(service):
    cfg = _cfg(service)
    edef = service.content.enemies[cfg["enemy"]]
    assert 4 <= max(abs(cfg["x"]), abs(cfg["y"])) <= 6
    assert edef["boss"] and not edef["biomes"] and edef["level_min"] == edef["level_max"]
    assert service._zone(cfg["x"], cfg["y"]).biome == cfg["biome"]
    # Same place for every world seed (only the biome is forced; the coordinates are fixed in balance.yaml).
    assert zone_at(1, cfg["x"], cfg["y"]).lejania == zone_at(999, cfg["x"], cfg["y"]).lejania


def test_lair_screen_shows_the_guardian_and_the_button(service):
    make_hero(service)
    _to_lair(service)
    zone = service.act("test:1", "home")
    text = "\n".join(zone.body)
    assert service._guardian_name() in text and "Pionero" in text
    menu = service.act("test:1", "explore_menu")
    ids = [a.id for a in menu.actions]
    assert "boss" in ids and len(menu.actions) <= 4
    assert "⚔️ Desafiar al Guardián" in [a.label for a in menu.actions]
    energy = service._load("test:1").energy
    service.act("test:1", "gather")                 # no gathering in the lair, and no energy spent
    assert service._load("test:1").activity is None and service._load("test:1").energy == energy
    assert not service.texts.missing


def test_map_and_places_show_the_lair_once_discovered(service):
    make_hero(service)
    cfg = _cfg(service)
    before = "\n".join(service.act("test:1", "places").body)     # D-223 (0.30.2): 📒 Lugares lists the important places
    assert "👑" not in before
    _to_lair(service)
    hero = service._load("test:1")
    hero.x, hero.y = 0, 0
    service._save(hero)
    assert "👑" not in "\n".join(service.act("test:1", "map").body)        # the map draws nothing but you and the 🔥
    places = service.act("test:1", "places")
    assert any(a.id == f"goask:{cfg['x']}:{cfg['y']}" for a in places.actions)   # asks first (D-223)
    assert service.act("test:1", f"goask:{cfg['x']}:{cfg['y']}").actions[0].id == f"goto:{cfg['x']}:{cfg['y']}"
    assert "👑" in "\n".join(places.body)


def test_no_button_away_from_the_lair(service):
    make_hero(service)
    menu = service.act("test:1", "explore_menu")
    assert "boss" not in [a.id for a in menu.actions]
    view = service.act("test:1", "boss")
    assert service.store.get("combat", "test:1") is None
    assert view.notice


def test_phases_change_moves_and_rage(content, service):
    eid = _cfg(service)["enemy"]
    edef = content.enemies[eid]
    make_hero(service)
    hero = service._load("test:1")
    kit = service._kit(hero)
    state = make_combat(eid, edef, edef["level_min"], kit, seed=11)
    enemy = state["enemy"]
    assert enemy["phase"] == 0 and enemy["next_move"] in [m["id"] for m in edef["moves"]]
    base_attack = enemy["attack"]
    # Drop to the first threshold: the announced move still lands, then the phase changes.
    enemy["hp"] = int(enemy["max_hp"] * edef["phases"][0]["at"]) - 1
    hero.hp = 10_000
    lines = resolve_round(state, hero, kit, {"type": "dodge"}, service.ctx)
    assert enemy["phase"] == 1
    assert abs(enemy["attack"] - base_attack * edef["phases"][0]["attack_mult"]) < 1e-6
    assert enemy["next_move"] in [m["id"] for m in phase_moves(edef, 1)]
    assert any("fase 2" in line for line in lines)
    # Second threshold: angrier.
    enemy["hp"] = int(enemy["max_hp"] * edef["phases"][1]["at"]) - 1
    resolve_round(state, hero, kit, {"type": "dodge"}, service.ctx)
    assert enemy["phase"] == 2 and enemy["attack"] > base_attack * edef["phases"][0]["attack_mult"]
    assert enemy["next_move"] in [m["id"] for m in phase_moves(edef, 2)]
    # Phases never go back, even if the boss heals.
    enemy["hp"] = enemy["max_hp"]
    resolve_round(state, hero, kit, {"type": "dodge"}, service.ctx)
    assert enemy["phase"] == 2
    assert phase_for(edef, enemy["max_hp"], enemy["max_hp"]) == 0


def test_phase_moves_have_texts_and_common_enemies_do_not_change(content, service):
    eid = _cfg(service)["enemy"]
    edef = content.enemies[eid]
    for phase in edef["phases"]:
        assert service.texts.has(f"enemy.{eid}.phases.{phase['id']}")
        for move in phase["moves"]:
            assert service.texts.has(f"enemy.{eid}.moves.{move['id']}.warn")
            same = find_move(edef, move["id"])
            assert same.get("power") == move.get("power") and same.get("tags") == move.get("tags")
    wolf = content.enemies["lobo_ceniciento"]
    assert phase_moves(wolf, 3) == wolf["moves"] and phase_for(wolf, 1, 100) == 0


def test_guardian_cannot_be_fled_dodge_instead(service):
    make_hero(service)
    _to_lair(service)
    view = service.act("test:1", "boss")
    ids = [a.id for a in view.actions]
    assert "flee" not in ids and "dodge" in ids and len(view.actions) <= 6
    assert any("fase 1 de 3" in line for line in view.body)
    state = service.store.get("combat", "test:1")
    hero = service._load("test:1")
    assert validate_choice(state, hero, service._kit(hero), {"type": "flee"}, service.ctx)
    after = service.act("test:1", "flee")
    assert service.store.get("combat", "test:1") is not None and after.notice


def test_guardian_never_appears_at_random(service):
    make_hero(service)
    hero = service._load("test:1")
    boss = _cfg(service)["enemy"]
    for x in range(-8, 9, 2):
        for y in range(-8, 9, 2):
            zone = service._zone(x, y)
            service._start_combat(hero, zone, Rng(x * 100 + y), "encounter.found")
            assert service.store.get("combat", hero.id)["enemy"]["id"] != boss
            service.store.delete("combat", hero.id)


def test_first_win_gives_memento_for_you(service):
    make_hero(service, class_id="mago_fuego")
    hero = _to_lair(service)
    hero.level = 6                      # the pieces ask for level 5
    service._save(hero)
    end = _win_guardian(service)
    assert end.kind == "combat_end" and end.title.startswith("🏆")
    hero = service._load("test:1")
    assert hero.backpack.get("recuerdo_raigambre") == 1
    assert hero.guardians["raigambre"]["wins"] == 1
    assert "memento" in [a.id for a in end.actions]
    memento = service.act("test:1", "memento")
    options = [a.id[4:] for a in memento.actions if a.id.startswith("mem:")]
    assert options == ["guardian_baston", "guardian_tela"] and len(memento.actions) <= 4
    picked = service.act("test:1", "mem:guardian_tela")
    hero = service._load("test:1")
    assert "recuerdo_raigambre" not in hero.backpack and hero.backpack.get("guardian_tela") == 1
    assert picked.kind == "item" and "equip:guardian_tela" in [a.id for a in picked.actions]
    # The Memento is spent: the other piece can no longer be taken.
    service.act("test:1", "mem:guardian_baston")
    assert "guardian_baston" not in service._load("test:1").backpack
    assert not service.texts.missing


def test_wait_before_challenging_again_and_repeat_rewards(service, clock):
    make_hero(service)
    _to_lair(service)
    _win_guardian(service)
    service.act("test:1", "home")
    blocked = service.act("test:1", "boss")
    assert service.store.get("combat", "test:1") is None and "Vuelve en" in (blocked.notice or "")
    assert "Vuelve en" in "\n".join(service.act("test:1", "explore_menu").body)
    clock.advance(_cfg(service)["cooldown_hours"] * 3600 + 1)
    gold = service._load("test:1").gold
    end = _win_guardian(service)
    hero = service._load("test:1")
    assert hero.guardians["raigambre"]["wins"] == 2
    assert hero.gold > gold and hero.backpack.get("recuerdo_raigambre") == 1   # no second Memento
    assert "memento" in [a.id for a in end.actions]                            # the unused one is still there


def test_pioneer_saved_forever_and_server_told_once(service):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram", "mago_fuego")
    events = []
    service.bus.subscribe(BossDefeated, events.append)
    _to_lair(service, "test:1")
    _win_guardian(service, "test:1")
    assert service.store.get("meta", "guardian:raigambre")["name"] == "Lyra"
    hero = service._load("test:1")
    assert hero.titles == ["pionero_raigambre"]
    assert "Pionero del Claro" in "\n".join(service.act("test:1", "hero").body)
    news = [v for acc, v in service.tick() if v.kind == "news"]
    assert len(news) == 1 and "Lyra" in news[0].body[0]
    assert events[-1].first_in_server and events[-1].first_win
    # A second hero wins: it gets its own Memento, but no title and no new news.
    _to_lair(service, "test:2")
    _win_guardian(service, "test:2")
    other = service._load("test:2")
    assert other.backpack.get("recuerdo_raigambre") == 1 and not other.titles
    assert not [v for acc, v in service.tick() if v.kind == "news"]
    assert service.store.get("meta", "guardian:raigambre")["name"] == "Lyra"
    assert not events[-1].first_in_server
    assert "Lyra" in "\n".join(service.act("test:2", "home").body)


def test_every_button_in_the_lair_works(content):
    """Like tests/test_buttons.py, but starting in the lair and with a won Memento (D-46, D-75)."""
    from collections import deque

    from engine.core import FixedClock, MemoryStore
    from engine.service import GameService

    def build(path):
        service = GameService(content, MemoryStore(), FixedClock(), world_seed=7)
        make_hero(service, "test:1", "Lyra", "paladin_reprension")
        hero = _to_lair(service)
        hero.backpack["recuerdo_raigambre"] = 1
        service._save(hero)
        view = service.view("test:1")
        for action in path:
            view = service.act("test:1", action)
        return service, view

    seen, queue = set(), deque([["explore_menu"], ["bag"]])
    while queue:
        path = queue.popleft()
        service, view = build(path)
        assert len(view.actions) <= (6 if view.kind == "combat" else 4), (path, view.kind)
        assert not service.texts.missing, (path, service.texts.missing)
        key = (view.kind, tuple(a.id for a in view.actions))
        if key in seen:
            continue
        seen.add(key)
        for action in view.actions:
            if len(path) < 4 and not action.id.startswith(("go:", "goto:", "explore", "gather", "sellg:")):
                queue.append(path + [action.id])
    kinds = {k for k, _ in seen}
    assert {"explore_menu", "combat", "memento", "item"} <= kinds
