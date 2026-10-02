# Mazmorras, Mítica+ y bandas

> **Módulo** [06 · Contenido](README.md) · **Depende de:** [Combate](../04-combate/README.md), [Jefes](jefes.md), [Social](../08-social/gremios-y-social.md) (buscador de grupos), [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md) (dónde están las entradas, §1.15) · **Alimenta a:** [Equipamiento](../03-personaje/equipamiento.md) (botín), [Progresión](../03-personaje/progresion.md) (temporadas), [Economía](../07-economia/README.md) (materiales y piezas para vender) · **Estado:** §0 en el juego (mazmorras para uno); el resto, propuesta

> ⚠️ **Lo que decidió el dueño (1-oct-2026) manda sobre lo de abajo:** las mazmorras tienen estructura fija y cambian cada día de facción, jefe, camino y botín; todo tipo de enemigo tiene su jefe; la misma mazmorra se corre con 5, 10, 20 o más de 25 jugadores, con más dificultad y recompensa; tanques y curadores con recompensa propia (D-164). Para el jugador solo: mazmorras chicas de recompensa modesta y mazmorras profundas por pisos (D-170). Jefes de mundo (D-150) y PvP en mazmorras: en la segunda tanda de la entrevista (P-108, P-110).

---

## 0. En el juego: mazmorras para uno (D-164, D-165, D-170, D-171)

El dueño pidió (1-oct-2026) mazmorras con **estructura fija que cambian cada día** (D-164), botín que **no está cortado a tu medida** (D-165), tres caminos para el que juega solo: **mazmorras chicas** de recompensa modesta y **mazmorras profundas por pisos** (D-170), y un mapa que **muestra que hay algo, no qué es** (D-171). Esta es la **capa simple** (D-44), ya en el juego. Los números son propuesta de Claude (se ajustan en la beta) y viven en `content/balance.yaml` → `dungeons`; las familias de enemigos, en `content/dungeons.yaml`; las cuentas, en `engine/world/dungeons.py`; las pantallas, en `engine/service/game.py` (sección "solo dungeons"); los textos, en `content/locales/es_mazmorras.yaml`. Pruebas: `tests/test_mazmorras.py`.

### 0.1 Dónde están

- El mapa se parte en **tramos de 6 × 6 zonas**; cada tramo tiene **2 entradas, o 3 con 50 %** (D-181, desde la 0.26.1; antes 1 o 2), en zonas de **Lejanía 2 o más**, nunca pegadas dentro del tramo. En un mapa de 13 × 13 hay unas 10 a 12 (solo ves las cercanas). **1 de cada 4 es 🌀 profunda**; las demás, 🕳️ chicas.
- El lugar sale solo de la semilla del mundo y las coordenadas: **nunca se mueve** y es el mismo para todos. Nunca hay una en el Claro ni en la guarida del Guardián. El **territorio de un campamento de jugadores** la tapa mientras exista (como a los campamentos enemigos). Un **👹 campamento enemigo** en pie sobre su zona tapa la entrada ese día: 🧭 Explorar muestra el menú del campamento y, cuando cae, la entrada se abre otra vez.
- **En el 🗺️ Mapa** (D-171, D-181): la 🕳️ cueva (hasta la 0.26, ❓) si anduviste cerca (a 2 zonas o menos de una que recuerdas): sabes que hay una mazmorra, no cuál. Al pisar la zona, o estudiarla desde la de al lado (explorar alrededor, D-107), sabes qué es: 🕳️ chica o 🌀 profunda. Debajo del mapa, las 3 más cercanas, y el botón **🕳️ Ir a la cueva** o **🕳️ Ir a la mazmorra** te lleva zona por zona. Detalle en [Mapa infinito y viaje](../02-mundo/mapa-infinito-y-viaje.md) §1.15.
- **En la zona:** al llegar lo dice ("🕳️ ¡La entrada de una mazmorra chica!"), 📍 Zona muestra qué familia la ocupa hoy y **🧭 Explorar** cambia 🏹 Cazar por **🕳️ Entrar** o **🌀 Descender** (siguen siendo 4 botones). 🏹 Cazar pasa adentro de la pantalla de la mazmorra.

