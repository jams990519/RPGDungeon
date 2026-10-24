"""📊 Light play telemetry for the team's reports: per account and per 3-hour slot (D-341 confirmed, D-344 provisional).

The owner (24-oct-2026) wants the reports chat to get, every 3 hours, who played, with their @, how much each one plays and
gathers and what kind of content each one does most; "a constant database report, so the server is not overloaded". This
module only COUNTS: every button and typed text (act, text), the timed activities a hero keeps running, the units that really
enter the backpack by gathering (also chopping, fishing and skinning), fights, crafts, XP, levels, coins, market trades,
dungeons and quests. Counts live in memory and go to the store at most once a minute per account (flush_telemetry, called by
tick()), in one record per account and slot ("telemetry", key "<slot>:<account>"); a restart can lose at most the last minute.
Records older than 3 days are deleted (the reports chat keeps the history). It never changes a rule, a hero or a screen, and
it knows nothing about Telegram: the account id is the client's, the report that reads this lives in adapters/reports.py.

[ES]
Para qué sirve: la medición liviana del juego para los informes del equipo (pedido del dueño, 24-oct-2026, D-341: "quiero que
    me saque los promedios de jugadores activos con más detalles, quiénes son, con su arroba, y cuál es el tipo de contenido que
    más hacen... la especificación de cuánto juegan y juntan, eso lo quiero por jugador"; "que sea como un reporte constante de
    base de datos, para evitar que el servidor se sobrecargue"). Cuenta, por cuenta y por tramo de 3 horas: los botones y textos
    por tipo de contenido (CATEGORIES), los minutos con al menos un botón, las sesiones (una pausa de más de 15 minutos corta la
    sesión), los minutos de actividades con tiempo (viajes, lotes de explorar, recolectar, talar, pescar y cazar, descanso), las
    unidades que entran de verdad a la mochila al recolectar, talar, pescar y despellejar (no por la experiencia de oficio), los
    hallazgos al explorar, las peleas ganadas, perdidas y huidas, lo fabricado, la experiencia, los niveles, las monedas que
    entran y salen, el 🏛️ Mercado y el 🛒 mercader, las mazmorras, las misiones y los encargos. Cómo se aplicó lo eligió Claude:
    D-344 (provisional). Es parte de GameService (una "mezcla", como LadderMixin), en su propio archivo.
Documento de diseño: diseno/01-plataforma/informes.md §2 (qué se mide) y §4 (cómo está hecho)
Módulo: M20 Administración y telemetría (D-241.4: telemetría con exportación; D-341, D-344)
Depende de: engine.core.events (escucha HeroCreated, ItemCrafted, CombatEnded, ProfessionRankUp, TravelArrived, BossDefeated y
    HeroFellForever en el bus del servicio), el almacén y el reloj del servicio; los ids de botón de engine/service/game.py
    (COMMANDS, se lee tarde para no importar en círculo) y de cada mezcla (ACTION_RULES copia sus prefijos)
Lo usan: engine/service/game.py (GameService hereda de esta clase; act() y text() llevan el decorador tracked; _save llama a
    _tel_saved; tick() llama a _tel_tick; __init__ llama a _tel_listen; _end_combat a _tel_items con lo despellejado;
    _explore_step a _tel_items con el hallazgo; _buy, _dng_fight a _tel_add), engine/service/story.py (_story_event llama a
    _tel_story; _quest_complete y _claim_daily a _tel_add), engine/service/market.py (_market_buy y _market_fill a _tel_add);
    adapters/reports.py (flush_telemetry, telemetry_window, telemetry_since, SLOT_SECONDS, KEEP_SECONDS, CATEGORIES)
Eventos que publica: ninguno
Eventos que escucha: HeroCreated, ItemCrafted, CombatEnded, ProfessionRankUp, TravelArrived, BossDefeated, HeroFellForever
Datos de los que es dueño: espacio "telemetry" (clave "<tramo>:<cuenta>", tramo = int(hora // 10800)): {"slot", "account",
    "actions", "cats" {tipo: botones}, "mins" [minutos del tramo con al menos un botón, 0-179], "sessions", "last" (hora del
    último botón), "timed" {actividad: minutos}, "items" {objeto: unidades recolectadas o despellejadas}, "found" {objeto:
    hallazgos al explorar}, "made" {objeto: unidades fabricadas}, "won", "lost", "fled", "crafts", "xp", "levels", "coins_in",
    "coins_out", "explore_steps", "gather_steps", "arrivals", "merchant_sold", "merchant_bought", "mkt_bought", "mkt_sold",
    "dng_runs", "dng_fights", "quests", "tasks", "given", "fed", "created", "rank_ups", "boss_wins", "fell", "camps_founded",
    "infiltrations", "enemy_camps", "base" (oro, experiencia, nivel, nombre y fin de la actividad del último guardado: la base
    para seguir contando después de un reinicio)}. Se borra a los 3 días (KEEP_SECONDS). Nunca toca un héroe ni otro espacio.
Reglas que nunca se rompen:
    1. Solo cuenta: nunca cambia un héroe, una regla, una pantalla ni lo que devuelve act() o text(). Un error al medir nunca
       corta una jugada (_quiet: se anota en "errors" y el juego sigue).
    2. Liviano (D-341: "para evitar que el servidor se sobrecargue"): nada se escribe por botón; se escribe como mucho una vez por
       minuto (FLUSH_SECONDS) y solo las cuentas que cambiaron. Un reinicio pierde como mucho el último minuto.
    3. El motor no sabe de Telegram: la cuenta es la del cliente y el @ lo guarda el adaptador (set_handle, "prefs").
    4. Lo del jugador se guarda para siempre (D-64): esto solo borra lo suyo ("telemetry") de más de 3 días.
Si cambias esto, revisa:
    - El informe: adapters/reports.py (lee telemetry_window y los nombres de CATEGORIES y de las actividades)
    - Los botones nuevos: un prefijo nuevo que no está en ACTION_RULES cuenta como "menus" (menús y otros) hasta sumarlo
    - Pruebas: tests/test_informes_por_jugador.py
"""

