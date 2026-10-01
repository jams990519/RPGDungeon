# Alquimia y elixires: ingredientes con propiedades y elixires con nombre propio

> **Módulo** [07 · Economía](README.md) · **Depende de:** [Profesiones](profesiones.md) (Alquimia, Herboristería, Desuello), [Fabricación](fabricacion.md) (minijuego, calidad de las vetas, descubrimiento), [Escalera de conocimiento](escalera-de-conocimiento.md) (expedientes de ingrediente, técnicas de Alquimia), [Condiciones](../05-salud/condiciones.md) (Toxicidad y dependencia), [Geografía y recursos](../02-mundo/geografia-y-recursos.md) (terrenos, yacimientos únicos), [Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md) (estaciones, clima, día y noche) · **Se conecta con:** [Ronda y acciones](../04-combate/ronda-y-acciones.md) (🎒 Mochila y cinturón), [Daño y estados](../04-combate/dano-y-estados.md) (estados por acumulación), [Peligros del entorno](../05-salud/peligros-del-entorno.md), [Curación](../05-salud/curacion-y-tratamientos.md), [Investigación médica](../05-salud/investigacion-medica.md), [Mente](../05-salud/mente.md) (estrés), [Inventario y mochilas](../03-personaje/inventario-y-mochilas.md), [Balance](../03-personaje/balance.md), [PvP](../06-contenido/pvp.md), [Investigación y maestría](investigacion-y-maestria.md) (patentes), [Propiedad y concesiones](propiedad-y-concesiones.md) (botica propia), [Red de sistemas](../00-vision/red-de-sistemas.md) · **Estado:** propuesta (la regla de fondo es D-55, confirmada)

**Qué pediste.**
- "Incluso seas capaz de crear tus propios elixires, no solamente con una curación, sino con una curación con un plus de varias cosas."

Eso ya quedó registrado como **D-55** en [Decisiones](../00-vision/decisiones.md): el alquimista combina ingredientes y crea elixires con nombre propio, que curan y suman varios efectos a la vez, con límites de balance. Este documento lo arma. Es la **cima** de la Alquimia en la [Escalera de conocimiento](escalera-de-conocimiento.md) §3.3, pero se empieza a probar desde el rango Aprendiz, con mezclas de un solo efecto.

**De dónde sale.**
- *The Elder Scrolls V: Skyrim*: cada ingrediente tiene **cuatro efectos ocultos**. Comerlo revela el primero; los demás se descubren mezclando. Al juntar dos ingredientes, aparecen en la poción **los efectos que comparten**, buenos y malos.
- *The Witcher 3*: pociones de efecto corto, **decocciones** de efecto largo y una barra de **Toxicidad** que impide encadenarlas. Ya la usa [Condiciones](../05-salud/condiciones.md) §4.
- *Potion Craft*: el alquimista descubre recetas probando, les pone **nombre** y las vende en su tienda. La fama de la botica depende de sus pociones.
- *Kingdom Come: Deliverance*: la receta es **paso a paso** (qué va primero, cuánto hierve, cuándo se destila). Equivocarse en el orden arruina la poción.
- *Final Fantasy XIV*: el **minijuego de fabricación** por turnos decide la **calidad**. Es el que ya usa [Fabricación](fabricacion.md) §2.
- *Path of Exile*: los **frascos con modificadores** (cura más un efecto extra, como quitar el sangrado o subir la armadura) y un número limitado de cargas.
- *Atelier* (la saga): los objetos **heredan rasgos** de sus ingredientes, y elegir el ingrediente justo para pasar un rasgo es el corazón del juego.

**Por qué conviene.** La poción de vida de un toque sigue existiendo para todos. Pero quien quiera ser alquimista tiene un juego propio: conocer ingredientes, juntarlos en el lugar y la estación justos, y crear un elixir que nadie más hace, con su nombre en la etiqueta. Eso da oficio, fama y comercio sin dar más poder del que el [Balance](../03-personaje/balance.md) permite.

---

## 1. La regla, en corto

1. **Cada ingrediente tiene 4 propiedades.** La primera se ve al recogerlo; las otras se descubren (§3).
2. **Mezclar es compartir.** Se juntan de 2 a 4 ingredientes en el alambique. Cada propiedad que aparece en **dos o más** ingredientes da su efecto al elixir (§4 y §5).
3. **El minijuego decide la potencia y la estabilidad** (§5.3). La mezcla rápida es de un toque y llega a Notable.
4. **El alquimista le pone nombre** y la receta queda registrada a su nombre: se vende, se enseña y se patenta (§5.4).
5. **Los límites son duros:** efectos por rango, reparto de potencia, topes por efecto, nada se acumula con lo mismo, Toxicidad, dependencia, reglas de PvP y caducidad (§6).
6. **Un elixir se bebe, no se da.** Solo afecta a quien lo toma. Así nunca reemplaza a un sanador ni a un defensor (§7.3).
7. **Nada se compra con dinero real** (D-43). Ni ingredientes, ni recetas, ni potencia. Los aceleradores no tocan los expedientes ni los ingredientes de temporada (ver [Escalera de conocimiento](escalera-de-conocimiento.md) §1, regla 6).

### 1.1 Ligero: capa simple y capa profunda (D-44)

| Quién | Qué hace | Cuánto le pide |
|---|---|---|
| **Jugador de paso** (casi todos) | Compra en el mercado o en la botica una poción conocida, o un elixir con nombre de otro jugador, y lo pone en el cinturón | **Un toque.** No necesita saber que existen las propiedades |
| **Alquimista de todos los días** | Fabrica con un toque las recetas que ya sabe (de entrenador, compradas o propias), en modo rápido | Un toque por tanda. Hasta calidad Notable |
| **Alquimista inventor** | Abre el alambique, prueba ingredientes, descubre propiedades, juega el minijuego y registra elixires con nombre | Lo que quiera: es su carrera |

**Las pistas, no las respuestas** (D-56). La primera vez que dos ingredientes comparten una propiedad, el alambique dice solo: *"🔎 Estos dos tienen algo en común. Embotéllalo y verás qué."* Lo demás se aprende probando (ver [Aprendizaje y pistas](../00-vision/aprendizaje-y-pistas.md)).

## 2. Las propiedades

Las propiedades son **el mismo vocabulario** que usa la [Investigación médica](../05-salud/investigacion-medica.md) §2.3 y §2.4 (Fría, Cálida, Purificante, Cicatrizante…). Un ingrediente tiene las mismas propiedades para el médico y para el alquimista; cada uno las usa a su manera.

Hay cuatro clases de propiedad:

| Clase | Cómo actúa | Ejemplos |
|---|---|---|
| ✅ **De efecto** | Si **dos o más** ingredientes la comparten, el elixir gana su efecto (§4.1) | Cicatrizante, Ignífuga, Despertadora |
| ⚠️ **Negativa** | Si dos o más la comparten, el elixir gana un **efecto secundario** (§4.2). No cuenta para el límite de efectos, y no se puede quitar sin una técnica | Amarga, Nerviosa, Adormecedora, Tóxica |
| 🔧 **Modificadora** | Actúa con **un solo** ingrediente que la tenga. No da efecto: cambia el elixir | Pura, Dulce, Conservante, Pegajosa, Salvaje |
| ⚕️ **Médica** | No da nada en un elixir: solo sirve en los remedios de la investigación médica | de Memoria, Ordenadora, Regenerativa, Contagiosa |

**Modificadoras:**

| Propiedad | Qué hace en el elixir |
|---|---|
| 💠 **Pura** | +1 nivel de estabilidad (dura más fresco, §6.8) |
| 🍬 **Dulce** | −5 de Toxicidad por cada ingrediente dulce, hasta −10 |
| 🧊 **Conservante** | +50 % de días fresco |
| 🕸️ **Pegajosa** | +1 ronda (o +10 pasos fuera de combate) a los efectos con duración |
| 🐾 **Salvaje** | +10 % de potencia, pero −1 nivel de estabilidad y el doble de tolerancia (§6.7) |

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

Cada lote de ingrediente tiene **Potencia** y **Pureza**, como cualquier material (ver [Fabricación](fabricacion.md) §3 y [Investigación médica](../05-salud/investigacion-medica.md) §2.4). Del lote salen la fuerza del efecto y la estabilidad del elixir.

| Qué la mueve | Cómo | Ejemplo |
|---|---|---|
| **La veta o la planta** | Cada nodo tiene su calidad, que rota cada semana | Un campo de cardos de potencia 115 es noticia para los alquimistas de la región |
| **La zona** | Las Lejanías más lejanas dan lotes con techo más alto | La Hierba curativa del Claro llega a 100; la de Lejanía 9, a 125 |
| **La estación** | En su estación, el ingrediente está **en sazón**: +10 % de potencia. Fuera de estación solo hay lotes conservados, con −10 % | La Raíz de mandrágora tierna solo es tierna en primavera |
| **La hora y el clima** | Algunos solo existen de noche, con ventisca o con tormenta | La Flor de Ciénaga Tardía, de noche en otoño |

**Potencia del ingrediente en el elixir:** el promedio de la Potencia de los lotes usados (100 = normal) multiplica los efectos, entre ×0,8 y ×1,25. Los materiales de temporada llevan 🌙 y los de yacimiento único ⭐ en la mochila (ver [Escalera de conocimiento](escalera-de-conocimiento.md) §2.4).

### 3.3 Veinte ingredientes de ejemplo

La propiedad en **negrita** es la que se ve al recogerlo. Las demás se descubren (§3.4). Los que ya aparecen en la [Investigación médica](../05-salud/investigacion-medica.md) §2.4 conservan las dos propiedades que dice ese documento.

| Ingrediente | Propiedades | Dónde | Cuándo | Quién lo trae |
|---|---|---|---|---|
| 🌿 **Hierba curativa** | **Cicatrizante** · Vivificante · Creciente · Amarga | 🌾 Llanura y 🌲 bosque, cualquier Lejanía | Siempre; poca en invierno | Herborista; cualquiera al explorar |
| 🌺 **Cardo rojo** | **Coagulante** · Cicatrizante · Aguda · Nerviosa | 🌾 Llanura, Lejanías cercanas | Primavera y verano | Herborista |
| 🌊 **Alga de costa** | **Acuática** · Coagulante · Mineral · Emoliente | 🌊 Costa y lagos | Siempre; con marea baja rinde el doble | Herborista o pescador |
| ⬛ **Carbón de montaña** | **Pulmonar** · Purificante · Pétrea · Amarga | ⛰️ Montaña | Siempre | Minero |
| 🌋 **Flor de Ceniza** | **Ignífuga** · Cicatrizante · Cálida · Nerviosa | 🌋 Tierras volcánicas y laderas quemadas | Verano; después de una erupción, más | Herborista con capa ignífuga |
| 🍄 **Hongo luminoso** | **Sombría** · Resonante · Luminosa · Adormecedora | 🕳️ Cueva y subsuelo | Siempre; de noche rinde el doble | Herborista con luz |
| 🕸️ **Corazón de micelio** | **Creciente** · Pegajosa · Renovadora · Tóxica | 🕳️ Cueva (Micelio Andante) | Siempre; **cultivado** en casa rinde más | Cazador, después Agricultor |
| 🐸 **Glándula de sapo de ciénaga** | **Despertadora** · Acuática · Salvaje · Tóxica | 🐸 Pantano (monstruo) | Verano, época de canto | Cazador con Desuello |
| 🌵 **Pulpa de cactus de duna** | **Mineral** · Fría · Emoliente · Dulce | 🏜️ Desierto | Siempre; la flor nocturna da lotes mejores | Herborista o aguador |
| 🟠 **Ámbar de tundra** | **Conservante** · Pétrea · Terrosa · Cálida | ❄️ Tundra | Siempre | Minero |
| 👁️ **Ojo de lince de las nieves** | **Aguda** · Sombría · Aislante · Salvaje | ❄️ Tundra y ⛰️ montaña (monstruo) | Invierno | Cazador con Desuello |
| 🌱 **Raíz de mandrágora tierna** | **Sedante** · Adormecedora · Calmante · Renovadora | 🐸 Pantano, Lejanías medias | Primavera 🌙 | Herborista con tapones de cera |
| 🌸 **Flor de Ciénaga Tardía** | **Fría** · Amarga · Purificante · Sombría | 🐸 Pantano, Lejanías medias | Otoño, de noche 🌙 | Herborista con máscara de carbón |
| 🌿 **Musgo de Cumbre Blanca** | **Cálida** · Pulmonar · Aislante · Pura | ⛰️ Picos Helados, Lejanías lejanas | Invierno, después de una ventisca 🌙 | Herborista aclimatado |
| 💧 **Agua de fondo del Oasis Hondo** | **Pura** · Mineral · Fría · Conservante | 🏜️ Desierto, Lejanías medias | Verano, cuando el oasis baja 🌙 | Aguador con frasco de vidrio de duna |
| ❄️ **Lágrima helada** | **Fría** · Conservante · Aislante · Resonante | ❄️ Tundra y pasos (Novia de Escarcha) | Con ventisca 🌙 | Cazadores en grupo |
| 🦎 **Escama de salamandra en muda** | **Cálida** · Renovadora · Ignífuga · Salvaje | 🌋 Tierras volcánicas, Lejanías lejanas | Verano, época de muda 🌙 | Cazador con capa ignífuga |
| 🍯 **Miel negra** | **Cicatrizante** · Dulce · Sedante · Renovadora | 🏛️ Ruinas y 🌲 bosque (Árbol Hueco) | Otoño 🌙 | Cazador y herborista |
| 🌼 **Polen de Flor de Difuntos** | **Calmante** · de Memoria · Luminosa · Adormecedora | 🌾 Llanuras | Solo en el festival de difuntos 🌙 | Herborista o agricultor |
| ⚡ **Agua de rayo** | **Vivificante** · Nerviosa · Terrosa · Despertadora | 🌸 Tierras flotantes, Lejanías muy lejanas | Solo con tormenta 🌙 | Explorador con pararrayos |

