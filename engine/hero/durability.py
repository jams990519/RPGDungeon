"""Gear durability (D-139, confirmed; how it was applied: D-333, provisional; 0.57): wear, damage, repairs and the final break.

Every gear piece (weapons, armor, jewels: items.yaml kind "gear"; never consumables, bags or chests) has its own durability
record {"id": item id, "cur": current, "max": maximum, "rep": repairs done}. A piece nobody used yet has no record at all:
it counts as new (durability.max over durability.max, 0 repairs), so every piece of before 0.57 starts full and nobody loses
anything on patch day (D-64). The worn pieces keep their record by slot (Hero.gear_wear); the used copies in the backpack
keep theirs by item id (Hero.bag_wear, one record per used copy; the copies without a record are new).

Every fight lowers the durability of each worn piece (durability.wear: a little on a win, more when fleeing, the most on a
defeat). At 0 the piece is "damaged": it stays worn and in the backpack but gives no stats until it is repaired (never
deleted at 0). A repair puts it back to its maximum and lowers that maximum (durability.repair_loss); after
durability.repairs repairs (durability.masterwork_repairs for a ✒️ masterwork) the piece lives its last life: the next time
it reaches 0 it breaks for ever (the only way a piece leaves by game rule; the screens warn before the last repair).

[ES]
Para qué sirve: las cuentas puras del desgaste del equipo que pidió el dueño (D-139, E-23: "el equipo se gasta, se repara y un
    día se rompe, con una duración generosa que dé trabajo a los artesanos"). Cómo se aplicó lo eligió Claude en la capa
    simple (D-44): D-333, provisional, con la recomendación de E-70 (P-93: unas 3 semanas de juego diario por reparación y
    se rompe tras unas 5 reparaciones, unos 4 meses). Sin pantallas ni textos: eso está en engine/service/repair.py.
Documento de diseño: diseno/03-personaje/equipamiento.md §4 (y §11, lo que está en el juego); diseno/07-economia/profesiones.md
    §0.12 (quién repara)
Módulo: M4 Equipo e inventario (en el código, junto al equipo del héroe: engine/hero)
Depende de: content/balance.yaml (bloque durability), content/items.yaml (kind, type, req_level, price, masterwork)
Lo usan: engine/hero/gear.py (gear_bonus no suma una pieza dañada; is_better la cuenta en 0; equip y unequip llevan el
    registro de cada copia), engine/service/repair.py (desgaste al terminar una pelea, reparar, encargos), engine/service/game.py
    (_forget_piece: sync_bag; las vistas de equipo), engine/service/market.py y engine/service/gremio.py (la durabilidad viaja
    con cada pieza en el 🏛️ Mercado y la ⚔️ Armería: take_copies, take_worst, put_back)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: Hero.gear_wear (ranura -> registro de la pieza puesta) y Hero.bag_wear (id de pieza -> registros
    de las copias usadas de la mochila). Un registro: {"id", "cur", "max", "rep"}. Sin registro = pieza nueva.
Reglas que nunca se rompen:
    1. Una pieza sin registro está nueva y llena (durability.max). Nadie pierde nada el día del parche (D-64).
    2. En 0 la pieza queda dañada: sigue puesta y en la mochila, no da bonos y nunca se borra. Solo se rompe (y sale del
       juego) si llega a 0 cuando ya no le quedan reparaciones (wear_fight devuelve "broken").
    3. Lo que sale de la mochila sale primero la copia más gastada (take_worst, sync_bag); lo que se pone, la mejor
       (take_best). Así vender o dejar una pieza nunca empeora la que te queda.
    4. Solo las piezas puestas se gastan; las de la mochila guardan su registro tal cual.
Si cambias esto, revisa:
    - Números: balance.yaml durability (max, wear, low_pct, repair_loss, repairs, masterwork_repairs, rank_margin, material,
      material_step, energy, xp, npc_mult, order_mult, order_days, repair_by); el registro de balance
      (diseno/03-personaje/balance.md, "el equipo se gasta") y la cascada C-36 del mapa de impacto
    - El combate no lee esto directo: lo lee gear_bonus (engine/hero/gear.py). tools/sim.py y tools/balance_report.py arman
      héroes sin registros: rinden igual que antes (equipo lleno)
    - Pruebas: tests/test_desgaste_reparacion.py
"""

