"""High-level bestiary (D-108): every danger biome has enemies for every level 1-100, picks follow the zone level,
fights stay winnable and the XP pace to level 100 stays on the D-108 track.

[ES] Pruebas del bestiario por niveles (D-108, confirmada): cada bioma con peligro tiene enemigos propios en cada
nivel del 1 al 100 (al menos 2 sin contar al bandido desde el nivel 2), los rangos y textos son válidos, el
enemigo que sale respeta el nivel de la zona y cambia según la semilla, las zonas más allá de la última franja
traen a los de la franja más alta, una pelea de cada franja se gana con juego atento y el ritmo de experiencia
hasta el nivel 100 sigue cerca de 1,8 años (progresion.md §1.2). Si cambias content/enemies.yaml, corre esto.
"""

import sys
from pathlib import Path

import pytest

from conftest import make_hero
from engine.combat import make_combat, resolve_round
from engine.core import Rng, Texts
from engine.hero import Hero, hero_stats, xp_for_level
from engine.world import raids as raid_rules
from engine.world.encounters import clamp_level, encounter_pool
from engine.world.mapgen import Zone

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import sim  # noqa: E402  (tools/sim.py: the same combat helpers the balance log uses)

KNOWN_TAGS = {"blockable", "dodgeable", "interruptible"}


def danger_biomes(content):
    return [b for b, d in content.biomes.items() if d.get("danger", 0) > 0]


def own(content, biome, level):
    """Non-boss enemies of the biome that hold this level, without the bandit (it is everywhere)."""
    return [eid for eid, e in content.enemies.items() if biome in e.get("biomes", []) and not e.get("boss")
            and eid != "bandido_errante" and e["level_min"] <= level <= e["level_max"]]


def test_every_danger_biome_has_enemies_at_every_level(content):
    for biome in danger_biomes(content):
        for level in range(1, 101):
            assert any(e["level_min"] <= level <= e["level_max"] for _, e in encounter_pool(content.enemies, biome, level)), (biome, level)
            assert len(own(content, biome, level)) >= (1 if level == 1 else 2), (biome, level)   # variety, not one enemy over and over


def test_enemy_ranges_texts_and_numbers_are_valid(content):
    t = Texts(content.texts)
    for eid, e in content.enemies.items():
        assert isinstance(e["level_min"], int) and isinstance(e["level_max"], int), eid
        assert 1 <= e["level_min"] <= e["level_max"] <= 100, eid
        assert t.has(e["name_key"]) and e["name_key"] == f"enemy.{eid}.name", eid
        assert e["xp"] > 0 and e["base"]["hp"] > 0 and e["base"]["attack"] > 0, eid
        low, high = e.get("gold", [1, 3])
        assert 0 <= low <= high, eid
        assert set(e.get("biomes", [])) <= set(content.biomes), eid
        for item_id, chance in e.get("loot", {}).items():
            assert item_id in content.items and 0 < chance <= 1, (eid, item_id)
        moves = list(e["moves"]) + [m for p in e.get("phases") or [] for m in p.get("moves") or []]
        assert 2 <= len(e["moves"]) <= 4, eid
        for move in moves:
            assert set(move.get("tags", [])) <= KNOWN_TAGS and move.get("weight", 1) > 0, (eid, move["id"])
            assert move.get("kind", "hit") in ("hit", "channel"), (eid, move["id"])
            assert t.has(f"enemy.{eid}.moves.{move['id']}.name"), (eid, move["id"])
            warn = t.t(f"enemy.{eid}.moves.{move['id']}.warn")
            basic = move.get("kind", "hit") == "hit" and set(move.get("tags", [])) == {"blockable", "dodgeable"} \
                and move.get("power", 1.0) <= 1.5
            assert basic or "(" in warn, (eid, move["id"])    # every big or special move says how to answer it
    assert not t.missing


def test_picks_follow_the_zone_level_and_vary(service):
    make_hero(service)
    hero = service._load("test:1")
    for level in (20, 50, 90):
        for biome in danger_biomes(service.content):
            zone = Zone(x=level, y=0, biome=biome, lejania=level, ring=10, level=level, name_index=(0, 0))
            seen = set()
            for seed in range(40):
                service._start_combat(hero, zone, Rng(seed), "encounter.found")
                state = service.store.get("combat", "test:1")
                edef = service.content.enemies[state["enemy"]["id"]]
                assert biome in edef["biomes"] and not edef.get("boss")
                assert edef["level_min"] <= level <= edef["level_max"], (biome, level, state["enemy"]["id"])
                assert state["enemy"]["level"] in (level, level + 1) and state["enemy"]["level"] <= edef["level_max"]
                seen.add(state["enemy"]["id"])
            assert len(seen) >= 3, (biome, level, seen)     # the bandit and at least 2 of the biome's own


