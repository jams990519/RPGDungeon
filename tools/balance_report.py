"""Class and role balance report (D-110): every spec at several levels, with and without points, loot gear,
crafted gear and profession perks; plus the Guardian and the Noche de prueba.

Usage (from the repository root):
    python3 tools/balance_report.py [--levels=1,10,25,50,75,100] [--scenarios=a,b,c,b3] [--seeds=6]
                                    [--only=spec1,spec2] [--roles] [--jobs=4]
        One line per spec and level: win %, health left % and rounds against every normal enemy that holds that
        level (content/enemies.yaml level_min..level_max), at that level, with attentive play and a full belt
        (3 potions, 2 bandages). Scenarios:
            a  = starter gear (tier-1 weapon and chest), no talent points (the bare class).
            b  = real kit: level - 1 points in the spec (automatic bar, passives) and, in every slot, the best
                 lootable piece of its type for its level (no crafted, no Guardian pieces).
            c  = b + the best crafted piece where one exists for its level (D-113) + every profession perk that
                 applies to the hero at rank 100 (D-111: perk_bonus, heal_bonus, item_bonus).
            b3 = b against the enemies of level + 3 (harder fights; skipped at level 100).
            p1 = level - 1 points and the tier-1 piece of its type in every slot (the old bestiary check: who is weak
                 when the gear does not keep up). Not in the default list; ask for it with --scenarios=p1.
        --roles prints only the per-role summary table (median of the specs of each role).
    python3 tools/balance_report.py --boss [--seeds=100]
        The region Guardian (tools/sim.py --boss: level 6, gear up to tier 2). Target 45-90 % per spec.
    python3 tools/balance_report.py --trial [--seeds=20]
        The Noche de prueba (D-99): for every danger biome, the strongest enemy of the zone level + 2 with life × 2
        and attack × 1.3 (balance.yaml raids.trial), against heroes of the zone level with tier-1 gear in every slot
        and with poco común gear (tier 2), with and without the 11 defense points of the camp upgrades (D-101).
    python3 tools/balance_report.py --sources [--seeds=6]
        Does every upgrade add up? Per role, levels 10 and 50, what each source adds: no points / points,
        no gear / starter / loot / crafted, no perks / perks (the camp defense is in --trial).
    python3 tools/balance_report.py --pace [--seeds=4]
        D-108: years to level 100 with full energy, from the enemies' experience and corrected by the losses of b.
    Any mode accepts --content=<folder> to measure another copy of content/ (for example, the one before a change).

[ES]
Para qué sirve: medir de una vez si las clases cumplen su rol (D-110): el ataque mata más rápido, la defensa
termina con más vida, la curación se sostiene y el soporte queda en medio; y si cada mejora (niveles, talentos,
equipo de botín, equipo de artesano, beneficios de oficio y defensas del campamento) suma de verdad. Imprime las
tablas que van al registro de balance (diseno/03-personaje/balance.md §7, "pasada de balance de clases y roles").
Documento de diseño: diseno/03-personaje/balance.md §3 y §7 (D-110); diseno/03-personaje/equipamiento.md §11 (D-113)
Módulo: herramienta (no es parte del juego; no lo usa ningún cliente)
Depende de: tools/sim.py (C, CTX, choose, spec_hero, level_gear, boss_mode), engine.combat, engine.hero,
    engine.professions (perks), engine.world (encounters, raids), content/*
Lo usan: las personas e IAs que mueven números de balance (antes de cambiar classes.yaml, items.yaml,
    enemies.yaml o balance.yaml) y tests/test_balance_d110.py (una muestra chica)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno (no guarda nada)
Reglas que nunca se rompen:
    1. Usa las mismas funciones de combate que el juego (make_combat, resolve_round) y la forma de jugar atenta de
       tools/sim.py (choose con attentive=True): no tiene reglas propias.
    2. Es determinista: las mismas semillas dan los mismos números (también con --jobs).
Si cambias esto, revisa:
    - Que los escenarios sigan diciendo lo mismo que el registro de balance (a, b, c, b3 de arriba)
    - tests/test_balance_d110.py usa kit_for, fight y pool_at
"""

