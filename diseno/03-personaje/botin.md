# Botín

> **Módulo** [03 · Personaje](README.md) · **Depende de:** [Equipamiento](equipamiento.md), [Economía](../07-economia/economia.md) (Mercado Negro, monedas), [Jefes](../06-contenido/jefes.md), [Bestiario](../06-contenido/bestiario.md) · **Se conecta con:** [Fabricación](../07-economia/fabricacion.md), [Profesiones](../07-economia/profesiones.md), [Cacerías](../06-contenido/cacerias.md), [Mazmorras y bandas](../06-contenido/mazmorras-y-bandas.md), [Misiones y exploración](../06-contenido/misiones-y-exploracion.md), [Gremios y social](../08-social/gremios-y-social.md), [Descubrimiento y colecciones](descubrimiento-y-colecciones.md), [Crimen y justicia](../06-contenido/crimen-y-justicia.md), [Balance](balance.md) · **Estado:** propuesta

> **Nota (D-58).** Los ejemplos todavía nombran pisos, tramos y Guardianes de piso, que D-58 quitó. Hasta el barrido general, *tramo* se lee como *anillo* del [mapa infinito](../02-mundo/mapa-infinito-y-viaje.md) (el tier T1 a T10 sigue igual) y el Guardián como un jefe de mundo de ese anillo.

Pediste un sistema de botín **bastante variado**, de equipo o de cualquier otra cosa. Este documento dice qué puede caer, de dónde, con qué probabilidad, cómo se reparte en grupo, cómo se muestra en un chat y cómo se evita que el mundo se llene de objetos sin valor.

**De dónde sale.**
- *Diablo* y *Diablo II*: prefijos y sufijos con nombre, objetos únicos y de conjunto, objetos sin identificar que se leen con un pergamino o con Deckard Cain, y los objetos etéreos de *Diablo II* (más fuertes, pero no se pueden reparar).
- *Path of Exile*: afijos por niveles, únicos con texto de historia, objetos corrompidos que ya no se pueden modificar, cartas de adivinación (juntas un mazo completo y lo cambias por un objeto concreto) y **filtros de botín** que escribe el jugador y comparte la comunidad.
- *World of Warcraft*: tablas de botín por jefe, **botín personal** con 2 horas para regalarlo dentro del grupo, Necesidad/Codicia, tiradas extra (desde *Mists of Pandaria*), **protección contra mala racha**, el Gran Tesoro semanal (aquí, Tesoro Semanal) y el tope de dos legendarios equipados de *Legion*. También una lección: en *Shadowlands* quitó el "forjado de titanes" (mejoras al azar sobre un objeto ya ganado) porque nadie sentía terminado su equipo.
- *EverQuest*: sus gremios inventaron los **DKP**, puntos por asistir a la banda que se gastan en botín.
- *Albion Online*: el **Mercado Negro** compra lo que fabrican los jugadores y lo siembra en el botín de monstruos y cofres.
- *Monster Hunter*: cada parte rota da su material, y capturar a la presa da una tabla de recompensas distinta de matarla.
- *Borderlands*: armas armadas por piezas, cada fabricante con su estilo, y por eso millones de combinaciones.
- *Elden Ring*: el **Recuerdo** de cada jefe, que se cambia por una de dos piezas, y los Mausoleos Andantes, que duplican un Recuerdo para conseguir la otra.
- *Dark Souls*: la historia del mundo contada en la descripción de los objetos.
- *NetHack*: el arma maldita que se te pega a la mano.
- *EVE Online*: el registro de cada nave destruida, con lo que llevaba y quién la destruyó.

**Por qué conviene.**
- Cada combate termina con una sorpresa chica, y eso hace volver.
- Casi todo lo que cae es **materia prima de otro jugador**: el botín mueve la economía en lugar de reemplazarla.
- Lo importante no depende de la suerte. Lo divertido, sí.

---

## 1. Las cuatro reglas del botín

1. **Nada sale de la nada** (ver [Red de sistemas](../00-vision/red-de-sistemas.md)).
   - Todo el equipo que sueltan monstruos y cofres lo fabricó un jugador y lo compró el Mercado Negro.
   - Los jefes sueltan **artefactos**, que forja un artesano.
   - Las reliquias antiguas salen **rotas**, y las restaura un artesano.
2. **Lo importante es seguro; lo divertido, al azar.** El Recuerdo, la Constancia (protección contra mala racha) y el Tesoro Semanal garantizan el progreso. El azar decide las sorpresas: una carta, una curiosidad, un afijo raro.
3. **La rareza ensancha, no sube.** Un objeto raro cambia **cómo** juegas, no cuánto pegas. Dentro de un tramo, el mejor botín y la mejor fabricación tienen el mismo techo de Poder de Objeto (§4.1).
4. **Todo se gasta, se desmonta o se dona.** Ningún objeto vive para siempre en el mercado (§9).

**Amplio pero ligero** (D-44, en [Decisiones](../00-vision/decisiones.md)). La capa simple es ver el resumen del combate y seguir: el filtro por defecto vende lo común y muestra lo importante. Tasar, filtros propios, piezas malditas, conjuntos y restaurar reliquias son capas opcionales para quien las quiera.

## 2. Qué puede caer: 20 categorías

"Libre" se comercia; "Ligado" no (ver [Equipamiento](equipamiento.md), §5).

| Categoría | Ejemplos | De dónde sale | Para qué sirve | Quién lo aprovecha | Comercio |
|---|---|---|---|---|---|
| ⚔️ **Equipo** | Armas, armaduras, joyas, herramientas de oficio | Monstruos y cofres (reserva del Mercado Negro), Tesoro Semanal | Usarlo, venderlo, desmontarlo | Todos; los artesanos lo desmontan | Libre; los únicos, ligados al equipar |
| 🪨 **Materiales del terreno** | Mineral, madera, hierbas, sal, cristal, especias | Recolección, encargos, expediciones, bolsas de humanoides | Refinado y fabricación | Fundición, Aserradero, Destilación y todos los oficios | Libre |
| 🦴 **Partes de monstruo** | Piel, colmillo, escamas, glándulas, cola rota | Despiece y partes rotas ([Daño y estados](../04-combate/dano-y-estados.md), §3) | Recetas temáticas | Curtiduría, Alquimia, Herrería, Cocina | Libre |
| 💠 **Artefactos de jefe** | Garra del Wyrm, Colmillo de Vidrio, Corazón del Coloso | Jefes (mayores); élites, Templados y únicos con nombre (menores) | Ingrediente de armas y armaduras únicas con técnica propia | Herrería, Peletería, Sastrería, Carpintería, Joyería | Libre |
| 📐 **Planos y recetas** | Plano de la Garra de las Dunas, receta de Elixir de Cuarzo | Jefes, jefes ocultos, cofres de oro, reputación | Aprender a fabricar; investigar y copiar el plano | Oficios mayores | Libre (las copias tienen 10 usos) |
| 🧩 **Fragmentos de recetas** | "Elixir de Cuarzo (2/5)" | Élites, cofres, pesca, arqueología | Con 5 iguales aprendes la receta (como las cartas de adivinación de *Path of Exile*) | Alquimia, Cocina, Inscripción | Libre |
| 💎 **Gemas de joyería** | Rubí en bruto, Ojo de Tormenta | Minería, cofres de plata, criaturas de cristal | Tallarlas y engarzarlas | Joyería | Libre. No confundir con las 💎 Gemas premium |
| 🔮 **Runas y esencias** | Runa de infusión, esencia de fuego, polvo arcano | Desencantar, élites Corruptos, cofres, jefes | Encantamiento de +1 a +4; también moneda de trueque | Encantamiento, Extracción de Esencias | Libre |
| 🧪 **Consumibles** | Pociones, vendas, aceites de caza, cebos, comida | Cofres, mochilas de humanoides, pesca | Usarlos | Todos | Libre |
| 🪙 **Oro** y ✨ **Esencia** | — | Oro: humanoides y contratos. Esencia: todo lo que se vence | Comerciar; mejorar equipo y maestrías | Todos | Oro libre; Esencia intransferible |
| 🗝️ **Llaves y mapas del tesoro** | Llave de cripta, mapa rasgado del piso 33, Llave del Piso | Campeones, cofres, pesca, humanoides | Abrir cofres sellados, desenterrar tesoros, Mítica+ | Cartógrafo (descifra mapas), explorador | Libre; las Llaves del Piso, ligadas |
| 🃏 **Cartas del Mazo de Bestias** | Carta del Necrófago, carta dorada de un jefe | Cualquier monstruo (poco), jefes (más) | Duelos de cartas en la taberna, colección ([Minijuegos](../08-social/minijuegos-y-formatos-telegram.md)) | Coleccionistas, tahúres | Libre |
| 🥚 **Mascotas y huevos de montura** | Huevo de wyrm, cría de lobo, mascota de duelo | Nidos, captura viva, jefes ocultos, pesca rara | Criar, domar, duelos de mascotas | Ganadería | Libre hasta que se doma |
| 🎨 **Apariencias y tintes** | Apariencia de Pesadilla, tinte Azul Abismo, pigmento de cristal | Jefes en dificultades altas, cofres, plantas y criaturas raras | Transfiguración y moda | Sastrería (tintes) | Apariencias ligadas a la cuenta; tintes libres |
| 🏺 **Piezas de arqueología** | Fragmento de vasija, sello antiguo | Excavaciones; el Anticuario del piso 64 | Completar objetos, colección, museo | Arqueología, Erudito | Libre |
| 📜 **Libros y pergaminos de lore** | *Diario del Primer Superviviente, tomo II* | Humanoides cultos, bibliotecas en ruinas, cofres | Leer (colección de Libros), pistas del Gran Misterio, idiomas antiguos | Erudito, Inscripción | Libre |
| 🔍 **Pistas de investigación** | Carta manchada, llave sin cerradura, muestra de sangre | Escenas de casos, humanoides, monstruos Enfermos (muestras) | Tablero de corcho, curas, jefes ocultos ([Investigaciones](../06-contenido/investigaciones.md)) | Detective, Médico, Erudito | Según el caso |
| ☠️ **Reliquias malditas** | Hacha del Hambriento, Anillo del Avaro | Criptas, cofres de zona negra, piezas sin tasar | Poder con precio (§4.5) | Quien acepte el riesgo; sacerdotes | Libre; contrabando donde la ciudad lo prohíbe |
| 🏛️ **Curiosidades para el museo** | Fósil de cristal, moneda de un reino perdido, imitación antigua | Arqueología, pesca, apariciones en el chat, piezas falsas al tasar | Donar al museo, decorar la casa | Museo, coleccionistas | Libre |
| 🏆 **Trofeos** | Cabeza de alfa, asta de ceniza, colmillo de Guardián | Cacerías (tres estrellas), únicos con nombre, jefes | Sala de trofeos ([Casa propia](../09-construccion/casa-propia.md)), títulos | Coleccionistas | Libre; los únicos del servidor, ligados |

