"""Chain combat rules (0.31, D-225 to D-229): energy, the role orders, marks, the spender, variety and the 12 combos of the patch.

[ES] Pruebas de la cadena del parche de clases: la energía (arranca con 5, +2 por turno antes de pagar, el Básico da +1, sin
tope), los costos (0, 2, 3 y 6), el orden de cada rol, las marcas (los básicos seguidos cuentan como una, romper el orden
las pierde, tejer después de cumplir el orden no corta), el premio del gastador (+10 %, +25 %, +50 %), el gastador sin combo
(85 %), la variedad, el tope de 5 objetivos y que defenderse o tomar una poción cuesta 1 de energía y gasta el turno. Los 12
combos del §4 del parche, verificados turno a turno: la energía con la que termina cada uno y sus marcas.
Archivo: tests/test_cadena.py · Módulo: M5 Combate · Prueba: engine/combat/chain.py y engine/combat/chain_round.py.
"""

import pytest

from conftest import make_hero
from engine.combat import chain
from engine.core import Rng, load_content


@pytest.fixture(scope="module")
def bal():
    return load_content().balance


def play(links, role, bal):
    """Play a sequence of buttons with the chain rules; returns (energy after the last button, marks cashed, cash)."""
    c = chain.cfg(bal)
    req = [link for link in c["orders"][role] if link != "H3"]
    state = chain.new_chain()
    energy = c["energy"]["start"]
    cash = None
    for link in links:
        energy += c["energy"]["per_turn"]
        cost = chain.cost_of(link, bal)
        assert cost <= energy, (links, link, energy)            # every combo of the patch can be paid turn by turn
        energy -= cost
        if link == "B":
            energy += c["energy"]["basic_gain"]
        if link == "H3":
            cash = chain.spend(state, req, bal)
        else:
            chain.press(state, link, req)
    return energy, (cash or {}).get("marks", 0), cash


# §4 of the patch: three combos per role, starting with 5 energy and +2 per turn: (buttons, marks, energy at the end)
COMBOS = {
    "tanque": [("B H2 H1 H3", 4, 3), ("B H2 H1 B H1 H3", 6, 6), ("B B B H2 H1 H3", 4, 9)],
    "sanador": [("B H1 H2 H3", 4, 3), ("B H1 B H2 H1 H3", 6, 6), ("B B B H1 H2 H3", 4, 9)],
    "dps": [("H1 H2 H3", 3, 0), ("H1 B H2 B H1 H3", 6, 6), ("B B H1 H2 H3", 4, 6)],
    "soporte": [("H2 H1 H3", 3, 0), ("H2 B H1 B H1 H3", 6, 6), ("B B H2 H1 H3", 4, 6)],
}


@pytest.mark.parametrize("role,combo,marks,energy", [(r, *c) for r, cs in COMBOS.items() for c in cs])
def test_the_twelve_combos_of_the_patch(role, combo, marks, energy, bal):
    end, cashed, cash = play(combo.split(), role, bal)
    assert end == energy and cashed == marks and cash["valid"]


def test_the_costs_energy_and_orders_are_the_patch(bal):
    c = chain.cfg(bal)
    assert c["costs"] == {"B": 0, "H1": 2, "H2": 3, "H3": 6}
    assert c["energy"]["start"] == 5 and c["energy"]["per_turn"] == 2 and c["energy"]["basic_gain"] == 1
    assert c["energy"]["defend_cost"] == 1 and c["energy"]["item_cost"] == 1
    assert c["orders"] == {"tanque": ["B", "H2", "H1", "H3"], "sanador": ["B", "H1", "H2", "H3"],
                           "dps": ["H1", "H2", "H3"], "soporte": ["H2", "H1", "H3"]}
    assert c["target_cap"] == 5


def test_marks_pay_10_25_and_50_percent(bal):
    assert [chain.mark_bonus(n, bal) for n in range(0, 8)] == [0, 0, 0.10, 0.25, 0.25, 0.50, 0.50, 0.50]


def test_basics_in_a_row_count_as_one_mark_and_never_make_a_combo(bal):
    end, marks, cash = play("B B B H3".split(), "dps", bal)
    assert not cash["valid"] and cash["mult"] == pytest.approx(0.85) and cash["bonus"] == 0      # no easy prize
    state = chain.new_chain()
    for _ in range(4):
        chain.press(state, "B", ["B", "H2", "H1"])
    assert state["marks"] == 1


def test_a_button_out_of_order_cuts_the_chain(bal):
    req = ["B", "H2", "H1"]                                     # the tank
    state = chain.new_chain()
    chain.press(state, "B", req)
    chain.press(state, "H2", req)
    assert state["marks"] == 2
    result = chain.press(state, "B", req)                       # the Básico never cuts
    assert result["lost"] == 0 and state["marks"] == 3
    state = chain.new_chain()
    chain.press(state, "B", req)
    result = chain.press(state, "H1", req)                      # H1 before H2: out of order
    assert result["lost"] == 1 and state["marks"] == 0 and state["step"] == 0


