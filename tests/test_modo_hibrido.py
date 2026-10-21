"""The 🔀 hybrid mode of level 10 (0.54, D-231, D-312; how it was built: D-330).

[ES] Pruebas del modo híbrido: desde el nivel chain.hybrid.level (10) y con el segundo rol abierto, cada uno de los 3 botones
de rol (Constructor, Preparador, Gastador) se cambia por el del mismo puesto del otro rol de la clase (D-312: los 3; el Básico
no cambia y siguen 4 botones). No se ofrece antes del nivel ni sin segundo rol (D-287: ni botón ni línea; un /hibrido recibe un
aviso corto); cada puesto se cambia y se devuelve; el combate usa la habilidad prestada con sus números y sus marcas (daño,
curación, agro) y el cuerpo del rol activo, con una semilla fija; la elección se guarda (por pareja de roles) y vuelve al
recargar; cada rol guarda la suya al cambiar de rol; no se toca en una pelea; quien nunca lo toca pelea igual que antes; las
6 clases (también el Paladín sanador y DPS, D-233) tienen pareja en los 3 puestos, y un puesto sin pareja sale con "—" y no se
cambia. Ningún texto falta, en los dos idiomas.
Archivo: tests/test_modo_hibrido.py · Módulo: M3 Clases y talentos (y M5 Combate) · Prueba: engine/classes/talents.py
(hybrid_open, hybrid_pairs, hybrid_choice, toggle_hybrid, chain_bar, kit), engine/service/game.py (_hybrid_view,
_hybrid_action, _bar_view, _chain_talents_view, _level_point_lines), engine/hero/hero.py (Hero.hybrid),
content/balance.yaml (chain.hybrid).
"""

import copy

import pytest

from conftest import make_hero
from engine.classes import (
    HYBRID_LINKS,
    chain_bar,
    hybrid_choice,
    hybrid_open,
    hybrid_pairs,
    hybrid_partner,
    is_chain_spec,
    kit,
    specs_of,
    switch_role,
    sync_chain,
    toggle_hybrid,
)
from engine.combat import CombatContext, make_combat, resolve_round
from engine.core import FixedClock, MemoryStore, Rng, Texts
from engine.hero import Hero, hero_stats
from engine.service import GameService


def ids(view):
    return [a.id for a in view.actions]


def body(view):
    return "\n".join(view.body)


def hero_at(service, level, class_id="guerrero_tanque"):
    """A hero of that role at that level (saved)."""
    make_hero(service, class_id=class_id)
    hero = service._load("test:1")
    hero.level = level
    service._save(hero)
    return service._load("test:1")


def chain_specs(content):
    return [cid for cid, cdef in content.classes.items() if is_chain_spec(content.classes, cid) and not cdef.get("retired")]


# ---------------------------------------------------------------- when it is offered


def test_not_offered_before_level_ten(service, content):
    assert content.balance["chain"]["hybrid"]["level"] == 10 and content.balance["chain"]["hybrid"]["max_mixed"] == 3
    hero = hero_at(service, 9)
    assert not hybrid_open(content.classes, content.balance, hero)
    bar = service.act("test:1", "bar")
    assert "hyb" not in ids(bar) and "🔀" not in body(bar)                 # D-287: nothing announced before its level
    assert "🔀" not in body(service.act("test:1", "talents"))
    locked = service.act("test:1", "hyb")                                   # a typed /hibrido: a short reply
    assert locked.kind == "talents" and "nivel 10" in locked.notice
    service.act("test:1", "hyb:H1")
    assert service._load("test:1").hybrid == {}
    assert service.text("test:1", "/hibrido").kind == "talents"
    hero = service._load("test:1")
    hero.level = 10
    service._save(hero)
    bar = service.act("test:1", "bar")
    assert ids(bar) == ["hyb", "talents"] and len(bar.actions) <= 4
    assert service.act("test:1", "hyb").kind == "hybrid"
    assert service.text("test:1", "/hybrid").kind == "hybrid"
    assert not service.texts.missing


