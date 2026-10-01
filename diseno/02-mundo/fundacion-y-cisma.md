# Fundación y cisma: el mundo empieza de cero y los jugadores deciden si se divide

> **Módulo** [02 · Mundo](README.md) · **Depende de:** [Mapa infinito y viaje](mapa-infinito-y-viaje.md), [Construcción](../09-construccion/README.md), [Profesiones](../07-economia/profesiones.md), [Gremios y vida social](../08-social/gremios-y-social.md) §0 (el castillo pide gremio, D-97) · **Alimenta a:** [Ciudades y el Castillo](ciudades-y-castillo.md), [Supervivencia del asentamiento](supervivencia-del-asentamiento.md), [Facciones](facciones.md), [PvP](../06-contenido/pvp.md), [Economía](../07-economia/economia.md) · **Estado:** §1 y §2 están en el juego (0.9.2); §3 en adelante es propuesta

**Qué pidió el dueño.** Que no exista un castillo al empezar: que todo arranque **desde cero** y la gente **construya el mundo** (D-45). Que el Claro sea la sede común y que los jugadores **funden sus propios campamentos**, que crezcan hasta ciudades y castillos (D-71, D-81, D-87). Que el mundo se pueda **dividir** por decisión de los jugadores, con desventajas para quien queda. Y que haya gente dedicada a todo: agricultores, cazadores, expertos en cada cosa.

**Las dos piezas de hoy.**
1. **El Claro:** el **campamento base** de todo el servidor, con mercader y posada. **No crece** (D-98): la obra común que lo subía de fogata a castillo se quitó en la 0.11.
2. **Los campamentos de jugadores:** cada uno se funda lejos del Claro, tiene nombre y miembros, y crece **eligiendo zonas** hasta castillo.

Todo lo demás de este documento (necesidades, gobierno, cisma, relaciones entre castillos) es la capa profunda que se monta encima, como propuesta.

---

## 1. El Claro: la obra común (historia: se quitó en la 0.11)

> **Ya no existe (D-98, confirmada por el dueño el 1-oct-2026):** el Claro es el **campamento base** y no crece. La obra común se quitó en la 0.11: ya no se aportan materiales al Claro y su etapa guardada queda fija (decide la posada y sus zonas). Todo el crecimiento (niveles, mejoras, conocimiento, castillo) es solo para los campamentos de los jugadores. Esta sección queda como historia de la 0.4 a la 0.10.1.

Al abrir el servidor no hay ciudad. En el centro del mapa, en (0, 0), está **el Claro**: una fogata entre ruinas. Ahí despierta cada héroe nuevo.

### 1.1 La obra común, por etapas

Todos los jugadores levantan juntos el Claro. En **🏕️ Campamento → 🔥 Obra del campamento**, el botón **🤲 Aportar mis materiales** entrega de una vez todo lo que la etapa todavía pide y que llevas en la mochila. Cuando se completa la lista, el Claro sube de etapa para todos.

| Etapa | Para pasar a la siguiente hace falta | Zonas del Claro | Posada |
|---|---|---|---|
| **Fogata** | 40 de madera y 30 de fibra | 1 | 4 🥉 |
| **Campamento** | 120 de madera, 80 de fibra y 60 de piedra | 2 | 3 🥉 |
| **Aldea** | 300 de madera, 250 de piedra, 150 de fibra y 40 de metal | 3 | 2 🥉 |
| **Pueblo** | 700 de madera, 600 de piedra, 150 de metal y 100 de hierba curativa | 4 | 1 🥉 |
| **Ciudad** | 1.500 de madera, 1.500 de piedra, 400 de metal y 600 de fibra | 5 | 1 🥉 |
| **Castillo** | Nada más por ahora: "lo que sigue lo deciden sus habitantes" | 6 | 1 🥉 |

