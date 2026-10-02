# Equipamiento

> **Módulo** [03 · Personaje](README.md) · **Depende de:** [Fabricación](../07-economia/fabricacion.md), [Jefes](../06-contenido/jefes.md) · **Alimenta a:** [Combate](../04-combate/README.md), [Heridas](../05-salud/heridas.md), [Economía](../07-economia/economia.md) · **Se conecta con:** [Inventario y mochilas](inventario-y-mochilas.md) · **Estado:** propuesta, con D-46 (6 botones) aplicada. Del 2-oct-2026: ranuras para gemas solo en armaduras y armas (D-199, confirmada, §3.1) y qué estadística da cada tipo de armadura (D-206, provisional, §2.1)

**De dónde sale.**
- *World of Warcraft*: 16 ranuras, tipos de armadura, calidades por color, nivel de objeto, conjuntos, gemas, encantamientos, pistas de mejora y Gran Tesoro semanal.
- *Albion Online*: tiers de T1 a T8, encantamiento de .1 a .4, calidad al fabricar, durabilidad y destrucción. Casi todo lo fabrican jugadores, y los jefes sueltan **artefactos** que sirven de ingrediente.
- *Elden Ring*: la carga de equipo decide cómo te mueves, y el **Recuerdo** del jefe se cambia por un objeto concreto.
- *Diablo* y *Path of Exile*: afijos.
- *Star Wars Galaxies*: el nombre del artesano grabado en el objeto.

---

## 1. Ranuras

Son las 16 de WoW, agrupadas para que se lean bien en un teléfono. Cada ranura de armadura está atada a la zona del cuerpo que protege (ver [Heridas](../05-salud/heridas.md)).

| Grupo | Ranura | Protege |
|---|---|---|
| **Armas** | Mano principal · Mano secundaria (o arma a dos manos) | — |
| **Armadura** | Cabeza | Cabeza |
| | Hombros · Pecho | Torso |
| | Cintura | Abdomen |
| | Muñecas · Manos | Brazos |
| | Piernas · Pies | Piernas |
| | Espalda (capa) | Clima (frío, calor, lluvia) |
| **Joyas** | Cuello · Anillo ×2 | — |
| **Abalorios** | Abalorio ×2 | Efecto activable o pasivo |
| **Utilidad** | Herramienta de oficio ×2 · Mochila · Cinturón · Montura | — (ver §8) |
| **Cosmético** | Tabardo · Camisa · Apariencias | — |

Se puede lanzar con 10 ranuras (armas, cabeza, hombros, pecho, manos, piernas, pies, capa, anillo, cuello) y llegar a las 16 en la beta.

## 2. Tipos de armadura y carga

| Tipo | Clases que la dominan | Protege mejor contra | Peso |
|---|---|---|---|
| **Tela** | Mago, Sacerdote, Brujo, Nigromante | Daño místico | Ligero |
| **Cuero** | Pícaro, Druida, Monje, Cazador de Demonios, Bardo | Perforación; elemental a medias | Medio-ligero |
| **Malla** | Cazador, Chamán, Evocador | Corte, perforación | Medio |
| **Placas** | Guerrero, Paladín, Caballero de la Muerte | Corte (mucho), perforación | Pesado |

- **Dominio:** tu clase domina un tipo de armadura y recibe un bono si llevas todo el conjunto de ese tipo, como la especialización de armadura de WoW.
- **Libertad con costo:** puedes ponerte cualquier armadura, pero sin dominio no recibes el bono y el **peso** te castiga. Un mago en placas es posible, y es lento.
- **Carga** (Elden Ring): el peso del equipo frente a tu capacidad (que sale de la raza y el aguante).

  | Carga | Efecto |
  |---|---|
  | Ligera (<30 %) | +iniciativa; Huir falla menos |
  | Media (30-70 %) | Normal |
  | Pesada (70-100 %) | −iniciativa; Aguante máximo −1 (hay para una respuesta menos; ver [Ronda y acciones](../04-combate/ronda-y-acciones.md)) |
  | Sobrecargado (>100 %) | No puedes esquivar (ni con respuestas 💨 ni con 🌀 Esquivar) y Huir siempre falla |

### 2.1 Qué estadística da cada tipo (D-206, provisional)

