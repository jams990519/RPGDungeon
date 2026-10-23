"""🗺️ Pergamino de mapa: the 🧭 Explorador's map scroll (D-311 part 5, D-213, E-180; how it was applied: D-326).

From balance.yaml map_scroll.rank, a 🧭 Explorador makes a scroll with the zones of its 6 × 6 region (a fixed grid,
map_scroll.region) that it investigated itself to map_view.fog.color_at (50 %) or more, if there are at least
map_scroll.min_zones of them; it costs map_scroll.energy and map_scroll.materials and gives map_scroll.explorer_xp. Each copy
is its own record in Hero.map_scrolls (zones, author, region) and the backpack only counts them, like a ✒️ masterwork carries
its signature. Whoever uses one (📜 Usar) sees those zones in colour for ever (Hero.charted): only the map colour and the
legend, never the resources, the nodes, the places or "Moverte allá". It is sold in the 🏛️ Mercado (market.py, category
"maps") at a free price inside map_scroll.price_min/price_max.

[ES]
Para qué sirve: la parte 5 de D-311 (confirmada por el dueño, E-180): "el 🧭 Explorador hace un 🗺️ pergamino con las zonas que
    exploró al 50 % o más de una región de 6 × 6 y lo vende al precio que quiera; quien lo usa ve esos colores para siempre".
    La forma (botones, región fija, números) la eligió Claude en la capa simple (D-44): D-326, provisional. Es parte de
    GameService (una "mezcla", como MarketMixin), en su propio archivo para no agrandar game.py.
Documento de diseño: diseno/02-mundo/mapa-infinito-y-viaje.md §1.9.4; diseno/07-economia/economia.md §3.0 (la venta)
Módulo: capa de servicios (M8 Mundo: el mapa de cada héroe; M13 Economía: algo que se vende)
Depende de: content/balance.yaml (bloque map_scroll; map_view.fog.color_at; explorer.profession), content/items.yaml
    (pergamino_mapa, kind map_scroll), content/locales/es_pergamino.yaml y en_pergamino.yaml (textos), engine.hero (Hero) y
    las ayudas de GameService (_fog_cfg, _fog_stage, _known_pct, _known_terrains, _terrain_label, _zone, _zone_name,
    _explorer_rank, _explorer_cfg, _prof_gain, _prof_name, _spend_energy, _no_energy_notice, _item_list, _codes, _code_target,
    _status_line); D-338 (0.62): _bag_room y _bag_no_room de engine/service/backpack.py (los pergaminos son un tipo de la
    mochila, hasta 30: hacer uno pide lugar)
Lo usan: engine/service/game.py (GameService hereda de esta clase): _idle_action (SCROLL_ACTIONS: "scrolls" y "scr:…", también
    ocupado: es un menú), text() (/pm1 con SCROLL_CODE_RE, fuera de combate), COMMANDS (/pergaminos, /scrolls), _load
    (_scroll_sync), _fog_cell y _zone_view (_charted_set), _known_terrains y _fog_notices (las zonas de Hero.charted), _map_view
    (el botón 🗺️ Pergaminos, _scroll_shows), _bag_view (_scroll_bag_lines), _explorer_unlocks y _explorer_prof_lines
    (_explorer_thresholds: el umbral "map_scroll"); engine/service/market.py (_scroll_item, _scroll_find, _scroll_take,
    _scroll_add, _scroll_summary, _scroll_new y la banda de precio)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño:
    Hero.map_scrolls (cada pergamino que lleva el héroe: {"id", "by", "center", "size", "zones", "at"}) y Hero.charted (las zonas
        que ve a color por un pergamino) — se guardan en la ficha del héroe (espacio "hero").
    "meta"/"map_scroll": {"seq"}: el último número de pergamino ("p1", "p2"…; nunca se reutiliza).
    "gremio_codes" (de gremio.py) suma "scrolls": el orden de la lista de 🗺️ Pergaminos con /pm1 (solo pantalla).
Reglas que nunca se rompen:
    1. Solo el color (D-311.5): un pergamino nunca toca exploration, known, nodes ni lo que pide fundar; por eso no da recursos,
       ni nodos, ni lugares, ni "Moverte allá" (D-222).
    2. La mochila cuenta lo que hay en Hero.map_scrolls (_scroll_sync); los datos mandan. Todo pergamino que entra o sale pasa
       por _scroll_add y _scroll_take (también los del 🏛️ Mercado). Nada se pierde (D-64): un pergamino está en una mochila, en
       una orden o en 📦 Entregas, hasta que alguien lo usa.
    3. Solo entra lo que el autor investigó él mismo al 50 % (no lo de su gremio ni lo de otro pergamino), y nunca las 🔥 fogatas
       (se ven siempre).
    4. Ningún texto visible se escribe aquí: todo sale de content/locales (es_pergamino.yaml y en_pergamino.yaml).
Si cambias esto, revisa:
    - Números: balance.yaml map_scroll (rank, region, min_zones, energy, materials, explorer_xp, price_min, price_max); el
      registro de balance (diseno/03-personaje/balance.md)
    - Pantallas y botones: "scrolls", "scr:make", "scr:do", "scr:v:<id>", "scr:use:<id>" (ids estables) y el tope de 4 botones
    - Mapa de impacto: diseno/01-plataforma/mapa-de-impacto.md (M8 "🗺️ Pergamino de mapa", M13 y la cascada C-32)
    - Pruebas: tests/test_pergamino_mapa.py; tests/test_mercado.py (las categorías de 🛍️ Comprar)
"""

