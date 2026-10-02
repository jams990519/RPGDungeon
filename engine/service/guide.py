"""Guided path of the game service (D-190 confirmed, D-193 provisional): a mixin of GameService.

The guided path replaces the old hint tutorial: right after creating the hero, the game sends the player to do ONE action
at a time (move, explore, gather, hunt, the map, back to the camp, the camp, its trainer, the hero; later, finding a spot
and founding an own camp), each with a short, detailed explanation in the TowerWars format the owner asked for, and a
small reward. On top of that, one-time tips arrive as the player meets new things (a first fight, low energy, a cave, a
node, an enemy camp...), never all at once: at most one per screen. Steps and tips are data (content/guide.yaml, texts in
content/locales/es_guia.yaml); progress lives in Hero.guide. The engine tells the guide what happened through ONE hook,
_guide_event(hero, kind, **data), and button steps are checked before every idle action's screen (_guide_before).

[ES]
Para qué sirve: el 🧭 camino guiado. Te manda a hacer una sola cosa a la vez, te explica lo justo con el botón exacto y te
da un premio chico por paso; y te da los avisos de una sola vez ("tutoriales a medida que desbloqueas cosas", D-190).
Muestra la línea "🧭 Ahora:" en las pantallas principales, la pantalla /guia y la bienvenida al crear el héroe. Es parte
de GameService (una "mezcla", como StoryMixin), en su propio archivo para no agrandar game.py.
Documento de diseño: diseno/03-personaje/camino-guiado.md; D-190 (pedido del dueño) y D-193 (cómo se aplicó)
Módulo: capa de servicios (M10 Misiones: el camino es una cadena de pasos; los avisos son de M19 Mensajería)
Depende de: content/guide.yaml (pasos y avisos), content/locales/es_guia.yaml (textos), content/balance.yaml (bloques guide,
    tutorial (solo para leer el tutorial viejo), travel, energy, explore, gather, hunt, exploration y camps), engine.hero,
    engine.messaging y las ayudas de GameService (_give_xp, _money, _xp_mult, _claro_zones, _territory, _own_camp_here,
    _camp_requirements, _route_seconds, _fmt_duration, _seconds, _energy_period, _bag_cap, _bag_full, _prof_rank,
    _node_found, _dng_kind, _ecamp_standing, _zone, _join)
Lo usan: engine/service/game.py (GameService hereda de esta clase; llama a _guide_new_request al empezar _settle, a
    _guide_event en _settle (explorar y recolectar),
    _arrive, _end_combat (y _auto_combat lee state["guide"]) y _found_camp; a _guide_before en act() y view(); a _guide_new
    y _guide_view al crear el héroe; a _guide_hint desde _tutorial_hint (las pantallas de zona, explorar, campamento y
    héroe) y a _guide_tip_lines desde _combat_view; a _guide_view con la acción "guide" y /guia)
Eventos que publica: ninguno
Eventos que escucha: ninguno (el motor llama al gancho _guide_event)
Datos de los que es dueño: Hero.guide {"v", "done" [pasos hechos], "tips" [avisos mostrados], "away" [zonas pisadas fuera del
    Claro después del camino básico], "intro" [el paso de fundar que ya se explicó al salir], "fresh" [el paso que el aviso de
    esta pantalla acaba de presentar; se borra solo]}. Hero.tutorial y balance.yaml tutorial solo se leen (E-133).
Reglas que nunca se rompen:
    1. Un solo paso a la vez: el actual es el primero de content/guide.yaml que no está hecho.
    2. Cada paso paga una sola vez; un paso saltado (héroes de antes, E-133, o "skip") no paga.
    3. Cada aviso sale una sola vez por héroe, y como mucho uno por pantalla (nunca todos de golpe, D-190).
    4. El camino nunca bloquea nada: es solo texto y premios chicos; el menú y todos los botones siguen andando.
    5. No hay tutorial de fundar campamento mientras estás en el Claro (D-190): empieza al salir, después del camino básico.
    6. Lo guardado solo crece: nunca se borra un paso hecho ni un aviso visto (D-64).
Si cambias esto, revisa:
    - Datos: content/guide.yaml (ids estables, C-18; el orden de los pasos), content/locales/es_guia.yaml (cada paso necesita
      name, task e intro; cada aviso, name y text) y balance.yaml guide (premio, veterano, movimientos, umbrales)
    - Servicio: engine/service/game.py (dónde se llama _guide_event: si un camino deja de llamarlo, su paso no avanza más;
      los ids de botón "map", "claro", "trainer" y "hero": si cambian, el paso que los pide no avanza)
    - Pantallas: las que llaman a _tutorial_hint (zona, 🧭 Explorar, campamento, héroe, campamento enemigo) muestran la línea
      "🧭 Ahora:" y un aviso; _combat_view muestra el aviso de la primera pelea
    - Mapa de impacto: cascada C-29
    - Pruebas: tests/test_camino_guiado.py (y tests/test_service.py, la creación)
"""

