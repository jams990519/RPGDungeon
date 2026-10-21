"""The castle's growing waves (D-122, confirmed; how they were applied: D-329, provisional; 0.53).

[ES] Pruebas de las 🌊 oleadas crecientes del paso a castillo: mientras el campamento está en el nivel anterior al castillo
(8 → 9), sus oleadas normales (3 por semana) son una serie de 5 (balance.yaml ladder.castle_waves), cada una un 20 % más
fuerte que una oleada normal; se aprueba ganando 3 y, con 3 perdidas, la serie se pierde y vuelve a empezar después de 3
días. Sin la serie aprobada no se llega a castillo. ⏫ Siguiente nivel lo dice en una línea (en los dos idiomas) y cada
miembro recibe el parte de cada oleada (_push_each). Un castillo que ya existe no las recibe (D-64).
"""

import pytest

from conftest import make_hero
from engine.combat import make_combat
from engine.world import raids as raid_rules
from test_camps import place
from test_idiomas import english_hero
from test_raids import DAY, HOUR, KEY, RAID_GAP, camp, camp_at_level, guild_ready, open_raid, set_rations, win


def ids(view):
    return [a.id for a in view.actions]


def text(view):
    return "\n".join(view.body)


def ends(service):
    """Every member's report of the wave that just closed: {account: body text} (kind camp_raid_end)."""
    return {acc: text(view) for acc, view in service.tick() if view.kind == "camp_raid_end"}


def wave(service, clock, members, won):
    """Let the next raid of the camp come, test:1 defends and wins it (won=True) or nobody defends; then it closes.

    Returns the raid as it arrived (with "wave" and "wave_mult" if it was a growing wave)."""
    open_raid(service, clock, members)
    raid = dict(camp(service)["raid"])
    if won:
        service.act("test:1", "defend")
        win(service, "test:1")
    clock.advance(HOUR + 1)
    service.act("test:1", "claro")
    assert not camp(service).get("raid")
    return raid


def series(service):
    return camp(service).get("castle_waves") or {}


def castle_ready_but_the_waves(service):
    """test:1's camp at level 8 with everything the castle asks but the growing waves (D-99, D-101, D-253.2, D-304)."""
    make_hero(service, "test:1", "Lyra")
    camp_at_level(service, 8)
    guild_ready(service)                                    # the guild, 1 active of 1, 15 improvements
    record = service._upgrades(KEY)
    record["built"].update({"torres_arqueros": 0.0, "foso": 0.0})      # the works of the 8 → 9 checklist
    service.store.put("upgrades", KEY, record)
    data = camp(service)
    data["trial_won"] = True                                # the 🌙 Noche de prueba is its own gate (tests/test_raids.py)
    service.store.put("camp", KEY, data)
    set_rations(service, 60)
    place(service, "test:1", 6, 0, backpack={"madera": 999, "piedra": 999, "fibra": 999}, chests=99)


# ---------------------------------------------------------------- the pure rules (engine/world/raids.py)


def test_the_pure_rules_of_the_series():
    assert [raid_rules.wave_mult(n, 0.2) for n in range(1, 6)] == pytest.approx([1.2, 1.4, 1.6, 1.8, 2.0])
    assert raid_rules.wave_mult(3, -1) == 1.0 and raid_rules.wave_mult(0, 0.2) == 1.0     # never weaker than a normal raid
    assert raid_rules.series_outcome(0, 0, 5, 3) is None
    assert raid_rules.series_outcome(2, 2, 5, 3) is None                # 1 left: still possible
    assert raid_rules.series_outcome(3, 0, 5, 3) == "passed"            # decided early: 3 of 5
    assert raid_rules.series_outcome(3, 2, 5, 3) == "passed"
    assert raid_rules.series_outcome(0, 3, 5, 3) == "failed"            # "si pierde más de las que gana, no aprueba"
    assert raid_rules.series_outcome(2, 3, 5, 3) == "failed"
    assert raid_rules.series_outcome(1, 0, 1, 9) == "passed"            # pass_wins never above the count


# ---------------------------------------------------------------- the gate


