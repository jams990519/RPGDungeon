"""Hunting party of a player camp (D-106, provisional): the pure rules.

Simple layer: a camp member calls a party in the zone where they are; camp members present there can join.
For a window (balance hunt.party.minutes) every hunt victory of a member in that zone gets a group bonus
(more xp and loot chance per companion present) and adds to a shared tally of prey. When the window ends the
service closes it lazily (when a camp member plays), sends a report and, if the tally reached the target,
pays a small reward. Combat stays 1 vs 1: "going together" means hunting in the same zone at the same time.
These helpers are pure: the service reads the store, finds who is present and calls them.

[ES]
Para qué sirve: las cuentas de la 🏹 Partida de caza de un campamento de jugadores: el bono de grupo por
compañero presente (con tope), la meta de presas según cuántos cazadores se unieron, si se ganó el premio
del final y la cuenta de presas de cada cazador.
Documento de diseño: diseno/06-contenido/cacerias.md §0 (D-106, provisional)
Módulo: M15 Social (la cacería en sí es de M10 Misiones; su código vive en engine/service/game.py)
Depende de: ninguno (los números llegan de content/balance.yaml, bloque hunt.party)
Lo usan: engine/service/game.py (sección "hunting": _call_hunt_party, _join_hunt_party, _hunt_bonus,
    _hunt_fight_done, _hunt_party_settle)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno (el servicio guarda la partida abierta en el espacio "hunt_party", clave "x:y"
    del campamento: {"x", "y", "at", "until", "caller", "members": {héroe: presas}, "prey"})
Reglas que nunca se rompen:
    1. El bono nunca pasa del tope, y sin compañeros presentes es 0: cazar solo rinde lo de siempre.
    2. Una partida de menos de min_hunters cazadores nunca da el premio del final.
    3. La meta nunca baja de prey_per_hunter × min_hunters, aunque se haya unido uno solo.
Si cambias esto, revisa:
    - Servicio: engine/service/game.py (sección "hunting" y _end_combat, que aplica el bono a la experiencia y al botín)
    - Números: balance.yaml hunt.party (bonus_per_companion, bonus_cap, prey_per_hunter, min_hunters, reward)
    - Pruebas: tests/test_hunt.py
"""

from __future__ import annotations

from typing import Any


def party_bonus(companions: int, per_companion: float, cap: float) -> float:
    """Group bonus of one hunt victory: per_companion for each companion present, never above cap.

    [ES]
    Qué hace: el bono de grupo de una presa (+10 % por compañero presente, tope +30 % con los números de hoy).
    Se suma a la experiencia y a la probabilidad de botín de esa pelea, nunca a las monedas.
    La llama: el servicio (_hunt_bonus) al ganar una pelea de cacería.
    Si cambia, afecta: cuánto conviene cazar en grupo frente a cazar solo.
    """
    return max(0.0, min(float(cap), max(0, int(companions)) * float(per_companion)))


def party_target(hunters: int, per_hunter: int, min_hunters: int) -> int:
    """Prey the whole party needs for the final reward: per_hunter × hunters (at least min_hunters of them).

    [ES]
    Qué hace: la meta de presas entre todos: 3 por cazador que se unió, contando como mínimo a 2 cazadores.
    La llaman: el servicio (pantalla de cacería, aviso de la partida y cierre).
    Si cambia, afecta: qué tan fácil es el premio del final para una partida chica o grande.
    """
    return max(1, int(per_hunter)) * max(int(min_hunters), int(hunters))


def add_prey(party: dict[str, Any], hero_id: str) -> None:
    """Count one prey for a member of the party (and for the shared tally).

    [ES]
    Qué hace: suma 1 presa al cazador y 1 a la cuenta de la partida. El llamador guarda la partida.
    La llama: el servicio (_hunt_fight_done) al ganar una pelea de cacería en la zona de la partida.
    Si cambia, afecta: el informe del final y si se llega a la meta.
    """
    members = party.setdefault("members", {})
    members[hero_id] = int(members.get(hero_id, 0)) + 1
    party["prey"] = int(party.get("prey", 0)) + 1


def reward_earned(party: dict[str, Any], per_hunter: int, min_hunters: int) -> bool:
    """True if the party had enough hunters and reached its target.

    [ES]
    Qué hace: dice si la partida gana el premio del final (al menos min_hunters cazadores y la meta cumplida).
    La llama: el servicio al cerrar la partida.
    Si cambia, afecta: quién cobra el premio de la partida.
    """
    hunters = len(party.get("members", {}))
    return hunters >= int(min_hunters) and int(party.get("prey", 0)) >= party_target(hunters, per_hunter, min_hunters)


def rewarded(party: dict[str, Any]) -> list[str]:
    """Members who hunted at least one prey (only they get the final reward).

    [ES]
    Qué hace: la lista de cazadores con al menos 1 presa: los que cobran el premio si se cumplió la meta.
    Así unirse sin cazar no cobra nada.
    La llama: el servicio al cerrar la partida.
    Si cambia, afecta: quién cobra el premio de la partida.
    """
    return [hero_id for hero_id, prey in party.get("members", {}).items() if int(prey) > 0]