from __future__ import annotations

import re
from typing import Any

from engine.hero import Hero
from engine.messaging import Action, View
from engine.world import mapgen

# Button ids of the map scrolls: the list ("scrolls") and "scr:<what>[:<id>]". [ES] Los botones del pergamino (ids estables).
SCROLL_ACTIONS = ("scrolls", "scr:")
# /pm1 = the 1st scroll of the last 🗺️ Pergaminos list. [ES] El código de cada pergamino de la lista (no choca con /p1 ni /m1).
SCROLL_CODE_RE = re.compile(r"^/pm_?(\d{1,2})(@\w+)?$")


class MapScrollMixin:
    """🗺️ Pergamino de mapa (D-311 part 5, D-326). Mixed into GameService; uses its helpers (see the module's [ES] header).

    [ES]
    Qué es: hacer, guardar, usar y mostrar los pergaminos de mapa del 🧭 Explorador.
    Quién la usa: GameService (hereda de esta clase) y MarketMixin (para venderlos).
    Si cambia, afecta: el 🗺️ Mapa de quien usa un pergamino y lo que se vende en 🏛️ Mercado → 🗺️ Mapas.
    """

    # ------------------------------------------------------------------ config and the region grid

    def _scroll_cfg(self) -> dict[str, Any]:
        return self.content.balance.get("map_scroll", {})

    def _scroll_item(self) -> str:
        """The item id the backpack counts scrolls with (map_scroll.item, "pergamino_mapa")."""
        return str(self._scroll_cfg().get("item", "pergamino_mapa"))

    def _scroll_size(self) -> int:
        return max(1, int(self._scroll_cfg().get("region", 6)))

    def _scroll_region(self, x: int, y: int) -> tuple[int, int]:
        """The region (rx, ry) of a zone on the fixed grid of map_scroll.region zones; the Claro's is (0, 0), from (-3, -3)
        to (2, 2), and each 🔥 bonfire (every 12 zones) falls near the middle of its own."""
        size = self._scroll_size()
        half = size // 2
        return (x + half) // size, (y + half) // size

    def _scroll_center(self, rx: int, ry: int) -> tuple[int, int]:
        size = self._scroll_size()
        return rx * size, ry * size

    @staticmethod
    def _scroll_bounds_of(center: tuple[int, int], size: int) -> tuple[int, int, int, int]:
        """(x0, y0, x1, y1) of the square of `size` zones around `center` (the center sits at offset size // 2)."""
        half = size // 2
        x0, y0 = int(center[0]) - half, int(center[1]) - half
        return x0, y0, x0 + size - 1, y0 + size - 1

    def _scroll_name(self, data: dict[str, Any]) -> str:
        """"Región de Vado Gris (6, 0)": the name and coordinates of the zone at the center of a scroll's region."""
        cx, cy = (int(v) for v in (data.get("center") or [0, 0]))
        return self.texts.t("scroll.region", name=self._zone_name(self._zone(cx, cy)), x=cx, y=cy)

    def _scroll_place(self, data: dict[str, Any]) -> str:
        """Only the center zone's name, for a short button label."""
        cx, cy = (int(v) for v in (data.get("center") or [0, 0]))
        return self._zone_name(self._zone(cx, cy))

    def _scroll_summary(self, data: dict[str, Any]) -> str:
        """"Región de Vado Gris (6, 0) · 9 zonas · ✍️ Lyra": one scroll in one line (lists, the market, notices)."""
        return self.texts.t("scroll.summary", region=self._scroll_name(data), n=len(data.get("zones") or []),
                            by=data.get("by") or "?")

    # ------------------------------------------------------------------ what a hero sees in colour

    def _charted_set(self, hero: Hero) -> set[str]:
        """Hero.charted as a set, kept for this request (charted only grows, so its length says when to build it again)."""
        memo = hero.__dict__.get("_charted_memo")
        if memo is None or memo[0] != len(hero.charted):
            memo = (len(hero.charted), set(hero.charted))
            hero.__dict__["_charted_memo"] = memo
        return memo[1]

    def _sees_colour(self, hero: Hero, key: str) -> bool:
        """True if zone "x:y" already shows its colour on this hero's map: a 🔥 bonfire, investigated to color_at (by the hero
        or its guild, D-282) or charted by a scroll."""
        x, y = (int(v) for v in key.split(":"))
        if mapgen.is_bonfire(x, y) or key in self._charted_set(hero):
            return True
        return self._known_pct(hero, x, y) >= int(self._fog_cfg()["color_at"])

    def _scroll_new(self, hero: Hero, zones: list[str]) -> list[str]:
        """The zones of a scroll this hero does not see in colour yet (what using it would add)."""
        return [key for key in zones if isinstance(key, str) and ":" in key and not self._sees_colour(hero, key)]

    def _scroll_own_zones(self, hero: Hero, rx: int, ry: int) -> list[str]:
        """The zones of region (rx, ry) the hero itself investigated to color_at (50 %) or more, north row first; never a
        🔥 bonfire (always in colour) and never what only its guild or a scroll gave it (rule 3)."""
        color_at = int(self._fog_cfg()["color_at"])
        x0, y0, x1, y1 = self._scroll_bounds_of(self._scroll_center(rx, ry), self._scroll_size())
        return [f"{x}:{y}" for y in range(y1, y0 - 1, -1) for x in range(x0, x1 + 1)
                if not mapgen.is_bonfire(x, y) and int(hero.exploration.get(f"{x}:{y}", 0)) >= color_at]

    # ------------------------------------------------------------------ the copies a hero carries (rule 2)

    def _scroll_sync(self, hero: Hero) -> None:
        """The backpack counts the scrolls the hero carries: map_scroll.item = len(Hero.map_scrolls), or nothing."""
        item = self._scroll_item()
        n = len(hero.map_scrolls)
        if n:
            hero.backpack[item] = n
        else:
            hero.backpack.pop(item, None)

    def _scroll_add(self, hero: Hero, data: dict[str, Any]) -> None:
        hero.map_scrolls.append(dict(data))
        self._scroll_sync(hero)

    def _scroll_find(self, hero: Hero, sid: str | None) -> dict[str, Any] | None:
        return next((s for s in hero.map_scrolls if sid and s.get("id") == sid), None)

    def _scroll_take(self, hero: Hero, sid: str | None) -> dict[str, Any] | None:
        """Take one scroll out of the hero (to use it or to put it in a market order); None if it does not carry it."""
        data = self._scroll_find(hero, sid)
        if data is None:
            return None
        hero.map_scrolls = [s for s in hero.map_scrolls if s is not data]
        self._scroll_sync(hero)
        return data

    def _scroll_rank_ok(self, hero: Hero) -> bool:
        return self._explorer_rank(hero) >= int(self._scroll_cfg().get("rank", 15))

    def _scroll_shows(self, hero: Hero) -> bool:
        """The 🗺️ Pergaminos button shows when you carry one or your 🧭 rank makes them (D-287: what is locked is not shown)."""
        return bool(hero.map_scrolls) or self._scroll_rank_ok(hero)

    def _scroll_bag_lines(self, hero: Hero) -> list[str]:
        """🎒 Mochila: one line when the hero carries scrolls (they are not in 📦 Recursos)."""
        return [self.texts.t("scroll.bag_line", n=len(hero.map_scrolls))] if hero.map_scrolls else []

    def _explorer_thresholds(self) -> list[tuple[str, int]]:
        """explorer.ranks plus the 🗺️ scroll's rank (map_scroll.rank, "map_scroll"), lowest first (a stable sort keeps the
        order of equal ranks). [ES] Lo leen _explorer_unlocks y _explorer_prof_lines: así el rango del pergamino se avisa y se
        lista como los demás umbrales del 🧭 Explorador."""
        pairs = [(key, int(rank)) for key, rank in self._explorer_cfg()["ranks"].items()]
        if self._scroll_cfg().get("rank") is not None:
            pairs.append(("map_scroll", int(self._scroll_cfg()["rank"])))
        return sorted(pairs, key=lambda kv: kv[1])

    # ------------------------------------------------------------------ screens

    def _scroll_action(self, hero: Hero, action_id: str) -> View:
        """Route "scrolls" and "scr:…". Menus and using a scroll work while busy (nothing moves you); never in a fight.

        [ES] Qué hace: reparte los botones del pergamino. La llama: _idle_action. Si cambia, afecta: los botones "scr:…"
        (ids estables: solo se agregan)."""
        parts = action_id.split(":")
        what = parts[1] if len(parts) > 1 else ""
        arg = parts[2] if len(parts) > 2 else ""
        if what == "make":
            return self._scroll_make_view(hero)
        if what == "do":
            return self._scroll_make(hero)
        if what == "v":
            return self._scroll_view(hero, arg)
        if what == "use":
            return self._scroll_use(hero, arg)
        return self._scrolls_view(hero)

    def _scroll_code(self, hero: Hero, n: int) -> View:
        """/pm2: the 2nd scroll of the last 🗺️ Pergaminos list (typed or tapped)."""
        sid = self._code_target(hero, "scrolls", n)
        if not sid or self._scroll_find(hero, sid) is None:
            return self._scrolls_view(hero, notice=self.texts.t("scroll.bad_code", code=f"/pm{n}"))
        return self._scroll_view(hero, sid)

    def _scrolls_view(self, hero: Hero, notice: str | None = None) -> View:
        """🗺️ Pergaminos: what a scroll is, the ones you carry (each with /pm1, its region, zones, author and how many are new
        for you) and, from the 🧭 rank, 🗺️ Hacer pergamino.

        [ES]
        Qué hace: la pantalla de los pergaminos de mapa (D-326). Cada pergamino que llevas en una línea con su código (/pm1):
        región, zonas, quién lo hizo y cuántas zonas todavía no ves a color (🆕). Botones: 🗺️ Hacer pergamino (desde
        map_scroll.rank del 🧭 Explorador), los primeros pergaminos (abren su ficha con 📜 Usar) y ↩️ Volver al 🗺️ Mapa: 4 como
        mucho. La llaman: el botón 🗺️ Pergaminos del 🗺️ Mapa, /pergaminos, /scrolls y la línea de la 🎒 Mochila.
        Si cambia, afecta: tests/test_pergamino_mapa.py.
        """
        t = self.texts
        body = [t.t("scroll.intro", pct=int(self._fog_cfg()["color_at"]), size=self._scroll_size())]
        ids: list[str] = []
        if hero.map_scrolls:
            body += ["", t.t("scroll.yours_title", n=len(hero.map_scrolls))]
            for data in hero.map_scrolls:
                ids.append(str(data.get("id")))
                body.append(t.t("scroll.line", code=f"/pm{len(ids)}", summary=self._scroll_summary(data),
                                new=len(self._scroll_new(hero, data.get("zones") or []))))
            body.append(t.t("scroll.use_hint"))
        else:
            body += ["", t.t("scroll.none")]
        self._codes(hero, "scrolls", ids)
        actions: list[Action] = []
        if self._scroll_rank_ok(hero):
            body += ["", t.t("scroll.make_hint", rank=int(self._scroll_cfg().get("rank", 15)))]
            actions.append(Action(id="scr:make", label=t.t("scroll.make_button")))
        for n, data in enumerate(hero.map_scrolls[:3 - len(actions)], 1):
            actions.append(Action(id=f"scr:v:{data.get('id')}", label=t.t("scroll.open_button", n=n, name=self._scroll_place(data))))
        actions.append(Action(id="map", label=t.t("menu.back")))
        return View(kind="map_scrolls", title=t.t("scroll.title"), body=body, actions=actions, notice=notice)

    def _scroll_view(self, hero: Hero, sid: str, notice: str | None = None) -> View:
        """One scroll you carry: its region and corners, who made it, how many zones it shows and how many are new for you;
        📜 Usar and ↩️ Volver."""
        t = self.texts
        data = self._scroll_find(hero, sid)
        if data is None:
            return self._scrolls_view(hero, notice=notice or t.t("scroll.gone"))
        zones = list(data.get("zones") or [])
        new = self._scroll_new(hero, zones)
        x0, y0, x1, y1 = self._scroll_bounds_of(tuple(data.get("center") or [0, 0]), int(data.get("size") or self._scroll_size()))
        body = [self._scroll_name(data), t.t("scroll.by", name=data.get("by") or "?"),
                t.t("scroll.zones_line", n=len(zones), x0=x0, y0=y0, x1=x1, y1=y1),
                t.t("scroll.new_line", n=len(new)) if new else t.t("scroll.nothing_new"),
                "", t.t("scroll.use_explain")]
        actions = [Action(id=f"scr:use:{sid}", label=t.t("scroll.use_button")), Action(id="scrolls", label=t.t("menu.back"))]
        return View(kind="map_scroll", title=t.t("scroll.item_title"), body=body, actions=actions, notice=notice)

    def _scroll_use(self, hero: Hero, sid: str) -> View:
        """📜 Usar: the scroll is spent and its zones show in colour on your map for ever (Hero.charted); says how many were
        new and which terrains joined your legend. Only the colour (rule 1).

        [ES] Qué hace: gasta el pergamino y suma sus zonas a Hero.charted (sin repetir; también las que ya veías a color por tu
        gremio, que podrías dejar de ver si te vas: el pergamino es para siempre). Dice cuántas zonas son nuevas en tu mapa y
        los terrenos que entran a tu leyenda. La llaman: el botón 📜 Usar de la ficha del pergamino. Si cambia, afecta:
        tests/test_pergamino_mapa.py.
        """
        t = self.texts
        data = self._scroll_take(hero, sid)
        if data is None:
            return self._scrolls_view(hero, notice=t.t("scroll.gone"))
        zones = [key for key in (data.get("zones") or []) if isinstance(key, str) and ":" in key]
        new = self._scroll_new(hero, zones)
        before = set(self._known_terrains(hero))
        charted = set(self._charted_set(hero))
        for key in zones:
            x, y = (int(v) for v in key.split(":"))
            if key not in charted and not mapgen.is_bonfire(x, y):
                hero.charted.append(key)
                charted.add(key)
        lines = [t.t("scroll.used", region=self._scroll_name(data), n=len(new), total=len(zones))]
        joined = [biome for biome in self._known_terrains(hero) if biome not in before]
        if joined:
            lines.append(t.t("scroll.new_terrains", terrains=" · ".join(self._terrain_label(b) for b in joined),
                             n=len(self._known_terrains(hero)), total=len(self.content.biomes)))
        return self._scrolls_view(hero, notice="\n".join(lines))

    def _scroll_minimap(self, hero: Hero, rx: int, ry: int) -> list[str]:
        """The region as the scroll would draw it: 🧍 you, 🔥 bonfires, the colour of each zone you investigated to 50 % (it
        goes in) and ▫️ the rest (it does not)."""
        color_at = int(self._fog_cfg()["color_at"])
        blank = self._fog_stage(0)["mark"]
        x0, y0, x1, y1 = self._scroll_bounds_of(self._scroll_center(rx, ry), self._scroll_size())
        rows = []
        for y in range(y1, y0 - 1, -1):
            row = ""
            for x in range(x0, x1 + 1):
                if (x, y) == (hero.x, hero.y):
                    row += "🧍"
                elif mapgen.is_bonfire(x, y) or int(hero.exploration.get(f"{x}:{y}", 0)) >= color_at:
                    biome = self.content.biomes[self._zone(x, y).biome]
                    row += biome.get("color", biome["emoji"])
                else:
                    row += blank
            rows.append(row)
        return rows

    def _scroll_missing(self, hero: Hero, zones: list[str]) -> list[str]:
        """Why a scroll cannot be made now (empty when it can): too few zones, materials, energy or, since 0.62 (D-338), no
        room for it in the backpack (its type full at 30, or a new type with none free)."""
        t = self.texts
        cfg = self._scroll_cfg()
        lines = []
        need = int(cfg.get("min_zones", 6))
        if len(zones) < need:
            lines.append(t.t("scroll.need_zones", n=need - len(zones), need=need, pct=int(self._fog_cfg()["color_at"])))
        materials = {i: int(n) for i, n in (cfg.get("materials") or {}).items()}
        missing = {i: n for i, n in materials.items() if hero.backpack.get(i, 0) < n}
        if missing:
            lines.append(t.t("scroll.need_items", items=self._item_list(missing)))
        if hero.energy < int(cfg.get("energy", 5)):
            lines.append(self._no_energy_notice(hero))
        if not missing:                                 # D-338 (0.62): the new scroll needs room in its type
            after = {i: n - materials.get(i, 0) for i, n in hero.backpack.items() if n - materials.get(i, 0) > 0}
            if self._bag_room(hero, self._scroll_item(), after) < 1:
                lines.append(self._bag_no_room(hero, self._scroll_item()))
        return lines

    def _scroll_make_view(self, hero: Hero, notice: str | None = None) -> View:
        """🗺️ Hacer pergamino: your region (a minimap of what would go in), how many zones at 50 % it holds against the minimum,
        the cost and the 🧭 experience; ✅ Hacer pergamino only when everything is there.

        [ES]
        Qué hace: la pantalla para hacer un pergamino (D-326). La región es la de la cuadrícula fija donde estás parado
        (map_scroll.region: 6 × 6). Un minimapa muestra lo que entraría (a color: lo que investigaste tú al 50 %; ▫️ lo que no;
        🔥 las fogatas, que no cuentan), cuántas zonas son contra el mínimo (map_scroll.min_zones), lo que cuesta (⚡ y
        materiales) y la experiencia de 🧭 Explorador. Si falta algo, lo dice y no muestra el botón. Sin el rango vuelve a
        🗺️ Pergaminos con el aviso. La llaman: 🗺️ Hacer pergamino. Si cambia, afecta: tests/test_pergamino_mapa.py.
        """
        t = self.texts
        cfg = self._scroll_cfg()
        if not self._scroll_rank_ok(hero):
            return self._scrolls_view(hero, notice=t.t("scroll.need_rank", rank=int(cfg.get("rank", 15)),
                                                       have=self._explorer_rank(hero)))
        rx, ry = self._scroll_region(hero.x, hero.y)
        center = self._scroll_center(rx, ry)
        size = self._scroll_size()
        x0, y0, x1, y1 = self._scroll_bounds_of(center, size)
        zones = self._scroll_own_zones(hero, rx, ry)
        materials = {i: int(n) for i, n in (cfg.get("materials") or {}).items()}
        body = [t.t("scroll.make_intro", pct=int(self._fog_cfg()["color_at"])), "",
                t.t("scroll.make_region", region=self._scroll_name({"center": list(center)}), x0=x0, y0=y0, x1=x1, y1=y1, size=size)]
        body += self._scroll_minimap(hero, rx, ry)
        body += [t.t("scroll.make_legend", blank=self._fog_stage(0)["mark"], pct=int(self._fog_cfg()["color_at"])), "",
                 t.t("scroll.make_zones", n=len(zones), need=int(cfg.get("min_zones", 6))),
                 t.t("scroll.make_cost", energy=int(cfg.get("energy", 5)), items=self._item_list(materials)),
                 t.t("scroll.make_xp", name=self._prof_name(self._explorer_cfg()["profession"]), xp=int(cfg.get("explorer_xp", 0)))]
        missing = self._scroll_missing(hero, zones)
        actions = []
        if missing:
            body += [""] + missing
        else:
            actions.append(Action(id="scr:do", label=t.t("scroll.do_button", energy=int(cfg.get("energy", 5)))))
        body += ["", self._status_line(hero)]
        actions.append(Action(id="scrolls", label=t.t("menu.back")))
        return View(kind="map_scroll_make", title=t.t("scroll.make_title"), body=body, actions=actions, notice=notice)

    def _scroll_make(self, hero: Hero) -> View:
        """✅ Hacer pergamino: checks the rank, the zones, the materials and the energy (nothing is spent if one fails); then
        spends them, puts a new scroll in the backpack and gives the 🧭 Explorador its experience.

        [ES] Qué hace: hace el pergamino de tu región con las zonas que investigaste tú al 50 % (map_scroll). Gasta la energía y
        los materiales, le pone un número que nunca se repite ("meta"/"map_scroll"), tu nombre, el centro y el tamaño de la
        región y sus zonas, lo suma a la mochila (_scroll_add) y da map_scroll.explorer_xp de 🧭 Explorador. Se puede en
        cualquier lugar y aunque estés en un lote (no te mueve), nunca en una pelea. La llaman: el botón ✅ Hacer pergamino.
        Si cambia, afecta: tests/test_pergamino_mapa.py.
        """
        t = self.texts
        cfg = self._scroll_cfg()
        if not self._scroll_rank_ok(hero):
            return self._scroll_make_view(hero)
        rx, ry = self._scroll_region(hero.x, hero.y)
        zones = self._scroll_own_zones(hero, rx, ry)
        missing = self._scroll_missing(hero, zones)
        if missing:
            return self._scroll_make_view(hero, notice=self._join(missing))
        if not self._spend_energy(hero, "map_scroll", int(cfg.get("energy", 5))):
            return self._scroll_make_view(hero, notice=self._no_energy_notice(hero))
        for item_id, n in (cfg.get("materials") or {}).items():
            hero.backpack[item_id] = hero.backpack.get(item_id, 0) - int(n)
            if hero.backpack[item_id] <= 0:
                del hero.backpack[item_id]
        meta = self.store.get("meta", "map_scroll") or {"seq": 0}
        meta["seq"] = int(meta.get("seq", 0)) + 1
        self.store.put("meta", "map_scroll", meta)
        center = self._scroll_center(rx, ry)
        data = {"id": f"p{meta['seq']}", "by": hero.name, "center": list(center), "size": self._scroll_size(),
                "zones": zones, "at": self.clock.now()}
        self._scroll_add(hero, data)
        xp = int(cfg.get("explorer_xp", 0))
        pid = self._explorer_cfg()["profession"]
        lines = [t.t("scroll.made", summary=self._scroll_summary(data)),
                 t.t("scroll.made_xp", name=self._prof_name(pid), xp=xp)]
        lines += self._prof_gain(hero, pid, xp)
        lines.append(t.t("scroll.sell_hint"))
        return self._scrolls_view(hero, notice="\n".join(lines))
