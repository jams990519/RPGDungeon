# Bestiario

> **Módulo** [06 · Contenido](README.md) · **Depende de:** [Daño y estados](../04-combate/dano-y-estados.md), [Ronda y acciones](../04-combate/ronda-y-acciones.md), [Avisos y tácticas](../04-combate/avisos-y-tacticas.md), [Torre y pisos](../02-mundo/torre-y-pisos.md), [Geografía y recursos](../02-mundo/geografia-y-recursos.md), [Enfermedades](../05-salud/enfermedades.md) · **Se conecta con:** [Cacerías](cacerias.md), [Jefes](jefes.md), [Heridas](../05-salud/heridas.md), [Mente](../05-salud/mente.md), [Rasgos adquiridos](../05-salud/rasgos-adquiridos.md), [Peligros del entorno](../05-salud/peligros-del-entorno.md), [Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md), [Equipamiento](../03-personaje/equipamiento.md), [Fabricación](../07-economia/fabricacion.md), [Profesiones](../07-economia/profesiones.md), [Descubrimiento y colecciones](../03-personaje/descubrimiento-y-colecciones.md) · **Estado:** propuesta

Pediste una **alta variedad de monstruos**, incluso con la posibilidad de pegarte enfermedades o cualquier otro efecto. Este documento arma el bestiario completo: cómo se describe un monstruo, cómo se comporta por turnos, qué contagia, qué deja y cómo cambia el mundo según se lo cace o no. Los jefes están en [Jefes](jefes.md); aquí están todos los demás.

