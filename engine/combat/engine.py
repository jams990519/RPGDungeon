"""Round resolution for a solo fight against one enemy (version 0.1).

Order of a round (ronda-y-acciones.md §6):
  1. Responses (block, dodge, shield) and belt items.
  2. Everything else by initiative: the hero's action and the enemy's announced move.
     Acting before the enemy lets an interrupt cancel an interruptible move.
  3. Flee, at the end.
The enemy's next move is chosen at the end of each round and shown as the
warning (aviso) of the next one.

[ES]
Para qué sirve: aplicar las reglas de una ronda y escribir el resumen.
Documento de diseño: diseno/04-combate/ronda-y-acciones.md §1-§6 y §10; avisos-y-tacticas.md
Módulo: M5 Combate
Depende de: engine.core (Rng, Texts), engine.hero.hero_stats, contenido (clases, enemigos, objetos, balance)
Lo usan: engine/service/game.py
Eventos que publica: ninguno (devuelve el resultado; el servicio publica)
Eventos que escucha: ninguno
Datos de los que es dueño: el estado de combate (dict) que el servicio guarda en "combat"
Reglas que nunca se rompen:
    1. validate_choice se llama antes de resolve_round: una elección inválida no gasta la ronda.
    2. Una respuesta cuesta Aguante; el Aguante solo vuelve en rondas sin respuesta (ronda §3 y §5).
    3. La Toxicidad al máximo impide beber pociones (ronda §4).
Si cambias esto, revisa:
    - Servicio: engine/service/game.py (vista de combate, recompensas)
    - Números: balance.yaml combat.*
    - Pruebas: tests/test_combat.py
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


def choose_next_move(enemy_def: dict[str, Any], rng: Rng) -> str:
    """Pick the enemy's next move by weight. [ES] Qué hace: elige el próximo ataque (el que se avisa). La llaman: el combate. Si cambia, afecta: la frecuencia de cada ataque."""
    moves = enemy_def["moves"]
    return rng.pick_weighted([m["id"] for m in moves], [m.get("weight", 1) for m in moves])


def _move(enemy_def: dict[str, Any], move_id: str) -> dict[str, Any]:
    for move in enemy_def["moves"]:
        if move["id"] == move_id:
            return move
    return enemy_def["moves"][0]


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
    move = _move(enemy_def, enemy["next_move"])
    move_name = t.t(f"enemy.{enemy['id']}.moves.{move['id']}.name")

    def name_of(a: dict[str, Any]) -> str:
        return t.t(f"ability.{a['id']}.name")

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
        healed = min(stats["max_hp"] - hero.hp, round(stats["max_hp"] * item.get("heal", 0.0)))
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
            dmg, crit = _roll_damage(stats["attack"], spec.get("power", 1.0), enemy["armor"], rng, bal)
            enemy["hp"] -= dmg
            hs["resource"] = min(class_def["resource_max"], hs["resource"] + spec.get("gain", 0))
            hs["combo"] = min(5, hs["combo"] + spec.get("combo", 0))
            lines.append(t.t("combat.hit_enemy", action=t.t(f"class.{hero.class_id}.attack_name"), dmg=dmg, crit=t.t("combat.crit") if crit else ""))
        elif ability and ability["kind"] != "response":
            hs["resource"] -= ability.get("cost", 0)
            if ability.get("cooldown"):
                hs["cooldowns"][ability["id"]] = ability["cooldown"] + 1
            akind = ability["kind"]
            if akind in ("strike", "interrupt", "finisher"):
                power = ability.get("power", 1.0)
                if akind == "finisher":
                    power += ability.get("per_combo", 0.0) * hs["combo"]
                    hs["combo"] = 0
                dmg, crit = _roll_damage(stats["attack"], power, enemy["armor"], rng, bal)
                enemy["hp"] -= dmg
                lines.append(t.t("combat.hit_enemy", action=name_of(ability), dmg=dmg, crit=t.t("combat.crit") if crit else ""))
                if akind == "interrupt":
                    if not hero_first:
                        lines.append(t.t("combat.interrupt_late", move=move_name))
                    elif "interruptible" in move.get("tags", []):
                        interrupted = True
                        lines.append(t.t("combat.interrupted", move=move_name))
                    else:
                        lines.append(t.t("combat.not_interruptible", move=move_name))
            elif akind == "heal":
                healed = min(stats["max_hp"] - hero.hp, round(stats["max_hp"] * ability.get("value", 0.0)))
                hero.hp += healed
                lines.append(t.t("combat.heal", action=name_of(ability), amount=healed))
            elif akind == "dot":
                enemy["dot"] = {"power": ability.get("power", 0.5), "rounds": ability.get("rounds", 3)}
                lines.append(t.t("combat.dot_applied", action=name_of(ability), rounds=ability.get("rounds", 3)))

    def enemy_acts() -> None:
        if enemy["hp"] <= 0 or interrupted:
            return
        if move.get("kind") == "channel":
            enemy["buff"] = move.get("buff", 1.5)
            lines.append(t.t("combat.channel", enemy=enemy_name, move=move_name))
            return
        dmg, crit = _roll_damage(enemy["attack"], move.get("power", 1.0) * enemy["buff"], stats["armor"], rng, bal)
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
        dmg = max(1, round(stats["attack"] * enemy["dot"]["power"]))
        enemy["hp"] -= dmg
        enemy["dot"]["rounds"] -= 1
        lines.append(t.t("combat.dot_tick", enemy=enemy_name, dmg=dmg))
        if enemy["dot"]["rounds"] <= 0:
            enemy["dot"] = None

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
    for key in list(hs["cooldowns"]):
        hs["cooldowns"][key] -= 1
        if hs["cooldowns"][key] <= 0:
            del hs["cooldowns"][key]
    if state["outcome"] is None:
        enemy["next_move"] = choose_next_move(enemy_def, rng)
        state["round"] += 1
    state["draws"] = rng.draws
    state["log"] = lines
    return lines
