"""🔭 Reconnaissance from afar and 🥷 stealth of the 🧭 Explorador (D-172).

[ES] Pruebas del reconocimiento y del sigilo. 🔭 Reconocer se abre al rango 10 de Explorador y llega a 1 zona (2 al 30, 3 al 50),
nunca a tu propia zona; cuesta 2 ⚡, da experiencia de Explorador, de héroe y unas monedas, y se hace una vez por lugar y día
(al otro día, otra vez). Muestra lo mismo que vería cualquiera ese día: la familia y el jefe de una mazmorra (y el récord de la
profunda), la guarnición y el jefe de un campamento enemigo, sin su cofre y sin gastar la infiltración. Lo reconocido queda en el
🗺️ Mapa y en 📍 Zona. 🥷 Sigilo crece parejo con el rango (25 % al 100, más la 🕵️ Infiltrado, con tope), evita peleas al azar al
explorar con ✋ Manual y en la emboscada del viaje, y nunca en lotes automáticos, cacerías, asaltos, mazmorras, oleadas ni el
Guardián. Los héroes de antes cargan, ninguna pantalla pasa de 4 botones y ningún texto falta.
"""

import re
from collections import deque

import pytest

from conftest import make_hero
from engine.core import FixedClock, MemoryStore
from engine.hero import Hero
from engine.professions import xp_for_rank
from engine.service import GameService
from engine.world import enemy_camps as camp_rules
from test_boss import _to_lair
from test_camps import place
from test_enemy_camps import camp_zone
from test_hunt import win
from test_mazmorras import dungeon_zone
from test_options import ready
from test_raids import camp_at_level, open_raid

DAY = 86400
MINUTE = 60
SEED = 12345


def ids(view):
    return [a.id for a in view.actions]


def rank_xp(service, rank):
    return xp_for_rank(service.content.balance["professions"]["rank_formula"], rank)


def scout_at(service, x, y, rank, account="test:1", name="Lyra", known=None, **extra):
    """A hero (made if needed) standing at (x, y) with that 🧭 Explorador rank, full energy, tutorial done."""
    if service._load(account) is None:
        make_hero(service, account, name)
    profs = {"explorador": rank_xp(service, rank)} if rank > 1 else {}
    data = {"energy": 50, "tutorial": len(service.content.balance["tutorial"]["steps"]), "professions": profs,
            "known": known if known is not None else ["0:0", f"{x}:{y}"]}
    data.update(extra)
    place(service, account, x, y, **data)
    return service._load(account)


def report_facts(view):
    """The lines of a 🔭 report that say what is there (not the header, the reward or the status line)."""
    return [line for line in view.body if line.startswith(("Hoy la ocupan", "👑", "👹", "🕳️ Una", "🌀 Una", "👹 Un", "🎁", "🏆 El", "🏆 Hoy"))]


# ---------------------------------------------------------------- reach by rank

def test_reach_grows_with_explorer_rank(service):
    make_hero(service)
    reach = {}
    for rank in (1, 9, 10, 29, 30, 49, 50, 100):
        reach[rank] = service._recon_range(scout_at(service, 0, 0, rank))
    assert reach == {1: 0, 9: 0, 10: 1, 29: 1, 30: 2, 49: 2, 50: 3, 100: 3}
    ranks = service.content.balance["explorer"]["ranks"]
    assert (ranks["recon"], ranks["recon_far"], ranks["recon_wide"]) == (10, 30, 50)


def test_locked_before_rank_10_and_nothing_is_spent(service):
    cx, cy = camp_zone(service)
    scout_at(service, cx + 1, cy, 9)
    view = service.act("test:1", "recon")
    assert view.kind == "recon" and ids(view) == ["map"] and any("rango 10" in line for line in view.body)
    service.act("test:1", f"rcn:{cx}:{cy}")
    hero = service._load("test:1")
    assert hero.energy == 50 and service.store.get("recon", "test:1") is None
    assert service.commands()["/reconocer"] == "recon"
    assert not service.texts.missing


