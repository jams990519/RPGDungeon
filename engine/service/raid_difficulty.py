"""⚔️ Escalating difficulty of the camps' waves (D-153, confirmed in E-37; how it was applied: D-337, provisional; 0.61).

"It starts medium and grows with time and progress. At the castle, the enemies already know where you are and the waves are
stronger." A camp's NORMAL raid (raids.per_week, D-154) comes with a strength multiplier on its attackers' life and attack,
fixed when the raid opens (camp["raid"]["difficulty"]) and applied in _defend before the camp's 🛡️ Defensa (D-101):
(base + per_level × (level − 1) + per_week × weeks since founding, capped at time_cap) × castle_mult at the castle
(engine/world/raids.py difficulty_parts). The base (1.0) is the wave of before 0.61, "medium". The level counts up to the
city's (the castle is "the city × castle_mult"). The Noche de prueba and the castle's growing waves (D-329) keep their own
strength and never add this: a raid with "wave" gets no "difficulty". Weeks count from camp["created"]; a camp without it
counts from the first time the raid clock sees it after the patch (camp["difficulty_from"]). The difficulty only reads the
camp: nothing is lost (D-64), and raids already open keep the strength they had.

[ES]
Para qué sirve: la ⚔️ dificultad escalonada de D-153 (confirmada por el dueño en la entrevista de voz, E-37: "empieza media y
    sube con el tiempo y el avance; al llegar a castillo, los enemigos ya saben dónde estás y las oleadas son más fuertes") en la
    capa simple (D-44): las oleadas NORMALES de cada campamento llegan un poco más fuertes con el nivel del campamento y con las
    semanas desde que se fundó (con tope), y un 25 % más en el castillo. Cómo se aplicó lo eligió Claude: D-337 (provisional),
    y se le pregunta al dueño (E-284 a E-286). Es parte de GameService (una "mezcla", como LadderMixin), en su propio archivo
    para no agrandar game.py.
Documento de diseño: diseno/09-construccion/escalera-del-asentamiento.md §0.8 y diseno/02-mundo/supervivencia-del-asentamiento.md
    §0.5 (cómo quedó); diseno/03-personaje/balance.md (registro de balance, 0.61)
Módulo: capa de servicios (M9 Frontera y Fundación: las oleadas de los campamentos)
Depende de: content/balance.yaml (raids.difficulty: base, per_level, per_week, time_cap, castle_mult y labels; raids.trial.to_level,
    el castillo), engine.world.raids (difficulty_parts, difficulty_label), content/locales/es_dificultad.yaml y
    en_dificultad.yaml (textos) y las ayudas de GameService (_day_seconds, _castle_wave_next, texts)
Lo usan: engine/service/game.py (GameService hereda de esta clase): _raid_settle (_difficulty_mark: la fecha del parche en un
    campamento sin "created"), _open_raid (_difficulty_for_raid: fija la fuerza de la oleada normal que llega), _defend (la
    aplica a la pelea y dice _difficulty_fight_line), _raid_notice (_difficulty_open_lines), _raid_watch y _raid_lines
    (_difficulty_lines y _difficulty_open_lines: 🗼 el aviso de la torre, 🏰 Gestionar, ℹ️ Información y la oleada en curso),
    _lvlup_view (_difficulty_lvlup_line: el aviso del paso a castillo) y _faq_values (_difficulty_faq_values: ❓ /d66)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño (dentro del registro "camp", clave "x:y"):
    "raid"."difficulty": la fuerza de la oleada normal abierta (×1,00 en adelante), fijada al abrirse; la 🌙 Noche de prueba y
        las 🌊 oleadas crecientes no la llevan.
    "difficulty_from": solo en un campamento sin "created" (no debería haber: todos lo guardan desde que existen): la hora en que
        el reloj de las oleadas lo vio por primera vez después de la 0.61; las semanas cuentan desde ahí.
Reglas que nunca se rompen:
    1. Solo las oleadas normales: la 🌙 Noche de prueba (raids.trial) y las 🌊 oleadas crecientes (D-329, una oleada con "wave")
       siguen exactamente como estaban; los monstruos de afuera (lo del héroe) no cambian.
    2. Suave y con tope (D-153, D-44): el nivel cuenta como mucho el de la ciudad y el tiempo como mucho time_cap; la 🛡️ Defensa
       frena después, como siempre (D-101), así que las defensas construidas y reparadas mantienen las oleadas ganables.
    3. Nadie pierde nada (D-64): solo cambia la fuerza de las oleadas que se abran desde ahora; una oleada abierta guarda la suya.
    4. Ningún texto visible se escribe aquí: todo sale de content/locales (es_dificultad.yaml y en_dificultad.yaml); los avisos a
       otros jugadores los arman los llamadores con _push_each (D-250), y estas funciones solo leen (se llaman una vez por
       jugador).
Si cambias esto, revisa:
    - Números: balance.yaml raids.difficulty y el registro de balance (diseno/03-personaje/balance.md, 0.61)
    - Pantallas: el aviso de la oleada, la 🗼 torre, 🏰 Gestionar, ℹ️ Información, ⏫ Siguiente nivel del nivel 8 y ❓ /d66 y /d39
    - Mapa de impacto: diseno/01-plataforma/mapa-de-impacto.md (M9 "La dificultad escalonada" y la cascada C-40)
    - Pruebas: tests/test_dificultad_escalonada.py; tests/test_raids.py (la oleada con defensas) y
      tests/test_oleadas_crecientes_castillo.py (la serie sin cambios)
"""

