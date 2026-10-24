"""Player report for the game team, every 3 hours: who played (with their @), how much, what content, card by card.

[ES]
Para qué sirve: arma el informe de jugadores que el bot manda al chat de informes cada 3 horas (a las 00, 03, 06 … 21 UTC),
    en dos archivos: un .txt para leer y un .csv con una fila por jugador (se abre en Excel o Google Sheets). Pedido del dueño,
    24-oct-2026 (D-341, confirmada): "quiero que me saque los promedios de jugadores activos con más detalles, quiénes son, con
    su arroba, y cuál es el tipo de contenido que más hacen... la especificación de cuánto juegan y juntan, eso lo quiero por
    jugador. Aunque sea largo el documento, no importa"; "que los documentos que vayan llegando a Lost Realms Report sean como
    un reporte constante de base de datos, para evitar que el servidor se sobrecargue". Reemplaza al informe diario genérico de
    la 0.33 (D-260: "no por jugador, sino genérico; coge a 10 jugadores"). Lee los contadores de la telemetría del motor
    (engine/service/telemetry.py, D-344) y las fichas de los héroes; desde la 0.46 (D-320) cuenta el 🏛️ Mercado ("market_log")
    y desde la 0.59 (D-335) los 📜 pedidos de fabricación (market_lines). Si existe "migrations"/"malla_to_leather" (la
    conversión de la malla de la 0.62.2), lista a quién se le convirtió (malla_lines).
Documento de diseño: diseno/01-plataforma/informes.md
Módulo: M20 Administración y telemetría (D-241.4, D-260, D-341, D-344)
Depende de: engine.service (GameService: store, content, clock, texts, flush_telemetry, telemetry_window, telemetry_since y
    las ayudas que solo leen: _place_label, _hero_title, _prof_name, _prof_rank, _my_gremio, _bag_types_used, _bag_types_cap,
    _bag_gear_used, _pack_gear_cap, _pbag_worn, _money, _today), engine.service.telemetry (SLOT_SECONDS, KEEP_SECONDS,
    CATEGORIES, merge), engine.hero (Hero)
Lo usan: adapters/telegram/bot.py (send_reports, dentro de notifier: due, generate, pending, mark_sent);
    tests/test_informes_por_jugador.py, tests/test_fogata_ordenada.py, tests/test_mercado.py y tests/test_solo_privado.py
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: espacio "reports" (clave "slots": {"sent_until": fin de la ventana del último informe que salió,
    "pending": clave del informe armado que todavía no salió entero}; la clave vieja "players" de la 0.33 se borra a los 3 días)
    y "report_out" (clave "s<tramo>": el informe armado de ese tramo, {"key", "since", "until", "at", "txt_name", "txt",
    "csv_name", "csv", "caption", "sent": {"txt", "csv"}}; se guarda 3 días por si Telegram falla y hay que mandarlo de
    nuevo). "report_snap" (las fotos diarias de la 0.33) ya no se escribe: lo que queda se borra a los 3 días.
Reglas que nunca se rompen:
    1. Con nombres y @, solo para el equipo (D-341 reemplaza la regla "sin nombres ni cuentas" de D-260): el informe va
       únicamente al chat de informes (RPG_REPORTS_CHAT_ID); nunca a un jugador ni a otro grupo.
    2. Solo lectura del juego: un informe nunca cambia un héroe, un campamento ni una regla. Lo único que borra es lo suyo
       de más de 3 días (D-341: "el servidor solo ... de los últimos 3 días no más, el resto al grupo de reportes"); nunca
       el progreso de nadie ni lo de otros módulos (por ejemplo "market_log" es del mercado).
    3. Es para el equipo, no para los jugadores: va en español y no pasa por los archivos de idiomas.
    4. Sin avalancha: uno por tramo de 3 horas; si el bot estuvo apagado varios tramos, sale uno solo que cubre desde el
       último que salió (como mucho 3 días, lo que guarda el servidor).
Si cambias esto, revisa:
    - El bot: adapters/telegram/bot.py (REPORTS_CHAT_ID, send_reports, notifier)
    - Lo que se mide: engine/service/telemetry.py (los contadores y CATEGORIES), los campos de Hero (engine/hero/hero.py),
      los oficios (content/professions.yaml) y el mercado (engine/service/market.py _mkt_log, espacio "market_log";
      engine/service/craft_orders.py, "craft_*" y "craft_order")
    - Pruebas: tests/test_informes_por_jugador.py
"""

from __future__ import annotations

import csv
import io
from collections import Counter
from datetime import datetime, timezone
from typing import Any, NamedTuple

from engine.hero import Hero
from engine.service.telemetry import CATEGORIES, KEEP_SECONDS, SLOT_SECONDS, merge

DAY = 86400.0
WEEK = 7 * DAY
STATE_KEY = "slots"            # "reports"/"slots": the last report that went out and the one waiting
OUT_NAMESPACE = "report_out"   # the reports built, kept 3 days (re-sent if Telegram fails)
TOP_ITEMS = 15                 # how many items the "most gathered" lines show
CATEGORY_NAMES = {"explore": "explorar", "gather": "recolectar (también talar y pescar)", "fight": "cazar y pelear",
                  "travel": "viajar y mapa", "craft": "fabricar, refinar, cocinar y oficios", "market": "mercado y mercader",
                  "camp": "campamento y gremio (obras, depósitos, fondo)", "dungeon": "mazmorras", "quests": "misiones y tablón",
                  "social": "social y chat", "hero": "héroe, equipo y mochila", "menus": "menús y otros"}
SHORT_NAMES = {"explore": "explorar", "gather": "recolectar", "fight": "pelear", "travel": "viajar", "craft": "fabricar",
               "market": "mercado", "camp": "campamento", "dungeon": "mazmorras", "quests": "misiones", "social": "social",
               "hero": "heroe", "menus": "menus"}
CARD_NAMES = {"explore": "explorar", "gather": "recolectar", "fight": "pelear", "travel": "viajar", "craft": "fabricar",
              "market": "mercado", "camp": "campamento", "dungeon": "mazmorras", "quests": "misiones", "social": "social",
              "hero": "héroe", "menus": "menús"}