from __future__ import annotations

import math
from typing import Any

# Fight outcome -> the key of balance.yaml durability.wear. [ES] Resultado de la pelea -> clave del desgaste.
OUTCOME_WEAR = {"victory": "win", "defeat": "defeat"}
EPS = 1e-6


def cfg(balance: dict[str, Any]) -> dict[str, Any]:
    """balance.yaml "durability" ({} if missing: then nothing ever wears). [ES] El bloque de números; sin él, nada se gasta."""
    return balance.get("durability") or {}


def wears(item: dict[str, Any] | None) -> bool:
    """True for a piece that has durability: any items.yaml kind "gear" (weapons, armor, jewels). [ES] Solo el equipo."""
    return bool(item) and item.get("kind") == "gear"


def start_max(balance: dict[str, Any]) -> float:
    """The durability of a new piece (durability.max, 100). [ES] La durabilidad de una pieza nueva."""
    return float(cfg(balance).get("max", 100))


def new_record(item_id: str, balance: dict[str, Any]) -> dict[str, Any]:
    """A new piece's record: full, never repaired. [ES] El registro de una pieza nueva: llena y sin reparar."""
    full = start_max(balance)
    return {"id": item_id, "cur": full, "max": full, "rep": 0}


def is_new(rec: dict[str, Any] | None, balance: dict[str, Any]) -> bool:
    """True if a record says nothing a new piece would not (full, its first maximum, never repaired); None counts as new."""
    if not rec:
        return True
    full = start_max(balance)
    return float(rec.get("cur", full)) >= full - EPS and float(rec.get("max", full)) >= full - EPS and int(rec.get("rep", 0)) == 0


def worn_record(hero: Any, slot: str, balance: dict[str, Any]) -> dict[str, Any] | None:
    """A copy of the record of the piece worn in a slot (a new one if it has none); None if nothing is worn there.

    [ES] Qué hace: da el registro de la pieza puesta en esa ranura (uno nuevo si no tiene). Si el registro guardado es de otra
    pieza (alguien cambió Hero.gear sin pasar por equip), cuenta como nueva: nunca se le pasa el desgaste de otra.
    La llaman: gear.py (slot_damaged), repair.py y las vistas. Si cambia, afecta: qué durabilidad se ve y se usa."""
    item_id = (getattr(hero, "gear", None) or {}).get(slot)
    if not item_id:
        return None
    rec = (getattr(hero, "gear_wear", None) or {}).get(slot)
    if not rec or rec.get("id") != item_id:
        return new_record(item_id, balance)
    return dict(rec)


def set_worn(hero: Any, slot: str, rec: dict[str, Any] | None, balance: dict[str, Any]) -> None:
    """Keep the record of the piece worn in `slot` (a new one is not kept: no record = new). [ES] Guarda el registro puesto."""
    if rec is None or is_new(rec, balance):
        hero.gear_wear.pop(slot, None)
    else:
        hero.gear_wear[slot] = dict(rec)


def damaged(rec: dict[str, Any] | None) -> bool:
    """True when the durability is 0: the piece gives no stats until it is repaired. [ES] Pieza dañada (en 0)."""
    return bool(rec) and float(rec.get("cur", 1.0)) <= EPS


def slot_damaged(hero: Any, slot: str, balance: dict[str, Any]) -> bool:
    """True if the piece worn in `slot` is damaged (0 durability). [ES] Dice si la pieza puesta en esa ranura está dañada.
    La llaman: gear_bonus e is_better (engine/hero/gear.py) y las vistas. Si cambia, afecta: los bonos en combate."""
    return damaged(worn_record(hero, slot, balance))


def shown(value: float) -> int:
    """The whole number players see: rounded up, so it says 0 only when the piece really is at 0. [ES] El número que se ve."""
    return max(0, int(math.ceil(float(value) - EPS)))