### 0.2 Lo que cambia cada día y lo que no

| Cambia cada día (igual para todos) | No cambia nunca |
|---|---|
| **La familia que la llena** (hoy duendes, mañana limos, pasado dragones): una de las 14 de `content/dungeons.yaml`, sin importar el bioma. Cada mazmorra tiene su propio orden: en cada vuelta de 14 días sale cada familia una vez, y **nunca la misma dos días seguidos** | El lugar y el tipo (🕳️ o 🌀) |
| **El jefe**: el más fuerte de esa familia que cabe en el nivel de la mazmorra, en versión élite (**+80 % de vida, +20 % de ataque**). Así todo tipo de enemigo tiene su jefe | El nivel: el de la zona **+ 1**, como los campamentos enemigos |
| **El camino**: los nombres de las 4 salas y de la sala del jefe ("🔥 la forja fría → 💧 la cisterna → … → 👑 la sala del trono") | La estructura: la chica, **4 salas y el jefe**; la profunda, pisos que se endurecen |
| **El botín**: los materiales del cofre y de la bolsa son los de la familia del día | Que las peleas son siempre a mano (nunca automáticas, D-114) |

Las 14 familias cubren a los 100 enemigos comunes: 🐺 manada de lobos, 🐻 osos y fieras, 🐗 bestias de colmillo y cuerno, 🕷️ arañas e insectos, 🟢 limos del cieno, 🍄 hongos y plantas vivas, 💀 no muertos, 👻 espectros, 🗡️ forajidos y cultistas, 👹 duendes, ogros y gigantes, 🐉 sierpes y dragones, 🗿 gólems y elementales, 🦅 bestias aladas y 🐀 alimañas. En cada sala sale un enemigo de la familia cuya franja de nivel tiene el nivel de la mazmorra (o la más cercana, como D-108), **con el nivel de la mazmorra**: las franjas de `enemies.yaml` escalan parejo (D-110), así un lobo de nivel 30 es tan duro como cualquier enemigo común de nivel 30.

### 0.3 🕳️ La mazmorra chica (como los *delves* de Elder Scrolls Online)

- **Estructura fija:** 4 salas y el jefe, 5 peleas a mano de **2 ⚡** cada una (10 ⚡ toda la mazmorra; como una presa o un asalto, D-108).
- **Toda la energía de entrada (D-196, en el juego desde la 0.29.1):** para pelear la siguiente sala hay que tener la energía de **todas** las peleas que faltan hoy (10 ⚡ al empezar, 2 antes del jefe). Se sigue cobrando pelea por pelea; nadie queda a medias.
- **Tu avance es tuyo y dura el día:** cada victoria despeja una sala (✅); si huyes o caes, **lo despejado hoy queda** y sigues desde la siguiente cuando quieras. Al otro día empieza de cero, con otra familia.
- **El cofre del jefe, una vez por mazmorra y día:** monedas de **1,5 peleas comunes** de su nivel (nivel 7: 10 🥉; nivel 40: 29 🥉), **1 a 3 materiales** de la familia del día (D-165: también de otros oficios, como 💠 gema en bruto, 🌸 flor de luna o 🔩 lingote) y **20 %** de una pieza de equipo de su nivel **de cualquier clase y tipo** (D-165: si no es tuya, se vende; nunca equipo de artesano). **No da experiencia extra**: la experiencia es la de las 5 peleas (D-118). La pantalla muestra el cofre de hoy antes de entrar.
- **Pantalla:** el nivel, la familia y el jefe de hoy, el camino, las salas despejadas, el cofre y **[⚔️ Sala N · ⚡2]** (o **[👑 Jefe · ⚡2]**) **[🏹 Cazar] [↩️ Volver]**. Tras ganar una sala sale **⚔️ Sala N+1** en el final de la pelea.

### 0.4 🌀 La mazmorra profunda (como el *Deep Dungeon* de Final Fantasy XIV)

