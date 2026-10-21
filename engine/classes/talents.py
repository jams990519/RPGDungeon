"""Talent points, unlocks, the 3-slot bar and the effective combat kit of a hero.

[ES]
Para qué sirve: calcular qué habilidades tiene cada héroe según sus puntos (8 por especialización,
repartidas en los 100 niveles), armar su barra de 3 (elegida por el jugador o automática) y devolver
el "kit" (clase + habilidades + mejoras pasivas) que usa el combate.
Documento de diseño: diseno/03-personaje/talentos.md (D-68, D-79)
Módulo: M3 Clases y talentos
Depende de: content/classes.yaml (group, role, abilities), content/balance.yaml (talents; chain.second_role_level, chain.hybrid)
Lo usan: engine/service/game.py
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno (lee y cambia hero.talents, hero.points, hero.unlocked, hero.bar y hero.hybrid)
Reglas que nunca se rompen:
    1. bar() siempre pone una respuesta en la casilla 1 si el héroe tiene alguna desbloqueada.
    2. Un héroe nunca pierde una habilidad desbloqueada (salvo al reiniciar talentos o si su especialización se retira).
    3. Una barra guardada que ya no vale (hero.bar) no rompe nada: se usa la barra automática.
    4. El modo híbrido (0.54, D-312) solo cambia un botón de rol por el del mismo puesto (link) del otro rol: el Básico, el
       orden de los botones (H1, H2, H3) y su número nunca cambian; una elección guardada que ya no vale (modo cerrado,
       puesto sin pareja) se ignora y se pelea con la barra del rol.
Si cambias esto, revisa:
    - Combate: engine/combat/engine.py recibe el kit como class_def (el orden de la barra es el de los botones)
    - Servicio: engine/service/game.py (pantallas 🌟 Talentos y 🎛️ Barra de combate)
    - D-110: la barra automática de Defensa guarda su curación más nueva en la casilla 3 (HEAL_FIRST_ROLES); la mejora
      pasiva puede traer armor (talents.passive.defensa), que hero_stats suma a la armadura (tools/balance_report.py)
    - 0.31 (D-225, D-230): las clases nuevas (system: chain) no reparten puntos a mano: van solos al rol activo
      (sync_chain), sus 3 habilidades están siempre abiertas, la barra es la del rol (el modo híbrido de la 0.54 la mezcla,
      abajo) y desde el nivel 5 se cambia de rol gratis
      (switch_role). Un héroe con una especialización vieja (retired con migrate_to) pasa a la nueva al cargar, con su
      nivel, experiencia, equipo y monedas (ensure_talents)
    - 0.54 (D-231, D-312, D-330): el 🔀 modo híbrido. Desde chain.hybrid.level (10) y con el segundo rol abierto, cada uno de
      los 3 botones de rol (H1, H2, H3) puede llevar la habilidad del MISMO puesto del otro rol de la clase (toggle_hybrid);
      el Básico nunca cambia y la barra sigue con 4 botones. La elección se guarda en hero.hybrid por pareja de roles
      ("<rol activo>><rol que presta>": cada rol guarda la suya al cambiar de rol) y como mucho chain.hybrid.max_mixed (3).
      kit() pasa balance a bar(), que arma la barra con chain_bar: la habilidad prestada es la del otro rol tal cual (sus
      números y sus marcas: daño, cura, agro), marcada con from_spec. El cuerpo (vida, ataque, armadura, iniciativa, la mejora
      pasiva de los puntos) y el orden de la cadena siguen siendo los del rol activo. Quien no toca el modo híbrido pelea
      igual que antes (hero.hybrid vacío)
    - Pruebas: tests/test_talents.py, tests/test_spec_abilities.py, tests/test_balance_d110.py, tests/test_clases_031.py,
      tests/test_modo_hibrido.py
"""

from __future__ import annotations

import copy
from typing import Any

from engine.hero.hero import Hero


