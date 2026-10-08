"""Talents by level (D-68) and max 3 specs per class (D-69). [ES] Pruebas de talentos por nivel."""

import pytest

from conftest import legacy_content, make_hero
from engine.classes import specs_of


@pytest.fixture
def content():
    """0.31: these tests cover the old talent and bar system (D-79), still in the code for the retired specs."""
    return legacy_content()


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
    hero = service._load("test:1")
    service._give_xp(hero, 2 * service.content.balance["hero"]["xp_formula"]["base"])   # enough for level 2
    service._save(hero)
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


def test_respec_refunds_points_for_gold(service):
    make_hero(service, class_id="guerrero")
    hero = service.store.get("hero", "test:1")
    hero.update({"level": 3, "points": 2, "gold": 100})
    service.store.put("hero", "test:1", hero)
    service.act("test:1", "pt:guerrero_furia")
    service.act("test:1", "pt:guerrero")
    view = service.act("test:1", "respec")
    hero = service._load("test:1")
    assert hero.talents == {} and hero.points == 2 and hero.gold == 100 - 30
    assert "🔄" in (view.notice or "")


def test_double_spec_after_dedication_paid_with_bags(service):
    from conftest import make_hero
    make_hero(service, "test:1", "Lyra", "guerrero")
    hero = service._load("test:1")
    hero.level, hero.points = 12, 11
    service._save(hero)
    view = service.act("test:1", "dual")
    assert view.kind == "dual" and not any(a.id == "dual_unlock" for a in view.actions)
    for _ in range(10):
        service.act("test:1", f"pt:{hero.class_id}")
    hero = service._load("test:1")
    hero.bags = 3
    service._save(hero)
    view = service.act("test:1", "dual_unlock")
    hero = service._load("test:1")
    assert hero.dual_unlocked and hero.bags == 0 and len(view.actions) <= 4
    first = (hero.class_id, dict(hero.talents))
    service.act("test:1", "dual_switch")
    hero = service._load("test:1")
    assert hero.profile == 2 and hero.talents == {} and hero.points == 11
    other = [s for s in specs_of(service.content.classes, "guerrero") if s != first[0]][0]
    service.act("test:1", f"pt:{other}")
    service.act("test:1", "dual_switch")
    hero = service._load("test:1")
    assert (hero.class_id, hero.talents) == first and hero.points == 1
    service.act("test:1", "dual_switch")
    hero = service._load("test:1")
    assert hero.talents == {other: 1} and hero.points == 10
