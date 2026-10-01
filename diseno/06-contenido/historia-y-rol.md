# Historia y rol: lo que hace largo al juego

> **Módulo** [06 · Contenido](README.md) · **Depende de:** [Creación de personaje](../03-personaje/creacion-de-personaje.md) (trasfondos), [Misiones y exploración](misiones-y-exploracion.md), [Roles y caminos de juego](../00-vision/roles-y-caminos-de-juego.md) · **Alimenta a:** [Progresión](../03-personaje/progresion.md), [Gremios y social](../08-social/gremios-y-social.md), [Campamentos](../02-mundo/fundacion-y-cisma.md) · **Estado:** §0 en el juego (capa simple, D-117, provisional); §1 a §3 son la propuesta completa

**De dónde sale.**
- *Fallen London* y las aventuras de texto: historias con decisiones, escritas para leerse en el teléfono.
- *World of Warcraft*: campañas por zona, facciones con reputación y títulos.
- *Dragon Age: Origins*: un origen propio para cada héroe, con su primera historia.
- *The Witcher*: dilemas cuyas consecuencias se ven después.
- *Chat Wars* y los MMO de rol en Telegram: el rol entre jugadores hace la comunidad.

**Qué pidió el dueño (1-oct-2026).** "No me interesa que el progreso sea lento. Quiero más bien que el juego sea un roleplay con RPG; o sea, debe ser largo." Se tomó así: **lo largo tiene que salir de la historia y del rol**, no de subir de nivel despacio. El progreso se siente seguido (siempre hay algo que ganar), y lo que dura años es todo lo que hay para vivir: la historia del mundo, el propio personaje, las facciones, los oficios, el campamento y el castillo.

---

## 0. En el juego: la capa simple (D-117, provisional)

Lo que ya se juega de §1. La historia es **datos**: misiones, personajes, facciones y encargos están en `content/story.yaml` y sus textos en `content/locales/es_historia.yaml`; el motor solo los hace andar (`engine/story/` y `engine/service/story.py`). Agregar una misión o un capítulo es escribir datos y textos, sin tocar el código.

### 0.1 Dónde se juega

- **📖 Historia** es el 6.º botón del menú de abajo (D-46 deja hasta 6; ⚙️ Opciones sigue último) y también **/historia**. Muestra:
  - tu origen y el capítulo, con la misión en que vas (por ejemplo, "misión 2 de 7");
  - **🎯 Ahora:** qué hacer en cada misión en curso y cuánto llevas ("🪓 Recolecta 🌿 Hierba curativa (2/4)"), o desde qué nivel empieza la siguiente;
  - los encargos de hoy cumplidos y cuándo cambian;
  - tu rango y tus puntos con cada facción;
  - los atajos: /diario, /bio, /saludar, /brindar.
- **Botones (4):** 🎯 Misiones · 🧑 Personajes · ⚜️ Facciones · 📔 Diario. Sin origen elegido, 🎭 Elegir origen toma el lugar de 📔 Diario (el diario sigue en /diario).
- **🎯 Misiones:** el texto del paso en curso de cada misión (lo que pasa, 2 a 5 líneas) y su objetivo. Si el paso es una decisión, sus opciones son los botones (hasta 3, más ↩️ Volver); si no, 📜 Encargos y ↩️ Volver.
- **🏕️ Campamento en el Claro:** 🛒 Mercader · 🛌 Posada · ⚒️ Oficios · **📜 Tablón**. El tablón tomó el lugar de ↩️ Volver (📍 Zona, en el menú de abajo, vuelve). También se abre con **/encargos** y desde 🎯 Misiones.
- **👤 Héroe:** la ficha suma tu origen (con el atajo /historia), el emblema de tu mejor oficio y tu biografía. Los títulos de la historia salen junto al de Pionero. Sigue con sus 4 botones.

### 0.2 🎭 El origen