def specs_of(classes: dict[str, Any], group: str) -> list[str]:
    """Spec ids of a class, in content order. [ES] Qué hace: lista las especializaciones de una clase. La llaman: el servicio. Si cambia, afecta: el orden en pantalla."""
    return [cid for cid, c in classes.items() if c.get("group", cid) == group and not c.get("retired")]


def default_spec(classes: dict[str, Any], group: str) -> str:
    """First spec of a class: the hero's starting point. [ES] Qué hace: da la especialización inicial de una clase. La llaman: la creación de héroe. Si cambia, afecta: los héroes nuevos."""
    return specs_of(classes, group)[0]


def base_response(classes: dict[str, Any], group: str) -> str:
    """The free starting response of a class (first response of its first spec). [ES] Qué hace: da la respuesta defensiva con la que empieza la clase. La llaman: la creación de héroe. Si cambia, afecta: el kit inicial."""
    for ability in classes[default_spec(classes, group)]["abilities"]:
        if ability["kind"] == "response":
            return ability["id"]
    return classes[default_spec(classes, group)]["abilities"][0]["id"]


def _abilities(classes: dict[str, Any], group: str) -> dict[str, tuple[str, int, dict[str, Any]]]:
    out = {}
    for spec in specs_of(classes, group):
        for index, ability in enumerate(classes[spec]["abilities"]):
            out[ability["id"]] = (spec, index, ability)
    return out


def unlock_points(balance: dict[str, Any]) -> list[int]:
    """Points in a spec needed to unlock each of its abilities, in order (8 values). [ES] Qué hace: dice cuántos puntos pide cada habilidad. La llaman: el servicio y spend_point. Si cambia, afecta: el ritmo de desbloqueo."""
    return list(balance["talents"]["unlock"])


def _unlock_spec(classes: dict[str, Any], balance: dict[str, Any], hero: Hero, spec: str) -> list[str]:
    """Unlock every ability of a spec the hero's points there already pay for; returns the new ids."""
    new = []
    abilities = classes[spec]["abilities"]
    for index, need in enumerate(unlock_points(balance)):
        if index < len(abilities) and hero.talents.get(spec, 0) >= need and abilities[index]["id"] not in hero.unlocked:
            hero.unlocked.append(abilities[index]["id"])
            new.append(abilities[index]["id"])
    return new


def _group(classes: dict[str, Any], hero: Hero) -> str:
    return classes[hero.class_id].get("group", hero.class_id)


def ensure_talents(classes: dict[str, Any], balance: dict[str, Any], hero: Hero) -> None:
    """Initialise or migrate a hero to the talent system (heroes made before it keep their progress).

    [ES]
    Qué hace: prepara los talentos de un héroe; a los héroes viejos les da los puntos que les
    corresponden por nivel, puestos en su especialización actual.
    La llaman: el servicio al cargar un héroe.
    Si cambia, afecta: los héroes guardados.
    """
    old = classes.get(hero.class_id, {})
    if old.get("retired") and old.get("migrate_to") in classes:
        # 0.31 (D-225): the old classes were replaced. The hero moves to the new spec its old one maps to, keeping level,
        # experience, gear and coins; its points are collected and placed again in the new role (sync_chain below).
        # 0.32 (D-233): the Chamán became the Paladín, so a pointer may lead to another retired spec: follow it (a few hops).
        for _ in range(5):
            spec = classes.get(hero.class_id, {})
            if not (spec.get("retired") and spec.get("migrate_to") in classes):
                break
            hero.class_id = spec["migrate_to"]
        hero.talents, hero.points, hero.unlocked, hero.bar = {}, 0, [], []
        hero.profiles, hero.dual_unlocked, hero.profile = {}, False, 1
    group = _group(classes, hero)
    if classes.get(hero.class_id, {}).get("retired"):
        # The spec was retired (D-69): move to the class's first spec and refund its points.
        hero.points += hero.talents.pop(hero.class_id, 0)
        hero.class_id = default_spec(classes, group)
        retired_ids = {a["id"] for cid, c in classes.items() if c.get("retired") for a in c["abilities"]}
        hero.unlocked = [a for a in hero.unlocked if a not in retired_ids]
    if is_chain_spec(classes, hero.class_id):
        sync_chain(classes, hero)
        return
    if hero.unlocked:
        # Heroes saved before abilities 4-8 existed (D-79): unlock what their points already pay for.
        for spec in specs_of(classes, group):
            if hero.talents.get(spec):
                _unlock_spec(classes, balance, hero, spec)
        return
    hero.unlocked = [base_response(classes, group)]
    if hero.level > 1 and not hero.talents:
        for _ in range(hero.level - 1):
            hero.points += 1
            spend_point(classes, balance, hero, hero.class_id)


