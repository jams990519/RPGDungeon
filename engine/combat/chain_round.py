"""One round of chain combat (0.31): validate a choice and resolve it for a class with system: chain.

Round order (the same as the old system, ronda-y-acciones.md §6): defending and belt items first; then the hero's button
and the enemy's announced move by initiative; damage over time and healing over time; flee at the end; the enemy's next
move is chosen and shown as the next warning. What changes is the hero's side: combat energy instead of a class resource,
the four buttons and the chain (engine/combat/chain.py).

In a solo fight the hero is the only ally: an ability that picks an ally, heals several players or buffs the group lands
on the hero (a chain heal of 30 + 30 + 30 lands whole on you); one that hits several enemies hits the one in front of you.
Threat (agro) only matters in group fights, which do not exist yet: the tank's buttons keep their defense part.

[ES]
Para qué sirve: jugar una ronda con las reglas de la cadena: energía (+2 al empezar el turno, +1 del Básico, sin tope),
marcas, gastador con premio, defenderse o tomar poción por 1 de energía, y el efecto de cada botón (golpe, sangrado o
quemadura, aguante o esquiva del tanque, curación, escudo, potenciar, exponer, debilitar).
Documento de diseño: diseno/04-combate/combate-en-cadena.md (D-225 a D-232)
Módulo: M5 Combate
Depende de: engine.combat.chain (las reglas de la cadena), engine.combat.engine (_roll_damage, find_move, choose_next_move,
    _update_phase), engine.core (Rng, Texts), engine.hero.hero_stats, balance.yaml chain y combat, classes.yaml
Lo usan: engine/combat/engine.py (validate_choice y resolve_round mandan aquí a las clases con system: chain)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno (cambia el estado de combate que le pasan, como el motor viejo)
Reglas que nunca se rompen:
    1. validate_chain se llama antes de resolve_chain: una elección inválida no gasta la ronda ni la energía.
    2. La energía del turno se suma antes de pagar (un gastador de 6 se paga con 4 en la mano).
    3. La Toxicidad al máximo impide beber pociones (igual que antes).
    4. Un jefe cambia de fase solo al final de la ronda (D-82), igual que antes.
Si cambias esto, revisa:
    - Reglas de la cadena: engine/combat/chain.py; números: balance.yaml chain.*; botones: classes.yaml (system: chain)
    - Forma de jugar: engine/combat/auto.py (chain_choice)
    - Pruebas: tests/test_cadena.py, tests/test_clases_031.py
"""

from __future__ import annotations

from typing import Any

from engine.combat import chain
from engine.combat.engine import CombatContext, _roll_damage, _update_phase, choose_next_move, find_move
from engine.core.rng import Rng
from engine.hero.hero import Hero, hero_stats

# Who plays the role's main output: the variety bonus (D-229) grows it.
ROLE_OUTPUT = {"dps": "damage", "sanador": "heal", "tanque": "guard", "soporte": "buff"}


def available_energy(state: dict[str, Any], balance: dict[str, Any]) -> int:
    """Energy the hero can spend this turn: what it holds plus the turn's gain.

    [ES] Qué hace: la energía que se puede gastar este turno (la guardada + chain.energy.per_turn). La llaman: validate_chain,
    la IA y la vista. Si cambia, afecta: qué botones se pueden tocar.
    """
    return int(state["hero"]["resource"]) + int(chain.cfg(balance)["energy"]["per_turn"])