def max_repairs(item: dict[str, Any], balance: dict[str, Any]) -> int:
    """How many repairs a piece takes before its last life: durability.repairs, or masterwork_repairs for a ✒️ masterwork."""
    c = cfg(balance)
    if item.get("masterwork"):
        return int(c.get("masterwork_repairs", c.get("repairs", 5)))
    return int(c.get("repairs", 5))


def repairs_left(rec: dict[str, Any] | None, item: dict[str, Any], balance: dict[str, Any]) -> int:
    """How many more repairs the piece takes (0 = its last life: at 0 it breaks). [ES] Cuántas reparaciones le quedan."""
    return max(0, max_repairs(item, balance) - int((rec or {}).get("rep", 0)))


def low_line(rec: dict[str, Any], balance: dict[str, Any]) -> float:
    """The durability under which a piece counts as worn out (durability.low_pct of its maximum). [ES] El umbral del aviso."""
    return float(rec.get("max", start_max(balance))) * float(cfg(balance).get("low_pct", 0.2))


def is_low(rec: dict[str, Any] | None, balance: dict[str, Any]) -> bool:
    """True when a piece is worn out (at or under low_pct of its maximum) but not yet damaged. [ES] Pieza gastada (⚠️)."""
    return bool(rec) and not damaged(rec) and float(rec.get("cur", 0.0)) <= low_line(rec, balance) + EPS


def needs_repair(rec: dict[str, Any] | None) -> bool:
    """True if the piece is below its maximum (a repair would give something back). [ES] Dice si le falta durabilidad."""
    return bool(rec) and float(rec.get("cur", 0.0)) < float(rec.get("max", 0.0)) - EPS


def fight_loss(balance: dict[str, Any], outcome: str | None) -> float:
    """What one fight takes from each worn piece: durability.wear win, defeat or flee (any other end). [ES] Desgaste por pelea."""
    wear = cfg(balance).get("wear") or {}
    return float(wear.get(OUTCOME_WEAR.get(outcome or "", "flee"), 0.0))


def wear_fight(hero: Any, items: dict[str, Any], balance: dict[str, Any], outcome: str | None) -> list[tuple[str, str, str]]:
    """Wear every worn piece after a fight; returns the news as (slot, item id, "low" | "damaged" | "broken").

    "low": it just went at or under low_pct of its maximum; "damaged": it just reached 0 and still takes repairs (it stays worn,
    without stats); "broken": it reached 0 in its last life and was taken off and destroyed (hero.gear and hero.gear_wear lose
    it; the caller forgets its ✨ and ✒️ if it was the last copy). An already damaged piece loses nothing more.

    [ES]
    Qué hace: gasta cada pieza puesta según cómo terminó la pelea (balance.yaml durability.wear: ganar, huir o perder) y dice
    qué pasó: "low" (acaba de quedar gastada, el aviso del 20 %), "damaged" (llegó a 0: sigue puesta, sin bonos) o "broken"
    (llegó a 0 sin reparaciones: se rompe y sale del equipo). Una pieza ya dañada no pierde más.
    La llama: engine/service/repair.py _wear_after_fight (desde _end_combat: toda pelea, a mano o automática).
    Si cambia, afecta: cuánto dura cada pieza, cuándo se avisa y cuándo se rompe (registro de balance, C-36).
    """
    loss = fight_loss(balance, outcome)
    news: list[tuple[str, str, str]] = []
    if loss <= 0:
        return news
    for slot, item_id in list((hero.gear or {}).items()):
        if not wears(items.get(item_id)):
            continue
        rec = worn_record(hero, slot, balance)
        if rec is None or damaged(rec):
            continue
        before = float(rec["cur"])
        after = round(max(0.0, before - loss), 4)
        rec["cur"] = after
        if after <= EPS:
            if repairs_left(rec, items[item_id], balance) <= 0:
                hero.gear.pop(slot, None)
                hero.gear_wear.pop(slot, None)
                news.append((slot, item_id, "broken"))
                continue
            news.append((slot, item_id, "damaged"))
        elif before > low_line(rec, balance) + EPS >= after:
            news.append((slot, item_id, "low"))
        set_worn(hero, slot, rec, balance)
    return news


