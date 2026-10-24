"""📜 Crafting orders between players (D-140, confirmed; how it was applied: D-335, provisional; 0.59): the service side.

A player asks an artisan to make a recipe (any recipe of a refining or crafting profession; since 0.62, D-339, also the 🎒
profession backpacks of the gathering professions) from 🏛️ Mercado → 📜 Pedidos de
fabricación (/pedidos, /orders), from a profession's screen they do not know, or from a recipe they cannot make:
- they pick the profession (/cf1), the recipe (/r1, the codes of the last recipe list, D-321) and the quantity (1 to
  craft_order.max_units);
- the materials: either they put them in (they leave the backpack into the order: escrow) or they pay coins so the artisan
  supplies them, at the recipe's reference value (items.yaml price of each input) or at a price they type ("m120");
- the labor fee (mano de obra), always apart (D-140): suggested craft_order.labor_per_energy × energy × (1 + rank ÷
  labor_rank_step) per make, changed with ×1/×2/×3 or typed ("50"), inside the market band (market.price_min to price_max
  times the suggested fee, D-26: the same band that stops passing coins to an alt).
The coins (labor, plus the materials when the artisan supplies them) are escrowed like a market buy order. Any artisan with the
profession, the rank, the 🎓 specialization and the 📚 book the recipe asks takes it from 🔨 Para hacer, from the station's list
or with /co1, at a station of that profession: it crafts at once (the artisan pays the ⚡ and, when the poster paid for them,
the materials), the item travels to the poster's 📦 Entregas (market.delivery_minutes) and a ✒️ masterwork keeps the artisan's
signature; the artisan gets the escrowed coins minus the market tax (market.tax, on everything it gets, burnt) and the normal
profession and hero xp. An order lasts craft_order.order_days; the poster cancels it while nobody took it; on expiry or cancel
the coins go back to the wallet and the materials to 📦 Entregas (ready at once). At most market.max_orders open orders each.

[ES]
Para qué sirve: los 📜 pedidos de fabricación entre jugadores (D-140, confirmada por el dueño en E-24: "le das al artesano los
    materiales, o le pagas para que los consiga, más su mano de obra; todo servicio entre jugadores se cobra aparte del costo
    de materiales y procesos"). Encargar (elegir oficio, receta, cantidad, quién pone los materiales y la mano de obra), la
    lista de pedidos que un artesano puede hacer, hacerlos (fabrica al momento y lo hecho viaja a 📦 Entregas), cancelar y
    vencer. La forma la eligió Claude en la capa simple (D-44), con la maquinaria de los 📜 encargos de reparación (D-333) y del
    🏛️ Mercado (D-320): D-335, provisional; preguntas E-278 a E-280. Es parte de GameService (una "mezcla", como RepairMixin),
    en su propio archivo para no agrandar game.py.
Documento de diseño: diseno/07-economia/profesiones.md §0.13; diseno/07-economia/economia.md §3.0, §5 y §7
Módulo: capa de servicios (M13 Economía: la custodia, la banda y el impuesto; M14 Oficios: quién fabrica, su experiencia y la
    ✒️ firma)
Depende de: content/balance.yaml (craft_order; market.tax, max_orders, price_min, price_max, delivery_minutes, per_page;
    professions.list_per_page), content/professions.yaml (recetas: profession, inputs, output, min_rank, energy, spec),
    content/items.yaml (price de los materiales, kind, req_level, la gemela ✒️ <id>_obra), content/locales/es_pedidos.yaml y
    en_pedidos.yaml (textos), engine.professions (masterwork_id, missing_for) y las ayudas de GameService (_recipes,
    _prof_catalog, _prof_rank, _prof_name, _knows, _recipe_name, _gear_name, _item_label, _item_list, _money, _gear_status,
    _gear_stats_text, _pspec_mark, _pspec_name, _pspec_recipe_ok, _pspec_recipe_lock, _pspec_masterwork, _book_missing,
    _book_lock_line, _stations_here, _masterwork_chance, _make_xp, _batch_prof_xp, _xp_mult, _give_xp, _prof_gain,
    _pay_energy, _story_event, _codes, _code_target, _push_each, _join, _seconds, _fmt_duration; de MarketMixin: _mkt_cfg,
    _mkt_tax, _mkt_credit, _mkt_box_add, _mkt_left, _mkt_fit, _mkt_log, _mkt_delivery_seconds)
Lo usan: engine/service/game.py (GameService hereda de esta clase): _idle_action (CRAFT_ORDER_ACTIONS: "cord", "cord:new",
    "cord:p:<oficio>:<página>", "cord:r:<receta>", "cord:d", "cord:q:<n>", "cord:m:<mats|coins>", "cord:l:<×>", "cord:ok",
    "cord:t:<página>", "cord:my:<id>", "cord:x:<id>"; también ocupado: son menús, y hacer revisa el lugar), text() (/cf1 /co1
    /cm1 con CRAFT_ORDER_CODE_RE; el texto suelto con un borrador abierto, "corder_open": _corder_typed), act() (borra
    "corder_open" con un botón que no es "cord…"), tick() (_corder_tick: los pedidos que vencen), COMMANDS (/pedidos, /orders),
    _recipe_code (/r1 de la lista de encargar: "receta|order|página" abre el borrador), _recipe_view (el botón 📜 Encargar de
    una receta que no puedes hacer), _station_view (_corder_station_lines: los pedidos que puedes hacer en esa estación, con
    /co1), _prof_detail_view (_corder_prof_lines y el botón 📜 Encargar de un oficio que no sabes) y _faq_values
    (_corder_faq_values); engine/service/market.py (_market_view: el botón 📜 Pedidos de fabricación; _market_draft_new borra
    "corder_open"); adapters/reports.py (market_lines lee "craft_*" de "market_log")
Eventos que publica: ItemCrafted (al hacer un pedido, como _make: la pieza normal y lo hecho)
Eventos que escucha: ninguno
Datos de los que es dueño:
    "craft_order" (clave el id del pedido, "p1", "p2"…; nunca se reutiliza): {"id", "by" (cuenta de quien encarga), "name" (su
        héroe), "rid" (la receta), "item" (lo que sale), "units" (cuántas unidades salen en total), "n" (veces), "prof" (oficio),
        "rank" (rango que pide), "mode" ("mats": los materiales los puso quien encarga; "coins": los consigue el artesano),
        "mats" (los materiales apartados, solo en "mats": {id: unidades} del total), "labor" (mano de obra por vez, 🥉),
        "mats_price" (lo que paga por los materiales de cada vez, solo en "coins"), "coins" (🥉 apartadas: (labor +
        mats_price) × n), "at", "until"}. Se BORRA al hacerse, cancelarse, vencer o quedar sin sentido (la receta ya no está):
        lo apartado vuelve en todos los casos menos al hacerse.
    "corder_open" (clave la cuenta): {"rid", "n", "mode", "labor", "mats_price", "page"}: el borrador mientras se arma; el texto
        suelto que escribes es la mano de obra ("50"), la cantidad ("x3") o el precio de los materiales ("m120"). Solo pantalla:
        act() lo borra con cualquier otro botón.
    "meta"/"craft_order": {"seq" (último número de pedido), "next_expire" (el pedido que vence antes)}.
    "gremio_codes" (de gremio.py) suma "corder_profs" (/cf1), "corder_take" (/co1) y "corder_mine" (/cm1); "recipes" (/r1) lleva
        "receta|order|página" cuando la última lista fue la de encargar. Solo pantalla.
    "market_log" (de market.py) suma "craft_posted", "craft_done", "craft_coins", "craft_tax", "craft_cancelled" y
        "craft_expired" para el informe de jugadores (adapters/reports.py).
Reglas que nunca se rompen:
    1. Nada se pierde (D-64): las monedas y los materiales de un pedido están en el pedido o vuelven (monedas a la bolsa,
       materiales a 📦 Entregas). Lo hecho siempre llega a 📦 Entregas, aunque la mochila esté llena.
    2. Nadie hace su propio pedido; un pedido se relee del almacén antes de hacerlo y se borra en la misma llamada.
    3. La mano de obra y el precio de los materiales van dentro de la banda del mercado (D-26: market.price_min a price_max
       veces su referencia): la misma traba que el 🏛️ Mercado contra pasar monedas a una cuenta alterna.
    4. El impuesto es un porcentaje (D-27): lo paga el artesano sobre todo lo que cobra y se quema (market.tax).
    5. A otra cuenta se le paga o se le entrega a través de su ficha guardada o de su 📦 Entregas (_mkt_credit, _mkt_box_add);
       al héroe que juega ahora, en memoria.
    6. Ningún texto visible se escribe aquí: todo sale de content/locales (es_pedidos.yaml y en_pedidos.yaml), y todo aviso a
       otro jugador se arma con _push_each (le llega en su idioma, D-250).
Si cambias esto, revisa:
    - Números: balance.yaml craft_order (y market: tax, max_orders, price_min, price_max, delivery_minutes); el registro de
      balance (diseno/03-personaje/balance.md, "los pedidos de fabricación") y la cascada C-38 del mapa de impacto
    - Pantallas y botones: "corders" (3 botones), "corder_profs", "corder_recipes", "corder_draft" (filas: cantidad, quién pone
      los materiales, mano de obra, ✅ Encargar y ↩️ Volver), "corder_take", "corder_mine"; 🏛️ Mercado suma 📜 Pedidos de
      fabricación (8 botones, HUB_KINDS); los ids "cord…" (64 bytes como máximo en Telegram); los códigos /cf, /co y /cm no
      pueden chocar con los de antes (tests/test_pedidos_de_fabricacion.py)
    - Pruebas: tests/test_pedidos_de_fabricacion.py; tests/test_mercado.py (el botón del 🏛️ Mercado)
"""

