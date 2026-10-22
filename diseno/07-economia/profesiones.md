# Profesiones

> **Módulo** [07 · Economía](README.md) · **Depende de:** [Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md) (vetas), [Economía](economia.md) · **Alimenta a:** [Equipamiento](../03-personaje/equipamiento.md), [Salud](../05-salud/README.md), [Fabricación](fabricacion.md) · **Estado:** §0 en el juego (fase 1, D-109, ver §0.1; beneficios §0.2 y §0.4, con la obra maestra y los muebles de D-116; fase 2 del lado del campamento, D-115: 🎣 Pescador, 🍲 Cocina, 🗿 Cantería y 🏗️ Construcción, ver §0.4; el ✨ Encantamiento y el artesano de cabeza, manos, piernas y pies de la fase 2 de D-115, §0.5; las 🎓 especializaciones de D-141, §0.6 y §5; la reforma de recetas de D-306 en la 0.44: tramos cada 5, colores de receta y 📚 libros, §0.8; en la 0.52, también en el refinado, la ⚗️ Alquimia, la 🩺 Medicina y la 🍲 Cocina, §0.11; desde la 0.57, 🔧 reparar el equipo y los 📜 encargos de reparación, §0.12; desde la 0.59, los 📜 pedidos de fabricación, §0.13); el resto, propuesta

> **Repaso del 2-oct-2026 (D-194, D-195):** el dueño redefinió los oficios: refinar pasa a ser estructuras del asentamiento, cuatro oficios de armadura (tres desde D-208: ya no hay malla), oficios nuevos (Ladrón, Agricultura, Ganadería; el Mallero se cayó con D-208) y la granja de cada etapa. El 2-oct también decidió que el Joyero refina las gemas desde la mena del Minero, sin Gemólogo (D-198), y que las ranuras para gemas van solo en armaduras y armas (D-199). Ver [Repaso de los oficios](oficios-repaso-2-oct.md). Hasta que se programe, este documento describe lo que está en el juego.

**De dónde sale.**
- *World of Warcraft*: profesiones primarias (Minería, Herboristería, Desuello, Herrería, Peletería, Sastrería, Ingeniería, Alquimia, Encantamiento, Joyería, Inscripción) y secundarias (Cocina, Pesca, Arqueología, Primeros Auxilios). Desde *Dragonflight*: especializaciones, conocimiento semanal y pedidos de fabricación.
- *Albion Online*: recolección por tiers, paso de refinado, maestría por cada tipo de objeto, Enfoque diario, ciudades con bonos de fabricación, granjas y animales.
- *Final Fantasy XIV*: cada oficio es casi una clase, con un minijuego de fabricación por turnos.
- *Star Wars Galaxies*: recursos con estadísticas que cambian según dónde y cuándo aparecen; experimentación; oficios sociales (animador, médico).
- *RuneScape*: habilidades de 1 a 99 (y hasta 120) que llevan años. El 99 pide 13 millones de experiencia.
- *Black Desert*: trabajadores PNJ y nodos.
- *EVE Online*: investigación de planos.
- *Ultima Online*: un tope total de habilidades que obliga a elegir.
- *Dofus*: oficios de recolección y fabricación dentro de un MMO por turnos.

**Por qué conviene.** Quien no quiera pelear tiene que poder jugar dos años siendo herrero, médico o comerciante, y ser **necesario** para los demás.

---

> **0.39.2 (D-298, orden del dueño):** 💱 Comercio está **bloqueado** hasta que existan las caravanas: no se ve, no se aprende, no sube al vender y no da beneficio (tampoco sus 🎓 especializaciones). Lo que sigue sobre el Comercio describe cómo era y cómo volverá a abrirse. El rango ganado queda guardado.

## 0.0 Los oficios se aprenden (D-257, en el juego desde la 0.33)

El dueño pidió (17-oct): "cocina es una profesión: no debería salirme hasta que yo no aprenda la profesión… cuando yo le doy a aprender, voy a pagar por la primera receta". Y: "el jugador va a ir aprendiendo recetas a medida que va haciendo recetas".

- **Sube solo, sin aprenderse:** solo la 🧭 exploración (`learn: auto` en `content/professions.yaml`). **Desde la 0.35 (D-272)** la 🪓 recolección (🪓 Leñador, ⛏️ Minero, 🌿 Herbolario, 🎣 Pescador) también se aprende: el dueño, el 18-oct, "Herbolario es una profesión que tienes que aprender… solamente van a tener exploración… porque farmear te va a dar recursos base". Sin el oficio, recolectar da igual los recursos base, pero no la unidad de más, los hallazgos raros ni la experiencia. Quien ya tenía experiencia en uno lo conserva aprendido (`grandfather: true`).
- **Se aprenden una vez:** todos los demás, también el 🔪 Desollador (sin él, las bestias dan su botín de siempre, sin la unidad de más), el 💱 Comercio (sin él, se vende igual, sin las monedas de más), el ✨ Encantamiento y la 🏗️ Construcción (esta, siendo miembro de un campamento).
- **Dónde:** en 🔬 Investigar del Claro o en 🧑‍🏫 Entrenador → 📚 Aprender oficios. Cada oficio tiene su código (/cocina); su pantalla dice qué hace, su primera receta y lo que cuesta.
- **Cuánto:** su primera receta. **Desde la 0.43 (D-306.4):** 🥈1 los de fabricación (y ✨ Encantamiento) y 🥉50 los de recolección y refinado (y 🏗️ Construcción) (`professions.learn_price`, un precio por rama; antes 🥉20 todos, P-231). Gratis si ya lo practicabas antes: conservas tu rango (D-64).
- **Títulos (desde la 0.43, D-306.1):** al tope de tu título (20, 40, 60, 80, 95) el oficio no guarda experiencia hasta que compras el siguiente en 🧑‍🏫 Entrenador → 🎖️ Títulos. Ver §0.7.
- **Qué abre:** el oficio en rango 1, con todas sus recetas de rango 1. Las demás se abren **haciendo recetas**, rango por rango, como hasta ahora; desde la 0.44 (D-306), las de rango 25, 50 y 75 o más piden además su 📚 libro de recetas del Entrenador (§0.8).
- **Sin aprenderlo:** rango 0. No se hace ninguna de sus recetas, no da beneficio ni especialización y no sube. La experiencia de antes queda guardada (`Hero.professions`); lo aprendido, en `Hero.learned`.
- **📋 Mis oficios:** una línea corta por oficio que tienes ("⛏️ Minero · rango 2 (Aprendiz) ▓▓▓▓░░░░ 55 %  /minero"). Lo largo (qué junta, su beneficio, lo que abre el próximo rango, sus especializaciones) sale tocando el código.
- **🛠️ Fabricar** muestra lo mismo, corto, y las estaciones. Ya no lista los oficios "sin empezar": esos están en 📚 Aprender oficios.

## 0. Fase 1 para programar (D-109)

El dueño pidió (1-oct-2026) preparar los oficios **como en World of Warcraft**: para que un carpintero avance hace falta un recolector y alguien que refine; para crear pociones hace falta herbología y alquimia; los joyeros y los guerreros necesitan lo que hacen otros. **Que avanzar no dependa de una sola cosa y que 50 jugadores tengan tareas distintas, con mucha variedad.** Sigue valiendo D-57: no hay tope duro de oficios (desde la 0.33 cada uno se aprende una vez, §0.0); quien quiere serlo todo avanza mucho más lento que el especialista, porque cada oficio pide su tiempo, sus materiales y su estación.

Esta es la **capa simple** que se programa primero, con los recursos que ya hay en el juego. El resto de este documento (maestría por objeto, exámenes, enfermedades laborales) queda como capa profunda, para después. Las especializaciones ya están en su capa simple (§0.6).

**Las tres capas, en chico:**

| Recolección (sube al recolectar) | Refinado (en una estación) | Fabricación (pide materiales de 2 o más ramas) |
|---|---|---|
| 🪓 **Leñador:** 🪵 madera | **Aserradero:** madera → tablón | **Carpintería:** arcos, bastones y escudos (tablones + tela o cuero) |
| ⛏️ **Minero:** piedra, metal, arcilla; desde un rango, gemas en bruto | **Fundición:** metal → lingote | **Herrería:** armas y placas (lingotes + cuero para el mango) |
| 🌿 **Herbolario:** hierba curativa, fibra; desde un rango, flores raras | **Destilación:** hierbas → extracto · **Tejeduría:** fibra → tela | **Alquimia:** pociones (extracto + arcilla para el frasco) · **Sastrería:** túnicas y vendas (tela) |
| 🔪 **Desollador:** carne y piel de las bestias | **Curtiduría:** piel → cuero | **Peletería:** armaduras de cuero (cuero + tela) · **Joyería:** anillos y joyas (lingote + gema) |

**Reglas de la fase 1:**
- **Cada oficio tiene su rango, de 1 a 100,** que sube haciéndolo. Los rangos abren recetas y materiales mejores (Aprendiz, Oficial, Experto, Artesano, Maestro, Gran Maestro, como en el §4). Los recolectores juntan un poco más con cada rango.
- **Nadie es autosuficiente por diseño:** casi toda receta útil pide materiales de dos ramas o más. El herrero necesita al curtidor; el alquimista, al herbolario y al minero (arcilla); el joyero, al minero y al fundidor.
- **Refinar y fabricar gastan energía** como toda acción fuera del combate (D-78), y dan experiencia de héroe a un ritmo parecido al de los otros caminos (D-108): un artesano también llega al nivel 100.
- **Lo fabricado compite con el botín:** el equipo de artesano de rango alto es tan bueno como el de los jefes de su nivel, o mejor en algo. Así el artesano es necesario.
- **Comerciar entre jugadores** es la pieza que hace que se necesiten: un mercado sencillo en el Claro (y en los campamentos que lo construyan) donde cada uno pone a la venta lo que hace y otros lo compran con 🥉. Va en una segunda tanda, apenas esté la cadena.
- **Las estaciones:** el Claro tiene las básicas; las mejoras del campamento (D-101) suman las suyas (taller, fragua, alambique), con algo más de rendimiento.

**De dónde sale:** *World of Warcraft* (oficios primarios que se necesitan entre sí), *Albion Online* (el paso de refinado) y *Dofus* (oficios dentro de un juego por turnos).

### 0.1 En el juego (fase 1)

> **Desde la 0.29 (D-191, D-192):** el **🧑‍🏫 Entrenador** de 🏕️ Campamento (y /entrenador) presenta los oficios por familia, cuántos puedes empezar hoy y lo que llega después (🎓 especializaciones al 25 y al 75, 🏗️ Construcción con tu campamento, recetas nuevas con cada rango). En el centro de 🏕️ Campamento, **🛠️ Fabricar** abre ⚒️ Oficios y **🍲 Cocinar** abre la estación de la 🍲 Cocina con solo sus recetas. Ver [Menús](../01-plataforma/menus-campamento-y-heroe.md) §2 y §4.

Lo que ya está programado. El catálogo vive en `content/professions.yaml` (oficios, estaciones y recetas), los números en `content/balance.yaml` → `professions` y las cuentas en `engine/professions/`. Cada héroe guarda la experiencia de cada oficio (`Hero.professions`); los héroes de antes empiezan todos los oficios en rango 1.

**Los oficios.** Los 15 de la fase 1, la 🩺 Medicina, el 🧭 Explorador, el 💱 Comercio y los 4 de la fase 2 del lado del campamento (D-115, marcados "fase 2"). No hay tope: cualquiera puede subirlos todos (D-57).

| Rama | Oficio | Cómo sube |
|---|---|---|
| Recolección | 🪓 Leñador | 1 de experiencia de oficio por cada 🪵 madera recolectada (también con 🪓 Talar, que junta solo madera, desde la 0.42: D-305) |
| | ⛏️ Minero | 1 por cada 🪨 piedra, ⚙️ metal o 🏺 arcilla; desde el rango 10, 💠 gemas en bruto |
| | 🌿 Herbolario | 1 por cada 🌿 hierba curativa o 🧵 fibra; desde el rango 10, 🌸 flores de luna |
| | 🔪 Desollador | 1 por cada 🍖 carne o 🦌 piel que sueltan las bestias al vencerlas |
| | 🎣 Pescador (fase 2) | 1 por cada 🐟 pescado, que sale en las zonas con agua: todo el 🐸 pantano y 3 de cada 10 zonas de 🌲 bosque y de 🌾 pradera (ríos y lagunas) |
| Exploración (D-112) | 🧭 Explorador | 5 por cada vuelta de 🔎 exploración y 6 más al dejar una zona al 100 %; 15 por cada 🕵️ infiltración; 12 por cada 🔭 reconocimiento de lejos (D-172); 30 por cada 🗺️ pergamino de mapa (D-326, desde el rango 15). Con el rango ve más en el mapa ([Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md) §1.14) |
| Refinado | 🪚 Aserradero · 🔥 Fundición · 💧 Destilación · 🧶 Tejeduría · 🪣 Curtiduría · 🗿 Cantería (fase 2) | 6 por cada vez que refinas en una estación |
| Fabricación | 🪑 Carpintería · 🔨 Herrería · ⚗️ Alquimia · 🪡 Sastrería · 🦺 Peletería · 💍 Joyería · 🩺 Medicina · 🍲 Cocina (fase 2) | 12 por cada pieza de equipo (6 por las vendas y la poción de vida, 8 por la poción mayor); la Cocina, 6 por cada ⚡ |
| Artes arcanas (fase 2 de D-115) | ✨ Encantamiento | 6 por cada pieza que desencantas (1 ⚡) y 12 por cada encantamiento (2 ⚡). Sin estación: desde 🛡️ Equipo → una pieza → ✨ Encantamiento, o con /encantar (§0.5) |
| Servicio | 💱 Comercio (D-116) · 🏗️ Construcción (fase 2) | El Comercio, 1 por cada 🥉 que cobras vendiendo; la Construcción, 1 por cada material que aportas a una obra de tu campamento o a reparar sus defensas (un 🟫 tablón o un 🧱 sillar, 3: lo crudo que lleva) |

