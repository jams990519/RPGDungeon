"""Guild from the first moment (D-269), 👥 Jugadores at the bonfire (D-265) and camp works that take time: a GameService mixin.

A hero can create a guild before having a camp (🥉20, a free name, 5 members). Others ask to join and the leader or an
officer accepts (or the leader invites from a player's card). The guild shows where each member is and what they do,
carries 📢 messages to every member, keeps a fund that every member fills from wherever they are, and has a 📍 meeting
point. The leader founds the camp where he stands with at least 2 members present: the fund pays, and the founding is a
work in progress that advances with the members present (1 h with 2, 30 min with 4, never under 10 min). When it ends, the
camp is created with the guild's name, the guild becomes the camp's guild (the D-97 record) and every other member is
invited. Every camp improvement whose materials are complete is also a work in progress (60 min x its level x 2 / members
present in the camp's territory). Works advance lazily: on every order of a member and in tick() when one is due.

[ES]
Para qué sirve: el gremio desde el primer momento (D-269, reemplaza a D-252), la pantalla 👥 Jugadores de la fogata (D-265 y
    D-274.1-2), el botón 🏗️ Moverte a la construcción de 📍 Zona (pedido del dueño, 18-oct) y las obras que tardan (D-269.4,
    D-274.4). Las reglas chicas que no dijo el dueño (salir, el fondo, presentes, obras a la vez...) están en D-276 (provisional). Es parte de GameService (una "mezcla", como StoryMixin y GuideMixin), en su propio archivo para no agrandar game.py.
    0.39 (pedido del dueño, 19-oct-2026): los 🤝 ayudantes del fundador (D-289), la ⚔️ Armería del gremio (D-290), el gremio
    que después de fundar conserva sus herramientas: 💰 Depositar desde cualquier lugar, 📢 Mensaje, los miembros con su
    código y los mensajes de antes (D-291), y los del gremio que esperan lugar en el campamento lleno (D-294).
    D-302 (0.39.4, pedido del dueño del 20-oct-2026: menos texto en pantalla y "submenús con más información"): la pantalla del
    gremio (antes y después de fundar) deja arriba solo lo del gremio y pasa el resto a submenús: 👥 Miembros
    (_guild_members_view: los miembros con /m1, los 🤝 ayudantes, los ⏳ que esperan lugar, 🙋 Solicitudes), 💰 Fondos
    (_guild_funds_view: cada recurso con su código de 📦 Recursos, en orden por código, y 💰 Depositar) y 📢 Chat
    (_guild_chat_view: los mensajes del último día, como mucho gremio.chat_shown y gremio.chat_max_chars letras, y 📢 Mensaje).
    La ⚔️ Armería muestra su "0/30" solo en su pantalla.
    D-304 (0.41, pedido del dueño del 20-oct-2026: "dame la opción como dueño de gremio para agregar un asistente… que pueda
    definir hacia dónde va a avanzar el territorio junto contigo"): en los textos, los 🤝 ayudantes se llaman asistentes (los
    ids no cambian: "helpers", "ghelp:"); además de activar obras, invitar y responder solicitudes, eligen hacia dónde crece el
    territorio (game.py _grow_view/_grow_camp, con _camp_manager). En 👥 Miembros el fundador ve cuántos tiene y cómo nombrar
    uno (_helpers_founder_line).
    D-303 (0.41.1, orden del dueño: 🪵 madera en todas las zonas): como ahora casi toda zona tiene madera, el 🔎 buscador de
    recursos (_resource_search_view) pone primero las zonas cercanas Y ricas: a cada zona le suma a la distancia
    (1 - riqueza) × gremio.search_rich_penalty (4) zonas, así un bosque con madera al 100 % a 3 zonas sale antes que una
    montaña con madera al 30 % a 1 zona. La distancia que se muestra es la de verdad.
    D-322 (0.47, pedido del dueño del 21-oct-2026: "que los jugadores del gremio puedan primero construir las estructuras y
    después poder utilizar los recursos para las profesiones de cada uno"): el 💰 fondo del campamento sigue alimentando primero
    las obras activas y ⏫ Siguiente nivel (lo que les falta queda guardado: _fund_reserve); lo que sobra (_fund_surplus) un
    miembro lo usa al refinar y fabricar en las estaciones de SU campamento, como si lo llevara en la mochila (primero la
    mochila, después el fondo: game.py _station_view, _recipe_view y _make con _fund_pool y _fund_take), con un tope por día
    real (fund_crafts.daily_cap), 📜 Quién usó qué (_fund_log_view) y un interruptor 🔓/🔒 del fundador o un 🤝 asistente en
    💰 Fondos (_fund_craft_toggle). Las reglas chicas las eligió Claude (D-322, provisional).
    D-327 (0.51, la escalera del asentamiento, D-253): los 🤝 asistentes son los oficiales de D-253.4 ("aceptan gente el líder
    y los oficiales"): una sola lista ("helpers"), con el tope de D-289 (1 cada 5 miembros); antes de fundar, los oficiales del
    gremio siguen como siempre y al fundar pasan a asistentes. El cupo del campamento es el de su etapa (game.py _members_cap,
    ladder.py) y quien no juega 30 días sale solo (ladder.py _idle_tick): 👥 Miembros lo dice (_idle_line) y marca con 💤 a
    quien ya fue avisado (_camp_member_line).
    D-331 (0.55, las 🪖 escuadras de 5, D-253.1 Forma B): 👥 Miembros del campamento suma la línea de tu escuadra y el botón
    🪖 Escuadras, y la tarjeta de un miembro su escuadra con 🗳️ Votar como jefe y 🔀 Cambiar de escuadra. Las reglas viven en
    engine/service/squads.py; aquí solo están los ganchos (_camp_members_view y _camp_member_view).
    D-336 (0.60, la 💀 muerte permanente, D-147): quien la juró no crea un gremio (_gremio_new, _gremio_name) ni recibe el
    liderazgo (_gremio_lead), porque todavía no hay sucesión de fundador; al caer sale del gremio como un miembro
    (engine/service/permadeath.py _oath_unlink usa _gremio_leave_member). Su nombre lleva 💀 en la tarjeta (_player_card). Usa las
    ayudas de PermadeathMixin _oath_no_lead, _oath_account_on y _oath_mark.
Documento de diseño: diseno/09-construccion/escalera-del-asentamiento.md §0 (cómo está D-269 en el juego);
    diseno/01-plataforma/menus-campamento-y-heroe.md (👥 Jugadores en la fogata); diseno/08-social/gremios-y-social.md §0
Módulo: capa de servicios (M15 Social: el gremio; M14 Construcción: la fundación y las obras con tiempo)
Depende de: content/balance.yaml (bloques gremio, works, bonfire, presence, camps y guild), content/locales/es_gremio.yaml y
    en_gremio.yaml (textos), engine.social.guilds (contadores del gremio del campamento, D-97), engine.hero, engine.messaging y las
    ayudas de GameService (_zone, _zone_name, _money, _item_list, _bar, _fmt_duration, _seconds, _join, _ago, _banner,
    _emblem_name, _load, _save, _push, _push_each, _speaking, _name_key, _camp_requirements, _camp_here_view, _main_view,
    _guild_view, _members_cap, _upgrades, _upgrade_catalog, _upgrade_name, _create_camp, _territory, _trip_seconds, _zone_players;
    0.39: _active_works, _feed_works, _upgrade_need, _camp_perks, _credit_raw, _missing_text, _works_refresh, _camp_member_order,
    _gear_name, _enchant_mark, _forget_piece, _bag_room y _bag_no_room (D-338, 0.62: el tope del equipo suelto, de
    engine/service/backpack.py); 0.47 (D-322): _upgrades_here, _lvlup_need,
    _lvlup_progress, _camp_top_level, _recipes, _recipe_name y _today; 0.49 (D-325): _harvest_line, la línea de la 🌾 cosecha
    de la muralla en 💰 Fondos), content/balance.yaml fund_crafts y
    content/locales/es_fondo_oficios.yaml y en_fondo_oficios.yaml (los textos del fondo para oficios); 0.51 (D-327):
    _idle_line y _idle_warned_mark de engine/service/ladder.py (LadderMixin); 0.55 (D-331): _squads_members_line,
    _squad_card_lines y _squad_card_actions de engine/service/squads.py (SquadsMixin) y content/locales/es_escuadras.yaml y
    en_escuadras.yaml (el botón 🪖 Escuadras)
Lo usan: engine/service/game.py (GameService hereda de esta clase): act() (las respuestas "gans:", "ginv:", "gcamp:", "cinv:" antes del
    combate y _works_settle después de _settle), view() y text() (_works_settle; los códigos /j1 /p1, /g1, /m1, /f02 y /inv_<código>;
    _gremio_text desde _name_camp), tick() (_works_tick), _idle_action (GREMIO_ACTIONS, "found" → _start_founding),
    _guild_view (sin campamento abre _gremio_view), _camp_hub_lines y _camp_hub_actions (👥 Jugadores en la fogata),
    _camp_requirements (las condiciones del gremio para fundar), _camp_here_view (la fundación en curso), _zone_view y
    _activity_view (🏗️ Moverte a la construcción), _important_places y _can_goto (el punto de reunión y la construcción),
    _give_to_work, _open_works y _upgrades_view (las obras en curso y el fondo del campamento); 0.39: _camp_manager y
    _camp_managers (quién activa obras y recibe solicitudes: _give_to_work, _activate_work, _stop_work, _works_entries,
    _services_view, _service_type_view, _upgrades_view, _guild_view, _ask_join, _answer_join), _helpers_line,
    _camp_member_line, _member_camp y text() (/a1, /t1: _armory_in_code, _armory_out_code); D-302: _guild_view (los botones
    "gmembers", "gfunds" y "gchat" que abren _guild_members_view, _guild_funds_view y _guild_chat_view; _armory_line se quitó:
    la cuenta de la armería está solo en ⚔️ Armería). Usa también _resource_code de game.py (el código /07 de cada recurso).
    D-322 (0.47): game.py _station_view (_fund_pool, _fund_pool_lines; el estado ✅💰 lo arma _recipe_status), _recipe_view
    (_fund_pool, _fund_pool_lines, _fund_cap), _make (_fund_pool, _fund_take, _fund_cap) y _faq_values (_fund_faq_values);
    aquí, _guild_funds_view (_fund_craft_lines y los botones "gflog" y "gfcraft")
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño:
    "gremio" (clave el id del gremio, "g1", "g2"…; nunca se reutiliza): {"id", "name", "leader", "officers" [cuentas],
        "members" [cuentas, el líder primero], "requests" [quién pidió entrar], "invites" [a quién invitó el líder o un oficial],
        "created", "messages" [{"by", "id", "text", "at"}, los últimos gremio.messages_kept], "fund" {objeto: cantidad},
        "gave" {cuenta: {objeto: cantidad}} (quién dio qué, para siempre), "meet" [x, y] o None y "meet_by" (el 📍 punto de
        reunión), "founding" (la fundación en curso: {"x", "y", "need", "done", "at", "floor", "started", "paid"} o None),
        "camp" ("x:y" del campamento ya fundado) e "invited" [miembros que todavía no respondieron la invitación al campamento],
        "closed" (True si se disolvió: su nombre queda libre)}
    "gremio_of" (clave la cuenta): {"gremio": id}: a qué gremio pertenece (antes del campamento, o mientras espera responder
        la invitación). Después de fundar, el gremio de un miembro es el de su campamento (Hero.camp, D-97).
    "gremio_codes" (clave la cuenta): el orden de la última lista que vio con códigos ({"players", "guilds", "members"}): solo
        pantalla, como "places_shown".
    "works_open" (clave "found:<id>" o "build:<x:y>"): {"kind": "found" o "build", "ref", "eta"}: índice de las obras en curso,
        para que tick() solo mire las que ya podrían haber terminado.
    "meta"/"gremio_seq": {"n"}: el último número de gremio usado.
    Además: "guild_name" y "camp_name" guardan {"gremio": id} mientras el gremio no tiene campamento (el nombre queda
        reservado para los dos); el campamento guarda "gremio" (id) y el gremio D-97 del campamento también; "upgrades" guarda
        "building" {mejora: {"need", "done", "at", "floor", "by", "started"}} (obras en curso) y "fund" {objeto: cantidad} (lo
        que sobró del fondo al fundar: se usa primero al aportar a una obra).
    D-280 (0.36.1): "player_code" (clave el código de 8 cifras): {"account"}; "player_code_of" (clave la cuenta): {"code"}. El
        código de jugador nunca cambia. El campamento suma "invites" [cuentas que su fundador invitó con /inv_ y no respondieron].
    D-282 (0.38): lo que el gremio sabe de las zonas no se guarda aparte: sale de la "exploration" de cada compañero
        (_mates_knowledge) y "gremio_codes" suma "zones" (el orden de 🗺️ Zonas del gremio para /z1: solo pantalla).
    D-285 (0.38.1): el chat del gremio. Todo texto suelto de un miembro (_guild_chat, desde text()) va a todos: se guarda en
        "messages" del gremio o, ya con campamento, en "messages" del campamento (los últimos gremio.messages_kept).
    D-289 (0.39): el campamento suma "helpers" [cuentas]: los 🤝 ayudantes del fundador (tope máx(1, ⌈miembros ÷
        camps.helpers_per_members⌉)). Activan obras, invitan con /inv_ y responden solicitudes; no renombran, no nombran
        ayudantes ni crean el gremio D-97. Al fundar, los oficiales del gremio que entran al campamento quedan de ayudantes.
    D-290 (0.39): "armory" (la ⚔️ Armería del gremio; clave el id del gremio antes del campamento y la clave "x:y" del
        campamento después: al fundar se muda): {"items": [{"id", "item", "enchant", "sig", "by", "by_id", "at"}], "log":
        [{"k": "in" | "out", "who", "item", "at"}] (los últimos armory.log_kept), "seq"}. Cada pieza guarda su ✨ encantamiento
        y su ✒️ firma (los de Hero.gear_enchants y Hero.gear_signatures), así nada se pierde. D-333 (0.57): una pieza usada guarda
        también su 🔧 durabilidad ("wear": el registro de engine/hero/durability.py; sin "wear" = nueva): sale la copia más gastada
        de la mochila (take_worst) y vuelve con ella al tomarla (put_back). "gremio_codes" suma "arm_in" y
        "arm_out" (el orden de /a1 y /t1: solo pantalla).
    D-294 (0.39): del gremio sin ser del campamento. El campamento suma "waiting" [cuentas que esperan lugar: tienen lo del
        gremio, nada del campamento; tope gremio.waiting_max], "wait_invites" [a quién invitaron al gremio con el campamento lleno,
        hasta que responde: "cwait:"] y "room_told" (cuántos lugares libres se avisaron la última vez). "camp_wait" (clave la
        cuenta): {"camp": "x:y"}: en qué campamento espera (lo lee _waiting_key). Quien espera NO está en "members" ni tiene
        Hero.camp: cupo, presencia, obras, oleadas, despensa, territorio y castillo no lo cuentan. Lo une el fundador o un
        ayudante (_camp_join_waiting), nunca solo. Para sumar reglas de "del gremio, no del campamento", usar _guild_camp.
    D-291 (0.39): después de fundar, 💰 Depositar y /f02 ponen en el fondo del campamento ("upgrades"."fund", quién dio qué en
        "upgrades"."gave") y el fondo alimenta las obras activas (game.py _feed_works); al fundar, los 📢 mensajes del gremio
        pasan a "messages" del campamento. Lo que se dio al fondo antes de fundar sigue en "gave" del gremio (se lee junto).
        D-325 (0.49): la 🌾 cosecha de la muralla (game.py _harvest_deliver) también pone en "upgrades"."fund" cada semana; no
        es de nadie, así que no va a "gave" (queda en "upgrades"."harvest"."total").
    D-322 (0.47): "upgrades" suma "fund_crafts" (True/False: el fondo para oficios 🔓 abierto o 🔒 cerrado; sin el campo,
        fund_crafts.default_open), "fund_used" ({"day": _today(), "by": {cuenta: unidades}}: lo que cada miembro tomó hoy para
        sus oficios; un día nuevo empieza de cero) y "fund_log" ([{"k": "use" | "open" | "close", "who", "id", "at", y en "use"
        "items" {material: n}, "recipe", "times"}], los últimos fund_crafts.log_kept: 📜 Quién usó qué).
Reglas que nunca se rompen:
    1. Un gremio por héroe: quien es miembro de un campamento tiene el gremio de su campamento (D-97) y no entra a otro.
    2. Antes del campamento caben gremio.members_before_camp (5); entra quien pide y acepta el líder o un oficial (o quien
       acepta la invitación del líder o un oficial). Nadie entra a la fuerza.
    3. Lo depositado en el fondo es del gremio: no vuelve a quien lo dio (queda anotado en "gave"); si el último miembro
       disuelve el gremio, el fondo vuelve entero a su mochila. Nada se pierde.
    4. Una obra (fundar o una mejora) avanza solo con miembros presentes (D-274.6: en la zona, o en el territorio para las
       mejoras, jugaron en los últimos presence.minutes o exploran, recolectan, cazan o duermen ahí): tiempo = minutos ×
       referencia ÷ presentes, nunca menos del piso; con nadie, se pausa. Lo construido nunca se borra.
    5. Las mejoras que ya estaban construidas siguen construidas; los campamentos y gremios de antes siguen igual (D-64).
    6. Ningún texto visible se escribe aquí: todo sale de content/locales (es_gremio.yaml y en_gremio.yaml; desde la 0.39
       también es_servicios.yaml y en_servicios.yaml), y todo aviso a otro jugador se arma con _push_each (le llega en su
       idioma, D-250).
    7. La ⚔️ Armería nunca pierde una pieza (D-290): entra con su encantamiento y su firma, y sale igual; si quien la toma ya
       lleva una pieza igual con otro encantamiento o firma, no se la lleva (las copias de una pieza comparten esos datos).
       Si el gremio se disuelve, las piezas vuelven al último miembro.
    8. D-322: primero las obras. Lo que les falta a las obras activas y a ⏫ Siguiente nivel nunca se usa para oficios (la
       reserva se calcula cada vez); un miembro toma del fondo solo en las estaciones de su campamento, después de su mochila,
       sin pasar el tope del día, y cada unidad queda en 📜 Quién usó qué. Hacer una receta sigue siendo todo o nada.
Si cambias esto, revisa:
    - Números: balance.yaml gremio, works, bonfire.cap, presence.bonfire_seconds, camps.found_cost y guild.levels[0].capacity;
      desde la 0.39, camps.helpers_per_members (D-289), armory.slots y armory.log_kept (D-290) y gremio.waiting_max (D-294);
      desde la 0.39.4 (D-302), gremio.messages_kept (50), gremio.chat_hours, gremio.chat_shown y gremio.chat_max_chars;
      desde la 0.47 (D-322), fund_crafts.daily_cap (40), default_open, log_kept y log_shown
    - Servicio: engine/service/game.py (los ganchos de "Lo usan"); engine/service/guide.py (el paso "found" lee
      _camp_requirements y se completa con el evento "camp" que manda _create_camp)
    - Pantallas y botones: HUB_KINDS ("gremio" y "guild": hasta 8 botones; los submenús de D-302, "guild_members",
      "guild_funds" y "guild_chat", tienen 4 como máximo; desde la 0.55, D-331, "guild_members" del campamento suma
      🪖 Escuadras y la tarjeta del miembro 🗳️ y 🔀), el layout de 📍 Zona ([2, 2, 1, 1] o [2, 2, 1, 1, 1] con
      🏗️ Moverte a la construcción) y los ids de GREMIO_ACTIONS y GREMIO_ANSWERS (64 bytes como máximo en Telegram)
    - Mapa de impacto: diseno/01-plataforma/mapa-de-impacto.md (el gremio desde el inicio y las obras con tiempo; desde la
      0.55, M15 "Las escuadras" y C-35)
    - Pruebas: tests/test_gremio_desde_el_inicio.py; tests/test_camps.py (found_at funda por el gremio), tests/test_guilds.py,
      tests/test_camp_upgrades.py (las obras con tiempo), tests/test_menus_y_dudas.py (la fogata con 👥 Jugadores);
      0.39: tests/test_ayudantes.py, tests/test_armeria.py, tests/test_deposito_tras_fundar.py, tests/test_servicios_por_tipo.py,
      tests/test_espera_del_gremio.py; 0.39.4: tests/test_submenus_campamento_gremio.py (D-302) y tests/test_chat_del_gremio.py;
      0.47: tests/test_fondo_para_oficios.py (D-322); 0.55: tests/test_escuadras.py (D-331: 🪖 en 👥 Miembros y en la tarjeta)
"""

from __future__ import annotations

import re
import unicodedata
from typing import Any

from engine.core.rng import hash_unit
from engine.hero import Hero, durability
from engine.messaging import Action, View
from engine.social import guilds as guild_rules
from engine.world import mapgen                          # D-265: the 9 bonfires

# Typed codes of the guild screens. [ES] /j1 (o /p1 en inglés): la tarjeta de un jugador de 👥 Jugadores; /g1: un gremio de
# 🔎 Buscar gremio; /m1: un miembro de tu gremio; /f02: depositar en el fondo todo lo que llevas del recurso 02 (su código de
# 📦 Recursos, como /v02 al vender).
PLAYER_CODE_RE = re.compile(r"^/(?:j|p)_?(\d{1,2})(@\w+)?$")
GUILD_CODE_RE = re.compile(r"^/g_?(\d{1,2})(@\w+)?$")
MEMBER_CODE_RE = re.compile(r"^/m_?(\d{1,2})(@\w+)?$")
FUND_CODE_RE = re.compile(r"^/f(\d{1,3})(@\w+)?$")
# D-280: /inv_12345678 invites the player with that code (👤 Héroe) to your guild, or to your camp once founded. "/inv"
# alone is still 🎒 Mochila. [ES] /inv_ más el código de jugador: invitar al gremio (o al campamento ya fundado).
INVITE_CODE_RE = re.compile(r"^/inv_?(\d{4,16})(@\w+)?$")
# D-282: /z2 = the 2nd zone of the last 🗺️ Zonas del gremio list (lays out the road in 🔗 Moverte, like /ir x y).
ZONE_CODE_RE = re.compile(r"^/z_?(\d{1,2})(@\w+)?$")
# D-290: ⚔️ Armería: /a2 leaves the 2nd unworn piece of your list in the guild's armory; /t2 takes the 2nd piece of the armory.
# [ES] /a01 también vale (como /f02). La lista es la de la última pantalla ⚔️ Armería que viste.
ARMORY_IN_RE = re.compile(r"^/a_?(\d{1,2})(@\w+)?$")
ARMORY_OUT_RE = re.compile(r"^/t_?(\d{1,2})(@\w+)?$")
# Guild names follow the camp names (the camp takes the guild's name when it is founded). [ES] Igual que CAMP_NAME_RE.
GREMIO_NAME_RE = re.compile(r"^[^\W_][\w '\-]{2,23}$", re.UNICODE)
# Button ids (or prefixes) that _gremio_action routes (menus: they also work while busy). [ES] Si cambian, cambian los botones.
GREMIO_ACTIONS = ("players", "pcard:", "gnew", "glist", "gcard:", "greq:", "greqs", "ginvite:", "gmsg", "gchat_tggle", "gfund", "gmeet", "gzones",
                  "gmeetset", "gfound", "gfoundx", "gleave", "gmem:", "goff:", "glead:", "glead!:", "gkick:", "gkick!:",
                  "garm",        # D-290: ⚔️ Armería
                  "ghelp:",      # D-289: 🤝 Hacer ayudante / ✖️ Quitar ayudante (the founder, from a member's card)
                  "creqs",       # D-289: 🙋 Solicitudes to join the camp (the founder or a helper)
                  "cwjoin:",     # D-294: 🏕️ Unir al campamento a guild member who waits for room
                  "gwleave",     # D-294: 🚪 Salir del gremio while waiting for room ("gwleave!" confirms)
                  "gmembers", "gfunds", "gchat",   # D-302: 👥 Miembros, 💰 Fondos and 📢 Chat (the guild's submenus)
                  "gfcraft", "gflog")              # D-322: 🔓/🔒 the fund for the professions and 📜 Quién usó qué
# Answers that arrive as pushes: handled before the combat check, like "join:". [ES] Las respuestas que llegan como aviso.
GREMIO_ANSWERS = ("gans:", "ginv:", "gcamp:", "cinv:",   # D-280: "cinv:" = the camp's invitation by code
                  "cwait:")                              # D-294: the guild's invitation while its camp is full
EPS = 1e-6

def _guild_chat_toggle(self, hero: Hero) -> View:
    data = self.store.get("hero", hero.id) or {}
    enabled = not bool(data.get("chat_notifications", True))
    data["chat_notifications"] = enabled
    self.store.put("hero", hero.id, data)
    notice = self.texts.t("gremio.chat_notif_status", status="ON" if enabled else "OFF")
    return self._guild_chat_view(hero, notice=notice)

