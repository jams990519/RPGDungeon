"""The wall's harvest (D-309, confirmed; how: D-325, provisional): the land a camp's wall closes yields by itself.

With the 🧱 Muralla built, every zone of the camp's territory yields `share` of what each of its resources regrows per day,
into the camp's 💰 fund (never into a backpack). What it yields piles up lazily, like the zone stock: the service keeps
{"pile": {item: float}, "at": ts} and every settle adds rate × elapsed days, never more than `cap_days` days of each
resource. Once a week the whole units go to the fund (if a member played that week) and the fractions stay for the next.
These helpers are pure: the service reads the store, finds the zones and their resources, and calls them.

[ES]
Para qué sirve: las cuentas de la 🌾 cosecha de la muralla (pedido del dueño del 17-oct-2026, D-254; números confirmados el
    20-oct, D-309): cuánto da por día cada recurso del territorio cerrado, cuánto se junta con el tiempo (con su tope de 7
    días) y qué parte entera pasa al fondo. Cada zona da el 20 % de lo que vuelve a crecer cada uno de sus recursos;
    "lo que vuelve a crecer" sale de content/balance.yaml stock (D-325: sin el ×3 de la 0.42 mientras harvest.real_regen
    sea false). La cosecha no baja el recurso de la zona: quien recolecta a mano ahí encuentra lo mismo (escalera §5.4.5).
Documento de diseño: diseno/09-construccion/escalera-del-asentamiento.md §5 (§5.5: cómo quedó en el juego)
Módulo: M9 Frontera y Fundación (vive en engine/world hasta que exista engine/front), con M24 Construcción (la muralla)
Depende de: ninguno (los números llegan de content/balance.yaml, bloques harvest y stock)
Lo usan: engine/service/game.py (_harvest_rate, _harvest_state, _harvest_deliver, _harvest_tick, _harvest_line) y
    tools/camp_costs.py (el ritmo hasta castillo con la cosecha)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno (el servicio guarda la cosecha en "upgrades"/<x:y> → "harvest")
Reglas que nunca se rompen:
    1. Lo guardado nunca pasa de cap_days días de cosecha de cada recurso, ni baja de 0.
    2. Solo pasan al fondo unidades enteras; lo que sobra (la fracción) se queda para la semana siguiente (el servicio la
       guarda aparte, en "carry", fuera del tope: nunca se pierde).
    3. La cosecha sale de lo que vuelve a crecer, no del recurso que hay: estas cuentas no tocan el stock de las zonas.
Si cambias esto, revisa:
    - Servicio: engine/service/game.py (sección "🌾 the wall's harvest") y lo que muestra (⬆️ Mejorar, 💰 Fondos, ℹ️ Información)
    - Números: balance.yaml harvest (share, real_regen, week_days, cap_days, active_days) y stock (regen_per_hour, per_unit,
      regen_mult)
    - Pruebas: tests/test_cosecha_muralla.py; el ritmo hasta castillo: tools/camp_costs.py y tests/test_costos_edificios.py
"""

from __future__ import annotations

from typing import Iterable, Mapping


def regrow_per_day(stock: Mapping[str, object], resource: str, real: bool = False, well: float = 0.0) -> float:
    """Units of `resource` a zone regrows per day: stock.regen_per_hour × 24 ÷ stock.per_unit (24 with today's numbers).

    [ES]
    Qué hace: dice cuántas unidades de un recurso vuelven a crecer en una zona por día. Con real=False (D-325, lo de hoy),
    la cuenta de base: un 2 % por hora y cada unidad vale un 2 % → 24 por día, el número de la pregunta del dueño (E-216).
    Con real=True, lo que vuelve de verdad: × stock.regen_mult del recurso (×3 los 6 de base desde la 0.42) y × (1 + well),
    el ⛲ Pozo del campamento (stock_regen). La llaman: daily_rate. Si cambia, afecta: cuánto cosecha cada zona.
    """
    per_unit = float(stock.get("per_unit", 0.02) or 0.02)
    per_hour = float(stock.get("regen_per_hour", 0.0) or 0.0)
    units = per_hour * 24 / per_unit
    if real:
        mult = stock.get("regen_mult") or {}
        units *= float(mult.get(resource, 1.0)) * (1.0 + max(0.0, well))   # type: ignore[union-attr]
    return units


def daily_rate(zones: Iterable[Iterable[str]], stock: Mapping[str, object], share: float, real: bool = False,
               well: float = 0.0) -> dict[str, float]:
    """What the closed zones yield per day, per resource: share × what each resource of each zone regrows.

    [ES]
    Qué hace: suma, para cada zona cerrada, el `share` (20 %) de lo que vuelve a crecer cada uno de sus recursos por día.
    `zones` es una lista con los recursos de cada zona (ya filtrados: solo los que el fondo recibe). La llaman: el servicio
    (_harvest_rate) y tools/camp_costs.py. Si cambia, afecta: lo que llega al 💰 fondo cada semana.
    """
    rate: dict[str, float] = {}
    for resources in zones:
        for res in resources:
            rate[res] = rate.get(res, 0.0) + max(0.0, share) * regrow_per_day(stock, res, real, well)
    return rate


def accrue(pile: Mapping[str, float], rate: Mapping[str, float], days: float, cap_days: float) -> dict[str, float]:
    """The pile after `days` more days of harvest, each resource capped at cap_days days of its rate (rule 1).

    [ES]
    Qué hace: suma lo cosechado en el tiempo que pasó, sin pasar de cap_days (7) días de cada recurso. Lo que ya estaba de
    un recurso que hoy no se cosecha (por ejemplo, una zona que ya no cuenta) queda como estaba, nunca crece. La llaman:
    el servicio (_harvest_state). Si cambia, afecta: cuánto se guarda y el tope de 7 días.
    """
    out = {item: max(0.0, float(n)) for item, n in pile.items()}
    days = max(0.0, float(days))
    for item, per_day in rate.items():
        cap = max(0.0, float(per_day)) * max(0.0, float(cap_days))
        before = out.get(item, 0.0)
        out[item] = before if before >= cap else min(cap, before + max(0.0, float(per_day)) * days)   # over the cap: it waits
    return {item: n for item, n in out.items() if n > 0}


def split_units(pile: Mapping[str, float]) -> tuple[dict[str, int], dict[str, float]]:
    """(whole units for the fund, fractions kept for the next week) of a pile (rule 2).

    [ES]
    Qué hace: separa lo guardado en unidades enteras (van al 💰 fondo) y lo que sobra de cada recurso (menos de 1: queda
    para la semana siguiente). La llaman: el servicio (_harvest_deliver). Si cambia, afecta: lo que llega al fondo.
    """
    units = {item: int(n) for item, n in pile.items() if int(n) > 0}
    rest = {item: float(n) - int(n) for item, n in pile.items() if float(n) - int(n) > 1e-9}
    return units, rest
