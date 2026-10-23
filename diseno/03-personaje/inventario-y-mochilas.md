# Inventario y mochilas: qué llevas encima y dónde guardas el resto

> **Módulo** [03 · Personaje](README.md) · **Depende de:** [Equipamiento](equipamiento.md) (ranuras de Mochila, Cinturón y Montura; carga), [Profesiones](../07-economia/profesiones.md) (quién las fabrica) · **Alimenta a:** [Ronda y acciones](../04-combate/ronda-y-acciones.md) (el cinturón del botón 🎒 Mochila), [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md) (peso y tiempo de viaje), [Economía](../07-economia/economia.md) (cuánto se trae en cada viaje) · **Se conecta con:** [Secuelas y muerte](../05-salud/secuelas-y-muerte.md) (qué se pierde al caer), [Casa propia](../09-construccion/casa-propia.md) (almacén), [Monetización](../07-economia/monetizacion.md) · **Estado:** la mochila por tipos y las mochilas de oficio, **en el juego desde la 0.62** (D-338, confirmada; cómo: D-339, provisional; §0); el resto, propuesta (D-47 mochilas, D-46 cinturón). §1 a §3 quedan como historia (los reemplazó D-338)

**Qué pediste (D-47).** Mochilas fabricadas, con niveles de capacidad que se amplían; tipos de mochila según el oficio (herborista, minero, médico, comerciante…); un cinturón para el combate; alforjas, almacén y banco.

**De dónde sale.**
- *Diablo II*: el **cinturón de pociones**. Lo que está en el cinturón se usa en plena pelea; lo que está en el inventario, no. Un cinturón mejor tiene más filas.
- *Resident Evil 4*: el **maletín**. Poco espacio que obliga a decidir qué llevar, y ampliaciones que se consiguen jugando.
- *Albion Online*: el **peso** que frena, las **monturas de carga** (buey, mamut) para mover mucho, los **bancos locales** de cada ciudad y el riesgo de perder lo que llevas según la zona.
- *Kenshi*: las mochilas tienen forma y uso distintos; algunas estorban el combate o el sigilo, y la del ladrón no.
- *Escape from Tarkov*: mochilas **por tamaño** y estuches especiales (de medicinas, de documentos, de munición) que solo aceptan ciertas cosas.
- *Valheim*: el peso manda, el cinturón de fuerza sube la carga, y para mover mucho hay que construir un carro o un barco.
- *RuneScape*: **28 casillas** fijas que caben en una pantalla, el banco con pestañas y las bolsas de oficio (saco de hierbas, bolsa de gemas, bolsa de carbón).
- *Stardew Valley*: las **mejoras de mochila** (12 → 24 → 36), que se pagan con oro del juego y se sienten como un hito.

**Por qué este diseño.** En un juego de texto, el inventario tiene que caber en un mensaje y manejarse con pocos toques. Las casillas son fáciles de contar; el peso le da sentido al viaje (D-58) y al comercio. Y como la mochila se fabrica y tiene tipos por oficio, es otro producto que mueve la economía de jugadores.

---

## 0. Cómo está en el juego (0.62: D-338, confirmada; cómo se aplicó: D-339, provisional)

**Qué pidió el dueño (23-oct-2026).** "La mochila de hoy (60 de espacio) se llena demasiado rápido. Quiero poder farmear mucho más, aunque tarde, y que el límite sea el inventario." Él mismo respondió los puntos abiertos: 50 tipos y 30 de cada uno, todo cuenta menos el equipo, mochilas de oficio en dos niveles (40 y 50), hasta 3 a la vez y nadie pierde lo que ya tiene (D-338).

**De dónde sale.** *RuneScape*: las bolsas de oficio (saco de hierbas, bolsa de gemas) que solo guardan lo de su oficio. *World of Warcraft*: las bolsas de profesión (de herbalista, de minero) con más casillas para lo de su oficio, y el inventario que cuenta casillas de cosas apiladas. *Albion Online*: farmear mucho y volver a la ciudad a vender. *Stardew Valley*: las pilas grandes de un mismo recurso.

### 0.1 Tipos de artículo, no espacio

