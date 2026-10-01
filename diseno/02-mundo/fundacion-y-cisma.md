# Fundación y cisma: el mundo empieza de cero y los jugadores deciden si se divide

> **Módulo** [02 · Mundo](README.md) · **Depende de:** [Construcción](../09-construccion/README.md), [Profesiones](../07-economia/profesiones.md) · **Alimenta a:** [Facciones](facciones.md), [Ciudades y el Castillo](ciudades-y-castillo.md), [PvP](../06-contenido/pvp.md), [Economía](../07-economia/economia.md) · **Estado:** propuesta

**Qué pediste.** Que no exista un castillo al empezar: que todo arranque **desde cero** y la gente **construya el mundo**. Que ese mundo se pueda **dividir** por decisión de los jugadores: todos empiezan construyendo un castillo, pero cierta cantidad de jugadores puede **separarse**, y eso trae **desventajas para el castillo** que dejan. Y que haya gente dedicada a todo: agricultores, cazadores, expertos en cada cosa.

**De dónde sale.**
- *Sword Art Online*: los jugadores atrapados en el Piso 1 tuvieron que organizarse solos y se partieron en grupos con visiones distintas (los que querían avanzar, los que querían proteger a los débiles, los que querían el control).
- *EVE Online*: alianzas enteras que se separan y cambian el mapa, con historia escrita por los jugadores.
- *Star Wars Galaxies*: ciudades de jugadores con alcalde, que crecían o morían según cuánta gente vivía en ellas.
- *Rust*, *Conan Exiles* y *Wurm Online*: empezar sin nada y construirlo todo.
- *Civilization* y *Crusader Kings*: rebeliones, secesiones y el costo de dividir un reino.
- *Chat Wars* y TowerWars: la vida en torno a un castillo, con su chat y sus órdenes.

---

## 1. Día uno: el Claro

Al abrir el servidor **no hay ciudad**. En el Piso 1 hay un **Claro** con una fogata, un pozo, unos pocos PNJ supervivientes (una sanadora, un viejo constructor, una cazadora) y un montón de restos. Es todo.

- El tutorial **es** la fundación: el PNJ constructor te enseña a levantar un cobertizo, la cazadora a rastrear, la sanadora a vendar.
- Todo lo que después será una ciudad (posada, mercado, forja, sanatorio, el Castillo) **lo construyen los jugadores**, con materiales que **recolectan, cultivan, cazan y fabrican** ellos mismos.
- Los primeros en construir cada edificio quedan registrados para siempre como **Fundadores** ("Fundadora de la Primera Forja").

**Por qué conviene.** Los primeros días del servidor se vuelven historia compartida: cada jugador ve crecer la ciudad que ayudó a levantar, y su nombre queda en ella.

## 2. Las necesidades del asentamiento

Un asentamiento es como un organismo: **necesita cosas todos los días** y las consigue de los jugadores. Si le faltan, sus servicios empeoran.

| Necesidad | Quién la cubre | Si falta… |
|---|---|---|
| 🌾 **Comida** | Agricultores, ganaderos, cazadores, pescadores, cocineros | La población PNJ se va, la posada no cura, el estrés sube en toda la ciudad |
| 🪵 **Materiales** | Mineros, leñadores, canteros, refinadores | No se puede construir ni reparar |
| 🔨 **Herramientas y equipo** | Herreros, carpinteros, sastres, peleteros | Las estaciones públicas pierden nivel; los guardias pelean peor |
| 🛡 **Defensa** | Guerreros, guardias, constructores (murallas) | Las incursiones de monstruos entran (ver [Defensa](../09-construccion/defensa-y-protecciones.md)) |
| ⚕️ **Salud** | Médicos, alquimistas, herboristas | Las enfermedades se propagan; el sanatorio cierra |
| 🎶 **Ánimo** | Bardos, taberneros, cocineros (banquetes), festivales | Sube el estrés; menos gente se muda |
| ⚖️ **Orden** | Guardia, alcalde, investigadores | Aparecen garitos y ladrones; sube el crimen PNJ |
| 🪙 **Tesoro** | Impuestos, comercio | No se pagan las obras ni el mantenimiento |

Cada necesidad tiene una **barra semanal** visible para todos en `/ciudad`. El asentamiento publica pedidos ("*faltan 400 de trigo y 60 vendas esta semana*") que cualquiera puede cubrir a cambio de oro y reputación.

**No alcanza con cubrirlas una vez.** La comida, la salud, el ánimo, la defensa y el orden son **medidores con umbrales** que hay que sostener **día tras día**: la comida se come y se pudre, los inviernos cortan las cosechas, la falta de agua limpia y de higiene trae brotes, y los aldeanos PNJ llegan o se van según cómo esté la ciudad. Además, la riqueza, el tamaño y el ruido de la ciudad atraen **incursiones** de bestias y saqueadores cada vez más fuertes. Todo eso está en [Supervivencia del asentamiento](supervivencia-del-asentamiento.md).