from __future__ import annotations

import functools
import re
from typing import Any, Callable

from engine.core.events import (BossDefeated, CombatEnded, HeroCreated, HeroFellForever, ItemCrafted, ProfessionRankUp,
                                TravelArrived)

SLOT_SECONDS = 3 * 3600         # D-341: a report every 3 hours, aligned to 00, 03, 06 … 21 UTC
KEEP_SECONDS = 3 * 86400        # D-341: "el servidor solo ... de los últimos 3 días no más"
FLUSH_SECONDS = 60              # D-344: counts go to the store at most once a minute (a restart loses at most that)
SESSION_GAP_SECONDS = 15 * 60   # D-344: a pause longer than 15 minutes starts a new session
NAMESPACE = "telemetry"
# D-344: the kinds of content a button belongs to, in report order. Stable ids (the report names them in Spanish).
# [ES] Los tipos de contenido de cada botón: explorar, recolectar (también talar y pescar), cazar y pelear, viajar, fabricar
# (refinar, cocinar, encantar, reparar y los oficios), mercado y mercader, campamento y gremio (obras, depósitos, fondo),
# mazmorras, misiones y tablón, social y chat, héroe y equipo, y menús y otros.
CATEGORIES = ("explore", "gather", "fight", "travel", "craft", "market", "camp", "dungeon", "quests", "social", "hero", "menus")
# Button ids (or prefixes) of each kind, first match wins (a new button that is not here counts as "menus").
# [ES] Prefijos de los botones de cada tipo; el primero que coincide gana. "guide" solo (el 🧭 camino guiado) es de misiones,
# pero "guides" y "guide:" (📚 Guías) son de menús: van antes.
ACTION_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("menus", ("guides", "guide:", "dudas", "duda:", "home", "refresh", "options", "opt:", "tz", "lang", "fb", "fbk:", "stop",
               "claro", "back", "fallen")),
    ("social", ("gmsg", "gchat", "players", "pcard:", "bio", "gesture:", "rel:")),
    ("dungeon", ("dungeon", "dgo", "dout")),
    ("gather", ("gather", "chop", "fish", "do:gather", "do:chop", "do:fish", "amt:gather", "amt:chop", "amt:fish")),
    ("explore", ("explore", "do:explore", "amt:explore", "recon", "rcn:", "infiltrate", "scrolls", "scr:", "gzones")),
    ("fight", ("hunt", "prey", "do:hunt", "amt:hunt", "boss", "assault", "defend", "trial", "atk", "ab:", "flee", "dodge")),
    ("travel", ("go:", "goto:", "goask:", "walk", "wlk:", "map", "zmap", "places", "plc:")),
    ("craft", ("oficios", "est:", "esto:", "rec:", "mk:", "myprof", "learnlist", "pview:", "learn:", "ptend", "cook", "ench",
               "enc:", "dis:", "dis!:", "pspec", "pspv:", "pspp:", "pspx", "ptitle", "pbook", "trainer", "rpr", "rpo:", "rpx:",
               "rpl")),
    ("market", ("mkt", "cord", "shop", "buy:", "sell:", "sellg:", "gems", "gem:")),
    ("camp", ("camp", "found", "rename", "cancel_name", "improve", "lvl", "grow", "claim:", "upgrades", "upw", "upg:", "upsvc",
              "crest", "csell", "ctaller", "tsew", "tchest", "know", "kstart:", "kgive", "upf:", "uprep", "svc:", "upact:",
              "upstop:", "upkeep", "research", "guild", "askjoin", "leave", "join:", "squads", "sqvote:", "sqmv:", "sqto:",
              "sqname", "gnew", "glist", "gcard:", "greq", "ginvite:", "gfund", "gmeet", "gfound", "gleave", "gmem", "goff:",
              "glead", "gkick", "garm", "ghelp:", "creqs", "cwjoin:", "gwleave", "gfcraft", "gflog", "gans:", "ginv:", "gcamp:",
              "cinv:", "cwait:", "donate", "feed")),
    ("quests", ("story", "squests", "board", "npcs", "npc:", "talk:", "ch:", "factions", "journal", "jshow", "origin", "orig:",
                "origpick:", "dly:", "cjournal", "hjournal", "guide")),
    ("hero", ("hero", "stats", "health", "talents", "tal:", "pt:", "role:", "respec", "dual", "bar", "hyb", "chcls", "chgrp:",
              "chpick:", "chok:", "bag", "potions", "resources", "res:", "wallet", "sew", "chest", "gear", "unequip", "item:",
              "equip:", "use:", "memento", "mem:", "pbags", "oath", "inn")),
)
# Typed codes ("/ir2", "/v02", "/r3"...), first match wins; plain shortcuts ("/stats") go through COMMANDS first.
# [ES] Los códigos escritos y a qué tipo van (los atajos exactos como /stats van por el botón que abren).
TYPED_RULES: tuple[tuple[re.Pattern[str], str], ...] = tuple((re.compile(pattern), category) for pattern, category in (
    (r"^/(saludar|brindar|bio)\b", "social"), (r"^/j_?\d", "social"),
    (r"^/(dudas|help|faq)\b", "menus"), (r"^/?d\d{1,3}$", "menus"),
    (r"^/diario\b", "quests"),
    (r"^/(ir|go)", "travel"),
    (r"^/(buscar|search)\b", "explore"), (r"^/rc_?\d", "explore"), (r"^/pm_?\d", "explore"), (r"^/z_?\d", "explore"),
    (r"^/(cf|co|cm)_?\d", "market"), (r"^/(c|s|b|k|o)_?\d", "market"), (r"^/v\d", "market"),
    (r"^/(rp|ro)_?\d", "craft"), (r"^/r_?\d", "craft"),
    (r"^/(mp|mq)_?\d", "hero"), (r"^/(e|q)_?\d", "hero"), (r"^/\d", "hero"),
    (r"^/(f|a|t|g|m)_?\d", "camp"), (r"^/inv_", "camp"),
))
FIGHT_VIEWS = ("combat", "combat_end")     # a button that lands in a fight is fighting (a potion, the bag)
COUNT_FIELDS = ("actions", "sessions", "won", "lost", "fled", "crafts", "xp", "levels", "coins_in", "coins_out",
                "explore_steps", "gather_steps", "arrivals", "merchant_sold", "merchant_bought", "mkt_bought", "mkt_sold",
                "dng_runs", "dng_fights", "quests", "tasks", "given", "fed", "created", "rank_ups", "boss_wins", "fell",
                "camps_founded", "infiltrations", "enemy_camps")