**Rangos.** Experiencia de oficio total para el rango R = 9 × (R − 1)². Rango 10: 729 · 25: 5.184 · 50: 21.609 · 100: 88.209. Quien dedica toda su energía a un oficio de refinado o fabricación junta unos 240 por día: rango 25 en ~3 semanas, 50 en ~3 meses, **100 en ~1 año** (§4). Un recolector dedicado llega al 100 en 9 a 11 meses (junta más unidades por vuelta a medida que sube de nivel). Títulos: Aprendiz (1), Oficial (21), Experto (41), Artesano (61), Maestro (81), Gran Maestro (96). Los exámenes del §4 son capa profunda.

**Recolectar con oficio.** Cada rango suma 0,3 % de sacar una unidad más por unidad recolectada (rango 50: 15 %; rango 100: 30 %), sin pasar el espacio de la mochila (D-90). Desde el rango 10, cada vuelta en la que el minero junta algo de lo suyo tiene 5 % de dar una 💠 gema en bruto, +0,15 % por rango (18,5 % en el 100); lo mismo el herbolario con la 🌸 flor de luna. El desollador saca carne y piel del botín de las bestias, con la misma unidad extra por rango. Las unidades extra y los raros usan su propio sorteo: no cambian lo que la vuelta o la pelea dan.

**🦌 Piel.** Toda bestia que suelta carne suelta también piel, con 10 puntos menos de probabilidad que su carne (30 a 50 %, 1 o 2). Humanoides, no muertos, hongos y limos, nunca.

**Refinar** (1 ⚡ por vez; lo que sale vale en el mercader lo mismo que lo que entra, así refinar no fabrica monedas):

| Receta | Entra | Sale |
|---|---|---|
| Aserradero | 🪵 madera ×3 | 🟫 tablón |
| Fundición | ⚙️ pieza de metal ×2 | 🔩 lingote |
| Destilación | 🌿 hierba curativa ×3 | 🧴 extracto |
| Tejeduría | 🧵 fibra ×3 | 🧣 tela |
| Curtiduría | 🦌 piel ×2 | 🟤 cuero |
| 🗿 Cantería (fase 2) | 🪨 piedra ×3 | 🧱 sillar |

Al refinar, cada rango suma también 0,3 % de sacar una unidad más, y en las estaciones de tu campamento, +10 %.

> **Desde la 0.44 (D-306, §0.8):** en los 5 oficios de equipo hay un tramo cada 5 rangos (la pieza es del nivel del tramo: las de la tabla de abajo bajaron al rango 1, 5 o 10), las piezas cuestan 2, 3 o 4 ⚡ y dan de 12 a 24 de experiencia según el tramo, con colores de receta; las recetas de rango 25, 50 y 75 o más de cualquier oficio piden su 📚 libro de recetas; la malla se retiró y la Joyería empieza con el 📿 Colgante de cobre (sin gema). Las tablas de abajo muestran los materiales, que no cambiaron.

**Fabricar** (2 ⚡ por pieza de equipo; 1 ⚡ las vendas, la poción de vida y la poción mayor; 2 ⚡ la tanda de pociones mayores). Toda receta pide materiales de **dos oficios o más**; cada oficio de fabricación tiene recetas en los rangos 1, 25 y 50 (y los de equipo, también del 55 al 100: más abajo):

| Oficio | Rango 1 | Rango 25 | Rango 50 |
|---|---|---|---|
| 🪑 Carpintería (y sus 🪑 muebles, D-116: ver §0.4) | Bastón de roble (tablón ×3, tela) · Arco de olmo (tablón ×3, cuero) | Bastón labrado (tablón ×5, tela ×2) · Arco reforzado (tablón ×5, cuero ×2) | Báculo del artesano (tablón ×8, tela ×3, gema) · Arco del artesano (tablón ×8, cuero ×3, tela) |
| 🔨 Herrería | Espada forjada (lingote ×3, cuero) · Daga forjada (lingote ×2, cuero) · Peto forjado (lingote ×4, cuero ×2) | Espada, daga y peto templados (lingote ×5/×4/×7, cuero ×2/×2/×3) | Espada y daga del artesano (lingote ×8/×6, cuero ×3, gema) · Coraza del artesano (lingote ×10, cuero ×4, tela ×2) |
| ⚗️ Alquimia | Poción de vida ×2 (extracto, arcilla) | 🍷 Poción mayor (extracto ×2, arcilla, flor de luna) | Poción mayor ×2 (extracto ×3, arcilla ×2, flor de luna) |
| 🪡 Sastrería | Vendas ×3 (tela, hierba curativa) · Túnica de viajero (tela ×4, cuero) | Túnica teñida (tela ×6, extracto) | Túnica del artesano (tela ×9, extracto ×2, flor de luna) |
| 🦺 Peletería | Jubón de cuero (cuero ×4, tela) · Cota ligera (cuero ×2, lingote ×2) | Jubón reforzado (cuero ×6, tela ×2) · Cota remachada (cuero ×3, lingote ×4) | Jubón del artesano (cuero ×9, tela ×3, extracto) · Cota del artesano (cuero ×5, lingote ×7, tela ×2) |
| 💍 Joyería | Anillo engarzado (lingote, gema) | Collar de gemas (lingote ×2, gema ×2) | Amuleto del artesano (lingote ×3, gema ×3) |
| 🍲 Cocina (fase 2; también rangos 75 y 100, ver §0.4) | 🍱 Ración del campamento (carne, hierba) · 🍢 Pescado asado (pescado ×2, madera) | 🥘 Guiso del cazador (carne ×2, pescado ×2, hierba) | 🥫 Conservas en tarro (carne ×3, pescado ×3, arcilla, extracto) |

**Rangos 55 a 100: el equipo hasta el nivel 100 (D-110, D-113).** Cada línea de equipo (bastón y arco en la Carpintería; espada, daga y peto en la Herrería; túnica en la Sastrería; jubón y cota en la Peletería; joya en la Joyería) suma una receta por nivel de pieza, del nivel 10 al 100, una cada 5 rangos: **nivel de pieza 10 → rango 55, 20 → 60 … 100 → rango 100** (90 recetas). Piden lo refinado de 2 ramas o más, y más 💠 gemas y 🌸 flores de luna en los niveles altos; cuestan 2 ⚡ y dan 12 de experiencia de oficio, como las demás piezas (el ritmo de D-108 no cambia):

| Línea | Nivel 10 (rango 55) | Nivel 50 (rango 75) | Nivel 100 (rango 100) |
|---|---|---|---|
| 🪑 Bastón | tablón ×9, tela ×3, gema | tablón ×13, tela ×5, gema ×2, flor de luna | tablón ×21, tela ×8, gema ×4, flor de luna ×2 |
| 🪑 Arco | tablón ×9, cuero ×3, tela | tablón ×15, cuero ×5, tela ×2, gema | tablón ×22, cuero ×8, tela ×4, gema ×3 |
| 🔨 Espada · Daga | lingote ×9 / ×7, cuero ×3, gema | lingote ×13 / ×11, cuero ×5, gema ×2 | lingote ×18 / ×16, cuero ×8, gema ×4 |
| 🔨 Peto (placas) | lingote ×11, cuero ×4, tela ×2 | lingote ×15, cuero ×6, tela ×3, gema | lingote ×20, cuero ×9, tela ×5, gema ×3 |
| 🪡 Túnica (tela) | tela ×10, extracto ×2, flor de luna | tela ×15, extracto ×4, flor de luna ×2 | tela ×24, extracto ×7, flor de luna ×4 |
| 🦺 Jubón (cuero) | cuero ×10, tela ×3, extracto | cuero ×14, tela ×5, extracto ×2, gema | cuero ×21, tela ×8, extracto ×4, gema ×3 |
| 🦺 Cota (malla) | lingote ×8, cuero ×5, tela ×2 | lingote ×12, cuero ×7, tela ×3, gema | lingote ×17, cuero ×10, tela ×5, gema ×3 |
| 💍 Joya | lingote ×3, gema ×3 | lingote ×6, gema ×6, flor de luna | lingote ×8, gema ×11, flor de luna ×3 |

En 🛠️ Fabricar, las recetas de rango más alto salen primero (cada línea llega a tener 13).

**Cabeza, manos, piernas y pies (fase 2 de D-115).** La pasada de balance dejó lo mejor de cada nivel en manos de los artesanos solo en arma, pecho y joya. Ahora las otras cuatro ranuras también tienen equipo de artesano: **una pieza por tipo de armadura y por nivel de pieza** (3, 5, 8 y del 10 al 100), con los mismos rangos que el pecho de su tipo (nivel 3 → rango 1, 5 → 25, 8 → 50, y del 10 al 100 → rangos 55 a 100). Son **208 piezas y 208 recetas** (cada receta tiene el mismo id que la pieza que sale, por ejemplo `artesano_cabeza_placas_4`):

| Tipo | Oficio | Piezas (cabeza · manos · piernas · pies) | Materiales |
|---|---|---|---|
| Tela | 🪡 Sastrería | Tocado · Manguitos · Faldones · Zapatillas | 🧣 tela con 🟤 cuero (nivel 3) o 🧴 extracto (desde el 5), y 🌸 flor de luna desde el 8 |
| Cuero | 🦺 Peletería | Caperuza · Brazales · Zahones · Polainas | 🟤 cuero, 🧣 tela, 🧴 extracto desde el nivel 8 y 💠 gema desde el 40 |
| Malla | 🦺 Peletería | Almófar · Muñequeras · Perneras · Botines | 🔩 lingote, 🟤 cuero, 🧣 tela desde el nivel 8 y 💠 gema desde el 40 |
| Placas | 🔨 Herrería | Celada · Avambrazos · Musleras · Sabatones | 🔩 lingote, 🟤 cuero, 🧣 tela desde el nivel 8 y 💠 gema desde el 40 |

- **Nombres:** "de aprendiz" (nivel 3), "de oficial" (5), "del artesano" (8) y, del 10 al 100, los mismos lugares que el resto del equipo (de la frontera, del páramo … del alba eterna).
- **Bonos:** en los niveles 3, 5 y 8, los del botín de su nivel y un bono chico; del 10 al 100, 🟣 épicas con cada bono del botín de su nivel × 1,1 (redondeado) y un bono que el botín no tiene: **+1 % de ataque** en cabeza, piernas y pies (+2 % desde el nivel 60) y **+1 de defensa** en las manos. Siempre superan al botín de su nivel.
- **Materiales:** los del pecho de artesano de su tipo y nivel, en proporción al precio de la pieza (cada pieza chica vale ~75 % del pecho), con al menos 1 de cada uno. Por ejemplo, la celada del nivel 100 pide lingote ×15, cuero ×7, tela ×4 y gema ×2 (el peto, ×20, ×9, ×5 y ×3). Como el resto, se venden al mercader por menos que sus materiales y tienen su ✒️ obra maestra (con +1 % de ataque de más en cabeza, piernas y pies y +1 de defensa en las manos).

**El equipo de artesano** usa el sistema de equipo de siempre (ranuras, tipos, rarezas, nivel) y es **lo mejor de cada nivel** en arma, pecho y joya (D-113): rango 1 = como el botín poco común del nivel 3 y un bono chico (+1 % de vida en las armas, +1 % de ataque en las armaduras, +1 % de defensa en las joyas; desde D-113); rango 25 = como el raro del nivel 5 y un bono más (+2 % de vida en las armas, +1 % de ataque en las armaduras, +1 % de defensa en las joyas); rango 50 = como el épico del nivel 8 y algo más (+3 % de vida en las armas, +2 % de ataque en las armaduras, +2 % de defensa en las joyas); rangos 55 a 100 = 🟣 épicas con ~10 % más que el botín de su nivel (que llega como mucho a 🔵 raro) y un bono que crece (+3 a +5 % de vida en las armas, +2 a +4 % de ataque en las armaduras, +2 a +3 % de defensa en las joyas). Nunca sale en el botín al azar ni en el equipo inicial: solo de una receta. Se vende al mercader por menos que sus materiales. Desde la fase 2 de D-115 también hay artesano de cabeza, manos, piernas y pies (arriba); los escudos esperan su ranura (ver [Equipamiento](../03-personaje/equipamiento.md) §11).

**La 🍷 poción mayor** cura el 60 % de la vida, con 60 de toxicidad (una por pelea, junto con una de vida) y tiene 1 lugar en el cinturón. Solo la hace la Alquimia: el mercader no la vende.

**Experiencia de héroe (D-108).** Refinar y fabricar dan 20 de experiencia por cada ⚡, × (1 + 0,15 × (nivel − 1)), con nivel = el menor entre tu nivel y tu rango en ese oficio. Recolectar da 14 por ⚡ más sus peleas; en promedio, unos 20. Así quien solo fabrica llega al nivel 100 en ~2 años, como los otros caminos; un artesano novato aprende poco aunque sea de nivel alto (ver [Balance](../03-personaje/balance.md) §7).