from __future__ import annotations

import statistics
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import sim  # noqa: E402  (the same helpers and play policy as the rest of the balance log)
from engine.classes import kit  # noqa: E402
from engine.combat import CombatContext, make_combat, resolve_round  # noqa: E402
from engine.core import Texts, load_content  # noqa: E402
from engine.hero import Hero, hero_stats  # noqa: E402
from engine.hero.gear import gear_bonus, starter_gear  # noqa: E402
from engine.professions.rules import perks  # noqa: E402
from engine.world import raids as raid_rules  # noqa: E402

C = sim.C
LEVELS = [1, 10, 25, 50, 75, 100]
SCENARIOS = ["a", "b", "c", "b3"]
FULL_BELT = {"pocion_vida": 3, "venda": 2}
ROLE_ORDER = ["ataque", "defensa", "curacion", "soporte"]


def pool_at(level: int) -> list[str]:
    """Normal enemies (not bosses, not retired) whose level range holds this level. [ES] Qué hace: los enemigos
    comunes que pueden salir a ese nivel en algún bioma. La llaman: el informe y las pruebas. Si cambia, afecta: solo
    contra qué se mide."""
    return [eid for eid, e in C.enemies.items() if not e.get("boss") and not e.get("retired")
            and e["level_min"] <= level <= e["level_max"]]


def _type_for(hero: Hero, slot: str) -> str:
    cfg = C.balance["gear"]
    group = C.classes[hero.class_id].get("group", hero.class_id)
    if slot == "arma":
        return cfg["weapons_by_group"][group][0]
    if slot == "joya":
        return "joya"
    return cfg["armor_by_group"][group]


def best_piece(hero: Hero, slot: str, level: int, crafted: bool) -> str | None:
    """The best piece of the hero's type for a slot at its level: lootable only, or lootable and crafted.
    Best = highest required level, then the bigger sum of stats (a crafted piece beats loot of its level).
    [ES] Qué hace: elige la mejor pieza de una ranura para el nivel (solo botín, o botín y artesano). La llaman:
    gear_for. Si cambia, afecta: solo el informe."""
    typ = _type_for(hero, slot)
    pieces = []
    for iid, it in C.items.items():
        if it.get("kind") != "gear" or it.get("retired") or it.get("slot") != slot or it.get("type") != typ:
            continue
        source = it.get("source")
        if source and not (crafted and source == "crafted"):
            continue
        if it.get("req_level", 1) <= level:
            pieces.append((it.get("req_level", 1), sum(it.get("stats", {}).values()), iid))
    return max(pieces)[2] if pieces else None


def gear_for(hero: Hero, level: int, crafted: bool) -> None:
    """Wear the best piece in every slot (see best_piece). [ES] Qué hace: viste al héroe de prueba. La llama: kit_for."""
    for slot in C.balance["gear"]["slots"]:
        piece = best_piece(hero, slot, level, crafted)
        if piece:
            hero.gear[slot] = piece


def max_perks(hero: Hero) -> dict[str, float]:
    """Every profession perk that applies to this hero, at rank 100 (D-111). [ES] Qué hace: los beneficios de todos
    los oficios al rango 100 que valen para este héroe (su armadura, su arma y su rol). La llama: kit_for."""
    catalog = (C.professions or {}).get("professions") or {}
    cdef = C.classes[hero.class_id]
    group = cdef.get("group", hero.class_id)
    cfg = C.balance["gear"]
    weapon = C.items.get(hero.gear.get("arma", ""), {})
    max_rank = C.balance["professions"]["max_rank"]
    return perks(catalog, {pid: max_rank for pid in catalog}, max_rank, cfg["armor_by_group"].get(group),
                 weapon.get("type"), cdef.get("role"))