from __future__ import annotations

from typing import Any

from engine.world import raids as raid_rules


class RaidDifficultyMixin:
    """The camps' escalating wave difficulty (D-153, D-337). Mixed into GameService; uses its helpers (see the [ES] header).

    [ES]
    Qué es: la fuerza de las oleadas normales según el nivel, las semanas y el castillo, y las líneas que la muestran.
    Quién la usa: GameService (hereda de esta clase).
    Si cambia, afecta: qué tan fuertes llegan las oleadas normales de todos los campamentos y lo que se lee de ellas.
    """

    def _difficulty_cfg(self) -> dict[str, Any]:
        return self.content.balance["raids"].get("difficulty") or {}

    def _difficulty_castle_level(self) -> int:
        """The castle's level (raids.trial.to_level, 9: the same one the growing waves and the Noche de prueba use)."""
        return int(self.content.balance["raids"]["trial"]["to_level"])

    def _difficulty_start(self, camp: dict[str, Any]) -> float | None:
        """When the camp's weeks start: camp["created"], or camp["difficulty_from"] (stamped after the patch), or None."""
        for field in ("created", "difficulty_from"):
            if camp.get(field) is not None:
                return float(camp[field])
        return None

    def _difficulty_mark(self, camp: dict[str, Any]) -> bool:
        """game.py _raid_settle: a camp without "created" starts its weeks now (the patch, D-64). True if it wrote something.

        [ES] Qué hace: si el campamento no guarda su fecha de fundación ("created"), anota la hora de hoy ("difficulty_from")
        para contar las semanas desde el parche y no desde antes. Todos los campamentos guardan "created" desde que existen, así
        que casi nunca escribe. La llama: game.py _raid_settle (el llamador guarda). Si cambia, afecta: desde cuándo sube la
        dificultad de un campamento sin fecha."""
        if self._difficulty_start(camp) is not None:
            return False
        camp["difficulty_from"] = self.clock.now()
        return True

    def _difficulty_parts(self, camp: dict[str, Any]) -> dict[str, float]:
        """{"level", "time", "castle", "mult"} of the camp's next normal wave, now (engine/world/raids.py difficulty_parts).

        [ES] Qué hace: la fuerza que tendría hoy una oleada normal del campamento y de dónde sale (el nivel, las semanas desde la
        fundación y el castillo). Sin fecha de fundación todavía, las semanas cuentan 0. La llaman: _difficulty_for_raid y las
        líneas de esta mezcla. Si cambia, afecta: tests/test_dificultad_escalonada.py."""
        start = self._difficulty_start(camp)
        days = 0.0 if start is None else max(0.0, (self.clock.now() - start) / self._day_seconds())
        return raid_rules.difficulty_parts(int(camp.get("level", 1)), days, self._difficulty_cfg(),
                                           self._difficulty_castle_level())

    def _difficulty_for_raid(self, camp: dict[str, Any], raid: dict[str, Any]) -> None:
        """game.py _open_raid: fix the strength of a normal raid as it arrives ("difficulty"); never the trial or a growing wave.

        [ES] Qué hace: guarda en la oleada que llega su fuerza de hoy (raid["difficulty"]), que _defend aplica a cada pelea antes
        de la 🛡️ Defensa. No la pone en la 🌙 Noche de prueba ni en una 🌊 oleada creciente (la que tiene "wave": D-329 queda
        igual), ni si raids.difficulty no está. La llama: game.py _open_raid, después de _castle_wave_mark. Si cambia, afecta:
        qué tan fuertes llegan las oleadas normales."""
        if raid.get("kind") != "raid" or raid.get("wave") or not self._difficulty_cfg():
            return
        raid["difficulty"] = round(self._difficulty_parts(camp)["mult"], 4)

    # ------------------------------------------------------------------ what players read

    def _difficulty_num(self, value: float) -> str:
        """×1,12 in Spanish, ×1.12 in English: always two decimals (common.decimal_sep, D-250)."""
        return f"{float(value):.2f}".replace(".", self.texts.t("common.decimal_sep"))

    def _difficulty_label(self, mult: float) -> str:
        labels = self._difficulty_cfg().get("labels") or {}
        return self.texts.t(f"difficulty.label.{raid_rules.difficulty_label(mult, labels)}")

    def _difficulty_line(self, parts: dict[str, float]) -> str:
        """"⚔️ Dificultad de las oleadas: media ×1,09 (+6 % por el nivel y +3 % por el tiempo…)" (with the castle's × at the castle)."""
        values = {"label": self._difficulty_label(parts["mult"]), "mult": self._difficulty_num(parts["mult"]),
                  "lvl": int(round(parts["level"] * 100)), "time": int(round(parts["time"] * 100)),
                  "castle": self._difficulty_num(parts["castle"])}
        return self.texts.t("difficulty.line_castle" if parts["castle"] > 1 else "difficulty.line", **values)

    def _difficulty_castle_line(self, castle: float) -> list[str]:
        """"👁️ Los enemigos saben dónde está tu castillo: las oleadas llegan más fuertes (+25 %)." (empty before the castle)."""
        if castle <= 1:
            return []
        return [self.texts.t("difficulty.castle_line", pct=int(round((castle - 1) * 100)))]

    def _difficulty_lines(self, camp: dict[str, Any]) -> list[str]:
        """The camp's difficulty for its NEXT wave: 🗼 the watchtower, 🏰 Gestionar and ℹ️ Información (game.py _raid_lines).

        [ES] Qué hace: la línea "⚔️ Dificultad de las oleadas: media ×1,09 (…)" y, en el castillo, "👁️ Los enemigos saben dónde
        está tu castillo…". Si la próxima oleada es una 🌊 oleada creciente (nivel 8, D-329), dice que esa lleva su propia fuerza
        y cuál vuelve después. Sin raids.difficulty, nada. Solo lee (la llaman dentro de _push_each). La llaman: game.py
        _raid_lines y _raid_watch. Si cambia, afecta: tests/test_dificultad_escalonada.py."""
        if not self._difficulty_cfg():
            return []
        parts = self._difficulty_parts(camp)
        if self._castle_wave_next(camp) is not None:
            return [self.texts.t("difficulty.series_line", label=self._difficulty_label(parts["mult"]),
                                 mult=self._difficulty_num(parts["mult"]))]
        return [self._difficulty_line(parts)] + self._difficulty_castle_line(parts["castle"])

    def _difficulty_open_lines(self, camp: dict[str, Any], raid: dict[str, Any]) -> list[str]:
        """The difficulty of a normal raid that is ON (the arrival notice, the camp screen): its fixed strength.

        [ES] Qué hace: "⚔️ Dificultad de esta oleada: media ×1,09 (+9 % de vida y de ataque)" con la fuerza guardada en la oleada
        abierta (no la de hoy: una oleada nunca cambia mientras dura) y, en el castillo, la línea 👁️. La 🌙 Noche de prueba,
        una 🌊 oleada creciente o una oleada abierta antes del parche (sin "difficulty") no dicen nada. La llaman: game.py
        _raid_notice y _raid_lines. Si cambia, afecta: lo que se lee de la oleada en curso."""
        if raid.get("kind") != "raid" or raid.get("wave") or raid.get("difficulty") is None:
            return []
        mult = float(raid["difficulty"])
        pct = max(0, int(round((mult - 1) * 100)))
        line = self.texts.t("difficulty.open_line" if pct else "difficulty.open_line_base", label=self._difficulty_label(mult),
                            mult=self._difficulty_num(mult), pct=pct)
        return [line] + self._difficulty_castle_line(self._difficulty_parts(camp)["castle"])

    def _difficulty_fight_line(self, raid: dict[str, Any]) -> str | None:
        """The defender's line when the fight starts: "⚔️ Dificultad ×1,09: +9 % de vida y de ataque." (None at ×1 or none)."""
        mult = float(raid.get("difficulty", 1.0) or 1.0)
        if mult <= 1 + 1e-9:
            return None
        return self.texts.t("difficulty.fight", mult=self._difficulty_num(mult), pct=int(round((mult - 1) * 100)))

    def _difficulty_lvlup_line(self, target: int) -> str | None:
        """⏫ Siguiente nivel to the castle: "👁️ En el castillo los enemigos sabrán dónde están…" (None for any other level)."""
        cfg = self._difficulty_cfg()
        castle = float(cfg.get("castle_mult", 1.0) or 1.0) if cfg else 1.0
        if int(target) != self._difficulty_castle_level() or castle <= 1:
            return None
        return self.texts.t("difficulty.lvlup_castle", pct=int(round((castle - 1) * 100)))

    def _difficulty_faq_values(self) -> dict[str, Any]:
        """{diff_level}, {diff_week}, {diff_cap}, {diff_cap_weeks} and {diff_castle} for ❓ /d66 (percent, from balance.yaml)."""
        cfg = self._difficulty_cfg()
        per_week = float(cfg.get("per_week", 0) or 0)
        cap = float(cfg.get("time_cap", 0) or 0)
        weeks = cap / per_week if per_week > 0 else 0
        sep = self.texts.t("common.decimal_sep")
        return {"diff_level": f"{float(cfg.get('per_level', 0) or 0) * 100:g}".replace(".", sep),
                "diff_week": f"{per_week * 100:g}".replace(".", sep),
                "diff_cap": f"{cap * 100:g}".replace(".", sep),
                "diff_cap_weeks": f"{weeks:g}".replace(".", sep),
                "diff_castle": int(round((float(cfg.get("castle_mult", 1.0) or 1.0) - 1) * 100))}