- **Héroes nuevos:** después de confirmar la clase, el bot muestra los orígenes (3 por página, con ▶️ Más). Al tocar uno se ve su detalle y se confirma con ✅ Elegir. **Nunca bloquea:** con el menú de abajo se sigue jugando, y se elige después en 📖 Historia.
- **Héroes de antes:** la primera vez que abren 👤 Héroe o 📖 Historia después del parche, ven la elección una sola vez, sin perder nada; después, la ficha de siempre, y el origen queda en 📖 Historia → 🎭 Elegir origen.
- Cada origen da un **rasgo chico que nunca es de combate** (D-49), un **regalo** de una sola vez, su **cadena de 3 misiones** (niveles 1, 2 y 3) y, al terminarla, un **título**.

| Origen | Rasgo | Regalo | Su cadena | Título |
|---|---|---|---|---|
| 🪖 Soldado desertor | +15 % de experiencia de 🔪 Desollador | 2 🩹 vendas | «Botas de soldado» → «Herraduras al este» → «Una medalla en venta» | «Sin bandera» |
| 🛠️ Aprendiz de gremio | +10 % de experiencia en todos los oficios de refinado y de fabricación | 1 🟫 tablón y 1 🔩 lingote | «Manos que recuerdan» → «Las herramientas del maestro» → «Para cuando estés listo» | «Herencia del taller» |
| 🕳️ Huérfano de las Ruinas | El mercader del Claro le vende un 10 % más barato | 20 🥉 | «Ojos de la calle» → «Los túneles se mueven» → «Un nombre propio» | «Sombra de los túneles» |
| 🏵️ Noble caído | +10 % de reputación ganada con las facciones | 1 🥈 | «Un sello en la plata» → «Tierras que se fueron» → «Lo que hagas con él» | «Sangre sin tierra» |
| ⚕️ Curandero de aldea | +15 % de experiencia de 🌿 Herbolario | 3 🌿 hierbas curativas | «Manos que saben» → «Lo que trae el viento» → «La cura que faltó» | «Manos de hierba» |
| ⛏️ Minero de las vetas | +15 % de experiencia de ⛏️ Minero | 3 ⚙️ piezas de metal | «Polvo de mina» → «El sonido en lo hondo» → «Una veta que late» | «Oído de la veta» |

- El héroe despierta sin recuerdos (como siempre): el origen es **lo que recuerda**. Cada cadena presenta a los personajes del Claro y deja pistas del Colapso y de la Lejanía (el ámbar que late, la fiebre gris, los túneles que se mueven, los caminos de piedra).
- De [Creación de personaje](../03-personaje/creacion-de-personaje.md) §4 se tomaron 6 de los 8 trasfondos; el Juglar y el Cazador de recompensas quedan para más adelante. El "oficio a nivel 5" de §4 se cambió por un bono de experiencia de oficio (más parejo y sin saltarse rangos).

### 0.3 📖 Capítulo 1 · Las brasas del Claro (niveles 1 a 8)

Siete misiones en el Claro y sus alrededores. Terminan venciendo a **Raigambre**, el Guardián del Claro, y señalan lo que viene: bajo sus raíces hay un camino de piedra hacia el este (el Capítulo 2).