def test_no_castle_without_passing_the_series(service, clock):
    castle_ready_but_the_waves(service)
    assert service.content.balance["ladder"]["castle_waves"] == {"count": 5, "pass_wins": 3, "growth": 0.2, "retry_days": 3}
    view = service.act("test:1", "lvlgive")                 # the materials and the chests go in: still a city
    assert camp(service)["level"] == 8 and "lvlgo" not in ids(view)
    assert ("▫️ 🌊 Oleadas crecientes: ganar 3 de 5 (empiezan solas con la próxima oleada; cada una, un 20 % más fuerte)"
            in view.body)
    assert all(line.startswith("✅") for line in view.body if line.startswith(("✅", "▫️")) and "Oleadas" not in line)
    assert any(line.startswith("🌊 Las oleadas crecientes llegan solas") and "3 por semana" in line
               and "la 5.ª, un 100 % más" in line and "Si pierden 3, vuelven a empezar a los 3 días" in line
               for line in view.body)
    assert ids(view) == ["improve"]                         # they come by themselves: no new button (D-44)
    assert service.act("test:1", "lvlgo").notice == "Todavía falta algo de la lista."
    for n in (1, 2):
        raid = wave(service, clock, ("test:1",), won=True)
        assert raid["wave"] == n
        assert camp(service)["level"] == 8 and series(service)["won"] == n
    row = [line for line in service.act("test:1", "lvlup").body if "Oleadas crecientes" in line]
    assert row == ["▫️ 🌊 Oleadas crecientes: 2 ganadas, 0 perdidas de 5 (hace falta ganar 3; quedan 3)"]
    wave(service, clock, ("test:1",), won=True)             # the 3rd win: passed, the series ends early
    assert series(service)["passed"] is True and series(service)["won"] == 3
    after = wave(service, clock, ("test:1",), won=False)    # from now on the waves are normal ones again
    assert "wave" not in after and "wave_mult" not in after and series(service)["passed"] is True
    view = service.act("test:1", "lvlup")
    assert "✅ 🌊 Oleadas crecientes: superadas (3 ganadas, 0 perdidas)" in view.body and ids(view) == ["lvlgo", "improve"]
    service.act("test:1", "lvlgo")
    assert camp(service)["level"] == 9                      # a castle
    assert service._castle_waves_row(camp(service)) is None


# ---------------------------------------------------------------- the waves grow


def test_each_wave_is_stronger_than_the_last(service, clock):
    make_hero(service, "test:1", "Lyra")
    camp_at_level(service, 8)
    service.act("test:1", "claro")
    hero = service._load("test:1")
    ratios = []
    for n in (1, 2, 3):
        open_raid(service, clock, ("test:1",))
        raid = camp(service)["raid"]
        assert raid["kind"] == "raid" and raid["wave"] == n and raid["wave_mult"] == pytest.approx(1 + 0.2 * n)
        pct = 20 * n
        notice = [view for acc, view in service.tick() if view.kind == "camp_raid"][0]
        assert f"🌊 Oleada creciente {n} de 5: un {pct} % más fuerte que una oleada normal." in text(notice)
        assert f"🌊 Es la oleada creciente {n} de 5 (+{pct} %)." in service.act("test:1", "claro").body
        fight = service.act("test:1", "defend")
        assert f"🌊 Oleada creciente {n} de 5: +{pct} % de vida y de ataque." in fight.notice
        state = service.store.get("combat", "test:1")
        normal = make_combat(raid["enemy"], service.content.enemies[raid["enemy"]], raid["level"], service._kit(hero), 1)
        assert raid.get("defense", 0) == 0                  # no defenses here: only the wave's own strength
        assert state["enemy"]["max_hp"] == max(1, round(normal["enemy"]["max_hp"] * raid["wave_mult"]))
        assert state["enemy"]["attack"] == pytest.approx(normal["enemy"]["attack"] * raid["wave_mult"])
        ratios.append(state["enemy"]["attack"] / normal["enemy"]["attack"])
        if n < 3:
            win(service, "test:1")
        else:                                               # (the 3rd would pass the series: lose it instead)
            hero_now = service._load("test:1")
            state["outcome"] = "defeat"
            service._end_combat(hero_now, state)
            service._save(hero_now)
        clock.advance(HOUR + 1)
        service.act("test:1", "claro")
    assert ratios == sorted(ratios) and ratios[0] > 1       # stronger every time
    assert series(service) == {"won": 2, "lost": 1, "tries": 1}


# ---------------------------------------------------------------- 3 of 5 pass, 3 losses fail, retry after the wait


