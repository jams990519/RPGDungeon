# Crítica del proyecto y de la hoja de ruta (0.32), con comparaciones

> **Módulo** [00 · Visión](README.md) · **Depende de:** [Revisión de código](revision-codigo-0.32.md), [Mapa de impacto](../01-plataforma/mapa-de-impacto.md), [Decisiones](decisiones.md) · **Alimenta a:** la [hoja de ruta](hoja-de-ruta.md), el [sistema de preguntas](sistema-de-preguntas.md) y la reforma de estadísticas (D-210, D-211) · **Estado:** informe del 11-oct-2026, pedido por el dueño

**Qué pidió el dueño.** "Una revisión de todo, criticar absolutamente todo, revisar lo que pueda estar afectando el progreso o lo que falte; buscar en foros y analíticas cómo funcionan juegos parecidos para comparar; y que cualquier estadística que pueda romper otra, explicar el motivo." Más un resumen detallado de todo lo que la IA necesita que le explique.

Este documento critica **el diseño y el plan**. La crítica del **código** está en la [revisión de código](revision-codigo-0.32.md).

---

## 1. El resumen para el desarrollador: corregir 6 datos antes de mandarlo

De 25 datos comprobados contra el código, 19 son exactos. Estos no:

| Bloque | Dice | Es | Por qué importa |
|---|---|---|---|
| 1/6 | "539 pruebas" | **540** (17 min 45 s medidos hoy) | Dato suelto |
| 1/6 | "234 decisiones" / "102 documentos" | **235** y **104** (con los dos informes de hoy) | Dato suelto |
| 2/6 | "Como mucho 6 botones por pantalla" | **8** en los centros de 🏕️ Campamento, 👤 Héroe, 🏰 Gestionar y ❓ Dudas (`HUB_BUTTONS`, D-192) | Un desarrollador que diseñe pantallas con el límite de 6 va a chocar con el código |
| 2/6 | Cada terreno "tiene de 4 a 6 recursos propios" | Cada **zona** suma **2 o 3** propios y queda con **4 a 6 de tierra en total**; el catálogo del terreno tiene 10 a 15 | Es la diferencia entre el catálogo y lo que trae una zona |
| 4/6 | "Oleadas de enemigos cada 7 días" | **3 por semana** (`raids.per_week: 3`, D-154): una cada **2 días y 8 horas** | Error grande: triplica la presión real sobre el campamento |
| ~~5/6~~ | ~~"Un día del mundo dura hasta 4 días reales"~~ | **Error mío, no del resumen (corregido el 11-oct-2026).** El resumen dice bien: **D-126 confirmada** dice "un día del mundo dura hasta 4 días reales", y P-86 lo recomienda (franjas de ~32 h para que todos vean las tres). Lo que está viejo es el **mapa de impacto §4.3**, que sigue diciendo 6 horas y hay que corregir. Reconfirmado por el dueño en D-239.9 | — |
| 6/6 | "python -m adapters.cli.play --fast" | **Se cae en Windows** (R-03: `UnicodeEncodeError`, cp1252 contra los emoji) | Es la primera cosa que el desarrollador va a correr, y falla |

Y uno que **no era error**: el día del mundo de 4 días reales está bien en el resumen (D-126); lo viejo es el mapa de impacto §4.3.

Dos más, de precisión: "~60 parches" son **57** entradas en `patches.yaml`, y el almacén tiene **unos 25 espacios**, no los cinco del ejemplo.

---

## 2. Lo que está frenando el progreso de verdad