| # | Misión | Desde nivel | La da | Pasos | Premio de la misión |
|---|---|---|---|---|---|
| 1 | La fogata que no se apaga | 1 | 🍲 Marta | hablar · explorar 2 veces · llevarle 4 🪵 madera | 100 exp · 10 🥉 · 🔥 +15 |
| 2 | Todo vale algo | 1 | 🪙 Odo | hablar · vender 3 cosas · volver a hablar | 80 exp · 15 🥉 · ⚙️ +15 |
| 3 | Hierbas que recuerdan | 2 | 🌿 Iria | hablar · recolectar 4 🌿 hierbas · llevarle 3 | 138 exp · 10 🥉 · 2 🩹 · 🌀 +15 |
| 4 | Huellas al este | 2 | 🧭 Anselmo | hablar · llegar a Lejanía 2 · ganar 3 peleas · contarle | 229 exp · 20 🥉 · 🌀 +10 · 🔥 +5 |
| 5 | El ámbar que canta | 3 | ⚒️ Brena | hablar · fabricar o refinar 1 vez · **decisión 1** | 156 exp · 15 🥉 · 🔥 +10 |
| 6 | Raíces en el camino | 4 | 🧭 Anselmo | hablar · ganar 3 peleas en 🌲 bosque o 🐸 pantano · **decisión 2** · contarle | 348 exp · 20 🥉 · 🌀 +10 |
| 7 | El corazón de ámbar | 5 | 🍲 Marta | hablar · hablar con quien elegiste en la decisión 1 · llegar a la guarida · **vencer a Raigambre** · volver con Marta | 448 exp · 50 🥉 · las tres facciones +15 · título «Brasa del Claro» |

**Decisión 1 (misión 5): la astilla de ámbar que canta.**

| Opción | Reputación | Después |
|---|---|---|
| 🌿 Dársela a Iria | 🌀 +25 · 🔥 −5 | En la misión 7 te ayuda Iria: 2 🫙 ungüentos. Iria dice que la astilla repite "corazón" |
| ⚒️ Que Brena la funda | 🔥 +25 · ⚙️ −5 | En la misión 7 te ayuda Brena: 3 🔩 lingotes. Brena habla del hierro con vetas de ámbar |
| 🪙 Vendérsela a Odo | ⚙️ +25 · 🌀 −5 · 30 🥉 | En la misión 7 te ayuda Odo: 1 🥈. Brena le reprocha que el ámbar terminó en su bolsillo |

**Decisión 2 (misión 6): Tano, el chatarrero atrapado por las raíces.**

| Opción | Ahora | Después |
|---|---|---|
| 🫂 Cargar a Tano al Claro | ⚙️ +20 · 🔥 +10 | En la misión 7, Tano te da 50 🥉; Marta y Odo lo recuerdan |
| 🌀 Seguir el rastro | 🌀 +20 · ⚙️ −10 · 2 🌸 flores de luna | Tano no vuelve; Odo te lo reprocha |

- Las decisiones **se recuerdan para siempre** (Hero.story) y quedan en el diario. Cambian los saludos, quién te ayuda y el premio.
- Cada misión empieza hablando con quien la da, **en el Claro** (💬 Hablar en su ficha). Llevarle cosas (🤲 Entregar) se hace igual: se dan todas o ninguna.

### 0.4 🧑 Los personajes del Claro

| Personaje | Quién es | Facción | Su saludo cambia con |
|---|---|---|---|
| 🍲 Marta | La posadera de la Fogata | 🔥 La Llama Común | Si lo conoces, tu rango, la noche antes del bosque, si salvaste a Tano, el final |
| 🪙 Odo | El mercader | ⚙️ La Cofradía de los Restos | Si le vendiste el ámbar, qué pasó con Tano, tu rango, el final |
| 🌿 Iria | La sanadora | 🌀 El Círculo del Umbral | A quién le diste el ámbar, tu rango, el final |
| 🧭 Anselmo | El viejo explorador | 🌀 El Círculo del Umbral | Lo que descubriste de Raigambre, tu rango, el final |
| ⚒️ Brena | La herrera | 🔥 La Llama Común | Qué hiciste con el ámbar, tu rango, el final |

- Se ven en 📖 Historia → 🧑 Personajes (3 por página) o en 🏕️ Campamento → 📜 Tablón → 🧑 Personajes. ❗ marca a quien tiene algo para ti.
- Cada saludo es una línea que se elige por condiciones (misión hecha o en curso, decisión, rango con su facción, origen, si ya hablaron): gana la primera que se cumple (`content/story.yaml`, `npcs`).

