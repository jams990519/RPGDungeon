"""Daily player report for the game team: what the most active players do, how much they gather, how they play.

[ES]
Para qué sirve: arma el informe diario de los jugadores que el bot manda como archivo al chat de informes (pedido del
    dueño, 17-oct-2026: "va creándome un reporte, no por jugador, sino genérico; coge a 10 jugadores de acuerdo a la
    actividad"). Es la primera pieza de la telemetría con exportación diaria de D-241.4. Solo LEE el juego: no cambia
    ninguna regla ni ningún héroe; lo único que escribe es su propia foto del día (espacio "report_snap") y la marca del
    último informe (espacio "reports"), para comparar un día con el siguiente.
    D-320 (0.46): la sección 9 cuenta el 🏛️ Mercado entre jugadores (compras, unidades, monedas que cambiaron de mano, impuesto
    quemado, órdenes publicadas, canceladas y vencidas) con lo que el mercado anota cada día en "market_log" (clave el día).
Documento de diseño: diseno/01-plataforma/informes.md
Módulo: M20 Administración y telemetría (D-241.4)
Depende de: engine.service (GameService: store, content, clock), engine.hero (Hero)
Lo usan: adapters/telegram/bot.py (notifier: lo manda una vez por día al chat de informes); tests/test_informes.py
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: espacio "reports" (clave "players": {"day": último día enviado}) y "report_snap" (clave el día:
    {id del héroe: contadores}). Nunca se borra nada de los jugadores.
Reglas que nunca se rompen:
    1. Sin nombres ni cuentas: el informe es de todos juntos (el dueño pidió "genérico").
    2. Solo lectura del juego: un informe nunca cambia un héroe, un campamento ni una regla.
    3. Es para el equipo, no para los jugadores: va en español y no pasa por los archivos de idiomas.
Si cambias esto, revisa:
    - El bot: adapters/telegram/bot.py (REPORTS_CHAT_ID, notifier)
    - Lo que se mide: los campos de Hero (engine/hero/hero.py) y los oficios (content/professions.yaml); el mercado
      (engine/service/market.py _mkt_log, espacio "market_log")
    - Pruebas: tests/test_informes.py
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from typing import Any

from engine.hero import Hero

SAMPLE = 10                    # the owner: "coge a 10 jugadores de acuerdo a la actividad"
ACTIVE_DAYS = 7                # players seen in the last week can be in the sample
DAY = 86400.0


def _day(now: float) -> int:
    return int(now // DAY)


def _counters(service: Any, hero: Hero) -> dict[str, float]:
    """The numbers of one hero that a day can change (cumulative: the report compares two days)."""
    catalog = (service.content.professions or {}).get("professions") or {}
    profs = hero.professions or {}

    def total(branches: tuple[str, ...], skip: tuple[str, ...] = ()) -> int:
        return int(sum(xp for pid, xp in profs.items() if catalog.get(pid, {}).get("branch") in branches and pid not in skip))

    return {"level": hero.level, "xp": hero.xp, "gold": hero.gold, "kills": hero.kills, "zones": hero.zones_discovered,
            "gathered": total(("gather",), skip=("desollador",)), "skinned": int(profs.get("desollador", 0)),
            "explored": int(profs.get("explorador", 0)), "crafted": total(("refine", "craft")), "sold": int(profs.get("comercio", 0)),
            "seen": hero.seen_at}


def _heroes(service: Any) -> list[tuple[str, Hero]]:
    out = []
    for account, data in service.store.items("hero"):
        try:
            out.append((account, Hero.from_dict(data)))
        except TypeError:          # a broken record never stops the report
            continue
    return out


def due(service: Any) -> bool:
    """True if today's report has not been sent yet (one a day, the first time the bot looks)."""
    record = service.store.get("reports", "players") or {}
    return record.get("day") != _day(service.clock.now())


def mark_sent(service: Any) -> None:
    """Note that today's report went out (called by the bot once Telegram accepted the file)."""
    service.store.put("reports", "players", {"day": _day(service.clock.now()), "at": service.clock.now()})