### P-01 · El plan invierte el orden de lo que retiene
El resumen dice: 100 niveles, **2,5 años** al tope jugando toda la energía de cada día, y el combate en grupo, las bandas, el PvP y las temporadas van en "más adelante". La investigación de retención en juegos en línea dice lo contrario: los logros y el progreso retienen en las fases inicial y media, pero **cuando el jugador llega al tope, lo social es lo que más predice que se quede** ([Achievement and Friends, arXiv](https://arxiv.org/pdf/1702.08005)). Un juego que planea 2,5 años de progreso en solitario y deja lo social para después está construyendo la parte que no retiene primero.

**No digo que el plan esté mal; digo que el orden tiene un costo y hay que elegirlo a propósito.**

### P-02 · Las peleas comunes no tienen riesgo en ningún nivel
Medido con `tools/balance_report.py`: las 12 especializaciones ganan el **100 %** del nivel 1 al 100 en los tres escenarios, terminando con el 54-91 % de vida. Hoy el único riesgo del juego son el Guardián y la Noche de prueba. Un MMORPG donde pelear nunca puede salir mal convierte el combate en un botón de "cobrar".

### P-03 · Con un jugador, media docena de sistemas no se pueden probar
Gremios, partida de caza, encargos semanales del campamento, oleadas (las victorias necesarias se calculan sobre los **miembros activos**) y el cupo del gremio están escritos y probados con `n = 1`. No es un fallo del código: es que nadie sabe cómo se comportan con 10 ni con 40 personas. El castillo pide **40 a 50 jugadores** en el plan y hoy la muestra es 1.

### P-04 · El bucle de prueba del propio proyecto está roto en la máquina del dueño
La regla de antes de publicar es "correr las pruebas **y** arrancar el motor con un cliente". El cliente de consola se cae en Windows (R-03). O sea: el paso 2 de la lista de publicación no se puede cumplir en la máquina donde se trabaja. Una línea lo arregla.

---

## 3. Estadísticas que rompen otras estadísticas

Esto es lo que pidió explicado con el motivo. La reforma del punto 1 de la hoja de ruta (Fuerza, Agilidad, Intelecto, Vitalidad, Armadura + Crítico, Celeridad, Maestría, Versatilidad) **choca en seis sitios distintos** con lo que ya existe.

### E-01 · La armadura ya está contra el tope, y hoy acelera en vez de frenar
El código mitiga con `daño × (1 − armadura)` y corta en `gear.armor_cap = 60 %`. Medido con el mejor equipo de cada nivel:

| spec | nivel 1 | nivel 25 | nivel 50 | nivel 100 | % del tope al 100 |
|---|---|---|---|---|---|
| Guerrero · Tanque | 25,0 % | 41,8 % | 51,8 % | **55,0 %** | **92 %** |
| Druida · Tanque | 22,0 % | 38,8 % | 48,8 % | 51,0 % | 85 % |
| Sacerdote · Sanador | 12,0 % | 24,0 % | 29,0 % | 31,0 % | 52 % |
| Guerrero · DPS | 15,0 % | 27,0 % | 32,0 % | 35,0 % | 58 % |

Dos problemas, y van en direcciones opuestas:

1. **Antes del tope, la armadura acelera.** La vida efectiva es `vida / (1 − armadura)`. Subir del 0 al 10 % de armadura da **+11 %** de vida efectiva; subir del 50 al 60 % da **+25 %**. Cada punto vale más que el anterior, al revés de lo que hace cualquier juego moderno.
2. **En el tope vale exactamente cero.** Un tanque al 55 % tiene 5 puntos de margen. Si la reforma suma Armadura como estadística principal, el encantamiento 🛡️ Guarda (+1 o +2) y los puntos de Defensa (+0,2 por punto, hasta +10 al tope de 50), el tanque llega a 60 % y **tres fuentes distintas pasan a valer nada**.

**El diseño ya tenía la respuesta y no se implementó.** El mapa de impacto §4.1 dice que la mitigación es `def / (def + K)` con K = 60. Esa fórmula nunca llega al 100 %, cada punto vale menos en porcentaje y, sin embargo, **vale lo mismo en vida efectiva**: es lineal, no se rompe y no necesita tope ([Ask Mr. Robot](https://blog.askmrrobot.com/diminishing-returns-other-bfa-tank-formulas/), [MMO-Champion](https://www.mmo-champion.com/threads/1307030-Does-Armor-have-diminishing-returns)). Conclusión: **la reforma de estadísticas no puede empezar sin cambiar la fórmula de mitigación primero.**

### E-02 · Celeridad no tiene dónde existir en este combate
En Lost Realms se elige **una sola acción por ronda** (D-46) y la iniciativa es binaria: `iniciativa del héroe ≥ iniciativa del enemigo` decide solo quién golpea primero. Celeridad, tal como se entiende, significa más acciones o turnos más rápidos. En un sistema de una acción por ronda solo hay tres salidas y las tres son caras:

- **Dar energía de combate extra** → rompe la cadena: la energía es el freno que hace que el gastador cueste 6. Más energía = gastador en cada turno = las marcas dejan de importar.
- **Dar turnos extra** → es la estadística más rota de los juegos por turnos. En los foros de diseño es un clásico: la velocidad "o es la mejor inversión posible o no vale nada, sin término medio" ([ResetEra](https://www.resetera.com/threads/whats-a-turn-based-battle-system-where-the-speed-agility-stat-is-just-okay.810126/), [Unity Discussions](https://discussions.unity.com/t/turn-based-rpg-turn-order-when-you-use-haste/787490)).
- **Dejarla solo como iniciativa** → es un interruptor, no una estadística: pasado el umbral del enemigo, cada punto más vale cero.

**Recomendación: no meter Celeridad.** Si hace falta una cuarta secundaria, que sea algo que el sistema sí pueda pagar (por ejemplo, una que baje el costo de un botón de la cadena o que dé una marca extra cada N turnos).

### E-03 · Maestría contradice la regla madre, por definición
Maestría es, de diseño, la estadística que **diferencia** una especialización de otra: "se moldea alrededor de la identidad de la spec a la que sirve", y cada clase la convierte con un ratio distinto ([Maxroll](https://maxroll.gg/wow/resources/stat-diminishing-returns), [MMO-Champion](https://www.mmo-champion.com/threads/2631536-Mastery-fun-for-some-but-not-for-all)). La regla madre (D-232) dice lo contrario con las mismas palabras: las clases del mismo rol comparten los números y **solo cambia el sabor**. No se pueden tener las dos. Hay que elegir: o Maestría, o la regla madre.

### E-04 · Crítico y ataque se multiplican, y el equipo ya es exponencial
Hoy el daño es `ataque × poder × (0,9 a 1,1) × (1 − armadura)` y el crítico es un 10 % fijo con ×1,5. Si Crítico sube con el equipo **y** el ataque sube con el equipo, el daño crece como el **producto** de las dos, no como la suma. Eso es exactamente el motor del "stat squish" que obliga a achatar los números cada tanto: la progresión por equipo es exponencial por naturaleza ([foros de Blizzard](https://us.forums.blizzard.com/en/wow/t/why-is-blizzard-so-obsessed-with-stat-inflation/1191054)). Con 100 niveles y piezas cada 10, hay que fijar un **presupuesto de poder por nivel** antes de añadir secundarias, o el nivel 100 será ilegible.

### E-05 · Versatilidad cuenta dos veces
Versatilidad sube el daño y la curación **y** baja el daño recibido. Lo primero se solapa con el ataque y con el premio por marcas; lo segundo, con la armadura, que ya está al 92 % de su tope en los tanques. Una estadística que entra en dos presupuestos a la vez es la primera que se vuelve obligatoria para todos y la primera que hay que recortar.

### E-06 · Fuerza, Agilidad e Intelecto: hoy son el mismo número con tres nombres
El motor tiene **un** número de ofensiva, `attack`. Partirlo en tres principales obliga a decidir cuál usa cada clase, y ahí vuelve el choque con la regla madre: si las tres convierten igual a daño, son tres nombres para lo mismo (decoración); si convierten distinto, dos clases del mismo rol dejan de tener los mismos números. **Es la misma pregunta que E-03, por otra puerta.**

### E-07 · El punto 1 del plan se contradice consigo mismo
Dice "al subir de nivel se reparten pocos puntos, solo en las principales" y, dos líneas después, "con esto, subir de nivel deja de dar estadísticas por sí solo: la fuerza viene del equipo". Si el nivel reparte puntos de principales, el nivel **sí** da estadísticas. Hay que elegir cuál de las dos frases vale.

### E-08 · Ya hay cinco fuentes alimentando los mismos tres números
Antes de añadir nueve estadísticas, conviene ver lo que ya hay: `attack`, `hp` y `armor` reciben hoy aportes de **cinco** sitios distintos — la base de la clase y su `per_level`, la pasiva de talentos (hasta 50 puntos), las estadísticas del equipo, los beneficios de los oficios (D-111) y los encantamientos (D-115). Ninguno tiene presupuesto común: cada uno se decidió por su lado. La lección de TowerWars que está escrita en el diseño es "la ropa no contaba"; el riesgo de la reforma es el inverso: **que todo cuente dos veces**.

---

## 4. Cómo lo resuelven juegos parecidos

| Juego | Qué compara | Qué se puede copiar |
|---|---|---|
| **Torn** (texto, navegador, años de progreso) | El comparable más cercano: energía que se regenera, temporizadores, progreso que avanza con el chat cerrado | Es la prueba de que el modelo de energía + espera funciona a largo plazo en texto |
| **IdleOn, Queslar** (idle MMO) | Experiencias de varios años, aceptadas por el jugador | La escala de 2,5 años no es absurda **si** el juego es idle de verdad: avanzar sin estar presente |
| **World of Warcraft** | De dónde sale casi todo el vocabulario del diseño (oficios, rangos, secundarias, Maestría) | Lo que WoW tuvo que **añadir después**: rendimientos decrecientes en las secundarias (9.0) y achatar los números cada tanto. Las dos son deuda que se paga sí o sí |
| **Juegos por turnos en general** | La velocidad/Celeridad | El consenso es evitarla o encapsularla; ver E-02 |

---

## 5. Lo que necesito que me expliques

En rondas. Cada ronda depende de la anterior; si las contesto todas de golpe, las contesto mal.

### Ronda 1 — bloquean todo lo demás
1. ✅ **Contestada (11-oct-2026).** El documento existe: es la **revisión 30** del propio documento en Claude Docs, *Lost Realms — Estructura de clases y habilidades* (`c5182fff-c336-46ae-837f-538cb808925c`), con fecha 7-oct-2026. Leído entero. Lo de clases coincide con [combate-en-cadena.md](../04-combate/combate-en-cadena.md), **con dos diferencias**: el documento es anterior al Paladín (todavía dice Chamán, D-233 es del 9-oct, así que el repositorio es **más nuevo**) y lista **4 pendientes**, no 6 (el repositorio añadió la variedad y el orden del tanque). Lo que el documento trae y el repositorio no: la sección **Modo campamento** con los nodos y los territorios → registrada como **D-236**.
2. ✅ **Contestada.** Las 7 dudas están abajo, en §6, con lo que el propio documento y el dueño ya respondieron y lo que queda abierto.
3. **¿Maestría o regla madre?** (E-03, E-06). No caben las dos. Si quieres Maestría, la regla madre D-232 se cambia y hay que decirlo; si quieres la regla madre, la reforma lleva cuatro secundarias y no cinco.
4. **¿El nivel da estadísticas o no?** (E-07). Tu propio punto 1 dice las dos cosas.

### Ronda 2 — el sistema de habilidades (lo que quieres empezar)
5. **¿De dónde salen los puntos de mejora de habilidad?** Hoy no existen: solo hay 1 punto por nivel que se coloca solo. ¿Uno por nivel aparte del actual? ¿Cada X niveles? ¿Se compran con oficios?
6. **¿Qué mejora un punto?** ¿El poder de un botón, su costo de energía, las marcas que da, la duración de lo que deja?
7. **¿Se pueden deshacer?** Hoy hay un reinicio de talentos que cuesta monedas, para las clases viejas. Para las nuevas no hay nada.
8. **¿Cuántos botones acaba teniendo la barra?** Hoy son 4 + Defenderse + Mochila = 6, el tope de D-46. El modo híbrido mezcla habilidades: ¿sigue en 4 botones o sube?
9. **El híbrido del nivel 10: ¿cuántas habilidades del otro rol se mezclan?** (E-210: hoy `max_mixed: null`, apagado). Mi recomendación sigue siendo 1.

### Ronda 3 — lo que decide el tamaño del trabajo
10. **¿Los grupos entran ahora?** Sin grupos, el agro no existe y la mitad del diseño del tanque y del sanador es decorativo.
11. **¿La fórmula de mitigación se cambia a `def/(def+K)` antes de la reforma?** (E-01). Mi recomendación: sí, y es lo primero.
12. **Las civilizaciones del punto 2: ¿son el siguiente parche o van después de las estadísticas?** Son el sistema más grande de toda la hoja de ruta (territorio, nodos internos y externos, caravanas escoltadas, aldeanos que comen, un encargado que usa la energía de otros jugadores).
13. **"Un encargado puede usar la energía de los jugadores que se pongan disponibles para el reino":** ¿la energía se transfiere de verdad? Hoy la energía es personal y es el único freno del juego; que un jugador gaste la de otro es la puerta a las multicuentas.
14. ✅ **Contestada (D-239.9):** 4 días reales, como ya decía D-126. Hay que corregir el mapa de impacto §4.3.

---

## 6. Las 7 dudas del parche de mundo abierto (11-oct-2026)

Las dudas que el dueño traía del otro chat, con lo que **ya está respondido** por sus decisiones de hoy (D-236) y por el texto de su documento rev. 30, y lo que queda abierto.

| # | Duda | Estado |
|---|---|---|
| 1 | ¿El territorio se defiende a distancia desde el campamento cercano, o hay que mantener gente en el nodo para que cuente como controlado? | **Abierta.** D-236 dice que se domina al *rodear* el nodo con cuadrantes, no que haya que estar dentro. Falta decir si la presencia física cuenta |
| 2 | ¿Qué gana el dueño aparte del impuesto: recursos exclusivos, acceso a zonas, bonos de farmeo? | **Medio.** D-236 le da cerrar la zona (acceso exclusivo) y el peaje. Falta si además hay recursos o bonos propios |
| 3 | ¿Contra quién se pelea: PvP, PvE o ambos? | ✅ **Resuelta.** Los nodos y territorios son **PvP entre grupos** (D-236.4); el PvE sigue en las oleadas del campamento, que ya existen |
| 4 | ¿Qué cuesta mejorar el campamento y de dónde salen esos recursos? | **Medio.** El campamento ya tiene sus 20 mejoras con costos en el juego; lo que falta es el costo de **cada cuadrante** de expansión (D-236.6) |
| 5 | ¿Cómo se evita que un grupo gigante acapare todos los nodos? | **Abierta, y es la más importante.** Hoy no hay nada que lo frene: ni tope de nodos por grupo, ni costo creciente, ni cupo. Sin esto, el primer grupo grande se queda con el mapa |
| 6 | ¿Cómo farmea un jugador nuevo o sin grupo? | **Medio.** D-236.4 dice que solo *algunos* nodos quedan detrás de territorio y el resto es campo libre. Falta garantizar que lo que queda libre alcance |
| 7 | ¿Cada cuánto se puede atacar? ¿Hay cooldown o escudo después de una batalla? | **Medio.** La franja de 24 h del defensor (D-236.3) ya limita *cuándo*. Falta el enfriamiento o el escudo después de una batalla |

**Lo que el documento rev. 30 añade y conviene no perder:** "el nodo lo controlas y lo trabajas, pero vives aparte", lo que obliga a **proyectar fuerza a campo abierto**; el control de nodos es lo que le da sentido al tope de 5 objetivos (defender pide varios tanques y sanadores coordinados); y la cadena de cuadrantes entre el campamento y el nodo **es la línea de frente**, con una decisión geográfica real (plantar cerca cuesta menos expansión pero se pelea más; plantar lejos es más barato de terreno y obliga a sostener una cadena larga).

**Lo que esto implica y hay que decir en voz alta:** el parche de mundo abierto **depende del combate en grupo**. El propio documento lo dice ("defender un nodo exige varios tanques y sanadores coordinados"). Hoy no hay grupos, ni agro, ni peleas de más de uno contra uno. Así que el mundo abierto no es el parche siguiente: el parche siguiente es el que lo hace posible.

## De dónde sale

- **El documento del dueño**, *Lost Realms — Estructura de clases y habilidades*, revisión 30 (Claude Docs, 7-oct-2026): leído entero el 11-oct-2026.
- **El resumen de 6 mensajes** que el dueño preparó para un desarrollador (11-oct-2026), comprobado dato por dato contra `content/*.yaml` y el motor.
- **Las medidas** de `tools/balance_report.py` (armadura por nivel y escenario, victorias por rol) y `tools/sim.py`.
- **Las comparaciones** de los foros y análisis citados en §3 y §4: retención en juegos en línea (arXiv), rendimientos decrecientes de armadura y secundarias (Ask Mr. Robot, Maxroll, MMO-Champion), inflación de estadísticas (foros de Blizzard) y el problema de la velocidad en combate por turnos (ResetEra, Unity Discussions).
