"""🪖 Squads of 5 inside a camp's guild (D-253.1, Forma B; how it was applied: D-331, provisional; 0.55): the first slice.

Every camp's members are grouped in squads of up to ladder.squads.size (5). A camp of before 0.55 is grouped the first time
the engine looks at it, in join order (camp["members"] order); a new member goes to the first squad with room, or to a new
squad while the camp has squad slots left. The slots are ladder.squads.by_stage for the camp's stage (2, 3, 5, 8, 10), never
under ⌈members cap ÷ size⌉ (🛖 Cabañas, 🛏️ Literas and the old floor add room) nor ⌈members ÷ size⌉: nobody is ever left
out. Each squad has a 🎖️ chief: by default the founder in the founder's squad and the first member in the others; its members
vote with one button on a mate's card, and a candidate with more than half of the squad's votes becomes chief (otherwise the
chief stays). The chief moves the members of their own squad to another squad with room and names their squad; the founder
and the 🤝 assistants (the officers, D-327) move anyone. The squads only organize for now: the 🌙 Noche de prueba and the
🌊 growing waves (D-329) show how many squads had a winner, as information (the pass rules do not change: E-266).

[ES]
Para qué sirve: la 1.ª parte jugable de la Forma B de D-253 (confirmada el 17-oct-2026: "la escuadra de 5 como unidad para
    organizar y repartir las tareas": el grupo de 5 de D-246 pasa a ser una escuadra dentro del gremio). La forma (cuántas
    escuadras, cómo se vota al jefe, quién mueve, el nombre) la eligió Claude en la capa simple (D-44): D-331, provisional, y
    se le pregunta al dueño (E-266 a E-268). Es parte de GameService (una "mezcla", como LadderMixin), en su propio archivo
    para no agrandar game.py.
Documento de diseño: diseno/09-construccion/escalera-del-asentamiento.md §0.6 (cómo quedó) y §3;
    diseno/08-social/gremios-y-social.md §0.2
Módulo: capa de servicios (M15 Social: las escuadras y su jefe; M9 Frontera y Fundación: cuántas abre cada etapa)
Depende de: content/balance.yaml (ladder.squads: size, by_stage y name_max_chars; camps.stages), content/locales/es_escuadras.yaml
    y en_escuadras.yaml (textos), engine.hero (Hero) y las ayudas de GameService (_ladder_cfg, _camp_stage_id, _members_cap,
    _member_camp, _camp_manager, _camp_helpers, _camp_member_view, _guild_view, _hero_data, _hero_name, _online, _ago, _codes,
    _idle_warned_mark, _push_each)
Lo usan: engine/service/game.py (GameService hereda de esta clase): _idle_action (SQUAD_ACTIONS: "squads", "sqvote:", "sqmv:",
    "sqto:", "sqname"; también ocupado: es un menú), _name_camp (el modo "sqname": el nombre que escribe el jefe), _raid_lines
    (_squads_winners_line: la línea de la 🌙 Noche de prueba y de la 🌊 oleada creciente abierta), _resolve_raid
    (_squads_winners_report: el parte) y _faq_values (_squad_faq_values: {squad_size} de ❓ /d37); engine/service/gremio.py:
    _camp_members_view (_squads_members_line y el botón 🪖 Escuadras) y _camp_member_view (_squad_card_lines y
    _squad_card_actions: 🗳️ Votar como jefe y 🔀 Cambiar de escuadra)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño (dentro del registro "camp", clave "x:y"):
    "squads": [{"n", "name", "members", "chief", "votes"}], en el orden en que nacieron: "n" el número de la escuadra (1, 2…;
        nunca se reutiliza dentro del campamento), "name" el nombre que le puso su jefe ("" = sin nombre), "members" [cuentas, en
        el orden en que entraron a la escuadra], "chief" la cuenta del 🎖️ jefe (None si está vacía) y "votes" {votante: candidato}
        (solo votos entre miembros de esa escuadra). Se escribe la primera vez que una pantalla de escuadras mira el campamento
        (_squads) y en cada voto, cambio o nombre; una escuadra vacía queda (con su número y su nombre) y recibe a los que
        lleguen. Quien espera lugar (D-294) no está en ninguna escuadra: no es miembro del campamento.
Reglas que nunca se rompen:
    1. Nadie queda afuera ni pierde nada (D-64): cada miembro del campamento está en una sola escuadra; agrupar, mover o votar
       nunca saca a nadie del campamento ni toca su héroe. Si el cupo baja, las escuadras que ya están se quedan.
    2. Una escuadra nunca pasa de ladder.squads.size al mover gente; los nuevos entran en la primera con lugar.
    3. El jefe acomoda (mueve a los de su escuadra y le pone nombre) pero no acepta gente: aceptan el fundador y los 🤝
       asistentes (D-253.4, D-327). Votar es solo entre los de la misma escuadra; sin mayoría, el jefe sigue.
    4. Por ahora solo informan: las escuadras no cambian lo que pide la 🌙 Noche de prueba ni las 🌊 oleadas crecientes (E-266).
    5. Ningún texto visible se escribe aquí: todo sale de content/locales (es_escuadras.yaml y en_escuadras.yaml), y todo aviso a
       otro jugador se arma con _push_each (le llega en su idioma, D-250). El nombre de una escuadra se limpia
       (clean_squad_name): sin saltos de línea, letras invisibles ni < >, y como mucho name_max_chars letras.
Si cambias esto, revisa:
    - Números: balance.yaml ladder.squads (size, by_stage, name_max_chars) y camps.members_by_stage (by_stage × size tiene que
      dar el cupo de cada etapa); el registro de balance (diseno/03-personaje/balance.md)
    - Pantallas y botones: "squads", "sqvote:<cuenta>", "sqmv:<página>:<cuenta>", "sqto:<n>:<cuenta>" y "sqname" (ids estables;
      64 bytes como máximo en Telegram); la tarjeta del miembro tiene 4 botones como máximo (🤝, 🗳️, 🔀 y ↩️)
    - Mapa de impacto: diseno/01-plataforma/mapa-de-impacto.md (M15 "Las escuadras" y la cascada C-35)
    - Pruebas: tests/test_escuadras.py; tests/test_submenus_campamento_gremio.py (los botones de 👥 Miembros)
"""