| Qué | Tope | Dónde está |
|---|---|---|
| 🎒 **Tipos de artículo** distintos en la mochila | **50** | `content/balance.yaml` → `hero.backpack.types` |
| Unidades de cada tipo | **30** (30 × 50 = 1.500 como máximo) | `hero.backpack.per_type` |
| 🛡️ Piezas de equipo **sueltas** (aparte) | **20** (número de Claude, E-288) | `hero.backpack.gear_pieces` |
| 🎒 Mochilas de oficio puestas | **3**, de oficios distintos | `hero.backpack.prof_slots` |

- **Cuenta todo menos el equipo:** recursos, pociones y remedios, comida, 🪑 muebles sin colocar, los 🗺️ pergaminos de mapa (un tipo; cada pergamino es una unidad), las mochilas de oficio sin poner y el 🌰 Recuerdo. Las monedas, 💰 bolsas, 🪎 cofres y 💎 no están en la mochila.
- **El equipo suelto va aparte** porque cada pieza es única (durabilidad, ✒️ firma, ✨ encantamiento) y no se apila. Cada unidad es una pieza.
- **Nunca cuentan:** lo que llevas puesto y el cinturón (3 🧪, 2 🩹… como siempre). Las pociones que pasan del cinturón sí cuentan, como un tipo.
- El beneficio "bag" (🪓 Leñador +10 al rango 100; 🎒 Talabartería y 🛒 Mobiliario +10 con todo el dominio) daba espacio: ahora da **tipos** (la parte entera de lo ganado).
- `hero.backpack_capacity` (60) queda en `balance.yaml` como historia, sin uso.

### 0.2 Las 🎒 mochilas de oficio

Cada oficio de recolección hace la suya, "con su propio oficio", y desde rangos bajos:

| Oficio | Básica (40 por tipo) | Grande (50 por tipo) | Lo que guarda aparte |
|---|---|---|---|
| 🪓 Leñador | rango 5: 🪵 12 + 🟤 2 cuero | rango 40: 🪵 30 + 🟫 6 + 🟤 6 | madera, resina, corteza |
| ⛏️ Minero | rango 5: 🪨 10 + ⚙️ 3 + 🟤 2 | rango 40: 🪨 25 + ⚙️ 10 + 🔩 3 + 🟤 6 | piedra, metal, arcilla, carbón, sal, cuarzo, arena, hielo, chatarra, obsidiana y 💠 gema en bruto |
| 🌿 Herbolario | rango 5: 🌿 8 + 🧵 8 + 🟤 2 | rango 40: 🌿 20 + 🧵 20 + 🧣 4 + 🟤 4 | hierbas, fibra, bayas, setas, miel, mazorca, lino, juncos, nenúfar, cactus, dátiles, flor de escarcha, musgo, raíz amarga, tomillo y 🌸 flor de luna |
| 🎣 Pescador | rango 5: 🐟 12 + 🧵 8 + 🟤 1 | rango 40: 🐟 30 + 🧵 16 + 🧣 4 + 🟤 4 | pescado |
| 🔪 Desollador | rango 5: 🦌 10 + 🧵 6 | rango 40: 🦌 20 + 🟤 8 + 🧣 3 | carne y piel (son botín y entran siempre: su mochila sirve sobre todo para que no ocupen tipos) |

- **Se hacen al fuego** (los oficios de recolección no tenían estación): en cualquiera de las 9 🔥 Fogatas y en el 🔥 Fogón de tu campamento, desde 🛠️ Fabricar. 2 ⚡ la básica y 4 ⚡ la grande; sin 📚 libro de recetas. Piden algo de otro oficio (cuero, fibra o tela): nadie es autosuficiente (D-109).
- **Se llevan, no son una ranura de equipo.** 🎒 Mochila → 🎒 Mochilas de oficio (/mochilas): /mp1 te pones una de la mochila y /mq1 te la quitas. Una del mismo oficio se cambia (la de antes vuelve a la mochila). La que acabas de hacer se pone sola si es la primera de su oficio y queda lugar, o si es mejor que la puesta.
- **Puesta**, sale de la mochila y los recursos de su oficio **no ocupan tipos** (así se leyó "permite cargar más de un tipo de recurso de esa profesión", E-287): van a su compartimento, hasta 40 o 50 de cada uno. **Quitada** es un objeto más (un tipo): se vende en el 🏛️ Mercado (🛍️ Comprar → 🎒 Mochilas de oficio) o se encarga con 📜 Pedidos de fabricación. Las mochilas de otros orígenes (las de la 🎒 Talabartería del diseño, §2) serán mochilas normales.
- Los oficios de refinado todavía no tienen mochila (E-289 propone darles una para sus refinados).

