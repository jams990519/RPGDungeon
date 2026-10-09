"""Automatic fights (D-114): a basic but attentive way to play one fight alone.

The policy reads the enemy's warning, heals when low, interrupts big interruptible moves, answers big hits with the
right response (dodge, block, shield, or the basic dodge when attentive), keeps buffs and debuffs up, and otherwise
hits. With use_items it also drinks belt potions (and, when attentive, uses bandages) when life is low.
It only picks choices that validate_choice accepts, so an automatic fight follows exactly the rules of a manual one.

It is the ONE policy of the project: the game uses it for the automatic fights of a batch (engine/service/game.py)
and the balance simulator uses it for every number it prints (tools/sim.py).

[ES]
Para qué sirve: jugar sola una pelea con una forma de jugar básica pero atenta (lee el aviso, interrumpe, esquiva o
    bloquea los golpes grandes, mantiene mejoras y debilitamientos, se cura si está bajo y, si se permite, usa las
    pociones y vendas del cinturón). Las mismas reglas que una pelea a mano: solo elige lo que validate_choice acepta.
Documento de diseño: diseno/02-mundo/mapa-infinito-y-viaje.md §1.12.1 (D-114); diseno/04-combate/ronda-y-acciones.md
Módulo: M5 Combate
Depende de: engine.combat.engine (find_move, validate_choice, resolve_round), engine.hero (hero_stats),
    balance.yaml auto_fight.policy (umbrales de la forma de jugar) y auto_fight.max_rounds
Lo usan: engine/service/game.py (peleas automáticas de los lotes y de la cacería en lote) y tools/sim.py (todas las
    simulaciones de balance)
Eventos que publica: ninguno (el servicio publica HitReceived con on_hit, y CombatEnded en _end_combat)
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno (cambia el estado de combate que le pasan, como resolve_round)
Reglas que nunca se rompen:
    1. Una sola forma de jugar para el juego y el simulador: si cambia, cambian los números del simulador y las peleas
       automáticas de todos los jugadores (por eso los umbrales viven en balance.yaml).
    2. Nunca elige algo inválido: todo pasa por validate_choice; si nada sirve, ataca (siempre se puede).
    3. Sin use_items no toca el cinturón (opción 🧪 Pociones de ⚙️ Opciones).
    4. Una pelea automática siempre termina: a las auto_fight.max_rounds rondas el héroe la deja ("fled", sin premio
       ni castigo).
0.31 (D-225): las clases con system: chain juegan con chain_choice (sobrevivir y luego seguir el orden de su rol).
Si cambias esto, revisa:
    - Simulador: tools/sim.py (choose llama a choose_action; compara --summary, --real y --boss antes y después)
    - Servicio: engine/service/game.py _auto_combat (opción de pociones, eventos, fin de la pelea)
    - Números: balance.yaml auto_fight.policy y auto_fight.max_rounds; registro en diseno/03-personaje/balance.md
    - Pruebas: tests/test_options.py
"""

from __future__ import annotations

from typing import Any, Callable

from engine.combat.engine import CombatContext, find_move, resolve_round, validate_choice
from engine.hero.hero import Hero, hero_stats


def _belt_pick(hero: Hero, ctx: CombatContext, kind: str, missing: float) -> list[str]:
    """Belt items of a kind ("potion", "bandage"), best first: the biggest heal that fits the missing life, then the rest.

    [ES] Qué hace: ordena las pociones (o vendas) del cinturón: primero la que más cura sin pasarse de lo que falta, después
    las otras de menor a mayor. Con solo 🧪 Poción de vida en el cinturón (el simulador) da siempre esa.
    La llama: choose_action. Si cambia, afecta: qué poción bebe el héroe en las peleas automáticas.
    """
    items = [(float(ctx.items[i].get("heal", 0.0)), i) for i, n in hero.belt.items()
             if n > 0 and i in ctx.items and ctx.items[i].get("kind") == kind]
    fitting = sorted((it for it in items if it[0] <= missing), reverse=True)
    rest = sorted(it for it in items if it[0] > missing)
    return [i for _, i in fitting + rest]