def is_chain_spec(classes: dict[str, Any], spec: str) -> bool:
    """True for a 0.31 chain spec (system: chain). [ES] Qué hace: dice si la especialización es de las clases nuevas. La llaman: este módulo y el servicio. Si cambia, afecta: qué reglas de talentos y combate usa el héroe."""
    return classes.get(spec, {}).get("system") == "chain"


def sync_chain(classes: dict[str, Any], hero: Hero) -> None:
    """A chain hero's level points all sit in its active role; its four buttons are always open.

    [ES]
    Qué hace: en las clases nuevas (0.31) los puntos de nivel van solos al rol activo (1 por nivel, D-215: subir de nivel no
    da estadísticas por sí solo, las dan los puntos), los 3 botones de habilidad siempre están abiertos (todas las clases
    pegan desde el principio) y la barra es la del rol (Básico, H1, H2, H3). Al cambiar de rol los puntos se recogen y se ponen
    en el rol nuevo (chain.keep_points: pendiente 4 del parche; hoy no cambia nada porque los puntos tienen un solo destino).
    No toca hero.hybrid: lo que cambió el modo híbrido (0.54) se guarda por pareja de roles y sigue al volver a cada rol.
    La llaman: ensure_talents (cada vez que se carga el héroe), switch_role y el cambio de clase (D-270).
    Si cambia, afecta: la mejora pasiva de cada héroe de las clases nuevas.
    """
    hero.talents = {hero.class_id: max(0, hero.level - 1)}
    hero.points = 0
    hero.unlocked = [a["id"] for a in classes[hero.class_id]["abilities"]]
    hero.bar = []


def second_role_open(balance: dict[str, Any], hero: Hero) -> bool:
    """From chain.second_role_level (5) the hero can play the other role of its class. [ES] Qué hace: dice si el héroe ya aprendió su segundo rol (D-230). La llaman: switch_role y el servicio. Si cambia, afecta: cuándo se cambia de rol."""
    return hero.level >= int(balance["chain"]["second_role_level"])


def switch_role(classes: dict[str, Any], balance: dict[str, Any], hero: Hero, spec: str) -> bool:
    """Play the other role of the class (0.31, D-230). Returns True if done.

    [ES]
    Qué hace: cambia el rol activo a la otra especialización de la clase, desde el nivel chain.second_role_level y gratis.
    Los puntos se recogen y se reparten de nuevo en el rol nuevo (sync_chain). El modo híbrido no se toca: cada rol guarda
    su propia elección en hero.hybrid (D-330), así que el rol nuevo pelea con la suya.
    La llaman: el servicio (botón 🔄 en la especialización).
    Si cambia, afecta: el rol de cada héroe de las clases nuevas.
    """
    group = _group(classes, hero)
    if not is_chain_spec(classes, hero.class_id) or spec == hero.class_id or spec not in specs_of(classes, group):
        return False
    if not second_role_open(balance, hero):
        return False
    hero.class_id = spec
    sync_chain(classes, hero)
    return True


HYBRID_LINKS = ("H1", "H2", "H3")      # D-312: the three role buttons the hybrid mode can swap; the Básico (B) never changes


def hybrid_max(balance: dict[str, Any]) -> int:
    """How many role buttons the hybrid mode may swap at once (chain.hybrid.max_mixed; null or 0 = not offered).

    [ES] Qué hace: dice cuántos de los 3 botones de rol se pueden cambiar (D-312: los 3). La llaman: hybrid_open,
    hybrid_choice, toggle_hybrid y el servicio. Si cambia, afecta: cuántos botones presta el otro rol.
    """
    return int((balance["chain"].get("hybrid") or {}).get("max_mixed") or 0)


