"""Combat balance simulator: plays many solo fights with a simple "basic play" policy.

Usage (from the repository root):
    python3 tools/sim.py --summary [--only=spec1,spec2] [--real]
        One line per spec against enemies whose minimum level is 1-3, at the enemy's level.
        By default the hero uses the spec's first 3 abilities with no talent bonus and no gear (the old check);
        with --real it uses the real kit (level - 1 points in the spec, automatic bar, passives, starter gear).
    python3 tools/sim.py --bars --level=25 [--only=...] [--seeds=12]
        Every valid combat bar (slot 1 = a response, slots 2-3 = two other unlocked abilities) of every spec,
        with all points in that spec, against every enemy scaled to that level. Shows the automatic bar,
        the best and the worst bar of each spec, and flags bars clearly above the rest.
    python3 tools/sim.py [enemy_id ...]
        Win rate of every spec against each enemy at its minimum level.

[ES]
Para qué sirve: probar el balance del combate sin jugar a mano. Juega miles de peleas con una forma
de jugar básica (lee el aviso, se cura si está bajo, mantiene mejoras y debilitamientos, y pega).
Documento de diseño: diseno/03-personaje/talentos.md (D-79); diseno/04-combate/ronda-y-acciones.md
Módulo: herramienta (no es parte del juego; no lo usa ningún cliente)
Depende de: engine.core, engine.combat, engine.hero, engine.classes, content/*
Lo usan: las personas e IAs que mueven números de balance (antes de cambiar classes.yaml o balance.yaml)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno (no guarda nada)
Reglas que nunca se rompen:
    1. Usa las mismas funciones de combate que el juego (make_combat, validate_choice, resolve_round).
    2. Es determinista: las mismas semillas dan los mismos números.
Si cambias esto, revisa:
    - Que la forma de jugar (choose) siga entendiendo todos los "kind" de content/classes.yaml
    - Objetivos de D-79: victorias ≥ 95 % contra enemigos de nivel 1-3 (curadores ≥ 80 %) y ninguna barra muy por encima
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from engine.classes import bar_choices, bar_slots, base_response, kit, specs_of, spend_point  # noqa: E402
from engine.combat import CombatContext, make_combat, resolve_round, validate_choice  # noqa: E402
from engine.core import Texts, load_content  # noqa: E402
from engine.hero import Hero, hero_stats  # noqa: E402
from engine.hero.gear import gear_bonus, starter_gear  # noqa: E402

C = load_content()
CTX = CombatContext(C.classes, C.enemies, C.items, C.balance, Texts(C.texts))


def ok(state, hero, cdef, choice) -> bool:
    """True if the choice is valid now. [ES] Qué hace: pregunta al combate si se puede usar. La llaman: choose. Si cambia, afecta: solo el simulador."""
    return validate_choice(state, hero, cdef, choice, CTX) is None


def choose(state, hero, cdef, max_hp, enemy_id, stats):
    """Basic play: read the warning, heal when low, keep buffs and debuffs up, otherwise hit.

    [ES] Qué hace: elige la acción de la ronda como lo haría un jugador básico. La llaman: play. Si cambia, afecta: todos los números del simulador.
    """
    enemy, hs = state["enemy"], state["hero"]
    move = [m for m in C.enemies[enemy_id]["moves"] if m["id"] == enemy["next_move"]][0]
    tags = move.get("tags", [])
    abilities = list(enumerate(cdef["abilities"]))

    def can(i):
        return ok(state, hero, cdef, {"type": "ability", "index": i})

    def use(i):
        return {"type": "ability", "index": i}

    frac = hero.hp / max_hp
    if frac < 0.45:
        for i, a in abilities:
            if a["kind"] == "heal" and can(i):
                return use(i)
    if frac < 0.35 and hero.belt.get("pocion_vida") and ok(state, hero, cdef, {"type": "item", "item_id": "pocion_vida"}):
        return {"type": "item", "item_id": "pocion_vida"}
    first = stats["initiative"] >= enemy["initiative"]
    channel = move.get("kind") == "channel"
    big = (not channel) and move.get("power", 1) * enemy.get("buff", 1.0) > 1.5
    if channel and "interruptible" in tags and first:
        for i, a in abilities:
            if a["kind"] == "interrupt" and can(i):
                return use(i)
    if big:
        if "interruptible" in tags and first:
            for i, a in abilities:
                if a["kind"] == "interrupt" and can(i):
                    return use(i)
        prefs = []
        for i, a in abilities:
            r = a.get("response")
            if r == "dodge" and "dodgeable" in tags:
                prefs.append((0, i))
            elif r == "block" and "blockable" in tags:
                prefs.append((1, i))
            elif r == "shield":
                prefs.append((2, i))
        for _, i in sorted(prefs):
            if can(i):
                return use(i)
        for i, a in abilities:
            if a["kind"] == "weaken" and not enemy.get("weakened") and can(i):
                return use(i)
    for i, a in abilities:
        if a["kind"] == "hot" and frac < 0.8 and not hs.get("hot") and can(i):
            return use(i)
    for i, a in abilities:
        k = a["kind"]
        if k == "empower" and not hs.get("empower") and can(i):
            return use(i)
        if k == "expose" and not enemy.get("exposed") and can(i):
            return use(i)
        if k == "weaken" and not enemy.get("weakened") and can(i):
            return use(i)
    for i, a in abilities:
        k = a["kind"]
        if k == "dot" and not enemy.get("dot") and can(i):
            return use(i)
        if k == "finisher" and hs["combo"] >= 3 and can(i):
            return use(i)
        if k == "strike" and can(i):
            return use(i)
        if k == "heal" and frac < 0.6 and can(i):
            return use(i)
    return {"type": "attack"}


def play(cdef, enemy_id, hero_level, enemy_level, seed):
    """One fight; returns (won, hp left fraction, rounds). [ES] Qué hace: juega una pelea completa. La llaman: los modos del simulador. Si cambia, afecta: solo el simulador."""
    stats = hero_stats(cdef, hero_level)
    max_hp = stats["max_hp"]
    hero = Hero(id="t", name="T", class_id="x", level=hero_level, hp=max_hp, belt={"pocion_vida": 2, "venda": 1})
    state = make_combat(enemy_id, C.enemies[enemy_id], enemy_level, cdef, seed)
    for _ in range(60):
        if state["outcome"]:
            break
        resolve_round(state, hero, cdef, choose(state, hero, cdef, max_hp, enemy_id, stats), CTX)
    return state["outcome"] == "victory", hero.hp / max_hp, state["round"]


def spec_hero(spec, level, points=None):
    """A hero of the spec's class with its points all in that spec. [ES] Qué hace: arma un héroe de prueba. La llaman: los modos --real y --bars. Si cambia, afecta: solo el simulador."""
    group = C.classes[spec].get("group", spec)
    hero = Hero(id="t", name="T", class_id=spec, level=level)
    hero.unlocked = [base_response(C.classes, group)]
    hero.points = level - 1 if points is None else points
    while hero.points > 0:
        spend_point(C.classes, C.balance, hero, spec)
    return hero


