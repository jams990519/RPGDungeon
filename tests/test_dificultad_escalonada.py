"""The waves' escalating difficulty (D-153, confirmed in E-37; how it was applied: D-337, provisional; 0.61).

[ES] Pruebas de la ⚔️ dificultad escalonada: la oleada NORMAL de un campamento empieza en la fuerza de siempre ("media", ×1) y
sube despacio con el nivel del campamento (+2 % por nivel, como mucho el de la ciudad) y con las semanas desde que se fundó
(+2,5 % por semana, tope +20 %); en el castillo "los enemigos ya saben dónde estás": la fuerza de la ciudad × 1,25. Se fija al
abrir la oleada y la 🛡️ Defensa frena después. La 🌙 Noche de prueba y las 🌊 oleadas crecientes del nivel 8 (D-329) quedan
igual. Un campamento de antes cuenta desde su fecha de fundación ("created"); sin ella, desde el parche. La línea ⚔️ Dificultad
se lee en los dos idiomas (_push_each para los avisos).
"""

import pytest

from conftest import make_hero
from engine.combat import make_combat
from engine.world import raids as raid_rules
from test_idiomas import english_hero
from test_raids import DAY, HOUR, KEY, camp, camp_at_level, open_raid, win

WEEK = 7 * DAY
CFG = {"base": 1.0, "per_level": 0.02, "per_week": 0.025, "time_cap": 0.2, "castle_mult": 1.25,
       "labels": {"media": 1.0, "alta": 1.15, "muy_alta": 1.45}}


def text(view):
    return "\n".join([view.notice or ""] + view.body)


def set_camp(service, **fields):
    data = camp(service)
    data.update(fields)
    service.store.put("camp", KEY, data)
    return data


def normal_enemy(service, raid):
    hero = service._load("test:1")
    return make_combat(raid["enemy"], service.content.enemies[raid["enemy"]], raid["level"], service._kit(hero), 1)["enemy"]


# ---------------------------------------------------------------- the numbers and the pure rules


def test_the_numbers_live_in_balance_and_the_pure_rules():
    from engine.core import load_content
    assert load_content().balance["raids"]["difficulty"] == CFG
    parts = raid_rules.difficulty_parts
    assert parts(1, 0, CFG, 9)["mult"] == pytest.approx(1.0)                    # a new camp: the wave of always, "media"
    assert parts(5, 0, CFG, 9)["level"] == pytest.approx(0.08)                  # +2 % per level after the 1st
    assert parts(8, 0, CFG, 9)["mult"] == pytest.approx(1.14)
    assert parts(1, 14, CFG, 9)["time"] == pytest.approx(0.05)                  # +2,5 % per week since founding
    assert parts(1, 8 * 7, CFG, 9)["time"] == pytest.approx(0.2)                # the cap at 8 weeks...
    assert parts(1, 1000, CFG, 9)["time"] == pytest.approx(0.2)                 # ...and never above
    castle = parts(9, 1000, CFG, 9)
    assert castle["level"] == pytest.approx(0.14) and castle["castle"] == 1.25  # the castle counts as the city, × 1,25
    assert castle["mult"] == pytest.approx((1 + 0.14 + 0.2) * 1.25)
    assert parts(8, 1000, CFG, 9)["mult"] < raid_rules.wave_mult(3, 0.2)        # before the castle, below the 3rd growing wave
    assert parts(3, -5, CFG, 9)["time"] == 0 and parts(3, 7, {"per_week": -1, "per_level": -1}, 9)["mult"] == 1.0
    assert parts(9, 30, None, 9) == {"level": 0.0, "time": 0.0, "castle": 1.0, "mult": 1.0}     # no block: as before 0.61
    label = raid_rules.difficulty_label
    assert [label(m, CFG["labels"]) for m in (1.0, 1.14, 1.15, 1.44, 1.45, 2.0)] == [
        "media", "media", "alta", "alta", "muy_alta", "muy_alta"]
    assert label(0.9, CFG["labels"]) == "media" and label(1.3, None) == "media"


# ---------------------------------------------------------------- it starts medium and grows


