"""Combat round rules (D-46). [ES] Pruebas de la ronda de combate de 6 botones."""

import copy

from engine.combat import CombatContext, make_combat, resolve_round, validate_choice
from engine.core import Texts
from engine.hero import Hero, hero_stats


def setup(content, class_id="guerrero", enemy_id="lobo_ceniciento", seed=7):
    ctx = CombatContext(content.classes, content.enemies, content.items, content.balance, Texts(content.texts))
    cdef = content.classes[class_id]
    hero = Hero(id="t", name="T", class_id=class_id, hp=hero_stats(cdef, 1)["max_hp"], belt={"pocion_vida": 2, "venda": 1})
    state = make_combat(enemy_id, content.enemies[enemy_id], 1, cdef, seed)
    return ctx, cdef, hero, state


def test_same_seed_same_fight(content):
    ctx, cdef, hero, state = setup(content)
    hero2, state2 = copy.deepcopy(hero), copy.deepcopy(state)
    for _ in range(4):
        if state["outcome"]:
            break
        resolve_round(state, hero, cdef, {"type": "attack"}, ctx)
        resolve_round(state2, hero2, cdef, {"type": "attack"}, ctx)
    assert state == state2 and hero.hp == hero2.hp


def test_block_reduces_damage(content):
    ctx, cdef, hero, state = setup(content)
    state["enemy"]["next_move"] = "mordisco"
    blocked_hero, blocked_state = copy.deepcopy(hero), copy.deepcopy(state)
    resolve_round(state, hero, cdef, {"type": "attack"}, ctx)
    resolve_round(blocked_state, blocked_hero, cdef, {"type": "ability", "index": 1}, ctx)
    assert blocked_hero.hp > hero.hp
    assert blocked_state["hero"]["stamina"] == content.balance["combat"]["stamina_max"] - 1


def test_dodge_avoids_dodgeable(content):
    ctx, cdef, hero, state = setup(content, class_id="picaro")
    state["enemy"]["next_move"] = "salto"
    hp = hero.hp
    resolve_round(state, hero, cdef, {"type": "ability", "index": 1}, ctx)
    assert hero.hp == hp


def test_interrupt_cancels_channel_when_faster(content):
    ctx, cdef, hero, state = setup(content, class_id="picaro")
    state["enemy"]["next_move"] = "aullido"
    state["enemy"]["initiative"] = 0
    resolve_round(state, hero, cdef, {"type": "ability", "index": 2}, ctx)
    assert state["enemy"]["buff"] == 1.0


def test_cost_and_cooldown_validation(content):
    ctx, cdef, hero, state = setup(content)
    assert validate_choice(state, hero, cdef, {"type": "ability", "index": 0}, ctx) is not None  # no rage yet
    state["hero"]["resource"] = 100
    assert validate_choice(state, hero, cdef, {"type": "ability", "index": 0}, ctx) is None


def test_potion_uses_round_and_respects_toxicity(content):
    ctx, cdef, hero, state = setup(content)
    hero.hp = 10
    resolve_round(state, hero, cdef, {"type": "item", "item_id": "pocion_vida"}, ctx)
    assert hero.belt["pocion_vida"] == 1
    state["hero"]["toxicity"] = 90
    assert validate_choice(state, hero, cdef, {"type": "item", "item_id": "pocion_vida"}, ctx) is not None


def test_fight_reaches_an_outcome(content):
    ctx, cdef, hero, state = setup(content, seed=3)
    for _ in range(60):
        if state["outcome"]:
            break
        choice = {"type": "ability", "index": 0} if state["hero"]["resource"] >= 30 else {"type": "attack"}
        resolve_round(state, hero, cdef, choice, ctx)
    assert state["outcome"] in ("victory", "defeat")