def real_kit(hero):
    """The hero's combat kit as the game builds it: talents (bar + passives) and the starter gear (D-77). [ES] Qué hace: arma el kit real del héroe de prueba, con el equipo inicial. La llaman: --real y --bars. Si cambia, afecta: solo el simulador."""
    starter_gear(C.items, C.classes, C.balance, hero)
    out = kit(C.classes, C.balance, hero)
    out["gear_bonus"] = gear_bonus(C.items, hero)
    out["armor_cap"] = C.balance["gear"]["armor_cap"]
    return out


def run(cdef, enemies, level_of, hero_level=None, seeds=40):
    wins, hps, rounds = [], [], []
    worst = (101.0, "")
    for eid in enemies:
        lvl = level_of(eid)
        results = [play(cdef, eid, hero_level or lvl, lvl, s) for s in range(seeds)]
        w = 100 * sum(r[0] for r in results) / seeds
        wins.append(w)
        hps.append(100 * sum(r[1] for r in results) / seeds)
        rounds.append(sum(r[2] for r in results) / seeds)
        if w < worst[0]:
            worst = (w, eid)
    return min(wins), sum(wins) / len(wins), sum(hps) / len(hps), sum(rounds) / len(rounds), worst


def active_specs(only):
    out = []
    for cid, cdef in C.classes.items():
        if cdef.get("retired") or (only and not any(cid.startswith(o) for o in only)):
            continue
        out.append(cid)
    return out


def summary(only, real):
    early = [e for e in C.enemies if C.enemies[e]["level_min"] <= 3]
    print(f"{'spec':30s} {'rol':9s} min% avg%  hp%  rondas  peor")
    for cid in active_specs(only):
        if real:
            # Real kit: at each enemy level the hero has level - 1 points, the automatic bar, passives and starter gear.
            def kit_at(level):
                return real_kit(spec_hero(cid, level))
            per_level = {}
            res = []
            for eid in early:
                lvl = max(C.enemies[eid]["level_min"], 1)
                per_level.setdefault(lvl, kit_at(lvl))
                res.append(run(per_level[lvl], [eid], lambda e: max(C.enemies[e]["level_min"], 1)))
            mins = [r[0] for r in res]
            worst = min((r[4] for r in res), key=lambda w: w[0])
            line = (min(mins), sum(r[1] for r in res) / len(res), sum(r[2] for r in res) / len(res), sum(r[3] for r in res) / len(res), worst)
        else:
            cdef = dict(C.classes[cid])
            cdef["abilities"] = cdef["abilities"][:3]
            line = run(cdef, early, lambda e: max(C.enemies[e]["level_min"], 1))
        mn, avg, hp, rds, worst = line
        print(f"{cid:30s} {C.classes[cid]['role']:9s} {mn:4.0f} {avg:4.0f} {hp:4.0f}  {rds:5.1f}  {worst[1] if worst[0] < 100 else ''}")


