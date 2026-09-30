# PvP: de la arena a las zonas negras

> **Módulo** [06 · Contenido](README.md) · **Depende de:** [Combate](../04-combate/README.md), [Facciones](../02-mundo/facciones.md), [Balance](../03-personaje/balance.md) · **Alimenta a:** [Economía](../07-economia/economia.md) (materiales de riesgo, botín), [Progresión](../03-personaje/progresion.md) (temporadas) · **Estado:** propuesta

**Principio.** El PvP es **opcional para progresar**: hay una prueba de Sello para quien lo quiera (ver [Torre y pisos](../02-mundo/torre-y-pisos.md)). Y es **necesario para la economía**, porque los mejores materiales están donde hay riesgo. Nadie está obligado a pelear contra jugadores; quien lo hace, gana más.

---

## 1. Zonas por color

**De dónde sale.** Albion Online (zonas azules, amarillas, rojas y negras) y EVE Online (seguridad alta, baja y nula).

| Zona | PvP | Al caer (ver [Secuelas y muerte](../05-salud/secuelas-y-muerte.md)) | Qué se consigue ahí |
|---|---|---|---|
| 🔵 **Azul** | No | No se cae | Servicios |
| 🟡 **Amarilla** | Solo con **bandera** voluntaria | Esencia en la mancha; nadie te saquea | Recursos básicos del tramo |
| 🔴 **Roja** | Libre | Pueden saquear tu mochila | Recursos medios, jefes de campo |
| ⚫ **Negra** | Libre | Botín completo, con destrucción | Los mejores recursos, territorios de gremio, jefes ocultos |

La bandera amarilla da un pequeño bono de botín mientras está activa: quien acepta el riesgo, gana más.

## 2. Karma: el color del cursor

**De dónde sale.** SAO (cursor verde para los jugadores normales, naranja para quien atacó a un inocente, rojo para los asesinos), *Lineage 2* (karma), *Tibia* (calaveras) y *Ultima Online* (contador de asesinatos).

| Estado | Cómo se llega | Consecuencias |
|---|---|---|
| 🟢 **Verde** | Normal | — |
| 🟠 **Naranja** | Atacar primero a un verde en zona roja | Durante 1 hora cualquiera puede atacarte sin volverse naranja, y los guardias de los asentamientos no te venden |
| 🔴 **Rojo** | Matar a varios verdes (por ejemplo, 3 en 24 horas) | No puedes entrar a asentamientos azules, solo a refugios de forajidos. Al caer pierdes más (una pieza equipada al azar incluso en zona roja). Tu cabeza tiene **recompensa** automática |

- **Redención:** el karma baja con el tiempo, con misiones de penitencia o pagando una multa (sumidero de oro).
- En zona negra no hay karma: todos son presa.

## 3. Cazarrecompensas y prisión

- **Recompensas.** Cualquiera puede poner oro por la cabeza de un jugador rojo, o de un rival en zona negra. Quien lo mata cobra, menos una comisión (sumidero). Los contratos son públicos en el tablón.
- **Prisión.** Un rojo atrapado por los guardias, o entregado por un cazarrecompensas con *Grilletes*, pasa un tiempo en la prisión de la capital. Allí solo puede hacer trabajos forzados: recolección básica que va al asentamiento. Idea tomada de la cárcel de *Torn*.

## 4. Invasiones al estilo Souls

**De dónde sale.** Los invasores de *Dark Souls* y *Elden Ring*: un jugador entra al mundo de otro para cazarlo.

- Con un **Dedo de Sangre** (lo fabrican los inscriptores) un jugador puede **invadir** a otro que esté en una expedición, en una zona roja o negra, o en una Profundidad marcada como "abierta a invasores".
- El invadido puede pedir ayuda con los signos de sus aliados (ver [Jefes](jefes.md)).
- Si gana el invasor, cobra recompensa; si ganan el invadido y sus ayudantes, cobran ellos.
- **Nunca** en zonas azules, ni en amarillas sin bandera, ni en mazmorras normales, ni contra jugadores de nivel mucho menor.

## 5. Duelos y arenas

**Duelo.** Cualquier jugador puede retar a otro en un asentamiento. Sin consecuencias y sin heridas: se pelea a primera sangre.

**Arena asíncrona.** Peleas contra una **foto** de otro jugador que maneja la IA con sus [Tácticas](../04-combate/avisos-y-tacticas.md). Es rápida, no hay que esperar a nadie, y tus Tácticas son tu defensa. TowerWars ya tiene este formato y funciona como puerta de entrada al PvP.

**Arena en vivo:**

| Modo | Formato | De dónde sale |
|---|---|---|
| **1v1** | Clasificatoria | — |
| **2v2 y 3v3** | Clasificatoria, con equipos fijos | WoW |
| **Solo Shuffle** | Te anotas solo. 6 jugadores (2 sanadores y 4 de daño) juegan 6 rondas con todas las combinaciones posibles | WoW (*Dragonflight*). Ideal para Telegram: nadie tiene que armar equipo |
| **Todos contra todos** | 6 jugadores; gana el último en pie | — |

