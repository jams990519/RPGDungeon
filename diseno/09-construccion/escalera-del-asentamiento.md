# Escalera del asentamiento: de 5 a 200 jugadores

> **Módulo** [09 · Construcción](README.md) · **Depende de:** [Fundación y cisma](../02-mundo/fundacion-y-cisma.md), [Supervivencia del asentamiento](../02-mundo/supervivencia-del-asentamiento.md), [Gremios y social](../08-social/gremios-y-social.md), [Casa propia](casa-propia.md) · **Alimenta a:** [Defensa y protecciones](defensa-y-protecciones.md), [PvP](../06-contenido/pvp.md), [Economía](../07-economia/economia.md) · **Estado:** confirmado por el dueño en lo grande (D-252, D-253 y D-254, 17-oct-2026; D-269, 18-oct, reemplaza a D-252); los números son propuesta de Claude, a medir en la beta. **En el código (0.36): el gremio desde el primer momento, fundar con el gremio y las obras con tiempo (§0); (0.41): ⏫ Siguiente nivel con su lista, 🗺️ Agrandar territorio con tope de zonas por etapa y el 🤝 asistente (§0.2, D-304); (0.49): la 🌾 cosecha de la muralla, que reemplaza el +50 % de tu territorio (§5.5, D-309 y D-325); (0.51): un solo cupo por etapa hasta castillo, los 🤝 asistentes como oficiales, quien no juega 30 días libera su lugar y el castillo con 40 activos (§0.4, D-327); (0.53): las 🌊 oleadas crecientes del castillo (§0.5, D-329); (0.56): una 🎯 misión de grupo en cada subida de nivel (§0.6, D-136 y D-332)**; las escuadras, las etapas 7 a 10, mantener el castillo y la muralla por anillos todavía no

El dueño pidió (17-oct) armar los grupos, gremios y castillos para que "empecemos con 5 jugadores y a partir de ahí vaya creciendo incluso hasta 200 jugadores". Claude le mostró tres formas; eligió **A + B** con las cuatro recomendaciones, sumó la regla de la fogata y la idea de la muralla que cosecha sola.

---

## 0. Cómo está D-269 en el juego (0.36)

El 18-oct el dueño cambió el primer escalón: "hay que empezar a crear los grupos desde el primer momento" (D-269, **reemplaza a D-252**: el grupo ya no nace al construir). Cómo se aplicó, con las lecturas de D-274 (provisional):

- **👥 Jugadores en la fogata (D-265, D-274.1-2).** En el menú de 🏕️ Campamento de la fogata del Claro, 👥 Jugadores reemplaza a 🔬 Investigar (que ahí repetía 📚 Aprender oficios; en tu propio campamento 🔬 Investigar sigue). Lista a los que jugaron en la fogata en el último minuto, con clase, nivel y gremio, cada uno con su código (/j1) que abre su tarjeta: desde ahí el líder o un oficial ✉️ invita, o tú 🙋 pides entrar al gremio del otro. Arriba, "👥 N/20 en la fogata" (N con la regla de 15 min de 📍 Zona). Desde la 0.37 hay 9 🔥 fogatas (antes «hogueras», D-311), cada una con su 👥 Jugadores y su "N/20", y una llena reparte a los que llegan (D-265, D-277).
- **El gremio antes del campamento (D-269.1-2).** Cualquier héroe lo crea por 🥉20 con un nombre libre (que será el del campamento: es único entre gremios y campamentos). Un gremio por héroe. Caben **5**. Se entra pidiendo (desde 🔎 Buscar gremio o la tarjeta de un jugador) y acepta el **líder o un oficial**; el líder nombra oficiales, saca miembros y cede el liderazgo; cualquiera sale (si sale el último, el gremio se disuelve y el fondo vuelve a su mochila). Sirve para:
  - **ver a los miembros:** dónde está cada uno (zona y coordenadas), qué hace y si está en línea (🟢 con la regla de 15 min);
  - **📢 mensajes al gremio:** el texto le llega a cada miembro (hasta 200 letras; la pantalla guarda los últimos 5);
  - **💰 el fondo:** cada miembro deposita desde donde esté escribiendo o tocando el código de un material (/f02, el número de 📦 Recursos): "no tienen que llevarlo a ningún lugar". Se ve el total y quién dio qué.
- **📍 Punto de reunión y 🏗️ Moverte a la construcción.** El líder marca "📍 Punto de reunión: aquí" y se avisa a todos. Mientras el gremio tiene un lugar definido (el punto de reunión o la fundación en curso), cada miembro ve en 📍 Zona un botón ancho más, **🏗️ Moverte a la construcción** (pedido del dueño, 18-oct: "lo que te tomes realmente en llegar. No te mueves en diagonal"): pregunta "¿Viajar?" y el héroe va solo por el camino de verdad, primero este-oeste y después norte-sur, aunque nunca haya pisado esa zona. No sale si ya estás ahí, ni cuando el campamento ya está fundado y eres miembro.
- **Fundar con el gremio (D-269.3).** El líder funda donde está, con **al menos 2 miembros del gremio presentes** en la zona; siguen las reglas de siempre (Lejanía 2 o más, la zona explorada al 100 %, 4 vecinas conocidas, sin otro campamento a 2 zonas). El **fondo paga** `camps.found_cost` al empezar. Fundar es una **obra en curso**: tarda **60 min con 2 presentes** y menos con más (tiempo = 60 × 2 ÷ presentes: 4 → 30 min), **nunca menos de 10 min**; con 1 presente, el doble; sin nadie, se pausa. Al terminar nace el campamento con el **nombre del gremio** y el líder como fundador; el gremio pasa a ser **el gremio del campamento** (el de D-97, nivel 1, cupo 5) y **a cada otro miembro le llega la invitación**: decide si entra. Lo que sobró del fondo va a las obras del campamento (se pone primero al aportar).
- **Las obras con tiempo (D-269.4, D-274.4).** Cada 🔨 mejora, con sus materiales completos, pasa a 🏗️ obra en curso: **60 min × su nivel con 2 miembros dentro del territorio** del campamento (en cualquiera de sus zonas), con 1 el doble, nunca menos de 10 min, sin nadie en pausa. 🔨 Mejoras muestra cada obra con su barra, los presentes y lo que falta. Lo que ya estaba construido sigue construido.
- **Lo que no cambió:** los campamentos y gremios de antes siguen igual (D-64); el gremio del campamento sube de nivel como siempre (D-97). Dónde está el código: `engine/service/gremio.py`; los números, en `content/balance.yaml` (`gremio`, `works`, `bonfire`); la cascada, en el [mapa de impacto](../01-plataforma/mapa-de-impacto.md) C-30.
- **Lo que decidió Claude y espera al dueño (D-276, provisional):** varias obras en curso avanzan a la vez con los mismos presentes; con 1 solo presente la fundación también avanza (el doble de lento); la reparación de defensas, los muebles, los estudios y ⬆️ Agrandar siguen siendo al instante; el fondo recibe solo materiales (no comida ni monedas); después de fundar, los 📢 mensajes, el fondo y el punto de reunión quedan para los gremios sin campamento (el del campamento es la pantalla de D-97).

---

## 0.1 Las obras del campamento desde la 0.39 (D-287, D-288, D-291, D-295)