def test_zones_past_the_last_band_bring_the_highest_enemies(content):
    top = max(e["level_max"] for e in content.enemies.values() if not e.get("boss"))
    for biome in danger_biomes(content):
        pool = encounter_pool(content.enemies, biome, 150)
        assert pool and all(e["level_max"] == top for _, e in pool), biome      # never a level 6 wolf far away
        assert all(clamp_level(e, 151) == top for _, e in pool)
    assert encounter_pool(content.enemies, "claro", 5)                           # a biome without enemies still gets someone near its level
    assert all(e["level_min"] <= 5 <= e["level_max"] for _, e in encounter_pool(content.enemies, "claro", 5))
    # The raids use the same rule: the weekly raid and the Noche de prueba of a level 60 tundra camp.
    pool_ids = {eid for eid, _ in encounter_pool(content.enemies, "tundra", 60)}
    assert raid_rules.pick_enemy(content.enemies, "tundra", 60, roll=0.5)[0] in pool_ids
    strongest, level = raid_rules.pick_enemy(content.enemies, "tundra", 60, strongest=True)
    assert strongest in pool_ids and level == 60


def _fight(cdef, enemy_id, level, seed):
    stats = hero_stats(cdef, level)
    hero = Hero(id="t", name="T", class_id="x", level=level, hp=stats["max_hp"], belt={"pocion_vida": 3, "venda": 2})
    state = make_combat(enemy_id, sim.C.enemies[enemy_id], level, cdef, seed)
    for _ in range(120):
        if state["outcome"]:
            break
        resolve_round(state, hero, cdef, sim.choose(state, hero, cdef, stats["max_hp"], enemy_id, stats, attentive=True), sim.CTX)
    return state["outcome"] == "victory", hero.hp / stats["max_hp"]


@pytest.mark.parametrize("level,biome", [(20, "colinas"), (50, "pantano"), (90, "tundra")])
def test_a_fight_of_each_band_is_winnable_but_not_free(level, biome):
    """A hero of the zone's level (all points in one spec, poco común gear, attentive play, full belt) wins most fights
    against the toughest and the weakest enemy of the band, and still loses some life (balance.md §7, D-108)."""
    pool = encounter_pool(sim.C.enemies, biome, level)
    hardest = max(pool, key=lambda pair: raid_rules.power(pair[1], level))[0]
    softest = min(pool, key=lambda pair: raid_rules.power(pair[1], level))[0]
    for spec in ("guerrero", "mago_fuego", "druida_restauracion", "bardo_estratega"):
        cdef = sim.level_gear(sim.spec_hero(spec, level), level, 2)
        for enemy_id in {hardest, softest}:
            results = [_fight(cdef, enemy_id, level, seed) for seed in range(8)]
            wins = sum(r[0] for r in results)
            life_left = sum(r[1] for r in results) / len(results)
            assert wins >= 6, (spec, enemy_id, level, wins)
            assert life_left < 0.9, (spec, enemy_id, level, life_left)        # not trivial


def test_xp_pace_to_level_100_follows_d108(content):
    """With one won fight every 2 energy (20 a day, D-108) in zones of the hero's level, level 100 takes ~1.8 years."""
    hb = content.balance["hero"]
    scale = hb["xp_level_scale"]
    biomes = danger_biomes(content)

    def xp_per_fight(level):
        total = 0.0
        for biome in biomes:
            pool = encounter_pool(content.enemies, biome, level)
            total += sum(e["xp"] * (1 + scale * (clamp_level(e, level) - 1)) for _, e in pool) / len(pool)
        return total / len(biomes)

    days = sum((xp_for_level(hb["xp_formula"], lv + 1) - xp_for_level(hb["xp_formula"], lv)) / (20 * xp_per_fight(lv))
               for lv in range(1, hb["max_level"]))
    assert 1.7 <= days / 365 <= 2.1, days / 365


def test_every_enemy_renders_without_missing_texts(service):
    make_hero(service)
    hero = service._load("test:1")
    kit = service._kit(hero)
    for eid, edef in service.content.enemies.items():
        for move in edef["moves"]:
            state = make_combat(eid, edef, edef["level_max"], kit, 1)
            state["enemy"]["next_move"] = move["id"]
            view = service._combat_view(hero, state)
            assert view.kind == "combat" and len(view.actions) <= 6
    zone = Zone(x=95, y=0, biome="ruinas", lejania=95, ring=10, level=95, name_index=(0, 0))
    service._start_combat(hero, zone, Rng(3), "encounter.found")
    for _ in range(3):
        view = service.act("test:1", "atk")
    assert not service.texts.missing, service.texts.missing