def test_a_new_camp_starts_at_the_base_strength(service, clock):
    make_hero(service, "test:1", "Lyra")
    camp_at_level(service, 1)
    assert camp(service)["created"] == pytest.approx(clock.now())               # just founded
    assert service._difficulty_parts(camp(service)) == {"level": 0.0, "time": 0.0, "castle": 1.0, "mult": 1.0}
    info = service.act("test:1", "campinfo")
    assert "⚔️ Dificultad: media ×1,00 (sube con el tiempo y el nivel: +0 % por el nivel, +0 % por el tiempo)" in info.body
    open_raid(service, clock, ("test:1",))                                       # the first wave, ~2 days after founding
    raid = camp(service)["raid"]
    days = (raid["at"] - camp(service)["created"]) / DAY
    assert raid["difficulty"] == pytest.approx(1 + 0.025 * days / 7, abs=1e-4) and raid["difficulty"] < 1.01
    assert "⚔️ Dificultad de esta oleada: media ×1,01 (+1 % de vida y de ataque)." in service.act("test:1", "claro").body
    fight = service.act("test:1", "defend")
    state = service.store.get("combat", "test:1")
    normal = normal_enemy(service, raid)
    assert raid.get("defense", 0) == 0                                           # no defenses yet: only the difficulty
    assert state["enemy"]["max_hp"] == max(1, round(normal["max_hp"] * raid["difficulty"]))
    assert "⚔️ Dificultad ×1,01: +1 % de vida y de ataque." in fight.notice
    assert not service.texts.missing


def test_growth_by_time_is_gentle_and_capped(service, clock):
    make_hero(service, "test:1", "Lyra")
    camp_at_level(service, 1)
    for weeks, expected in ((1, 1.025), (4, 1.10), (8, 1.20), (30, 1.20)):
        set_camp(service, created=clock.now() - weeks * WEEK)
        assert service._difficulty_parts(camp(service))["mult"] == pytest.approx(expected)
    lines = service.act("test:1", "campinfo").body
    assert "⚔️ Dificultad: alta ×1,20 (sube con el tiempo y el nivel: +0 % por el nivel, +20 % por el tiempo)" in lines


def test_growth_by_level(service, clock):
    make_hero(service, "test:1", "Lyra")
    camp_at_level(service, 1)
    set_camp(service, created=clock.now())
    seen = []
    for level in range(1, 9):
        set_camp(service, level=level)
        seen.append(round(service._difficulty_parts(camp(service))["mult"], 4))
    assert seen == [1.0, 1.02, 1.04, 1.06, 1.08, 1.10, 1.12, 1.14]               # stronger each level, gently
    # a higher camp level makes the next normal wave stronger (before 0.61 the level changed nothing: zone level + 1)
    set_camp(service, level=6)
    open_raid(service, clock, ("test:1",))
    raid = camp(service)["raid"]
    assert raid["kind"] == "raid" and "wave" not in raid and raid["difficulty"] > 1.10


def test_defenses_still_hold_the_wave_back_after_the_difficulty(service, clock):
    make_hero(service, "test:1", "Lyra")
    camp_at_level(service, 5)
    set_camp(service, created=clock.now() - 3 * WEEK)
    walls = [uid for uid, u in service._upgrade_catalog().items() if u.get("defense") and u.get("level", 1) <= 5]
    service.store.put("upgrades", KEY, {"built": {uid: 0.0 for uid in walls}, "works": {}, "tech": {}})
    open_raid(service, clock, ("test:1",))
    raid = camp(service)["raid"]
    weaken = service._raid_weaken(raid)
    assert raid["defense"] >= 6 and weaken < 1
    assert raid["difficulty"] * weaken < 1                                        # with its defenses, softer than a bare wave
    service.act("test:1", "defend")
    state = service.store.get("combat", "test:1")
    normal = normal_enemy(service, raid)
    assert state["enemy"]["max_hp"] == max(1, round(round(normal["max_hp"] * raid["difficulty"]) * weaken))
    assert state["enemy"]["attack"] == pytest.approx(normal["attack"] * raid["difficulty"] * weaken)


# ---------------------------------------------------------------- the castle: the enemies know where you are


