"""Class and role balance pass (D-110) and crafted-over-loot gear (D-113): fast checks, not the full report.

[ES] Pruebas rápidas de la pasada de balance de clases y roles (D-110, confirmada) y del equipo de artesano por encima
del botín (D-113, provisional): cada tanque tiene más armadura base que el ataque de su clase; hay equipo en cada ranura
y tipo hasta el nivel 100, con niveles de pieza que suben; en cada nivel el mejor equipo de artesano supera al mejor
botín; el botín vuelve a soltar equipo cerca del nivel del enemigo en las franjas altas (y suelta menos desde el 10);
los puntos de Defensa dan armadura y la barra automática del tanque guarda su curación; y una muestra chica de peleas
con semilla fija comprueba el orden de los roles (la defensa termina con más vida que el ataque, el ataque mata en menos
rondas, la curación es la que más vida deja) y que nadie baje del piso de victorias. El informe completo es
tools/balance_report.py (registro en diseno/03-personaje/balance.md §7). Si mueves classes.yaml, items.yaml,
enemies.yaml o balance.yaml (gear, talents), corre esto.
"""

import statistics
import sys
from pathlib import Path

import pytest

from engine.classes import kit
from engine.core import Rng
from engine.hero import Hero, hero_stats
from engine.hero.gear import drop_chance_for, roll_gear

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import balance_report as report  # noqa: E402  (the D-110 report: the same kits and fights, in small)
import sim  # noqa: E402

CRAFTED_SLOTS = ("arma", "armadura", "joya")


def active(content):
    return [cid for cid, c in content.classes.items() if not c.get("retired")]


def lootable(content):
    return {iid: it for iid, it in content.items.items() if it.get("kind") == "gear" and not it.get("source") and not it.get("retired")}


def crafted(content):
    return {iid: it for iid, it in content.items.items() if it.get("kind") == "gear" and it.get("source") == "crafted"}


def test_every_tank_has_more_base_armor_than_its_attack_sibling(content):
    groups = {}
    for cid in active(content):
        groups.setdefault(content.classes[cid]["group"], []).append(cid)
    checked = 0
    for group, specs in groups.items():
        tanks = [s for s in specs if content.classes[s]["role"] == "defensa"]
        attackers = [s for s in specs if content.classes[s]["role"] == "ataque"]
        for tank in tanks:
            for attacker in attackers:
                assert content.classes[tank]["base"]["armor"] > content.classes[attacker]["base"]["armor"], (tank, attacker)
                checked += 1
    assert checked == 2                                     # 0.31: the 2 classes with a tank role (Guerrero and Druida)


def test_gear_goes_up_to_level_100_in_every_slot_and_type(content):
    cfg = content.balance["gear"]
    types = {"arma": {w for ws in cfg["weapons_by_group"].values() for w in ws}, "joya": {"joya"}}
    for slot in cfg["slots"]:
        if slot not in types:
            types[slot] = set(cfg["armor_by_group"].values())
    gear = lootable(content)
    for slot, kinds in types.items():
        for typ in kinds:
            pieces = sorted((it["req_level"], it["tier"], sum(it["stats"].values())) for it in gear.values()
                            if it["slot"] == slot and it["type"] == typ)
            assert pieces[0][0] == 1 and pieces[-1][0] == 100, (slot, typ)
            for (lv_a, tier_a, sum_a), (lv_b, tier_b, sum_b) in zip(pieces, pieces[1:]):
                assert lv_b > lv_a and tier_b == tier_a + 1 and sum_b > sum_a, (slot, typ, lv_b)   # it keeps improving
            assert max(b[0] - a[0] for a, b in zip(pieces, pieces[1:])) <= 10, (slot, typ)       # a tier every 10 levels or less


def test_best_crafted_beats_best_loot_at_every_level(content):
    """D-113: from level 3 (the first recipe) the best piece of each crafted slot is a crafted one, and loot from level 10
    on is at most raro (crafted: épico)."""
    cfg = content.balance["gear"]
    loot, made = lootable(content), crafted(content)
    types = {"arma": {w for ws in cfg["weapons_by_group"].values() for w in ws}, "armadura": set(cfg["armor_by_group"].values()),
             "joya": {"joya"}}

    def best(pool, slot, typ, level):
        fits = [it for it in pool.values() if it["slot"] == slot and it["type"] == typ and it["req_level"] <= level]
        return max(fits, key=lambda it: (it["req_level"], sum(it["stats"].values()))) if fits else None

    for slot in CRAFTED_SLOTS:
        for typ in types[slot]:
            for level in range(3, 101):
                b_loot, b_made = best(loot, slot, typ, level), best(made, slot, typ, level)
                assert b_made and b_made["req_level"] >= b_loot["req_level"], (slot, typ, level)
                assert all(b_made["stats"].get(k, 0) >= v for k, v in b_loot["stats"].items()), (slot, typ, level)
                assert sum(b_made["stats"].values()) > sum(b_loot["stats"].values()), (slot, typ, level)
    order = list(cfg["rarity_icon"])
    for it in loot.values():
        if it["req_level"] >= 10:
            assert order.index(it["rarity"]) <= order.index("raro"), it["name_key"]
    assert all(it["rarity"] == "epico" for it in made.values() if it["req_level"] >= 10)


