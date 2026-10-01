"""Camp raids and the Noche de prueba, phase 2 of "building is not enough" (D-99, provisional; only player camps).

[ES] Pruebas de las incursiones (para el jugador, "oleadas"): desde que se funda el campamento (D-105) llega una por
semana con reloj perezoso y un aviso al fundarlo; los miembros
conectados tocan 🛡️ Defender y pelean una vez cada uno; si alcanzan las victorias, premio chico; si no, la despensa
pierde una parte y nada más. La Noche de prueba traba el paso a castillo (nivel 9) hasta ganarla y se reintenta
a los 2 días. El Claro nunca tiene incursiones: es el campamento base (D-95, D-98). También el tope de 4 botones.
"""

import pytest

from conftest import make_hero
from engine.combat import make_combat
from engine.social import guilds as guild_rules
from engine.world import raids as raid_rules
from test_camps import found_at, place

DAY = 24 * 3600
HOUR = 3600
RAID_GAP = 7 * DAY / 3          # D-154: 3 raids per real week (balance.yaml raids.per_week)
KEY = "6:0"


def camp_at_level(service, level, members=("test:1",)):
    """Found a camp at 6:0 for test:1, then set its level and members straight in the store (all at the camp)."""
    found_at(service, "test:1", 6, 0)
    camp = service.store.get("camp", KEY)
    camp["level"], camp["members"] = level, list(members)
    service.store.put("camp", KEY, camp)
    for member in members:
        hero = service._load(member)
        hero.camp, hero.x, hero.y = KEY, 6, 0
        service._save(hero)
    return camp


def camp(service):
    return service.store.get("camp", KEY)


def guild_ready(service):
    """D-97: castillo also needs a ready guild; give the camp one straight in the store (guilds: test_guilds.py).
    D-101: and 15 improvements built (tests/test_camp_upgrades.py), so only the Noche de prueba is left."""
    cfg = service.content.balance["guild"]
    cfg["castle_min_members"] = len(camp(service)["members"])
    service.store.put("guild", KEY, {"name": "Lobos Grises", "camp": KEY, "founder_id": "test:1",
                                     "level": cfg["castle_min_level"],
                                     "progress": {k: 0 for k in guild_rules.COUNTERS}, "created": 0.0})
    need = service.content.balance["upgrades"]["castle_min_built"]
    built = {uid: 0.0 for uid in list(service._upgrade_catalog())[:need]}
    service.store.put("upgrades", KEY, {"built": built, "works": {}, "tech": {}})


def set_rations(service, rations):
    service.store.put("pantry", KEY, {"rations": float(rations), "at": service.clock.now()})


def pushes(service, kind):
    return [(account, view) for account, view in service.tick() if view.kind == kind]


def open_raid(service, clock, members):
    """Everyone plays just before the raid is due (so they count as active), then test:1 plays and it arrives."""
    for member in members:
        service.act(member, "hero")
    due = camp(service)["next_raid_at"]
    clock.advance(due - clock.now() - HOUR)
    for member in members:
        service.act(member, "hero")
    clock.advance(HOUR)
    return service.act("test:1", "claro")


def win(service, account):
    state = service.store.get("combat", account)
    state["enemy"]["hp"] = 1
    service.store.put("combat", account, state)
    return service.act(account, "atk")


def lose(service, account):
    hero = service._load(account)
    state = service.store.get("combat", account)
    state["outcome"] = "defeat"
    view = service._end_combat(hero, state)
    service._save(hero)
    return view


def test_pure_rules(content):
    assert raid_rules.required_wins(0, 0.5, 1) == 1                 # nobody active: still 1, no division by 0
    assert raid_rules.required_wins(3, 0.5, 1) == 2                 # rounded up
    assert raid_rules.required_wins(4, 0.5, 1) == 2
    assert raid_rules.required_wins(1, 0.5, 2) == 2                 # the Noche de prueba asks for 2 at least
    assert raid_rules.next_raid_at(100, 150, 1000) == 1100          # one interval after the last window
    assert raid_rules.next_raid_at(100, 5000, 1000) == 6000         # long quiet camp: counted from now
    assert raid_rules.food_lost(20, 0.25) == 5 and raid_rules.food_lost(0, 0.25) == 0
    enemy_id, level = raid_rules.pick_enemy(content.enemies, "bosque", 6, strongest=True)
    edef = content.enemies[enemy_id]
    assert not edef.get("boss") and "bosque" in edef["biomes"] and edef["level_min"] <= level <= edef["level_max"]
    others = [e for e in content.enemies.values() if "bosque" in e["biomes"] and not e.get("boss") and e["level_min"] <= 6 <= e["level_max"]]
    assert all(raid_rules.power(edef, level) >= raid_rules.power(e, 6) for e in others)
    assert raid_rules.pick_enemy(content.enemies, "bosque", 6, roll=0.99)[0] in content.enemies


