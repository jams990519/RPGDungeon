# Caravanas y aldeanos

> **Módulo** [02 · Mundo](README.md) · **Depende de:** [Decisiones](../00-vision/decisiones.md) (D-196 a D-207), [Supervivencia del asentamiento](supervivencia-del-asentamiento.md) (despensa, población), [Fundación y cisma](fundacion-y-cisma.md) (campamentos, territorio y etapas), [Mapa infinito y viaje](mapa-infinito-y-viaje.md) (nodos y viaje) · **Alimenta a:** [Repaso de los oficios](../07-economia/oficios-repaso-2-oct.md) (granja, recolección y estructuras), [PvP](../06-contenido/pvp.md) (emboscadas), [Camino guiado](../03-personaje/camino-guiado.md) (el paso de aportar), [Red de sistemas](../00-vision/red-de-sistemas.md) · **Estado:** decidido en lo básico (D-196 a D-205, confirmadas por el dueño el 2-oct-2026); los números son provisionales (D-207 y las recomendaciones de E-161 a E-165 y E-169). **Solo diseño:** nada de esto está programado, salvo la energía de entrada y el minuto por cuadro, que entran en la 0.29.1.

**Qué pidió el dueño (2-oct-2026).** Que el asentamiento tenga su propia gente: **aldeanos** que comen, hacen funcionar las estructuras y salen en **caravanas** a recolectar en los nodos de afuera, siempre con jugadores que los escoltan. Que moverse cueste **tiempo** y trabajar cueste **energía**, con **una sola barra** para todo. Y que el jugador aprenda primero a sostenerse solo y después entre a la **capa Imperio**: el asentamiento y la civilización. El texto tal cual está en la [Entrevista de voz](../00-vision/entrevista-de-voz.md) ("2-oct-2026 · Decisiones de diseño (continuación)").

## De dónde sale

- ***Ashes of Creation***: las caravanas que llevan recursos entre nodos, que otros jugadores pueden atacar y que hay que escoltar; los nodos que crecen y su zona de influencia.
- ***Albion Online***: mover recursos es lo arriesgado; las emboscadas en zonas peligrosas, y quien gana se lleva parte de la carga.
- ***Black Desert Online***: los trabajadores que recolectan en los nodos por el jugador, y que hay que alimentar para que sigan trabajando.
- ***Banished*** y ***Frostpunk***: una población que come cada día, que con hambre deja de trabajar y que se va si la hambruna dura.

---

## 1. Nodos internos y externos (D-201)

| | 🏠 Nodo interno | 🌲 Nodo externo |
|---|---|---|
| **Dónde está** | Dentro del territorio de la civilización (el asentamiento) | Fuera del territorio |
| **Quién lo farmea** | Los miembros, directamente, cada uno con su energía | Nadie directamente: **requiere caravana** (§2) |
| **Mejoras** | Se mejora directamente | Las mejoras de nodo aplican aquí |

- **Hoy en el juego** cualquiera que llega recolecta en cualquier nodo (D-184). Esto cambia cuando se programen las caravanas; hasta entonces todo sigue igual.
- Quién mejora los nodos (cada recolector los de su recurso) sigue abierto en E-146.

## 2. Caravanas: el farmeo grupal (D-202)

**Qué es.** La civilización envía **aldeanos** (la mano de obra que recolecta) a un **nodo externo**, y los jugadores **escoltan la caravana físicamente durante todo el trayecto**: van con ella, ida y vuelta.

**Cómo funciona.**

1. **Requisito:** un campamento mejorado. Las caravanas se abren desde la **2.ª o 3.ª mejora del asentamiento**.
2. **Se arma:** el encargado (§3) o un miembro elige el nodo externo, el tamaño de la caravana y los escoltas.
3. **Se paga la energía de entrada (D-196):** el costo total se reparte **por igual entre los escoltas**, y cada uno tiene que tener su parte antes de salir. *Propuesta:* si a uno no le alcanza, sale sin él solo si igual quedan los escoltas mínimos.
4. **Viaja:** al ritmo del viaje normal, 1 minuto por cuadro (D-197), ida y vuelta.
5. **Recolecta y vuelve:** los aldeanos recolectan en el nodo y la carga llega a la despensa o al almacén del asentamiento.

**Tamaños.** Un nodo se puede traer en **un solo viaje grande** o en **varios viajes más chicos**. A más tamaño (más capacidad y carga), más **escoltas mínimos obligatorios**. Números recomendados (E-165, provisionales):

