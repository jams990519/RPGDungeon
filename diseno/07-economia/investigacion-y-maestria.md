# Investigación y maestría: crecer en un oficio durante años

> **Módulo** [07 · Economía](README.md) · **Depende de:** [Profesiones](profesiones.md), [Fabricación](fabricacion.md), [Profundidad de un oficio](profundidad-de-un-oficio.md), [Investigaciones](../06-contenido/investigaciones.md), [Fundación y cisma](../02-mundo/fundacion-y-cisma.md) · **Se conecta con:** [Ciudades y el Castillo](../02-mundo/ciudades-y-castillo.md), [Propiedad y concesiones](propiedad-y-concesiones.md), [Progresión](../03-personaje/progresion.md), [Bestiario](../06-contenido/bestiario.md), [Curación](../05-salud/curacion-y-tratamientos.md), [Red de sistemas](../00-vision/red-de-sistemas.md) · **Estado:** propuesta

> **Nota (D-57 y D-58).** No hay límite de oficios (D-57): este documento ya no usa los "2 oficios mayores". Los anillos y las Lejanías son los del [mapa infinito](../02-mundo/mapa-infinito-y-viaje.md) (D-58).

**Qué pediste.** "Un sistema de crecimiento bajo las profesiones o la investigación sobre ciertas cosas bastante avanzado." Este documento sigue donde terminan [Profesiones](profesiones.md) (rangos del 1 al 100) e [Investigaciones](../06-contenido/investigaciones.md) (casos y conocimiento). Responde tres preguntas: qué hace un Gran Maestro después del 100, cómo se investiga algo nuevo y cómo avanza en conocimiento una ciudad entera.

**De dónde sale.**
- *Wurm Online*: más de 130 habilidades y ningún nivel de personaje. Cada habilidad sube hacia 100 y cada punto cuesta más que el anterior, así que los últimos llevan años. Las habilidades hijas (las ramas de la herrería o de la carpintería) alimentan a su habilidad madre.
- *Project Gorgon*: decenas de habilidades que se combinan; algunas solo se abren cuando subes otras.
- *EVE Online*: las habilidades se entrenan en tiempo real, incluso desconectado. Los planos se investigan durante días para gastar menos material y tiempo, y la **invención** convierte una copia en un plano mejor con una probabilidad de éxito.
- *Civilization*: el árbol tecnológico con requisitos. En *Civilization VI*, los **eurekas** adelantan una tecnología cuando haces algo relacionado con ella.
- *Stellaris*: la investigación se elige entre unas pocas **cartas** que salen al azar, así que cada imperio termina con tecnologías distintas.
- *Star Wars Galaxies*: la **experimentación**, que reparte puntos entre las propiedades de un objeto, con riesgo de fallar.
- *Final Fantasy XIV*: los **especialistas** de oficio. Se puede ser especialista en hasta tres oficios a la vez, y eso abre acciones propias.
- *World of Warcraft* (desde *Dragonflight*): **conocimiento de profesión**, con fuentes semanales y tope, que llena árboles de especialización.
- *Kenshi*: la mesa de investigación consume libros y reliquias antiguas para subir de nivel tecnológico.
- *Ultima Online*: libros escritos por los jugadores.
- **Los gremios medievales**: aprendiz, oficial y maestro. La "obra maestra" era la pieza que el oficial presentaba al gremio para que lo aceptaran como maestro.
- **La economía real**: la **patente** (un monopolio temporal a cambio de publicar el invento) y el **secreto industrial** (no publicar nada y arriesgarse a que otro lo descubra).

**Por qué conviene.** El rango 100 llega en un año. Si después no hay nada, el artesano veterano se aburre o se va. Con maestría, investigación, patentes y una ciudad que avanza, el oficio da **años**, y cada descubrimiento mueve el mercado. Nada de esto da poder de combate: da eficiencia, variedad, prestigio y oro.

---

## 1. Las piezas

| Pieza | De quién | Qué sube | Techo | Ritmo |
|---|---|---|---|---|
| **Rango 1-100** | Personaje | El oficio y sus ramas (ver [Profesiones](profesiones.md)) | 100 | Alrededor de un año |
| **Maestría** (§2) | Personaje | Cada rama, después del 100 | Sin tope, con rendimientos decrecientes | Años |
| **Saberes combinados** (§3) | Personaje | Habilidades nuevas que nacen al cruzar dos oficios | 100 por saber, y después su Maestría | Meses |
| **Puntos de Investigación** (§4) | Personaje | Se ganan estudiando y pagan proyectos | Tope semanal | Cada semana |
| **Proyectos** (§5) | Personaje o grupo | Recetas, planos, variantes, remedios, técnicas | — | Horas o días |
| **Árbol de la ciudad** (§6) | Ciudad o castillo | Técnicas, edificios y servicios para todos | No alcanza para todo: hay que elegir | Semanas |
| **Academias y Erudito** (§7) | Ciudad y rol | Aceleran todo lo anterior | — | — |
| **Patentes** (§8) | Economía | Regalías por lo que descubriste | 12 semanas, más 6 | — |
| **Enseñanza** (§9) | Comunidad | Aprendices, libros, exámenes | — | — |

```
 HACER (fabricar, curar, construir, cultivar, cazar, excavar)
    │ experiencia                    │ Puntos de Investigación (PI)
    ▼                                ▼
 RANGO 1-100 ──> MAESTRÍA        PROYECTOS ──> DESCUBRIMIENTO ──> PATENTE ──> PÚBLICO
       │                             │                                          │
       └──> SABERES COMBINADOS       └── donar PI ──> ÁRBOL DE LA CIUDAD <──────┘
                                                      (biblioteca pública)
```

## 2. Maestría: más allá del rango 100

### 2.1 Madre, ramas y objetos

El oficio es un árbol de tres niveles, como en Wurm.

| Nivel | Qué es | Ejemplo (Herrería) | Dónde se define |
|---|---|---|---|
| **Madre** | El oficio, del 1 al 100, con rangos y exámenes | Herrería 100, Gran Maestro | [Profesiones](profesiones.md) §4 |
| **Rama** | Subhabilidad que sube por separado | Forja de armas, Armería, Herramientas, Cerrajería, Piezas de prótesis | [Profundidad de un oficio](profundidad-de-un-oficio.md) §2.1 |
| **Objeto** | Maestría por tipo de objeto | Lanzas, espadas largas, mazas | [Profesiones](profesiones.md) §6 |

- Subir una rama le da a la madre un 10 % de esa experiencia. Una rama nunca pasa a su madre.
- Una madre alta facilita sus ramas: cada 10 niveles de la madre, sus ramas piden un 3 % menos de experiencia.

### 2.2 La curva sin tope

Cuando una rama llega a 100 (y su madre también), se abre su **Maestría**: un número que empieza en 0 y no tiene techo.

- Cada grado pide un **6 % más** de experiencia que el anterior.
- Cada **10 grados**, el bono recorre la mitad de lo que le falta para llegar a su techo. Nunca lo toca.
- **Especialidades** (como los especialistas de FFXIV): la Maestría sube en **hasta 3 ramas a la vez**. Cambiar una especialidad se puede una vez por semana, y la maestría de la rama que dejas queda guardada.

| Maestría | Tiempo orientativo (jugando esa rama con constancia) | Bono (parte de su techo) |
|---|---|---|
| M10 | 2 meses | 50 % |
| M20 | 6 meses | 75 % |
| M30 | 1 año | 87 % |
| M40 | 2 años | 94 % |
| M50 | 3-4 años | 97 % |

**Qué bonos da**, cada uno con su techo:

| Bono | Techo |
|---|---|
| Material que se ahorra al fabricar | −10 % |
| Enfoque que se gasta (ver [Economía](economia.md) §8) | −20 % |
| PA al empezar el minijuego (ver [Fabricación](fabricacion.md) §2) | +10 % |
| Probabilidad de que la calidad suba un escalón | +8 puntos |
| Durabilidad máxima que se pierde al reparar | −50 % |
| Tiempo de los proyectos de esa rama (§5) | −25 % |
| Puntos de experimentación (estilo SWG) | +1 en M10 y +1 en M30 |