- **🏘️ Servicios por tipo (D-288):** un botón por tipo de obra: 🏠 Casas (pozo, refugio, granero, ahumadero, cabañas, huerto, enfermería), ⚒️ Oficios (fogón, puesto de trueque y un edificio por oficio), 🛡️ Defensas y 📚 Saber (biblioteca). Cada tipo muestra lo construido con su botón de uso, las obras activas con lo que falta y las que esperan que las activen.
- **Un edificio por oficio (D-288):** 🪚 Aserradero, 🧶 Tejeduría y 🗿 Cantería (nivel 1); 🪣 Curtiduría, 💧 Alambique y 🏭 Fundición (2); 🪑 Carpintería y 🪡 Sastrería (3); 🦺 Peletería, ⚗️ Laboratorio de alquimia y 🩺 Botica (4); 🔨 Forja y 💍 Joyería (5). El 🧵 Taller y la Herrería se retiraron: quien ya los tenía conserva todas sus estaciones.
- **Lo que pide cada nivel, dicho entero (D-313, 0.41.1):** ⬆️ Mejorar y ⏫ Siguiente nivel listan cada obra y cada material con lo que le falta; 📜 Qué pide cada nivel muestra todas las subidas hasta castillo; lo depositado en 💰 Fondo llena el nivel después de las obras activas.
- **Obras que se activan (D-291):** todos ven las obras del nivel de su campamento; solo el fundador o un 🤝 asistente (antes "ayudante", D-304) toca ▶️ Activar (o ⏹️ Quitar, si nadie le dio nada), y todos aportan a las activas. Lo que estaba empezado antes de la 0.39 quedó activo solo.
- **Lo que no es de tu nivel no se ve (D-287):** las obras de niveles más altos, 🔬 Investigar sin 📚 Biblioteca y los avisos de "se abre al nivel X" ya no aparecen.
- **Cada obra nueva cuesta más (D-295):** un 15 % más por cada obra ya construida, con el precio fijo al activarla.

## 0.2 ⬆️ Mejorar campamento desde la 0.41 (D-304)

El dueño pidió (20-oct): "ponme en el botón de mejorar dos opciones: una, siguiente nivel, y dos, agrandar territorio… debes de construir esto, esto y esto a tal nivel para poder pasar al siguiente nivel, más los recursos que sean necesarios, en formato de lista. Y se va a ir completando". Y, el mismo día: "cada mejora debe ser visible para todos los miembros… dame la opción como dueño de gremio para agregar un asistente… que pueda definir hacia dónde va a avanzar el territorio junto contigo".

- **El nivel y las zonas van por separado.** Antes cada ⬆️ Agrandar sumaba 1 nivel y 1 zona (nivel = zonas, D-81). Ahora el nivel sube con ⏫ Siguiente nivel y las zonas con 🗺️ Agrandar territorio. Los campamentos de antes conservan su nivel y sus zonas (D-64).
- **🏰 Gestionar → ⬆️ Mejorar campamento:** el nivel y la etapa, las zonas usadas de su tope y cuántos requisitos del nivel siguiente están listos; dos botones: ⏫ Siguiente nivel y 🗺️ Agrandar territorio.
- **⏫ Siguiente nivel:** "Para subir a nivel N te falta:" y una lista con ✅ (listo) o ▫️ (falta) que se va llenando:
  - 🏗️ **Construir:** las obras que tienen que estar construidas (las elige Claude, provisional, `camps.level_up`; cada una es del nivel que el campamento ya tiene, así se ve y se activa). Si no, dice si está 🏗️ en obra, 🔨 activa o ⏸️ sin activar.
    Desde la 0.45.1 (D-319, provisional) lo que piden esas obras se hace con **rango 10 o menos** (15 las del paso a castillo), sin 🎓 especialización, sin 📚 libro y sin título comprado: la 🏥 Enfermería pide 🛏️ Literas (Carpintería 10), ungüentos y vendas; las 🏹 Torres, un 🗄️ Armero (Carpintería 15). Con 5 a 10 miembros que dan el 75 % de su energía, el castillo llega en unos 17,6 días y un carpintero dedicado llega a tiempo a cada nivel (`python tools/camp_costs.py`; [balance](../03-personaje/balance.md) §7, 0.45.1).
  - 📦 **Recursos:** 🪵 30, 🪨 20 y 🌿 10 por el nivel actual, con lo aportado (por ejemplo "🪵 Madera 12/30"); desde el nivel 6, 🪎 cofres (D-92: 1, 2 y 3; antes los pedía agrandar).
  - 🏰 **Para castillo (8 → 9):** el gremio listo (D-97), las 15 mejoras construidas (D-101) y la 🌙 Noche de prueba ganada (D-99, con su botón cuando es lo único que falta).
  - 🌾 Con la despensa vacía, una línea más: el campamento no sube (D-93).
  - Cualquier miembro aporta con **🤲 Aportar** (lo que hay en el 💰 fondo del campamento va primero; nunca toma de más; da experiencia, mérito y 🏗️ Construcción como las obras). Si el último aporte completa la lista, el campamento **sube en ese momento**; si lo último fue terminar una obra, cualquier miembro toca **⏫ Subir a nivel N**. Al subir se avisa a todos y caben 2 miembros más (desde la 0.51, el cupo es el de la etapa: §0.4). En castillo todavía no hay otro nivel.
- **🗺️ Agrandar territorio:** las zonas usadas de su tope, el costo (de tu mochila: lo de antes, 🪵15 🪨10 🌿5, por las zonas que ya tiene, sin cofres), un **minimapa de 5 × 5** centrado en el campamento (🏕️ el centro, 🟩 lo tuyo, 1️⃣ 2️⃣ las zonas de esta página, 🔸 otras libres, ⬛ de otro) y una línea por zona libre con su **dirección** (⬆️ Norte, ↗️ Noreste… el norte suma a la y) y los recursos que conoces. **La eligen el fundador o un 🤝 asistente**; los demás ven todo. Sumar una zona no sube el nivel.
- **Tope de zonas por etapa** (la tabla de E-218, confirmada): campamento **3** · aldea **5** · pueblo **9** · ciudad **15** · castillo **25**. Al tope: "sube de nivel para agrandar más". Quien ya tenía más, las conserva.
- **🤝 Asistentes:** el ayudante de D-289 se llama asistente en los textos (1 cada 5 miembros, como antes). Activa obras, elige hacia dónde crece el territorio, invita y acepta solicitudes. En 🛡️ Gremio → 👥 Miembros el fundador ve cuántos tiene y cómo nombrar uno (tocar el código /m2 de un miembro → 🤝 Hacer asistente). Desde la 0.51 son los oficiales de D-253.4 (§0.4).
- **Todo visible para todos:** 🔨 Mejoras nombra a cada miembro las obras de su nivel que siguen sin activar, muestra las activas con su barra y las 🏗️ en obra con su tiempo, y dice "⏫ Nivel N: x de y listos". La lista de ⏫ la ve cualquier miembro.
- **Dónde está:** `engine/service/game.py` (`_improve_view`, `_lvlup_rows`, `_lvlup_view`, `_lvlup_give`, `_lvlup_go`, `_level_up`, `_grow_view`, `_grow_camp`, `_territory_map`), `engine/service/gremio.py` (`_helpers_founder_line`); los números en `content/balance.yaml` (`camps.level_up`, `level_up_cost_per_level`, `zones_by_stage`, `territory_map_radius`, `grow_cost_per_level`, `chests_*`); los textos en `content/locales/es_nivel.yaml` y `en_nivel.yaml`; la cascada en el [mapa de impacto](../01-plataforma/mapa-de-impacto.md).

## 0.3 💰 El fondo del gremio: primero las obras, después los oficios (0.47, D-322)

El dueño pidió (21-oct): "diseña para que los jugadores del gremio puedan primero construir las estructuras y después poder utilizar los recursos para las profesiones de cada uno. Puedan utilizar los recursos del gremio". Cómo quedó (D-322, provisional):

