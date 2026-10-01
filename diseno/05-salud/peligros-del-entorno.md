# Peligros del entorno

> **Módulo** [05 · Salud](README.md) · **Depende de:** [Condiciones](condiciones.md), [Enfermedades](enfermedades.md), [Heridas](heridas.md), [Geografía y recursos](../02-mundo/geografia-y-recursos.md) (terrenos), [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md) (anillos), [Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md) (clima) · **Se conecta con:** [Ronda y acciones](../04-combate/ronda-y-acciones.md), [Secuelas y muerte](secuelas-y-muerte.md), [Curación](curacion-y-tratamientos.md), [Profesiones](../07-economia/profesiones.md), [Sistema de construcción](../09-construccion/sistema-de-construccion.md) (refugios), [PvP](../06-contenido/pvp.md) (zonas) · **Estado:** propuesta

Pediste que la salud, el combate y las heridas tengan **problemas propios de la zona donde estás**: contaminarte, morir hasta cierto punto por el frío, morir por falta de agua. Este documento lo arma. Cada terreno tiene sus peligros. Todos avisan antes, todos tienen retirada y todos se evitan con equipo que fabrica otro jugador. Es la decisión D-36 (ver [Decisiones](../00-vision/decisiones.md)).

**De dónde sale.**
- *The Long Dark*: el frío como enemigo principal. La sensación térmica suma el viento. Primero llega un **riesgo de hipotermia** (un aviso) y después la hipotermia. El agua hay que hervirla o da disentería. Se puede armar un refugio en la nieve.
- *Project Zomboid*: indicadores por niveles (moodles) de sed, frío, calor y ropa mojada. Cuando se corta el agua corriente, el agua recogida hay que hervirla.
- *DayZ*: hidratación y energía. Beber de un estanque sin purificar enferma; hay pastillas purificadoras y se puede hervir. Ropa mojada más frío es hipotermia. Zonas de gas tóxico que piden máscara y traje de protección.
- *Don't Starve*: te congelas en invierno y te sobrecalientas en verano (desde *Reign of Giants*), con ropa para cada estación. En la oscuridad total algo te ataca: la luz es un recurso.
- *S.T.A.L.K.E.R.*: la radiación **se acumula** y el contador Geiger avisa. Se baja con antirradiación (y vodka). Hay anomalías que esquivar, y las emisiones obligan a correr a un refugio.
- *Subnautica*: la barra de oxígeno bajo el agua. Un tanque más grande da más tiempo.
- *Red Dead Redemption 2*: la ropa inadecuada para el frío o el calor gasta los núcleos.
- *Frostpunk*: el frío amenaza a toda la ciudad. El pronóstico avisa las caídas de temperatura antes de que lleguen, y el calor sale de un generador que hay que mantener.
- *Kenshi*: regiones con lluvia ácida que dañan a quien cruza sin protección. Y razas que viven el cuerpo distinto: los esqueletos no comen y se reparan en vez de curarse.
- *Valheim*: cada bioma pide su preparación. En la montaña te congelas sin aguamiel de resistencia al frío o ropa de lobo. Mojado y con frío regeneras peor. Junto al fuego y bajo techo quedas **Descansado**. La niebla de las Mistlands pide una luz especial.

---

## 1. La regla: el lugar también pelea

- **Cada terreno tiene su peligro** (ver [Geografía y recursos](../02-mundo/geografia-y-recursos.md)). Al desierto le falta agua; a la tundra, calor; al pantano, aire limpio; a la cueva, luz.
- **El peligro es el precio del material.** El vidrio de duna, el azufre y los hongos luminosos están donde el cuerpo sufre. Quien se prepara los trae y los vende.
- **Solo cuenta lo que haces.** Los peligros avanzan con tus **pasos**, no con el reloj. Quedarte quieto, leer o cerrar Telegram no baja nada.
- **Por etapas, con aviso.** Leve → grave → crítico → derribado. Cada etapa se anuncia antes de llegar, y siempre hay botón de retirada.
- **En zona azul no hay peligro mortal.** Los asentamientos tienen agua, techo y fuego.

**Paso:** moverte un nodo, dar un paso de expedición, hacer 3 acciones de recolección o pelear 3 rondas.

## 2. Rigor contra protección

Cada nodo muestra el **rigor** de sus peligros, de 0 a 3. Tu equipo da **protección** contra cada uno, también de 0 a 3.

| Peligro | Rigor del nodo | Tu protección |
|---|---|---|
| ❄️ Frío | ❄️ a ❄️❄️❄️ | **Abrigo**: capa, ropa, pociones, fuego |
| ☀️ Calor | ☀️ a ☀️☀️☀️ | **Frescor**: ropa ligera, sombra, pociones |
| 🌑 Oscuridad | Penumbra, oscuridad, oscuridad total | **Luz**: antorcha, farol, cristal |
| ⛰️ Altitud | Aire fino 1 a 3 | **Aclimatación**: tiempo en la región |

**La cuenta.** Si tu protección iguala o supera el rigor, no pasa nada. Si falta, el peligro sube de etapa:

| Te falta | Sube una etapa cada |
|---|---|
| 1 punto | 4 pasos |
| 2 puntos | 2 pasos |
| 3 puntos | 1 paso |

Con 1 punto de menos llegas a derribado en 16 pasos: una expedición entera, con tiempo de sobra para volver. Sin nada en un nodo de rigor 3, en 4 pasos.

**La sed y la contaminación** usan su propia barra (§5.3 y §5.4), con las mismas etapas.

**Para bajar de etapa:** sal del nodo, sube tu protección o busca fuego y refugio (§7).

## 3. Morir hasta cierto punto: las etapas

| Etapa | Qué sientes | Qué hace | Qué dice el bot |
|---|---|---|---|
| 🟢 **Bien** | Nada | — | — |
| 🟡 **Leve** | Molestia | Penalización pequeña (ver cada peligro) | "⚠️ Empiezas a sentir frío. Te faltan 2 de abrigo." |
| 🟠 **Grave** | Sufres | Penalización clara. La vida deja de regenerarse | "⚠️ GRAVE. Te quedan unos 4 pasos." + [🏃 Retirada segura] |
| 🔴 **Crítico** | Te vas apagando | −5 % de vida por paso (−3 % por ronda en combate) | "🔴 CRÍTICO. Retírate ya." |
| 💀 **Derribado** | Caes en la nieve, en la arena, en el gas | Como un derribo de combate (ver [Ronda y acciones](../04-combate/ronda-y-acciones.md)) | "Caíste. Un aliado puede levantarte." |