## 3. Tablas de botín

### 3.1 Cómo se arma una tirada

Cada fuente tiene una **tabla con capas**, como las de WoW. El bot tira cada capa por separado.

| Capa | Qué trae | Cómo se decide |
|---|---|---|
| **Garantizada** | Esencia, despiece, pago del contrato | Siempre |
| **Probable** | Materiales, oro, consumibles | Lo normal es que salga |
| **Rara** | Equipo de rareza alta, artefactos menores, gemas, runas | Probabilidad baja |
| **Muy rara** | Cartas, curiosidades, piezas sin tasar, reliquias dañadas, huevos | Probabilidad muy baja |
| **Personal** | Lo que protege la Constancia (§7.3), materiales de conocimiento ★★★★ | Depende de tu historial, no del grupo |

**Lo nuevo pesa más.** Si en la capa muy rara cae una carta, una curiosidad o una apariencia, hay un 70 % de probabilidad de que sea una que **todavía no tienes**. Completar colecciones siempre avanza.

### 3.2 Monstruos y jefes

Probabilidades orientativas para zona amarilla y dificultad base. Las cambia el §3.5.

| Fuente | Garantizado | Probable | Raro | Muy raro | Límite |
|---|---|---|---|---|---|
| 🐺 **Monstruo común** | Esencia; despiece si alguien sabe Desuello | Material del terreno (40 %); oro y papeles si es humanoide (60 %) | Equipo Común a Raro (8 %); consumible (5 %) | Carta (1 %); pieza sin tasar (0,5 %); curiosidad (0,5 %) | — |
| ⭐ **Élite** | Esencia ×2; despiece ×2 | Equipo hasta Épico (25 %) | Artefacto menor (2 %, con Constancia); gema o runa (10 %) | Fragmento de receta (2 %); carta rara (1 %) | — |
| 🔷 **Campeones** (grupo de 3 a 5) | Lo de cada uno, más una **bolsa de grupo** | Bolsa: equipo hasta Épico (50 %) | Bolsa: llave o mapa del tesoro (5 %) | Bolsa: pieza sin tasar de brillo intenso (2 %) | — |
| 🏷 **Único con nombre** ([Bestiario](../06-contenido/bestiario.md), §8) | Trofeo; material exclusivo | Equipo Épico (50 %) | Artefacto menor (15 %, con Constancia) | Huevo o cría (1 %, si es bestia) | 1 vez por semana y personaje |
| 🐗 **Jefe de campo** | Esencia ×5; materiales del tramo; partes rotas | Una pieza hasta Épico por personaje | Artefacto menor (20 %); plano (5 %) | Reliquia dañada (1 %); apariencia (2 %) | 1 vez por día y personaje |
| 🐉 **Guardián del piso** | Esencia ×10; partes rotas; **Recuerdo** y **Sello** la primera vez | **Cofre del grupo:** un artefacto del Guardián cada 5 jugadores, y equipo del tramo | Plano del Guardián (10 %); carta de jefe (5 %) | Apariencia del Guardián (2 %) | Semanal |
| 👁 **Jefe oculto** | Esencia ×10; título la primera vez | Artefacto propio del jefe (30 %, con Constancia) | Reliquia dañada (10 %); libro de lore (25 %) | Huevo de montura o mascota (2 %) | Semanal |
| 🧱 **Muro** (pisos 25, 50 y 75) | Lo del Guardián ×2; Recuerdo de Muro (eliges entre 3) | Dos artefactos cada 5 jugadores | Plano de **conjunto** (15 %) | Apariencia y título únicos en Pesadilla | Semanal |

**Los artefactos mayores solo los sueltan jefes**; los menores, también élites, Templados y únicos con nombre. Ninguno es un objeto terminado: es el ingrediente de un arma o armadura con técnica propia (ver [Equipamiento](equipamiento.md), §6).

### 3.3 Cofres

| Cofre | Dónde | Qué trae | Riesgo |
|---|---|---|---|
| 🪵 **De madera** | Campos 🟡 y tierras salvajes 🔴 | Consumibles, materiales, algo de oro | Ninguno |
| ⛓ **De hierro** | Tierras salvajes 🔴 y laberintos | Equipo hasta Raro, gemas en bruto | Puede tener trampa |
| 🥈 **De plata** | Tierras salvajes 🔴 y zonas negras ⚫ | Runas, esencias, gemas talladas, mapa del tesoro (5 %) | Trampa o mímico |
| 🥇 **De oro** | Solo 🔴 y ⚫, uno por piso y día | Equipo hasta Legendario, pieza sin tasar (30 %), fragmento de receta (10 %) | Otros jugadores también lo buscan |
| 🏰 **De mazmorra** | Tras cada jefe y al final | Equipo de temporada, Esencia, Llave del Piso | Ninguno |
| ⏱ **De reloj** (Mítica+) | Al terminar a tiempo | Una pieza más por cada nivel que sube la llave | Ninguno |
| 🗝 **Sellado** | Se abre con su llave o se desentierra con un mapa | Botín de cofre de oro y una curiosidad garantizada | Suele estar en 🔴 o ⚫ |
| 🪤 **Trampa** | Cualquier cofre de hierro o mejor | **Trampa:** aguja envenenada, gas, explosivo o alarma que llama a una patrulla. **Mímico:** un monstruo ([Bestiario](../06-contenido/bestiario.md), §2.2) | Siempre hay una pista en el texto |

**Una trampa siempre avisa.** "*La cerradura brilla con grasa nueva.*" Ante un cofre sospechoso puedes:
- **examinar:** con Ingeniería o siendo Pícaro, ves qué trampa es;
- **desarmar:** con una ganzúa (Herrería); si fallas, salta;
- **abrir de lejos** con una vara (Carpintería): la trampa salta sin herirte, pero un explosivo destruye parte del contenido;
- **dejarlo.**

El mímico guarda lo que se tragó: si lo vences, deja botín de cofre de plata.

### 3.4 Actividades