def test_not_offered_without_a_second_role(content):
    content.balance["chain"]["second_role_level"] = 20                     # in memory only: the second role comes later
    service = GameService(content, MemoryStore(), FixedClock(), world_seed=12345, time_scale=1.0)
    hero = hero_at(service, 12)
    assert not hybrid_open(content.classes, content.balance, hero)
    assert "hyb" not in ids(service.act("test:1", "bar"))
    assert service.act("test:1", "hyb").kind == "talents"
    assert not toggle_hybrid(content.classes, content.balance, hero, "H1")


def test_reaching_level_ten_says_it_once(service, content):
    hero = hero_at(service, 9)
    assert not any("modo híbrido" in line for line in service._level_point_lines(hero))
    hero.level = 10
    assert any("modo híbrido" in line for line in service._level_point_lines(hero))
    hero.level = 11
    assert not any("modo híbrido" in line for line in service._level_point_lines(hero))


# ---------------------------------------------------------------- toggling


def test_each_of_the_three_slots_toggles(service, content):
    hero_at(service, 10)
    view = service.act("test:1", "hyb")
    assert view.kind == "hybrid" and ids(view) == ["hyb:H1", "hyb:H2", "hyb:H3", "bar"]
    dps = content.classes["guerrero_dps"]["abilities"]
    tank = content.classes["guerrero_tanque"]["abilities"]
    for index, link in enumerate(HYBRID_LINKS):
        view = service.act("test:1", f"hyb:{link}")
        hero = service._load("test:1")
        assert link in hybrid_choice(content.classes, content.balance, hero) and "🔀" in view.notice
        assert [a["id"] for a in chain_bar(content.classes, content.balance, hero)][index] == dps[index]["id"]
    hero = service._load("test:1")
    assert hero.hybrid == {"guerrero_tanque>guerrero_dps": ["H1", "H2", "H3"]}
    assert [a["id"] for a in kit(content.classes, content.balance, hero)["abilities"]] == [a["id"] for a in dps]
    for index, link in enumerate(HYBRID_LINKS):                             # and back, one by one
        view = service.act("test:1", f"hyb:{link}")
        hero = service._load("test:1")
        assert link not in hybrid_choice(content.classes, content.balance, hero) and "↩️" in view.notice
        assert [a["id"] for a in chain_bar(content.classes, content.balance, hero)][index] == tank[index]["id"]
    assert service._load("test:1").hybrid == {}                             # back to the role's bar: nothing saved
    assert not service.texts.missing


def test_the_screen_lists_current_and_alternative_and_marks_the_bar(service):
    hero_at(service, 10)
    view = service.act("test:1", "hyb")
    text = body(view)
    assert "✅ Revés · o Golpe heroico" in text and "Golpe de escudo (no cambia)" in text
    service.act("test:1", "hyb:H3")
    view = service.act("test:1", "hyb")
    assert "🔀 Ejecutar (de 🦏 Guerrero · DPS) · o Grito de dominio" in body(view)
    assert "💥 Usar Grito de dominio" in [a.label for a in view.actions]
    bar = service.act("test:1", "bar")
    assert any("Ejecutar" in line and "🔀 de 🦏 Guerrero · DPS" in line for line in bar.body)
    talents = service.act("test:1", "talents")
    assert "1 de 3" in body(talents)


def test_max_mixed_limits_how_many(content):
    content.balance["chain"]["hybrid"]["max_mixed"] = 1                    # in memory only
    service = GameService(content, MemoryStore(), FixedClock(), world_seed=12345, time_scale=1.0)
    hero_at(service, 10)
    service.act("test:1", "hyb:H1")
    view = service.act("test:1", "hyb:H2")
    assert "máximo" in view.notice and service._load("test:1").hybrid == {"guerrero_tanque>guerrero_dps": ["H1"]}
    assert "hasta 1" in body(view)
    content.balance["chain"]["hybrid"]["max_mixed"] = None                  # null: not offered (as before 0.54)
    assert not hybrid_open(content.classes, content.balance, service._load("test:1"))
    assert chain_bar(content.classes, content.balance, service._load("test:1")) == content.classes["guerrero_tanque"]["abilities"]


