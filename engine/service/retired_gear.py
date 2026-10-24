"""⛓️ → 🦺 No more mail (D-342, confirmed; how: D-343, provisional; 0.62.2): the one-time change and its notice.

The owner's order (24-oct-2026): "we removed mail; we leave only leather, cloth and plate". Mail (gear type "malla") no
longer exists in the game: balance.yaml gear.retired_types ({malla: cuero}) keeps it out of every generator (engine/hero/gear.py,
engine/world/dungeons.py), and this module changes, ONCE, every mail piece that still exists into its leather twin (same slot,
tier and source; a ✒️ masterwork into the twin's masterwork: engine/hero/gear.py retired_twin), wherever it is, keeping what each
piece carries (🔧 durability, ✨ enchantment, ✒️ signature). The 🎓 ⛓️ Malla specialization of the 🦺 Peletería
(peleteria_malla, retired: true in content/professions.yaml) leaves Hero.prof_specs: its place is free to pick another one at no
cost, and its mastery stays in Hero.spec_xp. Each player who had something changed reads it once, on their next screen.

[ES]
Para qué sirve: lo que pidió el dueño el 24-oct-2026 (D-342): "la malla la quitamos, dejamos cuero, tela y placa únicamente", con
    sus dos respuestas: las piezas de malla que ya tienen los jugadores (puestas o guardadas) "cambiarlas por la de cuero igual"
    (la de la misma ranura y el mismo nivel; la ✒️ obra maestra, por la obra maestra de cuero) con un aviso, y la 🎓 ⛓️ Malla
    de la Peletería "quitarla y elegir otra gratis" (su dominio queda guardado). Este archivo hace el cambio una sola vez al
    arrancar el motor (GameService.__init__ → _retire_gear_once), deja el registro de a quién se le cambió qué y muestra el
    aviso una vez (_retired_gear_notice, desde _settle). Cómo se aplicó lo eligió Claude (D-343, provisional).
    Es parte de GameService (una "mezcla", como BackpackMixin), en su propio archivo para no agrandar game.py.
Documento de diseño: diseno/03-personaje/equipamiento.md §11 (sin malla, D-342); diseno/07-economia/profesiones.md (Peletería)
Módulo: capa de servicios (M4 Equipo e inventario; M14 Oficios: la especialización retirada)
Depende de: content/balance.yaml (gear.retired_types; enchanting.enchants y gear.score para elegir el ✨ que queda; specs.mastery_xp),
    content/items.yaml (las piezas de malla siguen ahí, sin retired: true, para que las viejas carguen y se puedan cambiar),
    content/professions.yaml (specs con retired: true), engine/hero/gear.py (retired_twin, retired_types, gear_score),
    engine/professions/rules.py (spec_share), content/locales/es_sin_malla.yaml y en_sin_malla.yaml (el aviso), y las ayudas de
    GameService (_gear_name, _prof_name, _join)
Lo usan: engine/service/game.py (GameService hereda de esta clase: __init__ llama a _retire_gear_once; _settle suma
    _retired_gear_notice a los avisos de la primera pantalla); engine/service/permadeath.py (OATH_HERO_SPACES lleva
    "migration_notice": un aviso sin leer se va con el héroe que cae)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño:
    "migrations"/"malla_to_leather" (lo lee el informe de otro agente: el formato no cambia): {"at": hora del cambio, "version":
        "0.62.2", "accounts": {cuenta: {"hero": nombre del héroe (o ""), "handle": el @ de "prefs" (o ""), "pieces": [[de, a],
        …] una entrada por pieza}}, "other": {"armory": n, "gremio_fund": n, "camp_fund": n}}. "pieces" junta todo lo de ese
        jugador: lo puesto, la mochila y el cinturón, sus órdenes de venta del 🏛️ Mercado, sus 📦 Entregas y la bolsa de su bajada
        de 🌀 mazmorra. "other" cuenta lo de los lugares compartidos (sin un dueño solo): la ⚔️ Armería de cada gremio y los
        💰 fondos del gremio y del campamento (siempre con las tres claves, en 0 si no había nada). Es también la marca de "ya se
        hizo": si existe, el cambio no vuelve a correr.
    "migrations"/"peleteria_malla": {"at", "version", "accounts": {cuenta: {"hero", "handle", "specs": [[oficio, especialización,
        dominio guardado]]}}}: quién perdió una 🎓 especialización retirada (hoy solo la ⛓️ Malla de la Peletería).
    "migrations"/"malla_to_leather_kept": {"at", "items": {id: piezas}}: solo si alguna pieza de malla no tenía gemela (quedó como
        estaba). Con el contenido de hoy, todas tienen.
    "migration_notice" (clave la cuenta): {"malla_to_leather": [[de, a], …], "peleteria_malla": [[oficio, especialización], …]}:
        el aviso que falta mostrar; se borra al mostrarlo.
Reglas que nunca se rompen:
    1. Nadie pierde nada (D-64, D-342): cada pieza cambia por su gemela de cuero con su durabilidad, su ✨ y su ✒️; los topes de la
       mochila (D-338) no se miran (el equipo suelto sigue contando lo mismo). Si dos piezas de la misma gemela traían ✨ distintos
       (todas las copias de un id comparten uno, D-115), queda el mejor; una ✒️ firma que ya tenía la gemela se queda.
    2. Corre una sola vez: si "migrations"/"malla_to_leather" existe, no hace nada. Correrlo de nuevo no cambia nada (ya no hay
       malla).
    3. Lo archivado no se toca: el héroe caído de la 💀 muerte permanente ("fallen_hero") es un recuerdo y queda como cayó; los
       registros de historia (quién dio qué al fondo, "gave" y "fund_log"; los movimientos de la ⚔️ Armería, "log") tampoco.
    4. Una pieza sin gemela queda como está (y se anota en "malla_to_leather_kept").
    5. Ningún texto visible se escribe aquí: todo sale de content/locales (es_sin_malla.yaml y en_sin_malla.yaml).
Si cambias esto, revisa:
    - El formato de "migrations"/"malla_to_leather" lo lee el informe de otro agente: no cambiar sus claves
    - Dónde viven los objetos: si una función nueva guarda equipo en otro lugar del almacén antes de que corra este cambio, sumarlo
      aquí (hoy: "hero", "market_order", "market_index", "market_box", "market_open", "armory", "gremio", "upgrades",
      "repair_order" y "dungeon"; los 📜 pedidos de fabricación no pueden tener malla: sus recetas se retiraron en la 0.44)
    - Mapa de impacto: diseno/01-plataforma/mapa-de-impacto.md (M4 y la cascada C-42)
    - Pruebas: tests/test_sin_malla.py
"""