def _quality(rec: dict[str, Any]) -> tuple[float, float, int]:
    """How good a used copy is: more durability first, then a higher maximum, then fewer repairs."""
    return (float(rec.get("cur", 0.0)), float(rec.get("max", 0.0)), -int(rec.get("rep", 0)))


def take_best(hero: Any, item_id: str, balance: dict[str, Any]) -> dict[str, Any] | None:
    """Take the best copy of a piece out of the backpack's records (call it BEFORE the backpack loses the unit): None = a new
    copy (there is one without a record), else the best used record (removed from Hero.bag_wear).

    [ES] Qué hace: elige la copia que se pone: una nueva si la hay; si no, la usada con más durabilidad. La llama: equip (gear.py).
    Si cambia, afecta: qué copia te pones cuando tienes varias."""
    used = list((hero.bag_wear or {}).get(item_id) or [])
    if len(used) < int((hero.backpack or {}).get(item_id, 0)):
        return None
    if not used:
        return None
    best = max(range(len(used)), key=lambda i: _quality(used[i]))
    rec = used.pop(best)
    _keep_bag(hero, item_id, used)
    return dict(rec)


def take_worst(hero: Any, item_id: str) -> dict[str, Any] | None:
    """Take the most worn copy of a piece out of the backpack's records (call it BEFORE the backpack loses the unit): the worst
    used record, or None if every copy is new.

    [ES] Qué hace: elige la copia que sale de la mochila (vender, el mercado, la armería, desencantar): la más gastada. La llaman:
    take_copies, la ⚔️ Armería y sync_bag (por la misma regla). Si cambia, afecta: qué copia te queda."""
    used = list((hero.bag_wear or {}).get(item_id) or [])
    if not used:
        return None
    worst = min(range(len(used)), key=lambda i: _quality(used[i]))
    rec = used.pop(worst)
    _keep_bag(hero, item_id, used)
    return dict(rec)


def take_copies(hero: Any, item_id: str, n: int) -> list[dict[str, Any] | None]:
    """The records of `n` copies leaving the backpack, the most worn first (None = a new copy). [ES] Para el 🏛️ Mercado."""
    return [take_worst(hero, item_id) for _ in range(max(0, int(n)))]


def put_back(hero: Any, item_id: str, rec: dict[str, Any] | None, balance: dict[str, Any]) -> None:
    """A copy came into the backpack with this record (None or a new record keeps nothing: it is a new copy).

    [ES] Qué hace: guarda el registro de una copia que entra a la mochila (al quitártela, al comprarla o al tomarla de la
    armería). La llaman: unequip y equip (gear.py), el mercado y la armería. Si cambia, afecta: la durabilidad que viaja."""
    if rec is None or is_new(rec, balance):
        return
    used = list((hero.bag_wear or {}).get(item_id) or [])
    used.append({**dict(rec), "id": item_id})
    _keep_bag(hero, item_id, used)


def sync_bag(hero: Any) -> None:
    """Keep at most one record per copy in the backpack: when copies left by any road, the most worn records go with them.

    [ES] Qué hace: deja en Hero.bag_wear como mucho un registro por copia que queda en la mochila; si salió una copia por
    cualquier camino (vender al mercader, desencantar…), se va el registro más gastado (regla 3). La llama: _forget_piece
    (game.py), que corre después de cada salida de una pieza. Si cambia, afecta: qué copia te queda al vender."""
    for item_id in list((hero.bag_wear or {}).keys()):
        used = list(hero.bag_wear.get(item_id) or [])
        keep = max(0, int((hero.backpack or {}).get(item_id, 0)))
        if len(used) > keep:
            used.sort(key=_quality, reverse=True)
            used = used[:keep]
        _keep_bag(hero, item_id, used)