# ---------------------------------------------------------------- the 4th button, the body, the tags


def test_the_basic_button_never_changes(service, content):
    hero = hero_at(service, 10)
    for link in HYBRID_LINKS:
        toggle_hybrid(content.classes, content.balance, hero, link)
    cdef = kit(content.classes, content.balance, hero)
    assert cdef["attack"] == content.classes["guerrero_tanque"]["attack"]
    assert len(cdef["abilities"]) == 3 and [a["link"] for a in cdef["abilities"]] == list(HYBRID_LINKS)
    service._save(hero)
    hero = service._load("test:1")
    service._start_combat(hero, service._zone(1, 0), Rng(5), "encounter.ambush")
    service._save(hero)
    view = service.view("test:1")
    assert view.kind == "combat" and len(view.actions) <= 6
    assert view.actions[0].id == "atk" and "Golpe de escudo" in view.actions[0].label
    assert "Golpe heroico" in view.actions[1].label and "Ejecutar" in view.actions[3].label


def test_the_body_and_the_chain_stay_the_active_roles(service, content):
    hero = hero_at(service, 30)
    plain = kit(content.classes, content.balance, hero)
    for link in HYBRID_LINKS:
        toggle_hybrid(content.classes, content.balance, hero, link)
    mixed = kit(content.classes, content.balance, hero)
    assert mixed["base"] == content.classes["guerrero_tanque"]["base"] and mixed["role"] == "defensa"
    assert mixed["talent_bonus"] == plain["talent_bonus"]                  # the passive of the active role's points
    assert hero_stats(mixed, hero.level) == hero_stats(plain, hero.level)
    assert hero.talents == {"guerrero_tanque": 29}                           # D-238.4: points stay with the role


def test_a_borrowed_ability_keeps_its_own_tags(service, content):
    hero = hero_at(service, 10, "guerrero_dps")                             # a DPS borrowing the tank's buttons
    for link in HYBRID_LINKS:
        toggle_hybrid(content.classes, content.balance, hero, link)
    borrowed = kit(content.classes, content.balance, hero)["abilities"]
    tank = content.classes["guerrero_tanque"]["abilities"]
    for mine, theirs in zip(borrowed, tank):
        assert {k: v for k, v in mine.items() if k != "from_spec"} == theirs and mine["from_spec"] == "guerrero_tanque"
    assert borrowed[0]["threat"] == 1.0 and borrowed[2]["threat"] == 2.0     # the agro marks travel with the ability (D-312)
    assert "from_spec" not in content.classes["guerrero_tanque"]["abilities"][0]   # the content is never changed


# ---------------------------------------------------------------- combat


def fight(content, hero, choices, seed=4242, tame=False):
    """Play these choices against a sturdy wolf with a fixed seed (tame: it does not hurt); returns the state and the logs."""
    ctx = CombatContext(content.classes, content.enemies, content.items, content.balance, Texts(content.texts))
    cdef = kit(content.classes, content.balance, hero)
    state = make_combat("lobo_ceniciento", content.enemies["lobo_ceniciento"], hero.level, cdef, seed)
    state["enemy"]["hp"] = state["enemy"]["max_hp"] = 100_000
    if tame:
        state["enemy"]["attack"] = 0.0
    logs = []
    for choice in choices:
        state["hero"]["resource"] = 20                                     # enough energy for any button
        resolve_round(state, hero, cdef, choice, ctx)
        logs.append(list(state["log"]))
    return state, logs


