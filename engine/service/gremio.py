"""Guild from the first moment (D-269), 👥 Jugadores at the bonfire (D-265) and camp works that take time: a GameService mixin.

A hero can create a guild before having a camp (🥉20, a free name, 5 members). Others ask to join and the leader or an
officer accepts (or the leader invites from a player's card). The guild shows where each member is and what they do,
carries 📢 messages to every member, keeps a fund that every member fills from wherever they are, and has a 📍 meeting
point. The leader founds the camp where he stands with at least 2 members present: the fund pays, and the founding is a
work in progress that advances with the members present (1 h with 2, 30 min with 4, never under 10 min). When it ends, the
camp is created with the guild's name, the guild becomes the camp's guild (the D-97 record) and every other member is
invited. Every camp improvement whose materials are complete is also a work in progress (60 min x its level x 2 / members
present in the camp's territory). Works advance lazily: on every order of a member and in tick() when one is due.

[ES]
Para qué sirve: el gremio desde el primer momento (D-269, reemplaza a D-252), la pantalla 👥 Jugadores de la fogata (D-265 y
    D-274.1-2), el botón 🏗️ Moverte a la construcción de 📍 Zona (pedido del dueño, 18-oct) y las obras que tardan (D-269.4,
    D-274.4). Las reglas chicas que no dijo el dueño (salir, el fondo, presentes, obras a la vez...) están en D-275 (provisional). Es parte de GameService (una "mezcla", como StoryMixin y GuideMixin), en su propio archivo para no agrandar game.py.
Documento de diseño: diseno/09-construccion/escalera-del-asentamiento.md §0 (cómo está D-269 en el juego);
    diseno/01-plataforma/menus-campamento-y-heroe.md (👥 Jugadores en la fogata); diseno/08-social/gremios-y-social.md §0
Módulo: capa de servicios (M15 Social: el gremio; M14 Construcción: la fundación y las obras con tiempo)
Depende de: content/balance.yaml (bloques gremio, works, bonfire, presence, camps y guild), content/locales/es_gremio.yaml y
    en_gremio.yaml (textos), engine.social.guilds (contadores del gremio del campamento, D-97), engine.hero, engine.messaging y las
    ayudas de GameService (_zone, _zone_name, _money, _item_list, _bar, _fmt_duration, _seconds, _join, _ago, _banner,
    _emblem_name, _load, _save, _push, _push_each, _speaking, _name_key, _camp_requirements, _camp_here_view, _main_view,
    _guild_view, _members_cap, _upgrades, _upgrade_catalog, _upgrade_name, _create_camp, _territory, _trip_seconds, _zone_players)
Lo usan: engine/service/game.py (GameService hereda de esta clase): act() (las respuestas "gans:", "ginv:", "gcamp:" antes del
    combate y _works_settle después de _settle), view() y text() (_works_settle; los códigos /j1 /p1, /g1, /m1 y /f02;
    _gremio_text desde _name_camp), tick() (_works_tick), _idle_action (GREMIO_ACTIONS, "found" → _start_founding),
    _guild_view (sin campamento abre _gremio_view), _camp_hub_lines y _camp_hub_actions (👥 Jugadores en la fogata),
    _camp_requirements (las condiciones del gremio para fundar), _camp_here_view (la fundación en curso), _zone_view y
    _activity_view (🏗️ Moverte a la construcción), _important_places y _can_goto (el punto de reunión y la construcción),
    _give_to_work, _open_works y _upgrades_view (las obras en curso y el fondo del campamento)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño:
    "gremio" (clave el id del gremio, "g1", "g2"…; nunca se reutiliza): {"id", "name", "leader", "officers" [cuentas],
        "members" [cuentas, el líder primero], "requests" [quién pidió entrar], "invites" [a quién invitó el líder o un oficial],
        "created", "messages" [{"by", "id", "text", "at"}, los últimos gremio.messages_kept], "fund" {objeto: cantidad},
        "gave" {cuenta: {objeto: cantidad}} (quién dio qué, para siempre), "meet" [x, y] o None y "meet_by" (el 📍 punto de
        reunión), "founding" (la fundación en curso: {"x", "y", "need", "done", "at", "floor", "started", "paid"} o None),
        "camp" ("x:y" del campamento ya fundado) e "invited" [miembros que todavía no respondieron la invitación al campamento],
        "closed" (True si se disolvió: su nombre queda libre)}
    "gremio_of" (clave la cuenta): {"gremio": id}: a qué gremio pertenece (antes del campamento, o mientras espera responder
        la invitación). Después de fundar, el gremio de un miembro es el de su campamento (Hero.camp, D-97).
    "gremio_codes" (clave la cuenta): el orden de la última lista que vio con códigos ({"players", "guilds", "members"}): solo
        pantalla, como "places_shown".
    "works_open" (clave "found:<id>" o "build:<x:y>"): {"kind": "found" o "build", "ref", "eta"}: índice de las obras en curso,
        para que tick() solo mire las que ya podrían haber terminado.
    "meta"/"gremio_seq": {"n"}: el último número de gremio usado.
    Además: "guild_name" y "camp_name" guardan {"gremio": id} mientras el gremio no tiene campamento (el nombre queda
        reservado para los dos); el campamento guarda "gremio" (id) y el gremio D-97 del campamento también; "upgrades" guarda
        "building" {mejora: {"need", "done", "at", "floor", "by", "started"}} (obras en curso) y "fund" {objeto: cantidad} (lo
        que sobró del fondo al fundar: se usa primero al aportar a una obra).
Reglas que nunca se rompen:
    1. Un gremio por héroe: quien es miembro de un campamento tiene el gremio de su campamento (D-97) y no entra a otro.
    2. Antes del campamento caben gremio.members_before_camp (5); entra quien pide y acepta el líder o un oficial (o quien
       acepta la invitación del líder o un oficial). Nadie entra a la fuerza.
    3. Lo depositado en el fondo es del gremio: no vuelve a quien lo dio (queda anotado en "gave"); si el último miembro
       disuelve el gremio, el fondo vuelve entero a su mochila. Nada se pierde.
    4. Una obra (fundar o una mejora) avanza solo con miembros presentes (D-274.6: en la zona, o en el territorio para las
       mejoras, jugaron en los últimos presence.minutes o exploran, recolectan, cazan o duermen ahí): tiempo = minutos ×
       referencia ÷ presentes, nunca menos del piso; con nadie, se pausa. Lo construido nunca se borra.
    5. Las mejoras que ya estaban construidas siguen construidas; los campamentos y gremios de antes siguen igual (D-64).
    6. Ningún texto visible se escribe aquí: todo sale de content/locales (es_gremio.yaml y en_gremio.yaml), y todo aviso
       a otro jugador se arma con _push_each (le llega en su idioma, D-250).
Si cambias esto, revisa:
    - Números: balance.yaml gremio, works, bonfire.cap, presence.bonfire_seconds, camps.found_cost y guild.levels[0].capacity
    - Servicio: engine/service/game.py (los ganchos de "Lo usan"); engine/service/guide.py (el paso "found" lee
      _camp_requirements y se completa con el evento "camp" que manda _create_camp)
    - Pantallas y botones: HUB_KINDS ("gremio": hasta 8 botones), el layout de 📍 Zona ([2, 2, 1, 1] o [2, 2, 1, 1, 1] con
      🏗️ Moverte a la construcción) y los ids de GREMIO_ACTIONS y GREMIO_ANSWERS (64 bytes como máximo en Telegram)
    - Mapa de impacto: diseno/01-plataforma/mapa-de-impacto.md (el gremio desde el inicio y las obras con tiempo)
    - Pruebas: tests/test_gremio_desde_el_inicio.py; tests/test_camps.py (found_at funda por el gremio), tests/test_guilds.py,
      tests/test_camp_upgrades.py (las obras con tiempo), tests/test_menus_y_dudas.py (la fogata con 👥 Jugadores)
"""

from __future__ import annotations

import re
import unicodedata
from typing import Any

from engine.hero import Hero
from engine.messaging import Action, View
from engine.social import guilds as guild_rules

# Typed codes of the guild screens. [ES] /j1 (o /p1 en inglés): la tarjeta de un jugador de 👥 Jugadores; /g1: un gremio de
# 🔎 Buscar gremio; /m1: un miembro de tu gremio; /f02: depositar en el fondo todo lo que llevas del recurso 02 (su código de
# 📦 Recursos, como /v02 al vender).
PLAYER_CODE_RE = re.compile(r"^/(?:j|p)_?(\d{1,2})(@\w+)?$")
GUILD_CODE_RE = re.compile(r"^/g_?(\d{1,2})(@\w+)?$")
MEMBER_CODE_RE = re.compile(r"^/m_?(\d{1,2})(@\w+)?$")
FUND_CODE_RE = re.compile(r"^/f(\d{1,3})(@\w+)?$")
# Guild names follow the camp names (the camp takes the guild's name when it is founded). [ES] Igual que CAMP_NAME_RE.
GREMIO_NAME_RE = re.compile(r"^[^\W_][\w '\-]{2,23}$", re.UNICODE)
# Button ids (or prefixes) that _gremio_action routes (menus: they also work while busy). [ES] Si cambian, cambian los botones.
GREMIO_ACTIONS = ("players", "pcard:", "gnew", "glist", "gcard:", "greq:", "greqs", "ginvite:", "gmsg", "gfund", "gmeet",
                  "gmeetset", "gfound", "gfoundx", "gleave", "gmem:", "goff:", "glead:", "glead!:", "gkick:", "gkick!:")
# Answers that arrive as pushes: handled before the combat check, like "join:". [ES] Las respuestas que llegan como aviso.
GREMIO_ANSWERS = ("gans:", "ginv:", "gcamp:")
EPS = 1e-6


def _busy_kinds() -> tuple[str, ...]:
    """The activities that keep a hero present in its zone with the chat closed (game.PRESENT_BUSY, D-96)."""
    from engine.service.game import PRESENT_BUSY          # lazy: game.py imports this module
    return PRESENT_BUSY


def _plain(text: str) -> str:
    """Lower case, no accents: what a guild search compares."""
    norm = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in norm if not unicodedata.combining(ch)).casefold()


