"""💀 Optional permadeath and the 🪦 hall of the fallen (D-147, confirmed; how it was applied: D-336, provisional; 0.60).

A hero up to permadeath.max_level swears it in ⚙️ Opciones → 💀 Muerte permanente, with two confirmations (each valid for
permadeath.confirm_minutes, kept in the store so an old button cannot swear it alone). It cannot be undone. While sworn the
hero shows a 💀 mark before its name and earns prestige-only titles by days lived with the oath (permadeath.titles); it never
changes stats or coins. A sworn hero leads nothing (there is no founder succession yet): a camp founder or a guild leader
cannot swear it, and a sworn hero cannot create a guild or receive the leadership.

When a sworn hero loses any fight (_end_combat), it falls for ever: a memorial goes to the 🪦 hall ("fallen", "f1", "f2"…),
its open 🏛️ Mercado orders, 📜 crafting orders and 📜 repair orders are cancelled into it, it leaves its camp, its waiting list and its guild, its
per-hero records move with it, and the whole hero is kept in "fallen_hero" (never deleted, D-64). The account keeps its
language, player code and invite code; the next hero receives the ⚙️ Opciones and what was bought with 💎 ("reborn").

[ES]
Para qué sirve: la 💀 muerte permanente opcional que confirmó el dueño (D-147, E-31: "se activa en ⚙️ Opciones con doble
    confirmación; es una sola muerte: el héroe queda en la historia y hay que crear uno nuevo; los premios son solo de
    prestigio") en la capa simple (D-44). Las reglas chicas (hasta qué nivel, que no se apaga, que no lidera, qué pasa con lo
    suyo al caer) las eligió Claude: D-336, provisional; preguntas E-281 a E-283. Es parte de GameService (una "mezcla", como
    RepairMixin), en su propio archivo para no agrandar game.py.
Documento de diseño: diseno/05-salud/secuelas-y-muerte.md §4.2 (§4.2.0: cómo está en el juego); diseno/03-personaje/
    creacion-de-personaje.md (héroe nuevo después de caer)
Módulo: capa de servicios (M7 Salud: la muerte; M2 Héroe: crear otro; M19 Mensajería: el 🪦 Salón de los caídos)
Depende de: content/balance.yaml (permadeath), content/locales/es_muerte_permanente.yaml y en_muerte_permanente.yaml (textos),
    engine.hero (Hero) y las ayudas de GameService (_seconds, _day_seconds, _journal, _grant_title, _title_name, _place_label,
    _push_each, _join, _options_view, _my_gremio, _gremio_link, _gremio_leave_member, _waiting_key, _tell_waiting_room,
    _mkt_mine, _mkt_order, _mkt_close, _mkt_box, _mkt_box_put, _repair_mine, _repair_close; desde la 0.59, _corder_mine y
    _corder_close de engine/service/craft_orders.py)
Lo usan: engine/service/game.py (GameService hereda de esta clase): act() ("fallen" antes de mirar si hay héroe; el corte
    después de _settle si el héroe cayó; _oath_titles; borra "oath_confirm" con cualquier otro botón), text() (el mismo corte;
    /caidos sin héroe), _main_view (_fallen_view), _save (un héroe caído se escribe en su archivo), _end_combat
    (_fall_forever al final de una pelea perdida con 💀), _idle_action (OATH_ACTIONS), _options_view (el botón y la línea),
    _name_taken (_fallen_name_taken), _create_action (_reborn_apply), _hero_view (_oath_hero_lines) y los nombres con
    _oath_mark (👥 Jugadores de la zona, 👤 Héroe); engine/service/gremio.py (_gremio_new, _gremio_name, _gremio_lead:
    _oath_no_lead) y engine/service/story.py (_card_lines: _oath_mark; el 📔 Diario: "oath" y "fell")
Eventos que publica: HeroFellForever (engine/core/events.py) al caer para siempre
Eventos que escucha: ninguno
Datos de los que es dueño:
    Hero.oath (engine/hero/hero.py): {} apagada; {"at"} jurada; al caer suma "fell", "key" y "memorial".
    "oath_confirm" (clave la cuenta): {"step": 1 | 2, "at"}: la confirmación en curso (vale permadeath.confirm_minutes; act()
        la borra con cualquier botón que no sea "oath…").
    "fallen" (clave "f1", "f2"…; nunca se reutiliza): el 🪦 Salón: {"id", "account", "name", "class_id", "level", "enemy",
        "enemy_level", "x", "y", "at", "oath_at", "days", "titles", "archive"}.
    "fallen_hero" (clave "<cuenta>#<n>"): el héroe entero al caer, para siempre: {"hero" (Hero.to_dict, sigue al día si algo lo
        vuelve a guardar), "account", "at", "box" (lo que tenía en 📦 Entregas), "extra" (sus registros de OATH_HERO_SPACES)}.
    "reborn" (clave la cuenta): {"options", "gems", "banner", "xp_boost_until", "from"}: lo que recibe el próximo héroe.
    "meta"/"fallen_seq": {"n"}: el último número del Salón.
Reglas que nunca se rompen:
    1. Solo con la doble confirmación del jugador (dos pantallas, en el almacén y con tiempo): nada la jura solo.
    2. Nada se borra (D-64): el héroe caído queda entero en "fallen_hero"; las órdenes y los encargos se cancelan hacia él.
    3. Solo toca la cuenta del que cae: los demás jugadores solo ven que salió (campamento, espera, gremio) y reciben el aviso.
    4. Solo prestigio: la marca 💀 y los títulos no dan estadísticas, monedas ni nada que se venda.
    5. Un héroe con 💀 no lidera (no hay sucesión de fundador): no la jura un fundador ni un líder, y quien la juró no crea un
       gremio ni recibe el liderazgo.
    6. Ningún texto visible se escribe aquí: todo sale de content/locales, y todo aviso a otro jugador se arma con _push_each.
Si cambias esto, revisa:
    - Números: balance.yaml permadeath (max_level, confirm_minutes, hall_shown, titles); el registro de balance
      (diseno/03-personaje/balance.md, "la muerte permanente")
    - Pantallas y botones: "oath", "oath:ask", "oath:ask2", "oath:swear", "fallen", "newhero" (ids estables); ⚙️ Opciones tiene
      6 botones (EXTRA_BUTTON_KINDS "options" en game.py)
    - Mapa de impacto: diseno/01-plataforma/mapa-de-impacto.md (M7, M2 y la cascada C-39)
    - Pruebas: tests/test_muerte_permanente_y_regeneracion.py; tests/test_options.py y tests/test_guias.py (los botones de
      ⚙️ Opciones)
"""

