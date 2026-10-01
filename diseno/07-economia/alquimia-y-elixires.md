# Alquimia y elixires: ingredientes con propiedades y elixires con nombre propio

> **Módulo** [07 · Economía](README.md) · **Depende de:** [Profesiones](profesiones.md) (Alquimia, Herboristería, Desuello), [Fabricación](fabricacion.md) (minijuego, calidad de las vetas, descubrimiento), [Escalera de conocimiento](escalera-de-conocimiento.md) (expedientes de ingrediente, técnicas de Alquimia), [Condiciones](../05-salud/condiciones.md) (Toxicidad y dependencia), [Geografía y recursos](../02-mundo/geografia-y-recursos.md) (terrenos, yacimientos únicos), [Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md) (estaciones, clima, día y noche) · **Se conecta con:** [Ronda y acciones](../04-combate/ronda-y-acciones.md) (🎒 Mochila y cinturón), [Daño y estados](../04-combate/dano-y-estados.md) (estados por acumulación), [Peligros del entorno](../05-salud/peligros-del-entorno.md), [Curación](../05-salud/curacion-y-tratamientos.md), [Investigación médica](../05-salud/investigacion-medica.md), [Mente](../05-salud/mente.md) (estrés), [Inventario y mochilas](../03-personaje/inventario-y-mochilas.md), [Balance](../03-personaje/balance.md), [PvP](../06-contenido/pvp.md), [Investigación y maestría](investigacion-y-maestria.md) (patentes y enseñanza), [Propiedad y concesiones](propiedad-y-concesiones.md) (botica propia), [Red de sistemas](../00-vision/red-de-sistemas.md) · **Estado:** propuesta (la regla de fondo es D-55, confirmada)

**Qué pediste.**
- "Incluso seas capaz de crear tus propios elixires, no solamente con una curación, sino con una curación con un plus de varias cosas."

Eso quedó registrado como **D-55** en [Decisiones](../00-vision/decisiones.md): el alquimista combina ingredientes y crea elixires con nombre propio, que curan y suman varios efectos a la vez, con límites de balance. Este documento lo arma. Es la **cima** de la Alquimia en la [Escalera de conocimiento](escalera-de-conocimiento.md) §3.3, pero se empieza a probar desde el rango Aprendiz, con mezclas de un solo efecto.

**De dónde sale.**
- *The Elder Scrolls V: Skyrim*: cada ingrediente tiene **cuatro efectos ocultos**. Comerlo revela el primero; los demás se descubren mezclando. Al juntar ingredientes, la poción recibe **los efectos que comparten**, buenos y malos.
- *The Witcher 3*: pociones de efecto corto, **decocciones** de efecto largo y una barra de **Toxicidad** que impide encadenarlas. Ya la usa [Condiciones](../05-salud/condiciones.md) §4.
- *Potion Craft*: el alquimista descubre recetas probando, les pone **nombre** y las vende en su tienda. La fama de la botica depende de sus pociones.
- *Kingdom Come: Deliverance*: la receta es **paso a paso** (qué va primero, cuánto hierve, cuándo se destila). Equivocarse en el orden arruina la poción.
- *Final Fantasy XIV*: el **minijuego de fabricación** por turnos decide la **calidad**. Es el que ya usa [Fabricación](fabricacion.md) §2.
- *Path of Exile*: los **frascos con modificadores**: curan y suman un efecto extra, como quitar el sangrado o subir la armadura.
- *Atelier* (la saga): los objetos **heredan rasgos** de sus ingredientes, y elegir el ingrediente justo para pasar un rasgo es el corazón del juego.

**Por qué conviene.** La poción de vida de un toque sigue existiendo para todos. Pero quien quiera ser alquimista tiene un juego propio: conocer ingredientes, juntarlos en el lugar y la estación justos, y crear un elixir que nadie más hace, con su nombre en la etiqueta. Eso da oficio, fama y comercio sin dar más poder del que el [Balance](../03-personaje/balance.md) permite.

---

## 1. La regla, en corto

1. **Cada ingrediente tiene 4 propiedades.** La primera se ve al recogerlo; las otras se descubren (§3.4).
2. **Mezclar es compartir.** Se juntan de 2 a 4 ingredientes en el alambique. Cada propiedad que aparece en **dos o más** ingredientes da su efecto al elixir (§4 y §5).
3. **El minijuego decide la potencia y la estabilidad** (§5.3). El modo rápido es de un toque y llega a Notable.
4. **El alquimista le pone nombre** y la receta queda registrada a su nombre: se vende, se enseña y se patenta (§5.4).
5. **Los límites son duros:** efectos por rango, reparto de potencia, topes por efecto, nada se acumula con lo mismo, Toxicidad que crece con cada efecto y con la potencia, dependencia, reglas de PvP y caducidad (§6).
6. **Un elixir se bebe, no se da.** Solo afecta a quien lo toma. Así nunca reemplaza a un sanador ni a un defensor (§7.3).
7. **Nada se compra con dinero real** (D-43). Ni ingredientes, ni recetas, ni potencia, ni casillas del cinturón. Los aceleradores no tocan los expedientes ni los ingredientes de temporada (ver [Escalera de conocimiento](escalera-de-conocimiento.md) §1, regla 6).

### 1.1 Ligero: capa simple y capa profunda (D-44)

| Quién | Qué hace | Cuánto le pide |
|---|---|---|
| **Jugador de paso** (casi todos) | Compra una poción conocida al mercader del campamento (la poción de vida cuesta 6 💰, D-76) o un elixir con nombre de otro jugador en el mercado, y lo pone en el cinturón | **Un toque.** No necesita saber que existen las propiedades |
| **Alquimista de todos los días** | Fabrica las recetas que ya sabe (de entrenador, compradas o propias) en modo rápido | **Un toque** por tanda. Hasta calidad Notable |
| **Alquimista inventor** | Abre el alambique, prueba ingredientes, descubre propiedades, juega el minijuego y registra elixires con nombre | Lo que quiera: es su carrera |

**Pistas, no respuestas** (D-56). La primera vez que dos ingredientes comparten una propiedad, el alambique dice solo: *"🔎 Estos dos tienen algo en común. Embotéllalo y verás qué."* Lo demás se aprende probando (ver [Aprendizaje y pistas](../00-vision/aprendizaje-y-pistas.md)).

**Así se ve la capa simple.** Fabricar una receta conocida, con un toque:

```
⚗️ Recetas conocidas (Alquimia 47 · Experta)

🧪 Poción de vida · ❤️ 35 % · ☠️ 40
🍷 Trago de Caravana · 💧 Sales · ☀️ Frescor
🍷 Aliento de Cumbre de Mara · licencia, regalía 4 %

Tienes ingredientes para: 🧪 ×6 · 🍷 Trago ×3

[🧪 Fabricar ×6]   [🍷 Trago ×3]
[⚗️ Alambique]     [▶️ Ver más]
```

Máximo 4 botones en el mensaje, como pide D-75; el resto de las recetas está en "▶️ Ver más".

## 2. Las propiedades

Las propiedades son **el mismo vocabulario** que usa la [Investigación médica](../05-salud/investigacion-medica.md) §2.3 y §2.4 (Fría, Cálida, Purificante, Cicatrizante…). Un ingrediente tiene las mismas propiedades para el médico y para el alquimista; cada uno las usa a su manera.

Hay cuatro clases de propiedad:

| Clase | Cómo actúa | Ejemplos |
|---|---|---|
| ✅ **De efecto** | Si **dos o más** ingredientes la comparten, el elixir gana su efecto (§4.1) | Cicatrizante, Ignífuga, Despertadora |
| ⚠️ **Negativa** | Si dos o más la comparten, el elixir gana un **efecto secundario** (§4.2). No cuenta para el límite de efectos y no se quita sin una técnica | Amarga, Nerviosa, Adormecedora, Tóxica |
| 🔧 **Modificadora** | Actúa con **un solo** ingrediente que la tenga. No da efecto: cambia el elixir | Pura, Dulce, Conservante, Pegajosa, Salvaje |
| ⚕️ **Médica** | No da nada en un elixir: solo sirve en los remedios de la investigación médica | de Memoria, Ordenadora, Regenerativa, Contagiosa |

