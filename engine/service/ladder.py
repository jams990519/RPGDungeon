"""The settlement ladder, first playable slice (D-253, D-122; how it was applied: D-327): one cap per stage, the members who
stop playing free their place, and the castle's 40 active members; since 0.53 (D-329), the castle's growing waves.

One number says how many members fit in each stage of a camp (balance.yaml camps.members_by_stage): the guild's level no
longer adds room (the double cap of D-84 and D-97 ends). A camp from before 0.51 never gets less room than it had: the first
time the engine sees it, it keeps its old cap as a floor (camp["cap_floor"]). 🛖 Cabañas and 🛏️ Literas still add on top.
A camp member who does not play for ladder.idle_release_days (30) frees the place: warned at ladder.idle_warn_days (25),
released at least idle_release_days - idle_warn_days after the warning; never the founder. The hero keeps everything and can
ask to join again; what the member gave stays in the camp. It runs from tick(), every ladder.idle_scan_minutes, and counts
from max(Hero.seen_at, the first time the scan saw that member in that camp): nobody is released for days before the patch.
The step to the castle asks ladder.castle_active (40) members who played in the last ladder.active_days (7).
Since 0.53 (D-122, D-329) it also asks the growing waves: while the camp is on the step to the castle, its normal raids
(raids.per_week) become a series of ladder.castle_waves.count waves, each growth stronger than a normal one; the series passes
at pass_wins wins and is lost once that can no longer happen, and then starts again after retry_days.

[ES]
Para qué sirve: la 1.ª parte jugable de la escalera del asentamiento (D-253, confirmada el 17-oct-2026; D-122): (1) un solo
    cupo por etapa (D-253.1, Forma A): campamento 10, aldea 15, pueblo 25, ciudad 40 y castillo 50 (la "Casa" de 5 es el gremio
    antes del campamento, gremio.members_before_camp); (2) quien deja de jugar libera su lugar a los 30 días (D-253.3), con
    aviso a los 25; (3) el castillo pide 40 activos de la semana (D-253.2); (4) desde la 0.53 (D-122, confirmada; cómo se aplicó:
    D-329, provisional), el castillo pide también las 🌊 oleadas crecientes: mientras el campamento está en el nivel anterior al
    castillo, sus oleadas normales (3 por semana) son una serie de 5, cada una más fuerte; se aprueba ganando 3 y, con 3
    perdidas, vuelve a empezar a los 3 días. Los 🤝 asistentes (D-289, D-304) son los oficiales
    de D-253.4: aceptan solicitudes desde la 0.39 (gremio.py _camp_manager); aquí no hay nada nuevo de eso. Cómo se aplicó
    lo eligió Claude: D-327 (provisional). Es parte de GameService (una "mezcla", como MapScrollMixin), en su propio archivo
    para no agrandar game.py.
Documento de diseño: diseno/09-construccion/escalera-del-asentamiento.md §0.4 (cómo quedó) y §2, §4 y §7;
    diseno/08-social/gremios-y-social.md §0
Módulo: capa de servicios (M9 Frontera y Fundación: el cupo y el castillo; M15 Social: quién está en el gremio)
Depende de: content/balance.yaml (camps.members_by_stage, camps.members_base, camps.members_per_level, camps.stages,
    guild.levels → capacity (solo para el piso de los campamentos de antes), el bloque ladder (con castle_waves desde la 0.53),
    raids.trial.to_level y raids.per_week), content/locales/es_escalera.yaml y en_escalera.yaml (textos), engine.social.guilds
    (capacity), engine.world.raids (wave_mult, series_outcome) y las ayudas de GameService (_camp_stage_id, _day_seconds,
    _seconds, _hero_name, _camp_managers, _tell_waiting_room, _push_each, _camp_effect, _fmt_duration)
Lo usan: engine/service/game.py (GameService hereda de esta clase): _members_cap y _members_cap_at (_base_cap_at), tick()
    (_cap_floor_sweep y _idle_tick), _create_camp ("cap_floor": 0 en los campamentos nuevos), _castle_needs
    (_castle_active_row), _lvlup_view ("lvlup.gives" con _members_cap_at), _level_up ("lvlup.done"), _lvlall_view y
    _faq_values (_ladder_faq_values); engine/service/gremio.py: _camp_members_view (_idle_line) y _camp_member_line
    (_idle_warned_mark). Desde la 0.53 (D-329): game.py _open_raid (_castle_wave_mark), _raid_notice (_castle_wave_notice_line),
    _defend (_castle_wave_fight_line), _resolve_raid (_castle_wave_done), _raid_lines (_castle_wave_open_line), _lvlup_rows
    (_castle_waves_row), _lvlup_view (_castle_waves_how) y _lvlup_all_view (_castle_waves_all)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño (todo dentro del registro "camp", clave "x:y"):
    "cap_floor": el cupo que el campamento tenía antes de la 0.51 (la cuenta de antes: members_base + members_per_level por
        nivel, o el del gremio si era mayor; sin las 🛖 Cabañas ni los 🛏️ muebles, que se suman aparte). Se escribe una sola vez
        (_cap_floor_sweep, en el primer tick después de arrancar); los campamentos nuevos nacen con 0. Sin el campo, el piso es
        la cuenta de antes en vivo (así ningún campamento pierde lugar ni un segundo).
    "idle_watch" {cuenta: hora}: cuándo el barrido vio por primera vez a ese miembro en este campamento (el piso de "jugó por
        última vez": nadie cuenta días de antes del parche ni de antes de entrar).
    "idle_warned" {cuenta: hora}: a quién se avisó "en 5 días liberas tu lugar" y cuándo; si juega después, se borra.
    "meta"/"idle": {"next"}: cuándo vuelve a mirar el barrido (cada ladder.idle_scan_minutes).
    "castle_waves" (0.53, D-329) {"won", "lost", "passed", "retry_at", "tries", "passed_at"}: la serie de 🌊 oleadas crecientes
        del paso a castillo: ganadas y perdidas de la serie en curso, si ya la aprobó (para siempre, como "trial_won"), desde
        cuándo puede empezar la siguiente después de perder una y cuántas series empezaron. Se escribe al cerrar cada oleada
        de la serie. La oleada abierta lleva "wave" (su número) y "wave_mult" (su fuerza) en camp["raid"].
Reglas que nunca se rompen:
    1. Nadie pierde lugar por la escalera (D-64): el cupo de un campamento nunca baja de su "cap_floor"; si el cupo es menor que
       los miembros, nadie sale por eso.
    2. Solo sale quien no juega (D-253.3): nunca el fundador, nunca sin el aviso de antes, nunca contando días de antes del
       parche. Su héroe, su mochila, su equipo, sus oficios y su progreso quedan; lo que dio a las obras y al fondo queda en el
       campamento; puede volver a pedir entrar.
    3. Cuando alguien sale, quien espera lugar en el gremio entra solo (D-323: _tell_waiting_room).
    4. Ningún texto visible se escribe aquí: todo sale de content/locales (es_escalera.yaml y en_escalera.yaml), y todo aviso a
       otro jugador se arma con _push_each (le llega en su idioma, D-250).
    5. Las oleadas crecientes solo traban el paso a castillo (D-64): un castillo que ya existe nunca las recibe ni pierde nada;
       perder la serie no quita niveles, zonas, miembros ni nada personal (cada oleada perdida cuesta lo de una oleada normal
       perdida, D-99 y D-115), y aprobarla queda para siempre.
Si cambias esto, revisa:
    - Números: balance.yaml camps.members_by_stage (cupo por etapa), ladder (idle_warn_days, idle_release_days,
      idle_scan_minutes, castle_active, active_days, castle_waves) y raids.trial.min_wins (los 10 vencedores distintos de la
      Noche de prueba); raids.per_week marca el ritmo de las oleadas crecientes; el registro de balance
      (diseno/03-personaje/balance.md)
    - Quién entra: _members_cap lo leen _ask_join, _answer_join, _camp_room (y con él _tell_waiting_room), las invitaciones
      (_camp_invite_send, _camp_invite_answer, _gremio_camp_answer) y las pantallas de 🛡️ Gremio y 🏕️ Campamento
    - Mapa de impacto: diseno/01-plataforma/mapa-de-impacto.md (M9, M15 y la cascada C-35, que desde la 0.53 cubre también
      las oleadas crecientes)
    - Pruebas: tests/test_escalera_cupo_oficiales.py, tests/test_oleadas_crecientes_castillo.py; tests/test_espera_entra_sola.py,
      tests/test_espera_del_gremio.py, tests/test_camps.py, tests/test_guilds.py, tests/test_ayudantes.py, tests/test_siguiente_nivel.py y tests/test_raids.py
"""