**Lo que la Maestría nunca hace:** subir el techo de un objeto. La calidad máxima sigue siendo Obra Maestra, y el Poder de Objeto lo deciden el anillo, la Calidad, el Encantamiento y las Mejoras (ver [Equipamiento](../03-personaje/equipamiento.md) §3). Los puntos de experimentación solo **reparten** (más daño y menos durabilidad), nunca suman. Un Gran Maestro recién salido y uno de M50 pueden hacer la misma espada; el veterano la hace más seguido, más barata y con la forma que quiere.

- **Maestría descansada.** El tiempo fuera de línea acumula experiencia de maestría doble (hasta 3 días guardados), como la experiencia descansada de [Progresión](../03-personaje/progresion.md) §2. Quien entra poco no se queda atrás.
- **No se pierde nunca.** No hay óxido ni olvido. Dejar de practicar un oficio no la baja: queda guardada para cuando vuelvas.
- **Los aceleradores de oficio** (ver [Monetización](monetizacion.md) §3) suben la experiencia del 1 al 100. **No tocan** la Maestría, los Puntos de Investigación, los proyectos ni el árbol de la ciudad.

### 2.3 Hitos y títulos de maestría

| Hito | Requisito | Qué da |
|---|---|---|
| **Maestro de rama** | Rama a 100 | Título: "Maestro Ebanista", "Maestra Cirujana" |
| **Sello de taller** | M10 | Un emblema propio junto a tu firma dorada; un aprendiz más (§9) |
| **Acción de maestro** | M10 | Puedes investigar técnicas nuevas del minijuego para esa rama (§5) |
| **Examinador** | M20 | Juzgas exámenes de rango en la sala del Castillo y cobras por hacerlo |
| **Maestro de escuela** | M30 y 3 aprendices aprobados | Escribes tratados de técnica (§9); un aprendiz más |
| **Eminencia** | M40 | Retrato en el ala de Oficios del Castillo, con tus obras maestras |
| **Leyenda del oficio** | La Maestría más alta del servidor en esa rama al cerrar cada temporada | Título único de esa temporada y tu nombre en la crónica del gremio de artesanos |
| **Polímata** | 3 saberes combinados a 100 | Título |
| **Maestro de dos mundos** | Dos oficios mayores a 100 | Título |

Todos son prestigio. Ninguno da poder.

## 3. Saberes combinados

**De dónde sale.** *Project Gorgon* y los oficios reales: el boticario sabe de medicina y de química; el relojero, de metal y de mecanismos.

Cuando un personaje sube dos oficios a cierto nivel, puede abrir un **saber combinado**: una habilidad nueva, del 1 al 100, con recetas y servicios que ninguno de los dos oficios tiene por separado.

**Reglas.**
- **Requisito:** los dos oficios a **60** (Experto).
- **Examen mixto:** una pieza que use los dos oficios. Para Relojería, un reloj de bolsillo; para Farmacología, una dosis exacta para un paciente real.
- **Costo de entrada:** 50 PI de cualquier campo (§4).
- **No es un oficio aparte:** nace de los dos que ya tienes. No hay límite de oficios (D-57); el freno es el tiempo y el costo de subir los dos a 60.
- **Ocultos al principio.** La lista muestra "???" hasta que alguien del servidor abre cada saber. Esa persona sale en la Gaceta y en el Registro de descubridores (ver [Descubrimiento y colecciones](../03-personaje/descubrimiento-y-colecciones.md) §1).
- Al llegar a 100 abren su propia Maestría (§2).

| Saber | Se abre con | Qué hace | A quién le sirve |
|---|---|---|---|
| ⚗️ **Farmacología** | Medicina + Alquimia | Dosis exactas que suman menos Toxicidad; remedios de liberación lenta (una dosis dura más); antídotos de amplio espectro | Médicos, bandas largas, epidemias |
| ⏱ **Relojería** | Herrería + Ingeniería | Resortes y engranajes finos: mejores articulaciones de prótesis, cerraduras con tiempo, temporizadores de trampas, relojes de obra | Ingenieros de prótesis, defensa, constructores |
| 🍷 **Enología** | Cocina + Agricultura | Vinos y licores que se añejan en tiempo real en toneles (Tonelería); bebidas de banquete y de taberna | Taberneros, banquetes, bardos |
| 🧀 **Curados** | Cocina + Ganadería | Quesos, jamones y embutidos que se curan durante días; comida de viaje que no se pudre | Expediciones, caravanas |
| 🦴 **Anatomía comparada** | Medicina + Desuello y caza | Disecar partes de monstruo da el doble de PI; el Bestiario sube más rápido; mejores remedios de caza (ver [Bestiario](../06-contenido/bestiario.md) §3) | Cazadores, médicos, informantes |
| 🦌 **Taxidermia** | Desuello y caza + Carpintería | Trofeos montados para la sala de trofeos y el museo; conserva piezas de tres estrellas sin que se pudran | Cazadores, coleccionistas |
| 🔭 **Óptica** | Joyería + Ingeniería | Lentes para el diagnóstico y la cirugía (mejoran el minijuego del médico); catalejos para ver nodos lejanos; torres de vigía que avisan antes | Médicos, exploradores, defensa |
| 🗺 **Geología** | Minería + Inscripción | Lee el terreno: da una pista de en qué nodos aparecerán las vetas la semana siguiente (no el lugar exacto); mapas de vetas | Mineros, cartógrafos, informantes |
| 🌊 **Ingeniería hidráulica** | Construcción + Ingeniería | Norias, molinos de agua, acequias y acueductos; protege los campos de la Sequía | Agricultores, ciudades |
| 🎆 **Pirotecnia** | Alquimia + Ingeniería | Fuegos artificiales de festival (suben el 🎶 Ánimo de la ciudad), bengalas de señal, pólvora de cantería | Festivales, mineros, constructores |
| 🎨 **Tintorería fina** | Sastrería + Herboristería | Tintes raros para apariencias, tabardos y estandartes de gremio (solo cosmético) | Moda, gremios |
| ✴️ **Runología** | Encantamiento + Inscripción | Traduce inscripciones antiguas (más PI de arqueología); runas de protección y alarmas mágicas más duraderas para edificios | Eruditos, arqueólogos, defensa |
| 🏺 **Conservación** | Arqueología + Alquimia | Limpia y estabiliza piezas de ruinas: más PI por pieza, piezas completas para el museo y, a veces, una receta perdida | Arqueólogos, museos |
| 🦿 **Ortopedia** | Medicina + Ingeniería | Ajusta prótesis y férulas: las fracturas y las amputaciones se recuperan antes (ver [Curación](../05-salud/curacion-y-tratamientos.md)) | Pacientes, cirujanos |

**Saberes de oficio y reputación.** Algunos piden un oficio y un rango de reputación en lugar de dos oficios:

| Saber | Se abre con | Qué hace |
|---|---|---|
| ☠️ **Toxicología forense** | Alquimia 60 + rango Inspector de la Agencia (ver [Investigaciones](../06-contenido/investigaciones.md) §1.4) | Identifica venenos: una pista extra en los casos de envenenamiento |
| 🏹 **Medicina de campaña** | Primeros Auxilios 60 + rango Batidor de la Orden de Cazadores (ver [Cacerías](../06-contenido/cacerias.md) §7) | Las heridas moderadas vendadas en el campo no empeoran hasta llegar al médico |

## 4. Puntos de Investigación (PI)

Los PI son **personales**: no se comercian, no se compran y no los toca ningún acelerador. Vienen en cuatro **campos**, como las tres áreas de *Stellaris*. Un médico no paga una receta de herrería con lo que aprendió curando.

| Campo | Para qué proyectos | Oficios que más lo dan |
|---|---|---|
| ⚙️ **Técnica** | Metal, madera, mecanismos, obras | Herrería, Carpintería, Ingeniería, Construcción, Minería |
| 🌿 **Naturaleza** | Plantas, animales, comida | Agricultura, Ganadería, Herboristería, Cocina, Pesca |
| ⚕️ **Medicina** | Remedios, anatomía, enfermedades | Medicina, Alquimia, Desuello, Primeros Auxilios |
| 🔮 **Arcano** | Runas, esencias, el Vacío, lo antiguo | Encantamiento, Inscripción, Arqueología, Extracción de Esencias |

### 4.1 De dónde salen