### 0.3 Cuándo se frena y qué nunca se pierde

- **Recolectar** (🧺, 🪓 Talar y 🎣 Pescar): cada unidad mira su tipo. Un recurso lleno (o que sería un tipo nuevo sin tipos libres) deja de juntarse y lo demás sigue; la vuelta y el lote terminan cuando ya no cabe nada de lo que da la zona, sin cobrar la vuelta siguiente. El resumen dice qué se llenó ("🎒 Ya no caben más: 🪵 Madera 30/30") y, si sirve, la 💡 de las mochilas de oficio. La unidad de más del oficio también para en el tope.
- **Comprar al 🛒 mercader, 📦 Recoger de Entregas, lo que sale de una receta, tomar de la ⚔️ Armería y hacer un 🗺️ pergamino:** cada cosa hasta su tope; lo que no cabe espera en 📦 Entregas, y una receta que no cabe no gasta nada (se cuenta la mochila después de gastar los materiales). El aviso dice qué tope frena: "Llenos: 🧪 Poción de vida 30/30" o "Sin tipos libres (50/50) para: 🌿 Hierba curativa".
- **Entra siempre** (D-90): el botín, los hallazgos de explorar, los raros, los premios de la historia, las esencias de desencantar y lo que devuelve un gremio que se disuelve.
- **Nadie pierde nada** (D-338.4, D-64): quien ya pasaba un tope lo conserva todo; solo no entra más de ese tipo (o tipos nuevos) hasta bajar. La mochila lo dice: "🎒 Pasas un tope: no pierdes nada, pero hasta bajar de él no entra más de eso." Quitarse una mochila de oficio siempre se puede, aunque sus recursos pasen a contar como tipos por encima del tope.

### 0.4 Cómo se ve

```
🎒 Mochila
…
🎒 Mochilas de oficio: guardan aparte los recursos de su oficio. Te pones hasta 3.

🎒 Mochila: 12/50 tipos (hasta 30 de cada uno) · 🛡️ Equipo suelto: 3/20
Cuenta cada tipo distinto que llevas (recursos, pociones, comida…), hasta 30 de cada uno. El equipo suelto va aparte; lo puesto y el cinturón no cuentan.
🎒 Mochilas de oficio puestas: 🌿 Herbolario (40 por tipo)

[🛡️ Equipo] [🧪 Pociones]
[💰 Monedas] [📦 Recursos]
[🎒 Mochilas de oficio]
```

📦 Recursos: `🪵 Madera 7/30  /01` · `🌿 Hierba curativa 33/40 🎒  /06` (🎒 = va en tu mochila de oficio: no ocupa tipo). La ficha del héroe: `🎒 Mochila: 12/50 tipos — /inv`. ❓ /d30 (la mochila) y /d67 (las mochilas de oficio).

**Cuánto más se farmea** (registro de balance, 0.62): antes 60 unidades eran ~30 vueltas en una zona de nivel 1 (¾ de día de energía, 4 h); ahora una zona llena sus ~5,7 tipos a las ~170 unidades y la mochila entera guarda 1.500 (25 veces más, ~19 días de energía), más hasta 800 hierbas aparte con la mochila grande del Herbolario.

**Código:** `engine/service/backpack.py` (`BackpackMixin`), `Hero.prof_bags`, `content/items.yaml` (`kind: prof_bag`), `content/professions.yaml` (recetas, `stations.fire`), textos en `content/locales/es_mochila.yaml` y `en_mochila.yaml`; pruebas en `tests/test_mochila_por_tipos.py`.

---

