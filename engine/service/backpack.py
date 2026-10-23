"""🎒 The backpack counts item TYPES, not units, and the 🎒 profession backpacks (D-338, confirmed; how: D-339, provisional; 0.62).

"Today's backpack (60 of space) fills up too fast. I want to farm much more, even if it takes longer, and the limit to be the
inventory." The backpack holds up to balance.yaml hero.backpack.types (50) distinct item types with up to per_type (30) units
of each: every item that is not gear counts (resources, potions and remedies, food, furniture, map scrolls, profession
backpacks that are not on…). Loose gear pieces go apart with their own cap (gear_pieces, 20): each piece is unique and never
stacks. What is worn and the belt never count. A 🎒 profession backpack that is ON (Hero.prof_bags, up to prof_slots, of
different professions) gives the resources of its profession (gathers, skins and rare of content/professions.yaml) their own
compartment: they do not use the general types and hold up to its per_type (40 or 50, balance.yaml prof_backpacks). Nothing is
ever lost (D-338.4, D-90): a hero over a cap keeps everything and only cannot add more of that type, or new types, until it is
below; loot, finds and rewards still enter past the caps (_bag_add). What checks the caps: gathering (each unit, per resource;
🪓 Talar and 🎣 Pescar too) and its batches, the Claro trader, 📦 Entregas, crafting results, the ⚔️ Armería, the 🗺️ scroll.

[ES]
Para qué sirve: la mochila por tipos que pidió el dueño (D-338, confirmada el 23-oct-2026: "la mochila de hoy se llena demasiado
    rápido; quiero poder farmear mucho más, aunque tarde, y que el límite sea el inventario"): cuántos tipos y cuántas unidades
    de cada uno caben, el equipo suelto aparte, las 🎒 mochilas de oficio (ponérselas y quitárselas desde 🎒 Mochila, su
    compartimento y su tope) y los avisos de qué tope frena. Cómo se aplicó lo eligió Claude (D-339, provisional; E-287 a E-289).
    Es parte de GameService (una "mezcla", como RepairMixin), en su propio archivo para no agrandar game.py.
Documento de diseño: diseno/03-personaje/inventario-y-mochilas.md §0 (cómo está en el juego); diseno/07-economia/profesiones.md
    §0.14; diseno/03-personaje/balance.md (registro de balance, 0.62)
Módulo: capa de servicios (M4 Equipo e inventario: la mochila; M14 Oficios: quién hace las mochilas de oficio)
Depende de: content/balance.yaml (hero.backpack: types, per_type, gear_pieces, prof_slots; prof_backpacks.items), content/items.yaml
    (kind: gear no cuenta como tipo; kind: prof_bag), content/professions.yaml (gathers, skins y rare de cada oficio: lo que va
    al compartimento; las recetas de las mochilas), content/locales/es_mochila.yaml y en_mochila.yaml (textos) y las ayudas de
    GameService (_perks: el beneficio "bag" suma tipos; _prof_name, _prof_catalog, _recipes, _item_label, _codes, _code_target,
    _join)
Lo usan: engine/service/game.py (GameService hereda de esta clase): _gather_step, _gather_blocked, _continue_batch y
    _batch_summary (recolectar, 🪓 Talar, 🎣 Pescar y sus lotes), _trade_gather (la unidad de más), _buy y las pantallas del
    mercader, _make y _recipe_view (lo que sale tiene que caber), _amount_view, _activity_view y _explore_menu (la línea de la
    mochila), _bag_view, _resources_view y _hero_view (tipos y "x/30"), _idle_action (PBAG_ACTIONS), text() (/mp1 /mq1 con
    PBAG_CODE_RE), _faq_values (_pack_faq_values: ❓ /d30 y /d67, 📚 Guías); engine/service/market.py (📦 Recoger),
    engine/service/gremio.py (⚔️ Armería), engine/service/map_scroll.py (hacer un pergamino) y engine/service/guide.py
    (el aviso "bag_full": sin tipos libres)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: Hero.prof_bags (engine/hero/hero.py): las mochilas de oficio puestas. "gremio_codes" (de gremio.py)
    suma "pbag_on" (/mp1: las de la mochila) y "pbag_off" (/mq1: las puestas): solo pantalla.
Reglas que nunca se rompen:
    1. Nada se pierde (D-338.4, D-90, D-64): pasar un tope nunca borra nada; solo frena sumar más de ese tipo o tipos nuevos.
       Lo que se encuentra (botín, hallazgos, premios, la unidad de más del refinado) entra aunque pase el tope.
    2. El equipo nunca cuenta como tipo: va aparte, con gear_pieces. Lo puesto y el cinturón nunca cuentan.
    3. Hasta prof_slots mochilas de oficio puestas, de oficios distintos; quitarse una siempre se puede (sus recursos vuelven a
       contar como tipos, aunque pasen el tope).
    4. Ningún texto visible se escribe aquí: todo sale de content/locales (es_mochila.yaml y en_mochila.yaml).
Si cambias esto, revisa:
    - Números: balance.yaml hero.backpack y prof_backpacks; el registro de balance (diseno/03-personaje/balance.md, 0.62)
    - Pantallas y botones: 🎒 Mochila ("bag": 5 botones con 🎒 Mochilas de oficio, EXTRA_BUTTON_KINDS en game.py), "pbags"
      (hasta 4 botones), 📦 Recursos ("x/30"); los códigos /mp y /mq no pueden chocar con los de antes
    - Mapa de impacto: diseno/01-plataforma/mapa-de-impacto.md (M4 "El espacio de la mochila" y la cascada C-41)
    - Pruebas: tests/test_mochila_por_tipos.py; tests/test_backpack.py, test_resources.py, test_talar.py, test_professions.py,
      test_playtest_fixes.py, test_camino_guiado.py y test_mercado.py (los topes de antes)
"""