from __future__ import annotations

import unicodedata
from collections import Counter
from typing import Any

from engine.hero import Hero
from engine.messaging import Action, View

# Button ids of the squads (stable): 🪖 Escuadras, 🗳️ vote for a mate as chief, 🔀 the move screen (with its page), move to
# squad n, ✏️ name your squad. [ES] Los botones de las escuadras (ids estables): la pantalla, votar, la pantalla de mover
# ("sqmv:<página>:<cuenta>"), mover a la escuadra n ("sqto:<n>:<cuenta>") y ponerle nombre.
SQUAD_ACTIONS = ("squads", "sqvote:", "sqmv:", "sqto:", "sqname")
# Characters a squad name never keeps (besides control and invisible ones). [ES] Lo que el nombre nunca guarda.
NAME_DROP = set("<>«»")


def clean_squad_name(text: str, limit: int) -> str:
    """A squad name as it is kept: no control or invisible characters, no < > « », single spaces, at most `limit` letters.

    [ES] Qué hace: limpia lo que escribió el jefe: saca los caracteres de control y los invisibles (categoría Unicode C:
    saltos de línea, tabuladores, espacios de ancho cero…), los < > y las comillas « » (las usa la pantalla), junta los
    espacios y corta en `limit` letras. Puede devolver "" (nombre vacío: no sirve). La llama: _squad_name_text y las pruebas.
    Si cambia, afecta: qué nombres quedan (tests/test_escuadras.py)."""
    kept = "".join(" " if ch.isspace() else ch for ch in text
                   if ch.isspace() or (unicodedata.category(ch)[0] != "C" and ch not in NAME_DROP))
    kept = " ".join(kept.split())
    return kept[:max(1, int(limit))].strip()


