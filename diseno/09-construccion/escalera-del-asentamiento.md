# Escalera del asentamiento: de 5 a 200 jugadores

> **Módulo** [09 · Construcción](README.md) · **Depende de:** [Fundación y cisma](../02-mundo/fundacion-y-cisma.md), [Supervivencia del asentamiento](../02-mundo/supervivencia-del-asentamiento.md), [Gremios y social](../08-social/gremios-y-social.md), [Casa propia](casa-propia.md) · **Alimenta a:** [Defensa y protecciones](defensa-y-protecciones.md), [PvP](../06-contenido/pvp.md), [Economía](../07-economia/economia.md) · **Estado:** confirmado por el dueño en lo grande (D-252, D-253 y D-254, 17-oct-2026; D-269, 18-oct, reemplaza a D-252); los números son propuesta de Claude, a medir en la beta. **En el código (0.36): el gremio desde el primer momento, fundar con el gremio y las obras con tiempo (§0); (0.41): ⏫ Siguiente nivel con su lista, 🗺️ Agrandar territorio con tope de zonas por etapa y el 🤝 asistente (§0.2, D-304)**; la escalera de etapas (§2 a §7) todavía no

El dueño pidió (17-oct) armar los grupos, gremios y castillos para que "empecemos con 5 jugadores y a partir de ahí vaya creciendo incluso hasta 200 jugadores". Claude le mostró tres formas; eligió **A + B** con las cuatro recomendaciones, sumó la regla de la fogata y la idea de la muralla que cosecha sola.

---

## 0. Cómo está D-269 en el juego (0.36)

El 18-oct el dueño cambió el primer escalón: "hay que empezar a crear los grupos desde el primer momento" (D-269, **reemplaza a D-252**: el grupo ya no nace al construir). Cómo se aplicó, con las lecturas de D-274 (provisional):

- **👥 Jugadores en la fogata (D-265, D-274.1-2).** En el menú del campamento del Claro, 👥 Jugadores reemplaza a 🔬 Investigar (que ahí repetía 📚 Aprender oficios; en tu propio campamento 🔬 Investigar sigue). Lista a los que jugaron en la fogata en el último minuto, con clase, nivel y gremio, cada uno con su código (/j1) que abre su tarjeta: desde ahí el líder o un oficial ✉️ invita, o tú 🙋 pides entrar al gremio del otro. Arriba, "👥 N/20 en la fogata" (N con la regla de 15 min de 📍 Zona). Desde la 0.37 hay 9 hogueras, cada una con su 👥 Jugadores y su "N/20", y una llena reparte a los que llegan (D-265, D-277).
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
- **Obras que se activan (D-291):** todos ven las obras del nivel de su campamento; solo el fundador o un 🤝 asistente (antes "ayudante", D-304) toca ▶️ Activar (o ⏹️ Quitar, si nadie le dio nada), y todos aportan a las activas. Lo que estaba empezado antes de la 0.39 quedó activo solo.
- **Lo que no es de tu nivel no se ve (D-287):** las obras de niveles más altos, 🔬 Investigar sin 📚 Biblioteca y los avisos de "se abre al nivel X" ya no aparecen.
- **Cada obra nueva cuesta más (D-295):** un 15 % más por cada obra ya construida, con el precio fijo al activarla.

## 0.2 ⬆️ Mejorar campamento desde la 0.41 (D-304)

El dueño pidió (20-oct): "ponme en el botón de mejorar dos opciones: una, siguiente nivel, y dos, agrandar territorio… debes de construir esto, esto y esto a tal nivel para poder pasar al siguiente nivel, más los recursos que sean necesarios, en formato de lista. Y se va a ir completando". Y, el mismo día: "cada mejora debe ser visible para todos los miembros… dame la opción como dueño de gremio para agregar un asistente… que pueda definir hacia dónde va a avanzar el territorio junto contigo".

