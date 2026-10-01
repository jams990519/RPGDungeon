"""The 🧭 Explorador profession and the ⛺ enemy camps that move every day (D-112).

[ES] Pruebas del Explorador y de los campamentos enemigos: los campamentos salen cada día en zonas fijas para todos (semilla
del mundo + día), nunca en el Claro, la guarida ni el territorio de un campamento de jugadores, y al otro día cambian. En su
zona no se explora ni se recolecta (con aviso y sin gastar energía; un lote que cruza la medianoche se corta y devuelve la
vuelta). La guarnición se comparte: cada pelea vence a uno para todos y el jefe es élite. Al caer el jefe, el cofre es de
quien lo termina y cada uno que peleó gana su parte, una sola vez. Las peleas automáticas nunca pelean un campamento
(D-114). Infiltrarse pide rango 30, cuesta energía, revela la guarnición y el cofre, y si te descubren empieza una pelea.
Explorar sube el oficio, su beneficio suma puntos y el mapa muestra los campamentos según el rango. Ninguna pantalla pasa de
4 botones (6 en combate), ningún texto falta y los guardados de antes cargan.
"""

from collections import deque

import pytest

from conftest import make_hero
from engine.core import FixedClock, MemoryStore
from engine.hero import Hero
from engine.professions import rules as profession_rules
from engine.professions import xp_for_rank
from engine.service import GameService
from engine.world import enemy_camps as camp_rules
from test_camps import place
from test_hunt import win

DAY = 86400
MINUTE = 60


def ids(view):
    return [a.id for a in view.actions]


def rank_xp(service, rank):
    return xp_for_rank(service.content.balance["professions"]["rank_formula"], rank)


def camps_today(service, radius=9):
    return [(x, y) for x in range(-radius, radius + 1) for y in range(-radius, radius + 1) if service._ecamp_exists(x, y)]


def camp_zone(service):
    """The nearest standing enemy camp of today (the test seed always has some within 9 zones)."""
    found = sorted(camps_today(service), key=lambda p: (abs(p[0]) + abs(p[1]), p))
    assert found, "no enemy camp near the Claro today"
    return found[0]


def at_camp(service, account="test:1", name="Lyra", explorer_rank=1, **extra):
    """A hero standing in today's nearest enemy camp, tutorial done, full energy and life."""
    make_hero(service, account, name)
    x, y = camp_zone(service)
    hero = service._load(account)
    profs = {"explorador": rank_xp(service, explorer_rank)} if explorer_rank > 1 else {}
    place(service, account, x, y, energy=50, tutorial=len(service.content.balance["tutorial"]["steps"]),
          professions=profs, **extra)
    return x, y


def record(service, x, y):
    return service.store.get("enemy_camp", f"{service._today()}:{x}:{y}") or {}


def set_beaten(service, x, y, beaten):
    camp = service._ecamp(x, y)
    camp["beaten"] = beaten
    service._ecamp_save(camp)


# ---------------------------------------------------------------- pure rules

def test_pure_rules(content):
    seed = 12345
    hits = [(x, y) for x in range(-20, 21) for y in range(-20, 21) if camp_rules.has_camp(seed, 11, x, y, 0.03, 2)]
    assert hits and all(max(abs(x), abs(y)) >= 2 for x, y in hits)                          # never near the Claro
    assert hits == [(x, y) for x in range(-20, 21) for y in range(-20, 21) if camp_rules.has_camp(seed, 11, x, y, 0.03, 2)]
    assert 0.01 < len(hits) / (41 * 41) < 0.06                                               # ~3 % of the zones
    assert not any(camp_rules.has_camp(seed, 12, x, y, 0.03, 2) for x, y in hits)           # never two days in a row
    members = camp_rules.garrison(seed, 11, 4, 3, content.enemies, "bosque", 5, [4, 8])
    assert 4 <= len(members) <= 8 and members[-1]["chief"] and not any(m["chief"] for m in members[:-1])
    assert all(not content.enemies[m["id"]].get("boss") for m in members)
    assert members == camp_rules.garrison(seed, 11, 4, 3, content.enemies, "bosque", 5, [4, 8])
    cfg = content.balance["enemy_camps"]
    chest = camp_rules.chest(seed, 11, 4, 3, 5, {"madera": 1.0, "fibra": 0.5}, cfg["chest"])
    assert chest["coins"] == 5 * cfg["chest"]["coins_per_level"] and set(chest["items"]) <= {"madera", "fibra"}
    assert cfg["chest"]["materials"][0] <= sum(chest["items"].values()) <= cfg["chest"]["materials"][1]
    ecfg = content.balance["explorer"]
    assert camp_rules.sight(1, ecfg, 6) == 1 and camp_rules.sight(25, ecfg, 6) == 3 and camp_rules.sight(50, ecfg, 6) == 6
    inf = cfg["infiltrate"]
    assert camp_rules.detect_chance(30, inf, 30) == pytest.approx(0.45)
    assert camp_rules.detect_chance(100, inf, 30) == pytest.approx(0.10)
    assert camp_rules.detect_chance(30, inf, 30) > camp_rules.detect_chance(60, inf, 30)


