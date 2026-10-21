"""Camp costs from the first works to the castle (D-101, D-295, D-304, D-317, D-318): raw, energy, ranks and pace.

Usage (from the repository root):
    python tools/camp_costs.py                    # Markdown tables: per work, totals (before 0.45 / 0.45 / now), the pace
    python tools/camp_costs.py --share=0.5        # members give half their daily energy to the camp (default 0.75)
    python tools/camp_costs.py --growth-no-oficio # what if the 13 profession buildings did not raise the +15 % (P-246)
    python tools/camp_costs.py --content=<folder> # measure another copy of content/

Model (every number comes from content/, except the measured energy per hunted unit of tools/sim_oficios.py):
    - A work's base cost: content/camp_upgrades.yaml "cost" ("now"), the snapshot COST_045 of what 0.45.1 changed ("0.45")
      or "cost_before" when it has one ("before 0.45"). × (1 + upgrades.cost_growth × works already built), rounded up,
      coins too (D-295, GameService._upgrade_need), the works activated one after the other (the dearest order).
    - Paths: "list" = only the works camps.level_up asks (D-304; they are more than upgrades.castle_min_built), level by
      level: the works the next level asks, then ⏫ camps.level_up_cost_per_level × level. "full" = also every other work
      of each level (the 13 profession buildings and the 🏪 Trueque), after the list ones. The 🪎 chests (6→9) and the 🌙
      Noche de prueba do not change: they are left out.
    - Refined and crafted goods become raw through their recipe (the one without "variant" with the lowest rank; a 🎓
      exclusive one if it is the only one): energy = the recipe's ⚡ ÷ the units one make gives.
    - Gathering: the 6 base resources (balance.yaml stock.regen_mult) in your territory: gather.amount + 1 every 3 zone
      levels (zone at Lejanía camps.min_lejania), × gather.own_land_bonus rounded like GameService._gather_step: ~4.7
      units per ⚡ of whatever the zone has. 🦌 piel and 🍖 carne are hunted outside (no fights in a territory, D-81):
      tools/sim_oficios.py RAW_ENERGY (the piel ÷ professions.skinning.loot_mult). Any other resource: 1 per ⚡.
    - Pace: members by level = camps.members_base + members_per_level × (level − 1), at least 5 (the gremio) and at most
      10; each gives energy.per_day × share to the camp. Days = energy of the level ÷ energy per day of the camp.
    - Ranks: the highest min_rank of the goods a work asks, its 🎓 specialization if the recipe is exclusive, and the days
      of a dedicated crafter to reach it (all its ⚡ to the best recipe, the materials given, as tools/sim_oficios.py; a 🎓
      recipe also waits for specs.recipe_mastery of specs.mastery_xp after the first slot), with the raw it eats.

[ES]
Para qué sirve: recalcular lo que cuesta llevar un campamento hasta castillo con los números de hoy: por obra y en total,
    en crudo por recurso (lo refinado y lo fabricado pasado a crudo con sus recetas), la energía de juntar, refinar y
    fabricar, los oficios y rangos que pide cada obra, las monedas, y los días con 5 a 10 miembros activos. Compara antes de
    la 0.45, la 0.45 y hoy. Es la tabla del registro de balance (diseno/03-personaje/balance.md §7, bloque de la 0.45.1).
Documento de diseño: diseno/03-personaje/balance.md §7; diseno/09-construccion/escalera-del-asentamiento.md §0.2;
    diseno/00-vision/decisiones.md D-295, D-304, D-317, D-318 y D-319
Módulo: herramienta (M24 Construcción, M21 Simulador; no es parte del juego, no la usa ningún cliente)
Depende de: engine/professions/rules.py (rank_of, xp_for_rank),
    tools/sim_oficios.py (Sim: recetas, colores, energía por unidad cazada), content/camp_upgrades.yaml,
    content/professions.yaml, content/balance.yaml (upgrades, camps, gather, stock, energy, specs, travel)
Lo usan: quien cambie los costos de las obras, la escalera de niveles o las recetas que piden las obras;
    tests/test_costos_edificios.py (las bandas del ritmo)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: COST_045 y RANK_045 (la foto de la 0.45 de lo que cambió la 0.45.1, para comparar)
Reglas que nunca se rompen:
    1. El costo de cada obra se calcula como el juego (GameService._upgrade_need): × el crecimiento, hacia arriba.
Si cambias esto, revisa: tests/test_costos_edificios.py y el registro de balance (diseno/03-personaje/balance.md §7)
"""