Los yacimientos únicos (por ejemplo, la **Sal de Estrellas**: Purificante · Pura · Luminosa · Terrosa) y los ingredientes de evento (el **Hongo del Eclipse**) se suman con el mismo formato. Los nombres de Lejanía son orientativos hasta que el [Mapa infinito](../02-mundo/mapa-infinito-y-viaje.md) fije los rangos.

### 3.4 Descubrir las propiedades ocultas

Tres caminos, y se pueden mezclar:

| Camino | Cómo | Qué revela | Costo |
|---|---|---|---|
| 🔬 **Experimentar** | Mezclar en el alambique (§5). Al embotellar, cada propiedad compartida se revela en los ingredientes que la tienen. Una mezcla que no comparte nada también enseña: *"La Hierba curativa y el Ámbar no tienen nada en común"* | Las propiedades compartidas | Los ingredientes de la prueba |
| 👅 **Probar** | Comer un ingrediente crudo (un toque) | La siguiente propiedad oculta, solo hasta la 2ª | +10 de Toxicidad; si es Amarga o Tóxica, también su secundario |
| 📒 **El expediente** | Cada ingrediente tiene su expediente en la [Escalera de conocimiento](escalera-de-conocimiento.md) §2.2, que se llena solo al recoger, destilar y mezclar | ★ la 1ª y la calidad del lote · ★★ dónde y cuándo aparece, y la 2ª · ★★★ la 3ª · ★★★★ la 4ª y qué lo potencia | Tiempo |
| 💰 **Comprar la información** | Un **herbario** (copia de expediente hecha con Inscripción), la Biblioteca pública o un informante | Hasta ★★: las dos primeras. **Lo que se lee no reemplaza lo que se prueba** (misma regla que la medicina) | Oro |

- **Las propiedades son fijas** para cada ingrediente en todo el servidor. Lo que se descubre vale para siempre y se puede vender.
- **Una receta comprada no enseña propiedades.** Quien compra la receta de un elixir puede fabricarlo, pero no sabe por qué funciona (§5.4).

## 4. Qué puede tener un elixir

### 4.1 Catálogo de efectos

**Valor base** es lo que da el efecto en un elixir de **un solo efecto**, con ingredientes de potencia 100 y calidad Notable. **Tope** es el máximo absoluto, con cualquier calidad y cualquier ingrediente. **Toxicidad** es lo que suma el efecto con ese valor base (ver §6.6).

**❤️ Curación de vida**

| Efecto | Propiedad | Valor base | Tope | Duración | Toxicidad |
|---|---|---|---|---|---|
| ❤️ **Curación** | Cicatrizante | 35 % de la vida máxima (igual que la poción de vida) | 40 % | Al instante | 40 |
| 💗 **Regeneración** | Renovadora | 5 % de la vida máxima por ronda | 6 % por ronda | 4 rondas (fuera: 1 minuto) | 30 |

**💊 Curación de estados** (ver [Daño y estados](../04-combate/dano-y-estados.md) §2). Vaciar la barra y cortar el daño por ronda es igual con cualquier potencia; la potencia decide la **protección posterior**: la barra de ese estado se llena más despacio durante 3 rondas.

| Efecto | Propiedad | Qué hace siempre | Valor base de la protección | Tope | Toxicidad |
|---|---|---|---|---|---|
| 🟢 **Antídoto** | Purificante | Vacía la barra de Veneno y corta su daño | −50 % de acumulación | −60 % | 20 |
| 🩸 **Coagulante** | Coagulante | Vacía la barra de Sangrado y corta su daño | −50 % | −60 % | 15 |
| 🔥 **Bálsamo** | Emoliente | Vacía la barra de Quemadura y corta su daño | −50 % | −60 % | 15 |
| ❄️ **Calor interno** | Cálida | Vacía la barra de Congelación. Fuera de combate: +1 de abrigo | −50 % / 20 pasos | −60 % / 30 pasos | 15 |

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
| ☀️ **Frescor** | Fría | +1 de frescor fuera de combate; en combate anula el castigo de calor al Aguante | 30 pasos / 4 rondas | 20 pasos / 3 rondas | 15 |
| 💧 **Sales** | Mineral | Baja una etapa de sed, además del trago | Dos etapas | Al instante | 5 |
| ☣️ **Pulmón limpio** | Pulmonar | −20 de Contaminación y +1 de filtro | −30 y +1 | 20 pasos | 15 |

**⚔️ Ventajas temporales**

| Efecto | Propiedad | Valor base | Tope | Duración | Toxicidad |
|---|---|---|---|---|---|
| ⚡ **Iniciativa** 🔁 | Despertadora | +15 % de iniciativa | +20 % | 3 rondas | 25 |
| 🎯 **Precisión** | Aguda | +10 % de precisión | +12 % | 3 rondas | 25 |
| 🛡 **Protección de zona** | Pétrea | +20 % de armadura en **una** parte del cuerpo (cabeza, torso, brazos o piernas), que se elige al destilar y queda en la receta | +25 % | 5 rondas | 20 |

**⛏️ Efectos de oficio** (fuera de combate)

| Efecto | Propiedad | Valor base | Tope | Duración | Toxicidad |
|---|---|---|---|---|---|
| ⛏️ **Rendimiento** | Creciente | +10 % de rendimiento al recolectar o cosechar. **No** se aplica a los materiales 🌙 ni ⭐ | +15 % | 1 hora real | 10 |

**✨ Efectos raros**

| Efecto | Propiedad | Valor base | Tope | Duración | Toxicidad |
|---|---|---|---|---|---|
| 👁 **Visión nocturna** | Sombría | Sin penalización de oscuridad leve y media; en oscuridad total, de −40 % a −15 % | Igual | 30 pasos / 10 rondas | 15 |
| 🫧 **Respirar bajo el agua** | Acuática | Aire sin límite | 15 pasos | 10 pasos | 15 |
| 🧠 **Calma** 🔁 | Calmante | −15 de estrés (ver [Mente](../05-salud/mente.md)) | −20 | Al instante | 20 |
| 💊 **Analgesia** 🔁 | Sedante | −1 nivel de Dolor (ver [Condiciones](../05-salud/condiciones.md)) | −2 niveles | 1 hora real | 20 |