# ---------------------------------------------------------------- placement

def test_daily_placement_is_the_same_for_everyone_and_moves_the_next_day(content, clock):
    one = GameService(content, MemoryStore(), clock, world_seed=12345)
    two = GameService(content, MemoryStore(), clock, world_seed=12345)
    today = camps_today(one)
    assert today and today == camps_today(two)                                               # same for all players
    for x, y in today:
        assert max(abs(x), abs(y)) >= 2 and not one._is_lair(x, y) and not one._territory(x, y)
    clock.advance(DAY)
    tomorrow = camps_today(one)
    assert tomorrow and tomorrow != today and not set(today) & set(tomorrow)                 # somewhere else


def test_never_in_the_claro_the_lair_or_a_player_camp(service):
    make_hero(service)
    for x, y in service._claro_zones():
        assert not service._ecamp_exists(x, y)
    cfg = service._guardian_cfg()
    assert not service._ecamp_exists(cfg["x"], cfg["y"])
    x, y = camp_zone(service)
    service.store.put("camp", f"{x}:{y}", {"name": "Roca", "founder": "Lyra", "founder_id": "test:1", "members": ["test:1"],
                                            "relations": {}, "asked": [], "x": x, "y": y, "zones": [[x, y]]})
    service.store.put("territory", f"{x}:{y}", {"camp": f"{x}:{y}"})
    assert not service._ecamp_exists(x, y)


# ---------------------------------------------------------------- blocked zone

def test_exploring_and_gathering_are_blocked_without_spending(service):
    x, y = at_camp(service)
    for action in ("explore", "gather", "do:explore:5", "do:gather:max", "amt:explore:0"):
        view = service.act("test:1", action)
        hero = service._load("test:1")
        assert view.kind == "explore_menu" and "campamento enemigo" in view.notice, action
        assert hero.energy == 50 and hero.activity is None, action
    menu = service.act("test:1", "explore_menu")
    assert ids(menu) == ["assault", "infiltrate", "hunt", "map"]
    assert any("campamento enemigo" in line.lower() for line in service.act("test:1", "home").body)
    assert not service.texts.missing


def test_arriving_shows_the_camp(service, clock):
    x, y = at_camp(service)
    place(service, "test:1", x - 1, y, energy=50, downed=False)
    service.act("test:1", "go:e")
    clock.advance(30 * MINUTE)
    view = service.act("test:1", "home")
    assert "campamento enemigo" in (view.notice or "")


def test_a_batch_that_crosses_midnight_into_a_new_camp_stops_and_gives_the_round_back(service, clock):
    make_hero(service)
    day = service._today()
    zones = [(x, y) for x in range(-9, 10) for y in range(-9, 10)
             if service._ecamp_exists(x, y, day + 1) and not service._ecamp_exists(x, y, day)]
    x, y = sorted(zones, key=lambda p: abs(p[0]) + abs(p[1]))[0]
    place(service, "test:1", x, y, energy=50, tutorial=len(service.content.balance["tutorial"]["steps"]))
    clock.advance((day + 1) * DAY - clock.now() - 5 * MINUTE)          # 5 minutes before midnight
    service.act("test:1", "do:explore:5")
    assert service._load("test:1").energy == 49
    clock.advance(11 * MINUTE)                                          # the first round ends after midnight
    view = service.act("test:1", "home")
    hero = service._load("test:1")
    assert hero.activity is None and hero.energy == 50 and hero.exploration.get(f"{x}:{y}", 0) == 0
    assert "se instaló" in view.notice


# ---------------------------------------------------------------- the shared garrison