| Fuente | PI (orientativo) | Detalle |
|---|---|---|
| **Fabricar por primera vez** cada receta | 3-15, según el anillo | Una vez por receta. También da conocimiento de especialización (ver [Profesiones](profesiones.md) §5): son dos contadores distintos |
| **Fabricar en calidad Excelente u Obra Maestra** | 1-3 | Gastando Enfoque |
| **Estudiar un objeto** de otro artesano | 2-8 | El objeto no se pierde. Con **estudio a fondo** se destruye, da el doble y a veces una carta de idea (§5.1) |
| **Desmontar** equipo viejo o roto | 1-4 | Además del material que devuelve (ver [Fabricación](fabricacion.md) §9) |
| **Desencantar** | 1-4 🔮 | Además de las esencias |
| **Leer en una biblioteca** | 1 por hora, hasta 8 horas al día | Pasivo, en la biblioteca de tu casa, de tu gremio o pública. El campo depende del libro |
| **Resolver un caso** | 5-30 | El campo depende del caso: un envenenamiento da ⚕️; un robo de planos, ⚙️ (ver [Investigaciones](../06-contenido/investigaciones.md)) |
| **Arqueología** | 3-15 🔮 | Catalogar fragmentos y completar piezas. Las ruinas del anillo VII (Ruinas Olvidadas) dan el doble |
| **Disecar partes de monstruo** | 2-12 ⚕️ o 🌿 | Más si la parte es de tres estrellas, si es una parte rota (cola, alas, cuernos, núcleo) o si tu Bestiario de esa especie es ★★★★. Las criaturas del Vacío (anillo IX, Abismo Umbrío) dan 🔮. Las 10 primeras de cada especie dan el doble |
| **Muestras de enfermos** | 3-10 ⚕️ | Sangre o tejido de un monstruo Enfermo (ver [Bestiario](../06-contenido/bestiario.md) §9), o el primer diagnóstico de cada enfermedad |
| **Cosechar una variedad nueva** | 2-8 🌿 | Hibridación (ver [Animales y cultivos](../05-salud/animales-y-cultivos.md) §4) |
| **Prospectar una veta excepcional** | 3 ⚙️ | Pureza o dureza de 850 o más |
| **Fracasar en el minijuego** | 1 | Se aprende del error. Como mucho 5 al día |
| **Zona de riesgo** | +25 % en 🔴 roja · +50 % en ⚫ negra | Para disecar, excavar y tomar muestras ahí. En 🔵 azul y 🟡 amarilla, lo normal |

**Tope semanal: 300 PI.** Por encima, cada fuente da la cuarta parte, hasta un **máximo absoluto de 400 PI** por semana. El que juega 12 horas al día no se escapa, y el que juega una hora al día llega cerca del tope con la lectura, el Enfoque y algún caso.

### 4.2 En qué se gastan

| Gasto | Cuánto |
|---|---|
| Proyectos personales (§5) | 20-400 |
| Donar al árbol de tu ciudad (§6) | Lo que quieras; da reputación de Academia |
| Abrir un saber combinado (§3) | 50 |
| Barajar las cartas de idea (§5.1) | 10 |
| Registrar una patente (§8) | 20, más oro |
| Escribir un libro de técnica (§9) | 30-100 |
| Pensar algunas ideas del Gabinete de ideas (ver [Investigaciones](../06-contenido/investigaciones.md) §2.1) | Según la idea |

## 5. Proyectos de investigación personales

Un proyecto es una investigación con **costo, tiempo real y probabilidad de éxito**. Avanza mientras juegas y mientras estás desconectado, como el entrenamiento de habilidades de EVE. Para investigar hace falta el rango Oficial (21) en la rama.

### 5.1 Qué se puede investigar

- **Proyectos fijos**, siempre disponibles: mejorar un plano que tienes, estudiar a fondo una especie del Bestiario, buscar el remedio de una enfermedad de la que tienes muestras.
- **Cartas de idea** (estilo *Stellaris*): al abrir la mesa de investigación salen **3 cartas** con ideas posibles (4 con Biblioteca en casa, 5 en la Academia). Salen de lo que estudiaste: desmontar ballestas trae ideas de ballestas; disecar arañas trae ideas de antídotos. Si ninguna te sirve, barajas por 10 PI.
- **Ingeniería inversa:** estudiar a fondo una pieza hecha con una receta que no conoces te da su carta de idea y +10 % de éxito en ese proyecto.
- Así dos herreros nunca investigan lo mismo: cada uno termina con un recetario propio.

### 5.2 Tipos de proyecto

| Tipo | Ejemplo | Requisito | Costo | Tiempo | Éxito base | Resultado |
|---|---|---|---|---|---|---|
| **Receta nueva** | "Ballesta de palanca" (Arquería): más iniciativa, menos daño | Rama 60 | 80 PI ⚙️ + materiales de prueba | 2 días | 50 % | La receta, con tu nombre. Se puede patentar (§8) |
| **Mejora de plano** (estilo EVE) | Espada larga T5: −5 % de material por nivel, hasta 5 niveles | El plano original | 20-100 PI ⚙️ | 1 día por nivel | 90 % en el nivel 1, 50 % en el 5 | Plano mejorado; sus copias heredan la mejora |
| **Invención** (estilo EVE) | De una copia, una **variante**: "Hacha de filo dentado", que llena más el 🩸 Sangrado y pega menos | Rama 80 + una copia del plano | 150 PI + la copia | 3 días | 35 % | Plano de variante con 5 usos. Si falla, la copia se pierde |
| **Variante de planta** | "Corteza amarga doble", contra la Fiebre del Pantano (anillo IV) | Agricultura o Herboristería 60 | 60 PI 🌿 + semillas | Una cosecha (3-7 días) | 40 % | Semilla estable con nombre, en el Herbario |
| **Remedio** | "Suero de espuma rápido", contra el Mal de Espuma | Medicina o Alquimia 40 + muestras | 120 PI ⚕️ + 3 muestras | 30 horas | 40 % | Receta del remedio. Si cura una enfermedad nueva, los médicos pueden investigar después su vacuna (ver [Curación](../05-salud/curacion-y-tratamientos.md) §3) |
| **Técnica del minijuego** | "Templado en aceite" (Herrería): una vez por pieza, convierte una condición Pobre en Normal | M10 en la rama | 200 PI + 10 fabricaciones de práctica | 3 días | 60 % | Una acción nueva. Entra en tu barra de 8 en lugar de otra: más opciones, no más botones |
| **Estudio de especie** | Llevar al Lobo Lunar a ★★★★★ | ★★★★ y 200 vencidos (ver [Bestiario](../06-contenido/bestiario.md) §1.5) | 100 PI + 5 partes | 2 días | 70 % | Bestiario Maestro de esa especie |
| **Ensayo de material** | Medir la Resonancia del Roble Cantor de Lejanía 1 | Una muestra del yacimiento | 40 PI | 12 horas | 80 % | Ficha del material, que el Informante puede vender |
| **Proyecto de grupo** | La cura de la Plaga Pálida | 2 a 5 investigadores | Se suman los PI de todos | Días | Según el caso | El resultado es de todos (ver [Enfermedades](../05-salud/enfermedades.md) §4) |

**Una receta nueva es una variante, no un escalón.** Reparte el mismo poder de otra forma: más 🩸 Sangrado y menos daño, más daño a la 🟫 Postura y menos a la ❤️ Vida, menos peso y menos protección. O es un consumible de utilidad o un cosmético. Nunca un Tramo de objeto nuevo ni un techo nuevo. El descubrimiento por azar al combinar ingredientes (ver [Fabricación](fabricacion.md) §4) sigue existiendo: los proyectos son el camino deliberado.

### 5.3 Éxito, eurekas y fracaso

- **Éxito** = base + tu rango o tu maestría en la rama (hasta +15) + la mesa (casa +0; Biblioteca o anexo de la Academia +5; mesas de la Academia +10) + eurekas. Como mucho 95 %.
- **Eurekas** (estilo *Civilization VI*): mientras corre el proyecto, hacer algo relacionado suma. Diagnosticar un caso de Mal de Espuma mientras investigas su suero da +8 %. Cada proyecto muestra sus eurekas.
- **Revisar notas:** una vez cada 8 horas, un toque con dos opciones: **ir seguro** (+3 % de éxito) o **apurar** (−20 % del tiempo que falta y −3 % de éxito). Es juego pasivo que se revisa en un toque.
- **Fracaso normal:** recuperas la mitad de los PI y el próximo intento del mismo proyecto tiene +15 %, acumulable. Es la protección contra la mala racha de [Equipamiento](../03-personaje/equipamiento.md) §9.
- **Fracaso grave**, solo en proyectos de riesgo (invención, venenos, pirotecnia): se pierden los materiales y puedes quemarte las manos, una herida leve (ver [Heridas](../05-salud/heridas.md)). Nada permanente.
- **Novatos:** hasta el nivel 10 de personaje no hay fracasos graves, y los 3 primeros proyectos de cada personaje salen bien seguro: son el tutorial.
- **Proyectos a la vez:** 1. Con M20 en cualquier rama, o con el grado de Licenciado en la Academia (§7), 2.