### 3.1 Derribado por el entorno

- **En grupo:** un aliado te levanta con una acción y el remedio del peligro: un trago de agua, una manta, sacarte del gas.
- **Solo:** puedes usar un objeto de emergencia. Las **Sales de Reanimación** (Medicina) te levantan. La **Bengala de rescate** (Ingeniería) llama a una patrulla PNJ en zona amarilla, o publica un contrato de rescate para jugadores en zona roja o negra.
- **Si nadie te levanta, caes.** Se aplica la regla de la zona (ver [Secuelas y muerte](secuelas-y-muerte.md)):

| Zona | Si el entorno te hace caer |
|---|---|
| 🔵 Azul | No puede pasar: no hay peligro mortal |
| 🟡 Amarilla | Tu Esencia queda en la mancha, herida moderada, −10 % de durabilidad. Despiertas en el asentamiento o refugio más cercano |
| 🔴 Roja | Lo anterior, y tu mochila queda en el suelo para quien la encuentre |
| ⚫ Negra | Botín completo, con posible destrucción |
| Mazmorra o banda | Como en mazmorra: vuelves al inicio de la sala |
| Juramento de Hierro | Caer es caer. Por eso sus avisos llegan un paso antes |

Caer por el entorno deja **la herida del peligro**: congelación, quemadura, agotamiento por calor. Nunca dos heridas por la misma caída.

### 3.2 Retirada segura

En etapa grave aparece **[🏃 Retirada segura]**. Te lleva por el camino más corto al asentamiento, refugio o fuente de agua más cercana.
- Si la inicias en grave o antes, **llegas siempre**. Mientras vuelves, el peligro queda congelado en su etapa y no aparecen monstruos nuevos. Otros jugadores sí pueden encontrarte en zonas roja y negra, como siempre.
- Lo que recolectaste viaja contigo. Solo pierdes el resto de la expedición.
- En etapa crítica también puedes retirarte, pero el peligro sigue actuando.

## 4. Peligros por terreno y anillo

### 4.1 Por terreno

Cada región tiene de 2 a 4 terrenos (ver [Geografía y recursos](../02-mundo/geografia-y-recursos.md)).

| Terreno | Peligros propios | ¿Hay agua? | Rigor típico |
|---|---|---|---|
| 🌲 **Bosque** | Picaduras, garrapatas, noche cerrada en la espesura, esporas en la madera podrida | Sí; arroyos a veces dudosos | Bajo |
| 🌾 **Llanura** | Tormentas y rayos (terreno abierto), ola de calor en verano | Sí: pozos y ríos | Bajo |
| 🌊 **Costa y lagos** | Agua profunda, corrientes, agua salada que no se bebe | Salada o dulce | Bajo a medio |
| ⛰️ **Montaña** | Frío en las cumbres, aire fino, derrumbes, gas en las minas | Poca: nieve, manantiales | Medio |
| 🐸 **Pantano** | **Miasma**, esporas, mosquitos, lodo que traga, agua sucia | Sí, pero **sucia** | Medio a alto |
| 🏜️ **Desierto** | **Sed**, calor de día, frío de noche, arenas movedizas, tormentas de arena, escorpiones | **No**: oasis y pozos | Alto |
| ❄️ **Tundra** | **Frío**, ventiscas, nieve profunda, hielo fino sobre agua helada | Nieve, hay que derretirla | Alto |
| 🕳️ **Cueva y subsuelo** | **Oscuridad**, gas de mina, esporas, cuevas inundadas, derrumbes | Poca, a veces sucia | Medio a alto |
| 🌋 **Tierras volcánicas** | Calor extremo, **lava**, gases de azufre, erupciones | **No** | Muy alto |
| 🌸 **Tierras flotantes** | Aire fino, vientos que empujan al borde, tormentas de rayos | Lluvia, hay que juntarla | Medio |

### 4.2 Por anillo

El anillo marca el rigor máximo (ver [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md)). Un parche de desierto en el anillo II tiene rigor 1; el Mar de Dunas del anillo V, rigor 3. La columna Bioma dice el bioma que más pesa en ese anillo.

| Anillo (Lejanía) | Bioma | Peligro estrella | Rigor máximo | Qué pide |
|---|---|---|---|---|
| I · 1-3 | Bosque Susurrante | Picaduras, noche | 1, y nada pasa de leve (protección de novato) | Nada especial |
| II · 4-6 | Pradera Dorada | Tormentas, primer calor | 1 | Capa encerada |
| III · 7-9 | Cueva de Cristal | **Oscuridad**, **resonancia de cristal**, gas | 2 | Luz, forro de plomo |
| IV · 10-12 | Pantano Putrefacto | **Miasma**, mosquitos, agua sucia | 2 | Máscara de carbón, pastillas, repelente |
| V · 13-15 | Desierto Ardiente | **Sed** y calor | 3 | Agua, capa de lino blanco |
| VI · 16-18 | Picos Helados | **Frío**, altitud, avalanchas | 3 | Abrigo de piel, raquetas |
| VII · 19-21 | Ruinas Olvidadas | Polvo de maldición, derrumbes, trampas antiguas; cada región con su regla rara | 3 | Según la región |
| VIII · 22-24 | Ciudadela en Llamas | **Lava**, calor, gases de azufre | 3 | Resistencia al fuego, máscara |
| IX · 25-27 | Abismo Umbrío | **Corrupción del Vacío**, oscuridad mágica | 3 | Filtro bendito, luz sagrada |
| X · 28 y más | Jardines Flotantes | Aire fino, vientos del borde, rayos | 3 | Aclimatación, cuerda |

### 4.3 El clima y las estaciones suman

Ver [Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md). El rigor nunca pasa de 3.

| Clima o estación | Efecto |
|---|---|
| Ventisca | +1 ❄️ y menos luz |
| Ola de calor | +1 ☀️ |
| Lluvia | Te deja **Mojado**: el frío cuenta 1 punto más. Sube la miasma |
| Tormenta | Rayos en terreno abierto |
| Niebla | Menos luz: cuenta como penumbra |
| Invierno | +1 ❄️ en las regiones que ya tienen frío |
| Verano | +1 ☀️ en las regiones que ya tienen calor; algunos oasis se secan |

## 5. Catálogo de peligros

### 5.1 ❄️ Frío: de fresco a hipotermia

