"""Professions pace after the recipe reform (D-306, 0.44): days to rank 25 / 50 / 75 / 100 of a dedicated crafter.

Usage (from the repository root):
    python tools/sim_oficios.py            # a Markdown table, one line per crafting or refining profession
    python tools/sim_oficios.py --detail   # plus, per tiered profession, the recipe it makes at each rank band
    python tools/sim_oficios.py --content=<folder>   # measure another copy of content/ (for example, the one before a change)

Model (the "solo su ⚡" column of diseno/07-economia/simulacion-oficios.md: the materials are already in the backpack):
    - All the day's energy (balance.yaml energy.per_day) goes to one profession, starting at rank 1 with no xp.
    - At each make the crafter picks the recipe with the most profession xp per ⚡ among those its rank opens (not 🎓
      exclusive, not retired; every 📚 recipe book is bought on time). In the tiered professions (balance.yaml
      recipe_tiers.professions) the xp of a make is the recipe's xp × its color share at the rank it has then (the same
      rule as GameService._recipe_xp); the other professions give the recipe's whole xp, as before.
    - "Cadena aprox." adds the energy of gathering and refining every material yourself, with the energy per raw unit
      measured for the simulation of 18-oct (simulacion-oficios.md §1 and §4: mid distance, Lejanía ≤ 6) in RAW_ENERGY.
      It is an approximation: it ignores the other professions rising on the way, the rank's extra unit and travel.

[ES]
Para qué sirve: recalcula cuánto tarda un especialista en llevar un oficio al 25, 50, 75 y 100 con las recetas y los
    números de hoy (D-306: tramos cada 5 rangos, colores de receta, experiencia y energía que crecen con el tramo), cuántas
    piezas hace y una cuenta aproximada de lo que tarda si junta y refina todo él mismo. Es la tabla del §11 de
    simulacion-oficios.md (los scripts del 18-oct, que medían el mundo con el motor, quedaron fuera del repositorio; este
    reemplaza la parte de "solo su ⚡" y aproxima la cadena con lo que ellos midieron).
Documento de diseño: diseno/07-economia/simulacion-oficios.md §11; diseno/00-vision/decisiones.md D-306 y D-315
Módulo: herramienta (M14 Oficios, M21 Simulador; no es parte del juego, no la usa ningún cliente)
Depende de: engine/core/content.py (load_content), engine/professions/rules.py (rank_of, recipe_color, color_factor),
    content/balance.yaml (professions.rank_formula, energy.per_day, recipe_tiers), content/professions.yaml
Lo usan: quien cambie la curva, los tramos o la experiencia de las recetas (y el registro de balance)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno (solo lee e imprime)
Reglas que nunca se rompen:
    1. La regla de experiencia es la misma que la del juego (color por vez, con el rango de ese momento).
Si cambias esto, revisa: simulacion-oficios.md §11 y el registro de balance (diseno/03-personaje/balance.md)
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.core import load_content  # noqa: E402
from engine.professions.rules import color_factor, rank_of, recipe_color, xp_for_rank  # noqa: E402

# ⚡ per raw unit at mid distance (Lejanía ≤ 6), measured on 18-oct (simulacion-oficios.md §1 and §4). [ES] Energía por unidad
# cruda, de la simulación del 18-oct: recolectar en la mejor zona hasta Lejanía 6; la piel y la carne cazando (2 ⚡ por presa);
# gemas y flores de luna con el recolector en rango (con el metal o la hierba que salen en la misma vuelta). Aproximado.
RAW_ENERGY = {"madera": 0.65, "pieza_metal": 0.73, "fibra": 0.67, "hierba_curativa": 0.68, "piedra": 0.65, "arcilla": 1.0,
              "piel": 4.4, "carne": 3.3, "pescado": 1.5, "gema_bruta": 7.0, "flor_luna": 7.0}
# [ES] La piel se divide por balance.yaml professions.skinning.loot_mult.piel (0.43, D-306.5: ×2,5 → ~1,8 ⚡ por piel); con el
# contenido de antes (sin ese número) queda en 4,4.
OTHER_RAW = 1.0          # [ES] cualquier otro recurso propio de un terreno (~1 unidad por ⚡ en su terreno)
MARKS = (25, 50, 75, 100)


class Sim:
    """The content and the rules the simulation needs. [ES] El contenido y las reglas que usa la simulación."""

    def __init__(self, content_dir: Path | None = None) -> None:
        self.content = load_content(content_dir)
        balance = self.content.balance
        self.formula = balance["professions"]["rank_formula"]
        self.max_rank = int(balance["professions"]["max_rank"])
        self.per_day = float(balance["energy"]["per_day"])
        self.tiers = balance.get("recipe_tiers") or {}
        recipes = self.content.professions["recipes"]
        self.recipes = {rid: r for rid, r in recipes.items() if not r.get("retired") and not r.get("spec")}
        self.profs = self.content.professions["professions"]
        self._raw_cache: dict[str, float] = {}
        mult = float(((balance["professions"].get("skinning") or {}).get("loot_mult") or {}).get("piel", 1.0))
        self.raw_energy = dict(RAW_ENERGY, piel=RAW_ENERGY["piel"] / mult)

    def tiered(self, pid: str) -> bool:
        return pid in (self.tiers.get("professions") or [])

    def make_xp(self, rdef: dict[str, Any], rank: int) -> int:
        """Profession xp of one make at this rank (GameService._recipe_xp)."""
        base = int(rdef.get("xp", 0))
        if not self.tiered(rdef["profession"]):
            return base
        colors = self.tiers.get("colors") or []
        return int(base * color_factor(recipe_color(rank, int(rdef.get("min_rank", 1)), colors), colors) + 1e-9)

    def unit_energy(self, item: str) -> float:
        """⚡ to get one unit of a material yourself: gathered (RAW_ENERGY) or refined with the first recipe that makes it."""
        if item in self._raw_cache:
            return self._raw_cache[item]
        cost = self.raw_energy.get(item)
        if cost is None:
            refine = next((r for r in self.recipes.values() if item in r["output"]
                           and self.profs.get(r["profession"], {}).get("branch") == "refine"), None)
            if refine:
                made = int(refine["output"][item])
                cost = (int(refine.get("energy", 1)) + sum(self.unit_energy(i) * int(n) for i, n in refine["inputs"].items())) / made
            else:
                cost = OTHER_RAW
        self._raw_cache[item] = cost
        return cost

    def chain_energy(self, rdef: dict[str, Any]) -> float:
        """⚡ of one make with its materials gathered and refined by the crafter (per unit of output, like the xp)."""
        return int(rdef.get("energy", 1)) + sum(self.unit_energy(i) * int(n) for i, n in rdef["inputs"].items())

    def run(self, pid: str, chain: bool) -> dict[str, Any]:
        """Make the best recipe again and again until rank 100: energy and makes at each mark, and the recipe by rank."""
        own = [(rid, r) for rid, r in self.recipes.items() if r["profession"] == pid]
        xp, energy, makes = 0.0, 0.0, 0
        out: dict[str, Any] = {"marks": {}, "picks": {}}
        best_at: dict[int, tuple[str, dict[str, Any], float]] = {}
        stuck = 0
        while True:
            rank = rank_of(int(xp), self.formula, self.max_rank)
            for mark in MARKS:
                if rank >= mark and mark not in out["marks"]:
                    out["marks"][mark] = (energy, makes)
            if rank >= self.max_rank:
                break
            if rank not in best_at:
                options = []
                for rid, r in own:
                    if int(r.get("min_rank", 1)) > rank:
                        continue
                    gain = self.make_xp(r, rank)
                    cost = self.chain_energy(r) if chain else int(r.get("energy", 1))
                    if gain > 0:
                        options.append((gain / cost, rid, r, cost))
                if not options:
                    out["stuck"] = rank
                    break
                _, rid, r, cost = max(options, key=lambda o: o[0])
                best_at[rank] = (rid, r, cost)
                out["picks"][rank] = rid
            rid, r, cost = best_at[rank]
            gain = self.make_xp(r, rank)
            xp += gain
            energy += cost
            makes += 1
            stuck = stuck + 1 if gain == 0 else 0
        return out


def days(energy: float, per_day: float) -> str:
    return f"{energy / per_day:,.0f}".replace(",", ".")


def main(argv: list[str]) -> int:
    folder = next((Path(a.split("=", 1)[1]) for a in argv if a.startswith("--content=")), None)
    sim = Sim(folder)
    order = [pid for pid, p in sim.profs.items() if p.get("branch") in ("craft", "refine") and not p.get("locked")
             and any(r["profession"] == pid for r in sim.recipes.values())]
    print(f"Energía por día: {sim.per_day:g} ⚡ · curva: {sim.formula['base']} × (rango − 1)^{sim.formula['exponent']} "
          f"(rango 100: {xp_for_rank(sim.formula, 100):,} de experiencia)".replace(",", "."))
    print()
    print("| Oficio | Tramos y colores | Solo su ⚡: días al 25 / 50 / 75 / 100 | Veces hasta el 100 | Cadena aprox.: días al 25 / 50 / 100 |")
    print("|---|---|---|---|---|")
    for pid in order:
        alone, chain = sim.run(pid, chain=False), sim.run(pid, chain=True)
        marks = alone["marks"]
        solo = " / ".join(days(marks[m][0], sim.per_day) if m in marks else "—" for m in MARKS)
        if "stuck" in alone:
            solo += f" (se traba en el rango {alone['stuck']})"
        times = f"{marks[100][1]:,}".replace(",", ".") if 100 in marks else "—"
        cm = chain["marks"]
        chain_txt = " / ".join(days(cm[m][0], sim.per_day) if m in cm else "—" for m in (25, 50, 100))
        print(f"| {pid} | {'sí' if sim.tiered(pid) else 'no'} | {solo} | {times} | {chain_txt} |")
    if "--detail" in argv:
        for pid in order:
            if not sim.tiered(pid):
                continue
            picks = sim.run(pid, chain=False)["picks"]
            print(f"\n{pid}: " + " · ".join(f"r{rank}: {rid}" for rank, rid in sorted(picks.items()) if rank % 10 == 0 or rank == 1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