from __future__ import annotations

from typing import Any

from engine.hero import Hero
from engine.messaging import Action, View
from engine.social import guilds as guild_rules
from engine.world import raids as raid_rules

EPS = 1e-6


class LadderMixin:
    """The settlement ladder's first slice (D-253, D-327). Mixed into GameService; uses its helpers (see the [ES] header).

    [ES]
    Qué es: el cupo por etapa, quien deja de jugar, los activos del castillo y (0.53) sus oleadas crecientes.
    Quién la usa: GameService (hereda de esta clase) y GremioMixin (la línea 💤 de 👥 Miembros).
    Si cambia, afecta: quién entra y quién sigue en cada campamento, y cuándo se llega a castillo.
    """

    def _ladder_cfg(self) -> dict[str, Any]:
        return self.content.balance.get("ladder", {}) or {}

    # ------------------------------------------------------------------ 👥 one cap per stage (D-253.1)

    def _legacy_cap(self, camp: dict[str, Any], level: int | None = None) -> int:
        """The cap of before 0.51: members_base + members_per_level per level, or the guild's capacity if bigger (D-84, D-97).

        [ES] Qué hace: la cuenta de antes, sin las 🛖 Cabañas ni los 🛏️ muebles. Sirve para el piso de los campamentos de antes
        (cap_floor) y para una etapa que no está en camps.members_by_stage. La llaman: _cap_floor, _base_cap_at y
        _cap_floor_sweep. Si cambia, afecta: el piso de los campamentos de antes de la 0.51."""
        cfg = self.content.balance["camps"]
        level = int(camp.get("level", 1)) if level is None else int(level)
        base = int(cfg.get("members_base", 2)) + (level - 1) * int(cfg.get("members_per_level", 2))
        guild = self.store.get("guild", f"{camp['x']}:{camp['y']}")
        if guild:
            base = max(base, guild_rules.capacity(self.content.balance["guild"]["levels"], guild["level"]))
        return base

    def _stage_cap_at(self, level: int) -> int | None:
        """camps.members_by_stage of the stage of that level (campamento 10 … castillo 50), or None if the stage has none."""
        table = self.content.balance["camps"].get("members_by_stage") or {}
        value = table.get(self._camp_stage_id(int(level)))
        return int(value) if value is not None else None

    def _cap_floor(self, camp: dict[str, Any]) -> int:
        """The room a camp had before 0.51 (camp["cap_floor"]); without the field yet, the old count, live (D-64)."""
        if "cap_floor" in camp:
            return int(camp.get("cap_floor") or 0)
        return self._legacy_cap(camp)

    def _base_cap_at(self, camp: dict[str, Any], level: int) -> int:
        """The cap of the camp's stage at `level`, never under its floor; without 🛖 Cabañas and 🛏️ furniture (D-327).

        [ES] Qué hace: el cupo de la etapa (camps.members_by_stage) o, si la etapa no está en la tabla, la cuenta de antes; y
        nunca menos que el piso del campamento (cap_floor). Las 🛖 Cabañas y los 🛏️ muebles los suma _members_cap encima.
        La llaman: game.py _members_cap y _members_cap_at. Si cambia, afecta: quién entra a cada campamento."""
        stage = self._stage_cap_at(level)
        cap = stage if stage is not None else self._legacy_cap(camp, level)
        return max(cap, self._cap_floor(camp))

    def _cap_floor_sweep(self) -> None:
        """Once per process: every camp without "cap_floor" keeps its cap of before 0.51 as its floor (D-64, D-327).

        [ES] Qué hace: la primera vez que corre tick() después de arrancar, a cada campamento que todavía no tiene "cap_floor" le
        guarda la cuenta de antes (_legacy_cap): desde ahí el nivel del gremio ya no suma lugares, pero nadie tiene menos de lo
        que tenía. Los campamentos nuevos nacen con 0 (_create_camp). La llama: game.py tick(), antes de _waiting_sweep (así
        los que esperaban entran con el cupo nuevo). Si cambia, afecta: el piso de los campamentos de antes."""
        if getattr(self, "_cap_floors_set", False):
            return
        self._cap_floors_set = True
        for key, camp in list(self.store.items("camp")):
            if "cap_floor" not in camp:
                camp["cap_floor"] = self._legacy_cap(camp)
                self.store.put("camp", key, camp)

    # ------------------------------------------------------------------ 💤 who stops playing frees the place (D-253.3)

    def _idle_days(self) -> tuple[float, float]:
        """(warn, release) in days: ladder.idle_warn_days (25) and ladder.idle_release_days (30); release 0 turns it off."""
        cfg = self._ladder_cfg()
        release = float(cfg.get("idle_release_days", 0) or 0)
        warn = min(release, float(cfg.get("idle_warn_days", release) or release))
        return warn, release

    def _idle_tick(self) -> None:
        """tick(): every ladder.idle_scan_minutes, warn at 25 days without playing and free the place at 30 (D-253.3).

        [ES] Qué hace: como la cosecha (_harvest_tick), guarda en "meta"/"idle" cuándo vuelve a mirar y recorre los campamentos
        (_idle_camp). Sin ladder.idle_release_days (o en 0), no hace nada. La llama: game.py tick(). Si cambia, afecta: quién
        sale de cada campamento (tests/test_escalera_cupo_oficiales.py)."""
        _, release = self._idle_days()
        if release <= 0:
            return
        now = self.clock.now()
        meta = self.store.get("meta", "idle") or {}
        if float(meta.get("next", 0.0)) > now:
            return
        self.store.put("meta", "idle", {"next": now + self._seconds(float(self._ladder_cfg().get("idle_scan_minutes", 60)))})
        for key, camp in list(self.store.items("camp")):
            self._idle_camp(key, camp, now)

    def _idle_camp(self, key: str, camp: dict[str, Any], now: float) -> None:
        """One camp: note new members, forget the ones who played, warn at 25 days, release at 30 (never the founder).

        [ES] Qué hace: "jugó por última vez" = lo más nuevo entre Hero.seen_at (tocó un botón o escribió un comando: lo marca
        _mark_seen) y la primera vez que el barrido lo vio en este campamento ("idle_watch"). A los idle_warn_days le llega el
        aviso ("idle_warned"); si juega, se borra y la cuenta vuelve a empezar. A los idle_release_days, y con al menos
        (idle_release_days − idle_warn_days) desde el aviso, sale (_idle_release). El fundador nunca. La llama: _idle_tick.
        Si cambia, afecta: tests/test_escalera_cupo_oficiales.py."""
        warn_days, release_days = self._idle_days()
        day = self._day_seconds()
        warn_after, release_after = warn_days * day, release_days * day
        gap = release_after - warn_after
        members = list(camp.get("members") or [])
        founder = camp.get("founder_id")
        watch = dict(camp.get("idle_watch") or {})
        warned = dict(camp.get("idle_warned") or {})
        changed = False
        for book in (watch, warned):                    # who left (or is the founder) is not watched
            for account in [a for a in book if a not in members or a == founder]:
                book.pop(account)
                changed = True
        to_warn: list[tuple[str, int]] = []
        to_release: list[str] = []
        for account in members:
            if account == founder:
                continue
            if account not in watch:                    # first seen here: the count starts now, never before the patch
                watch[account] = now
                changed = True
                continue
            data = self.store.get("hero", account)
            if data is None:
                continue
            last = max(float(data.get("seen_at", 0.0) or 0.0), float(watch[account]))
            if account in warned and last > float(warned[account]):
                warned.pop(account)                     # played after the warning: the count starts again
                changed = True
            idle = now - last
            if account in warned:
                if idle >= release_after - EPS and now - float(warned[account]) >= gap - EPS:
                    to_release.append(account)
            elif idle >= warn_after - EPS:
                warned[account] = now
                changed = True
                left = max(release_after - idle, gap)
                to_warn.append((account, max(1, round(left / day))))
        for account in to_release:
            self._idle_release(key, camp, account)
            warned.pop(account, None)
            watch.pop(account, None)
        if changed or to_release:
            camp["idle_watch"] = watch
            camp["idle_warned"] = warned
            self.store.put("camp", key, camp)
        self._idle_notices(key, camp, to_warn, to_release, release_days)

    def _idle_release(self, key: str, camp: dict[str, Any], account: str) -> None:
        """Take a member who did not play out of the camp and its guild, like 🚪 Salir (the caller saves the camp).

        [ES] Qué hace: lo mismo que _leave_camp: sale de "members" y de los 🤝 asistentes, y su héroe queda sin campamento (con
        su mochila, su equipo, sus oficios y su progreso). Lo que dio queda en el campamento ("gave" no se toca). La llama:
        _idle_camp. Si cambia, afecta: qué le queda a quien sale."""
        camp["members"] = [m for m in camp.get("members") or [] if m != account]
        camp["helpers"] = [h for h in camp.get("helpers") or [] if h != account]     # D-289: a helper who leaves stops being one
        data = self.store.get("hero", account)
        if data is not None and data.get("camp") == key:
            data["camp"] = None
            self.store.put("hero", account, data)

    def _idle_notices(self, key: str, camp: dict[str, Any], to_warn: list[tuple[str, int]], to_release: list[str],
                      release_days: float) -> None:
        """The 💤 warning to each one, the release notice to each one and to the founder and the helpers; then who waits gets in."""
        t = self.texts
        name = camp["name"]
        days = int(round(release_days))
        for account, left in to_warn:
            self._push_each([account], lambda left=left: View(
                kind="gremio_news", title=t.t("ladder.warn_title"),
                body=[t.t("ladder.warn_push", camp=name, days=days, left=left)],
                actions=[Action(id="guild", label=t.t("gremio.button"))]))
        if not to_release:
            return
        self._push_each(to_release, lambda: View(kind="gremio_news", title=t.t("ladder.released_title"),
                                                 body=[t.t("ladder.released_push", camp=name, days=days)]))
        names = ", ".join(self._hero_name(a) for a in to_release)
        self._push_each(self._camp_managers(camp), lambda: View(
            kind="gremio_news", title=t.t("ladder.released_title"),
            body=[t.t("ladder.released_managers", names=names, camp=name, days=days)]))
        self._tell_waiting_room(key)                    # D-323: a place opened for who waits in the guild

    def _idle_line(self) -> str:
        """👥 Miembros: "💤 Quien no juega 30 días libera su lugar…" (empty when the rule is off)."""
        warn, release = self._idle_days()
        if release <= 0:
            return ""
        return self.texts.t("ladder.idle_line", days=int(round(release)), left=int(round(release - warn)))

    def _idle_warned_mark(self, camp: dict[str, Any], account: str) -> str:
        """"💤 " before a member who was warned and has not played since (the founder and the helpers see who is leaving)."""
        return self.texts.t("ladder.idle_mark") if account in (camp.get("idle_warned") or {}) else ""

    # ------------------------------------------------------------------ 🏰 the castle's active members (D-253.2, D-122)

    def _active_days(self) -> float:
        return float(self._ladder_cfg().get("active_days", 7) or 7)

    def _castle_active_need(self) -> int:
        return int(self._ladder_cfg().get("castle_active", 0) or 0)

    def _week_active(self, camp: dict[str, Any], actor: Hero | None = None) -> int:
        """Members of the camp who played (Hero.seen_at) in the last ladder.active_days (7): the castle's "activos"."""
        since = self.clock.now() - self._active_days() * self._day_seconds()
        count = 0
        for account in camp.get("members") or []:
            if actor is not None and account == actor.id:
                seen = actor.seen_at                    # fresher than the stored copy
            else:
                seen = float((self.store.get("hero", account) or {}).get("seen_at", 0.0) or 0.0)
            count += seen >= since
        return count

    def _castle_active_row(self, camp: dict[str, Any], actor: Hero | None = None) -> tuple[str, bool] | None:
        """⏫ Siguiente nivel's castle row: "👥 Activos esta semana: N de 40" (None when ladder.castle_active is 0).

        [ES] Qué hace: la línea del paso a castillo de D-253.2 ("40 activos con cupo de 50"): cuántos miembros jugaron en los
        últimos ladder.active_days de los ladder.castle_active que pide. La llama: game.py _castle_needs. Si cambia, afecta:
        quién llega a castillo (tests/test_escalera_cupo_oficiales.py, tests/test_siguiente_nivel.py)."""
        need = self._castle_active_need()
        if need <= 0:
            return None
        n = self._week_active(camp, actor)
        return self.texts.t("ladder.castle_active", n=n, need=need, days=int(round(self._active_days()))), n >= need

    # ------------------------------------------------------------------ 🌊 the castle's growing waves (D-122, D-329)

    def _waves_numbers(self) -> tuple[int, int, float, float]:
        """(count, pass_wins, growth, retry_days) of ladder.castle_waves; count 0 (or no block) turns the rule off.

        [ES] Qué hace: lee los números de las 🌊 oleadas crecientes (5 oleadas, se aprueba con 3, +20 % por oleada, 3 días de
        espera tras perder la serie). pass_wins nunca pasa de count ni baja de 1. La llaman: las funciones de esta sección.
        Si cambia, afecta: qué pide el paso a castillo (tests/test_oleadas_crecientes_castillo.py)."""
        cfg = self._ladder_cfg().get("castle_waves") or {}
        count = max(0, int(cfg.get("count", 0) or 0))
        need = min(count, max(1, int(cfg.get("pass_wins", count // 2 + 1) or 1))) if count else 0
        return count, need, max(0.0, float(cfg.get("growth", 0) or 0)), max(0.0, float(cfg.get("retry_days", 0) or 0))

    def _waves_step(self, camp: dict[str, Any]) -> bool:
        """True if the rule is on and the camp is one level under the castle (raids.trial.to_level - 1, the 8 → 9 step)."""
        if not self._waves_numbers()[0]:
            return False
        return int(camp.get("level", 1)) + 1 == int(self.content.balance["raids"]["trial"]["to_level"])

    @staticmethod
    def _waves_record(camp: dict[str, Any]) -> dict[str, Any]:
        """A copy of camp["castle_waves"] with "won" and "lost" always there (0 before the first wave of a series)."""
        record = dict(camp.get("castle_waves") or {})
        record["won"], record["lost"] = int(record.get("won", 0) or 0), int(record.get("lost", 0) or 0)
        return record

    def _waves_wait(self, camp: dict[str, Any]) -> float:
        """Seconds until a new series can start after a lost one (0 when it can)."""
        return max(0.0, float((camp.get("castle_waves") or {}).get("retry_at", 0.0) or 0.0) - self.clock.now())

    def _castle_wave_next(self, camp: dict[str, Any]) -> int | None:
        """The number (1..count) the camp's next raid takes in the castle's series, or None (off the step, passed, waiting).

        [ES] Qué hace: dice si la próxima oleada del campamento es una oleada creciente y cuál: solo en el nivel anterior al
        castillo, si la serie no está aprobada y no está esperando después de perder una. La llaman: _castle_wave_mark y
        las pruebas. Si cambia, afecta: qué oleadas cuentan para el castillo."""
        if not self._waves_step(camp) or (camp.get("castle_waves") or {}).get("passed") or self._waves_wait(camp) > 0:
            return None
        record = self._waves_record(camp)
        return record["won"] + record["lost"] + 1

    def _castle_wave_mark(self, camp: dict[str, Any], raid: dict[str, Any]) -> None:
        """game.py _open_raid: a weekly raid on the step to the castle becomes the next growing wave (its number and strength).

        [ES] Qué hace: si toca, le pone a la oleada que llega su número en la serie ("wave") y su fuerza ("wave_mult",
        raids.py wave_mult: 1 + 0,2 × número). Nada más se guarda hasta que la oleada se cierra. La llama: game.py _open_raid
        (solo la oleada semanal: la 🌙 Noche de prueba nunca es una oleada creciente). Si cambia, afecta: qué tan fuerte
        llega cada oleada del nivel 8."""
        n = self._castle_wave_next(camp)
        if n is None:
            return
        raid["wave"] = n
        raid["wave_mult"] = raid_rules.wave_mult(n, self._waves_numbers()[2])

    @staticmethod
    def _wave_pct(raid: dict[str, Any]) -> int:
        """How much stronger than a normal raid this growing wave is, in % (wave_mult 1.4 → 40)."""
        return int(round((float(raid.get("wave_mult", 1.0)) - 1) * 100))

    def _castle_wave_notice_line(self, raid: dict[str, Any]) -> str | None:
        """The arrival notice's line: "🌊 Oleada creciente 2 de 5: un 40 % más fuerte… hay que ganar 3 de 5" (None if normal)."""
        if not raid.get("wave"):
            return None
        count, need, _, _ = self._waves_numbers()
        return self.texts.t("ladder.waves_arrive", n=raid["wave"], count=count, pct=self._wave_pct(raid), need=need)

    def _castle_wave_fight_line(self, raid: dict[str, Any]) -> str | None:
        """The defender's line when the fight starts: "🌊 Oleada creciente 2 de 5: +40 % de vida y de ataque" (None if normal)."""
        if not raid.get("wave"):
            return None
        return self.texts.t("ladder.waves_fight", n=raid["wave"], count=self._waves_numbers()[0], pct=self._wave_pct(raid))

    def _castle_wave_open_line(self, raid: dict[str, Any]) -> list[str]:
        """The camp screen's extra line while a growing wave is on: "🌊 Oleada creciente 2 de 5 (+40 %)" (empty if normal)."""
        if not raid.get("wave"):
            return []
        return [self.texts.t("ladder.waves_open_line", n=raid["wave"], count=self._waves_numbers()[0], pct=self._wave_pct(raid))]

    def _castle_wave_done(self, camp: dict[str, Any], raid: dict[str, Any], won: bool) -> list[tuple[str, dict[str, Any]]]:
        """game.py _resolve_raid: count a closed growing wave; the series passes, fails (wait retry_days) or goes on.

        [ES] Qué hace: suma la oleada creciente que se cerró a la serie del campamento ("castle_waves": ganadas o perdidas).
        Con pass_wins ganadas la serie queda aprobada para siempre ("passed"); cuando ya no se puede llegar (con 5 oleadas, a
        las 3 perdidas: "si pierde más de las que gana, no aprueba", D-122) se pierde: la cuenta vuelve a 0 y la serie
        siguiente empieza con la primera oleada después de retry_days ("retry_at"). Devuelve las líneas (clave, valores) del
        parte que _resolve_raid les manda a todos los miembros con _push_each, cada uno en su idioma (D-250). El llamador
        guarda el campamento. La llama: game.py _resolve_raid (solo la oleada semanal con "wave"). Si cambia, afecta: cuándo
        se aprueba el castillo (tests/test_oleadas_crecientes_castillo.py)."""
        if not raid.get("wave") or not self._waves_step(camp) or (camp.get("castle_waves") or {}).get("passed"):
            return []
        count, need, _, retry_days = self._waves_numbers()
        record = self._waves_record(camp)
        if record["won"] + record["lost"] == 0:
            record["tries"] = int(record.get("tries", 0) or 0) + 1
        record["won" if won else "lost"] += 1
        values = {"camp": camp["name"], "n": raid["wave"], "won": record["won"], "lost": record["lost"], "count": count,
                  "need": need}
        outcome = raid_rules.series_outcome(record["won"], record["lost"], count, need)
        if outcome == "passed":
            record.update(passed=True, passed_at=self.clock.now())
            record.pop("retry_at", None)
            line = ("ladder.waves_passed", values)
        elif outcome == "failed":
            record["retry_at"] = float(raid["until"]) + self._seconds(retry_days * 24 * 60)
            record["won"] = record["lost"] = 0
            line = ("ladder.waves_failed", {**values, "retry_in": record["retry_at"] - self.clock.now()})
        else:
            line = ("ladder.waves_progress", {**values, "left": count - record["won"] - record["lost"]})
        camp["castle_waves"] = record
        return [line]

    def _castle_waves_row(self, camp: dict[str, Any]) -> tuple[str, bool] | None:
        """⏫ Siguiente nivel's castle row: "🌊 Oleadas crecientes: 2 ganadas, 1 perdida de 5 (…)" (None off the 8 → 9 step).

        [ES] Qué hace: la línea de las oleadas crecientes en la lista del paso a castillo (D-313: dice exactamente qué falta):
        antes de la primera ("ganar 3 de 5, empiezan con la próxima oleada"), en curso ("2 ganadas, 1 perdida de 5: hace falta
        ganar 3; quedan 2"), esperando después de perder la serie ("vuelven a empezar en …") o ✅ superadas. La llama:
        game.py _lvlup_rows (tipo "waves"). Si cambia, afecta: tests/test_oleadas_crecientes_castillo.py."""
        if not self._waves_step(camp):
            return None
        t = self.texts
        count, need, growth, _ = self._waves_numbers()
        record = self._waves_record(camp)
        won, lost = record["won"], record["lost"]
        if record.get("passed"):
            return t.t("ladder.waves_row_done", won=won, lost=lost, count=count), True
        wait = self._waves_wait(camp)
        if wait > 0:
            return t.t("ladder.waves_row_wait", time=self._fmt_duration(wait), need=need, count=count), False
        if won + lost == 0:
            return t.t("ladder.waves_row_new", need=need, count=count, pct=int(round(growth * 100))), False
        return t.t("ladder.waves_row", won=won, lost=lost, count=count, need=need, left=count - won - lost), False

    def _castle_waves_how(self) -> str:
        """⏫ Siguiente nivel, while the waves are missing: how they come, how much they grow and what losing the series costs."""
        count, need, growth, retry = self._waves_numbers()
        return self.texts.t("ladder.waves_how", per_week=int(self.content.balance["raids"]["per_week"]),
                            pct=int(round(growth * 100)), count=count,
                            top=int(round((raid_rules.wave_mult(count, growth) - 1) * 100)),
                            lose=count - need + 1, days=int(round(retry)))

    def _castle_waves_all(self) -> str:
        """📜 Qué pide cada nivel: " y superar las 🌊 5 oleadas crecientes (ganar 3)" for the castle line ("" when off)."""
        count, need, _, _ = self._waves_numbers()
        return self.texts.t("ladder.waves_all", count=count, need=need) if count else ""

    # ------------------------------------------------------------------ ❓ Dudas

    def _ladder_faq_values(self) -> dict[str, Any]:
        """{members_stages}, {idle_days}, {idle_left}, {castle_active}, {active_days} and {trial_winners} for ❓ Dudas; since
        0.53 (D-329) also {castle_waves}, {castle_waves_pass}, {castle_waves_pct} and {castle_waves_retry} (the growing waves)."""
        table = self.content.balance["camps"].get("members_by_stage") or {}
        stages = [s["id"] for s in self.content.balance["camps"]["stages"]]
        warn, release = self._idle_days()
        trial = self.content.balance["raids"]["trial"]
        count, need, growth, retry = self._waves_numbers()
        return {"members_stages": " · ".join(str(table[s]) for s in stages if s in table),
                "idle_days": int(round(release)), "idle_left": int(round(release - warn)),
                "castle_active": self._castle_active_need(), "active_days": int(round(self._active_days())),
                "trial_winners": int(trial.get("min_wins", 2)),
                "castle_waves": count, "castle_waves_pass": need, "castle_waves_pct": int(round(growth * 100)),
                "castle_waves_retry": int(round(retry))}