DICT_FIELDS = ("cats", "timed", "items", "found", "made")


def action_category(action_id: str) -> str:
    """The kind of content of a button id (ACTION_RULES; "menus" if no rule matches). [ES] Qué hace: dice el tipo de contenido de
    un botón. La llaman: _tel_action y las pruebas. Si cambia, afecta: el reparto de los informes."""
    for category, prefixes in ACTION_RULES:
        if action_id.startswith(prefixes):
            return category
    return "menus"


def typed_category(text: str) -> str:
    """The kind of content of a typed "/" command: its button if it is a shortcut (COMMANDS), else TYPED_RULES, else "menus".

    [ES] Qué hace: el tipo de contenido de un atajo escrito: si es un atajo de botón (/stats), el de su botón; si es un código
    (/ir2, /v02, /r3, /c1...), el de TYPED_RULES; si no, menús (una palabra de oficio, /minero, la reconoce _tel_pre_text con
    el catálogo de oficios). La llama: _tel_pre_text. Si cambia, afecta: el reparto de los informes.
    """
    from engine.service.game import COMMANDS, TYPED_ALIASES     # lazy: game.py imports this module
    low = text.strip().lower()
    word = low.split()[0].split("@")[0] if low.split() else ""
    word = TYPED_ALIASES.get(word, word)
    if word in COMMANDS:
        return action_category(COMMANDS[word])
    for pattern, category in TYPED_RULES:
        if pattern.match(low):
            return category
    return "menus"