🔁 = genera tolerancia y puede traer dependencia (§6.7).

### 4.2 Efectos secundarios

Salen de las propiedades **negativas** que comparten dos o más ingredientes. No cuentan para el límite de efectos.

| Secundario | Propiedad | En combate | Fuera de combate |
|---|---|---|---|
| 🤢 **Náusea** | Amarga | La próxima comida o poción rinde la mitad durante 3 rondas | La comida no sube el Sustento durante 10 minutos |
| 🫨 **Temblor** | Nerviosa | −8 % de precisión durante 3 rondas | −1 condición en el próximo minijuego de fabricación |
| 😴 **Somnolencia** | Adormecedora | −10 % de iniciativa durante 3 rondas | +1 nivel de Fatiga durante 30 minutos |
| 🧪 **Más toxicidad** | Tóxica | +15 de Toxicidad | +15 de Toxicidad |

**Quitar un secundario** pide la técnica *Destilado limpio* (escalón I de la Alquimia, ver [Escalera de conocimiento](escalera-de-conocimiento.md) §3.3): un paso más del minijuego que borra **un** secundario y gasta durabilidad. Los alquimistas novatos venden elixires con náusea más baratos; los buenos, limpios.

## 5. Crear un elixir propio

### 5.1 El alambique

- Es la estación de la Alquimia (ver [Fabricación](fabricacion.md) §6): hay alambiques públicos en los asentamientos (con tasa de uso), en las casas y en los salones de gremio. La capital con especialidad en alquimia da más retorno de material.
- El alambique tiene **Tramo y calidad**, como cualquier herramienta: uno mejor da más durabilidad en el minijuego.
- **Mezclar pide entre 2 y 4 ingredientes**, una unidad de cada uno por elixir. Una tanda da 3 elixires; con alambique de calidad alta, 4.

### 5.2 Cómo se forma la mezcla

1. **Se eligen los ingredientes.** El alambique muestra las propiedades que conoces de cada uno.
2. **Se calculan las compartidas.** Cada propiedad de efecto o negativa que aparece en dos o más ingredientes entra en el elixir. Las que no conoces aparecen como *"❔ algo en común (1·3)"*.
3. **Se aplica el límite del rango** (§6.1). Si salen más efectos de los que tu rango permite, **eliges cuáles quedan**. Los secundarios no se eligen: vienen con la mezcla.
4. **Se aplican las modificadoras** (Pura, Dulce, Conservante, Pegajosa, Salvaje).
5. **Se juega el minijuego** (§5.3) o se resuelve en modo rápido.
6. **Al embotellar** se revelan las propiedades ❔, y si la combinación es nueva, el alquimista le pone nombre (§5.4).

**El orden importa** (como en *Kingdom Come*). Cada receta registrada guarda el orden en que entraron los ingredientes y las acciones clave del minijuego. Repetir la receta tal cual da la misma calidad mínima; cambiar el orden puede mejorarla o arruinarla.

### 5.3 El minijuego del alambique

Es el minijuego de [Fabricación](fabricacion.md) §2 (estilo *Final Fantasy XIV*), en una versión **corta** de 4 a 8 pasos y con **6 botones**, como pide D-66. Tiene dos barras de resultado:

- **Calidad** → la **potencia**: Normal ×0,85 · Buena ×0,95 · Notable ×1 · Excelente ×1,1 · Obra Maestra ×1,2. El tope de cada efecto (§4.1) manda siempre.
- **Estabilidad** → **cuánto dura fresco** (§6.8): Baja, Media o Alta.

Y las de siempre: **Progreso**, **Durabilidad**, **PA** y la **Condición** que cambia cada paso.

| Acción | Efecto | Costo |
|---|---|---|
| 🔥 **Calentar** | +Progreso | Durabilidad |
| 🥄 **Remover** | +Calidad | Durabilidad, pocos PA |
| 💧 **Enfriar** | +Estabilidad, un poco de Progreso | PA |
| ⚗️ **Destilar** (propia del alquimista) | Convierte Progreso en Calidad; con condición Excelente, el doble | PA, durabilidad |
| 👁 **Observar** | Muestra la condición del paso siguiente | PA mínimos |
| 🍾 **Embotellar** | Termina. Si el Progreso no está lleno, sale con calidad un nivel menor | — |

- Las técnicas de la escalera suman acciones: *Destilado limpio* (I) quita un secundario; *Maceración larga* (II) deja reposar la mezcla de 2 a 12 horas reales y sube la Calidad sin gastar durabilidad; *Transmutación menor* (IV) cambia **una** propiedad de un ingrediente por otra de su misma familia (por ejemplo, Fría por Aislante), una vez por mezcla.
- Si la durabilidad llega a 0 antes de embotellar, se pierden los ingredientes. Lo descubierto en esa prueba **no** se pierde.
- **Modo rápido:** un toque. El resultado sale de tu rango, tu Maestría en Elixires y la calidad de los lotes. **Techo: Notable**, como toda fabricación rápida.

### 5.4 El nombre y la receta

- **Si la combinación de ingredientes no existe en el servidor**, el alquimista le pone nombre (hasta 32 letras, con el filtro de palabras de [Seguridad](../01-plataforma/seguridad-y-anti-trampas.md)). El bot le suma *"de [nombre del alquimista]"*: *"Aliento de Brasa de Ilse"*.
- **La receta queda registrada a su nombre**: ingredientes, orden, efectos elegidos y la parte del cuerpo de la Protección de zona, si la tiene. La Gaceta anuncia el primer elixir nuevo de cada semana.
- **Si la combinación ya existe**, el elixir lleva el nombre de quien la registró primero, y el alambique lo dice: *"Ya existe: Aliento de Brasa de Ilse (patentada)"*.
- **Qué se puede hacer con la receta** (ver [Investigación y maestría](investigacion-y-maestria.md) §8 y §9):

| Opción | Qué pasa |
|---|---|
| ⚖️ **Patentar** | Cualquiera puede aprenderla en el Registro de patentes, y paga una regalía cada vez que la fabrica, durante 12 semanas. Después es pública |
| 🔒 **Secreto de taller** | Solo la fabricas tú. Otro puede llegar a la misma combinación probando; si lo logra, la fabrica sin pagarte |
| 📖 **Publicar gratis** | Pasa a la Biblioteca pública. Da prestigio y Saber a tu ciudad |
| 📜 **Vender copias** | Copia de receta con usos limitados, hecha con Inscripción. Quien la compra la fabrica, pero no aprende las propiedades |
| 🎓 **Enseñar** | A tus aprendices, o en un tratado (ver [Investigación y maestría](investigacion-y-maestria.md) §9) |