**Modificadoras:**

| Propiedad | Qué hace en el elixir |
|---|---|
| 💠 **Pura** | +1 nivel de estabilidad (dura más tiempo fresco, §6.9) |
| 🍬 **Dulce** | −5 de Toxicidad por cada ingrediente dulce, hasta −10, sin bajar más del 15 % la Toxicidad del elixir (§6.7) |
| 🧊 **Conservante** | +50 % de días fresco |
| 🕸️ **Pegajosa** | +1 ronda (o +10 pasos fuera de combate) a los efectos con duración |
| 🐾 **Salvaje** | ×1,1 de potencia, pero −1 nivel de estabilidad y el doble de tolerancia (§6.8) |

## 3. Los ingredientes

### 3.1 De dónde salen

| Tipo | Quién lo trae | Ejemplos |
|---|---|---|
| 🌿 **Hierbas y flores** | Herboristería (y Agricultura, si se cultiva) | Hierba curativa, Cardo rojo, Flor de Ciénaga Tardía |
| 🍄 **Hongos** | Herboristería en cuevas y pantanos | Hongo luminoso, Corazón de micelio |
| 🦎 **Partes de monstruo** | Desuello y caza; [Cacerías](../06-contenido/cacerias.md) para las raras | Escama de salamandra en muda, Glándula de sapo de ciénaga |
| ⛏️ **Minerales** | Minería | Carbón de montaña, Ámbar de tundra |
| 💧 **Aguas especiales** | Exploradores y aguadores, con frasco | Agua de fondo del Oasis Hondo, Agua de rayo |

### 3.2 Potencia: la veta, la zona y la estación

Cada lote de ingrediente tiene **Potencia** y **Pureza**, como dice la [Investigación médica](../05-salud/investigacion-medica.md) §2.4. La Potencia mueve la fuerza del elixir; la Pureza, su estabilidad. Aquí se leen con **100 = normal**. [Fabricación](fabricacion.md) §3 todavía no nombra la Potencia entre sus atributos y usa otra escala (pureza 870), así que hay que igualarlos (§14).

| Qué la mueve | Cómo | Ejemplo |
|---|---|---|
| **La veta o la planta** | Cada nodo tiene su calidad, que rota cada semana | Un campo de cardos de potencia 115 es noticia para los alquimistas de la región |
| **La zona** | Los anillos más lejanos dan lotes con techo más alto | La Hierba curativa del anillo I llega a 100; la del anillo VI, a 125 |
| **La estación** | En su estación, el ingrediente está **en sazón**: +10 de potencia. Fuera de estación solo hay lotes conservados, con −10 | La Raíz de mandrágora solo es tierna en primavera |
| **La hora y el clima** | Algunos solo existen de noche, con ventisca o con tormenta | La Flor de Ciénaga Tardía, de noche en otoño |

**Potencia de los lotes en el elixir:** el promedio de la Potencia de los lotes usados (100 = normal) da un multiplicador entre **×0,8 y ×1,25**. Los materiales de temporada llevan 🌙 y los de yacimiento único ⭐ en la mochila (ver [Escalera de conocimiento](escalera-de-conocimiento.md) §2.4).

### 3.3 Veinte ingredientes de ejemplo

La propiedad en **negrita** es la que se ve al recogerlo. Las demás se descubren (§3.4). Los que ya aparecen en la [Investigación médica](../05-salud/investigacion-medica.md) §2.4 conservan las dos propiedades, el lugar y la estación que dice ese documento; aquí se completan las cuatro. La 🌿 Hierba curativa ya existe en el juego como material.

| Ingrediente | Propiedades | Dónde | Cuándo | Quién lo trae |
|---|---|---|---|---|
| 🌿 **Hierba curativa** | **Cicatrizante** · Vivificante · Creciente · Amarga | 🌾 Llanura, 🌲 bosque y 🐸 pantano (donde más hay), cualquier anillo, como ya hace el código | Siempre; poca en invierno | Herborista; cualquiera al explorar |
| 🌺 **Cardo rojo** | **Coagulante** · Cicatrizante · Aguda · Nerviosa | 🌾 Llanura, anillos I a III | Primavera y verano | Herborista |
| 🌊 **Alga de costa** | **Acuática** · Coagulante · Mineral · Emoliente | 🌊 Costa y lagos | Siempre; con marea baja rinde el doble | Herborista o pescador |
| ⬛ **Carbón de montaña** | **Pulmonar** · Purificante · Pétrea · Amarga | ⛰️ Montaña | Siempre | Minero |
| 🌋 **Flor de Ceniza** | **Ignífuga** · Cicatrizante · Cálida · Nerviosa | 🌋 Tierras volcánicas y laderas quemadas | Verano; después de una erupción, más | Herborista con capa ignífuga |
| 🍄 **Hongo luminoso** | **Sombría** · Resonante · Luminosa · Adormecedora | 🕳️ Cueva y subsuelo | Siempre; de noche rinde el doble | Herborista con luz |
| 🕸️ **Corazón de micelio** | **Creciente** · Pegajosa · Renovadora · Tóxica | 🕳️ Cueva, anillo III (Micelio Andante) | Siempre; **cultivado** en casa rinde más | Cazador, después Agricultor |
| 🐸 **Glándula de sapo de ciénaga** | **Despertadora** · Acuática · Salvaje · Tóxica | 🐸 Pantano (monstruo) | Verano, época de canto | Cazador con Desuello |
| 🌵 **Pulpa de cactus de duna** | **Mineral** · Fría · Emoliente · Dulce | 🏜️ Desierto | Siempre; la flor nocturna da lotes mejores | Herborista o aguador |
| 🟠 **Ámbar de tundra** | **Conservante** · Pétrea · Terrosa · Cálida | ❄️ Tundra | Siempre | Minero |
| 👁️ **Ojo de lince de las nieves** | **Aguda** · Sombría · Aislante · Salvaje | ❄️ Tundra y ⛰️ montaña (monstruo) | Invierno | Cazador con Desuello |
| 🌱 **Raíz de mandrágora tierna** | **Sedante** · Adormecedora · Calmante · Renovadora | 🐸 Pantano, anillo IV | Primavera 🌙 | Herborista con tapones de cera |
| 🌸 **Flor de Ciénaga Tardía** | **Fría** · Amarga · Purificante · Sombría | 🐸 Pantano, anillo IV | Otoño, de noche 🌙 | Herborista con máscara de carbón |
| 🌿 **Musgo de Cumbre Blanca** | **Cálida** · Pulmonar · Aislante · Pura | ⛰️ Montaña (Picos Helados), anillo VI | Invierno, después de una ventisca 🌙 | Herborista aclimatado |
| 💧 **Agua de fondo del Oasis Hondo** | **Pura** · Mineral · Fría · Conservante | 🏜️ Desierto, anillo V | Verano, cuando el oasis baja 🌙 | Aguador con frasco de vidrio de duna |
| ❄️ **Lágrima helada** | **Fría** · Conservante · Aislante · Resonante | ❄️ Tundra y pasos, anillo VI (Novia de Escarcha) | Con ventisca 🌙 | Cazadores en grupo |
| 🦎 **Escama de salamandra en muda** | **Cálida** · Renovadora · Ignífuga · Salvaje | 🌋 Tierras volcánicas, anillo VIII | Verano, época de muda 🌙 | Cazador con capa ignífuga |
| 🍯 **Miel negra** | **Cicatrizante** · Dulce · Sedante · Renovadora | 🏛️ Ruinas y 🌲 bosque, anillo VII (Árbol Hueco) | Otoño 🌙 | Cazador y herborista |
| 🌼 **Polen de Flor de Difuntos** | **Calmante** · de Memoria · Luminosa · Adormecedora | 🌾 Llanuras de cualquier anillo | Solo en el festival de difuntos 🌙 | Herborista o agricultor |
| ⚡ **Agua de rayo** | **Vivificante** · Nerviosa · Terrosa · Despertadora | 🌸 Tierras flotantes, anillo X | Solo con tormenta 🌙 | Explorador con pararrayos |