| Actividad | Garantizado | Probable | Raro | Muy raro |
|---|---|---|---|---|
| 🐾 **Cacería** ([Cacerías](../06-contenido/cacerias.md)) | Piezas de una a tres estrellas; pago del contrato | Material de cada parte rota | Trofeo de alfa; carta de la presa | Trofeo de bestia legendaria |
| 🪢 **Captura viva** | La presa viva (doma, cría, venta, el Foso) | Tabla propia: sangre, pelo y plumas sin dañar | Huevo del nido | — |
| 🧭 **Expedición** ([Misiones](../06-contenido/misiones-y-exploracion.md), §3) | Solo lo que traes de vuelta | Materiales de zona, vetas | Cofres del camino; mercader errante con ofertas raras | Mapa del tesoro; reliquia dañada (en ⚫) |
| 🎣 **Pesca** | Pescado | Algas, sal, perlas, conchas | Botella con mensaje (pista o mapa); cofre hundido (sin tasar) | Huevo de criatura acuática; reliquia dañada |
| 🏺 **Arqueología** | Fragmentos | Pieza común completa | Pieza rara (monturas de hueso, juguetes antiguos) | Reliquia dañada; pieza del Gran Misterio |
| 📯 **Jefe errante** ([Jefes](../06-contenido/jefes.md)) | **Una caja por participante** que hizo al menos una acción útil | Consumibles, Esencia, cartas comunes | Tintes y apariencias del jefe errante | Carta dorada del jefe errante |
| 🌍 **Jefe semanal de servidor** | Según la contribución | Materiales del tramo | Artefacto (con Constancia) | Título de temporada para el gremio que más aportó |

**Las cajas del jefe errante** se abren en el chat, a la vista: cada participante toca la suya y el resultado se edita en el mismo mensaje. Quien no hizo nada no recibe caja, así el chat no se llena de mirones.

### 3.5 Qué cambia la tabla

| Factor | Qué cambia | Ejemplo |
|---|---|---|
| **Tramo** | El tier de todo lo que cae (T1 a T10). Nunca cae algo de un tramo superior | Un lobo del piso 12 suelta pieles T2 |
| **Dificultad** | Cada escalón (Normal → Profundidades → Corrompido → Abismal → Pesadilla; en mazmorras, Heroica, Mítica y cada nivel de Mítica+) sube un 20 % la probabilidad de rareza y abre una rareza más | Legendario solo desde Abismal o Mítica, o en zonas 🔴 y ⚫ |
| **Color de zona** | 🔵 no hay combate · 🟡 ×1 · 🔴 ×1,5 a la rareza y mejor calidad de material · ⚫ ×2 y **materiales que solo existen ahí** | El mismo élite da más en ⚫, pero ahí puedes perderlo todo ([Secuelas y muerte](../05-salud/secuelas-y-muerte.md)) |
| **Modificadores del monstruo** | Los del [Bestiario](../06-contenido/bestiario.md), §7: Élite, Templado, Enfermo (muestras), Blindado… | Un Blindado da más escamas |
| **Partes rotas** | Cada parte rota da **su** material; la piel sale peor | Romper la cola del Wyrm da Escama de cola |
| **Cómo terminó** | Matar: tabla completa. Capturar: tabla de captura. Perdonar: la mitad. Huyó: nada | Ver [Mecánicas avanzadas](../04-combate/mecanicas-avanzadas.md), §9 (moral) |
| **Conocimiento** | ★★★★ abre materiales raros que otros no ven; ★★★★★ muestra la tabla completa en `/bestiario` | La glándula pura solo la saca un Experto |
| **Desuello en el grupo** | Sin desollador, solo "restos" de una estrella | Llevar uno vale la pena |
| **Ecología** | Una especie abundante suelta más; una escasa, menos | Ver [Bestiario](../06-contenido/bestiario.md), §10 |
| **Aceleradores** | Solo suben la cantidad de **recursos** (materiales, partes). Nunca equipo, artefactos, Recuerdos, cofres de jefe ni rareza | [Monetización](../07-economia/monetizacion.md), §3 |

**Tope.** Sumando todo, la probabilidad de una rareza nunca pasa del triple de la base. Nadie rompe una tabla apilando bonos.

## 4. Rareza y afijos

### 4.1 Rareza

| Rareza | Icono | Líneas de afijo | Vale en Poder de Objeto como la calidad… | En el equipo de botín (🟡, base) |
|---|---|---|---|---|
| Común | ⚪ | 0 | Normal | 60 % |
| Poco común | 🟢 | 1 | Buena | 28 % |
| Raro | 🔵 | 2 | Notable | 9,8 % |
| Épico | 🟣 | 3 | Excelente | 2 % |
| Legendario | 🟠 | 4 | Obra Maestra | 0,2 % (desde Abismal, Mítica, 🔴 o ⚫) |
| Reliquia | 🟡 | Efecto propio y 2 afijos fijos | Obra Maestra | Nunca cae terminada (§5) |

**Rareza y Calidad valen lo mismo.** Un Épico de botín vale como un Excelente fabricado, y un Legendario como una Obra Maestra. El cazador de botín y el artesano llegan al mismo techo.

**De dónde salen las piezas.** El Mercado Negro compra piezas **Normales y Buenas**, las que se hacen en cantidad con la fabricación rápida ([Fabricación](../07-economia/fabricacion.md), §1). Cuando una de esas piezas cae, el botín la **despierta**: recibe una rareza y sus afijos, y conserva la firma del artesano. La rareza reemplaza a la calidad como bono.

```
🔵 Hacha Dentada de la Roca   [PO 238]
T3 · Raro · +0 · Mejoras 0/3
Forjada por Tor el Fundidor ✒️ · despertada en el piso 23
+22 Fuerza
Dentada: +10 % de acumulación de 🩸 Sangrado
de la Roca: tu ⚓ Firmeza se llena un 15 % más rápido
Técnica: Hendidura
Durabilidad 88/88 · 3,4 kg · Libre
```

### 4.2 Prefijos y sufijos

Un objeto de botín se nombra **tipo + prefijo + sufijo**: "Hacha **Dentada** **de la Roca**".
- **Prefijos** (un adjetivo, que concuerda con el objeto): ofensivos.
- **Sufijos** ("de…"): defensa y utilidad.
- Como mucho, **2 prefijos y 2 sufijos**. Si hay dos, el nombre muestra el más fuerte.
- Cada afijo sale con un valor dentro de su rango por tramo. Los números son chicos a propósito ([Balance](balance.md), §4).

**Prefijos**

| Prefijo | Qué da | T1 | T5 | T10 |
|---|---|---|---|---|
| **Certero** | Crítico | +1 % | +2 % | +3 % |
| **Presto** | Celeridad (iniciativa) | +1 % | +2 % | +3 % |
| **Diestro** | Maestría | +1 % | +2 % | +3 % |
| **Versátil** | Versatilidad | +1 % | +2 % | +3 % |
| **Ígneo** | Daño de fuego por golpe, que llena 🔥 Quemadura | +3 | +8 | +14 |
| **Gélido** | Daño de escarcha por golpe, que llena ❄️ Congelación | +3 | +8 | +14 |
| **Ponzoñoso** | Daño de naturaleza por golpe, que llena 🟢 Veneno | +3 | +8 | +14 |
| **Bendito** | Daño sagrado por golpe | +3 | +8 | +14 |
| **Dentado** | Acumulación de 🩸 Sangrado | +5 % | +10 % | +15 % |
| **Quebrantador** | Daño a la 🟫 Postura | +4 % | +8 % | +12 % |
| **Sediento** | Robo de vida | +1 % | +2 % | +3 % |
| **Provocador** | Amenaza generada | +10 % | +15 % | +20 % |

**Sufijos**

| Sufijo | Qué da | T1 | T5 | T10 |
|---|---|---|---|---|
| **del Oso** | ❤️ Vida | +10 | +40 | +80 |
| **del Muro** | Armadura | +3 | +10 | +20 |
| **de la Salamandra** | Resistencia al fuego | +5 % | +8 % | +10 % |
| **del Invierno** | Resistencia a la escarcha | +5 % | +8 % | +10 % |
| **de la Víbora** | Acumulación de 🟢 Veneno recibida | −10 % | −15 % | −20 % |
| **de la Calma** | Estrés recibido ([Mente](../05-salud/mente.md)) | −5 % | −8 % | −10 % |
| **de la Roca** | La ⚓ Firmeza se llena más rápido | +10 % | +15 % | +20 % |
| **del Zorro** | La primera esquiva de cada combate cuesta 1 🔋 Aguante menos | Fijo | Fijo | Fijo |
| **del Sanador** | Curación recibida | +2 % | +3 % | +4 % |
| **del Viajero** | Peso del objeto | −5 % | −8 % | −10 % |
| **del Herrero** | Durabilidad máxima | +5 | +8 | +10 |
| **de la Liebre** | Probabilidad de huir | +10 % | +15 % | +20 % |

