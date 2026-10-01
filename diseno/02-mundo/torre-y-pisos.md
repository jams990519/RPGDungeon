# La Torre: 100 pisos y cómo se sube de uno a otro

> **Módulo** [02 · Mundo](README.md) · **Depende de:** [Jefes](../06-contenido/jefes.md), [Misiones](../06-contenido/misiones-y-exploracion.md) · **Alimenta a:** [Progresión](../03-personaje/progresion.md), [Economía](../07-economia/economia.md), [PvP](../06-contenido/pvp.md) · **Estado:** se retira (D-58)

> **Se retira por D-58:** ya no hay Torre ni pisos. El mundo es un mapa infinito y viajar toma tiempo. Qué pasa con cada concepto de este documento está en [Mapa infinito y viaje](mapa-infinito-y-viaje.md), §4. El Colapso y las comunidades PNJ siguen (D-45): ver [El Colapso y las comunidades](el-colapso-y-las-comunidades.md).

**De dónde sale.**
- *Sword Art Online*: un castillo flotante de 100 pisos. Cada piso es un mundo con ciudades, campos y un laberinto que termina en el jefe, y el piso siguiente no existe para nadie hasta que alguien mata a ese jefe.
- *World of Warcraft*: zonas con núcleos de misiones, reputaciones, mazmorras y bandas por región. Y la apertura de las puertas de Ahn'Qiraj, donde todo el servidor juntó materiales durante semanas para abrir contenido nuevo.
- *Elden Ring*: jefes de campo opcionales, jefes ocultos, un mundo que se explora sin que te lleven de la mano.
- *Albion Online*: zonas por color de riesgo; cuanto más peligrosa, mejores recursos.

**Por qué conviene.** Una torre como mundo entero da tres cosas que un MMORPG de texto necesita:
- Una meta visible para todo el servidor (el Frente).
- Una progresión que se entiende en una frase ("voy por el piso 23").
- Un calendario de contenido natural: cada piso nuevo es una actualización.

---

## 1. Premisa (reemplazable)

Un mundo roto en cien pedazos quedó apilado en una torre que flota sobre la nada. Cada piso es un fragmento con su cielo, su clima y sus pueblos. Quien despierta en el Piso 1 es un **Ascendente**: lleva en el pecho una marca que solo se apaga en la Cima. Nadie sabe qué hay en el Piso 100. Los rumores dicen que quien llegue podrá rehacer el mundo, o salir de él.

**El Colapso (sigue vigente con el mapa infinito, D-45).** Los supervivientes llaman **el Colapso** al día en que el mundo se rompió. Desde entonces todo está en ruinas, el conocimiento de antes se perdió y los pocos que quedaron, todos PNJ, resisten en comunidades con sus propias reglas. Los Ascendentes despiertan sin nada junto a la fogata del Claro: pueden unirse a una comunidad o fundar algo nuevo ahí mismo. Qué causó el Colapso es parte del Gran Misterio (ver [Investigaciones](../06-contenido/investigaciones.md)). Todo esto está en [El Colapso y las comunidades](el-colapso-y-las-comunidades.md).

La premisa es original a propósito. Los **sistemas** de WoW, SAO y Elden Ring se pueden copiar; sus nombres, personajes, lugares y textos no (ver [Referencias, apartado legal](../99-referencias/referencias.md)).

## 2. Estructura: 100 pisos en 10 tramos

Cada **tramo** de 10 pisos tiene un bioma dominante, un tier de materiales (T1-T10), una capital con mercado grande y una banda.

| Tramo | Pisos | Bioma dominante | Nivel | Materiales | Especial |
|---|---|---|---|---|---|
| I | 1-10 | 🌲 Bosque Susurrante | 1-10 | T1 | Piso 1: el Claro, donde los jugadores fundan el primer castillo desde cero |
| II | 11-20 | 🌾 Pradera Dorada | 11-20 | T2 | Primeras zonas rojas y primer mercado regional |
| III | 21-30 | 💎 Cueva de Cristal | 21-30 | T3 | **Piso 25: el Primer Muro** |
| IV | 31-40 | 🐸 Pantano Putrefacto | 31-40 | T4 | Enfermedades de pantano y primeras zonas negras |
| V | 41-50 | 🏜️ Desierto Ardiente | 41-50 | T5 | Calor extremo. **Piso 50: el Gran Muro** |
| VI | 51-60 | 🏔️ Picos Helados | 51-60 | T6 | Frío extremo, aclimatación |
| VII | 61-70 | 🏛️ Ruinas Olvidadas | 61-70 | T7 | Arqueología mayor, pisos con reglas raras |
| VIII | 71-80 | 🔥 Ciudadela en Llamas | 71-80 | T8 | **Piso 75: el Muro de la Calavera** |
| IX | 81-90 | 🌑 Abismo Umbrío | 81-90 | T9 | Cordura, corrupción del Vacío |
| X | 91-100 | 🌸 Jardines Flotantes | 91-100 | T10 | La Cima. El Piso 100 cierra la primera era |

