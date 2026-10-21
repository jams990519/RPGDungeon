"""Generate the recipe tiers of D-306: a tier every 5 ranks in every refining and crafting profession.

Version 0.44 (D-315) did the gear professions (piece level = rank); version 0.52 (D-328) adds the refining professions,
⚗️ Alchemy, 🩺 Medicine and 🍲 Cooking, so every profession with recipes has one tier every 5 ranks up to 100.

Usage (from the repository root):
    python tools/recipe_tiers.py            # write the content files below
    python tools/recipe_tiers.py --check    # change nothing; exit 1 (and say what) if a file is not up to date

What it writes (always the same output for the same input: running it twice changes nothing):
    content/professions.yaml
        - Every recipe of a tiered profession (balance.yaml recipe_tiers.professions) gets its rank, energy and xp:
          a gear piece of level N is made from rank tier_rank(N) (level 3 → 1, 5 → 5, 8 → 10, 10 → 10 … 100 → 100);
          its energy comes from recipe_tiers.energy_by_rank and its xp from recipe_tiers.xp_per_rank (base 12 per
          piece; 6 per ⚡ for the rest: bandages, 🪑 furniture, the hand-written refining, potions, remedies and dishes
          keep their energy and rank). 🎓 exclusive recipes keep their rank.
        - The mail recipes (output of type "malla", D-208) get retired: true. The mail pieces stay in content/items.yaml:
          whoever made one keeps it (D-64).
        - A generated block at the end ("BEGIN GENERATED" … "END GENERATED"):
            * gear (0.44): one recipe per line and per new level (15, 25 … 95), with the materials halfway between its
              two neighbours (rounded up);
            * refining (0.52, recipe_tiers.refine): one better refined material per tier (5, 10 … 100) in each refining
              profession, made from its base refined material, its raw material and a catalyst (resin, coal…);
            * ⚗️ 🩺 🍲 (0.52, recipe_tiers.consumables): one recipe per tier that has none (5, 10 … 100), interpolated
              between the hand-written "anchor" recipes around it (and a virtual top at rank 100 when the last anchor
              is lower): materials, units per make, heal, toxicity, rations and price.
          Every generated recipe costs tier_energy(rank) and gives tier_xp(12, rank), like a gear piece.
    content/items.yaml
        - A generated block at the end: the new crafted pieces (levels 15, 25 … 95 of each gear line), with stats and
          price halfway between the pieces of level N − 5 and N + 5 of the same line; and (0.52) the new refined
          materials, potions, remedies and dishes, each with its stable code (balance.yaml: code + rank ÷ 5).
    content/locales/es_tramos.yaml and en_tramos.yaml
        - The names of the new pieces (the noun of the line, from its level-10 piece, and the place of each level) and,
          since 0.52, of the new materials, potions, remedies and dishes (the noun of its base or anchor and the place of
          its tier), with what each one is for (resources.use.<id>, shown by its code /NNN).

[ES]
Para qué sirve: arma el contenido de la reforma de recetas (D-306, E-221) sin escribirlo a mano: un tramo cada 5 rangos en
    todos los oficios con recetas. En la 0.44 (D-315) los oficios de equipo (🪑 Carpintería, 🔨 Herrería, 🪡 Sastrería,
    🦺 Peletería y 💍 Joyería), con nivel de pieza = rango (simulacion-oficios.md §8.1), la energía y la experiencia que
    crecen con el tramo (§8.2) y las 67 recetas de malla retiradas (E-223, D-208): 180 piezas y 180 recetas. En la 0.52
    (D-328) el refinado (🪚 🔥 💧 🧶 🪣 🗿: un refinado mejor por tramo, 120 materiales), la ⚗️ Alquimia (19 pociones), la
    🩺 Medicina (18 remedios) y la 🍲 Cocina (16 platos), con efectos que crecen con el tramo: curan más, dan más raciones,
    valen más. Mueve el rango de las recetas de equipo que ya estaban (nunca para arriba: nadie pierde una receta, D-64) y
    la experiencia de las recetas de los oficios con tramos. Los IDs nuevos solo se agregan ("<línea>_nivel_<N>" en el
    equipo, "<base>_tramo_<N>" desde la 0.52); los de antes no cambian. Es idempotente: correrla dos veces no cambia nada.
Documento de diseño: diseno/07-economia/simulacion-oficios.md §8 y §11 (lo que quedó en el juego),
    diseno/07-economia/profesiones.md §0.8 y §0.11, diseno/07-economia/oficios-como-wow.md §3,
    diseno/00-vision/decisiones.md D-306, D-315 y D-328
Módulo: herramienta (M14 Oficios; no es parte del juego, no la usa ningún cliente)
Depende de: engine/professions/rules.py (tier_rank, tier_energy, tier_xp, branches_of), engine/core/content.py (_read_texts),
    content/balance.yaml (recipe_tiers: professions, step, energy_by_rank, xp_per_rank, refine, consumables;
    shop.sell_ratio, shop.remedy_sell_ratio), content/professions.yaml, content/items.yaml, content/locales
Lo usan: quien cambie balance.yaml recipe_tiers, el equipo de artesano o una receta "ancla" (las de recipe_tiers.consumables);
    tests/test_tramos_de_recetas.py y tests/test_tramos_refinado_alquimia_medicina_cocina.py (--check)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: los bloques "GENERATED" de professions.yaml e items.yaml y los archivos es_tramos.yaml y
    en_tramos.yaml (no se editan a mano: se cambia la herramienta o el balance y se vuelve a correr)
Reglas que nunca se rompen:
    1. IDs estables: nunca renombra ni borra; retira con retired: true. Lo generado depende solo de lo escrito a mano.
    2. Fabricar nunca fabrica monedas (D-113): lo nuevo vale en el mercader menos que sus materiales (las pociones y los
       remedios, con shop.remedy_sell_ratio).
    3. Toda receta nueva de fabricación pide materiales de 2 oficios o más (D-109); el refinado no hace falta.
    4. Los códigos (code) son estables: el "code" de cada línea en balance.yaml nunca cambia (código = code + rango ÷ 5).
    5. Un tramo nunca da menos que el de abajo: cada poción y remedio cura más, cada plato da más raciones y cada refinado
       vale más que el del tramo anterior (si no, la herramienta se detiene).
Si cambias esto, revisa: tests/test_tramos_de_recetas.py, tests/test_tramos_refinado_alquimia_medicina_cocina.py,
    tests/test_balance_d110.py, tests/test_oficios_equipo.py, tests/test_oficios_campamento.py, tests/test_professions.py,
    tests/test_backpack.py (códigos únicos), el registro de balance (diseno/03-personaje/balance.md) y la simulación
    (tools/sim_oficios.py, simulacion-oficios.md §11)
"""