El dueño pidió, el 2-oct-2026, la estadística principal de cada tipo, sus clases, su rol y qué mejora cada pieza. Lost Realms **no tiene fuerza, agilidad ni intelecto**: sus estadísticas de combate son ❤️ **vida**, ⚔️ **ataque** (un solo valor para lo físico y lo mágico), 🛡️ **armadura** (nunca más de 60 %) y ⚡ **iniciativa** (quién actúa primero). Las curaciones crecen con la vida máxima.

| Tipo | Estadística que prevalece | Clases | Roles | Qué mejora cada pieza |
|---|---|---|---|---|
| 🛡️ Placa | 🛡️ armadura y ❤️ vida | Guerrero, Paladín, Caballero de la Muerte | Tanques y cuerpo a cuerpo pesado; también curación (Paladín) y soporte | La armadura más alta de los cuatro y vida; poco ataque (guantes) |
| ⛓️ Malla | ⚔️ ataque con 🛡️ armadura media | Cazador, Chamán, Evocador | Daño a distancia, curación y soporte (híbridos) | Armadura media y ataque |
| 🦺 Cuero | ⚡ iniciativa y ⚔️ ataque | Pícaro, Monje, Druida, Cazador de demonios, Bardo | Daño cuerpo a cuerpo rápido, defensa por esquiva, curación y soporte | Iniciativa y ataque; armadura baja |
| 👘 Tela | ⚔️ ataque (poder mágico) y ❤️ vida (la curación crece con la vida máxima) | Sacerdote, Mago, Brujo, Nigromante | Daño mágico, curación y soporte | El ataque más alto y vida; armadura mínima |

- **Por qué así.** Sigue lo que ya tienen las clases de base: las de placa tienen la armadura más alta (0,14 a 0,22), las de malla, media (0,12 a 0,14), las de cuero, baja (0,10; sus especializaciones de defensa, 0,16 a 0,20) y la mayor iniciativa (11 a 14), y las de tela, la más baja (0,05; las de defensa, 0,12 a 0,14).
- **Hoy en el juego** los cuatro tipos dan lo mismo por pieza (el pecho, vida y armadura; los guantes suman ataque; las piezas de artesano, un poco de ataque) y solo la clase decide cuál rinde al 100 %; otro tipo rinde la mitad (D-83).
- **Cuándo se aplica:** con el código de los oficios, y medido con las herramientas de balance (`tools/sim.py`, `tools/balance_report.py`) para que ninguna clase se vuelva más fuerte por sorpresa. Los IDs de las piezas no cambian. Se confirma en E-168.
- **Quién fabrica cada tipo:** placa, la 🔨 Herrería; cuero, la 🦺 Peletería; tela, la 🪡 Sastrería; malla, un oficio propio, el ⛓️ Mallero (D-194). El 2-oct el dueño dijo "el Herrero hace placa y malla"; no se decidió y quedó en E-143.

## 3. Qué define a un objeto

Cada objeto tiene siete propiedades. En la pantalla se ven dos o tres; el resto está en el detalle.

| Propiedad | Valores | De dónde sale | Qué decide |
|---|---|---|---|
| **Anillo** | T1 a T10, uno por anillo (I a X) | Albion (tiers) | La base de sus números y el material con que se hace |
| **Calidad** (si es fabricado) | Normal · Buena · Notable · Excelente · Obra Maestra | Albion (calidad al fabricar) | Bono sobre la base; sale de la [fabricación](../07-economia/fabricacion.md) |
| **Rareza** (si es botín) | Común · Poco común · Raro · Épico · Legendario · Reliquia | WoW (colores) | Cuántos afijos tiene |
| **Encantamiento** | +0 a +4 | Albion (.1 a .4) | Cada nivel sube el Poder de Objeto como un anillo parcial. Se hace infundiendo runas, almas y reliquias |
| **Mejoras** | 0 a 3 | Pistas de mejora de WoW | Cada mejora cuesta Esencia y material, y nunca llega a la base del anillo siguiente |
| **Afijos** | 0 a 4 líneas | WoW (secundarias), Diablo | Crítico, Celeridad, Maestría, Versatilidad, resistencias, protección de zona, robo de vida… |
| **Engarces** (ranuras para gemas) | 0 a 3 (D-199: solo armaduras y armas de buena calidad) | WoW (gemas) | Gemas que refina la 💍 Joyería (D-198) |