def test_the_castle_multiplier_and_its_line(service, clock):
    make_hero(service, "test:1", "Lyra")
    camp_at_level(service, 9)
    set_camp(service, created=clock.now() - 20 * WEEK)
    parts = service._difficulty_parts(camp(service))
    assert parts["castle"] == 1.25 and parts["mult"] == pytest.approx((1 + 0.14 + 0.2) * 1.25)
    info = service.act("test:1", "campinfo").body
    assert ("⚔️ Dificultad: muy alta ×1,68 (sube con el tiempo y el nivel: +14 % por el nivel, +20 % por el tiempo; "
            "×1,25 por el castillo)") in info
    assert "👁️ Los enemigos saben dónde está tu castillo: las oleadas llegan más fuertes (+25 %)." in info
    open_raid(service, clock, ("test:1",))
    raid = camp(service)["raid"]
    assert raid["difficulty"] == pytest.approx(1.675) and "wave" not in raid     # a castle gets no growing waves (D-64)
    notice = [view for _, view in service.tick() if view.kind == "camp_raid"][0]
    assert "👁️ Los enemigos saben dónde está tu castillo: las oleadas llegan más fuertes (+25 %)." in notice.body
    service.act("test:1", "defend")
    state = service.store.get("combat", "test:1")
    normal = normal_enemy(service, raid)
    assert raid.get("defense", 0) == 0
    assert state["enemy"]["max_hp"] == max(1, round(normal["max_hp"] * 1.675))
    assert state["enemy"]["attack"] == pytest.approx(normal["attack"] * 1.675)


def test_the_step_to_the_castle_warns_about_it(service, clock):
    make_hero(service, "test:1", "Lyra")
    camp_at_level(service, 8)
    view = service.act("test:1", "lvlup")
    assert ("👁️ En el castillo los enemigos sabrán dónde está: las oleadas normales llegarán un 25 % más fuertes. "
            "Las defensas las frenan, como siempre.") in view.body
    set_camp(service, level=7)
    assert not any(line.startswith("👁️") for line in service.act("test:1", "lvlup").body)


# ---------------------------------------------------------------- what must not change


def test_the_growing_waves_and_the_trial_keep_their_own_strength(service, clock):
    make_hero(service, "test:1", "Lyra")
    camp_at_level(service, 8)
    set_camp(service, created=clock.now() - 20 * WEEK)                           # a lot of time: it would add +20 %
    assert any(line.startswith("⚔️ Dificultad: las 🌊 oleadas crecientes llevan su propia fuerza")
               for line in service.act("test:1", "campinfo").body)
    open_raid(service, clock, ("test:1",))
    raid = camp(service)["raid"]
    assert raid["wave"] == 1 and raid["wave_mult"] == pytest.approx(1.2) and "difficulty" not in raid     # D-329 unchanged
    service.act("test:1", "defend")
    state = service.store.get("combat", "test:1")
    normal = normal_enemy(service, raid)
    assert state["enemy"]["max_hp"] == max(1, round(normal["max_hp"] * 1.2))
    assert not any("Dificultad" in line for line in service.act("test:1", "claro").body)
    win(service, "test:1")
    clock.advance(HOUR + 1)
    service.act("test:1", "claro")
    # 🌙 the Noche de prueba: never a difficulty either
    service.act("test:1", "trial")
    trial = camp(service)["raid"]
    assert trial["kind"] == "trial" and "difficulty" not in trial
    service.act("test:1", "defend")
    state = service.store.get("combat", "test:1")
    sub = service.content.balance["raids"]["trial"]
    normal = normal_enemy(service, trial)
    assert state["enemy"]["max_hp"] == max(1, round(normal["max_hp"] * sub["enemy_hp_mult"]))
    assert state["enemy"]["attack"] == pytest.approx(normal["attack"] * sub["enemy_attack_mult"])


def test_after_passing_the_series_the_city_waves_take_the_difficulty(service, clock):
    make_hero(service, "test:1", "Lyra")
    camp_at_level(service, 8)
    set_camp(service, created=clock.now() - 2 * WEEK, castle_waves={"won": 3, "lost": 0, "passed": True})
    open_raid(service, clock, ("test:1",))
    raid = camp(service)["raid"]
    assert "wave" not in raid and raid["difficulty"] == pytest.approx(1.14 + 0.025 * (raid["at"] - camp(service)["created"])
                                                                      / WEEK, abs=1e-4)