### 5.4 Dónde se investiga

- **En casa**, en la Biblioteca o en la estación de tu oficio (ver [Casa propia](../09-construccion/casa-propia.md)).
- **En la Biblioteca de gremio** (ver [Gremios y organizaciones](../09-construccion/gremios-y-organizaciones.md)).
- **En las mesas públicas de la Academia**, pagando una tasa de uso (sumidero).
- **Trabajo de campo:** algunos proyectos piden ir a un nodo a tomar una muestra o una medida. El ensayo del Hierro Negro pide bajar a la Garganta de Hierro de Lejanía 4, en zona roja (ver [Geografía y recursos](../02-mundo/geografia-y-recursos.md) §3).

## 6. Árbol de conocimiento de la ciudad

**De dónde sale.** El árbol tecnológico de *Civilization*, pero colectivo: no lo investiga un jugador sino todos los residentes de una ciudad.

### 6.1 Reglas

- **Es de la ciudad o del castillo.** Lo aprovecha todo el que usa sus estaciones y servicios: los residentes en sus casas y talleres de la ciudad, y los visitantes en las estaciones públicas, pagando la tasa.
- **Antes de la Academia** (Campamento, Aldea y Villa), el árbol avanza solo con **obras y oficio**. Los nodos de fundación (◆) se aprenden al terminar su edificio. Los de nivel 2 y 3 se llenan con eurekas, oro y materiales donados, que antes de la Academia también suman Saber.
- **Con la Academia** (etapa Ciudad; ver [Fundación y cisma](../02-mundo/fundacion-y-cisma.md) §3) empieza la investigación de verdad: los residentes donan PI, los eruditos trabajan jornadas de estudio y se abren los nodos de nivel 4 en adelante.
- **Saber** es la barra de cada nodo. Se llena con:
  - PI donados por los residentes (1 PI = 1 Saber);
  - jornadas de estudio de los eruditos (§7);
  - eurekas de ciudad (§6.3);
  - los materiales de prueba que pide cada nodo, que se consumen (sumidero);
  - oro del tesoro, **como mucho el 25 %** del nodo. Una ciudad rica no se compra el árbol.
- **Un nodo a la vez** (dos con la Universidad). Cada nodo tiene un **tiempo mínimo**, de 1 a 7 días: aunque sobren donaciones, no termina antes.
- **Quién elige.** El **Rector de la Academia** (un cargo nuevo que se suma a los de [Fundación y cisma](../02-mundo/fundacion-y-cisma.md) §4 y que nombra el gobernador) propone 3 nodos disponibles. Los residentes votan con una encuesta nativa de Telegram de 24 horas. Si no hay Rector, propone el gobernador.
- **Costo por nivel:** nivel 2, 300 de Saber · nivel 3, 800 · nivel 4, 1.800 · nivel 5, 3.500 · cumbre, 6.000.
- **Cumbre: elige una.** El último nodo de cada rama es una elección entre dos que se excluyen. Se puede cambiar, pagando la otra entera y esperando 4 semanas. Así ninguna ciudad lo tiene todo.
- **Nada bloquea un anillo.** Cualquier ciudad con entrenadores fabrica las recetas de cualquier anillo. El árbol da eficiencia, variantes, edificios y servicios; nunca da acceso a un anillo ni poder de combate personal.
- **Nodos dormidos.** Si cae o se deja de mantener el edificio que pide un nodo, o si está en rojo la necesidad de la que depende (ver [Fundación y cisma](../02-mundo/fundacion-y-cisma.md) §2), el nodo se duerme. No se pierde: despierta cuando se arregla.

◆ = nodo de fundación: se aprende al terminar la obra que indica y no cuesta Saber.

### 6.2 Las ramas

**🌾 Agricultura**

| Nodo | Etapa | Desbloquea | Pide |
|---|---|---|---|
| ◆ Huerto comunal | Campamento | Campos de la ciudad; cosechas básicas | Construir el huerto y el corral |
| Rotación de cultivos | Aldea | Los campos de la ciudad y las granjas de residentes rotan solos: el suelo no se agota y hay +10 % de cosecha | 300 · 150 semillas de 3 cultivos |
| Abonos | Villa | Otro +10 % de cosecha; el abono de corral (Ganadería) pasa a tener demanda | 800 · 200 de abono de corral |
| Invernaderos | Ciudad | Plano de Invernadero para los constructores de la ciudad: cultivos fuera de estación y a salvo de la Helada (clave en los Picos Helados, anillo VI) | 1.800 · 300 de vidrio (Joyería) · 100 tablones |
| Hibridación dirigida | Ciudad | Jardín botánico: los proyectos de variante de planta de los residentes tienen +15 % de éxito y tardan un 25 % menos | 3.500 · 20 variedades distintas donadas al Herbario de la ciudad |
| Cumbre: **Gran Granero** o **Huertas finas** | Castillo | Granero: la necesidad de 🌾 Comida baja un 15 % y las conservas duran el doble. Huertas finas: la Enología y los Curados de los residentes suben de calidad con más facilidad | 6.000 · 500 sacos de grano y 100 de sal, o 300 cestos de uva y 100 toneles |

**⚒️ Metalurgia**

| Nodo | Etapa | Desbloquea | Pide |
|---|---|---|---|
| ◆ Fragua | Aldea | Fundición y forja públicas | Construir la forja |
| Alto horno | Aldea | +5 % de retorno de Fundición en la ciudad | 300 · 300 de piedra · 100 de carbón |
| Acero de crisol | Villa | Los fundidores de la ciudad hacen lingotes de crisol, en cualquier anillo: +10 % de Dureza y Flexibilidad (ver [Fabricación](fabricacion.md) §3). La calidad máxima no cambia | 800 · 200 lingotes de hierro · 100 de carbón |
| Acero estelar | Ciudad | Los herreros templan con polvo de estrella: toda pieza de metal forjada aquí tiene +15 % de durabilidad máxima y pierde la mitad al repararse | 1.800 · 120 lingotes de acero estelar (T5) |
| Aleaciones de fuego | Ciudad | La obsidiana y los metales de fuego (🌋 Tierras volcánicas) se funden aquí con un 15 % menos de material; herramientas de oficio que no se dañan con el calor | 3.500 · 100 de azufre · 60 de metal de fuego |
| Cumbre: **Fundición maestra** o **Herramientas maestras** | Castillo | Fundición maestra: +10 % de retorno en todo el refinado de metal. Herramientas maestras: las herramientas de oficio forjadas aquí duran un 30 % más y dan +5 % de PA | 6.000 · 300 lingotes de 3 anillos · un artefacto menor |

**⚕️ Medicina**

| Nodo | Etapa | Desbloquea | Pide |
|---|---|---|---|
| ◆ Enfermería | Aldea | Enfermería pública | Construir la enfermería |
| Antisépticos | Aldea | Receta de antiséptico para los alquimistas de la ciudad; las heridas tratadas aquí se infectan la mitad (menos Gangrena y menos Tétanos de Óxido) | 300 · 100 de aguardiente (Destilación) · 50 hierbas |
| ◆ Cirugía segura | Ciudad | Llega sola con el Sanatorio, como dice [Fundación y cisma](../02-mundo/fundacion-y-cisma.md) §3. Si la ciudad no tenía Antisépticos, también los aprende | Construir el Sanatorio |
| Vacunación pública | Ciudad | El Sanatorio vacuna a los residentes con las vacunas que los médicos ya investigaron; las vacunas fabricadas aquí duran el doble | 1.800 · 30 muestras de enfermos · 200 frascos (Joyería) |
| Cuarentena ordenada | Ciudad | En una epidemia, la cuarentena frena el contagio igual pero corta solo la mitad del comercio; mapa de contagios de la ciudad en `/ciudad` | 3.500 · 300 máscaras (Sastrería) · 100 jabones (Alquimia) |
| Cumbre: **Rehabilitación** o **Escuela de epidemiólogos** | Castillo | Rehabilitación: las secuelas tratables y el ajuste de prótesis tardan la mitad en el Sanatorio (ver [Secuelas y muerte](../05-salud/secuelas-y-muerte.md)). Escuela: los proyectos de cura y de vacuna de los residentes tienen +15 % de éxito, y la ciudad se entera antes de una plaga | 6.000 · 50 prótesis o férulas Notables, o 60 muestras de 6 enfermedades |