ACTIVITY_NAMES = {"travel": "viajar", "explore": "explorar", "gather": "recolectar", "chop": "talar", "fish": "pescar",
                  "hunt": "cazar", "rest": "descansar"}
DOING_NAMES = {"travel": "viajando", "explore": "explorando", "gather": "recolectando", "chop": "talando", "fish": "pescando",
               "hunt": "cazando", "rest": "descansando"}
ROLE_NAMES = {"defensa": "defensa", "ataque": "ataque", "curacion": "curación", "soporte": "soporte"}
CONTENT_SKIP = ("menus", "hero")   # the main content of a player is the top kind that is not just menus or the hero screens


class Report(NamedTuple):
    """One report: the window it covers and its two files (D-341: a readable .txt and a .csv table)."""
    since: float
    until: float
    txt_name: str
    txt: str
    csv_name: str
    csv: str


def boundary(now: float) -> float:
    """The start of the 3-hour slot `now` is in (00, 03, 06 … 21 UTC): a report covers up to here."""
    return float(int(now // SLOT_SECONDS) * SLOT_SECONDS)


def _state(service: Any) -> dict[str, Any]:
    return service.store.get("reports", STATE_KEY) or {}


def due(service: Any) -> bool:
    """True if a slot ended since the last report was built (one per slot; after a downtime, just one).

    [ES] Qué hace: dice si toca armar un informe: terminó un tramo de 3 horas desde el último armado (el que espera salir o el
    último que salió). La llama: el bot (send_reports) en cada vuelta. Si cambia, afecta: cada cuánto llega el informe.
    """
    state = _state(service)
    waiting = service.store.get(OUT_NAMESPACE, state["pending"]) if state.get("pending") else None
    last = waiting["until"] if waiting else state.get("sent_until")
    return last is None or float(last) < boundary(service.clock.now())


def generate(service: Any) -> dict[str, Any]:
    """Build the report up to the last slot boundary, keep it in "report_out" (3 days) and mark it as waiting to go out.

    [ES]
    Qué hace: arma el informe desde el último que salió (o las últimas 3 horas, la primera vez; nunca más de 3 días) hasta el
    comienzo del tramo de ahora, lo guarda en "report_out" y lo deja esperando a que el bot lo mande. Si había otro armado
    que no salió (Telegram falló), lo reemplaza: el nuevo cubre todo (sin avalancha, regla 4). También borra lo suyo de más
    de 3 días (prune). La llama: el bot (send_reports) cuando due() da True. Si cambia, afecta: lo que llega al chat.
    """
    now = service.clock.now()
    until = boundary(now)
    state = _state(service)
    waiting = service.store.get(OUT_NAMESPACE, state["pending"]) if state.get("pending") else None
    since = float(state.get("sent_until") or (waiting or {}).get("since") or until - SLOT_SECONDS)
    since = max(since, until - KEEP_SECONDS)
    if since >= until:
        since = until - SLOT_SECONDS
    report = build(service, since, until)
    old = state.get("pending")
    key = f"s{int(until // SLOT_SECONDS)}"
    if old and old != key:
        service.store.delete(OUT_NAMESPACE, old)          # never sent: the new one covers its window too
    stamp = datetime.fromtimestamp(until, timezone.utc).strftime("%Y-%m-%d %H:%M")
    record = {"key": key, "since": since, "until": until, "at": now, "txt_name": report.txt_name, "txt": report.txt,
              "csv_name": report.csv_name, "csv": report.csv, "caption": f"📊 Informe de jugadores · {stamp} UTC",
              "sent": {"txt": False, "csv": False}}
    service.store.put(OUT_NAMESPACE, key, record)
    state["pending"] = key
    service.store.put("reports", STATE_KEY, state)
    prune(service)
    return record


def pending(service: Any) -> dict[str, Any] | None:
    """The built report still waiting to go out (all or part of it), or None. [ES] La llama: el bot (send_reports)."""
    key = _state(service).get("pending")
    return service.store.get(OUT_NAMESPACE, key) if key else None


def mark_sent(service: Any, key: str, part: str) -> None:
    """Note that one file of a report ("txt" or "csv") went out; when both did, the report is done (the next starts there).

    [ES] Qué hace: anota que Telegram aceptó uno de los dos archivos; con los dos, el informe quedó enviado y el siguiente
    empieza donde terminó este. Así, si falla el segundo, no se repite el primero. La llama: el bot (send_reports).
    """
    record = service.store.get(OUT_NAMESPACE, key)
    if record is None:
        return
    record.setdefault("sent", {})[part] = True
    service.store.put(OUT_NAMESPACE, key, record)
    if all(record["sent"].get(p) for p in ("txt", "csv")):
        state = _state(service)
        state["sent_until"] = record["until"]
        if state.get("pending") == key:
            state["pending"] = None
        service.store.put("reports", STATE_KEY, state)


def prune(service: Any) -> None:
    """Delete the report's own data older than 3 days: built reports, the 0.33 daily photos and its old marker (rule 2).

    [ES] Qué hace: borra lo del informe de más de 3 días ("report_out", las fotos viejas de "report_snap" y la marca vieja
    "reports"/"players"). Nunca toca héroes ni lo de otros módulos; la telemetría la poda el motor (flush_telemetry).
    """
    now = service.clock.now()
    oldest = now - KEEP_SECONDS
    keep = _state(service).get("pending")
    for key, record in list(service.store.items(OUT_NAMESPACE)):
        if key != keep and float(record.get("until", 0)) < oldest:
            service.store.delete(OUT_NAMESPACE, key)
    for key, _ in list(service.store.items("report_snap")):
        if not key.isdigit() or int(key) * DAY < oldest:
            service.store.delete("report_snap", key)
    old = service.store.get("reports", "players")
    if old is not None and float(old.get("at", 0)) < oldest:
        service.store.delete("reports", "players")


# ---------------------------------------------------------------------- helpers that only read

def _heroes(service: Any) -> dict[str, Hero]:
    out: dict[str, Hero] = {}
    for account, data in service.store.items("hero"):
        try:
            out[account] = Hero.from_dict(data)
        except (TypeError, KeyError):                     # a broken record never stops the report
            continue
    return out


def _num(value: float, digits: int = 1) -> str:
    """1234.5 -> "1234,5" (decimal comma, as the team reads it)."""
    text = f"{value:.{digits}f}" if digits else str(int(round(value)))
    return text.replace(".", ",")


def _minutes(value: float) -> str:
    """Minutes as "2 h 05 min", "35 min" or "0 min"."""
    total = int(round(value))
    hours, mins = divmod(total, 60)
    return f"{hours} h {mins:02d} min" if hours else f"{mins} min"


def _when(ts: float) -> str:
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%d %H:%M") if ts else "nunca"


def _ago(now: float, ts: float) -> str:
    if not ts:
        return "nunca"
    left = max(0, int(now - ts) // 60)
    days, rest = divmod(left, 1440)
    hours, mins = divmod(rest, 60)
    if days:
        return f"hace {days} d {hours} h"
    return f"hace {hours} h {mins:02d} min" if hours else f"hace {mins} min"


def _item(service: Any, item_id: str) -> str:
    item = service.content.items.get(item_id) or {}
    if not item:
        return item_id
    return f"{item.get('emoji', '')} {service.texts.t(item['name_key'])}".strip()


def _items_line(service: Any, items: dict[str, int], top: int = TOP_ITEMS) -> str:
    ranked = sorted(((n, i) for i, n in items.items() if n), key=lambda p: (-p[0], p[1]))
    parts = [f"{_item(service, i)} {n}" for n, i in ranked[:top]]
    if len(ranked) > top:
        parts.append(f"y {len(ranked) - top} más")
    return " · ".join(parts) if parts else "nada"


def _share(counts: dict[str, int], names: dict[str, str], order: tuple[str, ...]) -> str:
    total = sum(counts.values())
    if not total:
        return "nada medido"
    ranked = sorted((k for k in counts if counts[k]), key=lambda k: (-counts[k], order.index(k) if k in order else 99))
    return " · ".join(f"{names.get(k, k)} {counts[k]} ({_num(100 * counts[k] / total, 0)} %)" for k in ranked)


def _main_content(cats: dict[str, int]) -> str | None:
    """The kind of content a player did most (by buttons), leaving out menus and the hero screens if there is anything else."""
    useful = {k: n for k, n in cats.items() if n and k not in CONTENT_SKIP}
    pool = useful or {k: n for k, n in cats.items() if n}
    if not pool:
        return None
    return max(pool, key=lambda k: (pool[k], -CATEGORIES.index(k) if k in CATEGORIES else -99))


def _main_activity(timed: dict[str, float]) -> str | None:
    pool = {k: v for k, v in timed.items() if v > 0}
    return max(pool, key=lambda k: pool[k]) if pool else None


def _empty() -> dict[str, Any]:
    """The counts of an account with nothing measured (every number 0)."""
    return merge([])


def _gathered(rec: dict[str, Any]) -> int:
    return int(sum((rec.get("items") or {}).values()))


def _fights(rec: dict[str, Any]) -> int:
    return int(rec.get("won", 0) + rec.get("lost", 0) + rec.get("fled", 0))


def _timed(rec: dict[str, Any]) -> float:
    return float(sum((rec.get("timed") or {}).values()))


def _produced(rec: dict[str, Any]) -> bool:
    return bool(_gathered(rec) or _timed(rec) or rec.get("xp") or _fights(rec) or rec.get("crafts"))


def _camp_line(service: Any, hero: Hero) -> tuple[str, str]:
    """(camp, guild) names as the report shows them ("" when none)."""
    camp = service.store.get("camp", hero.camp) if hero.camp else None
    camp_name = (camp or {}).get("name", "") if camp else ""
    guild = ""
    try:
        record = service._my_gremio(hero)
        guild = (record or {}).get("name", "")
    except Exception:                                     # noqa: BLE001 - reading only; a broken record is skipped
        guild = ""
    return camp_name, guild


def _doing(service: Any, hero: Hero) -> str:
    if (hero.oath or {}).get("fell"):
        return "💀 cayó para siempre"
    if service.store.get("combat", hero.id):
        return "en pelea"
    activity = hero.activity or {}
    kind = activity.get("kind")
    if not kind:
        return "sin actividad"
    if kind == "gather":
        kind = activity.get("mode") or ("chop" if activity.get("only") else "gather")
    ends = datetime.fromtimestamp(float(activity.get("until", 0)), timezone.utc).strftime("%H:%M")
    left = f", faltan {activity.get('left')} vueltas" if activity.get("left") else ""
    return f"{DOING_NAMES.get(kind, kind)} (termina {ends} UTC{left})"


def _prof_line(service: Any, hero: Hero) -> str:
    catalog = (service.content.professions or {}).get("professions") or {}
    ranks = []
    for pid, xp in (hero.professions or {}).items():
        if xp > 0 and pid in catalog:
            try:
                rank = service._prof_rank(hero, pid)
            except Exception:                             # noqa: BLE001
                continue
            learned = "" if pid in (hero.learned or []) or catalog[pid].get("learn") == "auto" else " (sin aprender)"
            ranks.append((rank, f"{service._prof_name(pid)} {rank}{learned}"))
    ranks.sort(key=lambda p: -p[0])
    return " · ".join(label for _, label in ranks) or "ninguno"


def _bag(service: Any, hero: Hero) -> tuple[int, int, int, int]:
    """(types used, types cap, loose gear, gear cap) of the 0.62 backpack (D-338); zeros if it cannot be read."""
    try:
        return (int(service._bag_types_used(hero)), int(service._bag_types_cap(hero)), int(service._bag_gear_used(hero)),
                int(service._pack_gear_cap()))
    except Exception:                                     # noqa: BLE001
        return 0, 0, 0, 0


class _Player:
    """Everything the report says about one account (read once, used by the .txt and the .csv)."""

    def __init__(self, service: Any, account: str, hero: Hero, win: dict[str, Any], day: dict[str, Any],
                 since: float, until: float, last: float = 0.0) -> None:
        prefs = service.store.get("prefs", account) or {}
        self.account = account
        self.hero = hero
        self.handle = prefs.get("handle") or ""
        self.lang = prefs.get("lang") or "es"
        self.win = win
        self.day = day
        first = float((service.store.get("player", account) or {}).get("first_seen") or 0.0)
        # the last time it played: its last button (Hero.seen_at, 0 if it only created the hero), the measured one, or its start
        self.seen = max(float(hero.seen_at or 0.0), float(last or 0.0), first)
        self.active_win = bool(win.get("actions")) or since <= self.seen < until
        self.active_day = bool(day.get("actions")) or until - DAY <= self.seen < until
        self.background = not day.get("actions") and _produced(day)
        cdef = service.content.classes.get(hero.class_id, {})
        self.group = cdef.get("group", hero.class_id)
        self.role = ROLE_NAMES.get(cdef.get("role", ""), cdef.get("role", "") or "-")
        self.main = _main_content(day.get("cats") or {})
        self.main_time = _main_activity(day.get("timed") or {})

    def fill(self, service: Any) -> "_Player":
        """The details only the cards and the table need (place, camp, what it does now, backpack, gear): read once."""
        hero = self.hero
        try:
            self.title = service._hero_title(hero)
        except Exception:                                 # noqa: BLE001
            self.title = hero.class_id
        self.camp, self.guild = _camp_line(service, hero)
        try:
            self.place = service._place_label(hero.x, hero.y)
        except Exception:                                 # noqa: BLE001
            self.place = f"({hero.x}, {hero.y})"
        self.doing = _doing(service, hero)
        self.bag = _bag(service, hero)
        slots = list(service.content.balance.get("gear", {}).get("slots") or [])
        self.worn = sum(1 for s in slots if (hero.gear or {}).get(s))
        self.slots = len(slots) or len(hero.gear or {})
        return self

    @property
    def at(self) -> str:
        return self.handle or "sin @"

    def sort_key(self) -> tuple[float, ...]:
        d = self.day
        return (d.get("actions", 0), d.get("active_minutes", 0), _timed(d), _gathered(d), d.get("xp", 0), self.seen)


def _collect(service: Any, since: float, until: float) -> dict[str, Any]:
    """Read the game once for the report: the heroes, the telemetry of the window and of the last 24 h, who is active."""
    service.flush_telemetry()                             # the last minute of counts, so the report has everything
    heroes = _heroes(service)
    win = service.telemetry_window(since, until)
    day = service.telemetry_window(until - DAY, until)
    kept = service.telemetry_window(until - KEEP_SECONDS, until + SLOT_SECONDS)    # the last button of the 3 days kept
    players: list[_Player] = []
    for account, hero in heroes.items():
        last = float((kept.get(account) or {}).get("last") or 0.0)
        p = _Player(service, account, hero, win.get(account) or _empty(), day.get(account) or _empty(), since, until, last)
        players.append(p)
    cards = sorted((p for p in players if p.active_day or p.background), key=lambda p: p.sort_key(), reverse=True)
    cards = [p.fill(service) for p in cards]
    no_hero = sorted(a for a, rec in day.items() if a not in heroes and rec.get("actions"))
    week = [p for p in players if until - WEEK <= p.seen or p.active_day]
    stopped = sorted((p for p in players if until - WEEK <= p.seen < until - DAY and not p.day.get("actions")),
                     key=lambda p: -p.seen)
    return {"heroes": heroes, "players": players, "cards": cards, "win": win, "day": day, "no_hero": no_hero,
            "week": week, "stopped": stopped, "since": since, "until": until, "now": service.clock.now(),
            "measured_since": service.telemetry_since()}


# ---------------------------------------------------------------------- the report

def build(service: Any, since: float | None = None, until: float | None = None) -> Report:
    """The report for the window [since, until) and the last 24 h before `until`, as a .txt and a .csv (D-341).

    [ES]
    Qué hace: arma los dos archivos. El .txt: cuántos juegan (3 h, 24 h y 7 días; héroes nuevos), los promedios por jugador
    activo (botones, minutos activos, sesiones, minutos de actividades con tiempo, unidades recolectadas, peleas,
    fabricaciones, experiencia y monedas) de la ventana y de las últimas 24 h, qué hacen más (reparto de botones por tipo y del
    tiempo por actividad, y el contenido principal de cada uno), lo que más se recolecta, quiénes son (niveles, clases, roles,
    idiomas, campamentos), oficios, mochila y economía, mapa, 💬 Feedback, el 🏛️ Mercado (market_lines), quién dejó de venir
    (jugó en 7 días y no en 24 h, con su @), la malla convertida de la 0.62.2 si existe (malla_lines) y una tarjeta por jugador
    activo en 24 h, del más activo al menos. El .csv: una fila por jugador de las tarjetas con los mismos números (3 h y 24 h).
    Sin `since`/`until`: las últimas 3 horas hasta el comienzo del tramo de ahora.
    La llama: generate (y las pruebas). Si cambia, afecta: lo que lee el equipo.
    """
    end = boundary(service.clock.now()) if until is None else float(until)
    start = end - SLOT_SECONDS if since is None else float(since)
    data = _collect(service, start, end)
    stamp = datetime.fromtimestamp(end, timezone.utc).strftime("%Y-%m-%d-%Hh")
    return Report(start, end, f"informe-jugadores-{stamp}.txt", _txt(service, data),
                  f"datos-jugadores-{stamp}.csv", _csv(service, data))


def _avg_lines(data: dict[str, Any]) -> list[str]:
    """Section 2: the averages per active player (with buttons measured) of the window and of the last 24 h."""
    rows = [("Botones (acciones)", lambda r: r.get("actions", 0), 1),
            ("Minutos activos (con al menos un botón)", lambda r: r.get("active_minutes", 0), 1),
            ("Sesiones (una pausa de más de 15 min corta)", lambda r: r.get("sessions", 0), 1),
            ("Minutos de actividades con tiempo (viajes, lotes, descanso)", _timed, 0),
            ("Unidades recolectadas (también talar, pescar y despellejar)", _gathered, 1),
            ("Peleas", _fights, 1), ("  ganadas", lambda r: r.get("won", 0), 1), ("  perdidas", lambda r: r.get("lost", 0), 1),
            ("Fabricaciones", lambda r: r.get("crafts", 0), 1), ("Experiencia de héroe", lambda r: r.get("xp", 0), 0),
            ("Monedas que entraron (🥉)", lambda r: r.get("coins_in", 0), 0),
            ("Monedas que salieron (🥉)", lambda r: r.get("coins_out", 0), 0)]
    win = [r for r in data["win"].values() if r.get("actions")]
    day = [r for r in data["day"].values() if r.get("actions")]
    out = [f"(entre los {len(win)} jugadores con botones medidos en la ventana y los {len(day)} de las últimas 24 h)"]
    for label, get, digits in rows:
        a = _num(sum(get(r) for r in win) / len(win), digits) if win else "0"
        b = _num(sum(get(r) for r in day) / len(day), digits) if day else "0"
        out.append(f"- {label}: ventana {a} · 24 h {b}")
    return out


def _txt(service: Any, data: dict[str, Any]) -> str:
    since, until, now = data["since"], data["until"], data["now"]
    hours = (until - since) / 3600
    lines: list[str] = []
    add = lines.append
    patches = service.content.patches or {}
    version = (list(patches.values())[-1] or {}).get("version", "?") if patches else "?"
    add(f"LOST REALMS · INFORME DE JUGADORES · {_when(until)} UTC · versión {version}")
    add("Para el equipo (D-341): quién juega, con su @, cuánto y qué. Solo para este chat.")
    window = f"{_when(since)} → {_when(until)} UTC ({_num(hours, 0)} h)"
    if hours > SLOT_SECONDS / 3600 + 0.01:
        window += " · el bot estuvo apagado o no pudo mandar: este informe cubre desde el último que salió"
    add(f"Ventana: {window}. Últimas 24 h: desde {_when(until - DAY)} UTC.")
    measured = data["measured_since"]
    if measured is None or measured >= until:
        add("Medición por jugador: empezó después de esta ventana; este informe solo trae lo que guardan las fichas "
            "(nivel, monedas, último botón). El próximo trae todo.")
    else:
        add(f"Medición por jugador desde: {_when(measured)} UTC (lo de antes no se midió).")
    add("")

    cards: list[_Player] = data["cards"]
    win_active = [p for p in data["players"] if p.active_win]
    day_active = [p for p in data["players"] if p.active_day]
    add("1. CUÁNTOS")
    created_win = sum(r.get("created", 0) for r in data["win"].values())
    created_day = sum(r.get("created", 0) for r in data["day"].values())
    add(f"- Héroes en total: {len(data['heroes'])} · nuevos en la ventana: {created_win} · en 24 h: {created_day}")
    add(f"- Jugadores activos (tocaron al menos un botón): ventana {len(win_active)} · 24 h {len(day_active)} · "
        f"7 días {len(data['week'])}")
    background = [p for p in cards if p.background]
    if background:
        add(f"- Con lotes que siguieron solos, sin tocar botones en 24 h: {len(background)}")
    if data["no_hero"]:
        add(f"- Cuentas sin héroe que tocaron botones en 24 h (creando o sin terminar): {len(data['no_hero'])}")
    errors = service.telemetry_errors()
    if errors:
        add(f"- Errores al medir desde que arrancó el bot: {errors} (el juego siguió; avisar a Claude)")
    add("")

    add("2. PROMEDIOS POR JUGADOR ACTIVO")
    lines += _avg_lines(data)
    add("")

    add("3. QUÉ HACEN MÁS")
    for label, recs in (("ventana", data["win"]), ("24 h", data["day"])):
        cats: Counter[str] = Counter()
        timed: Counter[str] = Counter()
        for rec in recs.values():
            cats.update(rec.get("cats") or {})
            timed.update(rec.get("timed") or {})
        add(f"- Botones por tipo ({label}): {_share(dict(cats), CATEGORY_NAMES, CATEGORIES)}")
        total = sum(timed.values())
        if total:
            parts = sorted(timed, key=lambda k: -timed[k])
            add(f"- Tiempo de actividades ({label}): " + " · ".join(
                f"{ACTIVITY_NAMES.get(k, k)} {_minutes(timed[k])} ({_num(100 * timed[k] / total, 0)} %)" for k in parts))
    mains = Counter(p.main for p in cards if p.main)
    if mains:
        add("- Contenido principal de cada jugador (24 h, por botones, sin contar menús): " + " · ".join(
            f"{CATEGORY_NAMES.get(k, k)} {n}" for k, n in mains.most_common()))
    add("")

    add("4. LO QUE MÁS SE RECOLECTA")
    for label, recs in (("ventana", data["win"]), ("24 h", data["day"])):
        items: Counter[str] = Counter()
        found: Counter[str] = Counter()
        for rec in recs.values():
            items.update(rec.get("items") or {})
            found.update(rec.get("found") or {})
        add(f"- {label}: {sum(items.values())} unidades · {_items_line(service, dict(items))}")
        if found:
            add(f"  hallazgos al explorar ({label}): {_items_line(service, dict(found), 6)}")
    add("")

    sample = cards
    add("5. QUIÉNES SON (los de las tarjetas)")
    if sample:
        levels = [p.hero.level for p in sample]
        add(f"- Nivel: promedio {_num(sum(levels) / len(levels))} · mínimo {min(levels)} · máximo {max(levels)}")
        groups = Counter(service.texts.t(f"class_group.{p.group}.name") for p in sample)
        add("- Clases: " + ", ".join(f"{g} {n}" for g, n in groups.most_common()))
        roles = Counter(p.role for p in sample)
        add("- Roles: " + ", ".join(f"{r} {n}" for r, n in roles.most_common()))
        langs = Counter(p.lang for p in sample)
        add("- Idioma: " + ", ".join(f"{lang} {n}" for lang, n in langs.most_common()))
        with_camp = sum(1 for p in sample if p.camp)
        with_guild = sum(1 for p in sample if p.guild and not p.camp)
        camps = sum(1 for _ in service.store.items("camp"))
        add(f"- Con campamento: {with_camp} · con gremio sin campamento: {with_guild} · de {len(sample)} · "
            f"campamentos en el mundo: {camps}")
    else:
        add("- Nadie jugó en las últimas 24 h.")
    add("")

    add("6. OFICIOS (los de las tarjetas)")
    learned = Counter(pid for p in sample for pid in (p.hero.learned or []))
    add("- Aprendidos: " + (", ".join(f"{service._prof_name(pid)} {n}" for pid, n in learned.most_common()) if learned
                            else "ninguno todavía"))
    ups = sum(p.day.get("rank_ups", 0) for p in sample)
    add(f"- Rangos de oficio subidos en 24 h: {ups}")
    add("")

    add("7. MOCHILA Y ECONOMÍA (los de las tarjetas)")
    if sample:
        golds = [p.hero.gold for p in sample]
        add(f"- Monedas: promedio {service._money(int(sum(golds) / len(golds)))} · mínimo {service._money(min(golds))} · "
            f"máximo {service._money(max(golds))}")
        types = [p.bag[0] for p in sample]
        add(f"- Mochila: promedio {_num(sum(types) / len(types))} tipos usados de {sample[0].bag[1] or 50} · "
            f"el que más, {max(types)}")
        carried: Counter[str] = Counter()
        for p in sample:
            for item_id, n in (p.hero.backpack or {}).items():
                if (service.content.items.get(item_id) or {}).get("kind") in ("material", "food"):
                    carried[item_id] += n
        add("- Lo que más llevan: " + _items_line(service, dict(carried), 8))
    add("")

    add("8. MAPA (los de las tarjetas)")
    if sample:
        far = [abs(p.hero.x) + abs(p.hero.y) for p in sample]
        add(f"- Distancia al Claro ahora (zonas): promedio {_num(sum(far) / len(far))} · la más lejana {max(far)}")
        known = [len(p.hero.known or []) for p in sample]
        add(f"- Zonas que recuerdan: promedio {_num(sum(known) / len(known))} · máximo {max(known)}")
        arrivals = sum(p.day.get("arrivals", 0) for p in sample)
        add(f"- Zonas a las que llegaron en 24 h (viajes): {arrivals}")
    add("")

    notes = [d for _, d in service.store.items("feedback") if until - DAY <= float(d.get("at", 0)) < until]
    add("9. FEEDBACK")
    add(f"- Mensajes de 💬 Feedback en las últimas 24 h: {len(notes)} (cada uno llega suelto a este chat).")
    add("")
    lines += market_lines(service, number=10)
    add("")

    add("11. DEJARON DE VENIR (jugaron en los últimos 7 días, pero no en las últimas 24 h)")
    if data["stopped"]:
        for p in data["stopped"]:
            add(f"- {p.at} · {p.hero.name} · nivel {p.hero.level} · última vez {_ago(until, p.seen)} ({_when(p.seen)} UTC)")
    else:
        add("- Nadie.")
    add("")
    malla = malla_lines(service, number=12)
    if malla:
        lines += malla
        add("")

    add(f"{13 if malla else 12}. TARJETAS POR JUGADOR (activos en las últimas 24 h, del más activo al menos)")
    if not cards:
        add("- Nadie jugó en las últimas 24 h.")
    for index, p in enumerate(cards, start=1):
        add("")
        lines += _card(service, p, index, until)
    return "\n".join(lines) + "\n"


def _card(service: Any, p: _Player, index: int, until: float) -> list[str]:
    """One player's card (section 12 or 13): who, where, how much they play and gather, what they do most."""
    h, win, day = p.hero, p.win, p.day
    out = [f"── {index}. {p.at} · {h.name} · {p.account} ──"]
    gained = f" (+{day.get('levels', 0)} en 24 h)" if day.get("levels") else ""
    out.append(f"Clase: {p.title} · rol {p.role} · nivel {h.level}{gained} · idioma {p.lang}")
    camp = f"campamento {p.camp}" if p.camp else (f"gremio {p.guild} (sin campamento)" if p.guild else "sin campamento ni gremio")
    out.append(f"Campamento: {camp}")
    out.append(f"Dónde está: {p.place} · ahora: {p.doing} · último botón: {_ago(until, p.seen)} ({_when(p.seen)} UTC)")
    if p.background:
        out.append("Sin botones en 24 h: su lote siguió solo.")
    out.append(f"Tiempo: ventana {win.get('active_minutes', 0)} min activos en {win.get('sessions', 0)} sesiones · "
               f"24 h {_minutes(day.get('active_minutes', 0))} activos en {day.get('sessions', 0)} sesiones")
    timed = day.get("timed") or {}
    if timed:
        out.append(f"Actividades con tiempo (24 h): {_minutes(_timed(day))} · " + " · ".join(
            f"{ACTIVITY_NAMES.get(k, k)} {_minutes(v)}" for k, v in sorted(timed.items(), key=lambda kv: -kv[1])))
    out.append(f"Botones: ventana {win.get('actions', 0)} · 24 h {day.get('actions', 0)} — "
               f"{_share(day.get('cats') or {}, CARD_NAMES, CATEGORIES)}")
    main = CATEGORY_NAMES.get(p.main, "nada medido") if p.main else "nada medido"
    by_time = f" · por tiempo: {ACTIVITY_NAMES.get(p.main_time, p.main_time)}" if p.main_time else ""
    out.append(f"Lo que más hace (24 h): {main}{by_time}")
    out.append(f"Recolectó: ventana {_gathered(win)} · 24 h {_gathered(day)} — {_items_line(service, day.get('items') or {})}")
    if day.get("found"):
        out.append(f"Hallazgos al explorar (24 h): {_items_line(service, day['found'], 6)}")
    out.append(f"Exploró (vueltas): 24 h {day.get('explore_steps', 0)} · recolectó (vueltas): 24 h {day.get('gather_steps', 0)}"
               f" · llegó a {day.get('arrivals', 0)} zonas")
    out.append(f"Peleas (24 h): {day.get('won', 0)} ganadas · {day.get('lost', 0)} perdidas · {day.get('fled', 0)} huidas"
               f" · ventana {_fights(win)}" + (f" · jefes vencidos {day['boss_wins']}" if day.get("boss_wins") else ""))
    made = day.get("made") or {}
    out.append(f"Fabricó (24 h): {day.get('crafts', 0)} veces — {_items_line(service, made, 8)}" if made else
               "Fabricó (24 h): nada")
    out.append(f"Experiencia: ventana +{win.get('xp', 0)} · 24 h +{day.get('xp', 0)} · rangos de oficio subidos {day.get('rank_ups', 0)}")
    out.append(f"Monedas (24 h): +{service._money(day.get('coins_in', 0))} / −{service._money(day.get('coins_out', 0))} · "
               f"tiene {service._money(h.gold)}")
    trade = []
    if day.get("mkt_bought") or day.get("mkt_sold"):
        trade.append(f"🏛️ Mercado: compró {day.get('mkt_bought', 0)} veces y vendió {day.get('mkt_sold', 0)}")
    if day.get("merchant_sold") or day.get("merchant_bought"):
        trade.append(f"🛒 Mercader: le vendió {day.get('merchant_sold', 0)} unidades y le compró {day.get('merchant_bought', 0)}")
    out.append("Comercio (24 h): " + (" · ".join(trade) if trade else "nada"))
    extra = []
    if day.get("dng_runs") or day.get("dng_fights"):
        extra.append(f"mazmorras: {day.get('dng_runs', 0)} entradas, {day.get('dng_fights', 0)} peleas")
    if day.get("quests") or day.get("tasks"):
        extra.append(f"misiones cerradas {day.get('quests', 0)} · encargos cobrados {day.get('tasks', 0)}")
    if day.get("given") or day.get("fed"):
        extra.append(f"al campamento: {day.get('given', 0)} materiales a obras · {day.get('fed', 0)} raciones a la despensa")
    if extra:
        out.append("También (24 h): " + " · ".join(extra))
    out.append(f"Oficios: {_prof_line(service, h)}")
    used, cap, loose, gear_cap = p.bag
    pbags = []
    try:
        pbags = [_item(service, i) for i in service._pbag_worn(h)]
    except Exception:                                     # noqa: BLE001
        pbags = []
    out.append(f"Mochila: {used}/{cap} tipos · equipo suelto {loose}/{gear_cap}"
               + (f" · 🎒 puestas: {', '.join(pbags)}" if pbags else "") + f" · equipo puesto {p.worn}/{p.slots} piezas")
    return out


CSV_BASE = ("cuenta", "arroba", "heroe", "clase", "rol", "nivel", "niveles_24h", "idioma", "campamento", "gremio", "x", "y",
            "lugar", "haciendo_ahora", "ultimo_boton_utc", "botones_3h", "botones_24h", "minutos_activos_3h",
            "minutos_activos_24h", "sesiones_3h", "sesiones_24h", "minutos_actividades_3h", "minutos_actividades_24h")
CSV_TAIL = ("contenido_principal_24h", "actividad_principal_24h", "recolectado_3h", "recolectado_24h", "recolectado_detalle_24h",
            "hallazgos_24h", "peleas_ganadas_3h", "peleas_ganadas_24h", "peleas_perdidas_3h", "peleas_perdidas_24h",
            "huidas_24h", "fabricaciones_3h", "fabricaciones_24h", "experiencia_3h", "experiencia_24h", "monedas_entraron_3h",
            "monedas_entraron_24h", "monedas_salieron_3h", "monedas_salieron_24h", "monedas_ahora", "mercado_compras_24h",
            "mercado_ventas_24h", "mercader_vendidas_24h", "mercader_compras_24h", "mazmorras_entradas_24h",
            "mazmorras_peleas_24h", "misiones_24h", "encargos_24h", "rangos_oficio_24h", "mochila_tipos", "mochila_tipos_tope",
            "equipo_suelto", "equipo_puesto", "oficios")


def _plain(label: str) -> str:
    """A name without its leading emoji ("🪵 Madera" -> "Madera"), for the .csv cells."""
    head, _, rest = label.partition(" ")
    return rest if rest and not any(ch.isalnum() for ch in head) else label


def _plain_items(service: Any, items: dict[str, int]) -> str:
    """{"madera": 30, "fibra": 10} -> "Madera:30; Fibra:10" (most first), for one .csv cell."""
    ranked = sorted(items.items(), key=lambda kv: (-kv[1], kv[0]))
    return "; ".join(f"{_plain(_item(service, i))}:{n}" for i, n in ranked if n)


def csv_header() -> list[str]:
    """The .csv columns: the base, buttons per kind of content (3 h and 24 h), then the rest (one header row, D-341)."""
    cats = [f"botones_{SHORT_NAMES[c]}_{w}" for c in CATEGORIES for w in ("3h", "24h")]
    return list(CSV_BASE) + cats + list(CSV_TAIL)


def _csv(service: Any, data: dict[str, Any]) -> str:
    """One row per player of the cards, the same numbers as the .txt (UTF-8 with BOM, so Excel shows the accents)."""
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\r\n")
    writer.writerow(csv_header())
    for p in data["cards"]:
        h, win, day = p.hero, p.win, p.day
        row: list[Any] = [p.account, p.handle, h.name, p.title, p.role, h.level, day.get("levels", 0), p.lang, p.camp, p.guild,
                          h.x, h.y, p.place, p.doing, _when(p.seen), win.get("actions", 0), day.get("actions", 0),
                          win.get("active_minutes", 0), day.get("active_minutes", 0), win.get("sessions", 0),
                          day.get("sessions", 0), int(round(_timed(win))), int(round(_timed(day)))]
        for c in CATEGORIES:
            row += [(win.get("cats") or {}).get(c, 0), (day.get("cats") or {}).get(c, 0)]
        detail = _plain_items(service, day.get("items") or {})
        found = _plain_items(service, day.get("found") or {})
        catalog = (service.content.professions or {}).get("professions") or {}
        profs = "; ".join(f"{_plain(service._prof_name(pid))}:{service._prof_rank(h, pid)}"
                          for pid, xp in sorted((h.professions or {}).items()) if xp > 0 and pid in catalog)
        row += [SHORT_NAMES.get(p.main, "") if p.main else "", ACTIVITY_NAMES.get(p.main_time, p.main_time or ""),
                _gathered(win), _gathered(day), detail, found, win.get("won", 0), day.get("won", 0), win.get("lost", 0),
                day.get("lost", 0), day.get("fled", 0), win.get("crafts", 0), day.get("crafts", 0), win.get("xp", 0),
                day.get("xp", 0), win.get("coins_in", 0), day.get("coins_in", 0), win.get("coins_out", 0),
                day.get("coins_out", 0), h.gold, day.get("mkt_bought", 0), day.get("mkt_sold", 0), day.get("merchant_sold", 0),
                day.get("merchant_bought", 0), day.get("dng_runs", 0), day.get("dng_fights", 0), day.get("quests", 0),
                day.get("tasks", 0), day.get("rank_ups", 0), p.bag[0], p.bag[1], p.bag[2], p.worn, profs]
        writer.writerow(row)
    return "﻿" + buffer.getvalue()


def market_lines(service: Any, number: int = 10) -> list[str]:
    """The 🏛️ player market of yesterday (a whole day) and of today so far, from "market_log" (D-320).

    [ES] Qué hace: las líneas del mercado entre jugadores para el informe (todos juntos): cuántas compras hubo, cuántas unidades
    y monedas cambiaron de mano, cuánto impuesto se quemó y cuántas órdenes se publicaron, cancelaron o vencieron; y cuántas
    órdenes hay abiertas ahora. D-335 (0.59): lo mismo de los 📜 pedidos de fabricación ("craft_*" de "market_log", que anota
    engine/service/craft_orders.py, y el espacio "craft_order"). Solo lee; "market_log" es del mercado (nunca se borra desde
    aquí). D-341: va con el número de sección que le da build (10). La llama: build(). Si cambia, afecta: lo que lee el equipo.
    """
    today = int(service._today())
    out = [f"{number}. MERCADO ENTRE JUGADORES"]
    for label, day in (("ayer", today - 1), ("hoy hasta ahora", today)):
        log = service.store.get("market_log", str(day)) or {}
        out.append(f"- {label}: compras {int(log.get('trades', 0))} · unidades {int(log.get('units', 0))} · monedas que "
                   f"cambiaron de mano (🥉) {int(log.get('coins', 0))} · impuesto quemado (🥉) {int(log.get('tax', 0))} · "
                   f"órdenes de venta {int(log.get('sell_orders', 0))} · pedidos de compra {int(log.get('buy_orders', 0))} · "
                   f"canceladas {int(log.get('cancelled', 0))} · vencidas {int(log.get('expired', 0))}")
    orders = [o for _, o in service.store.items("market_order")]
    out.append(f"- Órdenes abiertas ahora: {sum(1 for o in orders if o.get('side') == 'sell')} de venta · "
               f"{sum(1 for o in orders if o.get('side') == 'buy')} pedidos de compra")
    for label, day in (("ayer", today - 1), ("hoy hasta ahora", today)):     # D-335 (0.59): 📜 the crafting orders
        log = service.store.get("market_log", str(day)) or {}
        out.append(f"- Pedidos de fabricación {label}: publicados {int(log.get('craft_posted', 0))} · hechos "
                   f"{int(log.get('craft_done', 0))} · monedas a los artesanos (🥉) {int(log.get('craft_coins', 0))} · impuesto "
                   f"quemado (🥉) {int(log.get('craft_tax', 0))} · cancelados {int(log.get('craft_cancelled', 0))} · vencidos "
                   f"{int(log.get('craft_expired', 0))}")
    out.append(f"- Pedidos de fabricación abiertos ahora: {sum(1 for _ in service.store.items('craft_order'))}")
    return out


def malla_lines(service: Any, number: int = 12) -> list[str]:
    """Who had 🧥 mail pieces turned into leather by the 0.62.2 migration ("migrations"/"malla_to_leather"), or [] if none.

    [ES] Qué hace: si la migración de la 0.62.2 dejó su registro (formato {"at", "version", "accounts": {cuenta: {"hero",
    "handle", "pieces": [[de, a], ...]}}, "other": {...}}), lista a quién se le convirtió qué, con su @; si no convirtió nada,
    lo dice en una línea ("nadie tenía malla"). Sale solo en los informes de los 3 días que siguen al cambio (KEEP_SECONDS,
    lo mismo que guarda el servidor): el cambio corre una vez al arrancar y no hace falta repetirlo para siempre. Si no está
    el registro, no sale nada y nunca falla. Solo lee. La llama: build(). Si cambia, afecta: lo que lee el equipo.
    """
    try:
        record = service.store.get("migrations", "malla_to_leather")
    except Exception:                                     # noqa: BLE001
        return []
    if not record:
        return []
    try:
        at = record.get("at")
        if at is not None and service.clock.now() - float(at) > KEEP_SECONDS:   # only the 3 days after the change
            return []
        accounts = record.get("accounts") or {}
        out = [f"{number}. MALLA CONVERTIDA EN CUERO ({record.get('version', '0.62.2')}, {_when(float(record.get('at') or 0))} UTC)"]
        if not accounts and not any(v for v in (record.get("other") or {}).values()):
            out.append("- Nadie tenía piezas de malla: no hubo nada que cambiar.")
            return out
        out.append(f"- Jugadores con piezas convertidas: {len(accounts)}")
        for account, info in sorted(accounts.items(), key=lambda kv: str((kv[1] or {}).get("hero", ""))):
            info = info or {}
            pieces = info.get("pieces") or []
            moved = ", ".join(f"{_item(service, str(a))} → {_item(service, str(b))}" for a, b in
                              (pair for pair in pieces if isinstance(pair, (list, tuple)) and len(pair) == 2))
            out.append(f"- {info.get('handle') or 'sin @'} · {info.get('hero', '?')} · {account}: piezas {len(pieces)}"
                       + (f" ({moved})" if moved else ""))
        other = record.get("other") or {}
        if other:
            out.append("- Otros lugares: " + ", ".join(f"{k} {v if isinstance(v, (int, float)) else len(v)}"
                                                      for k, v in sorted(other.items()) if v))
        return out
    except Exception:                                     # noqa: BLE001 - an unexpected format never stops the report
        return [f"{number}. MALLA CONVERTIDA EN CUERO", "- El registro de la migración tiene otro formato: mirarlo a mano."]