def test_waves_start_when_the_camp_is_founded_and_never_in_the_claro(service, clock):
    make_hero(service, "test:1", "Lyra")
    view = found_at(service, "test:1", 6, 0)                        # D-105: from the very first level, with a warning
    assert "oleada" in view.notice and "Refuerza" in view.notice and "3 veces por semana" in view.notice
    assert camp(service)["next_raid_at"] == pytest.approx(clock.now() + RAID_GAP)
    assert any("Próxima oleada en 3 días" in line for line in view.body)
    clock.advance(RAID_GAP)
    view = service.act("test:1", "claro")
    assert camp(service)["raid"]["required"] == 1 and "defend" in [a.id for a in view.actions]   # a camp of one can defend it
    # The Claro is the base camp: it is not a "camp" record, so it never has raids (D-95, D-98).
    make_hero(service, "test:2", "Bram")
    for _ in range(3):
        clock.advance(RAID_GAP)
        for screen in ("claro", "camp"):
            view = service.act("test:2", screen)
            assert not any("leada" in line for line in view.body) and "defend" not in [a.id for a in view.actions]
    assert service.store.get("camp", "0:0") is None
    assert all(account == "test:1" for account, _ in pushes(service, "camp_raid"))
    assert service.act("test:2", "defend").notice == service.texts.t("raids.none")


def test_raid_arrives_after_the_interval(service, clock):
    make_hero(service, "test:1", "Lyra")
    camp_at_level(service, 5)
    view = service.act("test:1", "claro")
    assert camp(service)["next_raid_at"] == pytest.approx(clock.now() + RAID_GAP)   # existing camp: scheduled lazily
    assert any("Próxima oleada en 3 días" in line for line in view.body)
    clock.advance(RAID_GAP - 60)
    view = service.act("test:1", "claro")
    assert not camp(service).get("raid") and any("en 1 día" in line for line in view.body)
    assert not pushes(service, "camp_raid")
    clock.advance(60)
    view = service.act("test:1", "claro")
    raid = camp(service)["raid"]
    assert raid["kind"] == "raid" and raid["required"] == 1 and raid["until"] == pytest.approx(clock.now() + HOUR)
    assert any(line.startswith("🔔 ¡Oleada!") and "victorias 0/1" in line for line in view.body)
    assert [a.id for a in view.actions] == ["grow", "campfeed", "guild", "defend"]   # Defender takes the place of Volver
    notices = pushes(service, "camp_raid")
    assert [acc for acc, _ in notices] == ["test:1"]
    assert [a.id for a in notices[0][1].actions] == ["defend"] and "nivel" in notices[0][1].body[0]