def all_bars(spec, hero):
    """The automatic bar and every valid bar of a hero: (response, other, other). [ES] Qué hace: lista todas las barras posibles. La llaman: el modo --bars. Si cambia, afecta: solo el simulador."""
    hero.bar = []
    auto = bar_slots(C.classes, hero)
    responses = [auto[0]] + bar_choices(C.classes, hero, 1)
    known = {a["id"] for s in specs_of(C.classes, C.classes[spec]["group"]) for a in C.classes[s]["abilities"]}
    pool = [a for a in hero.unlocked if a in known]
    bars = []
    for resp in responses:
        for pair in itertools.combinations([a for a in pool if a != resp], 2):
            bars.append((resp,) + pair)
    return auto, bars


def bars_mode(only, level, seeds):
    enemies = list(C.enemies)
    abilities = {a["id"]: a for c in C.classes.values() for a in c["abilities"]}
    print(f"Nivel {level} (héroe y enemigos), {seeds} semillas × {len(enemies)} enemigos por barra")
    print(f"{'spec':28s} {'rol':9s} {'n':>3s}  {'auto win/hp':>11s}  {'mejor win/hp':>12s}  {'peor win/hp':>11s}  mejor barra")
    rows = []
    for cid in active_specs(only):
        hero = spec_hero(cid, level)
        auto, bars = all_bars(cid, hero)
        base = real_kit(hero)

        def score(bar):
            cdef = dict(base)
            cdef["abilities"] = [abilities[a] for a in bar]
            res = run(cdef, enemies, lambda e: level, hero_level=level, seeds=seeds)
            return res[1], res[2]

        results = [(score(b), b) for b in bars]
        auto_score = score(tuple(auto))
        best = max(results)
        worst = min(results)
        rows.append((cid, best[0]))
        print(f"{cid:28s} {C.classes[cid]['role']:9s} {len(bars):3d}  {auto_score[0]:5.0f}/{auto_score[1]:4.0f}  "
              f"{best[0][0]:6.0f}/{best[0][1]:4.0f}  {worst[0][0]:5.0f}/{worst[0][1]:4.0f}  {', '.join(best[1])}")
    if rows:
        # A bar is "clearly above" when its health left beats the median best bar of its role by more than 12 points.
        flagged = []
        for role in sorted({C.classes[r[0]]["role"] for r in rows}):
            values = sorted(r[1][1] for r in rows if C.classes[r[0]]["role"] == role)
            median = values[len(values) // 2]
            flagged += [f"{r[0]} ({r[1][1]:.0f} vs {median:.0f})" for r in rows if C.classes[r[0]]["role"] == role and r[1][1] > median + 12]
            print(f"Rol {role}: mediana de vida restante con la mejor barra {median:.0f} %")
        print(f"Barras muy por encima de su rol (+12): {', '.join(flagged) or 'ninguna'}")


def main():
    args = sys.argv[1:]
    only = [a[7:].split(",") for a in args if a.startswith("--only=")]
    only = only[0] if only else None
    level = int(next((a[8:] for a in args if a.startswith("--level=")), 25))
    seeds = int(next((a[8:] for a in args if a.startswith("--seeds=")), 12))
    if "--bars" in args:
        bars_mode(only, level, seeds)
    elif "--summary" in args:
        summary(only, "--real" in args)
    else:
        names = [a for a in args if not a.startswith("--")] or list(C.enemies)
        for eid in names:
            lvl = max(C.enemies[eid]["level_min"], 1)
            row = []
            for cid in active_specs(None):
                cdef = dict(C.classes[cid])
                cdef["abilities"] = cdef["abilities"][:3]
                r = [play(cdef, eid, lvl, lvl, s) for s in range(40)]
                row.append(f"{cid[:4]} {sum(w for w, _, _ in r) * 100 // 40:3d}%")
            print(f"{eid:20s} L{lvl:<2d} " + " | ".join(row))


if __name__ == "__main__":
    main()
