"""Story and roleplay screens of the game service (D-117, provisional): a mixin of GameService.

Simple layer of diseno/06-contenido/historia-y-rol.md §1: the hero's origin and its mission chain, the campaign by
chapters (chapter 1 in and around the Claro), named characters, three factions with reputation ranks, daily tasks of
the Claro board and weekly camp tasks, the hero journal, and small roleplay between players (/bio, /saludar, /brindar,
the profession emblem next to the name). The story itself is data (content/story.yaml + es_historia.yaml); this file
only runs it. Missions advance from real game events through one hook, _story_event(hero, kind, **data), that
GameService calls from the right places (explore, gather, fights won, craft, sell, arrive, found a camp, feed the
pantry, give to a work).

[ES]
Para qué sirve: las pantallas y las reglas guardadas de la historia y el rol: 📖 Historia (con 🎯 Misiones,
🧑 Personajes, ⚜️ Facciones y 📔 Diario), el 📜 Tablón del Claro, la elección del 🎭 origen, hablar con los personajes,
las decisiones, la reputación y sus rangos, los encargos del día y del campamento, el diario y su tarjeta, /bio, los
gestos y el emblema. Es parte de GameService (una "mezcla": GameService hereda de StoryMixin), separada en su propio
archivo para no agrandar game.py; usa sus ayudas (_give_xp, _bag_add, _zone_players, _push, _main_view...).
Documento de diseño: diseno/06-contenido/historia-y-rol.md §1 y "En el juego"; diseno/03-personaje/creacion-de-personaje.md §4
Módulo: capa de servicios (M10 Misiones; personajes, facciones y diario con M2 Héroe y M15 Social)
Depende de: engine.story (cuentas puras), engine.messaging, engine.hero, content/story.yaml,
    content/locales/es_historia.yaml, content/balance.yaml (bloque story)
Lo usan: engine/service/game.py (GameService hereda de esta clase; llama a _story_event, _story_action, _typed_command,
    _origin_offer, _origin_view, _story_hero_lines, _title_name, _emblem_name, _origin_prof_bonus, _shop_price, _journal)
Eventos que publica: ninguno
Eventos que escucha: ninguno (el gancho _story_event lo llama el servicio)
Datos de los que es dueño: Hero.origin, Hero.story, Hero.factions, Hero.journal, Hero.bio; espacio "camp_tasks" del
    almacén (clave "x:y" del campamento: {"week", "p" {encargo: avance}, "by" {encargo: {héroe: aporte}}, "paid"}),
    que se renueva solo cada semana
Reglas que nunca se rompen:
    1. Nada bloquea el juego: el origen se puede elegir después y el menú de abajo siempre funciona.
    2. Cada misión, paso, premio de rango y encargo se paga una sola vez.
    3. Una cosa que pasa en el juego avanza como mucho un paso de cada misión (el paso siguiente cuenta desde ahí).
    4. La historia nunca da poder de combate por sí sola (rasgos de oficio, precio o reputación; premios de monedas,
       consumibles, materiales y títulos).
    5. Los gestos y 📣 Mostrar solo llegan a los jugadores presentes en tu zona (D-96) y como mucho uno por minuto.
Si cambias esto, revisa:
    - Servicio: engine/service/game.py (llamadas a _story_event en _explore_step, _gather_step, _end_combat y
      _auto_combat, _make, _sell, _camp_sell, _sell_gear, _arrive, _found_camp, _camp_feed, _give_to_work y _give_to_study; el menú y
      los atajos; _hero_view; _claro_view; text())
    - Números: balance.yaml story (experiencia por ⚡, rangos, largo de la biografía, tope del diario, espera de gestos)
    - Datos: content/story.yaml y content/locales/es_historia.yaml
    - Pruebas: tests/test_story.py
"""

from __future__ import annotations

import time
from typing import Any

from engine.hero import Hero
from engine.messaging import Action, View
from engine.story import rules as story_rules

# Story button ids (or prefixes): _story_action routes them (GameService._idle_action sends them here).
STORY_ACTIONS = ("story", "squests", "board", "npcs", "npc:", "talk:", "ch:", "factions", "journal", "jshow",
                 "origin", "orig:", "origpick:", "bio", "gesture:")
# Events the daily tasks and the camp tasks can count. [ES] Lo que cuentan los encargos del día y los del campamento.
TASK_EVENTS = ("explore", "gather", "win", "craft", "sell")
CAMP_EVENTS = ("explore", "gather", "win", "feed", "build")