from __future__ import annotations

import math
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import yaml  # noqa: E402

from engine.core.content import _read_texts  # noqa: E402
from engine.professions.rules import branches_of, tier_energy, tier_rank, tier_xp  # noqa: E402

CONTENT = ROOT / "content"
BEGIN = "# ---- BEGIN GENERATED by tools/recipe_tiers.py"
END = "# ---- END GENERATED by tools/recipe_tiers.py"
NEW_LEVELS = (15, 25, 35, 45, 55, 65, 75, 85, 95)
# The place of each new level, after the noun in Spanish and before it in English. [ES] El lugar de cada nivel nuevo
# (como "de la frontera" en el nivel 10): va detrás del nombre en español y delante en inglés.
PLACE_ES = {15: "de la cañada", 25: "de las cenizas", 35: "del bastión", 45: "de la luna roja", 55: "del trueno",
            65: "de la penumbra", 75: "del coloso", 85: "del cometa", 95: "del cenit"}
PLACE_EN = {15: "Glen", 25: "Ashen", 35: "Bastion", 45: "Bloodmoon", 55: "Thunder", 65: "Gloom", 75: "Colossus",
            85: "Comet", 95: "Zenith"}
# D-328 (0.52): the place of every tier, 5 to 100: the gear's places (10 "de la frontera", 20 "del páramo"… as in es.yaml)
# and one new for the tier 5. [ES] El lugar de cada tramo del 5 al 100 para los refinados, pociones, remedios y platos nuevos:
# los mismos lugares que el equipo de ese nivel (así un jugador reconoce el tramo) y uno nuevo para el 5 ("del sendero").
TIER_PLACE_ES = {5: "del sendero", 10: "de la frontera", 20: "del páramo", 30: "de la vigía", 40: "del ocaso",
                 50: "de la tormenta", 60: "de la escarcha eterna", 70: "del abismo", 80: "de los titanes",
                 90: "de las estrellas", 100: "del alba eterna"} | PLACE_ES
TIER_PLACE_EN = {5: "Trail", 10: "Frontier", 20: "Wasteland", 30: "Vigil", 40: "Twilight", 50: "Storm", 60: "Everfrost",
                 70: "Abyssal", 80: "Titan", 90: "Starlit", 100: "Everdawn"} | PLACE_EN
# D-328: the noun of a new item when its base or anchor name does not fit before a place. [ES] El nombre corto de la línea
# cuando el de la receta ancla no queda bien delante del lugar ("Conservas en tarro del trueno" → "Conservas del trueno").
NOUN = {"vendaje_maestro": ("Vendaje maestro", "Master Bandage"), "racion_campamento": ("Ración", "Ration"),
        "guiso_cazador": ("Guiso", "Stew"), "conserva": ("Conservas", "Preserves"), "festin": ("Festín", "Feast"),
        "banquete": ("Banquete", "Banquet")}