- **El nivel y las zonas van por separado.** Antes cada ⬆️ Agrandar sumaba 1 nivel y 1 zona (nivel = zonas, D-81). Ahora el nivel sube con ⏫ Siguiente nivel y las zonas con 🗺️ Agrandar territorio. Los campamentos de antes conservan su nivel y sus zonas (D-64).
- **🏰 Gestionar → ⬆️ Mejorar campamento:** el nivel y la etapa, las zonas usadas de su tope y cuántos requisitos del nivel siguiente están listos; dos botones: ⏫ Siguiente nivel y 🗺️ Agrandar territorio.
- **⏫ Siguiente nivel:** "Para subir a nivel N te falta:" y una lista con ✅ (listo) o ▫️ (falta) que se va llenando:
  - 🏗️ **Construir:** las obras que tienen que estar construidas (las elige Claude, provisional, `camps.level_up`; cada una es del nivel que el campamento ya tiene, así se ve y se activa). Si no, dice si está 🏗️ en obra, 🔨 activa o ⏸️ sin activar.
  - 📦 **Recursos:** 🪵 30, 🪨 20 y 🌿 10 por el nivel actual, con lo aportado (por ejemplo "🪵 Madera 12/30"); desde el nivel 6, 🪎 cofres (D-92: 1, 2 y 3; antes los pedía agrandar).
  - 🏰 **Para castillo (8 → 9):** el gremio listo (D-97), las 15 mejoras construidas (D-101) y la 🌙 Noche de prueba ganada (D-99, con su botón cuando es lo único que falta).
  - 🌾 Con la despensa vacía, una línea más: el campamento no sube (D-93).
  - Cualquier miembro aporta con **🤲 Aportar** (lo que hay en el 💰 fondo del campamento va primero; nunca toma de más; da experiencia, mérito y 🏗️ Construcción como las obras). Si el último aporte completa la lista, el campamento **sube en ese momento**; si lo último fue terminar una obra, cualquier miembro toca **⏫ Subir a nivel N**. Al subir se avisa a todos y caben 2 miembros más. En castillo todavía no hay otro nivel.
- **🗺️ Agrandar territorio:** las zonas usadas de su tope, el costo (de tu mochila: lo de antes, 🪵15 🪨10 🌿5, por las zonas que ya tiene, sin cofres), un **minimapa de 5 × 5** centrado en el campamento (🏕️ el centro, 🟩 lo tuyo, 1️⃣ 2️⃣ las zonas de esta página, 🔸 otras libres, ⬛ de otro) y una línea por zona libre con su **dirección** (⬆️ Norte, ↗️ Noreste… el norte suma a la y) y los recursos que conoces. **La eligen el fundador o un 🤝 asistente**; los demás ven todo. Sumar una zona no sube el nivel.
- **Tope de zonas por etapa** (la tabla de E-218, confirmada): campamento **3** · aldea **5** · pueblo **9** · ciudad **15** · castillo **25**. Al tope: "sube de nivel para agrandar más". Quien ya tenía más, las conserva.
- **🤝 Asistentes:** el ayudante de D-289 se llama asistente en los textos (1 cada 5 miembros, como antes). Activa obras, elige hacia dónde crece el territorio, invita y acepta solicitudes. En 🛡️ Gremio → 👥 Miembros el fundador ve cuántos tiene y cómo nombrar uno (tocar el código /m2 de un miembro → 🤝 Hacer asistente).
- **Todo visible para todos:** 🔨 Mejoras nombra a cada miembro las obras de su nivel que siguen sin activar, muestra las activas con su barra y las 🏗️ en obra con su tiempo, y dice "⏫ Nivel N: x de y listos". La lista de ⏫ la ve cualquier miembro.
- **Dónde está:** `engine/service/game.py` (`_improve_view`, `_lvlup_rows`, `_lvlup_view`, `_lvlup_give`, `_lvlup_go`, `_level_up`, `_grow_view`, `_grow_camp`, `_territory_map`), `engine/service/gremio.py` (`_helpers_founder_line`); los números en `content/balance.yaml` (`camps.level_up`, `level_up_cost_per_level`, `zones_by_stage`, `territory_map_radius`, `grow_cost_per_level`, `chests_*`); los textos en `content/locales/es_nivel.yaml` y `en_nivel.yaml`; la cascada en el [mapa de impacto](../01-plataforma/mapa-de-impacto.md).

## 1. Lo decidido

| Decisión | Qué dice |
|---|---|
| **D-252** | *(18-oct: D-269 lo reemplaza: el gremio se crea desde el primer momento, §0.)* El grupo **nace al construir** uno mismo. En la fogata donde se sale **no se crea grupo**. |
| **D-269** | **El gremio desde el primer momento:** 🥉20, 5 antes del campamento, se pide entrar y aceptan el líder o un oficial; miembros a la vista, mensajes y un fondo; se funda con 2 miembros presentes y tarda (1 h con 2); cada obra tarda según los miembros en el territorio (§0). |
| **D-253.1** | **Forma A + B:** un solo cupo por etapa, y la **escuadra de 5** como unidad para organizarse. El castillo llega a 50 y el reino a 200. Las alianzas de castillos (Forma C) quedan para más adelante. |
| **D-253.2** | **Castillo:** 40 activos con cupo de 50 (D-122). |
| **D-253.3** | **Un miembro que no juega** libera su lugar a los **30 días** sin jugar. |
| **D-253.4** | **Aceptan gente** el líder y los oficiales. |
| **D-254** | La **muralla** crece con el asentamiento, y la tierra que encierra **cosecha sola** una parte de sus recursos. El porcentaje sigue abierto (P-227). |

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
- **Cambia la regla 10 del servicio**, que hoy dice "el gremio nunca saca a nadie".

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

## 6. Dónde no se crea grupo (D-252)