Además: **durabilidad** (actual y máxima), **peso**, **atadura** y **firma del artesano**.

### 3.1 Ranuras para gemas (D-199, 2-oct-2026)

Aquí "ranura" es el hueco donde va una gema (lo que la tabla llama engarce), no la ranura del cuerpo del §1.

- **Llevan ranura:** todas las piezas de armadura y las armas.
- **Nunca llevan ranura:** los anillos, collares, amuletos ni ningún accesorio. Su valor está en los bonos con que los crea el 💍 Joyero o el ⚗️ Alquimista (los amuletos pasan a la Alquimia, D-194).
- **Solo en piezas de buena calidad:** las comunes no llevan.
- **Cuántas (provisional, recomendación de E-149):** 1 en las piezas buenas y hasta 3 en las mejores. El ✨ encantamiento sigue aparte: una pieza puede tener gemas y su encantamiento.
- **Las gemas** las refina el Joyero desde la mena que junta el ⛏️ Minero (D-198).

### Poder de Objeto (PO)

Todo lo anterior se resume en un número, el **Poder de Objeto** (como el nivel de objeto de WoW o el *item power* de Albion). Lo usan el buscador de grupos para los requisitos mínimos y el mercado para ordenar.

```
⚔️ Espada Larga de Acero Estelar   [PO 412]
T5 · Excelente · +2 · Mejoras 1/3
Forjada por Lisbeth la Herrera ✒️
+38 Fuerza · +Crítico · +Protección de brazo
Técnica: Tajo Circular ⚔ (golpea a toda la vanguardia)
Durabilidad 84/100 (máx. 96) · 4,2 kg · Libre
```

## 4. Durabilidad: el equipo se gasta de verdad

**De dónde sale.** En Albion y EVE el equipo se pierde, se rompe y se reemplaza, y eso sostiene la economía durante años. En WoW casi nunca se pierde, y la fabricación depende de que llegue la próxima expansión.

- Cada objeto tiene **durabilidad actual**, que baja al combatir y al caer, y **durabilidad máxima**.
- **Reparar** devuelve la actual, cuesta oro (sumidero) y **baja un poco la máxima**. Un herrero de mucho nivel repara perdiendo menos máxima, así que su servicio vale más que el del PNJ.
- Cuando la máxima llega a 0, el objeto se rompe **para siempre**. Se puede desmontar para recuperar parte del material.
- Resultado: una pieza normal dura varias semanas de uso intenso. Siempre hay demanda de armas y armaduras, **aunque no salga contenido nuevo**.

## 5. Atadura

| Tipo | Regla | Para qué objetos |
|---|---|---|
| **Libre** | Se puede comerciar siempre | Casi todo lo fabricado, materiales, consumibles, **artefactos de jefe** |
| **Ligado al equipar** | Libre hasta que alguien se lo pone | Piezas fabricadas con artefactos (armas únicas) |
| **Ligado al recoger** | No se comercia | Solo recompensas de prestigio: cosméticos de Pionero, títulos, objetos de logro |

La mayor parte del poder se **fabrica y se comercia**. El jefe no te da la espada: te da el **artefacto** para que un herrero la haga.

## 6. De dónde sale el equipo

| Fuente | Qué da | Por qué |
|---|---|---|
| **Artesanos** | La mayoría de las piezas de todos los anillos | La economía gira alrededor de ellos (Albion) |
| **Jefes** | **Artefactos** (la Garra del Wyrm, el Corazón del Coloso), que son ingredientes de armas y armaduras únicas con técnicas propias; **planos** raros; materiales de partes rotas (ver [Daño y estados](../04-combate/dano-y-estados.md)) | Une el botín de jefe de WoW con la fabricación de Albion: importa matar al jefe, y también el herrero |
| **Recuerdos del Guardián** | La primera victoria contra cada Guardián da un Recuerdo **garantizado**, que se cambia por una de dos piezas icónicas de ese jefe | Elden Ring: recompensa determinista para lo más importante |
| **Mercado Negro** | Las piezas que sueltan los monstruos comunes **las fabricaron jugadores** y el Mercado Negro las compró | Albion: hasta el botín del mundo depende de los artesanos (ver [Economía](../07-economia/economia.md)) |
| **Tienda PNJ** | Equipo básico T1 y T2 | Para empezar |
| **Vendedores de reputación y PvP** | Piezas con afijos específicos | Metas de largo plazo |