Las mazmorras y los laberintos de cada piso tienen cinco dificultades: **Normal, Profundidades, Corrompido, Abismal y Pesadilla** (ver [Mazmorras y bandas](../06-contenido/mazmorras-y-bandas.md)).

## 3. Anatomía de un piso

Todos los pisos tienen las mismas piezas, aunque cambien el tamaño y el tema. Al entrar ves un **mapa de nodos**: un grafo de 20 a 60 lugares conectados, no una cuadrícula. Se lee bien en texto y se navega con botones.

| Pieza | Zona | Qué hay | Al caer |
|---|---|---|---|
| **Asentamiento** (1-3 por piso) | 🔵 Azul | Posada, sanador, mercado local, entrenadores, tablón de misiones, estaciones de oficio, piedra de paso | No se combate |
| **Campos** | 🟡 Amarilla | Misiones, recolección básica del tramo, élites raros, eventos | Pierdes la Esencia que llevas (recuperable) |
| **Tierras salvajes** | 🔴 Roja | Recolección media, jefes de campo, campamentos enemigos | PvP libre; botín de la mochila |
| **Profundidades** (desde el tramo IV) | ⚫ Negra | Los mejores recursos del tramo, jefes ocultos, territorios de gremio | PvP libre; botín completo, con posible destrucción |
| **Laberinto** | Instancia | El camino al Guardián: 10-12 salas y una antesala | Como mazmorra |
| **Mazmorras** (1-2 por piso) | Instancia | Contenido para 5 | Como mazmorra |
| **Guarida del Guardián** | Instancia de mundo | El jefe que abre la escalera | Ver [Secuelas y muerte](../05-salud/secuelas-y-muerte.md) |

Las reglas por color y el karma están en [PvP](../06-contenido/pvp.md); lo que pasa al caer, en [Secuelas y muerte](../05-salud/secuelas-y-muerte.md).

**Por qué conviene.** Los pisos bajos son seguros de verdad y los altos peligrosos de verdad, pero *dentro* de cada piso hay un gradiente de riesgo. El jugador tranquilo nunca está obligado a entrar a una zona roja para avanzar. Los mejores materiales sí están ahí, y eso crea el comercio: el que arriesga vende al que no.

## 4. Cómo se sube de un piso al siguiente

Hay **dos capas**: una colectiva (todo el servidor empuja el Frente) y una personal (cada héroe gana su propio Sello).

### 4.1 Capa colectiva: el Frente

El **Frente** es el piso más alto que el servidor ha abierto. Un piso recién publicado pasa por cuatro fases:

| Fase | Qué hace el servidor | Duración orientativa | Origen |
|---|---|---|---|
| **1. Descubrimiento** | Explora el piso entre todos. Cada nodo que visita cualquiera suma al **mapa del servidor**. Al llegar al 100 % del camino principal aparece la entrada del Laberinto | 2-5 días | SAO (los que despejaban el frente mapeaban el laberinto) |
| **2. Esfuerzo de guerra** | Todos donan materiales y oro al **Campamento de Asalto** del piso, con una meta visible por material. Al completarse se abre la Guarida | 3-7 días | WoW (Ahn'Qiraj), Chat Wars |
| **3. Asalto** | El Guardián se abre como **jefe de mundo**. Cualquier grupo de 5 a 25 lo puede intentar. El primer grupo que lo mata es **Pionero del Piso** | Hasta que caiga | SAO, Elden Ring |
| **4. Asentamiento** | La escalera se abre y **los jugadores construyen** el asentamiento del piso nuevo (con constructores de rango y materiales de todos los oficios), y luego abren mercado y rutas. El Guardián queda como **Eco del Guardián** para quien llegue después | Permanente | SAO (los pisos conquistados se volvían habitables) |

- **Pioneros.** El grupo de la primera muerte recibe un título permanente ("Pionero del Piso 17"), un cosmético único e irrepetible y su nombre en la Gaceta y en una placa del asentamiento. Ningún poder: la recompensa es el prestigio.
- **Crédito por facción.** Las facciones compiten por cuántos Pioneros tienen, y eso suma trofeos de temporada a la [guerra de facciones](../06-contenido/pvp.md).
- **Ritmo de publicación.** El servidor no puede pasar del **techo de contenido**, que es el último piso publicado. A un piso cada 1-2 semanas, 100 pisos dan entre 2 y 4 años de progresión vertical.

### 4.2 Capa personal: el Sello del Piso

Que la escalera esté abierta no significa que cualquiera pueda subirla. Para cruzar, cada héroe necesita el **Sello** de su piso actual.

**Obligatorio: derrotar al Guardián.** Vale en un asalto de mundo, con una contribución mínima de daño, curación o mitigación. También vale en su **Eco**, una instancia con la misma mecánica que se abre después de la primera muerte.

**Además, 3 de estas 6 pruebas, a elección:**

| Prueba | Para quién | Ejemplo |
|---|---|---|
| **Campaña** | El que sigue la historia | Cadena principal del piso: 5-8 misiones narrativas con decisiones |
| **Cartografía** | El explorador | Visitar el 60 % de los nodos del piso, o comprarle los mapas a un cartógrafo |
| **Laberinto** | El que pelea | Completar el Laberinto del piso en dificultad Normal |
| **Reputación** | El constante | Llegar a "Amistoso" con el asentamiento del piso |
| **Contribución artesanal** | El artesano | Entregar un encargo de oficio del piso: una pieza, 20 pociones, una estructura |
| **Senda de sangre** | El jugador de PvP | Ganar batallas o mantener el control de campo en las zonas rojas del piso |

**Por qué 3 de 6.** Nadie queda bloqueado por una actividad que detesta. Un artesano puro sube sin pisar una zona roja; un jugador de PvP sube sin hacer la campaña. Pero todos pasan por el Guardián: el jefe es la prueba común.

### 4.3 Viento de cola: los que llegan tarde

Un piso recibe **Viento de Cola** cuando el Frente está **5 o más pisos por encima**:
- Las pruebas bajan de 3 de 6 a 2 de 6, y a 1 de 6 si la distancia pasa de 15.
- El Eco del Guardián pierde un 10 % de vida por cada 5 pisos de distancia, con tope de 30 %. **La mecánica no cambia**: mismo jefe, mismo patrón.
- La experiencia en ese piso sube un 25 %.
- Los materiales de tramos viejos bajan de precio solos, porque sobra oferta.

**Origen:** los sistemas de puesta al día de WoW. **Por qué conviene:** en un servidor de dos años, quien llega en el mes 18 tiene que alcanzar a sus amigos en semanas, no en meses, sin que el contenido viejo pierda su identidad.

### 4.4 Nivel y piso van juntos

- Cada piso está pensado para **nivel ≈ número del piso** (±2).
- **Techo del Piso:** la experiencia baja al 10 % cuando tu nivel supera en 5 al piso de tu último Sello. No puedes llegar a nivel 40 farmeando el piso 12.
- Así, el nivel máximo del servidor en cada momento es en la práctica el Frente + 5. Cuando se publique el piso 100, el nivel 100 tendrá sentido.

## 5. Pisos especiales

| Piso | Qué lo hace distinto |
|---|---|
| **1 · El Claro** | Al lanzar no hay ciudad: solo una fogata y unos PNJ supervivientes. El tutorial es construir el primer asentamiento entre todos, hasta que llegue a Castillo (ver [Fundación y cisma](fundacion-y-cisma.md)). Aquí se eligen raza y trasfondo; la clase llega en el nivel 10. Zona azul y protección de novato |
| **Cada 10 · Capitales** | Al conquistarlo, el servidor construye aquí una capital con su Castillo (mercado regional, banco, entrenadores de oficios mayores, barrios de cada castillo). Aquí se abre la banda del tramo |
| **25, 50 y 75 · Los Muros** | En SAO fueron los pisos más sangrientos. Aquí son jefes de tramo con dos o tres fases estilo Elden Ring y un esfuerzo de guerra del doble de tamaño. El asalto pide varios grupos en frentes paralelos: uno contiene a los invocados mientras otro rompe la postura del jefe |
| **100 · La Cima** | Fin de la primera era. La primera muerte del jefe final cierra la temporada larga y abre la siguiente era, con torre e historia nuevas; los héroes conservan lo suyo |

## 6. Lecciones de TowerWars aplicadas aquí

- TowerWars tiene 50 pisos con nombre que se repiten en ciclos, y desde el piso 40 la dificultad deja de crecer. Aquí son **100 pisos únicos sin ciclos**, publicados de a poco.
- Su Torre en solitario (un pasillo de peleas más un jefe, que se puede repetir) funciona como base del **Laberinto** y de las [Profundidades](../06-contenido/misiones-y-exploracion.md).
- Su Torre de Gremio (oleadas más un jefe con fases, rondas de 90 s) es la base del **Asalto** y las bandas.

Ver P-07, P-08, P-09 y P-16 en [Preguntas abiertas](../00-vision/preguntas-abiertas.md).