- **Primero las obras.** Lo depositado con 💰 Depositar (/f02) sigue yendo a las obras activas (la que se activó primero, antes) y después a ⏫ Siguiente nivel, como desde la 0.39 y la 0.41.1 (D-291, D-313). Lo que todavía les falta de cada material es la **reserva**: queda guardado para ellas y nunca se usa para oficios. La reserva se cuenta cada vez, así una obra que se activa mañana también queda cubierta.
- **Después los oficios.** Lo que **sobra** (fondo − reserva, por material) lo usa cualquier miembro en las **estaciones de su campamento** (en el centro, con sus edificios de oficio; no en las 🔥 fogatas): al refinar, fabricar o cocinar, la receta toma primero de la mochila y lo que falta, del fondo, como si lo llevara. En la lista de recetas (/r1) sale **✅💰** lo que puedes hacer con ayuda del fondo; cada receta dice cuánto pondría el fondo ("+💰3" en cada material y "💰 Del fondo del gremio, por vez: …"). Todo o nada, como siempre.
- **Control (como la ⚔️ Armería, D-290):** cada miembro toma como mucho **40 unidades por día real** (`fund_crafts.daily_cap`, todos los materiales juntos); **📜 Quién usó qué** (en 🛡️ Gremio → 💰 Fondos) dice quién tomó qué y para qué receta, y quién abrió o cerró (los últimos 20; se ven 10); el fundador o un 🤝 asistente tiene el interruptor **🔓 abierto / 🔒 cerrado** en 💰 Fondos (empieza abierto). Solo los miembros del campamento: quien espera lugar en el gremio (D-294) o un visitante no tiene las estaciones del campamento.
- **💰 Fondos del campamento** dice, además de cada recurso con su código, si el fondo para oficios está abierto, el tope y lo que usaste hoy, qué está **guardado para las obras y el nivel** y qué **sobra para oficios**. Botones: 💰 Depositar · 📜 Quién usó qué · 🔒 Cerrar / 🔓 Abrir para oficios (fundador o asistente) · ↩️ Volver.
- **El 🏛️ Mercado no cambia:** el fondo no se vende ahí (D-320); lo que un miembro fabrica con el fondo es suyo, como todo lo que fabrica.
- **Dónde está:** `engine/service/gremio.py` (`_fund_reserve`, `_fund_surplus`, `_fund_pool`, `_fund_take`, `_fund_craft_lines`, `_fund_craft_toggle`, `_fund_log_view`), `engine/service/game.py` (`_recipe_status`, `_station_view`, `_recipe_view`, `_make`), `engine/professions/rules.py` (`fund_draw`, `max_times`); los números en `content/balance.yaml` → `fund_crafts`; lo guardado en `upgrades/<x:y>` (`fund_crafts`, `fund_used`, `fund_log`). Preguntas abiertas: P-251 a P-254 (E-240 a E-243).

**De dónde sale:** el banco de gremio de *World of Warcraft* (pestañas con permisos y un tope de retiros por día para cada rango, con su registro) y el almacén común de *Chat Wars*, donde el gremio junta para construir y los artesanos toman lo que sobra.

## 0.4 La escalera en el juego, 1.ª parte (0.51, D-253; cómo se aplicó: D-327)

La prioridad de lo grande es el asentamiento por etapas y el castillo (D-310). La 0.51 trae lo de D-253 que no necesita escuadras ni etapas nuevas; lo que decidió Claude está en D-327 (provisional) y se le pregunta al dueño (E-253 a E-256).

- **👥 Un solo cupo por etapa (D-253.1, Forma A).** Se acabó el doble cupo (el del campamento, 2 + 2 por nivel, y el del gremio, 4 a 30, donde ganaba el mayor). Cómo se repartió la tabla del §2 en los niveles de hoy:

| Etapa de la escalera | En el juego | Cupo |
|---|---|---|
| 1 · Casa | el gremio antes del campamento (D-269) | 5 |
| 2 · Campamento | niveles 1 y 2 | 10 |
| 3 · Aldea | niveles 3 y 4 | 15 |
| 4 · Pueblo | niveles 5 y 6 | 25 |
| 5 · Ciudad | niveles 7 y 8 | 40 |
| 6 · Castillo | nivel 9 | 50 |

  - El nivel del gremio (D-97) **ya no da lugares**; sigue subiendo y el castillo todavía pide nivel 5.
  - Las 🛖 Cabañas (+2) y las 🛏️ Literas (+1) **suman encima**: quien las construyó no pierde su efecto.
  - **Nadie pierde lugar (D-64):** la primera vez que el juego ve un campamento de antes, guarda su cupo viejo como piso (`cap_floor`); por ejemplo, una aldea con gremio de nivel 6 tenía 20 y sigue con 20 hasta que la etapa da más. Si un campamento tiene más miembros que su cupo, nadie sale por eso.
  - **Cuando el cupo sube** (al pasar de etapa, y el día del parche en los campamentos que ganaron lugar), quien espera lugar en el gremio entra solo, en orden de llegada (D-323).
  - ⏫ Siguiente nivel dice "Al subir: 👥 caben 15 (hoy 10)…" o, si el nivel siguiente es de la misma etapa, que el cupo crece en la etapa siguiente.
- **🤝 Los oficiales son los asistentes (D-253.4).** Desde la 0.39 los 🤝 asistentes (D-289, D-304) aceptan o rechazan a quien pide entrar, invitan con /inv_, activan obras y eligen hacia dónde crece el territorio. Se tomaron como los oficiales: una sola lista y un solo botón (🛡️ Gremio → 👥 Miembros → el código de un miembro → 🤝 Hacer asistente), con el tope que eligió el dueño, **1 cada 5 miembros** (D-289), mientras no haya escuadras (D-253.4 hablaba de 1 cada 2 a 4 escuadras). Antes del campamento, el líder nombra ⭐ oficiales como siempre, y al fundar pasan a asistentes.
- **💤 Quien deja de jugar libera su lugar (D-253.3).**
  - A los **25 días** sin jugar le llega "en 5 días liberas tu lugar en …", con un botón; tocar cualquier botón lo deja adentro y la cuenta vuelve a empezar.
  - A los **30 días** (y siempre 5 días o más después del aviso) sale del gremio y del campamento y su lugar queda libre: entra quien espera, y al fundador y a sus asistentes les llega quién salió.
  - **Nunca el fundador.** Conserva su héroe, su mochila, su equipo, sus oficios y su progreso; lo que dio a las obras y al fondo queda en el campamento; puede volver a pedir entrar.
  - "Jugar" es tocar un botón o escribir un comando (`Hero.seen_at`, la misma marca de la despensa y de 👥). **La cuenta empieza con el parche:** vale lo más nuevo entre esa marca y la primera vez que el juego vio al miembro en ese campamento, así nadie sale por días de antes (nadie puede salir antes del 20-nov) ni quien no tenía marca.
  - Solo los miembros del campamento: en el gremio sin campamento el líder ya puede 🚫 sacar a alguien, y quien espera lugar (D-294) no ocupa lugar.
  - 👥 Miembros dice la regla en una línea y marca con 💤 a quien ya fue avisado. Corre desde `tick()`, cada 60 min.
  - **Cambió la regla 10 del servicio** (`game.py`): "el cupo nunca saca a nadie; solo sale quien no juega 30 días, nunca el fundador".