- **Etiqueta:** cada frasco lleva el nombre, la calidad, la firma del alquimista, la fecha y los días que le quedan fresco. Las Obras Maestras van al registro público de obras maestras (ver [Fabricación](fabricacion.md) §8).

## 6. Límites de balance

**La idea.** Un elixir de varios efectos **ahorra rondas y casillas**, no suma poder. Beber un elixir de tres efectos tiene que valer más o menos lo mismo que beber tres pociones de un efecto, menos las dos rondas que te ahorras, y pagar ese ahorro con potencia y Toxicidad. Así no se rompe el presupuesto de poder de cada spec (ver [Balance](../03-personaje/balance.md) §2): los consumibles están **fuera** de los 100 puntos, y por eso tienen techo propio.

### 6.1 Efectos por rango

| Rango de Alquimia | Niveles | Efectos por elixir | Además |
|---|---|---|---|
| Aprendiz | 1-20 | 1 | Recetas de entrenador; descubre propiedades |
| Oficial | 21-40 | 1 | Usa las modificadoras; técnica *Destilado limpio* |
| Experto | 41-60 | 2 | Primer elixir con nombre de dos efectos |
| Artesano | 61-80 | 2 | Más techo de calidad en el minijuego |
| Maestro | 81-95 | 3 | Obras Maestras |
| Gran Maestro | 96-100 | 3 | Firma dorada |
| Gran Maestro con M10 en Elixires | 100 + Maestría 10 | **4**, si el cuarto es de oficio o de entorno (Rendimiento, Frescor, Sales, Pulmón limpio, Visión nocturna, Respirar bajo el agua) | El cuarto efecto nunca es de combate |

### 6.2 El reparto de la potencia

Cuantos más efectos, menos rinde cada uno:

| Efectos | Potencia de cada uno | Total |
|---|---|---|
| 1 | 100 % | 100 % |
| 2 | 65 % | 130 % |
| 3 | 50 % | 150 % |
| 4 | 40 % | 160 % |

El total sube un poco para que valga la pena combinar, pero un elixir de tres efectos **nunca cura tanto** como una poción de vida sola, y su Toxicidad es más alta (§6.6).

### 6.3 Topes por efecto

Cada efecto tiene su tope en §4.1, y **ningún elixir lo pasa**, con cualquier calidad, Maestría o ingrediente de yacimiento único. Los topes se revisan con el resto del balance y se anotan en el registro de balance.

### 6.4 Lo mismo no se acumula

- **Un mismo efecto no se suma con otro consumible.** Si bebes un elixir con 🔥 Resistencia al fuego y tienes activa otra resistencia al fuego (de poción o de elixir), queda la más fuerte y se renueva la duración.
- Los efectos **distintos** sí conviven: un elixir con Regeneración y una poción de Resistencia al fuego valen a la vez.
- **Con las habilidades de clase sí se suman**, porque esas ya están dentro del presupuesto de la spec.

### 6.5 Un elixir por ronda

Usar un elixir gasta tu elección de la ronda, como cualquier objeto del cinturón (D-46). Ningún efecto da una acción extra.

### 6.6 Toxicidad

Cada elixir suma Toxicidad (ver [Condiciones](../05-salud/condiciones.md) §4: por encima de 75 se pierde vida, y en 100 no puedes beber más).

**Toxicidad del elixir** = la suma de la Toxicidad de cada efecto × su reparto (§6.2) · + 5 por cada efecto después del primero · + 15 si tiene el secundario 🧪 · − 5 por cada ingrediente Dulce (hasta −10) · mínimo 10.

| Ejemplo | Cuenta | Toxicidad |
|---|---|---|
| Poción de vida (1 efecto) | 40 × 1 | **40** |
| Curación + Antídoto (2 efectos) | (40 + 20) × 0,65 + 5 | **44** |
| Curación + Regeneración + Resistencia al fuego, con Dulce | (40 + 30 + 25) × 0,5 + 10 − 5 | **52** |
| Iniciativa + Precisión, con Tóxica | (25 + 25) × 0,65 + 5 + 15 | **52** |

La calidad sube la potencia, **no** la Toxicidad. La técnica *Farmacología* (Medicina + Alquimia, ver [Investigación y maestría](investigacion-y-maestria.md) §3) baja un 10 % la Toxicidad de los elixires que fabricas.

### 6.7 Tolerancia y dependencia

Los efectos marcados 🔁 (Aguante, Iniciativa, Calma, Analgesia) generan **tolerancia**, como dice [Condiciones](../05-salud/condiciones.md) §4:

- Cada uso del mismo efecto en 24 horas reales rinde un 10 % menos (hasta −40 %). Un ingrediente Salvaje duplica la tolerancia que suma.
- **Dependencia:** más de 6 usos del mismo efecto 🔁 en 3 días reales. Trae **abstinencia** de ese efecto: −5 % de iniciativa y +10 de estrés al día hasta que pasan 2 días sin usarlo, o hasta que un médico la trata (ver [Curación](../05-salud/curacion-y-tratamientos.md)).
- **Siempre con aviso:** al quinto uso, el bot dice *"⚠️ Tu cuerpo se acostumbra al Aliento Rápido. Uno más y vas a depender de él."*
- La tolerancia baja sola con el tiempo, también sin conectarse.

### 6.8 Caducidad

Los elixires **caducan**, como los remedios (ver [Curación](../05-salud/curacion-y-tratamientos.md) §8). Eso mantiene la demanda viva y evita que alguien guarde mil frascos de una buena semana.

| Estabilidad | Días fresco (rinde 100 %) | Después |
|---|---|---|
| Baja | 5 días reales | −5 % de potencia por día, hasta 60 %. A los 15 días queda **pasado**: solo da sus secundarios y su Toxicidad |
| Media | 10 días | Igual |
| Alta | 20 días | Igual |

- **Conservante** suma la mitad de días fresco. Un **frasco de vidrio de duna** (Joyería) suma 5 días; uno de **cristal tallado**, 10.
- Las **pociones de entrenador** (poción de vida, resistencias básicas, remedios comunes) duran 30 días fresco.
- Lo que está en el cinturón caduca igual que lo de la mochila. En la bodega fría de una casa (ver [Casa propia](../09-construccion/casa-propia.md)) los días cuentan a la mitad.

### 6.9 PvP: arena, guerra y mundo abierto