| Etapa | Nombre | Fuera de combate | En combate |
|---|---|---|---|
| 🟡 Leve | **Frío** | Recolectas más lento | Iniciativa −10 % |
| 🟠 Grave | **Helado** | La vida no se regenera. Riesgo de **congelación** en manos y pies (herida, ver [Heridas](heridas.md)) | Iniciativa −20 %. Los golpes de escarcha suman el doble a Congelación |
| 🔴 Crítico | **Hipotermia** | −5 % de vida por paso. No puedes recolectar | Iniciativa −30 %, −3 % de vida por ronda |
| 💀 | **Derribado** | Caes en la nieve | — |

- **Dónde:** anillo VI, tundra, cumbres, cuevas de hielo, ventiscas y **las noches del desierto** (❄️1).
- **Mojado:** por lluvia, ríos, pantano o caer al agua. Mientras dura, el frío cuenta 1 punto más. Se seca junto al fuego o después de unos pasos en un nodo seco.
- **Agua helada:** caer por el hielo fino te deja Mojado y sube el frío dos etapas de golpe. Siempre avisa antes: "*el hielo cruje bajo tus botas*".
- **Calor gradual** (como dice [Heridas](heridas.md)): junto a una fogata, el frío baja una etapa por paso, no todo de golpe.
- **Enfermedad asociada:** Gripe de Escarcha (ver [Enfermedades](enfermedades.md)), más probable en etapa grave.

### 5.2 ☀️ Calor: de acalorado a golpe de calor

| Etapa | Nombre | Fuera de combate | En combate |
|---|---|---|---|
| 🟡 Leve | **Acalorado** | La sed baja un 50 % más rápido | Recuperas 1 Aguante menos cada 2 rondas |
| 🟠 Grave | **Agotado por calor** | La sed baja el doble. La vida no se regenera | Aguante máximo −1 |
| 🔴 Crítico | **Golpe de calor** | −5 % de vida por paso. Mareo: a veces el paso te lleva a un nodo que no elegiste | Aguante máximo −2, −3 % de vida por ronda, pierdes la acción rápida |
| 💀 | **Derribado** | Te desplomas | — |

- **Dónde:** desierto de día, tierras volcánicas, Ciudadela en Llamas, olas de calor, junto a la lava.
- **El metal calienta:** la armadura de placas al sol del mediodía cuenta 1 ☀️ más. En el desierto, el guerrero pesado viaja de noche o se pone una sobrecapa de lino.
- **Día y noche:** un día de juego dura 6 horas reales. De noche el desierto baja a ☀️0 y pasa a ❄️1. Quien viaja de noche necesita abrigo, no frescor.
- Caer por calor deja una **quemadura de sol** moderada (grado 2): caer siempre deja al menos una herida moderada (ver [Heridas](heridas.md)).

### 5.3 💧 Sed: la barra de Hidratación

**Una barra nueva, de 0 a 100.** Solo baja **mientras estás activo en terrenos sin agua**. Fuera de línea, en los asentamientos y en los terrenos con agua, no baja nunca. Como el Sustento, es **positiva primero**: bien hidratado ganas algo.

| Hidratación | Estado | Efecto |
|---|---|---|
| 81-100 | 💧 **Refrescado** | El calor tarda un paso más en subir de etapa |
| 41-80 | **Normal** | — |
| 21-40 | 🟡 **Sed** | Precisión −5 % |
| 1-20 | 🟠 **Sed grave** | La vida no se regenera. Aguante máximo −1 |
| 0 | 🔴 **Deshidratación** | −5 % de vida por paso hasta que bebas o caigas |

**Cuánto baja por paso:**

| Terreno o situación | 💧 por paso |
|---|---|
| Bosque, llanura, costa, pantano, asentamientos | 0 (hay agua) |
| Montaña, tundra, cueva, tierras flotantes | −1 |
| Desierto de noche | −2 |
| Tierras volcánicas | −4 |
| **Desierto de día** | **−5** |
| Acalorado ×1,5 · Agotado por calor ×2 · Tormenta de arena ×2 | Se multiplican |

Sin beber, en el desierto de día pasas de 100 a sed en unos 12 pasos. Una cantimplora llena duplica la distancia. **Beber un trago** es una acción rápida, como una poción, y sube 25.

**De dónde sale el agua:**

| Fuente | Dónde | Calidad | Nota |
|---|---|---|---|
| **Pozo** | Asentamientos, refugios, algunos nodos | 🟢 Limpia | Los pozos del camino los construyen jugadores (Construcción) y pueden cobrar peaje |
| **Oasis** | Nodos del desierto | 🟢 Limpia o 🟡 dudosa | Algunos se secan en verano o en una [sequía](../02-mundo/crisis-problemas-y-soluciones.md). En zona roja se pelean |
| **Cisterna** | Refugios construidos | 🟢 Limpia | Alguien tiene que llenarla: la abastecen caravanas |
| **Río, lago, arroyo** | Bosque, llanura, montaña | 🟡 Dudosa | Conviene hervirla |
| **Nieve y hielo** | Tundra, cumbres | 🟢 Al derretirla | Pide fogata y olla. Comer nieve cruda sube el frío una etapa |
| **Lluvia** | Nodos abiertos con lluvia | 🟢 Limpia | Con un colector o un odre abierto |
| **Cactus de agua, lianas** | Desierto, bosque | 🟢 Limpia | Poca, pero salva (Herboristería) |
| **Charco, pantano, agua estancada** | Pantano, cueva | 🔴 **Sucia** | Riesgo alto de disentería |
| **Mar** | Costa | 🧂 Salada | No se bebe: baja la Hidratación. La Destilación la vuelve dulce |

**Agua sucia → disentería.** El agua 🟡 dudosa tiene riesgo bajo; la 🔴 sucia, alto. La disentería (ver [Enfermedades](enfermedades.md)) hunde el Sustento y ahora también la Hidratación. Se evita así:
- **hirviendo** el agua: fogata y olla, una acción fuera de combate;
- con **pastillas purificadoras** (Alquimia), que limpian cualquier agua;
- con una **cantimplora con filtro** (Ingeniería), que limpia la dudosa pero no la sucia.

**Envenenar un pozo** es un delito grave (ver [Crimen y justicia](../06-contenido/crimen-y-justicia.md)), y un caso clásico de [Investigaciones](../06-contenido/investigaciones.md).

**Recipientes:**

