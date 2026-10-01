# Balance: que todas las clases valgan lo mismo, y que se pueda medir

> **Módulo** [03 · Personaje](README.md) · **Condiciona a:** [Clases](clases-y-especializaciones.md), [Equipamiento](equipamiento.md), [Combate](../04-combate/README.md), [PvP](../06-contenido/pvp.md) · **Estado:** propuesta

Pediste corregir los problemas de calibración de WoW y que las clases queden igualadas. Este documento dice **qué está roto**, **qué reglas lo impiden aquí** y **cómo se mide** que las reglas se cumplan.

> **Regla del dueño (D-49):** el sistema de clases tiene que estar **igualado**. Lo que hace la diferencia entre un jugador y otro son **sus oficios y el conocimiento extra que tenga**, no la clase que eligió (ver §5).
>
> **Regla del dueño (D-50):** cada clase tiene varios roles en sus specs (Ataque, Defensa, Curación y Soporte; ver [Clases](clases-y-especializaciones.md)) y todos pueden jugar solos. Cuesta distinto según el rol, pero siempre es posible (ver la regla 4).

---

## 1. Qué está roto en WoW

| # | Problema | Evidencia | Qué hacemos aquí |
|---|---|---|---|
| 1 | **Specs que dominan el meta** | Temporada 1 de *Midnight*: Reprensión y Mago de Escarcha arriba en M+; Mago de Fuego al fondo | Presupuesto de poder por spec, simulador y objetivos numéricos (§2 y §3) |
| 2 | **Tanques desiguales** | Temporada 1 de *Midnight*: en llaves altas dominó el Maestro Cervecero y el resto casi no aparecía | Mismos objetivos de mitigación y autonomía para las 11 specs de Defensa |
| 3 | **"Impuesto híbrido"** | Durante años las clases puras pegaron más por diseño; en *Icecrown Citadel* el Sacerdote Sombra rendía un 6 % menos a propósito | La unidad de balance es la **spec**, no la clase: mismo rol, mismo objetivo. Además, aquí todas las clases son híbridas (3 roles cada una, 4 el Druida) |
| 4 | **Utilidades obligatorias** | Ansia de Sangre fue exclusiva del Chamán hasta 2010, y hoy los grupos siguen buscando "lust" y resurrección en combate | Cada utilidad clave la tienen 4 o más clases **y** un consumible fabricado. Ninguna clase es obligatoria |
| 5 | **Soporte que se apila** | El Evocador de Aumentación apilado permitió matar un jefe Mítico en unos 30 s. Blizzard admitió que "su contribución es demasiado impactante" | Los efectos de Soporte de la **misma familia** no se suman sobre el mismo objetivo: queda el más fuerte (regla 5) |
| 6 | **Control encadenado en PvP** | El sistema de rendimientos decrecientes se reescribió en 12.0 para dar inmunidad tras 2 aplicaciones | **Firmeza** desde el primer día (ver [Ronda y acciones](../04-combate/ronda-y-acciones.md)) |
| 7 | **Sanadores inmortales o inútiles en arena** | WoW baja la curación a medida que avanza la partida ("dampening") | Amortiguación de curación por ronda en PvP |
| 8 | **Inflación de números** | En *Shadowlands* hubo que comprimirlo todo (nivel 120 → 50) porque el daño iba camino a los miles de millones | Números chicos desde el diseño (§4) |
| 9 | **Poder prestado** | Artefactos, Azerita, Pactos: poder que se da en una expansión y se quita en la siguiente. Blizzard reconoció el problema | Todo sistema de poder es permanente; lo temporal solo existe en ligas opcionales |
| 10 | **Raciales de combate** | Humano, Orco y No-muerto en PvP (ver [Creación](creacion-de-personaje.md)) | Ninguna racial toca el combate |
| 11 | **Suerte con el botín** | Semanas sin el objeto que necesitas; el Gran Tesoro semanal nació para paliarlo | Protección contra mala racha y recompensas deterministas de jefe (ver [Equipamiento](equipamiento.md)) |
| 12 | **Apilar clases en banda** | *Sunwell* (TBC) y los Evocadores de Aumentación | Aportes de grupo que no se suman y jefes diseñados para composiciones libres |
| 13 | **Botoneras enormes** | Rotaciones de más de 20 habilidades, que *Midnight* tuvo que podar | **6 botones por combate** (D-46): Atacar, 3 habilidades, Huir y Mochila. Nunca más |