**Por qué conviene.** Así **toda la infraestructura depende de farmear, fabricar y progresar**, y cada rol (agricultor, cazador, médico, bardo) es necesario de verdad. Ver [Red de sistemas](../00-vision/red-de-sistemas.md).

## 3. Crecer: del Claro al Castillo

| Etapa | Qué hace falta | Qué se desbloquea |
|---|---|---|
| **Claro** | — | Fogata, pozo, tutorial |
| **Campamento** | Primeras construcciones: cobertizos, huerto, corral, fogón | Descanso básico, primeras recetas |
| **Aldea** | Posada, mercado, forja, taller, enfermería | Mercado entre jugadores, estaciones públicas, oficios de rango Oficial |
| **Villa** | Muralla, templo, taberna, casa del consejo, banco | Gobierno (§4), impuestos, minijuegos de taberna, crédito |
| **Ciudad** | Sanatorio, academia, lonja de subastas, barrios | Subastas de puestos, investigación, cirugía segura |
| **Castillo** | El Castillo, con cada una de sus alas como obra aparte (ver [Ciudades y el Castillo](ciudades-y-castillo.md)) | Entrenadores de rango alto, la Fortuna, prisión, salón de embajadas |

Cada etapa es una **obra de servidor** (ver [Construcción](../09-construccion/gremios-y-organizaciones.md)). Pasar de Claro a Castillo debería llevar **semanas**, no días: es la primera temporada del juego.

**Construir no alcanza.** Terminar las obras de una etapa no la sube. Además hay que **sostener durante varios días seguidos** la población, la despensa, la salud pública y el ánimo mínimos de la etapa, y **superar incursiones** de bestias y enemigos de la zona; en la etapa de Castillo, también el **asedio de un monstruo grande**. Cada subida termina con una Noche de prueba, y una ciudad que no se sostiene puede **bajar de etapa**, aunque la propiedad personal de los jugadores nunca se pierde. Los requisitos completos están en [Supervivencia del asentamiento](supervivencia-del-asentamiento.md).

## 3.1 Nodos: los jugadores deciden dónde florece la civilización

**De dónde sale.** *Ashes of Creation* y su sistema de **nodos**: la actividad de los jugadores en una zona la hace crecer (campamento, aldea, pueblo, ciudad), y al crecer desbloquea servicios, mercado, gobierno y contenido. Los nodos vecinos quedan limitados, así que la comunidad decide dónde florece la civilización.

- **Cada piso tiene varios sitios de nodo** (5 a 10): lugares donde se puede fundar un asentamiento, cada uno con su geografía (ver [Geografía y recursos](geografia-y-recursos.md)).
- **Crecen con la actividad:** todo lo que hacen los jugadores en la zona de un nodo (misiones, recolección, fabricación, obras, comercio) suma **experiencia de nodo**. Con experiencia y con sus obras construidas, el nodo sube de etapa (§3).
- **Zona de influencia:** un nodo que crece limita a sus vecinos, que no pueden pasar de cierta etapa mientras él exista y se convierten en sus **vasallos** (aldeas que le pagan una parte de sus impuestos y reciben su protección). En un piso no puede haber dos ciudades pegadas: hay que elegir.
- **Decadencia:** si nadie sostiene un nodo (sin residentes activos, sin sus necesidades cubiertas), pierde experiencia, baja de etapa y termina en **ruinas**. Otro grupo puede refundarlo.
- **Destrucción:** los asentamientos en zonas rojas y negras se pueden **asediar y quemar** (ver [Defensa](../09-construccion/defensa-y-protecciones.md)). Al caer, los edificios quedan en ruinas y los vasallos quedan libres para crecer. Los campamentos de bandidos (ver [Crimen y justicia](../06-contenido/crimen-y-justicia.md)) son el primer ejemplo de asentamiento que se toma y se pierde; los gremios fundan asentamientos que crecen y que otros pueden quemar.

**Por qué conviene.** El mapa de la civilización lo dibujan los jugadores, cambia con el tiempo, y cada ciudad existe porque alguien la sostiene.

## 4. Gobierno

**De dónde sale.** *Wakfu* (Ankama, 2012): cada nación elige a un **gobernador** por voto popular, y el gobernador nombra cargos. Por ejemplo, un **Ecologista**, que dicta leyes sobre qué recursos se pueden recolectar para cuidar el ecosistema. También *Star Wars Galaxies*, con sus alcaldes de ciudades de jugadores.

Cuando el asentamiento llega a Villa, los residentes pueden **gobernarse**:
- **Gobernador (o alcalde):** se elige por **voto popular** cada temporada, con las **encuestas nativas de Telegram** en el grupo de la ciudad. Los candidatos se presentan con un mensaje fijado. Fija los impuestos locales (dentro de un rango), declara cuarentenas, da licencias (casinos, consultas, rutas) y decide qué obra va primero.
- **Cargos que nombra el gobernador:**

  | Cargo | Poder |
  |---|---|
  | **Ecologista** | Leyes de recolección: vedas de caza, cuotas de tala, qué especies se protegen o se cazan con recompensa (conecta con la ecología: ver [Mundo vivo](mundo-vivo-y-viaje.md)) |
  | **Tesorero** | Presupuesto de obras, pedidos semanales, tasas |
  | **Capitán de la Guardia** | Patrullas, redadas, contratación de guardias (ver [Crimen y justicia](../06-contenido/crimen-y-justicia.md)) |
  | **Maestro de Obras mayor** | Orden de las obras públicas y contratación de constructores |
  | **Juez mayor** | Preside el tribunal |
  | **Embajador** | Tratados con otros castillos |