Los yacimientos únicos (por ejemplo, la **Sal de Estrellas**: Purificante · Pura · Luminosa · Terrosa ⭐) y los ingredientes de evento (el **Hongo del Eclipse**: Sombría · Despertadora · …) se suman con el mismo formato. Los anillos siguen el [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md) (un anillo son 3 Lejanías).

### 3.4 Descubrir las propiedades ocultas

Cuatro caminos, y se pueden mezclar:

| Camino | Cómo | Qué revela | Costo |
|---|---|---|---|
| 🔬 **Experimentar** | Mezclar en el alambique (§5). Al embotellar, cada propiedad compartida se revela en los ingredientes que la tienen. Una mezcla que no comparte nada también enseña: *"La Hierba curativa y el Ámbar no tienen nada en común"* | Las propiedades compartidas | Los ingredientes de la prueba |
| 👅 **Probar** | Comer un ingrediente crudo (un toque) | La siguiente propiedad oculta, solo hasta la 2ª | +10 de Toxicidad; si es Amarga o Tóxica, también su secundario |
| 📒 **El expediente** | Cada ingrediente tiene su expediente en la [Escalera de conocimiento](escalera-de-conocimiento.md) §2.2, que se llena solo al recoger, destilar y mezclar | ★ la 1ª y la calidad del lote · ★★ dónde y cuándo aparece, y la 2ª · ★★★ la 3ª · ★★★★ la 4ª y qué lo potencia | Tiempo |
| 💰 **Comprar la información** | Un **herbario** (copia de expediente hecha con Inscripción), la Biblioteca pública o un informante | Hasta ★★: las dos primeras. **Lo que se lee no reemplaza lo que se prueba** (la misma regla que en la medicina) | Oro |

- **Las propiedades son fijas** para cada ingrediente en todo el servidor. Lo que se descubre vale para siempre y se puede vender.
- **Una receta comprada no enseña propiedades.** Quien compra la receta de un elixir puede fabricarlo, pero no sabe por qué funciona (§5.4).

## 4. Qué puede tener un elixir

### 4.1 Catálogo de efectos

**Valor base** es lo que da el efecto en un elixir de **un solo efecto**, con ingredientes de potencia 100 y calidad Notable. **Tope** es el máximo absoluto, con cualquier calidad y cualquier ingrediente. **Toxicidad** es lo que suma el efecto con su valor base (la cuenta completa está en §6.7).

**❤️ Curación de vida**

| Efecto | Propiedad | Valor base | Tope | Duración | Toxicidad |
|---|---|---|---|---|---|
| ❤️ **Curación** | Cicatrizante | 35 % de la vida máxima (igual que la poción de vida) | 40 % | Al instante | 40 |
| 💗 **Regeneración** | Renovadora | 5 % de la vida máxima por ronda | 6 % por ronda | 4 rondas (fuera de combate: 1 minuto) | 30 |

**💊 Curación de estados** (ver [Daño y estados](../04-combate/dano-y-estados.md) §2). Vaciar la barra y cortar el daño por ronda pasa con cualquier potencia; la potencia decide la **protección posterior**: durante 3 rondas, la barra de ese estado se llena más despacio.

| Efecto | Propiedad | Qué hace siempre | Protección (valor base) | Tope | Toxicidad |
|---|---|---|---|---|---|
| 🟢 **Antídoto** | Purificante | Vacía la barra de Veneno y corta su daño | −50 % de acumulación | −60 % | 20 |
| 🩸 **Coagulante** | Coagulante | Vacía la barra de Sangrado y corta su daño | −50 % | −60 % | 15 |
| 🔥 **Bálsamo** | Emoliente | Vacía la barra de Quemadura y corta su daño | −50 % | −60 % | 15 |
| ❄️ **Calor interno** | Cálida | Vacía la barra de Congelación. Fuera de combate: +1 de abrigo durante 20 pasos | −50 % | −60 % / 30 pasos | 15 |

La Podredumbre, la Locura y la Maldición **no** se curan con elixires propios: piden su remedio propio o una habilidad (ver [Daño y estados](../04-combate/dano-y-estados.md) §2).

**🔋 Recuperación**

| Efecto | Propiedad | Valor base | Tope | Toxicidad |
|---|---|---|---|---|
| 🔋 **Aguante** 🔁 | Vivificante | +1 ficha de Aguante | +2 (solo Excelente u Obra Maestra, y solo como único efecto) | 25 |
| 🔷 **Recurso** | Resonante | +30 % del recurso de clase (maná y similares) | 35 % | 30 |

**🛡 Resistencias** (al elemento y al entorno; ver [Peligros del entorno](../05-salud/peligros-del-entorno.md))

| Efecto | Propiedad | Valor base | Tope | Duración | Toxicidad |
|---|---|---|---|---|---|
| 🔥 **Resistencia al fuego** | Ignífuga | −30 % de daño de fuego; menos quemaduras por lava | −35 % | 3 rondas | 25 |
| ❄️ **Resistencia a la escarcha** | Aislante | −30 % de daño de escarcha | −35 % | 3 rondas | 25 |
| ⚡ **Resistencia al rayo** | Terrosa | −30 % de daño de rayo; el rayo de tormenta no salta a ti | −35 % | 3 rondas | 25 |
| 🌑 **Resistencia a la sombra** | Luminosa | −30 % de daño de sombra y la mitad del estrés que suma | −35 % | 3 rondas | 25 |
| ☀️ **Frescor** (contra el calor) | Fría | +1 de frescor fuera de combate; en combate anula el castigo de calor al Aguante | Igual | 20 pasos / 3 rondas (tope: 30 pasos / 4 rondas) | 15 |
| 💧 **Sales** (contra la sed) | Mineral | Baja una etapa de sed, además del trago | Dos etapas | Al instante | 5 |
| ☣️ **Pulmón limpio** (contra la contaminación) | Pulmonar | −20 de Contaminación y +1 de filtro | −30 y +1 | 20 pasos | 15 |

**⚔️ Ventajas temporales**

| Efecto | Propiedad | Valor base | Tope | Duración | Toxicidad |
|---|---|---|---|---|---|
| ⚡ **Iniciativa** 🔁 | Despertadora | +15 % de iniciativa | +20 % | 3 rondas | 25 |
| 🎯 **Precisión** | Aguda | +10 % de precisión | +12 % | 3 rondas | 25 |
| 🛡 **Protección de zona** | Pétrea | +20 % de armadura en **una** parte del cuerpo (cabeza, torso, brazos o piernas), que se elige al destilar y queda en la receta | +25 % | 5 rondas | 20 |

La **regeneración por ronda** es la 💗 Regeneración de la tabla de curación de vida.

**⛏️ Efectos de oficio** (fuera de combate)

| Efecto | Propiedad | Valor base | Tope | Duración | Toxicidad |
|---|---|---|---|---|---|
| ⛏️ **Rendimiento** | Creciente | +10 % de rendimiento al recolectar o cosechar. **No** se aplica a los materiales 🌙 ni ⭐ | +15 % | 1 hora real | 10 |

**✨ Efectos raros**

| Efecto | Propiedad | Valor base | Tope | Duración | Toxicidad |
|---|---|---|---|---|---|
| 👁 **Visión nocturna** | Sombría | Sin castigo en penumbra ni en oscuridad; en oscuridad total, el castigo baja de −40 % a −15 % | Igual | 30 pasos / 10 rondas | 15 |
| 🫧 **Respirar bajo el agua** | Acuática | Aire sin límite | 15 pasos | 10 pasos | 15 |
| 🧠 **Calma** 🔁 | Calmante | −15 de estrés (ver [Mente](../05-salud/mente.md)) | −20 | Al instante | 20 |
| 💊 **Analgesia** 🔁 | Sedante | −1 nivel de Dolor (ver [Condiciones](../05-salud/condiciones.md) §1) | −2 niveles | 1 hora real | 20 |