- **Bajas piso a piso hasta donde aguantes.** Son pisos de la mazmorra, no del mundo (D-58 sigue). Entrar cuesta **2 ⚡** más la primera pelea; cada pelea, **2 ⚡**. **Cada piso es una acción (D-196):** para empezarlo hay que tener la energía de todas sus peleas (y la entrada si no hay bajada abierta).
- **Cada piso:** el 1 tiene 1 pelea; desde el 2, 1 o (con 35 %) 2; **cada 5 pisos, la última es el jefe** de la familia de hoy (élite, encima de lo del piso). Cada piso más abajo los enemigos suben **1 nivel**, **+5 % de vida** y **+3 % de ataque** (piso 10: nivel + 9, +45 % de vida, +27 % de ataque).
- **Entre pisos no hay curación:** mientras la bajada está abierta **la vida no vuelve sola**; solo lo del cinturón (que se rellena de la mochila como siempre) y 🧪 Pociones. Subir de nivel en una pelea sí llena la vida, como siempre.
- **La bolsa:** cada piso despejado suma monedas de **media pelea común** de su nivel y **1 material** de la familia; cada piso de jefe, **30 %** de una pieza de cualquier clase (D-165). Lo que ganas **en cada pelea** (experiencia, monedas, botín) es tuyo igual, como en toda pelea.
- **⬇️ Bajar o 🚪 Salir con lo ganado** después de cada pelea: salir cobra **la bolsa entera**. **Si caes o huyes**, la bajada termina y te quedas con **la mitad** (monedas, cada material y las piezas, redondeado hacia abajo); caer además tiene lo de siempre (malherido y 10 % de las monedas). Irte de la zona, ponerte a hacer otra cosa o que cambie el día cierra la bajada como si salieras (bolsa entera).
- **Tu récord** (el piso más hondo que despejaste, para siempre) y **🏆 la lista de hoy** de esa mazmorra (los 3 más hondos) salen en su pantalla.
- **Pantalla:** sin bajada abierta, **[🌀 Descender · ⚡4] [🏹 Cazar] [↩️ Volver]**; con una abierta, el piso, la bolsa, lo que sigue y **[⬇️ Bajar al piso N · ⚡2 o ⚡4] [🚪 Salir con lo ganado] [🧪 Pociones] [↩️ Volver]** (el botón de bajar muestra la energía de todo el piso: 4 si tiene 2 peleas).

### 0.5 Cuánto da (registro de [Balance](../03-personaje/balance.md) §7)

La experiencia es la de las peleas, a la par de cazar (D-108, D-118: `hero.xp_formula` no se tocó). Promedio de las 14 familias frente al promedio de los 8 biomas con peligro:

| Zona | 🏹 Cazar | 🕳️ Chica (10 ⚡) | 🌀 Profunda, 5 pisos (~16 ⚡ con la entrada) |
|---|---|---|---|
| 3 | 26 de experiencia por ⚡ · 3,3 🥉 | 28 (×1,07) · 4,0 🥉 (×1,23) | 30 (×1,16) |
| 10 | 52 · 6,0 🥉 | 54 (×1,04) · 6,7 🥉 (×1,12) | 54 (×1,03) |
| 20 | 85 · 10,3 🥉 | 85 (×0,99) · 10,4 🥉 (×1,01) | 79 (×0,93) |
| 60 | 222 · 29,8 🥉 | 228 (×1,03) · 32,3 🥉 (×1,09) | 204 (×0,92) |
| 90 | 327 · 46,4 🥉 | 337 (×1,03) · 52,2 🥉 (×1,13) | 297 (×0,91) |

La chica da lo de cazar más un poco (el nivel + 1 y el cofre: unas 1,5 peleas de monedas, 1 a 3 materiales y 20 % de una pieza); la profunda da algo menos por ⚡ en los primeros pisos (la entrada cuesta) y más a medida que bajas (el nivel sube 1 por piso), siempre con el riesgo de perder la mitad de la bolsa. El viaje hasta la entrada y las pociones que se gastan comen la diferencia.