def test_defenders_wins_are_counted_and_a_defended_raid_pays_them(service, clock):
    members = ("test:1", "test:2", "test:3", "test:4")
    for n, name in enumerate(("Lyra", "Bram", "Cora", "Dain"), start=1):
        make_hero(service, f"test:{n}", name)
    camp_at_level(service, 5, members)
    service.act("test:1", "claro")
    service.act("test:2", "home")                  # Bram walks back to the Claro: defending works from anywhere
    hero = service._load("test:2")
    hero.x, hero.y = 0, 0
    service._save(hero)
    open_raid(service, clock, members)
    set_rations(service, 40)
    raid = camp(service)["raid"]
    assert raid["required"] == 2                   # half of the 4 active members
    assert sorted(acc for acc, _ in pushes(service, "camp_raid")) == list(members)
    before = {m: service._load(m) for m in members}
    fight = service.act("test:2", "defend")
    assert fight.kind == "combat" and "Sales a defender" in fight.notice
    assert service.act("test:2", "home").kind == "combat"        # mid-fight nothing else
    end = win(service, "test:2")
    assert end.kind == "combat_end" and any("Van 1 de 2" in line for line in end.body)
    service.act("test:3", "defend")
    end = lose(service, "test:3")
    assert any("no suma" in line for line in end.body)
    hero3 = service._load("test:3")              # normal defeat rules, nothing extra
    assert hero3.downed and hero3.gold == before["test:3"].gold - int(before["test:3"].gold * 0.1)
    assert service.act("test:2", "defend").notice == service.texts.t("raids.already")
    service.act("test:4", "defend")
    win(service, "test:4")
    raid = camp(service)["raid"]
    assert raid["wins"] == 2 and raid["fights"] == {"test:2": "won", "test:3": "lost", "test:4": "won"}
    member_view = service.act("test:4", "claro")
    assert "defend" not in [a.id for a in member_view.actions] and "upgrades" in [a.id for a in member_view.actions]   # D-101: 🔨 Mejoras is back
    until = raid["until"]
    clock.advance(HOUR + 1)
    service.act("test:1", "claro")
    after = camp(service)
    assert not after.get("raid") and after["raids"] == {"won": 1, "lost": 0}
    assert after["next_raid_at"] == pytest.approx(until + RAID_GAP)
    assert after["level"] == 5 and after["members"] == list(members) and len(after["zones"]) == 1
    ends = pushes(service, "camp_raid_end")
    assert sorted(acc for acc, _ in ends) == list(members) and "resistió" in ends[0][1].body[0]
    reward = service.content.balance["raids"]["reward"]
    for member in ("test:2", "test:4"):
        hero = service._load(member)
        assert hero.gold >= before[member].gold + reward["gold"] and hero.xp >= before[member].xp + reward["xp"]
    assert service._load("test:3").gold == hero3.gold + reward["gold"]       # who fought and lost is paid too
    assert service._load("test:1").gold == before["test:1"].gold              # who did not fight, no
    assert service.store.get("pantry", KEY)["rations"] > 39                   # defended: the pantry only fed people


def test_a_lost_raid_takes_part_of_the_pantry_and_nothing_else(service, clock):
    make_hero(service, "test:1", "Lyra")
    camp_at_level(service, 6)
    open_raid(service, clock, ("test:1",))
    set_rations(service, 20)
    gold, level, xp = (lambda h: (h.gold, h.level, h.xp))(service._load("test:1"))
    until = camp(service)["raid"]["until"]
    clock.advance(HOUR + 60)
    service.act("test:1", "claro")
    eaten = (HOUR + 60) / DAY                                          # 1 active member kept eating
    assert service.store.get("pantry", KEY)["rations"] == pytest.approx((20 - eaten) * 0.75)
    after = camp(service)
    assert after["level"] == 6 and after["members"] == ["test:1"] and len(after["zones"]) == 1
    assert after["raids"] == {"won": 0, "lost": 1} and after["next_raid_at"] == pytest.approx(until + RAID_GAP)
    hero = service._load("test:1")
    assert (hero.gold, hero.level, hero.xp) == (gold, level, xp)         # nothing personal is lost
    ends = pushes(service, "camp_raid_end")
    assert ends and "perdió 5 raciones" in " ".join(ends[0][1].body)


def test_a_fight_going_on_when_the_window_closes_still_counts(service, clock):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    camp_at_level(service, 5, ("test:1", "test:2"))
    open_raid(service, clock, ("test:1", "test:2"))
    service.act("test:2", "defend")
    clock.advance(HOUR + 60)
    service.act("test:1", "claro")
    assert camp(service).get("raid")                    # waits for Bram's fight (grace time)
    assert service.act("test:1", "defend").notice == service.texts.t("raids.none")   # the window is closed
    win(service, "test:2")
    service.act("test:1", "claro")
    assert camp(service)["raids"] == {"won": 1, "lost": 0}


def test_busy_heroes_finish_first(service, clock):
    make_hero(service, "test:1", "Lyra")
    camp_at_level(service, 5)
    open_raid(service, clock, ("test:1",))
    hero = service._load("test:1")
    hero.activity = {"kind": "explore", "until": clock.now() + 600}
    service._save(hero)
    view = service.act("test:1", "defend")
    assert view.notice == service.texts.t("raids.busy") and service.store.get("combat", "test:1") is None