🔁 = genera tolerancia y puede traer dependencia (§6.8).

### 4.2 Efectos secundarios

Salen de las propiedades **negativas** que comparten dos o más ingredientes. No cuentan para el límite de efectos.

| Secundario | Propiedad | En combate | Fuera de combate |
|---|---|---|---|
| 🤢 **Náusea** | Amarga | La próxima comida o poción rinde la mitad durante 3 rondas | La comida no sube el Sustento durante 10 minutos |
| 🫨 **Temblor** | Nerviosa | −8 % de precisión durante 3 rondas | La condición del próximo minijuego de fabricación empieza en Pobre |
| 😴 **Somnolencia** | Adormecedora | −10 % de iniciativa durante 3 rondas | +1 nivel de Fatiga durante 30 minutos |
| ☠️ **Más toxicidad** | Tóxica | +15 de Toxicidad | +15 de Toxicidad |

**Quitar un secundario** pide la técnica *Destilado limpio* (escalón I de la Alquimia, ver [Escalera de conocimiento](escalera-de-conocimiento.md) §3.3): un paso más del minijuego que borra **un** secundario y gasta durabilidad. Los alquimistas novatos venden elixires con náusea más baratos; los buenos, limpios.

## 5. Crear un elixir propio

### 5.1 El alambique

- Es la estación de la Alquimia (ver [Fabricación](fabricacion.md) §6): hay alambiques públicos en los asentamientos (con tasa de uso), en las casas y en los salones de gremio. La capital con especialidad en alquimia devuelve más material.
- El alambique tiene **anillo (T1 a T10) y calidad**, como cualquier herramienta: uno mejor da más durabilidad en el minijuego.
- **Una mezcla lleva de 2 a 4 ingredientes**, una unidad de cada uno por tanda. Una tanda da 3 elixires; con alambique de calidad alta, 4.

### 5.2 Cómo se forma la mezcla

1. **Se eligen los ingredientes.** El alambique muestra las propiedades que conoces de cada uno.
2. **Se calculan las compartidas.** Cada propiedad de efecto o negativa que aparece en dos o más ingredientes entra en el elixir. Si no conoces la propiedad en alguno de ellos, aparece como *"❔ algo en común (2·3)"*.
3. **Se aplica el límite del rango** (§6.1). Si salen más efectos de los que tu rango permite, **eliges cuáles quedan**. Los secundarios no se eligen: vienen con la mezcla.
4. **Se aplican las modificadoras** (Pura, Dulce, Conservante, Pegajosa, Salvaje).
5. **Se juega el minijuego** (§5.3) o se resuelve en modo rápido.
6. **Al embotellar** se revelan las propiedades ❔. Si con eso hay más efectos de los que permite tu rango, eliges cuál cambiar. Si la combinación es nueva, el alquimista le pone nombre (§5.4).

**El orden importa** (como en *Kingdom Come*). Cada receta registrada guarda el orden en que entraron los ingredientes y las acciones clave del minijuego. Repetir la receta tal cual asegura la misma calidad mínima; cambiar el orden puede mejorarla o arruinarla.

### 5.3 El minijuego del alambique

Es el minijuego de [Fabricación](fabricacion.md) §2 (estilo *Final Fantasy XIV*) en una versión **corta**: de 4 a 8 pasos y **4 botones**, para cumplir D-75. Tiene dos barras de resultado:

- **Calidad** → la **potencia**: Normal ×0,85 · Buena ×0,95 · Notable ×1 · Excelente ×1,1 · Obra Maestra ×1,2.
- **Estabilidad** → **cuánto dura fresco** (§6.9): Baja, Media o Alta.

Y las de siempre: **Progreso**, **Durabilidad**, **PA** y la **Condición**, que cambia en cada paso.

| Botón | Efecto | Costo |
|---|---|---|
| 🔥 **Calentar** | +Progreso | Durabilidad |
| 🥄 **Remover** | +Calidad. Con condición ✨ Excelente, el botón pasa a ser ⚗️ **Destilar**: convierte Progreso en Calidad, el doble | Durabilidad y pocos PA (Destilar: más PA) |
| 💧 **Enfriar** | +Estabilidad y un poco de Progreso | PA |
| 🍾 **Embotellar** | Termina. Si el Progreso no está lleno, la calidad baja un nivel | — |

- **Sin botón de Observar.** Con el expediente de la familia "elixires" en ★★★, la pantalla muestra también la condición del paso siguiente.
- **Las técnicas de la escalera no suman botones:** ocupan uno cuando se pueden usar. *Destilado limpio* (I) aparece en lugar de 💧 Enfriar mientras la mezcla tenga un secundario. *Maceración larga* (II): al tocar 🍾 Embotellar, el bot pregunta si embotellar ya o dejar reposar la mezcla de 2 a 12 horas reales, que sube la Calidad sin gastar durabilidad. *Transmutación menor* (IV) se usa antes de empezar: cambia **una** propiedad de un ingrediente por otra de su familia (por ejemplo, Fría por Aislante), una vez por mezcla.
- Si la durabilidad llega a 0 antes de embotellar, se pierden los ingredientes. Lo descubierto en esa prueba **no** se pierde.
- **Modo rápido:** un toque. El resultado sale de tu rango, tu Maestría en Elixires y la calidad de los lotes. **Techo: Notable**, como toda fabricación rápida.

### 5.4 El nombre y la receta

- **Si la combinación de ingredientes no existe en el servidor**, el alquimista le pone nombre (hasta 32 letras, escrito como mensaje y con el filtro de palabras de [Seguridad](../01-plataforma/seguridad-y-anti-trampas.md)). El bot le suma *"de [nombre del alquimista]"*: *"Aliento de Brasa de Ilse"*. La Gaceta anuncia el primer elixir nuevo de cada semana.
- **La receta queda registrada a su nombre**: ingredientes, orden, efectos elegidos y la parte del cuerpo de la Protección de zona, si la tiene.
- **Si la combinación ya existe**, el elixir lleva el nombre de quien la registró primero, y el alambique lo dice: *"Ya existe: Aliento de Brasa de Ilse (patentada)"*. Si era un secreto de taller y llegaste a ella por tu cuenta, la puedes fabricar sin pagar (así funciona el secreto, ver abajo).
- **Qué se puede hacer con la receta** (ver [Investigación y maestría](investigacion-y-maestria.md) §8 y §9):

| Opción | Qué pasa |
|---|---|
| ⚖️ **Patentar** | Se publica en el Registro de patentes: cualquiera puede aprenderla y paga una regalía (del 1 % al 10 % del precio de referencia) cada vez que la fabrica, durante 12 semanas, renovables una vez por 6. Después es pública. Cuesta 20 PI y 200 de oro, con un máximo de 5 patentes activas por personaje |
| 🔒 **Secreto de taller** | Solo la fabricas tú. Otro puede llegar a la misma combinación probando; si lo logra, la fabrica sin pagarte |
| 📖 **Publicar gratis** | Pasa a la Biblioteca pública. Da prestigio y Saber a tu ciudad |
| 📜 **Vender copias** | Copia de receta con usos limitados, hecha con Inscripción. Quien la compra la fabrica, pero no aprende las propiedades |
| 🎓 **Enseñar** | A tus aprendices, o en un recetario escrito con Inscripción (ver [Investigación y maestría](investigacion-y-maestria.md) §9) |

- **Etiqueta:** cada frasco lleva el nombre, la calidad, la firma del alquimista y los días que le quedan fresco. Las Obras Maestras van al registro público de obras maestras (ver [Fabricación](fabricacion.md) §8).

## 6. Límites de balance

**La idea.** Un elixir de varios efectos **ahorra rondas y casillas**, no suma poder. Beberlo tiene que valer algo menos que beber por separado las pociones de cada efecto: lo que se gana es la ronda y la casilla, y se paga con potencia y Toxicidad. Así no se rompe el presupuesto de poder de cada spec (ver [Balance](../03-personaje/balance.md) §2, y D-49): los consumibles están **fuera** de los 100 puntos de la spec, y por eso tienen techo propio.