def validate_chain(state: dict[str, Any], hero: Hero, class_def: dict[str, Any], choice: dict[str, Any], ctx: CombatContext) -> str | None:
    """A translated reason if the choice cannot be used now, else None (the chain version of validate_choice).

    [ES] Qué hace: revisa la energía de cada botón (Básico 0, H1 2, H2 3, H3 6; defenderse o una poción 1), los objetos, la
    Toxicidad y si se puede huir. La llama: engine/combat/engine.py validate_choice. Si cambia, afecta: qué botones funcionan.
    """
    t = ctx.texts
    hs = state["hero"]
    chain.ensure_hero(hs, ctx.balance)
    energy = available_energy(state, ctx.balance)
    c = chain.cfg(ctx.balance)
    kind = choice.get("type")
    if kind == "attack":
        return None
    if kind == "ability":
        link = chain.link_of(choice, class_def)
        if link is None:
            return t.t("combat.err.unknown")
        if chain.cost_of(link, ctx.balance) > energy:
            return t.t("chain.err.energy", n=chain.cost_of(link, ctx.balance), have=energy)
        return None
    if kind == "dodge":
        if int(c["energy"]["defend_cost"]) > energy:
            return t.t("chain.err.energy", n=int(c["energy"]["defend_cost"]), have=energy)
        return None
    if kind == "flee":
        return None if state["enemy"]["can_flee"] else t.t("combat.err.no_flee")
    if kind == "item":
        item_id = choice.get("item_id", "")
        if hero.belt.get(item_id, 0) <= 0 or item_id not in ctx.items:
            return t.t("combat.err.item")
        item = ctx.items[item_id]
        if item.get("toxicity", 0) and hs["toxicity"] + item["toxicity"] > ctx.balance["combat"]["toxicity_max"]:
            return t.t("combat.err.toxicity")
        if int(c["energy"]["item_cost"]) > energy:
            return t.t("chain.err.energy", n=int(c["energy"]["item_cost"]), have=energy)
        return None
    return t.t("combat.err.unknown")


def _shapes(hs: dict[str, Any], hero: Hero, balance: dict[str, Any]) -> list[str]:
    """Combo shapes that count for the variety bonus: this fight's, plus the hero's ever if chain.variety.scope is "permanent"."""
    shapes = list(hs.get("combos") or [])
    if chain.cfg(balance)["variety"].get("scope") == "permanent":
        shapes += list(hero.combo_shapes or [])
    return shapes