LEVEL10_ES, LEVEL10_EN = " de la frontera", "Frontier "
PIECE_XP = 12           # [ES] experiencia base de una pieza de equipo (2 ⚡ a 6 por ⚡, como antes de la 0.44); también la de cada receta generada en la 0.52
XP_PER_ENERGY = 6       # [ES] experiencia base por ⚡ de lo que no es equipo (vendas, 🪑 muebles, refinados, pociones, remedios y platos escritos a mano)


def _strip_generated(text: str) -> str:
    """The file without its generated block (and the blank line before it)."""
    start = text.find(BEGIN)
    if start < 0:
        return text
    line_start = text.rfind("\n", 0, start) + 1
    end = text.find(END, start)
    end = text.find("\n", end) + 1 if end >= 0 else len(text)
    return text[:line_start].rstrip("\n") + "\n" + text[end:]


def _flow(value: Any) -> str:
    """One YAML value in flow style, as the content files write it ({a: 1, b: "x"})."""
    if isinstance(value, dict):
        return "{" + ", ".join(f"{k}: {_flow(v)}" for k, v in value.items()) + "}"
    if isinstance(value, str):
        return f'"{value}"' if not re.fullmatch(r"[a-z_][a-z0-9_]*", value) else value
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return repr(round(value, 4))
    return str(value)


def _quote(text: str) -> str:
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _half_up(value: float) -> int:
    """Round half up (2.5 → 3), never below 0. [ES] Redondeo "de escuela": la mitad sube."""
    return max(0, int(math.floor(value + 0.5 + 1e-9)))