- **🏰 Castillo (D-253.2, D-122).** El paso 8 → 9 pide, además de lo de siempre (las obras, los materiales, los cofres, el gremio de nivel 5 y las 15 mejoras):
  - **"👥 Activos esta semana: N de 40"**: miembros que jugaron en los últimos 7 días; reemplaza a "10 miembros o más". La ciudad tiene cupo para 40 (más Cabañas y Literas): hacen falta casi todos activos la misma semana.
  - la 🌙 Noche de prueba con **10 vencedores distintos** como mínimo (antes 2; cada miembro pelea una vez).
  - **Queda para después:** las 5 oleadas crecientes de D-122 ("si pierde más de las que gana, no aprueba"), que son una pieza grande (una serie de oleadas que crecen, se cuentan y se aprueban; P-79). *Llegaron en la 0.53 (§0.5).*
- **Lo que no entra en esta parte:** las escuadras de 5 con su jefe (Forma B, §3), las etapas 7 a 10 con sus mejoras nuevas y la muralla por anillos (§5.2).
- **Dónde está:** `engine/service/ladder.py` (`LadderMixin`: `_base_cap_at`, `_cap_floor_sweep`, `_idle_tick`, `_idle_camp`, `_idle_release`, `_castle_active_row`), `engine/service/game.py` (`_members_cap`, `_members_cap_at`, `tick`, `_create_camp`, `_castle_needs`, `_lvlup_view`, `_level_up`), `engine/service/gremio.py` (`_camp_members_view`, `_camp_member_line`); los números en `content/balance.yaml` → `camps.members_by_stage`, `ladder` (`idle_warn_days`, `idle_release_days`, `idle_scan_minutes`, `castle_active`, `active_days`) y `raids.trial.min_wins`; lo guardado en `camp/<x:y>` (`cap_floor`, `idle_watch`, `idle_warned`) y `meta/idle`; los textos en `content/locales/es_escalera.yaml` y `en_escalera.yaml`; ❓ /d37 y /d42; las pruebas en `tests/test_escalera_cupo_oficiales.py`; la cascada en el [mapa de impacto](../01-plataforma/mapa-de-impacto.md) C-35.
- **Preguntas para el dueño:** E-253 a E-256 (P-264 a P-267).

## 0.5 Las 🌊 oleadas crecientes del castillo (0.53, D-122; cómo se aplicó: D-329)

D-122 (confirmada) pide que, antes del castillo, el campamento "defienda su estructura anterior durante varias oleadas que van creciendo: si pierde más de las que gana, no aprueba". Los números los propone Claude (D-329, provisional) y se le preguntan al dueño (E-260 a E-262).

- **Cuándo:** mientras el campamento está en el nivel 8 (la ciudad, el paso a castillo), sus oleadas de siempre (3 por semana, D-154) son una **serie de 5**. Empiezan solas con la primera oleada después de llegar al nivel 8, sin botón, y corren en paralelo con lo demás del castillo.
- **Cómo crecen:** cada una suma un 20 % a la vida y al ataque de una oleada normal.

| Oleada | 1.ª | 2.ª | 3.ª | 4.ª | 5.ª |
|---|---|---|---|---|---|
| Fuerza contra una oleada normal | ×1,2 | ×1,4 | ×1,6 | ×1,8 | ×2,0 |

  La 🛡️ Defensa del campamento las frena después, como a todas (D-101). Cada oleada daña las defensas (D-115), así que conviene repararlas entre una y otra.
- **Cuándo aprueba:** con **3 ganadas**. La serie termina apenas se decide:
  - con 3 ganadas queda aprobada para siempre, y las oleadas vuelven a ser normales;
  - con 3 perdidas ya no se puede: se pierde y vuelve a empezar desde la 1.ª después de **3 días** (se salta una oleada normal).
- **Qué cuesta perder:** lo de cualquier oleada perdida (el 25 % de la despensa y −2 de 🛡️ Defensa hasta reparar). Nada más.
- **Se ve:**
  - en ⏫ Siguiente nivel: "🌊 Oleadas crecientes: 2 ganadas, 1 perdida de 5 (hace falta ganar 3; quedan 2)" y, mientras faltan, una línea que explica cómo llegan;
  - en el aviso, en la pelea y en la pantalla del campamento: "🌊 Oleada creciente 2 de 5 (+40 %)";
  - en el parte de cada oleada, que les llega a todos los miembros en su idioma: cómo va la serie;
  - en 📜 Qué pide cada nivel, en ❓ /d39 y /d42 y en 📚 Guías → 🏕️ Campamento.
- **La 🌙 Noche de prueba y las oleadas** se hacen en cualquier orden: si solo faltan esas dos, ⏫ muestra el botón 🌙.
- **Nadie pierde (D-64):** un castillo que ya existe no recibe oleadas crecientes; solo traban el paso a castillo.
- **Mantener el castillo** ("después hay que mantener la estructura") queda para después (E-262, P-273).
- **Cuánto cuestan** (medido con las funciones de `tools/sim.py`: un defensor atento, con equipo poco común y de 3 a 8 niveles sobre el enemigo de la oleada (zonas de nivel 10 y 20)):

| Fuerza | Sin defensas | Con 6 puntos de 🛡️ | Con los 11 |
|---|---|---|---|
| ×1,2 (1.ª) | 87-100 % | 100 % | 100 % |
| ×1,6 (3.ª) | 36-77 % | 85-100 % | 100 % |
| ×2,0 (5.ª) | 9-33 % | 43-86 % | 94-100 % |

  Como cada oleada pide que gane la mitad de los activos, con muchos defensores lo que cuenta es si cada uno gana más de la mitad de las veces: con las defensas construidas y reparadas se aprueba; sin ellas, la 4.ª y la 5.ª se pierden casi siempre.
- **Dónde está:** `engine/service/ladder.py` (la sección de las oleadas crecientes), `engine/world/raids.py` (`wave_mult`, `series_outcome`) y los ganchos de `engine/service/game.py` (`_open_raid`, `_raid_notice`, `_defend`, `_resolve_raid`, `_raid_lines`, `_lvlup_rows`, `_lvlup_view`, `_lvlup_all_view`); los números en `content/balance.yaml` → `ladder.castle_waves` (`count` 5, `pass_wins` 3, `growth` 0,2, `retry_days` 3); lo guardado en `camp/<x:y>` → `castle_waves` y, en la oleada abierta, `wave` y `wave_mult`; los textos en `content/locales/es_escalera.yaml` y `en_escalera.yaml`; las pruebas en `tests/test_oleadas_crecientes_castillo.py`; la cascada en el [mapa de impacto](../01-plataforma/mapa-de-impacto.md) C-35.
- **Preguntas para el dueño:** E-260 a E-262 (P-271 a P-273).

## 0.6 Las 🎯 misiones de grupo de cada subida (0.56, D-136; cómo se aplicó: D-332)

D-136 (confirmada) pide que "para abrir cada nivel del campamento el grupo cumpla misiones juntos (farmear, recolectar, llenar la despensa); al terminarlas se abren el siguiente rango de misiones, el crecimiento y los materiales". La tabla del §2 las nombra en el campamento (la 1.ª), la aldea (la 2.ª) y la ciudad (la 4.ª). Cómo quedó lo eligió Claude (D-332, provisional) y se le pregunta al dueño (E-269 a E-271).

- **Una por subida.** Cada subida de nivel (1 → 2 … 8 → 9) pide, además de sus obras, sus materiales y lo del castillo, una **misión de grupo**: una meta para todos los miembros juntos, con lo de cada uno sumado, esté donde esté. Al subir empieza la del nivel siguiente ("el siguiente rango de misiones" de D-136).