## 2. Las reglas que no se negocian

1. **La spec es la unidad de balance, y se compara dentro de su rol.** Hay cuatro roles: ⚔ Ataque (15 specs), 🛡 Defensa (11), ✚ Curación (8) y ✦ Soporte (12) (ver [Clases](clases-y-especializaciones.md)). Se compara Protección con Sangre, Bestias y Legión, no Guerrero con Caballero de la Muerte. Entre roles distintos no se comparan números sueltos: se compara el grupo completo (§3).

2. **Presupuesto de poder de 100 puntos por spec**, repartido en seis ejes:

   | Eje | Qué mide |
   |---|---|
   | Daño sostenido | Daño por ronda contra un objetivo en una pelea larga |
   | Ráfaga | Daño en una ventana corta (3 rondas) |
   | Supervivencia | Mitigación, autocuración, defensivos |
   | Control | Aturdir, silenciar, interrumpir, retrasar iniciativa |
   | Utilidad de grupo | Aportes, curas externas, escudos, potenciar aliados, debilitar enemigos, resurrección, disipar |
   | Autonomía | Qué tan bien juega en solitario (misiones, Profundidades, expediciones) |

   - Cada spec suma 100 ± 3.
   - Ningún eje pasa de 35 ni baja de 5.
   - El perfil de cada spec se publica en la guía del juego como un gráfico de radar: el jugador sabe qué eligió.
   - El reparto cambia según el rol, pero la suma es la misma para todos:

   | Rol | Ejes altos | Ejes bajos |
   |---|---|---|
   | ⚔ Ataque | Daño sostenido, Ráfaga, Autonomía | Utilidad de grupo |
   | 🛡 Defensa | Supervivencia, Control | Ráfaga, Autonomía |
   | ✚ Curación | Utilidad de grupo (curas), Supervivencia | Daño, Autonomía |
   | ✦ Soporte | Utilidad de grupo (potenciar y debilitar), Control | Ráfaga |

3. **Kit mínimo garantizado.** Toda spec tiene en su repertorio una interrupción (o algo equivalente), un defensivo mayor, un defensivo menor o autocuración, un control, una forma de reposicionarse o escapar, y un aporte de grupo. En WoW hubo clases que pasaron expansiones enteras sin interrupción o sin defensivos. Con la barra de 6 (D-46) no todo cabe a la vez: elegir qué llevar es parte del juego, pero toda clase tiene al menos una habilidad que **responde a los avisos** (bloquear, esquivar, escudo, cambiar de fila), y la configuración inicial de cada spec la trae puesta.

4. **Autonomía por rol (D-50).** Toda spec puede hacer sola el contenido en solitario (misiones, encargos, Profundidades normales). Lo que cambia es **cuánto tarda**, medido contra la mediana de las specs de Ataque en los mismos escenarios:

   | Rol | Tiempo para terminar (objetivo) | Margen aceptado | Cómo se sostiene solo |
   |---|---|---|---|
   | ⚔ Ataque | 1× (la referencia) | 0,9× a 1,1× | Mata rápido; se cubre con su respuesta al aviso y el cinturón |
   | ✦ Soporte | ~1,25× (algo más lento) | 1,15× a 1,35× | Sus potenciaciones también cuentan para él y su compañero |
   | 🛡 Defensa | ~1,5× | 1,4× a 1,6× | Casi no cae; el modo en solitario devuelve parte de lo que bloquea como daño |
   | ✚ Curación | ~2× (el doble) | 1,8× a 2,2× | Se cura a sí mismo; el modo en solitario pasa parte de la curación a daño |

   - **Siempre posible:** con juego básico (las Tácticas por defecto), toda spec gana al menos el 90 % de las peleas del contenido en solitario de su tramo. Un rol puede tardar más; nunca puede quedarse atascado.
   - **Modo en solitario:** se enciende solo cuando no hay otro jugador en la pelea (con compañero PNJ o sin él) y se apaga en cuanto entra uno. No existe en grupo ni en PvP. Es crítico en Telegram, donde mucha gente juega sola a la hora que puede.
   - **La compensación está en el grupo:** Defensa y Curación son los roles más buscados, y el buscador les da una recompensa extra cuando faltan (la *Llamada a las armas*, ver [Clases](clases-y-especializaciones.md)).
   - Como toda clase tiene una spec de Ataque y cambiar de spec es gratis en un asentamiento, **ninguna clase** queda atada a un rol lento en solitario.