| Dónde | Qué vale | Por qué |
|---|---|---|
| 🏟️ **Arena clasificada** | **Solo la lista normalizada:** el cinturón de arena es igual para todos (ver [Ronda y acciones](../04-combate/ronda-y-acciones.md) §11) y trae poción de vida, una poción de resistencia a elección, un remedio de estados y una poción de recurso. **Ningún elixir propio** | En la clasificatoria decide la habilidad, igual que con el equipo normalizado (ver [PvP](../06-contenido/pvp.md)). Si entraran los elixires propios, ganaría quien tiene al mejor alquimista |
| 🏰 **Guerra de castillos, asedios y territorios** | Elixires propios **con potencia de guerra:** como máximo **2 efectos**, cada uno calculado con calidad Notable (sin bono de calidad ni de ingrediente Salvaje). Los elixires de más efectos se pueden llevar, pero en la batalla rinden como si solo tuvieran sus 2 primeros | La guerra premia la preparación y la economía del gremio, y el alquimista del castillo es parte del ejército. El tope impide que la guerra la gane solo quien tiene más oro para Obras Maestras |
| ⚔️ **Mundo abierto y zonas rojas y negras** | Todo, como en PvE | Prepararse para la zona es parte del riesgo. Ya rigen el **tope de golpe del 40 %** y la **amortiguación de curación** desde la ronda 8, que también se aplica a la curación de los elixires |

## 7. En combate

### 7.1 Desde la 🎒 Mochila

- Los elixires van en el **cinturón** (ver [Inventario y mochilas](../03-personaje/inventario-y-mochilas.md) §4): una casilla por elixir de un mismo nombre y calidad, hasta 3 unidades.
- **Usarlo gasta la elección de la ronda** y se resuelve primero, antes de los golpes, como cualquier objeto (ver [Ronda y acciones](../04-combate/ronda-y-acciones.md) §4 y §6). Por eso un elixir con Resistencia al fuego contesta un aliento avisado.
- Las **configuraciones guardadas** del cinturón ("solitario", "mazmorra", "PvP") recuerdan qué elixires lleva cada una.

### 7.2 Cómo se ve

Ronda 3 contra la Salamandra Madre. Avisa un aliento de fuego, y el Guerrero ya tiene la barra de Quemadura a la mitad:

```
⚔️ Ronda 3 · Salamandra Madre (jefa de campo)
⚠️ Toma aire: ALIENTO DE FUEGO a toda la vanguardia
   en esta ronda.

🟥 Tú — Guerrero Armas · Vanguardia
❤️ 540/1.120   🔷 Ira 30   🔋 ●●○○○
🔥▓▓▓▓▓▓░░░░ Quemadura
🧪 Toxicidad 0/100
⏱ 45 s

[⚔️ Atacar]        [✨ Golpe Mortal]
[✨ Parada]        [✨ Grito de Batalla]
[🏃 Huir]          [🎒 Mochila]
```

Toca 🎒 **Mochila**:

```
🎒 Cinturón (5 casillas)

1. 🧪 Poción de vida ×2 · ❤️ 35 % · 🧪 40
2. 🍷 Aliento de Brasa de Ilse ×1 · Excelente · fresco 8 días
   ❤️ 21 % · 💗 3 %/ronda ×4 · 🔥 −18 % fuego ×3 · 🧪 52
3. 💊 Ungüento para quemaduras ×2 · 🧪 15
4. 🩹 Venda ×3
5. —

[1 🧪]  [2 🍷]
[3 💊]  [4 🩹]
[↩️ Volver]
```

Elige el **Aliento de Brasa**. Con una sola ronda se cura, se protege del aliento y empieza a regenerar. No le quita la barra de quemadura: para eso haría falta el ungüento, otra ronda.

```
📜 Ronda 3
🍷 Bebes Aliento de Brasa de Ilse:
   ❤️ +235 · 💗 3 %/ronda (4 rondas) · 🔥 −18 % fuego (3 rondas)
🔥 La Salamandra Madre lanza ALIENTO DE FUEGO: −248 (−18 %)
   🔥▓▓▓▓▓▓▓▓░░ Quemadura
⚔️ Bram (Protección) golpea con el escudo: −160
❤️ 527/1.120 · 🧪 Toxicidad 52/100
```

Con 52 de Toxicidad todavía puede tomar una poción más, pero no dos: la Toxicidad sigue siendo el freno.

### 7.3 Elixires y roles (D-50)

Cada clase tiene specs de **Ataque, Defensa, Curación y Soporte**, y cada una cumple su papel en el grupo. Los elixires ayudan a todos, sobre todo en solitario, pero **no convierten a nadie en otro rol**:

- **Solo afectan a quien los bebe.** No se le dan a un aliado en combate. Curar y proteger a otros sigue siendo el trabajo de los specs de Curación, Defensa y Soporte.
- **Una cura de elixir rinde como máximo un 40 % de la vida, y la Toxicidad deja dos o tres por pelea.** Un sanador cura cada ronda.
- **Ningún efecto provoca, cubre una fila ni potencia al grupo.** Eso es de los specs de Defensa y Soporte.
- **Las bombas** (Alquimia e Ingeniería) son otra cosa: se lanzan, hacen daño o dejan una superficie, y tienen su propio máximo de 3 por pelea (ver [Mecánicas avanzadas](../04-combate/mecanicas-avanzadas.md)).

## 8. Fuera de combate

### 8.1 Expediciones

Los elixires de entorno son los que más se venden a exploradores, caravanas y gremios que cruzan terrenos duros (ver [Peligros del entorno](../05-salud/peligros-del-entorno.md) §7.2). Un elixir de varios efectos ahorra peso y casillas en la mochila.

| Elixir de ejemplo | Efectos | Para |
|---|---|---|
| *Trago de Caravana* (Experto) | 💧 Sales · ☀️ Frescor | Cruzar el desierto de día |
| *Aliento de Cumbre* (Experto) | ❄️ Calor interno · ☣️ Pulmón limpio | Minas altas con gas y frío |
| *Ojo de Ciénaga* (Maestro) | 👁 Visión nocturna · 🟢 Antídoto · ☣️ Pulmón limpio | Pantano de noche, con miasma y sapos venenosos |
| *Buzo del Lago Negro* (Gran Maestro, M10) | 🫧 Respirar bajo el agua · 👁 Visión nocturna · ❄️ Calor interno · ⛏️ Rendimiento | Recolectar en el fondo de un lago helado |

### 8.2 Oficios