**Estaciones y pantallas** (4 botones como mucho):
- **El Claro** tiene todas las estaciones básicas: 🏕️ Campamento → ⚒️ Oficios (su 3.er botón).
- **Tu campamento:** el 🧵 Taller abre aserradero, tejeduría, curtiduría, destilación, carpintería, sastrería, peletería, alquimia, medicina y 🗿 cantería; la 🔨 Herrería, fundición, herrería y joyería (D-101); el 🔥 Fogón, la 🍲 cocina (fase 2: desde el nivel 1). Se llega desde 🔨 Mejoras → 🏘️ Servicios → 🧵 Taller → ⚒️ Oficios (o ⚒️ Oficios en los servicios si hay otra estación y no Taller: la Herrería o el Fogón). Al refinar ahí, +10 % de sacar una unidad más. Todavía no hay alambique: destilar y la alquimia van en el Taller.
- **⚒️ Oficios** (también con **/oficios** desde cualquier lado, y la ficha del héroe lo nombra): tus rangos, con su barra, cómo subir cada uno y qué abre el próximo umbral; los oficios sin empezar; dónde están las estaciones. Botones: 🪚 Refinar · 🛠️ Fabricar · ↩️ Volver.
- **🪚 Refinar / 🛠️ Fabricar:** las recetas que tu rango abre en las estaciones de aquí, primero las que puedes hacer (✅), después aquellas de las que llevas algo (con lo que falta) y al final las demás; de a 2 por página si son más de 3.
- **📜 Receta:** lo que pide (✅ o ❌ con lo que llevas), lo que sale, la energía y lo que ganas. Botones: 🔨 Hacer 1 · 🔨 Hacer 5 (o lo que alcance) · 🔨 Hacer todo · ↩️ Volver. Si falta un material, la energía, la estación o el rango, no se gasta nada.

**Lo que falta (segunda tanda):** el **mercado entre jugadores** para venderse lo que cada uno hace. Mientras tanto cada jugador puede hacer toda la cadena él solo, más lento que el especialista, y vender lo que le sobre al mercader del Claro. Las 🎓 especializaciones ya están en su capa simple (§0.6); lo profundo (maestría por objeto, exámenes, calidad, herramientas, enfermedades laborales) sigue siendo propuesta.

**La red completa**, con los 26 oficios, sus especializaciones y en qué orden entran, está en [Red de oficios](red-de-oficios.md) (D-115). La fase 1 de arriba es su primera parte.

### 0.2 El beneficio de cada oficio (D-111)

El dueño pidió (1-oct-2026) que **cada oficio le dé un beneficio propio a un tipo de jugador**, que crece con la experiencia en ese oficio, como en World of Warcraft (la Herboristería cura, la Minería da aguante, el Desuello da crítico…). El ejemplo del dueño: **la medicina les da a los sanadores un porcentaje extra de sanación**.

**Regla:** el beneficio crece parejo con el rango, del 1 al 100: al rango 50 se tiene la mitad del valor de la tabla y al 100 el valor completo. Es chico a propósito: ayuda, pero no reemplaza al equipo ni a los talentos (D-110). Vale solo mientras haces aquello que el oficio mejora (por ejemplo, el de Herrería solo si llevas placas).

| Oficio | Para quién | Beneficio al rango 100 | Como en WoW |
|---|---|---|---|
| 🌿 Herbolario | Todos, sobre todo quien explora | La vida vuelve sola un **20 %** más rápido fuera de combate | Sangre de vida |
| ⛏️ Minero | Tanques | **+5 %** de vida máxima | Dureza |
| 🪓 Leñador | Recolectores | **+10** de espacio en la mochila | — |
| 🧭 Explorador (D-112 y D-172, en el juego) | Quien explora | Hasta **+5 puntos** de porcentaje por vuelta (+1 cada 20 rangos) y **🥷 Sigilo**: hasta **25 %** de evitar una pelea al azar al explorar con ✋ Manual y al llegar de un viaje (0,25 % por rango; nunca al cazar, asaltar, en mazmorras, oleadas ni el Guardián). Con el rango ve más en el mapa (tiempos de viaje en el 10, campamentos enemigos a 3 zonas en el 25 y en todo el mapa en el 50, su fuerza en el 75), infiltra campamentos desde el 30 y **🔭 reconoce de lejos** mazmorras y campamentos a 1 zona en el 10, 2 en el 30 y 3 en el 50 ([Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md) §1.14) | — |
| 🔪 Desollador | Ataque | **+4 %** de ataque | Maestro de anatomía |
| Refinado (aserradero, fundición, destilación, tejeduría, curtiduría) | Artesanos y comerciantes | Hasta **30 %** de sacar una unidad extra al refinar (0,3 % por rango, ya en la fase 1; +10 % en una estación del campamento) | El retorno de *Albion* |
| 🔨 Herrería | Quien usa placas (guerrero, paladín, caballero de la muerte) | **+3 puntos** de armadura (sin pasar el tope del 60 %) | Engarces de herrero |
| 🧶 Peletería | Quien usa cuero o malla (pícaro, druida, monje, cazador de demonios, bardo, cazador, chamán, evocador) | **+4 %** de ataque y **+3 %** de vida | Refuerzo de brazales |
| 🧵 Sastrería | Quien usa tela (sacerdote, mago, brujo, nigromante) | **+5 %** de ataque (poder de hechizos) | Bordado de capa |
| 🪵 Carpintería | Artesanos (no es de combate desde D-116) | Hasta **15 %** de que cada arco o bastón que fabricas salga ✒️ **obra maestra**, y 🪑 muebles para el campamento (§0.4). Antes (0.16 a 0.20): +4 % de ataque con arco o bastón | — |
| ⚗️ Alquimia | Todos | Las pociones curan un **30 %** más | Mixología |
| 💍 Joyería | Todos | **+3 %** de vida y de ataque | Gemas de joyero |
| 🩺 Medicina | Sanadores (rol de curación) | Tus curaciones curan un **15 %** más; las vendas, un **30 %** más | Primeros auxilios |
| ✨ Encantamiento (fase 2 de D-115, en el juego) | Artesanos y quien mejora su equipo (no es de combate) | Desencantar da hasta **30 %** más esencias (§0.5). Lo que da en combate son los encantamientos que pone en las piezas, no el beneficio | Desencantamiento |
| 🎣 Pescador · 🍲 Cocina · 🗿 Cantería · 🏗️ Construcción (fase 2) | Tu campamento (no tu héroe) | La despensa y las obras del campamento rinden más; rige el mejor rango entre sus miembros (ver §0.4) | — |

- **En el juego desde la 0.16.** Cada oficio empezado da su beneficio según su rango; ⚒️ Oficios muestra "✨ Beneficio ahora" en cada uno. Los de ataque, vida y armadura entran en tus estadísticas; el de la Medicina, en tus curaciones (si eres sanador) y en vendas, ungüentos y botiquines; el de la Alquimia, en las pociones (en combate y fuera); el del Herbolario, en la vida que vuelve sola; el del Leñador, en el espacio de la mochila. Datos: `perk` de cada oficio en `content/professions.yaml`; cuentas en `engine/professions/rules.py` (`perks`).
- **🩺 Medicina** es oficio de fabricación: sube haciendo 🫙 ungüentos (extracto + tela; cura 22 %, rango 1), 🧰 botiquines (extracto, tela y cuero; cura 35 %, rango 25) y 🩻 vendajes de maestro (con 🌸 flor de luna; cura 50 %, rango 50), sin toxicidad. Más adelante crece hacia el médico de §2.3 (diagnósticos, cirugías).
- **Se suman todos los que tengas** (D-57: sin tope de oficios); el freno es el tiempo de subir cada uno al 100. Si en la beta pesa demasiado, se decide en P-76.
- Los números son propuesta de Claude y se comprueban en la pasada de balance de D-110, con la simulación del 1 al 100.

### 0.3 Dos sistemas mezclados: World of Warcraft y Albion Online (D-113, provisional)

El dueño pidió (1-oct-2026) **mezclar el sistema de oficios de World of Warcraft con el de Albion Online**, para que la economía dependa de los jugadores **directamente, por sus oficios**, y no solo de forma indirecta (recolectar y vender). En la transcripción de voz dijo "algo online"; se tomó como *Albion Online*.

| De World of Warcraft | De Albion Online |
|---|---|
| Rango de oficio 1-100 que sube haciendo recetas; recetas que se abren por rango | **Casi todo el buen equipo lo fabrican los jugadores**: los monstruos sueltan sobre todo materiales y monedas, y equipo de menos calidad |
| El beneficio propio de cada oficio (§0.2, D-111) | **Aprender haciendo cada línea de objetos:** fabricar una línea (por ejemplo, espadas) sube su maestría; dominar un nivel de pieza abre el siguiente de esa línea, y la maestría mejora la calidad (§6) |
| **Pedidos de fabricación:** mandas materiales y una comisión a un artesano y él fabrica con su rango y su firma ([Economía](economia.md) §7; **en el juego desde la 0.59**, §0.13) | **El equipo se gasta:** cada pieza tiene durabilidad que baja al pelear; repararla cuesta y la deja un poco más gastada, hasta que se rompe. Siempre hay demanda de artesanos ([Equipamiento](../03-personaje/equipamiento.md) §4) |
| | **Mercado de órdenes:** órdenes de compra y de venta en el Claro (y en los campamentos que lo construyan), con un pequeño impuesto que saca monedas del juego ([Economía](economia.md)) |
| | **Refinar con retorno:** quien refina recupera una parte del material (el beneficio del refinado en §0.2), más en una estación de su campamento |

**Cómo queda la economía:** el recolector vende materia, el refinador la convierte, el artesano fabrica el equipo que todos necesitan y que se gasta, el comerciante compra y revende en el mercado, y los que pelean consumen equipo y pociones. Cada uno depende de otros.

**Cómo entra al juego, por partes:**
1. Oficios fase 1 (en curso): rangos, refinado y recetas de varias ramas.
2. Beneficios de oficio (D-111).
3. Pasada de balance (D-110), **hecha**: equipo por niveles hasta el 100, donde **lo mejor de cada nivel lo fabrican los jugadores** (arma, pecho y joya; recetas de los rangos 55 a 100) y el botín suelta menos (10 % desde el nivel 10) y peor (como mucho 🔵 raro). Ver §0.1 y [Balance](../03-personaje/balance.md) §7.
4. Mercado de órdenes, pedidos de fabricación, durabilidad y reparación: la segunda tanda de la economía de jugadores. **Hecha:** el 🏛️ Mercado (0.46), el desgaste y la reparación (0.57, §0.12) y los 📜 pedidos de fabricación (0.59, §0.13).

---

## 1. Tres capas y un anillo de servicios

```
RECOLECCIÓN ──> REFINADO ──> FABRICACIÓN ──> MERCADO
   (materia)     (material)    (objeto)          │
        ▲                                        │
        └──── SERVICIOS (médico, cartógrafo, transportista, informante…) ◄─┘
```

El paso de refinado viene de Albion: el mineral no sirve hasta que alguien lo funde. Eso crea un oficio más y un mercado intermedio.

## 2. Lista de oficios

### 2.1 Recolección

| Oficio | Qué obtiene | Dónde | Herramienta |
|---|---|---|---|
| **Minería** | Minerales, gemas en bruto, piedra | Vetas en cuevas y montañas | Pico |
| **Herboristería** | Hierbas, hongos, flores (algunas solo de noche) | Campos, bosques, pantanos | Hoz |
| **Tala** | Maderas | Bosques | Hacha de leñador |
| **Desuello y caza** | Pieles, cueros, huesos, partes de monstruo | De las criaturas vencidas; trampas | Cuchillo de desuello |
| **Extracción de Esencias** | Polvos, esencias y cristales arcanos | De objetos mágicos desencantados y fuentes arcanas | Cristal de extracción |
| **Agricultura** | Granos, fibras (lino, algodón), hierbas medicinales cultivadas, frutas, verduras | Huertos, granjas de casa, campos de la ciudad; según la estación y el clima | Azada, semillas |
| **Ganadería** | Leche, huevos, lana, carne, cuero de granja; crías de montura; doma de animales capturados | Corrales, establos, pastos | Cayado, forraje |

**Los agricultores y ganaderos alimentan a la ciudad:** la necesidad de comida de cada asentamiento se cubre sobre todo con ellos (ver [Fundación y cisma](../02-mundo/fundacion-y-cisma.md)). Una ciudad sin agricultores se vacía.

### 2.2 Refinado

| Oficio | Convierte | En |
|---|---|---|
| **Fundición** | Mineral | Lingotes |
| **Curtiduría** | Piel | Cuero |
| **Tejeduría** | Fibra y seda | Tela |
| **Aserradero** | Madera | Tablones |
| **Destilación** | Hierbas, esencias, granos | Extractos, alcoholes, bases alquímicas |

El refinado puede hacerlo cualquier recolector de su rama hasta cierto nivel, o un especialista con más retorno.

### 2.3 Oficios mayores (fabricación)