| Tamaño | Multiplica el costo | Escoltas mínimos | Carga (propuesta) |
|---|---|---|---|
| 🐴 Chica | × 1 | 2 | Un tercio de lo que trae la grande |
| 🐂 Mediana | × 2 | 4 | Dos tercios |
| 🐘 Grande | × 3 | 6 | Todo |

**Costo de energía.** La caravana **sí** cuesta energía, aunque moverse solo no la cueste, porque compromete el tiempo y la energía de los escoltas. Sube con el **tamaño del nodo** y con la **distancia**. Fórmula recomendada (E-165): **(10 ⚡ + 2 ⚡ por cuadro de distancia) × el tamaño**, repartido por igual entre los escoltas.

| Ejemplo | Costo total | Escoltas | Cada uno |
|---|---|---|---|
| Chica, a 5 cuadros | (10 + 10) × 1 = 20 ⚡ | 4 | 5 ⚡ (el ejemplo del dueño) |
| Mediana, a 5 cuadros | (10 + 10) × 2 = 40 ⚡ | 4 | 10 ⚡ |
| Grande, a 10 cuadros | (10 + 20) × 3 = 90 ⚡ | 6 | 15 ⚡ |

- **Un viaje grande o varios chicos** cuestan la misma energía en total; el grande ahorra tiempo de viaje y emboscadas, pero pide más escoltas a la vez y, si cae, se pierde más.
- **Cuántas a la vez:** suben con las etapas, porque a más etapas caben más jugadores disponibles para escoltar. El número exacto se fija con las etapas (D-200).

**Emboscadas.** Una caravana puede ser emboscada por **monstruos (PvE)** y por **otros jugadores (PvP)**, cuando haya PvP (E-76). Los escoltas pelean para defenderla.

**Si cae.**
- El atacante se lleva **parte de la carga**.
- Los aldeanos **no mueren**: vuelven al asentamiento, pero **pierden gran parte del material**.
- Al dueño de la caravana le llega el mensaje: *"⚠️ La caravana fue atacada. Los aldeanos lograron volver, pero se perdió gran parte de lo recolectado."*
- Cuánto se lleva el atacante y cuánto vuelve se ajusta al programarlo.

## 3. Encargado y jugadores disponibles para el reino (D-203)

- El jugador puede ponerse **"disponible para el reino"** en cierto momento.
- Un **encargado** (de caravanas, de agricultura…) **gasta la energía de los jugadores disponibles**, dirigiéndola a tareas y destinos concretos: una caravana, un nodo interno, una estructura.
- **Pendiente (E-163).** Recomendado: el encargado es un cargo que nombra el fundador del asentamiento (en el castillo se vota, D-157), uno por tarea; el jugador disponible se retira cuando quiera, salvo en una caravana o tarea ya en marcha, porque su energía ya está comprometida.

## 4. Energía y tiempo (D-196, D-197)

| Regla | Qué quiere decir | En el juego |
|---|---|---|
| **Una sola barra** | La misma energía para recolectar, combatir y escoltar: no se pueden hacer varias cosas a la vez | Sí: la energía de siempre (máximo 50) |
| **Se paga de entrada** | Para empezar una acción hay que tener toda la energía que pide; si no alcanza, no empieza; nadie queda a medias | 0.29.1, en las mazmorras (la chica pide antes de cada pelea la energía de todas las que le quedan; cada piso de la profunda, la de todas sus peleas). Los lotes, fabricar y cazar ya solo ofrecían lo que tu energía cubre |
| **Moverse cuesta tiempo** | 1 minuto real por cuadro (10 cuadros = 10 minutos), sin energía | 0.29.1 (antes, 2, 2, 3, 3, 4… minutos por zona, D-78) |
| **Trabajar cuesta energía** | Farmear según el tamaño del nodo; la caravana según su tamaño y la distancia (§2) | Hoy cada vuelta cuesta 1 ⚡; los nodos todavía no tienen tamaños. Recomendado (E-165): chico 1 ⚡, mediano 2, grande 3, que rinden más |