from __future__ import annotations

import math
import re
from typing import Any

from engine.core import ItemCrafted, Rng, hash_unit
from engine.hero import Hero
from engine.hero.gear import can_use, suits
from engine.messaging import Action, View
from engine.professions import masterwork_id, missing_for
from engine.professions import rules as profession_rules

# Button ids of 📜 Pedidos de fabricación (stable): "cord" (the hub) and "cord:<what>[:<args>]". [ES] Los botones de los pedidos.
CRAFT_ORDER_ACTIONS = ("cord",)
# /cf1 = the 1st profession of 📜 Encargar; /co1 = do the 1st order you can do; /cm1 = your 1st order. [ES] Los códigos.
CRAFT_ORDER_CODE_RE = re.compile(r"^/(cf|co|cm)_?(\d{1,2})(@\w+)?$")
# What a draft accepts as text: "50" (labor per make, 🥉), "50 x3" (and the quantity), "x3" (quantity), "m120" (materials).
LABOR_RE = re.compile(r"^\s*(\d{1,9})\s*(?:🥉)?\s*(?:[x×*]\s*(\d{1,3}))?\s*$")
QTY_RE = re.compile(r"^\s*[x×*]\s*(\d{1,3})\s*$")
MATS_RE = re.compile(r"^\s*m\s*(\d{1,9})\s*(?:🥉)?\s*$", re.IGNORECASE)
# The professions whose recipes can be ordered (content/professions.yaml branch). [ES] Las ramas que tienen recetas. D-339
# (0.62): también la recolección, que tiene las recetas de sus 🎒 mochilas de oficio (se hacen al fuego: stations.fire).
ORDER_BRANCHES = ("refine", "craft", "gather")