def choose_action(state: dict[str, Any], hero: Hero, class_def: dict[str, Any], ctx: CombatContext,
                  attentive: bool = True, use_items: bool = True) -> dict[str, Any]:
    """The round's choice of a basic (attentive=False) or attentive (attentive=True) player.

    Args:
        state: the fight state (make_combat / resolve_round).
        class_def: the hero's kit (abilities, resource, bonuses), as the service or the simulator builds it.
        attentive: also uses bandages when very low and the basic dodge against very big unanswered hits.
        use_items: may use belt items (potions; bandages when attentive). False never touches the belt.

    Returns:
        A choice that validate_choice accepts ({"type": "attack"} if nothing else fits).

    [ES]
    Qué hace: elige la acción de la ronda como un jugador básico (attentive=False) o atento (attentive=True, la que usan
    las peleas automáticas del juego): se cura con poca vida, bebe pociones si se permite, corta o responde los golpes
    grandes que avisa el enemigo, mantiene sus mejoras y los debilitamientos del enemigo y, si no, pega.
    La llaman: play_out (peleas automáticas) y tools/sim.py (choose).
    Si cambia, afecta: todos los números del simulador y cómo pelean solos los héroes de todos los jugadores.
    """
    if class_def.get("system") == "chain":            # 0.31: the six chain classes play their role's chain
        return chain_choice(state, hero, class_def, ctx, attentive, use_items)
    policy = ctx.balance["auto_fight"]["policy"]
    enemy, hs = state["enemy"], state["hero"]
    move = find_move(ctx.enemies[enemy["id"]], enemy["next_move"])
    tags = move.get("tags", [])
    abilities = list(enumerate(class_def["abilities"]))
    stats = hero_stats(class_def, hero.level)

    def ok(choice: dict[str, Any]) -> bool:
        return validate_choice(state, hero, class_def, choice, ctx) is None

    def can(i: int) -> bool:
        return ok({"type": "ability", "index": i})

    def use(i: int) -> dict[str, Any]:
        return {"type": "ability", "index": i}

    frac = hero.hp / stats["max_hp"]
    if frac < policy["heal_below"]:
        for i, a in abilities:
            if a["kind"] == "heal" and can(i):
                return use(i)
    if use_items and frac < policy["potion_below"]:
        for item_id in _belt_pick(hero, ctx, "potion", 1 - frac):
            if ok({"type": "item", "item_id": item_id}):
                return {"type": "item", "item_id": item_id}
    if use_items and attentive and frac < policy["bandage_below"]:
        for item_id in _belt_pick(hero, ctx, "bandage", 1 - frac):
            if ok({"type": "item", "item_id": item_id}):
                return {"type": "item", "item_id": item_id}
    first = stats["initiative"] >= enemy["initiative"]
    channel = move.get("kind") == "channel"
    power = move.get("power", 1) * enemy.get("buff", 1.0)
    big = (not channel) and power > policy["big_hit"]
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
        if attentive and power >= policy["dodge_hit"] and ok({"type": "dodge"}):
            return {"type": "dodge"}
        for i, a in abilities:
            if a["kind"] == "weaken" and not enemy.get("weakened") and can(i):
                return use(i)
    for i, a in abilities:
        if a["kind"] == "hot" and frac < policy["hot_below"] and not hs.get("hot") and can(i):
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
        if k == "finisher" and hs["combo"] >= policy["finisher_combo"] and can(i):
            return use(i)
        if k == "strike" and can(i):
            return use(i)
        if k == "heal" and frac < policy["heal_late_below"] and can(i):
            return use(i)
    return {"type": "attack"}