### 0.5 ⚜️ Facciones y reputación

- 🔥 **La Llama Común** (guardar el fuego y reconstruir), 🌀 **El Círculo del Umbral** (la verdad y el poder de la Lejanía) y ⚙️ **La Cofradía de los Restos** (vivir de lo que quedó).
- La reputación sube y baja con las misiones, las decisiones y los encargos.

| Rango | Desde | 🔥 La Llama Común | 🌀 El Círculo del Umbral | ⚙️ La Cofradía de los Restos |
|---|---|---|---|---|
| Mal visto | menos de 0 | (los personajes lo dicen; no quita nada) | | |
| Desconocido | 0 | | | |
| Conocido | 100 | título «Al calor de la Llama» | título «Mirada del Umbral» | título «De la Cofradía» |
| Apreciado | 300 | 2 🧪 pociones y 3 🩹 vendas | 2 🧴 extractos y 1 🌸 flor de luna | 2 🔩 lingotes y 50 🥉 |
| Honrado | 700 | título «Guarda del Fuego», 1 🍷 poción mayor y 1 🧰 botiquín | título «Voz del Umbral», 2 🌸 y 2 🫙 ungüentos | título «Mano de los Restos», 1 💠 gema y 1 🥈 50 🥉 |
| Héroe | 1.500 | título «Corazón de la Llama Común» y 1 🩻 vendaje maestro | título «Testigo de la Lejanía» y 2 💠 gemas | título «Leyenda de los Restos» y 5 🥈 |

- Cada rango paga **una sola vez para siempre**, aunque después bajes y vuelvas a subir. Bajar de rango se avisa y no quita nada.
- Con el Capítulo 1 se llega a Conocido con la facción que más ayudaste; los rangos altos son metas de meses (encargos). Más adelante: recetas, equipo y lugares propios de cada facción, y campamentos y gremios alineados (§1.4).

### 0.6 📜 Encargos

**Del tablón (diarios).** Cada día real hay 3: **uno de cada facción**, sorteados con la semilla del mundo y el día (iguales para todos; cambian solos a medianoche UTC). Cuentan donde estés y pagan apenas se cumplen, una vez por día.

| Facción | Encargos posibles (quién los da: qué piden) |
|---|---|
| 🔥 | Marta: 8 🪵 madera o 8 🧵 fibra · Brena: 3 ⚙️ metal, 6 🪨 piedra o fabricar 1 vez |
| 🌀 | Iria: 5 🌿 hierbas · Anselmo: explorar 4 veces fuera del Claro, cazar 2 presas con 🏹 Cazar o ganar 3 peleas |
| ⚙️ | Odo: vender 5 cosas, explorar 3 veces fuera del Claro o 4 🏺 arcilla |

- **Premio:** experiencia = 10 × ⚡ que pide (2 a 6) × (1 + 0,15 × (tu nivel − 1)); monedas = 8 a 12 🥉 × (1 + 0,1 × (tu nivel − 1)); +10 de reputación con la facción de quien lo da.

**Del campamento (semanales).** Cada semana, 2 encargos para cada campamento (sorteados por semilla, semana y campamento), **entre todos sus miembros**: cuenta lo que hace cada uno, en cualquier lugar. Al llegar a la meta, cada miembro que aportó al menos 1 cobra el premio (aunque no esté conectado) y recibe el aviso. Es la "misión con los miembros del campamento" que pidió el dueño.

| Encargo | Meta entre todos | Premio a cada uno |
|---|---|---|
| ⚔️ Limpiar los caminos | 15 peleas ganadas | 60 exp y 30 🥉 |
| 🗺️ Conocer el territorio | 30 exploraciones | 60 exp y 30 🥉 |
| 📦 Acopio para el campamento | 60 cosas recolectadas | 60 exp y 30 🥉 |
| 🔨 Manos a la obra | 40 materiales a las obras o al conocimiento | 60 exp y 30 🥉 |
| 🌾 Llenar la despensa (desde nivel 3) | 20 raciones a la despensa | 60 exp y 30 🥉 |