### 4.3 Afijos de zona del cuerpo

Solo salen en la armadura que protege esa zona (ver [Heridas](../05-salud/heridas.md), §1). Cuentan como sufijo. Convierten cada ranura en una decisión de salud, no solo de defensa.

| Zona · ranura | Afijo | Efecto |
|---|---|---|
| Cabeza · casco | **del Yelmo Firme** | −20 % de probabilidad de conmoción |
| Cabeza · casco | **del Ojo Abierto** | La ceguera te dura una ronda menos |
| Torso · pecho, hombros | **de la Coraza Viva** | Una vez por combate, la primera herida grave en el torso baja a moderada |
| Abdomen · cintura | **de las Entrañas de Hierro** | Las heridas de abdomen no aceleran el Sustento; −25 % de riesgo de infección |
| Brazos · muñecas, manos | **del Puño Cerrado** | No te pueden desarmar. Con un brazo fracturado puedes usar armas a dos manos, con −20 % de daño |
| Piernas · piernas, pies | **del Ciervo** | Las heridas leves y moderadas de pierna no bajan tu iniciativa |
| Espalda · capa | **del Nómada** | +1 de abrigo o de frescor ([Peligros del entorno](../05-salud/peligros-del-entorno.md)) |

### 4.4 Afijos de oficio

Solo salen en **herramientas** y **ropa de oficio** ([Profesiones](../07-economia/profesiones.md), §7). No tocan el combate. Son el "equipo de final de juego" del artesano: un recolector o un herrero también caza botín.

| Herramienta | Afijo | Efecto |
|---|---|---|
| Pico (Minería) | **Paciente** | +5 % de gemas en bruto por veta |
| Pico (Minería) | **del Topo** | Ves la Pureza de una veta sin prospectar |
| Hoz (Herboristería) | **Nocturna** | Recolectas hierbas de noche sin farol |
| Cuchillo de desuello | **Limpio** | +10 % de probabilidad de pieza de tres estrellas |
| Martillo (Herrería) | **del Templado** | +20 Puntos de Artesanía en el minijuego |
| Alambique (Alquimia) | **Generoso** | 8 % de probabilidad de una poción extra |
| Bisturí (Medicina) | **Firme** | El paciente se recupera un 10 % más rápido tras una cirugía |
| Caña (Pesca) | **de la Marea** | +5 % de tesoros al pescar |
| Pala (Arqueología) | **de la Erudita** | 10 % de probabilidad de un fragmento extra |
| Cualquiera | **del Enfoque** | −5 % de Enfoque gastado |
| Cualquiera | **del Maestro** | +5 % de maestría por objeto ganada |

```
🟢 Pico Paciente
T4 · Poco común · Herramienta de Minería
Forjado por Hilda ✒️ · despertado en el piso 36
Paciente: +5 % de gemas en bruto por veta
Durabilidad 60/60 · 2,8 kg · Libre
```

### 4.5 Afijos malditos: poder con precio

**De dónde sale.** El arma maldita de *NetHack*, los objetos corrompidos de *Path of Exile* y los objetos malditos del [Catálogo ampliado](../00-vision/catalogo-ampliado.md).

Una línea maldita reemplaza a una línea normal. Da **más** que un afijo normal (alrededor de una vez y media en el simulador) y cobra un **precio**.

| Afijo maldito | Poder | Precio |
|---|---|---|
| **del Hambriento** | +6 % de daño | El Sustento baja al doble |
| **del Avaro** | +15 % de oro de botín | Mientras lo llevas no puedes regalar, prestar ni comerciar nada |
| **del Insomne** | +1 🔋 Aguante máximo | El descanso baja el estrés la mitad |
| **del Sangrador** | +4 % de robo de vida | Las curas de otros te curan un 15 % menos |
| **de la Fiebre** | +4 % de Celeridad | Tu Inmunidad sube un 25 % más lento ([Enfermedades](../05-salud/enfermedades.md)) |
| **del Eco Hueco** | Tus críticos se repiten al 30 % la ronda siguiente | Los críticos que recibes, también |
| **del Paria** | +10 % de daño cuando juegas solo | Los PNJ de los asentamientos te cobran un 10 % más |
| **del Vacío** | +8 % de daño de sombra | +3 de estrés por ronda en combate |

**Reglas:**
- **No se ve sin tasar** (§6). Lo revela un tasador de rango Experto o un sacerdote.
- **Si te la pones, no te la quitas** sin un ritual del templo ([Curación](../05-salud/curacion-y-tratamientos.md)). Hay dos:
  - **Soltar:** barato. Te la quitas, y la pieza sigue maldita.
  - **Purificar:** caro (porcentaje del valor, más reactivos). La línea maldita pasa a ser una línea normal al azar.
- **Una línea maldita por pieza** y **dos piezas malditas puestas** como mucho.
- **No acepta Mejoras nuevas**, como los objetos corrompidos de *Path of Exile*.
- Un herrero también puede maldecir una pieza **a propósito** con un *Baño de Vacío* ([Catálogo ampliado](../00-vision/catalogo-ampliado.md)).
- Donde el consejo de la ciudad las prohíbe, son **contrabando** ([Crimen y justicia](../06-contenido/crimen-y-justicia.md)).

```
☠️ Hacha del Hambriento   [PO 318]
T4 · Épico · MALDITA · tasada por Vael ✒️
+30 Fuerza
Certera: +2 % de crítico
Quebrantadora: +6 % de daño a la Postura
del Hambriento: +6 % de daño · 🍖 el Sustento baja al doble
⚠️ Si te la pones, no te la quitas sin un ritual del templo
```

### 4.6 La variedad se multiplica: el material deja huella

**De dónde sale.** En *Borderlands* cada fabricante de armas tiene su estilo. Aquí el estilo lo da el **material**, que viene de la geografía ([Geografía y recursos](../02-mundo/geografia-y-recursos.md)).

| Material | De dónde | Qué le da al arma | Precio |
|---|---|---|---|
| **Hierro Negro** | Yacimiento único del piso 14 | +daño a la Postura | +15 % de peso |
| **Cristal de cueva** | Tramo III, Cueva de Cristal | +Crítico | −20 % de durabilidad máxima |
| **Acero Estelar** | Mineral estelar del tramo V | Equilibrado | Caro: sin precio en combate |
| **Obsidiana** | Tierras volcánicas, tramo VIII | +acumulación de Sangrado | Cada reparación baja más la máxima |
| **Roble Cantor** | Yacimiento único del piso 3 | Bastones y laúdes: +Celeridad | El fuego enemigo le quita durabilidad |
| **Hueso de bestia** | Tundra | −20 % de peso | −5 % de daño base |

**La cuenta.** Unos 20 tipos de arma, cada uno con su técnica, por 10 tramos, varios materiales, 24 afijos y 6 rarezas. Salen **millones** de combinaciones antes de contar encantamientos, gemas y únicos. Dos hachas T3 casi nunca son iguales.

## 5. Únicos con historia y conjuntos

### 5.1 Reglas de los únicos

**De dónde sale.** Los únicos de *Diablo* y *Path of Exile*, con su texto de historia, y las descripciones de *Dark Souls*.

- **Nunca caen terminados.** Salen por tres caminos, y los tres pasan por un artesano:

  | Camino | Qué cae | Quién lo termina |
  |---|---|---|
  | **Artefacto** | Un artefacto de jefe o de único con nombre | Un artesano con el rango del tramo |
  | **Reliquia dañada** | Un objeto antiguo roto y sin tasar (arqueología, pesca, cofres sellados, jefes ocultos) | Un erudito lo identifica (§6) y un artesano lo restaura con materiales del tramo |
  | **Recuerdo** | El Recuerdo de un Guardián (§7.5) | El Castillo, o un artesano |