def test_three_wins_of_five_pass(service, clock):
    make_hero(service, "test:1", "Lyra")
    camp_at_level(service, 8)
    service.act("test:1", "claro")
    expected = [(False, "0 ganadas y 1 perdida de 5", "quedan 4"), (True, "1 ganada y 1 perdida de 5", "quedan 3"),
                (False, "1 ganada y 2 perdidas de 5", "quedan 2"), (True, "2 ganadas y 2 perdidas de 5", "queda 1")]
    for n, (won, score, left) in enumerate(expected, start=1):
        raid = wave(service, clock, ("test:1",), won=won)
        assert raid["wave"] == n
        report = ends(service)["test:1"]                    # the short notice after each wave (_push_each)
        assert f"🌊 Oleadas crecientes de {camp(service)['name']}: {score}." in report and left in report
    raid = wave(service, clock, ("test:1",), won=True)      # the 5th, won: 3 of 5
    assert raid["wave"] == 5 and raid["wave_mult"] == pytest.approx(2.0)
    report = ends(service)["test:1"]
    assert "superó las oleadas crecientes (3 ganadas y 2 perdidas)! El castillo ya no las pide." in report
    assert series(service)["passed"] is True and series(service)["tries"] == 1
    assert service._castle_wave_next(camp(service)) is None


def test_three_losses_fail_and_it_starts_again_after_the_wait(service, clock):
    make_hero(service, "test:1", "Lyra")
    camp_at_level(service, 8)
    service.act("test:1", "claro")
    for won in (False, True, False):
        wave(service, clock, ("test:1",), won=won)
        ends(service)
    last = wave(service, clock, ("test:1",), won=False)     # the 3rd loss: 1 won, 3 lost, it cannot pass any more
    assert last["wave"] == 4
    report = ends(service)["test:1"]
    assert "perdió las oleadas crecientes (1 ganada y 3 perdidas). Vuelven a empezar desde la primera en" in report
    assert "No se pierde nada más." in report
    data = series(service)
    assert data["won"] == 0 and data["lost"] == 0 and not data.get("passed")
    assert data["retry_at"] == pytest.approx(last["until"] + 3 * DAY)
    assert camp(service)["level"] == 8                      # nothing else is lost: level, zones and members stay
    row = [line for line in service.act("test:1", "lvlup").body if "Oleadas crecientes" in line]
    assert len(row) == 1 and row[0].startswith("▫️ 🌊 Oleadas crecientes: perdidas; vuelven a empezar en ")
    assert row[0].endswith("(hay que ganar 3 de 5)")
    during = wave(service, clock, ("test:1",), won=False)   # 2 days and 8 hours later: still waiting, a normal wave
    assert "wave" not in during and series(service)["won"] == series(service)["lost"] == 0
    again = wave(service, clock, ("test:1",), won=True)     # after the 3 days: the series starts again from wave 1
    assert again["wave"] == 1 and again["wave_mult"] == pytest.approx(1.2)
    assert series(service)["won"] == 1 and series(service)["tries"] == 2
    assert again["at"] >= data["retry_at"]


# ---------------------------------------------------------------- the checklist row and the notices in both languages