| Recipiente | Tragos (+25 cada uno) | Peso | Quién lo hace |
|---|---|---|---|
| Cantimplora de cuero | 4 | Ligera | Peletería (el PNJ vende una peor, de 3) |
| Odre grande | 8 | Pesado | Peletería |
| Frasco de vidrio de duna | 3; el agua nunca se ensucia | Ligero, frágil | Joyería, con arena del desierto |
| Cantimplora con filtro | 4; limpia el agua dudosa | Media | Ingeniería y Peletería |
| Barril de caravana | 40 | Carga de montura o carro | Carpintería |

### 5.4 ☣️ Contaminación: una barra que se acumula

**Una barra nueva, de 0 a 100.** Sube en los nodos contaminados y baja sola fuera de ellos. Es la radiación de *S.T.A.L.K.E.R.* con fuentes de fantasía. No es la Toxicidad de las pociones (ver [Condiciones](condiciones.md)): son dos barras distintas.

- En un nodo ☣️1, ☣️2 o ☣️3 sube **+5, +10 o +20 por paso**.
- La **máscara** con el filtro correcto resta su nivel al rigor: filtro común 1, bueno 2, obra maestra 3. Los filtros se gastan con los pasos, así que siempre hay demanda.
- Fuera de la contaminación baja 10 por paso. En un asentamiento o refugio llega a 0 en una hora real, también fuera de línea.

| Barra | Etapa | Efecto |
|---|---|---|
| 0-24 | 🟢 Limpio | — |
| 25-49 | 🟡 Leve | Tos: precisión −5 %. Los PNJ notan el olor |
| 50-74 | 🟠 Grave | Vida máxima −10 %, curación recibida −20 %. En cada paso, riesgo de la enfermedad de la fuente |
| 75-99 | 🔴 Crítico | −5 % de vida por paso (−3 % por ronda) |
| 100 | 💀 Derribado | — |

**Fuentes:**

| Fuente | Dónde | Filtro que sirve | Enfermedad que puede dejar | Nota |
|---|---|---|---|---|
| 🐸 **Miasma** | Pantano (anillo IV), agua estancada | Carbón | Fiebre del Pantano | Sube con la lluvia y en verano |
| ⛏️ **Gas de mina** | Cuevas, minas profundas | Carbón | Tos del Minero | **Explota con llama abierta**: antorcha + gas = quemaduras a todo el grupo. Se usa farol de seguridad |
| 🍄 **Esporas** | Cuevas, bosque podrido, pantano | Lino fino | — | Alucinaciones: el estrés sube 2 por paso |
| 💎 **Resonancia de cristal** | Cueva de Cristal (anillo III), vetas crudas | Ninguno: **forro de plomo** o distancia | Temblor Arcano | Un **péndulo de resonancia** avisa, como un contador Geiger |
| 🌋 **Gases de azufre** | Tierras volcánicas, anillo VIII | Carbón | — | Se juntan en las hondonadas; el mapa marca los nodos bajos |
| 🌑 **Corrupción del Vacío** | Abismo Umbrío (anillo IX), grietas | **Bendito** | Fiebre del Vacío | Sube el estrés. **No** se vuelve Corrupción permanente por sí sola: esa es una elección (ver [Mente](mente.md)). Si se pierde la carrera de una Fiebre del Vacío contraída aquí, deja Corrupción menor, que el templo limpia |
| 🐀 **Plaga** | Nodos en brote durante una epidemia | Lino fino o bendito | Plaga Pálida | Solo durante eventos (ver [Enfermedades](enfermedades.md)) |
| 🏛️ **Polvo de maldición** | Ruinas Olvidadas (anillo VII), criptas | Bendito | Maldición menor | Se levanta con un ritual del templo |

### 5.5 Los demás peligros

| Peligro | Dónde | Cómo sube (leve → grave → crítico) | Salida | Protección |
|---|---|---|---|---|
| ⛰️ **Altitud** (aire fino) | Cumbres de los Picos Helados, Jardines Flotantes | Fatiga al doble → Aguante máximo −1 y dolor de cabeza → confusión y −5 % de vida por paso | Bajar un nodo baja una etapa | Aclimatación: +1 por cada hora real en la región, también fuera de línea (tope 3). Té de altura. El **Mal del Viajero** ([Enfermedades](enfermedades.md)) es la versión suave al llegar |
| 🌑 **Oscuridad** | Cuevas, subsuelo, noche en la espesura, Abismo | Penumbra: precisión −10 %, no ves los nodos vecinos → Oscuridad: precisión −25 %, trampas invisibles, estrés +2 por paso → Oscuridad total: **algo te muerde** en cada paso | Encender luz o volver a un nodo iluminado | Antorcha, farol, cristal luminoso, luz sagrada (§7) |
| 🌊 **Agua profunda** | Costa, lagos, ríos crecidos, cuevas inundadas | Barra 🫧 **Aire** de 3 pasos bajo el agua → sin aire: −10 % de vida por paso → ahogándote | [⬆️ Subir] siempre visible: una acción | Vejiga de aire, casco de buzo, poción de respirar bajo el agua. **Las placas hunden**: con armadura pesada no se nada, se cruza por puente o en barca |
| 🏜️ **Arenas movedizas y lodo** | Desierto, pantano | Hasta la rodilla → hasta la cintura (no puedes huir) → hasta el pecho | Quedarte quieto frena el hundimiento; soltar peso; que un aliado tire una cuerda | Vara de sondeo para detectarlas, cuerda, mapa de peligros |
| ⛈️ **Tormenta y rayos** | Terreno abierto: llanura, cumbres, tierras flotantes | Se anuncia 2 pasos antes → el rayo busca a quien lleve más metal: −25 % de vida, quemadura y 1 ronda aturdido | Refugio, bajar a un valle, soltar el arma de metal | Pararrayos en los refugios, capa encerada |
| 🌪️ **Tormenta de arena** | Desierto | Sin visibilidad → sed al doble → puedes perder el rumbo y retroceder un nodo | Refugio | Velo de desierto, brújula |
| 🌋 **Lava y erupciones** | Tierras volcánicas, Ciudadela en Llamas | Calor radiante: +1 ☀️ → en nodos de borde, un empujón deja quemadura grave → erupción avisada 2 pasos antes: quemaduras graves a quien se quede | Salir del nodo | Botas de obsidiana, capa ignífuga, poción de resistencia al fuego |
| 🦟 **Picaduras e insectos** | Pantano, bosque, desierto (escorpiones), cuevas (arañas) | Picazón → las picaduras suman a la barra de **Veneno** (ver [Daño y estados](../04-combate/dano-y-estados.md)) → la enfermedad que traen (mosquitos: Fiebre del Pantano) | Un enjambre se espanta con humo o fuego | Repelente, mosquitero para acampar |
| 🌨️ **Nieve profunda y avalanchas** | Tundra, Picos Helados | Moverte cuesta el doble de Vigor → no puedes huir → avalancha avisada ("*la nieve cruje sobre ti*"): si no te apartas, quedas enterrado, Mojado y con frío | Un aliado te desentierra, o sales solo en 3 rondas | Raquetas de nieve, pala plegable |
| 🌬️ **Vientos del borde** | Tierras flotantes, Jardines Flotantes | Aviso de ráfaga 1 paso antes → si no te agarras (reacción), te arrastra a un nodo más bajo con una fractura. Nunca al vacío | Agarrarse, alejarse del borde | Cuerda con ancla, botas con clavos |
| ☔ **Lluvia ácida** | Rara, anillos IV y VIII | Gasta la durabilidad del equipo expuesto y suma ☣️1 | Techo | Capa encerada |