> *Historia (de la 0.6 a la 0.61; lo reemplazó D-338 en la 0.62, §0):* la mochila tenía 60 de espacio y cada unidad ocupaba 1; el cinturón (3 pociones y 2 vendas) y lo que llevas puesto no cuentan. Todavía no hay peso (D-87). Usar algo del cinturón en combate gasta el turno (D-78). El cinturón tiene un lugar por cosa (`balance.yaml` → `hero.belt_slots`: 3 🧪 pociones de vida, 2 🩹 vendas, 1 🍷 poción mayor, 2 🫙 ungüentos, 1 🧰 botiquín y 1 🩻 vendaje de maestro); desde la 0.52 (D-328) las pociones y remedios de los tramos de ⚗️ y 🩺 comparten el lugar de la suya (la 🍷 mayor del tramo 60 va en el de la 🍷 mayor) y se pone primero lo que más cura: el cinturón no crece. La ficha del héroe cuenta igual que el resto del juego ("🎒 Mochila: 4/60", sin el cinturón). Recolectar con la mochila llena o en una zona agotada no empieza ni gasta energía; beber una poción o una venda con la vida llena tampoco se permite, para no gastarla en nada. **Mochila llena (D-90, provisional):** lo que encuentras nunca se pierde (botín, equipo, carne y hallazgos de explorar entran aunque pase de 60, por ejemplo 63/60), pero con la mochila en 60 o más no se recolecta ni se compra en el mercader hasta vender o usar cosas. La mochila, la pantalla del mercader y el aviso al intentarlo lo dicen: "🎒 Mochila llena (63/60): vende o usa cosas para volver a recolectar o comprar."

## 1. Casillas y peso: dos números, una regla cada uno *(historia: diseño anterior a D-338, nunca programado)*

> **Reemplazado por D-338 (0.62, §0).** La mochila del juego cuenta tipos de artículo (50) y unidades de cada uno (30), sin peso. Esta sección y las dos siguientes quedan como historia del diseño: el peso, las mochilas por niveles y los compartimentos podrían volver como capa profunda (D-44), pero no son la regla de hoy.

| Número | Qué limita | Regla |
|---|---|---|
| 📦 **Casillas** | Cuántas cosas distintas llevas | **Límite duro.** Con la mochila llena no recoges más (ver §9) |
| ⚖️ **Peso** | Cuánto te frena | **Límite suave.** Pasar del peso cómodo no te impide cargar, pero te hace más lento |

- **Las cosas iguales se apilan** en una sola casilla: materiales hasta 50, consumibles hasta 10, equipo de a 1.
- **Cada objeto tiene un peso** en kilos, que se ve en su detalle (ver [Equipamiento](equipamiento.md) §3).
- **El oro y la Esencia no ocupan casillas ni pesan.** La Esencia sí se arriesga al caer (ver §8).

**Qué hace el peso de la mochila.**

| Estado | Peso de la mochila | En el viaje | En combate |
|---|---|---|---|
| **Cómodo** | Hasta el peso cómodo | Normal | Normal |
| **Cargado** | Hasta 1,5 veces el peso cómodo | +25 % de tiempo de viaje | Tu Carga sube un escalón |
| **Abarrotado** | Hasta 2 veces el peso cómodo | +50 % de tiempo de viaje | Tu Carga sube dos escalones |
| — | Más de 2 veces | No puedes recoger más | — |

- La **Carga** es la de [Equipamiento](equipamiento.md) §2 (ligera, media, pesada, sobrecargado), que sale de lo que llevas puesto. La mochila solo la empeora cuando pasa del peso cómodo. Así basta mirar un número: si la mochila dice "cómodo", no te afecta.
- Los tiempos de viaje son los de [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md) (fila «Carga y heridas»). Una pierna herida o una secuela que frena se suman aparte.

## 2. Mochilas fabricadas, por niveles *(historia, ver §0)*

Todos empiezan con una **bolsa de tela**. Lo demás se fabrica: la **Peletería** hace las mochilas de cuero y la **Sastrería** las de tela (ver [Profesiones](../07-economia/profesiones.md)).

| Nivel | Mochila | Casillas | Peso cómodo | Quién la hace |
|---|---|---|---|---|
| 0 | Bolsa de tela (inicial) | 12 | 20 kg | Se recibe al crear el personaje |
| 1 | Morral | 16 | 30 kg | Sastrería o Peletería, rango Aprendiz |
| 2 | Mochila de viaje | 20 | 40 kg | Rango Oficial |
| 3 | Mochila de expedición | 24 | 50 kg | Rango Experto |
| 4 | Mochila de maestro | 28 | 60 kg | Rango Artesano, con un material raro |

Los números son orientativos y van al registro de balance.

**Se amplía, no se tira.** Una mochila sube de nivel con **mejoras** sobre la misma pieza, sin perder su tipo ni su calidad:

- **Costuras y refuerzos** (+2 casillas cada uno, hasta el tope de su nivel) y **correas** (+5 kg de peso cómodo). Los fabrica el mismo oficio.
- **Subir de nivel** pide al artesano del rango que toca, materiales y oro del juego.
- La **calidad** de la fabricación (ver [Fabricación](../07-economia/fabricacion.md)) da un pequeño extra: una mochila de calidad excelente lleva 1 casilla más.

## 3. Tipos de mochila según el oficio *(historia: lo que está en el juego, en §0.2)*

Cada mochila puede llevar **un compartimento de oficio**. El compartimento tiene casillas propias que solo aceptan ciertas cosas y da una comodidad de ese oficio. **Nunca da poder de combate**: ayuda a trabajar, a viajar y a comerciar. Así el oficio hace la diferencia, como pide D-49, sin desbalancear las peleas.

| Tipo | Para | Compartimento | Qué permite | Pieza extra (otro oficio) |
|---|---|---|---|---|
| 🌿 **Mochila de herborista** | Herboristería, Agricultura | Bolsillo de hierbas (+10 casillas, solo hierbas, hongos y flores) | Las hierbas no se marchitan durante el viaje; ves la estación de cada hierba que recoges | Forro de lino (Sastrería) |
| ⛏ **Mochila de minero** | Minería, Fundición | Saco de mineral (+8 casillas, solo mineral, piedra y gemas en bruto) | El mineral pesa la mitad; el pico va colgado y no ocupa casilla | Armazón de hierro (Herrería) |
| 🩺 **Botiquín de médico** | Medicina, Primeros Auxilios | Botiquín (+8 casillas, solo vendas, remedios e instrumental) | Tratar en el campo lo que pide instrumental (suturas, entablillar) sin volver a una enfermería; el instrumental no se ensucia | Estuche de instrumental (Herrería) |
| 🪤 **Morral de cazador** | Desuello y caza | Morral de trampas (+8 casillas, solo trampas, cebos, pieles y carne) | Las trampas van armadas y se colocan en un toque; pieles y carne tardan el doble en echarse a perder | Ganchos (Herrería) |
| 🐴 **Alforjas de buhonero** | Comercio | Fardo de mercancía (+10 casillas, solo bienes empaquetados para vender) | La mercancía empaquetada pesa un 25 % menos; ves el precio del mercado local al entrar a un asentamiento | Sello de comerciante (Inscripción) |
| 🔨 **Mochila de obra** | Construcción | Cinturón de herramientas (+6 casillas, solo herramientas y piezas de obra) | Las herramientas no ocupan casillas de la mochila; llevas a la obra las piezas pequeñas sin carreta | Hebillas (Herrería) |
| ⚗️ **Estuche de alquimista** | Alquimia | Estuche de frascos (+8 casillas, solo frascos, pociones e ingredientes) | Los frascos no se rompen al caer ni al viajar; las pociones se apilan hasta 15 | Frascos de vidrio soplado (Joyería) |
| 🍲 **Fiambrera de cocinero** | Cocina, Pesca | Despensa portátil (+8 casillas, solo comida e ingredientes) | La comida y el pescado no se estropean en el viaje; cocinar al fuego de campamento sin estación | Caja aislada (Carpintería) |
| 🗝 **Mochila de ladrón** | Ladrones (ver [Crimen y justicia](../06-contenido/crimen-y-justicia.md)) | Bolsillos ocultos (+4 casillas) | Lo que va en los bolsillos ocultos no aparece cuando un guardia te registra; no estorba el sigilo | Costuras dobles (Sastrería) |
| 🗺 **Portamapas de explorador** | Cartografía (Inscripción), Arqueología | Tubo de mapas (+6 casillas, solo mapas, notas y muestras) | Los mapas y las notas no se mojan ni se pierden; anotar un lugar nuevo es un toque | Tubo encerado (Carpintería) |
| 📜 **Cartapacio de escriba** | Inscripción | Cartapacio (+6 casillas, solo pergaminos, tintas y libros) | Copiar y leer pergaminos en el viaje; las tintas no se derraman | Tapas de cuero (Peletería) |

- **Una mochila, un compartimento.** Cambiar de tipo es cambiar de mochila: quien trabaja en varios oficios (D-57) tiene varias y elige cuál llevar en cada salida. Esa elección es parte del costo natural de serlo todo.
- **La mochila general** (sin compartimento) tiene 2 casillas más que una de oficio del mismo nivel. Es la mejor si no te dedicas a nada en particular.
- **Los cinturones no tienen tipo de oficio.** El cinturón decide lo que usas en combate, y el combate tiene que ser igual para todos (D-49).