- **Nombre, historia y un efecto propio** que cambia cómo se juega, más 2 afijos fijos.
- **Presupuesto parejo.** El efecto vale lo mismo que 2 afijos en el simulador ([Balance](balance.md), §3), y ningún único mueve un eje de la spec más de 3 puntos. Casi todos tienen un **precio**.
- **Cada tramo tiene únicos para todos los roles y los cuatro tipos de armadura.** Ninguna spec se queda sin opciones.
- **Dos puestos a la vez**, como máximo.
- **Ligado al equipar.** Hasta que alguien se lo pone, se comercia.
- **En la arena clasificada** su efecto cuenta con peso limitado, como los afijos ([PvP](../06-contenido/pvp.md), §5).
- **Se gastan como todo.** Al romperse no desaparecen: quedan como **Reliquia rota**, para el museo o la sala de trofeos, o para que un Gran Maestro la reforje con un artefacto nuevo del mismo origen.
- **Tienen historial y número de serie** (§9).

### 5.2 Doce únicos

**1. Arco de Colmillo Viejo** · T1 · Arco largo · Artefacto de Colmillo Viejo (piso 4) → Carpintería
> *"Colmillo Viejo sobrevivió a cuarenta cazadores. El arco que hicieron con su colmillo todavía tira hacia la presa que huye."*
- **Efecto:** apuntar a las piernas no tiene penalización de precisión.
- **Precio:** no puedes apuntar a la cabeza.
- **Cambia el juego:** eres quien no deja huir y quien atrasa al enemigo en la cola de iniciativa.

**2. Caña de la Primera Lluvia** · T1 · Herramienta de Pesca · Reliquia dañada, pescada en el lago del piso 6 → Carpintería
> *"Alguien pescaba en el Claro antes de que existiera el Claro. La caña sigue mojada, aunque no llueva."*
- **Efecto:** con lluvia, 1 de cada 10 capturas es un cofre hundido del piso (sin tasar).
- **Precio:** con lluvia no sacas peces de tres estrellas.
- **Cambia el juego:** el pescador sale justo cuando nadie más sale.

**3. Rompecercas** · T2 · Maza a dos manos · Artefacto de Rompecercas (piso 13) → Herrería
> *"Arrasó tres cosechas y once cercas. Dicen que la maza todavía huele a trigo pisado."*
- **Efecto:** cada golpe a las piernas de un enemigo Grande o Enorme le baja también la Postura, como un golpe pesado.
- **Precio:** −1 🔋 Aguante máximo.
- **Cambia el juego:** sin ser tanque, abres la ventana de golpes críticos para todo el grupo.

**4. Diapasón del Cantor** · T3 · Abalorio · Artefacto del Cantor de Cuarzo (piso 22) → Joyería
> *"El gólem cantaba solo cuando nadie minaba. Si acercas el diapasón al oído, se oye una galería vacía."*
- **Efecto:** una vez por combate, repites al 50 % la acción del aliado que actuó justo antes que tú en la cola.
- **Precio:** usarlo es tu jugada de esa ronda y cuesta 1 🔋 Aguante.
- **Cambia el juego:** premia mirar la cola de iniciativa ([Ronda y acciones](../04-combate/ronda-y-acciones.md), §6) y combinar con el grupo.

**5. Remo del Barquero** · T4 · Bastón · Artefacto del Barquero Ahogado (piso 38) → Carpintería
> *"Cobraba un objeto por cruzar. A los que no podían pagar, los cruzaba igual. Nunca dijo hacia qué orilla."*
- **Efecto:** levantas a un aliado derribado **desde cualquier fila** y cambias de lugar con él: él pasa a tu fila y tú a la suya.
- **Precio:** te llevas la herida que le tocaba por caer.
- **Cambia el juego:** el que salva a otros con su propio cuerpo. El médico del grupo tendrá trabajo.

**6. Amuleto del Sediento** · T5 · Cuello · Reliquia dañada de un cofre sellado de la tumba del piso 46 (puede salir maldita) → Joyería
> *"Lo enterraron con el rey para que nunca le faltara agua. El rey se levantó igual, a buscarla."*
- **Efecto:** cada vez que muere un enemigo en combate contigo, recuperas 1 🔋 Aguante.
- **Precio:** tu Hidratación baja el doble ([Condiciones](../05-salud/condiciones.md)).
- **Cambia el juego:** contra grupos esquivas mucho más, pero dependes del agua.

**7. Garra de las Dunas** · T5 · Arma de una mano · **Recuerdo** del Guardián del Piso 45 ([Jefes](../06-contenido/jefes.md), §4)
> *"El Wyrm no tenía nido. Dormía bajo la arena que él mismo había vuelto vidrio."*
- **Efecto:** técnica propia, *Barrido de Dunas*: arena que ciega a la vanguardia enemiga 2 rondas (−30 % de precisión).
- **Precio:** reemplaza la técnica del arma, y la ronda siguiente tu fila no puede apuntar a partes (la arena tapa todo).
- **Cambia el juego:** control defensivo para cualquier spec de vanguardia.

**8. Velo de la Novia** · T6 · Capa · Artefacto de la Novia del Paso (piso 53) → Sastrería
> *"Esperó en el paso cuarenta inviernos. El velo aprendió a esperar con ella."*
- **Efecto:** si usas una respuesta y el golpe no llega, no pierdes el Aguante: lo recuperas la ronda siguiente. +2 de abrigo.
- **Precio:** mientras lo llevas, solo puedes usar respuestas de esquivar y 🌀 Esquivar; nunca bloquear, desviar ni interrumpir.
- **Cambia el juego:** perdona leer mal un aviso, pero te quita las reacciones que ayudan al grupo.

**9. Corona Rota del Rey sin Corona** · T7 · Cabeza · Reliquia dañada (corona rota del Rey sin Corona, piso 68) → Arqueología la identifica, Joyería la restaura
> *"Perdió el reino, el nombre y la cabeza. La corona perdió solo una punta, y todavía no lo perdona."*
- **Efecto:** marcas a un enemigo para un **duelo de honor**. Mientras nadie más lo ataque, tú y él se hacen un 20 % más de daño.
- **Precio:** si un aliado lo ataca, el duelo se rompe y haces un 10 % menos de daño durante 2 rondas.
- **Cambia el juego:** en grupo, alguien se ocupa aparte de un invocado o de un adepto; solo, peleas cortas y arriesgadas.

**10. Manto de Brasaviva** · T8 · Pecho de tela · Artefacto de Brasaviva (piso 73) → Sastrería
> *"Renació tres veces. A la cuarta, alguien guardó una pluma antes de que el fuego terminara."*
- **Efecto:** la primera vez por combate que quedas derribado, al final de la ronda renaces con el 20 % de vida, en llamas.
- **Precio:** mientras ardes pierdes un 3 % de vida por ronda, hasta que un aliado gaste su ronda (🎒 Mochila) en apagar tus cenizas. En esa pelea no te pueden levantar con resurrección en combate.
- **Cambia el juego:** una segunda oportunidad que obliga al grupo a cuidarte.

**11. Cristalino del Pozo** · T9 · Abalorio · Artefacto del Ojo del Pozo (piso 89) → Joyería
> *"El Ojo miraba hacia abajo. Nadie se atrevió a preguntar qué veía en el fondo."*
- **Efecto:** ves también la **segunda** acción de cada enemigo en la cola, y la Locura no distorsiona sus avisos para ti.
- **Precio:** +2 de estrés por cada ronda de combate.
- **Cambia el juego:** guías al grupo en el Abismo Umbrío, y el bardo y el templo trabajan para ti.

**12. Rama de la Dríade Sin Nombre** · T10 · Bastón · Artefacto del jefe oculto del piso 99 → Carpintería
> *"No tenía nombre porque nadie la había visto. Cuando la vieron, ya no quedaba nadie para ponérselo."*
- **Efecto:** como tu jugada de la ronda, pasas a tu barra la mitad de un estado acumulado de un aliado (Sangrado, Veneno, Podredumbre…).
- **Precio:** mientras la llevas no puedes beber pociones.
- **Cambia el juego:** un tanque o un sanador que absorbe estados en lugar de curarlos.

### 5.3 Conjuntos

**De dónde sale.** Los conjuntos de *Diablo II* y los de banda de WoW.

- **Cuatro piezas** por conjunto, con un bono a las 2 y otro a las 4.
- **Cada pieza tiene un afijo menos.** El bono paga esa diferencia: el presupuesto queda parejo.
- **Se fabrican** con un **plano de conjunto** (Muros, bandas, reputación) y artefactos del tramo. Cada pieza la puede hacer un artesano distinto.
- **Abiertos a cualquier spec** que use ese tipo de armadura. El bono premia una mecánica común (leer avisos, emboscar, bloquear), no una spec concreta.
- Puedes llevar **dos bonos de 2 piezas** de conjuntos distintos, o **uno de 4**.

