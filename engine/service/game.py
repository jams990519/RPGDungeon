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
Depende de: engine.core, engine.hero, engine.world, engine.combat, engine.messaging, content/*
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
from typing import Any

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
from engine.messaging import Action, View
from engine.world import DIRECTIONS, Zone, travel_minutes, zone_at

ROMAN = ["0", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
NAME_RE = re.compile(r"^[^\W\d_][\w ]{1,15}$", re.UNICODE)


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
        if "seed" not in meta:
            meta["seed"] = world_seed if world_seed is not None else int(hash_unit("world", clock.now()) * 2**31)
            store.put("meta", "world", meta)
        self.world_seed = int(meta["seed"])
        self.ctx = CombatContext(content.classes, content.enemies, content.items, content.balance, self.texts)

    # ------------------------------------------------------------------ public API

    def view(self, account_id: str) -> View:
        """Current screen for an account. [ES] Qué hace: muestra la pantalla actual. La llaman: los clientes (al abrir o actualizar). Si cambia, afecta: todos los clientes."""
        hero = self._load(account_id)
        if hero is None:
            return self._creation_view(account_id)
        notices = self._settle(hero)
        self._save(hero)
        return self._main_view(hero, notice=self._join(notices))

    def text(self, account_id: str, text: str) -> View:
        """Handle free text (only used to name the hero). [ES] Qué hace: recibe texto escrito (el nombre del héroe). La llaman: los clientes. Si cambia, afecta: la creación de personaje."""
        hero = self._load(account_id)
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
        if self._name_taken(name):
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
        combat = self.store.get("combat", hero.id)
        if combat is not None:
            view = self._combat_action(hero, combat, action_id)
        else:
            view = self._idle_action(hero, action_id)
        self._save(hero)
        if notices:
            view.notice = self._join(notices + ([view.notice] if view.notice else []))
        return view

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
            notices = self._settle(hero)
            self._save(hero)
            out.append((account_id, self._main_view(hero, notice=self._join(notices))))
        return out

    # ------------------------------------------------------------------ storage helpers

    def _load(self, account_id: str) -> Hero | None:
        data = self.store.get("hero", account_id)
        return Hero.from_dict(data) if data else None

    def _save(self, hero: Hero) -> None:
        self.store.put("hero", hero.id, hero.to_dict())

    def _name_taken(self, name: str) -> bool:
        lowered = name.lower()
        return any(d.get("name", "").lower() == lowered for _, d in self.store.items("hero"))

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
        known = self._discovered(dest.x, dest.y) is not None
        minutes = travel_minutes(origin, dest, self.content.biomes, self.content.balance, known)
        return dest, self._seconds(minutes), known

    # ------------------------------------------------------------------ settle (lazy timers)

    def _settle(self, hero: Hero) -> list[str]:
        """Finish due timers and apply passive regeneration. Returns notice lines."""
        now = self.clock.now()
        notices: list[str] = []
        in_combat = self.store.get("combat", hero.id) is not None
        stats = hero_stats(self.content.classes[hero.class_id], hero.level)
        if not in_combat and hero.hp < stats["max_hp"] and hero.last_regen_at:
            minutes = (now - hero.last_regen_at) / (60 * self.time_scale)
            pct = self.content.balance["regen"]["hp_percent_per_minute"] / 100
            hero.hp = min(stats["max_hp"], hero.hp + int(stats["max_hp"] * pct * minutes))
        if not in_combat:
            hero.last_regen_at = now
        activity = hero.activity
        if not activity or activity["until"] > now or in_combat:
            return notices
        hero.activity = None
        rng = Rng(int(hash_unit(self.world_seed, hero.id, activity["until"]) * 2**31))
        if activity["kind"] == "travel":
            hero.x, hero.y = activity["to"]
            zone = self._zone(hero.x, hero.y)
            self.bus.publish(TravelArrived(hero.id, hero.x, hero.y))
            notices.append(self.texts.t("travel.arrived", name=self._zone_name(zone), biome=self._biome_label(zone)))
            if self._discovered(hero.x, hero.y) is None:
                self.store.put("zone", f"{hero.x}:{hero.y}", {"discovered_by": hero.name, "at": now})
                hero.zones_discovered += 1
                self.bus.publish(ZoneDiscovered(hero.id, hero.x, hero.y))
                notices.append(self.texts.t("travel.discovered"))
            danger = self.content.biomes[zone.biome]["danger"] * self.content.balance["explore"]["arrival_encounter_scale"]
            if rng.chance(danger):
                notices.append(self._start_combat(hero, zone, rng, "encounter.ambush"))
        elif activity["kind"] == "explore":
            zone = self._zone(hero.x, hero.y)
            notices.append(self._explore_outcome(hero, zone, rng))
        return notices

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
        return self.texts.t("explore.found_gold", gold=gold)

    # ------------------------------------------------------------------ creation

    def _creation_view(self, account_id: str) -> View:
        t = self.texts
        pending = self.store.get("pending", account_id)
        if not pending or pending.get("stage") != "class":
            self.store.put("pending", account_id, {"stage": "name"})
            return View(kind="create_name", title=t.t("create.title"), body=[t.t("create.intro"), "", t.t("create.ask_name")], expects_text=True)
        body = [t.t("create.ask_class", name=pending["name"]), ""]
        actions = []
        for class_id, cdef in self.content.classes.items():
            body.append(f"• {t.t(cdef['name_key'])} — {t.t(cdef['role_key'])}")
            actions.append(Action(id=f"cls:{class_id}", label=t.t(cdef["name_key"])))
        actions.append(Action(id="rename", label=t.t("create.rename")))
        return View(kind="create_class", title=t.t("create.title"), body=body, actions=actions)

    def _create_action(self, account_id: str, action_id: str) -> View:
        pending = self.store.get("pending", account_id) or {}
        if action_id == "rename":
            self.store.delete("pending", account_id)
            return self._creation_view(account_id)
        if not action_id.startswith("cls:") or pending.get("stage") != "class":
            return self._creation_view(account_id)
        class_id = action_id[4:]
        if class_id not in self.content.classes:
            return self._creation_view(account_id)
        if self._name_taken(pending["name"]):
            self.store.delete("pending", account_id)
            view = self._creation_view(account_id)
            view.notice = self.texts.t("create.name_taken")
            return view
        hb = self.content.balance["hero"]
        stats = hero_stats(self.content.classes[class_id], 1)
        hero = Hero(id=account_id, name=pending["name"], class_id=class_id, gold=hb["start_gold"], hp=stats["max_hp"],
                    belt=dict(hb["start_belt"]), backpack=dict(hb["start_backpack"]), last_regen_at=self.clock.now())
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
        if action_id == "bag":
            return self._bag_view(hero)
        if action_id.startswith("use:"):
            return self._use_out_of_combat(hero, action_id[4:])
        if action_id in ("home", "refresh"):
            return self._main_view(hero)
        if hero.activity:
            view = self._activity_view(hero)
            view.notice = t.t("activity.busy")
            return view
        if action_id.startswith("go:") and action_id[3:] in DIRECTIONS:
            direction = action_id[3:]
            dest, seconds, _ = self._route_seconds(hero, direction)
            until = self.clock.now() + seconds
            hero.activity = {"kind": "travel", "to": [dest.x, dest.y], "until": until, "dir": direction}
            self.bus.publish(TravelStarted(hero.id, dest.x, dest.y, until))
            return self._activity_view(hero, notice=t.t("travel.started", time=self._fmt_duration(seconds)))
        if action_id == "explore":
            seconds = self._seconds(self.content.balance["explore"]["minutes"])
            hero.activity = {"kind": "explore", "until": self.clock.now() + seconds}
            return self._activity_view(hero, notice=t.t("explore.started", time=self._fmt_duration(seconds)))
        return self._zone_view(hero)

    def _use_out_of_combat(self, hero: Hero, item_id: str) -> View:
        t = self.texts
        item = self.content.items.get(item_id)
        if not item or not item.get("heal"):
            return self._bag_view(hero)
        source = hero.backpack if hero.backpack.get(item_id, 0) > 0 else hero.belt
        if source.get(item_id, 0) <= 0:
            view = self._bag_view(hero)
            view.notice = t.t("combat.err.item")
            return view
        stats = hero_stats(self.content.classes[hero.class_id], hero.level)
        healed = min(stats["max_hp"] - hero.hp, round(stats["max_hp"] * item["heal"]))
        source[item_id] -= 1
        if source[item_id] <= 0:
            del source[item_id]
        hero.hp += healed
        view = self._bag_view(hero)
        view.notice = t.t("bag.used", item=t.t(item["name_key"]), amount=healed)
        return view

    # ------------------------------------------------------------------ views

    def _status_line(self, hero: Hero) -> str:
        stats = hero_stats(self.content.classes[hero.class_id], hero.level)
        return self.texts.t("hero.status_line", hp=hero.hp, max_hp=stats["max_hp"], gold=hero.gold, level=hero.level)

    def _zone_view(self, hero: Hero, notice: str | None = None) -> View:
        t = self.texts
        zone = self._zone(hero.x, hero.y)
        record = self._discovered(zone.x, zone.y) or {}
        body = [
            t.t("zone.header", name=self._zone_name(zone), biome=self._biome_label(zone)),
            t.t("zone.distance", lejania=zone.lejania, ring=ROMAN[zone.ring], level=zone.level),
        ]
        if record.get("discovered_by"):
            body.append(t.t("zone.discovered_by", name=record["discovered_by"]))
        body += [self._status_line(hero), "", t.t("zone.routes")]
        actions: list[Action] = []
        for direction in ("n", "s", "e", "w"):
            dest, seconds, known = self._route_seconds(hero, direction)
            where = f"{self._biome_label(dest)} {self._zone_name(dest)}" if known else t.t("zone.uncharted")
            body.append(t.t("zone.route_line", dir=t.t(f"dir.{direction}"), where=where, time=self._fmt_duration(seconds)))
            actions.append(Action(id=f"go:{direction}", label=t.t("zone.go_button", dir=t.t(f"dir.{direction}"), time=self._fmt_duration(seconds))))
        explore_time = self._fmt_duration(self._seconds(self.content.balance["explore"]["minutes"]))
        actions += [
            Action(id="explore", label=t.t("zone.explore_button", time=explore_time)),
            Action(id="map", label=t.t("menu.map")),
            Action(id="hero", label=t.t("menu.hero")),
            Action(id="bag", label=t.t("menu.bag")),
        ]
        return View(kind="zone", title=t.t("zone.title"), body=body, actions=actions, notice=notice)

    def _activity_view(self, hero: Hero, notice: str | None = None) -> View:
        t = self.texts
        activity = hero.activity or {}
        remaining = self._fmt_duration(activity.get("until", 0) - self.clock.now())
        if activity.get("kind") == "travel":
            x, y = activity["to"]
            dest = self._zone(x, y)
            known = self._discovered(x, y) is not None
            where = self._zone_name(dest) if known else t.t("zone.uncharted")
            body = [t.t("travel.on_the_way", where=where, dir=t.t(f"dir.{activity.get('dir', 'n')}")), t.t("travel.remaining", time=remaining)]
            title = t.t("travel.title")
        else:
            body = [t.t("explore.in_progress"), t.t("travel.remaining", time=remaining)]
            title = t.t("explore.title")
        body += ["", self._status_line(hero), t.t("activity.offline_ok")]
        actions = [
            Action(id="refresh", label=t.t("menu.refresh")),
            Action(id="map", label=t.t("menu.map")),
            Action(id="hero", label=t.t("menu.hero")),
            Action(id="bag", label=t.t("menu.bag")),
        ]
        return View(kind="activity", title=title, body=body, actions=actions, notice=notice)

    def _map_view(self, hero: Hero) -> View:
        t = self.texts
        radius = 3
        rows = []
        for y in range(hero.y + radius, hero.y - radius - 1, -1):
            row = ""
            for x in range(hero.x - radius, hero.x + radius + 1):
                if x == hero.x and y == hero.y:
                    row += "🧍"
                elif self._discovered(x, y) is not None:
                    row += self.content.biomes[self._zone(x, y).biome]["emoji"]
                else:
                    row += "▫️"
            rows.append(row)
        body = [t.t("map.legend")] + rows + ["", t.t("map.position", x=hero.x, y=hero.y, lejania=self._zone(hero.x, hero.y).lejania)]
        return View(kind="map", title=t.t("map.title"), body=body, actions=[Action(id="home", label=t.t("menu.back"))])

    def _hero_view(self, hero: Hero) -> View:
        t = self.texts
        cdef = self.content.classes[hero.class_id]
        stats = hero_stats(cdef, hero.level)
        curve = self.content.balance["hero"]["xp_curve"]
        body = [
            t.t("hero.name_line", name=hero.name, cls=t.t(cdef["name_key"]), role=t.t(cdef["role_key"])),
            t.t("hero.level_line", level=hero.level, xp=hero.xp, next=xp_for_level(curve, hero.level + 1)),
            t.t("hero.hp_line", hp=hero.hp, max_hp=stats["max_hp"]),
            t.t("hero.stats_line", attack=round(stats["attack"], 1), armor=round(stats["armor"] * 100), initiative=round(stats["initiative"])),
            t.t("hero.gold_line", gold=hero.gold),
            t.t("hero.record_line", kills=hero.kills, zones=hero.zones_discovered),
        ]
        return View(kind="hero", title=t.t("hero.title"), body=body, actions=[Action(id="home", label=t.t("menu.back"))])

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
        body = [t.t("bag.belt", items=self._item_list(hero.belt)), t.t("bag.backpack", items=self._item_list(hero.backpack)), "", self._status_line(hero)]
        actions = []
        for item_id in sorted(set(hero.backpack) | set(hero.belt)):
            item = self.content.items.get(item_id, {})
            if item.get("heal"):
                count = hero.backpack.get(item_id, 0) + hero.belt.get(item_id, 0)
                actions.append(Action(id=f"use:{item_id}", label=t.t("bag.use_button", emoji=item["emoji"], item=t.t(item["name_key"]), n=count)))
        actions.append(Action(id="home", label=t.t("menu.back")))
        return View(kind="bag", title=t.t("bag.title"), body=body, actions=actions)

    # ------------------------------------------------------------------ combat

    def _start_combat(self, hero: Hero, zone: Zone, rng: Rng, reason_key: str) -> str:
        candidates = [(eid, e) for eid, e in self.content.enemies.items() if zone.biome in e.get("biomes", [])]
        fitting = [(eid, e) for eid, e in candidates if e["level_min"] <= zone.level <= e["level_max"]]
        pool = fitting or candidates or list(self.content.enemies.items())
        enemy_id, enemy_def = pool[int(rng.random() * len(pool)) % len(pool)]
        level = max(enemy_def["level_min"], min(enemy_def["level_max"], zone.level + (1 if rng.chance(0.3) else 0)))
        seed = int(rng.random() * 2**31)
        state = make_combat(enemy_id, enemy_def, level, self.content.classes[hero.class_id], seed)
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
        cdef = self.content.classes[hero.class_id]
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
            t.t("combat.hero_line", name=hero.name, cls=t.t(cdef["name_key"])),
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
        for item_id, count in hero.belt.items():
            item = self.content.items.get(item_id)
            if item and item.get("belt"):
                actions.append(Action(id=f"use:{item_id}", label=f"{item['emoji']} {t.t(item['name_key'])} ×{count}"))
        actions.append(Action(id="back", label=t.t("menu.back")))
        body = [t.t("combat.belt_help"), t.t("combat.toxicity", n=state["hero"]["toxicity"])]
        return View(kind="combat_bag", title=t.t("combat.belt_title"), body=body, actions=actions)

    def _combat_action(self, hero: Hero, state: dict[str, Any], action_id: str) -> View:
        t = self.texts
        cdef = self.content.classes[hero.class_id]
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
            xp = int(edef["xp"] * (1 + 0.15 * (enemy["level"] - 1)))
            low, high = edef.get("gold", [1, 3])
            gold = int(rng.uniform(low, high + 1) * (1 + 0.1 * (enemy["level"] - 1)))
            hero.xp += xp
            hero.gold += gold
            hero.kills += 1
            lines.append(t.t("combat.rewards", xp=xp, gold=gold))
            for item_id, chance in edef.get("loot", {}).items():
                if item_id in self.content.items and rng.chance(chance):
                    hero.backpack[item_id] = hero.backpack.get(item_id, 0) + 1
                    item = self.content.items[item_id]
                    lines.append(t.t("combat.loot", item=f"{item['emoji']} {t.t(item['name_key'])}"))
            while hero.xp >= xp_for_level(hb["xp_curve"], hero.level + 1):
                hero.level += 1
                hero.hp = hero_stats(self.content.classes[hero.class_id], hero.level)["max_hp"]
                lines.append(t.t("combat.level_up", level=hero.level))
        elif outcome == "defeat":
            lost = int(hero.gold * hb["defeat_gold_loss"])
            hero.gold -= lost
            hero.hp = 1
            self.bus.publish(HeroDowned(hero.id))
            lines.append(t.t("combat.defeat_consequence", gold=lost))
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