### 6.1 Efectos por rango

| Rango de Alquimia | Niveles | Efectos por elixir | Además |
|---|---|---|---|
| Aprendiz | 1-20 | 1 | Recetas de entrenador; descubre propiedades |
| Oficial | 21-40 | 1 | Usa las modificadoras; técnica *Destilado limpio* |
| Experto | 41-60 | 2 | Primer elixir con nombre de dos efectos |
| Artesano | 61-80 | 2 | Más techo de calidad en el minijuego |
| Maestro | 81-95 | 3 | Obras Maestras |
| Gran Maestro | 96-100 | 3 | Firma dorada |
| Gran Maestro con M10 en Elixires | 100 y Maestría 10 | **4**, si el cuarto es de oficio o de entorno (Rendimiento, Frescor, Sales, Pulmón limpio, Visión nocturna, Respirar bajo el agua) | El cuarto efecto nunca es de combate |

**El límite vale también para fabricar.** Una receta comprada, con licencia o aprendida de un maestro pide el rango que permite sus efectos: un Experto no fabrica un elixir de tres efectos aunque tenga la receta. Lo puede comprar ya hecho y beberlo, eso sí.

### 6.2 El reparto de la potencia

Cuantos más efectos, menos rinde cada uno:

| Efectos | Potencia de cada uno | Total |
|---|---|---|
| 1 | 100 % | 100 % |
| 2 | 65 % | 130 % |
| 3 | 50 % | 150 % |
| 4 | 40 % | 160 % |

El total sube un poco para que valga la pena combinar, pero la **curación al instante** de un elixir de tres efectos nunca llega a la de una poción de vida sola (como máximo 35 % × 0,5 × 1,3 = 23 %). Si suma Regeneración, el total puede igualarla, pero repartido en 4 rondas y siempre bajo el tope de §6.4.

### 6.3 La potencia final

**Potencia de cada efecto** = valor base × reparto × calidad × lotes × Salvaje.

- El multiplicador de calidad × lotes × Salvaje **nunca pasa de ×1,3**.
- Después de la cuenta manda el **tope** de cada efecto (§4.1).
- **Efectos fijos.** Lo que no se puede partir (+1 ficha de Aguante, una etapa de sed, un nivel de Dolor, el aire sin límite, quitar el castigo de la oscuridad, vaciar la barra de un estado) se da **entero**. En ellos, la potencia mueve solo la duración o la protección posterior, y nunca baja de 1 ronda o 5 pasos. Para que no salgan gratis, la Toxicidad de **Aguante, Sales y Analgesia** entra entera en la cuenta de §6.7, sin reparto.

### 6.4 Topes

- **Por efecto:** cada efecto tiene su tope en §4.1, y **ningún elixir lo pasa**, con cualquier calidad, Maestría o ingrediente de yacimiento único.
- **Curación total por elixir: 40 % de la vida máxima**, sumando la curación al instante y la regeneración completa. Es el mismo número del tope de golpe en PvP (ver [Ronda y acciones](../04-combate/ronda-y-acciones.md) §11), así que un elixir nunca deshace más de un golpe máximo.
- Los topes se revisan con el resto del balance y se anotan en el registro de balance.

### 6.5 Lo mismo no se acumula

- **Un mismo efecto no se suma con otro consumible.** Si bebes un elixir con 🔥 Resistencia al fuego y ya tienes activa otra resistencia al fuego (de poción o de elixir), queda la más fuerte y se renueva la duración.
- Los efectos **distintos** sí conviven: un elixir con Regeneración y una poción de Resistencia al fuego valen a la vez.
- **Con las habilidades de clase sí se suman**, porque esas ya están dentro del presupuesto de la spec.

### 6.6 Un elixir por ronda

Usar un elixir gasta tu elección de la ronda, como cualquier objeto del cinturón (D-46). Ningún efecto da una acción extra.

### 6.7 Toxicidad: crece con cada efecto y con la potencia

Cada elixir suma Toxicidad (ver [Condiciones](../05-salud/condiciones.md) §4: por encima de 75 se pierde vida, y si un trago la llevaría por encima de 100, no se puede beber).

**Toxicidad del elixir** = (suma de la Toxicidad de cada efecto) × reparto × calidad × lotes × Salvaje · + 5 por cada efecto después del primero · + 15 si tiene el secundario ☠️ · − 5 por cada ingrediente Dulce (hasta −10) · mínimo 10 · se redondea hacia abajo. Aguante, Sales y Analgesia suman su Toxicidad entera, fuera del reparto (§6.3).

**Las rebajas tienen techo.** La Dulce y la *Farmacología* juntas bajan como máximo un **15 %** la Toxicidad del elixir. Sin ese techo, una poción de vida casera con dos ingredientes Dulce (35 % por 30 de Toxicidad) dejaría beber tres por pelea en lugar de dos: un 50 % más de curación por pelea. Con el techo queda en 34, y tres ya no caben.

| Ejemplo | Cuenta | Toxicidad |
|---|---|---|
| Poción de vida (1 efecto, Notable) | 40 × 1 | **40** |
| Curación + Antídoto (2 efectos, Notable) | (40 + 20) × 0,65 + 5 | **44** |
| Curación + Regeneración + Resistencia al fuego, con Dulce (Notable) | (40 + 30 + 25) × 0,5 + 10 − 5 | **52** |
| Iniciativa + Precisión, con el secundario ☠️ (Notable) | (25 + 25) × 0,65 + 5 + 15 | **52** |
| El mismo de tres efectos, Excelente y con Salvaje (§10) | (40 + 30 + 25) × 0,5 × 1,27 + 10 − 5 | **65** |

**Por qué la potencia también sube la Toxicidad.** La Toxicidad es el **presupuesto de la pelea**: con 100 de tope, nadie toma más de dos o tres tragos fuertes por combate. Si la calidad subiera la potencia sin subir la Toxicidad, el mejor alquimista daría más curación por pelea, y eso sí rompería el balance. Así, la calidad decide **cuánto rinde cada ronda** (menos rondas gastadas en beber), no cuánto rinde la pelea entera.

**Por qué un elixir de varios efectos no es mejor que las pociones sueltas.** Tres pociones de un efecto dan el 300 % de efecto por 95 de Toxicidad; el elixir de tres efectos da el 150 % por 57 (52 con un ingrediente Dulce). Rinde algo menos por cada punto de Toxicidad, y a cambio ahorra dos rondas y dos casillas.

La técnica combinada *Farmacología* (Medicina + Alquimia, ver [Investigación y maestría](investigacion-y-maestria.md) §3) baja un 10 % la Toxicidad de los elixires que fabricas, dentro del techo de rebajas del 15 %.

### 6.8 Tolerancia y dependencia

Los efectos marcados 🔁 (Aguante, Iniciativa, Calma, Analgesia) generan **tolerancia**, como dice [Condiciones](../05-salud/condiciones.md) §4:

- Cada uso del mismo efecto en 24 horas reales rinde un 10 % menos (hasta −40 %). Un ingrediente Salvaje duplica la tolerancia que suma.
- **Dependencia:** más de 6 usos del mismo efecto 🔁 en 3 días reales. Trae **abstinencia** de ese efecto: −5 % de iniciativa y +10 de estrés al día, hasta que pasan 2 días sin usarlo o hasta que un médico la trata (ver [Curación](../05-salud/curacion-y-tratamientos.md)).
- **Siempre con aviso:** al quinto uso, el bot dice *"⚠️ Tu cuerpo se acostumbra al Aliento Rápido. Uno más y vas a depender de él."*
- La tolerancia baja sola con el tiempo, también sin conectarse.

### 6.9 Caducidad

Los elixires **caducan**, como los remedios (ver [Curación](../05-salud/curacion-y-tratamientos.md) §8). Eso mantiene viva la demanda y evita que alguien guarde mil frascos de una buena semana.