from __future__ import annotations

import re
from typing import Any

from engine.hero import Hero
from engine.messaging import Action, View

# Button ids (stable): the 🎒 Mochilas de oficio screen. [ES] El botón de la pantalla de las mochilas de oficio.
PBAG_ACTIONS = ("pbags",)
# /mp1 = put on the 1st profession backpack listed as carried; /mq1 = take off the 1st one listed as on. [ES] Los códigos.
PBAG_CODE_RE = re.compile(r"^/(mp|mq)_?(\d{1,2})(@\w+)?$")


class BackpackMixin:
    """The backpack by types and the 🎒 profession backpacks (D-338, D-339). Mixed into GameService (see the module's header).

    [ES]
    Qué es: los topes de la mochila (tipos, unidades por tipo, equipo suelto), las mochilas de oficio y sus pantallas.
    Quién la usa: GameService (hereda de esta clase); market.py, gremio.py, map_scroll.py y guide.py usan sus ayudas.
    Si cambia, afecta: cuánto se puede juntar, comprar, recoger y fabricar antes de vender o usar cosas (C-41).
    """

    # ------------------------------------------------------------------ numbers

    def _pack_cfg(self) -> dict[str, Any]:
        """balance.yaml hero.backpack (types, per_type, gear_pieces, prof_slots)."""
        return self.content.balance["hero"].get("backpack") or {}

    def _pack_types(self) -> int:
        return int(self._pack_cfg().get("types", 50))

    def _pack_per_type(self) -> int:
        return int(self._pack_cfg().get("per_type", 30))

    def _pack_gear_cap(self) -> int:
        return int(self._pack_cfg().get("gear_pieces", 20))

    def _pbag_slots(self) -> int:
        return int(self._pack_cfg().get("prof_slots", 3))

    def _pbag_defs(self) -> dict[str, dict[str, Any]]:
        """balance.yaml prof_backpacks.items that exist in content/items.yaml: item id -> {"profession", "per_type"}."""
        items = (self.content.balance.get("prof_backpacks") or {}).get("items") or {}
        return {iid: dict(d) for iid, d in items.items() if iid in self.content.items and d.get("profession")}

    def _pbag_resources(self, pid: str) -> list[str]:
        """What a profession's backpack keeps in its compartment: its gathers, its skins and its rare find (D-339)."""
        pdef = ((self.content.professions or {}).get("professions") or {}).get(pid) or {}
        out = list(pdef.get("gathers") or []) + list(pdef.get("skins") or [])
        rare = (pdef.get("rare") or {}).get("item")
        if rare and rare not in out:
            out.append(rare)
        return out

    def _pbag_best(self, pid: str) -> int:
        """The best per-type cap a backpack of this profession gives (0 if the profession has none)."""
        return max((int(d.get("per_type", 0)) for d in self._pbag_defs().values() if d["profession"] == pid), default=0)

    def _pbag_worn(self, hero: Hero) -> list[str]:
        """The profession backpacks the hero has on (unknown ids are skipped, never deleted: D-64)."""
        defs = self._pbag_defs()
        return [iid for iid in (hero.prof_bags or []) if iid in defs]

    def _pbag_pockets(self, hero: Hero) -> dict[str, int]:
        """Resource id -> its per-type cap, for every resource of a profession whose backpack the hero has on."""
        defs = self._pbag_defs()
        out: dict[str, int] = {}
        for iid in self._pbag_worn(hero):
            cap = int(defs[iid].get("per_type", self._pack_per_type()))
            for res in self._pbag_resources(defs[iid]["profession"]):
                out[res] = max(out.get(res, 0), cap)
        return out

    # ------------------------------------------------------------------ counting (rule 2: gear apart; worn and belt never)

    def _bag_is_gear(self, item_id: str) -> bool:
        return (self.content.items.get(item_id) or {}).get("kind") == "gear"

    def _bag_types_cap(self, hero: Hero) -> int:
        """How many general types fit: types (50) + the "bag" perk (🪓 Leñador, 🎒 Talabartería, 🛒 Mobiliario), whole types.

        [ES] D-339 (0.62): el beneficio "bag" de D-111 daba +10 de espacio al rango 100; con la mochila por tipos da +10 TIPOS (la
        parte entera de lo que lleva ganado). La llaman: _bag_room, _bag_full y las líneas. Si cambia, afecta: cuántos tipos caben."""
        return self._pack_types() + int(float(self._perks(hero)["bag"]) + 1e-9)

    def _bag_types_used(self, hero: Hero, bag: dict[str, int] | None = None, pockets: dict[str, int] | None = None) -> int:
        """Distinct non-gear items in the backpack, without those in a worn profession backpack's compartment."""
        bag = hero.backpack if bag is None else bag
        pockets = self._pbag_pockets(hero) if pockets is None else pockets
        return sum(1 for iid, n in bag.items() if n > 0 and not self._bag_is_gear(iid) and iid not in pockets)

    def _bag_gear_used(self, hero: Hero, bag: dict[str, int] | None = None) -> int:
        """Loose gear pieces in the backpack (each unit is one piece; what is worn never counts)."""
        bag = hero.backpack if bag is None else bag
        return sum(int(n) for iid, n in bag.items() if n > 0 and self._bag_is_gear(iid))

    def _bag_type_cap(self, hero: Hero, item_id: str, pockets: dict[str, int] | None = None) -> int:
        """Units of one type that fit: per_type (30), or the worn profession backpack's (40 or 50) for its resources."""
        pockets = self._pbag_pockets(hero) if pockets is None else pockets
        return int(pockets.get(item_id, self._pack_per_type()))

    def _bag_room(self, hero: Hero, item_id: str, bag: dict[str, int] | None = None) -> int:
        """How many more units of this item fit (0 = none): gear by the loose-pieces cap; the rest by its type's cap and, for a
        type the backpack does not hold yet, a free general type (its compartment, if its profession's backpack is on).

        [ES]
        Qué hace: dice cuántas unidades más de algo caben en la mochila (D-338): el equipo, por el tope de piezas sueltas (20);
        lo demás, hasta el tope de su tipo (30, o 40/50 con la mochila de su oficio puesta) y, si es un tipo que no llevas, solo
        si queda un tipo libre (o va al compartimento de una mochila de oficio puesta). `bag` deja contar sobre otra mochila (lo
        que quedaría después de gastar los materiales de una receta). Quien ya pasa el tope tiene 0 (regla 1: no pierde nada).
        La llaman: recolectar, el mercader, 📦 Entregas, fabricar, la ⚔️ Armería y el 🗺️ pergamino.
        Si cambia, afecta: todo lo que se frena por la mochila (C-41).
        """
        if item_id not in self.content.items:
            return 0
        bag = hero.backpack if bag is None else bag
        if self._bag_is_gear(item_id):
            return max(0, self._pack_gear_cap() - self._bag_gear_used(hero, bag))
        pockets = self._pbag_pockets(hero)
        have = max(0, int(bag.get(item_id, 0)))
        room = max(0, self._bag_type_cap(hero, item_id, pockets) - have)
        if have <= 0 and item_id not in pockets and self._bag_types_used(hero, bag, pockets) >= self._bag_types_cap(hero):
            return 0
        return room

    def _bag_full(self, hero: Hero) -> bool:
        """True when no general type is free (D-338): nothing NEW fits, only more of what is not full yet.

        [ES] Qué hace: dice si la mochila ya no tiene tipos libres. Ya no frena todo (eso es _bag_room, por cosa): lo usan las
        líneas de la mochila y el aviso 💡 "Mochila llena" del camino guiado. Si cambia, afecta: cuándo sale ese aviso."""
        return self._bag_types_used(hero) >= self._bag_types_cap(hero)

    def _bag_add(self, hero: Hero, item_id: str, count: int) -> int:
        """Put found items in the backpack, even past every cap: what you find is never lost (D-90, D-338.4).

        [ES]
        Qué hace: guarda en la mochila lo que encuentras (hallazgos de explorar, el raro, los premios), aunque pase los topes.
        La llaman: _explore_step, _gather_step y _trade_gather (recolectar cuenta el lugar antes, con _bag_room), story.py.
        Si cambia, afecta: si los hallazgos se pierden con la mochila llena (D-90 dice que nunca).
        """
        count = max(0, count)
        if count:
            hero.backpack[item_id] = hero.backpack.get(item_id, 0) + count
        return count

    # ------------------------------------------------------------------ lines

    def _bag_space_line(self, hero: Hero) -> str:
        """"🎒 Mochila: 12/50 tipos (hasta 30 de cada uno) · 🛡️ Equipo suelto: 3/20" (or the line without free types)."""
        used, cap = self._bag_types_used(hero), self._bag_types_cap(hero)
        return self.texts.t("pack.space_full" if used >= cap else "pack.space", used=used, cap=cap, per=self._pack_per_type(),
                            gear=self._bag_gear_used(hero), gcap=self._pack_gear_cap())

    def _bag_item_line(self, hero: Hero, item_id: str) -> str:
        """"🪵 Madera: 12/30 en la mochila" (🪓 Talar and 🎣 Pescar say how much of their resource still fits)."""
        return self.texts.t("pack.item_line", item=self._item_label(item_id), n=hero.backpack.get(item_id, 0),
                            cap=self._bag_type_cap(hero, item_id))

    def _bag_why(self, hero: Hero, items: list[str]) -> str:
        """Why these items do not fit: "Llenos: 🪵 Madera 30/30. Sin tipos libres (50/50) para: 🌿 Hierba curativa." """
        t = self.texts
        pockets = self._pbag_pockets(hero)
        used, cap = self._bag_types_used(hero, pockets=pockets), self._bag_types_cap(hero)
        full, new, gear = [], [], False
        for item_id in dict.fromkeys(items):
            if item_id not in self.content.items or self._bag_room(hero, item_id) > 0:
                continue
            if self._bag_is_gear(item_id):
                gear = True
            elif hero.backpack.get(item_id, 0) > 0 or item_id in pockets:
                full.append(t.t("pack.item_full", item=self._item_label(item_id), n=hero.backpack.get(item_id, 0),
                                cap=self._bag_type_cap(hero, item_id, pockets)))
            else:
                new.append(self._item_label(item_id))
        parts = []
        if full:
            parts.append(t.t("pack.why_full", items=" · ".join(full)))
        if new:
            parts.append(t.t("pack.why_types", used=used, cap=cap, items=", ".join(new)))
        if gear:
            parts.append(t.t("pack.why_gear", gear=self._bag_gear_used(hero), gcap=self._pack_gear_cap()))
        return " ".join(parts)

    def _pbag_hint(self, hero: Hero, items: list[str]) -> list[str]:
        """The 💡 line about profession backpacks, when one of these items belongs to a profession whose best backpack the hero
        does not have on (empty otherwise)."""
        pockets = self._pbag_pockets(hero)
        defs = self._pbag_defs()
        for pid in dict.fromkeys(d["profession"] for d in defs.values()):
            best = self._pbag_best(pid)
            if any(item_id in self._pbag_resources(pid) and pockets.get(item_id, 0) < best for item_id in items):
                return [self.texts.t("pack.hint")]
        return []

    def _bag_gather_block(self, hero: Hero, items: list[str]) -> str:
        """Gathering cannot start (or go on): nothing of what is here fits. Says which cap blocks and the 💡 hint."""
        return self._join([self.texts.t("pack.gather_block", why=self._bag_why(hero, items))] + self._pbag_hint(hero, items))

    def _bag_no_room(self, hero: Hero, item_id: str) -> str:
        """One thing does not fit (the trader, 📦 Entregas, the ⚔️ Armería, a recipe, a scroll): which cap and what to do."""
        if self._bag_is_gear(item_id):
            return self.texts.t("pack.gear_full", gear=self._bag_gear_used(hero), gcap=self._pack_gear_cap())
        return self._join([self.texts.t("pack.no_room", why=self._bag_why(hero, [item_id]))] + self._pbag_hint(hero, [item_id]))

    def _bag_batch_full_line(self, hero: Hero, items: list[str], ended: bool = False) -> str:
        """End of a gathering batch: "🎒 Ya no caben más: 🪵 Madera 30/30 · 🌿 Hierba curativa (sin tipos libres)." and, when
        the batch went on with the rest (ended=False), that the rest kept coming in."""
        t = self.texts
        parts = []
        for item_id in dict.fromkeys(items):
            if item_id not in self.content.items or self._bag_room(hero, item_id) > 0:
                continue
            if hero.backpack.get(item_id, 0) > 0 or item_id in self._pbag_pockets(hero):
                parts.append(t.t("pack.item_full", item=self._item_label(item_id), n=hero.backpack.get(item_id, 0),
                                 cap=self._bag_type_cap(hero, item_id)))
            else:
                parts.append(t.t("pack.item_no_type", item=self._item_label(item_id)))
        if not parts:
            return ""
        return t.t("pack.batch_full_end" if ended else "pack.batch_full", items=" · ".join(parts))

    def _bag_over_lines(self, hero: Hero) -> list[str]:
        """Over a cap (an old hero, or a backpack just taken off): one line that nothing is lost, only blocked (D-338.4)."""
        pockets = self._pbag_pockets(hero)
        over = (self._bag_types_used(hero, pockets=pockets) > self._bag_types_cap(hero)
                or self._bag_gear_used(hero) > self._pack_gear_cap()
                or any(n > self._bag_type_cap(hero, iid, pockets) for iid, n in hero.backpack.items()
                       if n > 0 and not self._bag_is_gear(iid)))
        return [self.texts.t("pack.over_note")] if over else []

    def _pbag_worn_line(self, hero: Hero) -> list[str]:
        """"🎒 Mochilas de oficio puestas: 🪓 Leñador (40 por tipo) · 🌿 Herbolario (50 por tipo)"; nothing when none is on."""
        defs = self._pbag_defs()
        worn = self._pbag_worn(hero)
        if not worn:
            return []
        items = " · ".join(self.texts.t("pack.worn_item", prof=self._prof_name(defs[iid]["profession"]), per=defs[iid]["per_type"])
                           for iid in worn)
        return [self.texts.t("pack.worn_line", items=items)]

    # ------------------------------------------------------------------ 🎒 Mochilas de oficio (D-338.2, D-338.3)

    def _pbag_label(self, item_id: str) -> str:
        item = self.content.items.get(item_id) or {}
        return f"{item.get('emoji', '🎒')} {self.texts.t(item.get('name_key', 'item.' + item_id))}"

    def _pbag_carried(self, hero: Hero) -> list[str]:
        """The profession backpacks in the backpack (not on), in the order of balance.yaml prof_backpacks.items."""
        return [iid for iid in self._pbag_defs() if hero.backpack.get(iid, 0) > 0]

    def _pbag_ranks(self) -> tuple[int, int]:
        """(the lowest rank a basic backpack asks, the rank of the best one) from the recipes (5 and 40 today)."""
        defs = self._pbag_defs()
        ranks: dict[int, list[int]] = {}
        for rdef in self._recipes().values():
            out = next(iter(rdef.get("output") or {}), None)
            if out in defs:
                ranks.setdefault(int(defs[out].get("per_type", 0)), []).append(int(rdef.get("min_rank", 1)))
        if not ranks:
            return 0, 0
        return min(ranks[min(ranks)]), min(ranks[max(ranks)])

    def _pbags_view(self, hero: Hero, notice: str | None = None) -> View:
        """🎒 Mochilas de oficio: the ones on (/mq1 takes one off) and the ones in the backpack (/mp1 puts one on).

        [ES]
        Qué hace: la pantalla de las mochilas de oficio (D-338.2 y .3, pedido del dueño): para qué sirven, las puestas (hasta 3,
        de oficios distintos) con su oficio, su tope por tipo y cuántos tipos de su oficio llevas, y las que tienes en la mochila;
        cada una con su código (/mq1 quitar, /mp1 poner). Sin ninguna, dice quién las hace, desde qué rango y dónde. Botones:
        ↩️ Volver a 🎒 Mochila. Se abre también ocupado (es un menú) con /mochilas.
        La llaman: el botón 🎒 Mochilas de oficio de 🎒 Mochila, /mochilas (/backpacks) y los códigos. Si cambia, afecta:
        tests/test_mochila_por_tipos.py.
        """
        t = self.texts
        defs = self._pbag_defs()
        worn = self._pbag_worn(hero)
        carried = self._pbag_carried(hero)
        low = min((int(d["per_type"]) for d in defs.values()), default=0)
        high = max((int(d["per_type"]) for d in defs.values()), default=0)
        low_rank, high_rank = self._pbag_ranks()
        body = [t.t("pack.pbags_intro", slots=self._pbag_slots(), low=low, high=high), "",
                t.t("pack.pbags_worn_title", n=len(worn), slots=self._pbag_slots())]
        pockets = self._pbag_pockets(hero)
        for n, iid in enumerate(worn, 1):
            pid = defs[iid]["profession"]
            kinds = sum(1 for res in self._pbag_resources(pid) if hero.backpack.get(res, 0) > 0 and pockets.get(res))
            body.append(t.t("pack.pbags_worn_line", code=f"/mq{n}", item=self._pbag_label(iid), prof=self._prof_name(pid),
                            per=defs[iid]["per_type"], kinds=kinds))
        if not worn:
            body.append(t.t("pack.pbags_none"))
        body += ["", t.t("pack.pbags_carried_title")]
        for n, iid in enumerate(carried, 1):
            body.append(t.t("pack.pbags_carried_line", code=f"/mp{n}", item=self._pbag_label(iid), n=hero.backpack.get(iid, 0),
                            prof=self._prof_name(defs[iid]["profession"]), per=defs[iid]["per_type"]))
        if not carried:
            body.append(t.t("pack.pbags_none"))
        if worn or carried:
            body.append(t.t("pack.pbags_codes"))
        body += ["", t.t("pack.pbags_how", low_rank=low_rank, low=low, high_rank=high_rank, high=high), "",
                 self._bag_space_line(hero)]
        body += self._bag_over_lines(hero)
        self._codes(hero, "pbag_off", worn)
        self._codes(hero, "pbag_on", carried)
        return View(kind="prof_bags", title=t.t("pack.pbags_title"), body=body,
                    actions=[Action(id="bag", label=t.t("menu.back"))], notice=notice)

    def _pbag_action(self, hero: Hero, action_id: str) -> View:
        """Route "pbags" (the screen). [ES] La llama: _idle_action (también ocupado: es un menú)."""
        return self._pbags_view(hero)

    def _pbag_code(self, hero: Hero, letter: str, n: int) -> View:
        """/mp2 puts on the 2nd backpack of the last list's "in the backpack"; /mq2 takes off the 2nd one on (D-338.2)."""
        kind = "pbag_on" if letter == "mp" else "pbag_off"
        if kind not in (self.store.get("gremio_codes", hero.id) or {}):     # never opened the list: its order of now
            self._codes(hero, kind, self._pbag_carried(hero) if letter == "mp" else self._pbag_worn(hero))
        target = self._code_target(hero, kind, n)
        if target is None:
            return self._pbags_view(hero, notice=self.texts.t("pack.bad_code", code=f"/{letter}{n}"))
        return self._pbag_put_on(hero, target) if letter == "mp" else self._pbag_take_off(hero, target)

    def _pbag_put_on(self, hero: Hero, item_id: str, quiet: bool = False) -> View | None:
        """Put a profession backpack on (from the backpack): up to prof_slots, of different professions. One of the same
        profession is swapped (it goes back to the backpack). With quiet=True returns None on success (the crafting notice).

        [ES]
        Qué hace: se pone una mochila de oficio que está en la mochila (sale de ella: deja de contar como tipo). Si ya llevas una
        del mismo oficio, la cambia (la de antes vuelve a la mochila). Si ya llevas 3 de otros oficios, avisa y no cambia nada.
        La llaman: /mp1 y _pbag_auto_wear (la que acabas de fabricar). Si cambia, afecta: Hero.prof_bags y los topes.
        """
        t = self.texts
        defs = self._pbag_defs()
        if item_id not in defs or hero.backpack.get(item_id, 0) <= 0:
            return None if quiet else self._pbags_view(hero, notice=t.t("pack.pbag_gone"))
        pid = defs[item_id]["profession"]
        worn = self._pbag_worn(hero)
        same = next((iid for iid in worn if defs[iid]["profession"] == pid), None)
        if same is None and len(worn) >= self._pbag_slots():
            return None if quiet else self._pbags_view(hero, notice=t.t("pack.pbag_slots_full", slots=self._pbag_slots()))
        hero.backpack[item_id] -= 1
        if hero.backpack[item_id] <= 0:
            del hero.backpack[item_id]
        lines = [t.t("pack.pbag_on", item=self._pbag_label(item_id), prof=self._prof_name(pid), per=defs[item_id]["per_type"])]
        if same is not None:
            hero.prof_bags = [iid for iid in hero.prof_bags if iid != same]
            hero.backpack[same] = hero.backpack.get(same, 0) + 1
            lines.append(t.t("pack.pbag_swapped", item=self._pbag_label(same)))
        hero.prof_bags = list(hero.prof_bags or []) + [item_id]
        if quiet:
            return None
        return self._pbags_view(hero, notice=self._join(lines))

    def _pbag_take_off(self, hero: Hero, item_id: str) -> View:
        """Take a profession backpack off: it goes back to the backpack; its profession's resources count as types again, even
        past the cap (rule 3: nothing is lost, only blocked)."""
        t = self.texts
        defs = self._pbag_defs()
        if item_id not in (hero.prof_bags or []):
            return self._pbags_view(hero, notice=t.t("pack.pbag_gone"))
        hero.prof_bags = [iid for iid in hero.prof_bags if iid != item_id]
        hero.backpack[item_id] = hero.backpack.get(item_id, 0) + 1
        pid = (defs.get(item_id) or {}).get("profession", "")
        lines = [t.t("pack.pbag_off", item=self._pbag_label(item_id), prof=self._prof_name(pid) if pid else "",
                     used=self._bag_types_used(hero), cap=self._bag_types_cap(hero))]
        return self._pbags_view(hero, notice=self._join(lines + self._bag_over_lines(hero)))

    def _pbag_auto_wear(self, hero: Hero, item_id: str) -> list[str]:
        """A profession backpack just made goes on by itself when it is the first of its profession and a place is free, or
        when it beats the one of its profession you have on (like gear into an empty slot). Returns the notice line."""
        defs = self._pbag_defs()
        if item_id not in defs:
            return []
        pid, per = defs[item_id]["profession"], int(defs[item_id]["per_type"])
        worn = self._pbag_worn(hero)
        same = next((iid for iid in worn if defs[iid]["profession"] == pid), None)
        if same is not None and int(defs[same]["per_type"]) >= per:
            return []
        if same is None and len(worn) >= self._pbag_slots():
            return []
        self._pbag_put_on(hero, item_id, quiet=True)
        return [self.texts.t("pack.pbag_auto", prof=self._prof_name(pid), per=per)]

    # ------------------------------------------------------------------ crafting: what comes out has to fit

    def _make_fits(self, hero: Hero, rdef: dict[str, Any], times: int, draw: dict[str, int] | None = None) -> bool:
        """True if `times` makes of a recipe fit, counting the backpack after its materials leave (a type that empties frees
        its place). The extra units of refining and the finds enter anyway (rule 1)."""
        draw = draw or {}
        after = dict(hero.backpack)
        for item_id, n in (rdef.get("inputs") or {}).items():
            own = int(n) * times - int(draw.get(item_id, 0))
            if own > 0:
                after[item_id] = after.get(item_id, 0) - own
                if after[item_id] <= 0:
                    del after[item_id]
        out_id, out_n = next(iter(rdef["output"].items()))
        need = int(out_n) * times
        if self._pbag_takes_free_slot(hero, out_id):    # a 🎒 backpack that goes straight on needs no room (one of them)
            need -= 1
        return need <= 0 or self._bag_room(hero, out_id, after) >= need

    def _pbag_takes_free_slot(self, hero: Hero, item_id: str) -> bool:
        """True if a profession backpack just made would go on by itself into a FREE place (none of its profession on, a
        place left): _pbag_auto_wear does that, so it never needs room in the backpack (making one when the bag is full)."""
        defs = self._pbag_defs()
        if item_id not in defs:
            return False
        worn = self._pbag_worn(hero)
        return (len(worn) < self._pbag_slots()
                and not any(defs[iid]["profession"] == defs[item_id]["profession"] for iid in worn))

    def _make_fit_times(self, hero: Hero, rdef: dict[str, Any], times: int, draw_for: Any = None) -> int:
        """The most makes (up to `times`) whose result fits; draw_for(t) gives the fund's part for t makes, if any."""
        for n in range(max(0, times), 0, -1):
            if self._make_fits(hero, rdef, n, draw_for(n) if draw_for else None):
                return n
        return 0

    # ------------------------------------------------------------------ ❓ Dudas and 📚 Guías numbers

    def _pack_faq_values(self) -> dict[str, Any]:
        """{bag_types}, {bag_per_type}, {bag_gear}, {pbag_slots}, {pbag_low}, {pbag_high}, {pbag_low_rank}, {pbag_high_rank}."""
        defs = self._pbag_defs()
        low_rank, high_rank = self._pbag_ranks()
        return {"bag_types": self._pack_types(), "bag_per_type": self._pack_per_type(), "bag_gear": self._pack_gear_cap(),
                "pbag_slots": self._pbag_slots(),
                "pbag_low": min((int(d["per_type"]) for d in defs.values()), default=0),
                "pbag_high": max((int(d["per_type"]) for d in defs.values()), default=0),
                "pbag_low_rank": low_rank, "pbag_high_rank": high_rank}