def test_noche_de_prueba_gates_castillo(service, clock):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    camp_at_level(service, 8, ("test:1", "test:2"))
    guild_ready(service)
    service.act("test:2", "claro")
    view = service.act("test:1", "grow")
    assert view.kind == "camp_trial" and [a.id for a in view.actions] == ["trial", "claro"]
    assert "castillo" in view.body[0] and "Noche de prueba" in view.body[0]
    backpack = dict(service._load("test:1").backpack)
    view = service.act("test:1", "claim:6:1")
    assert view.kind == "camp_trial" and camp(service)["level"] == 8 and service._load("test:1").backpack == backpack
    set_rations(service, 0)                                          # empty pantry: cannot call it
    view = service.act("test:1", "trial")
    assert view.notice == service.texts.t("raids.trial_famine") and "trial" not in [a.id for a in view.actions]
    set_rations(service, 30)
    view = service.act("test:1", "trial")
    raid = camp(service)["raid"]
    assert view.notice == service.texts.t("raids.trial_sent") and raid["kind"] == "trial" and raid["required"] == 2
    assert [a.id for a in view.actions] == ["defend", "claro"]
    assert sorted(acc for acc, _ in pushes(service, "camp_raid")) == ["test:1", "test:2"]
    # The enemy is an elite: the strongest of the biome with more life and attack.
    fight = service.act("test:1", "defend")
    assert fight.kind == "combat" and "élite" in fight.notice
    state = service.store.get("combat", "test:1")
    normal = make_combat(raid["enemy"], service.content.enemies[raid["enemy"]], raid["level"], service._kit(service._load("test:1")), 1)
    trial = service.content.balance["raids"]["trial"]
    weaken = service._raid_weaken(raid)                              # D-101: the 15 improvements include defenses
    assert raid["defense"] > 0 and weaken < 1
    assert state["enemy"]["max_hp"] == round(round(normal["enemy"]["max_hp"] * trial["enemy_hp_mult"]) * weaken)
    assert state["enemy"]["attack"] == pytest.approx(normal["enemy"]["attack"] * trial["enemy_attack_mult"] * weaken)
    win(service, "test:1")                                           # 1 of 2: Bram never comes
    clock.advance(HOUR + 1)
    service.act("test:1", "claro")
    after = camp(service)
    assert not after.get("trial_won") and after["level"] == 8 and after["trial_retry_at"] > clock.now()
    assert service.store.get("pantry", KEY)["rations"] > 29          # a lost trial takes nothing
    assert "no ganó" in pushes(service, "camp_raid_end")[0][1].body[0]
    view = service.act("test:1", "grow")
    assert "trial" not in [a.id for a in view.actions] and any("Se puede volver a convocar" in line for line in view.body)
    assert service.act("test:1", "trial").notice.startswith("⏳")
    clock.advance(2 * DAY)
    service.act("test:2", "claro")
    view = service.act("test:1", "grow")
    assert [a.id for a in view.actions] == ["trial", "claro"]       # retry after trial.retry_days
    service.act("test:1", "trial")
    for member in ("test:1", "test:2"):
        service.act(member, "defend")
        win(service, member)
    clock.advance(HOUR + 1)
    service.act("test:1", "claro")
    assert camp(service)["trial_won"] is True
    assert "ganó la Noche de prueba" in pushes(service, "camp_raid_end")[0][1].body[0]
    view = service.act("test:1", "grow")
    assert view.kind == "camp_grow"
    claim = next(a.id for a in view.actions if a.id.startswith("claim:"))
    place(service, "test:1", 6, 0, backpack={"madera": 999, "piedra": 999, "fibra": 999}, chests=99)   # the usual cost (D-92)
    view = service.act("test:1", claim)
    assert camp(service)["level"] == 9 and any("castillo" in line for line in view.body)