def resolve_chain(state: dict[str, Any], hero: Hero, class_def: dict[str, Any], choice: dict[str, Any], ctx: CombatContext) -> list[str]:
    """Resolve one round for a chain class. Mutates state, hero.hp, hero.belt (and hero.combo_shapes if permanent).

    [ES]
    Qué hace: juega la ronda completa con las reglas de la cadena y deja elegido el próximo aviso del enemigo.
    La llama: engine/combat/engine.py resolve_round (system: chain), después de validate_choice.
    Si cambia, afecta: todo el combate de las clases nuevas.
    """
    t = ctx.texts
    bal = ctx.balance
    c = chain.cfg(bal)
    rng = Rng(state["seed"], state["draws"])
    enemy = state["enemy"]
    enemy_def = ctx.enemies[enemy["id"]]
    enemy_name = t.t(enemy_def["name_key"])
    hs = state["hero"]
    chain.ensure_hero(hs, bal)
    stats = hero_stats(class_def, hero.level)
    role = chain.role_of(class_def, bal)
    output = ROLE_OUTPUT[role]
    req = chain.required(class_def, bal)
    lines: list[str] = []
    kind = choice["type"]
    link = chain.link_of(choice, class_def)
    move = find_move(enemy_def, enemy["next_move"])
    move_name = t.t(f"enemy.{enemy['id']}.moves.{move['id']}.name")
    variety = chain.variety_bonus(_shapes(hs, hero, bal), bal)
    defend: float | None = None

    hs["resource"] += int(c["energy"]["per_turn"])

    def name_of(ability: dict[str, Any]) -> str:
        return t.t(f"ability.{ability['id']}.name")

    def role_mult(what: str) -> float:
        return 1 + variety if output == what else 1.0

    def hero_mult() -> float:
        mult = role_mult("damage")
        if hs.get("empower"):
            mult *= 1 + hs["empower"]["value"]
        if enemy.get("exposed"):
            mult *= 1 + enemy["exposed"]["value"]
        return mult

    def heal(amount: float) -> int:
        healed = min(stats["max_hp"] - hero.hp, round(amount))
        healed = max(0, healed)
        hero.hp += healed
        return healed

    # Step 1: defending and belt items go first (each is the turn's action and costs energy).
    if kind == "dodge":
        hs["resource"] -= int(c["energy"]["defend_cost"])
        defend = float(bal["combat"]["dodge_basic"])
        lines.append(t.t("chain.defend", pct=round(defend * 100)))
    elif kind == "item":
        hs["resource"] -= int(c["energy"]["item_cost"])
        item_id = choice["item_id"]
        item = ctx.items[item_id]
        hero.belt[item_id] -= 1
        if hero.belt[item_id] <= 0:
            del hero.belt[item_id]
        boost = class_def.get("item_bonus", {}).get(item.get("kind"), 0.0)      # D-111: Alquimia (potions), Medicina (bandages)
        healed = heal(stats["max_hp"] * item.get("heal", 0.0) * (1 + boost))
        hs["toxicity"] += item.get("toxicity", 0)
        lines.append(t.t("combat.item_used", item=t.t(item["name_key"]), amount=healed))

    hero_first = stats["initiative"] >= enemy["initiative"]
    if link and chain.ability_for(link, class_def).get("kind") in ("guard", "shield"):
        hero_first = True                       # stepping in, guarding or shielding covers this turn's hit (like a response)
    interrupted = False

    def apply(ability: dict[str, Any], scale: float, spender: bool) -> None:
        """The button's effect; `scale` is the spender's bonus × no-combo factor (1.0 for the other buttons)."""
        nonlocal interrupted
        akind = ability.get("kind", "strike")
        name = name_of(ability)
        rounds = int(ability.get("rounds", 2))
        if spender and role == "soporte":
            rounds = max(1, round(rounds * scale))                           # support: potency AND duration grow
        if akind == "strike":
            power = float(ability.get("power", 1.0))
            dot = enemy.get("dot")
            if ability.get("per_dot_age") and dot:
                power += float(ability["per_dot_age"]) * int(dot.get("age", 0))
            mult = hero_mult() * scale
            low = ability.get("low_hp")
            if low and enemy["hp"] <= enemy["max_hp"] * float(low["below"]):
                mult *= float(low["mult"])
            if ability.get("vs_mark") and (enemy.get("exposed") or {}).get("mark"):
                mult *= float(ability["vs_mark"])
            school = ability.get("school")
            charged = hs.get("charged")
            if charged and school and charged.get("school") == school:
                mult *= 1 + float(charged["value"])
                hs["charged"] = None
                lines.append(t.t("chain.charged_used", pct=round(float(charged["value"]) * 100)))
            boost = hs.get("next_bonus")
            if boost and school and boost.get("school") == school:
                mult *= 1 + float(boost["value"])
                hs["next_bonus"] = None
            dmg, crit = _roll_damage(stats["attack"], power * mult, enemy["armor"], rng, bal)
            enemy["hp"] -= dmg
            lines.append(t.t("combat.hit_enemy", action=name, dmg=dmg, crit=t.t("combat.crit") if crit else ""))
            if ability.get("consume_dot") and dot:
                extra = max(1, round(stats["attack"] * float(dot["power"]) * int(dot["rounds"]) * hero_mult() * scale))
                enemy["hp"] -= extra
                enemy["dot"] = None
                lines.append(t.t("chain.consume_dot", dmg=extra))
        elif akind == "dot":
            enemy["dot"] = {"power": float(ability.get("power", 0.4)) * scale, "rounds": int(ability.get("rounds", 3)), "age": 0,
                            "school": ability.get("school")}
            lines.append(t.t("chain.dot_applied", action=name, rounds=enemy["dot"]["rounds"]))
        elif akind == "guard":
            value = min(float(c["guard_cap"]), float(ability.get("value", 0.3)) * scale * role_mult("guard"))
            hs["guard"] = {"value": value, "rounds": rounds, "style": ability.get("style", "aguante")}
            lines.append(t.t(f"chain.guard_{hs['guard']['style']}", action=name, pct=round(value * 100), rounds=rounds))
            if ability.get("power"):                                         # the tank's spender also hits (Grito, Rugido)
                dmg, crit = _roll_damage(stats["attack"], float(ability["power"]) * hero_mult() * scale, enemy["armor"], rng, bal)
                enemy["hp"] -= dmg
                lines.append(t.t("combat.hit_enemy", action=name, dmg=dmg, crit=t.t("combat.crit") if crit else ""))
        elif akind == "heal":
            amount = stats["max_hp"] * float(ability.get("value", 0.1)) * (1 + class_def.get("heal_bonus", 0.0))
            if ability.get("chain_free"):
                amount *= role_mult("heal")                                   # D-227: Marea scales with players, not the chain
            else:
                amount *= scale * role_mult("heal")
            if spender and hs.get("heal_boost"):
                amount *= 1 + float(hs["heal_boost"]["value"])
                hs["heal_boost"] = None
                lines.append(t.t("chain.heal_boost_used"))
            healed = heal(amount)
            split = int(ability.get("split", 1))
            if split > 1:
                lines.append(t.t("chain.heal_split", action=name, n=min(split, chain.target_cap(bal)), amount=healed))
            elif ability.get("group"):
                lines.append(t.t("chain.heal_group", action=name, cap=chain.target_cap(bal), amount=healed))
            else:
                lines.append(t.t("combat.heal", action=name, amount=healed))
            if ability.get("hot"):
                hs["hot"] = {"value": float(ability["hot"]["value"]) * role_mult("heal"), "rounds": int(ability["hot"].get("rounds", 1))}
        elif akind == "shield":
            left = round(stats["max_hp"] * float(ability.get("value", 0.15)) * scale * role_mult("heal"))
            hs["shield"] = {"left": left, "rounds": rounds}
            lines.append(t.t("chain.shield_applied", action=name, amount=left, rounds=rounds))
        elif akind in ("empower", "expose", "weaken"):
            value = float(ability.get("value", 0.2)) * scale * role_mult("buff")
            holder, key = (hs, "empower") if akind == "empower" else (enemy, "exposed" if akind == "expose" else "weakened")
            holder[key] = {"value": value, "rounds": rounds, "mark": bool(ability.get("mark"))}
            lines.append(t.t(f"chain.{akind}_applied", action=name, pct=round(value * 100), rounds=rounds))
        elif akind == "debuff":
            parts = []
            for key, field in (("exposed", "expose"), ("weakened", "weaken")):
                if ability.get(field):
                    value = float(ability[field]) * scale * role_mult("buff")
                    enemy[key] = {"value": value, "rounds": rounds, "mark": False}
                    parts.append(round(value * 100))
            lines.append(t.t("chain.debuff_applied", action=name, expose=parts[0] if parts else 0,
                             weaken=parts[1] if len(parts) > 1 else 0, rounds=rounds))
        if akind in ("empower", "expose", "weaken", "debuff") and ability.get("power"):     # the support's spender also hits
            dmg, crit = _roll_damage(stats["attack"], float(ability["power"]) * hero_mult() * scale, enemy["armor"], rng, bal)
            enemy["hp"] -= dmg
            lines.append(t.t("combat.hit_enemy", action=name, dmg=dmg, crit=t.t("combat.crit") if crit else ""))
        # Side effects any button may carry (H2 always leaves something for the next turn, D-228).
        if ability.get("counter_per_dodge") and hs.get("dodges"):                # Rugido salvaje: one counter per dodge stored
            extra = max(1, round(stats["attack"] * float(ability["counter_per_dodge"]) * int(hs["dodges"]) * hero_mult() * scale))
            enemy["hp"] -= extra
            lines.append(t.t("chain.counter", n=hs["dodges"], dmg=extra))
            hs["dodges"] = 0
        if ability.get("charge"):
            hs["charged"] = {"school": ability["charge"]["school"], "value": float(ability["charge"]["value"]), "rounds": 3}
            lines.append(t.t("chain.charged", pct=round(float(ability["charge"]["value"]) * 100)))
        if ability.get("next_bonus"):
            hs["next_bonus"] = {"school": ability["next_bonus"]["school"], "value": float(ability["next_bonus"]["value"]), "rounds": 3}
            lines.append(t.t("chain.next_bonus", pct=round(float(ability["next_bonus"]["value"]) * 100)))
        if ability.get("heal_boost"):
            hs["heal_boost"] = {"value": float(ability["heal_boost"]), "rounds": 3}
            lines.append(t.t("chain.heal_boost", pct=round(float(ability["heal_boost"]) * 100)))
        if ability.get("dodge_marks"):
            hs["vapulear"] = {"rounds": int(ability["dodge_marks"])}
        if ability.get("guard"):
            g = ability["guard"]
            hs["guard"] = {"value": min(float(c["guard_cap"]), float(g["value"]) * role_mult("guard")), "rounds": int(g.get("rounds", 1)),
                           "style": g.get("style", "aguante")}
            lines.append(t.t(f"chain.guard_{hs['guard']['style']}", action=name, pct=round(hs["guard"]["value"] * 100),
                             rounds=hs["guard"]["rounds"]))
        if ability.get("weaken") and akind == "strike":
            enemy["weakened"] = {"value": float(ability["weaken"]) * role_mult("buff"), "rounds": int(ability.get("weaken_rounds", 2)),
                                 "mark": False}
            lines.append(t.t("chain.weaken_applied", action=name, pct=round(float(ability["weaken"]) * 100),
                             rounds=int(ability.get("weaken_rounds", 2))))
        if ability.get("extend"):
            holder, key = (hs, "empower") if ability["extend"] == "empower" else (enemy, "exposed")
            if holder.get(key) and holder[key]["rounds"] < int(c["extend_cap"]):
                holder[key]["rounds"] += 1                                       # never past chain.extend_cap turns left
                lines.append(t.t("chain.extended", rounds=holder[key]["rounds"]))
        if ability.get("interrupt"):
            if enemy.get("buff", 1.0) > 1.0:
                enemy["buff"] = 1.0
                lines.append(t.t("chain.charge_broken", enemy=enemy_name))
            if move.get("kind") == "channel" or "interruptible" in move.get("tags", []):
                if hero_first:
                    interrupted = True
                    lines.append(t.t("combat.interrupted", move=move_name))
                else:
                    lines.append(t.t("combat.interrupt_late", move=move_name))

    def hero_acts() -> None:
        if link is None:
            return
        ability = chain.ability_for(link, class_def)
        hs["resource"] -= chain.cost_of(link, bal)
        if link == "B":
            hs["resource"] += int(c["energy"]["basic_gain"])
        scale = 1.0
        if link == "H3":
            cash = chain.spend(hs["chain"], req, bal)
            scale = (1 + cash["bonus"]) * cash["mult"]
            if cash["valid"]:
                hs.setdefault("combos", []).append(cash["shape"])
                if c["variety"].get("scope") == "permanent" and cash["shape"] not in (hero.combo_shapes or []):
                    hero.combo_shapes = list(hero.combo_shapes or []) + [cash["shape"]]
                lines.append(t.t("chain.cashed", n=cash["marks"], pct=round(cash["bonus"] * 100)))
            else:
                lines.append(t.t("chain.no_combo", pct=round(cash["mult"] * 100)))
        else:
            result = chain.press(hs["chain"], link, req)
            if result["lost"]:
                lines.append(t.t("chain.broken", n=result["lost"]))
        apply(ability, scale, link == "H3")

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
        if defend is not None:
            dmg = max(1, round(dmg * (1 - defend)))
        guard = hs.get("guard")
        if guard and dmg > 0:
            dmg = max(0, round(dmg * (1 - guard["value"])))
            if guard.get("style") == "esquiva":
                hs["dodges"] = int(hs.get("dodges", 0)) + 1
                lines.append(t.t("chain.evaded", pct=round(guard["value"] * 100)))
                if hs.get("vapulear"):
                    hs["chain"]["marks"] += 1                                   # Vapulear: each dodge adds a mark
                    lines.append(t.t("chain.dodge_mark"))
            else:
                lines.append(t.t("chain.endured", pct=round(guard["value"] * 100)))
        shield = hs.get("shield")
        if shield and dmg > 0:
            absorbed = min(dmg, shield["left"])
            dmg -= absorbed
            shield["left"] -= absorbed
            lines.append(t.t("combat.shield", amount=absorbed))
            if shield["left"] <= 0:
                hs["shield"] = None
        hero.hp = max(0, hero.hp - dmg)
        lines.append(t.t("combat.enemy_hits", enemy=enemy_name, move=move_name, dmg=dmg, crit=t.t("combat.crit") if crit else ""))

    if hero_first:
        hero_acts()
        enemy_acts()
    else:
        enemy_acts()
        if hero.hp > 0:
            hero_acts()

    # Damage over time and healing over time tick after the actions.
    dot = enemy.get("dot")
    if dot and enemy["hp"] > 0:
        dmg = max(1, round(stats["attack"] * dot["power"] * hero_mult()))
        enemy["hp"] -= dmg
        dot["rounds"] -= 1
        dot["age"] = int(dot.get("age", 0)) + 1
        lines.append(t.t("combat.dot_tick", enemy=enemy_name, dmg=dmg))
        if dot["rounds"] <= 0:
            enemy["dot"] = None
    if hs.get("hot") and hero.hp > 0:
        healed = heal(stats["max_hp"] * hs["hot"]["value"] * (1 + class_def.get("heal_bonus", 0.0)))
        if healed > 0:
            lines.append(t.t("combat.hot_tick", amount=healed))

    # Outcome checks (as before).
    if enemy["hp"] <= 0:
        enemy["hp"] = 0
        state["outcome"] = "victory"
        lines.append(t.t("combat.victory", enemy=enemy_name))
    elif hero.hp <= 0:
        state["outcome"] = "defeat"
        lines.append(t.t("combat.defeat"))
    elif kind == "flee":
        cb = bal["combat"]
        chance = cb["flee_base"] + (stats["initiative"] - enemy["initiative"]) * cb["flee_per_initiative"]
        chance = max(cb["flee_min"], min(cb["flee_max"], chance))
        if rng.chance(chance):
            state["outcome"] = "fled"
            lines.append(t.t("combat.flee_ok"))
        else:
            lines.append(t.t("combat.flee_fail"))

    # End of round upkeep: timed effects run down.
    for holder, key in ((hs, "empower"), (hs, "hot"), (hs, "guard"), (hs, "vapulear"), (hs, "charged"), (hs, "next_bonus"),
                        (hs, "heal_boost"), (hs, "shield"), (enemy, "exposed"), (enemy, "weakened")):
        effect = holder.get(key)
        if effect and "rounds" in effect:
            effect["rounds"] -= 1
            if effect["rounds"] <= 0:
                holder[key] = None
    if state["outcome"] is None:
        if enemy_def.get("phases"):
            _update_phase(state, enemy_def, ctx, lines)
        enemy["next_move"] = choose_next_move(enemy_def, rng, enemy.get("phase", 0))
        state["round"] += 1
    state["draws"] = rng.draws
    state["log"] = lines
    return lines