def build(service: Any) -> tuple[str, str]:
    """The report as (file name, text). It also keeps today's photo of every active hero to compare tomorrow.

    [ES]
    Qué hace: arma el informe del día: cuántos jugadores hay y cuántos jugaron; los 10 más activos (los que más
    experiencia sumaron desde la foto anterior; el primer día, los que jugaron más reciente); quiénes son (niveles, clases,
    idiomas, campamentos), qué hacen ahora, cuánto juntaron, exploraron, pelearon, fabricaron y vendieron desde la foto
    anterior (y en total), sus oficios, su economía, la mochila y el mapa; cuántos mensajes de 💬 Feedback llegaron y, desde la
    0.46 (D-320), el 🏛️ Mercado entre jugadores de ayer y de hoy (market_lines). Guarda
    la foto de hoy en "report_snap".
    La llama: el bot (notifier). Si cambia, afecta: lo que lee el equipo cada día.
    """
    now = service.clock.now()
    today = _day(now)
    heroes = _heroes(service)
    previous = service.store.get("report_snap", str(today - 1)) or {}
    if not previous:                                   # the last photo before today, if a day was skipped
        for back in range(2, 8):
            previous = service.store.get("report_snap", str(today - back)) or {}
            if previous:
                break
    recent = [(acc, h) for acc, h in heroes if now - (h.seen_at or 0) <= ACTIVE_DAYS * DAY]
    snaps = {h.id: _counters(service, h) for _, h in heroes}

    def gained(hero: Hero, key: str) -> float:
        before = previous.get(hero.id)
        return snaps[hero.id][key] - before[key] if before and key in before else 0.0

    recent.sort(key=lambda ah: (gained(ah[1], "xp"), ah[1].seen_at or 0), reverse=True)
    sample = [h for _, h in recent[:SAMPLE]]
    service.store.put("report_snap", str(today), snaps)

    lines: list[str] = []
    add = lines.append
    version = (list((service.content.patches or {}).values())[-1] or {}).get("version", "?") if service.content.patches else "?"
    date = datetime.fromtimestamp(now, timezone.utc).strftime("%Y-%m-%d")
    add(f"LOST REALMS · INFORME DE JUGADORES · {date} (UTC) · versión {version}")
    add("Generado por el bot para el equipo. Genérico: sin nombres ni cuentas.")
    add("")
    played_today = sum(1 for _, h in heroes if now - (h.seen_at or 0) <= DAY)
    add("1. CUÁNTOS")
    add(f"- Héroes creados: {len(heroes)}")
    add(f"- Jugaron en las últimas 24 h: {played_today} · en los últimos 7 días: {len(recent)}")
    add(f"- Muestra de este informe: los {len(sample)} más activos (los que más experiencia sumaron desde el informe anterior).")
    first = not previous
    if first:
        add("- Es el primer informe con foto: desde el próximo se ve lo de cada día (ahora solo hay totales).")
    add("")
    if not sample:
        add("Nadie jugó en los últimos 7 días.")
        return f"informe-jugadores-{date}.txt", "\n".join(lines) + "\n"

    def avg(values: list[float]) -> str:
        return f"{sum(values) / len(values):.1f}".replace(".", ",") if values else "0"

    classes = (service.content.classes or {})
    add("2. QUIÉNES SON (muestra)")
    levels = [h.level for h in sample]
    add(f"- Nivel: promedio {avg(levels)} · mínimo {min(levels)} · máximo {max(levels)}")
    groups = Counter(classes.get(h.class_id, {}).get("group", h.class_id) for h in sample)
    add("- Clases: " + ", ".join(f"{g} {n}" for g, n in groups.most_common()))
    langs = Counter((service.store.get("prefs", acc) or {}).get("lang", "es") for acc, h in recent[:SAMPLE])
    add("- Idioma: " + ", ".join(f"{lang} {n}" for lang, n in langs.most_common()))
    with_camp = sum(1 for h in sample if h.camp)
    camps = sum(1 for _ in service.store.items("camp"))
    add(f"- Con campamento: {with_camp} de {len(sample)} · campamentos en el mundo: {camps}")
    add("")

    add("3. QUÉ HACEN AHORA (muestra)")
    doing = Counter(((h.activity or {}).get("kind") or "nada") for h in sample)
    fighting = sum(1 for h in sample if service.store.get("combat", h.id))
    names = {"travel": "viajando", "explore": "explorando", "gather": "recolectando", "hunt": "cazando", "rest": "descansando",
             "nada": "sin actividad"}
    add("- " + ", ".join(f"{names.get(k, k)} {n}" for k, n in doing.most_common()) + (f" · en pelea {fighting}" if fighting else ""))
    add("")

    add("4. CUÁNTO JUEGAN Y JUNTAN (muestra)")
    labels = [("gathered", "Unidades recolectadas"), ("skinned", "Carne y piel del 🔪 Desollador"), ("explored", "Puntos de 🧭 Explorador"),
              ("kills", "Peleas ganadas"), ("crafted", "Experiencia de refinar y fabricar"), ("sold", "Experiencia de 💱 Comercio (vender)"),
              ("xp", "Experiencia de héroe"), ("zones", "Zonas descubiertas"), ("gold", "Monedas (🥉)")]
    for key, label in labels:
        totals = [snaps[h.id][key] for h in sample]
        if first:
            add(f"- {label}: en total {int(sum(totals))} · promedio por jugador {avg(totals)}")
        else:
            day_values = [gained(h, key) for h in sample]
            add(f"- {label}: hoy {int(sum(day_values))} (promedio {avg(day_values)}) · en total {int(sum(totals))}")
    if not first:
        busiest = Counter()
        for h in sample:
            for key in ("gathered", "explored", "kills", "crafted"):
                busiest[key] += max(0.0, gained(h, key))
        if sum(busiest.values()) > 0:
            share = {k: 100 * v / sum(busiest.values()) for k, v in busiest.items()}
            add("- En qué gastan el tiempo (reparto de lo que sumaron hoy): " + ", ".join(
                f"{n} {int(round(share[k]))} %" for k, n in (("gathered", "recolectar"), ("explored", "explorar"),
                                                              ("kills", "pelear"), ("crafted", "fabricar"))))
    add("")

    add("5. OFICIOS (muestra)")
    catalog = (service.content.professions or {}).get("professions") or {}
    learned = Counter(pid for h in sample for pid in (h.learned or []))
    add("- Aprendidos: " + (", ".join(f"{pid} {n}" for pid, n in learned.most_common()) if learned else "ninguno todavía"))
    for pid in ("minero", "herbolario", "lenador", "pescador", "explorador"):
        if pid in catalog:
            values = [service._prof_rank(h, pid) for h in sample if (h.professions or {}).get(pid, 0) > 0]
            if values:
                add(f"- Rango de {pid}: promedio {avg(values)} · {len(values)} de {len(sample)} lo subieron")
    add("")

    add("6. MOCHILA Y ECONOMÍA (muestra)")
    golds = [h.gold for h in sample]
    add(f"- Monedas por jugador (🥉): promedio {avg(golds)} · mínimo {min(golds)} · máximo {max(golds)}")
    carried = Counter()
    for h in sample:
        for item_id, n in (h.backpack or {}).items():
            if (service.content.items.get(item_id) or {}).get("kind") in ("material", "food"):
                carried[item_id] += n
    add("- Lo que más llevan: " + (", ".join(f"{i} {n}" for i, n in carried.most_common(8)) if carried else "nada"))
    add("")

    add("7. MAPA (muestra)")
    far = [abs(h.x) + abs(h.y) for h in sample]
    add(f"- Distancia a la fogata ahora (zonas): promedio {avg(far)} · la más lejana {max(far)}")
    known = [len(h.known or []) for h in sample]
    add(f"- Zonas que recuerdan: promedio {avg(known)} · máximo {max(known)}")
    add("")

    pending = [d for _, d in service.store.items("feedback") if now - d.get("at", 0) <= DAY]
    add("8. FEEDBACK")
    add(f"- Mensajes de 💬 Feedback en las últimas 24 h: {len(pending)} (cada uno llega suelto a este chat).")
    add("")
    lines += market_lines(service)
    return f"informe-jugadores-{date}.txt", "\n".join(lines) + "\n"


