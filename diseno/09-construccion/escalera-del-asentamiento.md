# Escalera del asentamiento: de 5 a 200 jugadores

> **Módulo** [09 · Construcción](README.md) · **Depende de:** [Fundación y cisma](../02-mundo/fundacion-y-cisma.md), [Supervivencia del asentamiento](../02-mundo/supervivencia-del-asentamiento.md), [Gremios y social](../08-social/gremios-y-social.md), [Casa propia](casa-propia.md) · **Alimenta a:** [Defensa y protecciones](defensa-y-protecciones.md), [PvP](../06-contenido/pvp.md), [Economía](../07-economia/economia.md) · **Estado:** confirmado por el dueño en lo grande (D-252, D-253 y D-254, 17-oct-2026); los números son propuesta de Claude, a medir en la beta; **nada de esto está en el código todavía**

El dueño pidió (17-oct) armar los grupos, gremios y castillos para que "empecemos con 5 jugadores y a partir de ahí vaya creciendo incluso hasta 200 jugadores". Claude le mostró tres formas; eligió **A + B** con las cuatro recomendaciones, sumó la regla de la fogata y la idea de la muralla que cosecha sola.

---

## 1. Lo decidido

| Decisión | Qué dice |
|---|---|
| **D-252** | El grupo **nace al construir** uno mismo. En la fogata donde se sale **no se crea grupo**. |
| **D-253.1** | **Forma A + B:** un solo cupo por etapa, y la **escuadra de 5** como unidad para organizarse. El castillo llega a 50 y el reino a 200. Las alianzas de castillos (Forma C) quedan para más adelante. |
| **D-253.2** | **Castillo:** 40 activos con cupo de 50 (D-122). |
| **D-253.3** | **Un miembro que no juega** libera su lugar a los **30 días** sin jugar. |
| **D-253.4** | **Aceptan gente** el líder y los oficiales. |
| **D-254** | La **muralla** crece con el asentamiento, y la tierra que encierra **cosecha sola** una parte de sus recursos. El porcentaje sigue abierto (P-227). |

## 2. La escalera

Un solo número dice cuánta gente cabe en cada etapa: se acaba el doble cupo de hoy (el del campamento y el del gremio, donde gana el mayor).

| Etapa | Cupo | Cómo se sube | Qué abre | Zonas de muralla (P-229) |
|---|---|---|---|---|
| 1 · Casa | 5 | **Construir tu casa** tú mismo (nace el grupo, D-252) | Inventario compartido, misiones de grupo, despensa chica, primeras oleadas | 1 |
| 2 · Campamento | 10 | 3 mejoras y la 1.ª misión de grupo | El grupo pasa a gremio, 🎓 Academia (D-246) | 3 |
| 3 · Aldea | 15 | 8 activos, 6 mejoras y la 2.ª misión | Aldeanos y caravanas (D-205, D-202) | 5 |
| 4 · Pueblo | 25 | 12 activos, 10 mejoras y 3 oleadas ganadas | Territorio por cuadrantes (D-236), oficiales | 9 |
| 5 · Ciudad | 40 | 20 activos, 15 mejoras y la 4.ª misión | Mercado, segundo nodo | 15 |
| 6 · Castillo | 50 | **40 activos**, Noche de prueba con 10 vencedores distintos y 5 oleadas crecientes ganadas en su mayoría (D-122) | Peaje, guerra por nodos (D-236) | 25 |
| 7 · Fortaleza | 80 | Sostener el castillo 2 semanas, 60 activos | Mejoras de nivel alto | 35 |
| 8 · Ciudadela | 120 | 90 activos y una oleada mayor | Monstruo de asedio | 49 |
| 9 · Capital | 160 | 120 activos | Más territorio | 64 |
| 10 · Reino | **200** | 150 activos y un mes sostenido | La mejora más grande (la monarquía de D-155) | 81 |

- **Activo** es haber jugado en la última semana (hoy la despensa cuenta 24 horas; para subir de etapa conviene mirar la semana, para que no dependa de un día).
- **La Casa y el Grupo son la misma etapa** (D-252): la propuesta que vio el dueño tenía 11 etapas, con "Grupo" antes de "Casa".
- **Lo que no se tira:** los niveles, las 20 mejoras y las oleadas de hoy siguen. Las etapas se estiran hacia arriba, y hacen falta mejoras nuevas para las etapas 7 a 10 (hoy se acaban en el nivel 8).

## 3. Escuadras y cargos (Forma B)

