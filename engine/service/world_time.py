"""Time zones and the world clock on screen (D-124 and D-126, confirmed; D-239.9, confirmed; how: D-334, provisional; 0.58).

Two things the owner asked for, in their simple layer (D-44):
- 🕐 Zona horaria (⚙️ Opciones, /hora): each player picks the zone in which clock times are shown (one-tap presets for the
  Americas, Spain and the US east coast, 🌐 UTC, and ➖ 1 h / ➕ 1 h for any whole hour from UTC−12 to UTC+14). It is saved
  in the "prefs" space next to the language and only changes what is shown: every rule keeps one clock for everyone.
  _clock() writes a clock time ("14:32", "23/10 14:32" when it is not today, "14:32 UTC" for whoever never chose).
- The world clock: ☀️ day, 🌇 evening and 🌙 night, the same for everyone (engine/world/world_clock.py). 📍 Zona says the
  band and when the next one comes; 🧭 Explorar says which of the zone's resources come out more now; a gathering round
  and the finds of exploring weigh their resources by the band (_band_weights); the Braseros' night (raids.night.source
  "world") is the world's 🌙 night.

[ES]
Para qué sirve: lo que se ve del reloj. (1) D-124 (confirmada): cada jugador elige su zona horaria para ver las horas
    (⚙️ Opciones → 🕐 Zona horaria, /hora); los horarios de combate y de eventos siguen siendo los mismos para todos. (2) D-126
    y D-239.9 (confirmadas): día, tarde y noche en el mundo, un día del mundo de 4 días reales, y cada franja da recursos un
    poco distintos. Cómo se aplicó lo eligió Claude: D-334 (provisional). Es parte de GameService (una "mezcla", como
    LadderMixin), en su propio archivo para no agrandar game.py.
Documento de diseño: diseno/02-mundo/mundo-vivo-y-viaje.md §2 (el reloj del mundo y las zonas horarias)
Módulo: capa de servicios (M1 Núcleo: el reloj y las zonas horarias; M8 Mundo: día, tarde y noche; M14: qué se recolecta)
Depende de: engine/core/timezones.py (las cuentas de las zonas y la zona de quien se atiende), engine/world/world_clock.py (la
    franja y los pesos), content/balance.yaml (time_zones, world_clock), content/locales/es_dia_y_hora.yaml y
    en_dia_y_hora.yaml (textos tz.*, world_clock.*, options.tz_line, raids.night_line) y las ayudas de GameService
    (_fmt_duration, _known_resources, _item_label, _options_view, store "prefs")
Lo usan: engine/service/game.py (GameService hereda de esta clase): _zone_view (la línea del reloj del mundo), _explore_menu
    (la línea de lo que sale más), _gather_step y _explore_step (_band_weights), _is_night (los 🔥 Braseros), _options_view
    (la línea y el botón 🕐), act() ("tz", "tz:…"), _faq_values (_world_time_faq_values) y las horas con _clock: el 📜 Tablón,
    el lote, el viaje, la oleada y la 🗼 Torre de vigía, ⏫ Siguiente nivel; engine/service/story.py (el 📔 Diario con
    _local_date, el 📜 Tablón y los encargos del campamento con _clock) y engine/service/market.py (cuándo vence una orden)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: el campo "tz" del espacio "prefs" del almacén (clave la cuenta, que es también la clave del héroe;
    junto al idioma "lang"): el id de la zona elegida (un preset de time_zones.presets o una hora fija "utc-5"). Sin él, la
    zona por defecto (time_zones.default: UTC, la que el juego ya usaba).
Reglas que nunca se rompen:
    1. La zona horaria solo cambia lo que se ve: ninguna regla la lee (D-124). Las duraciones ("en 40 min") no cambian.
    2. La franja del mundo es la misma para todos en el mismo instante (no depende de la zona de nadie).
    3. Una franja cambia la mezcla de una vuelta, nunca cuántas unidades da, y ningún recurso desaparece (world_clock.py).
    4. Ningún texto visible se escribe aquí: todo sale de content/locales (es y en, D-250).
Si cambias esto, revisa:
    - Datos y números: content/balance.yaml time_zones y world_clock (y raids.night); el registro de balance
      (diseno/03-personaje/balance.md §7, 0.58)
    - Lo que muestra horas: las llamadas a _clock en engine/service/game.py, story.py y market.py
    - Mapa de impacto: diseno/01-plataforma/mapa-de-impacto.md (M1, M8, C-19 y §4.3)
    - Pruebas: tests/test_zona_horaria_y_dia.py; tests/test_options.py, tests/test_guias.py y tests/test_fogata_ordenada.py
      (⚙️ Opciones tiene 6 botones); tests/test_raids.py (la noche de los Braseros); tests/test_siguiente_nivel.py (la hora de una obra)
"""