def kit_for(spec: str, level: int, scenario: str) -> dict:
    """The combat kit of a test hero for a scenario (a, b, c, p1; b3 uses b). [ES] Qué hace: arma el kit del héroe de
    prueba para cada escenario del informe. La llaman: el informe y tests/test_balance_d110.py."""
    if scenario == "a":
        hero = sim.spec_hero(spec, level, points=0)
        starter_gear(C.items, C.classes, C.balance, hero)
    elif scenario == "p1":
        return sim.level_gear(sim.spec_hero(spec, level), level, 1)
    else:
        hero = sim.spec_hero(spec, level)
        gear_for(hero, level, crafted=scenario == "c")
    out = kit(C.classes, C.balance, hero)
    out["gear_bonus"] = gear_bonus(C.items, hero, C.classes, C.balance)
    out["armor_cap"] = C.balance["gear"]["armor_cap"]
    if scenario == "c":
        perk = max_perks(hero)
        out["perk_bonus"] = {k: perk[k] for k in ("attack", "hp", "armor")}
        out["heal_bonus"] = perk["heal"]
        out["item_bonus"] = {"potion": perk["potion"], "bandage": perk["bandage"]}
    return out


def fight(cdef: dict, enemy_id: str, hero_level: int, enemy_level: int, seed: int, belt: dict | None = None,
          hp_mult: float = 1.0, attack_mult: float = 1.0) -> tuple[bool, float, int]:
    """One fight with attentive play (tools/sim.py choose) and a full belt; returns (won, health left, rounds).
    hp_mult/attack_mult make the enemy an elite (the Noche de prueba). [ES] Qué hace: juega una pelea completa. La
    llaman: el informe y las pruebas. Si cambia, afecta: solo el informe."""
    stats = hero_stats(cdef, hero_level)
    hero = Hero(id="t", name="T", class_id="x", level=hero_level, hp=stats["max_hp"], belt=dict(belt or FULL_BELT))
    state = make_combat(enemy_id, C.enemies[enemy_id], enemy_level, cdef, seed)
    if hp_mult != 1.0 or attack_mult != 1.0:
        raid_rules.scale_enemy(state, hp_mult, attack_mult)
    for _ in range(120):
        if state["outcome"]:
            break
        resolve_round(state, hero, cdef, sim.choose(state, hero, cdef, stats["max_hp"], enemy_id, stats, attentive=True), sim.CTX)
    return state["outcome"] == "victory", hero.hp / stats["max_hp"], state["round"]


def measure(spec: str, level: int, scenario: str, seeds: int) -> tuple[float, float, float, str, float]:
    """Win %, health left %, rounds, worst enemy and its win % of a spec at a level in a scenario.
    Every enemy of the level gets `seeds` fights (at least 2). [ES] Qué hace: la medición de una celda del informe."""
    enemy_level = level + 3 if scenario == "b3" else level
    cdef = kit_for(spec, level, "b" if scenario == "b3" else scenario)
    wins, hps, rounds = [], [], []
    worst = (101.0, "")
    for eid in pool_at(enemy_level):
        res = [fight(cdef, eid, level, enemy_level, s * 7919 + level) for s in range(max(2, seeds))]
        w = 100 * sum(r[0] for r in res) / len(res)
        wins.append(w)
        hps.append(100 * sum(r[1] for r in res) / len(res))
        rounds.append(sum(r[2] for r in res) / len(res))
        worst = min(worst, (w, eid))
    n = len(wins) or 1
    return sum(wins) / n, sum(hps) / n, sum(rounds) / n, worst[1], worst[0]


def _cell(args):
    return args, measure(*args)


def run_cells(cells: list[tuple], jobs: int) -> dict:
    if jobs > 1:
        with ProcessPoolExecutor(max_workers=jobs) as pool:
            return dict(pool.map(_cell, cells, chunksize=4))
    return dict(map(_cell, cells))


