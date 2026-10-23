"""🏛️ Mercado: the player market (D-137, D-320): sell orders for gear and crafted goods, buy orders for resources.

One global book for every player (D-137). A seller lists a thing from the backpack (gear, potions, remedies, furniture,
cooked food, 💰 bags or 🪎 chests) at a unit price inside the item's price band (D-26); the units leave the backpack into
the order (escrow). Anyone buys at once from the category lists, cheapest first: the coins leave the buyer, the seller
gets them minus the market tax right away (a notice in its language), and the goods travel to the buyer's 📦 Entregas
box with an NPC transporter (market.delivery_minutes). A buyer asks for a resource (any material with a code: base,
terrain or refined) at a unit price: the coins are escrowed; anyone who carries that resource fills it, fully or in
part, gets the coins minus the tax at once, and the units travel to the asker's box. Orders expire after
market.order_days; on expiry or ❌ cancel what is left goes back (items to 📦 Entregas, ready at once; coins to the
wallet). The box is collected at any bonfire or at your camp, as far as the backpack has room: what does not fit stays.
D-326 (0.50): a 🗺️ map scroll (map_scroll.py) is sold one copy per order, category "maps", with its zones, author and region
travelling in the order and the box ("scroll"), at a free price (map_scroll.price_min to price_max instead of the band).

[ES]
Para qué sirve: el mercado entre jugadores que pidió el dueño el 21-oct-2026 ("los jugadores venden a otros jugadores el
    equipo que encuentran o fabrican; órdenes de venta para el equipo y lo fabricado; órdenes de compra para los recursos"),
    con la subasta global y los transportistas de D-137. Las reglas chicas las eligió Claude (D-320, provisional). Es parte
    de GameService (una "mezcla", como GremioMixin), en su propio archivo para no agrandar game.py.
Documento de diseño: diseno/07-economia/economia.md §3.0 (lo que está en el juego desde la 0.46) y §3 (el diseño completo)
Módulo: capa de servicios (M13 Economía: el primer libro de órdenes del juego)
Depende de: content/balance.yaml (bloque market; shop.sell_ratio para mostrar lo que paga el mercader; currency.bag_recipe,
    bag_coins y chest_recipe para el precio de referencia de 💰 bolsas y 🪎 cofres), content/items.yaml (kind, price, code,
    slot, req_level, masterwork), content/locales/es_mercado.yaml y en_mercado.yaml (textos), engine.hero (Hero) y las
    ayudas de GameService (_money, _gear_name, _gear_status, _gear_stats_text, _ench_defs, _ench_label, _forget_piece,
    _refill_belt, _fmt_duration, _seconds, _join, _load, _save, _push_each, _codes,
    _code_target, _upgrades_here, _camp_service, _main_view, _today); D-326: content/balance.yaml map_scroll (price_min,
    price_max) y las ayudas de MapScrollMixin (_scroll_item, _scroll_cfg, _scroll_find, _scroll_take, _scroll_add,
    _scroll_summary, _scroll_new); D-338 (0.62): las de BackpackMixin (engine/service/backpack.py: _bag_room, _bag_why,
    _bag_space_line, _pbag_hint) para 📦 Recoger: cada cosa entra hasta el tope de su tipo (o del equipo suelto)
Lo usan: engine/service/game.py (GameService hereda de esta clase): act() (borra "market_open" con cualquier botón que no sea
    del mercado; _idle_action manda MARKET_ACTIONS a _market_action), text() (los códigos /c1 /s1 /b07 /k1 /o1 con
    market_code, y el texto suelto con un borrador abierto: _market_typed), tick() (_market_tick: vencimientos y avisos de
    entregas que llegaron), COMMANDS (/mercado, /market), _shop_view (botón 🏛️ Mercado del 🛒 Mercader), _service_uses
    (botón 🏛️ Mercado al lado del 🏪 Puesto de trueque en ⚒️ Oficios de 🏘️ Servicios) y _faq_values (_market_faq_values);
    adapters/reports.py lee "market_log" (sección 9 del informe diario); D-335 (0.59): engine/service/craft_orders.py
    (CraftOrderMixin, los 📜 pedidos de fabricación) usa _mkt_cfg, _mkt_tax, _mkt_credit, _mkt_box_add, _mkt_box, _mkt_left,
    _mkt_fit, _mkt_log y _mkt_delivery_seconds: lo hecho viaja por 📦 Entregas con "why": "crafted"; los materiales
    devueltos, con "returned" o "expired"; y suma "craft_*" a "market_log"
Eventos que publica: ninguno (el evento OrderFilled del diseño, M13, queda para cuando haya telemetría por eventos)
Eventos que escucha: ninguno
Datos de los que es dueño:
    "market_order" (clave el id de la orden, "m1", "m2"…; nunca se reutiliza): {"id", "side": "sell" o "buy", "good" (id de
        items.yaml, o "bags" / "chests"), "n" (lo que queda), "n0" (lo publicado), "price" (precio por unidad en 🥉), "by"
        (cuenta), "name" (nombre del héroe al publicar), "at", "until" (vence), "x", "y" (dónde se publicó; para el
        transporte por distancia de más adelante), "enchant" y "sig" (el ✨ encantamiento y la ✒️ firma de la pieza: viajan
        con ella, como en la ⚔️ Armería), "scroll" (D-326: solo en un 🗺️ pergamino de mapa, siempre de a 1: su registro
        completo, {"id", "by", "center", "size", "zones", "at"}, que viaja con él), "wear" (D-333, 0.57: solo en el equipo con
        alguna copia usada: un registro de durabilidad por unidad, en el orden en que se venden, None = nueva; la próxima unidad
        es la primera)}. Una orden que se llena, se cancela o vence se BORRA (lo que quedaba ya volvió).
    "market_index" (clave "sell:<categoría>" o "buy"): {"ids": [[precio, id, good], …]} ordenado: ventas de la más barata a
        la más cara, compras de la que más paga a la que menos (a igual precio, la más vieja primero). Es solo un índice:
        se arregla solo si apunta a una orden que ya no está.
    "market_mine" (clave la cuenta): {"ids": [id, …]}: las órdenes activas de cada jugador (📋 Mis órdenes y el tope).
    "market_box" (clave la cuenta): {"items": [{"good", "n", "at" (cuándo llega), "enchant", "sig", "from" (de quién),
        "why" ("bought", "filled", "returned", "expired"; D-335: "crafted", lo que hizo un artesano por un pedido de
        fabricación), "told" (ya se avisó que llegó), "coins" (solo si son monedas),
        "scroll" (D-326: el 🗺️ pergamino que llega, con sus zonas), "wear" (D-333: la durabilidad de cada unidad, como en la
        orden)}]}: 📦 Entregas. Se borra al quedar vacía.
    "market_open" (clave la cuenta): {"side", "good", "price", "n", "scroll" (D-326: el id del 🗺️ pergamino que se vende)}:
        el borrador de una orden mientras se arma; el texto suelto que escribes es su precio (y "x5", su cantidad). Solo
        pantalla: act() lo borra con cualquier otro botón.
    "market_log" (clave el día, _today()): {"trades", "units", "coins", "tax", "sell_orders", "buy_orders", "cancelled",
        "expired"}: la cuenta del día para el informe diario (adapters/reports.py). Se guardan market.log_days días.
    "meta"/"market": {"seq" (último número de orden), "next_expire" (la orden que vence antes), "next_due" (la entrega que
        llega antes sin avisar)}: así tick() no recorre todo a cada rato.
    "gremio_codes" (de gremio.py) suma "mkt_offers", "mkt_sell", "mkt_fill" y "mkt_mine": el orden de las listas con /c1, /s1,
        /k1 y /o1 (solo pantalla).
Reglas que nunca se rompen:
    1. Nada se pierde (D-64): una unidad o una moneda de una orden está en la orden, en 📦 Entregas, en la mochila o en la
       bolsa de alguien; vencer o cancelar devuelve todo lo que queda; recoger con la mochila llena deja el resto en la caja.
    2. Una orden no se llena dos veces: la revisión y la escritura van en la misma llamada (un solo proceso del motor) y
       siempre se relee la orden del almacén antes de tocarla.
    3. Nadie se compra ni se vende a sí mismo; el precio va dentro de la banda de su objeto (D-26: de market.price_min a
       market.price_max veces su precio de referencia). La excepción es el 🗺️ pergamino de mapa (D-311.5, "al precio que
       quiera"; D-326): su banda es map_scroll.price_min a price_max (de 1 🥉 a 1 🥇).
    4. El impuesto es un porcentaje (D-27): lo paga quien cobra (el vendedor de una orden de venta, quien llena un pedido de
       compra) y se quema (sumidero).
    5. A otra cuenta se le paga a través de su ficha guardada; si es el héroe que juega ahora, en memoria (como
       _raid_reward), para que su _save no lo pise.
    6. Ningún texto visible se escribe aquí: todo sale de content/locales (es_mercado.yaml y en_mercado.yaml), y todo aviso
       a otro jugador se arma con _push_each (le llega en su idioma, D-250).
    7. Una pieza con ✨ o ✒️ que el comprador ya tiene con otro encantamiento o firma no entra a su mochila: espera en la caja
       (las copias de una pieza comparten esos datos, como en la ⚔️ Armería, D-290).
    8. D-326: un 🗺️ pergamino de mapa se vende de a uno (cada copia tiene sus zonas); sale de la mochila y vuelve a ella solo
       por _scroll_take y _scroll_add (map_scroll.py), así la mochila sigue contando lo que hay en Hero.map_scrolls.
    9. D-333 (0.57): la durabilidad viaja con cada pieza (engine/hero/durability.py): al publicar salen primero las copias más
       gastadas (take_copies), cada unidad lleva su registro en "wear" hasta 📦 Entregas, y al recogerla entra a la mochila con
       él (put_back). Quien compra ve la durabilidad de la próxima unidad ("🔧 80/96") en la lista y en la oferta.
Si cambias esto, revisa:
    - Números: balance.yaml market (tax, delivery_minutes, order_days, max_orders, max_units, price_min, price_max,
      price_buttons, ask_buttons, per_page, log_days); el registro de balance (diseno/03-personaje/balance.md)
    - Pantallas y botones: HUB_KINDS ("market" y "market_cats": hasta 8 botones, "market" con 📜 Pedidos de fabricación desde la
      0.59; "market_cats" 9 desde la 0.50 con 🗺️ Mapas y 10 desde la 0.62 con 🎒 Mochilas de oficio,
      EXTRA_BUTTON_KINDS), el layout del borrador (filas de precio y
      cantidad, ✅ Publicar y ↩️ Volver a lo ancho) y los ids "mkt…" (64 bytes como máximo en Telegram)
    - Servicio: engine/service/game.py (los ganchos de "Lo usan"); adapters/reports.py (sección 9)
    - Mapa de impacto: diseno/01-plataforma/mapa-de-impacto.md (M13 y la cascada C-32)
    - Horas (0.58, D-124, D-334): el detalle de una orden dice a qué hora vence en la zona horaria de quien mira (_clock de
      engine/service/world_time.py); la orden vence a la misma hora para todos ("until", segundos UTC)
    - Pruebas: tests/test_mercado.py; tests/test_fogata_ordenada.py (el 🛒 Mercader con 🏛️ Mercado); tests/test_pergamino_mapa.py
      (el 🗺️ pergamino en el mercado); tests/test_desgaste_reparacion.py (la durabilidad que viaja, D-333);
      tests/test_pedidos_de_fabricacion.py (los pedidos de fabricación usan la custodia, el impuesto, la banda y 📦 Entregas)
"""

