"""Chain combat (0.31): four buttons, combat energy, the role's chain, marks and the spender (D-225 to D-232).

Every class plays the same mechanic; only what each button does and the order each role asks change:
    B  (Básico, "attack"): costs 0 and gives +1 extra energy. Never breaks the chain; basics in a row count as one mark.
    H1 (Constructor), H2 (Preparador), H3 (Gastador): cost 2, 3 and 6 (balance.yaml chain.costs).
Energy: the fight starts with chain.energy.start (5); every turn the hero gains chain.energy.per_turn (2) before acting
(so a spender that costs 6 can be paid with 4 in hand); there is no cap. Defending or drinking a potion is the turn's
action and costs chain.energy.defend_cost / item_cost (1).
The chain: each role has an order (chain.orders; the role's links before H3). A correct button adds a mark; a button
out of order cuts the chain and the marks are lost. Once the order is done, links can be repeated before the spender
(weaving). The spender cashes every mark with the bonus of chain.mark_bonus and the chain starts again. A spender
without a valid combo (the order not done, or fewer than chain.combo_min_distinct different buttons) hits at
chain.no_combo_mult (85 %). Each different combo shape cashed adds to the variety bonus (chain.variety).

[ES]
Para qué sirve: las reglas del combate en cadena del parche 0.31 (las 6 clases nuevas): la energía, el orden de cada rol,
las marcas, el premio del gastador, la variedad y lo que hace cada botón. Las clases viejas (retiradas) siguen con
engine/combat/engine.py tal cual; resolve_round manda aquí a las clases con system: chain.
Documento de diseño: diseno/04-combate/combate-en-cadena.md (D-225 a D-232)
Módulo: M5 Combate
Depende de: engine.core (Rng), engine.hero.hero_stats, content/classes.yaml (system: chain), balance.yaml chain y combat
Lo usan: engine/combat/engine.py (make_combat, validate_choice, resolve_round la llaman con system: chain),
    engine/combat/auto.py (la forma de jugar de las peleas automáticas, chain_choice), engine/service/game.py (la vista
    de combate: chain_status, link_of, cost_of) y tools/sim.py (a través del motor)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: las claves de la cadena dentro del estado de combate ("chain", "combos", "guard", "shield",
    "dodges", "vapulear", "charged", "heal_boost", "next_bonus"; enemy "dot" con "age" y "school")
Reglas que nunca se rompen:
    1. El Básico nunca corta la cadena y varios seguidos cuentan como UNA marca (no se gana premio con básico, básico,
       gastador).
    2. Un botón fuera de orden corta la cadena: se pierden las marcas.
    3. El gastador siempre se puede usar si alcanza la energía; sin combo válido pega a chain.no_combo_mult.
    4. Ninguna habilidad en área toca a más de chain.target_cap (5) a la vez.
    5. No hay tope de energía.
    6. Los porcentajes del premio, el orden de cada rol y la variedad salen de balance.yaml chain (pendientes del dueño:
       se cambian ahí, nunca en el código).
Si cambias esto, revisa:
    - Números: balance.yaml chain.* (energía, costos, órdenes, premio por marcas, variedad); classes.yaml (system: chain)
    - Combos verificados del parche (tests/test_cadena.py: los 12 combos de §4 con su energía y sus marcas)
    - Forma de jugar: engine/combat/auto.py chain_choice (la usan las peleas automáticas y el simulador)
    - Vista: engine/service/game.py _combat_view (línea de la cadena y botones)
    - Pruebas: tests/test_cadena.py, tests/test_clases_031.py
"""

from __future__ import annotations

from typing import Any

LINKS = ("B", "H1", "H2", "H3")
CHAIN_KINDS = ("strike", "dot", "guard", "heal", "shield", "empower", "expose", "weaken", "debuff")


def is_chain(class_def: dict[str, Any]) -> bool:
    """True for a class of the 0.31 chain system. [ES] Qué hace: dice si la clase usa el combate en cadena. La llaman: el motor, la IA y el servicio. Si cambia, afecta: qué reglas juega cada héroe."""
    return class_def.get("system") == "chain"


def cfg(balance: dict[str, Any]) -> dict[str, Any]:
    """The chain block of balance.yaml. [ES] Qué hace: devuelve los números de la cadena. La llaman: todo este módulo. Si cambia, afecta: todo el combate en cadena."""
    return balance["chain"]


def role_of(class_def: dict[str, Any], balance: dict[str, Any]) -> str:
    """Chain role (tanque, sanador, dps, soporte) from the spec's role (defensa, curacion, ataque, soporte).

    [ES] Qué hace: traduce el rol de la especialización al rol de la cadena (chain.role_of). La llaman: order, la IA y la
    vista. Si cambia, afecta: qué orden pide cada clase.
    """
    return cfg(balance)["role_of"].get(class_def.get("role", "ataque"), "dps")