**🧱 Construcción**

| Nodo | Etapa | Desbloquea | Pide |
|---|---|---|---|
| ◆ Taller de obra | Aldea | Planos básicos de casa y de taller | Construir el taller |
| Mortero y cantería | Aldea | Muros de piedra; plano de casa de piedra, más durable | 300 · 300 de piedra · 100 de cal |
| Arcos de piedra | Villa | Puentes de piedra entre nodos (viajes más cortos); salones grandes con un 10 % menos de material | 800 · 500 de piedra labrada |
| Murallas mayores | Ciudad | Plano de Muralla mayor (el doble de durabilidad) y de torres de muralla (ver [Defensa](../09-construccion/defensa-y-protecciones.md) §2) | 1.800 · 1.000 de piedra · 200 lingotes |
| Bóvedas y cúpulas | Ciudad | Las alas del Castillo y las obras monumentales piden un 10 % menos de jornadas | 3.500 · 600 de piedra labrada · 200 tablones de roble |
| Cumbre: **Acueducto** o **Ciudadela** | Castillo | Acueducto: agua limpia; la Disentería casi desaparece de la ciudad y la necesidad de ⚕️ Salud baja un 10 %. Ciudadela: murallas y puertas con +25 % de durabilidad, que se reparan con la mitad de jornadas | 6.000 · 1.500 de piedra · 100 norias (Ingeniería hidráulica), o 400 lingotes |

**💰 Comercio**

| Nodo | Etapa | Desbloquea | Pide |
|---|---|---|---|
| ◆ Mercado | Aldea | Libro de órdenes local | Construir el mercado |
| Pesos y medidas | Aldea | La tasa de las órdenes del mercado de la ciudad baja 1 punto | 300 · 50 balanzas (Herrería) |
| Letras de cambio | Villa | Comprar órdenes en el mercado de otra ciudad con tratado sin viajar. La mercancía se queda allá: hay que ir a buscarla | 800 · 200 pergaminos (Inscripción) |
| Banca | Ciudad | Abre en la ciudad las licencias de banquero y los depósitos con interés (ver [Propiedad y concesiones](propiedad-y-concesiones.md) §4) | 1.800 · construir la bóveda del banco |
| Contratos a plazo | Ciudad | Comprar hoy, a precio fijo y con custodia del bot, la cosecha o el lote de la semana que viene | 3.500 · 100 contratos sellados (Inscripción) |
| Cumbre: **Gremio de mercaderes** o **Feria permanente** | Castillo | Gremio: 10 puestos nuevos en la plaza mayor, que salen a subasta (ver [Propiedad y concesiones](propiedad-y-concesiones.md) §2). Feria: los visitantes pagan 1 punto menos de impuesto de venta, y una feria mensual atrae compradores de otras ciudades | 6.000 · 50 carros (Carpintería) · 20 estandartes (Tintorería fina) |

**⚔️ Guerra**

| Nodo | Etapa | Desbloquea | Pide |
|---|---|---|---|
| ◆ Empalizada | Campamento | Cerco y empalizada | Construir la empalizada |
| Vigías | Aldea | Las torres de vigía de la ciudad avisan de una incursión una hora antes | 300 · 100 tablones · 20 cuernos de señal |
| Ingenios de asedio | Villa | Planos de catapulta pesada y de mantelete (una cubierta móvil) para los carpinteros de asedio y los ingenieros de la ciudad | 800 · 200 tablones de roble · 50 cuerdas |
| Trabuquete | Ciudad | Arma de asedio que daña las murallas el doble, pero es lenta y frágil contra las tropas. Pide antes Arcos de piedra | 1.800 · 300 tablones · 100 lingotes |
| Fuego de asedio | Ciudad | Explosivos de asedio (Ingeniería) y aceite hirviendo para los defensores | 3.500 · 200 de azufre · 100 de aceite |
| Cumbre: **Logística de campaña** o **Guardia veterana** | Castillo | Logística: los puestos avanzados se levantan un 20 % más rápido y las raciones de campaña gastan menos Sustento. Guardia veterana: los guardias PNJ de la ciudad tienen una regla de táctica más (ver [Defensa](../09-construccion/defensa-y-protecciones.md) §3) | 6.000 · 300 raciones (Cocina) · 100 armas de guardia |

Cada arma de asedio tiene su respuesta en otra rama: el Trabuquete choca con las Murallas mayores, y el Fuego de asedio, con las Runas de protección. Ninguna toca el combate personal.

**🔮 Arcano**

| Nodo | Etapa | Desbloquea | Pide |
|---|---|---|---|
| ◆ Altar de runas | Aldea | Mesa pública de encantamiento | Construir la mesa de encantamiento |
| Desencantamiento fino | Aldea | +10 % de esencias al desencantar en la ciudad | 300 · 100 polvos arcanos |
| Runas de protección | Villa | La protección rúnica de los edificios de la ciudad absorbe un 50 % más; alarmas mágicas más baratas | 800 · 150 esencias · 50 pergaminos |
| Encantamientos mayores | Ciudad | Se pueden encantar **herramientas y estaciones**: una forja encantada da +5 % de retorno; un alambique encantado, +5 % de calidad. El encantamiento de armas y armaduras (+0 a +4) no cambia | 1.800 · 300 esencias · 20 cristales arcanos |
| Estudio del Vacío | Ciudad | El Templo trata la corrupción y la Fiebre del Vacío un 25 % más rápido; disecar criaturas del Vacío da +25 % de PI 🔮 | 3.500 · 30 partes de criaturas del Vacío (anillo IX) |
| Cumbre: **Observatorio** o **Santuario de esencias** | Castillo | Observatorio: avisa con un día de anticipación de las lunas llenas, las plagas, las bestias legendarias del anillo y las vetas mágicas. Santuario: las runas cuestan un 10 % menos de esencias en la ciudad | 6.000 · 100 lentes (Óptica), o 500 esencias |

**⛵ Navegación** · Solo para ciudades con terreno 🌊 Costa y lagos. Llega con los barcos (ver [Catálogo ampliado](../00-vision/catalogo-ampliado.md)).

| Nodo | Etapa | Desbloquea | Pide |
|---|---|---|---|
| ◆ Muelle | Aldea | Pesca desde el muelle | Construir el muelle |
| Botes | Aldea | Plano de bote de pesca: pesca en aguas profundas | 300 · 200 tablones |
| Cartas de navegación | Villa | Las rutas de agua de la región aparecen en el mapa | 800 · 50 mapas (Inscripción) |
| Barcazas | Ciudad | Transporte por agua: más barato por kilo que la caravana y más lento | 1.800 · 400 tablones · 100 cuerdas · 50 velas (Sastrería) |
| Astillero | Ciudad | Barcos de carga grandes y barcos de guerra (piratería en aguas de zona roja) | 3.500 · 800 tablones de roble · 100 lingotes |
| Cumbre: **Puerto franco** o **Armada** | Castillo | Puerto franco: impuesto de mercado más bajo para lo que llega por agua, y un faro que evita naufragios. Armada: los barcos de guerra de la ciudad tienen +25 % de durabilidad, y hay escoltas navales contratables | 6.000 · 1 faro (obra) o 10 barcos de guerra |

**📜 Letras**

