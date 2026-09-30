# Balance: que todas las clases valgan lo mismo, y que se pueda medir

> **Módulo** [03 · Personaje](README.md) · **Condiciona a:** [Clases](clases-y-especializaciones.md), [Equipamiento](equipamiento.md), [Combate](../04-combate/README.md), [PvP](../06-contenido/pvp.md) · **Estado:** propuesta

Pediste corregir los problemas de calibración de WoW y que las clases queden igualadas. Este documento dice **qué está roto**, **qué reglas lo impiden aquí** y **cómo se mide** que las reglas se cumplan.

---

## 1. Qué está roto en WoW

| # | Problema | Evidencia | Qué hacemos aquí |
|---|---|---|---|
| 1 | **Specs que dominan el meta** | Temporada 1 de *Midnight*: Reprensión y Mago de Escarcha arriba en M+; Mago de Fuego al fondo | Presupuesto de poder por spec, simulador y objetivos numéricos (§2 y §3) |
| 2 | **Tanques desiguales** | Temporada 1 de *Midnight*: en llaves altas dominó el Maestro Cervecero y el resto casi no aparecía | Mismos objetivos de mitigación y autonomía para los 6 tanques |
| 3 | **"Impuesto híbrido"** | Durante años las clases puras pegaron más por diseño; en *Icecrown Citadel* el Sacerdote Sombra rendía un 6 % menos a propósito | La unidad de balance es la **spec**, no la clase: mismo rol, mismo objetivo |
| 4 | **Utilidades obligatorias** | Ansia de Sangre fue exclusiva del Chamán hasta 2010, y hoy los grupos siguen buscando "lust" y resurrección en combate | Cada utilidad clave la tienen 4 o más clases **y** un consumible fabricado. Ninguna clase es obligatoria |
| 5 | **Apoyo que se apila** | El Evocador de Aumentación apilado permitió matar un jefe Mítico en unos 30 s. Blizzard admitió que "su contribución es demasiado impactante" | Los efectos de apoyo del mismo tipo **no se suman**, con tope de un apoyo por grupo en contenido clasificado |
| 6 | **Control encadenado en PvP** | El sistema de rendimientos decrecientes se reescribió en 12.0 para dar inmunidad tras 2 aplicaciones | **Firmeza** desde el primer día (ver [Ronda y acciones](../04-combate/ronda-y-acciones.md)) |
| 7 | **Sanadores inmortales o inútiles en arena** | WoW baja la curación a medida que avanza la partida ("dampening") | Amortiguación de curación por ronda en PvP |
| 8 | **Inflación de números** | En *Shadowlands* hubo que comprimirlo todo (nivel 120 → 50) porque el daño iba camino a los miles de millones | Números chicos desde el diseño (§4) |
| 9 | **Poder prestado** | Artefactos, Azerita, Pactos: poder que se da en una expansión y se quita en la siguiente. Blizzard reconoció el problema | Todo sistema de poder es permanente; lo temporal solo existe en ligas opcionales |
| 10 | **Raciales de combate** | Humano, Orco y No-muerto en PvP (ver [Creación](creacion-de-personaje.md)) | Ninguna racial toca el combate |
| 11 | **Suerte con el botín** | Semanas sin el objeto que necesitas; el Gran Tesoro semanal nació para paliarlo | Protección contra mala racha y recompensas deterministas de jefe (ver [Equipamiento](equipamiento.md)) |
| 12 | **Apilar clases en banda** | *Sunwell* (TBC) y los Evocadores de Aumentación | Aportes de grupo que no se suman y jefes diseñados para composiciones libres |
| 13 | **Botoneras enormes** | Rotaciones de más de 20 habilidades, que *Midnight* tuvo que podar | **8 botones por combate**, nunca más |

## 2. Las reglas que no se negocian

1. **La spec es la unidad de balance.** Se compara Protección con Sangre y con Venganza, no Guerrero con Caballero de la Muerte.

2. **Presupuesto de poder de 100 puntos por spec**, repartido en seis ejes:

   | Eje | Qué mide |
   |---|---|
   | Daño sostenido | Daño por ronda contra un objetivo en una pelea larga |
   | Ráfaga | Daño en una ventana corta (3 rondas) |
   | Supervivencia | Mitigación, autocuración, defensivos |
   | Control | Aturdir, silenciar, interrumpir, retrasar iniciativa |
   | Utilidad de grupo | Aportes, curas externas, resurrección, disipar |
   | Autonomía | Qué tan bien juega en solitario (misiones, Profundidades, expediciones) |

   - Cada spec suma 100 ± 3.
   - Ningún eje pasa de 35 ni baja de 5.
   - El perfil de cada spec se publica en la guía del juego como un gráfico de radar: el jugador sabe qué eligió.

3. **Kit mínimo garantizado.** Toda spec tiene una interrupción (o algo equivalente), un defensivo mayor, un defensivo menor o autocuración, un control, una forma de reposicionarse o escapar, y un aporte de grupo. En WoW hubo clases que pasaron expansiones enteras sin interrupción o sin defensivos.