def _busy_kinds() -> tuple[str, ...]:
    """The activities that keep a hero present in its zone with the chat closed (game.PRESENT_BUSY, D-96)."""
    from engine.service.game import PRESENT_BUSY          # lazy: game.py imports this module
    return PRESENT_BUSY


def _hub_buttons() -> int:
    """game.HUB_BUTTONS (D-192: the hubs show up to 8 buttons, 2 per row)."""
    from engine.service.game import HUB_BUTTONS           # lazy: game.py imports this module
    return HUB_BUTTONS


def _plain(text: str) -> str:
    """Lower case, no accents: what a guild search compares."""
    norm = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in norm if not unicodedata.combining(ch)).casefold()


class GremioMixin:
    """Guild-from-the-start, bonfire players and timed works part of GameService (needs its store, texts and helpers).

    [ES]
    Qué es: la parte del gremio desde el inicio, de 👥 Jugadores y de las obras con tiempo, en su propio archivo.
    Quién la usa: GameService (hereda de aquí).
    Si cambia, afecta: la fogata, el gremio antes del campamento, cómo se funda un campamento y cuánto tardan sus mejoras.
    """

    # ------------------------------------------------------------------ data and links

    def _gremio_cfg(self) -> dict[str, Any]:
        return self.content.balance.get("gremio", {})

    def _gremio(self, gid: str | None) -> dict[str, Any] | None:
        return self.store.get("gremio", gid) if gid else None

    def _gremio_link(self, account: str) -> dict[str, Any] | None:
        """The guild record this account belongs to through "gremio_of" (before its camp, or waiting to answer it)."""
        link = self.store.get("gremio_of", account)
        record = self._gremio(link.get("gremio")) if link else None
        return record if record and not record.get("closed") else None

    def _my_gremio(self, hero: Hero) -> dict[str, Any] | None:
        """The hero's guild before it has a camp (None after founding: then its guild is its camp's, D-97)."""
        record = self._gremio_link(hero.id)
        return record if record and not record.get("camp") and hero.id in record.get("members", []) else None

    def _gremio_free(self, account: str, data: Hero | dict[str, Any] | None) -> bool:
        """True if this player can create or join a guild: no guild, no camp, not waiting for a camp's room (rule 1, D-294)."""
        if data is None:
            return False
        camp = data.camp if isinstance(data, Hero) else data.get("camp")
        return camp is None and self._gremio_link(account) is None and self._waiting_key(account) is None

    def _gremio_manager(self, record: dict[str, Any], account: str) -> bool:
        """The leader or an officer (they accept requests and invite, D-253)."""
        return account == record.get("leader") or account in record.get("officers", [])

    def _gremio_cap(self) -> int:
        return int(self._gremio_cfg().get("members_before_camp", 5))

    def _gremio_room(self, record: dict[str, Any]) -> bool:
        return len(record.get("members", [])) < self._gremio_cap()

    def _hero_data(self, account: str, actor: Hero | None) -> dict[str, Any] | None:
        """x, y, seen_at, activity, name, level, class_id and camp of a player: the actor's fresh copy, else the stored one."""
        if actor is not None and account == actor.id:
            return {"x": actor.x, "y": actor.y, "seen_at": actor.seen_at, "activity": actor.activity, "name": actor.name,
                    "level": actor.level, "class_id": actor.class_id, "camp": actor.camp}
        return self.store.get("hero", account)

    def _hero_name(self, account: str) -> str:
        return (self.store.get("hero", account) or {}).get("name", "?")

    def _guild_name_of(self, account: str, data: dict[str, Any] | None = None) -> str:
        """The name of a player's guild: its guild before the camp, or its camp's guild (D-97); "" if none."""
        record = self._gremio_link(account)
        if record:
            return record["name"]
        data = data if data is not None else self.store.get("hero", account)
        camp = (data or {}).get("camp") or self._waiting_key(account)     # D-294: waiting for room, already in the guild
        guild = self.store.get("guild", camp) if camp else None
        return guild["name"] if guild else ""

    def _codes(self, hero: Hero, kind: str, ids: list[str]) -> None:
        """Remember the order of a list with codes (/j1, /g1, /m1) so a code is what the player saw."""
        record = self.store.get("gremio_codes", hero.id) or {}
        record[kind] = ids
        self.store.put("gremio_codes", hero.id, record)

    def _code_target(self, hero: Hero, kind: str, n: int) -> str | None:
        shown = (self.store.get("gremio_codes", hero.id) or {}).get(kind, [])
        return shown[n - 1] if 1 <= n <= len(shown) else None

    def _class_label(self, data: dict[str, Any]) -> str:
        cid = data.get("class_id", "")
        group = self.content.classes.get(cid, {}).get("group", cid)
        return self.texts.t(f"class_group.{group}.name")

    # ------------------------------------------------------------------ presence and works that take time (D-269, D-274)

    def _presence_window(self, account: str, data: dict[str, Any] | None, zones: set[tuple[int, int]], start: float,
                         now: float, cache: dict[str, dict[str, Any]]) -> float:
        """Seconds this member counted as present in `zones` between `start` and `now` (D-274.6), from its stored record.

        [ES]
        Qué hace: estima cuánto estuvo presente un miembro entre la última revisión y ahora: desde que llegó a la zona (registro
        "presence") hasta ahora si explora, recolecta, caza o duerme ahí, o hasta 15 min (presence.minutes) después de su último
        botón. Viajando no cuenta. Usa la ficha guardada (lo que pasó en ese tiempo), nunca el botón de ahora.
        La llama: _advance_work. Si cambia, afecta: cuánto avanzan la fundación y las obras.
        """
        if not data:
            return 0.0
        pos = (data.get("x"), data.get("y"))
        if pos not in zones:
            return 0.0
        key = f"{pos[0]}:{pos[1]}"
        record = cache.setdefault(key, self.store.get("presence", key) or {})
        since = (record.get("seen") or {}).get(account)
        since = start if since is None else max(start, float(since))
        kind = (data.get("activity") or {}).get("kind")
        if kind == "travel":
            return 0.0
        if kind in _busy_kinds():
            until = now
        else:
            until = min(now, float(data.get("seen_at", 0.0)) + self._seconds(self.content.balance["presence"]["minutes"]))
        return max(0.0, until - since)

    def _present_now(self, members: list[str], zones: set[tuple[int, int]], actor: Hero | None) -> list[str]:
        """Members present in `zones` right now (D-274.6): there, and a button in presence.minutes or busy there."""
        cutoff = self.clock.now() - self._seconds(self.content.balance["presence"]["minutes"])
        out = []
        for account in members:
            data = self._hero_data(account, actor)
            if not data or (data.get("x"), data.get("y")) not in zones:
                continue
            kind = (data.get("activity") or {}).get("kind")
            if kind == "travel":
                continue
            if kind in _busy_kinds() or float(data.get("seen_at", 0.0)) >= cutoff:
                out.append(account)
        return out

    def _online(self, data: dict[str, Any]) -> bool:
        """🟢 en línea: a button in the last presence.minutes, or busy (exploring, gathering, hunting, sleeping), anywhere."""
        if (data.get("activity") or {}).get("kind") in _busy_kinds():
            return True
        return float(data.get("seen_at", 0.0)) >= self.clock.now() - self._seconds(self.content.balance["presence"]["minutes"])

    @staticmethod
    def _work_rate_cap(work: dict[str, Any]) -> float:
        """How many members a work can use at once: need / its floor (the minimum time, D-269: 10 min)."""
        return float(work["need"]) / max(EPS, float(work.get("floor") or 1.0))

    def _advance_work(self, work: dict[str, Any], members: list[str], zones: set[tuple[int, int]], actor: Hero | None) -> int:
        """Add to a work what the members present since its last check did; return how many are present now.

        [ES]
        Qué hace: suma al avance de una obra (fundar o una mejora) los segundos de cada miembro presente desde la última
        revisión ("at"), con el tope del piso de tiempo (nunca más rápido que gremio.found_floor_minutes / works.floor_minutes),
        y la deja revisada ahora. Devuelve cuántos están presentes ahora (para el tiempo que falta).
        La llaman: _founding_settle y _works_settle_camp. Si cambia, afecta: la regla "tiempo = minutos × 2 ÷ presentes".
        """
        now = self.clock.now()
        start = float(work.get("at", now))
        if now > start:
            cache: dict[str, dict[str, Any]] = {}
            total = sum(self._presence_window(a, self.store.get("hero", a), zones, start, now, cache) for a in members)
            gained = min(total, self._work_rate_cap(work) * (now - start))
            work["done"] = min(float(work["need"]), float(work.get("done", 0.0)) + gained)
        work["at"] = now
        return len(self._present_now(members, zones, actor))

    def _work_left(self, work: dict[str, Any], present: int) -> float | None:
        """Seconds left at this many members present; None if nobody is there (paused)."""
        if present <= 0:
            return None
        return max(0.0, float(work["need"]) - float(work.get("done", 0.0))) / min(float(present), self._work_rate_cap(work))

    def _work_line(self, key: str, name: str, work: dict[str, Any], present: int) -> str:
        """"🏗️ <name> ▓▓░░ 40 % · 👥 2 presentes · faltan 36 min" (or paused)."""
        t = self.texts
        need = max(EPS, float(work["need"]))
        pct = min(100, int(100 * float(work.get("done", 0.0)) / need))
        left = self._work_left(work, present)
        rest = t.t("works.left", n=present, time=self._fmt_duration(left)) if left is not None else t.t("works.paused")
        return t.t(key, name=name, bar=self._bar(float(work.get("done", 0.0)), need, 8), pct=pct, rest=rest)

    def _works_index(self, key: str, kind: str, ref: str, eta: float | None) -> None:
        self.store.put("works_open", key, {"kind": kind, "ref": ref, "eta": eta})

    def _works_settle(self, hero: Hero) -> list[str]:
        """Advance the works this hero takes part in (its guild's founding, its camp's improvements); notices for the hero.

        [ES]
        Qué hace: revisa la fundación del gremio del héroe y las obras en curso de su campamento (perezoso, como los viajes):
        las avanza con los presentes y termina las que ya llegaron. Devuelve los avisos para quien juega.
        La llaman: act(), view() y text() (después de _settle). Si cambia, afecta: cuándo terminan la fundación y las obras.
        """
        lines: list[str] = []
        record = self._gremio_link(hero.id)
        if record and record.get("founding") and not record.get("camp"):
            lines += self._founding_settle(record, hero)
        if hero.camp and self.store.get("works_open", f"build:{hero.camp}"):
            lines += self._works_settle_camp(hero.camp, hero)
        return lines

    def _works_tick(self) -> None:
        """tick(): finish the works whose expected end has come, even if no member plays now (their notices are pushed)."""
        now = self.clock.now()
        for key, entry in list(self.store.items("works_open")):
            eta = entry.get("eta")
            if eta is None or eta > now:
                continue
            if entry.get("kind") == "found":
                record = self._gremio(entry.get("ref"))
                if record and record.get("founding") and not record.get("camp"):
                    self._founding_settle(record, None)
                else:
                    self.store.delete("works_open", key)
            else:
                self._works_settle_camp(entry.get("ref", ""), None)

    # ------------------------------------------------------------------ 👥 Jugadores at the bonfire (D-265, D-274)

    def _players_view(self, hero: Hero, notice: str | None = None) -> View:
        """👥 Jugadores: who played at the bonfire in the last minute, the "N/20" counter and a code per player (D-265).

        [ES]
        Qué hace: la pantalla 👥 Jugadores de la fogata (D-274.1: reemplaza a 🔬 Investigar en el menú del Claro). Lista a los que
        tocaron un botón en la fogata en el último minuto (presence.bonfire_seconds) con su clase, nivel y gremio, cada uno con su
        código (/j1, /j2…: su tarjeta), y el contador "👥 N/20 en la fogata" (N con la regla de 15 min de 📍 Zona, D-274.2; 20 es
        bonfire.cap; desde la 0.37, en cualquiera de las 9 hogueras y con el reparto de D-265). Botones: 🛡️ Gremio, 🔄 Actualizar y ↩️ Volver.
        La llaman: 👥 Jugadores del Claro, /jugadores y /players. Si cambia, afecta: tests/test_gremio_desde_el_inicio.py.
        """
        t = self.texts
        if not mapgen.is_bonfire(hero.x, hero.y):       # D-265: any of the 9 bonfires
            return self._main_view(hero, notice=t.t("players.only_bonfire"))
        now = self.clock.now()
        window = self._seconds(float(self.content.balance["presence"].get("bonfire_seconds", 60)) / 60)
        present = self._zone_players(hero.x, hero.y, exclude=hero.id)
        cap = int(self.content.balance.get("bonfire", {}).get("cap", 20))
        recent = [p for p in present if p["seen"] >= now - window][:cap]
        body = [t.t("players.intro"), "", t.t("players.count", n=len(present) + 1, cap=cap), ""]
        for n, row in enumerate(recent, 1):
            guild = self._guild_name_of(row["id"])
            body.append(t.t("players.line", n=n, name=row["name"], cls=row["cls"], level=row["level"],
                            guild=t.t("players.guild_tag", name=guild) if guild else ""))
        body.append(t.t("players.hint") if recent else t.t("players.none"))
        self._codes(hero, "players", [row["id"] for row in recent])
        actions = [Action(id="guild", label=t.t("gremio.button")), Action(id="players", label=t.t("players.refresh")),
                   Action(id="claro", label=t.t("menu.back"))]
        return View(kind="players", title=t.t("players.title"), body=body, actions=actions, notice=notice)

    def _player_code(self, hero: Hero, n: int) -> View:
        """/j2: the card of the 2nd player of the last 👥 Jugadores list."""
        account = self._code_target(hero, "players", n)
        if account is None:
            return self._players_view(hero, notice=self.texts.t("players.bad_code"))
        return self._player_card(hero, account)

    def _player_card(self, hero: Hero, account: str, notice: str | None = None) -> View:
        """A player's card: class, level, guild, when they last played; ✉️ invite to your guild or 🙋 ask to join theirs.

        [ES]
        Qué hace: la tarjeta de otro jugador desde 👥 Jugadores. Si eres líder u oficial de un gremio sin campamento con lugar y
        ese jugador no tiene gremio ni campamento, ✉️ Invitar a mi gremio; si él está en un gremio sin campamento con lugar y tú
        no tienes, 🙋 Pedir entrar. Solo información y esos dos pedidos (D-96: ver a otros nunca da ventaja).
        La llaman: /j1 y "pcard:<cuenta>". Si cambia, afecta: tests/test_gremio_desde_el_inicio.py.
        """
        t = self.texts
        data = self.store.get("hero", account)
        if not data:
            return self._players_view(hero, notice=t.t("players.gone"))
        other = Hero.from_dict(data)
        guild = self._guild_name_of(account, data)
        body = [t.t("players.card_name", name=self._oath_mark(other) + self._banner(other) + self._emblem_name(other)),   # D-336: 💀
                t.t("players.card_class", cls=self._class_label(data), level=other.level),
                t.t("players.card_guild", name=guild) if guild else t.t("players.card_no_guild"),
                t.t("players.card_seen", ago=self._ago(other.seen_at))]
        if mapgen.is_bonfire(other.x, other.y):
            body.append(t.t("players.card_here", place=self._zone_name(self._zone(other.x, other.y))))
        body.append(t.t("players.card_code", code=self.player_code(account)))   # D-280: /inv_<code>
        actions = []
        mine = self._my_gremio(hero)
        theirs = self._gremio_link(account)
        camp = None if mine else self._member_camp(hero)
        if (mine and account != hero.id and self._gremio_manager(mine, hero.id) and self._gremio_room(mine)
                and self._gremio_free(account, data) and account not in mine.get("invites", [])):
            actions.append(Action(id=f"ginvite:{account}", label=t.t("gremio.invite_button")))
        elif camp and account != hero.id and self._camp_manager(camp, hero.id) and self._gremio_free(account, data):
            actions.append(Action(id=f"ginvite:{account}", label=t.t("gremio.invite_button")))   # D-294: camp or guild
        if (theirs and not theirs.get("camp") and account != hero.id and self._gremio_free(hero.id, hero)
                and self._gremio_room(theirs) and hero.id not in theirs.get("requests", [])):
            actions.append(Action(id=f"greq:{theirs['id']}", label=t.t("gremio.request_button", name=theirs["name"])))
        actions.append(Action(id="players", label=t.t("menu.back")))
        return View(kind="player_card", title=t.t("players.card_title"), body=body, actions=actions, notice=notice)

    # ------------------------------------------------------------------ the guild hub (D-269)

    def _gremio_action(self, hero: Hero, action_id: str) -> View:
        """Route the guild and bonfire buttons (GREMIO_ACTIONS). [ES] Qué hace: reparte los botones de esta sección (0.39: también
        ⚔️ "garm", 🤝 "ghelp:", 🙋 "creqs" y 💰 "gfund"/"gfund:svc", que después de fundar es el fondo del campamento; D-302,
        0.39.4: 👥 "gmembers", 💰 "gfunds" y 📢 "gchat", los submenús del gremio; D-322, 0.47: "gfcraft" abre o cierra el fondo
        para oficios y "gflog" es 📜 Quién usó qué). La llama:
        _idle_action. Si cambia, afecta: los IDs de botón del gremio (64 bytes como máximo en Telegram)."""
        arg = action_id.partition(":")[2]
        routes = {"players": lambda: self._players_view(hero), "gnew": lambda: self._gremio_new(hero),
                  "glist": lambda: self._gremio_list(hero), "greqs": lambda: self._gremio_requests_view(hero),
                  "gmsg": lambda: self._gremio_msg_ask(hero), "gfund": lambda: self._fund_view(hero),
                  "gmeet": lambda: self._gremio_meet_view(hero), "gmeetset": lambda: self._gremio_meet_set(hero),
                  "gfound": lambda: self._gremio_found_view(hero), "gfoundx": lambda: self._gremio_found_cancel(hero),
                  "gzones": lambda: self._gremio_zones_view(hero),
                  "garm": lambda: self._armory_view(hero),                  # D-290: ⚔️ Armería
                  "creqs": lambda: self._camp_requests_view(hero),          # D-289: the camp's join requests
                  "gmembers": lambda: self._guild_members_view(hero),       # D-302: 👥 Miembros
                  "gfunds": lambda: self._guild_funds_view(hero),           # D-302: 💰 Fondos (before "gfund": its prefix)
                  "gchat": lambda: self._guild_chat_view(hero),             # D-302: 📢 Chat
                  "gchat_toggle": lambda: self._guild_chat_toggle(hero),   
                  "gfcraft": lambda: self._fund_craft_toggle(hero),         # D-322: 🔓 / 🔒 the fund for the professions
                  "gflog": lambda: self._fund_log_view(hero),               # D-322: 📜 Quién usó qué
                  "gleave": lambda: self._gremio_leave(hero, confirmed=False)}
        if action_id in routes:
            return routes[action_id]()
        if action_id == "gleave!":
            return self._gremio_leave(hero, confirmed=True)
        if action_id == "gfund:svc":                    # D-291: 💰 Depositar from 🏘️ Servicios (its ↩️ goes back there)
            return self._fund_view(hero, back="upsvc")
        if action_id in ("gwleave", "gwleave!"):        # D-294: leave the guild while waiting for room
            return self._waiting_leave(hero, confirmed=action_id == "gwleave!")
        if action_id.startswith("cwjoin:"):             # D-294: 🏕️ Unir al campamento
            return self._camp_join_waiting(hero, arg)
        prefixed = {"pcard": lambda: self._player_card(hero, arg), "gcard": lambda: self._gremio_card(hero, arg),
                    "greq": lambda: self._gremio_request(hero, arg), "ginvite": lambda: self._gremio_invite(hero, arg),
                    "gmem": lambda: self._member_card(hero, arg), "goff": lambda: self._gremio_officer(hero, arg),
                    "ghelp": lambda: self._camp_helper_toggle(hero, arg),     # D-289
                    "glead": lambda: self._gremio_lead(hero, arg, confirmed=False),
                    "glead!": lambda: self._gremio_lead(hero, arg, confirmed=True),
                    "gkick": lambda: self._gremio_kick(hero, arg, confirmed=False),
                    "gkick!": lambda: self._gremio_kick(hero, arg, confirmed=True)}
        head = action_id.partition(":")[0]
        if head in prefixed:
            return prefixed[head]()
        return self._gremio_view(hero)

    def _guild_chat_toggle(self,hero: Hero) -> View:data = self.store.get("hero", hero.id) or {} enabled = not bool(data.get("chat_notifications", True)) 
        data["chat_notifications"] = enabled
        self.store.put("hero", hero.id, data)
        notice = self.texts.t("gremio.chat_notif_status", status="ON" if enabled else "OFF")
            return self._guild_chat_view(hero, notice=notice)

    def _gremio_view(self, hero: Hero, notice: str | None = None) -> View:
        """🛡️ Gremio before a camp: name, leader, founding and meeting point on top; members, fund and chat behind buttons (D-302).

        [ES]
        Qué hace: el centro del gremio antes del campamento (hasta 8 botones, de 2 en 2: HUB_KINDS "gremio"). Arriba el nombre,
        el líder y "👥 N/5", la fundación en curso con su barra y el 📍 punto de reunión. D-302 (0.39.4, la misma forma que el
        gremio después de fundar, pedido del dueño del 20-oct-2026): los miembros, el fondo y los mensajes ya no van en esta
        pantalla sino detrás de su botón; al líder o a un oficial, una línea corta si hay 🙋 solicitudes. Botones: 👥 Miembros
        (N/5) (cada miembro con /m1, 🙋 Solicitudes y 🚪 Salir; _gremio_members_view), 💰 Fondo del gremio (cada recurso con su
        código, lo que pide fundar y 💰 Depositar; _guild_funds_view), 📢 Chat (_guild_chat_view), ⚔️ Armería (D-290),
        📍 Reunión, 🔎 Buscar recursos, 🏕️ Fundar (el líder, o todos mientras se funda), 🚪 Salir (si entra en 8; si no, está en
        👥 Miembros) y ↩️ Volver. Sin gremio, qué es y cómo se crea o se busca (_gremio_none_view); con el campamento ya
        fundado, la invitación (_gremio_invite_view).
        La llaman: 🛡️ Gremio (de 👥 Jugadores y de /gremio sin campamento: _guild_view) y casi todas las acciones del gremio.
        Si cambia, afecta: tests/test_gremio_desde_el_inicio.py, tests/test_submenus_campamento_gremio.py y los recorridos de
        botones.
        """
        t = self.texts
        record = self._gremio_link(hero.id)
        if record and record.get("camp"):
            if hero.id in record.get("invited", []) and hero.camp is None:
                return self._gremio_invite_view(hero, record, notice)
            record = None
        if record is None or hero.id not in record.get("members", []):
            return self._gremio_none_view(hero, notice)
        leader = record["leader"]
        members = [leader] + [m for m in record["members"] if m != leader]
        body = [t.t("gremio.header", name=record["name"]),
                t.t("gremio.leader_line", leader=self._hero_name(leader) if leader != hero.id else hero.name,
                    n=len(members), cap=self._gremio_cap()), ""]
        founding = record.get("founding")
        if founding:
            zones = {(founding["x"], founding["y"])}
            present = len(self._present_now(record["members"], zones, hero))
            body.append(self._work_line("gremio.founding_line", self._place_label(founding["x"], founding["y"]), founding, present))
        meet = record.get("meet")
        body.append(t.t("gremio.meet_line", place=self._place_label(*meet)) if meet else t.t("gremio.meet_none"))
        manager = self._gremio_manager(record, hero.id)
        if manager and record.get("requests"):          # D-302: 🙋 the requests wait in 👥 Miembros
            body.append(t.t("guildmenu.requests_line", n=len(record["requests"])))
        self._codes(hero, "members", members)           # /m1 keeps working from this screen too
        actions = [Action(id="gmembers", label=t.t("guildmenu.members_button", n=len(members), cap=self._gremio_cap())),
                   Action(id="gfunds", label=t.t("guildmenu.gfunds_button")),
                   Action(id="gchat", label=t.t("guildmenu.chat_button")),
                   Action(id="garm", label=t.t("armory.button")),           # D-290: ⚔️ Armería from the first moment
                   Action(id="gmeet", label=t.t("gremio.meet_button")), Action(id="gzones", label=t.t("gzones.button"))]
        if hero.id == leader or founding:
            actions.append(Action(id="gfound", label=t.t("gremio.found_button")))
        if len(actions) < _hub_buttons() - 1:           # D-302: when it does not fit, 🚪 Salir waits in 👥 Miembros
            actions.append(Action(id="gleave", label=t.t("gremio.leave_button")))
        actions.append(Action(id=self._gremio_back(hero), label=t.t("menu.back")))
        return View(kind="gremio", title=t.t("gremio.title"), body=body, actions=actions, notice=notice)

    def _gremio_back(self, hero: Hero) -> str:
        """↩️ Volver of the guild: 👥 Jugadores at the bonfire, else 📍 Zona."""
        return "players" if mapgen.is_bonfire(hero.x, hero.y) and not hero.activity else "home"

    def _gremio_member_line(self, n: int, account: str, record: dict[str, Any], hero: Hero) -> str:
        """"/m1 👑 Lyra (nv 3) · 🟢 en línea · Colinas (5, 2) · 🔎 explorando"."""
        t = self.texts
        role = (t.t("gremio.role_leader") if account == record["leader"]
                else t.t("gremio.role_officer") if account in record.get("officers", []) else "")
        return self._member_row(n, account, role, hero)

    def _member_row(self, n: int, account: str, role: str, hero: Hero) -> str:
        """One member line with its code, role mark, level, online state, place and activity (before and after founding)."""
        t = self.texts
        data = self._hero_data(account, hero) or {}
        online = self._online(data)
        state = t.t("gremio.online") if online else t.t("gremio.offline", ago=self._ago(float(data.get("seen_at", 0.0))))
        kind = "combat" if self.store.get("combat", account) is not None else (data.get("activity") or {}).get("kind") or "idle"
        return t.t("gremio.member_line", code=f"/m{n}", role=role, name=data.get("name", "?"), level=data.get("level", 1),
                   state=state, where=self._place_label(data.get("x", 0), data.get("y", 0)),
                   activity=t.t(f"presence.activity.{kind}"))

    # ------------------------------------------------------------------ the guild's submenus: 👥 💰 📢 (D-302, 0.39.4)

    def _guild_members_view(self, hero: Hero, notice: str | None = None) -> View:
        """👥 Miembros: the guild's members (before founding) or the camp's (after it), with their codes (D-302).

        [ES] Qué hace: abre la pantalla de miembros que corresponde: la del gremio sin campamento (_gremio_members_view) o la del
        campamento (_camp_members_view; también para quien espera lugar, D-294). Sin gremio, la pantalla del gremio. La llama:
        el botón 👥 Miembros ("gmembers") y los ↩️ de la tarjeta de un miembro y de 🙋 Solicitudes. Si cambia, afecta:
        tests/test_submenus_campamento_gremio.py."""
        record = self._my_gremio(hero)
        if record:
            return self._gremio_members_view(hero, record, notice)
        camp = self._guild_camp(hero)
        if camp:
            return self._camp_members_view(hero, camp, notice)
        return self._gremio_view(hero, notice=notice)

    def _gremio_members_view(self, hero: Hero, record: dict[str, Any], notice: str | None = None) -> View:
        """👥 Miembros before founding: each member with /m1, where and doing what; 🙋 Solicitudes and 🚪 Salir (D-302).

        [ES] Qué hace: lo que la pantalla del gremio mostraba de los miembros (D-269): "👥 Miembros: N de 5", cada uno con su
        código (/m1: su tarjeta), 👑 el líder y ⭐ los oficiales, si está en línea, dónde está y qué hace, la pista de los
        códigos y, al líder o a un oficial con lugar, la de /inv_. Botones: 🙋 Solicitudes (líder u oficial, si hay), 🚪 Salir
        (siempre aquí: en el gremio solo si entra en 8) y ↩️ Volver al gremio. La llama: _guild_members_view. Si cambia, afecta:
        tests/test_submenus_campamento_gremio.py y tests/test_gremio_desde_el_inicio.py."""
        t = self.texts
        leader = record["leader"]
        members = [leader] + [m for m in record["members"] if m != leader]
        body = [t.t("guild.members", n=len(members), cap=self._gremio_cap()), ""]
        body += [self._gremio_member_line(n, account, record, hero) for n, account in enumerate(members, 1)]
        self._codes(hero, "members", members)
        body += ["", t.t("gremio.codes_hint")]
        manager = self._gremio_manager(record, hero.id)
        if manager and self._gremio_room(record):
            body.append(t.t("gremio.invite_hint"))     # D-280: /inv_ and the player's code
        actions = []
        if manager and record.get("requests"):
            actions.append(Action(id="greqs", label=t.t("gremio.requests_button", n=len(record["requests"]))))
        actions += [Action(id="gleave", label=t.t("gremio.leave_button")), Action(id="guild", label=t.t("menu.back"))]
        return View(kind="guild_members", title=t.t("guildmenu.members_title"), body=body, actions=actions, notice=notice)

    def _camp_members_view(self, hero: Hero, camp: dict[str, Any], notice: str | None = None) -> View:
        """👥 Miembros after founding: 🤝 helpers, each member with /m1, the ⏳ waiting block and 🙋 Solicitudes (D-302).

        [ES] Qué hace: lo que 🛡️ Gremio mostraba de los miembros después de fundar (D-291, D-289, D-294; pedido del dueño del
        20-oct-2026: "toda la información de los miembros dentro de ese botón. Esperando lugar en el campamento, lo mismo"):
        "👥 Miembros: N de cupo", la línea de 🤝 ayudantes (D-304, 0.41: en los textos, asistentes; al fundador le dice cómo
        nombrarlos, _helpers_founder_line), cada miembro con su código (/m1), 👑 el fundador y 🤝 los ayudantes,
        si está en línea, dónde está y qué hace, el bloque "⏳ Esperando lugar en el campamento" (sus códigos siguen después de
        los miembros; al fundador y a los ayudantes, cuántos lugares hay para unirlos), la pista de los códigos y, al fundador
        o a un ayudante con lugar, la de /inv_. Botones: 🙋 Solicitudes (fundador o ayudante, si hay) y ↩️ Volver al gremio.
        D-327 (0.51): el cupo es el de la etapa (_members_cap); al final, la línea 💤 de quien no juega 30 días (_idle_line), y
        💤 delante de quien ya fue avisado. Los 🤝 asistentes son los oficiales de D-253.4 (aceptan solicitudes).
        D-331 (0.55): debajo de los asistentes, la línea de tu 🪖 escuadra y su 🎖️ jefe (squads.py _squads_members_line), y el
        botón 🪖 Escuadras ("squads", solo para los miembros: quien espera lugar no está en ninguna); quedan 3 botones.
        La llama: _guild_members_view. Si cambia, afecta: tests/test_submenus_campamento_gremio.py, tests/test_ayudantes.py,
        tests/test_espera_del_gremio.py y tests/test_escuadras.py."""
        t = self.texts
        n, cap = len(camp["members"]), self._members_cap(camp)
        manager = self._camp_manager(camp, hero.id)
        helpers_line = (self._helpers_founder_line(camp, hero) if hero.id == camp.get("founder_id")    # D-304: how to name one
                        else self._helpers_line(camp, hero))
        body = [t.t("guild.members", n=n, cap=cap), helpers_line]     # D-289: 🤝 helpers (assistants in the texts)
        squad_line = self._squads_members_line(camp, hero)             # D-331: 🪖 your squad and its chief
        if squad_line:
            body.append(squad_line)
        body.append("")
        members = self._camp_member_order(hero, camp)
        body += [self._camp_member_line(i, account, camp, hero) for i, account in enumerate(members, 1)]
        body += self._waiting_lines(camp, hero, len(members) + 1)      # D-294: ⏳ their own block, codes go on
        self._codes(hero, "members", members + list(camp.get("waiting") or []))   # D-291: /m1 works after founding too
        body += ["", t.t("gremio.codes_hint")]
        idle = self._idle_line()                       # D-327: 💤 who does not play for 30 days frees the place
        if idle:
            body.append(idle)
        if manager and n < cap:
            body.append(t.t("gremio.invite_hint"))     # D-280, D-289: the founder or a helper invites with /inv_<code>
        actions = []
        requests = camp.get("requests") or []
        if manager and requests:                       # D-289: helpers answer the join requests too
            actions.append(Action(id="creqs", label=t.t("gremio.requests_button", n=len(requests))))
        if hero.id in camp["members"]:                 # D-331: 🪖 Escuadras (who waits for room is in no squad)
            actions.append(Action(id="squads", label=t.t("squads.button")))
        actions.append(Action(id="guild", label=t.t("menu.back")))
        return View(kind="guild_members", title=t.t("guildmenu.members_title"), body=body, actions=actions, notice=notice)

    def _fund_item_lines(self, fund: dict[str, int]) -> list[str]:
        """One line per thing in a fund, "/07 🪵 Madera ×12", by resource code (D-243); things without a code go last.

        [ES] Qué hace: lista un fondo en orden por el código de 📦 Recursos (el mismo /07 que abre para qué sirve cada recurso;
        el dueño: "todos los recursos y todas las cosas tienen que tener un código"). Lo que no tiene código (no debería haber:
        solo se depositan materiales con código) va al final, sin código. La llama: _guild_funds_view. Si cambia, afecta:
        tests/test_submenus_campamento_gremio.py."""
        t = self.texts

        def order(row: tuple[str, int]) -> tuple[int, int, str]:
            code = self.content.items[row[0]].get("code")
            return (0, int(code), row[0]) if code else (1, 0, row[0])

        rows = sorted(((i, n) for i, n in fund.items() if n > 0 and i in self.content.items), key=order)
        lines = []
        for item_id, n in rows:
            item = self.content.items[item_id]
            lines.append(t.t("guildmenu.fund_item", code=self._resource_code(item_id), emoji=item["emoji"],
                             item=t.t(item["name_key"]), n=n).strip())
        return lines

    def _guild_funds_view(self, hero: Hero, notice: str | None = None) -> View:
        """💰 Fondos: each thing in the fund with its resource code, what the fund is for, and 💰 Depositar (D-302).

        [ES] Qué hace: la pantalla del fondo, en orden por código (pedido del dueño del 20-oct-2026: "Fondo del campamento → un
        botón que se llame 💰 Fondos del campamento, listado en orden con su código"). Después de fundar: para qué sirve (le da
        a las obras activas lo que les falta), cuántas obras activas hay, cada recurso con su código de 📦 Recursos (/07) y la
        pista de los códigos. Antes de fundar (💰 Fondo del gremio): lo mismo con lo que pide fundar (✅ o ▫️). Botones:
        💰 Depositar ("gfund": tu mochila con los códigos /f02, quién dio qué) y ↩️ Volver al gremio. Sin gremio, la pantalla
        del gremio. D-322 (0.47): después de fundar suma el fondo para oficios (_fund_craft_lines: 🔓/🔒, el tope del día, lo
        guardado para las obras y el nivel, lo que sobra) y los botones 📜 Quién usó qué ("gflog") y, para el fundador o un 🤝
        asistente, 🔒 Cerrar / 🔓 Abrir para oficios ("gfcraft"): 4 botones como mucho. D-325 (0.49): debajo de las obras
        activas, la línea de la 🌾 cosecha de la muralla (game.py _harvest_line). La llama: el botón 💰 Fondos ("gfunds"; también
        el del aviso de la cosecha), el ↩️ de 💰 Depositar y de 📜 Quién usó qué, y _fund_craft_toggle. Si cambia, afecta:
        tests/test_submenus_campamento_gremio.py, tests/test_fondo_para_oficios.py y tests/test_cosecha_muralla.py."""
        t = self.texts
        record = self._my_gremio(hero)
        camp: dict[str, Any] | None = None
        upgrades: dict[str, Any] = {}
        if record:                                     # before founding: the guild's fund pays the founding
            fund = record.get("fund") or {}
            cost = self.content.balance["camps"]["found_cost"]
            ready = all(fund.get(i, 0) >= n for i, n in cost.items())
            body = [t.t("guildmenu.gfunds_intro"), ""] + (self._fund_item_lines(fund) or [t.t("guildmenu.funds_empty")])
            body += ["", ("✅ " if ready else "▫️ ") + t.t("gremio.fund_found", items=self._item_list(cost))]
            title = t.t("guildmenu.gfunds_title")
        else:
            camp = self._guild_camp(hero)
            if not camp:
                return self._gremio_view(hero, notice=notice)
            upgrades = self._upgrades(f"{camp['x']}:{camp['y']}")
            fund = upgrades.get("fund") or {}
            body = [t.t("guildmenu.funds_intro"), t.t("guildmenu.funds_works", n=len(self._active_works(camp, upgrades)))]
            body += self._harvest_line(camp, upgrades)       # D-325 (0.49): 🌾 what the wall's harvest brings to this fund
            body += [""] + (self._fund_item_lines(fund) or [t.t("guildmenu.funds_empty")])
            body += [""] + self._fund_craft_lines(camp, upgrades, hero)      # D-322: 🛠️ the fund for the professions
            title = t.t("guildmenu.funds_title")
        if fund:
            body += ["", t.t("guildmenu.funds_hint")]
        actions = [Action(id="gfund", label=t.t("services.deposit_button"))]
        if camp:                                       # D-322: 📜 Quién usó qué, and 🔓/🔒 for the founder or an assistant
            actions.append(Action(id="gflog", label=t.t("fcraft.log_button")))
            if self._camp_manager(camp, hero.id):
                actions.append(Action(id="gfcraft", label=t.t("fcraft.close_button" if self._fund_open(upgrades)
                                                              else "fcraft.open_button")))
        actions.append(Action(id="guild", label=t.t("menu.back")))
        return View(kind="guild_funds", title=title, body=body, actions=actions, notice=notice)

    def _chat_lines(self, messages: list[dict[str, Any]]) -> list[str]:
        """The chat lines of the last gremio.chat_hours, newest last, at most gremio.chat_shown and gremio.chat_max_chars.

        [ES] Qué hace: elige qué mensajes se ven en 📢 Chat (D-302, el dueño: "te sale el listado del chat del último día. Si es
        muy largo, lo reduces a la cantidad de mensajes que se puedan ver"): los de las últimas gremio.chat_hours (24 h), el
        más nuevo al final, como mucho gremio.chat_shown (20) y, si pasan de gremio.chat_max_chars letras (3.500, para que el
        mensaje de Telegram no pase su tope de 4.096), se quitan los más viejos. La llama: _guild_chat_view. Si cambia, afecta:
        tests/test_submenus_campamento_gremio.py."""
        t = self.texts
        cfg = self._gremio_cfg()
        since = self.clock.now() - self._seconds(float(cfg.get("chat_hours", 24)) * 60)
        shown = max(1, int(cfg.get("chat_shown", 20)))
        limit = max(1, int(cfg.get("chat_max_chars", 3500)))
        recent = [m for m in messages if float(m.get("at", 0.0)) >= since][-shown:]
        lines = [t.t("gremio.msg_line", name=m.get("by", "?"), text=m.get("text", "")) for m in recent]
        while lines and sum(len(line) + 1 for line in lines) > limit:
            lines.pop(0)
        return lines

    def _guild_chat_view(self, hero: Hero, notice: str | None = None) -> View:
        """📢 Chat: the guild's messages of the last day, the hint that any text goes to everyone, and 📢 Mensaje (D-302).

        [ES] Qué hace: la pantalla del chat del gremio (pedido del dueño del 20-oct-2026: "Últimos mensajes → conviértelo en un
        botón de 📢 Chat. Puedes verlo directamente cuando alguien escriba, o puedes venir aquí"). Antes de fundar, los mensajes
        del gremio; después, los del campamento (D-285, D-291; también para quien espera lugar, D-294). Muestra _chat_lines,
        "no hay mensajes del último día" si no hay, y la pista "💬 Escribe cualquier mensaje…". Botones: 📢 Mensaje ("gmsg") y
        ↩️ Volver al gremio. Sin gremio, la pantalla del gremio. La llaman: el botón 📢 Chat ("gchat"), el del aviso de un
        mensaje y _gremio_post. Si cambia, afecta: tests/test_submenus_campamento_gremio.py y tests/test_chat_del_gremio.py."""
        t = self.texts
        record = self._my_gremio(hero)
        camp = None if record else self._guild_camp(hero)
        if not (record or camp):
            return self._guild_view(hero, notice=notice)
        lines = self._chat_lines((record or camp).get("messages") or [])
        body = [t.t("guildmenu.chat_intro", hours=int(self._gremio_cfg().get("chat_hours", 24))), ""]
        body += lines or [t.t("guildmenu.chat_none")]
        body += ["", t.t("gremio.chat_hint"), status_text]
        actions = [Action(id="gmsg", label=t.t("gremio.msg_button")),
                   Action(id="gchat_toggle", label=t.t("gremio.chat_toggle_button")), Action(id="guild", label=t.t("menu.back"))]
        return View(kind="guild_chat", title=t.t("guildmenu.chat_title"), body=body, actions=actions, notice=notice)

    def _gremio_none_view(self, hero: Hero, notice: str | None = None) -> View:
        """No guild yet: what a guild is, its price and cap, and 🛡️ Crear gremio / 🔎 Buscar gremio."""
        t = self.texts
        cfg = self._gremio_cfg()
        body = [t.t("gremio.none_intro"), t.t("gremio.none_what"),
                t.t("gremio.none_cost", coins=self._money(int(cfg.get("found_coins", 20))), cap=self._gremio_cap()),
                t.t("gremio.none_found", n=int(cfg.get("found_min_members", 2)), minutes=int(cfg.get("found_minutes", 60))),
                "", t.t("gremio.none_code", code=self.player_code(hero.id))]      # D-280: so a leader can invite you
        actions = [Action(id="gnew", label=t.t("gremio.new_button")), Action(id="glist", label=t.t("gremio.list_button")),
                   Action(id="gzones", label=t.t("gzones.button")),          # D-296: 🔎 the resource finder, also alone
                   Action(id=self._gremio_back(hero), label=t.t("menu.back"))]
        return View(kind="gremio_none", title=t.t("gremio.title"), body=body, actions=actions, notice=notice)

    def _gremio_new(self, hero: Hero) -> View:
        """🛡️ Crear gremio: no guild and no camp, gremio.found_coins; then the next text is its name."""
        t = self.texts
        cost = int(self._gremio_cfg().get("found_coins", 20))
        if not self._gremio_free(hero.id, hero):
            return self._gremio_view(hero, notice=t.t("gremio.already"))
        if self._oath_no_lead(hero):                    # D-336: a 💀 hero leads nothing (there is no succession yet)
            return self._gremio_view(hero, notice=self._oath_no_lead(hero))
        if hero.gold < cost:
            return self._gremio_view(hero, notice=t.t("gremio.no_coins", coins=self._money(cost)))
        self.store.put("camp_naming", hero.id, {"mode": "gremio", "x": hero.x, "y": hero.y})
        return View(kind="name_gremio", title=t.t("gremio.title"), body=[t.t("gremio.ask_name")], expects_text=True,
                    actions=[Action(id="guild", label=t.t("gremio.cancel"))])

    def _gremio_text(self, hero: Hero, mode: str, text: str) -> View:
        """The free text of a guild prompt: its name ("gremio"), a 📢 message ("gmsg") or a search ("gsearch")."""
        if mode == "gmsg":
            return self._gremio_post(hero, text)
        if mode == "gsearch":
            return self._gremio_list(hero, query=text)
        if mode == "gzones":                             # D-282: a resource to look for among the guild's zones
            return self._gremio_zones_view(hero, query=text)
        return self._gremio_name(hero, text)

    def _gremio_name(self, hero: Hero, name: str) -> View:
        """The guild's name: like a camp name (it becomes the camp's), unique among guilds and camps; then it is created."""
        t = self.texts

        def again(key: str) -> View:
            return View(kind="name_gremio", title=t.t("gremio.title"), body=[t.t(key), t.t("gremio.ask_name")], expects_text=True,
                        actions=[Action(id="guild", label=t.t("gremio.cancel"))])

        if not GREMIO_NAME_RE.match(name):
            return again("gremio.bad_name")
        key = self._name_key(name)
        if self.store.get("guild_name", key) or self.store.get("camp_name", key):
            return again("gremio.name_taken")
        self.store.delete("camp_naming", hero.id)
        cost = int(self._gremio_cfg().get("found_coins", 20))
        if not self._gremio_free(hero.id, hero):
            return self._gremio_view(hero, notice=t.t("gremio.already"))
        if self._oath_no_lead(hero):                    # D-336: a 💀 hero leads nothing (a prompt opened before the oath)
            return self._gremio_view(hero, notice=self._oath_no_lead(hero))
        if hero.gold < cost:
            return self._gremio_view(hero, notice=t.t("gremio.no_coins", coins=self._money(cost)))
        seq = self.store.get("meta", "gremio_seq") or {"n": 0}
        seq["n"] = int(seq.get("n", 0)) + 1
        self.store.put("meta", "gremio_seq", seq)
        gid = f"g{seq['n']}"
        hero.gold -= cost
        self.store.put("gremio", gid, {"id": gid, "name": name, "leader": hero.id, "officers": [], "members": [hero.id],
                                       "requests": [], "invites": [], "created": self.clock.now(), "messages": [], "fund": {},
                                       "gave": {}, "meet": None, "founding": None, "camp": None, "invited": []})
        self.store.put("gremio_of", hero.id, {"gremio": gid})
        self.store.put("guild_name", key, {"gremio": gid})
        self.store.put("camp_name", key, {"gremio": gid})        # the camp will take this name: reserved
        return self._gremio_view(hero, notice=t.t("gremio.created", name=name, coins=self._money(cost)))

    def _gremio_list(self, hero: Hero, query: str | None = None, notice: str | None = None) -> View:
        """🔎 Buscar gremio: the guilds without a camp, most members first, each with its code (/g1); any text searches."""
        t = self.texts
        rows = [g for _, g in self.store.items("gremio") if not g.get("closed") and not g.get("camp")]
        if query:
            rows = [g for g in rows if _plain(query) in _plain(g["name"])]
        rows.sort(key=lambda g: (-len(g.get("members", [])), g.get("created", 0)))
        shown = rows[:int(self._gremio_cfg().get("list_shown", 8))]
        body = [t.t("gremio.list_intro") if not query else t.t("gremio.list_query", query=query), ""]
        for n, g in enumerate(shown, 1):
            full = "" if self._gremio_room(g) else t.t("gremio.list_full")
            body.append(t.t("gremio.list_line", n=n, name=g["name"], count=len(g.get("members", [])), cap=self._gremio_cap(),
                            leader=self._hero_name(g["leader"]), full=full))
        if not shown:
            body.append(t.t("gremio.list_none"))
        body += ["", t.t("gremio.list_hint")]
        self._codes(hero, "guilds", [g["id"] for g in shown])
        self.store.put("camp_naming", hero.id, {"mode": "gsearch", "x": hero.x, "y": hero.y})
        return View(kind="gremio_list", title=t.t("gremio.list_title"), body=body, expects_text=True, notice=notice,
                    actions=[Action(id="guild", label=t.t("menu.back"))])

    def _guild_code(self, hero: Hero, n: int) -> View:
        """/g2: the card of the 2nd guild of the last 🔎 Buscar gremio list."""
        gid = self._code_target(hero, "guilds", n)
        if gid is None:
            return self._gremio_list(hero, notice=self.texts.t("gremio.bad_code"))
        return self._gremio_card(hero, gid)

    def _gremio_card(self, hero: Hero, gid: str, notice: str | None = None) -> View:
        """A guild's card: leader, members and room; 🙋 Pedir entrar if you can."""
        t = self.texts
        record = self._gremio(gid)
        if not record or record.get("closed"):
            return self._gremio_list(hero, notice=t.t("gremio.gone"))
        names = [f"{self._hero_name(m)}" for m in record.get("members", [])]
        body = [t.t("gremio.header", name=record["name"]),
                t.t("gremio.leader_line", leader=self._hero_name(record["leader"]), n=len(names), cap=self._gremio_cap()),
                t.t("gremio.card_members", names=", ".join(names))]
        if record.get("camp"):
            body.append(t.t("gremio.card_has_camp"))
        actions = []
        if (not record.get("camp") and self._gremio_free(hero.id, hero) and self._gremio_room(record)
                and hero.id not in record.get("requests", [])):
            actions.append(Action(id=f"greq:{gid}", label=t.t("gremio.request_button", name=record["name"])))
        elif hero.id in record.get("requests", []):
            body.append(t.t("gremio.request_waiting"))
        actions.append(Action(id="glist", label=t.t("menu.back")))
        return View(kind="gremio_card", title=t.t("gremio.title"), body=body, actions=actions, notice=notice)

    # ------------------------------------------------------------------ joining: requests and invitations (D-269.1, D-253)

    def _gremio_request(self, hero: Hero, gid: str) -> View:
        """🙋 Pedir entrar: the leader and the officers get the request with ✅ / ❌ (each in their language)."""
        t = self.texts
        record = self._gremio(gid)
        if not record or record.get("closed") or record.get("camp"):
            return self._gremio_list(hero, notice=t.t("gremio.gone"))
        if not self._gremio_free(hero.id, hero):
            return self._gremio_view(hero, notice=t.t("gremio.already"))
        if not self._gremio_room(record):
            return self._gremio_card(hero, gid, notice=t.t("gremio.full"))
        if hero.id not in record["requests"]:
            record["requests"].append(hero.id)
            self.store.put("gremio", gid, record)
            managers = [record["leader"]] + [o for o in record.get("officers", []) if o != record["leader"]]
            self._push_each(managers, lambda: View(
                kind="gremio_request", title=t.t("gremio.request_title"),
                body=[t.t("gremio.request_body", name=hero.name, cls=self._class_label({"class_id": hero.class_id}),
                          level=hero.level, guild=record["name"])],
                actions=[Action(id=f"gans:{gid}:{hero.id}:y", label=t.t("gremio.accept")),
                         Action(id=f"gans:{gid}:{hero.id}:n", label=t.t("gremio.refuse"))]))
        return self._gremio_card(hero, gid, notice=t.t("gremio.request_sent", name=record["name"]))

    def _gremio_requests_view(self, hero: Hero) -> View:
        """🙋 Solicitudes: the first pending request with ✅ / ❌ (leader or officer)."""
        t = self.texts
        record = self._my_gremio(hero)
        if not record or not self._gremio_manager(record, hero.id) or not record.get("requests"):
            return self._gremio_view(hero)
        account = record["requests"][0]
        data = self.store.get("hero", account) or {}
        body = [t.t("gremio.request_body", name=data.get("name", "?"), cls=self._class_label(data), level=data.get("level", 1),
                    guild=record["name"]), t.t("gremio.requests_count", n=len(record["requests"]))]
        actions = [Action(id=f"gans:{record['id']}:{account}:y", label=t.t("gremio.accept")),
                   Action(id=f"gans:{record['id']}:{account}:n", label=t.t("gremio.refuse")),
                   Action(id="gmembers", label=t.t("menu.back"))]          # D-302: 🙋 lives in 👥 Miembros
        return View(kind="gremio_requests", title=t.t("gremio.request_title"), body=body, actions=actions)

    def _gremio_join(self, record: dict[str, Any], account: str) -> None:
        """Put a player in a guild (record saved by the caller) and link it."""
        if account not in record["members"]:
            record["members"].append(account)
        self.store.put("gremio_of", account, {"gremio": record["id"]})

    def _gremio_answer_action(self, hero: Hero, action_id: str) -> View:
        """Route the answers that arrive as pushes: a request (gans:), an invitation (ginv:) and the camp's (gcamp:)."""
        if action_id.startswith("gans:"):
            return self._gremio_answer(hero, action_id)
        if action_id.startswith("ginv:"):
            return self._gremio_invite_answer(hero, action_id)
        if action_id.startswith("cinv:"):
            return self._camp_invite_answer(hero, action_id)
        if action_id.startswith("cwait:"):              # D-294: into the guild while its camp is full
            return self._wait_invite_answer(hero, action_id)
        return self._gremio_camp_answer(hero, action_id)

    def _gremio_answer(self, hero: Hero, action_id: str) -> View:
        """✅ / ❌ a request: the leader or an officer; the player must still be free and the guild must have room.

        [ES]
        Qué hace: responde una solicitud ("gans:<gremio>:<cuenta>:y|n"). Entra si el líder o un oficial acepta, el jugador
        sigue sin gremio ni campamento y hay lugar (5 antes del campamento). Al jugador le llega la respuesta en su idioma.
        La llama: act() (antes del combate, como "join:"). Si cambia, afecta: quién entra a cada gremio.
        """
        t = self.texts
        parts = action_id.split(":")
        if len(parts) < 4 or parts[-1] not in ("y", "n"):
            return self._main_view(hero)
        gid, account, choice = parts[1], ":".join(parts[2:-1]), parts[-1]
        record = self._gremio(gid)
        if (not record or record.get("closed") or record.get("camp") or not self._gremio_manager(record, hero.id)
                or account not in record.get("requests", [])):
            return self._main_view(hero, notice=t.t("gremio.already_answered"))
        record["requests"].remove(account)
        data = self.store.get("hero", account)
        accepted = choice == "y" and self._gremio_free(account, data) and self._gremio_room(record)
        if accepted:
            self._gremio_join(record, account)
        self.store.put("gremio", gid, record)
        result = "accepted" if accepted else "refused"
        self._push_each([account], lambda: View(kind="gremio_answer", title=t.t("gremio.title"),
                                                body=[t.t(f"gremio.join_{result}", name=record["name"])],
                                                actions=[Action(id="guild", label=t.t("gremio.button"))]))
        return self._gremio_view(hero, notice=t.t(f"gremio.you_{result}", name=(data or {}).get("name", "?")))

    def _gremio_invite(self, hero: Hero, account: str) -> View:
        """✉️ Invitar a mi gremio (from a player's card or a visit notice): the player gets ✅ / ❌.

        [ES] Qué hace: antes de fundar, la invitación al gremio (líder u oficial). D-294 (0.39): después de fundar, el fundador o un
        🤝 ayudante invita al campamento si hay lugar o, si está lleno, al gremio (espera lugar). La llaman: "ginvite:<cuenta>"
        (tarjeta de 👥 Jugadores y el aviso de visita al campamento). Si cambia, afecta: tests/test_espera_del_gremio.py."""
        t = self.texts
        camp = None if self._my_gremio(hero) else self._member_camp(hero)
        if camp is not None and self._camp_manager(camp, hero.id):
            result = self._camp_or_wait_invite(hero, camp, account)
        else:
            result = self._gremio_invite_send(hero, account)
        if result == "only_managers":
            return self._players_view(hero, notice=t.t("gremio.only_managers"))
        return self._player_card(hero, account, notice=t.t(f"gremio.{result}", name=self._hero_name(account)))

    def _gremio_invite_send(self, hero: Hero, account: str) -> str:
        """Send the ✉️ invitation of your guild before its camp; returns the notice key (invite_sent, full, target_busy...).

        [ES]
        Qué hace: le manda al jugador la invitación del gremio (✅ / ❌) si eres líder u oficial, hay lugar y el jugador no
        tiene gremio ni campamento. La llaman: la tarjeta del jugador (✉️ Invitar) y /inv_<código> (D-280).
        Si cambia, afecta: quién puede invitar y tests/test_gremio_desde_el_inicio.py, tests/test_invitar_con_codigo.py.
        """
        t = self.texts
        record = self._my_gremio(hero)
        data = self.store.get("hero", account)
        if not record or not self._gremio_manager(record, hero.id):
            return "only_managers"
        if not self._gremio_room(record):
            return "full"
        if not self._gremio_free(account, data):
            return "target_busy"
        if account not in record["invites"]:
            record["invites"].append(account)
            self.store.put("gremio", record["id"], record)
            self._push_each([account], lambda: View(
                kind="gremio_invite", title=t.t("gremio.invite_title"),
                body=[t.t("gremio.invite_body", name=hero.name, guild=record["name"])],
                actions=[Action(id=f"ginv:{record['id']}:y", label=t.t("gremio.accept")),
                         Action(id=f"ginv:{record['id']}:n", label=t.t("gremio.refuse"))]))
        return "invite_sent"

    # ------------------------------------------------------------------ what the guild knows of the zones (D-282)

    def _mates(self, hero: Hero) -> list[str]:
        """The other accounts that share what they know of the zones with this hero (D-282).

        [ES]
        Qué hace: con quién comparte el héroe lo que sabe de las zonas (pedido del dueño, 18-oct-2026: "no tener que investigar
        doble la zona, para los del gremio únicamente"): los miembros de su gremio antes del campamento y, después, los
        miembros de su campamento (su gremio, D-97). D-294 (0.39): también los del gremio que esperan lugar en el campamento
        (camp["waiting"]): comparten zonas y chat con todos. Sin gremio ni campamento, nadie. La llaman: _mates_knowledge y
        _guild_chat. Si cambia, afecta: qué ve cada uno en 📍 Zona, el 🗺️ Mapa, 🗺️ Zonas del gremio, lo que pide fundar y a quién
        le llega el chat.
        """
        record = self._my_gremio(hero)
        if record:
            members = record.get("members", [])
        else:
            camp = self._guild_camp(hero)
            members = (list(camp.get("members", [])) + list(camp.get("waiting") or [])) if camp else []
        return [m for m in members if m != hero.id]

    def _mates_knowledge(self, hero: Hero) -> tuple[dict[str, int], dict[str, str], set[str]]:
        """What the mates know: the best % of each zone, who has it, and the zones they stood on (memo for this request).

        [ES]
        Qué hace: junta lo que exploraron los compañeros (el mejor % de cada zona entre ellos y el nombre de quien lo tiene) y las
        zonas que pisaron. Se lee una vez por pedido (queda guardado en el héroe cargado, no en la base: asdict no lo ve).
        La llaman: _known_pct, _knows_zone, _known_terrains y _gremio_zones_view.
        Si cambia, afecta: todo lo que el gremio comparte (D-282).
        """
        memo = hero.__dict__.get("_mates_memo")
        if memo is not None:
            return memo
        best: dict[str, int] = {}
        who: dict[str, str] = {}
        known: set[str] = set()
        for account in self._mates(hero):
            data = self.store.get("hero", account)
            if not data:
                continue
            for key, pct in (data.get("exploration") or {}).items():
                if int(pct) > best.get(key, 0):
                    best[key], who[key] = int(pct), data.get("name", "?")
            known.update(data.get("known") or [])
        memo = (best, who, known)
        hero.__dict__["_mates_memo"] = memo
        return memo

    def _known_pct(self, hero: Hero, x: int, y: int) -> int:
        """How far a zone is known: the hero's own % or the best of its guild's (D-282). Experience still uses its own."""
        key = f"{x}:{y}"
        return max(int(hero.exploration.get(key, 0)), self._mates_knowledge(hero)[0].get(key, 0))

    def _knows_zone(self, hero: Hero, x: int, y: int) -> bool:
        """The hero or a mate stood on that zone or explored it (D-282: the neighbours a founding asks for)."""
        key = f"{x}:{y}"
        best, _, known = self._mates_knowledge(hero)
        return hero.remembers(x, y) or key in known or best.get(key, 0) > 0

    def _gremio_zones_view(self, hero: Hero, query: str | None = None, notice: str | None = None) -> View:
        """🗺️ Zonas del gremio: the zones the guild knows, nearest first, with their resources, who explored them and a code.

        [ES]
        Qué hace: ordena lo que el gremio sabe de las zonas (D-282): las más cercanas primero (gzones.list_shown), cada una con
        su nombre y coordenadas, cuánto se conoce (el mejor % del gremio), los recursos ya descubiertos, quién la exploró y su
        código (/z1: arma el camino en 🔗 Moverte). D-296 (0.39.1, pedido del dueño): es también el 🔎 buscador de recursos:
        escribir un recurso ("madera") abre _resource_search_view (solo zonas investigadas al 50 % o más). Sin gremio ni
        campamento también se abre, con lo que exploraste tú y un aviso de que con un gremio verías lo de los demás. La llaman: el botón 🗺️ Zonas del gremio (🛡️ Gremio) y el texto
        escrito en esta pantalla. Si cambia, afecta: tests/test_conocimiento_del_gremio.py.
        """
        t = self.texts
        if query and " ".join(query.split()):              # D-296: a typed word is the 🔎 resource finder
            return self._resource_search_view(hero, query, notice=notice)
        alone = not self._mates(hero)                      # D-296: without a guild it lists what you explored yourself
        if alone and notice is None:
            notice = t.t("gzones.no_guild")
        best, who, _ = self._mates_knowledge(hero)
        merged, by = dict(best), dict(who)
        for key, pct in hero.exploration.items():
            if int(pct) > 0 and int(pct) >= merged.get(key, 0):
                merged[key], by[key] = int(pct), hero.name
        rows = []
        for key, pct in merged.items():
            x, y = (int(v) for v in key.split(":"))
            if pct <= 0 or mapgen.is_bonfire(x, y):
                continue
            known = self._known_resources(hero, x, y)
            rows.append((abs(x - hero.x) + abs(y - hero.y), x, y, pct, known, by.get(key, "?")))
        rows.sort()
        shown = rows[:int(self.content.balance.get("gremio", {}).get("zones_shown", 8))]
        self._codes(hero, "zones", [f"{x}:{y}" for _, x, y, _, _, _ in shown])
        self.store.put("camp_naming", hero.id, {"mode": "gzones", "x": hero.x, "y": hero.y})   # a text searches a resource
        body = [t.t("gzones.intro_alone" if alone else "gzones.intro"), ""]
        for n, (zones, x, y, pct, known, name) in enumerate(shown, 1):
            items = " ".join(self.content.items[r]["emoji"] for r in known) or "❔"
            body.append(t.t("gzones.line", n=n, place=self._place_label(x, y), pct=pct, items=items, who=name, zones=zones))
        if not shown:
            body.append(t.t("gzones.none_alone" if alone else "gzones.none"))
        elif len(rows) > len(shown):
            body.append(t.t("gzones.more", n=len(rows) - len(shown)))
        body += ["", t.t("gzones.hint", pct=self._search_min_pct())]
        actions = [Action(id="guild", label=t.t("menu.back"))]
        return View(kind="gremio_zones", title=t.t("gzones.title_alone" if alone else "gzones.title"), body=body,
                    actions=actions, notice=notice, expects_text=True)

    def _search_min_pct(self) -> int:
        """From what % of a zone investigated the 🔎 finder shows it (D-296: the owner said 50 %)."""
        return int(self._gremio_cfg().get("search_min_pct", 50))

    def _searchable_resources(self) -> list[str]:
        """Every resource a zone can have: the 6 base ones, every terrain's own ones and 🐟 fish (D-296)."""
        found = list(self.content.balance["resources"]["region_scale"])
        for bdef in self.content.biomes.values():
            found += [r for r in ((bdef or {}).get("own") or []) if r not in found]
        fish = ((self.content.balance.get("camp_professions") or {}).get("fish") or {}).get("resource")
        if fish and fish not in found:
            found.append(fish)
        return [r for r in found if r in self.content.items]

    def _resource_matches(self, query: str) -> list[str]:
        """The resources a typed word names, by their name in any language; an exact name wins over a part of one (D-296)."""
        wanted = _plain(" ".join(query.split()))
        if not wanted:
            return []
        names = {r: [_plain(n) for n in self.texts.all_languages(self.content.items[r]["name_key"])]
                 for r in self._searchable_resources()}
        exact = [r for r, plain in names.items() if wanted in plain]
        return exact or [r for r, plain in names.items() if any(wanted in n for n in plain)]

    def _resource_search_view(self, hero: Hero, query: str, notice: str | None = None) -> View:
        """🔎 The resource finder: where a resource is, in the zones you (or your guild) investigated to 50 % or more (D-296).

        [ES]
        Qué hace: el buscador de recursos (pedido del dueño, 19-oct-2026: "en el apartado del campamento y del gremio vas a poner
        un buscador de recursos… si busco madera, únicamente para zonas investigadas a más del 50 %, te va a decir en qué zona
        está para que puedas ir a farmearlo más fácil"). Con la palabra escrita (el nombre del recurso, con o sin tildes, en
        español o en inglés) lista las zonas investigadas al gremio.search_min_pct (50 %) o más, por ti o por tu gremio (D-282),
        donde ya se sabe que está: la más cercana primero, con su riqueza, cuánto queda (⏳ si está agotado) y el código /z1, que
        arma el camino en 🔗 Moverte. Sin gremio, usa solo lo que exploraste tú.
        D-303 (0.41.1: la 🪵 madera está en todas las zonas, pobre fuera del bosque): el orden pesa también la riqueza: cada
        zona cuenta como si estuviera (1 - riqueza) × gremio.search_rich_penalty zonas más lejos (con 4: al 30 %, 2,8 más;
        al 50 %, 2 más; al 100 %, nada). A igual cuenta, la más rica. La distancia que muestra es la de verdad.
        La llaman: _gremio_zones_view (lo escrito en 🔎 Buscar recursos), el atajo /buscar <recurso> (text()).
        Si cambia, afecta: tests/test_buscador_de_recursos.py y tests/test_conocimiento_del_gremio.py.
        """
        t = self.texts
        self.store.put("camp_naming", hero.id, {"mode": "gzones", "x": hero.x, "y": hero.y})   # another word searches again
        matches = self._resource_matches(query)
        actions = [Action(id="gzones", label=t.t("gzones.button")), Action(id="guild", label=t.t("menu.back"))]
        if not matches:
            examples = ", ".join(t.t(self.content.items[r]["name_key"]).lower()
                                 for r in self.content.balance["resources"]["region_scale"] if r in self.content.items)
            return View(kind="gremio_zones", title=t.t("rsearch.title"), body=[t.t("rsearch.unknown", query=query, examples=examples)],
                        actions=actions, notice=notice, expects_text=True)
        least = self._search_min_pct()
        best, _, _ = self._mates_knowledge(hero)
        keys = set(best) | {k for k, pct in hero.exploration.items() if int(pct) > 0}
        min_yield = float(self.content.balance["stock"]["min_yield"])
        rows = []
        for key in keys:
            x, y = (int(v) for v in key.split(":"))
            pct = self._known_pct(hero, x, y)
            if pct < least:
                continue
            known = self._known_resources(hero, x, y)
            here = [r for r in matches if r in known]
            if not here:
                continue
            resources, stock = self._zone_resources(x, y), self._stock(x, y)
            for res in here:
                rows.append((abs(x - hero.x) + abs(y - hero.y), x, y, res, pct, resources.get(res, 0.0), stock.get(res, 1.0)))
        penalty = float(self._gremio_cfg().get("search_rich_penalty", 0))   # D-303: near AND rich zones first
        rows.sort(key=lambda r: (round(r[0] + (1 - r[5]) * penalty, 2), -r[5], r[0], r[1], r[2], r[3]))
        shown = rows[:int(self._gremio_cfg().get("zones_shown", 8))]
        self._codes(hero, "zones", [f"{x}:{y}" for _, x, y, _, _, _, _ in shown])
        names = " · ".join(f"{self.content.items[r]['emoji']} {t.t(self.content.items[r]['name_key'])}" for r in matches)
        body = [t.t("rsearch.intro", names=names, pct=least), ""]
        for n, (zones, x, y, res, pct, rich, left) in enumerate(shown, 1):
            item = self.content.items[res]
            bars = round(left * 5)
            state = t.t("rsearch.empty") if left < min_yield else t.t("rsearch.left", bars=f"{'▰' * bars}{'▱' * (5 - bars)}")
            body.append(t.t("rsearch.line", n=n, emoji=item["emoji"], place=self._place_label(x, y), zones=zones, pct=pct,
                            rich=round(rich * 100), state=state))
        if not shown:
            body.append(t.t("rsearch.none", names=names, pct=least))
        elif len(rows) > len(shown):
            body.append(t.t("gzones.more", n=len(rows) - len(shown)))
        body += ["", t.t("rsearch.hint")]
        return View(kind="gremio_zones", title=t.t("rsearch.title"), body=body, actions=actions, notice=notice,
                    expects_text=True)

    def _zone_code(self, hero: Hero, n: int) -> View:
        """/z2: the 2nd zone of the last 🗺️ Zonas del gremio list: its road laid out in 🔗 Moverte (D-282, like /ir x y)."""
        key = self._code_target(hero, "zones", n)
        if key is None:
            return self._gremio_zones_view(hero, notice=self.texts.t("gzones.bad_code"))
        x, y = (int(v) for v in key.split(":"))
        return self._coord_walk(hero, x, y)

    # ------------------------------------------------------------------ the player code and /inv_<code> (D-280)

    def player_code(self, account_id: str) -> str:
        """The player's own 8-digit number, for /inv_<code> (D-280); stable: stored the first time it is asked for.

        [ES]
        Qué hace: el código de jugador (8 cifras), el que se escribe después de /inv_ para invitarlo a un gremio (pedido del
        dueño, 18-oct-2026: "/inv_ y el código de jugador"). Sale de la cuenta y se guarda la primera vez (espacios
        "player_code": código → cuenta y "player_code_of": cuenta → código); si dos cuentas dieran el mismo, la segunda prueba
        otro. Nunca cambia. La llaman: 👤 Héroe, la tarjeta de un jugador, 🛡️ Gremio y _account_by_code.
        Si cambia, afecta: los códigos que los jugadores ya se pasaron.
        """
        known = self.store.get("player_code_of", account_id)
        if known:
            return str(known["code"])
        salt = 0
        while True:
            code = str(10_000_000 + int(hash_unit("player_code", account_id, salt) * 90_000_000))
            owner = self.store.get("player_code", code)
            if owner is None or owner.get("account") == account_id:
                break
            salt += 1
        self.store.put("player_code", code, {"account": account_id})
        self.store.put("player_code_of", account_id, {"code": code})
        return code

    def _account_by_code(self, code: str) -> str | None:
        """The account whose player code this is (heroes that never showed theirs get one now), or None."""
        owner = self.store.get("player_code", code)
        if owner is None:
            for account, _ in self.store.items("hero"):
                if self.store.get("player_code_of", account) is None:
                    self.player_code(account)
            owner = self.store.get("player_code", code)
        account = (owner or {}).get("account")
        return account if account and self.store.get("hero", account) else None

    def _invite_code(self, hero: Hero, code: str) -> View:
        """/inv_<code>: invite that player to your guild, or to your camp once the guild founded it (D-280).

        [ES]
        Qué hace: el líder o un oficial de un gremio sin campamento invita con el código (lo mismo que ✉️ Invitar en la
        tarjeta, desde cualquier lugar); con el campamento ya fundado, invita su fundador o un 🤝 ayudante (D-289, 0.39), y al
        jugador le llega la invitación al campamento (✅ / ❌, "cinv:"). El jugador tiene que estar sin gremio ni campamento. Un código que no es de nadie,
        el tuyo propio o no tener permiso: avisa. La llama: text() con INVITE_CODE_RE.
        Si cambia, afecta: tests/test_invitar_con_codigo.py.
        """
        t = self.texts
        account = self._account_by_code(code)
        if account is None:
            return self._guild_view(hero, notice=t.t("gremio.code_unknown", code=code))
        if account == hero.id:
            return self._guild_view(hero, notice=t.t("gremio.code_self"))
        name = self._hero_name(account)
        if self._my_gremio(hero):
            return self._guild_view(hero, notice=t.t(f"gremio.{self._gremio_invite_send(hero, account)}", name=name))
        camp = self._member_camp(hero)
        if camp and self._camp_manager(camp, hero.id):  # D-289: the founder or a 🤝 helper; D-294: full → into the guild
            return self._guild_view(hero, notice=t.t(f"gremio.{self._camp_or_wait_invite(hero, camp, account)}", name=name))
        return self._guild_view(hero, notice=t.t("gremio.code_no_rights"))

    def _camp_invite_send(self, hero: Hero, camp: dict[str, Any], account: str) -> str:
        """The founder invites a free player into the camp (and so its guild, D-97); returns the notice key."""
        t = self.texts
        if not self._gremio_free(account, self.store.get("hero", account)):
            return "target_busy"
        if len(camp["members"]) >= self._members_cap(camp):
            return "full"
        key = f"{camp['x']}:{camp['y']}"
        invites = camp.setdefault("invites", [])
        if account not in invites:
            invites.append(account)
            self.store.put("camp", key, camp)
            name, founder = camp["name"], hero.name
            place = self._place_label(camp["x"], camp["y"])
            self._push_each([account], lambda: View(
                kind="camp_invite", title=t.t("gremio.cinv_title"),
                body=[t.t("gremio.cinv_body", name=founder, camp=name, place=place)],
                actions=[Action(id=f"cinv:{key}:y", label=t.t("gremio.camp_yes")),
                         Action(id=f"cinv:{key}:n", label=t.t("gremio.camp_no"))]))
        return "invite_sent"

    def _camp_invite_answer(self, hero: Hero, action_id: str) -> View:
        """✅ / ❌ a camp's invitation by code ("cinv:<x>:<y>:y|n"): in if still free and there is room (D-280)."""
        t = self.texts
        parts = action_id.split(":")
        if len(parts) != 4 or parts[3] not in ("y", "n"):
            return self._main_view(hero)
        key = f"{parts[1]}:{parts[2]}"
        camp = self.store.get("camp", key)
        if not camp or hero.id not in camp.get("invites", []):
            return self._main_view(hero, notice=t.t("gremio.already_answered"))
        camp["invites"].remove(hero.id)
        if parts[3] == "y" and not self._gremio_free(hero.id, hero):      # joined another guild or camp meanwhile
            self.store.put("camp", key, camp)
            return self._main_view(hero, notice=t.t("gremio.already"))
        joined = parts[3] == "y" and len(camp["members"]) < self._members_cap(camp)
        if joined:
            camp["members"].append(hero.id)
            hero.camp = key
        self.store.put("camp", key, camp)
        result = "joined" if joined else ("full" if parts[3] == "y" else "declined")
        managers = [m for m in self._camp_managers(camp) if m != hero.id]        # D-289: the founder and the helpers
        self._push_each(managers, lambda: View(kind="camp_answer", title=t.t("camps.title"),
                                               body=[t.t(f"gremio.camp_{result}_push", name=hero.name, camp=camp["name"])]))
        return self._main_view(hero, notice=t.t(f"gremio.camp_{result}", camp=camp["name"]))

    def _gremio_invite_answer(self, hero: Hero, action_id: str) -> View:
        """✅ / ❌ an invitation: in if still free and there is room; the leader is told."""
        t = self.texts
        parts = action_id.split(":")
        if len(parts) != 3 or parts[2] not in ("y", "n"):
            return self._main_view(hero)
        record = self._gremio(parts[1])
        if not record or record.get("closed") or record.get("camp") or hero.id not in record.get("invites", []):
            return self._main_view(hero, notice=t.t("gremio.already_answered"))
        record["invites"].remove(hero.id)
        accepted = parts[2] == "y" and self._gremio_free(hero.id, hero) and self._gremio_room(record)
        if accepted:
            self._gremio_join(record, hero.id)
        self.store.put("gremio", record["id"], record)
        result = "accepted" if accepted else "refused"
        self._push_each([record["leader"]], lambda: View(kind="gremio_answer", title=t.t("gremio.title"),
                                                         body=[t.t(f"gremio.invite_{result}", name=hero.name)]))
        if accepted:
            return self._gremio_view(hero, notice=t.t("gremio.welcome", name=record["name"]))
        return self._main_view(hero, notice=t.t("gremio.invite_declined"))

    # ------------------------------------------------------------------ members: officers, leader, leaving

    def _member_code(self, hero: Hero, n: int) -> View:
        """/m2: the 2nd member of your guild (the order of the last 🛡️ Gremio screen); after founding, of your camp (D-291)."""
        account = self._code_target(hero, "members", n)
        if account is None:
            return self._guild_view(hero, notice=self.texts.t("gremio.bad_code"))
        return self._member_card(hero, account)

    def _member_card(self, hero: Hero, account: str) -> View:
        """A member's card: the guild's before founding (_gremio_member_view), the camp's after it (_camp_member_view, D-291)."""
        if self._my_gremio(hero):
            return self._gremio_member_view(hero, account)
        if self._guild_camp(hero):
            return self._camp_member_view(hero, account)
        return self._gremio_view(hero, notice=self.texts.t("gremio.bad_code"))

    def _gremio_member_view(self, hero: Hero, account: str, notice: str | None = None) -> View:
        """A member's card: where, doing what, online, what they gave; the leader can name officers, hand over or remove."""
        t = self.texts
        record = self._my_gremio(hero)
        if not record or account not in record["members"]:
            return self._gremio_view(hero)
        data = self._hero_data(account, hero) or {}
        gave = (record.get("gave") or {}).get(account) or {}
        body = [self._gremio_member_line(record["members"].index(account) + 1, account, record, hero),
                t.t("gremio.member_class", cls=self._class_label(data), level=data.get("level", 1)),
                t.t("gremio.member_gave", items=self._item_list(gave)) if gave else t.t("gremio.member_gave_none")]
        actions = []
        if hero.id == record["leader"] and account != hero.id:
            officer = account in record.get("officers", [])
            actions += [Action(id=f"goff:{account}", label=t.t("gremio.unofficer_button" if officer else "gremio.officer_button")),
                        Action(id=f"glead:{account}", label=t.t("gremio.lead_button")),
                        Action(id=f"gkick:{account}", label=t.t("gremio.kick_button"))]
        actions.append(Action(id="gmembers", label=t.t("menu.back")))           # D-302: back to 👥 Miembros
        return View(kind="gremio_member", title=t.t("gremio.title"), body=body, actions=actions, notice=notice)

    def _gremio_officer(self, hero: Hero, account: str) -> View:
        """⭐ Nombrar oficial / ✖️ Quitar oficial (the leader). Officers accept requests and invite (D-253)."""
        t = self.texts
        record = self._my_gremio(hero)
        if not record or hero.id != record["leader"] or account not in record["members"] or account == hero.id:
            return self._gremio_view(hero)
        officers = record.setdefault("officers", [])
        named = account not in officers
        if named:
            officers.append(account)
        else:
            officers.remove(account)
        self.store.put("gremio", record["id"], record)
        key = "officer_named" if named else "officer_removed"
        self._push_each([account], lambda: View(kind="gremio_news", title=t.t("gremio.title"),
                                                body=[t.t(f"gremio.{key}_push", guild=record["name"])]))
        return self._gremio_member_view(hero, account, notice=t.t(f"gremio.{key}", name=self._hero_name(account)))

    def _gremio_confirm(self, title_key: str, body: str, yes: str, no: str) -> View:
        t = self.texts
        return View(kind="gremio_confirm", title=t.t(title_key), body=[body],
                    actions=[Action(id=yes, label=t.t("gremio.confirm_yes")), Action(id=no, label=t.t("gremio.confirm_no"))])

    def _gremio_lead(self, hero: Hero, account: str, confirmed: bool) -> View:
        """👑 Ceder liderazgo (asks first): the old leader stays as an officer."""
        t = self.texts
        record = self._my_gremio(hero)
        if not record or hero.id != record["leader"] or account not in record["members"] or account == hero.id:
            return self._gremio_view(hero)
        name = self._hero_name(account)
        if self._oath_account_on(account):              # D-336: a 💀 hero cannot receive the leadership (no succession yet)
            return self._gremio_view(hero, notice=t.t("oath.no_lead_other", name=name))
        if not confirmed:
            return self._gremio_confirm("gremio.title", t.t("gremio.lead_ask", name=name), f"glead!:{account}", f"gmem:{account}")
        record["leader"] = account
        officers = [o for o in record.get("officers", []) if o != account]
        record["officers"] = officers + [hero.id]
        record["members"] = [account] + [m for m in record["members"] if m != account]
        self.store.put("gremio", record["id"], record)
        self._push_each([account], lambda: View(kind="gremio_news", title=t.t("gremio.title"),
                                                body=[t.t("gremio.lead_push", name=hero.name, guild=record["name"])]))
        return self._gremio_view(hero, notice=t.t("gremio.lead_done", name=name))

    def _gremio_leave_member(self, record: dict[str, Any], account: str) -> None:
        """Take a member out of a guild (record saved by the caller); what they gave stays in the fund (rule 3)."""
        record["members"] = [m for m in record["members"] if m != account]
        record["officers"] = [o for o in record.get("officers", []) if o != account]
        self.store.delete("gremio_of", account)

    def _gremio_kick(self, hero: Hero, account: str, confirmed: bool) -> View:
        """🚫 Sacar del gremio (the leader; asks first). What they gave stays in the fund."""
        t = self.texts
        record = self._my_gremio(hero)
        if not record or hero.id != record["leader"] or account not in record["members"] or account == hero.id:
            return self._gremio_view(hero)
        name = self._hero_name(account)
        if not confirmed:
            return self._gremio_confirm("gremio.title", t.t("gremio.kick_ask", name=name), f"gkick!:{account}", f"gmem:{account}")
        self._gremio_leave_member(record, account)
        self.store.put("gremio", record["id"], record)
        self._push_each([account], lambda: View(kind="gremio_news", title=t.t("gremio.title"),
                                                body=[t.t("gremio.kicked_push", guild=record["name"])]))
        return self._gremio_view(hero, notice=t.t("gremio.kicked", name=name))

    def _gremio_leave(self, hero: Hero, confirmed: bool) -> View:
        """🚪 Salir del gremio (asks first). A leader with members hands over first; the last one dissolves it.

        [ES]
        Qué hace: un miembro sale (lo que dio queda en el fondo, regla 3). El líder con otros miembros primero cede el liderazgo
        (👑, desde la tarjeta del miembro). Si el líder está solo, el gremio se disuelve: se corta la fundación en curso, el
        fondo entero vuelve a su mochila (D-290: y las piezas de la ⚔️ Armería también) y su nombre queda libre. La llaman: 🚪 Salir y su confirmación ("gleave!").
        Si cambia, afecta: tests/test_gremio_desde_el_inicio.py.
        """
        t = self.texts
        record = self._my_gremio(hero)
        if not record:
            return self._gremio_view(hero)
        alone = record["members"] == [hero.id]
        if hero.id == record["leader"] and not alone:
            return self._gremio_view(hero, notice=t.t("gremio.leave_hand_over"))
        if not confirmed:
            return self._gremio_confirm("gremio.title", t.t("gremio.dissolve_ask" if alone else "gremio.leave_ask", name=record["name"]),
                                        "gleave!", "guild")
        if not alone:
            self._gremio_leave_member(record, hero.id)
            self.store.put("gremio", record["id"], record)
            self._push_each([record["leader"]], lambda: View(kind="gremio_news", title=t.t("gremio.title"),
                                                             body=[t.t("gremio.left_push", name=hero.name, guild=record["name"])]))
            return self._gremio_view(hero, notice=t.t("gremio.left", name=record["name"]))
        founding = record.get("founding")
        if founding:                                    # the founding stops: what the fund paid goes back to it first
            for item, n in (founding.get("paid") or {}).items():
                record["fund"][item] = record["fund"].get(item, 0) + n
            self.store.delete("works_open", f"found:{record['id']}")
        for item, n in record.get("fund", {}).items():  # rule 3: the last one takes the whole fund back (nothing is lost)
            hero.backpack[item] = hero.backpack.get(item, 0) + n
        given = dict(record.get("fund", {}))
        pieces = self._armory_empty_to(hero, record["id"])   # D-290 (rule 7): the armory's pieces too
        key = self._name_key(record["name"])
        for space in ("guild_name", "camp_name"):
            if (self.store.get(space, key) or {}).get("gremio") == record["id"] and "camp" not in (self.store.get(space, key) or {}):
                self.store.delete(space, key)
        record.update(closed=True, members=[], officers=[], requests=[], invites=[], founding=None, fund={})
        self.store.put("gremio", record["id"], record)
        self.store.delete("gremio_of", hero.id)
        lines = [t.t("gremio.dissolved", name=record["name"])]
        if given:
            lines.append(t.t("gremio.fund_back", items=self._item_list(given)))
        if pieces:
            lines.append(t.t("armory.back", items=" · ".join(self._gear_name(i) for i in pieces)))
        return self._gremio_none_view(hero, notice="\n".join(lines))

    # ------------------------------------------------------------------ 📢 messages, 💰 fund, 📍 meeting point (D-269.2)

    def _gremio_msg_ask(self, hero: Hero) -> View:
        """📢 Mensaje: the next text goes to every member (D-291: after founding too, to the camp's members).

        [ES] Qué hace: la próxima frase que escribas va a todo el gremio. ❌ Cancelar vuelve a 📢 Chat (D-302: el botón está
        ahí). La llaman: 📢 Mensaje de 📢 Chat ("gmsg"; también los botones viejos del gremio) y _gremio_post (texto vacío)."""
        t = self.texts
        if not self._my_gremio(hero) and not self._guild_camp(hero):
            return self._guild_view(hero)
        self.store.put("camp_naming", hero.id, {"mode": "gmsg", "x": hero.x, "y": hero.y})
        return View(kind="gremio_msg", title=t.t("gremio.title"),
                    body=[t.t("gremio.msg_ask", n=int(self._gremio_cfg().get("message_max_chars", 200)))], expects_text=True,
                    actions=[Action(id="gchat", label=t.t("gremio.cancel"))])

    def _gremio_post(self, hero: Hero, text: str) -> View:
        """Send a 📢 message: cut to gremio.message_max_chars, kept with the last gremio.messages_kept, pushed to every member.

        [ES]
        Qué hace: manda el texto a cada miembro (_push_each: el título les llega en su idioma; el texto es del jugador) y lo
        guarda con los últimos gremio.messages_kept (50 desde D-302). Lo que pasa del largo se corta con "…". D-291 (0.39):
        después de fundar también (va a los miembros del campamento, por _guild_chat). D-302 (0.39.4): vuelve a 📢 Chat, con
        tu mensaje al final. La llama: _gremio_text.
        Si cambia, afecta: tests/test_gremio_desde_el_inicio.py, tests/test_deposito_tras_fundar.py y
        tests/test_submenus_campamento_gremio.py.
        """
        t = self.texts
        record = self._my_gremio(hero)
        self.store.delete("camp_naming", hero.id)
        if not record and not self._guild_camp(hero):
            return self._guild_view(hero)
        if not " ".join(text.split()):
            return self._gremio_msg_ask(hero)
        self._guild_chat(hero, text)
        return self._guild_chat_view(hero, notice=t.t("gremio.msg_sent"))

    def _guild_chat(self, hero: Hero, text: str) -> str | None:
        """A message to the whole guild (or camp): kept with the last few and pushed to every mate; None without a guild.

        [ES]
        Qué hace: manda un mensaje a todos los compañeros (_mates: el gremio sin campamento o el campamento, D-282), cortado a
        gremio.message_max_chars, y lo guarda con los últimos gremio.messages_kept (en el gremio o en el campamento). D-285
        (pedido del dueño, 19-oct-2026: "cuando ya se crea un gremio, todos los mensajes que se envíen dentro del juego van a
        ser recibidos por el resto de jugadores"): cualquier texto suelto que escribe un miembro (que no sea un comando ni la
        respuesta a una pantalla que pide texto) llega a todos. Devuelve el aviso para quien lo mandó, o None si no tiene
        gremio. D-302 (0.39.4): se guardan los últimos 50 (gremio.messages_kept) para la pantalla 📢 Chat (_guild_chat_view, los
        del último día) y el botón del aviso abre 📢 Chat. La llaman: text() (el texto suelto) y _gremio_post (📢 Mensaje).
        Si cambia, afecta: el chat del gremio.
        """
        t = self.texts
        text = " ".join(text.split())
        record = self._my_gremio(hero)
        camp = None if record else self._guild_camp(hero)    # D-294: a member waiting for room chats with the guild too
        if not (record or camp) or not text:
            return None
        mates = self._mates(hero)
        cap = int(self._gremio_cfg().get("message_max_chars", 200))
        if len(text) > cap:
            text = text[:max(1, cap - 1)].rstrip() + "…"
        keep = max(1, int(self._gremio_cfg().get("messages_kept", 5)))
        entry = {"by": hero.name, "id": hero.id, "text": text, "at": self.clock.now()}
        if record:
            record["messages"] = ((record.get("messages") or []) + [entry])[-keep:]
            self.store.put("gremio", record["id"], record)
            name = record["name"]
        else:
            camp["messages"] = ((camp.get("messages") or []) + [entry])[-keep:]
            self.store.put("camp", f"{camp['x']}:{camp['y']}", camp)
            name = camp["name"]
        self._push_each(mates, lambda: View(
            kind="gremio_message", title=t.t("gremio.msg_push_title", name=name),
            body=[t.t("gremio.msg_line", name=hero.name, text=text)],
            actions=[Action(id="gchat", label=t.t("guildmenu.chat_button"))]))      # D-302: the push opens 📢 Chat
        return t.t("gremio.chat_sent", n=len(mates))

    def _gremio_fund_view(self, hero: Hero, notice: str | None = None) -> View:
        """💰 Fondo: totals, what founding asks, who gave what, and your backpack's materials with a code each (/f02).

        [ES]
        Qué hace: el fondo del gremio (D-269.2: "no tienen que llevarlo a ningún lugar"): cada miembro deposita desde donde esté
        escribiendo o tocando el código de un material (/f02, el mismo número de 📦 Recursos): pasa todo lo que lleva de eso.
        Muestra el total, lo que pide fundar (camps.found_cost) y quién dio qué. D-302 (0.39.4): es la pantalla de 💰 Depositar,
        dentro de 💰 Fondo del gremio (_guild_funds_view, la lista con los códigos de 📦 Recursos); su ↩️ Volver va ahí.
        La llaman: 💰 Depositar ("gfund") y _fund_code. Si cambia, afecta: tests/test_gremio_desde_el_inicio.py.
        """
        t = self.texts
        record = self._my_gremio(hero)
        if not record:
            return self._gremio_view(hero)
        fund = record.get("fund") or {}
        cost = self.content.balance["camps"]["found_cost"]
        ready = all(fund.get(i, 0) >= n for i, n in cost.items())
        body = [t.t("gremio.fund_intro"), "",
                t.t("gremio.fund_line", items=self._item_list(fund)) if fund else t.t("gremio.fund_empty"),
                ("✅ " if ready else "▫️ ") + t.t("gremio.fund_found", items=self._item_list(cost))]
        gave = record.get("gave") or {}
        if gave:
            body += ["", t.t("gremio.fund_gave_title")]
            body += [t.t("gremio.fund_gave_line", name=self._hero_name(acc) if acc != hero.id else hero.name,
                         items=self._item_list(items)) for acc, items in gave.items() if items]
        mine = self._fund_goods(hero)
        body += ["", t.t("gremio.fund_bag_title")]
        for item_id, n in mine:
            item = self.content.items[item_id]
            body.append(t.t("gremio.fund_bag_line", code=f"{int(item['code']):02d}", emoji=item["emoji"], item=t.t(item["name_key"]), n=n))
        if not mine:
            body.append(t.t("gremio.fund_bag_none"))
        return View(kind="gremio_fund", title=t.t("gremio.fund_title"), body=body, notice=notice,
                    actions=[Action(id="gfunds", label=t.t("menu.back"))])       # D-302: back to 💰 Fondo del gremio

    def _fund_goods(self, hero: Hero) -> list[tuple[str, int]]:
        """The materials of the backpack that the fund takes (with a code; never food: it is for the pantry), by code."""
        rows = [(i, n) for i, n in hero.backpack.items()
                if n > 0 and self.content.items.get(i, {}).get("kind") == "material" and self.content.items[i].get("code")
                and not self.content.items[i].get("food")]
        return sorted(rows, key=lambda kv: int(self.content.items[kv[0]]["code"]))

    def _fund_code(self, hero: Hero, code: int) -> View:
        """/f02: put every unit of that material you carry in the guild's fund, from wherever you are (not in a fight).

        [ES] Qué hace: deposita en el 💰 fondo todo lo que llevas de ese material (su código de 📦 Recursos). Antes de fundar, en
        el fondo del gremio; D-291 (0.39): después de fundar, en el fondo del campamento, que alimenta las obras activas
        (_camp_deposit). Sin gremio ni campamento, avisa. La llama: text() con FUND_CODE_RE. Si cambia, afecta:
        tests/test_gremio_desde_el_inicio.py y tests/test_deposito_tras_fundar.py."""
        t = self.texts
        if self.store.get("combat", hero.id) is not None:
            return self._main_view(hero)
        record = self._my_gremio(hero)
        if not record:
            camp = self._guild_camp(hero)
            if camp:                                    # D-291: after founding, the camp's fund (it feeds the active works)
                return self._camp_deposit(hero, camp, code)
            return self._gremio_view(hero, notice=t.t("gremio.fund_no_guild"))
        item_id = next((i for i, _ in self._fund_goods(hero) if int(self.content.items[i]["code"]) == code), None)
        if item_id is None:
            return self._gremio_fund_view(hero, notice=t.t("gremio.fund_no_code", code=f"/f{code:02d}"))
        n = hero.backpack.pop(item_id)
        record["fund"][item_id] = record["fund"].get(item_id, 0) + n
        mine = record.setdefault("gave", {}).setdefault(hero.id, {})
        mine[item_id] = mine.get(item_id, 0) + n
        self.store.put("gremio", record["id"], record)
        return self._gremio_fund_view(hero, notice=t.t("gremio.fund_given", items=self._item_list({item_id: n})))

    def _gremio_meet_view(self, hero: Hero, notice: str | None = None) -> View:
        """📍 Reunión: the meeting point, how far it is, 📍 Marcar aquí (leader) and 🧭 Ir al punto (with 📒 Lugares' question)."""
        t = self.texts
        record = self._my_gremio(hero)
        if not record:
            return self._gremio_view(hero)
        meet = record.get("meet")
        body = [t.t("gremio.meet_intro")]
        actions = []
        if meet:
            x, y = meet
            body.append(t.t("gremio.meet_line", place=self._place_label(x, y)))
            if (x, y) != (hero.x, hero.y):
                body.append(t.t("gremio.meet_far", zones=abs(x - hero.x) + abs(y - hero.y),
                                time=self._fmt_duration(self._trip_seconds(hero, x, y))))
                actions.append(Action(id=f"goask:{x}:{y}", label=t.t("gremio.meet_go")))
            else:
                body.append(t.t("gremio.meet_here"))
        else:
            body.append(t.t("gremio.meet_none"))
        if hero.id == record["leader"]:
            actions.insert(0, Action(id="gmeetset", label=t.t("gremio.meet_set")))
        actions.append(Action(id="guild", label=t.t("menu.back")))
        return View(kind="gremio_meet", title=t.t("gremio.meet_title"), body=body, actions=actions, notice=notice)

    def _gremio_meet_set(self, hero: Hero) -> View:
        """📍 Marcar aquí (the leader): the meeting point is this zone; every member is told, with a 🧭 Ir button."""
        t = self.texts
        record = self._my_gremio(hero)
        if not record or hero.id != record["leader"]:
            return self._gremio_meet_view(hero)
        record["meet"], record["meet_by"] = [hero.x, hero.y], hero.name
        self.store.put("gremio", record["id"], record)
        x, y = hero.x, hero.y
        self._push_each([m for m in record["members"] if m != hero.id], lambda: View(
            kind="gremio_news", title=t.t("gremio.meet_title"),
            body=[t.t("gremio.meet_push", name=hero.name, place=self._place_label(x, y))],
            actions=[Action(id=f"goask:{x}:{y}", label=t.t("gremio.meet_go")), Action(id="guild", label=t.t("gremio.button"))]))
        return self._gremio_meet_view(hero, notice=t.t("gremio.meet_done", place=self._place_label(x, y)))

    def _gremio_site(self, hero: Hero) -> tuple[int, int, str] | None:
        """Where this hero's guild builds: (x, y, kind) with kind "camp" (founded, you are invited), "found" or "meet".

        [ES]
        Qué hace: el lugar de la construcción del gremio del héroe (pedido del dueño, 18-oct): el campamento ya fundado si te
        invitaron y no respondiste, la fundación en curso o, si no hay, el 📍 punto de reunión. None si no hay lugar definido.
        La llaman: _build_site_action (📍 Zona y el viaje), _gremio_places (📒 Lugares) y _gremio_goal (_can_goto).
        """
        record = self._gremio_link(hero.id)
        if not record:
            return None
        if record.get("camp"):
            if hero.id not in record.get("invited", []) or hero.camp is not None:
                return None
            camp = self.store.get("camp", record["camp"])
            return (camp["x"], camp["y"], "camp") if camp else None
        if hero.id not in record.get("members", []):
            return None
        founding = record.get("founding")
        if founding:
            return founding["x"], founding["y"], "found"
        meet = record.get("meet")
        return (meet[0], meet[1], "meet") if meet else None

    def _build_site_action(self, hero: Hero) -> Action | None:
        """🏗️ Moverte a la construcción: a wide button of 📍 Zona (and of the trip) while the guild has a place defined.

        [ES]
        Qué hace: el botón que pidió el dueño (18-oct: "cuando ya se define el lugar donde se va a empezar la construcción, le
        va a salir un botón de moverse"): lleva a 📒 Lugares → "¿Viajar?" ("goask:x:y") y el héroe va solo por el camino de
        verdad, sin diagonales (_path: primero este-oeste, después norte-sur), aunque nunca haya pisado esa zona. No sale si no
        hay lugar definido, si ya estás ahí o si el campamento ya está fundado y eres miembro. En el viaje no sale si ya vas
        hacia ese lugar. La llaman: _zone_view (layout [2, 2, 1, 1, 1] solo con este botón) y _activity_view (de viaje).
        Si cambia, afecta: tests/test_gremio_desde_el_inicio.py y tests/test_buttons.py (los layouts de 📍 Zona).
        """
        site = self._gremio_site(hero)
        if site is None or (site[0], site[1]) == (hero.x, hero.y):
            return None
        goal = (hero.activity or {}).get("goal")
        if goal and list(goal) == [site[0], site[1]]:
            return None
        return Action(id=f"goask:{site[0]}:{site[1]}", label=self.texts.t("gremio.site_button"))

    def _gremio_places(self, hero: Hero) -> list[tuple[int, int, str, str]]:
        """(x, y, icon, name) of the guild's places for 📒 Lugares: the 🏗️ construction (or the camp) or the 📍 meeting point."""
        t = self.texts
        record = self._gremio_link(hero.id)
        if not record:
            return []
        out = []
        site = self._gremio_site(hero)
        if site and site[2] == "found":
            out.append((site[0], site[1], "🏗️", t.t("gremio.found_place", name=record["name"])))
        elif site and site[2] == "camp":
            out.append((site[0], site[1], "🏕️", record["name"]))
        meet = record.get("meet") if not record.get("camp") else None
        if meet and not any((x, y) == tuple(meet) for x, y, _, _ in out):
            # 📒 Lugares adds the coordinates (D-278)
            out.append((meet[0], meet[1], "📍", t.t("gremio.meet_place", name=self._zone_name(self._zone(*meet)))))
        return out

    def _gremio_goal(self, hero: Hero, gx: int, gy: int) -> bool:
        """True if (gx, gy) is one of the guild's places: a trip can go there even if never visited (_can_goto)."""
        return any((x, y) == (gx, gy) for x, y, _, _ in self._gremio_places(hero))

    # ------------------------------------------------------------------ founding the camp (D-269.3)

    def _founding_at(self, x: int, y: int) -> dict[str, Any] | None:
        """The guild founding a camp at (x, y) now, if any (from the "works_open" index)."""
        for key, entry in self.store.items("works_open"):
            if entry.get("kind") == "found":
                record = self._gremio(entry.get("ref"))
                founding = (record or {}).get("founding")
                if founding and (founding["x"], founding["y"]) == (x, y):
                    return record
        return None

    def _founding_near(self, x: int, y: int, gap: int) -> bool:
        """True if another guild is founding within `gap` zones of (x, y)."""
        for _, entry in self.store.items("works_open"):
            if entry.get("kind") == "found":
                founding = (self._gremio(entry.get("ref")) or {}).get("founding")
                if founding and max(abs(founding["x"] - x), abs(founding["y"] - y)) <= gap:
                    return True
        return False

    def _gremio_found_reqs(self, hero: Hero) -> list[tuple[str, bool]]:
        """The guild part of the founding requirements (D-269.3): lead a guild, 2 members here, the fund has the cost.

        [ES]
        Qué hace: las tres condiciones nuevas para fundar: ser líder de un gremio sin campamento, tener al menos
        gremio.found_min_members miembros del gremio presentes en la zona (contándote) y que el 💰 fondo tenga camps.found_cost.
        La llama: _camp_requirements (que suma las de siempre: Lejanía, explorada, vecinas conocidas, sin otro campamento cerca).
        Si cambia, afecta: quién puede fundar y el paso "found" del 🧭 camino guiado.
        """
        t = self.texts
        cfg = self._gremio_cfg()
        record = self._my_gremio(hero)
        leads = bool(record) and record["leader"] == hero.id
        need = int(cfg.get("found_min_members", 2))
        present = len(self._present_now(record["members"], {(hero.x, hero.y)}, hero)) if record else 0
        cost = self.content.balance["camps"]["found_cost"]
        fund = (record or {}).get("fund") or {}
        return [(t.t("camps.req_guild"), leads),
                (t.t("camps.req_members_here", n=present, need=need), leads and present >= need),
                (t.t("camps.req_fund", items=self._item_list(cost)), leads and all(fund.get(i, 0) >= n for i, n in cost.items()))]

    def _gremio_found_view(self, hero: Hero, notice: str | None = None) -> View:
        """🏕️ Fundar (from the guild): the founding in progress, or what founding here needs and 🏕️ Fundar aquí."""
        t = self.texts
        record = self._my_gremio(hero)
        if not record:
            return self._gremio_view(hero)
        founding = record.get("founding")
        actions = []
        if founding:
            zones = {(founding["x"], founding["y"])}
            present = len(self._present_now(record["members"], zones, hero))
            body = [t.t("gremio.found_progress_intro"),
                    self._work_line("gremio.founding_line", self._place_label(founding["x"], founding["y"]), founding, present),
                    t.t("gremio.found_rule", n=int(self._gremio_cfg().get("found_min_members", 2)),
                        minutes=int(self._gremio_cfg().get("found_minutes", 60)),
                        floor=int(self._gremio_cfg().get("found_floor_minutes", 10)))]
            if (founding["x"], founding["y"]) != (hero.x, hero.y):
                actions.append(Action(id=f"goask:{founding['x']}:{founding['y']}", label=t.t("gremio.site_button")))
            if hero.id == record["leader"]:
                actions.append(Action(id="gfoundx", label=t.t("gremio.found_cancel")))
        else:
            reqs = self._camp_requirements(hero)
            body = [t.t("gremio.found_intro", place=self._place_label(hero.x, hero.y)), ""]
            body += [("✅ " if ok else "▫️ ") + text for text, ok in reqs]
            body += ["", t.t("gremio.found_rule", n=int(self._gremio_cfg().get("found_min_members", 2)),
                             minutes=int(self._gremio_cfg().get("found_minutes", 60)),
                             floor=int(self._gremio_cfg().get("found_floor_minutes", 10)))]
            if hero.id == record["leader"] and all(ok for _, ok in reqs):
                actions.append(Action(id="found", label=t.t("gremio.found_here")))
        actions.append(Action(id="guild", label=t.t("menu.back")))
        return View(kind="gremio_found", title=t.t("gremio.found_title"), body=body, actions=actions, notice=notice)

    def _start_founding(self, hero: Hero) -> View:
        """🏕️ Fundar aquí: the leader, here, with the requirements met; the fund pays and the founding starts (a work).

        [ES]
        Qué hace: empieza la fundación donde está el líder (D-269.3: "donde el jefe decida"), si se cumple todo
        (_camp_requirements). El 💰 fondo paga camps.found_cost al empezar (si se cancela, vuelve al fondo). La fundación es una
        obra: necesita gremio.found_minutes × found_min_members minutos de miembros presentes (1 h con 2, 30 min con 4) y nunca
        tarda menos de found_floor_minutes. Se avisa a cada miembro (con 🧭 Ir). Reemplaza a fundar solo (D-252 ya no rige).
        La llaman: el botón "found" (🏕️ Campamento en una zona libre o 🏕️ Fundar del gremio). Si cambia, afecta:
        tests/test_camps.py (found_at) y tests/test_gremio_desde_el_inicio.py.
        """
        t = self.texts
        record = self._my_gremio(hero)
        if not record or record["leader"] != hero.id:
            return self._camp_here_view(hero, notice=t.t("camps.found_by_guild"))
        if record.get("founding"):
            return self._gremio_found_view(hero, notice=t.t("gremio.found_already"))
        if (hero.activity or {}).get("kind") == "travel":
            return self._main_view(hero, notice=t.t("activity.busy"))
        if not all(ok for _, ok in self._camp_requirements(hero)):
            return self._camp_here_view(hero, notice=t.t("camps.cannot"))
        cfg = self._gremio_cfg()
        cost = dict(self.content.balance["camps"]["found_cost"])
        for item, n in cost.items():
            record["fund"][item] -= n
            if record["fund"][item] <= 0:
                del record["fund"][item]
        now = self.clock.now()
        need = self._seconds(float(cfg.get("found_minutes", 60))) * int(cfg.get("found_min_members", 2))
        founding = {"x": hero.x, "y": hero.y, "need": need, "done": 0.0, "at": now, "started": now,
                    "floor": self._seconds(float(cfg.get("found_floor_minutes", 10))), "paid": cost}
        record["founding"] = founding
        self.store.put("gremio", record["id"], record)
        present = len(self._present_now(record["members"], {(hero.x, hero.y)}, hero))
        left = self._work_left(founding, present)
        self._works_index(f"found:{record['id']}", "found", record["id"], now + left if left is not None else None)
        x, y = hero.x, hero.y
        self._push_each([m for m in record["members"] if m != hero.id], lambda: View(
            kind="gremio_news", title=t.t("gremio.found_title"),
            body=[t.t("gremio.found_push", name=hero.name, place=self._place_label(x, y))],
            actions=[Action(id=f"goask:{x}:{y}", label=t.t("gremio.site_button")), Action(id="guild", label=t.t("gremio.button"))]))
        return self._camp_here_view(hero, notice=t.t("gremio.found_started", place=self._place_label(x, y),
                                                     time=self._fmt_duration(left) if left is not None else "—"))

    def _gremio_found_cancel(self, hero: Hero) -> View:
        """❌ Cancelar fundación (the leader): what the fund paid goes back to it."""
        t = self.texts
        record = self._my_gremio(hero)
        if not record or hero.id != record["leader"] or not record.get("founding"):
            return self._gremio_found_view(hero) if record else self._gremio_view(hero)
        for item, n in (record["founding"].get("paid") or {}).items():
            record["fund"][item] = record["fund"].get(item, 0) + n
        record["founding"] = None
        self.store.put("gremio", record["id"], record)
        self.store.delete("works_open", f"found:{record['id']}")
        self._push_each([m for m in record["members"] if m != hero.id], lambda: View(
            kind="gremio_news", title=t.t("gremio.found_title"), body=[t.t("gremio.found_cancel_push", name=hero.name)]))
        return self._gremio_found_view(hero, notice=t.t("gremio.found_cancelled"))

    def _founding_settle(self, record: dict[str, Any], actor: Hero | None) -> list[str]:
        """Advance a guild's founding with the members present; create the camp when it is done."""
        founding = record["founding"]
        present = self._advance_work(founding, record["members"], {(founding["x"], founding["y"])}, actor)
        if float(founding["done"]) >= float(founding["need"]) - EPS:
            return self._finish_founding(record, actor)
        self.store.put("gremio", record["id"], record)
        left = self._work_left(founding, present)
        self._works_index(f"found:{record['id']}", "found", record["id"], self.clock.now() + left if left is not None else None)
        return []

    def _founding_failed(self, record: dict[str, Any], actor: Hero | None, key: str) -> list[str]:
        """The founding cannot end (another camp took the place meanwhile): the fund gets back what it paid; all are told."""
        t = self.texts
        for item, n in (record["founding"].get("paid") or {}).items():
            record["fund"][item] = record["fund"].get(item, 0) + n
        record["founding"] = None
        self.store.put("gremio", record["id"], record)
        self.store.delete("works_open", f"found:{record['id']}")
        others = [m for m in record["members"] if actor is None or m != actor.id]
        self._push_each(others, lambda: View(kind="gremio_news", title=t.t("gremio.found_title"), body=[t.t(key)]))
        return [t.t(key)] if actor is not None and actor.id in record["members"] else []

    def _finish_founding(self, record: dict[str, Any], actor: Hero | None) -> list[str]:
        """The founding ended: create the camp (the guild's name, the leader founds), link the guild, invite the others.

        [ES]
        Qué hace: al terminar la fundación crea el campamento con el nombre del gremio y el líder como fundador (_create_camp:
        territorio, oleadas, 🧭 camino y 📔 diario del líder); crea el gremio del campamento (registro D-97 "guild", nivel 1, con
        "gremio" = id) y su cupo pasa a ser el del campamento (desde la 0.51, el de su etapa: 10, D-327); lo que sobró del fondo va a las obras
        del campamento ("upgrades"."fund"); a cada otro miembro le llega la invitación (✅ / ❌, "gcamp:"). Si mientras tanto otro
        campamento tomó el lugar (o el líder ya no puede), la fundación se corta y el fondo recupera lo pagado. D-291 y D-290
        (0.39): los 📢 mensajes del gremio pasan al campamento ("messages") y la ⚔️ Armería se muda con todas sus piezas.
        La llama: _founding_settle. Si cambia, afecta: tests/test_gremio_desde_el_inicio.py y tests/test_camps.py (found_at).
        """
        t = self.texts
        founding = record["founding"]
        x, y = founding["x"], founding["y"]
        key = f"{x}:{y}"
        gap = int(self.content.balance["camps"]["min_distance"])
        near = any(self.store.get("camp", f"{x + dx}:{y + dy}") for dx in range(-gap, gap + 1) for dy in range(-gap, gap + 1))
        leader_id = record["leader"]
        leader = actor if actor is not None and actor.id == leader_id else self._load(leader_id)
        if near or self._territory(x, y) or leader is None or leader.camp is not None:
            return self._founding_failed(record, actor, "gremio.found_failed")
        gid = record["id"]
        if leader is actor:
            lines = self._create_camp(leader, x, y, record["name"], gid)
        else:
            with self._speaking(leader_id):
                lines = self._create_camp(leader, x, y, record["name"], gid)
            self._save(leader)
            self._push(leader_id, View(kind="gremio_founded", title=lines[0] if lines else "", body=lines[1:]))
            lines = []
        now = self.clock.now()
        self.store.put("guild", key, {"name": record["name"], "camp": key, "founder_id": leader_id, "level": 1,
                                      "progress": {k: 0 for k in guild_rules.COUNTERS}, "created": now, "gremio": gid})
        self.store.put("guild_name", self._name_key(record["name"]), {"camp": key, "gremio": gid})
        camp_record = self.store.get("camp", key)
        if camp_record is not None:                     # D-291: the guild's 📢 messages go on in the camp's guild screen
            keep = max(1, int(self._gremio_cfg().get("messages_kept", 5)))
            camp_record["messages"] = list(record.get("messages") or [])[-keep:]
            camp_record["helpers"] = []                 # D-289: its officers become helpers as they join (_gremio_camp_answer)
            self.store.put("camp", key, camp_record)
        armory = self.store.get("armory", gid)
        if armory is not None:                          # D-290: ⚔️ the armory moves to the camp, every piece with it
            self.store.put("armory", key, armory)
            self.store.delete("armory", gid)
        leftover = record.get("fund") or {}
        if leftover:
            upgrades = self._upgrades(key)
            for item, n in leftover.items():
                upgrades["fund"][item] = upgrades["fund"].get(item, 0) + n
            self.store.put("upgrades", key, upgrades)
        others = [m for m in record["members"] if m != leader_id]
        record.update(camp=key, founding=None, fund={}, invited=others, founded_at=now)
        self.store.put("gremio", gid, record)
        self.store.delete("works_open", f"found:{gid}")
        self.store.delete("gremio_of", leader_id)
        leader_name, name = leader.name, record["name"]
        self._push_each(others, lambda: View(
            kind="gremio_camp_invite", title=t.t("gremio.camp_invite_title"),
            body=[t.t("gremio.camp_invite", leader=leader_name, name=name, place=self._place_label(x, y))],
            actions=[Action(id=f"gcamp:{gid}:y", label=t.t("gremio.camp_yes")),
                     Action(id=f"gcamp:{gid}:n", label=t.t("gremio.camp_no"))]))
        if leftover and lines:
            lines.append(t.t("gremio.fund_to_works", items=self._item_list(leftover)))
        if actor is not None and actor.id in others:
            lines.append(t.t("gremio.camp_invite", leader=leader_name, name=name, place=self._place_label(x, y)))
        return lines

    def _gremio_invite_view(self, hero: Hero, record: dict[str, Any], notice: str | None = None) -> View:
        """The guild founded its camp and you have not answered: ✅ Entrar al campamento / ❌ No, and 🏗️ go there."""
        t = self.texts
        camp = self.store.get("camp", record["camp"]) or {}
        x, y = camp.get("x", 0), camp.get("y", 0)
        body = [t.t("gremio.camp_invite", leader=camp.get("founder", "?"), name=record["name"], place=self._place_label(x, y))]
        actions = [Action(id=f"gcamp:{record['id']}:y", label=t.t("gremio.camp_yes")),
                   Action(id=f"gcamp:{record['id']}:n", label=t.t("gremio.camp_no")),
                   Action(id=self._gremio_back(hero), label=t.t("menu.back"))]
        return View(kind="gremio_camp_invite", title=t.t("gremio.camp_invite_title"), body=body, actions=actions, notice=notice)

    def _gremio_camp_answer(self, hero: Hero, action_id: str) -> View:
        """✅ / ❌ the camp's invitation after founding (the join flow of D-84 in reverse: the camp asks, the member decides).

        [ES]
        Qué hace: el miembro decide si entra al campamento que fundó su gremio ("gcamp:<gremio>:y|n"). Si entra y hay lugar
        (_members_cap: desde la 0.51, el cupo de la etapa, D-327), queda como miembro (Hero.camp); si no, sale del gremio y queda libre.
        D-289 (0.39): un oficial del gremio que entra queda de 🤝 ayudante, si hay lugar (1 por cada 5 miembros).
        Al fundador le llega la respuesta, como en _answer_join. La llama: act() (antes del combate).
        Si cambia, afecta: tests/test_gremio_desde_el_inicio.py.
        """
        t = self.texts
        parts = action_id.split(":")
        if len(parts) != 3 or parts[2] not in ("y", "n"):
            return self._main_view(hero)
        record = self._gremio(parts[1])
        if not record or not record.get("camp") or hero.id not in record.get("invited", []):
            return self._main_view(hero, notice=t.t("gremio.already_answered"))
        record["invited"].remove(hero.id)
        self.store.delete("gremio_of", hero.id)
        key = record["camp"]
        camp = self.store.get("camp", key)
        joined = (parts[2] == "y" and camp is not None and hero.camp is None
                  and len(camp["members"]) < self._members_cap(camp))
        if joined:
            camp["members"].append(hero.id)
            if hero.id in record.get("officers", []) and len(self._camp_helpers(camp)) < self._helpers_cap(camp):
                camp.setdefault("helpers", []).append(hero.id)    # D-289: an officer of the guild becomes a helper
            self.store.put("camp", key, camp)
            hero.camp = key
        else:
            record["members"] = [m for m in record["members"] if m != hero.id]
        self.store.put("gremio", record["id"], record)
        result = "joined" if joined else ("full" if parts[2] == "y" else "declined")
        if camp:
            self._push_each([camp["founder_id"]], lambda: View(kind="camp_answer", title=t.t("camps.title"),
                                                               body=[t.t(f"gremio.camp_{result}_push", name=hero.name, camp=camp["name"])]))
        return self._main_view(hero, notice=t.t(f"gremio.camp_{result}", camp=(camp or {}).get("name", record["name"])))

    # ------------------------------------------------------------------ camp works that take time (D-269.4, D-274.4)

    def _work_seconds(self, udef: dict[str, Any]) -> float:
        """Member-seconds an improvement needs once its materials are complete: minutes_per_level × level × members_ref."""
        cfg = self.content.balance.get("works", {})
        return self._seconds(float(cfg.get("minutes_per_level", 0))) * int(udef.get("level", 1)) * int(cfg.get("members_ref", 2))

    def _start_work(self, key: str, camp: dict[str, Any], uid: str, hero: Hero) -> bool:
        """Turn a complete improvement into a work in progress; False if it builds at once (works.minutes_per_level 0)."""
        need = self._work_seconds(self._upgrade_catalog().get(uid, {}))
        if need <= 0:
            return False
        record = self._upgrades(key)
        now = self.clock.now()
        record["building"][uid] = {"need": need, "done": 0.0, "at": now, "started": now, "by": hero.name,
                                   "floor": self._seconds(float(self.content.balance.get("works", {}).get("floor_minutes", 10)))}
        self.store.put("upgrades", key, record)
        return True

    def _camp_zones(self, camp: dict[str, Any]) -> set[tuple[int, int]]:
        return {(int(zx), int(zy)) for zx, zy in camp.get("zones", [[camp["x"], camp["y"]]])}

    def _works_settle_camp(self, key: str, actor: Hero | None) -> list[str]:
        """Advance every work in progress of a camp with the members present in its territory; build what is done.

        [ES]
        Qué hace: cada obra en curso ("upgrades"."building") avanza con los miembros presentes en cualquier zona del territorio
        del campamento (D-274.4); la que termina queda construida para siempre ("built") y se avisa a los miembros. Varias obras
        en curso avanzan a la vez, cada una con los mismos presentes. Actualiza el índice "works_open" (cuándo podría terminar
        la próxima). La llaman: _works_settle (botones de un miembro) y _works_tick. Si cambia, afecta: cuándo se terminan las
        mejoras (tests/test_gremio_desde_el_inicio.py).
        """
        t = self.texts
        camp = self.store.get("camp", key)
        record = self.store.get("upgrades", key) or {}
        building = record.get("building") or {}
        if not camp or not building:
            self.store.delete("works_open", f"build:{key}")
            return []
        zones = self._camp_zones(camp)
        done, etas = [], []
        for uid, work in list(building.items()):
            present = self._advance_work(work, camp["members"], zones, actor)
            if float(work["done"]) >= float(work["need"]) - EPS:
                record.setdefault("built", {})[uid] = self.clock.now()
                del building[uid]
                done.append(uid)
            else:
                left = self._work_left(work, present)
                if left is not None:
                    etas.append(self.clock.now() + left)
        record["building"] = building
        self.store.put("upgrades", key, record)
        if building:
            self._works_index(f"build:{key}", "build", key, min(etas) if etas else None)
        else:
            self.store.delete("works_open", f"build:{key}")
        lines = []
        if done:
            self._tell_waiting_room(key)                # D-294: 🛖 Cabañas may have made room
        for uid in done:
            others = [m for m in camp["members"] if actor is None or m != actor.id]
            self._push_each(others, lambda uid=uid: View(kind="camp_news", title=t.t("upgrades.built_push_title"),
                                                         body=[t.t("works.done_push", name=self._upgrade_name(uid), camp=camp["name"])]))
            if actor is not None and actor.id in camp["members"]:
                lines.append(t.t("works.done", name=self._upgrade_name(uid)))
        return lines

    def _works_refresh(self, key: str, camp: dict[str, Any], actor: Hero | None) -> None:
        """Recompute when a camp's next work could end (after one starts) without advancing anything new."""
        self._works_settle_camp(key, actor)

    def _building_lines(self, key: str, camp: dict[str, Any], hero: Hero) -> list[str]:
        """🏗️ Obras en curso of 🔨 Mejoras: one bar per work, with the members present in the territory and the time left."""
        t = self.texts
        building = (self.store.get("upgrades", key) or {}).get("building") or {}
        if not building:
            return []
        present = len(self._present_now(camp["members"], self._camp_zones(camp), hero))
        lines = ["", t.t("works.title")]
        lines += [self._work_line("works.line", self._upgrade_name(uid), work, present) for uid, work in building.items()]
        lines.append(t.t("works.rule", minutes=int(self.content.balance.get("works", {}).get("minutes_per_level", 60)),
                         floor=int(self.content.balance.get("works", {}).get("floor_minutes", 10))))
        return lines

    def _take_from_fund(self, record: dict[str, Any], need: dict[str, int], progress: dict[str, int]) -> dict[str, int]:
        """What the camp's fund gives a work; it only gives what the work lacks (D-269: what the guild's fund left at founding;
        D-291: also what the members deposit after it, with 💰 Depositar or /f02). [ES] La llaman: game.py _give_to_work y
        _feed_works. Si cambia, afecta: a dónde va el fondo del campamento."""
        fund = record.get("fund") or {}
        given: dict[str, int] = {}
        for item, n in need.items():
            give = min(n - int(progress.get(item, 0)), int(fund.get(item, 0)))
            if give <= 0:
                continue
            fund[item] -= give
            if fund[item] <= 0:
                del fund[item]
            progress[item] = int(progress.get(item, 0)) + give
            given[item] = give
        record["fund"] = fund
        return given

    # ------------------------------------------------------------------ 🤝 the founder's helpers (D-289, 0.39)

    def _member_camp(self, hero: Hero) -> dict[str, Any] | None:
        """The hero's camp if the hero is one of its members (after founding, its guild is that camp's guild, D-97)."""
        camp = self.store.get("camp", hero.camp) if hero.camp else None
        return camp if camp and hero.id in camp.get("members", []) else None

    @staticmethod
    def _camp_helpers(camp: dict[str, Any]) -> list[str]:
        """The 🤝 helpers of a camp that are still members (D-289); camps of before have none."""
        members = camp.get("members", [])
        return [h for h in camp.get("helpers") or [] if h in members and h != camp.get("founder_id")]

    def _helpers_cap(self, camp: dict[str, Any]) -> int:
        """How many 🤝 helpers a camp can have: 1 per camps.helpers_per_members members (5), never under 1 (D-289).

        [ES] Qué hace: el tope de ayudantes, máx(1, ⌈miembros ÷ 5⌉) (el dueño: "a medida que aumenta la cantidad puede
        aumentar también"). Si baja (alguien sale), los que ya son ayudantes se quedan; solo no se nombran nuevos. La llaman:
        la tarjeta del miembro, _camp_helper_toggle, _gremio_camp_answer y la línea de ayudantes. Si cambia, afecta: cuántos
        pueden activar obras, invitar y responder solicitudes (tests/test_ayudantes.py)."""
        per = max(1, int(self.content.balance["camps"].get("helpers_per_members", 5)))
        return max(1, -(-len(camp.get("members", [])) // per))

    def _camp_manager(self, camp: dict[str, Any] | None, account: str) -> bool:
        """The founder or one of its 🤝 helpers (D-289): they activate works (D-291), invite with /inv_ and answer requests.

        [ES] Qué hace: dice si esa cuenta manda en el campamento: el fundador o un ayudante que sigue siendo miembro. Renombrar,
        nombrar ayudantes y crear el gremio D-97 siguen siendo solo del fundador. La llaman: game.py (_give_to_work,
        _activate_work, _stop_work, _works_entries, _services_view, _service_type_view, _upgrades_view, _guild_view,
        _answer_join, y desde D-304 _grow_view y _grow_camp: eligen hacia dónde crece el territorio) y aquí (_invite_code,
        _camp_requests_view). Si cambia, afecta: quién activa obras, invita y agranda el territorio."""
        if not camp or account not in camp.get("members", []):
            return False
        return account == camp.get("founder_id") or account in self._camp_helpers(camp)

    def _camp_managers(self, camp: dict[str, Any]) -> list[str]:
        """The founder and the helpers: who gets the join requests and their answers (D-289)."""
        founder = camp.get("founder_id")
        return ([founder] if founder else []) + self._camp_helpers(camp)

    def _helpers_line(self, camp: dict[str, Any], hero: Hero) -> str:
        """"🤝 Ayudantes (1/1): Bram" or how the founder names them."""
        t = self.texts
        helpers = self._camp_helpers(camp)
        cap = self._helpers_cap(camp)
        if not helpers:
            return t.t("helpers.none", cap=cap)
        names = ", ".join(hero.name if h == hero.id else self._hero_name(h) for h in helpers)
        return t.t("helpers.line", n=len(helpers), cap=cap, names=names)

    def _helpers_founder_line(self, camp: dict[str, Any], hero: Hero) -> str:
        """The founder's 🤝 line in 👥 Miembros: "Asistentes: n de cap — tap a member's code" (D-304), or that they come later.

        [ES] Qué hace: al fundador le dice cuántos 🤝 asistentes tiene de su tope (_helpers_cap) y cómo nombrar uno (tocar el código
        /m2 de un miembro y elegir 🤝 Hacer asistente, en su tarjeta: _camp_member_view); con el fundador solo, que con más
        miembros podrá nombrar uno. Pedido del dueño del 20-oct-2026: "dame la opción como dueño de gremio para agregar un
        asistente". La llama: _camp_members_view. Si cambia, afecta: tests/test_ayudantes.py y tests/test_agrandar_territorio.py.
        """
        t = self.texts
        cap = self._helpers_cap(camp)
        if len(camp.get("members", [])) <= 1:
            return t.t("helpers.founder_alone", cap=cap)
        helpers = self._camp_helpers(camp)
        names = t.t("helpers.founder_names", names=", ".join(self._hero_name(h) for h in helpers)) if helpers else ""
        return t.t("helpers.founder_line", n=len(helpers), cap=cap, names=names)

    def _camp_member_line(self, n: int, account: str, camp: dict[str, Any], hero: Hero) -> str:
        """A camp member's line in 🛡️ Gremio (D-291): /m1, 👑 the founder or 🤝 a helper, online, where and doing what.

        [ES] D-327 (0.51): delante, 💤 si ya se le avisó que libera su lugar por no jugar (ladder.py _idle_warned_mark)."""
        t = self.texts
        role = (t.t("gremio.role_leader") if account == camp.get("founder_id")
                else t.t("helpers.role") if account in self._camp_helpers(camp)
                else t.t("waiting.role") if account in (camp.get("waiting") or []) else "")     # D-294: ⏳ waiting
        return self._member_row(n, account, self._idle_warned_mark(camp, account) + role, hero)   # D-327: 💤 warned

    def _camp_gave(self, camp: dict[str, Any]) -> dict[str, dict[str, int]]:
        """Who gave what to the fund: before founding (the guild's "gave") and to the camp's fund after it (D-291)."""
        out: dict[str, dict[str, int]] = {}
        sources = []
        record = self._gremio(camp.get("gremio"))
        if record:
            sources.append(record.get("gave") or {})
        sources.append((self.store.get("upgrades", f"{camp['x']}:{camp['y']}") or {}).get("gave") or {})
        for gave in sources:
            for account, items in gave.items():
                mine = out.setdefault(account, {})
                for item, n in (items or {}).items():
                    mine[item] = mine.get(item, 0) + int(n)
        return out

    def _camp_member_view(self, hero: Hero, account: str, notice: str | None = None) -> View:
        """A camp member's card (D-291): where, doing what, what they gave; the founder makes or unmakes 🤝 helpers (D-289).

        [ES] Qué hace: la tarjeta de un miembro del campamento (desde /m2 en 🛡️ Gremio): su línea, clase y nivel, lo que dio al
        fondo y los ayudantes. El fundador ve 🤝 Hacer ayudante (si hay lugar: 1 por cada 5 miembros) o ✖️ Quitar ayudante.
        D-294 (0.39): la tarjeta de quien espera lugar en el campamento (⏳); el fundador o un ayudante lo une con 🏕️ Unir al
        campamento cuando hay lugar (nunca solo). D-302 (0.39.4): su ↩️ Volver va a 👥 Miembros, donde está la lista.
        D-331 (0.55): su 🪖 escuadra y su 🎖️ jefe (y, si es de tu escuadra, sus votos para jefe: squads.py _squad_card_lines) y
        los botones 🗳️ Votar como jefe (a alguien de tu escuadra) y 🔀 Cambiar de escuadra (el jefe a los suyos; el fundador y
        los asistentes a cualquiera: _squad_card_actions); con 🤝 y ↩️, 4 botones como mucho. El código que dice es el que
        tocaste (la lista que viste por última vez: 👥 Miembros o 🪖 Escuadras). La llaman: /m1 (_member_code) y
        "gmem:<cuenta>". Si cambia, afecta: tests/test_ayudantes.py, tests/test_espera_del_gremio.py y tests/test_escuadras.py."""
        t = self.texts
        camp = self._guild_camp(hero)
        waiting = list(camp.get("waiting") or []) if camp else []
        if not camp or (account not in camp["members"] and account not in waiting):
            return self._guild_view(hero)
        order = self._camp_member_order(hero, camp) + waiting
        shown = (self.store.get("gremio_codes", hero.id) or {}).get("members") or []
        code = shown.index(account) + 1 if account in shown else order.index(account) + 1    # D-331: the /m you tapped
        data = self._hero_data(account, hero) or {}
        gave = self._camp_gave(camp).get(account) or {}
        body = [self._camp_member_line(code, account, camp, hero),
                t.t("gremio.member_class", cls=self._class_label(data), level=data.get("level", 1)),
                t.t("gremio.member_gave", items=self._item_list(gave)) if gave else t.t("gremio.member_gave_none")]
        actions = []
        if account in waiting:                          # D-294: waiting for room in the camp
            body.append(t.t("waiting.card"))
            if self._camp_manager(camp, hero.id):
                if self._camp_room(camp) > 0:
                    actions.append(Action(id=f"cwjoin:{account}", label=t.t("waiting.join_button")))
                else:
                    body.append(t.t("waiting.no_room"))
            actions.append(Action(id="gmembers", label=t.t("menu.back")))      # D-302: back to 👥 Miembros
            return View(kind="gremio_member", title=t.t("guild.title"), body=body, actions=actions, notice=notice)
        body.append(self._helpers_line(camp, hero))
        body += self._squad_card_lines(camp, hero, account)        # D-331: 🪖 their squad, its chief and the votes
        founder = camp.get("founder_id")
        if hero.id == founder and account != founder:
            helper = account in self._camp_helpers(camp)
            if helper or len(self._camp_helpers(camp)) < self._helpers_cap(camp):
                actions.append(Action(id=f"ghelp:{account}", label=t.t("helpers.remove_button" if helper else "helpers.make_button")))
            else:
                body.append(t.t("helpers.full", cap=self._helpers_cap(camp)))
        actions += self._squad_card_actions(camp, hero, account)   # D-331: 🗳️ Votar como jefe and 🔀 Cambiar de escuadra
        actions.append(Action(id="gmembers", label=t.t("menu.back")))          # D-302: back to 👥 Miembros
        return View(kind="gremio_member", title=t.t("guild.title"), body=body, actions=actions, notice=notice)

    def _camp_helper_toggle(self, hero: Hero, account: str) -> View:
        """🤝 Hacer ayudante / ✖️ Quitar ayudante: only the founder; the member is told in their language (D-289).

        [ES] Qué hace: el fundador nombra o saca a un ayudante desde la tarjeta del miembro. Nombrar solo si hay lugar
        (_helpers_cap); un ayudante nunca nombra a otro. Al miembro le llega el aviso. La llama: "ghelp:<cuenta>". Si cambia,
        afecta: tests/test_ayudantes.py."""
        t = self.texts
        camp = self._member_camp(hero)
        if not camp:
            return self._guild_view(hero)
        if camp.get("founder_id") != hero.id:
            return self._guild_view(hero, notice=t.t("helpers.only_founder"))
        if account not in camp["members"] or account == hero.id:
            return self._guild_view(hero)
        helpers = self._camp_helpers(camp)
        name = self._hero_name(account)
        if account in helpers:
            camp["helpers"] = [h for h in helpers if h != account]
            key = "removed"
        elif len(helpers) >= self._helpers_cap(camp):
            return self._camp_member_view(hero, account, notice=t.t("helpers.full", cap=self._helpers_cap(camp)))
        else:
            camp["helpers"] = helpers + [account]
            key = "named"
        self.store.put("camp", hero.camp, camp)
        camp_name = camp["name"]
        self._push_each([account], lambda: View(kind="gremio_news", title=t.t("guild.title"),
                                                body=[t.t(f"helpers.{key}_push", camp=camp_name)],
                                                actions=[Action(id="guild", label=t.t("gremio.button"))]))
        return self._camp_member_view(hero, account, notice=t.t(f"helpers.{key}", name=name))

    def _camp_requests_view(self, hero: Hero) -> View:
        """🙋 Solicitudes of the camp: the first pending request with ✅ / ❌ (the founder or a helper, D-289)."""
        t = self.texts
        camp = self._member_camp(hero)
        if not camp or not self._camp_manager(camp, hero.id) or not camp.get("requests"):
            return self._guild_view(hero)
        account = camp["requests"][0]
        data = self.store.get("hero", account) or {}
        key = f"{camp['x']}:{camp['y']}"
        body = [t.t("camps.join_body", name=data.get("name", "?"), level=data.get("level", 1), camp=camp["name"]),
                t.t("gremio.requests_count", n=len(camp["requests"]))]
        actions = [Action(id=f"join:{key}:{account}:y", label=t.t("camps.join_yes")),
                   Action(id=f"join:{key}:{account}:n", label=t.t("camps.join_no")),
                   Action(id="gmembers", label=t.t("menu.back"))]          # D-302: 🙋 lives in 👥 Miembros
        return View(kind="camp_requests", title=t.t("camps.join_title"), body=body, actions=actions)

    # ------------------------------------------------------------------ 💰 the camp's fund after founding (D-291, 0.39)

    def _fund_view(self, hero: Hero, back: str = "gfunds") -> View:
        """💰 Depositar: the guild's fund before founding, the camp's fund after it (D-291); nothing without a guild.

        [ES] Qué hace: abre la pantalla de depositar que corresponde. D-302 (0.39.4): su ↩️ Volver va a 💰 Fondos ("gfunds"),
        o a 🏘️ Servicios si vino de ahí ("gfund:svc"). La llama: _gremio_action ("gfund", "gfund:svc")."""
        if self._my_gremio(hero):
            return self._gremio_fund_view(hero)
        if self._guild_camp(hero):
            return self._camp_fund_view(hero, back=back)
        return self._gremio_view(hero)

    def _camp_fund_view(self, hero: Hero, back: str = "gfunds", notice: str | None = None) -> View:
        """💰 Fondo del campamento: what is in it, the active works it feeds (oldest first), who gave what, your codes (/f02).

        [ES] Qué hace: la pantalla de 💰 Depositar después de fundar (D-291, pedido del dueño: "una vez se crea el gremio no se
        puede perder el botón de depositar porque ahí es donde se va a depositar"). Se deposita desde cualquier lugar escribiendo
        o tocando el código de un material (/f02, como antes de fundar): pasa todo lo que llevas de eso al fondo, que le da a las
        obras activas lo que les falta, la que se activó primero antes (game.py _feed_works); lo que sobra queda en el fondo y se
        ve aquí. Muestra cada obra activa con lo que le falta, quién dio qué (antes y después de fundar) y tu mochila con códigos.
        ↩️ Volver a 💰 Fondos del campamento (D-302, _guild_funds_view: la lista con los códigos de 📦 Recursos) o a 🏘️ Servicios
        (de donde vino). La llaman: 💰 Depositar ("gfund", "gfund:svc") y _camp_deposit.
        Si cambia, afecta: tests/test_deposito_tras_fundar.py."""
        t = self.texts
        camp = self._guild_camp(hero)
        if not camp:
            return self._guild_view(hero)
        key = f"{camp['x']}:{camp['y']}"
        record = self._upgrades(key)
        fund = record.get("fund") or {}
        body = [t.t("cfund.intro"), "", t.t("cfund.line", items=self._item_list(fund)) if fund else t.t("cfund.empty")]
        works = self._active_works(camp, record)
        if works:
            perks = self._camp_perks(camp, hero)
            body += ["", t.t("cfund.active_title")]
            for n, uid in enumerate(works, 1):
                need = self._upgrade_need(self._upgrade_catalog()[uid], perks, record, uid)
                progress = dict(record["works"].get(uid, {}))
                self._credit_raw(need, progress)
                body.append(t.t("cfund.work_line", n=n, name=self._upgrade_name(uid), items=self._missing_text(need, progress) or "—"))
        else:
            body += ["", t.t("cfund.no_active")]
        gave = self._camp_gave(camp)
        if any(gave.values()):
            body += ["", t.t("gremio.fund_gave_title")]
            body += [t.t("gremio.fund_gave_line", name=hero.name if acc == hero.id else self._hero_name(acc),
                         items=self._item_list(items)) for acc, items in gave.items() if items]
        mine = self._fund_goods(hero)
        body += ["", t.t("gremio.fund_bag_title")]
        for item_id, n in mine:
            item = self.content.items[item_id]
            body.append(t.t("gremio.fund_bag_line", code=f"{int(item['code']):02d}", emoji=item["emoji"], item=t.t(item["name_key"]), n=n))
        if not mine:
            body.append(t.t("gremio.fund_bag_none"))
        return View(kind="camp_fund", title=t.t("cfund.title"), body=body, notice=notice,
                    actions=[Action(id=back if back in ("gfunds", "guild", "upsvc") else "gfunds", label=t.t("menu.back"))])

    def _camp_deposit(self, hero: Hero, camp: dict[str, Any], code: int) -> View:
        """/f02 after founding: all of that material into the camp's fund, from anywhere; then the fund feeds the works (D-291).

        [ES] Qué hace: pasa al 💰 fondo del campamento todo lo que llevas de ese material (comida no: es para la despensa), anota
        quién dio qué ("gave", para siempre; sin experiencia ni mérito, como el fondo de antes de fundar: eso lo da 🤲 Aportar) y
        el fondo alimenta las obras activas (_feed_works); si una se completa, empieza a construirse y se avisa. D-313 (0.41.1):
        después, lo que sobra llena ⏫ Siguiente nivel (game.py _feed_levelup), y si completa la lista el campamento sube. La llama:
        _fund_code. Si cambia, afecta: tests/test_deposito_tras_fundar.py y tests/test_siguiente_nivel.py."""
        t = self.texts
        item_id = next((i for i, _ in self._fund_goods(hero) if int(self.content.items[i]["code"]) == code), None)
        if item_id is None:
            return self._camp_fund_view(hero, notice=t.t("gremio.fund_no_code", code=f"/f{code:02d}"))
        key = f"{camp['x']}:{camp['y']}"
        record = self._upgrades(key)
        n = hero.backpack.pop(item_id)
        record["fund"][item_id] = record["fund"].get(item_id, 0) + n
        mine = record["gave"].setdefault(hero.id, {})
        mine[item_id] = mine.get(item_id, 0) + n
        lines = [t.t("cfund.given", items=self._item_list({item_id: n}))]
        record, fed, timed = self._feed_works(key, camp, record, hero)
        lines += fed
        record, fed = self._feed_levelup(key, camp, record, hero)     # D-313: then ⏫ Siguiente nivel, not only the works
        lines += fed
        self.store.put("upgrades", key, record)
        if timed:
            self._works_refresh(key, camp, hero)
        return self._camp_fund_view(hero, notice="\n".join(lines))

    # ------------------------------------------------------------------ 🛠️ the camp's fund for the professions (D-322, 0.47)
    # [ES] Pedido del dueño del 21-oct-2026: "que los jugadores del gremio puedan primero construir las estructuras y después
    # utilizar los recursos para las profesiones de cada uno". Primero las obras: el fondo sigue alimentando las obras activas y
    # ⏫ Siguiente nivel como siempre (game.py _feed_works y _feed_levelup), y lo que todavía les falta queda guardado (la
    # reserva). Después los oficios: lo que sobra, un miembro lo usa en las estaciones de SU campamento como si lo llevara en la
    # mochila (primero la mochila, después el fondo), con un tope por día, un registro de quién usó qué y un interruptor del
    # fundador o un 🤝 asistente (como la ⚔️ Armería, D-290). Las reglas chicas las eligió Claude (D-322, provisional).

    def _fcraft_cfg(self) -> dict[str, Any]:
        """balance.yaml "fund_crafts" (D-322): daily_cap, default_open, log_kept and log_shown."""
        return self.content.balance.get("fund_crafts", {})

    def _fund_reserve(self, camp: dict[str, Any], record: dict[str, Any], actor: Hero | None = None) -> dict[str, int]:
        """What the active works and the next level still lack, per material: the fund keeps it for them (D-322).

        [ES] Qué hace: suma lo que les falta a las obras activas (lo que pide cada una con los beneficios del campamento, menos lo
        aportado, con lo crudo de más contado como refinado: _credit_raw) y a ⏫ Siguiente nivel (camps.level_up_cost_per_level ×
        nivel, menos lo aportado); las monedas no (el fondo no guarda monedas). Eso nunca se usa para oficios. En castillo no hay
        nivel siguiente. La llaman: _fund_surplus y _fund_craft_lines. Si cambia, afecta: cuánto del fondo queda para oficios
        (tests/test_fondo_para_oficios.py)."""
        reserve: dict[str, int] = {}
        perks = self._camp_perks(camp, actor)
        catalog = self._upgrade_catalog()
        for uid in self._active_works(camp, record):
            if uid not in catalog:
                continue
            need = self._upgrade_need(catalog[uid], perks, record, uid)
            progress = dict(record["works"].get(uid, {}))
            self._credit_raw(need, progress)
            for item, n in need.items():
                lack = int(n) - int(progress.get(item, 0))
                if item != "coins" and lack > 0:
                    reserve[item] = reserve.get(item, 0) + lack
        level = int(camp.get("level", 1))
        if level < self._camp_top_level():
            given = self._lvlup_progress(record, level + 1)["given"]
            for item, n in self._lvlup_need(level).items():
                lack = int(n) - int(given.get(item, 0))
                if lack > 0:
                    reserve[item] = reserve.get(item, 0) + lack
        return reserve

    def _fund_surplus(self, camp: dict[str, Any], record: dict[str, Any], actor: Hero | None = None) -> dict[str, int]:
        """What the camp's fund holds beyond the reserve, per material (never below 0): what the professions may use (D-322)."""
        reserve = self._fund_reserve(camp, record, actor)
        surplus = {item: int(n) - reserve.get(item, 0) for item, n in (record.get("fund") or {}).items()}
        return {item: n for item, n in surplus.items() if n > 0}

    def _fund_open(self, record: dict[str, Any]) -> bool:
        """🔓 / 🔒: whether the members may use the fund for their professions (D-322); fund_crafts.default_open if never set."""
        return bool(record.get("fund_crafts", self._fcraft_cfg().get("default_open", True)))

    def _fund_cap(self) -> int:
        """Units of the fund one member may take per real day for the professions (fund_crafts.daily_cap, D-322)."""
        return max(0, int(self._fcraft_cfg().get("daily_cap", 40)))

    def _fund_used(self, record: dict[str, Any], account: str) -> int:
        """Units this member took from the fund for the professions today (a new real day starts at 0: _today)."""
        used = record.get("fund_used") or {}
        if used.get("day") != self._today():
            return 0
        return int((used.get("by") or {}).get(account, 0))

    def _fund_pool(self, hero: Hero, where: str | None) -> dict[str, Any] | None:
        """The camp's fund a member can use at the stations here (D-322), or None away from your own camp's stations.

        [ES] Qué hace: solo en el centro de TU campamento y con sus estaciones (where == "camp" de _stations_here; el 🔥 Claro no,
        y quien espera lugar en el gremio, D-294, no es miembro: no tiene estaciones del campamento) devuelve {"key", "camp",
        "record", "surplus" (lo que sobra después de la reserva), "open" (el interruptor), "left" (lo que te queda del tope de
        hoy), "usable" (lo que sobra si está abierto; vacío si está cerrado: el tope del día lo cuentan, con "left", fund_draw y
        max_times, así una receta que el fondo cubre pero el tope no dice "tope" y no "te falta")}. La llaman: game.py
        _station_view, _recipe_view y _make. Si cambia, afecta: dónde y cuánto se usa el fondo para oficios."""
        if where != "camp":
            return None
        here = self._upgrades_here(hero)
        if not here:
            return None
        camp, key = here
        record = self._upgrades(key)
        surplus = self._fund_surplus(camp, record, hero)
        is_open = self._fund_open(record)
        left = max(0, self._fund_cap() - self._fund_used(record, hero.id))
        return {"key": key, "camp": camp, "record": record, "surplus": surplus, "open": is_open, "left": left,
                "usable": dict(surplus) if is_open else {}}

    def _fund_pool_lines(self, pool: dict[str, Any] | None) -> list[str]:
        """The one line a recipe list or a recipe shows about the fund here: usable (and how much is left today), 🔒 or capped."""
        t = self.texts
        if not pool or not pool["surplus"]:
            return []
        if not pool["open"]:
            return [t.t("fcraft.list_closed")]
        if pool["left"] <= 0:
            return [t.t("fcraft.list_capped", cap=self._fund_cap())]
        return [t.t("fcraft.list_line", left=pool["left"])]

    def _fund_log(self, record: dict[str, Any], kind: str, hero: Hero, **extra: Any) -> None:
        """Add a line to 📜 Quién usó qué ("use", "open" or "close"), keeping the last fund_crafts.log_kept (D-322)."""
        keep = max(1, int(self._fcraft_cfg().get("log_kept", 20)))
        entry = {"k": kind, "who": hero.name, "id": hero.id, "at": self.clock.now(), **extra}
        record["fund_log"] = (list(record.get("fund_log") or []) + [entry])[-keep:]

    def _fund_take(self, hero: Hero, pool: dict[str, Any], draw: dict[str, int], rid: str, times: int) -> str:
        """Take `draw` out of the camp's fund for a recipe: today's count, 📜 the log, saved; the line for the maker (D-322).

        [ES] Qué hace: saca del 💰 fondo del campamento lo que la receta toma después de la mochila (el que llama ya comprobó que
        sale de lo que sobra y que no pasa el tope del día), suma esas unidades a lo que el miembro usó hoy ("fund_used": {"day",
        "by" {cuenta: n}}, se reinicia con el día real), lo anota en 📜 Quién usó qué ("fund_log") y guarda. Devuelve "💰 Del
        fondo del gremio: … · hoy llevas N de 40". La llama: game.py _make. Si cambia, afecta: el fondo y su registro."""
        record = pool["record"]
        fund = record["fund"]
        for item, n in draw.items():
            fund[item] = int(fund.get(item, 0)) - int(n)
            if fund[item] <= 0:
                del fund[item]
        today = self._today()
        used = dict(record.get("fund_used") or {})
        if used.get("day") != today:
            used = {"day": today, "by": {}}
        used["by"] = dict(used.get("by") or {})
        used["by"][hero.id] = int(used["by"].get(hero.id, 0)) + sum(int(n) for n in draw.values())
        record["fund_used"] = used
        self._fund_log(record, "use", hero, items=dict(draw), recipe=rid, times=times)
        self.store.put("upgrades", pool["key"], record)
        return self.texts.t("fcraft.took", items=self._item_list(draw), used=used["by"][hero.id], cap=self._fund_cap())

    def _fund_ago(self, at: float) -> str:
        """"1 min", "2 h 10 min" or "3 días" since a log line (D-322); never under a minute."""
        elapsed = max(0.0, self.clock.now() - float(at or 0.0))
        if elapsed >= 86400:
            return self.texts.t("fcraft.days", n=int(elapsed // 86400))
        return self._fmt_duration(max(60.0, elapsed))

    def _fund_log_lines(self, record: dict[str, Any], limit: int | None = None) -> list[str]:
        """📜 Quién usó qué, newest first: who took what for which recipe, and who opened or closed the fund (D-322)."""
        t = self.texts
        lines: list[str] = []
        for entry in reversed(list(record.get("fund_log") or [])):
            if limit is not None and len(lines) >= limit:
                break
            ago = self._fund_ago(entry.get("at", 0.0))
            kind = entry.get("k", "use")
            if kind in ("open", "close"):
                lines.append(t.t(f"fcraft.log_{kind}", name=entry.get("who", "?"), ago=ago))
                continue
            items = {i: int(n) for i, n in (entry.get("items") or {}).items() if i in self.content.items}
            rid = entry.get("recipe")
            recipe = self._recipe_name(rid) if rid in self._recipes() else "?"
            lines.append(t.t("fcraft.log_use", name=entry.get("who", "?"), items=self._item_list(items), recipe=recipe,
                             times=int(entry.get("times", 1) or 1), ago=ago))
        return lines

    def _fund_craft_lines(self, camp: dict[str, Any], record: dict[str, Any], hero: Hero) -> list[str]:
        """The 🛠️ part of 💰 Fondos del campamento: 🔓/🔒, the daily cap and your use today, what is kept and what is free (D-322).

        [ES] Qué hace: dice si el fondo para oficios está 🔓 abierto o 🔒 cerrado, el tope por día y cuánto usaste hoy, qué
        guarda el fondo para las obras activas y el nivel (lo que hay de la reserva) y qué sobra para oficios. La llama:
        _guild_funds_view. Si cambia, afecta: tests/test_fondo_para_oficios.py."""
        t = self.texts
        fund = record.get("fund") or {}
        lines = [t.t("fcraft.state_open", cap=self._fund_cap(), used=self._fund_used(record, hero.id)) if self._fund_open(record)
                 else t.t("fcraft.state_closed")]
        reserve = self._fund_reserve(camp, record, hero)
        kept = {item: min(int(n), reserve[item]) for item, n in fund.items() if reserve.get(item, 0) > 0 and int(n) > 0}
        if kept:
            lines.append(t.t("fcraft.reserved", items=self._item_list(kept)))
        if fund:
            surplus = self._fund_surplus(camp, record, hero)
            lines.append(t.t("fcraft.free", items=self._item_list(surplus)) if surplus else t.t("fcraft.free_none"))
        return lines

    def _fund_craft_toggle(self, hero: Hero) -> View:
        """🔓 Abrir / 🔒 Cerrar para oficios in 💰 Fondos: only the founder or a 🤝 assistant; written in 📜 the log (D-322).

        [ES] Qué hace: el fundador o un asistente (_camp_manager) abre o cierra el uso del fondo para oficios (el fondo sigue
        alimentando las obras y el nivel igual). Un miembro común no puede (aviso). Queda en 📜 Quién usó qué. La llama: el botón
        "gfcraft" de 💰 Fondos. Si cambia, afecta: tests/test_fondo_para_oficios.py."""
        t = self.texts
        camp = self._member_camp(hero)
        if not camp:
            return self._guild_funds_view(hero)
        if not self._camp_manager(camp, hero.id):
            return self._guild_funds_view(hero, notice=t.t("fcraft.only_managers"))
        key = f"{camp['x']}:{camp['y']}"
        record = self._upgrades(key)
        now_open = not self._fund_open(record)
        record["fund_crafts"] = now_open
        self._fund_log(record, "open" if now_open else "close", hero)
        self.store.put("upgrades", key, record)
        return self._guild_funds_view(hero, notice=t.t("fcraft.opened" if now_open else "fcraft.closed"))

    def _fund_log_view(self, hero: Hero) -> View:
        """📜 Quién usó qué: the last uses of the fund for the professions and who opened or closed it (D-322); ↩️ 💰 Fondos."""
        t = self.texts
        camp = self._guild_camp(hero)
        if not camp:
            return self._guild_funds_view(hero)
        record = self._upgrades(f"{camp['x']}:{camp['y']}")
        shown = max(1, int(self._fcraft_cfg().get("log_shown", 10)))
        lines = self._fund_log_lines(record, shown)
        body = [t.t("fcraft.log_intro", n=shown), ""] + (lines or [t.t("fcraft.log_none")])
        return View(kind="fund_log", title=t.t("fcraft.log_title"), body=body,
                    actions=[Action(id="gfunds", label=t.t("menu.back"))])

    def _fund_faq_values(self) -> dict[str, Any]:
        """{fund_cap} for ❓ Dudas and 📚 Guías (D-322)."""
        return {"fund_cap": self._fund_cap()}

    # ------------------------------------------------------------------ ⚔️ the guild's armory (D-290, 0.39)

    def _armory_cfg(self) -> dict[str, Any]:
        return self.content.balance.get("armory", {})

    def _armory_key(self, hero: Hero) -> str | None:
        """Where the hero's guild keeps its armory: the guild's id before founding, the camp's "x:y" after it."""
        record = self._my_gremio(hero)
        if record:
            return record["id"]
        camp = self._guild_camp(hero)                   # D-294: a member waiting for room uses it too
        return f"{camp['x']}:{camp['y']}" if camp else None

    def _armory(self, key: str) -> dict[str, Any]:
        data = self.store.get("armory", key) or {}
        data.setdefault("items", [])
        data.setdefault("log", [])
        data.setdefault("seq", 0)
        return data

    def _armory_label(self, entry: dict[str, Any]) -> str:
        """A piece of the armory with its marks: rarity, emoji, name, ✒️, ✨ and who signed it."""
        t = self.texts
        label = self._gear_name(entry["item"])
        if entry.get("enchant"):
            label += t.t("ench.mark")
        if entry.get("sig"):
            label += t.t("armory.signed", name=entry["sig"])
        if entry.get("wear"):                          # D-333: 🔧 a used piece says its durability
            label += " · " + self._dur_tag(entry["wear"])
        return label

    def _armory_gear(self, hero: Hero) -> list[str]:
        """The gear pieces in the backpack (never what is worn), best tier first: what can be left in the armory."""
        return sorted((i for i, n in hero.backpack.items() if n > 0 and self.content.items.get(i, {}).get("kind") == "gear"),
                      key=lambda i: (-int(self.content.items[i].get("tier", 1)), i))

    def _armory_log(self, data: dict[str, Any], kind: str, who: str, item_id: str) -> None:
        keep = max(1, int(self._armory_cfg().get("log_kept", 10)))
        data["log"] = (list(data.get("log") or []) + [{"k": kind, "who": who, "item": item_id, "at": self.clock.now()}])[-keep:]

    def _armory_view(self, hero: Hero, notice: str | None = None) -> View:
        """⚔️ Armería: the guild's shared gear chest, the last movements and your unworn pieces, with codes /t1 and /a1 (D-290).

        [ES] Qué hace: la armería del gremio (pedido del dueño, 19-oct-2026: "un botón de armamento… los miembros dejan las armas y
        armaduras que no usan y otros las toman, con registro de quién dejó o tomó qué"). Desde que existe el gremio (antes y
        después de fundar) y desde cualquier lugar: cada pieza con su código para tomarla (/t1) y quién la dejó, los últimos
        movimientos (armory.log_kept) y tu equipo sin usar con su código para dejarlo (/a1). Cabe armory.slots piezas. Todos los
        miembros pueden tomar. La llaman: ⚔️ Armería de 🛡️ Gremio ("garm"), /a1 y /t1. Si cambia, afecta: tests/test_armeria.py."""
        t = self.texts
        key = self._armory_key(hero)
        if key is None:
            return self._guild_view(hero, notice=t.t("armory.no_guild"))
        data = self._armory(key)
        cap = int(self._armory_cfg().get("slots", 30))
        body = [t.t("armory.intro"), "", t.t("armory.count", n=len(data["items"]), cap=cap)]
        items = [entry for entry in data["items"] if entry.get("item") in self.content.items]
        body += [t.t("armory.item_line", n=n, item=self._armory_label(entry), name=entry.get("by", "?"))
                 for n, entry in enumerate(items, 1)]
        if not items:
            body.append(t.t("armory.empty"))
        self._codes(hero, "arm_out", [entry["id"] for entry in items])
        if data["log"]:
            body += ["", t.t("armory.log_title")]
            body += [t.t(f"armory.log_{e.get('k', 'in')}", name=e.get("who", "?"), ago=self._ago(float(e.get("at", 0.0))),
                         item=self._gear_name(e["item"]) if e.get("item") in self.content.items else "?")
                     for e in reversed(data["log"])]
        mine = self._armory_gear(hero)
        listed = mine[:15]
        body += ["", t.t("armory.bag_title")]
        for n, item_id in enumerate(listed, 1):
            count = hero.backpack[item_id]
            body.append(t.t("armory.bag_line", n=n, item=self._gear_name(item_id) + self._enchant_mark(hero, item_id),
                            count=f" ×{count}" if count > 1 else ""))
        if not mine:
            body.append(t.t("armory.bag_none"))
        elif len(mine) > len(listed):
            body.append(t.t("armory.bag_more", n=len(mine) - len(listed)))
        self._codes(hero, "arm_in", listed)
        body += ["", t.t("armory.hint")]
        return View(kind="armory", title=t.t("armory.title"), body=body, notice=notice,
                    actions=[Action(id="guild", label=t.t("menu.back"))])

    def _armory_in_code(self, hero: Hero, n: int) -> View:
        """/a2: leave the 2nd piece of your last ⚔️ list in the guild's armory, with its ✨ and ✒️ (D-290)."""
        t = self.texts
        key = self._armory_key(hero)
        if key is None:
            return self._guild_view(hero, notice=t.t("armory.no_guild"))
        item_id = self._code_target(hero, "arm_in", n)
        if item_id is None or hero.backpack.get(item_id, 0) <= 0 or self.content.items.get(item_id, {}).get("kind") != "gear":
            return self._armory_view(hero, notice=t.t("armory.bad_code"))
        data = self._armory(key)
        cap = int(self._armory_cfg().get("slots", 30))
        if len(data["items"]) >= cap:
            return self._armory_view(hero, notice=t.t("armory.full", cap=cap))
        data["seq"] = int(data.get("seq", 0)) + 1
        enchant = (hero.gear_enchants or {}).get(item_id)
        wear = durability.take_worst(hero, item_id)    # D-333: the most worn copy goes, with its durability
        data["items"].append({"id": data["seq"], "item": item_id, "enchant": dict(enchant) if enchant else None,
                              "sig": (hero.gear_signatures or {}).get(item_id), "by": hero.name, "by_id": hero.id,
                              "at": self.clock.now(), **({"wear": wear} if wear else {})})
        hero.backpack[item_id] -= 1
        if hero.backpack[item_id] <= 0:
            del hero.backpack[item_id]
        self._forget_piece(hero, item_id)              # the last copy takes its ✨ and ✒️ with it (they travel in the entry)
        self._armory_log(data, "in", hero.name, item_id)
        self.store.put("armory", key, data)
        return self._armory_view(hero, notice=t.t("armory.left", item=self._armory_label(data["items"][-1])))

    def _armory_out_code(self, hero: Hero, n: int) -> View:
        """/t2: take the 2nd piece of the last ⚔️ list into your backpack (anyone in the guild), with its ✨ and ✒️ (D-290)."""
        t = self.texts
        key = self._armory_key(hero)
        if key is None:
            return self._guild_view(hero, notice=t.t("armory.no_guild"))
        entry_id = self._code_target(hero, "arm_out", n)
        data = self._armory(key)
        entry = next((e for e in data["items"] if e.get("id") == entry_id), None) if entry_id is not None else None
        if entry is None or entry.get("item") not in self.content.items:
            return self._armory_view(hero, notice=t.t("armory.gone"))
        item_id = entry["item"]
        if self._bag_room(hero, item_id) < 1:          # D-338 (0.62): the loose-gear cap (20) of the backpack
            return self._armory_view(hero, notice=self._bag_no_room(hero, item_id))
        holds = hero.backpack.get(item_id, 0) > 0 or item_id in hero.gear.values()
        if holds and ((entry.get("enchant") or None) != ((hero.gear_enchants or {}).get(item_id) or None)
                      or (entry.get("sig") or None) != ((hero.gear_signatures or {}).get(item_id) or None)):
            return self._armory_view(hero, notice=t.t("armory.conflict", item=self._gear_name(item_id)))   # rule 7
        data["items"].remove(entry)
        hero.backpack[item_id] = hero.backpack.get(item_id, 0) + 1
        durability.put_back(hero, item_id, entry.get("wear"), self.content.balance)     # D-333: with its durability
        if entry.get("enchant"):
            hero.gear_enchants[item_id] = dict(entry["enchant"])
        if entry.get("sig"):
            hero.gear_signatures[item_id] = entry["sig"]
        if item_id not in hero.gear_new:
            hero.gear_new.append(item_id)
        self._armory_log(data, "out", hero.name, item_id)
        self.store.put("armory", key, data)
        return self._armory_view(hero, notice=t.t("armory.took", item=self._armory_label(entry)))

    def _armory_empty_to(self, hero: Hero, key: str) -> list[str]:
        """A guild that dissolves gives every armory piece to its last member (rule 7: nothing is lost); returns the ids."""
        data = self.store.get("armory", key)
        if not data:
            return []
        pieces = []
        for entry in data.get("items") or []:
            item_id = entry.get("item")
            if item_id not in self.content.items:
                continue
            hero.backpack[item_id] = hero.backpack.get(item_id, 0) + 1
            durability.put_back(hero, item_id, entry.get("wear"), self.content.balance)     # D-333: with its durability
            if entry.get("enchant"):
                hero.gear_enchants.setdefault(item_id, dict(entry["enchant"]))
            if entry.get("sig"):
                hero.gear_signatures.setdefault(item_id, entry["sig"])
            pieces.append(item_id)
        self.store.delete("armory", key)
        return pieces

    # ------------------------------------------------------------------ ⏳ guild members waiting for room in the camp (D-294, 0.39)

    def _waiting_cap(self) -> int:
        """How many guild members can wait for room in the camp (gremio.waiting_max: 10, a fixed number the owner chose)."""
        return int(self._gremio_cfg().get("waiting_max", 10))

    def _waiting_key(self, account: str) -> str | None:
        """The "x:y" of the camp whose guild this account joined while the camp was full (D-294), or None.

        [ES] Qué hace: dice en qué campamento espera lugar esa cuenta (espacio "camp_wait": cuenta → {"camp"}), y solo si el
        campamento todavía la tiene en "waiting". La llaman: _guild_camp, _gremio_free, _guild_name_of y game.py _ask_join.
        Si cambia, afecta: quién cuenta como del gremio sin ser del campamento."""
        link = self.store.get("camp_wait", account)
        key = (link or {}).get("camp")
        camp = self.store.get("camp", key) if key else None
        return key if camp and account in (camp.get("waiting") or []) else None

    def _guild_camp(self, hero: Hero) -> dict[str, Any] | None:
        """The camp whose GUILD the hero belongs to: as a member, or waiting for room (D-294). Camp things use _member_camp.

        [ES] Qué hace: el campamento del gremio del héroe, sea miembro o espere lugar (D-294, pedido del dueño: "lo vas a invitar
        al gremio en sí… como está en el gremio, va a poder depositar para el gremio"). Todo lo del gremio usa esto (💰 fondo,
        📢 chat, ⚔️ Armería, 🗺️ zonas, 🛡️ Gremio); lo del campamento (servicios, estaciones, despensa, territorio, obras, cupo,
        oleadas, castillo) sigue mirando camp["members"]. Para un gremio de antes del campamento, _my_gremio.
        La llaman: _mates, _guild_chat, _gremio_msg_ask, _gremio_post, _member_card, _camp_member_view, _fund_view, _fund_code,
        _camp_fund_view, _armory_key y game.py _guild_view. Si cambia, afecta: qué puede hacer quien espera lugar."""
        camp = self._member_camp(hero)
        if camp:
            return camp
        key = self._waiting_key(hero.id)
        return self.store.get("camp", key) if key else None

    def _camp_room(self, camp: dict[str, Any]) -> int:
        """Free places in the camp now (its cap minus its members; who waits does not count, D-294)."""
        return max(0, self._members_cap(camp) - len(camp.get("members", [])))

    def _waiting_lines(self, camp: dict[str, Any], hero: Hero, start: int) -> list[str]:
        """🛡️ Gremio's block "⏳ Esperando lugar en el campamento" with each one's code (numbers go on after the members)."""
        t = self.texts
        waiting = list(camp.get("waiting") or [])
        if not waiting:
            return []
        lines = ["", t.t("waiting.title", n=len(waiting), cap=self._waiting_cap())]
        lines += [self._camp_member_line(start + i, account, camp, hero) for i, account in enumerate(waiting)]
        room = self._camp_room(camp)
        if room and self._camp_manager(camp, hero.id):
            lines.append(t.t("waiting.room", n=room))
        return lines

    def _camp_or_wait_invite(self, hero: Hero, camp: dict[str, Any], account: str) -> str:
        """The founder or a helper invites: into the camp if it has room, else into its guild to wait (D-294); a notice key."""
        if self._camp_room(camp) > 0:
            return self._camp_invite_send(hero, camp, account)
        return self._wait_invite_send(hero, camp, account)

    def _wait_invite_send(self, hero: Hero, camp: dict[str, Any], account: str) -> str:
        """✉️ Into the guild of a full camp (D-294): the player gets ✅ / ❌ ("cwait:"); a notice key.

        [ES] Qué hace: con el campamento lleno, el fundador o un ayudante invita al gremio a alguien sin campamento ni gremio;
        si acepta, espera lugar (camp["waiting"], tope gremio.waiting_max). La llaman: _camp_or_wait_invite (/inv_, la tarjeta
        de 👥 Jugadores y el aviso de visita). Si cambia, afecta: tests/test_espera_del_gremio.py."""
        t = self.texts
        if not self._gremio_free(account, self.store.get("hero", account)):
            return "target_busy"
        if len(camp.get("waiting") or []) >= self._waiting_cap():
            return "waiting_full"
        key = f"{camp['x']}:{camp['y']}"
        invites = camp.setdefault("wait_invites", [])
        if account not in invites:
            invites.append(account)
            self.store.put("camp", key, camp)
            who, name = hero.name, camp["name"]
            self._push_each([account], lambda: View(
                kind="camp_wait_invite", title=t.t("waiting.invite_title"),
                body=[t.t("waiting.invite_body", name=who, camp=name)],
                actions=[Action(id=f"cwait:{key}:y", label=t.t("gremio.accept")),
                         Action(id=f"cwait:{key}:n", label=t.t("gremio.refuse"))]))
        return "wait_invite_sent"

    def _wait_invite_answer(self, hero: Hero, action_id: str) -> View:
        """✅ / ❌ the guild's invitation of a full camp ("cwait:<x>:<y>:y|n"): in the guild, waiting for room (D-294)."""
        t = self.texts
        parts = action_id.split(":")
        if len(parts) != 4 or parts[3] not in ("y", "n"):
            return self._main_view(hero)
        key = f"{parts[1]}:{parts[2]}"
        camp = self.store.get("camp", key)
        if not camp or hero.id not in camp.get("wait_invites", []):
            return self._main_view(hero, notice=t.t("gremio.already_answered"))
        camp["wait_invites"].remove(hero.id)
        result = "declined"
        if parts[3] == "y":
            if not self._gremio_free(hero.id, hero):
                self.store.put("camp", key, camp)
                return self._main_view(hero, notice=t.t("gremio.already"))
            if len(camp.get("waiting") or []) >= self._waiting_cap():
                result = "full"
            else:
                camp.setdefault("waiting", []).append(hero.id)
                self.store.put("camp_wait", hero.id, {"camp": key})
                result = "accepted"
        self.store.put("camp", key, camp)
        name = camp["name"]
        self._push_each(self._camp_managers(camp), lambda: View(
            kind="camp_answer", title=t.t("camps.title"), body=[t.t(f"waiting.{result}_push", name=hero.name, camp=name)]))
        if result == "accepted":
            self._tell_waiting_room(key, hero)          # D-323: room already? then in at once
            camp = self.store.get("camp", key) or camp
            if hero.id in camp.get("members", []):
                return self._guild_view(hero, notice=t.t("waiting.joined_now", camp=name))
            return self._guild_view(hero, notice=t.t("waiting.welcome", camp=name))
        return self._main_view(hero, notice=t.t(f"waiting.{result}", camp=name))

    def _camp_join_waiting(self, hero: Hero, account: str) -> View:
        """🏕️ Unir al campamento: the founder or a helper turns a waiting guild member into a camp member, if there is room.

        [ES] Qué hace: desde D-323 (0.46.1) quien espera entra SOLO cuando hay lugar (_tell_waiting_room); este botón queda para
        el fundador o un asistente por si hace falta: desde la tarjeta de quien espera, lo une si hay lugar; desde ahí tiene también lo del campamento
        (Hero.camp). Se le avisa en su idioma. La llama: "cwjoin:<cuenta>". Si cambia, afecta: tests/test_espera_del_gremio.py."""
        t = self.texts
        camp = self._member_camp(hero)
        if not camp or not self._camp_manager(camp, hero.id):
            return self._guild_view(hero, notice=t.t("services.only_managers") if camp else None)
        key = f"{camp['x']}:{camp['y']}"
        if account not in (camp.get("waiting") or []):
            return self._guild_view(hero)
        if self._camp_room(camp) <= 0:
            return self._camp_member_view(hero, account, notice=t.t("waiting.no_room"))
        data = self.store.get("hero", account)
        camp["waiting"].remove(account)
        self.store.delete("camp_wait", account)
        if data is None or data.get("camp"):
            self.store.put("camp", key, camp)
            return self._guild_view(hero)
        camp["members"].append(account)
        data["camp"] = key
        self.store.put("hero", account, data)
        self.store.put("camp", key, camp)
        name = camp["name"]
        self._push_each([account], lambda: View(kind="camp_answer", title=t.t("camps.title"),
                                                body=[t.t("waiting.joined_push", camp=name)]))
        self._tell_waiting_room(key)
        return self._guild_view(hero, notice=t.t("waiting.joined", name=self._hero_name(account)))

    def _waiting_leave(self, hero: Hero, confirmed: bool) -> View:
        """🚪 Salir del gremio while waiting for room (asks first): what they deposited stays in the fund (D-294)."""
        t = self.texts
        key = self._waiting_key(hero.id)
        camp = self.store.get("camp", key) if key else None
        if not camp:
            return self._guild_view(hero)
        if not confirmed:
            return self._gremio_confirm("gremio.title", t.t("waiting.leave_ask", camp=camp["name"]), "gwleave!", "guild")
        camp["waiting"] = [a for a in camp.get("waiting") or [] if a != hero.id]
        self.store.put("camp", key, camp)
        self.store.delete("camp_wait", hero.id)
        name = camp["name"]
        self._push_each(self._camp_managers(camp), lambda: View(
            kind="gremio_news", title=t.t("gremio.title"), body=[t.t("waiting.left_push", name=hero.name, camp=name)]))
        return self._gremio_none_view(hero, notice=t.t("waiting.left", camp=name))

    def _tell_waiting_room(self, key: str, actor: Hero | None = None) -> None:
        """When the camp has room, who waits in its guild joins BY ITSELF, first come first in, until it is full (D-323).

        [ES] Qué hace: D-323 (orden del dueño del 21-oct-2026: "verifica que los jugadores que están en cola de espera para entrar
        en el campamento entren automáticamente cuando sube de nivel… garantiza que eso pase"; cambia D-294, que solo avisaba):
        cada vez que el campamento puede tener lugar (subir de nivel, el gremio que sube, 🛖 Cabañas, 🛏️ Literas, alguien que
        sale, al aceptar la espera o al abrir 🛡️ Gremio), los de camp["waiting"] entran solos en orden de llegada hasta llenar
        los lugares (_camp_room): pasan a miembros con Hero.camp, se les avisa en su idioma (waiting.joined_push) y al fundador y
        sus 🤝 asistentes (waiting.auto_joined_push). Quien ya no existe o ya tiene campamento sale de la espera sin ocupar lugar.
        `actor`: el héroe que está jugando ahora, si puede ser uno de los que esperan (así no se pisa con su copia en memoria).
        La llaman: game.py (_leave_camp, _level_up, _rise_guild, _complete_work, _place_furniture, _guild_view, el barrido de
        tick, _waiting_sweep) y aquí (_wait_invite_answer, _camp_join_waiting, _works_settle_camp).
        Si cambia, afecta: quién entra al campamento (tests/test_espera_del_gremio.py, tests/test_espera_entra_sola.py).
        """
        t = self.texts
        camp = self.store.get("camp", key)
        if not camp or not camp.get("waiting"):
            return
        joined: list[str] = []
        while camp.get("waiting") and self._camp_room(camp) > 0:
            account = camp["waiting"].pop(0)
            self.store.delete("camp_wait", account)
            if actor is not None and account == actor.id:
                if actor.camp:                          # already in another camp: out of the line, no place used
                    continue
                actor.camp = key
            else:
                data = self.store.get("hero", account)
                if data is None or data.get("camp"):
                    continue
                data["camp"] = key
                self.store.put("hero", account, data)
            camp["members"].append(account)
            joined.append(account)
        camp["room_told"] = 0
        self.store.put("camp", key, camp)
        if not joined:
            return
        name = camp["name"]
        self._push_each(joined, lambda: View(kind="camp_answer", title=t.t("camps.title"),
                                             body=[t.t("waiting.joined_push", camp=name)]))
        names = ", ".join(self._hero_name(a) if not (actor is not None and a == actor.id) else actor.name for a in joined)
        self._push_each([m for m in self._camp_managers(camp) if m not in joined], lambda: View(
            kind="gremio_news", title=t.t("gremio.title"), body=[t.t("waiting.auto_joined_push", names=names, camp=name)]))

    def _waiting_sweep(self) -> None:
        """Once per process: let in who waited since before D-323 where their camp already has room (the owner's order).

        [ES] Qué hace: la primera vez que corre tick() después de arrancar, revisa los campamentos con gente en espera y les
        aplica _tell_waiting_room: así entran también los que esperaban desde antes del parche. La llama: game.py tick().
        Si cambia, afecta: solo ese primer barrido."""
        if getattr(self, "_waiting_swept", False):
            return
        self._waiting_swept = True
        for key, camp in list(self.store.items("camp")):
            if camp.get("waiting"):
                self._tell_waiting_room(key)