| Nodo | Etapa | Desbloquea | Pide |
|---|---|---|---|
| ◆ Escribanía | Villa | Copiar documentos; archivo de la ciudad | Construir la casa del consejo |
| Biblioteca pública | Villa | +25 % de PI al leer para los residentes; guarda los libros de jugadores y las patentes vencidas (§8) | 300 · 100 libros donados · 50 estanterías (Carpintería) |
| Imprenta | Ciudad | Los escribas de la ciudad copian libros a mitad de costo y de tiempo | 800 · 50 juegos de tipos (Herrería) · 200 pliegos de papel |
| Gran Archivo | Ciudad | +25 % de PI de arqueología; las piezas del Gran Misterio que encuentran los residentes se exponen y dan una pista más a la ciudad (ver [Investigaciones](../06-contenido/investigaciones.md) §2.1) | 1.800 · 30 piezas de arqueología completas |
| Universidad | Castillo | Dos nodos a la vez; grado de Doctor y tribunales de tesis (§7) | 3.500 · construir la Universidad (obra) |
| Cumbre: **Colegio de inventores** o **Escuela de maestros** | Castillo | Colegio: los proyectos personales de los residentes tienen +10 % de éxito. Escuela: los aprendices de maestros residentes ganan otro +25 % de experiencia y los exámenes cuestan la mitad | 6.000 · 50 tratados escritos por residentes |

### 6.3 Eurekas, terreno y difusión

**Eurekas de ciudad.** Cosas que los residentes hacen y que adelantan un nodo:

| Nodo | Eureka | Adelanto |
|---|---|---|
| Acero de crisol | Los herreros de la ciudad fabrican 50 piezas de metal Excelentes | +25 % |
| Vacunación pública | Los médicos de la ciudad curan 100 casos de enfermedades ya investigadas | +25 % |
| Invernaderos | La ciudad pasa una helada sin perder cosechas | +15 % |
| Trabuquete | El castillo gana o defiende un asedio | +20 % |
| Letras de cambio | 500 órdenes cruzadas en el mercado de la ciudad en una semana | +15 % |
| Cartas de navegación | Visitar todos los nodos con agua de la región | +20 % |

- **Terreno** (ver [Geografía y recursos](../02-mundo/geografia-y-recursos.md) §1): cada nodo de la rama de su terreno empieza con un 15 % hecho. ⛰️ Montaña: Metalurgia · 🌲 Bosque: Construcción · 🌾 Llanura fértil: Agricultura · 🌊 Costa y lagos: Navegación · 🐸 Pantano: Medicina · 🏜️ Desierto: Comercio · 🌋 Tierras volcánicas: Guerra · 🕳️ Cueva y subsuelo, 🌸 Tierras flotantes: Arcano · ❄️ Tundra: Letras (inviernos largos, mucho para leer).
- **Capitales:** la rama más cercana a la especialidad de la capital (ver [Ciudades y el Castillo](../02-mundo/ciudades-y-castillo.md) §4) cuesta un 25 % menos. Capital del Pantano: Medicina. Capital del Desierto: Metalurgia y Construcción. Capital de Cristal: Arcano.
- **Difusión:** cada ciudad del servidor que ya tiene un nodo lo abarata un 10 % para las demás, hasta −40 %. Lo nuevo es caro; lo conocido se difunde.
- **Ingeniería inversa:** estudiar un objeto hecho con una técnica que tu ciudad no tiene suma un 2 % a ese nodo en tu ciudad, hasta un 20 %.
- **Intercambio por tratado:** dos castillos con tratado comercial (ver [Fundación y cisma](../02-mundo/fundacion-y-cisma.md) §6) pueden intercambiar un nodo cada uno por temporada. El que lo recibe paga el 30 % del costo y los materiales.

### 6.4 Por qué las ciudades terminan distintas, y qué hacen con eso

- **Elegir cuesta.** Un nodo a la vez, tiempo mínimo, votación y cumbres que se excluyen: cada ciudad prioriza lo suyo y nunca lo tiene todo.
- **La geografía empuja.** Eurekas de terreno, especialidad de la capital y Navegación solo con costa.
- **Comercio.** La técnica vive en las estaciones de la ciudad. El acero de crisol solo se funde donde está el nodo, pero los lingotes se venden en todas partes. Los herreros viajan a usar una forja ajena (pagando su tasa) o compran allá. Es la misma lógica de las especialidades de capital de [Fabricación](fabricacion.md) §6.
- **Rivalidad.** La Gaceta publica cada mes el **Atlas del saber**: qué ciudad tiene qué nodos y cuál terminó primero cada cumbre. Ser la primera con Vacunación pública es noticia, y durante una epidemia atrae residentes.

### 6.5 El cisma y el conocimiento

**Decisión: el cisma se lleva una parte del conocimiento.**

| | Ciudad que se queda | Castillo nuevo |
|---|---|---|
| **Nodos de nivel 1 a 3** | Los conserva | Los **recuerda**: se activan sin pagar Saber cuando construye la obra que piden |
| **Nodos de nivel 4, 5 y cumbre** | Los conserva | Los vuelve a investigar a mitad de costo: ya saben que se puede |
| **Nodo en curso** | Pierde el Saber que donaron los firmantes | Se lleva ese Saber para su primer nodo |
| **Patentes, libros, Maestría** | Son de cada persona y se van con ella | — |

**Por qué así.**
1. **El saber práctico viaja en las personas; las instituciones, no.** Un herrero que se va sabe templar acero, pero la Academia, la Biblioteca y la Universidad se quedan. Es la regla de [Fundación y cisma](../02-mundo/fundacion-y-cisma.md) §5.2: lo personal se va y los edificios no.
2. **Tiene que costar a los dos lados, sin ser una sentencia.** Si los que se van perdieran todo, nadie se iría nunca. Si se llevaran todo, el cisma sería una forma barata de copiar un árbol entero.
3. **La ciudad original no olvida lo que sabe.** Sus desventajas siguen siendo las de [Fundación y cisma](../02-mundo/fundacion-y-cisma.md) §5.3 (menos manos, obras a medias, mantenimiento). Solo pierde lo que aportaba quien se fue, igual que pasa con el tesoro.
4. **Repetir cismas no sirve para copiar conocimiento.** La mitad de costo solo vale para nodos que la ciudad original ya tenía, y sigue mandando el tiempo mínimo entre cismas (ver [Fundación y cisma](../02-mundo/fundacion-y-cisma.md) §6).
5. **Reunificación.** Si dos castillos vuelven a ser uno, se suman los árboles. Si eligieron cumbres distintas en una rama, el consejo vota cuál queda, y la otra se devuelve como Saber para el próximo nodo, a la mitad.

## 7. Academias, edificios y el Erudito

### 7.1 Edificios que aceleran la investigación

| Edificio | Escala | Qué da | Quién lo hace |
|---|---|---|---|
| **Estación de oficio o laboratorio** | Casa | Proyectos en casa | Carpintería; Joyería para el vidrio del laboratorio |
| **Biblioteca** | Casa | Lectura pasiva (PI), una carta de idea más, proyectos un 10 % más cortos | Construcción, Carpintería (estanterías), Inscripción (libros) |
| **Biblioteca de gremio** | Gremio | Lo mismo para los miembros, más proyectos de grupo y casos de gremio | Construcción |
| **Academia** | Ciudad (etapa Ciudad; después, ala del Castillo) | El árbol de la ciudad; mesas públicas (+10 % de éxito, con tasa de uso); 5 cartas de idea; sala de tesis; Registro de descubridores y Registro de patentes | Obra de servidor |
| **Anexos de la Academia** | Ciudad | +5 % de éxito en los proyectos de su campo y +10 % de Saber en su rama. **Fundición experimental** (⚙️, Metalurgia), **Jardín botánico** (🌿, Agricultura), **Anfiteatro anatómico** (⚕️, Medicina: aquí se disecan partes con público), **Observatorio menor** (🔮, Arcano), **Scriptorium** (Letras). Cada uno es una obra aparte y paga mantenimiento | Obra de ciudad |
| **Museo** | Ciudad | Donar piezas da Saber a la ciudad (ver [Descubrimiento y colecciones](../03-personaje/descubrimiento-y-colecciones.md) §3) | Obra de ciudad |

### 7.2 El Erudito

El **Erudito** es el rol del que investiga (ver [Roles](../00-vision/roles-y-caminos-de-juego.md)). No es una clase ni un oficio mayor: es un camino de reputación con la **Academia** (ver [Investigaciones](../06-contenido/investigaciones.md) §2.2) que convive con cualquier oficio.

