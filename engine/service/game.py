"""GameService: commands in, neutral views out. Version 0.1 (playable core).

What version 0.1 covers: hero creation (3 classes), the infinite map with
travel that takes real time (D-58), exploring a zone, solo fights with the
6-button bar (D-46), rewards, levels, belt and backpack, passive regeneration.

Timers are lazy: every command first "settles" the hero (finishes a trip or
an exploration whose time is up). tick() does the same for everyone so the
client can push arrival notices.

[ES]
Para qué sirve: es el juego visto desde afuera. Cada cliente llama a view(), text(),
act() y tick(), y recibe pantallas listas para dibujar.
Documento de diseño: diseno/02-mundo/mapa-infinito-y-viaje.md; diseno/04-combate/ronda-y-acciones.md;
    diseno/03-personaje/creacion-de-personaje.md; diseno/01-plataforma/web-y-multiplataforma.md §3
Módulo: capa de servicios (une M1, M2, M3, M5, M6, M8 y M19)
Depende de: engine.core, engine.hero (y engine.hero.gear: equipo, D-77), engine.world, engine.combat, engine.messaging, content/*
Lo usan: adapters/telegram/bot.py, adapters/cli/play.py, tests/test_service.py
Eventos que publica: HeroCreated, TravelStarted, TravelArrived, ZoneDiscovered, CombatStarted,
    HitReceived, HeroDowned, CombatEnded
Eventos que escucha: ninguno
Datos de los que es dueño: espacios "hero", "combat", "zone", "pending" y "meta" del almacén
Reglas que nunca se rompen:
    1. Toda orden empieza por _settle(): ningún temporizador se pierde ni se duplica.
    2. En combate no se viaja ni se explora; viajando no se explora (una actividad a la vez).
    3. Ningún texto visible se escribe aquí: todo sale de content/locales (Texts).
    4. El servicio no sabe qué cliente lo llama: el id de cuenta lo arma el adaptador.
Si cambias esto, revisa:
    - Adaptadores: adapters/telegram/render.py y bot.py (IDs de acción y tipos de vista)
    - Números: balance.yaml (explore, regen, hero, travel)
    - Pruebas: tests/test_service.py
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import asdict
from typing import Any

from engine.classes import base_response, default_spec, ensure_talents, kit as talent_kit, spend_point, specs_of, unlock_points
from engine.combat import CombatContext, make_combat, resolve_round, validate_choice
from engine.core import (
    Clock,
    CombatEnded,
    CombatStarted,
    Content,
    EventBus,
    HeroCreated,
    HeroDowned,
    HitReceived,
    Rng,
    Store,
    Texts,
    TravelArrived,
    TravelStarted,
    ZoneDiscovered,
    hash_unit,
)
from engine.hero import Hero, hero_stats, xp_for_level
from engine.hero.gear import auto_equip, can_use, equip, gear_bonus, piece_stats, roll_gear, starter_gear, suits, unequip
from engine.messaging import Action, View
from engine.world import DIRECTIONS, Zone, travel_minutes, zone_at
from engine.world.territory import first_zones, next_zone

ROMAN = ["0", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
NAME_RE = re.compile(r"^[^\W\d_][\w ]{1,15}$", re.UNICODE)
CAMP_NAME_RE = re.compile(r"^[^\W_][\w '\-]{2,23}$", re.UNICODE)


class GameService:
    """The engine's facade for every client.

    Args:
        content: loaded content.
        store: storage implementation.
        clock: time source.
        world_seed: fixed seed; if None, one is created once and saved in "meta".
        time_scale: multiplies every real-time duration (1.0 = normal; tests use smaller).
        bus: event bus (a new one if None).

    [ES]
    Qué es: la fachada del motor ("servicios de juego" en el diseño).
    Quién la usa: los adaptadores de cliente y las pruebas.
    Si cambia, afecta: todos los clientes.
    """

    def __init__(self, content: Content, store: Store, clock: Clock, world_seed: int | None = None,
                 time_scale: float = 1.0, bus: EventBus | None = None) -> None:
        self.content = content
        self.store = store
        self.clock = clock
        self.time_scale = max(0.0001, time_scale)
        self.bus = bus or EventBus()
        self.texts = Texts(content.texts)
        meta = store.get("meta", "world") or {}
        epoch = int(content.balance.get("world", {}).get("epoch", 1))
        if meta and meta.get("epoch", 1) != epoch:
            # A new epoch restarts the game: wipe player data and create a new world (D-64).
            for key, _ in list(store.items("hero")):
                if store.get("player", key) is None:
                    store.put("player", key, {"first_seen": clock.now()})
            for namespace in ("hero", "combat", "zone", "pending"):
                for key, _ in list(store.items(namespace)):
                    store.delete(namespace, key)
            meta = {}
        if "seed" not in meta or "epoch" not in meta:
            meta["epoch"] = epoch
            meta["seed"] = world_seed if world_seed is not None else int(hash_unit("world", clock.now()) * 2**31)
            store.put("meta", "world", meta)
        self.world_seed = int(meta["seed"])
        self.ctx = CombatContext(content.classes, content.enemies, content.items, content.balance, self.texts)

    # ------------------------------------------------------------------ public API

    def view(self, account_id: str) -> View:
        """Current screen for an account. [ES] Qué hace: muestra la pantalla actual. La llaman: los clientes (al abrir o actualizar). Si cambia, afecta: todos los clientes."""
        self._seen(account_id)
        hero = self._load(account_id)
        if hero is None:
            return self._creation_view(account_id)
        notices = self._settle(hero)
        self._save(hero)
        return self._main_view(hero, notice=self._join(notices))

    def text(self, account_id: str, text: str) -> View:
        """Handle free text (only used to name the hero). [ES] Qué hace: recibe texto escrito (el nombre del héroe). La llaman: los clientes. Si cambia, afecta: la creación de personaje."""
        self._seen(account_id)
        hero = self._load(account_id)
        if hero is not None and self.store.get("camp_naming", account_id):
            view = self._name_camp(hero, " ".join(text.split()))
            self._save(hero)
            return view
        if hero is not None:
            view = self.view(account_id)
            view.notice = self.texts.t("common.use_buttons")
            return view
        pending = self.store.get("pending", account_id) or {"stage": "name"}
        name = " ".join(text.split())
        if not NAME_RE.match(name):
            view = self._creation_view(account_id)
            view.notice = self.texts.t("create.bad_name")
            return view
        if self._name_taken(name, account_id):
            view = self._creation_view(account_id)
            view.notice = self.texts.t("create.name_taken")
            return view
        pending = {"stage": "class", "name": name}
        self.store.put("pending", account_id, pending)
        return self._creation_view(account_id)

    def act(self, account_id: str, action_id: str) -> View:
        """Handle a button press. [ES] Qué hace: ejecuta la acción de un botón. La llaman: los clientes. Si cambia, afecta: todos los botones."""
        hero = self._load(account_id)
        if hero is None:
            return self._create_action(account_id, action_id)
        notices = self._settle(hero)
        if action_id.startswith("rel:"):
            view = self._answer_visitor(hero, action_id)
            self._save(hero)
            return view
        if action_id.startswith("join:"):
            view = self._answer_join(hero, action_id)
            self._save(hero)
            return view
        combat = self.store.get("combat", hero.id)
        if combat is not None:
            view = self._combat_action(hero, combat, action_id)
        else:
            view = self._idle_action(hero, action_id)
        self._save(hero)
        if notices:
            view.notice = self._join(notices + ([view.notice] if view.notice else []))
        return view

    def invite_code(self, account_id: str) -> str:
        """Short stable invite code for an account. [ES] Qué hace: da el código de invitación del jugador. La llaman: el servicio y los clientes. Si cambia, afecta: los enlaces ya compartidos."""
        return format(int(hash_unit("invite", account_id) * 36**7), "x")[:8]

    def register_referral(self, account_id: str, code: str) -> None:
        """Remember who invited a new account (before it creates a hero).

        [ES]
        Qué hace: anota quién invitó a un jugador nuevo, si todavía no tiene héroe.
        La llaman: los clientes cuando alguien entra con un enlace de invitación.
        Si cambia, afecta: el premio de energía por invitar.
        """
        if self._load(account_id) is not None or not code:
            return
        owner = self.store.get("invite_code", code)
        if owner and owner.get("account") != account_id:
            self.store.put("referral", account_id, {"referrer": owner["account"]})

    def _seen(self, account_id: str) -> None:
        if self.store.get("player", account_id) is None:
            self.store.put("player", account_id, {"first_seen": self.clock.now()})

    def players(self) -> list[str]:
        """Every account that ever played (survives the one-time reset). [ES] Qué hace: lista a todos los jugadores, para avisarles los parches. La llaman: los clientes. Si cambia, afecta: los avisos."""
        accounts = {k for k, _ in self.store.items("player")} | {k for k, _ in self.store.items("hero")}
        return sorted(accounts)

    def pending_announcement(self) -> View | None:
        """The newest patch notes if they were not announced yet; marks them announced.

        [ES]
        Qué hace: devuelve el aviso del parche nuevo una sola vez (y lo marca como avisado).
        La llaman: el bot al arrancar, para mandarlo a todos.
        Si cambia, afecta: los avisos de parches.
        """
        patches = self.content.patches or {}
        if not patches:
            return None
        latest = list(patches.values())[-1]
        meta = self.store.get("meta", "announce") or {}
        if meta.get("version") == latest["version"]:
            return None
        self.store.put("meta", "announce", {"version": latest["version"], "at": self.clock.now()})
        return View(kind="patch", title=latest["title"], body=["• " + line for line in latest["notes"]])

    def menu(self) -> list[Action]:
        """Global navigation shown by every client outside the screen (in Telegram, the bottom keyboard).

        [ES]
        Qué hace: da el menú fijo (Zona, Explorar, Campamento, Héroe); cada cliente lo dibuja abajo o al costado.
        La llaman: los adaptadores (Telegram lo pone en el teclado de abajo).
        Si cambia, afecta: la navegación de todos los clientes.
        """
        t = self.texts
        return [Action(id="home", label=t.t("menu.zone")), Action(id="explore_menu", label=t.t("menu.explore")),
                Action(id="claro", label=t.t("menu.camp")), Action(id="hero", label=t.t("menu.hero"))]

    def tick(self) -> list[tuple[str, View]]:
        """Finish every timer that is due; return (account_id, view) notifications.

        [ES]
        Qué hace: cumple los viajes y exploraciones que ya terminaron y devuelve los avisos.
        La llaman: el adaptador de Telegram cada pocos segundos.
        Si cambia, afecta: los avisos de llegada.
        """
        now = self.clock.now()
        out: list[tuple[str, View]] = []
        for account_id, data in self.store.items("hero"):
            activity = data.get("activity")
            if not activity or activity.get("until", 0) > now:
                continue
            hero = Hero.from_dict(data)
            ensure_talents(self.content.classes, self.content.balance, hero)
            notices = self._settle(hero)
            self._save(hero)
            out.append((account_id, self._main_view(hero, notice=self._join(notices))))
        for account_id, box in list(self.store.items("outbox")):
            self.store.delete("outbox", account_id)
            for item in box.get("items", []):
                actions = [Action(**a) for a in item.pop("actions", [])]
                out.append((account_id, View(actions=actions, **item)))
        return out

    def _push(self, account_id: str, view: View) -> None:
        """Queue a message for another player; tick() delivers it (camp contacts, D-71)."""
        box = self.store.get("outbox", account_id) or {"items": []}
        box["items"].append(asdict(view))
        self.store.put("outbox", account_id, box)

    # ------------------------------------------------------------------ storage helpers

    def _load(self, account_id: str) -> Hero | None:
        data = self.store.get("hero", account_id)
        if not data:
            return None
        hero = Hero.from_dict(data)
        ensure_talents(self.content.classes, self.content.balance, hero)
        energy = self.content.balance["energy"]
        if hero.energy_version < energy["version"]:   # 0.6.1: everyone starts again with full energy (D-78)
            hero.energy = max(hero.energy, energy["max"])
            hero.energy_version = energy["version"]
        if not hero.gear_started:          # 0.6: every hero gets its starter gear once (D-77)
            starter_gear(self.content.items, self.content.classes, self.content.balance, hero)
            hero.gear_started = True
        return hero

    def _hero_icon(self, hero: Hero) -> str:
        """The hero's icon: its main spec's unique icon once it has points, else its class icon (D-70)."""
        if hero.talents.get(hero.class_id):
            return self.content.classes[hero.class_id].get("icon", "")
        group = self.content.classes[hero.class_id].get("group", hero.class_id)
        return self.texts.t(f"class_group.{group}.name").split(" ")[0]

    def _hero_title(self, hero: Hero) -> str:
        """Class and spec name; before the first talent point, only the class (D-68)."""
        if hero.talents.get(hero.class_id):
            return self.texts.t(self.content.classes[hero.class_id]["name_key"])
        group = self.content.classes[hero.class_id].get("group", hero.class_id)
        return self.texts.t(f"class_group.{group}.name") + " · " + self.texts.t("talents.no_spec")

    def _kit(self, hero: Hero) -> dict[str, Any]:
        """The hero's effective class (main spec + bar of 3 + talent bonuses, D-68) plus worn gear (D-77)."""
        kit = talent_kit(self.content.classes, self.content.balance, hero)
        kit["gear_bonus"] = gear_bonus(self.content.items, hero, self.content.classes, self.content.balance)
        kit["armor_cap"] = self.content.balance["gear"]["armor_cap"]
        return kit

    def _money(self, amount: int) -> str:
        """Coins as 🥇 gold · 🪙 silver · 🥉 bronze (D-80, D-85): 100 bronze = 1 silver, 100 silver = 1 gold."""
        cfg = self.content.balance["currency"]
        rate = cfg["rate"]
        gold, rest = divmod(max(0, int(amount)), rate * rate)
        silver, bronze = divmod(rest, rate)
        parts = [f"{cfg['icons'][k]}{v}" for k, v in (("gold", gold), ("silver", silver), ("bronze", bronze)) if v]
        return " ".join(parts) or f"{cfg['icons']['bronze']}0"

    def _save(self, hero: Hero) -> None:
        self.store.put("hero", hero.id, hero.to_dict())

    @staticmethod
    def _name_key(name: str) -> str:
        """Comparison key for names: no case, no accents, no spaces ("José Luis" == "joseluis")."""
        plain = unicodedata.normalize("NFKD", name)
        return "".join(ch for ch in plain if not unicodedata.combining(ch) and not ch.isspace()).casefold()

    def _name_taken(self, name: str, account_id: str | None = None) -> bool:
        """True if a hero, or another player still choosing a class, already uses this name."""
        key = self._name_key(name)
        if any(self._name_key(d.get("name", "")) == key for _, d in self.store.items("hero")):
            return True
        return any(acc != account_id and self._name_key(p.get("name", "")) == key
                   for acc, p in self.store.items("pending") if p.get("stage") == "class")

    @staticmethod
    def _join(lines: list[str]) -> str | None:
        lines = [line for line in lines if line]
        return "\n".join(lines) if lines else None

    def _seconds(self, minutes: float) -> float:
        return minutes * 60 * self.time_scale

    def _fmt_duration(self, seconds: float) -> str:
        seconds = max(0, int(round(seconds)))
        if seconds < 60:
            return self.texts.t("time.seconds", n=seconds)
        minutes = (seconds + 59) // 60
        if minutes < 60:
            return self.texts.t("time.minutes", n=minutes)
        return self.texts.t("time.hours", h=minutes // 60, m=minutes % 60)

    # ------------------------------------------------------------------ world helpers

    def _zone(self, x: int, y: int) -> Zone:
        parts = (len(self.texts.list("world.name_first")) or 1, len(self.texts.list("world.name_second")) or 1)
        return zone_at(self.world_seed, x, y, self.content.balance["travel"].get("level_per_lejania", 0.9), parts)

    def _discovered(self, x: int, y: int) -> dict[str, Any] | None:
        if x == 0 and y == 0:
            return {"discovered_by": None}
        return self.store.get("zone", f"{x}:{y}")

    def _zone_name(self, zone: Zone) -> str:
        if zone.x == 0 and zone.y == 0:
            return self.texts.t("world.claro_name")
        first = self.texts.list("world.name_first")
        second = self.texts.list("world.name_second")
        if not first or not second:
            return f"{zone.x},{zone.y}"
        return f"{first[zone.name_index[0] % len(first)]} {second[zone.name_index[1] % len(second)]}"

    def _biome_label(self, zone: Zone) -> str:
        biome = self.content.biomes[zone.biome]
        return f"{biome['emoji']} {self.texts.t(biome['name_key'])}"

    def _route_seconds(self, hero: Hero, direction: str) -> tuple[Zone, float, bool]:
        dx, dy = DIRECTIONS[direction]
        origin = self._zone(hero.x, hero.y)
        dest = self._zone(hero.x + dx, hero.y + dy)
        known = hero.remembers(dest.x, dest.y)
        minutes = travel_minutes(dest.x, dest.y, self._anchors(hero), self.content.balance)
        return dest, self._seconds(minutes), known

    def _leg_seconds(self, hero: Hero, x: int, y: int, nx: int, ny: int) -> float:
        minutes = travel_minutes(nx, ny, self._anchors(hero), self.content.balance)
        return self._seconds(minutes)

    def _anchors(self, hero: Hero) -> list[tuple[int, int, int]]:
        """Where travel distance is counted from (D-78): the Claro and the hero's own camp."""
        anchors = [(x, y, 0) for x, y in self._claro_zones()]
        camp = self.store.get("camp", hero.camp) if hero.camp else None
        if camp:
            anchors += [(x, y, 0) for x, y in camp.get("zones", [[camp["x"], camp["y"]]])]
        return anchors

    def _claro_zones(self) -> list[list[int]]:
        """The Claro covers one more zone per settlement stage (D-81)."""
        return first_zones(0, 0, self._settlement()["stage"] + 1)

    def _territory(self, x: int, y: int) -> dict[str, Any] | None:
        """Whose land a zone is: {"claro": True} or the camp record, or None (D-81)."""
        if [x, y] in self._claro_zones():
            return {"claro": True}
        ref = self.store.get("territory", f"{x}:{y}")
        return self.store.get("camp", ref["camp"]) if ref else None

    @staticmethod
    def _path(x: int, y: int, tx: int, ty: int) -> list[list[int]]:
        """Zone-by-zone path: first along x, then along y."""
        path = []
        while x != tx:
            x += 1 if tx > x else -1
            path.append([x, y])
        while y != ty:
            y += 1 if ty > y else -1
            path.append([x, y])
        return path

    # ------------------------------------------------------------------ settle (lazy timers)

    def _settle(self, hero: Hero) -> list[str]:
        """Finish due timers and apply passive regeneration. Returns notice lines."""
        now = self.clock.now()
        notices: list[str] = []
        in_combat = self.store.get("combat", hero.id) is not None
        stats = hero_stats(self._kit(hero), hero.level)
        if not in_combat and hero.hp < stats["max_hp"] and hero.last_regen_at:
            regen = self.content.balance["regen"]
            pct = (regen["downed_percent_per_minute"] if hero.downed else regen["hp_percent_per_minute"]) / 100
            per_second = stats["max_hp"] * pct / (60 * self.time_scale)
            gained = int((now - hero.last_regen_at) * per_second)
            if gained > 0:
                hero.hp = min(stats["max_hp"], hero.hp + gained)
                # keep the unused fraction so slow (downed) recovery is never lost between orders
                hero.last_regen_at = now if hero.hp >= stats["max_hp"] else hero.last_regen_at + gained / per_second
        elif not in_combat:
            hero.last_regen_at = now
        if hero.hp >= stats["max_hp"]:
            hero.downed = False
        self._regen_energy(hero, now)
        while hero.activity and hero.activity["until"] <= now and self.store.get("combat", hero.id) is None:
            activity = hero.activity
            hero.activity = None
            rng = Rng(int(hash_unit(self.world_seed, hero.id, activity["until"]) * 2**31))
            if activity["kind"] == "travel":
                notices += self._arrive(hero, activity, rng)
            elif activity["kind"] == "explore":
                zone = self._zone(hero.x, hero.y)
                if f"{zone.x}:{zone.y}" not in hero.explored:
                    hero.explored.append(f"{zone.x}:{zone.y}")
                notices.append(self._explore_outcome(hero, zone, rng))
                if zone.x == 0 and zone.y == 0:
                    notices += self._tutorial(hero, "explore_claro")
            elif activity["kind"] == "gather":
                zone = self._zone(hero.x, hero.y)
                notices.append(self._gather_outcome(hero, zone, rng))
                notices += self._tutorial(hero, "gather")
            elif activity["kind"] == "rest":
                hero.hp = hero_stats(self._kit(hero), hero.level)["max_hp"]
                notices.append(self.texts.t("inn.rested"))
                notices += self._tutorial(hero, "heal")
        return notices

    def _arrive(self, hero: Hero, activity: dict[str, Any], rng: Rng) -> list[str]:
        """Finish one travel leg; chain the next leg of a multi-zone trip if any."""
        notices: list[str] = []
        hero.x, hero.y = activity["to"]
        zone = self._zone(hero.x, hero.y)
        hero.remember(hero.x, hero.y)
        self.bus.publish(TravelArrived(hero.id, hero.x, hero.y))
        notices += self._visit_camp(hero)
        if zone.lejania >= 1:
            notices += self._tutorial(hero, "leave_claro")
        path = [list(p) for p in activity.get("path", [])]
        final = not path
        if final:
            notices.append(self.texts.t("travel.arrived", name=self._zone_name(zone), biome=self._biome_label(zone)))
        if self._discovered(hero.x, hero.y) is None:
            self.store.put("zone", f"{hero.x}:{hero.y}", {"discovered_by": hero.name, "at": activity["until"]})
            hero.zones_discovered += 1
            self.bus.publish(ZoneDiscovered(hero.id, hero.x, hero.y))
            notices.append(self.texts.t("travel.discovered_named", name=self._zone_name(zone)))
        danger = self.content.biomes[zone.biome]["danger"] * self.content.balance["explore"]["arrival_encounter_scale"]
        if self._territory(hero.x, hero.y):
            danger = 0.0                      # camps and the Claro protect their land (D-81)
        if rng.chance(danger):
            if not final:
                notices.append(self.texts.t("travel.interrupted", name=self._zone_name(zone)))
            notices.append(self._start_combat(hero, zone, rng, "encounter.ambush"))
            return notices
        if path and not self._spend_energy(hero, "move"):
            notices.append(self.texts.t("energy.route_stopped", name=self._zone_name(zone)))
            path = []
        if path:
            nx, ny = path.pop(0)
            seconds = self._leg_seconds(hero, hero.x, hero.y, nx, ny)
            hero.activity = {"kind": "travel", "to": [nx, ny], "until": activity["until"] + seconds,
                             "dir": activity.get("dir", "n"), "path": path, "goal": activity.get("goal")}
        return notices

    def _energy_period(self) -> float:
        cfg = self.content.balance["energy"]
        return 86400 / cfg["per_day"] * self.time_scale

    def _regen_energy(self, hero: Hero, now: float) -> None:
        """Lazy energy regeneration: +1 every (day / per_day) seconds, up to the max (D-65)."""
        cfg = self.content.balance["energy"]
        if hero.energy >= cfg["max"] or not hero.energy_at:
            hero.energy_at = now
            return
        gained = int((now - hero.energy_at) // self._energy_period())
        if gained > 0:
            hero.energy = min(cfg["max"], hero.energy + gained)
            hero.energy_at = now if hero.energy >= cfg["max"] else hero.energy_at + gained * self._energy_period()

    def _spend_energy(self, hero: Hero, kind: str) -> bool:
        """Pay the energy of a non-combat action: move, explore or gather (D-78)."""
        cost = self.content.balance["energy"][f"per_{kind}"]
        if hero.energy < cost:
            return False
        if hero.energy >= self.content.balance["energy"]["max"]:
            hero.energy_at = self.clock.now()
        hero.energy -= cost
        return True

    def _no_energy_notice(self, hero: Hero) -> str:
        wait = self._energy_period() - (self.clock.now() - hero.energy_at)
        return self.texts.t("energy.empty", time=self._fmt_duration(max(1, wait)), per_day=self.content.balance["energy"]["per_day"])

    def _explore_outcome(self, hero: Hero, zone: Zone, rng: Rng) -> str:
        bal = self.content.balance["explore"]
        roll = rng.random()
        if roll < bal["encounter"] and self.content.biomes[zone.biome]["danger"] > 0:
            return self._start_combat(hero, zone, rng, "encounter.found")
        if roll < bal["encounter"] + bal["item"]:
            options = ["hierba_curativa", "pieza_metal", "venda", "pocion_vida"]
            item_id = rng.pick_weighted(options, [5, 3, 2, 1])
            hero.backpack[item_id] = hero.backpack.get(item_id, 0) + 1
            item = self.content.items[item_id]
            return self.texts.t("explore.found_item", item=f"{item['emoji']} {self.texts.t(item['name_key'])}")
        gold = int(zone.level * rng.uniform(2, 5)) + 1
        hero.gold += gold
        return self.texts.t("explore.found_gold", gold=self._money(gold))

    # ------------------------------------------------------------------ creation

    def _class_groups(self) -> list[str]:
        """Class ids in content order; each groups several specs (content/classes.yaml "group")."""
        groups: list[str] = []
        for class_id, cdef in self.content.classes.items():
            group = cdef.get("group", class_id)
            if group not in groups and not cdef.get("retired"):
                groups.append(group)
        return groups

    def _creation_view(self, account_id: str) -> View:
        t = self.texts
        pending = self.store.get("pending", account_id)
        if not pending or pending.get("stage") != "class":
            self.store.put("pending", account_id, {"stage": "name"})
            return View(kind="create_name", title=t.t("create.title"), body=[t.t("create.intro"), "", t.t("create.ask_name")], expects_text=True)
        group = pending.get("group")
        if not group:
            groups = self._class_groups()
            per = 3
            pages = max(1, (len(groups) + per - 1) // per)
            page = int(pending.get("page", 0)) % pages
            body = [t.t("create.ask_class", name=pending["name"]), t.t("create.page", n=page + 1, total=pages), ""]
            actions = []
            for gid in groups[page * per:(page + 1) * per]:
                body.append(f"• {t.t(f'class_group.{gid}.name')} — {t.t(f'class_group.{gid}.desc')}")
                actions.append(Action(id=f"grp:{gid}", label=t.t(f"class_group.{gid}.name")))
            body += ["", t.t("create.rename_hint")]
            if pages > 1:
                actions.append(Action(id=f"page:{(page + 1) % pages}", label=t.t("create.next")))
            return View(kind="create_class", title=t.t("create.title"), body=body, actions=actions, expects_text=True)
        else:
            # Confirmation step: show the class and its specs, then choose it or go back (D-74).
            body = [t.t("create.confirm_class", group=t.t(f"class_group.{group}.name"), desc=t.t(f"class_group.{group}.desc")), "",
                    t.t("create.its_specs")]
            for class_id in specs_of(self.content.classes, group):
                cdef = self.content.classes[class_id]
                body.append(f"• {t.t(cdef['name_key'])} — {t.t('role.' + cdef.get('role', 'ataque'))}: {t.t(cdef['role_key'])}")
            body += ["", t.t("create.spec_later")]
            actions = [Action(id=f"cls:{default_spec(self.content.classes, group)}", label=t.t("create.choose_class", group=t.t(f"class_group.{group}.name"))),
                       Action(id="grp:", label=t.t("create.back_to_classes"))]
        return View(kind="create_class", title=t.t("create.title"), body=body, actions=actions)

    def _create_action(self, account_id: str, action_id: str) -> View:
        pending = self.store.get("pending", account_id) or {}
        if action_id == "rename":
            self.store.delete("pending", account_id)
            return self._creation_view(account_id)
        if action_id.startswith("page:") and pending.get("stage") == "class" and action_id[5:].isdigit():
            pending["page"] = int(action_id[5:])
            self.store.put("pending", account_id, pending)
            return self._creation_view(account_id)
        if action_id.startswith("grp:") and pending.get("stage") == "class":
            group = action_id[4:]
            groups = self._class_groups()
            pending["group"] = group if group in groups else None
            if group in groups:
                pending["page"] = groups.index(group) // 3   # "back" returns to this class's page
            self.store.put("pending", account_id, pending)
            return self._creation_view(account_id)
        if not action_id.startswith("cls:") or pending.get("stage") != "class":
            return self._creation_view(account_id)
        class_id = action_id[4:]
        if class_id not in self.content.classes:
            return self._creation_view(account_id)
        if self._name_taken(pending["name"], account_id):
            self.store.delete("pending", account_id)
            view = self._creation_view(account_id)
            view.notice = self.texts.t("create.name_taken")
            return view
        hb = self.content.balance["hero"]
        group = self.content.classes[class_id].get("group", class_id)
        stats = hero_stats(self.content.classes[class_id], 1)
        hero = Hero(id=account_id, name=pending["name"], class_id=class_id, gold=hb["start_gold"], hp=stats["max_hp"],
                    energy=self.content.balance["energy"]["max"], energy_at=self.clock.now(),
                    belt=dict(hb["start_belt"]), backpack=dict(hb["start_backpack"]), last_regen_at=self.clock.now())
        hero.unlocked = [base_response(self.content.classes, group)]
        starter_gear(self.content.items, self.content.classes, self.content.balance, hero)
        hero.gear_started = True
        hero.hp = hero_stats(self._kit(hero), 1)["max_hp"]
        hero.energy_version = self.content.balance["energy"]["version"]
        referral = self.store.get("referral", account_id)
        if referral:
            hero.referred_by = referral["referrer"]
            hero.energy += self.content.balance["invite"]["bonus_invited"]
            self.store.delete("referral", account_id)
        self.store.put("invite_code", self.invite_code(account_id), {"account": account_id})
        self._pay_referral(hero)
        self._save(hero)
        self.store.delete("pending", account_id)
        self.bus.publish(HeroCreated(hero.id, class_id))
        return self._zone_view(hero, notice=self.texts.t("create.welcome", name=hero.name))

    # ------------------------------------------------------------------ idle actions

    def _main_view(self, hero: Hero, notice: str | None = None) -> View:
        combat = self.store.get("combat", hero.id)
        if combat is not None:
            return self._combat_view(hero, combat, notice)
        if hero.activity:
            return self._activity_view(hero, notice)
        return self._zone_view(hero, notice)

    def _idle_action(self, hero: Hero, action_id: str) -> View:
        t = self.texts
        if action_id == "map":
            return self._map_view(hero)
        if action_id == "hero":
            return self._hero_view(hero)
        if action_id == "stats":
            return self._stats_view(hero)
        if action_id == "explore_menu":
            return self._explore_menu(hero)
        if action_id == "talents":
            return self._talents_view(hero)
        if action_id == "respec":
            return self._respec(hero)
        if action_id.startswith("tal:"):
            return self._spec_view(hero, action_id[4:])
        if action_id.startswith("pt:"):
            spec = action_id[3:]
            new = spend_point(self.content.classes, self.content.balance, hero, spec)
            names = ", ".join(t.t(f"ability.{a}.name") for a in new)
            notice = t.t("talents.spent") + (" " + t.t("talents.unlocked", names=names) if new else "")
            return self._spec_view(hero, spec, notice=notice)
        if action_id == "bag":
            return self._bag_view(hero)
        if action_id == "potions":
            return self._potions_view(hero)
        if action_id == "wallet":
            return self._wallet_view(hero)
        if action_id == "gems":
            return self._gem_shop_view(hero)
        if action_id.startswith("gem:"):
            return self._buy_with_gems(hero, action_id[4:])
        if action_id == "sew":
            return self._sew_bag(hero)
        if action_id == "gear":
            return self._worn_view(hero)
        if action_id.startswith("gear:"):
            page = action_id[5:]
            return self._gear_view(hero, int(page) if page.isdigit() else 0)
        if action_id.startswith("item:"):
            return self._item_view(hero, action_id[5:])
        if action_id.startswith("equip:"):
            return self._equip(hero, action_id[6:])
        if action_id.startswith("unequip:"):
            item_id = unequip(hero, action_id[8:])
            self._clamp_hp(hero)
            if not item_id:
                return self._gear_view(hero)
            return self._item_view(hero, item_id, notice=self.texts.t("gear.unequipped", item=self._gear_name(item_id)))
        if action_id == "places":
            return self._places_view(hero)
        in_claro = hero.x == 0 and hero.y == 0 and not hero.activity
        if action_id == "found":
            return self._ask_camp_name(hero, "found")
        if action_id == "rename":
            return self._ask_camp_name(hero, "rename")
        if action_id == "cancel_name":
            self.store.delete("camp_naming", hero.id)
            return self._camp_here_view(hero)
        if action_id == "grow":
            return self._grow_camp(hero)
        if action_id == "askjoin":
            return self._ask_join(hero)
        if action_id == "leave":
            return self._leave_camp(hero)
        if action_id == "claro" and not in_claro:
            return self._camp_here_view(hero)
        if action_id == "claro":
            return View(kind="claro", title=t.t("claro.title"), body=[t.t("claro.intro"), self._status_line(hero)] + self._tutorial_hint(hero),
                        actions=[Action(id="camp", label=t.t("camp.button")), Action(id="shop", label=t.t("shop.button")),
                                 Action(id="inn", label=t.t("inn.button", price=self._money(self._inn_price()))), Action(id="home", label=t.t("menu.back"))])
        if action_id in ("camp", "donate"):
            if not in_claro:
                return self._main_view(hero, notice=t.t("shop.only_in_claro"))
            return self._donate(hero) if action_id == "donate" else self._camp_view(hero)
        if action_id.startswith("sellg:"):
            return self._sell_gear(hero, action_id[6:], in_claro)
        if action_id in ("shop", "inn") or action_id.startswith(("buy:", "sell:")):
            if not in_claro:
                return self._main_view(hero, notice=t.t("shop.only_in_claro"))
            if action_id == "shop":
                return self._shop_view(hero)
            if action_id.startswith("buy:"):
                return self._buy(hero, action_id[4:])
            if action_id.startswith("sell:"):
                return self._sell(hero, action_id[5:])
            return self._rest(hero)
        if action_id.startswith("use:"):
            return self._use_out_of_combat(hero, action_id[4:])
        if action_id in ("home", "refresh"):
            return self._main_view(hero)
        if hero.activity:
            view = self._activity_view(hero)
            view.notice = t.t("activity.busy")
            return view
        if action_id.startswith("go:") and action_id[3:] in DIRECTIONS:
            if not self._spend_energy(hero, "move"):
                return self._zone_view(hero, notice=self._no_energy_notice(hero))
            direction = action_id[3:]
            dest, seconds, _ = self._route_seconds(hero, direction)
            until = self.clock.now() + seconds
            hero.activity = {"kind": "travel", "to": [dest.x, dest.y], "until": until, "dir": direction}
            self.bus.publish(TravelStarted(hero.id, dest.x, dest.y, until))
            return self._activity_view(hero, notice=t.t("travel.started", time=self._fmt_duration(seconds)))
        if action_id.startswith("goto:"):
            try:
                gx, gy = (int(v) for v in action_id[5:].split(":"))
            except ValueError:
                return self._places_view(hero)
            if not hero.remembers(gx, gy) or (gx, gy) == (hero.x, hero.y):
                return self._places_view(hero)
            if not self._spend_energy(hero, "move"):
                return self._zone_view(hero, notice=self._no_energy_notice(hero))
            path = self._path(hero.x, hero.y, gx, gy)
            nx, ny = path.pop(0)
            seconds = self._leg_seconds(hero, hero.x, hero.y, nx, ny)
            dx, dy = gx - hero.x, gy - hero.y
            direction = ("e" if dx > 0 else "w") if abs(dx) >= abs(dy) else ("n" if dy > 0 else "s")
            hero.activity = {"kind": "travel", "to": [nx, ny], "until": self.clock.now() + seconds, "dir": direction,
                             "path": path, "goal": [gx, gy]}
            notices = self._tutorial(hero, "use_places")
            return self._activity_view(hero, notice=self._join([t.t("travel.started_route", name=self._zone_name(self._zone(gx, gy)))] + notices))
        if action_id in ("gather", "explore") and not self._spend_energy(hero, action_id):
            return self._explore_menu(hero, notice=self._no_energy_notice(hero))
        if action_id == "gather":
            seconds = self._seconds(self.content.balance["gather"]["minutes"])
            hero.activity = {"kind": "gather", "until": self.clock.now() + seconds}
            return self._activity_view(hero, notice=t.t("gather.started", time=self._fmt_duration(seconds)))
        if action_id == "explore":
            seconds = self._seconds(self.content.balance["explore"]["minutes"])
            hero.activity = {"kind": "explore", "until": self.clock.now() + seconds}
            return self._activity_view(hero, notice=t.t("explore.started", time=self._fmt_duration(seconds)))
        return self._zone_view(hero)

    def _use_out_of_combat(self, hero: Hero, item_id: str) -> View:
        t = self.texts
        item = self.content.items.get(item_id)
        if not item or not item.get("heal"):
            return self._potions_view(hero)
        source = hero.backpack if hero.backpack.get(item_id, 0) > 0 else hero.belt
        if source.get(item_id, 0) <= 0:
            return self._potions_view(hero, notice=t.t("combat.err.item"))
        stats = hero_stats(self._kit(hero), hero.level)
        healed = min(stats["max_hp"] - hero.hp, round(stats["max_hp"] * item["heal"]))
        source[item_id] -= 1
        if source[item_id] <= 0:
            del source[item_id]
        hero.hp += healed
        return self._potions_view(hero, notice=self._join([t.t("bag.used", item=t.t(item["name_key"]), amount=healed)] + self._tutorial(hero, "heal")))

    # ------------------------------------------------------------------ views

    def _status_line(self, hero: Hero) -> str:
        stats = hero_stats(self._kit(hero), hero.level)
        return self.texts.t("hero.status_line", hp=hero.hp, max_hp=stats["max_hp"], gold=self._money(hero.gold), level=hero.level,
                            energy=hero.energy, max_energy=self.content.balance["energy"]["max"])

    def _zone_view(self, hero: Hero, notice: str | None = None) -> View:
        t = self.texts
        zone = self._zone(hero.x, hero.y)
        record = self._discovered(zone.x, zone.y) or {}
        body = [
            t.t("zone.header", name=self._zone_name(zone), biome=self._biome_label(zone)),
            t.t("zone.distance", x=zone.x, y=zone.y, lejania=zone.lejania, ring=ROMAN[zone.ring], level=zone.level),
        ]
        if record.get("discovered_by"):
            body.append(t.t("zone.discovered_by", name=record["discovered_by"]))
        camp = self.store.get("camp", f"{zone.x}:{zone.y}")
        land = self._territory(zone.x, zone.y)
        if camp:
            body.append(t.t("camps.zone_line", name=camp["name"], n=len(camp["members"])))
        elif land and land.get("claro"):
            if (zone.x, zone.y) != (0, 0):
                body.append(t.t("camps.claro_land"))
        elif land:
            body.append(t.t("camps.land_line", name=land["name"]))
        body += [self._status_line(hero)]
        body += self._tutorial_hint(hero)
        body += ["", t.t("zone.routes")]
        actions: list[Action] = []
        for direction in ("n", "s", "e", "w"):
            dest, seconds, known = self._route_seconds(hero, direction)
            if known:
                where = f"{self._biome_label(dest)} {self._zone_name(dest)}"
            elif self._discovered(dest.x, dest.y) is not None:
                where = t.t("zone.known_by_others")
            else:
                where = t.t("zone.uncharted")
            body.append(t.t("zone.route_line", dir=t.t(f"dir.{direction}"), where=where, time=self._fmt_duration(seconds)))
            actions.append(Action(id=f"go:{direction}", label=t.t("zone.go_button", dir=t.t(f"dir.{direction}"), time=self._fmt_duration(seconds))))
        explore_time = self._fmt_duration(self._seconds(self.content.balance["explore"]["minutes"]))
        body += ["", t.t("menu.hint")]
        return View(kind="zone", title=t.t("zone.title"), body=body, actions=actions, notice=notice)

    def _activity_view(self, hero: Hero, notice: str | None = None) -> View:
        t = self.texts
        activity = hero.activity or {}
        remaining = self._fmt_duration(activity.get("until", 0) - self.clock.now())
        if activity.get("kind") == "travel":
            x, y = activity["to"]
            dest = self._zone(x, y)
            known = hero.remembers(x, y)
            where = self._zone_name(dest) if known else t.t("zone.uncharted")
            body = [t.t("travel.on_the_way", where=where, dir=t.t(f"dir.{activity.get('dir', 'n')}")), t.t("travel.remaining", time=remaining)]
            if activity.get("goal"):
                gx, gy = activity["goal"]
                total = (activity.get("until", 0) - self.clock.now())
                cx, cy = x, y
                for nx, ny in activity.get("path", []):
                    total += self._leg_seconds(hero, cx, cy, nx, ny)
                    cx, cy = nx, ny
                body.append(t.t("travel.goal", name=self._zone_name(self._zone(gx, gy)), legs=len(activity.get("path", [])) + 1, time=self._fmt_duration(total)))
            title = t.t("travel.title")
        elif activity.get("kind") == "gather":
            body = [t.t("gather.in_progress"), t.t("travel.remaining", time=remaining)]
            title = t.t("gather.title")
        elif activity.get("kind") == "rest":
            body = [t.t("inn.in_progress"), t.t("travel.remaining", time=remaining)]
            title = t.t("inn.title")
        else:
            body = [t.t("explore.in_progress"), t.t("travel.remaining", time=remaining)]
            title = t.t("explore.title")
        body += ["", self._status_line(hero), t.t("activity.offline_ok")]
        actions = [Action(id="refresh", label=t.t("menu.refresh"))]
        return View(kind="activity", title=title, body=body, actions=actions, notice=notice)

    # ------------------------------------------------------------------ gathering, camp, tutorial

    def _gather_outcome(self, hero: Hero, zone: Zone, rng: Rng) -> str:
        """Gather the zone's materials (biomes.yaml "gather"); dangerous zones may ambush."""
        bal = self.content.balance["gather"]
        danger = self.content.biomes[zone.biome]["danger"] * bal["encounter_scale"]
        if danger > 0 and rng.chance(danger):
            return self._start_combat(hero, zone, rng, "gather.ambush")
        table = self.content.biomes[zone.biome].get("gather", {})
        if not table:
            return self.texts.t("camp.nothing")
        low, high = bal["amount"]
        amount = int(rng.uniform(low, high + 1)) + zone.level // 3
        found: dict[str, int] = {}
        for _ in range(max(1, amount)):
            item_id = rng.pick_weighted(list(table), list(table.values()))
            found[item_id] = found.get(item_id, 0) + 1
        for item_id, count in found.items():
            hero.backpack[item_id] = hero.backpack.get(item_id, 0) + count
        return self.texts.t("gather.found", items=self._item_list(found))

    def _settlement(self) -> dict[str, Any]:
        data = self.store.get("settlement", "claro")
        return data or {"stage": 0, "progress": {}, "merit": {}}

    def _inn_price(self) -> int:
        inn = self.content.balance["inn"]
        stage = self._settlement()["stage"]
        return max(1, inn["price"] - stage * self.content.balance["settlement"]["inn_discount_per_stage"])

    def _camp_view(self, hero: Hero, notice: str | None = None) -> View:
        t = self.texts
        stages = self.content.balance["settlement"]["stages"]
        data = self._settlement()
        stage = stages[data["stage"]]
        body = [t.t("camp.intro"), t.t("camp.stage", stage=t.t(f"camp.stages.{stage['id']}"), n=data["stage"] + 1, total=len(stages)), ""]
        if stage["needs"]:
            nxt = stages[data["stage"] + 1]["id"]
            body.append(t.t("camp.needs_title", next=t.t(f"camp.stages.{nxt}")))
            for item_id, need in stage["needs"].items():
                have = min(need, data["progress"].get(item_id, 0))
                item = self.content.items[item_id]
                body.append(t.t("camp.need_line", emoji=item["emoji"], item=t.t(item["name_key"]), have=have, need=need, bar=self._bar(have, need, 8)))
        else:
            body.append(t.t("camp.complete"))
        body.append(t.t("camp.bonus", price=self._money(self._inn_price())))
        top = sorted(data["merit"].items(), key=lambda kv: -kv[1])[:5]
        if top:
            body += ["", t.t("camp.top_title")] + [t.t("camp.top_line", n=i + 1, name=name, merit=m) for i, (name, m) in enumerate(top)]
        body += ["", t.t("camp.your_merit", merit=hero.merit)]
        body += self._tutorial_hint(hero)
        actions = [Action(id="donate", label=t.t("camp.donate_button")), Action(id="claro", label=t.t("menu.back"))]
        return View(kind="camp", title=t.t("camp.title"), body=body, actions=actions, notice=notice)

    def _donate(self, hero: Hero) -> View:
        """Give every material the current stage still needs; earn xp and merit; maybe level up the camp."""
        t = self.texts
        cfg = self.content.balance["settlement"]
        data = self._settlement()
        stage = cfg["stages"][data["stage"]]
        given: dict[str, int] = {}
        for item_id, need in stage["needs"].items():
            missing = need - data["progress"].get(item_id, 0)
            count = min(missing, hero.backpack.get(item_id, 0))
            if count > 0:
                given[item_id] = count
                data["progress"][item_id] = data["progress"].get(item_id, 0) + count
                hero.backpack[item_id] -= count
                if hero.backpack[item_id] <= 0:
                    del hero.backpack[item_id]
        if not given:
            return self._camp_view(hero, notice=t.t("camp.nothing"))
        units = sum(given.values())
        xp = units * cfg["xp_per_unit"]
        hero.merit += units
        data["merit"][hero.name] = data["merit"].get(hero.name, 0) + units
        lines = [t.t("camp.donated", items=self._item_list(given), xp=xp, merit=units)]
        lines += self._give_xp(hero, xp)
        if all(data["progress"].get(i, 0) >= n for i, n in stage["needs"].items()):
            data["stage"] += 1
            data["progress"] = {}
            lines.append(t.t("camp.stage_up", stage=t.t(f"camp.stages.{cfg['stages'][data['stage']]['id']}")))
        self.store.put("settlement", "claro", data)
        lines += self._tutorial(hero, "donate")
        return self._camp_view(hero, notice="\n".join(lines))

    def _xp_mult(self, hero: Hero) -> float:
        """Experience accelerator bought with gems (D-43, D-80): ×1.5 while active."""
        boost = self.content.balance["currency"]["gem_shop"]["xp_boost"]
        return boost["xp_mult"] if hero.xp_boost_until > self.clock.now() else 1.0

    def _give_xp(self, hero: Hero, xp: int) -> list[str]:
        hero.xp += int(xp * self._xp_mult(hero))
        lines = []
        hb = self.content.balance["hero"]
        formula = hb["xp_formula"]
        while hero.level < hb["max_level"] and hero.xp >= xp_for_level(formula, hero.level + 1):
            hero.level += 1
            hero.points += 1
            hero.hp = hero_stats(self._kit(hero), hero.level)["max_hp"]
            lines.append(self.texts.t("combat.level_up", level=hero.level))
            lines.append(self.texts.t("talents.new_point"))
        self._pay_referral(hero)
        return lines

    def _pay_referral(self, hero: Hero) -> None:
        """When an invited hero reaches the reward level, the inviter gets bonus energy (once)."""
        cfg = self.content.balance["invite"]
        if not hero.referred_by or hero.referral_paid or hero.level < cfg["reward_level"]:
            return
        hero.referral_paid = True
        data = self.store.get("hero", hero.referred_by)
        if not data:
            return
        inviter = Hero.from_dict(data)
        cap = self.content.balance["energy"]["max"] * cfg["cap_factor"]
        inviter.energy = min(cap, inviter.energy + cfg["bonus_referrer"])
        inviter.invites += 1
        self._save(inviter)

    def _tutorial(self, hero: Hero, step: str) -> list[str]:
        """Advance the tutorial if this is the current step; small reward (D-56: hints, not solutions)."""
        cfg = self.content.balance["tutorial"]
        steps = cfg["steps"]
        if hero.tutorial >= len(steps) or steps[hero.tutorial] != step:
            return []
        hero.tutorial += 1
        hero.gold += cfg["reward_gold"]
        lines = [self.texts.t("tutorial.reward", gold=self._money(cfg["reward_gold"]), xp=cfg["reward_xp"])]
        return lines + self._give_xp(hero, cfg["reward_xp"])

    def _tutorial_hint(self, hero: Hero) -> list[str]:
        steps = self.content.balance["tutorial"]["steps"]
        if hero.tutorial >= len(steps):
            return []
        return ["", self.texts.t("tutorial.hint_title", n=hero.tutorial + 1, total=len(steps)),
                self.texts.t(f"tutorial.steps.{steps[hero.tutorial]}")]

    def _shop_view(self, hero: Hero, notice: str | None = None) -> View:
        """The Claro trader: buy belt items, sell materials (half price)."""
        t = self.texts
        shop = self.content.balance["shop"]
        body = [t.t("shop.intro"), t.t("hero.gold_line", gold=self._money(hero.gold)), ""]
        actions = []
        for item_id in shop["sells"]:
            item = self.content.items[item_id]
            body.append(t.t("shop.buy_line", emoji=item["emoji"], item=t.t(item["name_key"]), price=self._money(item["price"])))
            actions.append(Action(id=f"buy:{item_id}", label=t.t("shop.buy_button", emoji=item["emoji"], price=self._money(item["price"]))))
        sellable = {i: n for i, n in hero.backpack.items() if self.content.items.get(i, {}).get("kind") == "material"}
        if sellable:
            total = sum(max(1, int(self.content.items[i]["price"] * shop["sell_ratio"])) * n for i, n in sellable.items())
            body.append(t.t("shop.sell_line", items=self._item_list(sellable), total=self._money(total)))
            actions = actions[:2]
            actions.append(Action(id="sell:all", label=t.t("shop.sell_all_button", total=self._money(total))))
        actions.append(Action(id="claro", label=t.t("menu.back")))
        return View(kind="shop", title=t.t("shop.title"), body=body, actions=actions, notice=notice)

    def _buy(self, hero: Hero, item_id: str) -> View:
        t = self.texts
        if item_id not in self.content.balance["shop"]["sells"]:
            return self._shop_view(hero)
        item = self.content.items[item_id]
        if hero.gold < item["price"]:
            return self._shop_view(hero, notice=t.t("shop.no_gold"))
        hero.gold -= item["price"]
        hero.backpack[item_id] = hero.backpack.get(item_id, 0) + 1
        self._refill_belt(hero)
        return self._shop_view(hero, notice=t.t("shop.bought", item=t.t(item["name_key"])))

    def _sell(self, hero: Hero, item_id: str) -> View:
        t = self.texts
        if item_id == "all":
            total, sold = 0, {}
            for i, n in list(hero.backpack.items()):
                item = self.content.items.get(i, {})
                if item.get("kind") == "material" and n > 0:
                    total += max(1, int(item["price"] * self.content.balance["shop"]["sell_ratio"])) * n
                    sold[i] = n
                    del hero.backpack[i]
            hero.gold += total
            return self._shop_view(hero, notice=t.t("shop.sold_all", items=self._item_list(sold), total=self._money(total)) if sold else None)
        item = self.content.items.get(item_id, {})
        if item.get("kind") != "material" or hero.backpack.get(item_id, 0) <= 0:
            return self._shop_view(hero)
        price = max(1, int(item["price"] * self.content.balance["shop"]["sell_ratio"]))
        hero.backpack[item_id] -= 1
        if hero.backpack[item_id] <= 0:
            del hero.backpack[item_id]
        hero.gold += price
        return self._shop_view(hero, notice=t.t("shop.sold", item=t.t(item["name_key"]), price=self._money(price)))

    def _rest(self, hero: Hero) -> View:
        """Inn: pay gold, sleep a few minutes, wake with full health."""
        t = self.texts
        inn = self.content.balance["inn"]
        price = self._inn_price()
        if hero.gold < price:
            return self._zone_view(hero, notice=t.t("shop.no_gold"))
        hero.gold -= price
        seconds = self._seconds(inn["minutes"])
        hero.activity = {"kind": "rest", "until": self.clock.now() + seconds}
        return self._activity_view(hero, notice=t.t("inn.started", price=self._money(price), time=self._fmt_duration(seconds)))

    def _explore_menu(self, hero: Hero, notice: str | None = None) -> View:
        t = self.texts
        zone = self._zone(hero.x, hero.y)
        explore_time = self._fmt_duration(self._seconds(self.content.balance["explore"]["minutes"]))
        gather_time = self._fmt_duration(self._seconds(self.content.balance["gather"]["minutes"]))
        body = [t.t("zone.header", name=self._zone_name(zone), biome=self._biome_label(zone)), t.t("explore.menu_intro")]
        body += self._tutorial_hint(hero)
        actions = [Action(id="explore", label=t.t("zone.explore_button", time=explore_time)),
                   Action(id="gather", label=t.t("gather.button", time=gather_time)),
                   Action(id="map", label=t.t("menu.map")), Action(id="places", label=t.t("menu.places"))]
        return View(kind="explore_menu", title=t.t("explore.menu_title"), body=body, actions=actions, notice=notice)

    # ------------------------------------------------------------------ player camps (D-71)

    def _camp_requirements(self, hero: Hero) -> list[tuple[str, bool]]:
        t = self.texts
        cfg = self.content.balance["camps"]
        zone = self._zone(hero.x, hero.y)
        known = sum(1 for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx or dy) and hero.remembers(zone.x + dx, zone.y + dy))
        near = any(self.store.get("camp", f"{zone.x + dx}:{zone.y + dy}")
                   for dx in range(-cfg["min_distance"], cfg["min_distance"] + 1)
                   for dy in range(-cfg["min_distance"], cfg["min_distance"] + 1))
        cost_ok = all(hero.backpack.get(i, 0) >= n for i, n in cfg["found_cost"].items())
        return [
            (t.t("camps.req_far", n=cfg["min_lejania"]), zone.lejania >= cfg["min_lejania"]),
            (t.t("camps.req_explored"), f"{zone.x}:{zone.y}" in hero.explored),
            (t.t("camps.req_known", n=known, need=cfg["known_neighbors"]), known >= cfg["known_neighbors"]),
            (t.t("camps.req_alone", n=cfg["min_distance"]), not near and not self._territory(zone.x, zone.y)),
            (t.t("camps.req_cost", items=self._item_list(cfg["found_cost"])), cost_ok),
            (t.t("camps.req_one"), hero.camp is None),
        ]

    def _camp_here_view(self, hero: Hero, notice: str | None = None) -> View:
        t = self.texts
        zone = self._zone(hero.x, hero.y)
        key = f"{zone.x}:{zone.y}"
        camp = self.store.get("camp", key)
        if camp:
            level = camp.get("level", 1)
            body = [t.t("camps.info", name=camp["name"], founder=camp["founder"], x=zone.x, y=zone.y, n=len(camp["members"])),
                    t.t("camps.size", level=level, zones=len(camp.get("zones", [[zone.x, zone.y]]))),
                    t.t("camps.members_cap", n=len(camp["members"]), cap=self._members_cap(camp))]
            actions = []
            if hero.id in camp["members"]:
                body += [t.t("camps.you_member"), t.t("camps.grow_cost", items=self._item_list(self._grow_cost(level)))]
                actions.append(Action(id="grow", label=t.t("camps.grow_button")))
                if camp.get("founder_id") == hero.id:
                    actions.append(Action(id="rename", label=t.t("camps.rename_button")))
                else:
                    actions.append(Action(id="leave", label=t.t("camps.leave_button")))
            else:
                rel = camp["relations"].get(hero.id)
                body.append(t.t(f"camps.relation.{rel or 'unknown'}"))
                if hero.id in camp.get("requests", []):
                    body.append(t.t("camps.join_waiting"))
                elif hero.camp is None and rel != "hostile":
                    actions.append(Action(id="askjoin", label=t.t("camps.join_button")))
            actions.append(Action(id="home", label=t.t("menu.back")))
            return View(kind="player_camp", title=t.t("camps.title"), body=body, actions=actions, notice=notice)
        reqs = self._camp_requirements(hero)
        body = [t.t("camps.found_intro", x=zone.x, y=zone.y), ""] + [("✅ " if ok else "▫️ ") + text for text, ok in reqs]
        actions = [Action(id="found", label=t.t("camps.found_button"))] if all(ok for _, ok in reqs) else []
        actions.append(Action(id="home", label=t.t("menu.back")))
        return View(kind="found_camp", title=t.t("camps.title"), body=body, actions=actions, notice=notice)

    def _ask_camp_name(self, hero: Hero, mode: str) -> View:
        """Founding or renaming a camp: the next text the player writes is its name (D-84)."""
        t = self.texts
        camp = self.store.get("camp", f"{hero.x}:{hero.y}")
        if mode == "found" and (camp or hero.activity or not all(ok for _, ok in self._camp_requirements(hero))):
            return self._camp_here_view(hero, notice=t.t("camps.cannot"))
        if mode == "rename" and (not camp or camp.get("founder_id") != hero.id):
            return self._camp_here_view(hero)
        self.store.put("camp_naming", hero.id, {"mode": mode, "x": hero.x, "y": hero.y})
        return View(kind="name_camp", title=t.t("camps.title"), body=[t.t("camps.ask_name")], expects_text=True,
                    actions=[Action(id="cancel_name", label=t.t("camps.cancel_name"))])

    def _name_camp(self, hero: Hero, name: str) -> View:
        t = self.texts
        pending = self.store.get("camp_naming", hero.id)
        if (pending["x"], pending["y"]) != (hero.x, hero.y):
            self.store.delete("camp_naming", hero.id)
            return self._camp_here_view(hero)
        if not CAMP_NAME_RE.match(name):
            return View(kind="name_camp", title=t.t("camps.title"), body=[t.t("camps.bad_name"), t.t("camps.ask_name")], expects_text=True,
                        actions=[Action(id="cancel_name", label=t.t("camps.cancel_name"))])
        taken = self.store.get("camp_name", self._name_key(name))
        key = f"{hero.x}:{hero.y}"
        if taken and taken.get("camp") != key:
            return View(kind="name_camp", title=t.t("camps.title"), body=[t.t("camps.name_taken"), t.t("camps.ask_name")], expects_text=True,
                        actions=[Action(id="cancel_name", label=t.t("camps.cancel_name"))])
        self.store.delete("camp_naming", hero.id)
        if pending["mode"] == "rename":
            camp = self.store.get("camp", key)
            if not camp or camp.get("founder_id") != hero.id:
                return self._camp_here_view(hero)
            old = camp["name"]
            self.store.delete("camp_name", self._name_key(old))
            camp["name"] = name
            self.store.put("camp", key, camp)
            self.store.put("camp_name", self._name_key(name), {"camp": key})
            return self._camp_here_view(hero, notice=t.t("camps.renamed", name=name))
        return self._found_camp(hero, name)

    def _found_camp(self, hero: Hero, name: str) -> View:
        t = self.texts
        if hero.activity or not all(ok for _, ok in self._camp_requirements(hero)):
            return self._camp_here_view(hero, notice=t.t("camps.cannot"))
        for item_id, n in self.content.balance["camps"]["found_cost"].items():
            hero.backpack[item_id] -= n
            if hero.backpack[item_id] <= 0:
                del hero.backpack[item_id]
        key = f"{hero.x}:{hero.y}"
        self.store.put("camp_name", self._name_key(name), {"camp": key})
        self.store.put("camp", key, {"name": name, "founder": hero.name, "founder_id": hero.id,
                                      "members": [hero.id], "relations": {}, "asked": [], "x": hero.x, "y": hero.y, "created": self.clock.now(),
                                      "level": 1, "zones": [[hero.x, hero.y]]})
        self.store.put("territory", key, {"camp": key})
        hero.camp = key
        return self._camp_here_view(hero, notice=t.t("camps.founded", name=name, x=hero.x, y=hero.y))

    def _members_cap(self, camp: dict[str, Any]) -> int:
        """More people fit as the camp grows (D-84): base + per level above 1."""
        cfg = self.content.balance["camps"]
        return cfg["members_base"] + (camp.get("level", 1) - 1) * cfg["members_per_level"]

    def _ask_join(self, hero: Hero) -> View:
        """Ask the founder to let you in; the founder decides with two buttons (D-84)."""
        t = self.texts
        key = f"{hero.x}:{hero.y}"
        camp = self.store.get("camp", key)
        if not camp or hero.id in camp["members"] or hero.camp is not None or camp["relations"].get(hero.id) == "hostile":
            return self._camp_here_view(hero)
        if len(camp["members"]) >= self._members_cap(camp):
            return self._camp_here_view(hero, notice=t.t("camps.full"))
        requests = camp.setdefault("requests", [])
        if hero.id not in requests:
            requests.append(hero.id)
            self.store.put("camp", key, camp)
            ask = View(kind="camp_join", title=t.t("camps.join_title"), body=[t.t("camps.join_body", name=hero.name, level=hero.level, camp=camp["name"])],
                       actions=[Action(id=f"join:{key}:{hero.id}:y", label=t.t("camps.join_yes")),
                                Action(id=f"join:{key}:{hero.id}:n", label=t.t("camps.join_no"))])
            self._push(camp["founder_id"], ask)
        return self._camp_here_view(hero, notice=t.t("camps.join_sent"))

    def _answer_join(self, hero: Hero, action_id: str) -> View:
        t = self.texts
        parts = action_id.split(":")
        if len(parts) < 5 or parts[-1] not in ("y", "n"):
            return self._main_view(hero)
        key, visitor, choice = f"{parts[1]}:{parts[2]}", ":".join(parts[3:-1]), parts[-1]
        camp = self.store.get("camp", key)
        if not camp or camp.get("founder_id") != hero.id or visitor not in camp.get("requests", []):
            return self._main_view(hero, notice=t.t("camps.already_answered"))
        camp["requests"].remove(visitor)
        data = self.store.get("hero", visitor)
        accepted = choice == "y" and data is not None and data.get("camp") is None and len(camp["members"]) < self._members_cap(camp)
        if accepted:
            camp["members"].append(visitor)
            data["camp"] = key
            self.store.put("hero", visitor, data)
        self.store.put("camp", key, camp)
        result = "accepted" if accepted else "refused"
        self._push(visitor, View(kind="camp_answer", title=t.t("camps.title"), body=[t.t(f"camps.join_{result}", camp=camp["name"])]))
        return self._main_view(hero, notice=t.t(f"camps.you_{result}"))

    def _leave_camp(self, hero: Hero) -> View:
        t = self.texts
        key = hero.camp
        camp = self.store.get("camp", key) if key else None
        if not camp or camp.get("founder_id") == hero.id:
            return self._camp_here_view(hero)
        if hero.id in camp["members"]:
            camp["members"].remove(hero.id)
            self.store.put("camp", key, camp)
        hero.camp = None
        return self._camp_here_view(hero, notice=t.t("camps.left", camp=camp["name"]))

    def _grow_cost(self, level: int) -> dict[str, int]:
        return {i: n * level for i, n in self.content.balance["camps"]["grow_cost_per_level"].items()}

    def _grow_camp(self, hero: Hero) -> View:
        """Make the camp bigger: pay materials, take the next free zone of the spiral (1, 2, 3, 4... zones)."""
        t = self.texts
        key = f"{hero.x}:{hero.y}"
        camp = self.store.get("camp", key)
        if not camp or hero.id not in camp["members"] or hero.activity:
            return self._camp_here_view(hero)
        level = camp.get("level", 1)
        cost = self._grow_cost(level)
        if any(hero.backpack.get(i, 0) < n for i, n in cost.items()):
            return self._camp_here_view(hero, notice=t.t("camps.grow_missing", items=self._item_list(cost)))
        zones = camp.get("zones", [[camp["x"], camp["y"]]])
        new = next_zone(camp["x"], camp["y"], zones, lambda x, y: self._territory(x, y) is None)
        if new is None:
            return self._camp_here_view(hero, notice=t.t("camps.grow_blocked"))
        for item_id, n in cost.items():
            hero.backpack[item_id] -= n
            if hero.backpack[item_id] <= 0:
                del hero.backpack[item_id]
        camp["zones"] = zones + [new]
        camp["level"] = level + 1
        self.store.put("camp", key, camp)
        self.store.put("territory", f"{new[0]}:{new[1]}", {"camp": key})
        return self._camp_here_view(hero, notice=t.t("camps.grown", zones=len(camp["zones"]), x=new[0], y=new[1]))

    def _visit_camp(self, hero: Hero) -> list[str]:
        """Arriving at someone's camp: tell the visitor and ask its members friendly or hostile (once)."""
        t = self.texts
        key = f"{hero.x}:{hero.y}"
        camp = self.store.get("camp", key)
        if not camp or hero.id in camp["members"]:
            return []
        lines = [t.t("camps.found_it", name=camp["name"], founder=camp["founder"])]
        if hero.id not in camp["relations"] and hero.id not in camp["asked"]:
            camp["asked"].append(hero.id)
            self.store.put("camp", key, camp)
            ask = View(kind="camp_visit", title=t.t("camps.visit_title"),
                       body=[t.t("camps.visit_body", name=hero.name, camp=camp["name"], level=hero.level)],
                       actions=[Action(id=f"rel:{key}:{hero.id}:f", label=t.t("camps.friendly")),
                                Action(id=f"rel:{key}:{hero.id}:h", label=t.t("camps.hostile"))])
            for member in camp["members"]:
                self._push(member, ask)
            lines.append(t.t("camps.members_told"))
        else:
            lines.append(t.t(f"camps.relation.{camp['relations'].get(hero.id, 'unknown')}"))
        return lines

    def _answer_visitor(self, hero: Hero, action_id: str) -> View:
        t = self.texts
        parts = action_id.split(":")
        if len(parts) < 5 or parts[-1] not in ("f", "h"):
            return self._main_view(hero)
        key, visitor, choice = f"{parts[1]}:{parts[2]}", ":".join(parts[3:-1]), parts[-1]
        camp = self.store.get("camp", key)
        if not camp or hero.id not in camp["members"]:
            return self._main_view(hero)
        if visitor in camp["relations"]:
            return self._main_view(hero, notice=t.t("camps.already_answered"))
        relation = "friendly" if choice == "f" else "hostile"
        camp["relations"][visitor] = relation
        self.store.put("camp", key, camp)
        self._push(visitor, View(kind="camp_answer", title=t.t("camps.title"), body=[t.t(f"camps.answer.{relation}", camp=camp["name"], name=hero.name)]))
        return self._main_view(hero, notice=t.t("camps.you_answered", relation=t.t(f"camps.relation.{relation}")))

    def _talents_view(self, hero: Hero, notice: str | None = None) -> View:
        t = self.texts
        group = self.content.classes[hero.class_id].get("group", hero.class_id)
        body = [t.t("talents.intro"), t.t("talents.points", n=hero.points), ""]
        if not hero.talents:
            body[:0] = [t.t("talents.choose_first"), ""]
        actions = []
        for spec in specs_of(self.content.classes, group):
            sdef = self.content.classes[spec]
            pts = hero.talents.get(spec, 0)
            mark = " ⭐" if spec == hero.class_id and pts else ""
            body.append(t.t("talents.spec_line", name=t.t(sdef["name_key"]), role=t.t("role." + sdef.get("role", "ataque")), n=pts) + mark)
            actions.append(Action(id=f"tal:{spec}", label=t.t(sdef["name_key"])))
        actions.append(Action(id="hero", label=t.t("menu.back")))
        return View(kind="talents", title=t.t("talents.title"), body=body, actions=actions, notice=notice)

    def _respec_cost(self, hero: Hero) -> int:
        return int(self.content.balance["talents"]["respec_cost_per_level"] * hero.level)

    def _respec(self, hero: Hero) -> View:
        """Change specialization: refund every talent point for gold (D-74). The class never changes."""
        t = self.texts
        cost = self._respec_cost(hero)
        if not hero.talents:
            return self._talents_view(hero)
        if hero.gold < cost:
            return self._talents_view(hero, notice=t.t("shop.no_gold"))
        hero.gold -= cost
        hero.points += sum(hero.talents.values())
        hero.talents = {}
        group = self.content.classes[hero.class_id].get("group", hero.class_id)
        hero.unlocked = [base_response(self.content.classes, group)]
        return self._talents_view(hero, notice=t.t("talents.respec_done", cost=self._money(cost), n=hero.points))

    def _spec_view(self, hero: Hero, spec: str, notice: str | None = None) -> View:
        t = self.texts
        group = self.content.classes[hero.class_id].get("group", hero.class_id)
        if spec not in specs_of(self.content.classes, group):
            return self._talents_view(hero)
        sdef = self.content.classes[spec]
        pts = hero.talents.get(spec, 0)
        body = [t.t("talents.spec_title", name=t.t(sdef["name_key"]), role=t.t("role." + sdef.get("role", "ataque"))),
                t.t(sdef["role_key"]), t.t("talents.spec_points", n=pts, free=hero.points), ""]
        for index, need in enumerate(unlock_points(self.content.balance)):
            if index >= len(sdef["abilities"]):
                break
            ability = sdef["abilities"][index]
            state = "✅" if ability["id"] in hero.unlocked else f"🔒 {need}"
            body.append(f"{state} {self._ability_label(ability, sdef['resource'])}")
        actions = []
        if hero.points > 0:
            actions.append(Action(id=f"pt:{spec}", label=t.t("talents.spend_button")))
        if hero.talents:
            actions.append(Action(id="respec", label=t.t("talents.respec_button", cost=self._money(self._respec_cost(hero)))))
        actions.append(Action(id="talents", label=t.t("menu.back")))
        return View(kind="talent_spec", title=t.t("talents.title"), body=body, actions=actions, notice=notice)

    def _places_view(self, hero: Hero) -> View:
        """Places this hero remembers, nearest first, with an estimated trip time (D-61)."""
        t = self.texts
        places = []
        for key in hero.known:
            x, y = (int(v) for v in key.split(":"))
            if (x, y) == (hero.x, hero.y):
                continue
            seconds, cx, cy = 0.0, hero.x, hero.y
            for nx, ny in self._path(hero.x, hero.y, x, y):
                seconds += self._leg_seconds(hero, cx, cy, nx, ny)
                cx, cy = nx, ny
            places.append((seconds, x, y))
        places.sort()
        body = [t.t("places.intro", n=len(hero.known))]
        actions = []
        for seconds, x, y in places[:3]:
            zone = self._zone(x, y)
            body.append(t.t("places.line", biome=self.content.biomes[zone.biome]["emoji"], name=self._zone_name(zone),
                            zones=abs(x - hero.x) + abs(y - hero.y), time=self._fmt_duration(seconds)))
            actions.append(Action(id=f"goto:{x}:{y}", label=t.t("places.go_button", name=self._zone_name(zone), time=self._fmt_duration(seconds))))
        if not places:
            body.append(t.t("places.none"))
        elif len(places) > 3:
            body.append(t.t("places.more", n=len(places) - 3))
        actions.append(Action(id="explore_menu", label=t.t("menu.back")))
        return View(kind="places", title=t.t("places.title"), body=body, actions=actions)

    def _map_view(self, hero: Hero) -> View:
        t = self.texts
        radius = 3
        rows = []
        for y in range(hero.y + radius, hero.y - radius - 1, -1):
            row = ""
            for x in range(hero.x - radius, hero.x + radius + 1):
                if x == hero.x and y == hero.y:
                    row += "🧍"
                elif hero.remembers(x, y) and self.store.get("camp", f"{x}:{y}"):
                    row += "🏕️"
                elif hero.remembers(x, y):
                    row += self.content.biomes[self._zone(x, y).biome]["emoji"]
                elif self._discovered(x, y) is not None:
                    row += "▪️"
                else:
                    row += "▫️"
            rows.append(row)
        body = [t.t("map.legend")] + rows + ["", t.t("map.position", x=hero.x, y=hero.y, lejania=self._zone(hero.x, hero.y).lejania)]
        return View(kind="map", title=t.t("map.title"), body=body, actions=[Action(id="explore_menu", label=t.t("menu.back"))])

    def _hero_view(self, hero: Hero) -> View:
        """Hero sheet (D-76): level, xp, health, /stats, attack and defense, energy, resource, coins, /inv, /habilidades, status."""
        t = self.texts
        cdef = self._kit(hero)
        stats = hero_stats(cdef, hero.level)
        formula = self.content.balance["hero"]["xp_formula"]
        low, high = xp_for_level(formula, hero.level), xp_for_level(formula, hero.level + 1)
        top = hero.level >= self.content.balance["hero"]["max_level"]
        pct = 100.0 if top else min(100.0, max(0.0, 100 * (hero.xp - low) / max(1, high - low)))
        zone = self._zone(hero.x, hero.y)
        class_line = (t.t("hero.class_line", cls=self._hero_title(hero), role=t.t("role." + cdef.get("role", "ataque")))
                      if hero.talents.get(hero.class_id) else self._hero_title(hero))
        body = [
            t.t("hero.top_line", icon=self._hero_icon(hero), name=self._banner(hero) + hero.name, place=self._zone_name(zone)),
            t.t("hero.class_short", icon=self._hero_icon(hero), cls=class_line),
            t.t("hero.skills_link", n=hero.points),
            t.t("hero.level_pct", level=hero.level, pct=f"{pct:.2f}"),
            t.t("hero.xp_line", xp=hero.xp, next=high),
            t.t("hero.hp_line", hp=hero.hp, max_hp=stats["max_hp"]),
            *self._recovery_lines(hero, stats["max_hp"]),
            t.t("hero.stats_link"),
            t.t("hero.atk_def", attack=round(stats["attack"], 1), armor=round(stats["armor"] * 100)),
            t.t("hero.energy_line", energy=hero.energy, max_energy=self.content.balance["energy"]["max"]),
            t.t("hero.resource_line", resource=t.t(f"resource.{cdef['resource']}"), max=cdef.get("resource_max", 100)),
            self._coins_line(hero),
            t.t("hero.inv_link", n=sum(hero.backpack.values()) + sum(hero.belt.values())),
            "",
            t.t("hero.status_title", status=self._status_text(hero)),
        ]
        cfg = self.content.balance["invite"]
        body += ["", t.t("invite.line", code=self.invite_code(hero.id), n=hero.invites, bonus=cfg["bonus_referrer"], level=cfg["reward_level"])]
        body += self._tutorial_hint(hero)
        actions = [Action(id="bag", label=t.t("bag.button_new" if hero.gear_new else "menu.bag")), Action(id="talents", label=t.t("talents.button", n=hero.points)),
                   Action(id="stats", label=t.t("hero.stats_button")), Action(id="home", label=t.t("menu.back"))]
        return View(kind="hero", title=t.t("hero.title"), body=body, actions=actions, meta={"invite_code": self.invite_code(hero.id)})

    def _coins_line(self, hero: Hero) -> str:
        """🥉 bronze · 🪙 silver · 🥇 gold · 💰 bags · 💎 diamonds, each with its amount, zeros included (D-86)."""
        cfg = self.content.balance["currency"]
        rate = cfg["rate"]
        gold, rest = divmod(max(0, hero.gold), rate * rate)
        silver, bronze = divmod(rest, rate)
        icons = cfg["icons"]
        parts = [(icons["bronze"], bronze), (icons["silver"], silver), (icons["gold"], gold), (icons["bags"], hero.bags), (icons["gems"], hero.gems)]
        return self.texts.t("hero.coins_line", coins="   ".join(f"{i} {n}" for i, n in parts))

    def _recovery_lines(self, hero: Hero, max_hp: int) -> list[str]:
        """How health comes back by itself: normal, or much slower after falling (D-83)."""
        if hero.hp >= max_hp:
            return []
        regen = self.content.balance["regen"]
        pct = regen["downed_percent_per_minute"] if hero.downed else regen["hp_percent_per_minute"]
        seconds = (max_hp - hero.hp) / (max_hp * pct / 100) * 60 * self.time_scale
        key = "hero.downed_line" if hero.downed else "hero.regen_line"
        return [self.texts.t(key, pct=f"{pct:g}", time=self._fmt_duration(seconds))]

    def _status_text(self, hero: Hero) -> str:
        t = self.texts
        if self.store.get("combat", hero.id):
            return t.t("hero.status.combat")
        kind = (hero.activity or {}).get("kind")
        return t.t(f"hero.status.{kind}") if kind else t.t("hero.status.idle")

    def _stats_view(self, hero: Hero) -> View:
        """Every characteristic with a short explanation of what it does (D-76)."""
        t = self.texts
        cdef = self._kit(hero)
        stats = hero_stats(cdef, hero.level)
        bonus = cdef.get("talent_bonus", {})
        body = [
            t.t("stats.hp", value=stats["max_hp"]),
            t.t("stats.attack", value=round(stats["attack"], 1)),
            t.t("stats.defense", value=round(stats["armor"] * 100)),
            t.t("stats.initiative", value=round(stats["initiative"])),
            t.t("stats.stamina", value=self.content.balance["combat"]["stamina_max"]),
            t.t("stats.resource", resource=t.t(f"resource.{cdef['resource']}"), value=cdef.get("resource_max", 100)),
            t.t("stats.energy", value=hero.energy, max=self.content.balance["energy"]["max"], per_day=self.content.balance["energy"]["per_day"]),
            t.t("stats.toxicity", value=self.content.balance["combat"]["toxicity_max"]),
            t.t("stats.talents", attack=round(bonus.get("attack", 0) * 100), hp=round(bonus.get("hp", 0) * 100)),
            t.t("stats.gear", **self._gear_numbers(cdef.get("gear_bonus", {}))),
        ]
        return View(kind="stats", title=t.t("stats.title"), body=body, actions=[Action(id="hero", label=t.t("menu.back"))])

    def _item_list(self, items: dict[str, int]) -> str:
        if not items:
            return self.texts.t("bag.empty")
        parts = []
        for item_id, count in items.items():
            item = self.content.items.get(item_id)
            if item:
                parts.append(f"{item['emoji']} {self.texts.t(item['name_key'])} ×{count}")
        return " · ".join(parts)

    def _bag_view(self, hero: Hero) -> View:
        t = self.texts
        loose = {i: n for i, n in hero.backpack.items() if self.content.items.get(i, {}).get("kind") != "gear"}
        body = [t.t("bag.belt", items=self._item_list(hero.belt)), t.t("bag.backpack", items=self._item_list(loose)), "", self._status_line(hero)]
        body += self._recovery_lines(hero, hero_stats(self._kit(hero), hero.level)["max_hp"])
        actions = [Action(id="gear", label=t.t("gear.button_new" if hero.gear_new else "gear.button")),
                   Action(id="potions", label=t.t("potions.button")), Action(id="wallet", label=t.t("wallet.button")),
                   Action(id="hero", label=t.t("menu.back"))]
        return View(kind="bag", title=t.t("bag.title"), body=body, actions=actions)

    def _potions_view(self, hero: Hero, notice: str | None = None) -> View:
        """Every potion and remedy you carry, with what it does, and a button to use it (D-86)."""
        t = self.texts
        owned = {}
        for item_id in list(hero.belt) + list(hero.backpack):
            item = self.content.items.get(item_id, {})
            if item.get("heal"):
                owned[item_id] = hero.belt.get(item_id, 0) + hero.backpack.get(item_id, 0)
        body = [t.t("potions.intro")]
        actions = []
        for item_id, count in owned.items():
            item = self.content.items[item_id]
            body.append(t.t("potions.line", emoji=item["emoji"], item=t.t(item["name_key"]), n=count,
                            heal=round(item["heal"] * 100), tox=item.get("toxicity", 0)))
            if len(actions) < 3:
                actions.append(Action(id=f"use:{item_id}", label=t.t("bag.use_button", emoji=item["emoji"], item=t.t(item["name_key"]), n=count)))
        if not owned:
            body.append(t.t("potions.none"))
        body += ["", self._status_line(hero)]
        actions.append(Action(id="bag", label=t.t("menu.back")))
        return View(kind="potions", title=t.t("potions.title"), body=body, actions=actions, notice=notice)

    # ------------------------------------------------------------------ currencies (D-80)

    def _banner(self, hero: Hero) -> str:
        return self.texts.t(f"wallet.banner_tag.{hero.banner}") + " " if hero.banner else ""

    def _wallet_view(self, hero: Hero, notice: str | None = None) -> View:
        """The five currencies: bronze, silver, gold (earned), bags (sewn), gems (bought)."""
        t = self.texts
        cfg = self.content.balance["currency"]
        in_claro = hero.x == 0 and hero.y == 0 and not hero.activity
        body = [
            t.t("wallet.coins", coins=self._money(hero.gold)),
            t.t("wallet.coins_help", rate=cfg["rate"]),
            "",
            t.t("wallet.bags", n=hero.bags),
            t.t("wallet.bags_help", items=self._item_list(cfg["bag_recipe"]), coins=self._money(cfg["bag_coins"])),
            "",
            t.t("wallet.gems", n=hero.gems),
            t.t("wallet.gems_help"),
            "",
            t.t("wallet.cards", n=hero.cards),
            t.t("wallet.cards_help"),
        ]
        if hero.xp_boost_until > self.clock.now():
            body += ["", t.t("wallet.boost_on", time=self._fmt_duration(hero.xp_boost_until - self.clock.now()))]
        actions = []
        if in_claro:
            actions.append(Action(id="sew", label=t.t("wallet.sew_button")))
        else:
            body.append(t.t("wallet.sew_in_claro"))
        actions += [Action(id="gems", label=t.t("wallet.gems_button")), Action(id="bag", label=t.t("menu.back"))]
        return View(kind="wallet", title=t.t("wallet.title"), body=body, actions=actions, notice=notice)

    def _sew_bag(self, hero: Hero) -> View:
        """Sew one bag in the Claro: thread, a metal clasp and coins (a sink for coins and materials)."""
        t = self.texts
        cfg = self.content.balance["currency"]
        if not (hero.x == 0 and hero.y == 0 and not hero.activity):
            return self._wallet_view(hero, notice=t.t("shop.only_in_claro"))
        missing = {i: n for i, n in cfg["bag_recipe"].items() if hero.backpack.get(i, 0) < n}
        if missing or hero.gold < cfg["bag_coins"]:
            return self._wallet_view(hero, notice=t.t("wallet.sew_missing", items=self._item_list(cfg["bag_recipe"]), coins=self._money(cfg["bag_coins"])))
        for item_id, n in cfg["bag_recipe"].items():
            hero.backpack[item_id] -= n
            if hero.backpack[item_id] <= 0:
                del hero.backpack[item_id]
        hero.gold -= cfg["bag_coins"]
        hero.bags += 1
        return self._wallet_view(hero, notice=t.t("wallet.sewn", n=hero.bags))

    def _gem_shop_view(self, hero: Hero, notice: str | None = None) -> View:
        t = self.texts
        shop = self.content.balance["currency"]["gem_shop"]
        phase = self.content.balance["currency"]["banner_phase"]
        boost = shop["xp_boost"]
        body = [t.t("wallet.gems", n=hero.gems), t.t("wallet.gem_shop_intro"), "",
                t.t("wallet.xp_boost_line", pct=round((boost["xp_mult"] - 1) * 100), days=boost["days"], gems=boost["gems"]),
                t.t(f"wallet.banner_line.{phase}", gems=shop["banner"]["gems"])]
        if hero.banner:
            body.append(t.t("wallet.banner_owned", tag=self._banner(hero).strip()))
        actions = [Action(id="gem:xp_boost", label=t.t("wallet.xp_boost_button", gems=boost["gems"]))]
        if not hero.banner:
            actions.append(Action(id="gem:banner", label=t.t("wallet.banner_button", gems=shop["banner"]["gems"])))
        actions.append(Action(id="wallet", label=t.t("menu.back")))
        return View(kind="gems", title=t.t("wallet.gem_shop_title"), body=body, actions=actions, notice=notice)

    def _buy_with_gems(self, hero: Hero, what: str) -> View:
        t = self.texts
        cfg = self.content.balance["currency"]
        shop = cfg["gem_shop"]
        if what not in shop or (what == "banner" and hero.banner):
            return self._gem_shop_view(hero)
        price = shop[what]["gems"]
        if hero.gems < price:
            return self._gem_shop_view(hero, notice=t.t("wallet.no_gems"))
        hero.gems -= price
        if what == "xp_boost":
            start = max(self.clock.now(), hero.xp_boost_until)
            hero.xp_boost_until = start + shop["xp_boost"]["days"] * 86400
            return self._gem_shop_view(hero, notice=t.t("wallet.boost_bought"))
        hero.banner = cfg["banner_phase"]
        return self._gem_shop_view(hero, notice=t.t("wallet.banner_bought", tag=self._banner(hero).strip()))

    # ------------------------------------------------------------------ gear (D-77)

    def _gear_name(self, item_id: str) -> str:
        item = self.content.items[item_id]
        icon = self.content.balance["gear"]["rarity_icon"].get(item.get("rarity", "comun"), "")
        return f"{icon}{item['emoji']} {self.texts.t(item['name_key'])}"

    def _gear_stats_text(self, stats: dict[str, float]) -> str:
        t = self.texts
        parts = [t.t(f"gear.stat.{k}", value=f"{'+' if v >= 0 else '−'}{abs(round(v * 100))}") for k, v in stats.items() if round(v * 100)]
        return " · ".join(parts) or t.t("gear.no_stats")

    def _gear_numbers(self, bonus: dict[str, float]) -> dict[str, int]:
        return {k: round(bonus.get(k, 0.0) * 100) for k in ("attack", "hp", "armor")}

    def _worn_list(self, hero: Hero) -> str:
        names = [self._gear_name(hero.gear[slot]) for slot in self.content.balance["gear"]["slots"] if hero.gear.get(slot) in self.content.items]
        return " · ".join(names) or self.texts.t("bag.empty")

    def _gear_status(self, hero: Hero, item: dict[str, Any]) -> str:
        """The game's advice (D-83): it suits your class or not, and whether your level allows it yet."""
        t = self.texts
        fits = suits(item, hero, self.content.classes, self.content.balance)
        if can_use(item, hero, self.content.classes, self.content.balance) == "level":
            return t.t("gear.for_you_later" if fits else "gear.not_for_you_later", level=item["req_level"], type=t.t(f"gear.type.{item['type']}"))
        return t.t("gear.for_you") if fits else t.t("gear.not_for_you", type=t.t(f"gear.type.{item['type']}"))

    def _real_stats(self, hero: Hero, item_id: str) -> dict[str, float]:
        return piece_stats(self.content.items[item_id], hero, self.content.classes, self.content.balance)

    def _gear_diff(self, hero: Hero, item_id: str) -> tuple[dict[str, float], float]:
        """Stats of a piece minus the piece worn in its slot, and a single score (>0 = better)."""
        item = self.content.items[item_id]
        mine = self._real_stats(hero, item_id)
        worn_id = hero.gear.get(item["slot"], "")
        worn = self._real_stats(hero, worn_id) if worn_id in self.content.items else {}
        diff = {k: mine.get(k, 0.0) - worn.get(k, 0.0) for k in sorted(set(mine) | set(worn))}
        return diff, diff.get("attack", 0.0) + diff.get("hp", 0.0) + 2 * diff.get("armor", 0.0)

    def _loot_line(self, hero: Hero, item_id: str) -> str:
        """A gear drop: put on by itself only if that slot was empty (D-83); the details live in 👤 Héroe → 🛡️ Equipo."""
        if item_id not in hero.gear_new:
            hero.gear_new.append(item_id)
        if auto_equip(hero, item_id, self.content.items, self.content.classes, self.content.balance):
            self._clamp_hp(hero)
            return self.texts.t("gear.loot_worn")
        return self.texts.t("gear.loot")

    def _clamp_hp(self, hero: Hero) -> None:
        hero.hp = min(hero.hp, hero_stats(self._kit(hero), hero.level)["max_hp"])

    def _worn_view(self, hero: Hero, notice: str | None = None) -> View:
        """What you wear, one simple line per piece: icon, name and what it gives you (D-86)."""
        t = self.texts
        body = []
        for slot in self.content.balance["gear"]["slots"]:
            item_id = hero.gear.get(slot)
            if item_id in self.content.items:
                item = self.content.items[item_id]
                body.append(t.t("gear.simple_line", emoji=item["emoji"], item=t.t(item["name_key"]) + self._new_mark(hero, item_id),
                                stats=self._gear_stats_text(self._real_stats(hero, item_id))))
        if not body:
            body.append(t.t("gear.nothing_worn"))
        body += ["", t.t("gear.total", stats=self._gear_stats_text(gear_bonus(self.content.items, hero, self.content.classes, self.content.balance)))]
        loose = sum(n for i, n in hero.backpack.items() if self.content.items.get(i, {}).get("kind") == "gear")
        body.append(t.t("gear.in_bag", n=loose))
        actions = [Action(id="gear:0", label=t.t("gear.equip_menu_new" if hero.gear_new else "gear.equip_menu")),
                   Action(id="bag", label=t.t("menu.back"))]
        return View(kind="gear_worn", title=t.t("gear.title"), body=body, actions=actions, notice=notice)

    def _gear_view(self, hero: Hero, page: int = 0, notice: str | None = None) -> View:
        """Worn pieces, gear in the backpack marked for you / later / not for you, one button per piece."""
        t = self.texts
        slots = self.content.balance["gear"]["slots"]
        body = []
        loose = [i for i in hero.backpack if self.content.items.get(i, {}).get("kind") == "gear"]
        loose.sort(key=lambda i: (i not in hero.gear_new, can_use(self.content.items[i], hero, self.content.classes, self.content.balance) is not None,
                                  not suits(self.content.items[i], hero, self.content.classes, self.content.balance), -self.content.items[i].get("tier", 1), i))
        if loose:
            body.append(t.t("gear.backpack_title", n=sum(hero.backpack[i] for i in loose)))
            for item_id in loose[:15]:
                count = hero.backpack[item_id]
                body.append(t.t("gear.backpack_line", item=self._gear_name(item_id) + self._new_mark(hero, item_id), n=f" ×{count}" if count > 1 else "",
                                status=self._gear_status(hero, self.content.items[item_id])))
            body.append(t.t("gear.hint"))
        else:
            body.append(t.t("gear.backpack_empty"))
        worn_names = [self._gear_name(hero.gear[slot]) for slot in slots if hero.gear.get(slot) in self.content.items]
        if worn_names:
            body += ["", t.t("gear.worn_title"), " · ".join(worn_names)]
        worn_new = [(hero.gear[slot], True) for slot in slots if hero.gear.get(slot) in hero.gear_new]
        worn_old = [(hero.gear[slot], True) for slot in slots if hero.gear.get(slot) in self.content.items and hero.gear[slot] not in hero.gear_new]
        pieces = worn_new + [(i, False) for i in loose] + worn_old       # what just dropped comes first
        actions = []
        if len(pieces) <= 3:
            shown = pieces
        else:
            pages = (len(pieces) + 1) // 2
            page %= pages
            shown = pieces[page * 2: page * 2 + 2]
        for item_id, worn in shown:
            label = t.t("gear.piece_worn" if worn else "gear.piece_button", item=self._gear_name(item_id) + self._new_mark(hero, item_id))
            actions.append(Action(id=f"item:{item_id}", label=label))
        if len(pieces) > 3:
            actions.append(Action(id=f"gear:{page + 1}", label=t.t("gear.more")))
        actions.append(Action(id="gear", label=t.t("menu.back")))
        return View(kind="gear", title=t.t("gear.equip_title"), body=body, actions=actions, notice=notice)

    def _new_mark(self, hero: Hero, item_id: str) -> str:
        return " 🆕" if item_id in hero.gear_new else ""

    def _item_view(self, hero: Hero, item_id: str, notice: str | None = None) -> View:
        """One piece: slot, type, level, stats, for you or not, compared with what you wear; equip, take off or sell."""
        t = self.texts
        item = self.content.items.get(item_id)
        worn_slot = next((slot for slot, iid in hero.gear.items() if iid == item_id), None)
        if not item or item.get("kind") != "gear" or (not worn_slot and hero.backpack.get(item_id, 0) <= 0):
            return self._gear_view(hero, notice=notice)
        body = [
            self._gear_name(item_id),
            t.t("gear.detail_line", slot=t.t(f"gear.slot.{item['slot']}"), type=t.t(f"gear.type.{item['type']}"),
                rarity=t.t(f"gear.rarity.{item.get('rarity', 'comun')}"), level=item.get("req_level", 1)),
            t.t("gear.detail_stats", stats=self._gear_stats_text(item.get("stats", {})))
            + ("" if suits(item, hero, self.content.classes, self.content.balance)
               else " " + t.t("gear.detail_real", stats=self._gear_stats_text(self._real_stats(hero, item_id)))),
            self._gear_status(hero, item),
        ]
        if item_id in hero.gear_new:
            hero.gear_new.remove(item_id)
        actions = []
        in_claro = hero.x == 0 and hero.y == 0 and not hero.activity
        price = max(1, int(item.get("price", 1) * self.content.balance["shop"]["sell_ratio"]))
        if worn_slot:
            body.append(t.t("gear.is_worn"))
            actions.append(Action(id=f"unequip:{worn_slot}", label=t.t("gear.unequip_button")))
        else:
            usable = can_use(item, hero, self.content.classes, self.content.balance)
            if hero.gear.get(item["slot"]):
                diff, score = self._gear_diff(hero, item_id)
                key = "gear.compare_better" if score > 0 else "gear.compare_worse" if score < 0 else "gear.compare_same"
                body.append(t.t(key, stats=self._gear_stats_text(diff)))
            if usable is None:
                actions.append(Action(id=f"equip:{item_id}", label=t.t("gear.equip_button")))
            if in_claro:
                actions.append(Action(id=f"sellg:{item_id}", label=t.t("gear.sell_button", price=self._money(price))))
            else:
                body.append(t.t("gear.sell_in_claro", price=self._money(price)))
        actions.append(Action(id="gear:0", label=t.t("menu.back")))
        return View(kind="item", title=t.t("gear.item_title"), body=body, actions=actions, notice=notice)

    def _equip(self, hero: Hero, item_id: str) -> View:
        t = self.texts
        error = equip(hero, item_id, self.content.items, self.content.classes, self.content.balance)
        if error:
            return self._gear_view(hero, notice=t.t(f"gear.err.{error}"))
        self._clamp_hp(hero)
        return self._worn_view(hero, notice=t.t("gear.equipped", item=self._gear_name(item_id)))

    def _sell_gear(self, hero: Hero, item_id: str, in_claro: bool) -> View:
        t = self.texts
        item = self.content.items.get(item_id, {})
        if not in_claro:
            return self._gear_view(hero, notice=t.t("shop.only_in_claro"))
        if item.get("kind") != "gear" or hero.backpack.get(item_id, 0) <= 0:
            return self._gear_view(hero)
        price = max(1, int(item.get("price", 1) * self.content.balance["shop"]["sell_ratio"]))
        hero.backpack[item_id] -= 1
        if hero.backpack[item_id] <= 0:
            del hero.backpack[item_id]
        hero.gold += price
        return self._gear_view(hero, notice=t.t("shop.sold", item=self._gear_name(item_id), price=self._money(price)))

    # ------------------------------------------------------------------ combat

    def _start_combat(self, hero: Hero, zone: Zone, rng: Rng, reason_key: str) -> str:
        candidates = [(eid, e) for eid, e in self.content.enemies.items() if zone.biome in e.get("biomes", [])]
        fitting = [(eid, e) for eid, e in candidates if e["level_min"] <= zone.level <= e["level_max"]]
        pool = fitting or candidates or list(self.content.enemies.items())
        enemy_id, enemy_def = pool[int(rng.random() * len(pool)) % len(pool)]
        level = max(enemy_def["level_min"], min(enemy_def["level_max"], zone.level + (1 if rng.chance(0.3) else 0)))
        seed = int(rng.random() * 2**31)
        state = make_combat(enemy_id, enemy_def, level, self._kit(hero), seed)
        self.store.put("combat", hero.id, state)
        hero.activity = None
        self.bus.publish(CombatStarted(hero.id, enemy_id, seed))
        return self.texts.t(reason_key, enemy=self.texts.t(enemy_def["name_key"]), level=level)

    def _bar(self, value: float, maximum: float, size: int = 10) -> str:
        filled = 0 if maximum <= 0 else max(0, min(size, round(size * value / maximum)))
        return "▓" * filled + "░" * (size - filled)

    def _ability_label(self, ability: dict[str, Any], resource: str) -> str:
        t = self.texts
        icon = {"strike": "✨", "finisher": "🗡️", "heal": "💚", "dot": "🩸", "interrupt": "✋"}.get(ability["kind"], "✨")
        if ability["kind"] == "response":
            icon = {"block": "🛡", "dodge": "💨", "shield": "🫧"}.get(ability.get("response"), "🛡")
        name = t.t("ability." + ability["id"] + ".name")
        label = f"{icon} {name}"
        if ability.get("cost"):
            label += f" ({ability['cost']})"
        elif ability["kind"] == "response":
            label += f" (🔋{ability.get('stamina', 1)})"
        return label

    def _combat_view(self, hero: Hero, state: dict[str, Any], notice: str | None = None) -> View:
        t = self.texts
        cdef = self._kit(hero)
        stats = hero_stats(cdef, hero.level)
        enemy = state["enemy"]
        edef = self.content.enemies[enemy["id"]]
        hs = state["hero"]
        stamina_max = self.content.balance["combat"]["stamina_max"]
        stamina = stamina_max if hs["stamina"] is None else hs["stamina"]
        pct = round(100 * enemy["hp"] / enemy["max_hp"])
        body = []
        if state.get("log"):
            body += [t.t("combat.last_round", n=state["round"] - 1)] + state["log"] + [""]
        body += [
            t.t("combat.enemy_line", enemy=t.t(edef["name_key"]), level=enemy["level"]),
            t.t("combat.enemy_hp", pct=pct, bar=self._bar(enemy["hp"], enemy["max_hp"])),
            "",
            t.t("combat.warning", text=t.t(f"enemy.{enemy['id']}.moves.{enemy['next_move']}.warn")),
            "",
            t.t("combat.hero_line", icon=self._hero_icon(hero), name=hero.name, cls=self._hero_title(hero)),
            t.t("combat.hero_bars", hp=hero.hp, max_hp=stats["max_hp"], resource=t.t(f"resource.{cdef['resource']}"),
                value=hs["resource"], stamina="●" * stamina + "○" * (stamina_max - stamina)),
        ]
        if hs["combo"]:
            body.append(t.t("combat.combo", n=hs["combo"]))
        if hs["toxicity"]:
            body.append(t.t("combat.toxicity", n=hs["toxicity"]))
        body.append(t.t("combat.belt", items=self._item_list(hero.belt)))
        actions = [Action(id="atk", label=t.t("combat.attack_button"))]
        for index, ability in enumerate(cdef["abilities"][:3]):
            reason = validate_choice(state, hero, cdef, {"type": "ability", "index": index}, self.ctx)
            actions.append(Action(id=f"ab:{index}", label=self._ability_label(ability, cdef["resource"]), enabled=reason is None))
        if enemy["can_flee"]:
            actions.append(Action(id="flee", label=t.t("combat.flee_button")))
        else:
            actions.append(Action(id="dodge", label=t.t("combat.dodge_button"), enabled=stamina >= 1))
        actions.append(Action(id="bag", label=t.t("combat.bag_button")))
        title = t.t("combat.title", n=state["round"])
        return View(kind="combat", title=title, body=body, actions=actions, notice=notice)

    def _combat_bag_view(self, hero: Hero, state: dict[str, Any]) -> View:
        t = self.texts
        actions = []
        for item_id, count in list(hero.belt.items())[:3]:
            item = self.content.items.get(item_id)
            if item and item.get("belt"):
                actions.append(Action(id=f"use:{item_id}", label=f"{item['emoji']} {t.t(item['name_key'])} ×{count}"))
        actions.append(Action(id="back", label=t.t("menu.back")))
        body = [t.t("combat.belt_help"), t.t("combat.toxicity", n=state["hero"]["toxicity"])]
        return View(kind="combat_bag", title=t.t("combat.belt_title"), body=body, actions=actions)

    def _combat_action(self, hero: Hero, state: dict[str, Any], action_id: str) -> View:
        t = self.texts
        cdef = self._kit(hero)
        if action_id == "bag":
            return self._combat_bag_view(hero, state)
        choice: dict[str, Any] | None = None
        if action_id == "atk":
            choice = {"type": "attack"}
        elif action_id.startswith("ab:") and action_id[3:].isdigit():
            choice = {"type": "ability", "index": int(action_id[3:])}
        elif action_id == "flee":
            choice = {"type": "flee"}
        elif action_id == "dodge":
            choice = {"type": "dodge"}
        elif action_id.startswith("use:"):
            choice = {"type": "item", "item_id": action_id[4:]}
        if choice is None:
            return self._combat_view(hero, state)
        reason = validate_choice(state, hero, cdef, choice, self.ctx)
        if reason:
            return self._combat_view(hero, state, notice=reason)
        hp_before = hero.hp
        resolve_round(state, hero, cdef, choice, self.ctx)
        if hero.hp < hp_before:
            self.bus.publish(HitReceived(hero.id, hp_before - hero.hp, False))
        if state["outcome"] is None:
            self.store.put("combat", hero.id, state)
            return self._combat_view(hero, state)
        return self._end_combat(hero, state)

    def _end_combat(self, hero: Hero, state: dict[str, Any]) -> View:
        t = self.texts
        outcome = state["outcome"]
        enemy = state["enemy"]
        edef = self.content.enemies[enemy["id"]]
        lines = list(state["log"]) + [""]
        rng = Rng(state["seed"], state["draws"])
        hb = self.content.balance["hero"]
        if outcome == "victory":
            xp = int(edef["xp"] * (1 + 0.15 * (enemy["level"] - 1)) * self._xp_mult(hero))
            low, high = edef.get("gold", [1, 3])
            gold = int(rng.uniform(low, high + 1) * (1 + 0.1 * (enemy["level"] - 1)))
            hero.xp += xp
            hero.gold += gold
            hero.kills += 1
            lines += self._tutorial(hero, "win_fight")
            lines.append(t.t("combat.rewards", xp=xp, gold=self._money(gold)))
            for item_id, chance in edef.get("loot", {}).items():
                if item_id in self.content.items and rng.chance(chance):
                    hero.backpack[item_id] = hero.backpack.get(item_id, 0) + 1
                    item = self.content.items[item_id]
                    lines.append(t.t("combat.loot", item=f"{item['emoji']} {t.t(item['name_key'])}"))
            dropped = roll_gear(self.content.items, self.content.classes, self.content.balance, hero, enemy["level"], rng)
            if dropped:
                hero.backpack[dropped] = hero.backpack.get(dropped, 0) + 1
                lines.append(self._loot_line(hero, dropped))
            while hero.level < hb["max_level"] and hero.xp >= xp_for_level(hb["xp_formula"], hero.level + 1):
                hero.level += 1
                hero.points += 1
                hero.hp = hero_stats(self._kit(hero), hero.level)["max_hp"]
                lines.append(t.t("combat.level_up", level=hero.level))
                lines.append(t.t("talents.new_point"))
            self._pay_referral(hero)
        elif outcome == "defeat":
            lost = int(hero.gold * hb["defeat_gold_loss"])
            hero.gold -= lost
            hero.hp = 1
            hero.downed = True                 # D-83: falling means a long recovery
            self.bus.publish(HeroDowned(hero.id))
            lines.append(t.t("combat.defeat_consequence", gold=self._money(lost)))
        refilled = self._refill_belt(hero)
        if refilled:
            lines.append(t.t("combat.belt_refilled"))
        hero.last_regen_at = self.clock.now()
        self.store.delete("combat", hero.id)
        self.bus.publish(CombatEnded(hero.id, outcome))
        title = t.t(f"combat.end_title.{outcome}")
        return View(kind="combat_end", title=title, body=lines, actions=[Action(id="home", label=t.t("menu.continue"))])

    def _refill_belt(self, hero: Hero) -> bool:
        changed = False
        for item_id, slots in self.content.balance["hero"]["belt_slots"].items():
            while hero.belt.get(item_id, 0) < slots and hero.backpack.get(item_id, 0) > 0:
                hero.belt[item_id] = hero.belt.get(item_id, 0) + 1
                hero.backpack[item_id] -= 1
                if hero.backpack[item_id] <= 0:
                    del hero.backpack[item_id]
                changed = True
        return changed