- Los números están en `content/balance.yaml` (`settlement.stages`).
- **Cada material aportado da 2 de experiencia y 1 de mérito.** La obra muestra a los 5 que más aportaron y tu mérito (`settlement.xp_per_unit`).
- **Cada etapa baja 1 🥉 el precio de la posada,** hasta un mínimo de 1 (`settlement.inn_discount_per_stage`).
- **El Claro ocupa 1 zona más por etapa** (D-81). Crece en una espiral fija: norte, este, sur, oeste y las diagonales.
- **Una etapa ganada no se pierde.** Hoy el Claro nunca baja.
- **El Claro no se mantiene** (D-95, confirmada por el dueño): es el campamento principal del mapa y no tiene dueño, así que no tiene despensa ni otros mínimos; y tampoco crece (D-98). La comida (D-93) es solo para los campamentos de jugadores. Detalle en [Supervivencia del asentamiento](supervivencia-del-asentamiento.md) §0.4.

### 1.2 Lo que ofrece el Claro

- **🏪 Mercader:** vende pociones de vida, vendas y 🥖 provisiones (comida cara de emergencia, D-93), y compra materiales a la mitad de su precio (`shop`).
- **🛏️ Posada:** pagas, duermes 5 minutos y despiertas con la vida llena. También cura al héroe malherido (D-83). Con la vida ya llena no cobra: te avisa que no hace falta.
- **💰 Costura de bolsas:** 4 de fibra, 1 pieza de metal y 1 🥈 por bolsa (D-80).
- **Venta de equipo** que no te sirve.
- **Territorio seguro:** en las zonas del Claro no te atacan: ni al llegar, ni al explorar, ni al recolectar.
- **Ancla del viaje:** la distancia de cada viaje se cuenta desde el borde del Claro o de tu campamento (D-78).

Los servicios se usan en la zona central (0, 0), sin estar haciendo otra cosa.

## 2. Los campamentos de los jugadores (en el juego)

### 2.1 Fundar

En **🏕️ Campamento**, fuera del Claro, el bot muestra qué falta para fundar en la zona donde estás:

| Requisito | Valor | Dónde se ajusta |
|---|---|---|
| Lejos del Claro | Lejanía 2 o más | `camps.min_lejania` |
| Zona explorada | Al 100 % (D-87) | `exploration` |
| Conocer los alrededores | Haber pisado 4 de las 8 zonas vecinas | `camps.known_neighbors` |
| Lugar libre | Ningún campamento a 2 zonas o menos, y no estar en territorio ajeno | `camps.min_distance` |
| Costo | 20 de madera y 10 de piedra | `camps.found_cost` |
| Un solo campamento | No pertenecer a otro | — |

- Al fundar, **escribes el nombre** del campamento: de 3 a 24 caracteres, **único en el mundo**. El fundador lo puede cambiar cuando quiera (D-84). Si en vez de escribirlo tocas otro botón, la pregunta se cancela: un texto escrito más tarde ya no funda nada.
- Al fundarlo, el campamento ocupa 1 zona y su fundador es su primer miembro.

### 2.2 Miembros

- Otro jugador que llega al campamento toca **🙋 Pedir unirme**. El fundador recibe un aviso y decide con **✅ Aceptar** o **❌ Rechazar** (D-84).
- **Cupo sin gremio:** caben 2 miembros al nivel 1 y 2 más por cada nivel (`camps.members_base`, `camps.members_per_level`).
- **Cupo con gremio** (D-97, provisional): el fundador puede crear el **gremio** del campamento, y desde ese momento el cupo lo da el nivel del gremio: 4 al nivel 1, 6, 8, 12, 16, 20, 25 y 30 al nivel 8 (`guild.levels`). El gremio sube con lo que hacen sus miembros juntos (exploraciones, peleas ganadas y recursos recolectados). Nadie sale si el cupo baja. Los miembros del gremio son los del campamento. Detalle: [Gremios y vida social](../08-social/gremios-y-social.md) §0.
- Cada jugador pertenece a **un solo campamento**. Un miembro puede salir con **🚪 Salir del campamento** (dentro de 🛡️ Gremio). El fundador no puede salir.
- Para cada miembro, el viaje cuenta la distancia desde el campamento (D-78).