from __future__ import annotations

import math
import re
from typing import Any

from engine.hero import Hero, durability
from engine.hero.gear import can_use, suits
from engine.messaging import Action, View
from engine.world import mapgen

# Button ids of the market: "mkt" (the hub) and "mkt:<what>[:<args>]". [ES] Los botones del mercado (ids estables).
MARKET_ACTIONS = ("mkt",)
# The categories of 🛍️ Comprar, in button order. [ES] Las categorías de las órdenes de venta, en el orden de sus botones
# (ids estables: van en los botones "mkt:cat:<categoría>" y en las claves del índice "sell:<categoría>").
MARKET_CATEGORIES = ("weapons", "armor", "jewels", "remedies", "furniture", "food", "coinbags",
                     "maps",         # D-326 (0.50): 🗺️ Mapas, the 🧭 Explorador's map scrolls (one per order, each with its zones)
                     "packs")        # D-339 (0.62): 🎒 Mochilas, the gathering professions' profession backpacks (kind prof_bag)
# Goods that are coins kept apart (Hero.bags, Hero.chests), not backpack items. [ES] 💰 bolsas y 🪎 cofres.
COIN_GOODS = ("bags", "chests")
# Typed codes of the market lists. [ES] /c1: una oferta de 🛍️ Comprar; /s1: algo tuyo de 🏷️ Vender; /b07: pedir el recurso con
# el código 07 (el mismo de 📦 Recursos); /k1: un pedido de 📥 Pedidos de compra para venderle; /o1: una de 📋 Mis órdenes.
MARKET_CODE_RE = re.compile(r"^/(c|s|b|k|o)_?(\d{1,3})(@\w+)?$")
MARKET_CODE_KINDS = {"c": "mkt_offers", "s": "mkt_sell", "b": "ask", "k": "mkt_fill", "o": "mkt_mine"}
# What a draft accepts as text: "25" (price in 🥉), "25 x3" or "25x3" (price and quantity), "x3" (quantity only).
PRICE_RE = re.compile(r"^\s*(\d{1,9})\s*(?:🥉)?\s*(?:[x×*]\s*(\d{1,6}))?\s*$")
QTY_RE = re.compile(r"^\s*[x×*]\s*(\d{1,6})\s*$")


def market_code(low: str) -> tuple[str, int] | None:
    """("c" | "s" | "b" | "k" | "o", number) for a typed market code ("/c2", "/b07", "/o_1"), else None.

    [ES] Qué hace: reconoce los códigos que se escriben en las listas del mercado. La llama: GameService.text().
    Si cambia, afecta: qué códigos entiende el mercado (no deben chocar con /e, /q, /v, /d, /j, /p, /g, /m, /f, /z, /a, /t, /r
    ni /ir, /go: tests/test_mercado.py lo revisa).
    """
    match = MARKET_CODE_RE.match(low)
    return (match.group(1), int(match.group(2))) if match else None