def hybrid_partner(classes: dict[str, Any], hero: Hero) -> str | None:
    """The role that lends its abilities: the other active role of the hero's class (None if there is none).

    [ES] Qué hace: devuelve el otro rol de la clase (el que presta sus botones). La llaman: este módulo y el servicio. Si
    cambia, afecta: de dónde salen las habilidades prestadas.
    """
    others = [s for s in specs_of(classes, _group(classes, hero)) if s != hero.class_id and is_chain_spec(classes, s)]
    return others[0] if others else None


def hybrid_open(classes: dict[str, Any], balance: dict[str, Any], hero: Hero) -> bool:
    """True when the hero can use the hybrid mode: a chain role, level chain.hybrid.level, second role open, max_mixed > 0.

    [ES] Qué hace: dice si el 🔀 modo híbrido está abierto (D-231: nivel 10; hace falta el segundo rol, D-230). La llaman:
    hybrid_choice, toggle_hybrid y el servicio (botón 🔀 Modo híbrido, D-287: antes no se muestra). Si cambia, afecta:
    quién ve y usa el modo híbrido.
    """
    if not is_chain_spec(classes, hero.class_id) or hybrid_max(balance) <= 0:
        return False
    if hero.level < int(balance["chain"]["hybrid"]["level"]) or not second_role_open(balance, hero):
        return False
    return hybrid_partner(classes, hero) is not None


def _in_slot(class_def: dict[str, Any], link: str) -> dict[str, Any] | None:
    """The ability of a chain spec in a slot (H1, H2, H3), or None."""
    return next((a for a in class_def.get("abilities") or [] if a.get("link") == link), None)


def hybrid_pairs(classes: dict[str, Any], hero: Hero) -> list[tuple[str, dict[str, Any] | None, dict[str, Any] | None]]:
    """Each role slot in order: (link, the active role's ability, the other role's ability in the same slot or None).

    [ES] Qué hace: para cada puesto (Constructor, Preparador, Gastador) da la habilidad de tu rol y la del mismo puesto de tu
    otro rol (None si no tiene: ese puesto no se puede cambiar y la pantalla muestra "—"). La llaman: hybrid_choice,
    toggle_hybrid y la pantalla 🔀 Modo híbrido. Si cambia, afecta: qué se puede cambiar.
    """
    partner = hybrid_partner(classes, hero)
    own, other = classes[hero.class_id], (classes[partner] if partner else {})
    return [(link, _in_slot(own, link), _in_slot(other, link)) for link in HYBRID_LINKS]


def hybrid_key(classes: dict[str, Any], hero: Hero) -> str | None:
    """Where the choice is saved in hero.hybrid: "<active role>><lending role>" (one choice per role pair and direction).

    [ES] Qué hace: la clave de la elección guardada, por pareja de roles (D-330: cada rol guarda la suya; al cambiar de rol se
    usa la del rol nuevo). La llaman: hybrid_choice y toggle_hybrid. Si cambia, afecta: las elecciones guardadas (las
    claves viejas dejarían de leerse).
    """
    partner = hybrid_partner(classes, hero)
    return f"{hero.class_id}>{partner}" if partner else None


def hybrid_choice(classes: dict[str, Any], balance: dict[str, Any], hero: Hero) -> list[str]:
    """The role slots swapped right now, in order (H1, H2, H3); [] while the mode is closed.

    [ES] Qué hace: devuelve los puestos que llevan la habilidad del otro rol. Una elección guardada que ya no vale (modo
    cerrado, puesto sin pareja, más que chain.hybrid.max_mixed) se ignora sin borrarla. La llaman: chain_bar, toggle_hybrid
    y el servicio. Si cambia, afecta: qué botones salen en combate.
    """
    if not hybrid_open(classes, balance, hero):
        return []
    saved = (hero.hybrid or {}).get(hybrid_key(classes, hero) or "") or []
    valid = [link for link, own, other in hybrid_pairs(classes, hero) if link in saved and own and other]
    return valid[:hybrid_max(balance)]