| Estabilidad | Días fresco (rinde 100 %) | Después |
|---|---|---|
| Baja | 5 días reales | −5 % de potencia por día, hasta el 60 %. A los 15 días queda **pasado**: solo da sus secundarios y su Toxicidad |
| Media | 10 días | Igual |
| Alta | 20 días | Igual |

- **Conservante** suma la mitad de días fresco. Un **frasco de vidrio de duna** (Joyería) suma 5 días; uno de **cristal tallado**, 10.
- Las **pociones de entrenador** (poción de vida, resistencias básicas, remedios comunes) duran 30 días frescas.
- Lo que está en el cinturón caduca igual que lo de la mochila. En la despensa de una casa (ver [Casa propia](../09-construccion/casa-propia.md)) los días cuentan a la mitad.

### 6.10 PvP: arena, guerra y mundo abierto

| Dónde | Qué vale | Por qué |
|---|---|---|
| 🏟️ **Arena clasificada** | **Solo la lista normalizada.** El cinturón de arena es igual para todos (ver [Ronda y acciones](../04-combate/ronda-y-acciones.md) §11): poción de vida, una poción de resistencia a elección, un remedio de estados y una poción de recurso, todos a calidad Notable. **Ningún elixir propio** | En la clasificatoria decide la habilidad, igual que con el equipo normalizado (ver [PvP](../06-contenido/pvp.md) §5). Si entraran los elixires propios, ganaría quien tiene al mejor alquimista |
| 🏰 **Guerra de castillos, asedios y territorios** | Elixires propios con **potencia de guerra:** como máximo **2 efectos**, calculados a calidad Notable, lotes 100 y sin Salvaje (multiplicador ×1). Un elixir de más efectos se puede llevar, pero en la batalla rinde como un elixir de solo sus 2 primeros efectos (reparto 65 %, con su Toxicidad calculada igual) | La guerra premia la preparación y la economía del gremio, y el alquimista del castillo es parte del ejército. El tope impide que la gane solo quien tiene más oro para Obras Maestras |
| ⚔️ **Mundo abierto y zonas rojas y negras** | Todo, como en PvE | Prepararse para la zona es parte del riesgo. Ya rigen el **tope de golpe del 40 %** y la **amortiguación de curación** desde la ronda 8, que también se aplica a la curación de los elixires |

## 7. En combate

### 7.1 Desde la 🎒 Mochila

- Los elixires van en el **cinturón** (ver [Inventario y mochilas](../03-personaje/inventario-y-mochilas.md) §4): una casilla por elixir del mismo nombre y calidad, hasta 3 unidades. El cinturón tiene de 3 a 6 casillas.
- **Usarlo gasta la elección de la ronda** y se resuelve primero, antes de los golpes, como cualquier objeto (ver [Ronda y acciones](../04-combate/ronda-y-acciones.md) §4 y §6). Por eso un elixir con Resistencia al fuego contesta un aliento avisado.
- La Mochila muestra **3 objetos por página** (D-75). Con 3 objetos o menos, el cuarto botón es ↩️ Volver, como ya hace el código. Con más, el cuarto botón pasa a ser "▶️ Ver más" y ↩️ Volver queda en la última página; **esto falta en el código**, que hoy muestra solo las 3 primeras casillas y deja las demás sin botón. El jugador ordena su cinturón: las tres primeras casillas son las que salen primero.
- Las **configuraciones guardadas** del cinturón ("solitario", "mazmorra", "PvP") recuerdan qué elixires lleva cada una.

### 7.2 Cómo se ve

Ronda 3 contra la Salamandra Madre. Avisa un aliento de fuego, y el Guerrero Furia ya tiene la barra de Quemadura por la mitad:

```
⚔️ Ronda 3 · Salamandra Madre (jefa de campo)
⚠️ Toma aire: ALIENTO DE FUEGO a toda la vanguardia
   en esta ronda.

🟥 Tú — 💢 Guerrero Furia · Vanguardia
❤️ 540/1.120   💢 Ira 30   🔋 ●●○○○
🔥▓▓▓▓▓▓░░░░ Quemadura
☠️ Toxicidad 0/100
⏱ 45 s

[⚔️ Atacar]        [✨ Golpe Colosal]
[🤺 Parada]        [✨ Ejecutar]
[🏃 Huir]          [🎒 Mochila]
```

Toca 🎒 **Mochila**:

```
🎒 Cinturón (5 casillas) · ☠️ Toxicidad 0/100

1. 🍷 Aliento de Brasa de Ilse ×1 · Excelente
   ❤️ 22 % · 💗 3 %×4 · 🔥 −19 % ×3 · ☠️ 65
2. 🧪 Poción de vida ×2 · ❤️ 35 % · ☠️ 40
3. 💊 Ungüento para quemaduras ×2 · ☠️ 15
4. 🩹 Venda ×3
5. —

[🍷 Aliento ×1]   [🧪 Vida ×2]
[💊 Ungüento ×2]  [▶️ Ver más]
```

"▶️ Ver más" lleva a la venda y a "↩️ Volver". Elige el **Aliento de Brasa**: con una sola ronda se cura, se protege del aliento y empieza a regenerar. No le vacía la barra de Quemadura: para eso haría falta el ungüento, otra ronda.

```
📜 Ronda 3
🍷 Bebes Aliento de Brasa de Ilse:
   ❤️ +249 · 💗 +36 por ronda (4 rondas)
   🔥 −19 % de fuego (3 rondas)
🔥 La Salamandra Madre lanza ALIENTO DE FUEGO: −248 (−19 %)
   🔥▓▓▓▓▓▓▓▓░░ Quemadura
⚔️ Bram (Protección) golpea con el escudo: −160
💗 Regeneras +36
❤️ 577/1.120 · ☠️ Toxicidad 65/100
```

Con 65 de Toxicidad ya no le cabe otra poción de vida (65 + 40 pasa de 100). Sí le cabe el ungüento (15), pero con 80 empezaría a perder vida. La Toxicidad sigue siendo el freno.

### 7.3 Elixires y roles (D-50)

Cada clase tiene specs de **Ataque, Defensa, Curación y Soporte**, y cada una cumple su papel en el grupo. Los elixires ayudan a todos, sobre todo en solitario, pero **no convierten a nadie en otro rol**:

- **Solo afectan a quien los bebe.** No se le dan a un aliado en combate. Curar y proteger a otros sigue siendo el trabajo de los specs de Curación, Defensa y Soporte.
- **Un elixir cura como máximo el 40 % de la vida, y la Toxicidad deja dos o tres tragos por pelea.** Un sanador cura cada ronda.
- **Ningún efecto provoca, cubre una fila ni potencia al grupo.** Eso es de los specs de Defensa y Soporte.
- **Las bombas y los frascos lanzables** (Alquimia e Ingeniería) son otra cosa: se lanzan, hacen daño o dejan una superficie, y tienen su propio máximo de 3 por pelea (ver [Mecánicas avanzadas](../04-combate/mecanicas-avanzadas.md)).

## 8. Fuera de combate

### 8.1 Expediciones

Los elixires de entorno son los que más se venden a exploradores, caravanas y gremios que cruzan terrenos duros (ver [Peligros del entorno](../05-salud/peligros-del-entorno.md) §7.2). Un elixir de varios efectos ahorra peso y casillas en la mochila, y un solo trago en lugar de tres.

| Elixir de ejemplo | Efectos | Para |
|---|---|---|
| *Trago de Caravana* (Experto) | 💧 Sales · ☀️ Frescor | Cruzar el desierto de día |
| *Aliento de Cumbre* (Experto) | ❄️ Calor interno · ☣️ Pulmón limpio | Minas altas con gas y frío |
| *Ojo de Ciénaga* (Maestro) | 👁 Visión nocturna · 🟢 Antídoto · ☣️ Pulmón limpio | Pantano de noche, con miasma y sapos venenosos |
| *Buzo de Arrecife* (Gran Maestro, M10) | 🔥 Bálsamo · 🫧 Respirar bajo el agua · 💧 Sales · ☀️ Frescor | Bucear de día en costas cálidas, entre corales que queman. Sale de Alga de costa, Glándula de sapo, Pulpa de cactus y Lágrima helada |