from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

from engine.professions.rules import rank_of, xp_for_rank  # noqa: E402
from sim_oficios import Sim  # noqa: E402

# What 0.45 asked in the works that 0.45.1 changed (D-319). [ES] Lo que pedía la 0.45 en las obras que cambió la 0.45.1;
# las demás obras piden hoy lo mismo que en la 0.45. Solo para la columna "0.45" de las tablas.
COST_045: dict[str, dict[str, int]] = {
    "muralla": {"piedra": 210, "madera": 60, "arcilla": 40, "paveses_roble": 1},
    "huerto": {"madera": 45, "fibra": 60, "hierba_curativa": 50, "arcilla": 40, "carro_viveres": 1},
    "forja": {"lingote": 60, "cuero_curtido": 15, "madera": 10, "piedra": 10},
}
RANK_045: dict[str, int] = {"literas_roble": 40, "armero_roble": 70}   # [ES] el rango de esas recetas en la 0.45
VERSIONS = ("before", "045", "now")
LABEL = {"before": "antes de la 0.45", "045": "0.45", "now": "hoy"}
TOP_RANK = 75                                          # [ES] hasta dónde mide al artesano dedicado


class Acc:
    """What a cost adds up to. [ES] Lo que suma un costo: crudo por recurso, energía, oficios y rangos, monedas."""

    def __init__(self) -> None:
        self.raw: dict[str, float] = {}
        self.gather = 0.0
        self.make = 0.0
        self.coins = 0
        self.needs: dict[str, int] = {}                          # [ES] oficio → rango más alto (refinado incluido)
        self.crafted: dict[tuple[str, str], int] = {}             # [ES] (oficio de fabricación, 🎓 o "") → rango más alto

    def add(self, other: "Acc") -> None:
        for k, n in other.raw.items():
            self.raw[k] = self.raw.get(k, 0.0) + n
        self.gather += other.gather
        self.make += other.make
        self.coins += other.coins
        for pid, rank in other.needs.items():
            self.needs[pid] = max(self.needs.get(pid, 0), rank)
        for key, rank in other.crafted.items():
            self.crafted[key] = max(self.crafted.get(key, 0), rank)

    @property
    def energy(self) -> float:
        return self.gather + self.make

    @property
    def raw_total(self) -> float:
        return sum(self.raw.values())