def report(only, levels, scenarios, seeds, roles_only, jobs) -> None:
    specs = sim.active_specs(only)
    cells = [(spec, lv, sc, seeds) for spec in specs for lv in levels for sc in scenarios if not (sc == "b3" and lv >= 100)]
    out = run_cells(cells, jobs)
    print(f"Niveles {levels}; escenarios {scenarios}; {seeds} peleas por enemigo; juego atento y cinturón lleno")
    for sc in scenarios:
        print(f"\n== Escenario {sc} ==")
        if not roles_only:
            print(f"{'spec':28s} {'rol':9s} " + " ".join(f"{'L' + str(lv):>16s}" for lv in levels))
            for spec in specs:
                row = []
                for lv in levels:
                    r = out.get((spec, lv, sc, seeds))
                    row.append(f"{r[0]:4.0f}/{r[1]:3.0f}/{r[2]:4.1f}" if r else f"{'—':>14s}")
                    row[-1] = f"{row[-1]:>16s}"
                print(f"{spec:28s} {C.classes[spec]['role']:9s} " + " ".join(row))
        print(f"{'rol (mediana)':28s} {'specs':9s} " + " ".join(f"{'L' + str(lv) + ' gana/vida/rondas':>24s}" for lv in levels))
        for role in ROLE_ORDER:
            members = [s for s in specs if C.classes[s]["role"] == role]
            if not members:
                continue
            row = []
            for lv in levels:
                rs = [out[(s, lv, sc, seeds)] for s in members if (s, lv, sc, seeds) in out]
                if not rs:
                    row.append(f"{'—':>24s}")
                    continue
                med = [statistics.median(r[i] for r in rs) for i in range(3)]
                low = min(r[0] for r in rs)
                row.append(f"{med[0]:4.0f} ({low:3.0f})/{med[1]:3.0f}/{med[2]:4.1f}".rjust(24))
            print(f"{role:28s} {len(members):<9d} " + " ".join(row))
        floor = min((out[c][0], c[0], c[1]) for c in out if c[2] == sc) if any(c[2] == sc for c in out) else None
        if floor:
            print(f"Peor especialización: {floor[1]} al nivel {floor[2]} gana el {floor[0]:.0f} %")


TRIAL_GEAR = (("inicial (1)", 1), ("poco común", 2), ("su nivel", "b"))


def _trial_cell(args):
    """One Noche de prueba cell: zone level, gear, defense points, biome -> win % of all specs."""
    zone_level, gear, defense, biome, seeds = args
    trial = C.balance["raids"]["trial"]
    raids = C.balance["raids"]
    weak = max(raids["defense_floor"], 1 - defense * raids["defense_weaken_per_point"])
    enemy_id, enemy_level = raid_rules.pick_enemy(C.enemies, biome, zone_level + trial["enemy_level_bonus"], strongest=True)
    wins = total = 0
    for spec in sim.active_specs(None):
        if gear == "b":
            cdef = kit_for(spec, zone_level, "b")
        else:
            cdef = sim.level_gear(sim.spec_hero(spec, zone_level), zone_level, gear)
        for s in range(seeds):
            won, _, _ = fight(cdef, enemy_id, zone_level, enemy_level, s * 104729 + zone_level,
                              hp_mult=trial["enemy_hp_mult"] * weak, attack_mult=trial["enemy_attack_mult"] * weak)
            wins += won
            total += 1
    return args, 100 * wins / total