### 8.2 Oficios

- **Rendimiento** (Creciente) sube lo que se saca al recolectar o cosechar, durante una hora real. Nunca multiplica los materiales 🌙 ni ⭐, igual que el acelerador.
- **Analgesia** deja trabajar con una herida leve sin que el Dolor estropee el minijuego.
- **Frescor** y **Calor interno** sirven al minero de la montaña y al herrero junto a la forja.

### 8.3 La investigación médica

La Alquimia y la Medicina comparten los ingredientes y el vocabulario de propiedades:

- Los **remedios** que salen de la [Investigación médica](../05-salud/investigacion-medica.md) (febrífugos, antitoxinas, sueros) los fabrica en cantidad un alquimista que tenga la receta del protocolo.
- Lo que el alquimista descubre de un ingrediente **le sirve al médico**: el expediente del ingrediente es el mismo para los dos oficios (si el dueño lo confirma, §12).
- La técnica combinada *Farmacología* (Medicina + Alquimia) da dosis con menos Toxicidad y remedios de liberación lenta (ver [Investigación y maestría](investigacion-y-maestria.md) §3).
- El médico trata la **intoxicación** y la **dependencia** de elixires (ver [Curación](../05-salud/curacion-y-tratamientos.md)).

## 9. Economía y roles

| Rol | Cómo gana | Con qué |
|---|---|---|
| **Alquimista con fama** | Su elixir con nombre se pide por su nombre ("para el Ojo de Ciénaga, ve con Mara"). Vende en su puesto o en una **botica** propia (ver [Propiedad y concesiones](propiedad-y-concesiones.md)), cobra regalías por sus patentes y vende copias de receta | Alquimia, Maestría, patentes |
| **Herborista** | Abastece de hierbas y flores en sazón; los lotes de potencia alta valen el doble | Herboristería, el calendario de floraciones |
| **Cazador proveedor** | Glándulas, escamas y ojos de monstruo, por encargo | Desuello, [Cacerías](../06-contenido/cacerias.md) |
| **Minero y aguador** | Carbón, ámbar, sales, aguas especiales | Minería, exploración |
| **Joyero** | Frascos de vidrio de duna y de cristal tallado, que alargan la frescura | Joyería |
| **Escriba e informante** | Herbarios (copias de expediente) y notas de dónde y cuándo aparece cada ingrediente | Inscripción |
| **Médico** | Trata la dependencia y la intoxicación; compra remedios al por mayor | Medicina |

**Demanda por estación** (ver [Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md) §4):
- **Invierno:** suben el Calor interno y el Pulmón limpio; escasean las hierbas, y quien guardó hierbas conservadas cobra caro. Llegan el Musgo de Cumbre Blanca y el Ojo de lince.
- **Primavera:** llega la mandrágora; suben la Analgesia y la Calma.
- **Verano:** suben el Frescor y las Sales; se juntan escamas de salamandra y agua del Oasis Hondo.
- **Otoño:** Flor de Ciénaga y Miel negra; el festival de difuntos trae el único Polen del año.

**Sumideros.** La tasa del alambique público, la regalía de patente (con su impuesto), los frascos que se rompen, los elixires que caducan y las pruebas que fallan: todo saca oro y materiales del juego (ver [Economía](economia.md)).

## 10. Cómo se ve en el alambique

**Mezclar.** Ilse, alquimista Maestra (Alquimia 84), prueba tres ingredientes para la cacería de la Salamandra Madre:

```
⚗️ Alambique · Casa de Ilse (Alquimia 84 · Maestra)

Ingredientes (3/4):
 1. 🍯 Miel negra · pot. 112 🌙
 2. 🦎 Escama de salamandra en muda · pot. 104 🌙
 3. 🌋 Flor de Ceniza · pot. 100

Comparten:
 ✅ Cicatrizante (1·3) → ❤️ Curación
 ✅ Renovadora (1·2)   → 💗 Regeneración
 ✅ Ignífuga (2·3)     → 🔥 Resistencia al fuego
 ❔ algo en común (2·3)
Modificadoras: 🍬 Dulce (−5 ☠️) · 🐾 Salvaje (×1,1, −estabilidad)
Secundarios: ninguno
Toxicidad estimada: 59 si sale Notable

[🔥 Empezar]        [⚡ Rápido (Notable)]
[➕ Ingrediente]    [▶️ Ver más]
```

"▶️ Ver más" tiene ➖ Quitar uno, 📜 Recetas y ↩️ Volver.

**El minijuego.** Paso 4 de 6:

```
⚗️ Mezcla nueva · paso 4
Progreso    ▓▓▓▓▓▓▓░░░  70 %
Calidad     ▓▓▓▓▓▓░░░░  → Notable
Estabilidad ▓▓▓▓░░░░░░  Media
Durabilidad ●●○○   PA 96/240
Condición: ✨ EXCELENTE · siguiente: Normal

[🔥 Calentar]   [⚗️ Destilar ×2]
[💧 Enfriar]    [🍾 Embotellar]
```

Con la condición Excelente, 🥄 Remover pasó a ser ⚗️ Destilar. Ilse destila, la Calidad salta a Excelente, calienta una vez más y embotella.

**El resultado.** Al embotellar se revela la propiedad ❔: la Flor de Ceniza también es Cálida, que daría ❄️ Calor interno. Como Ilse es Maestra y ya tiene tres efectos, el bot le pregunta si quiere cambiar alguno; ella se queda con los tres de combate.

```
✨ ¡Elixir nuevo! Nadie en el servidor lo había hecho.

🍷 ×3 · Calidad: Excelente · Estabilidad: Media
   (fresco 10 días)
❤️ Curación 22 % · 💗 Regeneración 3 %/ronda ×4
🔥 Resistencia al fuego −19 % ×3 rondas
☠️ Toxicidad 65
🔎 Descubriste: Flor de Ceniza → Cálida

✍️ Escribe su nombre (hasta 32 letras):
> Aliento de Brasa

📜 Registrado: «Aliento de Brasa de Ilse»
[⚖️ Patentar]        [🔒 Secreto de taller]
[📖 Publicar gratis] [▶️ Ver más]
```

"▶️ Ver más" tiene 📜 Vender copias y 🔍 Ver receta.

**Las cuentas.** Tres efectos: 50 % de potencia cada uno. Calidad Excelente ×1,1, lotes ×1,05 (promedio 105) y Salvaje ×1,1: ×1,27, por debajo del máximo de ×1,3. Cada efecto rinde 0,5 × 1,27 = 0,635 de su valor base. Curación 35 % × 0,635 = 22 %. Regeneración 5 % × 0,635 = 3,2 % por ronda. Fuego −30 % × 0,635 = −19 %. Curación total: 22 % + 4 × 3,2 % = 35 %, debajo del tope de 40 %. Toxicidad: (40 + 30 + 25) × 0,5 × 1,27 = 60, + 10 por los dos efectos extra, − 5 por la Miel (Dulce) = **65**.

**Lo más simple.** Un Aprendiz junta Hierba curativa y Cardo rojo. Comparten solo Cicatrizante: sale una poción de vida casera de un efecto. La Amarga de la hierba y la Nerviosa del cardo no se cruzan, así que no hay secundarios.

## 11. Su fila en la red de sistemas

Como pide la [Red de sistemas](../00-vision/red-de-sistemas.md) §3:

| Sistema | Consume (entradas) | Produce (salidas) | Depende del farmeo | Depende de la fabricación | Depende de la progresión |
|---|---|---|---|---|---|
| **Alquimia y elixires** | Ingredientes (hierbas, hongos, partes de monstruo, minerales, aguas especiales), frascos, alambiques, tasas de uso, PI para patentes y técnicas | Pociones, elixires con nombre, remedios de protocolo, recetas, copias y patentes, demanda de ingredientes de temporada, pacientes con dependencia o intoxicación | Herboristería, Desuello y caza, Minería, Pesca, Agricultura (cultivo de micelio y de hierbas) | Alambique (Herrería e Ingeniería), frascos (Joyería), herbarios y copias (Inscripción), cinturones (Peletería) | Rango de Alquimia (efectos por elixir), expedientes de ingrediente, técnicas de la escalera, Maestría en Elixires |