def test_weaving_after_the_order_is_done_does_not_cut(bal):
    req = ["H1", "H2"]
    state = chain.new_chain()
    for link in ("H1", "H2", "H1", "H2", "H1"):
        assert chain.press(state, link, req)["lost"] == 0
    assert state["marks"] == 5
    cash = chain.spend(state, req, bal)
    assert cash["valid"] and cash["marks"] == 6 and cash["bonus"] == 0.50 and state["marks"] == 0


def test_a_spender_without_h1_or_h2_hits_at_85_percent(bal):
    for combo in ("H3", "B H3", "H1 H3", "B H1 H3"):            # dps: the order is H1, H2
        _, _, cash = play(combo.split(), "dps", bal)
        assert not cash["valid"] and cash["mult"] == pytest.approx(0.85) and cash["marks"] == 0


def test_variety_grows_with_different_combos(bal):
    assert chain.variety_bonus([], bal) == 0
    assert chain.variety_bonus(["H1-H2-H3", "H1-H2-H3"], bal) == 0
    assert chain.variety_bonus(["H1-H2-H3", "B-H1-H2-H3"], bal) == pytest.approx(0.02)
    assert chain.variety_bonus(["H1-H2-H3", "B-H1-H2-H3", "H1-B-H2-H3"], bal) == pytest.approx(0.03)
    assert chain.cfg(bal)["variety"]["scope"] in ("fight", "permanent")


def test_no_area_ability_touches_more_than_five(bal):
    classes = load_content().classes
    for cdef in classes.values():
        if cdef.get("system") != "chain":
            continue
        for ability in [cdef["attack"]] + cdef["abilities"]:
            assert int(ability.get("targets", 1)) <= chain.target_cap(bal)
            assert int(ability.get("split", 1)) <= chain.target_cap(bal)


def fight(service, spec):
    """A hero of that spec in a fight against a wolf (energy as the patch: 5 to start)."""
    hero = make_hero(service)
    hero = service._load("test:1")
    hero.class_id = spec
    service._save(hero)
    hero = service._load("test:1")
    service._start_combat(hero, service._zone(1, 0), Rng(3), "encounter.ambush")
    service._save(hero)
    return service._load("test:1")


def test_defending_and_potions_cost_one_energy_and_the_turn(service):
    hero = fight(service, "guerrero_dps")
    state = service.store.get("combat", "test:1")
    state["enemy"]["hp"] = state["enemy"]["max_hp"] = 10_000                 # it must last a few rounds
    service.store.put("combat", "test:1", state)
    service.act("test:1", "dodge")
    state = service.store.get("combat", "test:1")
    assert state["hero"]["resource"] == 5 + 2 - 1                            # +2 for the turn, -1 for defending
    assert any("Te defiendes" in line for line in state["log"])
    hero = service._load("test:1")
    hero.belt["pocion_vida"] = 1
    hero.hp = 5
    service._save(hero)
    service.act("test:1", "use:pocion_vida")
    state = service.store.get("combat", "test:1")
    assert state["hero"]["resource"] == 6 + 2 - 1
    assert not service.texts.missing


def test_there_is_no_energy_cap(service):
    hero = fight(service, "guerrero_tanque")
    state = service.store.get("combat", "test:1")
    state["enemy"]["hp"] = state["enemy"]["max_hp"] = 100_000
    state["enemy"]["attack"] = 0.0
    service.store.put("combat", "test:1", state)
    for _ in range(40):
        hero = service._load("test:1")
        hero.hp = 999
        service._save(hero)
        service.act("test:1", "atk")
    state = service.store.get("combat", "test:1")
    assert state["hero"]["resource"] >= 5 + 40 * 3 - 5                     # +3 a turn with the Básico, never capped


def test_a_spender_needs_its_energy_this_turn(service):
    hero = fight(service, "mago_dps")
    state = service.store.get("combat", "test:1")
    state["hero"]["resource"] = 3                                          # 3 + 2 = 5 < 6
    service.store.put("combat", "test:1", state)
    view = service.act("test:1", "ab:2")
    assert view.kind == "combat" and "energía" in (view.notice or "")
    state = service.store.get("combat", "test:1")
    assert state["hero"]["resource"] == 3 and state["round"] == 1          # nothing was spent
    state["hero"]["resource"] = 4                                          # 4 + 2 = 6: enough
    service.store.put("combat", "test:1", state)
    service.act("test:1", "ab:2")
    assert service.store.get("combat", "test:1") is None or service.store.get("combat", "test:1")["round"] == 2


def test_every_preparer_leaves_something_for_the_next_turn():
    classes = load_content().classes
    lasting = ("dot", "guard", "shield", "empower", "expose", "weaken", "debuff")
    for spec, cdef in classes.items():
        if cdef.get("system") != "chain":
            continue
        h2 = next(a for a in cdef["abilities"] if a["link"] == "H2")
        assert h2["kind"] in lasting or h2.get("charge") or h2.get("next_bonus") or h2.get("heal_boost"), spec
        if h2["kind"] in lasting and h2["kind"] != "dot":
            assert int(h2.get("rounds", 1)) >= 2, spec                       # still there next turn