def test_button_limits_during_raids(service, clock):
    make_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    camp_at_level(service, 8, ("test:1", "test:2"))
    guild_ready(service)
    open_raid(service, clock, ("test:1", "test:2"))
    for account in ("test:1", "test:2"):
        view = service.act(account, "claro")
        assert len(view.actions) <= 4 and "defend" in [a.id for a in view.actions]
        assert ("rename" if account == "test:1" else "leave") not in [a.id for a in view.actions]
        trial = service.act(account, "grow")                 # a weekly raid is on: no trial now, but Defender works
        assert trial.kind == "camp_trial" and len(trial.actions) <= 4 and "trial" not in [a.id for a in trial.actions]
    for _, view in service.tick():
        assert len(view.actions) <= 4 and all(len(a.id.encode()) <= 64 for a in view.actions)
    assert not service.texts.missing


def test_the_noche_de_prueba_counts_as_that_weeks_raid(service, clock):
    make_hero(service, "test:1", "Lyra")
    camp_at_level(service, 8)
    service.act("test:1", "claro")
    data = camp(service)
    data["next_raid_at"] = clock.now() + 30 * 60          # the weekly raid comes due during the trial
    service.store.put("camp", KEY, data)
    service.act("test:1", "trial")
    until = camp(service)["raid"]["until"]
    clock.advance(HOUR + 1)
    service.act("test:1", "claro")
    after = camp(service)
    assert not after.get("raid") and after["next_raid_at"] == pytest.approx(until + RAID_GAP)


def build_all(service, ids):
    """Mark camp improvements as built straight in the store (building them is tested in test_camp_upgrades.py)."""
    service.store.put("upgrades", KEY, {"built": {uid: 0.0 for uid in ids}, "works": {}, "tech": {}})


def test_defenses_weaken_the_wave_and_the_watchtower_warns(service, clock):
    # D-101: every 🛡️ Defensa point takes raids.defense_weaken_per_point of the attackers' life and attack.
    make_hero(service, "test:1", "Lyra")
    camp_at_level(service, 5)
    service.act("test:1", "claro")
    catalog = service._upgrade_catalog()
    walls = [uid for uid, u in catalog.items() if u.get("defense")]
    build_all(service, walls)
    defense = service._camp_defense(camp(service))
    assert defense == sum(catalog[uid]["defense"] for uid in walls)
    cfg = service.content.balance["raids"]
    # 🗼 the watchtower: one heads-up to the active members in the last warning hours, then the hours on screen
    due = camp(service)["next_raid_at"]
    clock.advance(due - clock.now() - 3 * HOUR)
    service.act("test:1", "claro")
    assert not pushes(service, "camp_watch")
    clock.advance(2 * HOUR)
    view = service.act("test:1", "claro")
    watch = pushes(service, "camp_watch")
    assert [acc for acc, _ in watch] == ["test:1"] and "torre" in watch[0][1].body[0]
    assert any(line.startswith("🗼") for line in view.body)
    service.act("test:1", "claro")
    assert not pushes(service, "camp_watch")                         # only once per raid
    clock.advance(HOUR)
    service.act("test:1", "claro")
    raid = camp(service)["raid"]
    night = service._is_night(raid["at"])
    assert raid["defense"] == service._camp_defense(camp(service), night=night)
    weaken = max(cfg["defense_floor"], 1 - cfg["defense_weaken_per_point"] * raid["defense"])
    assert service._raid_weaken(raid) == pytest.approx(weaken) and weaken < 1
    notice = pushes(service, "camp_raid")[0][1]
    assert any("Defensa" in line and "%" in line for line in notice.body)
    service.act("test:1", "defend")
    state = service.store.get("combat", "test:1")
    normal = make_combat(raid["enemy"], service.content.enemies[raid["enemy"]], raid["level"], service._kit(service._load("test:1")), 1)
    assert state["enemy"]["max_hp"] == max(1, round(normal["enemy"]["max_hp"] * weaken))
    assert not service.texts.missing


def test_braseros_count_only_at_night(service):
    make_hero(service, "test:1", "Lyra")
    camp_at_level(service, 6)
    braseros = [uid for uid, u in service._upgrade_catalog().items() if u.get("effect", {}).get("night_defense")]
    build_all(service, braseros)
    day, night = service._camp_defense(camp(service)), service._camp_defense(camp(service), night=True)
    assert braseros and night == day + 1
    offset = service.content.balance["raids"]["night"]["utc_offset_hours"]
    noon, midnight = (12 - offset) * HOUR, (24 - offset) * HOUR
    assert not service._is_night(noon) and service._is_night(midnight)