def order(class_def: dict[str, Any], balance: dict[str, Any]) -> list[str]:
    """The role's full chain, spender included (e.g. tanque: B, H2, H1, H3). [ES] Qué hace: el orden que pide el rol, configurable (pendiente 6 del parche: el del tanque está en revisión). La llaman: required, la vista y la IA. Si cambia, afecta: qué botones suman marca."""
    return list(cfg(balance)["orders"][role_of(class_def, balance)])


def required(class_def: dict[str, Any], balance: dict[str, Any]) -> list[str]:
    """The links the role needs before the spender. [ES] Qué hace: el orden sin el gastador. La llaman: press y la IA. Si cambia, afecta: cuándo está hecho el combo."""
    return [link for link in order(class_def, balance) if link != "H3"]


def cost_of(link: str, balance: dict[str, Any]) -> int:
    """Energy a button costs (B 0, H1 2, H2 3, H3 6). [ES] Qué hace: el costo de cada botón. La llaman: validate, resolve y la vista. Si cambia, afecta: el ritmo de toda pelea."""
    return int(cfg(balance)["costs"][link])


def link_of(choice: dict[str, Any], class_def: dict[str, Any]) -> str | None:
    """Which button a choice is: "B" for the attack, the ability's link for an ability, None otherwise.

    [ES] Qué hace: dice qué botón de la cadena es una elección. La llaman: validate, resolve, la IA y la vista. Si cambia,
    afecta: qué cuesta y qué suma cada elección.
    """
    if choice.get("type") == "attack":
        return "B"
    if choice.get("type") == "ability":
        index = choice.get("index", -1)
        abilities = class_def.get("abilities") or []
        if 0 <= index < len(abilities):
            return abilities[index].get("link")
    return None


def ability_for(link: str, class_def: dict[str, Any]) -> dict[str, Any]:
    """The definition behind a button (the attack for B). [ES] Qué hace: devuelve la habilidad de un botón. La llaman: resolve y la vista. Si cambia, afecta: qué hace cada botón."""
    if link == "B":
        return class_def["attack"]
    for ability in class_def.get("abilities") or []:
        if ability.get("link") == link:
            return ability
    return class_def["attack"]


def new_chain() -> dict[str, Any]:
    """An empty chain: step in the order, marks, last button and buttons pressed. [ES] Qué hace: una cadena vacía. La llaman: init_hero y press. Si cambia, afecta: el estado guardado de las peleas."""
    return {"step": 0, "marks": 0, "last": None, "seq": []}


def init_hero(balance: dict[str, Any]) -> dict[str, Any]:
    """The hero side of a new chain fight. [ES] Qué hace: arma la parte del héroe de una pelea nueva (energía inicial, cadena vacía). La llaman: make_combat y ensure_hero. Si cambia, afecta: cómo empieza cada pelea."""
    return {"resource": int(cfg(balance)["energy"]["start"]), "stamina": None, "cooldowns": {}, "combo": 0, "toxicity": 0,
            "chain": new_chain(), "combos": []}


def ensure_hero(hs: dict[str, Any], balance: dict[str, Any]) -> None:
    """A fight saved by the old system goes on with chain keys (a hero moved to a 0.31 class mid-fight).

    [ES] Qué hace: si la pelea guardada no tiene cadena (empezó con una clase vieja), la agrega con la energía inicial.
    La llama: resolve_round y validate_choice. Si cambia, afecta: las peleas a medio jugar al desplegar el parche.
    """
    if "chain" not in hs:
        hs["chain"] = new_chain()
        hs["combos"] = []
        hs["resource"] = int(cfg(balance)["energy"]["start"])


def mark_bonus(marks: int, balance: dict[str, Any]) -> float:
    """The spender's bonus for this many marks (2: +10 %, 3-4: +25 %, 5+: +50 %; balance.yaml chain.mark_bonus).

    [ES] Qué hace: el premio por marcas (borrador: pendiente 1 del parche, se cambia en balance.yaml). La llaman: resolve y la
    vista. Si cambia, afecta: cuánto pega, cura o protege cada gastador.
    """
    best = 0.0
    for tier in cfg(balance)["mark_bonus"]:
        if marks >= int(tier["marks"]):
            best = float(tier["bonus"])
    return best


