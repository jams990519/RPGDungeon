"""The camp's group missions (D-136, confirmed; how it was applied: D-332, provisional; 0.56): one shared goal per level-up.

Every level-up of a player camp (1 → 2 … 8 → 9) asks one group mission besides its works, materials and the castle gates:
a goal the members complete together, with what each member does summed (defeat N monsters, gather N of a resource, bring
N rations to the pantry, win N wave fights). The missions are data (content/story.yaml group_missions, stable ids, one per
target level); their numbers live in balance.yaml group_missions. A mission becomes active when the camp reaches its level
(the founding starts the first one, every level-up the next one) and its goal is fixed then: the base goal grows with the
level and, gently, with the members who played in the last week (ladder.active_days). It counts through the story hook
(_story_event → _gm_event) the same events the weekly camp tasks count, from any place. When it is reached, the camp's 💰
fund gets a small reward (group_missions.reward_per_level × the level the camp is leaving) and every other member is told
in their own language (_push_each). It only gates the next level-up: a camp keeps every level it has (D-64). A camp from
before 0.56 (no record) does not need the mission of the level-up it was already working on: that row reads as done and
its first mission comes with its next level-up (D-332: the fairest option, nobody gets a new obstacle half-way).

[ES]
Para qué sirve: las 🎯 misiones de grupo de D-136 (confirmada por el dueño: "para abrir cada nivel del campamento el grupo
    cumple misiones juntos: farmear, recolectar, llenar la despensa; al terminarlas se abren el siguiente rango de misiones,
    el crecimiento y los materiales"). Capa simple (D-44): una misión por subida de nivel, entre todos los miembros, con lo
    de cada uno sumado (vencer monstruos, juntar un recurso, llevar raciones a la despensa, ganar peleas de oleada). Sale como
    una línea más de ⏫ Siguiente nivel, en 📜 Qué pide cada nivel y en el 📜 Tablón; al cumplirla, un premio chico al 💰 fondo
    del campamento y un aviso a cada miembro en su idioma. Cómo se aplicó lo eligió Claude: D-332 (provisional). Es parte de
    GameService (una "mezcla", como LadderMixin), en su propio archivo para no agrandar game.py.
Documento de diseño: diseno/09-construccion/escalera-del-asentamiento.md §0.7 (cómo quedó) y §2;
    diseno/02-mundo/supervivencia-del-asentamiento.md §0.7
Módulo: capa de servicios (M9 Frontera y Fundación: lo que pide subir de nivel; M10 Misiones: cómo se cuenta)
Depende de: content/story.yaml (group_missions: id → to_level y goal), content/balance.yaml (group_missions: per_member,
    members_cap, reward_per_level; ladder.active_days para "activos"), content/locales/es_misiones_grupo.yaml y
    en_misiones_grupo.yaml (textos), engine.story.rules (target y amount: los mismos tipos de objetivo que los encargos;
    "defend" desde la 0.56) y las ayudas de GameService (_week_active de ladder.py, _camp_top_level, _upgrades,
    _lvlup_rows, _item_list, _item_label, _hero_name, _push_each)
Lo usan: engine/service/game.py (GameService hereda de esta clase): _create_camp y _level_up (_gm_start y _gm_new_line),
    _lvlup_rows (_gm_row, tipo "mission"), _lvlup_view (_gm_how_line), _lvlup_all_view (_gm_all_part); y
    engine/service/story.py: _story_event (_gm_event) y _camp_task_lines del 📜 Tablón (_gm_board_lines)
Eventos que publica: ninguno
Eventos que escucha: ninguno (_gm_event lo llama el gancho de la historia, _story_event)
Datos de los que es dueño: el espacio "group_mission" del almacén, clave "x:y" del campamento:
    {"to": nivel al que sube, "id": la misión (o None si ese nivel no tiene), "n": la meta fijada al empezar, "p": lo
    hecho entre todos, "by": {cuenta: lo suyo}, "active": activos con que se fijó la meta, "since": cuándo empezó,
    "done_at": cuándo se cumplió (se paga una sola vez), "reward": lo que recibió el fondo}. Se escribe al fundar, al subir
    de nivel y con cada cosa que cuenta. Un campamento sin registro (de antes de la 0.56) o con uno de otro nivel no tiene
    misión que cumplir en esa subida.
Reglas que nunca se rompen:
    1. Nadie pierde (D-64): la misión solo traba la subida siguiente; nunca quita niveles, zonas, miembros ni nada personal.
       Un campamento de antes de la 0.56 no necesita la misión de la subida en la que ya estaba (D-332).
    2. Cada misión se paga una sola vez ("done_at"); lo que pasa después de cumplirla no cuenta.
    3. Solo cuentan los miembros del campamento (no quien espera lugar en el gremio ni un visitante), en cualquier lugar.
    4. La meta queda fija al empezar: que entren o salgan miembros no la cambia a mitad de camino.
    5. Ningún texto visible se escribe aquí: todo sale de content/locales (es_misiones_grupo.yaml y en_misiones_grupo.yaml),
       y todo aviso a otro jugador se arma con _push_each (le llega en su idioma, D-250).
    6. El premio va al 💰 fondo ("upgrades"."fund"), nunca a la mochila de nadie, y no sube el nivel solo: si era lo último,
       cualquier miembro toca ⏫ Subir. _gm_event solo lo llaman eventos (ganar, recolectar, alimentar) que no guardan
       "upgrades" después: si otro camino lo llamara así, pisaría el premio.
Si cambias esto, revisa:
    - Datos y números: content/story.yaml group_missions (una por nivel de destino; ids estables, retired: true para
      retirar) y balance.yaml group_missions (per_member, members_cap, reward_per_level); el registro de balance
      (diseno/03-personaje/balance.md §7, 0.56)
    - Lo que cuenta: engine/story/rules.py amount (win, gather, feed y defend) y las llamadas a _story_event de game.py
      (_end_combat manda raid=True en las peleas de oleada; _gather_step; _camp_feed)
    - Mapa de impacto: diseno/01-plataforma/mapa-de-impacto.md (M9, M10 y la cascada C-36)
    - Pruebas: tests/test_misiones_de_grupo.py; las que suben campamentos de nivel (tests/test_siguiente_nivel.py y las que
      usan pass_group_mission de tests/conftest.py)
"""