### 0.7 📔 El diario del héroe

- Anota en tercera persona: el despertar, el origen, cada misión cumplida, cada decisión, el fin de un capítulo, la primera victoria contra un Guardián, el título de Pionero, el campamento que fundaste, los títulos y los rangos de facción. Guarda las últimas 200 entradas y muestra 12.
- **/diario** abre el tuyo (o 📖 Historia → 📔 Diario), con tu tarjeta arriba: nombre con emblema, clase, nivel, origen, biografía, títulos, rangos y encargos cumplidos.
- **📣 Mostrar en la zona** (o **/diario mostrar**) le manda tu tarjeta (con tus 5 últimos hechos) a los jugadores presentes en tu zona; **/diario Nombre** muestra la tarjeta de otro héroe. En Telegram, el mensaje también se puede reenviar.

### 0.8 🎭 Rol entre jugadores

- **/bio texto:** tu biografía, hasta 200 letras, en una línea. Sale en tu ficha y en tu tarjeta. /bio borrar la quita; /bio solo, la muestra.
- **/saludar** (a todos los de tu zona) o **/saludar Nombre**, y **/brindar** (o **/brindar tu brindis**, hasta 80 letras): una línea narrada ("👋 Lyra saluda a Bram.") que les llega a los jugadores **presentes en tu zona** (los de 👥 en 📍 Zona, D-96). Uno por minuto como mucho; si no hay nadie, avisa y no gasta la espera.
- **Emblema:** desde el rango 5 de un oficio, el emoji de tu mejor oficio va junto a tu nombre ("🩺 Lyra") en la lista 👥 de 📍 Zona, en los gestos y en tu tarjeta. La ficha lo explica ("🏷️ Emblema: 🩺 Medicina, rango 12, Aprendiz"). Es un emoji y no una palabra ("Médica") porque el héroe no guarda género (pregunta para el dueño).

### 0.9 Cómo avanza y cuánto da

- **Un solo gancho:** el juego avisa a la historia cuando pasa algo (`_story_event`): explorar, recolectar, ganar una pelea (con su bioma, si fue una presa de 🏹 Cazar o el Guardián), fabricar o refinar, vender, llegar a una zona, fundar un campamento, aportar a la despensa o a una obra. Las peleas automáticas de los lotes (D-114) cuentan igual.
- Un objetivo cuenta **desde que es el paso actual**; cada cosa que pasa avanza como mucho un paso. Los objetivos de estado (una zona explorada al 100 %, tener campamento, un nivel) se cumplen solos si ya está.
- El aviso de un paso o una misión cumplida sale **una vez**: en el resumen del lote, en el final de la pelea o en la pantalla.
- **Experiencia (D-108):** cada misión paga 20 × los ⚡ que pide (lo que da explorar por ⚡) × (1 + 0,15 × (nivel de la misión − 1)), una sola vez. El Capítulo 1 (57 ⚡) da ~1.500 y un origen (15 a 18 ⚡) ~400: juntos, un 16 % de lo que pide el nivel 8. Los encargos pagan la mitad por ⚡ y suman ~15 % al ritmo de un día entero. Registro en [Balance](../03-personaje/balance.md) §7. La velocidad de los niveles sigue en P-77.
- **Nunca:** poder de combate por la historia, botones de más (4 arriba, 6 abajo) ni pantallas que bloqueen.
- **Pruebas:** `tests/test_story.py`.

---

## 1. La capa simple para programar (en orden)