**Combinaciones que conviene conocer:**
- Antorcha + gas de mina = explosión.
- Placas + agua profunda = te hundes. Placas + sol del mediodía = +1 ☀️. Placas + tormenta = el rayo te elige a ti.
- Mojado + frío = el frío cuenta 1 punto más.
- El desierto de noche pide abrigo, no frescor.
- El calor acelera la sed.
- El humo de una fogata espanta a los mosquitos, pero en una cueva con gas no se enciende fuego.

**Tope:** en un mismo nodo, como máximo **dos peligros** suben a la vez. El bot muestra primero el más urgente.

## 6. En el combate por turnos

- El entorno actúa **al principio de cada ronda**, antes de las acciones, y aparece en la cabecera del mensaje vivo.
- Los cambios del entorno **se avisan como el ataque de un jefe** (ver [Avisos y tácticas](../04-combate/avisos-y-tacticas.md)): "*⚠️ La tormenta se acerca: en 2 rondas cae un rayo sobre quien lleve más metal.*"
- **Las criaturas nativas no sufren su entorno.** Los visitantes sí, incluidos los monstruos de otro bioma y los otros jugadores.

| Entorno | Efecto por ronda |
|---|---|
| ❄️ **Frío** | Iniciativa −10, −20 o −30 % según la etapa; en crítico, −3 % de vida |
| ☀️ **Calor** | Menos Aguante: recuperas 1 menos cada 2 rondas, luego máximo −1, luego máximo −2 y −3 % de vida |
| 💧 **Sed** | En terreno sin agua, cada 3 rondas cuentan como un paso. En grave, la vida no se regenera; en crítico, −3 % por ronda |
| ☣️ **Gas** | En nodos ☣️2 y ☣️3, daño por ronda que **ignora la armadura** (1 o 2 % de la vida), y la barra de Contaminación sube. El filtro correcto lo anula |
| 🌑 **Oscuridad** | Precisión −10, −25 o −40 %; a distancia, el doble. En oscuridad total, lo que vive ahí golpea cada 3 rondas |
| 🌊 **Agua profunda** | Sin armas a dos manos ni hechizos hablados. El Aire baja 1 por ronda sumergido |
| 🌨️ **Nieve profunda** | Cambiar de fila cuesta la acción entera, huir falla el doble, esquivar cuesta +1 Aguante |
| 🏜️ **Arenas movedizas** | Te hundes una etapa por cada ronda en que atacas. Un aliado con cuerda te saca con una acción rápida |
| ⛈️ **Tormenta** | Un rayo avisado cada 4 rondas sobre quien lleve más metal. Si estás **Agrupado**, salta a tus vecinos; **Disperso**, solo te pega a ti |
| 🌋 **Lava** | Los empujones y derribos cerca del borde dejan una quemadura grave |

- **Usar el entorno:** atraer al rival sin máscara hacia la miasma, pelear de noche en el desierto contra quien no trajo abrigo, retirarse a un nodo iluminado cuando te persigue algo que odia la luz. En PvP, quien se preparó para la zona le gana a quien solo trajo más daño. El tope de golpe de PvP (40 % de la vida) también limita lo que el entorno quita en una ronda.
- **Jefes con entorno:** el Wyrm de las Dunas levanta una tormenta de arena que ciega a la vanguardia; un Guardián de hielo puede subir el ❄️ de la sala en cada fase (ver [Jefes](../06-contenido/jefes.md)).

```
⚔️ Ronda 4 · Escorpiones de Vidrio ×2
🏜️ Mediodía ☀️☀️☀️ · tu frescor ☀️☀️
🌡️ Acalorado · 💧 46 (cada 3 rondas −7)

⚠️ El viento trae arena: TORMENTA en 2 rondas
(precisión −25 %, sed al doble).

🟥 Tú — Cazador Supervivencia · Retaguardia
❤️ 610/940   🔋 Aguante ●●●○○ (calor: −1 cada 2 rondas)
Turnos: Tú → ESCORPIÓN → Bram → ESCORPIÓN
⏱ 60 s

[🏹 Disparo]      [🪤 Trampa]
[💧 Beber (+25)]  [🧪 Objetos]
[🔁 Fila / Formación] [🏃 Huir]
```

## 7. Protección: qué se fabrica y quién lo hace

La capa es la ranura de clima (ver [Equipamiento](../03-personaje/equipamiento.md)). El PNJ vende lo básico, peor; lo bueno lo hacen los artesanos (ver [Fabricación](../07-economia/fabricacion.md)).

### 7.1 Equipo