## 4. El cinturón de combate

El cinturón es lo único que se abre con el botón 🎒 **Mochila** en combate (D-46). Las reglas de uso están en [Ronda y acciones](../04-combate/ronda-y-acciones.md) §4; aquí, lo que es el cinturón como objeto.

| Cinturón | Casillas | Quién lo hace |
|---|---|---|
| Cordel (inicial) | 3 | Se recibe al crear el personaje |
| Cinturón de cuero | 4 | Peletería, rango Aprendiz |
| Cinturón reforzado | 5 | Peletería, rango Experto |
| Cinturón de maestro | 6 | Peletería, rango Artesano |

- **Cada casilla lleva un solo tipo de objeto**, hasta 3 unidades. Seis casillas es el tope: con más, el menú del combate dejaría de caber en la pantalla.
- **Qué va:** pociones de vida, de resistencia y de recurso, remedios para estados (antídoto para el veneno, coagulante y venda para el sangrado, ungüento para la quemadura, tónico caliente para la congelación), vendas, bombas, comida rápida y el kit de ajuste de prótesis.
- **Límites que ya existen:** usar un objeto gasta la elección de la ronda, la **Toxicidad** limita cuántas pociones aguantas (ver [Condiciones](../05-salud/condiciones.md) §4) y hay un máximo de 3 lanzables por pelea (ver [Mecánicas avanzadas](../04-combate/mecanicas-avanzadas.md)).
- **Se prepara antes de salir** y **se rellena solo** desde la mochila al terminar cada pelea, si tienes con qué.
- **Configuraciones guardadas:** el cinturón se guarda junto con cada configuración de [Talentos](talentos.md) ("solitario", "mazmorra", "PvP"). Cambiar de configuración cambia también el cinturón, en un toque.
- **En la arena clasificada** el cinturón es el mismo para todos (ver [Ronda y acciones](../04-combate/ronda-y-acciones.md) §11).
- **No se compra con dinero real.** Ni casillas ni cinturones (D-43): el cinturón es poder de combate.

## 5. Alforjas de montura y carretas de caravana

| Medio | Capacidad orientativa | Qué cambia | Quién lo hace |
|---|---|---|---|
| 🐎 **Alforjas de montura** | +12 casillas y +30 kg de peso cómodo | Solo mientras vas montado. No se abren en combate | Peletería (rama Monturas) |
| 🐂 **Montura de carga** (mula, buey) | +24 casillas y +80 kg | No acorta el viaje como una montura de silla; lleva mucho más | Ganadería; alforjas de Peletería |
| 🛒 **Carreta de caravana** | Cientos de casillas, toneladas | Va despacio y por caminos; se puede asaltar en zonas rojas y negras; la mejoran los caminos y las escoltas | Carpintería (carros de caravana); el oficio de Comercio suma capacidad |

- La montura y sus alforjas ocupan la ranura de **Montura** de [Equipamiento](equipamiento.md) §1.
- Las monturas y los tiempos de viaje están en [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md); las caravanas, los peajes y los asaltos, en [Economía](../07-economia/economia.md) y en [Propiedad y concesiones](../07-economia/propiedad-y-concesiones.md) (concesiones de ruta).
- **Por qué conviene.** Si mover mucho fuera fácil, no habría oficio de transportista ni mercados distintos en cada lugar (D-58).

## 6. Dónde se guarda lo que no llevas

Lo guardado **nunca se pierde al caer**. Todo depósito está **en un lugar** del mapa: lo que guardas en un asentamiento está ahí, y para usarlo hay que ir (D-58).

| Depósito | Dónde | Capacidad orientativa | Para qué |
|---|---|---|---|
| 🛏 **Cuarto** | Tu comunidad o tu asentamiento de residencia | 10 casillas | Lo básico; sus guardias lo cuidan (ver [El Colapso y las comunidades](../02-mundo/el-colapso-y-las-comunidades.md)) |
| 🏦 **Banco personal** | Cada asentamiento con banco | 50 casillas por banco, en pestañas | Lo tuyo, en ese lugar. Un banco en cada ciudad donde comercias |
| 🏦 **Banco de cuenta** | En los mismos bancos | 20 casillas por banco | Compartido entre los personajes de tu cuenta, en ese lugar. Sirve para pasarle cosas a otro héroe tuyo |
| 🏠 **Almacén de casa** | Tu casa (ver [Casa propia](../09-construccion/casa-propia.md)) | Según la habitación y sus estanterías y cofres | Lo grande: materiales del taller, cosechas, trofeos. Al lado de tus estaciones |
| 🏰 **Almacén de gremio** | El salón del gremio | Según la obra | Compartido, con permisos por rango (ver [Gremios y social](../08-social/gremios-y-social.md)) |