class MarketMixin:
    """🏛️ Mercado (D-137, D-320). Mixed into GameService; uses its helpers (see the module's [ES] header).

    [ES]
    Qué es: el mercado entre jugadores, con órdenes de venta, pedidos de compra, 📋 Mis órdenes y 📦 Entregas.
    Quién la usa: GameService (hereda de esta clase).
    Si cambia, afecta: el comercio entre jugadores y las monedas que entran y salen (C-32 del mapa de impacto).
    """

    # ------------------------------------------------------------------ config and goods

    def _mkt_cfg(self) -> dict[str, Any]:
        return self.content.balance.get("market", {})

    def _mkt_delivery_seconds(self) -> float:
        """How long an NPC transporter takes to bring what you bought (market.delivery_minutes, D-137)."""
        return self._seconds(float(self._mkt_cfg().get("delivery_minutes", 30)))

    def _mkt_order_seconds(self) -> float:
        """How long an order stays up (market.order_days)."""
        return self._seconds(float(self._mkt_cfg().get("order_days", 7)) * 24 * 60)

    def _mkt_category(self, good: str) -> str | None:
        """The 🛍️ Comprar category of a good that can be put up for sale, or None (materials go by buy orders)."""
        if good in COIN_GOODS:
            return "coinbags"
        item = self.content.items.get(good) or {}
        kind = item.get("kind")
        if kind == "gear":
            slot = item.get("slot")
            return "weapons" if slot == "arma" else "jewels" if slot == "joya" else "armor"
        if kind in ("potion", "bandage"):
            return "remedies"
        if kind == "furniture":
            return "furniture"
        if kind == "food":
            return "food"
        if kind == "map_scroll":                         # D-326: 🗺️ map scrolls
            return "maps"
        if kind == "prof_bag":                           # D-339 (0.62): 🎒 profession backpacks (only the ones not on)
            return "packs"
        return None

    def _mkt_is_resource(self, good: str) -> bool:
        """True for what buy orders ask for: any material with a resource code (base, terrain, refined, fish…)."""
        item = self.content.items.get(good) or {}
        return item.get("kind") == "material" and bool(item.get("code"))

    def _mkt_bag_price(self) -> int:
        cur = self.content.balance["currency"]
        return int(cur.get("bag_coins", 0)) + sum(int(self.content.items.get(i, {}).get("price", 0)) * int(n)
                                                  for i, n in (cur.get("bag_recipe") or {}).items())

    def _mkt_ref_price(self, good: str) -> int:
        """The reference price of one unit: items.yaml "price"; a 💰 bag or a 🪎 chest, what its recipe takes (coins + materials)."""
        if good == "bags":
            return max(1, self._mkt_bag_price())
        if good == "chests":
            recipe = dict(self.content.balance["currency"].get("chest_recipe") or {})
            bags = int(recipe.pop("bags", 0))
            return max(1, bags * self._mkt_bag_price() + sum(int(self.content.items.get(i, {}).get("price", 0)) * int(n)
                                                              for i, n in recipe.items()))
        return max(1, int((self.content.items.get(good) or {}).get("price", 1)))

    def _mkt_band(self, good: str) -> tuple[int, int]:
        """(lowest, highest) unit price allowed (D-26): market.price_min and price_max times the reference price. A 🗺️ map
        scroll is the exception (D-311.5: "at whatever price they want"; D-326): map_scroll.price_min to price_max."""
        if good == self._scroll_item():
            scfg = self._scroll_cfg()
            low = max(1, int(scfg.get("price_min", 1)))
            return low, max(low, int(scfg.get("price_max", 10000)))
        cfg = self._mkt_cfg()
        ref = self._mkt_ref_price(good)
        low = max(1, int(ref * float(cfg.get("price_min", 0.25))))
        high = max(low, int(math.ceil(ref * float(cfg.get("price_max", 10)))))
        return low, high

    def _mkt_clamp(self, good: str, price: int) -> int:
        low, high = self._mkt_band(good)
        return min(high, max(low, int(price)))

    def _mkt_tax(self, total: int) -> int:
        """The market tax on a sale of `total` coins (market.tax, rounded half up): a sink, paid by who gets the coins."""
        return max(0, min(int(total), int(total * float(self._mkt_cfg().get("tax", 0.05)) + 0.5)))

    def _mkt_name(self, good: str) -> str:
        """"🧪 Poción de vida", "🟢⚔️ Espada …" (with ✒️), "💰 Bolsa"; "?" for something no longer in the catalog."""
        t = self.texts
        if good in COIN_GOODS:
            return t.t(f"market.good.{good}")
        item = self.content.items.get(good)
        if not item:
            return "?"
        if item.get("kind") == "gear":
            return self._gear_name(good)
        return f"{item['emoji']} {t.t(item['name_key'])}"

    def _mkt_label(self, entry: dict[str, Any]) -> str:
        """An order or a box entry with its marks: the name, ✨ if enchanted and who signed a ✒️ masterwork."""
        t = self.texts
        label = self._mkt_name(entry.get("good", ""))
        if entry.get("enchant"):
            label += t.t("ench.mark")
        if entry.get("sig"):
            label += t.t("market.signed", name=entry["sig"])
        if entry.get("scroll"):                          # D-326: a 🗺️ scroll says its region, zones and author
            label += t.t("market.scroll_mark", summary=self._scroll_summary(entry["scroll"]))
        if durability.wears(self.content.items.get(entry.get("good", ""))):     # D-333: 🔧 the next unit's durability
            wear = list(entry.get("wear") or [])
            label += " · " + self._dur_tag(wear[0] if wear else None)
        return label

    def _mkt_enchant_text(self, enchant: dict[str, Any] | None) -> str:
        """"⚔️ Filo +2 % ataque" for an enchantment record carried by an order; "" if none."""
        edef = self._ench_defs().get((enchant or {}).get("id", ""))
        if not edef:
            return ""
        return f"{self._ench_label(enchant['id'])} {self._gear_stats_text({edef['stat']: float(enchant.get('value', 0.0))})}"

    def _mkt_fit(self, hero: Hero, good: str) -> str:
        """A short mark for a gear line: ✅ for you, 🔒 from level N, ⚠️ not your class; "" for anything else."""
        t = self.texts
        item = self.content.items.get(good) or {}
        if item.get("kind") != "gear":
            return ""
        fits = suits(item, hero, self.content.classes, self.content.balance)
        if can_use(item, hero, self.content.classes, self.content.balance) == "level":
            return t.t("market.fit_later", level=item.get("req_level", 1))
        return t.t("market.fit_yes") if fits else t.t("market.fit_no")

    def _mkt_left(self, seconds: float) -> str:
        """Time left as "6 d 23 h" past a day, else as _fmt_duration ("3 h 5 min", "12 min")."""
        seconds = max(0.0, seconds)
        if seconds >= 86400:
            days, rest = divmod(int(seconds), 86400)
            return self.texts.t("market.time_days", d=days, h=rest // 3600)
        return self._fmt_duration(seconds)

    # ------------------------------------------------------------------ where, and what a hero holds

    def _mkt_where(self, hero: Hero) -> str | None:
        """Where the hero can trade now: "fire" (any bonfire, not busy), "camp" (the center of its camp with the 🏪 Puesto
        de trueque, not busy), or None (browse only)."""
        if hero.activity:
            return None
        if mapgen.is_bonfire(hero.x, hero.y):
            return "fire"
        here = self._upgrades_here(hero)
        if here and self._camp_service(here[0], "sell_ratio"):
            return "camp"
        return None

    def _mkt_can_collect(self, hero: Hero) -> bool:
        """📦 Recoger works at any bonfire or at the center of your camp (with or without the 🏪 Puesto), not busy."""
        if hero.activity:
            return False
        return mapgen.is_bonfire(hero.x, hero.y) or self._upgrades_here(hero) is not None

    def _mkt_back(self, hero: Hero) -> str:
        """Where ↩️ Volver of the market hub goes: the 🛒 Mercader at a bonfire, ⚒️ Oficios of your camp, else 📍 Zona."""
        where = self._mkt_where(hero)
        return "shop" if where == "fire" else "svc:oficio" if where == "camp" else "home"

    def _mkt_have(self, hero: Hero, good: str) -> int:
        """How many units of a good the hero can put up: backpack units (never the belt or what is worn); bags and chests."""
        if good == "bags":
            return int(hero.bags)
        if good == "chests":
            return int(hero.chests)
        return int(hero.backpack.get(good, 0))

    def _mkt_take(self, hero: Hero, good: str, n: int) -> list[dict[str, Any] | None]:
        """Take `n` units of a good out of the hero; for gear, returns the durability record of each unit that leaves, the most
        worn first (None = a new copy; D-333), else []."""
        wear: list[dict[str, Any] | None] = []
        if good == "bags":
            hero.bags -= n
        elif good == "chests":
            hero.chests -= n
        else:
            if durability.wears(self.content.items.get(good)):
                wear = durability.take_copies(hero, good, n)     # D-333: before the backpack loses them
            hero.backpack[good] = hero.backpack.get(good, 0) - n
            if hero.backpack[good] <= 0:
                del hero.backpack[good]
            self._forget_piece(hero, good)          # the last copy takes its ✨ and ✒️ along (they travel in the order)
        return wear

    def _mkt_sellables(self, hero: Hero) -> list[str]:
        """What the hero can put up for sale, by category order then name: gear, remedies, furniture, food, bags, chests and
        🗺️ map scrolls. Each scroll is its own line, "<item>@<scroll id>" (D-326: every copy has its own zones)."""
        scroll = self._scroll_item()
        goods = [i for i, n in hero.backpack.items() if n > 0 and i != scroll and self._mkt_category(i)]
        goods += [g for g in COIN_GOODS if self._mkt_have(hero, g) > 0]
        goods += [f"{scroll}@{data.get('id')}" for data in hero.map_scrolls]
        order = {cat: n for n, cat in enumerate(MARKET_CATEGORIES)}

        def key(good: str) -> tuple[Any, ...]:
            base = good.partition("@")[0]
            return (order[self._mkt_category(base)], -int((self.content.items.get(base) or {}).get("tier", 0)), self._mkt_name(base))

        return sorted(goods, key=key)

    def _mkt_resources(self) -> list[str]:
        """Every resource a buy order can ask for, by its code (the codes of 📦 Recursos, /07)."""
        return sorted((i for i in self.content.items if self._mkt_is_resource(i)), key=lambda i: int(self.content.items[i]["code"]))

    # ------------------------------------------------------------------ storage

    def _mkt_meta(self) -> dict[str, Any]:
        return self.store.get("meta", "market") or {"seq": 0}

    def _mkt_order(self, oid: str | None) -> dict[str, Any] | None:
        return self.store.get("market_order", oid) if oid else None

    @staticmethod
    def _mkt_index_key(order: dict[str, Any], category: str | None) -> str:
        return f"sell:{category}" if order["side"] == "sell" else "buy"

    def _mkt_index(self, key: str) -> list[list[Any]]:
        return list((self.store.get("market_index", key) or {}).get("ids") or [])

    def _mkt_index_put(self, key: str, rows: list[list[Any]]) -> None:
        if rows:
            self.store.put("market_index", key, {"ids": rows})
        else:
            self.store.delete("market_index", key)

    @staticmethod
    def _mkt_seq(oid: str) -> int:
        return int(oid[1:]) if oid[1:].isdigit() else 0

    def _mkt_index_add(self, order: dict[str, Any]) -> None:
        key = self._mkt_index_key(order, self._mkt_category(order["good"]))
        rows = [row for row in self._mkt_index(key) if row[1] != order["id"]] + [[order["price"], order["id"], order["good"]]]
        sign = 1 if order["side"] == "sell" else -1           # sells: cheapest first; buys: best price first
        rows.sort(key=lambda row: (sign * int(row[0]), self._mkt_seq(str(row[1]))))
        self._mkt_index_put(key, rows)

    def _mkt_index_remove(self, order: dict[str, Any]) -> None:
        key = self._mkt_index_key(order, self._mkt_category(order["good"]))
        self._mkt_index_put(key, [row for row in self._mkt_index(key) if row[1] != order["id"]])

    def _mkt_mine(self, account: str) -> list[str]:
        return list((self.store.get("market_mine", account) or {}).get("ids") or [])

    def _mkt_mine_put(self, account: str, ids: list[str]) -> None:
        if ids:
            self.store.put("market_mine", account, {"ids": ids})
        else:
            self.store.delete("market_mine", account)

    def _mkt_box(self, account: str) -> list[dict[str, Any]]:
        return list((self.store.get("market_box", account) or {}).get("items") or [])

    def _mkt_box_put(self, account: str, items: list[dict[str, Any]]) -> None:
        if items:
            self.store.put("market_box", account, {"items": items})
        else:
            self.store.delete("market_box", account)

    def _mkt_box_add(self, account: str, entry: dict[str, Any]) -> None:
        """Put something in a player's 📦 Entregas; a future arrival moves meta "next_due" so tick() tells it once."""
        self._mkt_box_put(account, self._mkt_box(account) + [entry])
        if not entry.get("told"):
            meta = self._mkt_meta()
            due = meta.get("next_due")
            meta["next_due"] = entry["at"] if due is None else min(float(due), entry["at"])
            self.store.put("meta", "market", meta)

    def _mkt_log(self, **counts: int) -> None:
        """Add to today's market counts ("market_log"/<day>) for the daily report; drop days past market.log_days."""
        day = str(self._today())
        record = self.store.get("market_log", day)
        if record is None:
            keep = int(self._mkt_cfg().get("log_days", 30))
            for key, _ in list(self.store.items("market_log")):
                if key.isdigit() and int(key) <= int(day) - keep:
                    self.store.delete("market_log", key)
            record = {}
        for key, n in counts.items():
            record[key] = int(record.get(key, 0)) + int(n)
        self.store.put("market_log", day, record)

    def _mkt_credit(self, account: str, coins: int, actor: Hero | None) -> None:
        """Pay coins to a player: the hero playing now in memory, anyone else through its saved record (rule 5). If there is
        no hero (never, but D-64), the coins wait in its 📦 Entregas."""
        if coins <= 0:
            return
        if actor is not None and actor.id == account:
            actor.gold += coins
            return
        target = self._load(account)
        if target is None:
            self._mkt_box_add(account, {"good": "coins", "coins": coins, "n": 0, "at": self.clock.now(), "told": True,
                                        "why": "returned", "from": ""})
            return
        target.gold += coins
        self._save(target)

    # ------------------------------------------------------------------ lifecycle: expiry, closing, arrivals

    def _mkt_close(self, order: dict[str, Any], why: str, actor: Hero | None) -> list[str]:
        """End an order (filled, cancelled or expired): give back what is left, drop it from the index and the owner's list,
        delete it. Returns a line for the actor if it is its own order; the owner of an expired one gets a notice."""
        left = int(order.get("n", 0))
        owner = order["by"]
        now = self.clock.now()
        if left > 0 and order["side"] == "sell":
            self._mkt_box_add(owner, {"good": order["good"], "n": left, "at": now, "enchant": order.get("enchant"),
                                      "sig": order.get("sig"), "from": "", "why": "expired" if why == "expired" else "returned",
                                      "told": True, **({"scroll": order["scroll"]} if order.get("scroll") else {}),
                                      **({"wear": order["wear"]} if any(order.get("wear") or []) else {})})   # D-333
        elif left > 0:
            self._mkt_credit(owner, left * int(order["price"]), actor)
        self._mkt_index_remove(order)
        self._mkt_mine_put(owner, [oid for oid in self._mkt_mine(owner) if oid != order["id"]])
        self.store.delete("market_order", order["id"])
        if why in ("expired", "cancelled"):
            self._mkt_log(**{why: 1})
        if left <= 0 or why == "filled":
            return []

        def back_line() -> str:                   # built in the language in use (the owner's, inside _push_each)
            if order["side"] == "sell":
                return self.texts.t("market.back_items", item=self._mkt_label(order), n=left)
            return self.texts.t("market.back_coins", coins=self._money(left * int(order["price"])), item=self._mkt_name(order["good"]))

        if why == "expired" and (actor is None or actor.id != owner):
            self._push_each([owner], lambda: View(kind="market_notice", title=self.texts.t("market.expired_title"),
                                                  body=[back_line(), self.texts.t("market.collect_hint")],
                                                  actions=[Action(id="mkt", label=self.texts.t("market.button"))]))
            return []
        return [back_line()]

    def _mkt_settle(self, actor: Hero | None) -> list[str]:
        """Close every order whose time ran out (lazily, and from tick()). Cheap: it only scans when meta "next_expire" says
        one is due. Returns the lines for the actor's own expired orders."""
        meta = self._mkt_meta()
        due = meta.get("next_expire")
        now = self.clock.now()
        if due is None or now < float(due):
            return []
        lines: list[str] = []
        soonest: float | None = None
        for oid, order in list(self.store.items("market_order")):
            if float(order.get("until", 0)) <= now:
                lines += self._mkt_close(order, "expired", actor)
            else:
                soonest = float(order["until"]) if soonest is None else min(soonest, float(order["until"]))
        meta = self._mkt_meta()                      # _mkt_close may have moved next_due
        meta["next_expire"] = soonest
        self.store.put("meta", "market", meta)
        if actor is not None and lines:
            return [self.texts.t("market.expired_title")] + lines
        return lines

    def _mkt_arrivals(self) -> None:
        """Tell each player once that a delivery reached its 📦 Entregas (only when meta "next_due" says one may have)."""
        meta = self._mkt_meta()
        due = meta.get("next_due")
        now = self.clock.now()
        if due is None or now < float(due):
            return
        soonest: float | None = None
        for account, box in list(self.store.items("market_box")):
            items = list(box.get("items") or [])
            arrived = [e for e in items if not e.get("told") and float(e.get("at", 0)) <= now]
            for entry in items:
                if not entry.get("told") and float(entry.get("at", 0)) > now:
                    soonest = float(entry["at"]) if soonest is None else min(soonest, float(entry["at"]))
            if not arrived:
                continue
            for entry in arrived:
                entry["told"] = True
            self._mkt_box_put(account, items)
            labels = list(arrived)
            self._push_each([account], lambda labels=labels: View(
                kind="market_notice", title=self.texts.t("market.arrived_title"),
                body=[self.texts.t("market.arrived_line", item=self._mkt_label(e), n=e.get("n", 0)) for e in labels]
                + [self.texts.t("market.collect_hint")],
                actions=[Action(id="mkt:box", label=self.texts.t("market.box_button", n=len(labels)))]))
        meta = self._mkt_meta()
        meta["next_due"] = soonest
        self.store.put("meta", "market", meta)

    def _market_tick(self) -> None:
        """tick(): close the orders that ran out and tell who got a delivery. [ES] Lo llama tick() antes de mirar a los héroes."""
        self._mkt_settle(None)
        self._mkt_arrivals()

    # ------------------------------------------------------------------ the hub

    def _market_view(self, hero: Hero, notice: str | None = None) -> View:
        """🏛️ Mercado: one book for every player (D-137): buy, sell, the buy orders, ask for resources, your orders, 📦 Entregas.

        [ES]
        Qué hace: la entrada del mercado entre jugadores (D-320): tus monedas, tus órdenes activas contra el tope, lo que
        espera en 📦 Entregas (listo o en camino), el impuesto y el tiempo del transporte, y si aquí solo se puede mirar (para
        publicar, comprar, vender a un pedido o recoger hay que estar en una 🔥 fogata o en tu campamento con 🏪 Puesto de
        trueque). Hasta 8 botones (HUB_KINDS "market"): 🛍️ Comprar, 🏷️ Vender, 📥 Pedidos de compra, 📝 Pedir recursos,
        📋 Mis órdenes, 📦 Entregas, 📜 Pedidos de fabricación (D-335, 0.59: engine/service/craft_orders.py) y ↩️ Volver (al
        🛒 Mercader, a ⚒️ Oficios de tu campamento o a 📍 Zona).
        La llaman: el botón 🏛️ Mercado del 🛒 Mercader y de ⚒️ Oficios (con el 🏪 Puesto de trueque), /mercado y /market.
        Si cambia, afecta: tests/test_mercado.py.
        """
        t = self.texts
        cfg = self._mkt_cfg()
        mine = self._mkt_mine(hero.id)
        box = self._mkt_box(hero.id)
        now = self.clock.now()
        ready = sum(1 for e in box if float(e.get("at", 0)) <= now)
        body = [t.t("market.intro"), t.t("hero.gold_line", gold=self._money(hero.gold)),
                t.t("market.orders_line", n=len(mine), cap=int(cfg.get("max_orders", 10)))]
        if box:
            body.append(t.t("market.box_line", ready=ready, coming=len(box) - ready))
        body += ["", t.t("market.rules_line", pct=round(float(cfg.get("tax", 0.05)) * 100),
                         time=self._fmt_duration(self._mkt_delivery_seconds()), days=int(cfg.get("order_days", 7)))]
        if self._mkt_where(hero) is None:
            body += ["", t.t("market.browse_only")]
        actions = [Action(id="mkt:cats", label=t.t("market.shop_button")), Action(id="mkt:sell:0", label=t.t("market.sell_button")),
                   Action(id="mkt:fill:0", label=t.t("market.fill_button")), Action(id="mkt:ask:0", label=t.t("market.ask_button")),
                   Action(id="mkt:mine", label=t.t("market.mine_button", n=len(mine))),
                   Action(id="mkt:box", label=t.t("market.box_button", n=len(box))),
                   Action(id="cord", label=t.t("corder.market_button")),        # D-335 (0.59): 📜 Pedidos de fabricación
                   Action(id=self._mkt_back(hero), label=t.t("menu.back"))]
        return View(kind="market", title=t.t("market.title"), body=body, actions=actions, notice=notice)

    def _market_action(self, hero: Hero, action_id: str) -> View:
        """Route a "mkt…" button. Menus open while busy; trading checks the place (_mkt_where, _mkt_can_collect) itself.

        [ES] Qué hace: reparte los botones del mercado. Antes de cada uno cierra las órdenes vencidas (_mkt_settle), así lo
        que se ve está al día aunque tick() no haya corrido. La llama: _idle_action. Si cambia, afecta: todos los botones
        "mkt…" (ids estables: solo se agregan).
        """
        expired = self._mkt_settle(hero)
        parts = action_id.split(":")
        what = parts[1] if len(parts) > 1 else ""
        arg = parts[2] if len(parts) > 2 else ""
        page = int(arg) if arg.isdigit() else 0
        if what == "cats":
            view = self._market_cats_view(hero)
        elif what == "cat":
            view = self._market_list_view(hero, arg, int(parts[3]) if len(parts) > 3 and parts[3].isdigit() else 0)
        elif what == "o":
            view = self._market_offer_view(hero, arg)
        elif what == "buy":
            view = self._market_buy(hero, arg, parts[3] if len(parts) > 3 else "1")
        elif what == "sell":
            view = self._market_sell_list(hero, page)
        elif what == "draft":
            view = self._market_draft_view(hero)
        elif what == "p":
            view = self._market_draft_price(hero, arg)
        elif what == "q":
            view = self._market_draft_qty(hero, arg)
        elif what == "ok":
            view = self._market_publish(hero)
        elif what == "fill":
            view = self._market_fill_list(hero, page)
        elif what == "bo":
            view = self._market_bo_view(hero, arg)
        elif what == "give":
            view = self._market_fill(hero, arg, parts[3] if len(parts) > 3 else "a")
        elif what == "ask":
            view = self._market_ask_list(hero, page)
        elif what == "mine":
            view = self._market_mine_view(hero)
        elif what == "my":
            view = self._market_my_view(hero, arg)
        elif what == "x":
            view = self._market_cancel(hero, arg)
        elif what == "box":
            view = self._market_box_view(hero)
        elif what == "get":
            view = self._market_collect(hero)
        else:
            view = self._market_view(hero)
        if expired:
            view.notice = self._join(expired + ([view.notice] if view.notice else []))
        return view

    def _market_code(self, hero: Hero, letter: str, n: int) -> View:
        """/c2, /s2, /b07, /k2, /o2 (typed or tapped): the offer, your thing to sell, the resource to ask for, the buy order
        to fill or your order with that number in the last list shown (/b uses the resource's own code, /07)."""
        t = self.texts
        expired = self._mkt_settle(hero)
        if letter == "b":
            good = next((i for i in self._mkt_resources() if int(self.content.items[i]["code"]) == n), None)
            view = (self._market_draft_new(hero, "buy", good) if good
                    else self._market_ask_list(hero, 0, notice=t.t("market.bad_code", code=f"/b{n:02d}")))
        else:
            target = self._code_target(hero, MARKET_CODE_KINDS[letter], n)
            if letter == "s":
                good, _, sid = (target or "").partition("@")        # D-326: "<item>@<scroll id>" is one 🗺️ scroll
                ok = bool(target) and (self._scroll_find(hero, sid) is not None if sid else self._mkt_have(hero, good) > 0)
                view = (self._market_draft_new(hero, "sell", good, scroll=sid or None) if ok
                        else self._market_sell_list(hero, 0, notice=t.t("market.bad_code", code=f"/s{n}")))
            elif letter == "c":
                view = self._market_offer_view(hero, target or "", notice=None if target else t.t("market.bad_code", code=f"/c{n}"))
            elif letter == "k":
                view = self._market_bo_view(hero, target or "", notice=None if target else t.t("market.bad_code", code=f"/k{n}"))
            else:
                view = self._market_my_view(hero, target or "", notice=None if target else t.t("market.bad_code", code=f"/o{n}"))
        if expired:
            view.notice = self._join(expired + ([view.notice] if view.notice else []))
        return view

    # ------------------------------------------------------------------ 🛍️ Comprar: sell orders by category

    def _market_cats_view(self, hero: Hero, notice: str | None = None) -> View:
        """🛍️ Comprar: one button per category with how many offers it has (7 and ↩️ Volver: HUB_KINDS "market_cats")."""
        t = self.texts
        body = [t.t("market.cats_intro")]
        actions = []
        for cat in MARKET_CATEGORIES:
            count = len(self._mkt_index(f"sell:{cat}"))
            actions.append(Action(id=f"mkt:cat:{cat}:0", label=t.t("market.cat_button", name=t.t(f"market.cat.{cat}"), n=count)))
        actions.append(Action(id="mkt", label=t.t("menu.back")))
        return View(kind="market_cats", title=t.t("market.shop_title"), body=body, actions=actions, notice=notice)

    def _market_list_view(self, hero: Hero, cat: str, page: int = 0, notice: str | None = None) -> View:
        """A category's offers, cheapest first, one line each with its code (/c1): what, how many, price, seller and, for gear,
        whether it suits you (✅, 🔒 level, ⚠️ class). Pages of market.per_page; ➡️ Más and ↩️ Volver."""
        t = self.texts
        if cat not in MARKET_CATEGORIES:
            return self._market_cats_view(hero)
        per = max(1, int(self._mkt_cfg().get("per_page", 8)))
        rows = self._mkt_index(f"sell:{cat}")
        pages = max(1, (len(rows) + per - 1) // per)
        page %= pages
        body = [t.t("market.list_title", name=t.t(f"market.cat.{cat}"))]
        shown: list[str] = []
        for row in rows[page * per:(page + 1) * per]:
            order = self._mkt_order(str(row[1]))
            if order is None:
                continue
            shown.append(order["id"])
            fit = self._mkt_fit(hero, order["good"])
            mine = t.t("market.yours") if order["by"] == hero.id else ""
            body.append(t.t("market.offer_line", code=f"/c{page * per + len(shown)}", item=self._mkt_label(order),
                            n=order["n"], price=self._money(order["price"]), name=order.get("name", "?"),
                            fit=f" · {fit}" if fit else "", mine=mine))
        self._codes(hero, "mkt_offers", [""] * (page * per) + shown)
        if not rows:
            body.append(t.t("market.list_empty"))
        else:
            body += ["", t.t("market.list_hint")]
            if pages > 1:
                body.append(t.t("market.page", n=page + 1, total=pages))
        actions = [Action(id=f"mkt:cat:{cat}:{page + 1}", label=t.t("market.more"))] if pages > 1 else []
        actions.append(Action(id="mkt:cats", label=t.t("menu.back")))
        return View(kind="market_list", title=t.t("market.shop_title"), body=body, actions=actions, notice=notice)

    def _market_offer_view(self, hero: Hero, oid: str, notice: str | None = None) -> View:
        """One offer: the piece (slot, type, level, stats, ✅/⚠️ for you, ✒️ signature, ✨ enchantment), seller, price, how many;
        🛒 Comprar 1 and 🛒 Comprar todo (×N); when it arrives. Your own offer: only ↩️ Volver (cancel it in 📋 Mis órdenes)."""
        t = self.texts
        order = self._mkt_order(oid)
        if order is None or order.get("side") != "sell":
            return self._market_cats_view(hero, notice=notice or t.t("market.gone"))
        good = order["good"]
        cat = self._mkt_category(good) or "weapons"
        body = [self._mkt_label(order)]
        item = self.content.items.get(good) or {}
        if item.get("kind") == "gear":
            body.append(t.t("gear.detail_line", slot=t.t(f"gear.slot.{item['slot']}"), type=t.t(f"gear.type.{item['type']}"),
                            rarity=t.t(f"gear.rarity.{item.get('rarity', 'comun')}"), level=item.get("req_level", 1)))
            body.append(t.t("gear.detail_stats", stats=self._gear_stats_text(item.get("stats", {}))))
            body.append(self._gear_status(hero, item))
            if item.get("masterwork"):
                body.append(t.t("gear.masterwork_by", name=order["sig"]) if order.get("sig") else t.t("gear.masterwork_unsigned"))
            enchant = self._mkt_enchant_text(order.get("enchant"))
            if enchant:
                body.append(t.t("ench.item_line", enchant=enchant))
            wear = list(order.get("wear") or [])          # D-333: 🔧 the next unit's durability and repairs left
            body.append(self._dur_line(wear[0] if wear else None, good))
            if int(order["n"]) > 1:
                rest = [self._dur_tag(wear[i] if i < len(wear) else None) for i in range(1, min(int(order["n"]), 5))]
                body.append(t.t("market.wear_rest", tags=" · ".join(rest)))
        if order.get("scroll"):                           # D-326: how many of its zones are new for you; only the colour
            new = self._scroll_new(hero, list(order["scroll"].get("zones") or []))
            body += [t.t("scroll.new_line", n=len(new)) if new else t.t("scroll.nothing_new"), t.t("scroll.use_explain")]
        body += ["", t.t("market.offer_detail", name=order.get("name", "?"), price=self._money(order["price"]), n=order["n"],
                         left=self._mkt_left(float(order["until"]) - self.clock.now()),
                         clock=self._clock(float(order["until"]))),       # D-124, D-334: 🕐 when it expires, in your zone
                 t.t("market.delivery_line", time=self._fmt_duration(self._mkt_delivery_seconds()))]
        actions = []
        if order["by"] == hero.id:
            body.append(t.t("market.own_offer"))
        else:
            if self._mkt_where(hero) is None:
                body.append(t.t("market.browse_only"))
            actions.append(Action(id=f"mkt:buy:{oid}:1", label=t.t("market.buy_one", price=self._money(order["price"]))))
            if order["n"] > 1:
                actions.append(Action(id=f"mkt:buy:{oid}:a", label=t.t("market.buy_all", n=order["n"],
                                                                     price=self._money(order["price"] * order["n"]))))
        actions.append(Action(id=f"mkt:cat:{cat}:0", label=t.t("menu.back")))
        return View(kind="market_offer", title=t.t("market.offer_title"), body=body, actions=actions, notice=notice)

    def _market_buy(self, hero: Hero, oid: str, amount: str) -> View:
        """🛒 Comprar: coins leave the buyer, the seller gets them minus the tax at once (with a notice), the goods travel to
        the buyer's 📦 Entregas (market.delivery_minutes). Refused without coins, at the wrong place, or your own order."""
        t = self.texts
        order = self._mkt_order(oid)                      # rule 2: always read fresh from the store
        if order is None or order.get("side") != "sell" or int(order.get("n", 0)) <= 0:
            return self._market_cats_view(hero, notice=t.t("market.gone"))
        if order["by"] == hero.id:
            return self._market_offer_view(hero, oid, notice=t.t("market.own_offer"))
        if self._mkt_where(hero) is None:
            return self._market_offer_view(hero, oid, notice=t.t("market.need_place"))
        n = int(order["n"]) if amount == "a" else max(1, min(int(order["n"]), int(amount) if amount.isdigit() else 1))
        cost = n * int(order["price"])
        if hero.gold < cost:
            return self._market_offer_view(hero, oid, notice=t.t("market.no_coins", price=self._money(cost)))
        hero.gold -= cost
        order["n"] = int(order["n"]) - n
        tax = self._mkt_tax(cost)
        seller = order["by"]
        self._mkt_credit(seller, cost - tax, hero)
        arrive = self.clock.now() + self._mkt_delivery_seconds()
        wear = list(order.get("wear") or [])             # D-333: the next units' durability goes with them
        bought = wear[:n]
        if wear:
            order["wear"] = wear[n:]
        self._mkt_box_add(hero.id, {"good": order["good"], "n": n, "at": arrive, "enchant": order.get("enchant"),
                                    "sig": order.get("sig"), "from": order.get("name", "?"), "why": "bought", "told": False,
                                    **({"scroll": order["scroll"]} if order.get("scroll") else {}),   # D-326: its zones travel
                                    **({"wear": bought} if any(bought) else {})})
        snap = {**order, "wear": bought}                  # D-333: the notices name the units that were bought
        label = self._mkt_label(snap)
        if order["n"] <= 0:
            self._mkt_close(order, "filled", hero)
        else:
            self.store.put("market_order", oid, order)
        self._mkt_log(trades=1, units=n, coins=cost, tax=tax)
        buyer = hero.name
        self._push_each([seller], lambda: View(          # built again in the seller's language (D-250)
            kind="market_notice", title=self.texts.t("market.sold_title"),
            body=[self.texts.t("market.sold_line", name=buyer, item=self._mkt_label(snap), n=n, coins=self._money(cost - tax),
                               tax=self._money(tax))],
            actions=[Action(id="mkt:mine", label=self.texts.t("market.mine_button", n=len(self._mkt_mine(seller))))]))
        cat = self._mkt_category(order["good"]) or "weapons"
        return self._market_list_view(hero, cat, notice=t.t("market.bought", item=label, n=n, price=self._money(cost),
                                                            time=self._fmt_duration(self._mkt_delivery_seconds())))

    # ------------------------------------------------------------------ 🏷️ Vender: your things, the draft and publishing

    def _market_sell_list(self, hero: Hero, page: int = 0, notice: str | None = None) -> View:
        """🏷️ Vender: what you can put up (gear, remedies, furniture, food, 💰 bags, 🪎 chests), one line each with /s1, how
        many you have and its reference price. Resources are not sold here: they go to 📥 Pedidos de compra."""
        t = self.texts
        goods = self._mkt_sellables(hero)
        per = max(1, int(self._mkt_cfg().get("per_page", 8)))
        pages = max(1, (len(goods) + per - 1) // per)
        page %= pages
        self._codes(hero, "mkt_sell", goods)
        body = [t.t("market.sell_intro")]
        for n, good in enumerate(goods[page * per:(page + 1) * per], page * per + 1):
            base, _, sid = good.partition("@")
            scroll = self._scroll_find(hero, sid) if sid else None
            if scroll is not None:                        # D-326: one line per 🗺️ scroll, with its region, zones and author
                body.append(t.t("market.sell_line", code=f"/s{n}", item=self._mkt_label({"good": base, "scroll": scroll}), n=1,
                                price=self._money(self._mkt_ref_price(base)), fit=""))
                continue
            fit = self._mkt_fit(hero, good)
            body.append(t.t("market.sell_line", code=f"/s{n}", item=self._mkt_name(good) + (self._enchant_mark(hero, good)
                            + self._bag_wear_note(hero, good, worst=True)          # D-333: 🔧 the copy that goes first
                            if good not in COIN_GOODS else ""), n=self._mkt_have(hero, good),
                            price=self._money(self._mkt_ref_price(good)), fit=f" · {fit}" if fit else ""))
        if not goods:
            body.append(t.t("market.sell_none"))
        else:
            body += ["", t.t("market.sell_hint")]
            if pages > 1:
                body.append(t.t("market.page", n=page + 1, total=pages))
        body.append(t.t("market.sell_resources_hint"))
        actions = [Action(id=f"mkt:sell:{page + 1}", label=t.t("market.more"))] if pages > 1 else []
        actions.append(Action(id="mkt", label=t.t("menu.back")))
        return View(kind="market_sell", title=t.t("market.sell_title"), body=body, actions=actions, notice=notice)

    def _market_draft_new(self, hero: Hero, side: str, good: str, scroll: str | None = None) -> View:
        """Open a draft order ("market_open"): a sale of `good` (1 unit at its reference price) or a buy order (10 units).
        D-326: `scroll` is the id of the 🗺️ map scroll being sold (always 1: every copy has its own zones)."""
        cfg = self._mkt_cfg()
        asks = list(cfg.get("ask_buttons") or [1, 10, 50])
        self.store.delete("corder_open", hero.id)          # D-335: only one draft that reads typed numbers at a time
        draft = {"side": side, "good": good, "price": self._mkt_clamp(good, self._mkt_ref_price(good)),
                 "n": 1 if side == "sell" else int(asks[1] if len(asks) > 1 else asks[0])}
        if scroll:
            draft["scroll"] = scroll
        self.store.put("market_open", hero.id, draft)
        return self._market_draft_view(hero)

    def _mkt_draft(self, hero: Hero) -> dict[str, Any] | None:
        draft = self.store.get("market_open", hero.id)
        if not draft or draft.get("side") not in ("sell", "buy"):
            return None
        good = draft.get("good", "")
        if draft["side"] == "sell" and not self._mkt_category(good):
            return None
        if draft["side"] == "buy" and not self._mkt_is_resource(good):
            return None
        if draft["side"] == "sell" and good == self._scroll_item():   # D-326: a 🗺️ scroll is sold one copy at a time
            if self._scroll_find(hero, draft.get("scroll")) is None:
                return None
            draft["n"] = 1
        return draft

    def _mkt_qty_choices(self, hero: Hero, draft: dict[str, Any]) -> list[tuple[str, int]]:
        """The quick quantity buttons of a draft: sell, 1 · half · all you have (when you have more than 1); buy,
        market.ask_buttons (1, 10, 50)."""
        if draft["side"] == "buy":
            return [(str(n), int(n)) for n in (self._mkt_cfg().get("ask_buttons") or [1, 10, 50])]
        if draft.get("scroll"):                           # D-326: one 🗺️ scroll per order
            return []
        have = self._mkt_have(hero, draft["good"])
        if have <= 1:
            return []
        out: list[tuple[str, int]] = []
        for key, value in (("1", 1), ("h", max(1, have // 2)), ("a", have)):
            if value not in [v for _, v in out]:
                out.append((key, value))
        return out

    def _market_draft_view(self, hero: Hero, notice: str | None = None) -> View:
        """The draft of an order: what, how many you have (or your coins), the reference price and the band (D-26), your price
        and quantity, what you would get after the tax (or what is set aside), the lifetime and how to type a price.

        [ES]
        Qué hace: arma la orden antes de publicarla. Botones: el precio rápido (×1, ×2, ×3 del precio de referencia,
        market.price_buttons, dentro de la banda), la cantidad rápida (1, la mitad y todo lo que tienes; en un pedido de compra,
        market.ask_buttons), ✅ Publicar y ↩️ Volver, en filas (layout). Lo que escribes es el precio en 🥉 ("30") y, con x, la
        cantidad ("30 x5"). La llaman: /s1 (vender), /b07 (pedir) y los botones del borrador. Si cambia, afecta:
        tests/test_mercado.py.
        """
        t = self.texts
        draft = self._mkt_draft(hero)
        if draft is None:
            return self._market_view(hero, notice=notice)
        cfg = self._mkt_cfg()
        good, price, n = draft["good"], int(draft["price"]), int(draft["n"])
        low, high = self._mkt_band(good)
        ref = self._mkt_ref_price(good)
        total = price * n
        sell = draft["side"] == "sell"
        scroll = self._scroll_find(hero, draft.get("scroll")) if sell and draft.get("scroll") else None
        body = [self._mkt_label({"good": good, "scroll": scroll}) if scroll is not None    # D-326: the 🗺️ scroll being sold
                else self._mkt_name(good) + (self._enchant_mark(hero, good) if sell and good not in COIN_GOODS else "")]
        item = self.content.items.get(good) or {}
        if sell and item.get("kind") == "gear":
            body.append(self._gear_status(hero, item))
            note = self._masterwork_note(hero, good)
            if note:
                body.append(note)
        if sell:
            body.append(t.t("market.draft_have", n=1 if scroll is not None else self._mkt_have(hero, good)))
        else:
            body.append(t.t("hero.gold_line", gold=self._money(hero.gold)))
            best = next((row for row in self._mkt_index("buy") if row[2] == good), None)
            if best:
                body.append(t.t("market.best_ask", price=self._money(int(best[0]))))
        body += [t.t("market.draft_ref", price=self._money(ref), low=self._money(low), high=self._money(high)),
                 "", t.t("market.draft_order", n=n, price=self._money(price), total=self._money(total))]
        tax = self._mkt_tax(total)
        body.append(t.t("market.draft_net", net=self._money(total - tax), tax=self._money(tax),
                        pct=round(float(cfg.get("tax", 0.05)) * 100)) if sell else t.t("market.draft_escrow", total=self._money(total)))
        body += [t.t("market.draft_life", days=int(cfg.get("order_days", 7))), "", t.t("market.draft_hint")]
        if self._mkt_where(hero) is None:
            body.append(t.t("market.browse_only"))
        prices = [Action(id=f"mkt:p:{m}", label=t.t("market.price_button", m=m, price=self._money(self._mkt_clamp(good, ref * int(m)))))
                  for m in (cfg.get("price_buttons") or [1, 2, 3])]
        qtys = [Action(id=f"mkt:q:{key}", label=t.t("market.qty_all", n=value) if key == "a" else t.t("market.qty_button", n=value))
                for key, value in self._mkt_qty_choices(hero, draft)]
        actions = prices + qtys + [Action(id="mkt:ok", label=t.t("market.publish_button", total=self._money(total))),
                                   Action(id="mkt:sell:0" if sell else "mkt:ask:0", label=t.t("menu.back"))]
        layout = [len(prices)] + ([len(qtys)] if qtys else []) + [1, 1]
        title = t.t("market.draft_sell_title" if sell else "market.draft_buy_title")
        return View(kind="market_draft", title=title, body=body, actions=actions, notice=notice, layout=layout)

    def _market_draft_price(self, hero: Hero, mult: str) -> View:
        draft = self._mkt_draft(hero)
        if draft is None or not mult.isdigit():
            return self._market_view(hero)
        draft["price"] = self._mkt_clamp(draft["good"], self._mkt_ref_price(draft["good"]) * int(mult))
        self.store.put("market_open", hero.id, draft)
        return self._market_draft_view(hero)

    def _market_draft_qty(self, hero: Hero, key: str) -> View:
        draft = self._mkt_draft(hero)
        if draft is None:
            return self._market_view(hero)
        value = dict(self._mkt_qty_choices(hero, draft)).get(key)
        if value is None and key.isdigit():
            value = int(key)
        if value:
            draft["n"] = max(1, min(int(value), int(self._mkt_cfg().get("max_units", 500))))
            self.store.put("market_open", hero.id, draft)
        return self._market_draft_view(hero)

    def _market_typed(self, hero: Hero, text: str) -> View:
        """Text while a draft is open: "30" sets the price in 🥉, "30 x5" the price and the quantity, "x5" the quantity.

        [ES] Qué hace: el precio (y la cantidad) escritos. Un precio fuera de la banda (D-26) se corrige al borde y se avisa;
        un texto que no es un número avisa cómo escribirlo. La llama: GameService.text() con "market_open" guardado.
        Si cambia, afecta: tests/test_mercado.py.
        """
        t = self.texts
        draft = self._mkt_draft(hero)
        if draft is None:
            self.store.delete("market_open", hero.id)
            return self._market_view(hero)
        qty = QTY_RE.match(text)
        match = PRICE_RE.match(text) if not qty else None
        if not qty and not match:
            return self._market_draft_view(hero, notice=t.t("market.type_number"))
        notes = []
        if match:
            wanted = int(match.group(1))
            draft["price"] = self._mkt_clamp(draft["good"], wanted)
            if draft["price"] != wanted:
                low, high = self._mkt_band(draft["good"])
                notes.append(t.t("market.band_fixed", low=self._money(low), high=self._money(high)))
        count = (qty.group(1) if qty else match.group(2)) if (qty or match.group(2)) else None
        if count is not None:
            draft["n"] = max(1, min(int(count), int(self._mkt_cfg().get("max_units", 500))))
        self.store.put("market_open", hero.id, draft)
        return self._market_draft_view(hero, notice=self._join(notes))

    def _mkt_new_order(self, hero: Hero, side: str, good: str, price: int, n: int,
                       enchant: dict[str, Any] | None = None, sig: str | None = None,
                       scroll: dict[str, Any] | None = None,
                       wear: list[dict[str, Any] | None] | None = None) -> dict[str, Any]:
        meta = self._mkt_meta()
        meta["seq"] = int(meta.get("seq", 0)) + 1
        now = self.clock.now()
        until = now + self._mkt_order_seconds()
        meta["next_expire"] = until if meta.get("next_expire") is None else min(float(meta["next_expire"]), until)
        self.store.put("meta", "market", meta)
        order = {"id": f"m{meta['seq']}", "side": side, "good": good, "n": n, "n0": n, "price": price, "by": hero.id,
                 "name": hero.name, "at": now, "until": until, "x": hero.x, "y": hero.y,
                 "enchant": dict(enchant) if enchant else None, "sig": sig}
        if scroll:                                        # D-326: the 🗺️ scroll's zones, author and region travel with it
            order["scroll"] = dict(scroll)
        if wear and any(wear):                            # D-333: 🔧 each unit's durability travels with it (None = new)
            order["wear"] = [dict(r) if r else None for r in wear]
        self.store.put("market_order", order["id"], order)
        self._mkt_index_add(order)
        self._mkt_mine_put(hero.id, self._mkt_mine(hero.id) + [order["id"]])
        return order

    def _market_publish(self, hero: Hero) -> View:
        """✅ Publicar: checks the place, the cap of active orders, the band (D-26), and that you have the units (a sale) or the
        coins (a buy order); then the units or the coins go into the order (escrow) and it shows in the book at once."""
        t = self.texts
        draft = self._mkt_draft(hero)
        if draft is None:
            return self._market_view(hero)
        cfg = self._mkt_cfg()
        if self._mkt_where(hero) is None:
            return self._market_draft_view(hero, notice=t.t("market.need_place"))
        if len(self._mkt_mine(hero.id)) >= int(cfg.get("max_orders", 10)):
            return self._market_draft_view(hero, notice=t.t("market.too_many", cap=int(cfg.get("max_orders", 10))))
        good, n = draft["good"], int(draft["n"])
        price = int(draft["price"])
        low, high = self._mkt_band(good)
        if not low <= price <= high or n < 1 or n > int(cfg.get("max_units", 500)):
            return self._market_draft_view(hero, notice=t.t("market.band_fixed", low=self._money(low), high=self._money(high)))
        if draft["side"] == "sell" and draft.get("scroll"):    # D-326: the 🗺️ scroll leaves the backpack with its zones
            data = self._scroll_take(hero, draft["scroll"])
            if data is None:
                return self._market_sell_list(hero, notice=t.t("market.not_enough", n=0))
            order = self._mkt_new_order(hero, "sell", good, price, 1, scroll=data)
            self._mkt_log(sell_orders=1)
            notice = t.t("market.listed", item=self._mkt_label(order), n=1, price=self._money(price))
        elif draft["side"] == "sell":
            if self._mkt_have(hero, good) < n:
                return self._market_draft_view(hero, notice=t.t("market.not_enough", n=self._mkt_have(hero, good)))
            enchant = (hero.gear_enchants or {}).get(good) if good not in COIN_GOODS else None
            sig = (hero.gear_signatures or {}).get(good) if good not in COIN_GOODS else None
            wear = self._mkt_take(hero, good, n)              # D-333: the most worn copies go first, each with its durability
            order = self._mkt_new_order(hero, "sell", good, price, n, enchant, sig, wear=wear)
            self._mkt_log(sell_orders=1)
            notice = t.t("market.listed", item=self._mkt_label(order), n=n, price=self._money(price))
        else:
            total = price * n
            if hero.gold < total:
                return self._market_draft_view(hero, notice=t.t("market.no_coins", price=self._money(total)))
            hero.gold -= total
            order = self._mkt_new_order(hero, "buy", good, price, n)
            self._mkt_log(buy_orders=1)
            notice = t.t("market.asked", item=self._mkt_name(good), n=n, price=self._money(price), total=self._money(total))
        self.store.delete("market_open", hero.id)
        return self._market_mine_view(hero, notice=notice)

    # ------------------------------------------------------------------ 📥 Pedidos de compra: fill a buy order

    def _market_fill_list(self, hero: Hero, page: int = 0, notice: str | None = None) -> View:
        """📥 Pedidos de compra: every open buy order, the ones you can fill first (you carry that resource), then the best
        price; one line each with /k1, what it asks for, the price, the asker and how many you carry."""
        t = self.texts
        rows = self._mkt_index("buy")
        rows.sort(key=lambda row: (hero.backpack.get(str(row[2]), 0) <= 0,))          # stable: keeps the price order
        per = max(1, int(self._mkt_cfg().get("per_page", 8)))
        pages = max(1, (len(rows) + per - 1) // per)
        page %= pages
        body = [t.t("market.fill_intro")]
        shown: list[str] = []
        for row in rows[page * per:(page + 1) * per]:
            order = self._mkt_order(str(row[1]))
            if order is None:
                continue
            shown.append(order["id"])
            carry = hero.backpack.get(order["good"], 0)
            body.append(t.t("market.ask_order_line", code=f"/k{page * per + len(shown)}", item=self._mkt_name(order["good"]),
                            n=order["n"], price=self._money(order["price"]), name=order.get("name", "?"),
                            carry=t.t("market.you_carry", n=carry) if carry > 0 else "",
                            mine=t.t("market.yours") if order["by"] == hero.id else ""))
        self._codes(hero, "mkt_fill", [""] * (page * per) + shown)
        if not rows:
            body.append(t.t("market.fill_empty"))
        else:
            body += ["", t.t("market.fill_hint")]
            if pages > 1:
                body.append(t.t("market.page", n=page + 1, total=pages))
        actions = [Action(id=f"mkt:fill:{page + 1}", label=t.t("market.more"))] if pages > 1 else []
        actions.append(Action(id="mkt", label=t.t("menu.back")))
        return View(kind="market_fill", title=t.t("market.fill_title"), body=body, actions=actions, notice=notice)

    def _market_bo_view(self, hero: Hero, oid: str, notice: str | None = None) -> View:
        """One buy order: what it asks for, the price, how many, who; 💰 Vender todo lo que puedes (and 💰 Vender 1)."""
        t = self.texts
        order = self._mkt_order(oid)
        if order is None or order.get("side") != "buy":
            return self._market_fill_list(hero, notice=notice or t.t("market.gone"))
        carry = hero.backpack.get(order["good"], 0)
        can = min(carry, int(order["n"]))
        price = int(order["price"])
        body = [self._mkt_name(order["good"]),
                t.t("market.bo_detail", name=order.get("name", "?"), price=self._money(price), n=order["n"],
                    left=self._mkt_left(float(order["until"]) - self.clock.now()),
                    clock=self._clock(float(order["until"]))),       # D-124, D-334: 🕐 when it expires, in your zone
                t.t("market.you_carry_line", n=carry)]
        actions = []
        if order["by"] == hero.id:
            body.append(t.t("market.own_offer"))
        elif can > 0:
            tax = self._mkt_tax(can * price)
            body.append(t.t("market.fill_net", n=can, net=self._money(can * price - tax), tax=self._money(tax)))
            if self._mkt_where(hero) is None:
                body.append(t.t("market.browse_only"))
            actions.append(Action(id=f"mkt:give:{oid}:a", label=t.t("market.give_all", n=can, price=self._money(can * price))))
            if can > 1:
                actions.append(Action(id=f"mkt:give:{oid}:1", label=t.t("market.give_one", price=self._money(price))))
        else:
            body.append(t.t("market.fill_none"))
        actions.append(Action(id="mkt:fill:0", label=t.t("menu.back")))
        return View(kind="market_bo", title=t.t("market.bo_title"), body=body, actions=actions, notice=notice)

    def _market_fill(self, hero: Hero, oid: str, amount: str) -> View:
        """💰 Vender to a buy order: the units leave your backpack, you get price × units minus the tax at once, and the units
        travel to the asker's 📦 Entregas (with a notice). The order shrinks, and closes when it has all it asked for."""
        t = self.texts
        order = self._mkt_order(oid)                      # rule 2: always read fresh from the store
        if order is None or order.get("side") != "buy" or int(order.get("n", 0)) <= 0:
            return self._market_fill_list(hero, notice=t.t("market.gone"))
        if order["by"] == hero.id:
            return self._market_bo_view(hero, oid, notice=t.t("market.own_offer"))
        if self._mkt_where(hero) is None:
            return self._market_bo_view(hero, oid, notice=t.t("market.need_place"))
        good = order["good"]
        carry = hero.backpack.get(good, 0)
        wanted = int(order["n"]) if amount == "a" else (int(amount) if amount.isdigit() else 1)
        n = max(0, min(carry, int(order["n"]), wanted))
        if n <= 0:
            return self._market_bo_view(hero, oid, notice=t.t("market.fill_none"))
        total = n * int(order["price"])
        tax = self._mkt_tax(total)
        self._mkt_take(hero, good, n)
        hero.gold += total - tax                          # the coins were set aside when the order was published
        order["n"] = int(order["n"]) - n
        asker = order["by"]
        self._mkt_box_add(asker, {"good": good, "n": n, "at": self.clock.now() + self._mkt_delivery_seconds(), "from": hero.name,
                                  "why": "filled", "told": False})
        if order["n"] <= 0:
            self._mkt_close(order, "filled", hero)
        else:
            self.store.put("market_order", oid, order)
        self._mkt_log(trades=1, units=n, coins=total, tax=tax)
        seller, label = hero.name, self._mkt_name(good)
        time = self._fmt_duration(self._mkt_delivery_seconds())
        self._push_each([asker], lambda: View(          # built again in the asker's language (D-250)
            kind="market_notice", title=self.texts.t("market.filled_title"),
            body=[self.texts.t("market.filled_line", name=seller, item=self._mkt_name(good), n=n,
                               time=self._fmt_duration(self._mkt_delivery_seconds()))],
            actions=[Action(id="mkt:box", label=self.texts.t("market.box_button", n=len(self._mkt_box(asker))))]))
        return self._market_fill_list(hero, notice=t.t("market.gave", item=label, n=n, net=self._money(total - tax),
                                                       tax=self._money(tax), time=time))

    # ------------------------------------------------------------------ 📝 Pedir recursos: the resource list

    def _market_ask_list(self, hero: Hero, page: int = 0, notice: str | None = None) -> View:
        """📝 Pedir recursos: every resource with its own code (/b07 opens the draft of a buy order for it), its reference price
        and the best open buy order, a page at a time (2 × market.per_page)."""
        t = self.texts
        goods = self._mkt_resources()
        per = max(1, 2 * int(self._mkt_cfg().get("per_page", 8)))
        pages = max(1, (len(goods) + per - 1) // per)
        page %= pages
        best: dict[str, int] = {}
        for row in self._mkt_index("buy"):
            best.setdefault(str(row[2]), int(row[0]))
        body = [t.t("market.ask_intro")]
        for good in goods[page * per:(page + 1) * per]:
            code = int(self.content.items[good]["code"])
            body.append(t.t("market.ask_line", code=f"/b{code:02d}", item=self._mkt_name(good), ref=self._money(self._mkt_ref_price(good)),
                            best=t.t("market.ask_best", price=self._money(best[good])) if good in best else ""))
        body += ["", t.t("market.ask_hint")]
        if pages > 1:
            body.append(t.t("market.page", n=page + 1, total=pages))
        actions = [Action(id=f"mkt:ask:{page + 1}", label=t.t("market.more"))] if pages > 1 else []
        actions.append(Action(id="mkt", label=t.t("menu.back")))
        return View(kind="market_ask", title=t.t("market.ask_title"), body=body, actions=actions, notice=notice)

    # ------------------------------------------------------------------ 📋 Mis órdenes and ❌ cancel

    def _market_mine_view(self, hero: Hero, notice: str | None = None) -> View:
        """📋 Mis órdenes: your active orders (sales and buy orders), with what is left, the price and when each expires; /o1
        opens one to ❌ cancel it."""
        t = self.texts
        ids = []
        body = [t.t("market.mine_intro", n=len(self._mkt_mine(hero.id)), cap=int(self._mkt_cfg().get("max_orders", 10)))]
        now = self.clock.now()
        for oid in self._mkt_mine(hero.id):
            order = self._mkt_order(oid)
            if order is None:
                continue
            ids.append(oid)
            body.append(t.t("market.mine_line_" + order["side"], code=f"/o{len(ids)}",
                            item=self._mkt_label(order) if order["side"] == "sell" else self._mkt_name(order["good"]),
                            n=order["n"], n0=order.get("n0", order["n"]), price=self._money(order["price"]),
                            left=self._mkt_left(float(order["until"]) - now)))
        self._codes(hero, "mkt_mine", ids)
        body += ["", t.t("market.mine_hint")] if ids else [t.t("market.mine_none")]
        return View(kind="market_mine", title=t.t("market.mine_title"), body=body, notice=notice,
                    actions=[Action(id="mkt", label=t.t("menu.back"))])

    def _market_my_view(self, hero: Hero, oid: str, notice: str | None = None) -> View:
        """One of your orders: what is left, the price, the escrow and when it expires; ❌ Cancelar orden gives back what is left."""
        t = self.texts
        order = self._mkt_order(oid)
        if order is None or order.get("by") != hero.id:
            return self._market_mine_view(hero, notice=notice or t.t("market.gone"))
        sell = order["side"] == "sell"
        body = [self._mkt_label(order) if sell else self._mkt_name(order["good"]),
                t.t("market.my_detail_" + order["side"], n=order["n"], n0=order.get("n0", order["n"]), price=self._money(order["price"]),
                    total=self._money(int(order["n"]) * int(order["price"])),
                    left=self._mkt_left(float(order["until"]) - self.clock.now()),
                    clock=self._clock(float(order["until"]))),       # D-124, D-334: 🕐 when it expires, in your zone
                t.t("market.cancel_hint_" + order["side"])]
        actions = [Action(id=f"mkt:x:{oid}", label=t.t("market.cancel_button")), Action(id="mkt:mine", label=t.t("menu.back"))]
        return View(kind="market_order", title=t.t("market.my_title"), body=body, actions=actions, notice=notice)

    def _market_cancel(self, hero: Hero, oid: str) -> View:
        """❌ Cancelar: from anywhere; what is left goes back at once (units to 📦 Entregas, coins to your wallet)."""
        t = self.texts
        order = self._mkt_order(oid)
        if order is None or order.get("by") != hero.id:
            return self._market_mine_view(hero, notice=t.t("market.gone"))
        lines = self._mkt_close(order, "cancelled", hero)
        return self._market_mine_view(hero, notice=self._join([t.t("market.cancelled")] + lines))

    # ------------------------------------------------------------------ 📦 Entregas and 📦 Recoger

    def _market_box_view(self, hero: Hero, notice: str | None = None) -> View:
        """📦 Entregas: what you bought (on its way or arrived) and what came back from your orders; 📦 Recoger when something
        is ready and you are at a bonfire or your camp."""
        t = self.texts
        box = self._mkt_box(hero.id)
        now = self.clock.now()
        body = [t.t("market.box_intro")]
        for entry in box:
            if entry.get("good") == "coins":
                what = self._money(int(entry.get("coins", 0)))
            else:
                what = t.t("market.box_item", item=self._mkt_label(entry), n=entry.get("n", 0))
            when = (t.t("market.box_ready") if float(entry.get("at", 0)) <= now
                    else t.t("market.box_coming", time=self._fmt_duration(float(entry["at"]) - now)))
            source = t.t(f"market.why.{entry.get('why', 'bought')}", name=entry.get("from") or "?")
            body.append(t.t("market.box_entry", what=what, source=source, when=when))
        if not box:
            body.append(t.t("market.box_empty"))
        actions = []
        ready = any(float(e.get("at", 0)) <= now for e in box)
        if ready:
            if self._mkt_can_collect(hero):
                actions.append(Action(id="mkt:get", label=t.t("market.collect_button")))
            else:
                body += ["", t.t("market.collect_where")]
        body += ["", self._bag_space_line(hero)]        # D-338 (0.62): 🎒 types and loose gear
        actions.append(Action(id="mkt", label=t.t("menu.back")))
        return View(kind="market_box", title=t.t("market.box_title"), body=body, actions=actions, notice=notice)

    def _market_collect(self, hero: Hero) -> View:
        """📦 Recoger: everything ready that fits. Coins, 💰 bags and 🪎 chests always fit; items as far as the backpack has
        room (D-338, 0.62: each up to its type's cap, a new type only with a free one, gear up to the loose-pieces cap); a piece
        whose ✨/✒️ clashes with the copy you hold waits (rule 7). What stays, stays (never lost); the notice says which cap."""
        t = self.texts
        if not self._mkt_can_collect(hero):
            return self._market_box_view(hero, notice=t.t("market.collect_where"))
        now = self.clock.now()
        box = self._mkt_box(hero.id)
        got: list[str] = []
        stays: list[dict[str, Any]] = []
        full = clash = False
        blocked: list[str] = []                           # D-338: what waits for room, to say which cap
        for entry in box:
            good = entry.get("good", "")
            if float(entry.get("at", 0)) > now:
                stays.append(entry)
                continue
            if good == "coins":
                hero.gold += int(entry.get("coins", 0))
                got.append(self._money(int(entry.get("coins", 0))))
                continue
            n = int(entry.get("n", 0))
            if good in COIN_GOODS:
                setattr(hero, good, int(getattr(hero, good)) + n)
                got.append(t.t("market.box_item", item=self._mkt_label(entry), n=n))
                continue
            if entry.get("scroll"):                       # D-326: a 🗺️ scroll comes back as its own copy (D-338: 1 of its type)
                if self._bag_room(hero, self._scroll_item()) < 1:
                    full = True
                    blocked.append(self._scroll_item())
                    stays.append(entry)
                    continue
                self._scroll_add(hero, entry["scroll"])
                got.append(t.t("market.box_item", item=self._mkt_label(entry), n=1))
                continue
            if good not in self.content.items or n <= 0:
                stays.append(entry)                      # something no longer in the catalog waits (D-64)
                continue
            holds = hero.backpack.get(good, 0) > 0 or good in hero.gear.values()
            if holds and ((entry.get("enchant") or None) != ((hero.gear_enchants or {}).get(good) or None)
                          or (entry.get("sig") or None) != ((hero.gear_signatures or {}).get(good) or None)):
                clash = True
                stays.append(entry)
                continue
            room = self._bag_room(hero, good)            # D-338: up to its type's cap (or the loose-gear cap)
            take = min(n, room)
            if take <= 0:
                full = True
                blocked.append(good)
                stays.append(entry)
                continue
            hero.backpack[good] = hero.backpack.get(good, 0) + take
            wear = list(entry.get("wear") or [])          # D-333: each unit comes in with its durability
            for rec in wear[:take]:
                durability.put_back(hero, good, rec, self.content.balance)
            if entry.get("enchant"):
                hero.gear_enchants[good] = dict(entry["enchant"])
            if entry.get("sig"):
                hero.gear_signatures[good] = entry["sig"]
            if self.content.items[good].get("kind") == "gear" and good not in hero.gear_new:
                hero.gear_new.append(good)
            got.append(t.t("market.box_item", item=self._mkt_label(entry), n=take))
            if take < n:
                full = True
                blocked.append(good)
                stays.append({**entry, "n": n - take, **({"wear": wear[take:]} if wear else {})})
        self._mkt_box_put(hero.id, stays)
        self._refill_belt(hero)
        lines = [t.t("market.collected", items=", ".join(got))] if got else []
        if full:                                          # D-338: which cap keeps the rest in 📦 Entregas
            lines.append(t.t("market.collect_full", line=self._bag_why(hero, blocked)))
            lines += self._pbag_hint(hero, blocked)
        if clash:
            lines.append(t.t("market.collect_clash"))
        if not lines:
            lines.append(t.t("market.collect_nothing"))
        return self._market_box_view(hero, notice="\n".join(lines))

    # ------------------------------------------------------------------ ❓ Dudas and 📚 Guías numbers

    def _market_faq_values(self) -> dict[str, Any]:
        """The market numbers of ❓ Dudas and 📚 Guías ({market_tax}, {market_delivery}, {market_days}, {market_orders})."""
        cfg = self._mkt_cfg()
        return {"market_tax": round(float(cfg.get("tax", 0.05)) * 100),
                "market_delivery": self._fmt_duration(float(cfg.get("delivery_minutes", 30)) * 60),
                "market_days": int(cfg.get("order_days", 7)), "market_orders": int(cfg.get("max_orders", 10))}