def test_the_garrison_is_shared_between_players(service):
    x, y = at_camp(service, "test:1", "Lyra")
    at_camp(service, "test:2", "Bram")
    camp = service._ecamp(x, y)
    view = service.act("test:1", "assault")
    state = service.store.get("combat", "test:1")
    assert view.kind == "combat" and state["enemy_camp"]["chief"] is False and state["enemy"]["id"] == camp["garrison"][0]["id"]
    assert service._load("test:1").energy == 50 - service.content.balance["enemy_camps"]["fight_energy"]
    end = win(service, "test:1")
    assert record(service, x, y)["beaten"] == 1 and "assault" in ids(end)                    # ⚔️ Seguir asaltando
    menu = service.act("test:2", "explore_menu")
    assert any("vencieron a 1" in line for line in menu.body)
    service.act("test:2", "assault")
    assert service.store.get("combat", "test:2")["enemy"]["id"] == camp["garrison"][1]["id"]
    win(service, "test:2")
    rec = record(service, x, y)
    assert rec["beaten"] == 2 and set(rec["fighters"]) == {"test:1", "test:2"}


def test_the_chief_is_an_elite_and_only_falls_in_its_own_fight(service):
    from engine.combat import make_combat
    x, y = at_camp(service)
    camp = service._ecamp(x, y)
    last = len(camp["garrison"]) - 1
    set_beaten(service, x, y, last)
    service.act("test:1", "assault")
    state = service.store.get("combat", "test:1")
    chief = camp["garrison"][-1]
    plain = make_combat(chief["id"], service.content.enemies[chief["id"]], chief["level"], service._kit(service._load("test:1")), 1)
    cfg = service.content.balance["enemy_camps"]
    assert state["enemy_camp"]["chief"] and state["enemy"]["max_hp"] == round(plain["enemy"]["max_hp"] * cfg["chief_hp_mult"])
    assert state["enemy"]["attack"] == pytest.approx(plain["enemy"]["attack"] * cfg["chief_attack_mult"])
    assert any("Jefe del campamento" in line for line in service._combat_view(service._load("test:1"), state).body)
    # a guard fight that ends after the guards are gone never brings the chief down
    service.store.delete("combat", "test:1")
    hero = service._load("test:1")
    lines = service._ecamp_fight_done(hero, {"enemy_camp": {"day": camp["day"], "x": x, "y": y, "chief": False}, "outcome": "victory"})
    assert record(service, x, y)["beaten"] == last and not record(service, x, y).get("destroyed")
    assert any("solo falta el jefe" in line for line in lines)


def test_destroying_the_camp_pays_the_finisher_and_everyone_who_fought_once(service):
    x, y = at_camp(service, "test:1", "Lyra")
    at_camp(service, "test:2", "Bram")
    service.act("test:2", "assault")
    win(service, "test:2")                                              # Bram fought here today
    service.tick()
    camp = service._ecamp(x, y)
    set_beaten(service, x, y, len(camp["garrison"]) - 1)
    lyra, bram = service._load("test:1"), service._load("test:2")
    service.act("test:1", "assault")
    end = win(service, "test:1")
    rec = record(service, x, y)
    assert rec["destroyed"]["by"] == "test:1"
    cfg = service.content.balance["enemy_camps"]
    chest = service._ecamp_chest(camp)
    after = service._load("test:1")
    assert after.gold >= lyra.gold + chest["coins"] and any("cofre" in line for line in end.body)
    for item, n in chest["items"].items():
        assert after.backpack.get(item, 0) >= lyra.backpack.get(item, 0) + n
    share = int(camp["level"] * cfg["share"]["coins_per_level"])
    assert service._load("test:2").gold == bram.gold + share and service._load("test:2").xp > bram.xp
    pushes = [view for acc, view in service.tick() if acc == "test:2"]
    assert len(pushes) == 1 and pushes[0].kind == "ecamp_news"
    assert any(entry["k"] == "enemy_camp" for entry in after.journal)
    # once: the camp is gone for the day, nothing is paid again, and the zone is explorable again
    assert service._ecamp_standing(x, y) is None
    assert service.act("test:2", "assault").notice and service._load("test:2").gold == bram.gold + share
    menu = service.act("test:1", "explore_menu")
    assert "explore" in ids(menu) and any("cayó hoy" in line for line in menu.body)
    assert service._ecamp_fight_done(service._load("test:2"), {"enemy_camp": {"day": camp["day"], "x": x, "y": y, "chief": True},
                                                                "outcome": "victory"})[-1].startswith("⛺ Lyra")
    assert service._load("test:2").gold == bram.gold + share
    assert not service.texts.missing


def test_camps_come_back_somewhere_else_the_next_day(service, clock):
    x, y = at_camp(service)
    camp = service._ecamp(x, y)
    set_beaten(service, x, y, len(camp["garrison"]) - 1)
    service.act("test:1", "assault")
    win(service, "test:1")
    assert service._ecamp_standing(x, y) is None
    clock.advance(DAY)
    assert not service._ecamp_exists(x, y) and camps_today(service)                          # elsewhere, never the same zone
    view = service.act("test:1", "explore_menu")
    assert "explore" in ids(view)