def toggle_hybrid(classes: dict[str, Any], balance: dict[str, Any], hero: Hero, link: str) -> bool:
    """Swap one role slot for the other role's same slot, or put the own one back. Returns True if done.

    [ES]
    Qué hace: cambia un puesto (H1, H2 o H3) por el del mismo puesto de tu otro rol, o lo devuelve al tuyo, y lo guarda en
    hero.hybrid (por pareja de roles). Gratis; el servicio no lo deja en combate. No hace nada si el modo está cerrado, si
    ese puesto no tiene pareja o si ya hay chain.hybrid.max_mixed cambiados.
    La llaman: el servicio (botones de la pantalla 🔀 Modo híbrido).
    Si cambia, afecta: la barra de combate del héroe (chain_bar, kit).
    """
    if link not in HYBRID_LINKS or not hybrid_open(classes, balance, hero):
        return False
    _link, own, other = next(p for p in hybrid_pairs(classes, hero) if p[0] == link)
    if not (own and other):
        return False
    current = hybrid_choice(classes, balance, hero)
    if link in current:
        current.remove(link)
    elif len(current) >= hybrid_max(balance):
        return False
    else:
        current.append(link)
    key = hybrid_key(classes, hero) or ""
    saved = dict(hero.hybrid or {})
    ordered = [slot for slot in HYBRID_LINKS if slot in current]
    if ordered:
        saved[key] = ordered
    else:
        saved.pop(key, None)                   # back to the role's own bar: nothing saved (as a hero who never touched it)
    hero.hybrid = saved
    return True


def chain_bar(classes: dict[str, Any], balance: dict[str, Any] | None, hero: Hero) -> list[dict[str, Any]]:
    """The 3 role buttons a chain hero fights with (H1, H2, H3): its active role's, with the hybrid swaps applied.

    [ES]
    Qué hace: la barra de combate de las clases nuevas. Sin modo híbrido (o sin balance) son los 3 botones del rol activo, como
    siempre. Con él, cada puesto cambiado lleva la habilidad del mismo puesto del otro rol tal cual está en classes.yaml (sus
    números y sus marcas: daño, curación, agro, escuela), marcada con from_spec (el rol de donde viene). El puesto (link)
    no cambia, así que la cadena y el orden siguen siendo los del rol activo.
    La llaman: bar() (y por ella kit(), o sea todo el combate). Si cambia, afecta: qué hace cada botón en combate.
    """
    own = list(classes[hero.class_id]["abilities"])
    swapped = hybrid_choice(classes, balance, hero) if balance is not None else []
    if not swapped:
        return own
    partner = hybrid_partner(classes, hero) or ""
    out = []
    for ability in own:
        other = _in_slot(classes[partner], ability.get("link", "")) if ability.get("link") in swapped else None
        if other:
            borrowed = copy.deepcopy(other)
            borrowed["from_spec"] = partner    # the view says where it comes from; the combat reads only the ability itself
            out.append(borrowed)
        else:
            out.append(ability)
    return out


def spend_point(classes: dict[str, Any], balance: dict[str, Any], hero: Hero, spec: str) -> list[str]:
    """Put one point in a spec of the hero's class; returns newly unlocked ability ids.

    [ES]
    Qué hace: gasta un punto en una especialización, desbloquea habilidades y actualiza la
    especialización principal.
    La llaman: el servicio (botón ➕) y la migración de héroes viejos.
    Si cambia, afecta: el poder de cada héroe.
    """
    group = _group(classes, hero)
    if is_chain_spec(classes, hero.class_id):      # 0.31: the points place themselves (sync_chain); a call just uses one up
        hero.points = max(0, hero.points - 1)
        return []
    if hero.points <= 0 or spec not in specs_of(classes, group):
        return []
    hero.points -= 1
    hero.talents[spec] = hero.talents.get(spec, 0) + 1
    new = _unlock_spec(classes, balance, hero, spec)
    best = max(hero.talents.items(), key=lambda kv: kv[1])
    if best[1] > hero.talents.get(hero.class_id, 0):
        hero.class_id = best[0]
    return new