from __future__ import annotations

import time
from typing import Any

from engine.core import HeroFellForever
from engine.hero import Hero
from engine.messaging import Action, View

# Button ids (stable): the 💀 screen ("oath"), the two confirmations ("oath:ask", "oath:ask2") and the oath ("oath:swear").
# [ES] Los botones de la 💀 muerte permanente. "fallen" es el 🪦 Salón de los caídos (también sin héroe, desde act()).
OATH_ACTIONS = ("oath",)
HALL_ACTION = "fallen"
# What leaves the account with the fallen hero (records keyed by the hero's id: its route being laid out, its dungeon day, its
# scouting, its nodes, the order of its last lists and any open prompt). shop_week stays with the account (no free reset).
# [ES] Los registros por héroe que se van con él al archivo (así el héroe nuevo empieza sin lo que sabía el caído).
OATH_HERO_SPACES = ("walk", "dungeon", "recon", "nodes", "places_shown", "recon_shown", "gremio_codes", "journal_back",
                    "camp_naming", "market_open", "dudas_open", "feedback_open", "oath_confirm", "pending",
                    "corder_open")          # D-335 (0.59): an open 📜 crafting order draft


class PermadeathMixin:
    """💀 permadeath, its double confirmation, the fall and the 🪦 hall (D-147, D-336). GameService inherits it.

    [ES] Qué es: la muerte permanente opcional (D-147) como "mezcla" de GameService. Quién la usa: game.py, gremio.py y
    story.py (ver el encabezado). Si cambia, afecta: quién puede caer para siempre y qué le pasa a su cuenta.
    """

    # ------------------------------------------------------------------ state

    def _oath_cfg(self) -> dict[str, Any]:
        return self.content.balance.get("permadeath") or {}

    def _oath_on(self, hero: Hero) -> bool:
        """True while the hero lives under the sworn 💀 oath (not after the fall)."""
        oath = hero.oath or {}
        return bool(oath.get("at")) and not oath.get("fell")

    def _fell(self, hero: Hero) -> bool:
        """True once this hero fell for ever (it lives only in its "fallen_hero" record)."""
        return bool((hero.oath or {}).get("fell"))

    def _oath_account_on(self, account: str) -> bool:
        """True if that account's saved hero swore the oath (read from the store: for another player's card or the guild)."""
        oath = (self.store.get("hero", account) or {}).get("oath") or {}
        return bool(oath.get("at")) and not oath.get("fell")

    def _oath_mark(self, hero: Hero) -> str:
        """"💀 " before the name of a hero who swore the oath (prestige only), else ""."""
        return self.texts.t("oath.mark") + " " if (hero.oath or {}).get("at") else ""

    def _oath_days(self, hero: Hero, until: float | None = None) -> int:
        """Whole days lived with the oath (until the fall, or now)."""
        at = float((hero.oath or {}).get("at") or 0.0)
        end = float(until if until is not None else (hero.oath or {}).get("fell") or self.clock.now())
        return int(max(0.0, end - at) // self._day_seconds()) if at else 0

    def _oath_titles_cfg(self) -> list[dict[str, Any]]:
        return [dict(e) for e in self._oath_cfg().get("titles") or [] if e.get("id")]

    def _oath_block(self, hero: Hero) -> str | None:
        """Why this hero cannot swear the oath now (a notice), or None: already sworn, past the level, a founder or a leader."""
        t = self.texts
        if self._oath_on(hero) or self._fell(hero):
            return t.t("oath.already")
        top = int(self._oath_cfg().get("max_level", 0) or 0)
        if top and hero.level > top:
            return t.t("oath.too_high", n=top, name=hero.name)
        camp = self.store.get("camp", hero.camp) if hero.camp else None
        if camp and camp.get("founder_id") == hero.id:
            return t.t("oath.no_founder")
        record = self._my_gremio(hero)
        if record and record.get("leader") == hero.id:
            return t.t("oath.no_leader")
        return None

    def _oath_no_lead(self, hero: Hero) -> str | None:
        """The notice that stops a sworn hero from creating or leading a guild (rule 5), or None."""
        return self.texts.t("oath.no_lead") if self._oath_on(hero) else None

    # ------------------------------------------------------------------ ⚙️ Opciones → 💀 Muerte permanente

    def _oath_options_line(self, hero: Hero) -> str:
        """⚙️ Opciones: "💀 Muerte permanente: apagada." or "…: jurada, día N."."""
        if self._oath_on(hero):
            return self.texts.t("oath.options_on", days=self._oath_days(hero) + 1)
        return self.texts.t("oath.options_off")

    def _oath_titles_text(self) -> str:
        t = self.texts
        return " · ".join(t.t("oath.title_item", days=int(e.get("days", 0)), title=self._title_name(e["id"]))
                          for e in self._oath_titles_cfg())

    def _oath_view(self, hero: Hero, notice: str | None = None) -> View:
        """💀 Muerte permanente: the rules, the state, ☠️ Jurar (if allowed), 🪦 Salón de los caídos and ↩️ Volver.

        [ES] Qué hace: la pantalla de ⚙️ Opciones → 💀 Muerte permanente. Apagada: qué es, qué pasa al caer, qué se queda,
        el premio (solo prestigio), hasta qué nivel se jura y, si no se puede, por qué (_oath_block); con ☠️ Jurar si se
        puede. Jurada: el día y el próximo título. Botones: ☠️ Jurar (solo si se puede), 🪦 Salón de los caídos y ↩️ Volver a
        ⚙️ Opciones. La llaman: _oath_action. Si cambia, afecta: tests/test_muerte_permanente_y_regeneracion.py.
        """
        t = self.texts
        top = int(self._oath_cfg().get("max_level", 0) or 0)
        body = [t.t("oath.intro"), "", t.t("oath.rules_fall", name=hero.name), t.t("oath.rules_keep"),
                t.t("oath.rules_prize", titles=self._oath_titles_text()),
                t.t("oath.rules_when", n=top) if top else t.t("oath.rules_when_any"), t.t("oath.rules_lead"), ""]
        actions: list[Action] = []
        if self._oath_on(hero):
            days = self._oath_days(hero)
            body.append(t.t("oath.status_on", days=days))
            nxt = next((e for e in self._oath_titles_cfg() if e["id"] not in hero.titles), None)
            if nxt:
                body.append(t.t("oath.next_title", title=self._title_name(nxt["id"]), days=int(nxt.get("days", 0))))
        else:
            body.append(t.t("oath.status_off"))
            block = self._oath_block(hero)
            if block:
                body.append(block)
            else:
                actions.append(Action(id="oath:ask", label=t.t("oath.swear_button")))
        actions += [Action(id=HALL_ACTION, label=t.t("oath.hall_button")), Action(id="options", label=t.t("menu.back"))]
        return View(kind="oath", title=t.t("oath.title"), body=body, actions=actions, notice=notice)

    def _oath_confirmed(self, hero: Hero, step: int) -> bool:
        """True if the player passed confirmation `step` a moment ago (store "oath_confirm", permadeath.confirm_minutes)."""
        record = self.store.get("oath_confirm", hero.id) or {}
        window = self._seconds(float(self._oath_cfg().get("confirm_minutes", 10)))
        return int(record.get("step", 0)) == step and self.clock.now() - float(record.get("at", 0.0)) <= window

    def _oath_action(self, hero: Hero, action_id: str) -> View:
        """"oath" (the screen), "oath:ask" (1st warning), "oath:ask2" (2nd warning) and "oath:swear" (sworn, for ever).

        [ES] Qué hace: la doble confirmación de D-147. ☠️ Jurar abre la 1.ª advertencia (qué se pierde al caer) y guarda el
        paso 1; ✅ Entiendo abre la 2.ª (no se apaga nunca) solo con el paso 1 vigente y guarda el paso 2; 💀 Sí, para siempre
        jura solo con el paso 2 vigente (permadeath.confirm_minutes) y si _oath_block sigue sin reparos. Cualquier otro
        botón (y volver a la pantalla) borra la confirmación. Al jurar: Hero.oath = {"at": ahora} y una línea en el 📔 Diario.
        La llaman: _idle_action (OATH_ACTIONS). Si cambia, afecta: tests/test_muerte_permanente_y_regeneracion.py.
        """
        t = self.texts
        step = action_id.partition(":")[2]
        now = self.clock.now()
        if step not in ("ask", "ask2", "swear"):
            self.store.delete("oath_confirm", hero.id)
            return self._oath_view(hero)
        block = self._oath_block(hero)
        if block:
            self.store.delete("oath_confirm", hero.id)
            return self._oath_view(hero, notice=block)
        if step == "ask":
            self.store.put("oath_confirm", hero.id, {"step": 1, "at": now})
            body = [t.t("oath.confirm1", name=hero.name), "", t.t("oath.confirm1_lose", name=hero.name, level=hero.level),
                    t.t("oath.confirm1_lead"), t.t("oath.confirm1_prize")]
            return View(kind="oath_confirm", title=t.t("oath.confirm1_title"), body=body,
                        actions=[Action(id="oath:ask2", label=t.t("oath.confirm1_yes")),
                                 Action(id="oath", label=t.t("oath.confirm_no"))])
        if step == "ask2":
            if not self._oath_confirmed(hero, 1):
                self.store.delete("oath_confirm", hero.id)
                return self._oath_view(hero, notice=t.t("oath.confirm_again"))
            self.store.put("oath_confirm", hero.id, {"step": 2, "at": now})
            return View(kind="oath_confirm", title=t.t("oath.confirm2_title"), body=[t.t("oath.confirm2", name=hero.name)],
                        actions=[Action(id="oath:swear", label=t.t("oath.confirm2_yes")),
                                 Action(id="oath", label=t.t("oath.confirm_no"))])
        if not self._oath_confirmed(hero, 2):
            self.store.delete("oath_confirm", hero.id)
            return self._oath_view(hero, notice=t.t("oath.confirm_again"))
        self.store.delete("oath_confirm", hero.id)
        hero.oath = {"at": now}
        self._journal(hero, "oath")
        return self._oath_view(hero, notice=t.t("oath.sworn", name=hero.name))

    def _oath_titles(self, hero: Hero) -> list[str]:
        """Grant the prestige titles whose days the sworn hero already lived (permadeath.titles); their notice lines."""
        if not self._oath_on(hero):
            return []
        days = self._oath_days(hero)
        lines: list[str] = []
        for entry in self._oath_titles_cfg():
            if days >= int(entry.get("days", 0)) and entry["id"] not in hero.titles:
                lines += self._grant_title(hero, entry["id"])
        return lines

    def _oath_hero_lines(self, hero: Hero) -> list[str]:
        """👤 Héroe: "💀 Muerte permanente: día N de su única vida" while sworn."""
        return [self.texts.t("oath.hero_line", days=self._oath_days(hero) + 1)] if self._oath_on(hero) else []

    # ------------------------------------------------------------------ the fall

    def _fallen_mates(self, hero: Hero) -> list[str]:
        """Who hears the news: the other members of its camp, else of its guild before the camp."""
        camp = self.store.get("camp", hero.camp) if hero.camp else None
        if camp:
            return [m for m in camp.get("members") or [] if m != hero.id]
        record = self._gremio_link(hero.id)
        return [m for m in (record or {}).get("members") or [] if m != hero.id]

    def _oath_unlink(self, hero: Hero) -> dict[str, Any]:
        """Take the fallen hero out of everything shared, into itself; returns what goes to its record ("box", "extra").

        [ES] Qué hace: antes de archivar al héroe, cancela sus 📜 pedidos de fabricación (0.59: las monedas a su bolsa, los
        materiales a su 📦 Entregas), sus órdenes del 🏛️ Mercado (lo que quedaba vuelve a él: las monedas a su bolsa en memoria
        y las unidades a su 📦 Entregas, que se va entera al archivo) y sus 📜 encargos de reparación (las monedas vuelven a él); sale de su campamento como con 🚪 Salir (deja de ser asistente; lo que dio queda; quien espera
        entra solo, _tell_waiting_room), de la espera de un campamento lleno y de su gremio de antes del campamento (lo que dio
        queda en el fondo). Un fundador no sale (no puede jurarla: regla 5). Los registros por héroe de OATH_HERO_SPACES se van
        con él. Nada de otro jugador cambia, salvo que ya no está. La llama: _fall_forever.
        """
        out: dict[str, Any] = {}
        for order in self._corder_mine(hero.id):        # D-335 (0.59): its 📜 crafting orders: coins back, materials to the box
            self._corder_close(order, "cancelled", hero)
        for oid in self._mkt_mine(hero.id):
            order = self._mkt_order(oid)
            if order is not None and order.get("by") == hero.id:
                self._mkt_close(order, "cancelled", hero)
        box = self._mkt_box(hero.id)
        if box:
            out["box"] = box
            self._mkt_box_put(hero.id, [])
        self.store.delete("market_mine", hero.id)
        for order in self._repair_mine(hero.id):
            self._repair_close(order, "cancelled", hero)
        key = hero.camp
        camp = self.store.get("camp", key) if key else None
        if camp and camp.get("founder_id") != hero.id:
            camp["members"] = [m for m in camp.get("members") or [] if m != hero.id]
            camp["helpers"] = [h for h in camp.get("helpers") or [] if h != hero.id]
            self.store.put("camp", key, camp)
            hero.camp = None
            self._tell_waiting_room(key)                # a place opened for who waits in the guild (D-323)
        wait = self._waiting_key(hero.id)
        if wait:
            wcamp = self.store.get("camp", wait) or {}
            wcamp["waiting"] = [a for a in wcamp.get("waiting") or [] if a != hero.id]
            self.store.put("camp", wait, wcamp)
        self.store.delete("camp_wait", hero.id)
        record = self._gremio_link(hero.id)
        if record and record.get("leader") != hero.id:
            self._gremio_leave_member(record, hero.id)
            for part in ("invited", "requests", "invites"):
                record[part] = [a for a in record.get(part) or [] if a != hero.id]
            self.store.put("gremio", record["id"], record)
        extra: dict[str, Any] = {}
        for space in OATH_HERO_SPACES:
            data = self.store.get(space, hero.id)
            if data is not None:
                extra[space] = data
                self.store.delete(space, hero.id)
        if extra:
            out["extra"] = extra
        return out

    def _fall_forever(self, hero: Hero, state: dict[str, Any], lines: list[str]) -> View:
        """A sworn hero lost a fight: the memorial, the unlink, the archive and the screen to start again (D-147).

        [ES]
        Qué hace: el héroe con 💀 cae para siempre. Anota su lugar en el 🪦 Salón ("fallen", número que nunca se reutiliza):
        nombre, clase, nivel, quién lo venció y dónde, fecha, días con 💀 y títulos. Lo saca de todo lo compartido
        (_oath_unlink), lo marca caído (Hero.oath "fell", "key", "memorial"), escribe el 📔 Diario y guarda el héroe ENTERO
        en "fallen_hero" (D-64: nada se borra; desde aquí _save lo escribe ahí). Deja en "reborn" lo que recibe el próximo
        héroe de la cuenta (⚙️ Opciones y lo comprado con 💎: diamantes, estandarte y acelerador) y saca la ficha de "hero":
        la cuenta vuelve a la creación con su idioma y su código. Avisa a los compañeros de campamento o gremio (_push_each) y
        publica HeroFellForever. Devuelve la pantalla "fallen" con las líneas de la pelea arriba.
        La llama: _end_combat (al final, con todo lo demás de la pelea ya hecho). Si cambia, afecta: la cuenta del que cae y
        nada más (tests/test_muerte_permanente_y_regeneracion.py).
        """
        now = self.clock.now()
        enemy = state.get("enemy") or {}
        eid = str(enemy.get("id", ""))
        seq = self.store.get("meta", "fallen_seq") or {"n": 0}
        seq["n"] = int(seq.get("n", 0)) + 1
        self.store.put("meta", "fallen_seq", seq)
        mid, key = f"f{seq['n']}", f"{hero.id}#{seq['n']}"
        self.store.put("fallen", mid, {
            "id": mid, "account": hero.id, "name": hero.name, "class_id": hero.class_id, "level": hero.level, "enemy": eid,
            "enemy_level": int(enemy.get("level", 1) or 1), "x": hero.x, "y": hero.y, "at": now,
            "oath_at": (hero.oath or {}).get("at"), "days": self._oath_days(hero, now), "titles": list(hero.titles),
            "archive": key})
        mates = self._fallen_mates(hero)
        kept = self._oath_unlink(hero)
        hero.activity = None
        self._journal(hero, "fell", e=eid)
        self.store.put("reborn", hero.id, {"options": dict(hero.options or {}), "gems": int(hero.gems or 0),
                                           "banner": hero.banner, "xp_boost_until": float(hero.xp_boost_until or 0.0),
                                           "from": key})
        hero.gems = 0                                   # 💎 bought with real money go to the account, not to the archive
        hero.oath = dict(hero.oath or {}, fell=now, key=key, memorial=mid)
        self.store.put("fallen_hero", key, {"hero": hero.to_dict(), "account": hero.id, "at": now, **kept})
        self.store.delete("hero", hero.id)
        self.bus.publish(HeroFellForever(hero.id, mid))
        name = hero.name
        edef = self.content.enemies.get(eid) or {}
        if mates:
            self._push_each(mates, lambda: View(
                kind="fallen_news", title=self.texts.t("oath.news_title"),
                body=[self.texts.t("oath.news_body", name=name, enemy=self.texts.t(edef["name_key"]) if edef else eid)],
                actions=[Action(id=HALL_ACTION, label=self.texts.t("oath.hall_button"))]))
        return self._fallen_view(hero, notice=self._join(lines))

    def _memorial_line(self, record: dict[str, Any]) -> str:
        """One line of the 🪦 hall, in the reader's language."""
        t = self.texts
        cdef = self.content.classes.get(record.get("class_id", ""), {})
        group = cdef.get("group", record.get("class_id", ""))
        cls = t.t(f"class_group.{group}.name") if cdef else "?"
        edef = self.content.enemies.get(record.get("enemy", "")) or {}
        return t.t("oath.hall_line", name=record.get("name", "?"), cls=cls, level=int(record.get("level", 1)),
                   enemy=t.t(edef["name_key"]) if edef else record.get("enemy", "?"), elevel=int(record.get("enemy_level", 1)),
                   place=self._place_label(int(record.get("x", 0)), int(record.get("y", 0))),
                   date=time.strftime("%Y-%m-%d", time.gmtime(float(record.get("at", 0.0)))), days=int(record.get("days", 0)))

    def _fallen_view(self, hero: Hero, notice: str | None = None) -> View:
        """The screen after the fall: the memorial, what stays with the account and ✨ Crear héroe nuevo / 🪦 Salón.

        [ES] Qué hace: lo que ve el jugador al caer con 💀 (y si vuelve a ver ese héroe en la misma llamada, _main_view): su
        línea del 🪦 Salón, que salió de su campamento y gremio, lo que sigue con la cuenta y los botones ✨ Crear héroe nuevo
        (cualquier botón sin héroe abre la creación) y 🪦 Salón de los caídos. La llaman: _fall_forever, _main_view, act() y
        text(). Si cambia, afecta: tests/test_muerte_permanente_y_regeneracion.py.
        """
        t = self.texts
        record = self.store.get("fallen", str((hero.oath or {}).get("memorial", ""))) or {}
        body = ([self._memorial_line(record), ""] if record else []) + [t.t("oath.fell_body"), t.t("oath.fell_left"),
                                                                         t.t("oath.fell_keep")]
        return View(kind="fallen", title=t.t("oath.fell_title", name=hero.name), body=body, notice=notice,
                    actions=[Action(id="newhero", label=t.t("oath.new_hero_button")),
                             Action(id=HALL_ACTION, label=t.t("oath.hall_button"))])

    def _hall_view(self, account_id: str, hero: Hero | None, notice: str | None = None) -> View:
        """🪦 Salón de los caídos (/caidos, /fallen): the last permadeath.hall_shown fallen heroes, the latest first.

        [ES] Qué hace: la lista de los que juraron la 💀 y cayeron, con nombre, clase, nivel, quién los venció, dónde, fecha y
        días con 💀. Se abre también sin héroe (después de caer): ↩️ Volver va a 💀 Muerte permanente si hay héroe, o a la
        creación si no. La llaman: act() ("fallen", antes de mirar si hay héroe). Si cambia, afecta: el Salón de todos.
        """
        t = self.texts
        records = sorted((r for _, r in self.store.items("fallen")),
                         key=lambda r: int(str(r.get("id", "f0"))[1:] or 0), reverse=True)
        shown = max(1, int(self._oath_cfg().get("hall_shown", 10)))
        body = [t.t("oath.hall_intro"), ""] if records else [t.t("oath.hall_empty")]
        body += [self._memorial_line(r) for r in records[:shown]]
        if len(records) > shown:
            body.append(t.t("oath.hall_more", n=len(records) - shown))
        back = Action(id="oath", label=t.t("menu.back")) if hero is not None else Action(id="newhero",
                                                                                          label=t.t("oath.new_hero_button"))
        return View(kind="fallen_hall", title=t.t("oath.hall_title"), body=body, actions=[back], notice=notice)

    def _oath_faq_values(self) -> dict[str, Any]:
        """❓ /d65: {oath_level} (up to which level it is sworn) and {oath_days} ("7, 30 y 100")."""
        top = int(self._oath_cfg().get("max_level", 0) or 0)
        return {"oath_level": top or self.content.balance["hero"]["max_level"],
                "oath_days": self._faq_and([int(e.get("days", 0)) for e in self._oath_titles_cfg()])}

    # ------------------------------------------------------------------ the next hero

    def _fallen_name_taken(self, key: str, account_id: str | None) -> bool:
        """True if a fallen hero of ANOTHER account had this name (the hall keeps it; its own player may use it again)."""
        return any(self._name_key(r.get("name", "")) == key and r.get("account") != account_id
                   for _, r in self.store.items("fallen"))

    def _reborn_apply(self, hero: Hero) -> None:
        """A new hero of an account whose hero fell: its ⚙️ Opciones and what was bought with 💎 come back (store "reborn")."""
        reborn = self.store.get("reborn", hero.id)
        if not reborn:
            return
        hero.options = dict(reborn.get("options") or {})
        hero.gems += int(reborn.get("gems", 0) or 0)
        hero.banner = reborn.get("banner") or hero.banner
        hero.xp_boost_until = max(float(hero.xp_boost_until or 0.0), float(reborn.get("xp_boost_until", 0.0) or 0.0))
        self.store.delete("reborn", hero.id)