| Oficio | Fabrica | Especializaciones posibles |
|---|---|---|
| **Herrería** | Armas de metal, placas, malla, herramientas, piezas de prótesis | Forjador de armas, Armero, Herrero de herramientas |
| **Peletería** | Armaduras de cuero y malla ligera, mochilas, Tambores de Guerra | Cuero ligero, Cuero pesado, Monturas (sillas y alforjas) |
| **Sastrería** | Tela, túnicas, capas, vendas limpias, ropa de clima, máscaras | Túnicas mágicas, Ropa de clima, Textil médico |
| **Carpintería** | Arcos, bastones, escudos, varitas, férulas, carros de caravana, muebles | Arquería, Escudos, Mobiliario |
| **Ingeniería** | Artilugios, explosivos, torretas, **prótesis**, desfibriladores, armas de asedio | Prótesis, Asedio, Explosivos, Artilugios |
| **Joyería** | Anillos, collares, gemas talladas, engarces, ojos de cristal | Talla de gemas, Orfebrería |
| **Alquimia** | Pociones, elixires, antídotos, curas de enfermedades, venenos, transmutación | Pociones, Elixires, Venenos, Transmutación |
| **Encantamiento** | Encantamientos +1 a +4, runas, desencantar | Armas, Armaduras, Joyas |
| **Inscripción** | Pergaminos, glifos, mapas, libros de tácticas, fichas de jefe, contratos, Dedos de Sangre, Cuernos de Invocación | Cartografía, Pergaminos, Contratos |
| **Medicina** | Diagnósticos, suturas, tratamientos, cirugías (servicio), vacunas, Sales de Reanimación. Rangos propios: Enfermero → Médico → Cirujano (ver [Curación](../05-salud/curacion-y-tratamientos.md)) | Enfermería, Cirugía, Farmacia, Epidemiología |
| **Construcción** | Casas, talleres, salones de gremio, castillos, fortalezas, defensas, estaciones de oficio, obras públicas. Rangos propios: Peón → Albañil → Oficial de obra → Maestro de obras → Arquitecto (ver [Sistema de construcción](../09-construccion/sistema-de-construccion.md)) | Vivienda, Fortificación, Obras públicas, Interiorismo |

### 2.4 Oficios menores (sin límite)

| Oficio | Qué hace |
|---|---|
| **Cocina** | Comida de Sustento, caldos que suben la inmunidad, banquetes (ver [Condiciones](../05-salud/condiciones.md)) |
| **Pesca** | Pescado, tesoros, materiales raros; con minijuego |
| **Primeros Auxilios** | Vendar, suturar heridas leves y moderadas, entablillar (ver [Heridas](../05-salud/heridas.md)) |
| **Arqueología** | Excavar sitios; colecciones, lore, curiosidades |
| **Huerto casero** | Cultivar un poco en tu casa sin ser agricultor (ver [Casa propia](../09-construccion/casa-propia.md)); el que quiera más, aprende Agricultura |
| **Comercio** | Abrir un puesto propio en cualquier asentamiento; más capacidad de caravana |
| **Juglaría** | Tocar un instrumento en la taberna para bajar un poco el estrés (el Bardo lo hace mucho mejor) |

## 3. Límites: por qué no puedes serlo todo

> ⚠️ **Lo de abajo quedó viejo.** El dueño decidió (D-146, entrevista de voz E-30) que **no hay límite de oficios**: cualquiera puede aprenderlos todos, nada se olvida, y el juego solo recomienda especializarse en uno antes de pasar al siguiente. Abandonar un oficio es empezar de cero. Lo que sigue limitando es el tiempo y las especializaciones (una al rango 25 y otra al 75, D-141). Los beneficios se suman todos, y otros jugadores pueden darte los de sus oficios (D-121).

**De dónde sale.** WoW limita a 2 profesiones primarias; Ultima Online tenía un tope total de habilidades.

- **2 oficios mayores** por personaje.
- **Recolección:** puedes aprender todas, pero solo **una** llega a 100; las demás, hasta 60.
- **Refinado:** va con su rama de recolección.
- **Oficios menores:** todos, sin límite.
- **Cambiar un oficio mayor** es posible, pero empiezas de cero en el nuevo. El viejo queda congelado y puedes retomarlo si vuelves a cambiar.

**Por qué conviene.** Nadie es autosuficiente, así que todos se necesitan. Tener varios personajes con oficios distintos es una forma de jugar (los oficios no se comparten entre personajes; ver [Progresión](../03-personaje/progresion.md)).

## 4. Rangos

| Rango | Niveles | Qué abre |
|---|---|---|
| Aprendiz | 1-20 | Anillos I y II |
| Oficial | 21-40 | Anillos III y IV |
| Experto | 41-60 | Anillos V y VI |
| Artesano | 61-80 | Anillos VII y VIII |
| Maestro | 81-95 | Anillo IX, obras maestras |
| Gran Maestro | 96-100 | Anillo X, firma dorada, el título |

- La curva es larga a propósito: llegar a Gran Maestro en un oficio debería tomar **alrededor de un año** de juego constante. La referencia es el 99 de RuneScape.
- Cada rango pide pasar un **examen**: fabricar una pieza para el gremio de artesanos del asentamiento.
- **En el juego desde la 0.43 (D-306.1):** en lugar del examen, cada título se **compra** en el 🧑‍🏫 Entrenador al llegar al tope del anterior (Oficial 🥉50 y héroe de nivel 10, Experto 🥈2 y 20, Artesano 🥈10 y 30, Maestro 🥈30 y 40, Gran Maestro 🥈50 y 50). Los anillos de la tabla siguen siendo propuesta. Ver §0.7.

## 5. Especializaciones y conocimiento

**De dónde sale.** WoW desde *Dragonflight*.

> **En el juego (capa simple, D-141):** una especialización al rango 25 y otra al 75, nunca las tres, con un **dominio** que crece con la experiencia de oficio que ganas mientras la tienes (no con puntos de conocimiento). Cambiar cuesta monedas y empieza de cero en la nueva; el dominio de la vieja queda guardado. Detalle en §0.6 y en [Red de oficios](red-de-oficios.md) §3.1. Lo de abajo (árbol con ramas, conocimiento semanal con tope) sigue siendo la capa profunda.

- Cada oficio mayor tiene un **árbol de especialización** con 3 o 4 ramas (ver la tabla del §2.3).
- Los puntos de ese árbol se ganan con **conocimiento**: la primera vez que fabricas cada receta, misiones semanales de oficio, tratados que sueltan los jefes y el estudio de objetos de otros artesanos.
- El conocimiento semanal tiene tope. Eso impide que alguien con tiempo infinito se escape, y hace que el oficio se vuelva un hábito semanal.

## 6. Maestría por objeto

**De dónde sale.** Albion, donde cada tipo concreto de objeto (espada ancha, bastón de fuego) tiene su propia maestría.

- Fabricar un tipo de objeto sube su maestría: más probabilidad de buena calidad y menos Enfoque gastado.
- Dos herreros Gran Maestro pueden ser muy distintos: uno el mejor en lanzas, otro en escudos.
- **Por qué conviene:** nace la reputación del artesano ("para lanzas, ve con Lisbeth").
- **Primer paso en el juego (D-116):** la ✒️ obra maestra con firma (§0.4). Hoy la probabilidad sale solo del rango del oficio (la Carpintería hasta 15 %, los demás oficios de equipo hasta 5 %); la maestría por objeto la subiría por línea.

## 7. Herramientas y ropa de oficio

- Las ranuras de herramienta (ver [Equipamiento](../03-personaje/equipamiento.md)) llevan la herramienta de cada oficio: pico, hoz, martillo, alambique, bisturí.
- Tienen anillo de objeto (T1 a T10), calidad y durabilidad, y las fabrican otros artesanos.
- La **ropa de oficio** (delantal de herrero, máscara de minero, guantes de alquimista) protege de las enfermedades laborales y mejora el rendimiento.

## 8. Enfermedades laborales

| Oficio | Riesgo | Protección |
|---|---|---|
| Minería | Tos del Minero | Máscara (Sastrería) |
| Herrería | Quemaduras leves | Delantal de cuero (Peletería) |
| Alquimia | Toxicidad, irritación | Guantes y máscara |
| Encantamiento | Temblor Arcano | Descanso, runas de protección |
| Medicina | Contagio de pacientes | Máscara, lavado de manos (sí, es un botón) |
| Desuello | Infección por cortes | Guantes |

Son leves y se previenen. Ver [Enfermedades](../05-salud/enfermedades.md).

## 9. Oficios sociales y roles que emergen

En SAO, algunos de los personajes más recordados eran artesanos o comerciantes: la herrera del piso 48, el informante que vendía guías de cada piso. Aquí esos roles tienen herramientas:

| Rol | Cómo gana | Con qué |
|---|---|---|
| **Cartógrafo** | Vende mapas de regiones (quien los lee conoce los lugares y las rutas sin haber ido) y ubicaciones de vetas buenas | Inscripción |
| **Informante** | Vende fichas de jefes con los movimientos del Bestiario | Inscripción + conocimiento |
| **Médico** | Cobra por cirugías y tratamientos | Medicina |
| **Transportista y escolta** | Contratos de transporte, peajes | Comercio, combate |
| **Posadero** | Alquila camas con enfermería | Construcción, casa propia |
| **Artesano famoso** | Su firma vale más en el mercado | Maestría |
| **Guía de región** | Lleva novatos por una región a cambio de oro | Conocimiento, combate |

## 10. Quién necesita a quién

| Para hacer… | Hace falta… |
|---|---|
| Una espada larga T5 | Minero → Fundidor → Herrero (+ Curtidor para el mango) → Encantador → Joyero (engarce) |
| Una prótesis de brazo | Herrero (piezas) + Ingeniero (mecanismo) + Médico (implante) + Curtidor (correas) |
| Una poción de curación mayor | Herborista → Destilador → Alquimista (+ Soplador de vidrio: Joyería) |
| Una fortaleza de territorio | Cantería (Minería) + Aserradero + Constructores con rango + Herrero (puertas) + Ingeniero (defensas) |
| Alimentar una ciudad una semana | Agricultores + Ganaderos + Cazadores + Pescadores + Cocineros |
| Tratar una gangrena | Médico + Alquimista (antiséptico) + Sastre (vendas limpias) |
| Un banquete | Cocinero + Pescador + Granjero + Cazador |

Si hace falta más de un oficio para casi todo lo importante, el mercado nunca se queda quieto.

## 11. Estudiar un oficio: entrenadores y exámenes

Ningún oficio se sabe solo. **Construir, curar, forjar o cultivar se estudia**, igual que en la vida real:
- **Entrenadores** en las alas de Oficios de los Castillos (ver [Ciudades y el Castillo](../02-mundo/ciudades-y-castillo.md)): enseñan el rango inicial, las recetas de cada anillo y dan tareas semanales de conocimiento.
- **Exámenes** para cada rango: una pieza, una cirugía o una jornada de obra hecha con el minijuego, con una calidad mínima.
- **Maestros jugadores**: un Gran Maestro puede tomar aprendices y enseñarles sus recetas propias, cobrando por ello.
- **Sin rango, no hay trabajo de alto nivel:** en una obra de castillo solo trabajan constructores con el rango que pide cada etapa, y las enfermedades serias solo las trata alguien que estudió Medicina. **No ayuda cualquiera.**

## 12. Cobrar por trabajar

Cada oficio es también un **trabajo pagado**:

| Oficio | Cómo se cobra |
|---|---|
| Artesanos | Venta en el mercado, pedidos de fabricación con comisión, puesto o local propio (ver [Propiedad y concesiones](propiedad-y-concesiones.md)). **En el juego desde la 0.57:** los 📜 encargos de reparación (§0.12); **desde la 0.59**, los 📜 pedidos de fabricación con su mano de obra (§0.13) |
| Constructores | Paga por jornada de obra desde el presupuesto en custodia, más el bono de inauguración |
| Médicos | Consultas, cirugías y tratamientos con pago en custodia; sueldo como médico de gremio |
| Agricultores, ganaderos, cazadores | Venta de cosechas y carne, **pedidos semanales de la ciudad** para cubrir sus necesidades |
| Crupieres, guardias, escoltas, guías | Sueldo o contrato con el dueño del negocio, el gremio o la ciudad |
| Informantes, cartógrafos | Venta de fichas, mapas y datos de vetas |

## 13. Cuánto dura

Un jugador dedicado a los oficios tiene, por personaje: 2 mayores a 100, una recolección a 100, las demás a 60, los oficios menores, 3 o 4 árboles de especialización y decenas de maestrías por objeto. Con 2 o 3 personajes artesanos, son **años** de progreso sin tocar el PvP.

Ver P-37 a P-40 en [Preguntas abiertas](../00-vision/preguntas-abiertas.md).

### 0.4 Beneficios que no son de combate (D-116)

El dueño pidió (1-oct-2026) que **los beneficios de los oficios no sean solo para la batalla**: hay oficios que benefician solo al campamento o al castillo, oficios que te hacen ganar más dinero (ser comerciante no te ayuda en la pelea, pero cobras más) y oficios que te dejan fabricar piezas más exclusivas (el carpintero). Así cada tipo de jugador encuentra su oficio, pelee o no. La tabla completa, con el tipo de cada beneficio (los números son propuesta de Claude y crecen parejos con el rango, como en §0.2):