def test_out_of_reach_and_own_zone_are_refused_without_spending(service):
    cx, cy = camp_zone(service)
    scout_at(service, cx + 2, cy, 10)                                  # 2 zones away, reach 1
    view = service.act("test:1", f"rcn:{cx}:{cy}")
    assert view.notice and service._load("test:1").energy == 50
    scout_at(service, cx + 2, cy, 30)                                  # reach 2: now it is
    view = service.act("test:1", f"rcn:{cx}:{cy}")
    assert view.kind == "recon_report"
    scout_at(service, cx, cy, 100)                                     # standing there: that is 🕵️ or ⚔️, never 🔭
    assert all(a.id != f"rcn:{cx}:{cy}" for a in service.act("test:1", "recon").actions)
    before = service._load("test:1").energy
    assert service.act("test:1", f"rcn:{cx}:{cy}").notice and service._load("test:1").energy == before
    assert service.act("test:1", "rcn:nada").kind == "recon"           # a broken button just shows the screen


# ---------------------------------------------------------------- cost, rewards and once a day

def test_scouting_costs_energy_and_gives_explorer_xp_hero_xp_and_coins(service):
    cx, cy = camp_zone(service)
    hero = scout_at(service, cx + 1, cy, 10)
    camp = service._ecamp(cx, cy)
    before = (hero.energy, hero.professions["explorador"], hero.xp, hero.gold)
    view = service.act("test:1", f"rcn:{cx}:{cy}")
    after = service._load("test:1")
    cfg = service.content.balance["recon"]
    assert view.kind == "recon_report" and len(view.actions) <= 4
    assert after.energy == before[0] - cfg["energy"]
    assert after.professions["explorador"] == before[1] + cfg["explorer_xp"]
    assert after.xp == before[2] + cfg["hero_xp"]
    assert after.gold == before[3] + camp["level"] * cfg["coins_per_level"]
    assert f"goto:{cx}:{cy}" in ids(view) and ids(view)[-1] == "map"
    assert not service.texts.missing


def test_once_per_place_and_day(service, clock):
    cx, cy = camp_zone(service)
    scout_at(service, cx + 1, cy, 10)
    service.act("test:1", f"rcn:{cx}:{cy}")
    energy = service._load("test:1").energy
    again = service.act("test:1", f"rcn:{cx}:{cy}")
    assert "Ya reconociste" in again.notice and service._load("test:1").energy == energy
    assert f"rcn:{cx}:{cy}" not in ids(service.act("test:1", "recon"))
    assert any(line.startswith("✅ 👹") for line in service.act("test:1", "recon").body)
    # the next day the record is empty again (the camp moved: a dungeon can be scouted again)
    clock.advance(DAY)
    x, y = dungeon_zone(service, "small")
    scout_at(service, x + 1, y, 10)
    first = service.act("test:1", f"rcn:{x}:{y}")
    assert first.kind == "recon_report"
    clock.advance(DAY)
    assert service.act("test:1", f"rcn:{x}:{y}").kind == "recon_report"


def free_zone_next_to(service, x, y):
    """A zone next to (x, y) where you can explore and hunt: danger, no standing enemy camp, no protected land, no lair."""
    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
        if service.content.biomes[service._zone(nx, ny).biome]["danger"] > 0 and not service._ecamp_standing(nx, ny) \
                and not service._territory(nx, ny) and not service._is_lair(nx, ny):
            return nx, ny
    raise AssertionError("no free zone next to the target")


def test_scouting_works_during_a_batch_but_never_in_combat(service):
    x, y = dungeon_zone(service, "small")
    hx, hy = free_zone_next_to(service, x, y)
    scout_at(service, hx, hy, 10)
    assert service.act("test:1", "do:explore:5").kind == "activity"
    energy = service._load("test:1").energy
    view = service.act("test:1", f"rcn:{x}:{y}")
    hero = service._load("test:1")
    assert view.kind == "recon_report" and hero.activity and hero.activity["kind"] == "explore"   # instant: it never moves you
    assert hero.energy == energy - service.content.balance["recon"]["energy"] and (hero.x, hero.y) == (hx, hy)
    assert f"goto:{x}:{y}" not in ids(view)                                         # busy: no "go there" button
    scout_at(service, hx, hy, 10, activity=None, known=["0:0", f"{hx}:{hy}"])
    service.store.delete("recon", "test:1")
    service.act("test:1", "hunt")
    assert service.act("test:1", "prey").kind == "combat"
    assert service.act("test:1", "recon").kind == "combat"
    assert service.act("test:1", f"rcn:{x}:{y}").kind == "combat" and service.store.get("recon", "test:1") is None


# ---------------------------------------------------------------- what it shows

