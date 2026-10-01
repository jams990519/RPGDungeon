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
    diseno/03-personaje/creacion-de-personaje.md; diseno/01-plataforma/web-y-multiplataforma.md §3;
    diseno/06-contenido/jefes.md (el Guardián, D-82); diseno/08-social/gremios-y-social.md §0 (el gremio, D-97)
Módulo: capa de servicios (une M1, M2, M3, M5, M6, M8, M9, M15 y M19)
Depende de: engine.core, engine.hero (y engine.hero.gear: equipo, D-77), engine.world, engine.combat, engine.messaging,
    engine.social (cuentas del gremio, D-97), content/*
Lo usan: adapters/telegram/bot.py, adapters/cli/play.py, tests/test_service.py
Eventos que publica: HeroCreated, TravelStarted, TravelArrived, ZoneDiscovered, CombatStarted,
    HitReceived, HeroDowned, CombatEnded, BossDefeated
Eventos que escucha: ninguno
Datos de los que es dueño: espacios "hero", "combat", "zone", "pending" y "meta" del almacén
    (en "meta", "guardian:<id>" guarda para siempre al primer héroe que venció a cada Guardián, D-82)
    D-93 (provisional) y D-95: "pantry" (despensa de cada campamento de jugadores, clave "x:y"; el Claro no tiene:
    no tiene dueño, D-95):
    {"rations", "at"}, consumo perezoso) y "active" (registro de quién jugó hoy y ayer, claves "0" y "1"
    según el día; se pisa solo, nunca crece). Diseño: diseno/02-mundo/supervivencia-del-asentamiento.md §0.4
    D-97 (provisional): "guild" (gremio de un campamento, clave "x:y" del campamento: nombre, nivel, contadores)
    y "guild_name" (nombres de gremio tomados). Los miembros del gremio son los del campamento ("camp").
Reglas que nunca se rompen:
    1. Toda orden empieza por _settle(): ningún temporizador se pierde ni se duplica.
    2. En combate no se viaja ni se explora; viajando no se explora (una actividad a la vez).
    3. Ningún texto visible se escribe aquí: todo sale de content/locales (Texts).
    4. El servicio no sabe qué cliente lo llama: el id de cuenta lo arma el adaptador.
    5. El Pionero de un Guardián se escribe una sola vez y nunca se pisa; el aviso al servidor sale una sola vez.
    6. Nada se cobra a cambio de nada: un remedio con la vida llena, la posada sin heridas o recolectar con la
       mochila llena o la zona agotada se rechazan con un aviso, sin gastar energía, monedas ni objetos.
    7. La despensa (D-93) solo recibe lo que un jugador aporta: nunca toma comida de la mochila de nadie, y el
       hambre nunca baja la etapa del Claro ni quita niveles, zonas o miembros a un campamento.
    8. El gremio (D-97) nunca saca a nadie: si el cupo baja (por ejemplo, al crear el gremio), los que ya están se quedan.
Si cambias esto, revisa:
    - Adaptadores: adapters/telegram/render.py y bot.py (IDs de acción y tipos de vista); bot.py y
      adapters/cli/play.py leen menu() y commands() (atajos /stats, /doble...)
    - Números: balance.yaml (explore, regen, hero, travel, guardian)
    - Pruebas: tests/test_service.py, tests/test_boss.py, tests/test_buttons.py, tests/test_spec_abilities.py (barra, D-79),
      tests/test_playtest_fixes.py (fallos de la prueba de juego de la 0.9.2), tests/test_pantry.py (despensa, D-93)
    - Despensa (D-93): balance.yaml pantry; engine/world/pantry.py; textos pantry.* en es.yaml
    - Gremio (D-97): balance.yaml guild; engine/social/guilds.py; textos guild.* en es.yaml; tests/test_guilds.py.
      Sus contadores se suman en _settle (exploración y recolección) y en _end_combat (victoria)
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import asdict, replace
from typing import Any, Callable

from engine.classes import (
    bar_choices,
    bar_slots,
    base_response,
    default_spec,
    ensure_talents,
    kit as talent_kit,
    set_bar_slot,
    spend_point,
    specs_of,
    unlock_points,
)
from engine.combat import CombatContext, make_combat, resolve_round, validate_choice
from engine.core import (
    BossDefeated,
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
from engine.hero.gear import auto_equip, can_use, equip, gear_bonus, piece_stats, roll_gear, source_choices, starter_gear, suits, unequip
from engine.messaging import Action, View
from engine.world import DIRECTIONS, Zone, travel_minutes, zone_at
from engine.world import pantry as pantry_rules
from engine.social import guilds as guild_rules
from engine.world.territory import first_zones
from engine.world.resources import main_resource, zone_resources

# Typed shortcuts that the texts mention (e.g. "🔀 Doble especialización: /doble"); every client offers the same ones.
COMMANDS = {"/stats": "stats", "/inv": "bag", "/habilidades": "talents", "/hero": "hero", "/zona": "home",
            "/equipo": "gear", "/monedas": "wallet", "/doble": "dual", "/gremio": "guild"}
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
        self._mark_seen(hero)
        notices = self._settle(hero)
        if action_id not in ("found", "rename") and self.store.get("camp_naming", account_id):
            self.store.delete("camp_naming", account_id)    # leaving the name prompt cancels it (no surprise camp later)
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

    def commands(self) -> dict[str, str]:
        """Typed shortcuts (/stats, /inv, /doble...) -> action id; some screens only link to them.

        [ES]
        Qué hace: da los atajos escritos que nombran los textos (/stats, /inv, /habilidades, /doble...) y a qué
        botón equivalen. La 🔀 Doble especialización solo se abre con /doble, así que todo cliente debe ofrecerlos.
        La llaman: los adaptadores (Telegram y la consola).
        Si cambia, afecta: qué escribe el jugador en cada cliente y los textos que nombran los atajos (es.yaml).
        """
        return dict(COMMANDS)

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
            if notices:          # a batch step that simply goes on stays silent (D-87)
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
        if hero.explored and not hero.exploration:      # 0.8.1: one old exploration counts as 25 % (D-87)
            hero.exploration = {key: 25 for key in hero.explored}
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
        zone = zone_at(self.world_seed, x, y, self.content.balance["travel"].get("level_per_lejania", 0.9), parts)
        cfg = self._guardian_cfg()
        if cfg and (x, y) == (cfg["x"], cfg["y"]) and cfg.get("biome") in self.content.biomes:
            zone = replace(zone, biome=cfg["biome"])     # the Guardian's lair has a fixed biome (D-82)
        return zone

    def _discovered(self, x: int, y: int) -> dict[str, Any] | None:
        if x == 0 and y == 0:
            return {"discovered_by": None}
        return self.store.get("zone", f"{x}:{y}")

    def _zone_name(self, zone: Zone) -> str:
        if zone.x == 0 and zone.y == 0:
            return self.texts.t("world.claro_name")
        if self._is_lair(zone.x, zone.y):
            return self.texts.t("guardian.lair_name")
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
        tally: dict[str, int] = {}          # what this hero did for its guild (D-97), saved once below
        while hero.activity and hero.activity["until"] <= now and self.store.get("combat", hero.id) is None:
            activity = hero.activity
            hero.activity = None
            rng = Rng(int(hash_unit(self.world_seed, hero.id, activity["until"]) * 2**31))
            if activity["kind"] == "travel":
                notices += self._arrive(hero, activity, rng)
            elif activity["kind"] in ("explore", "gather"):
                zone = self._zone(hero.x, hero.y)
                activity.setdefault("left", 0)
                activity.setdefault("got", {})
                activity.setdefault("log", [])
                activity["done"] = activity.get("done", 0) + 1
                if activity["kind"] == "explore":
                    fight = self._explore_step(hero, zone, rng, activity)
                    tally["explorations"] = tally.get("explorations", 0) + 1
                    if zone.x == 0 and zone.y == 0:
                        activity["log"] += self._tutorial(hero, "explore_claro")
                else:
                    before = sum(activity["got"].values())
                    fight = self._gather_step(hero, zone, rng, activity)
                    tally["gathered"] = tally.get("gathered", 0) + sum(activity["got"].values()) - before
                    activity["log"] += self._tutorial(hero, "gather")
                if fight:
                    notices += self._batch_summary(hero, activity, "fight") + [fight]
                    continue
                reason = self._continue_batch(hero, activity, activity["until"])
                if reason:
                    notices += self._batch_summary(hero, activity, reason)
            elif activity["kind"] == "rest":
                hero.hp = hero_stats(self._kit(hero), hero.level)["max_hp"]
                notices.append(self.texts.t("inn.rested"))
                notices += self._tutorial(hero, "heal")
        self._guild_count(hero, tally)
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

    def _explore_step(self, hero: Hero, zone: Zone, rng: Rng, activity: dict[str, Any]) -> str | None:
        """One exploration: +15-30 % of the zone, maybe a find; returns a combat notice if a fight starts (D-87)."""
        t = self.texts
        key = f"{zone.x}:{zone.y}"
        before = self._known_resources(hero, zone.x, zone.y)
        low, high = self.content.balance["exploration"]["per_step"]
        hero.exploration[key] = min(100, self._explored_pct(hero, zone.x, zone.y) + int(rng.uniform(low, high + 1)))
        if key not in hero.explored:
            hero.explored.append(key)
        new = [r for r in self._known_resources(hero, zone.x, zone.y) if r not in before]
        if new:
            names = ", ".join(f"{self.content.items[r]['emoji']} {t.t(self.content.items[r]['name_key'])}" for r in new)
            activity["log"].append(t.t("explore.revealed", items=names))
        if hero.exploration[key] >= 100:
            activity["log"].append(t.t("explore.full", name=self._zone_name(zone)))
        bal = self.content.balance["explore"]
        roll = rng.random()
        if roll < bal["encounter"] and self.content.biomes[zone.biome]["danger"] > 0 and not self._territory(zone.x, zone.y):
            return self._start_combat(hero, zone, rng, "encounter.found")
        if roll < bal["encounter"] + bal["item"]:
            options = ["hierba_curativa", "pieza_metal", "venda", "pocion_vida"]
            item_id = rng.pick_weighted(options, [5, 3, 2, 1])
            if self._bag_add(hero, item_id, 1):
                activity["got"][item_id] = activity["got"].get(item_id, 0) + 1
            return None
        coins = int(zone.level * rng.uniform(2, 5)) + 1
        hero.gold += coins
        activity["coins"] = activity.get("coins", 0) + coins
        return None

    def _gather_step(self, hero: Hero, zone: Zone, rng: Rng, activity: dict[str, Any]) -> str | None:
        """One gathering: only the resources this zone has, less when it is depleted, up to the backpack's space (D-87)."""
        bal = self.content.balance["gather"]
        danger = self.content.biomes[zone.biome]["danger"] * bal["encounter_scale"]
        land = self._territory(zone.x, zone.y)
        if danger > 0 and not land and rng.chance(danger):
            return self._start_combat(hero, zone, rng, "gather.ambush")
        cfg = self.content.balance["stock"]
        resources = self._zone_resources(zone.x, zone.y)
        stock = self._stock(zone.x, zone.y)
        low, high = bal["amount"]
        amount = int(rng.uniform(low, high + 1)) + zone.level // 3
        if land and not land.get("claro") and hero.id in land.get("members", []):
            amount = int(amount * bal["own_land_bonus"] + 0.5)     # your camp's land gives more (D-87)
        got: dict[str, int] = {}
        for _ in range(max(1, amount)):
            options = [r for r in resources if stock[r] >= cfg["min_yield"]]
            if not options or self._bag_used(hero) >= self._bag_cap():
                break
            res = rng.pick_weighted(options, [resources[r] * stock[r] for r in options])
            if not self._bag_add(hero, res, 1):
                break
            stock[res] = max(0.0, stock[res] - cfg["per_unit"])
            got[res] = got.get(res, 0) + 1
        self.store.put("stock", f"{zone.x}:{zone.y}", {"levels": stock, "at": self.clock.now()})
        for res, n in got.items():
            activity["got"][res] = activity["got"].get(res, 0) + n
        if not got:
            activity["left"] = 0
            activity["log"].append(self.texts.t("batch.reason.bag_full" if self._bag_used(hero) >= self._bag_cap() else "batch.reason.depleted"))
        return None

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
        if action_id == "dual":
            return self._dual_view(hero)
        if action_id == "dual_unlock":
            return self._dual_unlock(hero)
        if action_id == "dual_switch":
            return self._dual_switch(hero)
        if action_id.startswith("tal:"):
            return self._spec_view(hero, action_id[4:])
        if action_id.startswith("pt:"):
            spec = action_id[3:]
            new = spend_point(self.content.classes, self.content.balance, hero, spec)
            names = ", ".join(t.t(f"ability.{a}.name") for a in new)
            notice = t.t("talents.spent") + (" " + t.t("talents.unlocked", names=names) if new else "")
            if new and hero.bar:
                notice += " " + t.t("bar.new_hint")
            return self._spec_view(hero, spec, notice=notice)
        if action_id == "bar":
            return self._bar_view(hero)
        if action_id.startswith("barslot:"):
            parts = action_id.split(":")
            slot = int(parts[1]) if parts[1].isdigit() else 0
            page = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0
            return self._bar_slot_view(hero, slot, page)
        if action_id.startswith("barset:"):
            parts = action_id.split(":", 2)
            slot = int(parts[1]) if len(parts) == 3 and parts[1].isdigit() else 0
            if slot and set_bar_slot(self.content.classes, hero, slot, parts[2]):
                return self._bar_view(hero, notice=t.t("bar.saved", name=t.t(f"ability.{parts[2]}.name"), n=slot))
            return self._bar_view(hero)
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
        if action_id == "memento":
            return self._memento_view(hero)
        if action_id.startswith("mem:"):
            return self._use_memento(hero, action_id[4:])
        in_claro = hero.x == 0 and hero.y == 0 and not hero.activity
        if action_id == "found":
            return self._ask_camp_name(hero, "found")
        if action_id == "rename":
            return self._ask_camp_name(hero, "rename")
        if action_id == "cancel_name":
            self.store.delete("camp_naming", hero.id)
            return self._camp_here_view(hero)
        if action_id == "grow" or action_id.startswith("grow:"):
            page = action_id[5:]
            return self._grow_view(hero, int(page) if page.isdigit() else 0)
        if action_id.startswith("claim:"):
            try:
                cx, cy = (int(v) for v in action_id[6:].split(":"))
            except ValueError:
                return self._camp_here_view(hero)
            return self._grow_camp(hero, cx, cy)
        if action_id == "campfeed":
            return self._camp_feed(hero)
        if action_id == "askjoin":
            return self._ask_join(hero)
        if action_id == "leave":
            return self._leave_camp(hero)
        if action_id == "guild":
            return self._guild_view(hero)
        if action_id == "guildnew":
            return self._ask_guild_name(hero)
        if action_id == "guildup":
            return self._rise_guild(hero)
        if action_id == "claro" and not in_claro:
            return self._camp_here_view(hero)
        if action_id == "claro":
            return self._claro_view(hero)
        if action_id in ("camp", "donate", "feed"):     # "feed": old 0.10 button, the Claro has no pantry now (D-95)
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
        if action_id == "stop":
            return self._stop_batch(hero)
        if hero.activity:
            view = self._activity_view(hero)
            view.notice = t.t("activity.busy")
            return view
        if action_id == "boss":
            return self._challenge_guardian(hero)
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
        if action_id == "gather" and self._is_lair(hero.x, hero.y):
            return self._explore_menu(hero, notice=t.t("guardian.no_gather"))
        if action_id in ("gather", "explore"):
            return self._amount_view(hero, action_id, 0)
        if action_id.startswith("amt:"):
            _, kind, page = action_id.split(":")
            return self._amount_view(hero, kind, int(page) if page.isdigit() else 0)
        if action_id.startswith("do:"):
            _, kind, amount = action_id.split(":")
            return self._start_batch(hero, kind, amount)
        return self._zone_view(hero)

    # ------------------------------------------------------------------ batches of energy (D-87)

    def _amount_view(self, hero: Hero, kind: str, page: int) -> View:
        """Choose how much energy to spend in a row (5, 10, 20, 40 or all) — or cancel (D-87)."""
        t = self.texts
        if kind not in ("gather", "explore"):
            return self._explore_menu(hero)
        zone = self._zone(hero.x, hero.y)
        if kind == "explore" and self._explored_pct(hero, zone.x, zone.y) >= 100:
            return self._explore_menu(hero, notice=t.t("explore.already_full"))
        if kind == "gather" and self._gather_blocked(hero, zone):
            return self._explore_menu(hero, notice=t.t(self._gather_blocked(hero, zone)))
        if hero.energy < 1:
            return self._explore_menu(hero, notice=self._no_energy_notice(hero))
        minutes = self.content.balance[kind]["minutes"]
        body = [t.t(f"batch.ask_{kind}", minutes=minutes), t.t("batch.energy", energy=hero.energy)]
        if kind == "gather":
            body.append(t.t("batch.space", used=self._bag_used(hero), cap=self._bag_cap()))
        else:
            body.append(t.t("batch.explored", pct=self._explored_pct(hero, zone.x, zone.y)))
        body.append(t.t("batch.cancel_hint"))
        options = [n for n in self.content.balance["energy"]["batch"] if n <= hero.energy]
        pages = [options[:2], options[2:]]
        page = page % 2
        actions = [Action(id=f"do:{kind}:{n}", label=t.t("batch.button", n=n)) for n in pages[page]]
        if page == 0:
            if len(options) > 2 or hero.energy not in options:
                actions.append(Action(id=f"amt:{kind}:1", label=t.t("batch.more")))
            actions.append(Action(id="explore_menu", label=t.t("batch.cancel")))
        else:
            if hero.energy not in options:
                actions.append(Action(id=f"do:{kind}:max", label=t.t("batch.max", n=hero.energy)))
            actions.append(Action(id=f"amt:{kind}:0", label=t.t("batch.back")))
        if not options:
            actions = [Action(id=f"do:{kind}:max", label=t.t("batch.max", n=hero.energy)), Action(id="explore_menu", label=t.t("batch.cancel"))]
        return View(kind="batch", title=t.t(f"batch.title_{kind}"), body=body, actions=actions[:4])

    def _start_batch(self, hero: Hero, kind: str, amount: str) -> View:
        t = self.texts
        if kind not in ("gather", "explore"):
            return self._explore_menu(hero)
        n = hero.energy if amount == "max" else (int(amount) if amount.isdigit() else 0)
        n = min(n, hero.energy)
        zone = self._zone(hero.x, hero.y)
        if kind == "gather" and self._gather_blocked(hero, zone):
            return self._explore_menu(hero, notice=t.t(self._gather_blocked(hero, zone)))   # no energy spent for nothing
        if n < 1 or not self._spend_energy(hero, kind):
            return self._explore_menu(hero, notice=self._no_energy_notice(hero))
        if kind == "explore" and self._explored_pct(hero, zone.x, zone.y) >= 100:
            hero.energy += self.content.balance["energy"][f"per_{kind}"]
            return self._explore_menu(hero, notice=t.t("explore.already_full"))
        seconds = self._seconds(self.content.balance[kind]["minutes"])
        hero.activity = {"kind": kind, "until": self.clock.now() + seconds, "left": n - 1, "total": n, "done": 0, "got": {}, "log": []}
        return self._activity_view(hero, notice=t.t(f"batch.started_{kind}", n=n, time=self._fmt_duration(seconds * n)))

    def _gather_blocked(self, hero: Hero, zone: Zone) -> str | None:
        """Text key of why gathering here would give nothing (full backpack or depleted zone), else None."""
        if self._bag_used(hero) >= self._bag_cap():
            return "batch.reason.bag_full"
        stock = self._stock(zone.x, zone.y)
        if all(level < self.content.balance["stock"]["min_yield"] for level in stock.values()):
            return "batch.reason.depleted"
        return None

    def _stop_batch(self, hero: Hero) -> View:
        """Cancel the batch: the step in progress gives its energy back (D-87)."""
        t = self.texts
        activity = hero.activity or {}
        if activity.get("kind") not in ("gather", "explore"):
            return self._main_view(hero)
        hero.energy += self.content.balance["energy"][f"per_{activity['kind']}"]
        hero.activity = None
        lines = self._batch_summary(hero, activity, "stopped")
        return self._explore_menu(hero, notice=self._join(lines))

    def _batch_summary(self, hero: Hero, activity: dict[str, Any], reason: str) -> list[str]:
        t = self.texts
        kind = activity["kind"]
        lines = []
        if activity.get("done"):
            if kind == "gather":
                lines.append(t.t("batch.gathered", n=activity["done"], items=self._item_list(activity.get("got", {}))))
            else:
                zone = self._zone(hero.x, hero.y)
                lines.append(t.t("batch.explored_done", n=activity["done"], pct=self._explored_pct(hero, zone.x, zone.y)))
                if activity.get("got"):
                    lines.append(t.t("batch.found", items=self._item_list(activity["got"])))
                if activity.get("coins"):
                    lines.append(t.t("batch.coins", coins=self._money(activity["coins"])))
        lines += activity.get("log", [])
        if reason not in ("done", "full_explored"):        # reaching 100 % already has its own line
            lines.append(t.t(f"batch.reason.{reason}"))
        return lines

    def _continue_batch(self, hero: Hero, activity: dict[str, Any], until: float) -> str | None:
        """After a finished step: start the next one, or say why the batch stops."""
        kind = activity["kind"]
        zone = self._zone(hero.x, hero.y)
        if activity["left"] <= 0:
            return "done"
        if kind == "explore" and self._explored_pct(hero, zone.x, zone.y) >= 100:
            return "full_explored"
        if kind == "gather" and self._bag_used(hero) >= self._bag_cap():
            return "bag_full"
        if not self._spend_energy(hero, kind):
            return "energy"
        activity["left"] -= 1
        activity["until"] = until + self._seconds(self.content.balance[kind]["minutes"])
        hero.activity = activity
        return None

    # ------------------------------------------------------------------ zone resources and exploration (D-87)

    def _bag_cap(self) -> int:
        return self.content.balance["hero"]["backpack_capacity"]

    def _bag_used(self, hero: Hero) -> int:
        return sum(hero.backpack.values())

    def _bag_add(self, hero: Hero, item_id: str, count: int) -> int:
        """Put items in the backpack up to its space; returns how many fit."""
        fit = max(0, min(count, self._bag_cap() - self._bag_used(hero)))
        if fit:
            hero.backpack[item_id] = hero.backpack.get(item_id, 0) + fit
        return fit

    def _zone_resources(self, x: int, y: int) -> dict[str, float]:
        zone = self._zone(x, y)
        return zone_resources(self.world_seed, x, y, zone.biome, self.content.balance, self.content.biomes)

    def _stock(self, x: int, y: int) -> dict[str, float]:
        """How much is left of each resource in a zone (1.0 = full), regenerating with time."""
        cfg = self.content.balance["stock"]
        data = self.store.get("stock", f"{x}:{y}") or {}
        hours = (self.clock.now() - data.get("at", self.clock.now())) / (3600 * self.time_scale)
        levels = data.get("levels", {})
        return {res: min(1.0, levels.get(res, 1.0) + hours * cfg["regen_per_hour"]) for res in self._zone_resources(x, y)}

    def _explored_pct(self, hero: Hero, x: int, y: int) -> int:
        return hero.exploration.get(f"{x}:{y}", 0)

    def _known_resources(self, hero: Hero, x: int, y: int) -> list[str]:
        """The resources this hero has found in a zone: more of them as it explores (D-87)."""
        pct = self._explored_pct(hero, x, y)
        ranked = list(self._zone_resources(x, y))
        reveal = self.content.balance["exploration"]["reveal_at"]
        count = len(ranked) if pct >= 100 else sum(1 for need in reveal if pct >= need)
        return ranked[:count]

    def _resources_line(self, hero: Hero, x: int, y: int) -> str:
        t = self.texts
        known = self._known_resources(hero, x, y)
        pct = self._explored_pct(hero, x, y)
        if not known:
            return t.t("explore.resources_unknown", pct=pct)
        stock = self._stock(x, y)
        parts = []
        for res in known:
            item = self.content.items[res]
            bars = round(stock[res] * 5)
            parts.append(f"{item['emoji']} {t.t(item['name_key'])} {'▰' * bars}{'▱' * (5 - bars)}")
        more = "" if pct >= 100 else " · ❔"
        return t.t("explore.resources_line", pct=pct, items=" · ".join(parts) + more)

    def _use_out_of_combat(self, hero: Hero, item_id: str) -> View:
        t = self.texts
        item = self.content.items.get(item_id)
        if not item or not item.get("heal"):
            return self._potions_view(hero)
        source = hero.backpack if hero.backpack.get(item_id, 0) > 0 else hero.belt
        if source.get(item_id, 0) <= 0:
            return self._potions_view(hero, notice=t.t("combat.err.item"))
        stats = hero_stats(self._kit(hero), hero.level)
        if hero.hp >= stats["max_hp"]:
            return self._potions_view(hero, notice=t.t("bag.full_hp"))      # never waste a remedy for 0 health
        healed = min(stats["max_hp"] - hero.hp, round(stats["max_hp"] * item["heal"]))
        source[item_id] -= 1
        if source[item_id] <= 0:
            del source[item_id]
        hero.hp += healed
        if item.get("kind") == "potion":
            hero.downed = False             # D-83: drinking a potion ends the slow recovery
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
        body.append(self._resources_line(hero, zone.x, zone.y))
        camp = self.store.get("camp", f"{zone.x}:{zone.y}")
        land = self._territory(zone.x, zone.y)
        if camp:
            body.append(t.t("camps.zone_line", name=camp["name"], n=len(camp["members"])))
        elif land and land.get("claro"):
            if (zone.x, zone.y) != (0, 0):
                body.append(t.t("camps.claro_land"))
        elif land:
            body.append(t.t("camps.land_line", name=land["name"]))
        body += self._lair_lines(zone)
        body += [self._status_line(hero)]
        body += self._tutorial_hint(hero)
        body += ["", t.t("zone.routes")]
        actions: list[Action] = []
        for direction in ("n", "s", "e", "w"):
            dest, seconds, known = self._route_seconds(hero, direction)
            if known:
                where = f"{self._biome_label(dest)} {self._zone_name(dest)}"
                if self._is_lair(dest.x, dest.y):
                    where += t.t("guardian.route_mark")
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
            body = [t.t("gather.in_progress"), t.t("batch.progress", done=activity.get("done", 0) + 1, total=activity.get("total", 1)),
                    t.t("travel.remaining", time=remaining), t.t("batch.space", used=self._bag_used(hero), cap=self._bag_cap())]
            title = t.t("gather.title")
        elif activity.get("kind") == "rest":
            body = [t.t("inn.in_progress"), t.t("travel.remaining", time=remaining)]
            title = t.t("inn.title")
        else:
            zone = self._zone(hero.x, hero.y)
            body = [t.t("explore.in_progress"), t.t("batch.progress", done=activity.get("done", 0) + 1, total=activity.get("total", 1)),
                    t.t("travel.remaining", time=remaining), t.t("batch.explored", pct=self._explored_pct(hero, zone.x, zone.y))]
            title = t.t("explore.title")
        body += ["", self._status_line(hero), t.t("activity.offline_ok")]
        actions = [Action(id="refresh", label=t.t("menu.refresh"))]
        if activity.get("kind") in ("gather", "explore"):
            actions.append(Action(id="stop", label=t.t("batch.stop")))
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

    def _claro_view(self, hero: Hero, notice: str | None = None) -> View:
        """The Claro's camp screen: the common work, the trader and the inn (no pantry: it has no owner, D-95)."""
        t = self.texts
        body = [t.t("claro.intro"), self._status_line(hero)]
        return View(kind="claro", title=t.t("claro.title"), body=body + self._tutorial_hint(hero),
                    actions=[Action(id="camp", label=t.t("camp.button")), Action(id="shop", label=t.t("shop.button")),
                             Action(id="inn", label=t.t("inn.button", price=self._money(self._inn_price()))), Action(id="home", label=t.t("menu.back"))],
                    notice=notice)

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
        lines = [t.t("camp.donated", items=self._item_list(given), xp=int(xp * self._xp_mult(hero)), merit=units)]   # the xp really given
        lines += self._give_xp(hero, xp)
        lines += self._claro_rise(data)
        self.store.put("settlement", "claro", data)
        lines += self._tutorial(hero, "donate")
        return self._camp_view(hero, notice="\n".join(lines))

    def _work_paid(self, data: dict[str, Any]) -> bool:
        """True when every material of the Claro's current stage is in."""
        stage = self.content.balance["settlement"]["stages"][data["stage"]]
        return bool(stage["needs"]) and all(data["progress"].get(i, 0) >= n for i, n in stage["needs"].items())

    def _claro_rise(self, data: dict[str, Any]) -> list[str]:
        """Raise the Claro one stage when its work is paid (it never goes down and has no pantry, D-95).

        [ES]
        Qué hace: sube el Claro de etapa cuando la obra común está pagada. El Claro no se mantiene: no tiene
        dueño, así que no tiene despensa (D-95); solo los campamentos de jugadores comen (D-93).
        La llama: _donate. Nunca baja la etapa.
        Si cambia, afecta: el ritmo del Claro hasta castillo (P-55), su territorio y la posada.
        """
        t = self.texts
        stages = self.content.balance["settlement"]["stages"]
        if not self._work_paid(data):
            return []
        nxt = stages[data["stage"] + 1]["id"]
        data["stage"] += 1
        data["progress"] = {}
        return [t.t("camp.stage_up", stage=t.t(f"camp.stages.{nxt}"))]

    # ------------------------------------------------------------------ settlement pantry (D-93, provisional)

    def _day_seconds(self) -> float:
        return self._seconds(24 * 60)

    def _mark_seen(self, hero: Hero) -> None:
        """Note that this hero is playing now (D-93).

        Hero.seen_at changes on every button; the shared registry ("active", two keys that alternate
        by day) is written only once per refresh slot, so counting active residents never scans heroes.

        [ES]
        Qué hace: anota que el héroe jugó ahora. El registro "active" guarda, para hoy y ayer, a quién se vio.
        Se escribe como mucho una vez por hora por héroe.
        La llama: act() en cada botón.
        Si cambia, afecta: cuántos comen de cada despensa.
        """
        now = self.clock.now()
        slot = self._seconds(self.content.balance["pantry"]["active_refresh_minutes"])
        if int(now // slot) != int(hero.seen_at // slot):
            day = int(now // self._day_seconds())
            key = str(day % 2)
            record = self.store.get("active", key) or {}
            if record.get("day") != day:
                record = {"day": day, "seen": {}}          # the slot held the day before yesterday: start it again
            entry = record["seen"].get(hero.id, {})
            entry["t"] = now
            record["seen"][hero.id] = entry
            self.store.put("active", key, record)
        hero.seen_at = now

    def _active_cutoff(self) -> float:
        return self.clock.now() - self._seconds(self.content.balance["pantry"]["active_hours"] * 60)

    def _active(self) -> dict[str, dict[str, float]]:
        """Heroes seen in the last pantry.active_hours: account -> {"t": last seen}."""
        day = int(self.clock.now() // self._day_seconds())
        merged: dict[str, dict[str, float]] = {}
        for key in ("0", "1"):
            record = self.store.get("active", key) or {}
            if record.get("day") not in (day, day - 1):
                continue
            for account, entry in record.get("seen", {}).items():
                row = merged.setdefault(account, {"t": 0.0})
                row["t"] = max(row["t"], entry.get("t", 0.0))
        cutoff = self._active_cutoff()
        return {account: row for account, row in merged.items() if row["t"] >= cutoff}

    def _camp_active(self, camp: dict[str, Any]) -> int:
        """Active members of a camp (they eat from its pantry)."""
        active = self._active()
        return sum(1 for member in camp.get("members", []) if member in active)

    def _pantry(self, key: str, active: int, eaters: Callable[[], int]) -> dict[str, float]:
        """Read a pantry after the lazy consumption and save it. A new one starts with pantry.start_days of food
        for max(active, eaters()) residents; that also covers settlements that existed before the patch."""
        cfg = self.content.balance["pantry"]
        now = self.clock.now()
        data = self.store.get("pantry", key)
        if data is None:
            rations = cfg["start_days"] * cfg["ration_per_day"] * max(1, active, eaters())
        else:
            days = (now - data.get("at", now)) / self._day_seconds()
            rations = pantry_rules.consume(data.get("rations", 0.0), active, days, cfg["ration_per_day"])
        data = {"rations": float(rations), "at": now}
        self.store.put("pantry", key, data)
        return data

    def _pantry_status(self, key: str, active: int, eaters: Callable[[], int]) -> dict[str, Any]:
        cfg = self.content.balance["pantry"]
        data = self._pantry(key, active, eaters)
        days = pantry_rules.days_left(data["rations"], active, cfg["ration_per_day"])
        return {"key": key, "rations": data["rations"], "active": active, "days": days,
                "state": pantry_rules.state(days, cfg["states"])}

    def _camp_pantry(self, camp: dict[str, Any]) -> dict[str, Any] | None:
        """A player camp's small pantry from pantry.camp_from_level on (None before)."""
        if camp.get("level", 1) < self.content.balance["pantry"]["camp_from_level"]:
            return None
        return self._pantry_status(f"{camp['x']}:{camp['y']}", self._camp_active(camp), lambda: len(camp.get("members", [])))

    def _camp_starving(self, camp: dict[str, Any]) -> bool:
        """True if the camp has a pantry and it is empty (hambruna): then it cannot grow."""
        pantry = self._camp_pantry(camp)
        return pantry is not None and pantry["state"] == "hambruna"

    def _pantry_line(self, pantry: dict[str, Any]) -> str:
        t = self.texts
        return t.t("pantry.line", state=t.t(f"pantry.state.{pantry['state']}"), rations=int(pantry["rations"]), days=pantry["days"])

    def _pantry_lines(self, pantry: dict[str, Any]) -> list[str]:
        return [self._pantry_line(pantry), self.texts.t("pantry.eaters", n=pantry["active"]), self.texts.t("pantry.how")]

    def _take_food(self, hero: Hero) -> tuple[dict[str, int], int]:
        """Take every food item out of the backpack; returns what was taken and its rations."""
        found, rations = pantry_rules.food_in(self.content.items, hero.backpack)
        for item_id in found:
            del hero.backpack[item_id]
        return found, rations

    def _add_rations(self, key: str, rations: int) -> None:
        """Add food to a pantry that was just read (and so already settled up to now)."""
        data = self.store.get("pantry", key) or {"rations": 0.0, "at": self.clock.now()}
        data["rations"] = float(data.get("rations", 0.0)) + rations
        self.store.put("pantry", key, data)

    def _food_reward(self, hero: Hero, given: dict[str, int], rations: int) -> tuple[list[str], int]:
        """Experience and merit for food given, like the common work (pantry.xp_per_ration, merit_per_ration)."""
        cfg = self.content.balance["pantry"]
        xp = rations * cfg["xp_per_ration"]
        merit = rations * cfg["merit_per_ration"]
        hero.merit += merit
        lines = [self.texts.t("pantry.fed", items=self._item_list(given), rations=rations, xp=int(xp * self._xp_mult(hero)), merit=merit)]
        return lines + self._give_xp(hero, xp), merit

    def _camp_feed(self, hero: Hero) -> View:
        """🌾 Aportar comida in your own camp (from level 3): the food goes to the camp's pantry (D-93).

        [ES]
        Qué hace: pasa toda la comida de la mochila a la despensa de tu campamento (hay que estar en él).
        La llaman: el botón 🌾 Aportar comida de la pantalla del campamento (miembros, desde nivel 3).
        Si cambia, afecta: si el campamento puede crecer (con la despensa vacía no crece).
        """
        t = self.texts
        key = f"{hero.x}:{hero.y}"
        camp = self.store.get("camp", key)
        if not camp or hero.id not in camp["members"] or hero.activity:
            return self._camp_here_view(hero)
        if self._camp_pantry(camp) is None:               # also settles the pantry up to now
            return self._camp_here_view(hero, notice=t.t("pantry.not_yet_camp", level=self.content.balance["pantry"]["camp_from_level"]))
        given, rations = self._take_food(hero)
        if not rations:
            return self._camp_here_view(hero, notice=t.t("pantry.no_food"))
        self._add_rations(f"{camp['x']}:{camp['y']}", rations)
        lines, _ = self._food_reward(hero, given, rations)
        return self._camp_here_view(hero, notice="\n".join(lines))

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
        lines = [self.texts.t("tutorial.reward", gold=self._money(cfg["reward_gold"]), xp=int(cfg["reward_xp"] * self._xp_mult(hero)))]
        return lines + self._give_xp(hero, cfg["reward_xp"])

    def _tutorial_hint(self, hero: Hero) -> list[str]:
        steps = self.content.balance["tutorial"]["steps"]
        if hero.tutorial >= len(steps):
            return []
        return ["", self.texts.t("tutorial.hint_title", n=hero.tutorial + 1, total=len(steps)),
                self.texts.t(f"tutorial.steps.{steps[hero.tutorial]}")]

    def _shop_view(self, hero: Hero, notice: str | None = None) -> View:
        """The Claro trader: buy belt items and 🥖 provisions (D-93), sell materials (half price).

        [ES] Hasta 3 botones de compra (shop.sells) + 💱 Vender materiales; ↩️ Volver solo si cabe (tope de 4, D-75).
        """
        t = self.texts
        shop = self.content.balance["shop"]
        body = [t.t("shop.intro"), t.t("hero.gold_line", gold=self._money(hero.gold)), ""]
        actions = []
        for item_id in shop["sells"]:
            item = self.content.items[item_id]
            body.append(t.t("shop.buy_line", emoji=item["emoji"], item=t.t(item["name_key"]), price=self._money(item["price"])))
            actions.append(Action(id=f"buy:{item_id}", label=t.t("shop.buy_button", emoji=item["emoji"], price=self._money(item["price"]))))
        actions = actions[:3]
        sellable = {i: n for i, n in hero.backpack.items()      # food stays: it feeds the pantry (D-93)
                    if self.content.items.get(i, {}).get("kind") == "material" and not self.content.items[i].get("food")}
        if sellable:
            total = sum(max(1, int(self.content.items[i]["price"] * shop["sell_ratio"])) * n for i, n in sellable.items())
            body.append(t.t("shop.sell_line", items=self._item_list(sellable), total=self._money(total)))
            actions.append(Action(id="sell:all", label=t.t("shop.sell_all_button", total=self._money(total))))
        if len(actions) < 4:     # 4 buttons at most (D-75); without room, 🏕️ Campamento in the menu goes back to the same place
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
                if item.get("kind") == "material" and not item.get("food") and n > 0:
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
        if hero.hp >= hero_stats(self._kit(hero), hero.level)["max_hp"]:
            return self._claro_view(hero, notice=t.t("inn.full_hp"))       # do not charge for a useless night
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
        body = [t.t("zone.header", name=self._zone_name(zone), biome=self._biome_label(zone)), t.t("explore.menu_intro"),
                self._resources_line(hero, zone.x, zone.y), t.t("batch.space", used=self._bag_used(hero), cap=self._bag_cap())]
        body += self._tutorial_hint(hero)
        actions = [Action(id="explore", label=t.t("zone.explore_button", time=explore_time)),
                   Action(id="gather", label=t.t("gather.button", time=gather_time)),
                   Action(id="map", label=t.t("menu.map")), Action(id="places", label=t.t("menu.places"))]
        if self._is_lair(zone.x, zone.y):
            # The lair (D-82): the challenge takes the gather slot (4 buttons at most, D-75).
            body += ["", self._guardian_ready_line(hero), t.t("guardian.no_gather")]
            actions[1] = Action(id="boss", label=t.t("guardian.button"))
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
            (t.t("camps.req_explored", pct=self._explored_pct(hero, zone.x, zone.y)), self._explored_pct(hero, zone.x, zone.y) >= 100),
            (t.t("camps.req_known", n=known, need=cfg["known_neighbors"]), known >= cfg["known_neighbors"]),
            (t.t("camps.req_alone", n=cfg["min_distance"]), not near and not self._territory(zone.x, zone.y)),
            (t.t("camps.req_cost", items=self._item_list(cfg["found_cost"])), cost_ok),
            (t.t("camps.req_one"), hero.camp is None),
        ]

    def _camp_here_view(self, hero: Hero, notice: str | None = None) -> View:
        """The player camp in this zone (or what founding one here needs).

        [ES]
        Qué hace: muestra el campamento de la zona. Botones de un miembro: ⬆️ Agrandar, 🌾 Aportar comida (desde
        nivel 3), 🛡️ Gremio (ahí están los miembros, ✏️ Renombrar y 🚪 Salir, D-97) y ↩️ Volver: 4 como máximo.
        La llaman: el botón 🏕️ Campamento fuera del Claro y casi todas las acciones de campamento.
        Si cambia, afecta: tests/test_camps.py, tests/test_pantry.py y tests/test_guilds.py (orden de los botones).
        """
        t = self.texts
        zone = self._zone(hero.x, hero.y)
        key = f"{zone.x}:{zone.y}"
        camp = self.store.get("camp", key)
        if camp:
            level = camp.get("level", 1)
            guild = self.store.get("guild", key)
            body = [t.t("camps.info", name=camp["name"], founder=camp["founder"], x=zone.x, y=zone.y, n=len(camp["members"])),
                    t.t("camps.stage_line", stage=self._camp_stage(level)),
                    t.t("camps.size", level=level, zones=len(camp.get("zones", [[zone.x, zone.y]]))),
                    t.t("guild.members_cap" if guild else "camps.members_cap", n=len(camp["members"]), cap=self._members_cap(camp))]
            if guild:
                body.append(t.t("guild.camp_line_visitor", name=guild["name"], level=guild["level"]))
            actions = []
            if hero.id in camp["members"]:
                body += [t.t("camps.you_member"), t.t("camps.grow_cost", items=self._item_list(self._grow_cost(level)))]
                actions.append(Action(id="grow", label=t.t("camps.grow_button")))
                pantry = self._camp_pantry(camp)          # D-93: from level 3 (aldea), a small pantry
                if pantry:
                    body += self._pantry_lines(pantry) + ([t.t("pantry.famine_camp")] if pantry["state"] == "hambruna" else [])
                    actions.append(Action(id="campfeed", label=t.t("pantry.feed_button")))
                # D-97: the guild screen holds the camp's members, rename (founder) and leave (members): 4 buttons at most
                actions.append(Action(id="guild", label=t.t("guild.button")))
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
        if pending.get("mode") == "guild":                 # the same prompt names a guild (D-97)
            return self._name_guild(hero, name, pending)
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
        """How many members fit: the guild's capacity if the camp has a guild (D-97), else base + per level (D-84).

        [ES]
        Qué hace: da el cupo del campamento. Con gremio, manda el nivel del gremio (guild.levels); sin gremio,
        la cuenta de siempre (camps.members_base + members_per_level por nivel). Nunca saca a nadie: si el cupo
        baja, solo impide que entren más.
        La llaman: la pantalla del campamento y del gremio, _ask_join y _answer_join.
        Si cambia, afecta: quién puede entrar a cada campamento y el mínimo de miembros para castillo.
        """
        guild = self.store.get("guild", f"{camp['x']}:{camp['y']}")
        if guild:
            return guild_rules.capacity(self.content.balance["guild"]["levels"], guild["level"])
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
            return self._camp_here_view(hero, notice=t.t("guild.full" if self.store.get("guild", key) else "camps.full"))
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

    def _grow_candidates(self, camp: dict[str, Any]) -> list[list[int]]:
        """Free zones touching the camp's land: where it can grow next (D-87: you choose)."""
        zones = camp.get("zones", [[camp["x"], camp["y"]]])
        seen, out = {tuple(z) for z in zones}, []
        for zx, zy in zones:
            for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                c = (zx + dx, zy + dy)
                if c not in seen and self._territory(*c) is None:
                    seen.add(c)
                    out.append(list(c))
        out.sort(key=lambda c: (max(abs(c[0] - camp["x"]), abs(c[1] - camp["y"])), c[1] < camp["y"], c))
        return out

    def _grow_view(self, hero: Hero, page: int = 0) -> View:
        """Pick which neighbouring zone the camp takes, seeing the resources you know there (D-87)."""
        t = self.texts
        camp = self.store.get("camp", f"{hero.x}:{hero.y}")
        if not camp or hero.id not in camp["members"]:
            return self._camp_here_view(hero)
        if self._camp_starving(camp):          # D-93: with an empty pantry the camp does not grow
            return self._camp_here_view(hero, notice=t.t("pantry.grow_famine"))
        level = camp.get("level", 1)
        candidates = self._grow_candidates(camp)
        body = [t.t("camps.grow_intro", items=self._item_list(self._grow_cost(level)))]
        castle = self._castle_needs(camp)      # D-97: becoming a castle needs a guild that is ready
        if castle:
            body += ["", t.t("guild.castle_title")] + [("✅ " if ok else "▫️ ") + text for text, ok in castle]
            if not all(ok for _, ok in castle):
                return View(kind="camp_grow", title=t.t("camps.grow_title"), body=body + ["", t.t("guild.castle_blocked")],
                            actions=[Action(id="guild", label=t.t("guild.button")), Action(id="claro", label=t.t("menu.back"))])
        if not candidates:
            return self._camp_here_view(hero, notice=t.t("camps.grow_blocked"))
        per = 3 if len(candidates) <= 3 else 2
        pages = max(1, (len(candidates) + per - 1) // per)
        page %= pages
        actions = []
        for cx, cy in candidates[page * per: page * per + per]:
            known = self._known_resources(hero, cx, cy)
            icons = "".join(self.content.items[r]["emoji"] for r in known) or "❔"
            body.append(t.t("camps.grow_option", x=cx, y=cy, items=icons))
            actions.append(Action(id=f"claim:{cx}:{cy}", label=t.t("camps.grow_option", x=cx, y=cy, items=icons)))
        if pages > 1:
            actions.append(Action(id=f"grow:{page + 1}", label=t.t("camps.grow_more")))
        actions.append(Action(id="claro", label=t.t("menu.back")))
        return View(kind="camp_grow", title=t.t("camps.grow_title"), body=body, actions=actions)

    def _camp_stage(self, level: int) -> str:
        stages = self.content.balance["camps"]["stages"]
        name = stages[0]["id"]
        for stage in stages:
            if level >= stage["from_level"]:
                name = stage["id"]
        return self.texts.t(f"camps.stage.{name}")

    def _grow_camp(self, hero: Hero, cx: int, cy: int) -> View:
        """Make the camp bigger: pay materials and take the chosen free zone next to its land (1, 2, 3, 4... zones)."""
        t = self.texts
        key = f"{hero.x}:{hero.y}"
        camp = self.store.get("camp", key)
        if not camp or hero.id not in camp["members"] or hero.activity:
            return self._camp_here_view(hero)
        if self._camp_starving(camp):          # D-93: with an empty pantry the camp does not grow
            return self._camp_here_view(hero, notice=t.t("pantry.grow_famine"))
        if not all(ok for _, ok in self._castle_needs(camp)):     # D-97: no castle without a guild that is ready
            return self._grow_view(hero)
        level = camp.get("level", 1)
        cost = self._grow_cost(level)
        if any(hero.backpack.get(i, 0) < n for i, n in cost.items()):
            return self._camp_here_view(hero, notice=t.t("camps.grow_missing", items=self._item_list(cost)))
        zones = camp.get("zones", [[camp["x"], camp["y"]]])
        new = [cx, cy] if [cx, cy] in self._grow_candidates(camp) else None
        if new is None:
            return self._grow_view(hero)
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

    # ------------------------------------------------------------------ guilds (D-97, provisional)

    def _guild_count(self, hero: Hero, amounts: dict[str, int]) -> None:
        """Add what the hero just did (explorations, victories, gathered resources) to its camp's guild (D-97).

        [ES]
        Qué hace: suma a los contadores del gremio de tu campamento lo que acabas de hacer. Solo cuenta lo que haces
        siendo miembro: el gremio es el de tu campamento de ahora. Como mucho una lectura y una escritura por orden.
        La llaman: _settle (cada exploración y lo recolectado) y _end_combat (cada victoria, también contra el Guardián).
        Si cambia, afecta: el ritmo de subida de todos los gremios. Las misiones contarán aquí cuando existan.
        """
        if not hero.camp or not any(n > 0 for n in amounts.values()):
            return
        guild = self.store.get("guild", hero.camp)
        if guild and guild_rules.count(guild, amounts):
            self.store.put("guild", hero.camp, guild)

    def _ago(self, seen_at: float) -> str:
        """'activo hace 5 min' from the last button press (Hero.seen_at, D-93); 0 means no data."""
        t = self.texts
        if not seen_at:
            return t.t("guild.ago.never")
        elapsed = max(0.0, self.clock.now() - seen_at)
        if elapsed < 60:
            return t.t("guild.ago.now")
        if elapsed < 3600:
            return t.t("guild.ago.minutes", n=int(elapsed // 60))
        if elapsed < 86400:
            return t.t("guild.ago.hours", n=int(elapsed // 3600))
        return t.t("guild.ago.days", n=int(elapsed // 86400))

    def _member_lines(self, hero: Hero, camp: dict[str, Any]) -> list[str]:
        """One line per camp member: name, level and when they last played (founder first, then the most recent).

        [ES]
        Qué hace: lista a los miembros con su nivel y "activo hace X". Sirve para ver quién juega a las mismas
        horas (el dueño lo dejó como comentario: no hay reglas que lo usen, D-97).
        La llama: _guild_view.
        Si cambia, afecta: solo lo que se muestra.
        """
        t = self.texts
        rows = []
        for member in camp["members"]:
            if member == hero.id:
                name, level, seen = hero.name, hero.level, hero.seen_at        # fresher than the stored copy
            else:
                data = self.store.get("hero", member) or {}
                name, level, seen = data.get("name", "?"), data.get("level", 1), data.get("seen_at", 0.0)
            rows.append((member == camp.get("founder_id"), seen, name, level))
        rows.sort(key=lambda r: (not r[0], -r[1]))
        return [t.t("guild.member_line", name=name, level=level, crown=t.t("guild.crown") if founder else "", ago=self._ago(seen))
                for founder, seen, name, level in rows]

    def _guild_view(self, hero: Hero, notice: str | None = None) -> View:
        """🛡️ Gremio: your camp's guild (or how to create it), its members and what it needs to rise (D-97).

        [ES]
        Qué hace: muestra el gremio de tu campamento: nombre, nivel, miembros (con nivel y "activo hace X") y el avance
        de lo que pide su nivel, con barras como la obra del Claro. Sin gremio, explica qué es y cuánto cuesta.
        Botones (3 como máximo): 🛡️ Crear gremio (fundador, sin gremio) o ⬆️ Subir el gremio (cuando cumplen),
        ✏️ Renombrar campamento (fundador) o 🚪 Salir del campamento (miembros), y ↩️ Volver. Crear, subir, renombrar
        y salir solo aparecen estando en el campamento; desde otro lugar (/gremio) solo se mira.
        La llaman: el botón 🛡️ Gremio del campamento y el atajo /gremio.
        Si cambia, afecta: tests/test_guilds.py y el recorrido de botones (4 como máximo).
        """
        t = self.texts
        camp = self.store.get("camp", hero.camp) if hero.camp else None
        if not camp or hero.id not in camp["members"]:
            return self._main_view(hero, notice=t.t("guild.no_camp"))
        cfg = self.content.balance["guild"]
        levels = cfg["levels"]
        guild = self.store.get("guild", hero.camp)
        here = (hero.x, hero.y) == (camp["x"], camp["y"])
        founder = camp.get("founder_id") == hero.id
        n, cap = len(camp["members"]), self._members_cap(camp)
        actions = []
        if guild is None:
            body = [t.t("guild.none", camp=camp["name"]), t.t("guild.what"),
                    t.t("guild.castle_hint", level=cfg["castle_min_level"], members=cfg["castle_min_members"]),
                    t.t("guild.cap_warning", cap=guild_rules.capacity(levels, 1)),
                    t.t("guild.found_cost", coins=self._money(cfg["found_coins"])) if founder else t.t("guild.only_founder", founder=camp["founder"]),
                    "", t.t("camps.members_cap", n=n, cap=cap)]
            body += self._member_lines(hero, camp)
            if founder and here:
                actions.append(Action(id="guildnew", label=t.t("guild.found_button")))
        else:
            body = [t.t("guild.header", name=guild["name"], level=guild["level"]), t.t("guild.camp_line", camp=camp["name"]),
                    "", t.t("guild.members", n=n, cap=cap)]
            body += self._member_lines(hero, camp) + [""]
            need = guild_rules.needs(levels, guild["level"])
            if need:
                body.append(t.t("guild.needs_title", next=guild["level"] + 1, cap=guild_rules.capacity(levels, guild["level"] + 1)))
                progress = guild.get("progress", {})
                order = list(guild_rules.COUNTERS)
                for k in sorted(need, key=lambda c: order.index(c) if c in order else len(order)):
                    have = min(need[k], progress.get(k, 0))
                    body.append(t.t("guild.need_line", label=t.t(f"guild.counter.{k}"), have=have, need=need[k], bar=self._bar(have, need[k], 8)))
                body.append(t.t("guild.how"))
                if guild_rules.can_rise(guild, levels):
                    body.append(t.t("guild.ready" if here else "guild.ready_away"))
                    if here:
                        actions.append(Action(id="guildup", label=t.t("guild.up_button")))
            else:
                body.append(t.t("guild.top"))
        if here:
            actions.append(Action(id="rename", label=t.t("guild.rename_camp")) if founder
                           else Action(id="leave", label=t.t("camps.leave_button")))
        actions.append(Action(id="claro" if here else "home", label=t.t("menu.back")))
        return View(kind="guild", title=t.t("guild.title"), body=body, actions=actions, notice=notice)

    def _can_found_guild(self, hero: Hero) -> bool:
        """The founder, standing at its camp, which has no guild yet (D-97)."""
        key = f"{hero.x}:{hero.y}"
        camp = self.store.get("camp", key)
        return bool(camp) and camp.get("founder_id") == hero.id and hero.camp == key and not self.store.get("guild", key)

    def _ask_guild_name(self, hero: Hero) -> View:
        """🛡️ Crear gremio: check the rules and the fee, then the next text the founder writes is the guild's name."""
        t = self.texts
        cfg = self.content.balance["guild"]
        if not self._can_found_guild(hero):
            return self._guild_view(hero, notice=t.t("guild.cannot"))
        if hero.gold < cfg["found_coins"]:
            return self._guild_view(hero, notice=t.t("guild.no_coins", coins=self._money(cfg["found_coins"])))
        self.store.put("camp_naming", hero.id, {"mode": "guild", "x": hero.x, "y": hero.y})
        return View(kind="name_guild", title=t.t("guild.title"), body=[t.t("guild.ask_name")], expects_text=True,
                    actions=[Action(id="guild", label=t.t("guild.cancel"))])

    def _name_guild(self, hero: Hero, name: str, pending: dict[str, Any]) -> View:
        """The founder wrote a guild name: same rules as camp names, unique among guilds (store "guild_name")."""
        t = self.texts

        def again(key: str) -> View:
            return View(kind="name_guild", title=t.t("guild.title"), body=[t.t(key), t.t("guild.ask_name")], expects_text=True,
                        actions=[Action(id="guild", label=t.t("guild.cancel"))])

        if (pending["x"], pending["y"]) != (hero.x, hero.y):
            self.store.delete("camp_naming", hero.id)
            return self._guild_view(hero)
        if not CAMP_NAME_RE.match(name):
            return again("guild.bad_name")
        if self.store.get("guild_name", self._name_key(name)):
            return again("guild.name_taken")
        self.store.delete("camp_naming", hero.id)
        return self._found_guild(hero, name)

    def _found_guild(self, hero: Hero, name: str) -> View:
        """Create the guild of the founder's camp: pay guild.found_coins, level 1, counters at 0; tell the members.

        [ES]
        Qué hace: crea el gremio del campamento (uno por campamento, vive con él: clave "x:y"). Desde ahora el cupo
        del campamento es el del gremio y lo que hacen sus miembros cuenta para subirlo.
        La llama: _name_guild, cuando el fundador escribe un nombre libre.
        Si cambia, afecta: el cupo del campamento, el castillo y el nombre único de los gremios.
        """
        t = self.texts
        cfg = self.content.balance["guild"]
        if not self._can_found_guild(hero):
            return self._guild_view(hero, notice=t.t("guild.cannot"))
        if hero.gold < cfg["found_coins"]:
            return self._guild_view(hero, notice=t.t("guild.no_coins", coins=self._money(cfg["found_coins"])))
        key = hero.camp
        camp = self.store.get("camp", key)
        hero.gold -= cfg["found_coins"]
        self.store.put("guild_name", self._name_key(name), {"camp": key})
        self.store.put("guild", key, {"name": name, "camp": key, "founder_id": hero.id, "level": 1,
                                       "progress": {k: 0 for k in guild_rules.COUNTERS}, "created": self.clock.now()})
        news = View(kind="guild_news", title=t.t("guild.founded_title"),
                    body=[t.t("guild.founded_push", founder=hero.name, name=name, camp=camp["name"])])
        for member in camp["members"]:
            if member != hero.id:
                self._push(member, news)
        return self._guild_view(hero, notice=t.t("guild.founded", name=name))

    def _rise_guild(self, hero: Hero) -> View:
        """⬆️ Subir el gremio: any member at the camp, once the counters cover the level's needs; tell the others."""
        t = self.texts
        key = f"{hero.x}:{hero.y}"
        camp = self.store.get("camp", key)
        guild = self.store.get("guild", key)
        if not camp or not guild or hero.id not in camp["members"]:
            return self._guild_view(hero)
        levels = self.content.balance["guild"]["levels"]
        if not guild_rules.rise(guild, levels):
            return self._guild_view(hero, notice=t.t("guild.not_ready"))
        self.store.put("guild", key, guild)
        text = t.t("guild.risen", name=guild["name"], level=guild["level"], cap=guild_rules.capacity(levels, guild["level"]))
        for member in camp["members"]:
            if member != hero.id:
                self._push(member, View(kind="guild_news", title=t.t("guild.risen_title"), body=[text]))
        return self._guild_view(hero, notice=text)

    def _castle_needs(self, camp: dict[str, Any]) -> list[tuple[str, bool]]:
        """What becoming a castle asks of the camp's guild (D-97); empty unless the next level is the castle.

        [ES]
        Qué hace: dice qué le falta al gremio para que el campamento pase a castillo (nivel 8 → 9): tener gremio,
        de nivel guild.castle_min_level o más, con guild.castle_min_members miembros o más. Vacío en cualquier
        otro nivel: después del castillo el campamento sigue creciendo sin pedir nada más.
        La llaman: _grow_view (lo muestra) y _grow_camp (lo exige).
        Si cambia, afecta: quién llega a castillo; los campamentos sin gremio se quedan en ciudad.
        """
        t = self.texts
        cfg = self.content.balance["guild"]
        castle = next((s["from_level"] for s in self.content.balance["camps"]["stages"] if s["id"] == "castillo"), None)
        if castle is None or camp.get("level", 1) + 1 != castle:
            return []
        guild = self.store.get("guild", f"{camp['x']}:{camp['y']}")
        n = len(camp["members"])
        level_line = (t.t("guild.castle_level", need=cfg["castle_min_level"], level=guild["level"]) if guild
                      else t.t("guild.castle_level_none", need=cfg["castle_min_level"]))
        return [(t.t("guild.castle_has_guild"), guild is not None),
                (level_line, bool(guild) and guild["level"] >= cfg["castle_min_level"]),
                (t.t("guild.castle_members", need=cfg["castle_min_members"], n=n), n >= cfg["castle_min_members"])]

    def _talents_view(self, hero: Hero, notice: str | None = None) -> View:
        t = self.texts
        group = self.content.classes[hero.class_id].get("group", hero.class_id)
        body = [t.t("talents.intro"), t.t("talents.points", n=hero.points), ""]
        if not hero.talents:
            body[:0] = [t.t("talents.choose_first"), ""]
        body.append(t.t("dual.link_on" if hero.dual_unlocked else "dual.link", n=hero.profile))
        actions = []
        for spec in specs_of(self.content.classes, group):
            sdef = self.content.classes[spec]
            pts = hero.talents.get(spec, 0)
            mark = " ⭐" if spec == hero.class_id and pts else ""
            body.append(t.t("talents.spec_line", name=t.t(sdef["name_key"]), role=t.t("role." + sdef.get("role", "ataque")), n=pts) + mark)
            actions.append(Action(id=f"tal:{spec}", label=t.t(sdef["name_key"])))
        body += ["", t.t("talents.bar_line", abilities=self._bar_names(hero))]
        # D-75: at most 4 buttons. The bar goes first; "back" only fits when the class has fewer than 3 specs
        # (the fixed menu 👤 Héroe always takes the player back).
        actions.append(Action(id="hero", label=t.t("menu.back")))        # the combat bar lives in each spec (D-86)
        return View(kind="talents", title=t.t("talents.title"), body=body, actions=actions, notice=notice)

    def _bar_names(self, hero: Hero) -> str:
        return ", ".join(self.texts.t(f"ability.{a}.name") for a in bar_slots(self.content.classes, hero)) or "—"

    def _class_abilities(self, hero: Hero) -> dict[str, tuple[dict[str, Any], str]]:
        """Every ability of the hero's class: id -> (ability, resource of its spec)."""
        group = self.content.classes[hero.class_id].get("group", hero.class_id)
        out = {}
        for spec in specs_of(self.content.classes, group):
            for ability in self.content.classes[spec]["abilities"]:
                out[ability["id"]] = (ability, self.content.classes[spec]["resource"])
        return out

    def _bar_view(self, hero: Hero, notice: str | None = None) -> View:
        """Combat bar (D-79): 3 slots; slot 1 is a response, slots 2 and 3 any other unlocked ability."""
        t = self.texts
        abilities = self._class_abilities(hero)
        slots = bar_slots(self.content.classes, hero)
        body = [t.t("bar.intro"), ""]
        for index in range(3):
            if index < len(slots):
                ability, resource = abilities[slots[index]]
                body.append(t.t("bar.slot_line", n=index + 1, ability=self._ability_label(ability, resource),
                                effect=self._ability_effect(ability, resource)))
            else:
                body.append(t.t("bar.slot_empty", n=index + 1))
        body += ["", t.t("bar.custom" if hero.bar else "bar.auto")]
        actions = [Action(id=f"barslot:{index + 1}", label=t.t("bar.slot_button", n=index + 1))
                   for index in range(min(3, max(1, len(slots))))]
        actions.append(Action(id="talents", label=t.t("menu.back")))
        return View(kind="bar", title=t.t("bar.title"), body=body, actions=actions, notice=notice)

    def _bar_slot_view(self, hero: Hero, slot: int, page: int = 0) -> View:
        """Pick what goes in one slot: unlocked abilities, a short line each, 4 buttons at most (D-75)."""
        t = self.texts
        if not 1 <= slot <= 3:
            return self._bar_view(hero)
        abilities = self._class_abilities(hero)
        slots = bar_slots(self.content.classes, hero)
        choices = bar_choices(self.content.classes, hero, slot)
        current = slots[slot - 1] if slot <= len(slots) else None
        body = [t.t("bar.pick_title", n=slot), t.t("bar.pick_rule_1" if slot == 1 else "bar.pick_rule_other")]
        if current:
            ability, resource = abilities[current]
            body.append(t.t("bar.pick_current", ability=self._ability_label(ability, resource)))
        body.append("")
        if not choices:
            body.append(t.t("bar.no_choices"))
        per = 3 if len(choices) <= 3 else 2
        pages = max(1, (len(choices) + per - 1) // per)
        page %= pages
        shown = choices[page * per:(page + 1) * per]
        if pages > 1:
            body.append(t.t("bar.page", n=page + 1, total=pages))
        actions = []
        for ability_id in shown:
            ability, resource = abilities[ability_id]
            body.append(t.t("bar.choice_line", ability=self._ability_label(ability, resource), effect=self._ability_effect(ability, resource)))
            actions.append(Action(id=f"barset:{slot}:{ability_id}", label=self._ability_label(ability, resource)))
        if pages > 1:
            actions.append(Action(id=f"barslot:{slot}:{(page + 1) % pages}", label=t.t("bar.more")))
        actions.append(Action(id="bar", label=t.t("menu.back")))
        return View(kind="bar_slot", title=t.t("bar.title"), body=body, actions=actions)

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
        hero.bar = []
        return self._talents_view(hero, notice=t.t("talents.respec_done", cost=self._money(cost), n=hero.points))

    # ------------------------------------------------------------------ double specialization (D-88)

    def _dual_view(self, hero: Hero, notice: str | None = None) -> View:
        """Two talent setups: unlock the second after dedicating yourself to your spec, paying bags."""
        t = self.texts
        cfg = self.content.balance["talents"]["dual"]
        main_points = hero.talents.get(hero.class_id, 0)
        body = [t.t("dual.intro")]
        actions = []
        if not hero.dual_unlocked:
            ok_points = main_points >= cfg["min_points"]
            ok_bags = hero.bags >= cfg["cost_bags"]
            body += ["", ("✅ " if ok_points else "▫️ ") + t.t("dual.req_points", need=cfg["min_points"], n=main_points),
                     ("✅ " if ok_bags else "▫️ ") + t.t("dual.req_bags", need=cfg["cost_bags"], n=hero.bags)]
            if ok_points and ok_bags:
                actions.append(Action(id="dual_unlock", label=t.t("dual.unlock_button", n=cfg["cost_bags"])))
        else:
            other = 2 if hero.profile == 1 else 1
            saved = hero.profiles.get(str(other), {})
            other_name = t.t(self.content.classes[saved["class_id"]]["name_key"]) if saved.get("talents") else t.t("dual.empty")
            body += ["", t.t("dual.active", n=hero.profile, name=self._hero_title(hero)), t.t("dual.other", n=other, name=other_name)]
            actions.append(Action(id="dual_switch", label=t.t("dual.switch_button", n=other)))
        actions.append(Action(id="talents", label=t.t("menu.back")))
        return View(kind="dual", title=t.t("dual.title"), body=body, actions=actions, notice=notice)

    def _dual_unlock(self, hero: Hero) -> View:
        t = self.texts
        cfg = self.content.balance["talents"]["dual"]
        if hero.dual_unlocked or hero.talents.get(hero.class_id, 0) < cfg["min_points"] or hero.bags < cfg["cost_bags"]:
            return self._dual_view(hero)
        hero.bags -= cfg["cost_bags"]
        hero.dual_unlocked = True
        hero.profile = 1
        return self._dual_view(hero, notice=t.t("dual.unlocked", n=cfg["cost_bags"]))

    def _dual_switch(self, hero: Hero) -> View:
        """Swap to the other setup: each keeps its own points, abilities and bar (points come from your level)."""
        t = self.texts
        if not hero.dual_unlocked or hero.activity:
            return self._dual_view(hero, notice=t.t("activity.busy") if hero.activity else None)
        group = self.content.classes[hero.class_id].get("group", hero.class_id)
        hero.profiles[str(hero.profile)] = {"talents": dict(hero.talents), "unlocked": list(hero.unlocked),
                                            "class_id": hero.class_id, "bar": list(hero.bar)}
        hero.profile = 2 if hero.profile == 1 else 1
        saved = hero.profiles.get(str(hero.profile)) or {}
        hero.talents = dict(saved.get("talents", {}))
        hero.unlocked = list(saved.get("unlocked") or [base_response(self.content.classes, group)])
        hero.class_id = saved.get("class_id") or default_spec(self.content.classes, group)
        hero.bar = list(saved.get("bar", []))
        hero.points = max(0, hero.level - 1 - sum(hero.talents.values()))
        self._clamp_hp(hero)
        return self._dual_view(hero, notice=t.t("dual.switched", n=hero.profile))

    def _spec_view(self, hero: Hero, spec: str, notice: str | None = None) -> View:
        t = self.texts
        group = self.content.classes[hero.class_id].get("group", hero.class_id)
        if spec not in specs_of(self.content.classes, group):
            return self._talents_view(hero)
        sdef = self.content.classes[spec]
        pts = hero.talents.get(spec, 0)
        body = [t.t("talents.spec_title", name=t.t(sdef["name_key"]), role=t.t("role." + sdef.get("role", "ataque"))),
                t.t(sdef["role_key"]), t.t("talents.spec_points", n=pts, free=hero.points), ""]
        following = None
        for index, need in enumerate(unlock_points(self.content.balance)):
            if index >= len(sdef["abilities"]):
                break
            ability = sdef["abilities"][index]
            label, effect = self._ability_label(ability, sdef["resource"]), self._ability_effect(ability, sdef["resource"])
            if ability["id"] in hero.unlocked:
                body.append(t.t("talents.ability_open", ability=label, effect=effect))
            else:
                body.append(t.t("talents.ability_locked", need=need, ability=label, effect=effect))
                if following is None:
                    following = (ability, need)
        body += ["", t.t("talents.legend")]
        if following:
            body.append(t.t("talents.next_unlock", name=t.t(f"ability.{following[0]['id']}.name"), need=following[1],
                            left=max(0, following[1] - pts)))
        else:
            body.append(t.t("talents.all_unlocked"))
        actions = []
        if hero.points > 0:
            actions.append(Action(id=f"pt:{spec}", label=t.t("talents.spend_button")))
        if hero.talents:
            actions.append(Action(id="respec", label=t.t("talents.respec_button", cost=self._money(self._respec_cost(hero)))))
        actions.append(Action(id="bar", label=t.t("bar.button")))
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
        shown = places[:3]
        lair = next((p for p in places if self._is_lair(p[1], p[2])), None)
        if lair and lair not in shown:
            shown = shown[:2] + [lair]          # the Guardian's lair is always offered (D-82)
        body = [t.t("places.intro", n=len(hero.known))]
        actions = []
        for seconds, x, y in shown:
            zone = self._zone(x, y)
            mark = t.t("guardian.route_mark") if self._is_lair(x, y) else ""
            body.append(t.t("places.line", biome=self.content.biomes[zone.biome]["emoji"], name=self._zone_name(zone) + mark,
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
                elif self._is_lair(x, y) and (hero.remembers(x, y) or self._discovered(x, y) is not None):
                    row += "👑"
                elif hero.remembers(x, y) and self.store.get("camp", f"{x}:{y}"):
                    row += "🏕️"
                elif self._explored_pct(hero, x, y) >= 100:
                    row += self.content.balance["resources"]["colors"][main_resource(self._zone_resources(x, y))]
                elif hero.remembers(x, y):
                    row += self.content.biomes[self._zone(x, y).biome]["emoji"]
                elif self._discovered(x, y) is not None:
                    row += "▪️"
                else:
                    row += "▫️"
            rows.append(row)
        body = [t.t("map.legend"), t.t("map.colors")] + rows + ["", t.t("map.position", x=hero.x, y=hero.y, lejania=self._zone(hero.x, hero.y).lejania)]
        cfg = self._guardian_cfg()
        if cfg and self._discovered(cfg["x"], cfg["y"]) is not None:
            body.append(t.t("guardian.map_line", x=cfg["x"], y=cfg["y"], lejania=self._zone(cfg["x"], cfg["y"]).lejania))
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
            *([t.t("guardian.titles_line", titles=", ".join(t.t(f"guardian.title.{x}") for x in hero.titles))] if hero.titles else []),
            t.t("hero.level_pct", level=hero.level, pct=f"{pct:.2f}"),
            t.t("hero.xp_line", xp=hero.xp, next=high),
            t.t("hero.hp_line", hp=hero.hp, max_hp=stats["max_hp"]),
            *self._recovery_lines(hero, stats["max_hp"]),
            t.t("hero.stats_link"),
            t.t("hero.atk_def", attack=round(stats["attack"], 1), armor=round(stats["armor"] * 100)),
            t.t("hero.energy_line", energy=hero.energy, max_energy=self.content.balance["energy"]["max"]),
            t.t("hero.resource_line", resource=t.t(f"resource.{cdef['resource']}"), max=cdef.get("resource_max", 100)),
            self._coins_line(hero),
            t.t("hero.inv_link", n=self._bag_used(hero), cap=self._bag_cap()),     # same count as "space in the backpack" (D-87)
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
        actions = [Action(id="gear:0", label=t.t("gear.equip_menu_new" if hero.gear_new else "gear.equip_menu"))]
        if self._has_memento(hero):
            actions.append(Action(id="memento", label=t.t("guardian.memento_button")))
        actions.append(Action(id="bag", label=t.t("menu.back")))
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

    # ------------------------------------------------------------------ the region Guardian (D-82)

    def _guardian_cfg(self) -> dict[str, Any] | None:
        """balance.yaml "guardian" if its enemy exists, else None (the game works without a Guardian)."""
        cfg = self.content.balance.get("guardian")
        return cfg if cfg and cfg.get("enemy") in self.content.enemies else None

    def _is_lair(self, x: int, y: int) -> bool:
        cfg = self._guardian_cfg()
        return bool(cfg) and (x, y) == (cfg["x"], cfg["y"])

    def _guardian_name(self) -> str:
        cfg = self._guardian_cfg()
        return self.texts.t(self.content.enemies[cfg["enemy"]]["name_key"]) if cfg else ""

    def _pioneer(self) -> dict[str, Any] | None:
        """The first hero of the server who beat the Guardian, saved for ever in "meta"."""
        cfg = self._guardian_cfg()
        return self.store.get("meta", f"guardian:{cfg['enemy']}") if cfg else None

    def _lair_lines(self, zone: Zone) -> list[str]:
        """Zone screen lines of the lair: who lives here and who beat it first."""
        if not self._is_lair(zone.x, zone.y):
            return []
        t = self.texts
        cfg = self._guardian_cfg()
        edef = self.content.enemies[cfg["enemy"]]
        pioneer = self._pioneer()
        return [t.t("guardian.zone_line", name=self._guardian_name(), level=edef["level_min"]),
                t.t("guardian.pioneer_line", name=pioneer["name"]) if pioneer else t.t("guardian.nobody_yet")]

    def _guardian_wait(self, hero: Hero) -> float:
        """Seconds until this hero may challenge the Guardian again (0 = now)."""
        cfg = self._guardian_cfg()
        record = hero.guardians.get(cfg["enemy"], {}) if cfg else {}
        if not record.get("last"):
            return 0.0
        ready = record["last"] + cfg["cooldown_hours"] * 3600 * self.time_scale
        return max(0.0, ready - self.clock.now())

    def _guardian_ready_line(self, hero: Hero) -> str:
        wait = self._guardian_wait(hero)
        if wait > 0:
            return self.texts.t("guardian.wait", name=self._guardian_name(), time=self._fmt_duration(wait))
        return self.texts.t("guardian.ready")

    def _challenge_guardian(self, hero: Hero) -> View:
        """Start the fight against the Guardian: only in its lair, idle, and after the hero's wait.

        [ES]
        Qué hace: empieza la pelea contra el Guardián (botón ⚔️ Desafiar al Guardián). No gasta energía
        (el combate no la usa, D-78); el Guardián tiene nivel fijo y no se puede huir.
        La llama: _idle_action con la acción "boss".
        Si cambia, afecta: tests/test_boss.py y la tabla del simulador (jefes.md §6).
        """
        t = self.texts
        cfg = self._guardian_cfg()
        if not cfg or not self._is_lair(hero.x, hero.y):
            return self._zone_view(hero, notice=t.t("guardian.not_here"))
        wait = self._guardian_wait(hero)
        if wait > 0:
            return self._explore_menu(hero, notice=t.t("guardian.wait", name=self._guardian_name(), time=self._fmt_duration(wait)))
        edef = self.content.enemies[cfg["enemy"]]
        seed = int(hash_unit(self.world_seed, hero.id, "guardian", self.clock.now()) * 2**31)
        state = make_combat(cfg["enemy"], edef, edef["level_min"], self._kit(hero), seed)
        self.store.put("combat", hero.id, state)
        self.bus.publish(CombatStarted(hero.id, cfg["enemy"], seed))
        return self._combat_view(hero, state, notice=t.t("guardian.started", name=self._guardian_name()))

    def _guardian_rewards(self, hero: Hero, state: dict[str, Any], rng: Rng) -> list[str]:
        """Victory against the Guardian: xp always; the first win gives the Memento, later wins coins and
        a chance of normal loot; the first hero of the server becomes Pioneer and everyone is told (once).

        [ES]
        Qué hace: paga la victoria contra el Guardián. Primera victoria del héroe: el Recuerdo garantizado.
        Siguientes: monedas (en bronce, enemies.yaml gold) y balance.yaml guardian.repeat_gear_chance de botín.
        Primer vencedor del servidor: queda en "meta" para siempre, gana el título y se avisa a todos por _push.
        La llama: _end_combat cuando el enemigo vencido tiene boss: true.
        Si cambia, afecta: la economía (monedas y equipo que entran), los títulos y los avisos a todos.
        """
        t = self.texts
        cfg = self._guardian_cfg()
        enemy = state["enemy"]
        edef = self.content.enemies[enemy["id"]]
        record = dict(hero.guardians.get(enemy["id"], {}))
        first_win = not record.get("wins")
        record["wins"] = record.get("wins", 0) + 1
        record["last"] = self.clock.now()
        hero.guardians[enemy["id"]] = record
        hero.kills += 1
        xp = int(edef["xp"] * (1 + 0.15 * (enemy["level"] - 1)) * self._xp_mult(hero))
        hero.xp += xp
        lines: list[str] = []
        if first_win:
            memento = next((iid for iid, it in self.content.items.items()
                            if it.get("kind") == "memento" and it.get("memento_of") == enemy["id"]), None)
            lines.append(t.t("guardian.rewards_first", xp=xp))
            if memento:
                hero.backpack[memento] = hero.backpack.get(memento, 0) + 1
                item = self.content.items[memento]
                lines.append(t.t("guardian.first_win", item=f"{item['emoji']} {t.t(item['name_key'])}"))
        else:
            low, high = edef.get("gold", [1, 3])
            gold = int(rng.uniform(low, high + 1))
            hero.gold += gold
            lines.append(t.t("combat.rewards", xp=xp, gold=self._money(gold)))
            dropped = roll_gear(self.content.items, self.content.classes, self.content.balance, hero, enemy["level"], rng,
                                chance=cfg["repeat_gear_chance"])
            if dropped:
                hero.backpack[dropped] = hero.backpack.get(dropped, 0) + 1
                lines.append(self._loot_line(hero, dropped))
        for item_id, chance in edef.get("loot", {}).items():
            if item_id in self.content.items and rng.chance(chance):
                hero.backpack[item_id] = hero.backpack.get(item_id, 0) + 1
                item = self.content.items[item_id]
                lines.append(t.t("combat.loot", item=f"{item['emoji']} {t.t(item['name_key'])}"))
        first_in_server = self._pioneer() is None
        if first_in_server:
            self.store.put("meta", f"guardian:{enemy['id']}", {"name": hero.name, "hero_id": hero.id, "at": self.clock.now()})
            title = f"pionero_{enemy['id']}"
            if title not in hero.titles:
                hero.titles.append(title)
            lines.append(t.t("guardian.pioneer_title", title=t.t(f"guardian.title.{title}")))
            news = View(kind="news", title=t.t("guardian.news_title"),
                        body=[t.t("guardian.news_body", hero=hero.name, boss=self._guardian_name(),
                                  title=t.t(f"guardian.title.{title}"))])
            for account_id in self.players():
                if account_id != hero.id:
                    self._push(account_id, news)
        lines.append(t.t("guardian.again_in", name=self._guardian_name(),
                         time=self._fmt_duration(cfg["cooldown_hours"] * 3600 * self.time_scale)))
        self.bus.publish(BossDefeated(hero.id, enemy["id"], first_win, first_in_server))
        return lines

    def _has_memento(self, hero: Hero) -> bool:
        return any(self.content.items.get(i, {}).get("kind") == "memento" and n > 0 for i, n in hero.backpack.items())

    def _memento_view(self, hero: Hero, notice: str | None = None) -> View:
        """The Memento: choose ONE of two unique pieces made for you (weapon or armor); the other is lost."""
        t = self.texts
        memento = next((i for i, n in hero.backpack.items() if n > 0 and self.content.items.get(i, {}).get("kind") == "memento"), None)
        if not memento:
            return self._bag_view(hero) if notice is None else self._main_view(hero, notice=notice)
        cfg = self._guardian_cfg() or {}
        options = source_choices(self.content.items, self.content.classes, self.content.balance, hero,
                                 cfg.get("memento_source", "guardian"))
        body = [t.t("guardian.memento_intro"), ""]
        actions = []
        for item_id in options:
            item = self.content.items[item_id]
            body.append(t.t("guardian.memento_option", item=self._gear_name(item_id), slot=t.t(f"gear.slot.{item['slot']}"),
                            stats=self._gear_stats_text(item.get("stats", {})), level=item.get("req_level", 1)))
            actions.append(Action(id=f"mem:{item_id}", label=self._gear_name(item_id)))
        actions.append(Action(id="bag", label=t.t("menu.back")))
        title = t.t(self.content.items[memento]["name_key"])
        return View(kind="memento", title=f"{self.content.items[memento]['emoji']} {title}", body=body, actions=actions, notice=notice)

    def _use_memento(self, hero: Hero, item_id: str) -> View:
        """Trade the Memento for the chosen piece; it goes to the backpack (shown with its Equip button)."""
        t = self.texts
        memento = next((i for i, n in hero.backpack.items() if n > 0 and self.content.items.get(i, {}).get("kind") == "memento"), None)
        cfg = self._guardian_cfg() or {}
        options = source_choices(self.content.items, self.content.classes, self.content.balance, hero,
                                 cfg.get("memento_source", "guardian"))
        if not memento or item_id not in options:
            return self._memento_view(hero)
        hero.backpack[memento] -= 1
        if hero.backpack[memento] <= 0:
            del hero.backpack[memento]
        hero.backpack[item_id] = hero.backpack.get(item_id, 0) + 1
        return self._item_view(hero, item_id, notice=t.t("guardian.memento_done", item=self._gear_name(item_id)))

    # ------------------------------------------------------------------ combat

    def _start_combat(self, hero: Hero, zone: Zone, rng: Rng, reason_key: str) -> str:
        common = [(eid, e) for eid, e in self.content.enemies.items() if not e.get("boss") and not e.get("retired")]
        candidates = [(eid, e) for eid, e in common if zone.biome in e.get("biomes", [])]
        fitting = [(eid, e) for eid, e in candidates if e["level_min"] <= zone.level <= e["level_max"]]
        pool = fitting or candidates or common
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
        icon = {"strike": "✨", "finisher": "🗡️", "heal": "💚", "dot": "🩸", "interrupt": "✋", "empower": "💪",
                "expose": "🎯", "weaken": "🔻", "hot": "💖"}.get(ability["kind"], "✨")
        if ability["kind"] == "response":
            icon = {"block": "🛡", "dodge": "💨", "shield": "🫧"}.get(ability.get("response"), "🛡")
        name = t.t("ability." + ability["id"] + ".name")
        label = f"{icon} {name}"
        if ability.get("cost"):
            label += f" ({ability['cost']})"
        elif ability["kind"] == "response":
            label += f" (🔋{ability.get('stamina', 1)})"
        elif ability.get("gain"):
            label += f" (+{ability['gain']})"
        return label

    @staticmethod
    def _num(value: float) -> str:
        """Short number for players: 1.3 -> "1,3", 2.0 -> "2"."""
        return f"{value:g}".replace(".", ",")

    def _ability_effect(self, ability: dict[str, Any], resource: str) -> str:
        """One short line of what an ability does, built from its numbers and the texts in ability_effect.*.

        [ES]
        Qué hace: explica en pocas palabras qué hace una habilidad (sale de sus números, así nunca miente).
        La llaman: las pantallas de especialización y de 🎛️ Barra de combate.
        Si cambia, afecta: solo lo que lee el jugador.
        """
        t = self.texts
        kind = ability["kind"]

        def pct(value: float) -> int:
            return round(value * 100)

        if kind == "response":
            text = t.t(f"ability_effect.{ability.get('response', 'block')}", pct=pct(ability.get("value", 0.0)))
        elif kind in ("strike", "interrupt"):
            text = t.t(f"ability_effect.{kind}", power=self._num(ability.get("power", 1.0)))
        elif kind == "finisher":
            text = t.t("ability_effect.finisher", power=self._num(ability.get("power", 1.0)), per=self._num(ability.get("per_combo", 0.0)))
        elif kind == "dot":
            text = t.t("ability_effect.dot", power=self._num(ability.get("power", 0.5)), rounds=ability.get("rounds", 3))
        elif kind == "heal":
            text = t.t("ability_effect.heal", pct=pct(ability.get("value", 0.0)))
        else:
            text = t.t(f"ability_effect.{kind}", pct=pct(ability.get("value", 0.2)), rounds=ability.get("rounds", 3))
        extras = []
        if ability.get("lifesteal"):
            extras.append(t.t("ability_effect.lifesteal", pct=pct(ability["lifesteal"])))
        if ability.get("combo"):
            extras.append(t.t("ability_effect.combo", n=ability["combo"]))
        if ability.get("gain"):
            extras.append(t.t("ability_effect.gain", n=ability["gain"], resource=t.t(f"resource.{resource}")))
        if kind == "response" and ability.get("stamina", 1) > 1:
            extras.append(t.t("ability_effect.stamina", n=ability["stamina"]))
        if ability.get("cooldown"):
            extras.append(t.t("ability_effect.cooldown", n=ability["cooldown"]))
        return " · ".join([text] + extras)

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
            *([t.t("combat.boss_phase", n=enemy.get("phase", 0) + 1, total=len(edef["phases"]) + 1)] if edef.get("phases") else []),
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
            busy = None if action_id in ("back", "home", "refresh") else t.t("combat.busy")   # menu buttons do nothing mid-fight: say why
            return self._combat_view(hero, state, notice=busy)
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
        actions = [Action(id="home", label=t.t("menu.continue"))]
        if outcome == "victory" and edef.get("boss"):
            lines += self._guardian_rewards(hero, state, rng)
            if self._has_memento(hero):
                actions.insert(0, Action(id="memento", label=t.t("guardian.memento_button")))
        elif outcome == "victory":
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
                    item = self.content.items[item_id]
                    low, high = item.get("loot_amount", [1, 1])      # D-93: 🍖 carne comes in 1-2
                    count = low if high <= low else min(high, int(rng.uniform(low, high + 1)))
                    hero.backpack[item_id] = hero.backpack.get(item_id, 0) + count
                    label = f"{item['emoji']} {t.t(item['name_key'])}" if count == 1 else self._item_list({item_id: count})
                    lines.append(t.t("combat.loot", item=label))
            dropped = roll_gear(self.content.items, self.content.classes, self.content.balance, hero, enemy["level"], rng)
            if dropped:
                hero.backpack[dropped] = hero.backpack.get(dropped, 0) + 1
                lines.append(self._loot_line(hero, dropped))
        if outcome == "victory":
            self._guild_count(hero, {"victories": 1})          # D-97: a win counts for the hero's guild
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
        return View(kind="combat_end", title=title, body=lines, actions=actions)

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