- **Rendimiento** (Creciente) sube lo que se saca al recolectar o cosechar, durante una hora real. Nunca multiplica los materiales 🌙 ni ⭐, igual que el acelerador.
- **Analgesia** deja trabajar con una herida leve sin que el Dolor estropee el minijuego.
- **Frescor** y **Calor interno** sirven al minero de la montaña y al herrero junto a la forja.

### 8.3 La investigación médica

La Alquimia y la Medicina comparten los ingredientes y el vocabulario de propiedades:

- Los **remedios** que salen de la [Investigación médica](../05-salud/investigacion-medica.md) (febrífugos, antitoxinas, sueros) los fabrica en cantidad un alquimista con la receta del protocolo.
- Lo que el alquimista descubre de un ingrediente **le sirve al médico**: el expediente del ingrediente es el mismo para los dos oficios (si el dueño lo confirma, §12).
- La técnica combinada *Farmacología* (Medicina + Alquimia) da dosis con menos Toxicidad y remedios de liberación lenta (ver [Investigación y maestría](investigacion-y-maestria.md) §3).

## 9. Economía y roles

| Rol | Cómo gana | Con qué |
|---|---|---|
| **Alquimista con fama** | Su elixir con nombre se pide por su nombre ("para el Ojo de Ciénaga, ve con Mara"). Vende en su puesto o en una **botica** propia (ver [Propiedad y concesiones](propiedad-y-concesiones.md)), cobra regalías por sus patentes y vende copias de receta | Alquimia, maestría, patentes |
| **Herborista** | Abastece de hierbas y flores en sazón; los lotes de potencia alta valen el doble | Herboristería, el calendario de floraciones |
| **Cazador proveedor** | Glándulas, escamas y ojos de monstruo, por encargo | Desuello, [Cacerías](../06-contenido/cacerias.md) |
| **Minero y aguador** | Carbón, ámbar, sales, aguas especiales | Minería, exploración |
| **Joyero** | Frascos de vidrio de duna y de cristal tallado, que alargan la frescura | Joyería |
| **Escriba e informante** | Herbarios (copias de expediente) y notas de dónde y cuándo aparece cada ingrediente | Inscripción |
| **Médico** | Trata la dependencia y la intoxicación; compra remedios al por mayor | Medicina |

**Demanda por estación.** Cada estación mueve la mesa:
- **Invierno:** suben el Calor interno y el Pulmón limpio; escasean las hierbas, y quien guardó hierbas conservadas cobra caro.
- **Primavera:** llega la mandrágora; suben la Analgesia y la Calma.
- **Verano:** suben el Frescor y las Sales; se juntan escamas de salamandra y agua del Oasis Hondo.
- **Otoño:** Flor de Ciénaga y Miel negra; el festival de difuntos trae el único Polen del año.

**Sumideros.** La tasa del alambique público, la regalía de patente (con su impuesto), los frascos que se rompen, los elixires que caducan y las pruebas que fallan: todo saca oro y materiales del juego (ver [Economía](economia.md)).

## 10. Cómo se ve en el alambique

**Mezclar.** Ilse, alquimista Maestra (Alquimia 84), prueba tres ingredientes para la cacería de la Salamandra Madre:

```
⚗️ Alambique · Casa de Ilse (Alquimia 84 · Maestra)

Ingredientes (3/4):
 1. 🍯 Miel negra · Excelente · pot. 112 🌙
 2. 🦎 Escama de salamandra en muda · Buena · pot. 104 🌙
 3. 🌋 Flor de Ceniza · Notable · pot. 100

Comparten:
 ✅ Cicatrizante (1·3) → ❤️ Curación
 ✅ Renovadora (1·2)   → 💗 Regeneración
 ✅ Ignífuga (2·3)     → 🔥 Resistencia al fuego
 ❔ algo en común (2·3)
Modificadores: 🍬 Dulce (−5 🧪) · 🐾 Salvaje (+10 %, −estabilidad)
Secundarios: ninguno
Toxicidad estimada: 52

[🔥 Empezar]        [⚡ Rápido (Notable)]
[➕ Ingrediente]    [➖ Quitar uno]
[📜 Recetas]        [↩️ Volver]
```

**El minijuego.** Paso 4 de 6:

```
⚗️ Mezcla nueva · paso 4
Progreso    ▓▓▓▓▓▓▓░░░  70 %
Calidad     ▓▓▓▓▓▓░░░░  → Notable
Estabilidad ▓▓▓▓░░░░░░  Media
Durabilidad ●●○○   PA 96/240
Condición: ✨ EXCELENTE

[🔥 Calentar]   [🥄 Remover]
[💧 Enfriar]    [⚗️ Destilar ×2]
[👁 Observar]   [🍾 Embotellar]
```

**El resultado.** Al embotellar se revela la propiedad ❔ (Cálida, que daría ❄️ Calor interno). Como Ilse es Maestra y ya tiene tres efectos, el bot le pregunta si quiere cambiar alguno; ella se queda con los tres de combate.

```
✨ ¡Elixir nuevo! Nadie en el servidor lo había hecho.

🍷 ×3 · Calidad: Excelente · Estabilidad: Media
   (fresco 10 días)
❤️ Curación 21 % · 💗 Regeneración 3 %/ronda ×4
🔥 Resistencia al fuego −18 % ×3 rondas
🧪 Toxicidad 52
🔎 Descubriste: Escama de salamandra → Cálida
              Flor de Ceniza → Cálida

✍️ Ponle nombre (hasta 32 letras):
> Aliento de Brasa

📜 Registrado: «Aliento de Brasa de Ilse»
[⚖️ Patentar]       [🔒 Secreto de taller]
[📖 Publicar gratis] [📜 Ver receta]
```

**Las cuentas.** Tres efectos: 50 % de potencia cada uno. Calidad Excelente ×1,1 y Salvaje ×1,1: ×0,605 en total. La potencia de los lotes (promedio 105) queda dentro del redondeo. Curación 35 % × 0,605 = 21 %. Regeneración 5 % × 0,605 = 3 % por ronda. Fuego −30 % × 0,605 = −18 %. Toxicidad (40 + 30 + 25) × 0,5 + 10 − 5 = 52.

**Lo más simple.** Un Aprendiz junta Hierba curativa y Cardo rojo. Comparten solo Cicatrizante: sale una poción de vida casera de un efecto. La Amarga de la hierba y la Nerviosa del cardo no se cruzan, así que no hay secundarios.

## 11. Su fila en la red de sistemas

Como pide la [Red de sistemas](../00-vision/red-de-sistemas.md) §3:

| Sistema | Consume | Produce | Depende del farmeo | Depende de la fabricación | Depende de la progresión |
|---|---|---|---|---|---|
| **Alquimia y elixires** | Ingredientes (hierbas, hongos, partes de monstruo, minerales, aguas especiales), frascos, alambiques, tasas de uso, PI ⚕️ para las técnicas | Pociones, elixires con nombre, remedios de protocolo, recetas, copias y patentes, demanda de ingredientes de temporada, pacientes con dependencia o intoxicación | Herboristería, Desuello y caza, Minería, Pesca, Agricultura (cultivo de micelio y hierbas) | Alambique (Herrería e Ingeniería), frascos (Joyería), herbarios y copias (Inscripción), cinturones (Peletería) | Rango de Alquimia (efectos por elixir), expedientes de ingrediente, técnicas de la escalera, Maestría en Elixires |

## 12. Preguntas para el dueño

Propuestas para numerar en [Preguntas abiertas](../00-vision/preguntas-abiertas.md) con el siguiente número libre:

| Pregunta | Propuesta |
|---|---|
| ¿Cuántos efectos como máximo en un elixir? | 1 de Aprendiz a 3 de Gran Maestro, y un 4º solo de oficio o entorno con M10. Más efectos en una ronda serían demasiado fuertes |
| ¿Los elixires propios entran en la arena clasificada? | No: solo la lista normalizada. En guerra de castillos, sí, con potencia de guerra (2 efectos a calidad Notable) |
| ¿Un elixir se le puede dar a un aliado en combate? | No. Así no reemplaza a los sanadores ni a los soportes |
| ¿Cuánto duran frescos? | De 5 a 20 días según la estabilidad; las pociones de entrenador, 30 |
| ¿El expediente de un ingrediente es el mismo para el alquimista y para el médico? | Sí: un solo expediente por ingrediente, que llenan los dos oficios |
| ¿Dos jugadores pueden registrar con nombres distintos la misma combinación? | No: la combinación tiene un solo nombre, el de quien la registró primero. Las variantes de calidad o de orden no cuentan como receta nueva |

## 13. Orden de construcción sugerido

La alquimia entra en el juego como un parche de contenido nuevo (D-60, avisado a todos según D-67). Mientras se sigue ajustando la misma alquimia, los cambios son subparches de ese parche; un número de parche nuevo queda para un contenido diferente.

1. **Primero:** ingredientes con 4 propiedades, la regla de compartir y el modo rápido con 1 efecto. Ya existen la poción de vida y la Toxicidad en el código.
2. **Segundo:** nombre y registro de recetas; 2 efectos; secundarios; caducidad.
3. **Tercero:** minijuego del alambique, modificadoras, 3 efectos, tolerancia y dependencia, reglas de PvP.
4. **Cuarto:** patentes y copias de receta, técnicas de la escalera (*Destilado limpio*, *Maceración larga*, *Transmutación menor*), el 4º efecto con M10.

## 14. Ediciones pendientes en otros documentos

No se hicieron: este proceso solo escribe este documento.

- [ ] **[Profesiones](profesiones.md)**: §2.3, en la fila de Alquimia enlazar aquí y nombrar los elixires propios; §8, sumar a la Alquimia la dependencia por probar ingredientes; §9, sumar el rol "Alquimista con fama" (botica, recetas con nombre); §10, sumar la fila "Un elixir con nombre: Herborista + Cazador + Joyero (frascos) → Alquimista".
- [ ] **[Fabricación](fabricacion.md)**: §2, decir que el alambique usa la versión corta del minijuego con 6 botones, la barra de Estabilidad y las acciones de §5.3; §4, el descubrimiento de alquimia sigue la regla de las propiedades compartidas y enlaza aquí; §6, el alambique como estación con Tramo y calidad; §8, los elixires con nombre van al registro de obras maestras cuando son Obra Maestra. **Aviso:** el minijuego de §2 tiene 8 botones y D-66 pide de 4 a 6 en el mensaje; conviene que el dueño decida si se recorta en todos los oficios.
- [ ] **[Condiciones](../05-salud/condiciones.md)**: §4, enlazar aquí la fórmula de Toxicidad por efecto (§6.6), los efectos 🔁 y los números de tolerancia y dependencia (§6.7).
- [ ] **[Ronda y acciones](../04-combate/ronda-y-acciones.md)**: §4, en la tabla del cinturón sumar la fila "🍷 Elixir con nombre: varios efectos en una ronda; solo para quien lo bebe"; §11, nombrar la lista normalizada del cinturón de arena (§6.9).
- [ ] **[Inventario y mochilas](../03-personaje/inventario-y-mochilas.md)**: §4, decir que dos elixires del mismo nombre con distinta calidad van en casillas distintas.
- [ ] **[PvP](../06-contenido/pvp.md)**: guerra de castillos y asedios, sumar la potencia de guerra de los elixires (§6.9).
- [ ] **[Curación](../05-salud/curacion-y-tratamientos.md)**: §8, enlazar la tabla de caducidad (§6.8); sumar el tratamiento de la dependencia de elixires.
- [ ] **[Investigación médica](../05-salud/investigacion-medica.md)**: §2.4, decir que las propiedades de los ingredientes son las mismas que usa la Alquimia y enlazar la tabla de §3.3 (que completa las cuatro propiedades de los ingredientes que ya estaban).
- [ ] **[Escalera de conocimiento](escalera-de-conocimiento.md)**: §3.3, ficha de Alquimia, cambiar "el detalle irá en el documento de alquimia y elixires, en redacción" por el enlace a este documento, y nombrar qué hace cada técnica del camino (§5.3).
- [ ] **[Peligros del entorno](../05-salud/peligros-del-entorno.md)**: §7.2, decir que las pociones de entorno se pueden combinar en un elixir (§8.1).
- [ ] **[Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md)**: §4, nombrar los ingredientes de alquimia de cada estación (§9).
- [ ] **[Geografía y recursos](../02-mundo/geografia-y-recursos.md)**: §1, en la fila del Pantano y en las demás, nombrar los ingredientes de §3.3.
- [ ] **[Investigación y maestría](investigacion-y-maestria.md)**: §8.2, aclarar que un elixir con nombre se patenta por su combinación de ingredientes.
- [ ] **[README de 07 · Economía](README.md)**: sumar la fila de este documento.
- [ ] **[Decisiones](../00-vision/decisiones.md)** D-55: cambiar "Alquimia y elixires (en redacción)" por el enlace a este documento.
- [ ] **[Red de sistemas](../00-vision/red-de-sistemas.md)** §3: sumar la fila de §11.
- [ ] **[Glosario](../00-vision/glosario.md)**: propiedad (de efecto, negativa, modificadora, médica), elixir con nombre, reparto de potencia, estabilidad, fresco y pasado, potencia de guerra, lista normalizada.
- [ ] **[Preguntas abiertas](../00-vision/preguntas-abiertas.md)**: sumar las preguntas de §12.