| Conjunto | Tipo · tramo | Origen | 2 piezas | 4 piezas |
|---|---|---|---|---|
| **Atuendo del Cartógrafo Perdido** | Tela · T3 | Plano del Primer Muro (piso 25) | Los avisos enemigos te llegan con una pista más, como si tu conocimiento tuviera una ★ más | Cuando una respuesta tuya acierta, tu siguiente habilidad cuesta un 30 % menos de recurso |
| **Pieles del Rastro** | Cuero · T2 | Plano de la Orden de Cazadores (rango Batidor) y artefactos menores de alfas | +10 % de piezas de tres estrellas al despiezar | Tu primera acción contra un enemigo que no te vio es crítica y lo **marca**: tu grupo ve su próxima acción |
| **Baluarte del Primer Muro** | Placas · T3 | Plano del Primer Muro (piso 25) | La ⚓ Firmeza se llena un 15 % más rápido | Cuando bloqueas un golpe avisado, tu fila entera recibe un 20 % menos de ese golpe |
| **Ajuar del Minero Viejo** | Ropa de oficio y pico · T4 | Plano de Herrería de herramientas (rango Experto) | Inmune a la Tos del Minero | Una vez por día "presientes" una veta: el mapa marca la mejor veta del piso durante 1 hora |

## 6. Objetos sin identificar

**De dónde sale.** El pergamino de identificar de *Diablo* y el de sabiduría de *Path of Exile*; Deckard Cain, que identificaba en *Diablo II*; y el arma maldita de *NetHack*, que nadie sabía que lo era hasta empuñarla.

### 6.1 Qué cae sin tasar

- **Una de cada tres** piezas Raras o mejores de zonas 🔴 y ⚫.
- Lo de brillo intenso de los cofres de oro y sellados, los cofres hundidos y **todas las reliquias dañadas**.
- **Nunca** lo común: no vale la pena tasarlo.
- **Hasta el nivel 10**, nada cae sin tasar.

Sin tasar ves el tipo, la ranura, el tramo, el peso y un **brillo**:

| Brillo | Qué puede ser |
|---|---|
| ✧ **Tenue** | Poco común o Raro |
| ✦ **Intenso** | Épico o Legendario |
| ✸ **Extraño** | Reliquia dañada, maldita o falsa. No se sabe hasta tasar |

### 6.2 Cómo se tasa

| Método | Quién | Qué revela | Costo | Límite |
|---|---|---|---|---|
| 📜 **Pergamino de Tasación** | Lo fabrica Inscripción | Rareza y afijos | El pergamino | No ve maldiciones ni historia |
| 🔮 **Tasador encantador** | Un jugador con Encantamiento | Rareza y afijos; la **maldición** desde rango Experto | Lo que cobre, por debajo del techo del PNJ | Con poco rango ve solo algunas líneas |
| 📖 **Tasador erudito** | Un jugador con Inscripción | La **historia** y el origen; si es una reliquia, qué hace falta para restaurarla; la maldición desde Experto | Lo que cobre | No ve los números de los afijos |
| 🕯 **Sacerdote** | El templo | Solo si está maldita | Donación | Nada más |
| 🏛 **Tasador del Castillo** | PNJ | Todo | Un porcentaje alto del valor; tarda 1 hora | Pone el techo de precio a los jugadores |
| 🎲 **Ponértela sin tasar** | Tú | Todo, después del primer combate | Gratis | Si está maldita, ya no te la quitas |

### 6.3 El Tasador: un rol nuevo

- Nace de dos oficios, **Encantamiento** o **Inscripción**, y vive en un puesto del mercado o en el ala de Oficios.
- **Maestría de tasación:** sube tasando objetos **distintos**, no el mismo cien veces. Con más maestría ves más líneas, detectas antes las maldiciones y notas los afijos dormidos (§6.4).
- **Certificado firmado.** Cada tasación deja un certificado reenviable ("tasado por Vael ✒️"). Un objeto con certificado se vende mejor.
- **Falsificar un certificado** es delito de falsificación ([Crimen y justicia](../06-contenido/crimen-y-justicia.md)): un detective lo puede rastrear.

### 6.4 Riesgo y sorpresa

| Al tasar una pieza de brillo intenso sale… | Probabilidad | Qué pasa |
|---|---|---|
| **Lo esperado** | 78 % | Una pieza normal de su rareza |
| **Afijo dormido** | 8 % | Sube una rareza. Solo lo despierta un tasador con maestría alta o el PNJ; si lo tasa uno de rango bajo, sigue dormido para el próximo |
| **Maldita** | 8 % | Trae una línea maldita (§4.5). Hay quien la busca a propósito |
| **Imitación** | 5 % | No sirve para pelear, pero es una **curiosidad** para el museo |
| **Reliquia dañada** | 1 % | El comienzo de un único (§5) |

- **Se puede vender sin tasar.** Comprar a ciegas es especular. Las bandas de precio por tramo y brillo ([Economía](../07-economia/economia.md), §3) impiden estafas y lavado de oro.
- **Llevarla sin tasar a una zona negra** es arriesgado: si caes, otro se queda con la sorpresa.

### 6.5 Cómo se ve

```
❓ Yelmo desconocido   T3 · Cabeza · 2,1 kg
✦ Brillo intenso · Cofre de oro, piso 27 (🔴)

[📜 Usar pergamino (1)]   [🔮 Buscar tasador]
[🏛 Tasador del Castillo] [🎲 Ponérmelo así]
[🏷 Vender sin tasar]     [↩ Volver]
```

Después de la tasación, el mismo mensaje pasa a:

```
🔮 Tasación de Vael (Encantamiento · Experto) ✒️
❓ Yelmo desconocido → 🟣 Yelmo Certero del Ojo Abierto
T3 · Épico · [PO 251]
+20 Intelecto
Certero: +2 % de crítico
Presto: +1 % de celeridad
del Ojo Abierto: la ceguera te dura 1 ronda menos
✨ ¡Afijo dormido! Era Raro y despertó a Épico.
No está maldito.

[📤 Reenviar certificado] [🎒 Guardar] [⚔️ Equipar]
```

## 7. Reparto, mala racha y recompensas seguras

### 7.1 Lo personal y el cofre del grupo

Todo botín de grupo tiene dos partes:
- **Personal, siempre:** Esencia, despiece, el material de **cada parte rota por el grupo** (como en *Monster Hunter*, todos lo reciben), Recuerdo, Sello, lo nuevo para tus colecciones y tu tirada de Constancia.
- **Cofre del grupo:** el equipo comerciable y los artefactos de jefe. Se reparte según el modo del grupo:

| Modo | Para quién | Cómo funciona |
|---|---|---|
| **Personal** | Por defecto en grupos de amigos y de gremio | El cofre tira por cada uno: con un artefacto cada 5 jugadores, cada uno tiene un 20 %. Lo que te toca, te toca, y tienes **2 horas** para regalarlo a alguien que estuvo |
| **Necesidad / Codicia** | Por defecto en grupos armados por el buscador | §7.2 |
| **Maestro de botín** | Grupos de gremio | El líder asigna. Cada asignación queda en el tema #banda del gremio |
| **Puntos de banda** | Gremios de banda | Los DKP de *EverQuest*: el bot suma puntos por asistir y los objetos se "compran" con puntos |
| **Subasta del gremio** | Gremios | Se puja en oro. El oro se reparte entre los presentes y el bot quema un porcentaje (sumidero) |

En los grupos armados al azar no existe el maestro de botín: nadie se puede quedar con todo.

### 7.2 Necesidad o Codicia, con el dado nativo

Ver [Gremios y social](../08-social/gremios-y-social.md), §4.

- Cada uno elige en 60 segundos:
  - 🙋 **Necesidad:** lo vas a usar. Solo si tu clase domina ese tipo de armadura, si es una herramienta de tu oficio o si es un artefacto para un arma que puedes usar.
  - 💰 **Codicia:** lo quieres para vender o desmontar.
  - 🚫 **Paso.** Si no eliges, pasas.
- Entre los empatados en la categoría más alta, el bot tira un 🎲 nativo por cada uno **en el chat de la sala**. El valor lo decide el servidor de Telegram y todos lo ven. Gana el más alto; si hay empate, vuelven a tirar solo los empatados.
- **Ganar con Necesidad liga el objeto.** Un artefacto ligado solo lo puede fabricar un artesano por pedido de fabricación para ti ([Economía](../07-economia/economia.md), §7). Así nadie pide Necesidad para revender.
- **Perder con Necesidad suma Constancia** para ese objeto (§7.3).