def _keep_bag(hero: Any, item_id: str, used: list[dict[str, Any]]) -> None:
    if used:
        hero.bag_wear[item_id] = used
    else:
        hero.bag_wear.pop(item_id, None)


def best_in_bag(hero: Any, item_id: str, balance: dict[str, Any]) -> dict[str, Any] | None:
    """The record of the copy equip would take (a new one if there is one), without taking it; None if none in the backpack."""
    count = int((hero.backpack or {}).get(item_id, 0))
    if count <= 0:
        return None
    used = list((hero.bag_wear or {}).get(item_id) or [])
    if len(used) < count:
        return new_record(item_id, balance)
    return dict(max(used, key=_quality))


def repaired(rec: dict[str, Any], balance: dict[str, Any]) -> dict[str, Any]:
    """The record after one repair: the maximum goes down by durability.repair_loss and the piece is full again at it.

    [ES] Qué hace: repara: baja el máximo (balance.yaml durability.repair_loss), llena hasta ese máximo y suma una reparación.
    La llama: engine/service/repair.py (uno mismo, el herrero de la fogata y los encargos). Si cambia, afecta: cuánto dura cada
    vida de la pieza."""
    loss = float(cfg(balance).get("repair_loss", 4))
    new_max = max(1.0, float(rec.get("max", start_max(balance))) - loss)
    return {**dict(rec), "cur": new_max, "max": new_max, "rep": int(rec.get("rep", 0)) + 1}


def repair_profession(item: dict[str, Any], balance: dict[str, Any]) -> str | None:
    """The crafting profession that repairs this piece (durability.repair_by: its type -> profession id), or None."""
    return (cfg(balance).get("repair_by") or {}).get(item.get("type", ""))


def repair_rank(item: dict[str, Any], balance: dict[str, Any]) -> int:
    """The profession rank a repair asks: the piece's level minus durability.rank_margin, at least 1. [ES] Rango que pide."""
    return max(1, int(item.get("req_level", 1)) - int(cfg(balance).get("rank_margin", 10)))


def repair_materials(item: dict[str, Any], balance: dict[str, Any]) -> dict[str, int]:
    """What one repair takes: 1 + level ÷ durability.material_step units of the repairing profession's base refined material."""
    c = cfg(balance)
    material = (c.get("material") or {}).get(repair_profession(item, balance) or "")
    if not material:
        return {}
    step = max(1, int(c.get("material_step", 20)))
    return {material: 1 + int(item.get("req_level", 1)) // step}


def materials_value(materials: dict[str, int], items: dict[str, Any]) -> int:
    """The reference value (items.yaml price) of some materials. [ES] Cuánto valen esos materiales."""
    return sum(int((items.get(i) or {}).get("price", 0)) * int(n) for i, n in materials.items())


def npc_price(item: dict[str, Any], items: dict[str, Any], balance: dict[str, Any]) -> int:
    """Coins the 🔥 campfire's smith asks: durability.npc_mult × the value of the repair's materials (at least 1).

    [ES] Qué hace: el precio del herrero de la fogata: claramente más caro que lo que le cuesta a un artesano (sus materiales).
    La llama: engine/service/repair.py. Si cambia, afecta: las monedas que se queman y cuánto conviene un artesano."""
    value = materials_value(repair_materials(item, balance), items)
    return max(1, int(math.ceil(float(cfg(balance).get("npc_mult", 3)) * value)))


def order_price(item: dict[str, Any], items: dict[str, Any], balance: dict[str, Any]) -> int:
    """Coins a 📜 repair order pays the artisan (D-140: labour on top of the materials it puts): durability.order_mult × value."""
    value = materials_value(repair_materials(item, balance), items)
    return max(1, int(math.ceil(float(cfg(balance).get("order_mult", 2)) * value)))


def repair_xp(item: dict[str, Any], balance: dict[str, Any]) -> int:
    """Profession xp of one repair: durability.xp × (1 + level ÷ 100) (6 by ⚡, like every recipe of D-328). [ES] Experiencia."""
    return int(round(float(cfg(balance).get("xp", 6)) * (1 + int(item.get("req_level", 1)) / 100)))