# ---------------------------------------------------------------- never automatic (D-114)

def test_automatic_fights_never_fight_an_enemy_camp(service):
    at_camp(service)
    service.act("test:1", "opt:fights")
    assert service._load("test:1").options["fights"] == "auto"
    service.act("test:1", "assault")
    hero = service._load("test:1")
    activity = {"kind": "explore", "done": 1, "left": 3, "got": {}, "log": [], "until": 0}
    lines = service._batch_fight(hero, activity, "aviso")
    assert lines is not None and service.store.get("combat", "test:1") is not None          # the fight waits for the player
    assert not activity.get("fights")


# ---------------------------------------------------------------- infiltration

def test_infiltration_needs_rank_30_and_costs_nothing_if_refused(service):
    x, y = at_camp(service)
    view = service.act("test:1", "infiltrate")
    assert "rango 30" in view.notice and service._load("test:1").energy == 50
    menu = service.act("test:1", "explore_menu")
    assert "(rango 30)" in menu.actions[1].label


def test_infiltration_reveals_the_camp_and_gives_exploration(service, monkeypatch):
    monkeypatch.setattr(camp_rules, "detect_chance", lambda *args: 0.0)
    x, y = at_camp(service, explorer_rank=30)
    before = service._load("test:1")
    view = service.act("test:1", "infiltrate")
    hero = service._load("test:1")
    cfg = service.content.balance["enemy_camps"]["infiltrate"]
    assert view.kind == "ecamp_intel" and len(view.actions) <= 4
    assert hero.energy == 50 - cfg["energy"] and hero.id in record(service, x, y)["scouted"]
    assert hero.exploration[f"{x}:{y}"] == cfg["explore_points"]
    assert hero.professions["explorador"] >= before.professions["explorador"] + cfg["explorer_xp"]
    assert any(line.startswith("👹 Quedan") for line in view.body) and any(line.startswith("👑 Jefe") for line in view.body)
    assert any(line.startswith("🎁 Cofre") for line in view.body)
    menu = service.act("test:1", "explore_menu")
    assert any(line.startswith("👹 Quedan") for line in menu.body)                            # it knows for the rest of the day
    again = service.act("test:1", "infiltrate")
    assert "Ya te infiltraste" in again.notice and service._load("test:1").energy == hero.energy
    assert not service.texts.missing


def test_being_detected_starts_a_manual_fight(service, monkeypatch):
    monkeypatch.setattr(camp_rules, "detect_chance", lambda *args: 1.0)
    x, y = at_camp(service, explorer_rank=30)
    view = service.act("test:1", "infiltrate")
    state = service.store.get("combat", "test:1")
    assert view.kind == "combat" and state["enemy_camp"]["x"] == x and "descubrieron" in view.notice
    assert "test:1" not in record(service, x, y).get("scouted", [])
    win(service, "test:1")
    assert record(service, x, y)["beaten"] == 1


# ---------------------------------------------------------------- the 🧭 Explorador

def test_exploring_raises_the_explorer_and_its_perk_adds_points(content):
    def one_round(rank):
        clock = FixedClock()
        service = GameService(content, MemoryStore(), clock, world_seed=12345)
        make_hero(service)
        x, y = 1, 0
        assert not service._ecamp_exists(x, y)
        profs = {"explorador": rank_xp(service, rank)} if rank > 1 else {}
        place(service, "test:1", x, y, energy=50, professions=profs, tutorial=len(content.balance["tutorial"]["steps"]))
        service.act("test:1", "do:explore:5")
        clock.advance(10 * MINUTE)
        service.act("test:1", "home")
        return service._load("test:1"), service

    novice, service = one_round(1)
    master, _ = one_round(100)
    cfg = content.balance["explorer"]
    assert novice.professions["explorador"] == cfg["xp_per_step"]
    assert master.exploration["1:0"] - novice.exploration["1:0"] == 5                         # +5 points at rank 100
    perks = profession_rules.perks(content.professions["professions"], {"explorador": 50}, 100, None, None, None)
    assert perks["explore"] == pytest.approx(2.5)
    view = service.act("test:1", "oficios")
    assert any("Explorador" in line for line in view.body) and any("🗺️" in line for line in view.body)
    assert any("En rango 10" in line for line in view.body)