from __future__ import annotations

import math
from typing import Any

from engine.hero import Hero
from engine.messaging import View
from engine.story import rules as story_rules

GM_SPACE = "group_mission"
GM_EVENTS = ("win", "gather", "feed")       # the story events a group mission can count ("defend" is a "win" with raid=True)
EPS = 1e-9


class GroupMissionMixin:
    """The camp's group missions (D-136, D-332). Mixed into GameService; uses its helpers (see the [ES] header).

    [ES]
    Qué es: una 🎯 misión de grupo por cada subida de nivel del campamento, contada entre todos los miembros.
    Quién la usa: GameService (hereda de esta clase) y StoryMixin (el gancho _story_event y el 📜 Tablón).
    Si cambia, afecta: qué pide cada subida de nivel y lo que dicen ⏫ Siguiente nivel, 📜 y el Tablón.
    """

    # ------------------------------------------------------------------ data

    def _gm_cfg(self) -> dict[str, Any]:
        return self.content.balance.get("group_missions", {}) or {}

    def _gm_defs(self) -> dict[str, dict[str, Any]]:
        """content/story.yaml group_missions without the retired ones (id → {to_level, goal})."""
        pool = (self.content.story or {}).get("group_missions") or {}
        return {mid: mdef for mid, mdef in pool.items() if not mdef.get("retired") and (mdef.get("goal") or {}).get("kind")}

    def _gm_for_level(self, to_level: int) -> str | None:
        """The mission of the level-up TO `to_level` (the first one in the file), or None if that level has none."""
        return next((mid for mid, mdef in self._gm_defs().items() if int(mdef.get("to_level", 0)) == int(to_level)), None)

    @staticmethod
    def _gm_key(camp: dict[str, Any]) -> str:
        return f"{camp['x']}:{camp['y']}"

    def _gm_target(self, mid: str, active: int) -> int:
        """The goal of a mission for a camp with `active` members: n × (1 + per_member × (active − 1)), active capped.

        [ES] Qué hace: la meta crece con el nivel (la n de cada misión en story.yaml) y, poco, con los miembros activos: cada
        activo después del primero suma group_missions.per_member (15 %) de la n, contando como mucho members_cap (40).
        Redondea hacia arriba. La llaman: _gm_start y _gm_all_part. Si cambia, afecta: cuánto pide cada misión."""
        cfg = self._gm_cfg()
        base = story_rules.target((self._gm_defs().get(mid) or {}).get("goal") or {})
        cap = max(1, int(cfg.get("members_cap", 40) or 40))
        active = max(1, min(int(active), cap))
        return max(1, math.ceil(base * (1 + float(cfg.get("per_member", 0.0) or 0.0) * (active - 1)) - EPS))

    def _gm_reward(self, level: int) -> dict[str, int]:
        """What the camp's 💰 fund gets for a mission done while at `level`: group_missions.reward_per_level × level."""
        per = self._gm_cfg().get("reward_per_level") or {}
        return {i: int(n) * int(level) for i, n in per.items() if i in self.content.items and int(n) > 0}

    # ------------------------------------------------------------------ the record

    def _gm_start(self, key: str, camp: dict[str, Any], actor: Hero | None = None) -> None:
        """Start the mission of the camp's next level-up: its goal is fixed now, with the members active this week.

        [ES] Qué hace: escribe en "group_mission"/<x:y> la misión de la subida siguiente (la del nivel del campamento + 1), con
        su meta fijada con los activos de la semana (_week_active, ladder.active_days; quien la empieza cuenta), y lo hecho en
        0. Si ese nivel no tiene misión, guarda el nivel sin misión (no traba nada). En el último nivel no hace nada. La llaman:
        game.py _create_camp (la primera, al fundar) y _level_up (la siguiente). Si cambia, afecta: cuándo empieza cada misión."""
        level = int(camp.get("level", 1))
        if level >= self._camp_top_level():
            return
        mid = self._gm_for_level(level + 1)
        active = max(1, self._week_active(camp, actor))
        self.store.put(GM_SPACE, key, {"to": level + 1, "id": mid, "n": self._gm_target(mid, active) if mid else 0,
                                       "p": 0, "by": {}, "active": active, "since": self.clock.now()})

    def _gm_state(self, camp: dict[str, Any]) -> dict[str, Any] | None:
        """The mission of the camp's next level-up: its record, {"waived": True} (a camp from before 0.56), or None.

        [ES] Qué hace: lee la misión de la subida siguiente. Sin registro, o con uno de otro nivel (un campamento de antes de
        la 0.56, D-332), esa subida no la pide: devuelve "waived" si ese nivel tiene misión en story.yaml. None si el campamento
        ya está en el último nivel, si ese nivel no tiene misión o si su misión se retiró (nada que mostrar ni que trabe).
        La llaman: _gm_row, _gm_how_line, _gm_board_lines y _gm_all_part."""
        level = int(camp.get("level", 1))
        if level >= self._camp_top_level():
            return None
        record = self.store.get(GM_SPACE, self._gm_key(camp))
        if record is None or int(record.get("to", 0)) != level + 1:
            return {"to": level + 1, "waived": True} if self._gm_for_level(level + 1) else None
        if record.get("id") not in self._gm_defs():
            return None
        return record

    @staticmethod
    def _gm_done(record: dict[str, Any]) -> bool:
        return bool(record.get("done_at")) or int(record.get("p", 0)) >= int(record.get("n", 0) or 0) > 0

    # ------------------------------------------------------------------ texts

    def _gm_goal_text(self, mid: str, n: int) -> str:
        """"vencer 20 monstruos", "juntar 96 🪵 Madera", "llevar 32 raciones a la despensa", "ganar 5 peleas de oleada"."""
        goal = (self._gm_defs().get(mid) or {}).get("goal") or {}
        kind = goal.get("kind")
        if kind == "gather" and goal.get("item") in self.content.items:
            return self.texts.t("gm.goal.gather_item", n=n, item=self._item_label(goal["item"]))
        return self.texts.t(f"gm.goal.{kind}", n=n)

    def _gm_row(self, camp: dict[str, Any]) -> tuple[str, bool] | None:
        """⏫ Siguiente nivel's row: "🎯 Misión de grupo: vencer 20 monstruos — 7 de 20 (faltan 13)" (None: nothing to show).

        [ES] Qué hace: la línea de la misión en la lista de la subida (D-313: dice exactamente qué falta): en curso, cumplida
        o, en un campamento de antes de la 0.56, que esta subida no la pide (✅). La llama: game.py _lvlup_rows (tipo
        "mission"). Si cambia, afecta: tests/test_misiones_de_grupo.py y la cuenta "x de y listos" de 🔨 Mejoras."""
        state = self._gm_state(camp)
        if state is None:
            return None
        t = self.texts
        if state.get("waived"):
            return t.t("gm.row_waived"), True
        n = int(state["n"])
        goal = self._gm_goal_text(state["id"], n)
        if self._gm_done(state):
            return t.t("gm.row_done", goal=goal), True
        p = min(n, int(state.get("p", 0)))
        return t.t("gm.row", goal=goal, p=p, n=n, left=n - p), False

    def _gm_how_line(self, camp: dict[str, Any], hero: Hero) -> str:
        """⏫ Siguiente nivel, while the mission is missing: what counts, what you did and what the fund gets."""
        state = self._gm_state(camp)
        if state is None or state.get("waived"):
            return ""
        kind = ((self._gm_defs().get(state["id"]) or {}).get("goal") or {}).get("kind", "win")
        return self.texts.t("gm.how", how=self.texts.t(f"gm.how_{kind}"), mine=int((state.get("by") or {}).get(hero.id, 0)),
                            reward=self._item_list(self._gm_reward(int(state["to"]) - 1)))

    def _gm_new_line(self, key: str) -> str:
        """"🎯 Nueva misión de grupo para subir a nivel 3: juntar 96 🪵 Madera." (empty if the next level has none)."""
        record = self.store.get(GM_SPACE, key) or {}
        if record.get("id") not in self._gm_defs():
            return ""
        return self.texts.t("gm.new", level=int(record["to"]), goal=self._gm_goal_text(record["id"], int(record["n"])))

    def _gm_all_part(self, camp: dict[str, Any], target: int, active: int | None = None) -> str:
        """📜 Qué pide cada nivel: " · 🎯 vencer 20 monstruos" for the level-up to `target` ("" if none or not needed).

        [ES] Qué hace: la subida en curso dice su meta fijada (o nada si esta subida no la pide); las siguientes, la meta con
        los activos de hoy (`active`, que el llamador cuenta una vez para toda la lista; puede cambiar hasta que empiece).
        La llama: game.py _lvlup_all_view."""
        level = int(camp.get("level", 1))
        if target == level + 1:
            state = self._gm_state(camp)
            if state is None or state.get("waived"):
                return ""
            mid, n = state["id"], int(state["n"])
        else:
            mid = self._gm_for_level(target)
            if not mid:
                return ""
            n = self._gm_target(mid, max(1, self._week_active(camp) if active is None else active))
        return self.texts.t("gm.all", goal=self._gm_goal_text(mid, n))

    def _gm_board_lines(self, hero: Hero, camp: dict[str, Any]) -> list[str]:
        """📜 Tablón, under the weekly camp tasks: the group mission of the next level-up, with yours (or that it is not needed)."""
        state = self._gm_state(camp)
        if state is None:
            return []
        t = self.texts
        if state.get("waived"):
            return [t.t("gm.board_waived", level=int(state["to"]))]
        n = int(state["n"])
        mark = t.t("story.mark_done" if self._gm_done(state) else "story.mark_todo")
        return [t.t("gm.board_line", mark=mark, level=int(state["to"]), goal=self._gm_goal_text(state["id"], n),
                    p=min(n, int(state.get("p", 0))), n=n, mine=int((state.get("by") or {}).get(hero.id, 0)))]

    # ------------------------------------------------------------------ counting

    def _gm_event(self, hero: Hero, kind: str, data: dict[str, Any]) -> list[str]:
        """Count what a member did for the camp's group mission; when it is reached, reward the fund and tell everyone.

        [ES] Qué hace: suma a la misión de la subida en curso lo que hizo un miembro, donde esté: cada pelea ganada (vencer
        monstruos; con raid=True también es una pelea de oleada para "defend"), cada unidad recolectada (de un recurso o de
        cualquiera) o cada ración llevada a la despensa (story_rules.amount, los mismos tipos que los encargos de campamento).
        Guarda lo de todos ("p") y lo de cada uno ("by"). Al llegar a la meta la cierra una sola vez (_gm_complete). Como mucho
        dos lecturas y una escritura. La llama: story.py _story_event. Si cambia, afecta: tests/test_misiones_de_grupo.py."""
        if not hero.camp or kind not in GM_EVENTS:
            return []
        camp = self.store.get("camp", hero.camp)
        if not camp or hero.id not in camp.get("members", []):
            return []
        record = self.store.get(GM_SPACE, hero.camp)
        if not record or record.get("done_at") or int(record.get("to", 0)) != int(camp.get("level", 1)) + 1:
            return []
        mdef = self._gm_defs().get(record.get("id"))
        if not mdef:
            return []
        got = story_rules.amount(mdef["goal"], kind, data)
        if got <= 0:
            return []
        record["p"] = int(record.get("p", 0)) + got
        by = record.setdefault("by", {})
        by[hero.id] = int(by.get(hero.id, 0)) + got
        lines: list[str] = []
        if record["p"] >= int(record.get("n", 0) or 0):
            record["done_at"] = self.clock.now()
            record["reward"] = self._gm_reward(int(record["to"]) - 1)
            self.store.put(GM_SPACE, hero.camp, record)
            lines = self._gm_complete(hero, camp, record)
        else:
            self.store.put(GM_SPACE, hero.camp, record)
        return lines

    def _gm_complete(self, hero: Hero, camp: dict[str, Any], record: dict[str, Any]) -> list[str]:
        """A mission was reached: the reward goes to the camp's 💰 fund, the others are told; the line for who closed it.

        [ES] Qué hace: suma el premio (group_missions.reward_per_level × el nivel que deja) al 💰 fondo del campamento
        ("upgrades"."fund", como la 🌾 cosecha: lo toman las obras activas y ⏫ Siguiente nivel la próxima vez que alguien
        aporta o deposita, y lo que sobra, los oficios), avisa a cada otro miembro en su idioma (_push_each: quién la cerró,
        cuánto puso cada uno y el premio) y, si con eso toda la lista de la subida está ✅, dice que cualquiera puede tocar
        ⏫ Subir (no sube sola: así no cambia el nivel en medio de una pelea o un lote). La llama: _gm_event."""
        t = self.texts
        key = hero.camp
        reward = dict(record.get("reward") or {})
        if reward:
            upgrades = self._upgrades(key)
            for item, n in reward.items():
                upgrades["fund"][item] = int(upgrades["fund"].get(item, 0)) + n
            self.store.put("upgrades", key, upgrades)
        name, n, mid = camp.get("name", "?"), int(record["n"]), record["id"]
        by = dict(record.get("by") or {})
        ready = all(ok for _, _, ok in self._lvlup_rows(camp, self._upgrades(key), hero))
        target = int(record["to"])

        def news(mine: int) -> View:
            body = [t.t("gm.push", hero=hero.name, camp=name, goal=self._gm_goal_text(mid, n), n=n, mine=mine,
                        reward=self._item_list(reward) if reward else t.t("gm.no_reward"))]
            return View(kind="camp_news", title=t.t("gm.push_title"),
                        body=body + ([t.t("gm.ready", level=target)] if ready else []))

        for member in [m for m in camp.get("members", []) if m != hero.id]:     # each one reads their own share
            self._push_each([member], lambda member=member: news(int(by.get(member, 0))))
        lines = [t.t("gm.done", camp=name, goal=self._gm_goal_text(mid, n), mine=int(by.get(hero.id, 0)), n=n,
                     reward=self._item_list(reward) if reward else t.t("gm.no_reward"))]
        if ready:
            lines.append(t.t("gm.ready", level=target))
        return lines