- **Los bancos cobran una pequeña tasa** por sacar objetos (sumidero de oro). Guardar es gratis.
- **El banco amplía pestañas** con oro del juego y con logros.

## 7. Ampliaciones: se fabrican y se ganan

| Cómo | Qué amplía |
|---|---|
| 🔨 **Se fabrican** | Mochilas, mejoras de mochila, cinturones, alforjas, carretas, estanterías y cofres del almacén. Es la vía principal y la que mueve la economía |
| 🏆 **Se ganan jugando** | Correas y costuras raras que dan cacerías, jefes y colecciones (por ejemplo, *correa de piel de Wyrm*: +5 kg); pestañas de banco por logros; la mochila de oficio de rango Maestro como premio del examen del oficio |
| 💳 **Dinero real** (D-43) | **Nada.** El dinero real solo compra cosméticos y aceleradores (ver [Monetización](../07-economia/monetizacion.md)), y el espacio no es ninguna de las dos cosas |

**Por qué nada.** Más mochila es más botín por viaje, más cinturón es más poder en la pelea y más banco es más ventaja en el comercio. Por eso **la mochila, el cinturón, las alforjas, las carretas y el banco nunca se venden por dinero real** (ver también [Equipamiento](equipamiento.md) §8).

## 8. Qué se pierde al caer

La tabla general está en [Secuelas y muerte](../05-salud/secuelas-y-muerte.md) §4.1. Esto define qué parte del inventario cae en cada zona:

| Zona | Mochila | Cinturón | Alforjas | Lo puesto |
|---|---|---|---|---|
| 🔵 **Azul** | No se puede caer | — | — | — |
| 🟡 **Amarilla** | Se queda contigo | Se queda contigo | Se quedan contigo | −10 % de durabilidad |
| 🔴 **Roja** | **Se puede saquear**, compartimento incluido | **Se puede saquear** | La montura huye y vuelve al último establo con sus alforjas | Se queda contigo, con −10 % de durabilidad |
| ⚫ **Negra** | Se puede saquear | Se puede saquear | Se pueden saquear | Se puede saquear |

- **Nunca se pierde:** lo guardado (§6), las **prótesis**, los objetos de misión y los objetos **atados** a tu personaje (ver [Equipamiento](equipamiento.md) §5).
- **No hay casillas a salvo.** No existe un "contenedor seguro" como el de *Tarkov*: el riesgo de la zona tiene que ser real. Lo que no quieres arriesgar se deja en el banco.
- **Juramento de Hierro:** las mismas reglas, con lo que ya dice [Secuelas y muerte](../05-salud/secuelas-y-muerte.md) §4.2.

## 9. Ligero de manejar: filtros y orden automático

La capa simple no pide ordenar nada (D-44):

- **Orden automático.** La mochila se ordena sola por grupos: 📦 Materiales, 🧪 Consumibles, ⚔️ Equipo, 📜 Misión, 💰 Para vender. Las pilas se juntan solas.
- **Filtros de un toque.** Cada grupo es un botón con su número; se abre solo lo que pides.
- **Al compartimento, solo.** Lo que va en el compartimento de oficio entra ahí primero, sin preguntar.
- **🏦 Depositar materiales.** En un banco o en tu casa, un toque manda todos los materiales al depósito. Los consumibles y el cinturón se quedan.
- **💰 Vender lo sobrante.** En un mercader PNJ, un toque vende lo marcado "para vender" (el equipo que no te sirve, ver [Botín](botin.md)). Lo marcado con 🔒 nunca se vende ni se tira.
- **Mochila llena.** El bot no pierde nada en silencio: ofrece cambiar lo nuevo por lo de menos valor, dejarlo o abrir la mochila.
  - *En el juego (D-90 y D-338, desde la 0.62):* lo encontrado entra siempre, aunque pase los topes; lo que se frena es sumar más de un tipo lleno o tipos nuevos (recolectar, comprar, recoger, fabricar) hasta que vendas o uses cosas (§0.3).

