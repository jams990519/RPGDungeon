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
    diseno/06-contenido/jefes.md (el Guardián, D-82); diseno/08-social/gremios-y-social.md §0 (el gremio, D-97);
    diseno/02-mundo/supervivencia-del-asentamiento.md §0.4-0.5 (despensa e incursiones de los campamentos, D-93 y D-99);
    diseno/06-contenido/cacerias.md §0 (🏹 Cazar en la zona y 🏹 Partida de caza del campamento, D-106)
    diseno/07-economia/profesiones.md §0 (oficios encadenados, fase 1, D-109; §0.5, el ✨ Encantamiento de la fase 2, D-115)
    diseno/07-economia/red-de-oficios.md §3 (las 🎓 especializaciones de oficio, D-115 y D-141)
    diseno/03-personaje/equipamiento.md §11 (✨ encantamientos y el aviso "⬆️ Tienes una pieza mejor", fase 2 de D-115)
    diseno/02-mundo/mapa-infinito-y-viaje.md §1.12.1 (⚙️ Opciones y peleas automáticas en los lotes, D-114)
    diseno/02-mundo/mapa-infinito-y-viaje.md §1.14 (el oficio 🧭 Explorador y los ⛺ campamentos enemigos de cada día, D-112)
    diseno/06-contenido/historia-y-rol.md §0 (historia y rol, capa simple, D-117: la parte de la historia vive en
    engine/service/story.py, StoryMixin, de la que GameService hereda)
Módulo: capa de servicios (une M1, M2, M3, M5, M6, M8, M9, M10, M14, M15 y M19)
Depende de: engine.core, engine.hero (y engine.hero.gear: equipo, D-77), engine.world, engine.combat (y su forma de jugar
    sola, engine/combat/auto.py play_out, D-114), engine.messaging,
    engine.social (cuentas del gremio, D-97, y de la partida de caza, D-106), engine.professions (rangos y recetas,
    D-109), engine.service.story (StoryMixin: 📖 Historia, origen, misiones, facciones, encargos, diario y gestos, D-117;
    usa engine.story), engine.world.enemy_camps (dónde están los campamentos enemigos de cada día, su guarnición y su
    cofre, D-112), content/*
Lo usan: adapters/telegram/bot.py, adapters/cli/play.py, tests/test_service.py
Eventos que publica: HeroCreated, TravelStarted, TravelArrived, ZoneDiscovered, CombatStarted,
    HitReceived, HeroDowned, CombatEnded, BossDefeated, ItemCrafted y ProfessionRankUp (oficios, D-109)
Eventos que escucha: ninguno
Datos de los que es dueño: espacios "hero", "combat", "zone", "pending" y "meta" del almacén
    (en "meta", "guardian:<id>" guarda para siempre al primer héroe que venció a cada Guardián, D-82)
    D-125: "shop_week" (compras con tope de la semana de cada héroe, clave su id: {"week", "bought"}; _shop_week)
    D-93 (provisional) y D-95: "pantry" (despensa de cada campamento de jugadores, clave "x:y"; el Claro no tiene:
    no tiene dueño, D-95):
    {"rations", "at"}, consumo perezoso) y "active" (registro de quién jugó hoy y ayer, claves "0" y "1"
    según el día; se pisa solo, nunca crece). Diseño: diseno/02-mundo/supervivencia-del-asentamiento.md §0.4
    D-96 (provisional): "presence" (clave "x:y": {"seen": {cuenta: hora en que se anotó}}): quién puede estar en
    cada zona. Es solo un índice: si alguien cuenta como presente se decide al leer, con su ficha (sigue en esa zona
    y tocó un botón hace menos de presence.minutes, o explora, recolecta o duerme ahí). Se poda al leer.
    Diseño: diseno/02-mundo/mapa-infinito-y-viaje.md §1.13
    D-97 (provisional): "guild" (gremio de un campamento, clave "x:y" del campamento: nombre, nivel, contadores)
    y "guild_name" (nombres de gremio tomados). Los miembros del gremio son los del campamento ("camp").
    D-99 (provisional): en cada "camp/<x:y>" de nivel 5 o más, "next_raid_at" (hora de la próxima incursión),
    "raid" (la incursión abierta: kind "raid" o "trial", at, until, required, wins, fights {héroe: fighting, won,
    lost o fled}, enemy, level), "raids" ({"won", "lost"}), "trial_won" y "trial_retry_at" (Noche de prueba).
    Una pelea de defensa lleva "raid" ({"camp", "at"}) en su estado de "combat". Diseño: §0.5 del mismo documento
    D-101 (provisional): "upgrades" (mejoras de un campamento, clave "x:y": "built" id → hora, "works" obras a medias
    con lo aportado, "tech" conocimiento aprendido, el estudio en curso y su avance). Lo construido nunca se borra.
    D-116: en "upgrades" también "furniture" (🪑 muebles colocados: id del mueble → {"by", "id", "at"}; uno de cada uno,
    nunca se borra) y Hero.gear_signatures (firma de cada ✒️ obra maestra que lleva el héroe).
    D-115 (fase 2, lado del equipo): Hero.gear_enchants (el ✨ encantamiento de cada pieza: id de la pieza → {"id", "value"});
    se borra con la última copia de la pieza (_forget_piece). La experiencia del ✨ Encantamiento va en
    Hero.professions["encantamiento"].
    D-141: Hero.prof_specs (las 🎓 especializaciones de cada oficio, en el orden elegido) y Hero.spec_xp (el dominio de cada
    una, que nunca se borra: queda guardado aunque la cambies).
    D-106 (provisional): "hunt_party" (la partida de caza abierta de un campamento, clave "x:y" del campamento: x, y,
    at, until, caller, members {héroe: presas}, prey; se borra al cerrarla). Una pelea de cacería lleva "hunt" ({"x", "y"})
    en su estado de "combat". Diseño: diseno/06-contenido/cacerias.md §0
    D-114: Hero.options (⚙️ Opciones; vacío = balance.yaml auto_fight.defaults) y la actividad "hunt" (🏹 Cazar en lote,
    con las mismas claves que un lote de explorar). Un lote con peleas automáticas suma en su actividad "fights"
    ({"won", "lost", "fled"}), "fight_xp", "fight_gold", "gold_lost", "loot" y "fight_trade" para el resumen del final.
    D-117 (provisional): Hero.origin, Hero.story, Hero.factions, Hero.journal y Hero.bio, y el espacio "camp_tasks"
    (encargos semanales de cada campamento, clave "x:y"); los maneja engine/service/story.py (ver su encabezado).
    D-112: "enemy_camp" (lo que los jugadores le hicieron a un ⛺ campamento enemigo ese día, clave "<día>:<x>:<y>":
    {"day", "x", "y", "beaten" (guardias vencidos entre todos), "destroyed" ({by, name, at} o None), "fighters" {héroe:
    peleas ganadas o perdidas}, "scouted" [héroes que se infiltraron]}). Dónde hay campamento no se guarda: sale de la
    semilla y el día. Al escribir el primero de un día se borran los de antes de ayer. Una pelea del campamento lleva
    "enemy_camp" ({"day", "x", "y", "chief"}) en su estado de "combat"; la experiencia del 🧭 Explorador va en
    Hero.professions["explorador"] y su título en Hero.titles.
Reglas que nunca se rompen:
    1. Toda orden empieza por _settle(): ningún temporizador se pierde ni se duplica.
    2. En combate no se viaja ni se explora; viajando no se explora (una actividad a la vez).
    3. Ningún texto visible se escribe aquí: todo sale de content/locales (Texts).
    4. El servicio no sabe qué cliente lo llama: el id de cuenta lo arma el adaptador.
    5. El Pionero de un Guardián se escribe una sola vez y nunca se pisa; el aviso al servidor sale una sola vez.
    6. Nada se cobra a cambio de nada: un remedio con la vida llena, la posada sin heridas, recolectar o comprar
       con la mochila llena o recolectar en la zona agotada se rechazan con un aviso, sin gastar energía, monedas ni objetos.
    7. La despensa (D-93) es solo de los campamentos de jugadores y solo recibe lo que un jugador aporta: nunca
       toma comida de la mochila de nadie, y el hambre nunca quita niveles, zonas o miembros. El Claro es el
       campamento base: no crece ni se mantiene (D-95, D-98).
    8. Lo que se encuentra nunca se pierde (D-90, provisional): botín, equipo, carne y hallazgos de explorar entran
       aunque la mochila pase de su espacio; con la mochila en su espacio o más, solo se frenan recolectar y comprar.
    9. Ver a otros jugadores en la zona (D-96) es solo información: nunca da premio, pelea ni ventaja, nunca se
       lista uno mismo, y el cruce al explorar usa su propio sorteo (no cambia ningún otro resultado de la vuelta).
    10. El gremio (D-97) nunca saca a nadie: si el cupo baja, los que ya están se quedan.
    11. Una incursión perdida (D-99) solo quita parte de la despensa: nunca niveles, zonas ni miembros.
    12. Las mejoras (D-101) son solo de los campamentos de jugadores (el Claro no crece, D-98): lo construido queda para
        siempre, cada aporte toma solo lo que la obra todavía pide, y sus efectos valen solo para los miembros (y,
        salvo la Defensa y los servicios, solo en el territorio del campamento).
    13. Cazar (D-106) solo da la pelea y su botín: nunca exploración ni recursos. No hay presas donde el bioma no tiene
        peligro (el Claro) ni en la guarida del Guardián. La partida de caza no junta a nadie en una pelea (el combate
        sigue de 1 contra 1) y solo avisa a los miembros presentes en la misma zona (sin teletransporte).
    14. Los oficios (D-109) no tienen tope (D-57). Refinar y fabricar se hacen enteros o no se hacen: si falta un
        material, energía, la estación o el rango, no se gasta nada. Las unidades extra y los raros de los oficios usan
        su propio sorteo: nunca cambian lo que la vuelta de recolección o la pelea dan por su cuenta.
    15. Una pelea automática (D-114) es una pelea normal jugada por el motor: mismas reglas (resolve_round), mismo sorteo y
        mismo final (_end_combat: botín, experiencia, gremio, partida de caza, oficios y derrota). Solo van solos los
        encuentros comunes de un lote y las presas de la cacería en lote; nunca el Guardián, las defensas del campamento ni
        las emboscadas del viaje. Con ✋ Manual (lo de siempre) el lote se corta en la pelea. El bot avisa una sola vez por
        lote, al final, aunque haya habido muchas peleas.
    16. La historia (D-117) nunca bloquea el juego ni da poder de combate: el origen se puede elegir después, el menú de
        abajo siempre funciona y los rasgos y premios son de oficio, precio, reputación, consumibles, materiales y títulos.
    17. Los campamentos enemigos (D-112) son los mismos para todos (semilla + día), nunca en el Claro, la guarida ni el
        territorio de un campamento de jugadores, ni dos días seguidos en la misma zona. Mientras uno está en pie, su zona
        no se explora ni se recolecta (aviso, nada se cobra; un lote que se topa con uno devuelve la vuelta). Sus peleas
        son siempre a mano (nunca automáticas, D-114); el jefe solo cae en su propia pelea y la caída se paga una sola vez.
Si cambias esto, revisa:
    - Adaptadores: adapters/telegram/render.py y bot.py (IDs de acción y tipos de vista); bot.py y
      adapters/cli/play.py leen menu() y commands() (atajos /stats, /doble...)
    - Números: balance.yaml (explore, regen, hero, travel, guardian)
    - Comercio (D-116): _merchant_sale suma su beneficio (+20 % al rango 100) y su experiencia en _sell, _camp_sell y
      _sell_gear; no toca el combate (professions.trade_xp_per_coin)
    - ✒️ Obra maestra (D-116): balance.yaml masterwork; las piezas "<id>_obra" que arma engine/professions/rules.py
      masterwork_items al cargar; el sorteo en _make (_masterwork_chance: la 🪑 Carpintería con su perk, los demás con
      masterwork.base_chance), la firma en Hero.gear_signatures, la marca ✒️ en _gear_name, _worn_view y _gear_view, la
      firma en _item_view (_masterwork_note), la línea ✒️ en _recipe_view y ⚒️ Oficios, y _sell_gear (paga su precio, más
      alto, y borra la firma con la última copia). Pruebas: tests/test_masterwork.py
    - ✨ Encantamiento (D-115, fase 2): sección "enchanting" (_ench_view con /encantar, _enchant_view desde el botón ✨ de
      _item_view, _enchant, _disenchant; botones "ench", "ench:<pieza>", "enc:<pieza>", "dis:<pieza>", "dis!:<pieza>" en
      ENCHANT_ACTIONS). Números en balance.yaml enchanting; cuentas en engine/professions/rules.py; el bono entra al kit por
      engine/hero/gear.py gear_bonus (real_stats). No suma botón a ⚒️ Oficios (sus 4 lugares quedan para las estaciones):
      ahí sale con su rango, su beneficio (prof.perk.disenchant) y el próximo umbral (_ench_next, _ench_unlocks en _prof_gain).
      Desencantar nunca fabrica monedas (precios de esencia y esencia_mayor en items.yaml). Pruebas: tests/test_oficios_equipo.py
    - 🎓 Especializaciones de oficio (D-115, D-141): sección "profession specializations" (_pspecs_view con /especialidad y el
      botón 🎓 Especialización de ⚒️ Oficios, _pspec_prof_view, _pspec_view, _pspec_switch_view, _pspec_pick, _pspec_switch;
      botones "pspecs", "pspec:", "pspv:", "pspp:", "pspx:", "pspx!:" en SPEC_ACTIONS). Datos en content/professions.yaml "specs"
      (y recetas con "spec"), números en balance.yaml specs, cuentas en engine/professions/rules.py (spec_*), textos en
      content/locales/es_especializaciones.yaml. Sus efectos entran por _pspec_bonus/_pspec_finds en _perks (perk), _merchant_sale
      (coins: goods, barter, gear), _trade_gather y _trade_loot (yield, find), _make y _recipe_view (yield, find, masterwork y la
      receta exclusiva: _pspec_recipe_ok), _station_view, _next_unlock y _prof_gain (recetas exclusivas; _pspec_gain sube el
      dominio y avisa al rango 25 y 75), _enchant_plan y _ench_view (enchant), _infiltrate (detect) y _ecamp_destroyed (coins:
      ecamp). Ojo: _spec_view es la pantalla de la especialización de CLASE (talentos); la de oficio es _pspec_view.
      Pruebas: tests/test_especializaciones.py
    - ⬆️ Pieza mejor (D-115, fase 2): _better_piece mira lo que entró a la mochila en _end_combat (botín, cofre, Guardián) y en
      _make; _better_line + _better_action (🔁 Equipar = "equip:<id>", primero, sin pasar 4 botones); en las peleas automáticas
      la línea va al resumen del lote (_auto_combat). La marca ⬆️ en _gear_view sale de engine/hero/gear.py is_better
      (balance.yaml gear.score). Nunca pone nada solo
    - 🪑 Muebles del campamento (D-116): items.yaml kind: furniture (effect), recetas de la Carpintería; _furniture_effect
      entra en _effect_at/_camp_effect (members → _members_cap) y en _camp_defense (defense → oleadas); se colocan desde
      🔨 Obras (_works_entries, _place_furniture, botón "upf:<id>"); 📦 Recursos los lista (tests/test_masterwork.py)
    - Beneficio de cada oficio (D-111): _perks (content/professions.yaml "perk", engine/professions/rules.py perks) entra en
      _kit (perk_bonus, heal_bonus, item_bonus), _settle (Herbolario), _use_out_of_combat (Alquimia, Medicina) y _bag_cap
      (Leñador); hero_stats y el combate lo leen del kit (tests/test_professions.py)
    - Pasada de balance de clases y roles (D-110, D-113): _stats_view muestra la armadura que dan los puntos de Defensa
      (stats.talents_armor); _station_view pone primero las recetas de rango más alto (equipo de artesano hasta el nivel
      100); el bono de botín de la partida de caza parte de gear.drop_chance_for (menos botín desde el nivel 10).
      Medir con tools/balance_report.py (tests/test_balance_d110.py)
    - Experiencia por camino (D-108): _zone_xp escala matar y recolectar con hero.xp_level_scale; gather.xp_per_step.
      Todos los caminos tienen que llegar al 100 a un ritmo parecido (diseno/03-personaje/progresion.md §1.2)
    - Explorar alrededor (D-107): con tu zona al 100 %, el lote sigue con las vecinas sin moverte (_explore_target,
      explore.around_radius); las vecinas exploradas quedan en hero.known y cuentan para fundar (tests/test_resources.py)
    - Encuentros (D-108): _start_combat elige el enemigo con engine/world/encounters.py (bioma de la zona y franja de
      nivel de content/enemies.yaml; más allá de la última franja, la más cercana). Pruebas: tests/test_bestiary.py
    - Pruebas: tests/test_service.py, tests/test_boss.py, tests/test_buttons.py, tests/test_spec_abilities.py (barra, D-79),
      tests/test_playtest_fixes.py (fallos de la prueba de juego de la 0.9.2), tests/test_pantry.py (despensa, D-93),
      tests/test_backpack.py (mochila llena D-90 y cofre D-92)
    - Despensa (D-93): balance.yaml pantry; engine/world/pantry.py; textos pantry.* en es.yaml
    - Mochila llena (D-90): balance.yaml hero.backpack_capacity; _bag_full, _bag_add, _gather_blocked, _buy
    - Cofre (D-92): balance.yaml currency.chest_recipe e icons.chests, camps.chests_from_level y chests_per_level;
      Hero.chests; _build_chest, _grow_chests; textos wallet.chest*, camps.chest* en es.yaml
      tests/test_zone_players.py (jugadores en la zona, D-96)
    - Jugadores en la zona (D-96): balance.yaml presence; textos presence.* en es.yaml; Hero.seen_at (lo marca
      _mark_seen: si cambia cuándo se marca, cambia quién aparece en 📍 Zona); _arrive mueve la presencia al llegar
    - Gremio (D-97): balance.yaml guild; engine/social/guilds.py; textos guild.* en es.yaml; tests/test_guilds.py.
      Sus contadores se suman en _settle (exploración y recolección) y en _end_combat (victoria)
      tests/test_raids.py (incursiones y Noche de prueba, D-99)
    - Incursiones (D-99): balance.yaml raids; engine/world/raids.py; textos raids.* en es.yaml; los botones
      🛡️ Defender ("defend") y 🌙 Noche de prueba ("trial"); _grow_view/_grow_camp (castillo pide la prueba ganada)
    - Mejoras y conocimiento (D-101): content/camp_upgrades.yaml (catálogo), balance.yaml upgrades; textos upgrades.*,
      knowledge.*, upgrade.* y tech.* en es.yaml; tests/test_camp_upgrades.py. Sus efectos tocan _settle (vida: Fogón y
      Enfermería), _explore_step (Cartografía), _gather_step (Herramientas), _end_combat (Rastreo), _stock (Pozo),
      _members_cap (Cabañas), _camp_pantry y _camp_feed (Granero, Huerto, Ahumadero), _wallet_view, _sew_bag y
      _build_chest (Taller), _item_view y _sell_gear (Herrería), _grow_view y _grow_camp (15 mejoras para castillo).
      _camp_defense lo leen las oleadas: _open_raid la guarda y _raid_weaken frena a los atacantes; la Torre de vigía
      avisa con _raid_watch (tests/test_raids.py)
      tests/test_hunt.py (cacería en la zona y partida de caza, D-106)
    - Cacería (D-106): balance.yaml hunt; engine/social/hunting.py; textos hunt.* en es.yaml; los botones
      🏹 Cazar ("hunt"), 🏹 Buscar presa y 🏹 Otra presa ("prey"), 🏹 Partida de caza ("huntparty") y 🏹 Unirme
      ("huntjoin"); _explore_menu (4 botones: 📒 Lugares se mudó a 🗺️ Mapa, que es la vuelta de _places_view),
      _start_combat (marca "hunt" en el combate), _end_combat (bono, cuenta de presas y 🏹 Otra presa) y la presencia
      de D-96 (_zone_players decide a quién avisa la partida y quién da bono); _spend_energy recibe el costo de cazar
    - Oficios encadenados (D-109): content/professions.yaml (oficios, estaciones y recetas), balance.yaml professions
      (curva de rango, unidad extra, raros, experiencia de héroe por ⚡, bono del campamento), engine/professions;
      Hero.professions; textos prof.*, profession.* e item.* en es.yaml; tests/test_professions.py. Tocan _gather_step
      (_trade_gather: oficio, unidad extra y raros), _batch_summary (línea ⚒️ Oficios), _end_combat (_trade_loot: carne y
      piel del 🔪 Desollador), _claro_view (⚒️ Oficios es su 3.er botón), _workshop_view (4.º botón) y _services_view
      (⚒️ Oficios si hay 🔨 Herrería sin 🧵 Taller), _hero_view (línea /oficios) y COMMANDS (/oficios). La experiencia de
      héroe al refinar y fabricar (_make_xp) sigue a D-108: tiene que quedar a la par de recolectar por cada ⚡
    - ⚙️ Opciones y peleas automáticas (D-114): balance.yaml auto_fight (opciones por defecto, % de 🩹 Retirarse, tope de
      rondas y umbrales de la forma de jugar) y hunt.batch / hunt.batch_minutes; engine/combat/auto.py (la forma de jugar,
      la misma que usa tools/sim.py); Hero.options; textos options.*, auto.*, batch.*_hunt, batch.reason.auto_* y hunt.batch_*
      y hunt.mode_* en es.yaml; tests/test_options.py. Tocan menu() (⚙️ Opciones, último botón), COMMANDS (/opciones), _idle_action ("options",
      "opt:"), _settle (_batch_fight → _auto_combat → _end_combat), _amount_view, _start_batch, _stop_batch, _continue_batch,
      _batch_summary (_auto_summary), _activity_view, _hunt_view y _hunt ("prey" abre 🏹 Cazar en lote en automático) y
      PRESENT_BUSY (quien caza en lote cuenta como presente, D-96)
    - Historia y rol (D-117): content/story.yaml (orígenes, misiones, personajes, facciones, encargos), textos story.* en
      content/locales/es_historia.yaml, balance.yaml story; engine/service/story.py y engine/story; tests/test_story.py.
      El gancho _story_event se llama en _arrive (visit), _explore_step (explore), _gather_step (gather), _end_combat (win,
      también las peleas automáticas: _auto_combat pasa state["story"] al resumen del lote), _make (craft), _sell, _camp_sell
      y _sell_gear (sell), _found_camp (camp), _camp_feed (feed) y _give_to_work / _give_to_study (build). Tocan además
      menu() (📖 Historia es el 6.º botón, ⚙️ Opciones sigue último), COMMANDS (/historia, /diario, /bio, /encargos,
      /saludar, /brindar), text() (atajos con texto), _idle_action (STORY_ACTIONS; "hero" ofrece el origen una vez),
      _create_action (el origen después de la clase), _claro_view (📜 Tablón en lugar de ↩️ Volver), _shop_view y _buy (descuento
      del origen), _prof_gain (experiencia de oficio del origen), _hero_view (origen, emblema, biografía y títulos de la
      historia), _zone_players (emblema junto al nombre) y tick() (relee el héroe: otro pudo pagarle un encargo de campamento)
    - 🧭 Explorador y ⛺ campamentos enemigos (D-112): balance.yaml explorer (experiencia del oficio, umbrales del mapa) y
      enemy_camps (densidad, guarnición, jefe, energía, cofre, parte, infiltración); content/professions.yaml (explorador,
      rama explore, perk explore); engine/world/enemy_camps.py; textos ecamp.*, explorer.* y los de profession.explorador,
      prof.perk.explore, prof.branch.explore, batch.reason.enemy_camp y story.journal.enemy_camp* en
      content/locales/es_exploracion.yaml; tests/test_enemy_camps.py. Tocan _settle (un lote en la zona de un campamento se
      corta y devuelve la vuelta), _arrive (aviso al llegar), _explore_target (salta zonas con campamento), _explore_step
      (experiencia y beneficio del Explorador), _amount_view, _start_batch y _continue_batch (explorar y recolectar
      bloqueados), _batch_summary (línea ⚒️ Oficios al explorar), _zone_view (línea y marca ⛺ en las rutas), _explore_menu
      (_ecamp_menu: ⚔️ Asaltar, 🕵️ Infiltrarse, 🏹 Cazar, 🗺️ Mapa), _idle_action ("assault", "infiltrate"; "goto:" acepta
      un campamento visible), _places_view (8 lugares desde el rango 10), _map_view (⛺, líneas y ⛺ Ir al más cercano),
      _batch_fight (nunca pelea solo un campamento), _end_combat (_ecamp_fight_done y ⚔️ Seguir asaltando), _combat_view
      (marca del jefe), _prof_gain (umbrales del mapa y el título), _next_unlock, _professions_view y _perk_text. El gancho
      _story_event recibe "infiltrate" y "enemy_camp" (📔 Diario, engine/service/story.py _story_marks)
"""

from __future__ import annotations

import math
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
from engine.combat import CombatContext, make_combat, play_out, resolve_round, validate_choice
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
    ItemCrafted,
    ProfessionRankUp,
    Rng,
    Store,
    Texts,
    TravelArrived,
    TravelStarted,
    ZoneDiscovered,
    hash_unit,
)
from engine.hero import Hero, hero_stats, xp_for_level
from engine.hero.gear import (auto_equip, can_use, drop_chance_for, equip, gear_bonus, roll_gear, source_choices,
                              starter_gear, suits, unequip)
from engine.hero.gear import gear_score, is_better, piece_score, real_stats     # D-115 (fase 2): ✨ encantamientos y ⬆️ pieza mejor
from engine.professions import gatherer_of, masterwork_chance, masterwork_id, max_times, missing_for, rank_of, rank_title, xp_for_rank
from engine.professions import rules as profession_rules
from engine.messaging import Action, View
from engine.world import DIRECTIONS, Zone, travel_minutes, zone_at
from engine.world import pantry as pantry_rules
from engine.social import guilds as guild_rules
from engine.social import hunting as hunt_rules
from engine.service.story import STORY_ACTIONS, StoryMixin
from engine.world import raids as raid_rules
from engine.world import enemy_camps as camp_rules
from engine.world.encounters import clamp_level, encounter_pool
from engine.world.territory import first_zones
from engine.world.resources import main_resource, zone_resources

# Typed shortcuts that the texts mention (e.g. "🔀 Doble especialización: /doble"); every client offers the same ones.
COMMANDS = {"/stats": "stats", "/inv": "bag", "/habilidades": "talents", "/hero": "hero", "/zona": "home",
            "/equipo": "gear", "/monedas": "wallet", "/doble": "dual", "/gremio": "guild", "/salud": "health",
            "/oficios": "oficios", "/opciones": "options",
            "/historia": "story", "/diario": "journal", "/bio": "bio", "/encargos": "board",     # D-117: story and roleplay
            "/saludar": "gesture:saludar", "/brindar": "gesture:brindar",
            "/encantar": "ench",                                                               # D-115: ✨ Encantamiento
            "/especialidad": "pspecs"}                                                         # D-141: 🎓 Especialización
ROMAN = ["0", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
NAME_RE = re.compile(r"^[^\W\d_][\w ]{1,15}$", re.UNICODE)
CAMP_NAME_RE = re.compile(r"^[^\W_][\w '\-]{2,23}$", re.UNICODE)
# Timed activities done INSIDE the zone: the hero counts as present while doing them, even with the chat closed (D-96).
PRESENT_BUSY = ("explore", "gather", "rest", "hunt")
# Activities that go in batches of energy (D-87); "hunt" only with ⚔️ automatic fights (D-114).
BATCH_KINDS = ("explore", "gather", "hunt")
# Button ids (or prefixes) of the camp improvements, their services and the knowledge (D-101): _upgrade_action routes them.
UPGRADE_ACTIONS = ("upgrades", "upw", "upg:", "upsvc", "crest", "csell", "ctaller", "tsew", "tchest", "know", "kstart:", "kgive",
                   "upf:")       # D-116: 🪑 Colocar a camp furniture piece (from 🔨 Obras)
# Button ids (or prefixes) of ⚒️ Oficios, its stations, recipes and "make" (D-109): _prof_action routes them.
PROF_ACTIONS = ("oficios", "est:", "rec:", "mk:")
# Button ids (or prefixes) of ✨ Encantamiento (D-115, phase 2): the hub, a piece's screen, enchant, disenchant (and confirm it).
ENCHANT_ACTIONS = ("ench", "enc:", "dis:", "dis!:")
# Button ids (or prefixes) of 🎓 Especialización (D-141): the hub (and its pages), a profession, a specialization, pick it, switch
# (asks first) and switch confirmed. _pspec_action routes them.
SPEC_ACTIONS = ("pspecs", "pspec:", "pspv:", "pspp:", "pspx:", "pspx!:")


class GameService(StoryMixin):
    """The engine's facade for every client (the story and roleplay part lives in engine/service/story.py, D-117).

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
        self._raid_settle(hero)
        self._hunt_party_settle(hero)       # D-106: the camp's hunting party closes lazily too
        self._save(hero)
        return self._main_view(hero, notice=self._join(notices))

    def text(self, account_id: str, text: str) -> View:
        """Handle free text: the hero's name, a camp or guild name, or a typed command ("/bio ...", "/saludar Bram").

        [ES]
        Qué hace: recibe texto escrito: el nombre del héroe al crearlo, el nombre de un campamento o gremio, o un atajo
        escrito con "/" (D-117: /bio <texto>, /saludar <nombre>, /brindar <texto>, /diario <nombre>; los atajos sin texto,
        como /stats, van como su botón). Un "/" sin héroe todavía muestra la creación, sin error.
        La llaman: los clientes (Telegram manda aquí todo texto que empieza con "/" y no es un atajo exacto).
        Si cambia, afecta: la creación de personaje, los nombres de campamento y gremio, y los atajos con texto.
        """
        self._seen(account_id)
        hero = self._load(account_id)
        if text.lstrip().startswith("/"):
            if hero is None:
                return self.view(account_id)
            self._mark_seen(hero)
            notices = self._settle(hero)
            typed = self._typed_command(hero, text)      # D-117: commands that carry text
            self._save(hero)
            if typed is None:
                word = text.split()[0].split("@")[0].lower() if text.split() else ""
                typed = self.act(account_id, COMMANDS[word]) if word in COMMANDS else self.view(account_id)
            if notices:                                  # what _settle finished (a trip, a batch) is told once, here
                typed.notice = self._join(notices + ([typed.notice] if typed.notice else []))
            return typed
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
        self._presence_note(hero)                       # D-96: others see you in 📍 Zona
        self._raid_settle(hero)             # D-99: the camp's raid clock is lazy too
        self._hunt_party_settle(hero)       # D-106: and so is its hunting party
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
        Qué hace: da el menú fijo (Zona, Explorar, Campamento, Héroe, 📖 Historia y ⚙️ Opciones; D-114, D-117); cada cliente
        lo dibuja abajo o al costado. D-46 deja hasta 6: ya están los 6. ⚙️ Opciones sigue siendo el último.
        La llaman: los adaptadores (Telegram lo pone en el teclado de abajo, de 2 en 2: con 6 quedan 3 filas).
        Si cambia, afecta: la navegación de todos los clientes (tests/test_buttons.py y tests/test_options.py miran el tope).
        """
        t = self.texts
        return [Action(id="home", label=t.t("menu.zone")), Action(id="explore_menu", label=t.t("menu.explore")),
                Action(id="claro", label=t.t("menu.camp")), Action(id="hero", label=t.t("menu.hero")),
                Action(id="story", label=t.t("menu.story")),          # D-117: 📖 Historia, the 6th and last slot of D-46
                Action(id="options", label=t.t("menu.options"))]

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
            data = self.store.get("hero", account_id) or data     # fresh: an earlier hero may have paid this one (D-117 camp tasks)
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
        perk = self._perks(hero)                  # D-111: each profession's own benefit, growing with its rank
        kit["perk_bonus"] = {k: perk[k] for k in ("attack", "hp", "armor")}
        kit["heal_bonus"] = perk["heal"]
        kit["item_bonus"] = {"potion": perk["potion"], "bandage": perk["bandage"]}
        return kit

    def _perks(self, hero: Hero) -> dict[str, float]:
        """The benefits of the hero's professions (D-111), each growing evenly with its rank (profession_rules.perks).

        [ES]
        Qué hace: junta los beneficios de los oficios que el héroe empezó (rango de cada uno), sabiendo qué armadura
        usa su clase, con qué arma pelea y qué rol juega (la Herrería solo con placas, la Medicina solo a sanadores).
        D-141: les suma los efectos "perk" de las 🎓 especializaciones que tiene (por su dominio): 🍷 Elixires (pociones),
        🩹 Primeros auxilios (vendas), 🩺 Cirugía (curaciones, solo sanadores), ☠️ Venenos (ataque), 🎒 Talabartería y 🛒 Mobiliario
        (mochila), 🗺️ Cartógrafo, 📜 Papel y Pergamino (exploración) y 💨 Desencantar (esencias).
        La llaman: _kit (ataque, vida, armadura, curación, pociones y vendas), _settle (vida que vuelve), _bag_cap.
        Si cambia, afecta: cuánto ayuda cada oficio (content/professions.yaml "perk" y "specs"; profesiones.md §0.2).
        """
        catalog = (self.content.professions or {}).get("professions") or {}
        ranks = {pid: self._prof_rank(hero, pid) for pid, xp in (hero.professions or {}).items() if xp > 0 and pid in catalog}
        cdef = self.content.classes.get(hero.class_id, {})
        group = cdef.get("group", hero.class_id)
        gear_cfg = self.content.balance["gear"]
        weapon = self.content.items.get(hero.gear.get("arma", ""), {})
        out = profession_rules.perks(catalog, ranks, self.content.balance["professions"]["max_rank"],
                                     gear_cfg["armor_by_group"].get(group), weapon.get("type"), cdef.get("role"))
        if hero.prof_specs:                             # D-141: the 🎓 specializations' perk effects, by their mastery
            for key in profession_rules.PERK_KEYS:
                out[key] += self._pspec_bonus(hero, "perk", key=key, role=cdef.get("role"))
        return out

    def _money(self, amount: int) -> str:
        """Coins as 🥇 gold · 🥈 silver · 🥉 bronze (D-80, D-85): 100 bronze = 1 silver, 100 silver = 1 gold."""
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
            pct = 1 / (regen["downed_full_minutes"] if hero.downed else regen["hp_full_minutes"])      # share of max hp per minute
            pct *= self._camp_regen_mult(hero)          # D-101: 🔥 Fogón / 🏥 Enfermería in your camp's territory
            pct *= 1 + self._perks(hero)["regen"]       # D-111: 🌿 Herbolario
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
            elif activity["kind"] in BATCH_KINDS:
                zone = self._zone(hero.x, hero.y)
                activity.setdefault("left", 0)
                activity.setdefault("got", {})
                activity.setdefault("log", [])
                if activity["kind"] in ("explore", "gather") and self._ecamp_standing(hero.x, hero.y):
                    hero.energy += self._step_cost(activity["kind"])    # D-112: an enemy camp stands here now: round given back
                    notices += self._batch_summary(hero, activity, "enemy_camp")
                    continue
                activity["done"] = activity.get("done", 0) + 1
                if activity["kind"] == "explore":
                    fight = self._explore_step(hero, zone, rng, activity)
                    tally["explorations"] = tally.get("explorations", 0) + 1
                    if zone.x == 0 and zone.y == 0:
                        activity["log"] += self._tutorial(hero, "explore_claro")
                elif activity["kind"] == "gather":
                    before = sum(activity["got"].values())
                    fight = self._gather_step(hero, zone, rng, activity)
                    tally["gathered"] = tally.get("gathered", 0) + sum(activity["got"].values()) - before
                    activity["log"] += self._tutorial(hero, "gather")
                else:                                   # D-114: a hunting batch, every prey is a fight
                    fight = self._hunt_step(hero, zone, rng)
                if fight:
                    stop = self._batch_fight(hero, activity, fight)    # D-114: ✋ the batch stops; ⚔️ the hero fights now
                    if stop is not None:
                        notices += stop
                        continue
                elif activity["kind"] != "hunt":
                    activity["log"] += self._cross_paths(hero, zone, activity)     # D-96: flavour only
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
        left = (hero.x, hero.y)
        hero.x, hero.y = activity["to"]
        self._presence_move(hero, *left)                # D-96: out of the zone it left, into the new one
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
            if self._ecamp_standing(hero.x, hero.y):
                notices.append(self.texts.t("ecamp.arrive"))      # D-112: an enemy camp stands here
        if self._discovered(hero.x, hero.y) is None:
            self.store.put("zone", f"{hero.x}:{hero.y}", {"discovered_by": hero.name, "at": activity["until"]})
            hero.zones_discovered += 1
            self.bus.publish(ZoneDiscovered(hero.id, hero.x, hero.y))
            notices.append(self.texts.t("travel.discovered_named", name=self._zone_name(zone)))
        notices += self._story_event(hero, "visit", x=hero.x, y=hero.y, lejania=zone.lejania, lair=self._is_lair(hero.x, hero.y))   # D-117
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

    def _spend_energy(self, hero: Hero, kind: str, cost: int | None = None) -> bool:
        """Pay the energy of a non-combat action: move, explore or gather (D-78); hunting passes its own cost (D-106)."""
        cost = self.content.balance["energy"][f"per_{kind}"] if cost is None else cost
        if hero.energy < cost:
            return False
        if hero.energy >= self.content.balance["energy"]["max"]:
            hero.energy_at = self.clock.now()
        hero.energy -= cost
        return True

    def _no_energy_notice(self, hero: Hero) -> str:
        wait = self._energy_period() - (self.clock.now() - hero.energy_at)
        return self.texts.t("energy.empty", time=self._fmt_duration(max(1, wait)), per_day=self.content.balance["energy"]["per_day"],
                            hunt=self.content.balance["hunt"]["energy"])

    def _explore_target(self, hero: Hero) -> tuple[int, int] | None:
        """The zone the next exploration studies: yours until 100 %, then the ones around you (D-107).

        [ES]
        Qué hace: dice qué zona estudia la próxima vuelta de exploración. Primero la tuya; cuando está al 100 %, la
        primera de alrededor (explore.around_radius casillas; primero norte, este, sur y oeste, después las diagonales)
        que no esté al 100 %. El héroe no se mueve: explora desde donde está. None si ya no queda nada cerca.
        D-112: una zona con un ⛺ campamento enemigo en pie no se explora: se salta (la tuya y las de alrededor).
        La llaman: _explore_step, _amount_view, _start_batch, _continue_batch y _activity_view.
        Si cambia, afecta: qué zonas se completan al explorar en lote y cuándo se corta el lote (tests/test_service.py).
        """
        if self._explored_pct(hero, hero.x, hero.y) < 100 and not self._ecamp_standing(hero.x, hero.y):
            return hero.x, hero.y
        for x, y in self._explore_around(hero):
            if self._explored_pct(hero, x, y) < 100 and not self._ecamp_standing(x, y):
                return x, y
        return None

    def _explore_around(self, hero: Hero) -> list[tuple[int, int]]:
        """The zones around the hero that exploring reaches without moving, nearest first, N E S W before diagonals."""
        radius = self.content.balance["explore"]["around_radius"]
        cells = [(dx, dy) for dx in range(-radius, radius + 1) for dy in range(-radius, radius + 1) if dx or dy]
        # nearest ring first; in a ring, straight lines before diagonals; then clockwise from the north
        cells.sort(key=lambda c: (max(abs(c[0]), abs(c[1])), abs(c[0]) + abs(c[1]), math.atan2(c[0], c[1]) % (2 * math.pi)))
        return [(hero.x + dx, hero.y + dy) for dx, dy in cells]

    def _explore_step(self, hero: Hero, zone: Zone, rng: Rng, activity: dict[str, Any]) -> str | None:
        """One exploration: +15-30 % of the zone studied, maybe a find; returns a combat notice if a fight starts (D-87).

        The zone studied is yours until 100 %, then the ones around you, without moving (D-107). Fights, finds and
        coins come from the zone where the hero stands.

        [ES] D-112: cada vuelta sube el oficio 🧭 Explorador (explorer.xp_per_step, más explorer.xp_full_zone al dejar una
        zona al 100 %; va al resumen del lote en "trade") y su beneficio suma puntos de exploración (parte entera del perk
        "explore": +1 cada 20 rangos, +5 al 100), sin otro sorteo: las vueltas de siempre dan lo mismo.
        """
        t = self.texts
        target = self._explore_target(hero) or (zone.x, zone.y)
        studied = zone if target == (zone.x, zone.y) else self._zone(*target)
        key = f"{studied.x}:{studied.y}"
        if studied is not zone and activity.get("target") != key:
            activity["log"].append(t.t("explore.around", name=self._zone_name(studied), x=studied.x, y=studied.y))
        activity["target"] = key
        hero.remember(studied.x, studied.y)           # it shows on your 🗺️ Mapa, like a zone you visited
        before = self._known_resources(hero, studied.x, studied.y)
        before_pct = self._explored_pct(hero, studied.x, studied.y)
        low, high = self.content.balance["exploration"]["per_step"]
        step = int(rng.uniform(low, high + 1)) + int(self._camp_tech_bonus(hero, studied.x, studied.y, "explore_points"))   # D-101: Cartografía
        step += int(self._perks(hero)["explore"])     # D-112: 🧭 Explorador, +1 point every 20 ranks (no extra draw)
        hero.exploration[key] = min(100, before_pct + step)
        if key not in hero.explored:
            hero.explored.append(key)
        new = [r for r in self._known_resources(hero, studied.x, studied.y) if r not in before]
        if new:
            names = ", ".join(f"{self.content.items[r]['emoji']} {t.t(self.content.items[r]['name_key'])}" for r in new)
            activity["log"].append(t.t("explore.revealed", items=names) if studied is zone
                                   else t.t("explore.revealed_there", name=self._zone_name(studied), items=names))
        bal = self.content.balance["explore"]
        xp = bal["xp_per_step"]                       # exploring teaches: experience every round (owner's request)
        if hero.exploration[key] >= 100:
            activity["log"].append(t.t("explore.full", name=self._zone_name(studied)))
            if before_pct < 100:
                xp += bal["xp_full_zone"]             # finishing a zone is worth more
        activity["xp"] = activity.get("xp", 0) + int(xp * self._xp_mult(hero))
        activity["log"] += self._give_xp(hero, xp)
        ecfg = self._explorer_cfg()                   # D-112: every round raises the 🧭 Explorador, a full zone more
        trade_xp = ecfg["xp_per_step"] + (ecfg["xp_full_zone"] if hero.exploration[key] >= 100 and before_pct < 100 else 0)
        trade = activity.setdefault("trade", {})
        trade[ecfg["profession"]] = trade.get(ecfg["profession"], 0) + trade_xp
        activity["log"] += self._prof_gain(hero, ecfg["profession"], trade_xp)
        activity["log"] += self._story_event(hero, "explore", x=zone.x, y=zone.y, lejania=zone.lejania)     # D-117
        roll = rng.random()
        if roll < bal["encounter"] and self.content.biomes[zone.biome]["danger"] > 0 and not self._territory(zone.x, zone.y):
            return self._start_combat(hero, zone, rng, "encounter.found")
        if roll < bal["encounter"] + bal["item"]:
            options = ["hierba_curativa", "pieza_metal", "venda", "pocion_vida"]
            item_id = rng.pick_weighted(options, [5, 3, 2, 1])
            self._bag_add(hero, item_id, 1)                  # never lost, even with a full backpack (D-90)
            activity["got"][item_id] = activity["got"].get(item_id, 0) + 1
            return None
        coins = int(zone.level * rng.uniform(2, 5)) + 1
        hero.gold += coins
        activity["coins"] = activity.get("coins", 0) + coins
        return None

    def _gather_step(self, hero: Hero, zone: Zone, rng: Rng, activity: dict[str, Any]) -> str | None:
        """One gathering: only the resources this zone has, less when it is depleted, up to the backpack's space (D-87, D-90)."""
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
            tools = 1 + self._camp_tech_bonus(hero, zone.x, zone.y, "gather_bonus")    # D-101: Herramientas
            amount = int(amount * bal["own_land_bonus"] * tools + 0.5)     # your camp's land gives more (D-87)
        got: dict[str, int] = {}
        for _ in range(max(1, amount)):
            options = [r for r in resources if stock[r] >= cfg["min_yield"]]
            if not options or self._bag_full(hero):      # gathering stops at the space (D-90); finds do not
                break
            res = rng.pick_weighted(options, [resources[r] * stock[r] for r in options])
            self._bag_add(hero, res, 1)
            stock[res] = max(0.0, stock[res] - cfg["per_unit"])
            got[res] = got.get(res, 0) + 1
        self.store.put("stock", f"{zone.x}:{zone.y}", {"levels": stock, "at": self.clock.now()})
        activity["log"] += self._trade_gather(hero, got, activity)    # D-109: gathering professions (rank, extra units, rare finds)
        for res, n in got.items():
            activity["got"][res] = activity["got"].get(res, 0) + n
        if got:
            activity["log"] += self._story_event(hero, "gather", items=dict(got))     # D-117: missions and tasks
        if got:                                       # D-108: gathering alone also reaches level 100
            xp = self._zone_xp(bal["xp_per_step"], zone.level)
            activity["xp"] = activity.get("xp", 0) + int(xp * self._xp_mult(hero))
            activity["log"] += self._give_xp(hero, xp)
        if not got:
            activity["left"] = 0
            activity["log"].append(self.texts.t("batch.reason.bag_full" if self._bag_full(hero) else "batch.reason.depleted"))
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
        hero.story["offered"] = True                     # D-117: the origin is chosen right now (or later, in 📖 Historia)
        self._journal(hero, "awoke")
        self._save(hero)
        self.store.delete("pending", account_id)
        self.bus.publish(HeroCreated(hero.id, class_id))
        return self._origin_view(hero, notice=self.texts.t("create.welcome", name=hero.name))

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
        if action_id == "hero":                         # D-117: heroes without an origin get the choice once, here or in 📖 Historia
            return self._origin_offer(hero) or self._hero_view(hero)
        if action_id == "options":                      # D-114: ⚙️ Opciones (bottom menu, /opciones); works while busy too
            return self._options_view(hero)
        if action_id.startswith(STORY_ACTIONS):         # D-117: 📖 Historia and its screens, 📜 Tablón, gestures; also while busy
            return self._story_action(hero, action_id)
        if action_id.startswith("opt:"):
            return self._set_option(hero, action_id[4:])
        if action_id == "stats":
            return self._stats_view(hero)
        if action_id == "health":
            return self._health_view(hero)
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
        if action_id == "resources" or action_id.startswith("res:"):
            page = action_id[4:]
            return self._resources_view(hero, int(page) if page.isdigit() else 0)
        if action_id == "wallet":
            return self._wallet_view(hero)
        if action_id == "gems":
            return self._gem_shop_view(hero)
        if action_id.startswith("gem:"):
            return self._buy_with_gems(hero, action_id[4:])
        if action_id == "sew":
            return self._sew_bag(hero)
        if action_id == "chest":
            return self._build_chest(hero)
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
        if action_id.startswith(ENCHANT_ACTIONS):       # D-115: ✨ Encantamiento (the screens work while busy; doing it, not)
            return self._enchant_action(hero, action_id)
        if action_id == "places":
            return self._places_view(hero)
        if action_id == "memento":
            return self._memento_view(hero)
        if action_id.startswith("mem:"):
            return self._use_memento(hero, action_id[4:])
        if action_id.startswith(PROF_ACTIONS):          # D-109: ⚒️ Oficios, its stations, recipes and 🔨 Hacer
            return self._prof_action(hero, action_id)
        if action_id.startswith(SPEC_ACTIONS):          # D-141: 🎓 Especialización (choosing works while busy: it is a menu)
            return self._pspec_action(hero, action_id)
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
        if action_id == "defend":                       # D-99: from the raid notice or the camp screen
            return self._defend(hero)
        if action_id == "trial":                        # D-99: call the Noche de prueba (grow screen, level 8)
            return self._start_trial(hero)
        if action_id == "huntjoin":                     # D-106: from the party notice; joining works while busy too
            return self._join_hunt_party(hero)
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
        if action_id.startswith(UPGRADE_ACTIONS):          # D-101: 🔨 Mejoras, their services and the knowledge
            return self._upgrade_action(hero, action_id)
        if action_id == "claro" and not in_claro:
            return self._camp_here_view(hero)
        if action_id == "claro":
            return self._claro_view(hero)
        if action_id in ("camp", "donate", "feed"):     # old buttons of the Claro's common work: it no longer grows (D-98)
            if not in_claro:
                return self._main_view(hero, notice=t.t("shop.only_in_claro"))
            return self._claro_view(hero, notice=t.t("claro.no_growth"))
        if action_id.startswith("sellg:"):
            return self._sell_gear(hero, action_id[6:], in_claro or self._sells_gear_here(hero))    # D-101: 🔨 Herrería
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
        if action_id == "assault":                      # D-112: ⚔️ Asaltar the enemy camp of this zone (a fight by hand)
            return self._assault(hero)
        if action_id == "infiltrate":                   # D-112: 🕵️ Infiltrarse (🧭 Explorador rank 30)
            return self._infiltrate(hero)
        if action_id == "hunt":                         # D-106: 🧭 Explorar → 🏹 Cazar (the hunt screen)
            return self._hunt_view(hero)
        if action_id == "prey":                         # D-106: 🏹 Buscar presa / 🏹 Otra presa: a fight right away
            return self._hunt(hero)
        if action_id == "huntparty":                    # D-106: call your camp's hunting party here
            return self._call_hunt_party(hero)
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
            # a remembered place, or an enemy camp the hero sees on its 🗺️ Mapa (D-112: ⛺ Ir al campamento)
            if not (hero.remembers(gx, gy) or self._ecamp_visible(hero, gx, gy)) or (gx, gy) == (hero.x, hero.y):
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

    def _step_cost(self, kind: str) -> int:
        """Energy of one step of a batch: 1 to explore or gather (energy.per_*), hunt.energy for a prey (D-108, D-114)."""
        if kind == "hunt":
            return int(self._hunt_cfg()["energy"])
        return int(self.content.balance["energy"][f"per_{kind}"])

    def _step_minutes(self, kind: str) -> float:
        """Minutes of one step of a batch: explore/gather minutes, hunt.batch_minutes for a prey (D-114)."""
        if kind == "hunt":
            return self._hunt_cfg()["batch_minutes"]
        return self.content.balance[kind]["minutes"]

    def _amount_view(self, hero: Hero, kind: str, page: int) -> View:
        """Choose how much energy to spend in a row (5, 10, 20, 40 or all) — or cancel (D-87).

        [ES]
        Qué hace: la pantalla "¿cuánta energía gastas?" de 🔎 Explorar, 🪓 Recolectar y, con ⚔️ Peleas automáticas, de
        🏹 Cazar en lote (D-114: hunt.batch, cada presa cuesta hunt.energy). Cada botón dice la energía y el tiempo
        estimado ("⚡ 10 · ⏱️ 1 h 40 min"); 4 botones como mucho, con ▶️ Más / ◀️ Volver. Dice además qué pasa si sale una
        pelea (⚙️ Opciones). Con un ⛺ campamento enemigo en pie en la zona (D-112) no se explora ni se recolecta: vuelve a
        🧭 Explorar con el aviso, sin gastar nada.
        La llaman: los botones 🔎 Explorar, 🪓 Recolectar y 🏹 Cazar en lote (acción "prey" en automático), y "amt:".
        Si cambia, afecta: tests/test_service.py, tests/test_resources.py, tests/test_options.py y el tope de 4 botones.
        """
        t = self.texts
        if kind not in BATCH_KINDS:
            return self._explore_menu(hero)
        camp_block = self._ecamp_block_line(hero) if kind in ("explore", "gather") else None
        if camp_block:                                  # D-112: an enemy camp stands here (nothing is spent)
            return self._explore_menu(hero, notice=camp_block)
        back = "hunt" if kind == "hunt" else "explore_menu"
        if kind == "hunt":
            blocked = self._hunt_batch_blocker(hero)
            if blocked:
                return self._hunt_view(hero, notice=blocked)
        zone = self._zone(hero.x, hero.y)
        if kind == "explore" and self._explore_target(hero) is None:
            return self._explore_menu(hero, notice=t.t("explore.already_full"))
        blocked = self._gather_blocked(hero, zone) if kind == "gather" else None
        if blocked:
            return self._explore_menu(hero, notice=blocked)
        per = self._step_cost(kind)
        if hero.energy < per:
            notice = self._no_energy_notice(hero)
            return self._hunt_view(hero, notice=notice) if kind == "hunt" else self._explore_menu(hero, notice=notice)
        minutes = self._step_minutes(kind)
        step = self._seconds(minutes)
        top = hero.energy - hero.energy % per          # the most energy whole steps can use (all of it, but for a prey)

        def total(n: int) -> str:                    # owner's request: every choice shows its estimated total time
            return self._fmt_duration(step * (n // per))

        body = [t.t(f"batch.ask_{kind}", minutes=minutes, energy=per), t.t("batch.energy", energy=hero.energy),
                t.t("batch.estimate_hunt" if kind == "hunt" else "batch.estimate", step=total(per), n=top, k=top // per,
                    total=total(top))]
        if kind == "gather":
            body.append(t.t("batch.space", used=self._bag_used(hero), cap=self._bag_cap(hero)))
        elif kind == "explore":
            body += self._explore_progress_lines(hero)
        body += self._auto_lines(hero, kind)            # D-114: what happens if a fight comes up (⚙️ Opciones)
        body.append(t.t("batch.cancel_hint"))
        batch = self._hunt_cfg()["batch"] if kind == "hunt" else self.content.balance["energy"]["batch"]
        options = [n for n in batch if n <= hero.energy]
        pages = [options[:2], options[2:]]
        page = page % 2
        actions = [Action(id=f"do:{kind}:{n}", label=t.t("batch.button", n=n, time=total(n))) for n in pages[page]]
        if page == 0:
            if len(options) > 2 or top not in options:
                actions.append(Action(id=f"amt:{kind}:1", label=t.t("batch.more")))
            actions.append(Action(id=back, label=t.t("batch.cancel")))
        else:
            if top not in options:
                actions.append(Action(id=f"do:{kind}:max", label=t.t("batch.max", n=top, time=total(top))))
            actions.append(Action(id=f"amt:{kind}:0", label=t.t("batch.back")))
        if not options:
            actions = [Action(id=f"do:{kind}:max", label=t.t("batch.max", n=top, time=total(top))),
                       Action(id=back, label=t.t("batch.cancel"))]
        return View(kind="batch", title=t.t(f"batch.title_{kind}"), body=body, actions=actions[:4])

    def _start_batch(self, hero: Hero, kind: str, amount: str) -> View:
        """Start a batch: pay the first step and set the timer; a hunt batch only with ⚔️ automatic fights (D-114).

        [ES]
        Qué hace: empieza el lote elegido ("do:explore:10", "do:gather:max", "do:hunt:20"): cobra la energía de la primera
        vuelta (1 ⚡; una presa, hunt.energy) y deja el reloj; las demás vueltas se cobran al empezar cada una. Si algo lo
        impide (mochila llena, zona agotada, nada por explorar, sin energía, un ⛺ campamento enemigo en pie en la zona (D-112);
        para cazar: ✋ Manual, sin presas, malherido o con la vida bajo el límite de ⚙️ Opciones) avisa y no cobra nada.
        La llaman: los botones de cantidad de _amount_view. Si cambia, afecta: el gasto de energía de todos los lotes.
        """
        t = self.texts
        if kind not in BATCH_KINDS:
            return self._explore_menu(hero)
        camp_block = self._ecamp_block_line(hero) if kind in ("explore", "gather") else None
        if camp_block:                                  # D-112: an enemy camp stands here (nothing is spent)
            return self._explore_menu(hero, notice=camp_block)
        if kind == "hunt":
            blocked = self._hunt_batch_blocker(hero)
            if blocked:
                return self._hunt_view(hero, notice=blocked)
        per = self._step_cost(kind)
        n = hero.energy if amount == "max" else (int(amount) if amount.isdigit() else 0)
        steps = min(n, hero.energy) // per
        zone = self._zone(hero.x, hero.y)
        blocked = self._gather_blocked(hero, zone) if kind == "gather" else None
        if blocked:
            return self._explore_menu(hero, notice=blocked)   # no energy spent for nothing
        if steps < 1 or not self._spend_energy(hero, kind, per):
            notice = self._no_energy_notice(hero)
            return self._hunt_view(hero, notice=notice) if kind == "hunt" else self._explore_menu(hero, notice=notice)
        if kind == "explore" and self._explore_target(hero) is None:
            hero.energy += per
            return self._explore_menu(hero, notice=t.t("explore.already_full"))
        seconds = self._seconds(self._step_minutes(kind))
        hero.activity = {"kind": kind, "until": self.clock.now() + seconds, "left": steps - 1, "total": steps, "done": 0, "got": {}, "log": []}
        return self._activity_view(hero, notice=t.t(f"batch.started_{kind}", n=steps, time=self._fmt_duration(seconds * steps)))

    def _gather_blocked(self, hero: Hero, zone: Zone) -> str | None:
        """The notice of why gathering here cannot start (full backpack, D-90, or depleted zone), else None."""
        if self._bag_full(hero):
            return self._bag_full_line(hero)
        stock = self._stock(zone.x, zone.y)
        if all(level < self.content.balance["stock"]["min_yield"] for level in stock.values()):
            return self.texts.t("batch.reason.depleted")
        return None

    def _stop_batch(self, hero: Hero) -> View:
        """Cancel the batch: the step in progress gives its energy back (D-87)."""
        activity = hero.activity or {}
        if activity.get("kind") not in BATCH_KINDS:
            return self._main_view(hero)
        hero.energy += self._step_cost(activity["kind"])
        hero.activity = None
        lines = self._batch_summary(hero, activity, "stopped")
        if activity["kind"] == "hunt":
            return self._hunt_view(hero, notice=self._join(lines))
        return self._explore_menu(hero, notice=self._join(lines))

    def _batch_summary(self, hero: Hero, activity: dict[str, Any], reason: str, **values: Any) -> list[str]:
        """The one message at the end of a batch (D-87): what it gave, its automatic fights (D-114) and why it stopped.

        [ES]
        Qué hace: arma el resumen del final del lote: lo recolectado o explorado, la experiencia, las peleas automáticas
        (cuántas ganó y perdió, lo que dieron y el botín, D-114), lo que pasó en el camino y por qué terminó. `values` va al
        texto del motivo (por ejemplo, el % de vida de ⚙️ Opciones).
        La llaman: _settle (al terminar o cortarse el lote) y _stop_batch.
        Si cambia, afecta: el único aviso que manda el bot al terminar cada lote.
        """
        t = self.texts
        kind = activity["kind"]
        lines = []
        if activity.get("done") and kind != "hunt":     # D-114: a hunting batch is only its fights (the lines below)
            if kind == "gather":
                lines.append(t.t("batch.gathered", n=activity["done"], items=self._item_list(activity.get("got", {}))))
                if activity.get("xp"):
                    lines.append(t.t("batch.xp_gather", xp=activity["xp"]))
                if activity.get("trade"):                 # D-109: what each gathering profession earned
                    lines.append(self._trade_summary(activity["trade"]))
            else:
                zone = self._zone(hero.x, hero.y)
                lines.append(t.t("batch.explored_done", n=activity["done"], pct=self._explored_pct(hero, zone.x, zone.y)))
                if activity.get("target", f"{zone.x}:{zone.y}") != f"{zone.x}:{zone.y}":     # it went on around you (D-107)
                    lines.append(self._around_line(hero))
                if activity.get("got"):
                    lines.append(t.t("batch.found", items=self._item_list(activity["got"])))
                if activity.get("coins"):
                    lines.append(t.t("batch.coins", coins=self._money(activity["coins"])))
                if activity.get("xp"):
                    lines.append(t.t("batch.xp", xp=activity["xp"]))
                if activity.get("trade"):                 # D-112: what the 🧭 Explorador earned
                    lines.append(self._trade_summary(activity["trade"]))
        lines += self._auto_summary(activity)           # D-114: ⚔️ N peleas automáticas: N ganadas...
        lines += activity.get("log", [])
        if reason not in ("done", "full_explored"):        # reaching 100 % already has its own line
            lines.append(t.t(f"batch.reason.{reason}", **values))
        return lines

    def _continue_batch(self, hero: Hero, activity: dict[str, Any], until: float) -> str | None:
        """After a finished step: start the next one, or say why the batch stops."""
        kind = activity["kind"]
        zone = self._zone(hero.x, hero.y)
        if activity["left"] <= 0:
            return "done"
        if kind in ("explore", "gather") and self._ecamp_standing(hero.x, hero.y):
            return "enemy_camp"                         # D-112: a camp came up here (a new day): the next round waits
        if kind == "explore" and self._explore_target(hero) is None:
            return "full_explored"
        if kind == "gather" and self._bag_full(hero):
            return "bag_full"
        if not self._spend_energy(hero, kind, self._step_cost(kind)):
            return "energy"
        activity["left"] -= 1
        activity["until"] = until + self._seconds(self._step_minutes(kind))
        hero.activity = activity
        return None

    # ------------------------------------------------------------------ zone resources and exploration (D-87)

    def _bag_cap(self, hero: Hero | None = None) -> int:
        """Backpack space: the base, plus the 🪓 Leñador's perk (D-111) when a hero is given."""
        base = self.content.balance["hero"]["backpack_capacity"]
        return base + (int(self._perks(hero)["bag"]) if hero is not None else 0)

    def _bag_used(self, hero: Hero) -> int:
        return sum(hero.backpack.values())

    def _bag_full(self, hero: Hero) -> bool:
        """True when the backpack is at or over its space: then gathering and buying wait (D-90).

        [ES]
        Qué hace: dice si la mochila llegó a su espacio (60) o lo pasó. Con la mochila llena no se recolecta ni se
        compra hasta vender o usar cosas; lo que se encuentra igual entra (D-90, provisional).
        La llaman: _gather_blocked, _continue_batch, _gather_step, _buy, _shop_view y _bag_view.
        Si cambia, afecta: cuándo se corta recolectar y cuándo el mercader no vende (balance.yaml hero.backpack_capacity).
        """
        return self._bag_used(hero) >= self._bag_cap(hero)

    def _bag_full_line(self, hero: Hero) -> str:
        """🎒 Mochila llena (63/60): sell or use things to gather or buy again (D-90)."""
        return self.texts.t("bag.full_line", used=self._bag_used(hero), cap=self._bag_cap(hero))

    def _bag_add(self, hero: Hero, item_id: str, count: int) -> int:
        """Put found items in the backpack, even beyond its space: what you find is never lost (D-90).

        [ES]
        Qué hace: guarda en la mochila lo que encuentras (hallazgos de explorar), aunque pase del espacio.
        La llaman: _explore_step y _gather_step (recolectar se corta antes, en el tope).
        Si cambia, afecta: si los hallazgos se pierden con la mochila llena (D-90 dice que nunca).
        """
        count = max(0, count)
        if count:
            hero.backpack[item_id] = hero.backpack.get(item_id, 0) + count
        return count

    def _zone_resources(self, x: int, y: int) -> dict[str, float]:
        zone = self._zone(x, y)
        return zone_resources(self.world_seed, x, y, zone.biome, self.content.balance, self.content.biomes)

    def _stock(self, x: int, y: int) -> dict[str, float]:
        """How much is left of each resource in a zone (1.0 = full), regenerating with time (faster with a camp's ⛲ Pozo, D-101)."""
        cfg = self.content.balance["stock"]
        data = self.store.get("stock", f"{x}:{y}") or {}
        hours = (self.clock.now() - data.get("at", self.clock.now())) / (3600 * self.time_scale)
        levels = data.get("levels", {})
        ref = self.store.get("territory", f"{x}:{y}") if levels else None
        regen = cfg["regen_per_hour"] * (1 + (self._effect_at(ref["camp"], "stock_regen") if ref else 0.0))
        return {res: min(1.0, levels.get(res, 1.0) + hours * regen) for res in self._zone_resources(x, y)}

    def _explored_pct(self, hero: Hero, x: int, y: int) -> int:
        return hero.exploration.get(f"{x}:{y}", 0)

    def _around_line(self, hero: Hero) -> str:
        """🔭 Alrededor: 3/8 zonas al 100 % (D-107)."""
        around = self._explore_around(hero)
        done = sum(1 for x, y in around if self._explored_pct(hero, x, y) >= 100)
        return self.texts.t("batch.around", done=done, total=len(around))

    def _explore_progress_lines(self, hero: Hero) -> list[str]:
        """How far exploring goes from here: your zone's %, then the zone around you being studied (D-107)."""
        t = self.texts
        lines = [t.t("batch.explored", pct=self._explored_pct(hero, hero.x, hero.y))]
        target = self._explore_target(hero)
        if target and target != (hero.x, hero.y):
            zone = self._zone(*target)
            lines += [self._around_line(hero),
                      t.t("batch.around_next", name=self._zone_name(zone), x=zone.x, y=zone.y, pct=self._explored_pct(hero, *target))]
        return lines

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
        boost = self._perks(hero)["potion" if item.get("kind") == "potion" else "bandage"] if item.get("kind") in ("potion", "bandage") else 0.0
        healed = min(stats["max_hp"] - hero.hp, round(stats["max_hp"] * item["heal"] * (1 + boost)))     # D-111
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
        body += self._ecamp_zone_lines(zone)            # D-112: ⛺ an enemy camp here (or its ruins today)
        body += self._zone_players_lines(hero, zone)    # D-96: who else is here now (nothing if nobody)
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
            if self._ecamp_standing(dest.x, dest.y):     # D-112: everyone sees a camp next door
                where += t.t("ecamp.route_mark")
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
                    t.t("travel.remaining", time=remaining), t.t("batch.space", used=self._bag_used(hero), cap=self._bag_cap(hero))]
            title = t.t("gather.title")
        elif activity.get("kind") == "rest":
            body = [t.t("inn.in_progress"), t.t("travel.remaining", time=remaining)]
            title = t.t("inn.title")
        elif activity.get("kind") == "hunt":            # D-114: hunting batch, automatic fights
            body = [t.t("hunt.batch_in_progress"), t.t("hunt.batch_progress", done=activity.get("done", 0) + 1, total=activity.get("total", 1)),
                    t.t("travel.remaining", time=remaining)]
            title = t.t("hunt.title")
        else:
            zone = self._zone(hero.x, hero.y)
            body = [t.t("explore.in_progress"), t.t("batch.progress", done=activity.get("done", 0) + 1, total=activity.get("total", 1)),
                    t.t("travel.remaining", time=remaining)] + self._explore_progress_lines(hero)
            title = t.t("explore.title")
        if activity.get("kind") in BATCH_KINDS:            # D-114: the automatic fights so far, and what happens if one comes up
            body += self._auto_summary(activity)[:1] + self._auto_lines(hero, activity.get("kind"))
        if activity.get("kind") in PRESENT_BUSY:          # D-96: 📍 Zona while busy in the zone also shows who is here
            body += self._zone_players_lines(hero, self._zone(hero.x, hero.y))
        body += ["", self._status_line(hero), t.t("activity.offline_ok")]
        actions = [Action(id="refresh", label=t.t("menu.refresh"))]
        if activity.get("kind") in BATCH_KINDS:
            actions.append(Action(id="stop", label=t.t("batch.stop")))
        return View(kind="activity", title=title, body=body, actions=actions, notice=notice)

    # ------------------------------------------------------------------ players in the zone (D-96, provisional)

    def _presence_note(self, hero: Hero) -> None:
        """Make sure the hero is listed in the presence record of its zone.

        One read per button; a write only when the hero is missing (just arrived, or pruned after being idle).
        Whether it really counts as present is decided on read, from the hero's own record.

        [ES]
        Qué hace: anota al héroe en el registro de presencia de su zona (espacio "presence", clave "x:y").
        Lee una vez por botón y solo escribe si falta (acaba de llegar o se lo quitó por estar inactivo).
        La llaman: act() en cada botón (después de _settle) y _presence_move al llegar a una zona.
        Si cambia, afecta: quién aparece en 👥 de 📍 Zona y con quién te cruzas al explorar o recolectar.
        """
        key = f"{hero.x}:{hero.y}"
        record = self.store.get("presence", key) or {"seen": {}}
        if hero.id in record.get("seen", {}):
            return
        record.setdefault("seen", {})[hero.id] = self.clock.now()
        self.store.put("presence", key, record)

    def _presence_move(self, hero: Hero, old_x: int, old_y: int) -> None:
        """On arrival: take the hero out of the zone it left and note it in the new one.

        [ES]
        Qué hace: al llegar a una zona, quita al héroe del registro de la zona que dejó y lo anota en la nueva
        (aunque el jugador tenga el chat cerrado: los tramos de una ruta llegan solos). Un registro vacío se borra.
        La llama: _arrive. Si cambia, afecta: que alguien siga "apareciendo" en una zona que ya dejó.
        """
        if (old_x, old_y) != (hero.x, hero.y):
            key = f"{old_x}:{old_y}"
            old = self.store.get("presence", key)
            if old and old.get("seen", {}).pop(hero.id, None) is not None:
                if old["seen"]:
                    self.store.put("presence", key, old)
                else:
                    self.store.delete("presence", key)
        self._presence_note(hero)

    def _zone_players(self, x: int, y: int, exclude: str | None = None) -> list[dict[str, Any]]:
        """Other players present in zone (x, y) now, most recently seen first; prunes the record on the way.

        Present = the hero is in that zone AND (pressed a button in the last presence.minutes, OR is
        exploring, gathering or sleeping there right now). Heroes who left, no longer exist or are idle
        for longer are taken out of the record (they come back with their next button).

        [ES]
        Qué hace: lista a los otros jugadores que están ahora en la zona, con lo que hacen (nombre, clase, nivel,
        actividad); el primero es el que jugó hace menos. "Está" = su héroe sigue en esa zona Y tocó un botón en
        los últimos presence.minutes (Hero.seen_at, que marca _mark_seen) O está explorando, recolectando o
        durmiendo ahí. Al leer, saca del registro a quien se fue, ya no existe o lleva más tiempo inactivo.
        Nunca saca a "exclude" (quien mira): su ficha guardada todavía no tiene el botón de ahora.
        La llaman: _zone_players_lines (📍 Zona y la pantalla de actividad) y _cross_paths.
        Si cambia, afecta: quién ve a quién; nada de reglas (sin premio, sin pelea, D-96).
        """
        key = f"{x}:{y}"
        record = self.store.get("presence", key)
        if not record or not record.get("seen"):
            return []
        t = self.texts
        cutoff = self.clock.now() - self._seconds(self.content.balance["presence"]["minutes"])
        players: list[dict[str, Any]] = []
        gone: list[str] = []
        for account in list(record["seen"]):
            if account == exclude:
                continue
            data = self.store.get("hero", account)
            if not data or (data.get("x"), data.get("y")) != (x, y):
                gone.append(account)
                continue
            kind = "combat" if self.store.get("combat", account) is not None else (data.get("activity") or {}).get("kind") or "idle"
            if data.get("seen_at", 0.0) < cutoff and kind not in PRESENT_BUSY:
                gone.append(account)
                continue
            other = Hero.from_dict(data)
            group = self.content.classes.get(other.class_id, {}).get("group", other.class_id)
            players.append({"id": account, "name": self._banner(other) + self._emblem_name(other), "plain": other.name,   # D-117: emblem
                            "cls": t.t(f"class_group.{group}.name"),
                            "level": other.level, "activity": t.t(f"presence.activity.{kind}"), "seen": other.seen_at})
        if gone:
            for account in gone:
                record["seen"].pop(account, None)
            if record["seen"]:
                self.store.put("presence", key, record)
            else:
                self.store.delete("presence", key)
        players.sort(key=lambda p: -p["seen"])
        return players

    def _zone_players_lines(self, hero: Hero, zone: Zone) -> list[str]:
        """👥 block of the zone screen: up to presence.max_listed players, then "… y N más". Empty if nobody.

        [ES]
        Qué hace: arma las líneas 👥 de 📍 Zona (una por jugador, con su actividad) y "… y N más" si pasan del
        tope presence.max_listed. Si no hay nadie, no muestra nada (pantallas cortas, D-86). No agrega botones.
        La llaman: _zone_view y _activity_view (explorando, recolectando o durmiendo).
        Si cambia, afecta: el largo de 📍 Zona en los tres clientes.
        """
        players = self._zone_players(zone.x, zone.y, exclude=hero.id)
        if not players:
            return []
        t = self.texts
        cap = max(1, int(self.content.balance["presence"]["max_listed"]))
        lines = [t.t("presence.title", n=len(players))]
        lines += [t.t("presence.line", name=p["name"], cls=p["cls"], level=p["level"], activity=p["activity"]) for p in players[:cap]]
        if len(players) > cap:
            lines.append(t.t("presence.more", n=len(players) - cap))
        return lines

    def _cross_paths(self, hero: Hero, zone: Zone, activity: dict[str, Any]) -> list[str]:
        """After an exploring or gathering step with no fight: maybe a "👋 you crossed X" line (flavour only).

        Uses its own deterministic draw (hash of world seed, hero and step end), so the step's Rng and every
        other result stay exactly as before. The same player is crossed at most once per batch.

        [ES]
        Qué hace: tras una vuelta de exploración o recolección sin pelea, con probabilidad presence.cross_chance,
        agrega al resumen "👋 Te cruzaste con Bram (🏰 Guerrero, nivel 2), que andaba 🪓 recolectando." si hay
        alguien en la zona. Solo texto: sin premio, sin pelea, sin PvP, en cualquier zona (también el Claro y los
        campamentos). Usa su propio sorteo fijo, así no cambia ningún otro resultado de la vuelta; a cada jugador
        te lo cruzas una sola vez por lote (activity["met"]).
        La llama: _settle. Si cambia, afecta: solo el texto del resumen del lote.
        """
        if hash_unit(self.world_seed, hero.id, activity["until"], "cross") >= self.content.balance["presence"]["cross_chance"]:
            return []
        met = activity.setdefault("met", [])
        others = [p for p in self._zone_players(zone.x, zone.y, exclude=hero.id) if p["id"] not in met]
        if not others:
            return []
        pick = others[int(hash_unit(self.world_seed, hero.id, activity["until"], "who") * len(others)) % len(others)]
        met.append(pick["id"])
        return [self.texts.t("presence.crossed", name=pick["name"], cls=pick["cls"], level=pick["level"], activity=pick["activity"])]

    # ------------------------------------------------------------------ gathering, camp, tutorial

    def _claro_view(self, hero: Hero, notice: str | None = None) -> View:
        """The Claro: the fixed base camp with the trader and the inn. It never grows (D-98) nor eats (D-95).

        [ES]
        Qué hace: muestra el campamento base, donde empiezan todos: mercader, posada, ⚒️ Oficios (las estaciones
        básicas de refinar y fabricar, D-109), 📜 Tablón (los encargos del día y los personajes del Claro, D-117; tomó el
        lugar de ↩️ Volver: 📍 Zona en el menú de abajo vuelve) y la pista para crecer fundando tu propio campamento.
        El Claro no crece ni se mantiene (D-95, D-98): no tiene obra común.
        La llaman: el botón 🏕️ Campamento estando en el Claro, y los botones viejos de la obra (camp, donate, feed).
        Si cambia, afecta: la primera pantalla de todos los jugadores nuevos (tope de 4 botones, D-75: ya están los 4;
        tests/test_pantry.py y tests/test_service.py miran el orden).
        """
        t = self.texts
        body = [t.t("claro.intro"), t.t("claro.grow_hint"), t.t("claro.trades_hint"), t.t("story.claro_hint"), self._status_line(hero)]
        return View(kind="claro", title=t.t("claro.title"), body=body + self._tutorial_hint(hero),
                    actions=[Action(id="shop", label=t.t("shop.button")),
                             Action(id="inn", label=t.t("inn.button", price=self._money(self._inn_price()))),
                             Action(id="oficios", label=t.t("prof.button")),      # D-109: the Claro has the basic stations
                             Action(id="board", label=t.t("story.button_board"))],  # D-117: the tasks board (📍 Zona in the menu goes back)
                    notice=notice)

    def _settlement(self) -> dict[str, Any]:
        data = self.store.get("settlement", "claro")
        return data or {"stage": 0, "progress": {}, "merit": {}}

    def _inn_price(self) -> int:
        inn = self.content.balance["inn"]
        stage = self._settlement()["stage"]
        return max(1, inn["price"] - stage * self.content.balance["settlement"]["inn_discount_per_stage"])

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

    def _pantry(self, key: str, active: int, eaters: Callable[[], int], ration: float | None = None,
                produce: float = 0.0) -> dict[str, float]:
        """Read a pantry after the lazy consumption and save it. A new one starts with pantry.start_days of food
        for max(active, eaters()) residents; that also covers settlements that existed before the patch.
        `ration` is what each active resident eats per day (default pantry.ration_per_day; less with a 🌾 Granero)
        and `produce` the rations added per day whoever plays (🥬 Huerto), D-101."""
        cfg = self.content.balance["pantry"]
        now = self.clock.now()
        data = self.store.get("pantry", key)
        if data is None:
            rations = cfg["start_days"] * cfg["ration_per_day"] * max(1, active, eaters())
        else:
            days = (now - data.get("at", now)) / self._day_seconds()
            per_day = cfg["ration_per_day"] if ration is None else ration
            rations = pantry_rules.consume(data.get("rations", 0.0), active, days, per_day) + max(0.0, days) * produce
        data = {"rations": float(rations), "at": now}
        self.store.put("pantry", key, data)
        return data

    def _pantry_status(self, key: str, active: int, eaters: Callable[[], int], ration: float | None = None,
                       produce: float = 0.0) -> dict[str, Any]:
        cfg = self.content.balance["pantry"]
        data = self._pantry(key, active, eaters, ration, produce)
        days = pantry_rules.days_left(data["rations"], active, cfg["ration_per_day"] if ration is None else ration)
        return {"key": key, "rations": data["rations"], "active": active, "days": days,
                "state": pantry_rules.state(days, cfg["states"])}

    def _camp_pantry(self, camp: dict[str, Any]) -> dict[str, Any] | None:
        """A player camp's small pantry from pantry.camp_from_level on (None before).

        D-101: a 🌾 Granero cuts what each member eats ("ration_cut") and a 🥬 Huerto adds rations every day
        ("rations_per_day"); both are kept in the result ("cut", "produce") for the pantry lines.
        """
        cfg = self.content.balance["pantry"]
        if camp.get("level", 1) < cfg["camp_from_level"]:
            return None
        cut = min(0.9, self._camp_effect(camp, "ration_cut"))
        produce = self._camp_effect(camp, "rations_per_day")
        status = self._pantry_status(f"{camp['x']}:{camp['y']}", self._camp_active(camp), lambda: len(camp.get("members", [])),
                                     cfg["ration_per_day"] * (1 - cut), produce)
        status["cut"], status["produce"] = cut, produce
        return status

    def _camp_starving(self, camp: dict[str, Any]) -> bool:
        """True if the camp has a pantry and it is empty (hambruna): then it cannot grow."""
        pantry = self._camp_pantry(camp)
        return pantry is not None and pantry["state"] == "hambruna"

    def _pantry_line(self, pantry: dict[str, Any]) -> str:
        t = self.texts
        return t.t("pantry.line", state=t.t(f"pantry.state.{pantry['state']}"), rations=int(pantry["rations"]), days=pantry["days"])

    def _pantry_lines(self, pantry: dict[str, Any]) -> list[str]:
        t = self.texts
        lines = [self._pantry_line(pantry), t.t("pantry.eaters", n=pantry["active"])]
        if pantry.get("cut"):                                   # D-101: 🌾 Granero
            lines.append(t.t("upgrades.granary_line", pct=round(pantry["cut"] * 100)))
        if pantry.get("produce"):                               # D-101: 🥬 Huerto
            lines.append(t.t("upgrades.garden_line", n=int(pantry["produce"])))
        return lines + [t.t("pantry.how")]

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
        smoked = int(self._camp_effect(camp, "meat_bonus")) * given.get("carne", 0)   # D-101: 🍖 Ahumadero
        rations += smoked
        self._add_rations(f"{camp['x']}:{camp['y']}", rations)
        lines, _ = self._food_reward(hero, given, rations)
        lines += self._story_event(hero, "feed", rations=rations)     # D-117: camp tasks
        if smoked:
            lines.insert(1, t.t("upgrades.smoked", n=smoked))
        return self._camp_here_view(hero, notice="\n".join(lines))

    def _xp_mult(self, hero: Hero) -> float:
        """Experience accelerator bought with gems (D-43, D-80): ×1.5 while active."""
        boost = self.content.balance["currency"]["gem_shop"]["xp_boost"]
        return boost["xp_mult"] if hero.xp_boost_until > self.clock.now() else 1.0

    def _zone_xp(self, base: float, level: int) -> int:
        """Experience of an action at a zone or enemy level: base × (1 + scale × (level − 1)), like every kill (D-108).

        [ES]
        Qué hace: escala la experiencia con el nivel, igual para matar bichos y para recolectar, así cada camino
        sigue rindiendo en los niveles altos (hero.xp_level_scale, 15 % más por nivel).
        La llaman: _gather_step, el combate (_end_combat y el Guardián).
        Si cambia, afecta: el ritmo hasta el nivel 100 de todos los caminos (diseno/03-personaje/progresion.md).
        """
        return int(base * (1 + self.content.balance["hero"]["xp_level_scale"] * (level - 1)))

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
        Con la mochila llena (D-90) muestra la línea de mochila llena; comprar se rechaza en _buy sin cobrar.
        """
        t = self.texts
        shop = self.content.balance["shop"]
        body = [t.t("shop.intro"), t.t("hero.gold_line", gold=self._money(hero.gold)), ""]
        actions = []
        for item_id in shop["sells"]:
            item = self.content.items[item_id]
            price = self._shop_price(hero, item_id)              # D-117: 🕳️ Huérfano de las Ruinas pays 10 % less
            body.append(t.t("shop.buy_line", emoji=item["emoji"], item=t.t(item["name_key"]), price=self._money(price)))
            cap = shop.get("weekly_cap", {}).get(item_id)
            if cap is not None:                                  # D-125: 20 🥖 provisions a week
                body.append(t.t("shop.cap_line", left=max(0, cap - self._shop_week(hero).get(item_id, 0)), n=cap))
            actions.append(Action(id=f"buy:{item_id}", label=t.t("shop.buy_button", emoji=item["emoji"], price=self._money(price))))
        actions = actions[:3]
        sellable = {i: n for i, n in hero.backpack.items()      # food stays: it feeds the pantry (D-93)
                    if self.content.items.get(i, {}).get("kind") == "material" and not self.content.items[i].get("food")
                    and not self.content.items[i].get("keep")}       # refined goods and rares are sold one by one (D-109)
        if sellable:
            total = sum(max(1, int(self.content.items[i]["price"] * shop["sell_ratio"])) * n for i, n in sellable.items())
            body.append(t.t("shop.sell_line", items=self._item_list(sellable), total=self._money(total)))
            actions.append(Action(id="sell:all", label=t.t("shop.sell_all_button", total=self._money(total))))
        if self._bag_full(hero):  # D-90: buying waits until there is room again
            body += ["", self._bag_full_line(hero)]
        if len(actions) < 4:     # 4 buttons at most (D-75); without room, 🏕️ Campamento in the menu goes back to the same place
            actions.append(Action(id="claro", label=t.t("menu.back")))
        return View(kind="shop", title=t.t("shop.title"), body=body, actions=actions, notice=notice)

    def _buy(self, hero: Hero, item_id: str) -> View:
        t = self.texts
        if item_id not in self.content.balance["shop"]["sells"]:
            return self._shop_view(hero)
        item = self.content.items[item_id]
        if self._bag_full(hero):
            return self._shop_view(hero, notice=self._bag_full_line(hero))   # D-90: sell or use things first (never charged)
        cap = self.content.balance["shop"].get("weekly_cap", {}).get(item_id)
        bought = self._shop_week(hero)
        if cap is not None and bought.get(item_id, 0) >= cap:      # D-125: never charged once the week's cap is reached
            return self._shop_view(hero, notice=t.t("shop.weekly_cap", item=t.t(item["name_key"]), n=cap))
        price = self._shop_price(hero, item_id)                  # D-117: the origin's discount, if any
        if hero.gold < price:
            return self._shop_view(hero, notice=t.t("shop.no_gold"))
        hero.gold -= price
        hero.backpack[item_id] = hero.backpack.get(item_id, 0) + 1
        if cap is not None:
            bought[item_id] = bought.get(item_id, 0) + 1
            self.store.put("shop_week", hero.id, {"week": self._today() // 7, "bought": bought})
        self._refill_belt(hero)
        return self._shop_view(hero, notice=t.t("shop.bought", item=t.t(item["name_key"])))

    def _shop_week(self, hero: Hero) -> dict[str, int]:
        """What the hero bought this real week from the capped items (balance.yaml shop.weekly_cap), {item_id: n}.

        [ES] D-125: cuenta las compras con tope de la semana (store "shop_week", clave el id del héroe). La semana es
        _today() // 7 (el mismo corte de día que la despensa y el tablón); al cambiar de semana empieza de cero.
        La usan _buy (rechaza sin cobrar al llegar al tope) y _shop_view (muestra cuántas quedan).
        """
        record = self.store.get("shop_week", hero.id) or {}
        if record.get("week") != self._today() // 7:
            return {}
        return dict(record.get("bought", {}))

    def _sell(self, hero: Hero, item_id: str) -> View:
        t = self.texts
        if item_id == "all":
            total, sold = 0, {}
            for i, n in list(hero.backpack.items()):
                item = self.content.items.get(i, {})
                if item.get("kind") == "material" and not item.get("food") and not item.get("keep") and n > 0:
                    total += max(1, int(item["price"] * self.content.balance["shop"]["sell_ratio"])) * n
                    sold[i] = n
                    del hero.backpack[i]
            if not sold:
                return self._shop_view(hero)
            total, trade = self._merchant_sale(hero, total)     # D-116: 💱 Comercio
            hero.gold += total
            lines = [t.t("shop.sold_all", items=self._item_list(sold), total=self._money(total))] + trade + self._tutorial(hero, "sell")
            lines += self._story_event(hero, "sell", n=sum(sold.values()), coins=total)          # D-117
            return self._shop_view(hero, notice="\n".join(lines))
        item = self.content.items.get(item_id, {})
        if item.get("kind") != "material" or hero.backpack.get(item_id, 0) <= 0:
            return self._shop_view(hero)
        price = max(1, int(item["price"] * self.content.balance["shop"]["sell_ratio"]))
        hero.backpack[item_id] -= 1
        if hero.backpack[item_id] <= 0:
            del hero.backpack[item_id]
        price, trade = self._merchant_sale(hero, price)         # D-116: 💱 Comercio
        hero.gold += price
        lines = [t.t("shop.sold", item=t.t(item["name_key"]), price=self._money(price))] + trade + self._tutorial(hero, "sell")   # D-98: the tutorial step that replaced donating
        lines += self._story_event(hero, "sell", n=1, coins=price)                             # D-117
        return self._shop_view(hero, notice="\n".join(lines))

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
        """🧭 Explorar: explore, gather, hunt and the map (4 buttons at most, D-75).

        [ES]
        Qué hace: el menú de la zona: 🔎 Explorar, 🪓 Recolectar, 🏹 Cazar (D-106) y 🗺️ Mapa. 📒 Lugares se mudó adentro
        de 🗺️ Mapa para dejarle lugar a 🏹 Cazar. En la guarida del Guardián (D-82) ⚔️ Desafiar al Guardián toma el lugar
        de recolectar y no hay 🏹 Cazar: quedan 3 botones. Con un ⛺ campamento enemigo en pie en la zona (D-112) el menú es
        el del campamento (_ecamp_menu: ⚔️ Asaltar y 🕵️ Infiltrarse en lugar de explorar y recolectar); si cayó hoy, una
        línea lo dice.
        La llaman: el botón 🧭 Explorar del menú fijo y las acciones de explorar, recolectar y cazar cuando rechazan algo.
        Si cambia, afecta: tests/test_boss.py, tests/test_hunt.py y tests/test_enemy_camps.py (los botones),
        tests/test_buttons.py (tope de 4) y la consola (adapters/cli/play.py numera estos botones).
        """
        t = self.texts
        zone = self._zone(hero.x, hero.y)
        camp = self._ecamp(zone.x, zone.y)
        if camp and not camp["destroyed"]:
            return self._ecamp_menu(hero, camp, notice=notice)
        explore_time = self._fmt_duration(self._seconds(self.content.balance["explore"]["minutes"]))
        gather_time = self._fmt_duration(self._seconds(self.content.balance["gather"]["minutes"]))
        body = [t.t("zone.header", name=self._zone_name(zone), biome=self._biome_label(zone)), t.t("explore.menu_intro"),
                self._resources_line(hero, zone.x, zone.y), t.t("batch.space", used=self._bag_used(hero), cap=self._bag_cap(hero))]
        if camp:                                        # D-112: the camp here fell today
            body.append(t.t("ecamp.ruins", name=camp["destroyed"].get("name", "?")))
        body += self._tutorial_hint(hero)
        actions = [Action(id="explore", label=t.t("zone.explore_button", time=explore_time)),
                   Action(id="gather", label=t.t("gather.button", time=gather_time)),
                   Action(id="hunt", label=t.t("hunt.button")),          # D-106; 📒 Lugares lives in 🗺️ Mapa now
                   Action(id="map", label=t.t("menu.map"))]
        if self._is_lair(zone.x, zone.y):
            # The lair (D-82): the challenge takes the gather slot and there is no prey but the Guardian (D-106).
            body += ["", self._guardian_ready_line(hero), t.t("guardian.no_gather")]
            actions = [actions[0], Action(id="boss", label=t.t("guardian.button")), actions[3]]
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
        Qué hace: muestra el campamento de la zona. Botones de un miembro (_camp_member_actions, 4 como máximo):
        ⬆️ Agrandar, 🌾 Aportar comida (desde nivel 3), 🛡️ Gremio (ahí están los miembros, ✏️ Renombrar y 🚪 Salir,
        D-97) y 🔨 Mejoras (D-101); sin despensa, también ↩️ Volver. Muestra las mejoras construidas y la 🛡️ Defensa
        (también a los visitantes).
        La llaman: el botón 🏕️ Campamento fuera del Claro y casi todas las acciones de campamento.
        Si cambia, afecta: tests/test_camps.py, tests/test_pantry.py, tests/test_guilds.py y tests/test_camp_upgrades.py
        (orden de los botones).
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
            if hero.id in camp["members"]:
                body += [t.t("camps.you_member"), t.t("camps.grow_cost", items=self._grow_cost_text(level)),
                         t.t("upgrades.camp_line", n=len(self._built(camp)), defense=self._camp_defense(camp))]   # D-101
                pantry = self._camp_pantry(camp)          # D-93: from level 3 (aldea), a small pantry
                if pantry:
                    body += self._pantry_lines(pantry) + ([t.t("pantry.famine_camp")] if pantry["state"] == "hambruna" else [])
                body += self._raid_lines(camp)            # D-99: the next raid, or the one going on
                # D-97: 🛡️ Gremio holds the members, rename and leave; D-99: 🛡️ Defender; D-101: 🔨 Mejoras (4 at most)
                actions = self._camp_member_actions(camp, hero, pantry)
            else:
                rel = camp["relations"].get(hero.id)
                body += [t.t("upgrades.defense", n=self._camp_defense(camp)), t.t(f"camps.relation.{rel or 'unknown'}")]
                actions = []
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
                                      "level": 1, "zones": [[hero.x, hero.y]], "next_raid_at": self.clock.now() + self._raid_interval()})
        self.store.put("territory", key, {"camp": key})
        hero.camp = key
        notice = t.t("camps.founded", name=name, x=hero.x, y=hero.y)
        story = self._story_event(hero, "camp", name=name)            # D-117: the journal (and any mission that asks for a camp)
        if story:
            notice += "\n" + "\n".join(story)
        if self._raid_cfg()["from_level"] <= 1:      # D-105: waves start with the camp, and the founder is told so
            notice += "\n" + t.t("raids.founded_warning", n=self._raid_cfg()["per_week"])
        return self._camp_here_view(hero, notice=notice)

    def _members_cap(self, camp: dict[str, Any]) -> int:
        """How many members fit: base + per level (D-84), or the guild's capacity if bigger (D-97).

        [ES]
        Qué hace: da el cupo del campamento: la cuenta de siempre (camps.members_base + members_per_level por
        nivel) o, si tiene gremio y es mayor, el cupo del nivel del gremio (guild.levels). Crear el gremio nunca
        baja el cupo, y nunca se saca a nadie.
        La llaman: la pantalla del campamento y del gremio, _ask_join y _answer_join.
        Si cambia, afecta: quién puede entrar a cada campamento y el mínimo de miembros para castillo.
        """
        cfg = self.content.balance["camps"]
        base = cfg["members_base"] + (camp.get("level", 1) - 1) * cfg["members_per_level"]
        guild = self.store.get("guild", f"{camp['x']}:{camp['y']}")
        if guild:              # the guild only adds room: creating it never lowers the cap
            base = max(base, guild_rules.capacity(self.content.balance["guild"]["levels"], guild["level"]))
        return base + int(self._camp_effect(camp, "members"))      # D-101: 🛖 Cabañas add room on top

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

    def _grow_chests(self, level: int) -> int:
        """🪎 chests that growing a camp from `level` costs (D-92, provisional): 0 below camps.chests_from_level,
        then chests_per_level × (level − chests_from_level + 1): 6→7 asks 1, 7→8 asks 2, 8→9 asks 3.

        [ES]
        Qué hace: dice cuántos cofres pide agrandar un campamento desde su nivel actual (desde el 6).
        La llaman: _grow_cost_text, _grow_view y _grow_camp.
        Si cambia, afecta: el ritmo de los campamentos hasta ciudad y castillo, y cuántas bolsas salen del juego
        (balance.yaml camps.chests_from_level y chests_per_level; tests/test_backpack.py).
        """
        cfg = self.content.balance["camps"]
        start = cfg.get("chests_from_level")
        if start is None or level < start:
            return 0
        return int(cfg.get("chests_per_level", 1)) * (level - start + 1)

    def _grow_cost_text(self, level: int) -> str:
        """The materials of growing from `level`, plus its 🪎 chests when it asks for them (D-92)."""
        text = self._item_list(self._grow_cost(level))
        chests = self._grow_chests(level)
        return text + (" · " + self.texts.t("camps.chest_cost", n=chests) if chests else "")

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
        body = [t.t("camps.grow_intro", items=self._grow_cost_text(level))]
        if self._grow_chests(level):     # D-92: from level 6 growing also costs chests
            body.append(t.t("camps.chests_have", n=hero.chests))
        castle = self._castle_needs(camp)      # D-97: becoming a castle needs a guild that is ready
        upgrades = self._castle_upgrades(camp)  # D-101: ...and upgrades.castle_min_built improvements built
        if castle:
            body += ["", t.t("guild.castle_title")] + [("✅ " if ok else "▫️ ") + text for text, ok in castle]
            body += [("✅ " if ok else "▫️ ") + text for text, ok in upgrades]
            if not all(ok for _, ok in castle):
                return View(kind="camp_grow", title=t.t("camps.grow_title"), body=body + ["", t.t("guild.castle_blocked")],
                            actions=[Action(id="guild", label=t.t("guild.button")), Action(id="claro", label=t.t("menu.back"))])
        if not all(ok for _, ok in upgrades):
            return View(kind="camp_grow", title=t.t("camps.grow_title"), body=body + ["", t.t("upgrades.castle_blocked")],
                        actions=[Action(id="upgrades", label=t.t("upgrades.button")), Action(id="claro", label=t.t("menu.back"))])
        if self._trial_needed(camp):           # D-99: then castillo needs a won Noche de prueba (after the guild, D-97)
            return self._trial_view(hero, camp)
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
        """Make the camp bigger: pay materials and take the chosen free zone next to its land (1, 2, 3, 4... zones).

        [ES]
        Qué hace: el miembro que agranda paga los materiales de su mochila (camps.grow_cost_per_level × nivel) y,
        desde el nivel 6, también 🪎 cofres (D-92); el campamento suma 1 nivel y la zona elegida. Con la despensa
        vacía no crece (D-93). Si falta algo, avisa y no cobra nada.
        La llaman: los botones de zona de ⬆️ Agrandar campamento (claim:x:y).
        Si cambia, afecta: niveles, zonas y cupo de miembros de los campamentos (tests/test_camps.py,
        tests/test_pantry.py, tests/test_backpack.py).
        """
        t = self.texts
        key = f"{hero.x}:{hero.y}"
        camp = self.store.get("camp", key)
        if not camp or hero.id not in camp["members"] or hero.activity:
            return self._camp_here_view(hero)
        if self._camp_starving(camp):          # D-93: with an empty pantry the camp does not grow
            return self._camp_here_view(hero, notice=t.t("pantry.grow_famine"))
        if not all(ok for _, ok in self._castle_needs(camp)):     # D-97: no castle without a guild that is ready
            return self._grow_view(hero)
        if not all(ok for _, ok in self._castle_upgrades(camp)):  # D-101: nor without 15 improvements built
            return self._grow_view(hero)
        if self._trial_needed(camp):           # D-99: castillo needs a won Noche de prueba
            return self._trial_view(hero, camp)
        level = camp.get("level", 1)
        cost = self._grow_cost(level)
        chests = self._grow_chests(level)          # D-92: paid from the chests of the member who grows
        if any(hero.backpack.get(i, 0) < n for i, n in cost.items()) or hero.chests < chests:
            lines = [t.t("camps.grow_missing", items=self._grow_cost_text(level))]
            if hero.chests < chests:
                lines.append(t.t("camps.grow_missing_chests", n=hero.chests, need=chests))
            return self._camp_here_view(hero, notice="\n".join(lines))
        zones = camp.get("zones", [[camp["x"], camp["y"]]])
        new = [cx, cy] if [cx, cy] in self._grow_candidates(camp) else None
        if new is None:
            return self._grow_view(hero)
        for item_id, n in cost.items():
            hero.backpack[item_id] -= n
            if hero.backpack[item_id] <= 0:
                del hero.backpack[item_id]
        hero.chests -= chests
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

    # ------------------------------------------------------------------ hunting (D-106, provisional)

    def _hunt_cfg(self) -> dict[str, Any]:
        return self.content.balance["hunt"]

    def _hunt_zone_blocker(self, hero: Hero) -> str | None:
        """Why nobody hunts in the hero's zone (no prey where the biome has no danger, the Guardian's lair), else None.

        [ES] Qué hace: dice por qué no se caza en esta zona: en el Claro (bioma sin peligro) no hay presas, y en la guarida
        solo está el Guardián (D-82). En el territorio de un campamento sí se caza: la tierra protege de las emboscadas, pero
        salir a buscar una presa es a propósito. La llaman: _hunt_view, _hunt, _call_hunt_party y _hunt_end_actions.
        Si cambia, afecta: dónde se puede cazar y dónde se puede convocar una partida de caza.
        """
        zone = self._zone(hero.x, hero.y)
        if self.content.biomes[zone.biome]["danger"] <= 0:
            return self.texts.t("hunt.no_prey")
        if self._is_lair(zone.x, zone.y):
            return self.texts.t("hunt.lair")
        return None

    def _hunt_view(self, hero: Hero, notice: str | None = None) -> View:
        """🏹 Cazar: what roams here, what a prey costs, the party of your camp; [Buscar presa] [Partida/Unirme] [Volver].

        [ES]
        Qué hace: la pantalla de cacería de la zona (D-106): qué enemigos rondan, cuánta energía cuesta cada presa, que no
        suma exploración ni recursos, tu vida y energía, y la partida de caza de tu campamento si hay una (o la pista para
        tener una). Botones: 🏹 Buscar presa (con ✋ Manual; con ⚔️ Peleas automáticas es 🏹 Cazar en lote, D-114),
        🏹 Partida de caza o 🏹 Unirme (si tienes campamento) y ↩️ Volver: 3 como máximo. Una línea dice cómo se pelea
        (⚙️ Opciones). Donde no hay presas vuelve a 🧭 Explorar con el aviso. Si estás malherido, lo avisa de entrada.
        La llaman: 🧭 Explorar → 🏹 Cazar, y las acciones de cacería cuando rechazan algo.
        Si cambia, afecta: tests/test_hunt.py, tests/test_options.py y el tope de 4 botones.
        """
        t = self.texts
        blocked = self._hunt_zone_blocker(hero)
        if blocked:
            return self._explore_menu(hero, notice=blocked)
        zone = self._zone(hero.x, hero.y)
        cost = self._hunt_cfg()["energy"]
        names: list[str] = []
        for _, edef in self._zone_enemies(zone):
            name = t.t(edef["name_key"])
            if name not in names:
                names.append(name)
        body = [t.t("zone.header", name=self._zone_name(zone), biome=self._biome_label(zone)), t.t("hunt.intro", energy=cost),
                t.t("hunt.prey_line", names=", ".join(names[:5])), t.t("hunt.rewards_hint"), self._status_line(hero)]
        body.append(t.t("hunt.mode_auto" if self._auto_on(hero) else "hunt.mode_manual"))     # D-114
        body += self._hunt_party_lines(hero)
        go = t.t("hunt.batch_button") if self._auto_on(hero) else t.t("hunt.go_button", energy=cost)
        actions = [Action(id="prey", label=go)]
        party_action = self._hunt_party_action(hero)
        if party_action:
            actions.append(party_action)
        actions.append(Action(id="explore_menu", label=t.t("menu.back")))
        if notice is None and hero.downed:
            notice = t.t("hunt.downed")
        return View(kind="hunt", title=t.t("hunt.title"), body=body, actions=actions, notice=notice)

    def _hunt(self, hero: Hero) -> View:
        """🏹 Buscar presa / 🏹 Otra presa: pay the energy and fight a common enemy of the zone right away.

        [ES]
        Qué hace: sale a cazar (D-106): cobra hunt.energy y empieza enseguida una pelea contra un enemigo común del bioma y
        el nivel de la zona (el mismo sorteo de los encuentros). No suma exploración ni recursos: da solo lo de la pelea.
        No se puede en el Claro ni en la guarida, malherido ni sin energía (se avisa y no se cobra). Ocupado (viajando,
        explorando, recolectando o durmiendo) lo frena antes _idle_action.
        Con ⚔️ Peleas automáticas (⚙️ Opciones, D-114) no pelea una presa: abre la pantalla de cantidad de 🏹 Cazar en lote.
        La llaman: los botones 🏹 Buscar presa (pantalla 🏹 Cazar) y 🏹 Otra presa (al ganar una presa), acción "prey".
        Si cambia, afecta: el gasto de energía y el ritmo de experiencia (balance.yaml hunt.energy), tests/test_hunt.py.
        """
        t = self.texts
        blocked = self._hunt_zone_blocker(hero)
        if blocked:
            return self._explore_menu(hero, notice=blocked)
        if self._auto_on(hero):                         # D-114: hunting in a batch, each prey fought alone
            return self._amount_view(hero, "hunt", 0)
        if hero.downed:
            return self._hunt_view(hero, notice=t.t("hunt.downed"))
        if not self._spend_energy(hero, "hunt", self._hunt_cfg()["energy"]):
            return self._hunt_view(hero, notice=self._no_energy_notice(hero))
        zone = self._zone(hero.x, hero.y)
        rng = Rng(int(hash_unit(self.world_seed, hero.id, "hunt", self.clock.now(), hero.kills) * 2**31))
        notice = self._start_combat(hero, zone, rng, "hunt.found", mark={"hunt": {"x": zone.x, "y": zone.y}})
        return self._combat_view(hero, self.store.get("combat", hero.id), notice=notice)

    def _hunt_batch_blocker(self, hero: Hero) -> str | None:
        """Why a hunting batch cannot start now (D-114): ✋ manual fights, no prey here, downed or life under the limit.

        [ES] Qué hace: dice por qué no se puede cazar en lote: con ✋ Manual se caza de a una presa; donde no hay presas
        (Claro, guarida); malherido; o con la vida por debajo del límite de 🩹 Retirarse de ⚙️ Opciones (el héroe no sale a
        pelear solo así). None si se puede. La llaman: _amount_view y _start_batch para "hunt".
        Si cambia, afecta: cuándo se puede cazar en lote (tests/test_options.py).
        """
        t = self.texts
        if not self._auto_on(hero):
            return t.t("hunt.batch_manual")
        blocked = self._hunt_zone_blocker(hero)
        if blocked:
            return blocked
        if hero.downed:
            return t.t("hunt.downed")
        if self._below_retreat(hero):
            return t.t("hunt.batch_low_hp", pct=self._option(hero, "retreat"))
        return None

    def _hunt_step(self, hero: Hero, zone: Zone, rng: Rng) -> str:
        """One prey of a hunting batch (D-114): a fight right away against a common enemy of the zone, marked as a hunt.

        [ES] Qué hace: cada vuelta de 🏹 Cazar en lote empieza una pelea contra un enemigo común de la zona (el mismo sorteo
        de los encuentros), marcada como cacería: cuenta para la partida de caza y su bono (D-106). La energía ya se cobró
        al empezar la vuelta (hunt.energy). Devuelve el aviso de la pelea; _batch_fight la pelea en automático.
        La llama: _settle. Si cambia, afecta: qué se caza en lote.
        """
        return self._start_combat(hero, zone, rng, "hunt.found", mark={"hunt": {"x": zone.x, "y": zone.y}})

    def _hunt_end_actions(self, hero: Hero) -> list[Action]:
        """Buttons a won hunt adds before ▶️ Continuar: 🏹 Otra presa (with energy, not downed) and the party button."""
        t = self.texts
        actions = []
        if not hero.downed and hero.energy >= self._hunt_cfg()["energy"] and not self._hunt_zone_blocker(hero):
            actions.append(Action(id="prey", label=t.t("hunt.again_button")))
        party_action = self._hunt_party_action(hero)
        if party_action:
            actions.append(party_action)
        return actions

    def _hunt_party(self, key: str) -> dict[str, Any] | None:
        """The camp's hunting party if one is open now (its window has not ended), else None."""
        party = self.store.get("hunt_party", key)
        return party if party and self.clock.now() < party["until"] else None

    def _hunt_target(self, party: dict[str, Any]) -> int:
        cfg = self._hunt_cfg()["party"]
        return hunt_rules.party_target(len(party.get("members", {})), cfg["prey_per_hunter"], cfg["min_hunters"])

    def _hunt_camp(self, hero: Hero) -> dict[str, Any] | None:
        """The hero's camp record if the hero is one of its members (who can call or join a hunting party)."""
        camp = self.store.get("camp", hero.camp) if hero.camp else None
        return camp if camp and hero.id in camp.get("members", []) else None

    def _hunt_party_action(self, hero: Hero) -> Action | None:
        """🏹 Partida de caza (no party open) or 🏹 Unirme (one open in this zone, not joined yet); None otherwise."""
        if self._hunt_camp(hero) is None:
            return None
        party = self._hunt_party(hero.camp)
        if party is None:
            return Action(id="huntparty", label=self.texts.t("hunt.party_button"))
        if hero.id not in party["members"] and (hero.x, hero.y) == (party["x"], party["y"]):
            return Action(id="huntjoin", label=self.texts.t("hunt.join_button"))
        return None

    def _hunt_companions(self, hero: Hero, party: dict[str, Any]) -> int:
        """Other party members present now in the party's zone (D-96 presence: pressed a button lately or busy there)."""
        present = {p["id"] for p in self._zone_players(party["x"], party["y"], exclude=hero.id)}
        return sum(1 for member in party["members"] if member != hero.id and member in present)

    def _hunt_bonus(self, hero: Hero, party: dict[str, Any]) -> float:
        """Group bonus of a hunt victory: +per companion present, capped (balance hunt.party)."""
        cfg = self._hunt_cfg()["party"]
        return hunt_rules.party_bonus(self._hunt_companions(hero, party), cfg["bonus_per_companion"], cfg["bonus_cap"])

    def _hunt_party_of_fight(self, hero: Hero, state: dict[str, Any]) -> dict[str, Any] | None:
        """The open party a finished hunt counts for: the hero's camp party, joined, in the zone of that hunt."""
        ref = state.get("hunt")
        if not ref or self._hunt_camp(hero) is None:
            return None
        party = self._hunt_party(hero.camp)
        if not party or hero.id not in party["members"] or (party["x"], party["y"]) != (ref["x"], ref["y"]):
            return None
        return party

    def _hunt_fight_done(self, hero: Hero, party: dict[str, Any], bonus: float) -> list[str]:
        """Count a won hunt for the party (saved now) and say how the tally goes."""
        hunt_rules.add_prey(party, hero.id)
        self.store.put("hunt_party", hero.camp, party)
        return [self.texts.t("hunt.party_prey", prey=party["prey"], target=self._hunt_target(party), pct=round(100 * bonus))]

    def _hunt_party_lines(self, hero: Hero) -> list[str]:
        """The hunt screen's party lines: the open party of your camp and your bonus now, or the hint to have a camp."""
        t = self.texts
        if not hero.camp:
            return [t.t("hunt.camp_hint")]
        party = self._hunt_party(hero.camp)
        camp = self._hunt_camp(hero)
        if not party or camp is None:
            return []
        zone = self._zone_name(self._zone(party["x"], party["y"]))
        lines = [t.t("hunt.party_line", camp=camp["name"], zone=zone, n=len(party["members"]), prey=party["prey"],
                     target=self._hunt_target(party), time=self._fmt_duration(party["until"] - self.clock.now()))]
        if hero.id in party["members"] and (hero.x, hero.y) == (party["x"], party["y"]):
            companions = self._hunt_companions(hero, party)
            lines.append(t.t("hunt.party_bonus_line", pct=round(100 * self._hunt_bonus(hero, party)), k=companions))
        return lines

    def _hunt_party_notice(self, hero: Hero, camp: dict[str, Any], party: dict[str, Any]) -> View:
        """The push the camp members present in the zone get: who calls, where, for how long, bonus and goal, [🏹 Unirme]."""
        t = self.texts
        cfg = self._hunt_cfg()["party"]
        zone = self._zone_name(self._zone(party["x"], party["y"]))
        body = [t.t("hunt.party_call", name=hero.name, camp=camp["name"], zone=zone, time=self._fmt_duration(party["until"] - party["at"])),
                t.t("hunt.party_how", per=round(100 * cfg["bonus_per_companion"]), cap=round(100 * cfg["bonus_cap"])),
                t.t("hunt.party_goal", per_hunter=cfg["prey_per_hunter"], xp=cfg["reward"]["xp"], gold=self._money(cfg["reward"]["gold"]))]
        return View(kind="hunt_party", title=t.t("hunt.party_title", zone=zone), body=body,
                    actions=[Action(id="huntjoin", label=t.t("hunt.join_button"))])

    def _call_hunt_party(self, hero: Hero) -> View:
        """🏹 Partida de caza: open your camp's hunting party in this zone and tell the members present here.

        [ES]
        Qué hace: un miembro de un campamento convoca la partida de caza en la zona donde está (D-106). Dura
        hunt.party.minutes y avisa (con 🏹 Unirme) solo a los miembros del campamento presentes en esta zona: tocaron un botón
        en los últimos presence.minutes o exploran, recolectan o duermen aquí (D-96). Los que están en otra zona no reciben
        nada (sin teletransporte). Una partida por campamento a la vez; si ya hay una aquí, te une. No gasta energía; no se
        puede donde no hay presas ni malherido.
        La llaman: el botón 🏹 Partida de caza (pantalla 🏹 Cazar o al ganar una presa), acción "huntparty".
        Si cambia, afecta: a quién llegan los avisos (tick() los entrega) y tests/test_hunt.py.
        """
        t = self.texts
        camp = self._hunt_camp(hero)
        if camp is None:
            return self._hunt_view(hero, notice=t.t("hunt.party_no_camp"))
        blocked = self._hunt_zone_blocker(hero)
        if blocked:
            return self._explore_menu(hero, notice=blocked)
        if hero.downed:
            return self._hunt_view(hero, notice=t.t("hunt.downed"))
        self._hunt_party_settle(hero)             # an ended party is closed (and reported) before a new one starts
        party = self._hunt_party(hero.camp)
        if party:
            here = (hero.x, hero.y) == (party["x"], party["y"])
            if here and hero.id not in party["members"]:
                return self._join_hunt_party(hero)
            if here:
                return self._hunt_view(hero, notice=t.t("hunt.party_member"))
            return self._hunt_view(hero, notice=t.t("hunt.party_already", zone=self._zone_name(self._zone(party["x"], party["y"])),
                                                    time=self._fmt_duration(party["until"] - self.clock.now())))
        now = self.clock.now()
        party = {"x": hero.x, "y": hero.y, "at": now, "until": now + self._seconds(self._hunt_cfg()["party"]["minutes"]),
                 "caller": hero.id, "members": {hero.id: 0}, "prey": 0}
        self.store.put("hunt_party", hero.camp, party)
        present = {p["id"] for p in self._zone_players(hero.x, hero.y, exclude=hero.id)}
        invited = [member for member in camp["members"] if member != hero.id and member in present]
        notice = self._hunt_party_notice(hero, camp, party)
        for member in invited:
            self._push(member, notice)
        return self._hunt_view(hero, notice=t.t("hunt.party_called" if invited else "hunt.party_called_alone", n=len(invited)))

    def _join_hunt_party(self, hero: Hero) -> View:
        """🏹 Unirme: join your camp's open hunting party, only from its zone (works while busy, D-106).

        [ES]
        Qué hace: te suma a la partida de caza abierta de tu campamento si estás en su zona. Se puede aunque estés
        explorando o recolectando (luego, para cazar, hay que terminar o parar). Si no hay partida, terminó o estás en otra
        zona, lo dice y no hace nada.
        La llaman: el botón 🏹 Unirme del aviso de la partida, de la pantalla 🏹 Cazar o del final de una presa ("huntjoin").
        Si cambia, afecta: quién suma bono y presas en la partida, tests/test_hunt.py.
        """
        t = self.texts
        camp = self._hunt_camp(hero)
        party = self._hunt_party(hero.camp) if camp else None
        if camp is None:
            return self._main_view(hero, notice=t.t("hunt.party_no_camp"))
        if party is None:
            return self._main_view(hero, notice=t.t("hunt.party_none"))
        if (hero.x, hero.y) != (party["x"], party["y"]):
            return self._main_view(hero, notice=t.t("hunt.party_wrong_zone", zone=self._zone_name(self._zone(party["x"], party["y"]))))
        if hero.id in party["members"]:
            notice = t.t("hunt.party_member")
        else:
            party["members"][hero.id] = 0
            self.store.put("hunt_party", hero.camp, party)
            notice = t.t("hunt.party_joined", camp=camp["name"])
        if hero.activity:
            return self._main_view(hero, notice=notice)
        return self._hunt_view(hero, notice=notice)

    def _hunt_party_settle(self, hero: Hero) -> None:
        """Close the hero's camp hunting party once its window ended (lazy clock, like raids, D-106).

        [ES]
        Qué hace: el reloj perezoso de la partida de caza (sin reloj de fondo): cuando un miembro del campamento juega
        después de que terminó la ventana, la cierra, manda el informe a los cazadores y paga el premio si llegaron a la meta.
        La llaman: view() y act(), después de _settle y _raid_settle; y _call_hunt_party antes de abrir otra.
        Si cambia, afecta: cuándo llega el informe y el premio de las partidas de todos los campamentos.
        """
        if not hero.camp:
            return
        party = self.store.get("hunt_party", hero.camp)
        if not party or self.clock.now() < party["until"]:
            return
        self.store.delete("hunt_party", hero.camp)
        self._resolve_hunt_party(hero.camp, party, hero)

    def _resolve_hunt_party(self, key: str, party: dict[str, Any], actor: Hero) -> None:
        """Report to every hunter of the party (prey together, each one's count) and pay the reward if they reached the goal."""
        t = self.texts
        cfg = self._hunt_cfg()["party"]
        camp = self.store.get("camp", key) or {}
        members = party.get("members", {})
        body = [t.t("hunt.party_end", prey=party.get("prey", 0), n=len(members), zone=self._zone_name(self._zone(party["x"], party["y"])),
                    target=self._hunt_target(party))]
        hunters = []
        for hero_id, prey in sorted(members.items(), key=lambda row: -row[1]):
            name = actor.name if hero_id == actor.id else (self.store.get("hero", hero_id) or {}).get("name", "?")
            hunters.append(t.t("hunt.party_end_hunter", name=name, prey=prey))
        if hunters:
            body.append(t.t("hunt.party_end_hunters", list=" · ".join(hunters)))
        if hunt_rules.reward_earned(party, cfg["prey_per_hunter"], cfg["min_hunters"]):
            for hero_id in hunt_rules.rewarded(party):
                self._raid_reward(hero_id, cfg["reward"], actor)        # pays online or not, the actor in memory
            body.append(t.t("hunt.party_end_reward", xp=cfg["reward"]["xp"], gold=self._money(cfg["reward"]["gold"])))
        elif len(members) < cfg["min_hunters"]:
            body.append(t.t("hunt.party_end_alone", n=cfg["min_hunters"]))
        else:
            body.append(t.t("hunt.party_end_short"))
        view = View(kind="hunt_party_end", title=t.t("hunt.party_end_title", camp=camp.get("name", "?")), body=body)
        for hero_id in members:
            self._push(hero_id, view)

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

    # ------------------------------------------------------------------ camp raids and the Noche de prueba (D-99, provisional)

    def _raid_cfg(self) -> dict[str, Any]:
        return self.content.balance["raids"]

    def _raid_sub(self, kind: str) -> dict[str, Any]:
        """The numbers of a raid kind: the weekly raid ("raid") or the Noche de prueba ("trial")."""
        cfg = self._raid_cfg()
        return cfg["trial"] if kind == "trial" else cfg

    def _raid_interval(self) -> float:
        """Real seconds between two raids: 7 / raids.per_week days (D-154: 3 per week)."""
        return self._seconds(7 / self._raid_cfg()["per_week"] * 24 * 60)

    def _days_until(self, when: float) -> int:
        return max(0, math.ceil((when - self.clock.now()) / self._day_seconds()))

    def _raid_settle(self, hero: Hero) -> None:
        """The lazy raid clock of the hero's camp (D-99): schedule it, open it when due, close it when its window ended.

        [ES]
        Qué hace: el reloj perezoso de las incursiones del campamento del héroe (sin reloj de fondo). La primera vez
        que un miembro juega en un campamento de nivel raids.from_level o más, agenda la próxima (7 / raids.per_week días, D-154).
        Cuando un miembro juega después de esa hora, llega la incursión: aviso con 🛡️ Defender a los miembros activos.
        Cuando su ventana terminó, la cierra (defendida o perdida). Solo campamentos de jugadores: el Claro no es un
        campamento guardado en "camp", así que nunca tiene incursiones (D-95, D-98).
        La llaman: view() y act(), después de _settle.
        Si cambia, afecta: cuándo llegan y cuándo terminan las incursiones de todos los campamentos.
        """
        if not hero.camp:
            return
        camp = self.store.get("camp", hero.camp)
        if not camp or hero.id not in camp.get("members", []):
            return
        now = self.clock.now()
        changed = False
        raid = camp.get("raid")
        if raid and self._raid_over(raid):
            self._resolve_raid(camp, raid, hero)
            changed = True
        if camp.get("level", 1) >= self._raid_cfg()["from_level"]:
            if camp.get("next_raid_at") is None:          # reached raids.from_level, or a camp from before the patch
                camp["next_raid_at"] = now + self._raid_interval()
                changed = True
            elif not camp.get("raid") and now >= camp["next_raid_at"]:
                self._open_raid(camp, "raid", hero.id)
                changed = True
            elif self._raid_watch(camp):                  # D-101: the watchtower sees it coming
                changed = True
        if changed:
            self.store.put("camp", hero.camp, camp)

    def _raid_over(self, raid: dict[str, Any]) -> bool:
        """True when the window closed and nobody is still fighting for it (or the grace time is over too)."""
        now = self.clock.now()
        if now < raid["until"]:
            return False
        if now >= raid["until"] + self._seconds(self._raid_cfg()["grace_minutes"]):
            return True
        return not any(result == "fighting" and self.store.get("combat", hid) for hid, result in raid["fights"].items())

    def _raid_enemy(self, camp: dict[str, Any], kind: str, at: float) -> tuple[str, int]:
        """The enemy of a raid: from the biome and level of the camp's zone; the strongest one for the Noche de prueba."""
        zone = self._zone(camp["x"], camp["y"])
        roll = hash_unit(self.world_seed, "raid", camp["x"], camp["y"], at)
        return raid_rules.pick_enemy(self.content.enemies, zone.biome, zone.level + self._raid_sub(kind)["enemy_level_bonus"],
                                     strongest=kind == "trial", roll=roll)

    def _open_raid(self, camp: dict[str, Any], kind: str, opener: str) -> None:
        """Start a raid (or the Noche de prueba) and tell the active members, with the 🛡️ Defender button (D-99).

        [ES]
        Qué hace: abre la incursión en el campamento (enemigo, ventana, victorias necesarias según los miembros activos)
        y les manda el aviso con 🛡️ Defender. Quien la abrió cuenta como activo. El llamador guarda el campamento.
        La llaman: _raid_settle (la semanal) y _start_trial (la Noche de prueba).
        Si cambia, afecta: a quién le llega el aviso y cuántas victorias hacen falta.
        """
        now = self.clock.now()
        sub = self._raid_sub(kind)
        active = self._active()
        told = [member for member in camp["members"] if member in active or member == opener]
        enemy_id, level = self._raid_enemy(camp, kind, now)
        raid = {"kind": kind, "at": now, "until": now + self._seconds(self._raid_cfg()["window_minutes"]),
                "required": raid_rules.required_wins(len(told), sub["required_share"], sub["min_wins"]),
                "wins": 0, "fights": {}, "enemy": enemy_id, "level": level,
                "defense": self._camp_defense(camp, night=self._is_night(now))}     # D-101: what the improvements hold back
        camp["raid"] = raid
        notice = self._raid_notice(camp, raid)
        for member in told:
            self._push(member, notice)

    def _raid_notice(self, camp: dict[str, Any], raid: dict[str, Any]) -> View:
        t = self.texts
        trial = raid["kind"] == "trial"
        enemy = t.t(self.content.enemies[raid["enemy"]]["name_key"])
        body = [t.t("raids.trial_arrive" if trial else "raids.arrive", enemy=enemy, level=raid["level"]),
                t.t("raids.need", need=raid["required"], time=self._fmt_duration(raid["until"] - raid["at"])),
                t.t("raids.trial_stakes", days=self._raid_cfg()["trial"]["retry_days"]) if trial else t.t("raids.stakes")]
        if raid.get("defense"):
            body.insert(1, t.t("raids.defense_line", defense=raid["defense"], pct=round(100 * (1 - self._raid_weaken(raid)))))
        return View(kind="camp_raid", title=t.t("raids.trial_title" if trial else "raids.title", camp=camp["name"]), body=body,
                    actions=[Action(id="defend", label=t.t("raids.defend_button"))])

    def _defend_action(self, camp: dict[str, Any], hero: Hero) -> Action | None:
        """🛡️ Defender while the camp's raid window is open and this member has not fought yet."""
        raid = camp.get("raid")
        if not raid or hero.id in raid["fights"] or self.clock.now() >= raid["until"]:
            return None
        return Action(id="defend", label=self.texts.t("raids.defend_button"))

    def _defend(self, hero: Hero) -> View:
        """🛡️ Defender: fight ONE combat for your camp's open raid, wherever you are (D-99).

        [ES]
        Qué hace: el miembro sale a defender su campamento: UNA pelea con el motor de combate normal contra el enemigo
        de la incursión (en la Noche de prueba, su versión élite). Se puede desde cualquier zona, sin energía, si no
        estás ocupado. Perder sigue las reglas normales de derrota: no hay castigo extra.
        La llaman: el botón 🛡️ Defender del aviso, de la pantalla del campamento o de la Noche de prueba.
        Si cambia, afecta: las victorias de la incursión (_raid_fight_done) y tests/test_raids.py.
        """
        t = self.texts
        key = hero.camp
        camp = self.store.get("camp", key) if key else None
        raid = camp.get("raid") if camp else None
        if not raid or hero.id not in camp["members"] or self.clock.now() >= raid["until"]:
            return self._main_view(hero, notice=t.t("raids.none"))
        if hero.id in raid["fights"]:
            return self._main_view(hero, notice=t.t("raids.already"))
        if hero.activity:
            return self._activity_view(hero, notice=t.t("raids.busy"))
        trial = raid["kind"] == "trial"
        edef = self.content.enemies[raid["enemy"]]
        seed = int(hash_unit(self.world_seed, hero.id, "raid", raid["at"]) * 2**31)
        state = make_combat(raid["enemy"], edef, raid["level"], self._kit(hero), seed)
        if trial:
            sub = self._raid_sub("trial")
            raid_rules.scale_enemy(state, sub["enemy_hp_mult"], sub["enemy_attack_mult"])
        weaken = self._raid_weaken(raid)
        if weaken < 1:                                  # D-101: walls, traps and towers hold part of the wave back
            raid_rules.scale_enemy(state, weaken, weaken)
        state["raid"] = {"camp": key, "at": raid["at"]}
        self.store.put("combat", hero.id, state)
        raid["fights"][hero.id] = "fighting"
        self.store.put("camp", key, camp)
        self.bus.publish(CombatStarted(hero.id, raid["enemy"], seed))
        notice = t.t("raids.trial_started" if trial else "raids.started", camp=camp["name"], enemy=t.t(edef["name_key"]), level=raid["level"])
        return self._combat_view(hero, state, notice=notice)

    def _raid_fight_done(self, hero: Hero, state: dict[str, Any]) -> list[str]:
        """Count a defender's finished fight on the camp's raid (a win only if it is still the same raid)."""
        t = self.texts
        ref = state["raid"]
        camp = self.store.get("camp", ref["camp"])
        raid = camp.get("raid") if camp else None
        if not raid or raid.get("at") != ref["at"]:
            return ["", t.t("raids.fight_late")]
        won = state["outcome"] == "victory"
        raid["fights"][hero.id] = "won" if won else ("lost" if state["outcome"] == "defeat" else "fled")
        if won:
            raid["wins"] += 1
        self.store.put("camp", ref["camp"], camp)
        return ["", t.t("raids.fight_won" if won else "raids.fight_lost", camp=camp["name"], wins=raid["wins"], need=raid["required"])]

    def _resolve_raid(self, camp: dict[str, Any], raid: dict[str, Any], actor: Hero) -> None:
        """Close a raid whose window ended: defended or lost, and tell every member (D-99).

        [ES]
        Qué hace: cierra la incursión. Defendida (victorias ≥ necesarias): premio chico a cada defensor (raids.reward
        o trial.reward). Perdida: la incursión semanal se lleva raids.loss_share de la despensa (si tiene) y nada más;
        la Noche de prueba no se lleva nada y se reintenta a los trial.retry_days. Agenda la próxima incursión semanal.
        Nunca toca niveles, zonas ni miembros (§15). El llamador guarda el campamento.
        La llama: _raid_settle.
        Si cambia, afecta: la despensa, la experiencia y las monedas de los defensores, y si el campamento puede ser castillo.
        """
        t = self.texts
        now = self.clock.now()
        trial = raid["kind"] == "trial"
        sub = self._raid_sub(raid["kind"])
        won = raid["wins"] >= raid["required"]
        camp.pop("raid", None)
        name, score = camp["name"], {"wins": raid["wins"], "need": raid["required"]}
        body: list[str] = []
        if won:
            body.append(t.t("raids.trial_won" if trial else "raids.defended", camp=name, **score))
            for hero_id in raid["fights"]:
                self._raid_reward(hero_id, sub["reward"], actor)
            if raid["fights"]:
                body.append(t.t("raids.reward", xp=sub["reward"]["xp"], gold=self._money(sub["reward"]["gold"])))
        if trial and camp.get("next_raid_at") is not None and camp["next_raid_at"] <= raid["until"]:
            # the weekly raid came due during the Noche de prueba: the trial was that week's raid
            camp["next_raid_at"] = raid_rules.next_raid_at(raid["until"], now, self._raid_interval())
        if trial and won:
            camp["trial_won"] = True
        elif trial:
            camp["trial_retry_at"] = raid["until"] + self._seconds(sub["retry_days"] * 24 * 60)
            body.append(t.t("raids.trial_lost", camp=name, time=self._fmt_duration(camp["trial_retry_at"] - now), **score))
        else:
            record = camp.setdefault("raids", {"won": 0, "lost": 0})
            record["won" if won else "lost"] += 1
            if not won:
                lost = self._raid_food_loss(camp)
                body += [t.t("raids.lost", camp=name, **score),
                         t.t("raids.lost_food", rations=lost) if lost else t.t("raids.lost_nothing")]
            camp["next_raid_at"] = raid_rules.next_raid_at(raid["until"], now, self._raid_interval())
            body.append(t.t("raids.next", n=self._days_until(camp["next_raid_at"])))
        view = View(kind="camp_raid_end", title=t.t("raids.trial_end_title" if trial else "raids.end_title", camp=name), body=body)
        for member in camp["members"]:
            self._push(member, view)

    def _raid_reward(self, hero_id: str, reward: dict[str, int], actor: Hero) -> None:
        """Pay a defender (online or not); the hero playing right now is paid in memory, so its save keeps it.

        Also pays the hunters of a hunting party that reached its goal (D-106).
        """
        target = actor if actor.id == hero_id else self._load(hero_id)
        if target is None:
            return
        target.gold += reward["gold"]
        self._give_xp(target, reward["xp"])
        if target is not actor:
            self._save(target)

    def _raid_weaken(self, raid: dict[str, Any]) -> float:
        """How much life and attack the raid's attackers keep after the camp's 🛡️ Defensa (1.0 = all, D-101).

        [ES]
        Qué hace: cada punto de 🛡️ Defensa que tenía el campamento al llegar la oleada les quita a los atacantes
        raids.defense_weaken_per_point de vida y de ataque (4 %: con las 8 defensas, 11 puntos, un 44 % menos; 12 de
        noche con los Braseros). Nunca baja de raids.defense_floor. Vale para la oleada semanal y la Noche de prueba.
        La llaman: _defend (la pelea de cada defensor) y _raid_notice (el aviso dice cuánto los frena).
        Si cambia, afecta: qué tan difícil es defender un campamento con mejoras (tests/test_raids.py).
        """
        cfg = self._raid_cfg()
        return max(cfg["defense_floor"], 1 - cfg["defense_weaken_per_point"] * raid.get("defense", 0))

    def _is_night(self, when: float) -> bool:
        """True if `when` falls in the night hours of raids.night (used by the Braseros' night defense, D-101)."""
        night = self._raid_cfg()["night"]
        hour = (when / 3600 + night["utc_offset_hours"]) % 24
        return hour >= night["from_hour"] or hour < night["to_hour"]

    def _raid_watch(self, camp: dict[str, Any]) -> bool:
        """🗼 Torre de vigía: tell the active members once, a few hours before the weekly raid. True if it told them."""
        hours = self._camp_effect(camp, "warning_hours")
        nxt = camp.get("next_raid_at")
        now = self.clock.now()
        if not hours or nxt is None or camp.get("raid") or camp.get("watched") == nxt:
            return False
        if not nxt - self._seconds(hours * 60) <= now < nxt:
            return False
        camp["watched"] = nxt
        t = self.texts
        view = View(kind="camp_watch", title=t.t("raids.watch_title", camp=camp["name"]),
                    body=[t.t("raids.watch", time=self._fmt_duration(nxt - now), defense=self._camp_defense(camp))])
        active = self._active()
        for member in camp["members"]:
            if member in active:
                self._push(member, view)
        return True

    def _raid_food_loss(self, camp: dict[str, Any]) -> int:
        """A lost raid takes raids.loss_share of the camp's pantry, if it has one; returns the rations taken."""
        if self._camp_pantry(camp) is None:              # also settles the consumption up to now
            return 0
        key = f"{camp['x']}:{camp['y']}"
        data = self.store.get("pantry", key)
        lost = raid_rules.food_lost(data["rations"], self._raid_cfg()["loss_share"])
        data["rations"] = max(0.0, data["rations"] - lost)
        self.store.put("pantry", key, data)
        return int(round(lost))

    def _raid_lines(self, camp: dict[str, Any]) -> list[str]:
        """The camp screen's raid line: the one going on, the next one (from pueblo) or a heads-up one level before."""
        t = self.texts
        cfg = self._raid_cfg()
        raid = camp.get("raid")
        if raid:
            left = self._fmt_duration(max(0.0, raid["until"] - self.clock.now()))
            return [t.t("raids.trial_line" if raid["kind"] == "trial" else "raids.open_line",
                        n=len(raid["fights"]), wins=raid["wins"], need=raid["required"], time=left)]
        level = camp.get("level", 1)
        if level >= cfg["from_level"]:
            nxt = camp.get("next_raid_at")
            hours = self._camp_effect(camp, "warning_hours")
            if nxt is not None and hours and 0 < nxt - self.clock.now() <= self._seconds(hours * 60):
                return [t.t("raids.watch_line", time=self._fmt_duration(nxt - self.clock.now()))]     # 🗼 Torre de vigía
            return [t.t("raids.next_line", n=self._days_until(nxt) if nxt is not None else math.ceil(7 / cfg["per_week"]))]
        if level == cfg["from_level"] - 1:
            return [t.t("raids.soon_line", level=cfg["from_level"])]
        return []

    def _trial_needed(self, camp: dict[str, Any]) -> bool:
        """True if growing one level needs a Noche de prueba the camp has not won yet (8 → 9, castillo)."""
        return camp.get("level", 1) + 1 == self._raid_sub("trial")["to_level"] and not camp.get("trial_won")

    def _trial_blocker(self, camp: dict[str, Any]) -> str | None:
        """Why the Noche de prueba cannot be called right now (a notice), or None."""
        t = self.texts
        if camp.get("raid"):
            return t.t("raids.trial_busy")
        wait = camp.get("trial_retry_at", 0.0) - self.clock.now()
        if wait > 0:
            return t.t("raids.trial_wait", time=self._fmt_duration(wait))
        if self._camp_starving(camp):
            return t.t("raids.trial_famine")
        return None

    def _trial_view(self, hero: Hero, camp: dict[str, Any], notice: str | None = None) -> View:
        """The grow screen at level 8: castillo needs a won Noche de prueba; call it or defend it here (D-99).

        [ES]
        Qué hace: en lugar de las zonas para crecer, muestra que castillo pide ganar la Noche de prueba, contra qué
        enemigo y cuántas victorias hacen falta. Botones: 🌙 Noche de prueba (si se puede convocar) o 🛡️ Defender
        (si ya empezó), y ↩️ Volver. Como mucho 2 botones.
        La llaman: _grow_view y _grow_camp (nivel 8 sin la prueba ganada) y _start_trial.
        Si cambia, afecta: cómo se llega a castillo.
        """
        t = self.texts
        sub = self._raid_sub("trial")
        enemy_id, level = self._raid_enemy(camp, "trial", 0.0)
        required = raid_rules.required_wins(self._camp_active(camp), sub["required_share"], sub["min_wins"])
        body = [t.t("raids.trial_intro", camp=camp["name"], enemy=t.t(self.content.enemies[enemy_id]["name_key"]), level=level),
                t.t("raids.trial_how", need=required, days=sub["retry_days"],
                    time=self._fmt_duration(self._seconds(self._raid_cfg()["window_minutes"])))]
        actions: list[Action] = []
        defend = self._defend_action(camp, hero)
        if camp.get("raid"):
            body += self._raid_lines(camp) + ([] if camp["raid"]["kind"] == "trial" else [t.t("raids.trial_busy")])
        else:
            blocker = self._trial_blocker(camp)
            body += [blocker] if blocker and blocker != notice else []
            actions += [] if blocker else [Action(id="trial", label=t.t("raids.trial_button"))]
        actions += [defend] if defend else []
        actions.append(Action(id="claro", label=t.t("menu.back")))
        return View(kind="camp_trial", title=t.t("raids.trial_screen"), body=body, actions=actions, notice=notice)

    def _start_trial(self, hero: Hero) -> View:
        """🌙 Noche de prueba: a member at the camp calls it (level 8, pantry not empty, no raid on, after the retry wait)."""
        t = self.texts
        key = f"{hero.x}:{hero.y}"
        camp = self.store.get("camp", key)
        if not camp or hero.id not in camp["members"] or hero.activity or not self._trial_needed(camp):
            return self._camp_here_view(hero)
        blocker = self._trial_blocker(camp)
        if blocker:
            return self._trial_view(hero, camp, notice=blocker)
        self._open_raid(camp, "trial", hero.id)
        self.store.put("camp", key, camp)
        return self._trial_view(hero, camp, notice=t.t("raids.trial_sent"))

    # ------------------------------------------------------------------ camp improvements (D-101, provisional)

    def _upgrade_catalog(self) -> dict[str, dict[str, Any]]:
        """Every camp improvement (content/camp_upgrades.yaml "upgrades"), retired ones included, in content order.

        [ES]
        Qué hace: da el catálogo de 🔨 Mejoras de los campamentos, en el orden del archivo (por nivel). Incluye las
        retiradas: lo ya construido sigue contando; solo dejan de poder construirse.
        La llaman: casi todas las funciones de esta sección.
        Si cambia, afecta: qué mejoras existen y en qué orden se muestran.
        """
        return (self.content.camp_upgrades or {}).get("upgrades") or {}

    def _tech_catalog(self) -> dict[str, dict[str, Any]]:
        """The camp knowledge that the Biblioteca opens (content/camp_upgrades.yaml "knowledge")."""
        return (self.content.camp_upgrades or {}).get("knowledge") or {}

    def _upgrades(self, key: str) -> dict[str, Any]:
        """The improvements record of the camp at `key` ("x:y"), with its three parts always present.

        [ES]
        Qué hace: lee del almacén (espacio "upgrades", clave "x:y" del campamento) lo que el campamento construyó
        ("built": id → hora en que se terminó), las obras a medias ("works": id → lo aportado, monedas en "coins")
        y su conocimiento ("tech": "done" aprendidos, "current" el que estudian y "progress" lo aportado). D-116: también
        los 🪑 muebles colocados ("furniture": id del mueble → {"by": nombre, "id": cuenta, "at": hora}), uno de cada uno.
        La llaman: las pantallas y acciones de 🔨 Mejoras y los efectos (_built_at, _furniture_effect).
        Si cambia, afecta: todo lo guardado de las mejoras; los campos solo se agregan (nunca se borra lo construido).
        """
        data = self.store.get("upgrades", key) or {}
        data.setdefault("built", {})
        data.setdefault("works", {})
        data.setdefault("tech", {})
        data.setdefault("furniture", {})        # D-116: 🪑 camp furniture placed (one of each piece)
        return data

    def _built_at(self, key: str | None) -> list[str]:
        """Ids of the improvements built by the camp at `key`, in catalog order (empty without a camp)."""
        if not key:
            return []
        built = (self.store.get("upgrades", key) or {}).get("built", {})
        return [uid for uid in self._upgrade_catalog() if uid in built] if built else []

    def _built(self, camp: dict[str, Any] | None) -> list[str]:
        """Ids of the improvements a player camp built; the Claro ({"claro": True}) and no camp have none (D-98)."""
        if not camp or "x" not in camp:
            return []
        return self._built_at(f"{camp['x']}:{camp['y']}")

    def _effect_at(self, key: str | None, name: str) -> float:
        """Sum of one effect over the camp's built improvements and its 🪑 furniture (D-116) at `key` ("x:y")."""
        if not key:
            return 0.0
        record = self.store.get("upgrades", key) or {}           # one read for both (_stock calls this per zone)
        built = record.get("built") or {}
        catalog = self._upgrade_catalog()
        total = float(sum(udef.get("effect", {}).get(name, 0) for uid, udef in catalog.items() if uid in built))
        return total + self._furniture_sum(record, name)

    def _furniture_effect(self, key: str | None, name: str) -> float:
        """Sum of one effect over the 🪑 furniture placed in the camp at `key` (D-116): one of each piece, never more.

        [ES]
        Qué hace: suma un efecto ("members", "defense"...) de los muebles colocados en el campamento (items.yaml "effect").
        Como se guardan por id de mueble, cada mueble cuenta una sola vez aunque alguien haga otro igual.
        La llaman: _effect_at (y por ahí _camp_effect: cupo de miembros, vida, despensa...) y _camp_defense ("defense").
        Si cambia, afecta: lo que suman los muebles de la 🪑 Carpintería a cada campamento.
        """
        if not key:
            return 0.0
        return self._furniture_sum(self.store.get("upgrades", key) or {}, name)

    def _furniture_sum(self, record: dict[str, Any], name: str) -> float:
        """Sum of one effect over the furniture of an "upgrades" record (D-116); unknown ids count 0."""
        placed = record.get("furniture") or {}
        return float(sum(self.content.items.get(fid, {}).get("effect", {}).get(name, 0) for fid in placed))

    def _camp_effect(self, camp: dict[str, Any] | None, name: str) -> float:
        """Sum of one effect over the improvements the camp built (0 for the Claro or no camp).

        [ES]
        Qué hace: suma un efecto ("regen_mult", "ration_cut", "members", "stock_regen"...) de todas las mejoras
        construidas. Las mejoras sin ese efecto suman 0.
        La llaman: la vida (_camp_regen_mult), la despensa (_camp_pantry, _camp_feed), el cupo (_members_cap) y
        las oleadas ("warning_hours" de la Torre de vigía: _raid_watch y _raid_lines). Suma también los 🪑 muebles
        colocados (D-116: las 🛏️ Literas de roble dan "members": 1).
        Si cambia, afecta: todos los efectos de las mejoras y de los muebles.
        """
        if not camp or "x" not in camp:
            return 0.0
        return self._effect_at(f"{camp['x']}:{camp['y']}", name)

    def _camp_service(self, camp: dict[str, Any] | None, name: str) -> dict[str, Any] | None:
        """The "service" block of the built improvement that opens `name` (rest_price, sell_ratio, craft...), or None."""
        catalog = self._upgrade_catalog()
        for uid in self._built(camp):
            service = catalog[uid].get("service") or {}
            if name in service:
                return service
        return None

    def _camp_defense(self, camp: dict[str, Any] | None, night: bool = False) -> int:
        """🛡️ Defensa of a camp: the sum of the defense points of its built improvements (+ night ones at night).

        The raids (built separately) read this number: each point makes a raid weaker or lowers the wins it needs.
        It never changes anything by itself.

        [ES]
        Qué hace: suma los puntos de 🛡️ Defensa de las mejoras construidas (Empalizada 1, Torre de vigía 1, Trampas 1,
        Perrera 1, Muralla de piedra 2, Braseros 1, Torres de arqueros 2, Foso 2: 11 en total) y la de los 🪑 muebles
        colocados (D-116: el 🗄️ Armero de roble, +1). Con night=True suma también "night_defense" (los Braseros: +1 de
        noche). El Claro y quien no tiene campamento: 0.
        La llaman: la pantalla del campamento, la de 🔨 Mejoras y _open_raid, que la guarda al llegar la oleada para
        debilitar a los atacantes (_raid_weaken: 4 % menos de vida y ataque por punto).
        Si cambia, afecta: cuánto protegen los alrededores de cada campamento cuando lleguen las oleadas.
        """
        catalog = self._upgrade_catalog()
        built = self._built(camp)
        points = sum(int(catalog[uid].get("defense", 0)) for uid in built)
        if camp and "x" in camp:                # D-116: 🗄️ the furniture's defense (one of each piece)
            points += int(self._furniture_effect(f"{camp['x']}:{camp['y']}", "defense"))
        if night:
            points += int(sum(catalog[uid].get("effect", {}).get("night_defense", 0) for uid in built))
        return points

    def _own_camp_here(self, hero: Hero, x: int | None = None, y: int | None = None) -> dict[str, Any] | None:
        """The hero's camp if zone (x, y) (by default where the hero is) is part of its territory and the hero is a member."""
        if not hero.camp:
            return None
        if x is None or y is None:
            x, y = hero.x, hero.y
        ref = self.store.get("territory", f"{x}:{y}")
        if not ref or ref.get("camp") != hero.camp:
            return None
        camp = self.store.get("camp", hero.camp)
        return camp if camp and hero.id in camp.get("members", []) else None

    def _camp_regen_mult(self, hero: Hero) -> float:
        """How much faster health comes back for a member in its camp's territory: Fogón (normal), Enfermería (after falling).

        [ES]
        Qué hace: devuelve el multiplicador de la vida que se recupera sola: ×1,5 con 🔥 Fogón (recuperación normal) y
        ×1,5 con 🏥 Enfermería (después de caer, D-83), solo para miembros parados en el territorio de su campamento.
        Fuera de ahí, o sin esas mejoras: ×1. No cambia los números de balance.yaml regen: los multiplica.
        La llama: _settle (la vida que se recupera sola). La pantalla de salud puede usarla para mostrar el tiempo real.
        Si cambia, afecta: cuánto tarda en curarse quien descansa en su campamento.
        """
        camp = self._own_camp_here(hero)
        if not camp:
            return 1.0
        return 1.0 + self._camp_effect(camp, "downed_regen_mult" if hero.downed else "regen_mult")

    def _camp_tech_bonus(self, hero: Hero, x: int, y: int, name: str, item: str | None = None) -> float:
        """What the camp's knowledge adds for a member at zone (x, y) (D-101): only in the territory, or also next to it
        for techs marked `near` (Rastreo: there are no fights inside the territory, D-81).

        [ES]
        Qué hace: suma el efecto `name` del 📚 Conocimiento aprendido por el campamento del héroe (gather_bonus,
        explore_points o loot_bonus de un objeto), solo si es miembro y está en el territorio; los estudios con
        near: true también valen en las zonas que tocan el territorio.
        La llaman: _gather_step (Herramientas), _explore_step (Cartografía) y _end_combat (Rastreo).
        Si cambia, afecta: lo que rinden recolectar, explorar y la carne del botín para los miembros.
        """
        if not hero.camp:
            return 0.0
        done = (self.store.get("upgrades", hero.camp) or {}).get("tech", {}).get("done", [])
        if not done:
            return 0.0
        catalog = self._tech_catalog()
        inside = self._own_camp_here(hero, x, y) is not None
        near: bool | None = None
        total = 0.0
        for tid in done:
            tdef = catalog.get(tid, {})
            value = tdef.get("effect", {}).get(name, 0)
            if item is not None:
                value = value.get(item, 0) if isinstance(value, dict) else 0
            if not value or isinstance(value, dict):
                continue
            if not inside and tdef.get("near"):
                if near is None:
                    near = any(self._own_camp_here(hero, x + dx, y + dy) for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)))
                if not near:
                    continue
            elif not inside:
                continue
            total += float(value)
        return total

    def _upgrade_name(self, uid: str) -> str:
        udef = self._upgrade_catalog().get(uid, {})
        return f"{udef.get('emoji', '')} {self.texts.t(udef.get('name_key', f'upgrade.{uid}.name'))}".strip()

    def _tech_name(self, tid: str) -> str:
        tdef = self._tech_catalog().get(tid, {})
        return f"{tdef.get('emoji', '')} {self.texts.t(tdef.get('name_key', f'tech.{tid}.name'))}".strip()

    @staticmethod
    def _work_need(definition: dict[str, Any]) -> dict[str, int]:
        """What an improvement or a study asks: its materials, plus "coins" (bronze) if it asks for coins."""
        need = {item_id: int(n) for item_id, n in (definition.get("cost") or {}).items()}
        if definition.get("coins"):
            need["coins"] = int(definition["coins"])
        return need

    def _need_lines(self, need: dict[str, int], progress: dict[str, int]) -> list[str]:
        """One progress bar per material (and coins) of a work: "🪵 Madera: 10/20 ▓▓▓▓░░░░"."""
        t = self.texts
        lines = []
        for key, n in need.items():
            have = min(n, int(progress.get(key, 0)))
            if key == "coins":
                lines.append(t.t("upgrades.coin_line", have=self._money(have), need=self._money(n), bar=self._bar(have, n, 8)))
            elif key in self.content.items:
                item = self.content.items[key]
                lines.append(t.t("camp.need_line", emoji=item["emoji"], item=t.t(item["name_key"]), have=have, need=n, bar=self._bar(have, n, 8)))
        return lines

    def _missing_text(self, need: dict[str, int], progress: dict[str, int]) -> str:
        """What a work still lacks, as "🪵 Madera ×10 · 🥉50"."""
        missing = {k: n - int(progress.get(k, 0)) for k, n in need.items() if n - int(progress.get(k, 0)) > 0}
        items = {k: n for k, n in missing.items() if k != "coins"}
        text = self._item_list(items) if items else ""
        if missing.get("coins"):
            text = (text + " · " if text else "") + self._money(missing["coins"])
        return text

    def _contribute(self, hero: Hero, need: dict[str, int], progress: dict[str, int]) -> dict[str, int]:
        """Move from the hero to a work everything it still needs that the hero carries (coins from Hero.gold).

        [ES]
        Qué hace: pasa de la mochila (y de las monedas) del héroe a la obra lo que la obra todavía pide y él lleva;
        nunca toma de más. Devuelve lo que se aportó. Si no lleva nada de lo que pide, no toca nada.
        La llaman: _give_to_work (obras) y _give_to_study (conocimiento).
        Si cambia, afecta: qué se lleva cada aporte de la mochila de los miembros.
        """
        given: dict[str, int] = {}
        for key, n in need.items():
            missing = n - int(progress.get(key, 0))
            have = hero.gold if key == "coins" else hero.backpack.get(key, 0)
            give = min(missing, have)
            if give <= 0:
                continue
            if key == "coins":
                hero.gold -= give
            else:
                hero.backpack[key] -= give
                if hero.backpack[key] <= 0:
                    del hero.backpack[key]
            progress[key] = int(progress.get(key, 0)) + give
            given[key] = give
        return given

    def _contribution_lines(self, hero: Hero, given: dict[str, int], name: str) -> list[str]:
        """The "you gave" line: experience and merit per material (upgrades.xp_per_unit, merit_per_unit); coins give none."""
        cfg = self.content.balance["upgrades"]
        units = sum(n for k, n in given.items() if k != "coins")
        xp = units * cfg["xp_per_unit"]
        merit = units * cfg["merit_per_unit"]
        hero.merit += merit
        text = self._missing_text(given, {})
        lines = [self.texts.t("upgrades.given", items=text, name=name, xp=int(xp * self._xp_mult(hero)), merit=merit)]
        return lines + self._give_xp(hero, xp)

    def _upgrades_here(self, hero: Hero) -> tuple[dict[str, Any], str] | None:
        """(camp, "x:y") when the hero stands at the center of a camp it belongs to; None otherwise."""
        key = f"{hero.x}:{hero.y}"
        camp = self.store.get("camp", key)
        if camp and hero.id in camp.get("members", []):
            return camp, key
        return None

    def _upgrades_elsewhere(self, hero: Hero) -> View:
        """Improvements are built at your own camp: the Claro has none (D-98); elsewhere, the camp screen says why."""
        t = self.texts
        if (hero.x, hero.y) == (0, 0):
            return self._claro_view(hero, notice=t.t("upgrades.claro_none"))
        return self._camp_here_view(hero, notice=t.t("upgrades.members_only"))

    def _open_works(self, camp: dict[str, Any], record: dict[str, Any]) -> list[str]:
        """Improvements the camp can build now: unlocked by its level, not built, not retired (catalog order)."""
        level = camp.get("level", 1)
        return [uid for uid, udef in self._upgrade_catalog().items()
                if not udef.get("retired") and uid not in record["built"] and int(udef.get("level", 1)) <= level]

    def _upgrade_action(self, hero: Hero, action_id: str) -> View:
        """Route the buttons of 🔨 Mejoras, its services and the knowledge (D-101). [ES] Qué hace: reparte los botones de esta sección. La llama: _idle_action. Si cambia, afecta: los IDs de botón de las mejoras."""
        if action_id == "upgrades":
            return self._upgrades_view(hero)
        if action_id.startswith("upw"):
            page = action_id[4:]
            return self._works_view(hero, int(page) if page.isdigit() else 0)
        if action_id.startswith("upg:"):
            return self._give_to_work(hero, action_id[4:])
        if action_id == "upsvc":
            return self._services_view(hero)
        if action_id == "crest":
            return self._camp_rest(hero)
        if action_id == "csell":
            return self._camp_sell(hero)
        if action_id in ("tsew", "tchest"):        # the Taller: same recipes as the Claro, back to the Taller screen
            here = self._upgrades_here(hero)
            if not here or not self._camp_service(here[0], "craft"):
                return self._workshop_view(hero)      # only at your camp with its Taller (never a Claro bag by this id)
            view = self._sew_bag(hero) if action_id == "tsew" else self._build_chest(hero)
            return self._workshop_view(hero, notice=view.notice)
        if action_id == "ctaller":
            return self._workshop_view(hero)
        if action_id.startswith("upf:"):
            return self._place_furniture(hero, action_id[4:])
        if action_id.startswith("kstart:"):
            return self._start_study(hero, action_id[7:])
        if action_id == "kgive":
            return self._give_to_study(hero)
        return self._knowledge_view(hero)

    def _camp_member_actions(self, camp: dict[str, Any], hero: Hero, pantry: dict[str, Any] | None) -> list[Action]:
        """The camp screen's buttons for a member, built in ONE place: 4 at most (D-75).

        [ES]
        Qué hace: arma los botones del campamento para un miembro: ⬆️ Agrandar, 🌾 Aportar comida (solo con despensa,
        desde nivel 3), 🛡️ Gremio y 🔨 Mejoras (D-101); sin despensa queda lugar para ↩️ Volver (el menú de abajo
        siempre vuelve). Mientras dura una oleada que todavía no peleaste, 🛡️ Defender (D-99) toma el 4.º lugar:
        el de ↩️ Volver o, con despensa, el de 🔨 Mejoras (vuelve al terminar la oleada).
        La llama: _camp_here_view.
        Si cambia, afecta: tests/test_camps.py, tests/test_pantry.py, tests/test_guilds.py, tests/test_raids.py y
        tests/test_camp_upgrades.py (orden de los botones).
        """
        t = self.texts
        actions = [Action(id="grow", label=t.t("camps.grow_button"))]
        if pantry:
            actions.append(Action(id="campfeed", label=t.t("pantry.feed_button")))
        actions += [Action(id="guild", label=t.t("guild.button")), Action(id="upgrades", label=t.t("upgrades.button"))]
        defend = self._defend_action(camp, hero)    # D-99: while a raid lasts, 🛡️ Defender takes the 4th place
        if defend:
            return actions[:3] + [defend]
        if len(actions) < 4:
            actions.append(Action(id="home", label=t.t("menu.back")))
        return actions

    def _upgrades_view(self, hero: Hero, notice: str | None = None) -> View:
        """🔨 Mejoras: built n of total (castle asks upgrades.castle_min_built), 🛡️ Defensa, the open works with bars.

        [ES]
        Qué hace: muestra las mejoras del campamento: cuántas construyeron de cuántas (y cuántas pide el castillo), la
        🛡️ Defensa, la lista de lo construido, las próximas obras abiertas con su barra de avance y qué se abre en el
        nivel siguiente. D-116: también los 🪑 muebles colocados (con quién los puso) y, si llevas un mueble que el
        campamento no tiene, el aviso de colocarlo en 🔨 Obras. Botones (4 como máximo): 🔨 Obras (obras abiertas y
        muebles para colocar), 🏘️ Servicios (si construyeron alguno), 📚 Conocimiento (con la Biblioteca) y ↩️ Volver.
        Solo para miembros, estando en el campamento; el Claro no tiene (D-98).
        La llaman: el botón 🔨 Mejoras del campamento y los ↩️ Volver de Obras, Servicios y Conocimiento.
        Si cambia, afecta: tests/test_camp_upgrades.py y el recorrido de botones (tope de 4).
        """
        here = self._upgrades_here(hero)
        if not here:
            return self._upgrades_elsewhere(hero)
        camp, key = here
        t = self.texts
        cfg = self.content.balance["upgrades"]
        catalog = self._upgrade_catalog()
        record = self._upgrades(key)
        built = [uid for uid in catalog if uid in record["built"]]
        total = sum(1 for uid, udef in catalog.items() if not udef.get("retired") or uid in record["built"])
        body = [t.t("upgrades.header", camp=camp["name"]),
                t.t("upgrades.count", n=len(built), total=total, need=cfg["castle_min_built"]),
                t.t("upgrades.defense", n=self._camp_defense(camp)), t.t("upgrades.defense_help"), ""]
        body.append(t.t("upgrades.built_line", names=" · ".join(self._upgrade_name(uid) for uid in built)) if built
                    else t.t("upgrades.none_built"))
        placed = [(fid, info) for fid, info in record["furniture"].items() if fid in self.content.items]
        if placed:                                  # D-116: 🪑 the camp's furniture, with who placed it
            body.append(t.t("upgrades.furniture_line", names=" · ".join(
                t.t("upgrades.furniture_by", name=self._item_label(fid), hero=info.get("by", "?")) for fid, info in placed)))
        to_place = self._furniture_to_place(hero, record)
        if to_place:
            body.append(t.t("upgrades.furniture_hint", names=" · ".join(self._item_label(fid) for fid in to_place)))
        works = self._open_works(camp, record)
        if works:
            body += ["", t.t("upgrades.open_title")]
            shown = max(1, int(cfg.get("open_shown", 3)))
            for uid in works[:shown]:
                need = self._work_need(catalog[uid])
                progress = record["works"].get(uid, {})
                have = sum(min(n, int(progress.get(k, 0))) for k, n in need.items())
                full = max(1, sum(need.values()))
                body.append(t.t("upgrades.open_line", name=self._upgrade_name(uid), bar=self._bar(have, full, 8), pct=int(100 * have / full)))
            if len(works) > shown:
                body.append(t.t("upgrades.open_more", n=len(works) - shown))
        level = camp.get("level", 1)
        locked = [uid for uid, udef in catalog.items()
                  if not udef.get("retired") and uid not in record["built"] and int(udef.get("level", 1)) > level]
        if locked:
            next_level = min(int(catalog[uid].get("level", 1)) for uid in locked)
            names = [self._upgrade_name(uid) for uid in locked if int(catalog[uid].get("level", 1)) == next_level]
            body.append(t.t("upgrades.locked_line", level=next_level, names=" · ".join(names), n=len(names)))
        services = {name for uid in built for name in (catalog[uid].get("service") or {})}
        actions = []
        if works or to_place:
            actions.append(Action(id="upw", label=t.t("upgrades.works_button", n=len(works) + len(to_place))))
        if services & {"rest_price", "sell_ratio", "craft", "sell_gear"}:
            actions.append(Action(id="upsvc", label=t.t("upgrades.services_button")))
        if "knowledge" in services:
            actions.append(Action(id="know", label=t.t("knowledge.button")))
        else:
            library = next((udef for udef in catalog.values() if (udef.get("service") or {}).get("knowledge")), None)
            if library:
                body.append(t.t("knowledge.locked", level=library.get("level", 1)))
        actions.append(Action(id="claro", label=t.t("menu.back")))
        return View(kind="camp_upgrades", title=t.t("upgrades.title"), body=body, actions=actions, notice=notice)

    def _works_view(self, hero: Hero, page: int = 0, notice: str | None = None) -> View:
        """🔨 Obras: the improvements the camp can build now, with a bar per material and a 🤲 button each (D-101).

        [ES]
        Qué hace: lista las obras abiertas (por el nivel del campamento) con lo que pide cada una y lo aportado. Cada
        botón 🤲 aporta todo lo que esa obra todavía pide y llevas (también sus monedas). Al final, los 🪑 muebles que
        llevas y el campamento no tiene, cada uno con su botón 🪑 Colocar (D-116). De a 3, o de a 2 con ➡️ Ver más si
        son más (4 botones como máximo, D-75).
        La llaman: 🔨 Obras de la pantalla de mejoras, cada aporte (vuelve a la página de esa obra) y _place_furniture.
        Si cambia, afecta: cómo aportan los miembros (tests/test_camp_upgrades.py).
        """
        here = self._upgrades_here(hero)
        if not here:
            return self._upgrades_elsewhere(hero)
        camp, key = here
        t = self.texts
        catalog = self._upgrade_catalog()
        record = self._upgrades(key)
        entries = self._works_entries(hero, camp, record)
        if not entries:
            return self._upgrades_view(hero, notice=notice or t.t("upgrades.no_works"))
        per = 3 if len(entries) <= 3 else 2
        pages = (len(entries) + per - 1) // per
        page %= pages
        body = [t.t("upgrades.works_intro")]
        if any(kind == "furn" for kind, _ in entries):
            body.append(t.t("upgrades.furniture_intro"))
        if pages > 1:
            body.append(t.t("upgrades.page", n=page + 1, total=pages))
        actions = []
        for kind, uid in entries[page * per: page * per + per]:
            if kind == "furn":                      # D-116: 🪑 a furniture piece you carry, ready to place
                name = self._item_label(uid)
                body += ["", t.t("upgrades.furniture_entry", name=name, desc=t.t(self.content.items[uid]["desc_key"]))]
                actions.append(Action(id=f"upf:{uid}", label=t.t("upgrades.furniture_button", name=name)))
                continue
            udef = catalog[uid]
            defense = int(udef.get("defense", 0))
            title = t.t("upgrades.work_line", name=self._upgrade_name(uid), level=udef.get("level", 1))
            body += ["", title + (t.t("upgrades.defense_mark", n=defense) if defense else ""), t.t(udef["desc_key"])]
            body += self._need_lines(self._work_need(udef), record["works"].get(uid, {}))
            actions.append(Action(id=f"upg:{uid}", label=t.t("upgrades.give_button", name=self._upgrade_name(uid))))
        if pages > 1:
            actions.append(Action(id=f"upw:{(page + 1) % pages}", label=t.t("upgrades.more")))
        actions.append(Action(id="upgrades", label=t.t("menu.back")))
        return View(kind="camp_works", title=t.t("upgrades.works_title"), body=body, actions=actions, notice=notice)

    def _give_to_work(self, hero: Hero, uid: str) -> View:
        """🤲 Aportar to one improvement: any member at the camp, no approval; when complete it is built for ever.

        [ES]
        Qué hace: el miembro aporta a la obra lo que lleva de lo que pide (_contribute) y gana experiencia y mérito por
        material. Si con eso se completa, la mejora queda construida para siempre y se avisa a los demás miembros.
        Si no lleva nada de lo que pide, avisa qué falta y no toca nada. Ocupado (viajando, explorando...) no aporta.
        La llaman: los botones 🤲 de 🔨 Obras (upg:<id>).
        Si cambia, afecta: el ritmo de las mejoras y el castillo (upgrades.castle_min_built).
        """
        here = self._upgrades_here(hero)
        if not here:
            return self._upgrades_elsewhere(hero)
        camp, key = here
        t = self.texts
        if hero.activity:
            return self._works_view(hero, notice=t.t("activity.busy"))
        record = self._upgrades(key)
        works = self._open_works(camp, record)
        if uid not in works:
            return self._works_view(hero)
        entries = self._works_entries(hero, camp, record)
        per = 3 if len(entries) <= 3 else 2
        page = entries.index(("work", uid)) // per
        udef = self._upgrade_catalog()[uid]
        need = self._work_need(udef)
        progress = record["works"].setdefault(uid, {})
        given = self._contribute(hero, need, progress)
        name = self._upgrade_name(uid)
        if not given:
            return self._works_view(hero, page, notice=t.t("upgrades.nothing_to_give", name=name, items=self._missing_text(need, progress)))
        lines = self._contribution_lines(hero, given, name)
        lines += self._story_event(hero, "build", n=sum(n for k, n in given.items() if k != "coins"))     # D-117: camp tasks
        if all(int(progress.get(k, 0)) >= n for k, n in need.items()):
            record["built"][uid] = self.clock.now()
            record["works"].pop(uid, None)
            lines.append(t.t("upgrades.built", name=name))
            news = View(kind="camp_news", title=t.t("upgrades.built_push_title"),
                        body=[t.t("upgrades.built_push", hero=hero.name, name=name, camp=camp["name"])])
            for member in camp["members"]:
                if member != hero.id:
                    self._push(member, news)
            page = 0
        self.store.put("upgrades", key, record)
        return self._works_view(hero, page, notice="\n".join(lines))

    def _furniture_to_place(self, hero: Hero, record: dict[str, Any]) -> list[str]:
        """🪑 Furniture pieces the hero carries that this camp does not have yet (D-116), in items.yaml order."""
        placed = record.get("furniture") or {}
        return [fid for fid, item in self.content.items.items()
                if item.get("kind") == "furniture" and hero.backpack.get(fid, 0) > 0 and fid not in placed]

    def _works_entries(self, hero: Hero, camp: dict[str, Any], record: dict[str, Any]) -> list[tuple[str, str]]:
        """What 🔨 Obras lists, in order: ("work", improvement id) for the open works, then ("furn", item id) for the
        🪑 furniture the hero can place (D-116). One list, so the pages of the screen and of each 🤲 match."""
        return [("work", uid) for uid in self._open_works(camp, record)] + [("furn", fid) for fid in self._furniture_to_place(hero, record)]

    def _place_furniture(self, hero: Hero, fid: str) -> View:
        """🪑 Colocar: a member places a furniture piece in their camp, for ever; one of each piece per camp (D-116).

        [ES]
        Qué hace: el miembro, en el centro de su campamento, coloca un mueble de la 🪑 Carpintería que lleva en la
        mochila: sale de la mochila, queda en el campamento para siempre con el nombre de quien lo puso y su bono
        (items.yaml "effect": 🛏️ Literas +1 miembro, 🗄️ Armero +1 de 🛡️ Defensa) vale para todos los miembros. Si el
        campamento ya tiene ese mueble, avisa y no gasta nada (uno de cada uno: un segundo igual no suma). Ocupado
        (viajando, explorando...) no se coloca. Avisa a los demás miembros.
        La llaman: los botones 🪑 Colocar de 🔨 Obras (upf:<id>).
        Si cambia, afecta: el cupo de miembros (_members_cap) y la 🛡️ Defensa (_camp_defense, oleadas).
        """
        here = self._upgrades_here(hero)
        if not here:
            return self._upgrades_elsewhere(hero)
        camp, key = here
        t = self.texts
        item = self.content.items.get(fid, {})
        if item.get("kind") != "furniture" or hero.backpack.get(fid, 0) <= 0:
            return self._works_view(hero)
        if hero.activity:
            return self._works_view(hero, notice=t.t("activity.busy"))
        record = self._upgrades(key)
        name = self._item_label(fid)
        if fid in record["furniture"]:
            return self._works_view(hero, notice=t.t("upgrades.furniture_already", name=name, camp=camp["name"]))
        hero.backpack[fid] -= 1
        if hero.backpack[fid] <= 0:
            del hero.backpack[fid]
        record["furniture"][fid] = {"by": hero.name, "id": hero.id, "at": self.clock.now()}
        self.store.put("upgrades", key, record)
        desc = t.t(item["desc_key"])
        news = View(kind="camp_news", title=t.t("upgrades.furniture_push_title"),
                    body=[t.t("upgrades.furniture_push", hero=hero.name, name=name, camp=camp["name"], desc=desc)])
        for member in camp["members"]:
            if member != hero.id:
                self._push(member, news)
        return self._works_view(hero, notice=t.t("upgrades.furniture_placed", name=name, camp=camp["name"], desc=desc))

    def _castle_upgrades(self, camp: dict[str, Any]) -> list[tuple[str, bool]]:
        """D-101: on the step to castle (8 → 9) the camp needs upgrades.castle_min_built improvements built; else [].

        [ES]
        Qué hace: dice si el campamento ya construyó las mejoras que pide el castillo (15). Vacío en cualquier otro
        nivel: los castillos que ya existen siguen creciendo sin pedir nada más.
        La llaman: _grow_view (lo muestra con ✅ o ▫️) y _grow_camp (lo exige).
        Si cambia, afecta: quién llega a castillo (balance.yaml upgrades.castle_min_built).
        """
        need = int(self.content.balance.get("upgrades", {}).get("castle_min_built", 0))
        castle = next((s["from_level"] for s in self.content.balance["camps"]["stages"] if s["id"] == "castillo"), None)
        if not need or castle is None or camp.get("level", 1) + 1 != castle:
            return []
        n = len(self._built(camp))
        return [(self.texts.t("upgrades.castle_line", need=need, n=n), n >= need)]

    def _services_view(self, hero: Hero, notice: str | None = None) -> View:
        """🏘️ Servicios: what the camp built to use there: 🛏️ Refugio, 💱 trade, 🧵 Taller (and the 🔨 Herrería note).

        [ES]
        Qué hace: junta los servicios construidos: 🛏️ Refugio (curarse como en la posada del Claro, más barato),
        💱 Vender materiales (Puesto de trueque; la comida nunca), 🧵 Taller (bolsas y cofres) y la nota de la
        🔨 Herrería (vender equipo desde 🛡️ Equipo). 4 botones como máximo: Refugio, Vender, Taller y ↩️ Volver.
        Las estaciones de oficio (D-109) se abren desde el 🧵 Taller; sin Taller y con 🔨 Herrería, ⚒️ Oficios toma su lugar.
        La llama: 🏘️ Servicios de 🔨 Mejoras, y cada servicio al terminar.
        Si cambia, afecta: qué se puede hacer en el campamento sin volver al Claro.
        """
        here = self._upgrades_here(hero)
        if not here:
            return self._upgrades_elsewhere(hero)
        camp, _ = here
        t = self.texts
        body = [t.t("upgrades.services_intro")]
        actions = []
        rest = self._camp_service(camp, "rest_price")
        if rest:
            price = self._money(int(rest["rest_price"]))
            body.append(t.t("upgrades.rest_line", price=price))
            actions.append(Action(id="crest", label=t.t("upgrades.rest_button", price=price)))
        trade = self._camp_service(camp, "sell_ratio")
        if trade:
            body.append(t.t("upgrades.trade_line"))
            sellable = {i: n for i, n in hero.backpack.items()
                        if n > 0 and self.content.items.get(i, {}).get("kind") == "material" and not self.content.items[i].get("food")}
            if sellable:
                total = sum(max(1, int(self.content.items[i]["price"] * trade["sell_ratio"])) * n for i, n in sellable.items())
                body.append(t.t("shop.sell_line", items=self._item_list(sellable), total=self._money(total)))
                actions.append(Action(id="csell", label=t.t("shop.sell_all_button", total=self._money(total))))
            else:
                body.append(t.t("upgrades.nothing_to_sell"))
        if self._camp_service(camp, "craft"):
            body.append(t.t("upgrades.workshop_line"))
            actions.append(Action(id="ctaller", label=t.t("upgrades.workshop_button")))
        if self._camp_service(camp, "sell_gear"):
            body.append(t.t("upgrades.smithy_line"))
            if not self._camp_service(camp, "craft") and self._stations_here(hero)[0]:
                actions.append(Action(id="oficios", label=t.t("prof.button")))   # D-109: no Taller: the Herrería's stations go here
        if len(body) == 1:
            body.append(t.t("upgrades.no_services"))
        body += ["", self._status_line(hero)]
        actions.append(Action(id="upgrades", label=t.t("menu.back")))
        return View(kind="camp_services", title=t.t("upgrades.services_title"), body=body, actions=actions[:4], notice=notice)

    def _camp_rest(self, hero: Hero) -> View:
        """🛏️ Refugio: like the Claro inn (pay, sleep, wake with full health), cheaper, at your camp (D-101)."""
        t = self.texts
        here = self._upgrades_here(hero)
        if not here:
            return self._upgrades_elsewhere(hero)
        service = self._camp_service(here[0], "rest_price")
        if not service:
            return self._services_view(hero)
        if hero.activity:
            return self._services_view(hero, notice=t.t("activity.busy"))
        if hero.hp >= hero_stats(self._kit(hero), hero.level)["max_hp"]:
            return self._services_view(hero, notice=t.t("inn.full_hp"))     # never charged for a useless night
        price = int(service["rest_price"])
        if hero.gold < price:
            return self._services_view(hero, notice=t.t("shop.no_gold"))
        hero.gold -= price
        seconds = self._seconds(service.get("rest_minutes", self.content.balance["inn"]["minutes"]))
        hero.activity = {"kind": "rest", "until": self.clock.now() + seconds}
        return self._activity_view(hero, notice=t.t("upgrades.rest_started", price=self._money(price), time=self._fmt_duration(seconds)))

    def _camp_sell(self, hero: Hero) -> View:
        """💱 Puesto de trueque: sell every material you carry at the camp; food never (it feeds the pantry, D-93)."""
        t = self.texts
        here = self._upgrades_here(hero)
        if not here:
            return self._upgrades_elsewhere(hero)
        service = self._camp_service(here[0], "sell_ratio")
        if not service:
            return self._services_view(hero)
        if hero.activity:
            return self._services_view(hero, notice=t.t("activity.busy"))
        total, sold = 0, {}
        for item_id, n in list(hero.backpack.items()):
            item = self.content.items.get(item_id, {})
            if item.get("kind") == "material" and not item.get("food") and not item.get("keep") and n > 0:
                total += max(1, int(item["price"] * service["sell_ratio"])) * n
                sold[item_id] = n
                del hero.backpack[item_id]
        if not sold:
            return self._services_view(hero, notice=t.t("upgrades.nothing_to_sell"))
        total, trade = self._merchant_sale(hero, total, "barter")   # D-116: 💱 Comercio (D-141: 🐪 Caravanero)
        hero.gold += total
        lines = [t.t("shop.sold_all", items=self._item_list(sold), total=self._money(total))] + trade + self._tutorial(hero, "sell")
        lines += self._story_event(hero, "sell", n=sum(sold.values()), coins=total)              # D-117
        return self._services_view(hero, notice="\n".join(lines))

    def _can_craft(self, hero: Hero) -> bool:
        """Bags and chests are made in the Claro, or at your camp once it built the 🧵 Taller (D-101); never while busy."""
        if hero.activity:
            return False
        if (hero.x, hero.y) == (0, 0):
            return True
        here = self._upgrades_here(hero)
        return bool(here) and self._camp_service(here[0], "craft") is not None

    def _sells_gear_here(self, hero: Hero) -> bool:
        """Your camp's 🔨 Herrería buys the gear you do not use, like the Claro (D-101)."""
        here = None if hero.activity else self._upgrades_here(hero)
        return bool(here) and self._camp_service(here[0], "sell_gear") is not None

    def _workshop_view(self, hero: Hero, notice: str | None = None) -> View:
        """🧵 Taller: sew 💰 bags and assemble 🪎 chests at the camp, with the Claro's recipes (D-101); ⚒️ Oficios opens the
        camp's profession stations (D-109). [ES] 4 botones: Coser, Armar cofre, ⚒️ Oficios y ↩️ Volver."""
        here = self._upgrades_here(hero)
        if not here:
            return self._upgrades_elsewhere(hero)
        t = self.texts
        if not self._camp_service(here[0], "craft"):
            return self._upgrades_view(hero, notice=notice)
        cfg = self.content.balance["currency"]
        bags_need, materials = self._chest_recipe()
        body = [t.t("upgrades.workshop_intro"), "",
                t.t("wallet.bags", n=hero.bags),
                t.t("upgrades.bag_recipe", items=self._item_list(cfg["bag_recipe"]), coins=self._money(cfg["bag_coins"])), "",
                t.t("wallet.chests", n=hero.chests),
                t.t("upgrades.chest_recipe", bags=bags_need, items=self._item_list(materials)),
                "", t.t("hero.gold_line", gold=self._money(hero.gold))]
        if self._stations_here(hero)[0]:                # D-109: the Taller's stations (and the Herrería's) for ⚒️ Oficios
            body.insert(1, t.t("prof.workshop_line"))
        actions = [Action(id="tsew", label=t.t("wallet.sew_button")), Action(id="tchest", label=t.t("wallet.chest_button")),
                   Action(id="oficios", label=t.t("prof.button")), Action(id="upsvc", label=t.t("menu.back"))]
        return View(kind="camp_workshop", title=t.t("upgrades.workshop_title"), body=body, actions=actions, notice=notice)

    def _knowledge_view(self, hero: Hero, notice: str | None = None) -> View:
        """📚 Conocimiento: studies the camp learns with its Biblioteca, one at a time, paid by the members together.

        [ES]
        Qué hace: muestra los estudios (Herramientas, Cartografía, Rastreo): ✅ aprendidos, 📖 el que estudian ahora
        con sus barras, ▫️ los que faltan. Sin estudio en curso, un botón 📖 por estudio para empezarlo (cualquier
        miembro); con uno en curso, 🤲 Aportar al estudio. Más ↩️ Volver: 4 botones como máximo.
        La llaman: 📚 Conocimiento de 🔨 Mejoras (solo con la Biblioteca construida).
        Si cambia, afecta: tests/test_camp_upgrades.py.
        """
        here = self._upgrades_here(hero)
        if not here:
            return self._upgrades_elsewhere(hero)
        camp, key = here
        t = self.texts
        if not self._camp_service(camp, "knowledge"):
            return self._upgrades_view(hero, notice=notice or t.t("upgrades.need_library"))
        tech = self._upgrades(key)["tech"]
        done, current = tech.get("done", []), tech.get("current")
        body = [t.t("knowledge.intro"), t.t("knowledge.rule"), ""]
        waiting = []
        for tid, tdef in self._tech_catalog().items():
            if tdef.get("retired") and tid not in done:
                continue
            name, desc = self._tech_name(tid), t.t(tdef["desc_key"])
            if tid in done:
                body.append(t.t("knowledge.done_line", name=name, desc=desc))
            elif tid == current:
                body.append(t.t("knowledge.current_line", name=name, desc=desc))
                body += self._need_lines(self._work_need(tdef), tech.get("progress", {}))
            else:
                body.append(t.t("knowledge.open_line", name=name, desc=desc))
                waiting.append(tid)
        actions = []
        if current:
            actions.append(Action(id="kgive", label=t.t("knowledge.give_button")))
        elif waiting:
            body += ["", t.t("knowledge.choose")]
            actions += [Action(id=f"kstart:{tid}", label=t.t("knowledge.start_button", name=self._tech_name(tid))) for tid in waiting[:3]]
        else:
            body += ["", t.t("knowledge.all_done")]
        actions.append(Action(id="upgrades", label=t.t("menu.back")))
        return View(kind="camp_knowledge", title=t.t("knowledge.title"), body=body, actions=actions, notice=notice)

    def _start_study(self, hero: Hero, tid: str) -> View:
        """📖 Start one study (any member at the camp with the Biblioteca), only if no other is under way (one at a time)."""
        here = self._upgrades_here(hero)
        if not here:
            return self._upgrades_elsewhere(hero)
        camp, key = here
        t = self.texts
        if not self._camp_service(camp, "knowledge"):
            return self._knowledge_view(hero)
        record = self._upgrades(key)
        tech = record["tech"]
        tdef = self._tech_catalog().get(tid)
        if tech.get("current"):
            return self._knowledge_view(hero, notice=t.t("knowledge.one_at_a_time"))
        if not tdef or tdef.get("retired") or tid in tech.get("done", []):
            return self._knowledge_view(hero)
        tech["current"], tech["progress"] = tid, {}
        self.store.put("upgrades", key, record)
        return self._knowledge_view(hero, notice=t.t("knowledge.started", name=self._tech_name(tid)))

    def _give_to_study(self, hero: Hero) -> View:
        """🤲 Aportar al estudio: like a work; when complete the camp knows it for ever and the members are told."""
        here = self._upgrades_here(hero)
        if not here:
            return self._upgrades_elsewhere(hero)
        camp, key = here
        t = self.texts
        if not self._camp_service(camp, "knowledge"):
            return self._knowledge_view(hero)
        if hero.activity:
            return self._knowledge_view(hero, notice=t.t("activity.busy"))
        record = self._upgrades(key)
        tech = record["tech"]
        tid = tech.get("current")
        tdef = self._tech_catalog().get(tid or "")
        if not tdef:
            return self._knowledge_view(hero)
        need = self._work_need(tdef)
        progress = tech.setdefault("progress", {})
        given = self._contribute(hero, need, progress)
        name = self._tech_name(tid)
        if not given:
            return self._knowledge_view(hero, notice=t.t("upgrades.nothing_to_give", name=name, items=self._missing_text(need, progress)))
        lines = self._contribution_lines(hero, given, name)
        lines += self._story_event(hero, "build", n=sum(n for k, n in given.items() if k != "coins"))     # D-117: camp tasks
        if all(int(progress.get(k, 0)) >= n for k, n in need.items()):
            tech.setdefault("done", []).append(tid)
            tech["current"], tech["progress"] = None, {}
            lines.append(t.t("knowledge.done", name=name))
            news = View(kind="camp_news", title=t.t("knowledge.push_title"),
                        body=[t.t("knowledge.push", hero=hero.name, name=name, camp=camp["name"])])
            for member in camp["members"]:
                if member != hero.id:
                    self._push(member, news)
        self.store.put("upgrades", key, record)
        return self._knowledge_view(hero, notice="\n".join(lines))

    # ------------------------------------------------------------------ chained professions, phase 1 (D-109)

    def _prof_cfg(self) -> dict[str, Any]:
        return self.content.balance["professions"]

    def _prof_catalog(self) -> dict[str, dict[str, Any]]:
        """The professions of content/professions.yaml, in file order (gathering, refining, crafting)."""
        return (self.content.professions or {}).get("professions") or {}

    def _recipes(self) -> dict[str, dict[str, Any]]:
        """Every recipe that can be made, in file order (retired ones are hidden)."""
        recipes = (self.content.professions or {}).get("recipes") or {}
        return {rid: rdef for rid, rdef in recipes.items() if not rdef.get("retired")}

    def _prof_rank(self, hero: Hero, pid: str) -> int:
        """A hero's rank (1-100) in a profession, from its profession xp (rank 1 if never started).

        [ES]
        Qué hace: da el rango de un oficio para este héroe (1 si nunca lo empezó), con la curva de
        balance.yaml professions.rank_formula.
        La llaman: todas las funciones de esta sección.
        Si cambia, afecta: qué recetas y materiales raros tiene abiertos cada uno.
        """
        cfg = self._prof_cfg()
        return rank_of(hero.professions.get(pid, 0), cfg["rank_formula"], cfg["max_rank"])

    def _prof_name(self, pid: str) -> str:
        pdef = self._prof_catalog().get(pid, {})
        return f"{pdef.get('emoji', '')} {self.texts.t(pdef.get('name_key', f'profession.{pid}.name'))}".strip()

    def _rank_title(self, rank: int) -> str:
        """Aprendiz, Oficial, Experto, Artesano, Maestro or Gran Maestro (content/professions.yaml "ranks")."""
        return self.texts.t(f"prof.rank.{rank_title(rank, (self.content.professions or {}).get('ranks') or [])}")

    def _item_label(self, item_id: str) -> str:
        item = self.content.items[item_id]
        return f"{item['emoji']} {self.texts.t(item['name_key'])}"

    def _recipe_name(self, rid: str) -> str:
        """What a recipe makes, as "🟢🗡️ Espada forjada" (gear, with its rarity) or "🧪 Poción de vida ×2"."""
        out_id, count = next(iter(self._recipes()[rid]["output"].items()))
        name = self._gear_name(out_id) if self.content.items[out_id].get("kind") == "gear" else self._item_label(out_id)
        return name + (f" ×{count}" if count > 1 else "")

    def _merchant_sale(self, hero: Hero, base: int, sale: str = "goods") -> tuple[int, list[str]]:
        """A sale to the merchant or a camp barter: the 💱 Comercio perk adds coins and the sale raises Comercio (D-116).

        [ES]
        Qué hace: a lo que pagan por una venta (al mercader del Claro, al 💱 Puesto de trueque del campamento o al
        vender equipo) le suma el beneficio del 💱 Comercio (hasta +20 % al rango 100) y le da al oficio 1 de
        experiencia por cada 🥉 de la venta. Devuelve el total a pagar y las líneas de subida de rango. D-141: "sale" dice
        qué venta es ("goods" materiales al mercader, "barter" el trueque del campamento, "gear" equipo) y suma el efecto
        "coins" de la 🎓 especialización del Comercio que coincide (📦 Abastecedor, 🐪 Caravanero, 🛡️ Tratante de equipo).
        La llaman: _sell, _camp_sell y _sell_gear.
        Si cambia, afecta: cuántas monedas entran al juego por ventas (sumidero/fuente, balance.yaml professions.trade_xp_per_coin).
        """
        total = int(round(base * (1 + self._perks(hero)["sell"] + self._pspec_bonus(hero, "coins", sale=sale))))   # D-141
        lines = self._prof_gain(hero, "comercio", int(base * self.content.balance["professions"]["trade_xp_per_coin"]))
        return total, lines

    def _prof_gain(self, hero: Hero, pid: str, xp: int) -> list[str]:
        """Add profession xp; on a new rank, a line (and ProfessionRankUp) plus the recipes or rare find it opens.

        [ES]
        Qué hace: suma experiencia a un oficio y, si sube de rango, avisa el rango nuevo, las recetas que abre y el
        material raro que empieza a aparecer; para el 🧭 Explorador (D-112), lo que abre en el mapa y, al 100, el título.
        Nunca resta (el rango no baja).
        La llaman: _trade_gather (recolectar), _trade_loot (botín de bestias), _make (refinar y fabricar), _explore_step y
        _infiltrate (🧭 Explorador) y _merchant_sale (💱 Comercio).
        D-141: la misma experiencia sube el dominio de las 🎓 especializaciones que tienes en ese oficio, y avisa cuando el
        oficio llega al 25 o al 75 (ya puedes elegir) o una especialización abre su receta exclusiva (_pspec_gain). Las recetas
        exclusivas que no puedes hacer no se anuncian.
        Si cambia, afecta: el avance de todos los oficios y los avisos de subida.
        """
        if xp <= 0 or pid not in self._prof_catalog():
            return []
        xp = int(round(xp * (1 + self._origin_prof_bonus(hero, pid))))      # D-117: the origin's trait (e.g. ⛏️ Minero +15 %)
        before = self._prof_rank(hero, pid)
        hero.professions[pid] = hero.professions.get(pid, 0) + int(xp)
        after = self._prof_rank(hero, pid)
        spec_lines = self._pspec_gain(hero, pid, int(xp), before, after)     # D-141: 🎓 mastery, "you can choose" and exclusive recipes
        if after <= before:
            return spec_lines
        self.bus.publish(ProfessionRankUp(hero.id, pid, after))
        t = self.texts
        lines = [t.t("prof.rank_up", name=self._prof_name(pid), rank=after, title=self._rank_title(after))]
        opened = [self._recipe_name(rid) for rid, rdef in self._recipes().items()
                  if rdef["profession"] == pid and before < int(rdef.get("min_rank", 1)) <= after and self._pspec_recipe_ok(hero, rdef)]
        if opened:
            lines.append(t.t("prof.unlocked", items=", ".join(opened)))
        rare = self._prof_catalog()[pid].get("rare")
        if rare and before < int(rare["min_rank"]) <= after:
            lines.append(t.t("prof.rare_unlocked", item=self._item_label(rare["item"])))
        lines += self._explorer_unlocks(hero, pid, before, after)     # D-112: what the 🧭 Explorador sees now (and its title)
        lines += self._ench_unlocks(pid, before, after)               # D-115: the ✨ enchantments a new rank opens
        return lines + spec_lines

    def _trade_gather(self, hero: Hero, got: dict[str, int], activity: dict[str, Any]) -> list[str]:
        """One gathering round raises its gathering professions (🪓 ⛏️ 🌿): profession xp per unit, an extra unit
        now and then by rank (up to the backpack's space, D-90) and, from the profession's rank, a rare find.

        It uses its own draw, so it never changes what the round itself gathered or whether a fight starts.

        [ES]
        Qué hace: después de cada vuelta de recolección, suma 1 de experiencia de oficio por unidad al oficio que la
        junta (madera → leñador; piedra, metal y arcilla → minero; hierba y fibra → herbolario), sortea una unidad más
        por unidad según el rango (professions.rank_yield, sin pasar el espacio de la mochila) y, desde el rango del
        raro, la 💠 gema en bruto o la 🌸 flor de luna. Agrega lo extra a `got` (cuenta para el resumen y el gremio).
        D-141: la 🎓 especialización suma a la unidad de más ("yield": ⚙️ Metales, 🪓 Tala rápida...) y sus hallazgos ("find":
        💠 Gemas, 🌸 Flores raras) se sortean aparte, una vez por vuelta del oficio.
        La llama: _gather_step.
        Si cambia, afecta: el ritmo de los oficios de recolección y cuánto material raro entra al juego.
        """
        if not got:
            return []
        cfg = self._prof_cfg()
        catalog = self._prof_catalog()
        rng = Rng(int(hash_unit(self.world_seed, hero.id, "trade", activity.get("until", 0), activity.get("done", 0)) * 2**31))
        gained: dict[str, int] = {}
        for res in list(got):
            pid = gatherer_of(res, catalog)
            if not pid:
                continue
            rank = self._prof_rank(hero, pid)
            chance = rank * cfg["rank_yield"] + self._pspec_bonus(hero, "yield", item=res)   # D-141: 🎓 e.g. ⚙️ Metales +20 %
            extra = sum(1 for _ in range(got[res]) if rng.chance(chance))
            extra = min(extra, max(0, self._bag_cap(hero) - self._bag_used(hero)))     # gathering stops at the space (D-90)
            if extra:
                self._bag_add(hero, res, extra)
                got[res] += extra
            gained[pid] = gained.get(pid, 0) + got[res] * cfg["gather_xp_per_unit"]
        lines: list[str] = []
        trade = activity.setdefault("trade", {})
        for pid, xp in gained.items():
            rank = self._prof_rank(hero, pid)
            rare = catalog[pid].get("rare")
            if rare and rank >= int(rare["min_rank"]) and rare["item"] in self.content.items:
                if rng.chance(cfg["rare_chance"] + cfg["rare_per_rank"] * (rank - int(rare["min_rank"]))):
                    self._bag_add(hero, rare["item"], 1)          # a find: never lost (D-90)
                    got[rare["item"]] = got.get(rare["item"], 0) + 1
            for item_id, chance in self._pspec_finds(hero, pid).items():     # D-141: 💠 Gemas, 🌸 Flores raras (own draw)
                find_rng = Rng(int(hash_unit(self.world_seed, hero.id, "spec_find", pid, item_id, activity.get("until", 0),
                                             activity.get("done", 0)) * 2**31))
                if find_rng.chance(chance):
                    self._bag_add(hero, item_id, 1)               # a find: never lost (D-90)
                    got[item_id] = got.get(item_id, 0) + 1
            trade[pid] = trade.get(pid, 0) + xp
            lines += self._prof_gain(hero, pid, xp)
        return lines

    def _trade_summary(self, trade: dict[str, int]) -> str:
        """⚒️ Oficios: 🪓 Leñador +12 · 🌿 Herbolario +7 (end of a gathering batch)."""
        parts = [f"{self._prof_name(pid)} +{xp}" for pid, xp in trade.items() if xp]
        return self.texts.t("prof.summary", items=" · ".join(parts))

    def _trade_loot(self, hero: Hero, item_id: str, count: int, lines: list[str], seed: int) -> int:
        """🔪 Desollador: carne and piel from a beast raise the profession; by rank, an extra unit now and then.

        Own draw (never changes the fight's other loot). Returns the extra units, already in the backpack.

        [ES]
        Qué hace: cuando una bestia suelta 🍖 carne o 🦌 piel, suma 1 de experiencia de Desollador por unidad y, según
        el rango, a veces una unidad más (el botín nunca se pierde, D-90). Los avisos de rango van a `lines`. D-141: la
        🎓 especialización suma a esa unidad de más (🦌 Pieles finas, 🍖 Carnicería) y 🦴 Trofeos sortea una 💠 gema por unidad.
        La llama: _end_combat (botín de cada victoria).
        Si cambia, afecta: cuánta carne y piel entra al juego (despensa y Curtiduría).
        """
        catalog = self._prof_catalog()
        pid = gatherer_of(item_id, catalog)
        if not pid or item_id not in (catalog[pid].get("skins") or []) or count <= 0:
            return 0
        cfg = self._prof_cfg()
        rank = self._prof_rank(hero, pid)
        rng = Rng(int(hash_unit(self.world_seed, hero.id, "skin", seed, item_id) * 2**31))
        chance = rank * cfg["rank_yield"] + self._pspec_bonus(hero, "yield", item=item_id)    # D-141: 🦌 Pieles finas, 🍖 Carnicería
        extra = sum(1 for _ in range(count) if rng.chance(chance))
        if extra:
            hero.backpack[item_id] = hero.backpack.get(item_id, 0) + extra
        finds = self._pspec_finds(hero, pid)                  # D-141: 🦴 Trofeos, per unit skinned (own draw)
        if finds:
            find_rng = Rng(int(hash_unit(self.world_seed, hero.id, "spec_find", seed, item_id) * 2**31))
            found = {f: n for f, chance in finds.items() if (n := sum(1 for _ in range(count + extra) if find_rng.chance(chance)))}
            for found_id, n in found.items():
                hero.backpack[found_id] = hero.backpack.get(found_id, 0) + n      # a find: never lost (D-90)
            if found:
                lines.append(self.texts.t("spec.found", items=self._item_list(found)))
        lines += self._prof_gain(hero, pid, (count + extra) * cfg["gather_xp_per_unit"])
        return extra

    def _stations_here(self, hero: Hero) -> tuple[list[str], str | None]:
        """(stations, "claro" | "camp") the hero can use where it stands, or ([], None); never while busy.

        [ES]
        Qué hace: dice qué estaciones de oficio hay donde está el héroe: todas las básicas en el Claro; en el centro de
        su campamento, las que abren sus mejoras construidas (🧵 Taller y 🔨 Herrería, content/professions.yaml
        "stations"). Ocupado (viaje, exploración...) no hay ninguna: una actividad a la vez.
        La llaman: ⚒️ Oficios, las estaciones, las recetas, _make, el Taller y los servicios del campamento.
        Si cambia, afecta: dónde se puede refinar y fabricar.
        """
        if hero.activity:
            return [], None
        stations = (self.content.professions or {}).get("stations") or {}
        if (hero.x, hero.y) == (0, 0):
            return list(stations.get("claro") or []), "claro"
        here = self._upgrades_here(hero)
        if not here:
            return [], None
        built = self._built(here[0])
        found: list[str] = []
        for uid, sids in (stations.get("camp") or {}).items():
            if uid in built:
                found += [sid for sid in sids if sid not in found]
        return (found, "camp") if found else ([], None)

    def _prof_back(self, hero: Hero) -> str:
        """Where ↩️ Volver of ⚒️ Oficios goes: the Claro, your camp's 🧵 Taller or services, or the hero sheet."""
        if (hero.x, hero.y) == (0, 0):
            return "claro"
        here = self._upgrades_here(hero)
        if here:
            return "ctaller" if self._camp_service(here[0], "craft") else "upsvc"
        return "hero"

    def _make_bonus(self, rank: int, where: str | None) -> float:
        """Chance of one more unit per refining: rank × professions.rank_yield, + professions.camp_bonus at your camp."""
        cfg = self._prof_cfg()
        return rank * cfg["rank_yield"] + (cfg["camp_bonus"] if where == "camp" else 0.0)

    def _makes_masterworks(self, pid: str) -> bool:
        """True if the profession has a recipe whose output has a ✒️ masterwork twin (gear pieces, D-116)."""
        return any(rdef["profession"] == pid and masterwork_id(out) in self.content.items
                   for rdef in self._recipes().values() for out in rdef["output"])

    def _masterwork_chance(self, hero: Hero, pid: str) -> float:
        """Chance that one gear piece made now with this profession comes out a ✒️ masterwork (D-116).

        [ES]
        Qué hace: da la probabilidad de obra maestra por pieza con el rango del héroe en ese oficio: la 🪑 Carpintería
        con su beneficio (hasta 15 %), los demás oficios que hacen equipo con balance.yaml masterwork.base_chance
        (hasta 5 %); parejo con el rango (profession_rules.masterwork_chance).
        La llaman: _make (el sorteo), _recipe_view (la línea ✒️) y _professions_view (el beneficio de cada oficio).
        Si cambia, afecta: cuántas obras maestras salen.
        """
        cfg = self.content.balance.get("masterwork") or {}
        return masterwork_chance(self._prof_catalog().get(pid, {}), self._prof_rank(hero, pid), self._prof_cfg()["max_rank"],
                                 float(cfg.get("base_chance", 0.0)))

    def _make_xp(self, hero: Hero, recipe: dict[str, Any], rank: int) -> int:
        """Hero xp of making a recipe once (D-108): hero_xp_per_energy × energy, scaled like a zone of level
        min(hero level, profession rank) — a novice crafter learns little; a dedicated one keeps pace with the others."""
        return self._zone_xp(self._prof_cfg()["hero_xp_per_energy"] * int(recipe.get("energy", 1)), min(hero.level, rank))

    def _pay_energy(self, hero: Hero, cost: int) -> None:
        """Pay `cost` energy (the caller checked it is there); same rule as _spend_energy (D-78)."""
        if hero.energy >= self.content.balance["energy"]["max"]:
            hero.energy_at = self.clock.now()
        hero.energy -= cost

    def _rank_bar(self, hero: Hero, pid: str) -> str:
        """▓▓▓░░░░░ 37 % towards the next rank (full at the top rank)."""
        cfg = self._prof_cfg()
        rank = self._prof_rank(hero, pid)
        if rank >= cfg["max_rank"]:
            return self._bar(1, 1, 8) + " 100 %"
        low, high = xp_for_rank(cfg["rank_formula"], rank), xp_for_rank(cfg["rank_formula"], rank + 1)
        have = hero.professions.get(pid, 0) - low
        return f"{self._bar(have, max(1, high - low), 8)} {int(100 * have / max(1, high - low))} %"

    def _next_unlock(self, hero: Hero, pid: str) -> str | None:
        """🔓 What the next rank threshold of a profession opens: its rare find, or its next recipes."""
        t = self.texts
        if pid == self._explorer_cfg()["profession"]:      # D-112: the 🧭 Explorador opens map info, not recipes
            return self._explorer_next(hero)
        if pid == self._ench_cfg().get("profession"):      # D-115: ✨ Encantamiento opens enchantments, not recipes
            return self._ench_next(hero)
        rank = self._prof_rank(hero, pid)
        rare = self._prof_catalog()[pid].get("rare")
        if rare and rank < int(rare["min_rank"]):
            return t.t("prof.next", rank=rare["min_rank"], items=self._item_label(rare["item"]))
        later = [(int(rdef.get("min_rank", 1)), rid) for rid, rdef in self._recipes().items()
                 if rdef["profession"] == pid and int(rdef.get("min_rank", 1)) > rank and self._pspec_recipe_ok(hero, rdef)]   # D-141
        if not later:
            return None
        need = min(r for r, _ in later)
        return t.t("prof.next", rank=need, items=", ".join(self._recipe_name(rid) for r, rid in later if r == need))

    def _stations_line(self, where: str | None, stations: list[str]) -> str:
        t = self.texts
        if where == "claro":
            return t.t("prof.stations_claro")
        if where == "camp":
            return t.t("prof.stations_camp", items=", ".join(self._prof_name(sid) for sid in stations),
                       pct=round(100 * self._prof_cfg()["camp_bonus"]))
        return t.t("prof.stations_none")

    def _prof_action(self, hero: Hero, action_id: str) -> View:
        """Route the buttons of ⚒️ Oficios (D-109): "oficios", "est:<branch>:<page>", "rec:<recipe>:<page>",
        "mk:<recipe>:<times>:<page>". [ES] Qué hace: reparte los botones de los oficios. La llama: _idle_action.
        Si cambia, afecta: los IDs de botón de los oficios (los clientes solo los reenvían)."""
        parts = action_id.split(":")
        page = int(parts[-1]) if len(parts) > 2 and parts[-1].isdigit() else 0
        if parts[0] == "est" and len(parts) >= 2:
            return self._station_view(hero, parts[1], page)
        if parts[0] == "rec" and len(parts) >= 2:
            return self._recipe_view(hero, parts[1], page)
        if parts[0] == "mk" and len(parts) >= 3 and parts[2].isdigit():
            return self._make(hero, parts[1], int(parts[2]), int(parts[3]) if len(parts) > 3 and parts[3].isdigit() else 0)
        return self._professions_view(hero)

    def _perk_text(self, perk: dict[str, Any] | None, rank: int) -> str:
        """"+2 % de ataque con placas": a profession's benefit at a rank, in words (D-111). Empty without a perk."""
        if not perk:
            return ""
        t = self.texts
        share = min(rank, self.content.balance["professions"]["max_rank"]) / self.content.balance["professions"]["max_rank"]
        parts = []
        for key in profession_rules.PERK_KEYS:
            if key in perk:
                value = float(perk[key]) * share
                shown = round(value, 1) if key == "bag" else (int(value) if key == "explore" else round(value * 100, 1))  # masterwork: "+15 % de obra maestra"
                parts.append(t.t(f"prof.perk.{key}", v=f"{shown:g}"))
        limit = perk.get("armor_type") or perk.get("weapon_type")
        if limit:
            names = limit if isinstance(limit, list) else [limit]
            parts.append(t.t("prof.perk.only_armor" if "armor_type" in perk else "prof.perk.only_weapon", what="/".join(names)))
        return " · ".join(parts)

    def _professions_view(self, hero: Hero, notice: str | None = None) -> View:
        """⚒️ Oficios: your rank in every profession you started, how to raise it and what the next rank opens;
        the professions not started yet; the stations where you stand. Buttons: 🪚 Refinar, 🛠️ Fabricar, ↩️ Volver.

        [ES]
        Qué hace: muestra los oficios que empezaste, agrupados en recolección, refinado y fabricación, cada uno con su
        rango (y título), la barra hasta el próximo, cómo se sube y qué abre el próximo umbral; después, los que faltan
        empezar (sin tope de oficios, D-57) y dónde están las estaciones. Con estaciones aquí (el Claro o tu
        campamento con 🧵 Taller o 🔨 Herrería): 🪚 Refinar y 🛠️ Fabricar. El 🧭 Explorador
        (D-112, rama 🧭 Exploración) muestra además qué abre cada rango en el mapa (✅ lo abierto) y el próximo umbral.
        D-141: bajo cada oficio, sus 🎓 especializaciones con su dominio (o "puedes elegir") y, desde que un oficio llega al
        rango 25, el botón 🎓 Especialización. 4 botones como mucho (D-75).
        La llaman: el atajo /oficios, ⚒️ Oficios del Claro, del 🧵 Taller y de los servicios del campamento.
        Si cambia, afecta: dónde ve el jugador sus oficios (tests/test_professions.py).
        """
        t = self.texts
        catalog = self._prof_catalog()
        body = [t.t("prof.intro")]
        started = [pid for pid in catalog if hero.professions.get(pid, 0) > 0]
        branch = None
        for pid in started:
            pdef = catalog[pid]
            if pdef.get("branch") != branch:
                branch = pdef.get("branch")
                body += ["", t.t(f"prof.branch.{branch}")]
            rank = self._prof_rank(hero, pid)
            body.append(t.t("prof.line", name=self._prof_name(pid), rank=rank, title=self._rank_title(rank), bar=self._rank_bar(hero, pid)))
            body.append(t.t("prof.how_line", how=t.t(pdef.get("how_key", f"profession.{pid}.how"))))
            perk = self._perk_text(pdef.get("perk"), rank)
            if "masterwork" not in (pdef.get("perk") or {}) and self._makes_masterworks(pid):    # D-116: ✒️ the base chance
                shown = round(100 * self._masterwork_chance(hero, pid), 1)
                perk = " · ".join(part for part in (perk, t.t("prof.perk.masterwork", v=f"{shown:g}")) if part)
            if perk:
                body.append(t.t("prof.perk_line", perk=perk))           # D-111: what this profession gives you now
            body += self._pspec_prof_lines(hero, pid)                     # D-141: 🎓 your specializations here (or "you can choose")
            body += self._explorer_prof_lines(hero, pid)                 # D-112: what each 🧭 rank opens on the map
            unlock = self._next_unlock(hero, pid)
            if unlock:
                body.append(unlock)
        if not started:
            body += ["", t.t("prof.none")]
        rest = [self._prof_name(pid) for pid in catalog if pid not in started]
        if rest:
            body += ["", t.t("prof.not_started", items=", ".join(rest))]
        stations, where = self._stations_here(hero)
        body += ["", self._stations_line(where, stations) if (where or not hero.activity) else t.t("activity.busy"),
                 t.t("prof.energy", energy=hero.energy, max=self.content.balance["energy"]["max"])]
        actions = []
        if stations:
            actions = [Action(id="est:refine:0", label=t.t("prof.refine_button")), Action(id="est:craft:0", label=t.t("prof.craft_button"))]
        if self._pspec_any(hero):                                         # D-141: 🎓 Especialización, from rank 25 (4 buttons at most)
            actions.append(Action(id="pspecs", label=t.t("spec.button")))
        actions.append(Action(id=self._prof_back(hero), label=t.t("menu.back")))
        return View(kind="professions", title=t.t("prof.title"), body=body, actions=actions, notice=notice)

    def _station_view(self, hero: Hero, branch: str, page: int = 0, notice: str | None = None) -> View:
        """🪚 Refinar / 🛠️ Fabricar: the recipes of this branch you can do here with your rank, ✅ first (you carry it
        all), then those you carry part of (with what is missing), then the rest; 2 per page when there are more than 3.

        [ES]
        Qué hace: lista las recetas de refinado o de fabricación de las estaciones de aquí que tu rango ya abre:
        primero las que puedes hacer (✅), después aquellas de las que llevas algo (con lo que falta) y al final las
        demás; dentro de cada grupo, las de rango más alto primero (D-110: cada línea tiene equipo hasta el nivel 100 y la
        más nueva es la que sirve). Cada receta es un botón que abre su detalle; de a 2 por página cuando son más de 3 (➡️ Ver más), con
        ↩️ Volver a ⚒️ Oficios: 4 botones como mucho (D-75). Las recetas de rango más alto se ven en ⚒️ Oficios. D-141: las recetas
        exclusivas de una 🎓 especialización solo aparecen (con 🎓 delante) para quien la tiene con el dominio que piden.
        La llaman: 🪚 Refinar y 🛠️ Fabricar de ⚒️ Oficios, ➡️ Ver más y ↩️ Volver de cada receta.
        Si cambia, afecta: cómo encuentra el jugador qué hacer (tests/test_professions.py).
        """
        t = self.texts
        if branch not in ("refine", "craft"):
            return self._professions_view(hero)
        if hero.activity:
            return self._professions_view(hero, notice=t.t("activity.busy"))
        stations, where = self._stations_here(hero)
        if not stations:
            return self._professions_view(hero, notice=notice or t.t("prof.no_station"))
        catalog = self._prof_catalog()
        recipes = self._recipes()
        entries: list[tuple[int, str, dict[str, int]]] = []
        elsewhere = False
        for rid, rdef in recipes.items():
            pid = rdef["profession"]
            if catalog.get(pid, {}).get("branch") != branch or self._prof_rank(hero, pid) < int(rdef.get("min_rank", 1)):
                continue
            if not self._pspec_recipe_ok(hero, rdef):                     # D-141: 🎓 exclusive recipes, only for their specialization
                continue
            if pid not in stations:
                elsewhere = True
                continue
            missing = missing_for(rdef, hero.backpack)
            carried = any(hero.backpack.get(item, 0) > 0 for item in rdef["inputs"])
            entries.append((0 if not missing else 1 if carried else 2, rid, missing))
        # Stable: inside each group the highest rank first (D-110: up to 13 tiers per line, the newest is the useful one),
        # then file order.
        entries.sort(key=lambda entry: (entry[0], -int(recipes[entry[1]].get("min_rank", 1))))
        per = int(self._prof_cfg()["per_page"])
        pages = 1 if len(entries) <= 3 else (len(entries) + per - 1) // per
        page %= pages
        shown = entries if pages == 1 else entries[page * per: page * per + per]
        body = [t.t(f"prof.station_intro_{branch}"), self._stations_line(where, stations),
                t.t("prof.energy", energy=hero.energy, max=self.content.balance["energy"]["max"]), ""]
        actions = []
        for _, rid, missing in shown:
            rdef = recipes[rid]
            name = self._pspec_mark(rdef) + self._recipe_name(rid)         # D-141: "🎓 " before an exclusive recipe
            body.append(t.t("prof.entry_ok" if not missing else "prof.entry", item=name,
                            inputs=self._item_list(rdef["inputs"]), energy=rdef["energy"]))
            if missing:
                body.append(t.t("prof.entry_missing", items=self._item_list(missing)))
            actions.append(Action(id=f"rec:{rid}:{page}", label=t.t("prof.entry_button_ok" if not missing else "prof.entry_button",
                                                                     item=name)))
        if not entries:
            body.append(t.t("prof.station_empty"))
        if pages > 1:
            body.append(t.t("prof.page", n=page + 1, total=pages))
            actions.append(Action(id=f"est:{branch}:{page + 1}", label=t.t("prof.more")))
        if elsewhere:
            body.append(t.t("prof.more_in_claro"))
        body.append(t.t("prof.locked_hint"))
        actions.append(Action(id="oficios", label=t.t("menu.back")))
        return View(kind="station", title=t.t(f"prof.station_title_{branch}"), body=body, actions=actions[:4], notice=notice)

    def _recipe_view(self, hero: Hero, rid: str, page: int = 0, notice: str | None = None) -> View:
        """One recipe: what it needs (✅ / ❌ with have/need), what it makes, energy, what you earn, 🔨 Hacer 1 / 5 / todo.

        [ES]
        Qué hace: muestra una receta: los materiales que pide con lo que llevas (✅ o ❌), lo que sale (con los bonos si
        es equipo, o cuánto cura si es poción), la energía por vez, la experiencia de héroe y de oficio que da, y la
        probabilidad de una unidad más al refinar. D-141: la de una 🎓 especialización dice de cuál es y, si no la tienes o te
        falta dominio, lo dice y no hay botón de hacer; la ✒️ obra maestra y la unidad de más suman lo de tus especializaciones. Botones: 🔨 Hacer 1, 🔨 Hacer 5 (o lo que alcance), 🔨 Hacer todo
        (si alcanza para más de 5) y ↩️ Volver a la estación: 4 como mucho (D-75). Si falta algo, lo dice y no hay botón.
        La llaman: los botones de cada receta en 🪚 Refinar / 🛠️ Fabricar, y _make al terminar (o al rechazar).
        Si cambia, afecta: tests/test_professions.py.
        """
        t = self.texts
        rdef = self._recipes().get(rid)
        if not rdef:
            return self._professions_view(hero, notice=notice)
        pid = rdef["profession"]
        branch = self._prof_catalog().get(pid, {}).get("branch", "craft")
        rank = self._prof_rank(hero, pid)
        need_rank = int(rdef.get("min_rank", 1))
        stations, where = self._stations_here(hero)
        body = [self._pspec_mark(rdef) + self._recipe_name(rid),
                t.t("prof.recipe_prof", name=self._prof_name(pid), rank=rank, title=self._rank_title(rank), need=need_rank)]
        if rdef.get("spec"):                                    # D-141: 🎓 whose exclusive recipe it is
            body.append(t.t("spec.recipe_line", spec=self._pspec_name(rdef["spec"])))
        body += ["", t.t("prof.recipe_needs")]
        for item_id, n in rdef["inputs"].items():
            have = hero.backpack.get(item_id, 0)
            body.append(t.t("prof.have_line" if have >= n else "prof.lack_line", item=self._item_label(item_id), have=have, need=n))
        out_id = next(iter(rdef["output"]))
        item = self.content.items[out_id]
        body.append("")
        if item.get("kind") == "gear":
            body.append(t.t("prof.gear_out", slot=t.t(f"gear.slot.{item['slot']}"), type=t.t(f"gear.type.{item['type']}"),
                            level=item.get("req_level", 1), stats=self._gear_stats_text(item.get("stats", {}))))
            body.append(self._gear_status(hero, item))
            if masterwork_id(out_id) in self.content.items:     # D-116: ✒️ the chance that it comes out a masterwork (+ D-141 🎓)
                chance = self._masterwork_chance(hero, pid) + self._pspec_masterwork(hero, item)
                body.append(t.t("prof.masterwork_line", pct=f"{round(100 * chance, 1):g}"))
        elif item.get("kind") == "furniture":                   # D-116: 🪑 camp furniture
            body.append(t.t("prof.furniture_out", desc=t.t(item["desc_key"])))
        elif item.get("heal"):
            body.append(t.t("prof.heal_out", heal=round(item["heal"] * 100), tox=item.get("toxicity", 0)))
        elif t.has(f"resources.use.{out_id}"):
            body.append(t.t("prof.material_out", use=t.t(f"resources.use.{out_id}")))
        body.append(t.t("prof.energy_cost", energy=rdef["energy"], have=hero.energy))
        body.append(t.t("prof.gains", xp=int(self._make_xp(hero, rdef, rank) * self._xp_mult(hero)), name=self._prof_name(pid), prof_xp=rdef["xp"]))
        spec_yield = self._pspec_bonus(hero, "yield", item=out_id) if item.get("kind") != "gear" else 0.0     # D-141: 🎓
        if branch == "refine" and round(100 * (self._make_bonus(rank, where) + spec_yield)):
            body.append(t.t("prof.yield_line", pct=round(100 * (self._make_bonus(rank, where) + spec_yield))))
        elif branch != "refine" and round(100 * spec_yield):
            body.append(t.t("spec.yield_line", pct=round(100 * spec_yield)))
        actions = []
        if rank < need_rank:
            body.append(t.t("prof.locked", need=need_rank, name=self._prof_name(pid), rank=rank))
        elif not self._pspec_recipe_ok(hero, rdef):              # D-141: only its 🎓 specialization, with enough mastery
            body.append(self._pspec_recipe_lock(hero, rdef))
        elif pid not in stations:
            body.append(t.t("activity.busy") if hero.activity else t.t("prof.no_station"))
        else:
            times = max_times(rdef, hero.backpack, hero.energy)
            batch = int(self._prof_cfg()["make_batch"])
            if times >= 1:
                actions.append(Action(id=f"mk:{rid}:1:{page}", label=t.t("prof.make_button", n=1)))
            if times >= 2:
                actions.append(Action(id=f"mk:{rid}:{min(batch, times)}:{page}", label=t.t("prof.make_button", n=min(batch, times))))
            if times > batch:
                actions.append(Action(id=f"mk:{rid}:{times}:{page}", label=t.t("prof.make_all", n=times)))
            missing = missing_for(rdef, hero.backpack)
            if missing:
                body.append(t.t("prof.missing_line", items=self._item_list(missing)))
            elif not times:
                body.append(self._no_energy_notice(hero))
        actions.append(Action(id=f"est:{branch}:{page}" if stations else "oficios", label=t.t("menu.back")))
        return View(kind="recipe", title=t.t("prof.recipe_title"), body=body, actions=actions[:4], notice=notice)

    def _make(self, hero: Hero, rid: str, times: int, page: int = 0) -> View:
        """🔨 Hacer: refine or craft a recipe `times` times at a station; all or nothing.

        [ES]
        Qué hace: hace la receta tantas veces: comprueba la estación (Claro o tu campamento), que no estés ocupado, tu
        rango, los materiales y la energía de TODAS las veces; si algo falta, avisa y no gasta nada (regla 6). Si
        alcanza: gasta la energía y los materiales, guarda lo que sale (al refinar, a veces una unidad más por el rango y
        el campamento), da experiencia de héroe (D-108) y de oficio, pone el equipo nuevo si esa ranura estaba vacía y
        llena el cinturón con las pociones. D-116: cada pieza de equipo puede salir ✒️ obra maestra (sorteo propio, con
        la probabilidad de _masterwork_chance): va a la mochila como "<id>_obra" con la firma del héroe
        (Hero.gear_signatures) y, si la ranura estaba vacía, es la que se pone. Los 🪑 muebles avisan dónde colocarlos.
        D-141: una receta exclusiva de otra 🎓 especialización se rechaza sin gastar nada; tus especializaciones suman a la
        unidad de más (al refinar, y en los remedios con su propio sorteo), a la ✒️ obra maestra de su línea y a sus hallazgos
        por vez (🪙 Metales preciosos).
        Publica ItemCrafted con la pieza normal y el total hecho (y ProfessionRankUp si sube de rango).
        La llaman: los botones 🔨 Hacer de la receta.
        Si cambia, afecta: la economía de los oficios (balance.yaml professions; content/professions.yaml).
        """
        t = self.texts
        rdef = self._recipes().get(rid)
        if not rdef or times < 1:
            return self._professions_view(hero)
        pid = rdef["profession"]
        if hero.activity:
            return self._recipe_view(hero, rid, page, notice=t.t("activity.busy"))
        stations, where = self._stations_here(hero)
        if pid not in stations:
            return self._recipe_view(hero, rid, page, notice=t.t("prof.no_station"))
        rank = self._prof_rank(hero, pid)
        if rank < int(rdef.get("min_rank", 1)):
            return self._recipe_view(hero, rid, page, notice=t.t("prof.locked", need=rdef["min_rank"], name=self._prof_name(pid), rank=rank))
        if not self._pspec_recipe_ok(hero, rdef):                # D-141: 🎓 exclusive recipe of another specialization (nothing spent)
            return self._recipe_view(hero, rid, page, notice=self._pspec_recipe_lock(hero, rdef))
        missing = missing_for(rdef, hero.backpack, times)
        if missing:
            return self._recipe_view(hero, rid, page, notice=t.t("prof.missing", items=self._item_list(missing)))
        cost = int(rdef.get("energy", 1)) * times
        if hero.energy < cost:
            return self._recipe_view(hero, rid, page, notice=self._no_energy_notice(hero))
        self._pay_energy(hero, cost)
        bag_before = dict(hero.backpack)                    # D-115: to tell a ⬆️ better piece among what comes out
        for item_id, n in rdef["inputs"].items():
            hero.backpack[item_id] -= int(n) * times
            if hero.backpack[item_id] <= 0:
                del hero.backpack[item_id]
        out_id, out_n = next(iter(rdef["output"].items()))
        item = self.content.items[out_id]
        extra = 0
        if self._prof_catalog()[pid].get("branch") == "refine":       # specialists and camps get more out (D-101)
            rng = Rng(int(hash_unit(self.world_seed, hero.id, "make", rid, self.clock.now(), hero.professions.get(pid, 0)) * 2**31))
            chance = self._make_bonus(rank, where) + self._pspec_bonus(hero, "yield", item=out_id)     # D-141: 🎓 e.g. 🔩 Hierro
            extra = sum(1 for _ in range(times) if rng.chance(chance))
        elif item.get("kind") != "gear":                              # D-141: 🎓 more remedies (🧪 Pociones, 💊 Farmacia, own draw)
            bonus = self._pspec_bonus(hero, "yield", item=out_id)
            if bonus > 0:
                spec_rng = Rng(int(hash_unit(self.world_seed, hero.id, "make_spec", rid, self.clock.now(), hero.professions.get(pid, 0)) * 2**31))
                extra = sum(1 for _ in range(times) if spec_rng.chance(bonus))
        found: dict[str, int] = {}
        for find_id, chance in self._pspec_finds(hero, pid).items():   # D-141: 🪙 Metales preciosos, per time made (own draw)
            find_rng = Rng(int(hash_unit(self.world_seed, hero.id, "spec_find", rid, find_id, self.clock.now(), hero.professions.get(pid, 0)) * 2**31))
            n = sum(1 for _ in range(times) if find_rng.chance(chance))
            if n:
                self._bag_add(hero, find_id, n)                         # a find: never lost (D-90)
                found[find_id] = n
        made = int(out_n) * times + extra
        twin = masterwork_id(out_id)
        masters = 0
        if item.get("kind") == "gear" and twin in self.content.items:      # D-116: ✒️ own draw, never changes the rest
            mw_rng = Rng(int(hash_unit(self.world_seed, hero.id, "masterwork", rid, self.clock.now(), hero.professions.get(pid, 0)) * 2**31))
            chance = self._masterwork_chance(hero, pid) + self._pspec_masterwork(hero, item)      # D-141: + 🎓 in its line
            masters = sum(1 for _ in range(made) if mw_rng.chance(chance))
        if made > masters:
            hero.backpack[out_id] = hero.backpack.get(out_id, 0) + made - masters
        if masters:
            hero.backpack[twin] = hero.backpack.get(twin, 0) + masters
            hero.gear_signatures[twin] = hero.name                          # the crafter's signature
        lines = [t.t("prof.made", items=self._item_list({out_id: made}), energy=cost)]
        if extra:
            lines.append(t.t("prof.made_extra", n=extra))
        if found:
            lines.append(t.t("spec.found", items=self._item_list(found)))
        if masters:
            lines.append(t.t("prof.masterwork_made", n=masters, item=self._gear_name(twin), name=hero.name))
        if item.get("kind") == "gear":
            for new_id in ([out_id] if made > masters else []) + ([twin] if masters else []):
                if new_id not in hero.gear_new:
                    hero.gear_new.append(new_id)
            worn = auto_equip(hero, twin if masters else out_id, self.content.items, self.content.classes, self.content.balance)
            if worn:
                self._clamp_hp(hero)
            lines.append(t.t("prof.gear_worn" if worn else "prof.gear_made"))
        elif item.get("kind") == "furniture":                               # D-116: 🪑 where to place it
            lines.append(t.t("prof.furniture_made"))
        if item.get("belt"):
            self._refill_belt(hero)
        self.bus.publish(ItemCrafted(hero.id, rid, out_id, made))
        xp = self._make_xp(hero, rdef, rank) * times
        prof_xp = int(rdef.get("xp", 0)) * times
        lines.append(t.t("prof.gained", xp=int(xp * self._xp_mult(hero)), name=self._prof_name(pid), prof_xp=prof_xp))
        lines += self._give_xp(hero, xp)
        lines += self._prof_gain(hero, pid, prof_xp)
        lines += self._story_event(hero, "craft", recipe=rid, profession=pid, item=out_id, n=times)     # D-117
        better = self._better_piece(hero, bag_before) if item.get("kind") == "gear" else None
        if better:                                          # D-115: ⬆️ what you just made beats what you wear
            lines.append(self._better_line(hero, better))
        view = self._recipe_view(hero, rid, page, notice="\n".join(lines))
        if better:                                          # 🔁 Equipar first; 4 buttons at most (D-75): it takes 🔨 Hacer todo's place
            view.actions.insert(0, self._better_action(better))
            while len(view.actions) > 4:
                view.actions.pop(-2)
        return view

    # ------------------------------------------------------------------ ✨ enchanting and the ⬆️ better piece (D-115, phase 2)

    def _ench_cfg(self) -> dict[str, Any]:
        """balance.yaml "enchanting" ({} if missing: then nothing can be enchanted and the game works the same)."""
        return self.content.balance.get("enchanting") or {}

    def _ench_defs(self) -> dict[str, dict[str, Any]]:
        """The enchantments (balance.yaml enchanting.enchants): id -> stat, slots, min, max, min_rank, material."""
        return self._ench_cfg().get("enchants") or {}

    def _ench_pid(self) -> str:
        return self._ench_cfg().get("profession", "encantamiento")

    def _ench_rank(self, hero: Hero) -> int:
        return self._prof_rank(hero, self._ench_pid())

    def _ench_label(self, eid: str) -> str:
        """"⚔️ Filo", "❤️ Vigor", "🛡️ Guarda" (ench.name.<id>)."""
        return self.texts.t(f"ench.name.{eid}")

    def _enchant_slot(self, item: dict[str, Any] | None) -> str | None:
        """Id of the enchantment a gear piece takes by its slot (one per slot in the simple layer), or None."""
        if not item or item.get("kind") != "gear":
            return None
        return profession_rules.enchant_for_slot(item.get("slot", ""), self._ench_defs())

    def _enchant_text(self, hero: Hero, item_id: str) -> str:
        """"⚔️ Filo +2% ataque": the enchantment on a piece the hero holds (Hero.gear_enchants); "" if none."""
        record = (hero.gear_enchants or {}).get(item_id) or {}
        edef = self._ench_defs().get(record.get("id", ""))
        if not edef:
            return ""
        return f"{self._ench_label(record['id'])} {self._gear_stats_text({edef['stat']: float(record.get('value', 0.0))})}"

    def _enchant_mark(self, hero: Hero, item_id: str) -> str:
        """" ✨" after the name of an enchanted piece, "" otherwise."""
        return self.texts.t("ench.mark") if (hero.gear_enchants or {}).get(item_id) else ""

    def _is_better(self, hero: Hero, item_id: str) -> bool:
        """⬆️ A piece the hero is not wearing, usable now, of its type and with a higher score (engine/hero/gear.py is_better)."""
        return is_better(self.content.items, item_id, hero, self.content.classes, self.content.balance)

    def _better_mark(self, hero: Hero, item_id: str) -> str:
        """" ⬆️" after a piece that is better than what the hero wears in its slot, "" otherwise."""
        return self.texts.t("gear.better_mark") if self._is_better(hero, item_id) else ""

    def _better_piece(self, hero: Hero, before: dict[str, int]) -> str | None:
        """The best ⬆️ better gear piece among those that came into the backpack since `before`, or None.

        [ES]
        Qué hace: mira qué piezas de equipo entraron a la mochila (botín, cofre, fabricar, obra maestra) y devuelve la mejor de
        las que son "⬆️ mejores" que lo que llevas (engine/hero/gear.py is_better: tu nivel, tu tipo y más puntaje). Una pieza
        que se puso sola (ranura vacía) ya no está en la mochila: no cuenta.
        La llaman: _end_combat (y por ahí las peleas automáticas) y _make.
        Si cambia, afecta: cuándo sale el aviso "⬆️ Tienes una pieza mejor" con su botón 🔁 Equipar.
        """
        new = [i for i, n in hero.backpack.items() if n > before.get(i, 0) and self.content.items.get(i, {}).get("kind") == "gear"]
        better = [i for i in new if self._is_better(hero, i)]
        if not better:
            return None
        return max(better, key=lambda i: (piece_score(self.content.items, i, hero, self.content.classes, self.content.balance), i))

    def _better_line(self, hero: Hero, item_id: str) -> str:
        """"⬆️ ¡Tienes una pieza mejor! … supera a lo que llevas en ⛑️ Cabeza: +2% vida" (what it adds over the worn piece)."""
        diff, _ = self._gear_diff(hero, item_id)
        return self.texts.t("gear.better_notice", item=self._gear_name(item_id),
                            slot=self.texts.t(f"gear.slot.{self.content.items[item_id]['slot']}"), stats=self._gear_stats_text(diff))

    def _better_action(self, item_id: str) -> Action:
        """🔁 Equipar <piece>: one tap puts the better piece on (the same "equip:<id>" as the piece's ✅ Equipar)."""
        item = self.content.items[item_id]
        return Action(id=f"equip:{item_id}", label=self.texts.t("gear.better_button", item=f"{item['emoji']} {self.texts.t(item['name_key'])}"))

    def _forget_piece(self, hero: Hero, item_id: str) -> None:
        """When the last copy of a piece leaves the hero, its ✒️ signature (D-116), ✨ enchantment (D-115) and 🆕 mark go too."""
        if hero.backpack.get(item_id, 0) > 0 or item_id in hero.gear.values():
            return
        hero.gear_signatures.pop(item_id, None)
        hero.gear_enchants.pop(item_id, None)
        if item_id in hero.gear_new:
            hero.gear_new.remove(item_id)

    def _ench_unlocks(self, pid: str, before: int, after: int) -> list[str]:
        """"🔓 Nuevo encantamiento: 🛡️ Guarda." when a new ✨ Encantamiento rank opens one (for _prof_gain)."""
        if pid != self._ench_pid():
            return []
        opened = [self._ench_label(eid) for eid, edef in self._ench_defs().items() if before < int(edef.get("min_rank", 1)) <= after]
        return [self.texts.t("ench.unlocked", items=", ".join(opened))] if opened else []

    def _ench_next(self, hero: Hero) -> str | None:
        """🔓 The next ✨ Encantamiento rank that opens an enchantment (for ⚒️ Oficios), or None."""
        rank = self._ench_rank(hero)
        later = [(int(edef.get("min_rank", 1)), eid) for eid, edef in self._ench_defs().items() if int(edef.get("min_rank", 1)) > rank]
        if not later:
            return None
        need = min(r for r, _ in later)
        return self.texts.t("prof.next", rank=need, items=", ".join(self._ench_label(eid) for r, eid in later if r == need))

    def _ench_need_text(self, hero: Hero, cost: dict[str, int]) -> str:
        """"✅ ✨ Esencia arcana: 5/3 · ❌ 🔩 Lingote: 0/1" (what a ✨ action asks, with what you carry)."""
        t = self.texts
        return " · ".join(t.t("prof.have_line" if hero.backpack.get(i, 0) >= n else "prof.lack_line", item=self._item_label(i),
                              have=hero.backpack.get(i, 0), need=n) for i, n in cost.items())

    def _enchant_plan(self, hero: Hero, item_id: str) -> dict[str, Any]:
        """What enchanting this piece would do now: the enchantment, its value at your rank, its cost and what stops it.

        [ES]
        Qué hace: arma el plan de encantar una pieza: qué encantamiento le toca por su ranura, cuánto suma con tu rango, qué
        pide (engine/professions/rules.py enchant_cost) y qué lo impide ("no_slot", "rank", "not_better" si ya tiene ese o uno
        mejor, "missing", "energy" o "busy"). No cambia nada. D-141: el valor suma lo de tu 🎓 especialización ⚔️ Armas
        (Filo) o 🛡️ Armaduras (Vigor y Guarda), por su dominio.
        La llaman: _enchant_view (lo que muestra) y _enchant (lo que hace): siempre dicen lo mismo.
        Si cambia, afecta: cuándo se puede encantar.
        """
        eid = self._enchant_slot(self.content.items.get(item_id))
        if not eid:
            return {"problem": "no_slot"}
        cfg = self._ench_cfg()
        enc = cfg.get("enchant") or {}
        edef = self._ench_defs()[eid]
        rank = self._ench_rank(hero)
        value = profession_rules.enchant_value(edef, rank, self._prof_cfg()["max_rank"],
                                               self._pspec_bonus(hero, "enchant", enchant=eid))     # D-141: 🎓 Armas / Armaduras
        cost = profession_rules.enchant_cost(self.content.items[item_id], edef, enc, cfg.get("essence", "esencia"),
                                             cfg.get("major_essence", "esencia_mayor"))
        energy = int(enc.get("energy", 2))
        missing = {i: n - hero.backpack.get(i, 0) for i, n in cost.items() if hero.backpack.get(i, 0) < n}
        current = (hero.gear_enchants or {}).get(item_id) or {}
        problem = None
        if rank < int(edef.get("min_rank", 1)):
            problem = "rank"
        elif current.get("id") == eid and float(current.get("value", 0.0)) >= value - 1e-9:
            problem = "not_better"
        elif missing:
            problem = "missing"
        elif hero.energy < energy:
            problem = "energy"
        elif hero.activity:
            problem = "busy"
        return {"eid": eid, "edef": edef, "rank": rank, "value": value, "cost": cost, "energy": energy, "missing": missing,
                "problem": problem, "current": current}

    def _disenchant_gives(self, item: dict[str, Any]) -> dict[str, int]:
        """Essences a piece gives when disenchanted, before the perk (engine/professions/rules.py disenchant_yield)."""
        cfg = self._ench_cfg()
        return profession_rules.disenchant_yield(item, cfg.get("disenchant") or {}, cfg.get("essence", "esencia"),
                                                 cfg.get("major_essence", "esencia_mayor"))

    def _enchant_action(self, hero: Hero, action_id: str) -> View:
        """Route the ✨ buttons (D-115): "ench" (hub, /encantar), "ench:<piece>", "enc:<piece>", "dis:<piece>", "dis!:<piece>".
        [ES] Qué hace: reparte los botones del ✨ Encantamiento. La llama: _idle_action. Si cambia, afecta: los IDs de botón."""
        if action_id.startswith("ench:"):
            return self._enchant_view(hero, action_id[5:])
        if action_id.startswith("enc:"):
            return self._enchant(hero, action_id[4:])
        if action_id.startswith("dis!:"):
            return self._disenchant(hero, action_id[5:], confirmed=True)
        if action_id.startswith("dis:"):
            return self._disenchant(hero, action_id[4:])
        return self._ench_view(hero)

    def _ench_view(self, hero: Hero, notice: str | None = None) -> View:
        """✨ Encantamiento (/encantar): your rank and perk, your essences, the three enchantments, the costs and how to start.

        [ES]
        Qué hace: explica el ✨ Encantamiento en una pantalla: tu rango (con su barra) y su beneficio, las esencias que llevas,
        qué encantamiento lleva cada ranura y cuánto suma con tu rango (🔒 si todavía no llegas), qué pide encantar y qué da
        desencantar, y lo que llevas encantado. Botones: 🛡️ Elegir pieza (🔁 Equipar) y ↩️ Volver a ⚒️ Oficios. No tiene
        botón en ⚒️ Oficios (sus 4 lugares quedan para las estaciones): se llega con /encantar o desde una pieza.
        La llaman: el atajo /encantar.
        Si cambia, afecta: cómo entiende el jugador el oficio (tests/test_oficios_equipo.py).
        """
        t = self.texts
        cfg = self._ench_cfg()
        pid = self._ench_pid()
        rank = self._ench_rank(hero)
        body = [t.t("ench.intro"), "", t.t("ench.rank_line", rank=rank, title=self._rank_title(rank), bar=self._rank_bar(hero, pid))]
        perk = self._perk_text(self._prof_catalog().get(pid, {}).get("perk"), rank)
        if perk:
            body.append(t.t("prof.perk_line", perk=perk))
        essences = {i: hero.backpack[i] for i in (cfg.get("essence"), cfg.get("major_essence")) if i and hero.backpack.get(i)}
        body.append(t.t("ench.essences_line", items=self._item_list(essences)) if essences else t.t("ench.essences_none"))
        body += ["", t.t("ench.table_title")]
        for eid, edef in self._ench_defs().items():
            value = profession_rules.enchant_value(edef, rank, self._prof_cfg()["max_rank"],
                                                   self._pspec_bonus(hero, "enchant", enchant=eid))     # D-141: 🎓
            lock = "" if rank >= int(edef.get("min_rank", 1)) else t.t("ench.lock", rank=edef.get("min_rank", 1))
            body.append(t.t("ench.table_line", name=self._ench_label(eid), slots=", ".join(t.t(f"gear.slot.{s}") for s in edef.get("slots", [])),
                            stats=self._gear_stats_text({edef["stat"]: value}), material=self._item_label(edef["material"]), lock=lock))
        enc, dis = cfg.get("enchant") or {}, cfg.get("disenchant") or {}
        by_rarity = dis.get("by_rarity") or {}
        body += ["", t.t("ench.cost_rule", base=enc.get("essences", 3), per=enc.get("essences_per_levels", 10),
                         major=enc.get("major_from_level", 50), mat_per=enc.get("material_per_levels", 50), energy=enc.get("energy", 2)),
                 t.t("ench.disenchant_rule", comun=by_rarity.get("comun", 1), poco_comun=by_rarity.get("poco_comun", 2),
                     raro=by_rarity.get("raro", 3), epico=by_rarity.get("epico", 4), per=dis.get("per_levels", 20), energy=dis.get("energy", 1))]
        worn = [f"{self._gear_name(i)} ({self._enchant_text(hero, i)})" for i in hero.gear.values() if self._enchant_text(hero, i)]
        body += ["", t.t("ench.worn_title", items=" · ".join(worn)) if worn else t.t("ench.worn_none"), t.t("ench.how"),
                 t.t("prof.energy", energy=hero.energy, max=self.content.balance["energy"]["max"])]
        actions = [Action(id="gear:0", label=t.t("ench.pick_button")), Action(id="oficios", label=t.t("menu.back"))]
        return View(kind="enchanting", title=t.t("ench.title"), body=body, actions=actions, notice=notice)

    def _enchant_view(self, hero: Hero, item_id: str, notice: str | None = None) -> View:
        """✨ One piece: its enchantment now, the one you can give it (value, cost, what is missing) and what disenchanting gives.

        [ES]
        Qué hace: la pantalla ✨ de una pieza (desde ✨ Encantamiento en la pieza): el encantamiento que tiene, el que le toca
        por su ranura con tu rango (o 🔒 el rango que pide, o que ya tiene el mejor que puedes hacer), qué pide (✅/❌ con lo
        que llevas) y la energía; si está en la mochila, cuánto da desencantarla (con tu beneficio); puesta, que hay que
        quitársela primero. Botones: ✨ Encantar (si se puede), 💨 Desencantar (solo de la mochila) y ↩️ Volver a la pieza: 3.
        La llaman: el botón ✨ Encantamiento de _item_view, y _enchant / _disenchant al terminar.
        Si cambia, afecta: tests/test_oficios_equipo.py.
        """
        t = self.texts
        item = self.content.items.get(item_id)
        worn = item_id in hero.gear.values()
        if not item or item.get("kind") != "gear" or (not worn and hero.backpack.get(item_id, 0) <= 0):
            return self._gear_view(hero, notice=notice)
        rank = self._ench_rank(hero)
        body = [self._gear_name(item_id), t.t("ench.rank_line", rank=rank, title=self._rank_title(rank), bar=self._rank_bar(hero, self._ench_pid()))]
        note = self._masterwork_note(hero, item_id)
        if note:
            body.append(note)
        current = self._enchant_text(hero, item_id)
        body += ["", t.t("ench.current", enchant=current) if current else t.t("ench.current_none")]
        actions = []
        plan = self._enchant_plan(hero, item_id)
        problem = plan["problem"]
        if problem == "no_slot":
            body.append(t.t("ench.no_slot"))
        else:
            name, stats = self._ench_label(plan["eid"]), self._gear_stats_text({plan["edef"]["stat"]: plan["value"]})
            if problem == "rank":
                body.append(t.t("ench.locked", name=name, need=plan["edef"].get("min_rank", 1), rank=rank))
            elif problem == "not_better":
                body.append(t.t("ench.offer_best"))
            else:
                body.append(t.t("ench.offer_replace" if current else "ench.offer", name=name, stats=stats))
                body.append(t.t("ench.needs", items=self._ench_need_text(hero, plan["cost"]), energy=plan["energy"]))
                if problem == "missing":
                    body.append(t.t("prof.missing_line", items=self._item_list(plan["missing"])))
                elif problem == "energy":
                    body.append(self._no_energy_notice(hero))
                elif problem == "busy":
                    body.append(t.t("activity.busy"))
                else:
                    actions.append(Action(id=f"enc:{item_id}", label=t.t("ench.enchant_button", stats=stats)))
        body.append("")
        if worn and hero.backpack.get(item_id, 0) <= 0:
            body.append(t.t("ench.worn_cant"))
        else:
            energy = int((self._ench_cfg().get("disenchant") or {}).get("energy", 1))
            pct = round(100 * self._perks(hero)["disenchant"])
            body.append(t.t("ench.disenchant_line", items=self._item_list(self._disenchant_gives(item)),
                            bonus=t.t("ench.disenchant_bonus", pct=pct) if pct else "", energy=energy))
            if not hero.activity and hero.energy >= energy:
                actions.append(Action(id=f"dis:{item_id}", label=t.t("ench.disenchant_button")))
        body.append(t.t("prof.energy", energy=hero.energy, max=self.content.balance["energy"]["max"]))
        actions.append(Action(id=f"item:{item_id}", label=t.t("menu.back")))
        return View(kind="enchant", title=t.t("ench.piece_title"), body=body, actions=actions, notice=notice)

    def _enchant(self, hero: Hero, item_id: str) -> View:
        """✨ Encantar: spend the essences, the material and the energy and put the enchantment on the piece; all or nothing.

        [ES]
        Qué hace: encanta la pieza (puesta o en la mochila) si el plan no tiene problemas: gasta las esencias, el material y la
        energía, guarda el encantamiento en Hero.gear_enchants (reemplaza al anterior: uno por pieza) con el valor de tu rango,
        y da experiencia de héroe (D-108, como fabricar) y de ✨ Encantamiento. Si algo falta, avisa y no gasta nada (regla 6).
        La llama: el botón ✨ Encantar.
        Si cambia, afecta: las estadísticas en combate (gear_bonus) y cuánto se gasta al encantar.
        """
        t = self.texts
        item = self.content.items.get(item_id)
        if not item or item.get("kind") != "gear" or (item_id not in hero.gear.values() and hero.backpack.get(item_id, 0) <= 0):
            return self._gear_view(hero)
        plan = self._enchant_plan(hero, item_id)
        problem = plan["problem"]
        if problem:
            notices = {"no_slot": t.t("ench.no_slot"), "not_better": t.t("ench.not_better"), "busy": t.t("activity.busy"),
                       "missing": t.t("prof.missing", items=self._item_list(plan.get("missing") or {})),
                       "energy": self._no_energy_notice(hero)}
            if problem == "rank":
                notices["rank"] = t.t("ench.locked", name=self._ench_label(plan["eid"]), need=plan["edef"].get("min_rank", 1), rank=plan["rank"])
            return self._enchant_view(hero, item_id, notice=notices[problem])
        pid = self._ench_pid()
        self._pay_energy(hero, plan["energy"])
        for material, n in plan["cost"].items():
            hero.backpack[material] -= n
            if hero.backpack[material] <= 0:
                del hero.backpack[material]
        hero.gear_enchants[item_id] = {"id": plan["eid"], "value": plan["value"]}
        lines = [t.t("ench.enchanted", item=self._gear_name(item_id), enchant=self._enchant_text(hero, item_id), energy=plan["energy"])]
        xp = self._make_xp(hero, {"energy": plan["energy"]}, plan["rank"])
        prof_xp = int((self._ench_cfg().get("enchant") or {}).get("xp", 12))
        lines.append(t.t("prof.gained", xp=int(xp * self._xp_mult(hero)), name=self._prof_name(pid), prof_xp=prof_xp))
        lines += self._give_xp(hero, xp)
        lines += self._prof_gain(hero, pid, prof_xp)
        return self._enchant_view(hero, item_id, notice="\n".join(lines))

    def _disenchant(self, hero: Hero, item_id: str, confirmed: bool = False) -> View:
        """💨 Desencantar: destroy one copy of a piece from the backpack for essences (a ✒️ masterwork asks first).

        [ES]
        Qué hace: destruye una pieza de la mochila (nunca una puesta) y da sus ✨ esencias (disenchant_yield) con el beneficio
        del oficio (hasta +30 % al rango 100, sorteo propio por pieza: disenchant_amount). Una ✒️ obra maestra pide
        confirmación antes. Gasta energía, da experiencia de héroe y de ✨ Encantamiento, y con la última copia se van su firma,
        su encantamiento y su 🆕 (_forget_piece). Las esencias valen en el mercader menos que la pieza: desencantar nunca
        fabrica monedas (tests/test_oficios_equipo.py). Si falta energía o estás ocupado, no hace nada.
        La llaman: los botones 💨 Desencantar y 💨 Sí, desencantar.
        Si cambia, afecta: cuánto equipo sale del juego y cuántas esencias entran.
        """
        t = self.texts
        item = self.content.items.get(item_id)
        if not item or item.get("kind") != "gear":
            return self._gear_view(hero)
        if hero.backpack.get(item_id, 0) <= 0:
            if item_id in hero.gear.values():
                return self._enchant_view(hero, item_id, notice=t.t("ench.worn_no"))
            return self._gear_view(hero)
        if item.get("masterwork") and not confirmed:           # D-116: a ✒️ masterwork is not lost by one tap
            who = (hero.gear_signatures or {}).get(item_id)
            body = [self._gear_name(item_id), t.t("ench.confirm", by=t.t("ench.confirm_by", name=who) if who else "")]
            actions = [Action(id=f"dis!:{item_id}", label=t.t("ench.confirm_button")), Action(id=f"ench:{item_id}", label=t.t("ench.cancel_button"))]
            return View(kind="disenchant_confirm", title=t.t("ench.confirm_title"), body=body, actions=actions)
        if hero.activity:
            return self._enchant_view(hero, item_id, notice=t.t("activity.busy"))
        cfg = self._ench_cfg().get("disenchant") or {}
        energy = int(cfg.get("energy", 1))
        if hero.energy < energy:
            return self._enchant_view(hero, item_id, notice=self._no_energy_notice(hero))
        pid = self._ench_pid()
        rank = self._ench_rank(hero)
        self._pay_energy(hero, energy)
        hero.backpack[item_id] -= 1
        if hero.backpack[item_id] <= 0:
            del hero.backpack[item_id]
        perk = self._perks(hero)["disenchant"]
        rng = Rng(int(hash_unit(self.world_seed, hero.id, "disenchant", item_id, self.clock.now(), hero.professions.get(pid, 0)) * 2**31))
        got = {i: profession_rules.disenchant_amount(n, perk, rng.random()) for i, n in self._disenchant_gives(item).items()}
        for essence, n in got.items():
            self._bag_add(hero, essence, n)                   # what you get is never lost (D-90)
        self._forget_piece(hero, item_id)
        lines = [t.t("ench.disenchanted", item=self._gear_name(item_id), items=self._item_list(got), energy=energy)]
        xp = self._make_xp(hero, {"energy": energy}, rank)
        prof_xp = int(cfg.get("xp", 6))
        lines.append(t.t("prof.gained", xp=int(xp * self._xp_mult(hero)), name=self._prof_name(pid), prof_xp=prof_xp))
        lines += self._give_xp(hero, xp)
        lines += self._prof_gain(hero, pid, prof_xp)
        if hero.backpack.get(item_id, 0) > 0 or item_id in hero.gear.values():
            return self._enchant_view(hero, item_id, notice="\n".join(lines))
        return self._gear_view(hero, notice="\n".join(lines))

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

    # ------------------------------------------------------------------ 🎓 profession specializations (D-115, D-141)
    # [ES] Especializaciones de oficio (red-de-oficios.md §3): 3 por oficio (content/professions.yaml "specs"); una al rango 25,
    # otra al 75, nunca las tres. Cada una suma un efecto chico en su línea que crece con su dominio (la experiencia de ese oficio
    # ganada mientras la tienes) y algunas tienen recetas exclusivas. Cambiar una por otra cuesta monedas (balance.yaml specs) y
    # empieza de cero en la nueva; el dominio de la vieja queda guardado (Hero.spec_xp). Pantallas: ⚒️ Oficios → 🎓 Especialización
    # (o /especialidad) → un oficio → una especialización → 🎓 Elegir o 🔄 Dejar otra (pide confirmación).

    def _pspec_cfg(self) -> dict[str, Any]:
        """balance.yaml "specs" ({} if missing: nobody can specialize and the game works the same)."""
        return self.content.balance.get("specs") or {}

    def _pspec_catalog(self) -> dict[str, list[dict[str, Any]]]:
        """content/professions.yaml "specs": profession id -> its specializations (in file order)."""
        return (self.content.professions or {}).get("specs") or {}

    def _pspec_slots_at(self) -> list[int]:
        """The profession ranks that open the first and the second specialization (balance.yaml specs.slots_at: 25, 75)."""
        return [int(rank) for rank in self._pspec_cfg().get("slots_at") or []]

    def _pspec_mastery_xp(self) -> int:
        return int(self._pspec_cfg().get("mastery_xp", 1))

    def _pspec_held(self, hero: Hero, pid: str) -> list[str]:
        """The specializations the hero holds in a profession, in the order chosen (unknown or retired ones ignored)."""
        return profession_rules.spec_held(self._pspec_catalog(), hero.prof_specs or {}, pid)

    def _pspec_share(self, hero: Hero, sid: str) -> float:
        """Mastery 0..1 of a specialization (held now or saved from before)."""
        return profession_rules.spec_share((hero.spec_xp or {}).get(sid, 0), self._pspec_mastery_xp())

    def _pspec_bonus(self, hero: Hero, kind: str, key: str | None = None, **ctx: Any) -> float:
        """What the hero's specializations add to one kind of effect here (engine/professions/rules.py spec_bonus).

        [ES]
        Qué hace: suma un tipo de efecto (yield, masterwork, perk, coins, enchant, detect) de las 🎓 especializaciones que el héroe
        tiene, por su dominio y solo si coincide con lo que pasa (ctx: item, slot, type, sale, enchant, role). Sin especializaciones,
        0 (los héroes de antes juegan igual).
        La llaman: _perks, _merchant_sale, _trade_gather, _trade_loot, _make, _recipe_view, _pspec_masterwork, _enchant_plan,
        _ench_view, _infiltrate y _ecamp_destroyed.
        Si cambia, afecta: todo lo que dan las especializaciones (content/professions.yaml "specs").
        """
        if not hero.prof_specs:
            return 0.0
        return profession_rules.spec_bonus(self._pspec_catalog(), hero.prof_specs, hero.spec_xp or {}, self._pspec_mastery_xp(),
                                           kind, key, **ctx)

    def _pspec_finds(self, hero: Hero, pid: str) -> dict[str, float]:
        """item -> chance of the "find" effects of the hero's specializations in this profession (items that exist only)."""
        if not hero.prof_specs:
            return {}
        finds = profession_rules.spec_finds(self._pspec_catalog(), hero.prof_specs, hero.spec_xp or {}, self._pspec_mastery_xp(), pid)
        return {item: chance for item, chance in finds.items() if item in self.content.items}

    def _pspec_masterwork(self, hero: Hero, item: dict[str, Any]) -> float:
        """✒️ masterwork chance the hero's specializations add to a gear piece of this slot and type (D-141)."""
        return self._pspec_bonus(hero, "masterwork", slot=item.get("slot"), type=item.get("type"))

    def _pspec_name(self, sid: str) -> str:
        """"⚙️ Metales": a specialization's emoji and name (spec.<id>.name)."""
        _, sdef = profession_rules.spec_owner(self._pspec_catalog(), sid)
        return f"{(sdef or {}).get('emoji', '')} {self.texts.t(f'spec.{sid}.name')}".strip()

    def _pspec_mark(self, rdef: dict[str, Any]) -> str:
        """"🎓 " before the name of an exclusive recipe, "" otherwise."""
        return self.texts.t("spec.mark") if rdef.get("spec") else ""

    def _pspec_bar(self, hero: Hero, sid: str) -> str:
        """▓▓░░░░░░ 25 % of mastery."""
        pct = int(100 * self._pspec_share(hero, sid) + 1e-9)
        return f"{self._bar(pct, 100, 8)} {pct} %"

    def _pspec_cost(self, hero: Hero, pid: str) -> int:
        """Coins to switch a specialization of this profession now (P-105: they grow with the rank)."""
        return profession_rules.switch_cost(self._prof_rank(hero, pid), self._pspec_cfg().get("switch_cost") or {})

    def _pspec_choice(self, hero: Hero, pid: str, sid: str) -> str:
        """"held", "locked", "pick" (free) or "switch" (paid) for this specialization now (rules.spec_choice)."""
        return profession_rules.spec_choice(self._pspec_catalog(), hero.prof_specs or {}, pid, sid, self._prof_rank(hero, pid),
                                            self._pspec_slots_at())

    def _pspec_exclusives(self, sid: str) -> list[str]:
        """The recipe ids only this specialization makes (recipes with spec: <id>), in file order."""
        return [rid for rid, rdef in self._recipes().items() if rdef.get("spec") == sid]

    def _pspec_recipe_ok(self, hero: Hero, rdef: dict[str, Any]) -> bool:
        """True if the recipe is not exclusive, or the hero holds its specialization with recipe_mastery of mastery (D-141).

        [ES]
        Qué hace: dice si el héroe puede ver y hacer una receta por su especialización: las normales siempre; las exclusivas
        (spec: <id>) solo si tiene esa 🎓 especialización con balance.yaml specs.recipe_mastery de dominio (25 %). El rango lo
        miran aparte quienes llaman.
        La llaman: _prof_gain, _next_unlock, _station_view, _recipe_view, _make y _spec_view.
        Si cambia, afecta: quién hace las piezas exclusivas.
        """
        sid = rdef.get("spec")
        if not sid:
            return True
        pid, sdef = profession_rules.spec_owner(self._pspec_catalog(), sid)
        if not sdef or sid not in self._pspec_held(hero, pid):
            return False
        return self._pspec_share(hero, sid) >= float(self._pspec_cfg().get("recipe_mastery", 0.0)) - 1e-9

    def _pspec_recipe_lock(self, hero: Hero, rdef: dict[str, Any]) -> str:
        """Why an exclusive recipe is closed: you do not hold its specialization, or not enough mastery yet."""
        t = self.texts
        sid = rdef.get("spec", "")
        pid, _ = profession_rules.spec_owner(self._pspec_catalog(), sid)
        need = int(100 * float(self._pspec_cfg().get("recipe_mastery", 0.0)) + 1e-9)
        if pid and sid in self._pspec_held(hero, pid):
            return t.t("spec.recipe_locked", spec=self._pspec_name(sid), pct=need, have=int(100 * self._pspec_share(hero, sid) + 1e-9))
        return t.t("spec.recipe_not_held", spec=self._pspec_name(sid), prof=self._prof_name(pid or rdef.get("profession", "")))

    def _pspec_value_text(self, kind: str, key: str | None, value: float) -> str:
        """A value as the texts show it: percent points for most, whole points for 🧭 exploration, units for 🎒 space."""
        if kind == "perk" and key == "explore":
            return f"{int(value + 1e-9)}"
        if kind == "perk" and key == "bag":
            return f"{round(value, 1):g}"
        return f"{round(value * 100, 1):g}"

    def _pspec_effect_text(self, sdef: dict[str, Any], share: float) -> str:
        """"+5 % de sacar una unidad más de ⚙️ Pieza de metal": a specialization's effects at a mastery (1.0 = all of it).

        [ES]
        Qué hace: escribe los efectos de una especialización con su valor a ese dominio (0 a 1), con los textos spec.effect.<tipo>
        (o prof.perk.<clave> para los beneficios). La llaman: _pspec_prof_view, _spec_view y _pspec_prof_lines.
        Si cambia, afecta: solo cómo se ven los efectos.
        """
        t = self.texts
        parts = []
        for effect in sdef.get("effects") or []:
            kind, key = effect.get("kind"), effect.get("key")
            v = self._pspec_value_text(kind, key, float(effect.get("value", 0.0)) * share)
            if kind == "perk":
                parts.append(t.t(f"prof.perk.{key}", v=v))
            elif kind in ("yield", "find"):
                what = ", ".join(self._item_label(i) for i in effect.get("items") or [] if i in self.content.items)
                parts.append(t.t(f"spec.effect.{kind}", v=v, what=what))
            elif kind == "masterwork":
                what = "/".join(t.t(f"gear.type.{typ}") for typ in effect.get("types") or [])
                if effect.get("slots"):
                    what = t.t("spec.slots_of", types=what, slots=", ".join(t.t(f"gear.slot.{slot}") for slot in effect["slots"]))
                parts.append(t.t("spec.effect.masterwork", v=v, what=what))
            elif kind == "coins":
                parts.append(t.t("spec.effect.coins", v=v, what=" · ".join(t.t(f"spec.sale.{sale}") for sale in effect.get("sales") or [])))
            elif kind == "enchant":
                parts.append(t.t("spec.effect.enchant", v=v, what=t.t("spec.and").join(self._ench_label(e) for e in effect.get("enchants") or [])))
            elif kind == "detect":
                parts.append(t.t("spec.effect.detect", v=v))
        return " · ".join(parts)

    def _pspec_any(self, hero: Hero) -> bool:
        """True if some profession with specializations reached the first threshold, or the hero holds one (🎓 button)."""
        slots_at = self._pspec_slots_at()
        if not slots_at:
            return False
        specs = self._pspec_catalog()
        if any((hero.prof_specs or {}).values()):
            return True
        return any(specs.get(pid) and self._prof_rank(hero, pid) >= slots_at[0] for pid, xp in (hero.professions or {}).items() if xp > 0)

    def _pspec_prof_lines(self, hero: Hero, pid: str) -> list[str]:
        """⚒️ Oficios, under a profession: "🎓 ⚙️ Metales (25 %)" for each one held, or "🎓 puedes elegir" with a free slot."""
        slots_at = self._pspec_slots_at()
        if not slots_at or not profession_rules.spec_list(self._pspec_catalog(), pid):
            return []
        t = self.texts
        held = self._pspec_held(hero, pid)
        lines = []
        if held:
            lines.append(t.t("spec.prof_line", items=", ".join(
                t.t("spec.prof_line_item", name=self._pspec_name(sid), pct=int(100 * self._pspec_share(hero, sid) + 1e-9)) for sid in held)))
        if len(held) < profession_rules.spec_slots(self._prof_rank(hero, pid), slots_at):
            lines.append(t.t("spec.prof_free"))
        return lines

    def _pspec_gain(self, hero: Hero, pid: str, xp: int, before: int, after: int) -> list[str]:
        """Profession xp also raises the mastery of the specializations held there; lines for what it opens (D-141).

        [ES]
        Qué hace: la experiencia que gana un oficio sube también el dominio de cada 🎓 especialización que el héroe tiene en él
        (Hero.spec_xp). Avisa cuando una abre su receta exclusiva (25 % de dominio, si el rango ya alcanza), cuando queda
        dominada (100 %) y cuando el oficio llega al rango 25 ("ya puedes elegir") o al 75 ("puedes sumar una segunda").
        La llama: _prof_gain (siempre, suba o no de rango).
        Si cambia, afecta: el ritmo de las especializaciones y sus avisos.
        """
        slots_at = self._pspec_slots_at()
        if not slots_at or not profession_rules.spec_list(self._pspec_catalog(), pid):
            return []
        t = self.texts
        lines: list[str] = []
        need = float(self._pspec_cfg().get("recipe_mastery", 0.0))
        full = self._pspec_mastery_xp()
        for sid in self._pspec_held(hero, pid):
            old = int((hero.spec_xp or {}).get(sid, 0))
            hero.spec_xp[sid] = old + max(0, int(xp))
            old_share = profession_rules.spec_share(old, full)
            new_share = profession_rules.spec_share(old + max(0, int(xp)), full)
            if old_share + 1e-9 < need <= new_share + 1e-9:
                opened = [self._recipe_name(rid) for rid in self._pspec_exclusives(sid)
                          if int(self._recipes()[rid].get("min_rank", 1)) <= before]   # the ones a rank-up opens are told there
                if opened:
                    lines.append(t.t("spec.recipe_unlocked", spec=self._pspec_name(sid), items=", ".join(opened)))
            if old_share < 1.0 <= new_share:
                lines.append(t.t("spec.mastered", spec=self._pspec_name(sid)))
        for index, rank in enumerate(slots_at[:2]):
            if before < rank <= after:
                lines.append(t.t("spec.unlock_first" if index == 0 else "spec.unlock_second", prof=self._prof_name(pid)))
        return lines

    def _pspec_action(self, hero: Hero, action_id: str) -> View:
        """Route the 🎓 buttons (D-141): "pspecs[:page]", "pspec:<profession>", "pspv:<spec>", "pspp:<spec>",
        "pspx:<spec>:<old>" (asks) and "pspx!:<spec>:<old>" (switches). [ES] Qué hace: reparte los botones de las
        especializaciones. La llama: _idle_action. Si cambia, afecta: los IDs de botón (los clientes solo los reenvían)."""
        if action_id.startswith("pspec:"):
            return self._pspec_prof_view(hero, action_id[6:])
        if action_id.startswith("pspv:"):
            return self._pspec_view(hero, action_id[5:])
        if action_id.startswith("pspp:"):
            return self._pspec_pick(hero, action_id[5:])
        if action_id.startswith("pspx!:"):
            sid, _, old = action_id[6:].partition(":")
            return self._pspec_switch(hero, sid, old)
        if action_id.startswith("pspx:"):
            sid, _, old = action_id[5:].partition(":")
            return self._pspec_switch_view(hero, sid, old)
        page = action_id.partition(":")[2]
        return self._pspecs_view(hero, int(page) if page.isdigit() else 0)

    def _pspecs_view(self, hero: Hero, page: int = 0, notice: str | None = None) -> View:
        """🎓 Especialización: how it works and every profession that can specialize, with what you hold; one button each.

        [ES]
        Qué hace: explica las especializaciones (una al rango 25, otra al 75, nunca las tres; el dominio; cambiar cuesta y
        empieza de cero) y lista los oficios que ya llegaron al 25, con las que tienes o "puedes elegir"; después, los oficios
        empezados que todavía no llegan. Un botón por oficio (de a 2 por página si son más de 3, ➡️ Ver más) y ↩️ Volver a
        ⚒️ Oficios: 4 como mucho (D-75).
        La llaman: 🎓 Especialización de ⚒️ Oficios, /especialidad y ↩️ Volver de un oficio.
        Si cambia, afecta: tests/test_especializaciones.py.
        """
        t = self.texts
        slots_at = self._pspec_slots_at() or [25, 75]
        first, second = slots_at[0], slots_at[-1]
        specs = self._pspec_catalog()
        catalog = self._prof_catalog()
        body = [t.t("spec.intro", first=first, second=second), t.t("spec.mastery_rule", full=self._pspec_mastery_xp()), ""]
        ready = [pid for pid in catalog if profession_rules.spec_list(specs, pid) and self._prof_rank(hero, pid) >= first]
        for pid in ready:
            held = self._pspec_held(hero, pid)
            free = len(held) < profession_rules.spec_slots(self._prof_rank(hero, pid), slots_at)
            names = ", ".join(self._pspec_name(sid) for sid in held)
            state = (t.t("spec.state_held_free", names=names) if held and free else t.t("spec.state_held", names=names) if held
                     else t.t("spec.state_free"))
            body.append(t.t("spec.hub_line", name=self._prof_name(pid), rank=self._prof_rank(hero, pid), state=state))
        if not ready:
            body.append(t.t("spec.none", rank=first))
        later = [self._prof_name(pid) for pid in catalog if profession_rules.spec_list(specs, pid)
                 and hero.professions.get(pid, 0) > 0 and self._prof_rank(hero, pid) < first]
        if later:
            body += ["", t.t("spec.locked_list", rank=first, items=", ".join(later))]
        per = int(self._pspec_cfg().get("per_page", 2))
        pages = 1 if len(ready) <= 3 else (len(ready) + per - 1) // per
        page %= pages
        shown = ready if pages == 1 else ready[page * per: page * per + per]
        actions = [Action(id=f"pspec:{pid}", label=self._prof_name(pid)) for pid in shown]
        if pages > 1:
            body.append(t.t("prof.page", n=page + 1, total=pages))
            actions.append(Action(id=f"pspecs:{(page + 1) % pages}", label=t.t("prof.more")))
        actions.append(Action(id="oficios", label=t.t("menu.back")))
        return View(kind="specs", title=t.t("spec.title"), body=body, actions=actions[:4], notice=notice)

    def _pspec_prof_view(self, hero: Hero, pid: str, notice: str | None = None) -> View:
        """🎓 One profession: its three specializations with their full effect, which you hold (mastery) or saved, and its
        exclusive recipes. A button per specialization and ↩️ Volver (4).

        [ES]
        Qué hace: la pantalla de las especializaciones de un oficio: tu rango, cuántos lugares tienes (0 antes del 25, 1 hasta el
        74, 2 desde el 75), cada especialización con su efecto completo, si la tienes (✅ con su dominio), si la tuviste (💾 dominio
        guardado) y sus recetas exclusivas. Un botón por especialización (abre su detalle) y ↩️ Volver a 🎓 Especialización.
        La llaman: los botones de oficio de 🎓 Especialización, y elegir o cambiar al terminar.
        Si cambia, afecta: tests/test_especializaciones.py.
        """
        t = self.texts
        specs = profession_rules.spec_list(self._pspec_catalog(), pid)
        if not specs or pid not in self._prof_catalog():
            return self._pspecs_view(hero, notice=notice)
        slots_at = self._pspec_slots_at()
        rank = self._prof_rank(hero, pid)
        held = self._pspec_held(hero, pid)
        slots = profession_rules.spec_slots(rank, slots_at)
        body = [t.t("spec.prof_intro", name=self._prof_name(pid), rank=rank, title=self._rank_title(rank), used=len(held), slots=slots)]
        if slots < len(slots_at):
            body.append(t.t("spec.next_first" if slots == 0 else "spec.next_second", rank=slots_at[slots]))
        body.append("")
        for sdef in specs:
            sid = sdef["id"]
            if sid in held:
                body.append(t.t("spec.line_held", name=self._pspec_name(sid), bar=self._pspec_bar(hero, sid)))
            elif self._pspec_share(hero, sid) > 0:
                body.append(t.t("spec.line_saved", name=self._pspec_name(sid), pct=int(100 * self._pspec_share(hero, sid) + 1e-9)))
            else:
                body.append(t.t("spec.line_other", name=self._pspec_name(sid)))
            body.append(t.t("spec.effect_line", effect=self._pspec_effect_text(sdef, 1.0)))
            exclusive = self._pspec_exclusives(sid)
            if exclusive:
                body.append(t.t("spec.exclusive_line", items=", ".join(self._recipe_name(rid) for rid in exclusive)))
        actions = [Action(id=f"pspv:{sdef['id']}", label=(t.t("spec.held_mark") if sdef["id"] in held else "") + self._pspec_name(sdef["id"]))
                   for sdef in specs[:3]]
        actions.append(Action(id="pspecs", label=t.t("menu.back")))
        return View(kind="prof_specs", title=t.t("spec.prof_title", name=self._prof_name(pid)), body=body, actions=actions, notice=notice)

    def _pspec_view(self, hero: Hero, sid: str, notice: str | None = None) -> View:
        """🎓 One specialization: what it does now and with all its mastery, its exclusive recipes and how to get it.

        [ES]
        Qué hace: el detalle de una especialización: de qué oficio es, qué hace, tu dominio (barra), su efecto ahora y con todo el
        dominio, sus recetas exclusivas (✅ abierta o 🔒 con el rango y el dominio que piden) y qué puedes hacer: nada si ya la
        tienes; 🔒 si tu rango no abre lugar; 🎓 Elegir si tienes un lugar libre (gratis); o 🔄 Dejar <otra> (cuesta monedas, una por
        cada una que tienes, y pide confirmación). Botones: 3 como mucho más ↩️ Volver al oficio.
        La llaman: los botones de especialización de la pantalla del oficio, y _pspec_switch_view al cancelar.
        Si cambia, afecta: tests/test_especializaciones.py.
        """
        t = self.texts
        pid, sdef = profession_rules.spec_owner(self._pspec_catalog(), sid)
        if not sdef or pid not in self._prof_catalog():
            return self._pspecs_view(hero, notice=notice)
        rank = self._prof_rank(hero, pid)
        share = self._pspec_share(hero, sid)
        held = self._pspec_held(hero, pid)
        body = [self._pspec_name(sid), t.t("spec.of_prof", prof=self._prof_name(pid), rank=rank, title=self._rank_title(rank)),
                t.t(f"spec.{sid}.desc"), "", t.t("spec.mastery_line", bar=self._pspec_bar(hero, sid)),
                t.t("spec.effect_now", effect=self._pspec_effect_text(sdef, share)),
                t.t("spec.effect_full", effect=self._pspec_effect_text(sdef, 1.0)), ""]
        exclusive = self._pspec_exclusives(sid)
        need = int(100 * float(self._pspec_cfg().get("recipe_mastery", 0.0)) + 1e-9)
        if exclusive:
            body.append(t.t("spec.exclusive_title"))
            for rid in exclusive:
                rdef = self._recipes()[rid]
                ok = self._pspec_recipe_ok(hero, rdef) and rank >= int(rdef.get("min_rank", 1))
                body.append(t.t("spec.exclusive_entry", mark="✅" if ok else "🔒", item=self._recipe_name(rid),
                                rank=rdef.get("min_rank", 1), pct=need))
        else:
            body.append(t.t("spec.exclusive_none"))
        body.append("")
        choice = self._pspec_choice(hero, pid, sid)
        actions = []
        if choice == "held":
            body.append(t.t("spec.held_note", prof=self._prof_name(pid)))
        elif choice == "locked":
            body.append(t.t("spec.locked_note", rank=(self._pspec_slots_at() or [25])[0], prof=self._prof_name(pid), have=rank))
        elif choice == "pick":
            body.append(t.t("spec.pick_note", n=len(held) + 1, prof=self._prof_name(pid)))
            actions.append(Action(id=f"pspp:{sid}", label=t.t("spec.pick_button", name=t.t(f"spec.{sid}.name"))))
        else:
            cost = self._money(self._pspec_cost(hero, pid))
            body.append(t.t("spec.switch_note", cost=cost, pct=int(100 * share + 1e-9)))
            for old in held[:2]:
                actions.append(Action(id=f"pspx:{sid}:{old}", label=t.t("spec.switch_button", name=t.t(f"spec.{old}.name"), cost=cost)))
        actions.append(Action(id=f"pspec:{pid}", label=t.t("menu.back")))
        return View(kind="spec", title=t.t("spec.view_title"), body=body, actions=actions, notice=notice)

    def _pspec_switch_view(self, hero: Hero, sid: str, old: str) -> View:
        """🔄 Asks before switching: what you leave (its mastery stays saved), what you take (its saved mastery) and the price."""
        t = self.texts
        pid, sdef = profession_rules.spec_owner(self._pspec_catalog(), sid)
        if not sdef or self._pspec_choice(hero, pid, sid) != "switch" or old not in self._pspec_held(hero, pid):
            return self._pspec_view(hero, sid) if sdef else self._pspecs_view(hero)
        cost = self._pspec_cost(hero, pid)
        body = [t.t("spec.confirm_body", old=self._pspec_name(old), new=self._pspec_name(sid), cost=self._money(cost)),
                t.t("spec.confirm_lose", pct=int(100 * self._pspec_share(hero, old) + 1e-9)),
                t.t("spec.confirm_start", new=self._pspec_name(sid), pct=int(100 * self._pspec_share(hero, sid) + 1e-9)),
                t.t("spec.gold_line", have=self._money(hero.gold))]
        actions = [Action(id=f"pspx!:{sid}:{old}", label=t.t("spec.confirm_button", cost=self._money(cost))),
                   Action(id=f"pspv:{sid}", label=t.t("menu.back"))]
        return View(kind="spec_switch", title=t.t("spec.confirm_title"), body=body, actions=actions)

    def _pspec_pick(self, hero: Hero, sid: str) -> View:
        """🎓 Elegir: take a specialization in a free slot (the first from rank 25, the second from 75), for free.

        [ES]
        Qué hace: suma la especialización a las del oficio si hay lugar libre (gratis). Si ya la tienes, tu rango no alcanza o
        tus lugares están llenos, avisa y no cambia nada. Su dominio empieza donde quedó (0 si nunca la tuviste).
        La llama: el botón 🎓 Elegir. Si cambia, afecta: Hero.prof_specs.
        """
        t = self.texts
        pid, sdef = profession_rules.spec_owner(self._pspec_catalog(), sid)
        if not sdef:
            return self._pspecs_view(hero)
        choice = self._pspec_choice(hero, pid, sid)
        if choice != "pick":
            notices = {"held": t.t("spec.err_held"), "switch": t.t("spec.err_full"),
                       "locked": t.t("spec.err_locked", rank=(self._pspec_slots_at() or [25])[0], prof=self._prof_name(pid))}
            return self._pspec_view(hero, sid, notice=notices[choice])
        hero.prof_specs[pid] = self._pspec_held(hero, pid) + [sid]
        hero.spec_xp.setdefault(sid, 0)
        return self._pspec_prof_view(hero, pid, notice=t.t("spec.picked", name=self._pspec_name(sid), prof=self._prof_name(pid)))

    def _pspec_switch(self, hero: Hero, sid: str, old: str) -> View:
        """🔄 Switch: pay the coins and put `sid` in the place of `old`; old's mastery stays saved (all or nothing).

        [ES]
        Qué hace: cambia una especialización por otra del mismo oficio: cobra balance.yaml specs.switch_cost (sube con el rango,
        P-105) y pone la nueva en el lugar de la vieja. La vieja deja de dar su efecto y sus recetas exclusivas, pero su dominio
        queda guardado (Hero.spec_xp) por si vuelves; la nueva empieza con el dominio que tenía guardado (0 si nunca la tuviste).
        Sin monedas, sin lugar lleno o con algo que no cuadra, avisa y no cobra nada (regla 6).
        La llama: el botón ✅ Sí, cambiar. Si cambia, afecta: Hero.prof_specs y las monedas (un sumidero).
        """
        t = self.texts
        pid, sdef = profession_rules.spec_owner(self._pspec_catalog(), sid)
        if not sdef:
            return self._pspecs_view(hero)
        held = self._pspec_held(hero, pid)
        if self._pspec_choice(hero, pid, sid) != "switch" or old not in held:
            return self._pspec_view(hero, sid, notice=t.t("spec.err_switch"))
        cost = self._pspec_cost(hero, pid)
        if hero.gold < cost:
            return self._pspec_view(hero, sid, notice=t.t("spec.no_gold", cost=self._money(cost), have=self._money(hero.gold)))
        hero.gold -= cost
        hero.prof_specs[pid] = [sid if s == old else s for s in held]
        hero.spec_xp.setdefault(sid, 0)
        return self._pspec_prof_view(hero, pid, notice=t.t("spec.switched", old=self._pspec_name(old), new=self._pspec_name(sid),
                                                             cost=self._money(cost)))

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
        """Places this hero remembers, nearest first, with an estimated trip time (D-61).

        [ES]
        Qué hace: 📒 Lugares: los 3 lugares que recuerdas más cerca (la guarida del Guardián siempre, D-82), con el tiempo
        del viaje; al elegir uno, el héroe va solo, zona por zona. Desde D-106 se abre en 🧭 Explorar → 🗺️ Mapa → 📒 Lugares
        (su ↩️ Volver vuelve al mapa), para dejarle lugar a 🏹 Cazar en 🧭 Explorar. D-112: desde el rango 10 de
        🧭 Explorador (explorer.ranks.travel) la lista llega a explorer.places_listed lugares con su tiempo (los botones
        siguen siendo 3), y un lugar con un ⛺ campamento enemigo en pie lo dice.
        La llaman: el botón 📒 Lugares del mapa y un "goto:" que ya no sirve.
        Si cambia, afecta: tests/test_service.py, tests/test_boss.py y tests/test_enemy_camps.py (lugares y guarida), el
        paso use_places del tutorial.
        """
        t = self.texts
        places = []
        for key in hero.known:
            x, y = (int(v) for v in key.split(":"))
            if (x, y) == (hero.x, hero.y):
                continue
            places.append((self._trip_seconds(hero, x, y), x, y))
        places.sort()
        shown = places[:3]
        lair = next((p for p in places if self._is_lair(p[1], p[2])), None)
        if lair and lair not in shown:
            shown = shown[:2] + [lair]          # the Guardian's lair is always offered (D-82)
        count = int(self._explorer_cfg()["places_listed"]) if self._explorer_has(hero, "travel") else 3
        listed = places[:count]
        if lair and lair not in listed:
            listed = listed[:count - 1] + [lair]
        body = [t.t("places.intro", n=len(hero.known))]
        for seconds, x, y in listed:
            zone = self._zone(x, y)
            mark = t.t("guardian.route_mark") if self._is_lair(x, y) else ""
            mark += t.t("ecamp.route_mark") if self._ecamp_standing(x, y) else ""     # D-112
            body.append(t.t("places.line", biome=self.content.biomes[zone.biome]["emoji"], name=self._zone_name(zone) + mark,
                            zones=abs(x - hero.x) + abs(y - hero.y), time=self._fmt_duration(seconds)))
        actions = []
        for seconds, x, y in shown:
            zone = self._zone(x, y)
            actions.append(Action(id=f"goto:{x}:{y}", label=t.t("places.go_button", name=self._zone_name(zone), time=self._fmt_duration(seconds))))
        if not places:
            body.append(t.t("places.none"))
        elif len(places) > len(listed):
            body.append(t.t("places.more", n=len(places) - len(listed)))
        if count == 3 and len(places) > 3:
            body.append(t.t("explorer.places_hint", rank=self._explorer_cfg()["ranks"]["travel"], n=self._explorer_cfg()["places_listed"]))
        actions.append(Action(id="map", label=t.t("menu.back")))
        return View(kind="places", title=t.t("places.title"), body=body, actions=actions)

    def _map_view(self, hero: Hero) -> View:
        """A square map around the hero: (2 × map_view.radius + 1) cells wide and as many tall.

        [ES]
        Qué hace: dibuja el mapa como un cuadrado de cuadritos alrededor del héroe, tan ancho como el mensaje y
        igual de alto (pedido del dueño). Con radio 6 son 13 × 13: llena el mensaje en los teléfonos grandes y no
        se parte en los de 375 puntos de ancho. Más radio puede partir las filas en teléfonos chicos.
        D-112: ⛺ marca los campamentos enemigos de hoy que ves (tu zona y las vecinas; con el 🧭 Explorador, a 3 zonas desde el
        rango 25 y todo el mapa desde el 50); debajo, los más cercanos (con su tiempo desde el rango 10 y su fuerza desde el
        75), hasta dónde ves y, desde el rango 10, el tiempo a la guarida y a tu campamento.
        La llaman: 🧭 Explorar → 🗺️ Mapa. Botones: 📒 Lugares (se mudó aquí desde 🧭 Explorar con D-106), ⛺ Ir al campamento
        enemigo más cercano que ves (D-112, si no estás ocupado ni parado en él) y ↩️ Volver: 3.
        Si cambia, afecta: cuánto del mundo ves de una vez y el largo del mensaje; que 📒 Lugares siga a mano
        (tests/test_enemy_camps.py, tests/test_boss.py).
        """
        t = self.texts
        radius = self.content.balance["map_view"]["radius"]
        seen = self._ecamp_seen(hero)                   # D-112: the enemy camps this hero sees today
        marks = {(camp["x"], camp["y"]) for camp in seen}
        rows = []
        for y in range(hero.y + radius, hero.y - radius - 1, -1):
            row = ""
            for x in range(hero.x - radius, hero.x + radius + 1):
                if x == hero.x and y == hero.y:
                    row += "🧍"
                elif self._is_lair(x, y) and (hero.remembers(x, y) or self._discovered(x, y) is not None):
                    row += "👑"
                elif (x, y) in marks:
                    row += "⛺"
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
        body += self._ecamp_map_lines(hero, seen)
        actions = [Action(id="places", label=t.t("menu.places"))]
        target = next((camp for camp in seen if (camp["x"], camp["y"]) != (hero.x, hero.y)), None)
        if target and not hero.activity:               # D-112: ⛺ go to the nearest enemy camp you see
            label = (t.t("ecamp.go_button_time", time=self._fmt_duration(self._trip_seconds(hero, target["x"], target["y"])))
                     if self._explorer_has(hero, "travel") else t.t("ecamp.go_button"))
            actions.append(Action(id=f"goto:{target['x']}:{target['y']}", label=label))
        actions.append(Action(id="explore_menu", label=t.t("menu.back")))
        return View(kind="map", title=t.t("map.title"), body=body, actions=actions)

    def _hero_view(self, hero: Hero) -> View:
        """Hero sheet (D-76): level, xp, health, /stats, attack and defense, energy, resource, coins, /inv, /habilidades, status.

        [ES] Qué hace: la ficha del héroe. Desde D-117 suma el origen (con el atajo /historia), el emblema de su mejor oficio y
        la biografía de /bio, y los títulos de la historia junto a los de Pionero. Sigue con 4 botones (tests/test_gear.py).
        """
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
            t.t("hero.trades_link"),                                    # D-109: ⚒️ Oficios lives behind /oficios
            *([t.t("guardian.titles_line", titles=", ".join(self._title_name(x) for x in hero.titles))] if hero.titles else []),
            *self._story_hero_lines(hero),                              # D-117: origin (/historia), role emblem and /bio
            t.t("hero.level_pct", level=hero.level, pct=f"{pct:.2f}"),
            t.t("hero.xp_line", xp=hero.xp, next=high),
            t.t("hero.hp_line", hp=hero.hp, max_hp=stats["max_hp"]),
            *self._recovery_lines(hero, stats["max_hp"]),
            t.t("hero.stats_link"),
            t.t("hero.atk_def", attack=round(stats["attack"], 1), armor=round(stats["armor"] * 100)),
            t.t("hero.energy_line", energy=hero.energy, max_energy=self.content.balance["energy"]["max"]),
            t.t("hero.resource_line", resource=t.t(f"resource.{cdef['resource']}"), max=cdef.get("resource_max", 100)),
            self._coins_line(hero),
            t.t("hero.inv_link", n=self._bag_used(hero), cap=self._bag_cap(hero)),     # same count as "space in the backpack" (D-87)
            "",
            t.t("hero.status_title", status=self._status_text(hero)),
        ]
        cfg = self.content.balance["invite"]
        body += ["", t.t("invite.line", code=self.invite_code(hero.id), n=hero.invites, bonus=cfg["bonus_referrer"], level=cfg["reward_level"])]
        body += self._tutorial_hint(hero)
        actions = [Action(id="bag", label=t.t("bag.button_new" if hero.gear_new else "menu.bag")), Action(id="talents", label=t.t("talents.button", n=hero.points)),
                   Action(id="stats", label=t.t("hero.stats_button")), Action(id="health", label=t.t("health.button"))]   # 4 buttons (D-75): back with the menu
        return View(kind="hero", title=t.t("hero.title"), body=body, actions=actions, meta={"invite_code": self.invite_code(hero.id)})

    def _coins_line(self, hero: Hero) -> str:
        """🥉 bronze · 🥈 silver · 🥇 gold · 💰 bags · 🪎 chests · 💎 diamonds, each with its amount, zeros included (D-86, D-92)."""
        cfg = self.content.balance["currency"]
        rate = cfg["rate"]
        gold, rest = divmod(max(0, hero.gold), rate * rate)
        silver, bronze = divmod(rest, rate)
        icons = cfg["icons"]
        parts = [(icons["bronze"], bronze), (icons["silver"], silver), (icons["gold"], gold), (icons["bags"], hero.bags),
                 (icons["chests"], hero.chests), (icons["gems"], hero.gems)]
        return self.texts.t("hero.coins_line", coins="   ".join(f"{i} {n}" for i, n in parts))

    def _recovery_lines(self, hero: Hero, max_hp: int) -> list[str]:
        """How health comes back by itself: normal, or much slower after falling (D-83)."""
        if hero.hp >= max_hp:
            return []
        regen = self.content.balance["regen"]
        full = (regen["downed_full_minutes"] if hero.downed else regen["hp_full_minutes"]) / self._camp_regen_mult(hero)   # D-101
        seconds = (max_hp - hero.hp) / max_hp * full * 60 * self.time_scale
        key = "hero.downed_line" if hero.downed else "hero.regen_line"
        return [self.texts.t(key, full=self._fmt_duration(full * 60), time=self._fmt_duration(seconds))]

    def _status_text(self, hero: Hero) -> str:
        t = self.texts
        if self.store.get("combat", hero.id):
            return t.t("hero.status.combat")
        kind = (hero.activity or {}).get("kind")
        return t.t(f"hero.status.{kind}") if kind else t.t("hero.status.idle")

    def _health_view(self, hero: Hero) -> View:
        """🩺 Salud: how your body is right now, how it recovers and what can cure it (owner's request).

        [ES]
        Qué hace: junta todo lo de la salud del héroe en una pantalla: vida, cómo está el cuerpo (sano, magullado,
        herido, muy herido o 🤕 malherido), cuánto falta para curarse solo, las enfermedades (hoy ninguna: llegan
        con la capa de salud, D-09) y con qué curarse. Aquí aparecerán las heridas por partes y las enfermedades.
        La llaman: el botón 🩺 Salud de la ficha del héroe y el atajo /salud.
        Si cambia, afecta: dónde ve el jugador su estado; los números salen de balance.yaml regen.
        """
        t = self.texts
        max_hp = hero_stats(self._kit(hero), hero.level)["max_hp"]
        pct = round(100 * hero.hp / max(1, max_hp))
        if hero.downed:
            body_state = "downed"
        else:
            body_state = next(name for name, low in (("healthy", 100), ("bruised", 60), ("hurt", 25), ("badly_hurt", 0)) if pct >= low)
        regen = self.content.balance["regen"]
        body = [t.t("health.hp", hp=hero.hp, max_hp=max_hp, pct=pct, bar=self._bar(hero.hp, max_hp, 10)),
                t.t("health.body", state=t.t(f"health.state.{body_state}")),
                *self._recovery_lines(hero, max_hp),
                t.t("health.recovery", full=self._fmt_duration(regen["hp_full_minutes"] * 60),
                    downed=self._fmt_duration(regen["downed_full_minutes"] * 60)),
                "",
                t.t("health.diseases"),
                t.t("health.toxicity"),
                "",
                t.t("health.cures"),
                t.t("health.coming")]
        actions = [Action(id="potions", label=t.t("potions.button")), Action(id="hero", label=t.t("menu.back"))]
        return View(kind="health", title=t.t("health.title"), body=body, actions=actions)

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
            t.t("stats.talents_armor" if round(bonus.get("armor", 0) * 100) else "stats.talents",   # D-110: Defensa points add armor
                attack=round(bonus.get("attack", 0) * 100), hp=round(bonus.get("hp", 0) * 100), armor=round(bonus.get("armor", 0) * 100)),
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
        """The backpack hub: what each button holds (it never lists everything you carry), the space line, health.

        [ES]
        Qué hace: explica para qué sirve cada botón (🛡️ Equipo, 🧪 Pociones, 💰 Monedas, 📦 Recursos) en lugar de
        listar todo lo que llevas: con miles de cosas no se podría leer (pedido del dueño). Muestra el espacio
        (o la mochila llena, D-90). Son 4 botones (D-75): para volver al héroe está 👤 Héroe en el menú de abajo.
        La llaman: el botón 🎒 Mochila de la ficha del héroe y el atajo /inv.
        Si cambia, afecta: cómo llega el jugador a su equipo, pociones, monedas y recursos.
        """
        t = self.texts
        space = self._bag_full_line(hero) if self._bag_full(hero) else t.t("batch.space", used=self._bag_used(hero), cap=self._bag_cap(hero))
        body = [t.t("bag.intro"), t.t("bag.help_gear"), t.t("bag.help_potions"), t.t("bag.help_wallet"), t.t("bag.help_resources"),
                "", space, self._status_line(hero)]
        body += self._recovery_lines(hero, hero_stats(self._kit(hero), hero.level)["max_hp"])
        actions = [Action(id="gear", label=t.t("gear.button_new" if hero.gear_new else "gear.button")),
                   Action(id="potions", label=t.t("potions.button")), Action(id="wallet", label=t.t("wallet.button")),
                   Action(id="resources", label=t.t("resources.button"))]
        return View(kind="bag", title=t.t("bag.title"), body=body, actions=actions)

    def _resources_view(self, hero: Hero, page: int = 0) -> View:
        """📦 Recursos: materials and food you carry, how many and what they are for, a page at a time.

        [ES]
        Qué hace: lista los materiales, la comida y los 🪑 muebles (D-116) de la mochila (no el equipo, que está en
        🛡️ Equipo, ni las pociones, que están en 🧪 Pociones), de a resources.per_page por página, con para qué sirve
        cada uno.
        La llaman: el botón 📦 Recursos de la mochila.
        Si cambia, afecta: dónde ve el jugador lo que recolectó (tope de 4 botones, D-75).
        """
        t = self.texts
        per = self.content.balance["resources"].get("per_page", 8)
        kinds = ("material", "food", "furniture")       # D-116: 🪑 furniture waits here until it is placed
        owned = sorted(((i, n) for i, n in hero.backpack.items() if n > 0 and self.content.items.get(i, {}).get("kind") in kinds),
                       key=lambda kv: (-kv[1], kv[0]))
        pages = max(1, (len(owned) + per - 1) // per)
        page %= pages
        body = [t.t("resources.intro")]
        for item_id, n in owned[page * per: page * per + per]:
            item = self.content.items[item_id]
            use = t.t(f"resources.use.{item_id}") if t.has(f"resources.use.{item_id}") else t.t("resources.use_default")
            body.append(t.t("resources.line", emoji=item["emoji"], item=t.t(item["name_key"]), n=n, use=use))
        if not owned:
            body.append(t.t("resources.none"))
        if pages > 1:
            body.append(t.t("resources.page", n=page + 1, total=pages))
        space = self._bag_full_line(hero) if self._bag_full(hero) else t.t("batch.space", used=self._bag_used(hero), cap=self._bag_cap(hero))
        body += ["", space]
        actions = [Action(id=f"res:{page + 1}", label=t.t("resources.more"))] if pages > 1 else []
        actions.append(Action(id="bag", label=t.t("menu.back")))
        return View(kind="resources", title=t.t("resources.title"), body=body, actions=actions)

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
        """The currencies: bronze, silver, gold (earned), bags (sewn), chests (assembled, D-92), gems (bought), cards.

        [ES]
        Qué hace: muestra cada moneda con su ayuda. En el Claro, o en tu campamento con 🧵 Taller (D-101): 💰 Coser una
        bolsa, 🪎 Armar cofre, 💎 Tienda de diamantes y ↩️ Volver (4 botones, D-75); en otro lugar, un aviso de dónde se hacen.
        La llaman: el botón 💰 Monedas de la mochila y el atajo /monedas.
        Si cambia, afecta: dónde se cosen las bolsas y se arman los cofres (tests/test_currency.py, tests/test_backpack.py).
        """
        t = self.texts
        cfg = self.content.balance["currency"]
        can_craft = self._can_craft(hero)          # the Claro, or your camp's 🧵 Taller (D-101)
        bags_need, materials = self._chest_recipe()
        body = [
            t.t("wallet.coins", coins=self._money(hero.gold)),
            t.t("wallet.coins_help", rate=cfg["rate"]),
            "",
            t.t("wallet.bags", n=hero.bags),
            t.t("wallet.bags_help", items=self._item_list(cfg["bag_recipe"]), coins=self._money(cfg["bag_coins"])),
            "",
            t.t("wallet.chests", n=hero.chests),
            t.t("wallet.chests_help", bags=bags_need, items=self._item_list(materials),
                level=self.content.balance["camps"]["chests_from_level"]),
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
        if can_craft:     # 4 buttons at most (D-75): sew, chest, gems, back
            actions += [Action(id="sew", label=t.t("wallet.sew_button")), Action(id="chest", label=t.t("wallet.chest_button"))]
        else:
            body.append(t.t("wallet.sew_in_claro"))
        actions += [Action(id="gems", label=t.t("wallet.gems_button")), Action(id="bag", label=t.t("menu.back"))]
        return View(kind="wallet", title=t.t("wallet.title"), body=body, actions=actions, notice=notice)

    def _chest_recipe(self) -> tuple[int, dict[str, int]]:
        """Bags and backpack materials one 🪎 chest needs (balance currency.chest_recipe; "bags" means Hero.bags)."""
        recipe = dict(self.content.balance["currency"]["chest_recipe"])
        return int(recipe.pop("bags", 0)), recipe

    def _build_chest(self, hero: Hero) -> View:
        """Assemble one 🪎 chest in the Claro (or your camp's 🧵 Taller, D-101): 10 sewn bags plus wood and metal (D-92).

        [ES]
        Qué hace: arma un cofre con 10 💰 bolsas (de Hero.bags) y madera y metal de la mochila; solo en el Claro o en tu
        campamento con 🧵 Taller (_can_craft), sin actividad. Si falta algo, avisa la receta y no gasta nada.
        La llaman: el botón 🪎 Armar cofre de 💰 Monedas y el del 🧵 Taller (tchest).
        Si cambia, afecta: el crecimiento de los campamentos grandes (_grow_chests) y cuántas bolsas y materiales
        salen del juego (balance.yaml currency.chest_recipe).
        """
        t = self.texts
        if not self._can_craft(hero):              # the Claro, or your camp's 🧵 Taller (D-101)
            return self._wallet_view(hero, notice=t.t("shop.only_in_claro"))
        bags, materials = self._chest_recipe()
        if hero.bags < bags or any(hero.backpack.get(i, 0) < n for i, n in materials.items()):
            return self._wallet_view(hero, notice=t.t("wallet.chest_missing", bags=bags, have=hero.bags, items=self._item_list(materials)))
        for item_id, n in materials.items():
            hero.backpack[item_id] -= n
            if hero.backpack[item_id] <= 0:
                del hero.backpack[item_id]
        hero.bags -= bags
        hero.chests += 1
        return self._wallet_view(hero, notice=t.t("wallet.chest_built", n=hero.chests))

    def _sew_bag(self, hero: Hero) -> View:
        """Sew one bag in the Claro (or your camp's 🧵 Taller, D-101): thread, a metal clasp and coins (a sink).

        [ES] Qué hace: cose una 💰 bolsa. La llaman: 💰 Coser una bolsa de 💰 Monedas y del 🧵 Taller (tsew).
        Si cambia, afecta: dónde se cosen las bolsas (tests/test_currency.py, tests/test_camp_upgrades.py).
        """
        t = self.texts
        cfg = self.content.balance["currency"]
        if not self._can_craft(hero):              # the Claro, or your camp's 🧵 Taller (D-101)
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
        """"🟣🏹 Arco del artesano" (rarity, emoji, name), with the ✒️ mark when it is a masterwork (D-116)."""
        item = self.content.items[item_id]
        icon = self.content.balance["gear"]["rarity_icon"].get(item.get("rarity", "comun"), "")
        return f"{icon}{item['emoji']} {self.texts.t(item['name_key'])}" + self._masterwork_mark(item_id)

    def _masterwork_mark(self, item_id: str) -> str:
        """" ✒️" after the name of a masterwork piece (D-116), "" for any other item."""
        return self.texts.t("gear.masterwork_mark") if self.content.items.get(item_id, {}).get("masterwork") else ""

    def _masterwork_note(self, hero: Hero, item_id: str) -> str:
        """"✒️ Obra maestra de Lyra" for a masterwork the hero holds (D-116); "" for any other piece.

        [ES]
        Qué hace: da la firma de una ✒️ obra maestra (quién la hizo, de Hero.gear_signatures); sin firma guardada,
        solo "✒️ Obra maestra". Para cualquier otra pieza, vacío.
        La llaman: 🔁 Equipar (_gear_view) y la pieza (_item_view).
        Si cambia, afecta: cómo se ve la firma del artesano.
        """
        if not self.content.items.get(item_id, {}).get("masterwork"):
            return ""
        who = (hero.gear_signatures or {}).get(item_id)
        return self.texts.t("gear.masterwork_by", name=who) if who else self.texts.t("gear.masterwork_unsigned")

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
        """What a piece gives this hero: half if off type, plus its ✨ enchantment (D-115; engine/hero/gear.py real_stats)."""
        return real_stats(self.content.items, item_id, hero, self.content.classes, self.content.balance)

    def _gear_diff(self, hero: Hero, item_id: str) -> tuple[dict[str, float], float]:
        """Stats of a piece minus the piece worn in its slot, and a single score (>0 = better; gear_score, balance gear.score)."""
        item = self.content.items[item_id]
        mine = self._real_stats(hero, item_id)
        worn_id = hero.gear.get(item["slot"], "")
        worn = self._real_stats(hero, worn_id) if worn_id in self.content.items else {}
        diff = {k: mine.get(k, 0.0) - worn.get(k, 0.0) for k in sorted(set(mine) | set(worn))}
        return diff, gear_score(diff, self.content.balance)

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
                body.append(t.t("gear.simple_line", emoji=item["emoji"],
                                item=t.t(item["name_key"]) + self._masterwork_mark(item_id) + self._enchant_mark(hero, item_id)
                                + self._new_mark(hero, item_id),
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
        """Worn pieces, gear in the backpack marked for you / later / not for you, one button per piece; a ✒️ masterwork
        also says who made it (D-116)."""
        t = self.texts
        slots = self.content.balance["gear"]["slots"]
        body = []
        loose = [i for i in hero.backpack if self.content.items.get(i, {}).get("kind") == "gear"]
        better = {i for i in loose if self._is_better(hero, i)}           # D-115: ⬆️ better than what you wear (and usable)
        loose.sort(key=lambda i: (i not in hero.gear_new, i not in better,
                                  can_use(self.content.items[i], hero, self.content.classes, self.content.balance) is not None,
                                  not suits(self.content.items[i], hero, self.content.classes, self.content.balance), -self.content.items[i].get("tier", 1), i))
        if loose:
            body.append(t.t("gear.backpack_title", n=sum(hero.backpack[i] for i in loose)))
            for item_id in loose[:15]:
                count = hero.backpack[item_id]
                note = self._masterwork_note(hero, item_id)                     # D-116: ✒️ Obra maestra de Lyra
                body.append(t.t("gear.backpack_line", item=self._gear_name(item_id) + self._enchant_mark(hero, item_id)
                                + self._better_mark(hero, item_id) + self._new_mark(hero, item_id), n=f" ×{count}" if count > 1 else "",
                                status=self._gear_status(hero, self.content.items[item_id]) + (f" · {note}" if note else "")))
            body.append(t.t("gear.hint"))
            if better:
                body.append(t.t("gear.better_hint"))
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
            label = t.t("gear.piece_worn" if worn else "gear.piece_button", item=self._gear_name(item_id)
                        + ("" if worn else self._better_mark(hero, item_id)) + self._new_mark(hero, item_id))
            actions.append(Action(id=f"item:{item_id}", label=label))
        if len(pieces) > 3:
            actions.append(Action(id=f"gear:{page + 1}", label=t.t("gear.more")))
        actions.append(Action(id="gear", label=t.t("menu.back")))
        return View(kind="gear", title=t.t("gear.equip_title"), body=body, actions=actions, notice=notice)

    def _new_mark(self, hero: Hero, item_id: str) -> str:
        return " 🆕" if item_id in hero.gear_new else ""

    def _item_view(self, hero: Hero, item_id: str, notice: str | None = None) -> View:
        """One piece: slot, type, level, stats, for you or not, compared with what you wear; equip, take off or sell
        (sell in the Claro, or at your camp with its 🔨 Herrería, D-101). A ✒️ masterwork shows who made it (D-116).
        [ES] Qué hace: muestra una pieza; si es obra maestra, su firma ("✒️ Obra maestra de Lyra") y por qué es mejor.
        La llaman: los botones de 🔁 Equipar. Si cambia, afecta: tests/test_gear.py y tests/test_masterwork.py."""
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
        note = self._masterwork_note(hero, item_id)
        if note:                                    # D-116: ✒️ who made it, and why it is better
            body.insert(1, note)
            body.insert(2, t.t("gear.masterwork_help", pct=round(100 * float((self.content.balance.get("masterwork") or {}).get("stat_bonus", 0)))))
        enchant = self._enchant_text(hero, item_id)
        if enchant:                                 # D-115: ✨ its enchantment
            body.append(t.t("ench.item_line", enchant=enchant))
        if item_id in hero.gear_new:
            hero.gear_new.remove(item_id)
        actions = []
        in_claro = (hero.x == 0 and hero.y == 0 and not hero.activity) or self._sells_gear_here(hero)   # D-101: 🔨 Herrería
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
        if self._enchant_slot(item):                # D-115: ✨ Encantamiento (enchant it, or disenchant it from the backpack)
            actions.append(Action(id=f"ench:{item_id}", label=t.t("ench.item_button")))
        actions.append(Action(id="gear:0", label=t.t("menu.back")))
        return View(kind="item", title=t.t("gear.item_title"), body=body, actions=actions, notice=notice)    # 4 at most: equip, sell, ✨, back

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
        price, _trade = self._merchant_sale(hero, price, "gear")   # D-116: 💱 Comercio (D-141: 🛡️ Tratante de equipo)
        hero.gold += price
        self._forget_piece(hero, item_id)                       # D-116 / D-115: the last copy takes its signature and enchantment
        story = self._story_event(hero, "sell", n=1, coins=price)                                    # D-117
        return self._gear_view(hero, notice=self._join([t.t("shop.sold", item=self._gear_name(item_id), price=self._money(price))] + story))

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
        xp = int(self._zone_xp(edef["xp"], enemy["level"]) * self._xp_mult(hero))
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

    # ------------------------------------------------------------------ enemy camps and the 🧭 Explorador (D-112)

    def _explorer_cfg(self) -> dict[str, Any]:
        return self.content.balance["explorer"]

    def _ecamp_cfg(self) -> dict[str, Any]:
        return self.content.balance["enemy_camps"]

    def _today(self) -> int:
        """Index of the real day: the same boundary as the pantry registry and the board's daily tasks (_day_seconds)."""
        return int(self.clock.now() // self._day_seconds())

    def _explorer_rank(self, hero: Hero) -> int:
        """The hero's 🧭 Explorador rank (1 if never started)."""
        return self._prof_rank(hero, self._explorer_cfg()["profession"])

    def _explorer_has(self, hero: Hero, key: str) -> bool:
        """True if the hero's 🧭 Explorador rank opens `key` (balance.yaml explorer.ranks: travel, camps_near, ...)."""
        return self._explorer_rank(hero) >= int(self._explorer_cfg()["ranks"][key])

    def _explorer_what(self, key: str) -> str:
        """What a 🧭 Explorador rank threshold opens, in words (⚒️ Oficios and the rank-up line)."""
        cfg = self._explorer_cfg()
        return self.texts.t(f"explorer.what.{key}", n=cfg["near_radius"], places=cfg["places_listed"])

    def _explorer_unlocks(self, hero: Hero, pid: str, before: int, after: int) -> list[str]:
        """Lines of the 🧭 Explorador thresholds crossed by a rank-up; rank 100 also gives the title (once, for ever)."""
        cfg = self._explorer_cfg()
        if pid != cfg["profession"]:
            return []
        lines: list[str] = []
        for key, rank in cfg["ranks"].items():
            if before < int(rank) <= after:
                lines.append(self.texts.t("explorer.opened", what=self._explorer_what(key)))
                if key == "master":
                    lines += self._grant_title(hero, cfg["title"])
        return lines

    def _explorer_prof_lines(self, hero: Hero, pid: str) -> list[str]:
        """⚒️ Oficios, 🧭 Explorador only: what every rank threshold opens on the map, ✅ the ones already open."""
        cfg = self._explorer_cfg()
        if pid != cfg["profession"]:
            return []
        t = self.texts
        rank = self._explorer_rank(hero)
        parts = [("✅" if rank >= int(need) else "") + t.t(f"explorer.short.{key}", rank=need, n=cfg["near_radius"])
                 for key, need in cfg["ranks"].items()]
        return [t.t("explorer.ranks_line", items=" · ".join(parts))]

    def _explorer_next(self, hero: Hero) -> str | None:
        """🔓 The next 🧭 Explorador threshold and what it opens (None at the top)."""
        rank = self._explorer_rank(hero)
        later = sorted((int(need), key) for key, need in self._explorer_cfg()["ranks"].items() if int(need) > rank)
        if not later:
            return None
        need, key = later[0]
        return self.texts.t("prof.next", rank=need, items=self._explorer_what(key))

    def _trip_seconds(self, hero: Hero, x: int, y: int) -> float:
        """Estimated travel time from the hero to a zone, leg by leg (the path 📒 Lugares follows)."""
        seconds, cx, cy = 0.0, hero.x, hero.y
        for nx, ny in self._path(hero.x, hero.y, x, y):
            seconds += self._leg_seconds(hero, cx, cy, nx, ny)
            cx, cy = nx, ny
        return seconds

    def _ecamp_exists(self, x: int, y: int, day: int | None = None) -> bool:
        """True if the zone holds an enemy camp that day (today by default), destroyed or not.

        [ES]
        Qué hace: dice si hay campamento enemigo en una zona ese día: el sorteo del día (engine/world/enemy_camps.py
        has_camp: Lejanía 2 o más, nunca dos días seguidos en la misma zona) y nunca en el Claro, en la guarida del
        Guardián, en el territorio de un campamento de jugadores ni donde el bioma no tiene peligro.
        La llaman: _ecamp y todo lo de esta sección. Si cambia, afecta: dónde están los campamentos de todos.
        """
        cfg = self._ecamp_cfg()
        day = self._today() if day is None else day
        if not camp_rules.has_camp(self.world_seed, day, x, y, cfg["density"], cfg["min_lejania"]):
            return False
        if self._is_lair(x, y) or self._territory(x, y):
            return False
        return self.content.biomes[self._zone(x, y).biome]["danger"] > 0

    def _ecamp(self, x: int, y: int, day: int | None = None) -> dict[str, Any] | None:
        """The enemy camp of a zone on a day (today by default) with what players did to it that day; None if none.

        [ES]
        Qué hace: arma el campamento enemigo de una zona: su nivel (zona + enemy_camps.level_bonus), su guarnición (el
        último es el jefe) y lo que guardó el almacén ese día: cuántos guardias vencieron entre todos ("beaten"), quién
        peleó ("fighters", héroe → peleas ganadas o perdidas), quién se infiltró ("scouted") y si ya cayó ("destroyed":
        quién lo terminó y cuándo). Sin registro, nadie lo tocó todavía.
        La llaman: _ecamp_standing, _ecamp_fight_done, la pantalla 🧭 Explorar y 📍 Zona.
        Si cambia, afecta: lo que comparten todos los que asaltan un campamento.
        """
        day = self._today() if day is None else day
        if not self._ecamp_exists(x, y, day):
            return None
        cfg = self._ecamp_cfg()
        zone = self._zone(x, y)
        level = zone.level + int(cfg["level_bonus"])
        record = self.store.get("enemy_camp", f"{day}:{x}:{y}") or {}
        members = camp_rules.garrison(self.world_seed, day, x, y, self.content.enemies, zone.biome, level, cfg["garrison"])
        return {"day": day, "x": x, "y": y, "level": level, "garrison": members,
                "beaten": int(record.get("beaten", 0)), "destroyed": record.get("destroyed"),
                "fighters": dict(record.get("fighters") or {}), "scouted": list(record.get("scouted") or [])}

    def _ecamp_save(self, camp: dict[str, Any]) -> None:
        """Keep what players did to a camp that day (shared by everyone); a day's first record drops the older ones."""
        key = f"{camp['day']}:{camp['x']}:{camp['y']}"
        if self.store.get("enemy_camp", key) is None:
            for old, data in list(self.store.items("enemy_camp")):
                if int(data.get("day", camp["day"])) < camp["day"] - 1:
                    self.store.delete("enemy_camp", old)
        self.store.put("enemy_camp", key, {"day": camp["day"], "x": camp["x"], "y": camp["y"], "beaten": camp["beaten"],
                                           "destroyed": camp["destroyed"], "fighters": camp["fighters"],
                                           "scouted": camp["scouted"]})

    def _ecamp_standing(self, x: int, y: int) -> dict[str, Any] | None:
        """Today's enemy camp of a zone if it still stands (not destroyed), else None."""
        camp = self._ecamp(x, y)
        return camp if camp and not camp["destroyed"] else None

    @staticmethod
    def _ecamp_left(camp: dict[str, Any]) -> int:
        """How many of the garrison still stand: the guards not beaten and the chief."""
        return 0 if camp["destroyed"] else len(camp["garrison"]) - camp["beaten"]

    @staticmethod
    def _ecamp_next(camp: dict[str, Any]) -> dict[str, Any]:
        """The garrison member the next fight is against: the first guard not beaten, then the chief."""
        return camp["garrison"][min(camp["beaten"], len(camp["garrison"]) - 1)]

    def _ecamp_sight(self, hero: Hero) -> int:
        """How many zones around it the hero sees enemy camps (1; 3 from 🧭 rank 25; the whole map from 50)."""
        return camp_rules.sight(self._explorer_rank(hero), self._explorer_cfg(), self.content.balance["map_view"]["radius"])

    def _ecamp_visible(self, hero: Hero, x: int, y: int) -> dict[str, Any] | None:
        """The standing camp at (x, y) if the hero sees it (within its sight, or it scouted it today), else None."""
        camp = self._ecamp_standing(x, y)
        if camp and (max(abs(x - hero.x), abs(y - hero.y)) <= self._ecamp_sight(hero) or hero.id in camp["scouted"]):
            return camp
        return None

    def _ecamp_seen(self, hero: Hero) -> list[dict[str, Any]]:
        """Standing enemy camps the hero sees on its 🗺️ Mapa, nearest first."""
        radius = self.content.balance["map_view"]["radius"]
        found = [camp for dx in range(-radius, radius + 1) for dy in range(-radius, radius + 1)
                 if (camp := self._ecamp_visible(hero, hero.x + dx, hero.y + dy))]
        found.sort(key=lambda c: (abs(c["x"] - hero.x) + abs(c["y"] - hero.y), c["x"], c["y"]))
        return found

    def _ecamp_intel(self, hero: Hero, camp: dict[str, Any]) -> bool:
        """True if the hero knows the camp's strength: it infiltrated it today, or its 🧭 rank is 75 or more."""
        return hero.id in camp["scouted"] or self._explorer_has(hero, "strength")

    def _ecamp_chest(self, camp: dict[str, Any]) -> dict[str, Any]:
        """What the camp's chest holds (fixed for the day: what 🕵️ Infiltrarse shows is what the finisher gets)."""
        resources = self._zone_resources(camp["x"], camp["y"])
        return camp_rules.chest(self.world_seed, camp["day"], camp["x"], camp["y"], camp["level"], resources,
                                self._ecamp_cfg()["chest"])

    def _ecamp_enemy_name(self, member: dict[str, Any]) -> str:
        return self.texts.t(self.content.enemies[member["id"]]["name_key"])

    def _ecamp_intel_lines(self, camp: dict[str, Any]) -> list[str]:
        """👹 who is left, 👑 the chief and 🎁 the chest of a camp (infiltration, or 🧭 rank 75 at the camp)."""
        t = self.texts
        cfg = self._ecamp_cfg()
        groups: dict[tuple[str, int], int] = {}
        for member in camp["garrison"][camp["beaten"]:-1]:
            groups[(member["id"], member["level"])] = groups.get((member["id"], member["level"]), 0) + 1
        names = ", ".join(t.t("ecamp.guard_group", enemy=self._ecamp_enemy_name({"id": eid}), n=n, level=level)
                          for (eid, level), n in groups.items())
        chief = camp["garrison"][-1]
        lines = [t.t("ecamp.intel_left", n=self._ecamp_left(camp), total=len(camp["garrison"]),
                     guards=names or t.t("ecamp.intel_no_guards")),
                 t.t("ecamp.intel_chief", enemy=self._ecamp_enemy_name(chief), level=chief["level"],
                     hp=round(100 * (cfg["chief_hp_mult"] - 1)), attack=round(100 * (cfg["chief_attack_mult"] - 1)))]
        chest = self._ecamp_chest(camp)
        items = [self._money(chest["coins"])] + ([self._item_list(chest["items"])] if chest["items"] else [])
        lines.append(t.t("ecamp.intel_chest", items=" · ".join(items), pct=round(100 * chest["gear_chance"]),
                         level=chest["gear_level"]))
        return lines

    def _ecamp_block_line(self, hero: Hero) -> str | None:
        """Why exploring and gathering wait in the hero's zone (a standing enemy camp), else None."""
        return self.texts.t("ecamp.blocked") if self._ecamp_standing(hero.x, hero.y) else None

    def _ecamp_zone_lines(self, zone: Zone) -> list[str]:
        """📍 Zona: a standing camp here (go to 🧭 Explorar → ⚔️ Asaltar), or the ruins of one that fell today."""
        camp = self._ecamp(zone.x, zone.y)
        if not camp:
            return []
        if camp["destroyed"]:
            return [self.texts.t("ecamp.ruins", name=camp["destroyed"].get("name", "?"))]
        return [self.texts.t("ecamp.zone_line")]

    def _ecamp_menu(self, hero: Hero, camp: dict[str, Any], notice: str | None = None) -> View:
        """🧭 Explorar in a zone with a standing enemy camp: [⚔️ Asaltar] [🕵️ Infiltrarse] [🏹 Cazar] [🗺️ Mapa].

        [ES]
        Qué hace: el menú de 🧭 Explorar cuando en tu zona hay un ⛺ campamento enemigo en pie (D-112): explorar y
        recolectar no se pueden (los enemigos no te dejan), así que sus lugares los toman ⚔️ Asaltar (cada pelea cuesta
        enemy_camps.fight_energy y vence a uno de la guarnición, para todos) y 🕵️ Infiltrarse (🧭 Explorador de rango 30;
        con menos, el botón dice el rango que pide). Dice cuántos vencieron hoy entre todos y, si te infiltraste hoy o
        tu rango de Explorador es 75 o más, quiénes quedan, el jefe y el cofre. 4 botones.
        La llama: _explore_menu. Si cambia, afecta: tests/test_enemy_camps.py y el tope de 4 botones.
        """
        t = self.texts
        zone = self._zone(hero.x, hero.y)
        cfg = self._ecamp_cfg()
        need = int(self._explorer_cfg()["ranks"]["infiltrate"])
        body = [t.t("zone.header", name=self._zone_name(zone), biome=self._biome_label(zone)), t.t("ecamp.here", level=camp["level"])]
        body.append(t.t("ecamp.progress", n=camp["beaten"]) if camp["beaten"] else t.t("ecamp.untouched"))
        if self._ecamp_intel(hero, camp):
            body += self._ecamp_intel_lines(camp)
        else:
            body.append(t.t("ecamp.intel_hint", rank=need))
        body += [t.t("ecamp.how", energy=cfg["fight_energy"]), self._status_line(hero)]
        body += self._tutorial_hint(hero)
        infiltrate = (t.t("ecamp.infiltrate_button", energy=cfg["infiltrate"]["energy"]) if self._explorer_rank(hero) >= need
                      else t.t("ecamp.infiltrate_locked_button", rank=need))
        actions = [Action(id="assault", label=t.t("ecamp.assault_button", energy=cfg["fight_energy"])),
                   Action(id="infiltrate", label=infiltrate),
                   Action(id="hunt", label=t.t("hunt.button")),
                   Action(id="map", label=t.t("menu.map"))]
        return View(kind="explore_menu", title=t.t("explore.menu_title"), body=body, actions=actions, notice=notice)

    def _ecamp_fight(self, hero: Hero, camp: dict[str, Any], how: str) -> str:
        """Start a fight against the camp's next garrison member (the chief, an elite, comes last). Always by hand (D-114).

        [ES]
        Qué hace: empieza la pelea contra el siguiente de la guarnición (el primer guardia sin vencer; al final, el jefe,
        con más vida y ataque: raids.scale_enemy). Marca la pelea con "enemy_camp" ({day, x, y, chief}) para que
        _end_combat la cuente para el campamento. Nunca va sola: _batch_fight no toca estas peleas (D-114).
        La llaman: _assault (⚔️ Asaltar) y _infiltrate (si te descubren). Devuelve el aviso de la pelea.
        Si cambia, afecta: contra quién pelea cada uno y qué tan difícil es el jefe.
        """
        t = self.texts
        member = self._ecamp_next(camp)
        edef = self.content.enemies[member["id"]]
        seed = int(hash_unit(self.world_seed, hero.id, "enemy_camp", camp["day"], camp["x"], camp["y"], self.clock.now()) * 2**31)
        state = make_combat(member["id"], edef, member["level"], self._kit(hero), seed)
        if member["chief"]:
            cfg = self._ecamp_cfg()
            raid_rules.scale_enemy(state, cfg["chief_hp_mult"], cfg["chief_attack_mult"])
        state["enemy_camp"] = {"day": camp["day"], "x": camp["x"], "y": camp["y"], "chief": member["chief"]}
        self.store.put("combat", hero.id, state)
        hero.activity = None
        self.bus.publish(CombatStarted(hero.id, member["id"], seed))
        key = "ecamp.chief_fight" if member["chief"] else f"ecamp.{how}_fight"
        return t.t(key, enemy=t.t(edef["name_key"]), level=member["level"])

    def _assault(self, hero: Hero) -> View:
        """⚔️ Asaltar: pay enemy_camps.fight_energy and fight the next of the camp's garrison right away (by hand).

        [ES]
        Qué hace: el botón ⚔️ Asaltar del menú del campamento enemigo: cobra la energía de una pelea (como una presa,
        D-108) y empieza enseguida la pelea contra el siguiente de la guarnición. Se rechaza sin cobrar si no hay
        campamento en pie aquí, si estás malherido o sin energía. Ocupado lo frena antes _idle_action.
        La llaman: ⚔️ Asaltar (🧭 Explorar en la zona del campamento, la pantalla de la infiltración y el final de una
        pelea ganada: ⚔️ Seguir asaltando). Si cambia, afecta: tests/test_enemy_camps.py.
        """
        t = self.texts
        camp = self._ecamp_standing(hero.x, hero.y)
        if not camp:
            return self._explore_menu(hero, notice=t.t("ecamp.none_here"))
        if hero.downed:
            return self._explore_menu(hero, notice=t.t("ecamp.downed"))
        if not self._spend_energy(hero, "assault", int(self._ecamp_cfg()["fight_energy"])):
            return self._explore_menu(hero, notice=self._no_energy_notice(hero))
        notice = self._ecamp_fight(hero, camp, "assault")
        return self._combat_view(hero, self.store.get("combat", hero.id), notice=notice)

    def _infiltrate(self, hero: Hero) -> View:
        """🕵️ Infiltrarse (🧭 Explorador rank 30+): not a fight. Success reveals the camp; if they find you, a fight starts.

        [ES]
        Qué hace: el Explorador se mete al campamento sin pelear (D-112). Pide rango explorer.ranks.infiltrate (30) y
        cuesta enemy_camps.infiltrate.energy (3 ⚡). Te descubren con detect_chance (45 % al rango 30, menos cada rango,
        10 % al 100): entonces empieza una pelea, a mano, con el siguiente de la guarnición (cuenta como un asalto). Si sale
        bien: quedas anotado para hoy ("scouted": ves su fuerza en 🧭 Explorar y en el mapa), ves quiénes quedan, el jefe y
        el cofre, y ganas un poco de exploración de esa zona y experiencia de Explorador. Una vez por campamento y día.
        Se rechaza sin cobrar sin campamento, con menos rango, ya infiltrado hoy, malherido o sin energía. D-141: la
        🎓 especialización 🕵️ Infiltrado baja la probabilidad de que te descubran (sin bajar de detect_min).
        La llama: el botón 🕵️ Infiltrarse. Si cambia, afecta: tests/test_enemy_camps.py.
        """
        t = self.texts
        camp = self._ecamp_standing(hero.x, hero.y)
        if not camp:
            return self._explore_menu(hero, notice=t.t("ecamp.none_here"))
        ecfg = self._explorer_cfg()
        need = int(ecfg["ranks"]["infiltrate"])
        rank = self._explorer_rank(hero)
        if rank < need:
            return self._explore_menu(hero, notice=t.t("ecamp.infiltrate_locked", need=need, rank=rank))
        if hero.id in camp["scouted"]:
            return self._explore_menu(hero, notice=t.t("ecamp.already_scouted"))
        if hero.downed:
            return self._explore_menu(hero, notice=t.t("ecamp.downed"))
        cfg = self._ecamp_cfg()["infiltrate"]
        if not self._spend_energy(hero, "infiltrate", int(cfg["energy"])):
            return self._explore_menu(hero, notice=self._no_energy_notice(hero))
        rng = Rng(int(hash_unit(self.world_seed, hero.id, "infiltrate", camp["x"], camp["y"], self.clock.now()) * 2**31))
        detect = max(float(cfg["detect_min"]), camp_rules.detect_chance(rank, cfg, need) - self._pspec_bonus(hero, "detect"))   # D-141
        if rng.chance(detect):
            notice = self._ecamp_fight(hero, camp, "detected")
            return self._combat_view(hero, self.store.get("combat", hero.id), notice=notice)
        camp["scouted"].append(hero.id)
        self._ecamp_save(camp)
        x, y = camp["x"], camp["y"]
        key = f"{x}:{y}"
        before = self._known_resources(hero, x, y)
        hero.exploration[key] = min(100, self._explored_pct(hero, x, y) + int(cfg["explore_points"]))
        if key not in hero.explored:
            hero.explored.append(key)
        lines = [t.t("ecamp.infiltrated", pct=hero.exploration[key])]
        new = [r for r in self._known_resources(hero, x, y) if r not in before]
        if new:
            lines.append(t.t("explore.revealed", items=", ".join(self._item_label(r) for r in new)))
        lines += self._ecamp_intel_lines(camp)
        lines.append(t.t("ecamp.infiltrate_xp", name=self._prof_name(ecfg["profession"]), xp=int(cfg["explorer_xp"])))
        lines += self._prof_gain(hero, ecfg["profession"], int(cfg["explorer_xp"]))
        lines += self._story_event(hero, "infiltrate", x=x, y=y, level=camp["level"])     # D-117 hook
        actions = [Action(id="assault", label=t.t("ecamp.assault_button", energy=self._ecamp_cfg()["fight_energy"])),
                   Action(id="explore_menu", label=t.t("menu.back"))]
        return View(kind="ecamp_intel", title=t.t("ecamp.intel_title"), body=lines + ["", self._status_line(hero)], actions=actions)

    def _ecamp_fight_done(self, hero: Hero, state: dict[str, Any]) -> list[str]:
        """Count a finished garrison fight on its camp (for everyone): a guard beaten, or the chief and the camp down.

        [ES]
        Qué hace: al terminar una pelea del campamento enemigo la cuenta para todos: ganar contra un guardia suma uno a
        "beaten" (nunca pasa de los guardias: el jefe solo cae en su propia pelea, aunque dos peleen a la vez); ganar
        contra el jefe destruye el campamento (_ecamp_destroyed: cofre y premios). Ganar o perder te anota como alguien
        que peleó ahí hoy (huir no). Si el campamento ya había caído, la pelea no cuenta para él (lo ganado es tuyo).
        Marca state["ecamp_again"] para ofrecer ⚔️ Seguir asaltando. La llama: _end_combat.
        Si cambia, afecta: la guarnición compartida y quién cobra al caer el jefe (tests/test_enemy_camps.py).
        """
        t = self.texts
        ref = state["enemy_camp"]
        camp = self._ecamp(ref["x"], ref["y"], ref["day"])
        if camp is None:
            return ["", t.t("ecamp.gone")]
        if camp["destroyed"]:
            return ["", t.t("ecamp.late", name=camp["destroyed"].get("name", "?"))]
        outcome = state["outcome"]
        if outcome in ("victory", "defeat"):
            camp["fighters"][hero.id] = camp["fighters"].get(hero.id, 0) + 1
        lines = [""]
        last = len(camp["garrison"]) - 1
        if outcome == "victory" and ref.get("chief"):
            camp["destroyed"] = {"by": hero.id, "name": hero.name, "at": self.clock.now()}
            self._ecamp_save(camp)
            return lines + self._ecamp_destroyed(hero, camp)
        if outcome == "victory":
            if camp["beaten"] < last:
                camp["beaten"] += 1
                lines.append(t.t("ecamp.guard_down", n=camp["beaten"]))
                if camp["beaten"] >= last:
                    lines.append(t.t("ecamp.chief_next"))
                elif self._ecamp_intel(hero, camp):
                    lines.append(t.t("ecamp.left", n=self._ecamp_left(camp)))
            else:
                lines.append(t.t("ecamp.no_guards_left"))
            state["ecamp_again"] = True
        else:
            lines.append(t.t("ecamp.still_standing", n=camp["beaten"]))
        self._ecamp_save(camp)
        return lines

    def _ecamp_destroyed(self, hero: Hero, camp: dict[str, Any]) -> list[str]:
        """The chief fell: the chest for the finisher and a share for everyone else who fought there that day (once).

        [ES]
        Qué hace: paga la caída del campamento enemigo, una sola vez (el que llega tarde ve "ya cayó"). Quien lo termina
        se lleva el cofre: monedas, materiales de la zona, experiencia y la probabilidad de una pieza de equipo del nivel
        del campamento (el sorteo de botín de siempre, roll_gear). Cada otro que peleó ahí ese día (ganó o perdió) gana
        enemy_camps.share (monedas y experiencia), aunque no esté jugando, y le llega un aviso. Anota el hecho en el
        📔 Diario (gancho _story_event "enemy_camp"). D-141: la 🎓 especialización 🐾 Rastreador del Explorador suma monedas
        al cofre y a la parte de quien la tiene.
        La llama: _ecamp_fight_done. Si cambia, afecta: cuántas monedas y equipo entran al juego por campamento.
        """
        t = self.texts
        cfg = self._ecamp_cfg()
        x, y = camp["x"], camp["y"]
        name = self._zone_name(self._zone(x, y))
        chest = self._ecamp_chest(camp)
        chest["coins"] = int(round(chest["coins"] * (1 + self._pspec_bonus(hero, "coins", sale="ecamp"))))   # D-141: 🐾 Rastreador
        hero.gold += chest["coins"]
        for item_id, count in chest["items"].items():
            self._bag_add(hero, item_id, count)               # a find: never lost (D-90)
        xp = self._zone_xp(cfg["chest"]["xp"], camp["level"])
        items = [self._money(chest["coins"])] + ([self._item_list(chest["items"])] if chest["items"] else [])
        lines = [t.t("ecamp.destroyed", name=name), t.t("ecamp.chest", items=" · ".join(items), xp=int(xp * self._xp_mult(hero)))]
        rng = Rng(int(hash_unit(self.world_seed, hero.id, "enemy_camp_gear", camp["day"], x, y) * 2**31))
        dropped = roll_gear(self.content.items, self.content.classes, self.content.balance, hero, chest["gear_level"], rng,
                            chance=chest["gear_chance"])
        if dropped:
            hero.backpack[dropped] = hero.backpack.get(dropped, 0) + 1
            lines.append(self._loot_line(hero, dropped))
        lines += self._give_xp(hero, xp)
        coins = int(camp["level"] * cfg["share"]["coins_per_level"])
        share_xp = self._zone_xp(cfg["share"]["xp"], camp["level"])
        others = [hid for hid in camp["fighters"] if hid != hero.id]
        for hid in others:
            target = self._load(hid)
            if target is None:
                continue
            their_coins = int(round(coins * (1 + self._pspec_bonus(target, "coins", sale="ecamp"))))   # D-141: 🐾 Rastreador
            target.gold += their_coins
            more = self._give_xp(target, share_xp)
            self._journal(target, "enemy_camp", x=x, y=y, f=0)
            self._save(target)
            self._push(hid, View(kind="ecamp_news", title=t.t("ecamp.news_title"),
                                 body=[t.t("ecamp.news_body", hero=hero.name, name=name, x=x, y=y),
                                       t.t("ecamp.share", gold=self._money(their_coins), xp=int(share_xp * self._xp_mult(target)))] + more))
        if others:
            lines.append(t.t("ecamp.shared", n=len(others), gold=self._money(coins)))
        lines += self._story_event(hero, "enemy_camp", x=x, y=y, level=camp["level"], destroyed=True)     # D-117: 📔 Diario
        return lines

    def _ecamp_again(self, hero: Hero, state: dict[str, Any]) -> list[Action]:
        """⚔️ Seguir asaltando after a won guard fight: the camp still stands here and you can pay another fight."""
        ref = state.get("enemy_camp") or {}
        if not state.get("ecamp_again") or (hero.x, hero.y) != (ref.get("x"), ref.get("y")) or hero.downed:
            return []
        cost = int(self._ecamp_cfg()["fight_energy"])
        if hero.energy < cost or not self._ecamp_standing(hero.x, hero.y):
            return []
        return [Action(id="assault", label=self.texts.t("ecamp.again_button", energy=cost))]

    def _ecamp_map_lines(self, hero: Hero, seen: list[dict[str, Any]]) -> list[str]:
        """🗺️ Mapa lines: the legend and the nearest camps (⏱️ time from 🧭 rank 10, 👹 strength from 75), how far you see,
        and from rank 10 the time to the Guardian's lair and to your camp."""
        t = self.texts
        cfg = self._explorer_cfg()
        travel = self._explorer_has(hero, "travel")
        lines: list[str] = []
        if seen:
            lines.append(t.t("ecamp.map_legend"))
            for camp in seen[:int(cfg["map_lines"])]:
                x, y = camp["x"], camp["y"]
                text = t.t("ecamp.map_line", x=x, y=y, zones=abs(x - hero.x) + abs(y - hero.y))
                if travel:
                    text += t.t("explorer.map_time", time=self._fmt_duration(self._trip_seconds(hero, x, y)))
                if self._ecamp_intel(hero, camp):
                    text += t.t("ecamp.map_strength", left=self._ecamp_left(camp), level=camp["level"],
                                chief=self._ecamp_enemy_name(camp["garrison"][-1]))
                lines.append(text)
            if len(seen) > int(cfg["map_lines"]):
                lines.append(t.t("ecamp.map_more", n=len(seen) - int(cfg["map_lines"])))
        rank = self._explorer_rank(hero)
        later = [int(cfg["ranks"][k]) for k in ("camps_near", "camps_all") if int(cfg["ranks"][k]) > rank]
        sight = self._ecamp_sight(hero)
        lines.append(t.t("ecamp.map_sight_next", n=sight, rank=later[0]) if later else t.t("ecamp.map_sight_all"))
        if travel:
            guardian = self._guardian_cfg()
            if guardian and self._discovered(guardian["x"], guardian["y"]) is not None \
                    and (hero.x, hero.y) != (guardian["x"], guardian["y"]):
                lines.append(t.t("explorer.time_lair", time=self._fmt_duration(self._trip_seconds(hero, guardian["x"], guardian["y"]))))
            camp = self.store.get("camp", hero.camp) if hero.camp else None
            if camp and (hero.x, hero.y) != (camp["x"], camp["y"]):
                lines.append(t.t("explorer.time_camp", name=camp["name"],
                                 time=self._fmt_duration(self._trip_seconds(hero, camp["x"], camp["y"]))))
        return lines

    # ------------------------------------------------------------------ ⚙️ Opciones and automatic fights (D-114)

    def _auto_cfg(self) -> dict[str, Any]:
        return self.content.balance["auto_fight"]

    def _option(self, hero: Hero, key: str) -> Any:
        """One of the player's ⚙️ Opciones: what the hero saved, else balance auto_fight.defaults (also for old heroes).

        [ES]
        Qué hace: lee una opción del jugador ("fights": "manual" o "auto"; "retreat": % de vida; "potions": sí/no). Si el
        héroe nunca la cambió (o lo guardado ya no vale), da la de balance.yaml auto_fight.defaults: ✋ Manual, 50 %, sí.
        La llaman: todo lo de esta sección, _hunt_view, _hunt y _hunt_batch_blocker.
        Si cambia, afecta: qué pasa con las peleas de los lotes de todos los jugadores.
        """
        cfg = self._auto_cfg()
        default = cfg["defaults"][key]
        value = (hero.options or {}).get(key, default)
        if key == "fights" and value not in ("manual", "auto"):
            return default
        if key == "retreat" and value not in cfg["retreat_choices"]:
            return default
        if key == "potions":
            return bool(value)
        return value

    def _auto_on(self, hero: Hero) -> bool:
        """True if the hero chose ⚔️ automatic fights in batches (D-114)."""
        return self._option(hero, "fights") == "auto"

    def _below_retreat(self, hero: Hero) -> bool:
        """True if the hero's life is under its 🩹 Retirarse limit (⚙️ Opciones): automatic fights stop there (D-114)."""
        max_hp = hero_stats(self._kit(hero), hero.level)["max_hp"]
        return hero.hp * 100 < self._option(hero, "retreat") * max_hp

    def _options_view(self, hero: Hero, notice: str | None = None) -> View:
        """⚙️ Opciones: what happens and what does not (D-114). 3 options, one button each, plus ↩️ Volver (4 at most).

        [ES]
        Qué hace: la pantalla ⚙️ Opciones (menú de abajo y /opciones). Explica cada opción con su valor de ahora y tiene un
        botón por opción que la cambia: ⚔️ Peleas en un lote (✋ Manual / ⚔️ Automática), 🩹 Retirarse con menos de
        (30 / 50 / 70 % de vida, auto_fight.retreat_choices) y 🧪 Pociones en peleas automáticas (sí / no); más ↩️ Volver.
        Se puede abrir mientras exploras, recolectas o cazas (la opción vale desde la próxima pelea), no en combate.
        La llaman: el botón ⚙️ Opciones del menú fijo, /opciones y _set_option.
        Si cambia, afecta: tests/test_options.py y el tope de 4 botones (D-75). Una opción nueva pide página o ciclo.
        """
        t = self.texts
        auto = self._auto_on(hero)
        pct = self._option(hero, "retreat")
        potions = self._option(hero, "potions")
        yes_no = t.t("options.value_yes" if potions else "options.value_no")
        body = [t.t("options.intro"), "",
                t.t("options.fights_auto" if auto else "options.fights_manual"),
                t.t("options.retreat", pct=pct),
                t.t("options.potions_on" if potions else "options.potions_off"),
                "", t.t("options.never_auto")]
        actions = [Action(id="opt:fights", label=t.t("options.fights_button", value=t.t("options.auto" if auto else "options.manual"))),
                   Action(id="opt:retreat", label=t.t("options.retreat_button", pct=pct)),
                   Action(id="opt:potions", label=t.t("options.potions_button", value=yes_no)),
                   Action(id="home", label=t.t("menu.back"))]
        return View(kind="options", title=t.t("options.title"), body=body, actions=actions, notice=notice)

    def _set_option(self, hero: Hero, key: str) -> View:
        """Change one option ("opt:fights" toggles, "opt:retreat" cycles 30 → 50 → 70, "opt:potions" toggles); saved now.

        [ES]
        Qué hace: cambia una opción con su botón y la guarda en Hero.options: ✋/⚔️ se alterna, el % de 🩹 Retirarse va
        pasando por auto_fight.retreat_choices y 🧪 Pociones se alterna. Vuelve a ⚙️ Opciones con el aviso de lo guardado.
        La llaman: los botones "opt:" de _options_view. Si cambia, afecta: lo que se guarda de cada jugador.
        """
        t = self.texts
        if key == "fights":
            hero.options["fights"] = "manual" if self._auto_on(hero) else "auto"
            notice = t.t("options.saved_auto" if self._auto_on(hero) else "options.saved_manual")
        elif key == "retreat":
            choices = list(self._auto_cfg()["retreat_choices"])
            hero.options["retreat"] = choices[(choices.index(self._option(hero, "retreat")) + 1) % len(choices)]
            notice = t.t("options.saved_retreat", pct=hero.options["retreat"])
        elif key == "potions":
            hero.options["potions"] = not self._option(hero, "potions")
            notice = t.t("options.saved_potions_on" if hero.options["potions"] else "options.saved_potions_off")
        else:
            return self._options_view(hero)
        return self._options_view(hero, notice=notice)

    def _auto_lines(self, hero: Hero, kind: str | None = None) -> list[str]:
        """The batch screens' line: what happens if a fight comes up, as ⚙️ Opciones says (D-114); a hunt only says the limits."""
        t = self.texts
        if not self._auto_on(hero):
            return [t.t("auto.batch_manual")]
        yes_no = t.t("options.value_yes" if self._option(hero, "potions") else "options.value_no")
        key = "auto.batch_hunt" if kind == "hunt" else "auto.batch_auto"
        return [t.t(key, pct=self._option(hero, "retreat"), potions=yes_no)]

    def _batch_fight(self, hero: Hero, activity: dict[str, Any], notice: str) -> list[str] | None:
        """A fight came up in a batch step (D-114): returns the batch's end lines, or None if the batch goes on.

        [ES]
        Qué hace: decide qué pasa con una pelea que sale en un lote (🔎 explorar, 🪓 recolectar o 🏹 cazar en lote).
        Con ✋ Manual, o si la pelea no es un encuentro común (Guardián, defensa del campamento, campamento enemigo de D-112:
        nunca van solas), el lote
        se corta y la pelea te espera, como siempre. Con ⚔️ Automática el héroe la pelea ya (_auto_combat): si gana y su vida
        no quedó bajo el límite de 🩹 Retirarse, el lote sigue (devuelve None); si pierde, la deja o queda bajo el límite,
        el lote se corta con su motivo. Si la pelea sale con la vida ya bajo el límite, no pelea solo: el lote se corta y la
        pelea te espera.
        La llama: _settle (una vez por pelea, también con el chat cerrado: el aviso sale una sola vez, al final del lote).
        Si cambia, afecta: todos los lotes con peleas (tests/test_options.py).
        """
        state = self.store.get("combat", hero.id)
        edef = self.content.enemies.get(state["enemy"]["id"], {}) if state else {}
        # never alone: the Guardian, camp defences and enemy camps (D-112: their fights are always by hand)
        if state is None or not self._auto_on(hero) or edef.get("boss") or state.get("raid") or state.get("enemy_camp"):
            return self._batch_summary(hero, activity, "fight") + [notice]
        pct = self._option(hero, "retreat")
        if self._below_retreat(hero):
            return self._batch_summary(hero, activity, "auto_wait", pct=pct) + [notice]
        outcome = self._auto_combat(hero, state, activity)
        if outcome == "defeat":
            return self._batch_summary(hero, activity, "auto_defeat", enemy=self.texts.t(edef["name_key"]),
                                       level=state["enemy"]["level"], gold=self._money(activity.get("gold_lost", 0)))
        if outcome != "victory":
            return self._batch_summary(hero, activity, "auto_fled")
        if self._below_retreat(hero):
            return self._batch_summary(hero, activity, "auto_low_hp", pct=pct)
        return None

    def _auto_combat(self, hero: Hero, state: dict[str, Any], activity: dict[str, Any]) -> str:
        """Fight the open fight alone now and close it as any fight (_end_combat); tally it in the batch. Returns the outcome.

        [ES]
        Qué hace: juega la pelea entera con la forma de jugar básica pero atenta del motor (engine/combat/auto.py play_out:
        las mismas reglas y el mismo sorteo que a mano; 🧪 Pociones según ⚙️ Opciones) y la cierra con _end_combat, como
        una pelea a mano: experiencia, monedas, botín, equipo, gremio, partida de caza, 🔪 Desollador, derrota (malherido y
        monedas perdidas) y cinturón. Suma al lote cuántas ganó, perdió o dejó, lo que dieron y el botín, y anota las subidas
        de nivel y de rango de oficio para el resumen. Publica HitReceived por cada golpe recibido.
        La llama: _batch_fight. Si cambia, afecta: las recompensas de las peleas automáticas (tienen que ser las de a mano).
        """
        t = self.texts
        level, xp, gold = hero.level, hero.xp, hero.gold
        bag, profs = dict(hero.backpack), dict(hero.professions)
        play_out(state, hero, self._kit(hero), self.ctx, use_items=self._option(hero, "potions"),
                 on_hit=lambda dmg: self.bus.publish(HitReceived(hero.id, dmg, False)))
        self._end_combat(hero, state)
        outcome = state["outcome"]
        ups = {t.t("combat.level_up", level=n) for n in range(level + 1, hero.level + 1)} | {t.t("talents.new_point")}
        activity["log"] += [line for line in state.get("story", []) if line not in ups]    # D-117 (level-ups come below)
        fights = activity.setdefault("fights", {})
        key = {"victory": "won", "defeat": "lost"}.get(outcome, "fled")
        fights[key] = fights.get(key, 0) + 1
        activity["fight_xp"] = activity.get("fight_xp", 0) + max(0, hero.xp - xp)
        if hero.gold >= gold:
            activity["fight_gold"] = activity.get("fight_gold", 0) + hero.gold - gold
        else:
            activity["gold_lost"] = activity.get("gold_lost", 0) + gold - hero.gold
        loot = activity.setdefault("loot", {})
        for item_id, count in hero.backpack.items():
            extra = count - bag.get(item_id, 0)
            if extra > 0:
                loot[item_id] = loot.get(item_id, 0) + extra
        cfg = self._prof_cfg()
        trade = activity.setdefault("fight_trade", {})
        for pid, now in hero.professions.items():
            if now > profs.get(pid, 0):
                trade[pid] = trade.get(pid, 0) + now - profs.get(pid, 0)
                rank = self._prof_rank(hero, pid)
                if rank > rank_of(profs.get(pid, 0), cfg["rank_formula"], cfg["max_rank"]):
                    activity["log"].append(t.t("prof.rank_up", name=self._prof_name(pid), rank=rank, title=self._rank_title(rank)))
        for new_level in range(level + 1, hero.level + 1):
            activity["log"] += [t.t("combat.level_up", level=new_level), t.t("talents.new_point")]
        if state.get("better") and self._is_better(hero, state["better"]):     # D-115: ⬆️ said once in the batch summary
            line = t.t("gear.better_batch", item=self._gear_name(state["better"]))
            if line not in activity["log"]:
                activity["log"].append(line)
        return outcome

    def _auto_summary(self, activity: dict[str, Any]) -> list[str]:
        """The batch summary's fight lines: "⚔️ 3 peleas automáticas: 3 ganadas", what they gave and their loot (D-114)."""
        fights = activity.get("fights") or {}
        total = sum(fights.values())
        if not total:
            return []
        t = self.texts
        parts = [t.t(f"auto.{key}", n=fights[key]) for key in ("won", "lost", "fled") if fights.get(key)]
        lines = [t.t("auto.summary", n=total, result=", ".join(parts))]
        if activity.get("fight_xp") or activity.get("fight_gold"):
            lines.append(t.t("auto.rewards", xp=activity.get("fight_xp", 0), gold=self._money(activity.get("fight_gold", 0))))
        if activity.get("loot"):
            lines.append(t.t("auto.loot", items=self._item_list(activity["loot"])))
        if activity.get("fight_trade"):
            lines.append(self._trade_summary(activity["fight_trade"]))
        return lines

    # ------------------------------------------------------------------ combat

    def _zone_enemies(self, zone: Zone) -> list[tuple[str, dict[str, Any]]]:
        """Enemies that can show up in a zone: its biome and level; if none fit, the closest band of its biome (D-108).

        [ES] Qué hace: los enemigos que salen en una zona (nunca jefes ni retirados). La llaman: _start_combat (encuentros,
        emboscadas y cacería) y la pantalla 🏹 Cazar (🐾 Por aquí rondan). Si cambia, afecta: qué enemigos salen en todo el mapa.
        """
        return encounter_pool(self.content.enemies, zone.biome, zone.level)     # D-108: the biome's band, or the closest one

    def _start_combat(self, hero: Hero, zone: Zone, rng: Rng, reason_key: str, mark: dict[str, Any] | None = None) -> str:
        """Start a fight against a common enemy of the zone; `mark` adds keys to the fight state (a hunt, D-106)."""
        pool = self._zone_enemies(zone)
        enemy_id, enemy_def = pool[int(rng.random() * len(pool)) % len(pool)]
        level = clamp_level(enemy_def, zone.level + (1 if rng.chance(0.3) else 0))
        seed = int(rng.random() * 2**31)
        state = make_combat(enemy_id, enemy_def, level, self._kit(hero), seed)
        if mark:
            state.update(mark)
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
            *([t.t("ecamp.chief_badge")] if (state.get("enemy_camp") or {}).get("chief") else []),     # D-112: the camp's chief
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
        bag_before = dict(hero.backpack)                # D-115: to tell a ⬆️ better piece that came in this fight
        # D-106: a hunt won while your camp's hunting party lasts in that zone gets the group bonus (0 otherwise)
        party = self._hunt_party_of_fight(hero, state) if outcome == "victory" else None
        bonus = self._hunt_bonus(hero, party) if party else 0.0
        if outcome == "victory" and edef.get("boss"):
            lines += self._guardian_rewards(hero, state, rng)
            if self._has_memento(hero):
                actions.insert(0, Action(id="memento", label=t.t("guardian.memento_button")))
        elif outcome == "victory":
            xp = int(self._zone_xp(edef["xp"], enemy["level"]) * self._xp_mult(hero) * (1 + bonus))   # D-106: party bonus
            low, high = edef.get("gold", [1, 3])
            gold = int(rng.uniform(low, high + 1) * (1 + 0.1 * (enemy["level"] - 1)))
            hero.xp += xp
            hero.gold += gold
            hero.kills += 1
            lines += self._tutorial(hero, "win_fight")
            lines.append(t.t("combat.rewards", xp=xp, gold=self._money(gold)))
            for item_id, chance in edef.get("loot", {}).items():
                chance += self._camp_tech_bonus(hero, hero.x, hero.y, "loot_bonus", item_id) if hero.camp else 0.0   # D-101: Rastreo
                if item_id in self.content.items and rng.chance(min(1.0, chance * (1 + bonus))):
                    item = self.content.items[item_id]
                    low, high = item.get("loot_amount", [1, 1])      # D-93: 🍖 carne comes in 1-2
                    count = low if high <= low else min(high, int(rng.uniform(low, high + 1)))
                    hero.backpack[item_id] = hero.backpack.get(item_id, 0) + count
                    count += self._trade_loot(hero, item_id, count, lines, state["seed"])     # D-109: 🔪 Desollador (carne, piel)
                    label = f"{item['emoji']} {t.t(item['name_key'])}" if count == 1 else self._item_list({item_id: count})
                    lines.append(t.t("combat.loot", item=label))
            drop = drop_chance_for(self.content.balance, enemy["level"]) * (1 + bonus) if bonus else None    # D-106: party bonus (D-113: less from level 10)
            dropped = roll_gear(self.content.items, self.content.classes, self.content.balance, hero, enemy["level"], rng, chance=drop)
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
            # D-117: a won fight moves missions and tasks (the zone's biome; a hunt; the Guardian); automatic fights read
            # state["story"] to put these lines in the batch summary (_auto_combat)
            state["story"] = self._story_event(hero, "win", enemy=enemy["id"], biome=self._zone(hero.x, hero.y).biome,
                                               level=enemy["level"], hunt=bool(state.get("hunt")), boss=bool(edef.get("boss")))
            lines += state["story"]
        elif outcome == "defeat":
            lost = int(hero.gold * hb["defeat_gold_loss"])
            hero.gold -= lost
            hero.hp = 1
            hero.downed = True                 # D-83: falling means a long recovery
            self.bus.publish(HeroDowned(hero.id))
            lines.append(t.t("combat.defeat_consequence", gold=self._money(lost)))
        if state.get("raid"):                  # D-99: a defender's fight counts for the camp's raid
            lines += self._raid_fight_done(hero, state)
        if party:                              # D-106: one more prey for the party's shared tally
            lines += self._hunt_fight_done(hero, party, bonus)
        if state.get("enemy_camp"):            # D-112: a fight of an enemy camp's garrison counts for everyone
            lines += self._ecamp_fight_done(hero, state)
        refilled = self._refill_belt(hero)
        if refilled:
            lines.append(t.t("combat.belt_refilled"))
        hero.last_regen_at = self.clock.now()
        self.store.delete("combat", hero.id)
        if outcome == "victory" and state.get("hunt"):
            actions = self._hunt_end_actions(hero) + actions     # D-106: 🏹 Otra presa (and the party) before ▶️ Continuar
        actions = self._ecamp_again(hero, state) + actions         # D-112: ⚔️ Seguir asaltando
        better = self._better_piece(hero, bag_before)              # D-115: ⬆️ a piece from this fight beats what you wear
        if better:
            state["better"] = better                               # automatic fights put the line in the batch summary
            lines.append(self._better_line(hero, better))
            if len(actions) < 4:                                   # 4 buttons at most (D-75): 🔁 Equipar first
                actions.insert(0, self._better_action(better))
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