## 7. Técnicas de equipo

Cada tipo de arma da **una técnica** y cada pecho o par de botas da **otra**. Con la barra de 6 botones (D-46), las técnicas ya no son botones fijos:

- **Una técnica puede ocupar una de tus 3 casillas de habilidad** (P-68), en lugar de una habilidad de clase. Solo una: la clase sigue siendo lo principal.
- **Se elige fuera de combate**, junto con tus configuraciones de talentos (ver [Talentos](talentos.md)). Si cambias de arma o de armadura, la técnica cambia sola.
- **Las técnicas marcadas 🛡 o 💨 son respuestas:** se resuelven antes que los golpes y cuestan Aguante, como las de clase. Le dan a cualquier clase otra forma de contestar un aviso (ver [Ronda y acciones](../04-combate/ronda-y-acciones.md)).
- **Sin técnica en la barra, el arma igual cuenta:** decide el tipo de daño y el alcance de tu ⚔️ Atacar (con lanza, llegas a la retaguardia desde la vanguardia).

| Pieza | Técnica | Tipo |
|---|---|---|
| Espada larga | *Tajo Circular*: golpea a toda la vanguardia | ⚔ Ataque |
| Lanza | *Estocada Profunda*: alcanza la retaguardia desde la vanguardia | ⚔ Ataque |
| Maza | *Quebrantahuesos*: mucho daño a la postura y más probabilidad de fractura | ⚔ Ataque |
| Hacha | *Hendidura*: abre una herida que sangra | ⚔ Ataque |
| Dagas | *Puñalada Trapera*: crítico garantizado por la espalda (si el objetivo mira a otro) | ⚔ Ataque |
| Arco largo | *Flecha Clavadora*: el objetivo no puede cambiar de fila | ⚔ Ataque |
| Ballesta | *Virote Perforante*: ignora parte de la armadura | ⚔ Ataque |
| Bastón | *Remanso*: recupera maná y baja el estrés propio | ✦ Recurso |
| Varita | *Chispa*: ataque a distancia gratis que acumula estado elemental | ⚔ Ataque |
| Escudo torre | *Muro*: la fila entera recibe menos daño esa ronda | 🛡 Respuesta |
| Pecho de placas | *Resistir*: ignoras derribos y empujones esa ronda | 🛡 Respuesta |
| Pecho de malla | *Cota Tensa*: la próxima herida baja un nivel de gravedad | 🛡 Respuesta |
| Pecho de cuero | *Capa de Humo*: esquiva garantizada esa ronda | 💨 Respuesta |
| Túnica | *Barrera Rúnica*: escudo que absorbe magia | 🛡 Respuesta |
| Botas de placas | *Carga*: cambia de fila y pega en la misma jugada | ⚔ Ataque y movimiento |
| Botas de cuero | *Paso Ligero*: +iniciativa durante 2 rondas | ✦ Iniciativa |

Las armas de artefacto tienen técnicas únicas. La Garra del Wyrm da *Barrido de Dunas*: arena que ciega a la vanguardia.

**Por qué conviene.** El equipo importa por lo que hace, no solo por sus números (Albion), y eso le da demanda a cada tipo de arma y armadura. Pero la técnica compite por una casilla con las habilidades de clase, así que nunca suma botones.

## 8. Cinturón y mochila

Dos ranuras de utilidad deciden qué llevas encima (D-47). El detalle de capacidades, tipos y niveles está en [Inventario y mochilas](inventario-y-mochilas.md).

| Ranura | Qué hace | Quién la fabrica |
|---|---|---|
| 🎒 **Mochila** | Lo que cargas fuera de combate. Su capacidad sube por niveles, y hay tipos según el oficio (herborista, minero, médico, comerciante…) | Peletería o Sastrería |
| 🪢 **Cinturón** | Las pocas casillas de objetos que se pueden usar en combate con el botón 🎒 Mochila: pociones de vida y de resistencia, remedios, vendas, bombas, comida rápida. Un cinturón mejor tiene más casillas | Peletería |

- **No confundir con la pieza de cintura.** La cintura es armadura y protege el abdomen; el cinturón es una ranura de utilidad: no protege, carga.
- **En combate solo se usa el cinturón.** Se prepara antes de salir y se rellena solo desde la mochila al terminar cada pelea (ver [Ronda y acciones](../04-combate/ronda-y-acciones.md)).
- **Se fabrican y se mejoran con materiales y moneda del juego.** El dinero real no compra casillas ni capacidad (D-43; ver [Monetización](../07-economia/monetizacion.md)).