| Objeto | Contra | Protección | Oficio | Materia prima (terreno) |
|---|---|---|---|---|
| Capa de lana | Frío | Abrigo 1 | Sastrería | Lana (llanura) |
| Capa de piel gruesa | Frío | Abrigo 2 | Peletería | Pieles gruesas (tundra) |
| Abrigo de expedición | Frío | Abrigo 3 | Sastrería y Peletería | Pieles, grasa, lana |
| Capa de lino blanco y turbante | Calor | Frescor 2 | Sastrería | Lino (llanura) |
| Velo de desierto | Calor, tormenta de arena | Frescor 1; ves en la tormenta | Sastrería | Lino, algodón |
| Capa encerada | Lluvia, lluvia ácida | Nunca quedas Mojado | Sastrería | Tela, grasa (tundra) |
| Capa ignífuga | Fuego, lava | Frescor 1 y resistencia al fuego | Sastrería | Escamas de salamandra (Desuello, volcánico) |
| Forro de plomo | Resonancia de cristal | Resta 2 a la resonancia; pesa | Herrería | Plomo (montaña) |
| Botas de obsidiana | Lava | Sin quemaduras por el suelo | Herrería | Obsidiana (volcánico) |
| Botas con clavos | Hielo, vientos del borde | No resbalas; +1 para agarrarte | Herrería | Hierro |
| Raquetas de nieve | Nieve profunda | Anulan el Vigor doble | Carpintería y Peletería | Madera, cuero |
| Máscara con filtro de carbón | Miasma, gas, azufre | Filtro 1 a 3 según la calidad | Sastrería (máscara) y Alquimia (carbón activado) | Tela, carbón (montaña) |
| Filtro de lino fino | Esporas, plaga | Filtro 1 a 3 | Sastrería (Textil médico) | Lino |
| Filtro bendito | Vacío, polvo de maldición, plaga | Filtro 1 a 3 | Sastrería y una bendición del templo | Lino, reactivo sagrado |
| Péndulo de resonancia | Avisa la resonancia de cristal | — | Joyería | Cristal (cueva) |
| Canario de mina | Avisa el gas un paso antes | — | Ganadería | — |
| Antorcha | Oscuridad | Luz 2 durante 10 pasos. **Nunca con gas** | Carpintería (o PNJ) | Madera, grasa |
| Farol de aceite | Oscuridad | Luz 2, 30 pasos por carga | Herrería (farol) y Destilación (aceite) | Metal, grasa (tundra) |
| Farol de seguridad | Oscuridad con gas | Luz 2, llama cerrada | Ingeniería | Metal, vidrio |
| Cristal luminoso | Oscuridad | Luz 1 sin límite | Joyería | Cristales, hongos luminosos (cueva) |
| Luz sagrada | Oscuridad mágica del Abismo | Luz 3; la única que sirve ahí | Sacerdote (habilidad) o reliquia del templo | — |
| Vejiga de aire | Agua profunda | +3 pasos de Aire | Peletería | Vejiga de bestia |
| Casco de buzo | Agua profunda | +10 pasos de Aire; pesado | Ingeniería | Metal, vidrio, cuero |
| Vara de sondeo | Arenas movedizas, hielo fino | Las detecta antes de pisar | Carpintería | Madera |
| Cuerda | Arenas, avalanchas, vientos | Sacar a un aliado; anclarte | Tejeduría | Fibra |
| Brújula | Tormenta de arena, niebla | No pierdes el rumbo | Ingeniería | Metal, imán |
| Olla de campaña | Agua sucia, nieve | Hervir, derretir, cocinar caldos | Herrería | Metal |
| Repelente | Insectos | Menos picaduras durante 20 pasos | Herboristería y Alquimia | Hierbas |
| Mosquitero | Insectos al acampar | Acampar en el pantano sin picaduras | Sastrería | Tela fina |
| Bengala de rescate | Quedar derribado solo | Llama a una patrulla o publica un rescate | Ingeniería | Pólvora, azufre (volcánico) |

**Encantamiento** agrega runas de abrigo o de frescor a una capa: +1 al nivel, sin ocupar otra ranura.

### 7.2 Pociones y comida

Las pociones suman Toxicidad (ver [Condiciones](condiciones.md)), así que no se pueden encadenar.

| Consumible | Efecto | Oficio |
|---|---|---|
| Poción de Calor Interno | +1 de abrigo durante 20 pasos | Alquimia |
| Poción de Frescor | +1 de frescor durante 20 pasos | Alquimia |
| Poción de Resistencia al Fuego | Menos quemaduras por lava y fuego | Alquimia |
| Poción de Pulmón Limpio | +1 de filtro y −20 de Contaminación | Alquimia |
| Poción de respirar bajo el agua | Aire sin límite durante 10 pasos | Alquimia |
| Pastillas purificadoras | Limpian cualquier agua | Alquimia |
| Sales de rehidratación | Bajan una etapa de sed además del trago | Alquimia |
| Caldo caliente | Baja una etapa de frío y da +1 de abrigo durante 10 pasos | Cocina |
| Sopa fría o jugo de cactus | +25 de Hidratación y +1 de frescor durante 10 pasos | Cocina |
| Té de altura | +1 de aclimatación durante 10 pasos | Cocina y Herboristería |

### 7.3 Fuego y refugio

- **Kit de fogata** (leña de Tala o Aserradero, yesca): monta una fogata en un nodo seco y sin gas. Junto al fuego el frío baja una etapa por paso, la ropa se seca, se hierve agua y se cocina. En zona roja, otros ven el humo.
- **Tienda de campaña** (Sastrería): un descanso corto en cualquier nodo sin combate. Frío, calor y Contaminación bajan una etapa y no suben mientras descansas.
- **Refugios construidos** (Construcción): cabañas en zona amarilla y refugios en zona roja, según las reglas de [Sistema de construcción](../09-construccion/sistema-de-construccion.md). Dentro no suben los peligros del entorno. No son zona azul: en zona roja se pueden asaltar (ver [Defensa](../09-construccion/defensa-y-protecciones.md)).

| Refugio | Dónde | Qué da | Quién lo construye |
|---|---|---|---|
| Cabaña con chimenea | Tundra, cumbres | Frío a cero, descanso, ropa seca | Construcción y Carpintería |
| Refugio de la duna con cisterna | Desierto | Sombra; agua limpia si la cisterna está llena | Construcción e Ingeniería |
| Estación de filtrado | Pantano | Aire limpio (baja la Contaminación) y agua limpia | Construcción, Ingeniería y Alquimia (filtros) |
| Puesto de luz | Cuevas | Luz permanente en el nodo y sus vecinos | Construcción y Joyería |
| Santuario sellado | Abismo Umbrío | Filtra el Vacío | Construcción y templo |

Los refugios **cobran peaje** (lo decide el dueño) y necesitan **mantenimiento**: leña, filtros y agua que traen las caravanas. Un refugio bien puesto en el Mar de Dunas es un negocio, y en zona roja, un botín.

### 7.4 Servicios de jugadores

