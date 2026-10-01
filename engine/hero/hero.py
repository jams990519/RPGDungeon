"""Hero record and derived stats.

[ES]
Para qué sirve: guardar al héroe y calcular sus estadísticas según clase y nivel.
Documento de diseño: diseno/03-personaje/progresion.md; diseno/03-personaje/balance.md
Módulo: M2 Héroe
Depende de: content/classes.yaml, content/balance.yaml (hero.xp_curve)
Lo usan: engine/service/game.py, engine/combat/engine.py
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño: espacio "hero" del almacén (clave = id de cuenta)
Reglas que nunca se rompen:
    1. to_dict() y from_dict() van juntos: un campo nuevo necesita valor por defecto
       para que los héroes ya guardados sigan cargando.
Si cambias esto, revisa:
    - Almacén: héroes guardados en SQLite (campos nuevos con valor por defecto)
    - Números: classes.yaml base/per_level, balance.yaml hero.xp_curve y talents.passive (la Defensa suma armadura por punto, D-110)
    - seen_at (D-93): dice quién está activo y por lo tanto quién come de cada despensa
      (engine/service/game.py _mark_seen; tests/test_pantry.py)
    - chests (D-92, provisional): 🪎 cofres que se arman en el Claro y pagan el crecimiento de los campamentos
      grandes (engine/service/game.py _build_chest, _grow_chests; tests/test_backpack.py)
    - seen_at también dice quién aparece en la lista 👥 de 📍 Zona (D-96: tocó un botón en los últimos
      presence.minutes; engine/service/game.py _zone_players; tests/test_zone_players.py)
    - professions (D-109): experiencia de cada oficio (id de content/professions.yaml → experiencia); el rango sale
      de ahí (engine/professions/rules.py rank_of, balance.yaml professions.rank_formula). Vacío para los héroes
      guardados antes: empiezan todos los oficios en rango 1 (engine/service/game.py sección "professions";
      tests/test_professions.py). D-112: el 🧭 Explorador guarda aquí su experiencia con el id "explorador" (sube
      explorando; con el rango ve más en el mapa: engine/service/game.py sección "enemy camps"; tests/test_enemy_camps.py)
    - titles: también guarda "gran_explorador", el título del rango 100 del 🧭 Explorador (D-112, para siempre)
    - options (D-114): ⚙️ Opciones del jugador ("fights": "manual" | "auto", "retreat": % de vida, "potions": sí/no).
      Vacío = lo de balance.yaml auto_fight.defaults (también para los héroes guardados antes: ✋ Manual, 50 %, sí).
      Solo se guarda lo que el jugador cambia (engine/service/game.py _option, _options_view, _set_option;
      tests/test_options.py)
    - origin, story, factions, journal, bio (D-117, provisional): la historia y el rol. origin = id de origen de
      content/story.yaml (None = sin elegir: los héroes guardados antes lo eligen la primera vez que abren 👤 Héroe o
      📖 Historia, sin bloquear nada); story = misiones hechas, paso en curso, decisiones, encargos del día y premios
      cobrados; factions = reputación por facción; journal = entradas del 📔 Diario; bio = biografía de /bio. Todos
      vacíos por defecto, así los héroes viejos cargan igual (engine/service/story.py; tests/test_story.py)
    - Pruebas: tests/test_service.py
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class Hero:
    """A player's hero.

    Attributes:
        id: account id given by the client adapter (the engine does not parse it).
        name: hero name.
        class_id: id in content/classes.yaml.
        level, xp: progression.
        gold: ALL the hero's coins, counted in bronze (D-80: 100 bronze = 1 silver, 100 silver = 1 gold).
        bags: sewn bags (a currency made in the Claro); gems: bought diamonds (D-43, D-85).
        chests: 🪎 chests assembled in the Claro from 10 bags, wood and metal; they pay for growing
            big camps (D-92, provisional). 0 for heroes saved before it.
        dual_unlocked, profile, profiles: double specialization (D-88): two talent setups, the
            inactive one saved in profiles["1"|"2"] (talents, unlocked, class_id, bar).
        exploration: how well the hero knows each zone, "x:y" -> 0-100 % (D-87).
        cards: profession ID cards, shown to other players (D-85; earned with professions, still to come).
        xp_boost_until: end of the gem experience accelerator; banner: unique banner bought with gems.
        downed: fell in combat; health comes back much slower until full, a potion or the inn (D-83).
        gear_new: gear pieces not looked at yet (shown with 🆕 in the equipment screen).
        hp: current health (max is derived).
        x, y: zone coordinates on the infinite map; (0, 0) is the Claro.
        activity: None or {"kind": "travel"|"explore"|"gather"|"hunt"|"rest", "until": ts, ...} ("hunt": a hunting
            batch with automatic fights, D-114).
        belt, backpack: item id -> count.
        last_regen_at: timestamp of the last passive health regeneration.
        known: zones this hero has visited, as "x:y" (its own map memory, D-61).
        gear: worn pieces, slot -> item id (D-77); gear_started: starter gear already given.
        guardians: region Guardians fought, enemy id -> {"wins": n, "last": ts of the last win} (D-82).
        titles: title ids earned for ever, e.g. "pionero_raigambre" (first in the server to beat it).
        bar: combat bar chosen by the player, 3 ability ids, slot 1 = a response (D-79);
            empty means the automatic bar.
        seen_at: last time the player pressed a button (D-93); 0 for heroes saved before it.
            "Active" residents (they eat from the pantry) are those seen in the last 24 h.
            Players seen in the last presence.minutes are also listed in their zone (D-96).
        professions: profession xp, profession id (content/professions.yaml) -> xp (D-109). The rank (1-100)
            is derived from it; empty for heroes saved before it (every profession starts at rank 1). No cap (D-57).
        options: the player's ⚙️ Opciones (D-114): "fights" ("manual" or "auto": what happens when a fight comes up during
            a batch), "retreat" (auto fights: the batch stops below this % of life) and "potions" (auto fights may use
            the belt). Only what the player changed is saved; missing keys use balance.yaml auto_fight.defaults, so
            heroes saved before it load with ✋ Manual, 50 % and potions on.
        origin: origin id from content/story.yaml (D-117); None until chosen (heroes saved before it choose it the first
            time they open the hero sheet or 📖 Historia, never blocking play).
        story: story progress (D-117): "offered" (the origin choice was shown), "q" {quest id: {"s": step, "n": count}},
            "done" (quest ids), "c" {decision id: option}, "met" (characters talked to), "daily" {"day", "p", "done"},
            "ranks" {faction: highest rank index rewarded}, "g_at" (last gesture), "tasks" (daily tasks done), "jg"/"jt"
            (Guardians and titles already in the journal). Empty for heroes saved before it.
        factions: reputation points per faction id (D-117); missing = 0 (Desconocido).
        journal: 📔 Diario entries {"t": time, "k": text key, "v": values}, oldest first, capped (balance story.journal_max).
        bio: the short biography written with /bio (D-117); "" = none.

    [ES]
    Qué es: el héroe del jugador (en el diseño, "héroe").
    Quién la usa: el servicio lo crea, lo guarda y lo pasa al combate.
    Si cambia, afecta: los héroes guardados y todas las vistas.
    """

    id: str
    name: str
    class_id: str
    level: int = 1
    xp: int = 0
    gold: int = 0
    bags: int = 0
    chests: int = 0
    gems: int = 0
    hp: int = 1
    x: int = 0
    y: int = 0
    activity: dict[str, Any] | None = None
    belt: dict[str, int] = field(default_factory=dict)
    backpack: dict[str, int] = field(default_factory=dict)
    last_regen_at: float = 0.0
    kills: int = 0
    tutorial: int = 0
    energy: int = 20
    energy_at: float = 0.0
    invites: int = 0
    referred_by: str | None = None
    referral_paid: bool = False
    merit: int = 0
    talents: dict[str, int] = field(default_factory=dict)
    points: int = 0
    unlocked: list[str] = field(default_factory=list)
    explored: list[str] = field(default_factory=list)
    camp: str | None = None
    zones_discovered: int = 0
    known: list[str] = field(default_factory=lambda: ["0:0"])
    gear: dict[str, str] = field(default_factory=dict)
    gear_started: bool = False
    energy_version: int = 0
    xp_boost_until: float = 0.0
    banner: str | None = None
    downed: bool = False
    gear_new: list[str] = field(default_factory=list)
    cards: int = 0
    exploration: dict[str, int] = field(default_factory=dict)
    dual_unlocked: bool = False
    profile: int = 1
    profiles: dict[str, dict[str, Any]] = field(default_factory=dict)
    guardians: dict[str, dict[str, Any]] = field(default_factory=dict)
    titles: list[str] = field(default_factory=list)
    bar: list[str] = field(default_factory=list)
    seen_at: float = 0.0
    professions: dict[str, int] = field(default_factory=dict)
    options: dict[str, Any] = field(default_factory=dict)
    origin: str | None = None
    story: dict[str, Any] = field(default_factory=dict)
    factions: dict[str, int] = field(default_factory=dict)
    journal: list[dict[str, Any]] = field(default_factory=list)
    bio: str = ""

    def remembers(self, x: int, y: int) -> bool:
        """True if this hero has been in zone (x, y). [ES] Qué hace: dice si el héroe recuerda esa zona. La llaman: el servicio (mapa, rutas, lugares). Si cambia, afecta: qué ve cada héroe en su mapa."""
        return f"{x}:{y}" in self.known

    def remember(self, x: int, y: int) -> None:
        """Add zone (x, y) to the hero's memory. [ES] Qué hace: el héroe anota la zona en su memoria. La llaman: el servicio al llegar. Si cambia, afecta: el mapa personal."""
        key = f"{x}:{y}"
        if key not in self.known:
            self.known.append(key)

    def to_dict(self) -> dict[str, Any]:
        """Serialize for storage. [ES] Qué hace: lo convierte en datos guardables. La llaman: el servicio. Si cambia, afecta: el guardado."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Hero":
        """Load from storage, ignoring unknown fields. [ES] Qué hace: lo reconstruye desde lo guardado. La llaman: el servicio. Si cambia, afecta: la carga de héroes viejos."""
        known = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        return cls(**known)


def hero_stats(class_def: dict[str, Any], level: int) -> dict[str, float]:
    """Derived combat stats for a class at a level.

    Returns:
        dict with max_hp, attack, armor and initiative.

    [ES]
    Qué hace: calcula vida máxima, ataque, armadura e iniciativa, con los bonos de
    talentos (talent_bonus), de equipo (gear_bonus) y de oficios (perk_bonus, D-111) que trae el kit del servicio.
    La armadura suma la base, el equipo, los oficios y los talentos (D-110: los puntos de Defensa también dan
    armadura, balance.yaml talents.passive.defensa.armor), sin pasar armor_cap (60 %).
    La llaman: el servicio (vista del héroe) y el combate.
    Si cambia, afecta: el balance de todas las clases.
    """
    base = class_def["base"]
    per = class_def.get("per_level", {})
    bonus = class_def.get("talent_bonus", {})
    gear = class_def.get("gear_bonus", {})
    perk = class_def.get("perk_bonus", {})          # D-111: what the hero's professions add
    lv = max(1, level) - 1
    return {
        "max_hp": int((base["hp"] + per.get("hp", 0) * lv) * (1 + bonus.get("hp", 0.0)) * (1 + gear.get("hp", 0.0))
                      * (1 + perk.get("hp", 0.0))),
        "attack": float((base["attack"] + per.get("attack", 0) * lv) * (1 + bonus.get("attack", 0.0)) * (1 + gear.get("attack", 0.0))
                        * (1 + perk.get("attack", 0.0))),
        "armor": min(float(class_def.get("armor_cap", 0.6)), float(base.get("armor", 0.0)) + gear.get("armor", 0.0) + perk.get("armor", 0.0)
                     + bonus.get("armor", 0.0)),      # D-110: Defensa talent points also give armor
        "initiative": float(base.get("initiative", 10)),
    }


def xp_for_level(formula: dict[str, float], level: int) -> int:
    """Total xp needed to reach a level: base × (level − 1) ^ exponent. No level cap.

    [ES]
    Qué hace: dice cuánta experiencia total pide un nivel; crece rápido y no tiene tope (niveles infinitos).
    La llaman: el servicio al dar experiencia y en la vista del héroe.
    Si cambia, afecta: el ritmo de subida de nivel de todo el juego (balance.yaml hero.xp_formula).
    """
    if level <= 1:
        return 0
    return int(round(formula["base"] * (level - 1) ** formula["exponent"]))