## 9. Suerte, pero con red

**El problema de WoW:** semanas sin el objeto que necesitas.

1. **Protección contra mala racha.** Cada vez que un jefe no te da nada útil, sube tu probabilidad la próxima vez. WoW la agregó en 2013 a sus tiradas extra.
2. **Recuerdos del Guardián**, deterministas (§6).
3. **Tesoro Semanal.** Según lo que hiciste en la semana (mazmorras, bandas, Profundidades, PvP) se abren hasta 9 casillas y eliges **una** recompensa. Si ninguna te sirve, te llevas su valor en Esencia. Es el Gran Tesoro de WoW.
4. **Mejoras con Esencia.** Lo que no sale, se mejora.
5. **Tirada a la vista.** En grupo, "Necesidad / Codicia" se tira con el 🎲 nativo en el chat (ver [Gremios y social](../08-social/gremios-y-social.md)).

## 10. Apariencias y colecciones

- **Apariencias textuales.** Cada pieza tiene una descripción visual, y puedes ponerle a tu equipo la apariencia de otra pieza que hayas tenido (la transfiguración de WoW). Todo esto se ve en tu perfil y en las citas de combate.
- **Colección de apariencias** compartida por toda la cuenta.
- **Tarjeta de perfil** en imagen (fase tardía): tu equipo, tus cicatrices y tus títulos en una carta lista para reenviar.

Ver P-14, P-34 y P-68 en [Preguntas abiertas](../00-vision/preguntas-abiertas.md).

## 11. Lo que ya está en el juego (parches 0.6 y 0.7.2, D-77 y D-83; equipo hasta el nivel 100, D-110 y D-113; encantamientos, pieza mejor y artesano en todas las ranuras, fase 2 de D-115)

La capa simple (D-44). Todo lo de arriba sigue siendo el plan; esto es lo que hoy funciona en @LostRealmsbot.