| Oficio | Tipo | Beneficio al rango 100 | Estado |
|---|---|---|---|
| 🪓 Leñador | 🎒 Recolección | +10 de espacio en la mochila | en el juego |
| ⛏️ Minero | ⚔️ Combate | +5 % de vida | en el juego |
| 🌿 Herbolario | 🌿 Fuera de combate | La vida vuelve sola 20 % más rápido | en el juego |
| 🔪 Desollador | ⚔️ Combate | +4 % de ataque | en el juego |
| 🎣 Pescador | 🏰 Campamento | El 🐟 pescado crudo rinde **30 %** más en la despensa del campamento | **en el juego** (fase 2, ver abajo) |
| 🌾 Agricultor | 🏰 Campamento | El huerto del campamento da 1 ración más al día por cada agricultor de rango 50 o más | fase 3 |
| 🐑 Ganadero | 🐎 Viaje | Viajes 15 % más rápidos (monturas) | fase 3 |
| 🧭 Explorador | 🧭 Mapa | Ve más en el mapa (tiempos, 👹 campamentos enemigos, su fuerza), 🕵️ se infiltra desde el rango 30, 🔭 reconoce de lejos desde el 10 (2 ⚡: la familia y el jefe de hoy de una mazmorra, la guarnición de un campamento), 🗺️ hace pergaminos de mapa desde el 15 (las zonas que investigó al 50 % en su región de 6 × 6; se venden en el 🏛️ Mercado al precio que quiera, D-311.5, D-326, §1.9.4 del mapa), +5 puntos de exploración por vuelta y 🥷 hasta 25 % de sigilo (D-112, D-172; [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md) §1.14) | **en el juego** |
| Refinado (5 oficios) | 🛠️ Oficio | Hasta 30 % de sacar una unidad más al refinar | en el juego |
| 🗿 Cantería | 🏰 Castillo | Las obras del campamento piden **15 %** menos 🪨 piedra y 🧱 sillar (y, como todo refinado, hasta 30 % de sacar un sillar más) | **en el juego** (fase 2) |
| 🪑 Carpintería | 🛠️ Exclusivo | Hasta **15 %** de que una pieza salga **obra maestra**: exclusiva, con un bono más y tu firma; y muebles exclusivos para el campamento | **en el juego** (reemplazó al +4 % de ataque con arco o bastón; ver "La obra maestra en el juego", abajo) |
| 🔨 Herrería | ⚔️ Combate + 🛠️ | +3 de armadura con placas (en el juego); reparar cuesta 30 % menos cuando exista el desgaste | en el juego / con el desgaste |
| 🦺 Peletería | ⚔️ Combate | +4 % de ataque y +3 % de vida con cuero o malla | en el juego |
| 🪡 Sastrería | ⚔️ Combate | +5 % de ataque con tela | en el juego |
| ⚗️ Alquimia | ⚔️ Combate | Pociones +30 % | en el juego |
| 💍 Joyería | ⚔️ Combate | +3 % de vida y de ataque | en el juego |
| 🩺 Medicina | ⚔️ Combate | Curaciones +15 % (sanadores); vendas y ungüentos +30 % | en el juego |
| ✨ Encantamiento | 🛠️ Oficio | Desencantar da hasta **30 %** más esencias (parejo con el rango: 15 % al 50) | **en el juego** (fase 2 de D-115; ver §0.5) |
| 📜 Inscripción | 💰 Economía | Mapas y contratos valen 20 % más; una orden más en el mercado | fase 3 |
| ⚙️ Ingeniería | 🏰 Castillo | Cada trampa o torreta del campamento da +1 de defensa | fase 3 |
| 🍲 Cocina | 🏰 Campamento | Lo cocinado rinde **30 %** más en la despensa del campamento | **en el juego** (fase 2) |
| 🏗️ Construcción | 🏰 Castillo | Las mejoras del campamento piden **20 %** menos materiales y reparar las defensas después de una oleada cuesta **la mitad** | **en el juego** (fase 2) |
| 💱 **Comercio** | 💰 Economía | **+20 % de monedas** al vender al mercader, al 💱 trueque del campamento o tu equipo viejo; sube vendiendo (1 de experiencia por 🥉). Cuando exista el mercado de órdenes, también paga menos impuesto. **No da nada en combate** | **en el juego desde la 0.17** |

- **Los de campamento y castillo** valen para el campamento donde eres miembro: el que se dedica a construir o cocinar hace más fuerte a su grupo sin ser el que más pelea. **Rige el mejor rango entre los miembros de ahora** (no se suman): un campamento grande no rinde más por tener diez cocineros, y si el mejor se va, su beneficio se va con él (decisión de Claude, provisional: ver "Los oficios del campamento en el juego", abajo).
- **Los de economía** no tocan el combate: el comerciante gana su lugar con dinero, comprando y vendiendo para los demás.
- **Los exclusivos** hacen que el artesano sea buscado: una obra maestra firmada vale más en el mercado.

#### Los oficios del campamento en el juego (fase 2, D-115 y D-116)

El dueño pidió "tantas profesiones y especializaciones como hagan falta, que tengan que ver una con la otra y en conjunto mantengan el sistema" (D-115) y que haya beneficios "solo para el campamento o el castillo" (D-116). Esto es lo que ya está programado (capa simple, D-44; las especializaciones llegan después):

- **🎣 Pescador** (recolección). En las zonas con agua sale 🐟 **pescado**: todo el 🐸 pantano y **3 de cada 10** zonas de 🌲 bosque y de 🌾 pradera (sale de la semilla: siempre las mismas). Es un recurso más de la zona, que se suma a los de tierra **sin quitar ninguno**, con peso 0,5 (en el pantano, ~1 de cada 4 unidades de una vuelta); se agota y vuelve como los demás. Cada pescado da 1 de experiencia de Pescador y, con el rango, a veces uno más (como todo recolector). Vale **1 ración** en la despensa (la carne, 2).
- **🍲 Cocina** (fabricación). Vuelve carne, pescado y hierbas **raciones que valen más que lo crudo**: ×1,5 en el rango 1, ×1,75 en el 25, ×2 en el 50, ×2,25 en el 75 y ×2,5 en el 100. Se cocina en el Claro o en el 🔥 **Fogón** del campamento (nivel 1). Lo cocinado es comida: el mercader y el trueque no lo compran, va a la despensa.

| Rango | Plato | Lleva | Raciones (crudo → cocinado) | ⚡ |
|---|---|---|---|---|
| 1 | 🍱 Ración del campamento | carne, hierba curativa | 2 → 3 | 1 |
| 1 | 🍢 Pescado asado | pescado ×2, madera | 2 → 3 | 1 |
| 25 | 🥘 Guiso del cazador | carne ×2, pescado ×2, hierba | 6 → 10 | 2 |
| 50 | 🥫 Conservas en tarro | carne ×3, pescado ×3, arcilla, extracto | 9 → 18 | 2 |
| 75 | 🍗 Festín de la frontera | carne ×4, pescado ×4, hierba ×2, flor de luna | 12 → 27 | 2 |
| 100 | 🍽️ Banquete del castillo | carne ×6, pescado ×6, extracto ×2, flor de luna ×2 | 18 → 45 | 2 |

- **🗿 Cantería** (refinado). 🪨 piedra ×3 → 🧱 **sillar** (1 ⚡, 6 de experiencia de oficio), en el Claro o en el 🧵 Taller del campamento. Como todo refinado, hasta 30 % de sacar uno más con el rango (+10 % en el campamento).
- **Las mejoras grandes piden refinados.** Desde el **nivel 7** (ciudad), la 🏥 Enfermería, la 📚 Biblioteca, las 🏹 Torres de arqueros y el 🌊 Foso piden 🧱 sillar y 🟫 tablón en lugar de una parte de lo crudo, **con el mismo valor en crudo** (1 sillar = 3 piedras, 1 tablón = 3 maderas) más la energía de refinar. Lo ya construido no cambia, y **lo crudo que una obra ya tenía de más cuenta como refinado** (3 piedras = 1 sillar): nada de lo aportado se pierde.
- **🏗️ Construcción** (servicio). Sube **aportando**: 1 de experiencia por cada material que das a una obra de tu campamento o a la reparación de sus defensas (un tablón o un sillar, 3). Quien junta y aporta todo lo de un día llega al rango 100 en ~1 a 1,5 años, como los demás oficios. La experiencia de héroe la da el aporte (1 por material, como siempre).
- **🛠️ Las oleadas dañan las defensas.** Cada oleada semanal baja la 🛡️ Defensa del campamento: **−1 si la defienden, −2 si la pierden**, nunca más que la defensa construida (un campamento sin defensas no se daña) y la Noche de prueba no daña. Lo construido **nunca se pierde**: solo baja la Defensa (la próxima oleada llega más fuerte) hasta que la reparen. La pantalla del campamento y 🔨 Mejoras lo muestran ("🛠️ Defensas dañadas: −2 🛡️"). Se repara entre todos como una obra: 🔨 Mejoras → 🔨 Obras → **🛠️ Reparar defensas** (primera de la lista), con **2 🟫 tablones y 2 🧱 sillares por punto** (Aserradero + Cantería). Reloj perezoso: no hay tareas de fondo.
- **Cómo valen los beneficios de campamento.** Para cada oficio rige **el mejor rango entre los miembros de ahora**, y crece parejo con el rango (rango 50 = la mitad): 🎣 el pescado crudo rinde hasta +30 % en la despensa; 🍲 lo cocinado, hasta +30 %; 🗿 las obras piden hasta −15 % de piedra y sillar; 🏗️ las mejoras piden hasta −20 % de materiales (las monedas no) y reparar cuesta hasta la mitad. Las raciones de más se redondean hacia abajo (como el 🍖 Ahumadero) y lo que piden las obras, hacia arriba, nunca menos de 1. Si los beneficios ya cubren una obra, el próximo 🤲 la termina aunque no lleves nada. La pantalla del campamento, ⚒️ Oficios, 🔨 Mejoras y 🔨 Obras muestran la línea "🏰 Oficios del campamento" con cada beneficio y **quién lo da**.
- **Datos y código.** Oficios, estaciones y recetas en `content/professions.yaml`; números en `content/balance.yaml` → `camp_professions`; agua en `content/biomes.yaml` (`water`); el pescado, las comidas (`cooked`) y el sillar en `content/items.yaml`; las cuentas en `engine/professions/rules.py` (`camp_best_ranks`, `camp_perks`, `scaled_cost`) y `engine/world/resources.py` (`water_resources`); el daño y lo aportado a la reparación se guardan en las mejoras del campamento (`damage`, `repair`; 0 en los guardados de antes). Textos en `content/locales/es_oficios_campamento.yaml`. Pruebas: `tests/test_oficios_campamento.py`.
- **De dónde sale:** *World of Warcraft* (Pesca y Cocina como oficios secundarios que se alimentan entre sí), *Albion Online* (las construcciones que piden refinados y las comidas que hace un jugador para otros) y *Star Wars Galaxies* (el arquitecto que necesita al minero, y los oficios que solo funcionan juntos).

#### La obra maestra en el juego (D-116)

El dueño lo dijo así: "ser carpintero te permite hacer piezas más exclusivas". Esto es lo que ya está programado:

- **Qué es.** Al fabricar una pieza de equipo (arma, pecho o joya de artesano) puede salir ✒️ **obra maestra**: la misma pieza con **+10 % en cada bono** y **un bono más** según la ranura (las armas, **+1 de defensa**, que no tienen; las armaduras, **+2 % de ataque**; las joyas, **+2 % de vida**). Lleva la **firma** de quien la hizo: en 🔁 Equipar y en la pieza se ve "✒️ Obra maestra de Lyra", y su nombre lleva la marca ✒️. Nunca sale en el botín al azar ni en el equipo inicial.
- **Probabilidad por pieza**, pareja con el rango del oficio que fabrica (rango 50 = la mitad):

| Oficio | Rango 1 | Rango 50 | Rango 100 |
|---|---|---|---|
| 🪑 Carpintería (arcos y bastones) | 0,15 % | 7,5 % | **15 %** |
| 🔨 Herrería · 🪡 Sastrería · 🦺 Peletería · 💍 Joyería | 0,05 % | 2,5 % | **5 %** |
| ⚗️ Alquimia · 🩺 Medicina (pociones y remedios) y los 🪑 muebles | — | — | nunca |

  El carpintero es el especialista: su beneficio de oficio es justamente esto (`perk: {masterwork: 0.15}` en `content/professions.yaml`). La 📜 Receta muestra la probabilidad con tu rango y ⚒️ Oficios la pone en "✨ Beneficio ahora" de cada oficio que hace equipo.
- **Vender.** El mercader paga **25 % más** por una obra maestra que por la pieza normal. Como la pieza normal ya se vende por casi lo mismo que sus materiales (D-113), quien fabrica para vender gana en promedio, con la probabilidad más alta, hasta ~4 % más que el valor de los materiales: se aceptó porque cuesta energía y el mercado entre jugadores la va a poner en su precio.
- **🪑 Muebles exclusivos para el campamento** (solo la Carpintería, 4 ⚡ y 24 de experiencia de oficio cada uno):

| Mueble | Rango | Materiales | Lo que da al campamento |
|---|---|---|---|
| 🛏️ Literas de roble | 10 (hasta la 0.45, 40) | tablón ×12, tela ×4, cuero ×2 | **+1 lugar** para un miembro (se suma al cupo, al del gremio y a las 🛖 Cabañas) |
| 🗄️ Armero de roble | 15 (hasta la 0.45, 70) | tablón ×16, lingote ×6, cuero ×3 | **+1 de 🛡️ Defensa** contra las oleadas |

  D-319 (0.45.1): bajaron de rango porque la 🏥 Enfermería y las 🏹 Torres de arqueros los piden para subir de nivel (D-318, `camps.level_up`); con 40 y 70 un campamento quedaba trabado meses esperando a su carpintero. Los muebles de las 🎓 (🛡️ Paveses, 🛒 Carro de víveres) no cambian y ninguna obra de la lista los pide.

  Un miembro, en el centro de su campamento, lo coloca desde 🔨 Mejoras → 🔨 Obras → 🪑 Colocar. Queda para siempre, con el nombre de quien lo puso, y vale para todos los miembros. **Uno de cada mueble por campamento:** un segundo igual no suma (se guarda en la mochila). Los muebles no cuentan como mejoras para el castillo. Mientras no se colocan, se ven en 🎒 Mochila → 📦 Recursos.