def chain_choice(state: dict[str, Any], hero: Hero, class_def: dict[str, Any], ctx: CombatContext,
                 attentive: bool = True, use_items: bool = True) -> dict[str, Any]:
    """The round's choice for a chain class (0.31): survive first, then follow the role's chain.

    [ES]
    Qué hace: la forma de jugar de las clases nuevas en las peleas automáticas y el simulador. Primero sobrevive (el sanador
    usa su curación grande o la chica con poca vida; pociones; el tanque levanta su aguante o esquiva ante un golpe grande;
    el Mago interrumpe un ataque cargado con su Ruptura; con un golpe muy grande y nada mejor, se defiende). Después sigue
    el orden de su rol: toca el siguiente eslabón si le alcanza la energía; si no, el Básico (que nunca corta la cadena y da
    energía); con el orden cumplido suelta el gastador apenas puede. El sanador sano no gasta curaciones: pega con el
    Básico hasta que le hace falta curarse.
    La llama: choose_action (system: chain). Si cambia, afecta: las peleas automáticas y los números del simulador.
    """
    from engine.combat import chain
    from engine.combat.chain_round import available_energy

    bal = ctx.balance
    policy = bal["auto_fight"]["policy"]
    enemy, hs = state["enemy"], state["hero"]
    chain.ensure_hero(hs, bal)
    move = find_move(ctx.enemies[enemy["id"]], enemy["next_move"])
    tags = move.get("tags", [])
    stats = hero_stats(class_def, hero.level)
    role = chain.role_of(class_def, bal)
    req = chain.required(class_def, bal)
    energy = available_energy(state, bal)
    index = {a.get("link"): i for i, a in enumerate(class_def["abilities"])}

    def ok(choice: dict[str, Any]) -> bool:
        return validate_choice(state, hero, class_def, choice, ctx) is None

    def press(link: str) -> dict[str, Any] | None:
        choice = {"type": "attack"} if link == "B" else {"type": "ability", "index": index.get(link, -1)}
        return choice if ok(choice) else None

    # A hit that finishes the enemy beats anything else (the cheapest that surely kills: lowest roll, no crit).
    low = float(bal["combat"]["damage_spread"][0]) * (1 - float(enemy["armor"]))
    mult = (1 + (hs.get("empower") or {}).get("value", 0.0)) * (1 + (enemy.get("exposed") or {}).get("value", 0.0))
    for link in ("B", "H1", "H2", "H3"):
        spec = chain.ability_for(link, class_def)
        hit = float(spec.get("power", 0.0)) if spec.get("kind", "strike") in ("strike", "guard", "debuff") else 0.0
        if link == "H3" and not chain.preview(hs["chain"], req, bal)["valid"]:
            hit *= float(chain.cfg(bal)["no_combo_mult"])
        if hit and stats["attack"] * hit * mult * low >= enemy["hp"] and press(link):
            return press(link)
    frac = hero.hp / stats["max_hp"]
    if role == "sanador" and frac < policy["heal_below"]:
        for link in ("H3", "H1"):
            spec = chain.ability_for(link, class_def)
            if spec.get("kind") == "heal" and press(link):
                return press(link)
    if use_items and frac < policy["potion_below"]:
        for item_id in _belt_pick(hero, ctx, "potion", 1 - frac):
            if ok({"type": "item", "item_id": item_id}):
                return {"type": "item", "item_id": item_id}
    if use_items and attentive and frac < policy["bandage_below"]:
        for item_id in _belt_pick(hero, ctx, "bandage", 1 - frac):
            if ok({"type": "item", "item_id": item_id}):
                return {"type": "item", "item_id": item_id}
    channel = move.get("kind") == "channel"
    power = move.get("power", 1) * enemy.get("buff", 1.0)
    big = (not channel) and power > policy["big_hit"]
    first = stats["initiative"] >= enemy["initiative"]
    spender = chain.ability_for("H3", class_def)
    if spender.get("interrupt") and first and (channel or "interruptible" in tags) and press("H3"):
        return press("H3")
    if big and role == "tanque" and not hs.get("guard"):
        for link in ("H2", "H3"):
            if chain.ability_for(link, class_def).get("kind") == "guard" and press(link):
                return press(link)
    if big and attentive and power >= policy["dodge_hit"] and not hs.get("guard") and not hs.get("shield") and ok({"type": "dodge"}):
        return {"type": "dodge"}
    if role == "sanador" and frac >= policy["heal_late_below"]:
        h2 = chain.ability_for("H2", class_def)      # a healthy healer hits: its H2 if it is a hit (Paladín), else the Básico
        if h2.get("kind") == "strike" and hs["chain"]["last"] == "B" and press("H2"):
            return press("H2")
        return {"type": "attack"}
    nxt = chain.next_link(hs["chain"], req)
    if nxt != "B" and chain.cost_of(nxt, bal) <= energy and press(nxt):
        return press(nxt)
    return {"type": "attack"}


def play_out(state: dict[str, Any], hero: Hero, class_def: dict[str, Any], ctx: CombatContext, *,
             attentive: bool = True, use_items: bool = True, max_rounds: int | None = None,
             on_hit: Callable[[int], None] | None = None) -> int:
    """Play the fight to its end with choose_action. Returns the rounds played.

    If the fight has no outcome after max_rounds (balance auto_fight.max_rounds by default), the hero breaks it off:
    outcome "fled" (no reward, no penalty) with the line auto.gave_up.

    [ES]
    Qué hace: juega la pelea entera con choose_action, ronda por ronda con resolve_round (las mismas reglas que a mano).
    Si después de auto_fight.max_rounds rondas nadie cayó, el héroe la deja: resultado "fled", sin premio ni castigo.
    on_hit recibe el daño de cada ronda en que el héroe perdió vida (el servicio publica HitReceived).
    La llama: engine/service/game.py _auto_combat. Después, el servicio cierra la pelea con _end_combat (botín, experiencia,
    derrota) como cualquier pelea.
    Si cambia, afecta: las peleas automáticas de los lotes y de la cacería en lote.
    """
    limit = int(ctx.balance["auto_fight"]["max_rounds"] if max_rounds is None else max_rounds)
    rounds = 0
    while state["outcome"] is None:
        if rounds >= limit:
            state["outcome"] = "fled"
            state["log"] = list(state.get("log") or []) + [ctx.texts.t("auto.gave_up")]
            break
        before = hero.hp
        resolve_round(state, hero, class_def, choose_action(state, hero, class_def, ctx, attentive, use_items), ctx)
        rounds += 1
        if on_hit and hero.hp < before:
            on_hit(before - hero.hp)
    return rounds