| Subida | Misión (con 1 activo) | De la escalera |
|---|---|---|
| 1 → 2 (campamento) | ⚔️ vencer 20 monstruos | la 1.ª misión del campamento |
| 2 → 3 (aldea) | 🪵 juntar 60 de madera | la 2.ª misión, la de la aldea |
| 3 → 4 | 🌾 llevar 20 raciones a la despensa (existe desde el nivel 3) | |
| 4 → 5 (pueblo) | 🛡️ ganar 3 peleas de oleada (🛡️ Defender) | las "3 oleadas ganadas" del pueblo |
| 5 → 6 | ⚔️ vencer 40 monstruos | |
| 6 → 7 (ciudad) | 🪨 juntar 100 de piedra | la "4.ª misión" de la ciudad |
| 7 → 8 | 🌾 llevar 40 raciones a la despensa | |
| 8 → 9 (castillo) | ⚔️ vencer 80 monstruos | |

  La escalera hablaba de una por etapa, pero en el juego cada etapa tiene 2 niveles y D-136 dice "cada nivel": por eso son 8 (E-269).
- **Cuánto piden.** La meta crece con el nivel y, poco, con los miembros activos (los que jugaron en los últimos 7 días): un 15 % de la meta por cada activo después del primero, contando como mucho 40. Queda **fija al empezar** (al fundar, la 1.ª; al subir, la siguiente): si entra o sale gente, no cambia.

| Activos | 1 | 5 | 10 | 25 | 40 |
|---|---|---|---|---|---|
| Vencer monstruos (→ 2) | 20 | 32 | 47 | 92 | 137 |
| Peleas de oleada (→ 5) | 3 | 5 | 8 | 14 | 21 |
| Vencer monstruos (→ 9) | 80 | 128 | 188 | 368 | 548 |

  Cuanto más son, menos pone cada uno (con 10 activos, unas 5 peleas cada uno para el nivel 2).
- **Qué cuenta.** Lo mismo que los encargos semanales del campamento (0.20), con el mismo gancho: cada pelea ganada (🏹 Cazar, explorar, oleadas, mazmorras), cada unidad que se junta del recurso pedido, cada ración de 🌾 Aportar comida y, para las de oleada, cada pelea ganada con 🛡️ Defender. Solo los miembros del campamento (no quien espera lugar ni un visitante), desde que empieza la misión.
- **Se ve.** En ⏫ Siguiente nivel, bajo "🤝 Entre todos:", la línea "🎯 Misión de grupo: vencer 20 monstruos — 7 de 20 (faltan 13)" y otra con qué cuenta, cuánto llevas tú y el premio; también en ⬆️ Mejorar, en "x de y listos" de 🔨 Mejoras, en 📜 Qué pide cada nivel (las siguientes, con los activos de hoy), en el 📜 Tablón (debajo de los encargos de la semana, con lo tuyo), en el aviso al fundar y al subir ("🎯 Nueva misión de grupo para subir a nivel 3…"), en ❓ /d36 y en 📚 Guías → 🏕️ Campamento.
- **Al cumplirla.** Se cierra una sola vez. El 💰 fondo del campamento recibe un **premio chico: 🪵6 🪨4 🧵2 × el nivel que deja** (el 20 % de los materiales de esa subida; de 🪵6 🪨4 🧵2 en la primera a 🪵48 🪨32 🧵16 en la del castillo), que toman las obras y ⏫ como todo lo del fondo (§0.3); nunca va a la mochila de nadie. A cada otro miembro le llega el aviso en su idioma, con lo que puso. **No sube sola:** si era lo último de la lista, cualquier miembro toca ⏫ Subir a nivel N (E-270).
- **Nadie pierde (D-64).** La misión solo traba la subida siguiente. **Un campamento de antes de la 0.56 no necesita la misión de la subida en la que estaba:** la línea sale ✅ "esta subida no la pide" y la primera llega al subir. Se eligió esto, y no "contar desde el parche", porque es lo más justo: nadie recibe un obstáculo nuevo a mitad de un nivel que planeó con las reglas de antes (tampoco el que tenía toda la lista ✅ el día del parche), y todos los campamentos de antes quedan iguales. Una misión retirada deja de pedirse.
- **Quedan fuera:** las misiones de una escuadra (§3: "las misiones de grupo son de una escuadra"; E-271), varias misiones por subida y un premio para cada miembro (los encargos de la semana ya pagan experiencia y monedas).
- **Dónde está:** `engine/service/group_missions.py` (`GroupMissionMixin`: `_gm_target`, `_gm_start`, `_gm_state`, `_gm_row`, `_gm_how_line`, `_gm_new_line`, `_gm_all_part`, `_gm_board_lines`, `_gm_event`, `_gm_complete`); los ganchos en `engine/service/game.py` (`_create_camp`, `_level_up`, `_lvlup_rows` tipo "mission", `_lvlup_view`, `_lvlup_all_view`, `_end_combat` con `raid=True`) y `engine/service/story.py` (`_story_event`, `_camp_task_lines`); el tipo `defend` en `engine/story/rules.py`; las misiones en `content/story.yaml` → `group_missions` (ids estables, una por nivel de destino) y los números en `content/balance.yaml` → `group_missions` (`per_member` 0,15, `members_cap` 40, `reward_per_level`); lo guardado en el espacio `group_mission` (clave del campamento); los textos en `content/locales/es_misiones_grupo.yaml` y `en_misiones_grupo.yaml`; las pruebas en `tests/test_misiones_de_grupo.py`; la cascada en el [mapa de impacto](../01-plataforma/mapa-de-impacto.md) C-36.
- **Preguntas para el dueño:** E-269 a E-271 (P-280 a P-282).

## 1. Lo decidido

| Decisión | Qué dice |
|---|---|
| **D-252** | *(18-oct: D-269 lo reemplaza: el gremio se crea desde el primer momento, §0.)* El grupo **nace al construir** uno mismo. En la fogata donde se sale **no se crea grupo**. |
| **D-269** | **El gremio desde el primer momento:** 🥉20, 5 antes del campamento, se pide entrar y aceptan el líder o un oficial; miembros a la vista, mensajes y un fondo; se funda con 2 miembros presentes y tarda (1 h con 2); cada obra tarda según los miembros en el territorio (§0). |
| **D-253.1** | **Forma A + B:** un solo cupo por etapa, y la **escuadra de 5** como unidad para organizarse. El castillo llega a 50 y el reino a 200. Las alianzas de castillos (Forma C) quedan para más adelante. |
| **D-253.2** | **Castillo:** 40 activos con cupo de 50 (D-122). |
| **D-253.3** | **Un miembro que no juega** libera su lugar a los **30 días** sin jugar. |
| **D-253.4** | **Aceptan gente** el líder y los oficiales. |
| **D-254** | La **muralla** crece con el asentamiento, y la tierra que encierra **cosecha sola** una parte de sus recursos. |
| **D-309** | **Los números de la cosecha (confirmados, 20-oct):** el 20 % de lo que vuelve a crecer, al almacén del asentamiento, solo con jugadores activos esa semana y como mucho 7 días; reemplaza el +50 % de recolectar en tu territorio; las zonas por etapa son las de la tabla del §2 (en el juego como tope del territorio desde la 0.41). |
| **D-325** | *(Provisional, 0.49.)* Cómo quedó la cosecha en el juego (§5.5): con la 🧱 Muralla todo el territorio cosecha; 24 por recurso y día como base (sin el ×3 de la 0.42); llega sola al 💰 fondo una vez por semana, con un aviso. |
| **D-327** | *(Provisional, 0.51.)* Cómo quedó la 1.ª parte de la escalera (§0.4): el cupo por etapa (10, 15, 25, 40, 50; nadie pierde lugar), los asistentes son los oficiales (1 cada 5), quien no juega 30 días sale (aviso a los 25, nunca el fundador, desde el parche) y el castillo pide 40 activos de la semana y 10 vencedores en la Noche de prueba. |
| **D-329** | *(Provisional, 0.53.)* Cómo quedaron las 🌊 oleadas crecientes del castillo (§0.5): en el nivel 8, las oleadas del campamento son una serie de 5, cada una un 20 % más fuerte; se aprueba ganando 3; con 3 perdidas vuelve a empezar a los 3 días; un castillo que ya existe no las recibe. |
| **D-136** | **Misiones de grupo:** para abrir cada nivel del campamento, el grupo cumple misiones juntos (farmear, recolectar, llenar la despensa). |
| **D-332** | *(Provisional, 0.56.)* Cómo quedaron las 🎯 misiones de grupo (§0.6): una por subida de nivel, 8 hasta castillo; la meta crece con el nivel y un 15 % por activo y queda fija al empezar; al cumplirla, un premio chico al 💰 fondo; los campamentos de antes no la necesitan en la subida en la que estaban. |
| **D-322** | *(Provisional, 0.47.)* El 💰 fondo del campamento primero alimenta las obras activas y ⏫ Siguiente nivel (lo que les falta queda guardado); lo que sobra lo usan los miembros al refinar y fabricar en las estaciones de su campamento, hasta 40 por día, con 📜 Quién usó qué y un interruptor del fundador o un asistente (§0.3). |