1. **🎭 El origen del héroe.** Al crearlo se elige de dónde viene, entre 5 o 6 trasfondos de [Creación de personaje](../03-personaje/creacion-de-personaje.md) §4: por ejemplo, superviviente del Colapso, hijo de artesanos, desertor o peregrino.
   - Cada origen da una frase de presentación, un rasgo chico (algo de oficio o de mundo, nunca de poder de combate) y su **cadena de misiones de origen**: 3 o 4 misiones narrativas que presentan el mundo y a sus personajes.
   - Los héroes ya creados lo eligen la primera vez que entran después del parche, sin perder nada.
2. **📖 La campaña principal por capítulos.** La historia del Colapso y del misterio de la Lejanía.
   - Cada capítulo tiene de 5 a 8 misiones narrativas con **decisiones que cambian algo**: la reputación con una facción, qué personaje te ayuda después, una recompensa u otra.
   - El capítulo 1 pasa en el Claro y sus alrededores, el 2 cuando se abre la región de Raigambre, y así con cada región y Guardián. Se escribe un capítulo por parche grande.
3. **🧑 Personajes con nombre.** El mercader, la posadera, una sanadora, un viejo explorador y un herrero del Claro tienen nombre, voz y diálogos cortos. Dan misiones, recuerdan lo que elegiste y cambian lo que te dicen.
4. **⚜️ Facciones y reputación.** Tres facciones al empezar (por ejemplo, los que quieren reconstruir, los que buscan el poder de la Lejanía y los que viven de lo que queda).
   - Las misiones, las decisiones y lo que haces suben o bajan tu reputación, por rangos: de Desconocido a Héroe.
   - Cada rango da algo: un título, una receta, una pieza de equipo o un lugar al que solo ellos te dejan entrar.
   - Más adelante, los campamentos y gremios se pueden alinear con una facción.
5. **📜 Encargos del tablón.** Encargos cortos de los personajes, que rotan cada día: cazar, recolectar, llevar algo o investigar. También hay **encargos de campamento**, que se hacen entre los miembros: es la parte de misiones con el campamento que ya estaba en la cola.
6. **📔 El diario del héroe.** Una crónica de lo que hiciste (el primer Guardián, el campamento que fundaste, las decisiones de la campaña, tus títulos), que puedes mostrar a otros jugadores.
7. **🎭 Rol entre jugadores** (de [Roles y caminos de juego](../00-vision/roles-y-caminos-de-juego.md) §3):
   - una biografía corta que escribes tú;
   - el emblema de tu rol junto al nombre ("⚕️ Lyra, Médica");
   - gestos narrados en tu zona (`/saludar`, `/brindar`, `/pregonar`);
   - la tarjeta de presentación reenviable.

## 2. El ritmo: progreso seguido, juego largo

- **Siempre hay algo cerca:** cada sesión corta da algo (un paso de misión, un rango de oficio, una mejora del campamento, un nivel en los primeros días).
- **Los niveles acompañan a la historia:** el nivel de cada capítulo marca el ritmo; no hace falta repetir lo mismo para pasar de un capítulo a otro.
- **Lo que dura años:**
  - la campaña completa, región por región;
  - los oficios hasta Gran Maestro;
  - el castillo con su gremio;
  - la reputación con todas las facciones;
  - las colecciones y los títulos;
  - el rol con los demás jugadores.
- **La velocidad de los niveles es decisión del dueño (P-77).** La propuesta: llegar al nivel 100 en unos 8 meses jugando todos los días, en vez de 2 años, sin cambiar que cada camino lleve al 100 a un ritmo parecido (D-108).

## 3. Cómo encaja con lo que ya está

| Lo que ya hay | Cómo lo usa la historia |
|---|---|
| El Claro, Raigambre, los biomas y los 105 enemigos | Escenarios y enemigos de los capítulos |
| Campamentos, gremios y oleadas | Encargos de campamento; capítulos donde tu campamento defiende algo |
| Oficios y beneficios | Misiones de oficio, recetas como premio de facción |
| Exploración y campamentos enemigos (en la cola) | Misiones de investigación e infiltración |
| Títulos y Pioneros | El diario y las recompensas de reputación |