class GremioMixin:
    """Guild-from-the-start, bonfire players and timed works part of GameService (needs its store, texts and helpers).

    [ES]
    Qué es: la parte del gremio desde el inicio, de 👥 Jugadores y de las obras con tiempo, en su propio archivo.
    Quién la usa: GameService (hereda de aquí).
    Si cambia, afecta: la fogata, el gremio antes del campamento, cómo se funda un campamento y cuánto tardan sus mejoras.
    """

    # ------------------------------------------------------------------ data and links

    def _gremio_cfg(self) -> dict[str, Any]:
        return self.content.balance.get("gremio", {})

    def _gremio(self, gid: str | None) -> dict[str, Any] | None:
        return self.store.get("gremio", gid) if gid else None

    def _gremio_link(self, account: str) -> dict[str, Any] | None:
        """The guild record this account belongs to through "gremio_of" (before its camp, or waiting to answer it)."""
        link = self.store.get("gremio_of", account)
        record = self._gremio(link.get("gremio")) if link else None
        return record if record and not record.get("closed") else None

    def _my_gremio(self, hero: Hero) -> dict[str, Any] | None:
        """The hero's guild before it has a camp (None after founding: then its guild is its camp's, D-97)."""
        record = self._gremio_link(hero.id)
        return record if record and not record.get("camp") and hero.id in record.get("members", []) else None

    def _gremio_free(self, account: str, data: Hero | dict[str, Any] | None) -> bool:
        """True if this player can create or join a guild: no guild and no camp (rule 1)."""
        if data is None:
            return False
        camp = data.camp if isinstance(data, Hero) else data.get("camp")
        return camp is None and self._gremio_link(account) is None

    def _gremio_manager(self, record: dict[str, Any], account: str) -> bool:
        """The leader or an officer (they accept requests and invite, D-253)."""
        return account == record.get("leader") or account in record.get("officers", [])

    def _gremio_cap(self) -> int:
        return int(self._gremio_cfg().get("members_before_camp", 5))

    def _gremio_room(self, record: dict[str, Any]) -> bool:
        return len(record.get("members", [])) < self._gremio_cap()

    def _hero_data(self, account: str, actor: Hero | None) -> dict[str, Any] | None:
        """x, y, seen_at, activity, name, level, class_id and camp of a player: the actor's fresh copy, else the stored one."""
        if actor is not None and account == actor.id:
            return {"x": actor.x, "y": actor.y, "seen_at": actor.seen_at, "activity": actor.activity, "name": actor.name,
                    "level": actor.level, "class_id": actor.class_id, "camp": actor.camp}
        return self.store.get("hero", account)

    def _hero_name(self, account: str) -> str:
        return (self.store.get("hero", account) or {}).get("name", "?")

    def _guild_name_of(self, account: str, data: dict[str, Any] | None = None) -> str:
        """The name of a player's guild: its guild before the camp, or its camp's guild (D-97); "" if none."""
        record = self._gremio_link(account)
        if record:
            return record["name"]
        data = data if data is not None else self.store.get("hero", account)
        camp = (data or {}).get("camp")
        guild = self.store.get("guild", camp) if camp else None
        return guild["name"] if guild else ""

    def _codes(self, hero: Hero, kind: str, ids: list[str]) -> None:
        """Remember the order of a list with codes (/j1, /g1, /m1) so a code is what the player saw."""
        record = self.store.get("gremio_codes", hero.id) or {}
        record[kind] = ids
        self.store.put("gremio_codes", hero.id, record)

    def _code_target(self, hero: Hero, kind: str, n: int) -> str | None:
        shown = (self.store.get("gremio_codes", hero.id) or {}).get(kind, [])
        return shown[n - 1] if 1 <= n <= len(shown) else None

    def _class_label(self, data: dict[str, Any]) -> str:
        cid = data.get("class_id", "")
        group = self.content.classes.get(cid, {}).get("group", cid)
        return self.texts.t(f"class_group.{group}.name")

    def _place_label(self, x: int, y: int) -> str:
        return self.texts.t("gremio.place", name=self._zone_name(self._zone(x, y)), x=x, y=y)

    # ------------------------------------------------------------------ presence and works that take time (D-269, D-274)

    def _presence_window(self, account: str, data: dict[str, Any] | None, zones: set[tuple[int, int]], start: float,
                         now: float, cache: dict[str, dict[str, Any]]) -> float:
        """Seconds this member counted as present in `zones` between `start` and `now` (D-274.6), from its stored record.

        [ES]
        Qué hace: estima cuánto estuvo presente un miembro entre la última revisión y ahora: desde que llegó a la zona (registro
        "presence") hasta ahora si explora, recolecta, caza o duerme ahí, o hasta 15 min (presence.minutes) después de su último
        botón. Viajando no cuenta. Usa la ficha guardada (lo que pasó en ese tiempo), nunca el botón de ahora.
        La llama: _advance_work. Si cambia, afecta: cuánto avanzan la fundación y las obras.
        """
        if not data:
            return 0.0
        pos = (data.get("x"), data.get("y"))
        if pos not in zones:
            return 0.0
        key = f"{pos[0]}:{pos[1]}"
        record = cache.setdefault(key, self.store.get("presence", key) or {})
        since = (record.get("seen") or {}).get(account)
        since = start if since is None else max(start, float(since))
        kind = (data.get("activity") or {}).get("kind")
        if kind == "travel":
            return 0.0
        if kind in _busy_kinds():
            until = now
        else:
            until = min(now, float(data.get("seen_at", 0.0)) + self._seconds(self.content.balance["presence"]["minutes"]))
        return max(0.0, until - since)

    def _present_now(self, members: list[str], zones: set[tuple[int, int]], actor: Hero | None) -> list[str]:
        """Members present in `zones` right now (D-274.6): there, and a button in presence.minutes or busy there."""
        cutoff = self.clock.now() - self._seconds(self.content.balance["presence"]["minutes"])
        out = []
        for account in members:
            data = self._hero_data(account, actor)
            if not data or (data.get("x"), data.get("y")) not in zones:
                continue
            kind = (data.get("activity") or {}).get("kind")
            if kind == "travel":
                continue
            if kind in _busy_kinds() or float(data.get("seen_at", 0.0)) >= cutoff:
                out.append(account)
        return out

    def _online(self, data: dict[str, Any]) -> bool:
        """🟢 en línea: a button in the last presence.minutes, or busy (exploring, gathering, hunting, sleeping), anywhere."""
        if (data.get("activity") or {}).get("kind") in _busy_kinds():
            return True
        return float(data.get("seen_at", 0.0)) >= self.clock.now() - self._seconds(self.content.balance["presence"]["minutes"])

    @staticmethod
    def _work_rate_cap(work: dict[str, Any]) -> float:
        """How many members a work can use at once: need / its floor (the minimum time, D-269: 10 min)."""
        return float(work["need"]) / max(EPS, float(work.get("floor") or 1.0))

    def _advance_work(self, work: dict[str, Any], members: list[str], zones: set[tuple[int, int]], actor: Hero | None) -> int:
        """Add to a work what the members present since its last check did; return how many are present now.

        [ES]
        Qué hace: suma al avance de una obra (fundar o una mejora) los segundos de cada miembro presente desde la última
        revisión ("at"), con el tope del piso de tiempo (nunca más rápido que gremio.found_floor_minutes / works.floor_minutes),
        y la deja revisada ahora. Devuelve cuántos están presentes ahora (para el tiempo que falta).
        La llaman: _founding_settle y _works_settle_camp. Si cambia, afecta: la regla "tiempo = minutos × 2 ÷ presentes".
        """
        now = self.clock.now()
        start = float(work.get("at", now))
        if now > start:
            cache: dict[str, dict[str, Any]] = {}
            total = sum(self._presence_window(a, self.store.get("hero", a), zones, start, now, cache) for a in members)
            gained = min(total, self._work_rate_cap(work) * (now - start))
            work["done"] = min(float(work["need"]), float(work.get("done", 0.0)) + gained)
        work["at"] = now
        return len(self._present_now(members, zones, actor))

    def _work_left(self, work: dict[str, Any], present: int) -> float | None:
        """Seconds left at this many members present; None if nobody is there (paused)."""
        if present <= 0:
            return None
        return max(0.0, float(work["need"]) - float(work.get("done", 0.0))) / min(float(present), self._work_rate_cap(work))

    def _work_line(self, key: str, name: str, work: dict[str, Any], present: int) -> str:
        """"🏗️ <name> ▓▓░░ 40 % · 👥 2 presentes · faltan 36 min" (or paused)."""
        t = self.texts
        need = max(EPS, float(work["need"]))
        pct = min(100, int(100 * float(work.get("done", 0.0)) / need))
        left = self._work_left(work, present)
        rest = t.t("works.left", n=present, time=self._fmt_duration(left)) if left is not None else t.t("works.paused")
        return t.t(key, name=name, bar=self._bar(float(work.get("done", 0.0)), need, 8), pct=pct, rest=rest)

    def _works_index(self, key: str, kind: str, ref: str, eta: float | None) -> None:
        self.store.put("works_open", key, {"kind": kind, "ref": ref, "eta": eta})

    def _works_settle(self, hero: Hero) -> list[str]:
        """Advance the works this hero takes part in (its guild's founding, its camp's improvements); notices for the hero.

        [ES]
        Qué hace: revisa la fundación del gremio del héroe y las obras en curso de su campamento (perezoso, como los viajes):
        las avanza con los presentes y termina las que ya llegaron. Devuelve los avisos para quien juega.
        La llaman: act(), view() y text() (después de _settle). Si cambia, afecta: cuándo terminan la fundación y las obras.
        """
        lines: list[str] = []
        record = self._gremio_link(hero.id)
        if record and record.get("founding") and not record.get("camp"):
            lines += self._founding_settle(record, hero)
        if hero.camp and self.store.get("works_open", f"build:{hero.camp}"):
            lines += self._works_settle_camp(hero.camp, hero)
        return lines

    def _works_tick(self) -> None:
        """tick(): finish the works whose expected end has come, even if no member plays now (their notices are pushed)."""
        now = self.clock.now()
        for key, entry in list(self.store.items("works_open")):
            eta = entry.get("eta")
            if eta is None or eta > now:
                continue
            if entry.get("kind") == "found":
                record = self._gremio(entry.get("ref"))
                if record and record.get("founding") and not record.get("camp"):
                    self._founding_settle(record, None)
                else:
                    self.store.delete("works_open", key)
            else:
                self._works_settle_camp(entry.get("ref", ""), None)

    # ------------------------------------------------------------------ 👥 Jugadores at the bonfire (D-265, D-274)

    def _players_view(self, hero: Hero, notice: str | None = None) -> View:
        """👥 Jugadores: who played at the bonfire in the last minute, the "N/20" counter and a code per player (D-265).

        [ES]
        Qué hace: la pantalla 👥 Jugadores de la fogata (D-274.1: reemplaza a 🔬 Investigar en el menú del Claro). Lista a los que
        tocaron un botón en la fogata en el último minuto (presence.bonfire_seconds) con su clase, nivel y gremio, cada uno con su
        código (/j1, /j2…: su tarjeta), y el contador "👥 N/20 en la fogata" (N con la regla de 15 min de 📍 Zona, D-274.2; 20 es
        bonfire.cap: el reparto a otras hogueras llega con el 0.36). Botones: 🛡️ Gremio, 🔄 Actualizar y ↩️ Volver.
        La llaman: 👥 Jugadores del Claro, /jugadores y /players. Si cambia, afecta: tests/test_gremio_desde_el_inicio.py.
        """
        t = self.texts
        if (hero.x, hero.y) != (0, 0):
            return self._main_view(hero, notice=t.t("players.only_bonfire"))
        now = self.clock.now()
        window = self._seconds(float(self.content.balance["presence"].get("bonfire_seconds", 60)) / 60)
        present = self._zone_players(0, 0, exclude=hero.id)
        cap = int(self.content.balance.get("bonfire", {}).get("cap", 20))
        recent = [p for p in present if p["seen"] >= now - window][:cap]
        body = [t.t("players.intro"), "", t.t("players.count", n=len(present) + 1, cap=cap), ""]
        for n, row in enumerate(recent, 1):
            guild = self._guild_name_of(row["id"])
            body.append(t.t("players.line", n=n, name=row["name"], cls=row["cls"], level=row["level"],
                            guild=t.t("players.guild_tag", name=guild) if guild else ""))
        body.append(t.t("players.hint") if recent else t.t("players.none"))
        self._codes(hero, "players", [row["id"] for row in recent])
        actions = [Action(id="guild", label=t.t("gremio.button")), Action(id="players", label=t.t("players.refresh")),
                   Action(id="claro", label=t.t("menu.back"))]
        return View(kind="players", title=t.t("players.title"), body=body, actions=actions, notice=notice)

    def _player_code(self, hero: Hero, n: int) -> View:
        """/j2: the card of the 2nd player of the last 👥 Jugadores list."""
        account = self._code_target(hero, "players", n)
        if account is None:
            return self._players_view(hero, notice=self.texts.t("players.bad_code"))
        return self._player_card(hero, account)

    def _player_card(self, hero: Hero, account: str, notice: str | None = None) -> View:
        """A player's card: class, level, guild, when they last played; ✉️ invite to your guild or 🙋 ask to join theirs.

        [ES]
        Qué hace: la tarjeta de otro jugador desde 👥 Jugadores. Si eres líder u oficial de un gremio sin campamento con lugar y
        ese jugador no tiene gremio ni campamento, ✉️ Invitar a mi gremio; si él está en un gremio sin campamento con lugar y tú
        no tienes, 🙋 Pedir entrar. Solo información y esos dos pedidos (D-96: ver a otros nunca da ventaja).
        La llaman: /j1 y "pcard:<cuenta>". Si cambia, afecta: tests/test_gremio_desde_el_inicio.py.
        """
        t = self.texts
        data = self.store.get("hero", account)
        if not data:
            return self._players_view(hero, notice=t.t("players.gone"))
        other = Hero.from_dict(data)
        guild = self._guild_name_of(account, data)
        body = [t.t("players.card_name", name=self._banner(other) + self._emblem_name(other)),
                t.t("players.card_class", cls=self._class_label(data), level=other.level),
                t.t("players.card_guild", name=guild) if guild else t.t("players.card_no_guild"),
                t.t("players.card_seen", ago=self._ago(other.seen_at))]
        if (other.x, other.y) == (0, 0):
            body.append(t.t("players.card_here"))
        actions = []
        mine = self._my_gremio(hero)
        theirs = self._gremio_link(account)
        if (mine and account != hero.id and self._gremio_manager(mine, hero.id) and self._gremio_room(mine)
                and self._gremio_free(account, data) and account not in mine.get("invites", [])):
            actions.append(Action(id=f"ginvite:{account}", label=t.t("gremio.invite_button")))
        if (theirs and not theirs.get("camp") and account != hero.id and self._gremio_free(hero.id, hero)
                and self._gremio_room(theirs) and hero.id not in theirs.get("requests", [])):
            actions.append(Action(id=f"greq:{theirs['id']}", label=t.t("gremio.request_button", name=theirs["name"])))
        actions.append(Action(id="players", label=t.t("menu.back")))
        return View(kind="player_card", title=t.t("players.card_title"), body=body, actions=actions, notice=notice)

    # ------------------------------------------------------------------ the guild hub (D-269)

    def _gremio_action(self, hero: Hero, action_id: str) -> View:
        """Route the guild and bonfire buttons (GREMIO_ACTIONS). [ES] Qué hace: reparte los botones de esta sección. La llama: _idle_action."""
        arg = action_id.partition(":")[2]
        routes = {"players": lambda: self._players_view(hero), "gnew": lambda: self._gremio_new(hero),
                  "glist": lambda: self._gremio_list(hero), "greqs": lambda: self._gremio_requests_view(hero),
                  "gmsg": lambda: self._gremio_msg_ask(hero), "gfund": lambda: self._gremio_fund_view(hero),
                  "gmeet": lambda: self._gremio_meet_view(hero), "gmeetset": lambda: self._gremio_meet_set(hero),
                  "gfound": lambda: self._gremio_found_view(hero), "gfoundx": lambda: self._gremio_found_cancel(hero),
                  "gleave": lambda: self._gremio_leave(hero, confirmed=False)}
        if action_id in routes:
            return routes[action_id]()
        if action_id == "gleave!":
            return self._gremio_leave(hero, confirmed=True)
        prefixed = {"pcard": lambda: self._player_card(hero, arg), "gcard": lambda: self._gremio_card(hero, arg),
                    "greq": lambda: self._gremio_request(hero, arg), "ginvite": lambda: self._gremio_invite(hero, arg),
                    "gmem": lambda: self._gremio_member_view(hero, arg), "goff": lambda: self._gremio_officer(hero, arg),
                    "glead": lambda: self._gremio_lead(hero, arg, confirmed=False),
                    "glead!": lambda: self._gremio_lead(hero, arg, confirmed=True),
                    "gkick": lambda: self._gremio_kick(hero, arg, confirmed=False),
                    "gkick!": lambda: self._gremio_kick(hero, arg, confirmed=True)}
        head = action_id.partition(":")[0]
        if head in prefixed:
            return prefixed[head]()
        return self._gremio_view(hero)

    def _gremio_view(self, hero: Hero, notice: str | None = None) -> View:
        """🛡️ Gremio before a camp: members (where, doing what, online), founding, meeting point, fund and messages (D-269).

        [ES]
        Qué hace: el centro del gremio antes del campamento (hasta 8 botones, de 2 en 2: HUB_KINDS "gremio"). Arriba el nombre,
        el líder y "👥 N/5"; la fundación en curso con su barra; el 📍 punto de reunión; el 💰 fondo; cada miembro con su código
        (/m1), si está en línea (regla de 15 min), dónde está y qué hace; y los últimos 📢 mensajes. Botones: 📢 Mensaje,
        💰 Fondo, 📍 Reunión, 🏕️ Fundar (el líder), 🙋 Solicitudes (líder u oficial, si hay), 🚪 Salir y ↩️ Volver. Sin gremio,
        qué es y cómo se crea o se busca (_gremio_none_view); con el campamento ya fundado, la invitación (_gremio_invite_view).
        La llaman: 🛡️ Gremio (de 👥 Jugadores y de /gremio sin campamento: _guild_view) y casi todas las acciones del gremio.
        Si cambia, afecta: tests/test_gremio_desde_el_inicio.py y los recorridos de botones.
        """
        t = self.texts
        record = self._gremio_link(hero.id)
        if record and record.get("camp"):
            if hero.id in record.get("invited", []) and hero.camp is None:
                return self._gremio_invite_view(hero, record, notice)
            record = None
        if record is None or hero.id not in record.get("members", []):
            return self._gremio_none_view(hero, notice)
        leader = record["leader"]
        members = [leader] + [m for m in record["members"] if m != leader]
        body = [t.t("gremio.header", name=record["name"]),
                t.t("gremio.leader_line", leader=self._hero_name(leader) if leader != hero.id else hero.name,
                    n=len(members), cap=self._gremio_cap()), ""]
        founding = record.get("founding")
        if founding:
            zones = {(founding["x"], founding["y"])}
            present = len(self._present_now(record["members"], zones, hero))
            body.append(self._work_line("gremio.founding_line", self._place_label(founding["x"], founding["y"]), founding, present))
        meet = record.get("meet")
        body.append(t.t("gremio.meet_line", place=self._place_label(*meet)) if meet else t.t("gremio.meet_none"))
        body.append(t.t("gremio.fund_line", items=self._item_list(record["fund"])) if record.get("fund") else t.t("gremio.fund_empty"))
        body += ["", t.t("gremio.members_title")]
        for n, account in enumerate(members, 1):
            body.append(self._gremio_member_line(n, account, record, hero))
        self._codes(hero, "members", members)
        messages = record.get("messages") or []
        if messages:
            body += ["", t.t("gremio.messages_title")]
            body += [t.t("gremio.msg_line", name=m.get("by", "?"), text=m.get("text", "")) for m in messages]
        body += ["", t.t("gremio.codes_hint")]
        actions = [Action(id="gmsg", label=t.t("gremio.msg_button")), Action(id="gfund", label=t.t("gremio.fund_button")),
                   Action(id="gmeet", label=t.t("gremio.meet_button"))]
        if hero.id == leader or founding:
            actions.append(Action(id="gfound", label=t.t("gremio.found_button")))
        if self._gremio_manager(record, hero.id) and record.get("requests"):
            actions.append(Action(id="greqs", label=t.t("gremio.requests_button", n=len(record["requests"]))))
        actions.append(Action(id="gleave", label=t.t("gremio.leave_button")))
        actions.append(Action(id=self._gremio_back(hero), label=t.t("menu.back")))
        return View(kind="gremio", title=t.t("gremio.title"), body=body, actions=actions, notice=notice)

    def _gremio_back(self, hero: Hero) -> str:
        """↩️ Volver of the guild: 👥 Jugadores at the bonfire, else 📍 Zona."""
        return "players" if (hero.x, hero.y) == (0, 0) and not hero.activity else "home"

    def _gremio_member_line(self, n: int, account: str, record: dict[str, Any], hero: Hero) -> str:
        """"/m1 👑 Lyra (nv 3) · 🟢 en línea · Colinas (5, 2) · 🔎 explorando"."""
        t = self.texts
        data = self._hero_data(account, hero) or {}
        role = (t.t("gremio.role_leader") if account == record["leader"]
                else t.t("gremio.role_officer") if account in record.get("officers", []) else "")
        online = self._online(data)
        state = t.t("gremio.online") if online else t.t("gremio.offline", ago=self._ago(float(data.get("seen_at", 0.0))))
        kind = "combat" if self.store.get("combat", account) is not None else (data.get("activity") or {}).get("kind") or "idle"
        return t.t("gremio.member_line", code=f"/m{n}", role=role, name=data.get("name", "?"), level=data.get("level", 1),
                   state=state, where=self._place_label(data.get("x", 0), data.get("y", 0)),
                   activity=t.t(f"presence.activity.{kind}"))

    def _gremio_none_view(self, hero: Hero, notice: str | None = None) -> View:
        """No guild yet: what a guild is, its price and cap, and 🛡️ Crear gremio / 🔎 Buscar gremio."""
        t = self.texts
        cfg = self._gremio_cfg()
        body = [t.t("gremio.none_intro"), t.t("gremio.none_what"),
                t.t("gremio.none_cost", coins=self._money(int(cfg.get("found_coins", 20))), cap=self._gremio_cap()),
                t.t("gremio.none_found", n=int(cfg.get("found_min_members", 2)), minutes=int(cfg.get("found_minutes", 60)))]
        actions = [Action(id="gnew", label=t.t("gremio.new_button")), Action(id="glist", label=t.t("gremio.list_button")),
                   Action(id=self._gremio_back(hero), label=t.t("menu.back"))]
        return View(kind="gremio_none", title=t.t("gremio.title"), body=body, actions=actions, notice=notice)

    def _gremio_new(self, hero: Hero) -> View:
        """🛡️ Crear gremio: no guild and no camp, gremio.found_coins; then the next text is its name."""
        t = self.texts
        cost = int(self._gremio_cfg().get("found_coins", 20))
        if not self._gremio_free(hero.id, hero):
            return self._gremio_view(hero, notice=t.t("gremio.already"))
        if hero.gold < cost:
            return self._gremio_view(hero, notice=t.t("gremio.no_coins", coins=self._money(cost)))
        self.store.put("camp_naming", hero.id, {"mode": "gremio", "x": hero.x, "y": hero.y})
        return View(kind="name_gremio", title=t.t("gremio.title"), body=[t.t("gremio.ask_name")], expects_text=True,
                    actions=[Action(id="guild", label=t.t("gremio.cancel"))])

    def _gremio_text(self, hero: Hero, mode: str, text: str) -> View:
        """The free text of a guild prompt: its name ("gremio"), a 📢 message ("gmsg") or a search ("gsearch")."""
        if mode == "gmsg":
            return self._gremio_post(hero, text)
        if mode == "gsearch":
            return self._gremio_list(hero, query=text)
        return self._gremio_name(hero, text)

    def _gremio_name(self, hero: Hero, name: str) -> View:
        """The guild's name: like a camp name (it becomes the camp's), unique among guilds and camps; then it is created."""
        t = self.texts

        def again(key: str) -> View:
            return View(kind="name_gremio", title=t.t("gremio.title"), body=[t.t(key), t.t("gremio.ask_name")], expects_text=True,
                        actions=[Action(id="guild", label=t.t("gremio.cancel"))])

        if not GREMIO_NAME_RE.match(name):
            return again("gremio.bad_name")
        key = self._name_key(name)
        if self.store.get("guild_name", key) or self.store.get("camp_name", key):
            return again("gremio.name_taken")
        self.store.delete("camp_naming", hero.id)
        cost = int(self._gremio_cfg().get("found_coins", 20))
        if not self._gremio_free(hero.id, hero):
            return self._gremio_view(hero, notice=t.t("gremio.already"))
        if hero.gold < cost:
            return self._gremio_view(hero, notice=t.t("gremio.no_coins", coins=self._money(cost)))
        seq = self.store.get("meta", "gremio_seq") or {"n": 0}
        seq["n"] = int(seq.get("n", 0)) + 1
        self.store.put("meta", "gremio_seq", seq)
        gid = f"g{seq['n']}"
        hero.gold -= cost
        self.store.put("gremio", gid, {"id": gid, "name": name, "leader": hero.id, "officers": [], "members": [hero.id],
                                       "requests": [], "invites": [], "created": self.clock.now(), "messages": [], "fund": {},
                                       "gave": {}, "meet": None, "founding": None, "camp": None, "invited": []})
        self.store.put("gremio_of", hero.id, {"gremio": gid})
        self.store.put("guild_name", key, {"gremio": gid})
        self.store.put("camp_name", key, {"gremio": gid})        # the camp will take this name: reserved
        return self._gremio_view(hero, notice=t.t("gremio.created", name=name, coins=self._money(cost)))

    def _gremio_list(self, hero: Hero, query: str | None = None, notice: str | None = None) -> View:
        """🔎 Buscar gremio: the guilds without a camp, most members first, each with its code (/g1); any text searches."""
        t = self.texts
        rows = [g for _, g in self.store.items("gremio") if not g.get("closed") and not g.get("camp")]
        if query:
            rows = [g for g in rows if _plain(query) in _plain(g["name"])]
        rows.sort(key=lambda g: (-len(g.get("members", [])), g.get("created", 0)))
        shown = rows[:int(self._gremio_cfg().get("list_shown", 8))]
        body = [t.t("gremio.list_intro") if not query else t.t("gremio.list_query", query=query), ""]
        for n, g in enumerate(shown, 1):
            full = "" if self._gremio_room(g) else t.t("gremio.list_full")
            body.append(t.t("gremio.list_line", n=n, name=g["name"], count=len(g.get("members", [])), cap=self._gremio_cap(),
                            leader=self._hero_name(g["leader"]), full=full))
        if not shown:
            body.append(t.t("gremio.list_none"))
        body += ["", t.t("gremio.list_hint")]
        self._codes(hero, "guilds", [g["id"] for g in shown])
        self.store.put("camp_naming", hero.id, {"mode": "gsearch", "x": hero.x, "y": hero.y})
        return View(kind="gremio_list", title=t.t("gremio.list_title"), body=body, expects_text=True, notice=notice,
                    actions=[Action(id="guild", label=t.t("menu.back"))])

    def _guild_code(self, hero: Hero, n: int) -> View:
        """/g2: the card of the 2nd guild of the last 🔎 Buscar gremio list."""
        gid = self._code_target(hero, "guilds", n)
        if gid is None:
            return self._gremio_list(hero, notice=self.texts.t("gremio.bad_code"))
        return self._gremio_card(hero, gid)

    def _gremio_card(self, hero: Hero, gid: str, notice: str | None = None) -> View:
        """A guild's card: leader, members and room; 🙋 Pedir entrar if you can."""
        t = self.texts
        record = self._gremio(gid)
        if not record or record.get("closed"):
            return self._gremio_list(hero, notice=t.t("gremio.gone"))
        names = [f"{self._hero_name(m)}" for m in record.get("members", [])]
        body = [t.t("gremio.header", name=record["name"]),
                t.t("gremio.leader_line", leader=self._hero_name(record["leader"]), n=len(names), cap=self._gremio_cap()),
                t.t("gremio.card_members", names=", ".join(names))]
        if record.get("camp"):
            body.append(t.t("gremio.card_has_camp"))
        actions = []
        if (not record.get("camp") and self._gremio_free(hero.id, hero) and self._gremio_room(record)
                and hero.id not in record.get("requests", [])):
            actions.append(Action(id=f"greq:{gid}", label=t.t("gremio.request_button", name=record["name"])))
        elif hero.id in record.get("requests", []):
            body.append(t.t("gremio.request_waiting"))
        actions.append(Action(id="glist", label=t.t("menu.back")))
        return View(kind="gremio_card", title=t.t("gremio.title"), body=body, actions=actions, notice=notice)

    # ------------------------------------------------------------------ joining: requests and invitations (D-269.1, D-253)

    def _gremio_request(self, hero: Hero, gid: str) -> View:
        """🙋 Pedir entrar: the leader and the officers get the request with ✅ / ❌ (each in their language)."""
        t = self.texts
        record = self._gremio(gid)
        if not record or record.get("closed") or record.get("camp"):
            return self._gremio_list(hero, notice=t.t("gremio.gone"))
        if not self._gremio_free(hero.id, hero):
            return self._gremio_view(hero, notice=t.t("gremio.already"))
        if not self._gremio_room(record):
            return self._gremio_card(hero, gid, notice=t.t("gremio.full"))
        if hero.id not in record["requests"]:
            record["requests"].append(hero.id)
            self.store.put("gremio", gid, record)
            managers = [record["leader"]] + [o for o in record.get("officers", []) if o != record["leader"]]
            self._push_each(managers, lambda: View(
                kind="gremio_request", title=t.t("gremio.request_title"),
                body=[t.t("gremio.request_body", name=hero.name, cls=self._class_label({"class_id": hero.class_id}),
                          level=hero.level, guild=record["name"])],
                actions=[Action(id=f"gans:{gid}:{hero.id}:y", label=t.t("gremio.accept")),
                         Action(id=f"gans:{gid}:{hero.id}:n", label=t.t("gremio.refuse"))]))
        return self._gremio_card(hero, gid, notice=t.t("gremio.request_sent", name=record["name"]))

    def _gremio_requests_view(self, hero: Hero) -> View:
        """🙋 Solicitudes: the first pending request with ✅ / ❌ (leader or officer)."""
        t = self.texts
        record = self._my_gremio(hero)
        if not record or not self._gremio_manager(record, hero.id) or not record.get("requests"):
            return self._gremio_view(hero)
        account = record["requests"][0]
        data = self.store.get("hero", account) or {}
        body = [t.t("gremio.request_body", name=data.get("name", "?"), cls=self._class_label(data), level=data.get("level", 1),
                    guild=record["name"]), t.t("gremio.requests_count", n=len(record["requests"]))]
        actions = [Action(id=f"gans:{record['id']}:{account}:y", label=t.t("gremio.accept")),
                   Action(id=f"gans:{record['id']}:{account}:n", label=t.t("gremio.refuse")),
                   Action(id="guild", label=t.t("menu.back"))]
        return View(kind="gremio_requests", title=t.t("gremio.request_title"), body=body, actions=actions)

    def _gremio_join(self, record: dict[str, Any], account: str) -> None:
        """Put a player in a guild (record saved by the caller) and link it."""
        if account not in record["members"]:
            record["members"].append(account)
        self.store.put("gremio_of", account, {"gremio": record["id"]})

    def _gremio_answer_action(self, hero: Hero, action_id: str) -> View:
        """Route the answers that arrive as pushes: a request (gans:), an invitation (ginv:) and the camp's (gcamp:)."""
        if action_id.startswith("gans:"):
            return self._gremio_answer(hero, action_id)
        if action_id.startswith("ginv:"):
            return self._gremio_invite_answer(hero, action_id)
        return self._gremio_camp_answer(hero, action_id)

    def _gremio_answer(self, hero: Hero, action_id: str) -> View:
        """✅ / ❌ a request: the leader or an officer; the player must still be free and the guild must have room.

        [ES]
        Qué hace: responde una solicitud ("gans:<gremio>:<cuenta>:y|n"). Entra si el líder o un oficial acepta, el jugador
        sigue sin gremio ni campamento y hay lugar (5 antes del campamento). Al jugador le llega la respuesta en su idioma.
        La llama: act() (antes del combate, como "join:"). Si cambia, afecta: quién entra a cada gremio.
        """
        t = self.texts
        parts = action_id.split(":")
        if len(parts) < 4 or parts[-1] not in ("y", "n"):
            return self._main_view(hero)
        gid, account, choice = parts[1], ":".join(parts[2:-1]), parts[-1]
        record = self._gremio(gid)
        if (not record or record.get("closed") or record.get("camp") or not self._gremio_manager(record, hero.id)
                or account not in record.get("requests", [])):
            return self._main_view(hero, notice=t.t("gremio.already_answered"))
        record["requests"].remove(account)
        data = self.store.get("hero", account)
        accepted = choice == "y" and self._gremio_free(account, data) and self._gremio_room(record)
        if accepted:
            self._gremio_join(record, account)
        self.store.put("gremio", gid, record)
        result = "accepted" if accepted else "refused"
        self._push_each([account], lambda: View(kind="gremio_answer", title=t.t("gremio.title"),
                                                body=[t.t(f"gremio.join_{result}", name=record["name"])],
                                                actions=[Action(id="guild", label=t.t("gremio.button"))]))
        return self._gremio_view(hero, notice=t.t(f"gremio.you_{result}", name=(data or {}).get("name", "?")))

    def _gremio_invite(self, hero: Hero, account: str) -> View:
        """✉️ Invitar a mi gremio (from a player's card): the player gets ✅ / ❌."""
        t = self.texts
        record = self._my_gremio(hero)
        data = self.store.get("hero", account)
        if not record or not self._gremio_manager(record, hero.id):
            return self._players_view(hero, notice=t.t("gremio.only_managers"))
        if not self._gremio_room(record):
            return self._player_card(hero, account, notice=t.t("gremio.full"))
        if not self._gremio_free(account, data):
            return self._player_card(hero, account, notice=t.t("gremio.target_busy"))
        if account not in record["invites"]:
            record["invites"].append(account)
            self.store.put("gremio", record["id"], record)
            self._push_each([account], lambda: View(
                kind="gremio_invite", title=t.t("gremio.invite_title"),
                body=[t.t("gremio.invite_body", name=hero.name, guild=record["name"])],
                actions=[Action(id=f"ginv:{record['id']}:y", label=t.t("gremio.accept")),
                         Action(id=f"ginv:{record['id']}:n", label=t.t("gremio.refuse"))]))
        return self._player_card(hero, account, notice=t.t("gremio.invite_sent", name=(data or {}).get("name", "?")))

    def _gremio_invite_answer(self, hero: Hero, action_id: str) -> View:
        """✅ / ❌ an invitation: in if still free and there is room; the leader is told."""
        t = self.texts
        parts = action_id.split(":")
        if len(parts) != 3 or parts[2] not in ("y", "n"):
            return self._main_view(hero)
        record = self._gremio(parts[1])
        if not record or record.get("closed") or record.get("camp") or hero.id not in record.get("invites", []):
            return self._main_view(hero, notice=t.t("gremio.already_answered"))
        record["invites"].remove(hero.id)
        accepted = parts[2] == "y" and self._gremio_free(hero.id, hero) and self._gremio_room(record)
        if accepted:
            self._gremio_join(record, hero.id)
        self.store.put("gremio", record["id"], record)
        result = "accepted" if accepted else "refused"
        self._push_each([record["leader"]], lambda: View(kind="gremio_answer", title=t.t("gremio.title"),
                                                         body=[t.t(f"gremio.invite_{result}", name=hero.name)]))
        if accepted:
            return self._gremio_view(hero, notice=t.t("gremio.welcome", name=record["name"]))
        return self._main_view(hero, notice=t.t("gremio.invite_declined"))

    # ------------------------------------------------------------------ members: officers, leader, leaving

    def _member_code(self, hero: Hero, n: int) -> View:
        """/m2: the 2nd member of your guild (the order of the last 🛡️ Gremio screen)."""
        account = self._code_target(hero, "members", n)
        if account is None or not self._my_gremio(hero):
            return self._gremio_view(hero, notice=self.texts.t("gremio.bad_code"))
        return self._gremio_member_view(hero, account)

    def _gremio_member_view(self, hero: Hero, account: str, notice: str | None = None) -> View:
        """A member's card: where, doing what, online, what they gave; the leader can name officers, hand over or remove."""
        t = self.texts
        record = self._my_gremio(hero)
        if not record or account not in record["members"]:
            return self._gremio_view(hero)
        data = self._hero_data(account, hero) or {}
        gave = (record.get("gave") or {}).get(account) or {}
        body = [self._gremio_member_line(record["members"].index(account) + 1, account, record, hero),
                t.t("gremio.member_class", cls=self._class_label(data), level=data.get("level", 1)),
                t.t("gremio.member_gave", items=self._item_list(gave)) if gave else t.t("gremio.member_gave_none")]
        actions = []
        if hero.id == record["leader"] and account != hero.id:
            officer = account in record.get("officers", [])
            actions += [Action(id=f"goff:{account}", label=t.t("gremio.unofficer_button" if officer else "gremio.officer_button")),
                        Action(id=f"glead:{account}", label=t.t("gremio.lead_button")),
                        Action(id=f"gkick:{account}", label=t.t("gremio.kick_button"))]
        actions.append(Action(id="guild", label=t.t("menu.back")))
        return View(kind="gremio_member", title=t.t("gremio.title"), body=body, actions=actions, notice=notice)

    def _gremio_officer(self, hero: Hero, account: str) -> View:
        """⭐ Nombrar oficial / ✖️ Quitar oficial (the leader). Officers accept requests and invite (D-253)."""
        t = self.texts
        record = self._my_gremio(hero)
        if not record or hero.id != record["leader"] or account not in record["members"] or account == hero.id:
            return self._gremio_view(hero)
        officers = record.setdefault("officers", [])
        named = account not in officers
        if named:
            officers.append(account)
        else:
            officers.remove(account)
        self.store.put("gremio", record["id"], record)
        key = "officer_named" if named else "officer_removed"
        self._push_each([account], lambda: View(kind="gremio_news", title=t.t("gremio.title"),
                                                body=[t.t(f"gremio.{key}_push", guild=record["name"])]))
        return self._gremio_member_view(hero, account, notice=t.t(f"gremio.{key}", name=self._hero_name(account)))

    def _gremio_confirm(self, title_key: str, body: str, yes: str, no: str) -> View:
        t = self.texts
        return View(kind="gremio_confirm", title=t.t(title_key), body=[body],
                    actions=[Action(id=yes, label=t.t("gremio.confirm_yes")), Action(id=no, label=t.t("gremio.confirm_no"))])

    def _gremio_lead(self, hero: Hero, account: str, confirmed: bool) -> View:
        """👑 Ceder liderazgo (asks first): the old leader stays as an officer."""
        t = self.texts
        record = self._my_gremio(hero)
        if not record or hero.id != record["leader"] or account not in record["members"] or account == hero.id:
            return self._gremio_view(hero)
        name = self._hero_name(account)
        if not confirmed:
            return self._gremio_confirm("gremio.title", t.t("gremio.lead_ask", name=name), f"glead!:{account}", f"gmem:{account}")
        record["leader"] = account
        officers = [o for o in record.get("officers", []) if o != account]
        record["officers"] = officers + [hero.id]
        record["members"] = [account] + [m for m in record["members"] if m != account]
        self.store.put("gremio", record["id"], record)
        self._push_each([account], lambda: View(kind="gremio_news", title=t.t("gremio.title"),
                                                body=[t.t("gremio.lead_push", name=hero.name, guild=record["name"])]))
        return self._gremio_view(hero, notice=t.t("gremio.lead_done", name=name))

    def _gremio_leave_member(self, record: dict[str, Any], account: str) -> None:
        """Take a member out of a guild (record saved by the caller); what they gave stays in the fund (rule 3)."""
        record["members"] = [m for m in record["members"] if m != account]
        record["officers"] = [o for o in record.get("officers", []) if o != account]
        self.store.delete("gremio_of", account)

    def _gremio_kick(self, hero: Hero, account: str, confirmed: bool) -> View:
        """🚫 Sacar del gremio (the leader; asks first). What they gave stays in the fund."""
        t = self.texts
        record = self._my_gremio(hero)
        if not record or hero.id != record["leader"] or account not in record["members"] or account == hero.id:
            return self._gremio_view(hero)
        name = self._hero_name(account)
        if not confirmed:
            return self._gremio_confirm("gremio.title", t.t("gremio.kick_ask", name=name), f"gkick!:{account}", f"gmem:{account}")
        self._gremio_leave_member(record, account)
        self.store.put("gremio", record["id"], record)
        self._push_each([account], lambda: View(kind="gremio_news", title=t.t("gremio.title"),
                                                body=[t.t("gremio.kicked_push", guild=record["name"])]))
        return self._gremio_view(hero, notice=t.t("gremio.kicked", name=name))

    def _gremio_leave(self, hero: Hero, confirmed: bool) -> View:
        """🚪 Salir del gremio (asks first). A leader with members hands over first; the last one dissolves it.

        [ES]
        Qué hace: un miembro sale (lo que dio queda en el fondo, regla 3). El líder con otros miembros primero cede el liderazgo
        (👑, desde la tarjeta del miembro). Si el líder está solo, el gremio se disuelve: se corta la fundación en curso, el
        fondo entero vuelve a su mochila y su nombre queda libre. La llaman: 🚪 Salir y su confirmación ("gleave!").
        Si cambia, afecta: tests/test_gremio_desde_el_inicio.py.
        """
        t = self.texts
        record = self._my_gremio(hero)
        if not record:
            return self._gremio_view(hero)
        alone = record["members"] == [hero.id]
        if hero.id == record["leader"] and not alone:
            return self._gremio_view(hero, notice=t.t("gremio.leave_hand_over"))
        if not confirmed:
            return self._gremio_confirm("gremio.title", t.t("gremio.dissolve_ask" if alone else "gremio.leave_ask", name=record["name"]),
                                        "gleave!", "guild")
        if not alone:
            self._gremio_leave_member(record, hero.id)
            self.store.put("gremio", record["id"], record)
            self._push_each([record["leader"]], lambda: View(kind="gremio_news", title=t.t("gremio.title"),
                                                             body=[t.t("gremio.left_push", name=hero.name, guild=record["name"])]))
            return self._gremio_view(hero, notice=t.t("gremio.left", name=record["name"]))
        founding = record.get("founding")
        if founding:                                    # the founding stops: what the fund paid goes back to it first
            for item, n in (founding.get("paid") or {}).items():
                record["fund"][item] = record["fund"].get(item, 0) + n
            self.store.delete("works_open", f"found:{record['id']}")
        for item, n in record.get("fund", {}).items():  # rule 3: the last one takes the whole fund back (nothing is lost)
            hero.backpack[item] = hero.backpack.get(item, 0) + n
        given = dict(record.get("fund", {}))
        key = self._name_key(record["name"])
        for space in ("guild_name", "camp_name"):
            if (self.store.get(space, key) or {}).get("gremio") == record["id"] and "camp" not in (self.store.get(space, key) or {}):
                self.store.delete(space, key)
        record.update(closed=True, members=[], officers=[], requests=[], invites=[], founding=None, fund={})
        self.store.put("gremio", record["id"], record)
        self.store.delete("gremio_of", hero.id)
        lines = [t.t("gremio.dissolved", name=record["name"])]
        if given:
            lines.append(t.t("gremio.fund_back", items=self._item_list(given)))
        return self._gremio_none_view(hero, notice="\n".join(lines))

    # ------------------------------------------------------------------ 📢 messages, 💰 fund, 📍 meeting point (D-269.2)

    def _gremio_msg_ask(self, hero: Hero) -> View:
        """📢 Mensaje: the next text goes to every member."""
        t = self.texts
        if not self._my_gremio(hero):
            return self._gremio_view(hero)
        self.store.put("camp_naming", hero.id, {"mode": "gmsg", "x": hero.x, "y": hero.y})
        return View(kind="gremio_msg", title=t.t("gremio.title"),
                    body=[t.t("gremio.msg_ask", n=int(self._gremio_cfg().get("message_max_chars", 200)))], expects_text=True,
                    actions=[Action(id="guild", label=t.t("gremio.cancel"))])

    def _gremio_post(self, hero: Hero, text: str) -> View:
        """Send a 📢 message: cut to gremio.message_max_chars, kept with the last gremio.messages_kept, pushed to every member.

        [ES]
        Qué hace: manda el texto a cada miembro (_push_each: el título les llega en su idioma; el texto es del jugador) y lo
        guarda en la pantalla del gremio (los últimos 5). Lo que pasa del largo se corta con "…". La llama: _gremio_text.
        Si cambia, afecta: tests/test_gremio_desde_el_inicio.py.
        """
        t = self.texts
        record = self._my_gremio(hero)
        self.store.delete("camp_naming", hero.id)
        if not record:
            return self._gremio_view(hero)
        text = " ".join(text.split())
        if not text:
            return self._gremio_msg_ask(hero)
        cap = int(self._gremio_cfg().get("message_max_chars", 200))
        if len(text) > cap:
            text = text[:max(1, cap - 1)].rstrip() + "…"
        keep = max(1, int(self._gremio_cfg().get("messages_kept", 5)))
        messages = (record.get("messages") or []) + [{"by": hero.name, "id": hero.id, "text": text, "at": self.clock.now()}]
        record["messages"] = messages[-keep:]
        self.store.put("gremio", record["id"], record)
        self._push_each([m for m in record["members"] if m != hero.id], lambda: View(
            kind="gremio_message", title=t.t("gremio.msg_push_title", name=record["name"]),
            body=[t.t("gremio.msg_line", name=hero.name, text=text)], actions=[Action(id="guild", label=t.t("gremio.button"))]))
        return self._gremio_view(hero, notice=t.t("gremio.msg_sent"))

    def _gremio_fund_view(self, hero: Hero, notice: str | None = None) -> View:
        """💰 Fondo: totals, what founding asks, who gave what, and your backpack's materials with a code each (/f02).

        [ES]
        Qué hace: el fondo del gremio (D-269.2: "no tienen que llevarlo a ningún lugar"): cada miembro deposita desde donde esté
        escribiendo o tocando el código de un material (/f02, el mismo número de 📦 Recursos): pasa todo lo que lleva de eso.
        Muestra el total, lo que pide fundar (camps.found_cost) y quién dio qué. ↩️ Volver al gremio.
        La llaman: 💰 Fondo del gremio y _fund_code. Si cambia, afecta: tests/test_gremio_desde_el_inicio.py.
        """
        t = self.texts
        record = self._my_gremio(hero)
        if not record:
            return self._gremio_view(hero)
        fund = record.get("fund") or {}
        cost = self.content.balance["camps"]["found_cost"]
        ready = all(fund.get(i, 0) >= n for i, n in cost.items())
        body = [t.t("gremio.fund_intro"), "",
                t.t("gremio.fund_line", items=self._item_list(fund)) if fund else t.t("gremio.fund_empty"),
                ("✅ " if ready else "▫️ ") + t.t("gremio.fund_found", items=self._item_list(cost))]
        gave = record.get("gave") or {}
        if gave:
            body += ["", t.t("gremio.fund_gave_title")]
            body += [t.t("gremio.fund_gave_line", name=self._hero_name(acc) if acc != hero.id else hero.name,
                         items=self._item_list(items)) for acc, items in gave.items() if items]
        mine = self._fund_goods(hero)
        body += ["", t.t("gremio.fund_bag_title")]
        for item_id, n in mine:
            item = self.content.items[item_id]
            body.append(t.t("gremio.fund_bag_line", code=f"{int(item['code']):02d}", emoji=item["emoji"], item=t.t(item["name_key"]), n=n))
        if not mine:
            body.append(t.t("gremio.fund_bag_none"))
        return View(kind="gremio_fund", title=t.t("gremio.fund_title"), body=body, notice=notice,
                    actions=[Action(id="guild", label=t.t("menu.back"))])

    def _fund_goods(self, hero: Hero) -> list[tuple[str, int]]:
        """The materials of the backpack that the fund takes (with a code; never food: it is for the pantry), by code."""
        rows = [(i, n) for i, n in hero.backpack.items()
                if n > 0 and self.content.items.get(i, {}).get("kind") == "material" and self.content.items[i].get("code")
                and not self.content.items[i].get("food")]
        return sorted(rows, key=lambda kv: int(self.content.items[kv[0]]["code"]))

    def _fund_code(self, hero: Hero, code: int) -> View:
        """/f02: put every unit of that material you carry in the guild's fund, from wherever you are (not in a fight)."""
        t = self.texts
        if self.store.get("combat", hero.id) is not None:
            return self._main_view(hero)
        record = self._my_gremio(hero)
        if not record:
            return self._gremio_view(hero, notice=t.t("gremio.fund_no_guild"))
        item_id = next((i for i, _ in self._fund_goods(hero) if int(self.content.items[i]["code"]) == code), None)
        if item_id is None:
            return self._gremio_fund_view(hero, notice=t.t("gremio.fund_no_code", code=f"/f{code:02d}"))
        n = hero.backpack.pop(item_id)
        record["fund"][item_id] = record["fund"].get(item_id, 0) + n
        mine = record.setdefault("gave", {}).setdefault(hero.id, {})
        mine[item_id] = mine.get(item_id, 0) + n
        self.store.put("gremio", record["id"], record)
        return self._gremio_fund_view(hero, notice=t.t("gremio.fund_given", items=self._item_list({item_id: n})))

    def _gremio_meet_view(self, hero: Hero, notice: str | None = None) -> View:
        """📍 Reunión: the meeting point, how far it is, 📍 Marcar aquí (leader) and 🧭 Ir al punto (with 📒 Lugares' question)."""
        t = self.texts
        record = self._my_gremio(hero)
        if not record:
            return self._gremio_view(hero)
        meet = record.get("meet")
        body = [t.t("gremio.meet_intro")]
        actions = []
        if meet:
            x, y = meet
            body.append(t.t("gremio.meet_line", place=self._place_label(x, y)))
            if (x, y) != (hero.x, hero.y):
                body.append(t.t("gremio.meet_far", zones=abs(x - hero.x) + abs(y - hero.y),
                                time=self._fmt_duration(self._trip_seconds(hero, x, y))))
                actions.append(Action(id=f"goask:{x}:{y}", label=t.t("gremio.meet_go")))
            else:
                body.append(t.t("gremio.meet_here"))
        else:
            body.append(t.t("gremio.meet_none"))
        if hero.id == record["leader"]:
            actions.insert(0, Action(id="gmeetset", label=t.t("gremio.meet_set")))
        actions.append(Action(id="guild", label=t.t("menu.back")))
        return View(kind="gremio_meet", title=t.t("gremio.meet_title"), body=body, actions=actions, notice=notice)

    def _gremio_meet_set(self, hero: Hero) -> View:
        """📍 Marcar aquí (the leader): the meeting point is this zone; every member is told, with a 🧭 Ir button."""
        t = self.texts
        record = self._my_gremio(hero)
        if not record or hero.id != record["leader"]:
            return self._gremio_meet_view(hero)
        record["meet"], record["meet_by"] = [hero.x, hero.y], hero.name
        self.store.put("gremio", record["id"], record)
        x, y = hero.x, hero.y
        self._push_each([m for m in record["members"] if m != hero.id], lambda: View(
            kind="gremio_news", title=t.t("gremio.meet_title"),
            body=[t.t("gremio.meet_push", name=hero.name, place=self._place_label(x, y))],
            actions=[Action(id=f"goask:{x}:{y}", label=t.t("gremio.meet_go")), Action(id="guild", label=t.t("gremio.button"))]))
        return self._gremio_meet_view(hero, notice=t.t("gremio.meet_done", place=self._place_label(x, y)))

    def _gremio_site(self, hero: Hero) -> tuple[int, int, str] | None:
        """Where this hero's guild builds: (x, y, kind) with kind "camp" (founded, you are invited), "found" or "meet".

        [ES]
        Qué hace: el lugar de la construcción del gremio del héroe (pedido del dueño, 18-oct): el campamento ya fundado si te
        invitaron y no respondiste, la fundación en curso o, si no hay, el 📍 punto de reunión. None si no hay lugar definido.
        La llaman: _build_site_action (📍 Zona y el viaje), _gremio_places (📒 Lugares) y _gremio_goal (_can_goto).
        """
        record = self._gremio_link(hero.id)
        if not record:
            return None
        if record.get("camp"):
            if hero.id not in record.get("invited", []) or hero.camp is not None:
                return None
            camp = self.store.get("camp", record["camp"])
            return (camp["x"], camp["y"], "camp") if camp else None
        if hero.id not in record.get("members", []):
            return None
        founding = record.get("founding")
        if founding:
            return founding["x"], founding["y"], "found"
        meet = record.get("meet")
        return (meet[0], meet[1], "meet") if meet else None

    def _build_site_action(self, hero: Hero) -> Action | None:
        """🏗️ Moverte a la construcción: a wide button of 📍 Zona (and of the trip) while the guild has a place defined.

        [ES]
        Qué hace: el botón que pidió el dueño (18-oct: "cuando ya se define el lugar donde se va a empezar la construcción, le
        va a salir un botón de moverse"): lleva a 📒 Lugares → "¿Viajar?" ("goask:x:y") y el héroe va solo por el camino de
        verdad, sin diagonales (_path: primero este-oeste, después norte-sur), aunque nunca haya pisado esa zona. No sale si no
        hay lugar definido, si ya estás ahí o si el campamento ya está fundado y eres miembro. En el viaje no sale si ya vas
        hacia ese lugar. La llaman: _zone_view (layout [2, 2, 1, 1, 1] solo con este botón) y _activity_view (de viaje).
        Si cambia, afecta: tests/test_gremio_desde_el_inicio.py y tests/test_buttons.py (los layouts de 📍 Zona).
        """
        site = self._gremio_site(hero)
        if site is None or (site[0], site[1]) == (hero.x, hero.y):
            return None
        goal = (hero.activity or {}).get("goal")
        if goal and list(goal) == [site[0], site[1]]:
            return None
        return Action(id=f"goask:{site[0]}:{site[1]}", label=self.texts.t("gremio.site_button"))

    def _gremio_places(self, hero: Hero) -> list[tuple[int, int, str, str]]:
        """(x, y, icon, name) of the guild's places for 📒 Lugares: the 🏗️ construction (or the camp) or the 📍 meeting point."""
        t = self.texts
        record = self._gremio_link(hero.id)
        if not record:
            return []
        out = []
        site = self._gremio_site(hero)
        if site and site[2] == "found":
            out.append((site[0], site[1], "🏗️", t.t("gremio.found_place", name=record["name"])))
        elif site and site[2] == "camp":
            out.append((site[0], site[1], "🏕️", record["name"]))
        meet = record.get("meet") if not record.get("camp") else None
        if meet and not any((x, y) == tuple(meet) for x, y, _, _ in out):
            out.append((meet[0], meet[1], "📍", t.t("gremio.meet_place", name=self._zone_name(self._zone(*meet)))))
        return out

    def _gremio_goal(self, hero: Hero, gx: int, gy: int) -> bool:
        """True if (gx, gy) is one of the guild's places: a trip can go there even if never visited (_can_goto)."""
        return any((x, y) == (gx, gy) for x, y, _, _ in self._gremio_places(hero))

    # ------------------------------------------------------------------ founding the camp (D-269.3)

    def _founding_at(self, x: int, y: int) -> dict[str, Any] | None:
        """The guild founding a camp at (x, y) now, if any (from the "works_open" index)."""
        for key, entry in self.store.items("works_open"):
            if entry.get("kind") == "found":
                record = self._gremio(entry.get("ref"))
                founding = (record or {}).get("founding")
                if founding and (founding["x"], founding["y"]) == (x, y):
                    return record
        return None

    def _founding_near(self, x: int, y: int, gap: int) -> bool:
        """True if another guild is founding within `gap` zones of (x, y)."""
        for _, entry in self.store.items("works_open"):
            if entry.get("kind") == "found":
                founding = (self._gremio(entry.get("ref")) or {}).get("founding")
                if founding and max(abs(founding["x"] - x), abs(founding["y"] - y)) <= gap:
                    return True
        return False

    def _gremio_found_reqs(self, hero: Hero) -> list[tuple[str, bool]]:
        """The guild part of the founding requirements (D-269.3): lead a guild, 2 members here, the fund has the cost.

        [ES]
        Qué hace: las tres condiciones nuevas para fundar: ser líder de un gremio sin campamento, tener al menos
        gremio.found_min_members miembros del gremio presentes en la zona (contándote) y que el 💰 fondo tenga camps.found_cost.
        La llama: _camp_requirements (que suma las de siempre: Lejanía, explorada, vecinas conocidas, sin otro campamento cerca).
        Si cambia, afecta: quién puede fundar y el paso "found" del 🧭 camino guiado.
        """
        t = self.texts
        cfg = self._gremio_cfg()
        record = self._my_gremio(hero)
        leads = bool(record) and record["leader"] == hero.id
        need = int(cfg.get("found_min_members", 2))
        present = len(self._present_now(record["members"], {(hero.x, hero.y)}, hero)) if record else 0
        cost = self.content.balance["camps"]["found_cost"]
        fund = (record or {}).get("fund") or {}
        return [(t.t("camps.req_guild"), leads),
                (t.t("camps.req_members_here", n=present, need=need), leads and present >= need),
                (t.t("camps.req_fund", items=self._item_list(cost)), leads and all(fund.get(i, 0) >= n for i, n in cost.items()))]

    def _gremio_found_view(self, hero: Hero, notice: str | None = None) -> View:
        """🏕️ Fundar (from the guild): the founding in progress, or what founding here needs and 🏕️ Fundar aquí."""
        t = self.texts
        record = self._my_gremio(hero)
        if not record:
            return self._gremio_view(hero)
        founding = record.get("founding")
        actions = []
        if founding:
            zones = {(founding["x"], founding["y"])}
            present = len(self._present_now(record["members"], zones, hero))
            body = [t.t("gremio.found_progress_intro"),
                    self._work_line("gremio.founding_line", self._place_label(founding["x"], founding["y"]), founding, present),
                    t.t("gremio.found_rule", n=int(self._gremio_cfg().get("found_min_members", 2)),
                        minutes=int(self._gremio_cfg().get("found_minutes", 60)),
                        floor=int(self._gremio_cfg().get("found_floor_minutes", 10)))]
            if (founding["x"], founding["y"]) != (hero.x, hero.y):
                actions.append(Action(id=f"goask:{founding['x']}:{founding['y']}", label=t.t("gremio.site_button")))
            if hero.id == record["leader"]:
                actions.append(Action(id="gfoundx", label=t.t("gremio.found_cancel")))
        else:
            reqs = self._camp_requirements(hero)
            body = [t.t("gremio.found_intro", place=self._place_label(hero.x, hero.y)), ""]
            body += [("✅ " if ok else "▫️ ") + text for text, ok in reqs]
            body += ["", t.t("gremio.found_rule", n=int(self._gremio_cfg().get("found_min_members", 2)),
                             minutes=int(self._gremio_cfg().get("found_minutes", 60)),
                             floor=int(self._gremio_cfg().get("found_floor_minutes", 10)))]
            if hero.id == record["leader"] and all(ok for _, ok in reqs):
                actions.append(Action(id="found", label=t.t("gremio.found_here")))
        actions.append(Action(id="guild", label=t.t("menu.back")))
        return View(kind="gremio_found", title=t.t("gremio.found_title"), body=body, actions=actions, notice=notice)

    def _start_founding(self, hero: Hero) -> View:
        """🏕️ Fundar aquí: the leader, here, with the requirements met; the fund pays and the founding starts (a work).

        [ES]
        Qué hace: empieza la fundación donde está el líder (D-269.3: "donde el jefe decida"), si se cumple todo
        (_camp_requirements). El 💰 fondo paga camps.found_cost al empezar (si se cancela, vuelve al fondo). La fundación es una
        obra: necesita gremio.found_minutes × found_min_members minutos de miembros presentes (1 h con 2, 30 min con 4) y nunca
        tarda menos de found_floor_minutes. Se avisa a cada miembro (con 🧭 Ir). Reemplaza a fundar solo (D-252 ya no rige).
        La llaman: el botón "found" (🏕️ Campamento en una zona libre o 🏕️ Fundar del gremio). Si cambia, afecta:
        tests/test_camps.py (found_at) y tests/test_gremio_desde_el_inicio.py.
        """
        t = self.texts
        record = self._my_gremio(hero)
        if not record or record["leader"] != hero.id:
            return self._camp_here_view(hero, notice=t.t("camps.found_by_guild"))
        if record.get("founding"):
            return self._gremio_found_view(hero, notice=t.t("gremio.found_already"))
        if (hero.activity or {}).get("kind") == "travel":
            return self._main_view(hero, notice=t.t("activity.busy"))
        if not all(ok for _, ok in self._camp_requirements(hero)):
            return self._camp_here_view(hero, notice=t.t("camps.cannot"))
        cfg = self._gremio_cfg()
        cost = dict(self.content.balance["camps"]["found_cost"])
        for item, n in cost.items():
            record["fund"][item] -= n
            if record["fund"][item] <= 0:
                del record["fund"][item]
        now = self.clock.now()
        need = self._seconds(float(cfg.get("found_minutes", 60))) * int(cfg.get("found_min_members", 2))
        founding = {"x": hero.x, "y": hero.y, "need": need, "done": 0.0, "at": now, "started": now,
                    "floor": self._seconds(float(cfg.get("found_floor_minutes", 10))), "paid": cost}
        record["founding"] = founding
        self.store.put("gremio", record["id"], record)
        present = len(self._present_now(record["members"], {(hero.x, hero.y)}, hero))
        left = self._work_left(founding, present)
        self._works_index(f"found:{record['id']}", "found", record["id"], now + left if left is not None else None)
        x, y = hero.x, hero.y
        self._push_each([m for m in record["members"] if m != hero.id], lambda: View(
            kind="gremio_news", title=t.t("gremio.found_title"),
            body=[t.t("gremio.found_push", name=hero.name, place=self._place_label(x, y))],
            actions=[Action(id=f"goask:{x}:{y}", label=t.t("gremio.site_button")), Action(id="guild", label=t.t("gremio.button"))]))
        return self._camp_here_view(hero, notice=t.t("gremio.found_started", place=self._place_label(x, y),
                                                     time=self._fmt_duration(left) if left is not None else "—"))

    def _gremio_found_cancel(self, hero: Hero) -> View:
        """❌ Cancelar fundación (the leader): what the fund paid goes back to it."""
        t = self.texts
        record = self._my_gremio(hero)
        if not record or hero.id != record["leader"] or not record.get("founding"):
            return self._gremio_found_view(hero) if record else self._gremio_view(hero)
        for item, n in (record["founding"].get("paid") or {}).items():
            record["fund"][item] = record["fund"].get(item, 0) + n
        record["founding"] = None
        self.store.put("gremio", record["id"], record)
        self.store.delete("works_open", f"found:{record['id']}")
        self._push_each([m for m in record["members"] if m != hero.id], lambda: View(
            kind="gremio_news", title=t.t("gremio.found_title"), body=[t.t("gremio.found_cancel_push", name=hero.name)]))
        return self._gremio_found_view(hero, notice=t.t("gremio.found_cancelled"))

    def _founding_settle(self, record: dict[str, Any], actor: Hero | None) -> list[str]:
        """Advance a guild's founding with the members present; create the camp when it is done."""
        founding = record["founding"]
        present = self._advance_work(founding, record["members"], {(founding["x"], founding["y"])}, actor)
        if float(founding["done"]) >= float(founding["need"]) - EPS:
            return self._finish_founding(record, actor)
        self.store.put("gremio", record["id"], record)
        left = self._work_left(founding, present)
        self._works_index(f"found:{record['id']}", "found", record["id"], self.clock.now() + left if left is not None else None)
        return []

    def _founding_failed(self, record: dict[str, Any], actor: Hero | None, key: str) -> list[str]:
        """The founding cannot end (another camp took the place meanwhile): the fund gets back what it paid; all are told."""
        t = self.texts
        for item, n in (record["founding"].get("paid") or {}).items():
            record["fund"][item] = record["fund"].get(item, 0) + n
        record["founding"] = None
        self.store.put("gremio", record["id"], record)
        self.store.delete("works_open", f"found:{record['id']}")
        others = [m for m in record["members"] if actor is None or m != actor.id]
        self._push_each(others, lambda: View(kind="gremio_news", title=t.t("gremio.found_title"), body=[t.t(key)]))
        return [t.t(key)] if actor is not None and actor.id in record["members"] else []

    def _finish_founding(self, record: dict[str, Any], actor: Hero | None) -> list[str]:
        """The founding ended: create the camp (the guild's name, the leader founds), link the guild, invite the others.

        [ES]
        Qué hace: al terminar la fundación crea el campamento con el nombre del gremio y el líder como fundador (_create_camp:
        territorio, oleadas, 🧭 camino y 📔 diario del líder); crea el gremio del campamento (registro D-97 "guild", nivel 1, con
        "gremio" = id) y su cupo pasa a ser el del campamento (guild.levels: 5 al nivel 1); lo que sobró del fondo va a las obras
        del campamento ("upgrades"."fund"); a cada otro miembro le llega la invitación (✅ / ❌, "gcamp:"). Si mientras tanto otro
        campamento tomó el lugar (o el líder ya no puede), la fundación se corta y el fondo recupera lo pagado.
        La llama: _founding_settle. Si cambia, afecta: tests/test_gremio_desde_el_inicio.py y tests/test_camps.py (found_at).
        """
        t = self.texts
        founding = record["founding"]
        x, y = founding["x"], founding["y"]
        key = f"{x}:{y}"
        gap = int(self.content.balance["camps"]["min_distance"])
        near = any(self.store.get("camp", f"{x + dx}:{y + dy}") for dx in range(-gap, gap + 1) for dy in range(-gap, gap + 1))
        leader_id = record["leader"]
        leader = actor if actor is not None and actor.id == leader_id else self._load(leader_id)
        if near or self._territory(x, y) or leader is None or leader.camp is not None:
            return self._founding_failed(record, actor, "gremio.found_failed")
        gid = record["id"]
        if leader is actor:
            lines = self._create_camp(leader, x, y, record["name"], gid)
        else:
            with self._speaking(leader_id):
                lines = self._create_camp(leader, x, y, record["name"], gid)
            self._save(leader)
            self._push(leader_id, View(kind="gremio_founded", title=lines[0] if lines else "", body=lines[1:]))
            lines = []
        now = self.clock.now()
        self.store.put("guild", key, {"name": record["name"], "camp": key, "founder_id": leader_id, "level": 1,
                                      "progress": {k: 0 for k in guild_rules.COUNTERS}, "created": now, "gremio": gid})
        self.store.put("guild_name", self._name_key(record["name"]), {"camp": key, "gremio": gid})
        leftover = record.get("fund") or {}
        if leftover:
            upgrades = self._upgrades(key)
            for item, n in leftover.items():
                upgrades["fund"][item] = upgrades["fund"].get(item, 0) + n
            self.store.put("upgrades", key, upgrades)
        others = [m for m in record["members"] if m != leader_id]
        record.update(camp=key, founding=None, fund={}, invited=others, founded_at=now)
        self.store.put("gremio", gid, record)
        self.store.delete("works_open", f"found:{gid}")
        self.store.delete("gremio_of", leader_id)
        leader_name, name = leader.name, record["name"]
        self._push_each(others, lambda: View(
            kind="gremio_camp_invite", title=t.t("gremio.camp_invite_title"),
            body=[t.t("gremio.camp_invite", leader=leader_name, name=name, place=self._place_label(x, y))],
            actions=[Action(id=f"gcamp:{gid}:y", label=t.t("gremio.camp_yes")),
                     Action(id=f"gcamp:{gid}:n", label=t.t("gremio.camp_no"))]))
        if leftover and lines:
            lines.append(t.t("gremio.fund_to_works", items=self._item_list(leftover)))
        if actor is not None and actor.id in others:
            lines.append(t.t("gremio.camp_invite", leader=leader_name, name=name, place=self._place_label(x, y)))
        return lines

    def _gremio_invite_view(self, hero: Hero, record: dict[str, Any], notice: str | None = None) -> View:
        """The guild founded its camp and you have not answered: ✅ Entrar al campamento / ❌ No, and 🏗️ go there."""
        t = self.texts
        camp = self.store.get("camp", record["camp"]) or {}
        x, y = camp.get("x", 0), camp.get("y", 0)
        body = [t.t("gremio.camp_invite", leader=camp.get("founder", "?"), name=record["name"], place=self._place_label(x, y))]
        actions = [Action(id=f"gcamp:{record['id']}:y", label=t.t("gremio.camp_yes")),
                   Action(id=f"gcamp:{record['id']}:n", label=t.t("gremio.camp_no")),
                   Action(id=self._gremio_back(hero), label=t.t("menu.back"))]
        return View(kind="gremio_camp_invite", title=t.t("gremio.camp_invite_title"), body=body, actions=actions, notice=notice)

    def _gremio_camp_answer(self, hero: Hero, action_id: str) -> View:
        """✅ / ❌ the camp's invitation after founding (the join flow of D-84 in reverse: the camp asks, the member decides).

        [ES]
        Qué hace: el miembro decide si entra al campamento que fundó su gremio ("gcamp:<gremio>:y|n"). Si entra y hay lugar
        (_members_cap: el cupo del gremio del campamento), queda como miembro (Hero.camp); si no, sale del gremio y queda libre.
        Al fundador le llega la respuesta, como en _answer_join. La llama: act() (antes del combate).
        Si cambia, afecta: tests/test_gremio_desde_el_inicio.py.
        """
        t = self.texts
        parts = action_id.split(":")
        if len(parts) != 3 or parts[2] not in ("y", "n"):
            return self._main_view(hero)
        record = self._gremio(parts[1])
        if not record or not record.get("camp") or hero.id not in record.get("invited", []):
            return self._main_view(hero, notice=t.t("gremio.already_answered"))
        record["invited"].remove(hero.id)
        self.store.delete("gremio_of", hero.id)
        key = record["camp"]
        camp = self.store.get("camp", key)
        joined = (parts[2] == "y" and camp is not None and hero.camp is None
                  and len(camp["members"]) < self._members_cap(camp))
        if joined:
            camp["members"].append(hero.id)
            self.store.put("camp", key, camp)
            hero.camp = key
        else:
            record["members"] = [m for m in record["members"] if m != hero.id]
        self.store.put("gremio", record["id"], record)
        result = "joined" if joined else ("full" if parts[2] == "y" else "declined")
        if camp:
            self._push_each([camp["founder_id"]], lambda: View(kind="camp_answer", title=t.t("camps.title"),
                                                               body=[t.t(f"gremio.camp_{result}_push", name=hero.name, camp=camp["name"])]))
        return self._main_view(hero, notice=t.t(f"gremio.camp_{result}", camp=(camp or {}).get("name", record["name"])))

    # ------------------------------------------------------------------ camp works that take time (D-269.4, D-274.4)

    def _work_seconds(self, udef: dict[str, Any]) -> float:
        """Member-seconds an improvement needs once its materials are complete: minutes_per_level × level × members_ref."""
        cfg = self.content.balance.get("works", {})
        return self._seconds(float(cfg.get("minutes_per_level", 0))) * int(udef.get("level", 1)) * int(cfg.get("members_ref", 2))

    def _start_work(self, key: str, camp: dict[str, Any], uid: str, hero: Hero) -> bool:
        """Turn a complete improvement into a work in progress; False if it builds at once (works.minutes_per_level 0)."""
        need = self._work_seconds(self._upgrade_catalog().get(uid, {}))
        if need <= 0:
            return False
        record = self._upgrades(key)
        now = self.clock.now()
        record["building"][uid] = {"need": need, "done": 0.0, "at": now, "started": now, "by": hero.name,
                                   "floor": self._seconds(float(self.content.balance.get("works", {}).get("floor_minutes", 10)))}
        self.store.put("upgrades", key, record)
        return True

    def _camp_zones(self, camp: dict[str, Any]) -> set[tuple[int, int]]:
        return {(int(zx), int(zy)) for zx, zy in camp.get("zones", [[camp["x"], camp["y"]]])}

    def _works_settle_camp(self, key: str, actor: Hero | None) -> list[str]:
        """Advance every work in progress of a camp with the members present in its territory; build what is done.

        [ES]
        Qué hace: cada obra en curso ("upgrades"."building") avanza con los miembros presentes en cualquier zona del territorio
        del campamento (D-274.4); la que termina queda construida para siempre ("built") y se avisa a los miembros. Varias obras
        en curso avanzan a la vez, cada una con los mismos presentes. Actualiza el índice "works_open" (cuándo podría terminar
        la próxima). La llaman: _works_settle (botones de un miembro) y _works_tick. Si cambia, afecta: cuándo se terminan las
        mejoras (tests/test_gremio_desde_el_inicio.py).
        """
        t = self.texts
        camp = self.store.get("camp", key)
        record = self.store.get("upgrades", key) or {}
        building = record.get("building") or {}
        if not camp or not building:
            self.store.delete("works_open", f"build:{key}")
            return []
        zones = self._camp_zones(camp)
        done, etas = [], []
        for uid, work in list(building.items()):
            present = self._advance_work(work, camp["members"], zones, actor)
            if float(work["done"]) >= float(work["need"]) - EPS:
                record.setdefault("built", {})[uid] = self.clock.now()
                del building[uid]
                done.append(uid)
            else:
                left = self._work_left(work, present)
                if left is not None:
                    etas.append(self.clock.now() + left)
        record["building"] = building
        self.store.put("upgrades", key, record)
        if building:
            self._works_index(f"build:{key}", "build", key, min(etas) if etas else None)
        else:
            self.store.delete("works_open", f"build:{key}")
        lines = []
        for uid in done:
            others = [m for m in camp["members"] if actor is None or m != actor.id]
            self._push_each(others, lambda uid=uid: View(kind="camp_news", title=t.t("upgrades.built_push_title"),
                                                         body=[t.t("works.done_push", name=self._upgrade_name(uid), camp=camp["name"])]))
            if actor is not None and actor.id in camp["members"]:
                lines.append(t.t("works.done", name=self._upgrade_name(uid)))
        return lines

    def _works_refresh(self, key: str, camp: dict[str, Any], actor: Hero | None) -> None:
        """Recompute when a camp's next work could end (after one starts) without advancing anything new."""
        self._works_settle_camp(key, actor)

    def _building_lines(self, key: str, camp: dict[str, Any], hero: Hero) -> list[str]:
        """🏗️ Obras en curso of 🔨 Mejoras: one bar per work, with the members present in the territory and the time left."""
        t = self.texts
        building = (self.store.get("upgrades", key) or {}).get("building") or {}
        if not building:
            return []
        present = len(self._present_now(camp["members"], self._camp_zones(camp), hero))
        lines = ["", t.t("works.title")]
        lines += [self._work_line("works.line", self._upgrade_name(uid), work, present) for uid, work in building.items()]
        lines.append(t.t("works.rule", minutes=int(self.content.balance.get("works", {}).get("minutes_per_level", 60)),
                         floor=int(self.content.balance.get("works", {}).get("floor_minutes", 10))))
        return lines

    def _take_from_fund(self, record: dict[str, Any], need: dict[str, int], progress: dict[str, int]) -> dict[str, int]:
        """What the camp's fund (what the guild's fund left at founding) gives a work first; it only gives what the work lacks."""
        fund = record.get("fund") or {}
        given: dict[str, int] = {}
        for item, n in need.items():
            give = min(n - int(progress.get(item, 0)), int(fund.get(item, 0)))
            if give <= 0:
                continue
            fund[item] -= give
            if fund[item] <= 0:
                del fund[item]
            progress[item] = int(progress.get(item, 0)) + give
            given[item] = give
        record["fund"] = fund
        return given