def test_a_dungeon_shows_the_same_for_everyone_and_what_you_find_there(service):
    x, y = dungeon_zone(service, "small")
    scout_at(service, x + 1, y, 10, "test:1", "Lyra")
    scout_at(service, x - 1, y, 10, "test:2", "Bram")
    one = service.act("test:1", f"rcn:{x}:{y}")
    two = service.act("test:2", f"rcn:{x}:{y}")
    facts = report_facts(one)
    assert facts == report_facts(two)
    info = service._dng_today(x, y)
    family = service._dng_family_label(info["family"])
    assert any(family in line for line in facts) and any(service._dng_enemy(info["boss"]) in line for line in facts)
    assert any(line.startswith("🕳️ Una") for line in facts) and any(line.startswith("🎁") for line in facts)
    scout_at(service, x, y, 10, "test:3", "Cira")                       # who walks in sees that family and that boss
    screen = service.act("test:3", "dungeon")
    assert any(family in line for line in screen.body) and any(service._dng_enemy(info["boss"]) in line for line in screen.body)


def test_a_deep_dungeon_shows_the_record_to_beat(service):
    x, y = dungeon_zone(service, "deep")
    scout_at(service, x + 1, y, 10)
    service._dng_top_save(Hero(id="other", name="Bram", class_id="guerrero"), x, y, service._today(), 7)
    view = service.act("test:1", f"rcn:{x}:{y}")
    assert any(line.startswith("🌀 Una") for line in view.body)
    assert any("Bram" in line and "piso 7" in line for line in view.body)
    assert not service.texts.missing


def test_a_camp_shows_garrison_and_chief_not_the_chest_and_infiltration_stays(service, monkeypatch):
    cx, cy = camp_zone(service)
    scout_at(service, cx + 1, cy, 30, "test:1", "Lyra")
    scout_at(service, cx - 1, cy, 30, "test:2", "Bram")
    one = service.act("test:1", f"rcn:{cx}:{cy}")
    assert report_facts(one) == report_facts(service.act("test:2", f"rcn:{cx}:{cy}"))
    assert any(line.startswith("👹 Quedan") for line in one.body) and any(line.startswith("👑 Jefe") for line in one.body)
    assert not any(line.startswith("🎁") for line in one.body)                      # the chest is for 🕵️ Infiltrarse
    assert "test:1" not in (service.store.get("enemy_camp", f"{service._today()}:{cx}:{cy}") or {}).get("scouted", [])
    monkeypatch.setattr(camp_rules, "detect_chance", lambda *args: 0.0)
    scout_at(service, cx, cy, 30, "test:1", "Lyra")
    inside = service.act("test:1", "infiltrate")                                    # recon never spends the infiltration
    assert inside.kind == "ecamp_intel"
    same = ("👹 Quedan", "👑")                                                        # the garrison and the chief (the 👹 header differs)
    assert [line for line in inside.body if line.startswith(same)] == [line for line in one.body if line.startswith(same)]


def test_scouted_places_show_on_the_map_and_on_the_routes(service):
    x, y = dungeon_zone(service, "deep")
    scout_at(service, x, y + 2, 30, known=["0:0", f"{x}:{y + 2}"])          # 2 zones away: the 🕳️ cave on the map
    view = service.act("test:1", "map")
    assert any(line.startswith(f"🕳️ ({x}, {y})") and "cueva" in line for line in view.body)
    assert any("/reconocer" in line for line in view.body)
    service.act("test:1", f"rcn:{x}:{y}")
    view = service.act("test:1", "map")
    family = service._dng_family_label(service._dng_today(x, y)["family"])
    assert any(line.startswith(f"🌀 ({x}, {y})") and family in line for line in view.body)   # 🌀 and today's family
    radius = service.content.balance["map_view"]["radius"]
    cells = re.findall(r".\ufe0f?", view.body[2 + radius + 2])                      # its row, 2 below you
    assert cells[radius] == "🌀"                                                     # its square: 🌀, no longer the cave
    scout_at(service, x, y + 1, 30, known=["0:0", f"{x}:{y + 1}"])          # next door: the route says it too
    zone = service.act("test:1", "home")
    emoji = service._dng_families()[service._dng_today(x, y)["family"]]["emoji"]
    assert any(line.startswith("⬇️") and f"🌀{emoji}" in line for line in zone.body)
    # the kind stays known (an entrance never moves); today's family does not
    service.clock.advance(DAY)
    scout_at(service, x, y + 2, 30, known=["0:0", f"{x}:{y + 2}"])
    view = service.act("test:1", "map")
    assert any(line.startswith(f"🌀 ({x}, {y})") and "🔭" not in line for line in view.body)
    assert not service.texts.missing