from __future__ import annotations

import math
from typing import Any

from engine.core import timezones as tz_rules
from engine.hero import Hero
from engine.messaging import Action, View
from engine.world import world_clock as wc_rules

# Button ids of 🕐 Zona horaria: "tz" (the screen), "tz:p:<page>", "tz:set:<zone id>" and "tz:step:-1" / "tz:step:1".
TZ_ACTIONS = ("tz",)


class WorldTimeMixin:
    """Time zones and the world clock (D-124, D-126, D-334). Mixed into GameService; uses its helpers (see the [ES] header).

    [ES] Qué es: la parte de GameService que muestra las horas en la zona de cada jugador y el día, la tarde y la noche del
    mundo. Quién la usa: GameService. Si cambia, afecta: las horas y la franja que ven todos.
    """

    # ------------------------------------------------------------------ settings

    def _tz_cfg(self) -> dict[str, Any]:
        return self.content.balance.get("time_zones") or {}

    def _wc_cfg(self) -> dict[str, Any]:
        return self.content.balance.get("world_clock") or {}

    # ------------------------------------------------------------------ 🕐 the zone of the player being served

    def _tz_current(self) -> str:
        """The zone that applies to the player being served (the chosen one, or the default). [ES] La zona que vale."""
        return tz_rules.resolve(self._tz_cfg(), tz_rules.current())

    def _tz_chosen(self) -> bool:
        """True if the player being served chose a zone that exists. [ES] Dice si el jugador eligió una zona."""
        return tz_rules.known(self._tz_cfg(), tz_rules.current())

    def _tz_offset(self, when: float, zone_id: str | None = None) -> int:
        return tz_rules.offset_seconds(self._tz_cfg(), zone_id if zone_id is not None else tz_rules.current(), when)

    def _tz_short(self, when: float, zone_id: str | None = None) -> str:
        """"UTC−5" (or "UTC") for a zone at an instant. [ES] La zona escrita corta."""
        sign, hours = tz_rules.offset_parts(self._tz_offset(when, zone_id))
        return self.texts.t("tz.offset", sign=sign, hours=hours) if sign else self.texts.t("tz.utc")

    def _tz_name(self, zone_id: str) -> str:
        """A zone's name: its preset's name ("🇨🇴 Colombia, Perú, Ecuador"), "🌐 UTC" or the fixed offset ("UTC−4")."""
        if tz_rules.preset(self._tz_cfg(), zone_id) is not None:
            return self.texts.t(f"tz.preset.{zone_id}")
        if zone_id == tz_rules.UTC_ID:
            return self.texts.t("tz.utc_button")
        return self._tz_short(self.clock.now(), zone_id)

    def _tz_label(self, zone_id: str, when: float | None = None) -> str:
        """A zone with its offset now: "🇨🇴 Colombia, Perú, Ecuador (UTC−5)"; a fixed one alone: "UTC−4"."""
        when = self.clock.now() if when is None else when
        if tz_rules.preset(self._tz_cfg(), zone_id) is not None:
            return self.texts.t("tz.with_offset", name=self._tz_name(zone_id), offset=self._tz_short(when, zone_id))
        return self._tz_short(when, zone_id)

    def _clock(self, when: float) -> str:
        """A clock time in the player's zone: "14:32"; "23/10 14:32" if it is not today there; "14:32 UTC" if never chosen.

        [ES]
        Qué hace: escribe una hora en la zona del jugador que se está atendiendo (o al que va el aviso: _speaking). Si no es
        hoy en su zona, suma la fecha; si nunca eligió zona, suma la zona ("14:32 UTC") para que nadie la confunda con la
        suya. Las duraciones siguen con _fmt_duration: esto es solo para "a qué hora".
        La llaman: el 📜 Tablón, el lote, el viaje, la oleada, la 🗼 Torre de vigía, ⏫ Siguiente nivel, el 🏛️ Mercado, la
        línea del reloj del mundo y ⚙️ Opciones. Si cambia, afecta: todas esas horas.
        """
        offset = self._tz_offset(when)
        text = tz_rules.clock_text(when, offset)
        if not tz_rules.same_day(when, self.clock.now(), offset):
            text = self.texts.t("tz.clock_date", date=tz_rules.date_text(when, offset), time=text)
        if not self._tz_chosen():
            text = self.texts.t("tz.clock_default", time=text, zone=self._tz_short(when))
        return text

    def _local_date(self, when: float) -> str:
        """"23/10" in the player's zone (the 📔 Diario). [ES] La fecha en la zona del jugador."""
        return tz_rules.date_text(when, self._tz_offset(when))

    # ------------------------------------------------------------------ ☀️ 🌇 🌙 the world clock

    def _world_band(self, when: float | None = None) -> dict[str, Any]:
        """The world's band at `when` (now if None): id, start, end, next (world_clock.py band_at, with time_scale)."""
        return wc_rules.band_at(self._wc_cfg(), self.clock.now() if when is None else when, self.time_scale)

    def _band_weights(self, band: str, resources: list[str], base: list[float]) -> list[float]:
        """The weights of a draw with the band's tilt (D-334): each base weight × its resource's weight in that band.

        [ES]
        Qué hace: los pesos del sorteo de una vuelta de recolectar (o de un hallazgo de explorar) con lo que cambia la franja:
        de día pesan más la madera y la piedra; de noche, las hierbas, las setas y el pescado (world_clock.weights). Cambia
        qué sale, no cuánto. La llaman: _gather_step y _explore_step. Si cambia, afecta: qué recursos entran al juego.
        """
        return wc_rules.weighted(self._wc_cfg(), band, resources, base)

    def _world_clock_line(self) -> str:
        """📍 Zona: "☀️ Es de día en el mundo · 🌇 la tarde llega en 5 h 20 min (🕐 18:00)".

        [ES]
        Qué hace: la línea del reloj del mundo: la franja de ahora, cuál sigue, en cuánto (una duración) y a qué hora en la
        zona del jugador. La llaman: _zone_view y la pantalla 🕐 Zona horaria. Si cambia, afecta: solo lo que se lee.
        """
        t = self.texts
        band = self._world_band()
        return t.t("world_clock.zone_line", now=t.t(f"world_clock.now.{band['id']}"), next=t.t(f"world_clock.next.{band['next']}"),
                   time=self._fmt_duration(band["end"] - self.clock.now()), clock=self._clock(band["end"]))

    def _band_tilt_lines(self, hero: Hero, x: int, y: int) -> list[str]:
        """🧭 Explorar: which of the zone's known resources come out more in this band ("☀️ De día, al 🧺 recolectar…")."""
        band = self._world_band()["id"]
        known = [r for r in self._known_resources(hero, x, y) if r in self.content.items]
        favoured = wc_rules.favoured(self._wc_cfg(), band, known)
        if not favoured:
            return []
        t = self.texts
        return [t.t("world_clock.tilt", band=t.t(f"world_clock.tilt_band.{band}"),
                    list=", ".join(self._item_label(r) for r in favoured[:4]))]

    def _world_time_faq_values(self) -> dict[str, Any]:
        """❓ /d05: {world_days} (how many real days a world day lasts) and {world_band_hours} (hours of each band)."""
        cfg = self._wc_cfg()
        hours = max(1.0, float(cfg.get("day_hours", 96)))

        def number(value: float) -> int | float:        # a number, so "{world_days|día|días}" picks the singular for 1
            return int(value) if value == int(value) else round(value, 1)
        return {"world_days": number(hours / 24), "world_band_hours": number(hours / len(wc_rules.bands(cfg)))}

    # ------------------------------------------------------------------ ⚙️ Opciones → 🕐 Zona horaria

    def _tz_options_line(self) -> str:
        """⚙️ Opciones: "🕐 Zona horaria: 🇨🇴 Colombia, Perú, Ecuador (UTC−5) · son las 14:32"."""
        t = self.texts
        now = self.clock.now()
        zone = self._tz_label(self._tz_current(), now)
        if not self._tz_chosen():
            zone = t.t("tz.default_zone", zone=zone)
        return t.t("options.tz_line", zone=zone, time=tz_rules.clock_text(now, self._tz_offset(now)))

    def _tz_entries(self) -> list[tuple[str, str]]:
        """The buttons of 🕐 Zona horaria in order: the presets, 🌐 UTC, then ➖ 1 h and ➕ 1 h."""
        entries = [("set", p["id"]) for p in tz_rules.presets(self._tz_cfg())]
        return entries + [("set", tz_rules.UTC_ID), ("step", "-1"), ("step", "1")]

    def _tz_page_of(self, zone_id: str) -> int:
        """The page whose buttons hold that zone (a fixed offset: the page with ➖ / ➕)."""
        per = max(1, int(self._tz_cfg().get("per_page", 6)))
        entries = self._tz_entries()
        for index, (kind, value) in enumerate(entries):
            if kind == "set" and value == zone_id:
                return index // per
        return (len(entries) - 1) // per

    def _tz_view(self, hero: Hero, page: int = 0, notice: str | None = None) -> View:
        """🕐 Zona horaria: your zone and its time, the game's time (UTC), the world clock and one button per zone.

        [ES]
        Qué hace: la pantalla para elegir la zona horaria (D-124): dice la zona que usas y qué hora es en ella, la hora del
        juego (UTC), la franja del mundo y que las reglas son las mismas para todos; cada zona de la página con la hora que
        muestra (así se elige la que coincide con tu reloj). Botones: hasta time_zones.per_page zonas (✅ en la tuya), ➡️ Más
        zonas o ⬅️ Primeras zonas si hay otra página, y ↩️ Volver a ⚙️ Opciones. En la última página, 🌐 UTC y ➖ 1 h / ➕ 1 h
        (cualquier hora fija de UTC−12 a UTC+14). Es un centro (HUB_KINDS "timezone"): hasta 8 botones.
        La llaman: _tz_action ("tz", "tz:p:<n>" y después de elegir). Si cambia, afecta: tests/test_zona_horaria_y_dia.py.
        """
        t = self.texts
        cfg = self._tz_cfg()
        now = self.clock.now()
        per = max(1, int(cfg.get("per_page", 6)))
        entries = self._tz_entries()
        pages = max(1, math.ceil(len(entries) / per))
        page = int(page) % pages
        current = self._tz_current()
        chosen = self._tz_chosen()
        zone = self._tz_label(current, now)
        body = [t.t("tz.intro"), "",
                t.t("tz.now", zone=zone if chosen else t.t("tz.default_zone", zone=zone),
                    time=tz_rules.clock_text(now, self._tz_offset(now)), date=tz_rules.date_text(now, self._tz_offset(now))),
                t.t("tz.game_clock", time=tz_rules.clock_text(now, 0)), self._world_clock_line(), "", t.t("tz.rules_same"), ""]
        actions: list[Action] = []
        for kind, value in entries[page * per:(page + 1) * per]:
            if kind == "set":
                mark = t.t("options.check_on") + " " if chosen and value == current else ""
                body.append(t.t("tz.choice_line", name=self._tz_name(value),
                                time=tz_rules.clock_text(now, self._tz_offset(now, value))))
                actions.append(Action(id=f"tz:set:{value}", label=mark + self._tz_name(value)))
            else:
                actions.append(Action(id=f"tz:step:{value}", label=t.t("tz.step_minus" if value == "-1" else "tz.step_plus")))
        if any(kind == "step" for kind, _ in entries[page * per:(page + 1) * per]):
            low, high = tz_rules.offset_range(cfg)
            body.append(t.t("tz.step_help", low=self._tz_short(now, tz_rules.fixed_id(low)),
                            high=self._tz_short(now, tz_rules.fixed_id(high))))
        zone_buttons = len(actions)
        layout = [2] * (zone_buttons // 2) + ([1] if zone_buttons % 2 else [])
        if pages > 1:
            nxt = (page + 1) % pages
            body.append(t.t("tz.page", n=page + 1, total=pages))
            actions.append(Action(id=f"tz:p:{nxt}", label=t.t("tz.more" if nxt else "tz.first")))
            layout.append(1)
        actions.append(Action(id="options", label=t.t("menu.back")))
        layout.append(1)
        return View(kind="timezone", title=t.t("tz.title"), body=body, actions=actions, notice=notice, layout=layout)

    def _tz_action(self, hero: Hero, action_id: str) -> View:
        """"tz" opens 🕐 Zona horaria; "tz:p:<n>" a page; "tz:set:<id>" saves a zone; "tz:step:-1|1" moves one hour.

        [ES]
        Qué hace: guarda la zona elegida en "prefs" (campo "tz", junto al idioma) y muestra la misma pantalla ya con la hora
        nueva y el aviso. ➖ / ➕ toman la hora que ves ahora y la corren una hora (una hora fija, de UTC−12 a UTC+14). Una zona
        que no existe (o un preset retirado) no se guarda. Nada del juego cambia: solo cómo se ven las horas (D-124).
        La llama: act() (también mientras exploras o viajas, como ⚙️ Opciones). Si cambia, afecta: lo que se guarda en "prefs".
        """
        t = self.texts
        cfg = self._tz_cfg()
        parts = action_id.split(":")
        if len(parts) >= 3 and parts[1] == "p":
            return self._tz_view(hero, page=int(parts[2]) if parts[2].lstrip("-").isdigit() else 0)
        zone_id = None
        if len(parts) >= 3 and parts[1] == "set":
            wanted = ":".join(parts[2:])
            entry = tz_rules.preset(cfg, wanted)
            if (entry is not None and not entry.get("retired")) or (entry is None and tz_rules.known(cfg, wanted)):
                zone_id = wanted
        elif len(parts) >= 3 and parts[1] == "step" and parts[2] in ("-1", "1"):
            zone_id = tz_rules.step(cfg, tz_rules.current(), self.clock.now(), int(parts[2]))
        if zone_id is None:
            return self._tz_view(hero)
        prefs = self.store.get("prefs", hero.id) or {}
        prefs["tz"] = zone_id
        self.store.put("prefs", hero.id, prefs)
        with tz_rules.use(zone_id):                     # the screen after choosing already shows the new time
            now = self.clock.now()
            notice = t.t("tz.saved", zone=self._tz_label(zone_id, now), time=tz_rules.clock_text(now, self._tz_offset(now)))
            return self._tz_view(hero, page=self._tz_page_of(zone_id), notice=notice)