def _is_response(ability: dict[str, Any]) -> bool:
    return ability["kind"] == "response"


def _known_unlocked(classes: dict[str, Any], hero: Hero) -> tuple[dict[str, tuple[str, int, dict[str, Any]]], list[str]]:
    known = _abilities(classes, _group(classes, hero))
    return known, [a for a in dict.fromkeys(hero.unlocked) if a in known]


DAMAGE_KINDS = ("strike", "finisher", "dot")


HEAL_FIRST_ROLES = ("defensa",)    # D-110: a tank's automatic bar keeps a heal in slot 3


def _auto_slots(known: dict[str, Any], unlocked: list[str], role: str | None = None) -> list[str]:
    """Automatic bar: newest response, newest damage ability (strike, finisher or dot), newest other one.

    D-110: for Defensa the third slot is the newest heal when one is unlocked (a tank whose
    automatic bar dropped its heal for a newer utility could not hold out, which is its role).
    """
    responses = [a for a in unlocked if _is_response(known[a][2])]
    if not responses:
        return unlocked[-3:]
    chosen = [responses[-1]]
    damage = [a for a in unlocked if known[a][2]["kind"] in DAMAGE_KINDS]
    if damage:
        chosen.append(damage[-1])
    heals = [a for a in unlocked if known[a][2]["kind"] == "heal" and a not in chosen]
    if role in HEAL_FIRST_ROLES and heals:
        chosen.append(heals[-1])
    for pool in ([a for a in unlocked if not _is_response(known[a][2])], unlocked):
        for ability_id in reversed(pool):
            if len(chosen) < 3 and ability_id not in chosen:
                chosen.append(ability_id)
    return chosen


def bar_slots(classes: dict[str, Any], hero: Hero, balance: dict[str, Any] | None = None) -> list[str]:
    """Ability ids of the bar, slot 1 first (slot 1 = a response).

    [ES]
    Qué hace: devuelve la barra en uso: la que eligió el jugador (hero.bar) si sigue valiendo; si no,
    la automática (casilla 1 = la respuesta más nueva, casilla 2 = el golpe más nuevo, casilla 3 = la otra
    habilidad más nueva; D-110: en Defensa, la curación más nueva, si ya abrió alguna).
    Si la barra elegida tiene casillas vacías y hay habilidades libres, las llena con las últimas.
    En las clases nuevas (0.31) son H1, H2 y H3 del rol activo; con balance, con los cambios del modo híbrido (0.54).
    La llaman: bar(), el servicio (pantalla 🎛️ Barra de combate) y set_bar_slot().
    Si cambia, afecta: qué botones salen en combate y en qué orden.
    """
    if is_chain_spec(classes, hero.class_id):      # 0.31: H1, H2, H3 (the Básico is ⚔️); 0.54: the hybrid swaps (D-312)
        return [a["id"] for a in chain_bar(classes, balance, hero)]
    known, unlocked = _known_unlocked(classes, hero)
    auto = _auto_slots(known, unlocked, classes.get(hero.class_id, {}).get("role"))
    saved = list(hero.bar or [])
    has_response = any(_is_response(known[a][2]) for a in unlocked)
    valid = (
        bool(saved)
        and len(saved) <= 3
        and len(set(saved)) == len(saved)
        and all(a in unlocked for a in saved)
        and (not has_response or _is_response(known[saved[0]][2]))
    )
    if not valid:
        return auto
    latest = list(reversed(unlocked))
    for ability_id in [a for a in latest if not _is_response(known[a][2])] + latest:
        if len(saved) >= min(3, len(unlocked)):
            break
        if ability_id not in saved:
            saved.append(ability_id)
    return saved