### 2.3 Visitantes

- Quien llega a un campamento ajeno lo **encuentra**: ve su nombre y su fundador.
- Los miembros reciben un aviso una sola vez por visitante y uno responde si es **🤝 Amistoso** o **⚔️ Hostil** (D-71).
- Un visitante hostil no puede pedir unirse. Hoy "hostil" es solo una marca: todavía no hay PvP.

### 2.4 Crecer eligiendo zonas

- Cualquier miembro toca **⬆️ Agrandar campamento** y paga de su mochila **15 de madera, 10 de piedra y 5 de fibra, por el nivel actual** (`camps.grow_cost_per_level`, D-81).
- **Desde el nivel 6, también 🪎 cofres** (D-92, provisional): 1 de 6 a 7, 2 de 7 a 8 y 3 de 8 a 9; la fórmula es `camps.chests_per_level` × (nivel actual − `chests_from_level` + 1), y sigue igual después del castillo. Los paga el miembro que agranda. Un cofre se arma en el Claro con 10 💰 bolsas, 10 de madera y 5 piezas de metal (ver [Economía](../07-economia/economia.md) §2). La pantalla de agrandar muestra el costo en cofres y cuántos tienes; si faltan, no se cobra nada.
- **Elige qué zona toma:** una zona libre que toque el territorio por norte, sur, este u oeste. El bot muestra los recursos que conoces de cada una, para elegir con estrategia (D-87).
- Cada mejora suma **1 nivel y 1 zona**. No hay nivel máximo: después del 9 sigue creciendo como castillo.
- **El castillo pide gremio** (D-97, provisional): para pasar del nivel 8 al 9 hace falta un gremio de nivel 5 o más con 10 miembros o más (`guild.castle_min_level`, `guild.castle_min_members`). Sin gremio, el campamento se queda en ciudad. La pantalla de agrandar lo muestra con ✅ y ▫️.

| Nivel | Nombre | Zonas | Cupo sin gremio | Costo de llegar desde el nivel anterior |
|---|---|---|---|---|
| 1 | Campamento | 1 | 2 | Fundar: 20 de madera y 10 de piedra |
| 3 | Aldea | 3 | 6 | 30 de madera, 20 de piedra y 10 de fibra |
| 5 | Pueblo | 5 | 10 | 60 de madera, 40 de piedra y 20 de fibra |
| 7 | Ciudad | 7 | 14 | 90 de madera, 60 de piedra, 30 de fibra y 1 🪎 cofre |
| 9 | Castillo | 9 | 18 (o el cupo del gremio, si es mayor) | 120 de madera, 80 de piedra, 40 de fibra y 3 🪎 cofres, y un gremio de nivel 5 con 10 miembros (D-97) |

Desde la fundación hasta castillo se pagan en total **560 de madera, 370 de piedra, 180 de fibra y 6 🪎 cofres** (1 + 2 + 3, de 6 a 9). Los nombres por nivel están en `camps.stages`.

**Qué da el territorio:**
- En cualquier territorio (de tu campamento, de otro o del Claro) no te atacan: ni al llegar, ni al explorar, ni al recolectar.
- **En el territorio de tu campamento recolectas un 50 % más** (`gather.own_land_bonus`, D-87).
- Nadie puede fundar otro campamento encima.
- El viaje cuenta la distancia desde la zona más cercana de tu territorio.

### 2.5 Lo que todavía no tienen