class SquadsMixin:
    """🪖 The squads of a camp's guild (D-253.1 Forma B, D-331). Mixed into GameService; uses its helpers (see the [ES] header).

    [ES]
    Qué es: agrupar a los miembros de cada campamento en escuadras de 5, su 🎖️ jefe (votado), moverlos, el nombre y la línea
    de las escuadras con un vencedor.
    Quién la usa: GameService (hereda de esta clase) y GremioMixin (👥 Miembros y la tarjeta de un miembro).
    Si cambia, afecta: cómo se ve y se organiza cada campamento; nunca quién es miembro.
    """

    # ------------------------------------------------------------------ numbers

    def _squad_cfg(self) -> dict[str, Any]:
        return self._ladder_cfg().get("squads") or {}

    def _squad_size(self) -> int:
        """ladder.squads.size: how many fit in a squad (5, D-246 and D-253)."""
        return max(1, int(self._squad_cfg().get("size", 5) or 5))

    def _squad_name_max(self) -> int:
        return max(1, int(self._squad_cfg().get("name_max_chars", 20) or 20))

    def _squad_slots(self, camp: dict[str, Any]) -> int:
        """How many squads the camp may have: its stage's (2 to 10), never under ⌈cap ÷ 5⌉ nor ⌈members ÷ 5⌉ (D-331).

        [ES] Qué hace: el número de escuadras que abre la etapa del campamento (ladder.squads.by_stage: campamento 2, aldea 3,
        pueblo 5, ciudad 8, castillo 10) y, si el campamento tiene más cupo (🛖 Cabañas, 🛏️ Literas o el piso de antes,
        _members_cap) o más miembros que eso, las que hagan falta para que todos quepan de a 5. Así el cupo de miembros y el de
        escuadras nunca se contradicen. La llaman: _squads_normal, la pantalla 🪖 Escuadras y la de mover. Si cambia, afecta:
        cuándo nace una escuadra nueva (tests/test_escuadras.py)."""
        size = self._squad_size()
        table = self._squad_cfg().get("by_stage") or {}
        stage = int(table.get(self._camp_stage_id(int(camp.get("level", 1)))) or 0)
        by_cap = -(-int(self._members_cap(camp)) // size)
        by_members = -(-len(camp.get("members") or []) // size)
        return max(1, stage, by_cap, by_members)

    # ------------------------------------------------------------------ the squads of a camp (grouping, chief, votes)

    @staticmethod
    def _squad_settle(squad: dict[str, Any], founder: str | None) -> None:
        """Keep only votes among the squad's members; a candidate with more than half of them is chief, else the chief stays.

        [ES] Qué hace: la regla del jefe (D-331, provisional): solo cuentan los votos de un miembro de la escuadra por otro
        miembro de la escuadra; quien tiene más de la mitad de los votos de la escuadra es el jefe; si nadie la tiene, el jefe
        sigue; si el jefe ya no está (salió del campamento o pasó a otra escuadra), es el fundador si está en ella o, si no, el
        primero de la escuadra. Una escuadra vacía no tiene jefe. La llaman: _squads_normal, _squad_move y _squad_vote."""
        members = squad["members"]
        squad["votes"] = {v: c for v, c in (squad.get("votes") or {}).items() if v in members and c in members}
        if not members:
            squad["chief"] = None
            return
        winner = next((c for c, n in Counter(squad["votes"].values()).items() if 2 * n > len(members)), None)
        if winner is not None:
            squad["chief"] = winner
        elif squad.get("chief") not in members:
            squad["chief"] = founder if founder in members else members[0]

    def _squads_normal(self, camp: dict[str, Any]) -> list[dict[str, Any]]:
        """The camp's squads as they should be now (a new list; the camp is not touched): everyone placed, chiefs settled.

        [ES] Qué hace: parte de camp["squads"] (si no hay, de nada: un campamento de antes de la 0.55), saca a quien ya no es
        miembro (salió, lo liberó el barrido de los 30 días) y a quien aparece dos veces, y pone a cada miembro sin escuadra
        en orden de llegada (el orden de camp["members"]) en la primera escuadra con lugar o, si no hay, en una nueva (siempre
        hay lugar: _squad_slots nunca deja a nadie afuera). Después arregla votos y jefes (_squad_settle). No guarda nada: lo
        guarda _squads; _squads_winners la usa sin guardar. Si cambia, afecta: quién está en cada escuadra."""
        members = list(camp.get("members") or [])
        known = set(members)
        size = self._squad_size()
        squads: list[dict[str, Any]] = []
        placed: set[str] = set()
        for raw in camp.get("squads") or []:
            mine = []
            for account in raw.get("members") or []:
                if account in known and account not in placed:
                    mine.append(account)
                    placed.add(account)
            n = int(raw.get("n") or 0) or max((s["n"] for s in squads), default=0) + 1
            squads.append({"n": n, "name": str(raw.get("name") or ""), "members": mine, "chief": raw.get("chief"),
                           "votes": dict(raw.get("votes") or {})})
        for account in members:                         # join order: the founder first, then who came in after
            if account in placed:
                continue
            target = next((s for s in squads if len(s["members"]) < size), None)
            if target is None:                          # every squad is full: a new one (the slots always allow it)
                target = {"n": max((s["n"] for s in squads), default=0) + 1, "name": "", "members": [], "chief": None,
                          "votes": {}}
                squads.append(target)
            target["members"].append(account)
            placed.add(account)
        founder = camp.get("founder_id")
        for squad in squads:
            self._squad_settle(squad, founder)
        return squads

    def _squads(self, key: str, camp: dict[str, Any]) -> list[dict[str, Any]]:
        """The camp's squads, grouped and saved if they changed (the first look at a camp of before 0.55 groups it, D-64).

        [ES] Qué hace: _squads_normal y, si cambió algo (un campamento de antes que se agrupa por primera vez, alguien que
        entró o salió), lo guarda en camp["squads"] y en el almacén. La llaman: las pantallas y acciones de esta sección y la
        tarjeta del miembro (gremio.py). Si cambia, afecta: lo guardado de las escuadras."""
        squads = self._squads_normal(camp)
        if squads != camp.get("squads"):
            camp["squads"] = squads
            self.store.put("camp", key, camp)
        return squads

    @staticmethod
    def _squad_of(squads: list[dict[str, Any]], account: str) -> dict[str, Any] | None:
        return next((s for s in squads if account in s["members"]), None)

    def _squad_label(self, squad: dict[str, Any]) -> str:
        """"Escuadra 2" or "Escuadra 2 «Lobos»" in the player's language."""
        t = self.texts
        if squad.get("name"):
            return t.t("squads.label_named", n=squad["n"], name=squad["name"])
        return t.t("squads.label", n=squad["n"])

    def _squad_chief_name(self, squad: dict[str, Any], hero: Hero) -> str:
        chief = squad.get("chief")
        if not chief:
            return "—"
        return hero.name if chief == hero.id else self._hero_name(chief)

    def _squad_can_move(self, camp: dict[str, Any], squads: list[dict[str, Any]], actor: str, account: str) -> bool:
        """The founder and the 🤝 assistants move anyone; a squad's chief moves the members of their own squad (D-331)."""
        if actor not in camp.get("members", []) or account not in camp.get("members", []):
            return False
        if self._camp_manager(camp, actor):
            return True
        squad = self._squad_of(squads, account)
        return bool(squad) and squad.get("chief") == actor

    def _squad_targets(self, camp: dict[str, Any], squads: list[dict[str, Any]], account: str) -> list[tuple[int, str]]:
        """Where a member can go: (n, label) of every other squad with room, then a new squad if the camp has a slot left."""
        t = self.texts
        size = self._squad_size()
        here = self._squad_of(squads, account)
        out = [(s["n"], t.t("squads.move_to", label=self._squad_label(s), n=len(s["members"]), size=size))
               for s in squads if s is not here and len(s["members"]) < size]
        if len(squads) < self._squad_slots(camp):
            new = max((s["n"] for s in squads), default=0) + 1
            out.append((new, t.t("squads.move_new", n=new)))
        return out

    # ------------------------------------------------------------------ hooks for 👥 Miembros and a member's card (gremio.py)

    def _squads_members_line(self, camp: dict[str, Any], hero: Hero) -> str:
        """👥 Miembros: "🪖 Tu escuadra: Escuadra 1 · 🎖️ jefe: Lyra (en total, 2 escuadras)." ("" for who waits for room).

        [ES] La llama: gremio.py _camp_members_view. Si cambia, afecta: tests/test_escuadras.py."""
        if hero.id not in camp.get("members", []):
            return ""
        squads = self._squads(f"{camp['x']}:{camp['y']}", camp)
        mine = self._squad_of(squads, hero.id)
        if mine is None:
            return ""
        used = sum(1 for s in squads if s["members"])
        return self.texts.t("squads.members_line", label=self._squad_label(mine), chief=self._squad_chief_name(mine, hero),
                            n=used)

    def _squad_card_lines(self, camp: dict[str, Any], hero: Hero, account: str) -> list[str]:
        """A member's card: their squad and chief and, for a mate of your squad, their chief votes (D-331).

        [ES] Qué hace: "🪖 Escuadra 2 · 🎖️ jefe: Bram" y, si es de tu escuadra, "🗳️ Votos para que sea jefe: 2 de 4 (gana con
        3)". La llama: gremio.py _camp_member_view (no en la tarjeta de quien espera lugar)."""
        t = self.texts
        squads = self._squads(f"{camp['x']}:{camp['y']}", camp)
        squad = self._squad_of(squads, account)
        if squad is None:
            return []
        lines = [t.t("squads.card_line", label=self._squad_label(squad), chief=self._squad_chief_name(squad, hero))]
        if hero.id in squad["members"]:
            n = len(squad["members"])
            votes = sum(1 for c in squad["votes"].values() if c == account)
            lines.append(t.t("squads.card_votes", votes=votes, n=n, need=n // 2 + 1))
        return lines

    def _squad_card_actions(self, camp: dict[str, Any], hero: Hero, account: str) -> list[Action]:
        """A member's card: 🗳️ Votar como jefe / ✖️ Quitar mi voto (a mate of your squad) and 🔀 Cambiar de escuadra (who may).

        [ES] Qué hace: los dos botones de las escuadras en la tarjeta (con 🤝 Hacer asistente y ↩️ Volver quedan 4 como mucho).
        🔀 sale si puedes mover a ese miembro (_squad_can_move) y hay adónde (_squad_targets). La llama: gremio.py
        _camp_member_view. Si cambia, afecta: tests/test_escuadras.py."""
        t = self.texts
        if hero.id not in camp.get("members", []):
            return []
        squads = self._squads(f"{camp['x']}:{camp['y']}", camp)
        squad = self._squad_of(squads, account)
        if squad is None:
            return []
        actions = []
        if hero.id in squad["members"]:
            voted = squad["votes"].get(hero.id) == account
            actions.append(Action(id=f"sqvote:{account}", label=t.t("squads.unvote_button" if voted else "squads.vote_button")))
        if self._squad_can_move(camp, squads, hero.id, account) and self._squad_targets(camp, squads, account):
            actions.append(Action(id=f"sqmv:0:{account}", label=t.t("squads.move_button")))
        return actions

    # ------------------------------------------------------------------ the screens and actions

    def _squad_action(self, hero: Hero, action_id: str) -> View:
        """Route SQUAD_ACTIONS: "squads", "sqvote:<account>", "sqmv:<page>:<account>", "sqto:<n>:<account>" and "sqname".

        [ES] La llama: game.py _idle_action. Si cambia, afecta: los ids de botón de las escuadras (64 bytes en Telegram)."""
        head, _, arg = action_id.partition(":")
        if head == "sqvote":
            return self._squad_vote(hero, arg)
        if head in ("sqmv", "sqto"):
            number, _, account = arg.partition(":")
            if not number.isdigit():
                return self._squads_view(hero)
            if head == "sqmv":
                return self._squad_move_view(hero, account, int(number))
            return self._squad_move(hero, account, int(number))
        if head == "sqname":
            return self._squad_name_ask(hero)
        return self._squads_view(hero)

    def _squad_member_row(self, n: int, account: str, squad: dict[str, Any], camp: dict[str, Any], hero: Hero) -> str:
        """"/m3 🎖️ 🤝 Bram (nv 5) · 🟢 en línea": code, marks (👑 founder, 🤝 assistant, 🎖️ chief, 💤 warned), level and state."""
        t = self.texts
        data = self._hero_data(account, hero) or {}
        role = self._idle_warned_mark(camp, account)
        if account == camp.get("founder_id"):
            role += t.t("gremio.role_leader")
        elif account in self._camp_helpers(camp):
            role += t.t("helpers.role")
        if account == squad.get("chief"):
            role += t.t("squads.role_chief")
        state = (t.t("gremio.online") if self._online(data)
                 else t.t("gremio.offline", ago=self._ago(float(data.get("seen_at", 0.0) or 0.0))))
        return t.t("squads.member_line", code=f"/m{n}", role=role, name=data.get("name", "?"), level=data.get("level", 1),
                   state=state)

    def _squads_view(self, hero: Hero, notice: str | None = None) -> View:
        """🪖 Escuadras: every squad (yours first) with its number, name, 🎖️ chief and members with /m codes (D-331).

        [ES]
        Qué hace: la pantalla de las escuadras del campamento (🛡️ Gremio → 👥 Miembros → 🪖 Escuadras): arriba cuántas hay y
        cuántas abre la etapa; después cada escuadra, primero la tuya, con su número, su nombre, su 🎖️ jefe y sus miembros
        (código /m1, 👑 el fundador, 🤝 los asistentes, 🎖️ el jefe, 💤 quien fue avisado, nivel y si está en línea o cuándo
        jugó), y la pista de cómo votar y mover (desde la tarjeta de cada uno: los códigos /m de aquí abren esa tarjeta).
        Botones: ✏️ Nombre de la escuadra (solo su jefe) y ↩️ Volver a 👥 Miembros. Solo los miembros del campamento (quien
        espera lugar vuelve al gremio). La llaman: el botón 🪖 Escuadras ("squads"), _squad_name_text y el ❌ del nombre. Si
        cambia, afecta: tests/test_escuadras.py.
        """
        t = self.texts
        camp = self._member_camp(hero)
        if not camp:
            return self._guild_view(hero, notice=notice)
        squads = self._squads(f"{camp['x']}:{camp['y']}", camp)
        mine = self._squad_of(squads, hero.id)
        size = self._squad_size()
        used = [s for s in squads if s["members"]]
        body = [t.t("squads.header", n=len(used), size=size, slots=self._squad_slots(camp)), ""]
        codes: list[str] = []
        for squad in ([mine] if mine else []) + [s for s in squads if s is not mine]:
            key = "squads.squad_line_mine" if squad is mine else "squads.squad_line"
            body.append(t.t(key, label=self._squad_label(squad), n=len(squad["members"]), size=size,
                            chief=self._squad_chief_name(squad, hero)))
            for account in squad["members"]:
                codes.append(account)
                body.append(self._squad_member_row(len(codes), account, squad, camp, hero))
            if not squad["members"]:
                body.append(t.t("squads.squad_empty"))
            body.append("")
        body.append(t.t("squads.hint"))
        self._codes(hero, "members", codes)             # /m3 opens that member's card (to vote or move)
        actions = []
        if mine and mine.get("chief") == hero.id:
            actions.append(Action(id="sqname", label=t.t("squads.name_button")))
        actions.append(Action(id="gmembers", label=t.t("menu.back")))
        return View(kind="squads", title=t.t("squads.title"), body=body, actions=actions, notice=notice)

    def _squad_vote(self, hero: Hero, account: str) -> View:
        """🗳️ Votar como jefe (or ✖️ take the vote back): only for a mate of your own squad; a majority makes the chief.

        [ES] Qué hace: anota (o borra, si ya lo habías votado) tu voto por ese compañero de tu escuadra. Con más de la mitad de
        los votos de la escuadra pasa a ser el 🎖️ jefe (_squad_settle) y a los demás de la escuadra les llega el aviso, cada
        uno en su idioma (_push_each). Sin mayoría, el jefe sigue. La llama: "sqvote:<cuenta>" (la tarjeta del miembro). Si
        cambia, afecta: tests/test_escuadras.py."""
        t = self.texts
        camp = self._member_camp(hero)
        if not camp:
            return self._guild_view(hero)
        key = f"{camp['x']}:{camp['y']}"
        squads = self._squads(key, camp)
        squad = self._squad_of(squads, hero.id)
        if squad is None or account not in squad["members"]:
            if account in camp["members"]:
                return self._camp_member_view(hero, account, notice=t.t("squads.vote_other"))
            return self._squads_view(hero, notice=t.t("squads.vote_other"))
        before = squad.get("chief")
        name = hero.name if account == hero.id else self._hero_name(account)
        if squad["votes"].get(hero.id) == account:
            squad["votes"].pop(hero.id)
            notes = [t.t("squads.unvoted")]
        else:
            squad["votes"][hero.id] = account
            n = len(squad["members"])
            votes = sum(1 for c in squad["votes"].values() if c == account)
            notes = [t.t("squads.voted", name=name, votes=votes, n=n, need=n // 2 + 1)]
        self._squad_settle(squad, camp.get("founder_id"))
        camp["squads"] = squads
        self.store.put("camp", key, camp)
        if squad.get("chief") != before:
            label = self._squad_label(squad)
            chief_name = self._squad_chief_name(squad, hero)
            notes.append(t.t("squads.new_chief", name=chief_name, label=label))
            camp_name = camp["name"]
            self._push_each([m for m in squad["members"] if m != hero.id], lambda: View(
                kind="gremio_news", title=t.t("squads.title"),
                body=[t.t("squads.new_chief_push", name=chief_name, label=self._squad_label(squad), camp=camp_name)],
                actions=[Action(id="squads", label=t.t("squads.button"))]))
        return self._camp_member_view(hero, account, notice=" ".join(notes))

    def _squad_move_view(self, hero: Hero, account: str, page: int = 0, notice: str | None = None) -> View:
        """🔀 Cambiar de escuadra: where that member can go (squads with room and a new one if allowed), up to 3 per page.

        [ES] Qué hace: la pantalla para mover a un miembro: dónde está y un botón por cada escuadra con lugar (y 🆕 una nueva si
        la etapa abre otra). Con 4 botones como máximo (D-75): hasta 3 destinos y ↩️ Volver; con más, 2 por página y
        ➡️ Más escuadras. Solo quien puede moverlo (_squad_can_move). La llama: "sqmv:<página>:<cuenta>". Si cambia, afecta:
        tests/test_escuadras.py."""
        t = self.texts
        camp = self._member_camp(hero)
        if not camp or account not in camp["members"]:
            return self._guild_view(hero)
        squads = self._squads(f"{camp['x']}:{camp['y']}", camp)
        if not self._squad_can_move(camp, squads, hero.id, account):
            return self._camp_member_view(hero, account, notice=t.t("squads.cannot_move"))
        targets = self._squad_targets(camp, squads, account)
        if not targets:
            return self._camp_member_view(hero, account, notice=t.t("squads.no_room"))
        here = self._squad_of(squads, account)
        name = hero.name if account == hero.id else self._hero_name(account)
        body = [t.t("squads.move_ask", name=name, label=self._squad_label(here) if here else "—")]
        per = len(targets) if len(targets) <= 3 else 2
        pages = -(-len(targets) // per)
        page = page % pages
        actions = [Action(id=f"sqto:{n}:{account}", label=label) for n, label in targets[page * per:(page + 1) * per]]
        if pages > 1:
            actions.append(Action(id=f"sqmv:{(page + 1) % pages}:{account}", label=t.t("squads.more")))
        actions.append(Action(id=f"gmem:{account}", label=t.t("menu.back")))
        return View(kind="squad_move", title=t.t("squads.move_title"), body=body, actions=actions, notice=notice)

    def _squad_move(self, hero: Hero, account: str, number: int) -> View:
        """Move a member to squad `number` (an existing one with room, or the next new one while slots are left).

        [ES] Qué hace: pasa al miembro a otra escuadra: sale de la suya (su voto y los votos por él se borran) y entra al final
        de la otra; si era el jefe, su escuadra tiene jefe nuevo (_squad_settle). Nunca llena una escuadra de más ni abre más
        escuadras que las de la etapa. Al miembro le llega el aviso (_push_each) si lo movió otro. La llama:
        "sqto:<n>:<cuenta>". Si cambia, afecta: tests/test_escuadras.py."""
        t = self.texts
        camp = self._member_camp(hero)
        if not camp or account not in camp["members"]:
            return self._guild_view(hero)
        key = f"{camp['x']}:{camp['y']}"
        squads = self._squads(key, camp)
        if not self._squad_can_move(camp, squads, hero.id, account):
            return self._camp_member_view(hero, account, notice=t.t("squads.cannot_move"))
        here = self._squad_of(squads, account)
        if here is None or here["n"] == number:
            return self._camp_member_view(hero, account)
        size = self._squad_size()
        target = next((s for s in squads if s["n"] == number), None)
        if target is None:
            new = max((s["n"] for s in squads), default=0) + 1
            if number != new or len(squads) >= self._squad_slots(camp):
                return self._camp_member_view(hero, account, notice=t.t("squads.no_room"))
            target = {"n": new, "name": "", "members": [], "chief": None, "votes": {}}
            squads.append(target)
        if len(target["members"]) >= size:
            return self._camp_member_view(hero, account, notice=t.t("squads.full", size=size))
        before = here.get("chief")
        here["members"] = [m for m in here["members"] if m != account]
        target["members"].append(account)
        founder = camp.get("founder_id")
        self._squad_settle(here, founder)
        self._squad_settle(target, founder)
        camp["squads"] = squads
        self.store.put("camp", key, camp)
        name = hero.name if account == hero.id else self._hero_name(account)
        camp_name, who = camp["name"], hero.name
        if account != hero.id:
            self._push_each([account], lambda: View(
                kind="gremio_news", title=t.t("squads.title"),
                body=[t.t("squads.moved_push", who=who, label=self._squad_label(target), camp=camp_name)],
                actions=[Action(id="squads", label=t.t("squads.button"))]))
        if here["members"] and here.get("chief") != before:
            chief = here["chief"]
            chief_name = self._hero_name(chief) if chief != hero.id else hero.name
            self._push_each([m for m in here["members"] if m != hero.id], lambda: View(
                kind="gremio_news", title=t.t("squads.title"),
                body=[t.t("squads.new_chief_push", name=chief_name, label=self._squad_label(here), camp=camp_name)],
                actions=[Action(id="squads", label=t.t("squads.button"))]))
        return self._camp_member_view(hero, account, notice=t.t("squads.moved", name=name, label=self._squad_label(target)))

    def _squad_name_ask(self, hero: Hero) -> View:
        """✏️ Nombre de la escuadra: only its 🎖️ chief; the next text the chief writes is the name (camp_naming "sqname")."""
        t = self.texts
        camp = self._member_camp(hero)
        if not camp:
            return self._guild_view(hero)
        squads = self._squads(f"{camp['x']}:{camp['y']}", camp)
        mine = self._squad_of(squads, hero.id)
        if not mine or mine.get("chief") != hero.id:
            return self._squads_view(hero, notice=t.t("squads.only_chief"))
        self.store.put("camp_naming", hero.id, {"mode": "sqname", "x": hero.x, "y": hero.y})
        return View(kind="squad_name", title=t.t("squads.title"), body=[t.t("squads.name_ask", n=self._squad_name_max())],
                    expects_text=True, actions=[Action(id="squads", label=t.t("squads.cancel"))])

    def _squad_name_text(self, hero: Hero, text: str) -> View:
        """The name the chief wrote: cleaned (clean_squad_name) and kept; an empty one asks again (D-331).

        [ES] Qué hace: limpia el nombre (sin saltos de línea, letras invisibles ni < >; como mucho ladder.squads.name_max_chars
        letras) y se lo pone a la escuadra del jefe; vacío, lo vuelve a pedir. Si ya no es el jefe, no cambia nada. La llama:
        game.py _name_camp (el modo "sqname"). Si cambia, afecta: tests/test_escuadras.py."""
        t = self.texts
        self.store.delete("camp_naming", hero.id)
        camp = self._member_camp(hero)
        if not camp:
            return self._guild_view(hero)
        key = f"{camp['x']}:{camp['y']}"
        squads = self._squads(key, camp)
        mine = self._squad_of(squads, hero.id)
        if not mine or mine.get("chief") != hero.id:
            return self._squads_view(hero, notice=t.t("squads.only_chief"))
        name = clean_squad_name(text, self._squad_name_max())
        if not name:
            view = self._squad_name_ask(hero)
            view.notice = t.t("squads.name_bad")
            return view
        mine["name"] = name
        camp["squads"] = squads
        self.store.put("camp", key, camp)
        return self._squads_view(hero, notice=t.t("squads.named", label=self._squad_label(mine)))

    # ------------------------------------------------------------------ 🌙 the Noche de prueba and 🌊 the growing waves (info only)

    def _squads_winners(self, camp: dict[str, Any], raid: dict[str, Any]) -> tuple[int, int]:
        """(squads with at least one winner of this raid, squads with members): the D-253 "N escuadras que vencen", as info."""
        won = {account for account, result in (raid.get("fights") or {}).items() if result == "won"}
        squads = [s for s in self._squads_normal(camp) if s["members"]]
        return sum(1 for s in squads if won.intersection(s["members"])), len(squads)

    @staticmethod
    def _squads_count_raid(raid: dict[str, Any]) -> bool:
        """The raids whose line shows the squads: the 🌙 Noche de prueba and a 🌊 growing wave of the castle (D-329)."""
        return raid.get("kind") == "trial" or bool(raid.get("wave"))

    def _squads_winners_line(self, camp: dict[str, Any], raid: dict[str, Any]) -> list[str]:
        """The open raid's line: "🪖 Escuadras con al menos un vencedor: 2 de 3." (only the Noche de prueba and the waves).

        [ES] Qué hace: solo información (D-331; si pasa a ser una regla, lo decide el dueño: E-266): cuántas escuadras ya tienen
        al menos un miembro que ganó su pelea en esta 🌙 Noche de prueba o 🌊 oleada creciente. No guarda nada. La llama: game.py
        _raid_lines (la pantalla del campamento, 🏰 Gestionar, ℹ️ Información y la pantalla de la Noche de prueba). Si cambia,
        afecta: tests/test_escuadras.py."""
        if not self._squads_count_raid(raid):
            return []
        n, total = self._squads_winners(camp, raid)
        return [self.texts.t("squads.winners_line", n=n, total=total)]

    def _squads_winners_report(self, camp: dict[str, Any], raid: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
        """The closing report's line (key, values), written in each member's language by _resolve_raid (D-250)."""
        if not self._squads_count_raid(raid):
            return []
        n, total = self._squads_winners(camp, raid)
        return [("squads.winners_report", {"n": n, "total": total})]

    # ------------------------------------------------------------------ ❓ Dudas

    def _squad_faq_values(self) -> dict[str, Any]:
        """{squad_size} for ❓ /d37 (the squads of 5, D-331)."""
        return {"squad_size": self._squad_size()}