class Tiers:
    """Everything the tool computes from the hand-written content. [ES] Lo que la herramienta calcula de lo escrito a mano."""

    def __init__(self) -> None:
        self.balance = yaml.safe_load((CONTENT / "balance.yaml").read_text(encoding="utf-8"))
        self.cfg = self.balance["recipe_tiers"]
        self.prof_text = (CONTENT / "professions.yaml").read_text(encoding="utf-8")
        self.items_text = (CONTENT / "items.yaml").read_text(encoding="utf-8")
        self.profs = yaml.safe_load(_strip_generated(self.prof_text))
        self.items = yaml.safe_load(_strip_generated(self.items_text))
        es, en = _read_texts(CONTENT / "locales", "es"), _read_texts(CONTENT / "locales", "en")
        self.es, self.en = es["item"], en["item"]
        self.prof_names = {pid: (es["profession"][pid]["name"], en["profession"][pid]["name"])
                           for pid in self.profs["professions"] if pid in es.get("profession", {})}
        self.tiered = list(self.cfg["professions"])
        self.updates: dict[str, dict[str, Any]] = {}
        self.new_items: dict[str, dict[str, Any]] = {}
        self.new_recipes: dict[str, dict[str, Any]] = {}
        self.names: dict[str, tuple[str, str]] = {}
        # D-328 (0.52): the refining and consumable tiers, apart so the block keeps the 0.44 part first
        self.tier_items: dict[str, dict[str, Any]] = {}
        self.tier_recipes: dict[str, dict[str, Any]] = {}
        self.tier_names: dict[str, tuple[str, str]] = {}
        self.uses: dict[str, tuple[str, str]] = {}
        self._compute()
        self._compute_refine()
        self._compute_consumables()

    def _gear(self, rdef: dict[str, Any]) -> dict[str, Any] | None:
        out = next(iter(rdef.get("output") or {}), None)
        item = self.items.get(out) or {}
        return item if item.get("kind") == "gear" else None

    def _energy_xp(self, rdef: dict[str, Any], rank: int) -> tuple[int, int]:
        """(energy, xp) of a recipe of a tiered profession at this rank (gear pieces: by tier; the rest keep their ⚡)."""
        if self._gear(rdef):
            return tier_energy(rank, self.cfg["energy_by_rank"]), tier_xp(PIECE_XP, rank, float(self.cfg["xp_per_rank"]))
        energy = int(rdef.get("energy", 1))
        return energy, tier_xp(XP_PER_ENERGY * energy, rank, float(self.cfg["xp_per_rank"]))

    def _tier_energy_xp(self, rank: int) -> tuple[int, int]:
        """(energy, xp) of a generated recipe of this rank (D-328: like a gear piece of the same tier)."""
        return tier_energy(rank, self.cfg["energy_by_rank"]), tier_xp(PIECE_XP, rank, float(self.cfg["xp_per_rank"]))

    def _tiers(self) -> list[int]:
        step = int(self.cfg["step"])
        return list(range(step, 101, step))

    def _compute(self) -> None:
        step = int(self.cfg["step"])
        recipes = self.profs["recipes"]
        lines: dict[tuple[str, str, str], dict[int, tuple[str, str]]] = {}
        for rid, rdef in recipes.items():
            if rdef.get("profession") not in self.tiered:
                continue
            item = self._gear(rdef)
            change: dict[str, Any] = {}
            rank = int(rdef.get("min_rank", 1))
            if item and item.get("type") == "malla":            # E-223 / D-208: no more mail (the pieces stay)
                if not rdef.get("retired"):
                    change["retired"] = True
                if change:
                    self.updates[rid] = change
                continue
            if rdef.get("retired"):
                continue
            if item and not rdef.get("spec"):
                rank = tier_rank(int(item.get("req_level", 1)), step)
                out_id = next(iter(rdef["output"]))
                if out_id.startswith("artesano_"):
                    lines.setdefault((rdef["profession"], item["slot"], item["type"]), {})[int(item["req_level"])] = (out_id, rid)
            energy, xp = self._energy_xp(rdef, rank)
            for key, value in (("min_rank", rank), ("energy", energy), ("xp", xp)):
                if int(rdef.get(key, 0)) != value:
                    change[key] = value
            if change:
                self.updates[rid] = change
        ratio = float(self.balance["shop"]["sell_ratio"])
        for (pid, _slot, _typ), by_level in lines.items():
            if 10 not in by_level:
                continue
            base10 = by_level[10][0]
            name_es, name_en = self.es[base10], self.en[base10]
            if not name_es.endswith(LEVEL10_ES) or not name_en.startswith(LEVEL10_EN):
                raise SystemExit(f"recipe_tiers: the level-10 piece {base10} does not follow the naming pattern")
            noun_es, noun_en = name_es[: -len(LEVEL10_ES)], name_en[len(LEVEL10_EN):]
            for level in NEW_LEVELS:
                if level - 5 not in by_level or level + 5 not in by_level:
                    raise SystemExit(f"recipe_tiers: {pid} line of {base10} lacks a neighbour of level {level}")
                (low_id, low_rid), (up_id, up_rid) = by_level[level - 5], by_level[level + 5]
                low, up = self.items[low_id], self.items[up_id]
                new_id = re.sub(r"_\d+$", "", up_id) + f"_nivel_{level}"
                new_rid = new_id if up_rid == up_id else re.sub(r"_\d+$", f"_{level}", up_rid)
                if new_id in self.items or new_rid in recipes:
                    raise SystemExit(f"recipe_tiers: {new_id} / {new_rid} already exist by hand")
                stats = {k: round((float(low.get("stats", {}).get(k, 0)) + float(v)) / 2, 3) for k, v in up["stats"].items()}
                item = {"name_key": f"item.{new_id}", "emoji": up["emoji"], "kind": "gear", "slot": up["slot"],
                        "type": up["type"], "tier": low["tier"], "rarity": up["rarity"], "req_level": level,
                        "source": "crafted", "stats": stats,
                        "price": int(math.floor((int(low["price"]) + int(up["price"])) / 2 + 0.5))}
                low_in, up_in = recipes[low_rid]["inputs"], recipes[up_rid]["inputs"]
                inputs = {k: max(1, math.ceil((int(low_in.get(k, 0)) + int(n)) / 2)) for k, n in up_in.items()}
                first = next(iter(inputs))
                while item["price"] * ratio >= sum(self.items[k]["price"] * n for k, n in inputs.items()):
                    inputs[first] += 1                           # D-113: crafting never makes coins at the merchant
                rdef = {"profession": pid, "inputs": inputs, "output": {new_id: 1}, "min_rank": level}
                rdef["energy"], rdef["xp"] = self._energy_xp(rdef | {"output": {up_id: 1}}, level)
                self.new_items[new_id] = item
                self.new_recipes[new_rid] = rdef
                self.names[new_id] = (f"{noun_es} {PLACE_ES[level]}", f"{PLACE_EN[level]} {noun_en}")

    # ------------------------------------------------------------------ D-328 (0.52): refining tiers

    def _new_id(self, base: str, rank: int) -> str:
        new_id = f"{base}_tramo_{rank}"
        if new_id in self.items or new_id in self.profs["recipes"] or new_id in self.tier_items:
            raise SystemExit(f"recipe_tiers: {new_id} already exists by hand")
        return new_id

    def _noun(self, base: str) -> tuple[str, str]:
        return NOUN.get(base) or (self.es[base], self.en[base])

    def _compute_refine(self) -> None:
        """One better refined material per tier (5 … 100) in each refining profession (balance.yaml recipe_tiers.refine).

        [ES] Qué hace: cada oficio de refinado gana un material por tramo, hecho con su refinado de siempre, su crudo y un
        catalizador (resina, carbón, raíz amarga, lino, corteza, arena): 1 + rango ÷ base_every del refinado de siempre,
        rango ÷ raw_every del crudo (crece en cada tramo) y 1 + rango ÷ catalyst_every del catalizador. Vale lo que valen sus
        materiales más su ⚡ (como el tablón: 3 maderas + 1), así refinar nunca fabrica monedas (D-113).
        """
        cfg = self.cfg.get("refine") or {}
        lines = cfg.get("lines") or {}
        base_every, raw_every = int(cfg.get("base_every", 50)), int(cfg.get("raw_every", 5))
        cat_every = int(cfg.get("catalyst_every", 25))
        ratio = float(self.balance["shop"]["sell_ratio"])
        step = int(self.cfg["step"])
        for pid, line in lines.items():
            base, raw, cat = line["base"], line["raw"], line["catalyst"]
            emoji, noun = self.items[base]["emoji"], self._noun(base)
            pname = self.prof_names.get(pid, (pid, pid))
            pemoji = self.profs["professions"][pid]["emoji"]
            last_price = int(self.items[base]["price"])
            for rank in self._tiers():
                inputs = {base: 1 + rank // base_every, raw: rank // raw_every, cat: 1 + rank // cat_every}
                inputs = {k: n for k, n in inputs.items() if n > 0}
                energy, xp = self._tier_energy_xp(rank)
                price = sum(int(self.items[k]["price"]) * n for k, n in inputs.items()) + energy
                if price <= last_price or price * ratio >= sum(int(self.items[k]["price"]) * n for k, n in inputs.items()):
                    raise SystemExit(f"recipe_tiers: the {pid} tier {rank} is not worth more than the one below (or makes coins)")
                last_price = price
                new_id = self._new_id(base, rank)
                self.tier_items[new_id] = {"name_key": f"item.{new_id}", "code": int(line["code"]) + rank // step,
                                           "emoji": emoji, "kind": "material", "keep": True, "price": price}
                self.tier_recipes[new_id] = {"profession": pid, "inputs": inputs, "output": {new_id: 1}, "min_rank": rank,
                                             "energy": energy, "xp": xp}
                self.tier_names[new_id] = (f"{noun[0]} {TIER_PLACE_ES[rank]}", f"{TIER_PLACE_EN[rank]} {noun[1]}")
                self.uses[new_id] = (f"{pemoji} refinado del tramo {rank} de {pname[0]}: vale más que el del tramo anterior; "
                                     f"se vende al 🛒 Mercader y en el 🏛️ Mercado",
                                     f"{pemoji} {pname[1]} refined good of tier {rank}: worth more than the tier below; "
                                     f"sold to the 🛒 Merchant and on the 🏛️ Market")

    # ------------------------------------------------------------------ D-328 (0.52): potions, remedies and dishes

    def _anchor(self, rid: str) -> dict[str, Any]:
        """An anchor recipe as the interpolation needs it: rank, inputs per make, units per make and its item's effect."""
        rdef = self.profs["recipes"][rid]
        out_id, out_n = next(iter(rdef["output"].items()))
        item = self.items[out_id]
        return {"rank": int(rdef.get("min_rank", 1)), "inputs": dict(rdef["inputs"]), "output": int(out_n), "item": out_id,
                "heal": float(item.get("heal", 0.0)), "toxicity": float(item.get("toxicity", 0)),
                "food": float(item.get("food", 0)), "price": float(item.get("price", 1))}

    def _compute_consumables(self) -> None:
        """One recipe per tier that has none in ⚗️ 🩺 🍲, along its line (balance.yaml recipe_tiers.consumables).

        [ES] Qué hace: cada oficio tiene "líneas": cada una empieza en una receta ancla escrita a mano (la 🧪 poción de vida,
        la 🍷 mayor, el 🫙 ungüento…) y termina en su "to" (un punto escrito en balance.yaml: rango, unidades por vez,
        materiales, cuánto cura y precio) o, sin "to", justo antes del ancla de la línea siguiente. Para cada tramo (5, 10 …
        100) que no tiene ya su ancla, arma una receta y su objeto a mitad de camino (según el rango) entre las dos puntas:
        materiales por vez (los de la punta más cercana), unidades por vez, cuánto cura o cuántas raciones da y su precio. La
        toxicidad es la de su ancla (la misma en toda la línea: no cambia qué pociones se pueden juntar en una pelea) y el
        objeto nuevo va en el cinturón con el lugar (belt_slot) de su ancla: el cinturón no crece.
        """
        groups = self.cfg.get("consumables") or {}
        remedy_ratio = float(self.balance["shop"].get("remedy_sell_ratio", self.balance["shop"]["sell_ratio"]))
        ratio = float(self.balance["shop"]["sell_ratio"])
        step = int(self.cfg["step"])
        all_recipes = dict(self.profs["recipes"]) | self.tier_recipes
        for pid, group in groups.items():
            lines = group["lines"]
            starts = [self._anchor(line["anchor"]) for line in lines]
            covered = {start["rank"] for start in starts}
            last_effect = 0.0
            for n, (line, start) in enumerate(zip(lines, starts)):
                if line.get("to"):
                    raw_end = dict(line["to"])
                    end = {"inputs": dict(raw_end["inputs"]), "output": int(raw_end.get("output", 1)), "rank": int(raw_end["rank"]),
                           "heal": float(raw_end.get("heal", 0.0)), "food": float(raw_end.get("food", 0)),
                           "price": float(raw_end.get("price", raw_end.get("food", 1)))}
                    last_rank = end["rank"]
                elif n + 1 < len(starts):
                    end, last_rank = starts[n + 1], starts[n + 1]["rank"] - step
                elif start["rank"] >= self._tiers()[-1]:                     # [ES] el ancla del 100 (🍽️ banquete) no tiene tramos después
                    continue
                else:
                    raise SystemExit(f"recipe_tiers: the last {pid} line needs a 'to'")
                last_effect = max(last_effect, start["heal"] or start["food"])
                base = start["item"]
                kind = self.items[base]["kind"]
                for rank in range(start["rank"] - start["rank"] % step + step, last_rank + 1, step):
                    covered.add(rank)
                    t = (rank - start["rank"]) / (end["rank"] - start["rank"])
                    out_n = max(1, _half_up(start["output"] + (end["output"] - start["output"]) * t))
                    # [ES] los materiales de la punta más cercana (el ancla hasta la mitad del camino, el final desde ahí),
                    # cada uno con su cantidad a mitad de camino entre las dos puntas (al menos 1); la carne y el pescado (lo
                    # que es comida) van siempre a mitad de camino entre las dos, así un plato nunca rinde de más
                    near = (start if t < 0.5 else end)["inputs"]
                    food_keys = [k for k in list(end["inputs"]) + list(start["inputs"]) if self.items[k].get("food")]
                    inputs: dict[str, int] = {}
                    for key in list(dict.fromkeys(list(near) + food_keys)):
                        lo, hi = float(start["inputs"].get(key, 0)), float(end["inputs"].get(key, 0))
                        n_in = _half_up(lo + (hi - lo) * t)
                        if key in near or n_in > 0:
                            inputs[key] = max(1, n_in)
                    price = start["price"] + (end["price"] - start["price"]) * t       # [ES] precio por unidad, como el de sus puntas
                    item: dict[str, Any] = {"name_key": "", "code": int(group["code"]) + rank // step,
                                            "emoji": self.items[base]["emoji"], "kind": kind}
                    if kind == "food":
                        food = _half_up(start["food"] + (end["food"] - start["food"]) * t)
                        item |= {"cooked": True, "food": food, "price": food}
                        effect = float(food)
                        raw_food = sum(int(self.items[k].get("food", 0)) * c for k, c in inputs.items())
                        if not food * out_n > raw_food > 0:
                            raise SystemExit(f"recipe_tiers: the {pid} dish of tier {rank} is not worth more than its raw food")
                        sell = ratio
                    else:
                        heal = round(start["heal"] + (end["heal"] - start["heal"]) * t, 2)
                        item |= {"heal": heal, "toxicity": int(start["toxicity"]), "belt": True, "belt_slot": base,
                                 "price": max(1, _half_up(price))}
                        effect = heal
                        sell = remedy_ratio
                    if effect <= last_effect:
                        raise SystemExit(f"recipe_tiers: the {pid} tier {rank} does not do more than the tier below")
                    last_effect = effect
                    cost = sum(int(self.items[k]["price"]) * c for k, c in inputs.items()) / out_n
                    if item["price"] * sell >= cost:
                        raise SystemExit(f"recipe_tiers: the {pid} tier {rank} makes coins at the merchant (D-113)")
                    new_id = self._new_id(base, rank)
                    item["name_key"] = f"item.{new_id}"
                    energy, xp = self._tier_energy_xp(rank)
                    rdef = {"profession": pid, "inputs": inputs, "output": {new_id: out_n}, "min_rank": rank,
                            "energy": energy, "xp": xp}
                    if len(branches_of(rdef, self.profs["professions"], all_recipes)) < 2:
                        raise SystemExit(f"recipe_tiers: the {pid} recipe of tier {rank} needs 2 professions or more (D-109)")
                    self.tier_items[new_id] = item
                    self.tier_recipes[new_id] = rdef
                    noun = self._noun(base)
                    self.tier_names[new_id] = (f"{noun[0]} {TIER_PLACE_ES[rank]}", f"{TIER_PLACE_EN[rank]} {noun[1]}")
                    self.uses[new_id] = self._use_texts(item, rank)
            missing = [rank for rank in self._tiers() if rank not in covered]
            if missing:
                raise SystemExit(f"recipe_tiers: {pid} has no recipe at the tiers {missing}")

    @staticmethod
    def _use_texts(item: dict[str, Any], rank: int) -> tuple[str, str]:
        """What a new potion, remedy or dish does, in Spanish and English (resources.use.<id>, shown by its code)."""
        if item["kind"] == "food":
            return (f"🍲 comida: {item['food']} raciones en la despensa de tu campamento (tramo {rank})",
                    f"🍲 food: {item['food']} rations in your camp's pantry (tier {rank})")
        pct = round(item["heal"] * 100)
        if item["toxicity"]:
            return (f"{item['emoji']} cura {pct} % de tu vida · ☠️ {item['toxicity']} de toxicidad (tramo {rank}); va en el cinturón",
                    f"{item['emoji']} heals {pct}% of your health · ☠️ {item['toxicity']} toxicity (tier {rank}); it goes on the belt")
        return (f"{item['emoji']} cura {pct} % de tu vida, sin toxicidad (tramo {rank}); va en el cinturón",
                f"{item['emoji']} heals {pct}% of your health, no toxicity (tier {rank}); it goes on the belt")

    # ------------------------------------------------------------------ writing

    def professions_text(self) -> str:
        text = _strip_generated(self.prof_text)
        text = _edit_recipes(text, self.updates)
        block = [
            "",
            f"  {BEGIN} (D-306, 0.44; D-328, 0.52). Do not edit by hand: change the tool or balance.yaml recipe_tiers and run it again.",
            "  # [ES] Los tramos nuevos de los oficios de equipo (E-221): una receta por línea en los niveles 15, 25 … 95, desde",
            "  # [ES] el rango igual al nivel; materiales a mitad de camino entre sus dos vecinas; energía y experiencia por tramo.",
        ]
        block += [f"  {rid}: {_flow(rdef)}" for rid, rdef in self.new_recipes.items()]
        block += [
            "  # [ES] D-328 (0.52): un tramo cada 5 en el refinado (un refinado mejor por tramo: su refinado de siempre, su crudo y",
            "  # [ES] un catalizador; balance.yaml recipe_tiers.refine) y en ⚗️ 🩺 🍲 (a mitad de camino entre sus recetas ancla,",
            "  # [ES] recipe_tiers.consumables). Energía y experiencia como una pieza de equipo del mismo tramo.",
        ]
        block += [f"  {rid}: {_flow(rdef)}" for rid, rdef in self.tier_recipes.items()]
        block.append(f"  {END}")
        return text.rstrip("\n") + "\n" + "\n".join(block) + "\n"

    def items_text_out(self) -> str:
        text = _strip_generated(self.items_text)
        block = [
            "",
            f"{BEGIN} (D-306, 0.44; D-328, 0.52). Do not edit by hand: change the tool and run it again.",
            "# [ES] Equipo de artesano de los tramos nuevos (E-221): niveles 15, 25 … 95 de cada línea, 🟣 épico, con bonos y",
            "# [ES] precio a mitad de camino entre las piezas de su línea de 5 niveles menos y 5 más. Solo de una receta.",
        ]
        block += [f"{iid}: {_flow(item)}" for iid, item in self.new_items.items()]
        block += [
            "# [ES] D-328 (0.52): los refinados de cada tramo (valen sus materiales más su ⚡) y las pociones, remedios y platos de",
            "# [ES] cada tramo (curan más y dan más raciones que los del tramo anterior). Código = code de su línea en balance.yaml",
            "# [ES] + rango ÷ 5 (estable). belt_slot: el lugar del cinturón que comparten con su receta ancla (no lo agrandan).",
        ]
        block += [f"{iid}: {_flow(item)}" for iid, item in self.tier_items.items()]
        block.append(END)
        return text.rstrip("\n") + "\n" + "\n".join(block) + "\n"

    def locale_text(self, lang: str) -> str:
        if lang == "es":
            head = ["# Generated by tools/recipe_tiers.py (D-306, 0.44; D-328, 0.52): the names of the crafted pieces of the new tiers",
                    "# and of the refined goods, potions, remedies and dishes of every tier.",
                    "# [ES] Generado por tools/recipe_tiers.py: los nombres de las piezas de artesano de los tramos nuevos",
                    "# (niveles 15, 25 … 95) y, desde la 0.52, de los refinados, pociones, remedios y platos de cada tramo con lo que",
                    "# hace cada uno (resources.use). No se edita a mano: se cambia PLACE_ES / TIER_PLACE_ES en la herramienta y se",
                    "# vuelve a correr. Se junta con es.yaml y los demás es_*.yaml al cargar (engine/core/content.py). Su par inglés:",
                    "# en_tramos.yaml."]
        else:
            head = ["# Generated by tools/recipe_tiers.py (D-306, 0.44; D-328, 0.52): the names of the crafted pieces of the new tiers",
                    "# (levels 15, 25 … 95) and of the refined goods, potions, remedies and dishes of every tier, with what each one",
                    "# does (resources.use). Do not edit by hand: change PLACE_EN / TIER_PLACE_EN in the tool and run it again.",
                    "# [ES] Par inglés de es_tramos.yaml (generado)."]
        index = 0 if lang == "es" else 1
        body = ["item:"] + [f"  {iid}: {_quote(names[index])}" for iid, names in self.names.items()]
        body += [f"  {iid}: {_quote(names[index])}" for iid, names in self.tier_names.items()]
        body += ["", "resources:", "  use:"] + [f"    {iid}: {_quote(texts[index])}" for iid, texts in self.uses.items()]
        return "\n".join(head + [""] + body) + "\n"


def _edit_recipes(text: str, updates: dict[str, dict[str, Any]]) -> str:
    """Set min_rank, energy, xp and retired of the given recipes in professions.yaml, keeping every comment."""
    out: list[str] = []
    lines = text.split("\n")
    in_recipes = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.match(r"^recipes:\s*(#.*)?$", line):
            in_recipes = True
        elif re.match(r"^[a-z_]+:", line):
            in_recipes = False
        flow = re.match(r"^  (\w+): (\{.*\})(\s*#.*)?$", line) if in_recipes else None
        block = re.match(r"^  (\w+):\s*(#.*)?$", line) if in_recipes else None
        if flow and flow.group(1) in updates:
            change = updates[flow.group(1)]
            body = flow.group(2)
            for key in ("min_rank", "energy", "xp"):
                if key in change:
                    body = re.sub(rf"(?<![\w]){key}: \d+", f"{key}: {change[key]}", body)
            if change.get("retired") and "retired:" not in body:
                body = body[:-1] + ", retired: true}"
            out.append(f"  {flow.group(1)}: {body}{flow.group(3) or ''}")
            i += 1
            continue
        if block and block.group(1) in updates:
            change = updates[block.group(1)]
            out.append(line)
            i += 1
            fields: list[str] = []
            while i < len(lines) and lines[i].startswith("    "):
                fields.append(lines[i])
                i += 1
            for n, field in enumerate(fields):
                for key in ("min_rank", "energy", "xp"):
                    if key in change:
                        fields[n] = re.sub(rf"^(    {key}: )\d+", rf"\g<1>{change[key]}", fields[n])
            if change.get("retired") and not any(f.startswith("    retired:") for f in fields):
                fields.append("    retired: true")
            out += fields
            continue
        out.append(line)
        i += 1
    return "\n".join(out)


def main(argv: list[str]) -> int:
    check = "--check" in argv
    tiers = Tiers()
    files = {
        CONTENT / "professions.yaml": tiers.professions_text(),
        CONTENT / "items.yaml": tiers.items_text_out(),
        CONTENT / "locales" / "es_tramos.yaml": tiers.locale_text("es"),
        CONTENT / "locales" / "en_tramos.yaml": tiers.locale_text("en"),
    }
    stale = [path for path, text in files.items() if not path.exists() or path.read_text(encoding="utf-8") != text]
    if check:
        for path in stale:
            print(f"recipe_tiers: {path.relative_to(ROOT)} is not up to date: run python tools/recipe_tiers.py")
        return 1 if stale else 0
    for path in stale:
        path.write_text(files[path], encoding="utf-8")
        print(f"recipe_tiers: wrote {path.relative_to(ROOT)}")
    print(f"recipe_tiers: {len(tiers.new_items)} new pieces, {len(tiers.new_recipes)} new recipes, "
          f"{sum(1 for c in tiers.updates.values() if c.get('retired'))} mail recipes retired, "
          f"{len(tiers.updates)} recipes updated; D-328: {len(tiers.tier_recipes)} refining, potion, remedy and dish "
          f"recipes ({sum(1 for i in tiers.tier_items.values() if i['kind'] == 'material')} refined goods)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