class CraftOrderMixin:
    """📜 Crafting orders between players (D-140, D-335). Mixed into GameService; uses its helpers (see the module's header).

    [ES]
    Qué es: encargar una receta a un artesano (materiales o monedas para que los consiga, más su mano de obra), la lista de
    pedidos que puedes hacer, hacerlos, cancelarlos y su vencimiento.
    Quién la usa: GameService (hereda de esta clase).
    Si cambia, afecta: la paga de los artesanos, las monedas que se queman y lo que se fabrica (C-38).
    """

    # ------------------------------------------------------------------ numbers and small helpers

    def _corder_cfg(self) -> dict[str, Any]:
        return self.content.balance.get("craft_order") or {}

    def _corder_days(self) -> int:
        return int(self._corder_cfg().get("order_days", 7))

    def _corder_cap(self) -> int:
        """Open crafting orders per player: the same number as the market's orders (market.max_orders), counted apart."""
        return int(self._mkt_cfg().get("max_orders", 10))

    def _corder_max_units(self) -> int:
        return max(1, int(self._corder_cfg().get("max_units", 5)))

    def _corder_tax_pct(self) -> int:
        return round(float(self._mkt_cfg().get("tax", 0.05)) * 100)

    def _corder_profs(self) -> list[str]:
        """The professions whose recipes can be ordered (refining and crafting, with recipes; since 0.62 the gathering ones
        too, for their 🎒 profession backpacks, D-339), in catalog order."""
        catalog = self._prof_catalog()
        with_recipes = {rdef["profession"] for rdef in self._recipes().values()}
        return [pid for pid, pdef in catalog.items() if pdef.get("branch") in ORDER_BRANCHES and pid in with_recipes]

    def _corder_recipe(self, rid: str | None) -> dict[str, Any] | None:
        """The recipe if it can be ordered now (not retired, of a refining or crafting profession that is not locked)."""
        rdef = self._recipes().get(rid or "")
        if not rdef or rdef.get("profession") not in self._corder_profs():
            return None
        return rdef

    def _corder_out(self, rdef: dict[str, Any]) -> tuple[str, int]:
        out_id, count = next(iter(rdef["output"].items()))
        return out_id, int(count)

    def _corder_mats_value(self, rdef: dict[str, Any]) -> int:
        """What the materials of one make are worth: the reference price of each input (items.yaml price) × how many."""
        return max(1, sum(int((self.content.items.get(i) or {}).get("price", 1)) * int(n) for i, n in rdef["inputs"].items()))

    def _corder_labor_ref(self, rdef: dict[str, Any]) -> int:
        """The suggested labor fee of one make: labor_per_energy × energy × (1 + rank ÷ labor_rank_step), at least 1 🥉.

        [ES] Qué hace: la mano de obra sugerida de una vez, por la energía y el tramo de la receta (la espada de nivel 45, 2 ⚡ y
        rango 45: 8 × 2 × 3,25 = 52 🥉; una pieza del rango 100 con 4 ⚡: 192 🥉). La llaman: el borrador y la banda.
        Si cambia, afecta: cuánto cobran los artesanos por su trabajo (registro de balance, C-38).
        """
        cfg = self._corder_cfg()
        step = max(1.0, float(cfg.get("labor_rank_step", 20)))
        value = float(cfg.get("labor_per_energy", 8)) * int(rdef.get("energy", 1)) * (1 + int(rdef.get("min_rank", 1)) / step)
        return max(1, int(round(value)))

    def _corder_band(self, ref: int) -> tuple[int, int]:
        """(lowest, highest) for a price whose reference is `ref`: the market band (D-26, market.price_min to price_max)."""
        cfg = self._mkt_cfg()
        low = max(1, int(ref * float(cfg.get("price_min", 0.25))))
        return low, max(low, int(math.ceil(ref * float(cfg.get("price_max", 10)))))

    def _corder_clamp(self, ref: int, value: int) -> int:
        low, high = self._corder_band(ref)
        return min(high, max(low, int(value)))

    def _corder_name(self, item_id: str) -> str:
        """"🟢🗡️ Espada …" for gear (with ✒️ when it is a masterwork), "🧪 Poción de vida" for the rest; "?" if gone."""
        item = self.content.items.get(item_id)
        if not item:
            return "?"
        return self._gear_name(item_id) if item.get("kind") == "gear" else self._item_label(item_id)

    def _corder_product(self, item_id: str, units: int) -> str:
        """"🟢🗡️ Espada de nivel 45 ×2": what an order makes, in units."""
        return self.texts.t("corder.product", item=self._corder_name(item_id), n=int(units))

    def _corder_inputs(self, rdef: dict[str, Any], times: int) -> dict[str, int]:
        return {item: int(n) * int(times) for item, n in rdef["inputs"].items()}

    # ------------------------------------------------------------------ storage

    def _corder_meta(self) -> dict[str, Any]:
        return self.store.get("meta", "craft_order") or {"seq": 0}

    def _corder_get(self, oid: str | None) -> dict[str, Any] | None:
        return self.store.get("craft_order", oid) if oid else None

    def _corder_all(self) -> list[dict[str, Any]]:
        return [order for _, order in self.store.items("craft_order")]

    def _corder_mine(self, account: str) -> list[dict[str, Any]]:
        """This account's open orders, oldest first. [ES] Los pedidos abiertos de una cuenta."""
        return sorted((o for o in self._corder_all() if o.get("by") == account), key=lambda o: float(o.get("at", 0)))

    def _corder_lock(self, hero: Hero, rdef: dict[str, Any]) -> str | None:
        """Why this hero cannot make this recipe for an order (profession, rank, 🎓 specialization, 📚 book), or None."""
        t = self.texts
        pid = rdef["profession"]
        rank = self._prof_rank(hero, pid)
        need = int(rdef.get("min_rank", 1))
        if not rank:
            return t.t("corder.need_prof", prof=self._prof_name(pid))
        if rank < need:
            return t.t("corder.need_rank", prof=self._prof_name(pid), need=need, rank=rank)
        if not self._pspec_recipe_ok(hero, rdef):
            return self._pspec_recipe_lock(hero, rdef)
        if self._book_missing(hero, rdef):
            return self._book_lock_line(hero, rdef)
        return None

    def _corder_can_take(self, hero: Hero, order: dict[str, Any]) -> bool:
        """True if this hero could make that order (its profession, rank, specialization and books; place and energy apart)."""
        rdef = self._corder_recipe(order.get("rid"))
        return rdef is not None and self._corder_lock(hero, rdef) is None

    def _corder_takeable(self, hero: Hero, pids: list[str] | None = None) -> list[dict[str, Any]]:
        """Other players' orders this hero can make (only of `pids` if given), the best paid first, then the oldest."""
        found = [o for o in self._corder_all() if o.get("by") != hero.id and (pids is None or o.get("prof") in pids)
                 and self._corder_can_take(hero, o)]
        return sorted(found, key=lambda o: (-int(o.get("coins", 0)), float(o.get("at", 0))))

    # ------------------------------------------------------------------ routing

    def _corder_action(self, hero: Hero, action_id: str) -> View:
        """Route a "cord…" button. Menus open while busy; making an order checks the place and the activity itself.

        [ES] Qué hace: reparte los botones de los pedidos de fabricación; antes cierra los vencidos (_corder_settle). La llama:
        _idle_action. Si cambia, afecta: los botones "cord…" (ids estables: solo se agregan).
        """
        self._corder_settle(hero)
        parts = action_id.split(":")
        what = parts[1] if len(parts) > 1 else ""
        arg = parts[2] if len(parts) > 2 else ""
        if what == "new":
            return self._corder_profs_view(hero)
        if what == "p" and arg:
            return self._corder_recipes_view(hero, arg, int(parts[3]) if len(parts) > 3 and parts[3].isdigit() else 0)
        if what == "r" and arg:
            return self._corder_draft_new(hero, arg)
        if what == "d":
            return self._corder_draft_view(hero)
        if what in ("q", "m", "l"):
            return self._corder_draft_set(hero, what, arg)
        if what == "ok":
            return self._corder_publish(hero)
        if what == "t":
            return self._corder_take_view(hero, int(arg) if arg.isdigit() else 0)
        if what == "my":
            return self._corder_my_view(hero, arg)
        if what == "x":
            return self._corder_cancel(hero, arg)
        return self._corder_view(hero)

    def _corder_code(self, hero: Hero, letter: str, n: int) -> View:
        """/cf2 opens the 2nd profession of 📜 Encargar; /co2 makes the 2nd order you can do; /cm2 opens your 2nd order."""
        t = self.texts
        self._corder_settle(hero)
        if letter == "cf":
            pid = self._code_target(hero, "corder_profs", n)
            if not pid:
                return self._corder_profs_view(hero, notice=t.t("corder.bad_code"))
            return self._corder_recipes_view(hero, pid)
        if letter == "co":
            oid = self._code_target(hero, "corder_take", n)
            if not oid:
                return self._corder_take_view(hero, notice=t.t("corder.bad_code"))
            return self._corder_take(hero, oid)
        oid = self._code_target(hero, "corder_mine", n)
        if not oid:
            return self._corder_view(hero, notice=t.t("corder.bad_code"))
        return self._corder_my_view(hero, oid)

    # ------------------------------------------------------------------ the hub and choosing what to order

    def _corder_mats_text(self, order: dict[str, Any], viewer: Hero) -> str:
        """Who puts the materials, said for whoever looks: the poster, or an artisan (with what it would spend)."""
        t = self.texts
        mine = order.get("by") == viewer.id
        if order.get("mode") == "mats":
            return t.t("corder.mats_put_mine") if mine else t.t("corder.mats_put_by", name=order.get("name", "?"))
        if mine:
            return t.t("corder.mats_paid_mine", price=self._money(int(order.get("mats_price", 0)) * int(order.get("n", 1))))
        rdef = self._corder_recipe(order.get("rid"))
        items = self._item_list(self._corder_inputs(rdef, int(order.get("n", 1)))) if rdef else "?"
        return t.t("corder.mats_yours", items=items)

    def _corder_view(self, hero: Hero, notice: str | None = None) -> View:
        """📜 Pedidos de fabricación: how it works, your open orders (/cm1) and how many of others' you can do.

        [ES]
        Qué hace: la entrada de los pedidos de fabricación (🏛️ Mercado → 📜 Pedidos de fabricación, /pedidos, /orders): cómo
        funcionan, tus pedidos abiertos contra el tope (cada uno con su código /cm1, lo que pediste, quién pone los materiales,
        lo apartado y cuándo vence) y cuántos pedidos de otros puedes hacer. Botones: 📜 Encargar, 🔨 Para hacer (n) y
        ↩️ Volver al 🏛️ Mercado. Si cambia, afecta: tests/test_pedidos_de_fabricacion.py.
        """
        t = self.texts
        mine = self._corder_mine(hero.id)
        now = self.clock.now()
        body = [t.t("corder.intro", days=self._corder_days(), tax=self._corder_tax_pct(),
                    time=self._fmt_duration(self._mkt_delivery_seconds())), "",
                t.t("corder.mine_title", n=len(mine), cap=self._corder_cap())]
        for n, order in enumerate(mine, 1):
            body.append(t.t("corder.mine_line", code=f"/cm{n}", product=self._corder_product(order["item"], order["units"]),
                            mats=self._corder_mats_text(order, hero), coins=self._money(int(order["coins"])),
                            left=self._mkt_left(float(order["until"]) - now)))
        self._codes(hero, "corder_mine", [o["id"] for o in mine])
        body.append(t.t("corder.mine_hint") if mine else t.t("corder.mine_none"))
        takeable = self._corder_takeable(hero)
        if takeable:
            body += ["", t.t("corder.take_line", n=len(takeable))]
        actions = [Action(id="cord:new", label=t.t("corder.new_button")),
                   Action(id="cord:t:0", label=t.t("corder.take_button", n=len(takeable))),
                   Action(id="mkt", label=t.t("menu.back"))]
        return View(kind="corders", title=t.t("corder.title"), body=body, actions=actions, notice=notice)

    def _corder_profs_view(self, hero: Hero, notice: str | None = None) -> View:
        """📜 Encargar: one line per profession with recipes (refining and crafting), with its code (/cf1) and its recipes."""
        t = self.texts
        profs = self._corder_profs()
        counts: dict[str, int] = {}
        for rdef in self._recipes().values():
            counts[rdef["profession"]] = counts.get(rdef["profession"], 0) + 1
        body = [t.t("corder.profs_intro"), ""]
        for n, pid in enumerate(profs, 1):
            known = t.t("corder.prof_known", rank=self._prof_rank(hero, pid)) if self._knows(hero, pid) else ""
            body.append(t.t("corder.prof_line", code=f"/cf{n}", prof=self._prof_name(pid), n=counts.get(pid, 0), known=known))
        self._codes(hero, "corder_profs", profs)
        return View(kind="corder_profs", title=t.t("corder.new_title"), body=body, notice=notice,
                    actions=[Action(id="cord", label=t.t("menu.back"))])

    def _corder_recipes_view(self, hero: Hero, pid: str, page: int = 0, notice: str | None = None) -> View:
        """The recipes of one profession to order, a list with codes (/r1, as D-321): the pieces you can wear first.

        [ES]
        Qué hace: la lista de lo que se le puede encargar a un oficio (todas sus recetas, también las que tú no puedes hacer):
        una línea por receta con su código /rN (el mismo de la lista de recetas de D-321: _recipe_code abre el borrador), la
        pieza o el tramo, el rango que pide y, en el equipo, si te sirve (✅, 🔒 nivel, ⚠️ clase). Primero el equipo que puedes
        usar ya y te sirve, después el que puedes usar, después el de más nivel (el más cercano primero); dentro de los dos
        primeros grupos y en lo que no es equipo, el de nivel (o tramo) más alto. De a
        professions.list_per_page por página; ➡️ Más y ↩️ Volver a 📜 Encargar.
        """
        t = self.texts
        if pid not in self._corder_profs():
            return self._corder_profs_view(hero)
        rows: list[tuple[tuple[int, int, int], str]] = []
        for order, (rid, rdef) in enumerate(self._recipes().items()):
            if rdef["profession"] != pid:
                continue
            out_id, _ = self._corder_out(rdef)
            item = self.content.items.get(out_id) or {}
            if item.get("kind") == "gear":                 # what you can wear now and suits you, then what you can wear, then later
                later = can_use(item, hero, self.content.classes, self.content.balance) == "level"
                group = 2 if later else (0 if suits(item, hero, self.content.classes, self.content.balance) else 1)
                level = int(item.get("req_level", 0))
                rows.append(((group, level if later else -level, order), rid))     # later: the nearest level first
            else:
                rows.append(((0, -int(rdef.get("min_rank", 1)), order), rid))
        rows.sort()
        per = max(1, int(self._prof_cfg().get("list_per_page", 8)))
        pages = max(1, (len(rows) + per - 1) // per)
        page %= pages
        shown = rows[page * per:(page + 1) * per]
        body = [t.t("corder.recipes_intro", prof=self._prof_name(pid)), t.t("corder.recipes_legend"), ""]
        codes = []
        for _, rid in shown:
            rdef = self._recipes()[rid]
            out_id, _ = self._corder_out(rdef)
            item = self.content.items.get(out_id) or {}
            codes.append(f"{rid}|order|{page}")
            level = (t.t("rlist.level", n=item["req_level"]) if item.get("kind") == "gear" and item.get("req_level")
                     else t.t("rlist.tier", n=int(rdef.get("min_rank", 1))))
            fit = self._mkt_fit(hero, out_id)
            body.append(t.t("corder.recipe_line", code=f"/r{len(codes)}", item=self._pspec_mark(rdef) + self._recipe_name(rid),
                            level=level, prof=self._prof_catalog()[pid].get("emoji", ""), need=int(rdef.get("min_rank", 1)),
                            fit=f" · {fit}" if fit else ""))
        self._codes(hero, "recipes", codes)
        body += ["", t.t("corder.recipes_hint")]
        if pages > 1:
            body.append(t.t("rlist.count", n=len(rows), page=page + 1, total=pages))
        actions = [Action(id=f"cord:p:{pid}:{page + 1}", label=t.t("corder.more"))] if pages > 1 else []
        actions.append(Action(id="cord:new", label=t.t("menu.back")))
        return View(kind="corder_recipes", title=t.t("corder.new_title"), body=body, actions=actions, notice=notice)

    # ------------------------------------------------------------------ the draft and posting

    def _corder_draft_new(self, hero: Hero, rid: str, page: int = 0) -> View:
        """Open the draft of an order for a recipe ("corder_open"): 1 make, your materials if you carry them all (else coins),
        the suggested labor fee and the materials at their reference value. A market draft that was open is dropped."""
        rdef = self._corder_recipe(rid)
        if rdef is None:
            return self._corder_profs_view(hero, notice=self.texts.t("corder.gone_recipe"))
        self.store.delete("market_open", hero.id)          # only one draft that reads typed numbers at a time
        mode = "coins" if missing_for(rdef, hero.backpack) else "mats"
        draft = {"rid": rid, "n": 1, "mode": mode, "labor": self._corder_labor_ref(rdef),
                 "mats_price": self._corder_mats_value(rdef), "page": int(page)}
        self.store.put("corder_open", hero.id, draft)
        return self._corder_draft_view(hero)

    def _corder_draft(self, hero: Hero) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
        """(draft, recipe) of the open draft, or (None, None) if there is none or its recipe can no longer be ordered."""
        draft = self.store.get("corder_open", hero.id)
        rdef = self._corder_recipe((draft or {}).get("rid"))
        if not draft or rdef is None:
            return None, None
        return draft, rdef

    def _corder_draft_set(self, hero: Hero, what: str, arg: str) -> View:
        """The draft's buttons: the quantity ("q"), who puts the materials ("m": mats or coins) and the labor fee ×N ("l")."""
        draft, rdef = self._corder_draft(hero)
        if draft is None:
            return self._corder_view(hero)
        if what == "q" and arg.isdigit():
            draft["n"] = max(1, min(int(arg), self._corder_max_units()))
        elif what == "m" and arg in ("mats", "coins"):
            draft["mode"] = arg
        elif what == "l" and arg.isdigit():
            ref = self._corder_labor_ref(rdef)
            draft["labor"] = self._corder_clamp(ref, ref * int(arg))
        self.store.put("corder_open", hero.id, draft)
        return self._corder_draft_view(hero)

    def _corder_total(self, draft: dict[str, Any]) -> int:
        """The coins an order escrows: (labor + the materials' price when the artisan supplies them) × the makes."""
        mats = int(draft.get("mats_price", 0)) if draft.get("mode") == "coins" else 0
        return (int(draft.get("labor", 0)) + mats) * int(draft.get("n", 1))

    def _corder_out_lines(self, hero: Hero, out_id: str) -> list[str]:
        """What the recipe makes, as the recipe screen says it (gear with its stats and whether it suits you, a potion…)."""
        t = self.texts
        item = self.content.items.get(out_id) or {}
        if item.get("kind") == "gear":
            lines = [t.t("prof.gear_out", slot=t.t(f"gear.slot.{item['slot']}"), type=t.t(f"gear.type.{item['type']}"),
                         level=item.get("req_level", 1), stats=self._gear_stats_text(item.get("stats", {}))),
                     self._gear_status(hero, item)]
            if masterwork_id(out_id) in self.content.items:
                lines.append(t.t("corder.masterwork_line"))
            return lines
        if item.get("kind") == "furniture":
            return [t.t("prof.furniture_out", desc=t.t(item["desc_key"]))]
        if item.get("food"):
            return [t.t("camp_prof.food_out", rations=item["food"])]
        if item.get("heal"):
            return [t.t("prof.heal_out", heal=round(item["heal"] * 100), tox=item.get("toxicity", 0))]
        if t.has(f"resources.use.{out_id}"):
            return [t.t("prof.material_out", use=t.t(f"resources.use.{out_id}"))]
        return []

    def _corder_draft_view(self, hero: Hero, notice: str | None = None) -> View:
        """The draft of a crafting order: what it makes, who can make it, how many, the materials (yours or paid), the labor
        fee with its band, what is set aside, what the artisan gets after the tax, the lifetime and how to type numbers.

        [ES]
        Qué hace: arma el pedido antes de publicarlo. Dice la pieza (o lo que sale) y si te sirve, quién la hace (oficio y
        rango, 🎓 y 📚 si los pide), la cantidad, los materiales (los pones tú: cuáles y cuánto llevas, ✅/❌; o los consigue el
        artesano: lo que pagas por ellos, su referencia y su banda), la mano de obra (sugerida y banda), lo que apartas, lo que
        cobra el artesano menos el impuesto, cuánto dura y cómo escribir los números. Botones en filas (layout): la cantidad
        (craft_order.qty_buttons), 🧺 Pongo yo / 🥉 Que los consiga, la mano de obra ×1 ×2 ×3 (craft_order.labor_buttons),
        ✅ Encargar y ↩️ Volver a la lista de ese oficio. La llaman: /r1 de la lista de encargar, el botón 📜 Encargar de una
        receta y los botones del borrador. Si cambia, afecta: tests/test_pedidos_de_fabricacion.py.
        """
        t = self.texts
        draft, rdef = self._corder_draft(hero)
        if draft is None:
            self.store.delete("corder_open", hero.id)
            return self._corder_view(hero, notice=notice)
        cfg = self._corder_cfg()
        pid = rdef["profession"]
        out_id, out_n = self._corder_out(rdef)
        n = int(draft["n"])
        labor_ref = self._corder_labor_ref(rdef)
        labor_low, labor_high = self._corder_band(labor_ref)
        mats_ref = self._corder_mats_value(rdef)
        mats_low, mats_high = self._corder_band(mats_ref)
        total = self._corder_total(draft)
        body = [self._pspec_mark(rdef) + self._recipe_name(draft["rid"])]
        body += self._corder_out_lines(hero, out_id)
        who = t.t("corder.who_line", prof=self._prof_name(pid), need=int(rdef.get("min_rank", 1)))
        extra = []
        if rdef.get("spec"):
            extra.append(t.t("corder.who_spec", spec=self._pspec_name(rdef["spec"])))
        need_books = self._corder_books(rdef)
        if need_books:
            extra.append(t.t("corder.who_books", prof=self._prof_name(pid), ranks=", ".join(str(r) for r in need_books)))
        body.append(who + "".join(extra))
        body += ["", t.t("corder.qty_line", n=n, max=self._corder_max_units(), product=self._corder_product(out_id, out_n * n))]
        inputs = self._corder_inputs(rdef, n)
        if draft["mode"] == "mats":
            body.append(t.t("corder.mats_mine_title"))
            for item_id, need in inputs.items():
                have = hero.backpack.get(item_id, 0)
                body.append(t.t("prof.have_line" if have >= need else "prof.lack_line", item=self._item_label(item_id),
                                have=have, need=need))
            missing = missing_for(rdef, hero.backpack, n)
            if missing:
                body.append(t.t("corder.mats_missing", items=self._item_list(missing)))
        else:
            body.append(t.t("corder.mats_coins_line", each=self._money(int(draft["mats_price"])),
                            total=self._money(int(draft["mats_price"]) * n), ref=self._money(mats_ref),
                            low=self._money(mats_low), high=self._money(mats_high)))
            body.append(t.t("corder.mats_coins_items", items=self._item_list(inputs)))
        body.append(t.t("corder.labor_line", each=self._money(int(draft["labor"])), total=self._money(int(draft["labor"]) * n),
                        ref=self._money(labor_ref), low=self._money(labor_low), high=self._money(labor_high)))
        tax = self._mkt_tax(total)
        body += ["", t.t("corder.escrow_line", total=self._money(total), gold=self._money(hero.gold)),
                 t.t("corder.pay_line", pay=self._money(total - tax), tax=self._money(tax), pct=self._corder_tax_pct()),
                 t.t("corder.life_line", days=self._corder_days(), time=self._fmt_duration(self._mkt_delivery_seconds())),
                 "", t.t("corder.typed_hint")]
        qtys = [Action(id=f"cord:q:{q}", label=t.t("corder.qty_button", n=q, mark=t.t("corder.mark_on") if q == n else ""))
                for q in (cfg.get("qty_buttons") or [1, 2, 5]) if int(q) <= self._corder_max_units()]
        modes = [Action(id="cord:m:mats", label=t.t("corder.mode_mats_button",
                                                    mark=t.t("corder.mark_on") if draft["mode"] == "mats" else "")),
                 Action(id="cord:m:coins", label=t.t("corder.mode_coins_button",
                                                     mark=t.t("corder.mark_on") if draft["mode"] == "coins" else ""))]
        labors = [Action(id=f"cord:l:{m}", label=t.t("corder.labor_button", m=m,
                                                     price=self._money(self._corder_clamp(labor_ref, labor_ref * int(m)))))
                  for m in (cfg.get("labor_buttons") or [1, 2, 3])]
        actions = qtys + modes + labors + [Action(id="cord:ok", label=t.t("corder.publish_button", total=self._money(total))),
                                           Action(id=f"cord:p:{pid}:{int(draft.get('page', 0))}", label=t.t("menu.back"))]
        layout = ([len(qtys)] if qtys else []) + [len(modes), len(labors), 1, 1]
        return View(kind="corder_draft", title=t.t("corder.draft_title"), body=body, actions=actions, notice=notice,
                    layout=layout)

    def _corder_books(self, rdef: dict[str, Any]) -> list[int]:
        """The 📚 book ranks a recipe asks of whoever makes it (recipe_tiers.books), lowest first; none for a no_book recipe
        (the 🎒 profession backpacks, D-339)."""
        if rdef.get("no_book"):
            return []
        return list(profession_rules.books_for(int(rdef.get("min_rank", 1)), self._books_cfg()))

    def _corder_typed(self, hero: Hero, text: str) -> View:
        """Text while a draft is open: "50" sets the labor fee of each make, "50 x3" also the quantity, "x3" the quantity and
        "m120" what you pay for the materials of each make (only when the artisan supplies them).

        [ES] Qué hace: los números escritos del borrador. Lo que sale de la banda (D-26) se corrige al borde y se avisa; un texto
        que no es un número avisa cómo escribirlo. La llama: GameService.text() con "corder_open" guardado.
        Si cambia, afecta: tests/test_pedidos_de_fabricacion.py.
        """
        t = self.texts
        draft, rdef = self._corder_draft(hero)
        if draft is None:
            self.store.delete("corder_open", hero.id)
            return self._corder_view(hero)
        qty = QTY_RE.match(text)
        mats = MATS_RE.match(text) if not qty else None
        labor = LABOR_RE.match(text) if not qty and not mats else None
        if not (qty or mats or labor):
            return self._corder_draft_view(hero, notice=t.t("corder.type_number"))
        notes = []
        if mats:
            if draft["mode"] != "coins":
                return self._corder_draft_view(hero, notice=t.t("corder.mats_typed_mode"))
            ref = self._corder_mats_value(rdef)
            wanted = int(mats.group(1))
            draft["mats_price"] = self._corder_clamp(ref, wanted)
            if draft["mats_price"] != wanted:
                low, high = self._corder_band(ref)
                notes.append(t.t("corder.band_fixed", low=self._money(low), high=self._money(high)))
        if labor:
            ref = self._corder_labor_ref(rdef)
            wanted = int(labor.group(1))
            draft["labor"] = self._corder_clamp(ref, wanted)
            if draft["labor"] != wanted:
                low, high = self._corder_band(ref)
                notes.append(t.t("corder.band_fixed", low=self._money(low), high=self._money(high)))
        count = qty.group(1) if qty else (labor.group(2) if labor else None)
        if count is not None:
            draft["n"] = max(1, min(int(count), self._corder_max_units()))
        self.store.put("corder_open", hero.id, draft)
        return self._corder_draft_view(hero, notice=self._join(notes))

    def _corder_publish(self, hero: Hero) -> View:
        """✅ Encargar: checks the cap, the band (D-26), the quantity and that you have the materials (yours) and the coins;
        then the materials and the coins go into the order (escrow) and artisans see it at once. From anywhere.

        [ES]
        Qué hace: publica el pedido. Revisa el tope de pedidos abiertos (market.max_orders), que la mano de obra y el precio de
        los materiales estén en la banda, la cantidad, los materiales (si los pones tú: salen de la mochila al pedido) y las
        monedas (se apartan). Se puede encargar desde cualquier lugar, como un 📜 encargo de reparación. La llama: ✅ Encargar.
        """
        t = self.texts
        draft, rdef = self._corder_draft(hero)
        if draft is None:
            self.store.delete("corder_open", hero.id)
            return self._corder_view(hero, notice=t.t("corder.gone_recipe"))
        if len(self._corder_mine(hero.id)) >= self._corder_cap():
            return self._corder_draft_view(hero, notice=t.t("corder.too_many", cap=self._corder_cap()))
        n = int(draft["n"])
        labor_ref, mats_ref = self._corder_labor_ref(rdef), self._corder_mats_value(rdef)
        bands_ok = self._corder_clamp(labor_ref, int(draft["labor"])) == int(draft["labor"]) and (
            draft["mode"] != "coins" or self._corder_clamp(mats_ref, int(draft["mats_price"])) == int(draft["mats_price"]))
        if not bands_ok or not 1 <= n <= self._corder_max_units():
            low, high = self._corder_band(labor_ref)
            return self._corder_draft_view(hero, notice=t.t("corder.band_fixed", low=self._money(low), high=self._money(high)))
        inputs = self._corder_inputs(rdef, n)
        if draft["mode"] == "mats":
            missing = missing_for(rdef, hero.backpack, n)
            if missing:
                return self._corder_draft_view(hero, notice=t.t("corder.mats_missing", items=self._item_list(missing)))
        total = self._corder_total(draft)
        if hero.gold < total:
            return self._corder_draft_view(hero, notice=t.t("corder.no_coins", price=self._money(total)))
        hero.gold -= total
        if draft["mode"] == "mats":
            for item_id, count in inputs.items():         # escrow: the materials leave the backpack into the order
                hero.backpack[item_id] -= count
                if hero.backpack[item_id] <= 0:
                    del hero.backpack[item_id]
        meta = self._corder_meta()
        meta["seq"] = int(meta.get("seq", 0)) + 1
        now = self.clock.now()
        until = now + self._seconds(self._corder_days() * 24 * 60)
        meta["next_expire"] = until if meta.get("next_expire") is None else min(float(meta["next_expire"]), until)
        self.store.put("meta", "craft_order", meta)
        out_id, out_n = self._corder_out(rdef)
        order = {"id": f"p{meta['seq']}", "by": hero.id, "name": hero.name, "rid": draft["rid"], "item": out_id,
                 "units": out_n * n, "n": n, "prof": rdef["profession"], "rank": int(rdef.get("min_rank", 1)),
                 "mode": draft["mode"], "mats": inputs if draft["mode"] == "mats" else {}, "labor": int(draft["labor"]),
                 "mats_price": int(draft["mats_price"]) if draft["mode"] == "coins" else 0, "coins": total, "at": now,
                 "until": until}
        self.store.put("craft_order", order["id"], order)
        self.store.delete("corder_open", hero.id)
        self._mkt_log(craft_posted=1)
        notice = t.t("corder.posted", product=self._corder_product(out_id, out_n * n), coins=self._money(total),
                     prof=self._prof_name(rdef["profession"]), need=int(rdef.get("min_rank", 1)), days=self._corder_days())
        return self._corder_view(hero, notice=notice)

    # ------------------------------------------------------------------ your order: see it and cancel it

    def _corder_my_view(self, hero: Hero, oid: str, notice: str | None = None) -> View:
        """One of your orders: what, how many, who puts the materials, the labor fee, what is set aside and when it expires;
        ❌ Cancelar pedido gives everything back."""
        t = self.texts
        order = self._corder_get(oid)
        if order is None or order.get("by") != hero.id:
            return self._corder_view(hero, notice=notice or t.t("corder.gone"))
        body = [self._corder_product(order["item"], order["units"]),
                t.t("corder.who_line", prof=self._prof_name(order.get("prof", "")), need=int(order.get("rank", 1))),
                self._corder_mats_text(order, hero)]
        if order.get("mode") == "mats":
            body.append(t.t("corder.my_mats", items=self._item_list(order.get("mats") or {})))
        body += [t.t("corder.my_labor", each=self._money(int(order["labor"])), total=self._money(int(order["labor"]) * int(order["n"]))),
                 t.t("corder.my_escrow", coins=self._money(int(order["coins"])),
                     left=self._mkt_left(float(order["until"]) - self.clock.now())),
                 t.t("corder.cancel_hint")]
        actions = [Action(id=f"cord:x:{oid}", label=t.t("corder.cancel_button")), Action(id="cord", label=t.t("menu.back"))]
        return View(kind="corder_mine", title=t.t("corder.my_title"), body=body, actions=actions, notice=notice)

    def _corder_cancel(self, hero: Hero, oid: str) -> View:
        """❌ Cancelar pedido: from anywhere, while nobody took it; the coins come back now, the materials to 📦 Entregas."""
        order = self._corder_get(oid)
        if order is None or order.get("by") != hero.id:
            return self._corder_view(hero, notice=self.texts.t("corder.gone"))
        return self._corder_view(hero, notice=self._corder_close(order, "cancelled", hero))

    def _corder_close(self, order: dict[str, Any], why: str, actor: Hero | None) -> str:
        """End an order without making it ("cancelled" by its owner, "expired" or "void" when its recipe is gone): the coins go
        back to the wallet and the materials to 📦 Entregas, ready at once (rule 1); the order is deleted. A cancel returns the
        owner's line; "expired" and "void" send the owner a notice in its language (rule 6)."""
        owner = order["by"]
        coins = int(order.get("coins", 0))
        mats = {k: int(v) for k, v in (order.get("mats") or {}).items() if int(v) > 0}
        self.store.delete("craft_order", order["id"])
        self._mkt_credit(owner, coins, actor)              # in memory if the owner is playing now, else its saved record
        now = self.clock.now()
        for item_id, count in mats.items():                 # never lost: the box keeps them until there is room (D-64)
            self._mkt_box_add(owner, {"good": item_id, "n": count, "at": now, "enchant": None, "sig": None, "from": "",
                                      "why": "expired" if why == "expired" else "returned", "told": True})
        self._mkt_log(**{f"craft_{'expired' if why == 'expired' else 'cancelled'}": 1})
        item, units = order.get("item", ""), int(order.get("units", 0))

        def back() -> str:                                 # built in the language in use (the owner's, inside _push_each)
            key = "corder.back_both" if mats else "corder.back_coins"
            return self.texts.t(key, coins=self._money(coins), items=self._item_list(mats) if mats else "")

        if why == "cancelled" and actor is not None and actor.id == owner:
            return self._join([self.texts.t("corder.cancelled"), back()]) or ""
        key = "expired" if why == "expired" else "void"
        self._push_each([owner], lambda: View(kind="corder_notice", title=self.texts.t(f"corder.push_{key}_title"),
                                              body=[self.texts.t(f"corder.push_{key}", product=self._corder_product(item, units)),
                                                    back()],
                                              actions=[Action(id="cord", label=self.texts.t("corder.market_button"))]))
        return ""

    def _corder_settle(self, actor: Hero | None) -> None:
        """Close every order whose time ran out (lazily, and from tick()); only scans when meta "next_expire" is due."""
        meta = self._corder_meta()
        due = meta.get("next_expire")
        now = self.clock.now()
        if due is None or now < float(due):
            return
        soonest: float | None = None
        for order in self._corder_all():
            if float(order.get("until", 0)) <= now:
                self._corder_close(order, "expired", actor)
            else:
                soonest = float(order["until"]) if soonest is None else min(soonest, float(order["until"]))
        meta = self._corder_meta()
        meta["next_expire"] = soonest
        self.store.put("meta", "craft_order", meta)

    def _corder_tick(self) -> None:
        """tick(): the orders that ran out give everything back (with a notice). [ES] Lo llama tick()."""
        self._corder_settle(None)

    # ------------------------------------------------------------------ the artisan: the list and making an order

    def _corder_take_entry(self, hero: Hero, order: dict[str, Any], code: str) -> str:
        """One line of an order an artisan could make: code, what, whose, profession and rank, the pay after the tax, the
        materials, the energy, and ✅ (you can) or 🔒 (you cannot yet)."""
        t = self.texts
        rdef = self._corder_recipe(order.get("rid")) or {}
        coins = int(order.get("coins", 0))
        energy = int(rdef.get("energy", 1)) * int(order.get("n", 1))
        return t.t("corder.take_entry", code=code, product=self._corder_product(order["item"], order["units"]),
                   name=order.get("name", "?"), prof=self._prof_name(order.get("prof", "")), need=int(order.get("rank", 1)),
                   pay=self._money(coins - self._mkt_tax(coins)), mats=self._corder_mats_text(order, hero), energy=energy,
                   fit=t.t("corder.fit_yes") if self._corder_can_take(hero, order) else t.t("corder.fit_no"))

    def _corder_take_view(self, hero: Hero, page: int = 0, notice: str | None = None) -> View:
        """🔨 Para hacer: other players' orders, the ones you can make first (✅, the best paid first; the rest 🔒), with /co1.

        [ES]
        Qué hace: la lista de pedidos de fabricación de los demás: lo que piden, de quién, qué oficio y rango, cuánto cobras (ya
        sin el impuesto), quién pone los materiales (o cuáles pones tú) y la ⚡; primero los que puedes hacer (✅) y, dentro, los
        que más pagan; cada uno con su código (/co1). Páginas de market.per_page; ➡️ Más y ↩️ Volver a 📜 Pedidos.
        """
        t = self.texts
        orders = [o for o in self._corder_all() if o.get("by") != hero.id]
        orders.sort(key=lambda o: (not self._corder_can_take(hero, o), -int(o.get("coins", 0)), float(o.get("at", 0))))
        per = max(1, int(self._mkt_cfg().get("per_page", 8)))
        pages = max(1, (len(orders) + per - 1) // per)
        page %= pages
        shown = orders[page * per:(page + 1) * per]
        body = [t.t("corder.take_intro", tax=self._corder_tax_pct()), ""]
        for n, order in enumerate(shown, page * per + 1):
            body.append(self._corder_take_entry(hero, order, f"/co{n}"))
        self._codes(hero, "corder_take", [""] * (page * per) + [o["id"] for o in shown])
        if not orders:
            body.append(t.t("corder.take_none"))
        else:
            body += ["", t.t("corder.take_hint")]
            if pages > 1:
                body.append(t.t("corder.page", n=page + 1, total=pages))
        actions = [Action(id=f"cord:t:{page + 1}", label=t.t("corder.more"))] if pages > 1 else []
        actions.append(Action(id="cord", label=t.t("menu.back")))
        return View(kind="corder_take", title=t.t("corder.take_title"), body=body, actions=actions, notice=notice)

    def _corder_take(self, hero: Hero, oid: str) -> View:
        """/co1: make another player's order now. The artisan pays the ⚡ (and the materials, when the poster paid for them),
        what comes out travels to the poster's 📦 Entregas (a ✒️ masterwork with the artisan's signature), the artisan gets the
        escrowed coins minus the market tax and the profession and hero xp, and the poster a notice in its language.

        [ES]
        Qué hace: hace un pedido de fabricación. Relee el pedido (regla 2); revisa que no sea tuyo, que la receta siga (si no,
        lo cierra y devuelve todo: regla 1), tu oficio, rango, 🎓 y 📚, que no estés ocupado, la estación de ese oficio, la ⚡ de
        todas las veces y, si los materiales los pones tú, que los lleves (si algo falta, avisa y no gasta nada). Después:
        borra el pedido, gastas la ⚡ (y tus materiales), fabrica justo lo pedido (sin la unidad de más del refinado; el equipo
        sortea la ✒️ obra maestra con tu probabilidad, como _make), lo hecho viaja a 📦 Entregas de quien encargó
        (market.delivery_minutes; la obra maestra con tu firma), cobras lo apartado menos el impuesto del mercado (market.tax,
        sobre todo lo que cobras: se quema), ganas la experiencia de oficio (por color, _batch_prof_xp) y de héroe de esas
        veces, cuenta para las misiones de fabricar (_story_event "craft") y publica ItemCrafted. Quien encargó recibe un aviso
        en su idioma (_push_each). La llaman: los códigos /co1. Si cambia, afecta: la paga de los artesanos
        (tests/test_pedidos_de_fabricacion.py).
        """
        t = self.texts
        order = self._corder_get(oid)
        if order is None:
            return self._corder_take_view(hero, notice=t.t("corder.gone"))
        if order.get("by") == hero.id:
            return self._corder_take_view(hero, notice=t.t("corder.own"))
        rdef = self._corder_recipe(order.get("rid"))
        if rdef is None:                                     # the recipe left the game: everything goes back (D-64)
            self._corder_close(order, "void", hero)
            return self._corder_take_view(hero, notice=t.t("corder.void"))
        pid = rdef["profession"]
        times = int(order.get("n", 1))
        energy = int(rdef.get("energy", 1)) * times
        inputs = self._corder_inputs(rdef, times)
        error = self._corder_lock(hero, rdef)
        if error is None and hero.activity:
            error = t.t("corder.busy")
        if error is None and pid not in self._stations_here(hero)[0]:
            error = t.t("corder.need_station", prof=self._prof_name(pid))
        if error is None and hero.energy < energy:
            error = t.t("corder.need_energy", energy=energy, have=hero.energy)
        if error is None and order.get("mode") == "coins":
            missing = missing_for(rdef, hero.backpack, times)
            if missing:
                error = t.t("corder.missing", items=self._item_list(missing))
        if error:
            return self._corder_take_view(hero, notice=error)
        self.store.delete("craft_order", oid)                # rule 2: gone before anything else can take it
        rank = self._prof_rank(hero, pid)
        self._pay_energy(hero, energy)
        if order.get("mode") == "coins":                     # the artisan supplies the materials (the poster paid for them)
            for item_id, count in inputs.items():
                hero.backpack[item_id] -= count
                if hero.backpack[item_id] <= 0:
                    del hero.backpack[item_id]
        out_id, out_n = self._corder_out(rdef)
        item = self.content.items[out_id]
        made = out_n * times
        twin = masterwork_id(out_id)
        masters = 0
        if item.get("kind") == "gear" and twin in self.content.items:      # D-116: ✒️ own draw, as _make
            rng = Rng(int(hash_unit(self.world_seed, hero.id, "corder_mw", oid, self.clock.now()) * 2**31))
            chance = self._masterwork_chance(hero, pid) + self._pspec_masterwork(hero, item)
            masters = sum(1 for _ in range(made) if rng.chance(chance))
        poster = order["by"]
        arrive = self.clock.now() + self._mkt_delivery_seconds()
        delivered: dict[str, int] = {}
        if made > masters:
            delivered[out_id] = made - masters
            self._mkt_box_add(poster, {"good": out_id, "n": made - masters, "at": arrive, "enchant": None, "sig": None,
                                       "from": hero.name, "why": "crafted", "told": False})
        if masters:                                          # the ✒️ masterwork travels with the artisan's signature
            delivered[twin] = masters
            self._mkt_box_add(poster, {"good": twin, "n": masters, "at": arrive, "enchant": None, "sig": hero.name,
                                       "from": hero.name, "why": "crafted", "told": False})
        coins = int(order.get("coins", 0))
        tax = self._mkt_tax(coins)
        hero.gold += coins - tax                             # the tax is burnt (D-27), like the market's
        self.bus.publish(ItemCrafted(hero.id, order["rid"], out_id, made))
        xp = self._make_xp(hero, rdef, rank) * times
        prof_xp = self._batch_prof_xp(hero, rdef, times)
        lines = [t.t("prof.gained", xp=int(xp * self._xp_mult(hero)), name=self._prof_name(pid), prof_xp=prof_xp)]
        lines += self._give_xp(hero, xp)
        lines += self._prof_gain(hero, pid, prof_xp)
        lines += self._story_event(hero, "craft", recipe=order["rid"], profession=pid, item=out_id, n=times)
        self._mkt_log(craft_done=1, craft_coins=coins, craft_tax=tax)
        artisan, name = hero.name, order.get("name", "?")
        time_text = self._fmt_duration(self._mkt_delivery_seconds())
        made_text = ", ".join(self._corder_product(good, count) for good, count in delivered.items())

        def done() -> View:                                  # built again in the poster's language (D-250)
            what = ", ".join(self._corder_product(good, count) for good, count in delivered.items())
            body = [self.texts.t("corder.push_done", name=artisan, items=what,
                                 time=self._fmt_duration(self._mkt_delivery_seconds()), coins=self._money(coins))]
            if masters:
                body.append(self.texts.t("corder.push_masterwork", name=artisan))
            return View(kind="corder_notice", title=self.texts.t("corder.push_done_title"), body=body,
                        actions=[Action(id="mkt:box", label=self.texts.t("market.box_button", n=len(self._mkt_box(poster))))])

        self._push_each([poster], done)
        mats_line = (t.t("corder.done_mats_yours", items=self._item_list(inputs)) if order.get("mode") == "coins"
                     else t.t("corder.done_mats_given", name=name))
        head = t.t("corder.done", name=name, items=made_text, pay=self._money(coins - tax),
                   tax=self._money(tax), energy=energy, mats=mats_line, time=time_text)
        if masters:
            lines.insert(0, t.t("corder.done_masterwork", n=masters, item=self._gear_name(twin), name=artisan))
        return self._corder_take_view(hero, notice=self._join([head] + lines))

    # ------------------------------------------------------------------ other screens' lines and buttons

    def _corder_station_lines(self, hero: Hero, pids: list[str]) -> list[str]:
        """The orders this hero can make at this station (its professions `pids`), up to craft_order.station_shown, with /co1;
        and how many more there are. Empty when there are none."""
        t = self.texts
        found = self._corder_takeable(hero, pids)
        if not found:
            return []
        shown = found[:max(1, int(self._corder_cfg().get("station_shown", 3)))]
        lines = ["", t.t("corder.station_title", n=len(found))]
        lines += [self._corder_take_entry(hero, order, f"/co{n}") for n, order in enumerate(shown, 1)]
        self._codes(hero, "corder_take", [o["id"] for o in shown])
        if len(found) > len(shown):
            lines.append(t.t("corder.station_more", n=len(found) - len(shown)))
        return lines

    def _corder_prof_lines(self, hero: Hero, pid: str) -> list[str]:
        """"📜 Pedidos de fabricación que puedes hacer: 2 — /pedidos" on a profession's screen (only when there are some)."""
        n = len(self._corder_takeable(hero, [pid]))
        return [self.texts.t("corder.prof_orders_line", n=n)] if n else []

    def _corder_recipe_action(self, rid: str) -> Action:
        """📜 Encargar a un artesano: the button of a recipe you cannot make (it opens the order's draft)."""
        return Action(id=f"cord:r:{rid}", label=self.texts.t("corder.recipe_button"))

    def _corder_faq_values(self) -> dict[str, Any]:
        """The numbers of ❓ /d64 ({corder_days}, {corder_units}, {corder_orders})."""
        return {"corder_days": self._corder_days(), "corder_units": self._corder_max_units(), "corder_orders": self._corder_cap()}