def test_the_row_and_the_notices_read_well_in_both_languages(service, clock):
    make_hero(service, "test:1", "Lyra")
    english_hero(service, "test:2", "Bram")
    camp_at_level(service, 8, ("test:1", "test:2"))
    service.act("test:1", "claro")
    rows = {}
    for lang in ("es", "en"):
        with service.texts.use(lang):
            rows[lang] = [service._castle_waves_row(camp(service))[0]]
    raid = wave(service, clock, ("test:1", "test:2"), won=True)
    assert raid["wave"] == 1 and raid["required"] == 1     # half of the 2 active members
    reports = ends(service)
    assert "🌊 Oleadas crecientes de" in reports["test:1"] and "1 ganada y 0 perdidas de 5" in reports["test:1"]
    assert "growing waves: 1 win and 0 losses of 5. To become a castle you need to win 3; 4 waves left." in reports["test:2"]
    data = camp(service)
    data["castle_waves"] = {"won": 2, "lost": 1, "tries": 1}
    service.store.put("camp", KEY, data)
    view = service.act("test:2", "lvlup")                  # the English member's checklist
    assert "▫️ 🌊 Growing waves: 2 wins, 1 loss of 5 (you need to win 3; 2 waves left)" in view.body
    assert any(line.startswith("🌊 The growing waves come by themselves") and "wave 5, 100% more" in line for line in view.body)
    es_view = service.act("test:1", "lvlup")
    assert "▫️ 🌊 Oleadas crecientes: 2 ganadas, 1 perdida de 5 (hace falta ganar 3; quedan 2)" in es_view.body
    data["castle_waves"] = {"won": 0, "lost": 0, "tries": 1, "retry_at": clock.now() + DAY}
    service.store.put("camp", KEY, data)
    for lang in ("es", "en"):
        with service.texts.use(lang):
            rows[lang].append(service._castle_waves_row(camp(service))[0])
    data["castle_waves"] = {"won": 3, "lost": 1, "tries": 1, "passed": True}
    service.store.put("camp", KEY, data)
    for lang in ("es", "en"):
        with service.texts.use(lang):
            rows[lang].append(service._castle_waves_row(camp(service)))
    assert rows["es"] == ["🌊 Oleadas crecientes: ganar 3 de 5 (empiezan solas con la próxima oleada; cada una, un 20 % más fuerte)",
                          "🌊 Oleadas crecientes: perdidas; vuelven a empezar en 24 h 0 min (hay que ganar 3 de 5)",
                          ("🌊 Oleadas crecientes: superadas (3 ganadas, 1 perdida)", True)]
    assert rows["en"] == ["🌊 Growing waves: win 3 of 5 (they start by themselves with the next wave; each one 20% stronger)",
                          "🌊 Growing waves: lost; they start again in 24 h 0 min (you need to win 3 of 5)",
                          ("🌊 Growing waves: passed (3 wins, 1 loss)", True)]
    every = service.act("test:1", "lvlall")
    assert any("y superar las 🌊 5 oleadas crecientes (ganar 3)." in line for line in every.body)
    assert any("and getting through the 🌊 5 growing waves (win 3)." in line for line in service.act("test:2", "lvlall").body)
    for lang in ("es", "en"):
        with service.texts.use(lang):
            values = service._faq_values()
            answers = service.texts.t("faq.d39.a", **values) + service.texts.t("faq.d42.a", **values)
            assert "{" not in answers and "5" in answers and "20" in answers
    assert values["castle_waves"] == 5 and values["castle_waves_pass"] == 3 and values["castle_waves_pct"] == 20
    assert values["castle_waves_retry"] == 3
    assert not service.texts.fallbacks.get("en") and not service.texts.missing


# ---------------------------------------------------------------- what does not change (D-64)


def test_an_existing_castle_and_lower_camps_are_unaffected(service, clock):
    make_hero(service, "test:1", "Lyra")
    camp_at_level(service, 9)                              # a castle from before 0.53: it never needed the waves
    service.act("test:1", "claro")
    assert service._castle_waves_row(camp(service)) is None and service._castle_wave_next(camp(service)) is None
    raid = wave(service, clock, ("test:1",), won=True)
    assert "wave" not in raid and "castle_waves" not in camp(service) and camp(service)["level"] == 9
    assert service.act("test:1", "lvlup").body == ["🏰 Tu campamento llegó a castillo: todavía no hay un nivel más."]
    data = camp(service)
    data["level"] = 7                                      # a city one level lower: normal waves, no row
    service.store.put("camp", KEY, data)
    raid = wave(service, clock, ("test:1",), won=False)
    assert "wave" not in raid and "castle_waves" not in camp(service)
    assert not any("Oleadas crecientes" in line for line in service.act("test:1", "lvlup").body)
    data = camp(service)
    data["level"] = 8                                      # the Noche de prueba is never a growing wave
    service.store.put("camp", KEY, data)
    set_rations(service, 30)
    service.act("test:1", "trial")
    trial = camp(service)["raid"]
    assert trial["kind"] == "trial" and "wave" not in trial
    service.content.balance["ladder"]["castle_waves"]["count"] = 0      # count 0 turns the rule off
    assert service._castle_waves_row(camp(service)) is None
    assert not any("Oleadas crecientes" in line for line in service.act("test:1", "lvlup").body)
    assert RAID_GAP < 3 * DAY                               # (the wait after a lost series skips one normal wave)