- **Datos y código.** Números en `content/balance.yaml` → `masterwork`; las piezas gemelas `<id>_obra` las arma el motor al cargar (`engine/professions/rules.py`, `masterwork_items`); la firma se guarda en `Hero.gear_signatures` (vacío para los héroes de antes); los muebles son `kind: furniture` en `content/items.yaml` y se guardan en las mejoras del campamento (`furniture`). Pruebas: `tests/test_masterwork.py`.
- **Lo que queda para después.** Hoy la firma se guarda por héroe y por tipo de pieza: todas las copias de un mismo arco firmado comparten la firma, y solo firma uno mismo, porque no hay mercado entre jugadores. **Cuando exista el mercado, la firma tiene que viajar con cada pieza** (un registro de obras maestras por pieza, como pide la ficha M14). La maestría por objeto (§6) podría subir la probabilidad de cada línea.

**De dónde sale:** *World of Warcraft* (las piezas firmadas por el artesano y los procs de fabricación de más calidad), *Albion Online* (la calidad "obra maestra" de lo fabricado) y *Ultima Online* (los objetos con el nombre de su artesano, que se buscaban por quién los hacía).


### 0.5 El ✨ Encantamiento en el juego (fase 2 de D-115, lado del equipo)

El dueño pidió (1-oct-2026) **tantos oficios como hagan falta, que dependan unos de otros y mantengan el sistema** (D-115). En la [Red de oficios](red-de-oficios.md) el Encantamiento cierra el ciclo del equipo: **el encantador desencanta lo viejo**, el gran sumidero de equipo, y con eso mejora lo nuevo. Esta es la capa simple (D-44); lo que está programado:

- **Un oficio de rama propia (✨ Artes arcanas).** No tiene estación ni recetas: se hace desde 👤 Héroe → 🎒 Mochila → 🛡️ Equipo → 🔁 Equipar → una pieza → **✨ Encantamiento**, o con **/encantar** (la pantalla general: tu rango, tus esencias, qué encantamiento lleva cada ranura y qué cuesta). No suma un botón a ⚒️ Oficios: ahí aparece con su rango, cómo se sube, su beneficio y el próximo umbral. Se puede hacer en cualquier lado, mientras no estés ocupado (una actividad a la vez).
- **💨 Desencantar** (1 ⚡, 6 de experiencia de oficio y experiencia de héroe como al refinar, D-108): destruye **una** pieza de la mochila (nunca una puesta) y da **✨ esencias arcanas**: ⚪ común 1, 🟢 poco común 2, 🔵 rara 3, 🟣 épica 4, **+1 cada 20 niveles** de la pieza (una rara del nivel 100 da 8). Las 🟣 épicas (el artesano desde el nivel 8, las ✒️ obras maestras y las piezas del Guardián) dan además **🔮 1 esencia mayor**. Una ✒️ obra maestra pide confirmación ("💨 Sí, desencantar"). Con la última copia de una pieza se van su firma y su encantamiento.
- **El beneficio del oficio:** desencantar da **hasta 30 % más esencias** al rango 100, parejo con el rango (la parte entera siempre y una más con la probabilidad de la fracción).
- **✨ Encantar** (2 ⚡, 12 de experiencia de oficio): le pone a una pieza (puesta o en la mochila) **un** encantamiento; la ranura decide cuál:

| Encantamiento | Ranuras | Bono (según tu rango al encantar) | Desde | Material |
|---|---|---|---|---|
| ⚔️ Filo | arma, manos | +1 % de ataque (rangos 1-25) · +2 % (26-75) · +3 % (76-100) | rango 1 | 🔩 lingote (Fundición) |
| ❤️ Vigor | pecho, cabeza, piernas | +1 % de vida · +2 % · +3 % (mismos rangos) | rango 1 | 🧴 extracto (Destilación) |
| 🛡️ Guarda | pies, joya | +1 de defensa (rangos 25-50) · +2 (51-100) | rango 25 | 💠 gema en bruto (Minero) |

- **Qué pide encantar:** ✨ **3 esencias y 1 más cada 10 niveles** de la pieza (nivel 50: 8; nivel 100: 13), **🔮 1 esencia mayor** si la pieza es de nivel 50 o más, y su material: **1, y 1 más cada 50 niveles** (nivel 100: 3). Si falta algo, la energía o el rango, no se gasta nada.
- **Uno por pieza.** Encantar otra vez **reemplaza** al anterior (nunca se suman) y solo se puede cuando el número sube (por ejemplo, de +1 % a +2 % al llegar al rango 26). El valor queda guardado en la pieza: subir de rango después no lo cambia solo.
- **Cuánto pesa:** con las 7 ranuras encantadas al rango 100, **+6 % de ataque, +9 % de vida y +4 de defensa** (la defensa sigue sin pasar el 60 %). Es chico a propósito, como los beneficios de §0.2: ayuda, pero no reemplaza al equipo.
- **Quién necesita a quién.** El encantador necesita equipo para desencantar (botín y, para las esencias mayores, piezas 🟣 de los artesanos) y los materiales de la Fundición, la Destilación y el Minero; a cambio, mejora el equipo de todos y saca del juego el equipo viejo.
- **Nunca fabrica monedas:** las esencias valen poco en el mercader (✨ 1 🥉, 🔮 3 🥉, y 💱 Vender todo no las vende): desencantar y vender las esencias siempre paga menos que vender la pieza, aun con el beneficio del rango 100 (`tests/test_oficios_equipo.py` lo comprueba con cada pieza).
- **Dónde se ve:** ✨ junto al nombre de la pieza en 🛡️ Equipo y en 🔁 Equipar; en la pieza, "✨ Encantamiento: ⚔️ Filo +2% ataque"; en /encantar, lo que llevas encantado.
- **Datos y código:** números en `content/balance.yaml` → `enchanting`; el oficio en `content/professions.yaml` (`encantamiento`, `branch: enchant`, `perk: {disenchant: 0.30}`); las esencias en `content/items.yaml` (`esencia`, `esencia_mayor`); las cuentas en `engine/professions/rules.py` (`disenchant_yield`, `disenchant_amount`, `enchant_for_slot`, `enchant_value`, `enchant_cost`); el encantamiento de cada pieza en `Hero.gear_enchants` (vacío para los héroes de antes) y su bono en `engine/hero/gear.py` (`real_stats`, `gear_bonus`); las pantallas en `engine/service/game.py` (sección "enchanting"). Pruebas: `tests/test_oficios_equipo.py`.
- **Lo que queda para después (capa profunda):** elegir el encantamiento (más de uno por ranura), encantamientos más fuertes con esencias mayores, runas para las defensas del campamento (Construcción) y vender esencias entre jugadores en el mercado. Sus tres especializaciones (⚔️ Armas, 🛡️ Armaduras y 💨 Desencantar) ya están en el juego (§0.6). Como la firma de la obra maestra, hoy el encantamiento se guarda por héroe y por tipo de pieza (todas las copias del mismo id lo comparten): cuando exista el mercado, tiene que viajar con cada pieza.

**De dónde sale:** *World of Warcraft* (el encantador desencanta lo que otros fabrican en polvos y esencias, y encanta una ranura por pieza) y *Albion Online* (el encantamiento como el gran sumidero de equipo y materiales).


### 0.6 Las 🎓 especializaciones en el juego (D-115, D-141)

El dueño confirmó (entrevista de voz, E-25) **una especialización al rango 25 y otra al 75, nunca las tres** (D-141), como proponía la [Red de oficios](red-de-oficios.md) §3: cada oficio tiene 3; la especialización da recetas que solo ella hace, mejor calidad en su línea y más rendimiento; cambiar se puede pagando y empezando de cero, y lo aprendido en la vieja queda guardado. Esta es la capa simple (D-44); la tabla completa de las 57 y sus números está en [Red de oficios](red-de-oficios.md) §3.1.

- **Dónde:** ⚒️ Oficios → 🎓 Especialización (aparece cuando un oficio llega al rango 25; también /especialidad) → un oficio → una especialización → 🎓 Elegir o 🔄 Dejar otra. Debajo de cada oficio, en ⚒️ Oficios, se ven las que tienes con su dominio, o "🎓 Puedes elegir especialización".
- **Lugares:** ninguno antes del rango 25; uno del 25 al 74; dos desde el 75. Elegir en un lugar libre es gratis.
- **Dominio:** el efecto crece parejo con la experiencia de ese oficio que ganas mientras la tienes: 7.200 para el 100 % (~1 mes dedicado). Es lo que hace que cambiar sea empezar de cero.
- **Cambiar** (P-105, la recomendación): 100 🥉 + 20 🥉 por rango del oficio, con confirmación. La que dejas pierde su efecto y sus recetas exclusivas; su dominio queda guardado por si vuelves.
- **Qué da cada una:** más rendimiento en su línea (recolectores +20 %, refinadores +15 % o +5 % y algo de su línea, remedios +20-25 %), ✒️ obra maestra de más en su línea (+5 % los artesanos de equipo), hallazgos (💠 gemas, 🌸 flores de luna), beneficios (pociones, vendas, curaciones, mochila, exploración, esencias), monedas (Comercio, Rastreador) o un punto más al encantar.
- **Recetas exclusivas:** 18. Cada especialización de equipo tiene dos piezas (nivel 5, rango 25; nivel 100, rango 100) que son la pieza de artesano de su línea con cada bono × 1,05 y un punto propio, con su ✒️ obra maestra; la 🪑 Carpintería suma dos muebles (🛡️ Paveses de roble, +1 de Defensa; 🛒 Carro de víveres, los miembros comen 5 % menos). Se abren con 25 % de dominio y solo las ve quien tiene esa especialización.
- **Calidad por especialización** (D-143): más adelante, sobre este mismo dominio.
- **Datos y código:** `content/professions.yaml` (`specs`, recetas con `spec`), `content/balance.yaml` → `specs`, `engine/professions/rules.py` (`spec_*`, `switch_cost`), `Hero.prof_specs` y `Hero.spec_xp` (vacíos para los héroes de antes), la sección "profession specializations" de `engine/service/game.py` y los textos de `content/locales/es_especializaciones.yaml`. Pruebas: `tests/test_especializaciones.py`.

**De dónde sale:** *World of Warcraft* desde *Dragonflight* (las especializaciones de cada oficio y su avance con la práctica) y *Albion Online* (el retorno de material del especialista).

### 0.7 Títulos que se compran y los arreglos de lo que no avanzaba (0.43, D-306; cómo se aplicó: D-316)

El dueño confirmó el 20-oct-2026 (E-222, E-223, E-228) que los oficios se aprendan "como en WoW" ([Oficios como WoW](oficios-como-wow.md) §3 y §4) y que se arreglen los oficios que la [simulación](simulacion-oficios.md) §8.6 mostró trabados.

- **🎖️ Títulos:** Aprendiz viene con el oficio. Al tope de tu título (rango 20, 40, 60, 80 o 95) el oficio **no guarda experiencia**: lo que no entra se pierde (D-316) hasta que compras el siguiente. Se compra solo en el tope, con el nivel de héroe y las monedas de `balance.yaml` → `professions.titles` (Oficial 🥉50 y nivel 10, Experto 🥈2 y 20, Artesano 🥈10 y 30, Maestro 🥈30 y 40, Gran Maestro 🥈50 y 50). Dónde: 🧑‍🏫 Entrenador → 🎖️ Títulos (el botón sale cuando un oficio llegó al tope; siempre con /titulos) o la pantalla del oficio (🎖️ Comprar). 📋 Mis oficios y ⚒️ Oficios ponen debajo del oficio "🔒 Tope de Oficial: compra Experto en el Entrenador (🥈2, nivel 20)".
- **El progreso no se pierde (D-64):** el título que vale es el mayor entre el comprado (`Hero.prof_titles`) y el que ya da tu rango. Quien pasaba un tope antes de la 0.43 conserva su rango y tiene gratis los títulos hasta él; solo compra los que vienen.
- **El 🧭 Explorador** (sube solo) no tiene títulos (D-316).
- **Precios de aprender por rama:** fabricación y ✨ Encantamiento 🥈1; recolección, refinado y 🏗️ Construcción 🥉50.
- **🦌 Piel y 🔪 Desollador:** cada bestia suelta 2,5 veces la piel de antes (`professions.skinning.loot_mult`, para todos) y el Desollador gana +3 por bestia desollada (`xp_per_beast`), además de 1 por unidad.
- **🎣 Pescar:** botón de 🧭 Explorar que junta solo 🐟 pescado, como 🪓 Talar (D-314); en el pantano siempre y en otras zonas con agua cuando ya sabes que hay pescado.
- **🧱 Mantenimiento:** la obra que se repite en 🔨 Obras (desde que el campamento construyó una obra): 🪵15 🪨15 🧵10 por vuelta = 40 de experiencia de 🏗️ Construcción; sin otro efecto (`camp_professions.maintenance`). Con esto la Construcción pasa del rango 24, que era el techo de todo el catálogo de obras.
- **🧪 Mercader:** compra pociones y remedios de la mochila (no los del cinturón) al 25 % de su precio (`shop.remedy_sell_ratio`), hasta que haya mercado entre jugadores; se venden con /v61 a /v66.
- **Datos y código:** `content/balance.yaml` (`professions.titles`, `learn_price`, `skinning`; `shop.remedy_sell_ratio`; `camp_professions.maintenance`), `content/items.yaml` (códigos 61-66), `Hero.prof_titles`, `engine/professions/rules.py` (`title_cap`, `held_title_index`, `xp_room`), `engine/service/game.py` (sección "🎖️ profession titles", `_prof_gain`, `_learn_price`, `_skin_loot_count`, `_can_fish`, `_maintain`, `_sell_price`) y los textos de `content/locales/es_titulos_pesca.yaml`. Pruebas: `tests/test_titulos_de_oficio.py`.