5. **Aportes de grupo equivalentes y no acumulables.** Cada clase aporta un efecto de grupo de valor parecido (alrededor del 3 % del rendimiento del grupo), y dos del mismo tipo no se suman.
   - **Los efectos de Soporte van aparte**, porque son el trabajo de un rol entero, y siguen la **regla de familias**: cada efecto pertenece a una familia (Potenciar, Proteger, Debilitar, Controlar o Reabastecer) y dos de la misma familia **no se suman sobre el mismo objetivo**: queda el más fuerte.
   - Así, dos Evocadores de Aumentación no pueden apilarse sobre el mismo atacante (el problema 5 de WoW), pero un Pícaro Forajido (Potenciar) y un Brujo de Aflicción (Debilitar) sí trabajan juntos.
   - No hay tope de soportes por grupo: el simulador comprueba que un grupo con 3 soportes rinde menos que uno equilibrado, porque el soporte multiplica un daño que tiene que existir.

6. **Utilidades clave compartidas, más un consumible fabricado:**
   - **Clamor** (el "lust"): +30 % de iniciativa y enfriamientos al doble de velocidad durante 3 rondas, una vez por pelea. Lo tienen Chamán, Mago, Cazador, Evocador y Bardo, y también los Tambores de Guerra (Peletería).
   - **Resurrección en combate** (cargas compartidas por pelea): Caballero de la Muerte, Druida, Brujo, Paladín y Nigromante, más las Sales de Reanimación (Medicina) y el Desfibrilador (Ingeniería).
   - **Disipar magia, curar veneno, curar enfermedad**: cada una la tienen al menos 4 clases.

7. **Estadísticas secundarias aplanadas.** Para ninguna spec una secundaria puede valer más de 1,3 veces otra, y todas tienen rendimientos decrecientes suaves. Se acaba el "esta spec solo quiere celeridad".

8. **Mismo escalado con el equipo.** Todas las specs escalan igual con el Poder de Objeto. El simulador lo comprueba en cada tramo: ninguna spec puede "despertar" en el tramo 8 ni morirse en el 3.

9. **Dificultad declarada, techo parejo.** Cada spec lleva una etiqueta de dificultad (★ a ★★★), y el simulador mide dos cosas:
   - **Juego básico**, con las [Tácticas](../04-combate/avisos-y-tacticas.md) automáticas por defecto: todas las specs a ±10 % de la mediana de su rol.
   - **Juego óptimo**, con el mejor plan posible: todas a ±3 % de la mediana de su rol.

   Así una spec fácil no domina y una difícil no queda inútil. En un juego por turnos no hay velocidad de dedos: la dificultad es **planificar**.

10. **Sin poder racial, sin poder prestado, sin clase obligatoria.** Los jefes se diseñan para composiciones libres; ninguna pelea pide "dos Chamanes".

## 3. Cómo se mide

**Simulador de combate** (el equivalente a SimulationCraft, módulo M21). Corre cada spec contra un conjunto fijo de escenarios en cada tramo de equipo: un objetivo, varios objetivos, pelea con cambios de fila, pelea con fases, y PvP 1v1 contra cada una de las otras specs. Además corre:
- **Grupos de referencia** (1 🛡 + 1 ✚ + 3 de ⚔ o ✦, en todas las combinaciones), porque Defensa, Curación y Soporte solo se entienden en grupo.
- **Escenarios en solitario** (misión, encargo, Profundidades normales) para medir la autonomía de la regla 4.

Corre con cada cambio de balance y **antes** de publicarlo.

