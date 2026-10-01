"""Talents by level (D-68) and max 3 specs per class (D-69). [ES] Pruebas de talentos por nivel."""

from conftest import make_hero
from engine.classes import specs_of


def test_every_class_has_at_most_three_specs(content):
    groups = {c.get("group", cid) for cid, c in content.classes.items() if not c.get("retired")}
    for group in groups:
        assert 1 <= len(specs_of(content.classes, group)) <= 3, group


def test_new_hero_starts_with_attack_and_one_response(service):
    make_hero(service, class_id="picaro")
    hero = service._load("test:1")
    abilities = service._kit(hero)["abilities"]
    assert len(abilities) == 1 and abilities[0]["kind"] == "response"
    assert hero.points == 0


def test_level_up_gives_point_and_point_unlocks_ability(service):
    make_hero(service, class_id="guerrero")
    hero = service.store.get("hero", "test:1")
    hero["backpack"].update({"madera": 40, "fibra": 30})   # 70 units x 2 xp -> level 2
    service.store.put("hero", "test:1", hero)
    service.act("test:1", "donate")
    hero = service._load("test:1")
    assert hero.level >= 2 and hero.points >= 1
    view = service.act("test:1", "pt:guerrero_furia")
    hero = service._load("test:1")
    assert hero.talents == {"guerrero_furia": 1}
    assert hero.class_id == "guerrero_furia"            # main spec follows the points
    kit = service._kit(hero)
    assert len(kit["abilities"]) == 2 and any(a["kind"] == "response" for a in kit["abilities"])
    assert "🌟" in (view.notice or "")


def test_retired_spec_is_migrated(service):
    make_hero(service, class_id="druida_feral")
    hero = service.store.get("hero", "test:1")
    hero["class_id"] = "druida_equilibrio"
    hero["talents"] = {"druida_equilibrio": 2}
    service.store.put("hero", "test:1", hero)
    hero = service._load("test:1")
    assert hero.class_id != "druida_equilibrio" and hero.points == 2 and "druida_equilibrio" not in hero.talents


def test_every_spec_has_a_unique_icon(content):
    icons = [c["icon"] for c in content.classes.values() if not c.get("retired")]
    assert all(icons) and len(icons) == len(set(icons))