**De dónde sale:** *World of Warcraft* (los títulos que se compran al entrenador, de Aprendiz a Gran maestro, y la Pesca como oficio secundario con su propia acción).

### 0.9 Las recetas en lista con código (D-321)

🪚 Refinar, 🛠️ Fabricar y 🍲 Cocinar muestran las recetas como una **lista**: una línea por receta con su código **/r1, /r2…**, su color (🟧 🟨 🟩 ⬜), si la puedes hacer (✅ lo llevas todo, 🔸 te falta algo, ▫️ no llevas nada), la pieza con su nivel y la experiencia que da. Van agrupadas por oficio, 8 por página, y el botón **✅ Solo las que puedo hacer** filtra. El código abre la receta, con su detalle y los botones de cantidad. Pedido del dueño (21-oct): "un formato de listado fácil de entender, porque a medida que se aprende salen muchas recetas".

### 0.10 El 💰 fondo del gremio en tu oficio (D-322, desde la 0.47)

En las estaciones de **tu campamento** (no en las 🔥 fogatas), lo que **sobra** en el 💰 fondo del gremio después de las obras activas y de ⏫ Siguiente nivel cuenta como si lo llevaras: la receta toma primero de tu mochila y lo que falta, del fondo. La lista con código lo marca **✅💰** (la haces con ayuda del fondo) y cada receta dice cuánto pondría ("✅ 🪵 Madera: 1/3 +💰2" y "💰 Del fondo del gremio, por vez: 🪵 Madera ×2"); los botones de cantidad cuentan la mochila y el fondo. Cada miembro toma como mucho **40 por día** (`fund_crafts.daily_cap`), queda anotado en 📜 Quién usó qué y el fundador o un 🤝 asistente puede cerrarlo. Lo que sale es tuyo, como siempre (y la experiencia de oficio también). Cómo funciona el fondo: [Escalera del asentamiento](../09-construccion/escalera-del-asentamiento.md) §0.3.

- **Datos y código:** `engine/professions/rules.py` (`fund_draw`: lo que pone el fondo después de la mochila; `max_times` con `fund` y `fund_cap`), `engine/service/game.py` (`_recipe_status`, `_station_view`, `_recipe_view`, `_make`) y `engine/service/gremio.py` (`_fund_pool`, `_fund_take`).

**De dónde sale:** el banco de gremio de *World of Warcraft*, con retiros por día, pero sin sacar nada: el material se usa ahí mismo, en la estación.

### 0.8 La reforma de recetas en el juego (D-306, desde la 0.44)

El dueño decidió el 20-oct (E-221, E-222, E-223) acercar los oficios a WoW: **un tramo de recetas cada 5 rangos**, **colores de receta** y **libros de recetas** que vende el 🧑‍🏫 Entrenador. Lo pidió para que "las profesiones sean un camino lento, pero que se vea la progresión": antes un oficio se subía al 100 repitiendo su receta más barata (7.351 dagas forjadas, [Simulación](simulacion-oficios.md) §0). Cómo se aplicó lo que el dueño no dijo: D-315 (provisional).

- **Tramos cada 5 rangos** en los oficios de equipo (🪑 Carpintería, 🔨 Herrería, 🪡 Sastrería, 🦺 Peletería y 💍 Joyería; `balance.yaml` → `recipe_tiers.professions`): cada línea de equipo tiene una receta en los rangos 1, 5, 10 … 100 y la pieza que sale es del **nivel del tramo** (rango 30 → pieza de nivel 30). Las de antes bajaron de rango (nivel 3 → rango 1, 5 → 5, 8 → 10, 10 → 10 … 100 → 100; nadie pierde una receta) y se agregaron **180 piezas y 180 recetas** de los niveles 15, 25 … 95, con bonos, precio y materiales a mitad de camino entre sus vecinas. Las 🎓 exclusivas siguen en el 25 y el 100.
- **Colores de receta** (`recipe_tiers.colors`): con d = tu rango − el de la receta, 🟧 naranja (d < 5) da la experiencia de oficio entera, 🟨 amarilla (5 a 9) la mitad, 🟩 verde (10 a 14) un cuarto y ⬜ gris (15 o más) nada. Una receta gris se sigue pudiendo hacer (para tener la pieza o venderla), pero no te hace subir. En un lote el color se calcula vez por vez. **En la 0.44 solo regían en los 5 oficios de equipo;** desde la 0.52 rigen en todos (§0.11).
- **Experiencia y energía que crecen con el tramo:** una pieza da 12 × (1 + rango ÷ 100) de experiencia de oficio (12 en el rango 1, 18 en el 50, 24 en el 100) y cuesta **2 ⚡ hasta el 50, 3 desde el 55 y 4 desde el 85** (`xp_per_rank`, `energy_by_rank`). Los 🪑 muebles y las vendas guardan su energía y su experiencia crece igual. Con eso, **un especialista con los materiales en la mano llega al 100 en ~11 meses** (329 días; antes 368) haciendo unas 4.600 piezas, y tiene que fabricar lo nuevo para subir ([Simulación](simulacion-oficios.md) §11).
- **En 🛠️ Fabricar:** cada receta lleva su color delante y la experiencia de oficio que da ahora ("✅ 🟧 🟣🗡️ Hoja de las cenizas ← … · ⚡2 · 🔨+15"), con una línea de leyenda arriba ("🟧 experiencia entera · 🟨 la mitad · 🟩 un cuarto · ⬜ nada"); en un mismo tramo sale primero la pieza de nivel más alto. La 📜 receta dice su color en una frase y lo que ganas con él.
- **📚 Libros de recetas** (E-222; `recipe_tiers.books`): las recetas de rango 25 o más de un oficio piden su libro del 25 (🥈2); las de 50 o más, también el del 50 (🥈10); las de 75 o más, también el del 75 (🥈25). Vale para todos los oficios (también ⚗️, 🩺 y 🍲). Se compran en 🧑‍🏫 Entrenador → **📚 Libros de recetas** (el botón sale cuando hay algo que mostrar), solo desde tu rango (D-287) y una vez para siempre (`Hero.recipe_books`). Sin el libro, las recetas de ese tramo no salen en 🛠️ Fabricar: una línea dice cuántas abre el libro ("📚 Con el libro 🔨 Herrería 25 se abren 7 recetas más aquí"). Al llegar al rango 25, 50 o 75, el aviso de subida dice que el Entrenador ya vende el libro. Sin libro se puede seguir subiendo un poco con las recetas viejas (🟨 y 🟩) hasta que se ponen grises.
- **Quien ya practicaba no pierde nada (D-64):** la primera vez que entra después de la 0.44, cada héroe recibe gratis los libros de los rangos que ya tenía en cada oficio (con su experiencia guardada, aunque no lo hubiera aprendido), una sola vez (`Hero.books_checked`). Los rangos siguientes se compran.
- **💍 Joyería sin gema al empezar (E-223):** su primera receta es el 📿 Colgante de cobre (nivel 1, 🔩 lingote y 🟤 cuero), antes del 💍 Anillo engarzado (nivel 3, con 💠 gema). Desde el tramo 5 las joyas piden gemas, como antes.
- **Sin malla (E-223, D-208):** las 67 recetas de malla (cota, almófar, muñequeras, perneras, botines y las 2 exclusivas de la ⛓️ Malla ligera) quedaron con `retired: true`: ya no se ven ni se hacen. Las piezas de malla que alguien tenga siguen en su mochila (se ponen, se venden y se desencantan como siempre). Qué hacer con la 🎓 ⛓️ Malla ligera: P-243.
- **Datos y código:** `content/balance.yaml` → `recipe_tiers`; `content/professions.yaml` (los rangos, la energía y la experiencia de los 5 oficios de equipo, y el bloque generado al final) y `content/items.yaml` (el bloque generado al final), escritos por **`tools/recipe_tiers.py`** (se vuelve a correr si cambian los números; `tests/test_tramos_de_recetas.py` avisa si quedó viejo); las cuentas en `engine/professions/rules.py` (`tier_rank`, `tier_energy`, `tier_xp`, `recipe_color`, `color_factor`, `books_for`, `book_price`, `book_id`); las pantallas en la sección "recipe tiers, colors and books" de `engine/service/game.py` (`_recipe_xp`, `_batch_prof_xp`, `_book_missing`, `_books_view`, `_buy_book`, `_grant_old_books`); los textos en `content/locales/es_recetas.yaml` y los nombres de las piezas nuevas en `es_tramos.yaml` (generado), con su par inglés. La simulación: `tools/sim_oficios.py`.
- **Lo que faltaba** (tramos cada 5 y colores para el refinado, la ⚗️ Alquimia, la 🩺 Medicina y la 🍲 Cocina) salió en la 0.52: §0.11. La cadena en solitario queda mucho más lenta que antes (P-245).

**De dónde sale:** *World of Warcraft* (los colores de receta naranja, amarillo, verde y gris; el entrenador que enseña las recetas de cada tramo) y *Albion Online* (piezas por tier que piden más material).

### 0.11 Los tramos en el refinado, la ⚗️ Alquimia, la 🩺 Medicina y la 🍲 Cocina (D-306, desde la 0.52; cómo se aplicó: D-328)

La reforma de recetas (§0.8) llega a **todos los oficios con recetas**: los 6 de refinado (🪚 Aserradero, 🔥 Fundición, 💧 Destilación, 🧶 Tejeduría, 🪣 Curtiduría y 🗿 Cantería), la ⚗️ Alquimia, la 🩺 Medicina y la 🍲 Cocina tienen ahora **una receta cada 5 rangos hasta el 100**, con los mismos colores (🟧 🟨 🟩 ⬜), la misma energía y experiencia por tramo que el equipo y los mismos 📚 libros. Todo lo arma `tools/recipe_tiers.py` con los números de `balance.yaml` → `recipe_tiers` (`refine`, `consumables`, `book_gifts`). Cómo se aplicó lo que el dueño no dijo: D-328 (provisional).

- **Refinado: un refinado mejor por tramo.** Del tramo 5 al 100, cada oficio de refinado hace un material nuevo con su refinado de siempre, su crudo y un catalizador de terreno (el mismo de su receta variante):

| Oficio | Material de siempre (rango 1) | Tramo N: lo que pide | Tramo 5 → tramo 100 |
|---|---|---|---|
| 🪚 Aserradero | 🟫 Tablón (3 maderas) | tablón, madera y 💧 resina | 1 + 1 + 1 → 3 + 20 + 5 |
| 🔥 Fundición | 🔩 Lingote (2 metales) | lingote, metal y carbón | igual |
| 💧 Destilación | 🧴 Extracto (3 hierbas) | extracto, hierba y raíz amarga | igual |
| 🧶 Tejeduría | 🧣 Tela (3 fibras) | tela, fibra y lino | igual |
| 🪣 Curtiduría | 🟤 Cuero (2 pieles) | cuero, piel y corteza | igual |
| 🗿 Cantería | 🧱 Sillar (3 piedras) | sillar, piedra y arena | igual |

  Cantidades: refinado de siempre 1 + rango ÷ 50, crudo rango ÷ 5 (sube en cada tramo), catalizador 1 + rango ÷ 25. Cada uno se llama como el lugar del equipo de ese nivel ("Tablón del sendero" en el 5, "Lingote de la frontera" en el 10, "Tela de la tormenta" en el 50, "Sillar del alba eterna" en el 100) y vale lo que sus materiales más su ⚡ (como el tablón: 3 maderas + 1), así refinar no fabrica monedas (D-113). **Hoy ninguna receta los pide:** dan experiencia y se venden al 🛒 Mercader (a la mitad) y en el 🏛️ Mercado (pedidos de compra con su código, /101 a /220). Que los pidan las piezas de los tramos altos es una pregunta abierta (P-268). Los ids de siempre no cambian: las obras del campamento (D-317, D-319) y las recetas de fabricación siguen pidiendo tablón, lingote, extracto, tela, cuero y sillar.
- **⚗️ Alquimia, 🩺 Medicina y 🍲 Cocina: lo que cura y alimenta crece con el tramo.** Cada tramo sin receta gana una, a mitad de camino entre la receta "ancla" de siempre y la siguiente (o el punto final de `recipe_tiers.consumables`): materiales, unidades por vez, efecto y precio.