- **Clasificación Glicko-2**, mejor que Elo para jugadores que entran y salen, como es típico en Telegram.
- **Temporadas** de 3 meses, con títulos para los mejores (*Gladiador de la Torre*) y cosméticos por rango.
- **Equipo normalizado en clasificatoria.** Todos pelean con una plantilla de estadísticas según su spec; tu equipo aporta sus técnicas y sus afijos con peso limitado. Decide la habilidad, no quién farmeó más. WoW probó plantillas en *Legion*; aquí se usan desde el primer día en la clasificatoria, y en el mundo abierto cuenta el equipo completo.
- Reglas de PvP (ver [Ronda y acciones](../04-combate/ronda-y-acciones.md)): Firmeza, amortiguación de curación desde la ronda 8, ningún golpe puede quitar más del 40 % de la vida, modificadores por spec.

## 6. Campos de batalla por nodos

Los campos de batalla de WoW (capturar la bandera, controlar bases) no funcionan en tiempo real por texto. Sí funcionan como **juego de tablero**:
- El mapa es un **grafo de 5 a 9 nodos**: minas, torres, santuarios.
- Juegan de 8 a 15 jugadores por bando. Cada ronda (60 s), cada uno elige moverse a un nodo, atacar, defender o capturar.
- Los choques en cada nodo se resuelven con el combate normal, en paralelo en todos los nodos.
- Controlar nodos da puntos por ronda. Gana el primero en llegar a 1.000 puntos, o quien tenga más al final de 30 rondas.

| Campo | Regla | Inspiración |
|---|---|---|
| **Paso de las Espinas** | Captura la reliquia y llévala a tu base | Garganta Grito de Guerra |
| **Cuenca de Cristal** | 5 nodos, puntos por nodo | Cuenca de Arathi |
| **Valle de Hierro** (épico, 40 contra 40) | Asedio con jefes PNJ en cada base; dura horas, con rondas lentas | Valle de Alterac |
| **Relámpago** | 8 contra 8, partidas de 12 rondas, cola individual | *Blitz* de WoW (2024) |

## 7. Guerra de facciones

**De dónde sale.** Chat Wars, el juego de este género más longevo de Telegram (desde 2016): cada jugador elige atacar otro castillo o defender el suyo antes de una batalla a hora fija, y el resultado se publica en un canal. TowerWars adoptó el mismo formato con 4 castillos y dos batallas al día, y funciona.

**Cómo funciona aquí:**
- **Cada castillo es una facción** (ver [Facciones](../02-mundo/facciones.md)). La guerra empieza con el primer cisma: antes no hay contra quién pelear.
- **Dos batallas al día** a hora fija, con aviso 15 minutos antes (horario por definir: P-31).
- Antes de cada batalla, cada jugador elige: **atacar** un puesto enemigo, **defender** uno propio o **no participar**.
- Las facciones controlan **puestos avanzados** en los pisos, al principio uno por tramo. Las batallas deciden quién los conquista o los defiende.
- **Poder de guerra:** sale del mismo número de poder que usa todo el juego (clase, equipo y talentos), con una sola fuente de verdad. TowerWars tuvo un error serio porque la guerra calculaba el poder por su lado y el equipo no contaba.
- **Reglas probadas en TowerWars:** quien ataca no defiende; solo cuentan los jugadores activos en los últimos 3 días; romper un puesto vacío no paga.
- Controlar el puesto de un piso le da a tu facción un pequeño descuento en los impuestos de ese asentamiento, acceso a una veta especial y la posibilidad de cobrar peaje a las caravanas de otras facciones.
- **Parte narrado** en la Gaceta, que se puede reenviar.
- Trofeos por jornada y por temporada, con bono del débil (ver [Facciones](../02-mundo/facciones.md)).

## 8. Guerras de gremio y territorios

**De dónde sale.** Los territorios de Albion en zonas negras, los asedios de castillos de *Lineage 2*, la soberanía de EVE y *Bastion Siege* (estrategia de fortalezas por Telegram, hacia 2017).

- Hay **territorios** en las Profundidades (zonas negras) de cada piso desde el tramo IV.
- Un gremio, o una alianza de gremios, reclama un territorio con un **estandarte**. Para defenderlo construye y mantiene una **fortaleza** (con constructores de rango; ver [Construcción](../09-construccion/README.md)) y paga un mantenimiento semanal (sumidero).
- **Ventanas de asedio** semanales a una hora fija que elige el defensor dentro de un rango, para que nadie ataque a las 4 de la mañana del defensor.
- El asedio usa el tablero de nodos (§6), con murallas, puertas y armas de asedio fabricadas por ingenieros y carpinteros.
- **Qué da un territorio:** una veta o un jardín exclusivo, impuestos sobre lo que se recolecta ahí, un salón con bonos de fabricación para los miembros y prestigio en el mapa.

## 9. PvP y Juramento de Hierro

Los personajes del Juramento de Hierro (muerte permanente) **no pueden ser atacados** fuera de las zonas negras y las arenas, y en la arena caer no los mata. Morir para siempre por culpa de otro jugador en una zona roja sería la forma más rápida de que nadie juegue ese modo. Si entran a una zona negra, aceptan el riesgo, y la Gaceta lo cuenta.

Ver P-26 a P-31 en [Preguntas abiertas](../00-vision/preguntas-abiertas.md).