from __future__ import annotations

import logging
from collections import Counter
from typing import Any

from engine.hero import Hero
from engine.hero.gear import gear_score, retired_twin, retired_types
from engine.professions import rules as profession_rules

log = logging.getLogger(__name__)

# Where the one-time changes are recorded, and their keys (stable: another agent's report reads MAIL_KEY).
# [ES] Dónde se anota el cambio de una sola vez y con qué clave (estables: el informe de otro agente lee MAIL_KEY).
MIGRATION_SPACE = "migrations"
MAIL_KEY = "malla_to_leather"
SPEC_KEY = "peleteria_malla"
KEPT_KEY = "malla_to_leather_kept"
MAIL_VERSION = "0.62.2"
# The notice each changed player reads once (keyed by account). [ES] El aviso de una sola vez de cada jugador.
NOTICE_SPACE = "migration_notice"
# Shared places without a single owner: always in the record's "other", 0 if nothing was there. [ES] Lugares compartidos.
SHARED_PLACES = ("armory", "gremio_fund", "camp_fund")


class RetiredGearMixin:
    """The one-time change of mail into leather and the retired 🎓 Malla (D-342, D-343). Mixed into GameService (see the header).

    [ES]
    Qué es: el cambio de una sola vez de toda pieza de malla por su gemela de cuero, la 🎓 especialización retirada y el aviso.
    Quién la usa: GameService (hereda de esta clase): __init__ y _settle.
    Si cambia, afecta: qué tienen los jugadores después de la 0.62.2 y su aviso (C-42).
    """

    # ------------------------------------------------------------------ the twin of a piece

    def _rgear_twin(self, item_id: Any, kept: Counter | None = None) -> str | None:
        """The leather twin of a mail piece (engine/hero/gear.py retired_twin), cached; None for anything else. A mail piece
        without a twin is counted in `kept` (it stays as it is)."""
        if not isinstance(item_id, str) or not item_id:
            return None
        cache = self.__dict__.setdefault("_rgear_cache", {})
        if item_id not in cache:
            cache[item_id] = retired_twin(self.content.items, item_id, self.content.balance)
        twin = cache[item_id]
        if twin is None and kept is not None:
            item = self.content.items.get(item_id) or {}
            if item.get("kind") == "gear" and item.get("type") in retired_types(self.content.balance):
                kept[item_id] += 1
        return twin

    def _rgear_enchant_score(self, record: dict[str, Any] | None) -> float:
        """How good a ✨ enchantment record is (gear.score of its stat): the better one stays when two meet on one id."""
        edef = ((self.content.balance.get("enchanting") or {}).get("enchants") or {}).get((record or {}).get("id"))
        if not edef:
            return 0.0
        return gear_score({edef["stat"]: float((record or {}).get("value", 0.0))}, self.content.balance)

    def _rgear_wear(self, records: Any, twin: str) -> Any:
        """Durability records (D-333) of a changed piece: the same ones, now naming the twin (None stays None = new)."""
        if isinstance(records, list):
            return [dict(rec, id=twin) if isinstance(rec, dict) else rec for rec in records]
        if isinstance(records, dict):
            return dict(records, id=twin)
        return records

    # ------------------------------------------------------------------ one hero sheet

    def _rgear_hero(self, data: dict[str, Any], kept: Counter) -> list[list[str]]:
        """Change every mail piece of one saved hero (a raw "hero" record) into its twin; returns [[from, to], …] per piece.

        [ES]
        Qué hace: cambia en la ficha guardada de un héroe cada pieza de malla por su gemela de cuero: lo puesto (Hero.gear y su
        durabilidad en Hero.gear_wear), la mochila y el cinturón (cada unidad), la durabilidad de las copias usadas
        (Hero.bag_wear), el ✨ (Hero.gear_enchants: si la gemela ya tenía otro, queda el mejor), la ✒️ firma (Hero.gear_signatures:
        si la gemela ya tenía, se queda la suya), las marcas 🆕 (Hero.gear_new) y el resumen del lote en curso (activity "loot").
        Nunca mira los topes de la mochila (nadie pierde nada). La llama: _retire_gear_once. Si cambia, afecta: la ficha de todos.
        """
        pieces: list[list[str]] = []
        gear = data.get("gear") or {}
        held = set(gear.values()) | {i for space in ("backpack", "belt") for i, n in (data.get(space) or {}).items() if int(n or 0) > 0}
        for slot, item_id in list(gear.items()):
            twin = self._rgear_twin(item_id, kept)
            if twin:
                gear[slot] = twin
                pieces.append([item_id, twin])
        for slot, rec in list((data.get("gear_wear") or {}).items()):
            twin = self._rgear_twin((rec or {}).get("id"))
            if twin:
                data["gear_wear"][slot] = self._rgear_wear(rec, twin)
        for space in ("backpack", "belt"):
            bag = data.get(space) or {}
            for item_id in list(bag):
                twin = self._rgear_twin(item_id, kept)
                if not twin:
                    continue
                count = int(bag.pop(item_id) or 0)
                if count > 0:
                    bag[twin] = int(bag.get(twin, 0)) + count
                    pieces += [[item_id, twin] for _ in range(count)]
        # The records that go with a piece move only if the hero really held it: a record left without its piece (it should not
        # exist: _forget_piece clears it) stays as it is, so it never gives the twin a free ✨. [ES] Solo se mueve lo de una pieza
        # que el héroe tenía de verdad; un registro sin pieza queda como está (nunca regala un ✨ a la gemela).
        wear = data.get("bag_wear") or {}
        for item_id in list(wear):
            twin = self._rgear_twin(item_id) if item_id in held else None
            if twin:
                wear[twin] = list(wear.get(twin) or []) + list(self._rgear_wear(wear.pop(item_id) or [], twin))
        enchants = data.get("gear_enchants") or {}
        for item_id in list(enchants):
            twin = self._rgear_twin(item_id) if item_id in held else None
            if twin:
                mine, theirs = enchants.pop(item_id), enchants.get(twin)
                enchants[twin] = mine if not theirs or self._rgear_enchant_score(mine) > self._rgear_enchant_score(theirs) else theirs
        signatures = data.get("gear_signatures") or {}
        for item_id in list(signatures):
            twin = self._rgear_twin(item_id) if item_id in held else None
            if twin:
                signatures.setdefault(twin, signatures.pop(item_id))
        if data.get("gear_new"):
            fresh: list[str] = []
            for item_id in data["gear_new"]:
                new_id = self._rgear_twin(item_id) or item_id
                if new_id not in fresh:
                    fresh.append(new_id)
            data["gear_new"] = fresh
        loot = (data.get("activity") or {}).get("loot")
        if isinstance(loot, dict):
            for item_id in list(loot):
                twin = self._rgear_twin(item_id)
                if twin:
                    loot[twin] = int(loot.get(twin, 0)) + int(loot.pop(item_id) or 0)
        return pieces

    def _rgear_specs(self, data: dict[str, Any]) -> list[list[Any]]:
        """Take the retired 🎓 specializations (content/professions.yaml specs with retired: true) out of one saved hero's
        Hero.prof_specs; returns [[profession, spec, mastery xp kept], …]. Hero.spec_xp is never touched (D-141, D-342)."""
        retired = {sdef.get("id"): pid for pid, rows in ((self.content.professions or {}).get("specs") or {}).items()
                   for sdef in rows or [] if sdef.get("retired")}
        held = data.get("prof_specs") or {}
        lost: list[list[Any]] = []
        for pid in list(held):
            sids = list(held.get(pid) or [])
            gone = [sid for sid in sids if sid in retired]
            if not gone:
                continue
            lost += [[pid, sid, int((data.get("spec_xp") or {}).get(sid, 0))] for sid in gone]
            rest = [sid for sid in sids if sid not in retired]
            if rest:
                held[pid] = rest
            else:
                del held[pid]
        return lost

    # ------------------------------------------------------------------ the one-time change

    def _retire_gear_once(self) -> None:
        """Change every mail piece into its leather twin everywhere, take the retired 🎓 specializations off and record it, once.

        [ES]
        Qué hace: la primera vez que arranca el motor después de la 0.62.2 (si no existe "migrations"/"malla_to_leather"):
        cambia cada pieza de malla por su gemela de cuero en todas las fichas de héroe (_rgear_hero), en las órdenes de venta
        del 🏛️ Mercado (la pieza apartada, con su durabilidad; también la fila del índice y un borrador abierto), en
        📦 Entregas, en la ⚔️ Armería de cada gremio, en los 💰 fondos del gremio y del campamento, en la pieza que nombra un
        📜 encargo de reparación (así sigue valiendo) y en la bolsa de una bajada de 🌀 mazmorra; saca la 🎓 ⛓️ Malla de quien la
        tenía (_rgear_specs); deja el registro ("migrations") y el aviso de cada jugador ("migration_notice"). No toca lo
        archivado (el héroe caído, "fallen_hero"), ni la historia (lo que cada uno dio al fondo, los movimientos de la Armería).
        Correrlo dos veces no cambia nada.
        La llama: GameService.__init__ (al arrancar, antes de cualquier pantalla). Si cambia, afecta: lo que tiene cada jugador
        después del parche (tests/test_sin_malla.py).
        """
        if self.store.get(MIGRATION_SPACE, MAIL_KEY) is not None:
            return
        now = self.clock.now()
        kept: Counter = Counter()
        owned: dict[str, list[list[str]]] = {}
        specs: dict[str, list[list[Any]]] = {}
        other = {place: 0 for place in SHARED_PLACES}
        names: dict[str, str] = {}
        for account, data in list(self.store.items("hero")):
            names[account] = str(data.get("name") or "")
            pieces = self._rgear_hero(data, kept)
            lost = self._rgear_specs(data)
            if pieces or lost:
                self.store.put("hero", account, data)
            if pieces:
                owned.setdefault(account, []).extend(pieces)
            if lost:
                specs[account] = lost
        for oid, order in list(self.store.items("market_order")):       # 🏛️ the escrowed piece of a sell order
            twin = self._rgear_twin(order.get("good"), kept)
            if not twin:
                continue
            old = order["good"]
            order["good"] = twin
            if order.get("wear"):
                order["wear"] = self._rgear_wear(order["wear"], twin)
            self.store.put("market_order", oid, order)
            if order.get("side") == "sell":
                owned.setdefault(str(order.get("by", "")), []).extend([old, twin] for _ in range(int(order.get("n", 0))))
        for key, index in list(self.store.items("market_index")):
            rows = [list(row) for row in index.get("ids") or []]
            changed = False
            for row in rows:
                twin = self._rgear_twin(row[2] if len(row) > 2 else None)
                if twin:
                    row[2], changed = twin, True
            if changed:
                self.store.put("market_index", key, dict(index, ids=rows))
        for account, box in list(self.store.items("market_box")):      # 📦 Entregas
            changed = False
            for entry in box.get("items") or []:
                twin = self._rgear_twin(entry.get("good"), kept)
                if twin:
                    owned.setdefault(account, []).extend([entry["good"], twin] for _ in range(int(entry.get("n", 1))))
                    entry["good"] = twin
                    if entry.get("wear"):
                        entry["wear"] = self._rgear_wear(entry["wear"], twin)
                    changed = True
            if changed:
                self.store.put("market_box", account, box)
        for account, draft in list(self.store.items("market_open")):   # an open sale draft (screen only)
            twin = self._rgear_twin(draft.get("good"))
            if twin:
                self.store.put("market_open", account, dict(draft, good=twin))
        for key, armory in list(self.store.items("armory")):           # ⚔️ each guild's armory (its "log" is history)
            changed = False
            for entry in armory.get("items") or []:
                twin = self._rgear_twin(entry.get("item"), kept)
                if twin:
                    entry["item"] = twin
                    if entry.get("wear"):
                        entry["wear"] = self._rgear_wear(entry["wear"], twin)
                    other["armory"] += 1
                    changed = True
            if changed:
                self.store.put("armory", key, armory)
        for space, place in (("gremio", "gremio_fund"), ("upgrades", "camp_fund")):     # 💰 funds ("gave", "fund_log": history)
            for key, record in list(self.store.items(space)):
                fund = record.get("fund") or {}
                changed = False
                for item_id in list(fund):
                    twin = self._rgear_twin(item_id, kept)
                    if twin:
                        count = int(fund.pop(item_id) or 0)
                        fund[twin] = int(fund.get(twin, 0)) + count
                        other[place] += max(0, count)
                        changed = True
                if changed:
                    self.store.put(space, key, record)
        for key, order in list(self.store.items("repair_order")):      # 📜 the worn piece it names (already counted above)
            twin = self._rgear_twin(order.get("item"))
            if twin:
                self.store.put("repair_order", key, dict(order, item=twin))
        for account, record in list(self.store.items("dungeon")):      # 🌀 the pot of an open deep run
            pot = ((record.get("deep") or {}).get("pot") or {})
            gear = list(pot.get("gear") or [])
            new = [self._rgear_twin(piece, kept) or piece for piece in gear]
            if new != gear:
                owned.setdefault(account, []).extend([old, twin] for old, twin in zip(gear, new) if old != twin)
                pot["gear"] = new
                self.store.put("dungeon", account, record)
        self._rgear_record(now, owned, specs, other, names, kept)

    def _rgear_record(self, now: float, owned: dict[str, list[list[str]]], specs: dict[str, list[list[Any]]],
                      other: dict[str, int], names: dict[str, str], kept: Counter) -> None:
        """Write the records of _retire_gear_once ("migrations") and each changed player's one-time notice."""
        owned = {account: pieces for account, pieces in owned.items() if account and pieces}

        def who(account: str) -> dict[str, str]:
            return {"hero": names.get(account, ""), "handle": str((self.store.get("prefs", account) or {}).get("handle") or "")}

        for account in set(owned) | set(specs):
            notice: dict[str, Any] = {}
            if owned.get(account):
                notice[MAIL_KEY] = [list(pair) for pair in owned[account]]
            if specs.get(account):
                notice[SPEC_KEY] = [[pid, sid] for pid, sid, _ in specs[account]]
            self.store.put(NOTICE_SPACE, account, notice)
        if specs:
            self.store.put(MIGRATION_SPACE, SPEC_KEY, {"at": now, "version": MAIL_VERSION,
                                                       "accounts": {a: dict(who(a), specs=s) for a, s in specs.items()}})
        if kept:
            self.store.put(MIGRATION_SPACE, KEPT_KEY, {"at": now, "items": dict(kept)})
            log.warning("mail pieces without a leather twin, kept as they were: %s", dict(kept))
        self.store.put(MIGRATION_SPACE, MAIL_KEY, {
            "at": now, "version": MAIL_VERSION,
            "accounts": {a: dict(who(a), pieces=[list(pair) for pair in p]) for a, p in owned.items()},
            "other": dict(other)})

    # ------------------------------------------------------------------ the notice

    def _retired_gear_notice(self, hero: Hero) -> list[str]:
        """The one-time notice of what changed for this player (pieces now of leather, the 🎓 to pick again); [] if none.

        [ES]
        Qué hace: si el cambio de la 0.62.2 tocó algo de este jugador ("migration_notice"), devuelve el aviso en su idioma (lo
        arma la pantalla que lo llama, dentro de _speaking): qué piezas ahora son de cuero (×N si eran varias iguales) y que la
        🎓 ⛓️ Malla se retiró y puede elegir otra gratis, con su dominio guardado. Lo borra al devolverlo: sale una sola vez.
        La llama: _settle (la primera pantalla del jugador: view, act, text o el aviso de tick). Si cambia, afecta: solo el aviso.
        """
        data = self.store.get(NOTICE_SPACE, hero.id)
        if not data:
            return []
        self.store.delete(NOTICE_SPACE, hero.id)
        t = self.texts
        items = self.content.items
        lines: list[str] = []
        pieces = Counter(tuple(pair) for pair in data.get(MAIL_KEY) or [] if len(pair) == 2)
        if pieces:
            lines.append(t.t("nomail.notice"))
            for (old, new), count in pieces.items():
                old_name = self._gear_name(old) if old in items else old
                new_name = self._gear_name(new) if new in items else new
                lines.append(t.t("nomail.line" if count == 1 else "nomail.line_n", old=old_name, new=new_name, n=count))
            lines.append(t.t("nomail.kept"))
        catalog = (self.content.professions or {}).get("specs") or {}
        full = int((self.content.balance.get("specs") or {}).get("mastery_xp", 1))
        for pid, sid in (tuple(pair) for pair in data.get(SPEC_KEY) or [] if len(pair) == 2):
            sdef = next((s for s in catalog.get(pid) or [] if s.get("id") == sid), {})
            spec = f"{sdef.get('emoji', '')} {t.t(f'spec.{sid}.name')}".strip()
            pct = int(100 * profession_rules.spec_share((hero.spec_xp or {}).get(sid, 0), full) + 1e-9)
            lines.append(t.t("nomail.spec", spec=spec, prof=self._prof_name(pid), pct=pct))
        return lines