**Medido con el motor** (`tools/balance_report.py`, puntos y botín de su nivel, el héroe del nivel de la zona): el jefe de la chica se gana **94-100 %** de las veces en las zonas 3, 10, 60 y 90 (79 % en la 30, con un bache para dos especializaciones de curación), como el de un campamento enemigo. En la profunda, sin curarse y con 3 pociones y 2 vendas en el cinturón (y otras tantas de repuesto), se bajan **3 o 4 pisos** en promedio en los niveles bajos y medios, y **8 a 10** en los altos (las defensas, mucho más). Detalle en [Balance](../03-personaje/balance.md) §7.

### 0.6 Lo que todavía no entra

- **Grupos de 5, 10, 20 o más de 25** en la misma mazmorra, con más dificultad y recompensa, y la recompensa propia de tanques y curadores (D-164): después.
- **Mazmorras de grupo y jefes de mundo** (P-108, P-110): sin decidir.
- **Cuánto del botín global es de tu tipo** (P-111): sin decidir; el botín de las peleas sigue igual (70 % de tu tipo). Solo el cofre y la bolsa de las mazmorras siguen D-165 (cualquier clase por igual).
- **Enfermedades** que transmiten los enemigos (D-166): después.
- La Mítica+, las bandas y lo de §1-4: siguen siendo propuesta.

### 0.7 De dónde sale

- **Los *delves* de Elder Scrolls Online** (y los de *The War Within* de WoW): mazmorras cortas para uno, de recompensa modesta, que se hacen en una sesión.
- **El *Deep Dungeon* de Final Fantasy XIV** (*Palace of the Dead*): pisos hacia abajo, cada uno más duro, sin volver a curarte entre pisos, y la decisión de seguir o salir con lo ganado.
- **La rotación diaria** (D-164) toma la idea de las mazmorras con afijos de WoW, pero cambia lo de adentro (la facción) y no las reglas.

### 0.8 Decisiones de Claude (provisionales, para que el dueño las confirme)

1. **Tramos de 6 × 6 con 2 o 3 entradas, 1 de cada 4 profunda.** D-171 decía "1 o 2 mazmorras por tramo" y D-181 "2 o 3 por zona" (entendido por tramo, D-182; a confirmar en E-126); el tamaño del tramo lo fijó Claude.
2. **La mazmorra toma el lugar de 🏹 Cazar en 🧭 Explorar** (en esa zona) para seguir en 4 botones; 🏹 Cazar queda dentro de la pantalla de la mazmorra.
3. **El territorio de un campamento de jugadores tapa la entrada** y **un campamento enemigo en pie la bloquea ese día** (el lugar de las mazmorras es fijo y el de los campamentos enemigos cambia cada día).
4. **El cofre no da experiencia** y vale unas 1,5 peleas de monedas, para que la chica quede "modesta" (D-170) y la experiencia por ⚡ a la par de cazar (D-118).
5. **Huir en la profunda cuenta como caer** para la bolsa (te quedas con la mitad), pero sin quedar malherido ni perder monedas.
6. **Mientras la bajada está abierta la vida no vuelve sola**; irte de la zona, hacer otra cosa o el cambio de día cierran la bajada con la bolsa entera.
7. **Los enemigos de la mazmorra usan el nivel de la mazmorra**, aunque su franja de `enemies.yaml` sea otra (las franjas escalan parejo desde D-110); el jefe es el más fuerte de los que caben en ese nivel.

---

## 1. Mazmorras

Grupos de 5: 1 tanque, 1 sanador y 3 de daño, o 1 apoyo y 2 de daño. Cada región tiene 1 o 2 mazmorras, y cada anillo, 4 a 6 en rotación.

| Dificultad | Qué cambia | Bloqueo |
|---|---|---|
| **Normal** | Para aprender la mazmorra | Sin bloqueo |
| **Heroica** | Más daño y mecánicas extra | Diario |
| **Mítica** | Jefes con una fase adicional | Semanal |
| **Mítica+** (Llave de Mazmorra) | Ver §2 | Sin bloqueo |