| Quién | Qué vende |
|---|---|
| **Guía de región** (ver [Roles](../00-vision/roles-y-caminos-de-juego.md)) | Conoce los oasis, las arenas y las bolsas de gas; cobra por cruzar a un grupo |
| **Cartógrafo** (Inscripción) | **Mapas de peligros**: rigor, fuentes de agua y arenas movedizas antes de pisar |
| **Aguador** (Comercio) | Agua en la puerta del desierto; contratos para llenar cisternas |
| **Rescatista** | Toma los contratos de las bengalas de rescate |
| **Criador** (Ganadería) | Lagartos de carga que llevan un barril de agua; yaks que abren camino en la nieve profunda |

## 8. Curación

La tabla general de problema → cura y el oficio de médico están en [Curación](curacion-y-tratamientos.md). Aquí va lo que deja el entorno.

| Daño | Primera respuesta (en el campo) | Cura completa | Quién |
|---|---|---|---|
| Hipotermia | Fogata, manta, caldo caliente; calor gradual | Reposo bajo techo | Cualquiera; posada |
| Congelación (herida) | Calor gradual, nunca brusco | Tratamiento; amputación limpia si hay necrosis | Médico |
| Golpe de calor | Sombra, agua, paños húmedos | Reposo | Cualquiera |
| Quemadura de sol o de lava | Ungüento | Injerto en grado 3 | Alquimia, Médico |
| Deshidratación | Beber: cada trago sube 25 | Sales de rehidratación y reposo | Alquimia |
| Disentería | Carbón, agua hervida | Purga y dieta | Alquimia, Cocina, Médico |
| Contaminación alta | Salir del nodo; Poción de Pulmón Limpio | Reposo en un asentamiento; purga | Alquimia |
| Enfermedad de la fuente (Fiebre del Pantano, Tos del Minero, Temblor Arcano, Fiebre del Vacío, Plaga Pálida) | La de cada una | Ver [Enfermedades](enfermedades.md) | Médico |
| Vacío (estrés y fiebre) | Salir; filtro bendito | Purificación en el templo | Templo |
| Mal de altura | Bajar un nodo; té de altura | Aclimatarse (el tiempo cuenta también fuera de línea) | — |
| Estrés por oscuridad o esporas | Luz, compañía | Taberna, bardo (ver [Mente](mente.md)) | Bardo |
| Casi ahogado | Reanimar (Primeros Auxilios) | Reposo; riesgo de neumonía si además hacía frío | Enfermero |
| Rayo | Curación, vendas | La quemadura; a veces una conmoción (ver [Heridas](heridas.md)) | Médico |
| Picaduras | Antídoto, repelente | El antídoto de ese veneno; la enfermedad que trajeron | Alquimia |
| Enterrado por avalancha | Desenterrar, dar calor | Fracturas o contusiones | Médico |

Descansar en una posada, en casa o en un refugio devuelve todas las barras del entorno a cero, también fuera de línea.

## 9. Linajes: quién resiste qué

Todo sale del rasgo de cuerpo que cada linaje ya tiene (ver [Creación de personaje](../03-personaje/creacion-de-personaje.md)). Ninguno ignora un peligro entero: más allá del anillo V, el equipo sigue haciendo falta.

| Linaje | Rasgo que ya tiene | En el entorno |
|---|---|---|
| **Humano** | Se aclimata en la mitad del tiempo | Altitud y Mal del Viajero: la mitad |
| **Enano** | Resiste enfermedades de mina y de frío | Tos del Minero a la mitad por gas y polvo; le cuesta más contraer la Gripe de Escarcha |
| **Gnomo** | Cabe por pasadizos que otros no | Atajos que esquivan nodos de peligro en cuevas y laberintos |
| **Elfo del Alba** | Resiste la Quemadura de Maná | La resonancia de cristal le sube a la mitad |
| **Elfo Sombrío** | Ve de noche sin penalización | Ignora la penumbra y la oscuridad; no la oscuridad total ni la mágica del Abismo |
| **Orco** | Las heridas leves no le penalizan | Las congelaciones y quemaduras leves tampoco |
| **Trol** | Regenera al doble; come el doble | Congelaciones y quemaduras sanan al doble. Su Hidratación baja más rápido, como su Sustento |
| **Renacido** | No sangra ni enferma de males naturales; casi no come | No contrae las enfermedades naturales del entorno (disentería, Fiebre del Pantano, Tos del Minero) y su Hidratación baja a la mitad. El Vacío y la plaga le afectan, y su barra de Contaminación sube igual |
| **Taurino** | Carga más peso | Lleva odres y barriles sin penalización |
| **Goblin** | Resiste venenos y explosiones | Picaduras venenosas y explosiones de gas: la mitad |
| **Licántropo** | Olfato | Huele si el agua es segura y detecta el gas un paso antes. En forma bestial viaja más rápido: menos pasos, menos exposición |
| **Dracónido** | Resiste frío y calor extremos | El frío y el calor le cuentan 1 punto menos de rigor. Con vuelo corto cruza ríos, grietas de lava y arenas movedizas conocidas |

## 10. Cómo se ve en Telegram: cruzar el Mar de Dunas

Un solo mensaje vivo que se edita en cada paso. Mira lleva una capa de lino blanco (le falta un punto de frescor) y una sola cantimplora de cuero.

**La salida:**

```
🏜️ Expedición · Lejanía 13 · Mar de Dunas
Zona 🔴 roja · Mediodía ☀️☀️☀️
Tu frescor: ☀️☀️ (capa de lino blanco)
💧 Hidratación ▓▓▓▓▓▓▓▓▓▓ 100 · Refrescado
🌡️ Calor 🟢 bien
🎒 Cantimplora 4/4
🗺 Mapa de peligros de Lisbeth (cartógrafa, primavera)
📍 Paso 0/20

[➡️ Avanzar] [🎒 Mochila] [🗺 Mapa] [🏃 Volver]
```

**Paso 6:** como le falta un punto de frescor, el calor ya subió.

```
📍 Paso 6/20 · Dunas Rojas
💧 ▓▓▓▓▓▓▓░░░ 67
🌡️ Calor 🟡 Acalorado · te falta 1 de frescor
   La sed baja un 50 % más rápido
⛏️ Encontraste: Vidrio de duna ×3

⚠️ A este ritmo, sed en 4 pasos.
💡 Según tu mapa, el Oasis de las Tres Palmas está a 2 pasos.

[➡️ Avanzar] [💧 Beber (+25)] [🏃 Volver]
```

**Paso 8:** el oasis está seco. El mapa era de primavera.