def test_a_scouted_camp_shows_its_strength_on_the_map(service):
    cx, cy = camp_zone(service)
    scout_at(service, cx + 1, cy, 10)
    mark = f"👹 ({cx}, {cy})"
    assert not any(line.startswith(mark) and "💪" in line for line in service.act("test:1", "map").body)
    service.act("test:1", f"rcn:{cx}:{cy}")
    assert any(line.startswith(mark) and "💪" in line for line in service.act("test:1", "map").body)


def test_explore_menu_tells_what_you_can_scout(service):
    x, y = dungeon_zone(service, "small")
    scout_at(service, x + 1, y, 10)
    menu = service.act("test:1", "explore_menu")
    assert any("/reconocer" in line for line in menu.body) and len(menu.actions) <= 4
    service.act("test:1", f"rcn:{x}:{y}")
    pending = service._recon_pending(service._load("test:1"))
    assert any("/reconocer" in line for line in service.act("test:1", "explore_menu").body) == bool(pending)


# ---------------------------------------------------------------- 🥷 stealth

def test_stealth_grows_evenly_with_rank_and_the_infiltrado_adds_some(service):
    make_hero(service)
    chance = {rank: service._stealth_chance(scout_at(service, 0, 0, rank)) for rank in (1, 10, 50, 100)}
    assert chance[1] == 0.0 and chance[10] == pytest.approx(0.025)                  # rank 1 = not started yet
    assert chance[50] == pytest.approx(0.125) and chance[100] == pytest.approx(0.25)
    assert service._stealth_chance(Hero(id="n", name="N", class_id="guerrero")) == 0.0
    full = service.content.balance["specs"]["mastery_xp"]
    spy = Hero(id="s", name="S", class_id="guerrero", professions={"explorador": rank_xp(service, 100)},
               prof_specs={"explorador": ["explorador_infiltrado"]}, spec_xp={"explorador_infiltrado": full})
    assert service._stealth_chance(spy) == pytest.approx(0.35)
    service.content.balance["explorer"]["stealth_max"] = 0.3
    assert service._stealth_chance(spy) == pytest.approx(0.3)                       # never past the cap
    view = service.act("test:1", "oficios")
    assert any("🥷" in line and "25" in line for line in view.body)                 # in the explorer's perk line
    assert any("🔭" in line for line in view.body)                                  # and the 🔭 thresholds
    assert not service.texts.missing


def explore_round(service, clock, monkeypatch, chance, auto):
    """One exploration round where a fight always comes up, with 🥷 at `chance`; returns (hero, pushes)."""
    service.content.balance["explore"]["encounter"] = 1.0
    monkeypatch.setattr(GameService, "_stealth_chance", lambda self, hero: chance)
    ready(service, auto=auto, level=30)
    service.act("test:1", "do:explore:5")
    clock.advance(10 * MINUTE)
    pushes = [view for acc, view in service.tick() if acc == "test:1"]
    return service._load("test:1"), pushes


def test_stealth_avoids_a_random_fight_while_exploring_by_hand(service, clock, monkeypatch):
    hero, _ = explore_round(service, clock, monkeypatch, 1.0, auto=False)
    assert service.store.get("combat", "test:1") is None and hero.activity and hero.activity["kind"] == "explore"
    assert hero.activity.get("sneaked") == 1
    view = service.act("test:1", "stop")
    assert any("Sigilo" in line for line in (view.notice or "").split("\n") + view.body)


def test_without_stealth_the_fight_comes(service, clock, monkeypatch):
    explore_round(service, clock, monkeypatch, 0.0, auto=False)
    assert service.store.get("combat", "test:1") is not None


def test_automatic_batches_are_unaffected(service, clock, monkeypatch):
    hero, _ = explore_round(service, clock, monkeypatch, 1.0, auto=True)
    assert hero.kills >= 1                                                          # it fought: stealth stayed out
    assert not (hero.activity or {}).get("sneaked")


def wild_row(service):
    """Three zones in a row (west to east) where an arrival can be ambushed: danger, no land, no lair, no enemy camp."""
    def wild(x, y):
        return service.content.biomes[service._zone(x, y).biome]["danger"] > 0 and not service._territory(x, y) \
            and not service._is_lair(x, y) and not service._ecamp_standing(x, y)
    for x in range(2, 12):
        for y in range(-6, 7):
            if wild(x, y) and wild(x + 1, y) and wild(x + 2, y):
                return x, y
    raise AssertionError("no wild row")