## 2. La escalera

Un solo número dice cuánta gente cabe en cada etapa: se acaba el doble cupo de hoy (el del campamento y el del gremio, donde gana el mayor).

| Etapa | Cupo | Cómo se sube | Qué abre | Zonas de muralla (P-229) |
|---|---|---|---|---|
| 1 · Casa | 5 | **Construir tu casa** tú mismo (nace el grupo, D-252) | Inventario compartido, misiones de grupo, despensa chica, primeras oleadas | 1 |
| 2 · Campamento | 10 | 3 mejoras y la 1.ª misión de grupo | El grupo pasa a gremio, 🎓 Academia (D-246) | 3 |
| 3 · Aldea | 15 | 8 activos, 6 mejoras y la 2.ª misión | Aldeanos y caravanas (D-205, D-202) | 5 |
| 4 · Pueblo | 25 | 12 activos, 10 mejoras y 3 oleadas ganadas | Territorio por cuadrantes (D-236), oficiales | 9 |
| 5 · Ciudad | 40 | 20 activos, 15 mejoras y la 4.ª misión | Mercado, segundo nodo | 15 |
| 6 · Castillo | 50 | **40 activos**, Noche de prueba con 10 vencedores distintos y 5 oleadas crecientes ganadas en su mayoría (D-122) | Peaje, guerra por nodos (D-236) | 25 |
| 7 · Fortaleza | 80 | Sostener el castillo 2 semanas, 60 activos | Mejoras de nivel alto | 35 |
| 8 · Ciudadela | 120 | 90 activos y una oleada mayor | Monstruo de asedio | 49 |
| 9 · Capital | 160 | 120 activos | Más territorio | 64 |
| 10 · Reino | **200** | 150 activos y un mes sostenido | La mejora más grande (la monarquía de D-155) | 81 |

- **Las misiones de grupo** (D-136) están en el juego desde la 0.56 con **una por subida de nivel**, no una por etapa: la 1.ª, la 2.ª, las "3 oleadas ganadas" y la 4.ª de la tabla caen en las subidas 1 → 2, 2 → 3, 4 → 5 y 6 → 7 (§0.6, D-332, provisional; E-269).
- **Activo** es haber jugado en la última semana (hoy la despensa cuenta 24 horas; para subir de etapa conviene mirar la semana, para que no dependa de un día).
- **La Casa y el Grupo son la misma etapa** (D-252): la propuesta que vio el dueño tenía 11 etapas, con "Grupo" antes de "Casa".
- **Lo que no se tira:** los niveles, las 20 mejoras y las oleadas de hoy siguen. Las etapas se estiran hacia arriba, y hacen falta mejoras nuevas para las etapas 7 a 10 (hoy se acaban en el nivel 8).

## 3. Escuadras y cargos (Forma B)

- **La escuadra:** el grupo de 5 de D-246 pasa a ser una escuadra dentro del gremio. Cada etapa abre lugar para más escuadras: 1, 2, 3, 5 y 8 hasta la ciudad, **10 en el castillo** (50 personas) y **40 en el reino** (200).
- **Cargos:**
  - el **líder** (quien construyó, D-252);
  - un **oficial** cada 2 a 4 escuadras, que nombra el líder;
  - un **jefe** por escuadra, que eligen sus 5.
- **Quién acepta gente:** el líder y los oficiales (D-253.4). El jefe de escuadra acomoda a los nuevos en su escuadra, pero no los acepta.
- **Las tareas se reparten por escuadra:**
  - la Noche de prueba se gana con "N escuadras que vencen" (por ejemplo, 8 de 10 en el castillo);
  - cada escuadra defiende un tramo de la muralla o un nodo;
  - las misiones de grupo son de una escuadra.
- **Encaja con el combate:** una habilidad de área alcanza a 5 objetivos (`chain.target_cap: 5`), justo una escuadra (D-246.4).

## 4. Quien deja de jugar

- **A los 30 días sin jugar**, el miembro deja de ocupar lugar: sale del gremio y su lugar queda libre (D-253.3).
- **Puede volver a pedir entrar,** y lo acepta el líder o un oficial.
- **Propuesta de Claude:** avisarle a los 25 días ("en 5 días liberas tu lugar en …"), y que lo que aportó a las obras quede en el asentamiento.
- **Cambia la regla 10 del servicio**, que decía "el gremio nunca saca a nadie".
- **En el juego desde la 0.51** (§0.4, D-327), con la propuesta de Claude, nunca para el fundador y contando desde el parche.

## 5. La muralla y la tierra que cosecha sola (D-254)

### 5.1 Lo que pidió el dueño

"Agrega la cantidad de muralla que pueden ampliar de acuerdo al tamaño del campamento, o sea, territorio tomado te genera farmeo del 40 % de los recursos de la zona o quizás menos, en automático, fomentando a que tomen todo el territorio alrededor."

### 5.2 Cómo se arma

- **La muralla es el borde del territorio.** Cada etapa deja cerrar más zonas (columna de la tabla del §2). Crece en anillos alrededor del centro: 1, 3 × 3 = 9, 5 × 5 = 25, 7 × 7 = 49, 9 × 9 = 81. Queda más o menos **una zona cada 2 o 3 jugadores** de cupo.
- **Cerrar una zona nueva cuesta:**
  - materiales, y más cuanto más lejos del centro (D-239.4);
  - mantenimiento por zona (D-239.5);
  - y la muralla hay que defenderla: las oleadas le pegan y una escuadra cuida cada tramo.

  Así, tomar todo lo de alrededor conviene, pero no sale gratis.
- **Cada zona cerrada cosecha sola** una parte de lo que la zona vuelve a crecer cada día, sin gastar energía.

### 5.3 Cuánto da: los números de hoy

| Dato | Valor | De dónde sale |
|---|---|---|
| Lo que junta un jugador por día recolectando | unas **80 unidades** (40 de energía, de 1 a 3 por vuelta en zonas bajas) | `gather`, `energy.per_day` |
| Lo que vuelve a crecer cada recurso de una zona | unas **24 unidades por día** | `stock.regen_per_hour` 0,02 por cada 0,02 que gasta una unidad |
| Una zona con 3 recursos | unas **72 por día** | |