def tracked(kind: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorate a public entry point (act, text) so each call a client makes is counted once (nested calls are not).

    [ES] Qué hace: cuenta cada botón (act) o texto (text) que manda un cliente, una sola vez aunque text() llame a act() por
    dentro. Lo de antes de la jugada (para un texto suelto, qué pantalla esperaba el texto) se mira antes; el tipo final, con
    la vista que devolvió (una pelea es pelear). La usan: act y text de GameService. Si cambia, afecta: lo que cuentan los
    informes, nunca la jugada.
    """
    def decorate(method: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(method)
        def wrapper(self: Any, account_id: str, arg: str, *args: Any, **kwargs: Any) -> Any:
            if getattr(self, "_tel_depth", 0):
                return method(self, account_id, arg, *args, **kwargs)
            pre = self._tel_pre(kind, account_id, arg)
            self._tel_depth = 1
            try:
                view = method(self, account_id, arg, *args, **kwargs)
            finally:
                self._tel_depth = 0
            self._tel_action(account_id, kind, arg, pre, getattr(view, "kind", ""))
            return view
        return wrapper
    return decorate


def _quiet(method: Callable[..., Any]) -> Callable[..., Any]:
    """Telemetry never breaks a move: an error is counted in the state ("errors") and the game goes on (rule 1)."""
    @functools.wraps(method)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        try:
            return method(self, *args, **kwargs)
        except Exception:                                   # noqa: BLE001 - measuring must never stop a move
            state = self._tel_state()
            state["errors"] = state.get("errors", 0) + 1
            return None
    return wrapper


def merge(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Add several slot records of one account into one (counts and dicts summed, "active_minutes" = minutes with a button).

    [ES] Qué hace: suma los tramos de una cuenta en una ventana (3 h, 24 h): los contadores y los diccionarios se suman, los
    minutos con botón se cuentan ("active_minutes") y "last" es el último botón. La usan: telemetry_window y las pruebas.
    """
    out: dict[str, Any] = {field: 0 for field in COUNT_FIELDS}
    out.update({field: {} for field in DICT_FIELDS})
    out["active_minutes"] = 0
    out["last"] = 0.0
    out["slots"] = 0
    for rec in records:
        out["slots"] += 1
        for field in COUNT_FIELDS:
            out[field] += rec.get(field, 0) or 0
        for field in DICT_FIELDS:
            for key, n in (rec.get(field) or {}).items():
                out[field][key] = out[field].get(key, 0) + n
        out["active_minutes"] += len(rec.get("mins") or [])
        out["last"] = max(out["last"], float(rec.get("last") or 0.0))
    for key, value in out["timed"].items():
        out["timed"][key] = round(value, 1)
    return out


class TelemetryMixin:
    """The light per-account, per-slot play telemetry (D-341, D-344). Mixed into GameService; uses its store and clock.

    [ES]
    Qué es: los contadores de juego de cada cuenta por tramo de 3 horas, en memoria y guardados una vez por minuto.
    Quién la usa: GameService (hereda de esta clase) y el informe (adapters/reports.py).
    Si cambia, afecta: lo que dicen los informes de jugadores; nunca el juego.
    """

    # ------------------------------------------------------------------ state

    def _tel_state(self) -> dict[str, Any]:
        """The in-memory buffer (created on first use): records touched, dirty keys, caches per account, last flush."""
        state = self.__dict__.get("_tel")
        if state is None:
            state = {"recs": {}, "dirty": set(), "accounts": {}, "flushed_at": self.clock.now(), "pruned": None, "errors": 0}
            self.__dict__["_tel"] = state
        return state

    def _tel_slot(self, now: float | None = None) -> int:
        return int((self.clock.now() if now is None else now) // SLOT_SECONDS)

    def _tel_rec(self, account: str, now: float | None = None) -> dict[str, Any]:
        """The record of this account in the current slot: from memory, else the store, else a new one (not written yet)."""
        state = self._tel_state()
        slot = self._tel_slot(now)
        key = f"{slot}:{account}"
        rec = state["recs"].get(key)
        if rec is None:
            rec = self.store.get(NAMESPACE, key) or {"slot": slot, "account": account}
            state["recs"][key] = rec
        return rec

    def _tel_touch(self, account: str) -> dict[str, Any]:
        """The current record of an account, marked to be written at the next flush."""
        rec = self._tel_rec(account)
        self._tel_state()["dirty"].add(f"{rec['slot']}:{account}")
        return rec

    def _tel_cache(self, account: str) -> dict[str, Any]:
        """What the telemetry remembers of an account between moves: its last button and the base of its last save. After a
        restart it comes from the newest record (this slot's or the one before), so a session and the counts go on."""
        state = self._tel_state()
        cache = state["accounts"].get(account)
        if cache is None:
            rec = self._tel_rec(account)
            if "base" not in rec and "last" not in rec:
                rec = self.store.get(NAMESPACE, f"{self._tel_slot() - 1}:{account}") or {}
            cache = {"last": rec.get("last"), "base": rec.get("base")}
            state["accounts"][account] = cache
        return cache

    # ------------------------------------------------------------------ hooks

    def _tel_pre(self, kind: str, account: str, arg: str) -> str | None:
        """Before a typed text is handled: its kind of content (the screen waiting for it decides; a button needs nothing)."""
        if kind != "text":
            return None
        try:
            return self._tel_pre_text(account, arg)
        except Exception:                                   # noqa: BLE001 - rule 1
            return "menus"

    def _tel_pre_text(self, account: str, text: str) -> str:
        """The kind of content of a typed text: a "/" command by its code; loose text by the screen that waits for it (the
        hero's name, a camp's name, 💬 Feedback, ❓ Dudas, a 🏛️ price or a 📜 fee), else a message to the guild (social)."""
        if text.strip().startswith("/"):
            category = typed_category(text)
            if category == "menus" and self._prof_code(text):
                return "craft"                              # /minero, /herreria: a profession's screen (D-257)
            return category
        if self.store.get("hero", account) is None:
            return "menus"                                  # the hero's name while creating it
        if self.store.get("camp_naming", account):
            return "camp"
        if self.store.get("feedback_open", account) or self.store.get("dudas_open", account):
            return "menus"
        if self.store.get("market_open", account) or self.store.get("corder_open", account):
            return "market"
        return "social"                                     # D-285: loose text is a message to the guild

    @_quiet
    def _tel_action(self, account: str, kind: str, arg: str, pre: str | None, view_kind: str) -> None:
        """Count one button or text: its kind of content, the minute, and a new session after a pause of 15 minutes or more."""
        now = self.clock.now()
        category = pre if kind == "text" else action_category(arg or "")
        if view_kind in FIGHT_VIEWS and category in ("hero", "menus"):
            category = "fight"
        cache = self._tel_cache(account)
        rec = self._tel_touch(account)
        rec["actions"] = rec.get("actions", 0) + 1
        cats = rec.setdefault("cats", {})
        cats[category] = cats.get(category, 0) + 1
        minute = int((now - rec["slot"] * SLOT_SECONDS) // 60)
        mins = rec.setdefault("mins", [])
        if minute not in mins:
            mins.append(minute)
        last = cache.get("last")
        if last is None or now - float(last) > SESSION_GAP_SECONDS:
            rec["sessions"] = rec.get("sessions", 0) + 1
        cache["last"] = now
        rec["last"] = now

    @_quiet
    def _tel_add(self, account: str, **counts: int) -> None:
        """Add to plain counters of an account (merchant, market, dungeons, quests...)."""
        if not account:
            return
        rec = self._tel_touch(account)
        for field, n in counts.items():
            rec[field] = rec.get(field, 0) + n

    @_quiet
    def _tel_items(self, account: str, field: str, items: dict[str, int]) -> None:
        """Add units per item to a dict counter ("items": gathered or skinned; "found": exploring; "made": crafted)."""
        items = {k: int(n) for k, n in (items or {}).items() if n}
        if not account or not items:
            return
        rec = self._tel_touch(account)
        bucket = rec.setdefault(field, {})
        for item_id, n in items.items():
            bucket[item_id] = bucket.get(item_id, 0) + n

    @_quiet
    def _tel_saved(self, hero: Any) -> None:
        """After a hero is saved: coins in and out, XP and levels gained, and the minutes of timed activity it took on, as the
        difference with its last save (the first save of an account after a restart without a record only sets the base)."""
        now = self.clock.now()
        activity = hero.activity or {}
        label = activity.get("kind") or ""
        if label == "gather":                               # D-305, D-306.5: 🪓 Talar and 🎣 Pescar are modes of gathering
            label = activity.get("mode") or ("chop" if activity.get("only") else "gather")
        until = float(activity.get("until") or 0.0)
        cur = {"name": hero.name, "gold": int(hero.gold), "xp": int(hero.xp), "level": int(hero.level), "until": until,
               "act": label}
        cache = self._tel_cache(hero.id)
        base = cache.get("base")
        cache["base"] = cur
        if not base or base.get("name") != hero.name:       # first sight, or a new hero on the account (D-336)
            return
        coins = cur["gold"] - int(base.get("gold", 0))
        xp = cur["xp"] - int(base.get("xp", 0))
        levels = cur["level"] - int(base.get("level", 0))
        minutes = 0.0
        if label and until > now:
            if label != base.get("act"):
                minutes = (until - now) / 60.0              # a new activity: the time it takes from now
            elif until > float(base.get("until") or 0.0):
                minutes = (until - max(now, float(base.get("until") or 0.0))) / 60.0    # the next step of the same one
        elif not label:
            cur["until"] = min(until, now)
        if not (coins or xp > 0 or levels > 0 or minutes > 0):
            return
        rec = self._tel_touch(hero.id)
        if coins > 0:
            rec["coins_in"] = rec.get("coins_in", 0) + coins
        elif coins < 0:
            rec["coins_out"] = rec.get("coins_out", 0) - coins
        if xp > 0:
            rec["xp"] = rec.get("xp", 0) + xp
        if levels > 0:
            rec["levels"] = rec.get("levels", 0) + levels
        if minutes > 0:
            timed = rec.setdefault("timed", {})
            timed[label] = round(timed.get(label, 0.0) + minutes, 2)

    @_quiet
    def _tel_story(self, hero: Any, kind: str, data: dict[str, Any]) -> None:
        """What the story hook sees (_story_event): exploring and gathering rounds, the units gathered, merchant sales, food
        for the pantry, gifts to the works, infiltrations, enemy camps destroyed and camps founded. Fights and crafts come
        from their events (CombatEnded, ItemCrafted), not from here."""
        account = hero.id
        if kind == "explore":
            self._tel_add(account, explore_steps=1)
        elif kind == "gather":
            self._tel_add(account, gather_steps=1)
            self._tel_items(account, "items", data.get("items") or {})
        elif kind == "sell":
            self._tel_add(account, merchant_sold=int(data.get("n", 0) or 0))
        elif kind == "feed":
            self._tel_add(account, fed=int(data.get("rations", 0) or 0))
        elif kind == "build":
            self._tel_add(account, given=int(data.get("n", 0) or 0))
        elif kind == "infiltrate":
            self._tel_add(account, infiltrations=1)
        elif kind == "enemy_camp" and data.get("destroyed"):
            self._tel_add(account, enemy_camps=1)
        elif kind == "camp":
            self._tel_add(account, camps_founded=1)

    def _tel_listen(self) -> None:
        """Subscribe to the engine events the report counts (called once by GameService.__init__)."""
        bus = self.bus
        bus.subscribe(HeroCreated, lambda e: self._tel_add(e.hero_id, created=1))
        bus.subscribe(ItemCrafted, self._tel_on_crafted)
        bus.subscribe(CombatEnded, self._tel_on_fight)
        bus.subscribe(ProfessionRankUp, lambda e: self._tel_add(e.hero_id, rank_ups=1))
        bus.subscribe(TravelArrived, lambda e: self._tel_add(e.hero_id, arrivals=1))
        bus.subscribe(BossDefeated, lambda e: self._tel_add(e.hero_id, boss_wins=1))
        bus.subscribe(HeroFellForever, lambda e: self._tel_add(e.hero_id, fell=1))

    def _tel_on_crafted(self, event: ItemCrafted) -> None:
        self._tel_add(event.hero_id, crafts=1)
        self._tel_items(event.hero_id, "made", {event.item_id: int(event.count)})

    def _tel_on_fight(self, event: CombatEnded) -> None:
        field = {"victory": "won", "defeat": "lost", "fled": "fled"}.get(event.outcome)
        if field:
            self._tel_add(event.hero_id, **{field: 1})

    # ------------------------------------------------------------------ flush and reading

    @_quiet
    def _tel_tick(self) -> None:
        """From tick() (every few seconds): write the counts if a minute went by since the last write (rule 2)."""
        if self.clock.now() - float(self._tel_state()["flushed_at"]) >= FLUSH_SECONDS:
            self.flush_telemetry()

    def flush_telemetry(self) -> int:
        """Write every record that changed since the last write, forget older slots in memory and, once per slot, delete
        records older than 3 days from the store. Returns how many records it wrote.

        [ES]
        Qué hace: guarda los contadores que cambiaron (una escritura por cuenta y tramo) con la base del último guardado de cada
        héroe, para seguir contando después de un reinicio; olvida en memoria los tramos viejos y, una vez por tramo, borra del
        almacén lo de más de 3 días (KEEP_SECONDS). La llaman: _tel_tick (como mucho una vez por minuto) y el informe antes de
        armarse (adapters/reports.py). Si cambia, afecta: cuánto escribe el servidor y lo que lee el informe.
        """
        state = self._tel_state()
        now = self.clock.now()
        slot = self._tel_slot(now)
        written = 0
        for key in sorted(state["dirty"]):
            rec = state["recs"].get(key)
            if rec is None:
                continue
            cache = state["accounts"].get(rec.get("account", ""))
            if cache and cache.get("base"):
                rec["base"] = dict(cache["base"])
            self.store.put(NAMESPACE, key, rec)
            written += 1
        state["dirty"] = set()
        state["flushed_at"] = now
        state["recs"] = {k: r for k, r in state["recs"].items() if int(r.get("slot", 0)) >= slot}
        if state.get("pruned") != slot:
            self._tel_prune(slot)
            state["pruned"] = slot
        return written

    def _tel_prune(self, slot: int) -> None:
        """Delete the "telemetry" records of slots older than KEEP_SECONDS (rule 4: only its own data)."""
        oldest = slot - KEEP_SECONDS // SLOT_SECONDS
        for key, rec in list(self.store.items(NAMESPACE)):
            if int(rec.get("slot", 0)) < oldest:
                self.store.delete(NAMESPACE, key)

    def telemetry_window(self, since: float, until: float) -> dict[str, dict[str, Any]]:
        """Every account's counts for the slots that start in [since, until), merged (merge). Reads the store: flush first.

        [ES] Qué hace: junta, por cuenta, los tramos de una ventana (los de las últimas 3 h, las últimas 24 h...). La llama: el
        informe (adapters/reports.py), después de flush_telemetry. Si cambia, afecta: lo que dice el informe.
        """
        first, last = int(since // SLOT_SECONDS), int(until // SLOT_SECONDS)
        grouped: dict[str, list[dict[str, Any]]] = {}
        for _, rec in self.store.items(NAMESPACE):
            if first <= int(rec.get("slot", -1)) < last and rec.get("account"):
                grouped.setdefault(rec["account"], []).append(rec)
        return {account: merge(recs) for account, recs in grouped.items()}

    def telemetry_since(self) -> float | None:
        """When the oldest slot still in the store starts (the report says since when it measures), or None."""
        slots = [int(rec.get("slot", 0)) for _, rec in self.store.items(NAMESPACE)]
        return min(slots) * SLOT_SECONDS if slots else None

    def telemetry_errors(self) -> int:
        """How many times measuring failed since the bot started (rule 1: the game went on). [ES] Para el informe."""
        return int(self._tel_state().get("errors", 0))