- **Leyes:** el gobernador y sus cargos votan leyes de una lista (prohibir el juego ilegal, bajar impuestos a los agricultores, veda de ciervos este mes, recompensa por lobos).
- **Mandatos que vencen:** cada mandato dura una temporada, y nadie puede tener el mismo cargo más de **dos mandatos seguidos**. Si no, las mismas tres personas gobiernan para siempre y el juego muere.
- **Moción de censura:** los residentes pueden destituir al gobernador con una votación (ver [Crisis](crisis-problemas-y-soluciones.md)).
- **Residentes:** vota quien vive ahí (tiene casa o paga posada) y está activo.

## 5. El cisma: cuando un grupo se va

### 5.1 Cómo se decide

1. **Motivo.** Cualquier cosa: no les gusta el alcalde, quieren otra política, quieren fundar más arriba, rivalidades de gremios.
2. **Carta de fundación.** Un grupo redacta una carta (nombre, emblema y lugar del nuevo asentamiento) y la firma. Firmar es reenviar el mensaje de la carta al bot: el reenvío como firma (ver [Telegram](../01-plataforma/telegram.md)).
3. **Mínimo.** Hace falta que firme una cantidad mínima de residentes activos, por ejemplo el 15 % de la ciudad o 30 jugadores, lo que sea mayor, con al menos un Maestro de obras entre ellos.
4. **Anuncio.** El cisma se anuncia en la Gaceta y hay **7 días de plazo**: los que se van se preparan, los que se quedan pueden negociar para que no se vayan.
5. **Salida.** Pasado el plazo, los firmantes dejan de ser residentes del castillo original y fundan un **Claro nuevo** en otro lugar de un piso ya conquistado.

### 5.2 Qué se llevan y qué dejan

| | Se llevan | Dejan |
|---|---|---|
| **Personal** | Todo lo suyo: inventario, oro, oficios, casa (se desmonta y se vuelve materiales, perdiendo una parte) | — |
| **Común** | Una parte del tesoro de la ciudad, proporcional a lo que aportaron en impuestos y donaciones | Los edificios públicos: no se mueven |

### 5.3 Desventajas para el castillo que dejan

- **Menos manos:** las necesidades (§2) son las mismas, pero hay menos gente para cubrirlas, y algunos servicios pueden bajar de nivel.
- **Obras a medias:** si los que se van trabajaban en una obra, la obra se frena.
- **Mantenimiento:** los edificios siguen costando lo mismo, repartido entre menos.
- **Herida en el ánimo:** "Castillo dividido" durante unas semanas: más estrés y menos reputación.
- **Un vecino nuevo:** que puede ser aliado, competidor o enemigo.

### 5.4 Desventajas para los que se van

- **Empiezan de cero:** otro Claro, sin servicios, sin murallas.
- **Pierden reputación** con el castillo original (se recupera con el tiempo o con tratados).
- **Las incursiones de monstruos** llegan igual, con menos defensas.

**Por qué conviene.** Dividirse es una decisión **con peso**, no un botón. Pero es posible, y eso le da poder real a la comunidad. Las facciones no las decide el diseñador: **nacen de la historia del servidor**.

## 6. Después del cisma: relaciones entre castillos

| Relación | Qué implica |
|---|---|
| **Tratado comercial** | Menos impuestos entre sus mercados, caravanas protegidas |
| **Alianza** | Defensa mutua ante incursiones, bandas conjuntas |
| **Neutralidad** | Nada especial |
| **Rivalidad** | Guerra de castillos a hora fija por los puestos avanzados (ver [PvP](../06-contenido/pvp.md)) |
| **Reunificación** | Si los dos consejos lo votan, vuelven a ser uno y suman lo construido |

- **Tope de castillos:** para que el servidor no se fragmente en cien pueblos vacíos, hay un máximo de castillos activos (por ejemplo, 7, como los castillos de Chat Wars) y un tiempo mínimo entre cismas.
- **Un castillo que se vacía** baja de etapa; si queda sin residentes activos durante semanas, pasa a **ruinas** que otros pueden ocupar.

## 7. Todo en texto y por turnos

- `/ciudad` muestra la etapa, las barras de necesidades, las obras en curso y los pedidos de la semana.
- Las obras avanzan por **jornadas** con el minijuego de construcción (ver [Sistema de construcción](../09-construccion/sistema-de-construccion.md)).
- Las elecciones y las leyes se votan con **encuestas nativas** de Telegram.
- Las cartas de fundación se firman **reenviando** el mensaje.
- Todo lo importante sale en la **Gaceta**.

Ver P-54 y P-55 en [Preguntas abiertas](../00-vision/preguntas-abiertas.md).