- **Escoltar es trabajar:** el escolta paga su parte de energía y además pone su tiempo, porque viaja con la caravana.
- **Mientras viajas (E-162).** Recomendado, como hoy: puedes mirar todo (mochila, héroe, mapa, dudas), pero no trabajar hasta llegar.
- **El minuto por cuadro (E-161).** Recomendado: fijo por ahora; más adelante, las monturas de la Ganadería lo bajan a 30 segundos, nunca a cero.

## 5. Aldeanos y comida (D-205; números en D-207, provisional)

**Lo que decidió el dueño (D-205).**
- Los **aldeanos PNJ comen**. **Los jugadores no cuentan como población que come.**
- La **granja produce comida sola** según la etapa (D-195).
- Los aldeanos **hacen funcionar las estructuras** y **forman las caravanas**.

**Los números (D-207, propuesta de Claude, para ajustar en la beta).** Los nombres de las etapas siguen los niveles de hoy hasta que D-200 los fije.

| Nivel | Etapa de hoy | Aldeanos (máximo) | Comen por día | La granja da por día | Falta (lo ponen los jugadores) |
|---|---|---|---|---|---|
| 1 | Campamento | 3 | 3 | 2 | 1 |
| 3 | Aldea | 9 | 9 | 5 | 4 |
| 5 | Pueblo | 15 | 15 | 8 | 7 |
| 7 | Ciudad | 21 | 21 | 11 | 10 |
| 9 | Castillo | 27 | 27 | 14 | 13 |

- **Cada aldeano come 1 ración por día real**, la misma ración de la despensa de hoy.
- **Aldeanos:** 3 por nivel del asentamiento. Llega **1 nuevo por día** mientras haya lugar y al menos **3 días de comida** guardada.
- **La granja** da cerca de **la mitad** de lo que come la población completa, un poco más al principio: ⌈1,5 × nivel⌉ raciones por día.
- **El resto lo ponen los jugadores**: 🌾 Agricultura, 🐄 Ganadería, cocineros, cazadores y pescadores (D-125). Así crecer sigue pidiendo oficios.

**Hambre (déficit).**
- Los aldeanos **nunca mueren**.
- Los que no comen ese día **no trabajan**: las estructuras y las caravanas van más lento, en proporción.
- En **hambruna**, el asentamiento **no crece** (no llegan aldeanos nuevos y no se puede agrandar) y **nunca pierde niveles**, como hoy.
- Tras **3 días seguidos de hambruna**, se va **1 aldeano por día**, hasta un mínimo de 2.

**Qué cambia frente a hoy.** Hoy comen los **miembros activos** del campamento desde el nivel 3 (D-93, [Supervivencia del asentamiento](supervivencia-del-asentamiento.md) §0.4). Con D-205 comen los aldeanos, no los jugadores. Se aplica cuando se programen las etapas del asentamiento; hasta entonces la despensa sigue igual. Los estados de la despensa (🟢 abundancia a 🔴 hambruna) seguirían igual, contados con los aldeanos.

## 6. Cómo se conecta

| Sistema | Consume | Produce |
|---|---|---|
| **🛒 Caravanas** | Energía de los escoltas (repartida por igual), aldeanos del asentamiento, tiempo de viaje, un campamento mejorado | Recursos de los nodos externos para el asentamiento; trabajo en común para los disponibles; riesgo de emboscada (PvE y PvP) y botín para quien la asalta |
| **🧑‍🌾 Aldeanos** | Comida de la granja y la que aportan los jugadores; lugar en el asentamiento | Trabajo: hacen funcionar las estructuras y forman las caravanas |
| **🌾 Granja** | La etapa del asentamiento | Comida para los aldeanos (cerca de la mitad de lo que comen) |

Las filas completas están en la [Red de sistemas](../00-vision/red-de-sistemas.md) §3.

## 7. Preguntas para el dueño

En el [Sistema de preguntas](../00-vision/sistema-de-preguntas.md), tanda 1, bloque A3:

- **E-161 (P-160):** el minuto por cuadro, ¿fijo o se acelera?
- **E-162 (P-161):** ¿qué puedes hacer mientras viajas?
- **E-163 (P-162):** el cargo del encargado y si el disponible puede retirarse.
- **E-164 (P-163):** el premio por terminar el tutorial.
- **E-165 (P-164):** la energía por tamaño de nodo y por tamaño y distancia de caravana.
- **E-169 (P-168):** los números de la comida de los aldeanos (D-207).
- Y en el bloque B, **E-58 (P-81):** cuántos jugadores por asentamiento en cada etapa (D-200).