Hoy un campamento de jugadores **no tiene servicios** (ni mercader, ni posada, ni almacén común) ni una obra común propia. Crecer es pagar materiales (y, desde el nivel 6, 🪎 cofres, D-92); desde el nivel 3 (aldea), además, la **despensa** no puede estar vacía (D-93, provisional; ver [Supervivencia del asentamiento](supervivencia-del-asentamiento.md) §0.4), y para ser castillo hace falta un **gremio** listo (D-97, provisional; ver [Gremios y vida social](../08-social/gremios-y-social.md) §0). El gremio todavía no tiene rangos, banco ni salón. Lo que viene después es propuesta (§3 a §7 y [Ciudades y el Castillo](ciudades-y-castillo.md)).

**Por qué conviene así.** El Claro junta a todo el servidor en una meta común desde el primer día. Los campamentos dan a cada grupo un lugar propio, con decisiones reales: dónde fundar, a quién aceptar y qué zonas tomar.

## 3. Las necesidades del asentamiento (propuesta)

Más adelante, un asentamiento (el Claro o un campamento grande) **necesitaría cosas todos los días** y las conseguiría de los jugadores. Si le faltan, sus servicios empeoran.

| Necesidad | Quién la cubre | Si falta… |
|---|---|---|
| 🌾 **Comida** | Agricultores, ganaderos, cazadores, pescadores, cocineros | La gente se va, la posada no cura, sube el estrés |
| 🪵 **Materiales** | Leñadores, canteros, recolectores (ya en el juego: madera, piedra, fibra, hierba, metal y arcilla) | No se puede construir ni reparar |
| 🔨 **Herramientas y equipo** | Herreros, carpinteros, sastres | Las estaciones públicas pierden nivel |
| 🛡 **Defensa** | Guerreros, guardias, constructores (murallas) | Las incursiones de monstruos entran (ver [Defensa](../09-construccion/defensa-y-protecciones.md)) |
| ⚕️ **Salud** | Médicos, alquimistas, herboristas | Las enfermedades se propagan |
| 🎶 **Ánimo** | Bardos, taberneros, cocineros, festivales | Sube el estrés; menos gente se suma |
| ⚖️ **Orden** | Guardia, gobierno, investigadores | Aparecen ladrones y garitos |
| 🪙 **Tesoro** | Impuestos, comercio | No se pagan las obras ni el mantenimiento |

- **Capa simple:** el jugador ve unas pocas barras y toca 📋 Aportar, igual que hoy aporta a la obra común.
- **Capa profunda:** los medidores con umbrales, la despensa, las incursiones y las decisiones están en [Supervivencia del asentamiento](supervivencia-del-asentamiento.md).
- **Por qué conviene:** toda la infraestructura depende de farmear, fabricar y progresar, y cada rol es necesario de verdad. Ver [Red de sistemas](../00-vision/red-de-sistemas.md).

## 4. Qué abre cada etapa (propuesta)

Las etapas ya existen con sus nombres. Lo que falta es que cada una **abra algo**. La misma escala sirve para el Claro (por etapas de la obra común) y para los campamentos (por nivel).

| Etapa | Claro | Campamento de jugadores | Qué abriría (propuesta) |
|---|---|---|---|
| **Fogata** | Etapa 1 | — | Hoy: mercader, posada y costura. Tutorial |
| **Campamento** | Etapa 2 | Nivel 1-2 | Descanso básico en el campamento propio |
| **Aldea** | Etapa 3 | Nivel 3-4 | Almacén común, un servicio propio (posada o mercader), primeras recetas |
| **Pueblo** | Etapa 4 | Nivel 5-6 | Gobierno (§5), taller público, mercado entre jugadores |
| **Ciudad** | Etapa 5 | Nivel 7-8 | Estaciones públicas mejores, cirugía segura, investigación |
| **Castillo** | Etapa 6 | Nivel 9 o más | El Castillo y sus alas, cada una como obra aparte (ver [Ciudades y el Castillo](ciudades-y-castillo.md)) |

*Los documentos viejos llaman "Claro" a la primera etapa y "Villa" a la cuarta. Hoy son **Fogata** y **Pueblo**.*