def test_stealth_avoids_the_ambush_when_arriving(service, clock, monkeypatch):
    service.content.balance["explore"]["arrival_encounter_scale"] = 100.0           # an ambush on every arrival
    monkeypatch.setattr(GameService, "_stealth_chance", lambda self, hero: 1.0)
    x, y = wild_row(service)
    scout_at(service, x, y, 1, level=30)
    service.act("test:1", "go:e")
    clock.advance(30 * MINUTE)
    view = service.act("test:1", "home")
    assert service._load("test:1").x == x + 1 and service.store.get("combat", "test:1") is None
    assert "🥷" in (view.notice or "")
    monkeypatch.setattr(GameService, "_stealth_chance", lambda self, hero: 0.0)     # without it, the ambush comes
    service.act("test:1", "go:e")
    clock.advance(30 * MINUTE)
    service.act("test:1", "home")
    assert service.store.get("combat", "test:1") is not None


def test_stealth_never_applies_to_chosen_fights(service, clock, monkeypatch):
    calls = []

    def spy(self, hero, *parts):
        calls.append(parts)
        return True
    monkeypatch.setattr(GameService, "_sneaks_past", spy)
    monkeypatch.setattr(GameService, "_stealth_chance", lambda self, hero: 1.0)
    # 🏹 hunting (a fight you choose)
    ready(service, auto=False)
    service.act("test:1", "hunt")
    assert service.act("test:1", "prey").kind == "combat"
    win(service, "test:1")
    # ⚔️ assaulting an enemy camp
    cx, cy = camp_zone(service)
    scout_at(service, cx, cy, 100)
    assert service.act("test:1", "assault").kind == "combat"
    win(service, "test:1")
    # 🕳️ a dungeon
    x, y = dungeon_zone(service, "small")
    scout_at(service, x, y, 100, level=20, hp=10 ** 6)
    assert service.act("test:1", "dgo").kind == "combat"
    win(service, "test:1")
    # 👑 the Guardian
    _to_lair(service)
    assert service.act("test:1", "boss").kind == "combat"
    service.store.delete("combat", "test:1")
    assert calls == []
    # 🛡️ a raid on your camp
    camp_at_level(service, 5)
    open_raid(service, clock, ["test:1"])
    assert service.act("test:1", "defend").kind == "combat"
    assert calls == []


def test_automatic_hunting_batches_still_fight_every_prey(service, clock, monkeypatch):
    monkeypatch.setattr(GameService, "_stealth_chance", lambda self, hero: 1.0)
    hero = ready(service, level=30)
    kills = hero.kills
    service.act("test:1", "hunt")
    service.act("test:1", "prey")
    service.act("test:1", "do:hunt:4")
    for _ in range(3):
        clock.advance(16 * MINUTE)
        service.tick()
    assert service._load("test:1").kills == kills + 2


# ---------------------------------------------------------------- old heroes, buttons and texts

def test_old_heroes_load(service):
    make_hero(service)
    data = service.store.get("hero", "test:1")
    for key in ("professions", "prof_specs", "spec_xp", "options", "titles"):
        data.pop(key, None)
    service.store.put("hero", "test:1", data)
    for screen in ("home", "explore_menu", "map", "recon", "oficios", "options", "hero"):
        assert service.act("test:1", screen).kind, screen
    hero = Hero.from_dict(service.store.get("hero", "test:1"))
    assert service._stealth_chance(hero) == 0.0 and service._recon_range(hero) == 0
    assert service.store.get("recon", "test:1") is None
    assert not service.texts.missing


def test_every_recon_screen_keeps_four_buttons_and_its_texts(content):
    def build(path):
        service = GameService(content, MemoryStore(), FixedClock(), world_seed=SEED)
        make_hero(service)
        cx, cy = camp_zone(service)
        scout_at(service, cx + 1, cy, 100, known=["0:0", f"{cx + 1}:{cy}", f"{cx + 2}:{cy}"])
        view = service.act("test:1", "recon")                  # /reconocer (the map button only shows when it fits)
        for action in path:
            view = service.act("test:1", action)
        return service, view

    seen, queue, kinds = set(), deque([[]]), set()
    while queue and len(seen) < 40:
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
            if not action_id.startswith(("go:", "goto:", "do:", "ab:", "use:", "prey", "flee")):
                queue.append(path + [action_id])
    assert {"map", "recon", "recon_report"} <= kinds