def variety_bonus(shapes: list[str], balance: dict[str, Any]) -> float:
    """The variety bonus for this many different combo shapes (chain.variety.steps). [ES] Qué hace: el bono por variedad (+2 % con 2 combos distintos, +3 % con 3; pendiente 5 del parche: chain.variety.scope dice si dura la pelea o para siempre). La llaman: resolve y la vista. Si cambia, afecta: el premio por variar."""
    count = len(set(shapes))
    best = 0.0
    for step in cfg(balance)["variety"]["steps"]:
        if count >= int(step["combos"]):
            best = float(step["bonus"])
    return best


def press(chain: dict[str, Any], link: str, req: list[str]) -> dict[str, Any]:
    """Press B, H1 or H2: advance the order, add a mark or cut the chain. Returns {"mark": bool, "lost": marks lost}.

    [ES]
    Qué hace: aplica la regla de dependencia (igual para las 6 clases, solo cambia el orden):
      - El Básico nunca corta: si es el siguiente eslabón del orden, avanza; suma marca salvo que el anterior también
        fuera Básico (los básicos seguidos cuentan como una sola).
      - H1 o H2: con el orden ya cumplido, se repiten sin cortar (tejer) y suman marca; si es el siguiente eslabón,
        avanza y suma; si no, la cadena se corta (se pierden las marcas) y, si ese botón abre el orden, empieza una nueva.
    La llaman: resolve_round y la IA (para prever). Si cambia, afecta: las marcas de todas las clases.
    """
    out = {"mark": False, "lost": 0}
    complete = chain["step"] >= len(req)
    if link == "B":
        if not complete and req[chain["step"]] == "B":
            chain["step"] += 1
        if chain["last"] != "B":
            chain["marks"] += 1
            out["mark"] = True
    elif complete or req[chain["step"]] == link:
        if not complete:
            chain["step"] += 1
        chain["marks"] += 1
        out["mark"] = True
    else:
        out["lost"] = chain["marks"]
        chain.update(new_chain())
        if req and req[0] == link:
            chain["step"], chain["marks"], out["mark"] = 1, 1, True
    chain["last"] = link
    chain["seq"].append(link)
    return out


def spend(chain: dict[str, Any], req: list[str], balance: dict[str, Any]) -> dict[str, Any]:
    """Cash the chain with the spender. Returns {"valid", "marks", "bonus", "mult", "shape"} and empties the chain.

    [ES]
    Qué hace: el gastador cobra las marcas. Combo válido = el orden del rol cumplido y al menos chain.combo_min_distinct
    botones distintos (contando el gastador): suma su marca y da el premio por marcas. Sin combo válido pega a
    chain.no_combo_mult (85 %) y sin premio. Siempre deja la cadena en cero.
    La llaman: resolve_round y la vista (para prever). Si cambia, afecta: cuánto rinde cada gastador.
    """
    c = cfg(balance)
    seq = list(chain["seq"]) + ["H3"]
    valid = chain["step"] >= len(req) and len(set(seq)) >= int(c["combo_min_distinct"])
    marks = chain["marks"] + 1 if valid else 0
    bonus = mark_bonus(marks, balance) if valid else 0.0
    mult = 1.0 if valid else float(c["no_combo_mult"])
    shape = "-".join(_squeeze(seq)) if valid else ""
    chain.update(new_chain())
    return {"valid": valid, "marks": marks, "bonus": bonus, "mult": mult, "shape": shape}


def _squeeze(seq: list[str]) -> list[str]:
    """Basics in a row count as one (for the combo shape too)."""
    out: list[str] = []
    for link in seq:
        if not (link == "B" and out and out[-1] == "B"):
            out.append(link)
    return out


def preview(chain: dict[str, Any], req: list[str], balance: dict[str, Any]) -> dict[str, Any]:
    """What the spender would cash right now, without changing the chain. [ES] Qué hace: prevé el premio del gastador (para la vista y la IA). La llaman: la vista y la IA. Si cambia, afecta: lo que el jugador lee."""
    copy = {"step": chain["step"], "marks": chain["marks"], "last": chain["last"], "seq": list(chain["seq"])}
    return spend(copy, req, balance)


def next_link(chain: dict[str, Any], req: list[str]) -> str:
    """The next link of the order, or "H3" when it is done. [ES] Qué hace: dice qué botón sigue en el orden. La llaman: la vista y la IA. Si cambia, afecta: la pista de la cadena."""
    return req[chain["step"]] if chain["step"] < len(req) else "H3"


def target_cap(balance: dict[str, Any]) -> int:
    """At most this many targets for any area or group ability (5). [ES] Qué hace: el tope de objetivos de toda habilidad en área. La llaman: resolve. Si cambia, afecta: grupos grandes (obliga a llevar más de un sanador)."""
    return int(cfg(balance)["target_cap"])