**Objetivos numéricos.** Cada métrica compara specs del **mismo rol**; las dos filas que cruzan roles lo dicen.

| Métrica | Specs que se comparan | Objetivo |
|---|---|---|
| Daño sostenido (juego óptimo) | ⚔ Ataque | A ±3 % de la mediana de Ataque |
| Ráfaga | ⚔ Ataque | ±5 % |
| Mitigación efectiva: daño que evita al grupo, contando la mascota, el demonio o los esqueletos | 🛡 Defensa | ±4 % |
| Curación efectiva, sin contar la que sobra | ✚ Curación | ±4 % |
| Aumento del grupo: cuánto más rinde el grupo con esa spec que con un Ataque medio, sumando su propio daño | ✦ Soporte | ±4 % de la mediana de Soporte |
| Daño propio del Soporte | ✦ Soporte | Entre el 60 y el 75 % de la mediana de Ataque |
| Soporte frente a Ataque (cruza roles) | ✦ y ⚔ | Un grupo con 2 de Ataque + 1 de Soporte rinde lo mismo que con 3 de Ataque (±3 %); con 3 de Soporte, rinde menos |
| Tiempo en solitario (cruza roles) | Todas | El objetivo de su rol en la regla 4, y a ±10 % de la mediana de su rol |
| Victorias en solitario (juego básico) | Todas | 90 % o más en el contenido en solitario de su tramo |
| Victorias por spec en arena clasificada | Todas | 47-53 % |
| Popularidad en contenido alto (M+ 15 o más, top 500 de arena) | Todas, dentro de su rol | Ninguna spec por encima del doble del promedio de su rol |

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

## 5. La diferencia la hacen los oficios y el conocimiento

Si todas las clases rinden lo mismo, ¿qué separa a un jugador bueno de uno nuevo? Lo que **sabe** y lo que **sabe hacer**:

| Fuente de ventaja | Cómo ayuda en combate y en el mundo | Tope para que no se desboque |
|---|---|---|
| **Conocimiento del bestiario** | Ver la pista de los avisos, las debilidades y las partes rompibles de cada monstruo y jefe (ver [Avisos](../04-combate/avisos-y-tacticas.md)) | La pista ayuda a decidir, no decide por ti |
| **Oficios propios** | Fabricarte o mandarte a hacer mejor equipo; pociones, remedios y comidas de más calidad; curarte heridas tú mismo con Medicina | El equipo tiene techo por tramo; la toxicidad limita las pociones |
| **Investigación** | Recetas, técnicas y mejoras que otros todavía no tienen (ver [Investigaciones](../06-contenido/investigaciones.md)) | El conocimiento se difunde con el tiempo; patentes que vencen |
| **Conocimiento del mundo** | Saber dónde están las vetas buenas, los yacimientos únicos, los atajos y los secretos | Las vetas se mueven; los secretos se comparten |
| **Maestrías y rasgos** | Pequeños bonos por constancia (ver [Progresión](progresion.md), [Rasgos](../05-salud/rasgos-adquiridos.md)) | Nunca más del 5 % en combate |
| **Habilidad del jugador** | Leer los avisos, planificar las rondas, preparar el cinturón de la mochila | Ninguno: es lo que se quiere premiar |

**Lo que nunca hace la diferencia:** la clase elegida, la raza, ni el dinero real (ver [Monetización](../07-economia/monetizacion.md)).

## 6. Lección de TowerWars: nada de puntos de estadística sueltos

TowerWars reparte un punto de personaje por nivel en ataque, defensa, vida o maná. Su propio documento de estado reconoce dos problemas:
- +1 de vida no es una elección real al lado de +1 de ataque: uno mueve el 1 % y el otro el 20 %.
- Después de un reinicio, los jugadores recibieron repartos distintos según la fecha en que llegaron al nivel 10.

Aquí las estadísticas salen del **equipo**, la raza no aporta combate y los puntos por nivel van a los **árboles de talentos** (ver [Talentos](talentos.md)). No hay elecciones falsas ni desigualdades por fecha.

Ver P-12 y P-30 en [Preguntas abiertas](../00-vision/preguntas-abiertas.md).