| Pieza del sistema | En el juego | Dónde está |
|---|---|---|
| **Ranuras** | 7: ⚔️ arma, ⛑️ cabeza, 🥋 pecho (`armadura`), 🧤 manos, 👖 piernas, 🥾 pies y 💍 joya (D-83) | `content/balance.yaml` → `gear.slots` |
| **Tipos** | Armadura de tela, cuero, malla o placas según la clase (tabla del §2). Armas: espada, daga, arco o bastón; cada clase usa una o dos. Las joyas sirven a todos | `gear.armor_by_group`, `gear.weapons_by_group` |
| **Requisitos** | Solo el **nivel** impide ponerse una pieza (D-83). Juegas como quieras: una pieza que no es de tu clase se puede llevar, pero rinde la mitad (`gear.off_type_factor`). Es la "libertad con costo" del §2, sin el peso todavía | `engine/hero/gear.py` → `can_use`, `suits`, `piece_stats` |
| **El juego aconseja** | Cada pieza dice ✅ te sirve (es de tu clase), ⚠️ no es de tu clase (rinde la mitad) o 🔒 desde el nivel N. Al verla se compara con lo que llevas (⬆️ mejor, ⬇️ peor) y muestra cuánto te da a ti. Tú decides | `engine/service/game.py` → `_gear_view`, `_item_view` |
| **⬆️ Tienes una pieza mejor (fase 2 de D-115)** | Cuando te llega una pieza (botín de una pelea, del 👹 cofre de un campamento enemigo o del Guardián, o algo que fabricaste, también una ✒️ obra maestra) que es **mejor** que la que llevas en esa ranura **y la puedes usar**, el mensaje lo dice ("⬆️ ¡Tienes una pieza mejor! … supera a lo que llevas en ⛑️ Cabeza: +2% vida") y ofrece el botón **🔁 Equipar** (un toque y te la pones; va primero y, si no entra en los 4 botones, toma el lugar de 🔨 Hacer todo). En las peleas automáticas de un lote, el aviso va en el resumen del final (sin botón). En 🔁 Equipar, las piezas mejores salen primero, marcadas con ⬆️. **Mejor** = tu nivel la permite, es de tu tipo (tu armadura, tu arma o una joya) y su **puntaje** pasa al de la que llevas (sin nada puesto, cuenta 0). **Puntaje** = ataque % + vida % + 2 × defensa de lo que la pieza te da de verdad (la mitad si no es de tu tipo, más su ✨ encantamiento): es el mismo número que ya usaba la comparación ⬆️/⬇️. Nunca se pone sola (salvo en una ranura vacía, como siempre): no hay opción en ⚙️ Opciones para eso | `balance.yaml` → `gear.score`; `engine/hero/gear.py` → `gear_score`, `piece_score`, `is_better`; `engine/service/game.py` → `_better_piece`, `_better_line`, `_better_action` (en `_end_combat`, `_auto_combat` y `_make`) |
| **✨ Encantamientos (fase 2 de D-115)** | Cada pieza puede llevar **un** encantamiento que suma mientras la llevas puesta; la ranura decide cuál: ⚔️ **Filo** (arma y manos, ataque), ❤️ **Vigor** (pecho, cabeza y piernas, vida) y 🛡️ **Guarda** (pies y joya, defensa, desde el rango 25). Vale lo que da tu rango de ✨ Encantamiento al hacerlo: +1 % (rangos 1 a 25), +2 % (26 a 75), +3 % (76 a 100); la Guarda, +1 de defensa (25 a 50) y +2 (51 a 100). Encantar otra vez **reemplaza** al anterior (nunca se suma) y solo se puede si el número sube. Con las 7 ranuras encantadas al rango 100: +6 % de ataque, +9 % de vida y +4 de defensa (la defensa sigue sin pasar el 60 %). Se ve con ✨ junto al nombre en 🛡️ Equipo y en 🔁 Equipar, y en la pieza ("✨ Encantamiento: ⚔️ Filo +2% ataque"). Cómo se hace y qué cuesta: [Profesiones](../07-economia/profesiones.md) §0.5 | `balance.yaml` → `enchanting`; `Hero.gear_enchants`; `engine/hero/gear.py` → `enchant_stats`, `real_stats`, `gear_bonus` |
| **Niveles de pieza (D-110)** | 14 en el botín: ⚪ común (nivel 1), 🟢 poco común (3), 🔵 rara (5), 🟣 épica (8) y, desde ahí, una pieza cada 10 niveles (10, 20 … 100) en las 7 ranuras y los 4 tipos de armadura y de arma. El equipo sigue mejorando hasta el nivel 100. Sin afijos todavía | `content/items.yaml` (sección D-110 / D-113, al final) |
| **Bonos** | Arma: +4/8/12/17 % de ataque hasta el nivel 8 y de +19 % (nivel 10) a +35 % (nivel 100). Pecho: +5/9/14/20 % de vida y +1/2/3/4 % de defensa; de +22 % a +40 % de vida y hasta +6 % de defensa al 100. Joya: vida y ataque (+21 % y +16 % al 100). Cabeza, manos, piernas y pies, menos. Con las 7 ranuras del botín: +29 % de ataque, +61 % de vida y +10 de defensa al nivel 8; +61 %, +124 % y +15 al 100. La defensa total nunca pasa de 60 % | `items.yaml` → `stats`; `gear.armor_cap` |
| **Botín (D-113)** | El 15 % de las victorias suelta una pieza (desde el nivel 10, el **10 %**: el botín suelta menos), de nivel cercano al del enemigo (de −4 a +1; si ahí no hay ningún nivel de pieza, el más cercano por debajo). El 70 % de las piezas es de tu tipo; lo raro sale menos. Desde el nivel 10 el botín llega como mucho a 🔵 raro. El aviso del combate solo dice que cayó algo; qué es, se mira en 👤 Héroe → 🛡️ Equipo, marcado con 🆕 (D-83) | `gear.drop_chance`, `gear.high_level_drop`, `gear.level_window`, `gear.for_you_chance`, `gear.rarity_weight`; `engine/hero/gear.py` → `roll_gear`, `drop_chance_for` |
| **Lo mejor lo fabrican los jugadores (D-113)** | En arma, pecho y joya, la mejor pieza de cada nivel desde el 3 es de artesano: rango 1 = la poco común del nivel 3 y un bono chico; rango 25 = la rara del 5 y algo más; rango 50 = la épica del 8 y algo más; y de los rangos 55 a 100, una 🟣 épica por cada nivel de pieza del 10 al 100 (rango 55 → nivel 10 … rango 100 → nivel 100), con ~10 % más que el botín de su nivel y un bono (vida en las armas, ataque en el pecho, defensa en la joya). **Desde la fase 2 de D-115, también en cabeza, manos, piernas y pies:** una pieza de artesano por tipo de armadura en los niveles 3, 5 y 8 (rangos 1, 25 y 50) y del 10 al 100 (rangos 55 a 100), con cada bono del botín de su nivel × 1,1 desde el 10 y un bono que el botín no tiene (+1 % de ataque en cabeza, piernas y pies, +2 % desde el nivel 60; +1 de defensa en las manos). Telas de la 🪡 Sastrería, cuero y malla de la 🦺 Peletería, placas de la 🔨 Herrería (208 piezas nuevas, cada una con su receta y su ✒️ obra maestra). Recetas en [Profesiones](../07-economia/profesiones.md) §0.1 | `items.yaml` (`source: crafted`), `content/professions.yaml`; `tests/test_balance_d110.py`, `tests/test_oficios_equipo.py` |
| **✒️ Obra maestra (D-116)** | Al fabricar una pieza de artesano puede salir **obra maestra**: la misma pieza con +10 % en cada bono y un bono más (arma +1 de defensa, pecho +2 % de ataque, joya +2 % de vida; desde la fase 2 de D-115, cabeza, piernas y pies +1 % de ataque y manos +1 de defensa), firmada por quien la hizo ("✒️ Obra maestra de Lyra" en 🔁 Equipar y en la pieza; su nombre lleva ✒️). Sale hasta el 15 % de las veces en los arcos y bastones de la 🪑 Carpintería y hasta el 5 % en las piezas de los demás oficios, según el rango. El mercader paga 25 % más por ella. Nunca sale en el botín al azar ni en el equipo inicial (`source: masterwork`). Ver [Profesiones](../07-economia/profesiones.md) §0.4 | `items.yaml` + `balance.yaml` → `masterwork` (las piezas `<id>_obra` las arma `engine/professions/rules.py` al cargar); `Hero.gear_signatures` |
| **Equipo inicial** | Arma y pecho básicos de tu clase, ya puestos. Los héroes que existían antes de la 0.6 los recibieron una vez | `starter_gear` |
| **Se pone solo** | Solo la primera pieza de una ranura vacía, aunque no sea la mejor para ti (si no tenías botas, te pone las que caen). Si ya llevas algo ahí, la pieza nueva va a la mochila (D-83) | `auto_equip` |
| **Dónde se ve** | 👤 Héroe → 🎒 Mochila → 🛡️ Equipo: lo que llevas puesto, una línea por pieza (icono, nombre y lo que te da). Desde ahí, 🔁 Equipar lista lo que tienes en la mochila para ver sus bonos, el consejo y ponértelo, o quitarte lo puesto. La ficha del héroe ya no muestra el equipo (D-86) | Cliente de Telegram |
| **Recuerdo del Guardián (D-82)** | La primera victoria de cada héroe contra Raigambre, el primer Guardián, da un 🌰 Recuerdo garantizado (§6). Se cambia en 🎒 Mochila por **una** de dos piezas 🟣 únicas "para ti": el arma de tu tipo principal o la armadura de tu tipo, desde nivel 5 (+15 % de ataque, o +17 % de vida y +4 % de defensa). Esas 8 piezas llevan `source: guardian` y nunca salen en el botín al azar | `items.yaml` → `recuerdo_raigambre`, `guardian_*`; `gear.py` → `source_choices`; [Jefes](../06-contenido/jefes.md) §6 |

**Cómo se mide:** `tools/balance_report.py` compara cada especialización con el equipo inicial, con el botín de su nivel y con el de artesano y los beneficios de oficio, del nivel 1 al 100 (registro en [Balance](balance.md) §7, "pasada de balance de clases y roles").

**Falta, en este orden:** más ranuras, durabilidad y reparación (D-113), elegir el encantamiento y encantamientos más fuertes (capa profunda del ✨ Encantamiento), afijos y la carga. Fabricar equipo ya está (D-109, ver [Profesiones](../07-economia/profesiones.md) §0.1), también en cabeza, manos, piernas y pies (fase 2 de D-115).