def test_rank_thresholds_are_announced_and_rank_100_gives_the_title(service):
    make_hero(service)
    hero = service._load("test:1")
    hero.professions = {"explorador": rank_xp(service, 10) - 1}
    lines = service._prof_gain(hero, "explorador", 5)
    assert any("📒 Lugares" in line for line in lines)
    hero.professions = {"explorador": rank_xp(service, 100) - 1}
    lines = service._prof_gain(hero, "explorador", 5)
    assert "gran_explorador" in hero.titles and any("Gran Explorador" in line for line in lines)
    assert not service.texts.missing


def test_the_map_shows_camps_by_explorer_rank(service):
    make_hero(service)
    cx, cy = camp_zone(service)

    def map_lines(rank, dx):
        profs = {"explorador": rank_xp(service, rank)} if rank > 1 else {}
        place(service, "test:1", cx + dx, cy, professions=profs)
        return service.act("test:1", "map").body

    mark = f"⛺ ({cx}, {cy})"
    assert any(line.startswith(mark) for line in map_lines(1, 1))                         # next door: everyone sees it
    assert not any(line.startswith(mark) for line in map_lines(1, 3))                     # 3 zones away: not without rank
    assert not any(line.startswith(mark) and "⏱️" in line for line in map_lines(1, 1))
    assert any(line.startswith(mark) and "⏱️" in line for line in map_lines(10, 1))        # rank 10: travel time
    assert any(line.startswith(mark) for line in map_lines(25, 3))                        # rank 25: 3 zones
    assert not any(line.startswith(mark) for line in map_lines(25, 5))
    assert any(line.startswith(mark) for line in map_lines(50, 5))                        # rank 50: the whole map
    assert not any(line.startswith(mark) and "👹" in line for line in map_lines(50, 5))
    assert any(line.startswith(mark) and "👹" in line for line in map_lines(75, 5))        # rank 75: its strength
    view = service.act("test:1", "map")
    assert len(view.actions) <= 4 and any(a.id == f"goto:{cx}:{cy}" for a in view.actions)
    service.act("test:1", f"goto:{cx}:{cy}")
    assert service._load("test:1").activity["kind"] == "travel"
    assert not service.texts.missing


def test_places_lists_more_from_explorer_rank_10(service):
    make_hero(service)
    known = ["0:0"] + [f"{x}:0" for x in range(1, 11)]
    place(service, "test:1", 0, 0, known=known)
    assert sum(1 for line in service.act("test:1", "places").body if "zonas" in line) == 3
    place(service, "test:1", 0, 0, known=known, professions={"explorador": rank_xp(service, 10)})
    view = service.act("test:1", "places")
    assert sum(1 for line in view.body if "zonas" in line) == service.content.balance["explorer"]["places_listed"]
    assert len(view.actions) <= 4


# ---------------------------------------------------------------- screens, texts and old saves

def test_every_camp_screen_keeps_four_buttons_and_its_texts(content, monkeypatch):
    monkeypatch.setattr(camp_rules, "detect_chance", lambda *args: 0.0)

    def build(path):
        service = GameService(content, MemoryStore(), FixedClock(), world_seed=12345)
        at_camp(service, explorer_rank=100)
        view = service.act("test:1", "explore_menu")
        for action in path:
            view = service.act("test:1", action)
        return service, view

    seen, queue, kinds = set(), deque([[]]), set()
    while queue and len(seen) < 60:
        path = queue.popleft()
        service, view = build(path)
        limit = 6 if view.kind == "combat" else 4
        assert len(view.actions) <= limit, (path, view.kind, ids(view))
        assert not service.texts.missing, (path, service.texts.missing)
        kinds.add(view.kind)
        key = (view.kind, tuple(ids(view)))
        if key in seen or len(path) >= 3:
            continue
        seen.add(key)
        for action_id in ids(view):
            if not action_id.startswith(("go:", "goto:", "do:", "ab:", "use:")):
                queue.append(path + [action_id])
    assert {"explore_menu", "ecamp_intel", "combat", "map"} <= kinds


def test_old_saves_load_and_old_fights_still_end(service):
    make_hero(service)
    data = service.store.get("hero", "test:1")
    data.pop("professions", None)
    data.pop("titles", None)
    service.store.put("hero", "test:1", data)
    for screen in ("home", "explore_menu", "map", "places", "oficios", "hero"):
        assert service.act("test:1", screen).kind
    hero = Hero.from_dict(service.store.get("hero", "test:1"))
    assert hero.professions.get("explorador", 0) == 0
    place(service, "test:1", 1, 0)
    service.act("test:1", "hunt")
    service.act("test:1", "prey")                                       # a fight without the enemy_camp mark
    assert "enemy_camp" not in service.store.get("combat", "test:1")
    win(service, "test:1")
    assert not service.texts.missing