> *(18-oct: D-269 reemplaza a D-252: el gremio se crea desde el primer momento, también en la fogata; ver §0. Lo de abajo queda como historia.)*

- **En la fogata de salida no se crea grupo.** Eso vale para el Claro y, cuando existan, para las hogueras de inicio (D-224, D-239.10).
- **El grupo nace cuando un jugador construye él mismo.** Cómo se leyó (D-256, provisional): levantar uno mismo la 🏠 casa de D-158 y, mientras la casa no exista en el juego, fundar el campamento. Aportar a la obra de otro no crea grupo.
- **Hoy ya se cumple sola:** no se puede fundar dentro del territorio del Claro ni a Lejanía menor que 2. Hay que mantenerla cuando lleguen los grupos y la casa.
- **Cambia D-246.2** ("cualquiera puede invitar desde el principio"): desde ahora invitan el líder y los oficiales, y recién desde la primera construcción.

## 7. Qué cambia del juego de hoy (cuando se programe)

| Hoy (0.33) | Con la escalera |
|---|---|
| Cupo del campamento 2 + 2 por nivel; el del gremio, 4 a 30; gana el mayor (`_members_cap`) | Un solo cupo por etapa: 5, 10, 15, 25, 40, 50, 80, 120, 160 y 200 |
| Solo el fundador acepta (`_answer_join`, D-84) | El líder y los oficiales |
| Nadie sale si no quiere (regla 10) | Sale a los 30 días sin jugar |
| Castillo: gremio de nivel 5 con 10 miembros, 15 mejoras y la Noche (`_castle_needs`) | 40 activos, la Noche con 10 vencedores distintos y 5 oleadas crecientes (D-122) |
| Desde la 0.41 (D-304): 🗺️ Agrandar territorio suma zonas hasta el tope de la etapa (3, 5, 9, 15 y 25; `_grow_camp`, `camps.zones_by_stage`); el nivel sube aparte, con ⏫ Siguiente nivel | Las zonas de muralla de cada etapa (P-229) |
| +50 % al recolectar en tu territorio (`gather.own_land_bonus`) | La tierra cosecha sola para el asentamiento (P-227, P-228) |
| No hay grupos | Grupo de 5 que nace al construir; escuadras dentro del gremio |

**Los jugadores de hoy no pierden nada (D-64):**
- cada campamento queda en la etapa que le corresponde por sus miembros y sus mejoras, nunca en una más baja;
- cada miembro de hoy sigue adentro;
- las zonas que ya tiene se quedan aunque pasen el tope de su etapa.

## 8. Red de sistemas

- **Consume:**
  - jugadores activos (para subir de etapa y para la Noche);
  - materiales (obras, muralla y mantenimiento);
  - defensa (oleadas que le pegan a la muralla).
- **Produce:**
  - lugar para más gente;
  - cargos;
  - territorio que cosecha para el almacén;
  - control de nodos y peaje (D-236);
  - motivos de conflicto entre asentamientos (la tierra de alrededor).
- **Amplio pero ligero (D-44):**
  - la capa simple es "construyes tu casa, invitas a 4 y crecen";
  - las escuadras, los cargos y la muralla aparecen recién cuando el asentamiento las necesita (cargos en el pueblo, muralla con zonas desde el campamento).

## 9. Preguntas abiertas

- **P-227 (E-216):** cuánto cosecha cada zona y a dónde va. Recomendado: 20 %, al almacén, con actividad y con tope de 7 días.
- **P-228 (E-217):** si la cosecha reemplaza el +50 % de hoy. Recomendado: sí.
- **P-229 (E-218):** ✅ Decidido (D-304): la tabla del §2 (en el juego, desde la 0.41, como tope de zonas del territorio hasta castillo).
- **Siguen de antes:**
  - P-224, la Academia o la Biblioteca;
  - P-79 / E-56, las oleadas del castillo;
  - P-82 / E-59, el monarca;
  - P-112 / E-89, la fusión de grupos;
  - P-97 / E-74, el tope diario por zona.

## De dónde sale

- **La escalera de etapas con un solo cupo:** las ciudades de Chat Wars y los niveles de clan de Clash of Clans, donde un número dice cuánta gente cabe.
- **Las escuadras de 5 y los cargos:** los grupos de 5 y los rangos de gremio de World of Warcraft (líder, oficiales, miembros), y los escuadrones de EVE Online.
- **La muralla que marca el territorio y crece por anillos:** el territorio de alianza de Rise of Kingdoms, que se agranda con banderas y fortalezas.
- **La tierra que produce sola:** los campos de recursos de Travian, que producen cada hora sin que nadie los trabaje. También las granjas de alianza de Rise of Kingdoms, que juntan recursos para la alianza, no para un jugador.
- **Liberar el lugar de quien no juega:** la regla de TowerWars de sacar a los inactivos (allí, a los 14 días; aquí, a los 30, como pidió el dueño).