**Construir no alcanzaría (capa profunda).** Para el Claro, desde la etapa Aldea, la propuesta es que pagar la obra no baste: habría que **sostener** unos días la comida, la salud y la defensa, y superar incursiones. Esto cambia cómo sube hoy el Claro, así que lo decide el dueño antes de programarse. El detalle está en [Supervivencia del asentamiento](supervivencia-del-asentamiento.md) §7.

### 4.1 Territorio y zonas de influencia (en parte en el juego)

**De dónde sale.** *Ashes of Creation* y sus **nodos**: la actividad de los jugadores hace crecer un lugar y limita a sus vecinos.

- **Ya en el juego:** un campamento no se funda a 2 zonas o menos de otro, cada zona es de un solo dueño y el campamento elige hacia dónde crece (D-87).
- **Vasallos (propuesta):** un campamento en ciudad o castillo podría tomar como vasallos a campamentos chicos cercanos que acepten. El vasallo paga una parte de lo que aporta y recibe protección y viaje más corto.
- **Decadencia (propuesta):** un campamento sin miembros activos durante semanas perdería niveles poco a poco y terminaría en **ruinas** que otro grupo puede refundar. Lo personal de cada jugador nunca se pierde.
- **Destrucción (propuesta, muy lejana):** en zonas rojas y negras, los asentamientos se podrían asediar (ver [Defensa](../09-construccion/defensa-y-protecciones.md)).

## 5. Gobierno (propuesta)

**De dónde sale.** *Wakfu* (Ankama, 2012): cada nación elige a un gobernador por voto, y el gobernador nombra cargos, como un **Ecologista** que dicta leyes de recolección. También *Star Wars Galaxies*, con sus alcaldes de ciudades de jugadores.

**Hoy** el fundador decide todo en su campamento: el nombre y quién entra. El Claro no tiene gobierno.

**La propuesta:**
- **Campamentos:** el fundador sigue siendo el jefe. Desde Pueblo (nivel 5), los miembros podrían votar un **consejo** que comparta las decisiones (aceptar miembros, hacia dónde crecer, qué obra va primero).
- **El Claro:** desde la etapa Pueblo, un **gobernador** elegido por voto, cada temporada, con las encuestas de Telegram. Votan los jugadores activos que aportaron a la obra común en el último mes.
- **Cargos que nombra el gobernador:**

  | Cargo | Poder |
  |---|---|
  | **Ecologista** | Leyes de recolección: vedas y cuotas en zonas agotadas (se conecta con el agotamiento de recursos, D-87) |
  | **Tesorero** | Presupuesto de obras, pedidos semanales, tasas |
  | **Capitán de la Guardia** | Patrullas y guardias (ver [Crimen y justicia](../06-contenido/crimen-y-justicia.md)) |
  | **Maestro de Obras** | Orden de las obras públicas |
  | **Juez** | Preside el tribunal |
  | **Embajador** | Tratados con los campamentos grandes |

- **Mandatos que vencen** por temporada (D-29). Propuesta: nunca más de **dos seguidos** en el mismo cargo.
- **Moción de censura:** los residentes pueden destituir al gobernador (ver [Crisis](crisis-problemas-y-soluciones.md)).

## 6. El cisma: cuando un grupo se va (propuesta)

**Hoy irse es libre y barato:** cualquiera sale de su campamento o funda uno nuevo con las reglas de §2. Eso no cambia. El **cisma** es la versión grande y política, para cuando haya gobierno y algo común que repartir.

### 6.1 Cómo se decide

1. **Motivo.** Cualquiera: no les gusta el gobierno, quieren otra política, rivalidades.
2. **Carta de fundación.** Un grupo escribe una carta (nombre, emblema y lugar) y la firma. Firmar es reenviar el mensaje de la carta al bot (ver [Telegram](../01-plataforma/telegram.md)).
3. **Mínimo de firmas.** En el Claro: el 15 % de los residentes activos o 30 jugadores, lo que sea mayor (P-54). En un campamento: un tercio de sus miembros, con un mínimo de 3.
4. **Plazo.** El cisma se anuncia y hay **7 días**: los que se van se preparan y los que se quedan pueden negociar.
5. **Salida.** Los firmantes dejan el lugar y fundan un campamento nuevo con las reglas normales (§2.1).