```
📍 Paso 8/20 · 🌴 Oasis de las Tres Palmas
💧 ▓▓▓▓▓░░░░░ 52
🟤 SECO: el verano se llevó el agua.
🌴 Queda la sombra: el calor baja una etapa (🟢 bien)
🎒 Cantimplora 4/4

[➡️ Seguir] [💧 Beber (+25)] [🏃 Volver]
```

**Paso 12:** el aviso.

```
📍 Paso 12/20 · Llano de Sal
💧 ▓▓▓▓▓▓░░░░ 57 · 🌡️ 🟡 Acalorado
🎒 Cantimplora 3/4

⚠️ TORMENTA DE ARENA en 2 pasos.
Durante la tormenta: sed al doble y puedes perder el rumbo.
🏚 Refugio de la Duna a 1 paso (peaje 10 🪙, cisterna 🟢 llena)

[🏚 Ir al refugio] [➡️ Arriesgarte] [🏃 Volver]
```

**Paso 19:** Mira se arriesgó. Con tormenta y calor, cada paso cuesta cuatro veces más agua.

```
📍 Paso 19/20 · Hondonada Blanca · 🌪 tormenta
💧 ▓▓░░░░░░░░ 19 · 🟠 SED GRAVE
🌡️ 🟠 Agotado por calor
   La vida no se regenera · Aguante máx. −1
🎒 Cantimplora 0/4

🟠 1 paso para la deshidratación.
🟠 1 paso para el golpe de calor.
🏚 Puesto del Pozo Hondo (gremio Arena Roja): 2 pasos.
   Con la retirada segura llegas sí o sí.

[🏃 Retirada segura al Pozo Hondo]
[➡️ Seguir (peligro)] [🎒 Mochila]
```

**La llegada:**

```
🏚 Puesto del Pozo Hondo · a salvo
🪣 Bebiste del pozo (peaje 10 🪙): 💧 19 → 100
🌡️ Calor 🟢 bien (sombra y descanso)
🎒 Traes: Vidrio de duna ×11 · Sal de roca ×6
   · Escama de Escorpión de Vidrio ×2
🌪 La tormenta pasa en unos 20 min.
💡 Lisbeth publicó un mapa de verano: 40 🪙.

[➡️ Seguir la expedición] [🏠 Volver al asentamiento]
```

En `/cuerpo`, el entorno ocupa una línea más: `🌡️ Acalorado · 💧 67 · ☣️ 0`.

## 11. Principios anti-frustración

1. **Nunca sin aviso.** Toda etapa se anuncia antes, con cuántos pasos quedan.
2. **Siempre hay retirada.** La retirada segura que empieza en etapa grave llega siempre.
3. **Azul es azul.** Asentamientos, escaleras y piedras de paso no tienen peligros del entorno.
4. **Solo cuenta lo que haces.** Pasos, no minutos. Fuera de línea todo se congela, y en un asentamiento o refugio todo se recupera, también fuera de línea.
5. **Protección de novato.** Hasta el nivel 10 ningún peligro pasa de leve, y el entorno no contagia enfermedades.
6. **Siempre hay una versión barata.** El PNJ vende cantimplora, antorcha y capa de lana. Son peores que las de un artesano, pero nadie queda fuera por falta de oro.
7. **Sin doble castigo.** Caer por el entorno sigue la regla de la zona y deja una sola herida. Como máximo dos peligros suben a la vez.
8. **Prepararse gana.** Con la protección justa, cada peligro queda en cero. La dificultad está en preparar la mochila, no en la suerte.
9. **Todo se lee en una línea.** En `/cuerpo` y en la cabecera de la expedición.
10. **Nada arruina un personaje, pero el cuerpo recuerda.** Fuera del Juramento de Hierro, lo peor que hace el entorno por sí solo es una caída con las reglas de su zona y una herida. Solo una congelación o un pulmón descuidados pese a todos los avisos pueden dejar una secuela definitiva, que se compensa (ver [Secuelas y muerte](secuelas-y-muerte.md) §5). La Contaminación del Vacío no deja Corrupción permanente por sí sola.

## 12. Cómo se conecta

Su fila en la [Red de sistemas](../00-vision/red-de-sistemas.md):

| Consume | Produce | Depende del farmeo | Depende de la fabricación | Depende de la progresión |
|---|---|---|---|---|
| Ropa de clima, cantimploras, máscaras, filtros, luz, pociones, comida, leña, refugios | Demanda constante para más de diez oficios, pacientes para los médicos, valor para los materiales de zonas hostiles, contratos de guía y de rescate | Pieles, lino, lana, grasa, carbón, obsidiana, hierbas | Todo el equipo de protección | Anillo del equipo, rango de los artesanos, aclimatación |

**A quién le da trabajo:**

| Oficio | Qué vende aquí |
|---|---|
| **Sastrería** | Capas de clima, máscaras, filtros de lino, mosquiteros, tiendas |
| **Peletería** | Capas de piel, cantimploras, odres, vejigas de aire |
| **Herrería** | Ollas, faroles, forros de plomo, botas de obsidiana y con clavos |
| **Carpintería** | Antorchas, varas de sondeo, raquetas, barriles |
| **Ingeniería** | Faroles de seguridad, cantimploras con filtro, brújulas, cascos de buzo, bengalas, pararrayos |
| **Joyería** | Frascos de vidrio de duna, cristales luminosos, péndulos de resonancia |
| **Alquimia** | Pociones de resistencia, pastillas purificadoras, carbón activado, repelente, sales de rehidratación |
| **Herboristería** | Cactus de agua, hierbas para repelente y té de altura |
| **Cocina** | Caldos calientes, sopas frías, jugos |
| **Destilación** | Aceite de farol; agua dulce a partir de agua de mar |
| **Construcción** | Pozos, cisternas, cabañas, refugios, estaciones de filtrado |
| **Ganadería** | Monturas del desierto y de la nieve, canarios de mina |
| **Inscripción** | Mapas de peligros |
| **Medicina y templo** | Curar lo que deja el entorno |

**Orden de construcción sugerido** (junto con la v4 de [Salud](README.md)):
1. Frío, calor y la barra de Hidratación, con fogatas y cantimploras.
2. La barra de Contaminación, oscuridad y agua profunda.
3. El resto de los peligros y los refugios construidos.

Ver D-36 en [Decisiones](../00-vision/decisiones.md) y P-23 en [Preguntas abiertas](../00-vision/preguntas-abiertas.md).