def chain_hero(content, spec, level=10):
    hero = Hero(id="x", name="X", class_id=spec, level=level)
    sync_chain(content.classes, hero)
    hero.hp = hero_stats(kit(content.classes, content.balance, hero), level)["max_hp"]
    return hero


def test_combat_uses_the_swapped_ability_with_a_fixed_seed(content):
    spender = {"type": "ability", "index": 2}
    plain = chain_hero(content, "guerrero_tanque")
    state, logs = fight(content, plain, [spender])
    assert state["hero"].get("guard") and any("Grito de dominio" in line for line in logs[0])
    mixed = chain_hero(content, "guerrero_tanque")
    assert toggle_hybrid(content.classes, content.balance, mixed, "H3")
    state, logs = fight(content, mixed, [spender])
    assert not state["hero"].get("guard")                                   # Ejecutar hits, it does not guard
    assert any("Ejecutar" in line for line in logs[0]) and state["enemy"]["hp"] < 100_000
    again, logs_again = fight(content, mixed, [spender])                    # the same seed gives the same fight
    assert again["enemy"]["hp"] == state["enemy"]["hp"] and logs_again == logs


def test_a_borrowed_heal_heals_and_follows_the_active_chain(content):
    hero = chain_hero(content, "paladin_dps")                               # D-233: Paladín DPS borrowing the healer's spender
    assert toggle_hybrid(content.classes, content.balance, hero, "H3")
    hero.hp = 10
    state, logs = fight(content, hero, [{"type": "ability", "index": 0}, {"type": "ability", "index": 1},
                                        {"type": "ability", "index": 2}], tame=True)
    assert any("Luz del alba" in line for line in logs[2]) and any("Cobras" in line for line in logs[2])   # combo: DPS order
    assert hero.hp > 10 and state["outcome"] is None


def test_automatic_fights_play_a_mixed_bar(content):
    from engine.combat import play_out
    ctx = CombatContext(content.classes, content.enemies, content.items, content.balance, Texts(content.texts))
    for spec in chain_specs(content):
        hero = chain_hero(content, spec)
        for link in HYBRID_LINKS:
            toggle_hybrid(content.classes, content.balance, hero, link)
        cdef = kit(content.classes, content.balance, hero)
        state = make_combat("lobo_ceniciento", content.enemies["lobo_ceniciento"], 3, cdef, 7)
        play_out(state, hero, cdef, ctx)
        assert state["outcome"] in ("victory", "defeat", "fled") or state["round"] > 1, spec


# ---------------------------------------------------------------- saving, roles, combat lock


def test_the_choice_survives_a_reload(content):
    store = MemoryStore()
    service = GameService(content, store, FixedClock(), world_seed=12345, time_scale=1.0)
    hero_at(service, 10)
    service.act("test:1", "hyb:H2")
    again = GameService(content, store, FixedClock(), world_seed=12345, time_scale=1.0)
    hero = again._load("test:1")
    assert hero.hybrid == {"guerrero_tanque>guerrero_dps": ["H2"]}
    assert again._kit(hero)["abilities"][1]["id"] == "guerrero_desgarrar_armadura"
    assert Hero.from_dict({"id": "x", "name": "X", "class_id": "guerrero_tanque"}).hybrid == {}   # old heroes load


def test_each_role_keeps_its_own_choice(service, content):
    hero_at(service, 10)
    service.act("test:1", "hyb:H2")                                         # as a tank: borrow the DPS's H2
    service.act("test:1", "role:guerrero_dps")
    hero = service._load("test:1")
    assert hero.class_id == "guerrero_dps" and hybrid_choice(content.classes, content.balance, hero) == []
    service.act("test:1", "hyb:H1")                                         # as a DPS: borrow the tank's H1
    service.act("test:1", "role:guerrero_tanque")
    hero = service._load("test:1")
    assert hybrid_choice(content.classes, content.balance, hero) == ["H2"]
    assert hero.hybrid == {"guerrero_tanque>guerrero_dps": ["H2"], "guerrero_dps>guerrero_tanque": ["H1"]}
    assert switch_role(content.classes, content.balance, hero, "guerrero_dps")
    assert [a["id"] for a in kit(content.classes, content.balance, hero)["abilities"]][0] == "guerrero_reves"