def test_crafted_gear_has_a_recipe_from_two_branches_and_sells_for_less_than_its_materials(content):
    recipes = content.professions["recipes"]
    ratio = content.balance["shop"]["sell_ratio"]
    made = crafted(content)
    by_output = {out: rdef for rdef in recipes.values() for out in rdef["output"]}
    for iid, it in made.items():
        rdef = by_output[iid]                                            # every crafted piece has its recipe
        materials = sum(content.items[m]["price"] * n for m, n in rdef["inputs"].items())
        assert it["price"] * ratio < materials, iid                     # crafting never makes coins at the merchant
        if it["req_level"] >= 10:
            assert rdef["min_rank"] == 50 + it["req_level"] // 2, iid   # level 10 → rank 55 ... level 100 → rank 100
            assert rdef["energy"] == 2 and rdef["xp"] == 12, iid        # same pace as the other pieces (D-108)


@pytest.mark.parametrize("enemy_level", [12, 15, 25, 47, 63, 88, 99])
def test_loot_drops_gear_near_high_enemy_levels(content, enemy_level):
    hero = Hero(id="x", name="X", class_id="guerrero", level=enemy_level)
    made = crafted(content)
    seen = set()
    for seed in range(60):
        dropped = roll_gear(content.items, content.classes, content.balance, hero, enemy_level, Rng(seed), chance=1.0)
        assert dropped and dropped not in made
        req = content.items[dropped]["req_level"]
        assert enemy_level - 10 < req <= enemy_level + 1, (enemy_level, dropped)     # near the enemy, never far below
        seen.add(dropped)
    assert len(seen) >= 5                                                          # many slots and types, not one piece
    assert drop_chance_for(content.balance, enemy_level) < content.balance["gear"]["drop_chance"]   # D-113: less loot
    assert drop_chance_for(content.balance, 5) == content.balance["gear"]["drop_chance"]


def test_defense_points_add_armor_and_the_tank_bar_keeps_a_heal(content):
    tank = sim.spec_hero("guerrero_tanque", 50)                                     # 0.31: the chain tank
    cdef = kit(content.classes, content.balance, tank)
    per_point = content.balance["talents"]["passive"]["defensa"]["armor"]
    assert cdef["talent_bonus"]["armor"] == pytest.approx(per_point * 49)
    assert hero_stats(cdef, 50)["armor"] == pytest.approx(content.classes["guerrero_tanque"]["base"]["armor"] + per_point * 49)
    attacker = kit(content.classes, content.balance, sim.spec_hero("guerrero_dps", 50))
    assert not attacker["talent_bonus"].get("armor")                               # only Defensa gets armor
    cdef["gear_bonus"] = {"armor": 0.9}
    assert hero_stats(cdef, 50)["armor"] == content.balance["gear"]["armor_cap"]   # never above the cap
    for spec in [s for s in active(content) if content.classes[s]["role"] == "defensa"]:
        bar = kit(content.classes, content.balance, sim.spec_hero(spec, 30))["abilities"]
        assert [a["link"] for a in bar] == ["H1", "H2", "H3"], spec                 # 0.31: the chain bar is fixed
        assert any(a["kind"] == "guard" for a in bar), spec                        # the tank's endurance or dodge


SAMPLE = {"ataque": ("guerrero_dps", "druida_dps", "mago_dps"),                   # 0.31: the chain classes
          "defensa": ("guerrero_tanque", "druida_tanque"),
          "curacion": ("sacerdote_sanador", "paladin_sanador"),                     # 0.32: the Paladín took the Chamán's place
          "soporte": ("cazador_soporte", "mago_soporte")}


@pytest.mark.parametrize("level", [50, 75])
def test_role_ordering_in_a_small_seeded_sample(level):
    """Level loot gear, attentive play, full belt, 6 enemies of the level × 3 seeds: the tank ends with more life than
    the attacker (and kills slower), the healer ends with the most life, and nobody falls below the win floor."""
    enemies = report.pool_at(level)[:6]
    results = {}
    for role, specs in SAMPLE.items():
        rows = []
        for spec in specs:
            cdef = report.kit_for(spec, level, "b")
            fights = [report.fight(cdef, eid, level, level, seed * 7919 + level) for eid in enemies for seed in range(3)]
            wins = sum(f[0] for f in fights) / len(fights)
            assert wins >= 0.85, (spec, level, wins)                                   # every spec stays playable
            rows.append((statistics.mean(f[1] for f in fights), statistics.mean(f[2] for f in fights)))
        results[role] = (statistics.mean(r[0] for r in rows), statistics.mean(r[1] for r in rows))
    life = {role: v[0] for role, v in results.items()}
    rounds = {role: v[1] for role, v in results.items()}
    assert life["defensa"] >= life["ataque"] + 0.05, results                         # the tank holds out (D-110)
    assert rounds["ataque"] < rounds["soporte"] < rounds["curacion"], results       # attack kills fastest, healing slowest
    assert rounds["ataque"] < rounds["defensa"], results
    assert life["curacion"] >= max(life["ataque"], life["soporte"]), results         # healing sustains
    assert life["ataque"] <= 0.75, results                                          # normal fights are not free anymore