**Buscador de grupos.** Te anotas por rol, el bot arma el grupo y abre una sala retransmitida (ver [Telegram](../01-plataforma/telegram.md)). Los grupos de gremio se arman en el chat del gremio.

## 2. Mítica+ con reloj de rondas

**De dónde sale.** Las piedras angulares de WoW: una llave con nivel, un temporizador y afijos que rotan cada semana. Si terminas a tiempo, la llave sube; si no, baja. Es el contenido de grupo más jugado de WoW desde 2016.

**Cómo se adapta a turnos.** El reloj no mide minutos: mide **rondas totales**. Cada llave tiene un límite, por ejemplo 120 rondas para toda la mazmorra.
- A tiempo, la llave sube 1 nivel. Con el 80 % de las rondas o menos, sube 2; con el 60 % o menos, sube 3.
- Si no se termina a tiempo, baja 1 nivel, y se sigue cobrando la recompensa por completarla.
- Cada caída suma rondas al reloj.
- Los niveles no tienen techo: es la escalera infinita del juego.

**Afijos semanales** (adaptados a turnos):

| Nivel | Afijo |
|---|---|
| +2 | **Guía:** sin penalización por caídas mientras se aprende (idea de *Midnight*) |
| +5 | Uno de cuatro, que rota: *Sangriento* (los enemigos dejan charcos que curan a otros enemigos si no se cambia de fila), *Explosivo* (aparecen orbes que hay que romper antes de 2 rondas), *Volcánico* (fuego avisado en una fila al azar), *Inspirador* (un enemigo por grupo es inmune al control) |
| +7 | *Tiránico* (jefes más fuertes) o *Fortificado* (enemigos comunes más fuertes) |
| +10 | Los dos a la vez |
| +12 | *Implacable:* cada caída cuesta el triple de rondas |

- **Temporadas** de 3 a 4 meses con 8 mazmorras en rotación, como en WoW; puntuación por jugador y título para el 0,1 % superior.
- Las Llaves de Mazmorra también son **moneda social**: se ofrecen en el chat del gremio.

## 3. Bandas

**De dónde sale.** Las bandas de WoW, con sus dificultades Buscador, Normal, Heroica y Mítica. En 2026, *Midnight* estrenó la Mítica flexible de 15 a 25 jugadores.

- **Una banda por anillo**, en su capital regional (la del anillo I, en Lejanía 3), con 6 a 9 jefes.
- **Tamaño flexible de 10 a 25** en todas las dificultades. La vida y la postura de los jefes escalan con la cantidad de jugadores; las mecánicas no.
- **Dificultades:** Buscador (armada por el bot, fácil, recompensa baja), Normal, Heroica y Mítica (para gremios organizados).
- Bloqueo semanal por jefe.
- Temporizador de 60 a 90 s por ronda, con el chat de la banda dentro de la pelea (TowerWars ya lo hace en su Torre de Gremio).
- Los jefes dan tareas a varios subgrupos a la vez: uno contiene invocaciones, otro rompe la postura, los sanadores se reparten las filas.

**Botín.** Personal por defecto, con 2 horas para regalarlo dentro del grupo, como en WoW. Los gremios pueden activar el reparto por maestro de botín en Mítica. En los grupos armados al azar, "Necesidad / Codicia" se tira con el 🎲 nativo en el chat de la sala (ver [Gremios y social](../08-social/gremios-y-social.md)).

## 4. Qué da cada cosa

Para que nadie esté obligado a hacer lo que no le gusta:

| Contenido | Lo que da mejor que nadie |
|---|---|
| Mazmorras y Mítica+ | Equipo de temporada, Esencia, puntuación |
| Bandas | Artefactos de jefe, planos, prestigio de gremio |
| Profundidades | Equipo para el que juega solo, progreso del compañero |
| Expediciones | Materiales de zona, vetas buenas |
| Asaltos a Guardianes | Recuerdos, títulos de Pionero, avance de la Frontera |
| PvP | Oro, recompensas de PvP, territorios |