4. **Autonomía mínima.** Toda spec puede hacer sola el contenido en solitario (misiones, encargos, Profundidades normales). Sanadores y tanques tienen un **modo en solitario** automático que convierte parte de su curación o mitigación en daño cuando juegan solos. Es crítico en Telegram, donde mucha gente juega sola a la hora que puede.

5. **Aportes de grupo equivalentes y no acumulables.** Cada clase aporta un efecto de grupo de valor parecido (alrededor del 3 % del rendimiento del grupo), y dos del mismo tipo no se suman.

6. **Utilidades clave compartidas, más un consumible fabricado:**
   - **Clamor** (el "lust"): +30 % de iniciativa y una acción rápida extra durante 3 rondas, una vez por pelea. Lo tienen Chamán, Mago, Cazador, Evocador y Bardo, y también los Tambores de Guerra (Peletería).
   - **Resurrección en combate** (cargas compartidas por pelea): Caballero de la Muerte, Druida, Brujo, Paladín y Nigromante, más las Sales de Reanimación (Medicina) y el Desfibrilador (Ingeniería).
   - **Disipar magia, curar veneno, curar enfermedad**: cada una la tienen al menos 4 clases.

7. **Estadísticas secundarias aplanadas.** Para ninguna spec una secundaria puede valer más de 1,3 veces otra, y todas tienen rendimientos decrecientes suaves. Se acaba el "esta spec solo quiere celeridad".

8. **Mismo escalado con el equipo.** Todas las specs escalan igual con el Poder de Objeto. El simulador lo comprueba en cada tramo: ninguna spec puede "despertar" en el tramo 8 ni morirse en el 3.

9. **Dificultad declarada, techo parejo.** Cada spec lleva una etiqueta de dificultad (★ a ★★★), y el simulador mide dos cosas:
   - **Juego básico**, con las [Tácticas](../04-combate/avisos-y-tacticas.md) automáticas por defecto: todas las specs a ±10 % de la mediana.
   - **Juego óptimo**, con el mejor plan posible: todas a ±3 %.

   Así una spec fácil no domina y una difícil no queda inútil. En un juego por turnos no hay velocidad de dedos: la dificultad es **planificar**.

10. **Sin poder racial, sin poder prestado, sin clase obligatoria.** Los jefes se diseñan para composiciones libres; ninguna pelea pide "dos Chamanes".

## 3. Cómo se mide

**Simulador de combate** (el equivalente a SimulationCraft, módulo M21). Corre cada spec contra un conjunto fijo de escenarios en cada tramo de equipo: un objetivo, varios objetivos, pelea con cambios de fila, pelea con fases, y PvP 1v1 contra cada una de las otras specs. Corre con cada cambio de balance y **antes** de publicarlo.

**Objetivos numéricos:**

| Métrica | Objetivo |
|---|---|
| Daño sostenido (juego óptimo) | Toda spec de daño a ±3 % de la mediana |
| Ráfaga | ±5 % |
| Mitigación efectiva de tanques | ±4 % |
| Curación efectiva de sanadores | ±4 % |
| Victorias por spec en arena clasificada | 47-53 % |
| Popularidad en contenido alto (M+ 15 o más, top 500 de arena) | Ninguna spec por encima del doble del promedio |

**Ritmo y registro:**
- Ajustes cada dos semanas; urgencias en cualquier momento.
- Cada número que se mueve va a un **registro de balance** con su antes → después y la medición que lo justifica. TowerWars trabaja así ("si un número de balance se movió y no está ahí, se movió a ciegas"), y aquí es obligatorio desde el día uno.
- **Consejo de clase:** por cada clase, un grupo de jugadores de referencia que recibe los cambios una semana antes. Su opinión entra en una cola de feedback clasificada por tema y gravedad.

## 4. Números chicos, para siempre

- Vida de un héroe: 100 al nivel 1, y del orden de 1.500 a 3.000 al nivel 100 con buen equipo.
- Golpes de un jugador: entre 20 y 400. Ningún número de jugador en pantalla pasa de 4 dígitos.
- Jefes: vida de 5 o 6 dígitos, nunca más.
- Mitigación de armadura con la fórmula **`def / (def + K)`** (la misma que usa TowerWars, con K = 60), con una K que crece por tramo para que la armadura nunca se convierta en inmunidad.
- Cada tramo sube los números alrededor de un 25 %, no un 100 %. Así el equipo de dos tramos atrás sigue sirviendo para algo: venderlo, desmontarlo o vestir a un alt.

## 5. Lección de TowerWars: nada de puntos de estadística sueltos

TowerWars reparte un punto de personaje por nivel en ataque, defensa, vida o maná. Su propio documento de estado reconoce dos problemas:
- +1 de vida no es una elección real al lado de +1 de ataque: uno mueve el 1 % y el otro el 20 %.
- Después de un reinicio, los jugadores recibieron repartos distintos según la fecha en que llegaron al nivel 10.

Aquí las estadísticas salen del **equipo**, la raza no aporta combate y los puntos por nivel van a los **árboles de talentos** (ver [Talentos](talentos.md)). No hay elecciones falsas ni desigualdades por fecha.

Ver P-12 y P-30 en [Preguntas abiertas](../00-vision/preguntas-abiertas.md).
