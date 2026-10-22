"""🔧 Gear wear and repairs (D-139, confirmed; how it was applied: D-333, provisional; 0.57): the service side.

After every fight each worn piece loses durability (engine/hero/durability.py wear_fight): the fight's lines (and an automatic
batch's summary) say when a piece goes worn out (low_pct), damaged (0: no stats, still worn) or broken (0 in its last life).
🛡️ Equipo → 🔧 Reparar (/reparar, /repair) lists the worn pieces with their durability and a code each (/rp1); a piece's screen
offers three ways to repair it:
- 🔨 yourself, with the crafting profession that makes that type of piece (durability.repair_by), at its station (any bonfire,
  or your camp with its building), with rank ≥ the piece's level − durability.rank_margin, paying the base refined material
  and ⚡ (durability.material, material_step, energy); it gives profession and hero xp: the artisans' work (D-139);
- 🛒 the smith of any 🔥 bonfire, for coins (durability.npc_mult × the materials' value: always dearer than an artisan), so
  nobody is ever stuck without the profession;
- 📜 a repair order (D-140: every service between players is paid apart): the owner escrows durability.order_mult × the
  materials' value; any artisan with the profession and the rank takes it from 📜 Encargos (/ro1) at a station, puts the
  materials and the energy, gets the coins minus the market tax (market.tax) and the profession xp, and the owner's worn piece
  is repaired on the spot (a notice in its language). An order lasts durability.order_days; then the coins go back.
Every repair lowers the piece's maximum (durability.repair_loss); before the last one the screen asks again.

[ES]
Para qué sirve: el lado del servicio del desgaste del equipo (D-139, confirmada por el dueño en E-23: "el equipo se gasta, se
    repara y un día se rompe, con una duración generosa que dé trabajo a los artesanos"): los avisos al terminar una pelea, la
    pantalla 🔧 Reparar y la de cada pieza, las tres formas de reparar (uno mismo con su oficio, el herrero de la fogata y los
    📜 encargos de reparación entre jugadores, D-140) y el vencimiento de los encargos. La forma la eligió Claude en la capa
    simple (D-44): D-333, provisional; preguntas E-272 a E-274. Es parte de GameService (una "mezcla", como SquadsMixin), en su
    propio archivo para no agrandar game.py.
Documento de diseño: diseno/03-personaje/equipamiento.md §4 y §11; diseno/07-economia/profesiones.md §0.12 y §12;
    diseno/07-economia/economia.md §5 y §7
Módulo: capa de servicios (M4 Equipo: la durabilidad; M14 Oficios: quién repara; M13 Economía: el herrero, el impuesto y los
    encargos)
Depende de: engine/hero/durability.py (las cuentas), content/balance.yaml (durability; market.tax), content/items.yaml (price
    del material, type, req_level, masterwork), content/professions.yaml (las estaciones), content/locales/es_desgaste.yaml y
    en_desgaste.yaml (textos) y las ayudas de GameService (_gear_name, _forget_piece, _clamp_hp, _stations_here, _prof_rank,
    _knows, _prof_name, _pay_energy, _no_energy_notice, _make_xp, _give_xp, _xp_mult, _prof_gain, _item_list, _money,
    _codes, _code_target, _push_each, _load, _save, _mkt_credit, _mkt_tax, _mkt_cfg, _mkt_left, _seconds, _join)
Lo usan: engine/service/game.py (GameService hereda de esta clase): _end_combat (_wear_after_fight, también en las peleas
    automáticas: state["wear"] va al resumen del lote en _auto_combat), _idle_action (REPAIR_ACTIONS: "rpr", "rpr:<ranura>",
    "rpr!:<ranura>:<self|npc>[:ok]", "rpo:<ranura>[:ok]", "rpx:<ranura>", "rpl[:<página>]"; también ocupado: es un menú, y
    hacer revisa el lugar), text() (/rp1 y /ro1: REPAIR_CODE_RE), tick() (_repair_tick: los encargos que vencen), COMMANDS
    (/reparar, /repair), _worn_view (el botón 🔧 Reparar y las marcas), _item_view, _gear_view, _unequip_view, _hero_view
    (_wear_hero_lines), _shop_view (wear.shop_line), _prof_detail_view (_repair_prof_lines) y _faq_values (_repair_faq_values);
    engine/service/market.py (_mkt_label, la oferta y 🏷️ Vender: _dur_tag, _dur_line, _bag_wear_note) y engine/service/gremio.py
    (_armory_label: _dur_tag)
Eventos que publica: ninguno (ObjetoReparado y ObjetoDestruido del diseño, M4, quedan para cuando haya telemetría por eventos)
Eventos que escucha: ninguno
Datos de los que es dueño:
    "repair_order" (clave "<cuenta>|<ranura>": un encargo por pieza puesta): {"id", "by" (cuenta del dueño), "name" (su héroe),
        "slot", "item" (la pieza al encargar), "price" (🥉 apartadas), "at", "until"}. Se borra al hacerse, cancelarse, vencer o
        quedar sin sentido (la pieza ya no está puesta o ya está llena): en todos esos casos las monedas vuelven al dueño.
    "meta"/"repair": {"next_expire"}: el encargo que vence antes, así tick() no recorre todo a cada rato.
    "gremio_codes" (de gremio.py) suma "repair" (las ranuras de /rp1) y "repair_orders" (los encargos de /ro1): solo pantalla.
Reglas que nunca se rompen:
    1. Nada se pierde (D-64): las monedas de un encargo están en el encargo o vuelven al dueño (hecho por otro, cancelado,
       vencido o sin sentido). Una pieza dañada nunca se borra; solo se rompe en su última vida (durability.wear_fight).
    2. Nadie toma su propio encargo; un encargo se relee del almacén antes de hacerlo y se borra en la misma llamada.
    3. Reparar siempre baja el máximo (durability.repair_loss) y antes de la última reparación se pregunta otra vez.
    4. A otra cuenta se le paga o se le repara a través de su ficha guardada (_load, _save); al héroe que juega ahora, en memoria
       (como el 🏛️ Mercado, _mkt_credit).
    5. Ningún texto visible se escribe aquí: todo sale de content/locales (es_desgaste.yaml y en_desgaste.yaml), y todo aviso
       a otro jugador se arma con _push_each (le llega en su idioma, D-250).
Si cambias esto, revisa:
    - Números: balance.yaml durability (y market.tax para lo que cobra el artesano); el registro de balance
      (diseno/03-personaje/balance.md, "el equipo se gasta") y la cascada C-37 del mapa de impacto
    - Pantallas y botones: "repair" (hasta 4 botones), "repair_piece" (🔨, 🛒, 📜/❌ y ↩️), "repair_confirm", "repair_orders";
      🛡️ Equipo ("gear_worn") suma 🔧 Reparar: 5 botones con el 🌰 Recuerdo (EXTRA_BUTTON_KINDS en game.py); los códigos /rp y
      /ro no pueden chocar con los de antes (tests/test_desgaste_reparacion.py)
    - Pruebas: tests/test_desgaste_reparacion.py
"""