**De dónde sale.**
- *Monster Hunter*: partes rompibles con materiales propios, monstruos que cojean y vuelven a su nido cuando están débiles, peleas de territorio entre monstruos (*World*), versiones "templadas" más fuertes (*World*) y el virus del Frenesí de *Monster Hunter 4*, que da un bonus a quien lo supera a tiempo.
- *Dark Souls* y *Elden Ring*: cofres que son monstruos (mímicos), estados por acumulación (la maldición de los basiliscos en *Dark Souls*, la podredumbre escarlata en *Elden Ring*) y enemigos que solo salen de noche, como los jinetes nocturnos (*Night's Cavalry*) de *Elden Ring*.
- *Darkest Dungeon*: enfermedades que se contraen en las expediciones y se tratan en el sanatorio, estrés por enemigos de terror, y un jefe errante (*The Collector*) que aparece sin aviso.
- *Diablo* y *Path of Exile*: monstruos campeones y únicos con modificadores (más rápido, más fuerte, "encantado de fuego", que estalla al morir), monstruos únicos con nombre propio, y el duende del tesoro (*Treasure Goblin*) de *Diablo III*, que huye cargado de botín. En *Path of Exile* (liga Bestiario, 2018) se capturan bestias con redes para usarlas en recetas.
- *Dragon Quest*: el limo metálico, casi invencible, que huye enseguida y da muchísima experiencia.
- *Pokémon*: una tabla de tipos con debilidades y resistencias que se aprende, y la Pokédex, que se llena viendo y atrapando.
- *The Witcher*: un bestiario por familias (necrófagos, espectros…) con aceites de espada contra cada familia (*The Witcher 3*). En el primer *The Witcher*, ciertos ingredientes solo se sacaban de un monstruo si habías estudiado sobre él.
- *Fear & Hunger*: combate por turnos en el que se le cortan miembros al enemigo para quitarle ataques, y un acechador (el Crow Mauler) que te persigue por el mapa.
- *Middle-earth: Shadow of Mordor*: el sistema Némesis. El orco que te mata asciende, te recuerda y se vuelve más fuerte.
- *Terraria*: la Corrupción y el Carmesí, biomas que se extienden solos si nadie los frena.
- *Dungeons & Dragons*: el mímico, el cofre que muerde.
- *World of Warcraft*: élites raros que aparecen cada tanto, y monstruos que intentan huir con poca vida.
- *Final Fantasy*: la Bomba, que se autodestruye.
- *Skyrim*: cada criatura contagia sus propias enfermedades (ver [Enfermedades](../05-salud/enfermedades.md)).

**Por qué conviene.**
- Un monstruo no es una bolsa de vida: es **un problema distinto** que se resuelve leyendo, preparándose y eligiendo bien.
- Cada familia pide otra cosa (fuego, plata, luz, máscaras, apuntar a las piernas) y **cada cosa la fabrica un oficio**.
- Las enfermedades de monstruo le dan trabajo a médicos y alquimistas.
- Las poblaciones hacen que el mundo cambie según lo que cazan los jugadores.

---

## 1. Anatomía de un monstruo

### 1.1 La ficha

Todo monstruo se describe con los mismos campos. El jugador los va descubriendo con el **conocimiento** (§1.5).

| Campo | Qué dice | Ejemplo (Necrófago) |
|---|---|---|
| **Familia** | Una de las 19 (§4). Decide debilidades, fobia y remedio de caza | No-muertos |
| **Talla** | Diminuta a Enorme (§1.2). Decide filas, Postura y partes | Mediana |
| **Hábitat** | Terreno, tramo y color de zona | 🐸 Pantano · tramo IV · zonas 🟡🔴 |
| **Horario** | Día, noche, clima o estación en que sale | Noche y niebla |
| **Comportamiento** | Su arquetipo (§2) | Carroñero |
| **Repertorio** | 2 a 4 movimientos, con sus avisos (§1.3) | Zarpa sucia, Festín, Remate |
| **Partes rompibles** | Qué se rompe y qué movimiento pierde | Garras (pierde *Zarpa sucia*) |
| **Estados que aplica** | Barras de acumulación que llena (ver [Daño y estados](../04-combate/dano-y-estados.md)) | 🟤 Podredumbre |
| **Contagio** | Qué enfermedad pega y por qué vía (§5 y §6) | 🦠 Podredumbre Gris, por zarpa |
| **Mente** | Terror (0 a 3) y fobia que puede dejar (§1.4) | Terror ●● · *Miedo a los muertos* |
| **Débil / resiste** | Por tipo de daño (§3) | Débil: fuego, sagrado · Resiste: veneno, sangrado |
| **Qué deja** | Materiales, partes, equipo, muestras, artefactos (§9) | Uñas de necrófago, bilis negra |
| **Conocimiento** | Tu nivel con esa especie (§1.5) | ★★★☆☆ |

**Hábitat y entorno.** Un monstruo nativo no sufre los peligros de su terreno (ver [Peligros del entorno](../05-salud/peligros-del-entorno.md)). Fuera de él, sí. Atraer con cebo a una bestia volcánica hasta un nodo frío la debilita, y eso es una táctica.

Así se ve la ficha con `/bestiario`:

```
📖 Bestiario — Necrófago           Conocimiento ★★★☆☆
No-muertos · Mediana · Terror ●●○
🐸 Pantano · tramo IV (pisos 31-40) · 🟡🔴
🌙 Noche y niebla · Carroñero

Repertorio
 • Zarpa sucia  🦠 Podredumbre Gris
   "olfatea la herida abierta de X"
 • Festín  (se cura comiendo un cadáver)
   "se arrastra hacia el cuerpo caído"
 • Remate  (golpe a un derribado)
   "se agazapa junto a X, que está en el suelo"

Débil: 🔥 Fuego · ✨ Sagrado
Resiste: 🟢 Veneno · 🩸 Sangrado (no sangra)
Partes: Garras → pierde Zarpa sucia
        Mandíbula → pierde Festín
Deja: uñas de necrófago · bilis negra · 🃏 carta (rara)
Puede dejar: Miedo a los muertos
Remedio: Aceite de necrófagos (Alquimia)

[⚔️ Cazar] [🧾 Contratos] [🗺 Dónde vive]
```

### 1.2 Talla, filas y vida

El bando enemigo también tiene **vanguardia y retaguardia** (ver [Ronda y acciones](../04-combate/ronda-y-acciones.md)). La talla decide cuánto ocupa y cuánto aguanta.

| Talla | Ejemplos | Ocupa | Postura | Partes rompibles | Vida (en vidas de un jugador del mismo tramo) |
|---|---|---|---|---|---|
| **Diminuta** | Mosquitos, ratas, murciélagos | Van en **enjambre**: el enjambre ocupa un hueco | No | No | ×0,1 cada uno; enjambre de 6 a 10 |
| **Pequeña** | Zorro, kóbold, limo | 1 hueco | No | No | ×0,3 |
| **Mediana** | Lobo, necrófago, bandido | 1 hueco | Solo élites | Las humanoides: cabeza, brazos, piernas | ×0,6 a ×1 |
| **Grande** | Oso, gólem, wyrm joven | 2 huecos | Sí | 1 o 2 especiales | ×2 a ×3 |
| **Enorme** | Gigante, forjado, tortuga volcán | Toda su fila | Sí, alta | 2 a 4 | ×5 a ×8 |
| **Colosal** | Solo jefes (ver [Jefes](jefes.md)) | Las dos filas | Muy alta | Muchas | 5 o 6 dígitos |

**Ejemplo de números.** En el tramo V un jugador tiene unos 900 de vida. Un lobo tiene unos 600; un gigante, unos 6.000. Ningún monstruo común pasa de 4 dígitos, tampoco con modificadores (§7).

### 1.3 Repertorio y avisos

- Un monstruo común tiene de **2 a 4 movimientos**. Un élite, uno más. Un único con nombre, de 5 a 7.
- **Llevan aviso** (ver [Avisos y tácticas](../04-combate/avisos-y-tacticas.md)) todos los golpes que:
  - **contagian** una enfermedad (el aviso lleva 🦠);
  - derriban, inmovilizan o hieren grave;
  - pegan en área o a una fila;
  - canalizan, invocan o explotan.
- Los golpes normales a un objetivo no llevan aviso. Así el mensaje no se llena de texto y los avisos importan.
- Los monstruos comunes **no mienten** en sus avisos. Los retrasos y las fintas son de élites, únicos y aberraciones del Abismo.

### 1.4 Mente: terror y fobias

- **Terror (0 a 3):** cuánto estrés sube al verlo y al recibir uno de sus críticos (ver [Mente](../05-salud/mente.md)). Una bestia es ○ o ●; un espectro o una aberración, ●●●.
- **Presencia:** algunas criaturas del Vacío y del Abismo suben el estrés o bajan la **cordura** en cada ronda, mientras sigan vivas.
- **Fobias:** una herida **grave** de una familia puede dejar su fobia (ver [Rasgos adquiridos](../05-salud/rasgos-adquiridos.md)): estrés extra contra esa familia. Se quita venciendo a 10 de ellos sin huir, o en el templo.
- **El lado bueno:** vencer a 500 de una misma familia da el rasgo *Azote de [familia]*: +1 nivel de conocimiento con toda la familia y un 10 % más de materiales al despiezarla. Es premio de oficio, no de combate.

### 1.5 Conocimiento del bestiario

Saber de un monstruo es progresión (ver [Progresión](../03-personaje/progresion.md)). Cada especie tiene su propio nivel de conocimiento.

| Nivel | Cómo se sube | Qué revela |
|---|---|---|
| ☆ **Desconocido** | — | Solo el texto: "*una criatura que no conoces*" |
| ★ **Visto** | Verlo una vez | Nombre, familia, talla y hábitat |
| ★★ **Vencido** | Vencer a 1 | Debilidades, resistencias y partes rompibles |
| ★★★ **Estudiado** | Vencer a 10, o leer su ficha | Qué contagia y cómo. Los avisos traen la pista: "*(lo conoces: esquivar la mordida evita el contagio)*" |
| ★★★★ **Experto** | Vencer a 50, o despiezar 3 piezas de tres estrellas | Qué deja cada parte. Ves cuándo va a huir. Puedes sacarle **materiales raros** que otros no ven, como los ingredientes de *The Witcher* |
| ★★★★★ **Maestro** | Vencer a 200 y una investigación (ver [Investigaciones](investigaciones.md)) | Sus modificadores posibles, su población en cada piso y sus migraciones |

- El conocimiento es de la cuenta, como el Bestiario de [Descubrimiento y colecciones](../03-personaje/descubrimiento-y-colecciones.md).
- Las **fichas** se escriben con Inscripción y las vende el **Informante** (ver [Profesiones](../07-economia/profesiones.md)). Leer una ficha sube a ★★★, nunca más arriba: lo demás hay que vivirlo.

## 2. Arquetipos de comportamiento por turnos

Cada monstruo tiene un arquetipo. El arquetipo decide qué hace en la ronda y cómo se le gana.

| Arquetipo | Qué hace en la ronda | Aviso típico | Cómo se le gana | Ejemplos |
|---|---|---|---|---|
| **Manada que rodea** | Desde la ronda 2, si son más que el grupo, uno salta a la retaguardia aunque haya vanguardia. Más daño contra quien está solo en su fila | "*los lobos se abren en abanico…*" | Formación Agrupado, un tanque que provoque a todos, y **matar al alfa**: sin él, la manada huye | Lobo Gris, Sabueso Infernal, Perro de Ceniza |
| **Emboscador** | Ataca primero: el grupo no actúa en la ronda 0, solo puede reaccionar | Una pista en el texto de exploración: "*la hierba se mueve sin viento*" | Avanzar **con cuidado** (más lento, anula la emboscada), farol, perro, el olfato del Licántropo, la *Visión Espectral* del Cazador de Demonios | Tigre de Duna, Víbora de Hierba, Caimán de Lodo |
| **Huidizo** | Huye en la ronda 2 o 3, o al primer golpe fuerte. Se lleva su botín | "*mira hacia la salida*" | Apuntar a las **piernas** (no puede huir), *Flecha Clavadora*, trampas, iniciativa alta | Limo Metálico, Zorro Espumoso, Lagartija de Cuarzo |
| **Carroñero** | Va a por los **derribados** con un golpe de remate. Come cadáveres para curarse | Siempre: "*se agazapa junto a X, que está en el suelo*" | Levantar al derribado esa misma ronda, arrastrarse a la retaguardia, que el tanque lo cubra. Despiezar o quemar los cuerpos | Necrófago, Buitre de Hueso, Cuervo de Carroña |
| **Territorial** | No pelea si no entras en su nodo. Te da una ronda de gruñido para irte. En su nido es más fuerte | En exploración: "*marcas de garras en los árboles*" | Retirarse a tiempo, o **atraerlo con cebo** fuera del nido, donde pierde Postura | Jabalí Colmillo de Hierro, Grifo, Ogro del Puente |
| **Invocador** | Desde la retaguardia, canaliza y trae aliados | "*empieza a cantar sobre los cuerpos*" | **Interrumpir**, o matarlo primero (lanzas, distancia, hechizos) | Araña Nodriza, Tejedor de Carne, Diablillo |
| **Sanador de su grupo** | Cura al más herido de su bando; una vez por pelea, levanta a un caído | "*alza las manos sobre el herido*" | Interrumpir, silenciar, marcarlo y matarlo primero | Cultista de la Podredumbre, Jardinero Mecánico, Dríade Marchita |
| **Kamikaze** | Se infla una ronda y estalla en su fila | "*se hincha y empieza a brillar*" | Matarlo **antes** del aviso, o dispersarse. Congelarlo lo apaga | Hongo Esporón, Escarabajo Bombardero, Fanático del Vacío |
| **Parásito** | Se pega a un jugador. Cada ronda le chupa vida o le llena una barra | "*algo trepa por la pierna de X*" | Arrancarlo (§2.1) | Sanguijuela Gigante, Larva del Vacío, Gusano Susurrante |
| **Mimético** | Se disfraza de cofre, de PNJ, de planta o de pasadizo | Siempre deja **una pista** en el texto (§2.2) | Examinar antes de tocar | Mímico, Peregrino Falso, Boca del Fondo |
| **Ladrón** | Roba un objeto de la mochila y huye en 2 rondas | "*sus ojos se clavan en tu bolsa*" | Matarlo o cortarle la huida; si escapa, seguir su rastro (§2.3) | Kóbold Minero, Harpía de Ruinas, Diablillo |
| **Corruptor del terreno** | Deja una zona dañina en una fila (lava, moho, raíces, hielo) | "*el suelo bajo la retaguardia se cubre de moho*" | **Cambiar de fila** antes del final de la ronda. Fuera de combate, matarlo limpia el nodo | Micelio Andante, Elemental de Magma, Señor de la Fosa |
| **Acechador** | Te sigue de nodo en nodo y ataca cuando estás herido o solo | "*sientes que algo te sigue*" | No separarse, descansar en un nodo seguro, ponerle una trampa en el camino | Buitre de Hueso, Sabueso Infernal (en Pesadilla) |
| **Enjambre** | Muchos diminutos. Los golpes a un objetivo fallan la mitad | "*el zumbido sube*" | Daño en área, humo, fuego | Mosquitos de Ciénaga, Pez Colmillo, Murciélago Vampiro |

**Moral.** Las bestias, los insectos y los humanoides **huyen** si cae su alfa o si les queda menos del 25 % de vida. Los no-muertos, los constructos y las aberraciones nunca huyen. Un monstruo que huye se lleva su botín, pero deja rastro (ver [Cacerías](cacerias.md)).

### 2.1 Parásitos: cómo se arrancan

- Un parásito pegado **cuenta como enemigo** y como carga del jugador al que se pegó.
- Pegarle sin apuntar le hace la mitad del daño **también al portador**. Con *Apuntar* (acción rápida) no hay daño al portador.
- El portador puede **arrancárselo** con su acción entera. Un aliado puede hacerlo con su acción.
- **Sal gruesa** o una **antorcha** lo hacen soltarse con una acción rápida.
- Un parásito cuenta para la **Firmeza**: nadie queda controlado por uno más de dos veces seguidas.

### 2.2 Miméticos: siempre hay una pista

El mímico no es una trampa de azar. Todo mimético deja **una pista en el texto**, y hay cuatro formas de verla:
- **Leer:** "*la cerradura está húmeda*", "*el viajero no deja huellas*".
- **Examinar:** una acción fuera de combate que revela al mimético si tu conocimiento de la especie es ★★ o más.
- **Golpear primero:** abre el combate sin sorpresa, pero un cofre de verdad pierde parte de su contenido.
- **Linajes:** el Goblin ve el precio de los objetos, y un mímico **no tiene precio**. El Licántropo lo huele.

```
🧰 Sala del fondo · Ruinas del piso 63
Un cofre de roble con remaches de bronce.
La cerradura está cubierta de algo húmedo.

[🔓 Abrir]          [🔍 Examinar]
[🗡 Golpearlo antes] [🚶 Dejarlo]
```

El mímico guarda lo que se tragó: si lo vences, deja un botín de verdad.

### 2.3 Ladrones: qué roban y cómo se recupera

- Solo roban **de la mochila**: consumibles o materiales. **Nunca** lo que llevas puesto ni objetos ligados.
- **No roban a novatos** (hasta el nivel 10), como en [Crimen y justicia](crimen-y-justicia.md).
- Si escapa, deja rastro durante **una hora de juego**. Seguirlo lleva a su madriguera, donde está lo tuyo y lo que robó a otros.
- Una **bolsa con cierre** (Peletería) protege un objeto elegido.

## 3. Tipos de daño: debilidades, resistencias y remedios de caza

Como la tabla de tipos de *Pokémon*, cada familia es débil o resistente a ciertos tipos de daño (ver [Daño y estados](../04-combate/dano-y-estados.md)). La tabla se aprende con el conocimiento (★★).

**Reglas fijas:**
- **Débil:** +30 % de daño. **Resiste:** −30 %. Nunca más.
- **Ningún monstruo común es inmune a un tipo de daño.**
- **Inmunidad a un estado** (un gólem no sangra, un no-muerto no se envenena): la acumulación que no puede entrar se convierte en **daño directo** (el 70 %), o en daño a la **Postura** si la tiene. Así el Pícaro de Asesinato no queda inútil contra un gólem.

### Remedios de caza

Como los aceites de *The Witcher 3*, cada familia tiene su remedio. Son **consumibles**: los usa cualquier spec, y los fabrica un oficio.

| Remedio | Contra | Efecto | Quién lo fabrica |
|---|---|---|---|
| **Aceite de bestias** | Bestias, gigantes | +15 % de daño durante un combate | Alquimia |
| **Aceite de insectos** | Insectos y arácnidos, limos | +15 % | Alquimia |
| **Aceite de necrófagos** | No-muertos, mutantes | +15 % | Alquimia (con uñas de necrófago) |
| **Aceite de espectros** | Espectros, aberraciones | +15 %, y los golpes físicos no pierden daño por incorporeidad | Alquimia y Encantamiento |
| **Baño de plata** | Espectros, licántropos, vampiros | Cuentan como débiles (+30 %). Dura 5 combates | Joyería y Herrería |
| **Baño de hierro frío** | Feéricos corruptos | Cuentan como débiles (+30 %). Dura 5 combates | Herrería |
| **Agua bendita** | No-muertos, demonios | Frasco arrojadizo: daño sagrado a una fila | Templo |
| **Frasco de agua helada** | Bestias volcánicas | Las "templa": el siguiente golpe contundente les rompe la piel | Alquimia |
| **Sal gruesa** | Limos, parásitos | Arranca un parásito como acción rápida; un limo no se divide esa ronda | Recolección en costa y desierto |
| **Bengala** | Aberraciones, sombras | Luz: revela lo invisible y baja la ganancia de estrés 3 rondas | Ingeniería |
| **Tapones de cera** | Mandrágora, sirenas, plañideras | Inmune a gritos y cantos. **Costo:** no oyes las pistas de voz de los avisos | Cera de abeja del bosque |

- **Un aceite por arma.** Cambiarlo es una acción rápida.
- Los aceites no suman Toxicidad: van en el arma, no en el cuerpo.

## 4. Las 19 familias

| # | Familia | Dónde abunda | Débil a | Resiste | Terror | Fobia que puede dejar |
|---|---|---|---|---|---|---|
| 1 | **Bestias** | Tramos I a VI · bosque, llanura, cueva, desierto, tundra | Perforación, fuego | — | ● | *Miedo a las bestias* |
| 2 | **Insectos y arácnidos** | I a V · bosque, llanura, cueva, pantano, desierto | Fuego, contundente | Naturaleza | ● | *Aracnofobia* |
| 3 | **Reptiles y dracónidos** | I a VI · bosque, llanura, pantano, desierto, montaña | Escarcha | Fuego, corte | ●● | *Miedo a los reptiles* |
| 4 | **No-muertos** | II a VII · llanura, pantano, desierto, ruinas | Sagrado, fuego, contundente | Naturaleza, sombra; no sangran | ●● | *Miedo a los muertos* |
| 5 | **Espectros** | I a IX · bosque, pantano, tundra, ruinas, abismo | Sagrado, arcano | Física, salvo al condensarse | ●●● | *Miedo a los fantasmas* |
| 6 | **Plantas y hongos** | I a X · bosque, pantano, cueva, tierras flotantes | Fuego, corte | Naturaleza, contundente | ● | *Miedo a las esporas* |
| 7 | **Limos y parásitos** | I a VIII · bosque, pantano, cueva, volcánico | Fuego, escarcha | Corte, perforación | ● | *Asco a lo viscoso* |
| 8 | **Elementales** | II a X · según el clima | El elemento contrario | Su propio elemento | ○ | — |
| 9 | **Gólems y constructos** | II a X · llanura, pantano, ruinas, ciudadela, tierras flotantes | Rayo, contundente | Corte, naturaleza; no sangran, no duermen, no enloquecen | ○ | — |
| 10 | **Humanoides salvajes** | I a IX · todos | Según su armadura | Según su armadura | ● (cultistas ●●) | — |
| 11 | **Gigantes** | II a X · llanura, montaña, pantano, tundra, volcánico, tierras flotantes | Perforación; las piernas | Contundente | ● | *Miedo a los gigantes* |
| 12 | **Criaturas acuáticas** | I a X · costa, lagos, pantano | Rayo | Fuego, escarcha | ● | *Miedo al agua profunda* |
| 13 | **Aves y criaturas del aire** | I a X · bosque, cueva, desierto, montaña, ruinas, tierras flotantes | Perforación, rayo | Contundente (en vuelo no lo alcanzan) | ○ | — |
| 14 | **Demonios y criaturas del Vacío** | VIII y IX · ciudadela, volcánico, abismo | Sagrado | Sombra, Vacío; los demonios, fuego | ●●● | *Miedo a los demonios* |
| 15 | **Feéricos corruptos** | I-II, VII, X · bosque, ruinas, tierras flotantes | Hierro frío, fuego | Arcano, naturaleza | ● | — |
| 16 | **Mutantes de la contaminación** | II a VIII · nodos contaminados | Fuego, sagrado | Naturaleza, podredumbre | ●● | *Miedo a lo deforme* |
| 17 | **Aberraciones del Abismo** | IX y Pesadillas · abismo, cueva | Sagrado, luz | Sombra, Vacío, locura | ●●● | *Miedo a la oscuridad* |
| 18 | **Criaturas de cristal** | III y V · cueva, montaña, desierto | Contundente | Corte, perforación | ○ | — |
| 19 | **Bestias volcánicas** | VIII · volcánico, ciudadela | Escarcha, agua | Fuego; no se queman | ● | *Miedo al fuego* |

**Cómo leer las tablas que siguen:** tramo en números romanos (ver [Torre y pisos](../02-mundo/torre-y-pisos.md)) y terreno con su icono (ver [Geografía y recursos](../02-mundo/geografia-y-recursos.md)). Los estados por acumulación van con su icono; las enfermedades, con 🦠.

### 4.1 Bestias

Las más comunes. Enseñan las reglas básicas: manada, huida y partes. Su carne se cocina y su piel es la base de la Peletería.

| Monstruo | Tramo / terreno | Rasgo principal | Contagia o aplica | Parte rompible → lo que deja |
|---|---|---|---|---|
| **Lobo Gris** | I-II · 🌲 Bosque, 🌾 Llanura | **Manada** de 3 a 6. Rodea al que queda solo. Si cae el alfa, huyen | 🩸 Sangrado. En manadas enfermas, 🦠 **Mal de Espuma** (desde el tramo II) | Colmillos → colmillos (flechas, collares) · piel de lobo |
| **Jabalí Colmillo de Hierro** | II · 🌾 Llanura | **Territorial**. Carga en línea recta contra la vanguardia: "*escarba la tierra*" | Derribo, contusión | Colmillos (pierde *Carga*) → marfil (mangos, Carpintería) · carne · cuero |
| **Zorro Espumoso** | II · 🌲 Bosque | **Huidizo**. Muerde a la retaguardia y escapa | 🦠 **Mal de Espuma** por mordida | Cola → cola de zorro (cebo, cosmético). Su carne no se come |
| **Oso Cavernario** | III · 🕳️ Cueva, ⛰️ Montaña | Grande, con Postura. *Abrazo*: inmoviliza a uno 2 rondas | Fractura, contusión | Garras (pierde *Zarpazo doble*) → garras · grasa (velas, Cocina) · piel gruesa |
| **Tigre de Duna** | V · 🏜️ Desierto · noche | **Emboscador** bajo la arena | 🩸 Sangrado fuerte | Colmillos de sable → dagas · piel rayada (tres estrellas solo con golpe limpio a la cabeza) |
| **Licántropo Salvaje** | VI · ❄️ Tundra, 🌲 Bosque · luna llena | Veloz. Se regenera, salvo con plata o fuego | 🦠 **Mordida del Lobo Lunar** → licantropía | Garras → garra de licántropo (ritual de cura) · piel maldita |

### 4.2 Insectos y arácnidos

Poca vida y mucha cantidad. Castigan a quien no tiene daño en área.

| Monstruo | Tramo / terreno | Rasgo principal | Contagia o aplica | Parte rompible → lo que deja |
|---|---|---|---|---|
| **Araña Tejedora** | I · 🌲 Bosque | **Emboscadora**. Telaraña: el objetivo pierde su acción rápida 2 rondas | 🟢 Veneno leve | Glándula → seda cruda (Tejeduría) · glándula de veneno |
| **Mantis Segadora** | II · 🌾 Llanura | Combo de dos golpes; el segundo llega retrasado | 🩸 Sangrado | Brazos-guadaña (pierde el combo) → hojas curvas (dagas) |
| **Langosta de Plaga** | II · 🌾 Llanura · verano | **Enjambre** que **devora cultivos**: si nadie lo frena, arrasa los campos del piso (ver [Animales y cultivos](../05-salud/animales-y-cultivos.md)) | Se come la comida de la mochila | Sin partes → quitina (abono) · cebo para peces |
| **Araña Nodriza** | III · 🕳️ Cueva | **Invocadora**: pone huevos que se abren en 2 rondas | 🦠 **Puesta de Araña** en heridas abiertas · 🟢 Veneno | Abdomen (romperlo cancela la puesta) → saco de huevos (Alquimia) · seda fina |
| **Mosquitos de Ciénaga** | IV · 🐸 Pantano · lluvia | **Enjambre** diminuto. El humo y el área lo deshacen | 🦠 **Fiebre del Pantano** por picadura | Sin partes → alas de mosquito (reactivo menor) |
| **Escorpión de Vidrio** | V · 🏜️ Desierto | Blindado. El aguijón llena el veneno rápido | 🟢 Veneno fuerte | Aguijón (pierde *Picadura*) → aguijón · caparazón (placas ligeras) |

### 4.3 Reptiles y dracónidos

Escamas que frenan el corte. Con frío se vuelven lentos. Los dracónidos son la caza mayor clásica.

| Monstruo | Tramo / terreno | Rasgo principal | Contagia o aplica | Parte rompible → lo que deja |
|---|---|---|---|---|
| **Tortuga Musgosa** | I · 🌲 Bosque, 🌊 lagos | Blindada: resiste todo menos el contundente. Apuntar a las piernas la da vuelta y queda expuesta | — | Caparazón → escudo ligero (Carpintería) · musgo (Herboristería) |
| **Víbora de Hierba** | II · 🌾 Llanura | **Emboscadora**. Muerde a quien recolecta en la hierba alta | 🟢 Veneno (se llena rápido) | Colmillos → veneno de víbora (antídotos) · piel |
| **Caimán de Lodo** | IV · 🐸 Pantano, 🌊 ríos | **Emboscador** del agua. *Arrastre*: lleva a uno al agua 2 rondas | Herida profunda; mordida sucia que sube el riesgo de 🦠 **Gangrena** | Cola (pierde *Coletazo*) → cuero de caimán (cuero pesado) |
| **Basilisco de Pantano** | IV · 🐸 Pantano | *Mirada pétrea*. Se evita con *Apartar la vista* (acción rápida, −25 % de precisión) | ☠️ Maldición de piedra: pierde 2 turnos y recibe más contundente | Ojos → ojo de basilisco (tónico contra la piedra) |
| **Wyrm Joven de las Dunas** | V · 🏜️ Desierto | Grande. Se hunde en la arena y sale por la retaguardia | 🔥 Quemadura (aliento de vidrio) | Alas, cola → escamas de wyrm · glándula de arena. Presa de [Cacerías](cacerias.md) |
| **Draco de Escarcha** | VI · ⛰️ Montaña | Grande y volador. Aliento canalizado: hay que **interrumpir** | ❄️ Congelación · herida de congelación | Alas (lo bajan a tierra) → membrana de ala · escama helada |

### 4.4 No-muertos

No sangran, no se envenenan y no tienen miedo. Suben el estrés. Son los grandes portadores de podredumbre.

| Monstruo | Tramo / terreno | Rasgo principal | Contagia o aplica | Parte rompible → lo que deja |
|---|---|---|---|---|
| **Esqueleto Soldado** | II · 🌾 viejos campos de batalla | Se vuelve a armar una vez si no se le rompe el cráneo con contundente | 🦠 **Tétanos de Óxido** (armas oxidadas) | Cráneo → polvo de hueso (abono, Alquimia) · chatarra (Fundición) |
| **Necrófago** | IV · 🐸 Pantano · noche | **Carroñero**: remata derribados y come cadáveres para curarse | 🟤 Podredumbre · 🦠 **Podredumbre Gris** por zarpa | Garras, mandíbula → uñas de necrófago (aceite de necrófagos) · bilis negra |
| **Portador de la Plaga** | Cualquier tramo y terreno, solo en una epidemia | **Kamikaze**: al morir revienta en una nube que llena el Contagio de toda su fila | 🦠 **Plaga Pálida** (en el evento) | Vientre → bilis de plaga (muestras para la cura; ver [Eventos](eventos.md)) |
| **Momia de Arena** | V · 🏜️ Desierto · tumbas | Las vendas arden: el fuego la daña de más | ☠️ *Polvo de tumba*: no recibe curación 2 rondas | Vendas → lino antiguo (Arqueología) · amuleto funerario |
| **Caballero Hueco** | VII · 🏛️ Ruinas | Mediano con Postura. Bloquea, contraataca y usa golpes retrasados | Fractura, laceración | Yelmo → acero antiguo (variante de Fundición) · a veces un plano antiguo |
| **Engendro Vampírico** | VII · 🏛️ Ruinas · noche | Roba vida. Al 30 % se vuelve niebla y huye | 🦠 **Fiebre de Sangre** → vampirismo | Colmillos → colmillo de vampiro · ceniza de vampiro (reactivo de templo) |

### 4.5 Espectros

Incorpóreos: resisten la física, salvo en la ronda en que **se condensan** para atacar. Esa ronda el aviso lo dice y la física les pega como si fueran débiles. Con plata o aceite de espectros, siempre.

| Monstruo | Tramo / terreno | Rasgo principal | Contagia o aplica | Parte rompible → lo que deja |
|---|---|---|---|---|
| **Fuego Fatuo** | I · 🌲 Bosque · noche | **Huidizo**. En exploración, aleja al grupo del camino hacia un nodo peligroso | — (engaña) | Sin partes → luz fatua (faroles, Encantamiento) |
| **Poltergeist** | II · 🌾 granjas abandonadas | **Ladrón**: arranca un consumible de la mochila y lo lanza contra el grupo | Contusión | Sin partes → polvo de éter (Encantamiento) |
| **Plañidera** | IV · 🐸 Pantano, VII · 🏛️ Ruinas | Lamento canalizado que sube el estrés de todos. Hay que **interrumpir** | 🌀 Locura · estrés | Velo → ectoplasma (tinta de Inscripción) |
| **Novia de Escarcha** | VI · ❄️ Tundra, ⛰️ pasos · ventisca | Canto que adormece | 💤 Sueño · ❄️ Congelación; fuera de combate, más riesgo de 🦠 **Gripe de Escarcha** | Velo helado → lágrima helada (Joyería) |
| **Soldado Fantasma** | VII · 🏛️ Ruinas | Repite la batalla en que murió: su repertorio va **siempre en el mismo orden** | ❄️ Congelación | Sin partes → fragmento de memoria (pistas de lore, [Investigaciones](investigaciones.md)) |
| **Sombra Hambrienta** | IX · 🌑 Abismo | Invisible sin luz. Apaga faroles y antorchas. Es lo que muerde en la oscuridad total (ver [Peligros del entorno](../05-salud/peligros-del-entorno.md)) | 🌀 Locura · baja la cordura | Sin partes → esencia de sombra (Encantamiento) |

### 4.6 Plantas y hongos

Se mueven poco: el peligro es quedarse en su fila. Muchas se esconden entre las plantas que busca un herborista.

| Monstruo | Tramo / terreno | Rasgo principal | Contagia o aplica | Parte rompible → lo que deja |
|---|---|---|---|---|
| **Hongo Esporón** | I · 🌲 Bosque | **Kamikaze** menor: revienta en esporas | Tos 2 rondas (Aguante −1). En el tramo I, nada más | Sombrero → setas (Cocina, Alquimia) |
| **Enredadera Estranguladora** | II · 🌲 Bosque, IV · 🐸 | **Parásito**: agarra una pierna y aprieta cada ronda | Inmoviliza · contusión | Raíz → fibra (cuerda, Tejeduría) · savia |
| **Micelio Andante** | III · 🕳️ Cueva | **Corrompe el terreno**: cubre de moho una fila | 🦠 **Pulmón de Moho** por esporas | Núcleo → hongos luminosos · corazón de micelio (cultivar hongos, Agricultura) |
| **Mandrágora** | IV · 🐸 Pantano | Parece una hierba. Arrancada sin tapones, grita | 💤 Sueño a todo el grupo | Raíz → raíz de mandrágora (sedantes de caza, Alquimia) |
| **Árbol Hueco** | VII · 🌲 Bosque, 🏛️ Ruinas | Enorme, con Postura. Al romperle el tronco sale un enjambre | Contusión · derribo | Tronco → madera de corazón (variante de Carpintería) · miel negra |
| **Rosal Sangriento** | X · 🌸 Tierras flotantes | Su perfume atrae: el marcado camina a la vanguardia. Espinas | 🩸 Sangrado · 🌀 Locura leve | Flor → pétalos (perfumes, Encantamiento) |

### 4.7 Limos y parásitos

El corte y la perforación los dividen. El fuego y la escarcha los rompen. Los parásitos se pegan y hay que arrancarlos (§2.1).

| Monstruo | Tramo / terreno | Rasgo principal | Contagia o aplica | Parte rompible → lo que deja |
|---|---|---|---|---|
| **Limo Verde** | I · 🌲 Bosque, 🐸 | Se divide en dos al recibir corte. Gasta la durabilidad del arma | 🟢 Veneno leve | Núcleo → gelatina (cola de Carpintería) |
| **Limo Metálico** | II-III · 🕳️ Cueva | **Huidizo**: durísimo, escapa en 3 rondas. Da mucha Esencia | — | Núcleo → gota de mercurio (Encantamiento) |
| **Mímico** | Todos los tramos · mazmorras, ruinas | **Mimético**: parece un cofre (§2.2) | Herida profunda · 🟢 Veneno (saliva) | Lengua → pegamento de mímico (Ingeniería) · el botín que se tragó |
| **Sanguijuela Gigante** | IV · 🐸 Pantano | **Parásito**: chupa vida cada ronda y se cura con ella | 🩸 Sangrado · anemia (vida máxima −5 % una hora) | Boca → saliva anticoagulante (ungüento para contusiones, Medicina) |
| **Cieno Ácido** | VIII · 🌋 Volcánico | Cada golpe baja la durabilidad y la defensa de la zona que toca | 🔥 Quemadura (ácido) | Núcleo → ácido fuerte (grabado de Joyería) |

### 4.8 Elementales

Débiles al elemento contrario y resistentes al propio. Llegan con el clima (ver [Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md)).

| Monstruo | Tramo / terreno | Rasgo principal | Contagia o aplica | Parte rompible → lo que deja |
|---|---|---|---|---|
| **Chispa Errante** | II · 🌾 Llanura · tormenta | Salta en cadena entre los **agrupados** | 🔥 Quemadura (rayo) · llena la Firmeza | Sin partes → chispa embotellada (Ingeniería) |
| **Elemental de Piedra** | III · ⛰️ Montaña, 🕳️ | Blindado y lento | Fractura | Núcleo → gema en bruto · piedra rúnica |
| **Remolino de Arena** | V · 🏜️ Desierto · tormenta de arena | Veloz. Con tormenta se divide en dos | Ceguera (precisión −50 %) | Sin partes → arena de vidrio fino (Joyería) |
| **Ventisquero** | VI · ❄️ Tundra · ventisca | **Explosivo al morir**: nova de hielo | ❄️ Congelación · herida de congelación | Núcleo → hielo eterno (conservar comida) |
| **Elemental de Magma** | VIII · 🌋 Volcánico | **Corrompe el terreno**: lava en una fila | 🔥 Quemadura | Núcleo → obsidiana ígnea (Herrería T8) |
| **Céfiro** | X · 🌸 Tierras flotantes | *Ráfaga*: cambia de fila a dos jugadores y les deshace la formación | Llena la Firmeza | Sin partes → esencia de viento (varitas) |

### 4.9 Gólems y constructos

No sienten dolor ni miedo. Casi todos tienen un núcleo o una runa que, rota, los apaga.

| Monstruo | Tramo / terreno | Rasgo principal | Contagia o aplica | Parte rompible → lo que deja |
|---|---|---|---|---|
| **Espantapájaros Animado** | II · 🌾 Llanura · noche | Solo se anima de noche en los campos. Muy débil al fuego | Estrés | Sin partes → semillas encantadas (variedades raras, Agricultura) |
| **Gólem de Barro** | IV · 🐸 Pantano | Se cura cada ronda mientras pise lodo. La escarcha lo seca | Contusión | Núcleo → arcilla fina (ladrillo de calidad, Construcción) |
| **Autómata de Ruinas** | VII · 🏛️ Ruinas | Patrulla fija. Si ve al grupo, da la **alarma**: llega otro en 2 rondas | Contusión | Núcleo → engranajes · núcleo de autómata (**prótesis**, Ingeniería) |
| **Centinela Rúnico** | VII · 🏛️ Ruinas | No se mueve. Canaliza un rayo: interrumpir o romper su runa | 🔥 Quemadura (rayo) | Runa → runa antigua (Encantamiento) |
| **Forjado de Obsidiana** | VIII · 🔥 Ciudadela | Enorme. Se recalienta cada 3 rondas y abre una ventana de daño | 🔥 Quemadura · fractura | Placas → placas de obsidiana (Herrería) · a veces el artefacto *Corazón de la Forja* |
| **Jardinero Mecánico** | X · 🌸 Tierras flotantes | **Sanador de su grupo**: repara a otros constructos | 🩸 Sangrado (tijeras) | Tijeras → acero fino · aceite de engranaje (Ingeniería) |

### 4.10 Humanoides salvajes

Piensan: beben pociones, huyen para avisar, ponen trampas y se rinden. Sueltan equipo del Mercado Negro, oro y papeles. Conectan con [Crimen y justicia](crimen-y-justicia.md).

| Monstruo | Tramo / terreno | Rasgo principal | Contagia o aplica | Parte rompible → lo que deja |
|---|---|---|---|---|
| **Kóbold Minero** | I · 🕳️ Cueva, ⛰️ | **Ladrón**: roba de la mochila y huye por un túnel | — | Sin partes → lo robado · velas · pico viejo |
| **Bandido de Camino** | II · 🌾 rutas de caravana | Embosca caravanas. Si pierde la mitad del grupo, **se rinde** | 🩸 Sangrado | Equipo del Mercado Negro · oro · cartel de recompensa (se cobra en la guardia) |
| **Cultista de la Podredumbre** | IV · 🐸 Pantano | **Sanador de su grupo**. Sacrifica a un aliado para curar a todos | 🟤 Podredumbre · 🦠 **Podredumbre Gris** | Túnica · tomo prohibido ([Investigaciones](investigaciones.md)) |
| **Corsario de Costa** | V · 🌊 Costa | Red desde la retaguardia (inmoviliza) y arpón. Roba y huye en barca | Herida profunda | Ron · perlas · mapa del tesoro |
| **Saqueador de Tumbas** | VII · 🏛️ Ruinas | Pone **trampas** antes del combate y lanza bombas | 🔥 Quemadura · 🦠 **Tétanos de Óxido** | Herramientas de arqueología · mapas de ruinas |
| **Fanático del Vacío** | IX · 🌑 Abismo | **Kamikaze**: se inmola en la ronda 3, "*empieza a brillar por dentro*" | Estrés · 🦠 **Fiebre del Vacío** | Fragmento del Vacío (reactivo de Corrupción) |

### 4.11 Gigantes

Enormes, con Postura. Romperles las piernas los tira al suelo. Algunos negocian.

| Monstruo | Tramo / terreno | Rasgo principal | Contagia o aplica | Parte rompible → lo que deja |
|---|---|---|---|---|
| **Ogro del Puente** | II · 🌾 Llanura, ríos | **Territorial**. Cobra peaje: si pagas, no hay pelea | Fractura · derribo | Cinturón → cuero de ogro · el oro de los peajes |
| **Cíclope de Cantera** | III · ⛰️ Montaña | Lanza rocas a la retaguardia. Con el ojo roto, pega al azar | Fractura · conmoción | Ojo → lente de cíclope (catalejos, Ingeniería) |
| **Gigante del Fango** | IV · 🐸 Pantano | Se regenera, salvo la ronda en que recibe fuego o ácido | Mordida sucia: riesgo de 🦠 **Gangrena** | Hígado → sangre regenerativa (pociones, Alquimia) |
| **Gigante de Escarcha** | VI · ⛰️ Montaña, ❄️ | *Meteoro de hielo*: hay que agruparse para repartirlo | ❄️ Congelación | Barba helada → hielo eterno · piel de mamut que viste |
| **Titán de Ceniza** | VIII · 🌋 Volcánico | Cada paso deja fuego en una fila. La escarcha lo apaga una ronda | 🔥 Quemadura · 🦠 **Fiebre de Ceniza** | Corazón → brasa eterna (Herrería); en élites, artefacto menor |
| **Gigante de las Nubes** | X · 🌸 Tierras flotantes | *Soplido*: saca a un jugador del combate 2 rondas | Llena la Firmeza | Manto → algodón de nube (tela livianísima, Sastrería) |

### 4.12 Criaturas acuáticas

Esperan en vados, costas y pantanos. Muchas arrastran al agua (ver agua profunda en [Peligros del entorno](../05-salud/peligros-del-entorno.md)). Su carne cruda enferma.

| Monstruo | Tramo / terreno | Rasgo principal | Contagia o aplica | Parte rompible → lo que deja |
|---|---|---|---|---|
| **Pez Colmillo** | I · 🌊 lagos y vados | **Enjambre** en los vados: muerde a quien cruza | 🩸 Sangrado. Comido crudo, 🦠 **Parásito de Río** (desde el nivel 11) | Sin partes → pescado (Cocina) |
| **Cangrejo Acorazado** | II · 🌊 Costa | Blindado. *Tenaza*: desarma 1 ronda | Contusión · desarme | Pinzas (pierde *Tenaza*) → carne de cangrejo · caparazón |
| **Anguila de Tormenta** | IV · 🐸 Pantano, 🌊 | Descarga en cadena si el grupo pelea en un nodo con agua | 🔥 Quemadura (rayo) · aturde | Órgano eléctrico → batería orgánica (**desfibriladores**, Ingeniería) |
| **Sirena de Arrecife** | V · 🌊 Costa | Canto canalizado: arrastra a uno hacia el agua | 💤 Sueño · 🌀 Locura | Escamas iridiscentes (Joyería) · cuerdas vocales (instrumentos) |
| **Pulpo de las Ruinas Hundidas** | VII · 🌊 ruinas sumergidas | Grande: cada tentáculo es un ataque. Tinta que ciega | Ceguera | Tentáculos → tinta de pulpo (la mejor tinta de Inscripción) |
| **Medusa Flotante** | X · 🌸 lagos del cielo | Deriva sobre el grupo y toca a quien esté **disperso** | 🟢 Veneno paralizante · llena la Firmeza | Campana → gel anestésico (**cirugía**, Medicina) |

### 4.13 Aves y criaturas del aire

En vuelo solo las alcanzan armas a distancia, lanzas y hechizos. La ronda en que bajan a atacar, todos. Romperles las alas o la *Flecha Clavadora* las dejan en tierra.

| Monstruo | Tramo / terreno | Rasgo principal | Contagia o aplica | Parte rompible → lo que deja |
|---|---|---|---|---|
| **Cuervo de Carroña** | I · 🌲 Bosque | **Carroñero y ladrón**: se lleva objetos brillantes del botín antes de que lo recojas | Arañazo | Plumas negras (plumas de escribir, flechas) |
| **Murciélago Vampiro** | III · 🕳️ Cueva · noche | **Enjambre**. Muerde y se va | 🩸 Sangrado · 🦠 **Mal de Espuma** | Alas (reactivo) · guano (abono, Agricultura) |
| **Buitre de Hueso** | V · 🏜️ Desierto | **Carroñero y acechador**: sigue al grupo por el mapa y baja cuando alguien cae | 🩸 Sangrado · remate | Pico · plumas |
| **Grifo de Montaña** | VI · ⛰️ Montaña | **Territorial** con nido. *Picado*: levanta y suelta a uno | Esguince · fractura leve | Plumas de grifo (flechas finas) · huevo (cría de monturas, Ganadería) |
| **Harpía de Ruinas** | VII · 🏛️ Ruinas | **Ladrona**: roba a la retaguardia y huye volando | Arañazo · esguince | Garras · plumas |
| **Mantarraya del Cielo** | X · 🌸 Tierras flotantes | Planea sobre una fila y descarga | 🔥 Quemadura (rayo) · aturde | Piel de raya (capas contra el viento, Sastrería) |

### 4.14 Demonios y criaturas del Vacío

Suben el estrés y pueden dejar Corrupción (ver [Mente](../05-salud/mente.md)). Los demonios arden; las criaturas del Vacío apagan la luz.

| Monstruo | Tramo / terreno | Rasgo principal | Contagia o aplica | Parte rompible → lo que deja |
|---|---|---|---|---|
| **Diablillo** | VIII · 🔥 Ciudadela | **Ladrón e invocador**: roba una poción y se la bebe; si no muere en 3 rondas, llama a otro | 🔥 Quemadura | Cuerno → cuerno de diablillo (Alquimia) |
| **Sabueso Infernal** | VIII · 🌋, 🔥 | **Manada** de 3. En dificultad Pesadilla, **te caza** por el mapa | 🔥 Quemadura · **Frenesí** (§6.3) | Colmillos ígneos · glándula de azufre |
| **Señor de la Fosa** | VIII · 🔥 Ciudadela | Enorme. Abre grietas que **corrompen el terreno** e invoca diablillos | 🔥 Quemadura · Corrupción leve | Cuernos → sangre de demonio (Encantamiento); artefacto menor |
| **Peregrino Falso** | IX · 🌑 Abismo y caminos de pisos altos | **Mimético**: parece un PNJ perdido que pide ayuda | 🌀 Locura · estrés | Máscara → polvo de ecos · la carta que llevaba (pista de un caso) |
| **Tragaluz** | IX · 🌑 Abismo | *Presencia*: cada ronda baja la cordura del grupo | 🦠 **Fiebre del Vacío** · 🌀 Locura | Ojo negro (Encantamiento de sombra) |
| **Larva del Vacío** | IX · 🌑 Abismo | **Parásito**: se pega a la espalda y susurra | 🦠 **Fiebre del Vacío** | Larva seca (reactivo, Alquimia) |

### 4.15 Feéricos corruptos

Engañan más de lo que pegan. Viven en el Bosque Susurrante y en los Jardines Flotantes.

| Monstruo | Tramo / terreno | Rasgo principal | Contagia o aplica | Parte rompible → lo que deja |
|---|---|---|---|---|
| **Duendecillo Burlón** | I · 🌲 Bosque | **Ladrón** travieso: roba un objeto y lo **esconde** en otro nodo del piso | — | Polvo de hada (Encantamiento) |
| **Hada de Espinas** | I-II · 🌲 Bosque | **Emboscadora** en círculos de hongos: quien entra, se duerme | 💤 Sueño | Alas → ala de hada (cosméticos) |
| **Niño Cambiado** | VII · 🏛️, 🌲 | **Mimético**: parece un niño perdido. Si lo llevas al asentamiento, roba y escapa | 🦠 **Sopor Feérico** | Hilo de plata (Sastrería) |
| **Dríade Marchita** | VII · 🌲 Bosque | **Sanadora de su grupo** y **corruptora**: sus raíces atrapan una fila | 💤 Sueño · 🦠 **Sopor Feérico** por polen | Corazón → semilla de dríade (variedad mágica, Agricultura) |
| **Caballero de la Corte Marchita** | X · 🌸 Tierras flotantes | Élite. *Duelo*: desafía a uno; los demás que lo atacan reciben una espina | 🩸 Sangrado · 💤 Sueño | Espada → acero feérico, que no se oxida (Herrería) |
| **Polilla Lunar** | X · 🌸 · noche | Polvo de alas que duerme a una fila | 💤 Sueño · 🦠 **Sopor Feérico** | Alas → polvo lunar (tinta luminosa, Inscripción) |

### 4.16 Mutantes de la contaminación

Nacen en los nodos con ☣️ Contaminación (ver [Peligros del entorno](../05-salud/peligros-del-entorno.md)) y donde la actividad de los jugadores ensucia el piso (§10.6).

| Monstruo | Tramo / terreno | Rasgo principal | Contagia o aplica | Parte rompible → lo que deja |
|---|---|---|---|---|
| **Rata de Escoria** | II-III · ⛰️ minas y fundiciones | **Enjambre** que roe la mochila y se come la comida | 🦠 **Mal de Escoria** · 🦠 **Disentería** | Cola → cebo · grasa rancia (jabón) |
| **Lobo Bicéfalo** | III · ⛰️ Montaña | Dos mordidas por ronda. Romper una cabeza le quita un ataque | 🩸 Sangrado | Cabeza → trofeo · piel manchada |
| **Sapo Bilioso** | IV · 🐸 Pantano | Escupe bilis a la retaguardia. **Explota al morir** | 🟢 Veneno · 🦠 **Mal de Escoria** | Glándula → bilis (venenos de caza) |
| **Carpa de Tres Ojos** | IV · 🌊 ríos contaminados | Se pesca, no se pelea. Comerla enferma | 🦠 **Mal de Escoria** (al comerla) | Ojo extra (Alquimia) |
| **Abominación de Vertedero** | VII · pisos con contaminación alta | Élite. Come cadáveres de monstruos y crece una talla | 🟤 Podredumbre · 🦠 **Mal de Escoria** | Glándula mutágena (transmutación, Alquimia) |
| **Masa de Escoria** | VIII · 🌋, junto a forjas | **Se come las armas** que quedan en el suelo y se vuelve más dura | 🦠 **Tétanos de Óxido** | Núcleo → chatarra fundida (metal de calidad al azar, Fundición) |

### 4.17 Aberraciones del Abismo

Solo en el tramo IX y en las Pesadillas (ver [Misiones y exploración](misiones-y-exploracion.md)). Terror máximo, bajan la cordura y **sí mienten** en sus avisos.

| Monstruo | Tramo / terreno | Rasgo principal | Contagia o aplica | Parte rompible → lo que deja |
|---|---|---|---|---|
| **Ojo Flotante** | IX · 🌑 | Retaguardia. Revela al grupo (anula el sigilo) y llama a otros | 🌀 Locura | Cristalino → lente del abismo (Joyería) |
| **Tejedor de Carne** | IX · 🌑 | **Invocador**: cose cadáveres de monstruos en engendros | 🟤 Podredumbre · 🦠 **Podredumbre Gris** | Hilo de tendón (las mejores suturas, Medicina) |
| **Boca del Fondo** | IX · 🕳️ | **Mimético del terreno**: parece un pasadizo. Traga a uno 2 rondas | Herida profunda · estrés | Diente del abismo (Joyería) |
| **Gusano Susurrante** | IX · 🌑 | **Parásito** del oído: si no se arranca en 3 rondas, **decide la acción** de su portador una ronda | 🌀 Locura · 🦠 **Ojo del Abismo** | Larva → aceite de larva (Alquimia) |
| **Horror Sin Rostro** | IX · 🌑 | **Emboscador**: mete en el registro de combate una línea falsa con la voz de un aliado. La línea falsa nunca lleva el icono de clase | 🌀 Locura · estrés | Polvo de ecos (Inscripción) |
| **Engendro del Umbral** | IX · 🌑 | Élite enorme. **Cambia de debilidades** en cada fase; el Bestiario las revela | Estrés · 🦠 **Fiebre del Vacío** | Fragmento del Umbral (artefacto menor) |

### 4.18 Criaturas de cristal

Frágiles al contundente. Sus esquirlas se clavan y cristalizan la piel. Son la mejor fuente de **Resonancia**, el atributo de material de varitas e instrumentos (ver [Fabricación](../07-economia/fabricacion.md)).

| Monstruo | Tramo / terreno | Rasgo principal | Contagia o aplica | Parte rompible → lo que deja |
|---|---|---|---|---|
| **Lagartija de Cuarzo** | III · 🕳️ Cueva | **Huidiza**. Muerta de un golpe contundente, deja la gema entera | — | Gema en bruto (Joyería) |
| **Eriza de Cuarzo** | III · 🕳️ | Púas: quien la golpea cuerpo a cuerpo recibe un corte | 🩸 Sangrado | Púas de cuarzo (puntas de flecha) |
| **Polilla Prisma** | III · 🕳️ | Refleja la luz: ciega y desvía un hechizo por ronda | Ceguera | Polvo prismático (tinta) |
| **Gusano de Vetas** | III · ⛰️, 🕳️ | Se come las vetas: si nadie lo caza, **agota las vetas del piso** | 🦠 **Cristalosis** | Buche → las gemas que se comió |
| **Gólem de Cristal** | III · 🕳️ | Grande. Resuena: el contundente le baja más Postura | 🦠 **Cristalosis** por esquirlas · laceración | Núcleo resonante (Resonancia alta) |
| **Centinela de Vidrio** | V · 🏜️ Desierto · tras tormentas | Nace donde cae un rayo en la arena. Descarga en cadena | 🔥 Quemadura (rayo) · 🦠 **Cristalosis** | Vidrio de rayo (Joyería) |

### 4.19 Bestias volcánicas

Resisten el fuego y no se queman. Un frasco de agua helada o un golpe de escarcha las "templa", y el siguiente golpe contundente les rompe la piel. Es una combinación entre dos jugadores.

| Monstruo | Tramo / terreno | Rasgo principal | Contagia o aplica | Parte rompible → lo que deja |
|---|---|---|---|---|
| **Salamandra de Lava** | VIII · 🌋 | Nada en la lava. **Corrompe el terreno**: brasas en una fila | 🔥 Quemadura | Piel ignífuga (capas contra el calor) |
| **Perro de Ceniza** | VIII · 🌋 | **Manada**. Jadea ceniza | 🔥 Quemadura · 🦠 **Fiebre de Ceniza** | Pelaje de ceniza (Curtiduría) |
| **Escarabajo Bombardero** | VIII · 🌋, 🔥 | **Kamikaze**: estalla al morir o en la ronda 3 | 🔥 Quemadura en su fila | Caparazón de brasa (pólvora, Ingeniería) |
| **Lagarto de Obsidiana** | VIII · 🌋 | Blindado. El fuego lo endurece más | 🔥 Quemadura · fractura | Escama de obsidiana (Herrería T8) |
| **Tortuga Volcán** | VIII · 🌋 | Enorme y lenta. Erupción avisada cada 3 rondas | 🔥 Quemadura · 🦠 **Fiebre de Ceniza** | Caparazón → azufre · teja ígnea (Construcción) |
| **Fénix de Ceniza** | VIII · 🔥 Ciudadela | **Renace** una vez de sus cenizas si no se apagan (agua o escarcha) en la ronda siguiente | 🔥 Quemadura | Pluma de fénix (Sales de Reanimación de calidad, Medicina) |

**Total: 113 monstruos en 19 familias**, con todos los tramos y todos los terrenos cubiertos. A esto se suman los modificadores (§7) y los únicos con nombre (§8).

## 5. El contagio

### 5.1 La barra 🦠 Contagio

El contagio funciona como los estados por acumulación (ver [Daño y estados](../04-combate/dano-y-estados.md)): **no hay azar ciego**.

- Cada golpe que contagia **suma** a una barra 🦠 de esa enfermedad. Su aviso siempre lleva 🦠.
- Al llenarse, **contraes la enfermedad**: entra en incubación (ver [Enfermedades](../05-salud/enfermedades.md)).
- **La llenan más despacio:**
  - la armadura de la zona golpeada (como cualquier acumulación);
  - una **máscara** con filtro, contra esporas y nubes;
  - una **vacuna**, si los médicos ya investigaron la cura (la barra no sube);
  - haberte curado de esa enfermedad hace poco (inmunidad);
  - el linaje: el **Renacido** no enferma de males naturales; el **Enano** resiste los de mina y frío; el **Goblin**, los venenos (ver [Creación de personaje](../03-personaje/creacion-de-personaje.md)).
- **Al terminar el combate**, lo que quedó en la barra pasa a la herida como **herida sucia** durante una hora de juego:
  - **limpiarla** (venda limpia, Primeros Auxilios, un médico) la vacía;
  - si en esa hora te llega otra fuente de la misma enfermedad, se suma;
  - si pasa la hora sin llenarse, se vacía sola.

### 5.2 Vías de contagio

| Vía | Ejemplo | Cómo se evita |
|---|---|---|
| **Mordida o garra** | Zorro Espumoso, Necrófago | Esquivar el golpe avisado, armadura de la zona, limpiar la herida |
| **Picadura** | Mosquitos de Ciénaga | Humo, repelente (Alquimia), ropa cerrada (Sastrería) |
| **Esporas y nubes** | Micelio Andante, Portador de la Plaga | Máscara, formación Disperso, no quedarse en la fila |
| **Esquirlas** | Gólem de Cristal | Armadura de la zona, esquivar |
| **Parásito** | Gusano Susurrante, Larva del Vacío | Arrancarlo antes de que llene la barra |
| **Despiece** | Desollar un monstruo **Enfermo** sin guantes | Guantes de desuello (ver [Profesiones](../07-economia/profesiones.md)) |
| **Comer** | Carne cruda, pescado crudo, carne de un monstruo Enfermo | Cocinar. El Licántropo huele la carne mala |
| **Beber** | El río donde vive un Sapo Bilioso | Hervir, pastillas, filtro (ver [Peligros del entorno](../05-salud/peligros-del-entorno.md)) |
| **Otros jugadores** | El Pulmón de Moho se pega con la tos al grupo **agrupado** | Máscara, cuarentena |
| **Ganado** | Una bestia enferma muerde a tu montura o a tu rebaño | Cercos, veterinario (ver [Animales y cultivos](../05-salud/animales-y-cultivos.md)) |

## 6. Vectores de enfermedad

### 6.1 El catálogo actual: quién contagia qué

| Enfermedad (ver [Enfermedades](../05-salud/enfermedades.md)) | Monstruos que la contagian | Vía | Cómo se previene | Cómo se trata |
|---|---|---|---|---|
| **Fiebre del Pantano** | Mosquitos de Ciénaga | Picadura | Repelente, ropa cerrada, humo, máscara contra la miasma | Corteza amarga (Alquimia) |
| **Gripe de Escarcha** | Novia de Escarcha, Ventisquero, y el frío del tramo VI | Aliento helado y frío | Capa de piel (Peletería), fogata | Reposo caliente, caldo (Cocina) |
| **Disentería** | Rata de Escoria; agua donde vive un Sapo Bilioso; carne cruda de cualquier bestia | Comer, beber | Cocinar, hervir el agua, filtro | Carbón, agua hervida |
| **Gangrena** | Caimán de Lodo, Gigante del Fango; cualquier mordida sin limpiar | Herida sucia | Limpiar en la primera hora; vendas de lino limpio (Sastrería) | Limpiar, cirugía (Medicina) |
| **Tétanos de Óxido** | Esqueleto Soldado, Saqueador de Tumbas, Masa de Escoria | Armas oxidadas | Armadura de la zona; antitoxina preventiva | Antitoxina (Alquimia) |
| **Podredumbre Gris** | Necrófago, Cultista de la Podredumbre, Tejedor de Carne | Zarpa, magia | Aceite de necrófagos (matarlos rápido), esquivar la zarpa | Ungüento de plata (Alquimia y Joyería) |
| **Fiebre del Vacío** | Tragaluz, Larva del Vacío, Fanático del Vacío, Engendro del Umbral | Presencia, parásito, explosión | Luz, filtro bendito, salir de su alcance | Templo, bardo |
| **Plaga Pálida** | Portador de la Plaga (solo en el evento) | Nube al morir, y después los jugadores | Cazar a los portadores ([Cacerías](cacerias.md)), cuarentena | La cura que se investiga entre todos |
| **Parásito de Río** | Pez Colmillo, Carpa de Tres Ojos | Comer crudo | Cocinar el pescado | Purga (Alquimia) |
| **Fiebre de Sangre** | Engendro Vampírico | Mordida | Protección de cuello, no quedar derribado cerca de él | Ritual antes de 3 días (templo) |
| **Mordida del Lobo Lunar** | Licántropo Salvaje | Mordida en luna llena | Baño de plata para matarlo rápido; no cazar solo en luna llena | Ritual antes de la luna llena |
| **Tos del Minero, Temblor Arcano, Mal del Piso** | Ningún monstruo: son de oficio, de clase o de clima | — | — | Ver [Enfermedades](../05-salud/enfermedades.md) |

### 6.2 Enfermedades nuevas, propias de monstruos

Siguen el modelo de siempre: **carrera entre gravedad e inmunidad**, incubación que ya contagia, y un desenlace que **nunca mata** fuera del Juramento de Hierro.

**Velocidad de la carrera:** *lenta* (se gana sola con reposo), *media* (hace falta un remedio) o *rápida* (hace falta un médico).

| Enfermedad | Vector | Incubación y carrera | Síntomas | Prevención | Tratamiento | Si se pierde la carrera |
|---|---|---|---|---|---|---|
| **Mal de Espuma** | Zorro Espumoso, Murciélago Vampiro, lobos enfermos | 3 h · rápida | Irritable: a veces actúa solo, como *Temerario*. Tragar cuesta: beber pociones gasta la acción entera | Esquivar la mordida avisada; **suero de espuma** antes de los síntomas (Alquimia y Medicina) | Suero y sedantes (Médico) | Rasgo *Irascible* una semana: el estrés sube más al recibir críticos |
| **Pulmón de Moho** | Micelio Andante, Hongo Esporón (desde el tramo III) | 1 h · lenta · **se contagia al grupo agrupado** | Tos: Aguante máximo −1. Al toser delatas al grupo (sin sigilo) | Máscara de lino fino (Sastrería), formación Disperso | Vapor de hierbas (Herboristería y Alquimia), reposo | *Pulmón manchado*, crónico leve, como la Tos del Minero |
| **Puesta de Araña** | Araña Nodriza, la Reina Araña | 12 h · media | Picor; el Sustento baja más rápido. En el pico, **eclosión**: en tu próximo combate aparecen 2 crías del lado enemigo | Romper el abdomen de la Nodriza antes de la puesta; limpiar la herida | **Cirugía menor** (extraer parásitos) o purga fuerte (Alquimia) | Cicatrices. Si eclosiona dos veces, *Aracnofobia* |
| **Cristalosis** | Gólem de Cristal, Gusano de Vetas, Centinela de Vidrio | 6 h · lenta | La piel de la zona herida se vuelve cristal: resiste mejor el corte, pero se fractura más fácil. Iniciativa −1 | Armadura de la zona; esquivar las esquirlas | Baños de sal de roca y disolvente (Alquimia) | *Vetas de cristal*: marcas que brillan de noche, sin efecto |
| **Fiebre de Ceniza** | Perro de Ceniza, Titán de Ceniza, Tortuga Volcán | 2 h · media | Calor por dentro: la Hidratación baja el doble y, en zonas calientes, Aguante máximo −1 | Máscara húmeda, agua de sobra | Tónico refrescante (Alquimia), reposo en un lugar fresco | *Voz de ceniza* (cosmético) y una semana con menos tolerancia al calor |
| **Sopor Feérico** | Polilla Lunar, Dríade Marchita, Niño Cambiado | 4 h · lenta | La barra de 💤 Sueño se llena el doble. A veces un aviso llega con el texto confuso | Amuleto de hierro frío (Joyería), tapones de cera | Infusión despertadora (Cocina), campana del templo | *Tocado por las hadas*: un sueño con un rumor por semana (cosmético) y unos días de *Insomne* |
| **Mal de Escoria** | Rata de Escoria, Sapo Bilioso, Carpa de Tres Ojos, Abominación de Vertedero | 6 h · media | Manchas en la piel. La **Toxicidad máxima baja**: aguantas menos pociones (ver [Condiciones](../05-salud/condiciones.md)) | Máscara y guantes; no comer lo que vive en aguas sucias; bajar la contaminación del piso | Quelante (Alquimia) y depuración (Médico) | *Mutación menor* temporal: una marca, algo de resistencia al veneno y el Sustento baja más rápido. Se va con tratamiento |
| **Ojo del Abismo** | Gusano Susurrante, El Que Imita | 1 día · lenta | **Con ventaja:** ves lo invisible y las fintas de los avisos se marcan. **Con costo:** el estrés sube un 50 % más | Arrancar al gusano antes de 3 rondas; luz | Templo o bardo. **Se puede conservar** a propósito | *Visionario*: pesadillas y estrés en la oscuridad; se quita en el templo |

- **Ojo del Abismo** imita el Frenesí de *Monster Hunter* y la licantropía de *Skyrim*: una enfermedad que algunos quieren tener. Sus ventajas **no cuentan** en contenido clasificado (Mítica+, arena); el costo sí.
- Todas entran en la **investigación de curas y vacunas** (ver [Investigaciones](investigaciones.md)) y en el oficio de médico (ver [Curación](../05-salud/curacion-y-tratamientos.md)).

### 6.3 Contagios de combate

Duran un solo combate. No son enfermedades: no cuentan para el tope.

| Contagio | Quién lo pega | Qué pasa | Cómo se supera |
|---|---|---|---|
| **Frenesí** | Sabueso Infernal; monstruos con el modificador Corrupto | Barra de 3 rondas. Mientras dura, recibes −20 % de curación | Si en esas 3 rondas logras un crítico o rompes una parte, **lo superas**: +5 % de crítico el resto del combate. Si no, −20 % de curación 3 rondas más |
| **Tos de esporas** | Hongo Esporón, Micelio Andante | Aguante −1 mientras dure | Salir de la fila con esporas; máscara |
| **Marca de sangre** | Engendro Vampírico; modificador Vampírico | Todos los vampíricos van a por el marcado, y su vida los cura | Disipar magia, o matar al que marcó |
| **Huevos en la herida** | Araña Nodriza | Si la barra de Puesta pasa del 50 %, en 3 rondas sale una cría | Romper el abdomen de la Nodriza, sal gruesa |

## 7. Modificadores: la variedad que se multiplica

**De dónde sale.** Los campeones y únicos de *Diablo II*, los monstruos raros de *Path of Exile* y los templados de *Monster Hunter: World*. Un mismo lobo con distintos modificadores es otro problema.

| Modificador | Cómo se ve | Qué cambia en combate | Qué cambia en el botín |
|---|---|---|---|
| **Élite** | ⭐ | Vida ×2 y un movimiento más de su familia | +1 nivel de rareza posible; materiales ×2 |
| **Campeón** | 🔷 grupo de 3 a 5 | Todos comparten un modificador extra | Botín por cabeza y una bolsa de grupo |
| **Alfa de manada** | 👑 | La manada gana iniciativa y no huye mientras viva. Si cae, huyen | Trofeo de alfa (tres estrellas si se rompe limpio) |
| **Enfermo** | 🤢 | Sus golpes llenan el Contagio **el doble**. Tiene −20 % de vida y contagia a su propio grupo | **Muestra** de la enfermedad (la piden los médicos para investigar); su piel y su carne salen peor |
| **Corrupto** | 🟣 | Daño de Vacío añadido, sube el estrés, aplica Frenesí | Fragmentos del Vacío (Encantamiento) |
| **Blindado** | 🛡 | Armadura alta. El contundente y los golpes a las partes se la rompen | Más escamas o chatarra; las partes rotas dan más |
| **Veloz** | 💨 | Actúa primero y huye con facilidad | +Esencia |
| **Vampírico** | 🩸 | Roba vida y aplica Marca de sangre | Esencia vital (Alquimia) |
| **Explosivo al morir** | 💥 fuego, escarcha, veneno o esporas | Al morir estalla en su fila **la ronda siguiente**, con aviso. Congelarlo lo apaga | Glándula de su elemento |
| **Templado** | 🗡 | Vida ×1,5, golpes retrasados en su repertorio. Ya venció a otros jugadores (§10.4) | Una pieza de tres estrellas garantizada si se rompe una parte |
| **Invocador** | 🌀 | Llega con escolta y la repone cada 3 rondas | La escolta suelta lo suyo |
| **Legendario con nombre** | 🏷 | Ver §8 | Trofeo único, artefacto posible, título |

**Cuántos modificadores tiene un monstruo:**

| Lugar | Modificadores | Notas |
|---|---|---|
| 🟡 Zona amarilla | 0 o 1 | Solo Élite, Veloz o Alfa |
| 🔴 Zona roja | 1 o 2 | Cualquiera menos Legendario |
| ⚫ Zona negra | 2 o 3 | Aquí nacen los Templados |
| Mazmorra Normal · Profundidades · Corrompido · Abismal · Pesadilla | 0 · 1 · 1-2 · 2 · 3 | En Corrompido, uno es siempre Corrupto (ver [Mazmorras y bandas](mazmorras-y-bandas.md)) |

**Límites:**
- Un modificador nunca sube la vida de un monstruo común por encima de 4 dígitos.
- **Enfermo nunca se combina con Explosivo**, salvo durante una epidemia: evita nubes de contagio que nadie puede esquivar.
- El equipo que sueltan sale del **Mercado Negro**: lo fabricó un jugador (ver [Economía](../07-economia/economia.md)). El modificador decide qué tan buena es la pieza que sale de esa reserva (rareza y afijos), no crea objetos de la nada.

## 8. Monstruos únicos con nombre

**De dónde sale.** Los monstruos únicos con nombre de *Diablo*, los élites raros de *World of Warcraft* y el jefe errante de *Darkest Dungeon*.

**Reglas:**
- **No son Guardianes:** no dan Sello ni Recuerdo (ver [Jefes](jefes.md)).
- **Aparecen poco:** una ventana de 1 a 3 horas cada varios días, en un grupo de nodos. Antes hay una señal: un rumor en la taberna, huellas enormes, ganado muerto.
- **Dos tipos:** el **raro errante**, que vuelve a aparecer (cada personaje cobra su botín una vez por semana), y la **bestia legendaria de temporada**, una por tramo y temporada (ver [Cacerías](cacerias.md)).
- **Vida de 5 dígitos como mucho:** entre un monstruo común y un jefe de campo.
- **Primera muerte del servidor:** el nombre del grupo va al Registro de descubridores y a la Gaceta.
- **Botín:** trofeo único, material exclusivo, probabilidad de **artefacto menor** con protección contra mala racha, y una casilla en el **Tesoro Semanal** (ver [Equipamiento](../03-personaje/equipamiento.md)).

| Nombre | Tramo y lugar | Qué es | Cuándo aparece | Qué lo hace especial | Qué deja |
|---|---|---|---|---|---|
| **Colmillo Viejo** | I · piso 4 · 🌲 | Lobo Gris alfa que sobrevivió a muchos cazadores | Noches con muchos lobos en el piso | Rodea desde la primera ronda y llama a la manada cada 3 rondas | Piel de Colmillo Viejo (capa cosmética) · colmillo de alfa (arcos) |
| **La Madre de las Setas** | I · piso 7 · 🌲 | Hongo gigante | Tras dos días de lluvia | Esporas que duermen; en el tramo I, sin enfermedad | Micelio madre (cultivar setas raras, Agricultura) |
| **Rompecercas** | II · piso 13 · 🌾 | Jabalí enorme | Otoño, con cosechas en pie | Si nadie lo caza, arrasa los campos de los jugadores del piso | Colmillo de Rompecercas (maza única) · título *Salvador de la cosecha* |
| **El Espantajo de los Siete Campos** | II · piso 18 · 🌾 | Espantapájaros único | Luna nueva | Se esconde entre espantapájaros normales: hay que encontrar al verdadero | Semillas del Espantajo (variedad de cultivo única) |
| **El Cantor de Cuarzo** | III · piso 22 · 🕳️ | Gólem de cristal que canta | Si nadie mina en su galería durante 3 días | Su canto rompe gemas de la mochila si no lo interrumpes | Núcleo cantor (la mayor Resonancia: laúdes y varitas) |
| **La Reina Araña** | III · piso 27 · 🕳️ | Araña Nodriza gigantesca | Con mucha población de arañas | Puesta de Araña en área. Si vive, sus crías invaden los nodos vecinos | Seda real (Sastrería). Puede dejar *Aracnofobia* (ver [Rasgos adquiridos](../05-salud/rasgos-adquiridos.md)) |
| **Vieja Bilis** | IV · piso 34 · 🐸 | Sapo mutante enorme | Cuando sube la contaminación del piso | Si vive, ensucia el agua: sube la Disentería en el asentamiento | Bilis madre (Alquimia). Matarla baja la contaminación del piso |
| **El Barquero Ahogado** | IV · piso 38 · 🐸 🌊 | Espectro en una barca | Niebla | Cobra un objeto por cruzar. Si no pagas, pelea; si pagas, a veces devuelve algo mejor | Remo del barquero (bastón único) · moneda del barquero |
| **El Sediento** | V · piso 46 · 🏜️ | Momia errante | Ola de calor | Roba el agua de las mochilas: la Hidratación del grupo baja cada ronda | Vendas del Sediento (cosmético) · amuleto de la tumba |
| **Espejismo** | V · piso 49 · 🏜️ | Sirena del desierto | Mediodía | Aparece en el mapa como un oasis | Escama del Espejismo (Joyería) |
| **La Novia del Paso** | VI · piso 53 · ⛰️ | Novia de Escarcha única | Ventisca | Duerme a las caravanas que cruzan el paso | Velo de la Novia (capa de frío única) |
| **El Ciervo de Ceniza** | VI · piso 57 · ⛰️ | Bestia legendaria de temporada (ver [Cacerías](cacerias.md)) | Toda la temporada, moviéndose por el piso | Huye de nodo en nodo y deja rastros; no pelea hasta que lo acorralan | Asta de ceniza (trofeo único del servidor) · título |
| **El Anticuario** | VII · piso 64 · 🏛️ | Autómata que colecciona | Cuando alguien excava (Arqueología) | Roba piezas de arqueología y las guarda en su cámara | Lo robado · llave de su cámara (tesoro) |
| **El Rey sin Corona** | VII · piso 68 · 🏛️ | Caballero Hueco único | Eclipse | Duelo de honor: si lo atacan varios a la vez, llama a su guardia | Corona rota (Arqueología) · acero antiguo puro |
| **Brasaviva** | VIII · piso 73 · 🔥 | Fénix de Ceniza | Tras una erupción | Renace tres veces: cada vez hay que apagar sus cenizas | Pluma de Brasaviva (ingrediente de artefacto) |
| **Mandíbula de Forja** | VIII · piso 78 · 🌋 | Masa de Escoria gigante | Si las forjas del piso ensuciaron mucho en la semana | Se come las armas de los caídos | Corazón de escoria (metal de calidad excepcional al azar) |
| **El Que Imita** | IX · piso 84 · 🌑 | Horror Sin Rostro único | Solo ante grupos | Imita el registro de combate y la voz de los aliados | 🦠 *Ojo del Abismo* · máscara de ecos (cosmético) |
| **El Ojo del Pozo** | IX · piso 89 · 🕳️ | Ojo Flotante colosal | Cuando la cordura del piso está baja (evento) | Mira a una fila por ronda: Locura acumulada | Cristalino del Pozo (lente mayor, Joyería) |
| **El Jardinero Primero** | X · piso 93 · 🌸 | Autómata antiguo | Primavera | Repara a todos los constructos del piso mientras viva | Tijeras del Primero (apariencia de herramienta) · aceite antiguo |
| **La Polilla de la Última Luna** | X · piso 98 · 🌸 | Polilla Lunar gigante | La última noche de cada estación | Sopor Feérico en área | Polvo de la Última Luna (tinta que revela textos ocultos, [Investigaciones](investigaciones.md)) |

## 9. Qué deja un monstruo

**Nada sale de la nada** (ver [Red de sistemas](../00-vision/red-de-sistemas.md)). El botín de un monstruo tiene capas, y cada capa alimenta a un oficio.

| Capa | Qué es | De qué depende | Quién lo usa |
|---|---|---|---|
| **Esencia** | La moneda de progreso | Nivel y modificadores | Todos: mejoras y maestrías (ver [Economía](../07-economia/economia.md)) |
| **Despiece** | Piel, carne, huesos, glándulas | Tu Desuello, cómo lo mataste (calidad de una a tres estrellas) y tu conocimiento (★★★★ abre materiales raros) | Curtiduría, Cocina, Alquimia |
| **Partes rotas** | Material exclusivo de cada parte | Romperla en combate (ver [Daño y estados](../04-combate/dano-y-estados.md)) | Recetas temáticas ([Fabricación](../07-economia/fabricacion.md)) |
| **Equipo** | Piezas fabricadas por jugadores que compró el Mercado Negro | Zona y modificadores: Rareza (Común a Reliquia) y Afijos | Todos |
| **Oro y papeles** | Monedas, carteles, mapas, tomos, contratos | Solo humanoides | Investigaciones, Crimen, Cartografía |
| **Muestras** | Sangre o tejido de un monstruo Enfermo | El modificador Enfermo | Medicina: investigar curas y vacunas |
| **Crías y huevos** | Animales vivos | Captura viva o saquear un nido | Ganadería, doma, el Foso ([Peleas clandestinas](peleas-clandestinas.md)) |
| **Artefactos menores** | Ingredientes únicos para armas y armaduras con técnica propia | Élites, Templados y únicos con nombre, con protección contra mala racha. Los artefactos mayores son solo de jefes | Herrería, Peletería, Joyería |
| **Curiosidades** | Carta del **Mazo de Bestias**, trofeos, piezas de arqueología | Azar pequeño y conocimiento | Colecciones, sala de trofeos, museo ([Minijuegos](../08-social/minijuegos-y-formatos-telegram.md)) |

- **Si nadie del grupo sabe Desuello**, solo se sacan "restos": poco y de una estrella. Llevar un desollador al grupo vale la pena.
- **Las partes rotas mandan:** romper la cola da el material de la cola, pero la piel sale peor (ver [Cacerías](cacerias.md)).
- **El equipo de botín es un extra, nunca la fuente principal:** lo mejor lo fabrican los artesanos con lo que tú despiezas.

## 10. Ecología

### 10.1 Poblaciones

Cada especie tiene una **población por piso** (ver [Mundo vivo](../02-mundo/mundo-vivo-y-viaje.md)).

| Población | Qué pasa | Precio de sus materiales | Tablón |
|---|---|---|---|
| **Escasa** | Casi no aparece. Si se sigue cazando, desaparece del piso hasta la próxima estación | Sube | No paga. El Ecologista puede poner veda (ver [Fundación y cisma](../02-mundo/fundacion-y-cisma.md)) |
| **Normal** | — | Normal | Normal |
| **Abundante** | Aparecen alfas y élites | Baja | Paga más |
| **Plaga** | Invade zonas azules y amarillas: invasión o ataque a casas (ver [Defensa](../09-construccion/defensa-y-protecciones.md)) | Muy bajo | Paga el doble |

### 10.2 Depredadores y presas

| Depredador | Presa | Si se caza mucho la presa | Si se caza mucho al depredador |
|---|---|---|---|
| Lobo Gris | Ciervos, jabalíes | Los lobos bajan a las granjas y atacan el ganado | Los jabalíes se vuelven plaga y arrasan cosechas |
| Sapo Bilioso | Mosquitos de Ciénaga | — | Más mosquitos: sube la Fiebre del Pantano |
| Araña Nodriza | Murciélagos, lagartijas de cuarzo | Las arañas salen de la cueva a los caminos | Plaga de murciélagos: más Mal de Espuma |
| Grifo de Montaña | Cabras de montaña | Ataca caravanas y monturas | Las cabras pelan los pastos |
| Necrófago | **Cadáveres que dejan los jugadores** | Si se despieza o se quema todo, el necrófago escasea | Si nadie despieza, crecen y sube la Podredumbre Gris |
| Buitre de Hueso | Restos de combate | Menos combates, menos buitres | Más carroña sin limpiar, más necrófagos |
| Gusano de Vetas | Vetas de mineral | — | Si nadie lo caza, agota las vetas del piso |

### 10.3 Migraciones

- En **primavera** vuelven las migraciones, y el evento *Migración* lleva una especie por varios pisos (ver [Eventos](eventos.md)).
- Ejemplos: los grifos bajan del tramo VI al V en invierno; la langosta sube en verano por la Pradera Dorada; los murciélagos salen de las cuevas en otoño.
- **Siguen a los jugadores:** los carroñeros van detrás de las batallas, los mutantes detrás de la contaminación y las criaturas del Vacío detrás de la corrupción.

### 10.4 Monstruos que crecen si nadie los caza

**De dónde sale.** El sistema Némesis de *Shadow of Mordor* y los templados de *Monster Hunter: World*.

| Etapa | Cómo llega | Qué gana |
|---|---|---|
| **Joven** | Nace | Su repertorio básico |
| **Adulto** | Sobrevive un día de juego | Lo normal |
| **Veterano** | Derriba a un jugador y huye, o sobrevive 3 días | El modificador **Templado**. Recuerda: resiste el tipo de daño que más recibió (siempre dentro del −30 %) |
| **Alfa** | Veterano en una población Abundante | Lidera una manada (**Alfa de manada**) |
| **Con nombre** | Alfa que sobrevive una semana o que derribó a 5 jugadores | Se vuelve **único temporal**: el servidor le pone nombre ("el Tuerto del Piso 16") y sale en la Gaceta |

- **"Te recuerda".** Si un monstruo te derribó, su ficha lo dice. Cazarlo da *Venganza*: un trofeo y Esencia extra.
- **Límites:** un monstruo con nombre temporal por piso a la vez. Solo en zonas amarilla, roja y negra. Nunca pasa los números de su tramo.

### 10.5 Peleas de territorio

**De dónde sale.** *Monster Hunter: World*.

- Si dos monstruos **territoriales** coinciden en un nodo, pelean entre ellos una ronda. Los dos pierden vida y Postura, y el perdedor huye.
- Se puede provocar: llevar a uno con cebo al territorio del otro.
- Es una táctica de cazador: llegar a la pelea grande con el monstruo ya golpeado.

### 10.6 Contaminación y corrupción que se extienden

**De dónde sale.** La Corrupción de *Terraria*.

- **Contaminación.** Además de las fuentes naturales (ver [Peligros del entorno](../05-salud/peligros-del-entorno.md)), se propone que la actividad intensa de los jugadores suba el rigor ☣️ de un nodo: fundiciones y destilerías grandes, vertidos de alquimia, vetas sobreexplotadas.
  - Con ☣️1 aparecen ratas y sapos; con ☣️2, lobos bicéfalos; con ☣️3, Abominaciones de Vertedero, y a veces un único como Vieja Bilis o Mandíbula de Forja.
  - Se baja con cuotas del Ecologista, estaciones de filtrado (Construcción, Ingeniería y Alquimia) y cazando a los mutantes.
- **Corrupción del Vacío.** Desde las grietas del tramo IX se extiende a los nodos vecinos si nadie mata a los monstruos que la abren (Señor de la Fosa, Engendro del Umbral). Los monstruos de un nodo corrupto ganan el modificador **Corrupto**.
- **Terreno corrupto** fuera de combate: las hierbas se marchitan y las vetas rinden menos. Los herboristas y mineros pagan para que alguien lo limpie.

### 10.7 Brotes en la fauna

- Una especie puede **enfermar**: una parte de su población gana el modificador **Enfermo**.
- El brote pasa a los jugadores, a sus monturas y a su ganado (ver [Animales y cultivos](../05-salud/animales-y-cultivos.md)).
- Si nadie lo frena, puede ser la semilla de una **epidemia** de servidor (ver [Enfermedades](../05-salud/enfermedades.md)).
- La respuesta: cazar a los enfermos (*Cacería de plaga*), llevar muestras a los médicos y vacunar.

## 11. Cómo se ve en Telegram: una manada con un lobo enfermo

Piso 16, Pradera Dorada, de noche. Tú (Guerrero Protección), Lyra (Druida Restauración) y Ossian (Cazador Puntería) se cruzan con una manada de Lobos Grises. Uno está enfermo de Mal de Espuma.

**El mensaje vivo de la ronda 2:**

```
⚔️ Ronda 2 · Piso 16 · Pradera Dorada · 🌙 Noche
Manada de Lobos Grises (4)

🐺 Alfa Tuerto 👑   ❤️ ▓▓▓▓▓▓▓▓░░ 80%
🐺 Lobo             ❤️ ▓▓▓▓▓░░░░░ 50%
🐺 Lobo             ❤️ ▓▓▓▓▓▓▓▓▓▓ 100%
🤢 Lobo Enfermo     ❤️ ▓▓▓▓▓▓▓░░░ 70%
   Enfermo: Mal de Espuma (contagio ×2)

⚠️ Los lobos se abren en abanico… uno rodea
hacia la RETAGUARDIA.
⚠️🦠 El Lobo Enfermo babea espuma y clava la
mirada en LYRA.
(Lo conoces: esquivar la mordida evita el contagio)

🟥 Tú — Guerrero Protección · Vanguardia · Agrupado
❤️ 372/410   💢 Ira 40   🔋 Aguante ●●●○○
Lyra   ❤️ 238/260 · 🦠 ▓▓▓░░░░░░░ 30%
Ossian ❤️ 271/290 · 🦠 0%

Turnos: Ossian → LOBO ENFERMO → Tú → ALFA
        → Lyra → LOBO → LOBO
⏱ 45 s

[🛡 Bloqueo con escudo] [⚔️ Golpe de escudo]
[🗣 Grito desafiante]   [🌀 Torbellino]
[🔁 Fila / Formación]   [🎯 Apuntar]
[🧪 Objetos]            [📜 Registro]
```

**El mismo mensaje, ya resuelto:**

```
Ronda 2 — resumen
🎯 Ossian apunta a las PIERNAS del Lobo Enfermo:
   ya no puede huir
🦠 El Lobo Enfermo muerde a Lyra (no esquivó):
   Contagio 30% → 70%
🗣 Provocas a la manada: el lobo que rodeaba
   vuelve a la vanguardia
🩸 El Alfa Tuerto te muerde: −42 · Sangrado ▓▓▓░░
✨ Lyra se pone una cura en el tiempo
▸ Registro completo (tocar para abrir)
```

**Al terminar el combate:**

```
🏁 Victoria · Manada de Lobos Grises
Botín: Piel de lobo ★★★ · Piel de lobo ★★ ×2
       Colmillo ×6 · Trofeo del Alfa Tuerto
🧫 Muestra de Mal de Espuma (del Lobo Enfermo)
   La piden los médicos del asentamiento
⚠️ La carne del Lobo Enfermo no se puede comer

🩹 Lyra: mordida sucia en el brazo izquierdo
🦠 Contagio que quedó: 70% · se guarda 1 hora
   Limpiar la herida lo vacía.

[🩹 Limpiar y vendar]  [🧪 Suero de espuma]
[📖 Bestiario]         [🗺 Seguir]
```

**Lyra limpia la herida con una venda de lino limpio:**

```
🩹 Limpiaste la mordida (venda de lino de Mara ✒️)
🦠 Mal de Espuma 70% → 0%
Lyra no se contagió.
```

Si no la limpiaba y otra mordida llenaba la barra en esa hora, Lyra entraba en incubación sin saberlo. A las tres horas aparecían los síntomas, y para entonces solo un médico podía ganar la carrera.

## 12. Cómo se equilibra

### Contagio justo

1. **Siempre con aviso.** Todo golpe que contagia lleva 🦠 en el aviso. Nunca hay contagio por un golpe sin avisar.
2. **Barra visible, no azar.** El jugador ve cuánto falta y decide: esquivar, cambiar de fila, matar primero al enfermo.
3. **Siempre hay una ventana.** La herida sucia se puede limpiar durante una hora de juego.
4. **Tope de contagio:**
   - un combate no puede darte más de **una** enfermedad;
   - **una enfermedad seria a la vez**, salvo en epidemias (ver [Enfermedades](../05-salud/enfermedades.md)). Si ya tienes una, la barra de otra no pasa del 90 %: el golpe te hiere, pero no te contagia;
   - después de curarte, quedas inmune a esa enfermedad durante días.
5. **Los contagios de combate** (Frenesí, Marca de sangre) duran solo ese combate.
6. **Las Tácticas también cuidan el cuerpo** (ver [Avisos y tácticas](../04-combate/avisos-y-tacticas.md)). En resolución rápida el contagio sigue existiendo, pero tus reglas responden:

```
1. Si hay aviso 🦠 contra mí    → Esquivar
2. Si un aliado tiene parásito  → Arrancar parásito
3. Al terminar, si hay herida sucia → Limpiar (si llevo vendas)
```

### Protección de novato (hasta el nivel 10)

- En los pisos 1 a 10 ningún monstruo lleva enfermedades serias en su repertorio.
- Hasta el nivel 10 ninguna barra de enfermedad seria se llena: el golpe deja un **arañazo sucio** que enseña a limpiar heridas.
- No aparecen los modificadores Enfermo ni Corrupto.
- Los carroñeros no rematan derribados de nivel 10 o menos. Los ladrones no les roban.
- Los mímicos del tramo I solo asustan: muerden poco y guardan un cofre de verdad.

### Presupuesto de poder parejo

- Debilidades y resistencias con tope de **±30 %**, sin inmunidades a tipos de daño en monstruos comunes, y la regla de inmunidad a estados (§3). Así ninguna spec queda fuera contra una familia.
- El **simulador** (ver [Balance](../03-personaje/balance.md)) corre cada familia contra las 46 specs. Con juego básico, cada spec debe rendir a ±10 % de la mediana contra **cada familia**. Si una familia castiga a una spec más que eso, se cambia la familia, no la spec.
- Los remedios de caza son **consumibles para todos**, no poder de clase.
- Fobias y rasgos: como mucho un 3 % en combate. *Azote de [familia]* es premio de oficio (10 %), como permite [Rasgos adquiridos](../05-salud/rasgos-adquiridos.md).
- Las ventajas de *Ojo del Abismo* y del Frenesí no cuentan en contenido clasificado.

### Números chicos

- La vida de los monstruos va en múltiplos de la vida de un jugador del mismo tramo (§1.2).
- Ningún monstruo común pasa de 4 dígitos, tampoco con modificadores. Los únicos, de 5 como mucho. Los jefes, de 5 o 6.

### Economía y dinero real

- Todo lo que deja un monstruo **alimenta a un oficio**. Los remedios, las máscaras, las vacunas y las vendas los fabrican otros jugadores.
- Nada de esto se compra con dinero real (ver [Monetización](../07-economia/monetizacion.md)).

### Nada arruina un personaje

- Fuera del Juramento de Hierro, toda enfermedad de monstruo termina en curación o en un mal leve que se trata.
- Ningún parásito, ladrón ni mimético quita algo para siempre: lo robado se recupera o se reemplaza, y lo que llevas puesto nunca se roba.

### Cómo se prueba un monstruo

Igual que un jefe (ver [Jefes](jefes.md)): grupos de PNJ que juegan **bien** (siguen los avisos 🦠, limpian heridas) casi nunca se contagian. Grupos que juegan **mal** se contagian a menudo, pero nunca quedan sin salida. Si el grupo bueno se contagia igual, el monstruo está roto.

## 13. Cómo se conecta

Su fila en la [Red de sistemas](../00-vision/red-de-sistemas.md):

| Consume | Produce | Depende del farmeo | Depende de la fabricación | Depende de la progresión |
|---|---|---|---|---|
| Equipo, remedios de caza, máscaras, vendas, cebos, trampas, luz | Materiales de despiece y de partes, Esencia, muestras para curas, crías, artefactos menores, pacientes para los médicos, cartas y trofeos | Cebos (Cocina, Alquimia), sal, cera | Aceites, baños de plata y hierro frío, máscaras, vendas, trampas, bengalas | Conocimiento del bestiario, rangos de cazador, rango de Desuello |

**A quién le da trabajo:**

| Oficio | Qué saca de aquí |
|---|---|
| **Desuello y caza** | Todo el despiece; más con conocimiento alto |
| **Curtiduría, Peletería** | Pieles, cueros, escamas, piel ignífuga |
| **Alquimia** | Aceites, sueros, quelantes, antitoxinas, venenos de caza con glándulas |
| **Medicina** | Pacientes, muestras para vacunas, hilo de tendón, gel anestésico |
| **Herrería, Joyería** | Baños de plata y hierro frío, escamas de obsidiana, gemas, lentes |
| **Ingeniería** | Núcleos de autómata (prótesis), baterías orgánicas (desfibriladores), pólvora |
| **Inscripción** | Fichas del bestiario, tinta de pulpo, tinta luminosa |
| **Encantamiento** | Polvos, esencias, runas antiguas |
| **Agricultura, Ganadería** | Abono, semillas encantadas, huevos y crías |
| **Cocina** | Carne, cebos, infusiones |
| **Sastrería** | Máscaras, vendas limpias, seda real, algodón de nube |

**Qué se lanza primero.** Para el lanzamiento bastan las familias de los tramos I a III (unas 40 especies), con la barra de Contagio y tres enfermedades nuevas: Mal de Espuma, Pulmón de Moho y Puesta de Araña. El resto llega con cada piso nuevo.

**Queda abierto (para el dueño):**
- ¿Los mímicos pueden aparecer también fuera de las mazmorras, por ejemplo en ruinas de zona amarilla?
- ¿El Horror Sin Rostro puede imitar el nombre de un aliado real en el registro, o es mejor que imite solo a PNJ para no confundir?
- ¿La contaminación por actividad de los jugadores (§10.6) entra, o la contaminación queda solo como peligro natural?