from __future__ import annotations

from typing import Any

from engine.hero import Hero
from engine.messaging import Action, View

# Version of the Hero.guide record. [ES] Versión del registro Hero.guide: un héroe sin "v" es de antes de la 0.29 (E-133).
GUIDE_VERSION = 1


class GuideMixin:
    """Guided path part of GameService (needs its content, store, texts and helpers).

    [ES]
    Qué es: la parte del camino guiado del servicio del juego, en su propio archivo.
    Quién la usa: GameService (hereda de aquí).
    Si cambia, afecta: la bienvenida, la línea "🧭 Ahora:", los avisos de una sola vez y /guia.
    """

    # ------------------------------------------------------------------ data

    def _guide_cfg(self) -> dict[str, Any]:
        return self.content.balance.get("guide", {})

    def _guide_steps(self) -> list[tuple[str, dict[str, Any]]]:
        """(id, definition) of every live step, in order (content/guide.yaml "steps"; retired ones left out)."""
        steps = (self.content.guide or {}).get("steps") or {}
        return [(sid, s) for sid, s in steps.items() if isinstance(s, dict) and not s.get("retired")]

    def _guide_tips(self) -> list[tuple[str, dict[str, Any]]]:
        """(id, definition) of every live one-time tip, in priority order (content/guide.yaml "tips")."""
        tips = (self.content.guide or {}).get("tips") or {}
        return [(tid, d) for tid, d in tips.items() if isinstance(d, dict) and not d.get("retired")]

    def _guide_basic(self) -> list[str]:
        """Step ids of the basic path: up to and including the step marked basic_end (all of them if none is)."""
        out: list[str] = []
        for sid, step in self._guide_steps():
            out.append(sid)
            if step.get("basic_end"):
                break
        return out

    def _guide_name(self, sid: str) -> str:
        return self.texts.t(f"guide.step.{sid}.name")

    # ------------------------------------------------------------------ the hero's record

    @staticmethod
    def _guide_new() -> dict[str, Any]:
        """The guide record of a hero created now (D-193): nothing done, nothing seen."""
        return {"v": GUIDE_VERSION, "done": [], "tips": [], "away": 0}

    def _guide(self, hero: Hero) -> dict[str, Any]:
        """The hero's guide record with every key present; heroes saved before 0.29 are brought up to date once (E-133).

        [ES]
        Qué hace: da el registro del camino guiado del héroe con todas sus claves. Un héroe de antes de la 0.29 (sin "v") se
        pone al día una sola vez (_guide_migrate). Y quien tiene el tutorial viejo terminado (Hero.tutorial al final de
        balance.yaml tutorial.steps) tiene el camino básico hecho, sin premio.
        La llaman: todo este archivo. Si cambia, afecta: el avance guardado de todos los héroes.
        """
        guide = hero.guide if isinstance(hero.guide, dict) else {}
        hero.guide = guide
        for key in ("done", "tips"):
            if not isinstance(guide.get(key), list):
                guide[key] = []
        if not isinstance(guide.get("away"), int):
            guide["away"] = 0
        if not guide.get("v"):
            self._guide_migrate(hero, guide)
            guide["v"] = GUIDE_VERSION
        if self._guide_old_tutorial_done(hero):
            for sid in self._guide_basic():
                if sid not in guide["done"]:
                    guide["done"].append(sid)
        return guide

    def _guide_old_tutorial_done(self, hero: Hero) -> bool:
        steps = self.content.balance.get("tutorial", {}).get("steps") or []
        return bool(steps) and hero.tutorial >= len(steps)

    def _guide_migrate(self, hero: Hero, guide: dict[str, Any]) -> None:
        """Bring a hero saved before the guided path up to date, without rewards (E-133, provisional answer).

        [ES]
        Qué hace: pone al día a un héroe de antes de la 0.29. Si terminó el tutorial viejo o tiene balance.yaml
        guide.veteran_level o más, el camino básico queda hecho (sin premio); si no, quedan hechos los pasos que ya hizo a
        la vista (está fuera del Claro o pisó otra zona → moverte; exploró fuera del Claro → explorar; pasó el paso
        "gather" del tutorial viejo → recolectar; ganó alguna pelea → cazar). Con campamento, los pasos de fundar también.
        Los avisos de lo que ya conoce quedan vistos (primera pelea, nivel, oficio, nodo, opciones, origen, oleada); los
        demás le llegan cuando los encuentre.
        La llama: _guide (una sola vez por héroe). Si cambia, afecta: qué ven los jugadores de antes al llegar la 0.29.
        """
        done = guide["done"]
        ids = [sid for sid, _ in self._guide_steps()]
        old = self.content.balance.get("tutorial", {}).get("steps") or []
        veteran = self._guide_old_tutorial_done(hero) or hero.level >= int(self._guide_cfg().get("veteran_level", 5))
        if veteran:
            evidence = {sid: True for sid in self._guide_basic()}
        else:
            evidence = {
                "move": (hero.x, hero.y) != (0, 0) or len(hero.known) > 1,
                "explore": any(key != "0:0" and pct > 0 for key, pct in hero.exploration.items()),
                "gather": "gather" in old and hero.tutorial > old.index("gather"),
                "hunt": hero.kills > 0,
            }
        if hero.camp:
            evidence.update({"found_spot": True, "found": True})
        for sid in ids:
            if evidence.get(sid) and sid not in done:
                done.append(sid)
        camp = self.store.get("camp", hero.camp) if hero.camp else None
        raids = (camp or {}).get("raids")
        met = {
            "fight": hero.kills > 0,
            "level_up": hero.level >= 2,
            "rank_up": any(self._prof_rank(hero, pid) >= 2 for pid in hero.professions),
            "node": bool(self._node_found(hero)),
            "options": bool(hero.options),
            "origin": bool(hero.origin),
            "raid": isinstance(raids, dict) and sum(int(n) for n in raids.values()) > 0,
        }
        for tid, seen in met.items():
            if seen and tid not in guide["tips"]:
                guide["tips"].append(tid)

    def _guide_current(self, hero: Hero) -> tuple[int, str, dict[str, Any]] | None:
        """(number, id, definition) of the one step the hero has to do now, or None when the whole path is done."""
        done = set(self._guide(hero)["done"])
        for number, (sid, step) in enumerate(self._guide_steps(), start=1):
            if sid not in done:
                return number, sid, step
        return None

    def _guide_basic_done(self, hero: Hero) -> bool:
        done = set(self._guide(hero)["done"])
        return all(sid in done for sid in self._guide_basic())

    # ------------------------------------------------------------------ conditions

    def _guide_in_claro(self, hero: Hero) -> bool:
        return [hero.x, hero.y] in self._claro_zones()

    def _guide_where(self, hero: Hero, where: str | None) -> bool:
        """away: outside the Claro; home: in the Claro or in your own camp; spot: a good place to found a camp (D-190)."""
        if not where:
            return True
        if where == "away":
            return not self._guide_in_claro(hero)
        if where == "home":
            return self._guide_in_claro(hero) or self._own_camp_here(hero) is not None
        if where == "spot":
            return self._guide(hero)["away"] >= int(self._guide_cfg().get("found_moves", 2)) and self._guide_spot(hero)
        return False

    def _guide_spot(self, hero: Hero) -> bool:
        """True if founding could work here one day: far enough, no land and no camp near, and no camp of your own.

        [ES] Qué hace: dice si la zona sirve para fundar (lo que no se arregla trabajando ahí): Lejanía camps.min_lejania o
        más, fuera de todo territorio, sin otro campamento a camps.min_distance o menos y sin campamento propio. Explorar al
        100 %, conocer las vecinas y llevar los materiales se hace después (la pantalla de fundar los muestra). Es la misma
        cuenta que _camp_requirements (req_far, req_alone, req_one): si una cambia, cambia la otra.
        """
        cfg = self.content.balance["camps"]
        zone = self._zone(hero.x, hero.y)
        if hero.camp is not None or zone.lejania < cfg["min_lejania"] or self._territory(zone.x, zone.y):
            return False
        reach = int(cfg["min_distance"])
        return not any(self.store.get("camp", f"{zone.x + dx}:{zone.y + dy}")
                       for dx in range(-reach, reach + 1) for dy in range(-reach, reach + 1))

    def _guide_cond(self, hero: Hero, cond: str | None) -> bool:
        if cond == "home":
            return self._guide_where(hero, "home")
        if cond == "has_camp":
            return hero.camp is not None
        return False

    def _guide_matches(self, hero: Hero, step: dict[str, Any], event: str | None = None, action: str | None = None,
                       **data: Any) -> bool:
        done = step.get("done") or {}
        if event is not None and done.get("event") != event:
            return False
        if action is not None and done.get("action") != action:
            return False
        if done.get("hunt") and not data.get("hunt"):
            return False
        return self._guide_where(hero, done.get("where"))

    # ------------------------------------------------------------------ advancing

    def _guide_event(self, hero: Hero, kind: str, **data: Any) -> list[str]:
        """Something happened in the game: complete the current step if it waits for it; returns the lines to show.

        [ES]
        Qué hace: el único gancho del camino guiado. El motor avisa qué pasó: "arrive" (llegar a una zona, cada tramo),
        "explore" y "gather" (una vuelta del lote), "fight" (el final de una pelea; hunt=True si fue de 🏹 Cazar) y "camp"
        (fundaste un campamento). Si el paso actual espera eso, se completa (premio, lo que aprendiste y el paso que sigue).
        Al llegar fuera del Claro después del camino básico, también cuenta los movimientos para fundar (D-190) y, en el
        primero, explica que vas a buscar un buen lugar.
        La llaman: _settle, _arrive, _end_combat y _found_camp (engine/service/game.py).
        Si cambia, afecta: cuándo avanza cada paso (tests/test_camino_guiado.py).
        """
        guide = self._guide(hero)
        lines: list[str] = []
        current = self._guide_current(hero)
        if kind == "arrive" and self._guide_basic_done(hero) and not self._guide_in_claro(hero):
            guide["away"] += 1
            if current and current[2].get("hidden_home") and guide.get("intro") != current[1]:
                lines += self._guide_present(hero)              # D-190: the founding guide starts once you are away
        if current and self._guide_matches(hero, current[2], event=kind, **data):
            lines += self._guide_complete(hero, *current)
        return lines

    def _guide_action(self, hero: Hero, action_id: str) -> list[str]:
        """A button was pressed: complete the current step if it asks for that button ("map", "claro", "trainer", "hero")."""
        current = self._guide_current(hero)
        if current and self._guide_matches(hero, current[2], action=action_id):
            return self._guide_complete(hero, *current)
        return []

    def _guide_settle_state(self, hero: Hero) -> list[str]:
        """Skip (no reward) or complete the current step when its condition already holds, with no event (state/skip)."""
        guide = self._guide(hero)
        for _ in range(len(self._guide_steps())):
            current = self._guide_current(hero)
            if not current:
                break
            number, sid, step = current
            if self._guide_cond(hero, step.get("skip")):
                guide["done"].append(sid)                       # skipped: no reward, no text
                continue
            if self._guide_cond(hero, (step.get("done") or {}).get("state")):
                return self._guide_complete(hero, number, sid, step)
            break
        return []

    def _guide_complete(self, hero: Hero, number: int, sid: str, step: dict[str, Any]) -> list[str]:
        """Mark a step done: its reward (once), what you learned, the closing line, then the next step (or the next done)."""
        t = self.texts
        guide = self._guide(hero)
        if sid in guide["done"]:
            return []
        guide["done"].append(sid)
        values = self._guide_values(hero)
        lines = [t.t("guide.step_done", n=number, total=len(self._guide_steps()), name=self._guide_name(sid))]
        if step.get("reward"):
            cfg = self._guide_cfg()
            gold, xp = int(cfg.get("reward_gold", 0)), int(cfg.get("reward_xp", 0))
            hero.gold += gold
            lines.append(t.t("guide.reward", gold=self._money(gold), xp=int(xp * self._xp_mult(hero))))
            lines += self._give_xp(hero, xp)
        if t.has(f"guide.step.{sid}.learn"):
            lines += t.t(f"guide.step.{sid}.learn", **values).split("\n")
        if step.get("basic_end"):
            lines += [""] + t.t("guide.path_done").split("\n")
        chained = self._guide_settle_state(hero)                 # the next step may already hold (back home already)
        return lines + ([""] + chained if chained else self._guide_present(hero))

    # ------------------------------------------------------------------ texts

    def _guide_values(self, hero: Hero) -> dict[str, Any]:
        """The numbers the guide texts name, read from balance.yaml (so a text never says an old number)."""
        b = self.content.balance
        t = self.texts
        per_move = int(b["energy"].get("per_move", 0))
        low, high = b["exploration"]["per_step"]
        return {
            "name": hero.name,
            "move": t.t("guide.move_free") if per_move <= 0 else t.t("guide.move_cost", n=per_move),
            "first_time": self._fmt_duration(self._seconds(b["travel"]["first_minutes"])),
            "max_time": self._fmt_duration(self._seconds(b["travel"]["max_minutes"])),
            "explore_time": self._fmt_duration(self._seconds(b["explore"]["minutes"])),
            "gather_time": self._fmt_duration(self._seconds(b["gather"]["minutes"])),
            "per_explore": b["energy"]["per_explore"], "per_gather": b["energy"]["per_gather"],
            "pct_low": low, "pct_high": high,
            "batch": ", ".join(str(n) for n in b["energy"]["batch"]),
            "cap": self._bag_cap(hero), "hunt": b["hunt"]["energy"],
            "energy_now": hero.energy, "max_energy": b["energy"]["max"],
            "period": self._fmt_duration(self._energy_period()),
            "min_lejania": b["camps"]["min_lejania"],
        }

    def _guide_needs(self, hero: Hero) -> list[str]:
        """The founding requirements here, ✅ / ▫️ (the same list as the camp screen, _camp_requirements)."""
        return [("✅ " if ok else "▫️ ") + text for text, ok in self._camp_requirements(hero)]

    def _guide_now(self, hero: Hero, sid: str, step: dict[str, Any]) -> list[str]:
        """The "🧭 Ahora:" line of a step (plus what founding still needs, for the step that asks it)."""
        t = self.texts
        lines = [t.t("guide.now", task=t.t(f"guide.step.{sid}.task", **self._guide_values(hero)))]
        if step.get("needs") == "camp":
            missing = [text for text, ok in self._camp_requirements(hero) if not ok]
            lines.append(t.t("guide.missing", items=" · ".join(missing)) if missing else t.t("guide.ready"))
        return lines

    def _guide_hidden(self, hero: Hero, step: dict[str, Any]) -> bool:
        """A step with hidden_home says nothing while the hero is in the Claro (D-190: founding starts once away)."""
        return bool(step.get("hidden_home")) and self._guide_in_claro(hero)

    def _guide_present(self, hero: Hero) -> list[str]:
        """The current step as it starts: its number and name, its explanation and the "🧭 Ahora:" line."""
        current = self._guide_current(hero)
        if not current or self._guide_hidden(hero, current[2]):
            return []
        number, sid, step = current
        guide = self._guide(hero)
        guide["fresh"] = sid                                    # this screen's notice already says "🧭 Ahora:" (_guide_hint)
        if step.get("hidden_home"):
            guide["intro"] = sid                                # said once when away (_guide_event does not repeat it)
        t = self.texts
        values = self._guide_values(hero)
        values["needs"] = "\n".join(self._guide_needs(hero))
        return (["", t.t("guide.next_title", n=number, total=len(self._guide_steps()), name=self._guide_name(sid))]
                + t.t(f"guide.step.{sid}.intro", **values).split("\n") + self._guide_now(hero, sid, step))

    # ------------------------------------------------------------------ tips (one time, one per screen)

    def _guide_tip_ready(self, hero: Hero, when: str | None) -> bool:
        """Is this the moment of a tip? Each condition is something the hero meets for the first time."""
        cfg = self._guide_cfg()
        if when == "in_combat":
            return self.store.get("combat", hero.id) is not None
        if when == "downed":
            return hero.downed
        if when == "level_up":
            return hero.points > 0 and hero.level >= 2
        if when == "energy_low":
            return hero.energy <= int(cfg.get("energy_low", 10))
        if when == "bag_full":
            return self._bag_full(hero)
        if when == "cave":
            return self._dng_kind(hero.x, hero.y) is not None
        if when == "ecamp":
            return self._ecamp_standing(hero.x, hero.y) is not None
        if when == "node":
            return bool(self._node_found(hero))
        if when == "rank_up":
            return any(self._prof_rank(hero, pid) >= 2 for pid in hero.professions)
        if when == "raid":
            camp = self.store.get("camp", hero.camp) if hero.camp else None
            return bool(camp and camp.get("raid"))
        if when == "kills":
            return hero.kills >= int(cfg.get("options_kills", 3))
        if when == "path_done":
            return self._guide_basic_done(hero) and not hero.origin
        return False

    def _guide_tip(self, hero: Hero, screen: str = "main") -> list[str]:
        """One tip whose moment came (not seen yet, unlocked by its step), marked as seen; [] if none.

        [ES]
        Qué hace: elige UN aviso de content/guide.yaml "tips" (en su orden) que el héroe no vio, que ya abrió su paso (un
        paso con "unlocks") y cuyo momento llegó (_guide_tip_ready), lo marca como visto y devuelve su texto. "screen" dice
        dónde sale: "combat" (la pantalla de la pelea) o "main" (las pantallas principales).
        La llaman: _guide_hint y _guide_tip_lines. Si cambia, afecta: cuándo sale cada aviso (tests/test_camino_guiado.py).
        """
        guide = self._guide(hero)
        locked = {tid: sid for sid, step in self._guide_steps() for tid in step.get("unlocks") or []}
        for tid, tip in self._guide_tips():
            if tid in guide["tips"] or tip.get("screen", "main") != screen:
                continue
            if tid in locked and locked[tid] not in guide["done"]:
                continue
            if self._guide_tip_ready(hero, tip.get("when")):
                guide["tips"].append(tid)
                t = self.texts
                return ([t.t("guide.tip_title", name=t.t(f"guide.tip.{tid}.name"))]
                        + t.t(f"guide.tip.{tid}.text", **self._guide_values(hero)).split("\n"))
        return []

    # ------------------------------------------------------------------ what the screens show

    def _guide_hint(self, hero: Hero) -> list[str]:
        """The lines a main screen adds: the "🧭 Ahora:" task (if any) and, at most, one new tip.

        [ES]
        Qué hace: lo que agregan las pantallas principales (📍 Zona, 🧭 Explorar, 🏕️ Campamento, 👤 Héroe y el campamento
        enemigo, por _tutorial_hint): la línea "🧭 Ahora:" del paso actual (nada si el camino terminó o el paso espera a que
        salgas del Claro) y como mucho un aviso nuevo, que queda visto.
        La llama: GameService._tutorial_hint. Si cambia, afecta: el final de esas pantallas.
        """
        lines: list[str] = []
        current = self._guide_current(hero)
        fresh = self._guide(hero).pop("fresh", None)           # the notice just presented this step: not twice
        if current and not self._guide_hidden(hero, current[2]) and fresh != current[1]:
            lines += [""] + self._guide_now(hero, current[1], current[2]) + [self.texts.t("guide.now_hint")]
        tip = self._guide_tip(hero)
        if tip:
            lines += [""] + tip
        return lines

    def _guide_new_request(self, hero: Hero) -> None:
        """A new button or refresh starts: forget which step the last notice presented (the "🧭 Ahora:" line shows again)."""
        self._guide(hero).pop("fresh", None)

    def _guide_tip_lines(self, hero: Hero, screen: str) -> list[str]:
        """A new tip for a given screen ("combat"), with a blank line before; [] if none."""
        tip = self._guide_tip(hero, screen)
        return [""] + tip if tip else []

    def _guide_before(self, hero: Hero, action_id: str | None) -> list[str]:
        """Before an idle action's screen is built (or a refresh): steps that hold now and the button's step; their lines.

        [ES]
        Qué hace: antes de armar la pantalla de un botón fuera de combate (y en view()), completa el paso que ya se cumple sin
        evento (volviste al Claro, ya tienes campamento) o el que pide ese botón ("map", "claro", "trainer", "hero"), y
        devuelve sus líneas para el aviso. Va antes para que la línea "🧭 Ahora:" de la pantalla ya sea la del paso siguiente.
        La llaman: GameService.act() y view(). Si cambia, afecta: los pasos de botón del camino.
        """
        lines = self._guide_settle_state(hero)
        if action_id:
            lines += self._guide_action(hero, action_id)
        return lines

    def _guide_go(self, hero: Hero, step: dict[str, Any]) -> list[Action]:
        """The buttons of a step's screen: the 4 routes of 📍 Zona (go: routes) or the one button the step asks for."""
        t = self.texts
        go = step.get("go")
        if go == "routes":
            actions = []
            for direction in ("n", "s", "e", "w"):
                _, seconds, _ = self._route_seconds(hero, direction)
                actions.append(Action(id=f"go:{direction}", label=t.t("zone.go_button", dir=t.t(f"dir.{direction}"),
                                                                       time=self._fmt_duration(seconds))))
            return actions
        return [Action(id=go, label=t.t(f"guide.go.{go}"))] if go else []

    def _guide_view(self, hero: Hero, notice: str | None = None, welcome: bool = False) -> View:
        """🧭 Camino guiado (/guia; also the welcome right after creating the hero): the step now, explained, and its button.

        [ES]
        Qué hace: la pantalla del camino guiado. Al crear el héroe es la bienvenida "🔥 Llegaste al Claro": dónde estás, los
        terrenos de alrededor, cómo moverte (sin energía o con la que diga balance.yaml energy.per_move, y el tiempo) y las 4
        rutas como botones (D-190). Con /guia muestra el paso actual con su explicación y su botón, y los avisos que ya viste.
        Como mucho 4 botones (las rutas) o 1 (el del paso).
        La llaman: _create_action (welcome=True) y la acción "guide" (/guia).
        Si cambia, afecta: la primera pantalla de todos los jugadores nuevos (tests/test_service.py, tests/test_camino_guiado.py).
        """
        t = self.texts
        guide = self._guide(hero)
        body: list[str] = []
        actions: list[Action] = []
        current = self._guide_current(hero)
        if current and not self._guide_hidden(hero, current[2]):
            number, sid, step = current
            values = self._guide_values(hero)
            values["needs"] = "\n".join(self._guide_needs(hero))
            body += [t.t("guide.progress", n=number, total=len(self._guide_steps()), name=self._guide_name(sid)), ""]
            body += t.t(f"guide.step.{sid}.intro", **values).split("\n") + [""] + self._guide_now(hero, sid, step)
            actions = self._guide_go(hero, step)
        elif current:
            body += t.t("guide.path_done").split("\n") + ["", t.t("guide.waiting_away")]
        else:
            body.append(t.t("guide.all_done"))
        known = [tid for tid, _ in self._guide_tips() if tid in guide["tips"]]
        if known:
            body += ["", t.t("guide.learned_title")] + [f"• {t.t(f'guide.tip.{tid}.name')}" for tid in known]
        elif not welcome:
            body += ["", t.t("guide.learned_none")]
        title = t.t("guide.welcome_title") if welcome else t.t("guide.title")
        return View(kind="guide", title=title, body=body, actions=actions, notice=notice)
