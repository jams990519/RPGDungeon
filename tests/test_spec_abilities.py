"""8 abilities per specialization, unlocks spread over 100 levels and the player's own combat bar (D-79).

[ES] Pruebas de las 8 habilidades por especialización, su desbloqueo por puntos y la barra de combate elegible.
"""

from conftest import make_hero
from engine.classes import bar_choices, bar_slots, base_response, ensure_talents, kit, set_bar_slot, spend_point, specs_of
from engine.combat import CombatContext, make_combat, resolve_round
from engine.core import Texts
from engine.hero import Hero

KINDS = {"strike", "finisher", "interrupt", "heal", "hot", "dot", "empower", "expose", "weaken", "response"}


def active(content):
    return {cid: c for cid, c in content.classes.items() if not c.get("retired")}


def hero_with_points(content, spec, points, level=None):
    hero = Hero(id="t", name="T", class_id=spec, level=1)
    ensure_talents(content.classes, content.balance, hero)
    hero.level = level or points + 1
    hero.points = points
    while hero.points:
        spend_point(content.classes, content.balance, hero, spec)
    return hero


def test_every_active_spec_has_eight_abilities_with_unique_ids_and_texts(content):
    t = Texts(content.texts)
    ids = [a["id"] for c in content.classes.values() for a in c["abilities"]]
    assert len(ids) == len(set(ids))
    for cid, cdef in active(content).items():
        assert len(cdef["abilities"]) == 8, cid
        for ability in cdef["abilities"]:
            assert ability["kind"] in KINDS, (cid, ability["id"])
            if ability["kind"] == "response":
                assert ability["response"] in ("block", "dodge", "shield"), ability["id"]
            if ability["kind"] == "finisher":
                assert cdef["attack"].get("combo") or any(a.get("combo") for a in cdef["abilities"]), ability["id"]
            assert t.has(f"ability.{ability['id']}.name"), ability["id"]


def test_every_class_keeps_at_least_two_roles(content):
    groups = {c.get("group", cid) for cid, c in active(content).items()}
    for group in groups:
        roles = {content.classes[s]["role"] for s in specs_of(content.classes, group)}
        assert len(roles) >= 2, group


def test_unlock_table_has_eight_rising_steps_inside_100_levels(content):
    steps = content.balance["talents"]["unlock"]
    assert len(steps) == 8 and steps == sorted(steps) and len(set(steps)) == 8
    assert steps[-1] < content.balance["hero"]["max_level"]


def test_points_unlock_abilities_in_order(content):
    steps = content.balance["talents"]["unlock"]
    for spec in ("guerrero_furia", "mago_fuego", "bardo_trovador"):
        abilities = [a["id"] for a in content.classes[spec]["abilities"]]
        for points in (1, 9, 10, 33, 46):
            hero = hero_with_points(content, spec, points)
            expected = [a for a, need in zip(abilities, steps) if points >= need]
            free = base_response(content.classes, content.classes[spec]["group"])   # every hero starts with it
            assert all(a in hero.unlocked for a in expected), (spec, points)
            assert not any(a in hero.unlocked for a, need in zip(abilities, steps) if points < need and a != free), (spec, points)


def test_automatic_bar_has_a_response_first_and_a_damage_ability(content):
    for spec in active(content):
        hero = hero_with_points(content, spec, 46)
        bar = kit(content.classes, content.balance, hero)["abilities"]
        assert len(bar) == 3 and bar[0]["kind"] == "response", spec
        if any(a["kind"] in ("strike", "finisher", "dot") for a in content.classes[spec]["abilities"]):
            assert any(a["kind"] in ("strike", "finisher", "dot") for a in bar[1:]), spec


def test_chosen_bar_is_used_and_slot_one_must_be_a_response(content):
    hero = hero_with_points(content, "guerrero_furia", 24)
    assert bar_slots(content.classes, hero) == ["reflejo_de_hechizos", "sed_de_sangre", "temeridad"]   # automatic
    assert set_bar_slot(content.classes, hero, 2, "golpe_colosal")
    assert set_bar_slot(content.classes, hero, 3, "ejecutar")
    assert set_bar_slot(content.classes, hero, 1, "parada")
    assert not set_bar_slot(content.classes, hero, 1, "temeridad")         # slot 1 only takes a response
    assert not set_bar_slot(content.classes, hero, 2, "desenfreno")        # not unlocked yet (46 points)
    assert not set_bar_slot(content.classes, hero, 2, "parada")            # already in slot 1
    assert hero.bar == ["parada", "golpe_colosal", "ejecutar"]
    assert [a["id"] for a in kit(content.classes, content.balance, hero)["abilities"]] == hero.bar
    # Swapping: putting slot 3's ability in slot 2 moves the old one to slot 3.
    assert set_bar_slot(content.classes, hero, 2, "ejecutar")
    assert bar_slots(content.classes, hero) == ["parada", "ejecutar", "golpe_colosal"]
    # Slot 1 choices are only responses; slots 2-3 never offer slot 1's ability.
    assert bar_choices(content.classes, hero, 1) == ["reflejo_de_hechizos"]
    assert "parada" not in bar_choices(content.classes, hero, 2)


def test_invalid_saved_bar_falls_back_to_the_automatic_one(content):
    hero = hero_with_points(content, "guerrero_furia", 24)
    auto = bar_slots(content.classes, hero)
    for bad in (["ejecutar", "parada", "golpe_colosal"], ["no_existe"], ["parada", "parada"], ["parada", "desenfreno"]):
        hero.bar = bad
        assert bar_slots(content.classes, hero) == auto, bad
    hero.bar = ["parada"]                       # valid but short: the free slots are filled
    slots = bar_slots(content.classes, hero)
    assert slots[0] == "parada" and len(slots) == 3 and len(set(slots)) == 3