## 12. Preguntas para el dueño

Propuestas para numerar en [Preguntas abiertas](../00-vision/preguntas-abiertas.md) con el siguiente número libre:

| Pregunta | Recomendación |
|---|---|
| ¿Cuántos efectos como máximo en un elixir? | 1 de Aprendiz a 3 de Gran Maestro, y un 4º solo de oficio o de entorno con M10. Más efectos en una ronda serían demasiado fuertes |
| ¿Los elixires propios entran en la arena clasificada? | No: solo la lista normalizada. En la guerra de castillos sí, con potencia de guerra (2 efectos a calidad Notable) |
| ¿La calidad del elixir también sube la Toxicidad? | Sí, en la misma proporción. Así la Toxicidad sigue siendo el presupuesto de la pelea y la calidad solo ahorra rondas |
| ¿Un elixir se le puede dar a un aliado en combate? | No. Así no reemplaza a los sanadores ni a los soportes |
| ¿Cuánto duran frescos? | De 5 a 20 días según la estabilidad; las pociones de entrenador, 30 |
| ¿El expediente de un ingrediente es el mismo para el alquimista y para el médico? | Sí: un solo expediente por ingrediente, que llenan los dos oficios |
| ¿Dos jugadores pueden registrar con nombres distintos la misma combinación? | No: la combinación tiene un solo nombre, el de quien la registró primero. Las variantes de calidad o de orden no cuentan como receta nueva |

## 13. Orden de construcción sugerido

La alquimia entra en el juego como un parche de contenido nuevo (D-60, avisado a todos según D-67). Mientras se ajusta la misma alquimia, los cambios son subparches de ese parche (D-73).

1. **Primero:** ingredientes con 4 propiedades, la regla de compartir y el modo rápido con 1 efecto. La poción de vida (35 %, Toxicidad 40) y el tope de Toxicidad 100 ya existen en el código.
2. **Segundo:** nombre y registro de recetas; 2 efectos; secundarios; caducidad.
3. **Tercero:** minijuego del alambique de 4 botones, modificadoras, 3 efectos, tolerancia y dependencia, reglas de PvP.
4. **Cuarto:** patentes y copias de receta, técnicas de la escalera (*Destilado limpio*, *Maceración larga*, *Transmutación menor*), el 4º efecto con M10.

## 14. Ediciones pendientes en otros documentos

No se hicieron: este proceso solo escribe este documento.

- [ ] **[Profesiones](profesiones.md)**: §2.3, en la fila de Alquimia, enlazar aquí y nombrar los elixires propios; §8, sumar a la Alquimia el riesgo de dependencia y la Toxicidad por probar ingredientes; §9, sumar el rol "Alquimista con fama" (botica, recetas con nombre); §10, sumar la fila "Un elixir con nombre: Herborista + Cazador + Joyero (frascos) → Alquimista".
- [ ] **[Fabricación](fabricacion.md)**: §2, decir que el alambique usa la versión corta del minijuego (4 botones, barra de Estabilidad, Destilar como forma de Remover con condición Excelente) y enlazar §5.3; §4, el descubrimiento de alquimia sigue la regla de las propiedades compartidas y enlaza aquí; §3, sumar la Potencia a los atributos de los materiales y decir cómo se lee su escala frente a la de 100 = normal que usan este documento y la investigación médica; §6, el alambique como estación con Tramo y calidad; §8, los elixires con nombre Obra Maestra van al registro de obras maestras. **Aviso de contradicción:** §2 dice "máximo 8 botones" y su pantalla tiene 8, pero D-75 (confirmada) pone máximo 4 botones en el mensaje fuera de la barra de combate. Manda D-75: hay que recortar el minijuego de todos los oficios a 4 botones (o 3 y "▶️ Ver más"); este documento ya lo hace para el alambique.
- [ ] **[Condiciones](../05-salud/condiciones.md)**: §4, enlazar aquí la fórmula de Toxicidad por efecto y por potencia (§6.7), los efectos 🔁 y los números de tolerancia y dependencia (§6.8).
- [ ] **[Ronda y acciones](../04-combate/ronda-y-acciones.md)**: §4, en la tabla del cinturón sumar la fila "🍷 Elixir con nombre: varios efectos en una ronda; solo para quien lo bebe"; decir que la Mochila muestra 3 objetos y "▶️ Ver más" (D-75; el código muestra 3 y ↩️ Volver, pero aún no tiene la página siguiente); §11, nombrar la lista normalizada del cinturón de arena (§6.10).
- [ ] **[Daño y estados](../04-combate/dano-y-estados.md)**: §2, decir que los cuatro estados básicos también se curan con elixires (Antídoto, Coagulante, Bálsamo, Calor interno) y que estos dejan una protección posterior.
- [ ] **[Inventario y mochilas](../03-personaje/inventario-y-mochilas.md)**: §4, decir que dos elixires del mismo nombre con distinta calidad van en casillas distintas, y que el orden del cinturón decide qué sale en la primera página.
- [ ] **[PvP](../06-contenido/pvp.md)**: §5, la arena clasificada usa el cinturón normalizado; §8, sumar la potencia de guerra de los elixires en asedios y territorios (§6.10).
- [ ] **[Curación](../05-salud/curacion-y-tratamientos.md)**: §8, enlazar la tabla de caducidad (§6.9); sumar el tratamiento de la dependencia y de la intoxicación por elixires.
- [ ] **[Investigación médica](../05-salud/investigacion-medica.md)**: §2.4, decir que las propiedades de los ingredientes son las mismas que usa la Alquimia y enlazar la tabla de §3.3, que completa sus cuatro propiedades.
- [ ] **[Escalera de conocimiento](escalera-de-conocimiento.md)**: §3.3, ficha de Alquimia, cambiar "el detalle irá en el documento de alquimia y elixires, en redacción" por el enlace a este documento, y nombrar qué hace cada técnica del camino (§5.3).
- [ ] **[Peligros del entorno](../05-salud/peligros-del-entorno.md)**: §7.2, decir que las pociones de entorno se pueden combinar en un elixir (§8.1).
- [ ] **[Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md)**: §4, nombrar los ingredientes de alquimia de cada estación (§9).
- [ ] **[Geografía y recursos](../02-mundo/geografia-y-recursos.md)**: §1, en las filas de cada terreno, nombrar los ingredientes de §3.3.
- [ ] **[Investigación y maestría](investigacion-y-maestria.md)**: §8.2, aclarar que un elixir con nombre se patenta por su combinación de ingredientes; §5.2 (fila "Técnica del minijuego"), cambiar "entra en tu barra de 8" por la regla de D-75 (4 botones; la técnica ocupa uno existente, como en §5.3 de este documento); §3, decir que *Farmacología* baja la Toxicidad un 10 % dentro del techo de rebajas del 15 % (§6.7).
- [ ] **[README de 07 · Economía](README.md)**: sumar la fila de este documento (y, de paso, las de la escalera de conocimiento y de investigación y maestría, que tampoco están).
- [ ] **[Decisiones](../00-vision/decisiones.md)** D-55: cambiar "Alquimia y elixires (en redacción)" por el enlace a este documento.
- [ ] **[Red de sistemas](../00-vision/red-de-sistemas.md)** §3: sumar la fila de §11.
- [ ] **[Glosario](../00-vision/glosario.md)**: propiedad (de efecto, negativa, modificadora, médica), elixir con nombre, reparto de potencia, estabilidad, fresco y pasado, potencia de guerra, lista normalizada.
- [ ] **[Preguntas abiertas](../00-vision/preguntas-abiertas.md)**: sumar las preguntas de §12.