| Porcentaje | Por zona y día | Pueblo (9 zonas) | Castillo (25 zonas) | Reino (81 zonas) |
|---|---|---|---|---|
| **40 %** (lo que dijo el dueño) | ~29 | ~260 | ~720 (lo de 9 jugadores) | ~2.300 |
| **20 %** (recomendado) | ~14 | ~130 | ~360 (lo de 4 o 5 jugadores) | ~1.150 |

Con 40 activos recolectando (unas 3.200 unidades por día), la cosecha del castillo suma un **11 %** al 20 %, y un **22 %** al 40 %.

### 5.4 La recomendación de Claude (P-227, P-228 y P-229)

1. **Empezar con 20 %** y medir en la beta. Es más fácil subirlo después que bajarlo: a nadie le gusta que le quiten.
2. **La cosecha va al 📦 almacén del asentamiento,** no a la mochila de nadie. Sirve para las obras, la muralla, las reparaciones y la comida de los aldeanos. Así lo pide D-195: las mejoras producen "para el castillo, no para los jugadores".
3. **Solo cosecha si el asentamiento tuvo jugadores activos esa semana,** y se junta como mucho **7 días**. Un asentamiento abandonado no se llena solo.
4. **Reemplaza el +50 % de hoy** al recolectar en tu propio territorio (D-87, `gather.own_land_bonus: 1.5`), para no sumar dos bonos y para cumplir D-239.3, que dice "nada de bonos de farmeo aparte".
5. **La cosecha sale de lo que vuelve a crecer, no del recurso que hay:** el que recolecta a mano en esa zona encuentra lo mismo que hoy.

El dueño aceptó las recomendaciones 1 a 4 el 20-oct (D-309) y la tabla de zonas ya estaba en el juego (D-304).

### 5.5 Cómo quedó en el juego (0.49, D-309; cómo se aplicó: D-325, provisional)

- **Qué zonas cosechan (E-247).** El juego todavía no tiene la muralla por anillos del §5.2. Mientras tanto, con la **🧱 Muralla** construida (la obra de nivel 5 que pide subir a 6) **todo el territorio** del campamento cuenta como cerrado. Sin muralla no hay cosecha. Un campamento de nivel 5 sin muralla ve en ⬆️ Mejorar una pista con lo que daría; antes del nivel 5 no se nombra (D-287).
- **Cuánto (E-248).** Cada recurso de cada zona da el **20 % de 24 unidades por día** (lo que vuelve un recurso con `stock.regen_per_hour` 2 % y `stock.per_unit` 2 %, el número de la pregunta que respondió el dueño): 4,8 por recurso y día. Hoy una zona tiene de 4 a 6 recursos (D-180, D-303), así que da **unas 27 por día**, no 14 como en la tabla del §5.3, que contaba 3. No cuenta el ×3 de la 0.42 ni el ⛲ Pozo: eso doblaría la cosecha (`harvest.real_regen`, abierto en E-248).
- **Qué.** Solo los materiales que recibe el 💰 fondo: los de base, la 🪵 madera y los propios del terreno. El 🐟 pescado es comida y no entra (el fondo no recibe comida, D-276).
- **A dónde: el 💰 fondo del campamento**, el mismo de 💰 Depositar (D-291). Nunca va a la mochila de nadie. Del fondo la toman las obras activas y ⏫ Siguiente nivel la próxima vez que alguien aporta, deposita o activa una obra, y lo que sobra queda para los oficios (D-322). La cosecha no baja los recursos de la zona.
- **Cuándo.** Se guarda en el campamento, con un **tope de 7 días** por recurso, y **cada 7 días llega sola al fondo**, de una vez, si algún miembro tocó un botón en esos 7 días. Si nadie jugó, lo de esa semana se pierde: un campamento abandonado no se llena solo. Solo pasan unidades enteras; la fracción queda para la semana siguiente. Una muralla de antes de la 0.49 empieza a contar cuando el juego la ve (como mucho 1 hora antes): nadie cobra días de antes del parche.
- **Lo que se ve (D-44, capa simple).** Una línea **"🌾 Cosecha de la muralla: +N/día · guardado X (tope 7 días) · al 💰 fondo en N días"** en 🏰 Gestionar → ⬆️ Mejorar, en 🛡️ Gremio → 💰 Fondos y en ℹ️ Información. Cuando llega, **un aviso por semana** a cada miembro, en su idioma, con lo que llegó y el botón 💰 Fondos del campamento. ❓ /d61 lo explica.
- **El +50 % (E-217).** `gather.own_land_bonus` pasó de 1,5 a 1,0 (la clave queda): en tu territorio juntas lo mismo que afuera. Las ⚒️ Herramientas siguen dando +10 %. ❓ /d09, /d57, las guías e ℹ️ Información ya no prometen el +50 %.
- **Cuánto da, con números de hoy** (zonas al tope de su etapa):

| Etapa | Zonas | Cosecha por día | De base (ahorra energía de juntar) |
|---|---|---|---|
| Pueblo (la muralla llega aquí) | 9 | ~240 | ~120 (unos 40 ⚡) |
| Ciudad | 15 | ~400 | ~200 (unos 66 ⚡) |
| Castillo | 25 | ~670 | ~330 |

- **El ritmo hasta castillo** (`python tools/camp_costs.py`, de 5 a 10 miembros que dan el 75 % de su energía): **~20,7 días** (0.48, con el +50 %: 17,6; sin cosecha: 23,4; con el ×3 de E-248: 17,4). Las 31 obras: ~47,7 días (antes 41,1). Hasta la muralla no hay cosecha: el nivel 6 llega hacia el día 7,9 (antes 5,5; E-249). Con la mitad de la energía (`--share=0.5`): castillo ~29,5 días.
- **Dónde está:** `content/balance.yaml` → `harvest` (wall, share, real_regen, week_days, cap_days, active_days, scan_minutes) y `gather.own_land_bonus`; las cuentas en `engine/world/harvest.py`; la entrega en `engine/service/game.py` (sección "🌾 the wall's harvest": `_harvest_tick` desde `tick()`, `_harvest_deliver`, `_harvest_line`); lo guardado en `upgrades/<x:y>` → `harvest`; los textos en `content/locales/es_cosecha.yaml` y `en_cosecha.yaml`; las pruebas en `tests/test_cosecha_muralla.py`; la cascada en el [mapa de impacto](../01-plataforma/mapa-de-impacto.md) C-34.
- **Preguntas para el dueño:** E-247 a E-249 (P-258 a P-260).

## 6. Dónde no se crea grupo (D-252)

> *(18-oct: D-269 reemplaza a D-252: el gremio se crea desde el primer momento, también en la fogata; ver §0. Lo de abajo queda como historia.)*

- **En la fogata de salida no se crea grupo.** Eso vale para el Claro y para las otras 🔥 fogatas de inicio (D-224, D-239.10; en el juego desde la 0.37; antes «hogueras», D-311).
- **El grupo nace cuando un jugador construye él mismo.** Cómo se leyó (D-256, provisional): levantar uno mismo la 🏠 casa de D-158 y, mientras la casa no exista en el juego, fundar el campamento. Aportar a la obra de otro no crea grupo.
- **Hoy ya se cumple sola:** no se puede fundar dentro del territorio del Claro ni a Lejanía menor que 2. Hay que mantenerla cuando lleguen los grupos y la casa.
- **Cambia D-246.2** ("cualquiera puede invitar desde el principio"): desde ahora invitan el líder y los oficiales, y recién desde la primera construcción.