def test_old_hero_keeps_its_abilities_and_gets_what_its_points_pay_for(service, content):
    make_hero(service, class_id="guerrero")
    data = service.store.get("hero", "test:1")
    # A hero saved before D-79: 12 points in Furia, the old 3 abilities unlocked, no bar field.
    data.update({"level": 13, "class_id": "guerrero_furia", "talents": {"guerrero_furia": 12},
                 "unlocked": ["bloqueo_escudo", "golpe_colosal", "ejecutar", "parada"]})
    data.pop("bar", None)
    service.store.put("hero", "test:1", data)
    hero = service._load("test:1")
    assert hero.unlocked[:4] == ["bloqueo_escudo", "golpe_colosal", "ejecutar", "parada"]
    assert "sed_de_sangre" in hero.unlocked                     # 4th ability: 10 points
    assert "reflejo_de_hechizos" not in hero.unlocked           # 5th ability: 16 points
    assert hero.bar == []
    assert service._kit(hero)["abilities"][0]["kind"] == "response"


def test_passive_bonus_is_small_at_level_five(content):
    for spec in ("guerrero_furia", "guerrero", "paladin_sagrado", "guerrero_senor_guerra"):
        hero = hero_with_points(content, spec, 4, level=5)
        bonus = kit(content.classes, content.balance, hero)["talent_bonus"]
        assert 0 < bonus["attack"] + bonus["hp"] <= 0.05, (spec, bonus)
    hero = hero_with_points(content, "guerrero_furia", 99, level=100)
    assert kit(content.classes, content.balance, hero)["talent_bonus"]["attack"] <= 0.5 + 1e-9


def test_bar_screens_respect_button_limits(service, content):
    make_hero(service, class_id="guerrero")
    data = service.store.get("hero", "test:1")
    data.update({"level": 60, "points": 59})
    service.store.put("hero", "test:1", data)
    for _ in range(59):
        service.act("test:1", "pt:guerrero_furia")
    talents = service.act("test:1", "talents")
    assert talents.actions[0].id == "bar" and len(talents.actions) <= 4
    bar = service.act("test:1", "bar")
    assert bar.kind == "bar" and len(bar.actions) == 4
    seen = set()
    for slot in (1, 2, 3):
        view = service.act("test:1", f"barslot:{slot}")
        for _ in range(6):
            assert len(view.actions) <= 4
            seen.update(a.id for a in view.actions if a.id.startswith("barset:"))
            more = [a for a in view.actions if a.id.startswith("barslot:")]
            if not more:
                break
            view = service.act("test:1", more[0].id)
    auto = service._load("test:1")
    assert bar_slots(service.content.classes, auto) == ["reflejo_de_hechizos", "desenfreno", "regeneracion_enfurecida"]
    assert "barset:2:golpe_colosal" in seen and "barset:1:parada" in seen and "barset:3:temeridad" in seen
    done = service.act("test:1", "barset:2:golpe_colosal")
    assert "🎛️" in (done.notice or "")
    assert service._load("test:1").bar == ["reflejo_de_hechizos", "golpe_colosal", "regeneracion_enfurecida"]
    assert not service.texts.missing


def test_callback_ids_fit_telegram(content):
    longest = max(len(f"barset:3:{a['id']}".encode()) for c in content.classes.values() for a in c["abilities"])
    assert longest <= 64


def test_spec_view_lists_eight_abilities_and_the_next_unlock(service):
    make_hero(service, class_id="guerrero")
    data = service.store.get("hero", "test:1")
    data.update({"level": 12, "points": 11})
    service.store.put("hero", "test:1", data)
    for _ in range(11):
        view = service.act("test:1", "pt:guerrero_furia")
    lines = [line for line in view.body if line.startswith(("🔓", "🔒"))]
    assert len(lines) == 8 and sum(line.startswith("🔓") for line in lines) == 4
    assert any("16" in line and "Reflejo" in line for line in view.body if line.startswith("Siguiente"))
    assert not service.texts.missing


def test_every_ability_has_a_short_effect_line(service, content):
    for cdef in active(content).values():
        for ability in cdef["abilities"]:
            text = service._ability_effect(ability, cdef["resource"])
            assert text and "{" not in text, ability["id"]
    assert not service.texts.missing


def test_builders_give_resource_and_combo_points(content):
    ctx = CombatContext(content.classes, content.enemies, content.items, content.balance, Texts(content.texts))
    cdef = dict(content.classes["picaro"])
    mutilar = next(a for a in cdef["abilities"] if a["id"] == "mutilar")
    cdef["abilities"] = [mutilar]
    hero = Hero(id="t", name="T", class_id="picaro", level=5, hp=500)
    state = make_combat("tortuga_musgosa", content.enemies["tortuga_musgosa"], 1, cdef, seed=3)
    resolve_round(state, hero, cdef, {"type": "ability", "index": 0}, ctx)
    assert state["hero"]["combo"] == 2
    cdef = dict(content.classes["guerrero_furia"])
    sed = next(a for a in cdef["abilities"] if a["id"] == "sed_de_sangre")
    cdef["abilities"] = [sed]
    hero = Hero(id="t", name="T", class_id="guerrero_furia", level=5, hp=500)
    state = make_combat("tortuga_musgosa", content.enemies["tortuga_musgosa"], 1, cdef, seed=3)
    resolve_round(state, hero, cdef, {"type": "ability", "index": 0}, ctx)
    assert state["hero"]["resource"] == 15 and state["hero"]["cooldowns"].get("sed_de_sangre")