from __future__ import annotations

import re
from typing import Any

from engine.hero import Hero, durability
from engine.messaging import Action, View
from engine.world import mapgen

# Button ids of 🔧 Reparar (stable): the hub, a piece ("rpr:<slot>"), do it ("rpr!:<slot>:<self|npc>[:ok]"), post a repair order
# ("rpo:<slot>[:ok]"), cancel it ("rpx:<slot>") and the 📜 orders list ("rpl[:<page>]"). [ES] Los botones de 🔧 Reparar.
REPAIR_ACTIONS = ("rpr", "rpo:", "rpx:", "rpl")
# /rp1 = the 1st worn piece of 🔧 Reparar; /ro1 = take the 1st order of 📜 Encargos. [ES] Los códigos de 🔧 Reparar.
REPAIR_CODE_RE = re.compile(r"^/(rp|ro)_?(\d{1,2})(@\w+)?$")


class RepairMixin:
    """🔧 Gear wear and repairs (D-139, D-333). Mixed into GameService; uses its helpers (see the module's [ES] header).

    [ES]
    Qué es: los avisos de desgaste, la pantalla 🔧 Reparar, reparar (uno mismo, el herrero de la fogata) y los 📜 encargos de
    reparación entre jugadores.
    Quién la usa: GameService (hereda de esta clase).
    Si cambia, afecta: cuánto dura el equipo, la demanda de artesanos y las monedas que se queman (C-37).
    """

    # ------------------------------------------------------------------ numbers and small helpers

    def _dur_cfg(self) -> dict[str, Any]:
        return durability.cfg(self.content.balance)

    def _dur_tag(self, rec: dict[str, Any] | None) -> str:
        """"🔧 84/100", "⚠️ 🔧 18/100" (worn out) or "⚠️ 🔧 0/100 dañada" for a durability record (None = a new piece)."""
        bal = self.content.balance
        rec = rec or {"cur": durability.start_max(bal), "max": durability.start_max(bal), "rep": 0}
        top = durability.shown(rec.get("max", 0))
        if durability.damaged(rec):
            return self.texts.t("wear.tag_damaged", max=top)
        key = "wear.tag_low" if durability.is_low(rec, bal) else "wear.tag"
        return self.texts.t(key, cur=durability.shown(rec.get("cur", 0)), max=top)

    def _dur_left(self, rec: dict[str, Any] | None, item_id: str) -> str:
        """"5 reparaciones más" or "💔 última vida: sin reparaciones"."""
        left = durability.repairs_left(rec, self.content.items.get(item_id) or {}, self.content.balance)
        return self.texts.t("wear.left", n=left) if left else self.texts.t("wear.left_none")

    def _dur_line(self, rec: dict[str, Any] | None, item_id: str) -> str:
        """"🔧 Durabilidad: 84/96 · 4 reparaciones más" for a piece's screen."""
        bal = self.content.balance
        rec = rec or durability.new_record(item_id, bal)
        return self.texts.t("wear.line", cur=durability.shown(rec.get("cur", 0)), max=durability.shown(rec.get("max", 0)),
                            left=self._dur_left(rec, item_id))

    def _wear_state_lines(self, rec: dict[str, Any] | None, item_id: str) -> list[str]:
        """The ⚠️ lines of a piece: damaged, worn out, or in its last life (none for a healthy piece)."""
        bal = self.content.balance
        lines = []
        if durability.damaged(rec):
            lines.append(self.texts.t("wear.damaged_line"))
        elif durability.is_low(rec, bal):
            lines.append(self.texts.t("wear.low_line"))
        if rec and durability.repairs_left(rec, self.content.items.get(item_id) or {}, bal) <= 0:
            lines.append(self.texts.t("wear.last_life_line"))
        return lines

    def _bag_wear_note(self, hero: Hero, item_id: str, worst: bool = False) -> str:
        """" · 🔧 60/96" for the copy of a piece that equip would take (or, with `worst`, the one that leaves first); "" if new."""
        if not durability.wears(self.content.items.get(item_id)):
            return ""
        if worst:
            used = list((hero.bag_wear or {}).get(item_id) or [])
            rec = min(used, key=lambda r: (float(r.get("cur", 0)), float(r.get("max", 0)))) if used else None
        else:
            rec = durability.best_in_bag(hero, item_id, self.content.balance)
        if not rec or durability.is_new(rec, self.content.balance):
            return ""
        return " · " + self._dur_tag(rec)

    def _worn_alerts(self, hero: Hero) -> list[str]:
        """The slots whose worn piece is worn out or damaged (the ⚠️ of 🛡️ Equipo and the hero sheet)."""
        bal = self.content.balance
        out = []
        for slot in bal["gear"]["slots"]:
            rec = durability.worn_record(hero, slot, bal)
            if rec and durability.wears(self.content.items.get(rec["id"])) and (durability.damaged(rec) or durability.is_low(rec, bal)):
                out.append(slot)
        return out

    def _wear_hero_lines(self, hero: Hero) -> list[str]:
        """"⚠️ Equipo para reparar: 🗡️ Espada 0/100 — /reparar" on the hero sheet, only when something is worn out or damaged."""
        slots = self._worn_alerts(hero)
        if not slots:
            return []
        items = ", ".join(f"{self._gear_name(hero.gear[s])} {self._dur_tag(durability.worn_record(hero, s, self.content.balance))}"
                          for s in slots)
        return [self.texts.t("wear.hero_line", items=items)]

    def _needs_any_repair(self, hero: Hero) -> bool:
        """True if some worn piece is below its maximum and still takes repairs."""
        bal = self.content.balance
        for slot, item_id in (hero.gear or {}).items():
            item = self.content.items.get(item_id)
            rec = durability.worn_record(hero, slot, bal)
            if durability.wears(item) and durability.needs_repair(rec) and durability.repairs_left(rec, item, bal) > 0:
                return True
        return False

    def _repair_button_shown(self, hero: Hero) -> bool:
        """🛡️ Equipo shows 🔧 Reparar when something needs a repair, you have an open order, or there are orders you can take."""
        return self._needs_any_repair(hero) or bool(self._repair_mine(hero.id)) or bool(self._repair_takeable(hero))

    def _repair_button(self, hero: Hero) -> Action:
        key = "repair.button_alert" if self._worn_alerts(hero) else "repair.button"
        return Action(id="rpr", label=self.texts.t(key))

    def _repair_cost_text(self, item: dict[str, Any]) -> str:
        return self._item_list(durability.repair_materials(item, self.content.balance))

    # ------------------------------------------------------------------ wear after a fight

    def _wear_after_fight(self, hero: Hero, outcome: str | None) -> list[str]:
        """Wear the worn pieces after a fight (durability.wear_fight) and say what happened: ⚠️ worn out, ⚠️ damaged, 💔 broken.

        [ES]
        Qué hace: gasta el equipo puesto según cómo terminó la pelea y arma los avisos, una línea por tipo (las piezas se gastan
        juntas y suelen cruzar juntas): "⚠️ Desgaste alto: …" (una vez, al bajar del 20 %), "⚠️ Se dañó: …" (en 0: sigue puesta,
        sin bonos) y "💔 … se rompió para siempre" (en 0 sin reparaciones: se quita y, si era la última copia, se olvidan su ✨ y
        su ✒️ con _forget_piece). Si algo quedó sin bonos, la vida no pasa del máximo nuevo (_clamp_hp).
        La llama: _end_combat (toda pelea: a mano, automática, mazmorra, Guardián, defensa del campamento).
        Si cambia, afecta: los avisos de desgaste y lo que se rompe (tests/test_desgaste_reparacion.py).
        """
        bal = self.content.balance
        news = durability.wear_fight(hero, self.content.items, bal, outcome)
        lines: list[str] = []
        for kind in ("low", "damaged"):                   # one line per kind: the pieces wear together, so they cross together
            pieces = [f"{self._gear_name(item_id)} ({self._dur_tag(durability.worn_record(hero, slot, bal))})"
                      for slot, item_id, what in news if what == kind]
            if pieces:
                lines.append(self.texts.t(f"wear.{kind}", items=", ".join(pieces), n=len(pieces)))
        for _, item_id, kind in news:
            if kind == "broken":
                self._forget_piece(hero, item_id)          # the last copy takes its ✨ and ✒️ along
                lines.append(self.texts.t("wear.broken", item=self._gear_name(item_id)))
        if any(kind != "low" for _, _, kind in news):
            self._clamp_hp(hero)
        return lines

    # ------------------------------------------------------------------ routing

    def _repair_action(self, hero: Hero, action_id: str) -> View:
        """Route a 🔧 Reparar button. Menus open while busy; repairing checks the place and the activity itself.

        [ES] Qué hace: reparte los botones de 🔧 Reparar; antes cierra los encargos vencidos (_repair_settle). La llama:
        _idle_action. Si cambia, afecta: los botones "rpr…", "rpo:", "rpx:" y "rpl…" (ids estables: solo se agregan).
        """
        self._repair_settle(hero)
        head, _, rest = action_id.partition(":")
        parts = rest.split(":") if rest else []
        if head == "rpr" and not parts:
            return self._repair_view(hero)
        if head == "rpr":
            return self._repair_piece_view(hero, parts[0])
        if head == "rpr!" and len(parts) >= 2:
            return self._repair_do(hero, parts[0], parts[1], confirmed=len(parts) > 2 and parts[2] == "ok")
        if head == "rpo" and parts:
            return self._repair_post(hero, parts[0], confirmed=len(parts) > 1 and parts[1] == "ok")
        if head == "rpx" and parts:
            return self._repair_cancel(hero, parts[0])
        if head == "rpl":
            return self._repair_orders_view(hero, int(parts[0]) if parts and parts[0].isdigit() else 0)
        return self._repair_view(hero)

    def _repair_code(self, hero: Hero, letter: str, n: int) -> View:
        """/rp2 opens the 2nd worn piece of 🔧 Reparar; /ro2 takes the 2nd order of 📜 Encargos (D-333)."""
        self._repair_settle(hero)
        if letter == "rp":
            slot = self._code_target(hero, "repair", n)
            if slot is None or not hero.gear.get(slot):
                return self._repair_view(hero, notice=self.texts.t("repair.bad_code"))
            return self._repair_piece_view(hero, slot)
        oid = self._code_target(hero, "repair_orders", n)
        if oid is None:
            return self._repair_orders_view(hero, notice=self.texts.t("repair.bad_code"))
        return self._repair_take(hero, oid)

    # ------------------------------------------------------------------ the screens

    def _repair_view(self, hero: Hero, notice: str | None = None) -> View:
        """🔧 Reparar: every worn piece with its durability, repairs left and a code (/rp1); 📜 Encargos and ↩️ Volver.

        [ES]
        Qué hace: la pantalla de 🔧 Reparar (🛡️ Equipo → 🔧 Reparar, /reparar, /repair): cómo se gasta el equipo, cada pieza puesta
        con su código (/rp1), su durabilidad (⚠️ si está gastada o dañada), cuántas reparaciones le quedan y si tiene un 📜 encargo
        abierto; cuántos encargos de otros puedes hacer. Antes cierra tus encargos que ya no tienen sentido (la pieza ya no está
        puesta o está llena), con las monedas de vuelta. Botones: 📜 Encargos (n) y ↩️ Volver a 🛡️ Equipo.
        La llaman: el botón 🔧 Reparar, /reparar, /repair y los ↩️ Volver de sus pantallas. Si cambia, afecta: las pruebas de 🔧.
        """
        t = self.texts
        bal = self.content.balance
        cfg = self._dur_cfg()
        self._repair_own_check(hero)
        body = [t.t("repair.intro", loss=int(cfg.get("repair_loss", 4)), n=int(cfg.get("repairs", 5)),
                    mw=int(cfg.get("masterwork_repairs", cfg.get("repairs", 5)))), ""]
        worn = [slot for slot in bal["gear"]["slots"] if hero.gear.get(slot) in self.content.items]
        mine = {order["slot"] for order in self._repair_mine(hero.id)}
        for n, slot in enumerate(worn, 1):
            item_id = hero.gear[slot]
            rec = durability.worn_record(hero, slot, bal)
            body.append(t.t("repair.piece_line", code=f"/rp{n}", item=self._gear_name(item_id), tag=self._dur_tag(rec),
                            left=self._dur_left(rec, item_id), marks=t.t("repair.mark_order") if slot in mine else ""))
        self._codes(hero, "repair", worn)
        if not worn:
            body.append(t.t("repair.none_worn"))
        else:
            body += ["", t.t("repair.hint")]
        takeable = self._repair_takeable(hero)
        if takeable:
            body.append(t.t("repair.orders_line", n=len(takeable)))
        actions = [Action(id="rpl", label=t.t("repair.orders_button", n=len(takeable))), Action(id="gear", label=t.t("menu.back"))]
        return View(kind="repair", title=t.t("repair.title"), body=body, actions=actions, notice=notice)

    def _repair_piece_view(self, hero: Hero, slot: str, notice: str | None = None) -> View:
        """One worn piece: its durability, what a repair does, and who can repair it (🔨 you, 🛒 the smith, 📜 an order).

        [ES]
        Qué hace: la pantalla de reparar una pieza puesta: su durabilidad y las reparaciones que le quedan, el aviso si está
        dañada o gastada, qué hace la reparación (el máximo baja de N a M), el aviso de la última, la línea de la ✒️ obra maestra
        y las tres formas: 🔨 tú (oficio, rango, materiales y ⚡; dice si sabes el oficio y si te alcanza el rango), 🛒 el herrero
        de cualquier 🔥 fogata (monedas) y 📜 un encargo a un artesano (o el que ya abriste, con cuándo vence). Botones (4 como
        mucho): 🔨 Reparar yo (si sabes el oficio), 🛒 Herrero, 📜 Encargar o ❌ Cancelar encargo, y ↩️ Volver.
        La llaman: los códigos /rp1, "rpr:<ranura>" y el botón 🔧 Reparar de una pieza puesta (_item_view).
        """
        t = self.texts
        bal = self.content.balance
        cfg = self._dur_cfg()
        item_id = hero.gear.get(slot)
        item = self.content.items.get(item_id or "")
        if not item or not durability.wears(item):
            return self._repair_view(hero, notice=notice or t.t("repair.not_worn"))
        rec = durability.worn_record(hero, slot, bal) or durability.new_record(item_id, bal)
        left = durability.repairs_left(rec, item, bal)
        body = [self._gear_name(item_id), self._dur_line(rec, item_id)] + self._wear_state_lines(rec, item_id)
        if item.get("masterwork"):
            body.append(t.t("repair.masterwork_line", n=durability.max_repairs(item, bal), base=int(cfg.get("repairs", 5))))
        order = self._repair_order_of(hero.id, slot)
        actions: list[Action] = []
        can = durability.needs_repair(rec) and left > 0
        if not durability.needs_repair(rec):
            body.append(t.t("repair.state_full"))
        if can:
            after = durability.repaired(rec, bal)
            body.append(t.t("repair.after_line", old=durability.shown(rec["max"]), new=durability.shown(after["max"])))
            if left == 1:
                body.append(t.t("repair.last_warning"))
            pid = durability.repair_profession(item, bal) or ""
            need = durability.repair_rank(item, bal)
            rank = self._prof_rank(hero, pid) if pid else 0
            state = (t.t("repair.self_unknown", prof=self._prof_name(pid)) if not rank
                     else t.t("repair.self_low", rank=rank, need=need) if rank < need else t.t("repair.self_ok", rank=rank))
            npc = durability.npc_price(item, self.content.items, bal)
            price = durability.order_price(item, self.content.items, bal)
            body += ["", t.t("repair.options_title"),
                     t.t("repair.self_line", prof=self._prof_name(pid), need=need, items=self._repair_cost_text(item),
                         energy=int(cfg.get("energy", 1)), state=state),
                     t.t("repair.npc_line", price=self._money(npc))]
            if order:
                body.append(t.t("repair.order_open", price=self._money(int(order["price"])),
                                left=self._mkt_left(float(order["until"]) - self.clock.now())))
            else:
                body.append(t.t("repair.order_line", price=self._money(price), prof=self._prof_name(pid), need=need,
                                days=int(cfg.get("order_days", 7))))
            if rank:
                actions.append(Action(id=f"rpr!:{slot}:self", label=t.t("repair.self_button")))
            actions.append(Action(id=f"rpr!:{slot}:npc", label=t.t("repair.npc_button", price=self._money(npc))))
            actions.append(Action(id=f"rpx:{slot}", label=t.t("repair.cancel_button")) if order
                           else Action(id=f"rpo:{slot}", label=t.t("repair.order_button", price=self._money(price))))
        elif order:                                       # an order left over (the piece is full or out of repairs): cancel it
            actions.append(Action(id=f"rpx:{slot}", label=t.t("repair.cancel_button")))
        actions.append(Action(id="rpr", label=t.t("menu.back")))
        return View(kind="repair_piece", title=t.t("repair.piece_title"), body=body, actions=actions, notice=notice)

    def _repair_confirm_view(self, hero: Hero, slot: str, button_id: str, order: bool = False) -> View:
        """⚠️ Última reparación: asked once more before the last repair (or the order for it). [ES] La confirmación."""
        t = self.texts
        bal = self.content.balance
        item_id = hero.gear[slot]
        after = durability.repaired(durability.worn_record(hero, slot, bal) or durability.new_record(item_id, bal), bal)
        body = [t.t("repair.confirm", item=self._gear_name(item_id), max=durability.shown(after["max"]))]
        actions = [Action(id=button_id, label=t.t("repair.confirm_order_button" if order else "repair.confirm_button")),
                   Action(id=f"rpr:{slot}", label=t.t("menu.back"))]
        return View(kind="repair_confirm", title=t.t("repair.confirm_title"), body=body, actions=actions)

    # ------------------------------------------------------------------ repairing your own piece

    def _repair_checks(self, hero: Hero, slot: str) -> tuple[str | None, dict[str, Any], dict[str, Any] | None]:
        """(error text or None, the piece's item, its record) for a repair of the piece worn in `slot`."""
        t = self.texts
        bal = self.content.balance
        item_id = hero.gear.get(slot)
        item = self.content.items.get(item_id or "") or {}
        if not item_id or not durability.wears(item):
            return t.t("repair.not_worn"), item, None
        rec = durability.worn_record(hero, slot, bal)
        if not durability.needs_repair(rec):
            return t.t("repair.is_full"), item, rec
        if durability.repairs_left(rec, item, bal) <= 0:
            return t.t("repair.no_repairs"), item, rec
        return None, item, rec

    def _artisan_checks(self, hero: Hero, item: dict[str, Any]) -> str | None:
        """Why this hero cannot repair this piece with its profession here and now (rank, station, busy, materials, energy)."""
        t = self.texts
        bal = self.content.balance
        pid = durability.repair_profession(item, bal) or ""
        need = durability.repair_rank(item, bal)
        rank = self._prof_rank(hero, pid) if pid else 0
        if not rank:
            return t.t("repair.need_prof", prof=self._prof_name(pid) if pid else "?")
        if rank < need:
            return t.t("repair.need_rank", prof=self._prof_name(pid), need=need, rank=rank)
        if hero.activity:
            return t.t("repair.busy")
        stations, _ = self._stations_here(hero)
        if pid not in stations:
            return t.t("repair.need_station", prof=self._prof_name(pid))
        mats = durability.repair_materials(item, bal)
        missing = {m: n - hero.backpack.get(m, 0) for m, n in mats.items() if hero.backpack.get(m, 0) < n}
        if missing:
            return t.t("repair.missing", items=self._item_list(missing))
        if hero.energy < int(self._dur_cfg().get("energy", 1)):
            return self._no_energy_notice(hero)
        return None

    def _artisan_work(self, hero: Hero, item: dict[str, Any]) -> list[str]:
        """The artisan pays the materials and the energy and gets hero and profession xp (checked first: _artisan_checks)."""
        t = self.texts
        bal = self.content.balance
        pid = durability.repair_profession(item, bal) or ""
        energy = int(self._dur_cfg().get("energy", 1))
        rank = self._prof_rank(hero, pid)
        self._pay_energy(hero, energy)
        for material, n in durability.repair_materials(item, bal).items():
            hero.backpack[material] -= n
            if hero.backpack[material] <= 0:
                del hero.backpack[material]
        xp = self._make_xp(hero, {"energy": energy}, rank)
        prof_xp = durability.repair_xp(item, bal)
        lines = [t.t("prof.gained", xp=int(xp * self._xp_mult(hero)), name=self._prof_name(pid), prof_xp=prof_xp)]
        lines += self._give_xp(hero, xp)
        lines += self._prof_gain(hero, pid, prof_xp)
        return lines

    def _repair_do(self, hero: Hero, slot: str, how: str, confirmed: bool = False) -> View:
        """🔨 Reparar yo / 🛒 Herrero: repair the piece worn in `slot` now (asks again before the last repair).

        [ES]
        Qué hace: repara la pieza puesta. "self": con tu oficio (rango, estación, materiales y ⚡; da experiencia de oficio y de
        héroe). "npc": el herrero de la fogata (en cualquier 🔥 fogata, sin otra actividad, por monedas: durability.npc_mult ×
        el valor de los materiales; las monedas se queman). Antes de la última reparación pregunta otra vez. Si había un 📜
        encargo para esa pieza, se cierra y vuelven sus monedas. Si algo falta, avisa y no gasta nada.
        La llaman: los botones 🔨 Reparar yo y 🛒 Herrero (y ✅ Sí, reparar).
        Si cambia, afecta: cuánto cuesta reparar y la experiencia de los artesanos (tests/test_desgaste_reparacion.py).
        """
        t = self.texts
        bal = self.content.balance
        error, item, rec = self._repair_checks(hero, slot)
        if error:
            return self._repair_piece_view(hero, slot, notice=error)
        if how == "self":
            error = self._artisan_checks(hero, item)
        elif how == "npc":
            price = durability.npc_price(item, self.content.items, bal)
            if hero.activity:
                error = t.t("repair.busy")
            elif not mapgen.is_bonfire(hero.x, hero.y):
                error = t.t("repair.need_fire")
            elif hero.gold < price:
                error = t.t("repair.no_coins", price=self._money(price))
        else:
            return self._repair_piece_view(hero, slot)
        if error:
            return self._repair_piece_view(hero, slot, notice=error)
        if durability.repairs_left(rec, item, bal) == 1 and not confirmed:     # rule 3: the last repair asks again
            return self._repair_confirm_view(hero, slot, f"rpr!:{slot}:{how}:ok")
        item_id = hero.gear[slot]
        lines: list[str] = []
        if how == "self":
            materials = self._repair_cost_text(item)
            lines += self._artisan_work(hero, item)
        else:
            price = durability.npc_price(item, self.content.items, bal)
            hero.gold -= price                              # a sink: the smith's coins leave the game (D-27)
        fixed = durability.repaired(rec, bal)
        durability.set_worn(hero, slot, fixed, bal)
        left = self._dur_left(fixed, item_id)
        top = durability.shown(fixed["max"])
        if how == "self":
            head = t.t("repair.done_self", item=self._gear_name(item_id), max=top, left=left, items=materials,
                       energy=int(self._dur_cfg().get("energy", 1)))
        else:
            head = t.t("repair.done_npc", item=self._gear_name(item_id), price=self._money(price), max=top, left=left)
        lines = [head] + lines
        order = self._repair_order_of(hero.id, slot)
        if order:                                           # the order is no longer needed: its coins come back
            lines.append(self._repair_close(order, "cancelled", hero))
        return self._repair_piece_view(hero, slot, notice=self._join(lines))

    # ------------------------------------------------------------------ 📜 repair orders (D-140)

    def _repair_mine(self, account: str) -> list[dict[str, Any]]:
        """This account's open repair orders. [ES] Los encargos abiertos de una cuenta."""
        return [order for _, order in self.store.items("repair_order") if order.get("by") == account]

    def _repair_order_of(self, account: str, slot: str) -> dict[str, Any] | None:
        return self.store.get("repair_order", f"{account}|{slot}")

    def _repair_can_take(self, hero: Hero, order: dict[str, Any]) -> bool:
        """True if this hero knows the profession that repairs that piece with the rank it asks (place and materials apart)."""
        item = self.content.items.get(order.get("item", "")) or {}
        pid = durability.repair_profession(item, self.content.balance)
        return bool(pid) and self._prof_rank(hero, pid) >= durability.repair_rank(item, self.content.balance)

    def _repair_takeable(self, hero: Hero) -> list[dict[str, Any]]:
        """Other players' open orders this hero could take (its profession and rank)."""
        return [order for _, order in self.store.items("repair_order")
                if order.get("by") != hero.id and self._repair_can_take(hero, order)]

    def _repair_post(self, hero: Hero, slot: str, confirmed: bool = False) -> View:
        """📜 Encargar: escrow the order's coins and open a repair order for the piece worn in `slot` (one per piece).

        [ES]
        Qué hace: abre un 📜 encargo de reparación (D-140): aparta las monedas (durability.order_mult × el valor de los
        materiales) y deja la pieza a la vista de los artesanos en 📜 Encargos. Uno por pieza puesta; dura durability.order_days.
        Se puede encargar desde cualquier lugar (la pieza sigue puesta: el artesano la repara a distancia, como un transportista).
        Antes de la última reparación pregunta otra vez. La llaman: 📜 Encargar (y ✅ Sí, encargar).
        """
        t = self.texts
        bal = self.content.balance
        error, item, rec = self._repair_checks(hero, slot)
        if error:
            return self._repair_piece_view(hero, slot, notice=error)
        if self._repair_order_of(hero.id, slot):
            return self._repair_piece_view(hero, slot, notice=t.t("repair.already"))
        price = durability.order_price(item, self.content.items, bal)
        if hero.gold < price:
            return self._repair_piece_view(hero, slot, notice=t.t("repair.no_coins", price=self._money(price)))
        if durability.repairs_left(rec, item, bal) == 1 and not confirmed:
            return self._repair_confirm_view(hero, slot, f"rpo:{slot}:ok", order=True)
        hero.gold -= price
        now = self.clock.now()
        days = int(self._dur_cfg().get("order_days", 7))
        until = now + self._seconds(days * 24 * 60)
        order = {"id": f"{hero.id}|{slot}", "by": hero.id, "name": hero.name, "slot": slot, "item": hero.gear[slot],
                 "price": price, "at": now, "until": until}
        self.store.put("repair_order", order["id"], order)
        meta = self.store.get("meta", "repair") or {}
        meta["next_expire"] = until if meta.get("next_expire") is None else min(float(meta["next_expire"]), until)
        self.store.put("meta", "repair", meta)
        pid = durability.repair_profession(item, bal) or ""
        notice = t.t("repair.posted", item=self._gear_name(hero.gear[slot]), price=self._money(price), prof=self._prof_name(pid),
                     need=durability.repair_rank(item, bal), days=days)
        return self._repair_piece_view(hero, slot, notice=notice)

    def _repair_cancel(self, hero: Hero, slot: str) -> View:
        """❌ Cancelar encargo: from anywhere; the coins come back at once."""
        order = self._repair_order_of(hero.id, slot)
        if not order:
            return self._repair_piece_view(hero, slot, notice=self.texts.t("repair.gone"))
        return self._repair_piece_view(hero, slot, notice=self._repair_close(order, "cancelled", hero))

    def _repair_close(self, order: dict[str, Any], why: str, actor: Hero | None) -> str:
        """End an order without doing it ("cancelled" by its owner, "void" or "expired"): its coins go back to its owner (rule
        1) and the order is deleted. A cancel returns the owner's line; "void" and "expired" send the owner a notice in its
        language (also when the owner is the one playing: the coins came back without a button of theirs)."""
        price = int(order.get("price", 0))
        owner = order["by"]
        self.store.delete("repair_order", order["id"])
        self._mkt_credit(owner, price, actor)              # in memory if the owner is playing now, else its saved record
        name = self._gear_name(order["item"]) if order.get("item") in self.content.items else "?"
        if why == "cancelled" and actor is not None and actor.id == owner:
            return self.texts.t("repair.cancelled", price=self._money(price))
        key = "expired" if why == "expired" else "void"
        self._push_each([owner], lambda: View(kind="repair_notice", title=self.texts.t(f"repair.push_{key}_title"),
                                              body=[self.texts.t(f"repair.push_{key}", item=name, price=self._money(price))],
                                              actions=[Action(id="rpr", label=self.texts.t("repair.button"))]))
        return ""

    def _repair_own_check(self, hero: Hero) -> None:
        """Close this hero's orders that make no sense any more (the piece is no longer worn, is full or out of repairs)."""
        bal = self.content.balance
        for order in self._repair_mine(hero.id):
            slot = order.get("slot", "")
            item = self.content.items.get(order.get("item", "")) or {}
            rec = durability.worn_record(hero, slot, bal)
            if (hero.gear.get(slot) != order.get("item") or not durability.needs_repair(rec)
                    or durability.repairs_left(rec, item, bal) <= 0):
                self._repair_close(order, "void", hero)

    def _repair_settle(self, actor: Hero | None) -> None:
        """Close every repair order whose time ran out (lazily, and from tick()); only scans when meta "next_expire" is due."""
        meta = self.store.get("meta", "repair") or {}
        due = meta.get("next_expire")
        now = self.clock.now()
        if due is None or now < float(due):
            return
        soonest: float | None = None
        for _, order in list(self.store.items("repair_order")):
            if float(order.get("until", 0)) <= now:
                self._repair_close(order, "expired", actor)
            else:
                soonest = float(order["until"]) if soonest is None else min(soonest, float(order["until"]))
        meta["next_expire"] = soonest
        self.store.put("meta", "repair", meta)

    def _repair_tick(self) -> None:
        """tick(): the repair orders that ran out give their coins back (with a notice). [ES] Lo llama tick()."""
        self._repair_settle(None)

    def _repair_orders_view(self, hero: Hero, page: int = 0, notice: str | None = None) -> View:
        """📜 Encargos de reparación: other players' orders (the ones you can do first, ✅; the rest 🔒) with /ro1, and yours.

        [ES]
        Qué hace: la lista de encargos de reparación de los demás: la pieza y su durabilidad, de quién es, qué oficio y rango
        pide, cuánto cobras (ya sin el impuesto del mercado) y qué materiales gastas; primero los que puedes hacer (✅) y, dentro,
        los que más pagan; cada uno con su código (/ro1). Debajo, tus propios encargos. Páginas de market.per_page; botones
        ➡️ Más y ↩️ Volver a 🔧 Reparar. La llaman: 📜 Encargos (n) ("rpl", "rpl:<página>") y /ro1 con un aviso.
        """
        t = self.texts
        bal = self.content.balance
        tax_pct = round(float(self._mkt_cfg().get("tax", 0.05)) * 100)
        orders = [order for _, order in self.store.items("repair_order") if order.get("by") != hero.id
                  and order.get("item") in self.content.items]
        orders.sort(key=lambda o: (not self._repair_can_take(hero, o), -int(o.get("price", 0)), float(o.get("at", 0))))
        per = max(1, int(self._mkt_cfg().get("per_page", 8)))
        pages = max(1, (len(orders) + per - 1) // per)
        page %= pages
        body = [t.t("repair.orders_intro", energy=int(self._dur_cfg().get("energy", 1)), tax=tax_pct), ""]
        shown = orders[page * per:(page + 1) * per]
        for n, order in enumerate(shown, page * per + 1):
            item = self.content.items[order["item"]]
            pid = durability.repair_profession(item, bal) or ""
            owner = self.store.get("hero", order["by"]) or {}
            slot_rec = (owner.get("gear_wear") or {}).get(order["slot"])
            rec = slot_rec if slot_rec and slot_rec.get("id") == order["item"] else None
            price = int(order["price"])
            body.append(t.t("repair.order_entry", code=f"/ro{n}", item=self._gear_name(order["item"]), name=order.get("name", "?"),
                            tag=self._dur_tag(rec), prof=self._prof_name(pid), need=durability.repair_rank(item, bal),
                            pay=self._money(price - self._mkt_tax(price)), items=self._repair_cost_text(item),
                            fit=t.t("repair.fit_yes") if self._repair_can_take(hero, order) else t.t("repair.fit_no")))
        self._codes(hero, "repair_orders", [""] * (page * per) + [o["id"] for o in shown])
        if not orders:
            body.append(t.t("repair.orders_none"))
        else:
            body += ["", t.t("repair.orders_hint")]
            if pages > 1:
                body.append(t.t("repair.page", n=page + 1, total=pages))
        mine = self._repair_mine(hero.id)
        if mine:
            body += ["", t.t("repair.mine_title")]
            body += [t.t("repair.mine_entry", item=self._gear_name(o["item"]) if o.get("item") in self.content.items else "?",
                         price=self._money(int(o["price"])), left=self._mkt_left(float(o["until"]) - self.clock.now()))
                     for o in mine]
        actions = [Action(id=f"rpl:{page + 1}", label=t.t("repair.more"))] if pages > 1 else []
        actions.append(Action(id="rpr", label=t.t("menu.back")))
        return View(kind="repair_orders", title=t.t("repair.orders_title"), body=body, actions=actions, notice=notice)

    def _repair_take(self, hero: Hero, oid: str) -> View:
        """/ro1: do another player's repair order now: the artisan pays materials and ⚡, the owner's worn piece is repaired, the
        artisan gets the coins minus the market tax, and the owner a notice in its language (D-140).

        [ES]
        Qué hace: hace un encargo de reparación: relee el encargo (regla 2), revisa que no sea tuyo, tu oficio y rango, la
        estación, que no estés ocupado, los materiales y la energía (si algo falta, avisa y no gasta nada); revisa que la pieza
        del dueño siga puesta y necesite la reparación (si no, cierra el encargo y le devuelve las monedas: regla 1). Después:
        gastas materiales y ⚡, la pieza del dueño queda reparada en su ficha guardada (regla 4), cobras el precio menos el
        impuesto del mercado (market.tax: se quema), ganas experiencia de oficio y de héroe, y el dueño recibe un aviso en su
        idioma. La llaman: los códigos /ro1. Si cambia, afecta: la paga de los artesanos (tests/test_desgaste_reparacion.py).
        """
        t = self.texts
        bal = self.content.balance
        order = self.store.get("repair_order", oid)
        if not order or order.get("item") not in self.content.items:
            return self._repair_orders_view(hero, notice=t.t("repair.gone"))
        if order.get("by") == hero.id:
            return self._repair_orders_view(hero, notice=t.t("repair.own"))
        item = self.content.items[order["item"]]
        error = self._artisan_checks(hero, item)
        if error:
            return self._repair_orders_view(hero, notice=error)
        owner = self._load(order["by"])
        slot = order["slot"]
        rec = durability.worn_record(owner, slot, bal) if owner else None
        if (owner is None or owner.gear.get(slot) != order["item"] or not durability.needs_repair(rec)
                or durability.repairs_left(rec, item, bal) <= 0):
            self._repair_close(order, "void", hero)
            return self._repair_orders_view(hero, notice=t.t("repair.void"))
        self.store.delete("repair_order", oid)              # rule 2: gone before anything else can take it
        materials = self._repair_cost_text(item)
        lines = self._artisan_work(hero, item)
        price = int(order["price"])
        tax = self._mkt_tax(price)
        hero.gold += price - tax                             # the tax is burnt (D-27), like the market's
        fixed = durability.repaired(rec, bal)
        durability.set_worn(owner, slot, fixed, bal)
        self._save(owner)
        left_now = durability.repairs_left(fixed, item, bal)
        top = durability.shown(fixed["max"])
        name, item_id, artisan = order.get("name", "?"), order["item"], hero.name

        def done() -> View:                                  # built again in the owner's language (D-250)
            left = self.texts.t("wear.left", n=left_now) if left_now else self.texts.t("wear.left_none")
            return View(kind="repair_notice", title=self.texts.t("repair.push_done_title"),
                        body=[self.texts.t("repair.push_done", name=artisan, item=self._gear_name(item_id), max=top, left=left,
                                           price=self._money(price))],
                        actions=[Action(id="rpr", label=self.texts.t("repair.button"))])

        self._push_each([order["by"]], done)
        head = t.t("repair.done_order", item=self._gear_name(item_id), name=name, pay=self._money(price - tax),
                   tax=self._money(tax), items=materials, energy=int(self._dur_cfg().get("energy", 1)))
        return self._repair_orders_view(hero, notice=self._join([head] + lines))

    # ------------------------------------------------------------------ other screens' lines

    def _repair_prof_lines(self, hero: Hero, pid: str) -> list[str]:
        """"🔧 Reparas espada, daga, placas …" on the screen of a profession that repairs (durability.repair_by)."""
        bal = self.content.balance
        types = [typ for typ, who in (self._dur_cfg().get("repair_by") or {}).items() if who == pid]
        if not types:
            return []
        names = ", ".join(self.texts.t(f"gear.type.{typ}") for typ in types)
        return [self.texts.t("wear.prof_line", types=names, margin=int(self._dur_cfg().get("rank_margin", 10)),
                             n=len([o for o in self._repair_takeable(hero)
                                    if durability.repair_profession(self.content.items.get(o.get("item", "")) or {}, bal) == pid]))]

    def _repair_faq_values(self) -> dict[str, Any]:
        """The durability numbers of ❓ Dudas ({wear_low}, {repair_loss}, {repairs}, {repairs_mw}, {repair_margin},
        {repair_days})."""
        cfg = self._dur_cfg()
        return {"wear_low": round(float(cfg.get("low_pct", 0.2)) * 100), "repair_loss": int(cfg.get("repair_loss", 4)),
                "repairs": int(cfg.get("repairs", 5)), "repairs_mw": int(cfg.get("masterwork_repairs", cfg.get("repairs", 5))),
                "repair_margin": int(cfg.get("rank_margin", 10)), "repair_days": int(cfg.get("order_days", 7))}