- **La escuadra:** el grupo de 5 de D-246 pasa a ser una escuadra dentro del gremio. Cada etapa abre lugar para más escuadras: 1, 2, 3, 5 y 8 hasta la ciudad, **10 en el castillo** (50 personas) y **40 en el reino** (200).
- **Cargos:**
  - el **líder** (quien construyó, D-252);
  - un **oficial** cada 2 a 4 escuadras, que nombra el líder;
  - un **jefe** por escuadra, que eligen sus 5.
- **Quién acepta gente:** el líder y los oficiales (D-253.4). El jefe de escuadra acomoda a los nuevos en su escuadra, pero no los acepta.
- **Las tareas se reparten por escuadra:**
  - la Noche de prueba se gana con "N escuadras que vencen" (por ejemplo, 8 de 10 en el castillo);
  - cada escuadra defiende un tramo de la muralla o un nodo;
  - las misiones de grupo son de una escuadra.
- **Encaja con el combate:** una habilidad de área alcanza a 5 objetivos (`chain.target_cap: 5`), justo una escuadra (D-246.4).

## 4. Quien deja de jugar

- **A los 30 días sin jugar**, el miembro deja de ocupar lugar: sale del gremio y su lugar queda libre (D-253.3).
- **Puede volver a pedir entrar,** y lo acepta el líder o un oficial.
- **Propuesta de Claude:** avisarle a los 25 días ("en 5 días liberas tu lugar en …"), y que lo que aportó a las obras quede en el asentamiento.
- **Cambia la regla 10 del servicio**, que hoy dice "el gremio nunca saca a nadie".

## 5. La muralla y la tierra que cosecha sola (D-254)

### 5.1 Lo que pidió el dueño

"Agrega la cantidad de muralla que pueden ampliar de acuerdo al tamaño del campamento, o sea, territorio tomado te genera farmeo del 40 % de los recursos de la zona o quizás menos, en automático, fomentando a que tomen todo el territorio alrededor."

### 5.2 Cómo se arma

- **La muralla es el borde del territorio.** Cada etapa deja cerrar más zonas (columna de la tabla del §2). Crece en anillos alrededor del centro: 1, 3 × 3 = 9, 5 × 5 = 25, 7 × 7 = 49, 9 × 9 = 81. Queda más o menos **una zona cada 2 o 3 jugadores** de cupo.
- **Cerrar una zona nueva cuesta:**
  - materiales, y más cuanto más lejos del centro (D-239.4);
  - mantenimiento por zona (D-239.5);
  - y la muralla hay que defenderla: las oleadas le pegan y una escuadra cuida cada tramo.

  Así, tomar todo lo de alrededor conviene, pero no sale gratis.
- **Cada zona cerrada cosecha sola** una parte de lo que la zona vuelve a crecer cada día, sin gastar energía.

### 5.3 Cuánto da: los números de hoy

| Dato | Valor | De dónde sale |
|---|---|---|
| Lo que junta un jugador por día recolectando | unas **80 unidades** (40 de energía, de 1 a 3 por vuelta en zonas bajas) | `gather`, `energy.per_day` |
| Lo que vuelve a crecer cada recurso de una zona | unas **24 unidades por día** | `stock.regen_per_hour` 0,02 por cada 0,02 que gasta una unidad |
| Una zona con 3 recursos | unas **72 por día** | |

| Porcentaje | Por zona y día | Pueblo (9 zonas) | Castillo (25 zonas) | Reino (81 zonas) |
|---|---|---|---|---|
| **40 %** (lo que dijo el dueño) | ~29 | ~260 | ~720 (lo de 9 jugadores) | ~2.300 |
| **20 %** (recomendado) | ~14 | ~130 | ~360 (lo de 4 o 5 jugadores) | ~1.150 |

Con 40 activos recolectando (unas 3.200 unidades por día), la cosecha del castillo suma un **11 %** al 20 %, y un **22 %** al 40 %.

### 5.4 La recomendación de Claude (P-227, P-228 y P-229)

1. **Empezar con 20 %** y medir en la beta. Es más fácil subirlo después que bajarlo: a nadie le gusta que le quiten.
2. **La cosecha va al 📦 almacén del asentamiento,** no a la mochila de nadie. Sirve para las obras, la muralla, las reparaciones y la comida de los aldeanos. Así lo pide D-195: las mejoras producen "para el castillo, no para los jugadores".
3. **Solo cosecha si el asentamiento tuvo jugadores activos esa semana,** y se junta como mucho **7 días**. Un asentamiento abandonado no se llena solo.
4. **Reemplaza el +50 % de hoy** al recolectar en tu propio territorio (D-87, `gather.own_land_bonus: 1.5`), para no sumar dos bonos y para cumplir D-239.3, que dice "nada de bonos de farmeo aparte".
5. **La cosecha sale de lo que vuelve a crecer, no del recurso que hay:** el que recolecta a mano en esa zona encuentra lo mismo que hoy.

