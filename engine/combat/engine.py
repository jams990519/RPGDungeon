"""Round resolution for a solo fight against one enemy (version 0.1).

Order of a round (ronda-y-acciones.md §6):
  1. Responses (block, dodge, shield) and belt items.
  2. Everything else by initiative: the hero's action and the enemy's announced move.
     Acting before the enemy lets an interrupt cancel an interruptible move.
  3. Flee, at the end.
The enemy's next move is chosen at the end of each round and shown as the
warning (aviso) of the next one.

Bosses (D-82) may have "phases" in enemies.yaml: when their life drops to a
phase's threshold ("at", a fraction of max life), at the end of that round they
switch to the phase's move list and multiply their base attack ("attack_mult").
The move already announced still lands; only the next warning changes.

[ES]
Para qué sirve: aplicar las reglas de una ronda y escribir el resumen.
Documento de diseño: diseno/04-combate/ronda-y-acciones.md §1-§6 y §10; avisos-y-tacticas.md;
    diseno/06-contenido/jefes.md §2 regla 4 y §5 (fases de jefe, D-82)
Módulo: M5 Combate (y las fases de jefe de M6)
Depende de: engine.core (Rng, Texts), engine.hero.hero_stats, contenido (clases, enemigos, objetos, balance)
Lo usan: engine/service/game.py
Eventos que publica: ninguno (devuelve el resultado; el servicio publica)
Eventos que escucha: ninguno
Datos de los que es dueño: el estado de combate (dict) que el servicio guarda en "combat"
Reglas que nunca se rompen:
    1. validate_choice se llama antes de resolve_round: una elección inválida no gasta la ronda.
    2. Una respuesta cuesta Aguante; el Aguante solo vuelve en rondas sin respuesta (ronda §3 y §5).
    3. La Toxicidad al máximo impide beber pociones (ronda §4).
    4. Un jefe cambia de fase solo al final de la ronda: el golpe ya avisado se cumple tal cual (D-82).
    5. Las fases solo avanzan, nunca vuelven atrás, aunque el jefe se cure.
    6. Una habilidad que no es respuesta puede dar recurso (gain) y combos (combo, solo las que golpean);
       los combos nunca pasan de 5 (D-79).
Si cambias esto, revisa:
    - Servicio: engine/service/game.py (vista de combate, recompensas, Guardián)
    - Números: balance.yaml combat.*; enemies.yaml phases (at, attack_mult, moves)
    - Pruebas: tests/test_combat.py, tests/test_boss.py
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engine.core.i18n import Texts
from engine.core.rng import Rng
from engine.hero.hero import Hero, hero_stats


@dataclass
class CombatContext:
    """Everything a round needs besides the state.

    [ES]
    Qué es: el contenido y los textos que usa el combate.
    Quién la usa: el servicio la arma y la pasa a cada ronda.
    Si cambia, afecta: todas las funciones de combate.
    """

    classes: dict[str, Any]
    enemies: dict[str, Any]
    items: dict[str, Any]
    balance: dict[str, Any]
    texts: Texts


def make_combat(enemy_id: str, enemy_def: dict[str, Any], level: int, class_def: dict[str, Any], seed: int) -> dict[str, Any]:
    """Create the saved state of a new fight.

    [ES]
    Qué hace: arma el estado inicial de una pelea, con el primer aviso ya elegido.
    La llaman: el servicio cuando aparece un enemigo.
    Si cambia, afecta: las peleas nuevas (las guardadas siguen con su estado).
    """
    base, per = enemy_def["base"], enemy_def.get("per_level", {})
    lv = max(1, level) - 1
    max_hp = int(base["hp"] + per.get("hp", 0) * lv)
    state: dict[str, Any] = {
        "seed": seed,
        "draws": 0,
        "round": 1,
        "enemy": {
            "id": enemy_id,
            "level": level,
            "hp": max_hp,
            "max_hp": max_hp,
            "attack": float(base["attack"] + per.get("attack", 0) * lv),
            "armor": float(base.get("armor", 0.0)),
            "initiative": float(base.get("initiative", 10)),
            "next_move": None,
            "buff": 1.0,
            "dot": None,
            "can_flee": bool(enemy_def.get("can_flee", True)),
            "phase": 0,
            "base_attack": float(base["attack"] + per.get("attack", 0) * lv),
        },
        "hero": {
            "resource": int(class_def.get("resource_start", 0)),
            "stamina": None,
            "cooldowns": {},
            "combo": 0,
            "toxicity": 0,
        },
        "log": [],
        "outcome": None,
    }
    rng = Rng(seed)
    state["enemy"]["next_move"] = choose_next_move(enemy_def, rng)
    state["draws"] = rng.draws
    return state


def phase_moves(enemy_def: dict[str, Any], phase: int = 0) -> list[dict[str, Any]]:
    """The move list in use at a phase (0 = no phase yet). A phase without "moves" keeps the previous list.

    [ES]
    Qué hace: da la lista de golpes que usa el enemigo en esa fase (0 = la normal).
    La llaman: choose_next_move, el servicio y el simulador.
    Si cambia, afecta: qué golpes avisa un jefe en cada fase.
    """
    phases = enemy_def.get("phases") or []
    for index in range(min(phase, len(phases)), 0, -1):
        if phases[index - 1].get("moves"):
            return phases[index - 1]["moves"]
    return enemy_def["moves"]


def choose_next_move(enemy_def: dict[str, Any], rng: Rng, phase: int = 0) -> str:
    """Pick the enemy's next move by weight, from the current phase's list.

    [ES]
    Qué hace: elige el próximo ataque (el que se avisa) entre los de la fase actual.
    La llaman: el combate (y el simulador).
    Si cambia, afecta: la frecuencia de cada ataque.
    """
    moves = phase_moves(enemy_def, phase)
    return rng.pick_weighted([m["id"] for m in moves], [m.get("weight", 1) for m in moves])


def find_move(enemy_def: dict[str, Any], move_id: str) -> dict[str, Any]:
    """A move by id, searched in the base list and in every phase (falls back to the first move).

    [ES]
    Qué hace: busca un golpe por su id en todas las fases (un golpe avisado antes del cambio de fase sigue valiendo).
    La llaman: resolve_round y el simulador.
    Si cambia, afecta: qué golpe se resuelve cada ronda.
    """
    for move in list(enemy_def["moves"]) + [m for p in enemy_def.get("phases") or [] for m in p.get("moves") or []]:
        if move["id"] == move_id:
            return move
    return enemy_def["moves"][0]


def phase_for(enemy_def: dict[str, Any], hp: float, max_hp: float) -> int:
    """How many phase thresholds this life fraction has crossed (0 = none). [ES] Qué hace: dice en qué fase debería estar un jefe según su vida. La llaman: el combate y las pruebas. Si cambia, afecta: cuándo cambia de fase."""
    frac = hp / max_hp if max_hp else 0.0
    return sum(1 for p in enemy_def.get("phases") or [] if frac <= p["at"])


def _update_phase(state: dict[str, Any], enemy_def: dict[str, Any], ctx: "CombatContext", lines: list[str]) -> None:
    """End of round: move a boss to a later phase if its life crossed a threshold; apply its rage."""
    enemy = state["enemy"]
    new = phase_for(enemy_def, enemy["hp"], enemy["max_hp"])
    if new <= enemy.get("phase", 0):
        return
    enemy["phase"] = new
    phase = enemy_def["phases"][new - 1]
    enemy["attack"] = enemy.get("base_attack", enemy["attack"]) * phase.get("attack_mult", 1.0)
    if "armor" in phase:
        enemy["armor"] = float(phase["armor"])
    lines.append(ctx.texts.t(f"enemy.{enemy['id']}.phases.{phase['id']}"))
    lines.append(ctx.texts.t("combat.phase_change", n=new + 1, total=len(enemy_def["phases"]) + 1))


def validate_choice(state: dict[str, Any], hero: Hero, class_def: dict[str, Any], choice: dict[str, Any], ctx: CombatContext) -> str | None:
    """Return a translated reason if the choice cannot be used now, else None.

    Args:
        choice: {"type": "attack"} | {"type": "ability", "index": 0-2} | {"type": "flee"}
            | {"type": "dodge"} | {"type": "item", "item_id": str}.

    [ES]
    Qué hace: revisa costo, enfriamiento, Aguante, Toxicidad y objetos antes de jugar.
    La llaman: el servicio antes de resolver la ronda.
    Si cambia, afecta: qué botones funcionan en cada momento.
    """
    t = ctx.texts
    hs = state["hero"]
    stamina_max = ctx.balance["combat"]["stamina_max"]
    stamina = stamina_max if hs["stamina"] is None else hs["stamina"]
    kind = choice.get("type")
    if kind == "ability":
        index = choice.get("index", -1)
        abilities = class_def["abilities"]
        if not 0 <= index < len(abilities):
            return t.t("combat.err.unknown")
        ability = abilities[index]
        name = t.t(f"ability.{ability['id']}.name")
        if hs["cooldowns"].get(ability["id"], 0) > 0:
            return t.t("combat.err.cooldown", action=name, n=hs["cooldowns"][ability["id"]])
        if ability.get("cost", 0) > hs["resource"]:
            return t.t("combat.err.cost", resource=t.t(f"resource.{class_def['resource']}"))
        if ability["kind"] == "response" and stamina < ability.get("stamina", 1):
            return t.t("combat.err.stamina")
        if ability["kind"] == "finisher" and hs["combo"] <= 0:
            return t.t("combat.err.combo")
    elif kind == "dodge":
        if stamina < 1:
            return t.t("combat.err.stamina")
    elif kind == "flee":
        if not state["enemy"]["can_flee"]:
            return t.t("combat.err.no_flee")
    elif kind == "item":
        item_id = choice.get("item_id", "")
        if hero.belt.get(item_id, 0) <= 0 or item_id not in ctx.items:
            return t.t("combat.err.item")
        item = ctx.items[item_id]
        if item.get("toxicity", 0) and hs["toxicity"] + item["toxicity"] > ctx.balance["combat"]["toxicity_max"]:
            return t.t("combat.err.toxicity")
    elif kind != "attack":
        return t.t("combat.err.unknown")
    return None


def _roll_damage(attack: float, power: float, armor: float, rng: Rng, balance: dict[str, Any]) -> tuple[int, bool]:
    combat = balance["combat"]
    low, high = combat["damage_spread"]
    amount = attack * power * rng.uniform(low, high)
    crit = rng.chance(combat["crit_chance"])
    if crit:
        amount *= combat["crit_mult"]
    return max(1, round(amount * (1 - armor))), crit


def resolve_round(state: dict[str, Any], hero: Hero, class_def: dict[str, Any], choice: dict[str, Any], ctx: CombatContext) -> list[str]:
    """Resolve one round. Mutates state, hero.hp and hero.belt. Returns summary lines.

    [ES]
    Qué hace: juega la ronda completa (respuestas y objetos, acciones por iniciativa,
    huida) y deja elegido el próximo aviso del enemigo.
    La llaman: el servicio, después de validate_choice.
    Si cambia, afecta: todo el combate.
    """
    t = ctx.texts
    bal = ctx.balance
    rng = Rng(state["seed"], state["draws"])
    enemy = state["enemy"]
    enemy_def = ctx.enemies[enemy["id"]]
    enemy_name = t.t(enemy_def["name_key"])
    hs = state["hero"]
    stats = hero_stats(class_def, hero.level)
    stamina_max = bal["combat"]["stamina_max"]
    if hs["stamina"] is None:
        hs["stamina"] = stamina_max
    lines: list[str] = []
    kind = choice["type"]
    ability = class_def["abilities"][choice["index"]] if kind == "ability" else None
    used_response = False
    response: dict[str, Any] | None = None
    move = find_move(enemy_def, enemy["next_move"])
    move_name = t.t(f"enemy.{enemy['id']}.moves.{move['id']}.name")

    def name_of(a: dict[str, Any]) -> str:
        return t.t(f"ability.{a['id']}.name")

    def hero_mult() -> float:
        mult = 1.0
        if hs.get("empower"):
            mult *= 1 + hs["empower"]["value"]
        if enemy.get("exposed"):
            mult *= 1 + enemy["exposed"]["value"]
        return mult

    # Step 1: responses and items go first.
    if ability and ability["kind"] == "response":
        used_response = True
        hs["stamina"] -= ability.get("stamina", 1)
        hs["resource"] = min(class_def["resource_max"], hs["resource"] + ability.get("gain", 0))
        response = {"type": ability["response"], "value": ability.get("value", 0.0), "name": name_of(ability)}
        if ability["response"] == "shield":
            response["left"] = round(stats["max_hp"] * ability.get("value", 0.0))
    elif kind == "dodge":
        used_response = True
        hs["stamina"] -= 1
        response = {"type": "basic_dodge", "value": bal["combat"]["dodge_basic"], "name": t.t("combat.dodge_name")}
    elif kind == "item":
        item_id = choice["item_id"]
        item = ctx.items[item_id]
        hero.belt[item_id] -= 1
        if hero.belt[item_id] <= 0:
            del hero.belt[item_id]
        boost = class_def.get("item_bonus", {}).get(item.get("kind"), 0.0)      # D-111: Alquimia (potions), Medicina (bandages)
        healed = min(stats["max_hp"] - hero.hp, round(stats["max_hp"] * item.get("heal", 0.0) * (1 + boost)))
        hero.hp += healed
        hs["toxicity"] += item.get("toxicity", 0)
        lines.append(t.t("combat.item_used", item=t.t(item["name_key"]), amount=healed))

    # Step 2: hero action and enemy move, by initiative (tie: the hero, who chose first).
    hero_first = stats["initiative"] >= enemy["initiative"]
    interrupted = False

    def hero_acts() -> None:
        nonlocal interrupted
        if kind == "attack":
            spec = class_def["attack"]
            dmg, crit = _roll_damage(stats["attack"], spec.get("power", 1.0) * hero_mult(), enemy["armor"], rng, bal)
            enemy["hp"] -= dmg
            hs["resource"] = min(class_def["resource_max"], hs["resource"] + spec.get("gain", 0))
            hs["combo"] = min(5, hs["combo"] + spec.get("combo", 0))
            lines.append(t.t("combat.hit_enemy", action=t.t(f"class.{hero.class_id}.attack_name"), dmg=dmg, crit=t.t("combat.crit") if crit else ""))
        elif ability and ability["kind"] != "response":
            hs["resource"] -= ability.get("cost", 0)
            if ability.get("cooldown"):
                hs["cooldowns"][ability["id"]] = ability["cooldown"] + 1
            # Builders (D-79): optional resource gain and combo points on any non-response ability.
            if ability.get("gain"):
                hs["resource"] = min(class_def["resource_max"], hs["resource"] + ability["gain"])
            akind = ability["kind"]
            if akind in ("strike", "interrupt", "finisher"):
                power = ability.get("power", 1.0)
                if akind == "finisher":
                    power += ability.get("per_combo", 0.0) * hs["combo"]
                    hs["combo"] = 0
                dmg, crit = _roll_damage(stats["attack"], power * hero_mult(), enemy["armor"], rng, bal)
                enemy["hp"] -= dmg
                lines.append(t.t("combat.hit_enemy", action=name_of(ability), dmg=dmg, crit=t.t("combat.crit") if crit else ""))
                if ability.get("combo"):
                    hs["combo"] = min(5, hs["combo"] + ability["combo"])
                if ability.get("lifesteal"):
                    healed = min(stats["max_hp"] - hero.hp, round(dmg * ability["lifesteal"]))
                    if healed > 0:
                        hero.hp += healed
                        lines.append(t.t("combat.lifesteal", amount=healed))
                if akind == "interrupt":
                    if not hero_first:
                        lines.append(t.t("combat.interrupt_late", move=move_name))
                    elif "interruptible" in move.get("tags", []):
                        interrupted = True
                        lines.append(t.t("combat.interrupted", move=move_name))
                    else:
                        lines.append(t.t("combat.not_interruptible", move=move_name))
            elif akind == "heal":                       # D-111: 🩺 Medicina heals more for healers (heal_bonus)
                healed = min(stats["max_hp"] - hero.hp, round(stats["max_hp"] * ability.get("value", 0.0) * (1 + class_def.get("heal_bonus", 0.0))))
                hero.hp += healed
                lines.append(t.t("combat.heal", action=name_of(ability), amount=healed))
            elif akind == "dot":
                enemy["dot"] = {"power": ability.get("power", 0.5), "rounds": ability.get("rounds", 3)}
                lines.append(t.t("combat.dot_applied", action=name_of(ability), rounds=ability.get("rounds", 3)))
            elif akind in ("empower", "hot"):
                hs[akind] = {"value": ability.get("value", 0.2), "rounds": ability.get("rounds", 3)}
                lines.append(t.t(f"combat.{akind}_applied", action=name_of(ability), rounds=ability.get("rounds", 3)))
            elif akind in ("expose", "weaken"):
                key = "exposed" if akind == "expose" else "weakened"
                enemy[key] = {"value": ability.get("value", 0.2), "rounds": ability.get("rounds", 3)}
                lines.append(t.t(f"combat.{akind}_applied", action=name_of(ability), rounds=ability.get("rounds", 3)))

    def enemy_acts() -> None:
        if enemy["hp"] <= 0 or interrupted:
            return
        if move.get("kind") == "channel":
            enemy["buff"] = move.get("buff", 1.5)
            lines.append(t.t("combat.channel", enemy=enemy_name, move=move_name))
            return
        weak = 1 - enemy["weakened"]["value"] if enemy.get("weakened") else 1.0
        dmg, crit = _roll_damage(enemy["attack"], move.get("power", 1.0) * enemy["buff"] * weak, stats["armor"], rng, bal)
        enemy["buff"] = 1.0
        tags = move.get("tags", [])
        if response:
            rtype = response["type"]
            if rtype == "dodge":
                if "dodgeable" in tags:
                    lines.append(t.t("combat.dodged", move=move_name))
                    return
                lines.append(t.t("combat.cannot_dodge", move=move_name))
            elif rtype == "basic_dodge":
                dmg = max(1, round(dmg * (1 - response["value"])))
                lines.append(t.t("combat.basic_dodge", move=move_name))
            elif rtype == "block":
                frac = response["value"] if "blockable" in tags else bal["combat"]["partial_block"]
                dmg = max(0, round(dmg * (1 - frac)))
                key = "combat.blocked" if "blockable" in tags else "combat.partial_block"
                lines.append(t.t(key, pct=round(frac * 100)))
            elif rtype == "shield":
                absorbed = min(dmg, response["left"])
                dmg -= absorbed
                lines.append(t.t("combat.shield", amount=absorbed))
        hero.hp = max(0, hero.hp - dmg)
        lines.append(t.t("combat.enemy_hits", enemy=enemy_name, move=move_name, dmg=dmg, crit=t.t("combat.crit") if crit else ""))

    if hero_first:
        hero_acts()
        enemy_acts()
    else:
        enemy_acts()
        if hero.hp > 0:
            hero_acts()

    # Damage over time ticks after the actions.
    if enemy["dot"] and enemy["hp"] > 0:
        dmg = max(1, round(stats["attack"] * enemy["dot"]["power"] * hero_mult()))
        enemy["hp"] -= dmg
        enemy["dot"]["rounds"] -= 1
        lines.append(t.t("combat.dot_tick", enemy=enemy_name, dmg=dmg))
        if enemy["dot"]["rounds"] <= 0:
            enemy["dot"] = None

    if hs.get("hot") and hero.hp > 0:
        healed = min(stats["max_hp"] - hero.hp, round(stats["max_hp"] * hs["hot"]["value"] * (1 + class_def.get("heal_bonus", 0.0))))
        if healed > 0:
            hero.hp += healed
            lines.append(t.t("combat.hot_tick", amount=healed))

    # Outcome checks.
    if enemy["hp"] <= 0:
        enemy["hp"] = 0
        state["outcome"] = "victory"
        lines.append(t.t("combat.victory", enemy=enemy_name))
    elif hero.hp <= 0:
        state["outcome"] = "defeat"
        lines.append(t.t("combat.defeat"))
    elif kind == "flee":
        # Step 3: flee at the end of the round.
        c = bal["combat"]
        chance = c["flee_base"] + (stats["initiative"] - enemy["initiative"]) * c["flee_per_initiative"]
        chance = max(c["flee_min"], min(c["flee_max"], chance))
        if rng.chance(chance):
            state["outcome"] = "fled"
            lines.append(t.t("combat.flee_ok"))
        else:
            lines.append(t.t("combat.flee_fail"))

    # End of round upkeep.
    if not used_response:
        hs["stamina"] = min(stamina_max, hs["stamina"] + 1)
    hs["resource"] = min(class_def["resource_max"], hs["resource"] + class_def.get("resource_regen", 0))
    for holder, key in ((hs, "empower"), (hs, "hot"), (enemy, "exposed"), (enemy, "weakened")):
        if holder.get(key):
            holder[key]["rounds"] -= 1
            if holder[key]["rounds"] <= 0:
                holder[key] = None
    for key in list(hs["cooldowns"]):
        hs["cooldowns"][key] -= 1
        if hs["cooldowns"][key] <= 0:
            del hs["cooldowns"][key]
    if state["outcome"] is None:
        if enemy_def.get("phases"):
            _update_phase(state, enemy_def, ctx, lines)
        enemy["next_move"] = choose_next_move(enemy_def, rng, enemy.get("phase", 0))
        state["round"] += 1
    state["draws"] = rng.draws
    state["log"] = lines
    return lines