# ---------------------------------------------------------------- camps from before the patch (D-64)


def test_an_existing_camp_after_the_patch(service, clock):
    make_hero(service, "test:1", "Lyra")
    camp_at_level(service, 4)
    # a camp founded 3 weeks ago counts from its founding date ("created", stored by every camp)
    set_camp(service, created=clock.now() - 3 * WEEK)
    assert service._difficulty_parts(camp(service))["time"] == pytest.approx(0.075)
    # a raid opened before the patch has no "difficulty": it keeps the strength it had (×1) and says nothing new
    data = set_camp(service)
    now = clock.now()
    data["raid"] = {"kind": "raid", "at": now, "until": now + HOUR, "required": 1, "wins": 0, "fights": {},
                    "enemy": "lobo_gris", "level": 2, "defense": 0}
    service.store.put("camp", KEY, data)
    assert not any("Dificultad" in line for line in service.act("test:1", "claro").body)
    service.act("test:1", "defend")
    state = service.store.get("combat", "test:1")
    assert state["enemy"]["max_hp"] == normal_enemy(service, camp(service)["raid"])["max_hp"]
    win(service, "test:1")
    clock.advance(HOUR + 1)
    service.act("test:1", "claro")
    # a camp without a founding date counts its weeks from the patch: the first time the raid clock sees it
    data = camp(service)
    data.pop("created")
    service.store.put("camp", KEY, data)
    service.act("test:1", "hero")
    assert camp(service)["difficulty_from"] == pytest.approx(clock.now())
    assert service._difficulty_parts(camp(service))["time"] == 0
    clock.advance(2 * WEEK)
    assert service._difficulty_parts(camp(service))["time"] == pytest.approx(0.05)
    service.act("test:1", "hero")
    assert camp(service)["difficulty_from"] == pytest.approx(clock.now() - 2 * WEEK)     # written once
    assert camp(service)["level"] == 4 and camp(service)["members"] == ["test:1"]          # nothing else changed


# ---------------------------------------------------------------- both languages


def test_the_difficulty_line_in_both_languages(service, clock):
    english_hero(service, "test:1", "Lyra")
    make_hero(service, "test:2", "Bram")
    camp_at_level(service, 9, ("test:1", "test:2"))
    set_camp(service, created=clock.now() - 4 * WEEK)
    info = service.act("test:1", "campinfo").body
    assert ("⚔️ Difficulty: muy alta ×1.55 (grows with time and level: +14% for the level, +10% for time; ×1.25 for the castle)"
            .replace("muy alta", "very high") in info)
    assert "👁️ The enemies know where your castle is: the waves come stronger (+25%)." in info
    spanish = service.act("test:2", "campinfo").body
    assert ("⚔️ Dificultad: muy alta ×1,55 (sube con el tiempo y el nivel: +14 % por el nivel, +10 % por el tiempo; "
            "×1,25 por el castillo)") in spanish
    # 🗼 the watchtower's warning carries the line, to each member in their language (_push_each)
    service.store.put("upgrades", KEY, {"built": {"torre_vigia": 0.0}, "works": {}, "tech": {}})
    due = camp(service)["next_raid_at"]
    clock.advance(due - clock.now() - 3 * HOUR)                                 # both play (active), the tower not yet
    for member in ("test:1", "test:2"):
        service.act(member, "hero")
    clock.advance(2 * HOUR)                                                      # 1 hour before: the tower sees it
    service.act("test:1", "hero")
    watch = {acc: view for acc, view in service.tick() if view.kind == "camp_watch"}
    assert any(line.startswith("⚔️ Difficulty: very high") for line in watch["test:1"].body)
    assert any(line.startswith("⚔️ Dificultad: muy alta") for line in watch["test:2"].body)
    # ❓ /d66 in both languages, with every number filled in
    english = text(service.text("test:1", "/d66"))
    assert "Yes, slowly" in english and "2.5% for each week" in english and "{" not in english
    spanish = text(service.text("test:2", "/d66"))
    assert "Sí, despacio" in spanish and "2,5 % por cada semana" in spanish and "25 % más fuertes" in spanish
    assert "{" not in spanish
    assert not service.texts.missing