def bar(classes: dict[str, Any], hero: Hero, balance: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """The (up to) 3 abilities in use, slot 1 first.

    [ES]
    Qué hace: arma la barra de 3 habilidades (ver bar_slots); la casilla 1 es siempre una respuesta. En las clases nuevas,
    los 3 botones de rol (chain_bar): con balance, con lo que cambió el modo híbrido; sin balance, los del rol tal cual.
    La llaman: kit() (con balance: así pelea el héroe) y la vista del héroe.
    Si cambia, afecta: qué botones salen en combate.
    """
    if is_chain_spec(classes, hero.class_id):
        return chain_bar(classes, balance, hero)
    known = _abilities(classes, _group(classes, hero))
    return [known[a][2] for a in bar_slots(classes, hero)]


def bar_choices(classes: dict[str, Any], hero: Hero, slot: int) -> list[str]:
    """Unlocked ability ids that can go in a bar slot (1-3), excluding what is already there.

    [ES]
    Qué hace: lista lo que se puede poner en una casilla: en la 1, solo respuestas; en la 2 y la 3,
    cualquier otra habilidad desbloqueada que no esté en la casilla 1.
    La llaman: el servicio (pantalla para elegir casilla).
    Si cambia, afecta: qué opciones ve el jugador.
    """
    if is_chain_spec(classes, hero.class_id):      # 0.31: no free picking; 0.54: the hybrid mode swaps whole slots (toggle_hybrid)
        return []
    known, unlocked = _known_unlocked(classes, hero)
    slots = bar_slots(classes, hero)
    current = slots[slot - 1] if 0 < slot <= len(slots) else None
    if slot == 1:
        return [a for a in unlocked if _is_response(known[a][2]) and a != current]
    first = slots[0] if slots else None
    return [a for a in unlocked if a not in (current, first)]


def set_bar_slot(classes: dict[str, Any], hero: Hero, slot: int, ability_id: str) -> bool:
    """Put an unlocked ability in a slot (1-3); swaps if it already sits in another slot. Returns True if done.

    [ES]
    Qué hace: guarda la elección del jugador en hero.bar. Si la habilidad ya estaba en otra casilla,
    las cambia de lugar. Nunca deja la casilla 1 sin respuesta.
    La llaman: el servicio (botones de la pantalla 🎛️ Barra de combate).
    Si cambia, afecta: la barra guardada de cada héroe.
    """
    if not 1 <= slot <= 3 or ability_id not in bar_choices(classes, hero, slot):
        return False
    slots = bar_slots(classes, hero)
    if slot > len(slots):
        slots.append(ability_id)
    else:
        old = slots[slot - 1]
        if ability_id in slots:
            slots[slots.index(ability_id)] = old
        slots[slot - 1] = ability_id
    hero.bar = slots
    return True


def kit(classes: dict[str, Any], balance: dict[str, Any], hero: Hero) -> dict[str, Any]:
    """Effective class definition for combat and stats: main spec + bar + passive bonuses.

    [ES]
    Qué hace: devuelve la "clase efectiva" del héroe: recurso y estadísticas de su especialización
    principal, su barra de habilidades y las mejoras pasivas de sus puntos. En las clases nuevas la barra trae los cambios
    del 🔀 modo híbrido (0.54, D-330): la habilidad prestada usa sus propios números y el cuerpo es el del rol activo
    (vida, ataque, armadura, iniciativa y la mejora pasiva de sus puntos).
    La llaman: el servicio (combate, vida máxima, vistas).
    Si cambia, afecta: todo el combate del héroe.
    """
    base = copy.deepcopy(classes[hero.class_id])
    base["abilities"] = bar(classes, hero, balance)
    cfg = balance["talents"]
    bonus = {"attack": 0.0, "hp": 0.0}
    talents = hero.talents
    if is_chain_spec(classes, hero.class_id):      # 0.31: one point per level, all in the active role (sync_chain)
        talents = {hero.class_id: max(0, hero.level - 1)}
    for spec, points in talents.items():
        role = classes.get(spec, {}).get("role", "ataque")
        for stat, per_point in cfg["passive"].get(role, {}).items():
            bonus[stat] = bonus.get(stat, 0.0) + per_point * min(points, cfg["passive_cap"])
    base["talent_bonus"] = bonus
    return base