| Línea (ancla) | Tramos nuevos | Efecto | Toxicidad | Lugar del cinturón |
|---|---|---|---|---|
| 🧪 Poción de vida (rango 1, 35 %) | 5 a 20 (2 por vez) | cura 37 → 45 % | 40 | el de la poción de vida (3) |
| 🍷 Poción mayor (rango 25, 60 %) | 30 a 100 | cura 61 → 75 % | 60 | el de la mayor (1) |
| 🫙 Ungüento (rango 1, 22 %) | 5 a 20 (2 por vez) | cura 24 → 32 % | 0 | el del ungüento (2) |
| 🧰 Botiquín (rango 25, 35 %) | 30 a 45 | cura 38 → 47 % | 0 | el del botiquín (1) |
| 🩻 Vendaje de maestro (rango 50, 50 %) | 55 a 100 | cura 51 → 60 % | 0 | el del vendaje (1) |
| 🍱 Ración (1) → 🥘 Guiso (25) → 🥫 Conservas (50) → 🍗 Festín (75) → 🍽️ Banquete (100) | 5 a 95 sin ancla | 4 → 41 raciones (antes saltaba de 3 a 10, 18, 27 y 45) | — | — (van a la despensa) |

  La toxicidad es la de su ancla: siguen valiendo las mismas mezclas en una pelea (tope 100: dos de vida, o una mayor y una de vida); lo que cambia es cuánto cura cada una (como mucho, 120 % por pelea en el rango 100; antes 95 %). Las pociones y remedios nuevos **comparten el lugar del cinturón de su ancla**: el cinturón no crece; se llena primero con lo que más cura y nunca saca lo que ya está puesto. Ninguna pide nivel de héroe (P-270). En el tramo 50 de ⚗️ hay dos recetas: las 🍷 pociones mayores ×2 de siempre y la nueva.
- **Energía y experiencia:** lo nuevo cuesta y da como una pieza de equipo de su tramo (2 ⚡ hasta el 50, 3 desde el 55, 4 desde el 85; 12 × (1 + rango ÷ 100) de experiencia). Las recetas de siempre guardan su energía y su experiencia crece igual (6 por ⚡ × (1 + rango ÷ 100)): las de rango 1 siguen en 6, el 🧰 botiquín da 15 y el 🍽️ banquete 24. **Un especialista con los materiales en la mano llega al 100 en 329 días** en los 9 oficios (antes 368), y tiene que hacer lo de su tramo para subir ([Simulación](simulacion-oficios.md) §11).
- **📚 Libros:** las recetas de rango 25, 50 y 75 o más piden su libro, como en todos los oficios (ahora también en el refinado). Quien ya tenía el rango antes de la 0.52 recibe gratis, una vez, los libros que su oficio no pedía (refinado: 25, 50 y 75; ⚗️ y 🩺: el del 75), como el regalo de la 0.44 (D-64; `Hero.book_gifts`).
- **En la lista con código (§0.9):** lo que no es equipo dice su tramo ("/r1 🟧 ✅ 🟫 Tablón de la vigía · tramo 30 · 🪚+16"). Con un oficio al 100 son 21 tramos por oficio: van agrupados por oficio, primero lo que puedes hacer y, dentro, el tramo más alto, de a 8 por página; ✅ Solo las que puedo hacer filtra. El 💰 fondo del gremio (§0.10) pone lo que falta, como en toda receta.
- **Datos y código:** `content/balance.yaml` → `recipe_tiers` (`professions`, `refine`, `consumables`, `book_gifts`); `tools/recipe_tiers.py` (escribe el bloque generado de `content/professions.yaml` e `items.yaml` y los nombres de `content/locales/es_tramos.yaml` y `en_tramos.yaml`, con lo que hace cada cosa en `resources.use`); `engine/service/game.py` (`_station_view` con `rlist.tier`, `_refill_belt` y `_belt_members`, `_grant_book_gifts`); `engine/hero/hero.py` (`book_gifts`). Pruebas: `tests/test_tramos_refinado_alquimia_medicina_cocina.py`.

**De dónde sale:** *World of Warcraft* (la minería y la herrería por niveles de lingote; las pociones y los vendajes de Primeros Auxilios que curan más en cada nivel; la cocina con un plato por tramo) y *Albion Online* (el refinado por tier con más material en cada uno).

### 0.12 🔧 Reparar el equipo y los 📜 encargos de reparación (D-139 y D-140, desde la 0.57; cómo se aplicó: D-333)

El equipo se gasta en cada pelea ([Equipamiento](../03-personaje/equipamiento.md) §4.1) y lo reparan **los oficios que lo fabrican**: es el trabajo que el dueño pidió para los artesanos (D-139).

| Oficio | Repara | Gasta por reparación |
|---|---|---|
| 🔨 Herrería | espadas, dagas y placas | 🔩 lingote |
| 🪑 Carpintería | arcos y bastones | 🟫 tablón |
| 🦺 Peletería | cuero y malla (la malla ya no se fabrica, D-306, pero se repara) | 🟤 cuero |
| 🪡 Sastrería | tela | 🧣 tela |
| 💍 Joyería | joyas | 🔩 lingote |

- **Cuánto pide:** rango desde el nivel de la pieza − 10 (`durability.rank_margin`; la pieza de nivel 3 la repara un rango 1, la de nivel 50 un rango 40, la de nivel 100 un rango 90), estar en una estación de ese oficio (cualquier 🔥 fogata o el edificio de tu campamento), 1 + nivel ÷ 20 del refinado (`material_step`: 1 hasta el nivel 19, 6 en el 100) y ⚡1.
- **Qué da:** experiencia de oficio 6 × (1 + nivel ÷ 100) (de 6 a 12: 6 por ⚡, como toda receta) y experiencia de héroe como 1 ⚡ de fabricar. Respeta el tope del 🎖️ título (D-306.1).
- **Tu propia pieza:** si tienes el oficio, la reparas tú (🔨 Reparar yo) y solo gastas el refinado y la energía.
- **El herrero de la 🔥 fogata:** quien no tiene el oficio (o no quiere esperar) paga 3 × lo que valen esos materiales (`npc_mult`; la espada de nivel 3, 39 🥉; la pieza de nivel 100 en placas, 234 🥉). Siempre cuesta más que un artesano y esas monedas se queman ([Economía](economia.md) §5).
- **📜 Encargos de reparación (D-140: todo servicio entre jugadores se paga aparte):** el dueño de una pieza puesta aparta 2 × el valor de los materiales (`order_mult`) y la deja en 🔧 Reparar → 📜 Encargos. Cualquier artesano con el oficio y el rango la ve con ✅ y la toma con /ro1 desde una estación: pone el refinado y la ⚡, cobra al momento el precio menos el impuesto del mercado (5 %, se quema) y gana la experiencia; la pieza del dueño queda reparada sin moverse (como el transportista del 🏛️ Mercado) y le llega un aviso. Uno por pieza; dura 7 días (`order_days`); si se cancela, vence o ya no hace falta (la pieza ya no está puesta o está llena), las monedas vuelven. En la pantalla de cada oficio que repara sale cuántos encargos puedes hacer.
- **Ejemplo:** la espada de nivel 3 de un jugador sin Herrería: el herrero cobra 39 🥉; un encargo, 26 🥉; el herrero jugador gasta 1 🔩 lingote (13 🥉) y ⚡1, cobra 25 🥉 (1 de impuesto) y gana 6 de experiencia de Herrería.
- **Datos y código:** `content/balance.yaml` → `durability`; `engine/hero/durability.py` (las cuentas); `engine/service/repair.py` (las pantallas y los encargos); textos en `content/locales/es_desgaste.yaml` y `en_desgaste.yaml`; ❓ /d63. Preguntas: E-272 (los encargos y el herrero), E-273 (qué deja la pieza rota) y E-274 (la obra maestra).

**De dónde sale:** *Albion Online* (el equipo se gasta y se repara en la estación de su oficio; los jugadores cobran por usar su estación), *World of Warcraft* (los pedidos de fabricación con comisión, desde *Dragonflight*) y *Star Wars Galaxies* (el artesano vive de mantener el equipo de los demás).

### 0.13 📜 Pedidos de fabricación entre jugadores (D-140, desde la 0.59; cómo se aplicó: D-335)

El dueño lo dijo en la entrevista de voz (E-24): **"le das al artesano los materiales, o le pagas para que los consiga, más su mano de obra. Todo servicio entre jugadores se cobra aparte del costo de materiales y procesos."** La forma de hoy es la más simple (D-44), con la maquinaria de los 📜 encargos de reparación (§0.12) y del 🏛️ Mercado ([Economía](economia.md) §3.0).

| Qué | Cómo está hoy |
|---|---|
| **Dónde** | 🏛️ Mercado → 📜 Pedidos de fabricación (/pedidos, /orders): tus pedidos abiertos (/cm1), 📜 Encargar y 🔨 Para hacer. También desde la pantalla de un oficio que no sabes y desde una receta que no puedes hacer (sin el oficio, la 🎓 especialización o el 📚 libro): 📜 Encargar a un artesano |
| **Qué se encarga** | Cualquier receta de los 14 oficios de refinado y fabricación: el oficio (/cf1), lo que quieres (/r1, la lista con código de §0.9 con todo lo que hace ese oficio, también lo que tú no sabes hacer; primero el equipo que te sirve) y la cantidad, de 1 a 5 (`craft_order.max_units`) |
| **Los materiales** | O los **pones tú** (salen de tu mochila y quedan apartados en el pedido) o le **pagas al artesano para que los consiga**, a su precio de referencia (`price` de cada material en `items.yaml`) o al que escribes ("m120"), dentro de la banda del mercado |
| **La mano de obra** | Siempre aparte (D-140). Sugerida por la energía y el tramo de la receta: **8 🥉 por ⚡ × (1 + rango ÷ 20)** por vez (`labor_per_energy`, `labor_rank_step`): la espada de rango 1, 17 🥉; una de rango 45, 52 🥉; una pieza del rango 100, 192 🥉. Se cambia con ×1, ×2, ×3 o escribiendo el número ("50"), **de 0,25 a 10 veces la sugerida** (la banda del mercado, D-26: la misma traba contra pasar monedas a otra cuenta) |
| **Apartado** | La mano de obra y, si el artesano consigue los materiales, lo que pagas por ellos, como un pedido de compra del mercado. Se encarga desde cualquier lugar |
| **Hacerlo** | Lo ve con ✅ quien tiene el oficio, el rango, la 🎓 especialización y el 📚 libro que pide la receta: en 🔨 Para hacer (los que más pagan arriba), en su estación (🪚 Refinar, 🛠️ Fabricar o 🍲 Cocinar: hasta 3, `station_shown`), y la pantalla de su oficio dice cuántos puede hacer. Con /co1, en una estación de ese oficio (cualquier 🔥 fogata o el edificio de su campamento), lo fabrica al momento: pone la ⚡ de todas las veces y, si se los pagaron, los materiales. Hace justo lo pedido (sin la unidad de más del refinado ni los hallazgos de las 🎓); el equipo sortea la ✒️ obra maestra con su probabilidad |
| **Qué gana el artesano** | Todo lo apartado **menos el impuesto del mercado (5 %, sobre todo lo que cobra)**, al momento; la experiencia de oficio (por color, §0.8) y de héroe de esas veces, como al fabricar; y cuenta para las misiones de fabricar |
| **La entrega** | Lo hecho viaja a 📦 Entregas de quien encargó con el transportista del mercado (30 min); una ✒️ obra maestra llega **con la firma del artesano** (D-116). Le llega un aviso en su idioma |
| **Vida y topes** | 7 días (`order_days`); quien encargó lo cancela mientras nadie lo tomó; al cancelar o vencer, las monedas vuelven a la bolsa y los materiales a 📦 Entregas. Hasta 10 pedidos abiertos (`market.max_orders`, aparte de las órdenes del mercado). Nadie hace su propio pedido |

- **Ejemplo:** Lyra (guerrera, sin Herrería) quiere 2 🟢🗡️ Espadas forjadas y tiene los materiales (6 🔩 lingotes y 2 🟤 cueros): los pone y aparta 2 × 17 = 34 🥉 de mano de obra. Bram (🔨 Herrería 1) lo ve en su estación, toca /co1 en el Claro, gasta ⚡4, cobra 32 🥉 (2 de impuesto) y gana la experiencia de 2 espadas; a los 30 min Lyra recoge sus 2 espadas en 📦 Entregas. Si Lyra no tuviera los materiales, pagaría también 2 × 46 = 92 🥉 por ellos y Bram pondría los suyos (cobraría 120 🥉, 6 de impuesto).
- **Datos y código:** `content/balance.yaml` → `craft_order`; `engine/service/craft_orders.py` (las pantallas, la custodia, hacerlo, cancelar y vencer); los ganchos en `engine/service/game.py` (`_recipe_code`, `_recipe_view`, `_station_view`, `_prof_detail_view`, `text()`, `act()`, `tick()`) y `engine/service/market.py` (el botón); textos en `content/locales/es_pedidos.yaml` y `en_pedidos.yaml`; ❓ /d64. Preguntas: E-278 (la mano de obra y su banda), E-279 (el impuesto sobre todo o solo la mano de obra) y E-280 (pedidos personales y de gremio).

**De dónde sale:** *World of Warcraft* (los pedidos de fabricación desde *Dragonflight*: el cliente pone los materiales o parte de ellos y una comisión, el artesano fabrica con su calidad y su firma), *Albion Online* (el buen equipo lo hacen los jugadores y el mercado mueve los materiales) y *Star Wars Galaxies* (el artesano vive de lo que le encargan).