class StoryMixin:
    """Story and roleplay part of GameService (needs its content, store, clock, texts and helpers).

    [ES]
    Qué es: la parte de la historia y el rol del servicio del juego, en su propio archivo.
    Quién la usa: GameService (hereda de aquí).
    Si cambia, afecta: 📖 Historia, el 📜 Tablón, los personajes, el origen, el diario y los gestos.
    """

    # ------------------------------------------------------------------ data

    def _story_cfg(self) -> dict[str, Any]:
        return self.content.balance["story"]

    def _story_data(self) -> dict[str, Any]:
        return self.content.story or {}

    def _quest_defs(self) -> dict[str, dict[str, Any]]:
        quests = self._story_data().get("quests") or {}
        return {qid: q for qid, q in quests.items() if not q.get("retired")}

    def _origin_defs(self) -> dict[str, dict[str, Any]]:
        origins = self._story_data().get("origins") or {}
        return {oid: o for oid, o in origins.items() if not o.get("retired")}

    def _npc_defs(self) -> dict[str, dict[str, Any]]:
        return self._story_data().get("npcs") or {}

    def _faction_defs(self) -> dict[str, dict[str, Any]]:
        return self._story_data().get("factions") or {}

    def _ranks(self) -> list[dict[str, Any]]:
        return self._story_cfg()["ranks"]

    def _st(self, hero: Hero) -> dict[str, Any]:
        """The hero's story record with every key present (heroes saved before D-117 have an empty one)."""
        st = hero.story
        for key, empty in (("q", {}), ("done", []), ("c", {}), ("met", []), ("ranks", {}), ("jt", []), ("jg", [])):
            if not isinstance(st.get(key), type(empty)):
                st[key] = type(empty)()
        st.setdefault("tasks", 0)
        return st

    # ------------------------------------------------------------------ names

    def _npc_label(self, nid: str) -> str:
        npc = self._npc_defs().get(nid, {})
        return f"{npc.get('emoji', '')} {self.texts.t(f'story.npc.{nid}.name')}".strip()

    def _faction_name(self, fid: str) -> str:
        return self.texts.t(f"story.faction.{fid}.name")

    def _rank_name(self, index: int) -> str:
        ranks = self._ranks()
        return self.texts.t(f"story.rank.{ranks[max(0, min(index, len(ranks) - 1))]['id']}")

    def _quest_title(self, qid: str) -> str:
        return self.texts.t(f"story.quest.{qid}.title")

    def _origin_name(self, oid: str | None) -> str:
        return self.texts.t(f"story.origin.{oid}.name") if oid else ""

    def _title_name(self, tid: str) -> str:
        """A title's name: the Guardian's Pioneer titles (guardian.title.*) or the story ones (story.titles.*).

        [ES] Qué hace: el nombre de un título, sea de Pionero de un Guardián o de la historia (misiones y facciones).
        La llaman: la ficha del héroe, el diario y los avisos. Si cambia, afecta: cómo se leen los títulos.
        """
        key = f"guardian.title.{tid}"
        return self.texts.t(key) if self.texts.has(key) else self.texts.t(f"story.titles.{tid}")

    # ------------------------------------------------------------------ chains and quests

    def _chains(self, hero: Hero) -> list[tuple[str, list[str]]]:
        """(chain id, mission ids) of the hero: its origin chain (if chosen), then the current chapter of the campaign."""
        out: list[tuple[str, list[str]]] = []
        origin = self._origin_defs().get(hero.origin or "")
        if origin:
            out.append(("origin", [q for q in origin.get("chain", []) if q in self._quest_defs()]))
        done = set(self._st(hero)["done"])
        chapters = self._story_data().get("chapters") or {}
        last = None
        for cid, cdef in chapters.items():
            qids = [q for q in cdef.get("quests", []) if q in self._quest_defs()]
            last = (cid, qids)
            if not all(q in done for q in qids):
                out.append(last)
                return out
        if last:
            out.append(last)                         # every chapter done: the last one stays, complete
        return out

    def _current_quest(self, hero: Hero, qids: list[str]) -> str | None:
        done = self._st(hero)["done"]
        return next((q for q in qids if q not in done), None)

    def _active_quests(self, hero: Hero) -> list[str]:
        """The current mission of each chain whose level the hero has (at most one per chain)."""
        active = []
        for _, qids in self._chains(hero):
            qid = self._current_quest(hero, qids)
            if qid and int(self._quest_defs()[qid].get("level", 1)) <= hero.level:
                active.append(qid)
        return active

    def _step(self, hero: Hero, qid: str) -> dict[str, Any] | None:
        qdef = self._quest_defs().get(qid)
        if not qdef or qid in self._st(hero)["done"]:
            return None
        entry = self._st(hero)["q"].get(qid, {"s": 0, "n": 0})
        steps = qdef.get("steps") or []
        return steps[entry["s"]] if entry.get("s", 0) < len(steps) else None

    def _choice_of(self, hero: Hero, step: dict[str, Any]) -> str | None:
        """The option chosen in the decision a step depends on (its "by"), or that the step itself decided."""
        st = self._st(hero)
        if step.get("by"):
            return st["c"].get(step["by"])
        goal = step.get("goal") or {}
        return st["c"].get(goal.get("id")) if goal.get("kind") == "choice" else None

    def _goal(self, hero: Hero, step: dict[str, Any], qid: str | None = None) -> dict[str, Any]:
        """The step's goal with "@choice" resolved: the character chosen in the decision (or the mission's giver)."""
        goal = dict(step.get("goal") or {})
        if goal.get("npc") == "@choice":
            chosen = self._choice_of(hero, step)
            giver = self._quest_defs().get(qid or "", {}).get("giver")
            goal["npc"] = chosen if chosen in self._npc_defs() else giver
        return goal

    def _state_done(self, hero: Hero, goal: dict[str, Any]) -> bool:
        kind = goal.get("kind")
        if kind == "explored":
            x, y = goal.get("zone", [0, 0])
            return self._explored_pct(hero, int(x), int(y)) >= int(goal.get("pct", 100))
        if kind == "camp":
            return hero.camp is not None
        if kind == "level":
            return hero.level >= int(goal.get("n", 1))
        return False

    def _quest_progress(self, hero: Hero, qid: str, kind: str | None, data: dict[str, Any], announce: bool = True) -> list[str]:
        """Advance one mission with one game event (or only check its state goals when kind is None).

        [ES]
        Qué hace: con una cosa que pasó en el juego, avanza el paso actual de la misión si su objetivo la cuenta. Un
        evento avanza como mucho un paso; los objetivos de estado (zona explorada, campamento, nivel) se cumplen solos
        si ya está. Al cumplir un paso paga lo suyo (por la decisión que tomaste, si depende de una) y muestra lo que
        pasa; al cumplir el último, cierra la misión (_quest_complete). Con announce, avisa el objetivo del paso nuevo.
        La llaman: _story_event, _story_check, _talk y _choose.
        Si cambia, afecta: el avance de todas las misiones.
        """
        qdef = self._quest_defs().get(qid)
        st = self._st(hero)
        if not qdef or qid in st["done"]:
            return []
        entry = st["q"].setdefault(qid, {"s": 0, "n": 0})
        steps = qdef.get("steps") or []
        lines: list[str] = []
        moved = False
        while qid not in st["done"]:
            if entry["s"] >= len(steps):
                lines += self._quest_complete(hero, qid)
                break
            step = steps[entry["s"]]
            goal = self._goal(hero, step, qid)
            need = story_rules.target(goal)
            if goal.get("kind") in story_rules.STATE_GOALS:
                if not self._state_done(hero, goal):
                    break
            else:
                got = story_rules.amount(goal, kind, data) if kind else 0
                if got <= 0:
                    break
                kind = None                                 # one event moves one step at most
                entry["n"] = int(entry.get("n", 0)) + got
                if entry["n"] < need:
                    break
            lines += self._step_complete(hero, qid, step)
            entry["s"] += 1
            entry["n"] = 0
            moved = True
            if entry["s"] >= len(steps):
                lines += self._quest_complete(hero, qid)
                break
        if moved and announce and qid not in st["done"]:
            step = self._step(hero, qid)
            if step:
                lines.append(self.texts.t("story.step_next", title=self._quest_title(qid), goal=self._goal_line(hero, self._goal(hero, step, qid), 0)))
        return lines

    def _step_complete(self, hero: Hero, qid: str, step: dict[str, Any]) -> list[str]:
        """What happens when a step is done: its text (by decision, if any) and its reward or the decision's effects."""
        t = self.texts
        lines: list[str] = []
        option = self._choice_of(hero, step)
        base = f"story.quest.{qid}.{step['id']}_done"
        key = f"{base}_{option}" if option and t.has(f"{base}_{option}") else base
        if t.has(key):
            lines.append(t.t(key))
        goal = step.get("goal") or {}
        if goal.get("kind") == "choice":
            reward = (goal.get("effects") or {}).get(option) or {}
        else:
            reward = step.get("reward") or ((step.get("rewards") or {}).get(option) if option else None) or {}
        if reward:
            lines += self._apply_reward(hero, reward)
        return lines

    def _quest_xp(self, qdef: dict[str, Any]) -> int:
        """A mission's experience: story.xp_per_energy × its energy, scaled by its level like every kill (D-108)."""
        return self._zone_xp(self._story_cfg()["xp_per_energy"] * int(qdef.get("energy", 0)), int(qdef.get("level", 1)))

    def _chain_of(self, hero: Hero, qid: str) -> tuple[str, list[str]] | None:
        for chain, qids in self._chains(hero):
            if qid in qids:
                return chain, qids
        chapters = self._story_data().get("chapters") or {}
        for cid, cdef in chapters.items():
            if qid in cdef.get("quests", []):
                return cid, list(cdef["quests"])
        return None

    def _quest_complete(self, hero: Hero, qid: str) -> list[str]:
        """Close a mission: epilogue, rewards, journal; chapter end; announce (and check) the next one."""
        t = self.texts
        st = self._st(hero)
        qdef = self._quest_defs()[qid]
        st["q"].pop(qid, None)
        if qid not in st["done"]:
            st["done"].append(qid)
        lines = [t.t("story.quest_done", title=self._quest_title(qid))]
        if t.has(f"story.quest.{qid}.done"):
            lines.append(t.t(f"story.quest.{qid}.done"))
        lines += self._apply_reward(hero, qdef.get("reward") or {}, xp=self._quest_xp(qdef))
        self._journal(hero, "quest", q=qid)
        found = self._chain_of(hero, qid)
        if not found:
            return lines
        chain, qids = found
        chapters = self._story_data().get("chapters") or {}
        if chain in chapters and all(q in st["done"] for q in qids):
            self._journal(hero, "chapter", c=chain)
            lines.append(t.t("story.chapter_done", chapter=t.t(f"story.chapter.{chain}")))
            nxt = None
            following = list(chapters)[list(chapters).index(chain) + 1:]
            if following:
                nxt = next((q for q in chapters[following[0]].get("quests", []) if q in self._quest_defs()), None)
        else:
            nxt = self._current_quest(hero, qids)
        if nxt:
            level = int(self._quest_defs()[nxt].get("level", 1))
            if level <= hero.level:
                lines.append(t.t("story.next_quest", title=self._quest_title(nxt)))
                lines += self._quest_progress(hero, nxt, None, {})
            else:
                lines.append(t.t("story.next_locked", title=self._quest_title(nxt), level=level))
        return lines

    def _story_check(self, hero: Hero) -> list[str]:
        """Check the state goals of the current missions (a zone already explored, a camp, a level). [ES] Qué hace: cumple solos los pasos de estado que ya se cumplen. La llaman: 📖 Historia, elegir origen, hablar. Si cambia, afecta: los pasos de estado."""
        lines: list[str] = []
        for qid in self._active_quests(hero):
            lines += self._quest_progress(hero, qid, None, {})
        return lines

    # ------------------------------------------------------------------ rewards, reputation, titles and journal

    def _apply_reward(self, hero: Hero, reward: dict[str, Any], xp: int = 0) -> list[str]:
        """Pay a reward (experience, coins, items, reputation, title) and return its lines.

        [ES]
        Qué hace: paga un premio de la historia: experiencia (con el acelerador, como todo), monedas, cosas (entran
        aunque la mochila esté llena, D-90), reputación con las facciones (y lo que dé cada rango nuevo) y títulos.
        Devuelve una línea "🎁 ..." y las de subida de nivel, de rango y de título.
        La llaman: misiones, pasos, decisiones, encargos, premios de rango y el regalo del origen.
        Si cambia, afecta: todo lo que paga la historia.
        """
        t = self.texts
        parts: list[str] = []
        extra: list[str] = []
        if xp > 0:
            parts.append(t.t("story.reward_xp", xp=int(xp * self._xp_mult(hero))))
            extra += self._give_xp(hero, xp)
        coins = int(reward.get("coins", 0))
        if coins > 0:
            hero.gold += coins
            parts.append(f"+{self._money(coins)}")
        items = {i: int(n) for i, n in (reward.get("items") or {}).items() if i in self.content.items and int(n) > 0}
        for item_id, n in items.items():
            self._bag_add(hero, item_id, n)
        if items:
            parts.append(self._item_list(items))
        for fid, points in (reward.get("rep") or {}).items():
            gained, more = self._rep_gain(hero, fid, int(points))
            if gained:
                emoji = self._faction_defs().get(fid, {}).get("emoji", "")
                parts.append(t.t("story.rep_part", emoji=emoji, points=f"{gained:+d}"))
            extra += more
        if reward.get("title"):
            extra += self._grant_title(hero, reward["title"])
        return ([t.t("story.reward", items=" · ".join(parts))] if parts else []) + extra

    def _rank_of(self, hero: Hero, fid: str) -> int:
        return story_rules.rank_index(int(hero.factions.get(fid, 0)), self._ranks())

    def _rep_gain(self, hero: Hero, fid: str, points: int) -> tuple[int, list[str]]:
        """Change a faction's reputation; pay each new rank's reward once. Returns (points applied, lines).

        [ES]
        Qué hace: sube o baja la reputación con una facción (el 🏵️ Noble caído gana un 10 % más al subir). Si llega a un
        rango nuevo, lo avisa y paga lo que da ese rango (content/story.yaml rank_rewards) una sola vez para siempre,
        aunque después baje y vuelva a subir. Si baja de rango, lo avisa (no quita nada).
        La llaman: _apply_reward. Si cambia, afecta: los rangos y sus premios.
        """
        if fid not in self._faction_defs() or not points:
            return 0, []
        if points > 0:
            points = int(round(points * (1 + float(self._origin_trait(hero).get("rep_bonus", 0.0)))))
        t = self.texts
        st = self._st(hero)
        ranks = self._ranks()
        before = self._rank_of(hero, fid)
        hero.factions[fid] = int(hero.factions.get(fid, 0)) + points
        after = self._rank_of(hero, fid)
        lines: list[str] = []
        if after > before:
            best = int(st["ranks"].get(fid, story_rules.rank_position("desconocido", ranks)))
            rewards = (self._story_data().get("rank_rewards") or {}).get(fid) or {}
            for index in range(before + 1, after + 1):
                lines.append(t.t("story.rank_up", faction=self._faction_name(fid), rank=self._rank_name(index)))
                if index > best:
                    reward = rewards.get(ranks[index]["id"])
                    if reward:
                        lines += self._apply_reward(hero, {k: v for k, v in reward.items() if k != "rep"})
                    self._journal(hero, "rank", f=fid, r=ranks[index]["id"])
            st["ranks"][fid] = max(best, after)
        elif after < before:
            lines.append(t.t("story.rank_down", faction=self._faction_name(fid), rank=self._rank_name(after)))
        return points, lines

    def _grant_title(self, hero: Hero, tid: str) -> list[str]:
        """Give a title for ever (once) and write it in the journal."""
        if tid in hero.titles:
            return []
        hero.titles.append(tid)
        st = self._st(hero)
        if tid not in st["jt"]:
            st["jt"].append(tid)
            self._journal(hero, "title", t=tid)
        return [self.texts.t("story.title_won", title=self._title_name(tid))]

    def _journal(self, hero: Hero, key: str, **values: Any) -> None:
        """Write one deed in the hero's 📔 Diario (oldest ones go when it is full). [ES] Qué hace: anota un hecho en el diario. La llaman: la historia, el origen, la creación y los hitos (Guardián, campamento). Si cambia, afecta: lo que muestra el diario."""
        hero.journal.append({"t": self.clock.now(), "k": key, "v": values})
        cap = int(self._story_cfg()["journal_max"])
        if len(hero.journal) > cap:
            del hero.journal[:len(hero.journal) - cap]

    def _journal_text(self, entry: dict[str, Any]) -> str:
        t = self.texts
        key, v = entry.get("k", ""), entry.get("v") or {}
        if key == "origin":
            return t.t("story.journal.origin", origin=self._origin_name(v.get("o")))
        if key == "quest":
            return t.t("story.journal.quest", title=self._quest_title(v.get("q", "")))
        if key == "choice":
            return t.t("story.journal.choice", option=t.t(f"story.quest.{v.get('q')}.opt_{v.get('o')}"), title=self._quest_title(v.get("q", "")))
        if key == "chapter":
            return t.t("story.journal.chapter", chapter=t.t(f"story.chapter.{v.get('c')}"))
        if key == "guardian":
            edef = self.content.enemies.get(v.get("e", ""), {})
            return t.t("story.journal.guardian", name=t.t(edef["name_key"]) if edef else v.get("e", "?"))
        if key == "camp":
            return t.t("story.journal.camp", name=v.get("name", "?"))
        if key == "enemy_camp":                                       # D-112: finished it (f=1) or fought there (f=0)
            return t.t("story.journal.enemy_camp" if v.get("f") else "story.journal.enemy_camp_help", x=v.get("x"), y=v.get("y"))
        if key == "title":
            return t.t("story.journal.title", title=self._title_name(v.get("t", "")))
        if key == "rank":
            ranks = self._ranks()
            return t.t("story.journal.rank", faction=self._faction_name(v.get("f", "")),
                       rank=self._rank_name(story_rules.rank_position(v.get("r", ""), ranks)))
        return t.t("story.journal.awoke")

    def _journal_lines(self, hero: Hero, count: int) -> list[str]:
        lines = []
        for entry in hero.journal[-count:] if count > 0 else []:
            stamp = time.gmtime(float(entry.get("t", 0)))
            lines.append(self.texts.t("story.journal_line", date=f"{stamp.tm_mday:02d}/{stamp.tm_mon:02d}", text=self._journal_text(entry)))
        return lines

    # ------------------------------------------------------------------ the hook

    def _story_event(self, hero: Hero, kind: str, **data: Any) -> list[str]:
        """The one hook the game calls when something happens: advances missions, daily tasks and camp tasks.

        Kinds and data: explore (x, y, lejania of where the hero stands), gather (items), win (enemy, biome, level,
        hunt, boss), craft (recipe, profession, n), sell (n, coins), visit (x, y, lejania, lair), camp (name),
        feed (rations), build (n), infiltrate (x, y, level) and enemy_camp (x, y, level, destroyed) (D-112).

        [ES]
        Qué hace: el único gancho de la historia. El juego lo llama cuando pasa algo (explorar, recolectar, ganar una
        pelea, fabricar, vender, llegar a una zona, fundar un campamento, aportar a la despensa o a una obra) y aquí
        avanzan las misiones en curso, los encargos del día y los del campamento; también anota en el diario el primer
        Guardián, el título de Pionero y el campamento fundado. Devuelve las líneas para mostrar (una vez: el lote las
        junta en su resumen; una pelea, en su final).
        La llaman: engine/service/game.py en _explore_step, _gather_step, _end_combat, _make, _sell, _camp_sell,
        _sell_gear, _arrive, _found_camp, _camp_feed, _give_to_work y _give_to_study; y D-112: _infiltrate (🕵️ te
        infiltraste) y _ecamp_destroyed (⛺ destruiste un campamento enemigo: queda en el 📔 Diario).
        Si cambia, afecta: todo el avance de la historia (tests/test_story.py).
        """
        lines: list[str] = []
        for qid in self._active_quests(hero):
            lines += self._quest_progress(hero, qid, kind, data)
        lines += self._daily_event(hero, kind, data)
        lines += self._camp_event(hero, kind, data)
        self._story_marks(hero, kind, data)
        return lines

    def _story_marks(self, hero: Hero, kind: str, data: dict[str, Any]) -> None:
        """Journal milestones that other systems already announce: first Guardian win, Pioneer title, camp founded, enemy camp
        destroyed (D-112)."""
        st = self._st(hero)
        if kind == "win" and data.get("boss"):
            enemy = data.get("enemy", "")
            if (hero.guardians.get(enemy) or {}).get("wins") == 1 and enemy not in st["jg"]:
                st["jg"].append(enemy)
                self._journal(hero, "guardian", e=enemy)
            for tid in hero.titles:
                if tid not in st["jt"]:
                    st["jt"].append(tid)
                    self._journal(hero, "title", t=tid)
        elif kind == "camp":
            self._journal(hero, "camp", name=data.get("name", "?"))
        elif kind == "enemy_camp" and data.get("destroyed"):          # D-112: you brought an enemy camp down
            self._journal(hero, "enemy_camp", x=data.get("x"), y=data.get("y"), f=1)

    # ------------------------------------------------------------------ daily tasks (the Claro board)

    def _story_day(self) -> int:
        return int(self.clock.now() // self._day_seconds())

    def _daily_ids(self) -> list[str]:
        """Today's tasks: one per faction, the same for everybody (world seed + day)."""
        pool = self._story_data().get("daily") or {}
        givers = {nid: n.get("faction") for nid, n in self._npc_defs().items()}
        return story_rules.daily_pick(pool, list(self._faction_defs()), givers, self.world_seed, self._story_day())

    def _daily(self, hero: Hero) -> dict[str, Any]:
        """The hero's progress on today's tasks; a new day starts it again."""
        st = self._st(hero)
        day = self._story_day()
        record = st.get("daily") or {}
        if record.get("day") != day:
            record = {"day": day, "p": {}, "done": []}
            st["daily"] = record
        return record

    def _task_xp(self, hero: Hero, energy: int) -> int:
        """A task's experience: story.task_xp_per_energy × its energy, scaled by the hero's level (D-108)."""
        return self._zone_xp(self._story_cfg()["task_xp_per_energy"] * int(energy), hero.level)

    def _task_coins(self, hero: Hero, base: int) -> int:
        return int(round(int(base) * (1 + self._story_cfg()["task_coins_per_level"] * (hero.level - 1))))

    def _task_reward(self, hero: Hero, tdef: dict[str, Any]) -> tuple[dict[str, Any], int]:
        faction = self._npc_defs().get(tdef.get("giver"), {}).get("faction")
        reward = {"coins": self._task_coins(hero, tdef.get("coins", 0)), "rep": {faction: int(tdef.get("rep", 0))} if faction else {}}
        return reward, self._task_xp(hero, tdef.get("energy", 0))

    def _daily_event(self, hero: Hero, kind: str, data: dict[str, Any]) -> list[str]:
        """Count an event for today's tasks; a task done pays once, right away."""
        if kind not in TASK_EVENTS:
            return []
        pool = self._story_data().get("daily") or {}
        record = self._daily(hero)
        lines: list[str] = []
        for tid in self._daily_ids():
            if tid in record["done"]:
                continue
            tdef = pool[tid]
            got = story_rules.amount(tdef.get("goal") or {}, kind, data)
            if got <= 0:
                continue
            record["p"][tid] = int(record["p"].get(tid, 0)) + got
            if record["p"][tid] >= story_rules.target(tdef.get("goal") or {}):
                record["done"].append(tid)
                self._st(hero)["tasks"] = int(self._st(hero).get("tasks", 0)) + 1
                lines.append(self.texts.t("story.task_done", npc=self._npc_label(tdef.get("giver", "")), task=self.texts.t(f"story.daily.{tid}")))
                reward, xp = self._task_reward(hero, tdef)
                lines += self._apply_reward(hero, reward, xp=xp)
        return lines

    # ------------------------------------------------------------------ camp tasks (weekly, all members together)

    def _story_week(self) -> int:
        return int(self.clock.now() // (7 * self._day_seconds()))

    def _camp_task_ids(self, key: str, camp: dict[str, Any]) -> list[str]:
        pool = self._story_data().get("camp_tasks") or {}
        return story_rules.weekly_pick(pool, self.world_seed, self._story_week(), key, int(camp.get("level", 1)),
                                       int(self._story_cfg()["camp_tasks"]))

    def _camp_tasks(self, key: str) -> dict[str, Any]:
        record = self.store.get("camp_tasks", key) or {}
        if record.get("week") != self._story_week():
            record = {"week": self._story_week(), "p": {}, "by": {}, "paid": []}
        return record

    def _camp_event(self, hero: Hero, kind: str, data: dict[str, Any]) -> list[str]:
        """Count what a member did for the camp's weekly tasks; when one is reached, pay every member who helped.

        [ES]
        Qué hace: suma lo que hizo un miembro (ganar peleas, explorar, recolectar, aportar a la despensa o a las obras)
        a los encargos de la semana de su campamento. Al llegar a la meta, cada miembro que aportó al menos 1 cobra el
        premio (aunque no esté conectado) y los demás reciben el aviso. Como mucho una lectura y una escritura.
        La llama: _story_event. Si cambia, afecta: las "misiones con los miembros del campamento" que pidió el dueño.
        """
        if not hero.camp or kind not in CAMP_EVENTS:
            return []
        pool = self._story_data().get("camp_tasks") or {}
        camp = self.store.get("camp", hero.camp)
        if not camp or hero.id not in camp.get("members", []):
            return []
        ids = [tid for tid in self._camp_task_ids(hero.camp, camp) if story_rules.amount(pool[tid]["goal"], kind, data) > 0]
        if not ids:
            return []
        record = self._camp_tasks(hero.camp)
        lines: list[str] = []
        changed = False
        for tid in ids:
            if tid in record["paid"]:
                continue
            got = story_rules.amount(pool[tid]["goal"], kind, data)
            record["p"][tid] = int(record["p"].get(tid, 0)) + got
            by = record["by"].setdefault(tid, {})
            by[hero.id] = int(by.get(hero.id, 0)) + got
            changed = True
            if record["p"][tid] >= story_rules.target(pool[tid]["goal"]):
                record["paid"].append(tid)
                lines += self._camp_task_paid(hero, camp, tid, by)
        if changed:
            self.store.put("camp_tasks", hero.camp, record)
        return lines

    def _camp_task_paid(self, hero: Hero, camp: dict[str, Any], tid: str, by: dict[str, int]) -> list[str]:
        t = self.texts
        reward = (self._story_data().get("camp_tasks") or {})[tid].get("reward") or {}
        reward = {"xp": int(reward.get("xp", 0)), "gold": int(reward.get("gold", 0))}
        name = t.t(f"story.camp_task.{tid}")
        news = View(kind="camp_news", title=t.t("story.camp_task_push_title"),
                    body=[t.t("story.camp_task_push", hero=hero.name, task=name, camp=camp.get("name", "?"), xp=reward["xp"],
                              gold=self._money(reward["gold"]))])
        for member, given in by.items():
            if given <= 0:
                continue
            self._raid_reward(member, reward, hero)       # pays online or not; the actor in memory
            if member != hero.id:
                self._push(member, news)
        return [t.t("story.camp_task_done", task=name, xp=reward["xp"], gold=self._money(reward["gold"]))]

    # ------------------------------------------------------------------ origin

    def _origin_trait(self, hero: Hero) -> dict[str, Any]:
        return (self._origin_defs().get(hero.origin or "") or {}).get("trait") or {}

    def _origin_prof_bonus(self, hero: Hero, pid: str) -> float:
        """Extra profession experience from the hero's origin (a share: 0.15 = +15 %). [ES] Qué hace: el bono de experiencia de oficio del origen. La llama: _prof_gain. Si cambia, afecta: el ritmo de los oficios de quien tiene ese origen."""
        trait = self._origin_trait(hero)
        bonus = float((trait.get("prof_xp") or {}).get(pid, 0.0))
        branch = (self._prof_catalog().get(pid) or {}).get("branch")
        return bonus + float((trait.get("prof_xp_branch") or {}).get(branch, 0.0))

    def _shop_price(self, hero: Hero, item_id: str) -> int:
        """What the Claro merchant charges this hero for an item (the 🕳️ Huérfano pays less). [ES] Qué hace: el precio del mercader para este héroe. La llaman: _shop_view y _buy. Si cambia, afecta: cuántas monedas salen del juego al comprar."""
        price = int(self.content.items[item_id]["price"])
        discount = float(self._origin_trait(hero).get("shop_discount", 0.0))
        return max(1, int(round(price * (1 - discount))))

    def _origin_offer(self, hero: Hero) -> View | None:
        """Heroes without an origin get the choice once (new heroes at creation, old ones the first time they look)."""
        st = self._st(hero)
        if hero.origin or st.get("offered"):
            return None
        st["offered"] = True
        return self._origin_view(hero, notice=self.texts.t("story.origin_new"))

    def _origin_view(self, hero: Hero, page: int = 0, notice: str | None = None) -> View:
        """🎭 Choose your origin: a page of origins (3 + ▶️, 4 buttons at most); never blocking (the menu works).

        [ES]
        Qué hace: la pantalla para elegir de dónde viene el héroe: 3 orígenes por página con su frase, ▶️ Más para los
        siguientes; al tocar uno se ve su detalle y se confirma. No bloquea: con el menú de abajo se sigue jugando y se
        elige después en 📖 Historia.
        La llaman: la creación del héroe (después de confirmar la clase), _origin_offer y el botón 🎭 Elegir origen.
        Si cambia, afecta: tests/test_story.py y el tope de 4 botones.
        """
        if hero.origin:
            return self._story_view(hero, notice=notice)
        t = self.texts
        ids = list(self._origin_defs())
        per = max(1, int(self._story_cfg()["origin_page"]))
        pages = max(1, (len(ids) + per - 1) // per)
        page = page % pages
        body = [t.t("story.origin_ask"), t.t("story.origin_page", n=page + 1, total=pages), ""]
        actions = []
        for oid in ids[page * per:(page + 1) * per]:
            body.append(t.t("story.origin_list_line", name=self._origin_name(oid), intro=t.t(f"story.origin.{oid}.intro")))
            actions.append(Action(id=f"orig:{oid}", label=self._origin_name(oid)))
        body += ["", t.t("story.origin_later")]
        if pages > 1:
            actions.append(Action(id=f"origin:{(page + 1) % pages}", label=t.t("story.button_more")))
        return View(kind="origin", title=t.t("story.origin_title"), body=body, actions=actions[:4], notice=notice)

    def _origin_detail(self, hero: Hero, oid: str) -> View:
        t = self.texts
        odef = self._origin_defs().get(oid)
        if not odef or hero.origin:
            return self._origin_view(hero)
        first = next(iter(odef.get("chain") or []), None)
        body = [self._origin_name(oid), t.t(f"story.origin.{oid}.intro"), "",
                t.t("story.origin_detail_trait", trait=t.t(f"story.origin.{oid}.trait")),
                t.t("story.origin_detail_gift", gift=t.t(f"story.origin.{oid}.gift"))]
        if first:
            body.append(t.t("story.origin_detail_story", title=self._quest_title(first)))
        body += ["", t.t("story.origin_forever")]
        page = list(self._origin_defs()).index(oid) // max(1, int(self._story_cfg()["origin_page"]))
        actions = [Action(id=f"origpick:{oid}", label=t.t("story.button_choose")), Action(id=f"origin:{page}", label=t.t("menu.back"))]
        return View(kind="origin_detail", title=t.t("story.origin_title"), body=body, actions=actions)

    def _pick_origin(self, hero: Hero, oid: str) -> View:
        """Choose the origin for ever: its gift, a journal entry and its first mission (if the hero has its level)."""
        t = self.texts
        if hero.origin:
            return self._story_view(hero, notice=t.t("story.origin_already", origin=self._origin_name(hero.origin)))
        odef = self._origin_defs().get(oid)
        if not odef:
            return self._origin_view(hero)
        hero.origin = oid
        self._st(hero)["offered"] = True
        lines = [t.t("story.origin_chosen", origin=self._origin_name(oid))]
        lines += self._apply_reward(hero, odef.get("gift") or {})
        self._journal(hero, "origin", o=oid)
        lines += self._story_check(hero)
        return self._story_view(hero, notice=self._join(lines))

    # ------------------------------------------------------------------ routing

    def _story_action(self, hero: Hero, action_id: str) -> View:
        """Route the story buttons (STORY_ACTIONS). [ES] Qué hace: reparte los botones de la historia. La llama: _idle_action (también ocupado: mirar la historia no interrumpe nada). Si cambia, afecta: todos los botones de la historia."""
        if action_id == "story":
            return self._story_view(hero)
        if action_id == "squests":
            return self._quests_view(hero)
        if action_id == "board":
            return self._board_view(hero)
        if action_id == "npcs" or action_id.startswith("npcs:"):
            page = action_id[5:]
            return self._npcs_view(hero, int(page) if page.isdigit() else 0)
        if action_id.startswith("npc:"):
            return self._npc_view(hero, action_id[4:])
        if action_id.startswith("talk:"):
            return self._talk(hero, action_id[5:])
        if action_id.startswith("ch:"):
            parts = action_id.split(":")
            return self._choose(hero, parts[1], parts[2]) if len(parts) == 3 else self._quests_view(hero)
        if action_id == "factions":
            return self._factions_view(hero)
        if action_id == "journal":
            return self._journal_view(hero)
        if action_id == "jshow":
            return self._show_journal(hero)
        if action_id == "origin" or action_id.startswith("origin:"):
            page = action_id[7:]
            return self._origin_view(hero, int(page) if page.isdigit() else 0)
        if action_id.startswith("orig:"):
            return self._origin_detail(hero, action_id[5:])
        if action_id.startswith("origpick:"):
            return self._pick_origin(hero, action_id[9:])
        if action_id == "bio":
            return self._bio_view(hero)
        if action_id.startswith("gesture:"):
            return self._gesture(hero, action_id[8:])
        return self._story_view(hero)

    # ------------------------------------------------------------------ 📖 Historia and 🎯 Misiones

    def _goal_line(self, hero: Hero, goal: dict[str, Any], progress: int) -> str:
        """What a goal asks, in one line, with its progress ("🪓 Recolecta 🌿 Hierba curativa (2/4)")."""
        t = self.texts
        kind = goal.get("kind")
        n = story_rules.target(goal) if kind not in ("explore", "gather", "win", "craft", "sell", "feed", "build") else max(1, int(goal.get("n", 1)))
        p = min(n, int(progress))
        if kind == "talk":
            return t.t("story.goal.talk", npc=self._npc_label(goal.get("npc", "")))
        if kind == "deliver":
            items = " · ".join(t.t("story.goal.deliver_item", item=self._item_label(i), have=min(int(k), hero.backpack.get(i, 0)), need=int(k))
                               for i, k in (goal.get("items") or {}).items() if i in self.content.items)
            return t.t("story.goal.deliver", npc=self._npc_label(goal.get("npc", "")), items=items)
        if kind == "explore":
            key = "explore_claro" if goal.get("claro") else ("explore_outside" if goal.get("outside") else "explore")
            return t.t(f"story.goal.{key}", n=n, p=p)
        if kind == "explored":
            x, y = goal.get("zone", [0, 0])
            return t.t("story.goal.explored", zone=self._zone_name(self._zone(int(x), int(y))), pct=int(goal.get("pct", 100)),
                       now=self._explored_pct(hero, int(x), int(y)))
        if kind == "gather":
            if goal.get("item") in self.content.items:
                return t.t("story.goal.gather_item", item=self._item_label(goal["item"]), n=n, p=p)
            return t.t("story.goal.gather", n=n, p=p)
        if kind == "win":
            if goal.get("hunt"):
                return t.t("story.goal.hunt", n=n, p=p)
            if goal.get("biomes"):
                names = t.t("story.goal.biomes_join").join(self._biome_name(b) for b in goal["biomes"])
                return t.t("story.goal.win_biomes", n=n, p=p, biomes=names)
            return t.t("story.goal.win", n=n, p=p)
        if kind == "guardian":
            edef = self.content.enemies.get(goal.get("enemy", ""), {})
            return t.t("story.goal.guardian", name=t.t(edef["name_key"]) if edef else self._guardian_name())
        if kind == "visit":
            if goal.get("lair"):
                return t.t("story.goal.visit_lair")
            if "zone" in goal:
                x, y = goal["zone"]
                return t.t("story.goal.visit_zone", name=self._zone_name(self._zone(int(x), int(y))), x=x, y=y)
            return t.t("story.goal.visit_far", n=int(goal.get("lejania", 1)))
        if kind in ("craft", "sell", "feed", "build"):
            return t.t(f"story.goal.{kind}", n=n, p=p)
        if kind == "level":
            return t.t("story.goal.level", n=int(goal.get("n", 1)))
        if kind == "camp":
            return t.t("story.goal.camp")
        return t.t("story.goal.choice")

    def _biome_name(self, biome: str) -> str:
        bdef = self.content.biomes.get(biome)
        return f"{bdef['emoji']} {self.texts.t(bdef['name_key'])}" if bdef else biome

    def _quest_goal_line(self, hero: Hero, qid: str) -> str:
        step = self._step(hero, qid)
        if not step:
            return ""
        entry = self._st(hero)["q"].get(qid, {"n": 0})
        return self._goal_line(hero, self._goal(hero, step, qid), int(entry.get("n", 0)))

    def _story_view(self, hero: Hero, notice: str | None = None) -> View:
        """📖 Historia: origin and chapter progress, what to do now, today's tasks, factions; 4 buttons.

        [ES]
        Qué hace: la pantalla principal de la historia (6.º botón del menú de abajo y /historia): tu origen y su avance,
        el capítulo de la campaña, qué hacer ahora en cada misión, los encargos de hoy, tu rango con cada facción y los
        atajos (/diario, /bio, /saludar, /brindar). Botones: 🎯 Misiones, 🧑 Personajes, ⚜️ Facciones y 📔 Diario (sin
        origen, 🎭 Elegir origen en su lugar). Los héroes viejos sin origen ven primero la elección, una sola vez.
        La llaman: el botón 📖 Historia, /historia y las vueltas de sus pantallas.
        Si cambia, afecta: tests/test_story.py y el tope de 4 botones.
        """
        offer = self._origin_offer(hero)
        if offer:
            return offer
        t = self.texts
        notice = self._join(self._story_check(hero) + ([notice] if notice else []))
        st = self._st(hero)
        body = [t.t("story.intro"), ""]
        for chain, qids in self._chains(hero):
            done = sum(1 for q in qids if q in st["done"])
            if chain == "origin":
                key = "story.origin_line_done" if done >= len(qids) else "story.origin_line"
                body.append(t.t(key, origin=self._origin_name(hero.origin), done=min(done + 1, len(qids)), total=len(qids)))
            else:
                key = "story.chapter_done_line" if done >= len(qids) else "story.chapter_line"
                body.append(t.t(key, chapter=t.t(f"story.chapter.{chain}"), done=min(done + 1, len(qids)), total=len(qids)))
        if not hero.origin:
            body.insert(2, t.t("story.origin_none"))
        body += ["", t.t("story.now_title")]
        now = []
        for _, qids in self._chains(hero):
            qid = self._current_quest(hero, qids)
            if not qid:
                continue
            level = int(self._quest_defs()[qid].get("level", 1))
            if level > hero.level:
                now.append(t.t("story.now_locked", title=self._quest_title(qid), level=level))
            else:
                now.append(t.t("story.now_line", title=self._quest_title(qid), goal=self._quest_goal_line(hero, qid)))
        body += now or [t.t("story.now_none")]
        daily = self._daily(hero)
        ids = self._daily_ids()
        left = (self._story_day() + 1) * self._day_seconds() - self.clock.now()
        body += ["", t.t("story.tasks_line", done=sum(1 for i in ids if i in daily["done"]), total=len(ids), time=self._fmt_duration(left))]
        body.append(t.t("story.factions_line", list=self._factions_short(hero)))
        body += ["", t.t("story.links")]
        actions = [Action(id="squests", label=t.t("story.button_quests")), Action(id="npcs", label=t.t("story.button_npcs")),
                   Action(id="factions", label=t.t("story.button_factions"))]
        actions.append(Action(id="journal", label=t.t("story.button_journal")) if hero.origin
                       else Action(id="origin", label=t.t("story.button_origin")))
        return View(kind="story", title=t.t("story.title"), body=body, actions=actions, notice=notice)

    def _factions_short(self, hero: Hero) -> str:
        t = self.texts
        return " · ".join(t.t("story.faction_short", emoji=fdef.get("emoji", ""), rank=self._rank_name(self._rank_of(hero, fid)),
                              points=int(hero.factions.get(fid, 0)))
                          for fid, fdef in self._faction_defs().items())

    def _quests_view(self, hero: Hero, notice: str | None = None) -> View:
        """🎯 Misiones: each chain's current mission with its text and goal; a pending decision shows its options.

        [ES]
        Qué hace: muestra la misión en curso de tu origen y del capítulo: el texto del paso (lo que pasa), qué hacer y
        cuánto llevas. Si un paso es una decisión, sus opciones son los botones (hasta 3, más ↩️ Volver); si no,
        📜 Encargos y ↩️ Volver.
        La llaman: 🎯 Misiones de 📖 Historia y las decisiones. Si cambia, afecta: tests/test_story.py.
        """
        t = self.texts
        st = self._st(hero)
        notice = self._join(self._story_check(hero) + ([notice] if notice else []))
        body: list[str] = []
        choice: tuple[str, dict[str, Any]] | None = None
        if not hero.origin:
            body += [t.t("story.chain_origin_none"), ""]
        for chain, qids in self._chains(hero):
            done = sum(1 for q in qids if q in st["done"])
            qid = self._current_quest(hero, qids)
            if chain == "origin":
                head = t.t("story.chain_origin_done" if not qid else "story.chain_origin", origin=self._origin_name(hero.origin),
                           done=done, total=len(qids))
            else:
                head = t.t("story.chain_chapter_done" if not qid else "story.chain_chapter", chapter=t.t(f"story.chapter.{chain}"),
                           done=done, total=len(qids))
            body.append(head)
            if qid:
                body += self._quest_block(hero, qid)
                step = self._step(hero, qid)
                if step and (step.get("goal") or {}).get("kind") == "choice" and choice is None \
                        and int(self._quest_defs()[qid].get("level", 1)) <= hero.level:
                    choice = (qid, step)
            body.append("")
        actions: list[Action] = []
        if choice:
            qid, step = choice
            body.append(t.t("story.choice_hint"))
            for option in (step["goal"].get("options") or [])[:3]:
                actions.append(Action(id=f"ch:{qid}:{option}", label=t.t(f"story.quest.{qid}.opt_{option}")))
        else:
            actions.append(Action(id="board", label=t.t("story.button_tasks")))
        actions.append(Action(id="story", label=t.t("menu.back")))
        return View(kind="story_quests", title=t.t("story.quests_title"), body=body, actions=actions[:4], notice=notice)

    def _quest_block(self, hero: Hero, qid: str) -> list[str]:
        """A mission's current step: header, its text (by decision, if any) and its goal; or its level lock."""
        t = self.texts
        qdef = self._quest_defs()[qid]
        level = int(qdef.get("level", 1))
        if level > hero.level:
            return [t.t("story.quest_locked", title=self._quest_title(qid), level=level)]
        step = self._step(hero, qid)
        if not step:
            return []
        entry = self._st(hero)["q"].get(qid, {"s": 0})
        lines = [t.t("story.quest_head", title=self._quest_title(qid), step=int(entry.get("s", 0)) + 1, steps=len(qdef["steps"]))]
        lines.append(self._step_text(hero, qid, step))
        if (step.get("goal") or {}).get("kind") != "choice":
            lines.append(t.t("story.goal_now", goal=self._quest_goal_line(hero, qid)))
        return lines

    def _step_text(self, hero: Hero, qid: str, step: dict[str, Any]) -> str:
        t = self.texts
        option = self._choice_of(hero, step) if step.get("by") else None
        key = f"story.quest.{qid}.{step['id']}"
        return t.t(f"{key}_{option}") if option and t.has(f"{key}_{option}") else t.t(key)

    def _choose(self, hero: Hero, qid: str, option: str) -> View:
        """Take a decision: remembered for ever (journal), its effects paid, and the mission goes on.

        [ES]
        Qué hace: guarda lo que elegiste en una decisión (para siempre: cambia saludos, quién te ayuda después y premios),
        paga lo que cambia esa opción (reputación, cosas, monedas), lo anota en el diario y sigue la misión.
        La llaman: los botones de opción de 🎯 Misiones ("ch:<misión>:<opción>").
        Si cambia, afecta: las decisiones de la campaña (tests/test_story.py).
        """
        step = self._step(hero, qid) if qid in self._active_quests(hero) else None
        goal = (step or {}).get("goal") or {}
        if goal.get("kind") != "choice" or option not in (goal.get("options") or []):
            return self._quests_view(hero)
        st = self._st(hero)
        st["c"][goal.get("id", f"{qid}.{step['id']}")] = option
        self._journal(hero, "choice", q=qid, s=step["id"], o=option)
        lines = self._quest_progress(hero, qid, "choice", {"opt": option}, announce=False)
        lines += self._next_step_lines(hero, qid)
        return self._quests_view(hero, notice=self._join(lines))

    def _next_step_lines(self, hero: Hero, qid: str) -> list[str]:
        """After talking or deciding: the new step's text and goal, so the story reads as a scene."""
        step = self._step(hero, qid)
        if not step or (step.get("goal") or {}).get("kind") == "choice":
            return [self._step_text(hero, qid, step)] if step else []
        return [self._step_text(hero, qid, step), self.texts.t("story.goal_now", goal=self._quest_goal_line(hero, qid))]

    # ------------------------------------------------------------------ 🧑 Personajes

    def _npc_pending(self, hero: Hero, nid: str) -> list[tuple[str, dict[str, Any]]]:
        """(mission, goal) of the current steps that ask to talk to (or bring something to) this character."""
        out = []
        for qid in self._active_quests(hero):
            step = self._step(hero, qid)
            if not step:
                continue
            goal = self._goal(hero, step, qid)
            if goal.get("kind") in ("talk", "deliver") and goal.get("npc") == nid:
                out.append((qid, goal))
        return out

    def _in_claro(self, hero: Hero) -> bool:
        return (hero.x, hero.y) == (0, 0) and (hero.activity or {}).get("kind") != "travel"

    def _npcs_view(self, hero: Hero, page: int = 0, notice: str | None = None) -> View:
        """🧑 Personajes: the Claro's characters, 3 per page (❗ = has something for you); 4 buttons at most."""
        t = self.texts
        ids = list(self._npc_defs())
        per = max(1, int(self._story_cfg()["npc_page"]))
        pages = max(1, (len(ids) + per - 1) // per)
        page = page % pages
        body = [t.t("story.npcs_intro")]
        if not self._in_claro(hero):
            body.append(t.t("story.npcs_away"))
        body.append("")
        actions = []
        for nid in ids[page * per:(page + 1) * per]:
            npc = self._npc_defs()[nid]
            mark = t.t("story.npc_mark") if self._npc_pending(hero, nid) else ""
            body.append(t.t("story.npc_line", emoji=npc.get("emoji", ""), name=t.t(f"story.npc.{nid}.name"), role=t.t(f"story.npc.{nid}.role"),
                            faction=self._faction_defs().get(npc.get("faction"), {}).get("emoji", ""), mark=mark))
            actions.append(Action(id=f"npc:{nid}", label=self._npc_label(nid) + (t.t("story.npc_button_mark") if mark else "")))
        if pages > 1:
            body.append(t.t("story.page", n=page + 1, total=pages))
            if page + 1 < pages:
                actions.append(Action(id=f"npcs:{page + 1}", label=t.t("story.button_more")))
            else:
                actions.append(Action(id=f"npcs:{page - 1}", label=t.t("story.button_prev")))
        if len(actions) < 4:
            actions.append(Action(id="story", label=t.t("menu.back")))
        return View(kind="npcs", title=t.t("story.npcs_title"), body=body, actions=actions[:4], notice=notice)

    def _npc_line(self, hero: Hero, nid: str) -> str:
        """What a character says now: the first of its lines whose conditions hold (story.yaml npcs.<id>.lines)."""
        npc = self._npc_defs().get(nid, {})
        st = self._st(hero)
        facts = {"done": set(st["done"]), "active": set(self._active_quests(hero)), "choices": st["c"],
                 "rank": self._rank_of(hero, npc.get("faction", "")), "origin": hero.origin, "met": nid in st["met"]}
        for line in npc.get("lines") or []:
            if story_rules.matches(line.get("when"), facts, self._ranks()):
                return self.texts.t(f"story.npc.{nid}.lines.{line['key']}")
        return self.texts.t(f"story.npc.{nid}.lines.default")

    def _npc_view(self, hero: Hero, nid: str, notice: str | None = None) -> View:
        """One character: role, faction and your rank, what they say now, what they want from you; [💬 Hablar] [↩️ Volver].

        [ES]
        Qué hace: la ficha de un personaje del Claro: quién es, su facción y tu rango con ella, lo que te dice ahora (cambia
        con tus misiones, decisiones y reputación) y lo que una misión te pide con él. 💬 Hablar (o 🤲 Entregar) aparece
        si tiene algo para ti y estás en el Claro. Verlo en el Claro cuenta como conocerlo.
        La llaman: los botones de 🧑 Personajes y _talk. Si cambia, afecta: tests/test_story.py.
        """
        t = self.texts
        npc = self._npc_defs().get(nid)
        if not npc:
            return self._npcs_view(hero)
        fid = npc.get("faction", "")
        body = [t.t("story.npc_head", emoji=npc.get("emoji", ""), name=t.t(f"story.npc.{nid}.name"), role=t.t(f"story.npc.{nid}.role")),
                t.t("story.npc_faction", faction=self._faction_name(fid), rank=self._rank_name(self._rank_of(hero, fid)),
                    points=int(hero.factions.get(fid, 0))),
                "", t.t("story.npc_says", line=self._npc_line(hero, nid))]
        pending = self._npc_pending(hero, nid)
        for qid, goal in pending:
            body.append(t.t("story.npc_pending", goal=self._goal_line(hero, goal, 0)))
        actions: list[Action] = []
        if self._in_claro(hero):
            st = self._st(hero)
            if nid not in st["met"]:
                st["met"].append(nid)
            if pending:
                deliver = pending[0][1].get("kind") == "deliver"
                actions.append(Action(id=f"talk:{nid}", label=t.t("story.button_deliver" if deliver else "story.button_talk")))
        else:
            body.append(t.t("story.npc_away", name=t.t(f"story.npc.{nid}.name")))
        page = list(self._npc_defs()).index(nid) // max(1, int(self._story_cfg()["npc_page"]))
        actions.append(Action(id=f"npcs:{page}", label=t.t("menu.back")))
        return View(kind="npc", title=t.t("story.npcs_title"), body=body, actions=actions, notice=notice)

    def _talk(self, hero: Hero, nid: str) -> View:
        """💬 Hablar / 🤲 Entregar: advance the first mission step that asks for this character (in the Claro only).

        [ES]
        Qué hace: hablas con el personaje y avanza el primer paso que lo pide; si el paso es llevarle cosas, se las das
        (todas o ninguna: si falta algo, avisa qué y no toma nada). Muestra lo que pasa y el paso siguiente. Hay que estar
        en el Claro (no de viaje).
        La llama: el botón 💬 Hablar / 🤲 Entregar de la ficha del personaje. Si cambia, afecta: tests/test_story.py.
        """
        t = self.texts
        name = t.t(f"story.npc.{nid}.name")
        if nid not in self._npc_defs():
            return self._npcs_view(hero)
        if not self._in_claro(hero):
            return self._npc_view(hero, nid, notice=t.t("story.not_in_claro", name=name))
        lines: list[str] = []
        for qid, goal in self._npc_pending(hero, nid):
            if goal.get("kind") == "deliver":
                need = {i: int(n) for i, n in (goal.get("items") or {}).items() if i in self.content.items}
                missing = {i: n - hero.backpack.get(i, 0) for i, n in need.items() if hero.backpack.get(i, 0) < n}
                if missing:
                    lines.append(t.t("story.deliver_missing", name=name, items=self._item_list(missing)))
                    continue
                for item_id, n in need.items():
                    hero.backpack[item_id] -= n
                    if hero.backpack[item_id] <= 0:
                        del hero.backpack[item_id]
                lines.append(t.t("story.delivered", name=name, items=self._item_list(need)))
            lines += self._quest_progress(hero, qid, "talk", {"npc": nid}, announce=False)
            lines += self._next_step_lines(hero, qid)
            break
        if not lines:
            lines.append(t.t("story.nothing_to_say", name=name))
        return self._npc_view(hero, nid, notice=self._join(lines))

    # ------------------------------------------------------------------ 📜 Tablón, ⚜️ Facciones

    def _board_view(self, hero: Hero, notice: str | None = None) -> View:
        """📜 Tablón: today's three tasks (one per faction) and, with a camp, this week's camp tasks.

        [ES]
        Qué hace: el tablón de encargos del Claro (también desde 🎯 Misiones → 📜 Encargos y /encargos): los 3 encargos de
        hoy, quién los da, cuánto llevas y qué pagan; cuándo cambian; y, si tienes campamento, sus encargos de la semana
        con lo que llevan entre todos y lo que aportaste tú. Botones: 🧑 Personajes, 📖 Historia y ↩️ Volver (al Claro si
        estás ahí) — 3 como mucho.
        La llaman: el botón 📜 Tablón del Claro y 📜 Encargos. Si cambia, afecta: tests/test_story.py.
        """
        t = self.texts
        pool = self._story_data().get("daily") or {}
        daily = self._daily(hero)
        body = [t.t("story.board_intro"), ""]
        for tid in self._daily_ids():
            tdef = pool[tid]
            goal = tdef.get("goal") or {}
            reward, xp = self._task_reward(hero, tdef)
            emoji = self._faction_defs().get(self._npc_defs().get(tdef.get("giver"), {}).get("faction"), {}).get("emoji", "")
            prize = " · ".join([t.t("story.reward_xp", xp=int(xp * self._xp_mult(hero))), f"+{self._money(reward['coins'])}",
                                t.t("story.rep_part", emoji=emoji, points=f"+{int(tdef.get('rep', 0))}")])
            done = tid in daily["done"]
            body.append(t.t("story.board_line", mark=t.t("story.mark_done" if done else "story.mark_todo"), npc=self._npc_label(tdef.get("giver", "")),
                            task=t.t(f"story.daily.{tid}"), goal=self._goal_line(hero, goal, story_rules.target(goal) if done else daily["p"].get(tid, 0)),
                            reward=prize))
        left = (self._story_day() + 1) * self._day_seconds() - self.clock.now()
        body += [t.t("story.board_reset", time=self._fmt_duration(left)), ""]
        body += self._camp_task_lines(hero)
        actions = [Action(id="npcs", label=t.t("story.button_npcs"))]
        if self._in_claro(hero) and not hero.activity:
            actions += [Action(id="story", label=t.t("story.button_story")), Action(id="claro", label=t.t("menu.back"))]
        else:
            actions.append(Action(id="squests", label=t.t("menu.back")))
        return View(kind="board", title=t.t("story.board_title"), body=body, actions=actions, notice=notice)

    def _camp_task_lines(self, hero: Hero) -> list[str]:
        t = self.texts
        camp = self.store.get("camp", hero.camp) if hero.camp else None
        if not camp or hero.id not in camp.get("members", []):
            return [t.t("story.board_no_camp")]
        pool = self._story_data().get("camp_tasks") or {}
        record = self._camp_tasks(hero.camp)
        lines = [t.t("story.board_camp_title", camp=camp.get("name", "?"))]
        for tid in self._camp_task_ids(hero.camp, camp):
            reward = pool[tid].get("reward") or {}
            lines.append(t.t("story.board_camp_line", mark=t.t("story.mark_done" if tid in record["paid"] else "story.mark_todo"),
                             task=t.t(f"story.camp_task.{tid}"), p=min(int(record["p"].get(tid, 0)), story_rules.target(pool[tid]["goal"])),
                             n=story_rules.target(pool[tid]["goal"]), mine=int(record["by"].get(tid, {}).get(hero.id, 0)),
                             xp=int(reward.get("xp", 0)), gold=self._money(int(reward.get("gold", 0)))))
        left = (self._story_week() + 1) * 7 * self._day_seconds() - self.clock.now()
        lines.append(t.t("story.board_camp_reset", time=self._fmt_duration(left)))
        return lines

    def _factions_view(self, hero: Hero) -> View:
        """⚜️ Facciones: each faction, your rank and points, and what the next rank gives. [ES] Qué hace: muestra las tres facciones con tu rango, tus puntos y lo que da el rango siguiente. La llama: ⚜️ Facciones de 📖 Historia. Si cambia, afecta: solo lo que se muestra."""
        t = self.texts
        ranks = self._ranks()
        body = [t.t("story.factions_intro"), ""]
        for fid, fdef in self._faction_defs().items():
            index = self._rank_of(hero, fid)
            body.append(t.t("story.faction_head", emoji=fdef.get("emoji", ""), name=self._faction_name(fid), rank=self._rank_name(index),
                            points=int(hero.factions.get(fid, 0))))
            body.append(t.t(f"story.faction.{fid}.desc"))
            if index + 1 < len(ranks):
                nxt = ranks[index + 1]
                reward = ((self._story_data().get("rank_rewards") or {}).get(fid) or {}).get(nxt["id"]) or {}
                parts = []
                if reward.get("title"):
                    parts.append(t.t("story.faction_reward_title", title=self._title_name(reward["title"])))
                if reward.get("items"):
                    parts.append(self._item_list({i: int(n) for i, n in reward["items"].items() if i in self.content.items}))
                if reward.get("coins"):
                    parts.append(self._money(int(reward["coins"])))
                body.append(t.t("story.faction_next", rank=self._rank_name(index + 1), need=int(nxt["from"]),
                                reward=" · ".join(parts) or t.t("story.faction_reward_none")))
            else:
                body.append(t.t("story.faction_top"))
            body.append("")
        return View(kind="factions", title=t.t("story.factions_title"), body=body, actions=[Action(id="story", label=t.t("menu.back"))])

    # ------------------------------------------------------------------ 📔 Diario, tarjeta y /bio

    def _card_lines(self, hero: Hero, entries: int) -> list[str]:
        """The hero's card: name with emblem, class, level, origin, bio, titles, faction ranks, tasks and last deeds."""
        t = self.texts
        group = self.content.classes.get(hero.class_id, {}).get("group", hero.class_id)
        lines = [t.t("story.card_head", name=self._banner(hero) + self._emblem_name(hero), cls=t.t(f"class_group.{group}.name"), level=hero.level)]
        if hero.origin:
            lines.append(t.t("story.card_origin", origin=self._origin_name(hero.origin)))
        if hero.bio:
            lines.append(t.t("story.card_bio", bio=hero.bio))
        if hero.titles:
            lines.append(t.t("story.card_titles", titles=", ".join(self._title_name(x) for x in hero.titles)))
        known = [t.t("story.faction_short", emoji=fdef.get("emoji", ""), rank=self._rank_name(self._rank_of(hero, fid)), points=int(hero.factions.get(fid, 0)))
                 for fid, fdef in self._faction_defs().items() if hero.factions.get(fid)]
        if known:
            lines.append(t.t("story.card_factions", list=" · ".join(known)))
        if self._st(hero).get("tasks"):
            lines.append(t.t("story.card_tasks", n=int(self._st(hero)["tasks"])))
        journal = self._journal_lines(hero, entries)
        return lines + ([""] + journal if journal else [])

    def _journal_view(self, hero: Hero, notice: str | None = None) -> View:
        """📔 Diario: your card and your last deeds; [📣 Mostrar en la zona] [↩️ Volver]. [ES] Qué hace: tu diario (crónica de lo que hiciste) con tu tarjeta. La llaman: 📔 Diario de 📖 Historia y /diario. Si cambia, afecta: tests/test_story.py."""
        t = self.texts
        body = self._card_lines(hero, 0)
        journal = self._journal_lines(hero, int(self._story_cfg()["journal_shown"]))
        body += [""] + (journal or [t.t("story.journal_empty")]) + ["", t.t("story.journal_hint", name=hero.name)]
        actions = [Action(id="jshow", label=t.t("story.button_show")), Action(id="story", label=t.t("menu.back"))]
        return View(kind="journal", title=t.t("story.journal_title", name=hero.name), body=body, actions=actions, notice=notice)

    def _find_hero(self, name: str) -> Hero | None:
        key = self._name_key(name)
        for _, data in self.store.items("hero"):
            if self._name_key(data.get("name", "")) == key:
                return Hero.from_dict(data)
        return None

    def _card_view(self, hero: Hero, name: str) -> View:
        """/diario <name>: another hero's card (what everybody can see). [ES] Qué hace: la tarjeta de otro héroe: emblema, clase, nivel, origen, biografía, títulos, rangos y sus últimos hechos. La llama: /diario <nombre>. Si cambia, afecta: lo que los demás ven de cada uno."""
        t = self.texts
        other = hero if self._name_key(name) == self._name_key(hero.name) else self._find_hero(name)
        if other is None:
            return self._story_view(hero, notice=t.t("story.card_not_found", name=story_rules.clean_text(name, 20)))
        return View(kind="card", title=t.t("story.card_title", name=other.name), body=self._card_lines(other, int(self._story_cfg()["card_shown"])),
                    actions=[Action(id="story", label=t.t("menu.back"))])

    def _bio_view(self, hero: Hero, notice: str | None = None) -> View:
        """📝 Tu biografía: what you wrote with /bio and how to change it. [ES] Qué hace: muestra tu biografía y cómo escribirla. La llaman: /bio sin texto y después de guardarla. Si cambia, afecta: solo lo que se muestra."""
        t = self.texts
        body = [t.t("story.bio_now", bio=hero.bio) if hero.bio else t.t("story.bio_none"), "",
                t.t("story.bio_how", n=int(self._story_cfg()["bio_max"]))]
        return View(kind="bio", title=t.t("story.bio_title"), body=body, actions=[Action(id="hero", label=t.t("menu.back"))], notice=notice)

    def _set_bio(self, hero: Hero, text: str) -> View:
        t = self.texts
        if text.strip().lower() in self.texts.list("story.bio_clear_words"):
            hero.bio = ""
            return self._bio_view(hero, notice=t.t("story.bio_cleared"))
        hero.bio = story_rules.clean_text(text, int(self._story_cfg()["bio_max"]))
        return self._bio_view(hero, notice=t.t("story.bio_saved" if hero.bio else "story.bio_cleared"))

    # ------------------------------------------------------------------ roleplay: emblem, gestures, typed commands

    def _emblem(self, hero: Hero) -> tuple[str, str, int] | None:
        """(emoji, profession, rank) of the hero's best profession once it reaches story.emblem_min_rank, else None."""
        catalog = self._prof_catalog()
        best: tuple[int, int, str] | None = None
        for pid, xp in (hero.professions or {}).items():
            if pid in catalog and xp > 0:
                rank = self._prof_rank(hero, pid)
                if best is None or (rank, xp) > best[:2]:
                    best = (rank, xp, pid)
        if not best or best[0] < int(self._story_cfg()["emblem_min_rank"]):
            return None
        return catalog[best[2]].get("emoji", ""), best[2], best[0]

    def _emblem_name(self, hero: Hero) -> str:
        """The hero's name with its role emblem: "🩺 Lyra" (best profession from story.emblem_min_rank), else the name.

        [ES] Qué hace: el nombre con el emblema de su mejor oficio (desde el rango story.emblem_min_rank). La llaman: la
        lista 👥 de 📍 Zona, la tarjeta del diario y los gestos. Si cambia, afecta: cómo se ve tu nombre ante los demás.
        """
        emblem = self._emblem(hero)
        return self.texts.t("story.emblem_name", emoji=emblem[0], name=hero.name) if emblem else hero.name

    def _story_hero_lines(self, hero: Hero) -> list[str]:
        """Hero sheet lines: origin (and the /historia link), role emblem and biography."""
        t = self.texts
        lines = [t.t("story.hero_origin", origin=self._origin_name(hero.origin)) if hero.origin else t.t("story.hero_origin_none")]
        emblem = self._emblem(hero)
        if emblem:
            lines.append(t.t("story.hero_emblem", emoji=emblem[0], trade=self.texts.t(self._prof_catalog()[emblem[1]].get("name_key", "")),
                             rank=emblem[2], title=self._rank_title(emblem[2])))
        if hero.bio:
            lines.append(t.t("story.hero_bio", bio=hero.bio))
        return lines

    def _gesture_wait(self, hero: Hero) -> float:
        last = float(self._st(hero).get("g_at", 0.0))
        return max(0.0, last + float(self._story_cfg()["gesture_seconds"]) * self.time_scale - self.clock.now())

    def _gesture(self, hero: Hero, kind: str, arg: str = "") -> View:
        """/saludar [name] and /brindar [text]: one narrated line pushed to the players present in your zone (D-96).

        [ES]
        Qué hace: un gesto de rol que les llega a los jugadores presentes en tu zona (los de 👥 en 📍 Zona) como una línea
        narrada ("👋 Lyra saluda a Bram."). /saludar sin nombre saluda a todos; /brindar puede llevar tu brindis (corto).
        Uno por minuto como mucho (story.gesture_seconds); si no hay nadie, avisa y no gasta la espera.
        La llaman: /saludar, /brindar (text()) y los botones "gesture:". Si cambia, afecta: tests/test_story.py.
        """
        t = self.texts
        if kind not in ("saludar", "brindar"):
            return self._main_view(hero)
        wait = self._gesture_wait(hero)
        if wait > 0:
            return self._main_view(hero, notice=t.t("story.gesture_wait", time=self._fmt_duration(wait)))
        present = self._zone_players(hero.x, hero.y, exclude=hero.id)
        if not present:
            return self._main_view(hero, notice=t.t("story.gesture_alone"))
        zone = self._zone_name(self._zone(hero.x, hero.y))
        me = self._banner(hero) + self._emblem_name(hero)
        if kind == "saludar":
            target = None
            if arg.strip():
                target = next((p for p in present if self._name_key(p.get("plain", "")) == self._name_key(arg)), None)
                if target is None:
                    return self._main_view(hero, notice=t.t("story.gesture_not_here", name=story_rules.clean_text(arg, 20)))
            line = t.t("story.gesture_saludar_to", name=me, target=target["name"]) if target else t.t("story.gesture_saludar", name=me, zone=zone)
        else:
            toast = story_rules.clean_text(arg, int(self._story_cfg()["toast_max"]))
            line = t.t("story.gesture_brindar_text", name=me, text=toast) if toast else t.t("story.gesture_brindar", name=me)
        view = View(kind="gesture", title=t.t("story.gesture_title", zone=zone), body=[line])
        for player in present:
            self._push(player["id"], view)
        self._st(hero)["g_at"] = self.clock.now()
        return self._main_view(hero, notice=t.t("story.gesture_done", line=line, n=len(present)))

    def _show_journal(self, hero: Hero) -> View:
        """📣 Mostrar: push your card to the players present in your zone (same wait as the gestures)."""
        t = self.texts
        wait = self._gesture_wait(hero)
        if wait > 0:
            return self._journal_view(hero, notice=t.t("story.gesture_wait", time=self._fmt_duration(wait)))
        present = self._zone_players(hero.x, hero.y, exclude=hero.id)
        if not present:
            return self._journal_view(hero, notice=t.t("story.gesture_alone"))
        view = View(kind="card", title=t.t("story.card_push_title", name=hero.name), body=self._card_lines(hero, int(self._story_cfg()["card_shown"])))
        for player in present:
            self._push(player["id"], view)
        self._st(hero)["g_at"] = self.clock.now()
        return self._journal_view(hero, notice=t.t("story.shown", n=len(present), zone=self._zone_name(self._zone(hero.x, hero.y))))

    def _typed_command(self, hero: Hero, text: str) -> View | None:
        """Typed commands that carry text: /bio <texto>, /saludar <nombre>, /brindar <texto>, /diario <nombre|mostrar>.

        Returns None for anything else (plain shortcuts like /stats go through act()).

        [ES]
        Qué hace: los atajos escritos que llevan algo después: /bio con tu biografía (o "borrar"), /saludar con un nombre,
        /brindar con tu brindis, /diario con el nombre de otro héroe (su tarjeta) o "mostrar". Sin texto, /bio, /diario,
        /saludar y /brindar son atajos comunes (COMMANDS en game.py).
        La llama: GameService.text() cuando el texto empieza con "/". Si cambia, afecta: lo que entienden los tres clientes.
        """
        word, _, rest = text.strip().partition(" ")
        word = word.split("@")[0].lower()
        rest = rest.strip()
        if not rest:
            return None
        if word == "/bio":
            return self._set_bio(hero, rest)
        if word in ("/saludar", "/brindar"):
            return self._gesture(hero, word[1:], rest)
        if word == "/diario":
            return self._show_journal(hero) if rest.lower() in self.texts.list("story.journal_show_words") else self._card_view(hero, rest)
        return None