## 7. Qué cambia del juego de hoy (cuando se programe)

| Hoy (0.33) | Con la escalera |
|---|---|
| ~~Cupo del campamento 2 + 2 por nivel; el del gremio, 4 a 30; gana el mayor (`_members_cap`)~~ | **Hecho en la 0.51 (D-327) hasta castillo:** 5 (el gremio antes del campamento), 10, 15, 25, 40 y 50; nadie pierde lugar (§0.4). Faltan 80, 120, 160 y 200 (etapas 7 a 10) |
| ~~Solo el fundador acepta (`_answer_join`, D-84)~~ | **Hecho:** el fundador y sus 🤝 asistentes desde la 0.39 (D-289); desde la 0.51 los asistentes son los oficiales (§0.4) |
| ~~Nadie sale si no quiere (regla 10)~~ | **Hecho en la 0.51:** sale a los 30 días sin jugar, con aviso a los 25, nunca el fundador (§0.4) |
| Castillo: gremio de nivel 5 con 10 miembros, 15 mejoras y la Noche (`_castle_needs`) | **Hecho en la 0.51 y la 0.53:** 40 activos de la semana y la Noche con 10 vencedores distintos (§0.4), y las 5 oleadas crecientes, ganando 3 (§0.5, D-329). Falta mantener el castillo (P-273) |
| Desde la 0.41 (D-304): 🗺️ Agrandar territorio suma zonas hasta el tope de la etapa (3, 5, 9, 15 y 25; `_grow_camp`, `camps.zones_by_stage`); el nivel sube aparte, con ⏫ Siguiente nivel | Las zonas de muralla de cada etapa (P-229) |
| ~~+50 % al recolectar en tu territorio (`gather.own_land_bonus`)~~ | **Hecho en la 0.49 (D-309, D-325):** con la 🧱 Muralla, todo el territorio cosecha solo para el 💰 fondo y el +50 % ya no está (§5.5). Falta la muralla por anillos con su costo por zona |
| No hay grupos | Grupo de 5 que nace al construir; escuadras dentro del gremio |
| ~~Subir de nivel pide obras y materiales (D-136, las misiones de grupo, por programar)~~ | **Hecho en la 0.56 (D-332):** cada subida pide también una 🎯 misión de grupo entre todos (§0.6); faltan las misiones de escuadra (§3, E-271) |

**Los jugadores de hoy no pierden nada (D-64):**
- cada campamento queda en la etapa que le corresponde por sus miembros y sus mejoras, nunca en una más baja;
- cada miembro de hoy sigue adentro;
- las zonas que ya tiene se quedan aunque pasen el tope de su etapa.

## 8. Red de sistemas

- **Consume:**
  - jugadores activos (para subir de etapa y para la Noche);
  - materiales (obras, muralla y mantenimiento);
  - defensa (oleadas que le pegan a la muralla);
  - lo que hacen los miembros por el grupo (peleas, recolección, comida y defensa: las 🎯 misiones de grupo, §0.6).
- **Produce:**
  - lugar para más gente;
  - cargos;
  - territorio que cosecha para el almacén;
  - control de nodos y peaje (D-236);
  - motivos de conflicto entre asentamientos (la tierra de alrededor);
  - un premio chico de materiales para el 💰 fondo al cumplir cada misión de grupo.
- **Amplio pero ligero (D-44):**
  - la capa simple es "construyes tu casa, invitas a 4 y crecen";
  - las escuadras, los cargos y la muralla aparecen recién cuando el asentamiento las necesita (cargos en el pueblo, muralla con zonas desde el campamento).

## 9. Preguntas abiertas

- **P-227 (E-216):** ✅ Decidido (D-309): 20 %, al almacén, con actividad y con tope de 7 días (en el juego desde la 0.49, §5.5).
- **P-228 (E-217):** ✅ Decidido (D-309): la cosecha reemplaza el +50 % (en el juego desde la 0.49).
- **P-258 (E-247):** qué zonas cierra la muralla. Recomendado: todo el territorio con la muralla, hasta que llegue la muralla por anillos.
- **P-259 (E-248):** si la cosecha cuenta el ×3 de la 0.42. Recomendado: no por ahora (24 por recurso y día) y medirlo en la beta.
- **P-260 (E-249):** qué pasa antes de la muralla. Recomendado: dejarlo así; la muralla es la meta del pueblo.
- **P-271 a P-273 (E-260 a E-262):** las 🌊 oleadas crecientes (0.53, D-329): sus números, cómo empiezan y se reintentan, y qué es mantener el castillo. Recomendado: dejarlas así y medirlas en la beta; que el castillo reciba una serie cada 4 semanas y, si la pierde, se frene su crecimiento.
- **P-280 a P-282 (E-269 a E-271):** las 🎯 misiones de grupo (0.56, D-332): una por subida o una por etapa, sus números y su premio, y si son del campamento o de una escuadra. Recomendado: una por subida; dejar los números y medirlos en la beta; que sigan siendo del campamento y que, con escuadras, se vea lo de cada escuadra.
- **P-264 a P-267 (E-253 a E-256):** la 1.ª parte de la escalera (0.51, D-327): el cupo de cada etapa, el asistente como oficial, quien deja de jugar y los requisitos del castillo. Recomendado: dejarlo así y medirlo en la beta; un solo cargo con 1 cada 5; quitar el gremio de nivel 5 cuando lleguen las oleadas crecientes.
- **P-81 (E-58):** ✅ Decidido (D-253): esta escalera.
- **P-79 (E-56):** ✅ Decidido, provisional (D-327 y D-329): la Noche con 10 vencedores distintos y 5 oleadas crecientes ganando 3 (§0.4 y §0.5); E-260 y E-261 la reemplazan.
- **P-229 (E-218):** ✅ Decidido (D-304): la tabla del §2 (en el juego, desde la 0.41, como tope de zonas del territorio hasta castillo).
- **Siguen de antes:**
  - P-224, la Academia o la Biblioteca;
  - P-82 / E-59, el monarca;
  - P-112 / E-89, la fusión de grupos;
  - P-97 / E-74, el tope diario por zona.

## De dónde sale

- **La escalera de etapas con un solo cupo:** las ciudades de Chat Wars y los niveles de clan de Clash of Clans, donde un número dice cuánta gente cabe.
- **Las escuadras de 5 y los cargos:** los grupos de 5 y los rangos de gremio de World of Warcraft (líder, oficiales, miembros), y los escuadrones de EVE Online.
- **La muralla que marca el territorio y crece por anillos:** el territorio de alianza de Rise of Kingdoms, que se agranda con banderas y fortalezas.
- **La tierra que produce sola:** los campos de recursos de Travian, que producen cada hora sin que nadie los trabaje. También las granjas de alianza de Rise of Kingdoms, que juntan recursos para la alianza, no para un jugador.
- **Las oleadas que crecen antes del castillo:** los juegos de defensa de torres, donde cada oleada es más fuerte que la anterior, y la horda final de They Are Billions, que pone a prueba todo lo construido; el "gana la mayoría" es el "al mejor de 5" de los torneos.
- **Las misiones de grupo para subir:** los desafíos de gremio de *World of Warcraft* (metas que el gremio cumple entre todos con lo que cada uno hace jugando) y los *Clan Games* de *Clash of Clans* (una meta común que suma lo de cada miembro y abre premios para el clan).
- **Liberar el lugar de quien no juega:** la regla de TowerWars de sacar a los inactivos (allí, a los 14 días; aquí, a los 30, como pidió el dueño).
