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
    - learned (0.33, D-257): los oficios que el héroe aprendió pagando su primera receta. Solo la 🧭 exploración no se
      aprende (learn: auto en content/professions.yaml; desde la 0.35, D-272, la 🪓 recolección también se aprende, y quien
      ya la practicaba la conserva: grandfather). Un oficio que no está aquí tiene rango 0:
      no se hace ninguna receta ni sube, pero la experiencia de antes queda en professions y vuelve al aprenderlo
      (engine/service/game.py _knows, _learn; tests/test_aprender_oficios.py)
    - prof_specs y spec_xp (D-115, D-141): las 🎓 especializaciones de oficio (id de oficio → ids de especialización de
      content/professions.yaml "specs", en el orden elegido: la 1.ª desde el rango 25, la 2.ª desde el 75, nunca tres) y el
      dominio de cada una (id de especialización → experiencia de oficio ganada mientras la tenía). El dominio de una
      especialización que se cambia queda guardado por si vuelve. Vacíos por defecto: los héroes guardados antes cargan
      igual (engine/service/game.py sección "profession specializations"; tests/test_especializaciones.py)
    - prof_titles (D-306.1, 0.43): el 🎖️ título de oficio que el héroe COMPRÓ en el 🧑‍🏫 Entrenador (id de oficio → id de título
      de content/professions.yaml "ranks": oficial, experto, artesano, maestro, gran_maestro). Vacío por defecto: los héroes
      guardados antes cargan igual y tienen gratis los títulos hasta su rango (D-64: el título que vale es el mayor entre el
      comprado y el que da su rango; engine/professions/rules.py held_title_index). Al tope del título (20, 40, 60, 80, 95)
      el oficio no guarda experiencia hasta comprar el siguiente (engine/service/game.py _prof_gain, _buy_title;
      tests/test_titulos_de_oficio.py)
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
    - gear_signatures (D-116): la firma de cada ✒️ obra maestra que lleva el héroe (id de la pieza "<id>_obra" → nombre
      de quien la fabricó). Vacío por defecto: los héroes guardados antes cargan igual. Hoy solo firma uno mismo (no hay
      mercado entre jugadores); cuando exista, la firma tiene que viajar con la pieza (engine/service/game.py _make,
      _masterwork_note, _sell_gear; tests/test_masterwork.py)
    - gear_enchants (D-115, fase 2): el ✨ encantamiento de cada pieza (id de la pieza → {"id": filo | vigor | guarda, "value":
      el bono que quedó al encantar}). Vacío por defecto: los héroes guardados antes cargan igual. engine/hero/gear.py lo suma a
      lo que da la pieza (real_stats, gear_bonus); se borra con la última copia de la pieza (engine/service/game.py
      _forget_piece, al vender o desencantar; tests/test_oficios_equipo.py)
    - guide (D-190, D-193, provisional): el avance del 🧭 camino guiado ({"v": versión, "done": ids de pasos de
      content/guide.yaml, "tips": ids de los avisos ya mostrados, "away": zonas pisadas fuera del Claro después del camino
      básico}). Vacío por defecto: los héroes de antes cargan igual y engine/service/guide.py los pone al día la primera vez
      (E-133: con el tutorial viejo terminado o nivel 5+, el camino básico queda hecho sin premio). tutorial (el índice del
      tutorial viejo) se sigue leyendo para eso y ya no avanza: no se borra (tests/test_camino_guiado.py)
    - combo_shapes (0.31, D-229): los combos distintos de la cadena que el héroe cobró alguna vez; solo cuentan para la
      variedad si balance.yaml chain.variety.scope es "permanent" (pendiente 5 del parche). Vacío por defecto: los héroes
      guardados antes cargan igual (engine/combat/chain_round.py; tests/test_cadena.py)
    - recipe_books y books_checked (0.44, D-306): los 📚 libros de recetas que el héroe compró en el 🧑‍🏫 Entrenador
      ("<oficio>:<rango>", por ejemplo "herreria:25"; una receta de rango 25 o más pide los libros de su oficio hasta su rango)
      y si ya se le regalaron los libros de los rangos que tenía al llegar la 0.44 (D-64: quien ya practicaba conserva lo que
      podía hacer). Vacío y False por defecto: la primera carga de un héroe de antes le da sus libros y lo marca
      (engine/service/game.py _load, _grant_old_books, sección "recipe tiers, colors and books"; tests/test_tramos_de_recetas.py)
    - book_gifts (0.52, D-328): los regalos de libros de recetas que ya recibió el héroe (ids de balance.yaml
      recipe_tiers.book_gifts, "0.52"): la 0.52 dio tramos al refinado, a la ⚗️ Alquimia y a la 🩺 Medicina y con ellos libros
      que esos oficios no pedían; quien ya tenía el rango los recibe gratis una vez (D-64). Vacío por defecto: la primera
      carga de un héroe de antes le da sus libros y lo llena; un héroe nuevo nace con todos (engine/service/game.py _load,
      _grant_book_gifts; tests/test_tramos_refinado_alquimia_medicina_cocina.py)
    - map_scrolls y charted (0.50, D-311 parte 5 y D-326): los 🗺️ pergaminos de mapa que el héroe lleva, uno por copia
      ({"id": "p7", "by": autor, "center": [x, y], "size": 6, "zones": ["x:y", …], "at": hora}; la mochila solo cuenta
      cuántos hay con el id balance.yaml map_scroll.item) y las zonas que ve a color para siempre porque usó un pergamino
      ("x:y"). charted solo pinta el 🗺️ Mapa y suma su terreno a la leyenda: no da recursos, ni nodos, ni lugares, ni
      "Moverte allá" (eso sigue con exploration y known). Vacíos por defecto: los héroes guardados antes cargan igual
      (engine/service/map_scroll.py; engine/service/game.py _fog_cell, _known_terrains, _fog_notices y _zone_view;
      engine/service/market.py; tests/test_pergamino_mapa.py)
    - hybrid (0.54, D-312 y D-330): lo que cambió el 🔀 modo híbrido del nivel 10, por pareja de roles ("<rol activo>><rol
      que presta>", por ejemplo "guerrero_tanque>guerrero_dps" → ["H2"]): los botones de rol (H1, H2, H3) que llevan la
      habilidad del mismo puesto del otro rol. Cada rol guarda la suya al cambiar de rol. Vacío por defecto: los héroes
      guardados antes y quien nunca lo toca pelean con la barra de su rol, igual que antes (engine/classes/talents.py
      hybrid_choice, toggle_hybrid, chain_bar; engine/service/game.py _hybrid_view; tests/test_modo_hibrido.py)
    - gear_wear y bag_wear (0.57, D-139 y D-333): la durabilidad del equipo. gear_wear: ranura -> registro de la pieza puesta
      ({"id": la pieza, "cur": durabilidad, "max": máximo, "rep": reparaciones hechas}); bag_wear: id de pieza -> registros de
      las copias USADAS de la mochila (las que no tienen registro están nuevas). Vacíos por defecto: los héroes guardados antes
      cargan con todo su equipo lleno (D-64). Las cuentas son de engine/hero/durability.py; los mueven equip y unequip
      (engine/hero/gear.py), el final de cada pelea y las reparaciones (engine/service/repair.py), _forget_piece (game.py) y
      la durabilidad que viaja en el 🏛️ Mercado y la ⚔️ Armería (market.py, gremio.py; tests/test_desgaste_reparacion.py)
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
        learned: the professions the hero learned by paying their first recipe (0.33, D-257). Only exploration is never
            learned (learn: auto; gathering too until 0.35, D-272). A profession not learned has rank 0; its xp stays.
        prof_titles: the 🎖️ profession title the hero BOUGHT at the 🧑‍🏫 Entrenador (0.43, D-306.1), profession id -> title id
            of content/professions.yaml "ranks". The title that counts is the higher of this and the one the rank already
            gives (heroes saved before it keep their titles for free, D-64). Empty for heroes saved before it.
        class_changes: how many times the hero changed class (0.35, D-270): the first is free, then the price grows
            (balance.yaml class_change.prices). 0 for heroes saved before it.
        home: the bonfire where the hero was born (0.37, D-265): one of the 9; heroes from before have [0, 0] (the Claro)
        prof_specs: the 🎓 specializations the hero holds (D-115, D-141), profession id -> spec ids in the order chosen (the
            first from rank 25, the second from rank 75; never three). Empty for heroes saved before it.
        spec_xp: mastery of each specialization, spec id -> profession xp earned in its profession while holding it. Kept
            when the specialization is switched away (coming back resumes it). Empty for heroes saved before it.
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
        gear_signatures: who made each ✒️ masterwork the hero holds (D-116), "<piece>_obra" -> crafter's hero name.
            Empty for heroes saved before it. All copies of one masterwork id share one signature: fine while only the
            crafter holds its own masterworks; a player market will need the signature to travel with each piece.
        gear_enchants: the ✨ enchantment on each gear piece the hero holds (D-115, phase 2), item id -> {"id": enchant id
            from balance.yaml enchanting.enchants, "value": its bonus, fixed when it was made}. Empty for heroes saved before
            it. Like gear_signatures, all copies of one item id share it; it goes away with the last copy.
        tutorial: index of the old tutorial (before D-193); it no longer advances, only read to skip the guided path of
            heroes who finished it (E-133).
        guide: progress of the guided path (D-190, D-193): "v" (record version), "done" (step ids of content/guide.yaml),
            "tips" (one-time tip ids already shown), "away" (zones stepped on outside the Claro after the basic path).
            Empty for heroes saved before it: engine/service/guide.py fills it the first time it is read.
        combo_shapes: the different chain combos (0.31, D-229) the hero ever cashed with a spender, e.g. "B-H2-H1-H3". Only
            used when balance.yaml chain.variety.scope is "permanent" (the variety bonus then lasts for ever, not one fight).
            Empty for heroes saved before it.
        recipe_books: the 📚 recipe books the hero owns (D-306, 0.44), as "<profession>:<rank>" (e.g. "herreria:25"): a recipe
            of rank 25 or more needs every book of its profession up to its rank (balance.yaml recipe_tiers.books). Empty for
            heroes saved before it.
        books_checked: True once the 0.44 grant ran for this hero (D-64: who had already practised a profession gets, free,
            the books of the ranks it had reached). False for heroes saved before it; the first load grants and sets it.
        book_gifts: ids of balance.yaml recipe_tiers.book_gifts already given to this hero (D-328, 0.52: the recipe books the
            refining, Alchemy and Medicine professions did not ask before, free for the ranks already reached). Empty for heroes
            saved before it (the first load gives them and fills it); a new hero starts with every id.
        map_scrolls: the 🗺️ map scrolls the hero carries (0.50, D-326), one record per copy: "id" (global, "p1"…), "by" (the
            🧭 Explorador who made it), "center" and "size" (its region), "zones" ("x:y" investigated to 50 % by its maker) and
            "at". The backpack counts them under balance.yaml map_scroll.item. Empty for heroes saved before it.
        charted: zones ("x:y") this hero sees in colour for ever because it used a map scroll (D-311 part 5). Only the map
            colour and the legend: no resources, nodes, places or travel. Empty for heroes saved before it.
        hybrid: what the 🔀 hybrid mode swapped (0.54, D-312, D-330), per role pair "<active role>><lending role>" -> the role
            slots ("H1", "H2", "H3") that carry the other role's ability in the same slot. Each role keeps its own choice.
            Empty for heroes saved before it and for whoever never uses it (they fight with their role's own bar).
        gear_wear: the durability of each worn piece (0.57, D-139, D-333), slot -> {"id": item id, "cur": durability, "max":
            its maximum, "rep": repairs done}. A worn piece without a record is new (full). Empty for heroes saved before it.
        bag_wear: the durability of the USED copies in the backpack (0.57), item id -> one record per used copy (same shape);
            the copies without a record are new. Empty for heroes saved before it.

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
    prof_specs: dict[str, list[str]] = field(default_factory=dict)      # D-141: 🎓 specializations held per profession
    learned: list[str] = field(default_factory=list)                    # D-257: professions learned (first recipe paid)
    spec_xp: dict[str, int] = field(default_factory=dict)               # D-141: mastery of every specialization ever held
    options: dict[str, Any] = field(default_factory=dict)
    origin: str | None = None
    story: dict[str, Any] = field(default_factory=dict)
    factions: dict[str, int] = field(default_factory=dict)
    journal: list[dict[str, Any]] = field(default_factory=list)
    bio: str = ""
    gear_signatures: dict[str, str] = field(default_factory=dict)
    gear_enchants: dict[str, dict[str, Any]] = field(default_factory=dict)
    guide: dict[str, Any] = field(default_factory=dict)                 # D-193: 🧭 guided path progress (empty = not read yet)
    combo_shapes: list[str] = field(default_factory=list)               # D-229: different chain combos ever cashed (variety)
    class_changes: int = 0                                              # D-270: class changes done (the first is free)
    home: list[int] = field(default_factory=lambda: [0, 0])               # D-265: the bonfire where the hero was born (0.37)
    prof_titles: dict[str, str] = field(default_factory=dict)           # D-306.1 (0.43): 🎖️ profession titles bought
    recipe_books: list[str] = field(default_factory=list)               # D-306: 📚 recipe books owned, "<profession>:<rank>" (0.44)
    books_checked: bool = False                                         # D-306: the 0.44 books already granted to who practised
    book_gifts: list[str] = field(default_factory=list)                 # D-328 (0.52): ids of the book gifts already given
    map_scrolls: list[dict[str, Any]] = field(default_factory=list)     # D-326 (0.50): 🗺️ map scrolls carried, one record per copy
    charted: list[str] = field(default_factory=list)                    # D-311.5 (0.50): zones in colour for ever thanks to a scroll
    hybrid: dict[str, list[str]] = field(default_factory=dict)          # D-330 (0.54): 🔀 hybrid swaps per role pair ("a>b" -> ["H2"])
    gear_wear: dict[str, dict[str, Any]] = field(default_factory=dict)  # D-333 (0.57): 🔧 durability of each worn piece, by slot
    bag_wear: dict[str, list[dict[str, Any]]] = field(default_factory=dict)   # D-333 (0.57): 🔧 durability of the used copies in the bag

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
    talentos (talent_bonus), de equipo (gear_bonus, con los ✨ encantamientos de las piezas, D-115) y de oficios
    (perk_bonus, D-111) que trae el kit del servicio.
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