def market_lines(service: Any) -> list[str]:
    """Section 9: the 🏛️ player market of yesterday (a whole day) and of today so far, from "market_log" (D-320).

    [ES] Qué hace: las líneas del mercado entre jugadores para el informe (todos juntos, sin nombres): cuántas compras hubo,
    cuántas unidades y monedas cambiaron de mano, cuánto impuesto se quemó y cuántas órdenes se publicaron, cancelaron o
    vencieron; y cuántas órdenes hay abiertas ahora. Solo lee. La llama: build().
    Si cambia, afecta: lo que lee el equipo.
    """
    today = int(service._today())
    out = ["9. MERCADO ENTRE JUGADORES"]
    for label, day in (("ayer", today - 1), ("hoy hasta ahora", today)):
        log = service.store.get("market_log", str(day)) or {}
        out.append(f"- {label}: compras {int(log.get('trades', 0))} · unidades {int(log.get('units', 0))} · monedas que "
                   f"cambiaron de mano (🥉) {int(log.get('coins', 0))} · impuesto quemado (🥉) {int(log.get('tax', 0))} · "
                   f"órdenes de venta {int(log.get('sell_orders', 0))} · pedidos de compra {int(log.get('buy_orders', 0))} · "
                   f"canceladas {int(log.get('cancelled', 0))} · vencidas {int(log.get('expired', 0))}")
    orders = [o for _, o in service.store.items("market_order")]
    out.append(f"- Órdenes abiertas ahora: {sum(1 for o in orders if o.get('side') == 'sell')} de venta · "
               f"{sum(1 for o in orders if o.get('side') == 'buy')} pedidos de compra")
    return out