| Grado | Reputación con la Academia | Qué abre |
|---|---|---|
| **Estudiante** | Amistoso | Mesas públicas a mitad de tasa; jornadas de estudio |
| **Bachiller** | Honorable | Proyectos teóricos (abajo); clases públicas |
| **Licenciado** | Reverenciado | Un segundo proyecto a la vez |
| **Doctor** | Exaltado + una tesis aprobada | Puede ser nombrado Rector; forma parte de los tribunales de tesis; título "Doctor" |
| **Catedrático** | Cargo: uno por rama en cada Academia, votado por los Doctores cada temporada, con un máximo de dos mandatos seguidos | Propone al Rector el siguiente nodo de su rama y cobra un sueldo del tesoro |

**Qué hace un Erudito.**
- **Jornadas de estudio.** Son como las jornadas de obra del constructor: una sesión corta con el mismo motor del minijuego de [Fabricación](fabricacion.md) §2, con otros nombres.
  - Barras: **Comprensión** (progreso), **Rigor** (calidad), **Paciencia** (durabilidad) e **Ingenio** (PA). La condición cambia en cada paso: Clara, Brillante o Confusa.
  - Acciones: Leer, Anotar, Experimentar, Contrastar fuentes, Debatir (si hay otro erudito en la sala), Descansar la vista, Observar y Conclusión.
  - Al terminar, suma **Saber** al nodo en curso, da PI al erudito y le paga una jornada del tesoro de la ciudad (ver [Profesiones](profesiones.md) §12).
- **Proyectos teóricos.** Un Erudito puede investigar en cualquier campo sin tener el oficio, con −15 % de éxito. El resultado no es una receta sino un **Tratado**: un documento que un artesano con el oficio "aplica" fabricando la pieza una vez. El Erudito vende el Tratado, o va a medias con el artesano en la patente. Así el que piensa y el que hace se necesitan.
- **Clases públicas.** Anuncia una clase en el chat de la ciudad. Quienes asisten (en una sala retransmitida, ver [Telegram](../01-plataforma/telegram.md) §4) ganan PI del campo, y el Erudito cobra la entrada.
- **Vende conocimiento:** tratados, fichas de monstruo, traducciones de inscripciones (con Runología) y ensayos de material.

## 8. Patentes

**De dónde sale.** Las patentes reales: el Estado da al inventor un monopolio temporal a cambio de que publique cómo se hace. Y el **impuesto autodeclarado** que ya usa [Propiedad y concesiones](propiedad-y-concesiones.md) §3.

### 8.1 Patentar, guardar el secreto o publicar

Quien descubre algo primero en el servidor (una receta, una variante de plano, una variedad de planta, un remedio) elige qué hacer con eso:

| Opción | Qué pasa | Le conviene a |
|---|---|---|
| ⚖️ **Patentar** | La receta se publica en el Registro de patentes. Cualquiera puede aprenderla, pero mientras dure la patente paga una **regalía** cada vez que la fabrica | Quien quiere vivir de su invento |
| 🔒 **Secreto de taller** | Nadie más la recibe. Otros pueden redescubrirla investigando, y estudiar tus piezas les ayuda (ingeniería inversa, §5.1). Si lo logran, la usan sin pagarte | Quien quiere la exclusiva y acepta el riesgo |
| 📖 **Publicar gratis** | Pasa directo a la Biblioteca pública | Quien busca prestigio: reputación de Academia, Saber para su ciudad y el título "Mecenas" con 5 publicaciones |

### 8.2 Reglas de la patente

- **Registro:** en el Registro de patentes de cualquier Academia. Cuesta 20 PI y 200 de oro (sumidero). La patente vale en todo el servidor.
- **Regalía:** la fija el dueño, entre el 1 % y el 10 % del precio de referencia del objeto (su precio medio en el mercado). El bot la cobra sola al fabricar y se la paga al dueño, menos un 10 % de impuesto (sumidero).
- **Licencia:** en lugar de cobrar cada vez, el dueño puede vender licencias de uso libre hasta que la patente venza, al precio que quiera.
- **Duración: 12 semanas**, más o menos una temporada. Después la receta es **pública**: se aprende gratis en la Biblioteca pública o con el entrenador, pagando una tasa chica.
- **Renovación, una sola vez, por 6 semanas**, con tasa autodeclarada: el dueño declara cuánto vale su patente y paga cada semana el 2 % de ese valor, y cualquiera puede comprársela a ese precio. El máximo absoluto son 18 semanas.
- **Tope:** 5 patentes activas por personaje.
- **Se venden y se heredan:** una patente se puede vender a otro jugador con custodia del bot. Si cae un personaje de Juramento de Hierro, sus patentes pasan a ser públicas en el acto, con su nombre ("Receta de Mara, caída en Lejanía 13").
- **Descubrimiento simultáneo:** si dos personas terminan el mismo descubrimiento con menos de 24 horas de diferencia, la patente es de las dos.
- **Qué no se patenta:** las recetas de entrenador; los nodos de ciudad, que son de la ciudad; las técnicas del minijuego, que se enseñan (§9); y la cura de una epidemia de servidor, que es pública siempre (quien más aportó recibe el título; ver [Enfermedades](../05-salud/enfermedades.md) §4).

### 8.3 Por qué no rompe nada

- Una patente da **oro**, no poder: la receta la fabrica cualquiera que pague.
- Vence, y lo que vence es de todos. El conocimiento se difunde solo.
- El secreto de taller tiene riesgo: la exclusiva dura lo que tarde otro en redescubrirlo.

## 9. Enseñanza

### 9.1 Aprendices

Ya existen (ver [Ciudades y el Castillo](../02-mundo/ciudades-y-castillo.md) §3 y [Profesiones](profesiones.md) §11). Aquí se formalizan:
- **Contrato de aprendizaje** de 4 semanas, con custodia del bot. El Gran Maestro pone tareas semanales y un precio, o paga él si quiere formar gente para su taller.
- El aprendiz gana +25 % de experiencia en esa rama al cumplir las tareas, y mientras dure el contrato usa gratis las patentes de su maestro.
- El maestro gana PI, reputación y, cada vez que un aprendiz aprueba un examen de rango, un **Mérito** (cuentan para el hito Maestro de escuela, §2.3).
- **Cuántos aprendices:** 2; uno más con el Sello de taller (M10) y otro con Maestro de escuela (M30).
- El maestro puede enseñarles sus **técnicas del minijuego**. Es la única forma de pasar una técnica sin un libro.

### 9.2 Libros de técnica

Los jugadores escriben libros con **Inscripción** (ver libros de jugadores en [Catálogo ampliado](../00-vision/catalogo-ampliado.md)):

| Libro | Qué hace al leerlo | Límite |
|---|---|---|
| **Manual de rama** | +50 % de experiencia en esa rama durante 20 fabricaciones | Solo sirve hasta 10 niveles por debajo del autor. Una vez por libro y personaje |
| **Tratado de técnica** | Enseña una técnica del minijuego que el autor conoce | El lector necesita esa rama a 100; el autor, el hito Maestro de escuela |
| **Recetario** | Enseña recetas del autor: públicas, o sus secretos de taller (que dejan de ser secretos) | Las patentadas, solo con licencia |
| **Crónica, guía o novela** | Ningún bono: historia, mapas, opinión | — |

- Tienen **calidad** (la de la fabricación) y la **firma** del autor. Un libro nunca enseña más de lo que sabe quien lo escribió.
- Se copian a mano o en la Imprenta de la ciudad (§6.2, Letras) y se venden en el mercado. La Biblioteca pública presta copias para leer allí.
- **Por qué conviene:** un libro acelera sobre todo al que va atrás, porque el autor siempre está 10 niveles por encima del techo del libro. Y les da trabajo y oro a los escribas.

### 9.3 Exámenes

- **De rango** (ya existen, ver [Profesiones](profesiones.md) §4): ahora con **examinadores jugadores** (M20) que cobran y firman el acta. Si no hay examinador, juzga el PNJ.
- **De saber combinado** (§3): una pieza que usa los dos oficios.
- **De maestría:** un concurso de obra maestra por rama en cada festival. El jurado son tres examinadores o Eminencias, y el público vota con una encuesta. Es la obra maestra de los gremios medievales, vuelta a su sentido original.
- **Tesis** (Erudito): un proyecto teórico que se presenta ante un tribunal de tres Doctores. Aprobarla da el grado de Doctor.

## 10. Que los veteranos no se vuelvan inalcanzables