def trial_mode(seeds: int, jobs: int) -> None:
    """The Noche de prueba per biome and zone level: tier-1, tier-2 and level loot gear in every slot, with 0, 4 and 11
    defense points of the camp upgrades (D-101)."""
    trial = C.balance["raids"]["trial"]
    biomes = [b for b, d in C.biomes.items() if d.get("danger", 0) > 0]
    zones, defenses = (5, 15, 30, 60, 90), (0, 4, 11)
    cells = [(z, g, d, b, seeds) for z in zones for _, g in TRIAL_GEAR for d in defenses for b in biomes]
    if jobs > 1:
        with ProcessPoolExecutor(max_workers=jobs) as pool:
            out = dict(pool.map(_trial_cell, cells, chunksize=2))
    else:
        out = dict(map(_trial_cell, cells))
    print(f"Noche de prueba: enemigo más fuerte del bioma, nivel de la zona + {trial['enemy_level_bonus']}, vida × "
          f"{trial['enemy_hp_mult']}, ataque × {trial['enemy_attack_mult']}; 45 especializaciones, {seeds} peleas cada una")
    print(f"{'zona':>5s} {'equipo':>12s} {'defensa':>8s} " + " ".join(f"{b[:8]:>8s}" for b in biomes) + "   media")
    for z in zones:
        for label, g in TRIAL_GEAR:
            for d in defenses:
                row = [out[(z, g, d, b, seeds)] for b in biomes]
                print(f"{z:5d} {label:>12s} {d:8d} " + " ".join(f"{v:8.0f}" for v in row) + f"   {sum(row) / len(row):5.0f}")


def sources_mode(seeds: int, jobs: int) -> None:
    """What each upgrade adds, per role, at levels 10 and 50 (D-110: everything must add up)."""
    variants = [
        ("sin puntos, sin equipo", 0, "none", False),
        ("sin puntos, equipo inicial", 0, "starter", False),
        ("con puntos, equipo inicial", None, "starter", False),
        ("con puntos, botín de su nivel", None, "loot", False),
        ("con puntos, artesano", None, "crafted", False),
        ("con puntos, artesano y oficios", None, "crafted", True),
    ]
    specs = sim.active_specs(None)
    for level in (10, 50):
        print(f"\nNivel {level}: gana / vida / rondas (mediana del rol), {seeds} peleas por enemigo")
        print(f"{'variante':32s} " + " ".join(f"{r:>18s}" for r in ROLE_ORDER))
        for label, points, gear, with_perks in variants:
            row = []
            for role in ROLE_ORDER:
                rs = []
                for spec in [s for s in specs if C.classes[s]["role"] == role]:
                    hero = sim.spec_hero(spec, level, points=points)
                    if gear == "starter":
                        starter_gear(C.items, C.classes, C.balance, hero)
                    elif gear in ("loot", "crafted"):
                        gear_for(hero, level, crafted=gear == "crafted")
                    cdef = kit(C.classes, C.balance, hero)
                    cdef["gear_bonus"] = gear_bonus(C.items, hero, C.classes, C.balance)
                    cdef["armor_cap"] = C.balance["gear"]["armor_cap"]
                    if with_perks:
                        perk = max_perks(hero)
                        cdef["perk_bonus"] = {k: perk[k] for k in ("attack", "hp", "armor")}
                        cdef["heal_bonus"] = perk["heal"]
                        cdef["item_bonus"] = {"potion": perk["potion"], "bandage": perk["bandage"]}
                    res = [fight(cdef, eid, level, level, s * 7919 + level) for eid in pool_at(level) for s in range(seeds)]
                    rs.append((100 * sum(r[0] for r in res) / len(res), 100 * sum(r[1] for r in res) / len(res),
                               sum(r[2] for r in res) / len(res)))
                med = [statistics.median(r[i] for r in rs) for i in range(3)]
                row.append(f"{med[0]:4.0f}/{med[1]:3.0f}/{med[2]:4.1f}".rjust(18))
            print(f"{label:32s} " + " ".join(row))