class Model:
    """The content and the numbers of the model. [ES] El contenido y los supuestos (ver el encabezado)."""

    def __init__(self, content_dir: Path | None = None, share: float = 0.75, growth_no_oficio: bool = False) -> None:
        self.sim = Sim(content_dir)                                    # [ES] carga el contenido una sola vez
        self.content = self.sim.content
        bal = self.content.balance
        self.bal = bal
        self.share = share
        self.growth_no_oficio = growth_no_oficio
        stations = set(((self.content.professions.get("stations") or {}).get("camp") or {}))
        ladder_ids = {u for ids in ((bal["camps"].get("level_up") or {}).values()) for u in ids}
        # [ES] los 13 edificios de oficio (D-288, D-317): abren una estación y no los pide ⏫ (el 🔥 Fogón sí)
        self.trade_buildings = {uid for uid, u in self.content.camp_upgrades["upgrades"].items()
                                if not u.get("retired") and u.get("kind") == "oficio" and uid in stations and uid not in ladder_ids}
        self.catalog = {uid: u for uid, u in self.content.camp_upgrades["upgrades"].items() if not u.get("retired")}
        self.recipes = {rid: r for rid, r in self.content.professions["recipes"].items() if not r.get("retired")}
        self.profs = self.content.professions["professions"]
        self.growth = float(bal["upgrades"].get("cost_growth", 0.0))
        camps = bal["camps"]
        self.ladder = {int(k): [u for u in v if u in self.catalog] for k, v in (camps.get("level_up") or {}).items()}
        self.levelup_cost = {k: int(n) for k, n in (camps.get("level_up_cost_per_level") or {}).items()}
        self.top = max(self.ladder) if self.ladder else 9
        self.base = set(bal["stock"].get("regen_mult") or {})
        gather = bal["gather"]
        lejania = int(camps.get("min_lejania", 2))
        zone_level = max(1, round(1 + lejania * float(bal["travel"].get("level_per_lejania", 0.9))))
        low, high = gather["amount"]
        land = float(gather["own_land_bonus"])
        amounts = [int((a + zone_level // 3) * land + 0.5) for a in range(int(low), int(high) + 1)]
        self.zone_level = zone_level
        self.per_energy = sum(amounts) / len(amounts)                 # [ES] unidades por ⚡ en tu territorio
        self.per_day = float(bal["energy"]["per_day"])
        self.members_base = int(camps.get("members_base", 2))
        self.members_step = int(camps.get("members_per_level", 2))
        specs = bal.get("specs") or {}
        self.spec_slot = int((specs.get("slots_at") or [25])[0])
        self.spec_xp = float(specs.get("mastery_xp", 0)) * float(specs.get("recipe_mastery", 0))
        self._crafter: dict[str, dict[int, tuple[float, dict[str, float]]]] = {}

    # ---------------------------------------------------------------- costs

    def cost(self, uid: str, version: str) -> dict[str, int]:
        udef = self.catalog[uid]
        if version == "before" and udef.get("cost_before"):
            cost = dict(udef["cost_before"])
        elif version == "045" and uid in COST_045:
            cost = dict(COST_045[uid])
        else:
            cost = dict(udef["cost"])
        return {k: int(n) for k, n in cost.items()}

    def recipe_for(self, item: str) -> tuple[str, dict[str, Any]] | None:
        options = [(rid, r) for rid, r in self.recipes.items() if item in (r.get("output") or {}) and not r.get("variant")]
        if not options:
            return None
        return min(options, key=lambda o: (bool(o[1].get("spec")), int(o[1].get("min_rank", 1)), o[0]))

    def recipe_rank(self, rid: str, rdef: dict[str, Any], version: str) -> int:
        if version == "045" and rid in RANK_045:
            return RANK_045[rid]
        return int(rdef.get("min_rank", 1))

    def unit_energy(self, item: str) -> float:
        if item in self.base:
            return 1.0 / self.per_energy
        return float(self.sim.raw_energy.get(item, 1.0))

    def expand(self, item: str, n: float, version: str, acc: Acc) -> None:
        found = self.recipe_for(item)
        if found is None:
            acc.raw[item] = acc.raw.get(item, 0.0) + n
            acc.gather += n * self.unit_energy(item)
            return
        rid, rdef = found
        times = n / int(rdef["output"][item])
        acc.make += times * int(rdef.get("energy", 1))
        pid = rdef["profession"]
        rank = self.recipe_rank(rid, rdef, version)
        acc.needs[pid] = max(acc.needs.get(pid, 0), rank)
        if self.profs.get(pid, {}).get("branch") != "refine":
            key = (pid, str(rdef.get("spec") or ""))
            acc.crafted[key] = max(acc.crafted.get(key, 0), rank)
        for i, k in (rdef.get("inputs") or {}).items():
            self.expand(i, int(k) * times, version, acc)

    def analyze(self, cost: dict[str, int], version: str) -> Acc:
        acc = Acc()
        for item, n in cost.items():
            if item == "coins":
                acc.coins += int(n)
            else:
                self.expand(item, n, version, acc)
        return acc

    def work(self, uid: str, version: str, mult: float = 1.0) -> Acc:
        cost = self.cost(uid, version)
        coins = int(self.catalog[uid].get("coins") or 0)
        if coins:
            cost["coins"] = coins
        if mult != 1.0:
            cost = {k: max(1, math.ceil(n * mult - 1e-9)) for k, n in cost.items()}
        return self.analyze(cost, version)

    def required(self) -> dict[str, int]:
        """Work → the level it lets the camp reach (camps.level_up)."""
        return {uid: target for target, ids in self.ladder.items() for uid in ids}

    # ---------------------------------------------------------------- paths

    def path(self, version: str, full: bool) -> list[dict[str, Any]]:
        """Level by level from 1: the works built there (list ones first) and ⏫ to the next level."""
        required = self.required()
        built = 0
        steps = []
        for level in range(1, self.top):
            works = list(self.ladder.get(level + 1, []))
            if full:
                works += [uid for uid, u in self.catalog.items() if int(u["level"]) == level and uid not in required]
            acc = Acc()
            for uid in works:
                acc.add(self.work(uid, version, round(1.0 + self.growth * built, 4)))
                if not (self.growth_no_oficio and uid in self.trade_buildings):
                    built += 1
            acc.add(self.analyze({k: n * level for k, n in self.levelup_cost.items()}, version))
            members = min(10, max(5, self.members_base + self.members_step * (level - 1)))
            steps.append({"level": level, "works": works, "acc": acc, "members": members,
                          "days": acc.energy / (members * self.per_day * self.share)})
        return steps

    def total(self, steps: list[dict[str, Any]]) -> Acc:
        acc = Acc()
        for step in steps:
            acc.add(step["acc"])
        return acc

    # ---------------------------------------------------------------- the dedicated crafter

    def crafter(self, pid: str) -> dict[int, tuple[float, dict[str, float]]]:
        """Rank → (days, raw eaten) of a crafter giving all its ⚡ to the best recipe its rank opens (sim_oficios)."""
        if pid in self._crafter:
            return self._crafter[pid]
        sim = self.sim
        own = [r for r in sim.recipes.values() if r["profession"] == pid]
        xp, energy = 0.0, 0.0
        eaten: dict[str, float] = {}
        marks: dict[int, tuple[float, dict[str, float]]] = {}
        best: dict[int, dict[str, Any]] = {}
        while True:
            rank = rank_of(int(xp), sim.formula, sim.max_rank)
            if rank not in marks:
                acc = Acc()
                for item, n in eaten.items():
                    self.expand(item, n, "now", acc)
                marks[rank] = (energy / self.per_day, dict(acc.raw))
            if rank >= TOP_RANK:
                break
            if rank not in best:
                options = [(sim.make_xp(r, rank) / int(r.get("energy", 1)), i, r) for i, r in enumerate(own)
                           if int(r.get("min_rank", 1)) <= rank and sim.make_xp(r, rank) > 0]
                if not options:
                    break
                best[rank] = max(options, key=lambda o: (o[0], -o[1]))[2]
            rdef = best[rank]
            xp += sim.make_xp(rdef, rank)
            energy += int(rdef.get("energy", 1))
            for item, n in (rdef.get("inputs") or {}).items():
                eaten[item] = eaten.get(item, 0.0) + int(n)
        self._crafter[pid] = marks
        return marks

    def reach(self, pid: str, rank: int, spec: bool = False) -> tuple[float, float] | None:
        """(days, raw units eaten) for a dedicated crafter of `pid` to make a recipe of `rank` (🎓: + its mastery)."""
        if spec:
            formula = self.sim.formula
            rank = max(rank, rank_of(int(xp_for_rank(formula, self.spec_slot) + self.spec_xp), formula, self.sim.max_rank))
        marks = self.crafter(pid)
        hits = [r for r in marks if r >= rank]
        if not hits:
            return None
        days, raw = marks[min(hits)]
        return days, sum(raw.values())


# ---------------------------------------------------------------- printing


def fmt(n: float) -> str:
    return f"{n:,.0f}".replace(",", ".")


def raw_text(raw: dict[str, float]) -> str:
    return ", ".join(f"{k} {fmt(v)}" for k, v in sorted(raw.items(), key=lambda kv: -kv[1]) if v >= 0.5)


def needs_text(model: Model, acc: Acc) -> str:
    """"carpinteria 10; medicina 1; refinado 1: aserradero, …" (🎓 marks a specialization's exclusive recipe)."""
    parts = [f"{pid} {rank}" + (f" 🎓 {spec}" if spec else "")
             for (pid, spec), rank in sorted(acc.crafted.items(), key=lambda kv: (-kv[1], kv[0]))]
    refine = sorted(pid for pid in acc.needs if model.profs.get(pid, {}).get("branch") == "refine")
    if refine:
        parts.append("refinado 1: " + ", ".join(refine))
    return "; ".join(parts) or "—"


def top_need(model: Model, acc: Acc) -> tuple[str, int, str, tuple[float, float] | None]:
    """The crafted good that takes a dedicated crafter longest: (profession, rank, 🎓 or "", (days, raw eaten))."""
    best: tuple[str, int, str, tuple[float, float] | None] = ("", 0, "", None)
    for (pid, spec), rank in acc.crafted.items():
        if rank <= 1 and not spec:
            continue
        reach = model.reach(pid, rank, bool(spec))
        if best[3] is None or (reach and reach[0] > best[3][0]):
            best = (pid, rank, spec, reach)
    return best


def same_trade_specs(acc: Acc) -> int:
    """How many different 🎓 exclusive recipes of one same profession a cost asks (one hero holds one until rank 75)."""
    count: dict[str, int] = {}
    for pid, spec in acc.crafted:
        if spec:
            count[pid] = count.get(pid, 0) + 1
    return max(count.values(), default=0)


def main(argv: list[str]) -> int:
    folder = next((Path(a.split("=", 1)[1]) for a in argv if a.startswith("--content=")), None)
    share = next((float(a.split("=", 1)[1]) for a in argv if a.startswith("--share=")), 0.75)
    model = Model(folder, share, "--growth-no-oficio" in argv)
    required = model.required()
    print(f"Supuestos: {model.per_energy:.2f} unidades de recurso de base por ⚡ en tu territorio (zona de nivel "
          f"{model.zone_level}, +{int((float(model.bal['gather']['own_land_bonus']) - 1) * 100)} %); 🦌 piel "
          f"{model.unit_energy('piel'):.2f} ⚡ y 🍖 carne {model.unit_energy('carne'):.2f} ⚡ cazando; refinar y fabricar, el ⚡ "
          f"de su receta; cada miembro da {model.per_day * share:g} ⚡ por día ({share:.0%} de {model.per_day:g}); de 5 a 10 "
          f"miembros según el nivel; +{model.growth:.0%} por obra construida"
          + (" (sin contar los edificios de oficio)" if model.growth_no_oficio else "") + ", obras una tras otra.")
    print()
    print("## Obra por obra (costo de base, sin el +15 % por obra)")
    print()
    print("| Obra | Nivel | Para subir a | En crudo antes / 0.45 / hoy | ⚡ antes / 0.45 / hoy | Hoy pide (crudo) | Oficios y rango (hoy) | 🥉 |")
    print("|---|---|---|---|---|---|---|---|")
    for uid, udef in model.catalog.items():
        accs = {v: model.work(uid, v) for v in VERSIONS}
        crudo = " / ".join(fmt(accs[v].raw_total) for v in VERSIONS)
        energy = " / ".join(fmt(accs[v].energy) for v in VERSIONS)
        target = required.get(uid)
        print(f"| {uid} | {udef['level']} | {target or '—'} | {crudo} | {energy} | {raw_text(accs['now'].raw)} | "
              f"{needs_text(model, accs['now'])} | {accs['now'].coins or ''} |")
    print()
    print("## Del campamento al castillo (con el +15 % por obra y ⏫ Siguiente nivel)")
    print()
    print("| Camino | Versión | Obras | En crudo | 🦌 piel | ⚙️ metal | ⚡ juntar | ⚡ refinar y fabricar | ⚡ total | 🥉 | Días | "
          "Lo más alto que pide | Un artesano dedicado tarda |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for full in (False, True):
        for version in VERSIONS:
            steps = model.path(version, full)
            acc = model.total(steps)
            works = sum(len(s["works"]) for s in steps)
            days = sum(s["days"] for s in steps)
            pid, rank, spec, reach = top_need(model, acc)
            need = f"{pid} {rank}" + (" 🎓" if spec else "") if pid else "—"
            wait = f"{reach[0]:.0f} días ({fmt(reach[1])} en crudo)" if reach else "—"
            if same_trade_specs(acc) > 1:
                wait += f" · {same_trade_specs(acc)} 🎓 distintas de {pid}: 2 artesanos"
            metal = acc.raw.get("pieza_metal", 0.0)
            print(f"| {'lista (D-304)' if not full else 'completo'} | {LABEL[version]} | {works} | {fmt(acc.raw_total)} | "
                  f"{fmt(acc.raw.get('piel', 0))} | {fmt(metal)} | {fmt(acc.gather)} | {fmt(acc.make)} | {fmt(acc.energy)} | "
                  f"{fmt(acc.coins)} | {days:.1f} | {need} | {wait} |")
    print()
    print("## El camino de la lista, nivel por nivel (hoy)")
    print()
    print("| Nivel | Obras que pide el siguiente | Miembros | ⚡ | Días | Llega el día | Lo más alto que pide | Artesano dedicado |")
    print("|---|---|---|---|---|---|---|---|")
    day = 0.0
    for step in model.path("now", False):
        day += step["days"]
        pid, rank, spec, reach = top_need(model, step["acc"])
        need = f"{pid} {rank}" + (" 🎓" if spec else "") if pid else "refinado o nada"
        ok = "—" if not reach else f"{reach[0]:.0f} días" + (" ✅" if reach[0] <= day else f" (espera {reach[0] - day:.0f})")
        print(f"| {step['level']} → {step['level'] + 1} | {', '.join(step['works']) or '—'} | {step['members']} | "
              f"{fmt(step['acc'].energy)} | {step['days']:.1f} | {day:.1f} | {need} | {ok} |")
    print()
    print("Aparte y sin cambios: los 🪎 cofres desde el nivel 6 (6 hasta castillo), la 🌙 Noche de prueba y 🗺️ Agrandar territorio.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