## 6. Dónde no se crea grupo (D-252)

- **En la fogata de salida no se crea grupo.** Eso vale para el Claro y, cuando existan, para las hogueras de inicio (D-224, D-239.10).
- **El grupo nace cuando un jugador construye él mismo.** Cómo se leyó (D-256, provisional): levantar uno mismo la 🏠 casa de D-158 y, mientras la casa no exista en el juego, fundar el campamento. Aportar a la obra de otro no crea grupo.
- **Hoy ya se cumple sola:** no se puede fundar dentro del territorio del Claro ni a Lejanía menor que 2. Hay que mantenerla cuando lleguen los grupos y la casa.
- **Cambia D-246.2** ("cualquiera puede invitar desde el principio"): desde ahora invitan el líder y los oficiales, y recién desde la primera construcción.

## 7. Qué cambia del juego de hoy (cuando se programe)

| Hoy (0.33) | Con la escalera |
|---|---|
| Cupo del campamento 2 + 2 por nivel; el del gremio, 4 a 30; gana el mayor (`_members_cap`) | Un solo cupo por etapa: 5, 10, 15, 25, 40, 50, 80, 120, 160 y 200 |
| Solo el fundador acepta (`_answer_join`, D-84) | El líder y los oficiales |
| Nadie sale si no quiere (regla 10) | Sale a los 30 días sin jugar |
| Castillo: gremio de nivel 5 con 10 miembros, 15 mejoras y la Noche (`_castle_needs`) | 40 activos, la Noche con 10 vencedores distintos y 5 oleadas crecientes (D-122) |
| Cada nivel suma 1 zona, sin tope (D-81, `_grow_camp`) | Las zonas de muralla de cada etapa (P-229) |
| +50 % al recolectar en tu territorio (`gather.own_land_bonus`) | La tierra cosecha sola para el asentamiento (P-227, P-228) |
| No hay grupos | Grupo de 5 que nace al construir; escuadras dentro del gremio |

**Los jugadores de hoy no pierden nada (D-64):**
- cada campamento queda en la etapa que le corresponde por sus miembros y sus mejoras, nunca en una más baja;
- cada miembro de hoy sigue adentro;
- las zonas que ya tiene se quedan aunque pasen el tope de su etapa.

## 8. Red de sistemas

- **Consume:**
  - jugadores activos (para subir de etapa y para la Noche);
  - materiales (obras, muralla y mantenimiento);
  - defensa (oleadas que le pegan a la muralla).
- **Produce:**
  - lugar para más gente;
  - cargos;
  - territorio que cosecha para el almacén;
  - control de nodos y peaje (D-236);
  - motivos de conflicto entre asentamientos (la tierra de alrededor).
- **Amplio pero ligero (D-44):**
  - la capa simple es "construyes tu casa, invitas a 4 y crecen";
  - las escuadras, los cargos y la muralla aparecen recién cuando el asentamiento las necesita (cargos en el pueblo, muralla con zonas desde el campamento).

## 9. Preguntas abiertas

- **P-227 (E-216):** cuánto cosecha cada zona y a dónde va. Recomendado: 20 %, al almacén, con actividad y con tope de 7 días.
- **P-228 (E-217):** si la cosecha reemplaza el +50 % de hoy. Recomendado: sí.
- **P-229 (E-218):** cuántas zonas cierra la muralla por etapa. Recomendado: la tabla del §2.
- **Siguen de antes:**
  - P-224, la Academia o la Biblioteca;
  - P-79 / E-56, las oleadas del castillo;
  - P-82 / E-59, el monarca;
  - P-112 / E-89, la fusión de grupos;
  - P-97 / E-74, el tope diario por zona.

## De dónde sale

- **La escalera de etapas con un solo cupo:** las ciudades de Chat Wars y los niveles de clan de Clash of Clans, donde un número dice cuánta gente cabe.
- **Las escuadras de 5 y los cargos:** los grupos de 5 y los rangos de gremio de World of Warcraft (líder, oficiales, miembros), y los escuadrones de EVE Online.
- **La muralla que marca el territorio y crece por anillos:** el territorio de alianza de Rise of Kingdoms, que se agranda con banderas y fortalezas.
- **La tierra que produce sola:** los campos de recursos de Travian, que producen cada hora sin que nadie los trabaje. También las granjas de alianza de Rise of Kingdoms, que juntan recursos para la alianza, no para un jugador.
- **Liberar el lugar de quien no juega:** la regla de TowerWars de sacar a los inactivos (allí, a los 14 días; aquí, a los 30, como pidió el dueño).