def pace_mode(seeds: int, jobs: int) -> None:
    """D-108: years to level 100 with full energy (one fight every 2 energy, 20 a day, in zones of the hero's level),
    from the enemies' experience alone (the formula of tests/test_bestiary.py) and corrected by the win rate of
    scenario b (a lost fight gives no experience). [ES] Qué hace: la cuenta del ritmo de D-108 con y sin derrotas."""
    from engine.hero import xp_for_level
    from engine.world.encounters import clamp_level, encounter_pool

    hb = C.balance["hero"]
    scale = hb["xp_level_scale"]
    biomes = [b for b, d in C.biomes.items() if d.get("danger", 0) > 0]

    def xp_per_fight(level: int) -> float:
        total = 0.0
        for biome in biomes:
            pool = encounter_pool(C.enemies, biome, level)
            total += sum(e["xp"] * (1 + scale * (clamp_level(e, level) - 1)) for _, e in pool) / len(pool)
        return total / len(biomes)

    sample = [2, 5, 10, 25, 50, 75, 100]
    specs = sim.active_specs(None)
    out = run_cells([(s, lv, "b", seeds) for s in specs for lv in sample], jobs)
    mean_win = {lv: sum(out[(s, lv, "b", seeds)][0] for s in specs) / len(specs) / 100 for lv in sample}
    low_win = {lv: min(out[(s, lv, "b", seeds)][0] for s in specs) / 100 for lv in sample}

    def at(table: dict, level: int) -> float:
        lo = max(lv for lv in sample if lv <= max(level, sample[0]))
        hi = min(lv for lv in sample if lv >= min(level, sample[-1]))
        if hi == lo:
            return table[lo]
        return table[lo] + (table[hi] - table[lo]) * (level - lo) / (hi - lo)

    def years(win_table: dict | None) -> float:
        days = 0.0
        for lv in range(1, hb["max_level"]):
            need = xp_for_level(hb["xp_formula"], lv + 1) - xp_for_level(hb["xp_formula"], lv)
            days += need / (20 * xp_per_fight(lv) * (at(win_table, lv) if win_table else 1.0))
        return days / 365

    print("Victorias del escenario b (media de las 45 / la peor): " + " · ".join(
        f"L{lv} {100 * mean_win[lv]:.0f}/{100 * low_win[lv]:.0f} %" for lv in sample))
    print(f"Nivel 100 con toda la energía (20 peleas por día): solo experiencia {years(None):.2f} años; con las derrotas "
          f"de la media {years(mean_win):.2f}; con las de la peor especialización {years(low_win):.2f}")


def use_content(content_dir: str) -> None:
    """Measure another copy of content/ (for example the one before a change). [ES] Qué hace: cambia el contenido que
    mide el informe (la carpeta de --content=), para comparar antes y después. La llama: main."""
    global C
    sim.C = load_content(Path(content_dir))
    sim.CTX = CombatContext(sim.C.classes, sim.C.enemies, sim.C.items, sim.C.balance, Texts(sim.C.texts))
    C = sim.C


def main() -> None:
    args = sys.argv[1:]

    def opt(name, default):
        return next((a.split("=", 1)[1] for a in args if a.startswith(f"--{name}=")), default)

    if opt("content", None):
        use_content(opt("content", None))
    only = opt("only", None)
    only = only.split(",") if only else None
    jobs = int(opt("jobs", 4))
    if "--boss" in args:
        sim.boss_mode(only, 6, int(opt("seeds", 100)), 2)
    elif "--trial" in args:
        trial_mode(int(opt("seeds", 20)), jobs)
    elif "--pace" in args:
        pace_mode(int(opt("seeds", 4)), jobs)
    elif "--sources" in args:
        sources_mode(int(opt("seeds", 6)), jobs)
    else:
        levels = [int(x) for x in opt("levels", ",".join(map(str, LEVELS))).split(",")]
        scenarios = opt("scenarios", ",".join(SCENARIOS)).split(",")
        report(only, levels, scenarios, int(opt("seeds", 6)), "--roles" in args, jobs)


if __name__ == "__main__":
    main()