| Riesgo | Contrapeso |
|---|---|
| **Maestría infinita** | Rendimientos decrecientes: cada 10 grados se gana la mitad de lo que falta. Entre un Gran Maestro recién salido y uno de M50 hay unos puntos de eficiencia (como mucho −20 % de Enfoque y −10 % de material) |
| **Objetos mejores** | Techo de poder: ni la Maestría, ni los saberes, ni el árbol suben el techo de un objeto. La Obra Maestra, el Encantamiento +4 y el Poder de Objeto del anillo son iguales para todos. Las variantes reparten poder, no lo suman, y el presupuesto de 100 puntos de cada una de las 46 specs (ver [Balance](../03-personaje/balance.md) §2) no se toca |
| **Consumibles mejores** | Los remedios y consumibles nuevos siguen las reglas de [Balance](../03-personaje/balance.md): no se apilan con los de su tipo y no dan utilidades que nadie más tenga |
| **Recetas exclusivas** | Patentes que vencen (18 semanas como máximo), secretos que se redescubren, ingeniería inversa |
| **Ciudades viejas con todo** | Un nodo a la vez, tiempo mínimo, cumbres que se excluyen y difusión (−10 % por cada ciudad que ya lo tenga, hasta −40 %) |
| **El que juega todo el día** | Tope semanal de 300 PI (400 como máximo absoluto), Enfoque diario, tiempo real en proyectos y nodos, 3 especialidades de Maestría a la vez |
| **El que llega tarde** | Maestría descansada, libros de técnica, aprendices con +25 %, difusión de nodos, patentes viejas que ya son públicas. Además, cuando la Frontera está 2 Lejanías o más por delante de un anillo, subir rango con recetas de ese anillo da +25 % de experiencia: el Viento de Cola de los oficios (ver [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md) §2) |
| **Pagar para ganar** | Los PI, la Maestría, los proyectos, el Saber de la ciudad y las patentes no se compran ni se aceleran con dinero real (ver [Monetización](monetizacion.md)) |
| **Perderlo todo** | Nada de este sistema se pierde para siempre. Un fracaso cuesta materiales y la mitad de los PI; un nodo dormido despierta; la Maestría no se olvida. La única excepción es la de siempre: un personaje de Juramento de Hierro que cae |

## 11. Cómo se ve en Telegram

Todo son **mensajes vivos** que se editan solos (ver [Telegram](../01-plataforma/telegram.md) §3). Solo llega un mensaje nuevo cuando algo pide atención: terminó un proyecto, se abrió una votación, se completó un nodo.

**La Academia de una ciudad** (`/academia`):

```
🏛 Academia de Ribera Alta
Castillo · Lejanía 14 · 64 residentes activos · ⛰️ Montaña
Rector: Ilse la Docta

🔬 En curso: ⚒️ Metalurgia · Aleaciones de fuego
Saber     ▓▓▓▓▓▓▓░░░  2.480/3.500
Material  azufre 60/100 · metal de fuego 41/60
⏳ Termina en 2 días como pronto
💡 Eureka: 31/50 herramientas Excelentes (+25 %)
⛰️ Terreno: empezó con 15 % · 🌐 1 ciudad ya lo tiene (−10 %)

Tu aporte esta semana: 85 PI · Grado: Bachiller

🗳 Próximo nodo (la encuesta cierra en 14 h)
 1. ⚕️ Vacunación pública
 2. 💰 Banca
 3. 🔮 Encantamientos mayores

[🎁 Donar PI]         [🧱 Donar material]
[📚 Jornada de estudio] [🌳 Ver árbol]
[⚖️ Patentes]         [🗳 Votar]
```

**Una rama del árbol** (botón *Ver árbol*):

```
🌳 Ribera Alta · ⚒️ Metalurgia
✅ ◆ Fragua
✅ Alto horno
✅ Acero de crisol
✅ Acero estelar
🔬 Aleaciones de fuego ········ 70 %
🔒 Cumbre: Fundición maestra ⟷ Herramientas maestras
   (pide etapa Castillo · elegir una excluye la otra)

[⬅️ Ramas]  [📜 Detalle del nodo]
```

**Un proyecto personal** (`/investigar`), un mensaje vivo que avanza solo:

```
🧪 Proyecto · Suero de espuma rápido
Mara la Botica · Farmacología 34 · Medicina 72
⚕️ Mesa pública de la Academia de Ribera Alta

Tiempo  ▓▓▓▓▓▓░░░░  19 h de 30 h
Éxito   66 %  (base 40 · Farmacología +8 · Academia +10 · eureka +8)
Gastado: 120 PI ⚕️ · 3 muestras de Zorro Espumoso

💡 Eurekas
 ✅ Diagnosticar un caso de Mal de Espuma (+8 %)
 ⬜ Disecar un Zorro Espumoso de tres estrellas (+5 %)
📝 Puedes revisar tus notas ahora

Si falla: recuperas 60 PI y tienes +15 % en el próximo intento.

[🛡 Ir seguro]   [⏩ Apurar]
[💡 Eurekas]     [🛑 Cancelar]
```

**Al terminar**, llega un mensaje nuevo:

```
✅ Proyecto terminado: ¡éxito!
Suero de espuma rápido · Farmacología
Eres la primera del servidor 📜 Registro de descubridores

¿Qué haces con la receta?
⚖️ Patentar: cobras regalía 12 semanas; después es pública
🔒 Secreto de taller: solo tú, hasta que otro la descubra
📖 Publicar gratis: reputación de Academia y Saber para Ribera Alta

[⚖️ Patentar]   [🔒 Secreto]
[📖 Publicar]
```

**La maestría de un artesano** (`/maestria`):

```
🪚 Ansel el Paciente · Carpintería 100 (Gran Maestro) ✒️
Especialidades de Maestría (2/3)
 Ebanistería   M23  ▓▓▓▓▓▓▓▓░░  80 % del techo
 Obra          M4   ▓░░░░░░░░░  24 % del techo
Otras ramas: Arquería 88 · Tornería 70 · Tonelería 61
Saberes
 🦌 Taxidermia 47
 🍷 Enología: te falta Agricultura 60
 ??? nadie lo descubrió todavía
💤 Maestría descansada: 2 días guardados
🏅 Maestro Ebanista · Sello de taller · Examinador
```

## 12. Su fila en la red de sistemas

Como pide [Red de sistemas](../00-vision/red-de-sistemas.md) §5, este sistema llena su fila:

| Sistema | Consume | Produce | Depende del farmeo | Depende de la fabricación | Depende de la progresión |
|---|---|---|---|---|---|
| **Investigación y maestría** | PI (de fabricar, desmontar, disecar, casos, arqueología), materiales de prueba, muestras, donaciones a la ciudad, oro de tasas, tiempo real | Recetas, variantes, remedios, técnicas, nodos de ciudad, libros, regalías, títulos | Muestras, partes de monstruo, semillas, piezas de ruinas, materiales de prueba | Libros (Inscripción), estanterías y mesas (Carpintería), frascos y lentes (Joyería, Óptica), instrumental | Rangos de oficio, Maestría, grados de la Academia, etapa de la ciudad |

**Sumideros nuevos:** tasas de las mesas públicas, registro de patentes, el 10 % de impuesto de las regalías, la tasa autodeclarada de las renovaciones, las matrículas de examen y, sobre todo, los materiales que se consumen en proyectos y nodos.

## 13. Preguntas para decidir

Propuestas para numerar en [Preguntas abiertas](../00-vision/preguntas-abiertas.md):

| Pregunta | Propuesta |
|---|---|
| ¿Cuánto dura una patente? | 12 semanas, más una renovación de 6 con tasa autodeclarada |
| ¿El cisma se lleva conocimiento? | Sí: los nodos 1 a 3 se recuerdan; el resto, a mitad de costo |
| ¿Tope semanal de PI? | 300; por encima, cada fuente da la cuarta parte, hasta 400 como máximo absoluto |
| ¿Cumbres que se excluyen? | Sí, cambiables pagando la otra entera y esperando 4 semanas |
| ¿Saberes combinados ocultos hasta que alguien los abre? | Sí |
| ¿Cuántas especialidades de Maestría a la vez? | 3, como los especialistas de FFXIV |
| ¿La rama de Navegación desde el lanzamiento? | No: llega con los barcos |

Ver también P-37 a P-40 y P-49 en [Preguntas abiertas](../00-vision/preguntas-abiertas.md).