**Capa profunda (opcional):** reglas de recogida ("no recoger lo gris", "solo hierbas de calidad buena o mejor"), pestañas de banco con nombre y orden a mano.

## 10. Cómo se ve

**La mochila** (comando `/mochila` o botón 🎒 fuera de combate):

```
🎒 Mochila de herborista · Nivel 3 (Expedición)
📦 18/24 casillas · ⚖️ 41/50 kg · cómodo

🌿 Bolsillo de hierbas 7/10 · no se marchitan
   Hoja de plata ×14 · Hongo nocturno ×6 · Flor de escarcha ×3

[📦 Materiales 8] [🧪 Consumibles 5]
[⚔️ Equipo 2] [📜 Misión 1] [💰 Para vender 2]
[🪢 Cinturón] [🏦 Depositar materiales]
```

**El cinturón** (botón 🪢 Cinturón):

```
🪢 Cinturón reforzado · 5 casillas · hasta 3 por casilla
Configuración: Solitario ✓ · Mazmorra · PvP

1. 🧪 Poción de vida ×3
2. 🔥 Resistencia al fuego ×2
3. 💊 Coagulante ×2
4. 🩹 Venda ×3
5. 🍖 Pan de viaje ×3

↻ Se rellena solo al terminar cada pelea
   (quedan 🧪 ×7 y 🩹 ×4 en la mochila)

[✏️ Cambiar una casilla] [💾 Guardar en esta configuración]
```

**📦 Recursos con código (D-243, en el juego desde la 0.33).** El dueño pidió (17-oct) quitar de la lista "toda esa información" de para qué sirve cada recurso: "el icono, el nombre, la cantidad, dos espacios y el código de ese recurso". Para saber para qué es, se toca el código:

```
📦 Recursos
Lo que juntaste. Toca el código de un recurso para ver para qué sirve:
🪨 Piedra ×14  /02
🌿 Hierba curativa ×11  /06
⚙️ Pieza de metal ×9  /05
Página 1 de 2
```

- **El código es fijo y se escribe a mano** en `content/items.yaml` (`code: 2`), nunca sale del orden de la lista: agregar un recurso no cambia los códigos que el jugador ya conoce (regla de IDs estables). Hoy van del 1 al 52 (41 materiales, 7 comidas y 4 muebles). Los números pelados (`/07`) quedan reservados para siempre a los recursos.
- **Al tocar `/07`** se abre la pantalla del recurso: cuántos llevas y para qué sirve (el mismo texto que antes salía en la lista). Se puede mirar aunque no lo lleves; un código que no existe vuelve a 📦 Recursos con un aviso. Su botón: ↩️ Volver a 📦 Recursos.
- **Por ahora no se genera de las recetas** qué oficio lo junta y quién lo pide (punto c de D-243): el dueño dijo que eso "no me interesa que la gente lo sepa. No por ahora" (D-255).

**Mochila llena:**

```
⚠️ Mochila llena. Encontraste 🪨 Mineral de hierro ×3.

[🔄 Cambiarlo por 🦴 Hueso ×2 (lo de menos valor)]
[🗑 Dejarlo aquí] [🎒 Abrir la mochila]
```

## 11. Red de sistemas

| Consume | Produce |
|---|---|
| Cuero, tela, hilo, piezas de otros oficios (hierro, vidrio, madera), oro del juego para mejoras y tasas de banco | Demanda para Peletería, Sastrería y los oficios de las piezas extra; un límite a lo que se trae por viaje, que crea transportistas, caravanas y mercados locales; riesgo real en zonas rojas y negras; la preparación del cinturón como conocimiento del jugador (D-49) |

Se conecta con la [Red de sistemas](../00-vision/red-de-sistemas.md) por la economía (fabricación y sumideros), el viaje (peso) y el combate (cinturón).

## 12. Todo en texto, por turnos y sin dinero real que dé poder

- Todo es texto y botones: casillas que se cuentan, pesos en kilos y un mensaje por pantalla.
- El motor guarda el inventario igual para los tres clientes (Telegram, web y app). La web puede mostrar más casillas por pantalla, pero las reglas son las mismas (D-40, D-41).
- El dinero real no amplía nada de esto: solo compra cosméticos y aceleradores (D-43).