### 6.2 Qué se llevan y qué dejan

| | Se llevan | Dejan |
|---|---|---|
| **Personal** | Todo lo suyo: mochila, monedas, equipo, nivel y talentos | — |
| **Común** | Una parte del almacén y del tesoro (cuando existan), según lo que aportaron | Las zonas del territorio y las obras: no se mueven |

### 6.3 Desventajas

- **Para quien se queda:** menos manos para las mismas necesidades, obras a medias y un mes de "lugar dividido" (menos ánimo y reputación).
- **Para quien se va:** empieza en nivel 1, sin servicios, y pierde reputación con el lugar que dejó.

**Por qué conviene.** Dividirse es una decisión **con peso**, no un botón. Pero es posible, y eso le da poder real a la comunidad. Las facciones nacen de la historia del servidor (ver [Facciones](facciones.md)).

## 7. Relaciones entre campamentos (propuesta)

**La semilla ya existe:** cada campamento marca a cada visitante como 🤝 amistoso o ⚔️ hostil (D-71). La propuesta lleva eso de persona a campamento:

| Relación | Qué implicaría |
|---|---|
| **Tratado comercial** | Menos comisión entre sus mercados |
| **Alianza** | Defensa mutua ante incursiones, Guardianes juntos |
| **Neutralidad** | Nada especial |
| **Rivalidad** | Guerra de castillos a hora fija (ver [PvP](../06-contenido/pvp.md)), solo entre castillos con gobierno y solo si los dos la aceptan |
| **Reunificación** | Si los dos lo votan, vuelven a ser uno y suman miembros y zonas |

- **Tope de guerras:** ser castillo es una etapa que cualquier campamento alcanza (D-87), así que el tope ya no es de castillos sino de **reinos en guerra** al mismo tiempo, para que el servidor no se rompa en cien frentes (P-54).
- Antes del primer cisma no hay guerra de castillos.

## 8. Todo en texto y por turnos

- **Hoy:** el menú fijo **🏕️ Campamento** abre el mercader y la posada en el Claro (sin obra común desde la 0.11, D-98), o la pantalla del campamento donde estás. La zona muestra "🏕️ Territorio de…".
- **Propuesta:** `/ciudad` con la etapa, las barras de necesidades y los pedidos de la semana; elecciones con encuestas de Telegram; cartas de cisma firmadas reenviando el mensaje; todo lo importante en la Gaceta.

## 9. De dónde sale

- *Sword Art Online*: los jugadores atrapados tuvieron que organizarse solos y se partieron en grupos con visiones distintas.
- *Rust*, *Conan Exiles* y *Wurm Online*: empezar sin nada y construirlo todo.
- *Ashes of Creation*: nodos que crecen con la actividad y limitan a sus vecinos.
- *Star Wars Galaxies*: ciudades de jugadores con alcalde, que crecen o mueren según cuánta gente vive en ellas.
- *EVE Online*: alianzas que se separan y cambian el mapa.
- *Civilization* y *Crusader Kings*: secesiones y el costo de dividir un reino.
- *Chat Wars* y TowerWars: la vida en torno a un castillo, con su chat y sus órdenes.

## 10. Preguntas

- **P-54:** mínimo para un cisma y tope. Con D-87, el tope pasa a ser de reinos en guerra, no de castillos.
- **P-55:** cuánto debería tardar el Claro en llegar a castillo. Hoy depende solo de cuántos materiales aporta el servidor.
- Ver [Preguntas abiertas](../00-vision/preguntas-abiertas.md).