### 7.3 Constancia: la protección contra mala racha, a la vista

WoW esconde su protección contra mala racha. Aquí se ve, y tiene nombre: **Constancia** 🍀.

- Cada intento sin el objeto protegido sube su probabilidad. Al conseguirlo, vuelve a cero.
- Es **por personaje y por objeto**.
- Se muestra en el resumen: "🍀 Constancia (Colmillo de Vidrio): 4 intentos, +32 %".
- **No se compra, no se transfiere y no la tocan los aceleradores.**

| Qué protege | Base | Sube por intento | Seguro como mucho al intento |
|---|---|---|---|
| Un artefacto concreto de un jefe | 20 % | +8 % | 11 |
| Un artefacto menor de élites y únicos | 2 % | +2 % | 50 |
| Un plano de Guardián | 10 % | +5 % | 19 |
| Una pieza Legendaria (🔴, ⚫, Abismal o más) | 0,2 % | — | Tras 25 piezas Épicas seguidas sin ningún Legendario, la siguiente es Legendaria (unas 2,5 veces lo esperado: protege de la mala racha sin inflar los Legendarios) |
| Una carta, curiosidad o apariencia nueva | — | — | "Lo nuevo pesa más" (§3.1) |

### 7.4 Tesoro Semanal

Ver [Equipamiento](equipamiento.md), §9.

| Fila | Qué la abre | Casillas 1 · 2 · 3 | Qué ofrece |
|---|---|---|---|
| ⚔️ **Grupo** | Mazmorras y Mítica+ | 1 · 4 · 8 completadas | Equipo de tu tramo, con la rareza de lo más difícil que hiciste |
| 🐉 **Banda** | Jefes de banda, Guardianes y Muros | 2 · 4 · 6 jefes | Artefactos y planos |
| 🌍 **Mundo y oficio** | Profundidades, cacerías, expediciones, PvP, jefes de campo, **pedidos de la ciudad y exámenes de oficio** | 3 · 6 · 9 actividades | Materiales raros, tratados de conocimiento de oficio, aceleradores |

- Cada casilla abierta muestra una recompensa. **Eliges una** de hasta 9.
- Si ninguna te sirve, te llevas su valor en Esencia.
- **El artesano también abre su Tesoro.** Los tratados de conocimiento de la tercera fila suben los árboles de especialización ([Profesiones](../07-economia/profesiones.md), §5). Un herrero que no pelea sigue creciendo.

### 7.5 Recuerdos: lo determinista

- La **primera victoria** de cada personaje contra cada Guardián da su **Recuerdo**, en el asalto o en el Eco. Siempre, sin tirada.
- Se cambia por **una de dos piezas** icónicas del Guardián; en un Muro, por una de tres. Se puede guardar y elegir después.
- **Dos formas de cambiarlo:**
  - en el Castillo, al instante, en calidad Buena;
  - con un artesano, que lo usa como artefacto y forja la pieza con su calidad (puede salir Obra Maestra).
- **Fragmentos de Recuerdo.** Cada victoria siguiente contra ese Guardián da un fragmento. Con 5 tienes otro Recuerdo, y te llevas la otra pieza. Es la idea de los Mausoleos Andantes de *Elden Ring*.
- El Recuerdo es ligado: es tu victoria. La pieza, como las armas de artefacto, queda ligada al equiparla.

### 7.6 Dado de Fortuna: la tirada extra

**De dónde sale.** Las tiradas extra de WoW.

- Ganas **uno por semana** con la misión semanal del piso, y a veces en el Tesoro. Guardas 3 como mucho.
- Después de vencer a un jefe puedes gastar uno para **tirar otra vez** tu parte personal y tu parte del cofre en modo personal.
- Si no sale nada útil, te devuelve Esencia y suma Constancia.
- Es ligado y no se compra.

## 8. Filtro de botín en texto

**El problema.** Una expedición puede soltar 40 objetos. Telegram no manda mensajes de más de 4.096 caracteres, y nadie lee 40 líneas ([Telegram](../01-plataforma/telegram.md), §2).

**La solución.** Cada objeto va a uno de tres destinos:
- 👁 **Se muestra:** línea propia, arriba.
- 📦 **Se agrupa:** una línea por tipo ("Mineral de cristal ×12").
- 🤖 **Se resuelve solo:** se vende o se desmonta, y queda una línea de total.

| Qué | Destino por defecto |
|---|---|
| Reliquias, Legendarios, Épicos, artefactos, Recuerdos, planos | 👁 Arriba de todo |
| Lo nuevo para una colección (carta, curiosidad, apariencia) | 👁 Con la marca **NUEVO** |
| Sin tasar, malditos, pistas, llaves y mapas | 👁 |
| Partes de tres estrellas | 👁 |
| Raros | 👁 si sirven a tu spec o a tu oficio; si no, 📦 |
| Materiales y partes de una o dos estrellas, consumibles | 📦 |
| Poco comunes | 📦 o 🤖, según el perfil |
| Comunes | 🤖 Vendidos o desmontados |

**Lo que nunca se filtra.** Artefactos, Reliquias, Recuerdos, objetos sin tasar, malditos, ligados y pistas. El filtro no los puede vender ni desmontar.

**Perfiles.**

| Perfil | Para quién | Qué hace |
|---|---|---|
| **Novato** | Hasta el nivel 10 | Todo a la mochila, con una línea que explica cada cosa nueva |
| **Equilibrado** | Por defecto | La tabla de arriba |
| **Artesano** | Quien tiene oficio | Desmonta en lugar de vender y guarda los materiales de sus oficios |
| **Coleccionista** | Quien completa colecciones | Avisa de todo lo nuevo, aunque sea común |
| **Personalizado** | Cualquiera | Hasta 10 reglas con botones: "vender comunes T1 a T3", "desmontar poco comunes de placas", "avisar si cae algo para Guerrero Protección" |

- **Se comparte por reenvío**, como los filtros de *Path of Exile*: el bot genera un código corto y otro jugador lo pega con `/filtro`.
- **Mochila llena:** se vende primero lo peor según tu perfil, y se dice. Lo protegido espera 24 horas en el **saco** del asentamiento más cercano.
- **Un mensaje nuevo solo si importa.** El resumen va en el mismo mensaje vivo del combate. Solo un Legendario, una Reliquia o un artefacto mandan un mensaje aparte, para que suene la notificación.

```
✅ Victoria · Campamento kóbold (piso 23 · 🔴)
9 rondas · 6 enemigos

✨ +214 Esencia (sin depositar: 1.380 ⚠️ zona roja)
🟣 ÉPICO · Maza Quebrantadora del Oso (T3) [PO 251]
❓ Yelmo desconocido (T3) · ✦ brillo intenso
🃏 NUEVO · carta Kóbold Minero (Mazo de Bestias)
🧩 Fragmento de receta: Elixir de Cuarzo (2/5)
🪨 Mineral de cristal ×12 · Piedra ×20 · Hueso ×6
💰 12 objetos comunes vendidos automáticamente: +86 🪙
🔧 3 poco comunes desmontados: lingote T3 ×2, cuero T3 ×1
▸ Detalle (tocar para abrir)
```

```
🧹 Filtro de botín · perfil Artesano
⚪ Comunes ........... vender solos
🟢 Poco comunes ...... desmontar (Herrería)
🔵 Raros o mejores ... a la mochila
🃏 Lo nuevo .......... avisar ✔
🎯 Avisar para ....... Guerrero Protección ✔
🎒 Mochila llena ..... vender lo peor primero

[⚪ Comunes]   [🟢 Poco comunes]
[🔵 Raros+]    [🎯 Mi spec]
[📤 Compartir] [💾 Guardar]
```

## 9. Contra la inflación de objetos, y el valor de lo raro

**El problema.** Si los objetos se acumulan, a los pocos meses lo que cae no vale nada, nadie compra y el artesano se queda sin trabajo. En *Albion* el equipo se destruye tanto que el artesano siempre vende. Aquí se sigue a *Albion* ([Economía](../07-economia/economia.md), §1).

### 9.1 Por dónde sale cada objeto del juego