def test_blocked_in_combat(service, content):
    hero = hero_at(service, 10)
    service._start_combat(hero, service._zone(1, 0), Rng(5), "encounter.ambush")
    service._save(hero)
    for action in ("hyb", "hyb:H1", "bar"):
        view = service.act("test:1", action)
        assert view.kind == "combat" and "combate" in (view.notice or "")
    assert service.text("test:1", "/hibrido").kind == "combat"
    hero = service._load("test:1")
    view = service._hybrid_action(hero, "hyb:H1")                            # even through another door
    assert view.kind == "combat" and hero.hybrid == {}


def test_who_never_uses_it_fights_as_before(service, content):
    for spec in chain_specs(content):
        hero = chain_hero(content, spec, level=40)
        assert hero.hybrid == {}
        assert kit(content.classes, content.balance, hero)["abilities"] == content.classes[spec]["abilities"]


# ---------------------------------------------------------------- every class


def test_every_class_has_a_same_slot_partner_in_the_three_slots(content):
    specs = chain_specs(content)
    assert len(specs) == 12 and {"paladin_sanador", "paladin_dps"} <= set(specs)
    for spec in specs:
        hero = chain_hero(content, spec)
        partner = hybrid_partner(content.classes, hero)
        group = content.classes[spec]["group"]
        assert partner in specs_of(content.classes, group) and partner != spec, spec
        pairs = hybrid_pairs(content.classes, hero)
        assert [p[0] for p in pairs] == list(HYBRID_LINKS), spec
        for link, own, other in pairs:
            assert own and other and own["link"] == other["link"] == link, (spec, link)
            assert other in content.classes[partner]["abilities"], (spec, link)
        for link in HYBRID_LINKS:
            assert toggle_hybrid(content.classes, content.balance, hero, link), (spec, link)
        assert [a["id"] for a in chain_bar(content.classes, content.balance, hero)] == \
            [a["id"] for a in content.classes[partner]["abilities"]], spec


def test_a_slot_without_partner_shows_a_dash_and_is_skipped(content):
    content = copy.deepcopy(content)
    dps = content.classes["guerrero_dps"]
    dps["abilities"] = [a for a in dps["abilities"] if a["link"] != "H2"]   # in memory only: a class missing its H2
    service = GameService(content, MemoryStore(), FixedClock(), world_seed=12345, time_scale=1.0)
    hero = hero_at(service, 10)
    assert not toggle_hybrid(content.classes, content.balance, hero, "H2")
    view = service.act("test:1", "hyb")
    assert "hyb:H2" not in ids(view) and "🔹 Preparador: Interponerse · —" in body(view)
    hero.hybrid = {"guerrero_tanque>guerrero_dps": ["H2", "H3"]}           # a saved choice that no longer fits is ignored
    assert hybrid_choice(content.classes, content.balance, hero) == ["H3"]


def test_english_texts_exist(content):
    service = GameService(content, MemoryStore(), FixedClock(), world_seed=12345, time_scale=1.0)
    hero_at(service, 10)
    service.act("test:1", "lang:en")
    view = service.act("test:1", "hyb")
    assert view.title == "🔀 Hybrid mode" and "Use" in view.actions[0].label
    view = service.act("test:1", "hyb:H1")
    assert "you now use" in view.notice
    assert not service.texts.missing


@pytest.mark.parametrize("action", ["hyb", "hyb:H1", "hyb:H9", "hyb:"])
def test_odd_buttons_do_not_break(service, action):
    hero_at(service, 10)
    view = service.act("test:1", action)
    assert view.kind in ("hybrid", "talents") and len(view.actions) <= 4