| Salida | Qué se lleva | Cuánto |
|---|---|---|
| **Durabilidad máxima** | Todo el equipo | Una pieza dura semanas de uso intenso y después se rompe para siempre ([Equipamiento](equipamiento.md), §4) |
| **Zonas negras** | Lo que llevas puesto | Al caer, cada objeto puede destruirse en lugar de quedar en el suelo |
| **Desmontar** | Equipo viejo o repetido | Devuelve entre el 30 y el 50 % del material |
| **Desencantar** | Objetos mágicos | Los convierte en esencias |
| **Mercado Negro** | Equipo de tramos viejos | Tiene una **reserva por tramo**. Los monstruos solo sueltan equipo de esa reserva: si se vacía, sueltan más materiales; si sobra, retira lo más viejo y lo destruye |
| **Venta automática a PNJ** | Comunes | Se destruyen al venderse |
| **Fabricar** | Artefactos, gemas, runas, fragmentos | Se consumen |
| **Museo y sala de trofeos** | Curiosidades, Reliquias rotas, trofeos | Salen del mercado para siempre |
| **Rituales** | Piezas malditas | Purificar cuesta un porcentaje del valor |

**Se mide.** El informe económico mensual ([Economía](../07-economia/economia.md), §9) cuenta, por tramo y por rareza, cuántos objetos se crearon y cuántos se destruyeron. Si durante dos meses se crean más Épicos de los que se destruyen en un tramo, baja la tasa de rareza de sus tablas. Nunca se toca lo que ya tienen los jugadores.

### 9.2 Por qué lo raro sigue valiendo

- **Historial y número de serie.** Toda pieza Épica o mejor lleva su historia, como el registro de naves de *EVE*. Una pieza con historia se vende mejor.
  ```
  🟡 Garra de las Dunas · n.º 37 del servidor
  Forjada por Lisbeth la Herrera ✒️ con el Recuerdo de Bram
  Portadores: Bram (pisos 45-52) · Kira (desde el 53)
  Venció a 3 Guardianes · Cayó en ⚫ en el piso 51; la recuperó Kira
  ```
- **Lo raro ensancha.** Un Legendario no te vuelve intocable: te da opciones. Por eso sigue sirviendo cuando subes de tramo: para un personaje alterno, para la sala de trofeos, para el museo.
- **Nada de mejoras al azar** sobre objetos ya ganados, por la lección del forjado de titanes. Un objeto sale como sale, y se mejora con Mejoras y Encantamiento, que cuestan.
- **Bandas de precio** ([Economía](../07-economia/economia.md), §3): nadie vende un Legendario a 1 de oro a su cuenta alterna.
- **Primeros del servidor.** El primer Legendario de cada tramo y la primera restauración de cada Reliquia salen en la Gaceta y en el Registro de descubridores ([Descubrimiento y colecciones](descubrimiento-y-colecciones.md), §1).

## 10. Cómo se ve en Telegram: el botín de un Guardián

Grupo de 5 armado por el buscador. Acaban de vencer al **Guardián del Piso 45, Wyrm de las Dunas** ([Jefes](../06-contenido/jefes.md), §4), con la cola y las alas rotas. Cada uno recibe su parte personal por privado; el cofre del grupo se reparte en la sala.

```
🏆 Guardián del Piso 45 · Wyrm de las Dunas · VENCIDO
Asalto · 5 jugadores · 23 rondas · partes rotas: cola, alas

Tu parte (Ossian)
✨ +620 Esencia
📜 RECUERDO: Wyrm de las Dunas (primera victoria)
   → Garra de las Dunas o Escamas del Wyrm  [Elegir]
🦴 Escama de cola ★★★ · Membrana de ala ★★ ×2
🪨 Arena vítrea ×8 · Vidrio de duna ×3
🍀 Constancia (Colmillo de Vidrio): 4 intentos, +32 %
▸ Detalle (tocar para abrir)
```

```
🎁 Cofre del grupo · Necesidad o Codicia
💠 Colmillo de Vidrio · artefacto T5
   Ingrediente de: Daga de Vidrio (técnica Corte de Vidrio)
⏱ 60 s

[🙋 Necesidad] [💰 Codicia] [🚫 Paso]
```

Pasados los 60 segundos, el bot tira los dados en la sala. Cada 🎲 es el dado animado de Telegram:

```
🙋 Necesidad: Lyra, Ossian · 💰 Codicia: Bram · 🚫 Paso: Kira, Tor
Tiran los de Necesidad.
🎲 Lyra ⚃ 4
🎲 Ossian ⚃ 4
Empate. Vuelven a tirar Lyra y Ossian.
🎲 Lyra ⚁ 2
🎲 Ossian ⚄ 5
```

```
💠 Colmillo de Vidrio → Ossian (Necesidad, 🎲 5) · ligado
🍀 Constancia de Ossian (Colmillo de Vidrio): vuelve a 0
🍀 Constancia de Lyra (Colmillo de Vidrio): 6 intentos, +48 %
🎲 Te quedan 2 Dados de Fortuna. ¿Tirar otra vez tu parte?
[🎲 Usar un Dado de Fortuna] [✔ Terminar]
```

## 11. Cómo se conecta

| Sistema | Qué recibe del botín | Qué le da al botín |
|---|---|---|
| [Fabricación](../07-economia/fabricacion.md) y [Profesiones](../07-economia/profesiones.md) | Artefactos, planos, fragmentos, partes, gemas, runas; restauraciones; herramientas con afijos de oficio | Las piezas que siembra el Mercado Negro; los pergaminos de tasación; las ganzúas y varas |
| [Economía](../07-economia/economia.md) | Mercancía; sumideros (venta a PNJ, desmontar, rituales, subastas de gremio) | Bandas de precio; la reserva del Mercado Negro |
| [Bestiario](../06-contenido/bestiario.md) y [Cacerías](../06-contenido/cacerias.md) | — | Partes, crías, trofeos, muestras; el conocimiento abre materiales |
| [Salud](../05-salud/README.md) | Afijos de zona del cuerpo; muestras para curas | — |
| [Investigaciones](../06-contenido/investigaciones.md) | Pistas, libros, botellas con mensaje, tinta que revela textos | Jefes ocultos y su botín |
| [Colecciones](descubrimiento-y-colecciones.md) | Cartas, curiosidades, apariencias, piezas de arqueología, trofeos | "Lo nuevo pesa más" |
| [Crimen y justicia](../06-contenido/crimen-y-justicia.md) | Reliquias malditas de contrabando; certificados falsos | — |
| [Gremios y social](../08-social/gremios-y-social.md) | Necesidad/Codicia con 🎲, cajas del jefe errante, subastas | Maestro de botín, puntos de banda |
| [Casa propia](../09-construccion/casa-propia.md) | Trofeos y Reliquias rotas para la sala de trofeos | — |

## 12. Límites

- **Protección de novato (hasta el nivel 10).** Nada cae sin tasar ni maldito. Los cofres trampa solo tienen alarma. No se pueden equipar piezas malditas.
- **Nada arruina un personaje.** Una pieza maldita siempre se quita con un ritual. Perder el botín en zona roja o negra es un riesgo que eliges. Ningún objeto quita progreso. La única excepción es el Juramento de Hierro, que es opcional.
- **Números chicos.** Los afijos dan del 1 al 3 % o de 3 a 80 puntos. Ningún número de jugador en pantalla pasa de 4 dígitos.
- **Presupuesto parejo entre las 46 specs.** Afijos, únicos y conjuntos pasan por el simulador ([Balance](balance.md), §3). Un único vale lo que 2 afijos; los dos bonos de un conjunto completo, lo que los 4 afijos que le faltan a sus piezas.
- **Nada se compra con dinero real.** Los aceleradores solo suben la cantidad de recursos. No tocan equipo, artefactos, Recuerdos, rareza, Constancia ni Dados de Fortuna ([Monetización](../07-economia/monetizacion.md)).
- **Todo alimenta a otro sistema.** Si una categoría de botín no la compra nadie durante semanas, se le busca una salida: una receta nueva, un pedido de la ciudad, una sala del museo ([Red de sistemas](../00-vision/red-de-sistemas.md), §5).

## Preguntas para el dueño

1. ¿Se puede vender un objeto sin tasar (especular a ciegas)? **Propuesta:** sí, con bandas de precio por tramo y brillo.
2. ¿Dos únicos equipados a la vez, o uno? **Propuesta:** dos.
3. ¿Se permite la subasta de gremio en oro? Puede servir para lavar oro. **Propuesta:** sí, con porcentaje quemado y bandas de precio.
4. ¿Una Reliquia rota se puede reforjar, o solo va al museo? **Propuesta:** se puede reforjar con un artefacto nuevo del mismo origen.
5. ¿El Tasador es un oficio propio o una rama de Encantamiento e Inscripción? **Propuesta:** una rama, para no sumar oficios mayores.
